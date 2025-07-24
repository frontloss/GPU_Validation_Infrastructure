#######################################################################################################################
# @file         psr.py
# @brief        Contains PSR verification APIs
#
# @author       Rohit Kumar
#######################################################################################################################

import ctypes
import logging
import math
import os
import subprocess
import sys
import time
from datetime import datetime
from enum import IntEnum
from multiprocessing import Process, Queue

from Libs.Core.wrapper import control_api_args, control_api_wrapper

from Libs.Core import registry_access, display_essential, etl_parser, window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Core.vbt import vbt
from Libs.Feature.powercons import registry
from Tests.Planes.Common import planes_verification
from Tests.PowerCons.Functional.BLC import blc
from Tests.PowerCons.Functional.PSR import pr
from Tests.PowerCons.Functional.PSR import psr_util
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Modules import common, dpcd, dut, windows_brightness, state_machine as sm
from registers.mmioregister import MMIORegister

__FRAME_UPDATE_PATH = os.path.join(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "PowerCons"), "FrameUpdate.exe")
__PRE_SI_FRAME_COUNTER_UPDATE_TIMEOUT = 100  # 30 times
__PRE_SI_POLLING_DELAY = 30  # 30 seconds
__PRE_SI_FRAME_UPDATE_MAX = 8  # Wait for 8 frames before closing the psr util app
DEFAULT_MEDIA_FPS = 24
DEFAULT_PLAYBACK_DURATION = 30
DEFAULT_POLLING_DELAY = 0.01  # 10 ms
DEEP_SLEEP_STATE = 0x8

display_config_ = DisplayConfiguration()

##
# @brief        Helper dictionary for wake lines
WAKE_LINES = {
    5: 0x0,
    6: 0x1,
    7: 0x2,
    8: 0x3,
    9: 0x4,
    10: 0x5,
    11: 0x6,
    12: 0x7
}

##
# @brief        Helper dictionary for wake lines for Gen13 platforms
WAKE_LINES_GEN13 = {
    5: 0x2,
    6: 0x1,
    7: 0x0,
    8: 0x3,
    9: 0x6,
    10: 0x5,
    11: 0x4,
    12: 0x7
}
# PSR setup time in Micro secs
PSR_SETUP_TIME = {
    0: 330,
    1: 275,
    2: 220,
    3: 165,
    4: 110,
    5: 55,
    6: 0
}


##
# @brief        Helper object class for VSC DB16 pixel encoding formats
class SDP_DB16_PIXEL_ENCODING(IntEnum):
    RGB = 0
    YUV_444 = 1
    YUV_422 = 2
    YUV_420 = 3
    Y_ONLY = 4
    RAW = 5
    RESERVED = 6


##
# @brief        Helper object class for VSC DB16 RGB colorimetry formats
class SDP_RGB_COLORIMETRY_FORMAT(IntEnum):
    S_RGB = 0
    RGB_WIDE_GAMUT_FIXED_POINT = 1
    RGB_WIDE_GAMUT_FLOATING_POINT = 2
    ADOBE_RGB = 3
    DCI_P3 = 4
    CUSTOM_COLOR_PROFILE = 5
    ITU_R_BT_2020_RGB = 6
    RESERVED = 7


##
# @brief        Helper object class for VSC DB16 YUV colorimetry formats
class SDP_YUV_COLORIMETRY_FORMAT(IntEnum):
    ITU_R_BT_601 = 0
    ITU_R_BT_709 = 1
    XV_YCC_601 = 2
    XV_YCC_709 = 3
    S_YCC_601 = 4
    OP_YCC_601 = 5
    ITU_R_BT_2020_YC_CBC_CRC = 6
    ITU_R_BT_2020_Y_CB_CR = 7
    RESERVED = 8


##
# @brief        Helper object class for VSC DB17 Dynamic Range support
class SDP_DB17_DYNAMIC_RANGE_TYPE(IntEnum):
    VESA_RANGE = 0
    CTA_RANGE = 1


SDP_DB17_BPC_Type = {
    0: 6,  # only for RGB pixel encoding formats
    1: 8,
    2: 10,
    3: 12,
    4: 16
}


##
# @brief        Helper object class for VSC DB18 content type
class SDP_DB18_CONTENT_TYPE(IntEnum):
    NOT_DEFINED = 0
    GRAPHICS = 1
    PHOTO = 2
    VIDEO = 3
    GAME = 4
    RESERVED = 5  # all other values are reserved


##
# @brief        Helper object class for PSR block count
class PSR_BLOCK_COUNT_NUMBER(IntEnum):
    BLOCK_COUNT_NUMBER_2_BLOCKS = 0x0
    BLOCK_COUNT_NUMBER_3_BLOCKS = 0x1


##
# @brief        Helper object class for valid y co ordinates
class YCOORDINATE_VALID(IntEnum):
    INCLUDE_YCOORDINATE_VALID_EDP1_4A = 0x0
    DO_NOT_INCLUDE_YCOORDINATE_VALID_EDP_1_4 = 0x1


##
# @brief        Helper object class for aux frame sync
class AUX_FRAME_SYNC_ENABLE(IntEnum):
    AUX_FRAME_SYNC_ENABLE = 0x1
    AUX_FRAME_SYNC_DISABLE = 0x0


##
# @brief        Exposed enum class for user requested features
class UserRequestedFeature(IntEnum):
    PSR_NONE = 0
    PSR_1 = 1
    PSR_2 = 2
    PSR2_FFSU = 3
    PSR2_SFSU = 4
    PANEL_REPLAY = 5
    MAX = 6

    @staticmethod
    ##
    # @brief        This functions gives the  enum value of the user requested feature
    # @param[in]    feature
    # @return       Enum value of user requested feature
    def by_str(feature):
        return {'PSR1': UserRequestedFeature.PSR_1, 'PSR2': UserRequestedFeature.PSR_2,
                'PSR2_FFSU': UserRequestedFeature.PSR2_FFSU, 'PSR2_SFSU': UserRequestedFeature.PSR2_SFSU,
                'PANEL_REPLAY': UserRequestedFeature.PANEL_REPLAY
                }.get(feature, None)


##
# @brief        Helper object class for PSR state machine inputs
class PsrInputs(object):
    FRAME_UPDATE = "FrameUpdate"
    MMIO_PSR_ENTRY = "MmioPsrEntry"
    MMIO_PSR_EXIT = "MmioPsrExit"
    MMIO_SLEEP = "MmioSleep"
    MMIO_DEEP_SLEEP = "MmioDeepSleep"
    MMIO_SELECTIVE_UPDATE = "MmioSelectiveUpdate"


##
# @brief        State machine for PSR1 verification
class Psr1StateMachine(sm.StateMachine):
    psr_entry = sm.State("PSR_ENTRY")
    psr_exit = sm.State("PSR_EXIT")
    frame_update = sm.State("FRAME_UPDATE")

    psr_entry_count = 0
    consecutive_psr_exit_count = 0
    result = True

    ##
    # @brief        Defines the transition table and initialize the state machine
    # @param[in]    initial_state State, an object of type State class indicating the starting state of the machine
    # @param[in]    time_stamp datetime, an object of type datetime indicating the time stamp of initial state
    def __init__(self, initial_state, time_stamp):
        self.transition_table = [
            #####################################################################################################
            #                                   Transition Table                                                #
            #####################################################################################################
            # |CurrentState     |Input                   | Test | TransitionFunction             | NextState    |
            #####################################################################################################
            [self.psr_entry, PsrInputs.MMIO_PSR_ENTRY, None, None, self.psr_entry],
            [self.psr_entry, PsrInputs.MMIO_PSR_EXIT, None, None, self.psr_exit],
            [self.psr_entry, PsrInputs.FRAME_UPDATE, None, None, self.frame_update],
            [self.frame_update, PsrInputs.MMIO_PSR_EXIT, None, self.transition, self.psr_exit],
            [self.psr_exit, PsrInputs.MMIO_PSR_EXIT, None, self.transition, self.psr_exit],
            [self.psr_exit, PsrInputs.MMIO_PSR_ENTRY, None, self.transition, self.psr_entry],
            [self.psr_exit, PsrInputs.FRAME_UPDATE, None, None, self.frame_update]
        ]

        ##
        # Initialize state machine
        super(Psr1StateMachine, self).__init__(initial_state, self.transition_table)

    ##
    # @brief        This function checks the transition of PSR
    # @param[in]    current_state State, an object of type State class indicating the current state of the machine
    # @param[in]    next_state State, an object of type State class indicating the next state of the machine
    # @param[in]    state_input
    # @return       None
    def transition(self, current_state, next_state, state_input):
        if current_state.name == self.psr_exit.name and next_state.name == self.psr_entry.name:
            self.psr_entry_count += 1

        if current_state.name == self.psr_exit.name and next_state.name == self.psr_exit.name:
            self.consecutive_psr_exit_count += 1
            if self.consecutive_psr_exit_count > 8:
                logging.debug("\tTransition: PSR_EXIT -> PSR_ENTRY didn't occur ever after {0} inputs".format(
                    self.consecutive_psr_exit_count))
        else:
            self.consecutive_psr_exit_count = 0

        if current_state.name == self.psr_entry.name and next_state.name == self.psr_exit.name:
            logging.warning("\tPSR_EXIT happened without frame update")


##
# @brief        State machine for PSR2 verification
class Psr2StateMachine(sm.StateMachine):
    psr_exit = sm.State("PSR_EXIT")
    deep_sleep = sm.State("DEEP_SLEEP")
    sleep = sm.State("SLEEP")
    selective_update = sm.State("SELECTIVE_UPDATE")
    exit_frame_update = sm.State("EXIT_FRAME_UPDATE")
    frame_update = sm.State("FRAME_UPDATE")

    sleep_count = 0
    deep_sleep_count = 0
    selective_update_count = 0
    result = True

    ##
    # @brief        Defines the transition table and initialize the state machine
    # @param[in]    initial_state State, an object of type State class indicating the starting state of the machine
    # @param[in]    time_stamp datetime, an object of type datetime indicating the time stamp of initial state
    def __init__(self, initial_state, time_stamp):
        self.transition_table = [
            #####################################################################################################
            #                                   Transition Table                                                #
            #####################################################################################################
            # |CurrentState     |Input                   | Test | TransitionFunction             | NextState    |
            #####################################################################################################
            [self.psr_exit, PsrInputs.MMIO_PSR_EXIT, None, None, self.psr_exit],
            [self.psr_exit, PsrInputs.MMIO_SLEEP, None, self.transition, self.sleep],
            [self.psr_exit, PsrInputs.FRAME_UPDATE, None, None, self.exit_frame_update],
            [self.psr_exit, PsrInputs.MMIO_SELECTIVE_UPDATE, None, self.transition, self.selective_update],
            [self.sleep, PsrInputs.MMIO_SLEEP, None, None, self.sleep],
            [self.sleep, PsrInputs.MMIO_DEEP_SLEEP, None, self.transition, self.deep_sleep],
            [self.sleep, PsrInputs.MMIO_PSR_EXIT, None, self.transition, self.psr_exit],
            [self.sleep, PsrInputs.FRAME_UPDATE, None, None, self.frame_update],
            [self.frame_update, PsrInputs.MMIO_SELECTIVE_UPDATE, None, self.transition, self.selective_update],
            [self.selective_update, PsrInputs.MMIO_SLEEP, None, self.transition, self.sleep],
            [self.selective_update, PsrInputs.MMIO_DEEP_SLEEP, None, self.transition, self.deep_sleep],
            [self.deep_sleep, PsrInputs.FRAME_UPDATE, None, None, self.exit_frame_update],
            [self.deep_sleep, PsrInputs.MMIO_DEEP_SLEEP, None, None, self.deep_sleep],
            [self.deep_sleep, PsrInputs.MMIO_SLEEP, None, self.transition, self.sleep],
            [self.deep_sleep, PsrInputs.MMIO_PSR_EXIT, None, self.transition, self.psr_exit],
            [self.exit_frame_update, PsrInputs.MMIO_PSR_EXIT, None, None, self.psr_exit],
            [self.exit_frame_update, PsrInputs.FRAME_UPDATE, None, self.transition, self.sleep]
        ]

        ##
        # Initialize state machine
        super(Psr2StateMachine, self).__init__(initial_state, self.transition_table)

    ##
    # @brief        This function checks the transition of PSR
    # @param[in]    current_state State, an object of type State class indicating the current state of the machine
    # @param[in]    next_state State, an object of type State class indicating the next state of the machine
    # @param[in]    state_input
    # @return       None
    def transition(self, current_state, next_state, state_input):
        if current_state.name == self.psr_exit.name and next_state.name == self.sleep.name:
            self.sleep_count += 1

        if current_state.name == self.selective_update.name and next_state.name == self.sleep.name:
            self.sleep_count += 1

        if current_state.name == self.frame_update.name and next_state.name == self.selective_update.name:
            self.selective_update_count += 1

        if current_state.name == self.selective_update.name and next_state.name == self.deep_sleep.name:
            self.deep_sleep_count += 1

        ##
        # Sleep
        if current_state.name == self.sleep.name:
            if next_state.name == self.deep_sleep.name:
                self.deep_sleep_count += 1

            if next_state.name == self.psr_exit.name:
                logging.warning("\tPSR_EXIT happened without frame update")

        # Deep Sleep
        if current_state.name == self.deep_sleep.name:
            if next_state.name == self.sleep.name:
                self.sleep_count += 1

            if next_state.name == self.psr_exit.name:
                logging.warning("\tPSR_EXIT happened without frame update")

        if current_state.name == self.psr_exit.name and next_state.name == self.selective_update.name:
            self.selective_update_count += 1
            logging.warning("\tSELECTIVE_UPDATE happened without frame update")


##
# @brief        Exposed API to enable PSR in driver
# @param[in]    gfx_index string, gfx_0, gfx_1
# @param[in]    psr_version UserRequestedFeature, PSR version to be enabled
# @return       status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise
def enable(gfx_index, psr_version):
    assert psr_version in [UserRequestedFeature.PSR_1, UserRequestedFeature.PSR_2, UserRequestedFeature.PSR2_FFSU,
                           UserRequestedFeature.PSR2_SFSU, UserRequestedFeature.PANEL_REPLAY]

    # HSD -18013883922 WA - Delete reg key to avoid PSR disable due to PowerPlan settings set by previous Non-PSR Panel
    pwr_plan_val = registry.delete(gfx_index, key=registry.RegKeys.POWER_PLAN_AWARE_SETTINGS)
    feature_test_control = registry.FeatureTestControl(gfx_index)
    psr_status = None
    if feature_test_control.psr_disable != 0:
        feature_test_control.psr_disable = 0
        psr_status = feature_test_control.update(gfx_index)
        if psr_status is False:
            logging.error("\tFAILED to update FeatureTestControl registry")
            return False
    logging.info(f"\tPASS: {'User setting for PSR':<40} Expected= ENABLED, Actual= ENABLED")

    psr_ac = registry.write(gfx_index, registry.RegKeys.PSR.PSR_DISABLE_IN_AC, registry_access.RegDataType.DWORD, 0x0)
    if psr_ac is False:
        logging.error(f"\tFAILED to update {registry.RegKeys.PSR.PSR_DISABLE_IN_AC} registry")
        return False
    logging.info(f"\tPASS: {'User setting for PSR in AC':<40} Expected= ENABLED, Actual= ENABLED")

    psr2_dis = None
    sfsu_ffsu = None
    pr_status = None
    if psr_version >= UserRequestedFeature.PSR_2:
        psr2_dis = registry.write(gfx_index, registry.RegKeys.PSR.PSR2_DISABLE, registry_access.RegDataType.DWORD, 0x0)
        if psr2_dis is False:
            logging.error(f"\tFAILED to update {registry.RegKeys.PSR.PSR2_DISABLE} registry")
            return False
        if psr_version == UserRequestedFeature.PSR2_SFSU or psr_version == UserRequestedFeature.PSR2_FFSU:
            display_pc = registry.DisplayPcFeatureControl(gfx_index)
            if common.IS_PRE_SI:
                display_pc.DisableSelectiveFetch = 0
                sfsu_ffsu = display_pc.update(gfx_index)
                if sfsu_ffsu is False:
                    logging.error("\tFAILED to update DisplayPcFeatureControlFields registry")
                    return False
            else:
                if psr_version == UserRequestedFeature.PSR2_SFSU:
                    if display_pc.DisableSelectiveFetch != 0:
                        logging.error("Selective Fetch is disabled in DisplayPCFeatureControl")
                        return False
        if psr_version == UserRequestedFeature.PANEL_REPLAY:
            pr_status = pr.enable_for_efp(gfx_index)

    logging.info(f"\tPASS: User setting for {UserRequestedFeature(psr_version).name} Expected= ENABLED, Actual=ENABLED")
    return psr_status or psr2_dis or psr_ac or sfsu_ffsu or pwr_plan_val or pr_status


##
# @brief        Exposed API to disable PSR in driver
# @param[in]    gfx_index string, gfx_0, gfx_1
# @param[in]    psr_version UserRequestedFeature, PSR version to be disabled
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
def disable(gfx_index, psr_version):
    assert psr_version in [UserRequestedFeature.PSR_1, UserRequestedFeature.PSR_2, UserRequestedFeature.PSR2_FFSU,
                           UserRequestedFeature.PSR2_SFSU, UserRequestedFeature.PANEL_REPLAY]
    psr1 = None
    if psr_version == UserRequestedFeature.PSR_1:
        feature_test_control = registry.FeatureTestControl(gfx_index)
        if feature_test_control.psr_disable != 1:
            feature_test_control.psr_disable = 1
            psr1 = feature_test_control.update(gfx_index)
            if psr1 is False:
                logging.error("\tFAILED to update FeatureTestControl registry")
                return False

    psr2 = None
    pr_status = None
    if psr_version >= UserRequestedFeature.PSR_2:
        psr2 = registry.write(gfx_index, registry.RegKeys.PSR.PSR2_DISABLE, registry_access.RegDataType.DWORD, 0x1)
        if psr2 is False:
            logging.error(f"\tFAILED to update {registry.RegKeys.PSR.PSR2_DISABLE} registry")
            return False
    if psr_version == UserRequestedFeature.PANEL_REPLAY:
        pr_status = pr.disable_for_efp(gfx_index)
    logging.info(
        f"\tPASS: User setting for {UserRequestedFeature(psr_version).name} Expected= DISABLED, Actual= DISABLED")
    return psr1 or psr2 or pr_status


##
# @brief        Exposed API to check if given panel supports the given feature
# @param[in]    target_id Number target id of display
# @param[in]    feature Enum, UserRequestedFeature
# @return       True if given feature is supported by given panel, False if not supported, None in case of any error
def is_feature_supported_in_panel(target_id, feature):
    # Validate arguments
    if target_id < 1 or feature >= UserRequestedFeature.MAX:
        logging.error("\tInvalid arguments: target_id= {0}, feature= {1}".format(target_id, feature.name))
        return None

    # Get eDP DPCD version
    edp_dpcd_rev = dpcd.get_edp_revision(target_id)
    if edp_dpcd_rev is None or edp_dpcd_rev == dpcd.EdpDpcdRevision.EDP_UNKNOWN:
        logging.error("\tFailed to get eDP DPCD revision")
        return None

    # Check SET_POWER_CAPABLE
    # This bit must have a value of 1 if PSR is supported
    edp_general_caps = dpcd.EdpGeneralCapsReg(target_id)
    if edp_general_caps.set_power_capable != 1:
        logging.error("\tSET_POWER_CAPABLE bit is not set")
        return False

    # Get eDP supported PSR version
    edp_psr_version = dpcd.get_psr_version(target_id)
    if edp_psr_version is None or edp_psr_version == dpcd.EdpPsrVersion.EDP_PSR_UNKNOWN:
        logging.error("\tFailed to get eDP PSR version")
        return None

    if feature == UserRequestedFeature.PSR_1:
        # PSR1 is supported only on eDP 1.3+ panels
        if (edp_dpcd_rev < dpcd.EdpDpcdRevision.EDP_DPCD_1_3) or (edp_psr_version < dpcd.EdpPsrVersion.EDP_PSR_1):
            return False
    elif feature >= UserRequestedFeature.PSR_2:
        # PSR2 is supported only on eDP 1.4+ panels
        if (edp_dpcd_rev < dpcd.EdpDpcdRevision.EDP_DPCD_1_4) or (edp_psr_version < dpcd.EdpPsrVersion.EDP_PSR_2):
            return False

    return True


##
# @brief        Exposed API to check if given PSR version is enabled in driver or not
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    psr_version UserRequestedFeature
# @return       status Boolean, True, if enabled, False otherwise
def is_psr_enabled_in_driver(adapter, panel, psr_version):
    assert adapter
    assert panel
    assert psr_version in [UserRequestedFeature.PSR_1, UserRequestedFeature.PSR_2, UserRequestedFeature.PSR2_FFSU,
                           UserRequestedFeature.PSR2_SFSU, UserRequestedFeature.PANEL_REPLAY]
    psr_pr_status = False
    retry_count = 0
    while retry_count <= 2:
        if psr_version == UserRequestedFeature.PSR_1:
            srd_ctl_edp = MMIORegister.read(
                'SRD_CTL_REGISTER', 'SRD_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
            psr_pr_status = srd_ctl_edp.srd_enable == 1
        psr2_ctl_edp = MMIORegister.read(
            'PSR2_CTL_REGISTER', 'PSR2_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
        if UserRequestedFeature.PSR_2 <= psr_version < UserRequestedFeature.PANEL_REPLAY:
            if psr_version == UserRequestedFeature.PSR_2:
                psr_pr_status = psr2_ctl_edp.psr2_enable == 1
            logging.debug(" PSR2 Enable status = {0}".format("ENABLED" if psr2_ctl_edp.psr2_enable else "DISABLED"))
            psr2_man_trk = MMIORegister.read("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder,
                                             adapter.name, gfx_index=adapter.gfx_index)
            plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
            psr2_sel_fetch = MMIORegister.read("SEL_FETCH_PLANE_CTL_REGISTER", f"SEL_FETCH_PLANE_CTL_{plane_id}_{panel.pipe}",
                                               adapter.name, gfx_index=adapter.gfx_index)

            logging.debug("selective fetch status = {0}, Partial_frame_update = {1} ".format(
                "ENABLED" if psr2_sel_fetch.selective_fetch_plane_enable else "DISABLED",
                "ENABLED" if psr2_man_trk.sf_partial_frame_enable else "DISABLED"))
            if psr_version == UserRequestedFeature.PSR2_SFSU:
                psr_pr_status = psr2_ctl_edp.psr2_enable == 1 and psr2_man_trk.sf_partial_frame_enable == 1 \
                    and psr2_sel_fetch.selective_fetch_plane_enable == 1
            elif psr_version == UserRequestedFeature.PSR2_FFSU:
                psr_pr_status = psr2_ctl_edp.psr2_enable == 1 and psr2_man_trk.sf_partial_frame_enable == 1
        elif psr_version == UserRequestedFeature.PANEL_REPLAY:
            psr_pr_status = pr.is_enabled_in_driver(adapter, panel)
        if panel.psr_caps.early_transport_supported or panel.pr_caps.early_transport_supported:
            psr_pr_status &= (psr2_ctl_edp.enable_early_transport == 1)
        if psr_pr_status:
            break
        retry_count += 1
        time.sleep(1.5)
    return psr_pr_status


##
# @brief        Exposed API to check if Psr2 entered deep sleep state
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       status Boolean, True, if entered deep sleep, False otherwise
def verify_deep_sleep(adapter, panel):
    if not (panel.psr_caps.is_psr2_supported or panel.pr_caps.is_pr_supported):
        logging.error(f"PSR2/PR is not supported on {panel}")
        return False
    if adapter.name in common.GEN_12_PLATFORMS and panel.pipe == 'B':
        logging.info(f"PSR2 not supported on PIPE_{panel.pipe} on {panel.port}")
        return False
    # Hiding the task-bar to make sure that there's no update on screen
    logging.info("STEP: Hiding the task-bar")
    assert window_helper.toggle_task_bar(window_helper.Visibility.HIDE), "FAILED to hide the task-bar"
    logging.info("\tSuccessfully hide the task-bar")

    # Start ETL Tracer if not started
    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return False

    # 30 sec Sleep to make sure PSR enters deep sleep state
    time.sleep(30)

    # Stop ETL Tracer
    if etl_tracer.stop_etl_tracer() is False:
        logging.error("\tFailed to stop ETL Tracer(Test Issue)")
        return False
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
        logging.error(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")
        return False
    file_name = 'GfxTrace_DeepSleep.' + str(time.time()) + '.etl'
    etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
    os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    dc_state_data = etl_parser.get_event_data(etl_parser.Events.DC_STATE_DATA)
    if dc_state_data is None:
        logging.error("No DC state data found in ETL")
        return False
    for entry in range(len(dc_state_data)):
        if dc_state_data[entry].DcStateRequested in ['DC6', 'DC_PWR_STATE_SET_UPTO_DC6']:
            logging.info(f"PSR2 Entered Deep Sleep state for {panel.port}")
            return True
    logging.error(f"PSR2 did not enter Deep Sleep state for {panel.port}")
    return False


##
# @brief        Exposed API to check if Psr2 is disabled or not before driver disable
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    etl_file string path to the etl file
# @param[in]    h_total register instance
# @param[in]    v_total register instance
# @return       status Boolean, True, if disabled, False otherwise
def verify_psr2_disable(adapter, panel, etl_file, h_total, v_total):
    if not panel.psr_caps.is_psr2_supported:
        logging.error("PSR2 is not supported on {}".format(panel))
        return False
    etl_parser.generate_report(etl_file)
    ##
    # This is called by OS to stop the device, release all resources
    #  and transfer the display ownership to OS
    driver_disable = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_STOP_DEVICE_AND_RELEASE_POST_DISPLAY_OWNERSHIP)

    psr2_ctl = MMIORegister.get_instance("PSR2_CTL_REGISTER", "PSR2_CTL_" + panel.transcoder, adapter.name)
    psr2_val = etl_parser.get_mmio_data(psr2_ctl.offset, is_write=True)
    if driver_disable:
        for val in psr2_val:
            psr2_ctl.asUint = val.Data
            if psr2_ctl.psr2_enable == 0 and val.TimeStamp < driver_disable[0].StartTime:
                logging.info("PSR2 disabled before driver disable at {}".format(val.TimeStamp))
                break
    else:
        logging.error("DDI STOP DEVICE call not found in ETL")
        return False
    status = verify_psr2_pr_disable_sequence(adapter, panel, etl_file, h_total, v_total)
    return status


##
# @brief        Exposed API to verify Psr2 enable sequence
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    etl_file string, path of etl file
# @return       status Boolean, True, if disabled, False otherwise
def verify_psr2_pr_enable_sequence(adapter, panel, etl_file):
    man_trk = None
    sel_fetch = None
    psr2_enable_time = 0
    plane_enable_time = 0
    status = True
    edp_rev = 0
    psr_caps = 0
    psr_enable_in_sink = False
    psr2_ctl_val = None

    video_dip_ctl = MMIORegister.get_instance('VIDEO_DIP_CTL_REGISTER', 'VIDEO_DIP_CTL_' + panel.transcoder,
                                              adapter.name)
    etl_parser.generate_report(etl_file)
    dip_ctl = etl_parser.get_mmio_data(video_dip_ctl.offset)
    if dip_ctl is None:
        logging.error(f"VIDEO_DIP_CTL_{panel.transcoder} data not found")
        return False
    if panel.pr_caps.is_pr_supported:
        status = pr.verify_pr_enable_sequence(adapter, panel)
        status &= verify_sdp_data(adapter, panel, video_dip_ctl, dip_ctl, enable_check=True)
        return status
    if not panel.psr_caps.is_psr2_supported:
        logging.error("PSR2 is not supported on {}".format(panel))
        return False
    if not panel.psr_caps.is_psr2_supported:
        logging.error(f"PSR2 is not supported on {panel}")
        return False

    psr2_ctl = MMIORegister.get_instance("PSR2_CTL_REGISTER", "PSR2_CTL_" + panel.transcoder, adapter.name)
    plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
    plane_ctl = MMIORegister.get_instance("PLANE_CTL_REGISTER", "PLANE_CTL_" + str(plane_id) + "_" + panel.pipe, adapter.name)
    h_total_instance = MMIORegister.get_instance("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + panel.transcoder,
                                                 adapter.name)
    psr2_man_trk = MMIORegister.get_instance("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder,
                                             adapter.name)
    plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
    psr2_sel_fetch = MMIORegister.get_instance("SEL_FETCH_PLANE_CTL_REGISTER", f"SEL_FETCH_PLANE_CTL_{plane_id}_{panel.pipe}",
                                               adapter.name)
    alpm_ctl_reg = None
    # Fast wake line programming will happen in ALPM CTL Register from Gen15 onwards
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        alpm_ctl_reg = MMIORegister.get_instance("ALPM_CTL_REGISTER", "ALPM_CTL_" + panel.transcoder, adapter.name)
        alpm_ctl_val = etl_parser.get_mmio_data(alpm_ctl_reg.offset, is_write=True)
        if alpm_ctl_val is None:
            logging.error(f"ALPM_CTL_{panel.transcoder} data not found")
            return False
        alpm_ctl_reg.asUint = alpm_ctl_val[-1].Data

    aux = 'AUX_CHANNEL_' + panel.port.split('_')[1]
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        psr2_val = etl_parser.get_mmio_data(psr2_ctl.offset, is_write=True)
    else:
        # from GEN14+, Driver will write first 16 bits & last 16 bit's separately to avoid synchronization issues
        psr2_ctl_val = etl_parser.get_mmio_data(psr2_ctl.offset, is_write=True)
        psr2_val = etl_parser.get_mmio_data(0x60902, is_write=True)
    plane_data = etl_parser.get_mmio_data(plane_ctl.offset)
    if psr2_val is None:
        logging.error(f"PSR2_CTL_{panel.transcoder} data not found")
        return False
    if adapter.name not in common.PRE_GEN_12_PLATFORMS:
        man_trk = etl_parser.get_mmio_data(psr2_man_trk.offset)
        if man_trk is None:
            logging.error(f"PSR2_MAN_TRK_CTL_{panel.transcoder} data not found")
            return False
        sel_fetch = etl_parser.get_mmio_data(psr2_sel_fetch.offset)
        if sel_fetch is None:
            logging.error(f"SEL_FETCH_PLANE_CTL_{panel.pipe} data not found")
            return False
        dip_ctl = etl_parser.get_mmio_data(video_dip_ctl.offset)
        if dip_ctl is None:
            logging.error(f"VIDEO_DIP_CTL_{panel.transcoder} data not found")
            return False

    for val in plane_data:
        plane_ctl.asUint = val.Data
        if plane_ctl.plane_enable:
            logging.info(f"Plane{panel.pipe} is enabled at {val.TimeStamp}")
            plane_enable_time = val.TimeStamp
            break
    # No need to proceed if plane is not enabled
    if plane_enable_time == 0:
        logging.error(f"Plane{panel.pipe} is not enabled")
        status = False
    h_total_data = etl_parser.get_mmio_data(h_total_instance.offset)
    if h_total_data:
        h_total_instance.asUint = h_total_data[-1].Data
    else:
        logging.error("TRANS_HTOTAL_{} data not found".format(panel.transcoder))
        status = False
    # Get DPCD data from ETL to make sure driver reads below DPCD's
    # driver reads 5 bytes 700-704h in a single read
    edp_rev_details = etl_parser.get_dpcd_data(dpcd.Offsets.DPCD_VER, channel=aux)
    if edp_rev_details:
        # DPCD json data will be in format - '04-82-00-00-00'
        # get Byte 0 (700h) value
        edp_rev = int(edp_rev_details[-1].Data.split('-')[0], 16)
    else:
        logging.error("driver did not read panel EDP revision")
        status = False
    # driver reads 5 bytes 70-74h in a single read
    psr_ver_data = etl_parser.get_dpcd_data(dpcd.Offsets.PSR_CAPS_SUPPORTED_AND_VERSION, channel=aux)
    if psr_ver_data:
        data = psr_ver_data[-1].Data.split('-')
        psr_ver = int(data[0], 16)
        if psr_ver < dpcd.EdpPsrVersion.EDP_PSR_2:
            logging.error(f"Expected PSR version from panel = {dpcd.EdpPsrVersion.EDP_PSR_2.value} Actual = {psr_ver}")
            status = False
        psr_caps = int(data[1], 16)
    else:
        logging.error("driver did not read panel PSR Version(0x70h) DPCD")
        status = False
    logging.info("Panel native pixel clock value = {}".format(panel.native_mode.pixelClock_Hz))
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        psr2_ctl.asUint = psr2_val[-1].Data
    else:
        psr2_ctl.asUint = psr2_ctl_val[-1].Data + (psr2_val[-1].Data << 16)
    if __verify_su_wake_line_time(adapter, panel, h_total_instance, psr2_ctl, alpm_ctl_reg) is False:
        status = False
    psr_conf = etl_parser.get_dpcd_data(dpcd.Offsets.PSR_CONFIGURATION, channel=aux)
    if psr_conf is None:
        logging.error("DPCD 0x170H data not found")
        return False
    psr_configuration = dpcd.SinkPsrConfiguration(panel.target_id)
    for dpcd_data in psr_conf:
        if not dpcd_data.IsWrite:
            continue
        psr_configuration.value = int(dpcd_data.Data.split('-')[0], 16)
        if psr_configuration.psr_enable_in_sink:
            psr_enable_in_sink = True
            break
    if psr_enable_in_sink is False:
        logging.error("driver did not enable psr in sink")
        gdhm.report_driver_bug_pc("[PowerCons][PSR] Driver did not enable PSR2 in sink")
        return False
    logging.info("PSR enabled in sink DPCD (0x170h)")
    if edp_rev >= dpcd.EdpDpcdRevision.EDP_DPCD_1_4 and (psr_caps >> 4 & 1):
        # drive reads two bytes (0x2E-2Fh) in a single read
        # aux_frame_sync_support bit is removed from Gen-14 onwards
        if adapter.name in common.PRE_GEN_14_PLATFORMS:
            aux_frame_sync_support = etl_parser.get_dpcd_data(dpcd.Offsets.ALPM_CAP, channel=aux)
            if aux_frame_sync_support:
                aux_frame_sync = (int(aux_frame_sync_support[-1].Data.split('-')[1], 16) & 0x1) == 0x1
                logging.info("Aux frame sync support on panel = {}".format(aux_frame_sync))
            else:
                logging.error("driver did not read panel aux_frame_sync_support")
                status = False
        if adapter.name in common.PRE_GEN_13_PLATFORMS and \
                (not (
                        psr2_ctl.y_coordinate_enable and psr2_ctl.y_coordinate_valid == YCOORDINATE_VALID.INCLUDE_YCOORDINATE_VALID_EDP1_4A)):
            logging.error("driver did not programmed y co-ordinate value")
            status = False

        # aux_frame_sync_enable field is not applicable for Post Gen-14 platforms
        if adapter.name in common.PRE_GEN_14_PLATFORMS:
            if psr2_ctl.aux_frame_sync_enable == AUX_FRAME_SYNC_ENABLE.AUX_FRAME_SYNC_ENABLE:
                logging.error("driver did not disable Aux_Frame_sync when EDP 1.4 Panel is connected")
                status = False
    if not psr2_ctl.psr2_enable:
        logging.error("PSR2 not enabled by driver on {}".format(panel))
        status = False
    for val in psr2_val:
        if adapter.name in common.PRE_GEN_14_PLATFORMS:
            psr2_ctl.asUint = val.Data
        else:
            psr2_ctl.asUint = val.Data << 16
        if psr2_ctl.psr2_enable:
            psr2_enable_time = val.TimeStamp
            break
    if plane_enable_time > psr2_enable_time:
        logging.error("PSR2 is enabled before plane enable")
        status = False
    if adapter.name in common.PRE_GEN_13_PLATFORMS:
        if not psr2_ctl.selective_update_tracking_enable:
            logging.error("PSR2 selective update tracking not enabled by driver on {}".format(panel))
            status = False
    if adapter.name not in common.PRE_GEN_12_PLATFORMS:
        ##
        # Manual tracking is not supported on PIPE B on Gen12 Platforms
        if adapter.name in common.GEN_12_PLATFORMS and panel.pipe == 'B':
            logging.info("SKIP : Manual tracking check on PIPE B for {}".format(adapter.name))
        else:
            psr2_man_trk.asUint = man_trk[-1].Data
            psr2_sel_fetch.asUint = sel_fetch[-1].Data
            if psr2_man_trk.sf_partial_frame_enable != 1:
                logging.error("Manual tracking is not enabled by driver")
                status = False
            logging.info("Manual tracking is enabled in driver")
            if psr2_sel_fetch.selective_fetch_plane_enable != 1:
                logging.error("Selective Fetch is not enabled by driver on Plane_1_" + panel.transcoder)
                status = False
            logging.info("Selective Fetch is enabled by driver on Plane_1_" + panel.transcoder)
    status &= check_clk_gate_wa(adapter, panel, psr2_enable_time)
    status &= verify_sdp_data(adapter, panel, video_dip_ctl, dip_ctl, True)
    return status


##
# @brief        Exposed API to verify Psr2 enable sequence
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    etl_file string path to etl file
# @param[in]    h_total register instance
# @param[in]    v_total register instance
# @param[in]    check_idle_status Boolean True to check PSR2 Idle status, False to skip
# @return       status Boolean, True, if disabled, False otherwise
def verify_psr2_pr_disable_sequence(adapter, panel, etl_file, h_total, v_total, check_idle_status=True):
    status = True
    man_trk = None
    sel_fetch = None
    psr2_disable_time = None
    plane_disable_time = 0
    psr_disable_in_sink = False

    video_dip_ctl = MMIORegister.get_instance('VIDEO_DIP_CTL_REGISTER', 'VIDEO_DIP_CTL_' + panel.transcoder,
                                              adapter.name)
    etl_parser.generate_report(etl_file)
    dip_ctl = etl_parser.get_mmio_data(video_dip_ctl.offset)
    if dip_ctl is None:
        logging.error(f"VIDEO_DIP_CTL_{panel.transcoder} data not found")
        return False
    if panel.pr_caps.is_pr_supported:
        status = pr.verify_pr_disable_sequence(adapter, panel, h_total, v_total)
        status &= verify_sdp_data(adapter, panel, video_dip_ctl, dip_ctl)
        return status
    if not panel.psr_caps.is_psr2_supported:
        logging.error("PSR2 is not supported on {}".format(panel))
        return False

    psr2_ctl = MMIORegister.get_instance("PSR2_CTL_REGISTER", "PSR2_CTL_" + panel.transcoder, adapter.name)
    psr2_status = MMIORegister.get_instance("PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder, adapter.name)
    psr2_man_trk = MMIORegister.get_instance("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder,
                                             adapter.name)
    plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
    plane_ctl = MMIORegister.get_instance("PLANE_CTL_REGISTER", "PLANE_CTL_" + str(plane_id) + "_" + panel.pipe, adapter.name)
    psr2_sel_fetch = MMIORegister.get_instance("SEL_FETCH_PLANE_CTL_REGISTER", f"SEL_FETCH_PLANE_CTL_{plane_id}_{panel.pipe}",
                                               adapter.name)

    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        psr2_val = etl_parser.get_mmio_data(psr2_ctl.offset, is_write=True)
    else:
        # from GEN14+, Driver will write first 16 bits & last 16 bit's separately to avoid synchronization issues
        psr2_val = etl_parser.get_mmio_data(0x60902, is_write=True)
    psr2_status_val = etl_parser.get_mmio_data(psr2_status.offset)
    plane_data = etl_parser.get_mmio_data(plane_ctl.offset)
    if (psr2_val is None) or (psr2_status_val is None):
        logging.error(f"PSR registers data not found in {etl_file}")
        return False
    if adapter.name not in common.PRE_GEN_12_PLATFORMS:
        man_trk = etl_parser.get_mmio_data(psr2_man_trk.offset, is_write=True)
        if man_trk is None:
            logging.error(f"PSR2_MAN_TRK_CTL_{panel.transcoder} data not found")
            return False
        sel_fetch = etl_parser.get_mmio_data(psr2_sel_fetch.offset, is_write=True)
        if sel_fetch is None:
            logging.error(f"SEL_FETCH_PLANE_CTL_{panel.pipe} data not found")
            return False
        dip_ctl = etl_parser.get_mmio_data(video_dip_ctl.offset)
        if dip_ctl is None:
            logging.error(f"VIDEO_DIP_CTL_{panel.transcoder} data not found")
            return False
    aux = 'AUX_CHANNEL_' + panel.port.split('_')[1]
    psr_conf = etl_parser.get_dpcd_data(dpcd.Offsets.PSR_CONFIGURATION, channel=aux)
    if psr_conf is None:
        logging.error("DPCD 0x170H data not found")
        return False
    psr_configuration = dpcd.SinkPsrConfiguration(panel.target_id)
    for dpcd_data in psr_conf:
        if not dpcd_data.IsWrite:
            continue
        psr_configuration.value = int(dpcd_data.Data.split('-')[0], 16)
        if psr_configuration.psr_enable_in_sink == 0:
            psr_disable_in_sink = True
            break
    if psr_disable_in_sink is False:
        logging.error("driver did not disable psr in sink")
        gdhm.report_driver_bug_pc("[PowerCons][PSR] Driver did not disable PSR2 in sink")
        return False
    logging.info("Driver disabled PSR2 in sink via DPCD (0x170h)")
    if adapter.name in machine_info.PRE_GEN_16_PLATFORMS:
        vertical_total = v_total.vertical_total
    else:
        vertical_total = v_total.vrr_vmax
    rr = round(
        float(panel.native_mode.pixelClock_Hz) / (
                (h_total.horizontal_total + 1) * (vertical_total + 1)), 3)
    logging.debug(f"Panel Refresh Rate = {rr}")
    if check_idle_status:
        # Max wait time for PSR2 IDLE state = 2 full frame + 7.5 m sec
        # https://gfxspecs.intel.com/Predator/Home/Index/49274
        time_out = round((1000 * 2) / rr + 7.5, 4)  # milli secs
        status &= __verify_psr2_idle_status(psr2_ctl, psr2_val, psr2_status, psr2_status_val, time_out)

    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        psr2_ctl.asUint = psr2_val[-1].Data
    else:
        psr2_ctl.asUint = psr2_val[-1].Data << 16
    if adapter.name in common.PRE_GEN_12_PLATFORMS + common.GEN_12_PLATFORMS:
        # If not LRR: Driver should Program PSR2_CTL to clear Selective Update Tracking Enable.
        if (panel.lrr_caps.is_lrr_supported is False) and psr2_ctl.selective_update_tracking_enable:
            logging.error("selective update tracking is not disabled for non-LRR panel")
            status = False
        logging.info("selective update tracking is disabled for non-LRR panel")
    for val in psr2_val:
        psr2_ctl.asUint = val.Data
        if psr2_ctl.psr2_enable == 0:
            logging.info(f"PSR2 disabled at {val.TimeStamp}ms")
            psr2_disable_time = val.TimeStamp
            break
    if psr2_disable_time is None:
        logging.error("PSR2 is not disabled in driver")
        return False
    for plane in plane_data:
        plane_ctl.asUint = plane.Data
        if plane_ctl.plane_enable:
            continue
        plane_disable_time = plane.TimeStamp
        logging.info(f"Plane{panel.pipe} is disabled at {plane.TimeStamp}")
        break
    if plane_disable_time == 0:
        logging.error(f"Plane{panel.pipe} is not disabled during driver disable")
        gdhm.report_driver_bug_pc(f"[Powercons][PSR] Plane is not disabled during driver disable")
        status = False
    if psr2_disable_time > plane_disable_time:
        capture_state_entry = False
        # PSR2 will not be disabled if it is in CAPTURE state
        # Check whether PSR2 was in CAPTURE state before reporting out the error
        # This is fixed from Gen-15 platform onwards
        one_frame_time = (1/panel.max_rr) * 1000
        start_time = plane_disable_time - one_frame_time
        psr2_status_data = etl_parser.get_mmio_data(psr2_status.offset, start_time=start_time, end_time=plane_disable_time)
        if psr2_status_data is None or adapter.name not in common.PRE_GEN_15_PLATFORMS:
            logging.error("PSR2 is disabled after plane disable")
            gdhm.report_driver_bug_pc("[Powercons][PSR] PSR2 is disabled after plane disable")
            status = False
        else:
            for psr2_status_val in psr2_status_data:
                psr2_status.asUint = psr2_status_val.Data
                if psr2_status.psr2_state == 0x1:
                    capture_state_entry = True

            if capture_state_entry:
                logging.info("PSR2 was in CAPTURE state and hence PSR2 was disabled after Plane disable")
            else:
                logging.error("PSR2 is disabled after plane disable")
                gdhm.report_driver_bug_pc("[Powercons][PSR] PSR2 is disabled after plane disable")
                status = False
            
    if adapter.name in common.GEN_12_PLATFORMS:
        # Verify driver is waiting for one VBI before disabling Manual tracking for Gen 12 Platforms
        status &= __verify_vbi_wait(panel, psr2_ctl, psr2_man_trk)
    if adapter.name not in common.PRE_GEN_12_PLATFORMS:
        # Manual tracking is not supported on PIPE B on Gen12 Platforms
        if adapter.name in common.GEN_12_PLATFORMS and panel.pipe == 'B':
            logging.info("SKIP : Manual tracking check on PIPE B on {}".format(adapter.name))
        else:
            psr2_man_trk.asUint = man_trk[-1].Data
            psr2_sel_fetch.asUint = sel_fetch[-1].Data
            if psr2_sel_fetch.selective_fetch_plane_enable:
                logging.error("selective fetch is not disabled for Plane_1_" + panel.pipe)
                status = False
            logging.info("selective fetch is disabled for Plane_1_" + panel.pipe)
    
    status &= check_clk_gate_wa(adapter, panel, psr2_disable_time, enable_check=False)
    status &= verify_sdp_data(adapter, panel, video_dip_ctl, dip_ctl)
    return status


##
# @brief        Exposed API to verify PSR for given PSR configuration
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    feature to classify psr_util based on frame requirement
# @param[in]    etl_file String, path to ETL file
# @param[in]    polling_data data from etl containing timestamps
# @param[in]    method string, AUDIO/VIDEO
# @param[in]    pause_video Boolean, True if video is to be paused during playback, False otherwise
# @param[in]    is_vsync_disable_expected Boolean, True if VSync Disable call is expected, False otherwise
# @return       status Boolean, True if verification is successful, False otherwise
def verify(adapter, panel, feature, etl_file, polling_data, method, pause_video, is_vsync_disable_expected=False):
    if feature == UserRequestedFeature.PSR_1:
        status = verify_psr1(adapter, panel, polling_data)
    elif feature == UserRequestedFeature.PANEL_REPLAY:
        status = pr.verify_pr_hw_state(adapter, panel, etl_file)
    else:
        status = verify_psr2(adapter, panel, polling_data, method, pause_video, is_vsync_disable_expected)
    return status


##
# @brief        Exposed API to verify Psr1 enable sequence
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    polling_data data from etl with timestamps
# @return       status Boolean, True, if disabled, False otherwise
def verify_psr1(adapter, panel, polling_data):
    if panel.pipe not in ['A', 'B']:
        logging.warning(f"PSR is not supported in Pipe-{panel.pipe}")
        return True

    psr_state_machine = None
    polling_time_stamps = polling_data[1]
    polling_timeline = polling_data[0]
    utility_time_stamps = polling_data[3]
    utility_timeline = polling_data[2]
    srd_status = MMIORegister.get_instance("SRD_STATUS_REGISTER", "SRD_STATUS_" + panel.transcoder, adapter.name)

    time_stamps = polling_data[3] + polling_data[1]
    time_stamps.sort()

    for time_stamp in time_stamps:
        if psr_state_machine is None:
            if time_stamp not in polling_time_stamps:
                continue

            srd_status.asUint = polling_timeline[srd_status.offset][polling_time_stamps.index(time_stamp)]
            if srd_status.asUint is None:
                continue

            if srd_status.srd_state == 2:
                psr_state_machine = Psr1StateMachine(Psr1StateMachine.psr_entry, time_stamp)
            else:
                psr_state_machine = Psr1StateMachine(Psr1StateMachine.psr_exit, time_stamp)
        else:
            if time_stamp in utility_time_stamps:
                screen_update_entry = utility_timeline[utility_time_stamps.index(time_stamp)]
                if screen_update_entry['monitor_id'] == panel.monitor_id:
                    psr_state_machine.next_state(sm.Input(PsrInputs.FRAME_UPDATE, time_stamp))

            if time_stamp in polling_time_stamps:
                srd_status.asUint = polling_timeline[srd_status.offset][polling_time_stamps.index(time_stamp)]
                if srd_status.asUint is None:
                    continue

                if srd_status.srd_state == 2:
                    psr_state_machine.next_state(sm.Input(PsrInputs.MMIO_PSR_ENTRY, time_stamp))
                else:
                    psr_state_machine.next_state(sm.Input(PsrInputs.MMIO_PSR_EXIT, time_stamp))

    if psr_state_machine is None:
        logging.error("\tFAIL: No PSR data found in polling timeline")
        return False

    if psr_state_machine.psr_entry_count > 0 and psr_state_machine.result:
        logging.info("\tPASS: PSR Entry Count= {0}".format(psr_state_machine.psr_entry_count))
        return True
    logging.error("\tFAIL: PSR Entry Count= {0}".format(psr_state_machine.psr_entry_count))
    with open("Logs\\polling_data_{0}.txt".format(time.time()), "w") as f:
        f.write(str(polling_data))
    gdhm.report_bug(
        title="[Powercons][PSR]PSR Entry not Happened",
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )

    return False


##
# @brief        Exposed API for PSR2 verification
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    polling_data data from etl with timestamps
# @param[in]    method string indicates if the polling data corresponds to VIDEO
# @param[in]    pause_video indicates if there was a pause in the video
# @param[in]    is_basic_check [optional], boolean indicates if psr check has to basic
# @param[in]    state string, indicating IDLE/NO_SU
# @note         is_basic_check is used for basic PSR2 verification (used in LRR)
# @param[in]    is_vsync_disable_expected Boolean, True if VSync Disable call is expected, False otherwise
# @return       True if verification passed, False otherwise
def verify_psr2(adapter, panel, polling_data, method, pause_video, is_basic_check=False, state=None, is_vsync_disable_expected=False):
    if panel.pipe not in ['A', 'B']:
        logging.warning(f"PSR is not supported in Pipe-{panel.pipe}")
        return True

    status = True
    psr_state_machine = None
    polling_time_stamps = polling_data[1]
    polling_timeline = polling_data[0]
    deep_sleep_count = 0
    selective_update_count = 0
    idle_count = 0
    entry_count = 0
    exit_count = 0
    psr2_status = MMIORegister.get_instance("PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder, adapter.name)
    psr2_ctl = MMIORegister.get_instance("PSR2_CTL_REGISTER", "PSR2_CTL_" + panel.transcoder, adapter.name)
    utility_time_stamps = None
    utility_timeline = None
    block_fifo_underrun = 0
    su_fifo_underrun = 0
    idle_count_check = True
    skip_idle_count_check = False

    with open("Logs\\polling_data_{0}.txt".format(time.time()), "w") as f:
        f.write(str(polling_data))

    if is_basic_check is False:
        utility_time_stamps = polling_data[3]
        utility_timeline = polling_data[2]

    if method == 'VIDEO' or is_basic_check:
        time_stamps = polling_data[1][:]
    else:
        time_stamps = polling_data[3] + polling_data[1]
    time_stamps.sort()

    for time_stamp in time_stamps:
        # If there is an RR Switch during the workload, PSR2 will get disabled and enabled back
        # Having a check for PSR2 disable due to RR switch during workload to not consider PSR2 Idle state during workload as error
        if time_stamp in polling_time_stamps:
            if polling_timeline.get(psr2_ctl.offset):
                psr2_ctl.asUint = polling_timeline[psr2_ctl.offset][polling_time_stamps.index(time_stamp)]
                if psr2_ctl.psr2_enable == 0 and panel.lrr_caps.is_lrr_supported:
                    skip_idle_count_check = True

        if method == 'VIDEO':
            if time_stamp in polling_time_stamps:
                psr2_status.asUint = polling_timeline[psr2_status.offset][polling_time_stamps.index(time_stamp)]
                if psr2_status.asUint is None:
                    continue
                if psr2_status.psr2_state == 0x0:
                    idle_count += 1
                if psr2_status.psr2_state == 0x3 or psr2_status.psr2_state == 0x6:
                    selective_update_count += 1
                if psr2_status.psr2_state == 0x8:
                    deep_sleep_count += 1

                # FIFO UNDERRUN fields are not applicable for Post Gen-15 platforms
                if adapter.name in common.PRE_GEN_15_PLATFORMS:
                    if psr2_status.psr2_block_fifo_under_run == 1:
                        block_fifo_underrun += 1
                    if psr2_status.psr2_su_fifo_under_run == 1:
                        su_fifo_underrun += 1
        else:
            if is_basic_check:
                psr2_status.asUint = polling_timeline[psr2_status.offset][polling_time_stamps.index(time_stamp)]
                if psr2_status.asUint is None:
                    continue
                if state == 'IDLE' and psr2_status.psr2_state == 0x0:
                    idle_count += 1
                if psr2_status.psr2_state in [0x3, 0x8]:
                    entry_count += 1
                else:
                    exit_count += 1
                
                # FIFO UNDERRUN fields are not applicable for Post Gen-15 platforms
                if adapter.name in common.PRE_GEN_15_PLATFORMS:
                    if psr2_status.psr2_block_fifo_under_run == 1:
                        block_fifo_underrun += 1
                    if psr2_status.psr2_su_fifo_under_run == 1:
                        su_fifo_underrun += 1
                continue

            if psr_state_machine is not None:
                if time_stamp in utility_time_stamps:
                    screen_update_entry = utility_timeline[utility_time_stamps.index(time_stamp)]
                    if screen_update_entry['monitor_id'] == panel.monitor_id:
                        psr_state_machine.next_state(sm.Input(PsrInputs.FRAME_UPDATE, time_stamp))

            if time_stamp in polling_time_stamps:
                psr2_status.asUint = polling_timeline[psr2_status.offset][polling_time_stamps.index(time_stamp)]
                if psr2_status.asUint is None:
                    continue

                if psr_state_machine is None:
                    if psr2_status.psr2_state in [0x3, 0x8]:
                        psr_state_machine = Psr1StateMachine(Psr1StateMachine.psr_entry, time_stamp)
                    else:
                        psr_state_machine = Psr1StateMachine(Psr1StateMachine.psr_exit, time_stamp)
                else:
                    if psr2_status.psr2_state in [0x3, 0x8]:
                        psr_state_machine.next_state(sm.Input(PsrInputs.MMIO_PSR_ENTRY, time_stamp))
                    else:
                        psr_state_machine.next_state(sm.Input(PsrInputs.MMIO_PSR_EXIT, time_stamp))

                # FIFO UNDERRUN fields are not applicable for Post Gen-15 platforms
                if adapter.name in common.PRE_GEN_15_PLATFORMS:
                    if psr2_status.psr2_block_fifo_under_run == 1:
                        block_fifo_underrun += 1
                    if psr2_status.psr2_su_fifo_under_run == 1:
                        su_fifo_underrun += 1

    if skip_idle_count_check:
        logging.info(f"PSR2 was disabled during workload : {method}")

    if method == 'VIDEO':
        if is_basic_check:
            logging.info("\tIDLE state count= {0}".format(idle_count))
            logging.info("\tDEEP_SLEEP state count= {0}".format(deep_sleep_count))
            logging.info("\tSELECTIVE_UPDATE state count= {0}".format(selective_update_count))

            if state == 'NO_SU':
                if selective_update_count > 0:
                    logging.error("\tFAIL: PSR2 SELECTIVE_UPDATE is hitting")
                    return False

            if idle_count == 0 and deep_sleep_count == 0 and selective_update_count == 0:
                gdhm.report_driver_bug_pc("[Powercons][PSR2]PSR2 Entry not Happened during VIDEO PLAYBACK")
                return False

            if block_fifo_underrun > 0:
                logging.warning("\tBLOCK_FIFO_UNDERRUN raised by HW")
            if su_fifo_underrun > 0:
                logging.warning("\tSU_FIFO_UNDERRUN raised by HW")

            return True

        if pause_video:
            if adapter.name not in common.PRE_GEN_13_PLATFORMS + ['DG2']:
                display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
                # HSD-14015518096 -  there is a delay in MMIO read with DC6v , due to this intermediate HW states are
                # not possible to verify
                if display_pc.DisableDC6v == 0:
                    idle_count_check = False

            if idle_count_check:
                if idle_count != 0:
                    logging.info("\tPASS: IDLE state count Expected= Non-Zero, Actual= {0}".format(idle_count))
                else:
                    logging.error("\tFAIL: IDLE state count Expected= Non-Zero, Actual= {0}".format(idle_count))
                    status = False

            if deep_sleep_count != 0:
                logging.info(
                    "\tPASS: DEEP_SLEEP state count Expected= Non-Zero, Actual= {0}".format(deep_sleep_count))
            else:
                logging.error(
                    "\tFAIL: DEEP_SLEEP state count Expected= Non-Zero, Actual= {0}".format(deep_sleep_count))
                status = False
        else:
            # During video playback, PSR should not hit IDLE state
            if is_basic_check is False:
                if not skip_idle_count_check and not is_vsync_disable_expected:
                    if idle_count != 0:
                        logging.error("\tFAIL: IDLE state count Expected= 0, Actual= {0}".format(idle_count))
                        gdhm.report_driver_bug_pc("[Powercons][PSR2]PSR2 Entered IDLE state during VideoPlayback")
                        status = False
                    else:
                        logging.info("\tPASS: IDLE state count Expected= 0, Actual= {0}".format(idle_count))
                else:
                    logging.info(f"Skipping PSR2 Idle count check as PSR2 was disabled during workload {method}")

            if not is_vsync_disable_expected:
                # During video playback, PSR should not hit deep sleep
                if deep_sleep_count == 0:
                    logging.info("\tPASS: DEEP_SLEEP state count Expected= 0, Actual= {0}".format(deep_sleep_count))
                else:
                    logging.error("\tFAIL: DEEP_SLEEP state count Expected= 0, Actual= {0}".format(deep_sleep_count))
                    status = False


        if selective_update_count != 0:
            logging.info("\tPASS: SELECTIVE_UPDATE state count Expected= Non-Zero, Actual= {0}".format(
                selective_update_count))
        else:
            logging.error("\tFAIL: SELECTIVE_UPDATE state count Expected= Non-Zero, Actual= {0}".format(
                selective_update_count))
            status = False

        if status is False:
            with open("Logs\\polling_data_{0}.txt".format(time.time()), "w") as f:
                f.write(str(polling_data))

        if block_fifo_underrun > 0:
            logging.warning("\tBLOCK_FIFO_UNDERRUN raised by HW")
        if su_fifo_underrun > 0:
            logging.warning("\tSU_FIFO_UNDERRUN raised by HW")

        return status

    if is_basic_check:
        if state == 'IDLE':
            logging.info("\tIDLE state count= {0}".format(idle_count))
            logging.info("\tPSR Entry (SLEEP+DEEP SLEEP) Count= {0}".format(entry_count))
            if entry_count > 0:
                logging.error("\tFAIL: PSR SLEEP/DEEP SLEEP state is hitting")
                return False
            if idle_count > 0 or skip_idle_count_check:
                return True
            logging.error("\tFAIL: PSR IDLE state count is 0")
            return False
        else:
            if entry_count > 0:
                logging.info("\tPASS: PSR Entry Count= {0}".format(entry_count))
                return True
        logging.error("\tFAIL: PSR Entry Count= {0}".format(entry_count))
        gdhm.report_bug(
            title="[Powercons][PSR2]PSR2 Entry not Happened",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_POWERCONS,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        return False

    if psr_state_machine is None:
        logging.error("\tFAIL: No PSR data found in polling timeline")
        return False

    if block_fifo_underrun > 0:
        logging.warning("\tBLOCK_FIFO_UNDERRUN raised by HW")
    if su_fifo_underrun > 0:
        logging.warning("\tSU_FIFO_UNDERRUN raised by HW")

    if psr_state_machine.psr_entry_count > 0 and psr_state_machine.result:
        logging.info("\tPASS: PSR Entry Count= {0}".format(psr_state_machine.psr_entry_count))
        return True
    logging.error("\tFAIL: PSR Entry Count= {0}".format(psr_state_machine.psr_entry_count))
    gdhm.report_bug(
        title="[Powercons][PSR]PSR Entry not Happened",
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )

    return False


##
# @brief        Helper function to verify wake line time
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @param[in]    h_total register instance
# @param[in]    psr2_ctl register instance
# @param[in]    alpm_ctl_reg register instance
# @ return      True if verification successful, False otherwise
def __verify_su_wake_line_time(adapter, panel, h_total, psr2_ctl, alpm_ctl_reg):
    min_blk_count_wake_lines = WAKE_LINES[8]
    # HSD WA- 22012278275 - PSR2 IO/Fast wake times value mismatch
    min_wake_lines = 7
    max_wake_lines = 12
    min_bspec_su_wake_line = 5

    # verify driver programmed line time values matches with the Bspec values
    # line time in micro secs = H total / Pixel clock in MHZ
    line_time = round(
        ((h_total.horizontal_total + 1) / float(panel.native_mode.pixelClock_Hz / (1000 * 1000))), 3)  # in micro secs
    logging.info(f"Line time = {line_time} us")
    # PSR2 IO wake time = 10us PHY latency + 32us eDP standard maximum Fast Wake from FW_SLEEP.
    io_wake_time = 42 if adapter.name in common.PRE_GEN_15_PLATFORMS else 44
    io_buffer_wake = math.ceil(io_wake_time / line_time)
    fast_wake_time = io_wake_time if adapter.name in common.PRE_GEN_15_PLATFORMS else 42
    fast_wake = math.ceil(fast_wake_time / line_time)

    # Check for maximum and minimum wake line limits
    # IO Buffer wake and fast wake programming logic is different for Pre-Gen15 and Post Gen-15 platforms
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        if (io_buffer_wake > max_wake_lines) or (io_buffer_wake < min_wake_lines):
            io_buffer_wake = (min_wake_lines if io_buffer_wake < min_wake_lines else max_wake_lines)

        if (fast_wake > max_wake_lines) or (fast_wake < min_wake_lines):
            fast_wake = (min_wake_lines if fast_wake < min_wake_lines else max_wake_lines)
    else:
        io_buffer_wake = io_buffer_wake - min_bspec_su_wake_line if io_buffer_wake > min_bspec_su_wake_line else 0
        fast_wake = fast_wake - min_bspec_su_wake_line if fast_wake > min_bspec_su_wake_line else 0

    # Wa_22012278275 : D13ADL PSR2 IO/Fast wake times not matching with programming
    sku_name = machine_info.SystemInfo().get_sku_name(adapter.gfx_index)
    if adapter.name in ['ADLP'] and sku_name not in ['RPLP']:
        io_buffer_wake = WAKE_LINES_GEN13[io_buffer_wake]
        fast_wake = WAKE_LINES_GEN13[fast_wake]
    elif adapter.name in common.PRE_GEN_15_PLATFORMS:
        io_buffer_wake = WAKE_LINES[io_buffer_wake]
        fast_wake = WAKE_LINES[fast_wake]

    if io_buffer_wake != psr2_ctl.io_buffer_wake:
        logging.error(f"FAIL : IO Buffer lines value expected = {io_buffer_wake} actual = {psr2_ctl.io_buffer_wake}")
        gdhm.report_driver_bug_pc("[PowerCons][PSR] Incorrect IO Buffer Wake line programming by the driver")
        return False
    logging.info(f"PASS : IO Buffer lines value programmed correctly. Expected : {io_buffer_wake} Lines")

    # Pre-Gen15 - Fast wake lines will be programmed in PSR2 CTL Register
    # Post-Gen15 - Fast wake lines will be programmed in ALPM CTL Register
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        if fast_wake != psr2_ctl.fast_wake:
            logging.error("Fast wake lines value expected = {0} actual = {1}".format(fast_wake, psr2_ctl.fast_wake))
            return False
    else:
        if alpm_ctl_reg.extended_fast_wake_enable != 1:
            logging.error("extended_fast_wake_enable bit is not set by the driver")
            gdhm.report_driver_bug_pc("[PowerCons][PSR] extended_fast_wake_enable bit is not set by the driver")
            return False
        logging.info("PASS : extended_fast_wake_enable bit is set by the driver")

        if fast_wake != alpm_ctl_reg.extended_fast_wake_time:
            logging.error(f"FAIL : Fast wake lines value expected = {fast_wake} actual = {alpm_ctl_reg.extended_fast_wake_time}")
            gdhm.report_driver_bug_pc("[PowerCons][PSR] Incorrect Fast Wake line programming by the driver")
            return False
    logging.info(f"PASS : Fast wake lines value programmed correctly. Expected : {fast_wake} Lines")

    # If IO buffer wake lines or fast wake lines > 8, program Block count should be 3 blocks, else 2 blocks
    # block_count_number bit is removed from LNL
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        if fast_wake > min_blk_count_wake_lines:
            if psr2_ctl.block_count_number != PSR_BLOCK_COUNT_NUMBER.BLOCK_COUNT_NUMBER_3_BLOCKS:
                logging.error(
                    f"PSR block count value mismatch. Expected= {PSR_BLOCK_COUNT_NUMBER.BLOCK_COUNT_NUMBER_3_BLOCKS}, "
                    f"Actual= {psr2_ctl.block_count_number}")
                return False
        else:
            if psr2_ctl.block_count_number != PSR_BLOCK_COUNT_NUMBER.BLOCK_COUNT_NUMBER_2_BLOCKS:
                logging.error(
                    f"PSR block count value mismatch. Expected= {PSR_BLOCK_COUNT_NUMBER.BLOCK_COUNT_NUMBER_3_BLOCKS}, "
                    f"Actual= {psr2_ctl.block_count_number}")
                return False
    return True


##
# @brief        Helper function to verify psr2 idle status
# @param[in]    psr2_ctl, register instance
# @param[in]    psr2_val, list of PSR2 control register values
# @param[in]    psr2_status, register instance
# @param[in]    psr2_status_val, list of PSR2 status register values
# @param[in]    time_out, in ms, before which PSR2 should be in idle state
# @ return      True if PSR2 returned to IDLE state in a given time, False otherwise
def __verify_psr2_idle_status(psr2_ctl, psr2_ctl_val, psr2_status, psr2_status_val, time_out):
    logging.info("Verifying PSR2 Idle Status")
    for ctl_val in psr2_ctl_val:
        psr2_ctl.asUint = ctl_val.Data
        if psr2_ctl.psr2_enable == 1:
            continue
        for status_val in psr2_status_val:
            psr2_status.asUint = status_val.Data
            # Make sure that the current PSR2 Status Register read is after PSR2 Disable
            if status_val.TimeStamp < ctl_val.TimeStamp:
                continue
            if psr2_status.psr2_state == 0:
                if status_val.TimeStamp > (ctl_val.TimeStamp + time_out):
                    # PSR2 is not returning to IDLE state due to an existing bug : https://hsdes.intel.com/appstore/article/#/18023613869
                    # Currently avoiding the test from failing and only logging the failure to GDHM
                    # @todo Below logic should return False once the HSD gets implemented
                    # Create a JIRA for the same : https://jira.devtools.intel.com/browse/VSDI-34765
                    logging.error(f"PSR2 not returned to IDLE state before {time_out} ms")
                    gdhm.report_driver_bug_pc("[Powercons][PSR] PSR2 not returned to IDLE state before timeout")
                    return True
            logging.info(f"PSR2 returned to IDLE state at {status_val.TimeStamp}")
            return True
    logging.error("PSR2 did not return to IDLE state")
    gdhm.report_bug(
        title="[Powercons][PSR]PSR2 did not return to IDLE state",
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )
    return False


##
# @brief        Function to verify psr2 in pre-si
# @param[in]    feature to classify psr_util based on frame requirement
# @param[in]    monitor_ids a list of monitor id's
# @return      True if verification passes, False otherwise
def verify_pre_si(feature, monitor_ids):
    frame_counter = {}  # Read frame counter before updating the screen
    target_frame_counter = {}
    for adapter in dut.adapters.values():
        frame_counter[adapter.gfx_index] = {}
        target_frame_counter[adapter.gfx_index] = {}
        for panel in adapter.panels.values():
            if panel.is_lfp is False:
                continue
            pipe_frame_counter = MMIORegister.read(
                "PIPE_FRMCNT_REGISTER", "PIPE_FRMCNT_" + panel.pipe, adapter.name, gfx_index=adapter.gfx_index)
            frame_counter[adapter.gfx_index][panel.port] = pipe_frame_counter.pipe_frame_counter
            logging.info("\tFrameCounter({0}) before screen update= {1}".format(
                panel.port, frame_counter[adapter.gfx_index][panel.port]))
            target_frame_counter[adapter.gfx_index][panel.port] = \
                frame_counter[adapter.gfx_index][panel.port] + __PRE_SI_FRAME_UPDATE_MAX
    screen_update_process = None
    try:
        # Update the frame
        signal_queue = Queue()
        logging.info("\tStarted PSR utility at {0}".format(datetime.now()))
        screen_update_process = Process(target=psr_util.run, args=(monitor_ids, 1, True, signal_queue))
        screen_update_process.start()
        signal_queue.get()
        logging.info("\tFrame update completed at {0}".format(datetime.now()))

        def is_frame_update_limit_reached(fc, tfc):
            for gfx_index in fc.keys():
                for display, count in fc[gfx_index].items():
                    if count < tfc[gfx_index][display]:
                        return True

            return False

        status = False
        while is_frame_update_limit_reached(frame_counter, target_frame_counter):
            psr_status = {}
            for adapter in dut.adapters.values():
                psr_status[adapter.gfx_index] = {}
                for panel in adapter.panels.values():
                    if panel.is_lfp is False:
                        continue
                    pipe_frame_counter = MMIORegister.read(
                        "PIPE_FRMCNT_REGISTER", "PIPE_FRMCNT_" + panel.pipe, adapter.name, gfx_index=adapter.gfx_index)
                    frame_counter[adapter.gfx_index][panel.port] = pipe_frame_counter.pipe_frame_counter
                    logging.info("\tFrameCounter({0}) before screen update= {1}".format(
                        panel.port, frame_counter[adapter.gfx_index][panel.port]))

                    if feature == UserRequestedFeature.PSR_1:
                        srd_status = MMIORegister.read(
                            "SRD_STATUS_REGISTER", 'SRD_STATUS_' + panel.transcoder, adapter.name,
                            gfx_index=adapter.gfx_index)
                        if srd_status.srd_state == 0x2:
                            psr_status[adapter.gfx_index][panel.port] = True
                        else:
                            psr_status[adapter.gfx_index][panel.port] = False

                    if feature > UserRequestedFeature.PSR_1:
                        psr2_status = MMIORegister.read(
                            "PSR2_STATUS_REGISTER", 'PSR2_STATUS_' + panel.transcoder, adapter.name,
                            gfx_index=adapter.gfx_index)
                        psr2_ctl = MMIORegister.read(
                            "PSR2_CTL_REGISTER", 'PSR2_CTL_' + panel.transcoder, adapter.name,
                            gfx_index=adapter.gfx_index)
                        psr2_man_trk = MMIORegister.read("PSR2_MAN_TRK_CTL_REGISTER",
                                                         "PSR2_MAN_TRK_CTL_" + panel.transcoder,
                                                         adapter.name, gfx_index=adapter.gfx_index)
                        plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
                        psr2_sel_fetch = MMIORegister.read("SEL_FETCH_PLANE_CTL_REGISTER", f"SEL_FETCH_PLANE_CTL_{plane_id}_{panel.pipe}",
                                                        adapter.name, gfx_index=adapter.gfx_index)
                        if feature == UserRequestedFeature.PANEL_REPLAY:
                            pr_ctl = MMIORegister.read(
                                'TRANS_DP2_CTL_REGISTER', 'TRANS_DP2_CTL_' + panel.transcoder, adapter.name,
                                gfx_index=adapter.gfx_index)
                            alpm_ctl = MMIORegister.read(
                                'ALPM_CTL_REGISTER', 'ALPM_CTL_' + panel.transcoder, adapter.name,
                                gfx_index=adapter.gfx_index)
                            pr_alpm_ctl = MMIORegister.read(
                                'PR_ALPM_CTL_REGISTER', 'PR_ALPM_CTL_' + panel.transcoder, adapter.name,
                                gfx_index=adapter.gfx_index)
                        if psr2_status.psr2_state in [0x3, 0x8] and psr2_man_trk.sf_partial_frame_enable == 1 \
                                and psr2_sel_fetch.selective_fetch_plane_enable == 1:
                            psr_status[adapter.gfx_index][panel.port] = True
                        else:
                            psr_status[adapter.gfx_index][panel.port] = False
            if all(res is True for adapter in dut.adapters.values()
                   for res in psr_status[adapter.gfx_index].values()):
                status = True
                break

            time.sleep(__PRE_SI_POLLING_DELAY)
    except Exception as e:
        assert False, e
    finally:
        if "screen_update_process" in locals():
            # Close the PSR utility
            screen_update_process.terminate()
            logging.info("\tStopped PSR utility at {0}".format(datetime.now()))
    return status


##
# @brief        Exposed API to get polling offsets
# @param[in]    feature to classify psr_util based on frame requirement
# @return       offsets list
def get_polling_offsets(feature):
    psr_feature = feature
    offsets = []
    for adapter in dut.adapters.values():
        for panel in adapter.panels.values():
            if panel.is_lfp and panel.pipe not in ['A', 'B']:
                logging.warning("PSR/PR is supported only on Pipe-A and Pipe-B")
                continue
            if feature >= UserRequestedFeature.PSR_2 and adapter.name in ['TGL'] and panel.pipe == 'B':
                feature = UserRequestedFeature.PSR_1
            else:
                feature = psr_feature
            if feature == UserRequestedFeature.PSR_1:
                offsets.append(MMIORegister.get_instance(
                    "SRD_STATUS_REGISTER", "SRD_STATUS_" + panel.transcoder, adapter.name).offset)

            elif UserRequestedFeature.PSR_1 < feature < UserRequestedFeature.PANEL_REPLAY:
                offsets.append(MMIORegister.get_instance(
                    "PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder, adapter.name).offset)
            elif feature == UserRequestedFeature.PANEL_REPLAY:
                if panel.is_lfp:
                    offsets.append(MMIORegister.get_instance(
                        "PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder, adapter.name).offset)
                else:
                    if adapter.name in common.PRE_GEN_16_PLATFORMS:
                        offsets.append(MMIORegister.get_instance(
                            "SRD_STATUS_REGISTER", "SRD_STATUS_" + panel.transcoder, adapter.name).offset)
                    else:
                        offsets.append(MMIORegister.get_instance(
                            "PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder, adapter.name).offset)

    return offsets


##
# @brief        Exposed API to verify sink failures
# @param[in]    panel panel object
# @param[in]    feature to classify psr_util based on frame requirement
# @return       offsets
def verify_sink_failures(panel, feature):
    status = True
    frame_update = None
    target_id = panel.target_id
    retry_count = 1

    try:
        frame_update = subprocess.Popen(__FRAME_UPDATE_PATH)
        time.sleep(2)

        while (retry_count < 3):
            status = True
            if UserRequestedFeature.PSR_1 <= feature < UserRequestedFeature.PANEL_REPLAY:
                # Below DPCD checks applicable for both PSR1 & PSR2
                # Get Sink Device Psr Status
                sink_device_psr_status = dpcd.SinkDevicePsrStatus(target_id)
                if sink_device_psr_status.sink_device_self_refresh_status == 7:
                    logging.error("\tSINK_DEVICE_INTERNAL_ERROR raised by sink")
                    status = False

                # Get Sink Device Psr Configuration
                sink_device_psr_config = dpcd.SinkPsrConfiguration(target_id)
                if sink_device_psr_config.psr_enable_in_sink == 0:
                    logging.error("\tSource device did not enabled PSR in sink")
                    status = False

                if UserRequestedFeature.PSR_2 <= feature < UserRequestedFeature.PANEL_REPLAY:
                    # Get Psr2 Error Status
                    psr2_error_status = dpcd.Psr2ErrorStatus(target_id)
                    if psr2_error_status.vsc_sdp_uncorrectable_error == 1:
                        logging.error("\tVSC_SDP_UNCORRECTABLE_ERROR raised by sink")
                        status = False

                        if psr2_error_status.link_crc_error == 1:
                            logging.error("\tLINK_CRC_ERROR raised by sink")
                            status = False

                        if psr2_error_status.rfb_storage_error == 1:
                            logging.error("\tRFB_STORAGE_ERROR raised by sink")
                            status = False
                        # Get Sink Device AuxFrameSync Status
                        if dpcd.get_aux_frame_sync_support(target_id):
                            psr2_aux_sync_status = dpcd.SinkAuxFrameSyncStatus(target_id)
                            if psr2_aux_sync_status.aux_frame_sync_lock_error:
                                logging.error("\tSink device failed to achieve AUX_FRAME_SYNC Lock")
                                status = False
                        else:
                            logging.info("AUX_FRAME_SYNC is not supported in sink")
            elif feature == UserRequestedFeature.PANEL_REPLAY:
                pr_error_status = dpcd.PanelReplayErrorStatus(target_id)
                if pr_error_status.rfb_storage_error:
                    logging.error("\tPR RFB_STORAGE_ERROR raised by sink")
                    status = False
                if pr_error_status.vsc_sdp_for_pr_uncorrectable_error == 1:
                    logging.error("\tPR VSC_SDP_UNCORRECTABLE_ERROR raised by sink")
                    status = False
                if pr_error_status.active_frame_crc_error == 1:
                    logging.error("\tPR ACTIVE_FRAME_CRC_ERROR raised by sink")
                    status = False
                if panel.is_lfp:
                    if pr_error_status.adaptive_sync_sdp_missing_and_not_disabled:
                        logging.error(
                            "\t Adaptive-sync SDP missing and not disabled from a prior SDP with DB0[2] = 1")
                        status = False
            if status:
                break
            time.sleep(2)
            retry_count += 1
    except Exception as e:
        logging.error(e)
        status = False
    finally:
        if frame_update is not None:
            frame_update.kill()

    return status


##
# @brief        Exposed API to enable/disable PSR in AC
# @param[in]    adapter Adapter Object
# @param[in]    enable_in_ac Boolean, True- for enable in Ac , False- for disable in AC
# @return       status Boolean, True success & restart required, None success & no restart required, False otherwise
def enable_disable_psr_in_ac(adapter, enable_in_ac):
    reg_val = 0x0 if enable_in_ac else 0x1
    psr_ac = registry.write(adapter.gfx_index, registry.RegKeys.PSR.PSR_DISABLE_IN_AC,
                            registry_access.RegDataType.DWORD, reg_val)
    if psr_ac is False:
        logging.error(f"\tFAILED to update {registry.RegKeys.PSR.PSR_DISABLE_IN_AC} registry")
        return False
    logging.info(f"Updated reg key PsrDisableInAC= {reg_val}")
    return psr_ac


##
# @brief        Exposed API to enable/disable selective fetch in reg key
# @param[in]    gfx_index string , gfx_0/gfx_1
# @param[in]    panel panel object
# @param[in]    sel_fetch_enable Boolean, True- enable selective fetch , False- disable selective fetch
# @return       status Boolean, True if operation is successful, False otherwise
def enable_disable_selective_fetch(gfx_index, panel, sel_fetch_enable):
    sel_fetch_enable = 0x0 if sel_fetch_enable else 0x1
    status = None
    display_pc = None
    if panel.psr_caps.is_psr2_supported:
        display_pc = registry.DisplayPcFeatureControl(gfx_index)
        if display_pc.DisableSelectiveFetch != sel_fetch_enable:
            display_pc.DisableSelectiveFetch = sel_fetch_enable
    elif panel.pr_caps.is_pr_supported:
        display_pc = registry.DisplayPcFeatureCtrlDbg(gfx_index)
        if display_pc.DisablePanelReplaySelectiveFetch != sel_fetch_enable:
            display_pc.DisablePanelReplaySelectiveFetch = sel_fetch_enable

    status = display_pc.update(gfx_index)
    if status is False:
        logging.error("FAILED to update DisplayPCFeatureControl registry")
        return False
    logging.info(f"Updated DisableSelectiveFetch val= {sel_fetch_enable} on {panel}")
    return status


##
# @brief        Internal API to verify Manual tracking is disabled with VBI wait after disabling SelectiveUpdateTracking
# @param[in]    panel object
# @param[in]    psr2_ctl register instance
# @param[in]    psr2_man_trk register instance
# @return       status Boolean, True if verification is successful, False otherwise
def __verify_vbi_wait(panel, psr2_ctl, psr2_man_trk):
    frame_time_max_rr  = (1/panel.max_rr) * 1000
    vbi_wait_status = True
    psr2_ctl_data = etl_parser.get_mmio_data(psr2_ctl.offset, is_write=True)
    psr2_man_trk_data = etl_parser.get_mmio_data(psr2_man_trk.offset, is_write=True)

    if psr2_ctl_data is None:
        logging.error(f"PSR2_CTL_1_{panel.transcoder} MMIO data is empty")
        return False
    if psr2_man_trk_data is None:
        logging.error(f"PSR2_MAN_TRK_CTL_{panel.transcoder} MMIO data is empty")
        return False

    for psr2_ctl_val in psr2_ctl_data:
        psr2_ctl.asUint = psr2_ctl_val.Data
        if psr2_ctl.selective_update_tracking_enable != 0:
            continue
        logging.debug(f"Selective Update Tracking was disabled at {psr2_ctl_val.TimeStamp}")
        for psr2_man_trk_val in psr2_man_trk_data:
            psr2_man_trk.asUint = psr2_man_trk_val.Data
            if psr2_man_trk.psr2_manual_tracking_enable != 0:
                continue
            if psr2_man_trk_val.TimeStamp < psr2_ctl_val.TimeStamp:
                continue
            logging.debug(f"Manual Tracking was disabled at {psr2_man_trk_val.TimeStamp}")
            timestamp_diff = psr2_man_trk_val.TimeStamp - psr2_ctl_val.TimeStamp
            # Manual Tracking should be disabled after waiting for atleast one frame of Max RR
            if timestamp_diff < frame_time_max_rr :
                vbi_wait_status = False

    if not vbi_wait_status:
        logging.error("Driver didn't wait for VBI before disabling Manual Tracking")
        gdhm.report_driver_bug_pc("[Powercons][PSR] Driver didn't wait for VBI before disabling Manual Tracking")
        return False
    logging.info("ManualTracking was disabled after VBI wait")
    return True


##
# @brief        API to verify the PSR2 minimum vblank support in lines required to wake the IO when there is an update
#               starting from the first active line
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       status Boolean, True if verification is successful, False otherwise
def verify_psr2_vblank_support(adapter, panel):
    assert adapter
    assert panel

    # line time restriction check is not applicable from LNL+
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        return True

    min_block_count = 8
    max_block_count = 12
    max_line_time = 5250  # in Nano secs
    psr2_ctl_edp = MMIORegister.read(
        'PSR2_CTL_REGISTER', 'PSR2_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    vblank = MMIORegister.read(
        'TRANS_VBLANK_REGISTER', 'TRANS_VBLANK_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
    h_total = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + panel.transcoder,
                                adapter.name, gfx_index=adapter.gfx_index)
    # calculate line time in nano secs
    line_time_in_ns = round(
        ((h_total.horizontal_total + 1) / float(panel.native_mode.pixelClock_Hz / (1000 * 1000))) * 1000, 3)
    if adapter.name in common.GEN_11_PLATFORMS:
        min_line_time_in_ns = 6250  # in Nano secs
        block_count_lines = min_block_count
    else:
        # PSR2 requires total line time of at least 3.5us
        # Bspec - https://gfxspecs.intel.com/Predator/Home/Index/49274
        min_line_time_in_ns = 3500  # in Nano secs
        # If Line time is greater than 5.25 us, vblank should be greater than or equal to 8 lines.
        # If line time with less than 5.25 us, vblank should be greater than 12 lines.
        block_count_lines = (min_block_count if line_time_in_ns >= max_line_time else max_block_count)

    # PSR2 will not be enabled if (TRANS_VBLANK Vertical Blank END - TRANS_VBLANK Vertical Blank START) <
    # PSR2_CTL Block Count Number value in lines
    # minimum block count of 8 lines means PSR2 requires vblank to be at least 8 scan lines
    vblank_status = (vblank.vertical_blank_end - vblank.vertical_blank_start) < block_count_lines
    if vblank_status and (psr2_ctl_edp.psr2_enable == 0):
        logging.error(
            f"Required min Vblank val >=8 . Actual= {vblank.vertical_blank_end - vblank.vertical_blank_start}")
        return False
    if vblank_status and psr2_ctl_edp.psr2_enable:
        logging.error(f"PSR2 is enabled when (vblank_start - vblank_end) < {block_count_lines} block count lines")
        return False
    line_time_status = (line_time_in_ns < min_line_time_in_ns)
    if line_time_status and (psr2_ctl_edp.psr2_enable == 0):
        logging.error(f"line_time Excepted >= {min_line_time_in_ns} ns, Actual = {line_time_in_ns} ns")
        return False
    if line_time_status and psr2_ctl_edp.psr2_enable:
        logging.error(f"Psr2 is enabled when line_time < {min_line_time_in_ns} ns")
        return False
    return True


##
# @brief        Exposed API to update PSR setting in VBT
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @param[in]    enable_vbt boolean to indicate if psr has to be enabled
# @return       True if PSR is enabled in VBT, False otherwise
def update_vbt(adapter, panel, enable_vbt):
    expected_value = 1 if enable_vbt else 0
    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    if panel.is_lfp is False:
        logging.info("\tPanel is not LFP. Skip Vbt update")
        return True
    # Skip VBT update for unsupported VBT version
    if gfx_vbt.version < 228:
        logging.info("\tVbt version is < 228. Skip Vbt update")
        return True

    # Make sure PSR is enabled in VBT
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    psr_status = (gfx_vbt.block_44.PsrEnable[0] & (1 << panel_index)) >> panel_index
    if psr_status != expected_value:
        if enable_vbt:
            gfx_vbt.block_44.PsrEnable[0] |= (1 << panel_index)
        else:
            gfx_vbt.block_44.PsrEnable[0] &= (0 << panel_index)

        if gfx_vbt.apply_changes() is False:
            logging.error("\tFailed to apply changes to VBT")
            return False

        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            logging.error("\tFailed to restart display driver after VBT update")
            return False

        # Verify after restarting the driver
        gfx_vbt.reload()
        psr_status = (gfx_vbt.block_44.PsrEnable[0] & (1 << panel_index)) >> panel_index
        if psr_status != expected_value:
            logging.error(f"\tFailed to {'enable' if enable_vbt else 'disable'} PSR in VBT")
            return False
        logging.info(f"\tPASS: {'Enabled' if enable_vbt else 'Disabled'} PSR in VBT successfully {panel.port}")
    else:
        logging.info(f"\tPASS: PSR is {'enabled' if enable_vbt else 'disabled'} in VBT for {panel.port}")

    return True


##
# @brief        This function verifies PSR entry based on polling data
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    polling_data PSR1 registers polling data
# @param[in]    method VIDEO/APP/GAME
# @param[in]    feature PSR1/PSR2
# @return       True if verification successful else False
def verify_psr_entry(adapter, panel, polling_data, method="APP", feature=UserRequestedFeature.PSR_1):
    psr_entry_count = 0
    if feature == UserRequestedFeature.PSR_1:
        srd_status = MMIORegister.get_instance("SRD_STATUS_REGISTER", "SRD_STATUS_" + panel.transcoder, adapter.name)
        for val in polling_data[0][srd_status.offset]:
            srd_status.asUint = val
            if srd_status.srd_state == 2:
                psr_entry_count += 1
    elif feature >= UserRequestedFeature.PSR_2:
        psr2_status = MMIORegister.get_instance("PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder, adapter.name)
        for val in polling_data[0][psr2_status.offset]:
            psr2_status.asUint = val
            if psr2_status.psr2_state in [0x3, 0x8]:
                psr_entry_count += 1
    if method not in ['APP', 'IDLE'] and psr_entry_count:
        logging.error(
            f"{UserRequestedFeature(feature).name} Entry happened during {method} workload.Entry count = {psr_entry_count}")
        return False
    feature_str = UserRequestedFeature(feature).name
    logging.info(f"{feature_str} entry count = {psr_entry_count}")
    return True


##
# @brief        This function verifies PSR entry based on polling data
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    etl_file etl_file path
# @param[in]    feature PSR1/PSR2
# @param[in]    method VIDEO/APP/GAME
# @return       True if verification successful else False
def verify_psr_entry_via_etl(adapter, panel, etl_file, feature, method="APP"):
    etl_parser.generate_report(etl_file)
    psr_entry_count = 0
    vbi_enabled_duration = 0
    vbi_enabled_regions, _ = drrs.get_vsync_enable_disable_regions(etl_parser.Ddi.DDI_CONTROLINTERRUPT2)
    for (start_time, end_time) in vbi_enabled_regions:
        # It is possible that LinkM write happened before ETL tracing if VBI was enabled in the beginning.
        # Skipping the first region.
        if start_time == 0:
            continue
        # To avoid a scenario where VBI got enabled just before (few ms) stopping the ETL traces
        if end_time == sys.maxsize:
            continue

        vbi_enabled_duration += (end_time - start_time)
        logging.info(f"\tVBI Enabled Region: Start= {start_time}, End= {end_time}")

        if feature == UserRequestedFeature.PSR_1:
            srd_status = MMIORegister.get_instance("SRD_STATUS_REGISTER", "SRD_STATUS_" + panel.transcoder, adapter.name)
            srd_status_data = etl_parser.get_mmio_data(srd_status.offset, start_time=start_time, end_time=end_time)
            if not srd_status_data:
                logging.warning(f"No SRD Status Register data found inside the VSYNC Enable region {start_time} - {end_time}")
                continue
            for srd_status_val in srd_status_data:
                srd_status.asUint = srd_status_val.Data
                if srd_status.srd_state == 2:
                    psr_entry_count += 1
        elif feature >= UserRequestedFeature.PSR_2:
            psr2_status = MMIORegister.get_instance("PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder, adapter.name)
            psr2_status_data = etl_parser.get_mmio_data(psr2_status.offset, start_time=start_time, end_time=end_time)
            if not psr2_status_data:
                logging.warning(f"No PSR2 Status Register data found inside the VSYNC Enable region {start_time} - {end_time}")
                continue
            for psr2_status_val in psr2_status_data:
                psr2_status.asUint = psr2_status_val.Data
                # PSR2 States which indicate PSR2 entry 
                # 0x3 - Sleep | 0x6 - Selective Update | 0x8 - Deep Sleep
                if psr2_status.psr2_state in [0x8]:
                    logging.error(f"PSR2 deep sleep entry happened at {psr2_status_val.TimeStamp} ms")
                    psr_entry_count += 1

    if method not in ['APP', 'IDLE'] and psr_entry_count:
        logging.error(
            f"{UserRequestedFeature(feature).name} Entry happened during {method} workload.Entry count = {psr_entry_count}")
        return False
    feature_str = UserRequestedFeature(feature).name
    logging.info(f"{feature_str} entry count = {psr_entry_count}")
    return True


##
# @brief        This function checks if PSR Setup time is valid w.r.t vblank time
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    feature PSR1/PSR2
# @return       True if verification successful, False if Failed and None if no PSR
def verify_psr_setup_time(adapter, panel, feature):
    feature_str = UserRequestedFeature(feature).name
    psr_enable_status = True
    setup_time_verification_status = True
    if adapter.name not in common.GEN_11_PLATFORMS + ['TGL', 'RKL', 'DG1'] and (feature != UserRequestedFeature.PANEL_REPLAY):
        psr2_ctl = MMIORegister.read(
            'PSR2_CTL_REGISTER', 'PSR2_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
        srd_ctl = MMIORegister.read(
            'SRD_CTL_REGISTER', 'SRD_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)

        mode = display_config_.get_current_mode(panel.target_id)
        timing_data = display_config_.get_display_timings(panel.target_id)
        h_total = timing_data.hTotal
        v_total = timing_data.vTotal
        v_active = timing_data.vActive

        logging.debug(f"Mode data : VTotal : {v_total}, HTotal : {h_total}, VActive : {v_active}, Pixel Clock : {mode.pixelClock_Hz}Hz")
        # Multiply HTotal with no of segments if panel is MSO supported
        h_total_value = panel.mso_caps.no_of_segments * h_total if panel.mso_caps.is_mso_supported else h_total

        # calculate line time in micro secs
        line_time_in_us = round((h_total_value / float(mode.pixelClock_Hz / (1000 * 1000))), 3)
        logging.debug(f"line time in us = {line_time_in_us} us")
        vblank_time_in_us = (v_total - v_active) * line_time_in_us
        setup_time = PSR_SETUP_TIME[panel.psr_caps.setup_time]
        # For ADL+ platform the requirement to enable PSR is: PSR Setup time < VBlank time – 1 line time
        if setup_time <= (vblank_time_in_us - line_time_in_us):
            logging.info(f"{panel.port} doesn't have Setup Time Restriction")
            return True
        if adapter.name not in common.PRE_GEN_15_PLATFORMS:
            if feature > UserRequestedFeature.PSR_1:
                # In Gen-15 platforms, whenever there is Setup Time Restriction for the panel
                # VSC SDP will be sent one frame earlier to meet setup time so as to enable PSR1/PSR2
                logging.info(f"Panel's setup time {setup_time} > {vblank_time_in_us - line_time_in_us}"
                                f"(Vblank_time - line_time). Checking whether VSC SDP was sent one frame earlier")
                if not __verify_vsc_sdp_programming_one_frame_early(panel, feature, srd_ctl, psr2_ctl):
                    logging.error(f"Failed to verify VSC SDP entry one frame earlier on panel - {panel} in {adapter.name}")
                    return False
                # Check whether PSR is enabled when there is setup time restriction in the panel
                psr_enable_status = psr2_ctl.psr2_enable == 1
                if not psr_enable_status:
                    psr_disable_error_str = f"{feature_str} is not enabled on {panel.port} with Setup Time Restriction"
                    logging.error(f"FAIL : {psr_disable_error_str}")
                    gdhm.report_driver_bug_pc("[Powercons][PSR] " + psr_disable_error_str)
                    return False
                logging.info(f"Success : VSC SDP was sent one frame earlier and {feature_str} is enabled on {panel.port}")
                return True
            # Wa_16021150103 - Underrun is seen with PSR1 early frame capture feature due to a hw bug on LNL
            elif feature == UserRequestedFeature.PSR_1:
                    if adapter.name in ['LNL'] or (adapter.name in ['PTL'] and adapter.cpu_stepping == 0):
                        if srd_ctl.srd_enable:
                            logging.error(f"PSR1 not disabled on LNL or PTL A stepping system")
                            gdhm.report_driver_bug_pc("[Powercons][PSR] PSR1 not disabled for SetupTime restriction")
                            return False
                        logging.info(f"PSR Setup time restriction check failed and PSR disabled in driver on {panel.port}")
                        return None
                    else:
                        logging.info(f"Panel's setup time {setup_time} > {vblank_time_in_us - line_time_in_us}"
                             f"(Vblank_time - line_time). Checking whether VSC SDP was sent one frame earlier")
                        if not __verify_vsc_sdp_programming_one_frame_early(panel, feature, srd_ctl, psr2_ctl):
                            logging.error(f"Failed to verify VSC SDP entry one frame earlier on panel - {panel} in {adapter.name}")
                            return False
                        # Check whether PSR is enabled when there is setup time restriction in the panel
                        psr_enable_status = srd_ctl.srd_enable == 1
                        if not psr_enable_status:
                            psr_disable_error_str = f"{feature_str} is not enabled on {panel.port} with Setup Time Restriction"
                            logging.error(f"FAIL : {psr_disable_error_str}")
                            gdhm.report_driver_bug_pc("[Powercons][PSR] " + psr_disable_error_str)
                            return False
                        logging.info(f"Success : VSC SDP was sent one frame earlier and {feature_str} is enabled on {panel.port}")
                        return True


        # For Pre-Gen15 Platforms
        if feature >= UserRequestedFeature.PSR_2 and psr2_ctl.psr2_enable:
            setup_time_verification_status = False
        elif feature == UserRequestedFeature.PSR_1 and srd_ctl.srd_enable:
            setup_time_verification_status = False

        if not setup_time_verification_status:
            verification_error_str = f"{feature_str} is enabled when setup time {setup_time} > {vblank_time_in_us - line_time_in_us} (Vblank_time - line_time)"
            gdhm.report_driver_bug_pc("[Powercons][PSR] " + verification_error_str)
            return False
        logging.info(f"PSR Setup time restriction check failed and PSR disabled in driver on {panel.port}")
        # Returning None to skip PSR verification
        return None
    return True


##
# @brief        This function verifies PSR2 HBlank requirements
# @param[in]    adapter object
# @param[in]    panel object
# @return       True if verification successful else False
def verify_psr2_hblank_requirement(adapter, panel):
    assert adapter
    assert panel

    sku_name = machine_info.SystemInfo().get_sku_name(adapter.gfx_index)

    if panel.edp_caps.edp_revision >= dpcd.EdpDpcdRevision.EDP_DPCD_1_4_B:
        h_total = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + panel.transcoder,
                                    adapter.name, gfx_index=adapter.gfx_index)
        hblank = h_total.horizontal_total - h_total.horizontal_active
        hblank_time_ns = ((hblank * 1000 * 1000 * 1000) * 10 / panel.native_mode.pixelClock_Hz)
        # Display controller must completely transmit PSR2 SDPs with first and
        # last scan line indications in the horizontal blank region of the respective scan lines,
        # 100ns prior to the first pixel of the SU region.
        # However, this may not be possible for higher resolutions due to reduced blank duration.
        # If the PSR2 SDPs cannot be transmitted 100ns prior to the SU region, the eDP standard allows
        # display controller to transmit the PSR2 SDP during horizontal blanking of the previous scan line.
        # Bpsec link: https://gfxspecs.intel.com/Predator/Home/Index/49274 .
        # 1 PixelClockTime => 1/DotClockHz
        # *LinkSymbolClockHz = Bitrate/10
        lane_count = panel.max_lane_count
        link_rate_mbs = panel.link_rate * 1000
        # hblank check = (hblank time ns – (((60 / number of lanes) + 11) * 1000 / symbol clock frequency MHz) > 100 ns
        psr2_sdp_trans_time_ns = (((60 / lane_count) + 11) * 1000 * 10) / (link_rate_mbs / 10) + 0.5  # 0.5 tolerance
        psr2_sdp_scanline = (hblank_time_ns - psr2_sdp_trans_time_ns) < 1000
        psr2_ctl = MMIORegister.read(
            'PSR2_CTL_REGISTER', 'PSR2_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
        if psr2_sdp_scanline:
            if (adapter.name in common.GEN_12_PLATFORMS or (adapter.name in ['ADLP'] and sku_name not in ['RPLP'])) \
                    and psr2_ctl.psr2_enable:
                logging.error(f"PSR2 enabled when hblank is < 100 ns on {panel.port} on {adapter.name}")
                gdhm.report_driver_bug_pc("[PowerCons][PSR2] PSR2 enabled when hblank is < 100 ns")
                return False
            psr_confg = dpcd.SinkPsrConfiguration(panel.target_id)
            if psr_confg.su_region_scan_line_capture == 0:
                logging.error(f"su_region_scan_line_capture bit not set  in DPCD")
                gdhm.report_driver_bug_pc("[PowerCons][PSR2] su_region_scan_line_capture bit not set in DPCD")
            if psr2_ctl.psr2_enable == 0:
                logging.error(f"PSR2 not enabled when hblank is < 100 ns on {panel.port} on {adapter.name}")
                gdhm.report_driver_bug_pc("[PowerCons][PSR2] PSR2 not enabled when hblank is < 100 ns")
                return False
            if psr2_ctl.su_sdp_scanline_indication == 0:
                logging.error(f"su_region_scan_line_capture bit not set in PSR2_CTL register")
                gdhm.report_driver_bug_pc(
                    "[PowerCons][PSR2] su_region_scan_line_capture bit not set in PSR2_CTL register")
                return False
    return True


##
# @brief        This function configure PSR1/2 and then apply brightness change
# @param[in]    gfx_index object
# @param[in]    feature PSR1/PSR2/PR
# @param[in]    to_enable True/False
# @return       True if successful, False otherwise
def enable_disable_psr_with_brightness_change(gfx_index, feature, to_enable):
    if to_enable:
        psr_status = enable(gfx_index, feature)
    else:
        psr_status = disable(gfx_index, feature)
    if psr_status is False:
        return False
    if psr_status is True:
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            return False

    # WA for 14010407547 - make brightness work after disable/enable gfx-driver (fix will be in build 19575)
    if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
        blc.restart_display_service()
    # Doing brightness change to enable code path of AUX based and PSR client handling
    logging.info("\tSetting 75% brightness")
    if windows_brightness.set_current_brightness(75, 1) is False:
        # Avoiding fail of test as PSR verification is not dependent on brightness change
        logging.error("\t\tFAILED to apply 75% brightness")
        gdhm.report_bug(
            title="[PowerCons][BLC] Failed to apply 75% brightness in PSR test",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Test.DISPLAY_POWERCONS,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        return False
    logging.info("\t\tSuccessfully applied 75% brightness")
    return True


##
# @brief        This function verifies VSC SDP Header data
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    video_dip_ctl MMIO register Instance
# @param[in]    dip_ctl List of MMIO values
# @param[in]    enable_check True for PSR enable , False for disable
# @return       True if verification successful else False
def verify_sdp_data(adapter, panel, video_dip_ctl, dip_ctl, enable_check=False):
    status = True
    if adapter.name not in common.PRE_GEN_12_PLATFORMS:
        logging.info(f"Colorimetry Support on {panel.port} = {panel.hdr_caps.colorimetry_support}")
        video_dip_ctl.asUint = dip_ctl[-1].Data
        if panel.hdr_caps.is_hdr_supported:
            if panel.hdr_caps.colorimetry_with_sdp_supported is False:
                if (enable_check is False) and adapter.name in common.GEN_12_PLATFORMS and video_dip_ctl.vdip_enable_vsc:
                    logging.error(f"VDIP_ENABLE_VSC bit enabled for Aux based HDR Panel on {adapter.name}")
                    gdhm.report_driver_bug_pc("[PowerCons][PSR] VDIP VSC Enable Bit not enabled by driver for HDR Aux panel")
                    status = False
                elif adapter.name in common.GEN_13_PLATFORMS + ['MTL'] and video_dip_ctl.vdip_enable_vsc:
                    logging.error(f"VDIP_ENABLE_VSC bit enabled for Aux based HDR Panel on {adapter.name}")
                    gdhm.report_driver_bug_pc("[PowerCons][PSR] VDIP VSC Enable Bit enabled by driver for HDR Aux panel")
                    status = False
                if (panel.hdr_caps.colorimetry_support is False) and panel.hdr_caps.enable_sdp_override_aux:
                    logging.error("sdp_override_aux(BIT 7 in 344h) is set for Aux based HDR Panel")
                    gdhm.report_driver_bug_pc("[PowerCons][PSR] sdp_override_aux(344h) Bit 7 enabled on HDR Aux panel")
                    status = False
                logging.info("Aux Based HDR Panel connected. SKipping VSC SDP data check")
                return status
            if (panel.hdr_caps.enable_sdp_override_aux is False) and panel.hdr_caps.colorimetry_support:
                logging.error("sdp_override_aux(BIT 7 in 344h) bit is not set")
                gdhm.report_driver_bug_pc("[PowerCons][PSR] sdp_override_aux(344h) Bit 7 not enabled on HDR panel")
                status = False
        if panel.hdr_caps.colorimetry_support is False:
            # VSC DIP should not be enabled for non-colorimetry Panel due to H/W WA on GEN13
            if enable_check and (adapter.name in common.GEN_13_PLATFORMS + ['MTL'] and video_dip_ctl.vdip_enable_vsc):
                logging.error("vdip_enable_vsc bit is set by driver (Unexpected)")
                gdhm.report_driver_bug_pc("[PowerCons][PSR] VDIP VSC En"
                                          "able Bit set by driver when PSR enabled")
                status = False
            if adapter.name in common.GEN_12_PLATFORMS:
                # VSC SDP can still be used for PSR1/2 on GEN12
                if enable_check and (video_dip_ctl.vdip_enable_vsc == 0):
                    logging.error("vdip_enable_vsc bit is not set by driver (Unexpected)")
                    gdhm.report_driver_bug_pc("[PowerCons][PSR] VDIP VSC Enable Bit not enabled by driver")
                    status = False
                elif video_dip_ctl.vdip_enable_vsc and (enable_check is False):
                    logging.error("vdip_enable_vsc bit is set by driver (Unexpected)")
                    gdhm.report_driver_bug_pc("[PowerCons][PSR] VDIP VSC Enable Bit not disabled by driver")
                    status = False
        elif panel.hdr_caps.colorimetry_support:
            # For Gen12 - VSC DIP should be enabled for both PSR enable & disable
            # For Gen13 + MTL - VSC DIP should be enabled only for PSR disable case
            if adapter.name in common.GEN_12_PLATFORMS or (
                    adapter.name in common.GEN_13_PLATFORMS + ['MTL'] and (enable_check is False)):
                if video_dip_ctl.vdip_enable_vsc == 0:
                    logging.error("vdip_enable_vsc bit is not set by driver (Unexpected)")
                    gdhm.report_driver_bug_pc("[PowerCons][PSR] vdip_enable_vsc bit is not set by driver (Unexpected)")
                    status = False
            logging.info(f"vsc_select bit val = {video_dip_ctl.vsc_select}")
            if video_dip_ctl.vsc_select == 0x2:  # H/W controls data only
                info_frame = etl_parser.get_event_data(etl_parser.Events.INFO_FRAME_DATA)
                if info_frame is None:
                    logging.error("VSC DIP Data is not found in ETL")
                    gdhm.report_driver_bug_pc("[PowerCons][PSR] VSC DIP data not found in ETL")
                    return False
                # EX:{"Port":"PORT_A","Pipe":"PIPE_A","Protocol":"DD_PROTOCOL_DISPLAYPORT_EMBEDDED","DipType":"DIP_VSC",
                # "DipSize":23, "DipData":"00-07-04-0E-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00"}
                # DIP HEADER BYTES
                # HB0 - Secondary data Packet type = 0x0
                # HB1 - Secondary data Packet type = 0x7
                # HB2 - BIT [4:0] Revision Number
                #       01h - supports only 3D stereo
                #       02h - supports 3D stereo + PSR
                #       03h - supports 3D stereo + PSR2
                #       04h - supports 3D stereo + PSR/PSR2 + Y-co_ordinate
                #       05h - supports 3D stereo + PSR/PSR2 + Y-co_ordinate + Pixel Encoding/Colorimetry format
                #       06h - supports 3D stereo + PR + Y-co_ordinate
                #       07h - supports 3D stereo + PR + Y-co_ordinate + Pixel Encoding/Colorimetry format
                #      BIT [7:5] - Reserved - all Zeros
                # HB3 - BIT [4:0] Number of Valid data bytes
                #       01h - VSC SDP supports only 3D stereo (HB2 = 01h)
                #       08h - VSC SDP supports 3D stereo + PSR (HB2 = 02h)
                #       10h - VSC SDP supports 3D stereo + PR (HB2 = 06h)
                #       0Ch - VSC SDP supports 3D stereo + PSR2 (HB2 = 03h)
                #       0Eh - supports 3D stereo + PSR/PSR2 + Y-co_ordinate (HHB2 = 04h)
                #       13h - supports 3D stereo + PSR/PSR2 + Y-co_ordinate + Pixel Encoding/Colorimetry (HB2 = 05h)
                #       13h - supports 3D stereo + PR + Y-co_ordinate + Pixel Encoding/Colorimetry format (HB2 = 07h)
                #      BIT [7:5] - Reserved - all Zeros
                for vsc_data in info_frame:
                    if (vsc_data.Pipe == 'PIPE_' + panel.pipe) and (vsc_data.Port == "PORT_" + panel.port) \
                            and (vsc_data.Protocol == 'DD_PROTOCOL_DISPLAYPORT_EMBEDDED') and (
                            vsc_data.DipType == "DIP_VSC"):
                        sdp_data = vsc_data.DipData.split('-')
                        logging.info(f"VSC DIP Data= {sdp_data}")
                        if int(sdp_data[0]) != 0x0:
                            logging.error(f"HB0 val Expected= 0, Actual= {sdp_data[0]}")
                            status = False
                        if int(sdp_data[1]) != 0x7:
                            logging.error(f"HB1 val Expected= 0x7, Actual= {sdp_data[1]}")
                            status = False
                        if panel.pr_caps.is_pr_supported:
                            if int(sdp_data[2]) != 0x7:
                                logging.error(f"HB2 val Expected= 0x7, Actual= {sdp_data[2]}")
                                status = False
                            elif int(sdp_data[2]) != 0x5:
                                logging.error(f"HB2 val Expected= 0x5, Actual= {sdp_data[2]}")
                                status = False
                        if int(sdp_data[3]) != 0x13:
                            logging.error(f"HB3 val Expected= 0x13, Actual= {sdp_data[3]}")
                            status = False
                        pixel_encoding = int(sdp_data[16]) >> 4
                        colorimetry_format = int(sdp_data[16]) & 0xf
                        if pixel_encoding != SDP_DB16_PIXEL_ENCODING.RGB.value:
                            logging.error(f"DB16[7:4] pixel format Expected= 0(RGB),  Actual = {pixel_encoding}")
                            status = False
                        if colorimetry_format != SDP_RGB_COLORIMETRY_FORMAT.ITU_R_BT_2020_RGB.value:
                            logging.error(
                                f"DB16[3:0]colorimetry format Expected= 0x6(BT2020), Actual= {colorimetry_format}")
                            status = False
                        if int(sdp_data[17]) >> 7 != SDP_DB17_DYNAMIC_RANGE_TYPE.VESA_RANGE.value:
                            logging.error(f"DB17 Dynamic Range val Expected= 0x0(VESA), Actual= {sdp_data[17] >> 7}")
                            status = False
                        if panel.bpc != SDP_DB17_BPC_Type[int(sdp_data[17])]:
                            logging.error(f"DB17 BPC Expected= 0x2(BPC_10), Actual= {sdp_data[17]}")
                            status = False
                        if int(sdp_data[18]) != SDP_DB18_CONTENT_TYPE.NOT_DEFINED.value:
                            logging.error(f"DB17 BPC Expected= 0x0(Not Defined), Actual= {sdp_data[18]}")
                            status = False
    return status


##
# @brief        This function verifies PSR1 disable Sequence
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    driver_disable_etl ETL file
# @param[in]    h_total register instance
# @param[in]    v_total register instance
# @param[in]    check_idle_status Boolean True to check PSR1 Idle status, False to skip
# @return       True if verification successful else False
def verify_psr1_disable_sequence(adapter, panel, driver_disable_etl, h_total, v_total, check_idle_status=True):
    status = True
    psr_disable_time = 0
    plane_disable_time = 0
    psr_disable_in_sink = False


    srd_ctl = MMIORegister.get_instance("SRD_CTL_REGISTER", "SRD_CTL_" + panel.transcoder, adapter.name)
    srd_status = MMIORegister.get_instance("SRD_STATUS_REGISTER", "SRD_STATUS_" + panel.transcoder, adapter.name)
    video_dip_ctl = MMIORegister.get_instance('VIDEO_DIP_CTL_REGISTER', 'VIDEO_DIP_CTL_' + panel.transcoder,
                                              adapter.name)
    plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
    plane_ctl = MMIORegister.get_instance("PLANE_CTL_REGISTER", "PLANE_CTL_" + str(plane_id) + "_" + panel.pipe, adapter.name)
    etl_parser.generate_report(driver_disable_etl)

    srd_ctl_val = etl_parser.get_mmio_data(srd_ctl.offset, is_write=True)
    srd_status_val = etl_parser.get_mmio_data(srd_status.offset)
    plane_data = etl_parser.get_mmio_data(plane_ctl.offset, is_write=True)
    dip_ctl = etl_parser.get_mmio_data(video_dip_ctl.offset)
    if srd_ctl_val is None:
        logging.error(f"SRD_CTL_{panel.transcoder} data not found")
        return False
    if srd_status_val is None:
        logging.error(f"SRD_STATUS_{panel.transcoder} data not found")
        return False
    if plane_data is None:
        logging.error(f"PLANE_CTL_1_{panel.transcoder} data not found")
        return False
    if dip_ctl is None:
        logging.error(f"VIDEO_DIP_CTL_1_{panel.transcoder} data not found")
        return False
    aux = 'AUX_CHANNEL_' + panel.port.split('_')[1]
    psr_conf = etl_parser.get_dpcd_data(dpcd.Offsets.PSR_CONFIGURATION, channel=aux)
    if psr_conf is None:
        logging.error("DPCD 0x170H data not found")
        return False
    psr_configuration = dpcd.SinkPsrConfiguration(panel.target_id)
    for dpcd_data in psr_conf:
        if not dpcd_data.IsWrite:
            continue
        psr_configuration.value = int(dpcd_data.Data.split('-')[0], 16)
        if psr_configuration.psr_enable_in_sink == 0:
            psr_disable_in_sink = True
            break
    if psr_disable_in_sink is False:
        logging.error("driver did not disable psr in sink")
        gdhm.report_driver_bug_pc("[PowerCons][PSR] Driver did not disable PSR1 in sink")
        return False
    logging.info("PSR disabled in Sink DPCD(0x170h)")
    for val in srd_ctl_val:
        srd_ctl.asUint = val.Data
        if srd_ctl.srd_enable == 0:
            logging.info(f"PSR1 disabled at {val.TimeStamp}")
            psr_disable_time = val.TimeStamp
            break
    if psr_disable_time is None:
        logging.error("PSR1 is not disabled in driver")
        return False
    for plane in plane_data:
        plane_ctl.asUint = plane.Data
        if plane_ctl.plane_enable == 0:
            plane_disable_time = plane.TimeStamp
            logging.info(f"Plane{panel.pipe} is disabled at {plane.TimeStamp}")
            break
    if plane_disable_time == 0:
        logging.error(f"Plane_1_{panel.pipe} is not disabled during driver disable")
        status = False
    if psr_disable_time > plane_disable_time:
        logging.error("PSR1 is disabled after plane disable")
        status = False
    rr = round(
        float(panel.native_mode.pixelClock_Hz) / (
                (h_total.horizontal_total + 1) * (v_total.vertical_total + 1)), 3)
    logging.debug(f"Panel Refresh Rate = {rr}")
    if check_idle_status:
        # Max wait time for PSR1 IDLE state = 1 full frame + 7.5 m sec
        # https://gfxspecs.intel.com/Predator/Home/Index/49274
        time_out = round((1000 * 1) / rr + 7.5, 4)  # milli secs
        status &= __verify_psr1_idle_status(srd_ctl, srd_ctl_val, srd_status, srd_status_val, time_out)

    status &= verify_sdp_data(adapter, panel, video_dip_ctl, dip_ctl)
    return status


##
# @brief        This function verifies PSR1 Enable Sequence
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    etl_file ETL file
# @return       True if verification successful else False
def verify_psr1_enable_sequence(adapter, panel, etl_file):
    status = True
    psr_enable_time = 0
    plane_enable_time = 0
    psr_enable_in_sink = False

    srd_ctl = MMIORegister.get_instance("SRD_CTL_REGISTER", "SRD_CTL_" + panel.transcoder, adapter.name)
    srd_status = MMIORegister.get_instance("SRD_STATUS_REGISTER", "SRD_STATUS_" + panel.transcoder, adapter.name)
    video_dip_ctl = MMIORegister.get_instance('VIDEO_DIP_CTL_REGISTER', 'VIDEO_DIP_CTL_' + panel.transcoder,
                                              adapter.name)
    plane_id = planes_verification.get_plane_id_from_layerindex(1, 0, adapter.gfx_index)
    plane_ctl = MMIORegister.get_instance("PLANE_CTL_REGISTER", "PLANE_CTL_" + str(plane_id) + "_" + panel.pipe, adapter.name)
    etl_parser.generate_report(etl_file)

    srd_ctl_val = etl_parser.get_mmio_data(srd_ctl.offset, is_write=True)
    srd_status_val = etl_parser.get_mmio_data(srd_status.offset)
    plane_data = etl_parser.get_mmio_data(plane_ctl.offset, is_write=True)
    dip_ctl = etl_parser.get_mmio_data(video_dip_ctl.offset)
    if srd_ctl_val is None:
        logging.error(f"SRD_CTL_{panel.transcoder} data not found")
        return False
    if srd_status_val is None:
        logging.error(f"SRD_STATUS_{panel.transcoder} data not found")
        return False
    if plane_data is None:
        logging.error(f"PLANE_CTL_1_{panel.transcoder} data not found")
        return False
    if dip_ctl is None:
        logging.error(f"VIDEO_DIP_CTL_1_{panel.transcoder} data not found")
        return False
    aux = 'AUX_CHANNEL_' + panel.port.split('_')[1]
    psr_conf = etl_parser.get_dpcd_data(dpcd.Offsets.PSR_CONFIGURATION, channel=aux)
    if psr_conf is None:
        logging.error("DPCD 0x170H data not found")
        return False
    psr_configuration = dpcd.SinkPsrConfiguration(panel.target_id)
    for dpcd_data in psr_conf:
        if not dpcd_data.IsWrite:
            continue
        psr_configuration.value = int(dpcd_data.Data.split('-')[0], 16)
        if psr_configuration.psr_enable_in_sink:
            psr_enable_in_sink = True
            break
    if psr_enable_in_sink is False:
        logging.error("driver did not enable psr in sink")
        gdhm.report_driver_bug_pc("[PowerCons][PSR] Driver did not enable PSR1 in sink")
        return False
    logging.info("Driver enabled PSR1 in sink via DPCD (0x170h)")
    for val in plane_data:
        plane_ctl.asUint = val.Data
        if plane_ctl.plane_enable:
            logging.info(f"Plane{panel.pipe} is enabled at {val.TimeStamp}")
            plane_enable_time = val.TimeStamp
            break
    # No need to proceed if plane is not enabled
    if plane_enable_time == 0:
        logging.error(f"Plane{panel.pipe} is not enabled")
        return False
    for val in srd_ctl_val:
        srd_ctl.asUint = val.Data
        if srd_ctl.srd_enable:
            psr_enable_time = val.TimeStamp
            break
    if not psr_enable_time:
        logging.error(f"PSR1 not enabled by driver on {panel.port}")
        status = False
    if plane_enable_time > psr_enable_time:
        logging.error("PSR1 is enabled before plane enable")
        status = False
    status &= verify_sdp_data(adapter, panel, video_dip_ctl, dip_ctl, True)
    return status


##
# @brief        Helper function to verify psr1 idle status
# @param[in]    srd_ctl register instance
# @param[in]    srd_val list of PSR1 control register values
# @param[in]    srd_status register instance
# @param[in]    srd_status_val list of PSR1 status register values
# @param[in]    time_out in ms, before which PSR1 should be in idle state
# @return      True if PSR1 returned to IDLE state in a given time, False otherwise
def __verify_psr1_idle_status(srd_ctl, srd_val, srd_status, srd_status_val, time_out):
    logging.info("Verifying PSR1 Idle Status")
    for val in srd_val:
        srd_ctl.asUint = val.Data
        if srd_ctl.srd_enable == 0:
            for status in srd_status_val:
                srd_status.asUint = status.Data
                if srd_status.srd_state == 0:  # IDLE state
                    if status.TimeStamp > (val.TimeStamp + time_out):
                        logging.error(f"PSR1 not returned to IDLE state before {time_out} ms")
                        return False
                    logging.info(f"PSR1 returned to IDLE state at {status.TimeStamp} ms")
                    return True
    logging.error("PSR1 did not return to IDLE state")
    gdhm.report_bug(
        title="[Powercons][PSR]PSR1 did not return to IDLE state",
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )
    return False


##
# @brief        Helper function to verify psr2 clock gate WA
# @param[in]    adapter Adapter instance
# @param[in]    panel Panel instance
# @param[in]    enable_disable_time  time in ms w.r.t Psr enable/disable
# @param[in]    enable_check True if WA needs to be during psr enable False to check in PSR disable case
# @return      True if successful, False otherwise
def check_clk_gate_wa(adapter, panel, enable_disable_time, enable_check=True):
    clk_gate_wa_enable_time = 0
    clk_gate_wa_disable_time = 0
    sku_name = machine_info.SystemInfo().get_sku_name(adapter.gfx_index)
    if adapter.name in common.GEN_13_PLATFORMS or (adapter.name in ['MTL'] and sku_name not in ['ARL'] and (adapter.cpu_stepping == 0)):
        # HSD - 1509248917 WA - 21st bit CLKGATE_DIS_MISC should be set before PSR2 enable
        clk_gate_misc = MMIORegister.get_instance("CLKGATE_DIS_MISC_REGISTER", "CLKGATE_DIS_MISC", adapter.name)
        clk_gate_misc_data = etl_parser.get_mmio_data(clk_gate_misc.offset, is_write=True)
        if clk_gate_misc_data is None:
            logging.error(f"CLKGATE_DIS_MISC register data not found for {panel.transcoder}")
            return False
        for val in clk_gate_misc_data:
            clk_gate_misc.asUint = val.Data
            if enable_check:
                if clk_gate_misc.dmasc_gating_dis:
                    clk_gate_wa_enable_time = val.TimeStamp
                    break
            else:
                if clk_gate_misc.dmasc_gating_dis == 0:
                    clk_gate_wa_disable_time = val.TimeStamp
                    break
        if enable_check:
            if clk_gate_wa_enable_time == 0:
                logging.error("DmascGatingDis bit is not set by driver in CLKGATE_DIS_MISC Register")
                return False
            if clk_gate_wa_enable_time > enable_disable_time:
                logging.error("CLKGATE_DIS_MISC WA enabled after PSR enable (Unexpected)")
                return False
        else:
            if clk_gate_wa_disable_time == 0:
                logging.error("DmascGatingDis bit is not set by driver in CLKGATE_DIS_MISC Register")
                return False
            if clk_gate_wa_disable_time < enable_disable_time:
                logging.error("CLKGATE_DIS_MISC WA disabled before PSR disable (Unexpected)")
                return False
    return True


##
# @brief        This function verifies PSR1 & 2 restrictions
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    feature Enum PSR1/PSR2
# @return       feature Updated PSR feature version based on restrictions
def verify_psr_restrictions(adapter, panel, feature):
    if panel.pipe not in ['A', 'B']:
        logging.warning(f"PSR is not supported in Pipe-{panel.pipe}")
        return UserRequestedFeature.PSR_NONE
 
    if verify_psr_setup_time(adapter, panel, feature) is None:
        feature = UserRequestedFeature.PSR_NONE
    elif feature >= UserRequestedFeature.PSR_2:
        status = verify_psr2_vblank_support(adapter, panel)
        status &= verify_psr2_hblank_requirement(adapter, panel)
        if status is False:
            logging.info("PSR2 restrictions failed. Falling back to PSR1")
            feature = UserRequestedFeature.PSR_1
    return feature


##
# @brief        This function verifies WA for Delayed Vblank PSR supported panels
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    feature PSR_1/PSR_2
# @return       True if successful, False otherwise
def delayed_vblank_wa_check(adapter, panel, feature):
    if adapter.name not in common.GEN_12_PLATFORMS + common.GEN_13_PLATFORMS:
        return True
    if panel.psr_caps.is_psr2_supported is False:
        return True
    if is_psr_enabled_in_driver(adapter, panel, feature) is False:
        logging.info("Skipping Chicken Bit WA check for PSR disable case")
        return True
    # TODO: Enhance the verification for intercepted vblank for ADL . Until that restricting to GEN12
    # HSD-16014531253 WA :In high RR PSR panel set chicken bit so that high fixed LP7 watermark wont be selected by HW
    dcpr = MMIORegister.read("CHICKEN_DCPR_1_REGISTER", "CHICKEN_DCPR_1", adapter.name)
    if adapter.name in common.GEN_12_PLATFORMS:
        wm = MMIORegister.read("PLANE_WM_REGISTER", "PLANE_WM_7_1_" + panel.pipe, adapter.name)
    else:
        # HSD-16017372373 - Max LP WM level supported is 5 from GEN13 onwards
        wm = MMIORegister.read("PLANE_WM_REGISTER", "PLANE_WM_5_1_" + panel.pipe, adapter.name)
    delayed_vblank = is_delayed_vblank_supported(adapter, panel)
    # Chicken bit WA will be programmed for LP7WM disabled case / delayed Vblank
    if (adapter.name in common.GEN_12_PLATFORMS and (delayed_vblank or (wm.enable == 0))) or (
            adapter.name in common.GEN_13_PLATFORMS and (wm.enable == 0)):
        if panel.pipe == 'A' and dcpr.spare23 == 0:
            logging.error(f'Spare23 bit is not set for delayed vblank mode on {panel.port}')
            return False
        elif panel.pipe == 'B' and dcpr.spare24 == 0:
            logging.error(f'Spare24 bit is not set for delayed vblank mode on {panel.port}')
            return False
        logging.info(f'PASS: Chicken Bit is set for delayed vblank mode on {panel.port}')
    else:
        if panel.pipe == 'A' and dcpr.spare23 == 1:
            logging.error(f'Spare23 bit is set for non-delayed vblank mode on {panel.port}')
            return False
        elif panel.pipe == 'B' and dcpr.spare24 == 1:
            logging.error(f'Spare24 bit is set for non-delayed vblank mode on {panel.port}')
            return False
        logging.info(f'PASS: Chicken Bit is not set for non-delayed vblank mode on {panel.port}')
    return True


##
# @brief        This function check delayed vblank support for the given panel
# @param[in]    adapter object
# @param[in]    panel object
# @return       True if supported, False otherwise
def is_delayed_vblank_supported(adapter, panel):
    v_total = MMIORegister.read("TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_" + panel.transcoder, adapter.name)
    v_blank = MMIORegister.read("TRANS_VBLANK_REGISTER", "TRANS_VBLANK_" + panel.transcoder, adapter.name)
    if v_total.vertical_active != v_blank.vertical_blank_start:
        logging.info(f"Delayed vblank supported on {panel.port}")
        return True
    logging.info(f"Delayed vblank not supported on {panel.port}")
    return False


##
# @brief        This function enable/disable the delayed Vblank support using regkey
# @param[in]    adapter object
# @param[in]    enable_flag TRUE/FALSE
# @return       True if write is successful, False if failed, None if expected value is already present
def enable_disable_delayed_vblank_support(adapter, enable_flag):
    return registry.write(adapter.gfx_index, registry.RegKeys.DISPLAY_SW_WA_CONTROL, registry_access.RegDataType.DWORD,
                          0x0 if enable_flag else 0x2)


##
# @brief        Exposed API to reset PSR1 Setup Time Override using registry
# @param[in]    adapter Adapter
# @param[in]    panel Panel Object
# @return       True if registry deletion is successful False otherwise
def reset_psr1_setup_override(adapter, panel):
    reg_key = registry.RegKeys.PSR.PSR1_SETUP_TIME_OVERRIDE + panel.pnp_id
    delete_status = registry.delete(adapter.gfx_index, key=reg_key)
    if delete_status is False:
        logging.error(f"\tFailed to delete Reg Key {reg_key} after the verification")
    elif delete_status is None:
        logging.warning(f"\tRegKey {reg_key} was not found")
    return delete_status


##
# @brief        Exposed API to enable/disable PSR via IGCL
# @param[in]    panel - object of Panel
# @param[in]    enable_psr - Boolean
# @param[in]    pwr_src
# @param[in]    power_plan
# @return       True for success, False for failed. None for not-applicable
def enable_disable_psr_via_igcl(panel, enable_psr=True, pwr_src= None, power_plan= None):
    # IGCL is supported from Gen13 onwards
    if common.PLATFORM_NAME in common.PRE_GEN_13_PLATFORMS:
        return None
    # @todo make sure that PSR2 is supported before proceeding
    psr_pwr_opt_settings = control_api_args.ctl_power_optimization_settings_t()
    psr_pwr_opt_settings.Size = ctypes.sizeof(psr_pwr_opt_settings)
    if pwr_src is not None:
        psr_pwr_opt_settings.PowerSource = pwr_src
    if power_plan is not None:
        psr_pwr_opt_settings.PowerOptimizationPlan = power_plan
    psr_pwr_opt_settings.Enable = enable_psr
    psr_pwr_opt_settings.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.PSR.value
    if control_api_wrapper.set_psr(psr_pwr_opt_settings, panel.target_id) is False:
        logging.error(f"\t\tFAILED to {'enable' if enable_psr else 'disable'} PSR via IGCL on {panel.port}")
        return False
    logging.info(f"\t\tPSR {'enabled' if enable_psr else 'disabled'} successfully via IGCL on {panel.port}")
    return True


##
# @brief        Exposed API to get PSR status via IGCL
# @param[in]    panel Panel Object
# @param[in]    feature PSR feature
# @param[in]    pwr_src
# @param[in]    power_plan
# @return       True if PSR is Enabled, False if disabled, None if status check is failed
def get_status_via_igcl(panel, feature, pwr_src= None, power_plan= None):
    get_psr = control_api_args.ctl_power_optimization_settings_t()
    get_psr.Size = ctypes.sizeof(get_psr)
    get_psr.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.PSR.value
    if pwr_src is not None:
        get_psr.PowerSource = pwr_src
    if power_plan is not None:
        get_psr.PowerOptimizationPlan = power_plan
    if not control_api_wrapper.get_psr(get_psr, panel.target_id):
        logging.error("\t\tFail: Get PSR status via IGCL")
        report_gdhm('Failed to get PSR status via IGCL', feature)
        return None
    # @todo Note: PSR Version and FullFetchUpdate fields are not populated from Control Library DLL
    logging.info(f"\t\tPSR from IGCL : Version = {get_psr.FeatureSpecificData.PSRInfo.PSRVersion}, "
                 f"FullFetchUpdate = {get_psr.FeatureSpecificData.PSRInfo.FullFetchUpdate}")
    return True if get_psr.Enable else False


##
# @brief        Helper API to file GDHM bug during PSR failure scenarios
# @param[in]    title - GDHM bug title message
# @param[in]    psr_feature - GDHM bug title message
# @return       None
def report_gdhm(title, psr_feature):
    feature_str = UserRequestedFeature(psr_feature).name
    gdhm.report_bug(
        title=f"[PowerCons] [{feature_str}]" + title,
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )


##
# @brief        Exposed API to verify Selective Update region programming
# @param[in]    psr2_man_trk - PSR2 Manual Track register offset
# @param[in]    v_active - V Active region of the current/native mode
# @return       True if driver is programming full frame co-ordinates, False otherwise
def verify_su_region_programming(psr2_man_trk, v_active):
    actual_su_start_address = psr2_man_trk.su_region_start_address
    actual_su_end_address = psr2_man_trk.su_region_end_address

    if actual_su_start_address != 0 or actual_su_end_address != v_active - 1:
        logging.error(f"\tFAIL : Expected SU region (start, end) = (0, {v_active - 1}), Actual SU region(start, end) = "
                      f"({actual_su_start_address}, {actual_su_end_address})")
        return False
    logging.info(f"\tPASS : Expected SU region (start, end) = (0, {v_active - 1}), Actual SU region(start, end) = "
                 f"({actual_su_start_address}, {actual_su_end_address})")
    return True


# @brief        Exposed API to verify whether VSC SDP is sent one frame earlier for panels with setup time retriction in Gen-15
# @param[in]    panel - Object of Panel
# @param[in]    feature - PSR feature
# @param[in]    srd_ctl - register instance
# @param[in]    psr2_ctl - register instance
# @return       True for verification success, False for verification failure
def __verify_vsc_sdp_programming_one_frame_early(panel, feature, srd_ctl, psr2_ctl):
    aux = 'AUX_CHANNEL_' + panel.port.split('_')[1]
    is_frame_capture_bit_set = True
    etl_file_path = None

    if srd_ctl.psr_entry_setup_frames != 1:
        logging.error("\tPSR Entry Set-Up Frames bit is not set in SRD_CTL Register")
        gdhm.report_driver_bug_pc("[PowerCons][PSR] PSR Entry Set-Up Frames bit is not set in SRD_CTL Register")
        return False
    logging.info(f"\tPASS : PSR Entry Set-up frames bit is set to 1 in SRD_CTL register")

    # Stop the ETL tracer started during TestEnvironment initialization
    if etl_tracer.stop_etl_tracer() is False:
        logging.error("Failed to stop ETL trace")
        return False

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTrace_SDP_Verification' + '_' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL trace")
        return False
    if etl_parser.generate_report(etl_file_path) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        return False
    logging.info("\tSuccessfully generated ETL Parser report")

    etl_psr_cfg_data = etl_parser.get_dpcd_data(dpcd.Offsets.PSR_CONFIGURATION, channel=aux)
    sink_psr_cfg = dpcd.SinkPsrConfiguration(panel.target_id)
    if etl_psr_cfg_data is None:
        logging.error("No PSR Configuration data found in ETL")
        gdhm.report_driver_bug_pc("[PowerCons][PSR] No PSR Configuration data found in ETL")
        return False
    # Check whether the last read/write of PSR Configuration field in DPCD has Frame Capture Indication bit set
    logging.debug(f"PSR Configuration DPCD Data in ETL : {etl_psr_cfg_data}")
    last_cfg_write_data = etl_psr_cfg_data[-1]
    sink_psr_cfg.value = int(last_cfg_write_data.Data.split('-')[0], 16)
    if sink_psr_cfg.frame_capture_indication != 1:
        is_frame_capture_bit_set = False

    if not is_frame_capture_bit_set:
        logging.error("\tFrame Capture Indication field is not set in DPCD")
        gdhm.report_driver_bug_pc("[PowerCons][PSR] Frame Capture Indication field is not set in DPCD")
        return False
    logging.info("\tPASS : Frame Capture Indication field is set to 1 in DPCD")

    if feature >= UserRequestedFeature.PSR_2 and psr2_ctl.frame_before_su_entry < srd_ctl.psr_entry_setup_frames:
        logging.error("\tFrames Before SU Entry must be programmed to be greater than the Entry setup time")
        gdhm.report_driver_bug_pc("[PowerCons][PSR] Frames Before SU Entry is programmed to be lesser than the Entry setup time")
        return False
    logging.info(f"\tPASS : Frames Before SU Entry is greater than the Entry setup time")

    return True


