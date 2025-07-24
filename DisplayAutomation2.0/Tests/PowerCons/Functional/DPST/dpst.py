########################################################################################################################
# @file         dpst.py
# @brief        This file contains DPST/OPST verification APIs
#
# @author       Ashish Tripathi
########################################################################################################################
import ctypes
import datetime
import json
import logging
import math
import os
import random
import re
import shutil
import subprocess
import time
from enum import IntEnum
from random import randint, randrange

import win32api

from Libs.Core import etl_parser, window_helper, registry_access, display_essential
from Libs.Core import winkb_helper as kb
from Libs.Core import display_power
from Libs.Core.logger import etl_tracer, gdhm, html
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Core.vbt import vbt
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Libs.Feature.powercons import registry
from Libs.Feature.vdsc import dsc_verifier
from Tests.PowerCons.Functional.BLC import blc
from Tests.PowerCons.Functional.PSR import psr_util, psr
from Tests.PowerCons.Modules import validator_runner, dpcd, common, workload, polling
from Tests.PowerCons.Modules.dut_context import Panel, Adapter
from Tests.PowerCons.Modules.workload import PowerSource, change_power_source
from registers.mmioregister import MMIORegister

__APPLICATIONS_FOLDER = os.path.join(test_context.SHARED_BINARY_FOLDER, "Applications")
__DIANA_EXE = os.path.join(test_context.SHARED_BINARY_FOLDER, "DiAna\\DiAna.exe")

MAX_SFSU_DPST_SEGMENTS = 128
MIN_SFSU_DPST_SEGMENT_SIZE = 32


##
# @brief        DPST parameters
class DpstParameters(IntEnum):
    FEATURE_STATUS = 0
    AGGRESSIVENESS_LEVEL = 1
    EPSM_STATUS = 2


##
# @brief        DPST/OPST status
class Status(IntEnum):
    DISABLED = 0
    ENABLED = 1


##
# @brief        PanelType
class PanelType(IntEnum):
    LCD = 0
    OLED = 1


##
# @brief        Threshold INF for DPST/OPST
class Threshold(IntEnum):
    OLD = 0
    LOWER = 1
    UPPER = 2


##
# @brief        Method of Workload used for DPST/OPST tests
class WorkloadMethod(IntEnum):
    IDLE = 0
    PSR_UTIL = 1
    GOLDEN_IMAGE = 2


##
# @brief        Type of Event to be used for Workload
class FrameChangeType(IntEnum):
    NONE = 0
    SINGLE = 1
    CONTINUOUS = 2


##
# @brief        Type of Workload used for DPST/OPST tests
class WindowMode(IntEnum):
    FULLSCREEN = 0
    WINDOWED = 1
    PSR_UTIL = 1


##
# @brief        Type of Aggressiveness level for DPST feature
class Aggressiveness(IntEnum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5
    LEVEL_6 = 6


##
# @brief        Enum maintained to have list of features to be used for respective concurrency test.
class Feature(IntEnum):
    NONE = 0
    FBC = 1
    HDR = 2
    LACE = 3
    _3DLUT = 4
    PIPE_SCALAR = 5
    VDSC = 6


##
# @brief         Exposed object of XPST status
class XpstStatus(object):
    ##
    # @brief       Initializer for XPST Status instances
    def __init__(self):
        self.is_dpst_enabled = False
        self.is_dpst_supported = False
        self.is_opst_enabled = False
        self.is_opst_supported = False
        self.is_epsm_supported = False
        self.is_epsm_enabled = False
        self.min_level = 0
        self.max_level = 0
        self.current_level = 0

    ##
    # @brief       Function to get the string format of XpstStatus object
    # @return      string representation of the XpstStatus object
    def __repr__(self):
        return \
            f"DPST(Support={self.is_dpst_supported}, Status={self.is_dpst_enabled}), " \
            f"EPSM(Support={self.is_epsm_supported}, Status={self.is_epsm_enabled}), " \
            f"OPST(Support={self.is_opst_supported}, Status={self.is_opst_enabled}," \
            f"Level(Min={self.min_level}, Max={self.max_level}, Current={self.current_level})"


##
# @brief         Exposed object of XPST VBT params
class XpstVbtParams(object):
    ##
    # @brief       Initializer for XPST VBT params
    def __init__(self):
        self.dpst_status = None
        self.opst_status = None
        self.dpst_level = None
        self.opst_level = None

    ##
    # @brief       Function to get the string format of XpstVbtParams object
    # @return      string representation of the XpstVbtParams object
    def __repr__(self):
        return \
            f"DPST in VBT(Status= {self.dpst_status}, Level= {self.dpst_level}), " \
            f"OPST in VBT(Status= {self.opst_status}, Level= {self.opst_level})"

    ##
    # @brief       Function to compare the equality of the class
    # @param[in]   other class, another class to compare with self
    # @return      bool, True if equal else False
    def __eq__(self, other):
        if not isinstance(other, XpstVbtParams):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.dpst_status == other.dpst_status and self.dpst_level == other.dpst_level and \
            self.opst_status == other.opst_status and self.opst_level == other.opst_level


##
# @brief        Enum maintained to have list of XPST features to be used
class XpstFeature(IntEnum):
    DPST = 0
    OPST = 1


##
# @brief        Exposed API to enable DPST default settings
#               enable DPST Feature, Set aggressiveness level= 6, Disable EPSM
# @param[in]     adapter object of Adapter
# @param[in]     bpp_override boolean, DPST on 6BPC panel
# @return        status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise
def enable(adapter, bpp_override=False):
    assert adapter

    logging.info("Applying DPST default settings")
    override_status = None
    if bpp_override:
        override_status = set_bpp_override(adapter, override=True)
        if override_status is False:
            return False

    # Enable DPST feature
    logging.info("STEP: Enabling DPST feature")
    feature_test_control = registry.FeatureTestControl(adapter.gfx_index)
    dpst_status = None
    if feature_test_control.dpst_disable != registry.RegValues.DISABLE:
        feature_test_control.dpst_disable = registry.RegValues.DISABLE
        dpst_status = feature_test_control.update(adapter.gfx_index)
        if dpst_status is False:
            logging.error("FAILED to enable DPST feature")
            return False
    logging.info("\tSuccessfully enabled DPST feature")

    # set Aggressiveness level= 6
    aggressiveness_status = set_dpst_aggressiveness_level(adapter)
    if aggressiveness_status is False:
        return False

    # Disable EPSM
    epsm_status = set_epsm(adapter)
    if epsm_status is False:
        return False

    logging.info("Successfully applied DPST default settings")
    return override_status or dpst_status or aggressiveness_status or epsm_status


##
# @brief         Exposed API to disable DPST
# @param[in]     adapter object, Adapter
# @return        status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
def disable(adapter):
    assert adapter

    feature_test_control = registry.FeatureTestControl(adapter.gfx_index)
    status = None
    if feature_test_control.dpst_disable != registry.RegValues.ENABLE:
        feature_test_control.dpst_disable = registry.RegValues.ENABLE
        status = feature_test_control.update(adapter.gfx_index)
        if status is False:
            logging.error("FAILED to disable DPST in the driver")
            return False
    logging.info("Successfully disabled DPST in the driver")
    return status


##
# @brief         Exposed API to set dpst bpp override
# @param[in]     adapter object, Adapter
# @param[in]     override boolean
# @return        status Boolean, True success & restart required, None success & no restart required, False otherwise
def set_bpp_override(adapter=None, override=True):
    gfx_index = 'gfx_0'
    if adapter is not None:
        gfx_index = adapter.gfx_index
    registry.delete(gfx_index, key=registry.RegKeys.DC_POWER_POLICY_DATA)
    registry.delete(gfx_index, key=registry.RegKeys.AC_POWER_POLICY_DATA)
    registry.delete(gfx_index, key=registry.RegKeys.POWER_PLAN_AWARE_SETTINGS)

    value = registry.RegValues.ENABLE if override else registry.RegValues.DISABLE
    reg_key = registry.RegKeys.DPST.OVERRIDE_BPP

    logging.info(f"STEP: Updating {reg_key}= {value} on {gfx_index}")
    status = registry.write(gfx_index, reg_key, registry_access.RegDataType.DWORD, value)
    if status is False:
        logging.error(f"FAILED to update {reg_key}= {value} for 6BPC")
        return False
    logging.info(f"\tSuccessfully updated {reg_key}= {value} for 6BPC")
    return status


##
# @brief        Exposed API to get the aggressive level from INF
# @param[in]    adapter object, Adapter
# @return       registry value if registry read is successful, None otherwise
def get_aggressive_level(adapter):
    reg_key = registry.RegKeys.DPST.AGGRESSIVENESS_LEVEL
    level = registry.read(adapter.gfx_index, reg_key)
    if level is None:
        logging.error(f"FAILED to read Reg key= {reg_key}")
    return level


##
# @brief         Exposed API to set dpst aggressiveness level
# @param[in]     adapter object, Adapter
# @param[in]     level int, Dpst aggressiveness level
# @return        status Boolean, True success & restart required, None success & no restart required, False otherwise
def set_dpst_aggressiveness_level(adapter=None, level=6):
    gfx_index = 'gfx_0'
    if adapter is not None:
        gfx_index = adapter.gfx_index
    registry.delete(gfx_index, key=registry.RegKeys.DC_POWER_POLICY_DATA)
    registry.delete(gfx_index, key=registry.RegKeys.AC_POWER_POLICY_DATA)
    registry.delete(gfx_index, key=registry.RegKeys.POWER_PLAN_AWARE_SETTINGS)
    reg_key = registry.RegKeys.DPST.AGGRESSIVENESS_LEVEL

    logging.info(f"STEP: Updating {reg_key}= {level} on {gfx_index}")
    status = registry.write(gfx_index, reg_key, registry_access.RegDataType.BINARY, bytes([level]))
    if status is False:
        logging.error(f"FAILED to apply {reg_key}= {level}")
        return False
    logging.info(f"\tSuccessfully applied {reg_key}= {level}")
    return status


##
# @brief         Exposed API to set dpst aggressiveness level
# @param[in]     adapter object, Adapter
# @param[in]     weight int, Dpst Epsm Weight 70 - 100
# @return        status Boolean, True success & restart required, None success & no restart required, False otherwise
def set_epsm_weight(adapter, weight):
    reg_key = registry.RegKeys.DPST.EPSM_WEIGHT
    # this regkey should be value less than 100 from DPST8.0 so that EPSM support will be ON
    logging.info(f"Updating {reg_key} to {weight} on {adapter.gfx_index}")
    status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, weight)
    if status is False:
        logging.error(f"\tFAILED to update {reg_key}= {weight}")
    elif status is True:
        logging.info(f"\tSuccessfully updated {reg_key}= {weight}")
    elif status is None:
        logging.info(f"\tValue already set for {reg_key}= {weight}")

    return status


##
# @brief         Exposed API to set dpst EPSM(Enhanced Power Saving Mode)
# @param[in]     adapter object, Adapter
# @param[in]     disable_epsm boolean
# @return        status Boolean, True success & restart required, None success & no restart required, False otherwise
def set_epsm(adapter, disable_epsm=True):
    do_driver_restart = None
    status = registry.delete(adapter.gfx_index, key=registry.RegKeys.DC_POWER_POLICY_DATA)
    if status is False:
        logging.error(f"FAILED to delete {registry.RegKeys.DC_POWER_POLICY_DATA}")
        return False
    if status is True:
        do_driver_restart = True

    status = registry.delete(adapter.gfx_index, key=registry.RegKeys.AC_POWER_POLICY_DATA)
    if status is False:
        logging.error(f"FAILED to delete {registry.RegKeys.AC_POWER_POLICY_DATA}")
        return False
    if status is True:
        do_driver_restart = True

    status = registry.delete(adapter.gfx_index, key=registry.RegKeys.POWER_PLAN_AWARE_SETTINGS)
    if status is False:
        logging.error(f"FAILED to delete {registry.RegKeys.POWER_PLAN_AWARE_SETTINGS}")
        return False
    if status is True:
        do_driver_restart = True

    sku_name = None
    if adapter.name in ['ADLP']:
        sku_name = machine_info.SystemInfo().get_sku_name(adapter.gfx_index)

    if adapter.name not in common.PRE_GEN_14_PLATFORMS or (sku_name in ['TwinLake']):
        reg_key = registry.RegKeys.DPST.EPSM_WEIGHT
        # this regkey should be value less than 100 from DPST8.0 so that EPSM support will be ON
        logging.info(f"Updating {reg_key} to 99 on {adapter.gfx_index}")
        status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, 0x63)
        if status is False:
            logging.error(f"\tFAILED to update {reg_key}= 99")
            return False
        logging.info(f"\tSuccessfully updated {reg_key}= 99")
        if status is True:
            do_driver_restart = True

    if disable_epsm:
        status = registry.delete(adapter.gfx_index, registry.RegKeys.DPST.EPSM_WEIGHT)
        if status is False:
            logging.error(f"FAILED to delete {registry.RegKeys.DPST.EPSM_WEIGHT}")
            return False
        if status is True:
            do_driver_restart = True

    reg_key = registry.RegKeys.DPST.EPSM_STATUS
    value = 0 if disable_epsm else 1
    logging.info(f"{'Disabling' if disable_epsm else 'Enabling'} EPSM feature on {adapter.gfx_index}")
    status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, value)
    if status is False:
        logging.error(f"\tFAILED to update {reg_key}= {value}")
        return False
    logging.info(f"\tSuccessfully updated {reg_key}= {value}")
    if status is True:
        do_driver_restart = True

    return do_driver_restart


##
# @brief         Exposed API to set dpst backlight threshold
# @param[in]     adapter object, Adapter
# @param[in]     reg_type enum, BlcThreshold type
# @param[in]     value int, Dpst threshold percent/milli percent
# @return        status Boolean, True success & restart required, None success & no restart required, False otherwise
def set_dpst_backlight_threshold(adapter=None, reg_type=Threshold.OLD, value=15):
    gfx_index = 'gfx_0'
    if adapter is not None:
        gfx_index = adapter.gfx_index

    if reg_type == Threshold.OLD:
        reg_key = registry.RegKeys.DPST.DPST_BACKLIGHT_THRESHOLD
    elif reg_type == Threshold.LOWER:
        reg_key = registry.RegKeys.DPST.DPST_BACKLIGHT_THRESHOLD_LOWER
    else:
        reg_key = registry.RegKeys.DPST.DPST_BACKLIGHT_THRESHOLD_UPPER

    logging.info(f"STEP: Updating {reg_key}= {value} on {gfx_index}")
    status = registry.write(gfx_index, reg_key, registry_access.RegDataType.DWORD, value)
    if status is False:
        logging.error(f"\tFAILED to update {reg_key}= {value}")
        return False
    logging.info(f"\tSuccessfully updated {reg_key}= {value}")
    return status


##
# @brief        Exposed API to delete DPST Threshold INFs
# @param[in]    adapter object
# @return       status Boolean, True success & restart required, None success & no restart required, False otherwise
def delete_dpst_threshold_inf(adapter):
    reg_key = registry.RegKeys.DPST.DPST_BACKLIGHT_THRESHOLD
    status = registry.delete(adapter.gfx_index, key=reg_key)
    if status is False:
        logging.error(f"FAILED to delete registry key= {reg_key}")
        return False
    logging.info(f"Successfully deleted registry key= {reg_key}")
    return status


##
# @brief        Exposed API to delete the Dpst Threshold INFs
# @param[in]     adapter object, Adapter
# @return       status Boolean, True success & restart required, None success & no restart required, False otherwise
def delete_dpst_backlight_threshold(adapter):
    reg_keys = [
        registry.RegKeys.DPST.DPST_BACKLIGHT_THRESHOLD,
        registry.RegKeys.DPST.DPST_BACKLIGHT_THRESHOLD_LOWER,
        registry.RegKeys.DPST.DPST_BACKLIGHT_THRESHOLD_UPPER
    ]
    logging.info("STEP: Deleting DPST Threshold INFs")
    any_failure = False
    do_driver_restart = False
    for key in reg_keys:
        logging.info(f"\tDeleting registry= {key}")
        status = registry.delete(adapter.gfx_index, key=key)
        if status is False:
            logging.error(f"\tFAILED to delete {key}")
            any_failure = True
        do_driver_restart = True if status is True else do_driver_restart
    if any_failure:
        return False
    if do_driver_restart:
        return True
    return None


##
# @brief        Exposed API to update DPST 7 Smoothing Max speed
# @param[in]    adapter object of Adapter
# @param[in]    max_speed int value to be defined in reg key (milli hz accepted by driver)
# @return       status Boolean, True success & restart required, None success & no restart required, False otherwise
def update_dpst7_max_smoothening(adapter, max_speed: int):
    reg_key = registry.RegKeys.DPST.SMOOTHENING_MAX_SPEED
    logging.info("Step: Updating DPST Smoothing Max Speed")
    status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, max_speed)
    if status is False:
        logging.error(f"FAILED to update {reg_key}= {max_speed}")
        return False
    logging.info(f"\tSuccessfully updated {reg_key}= {max_speed}")
    return status


##
# @brief        Exposed API to verify DPST/OPST feature
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @param[in]    dpst_etl_file location of generated ETL file
# @param[in]    skip_report_generate requirement to generate report again
# @param[in]    feature optional, declare feature type for the verification
# @param[in]    verify_polled_offsets bool, optional flag to verify HW SFSU DPST offsets
# @param[in]    expect_sfsu_enable bool, optional flag to expect SFSU should be enabled or disabled
# @param[in]    is_psr_enabled_in_igcl bool, optional flag to say PSR is enabled or disabled in IGCL
# @return       status, boolean, True if DPST/OPST feature behave as expected ,
#                                None if required argument is not present,
#                                False otherwise
def verify(adapter, panel, dpst_etl_file, skip_report_generate=False, feature: XpstFeature = XpstFeature.DPST,
           verify_polled_offsets=False, expect_sfsu_enable=True, is_psr_enabled_in_igcl=True):
    assert adapter
    assert panel
    status = True
    if skip_report_generate is False:
        if os.path.exists(dpst_etl_file) is False:
            logging.error("{0} not Found".format(dpst_etl_file))
            return None
        # Generate reports from ETL file using EtlParser
        logging.info("Step: Generating EtlParser Report for {0}".format(dpst_etl_file))
        if etl_parser.generate_report(dpst_etl_file) is False:
            logging.error("\tFAILED to generate ETL Parser report (Test Issue)")
            return None
        logging.info("\tPASS: Successfully generated ETL Parser report")

    is_psr2_expected = False
    if panel.psr_caps.is_psr2_supported and panel.psr_caps.is_enabled_in_vbt:
        # proceed only when PSR2 is not disabled via registry key
        is_psr2 = registry.read(adapter.gfx_index, registry.RegKeys.PSR.PSR2_DISABLE) == registry.RegValues.DISABLE
        is_psr = registry.FeatureTestControl(adapter.gfx_index).psr_disable == registry.RegValues.DISABLE
        if is_psr2 and is_psr and is_psr_enabled_in_igcl:
            psr_version = psr.verify_psr_restrictions(adapter, panel, psr.UserRequestedFeature.PSR_2)
            is_psr2_expected = (psr.UserRequestedFeature.PSR_2 == psr_version)
    if adapter.name not in common.PRE_GEN_15_PLATFORMS and verify_polled_offsets:
        if XpstFeature.OPST == feature:
            status &= verify_dpst_prog_coefficient(adapter, panel)

        if is_psr2_expected and expect_sfsu_enable:
            status &= verify_dpst_sf_segments(adapter, panel)
        status &= verify_dpst_sf_ctl(adapter, panel, expect_enable=is_psr2_expected & expect_sfsu_enable)

    if adapter.name not in common.PRE_GEN_16_PLATFORMS:
        # legacy histogram read/write shouldn't happen. New register RECENT_DPST_HIST_BIN should be used by driver
        status &= verify_no_hist_bin_read(adapter, panel)
        if verify_polled_offsets:
            status &= verify_dpst_guard2(adapter, panel)

    # no need to verify anything further if DPST CTL is disabled
    if verify_dpst_ctl(adapter, panel, feature) is False:
        return False

    # Driver has to make sure to enable Dithering bit
    status &= verify_dithering(adapter, panel)

    if panel.psr_caps.is_psr2_supported is False:
        status &= verify_dpst_guard(adapter, panel)

    status &= verify_dpst_guardband_value(adapter, panel, is_psr2_expected)
    return status


##
# @brief        Exposed API to have Different workloads for DPST/OPST
# @param[in]    method enum WorkloadArgs
# @param[in]    frame_change enum, optional WorkloadArgs
# @param[in]    window_mode enum, optional WindowMode
# @param[in]    image_number int, optional
# @param[in]    polling_offsets bool, optional
# @return       new_etl_file location of generated ETL file, False otherwise
def run_workload(method: WorkloadMethod, frame_change: FrameChangeType = FrameChangeType.CONTINUOUS,
                 window_mode: WindowMode = WindowMode.FULLSCREEN, image_number: int = 0, polling_offsets=None):
    monitors = psr_util.app_controls.get_enumerated_display_monitors()
    monitor_ids = [_[0] for _ in monitors]

    # minimizing to desktop
    if window_helper.minimize_all_windows():
        logging.info("\tSuccessfully minimized to Desktop")
    else:
        logging.error("\tFAILED to Minimize Desktop")

    time.sleep(4)  # keeping delay for the ETL to start to make system idle

    status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeWorkload")
    if status is False:
        return False

    if polling_offsets is not None:
        logging.info(f"\tPolling started. Delay= 0.5 s, Offsets= {polling_offsets}")
        polling.start(polling_offsets, 0.5)

    if frame_change != FrameChangeType.SINGLE:
        if etl_tracer.start_etl_tracer() is False:
            logging.error("FAILED to start ETL Tracer(Test Issue)")
            return False
        if method == WorkloadMethod.IDLE:
            logging.info("Waiting for 30 seconds in idle screen")
            time.sleep(30)
        elif method == WorkloadMethod.PSR_UTIL:
            logging.info("Step: Launching PSR UTIL App for continuous frame update")
            psr_util.run(monitor_ids, wait_time=2500)
        elif method == WorkloadMethod.GOLDEN_IMAGE:
            logging.info(f"Launching Golden Images in {WindowMode(window_mode).name}")
            subprocess.Popen(os.path.join(__APPLICATIONS_FOLDER, "TestImages.exe"))
            time.sleep(4)  # breather for app launch

            if window_mode == WindowMode.WINDOWED:
                kb.press('DOWN')
                time.sleep(2)  # breather
            for _ in range(0, 17):
                logging.info(f"Changing to image {_}")
                kb.press('RIGHT')
                time.sleep(5)
                logging.info("Changing to complete white image")
                kb.press('0')
                time.sleep(5)
            logging.info("Closing the Golden Images")
            kb.press('ESC')

        # Stop ETL tracer
        if etl_tracer.stop_etl_tracer() is False:
            logging.error("\tFAILED to stop ETL Tracer(Test Issue)")
            return False

    else:
        logging.info("Launching TestImages.exe")
        subprocess.Popen(os.path.join(__APPLICATIONS_FOLDER, "TestImages.exe"))
        time.sleep(4)  # breather for app launch

        # move cursor to right bottom corner
        win32api.SetCursorPos((win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)))

        if window_mode == WindowMode.WINDOWED:
            kb.press('5')  # Keep Gradient Image
            time.sleep(1)
            subprocess.Popen(os.path.join(__APPLICATIONS_FOLDER, "TestImages.exe"))  # open another instance
            time.sleep(4)  # breather for app launch
            kb.press('DOWN')
            time.sleep(1)

        logging.info(f"Moving to {WindowMode(window_mode).name} mode")
        logging.info(f"Showing image #{image_number}")
        for _ in range(0, image_number - 1):
            logging.info("\tChanging to another image by pressing right arrow key")
            kb.press('RIGHT')
            time.sleep(0.5)  # breather

        if change_power_source(PowerSource.AC_MODE) is False:
            assert False, "Failed to switch power source"

        logging.info("Waiting for 10 seconds to make sure DPST is disabled and complete phase-out is done")
        time.sleep(10)

        if etl_tracer.start_etl_tracer() is False:
            logging.error("FAILED to start ETL Tracer(Test Issue)")
            return False

        time.sleep(2)  # breather

        if change_power_source(PowerSource.DC_MODE) is False:
            assert False, "Failed to switch power source"

        logging.info("Waiting for 10 seconds to have DPST enabled with IET adjustments")
        time.sleep(10)

        logging.info("Changing the image to have frame update")
        kb.press('RIGHT')

        logging.info("Waiting for 10 seconds to have IET adjustments")
        time.sleep(10)

        # Stop ETL tracer
        if etl_tracer.stop_etl_tracer() is False:
            logging.error("\tFAILED to stop ETL Tracer(Test Issue)")
            return False

        time.sleep(1)  # breather

        logging.info("Closing the Golden Images")
        kb.press('ESC')
        if window_mode == WindowMode.WINDOWED:
            kb.press('ESC')

    if polling_offsets is not None:
        _, _ = polling.stop()
        logging.info("\tPolling stopped")

    status, new_etl_file = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuringWorkload")
    if status is False:
        return False

    # restore from desktop
    if window_helper.restore_all_windows():
        logging.info("\tSuccessfully restored to desktop")
    else:
        logging.error("\tFAILED to restore Desktop")

    return new_etl_file


##
# @brief        Exposed API to verify EPSM status
# @param[in]    dpst_etl_file etl file for DPST events
# @return       True if Enabled, False otherwise
#               None, ETL file not found
def verify_epsm(dpst_etl_file):
    if os.path.exists(dpst_etl_file) is False:
        logging.error("{0} not Found".format(dpst_etl_file))
        return None

    json_file = validator_runner.run_diana("dpst_basic", dpst_etl_file, ['DPST'])
    if json_file is None:
        logging.error("FAILED to execute run_diana()")
        return False

    try:
        with open(json_file) as f:
            data = f.read()
            invalid_strings = re.findall('new Date\(\d+\)', data)
            for invalid_string in invalid_strings:
                data = data.replace(invalid_string, '"0"')
            d = json.loads(data)

            all_seq = []
            # parsing below string from json file  to get EPSM status
            # DpstRunAlgorithm(time): PipeId = PIPE_A, AggrLevel = 5, IsEPSMEnabled = 1, BacklightAdjust = 0,
            # BlackThresholdBinIndex = 0, ImageSize = 0, NumOfHighlightPixels = 0, LUT = values
            epsm_str = 'IsEPSMEnabled= '
            for msg in d['ReportQueue']:
                if 'DpstRunAlgorithm(' in msg['Header']:
                    histogram_dict = msg['Header']
                    ind = histogram_dict.index(epsm_str)
                    arr = (histogram_dict[ind + len(epsm_str):]).split(',')
                    int_arr = [str(_) for _ in arr]
                    all_seq.append(int_arr)
    except Exception as ex:
        logging.error(ex)
        return False

    logging.info("\tChecking EPSM status from traced ETL")
    status = None
    for seq in all_seq:
        status = False if seq[0] == '0' else True
    if status:
        logging.info("\tEPSM is Enabled!")
        return True
    logging.info("\tEPSM is Disabled!")
    return False


##
# @brief        Exposed API to generate brightness levels from dpst threshold
# @param[in]    thresholds list of [dpst_threshold, lower_threshold, upper_threshold]
# @param[in]    blc_args list of [is_high_precision, is_nits_supported, max_nits]
# @return       [[level_without_dpst], [level_with_dpst]] list of different brightness levels
def generate_brightness_levels(thresholds, blc_args):
    dpst_threshold = thresholds[0]
    lower_threshold = thresholds[1]
    upper_threshold = thresholds[2]
    is_high_precision = blc_args[0]
    is_nits_supported = blc_args[1]
    max_nits = blc_args[2]
    levels_without_dpst = []
    levels_with_dpst = []

    # only old INF is present
    if (dpst_threshold is not None) and ((lower_threshold or upper_threshold) is None):
        outside_threshold = randrange(blc.Percentage.MIN.value, dpst_threshold)
        inside_threshold = randint(dpst_threshold, blc.Percentage.MAX.value)
        # DPST should NOT work
        levels_without_dpst = [dpst_threshold - 1, outside_threshold]
        # DPST should work
        levels_with_dpst = [dpst_threshold + 1, inside_threshold]
    # new INF is present
    else:
        # only when lower threshold is present
        if (lower_threshold is not None) and (upper_threshold is None):
            lower = lower_threshold // 1000
            # milli-percent brightness3 (HighPrecision)
            if is_high_precision:
                # DPST should NOT work
                levels_without_dpst = [
                    i for i in random.sample(range(blc.MilliPercentage.MIN.value, lower_threshold), 2)
                ]
                levels_without_dpst.append(lower_threshold - 1)
                # DPST should work
                levels_with_dpst = [
                    i for i in random.sample(range(lower_threshold, blc.MilliPercentage.MAX.value + 1), 2)
                ]
                levels_with_dpst.append(lower_threshold + 1)
            # percent brightness3 (NITS to PWM)
            elif is_nits_supported:
                # DPST should NOT work
                value = [randrange(blc.Percentage.MIN.value, lower), lower - 1]
                levels_without_dpst = blc.convert_percent_to_milli_nits(value, max_nits)
                # DPST should work
                value = [i for i in random.sample(range(lower, blc.Percentage.MAX.value + 1), 2)]
                value.append(lower + 1)
                levels_with_dpst = blc.convert_percent_to_milli_nits(value, max_nits)
            # percent brightness2 (PWM)
            else:
                below_lower_threshold = randrange(blc.Percentage.MIN.value, lower)
                above_lower_threshold = randint(lower, blc.Percentage.MAX.value)
                # DPST should NOT work
                levels_without_dpst = [lower - 1, below_lower_threshold]
                # DPST should work
                levels_with_dpst = [lower + 1, above_lower_threshold]
        # only when upper threshold is present
        elif (lower_threshold is None) and (upper_threshold is not None):
            upper = upper_threshold // 1000
            # milli-percentage brightness3 (HighPrecision)
            if is_high_precision:
                # DPST should NOT work
                levels_without_dpst = [
                    i for i in random.sample(range(upper_threshold, blc.MilliPercentage.MAX.value + 1), 2)
                ]
                levels_without_dpst.append(upper_threshold + 1)
                # DPST should work
                levels_with_dpst = [
                    i for i in random.sample(range(blc.MilliPercentage.MIN.value, upper_threshold + 1), 2)
                ]
                levels_with_dpst.append(upper_threshold - 1)
            # percentage brightness3 (NITS to PWM)
            elif is_nits_supported:
                # DPST should NOT work
                value = [randint(upper + 1, blc.Percentage.MAX.value), upper + 1]
                levels_without_dpst = blc.convert_percent_to_milli_nits(value, max_nits)
                # DPST should work
                value = [i for i in random.sample(range(blc.Percentage.MIN.value, upper + 1), 2)]
                value.append(upper - 1)
                levels_with_dpst = blc.convert_percent_to_milli_nits(value, max_nits)
            # percentage brightness2 (PWM)
            else:
                below_upper_threshold = randrange(blc.Percentage.MIN.value, upper)
                above_upper_threshold = randint(upper + 1, blc.Percentage.MAX.value)
                # DPST should NOT work
                levels_without_dpst = [upper + 1, above_upper_threshold]
                # DPST should work
                levels_with_dpst = [upper - 1, below_upper_threshold]
        # when both lower and upper thresholds are present
        elif (lower_threshold is not None) and (upper_threshold is not None):
            upper = upper_threshold // 1000
            lower = lower_threshold // 1000
            # milli-percentage brightness3 (HighPrecision)
            if is_high_precision:
                # DPST should NOT work
                levels_without_dpst = [
                    upper_threshold + 1, lower_threshold - 1,
                    randint(upper_threshold + 1, blc.MilliPercentage.MAX.value),
                    randrange(blc.MilliPercentage.MIN.value, lower_threshold)
                ]
                # DPST should work
                levels_with_dpst = [i for i in random.sample(range(lower_threshold, upper_threshold + 1), 2)]
            # percentage brightness3 (NITS to PWM)
            elif is_nits_supported:
                # DPST should NOT work
                value = [
                    randint(upper + 1, blc.Percentage.MAX.value),
                    randrange(blc.Percentage.MIN.value, lower),
                    upper + 1,
                    lower - 1
                ]
                levels_without_dpst = blc.convert_percent_to_milli_nits(value, max_nits)
                # DPST should work
                value = [i for i in random.sample(range(lower, upper + 1), 2)]
                value.append(upper - 1)
                value.append(lower + 1)
                levels_with_dpst = blc.convert_percent_to_milli_nits(value, max_nits)
            # percentage brightness2 (PWM)
            else:
                # DPST should NOT work
                levels_without_dpst = [
                    upper + 1, randint(upper + 1, blc.Percentage.MAX.value),
                    lower - 1, randrange(blc.Percentage.MIN.value, lower)
                ]

                # DPST should work
                levels_with_dpst = [
                    upper - 1, randint(lower, upper),
                    lower + 1, randint(lower, upper),
                    lower, upper
                ]
    logging.info(f"Returning brightness level: Without DPST= {levels_without_dpst}, With DPST= {levels_with_dpst}")
    return [levels_without_dpst, levels_with_dpst]


##
# @brief        Exposed API to verify DPST GUARD register
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @return       status, True if Pass else False
def verify_dpst_guard(adapter, panel):
    dpst_guard = MMIORegister.get_instance("DPST_GUARD_REGISTER", "DPST_GUARD_" + panel.pipe, adapter.name)
    histogram_event_counter = 0
    fail_count = 0
    guard_mmio_output = etl_parser.get_mmio_data(dpst_guard.offset, is_write=True)
    if guard_mmio_output is None:
        logging.warning("\tNo MMIO entry found for register DPST_GUARD_" + panel.pipe)
        return False

    # Iterating through DPST GUARD data
    for mmio_data in guard_mmio_output:
        dpst_guard.asUint = mmio_data.Data
        logging.debug("\t\tDPST_GUARD_{0}: Histogram (InterruptEnable= {1}, EventStatus= {2}) on TimeStamp= {3}".format(
            panel.pipe, dpst_guard.histogram_interrupt_enable, dpst_guard.histogram_event_status, mmio_data.TimeStamp))

        if fail_count == 3:
            logging.error("Counter Maxed out: Histogram Interrupt is enabled but not Event Counter")
            gdhm.report_driver_bug_pc("[XPST] Histogram Event status is not happening(counter maxed out)")
            break

        if dpst_guard.histogram_interrupt_enable == 1:
            if dpst_guard.histogram_event_status == 1:
                histogram_event_counter += 1
                fail_count = 0
            elif dpst_guard.histogram_event_status == 0:
                logging.info("Trial - {0}: Ignoring if event status is not set".format(fail_count))
                fail_count += 1

    logging.info(f"\tDPST Histogram Event Counter= {histogram_event_counter}")

    return fail_count == 0


##
# @brief        Exposed API to verify DPST GUARD2 register for PTL+ platforms. Gets programmed at modeset
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @return       status, True if Pass else False
def verify_dpst_guard2(adapter, panel):
    if adapter.name in common.PRE_GEN_16_PLATFORMS:
        return True

    dpst_guard2 = MMIORegister.get_instance("DPST_GUARD2_REGISTER", "DPST_GUARD2_" + panel.pipe, adapter.name)
    guard_mmio_output = etl_parser.get_mmio_data(dpst_guard2.offset)
    if guard_mmio_output is None:
        logging.warning("\tNo MMIO entry found for register DPST_GUARD2_" + panel.pipe)
        return False

    # Iterating through DPST GUARD2 data
    status = True
    for mmio_data in guard_mmio_output:
        dpst_guard2.asUint = mmio_data.Data
        logging.debug("\t\tDPST_GUARD2_{0}: HighThresholdGuardband= {1}, HighThresholdEnable= {2} on "
                      "TimeStamp= {3}".format(panel.pipe, dpst_guard2.high_threshold_guardband,
                                              dpst_guard2.high_threshold_enable, mmio_data.TimeStamp))

        if dpst_guard2.high_threshold_enable != Status.ENABLED:
            logging.error("High Threshold Guardband is not enable")
            status = False

        # Threshold guardband is currently programmed as 10% of resolution
        expected_guardband = int(panel.current_mode.HzRes * panel.current_mode.VtRes * 0.1)
        if dpst_guard2.high_threshold_guardband != expected_guardband:
            logging.error("HighThresholdGuardband is not programmed as 10% of ImageSize. "
                          f"Expected= {expected_guardband}, Actual= {dpst_guard2.high_threshold_guardband}")
            status = False

    return status


##
# @brief        Exposed API to verify legacy histogram bin is not read
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @return       status, True if Pass else False
def verify_no_hist_bin_read(adapter, panel):
    if adapter.name in common.PRE_GEN_16_PLATFORMS:
        return True

    legacy_dpst_hist_bin = MMIORegister.get_instance(
        "DPST_HIST_BIN_REGISTER", "DPST_HIST_BIN_" + panel.pipe, adapter.name)
    guard_mmio_output = etl_parser.get_mmio_data(legacy_dpst_hist_bin.offset)
    if guard_mmio_output is None:
        logging.info(f"\tNo MMIO entry found for legacy register DPST_HIST_BIN_{panel.pipe} (Expected)")
        return True
    logging.error(f"\tMMIO entry found for legacy register DPST_HIST_BIN_{panel.pipe} (Unexpected)")
    return False


##
# @brief        Exposed API to verify DPST CTL register
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @param[in]    feature enum, XpstFeature
# @return       status, True if pass else False
def verify_dpst_ctl(adapter, panel, feature: XpstFeature):
    dpst_ctl = MMIORegister.get_instance("DPST_CTL_REGISTER", "DPST_CTL_" + panel.pipe, adapter.name)
    histogram_enable_counter = 0
    status = True

    # For DPST, value is 1: HSV mode
    # For OPST, value is 0: PreGen15= YUV LUMA, Gen15+= Programmable Coefficient Mode
    expected_histogram_mode = 1 if XpstFeature.DPST == feature else 0
    ctl_mmio_output = etl_parser.get_mmio_data(dpst_ctl.offset)
    if ctl_mmio_output is None:
        logging.warning("\tNo MMIO Entries found for register DPST_CTL_" + panel.pipe)
        ctl_val = MMIORegister.read(
            'DPST_CTL_REGISTER', 'DPST_CTL_' + panel.pipe, adapter.name, gfx_index=adapter.gfx_index)
        logging.info(f"DPST_CTL_{panel.pipe} {hex(ctl_val.offset)}= {hex(ctl_val.asUint)}")
        if ctl_val.ie_histogram_enable == 1 and ctl_val.histogram_mode_select == expected_histogram_mode:
            return True
        logging.error(f"IEHistogramEnable= {ctl_val.ie_histogram_enable}, ModeSelect= {ctl_val.histogram_mode_select}")
        return False

    # Iterating through DPST CTL data
    for mmio_data in ctl_mmio_output:
        dpst_ctl.asUint = mmio_data.Data
        logging.info(f"\t\tDPST_CTL_{panel.pipe} Offset= {hex(mmio_data.Offset)}= {hex(mmio_data.Data)} at "
                     f"{mmio_data.TimeStamp}")
        logging.debug(f"\t\t\tIE Histogram= {dpst_ctl.ie_histogram_enable}, "
                      f"Histogram Mode Select= {dpst_ctl.histogram_mode_select}")

        if dpst_ctl.ie_histogram_enable == 1:
            histogram_enable_counter += 1

        if dpst_ctl.histogram_mode_select != expected_histogram_mode:
            logging.error(f"\t\tHistogram Mode Select is value {dpst_ctl.histogram_mode_select} for {feature.name}")
            status &= False

    logging.info(f"\tDPST Histogram Enable Counter= {histogram_enable_counter}")

    if status is False:
        gdhm.report_driver_bug_pc(f"[XPST] HistogramModeSelect is not {expected_histogram_mode} for {feature.name}")

    return histogram_enable_counter != 0 and status


##
# @brief        Exposed API to verify DPST guardband delay and threshold guardband
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @param[in]    is_psr2_expected bool, flag to handle the expectation according to PSR2
# @return       status
def verify_dpst_guardband_value(adapter, panel, is_psr2_expected):
    html.step_start("Verifying DPST Guard Band values")
    dpst_guard = MMIORegister.get_instance("DPST_GUARD_REGISTER", "DPST_GUARD_" + panel.pipe, adapter.name)

    # Read PSR2 mmio register to verify Psr2 enable in driver

    logging.info(f"Panel on {panel.port} supports PSR2= {is_psr2_expected}")

    status = True
    guard_mmio_output = etl_parser.get_mmio_data(dpst_guard.offset)
    if guard_mmio_output is None:
        logging.error("\tNo MMIO entry found for register DPST_GUARD_" + panel.pipe)
        html.step_end()
        return False

    gdhm_message = set()
    for mmio_data in guard_mmio_output:
        dpst_guard.asUint = mmio_data.Data
        logging.info(
            f"\t\tDPST_GUARD_{panel.pipe}: Interrupt_Delay= {dpst_guard.guardband_interrupt_delay},"
            f"Threshold_Guardband ={dpst_guard.threshold_guardband}) on TimeStamp= {mmio_data.TimeStamp}")

        #  Pre MTL, the Low threshold guardband is programmed as 12%, LNL+, it will be 5%.
        if adapter.name in common.PRE_GEN_15_PLATFORMS:
            # Threshold guardband is currently programmed as 3% of resolution. H/w will make 3% * 4 to make it 12%.
            threshold_guardband = int(panel.current_mode.HzRes * panel.current_mode.VtRes * 0.03)
        else:
            # Threshold guardband is currently programmed as 5%. So, program 1.25% and H/w will do 1.25% * 4
            threshold_guardband = int(panel.current_mode.HzRes * panel.current_mode.VtRes * 0.0125)

        if dpst_guard.threshold_guardband == threshold_guardband:
            logging.debug(f"Valid Threshold Guardband is programmed. "
                          f"Actual= {dpst_guard.threshold_guardband}, Expected= {threshold_guardband} ")
        else:
            logging.error(
                f"FAIL: Invalid Threshold Guardband is programmed. "
                f"Actual= {dpst_guard.threshold_guardband}, Expected= {threshold_guardband} ")
            gdhm_message.add("[XPST] Invalid Threshold Guardband is programmed in DPST_GUARD")
            status &= False

        # skipping delay check for Pre Gen13 as PSR2 is having HW restriction. So, creating multiple conditions are
        # not needed. Test can focus only for Gen13+
        if adapter.name not in common.PRE_GEN_13_PLATFORMS + ['DG2']:
            # Added check for DPST Guardband Interrupt Delay and Threshold Guardband
            if dpst_guard.guardband_interrupt_delay not in [0x1, 0x4]:
                logging.error("FAIL: Guardband Interrupt Delay programmed as "
                              f"{dpst_guard.guardband_interrupt_delay} (Unexpected)")
                gdhm_message.add("[XPST] Invalid Guardband Interrupt Delay programmed. Expected= {1 or 4}")
                status &= False
                continue

            if is_psr2_expected:
                if dpst_guard.guardband_interrupt_delay != 0x1:
                    logging.error("FAIL: Guardband Interrupt Delay programmed as "
                                  f"{dpst_guard.guardband_interrupt_delay} (Unexpected)")
                    gdhm_message.add("[XPST] Invalid Guardband Interrupt Delay programmed. Expected= {1}")
                    status &= False
            else:
                if dpst_guard.guardband_interrupt_delay != 0x4:
                    logging.error("FAIL: Guardband Interrupt Delay programmed as "
                                  f"{dpst_guard.guardband_interrupt_delay} (Unexpected)")
                    gdhm_message.add("[XPST] Invalid Guardband Interrupt Delay programmed. Expected= {4}")
                    status &= False

        for message in gdhm_message:
            gdhm.report_driver_bug_pc(message)

    html.step_end()
    return status


##
# @brief        Exposed API to verify Dithering enable/disable
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @return       status
def verify_dithering(adapter, panel):
    if adapter.name in common.PRE_GEN_13_PLATFORMS + ['DG2']:
        return True
    html.step_start(f"Verifying Dithering for {panel.port}")
    status = True
    pipe_misc = MMIORegister.read("PIPE_MISC_REGISTER", "PIPE_MISC_" + panel.pipe, adapter.name)
    logging.info(f"\t\tPIPE_MISC_{panel.pipe}: Dithering= {pipe_misc.dithering_enable}")
    if pipe_misc.dithering_enable != 0x1:
        logging.error(f"FAIL: Dithering is not enabled for XPST (Unexpected)")
        gdhm.report_driver_bug_pc("[XPST] Dithering is disabled in PIPE_MISC REG (Unexpected)")
        status = False
    html.step_end()
    return status


##
# @brief        Exposed API to verify DPST PROG Coefficient register
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @return       status, True if pass else False
def verify_dpst_prog_coefficient(adapter, panel):
    html.step_start(f"Verifying Programmable Coefficient for RGB for {panel.port}")
    prog_offset = MMIORegister.get_instance("DPST_PROG_COEF_REGISTER", "DPST_PROG_COEF_" + panel.pipe, adapter.name)
    status = True

    prog_mmio_output = etl_parser.get_mmio_data(prog_offset.offset)
    if prog_mmio_output is None:
        logging.warning("\tNo MMIO Entries found for register DPST_PROG_COEF_" + panel.pipe)
        html.step_end()
        return False

    # BT601 standard: Red channel coef: 0.299 , Green channel coef: 0.587 , Blue channel coef: 0.114
    # All coefficients have a precision of 0.9. Coefficients are multiplied by 2^9 to get programming value.
    # Valid Values (R: 153, G: 301, B: 58)
    # Iterating through DPST Programmable Coefficient
    for mmio_data in prog_mmio_output:
        prog_offset.asUint = mmio_data.Data
        logging.info(f"\t\tDPST_PROG_COEF_{panel.pipe} Offset= {hex(mmio_data.Offset)}= {hex(mmio_data.Data)} at "
                     f"{mmio_data.TimeStamp}")
        logging.debug(f"\t\t\tRedCoefficient= {prog_offset.red_coefficient}, "
                      f"GreenCoefficient= {prog_offset.green_coefficient}, "
                      f"BlueCoefficient= {prog_offset.blue_coefficient}")

        if (prog_offset.red_coefficient != 0x99) or (prog_offset.green_coefficient != 0x12D) or (
                prog_offset.blue_coefficient != 0x3A):
            logging.error(f"\t\t\tRedCoefficient= {prog_offset.red_coefficient}, "
                          f"GreenCoefficient= {prog_offset.green_coefficient}, "
                          f"BlueCoefficient= {prog_offset.blue_coefficient}")
            status &= False

    if status:
        logging.info("Valid RGB values are programmed in DPST_PROG_COEF")
    else:
        logging.error("Invalid RGB values are programmed in DPST_PROG_COEF")
        gdhm.report_driver_bug_pc(f"[XPST] Invalid RGB values are programmed in DPST_PROG_COEF")

    html.step_end()
    return status


##
# @brief        Exposed API to verify DPST SF Segment values
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @return       status, True if pass else False
def verify_dpst_sf_segments(adapter: Adapter, panel: Panel):
    html.step_start(f"Verifying DPST SF Segments for {panel.port}")
    status = True

    seg_size = MIN_SFSU_DPST_SEGMENT_SIZE
    pipe_source_height = panel.current_mode.VtRes
    while seg_size <= pipe_source_height:
        if (pipe_source_height % seg_size == 0) and ((pipe_source_height // seg_size) <= MAX_SFSU_DPST_SEGMENTS):
            break
        seg_size += 1

    if panel.vdsc_caps.is_vdsc_supported:
        if dsc_verifier.verify_dsc_programming(adapter.gfx_index, panel.port) is False:
            logging.error("DSC verification is FAILED")
            html.step_end()
            return False
        edp_dss_ctl2 = MMIORegister.read('PIPE_DSS_CTL2_REGISTER', 'PIPE_DSS_CTL2_P' + panel.pipe,
                                         adapter.name, gfx_index=adapter.gfx_index)
        # make the segment size an integer multiple of DSC slice height that is greater than minimum segment size
        if edp_dss_ctl2.left_branch_vdsc_enable:
            dsc_pps3 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_3", 'PPS3_0_' + panel.pipe, adapter.name,
                                         gfx_index=adapter.gfx_index)
            logging.info(f"\tVDSC is enabled for {panel.port} and DSC slice height= {dsc_pps3.slice_height}")
            seg_size = math.ceil(seg_size / dsc_pps3.slice_height) * dsc_pps3.slice_height

    dpst_sf_seg = MMIORegister.get_instance("DPST_SF_SEG_REGISTER", "DPST_SF_SEG_" + panel.pipe, adapter.name)
    dpst_sf_seg_output = etl_parser.get_mmio_data(dpst_sf_seg.offset)
    if dpst_sf_seg_output is None:
        logging.warning("\tNo MMIO Entries found for register DPST_SF_SEG_" + panel.pipe)
        html.step_end()
        return False

    for mmio_data in dpst_sf_seg_output:
        dpst_sf_seg.asUint = mmio_data.Data
        logging.info(f"\t\tDPST_SF_SEG_{panel.pipe} Offset= {hex(mmio_data.Offset)}= {hex(mmio_data.Data)} at "
                     f"{mmio_data.TimeStamp}")
        logging.debug(f"\t\t\tSegment Size= {dpst_sf_seg.segment_size}, "
                      f"Start= {dpst_sf_seg.segment_start}, End= {dpst_sf_seg.segment_end}")

        # verification for SegmentStart and SegmentEnd will be taken care in DpstTracker via StateMachine
        # as it would need to be done for each selective fetch and dynamically changed
        if dpst_sf_seg.segment_size != seg_size:
            logging.error(f"\t\tSegment Size Mismatch. Expected= {seg_size}, Actual= {dpst_sf_seg.segment_size}")
            status = False

    if status:
        logging.info("Valid values are programmed in DPST_SF_SEG")
    else:
        logging.error("Invalid values are programmed in DPST_SF_SEG")
        gdhm.report_driver_bug_pc(f"[XPST] Invalid values are programmed in DPST_SF_SEG")

    html.step_end()
    return status


##
# @brief        Exposed API to verify DPST SF CTL register
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @param[in]    expect_enable bool, True if expected as Enable, else False
# @return       status, True if pass else False
def verify_dpst_sf_ctl(adapter, panel, expect_enable=True):
    html.step_start(f"Verifying DPST_SF_CTL for {panel.port}")
    dpst_sf_ctl = MMIORegister.get_instance("DPST_SF_CTL_REGISTER", "DPST_SF_CTL_" + panel.pipe, adapter.name)
    dpst_sf_ctl_enable_counter = 0

    ctl_mmio_output = etl_parser.get_mmio_data(dpst_sf_ctl.offset)
    if ctl_mmio_output is None:
        if expect_enable:
            logging.error(f"\tNo MMIO Entries found for register DPST_SF_CTL_{panel.pipe} (Unexpected)")
            gdhm.report_driver_bug_pc("[XPST] No MMIO entries found for DPST_SF_CTL (Expected= Enable)")
            html.step_end()
            return False

        logging.warning(f"\tNo MMIO Entries found for register DPST_SF_CTL_{panel.pipe} (Expected)")
        html.step_end()
        return True

    # Iterating through DPST CTL data
    for mmio_data in ctl_mmio_output:
        dpst_sf_ctl.asUint = mmio_data.Data
        logging.info(f"\t\tDPST_SF_CTL_{panel.pipe} Offset= {hex(mmio_data.Offset)}= {hex(mmio_data.Data)} at "
                     f"{mmio_data.TimeStamp}")
        logging.debug(f"\t\t\tSelective Fetch Enable= {dpst_sf_ctl.selective_fetch_enable}")

        if dpst_sf_ctl.selective_fetch_enable == 1:
            dpst_sf_ctl_enable_counter += 1

    logging.info(f"\tDPST Histogram Enable Counter= {dpst_sf_ctl_enable_counter}")

    is_dpst_sf_ctl_enabled = (dpst_sf_ctl_enable_counter != 0)
    if (is_dpst_sf_ctl_enabled and expect_enable is False) or (expect_enable and is_dpst_sf_ctl_enabled is False):
        message = f"DPST_SF_CTL 31st bit is Expected= {expect_enable}, Actual= {is_dpst_sf_ctl_enabled}"
        logging.error(f"{message}")
        gdhm.report_driver_bug_pc(f"[XPST] {message}")
        return False

    return True


##
# @brief         Exposed API to get power caps
# @param[in]     target_id - Target_id of the display
# @param[in]     power_source - AC/DC - default to DC
# @param[in]     power_scheme - POWER_SAVER/BALANCED/HIGH_PERFORMANCE - default to BALANCED
# @return        xpst_status if success, otherwise None
def get_status(target_id, power_source: display_power.PowerSource, power_scheme: display_power.PowerScheme):
    html.step_start("Fetching XPST Status using Control API")

    igcl_power_source = __igcl_map_power_source(power_source)
    igcl_power_plan = __igcl_map_power_plan(power_scheme)
    if igcl_power_source is None or igcl_power_plan is None:
        html.step_end()
        return None

    get_power_params = control_api_args.ctl_power_optimization_caps_t()
    get_power_params.Size = ctypes.sizeof(get_power_params)
    if control_api_wrapper.get_power_caps(get_power_params, target_id) is False:
        logging.error("FAILED to get power caps for feature support")
        html.step_end()
        return None

    dpst_flag = control_api_args.ctl_power_optimization_dpst_flag_t.DPST_FLAG_BKLT.value
    opst_flag = control_api_args.ctl_power_optimization_dpst_flag_t.DPST_FLAG_OPST.value
    epsm_flag = control_api_args.ctl_power_optimization_dpst_flag_t.DPST_FLAG_EPSM.value

    get_xpst = __igcl_init_dpst_structure(igcl_power_source, igcl_power_plan)
    if control_api_wrapper.get_dpst(get_xpst, target_id) is False:
        logging.error("FAILED to get DPST via Control API")
        html.step_end()
        return None

    xpst = XpstStatus()
    xpst.is_dpst_supported = (dpst_flag == (get_xpst.FeatureSpecificData.DPSTInfo.SupportedFeatures.value & dpst_flag))
    xpst.is_dpst_enabled = (dpst_flag == (get_xpst.FeatureSpecificData.DPSTInfo.EnabledFeatures.value & dpst_flag))
    xpst.is_epsm_supported = (epsm_flag == (get_xpst.FeatureSpecificData.DPSTInfo.SupportedFeatures.value & epsm_flag))
    xpst.is_epsm_enabled = (epsm_flag == (get_xpst.FeatureSpecificData.DPSTInfo.EnabledFeatures.value & epsm_flag))
    xpst.is_opst_supported = (opst_flag == (get_xpst.FeatureSpecificData.DPSTInfo.SupportedFeatures.value & opst_flag))
    xpst.is_opst_enabled = (opst_flag == (get_xpst.FeatureSpecificData.DPSTInfo.EnabledFeatures.value & opst_flag))
    xpst.min_level = get_xpst.FeatureSpecificData.DPSTInfo.MinLevel
    xpst.max_level = get_xpst.FeatureSpecificData.DPSTInfo.MaxLevel
    xpst.current_level = get_xpst.FeatureSpecificData.DPSTInfo.Level
    logging.info(f"\t{xpst}")
    html.step_end()
    return xpst


##
# @brief         Exposed API to set dpst/opst - also if together want to enable feature with aggr lvl
# @param[in]     panel object, Panel
# @param[in]     feature enum, XpstFeature
# @param[in]     enable_status bool, to enable or disable the feature
# @param[in]     power_source enum, from display_power PowerSource
# @param[in]     power_scheme enum, from display_power PowerScheme
# @return        True if Pass, otherwise False
def set_xpst(panel: Panel, feature: XpstFeature, enable_status: bool, power_source: display_power.PowerSource,
             power_scheme: display_power.PowerScheme):
    feature_str = XpstFeature(feature).name
    html.step_start(f"Setting {feature_str} to status= {enable_status} for {power_source.name} and {power_scheme.name}")
    logging.info(f"Requested for Feature {feature_str} Feature to set Status= {enable_status}")

    igcl_power_source = __igcl_map_power_source(power_source)
    igcl_power_plan = __igcl_map_power_plan(power_scheme)
    if igcl_power_source is None or igcl_power_plan is None:
        html.step_end()
        return False

    # init dpst structure and get the complete args in dpst_args
    dpst_args = __igcl_init_dpst_structure(igcl_power_source, igcl_power_plan)
    if control_api_wrapper.get_dpst(dpst_args, panel.target_id) is False:
        logging.error("\tFAILED to Get DPST via Control Library")
        html.step_end()
        return False

    dpst_flag = control_api_args.ctl_power_optimization_dpst_flag_t.DPST_FLAG_BKLT.value
    opst_flag = control_api_args.ctl_power_optimization_dpst_flag_t.DPST_FLAG_OPST.value
    current_status = None
    if feature == XpstFeature.DPST:
        current_status = (dpst_flag == (dpst_flag & dpst_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value))
    elif feature == XpstFeature.OPST:
        current_status = (opst_flag == (opst_flag & dpst_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value))

    if enable_status == current_status:
        logging.info(f"Requested setting is already set. {feature_str} Status= {current_status}")
        html.step_end()
        return True

    dpst_args.Enable = enable_status
    if feature == XpstFeature.DPST:
        dpst_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value |= dpst_flag
    else:
        dpst_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value |= opst_flag

    logging.info(f"\t{'Enabling' if enable_status else 'Disabling'} {feature_str} feature")
    if control_api_wrapper.set_dpst(dpst_args, panel.target_id) is False:
        logging.error(f"\tFAILED to {'Enable' if enable_status else 'Disable'} {feature_str} feature via Control API")
        html.step_end()
        return False

    logging.info(f"\tSuccessfully {'Enabled' if enable_status else 'Disabled'} {feature_str} feature via Control API")

    logging.info(f"\tValidating that {feature_str} feature is {'Enabled' if enable_status else 'Disabled'}")

    ftr_status = get_status(panel.target_id, power_source, power_scheme)
    if ftr_status is None:
        logging.error(f"\tFAILED to get status of {feature_str} feature")
        html.step_end()
        return False

    is_status_correct = False
    if feature == XpstFeature.OPST:
        if ftr_status.is_opst_enabled == enable_status:
            logging.info(f"\t{feature_str} feature is {'Enabled' if enable_status else 'Disabled'}")
            is_status_correct = True
        else:
            logging.error(f"\t{feature_str} feature is NOT {'Enabled' if enable_status else 'Disabled'}")
    elif feature == XpstFeature.DPST:
        if ftr_status.is_dpst_enabled == enable_status:
            logging.info(f"\t{feature_str} feature is {'Enabled' if enable_status else 'Disabled'}")
            is_status_correct = True
        else:
            logging.error(f"\t{feature_str} feature is NOT {'Enabled' if enable_status else 'Disabled'}")

    html.step_end()
    return is_status_correct


##
# @brief        API to configure VBT as requested for DPST and OPST
# @param[in]    adapter object, Adapter from dut
# @param[in]    panel object, Panel from dut
# @param[in]    requested_params class, XpstVbtParams
# @return       True if update is success, False otherwise
def configure_vbt(adapter: Adapter, panel: Panel, requested_params: XpstVbtParams):
    html.step_start(f"Configuring VBT to set {requested_params}")

    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    logging.info(f"\tRequested Params: {requested_params}")

    if (requested_params.dpst_status is not None and gfx_vbt.version < 228) or (
            requested_params.opst_status is not None and gfx_vbt.version < 247):
        logging.error(f"VBT minimum version is not meeting requirement for [DPST: 228+, OPST: 247+]. "
                      f"Current= {gfx_vbt.version}")
        html.step_end()
        return False

    current_params = XpstVbtParams()
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")

    if gfx_vbt.version >= 257 and adapter.name not in common.PRE_GEN_15_PLATFORMS:
        # fetch current status
        if requested_params.dpst_status is not None or requested_params.opst_status is not None:
            current_params.dpst_status = current_params.opst_status = (
                bool((gfx_vbt.block_44.XPSTSupport[0] & (1 << panel_index)) >> panel_index))
            current_params.dpst_level = current_params.opst_level = (
                    gfx_vbt.block_44.AgressivenessProfile4[panel_index] & 0x0f)

        # If caller doesn't care about XPST level, then assign the current level
        if requested_params.dpst_level is None and requested_params.opst_level is None:
            requested_params.opst_level = requested_params.dpst_level = current_params.opst_level

        # compare expected and current value to return early
        if requested_params == current_params:
            logging.info(f"\tAll params are already set as requested in VBT for {panel.port}")
            html.step_end()
            return True

        # OPST level
        if requested_params.opst_level:
            gfx_vbt.block_44.AgressivenessProfile4[panel_index] |= requested_params.opst_level
            # For VBT version 257, DPST and OPST both access same VBT field for level
            current_params.dpst_level = requested_params.dpst_level

        if requested_params.opst_status:
            gfx_vbt.block_44.XPSTSupport[0] |= (1 << panel_index)
            gfx_vbt.block_44.PanelIdentification[panel_index] = PanelType.OLED
            current_params.dpst_status = False

        # DPST level
        if requested_params.dpst_level:
            gfx_vbt.block_44.AgressivenessProfile4[panel_index] |= requested_params.dpst_level
            # For VBT version 257, DPST and OPST both access same VBT field for level
            current_params.opst_level = requested_params.opst_level

        if requested_params.dpst_status:
            gfx_vbt.block_44.XPSTSupport[0] |= (1 << panel_index)
            gfx_vbt.block_44.PanelIdentification[panel_index] = PanelType.LCD
            current_params.opst_status = False

        if gfx_vbt.apply_changes() is False:
            logging.error("\tFailed to apply changes to VBT")
            html.step_end()
            return False
        logging.info("\tSuccessfully applied VBT changes")

        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            logging.error("\tFailed to restart display driver after VBT update")
            html.step_end()
            return False
        logging.info("\tSuccessfully restarted display driver")

        gfx_vbt.reload()

    else:
        # fetch current status
        if requested_params.dpst_status is not None:
            current_params.dpst_status = bool((gfx_vbt.block_44.DpstEnable[0] & (1 << panel_index)) >> panel_index)
            current_params.dpst_level = gfx_vbt.block_44.AggressivenessProfile[panel_index] & 0x0f

        if requested_params.opst_status is not None:
            current_params.opst_status = bool((gfx_vbt.block_44.OPST[0] & (1 << panel_index)) >> panel_index)
            current_params.opst_level = gfx_vbt.block_44.AgressivenessProfile2[panel_index] & 0x0f

        # If caller doesn't care about OPST level, then assign the current level
        if requested_params.opst_level is None:
            requested_params.opst_level = current_params.opst_level

        # If caller doesn't care about DPST level, then assign the current level
        if requested_params.dpst_level is None:
            requested_params.dpst_level = current_params.dpst_level

        # compare expected and current value to return early
        if requested_params == current_params:
            logging.info(f"\tAll params are already set as requested in VBT for {panel.port}")
            html.step_end()
            return True

        # OPST level
        if requested_params.opst_level is not None:
            gfx_vbt.block_44.AgressivenessProfile2[panel_index] = requested_params.opst_level

        # OPST status
        if requested_params.opst_status is not None:
            if requested_params.opst_status:
                gfx_vbt.block_44.OPST[0] |= (1 << panel_index)
            else:
                gfx_vbt.block_44.OPST[0] &= ~(1 << panel_index)

        # DPST level
        if requested_params.dpst_level is not None:
            gfx_vbt.block_44.AggressivenessProfile[panel_index] = requested_params.dpst_level

        # DPST status
        if requested_params.dpst_status is not None:
            if requested_params.dpst_status:
                gfx_vbt.block_44.DpstEnable[0] |= (1 << panel_index)
            else:
                gfx_vbt.block_44.DpstEnable[0] &= ~(1 << panel_index)

        if gfx_vbt.apply_changes() is False:
            logging.error("\tFailed to apply changes to VBT")
            html.step_end()
            return False
        logging.info("\tSuccessfully applied VBT changes")

        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            logging.error("\tFailed to restart display driver after VBT update")
            html.step_end()
            return False
        logging.info("\tSuccessfully restarted display driver")

        gfx_vbt.reload()

        logging.info("\tVerifying that applied value is SET in VBT")
        # fetch current status
        if requested_params.dpst_status is not None:
            current_params.dpst_status = bool((gfx_vbt.block_44.DpstEnable[0] & (1 << panel_index)) >> panel_index)
            current_params.dpst_level = gfx_vbt.block_44.AggressivenessProfile[panel_index] & 0x0f

        if requested_params.opst_status is not None:
            current_params.opst_status = bool((gfx_vbt.block_44.OPST[0] & (1 << panel_index)) >> panel_index)
            current_params.opst_level = gfx_vbt.block_44.AgressivenessProfile2[panel_index] & 0x0f

    logging.info(f"VBT params after SET: {current_params}")

    # compare expected and current value
    if requested_params != current_params:
        logging.info(f"Requested Params: {requested_params}")
        logging.info(f"Current Params: {current_params}")
        logging.error(f"\tFailed to SET VBT Params as requested")
        html.step_end()
        return False

    logging.info(f"\tSuccessfully SET VBT Params as requested")
    html.step_end()
    return True


##
# @brief        API to set default VBT for DPST and OPST
# @param[in]    adapter object, Adapter from dut
# @param[in]    panel object, Panel from dut
# @return       True if update is success, False otherwise
def set_default_vbt(adapter: Adapter, panel: Panel):
    default_params = get_default_vbt_setting(adapter)
    return configure_vbt(adapter, panel, default_params)


##
# @brief        API to get default VBT setting for DPST and OPST
# @param[in]    adapter object, Adapter from dut
# @return       True if update is success, False otherwise
def get_default_vbt_setting(adapter: Adapter):
    vbt_params = XpstVbtParams()
    # DPST is enabled by default in every BKC
    vbt_params.dpst_status = True
    # From MTL+, DPST default level is 2
    vbt_params.dpst_level = 6 if adapter.name in common.PRE_GEN_14_PLATFORMS else 2
    # OPST is supported from ADL-P+
    vbt_params.opst_status = None if adapter.name in common.PRE_GEN_13_PLATFORMS + ['DG2'] else False
    # vbt level 0-1-2, driver level 1-2-3
    vbt_params.opst_level = None if adapter.name in common.PRE_GEN_13_PLATFORMS + ['DG2'] else 0

    return vbt_params


##
# @brief API to verify behavior as per VBT setting
# @param[in]    panel object, Panel
# @param[in]    feature - XpstFeature
# @param[in]    vbt_status  - current XPST status in VBT
# @param[in]    vbt_aggr_level - XPST aggressiveness level
# @param[in]    current_status - XPST feature current status
# @return       status, boolean, True if VBT DPST/OPST feature status and Level passes
#                                False otherwise
def verify_default_vbt(panel, feature, vbt_status, vbt_aggr_level, current_status):
    feature_str = XpstFeature(feature).name
    if feature == XpstFeature.OPST and vbt_aggr_level in [2, 3]:
        gdhm.report_driver_bug_pc(
            f"[PowerCons][{feature_str}] Aggressiveness level is not 1 in VBT by default for {panel.port}")
        return False

    #  DPST disabled in VBT
    if feature == XpstFeature.DPST:
        if vbt_status == 0:
            # reporting to GDHM as DPST default status should be enabled for GTA machines
            gdhm.report_driver_bug_pc(
                f"[PowerCons][{feature_str}] {feature_str} is not enabled in VBT by default for {panel.port}")
            if current_status:
                gdhm.report_driver_bug_pc(
                    f"[PowerCons][{feature_str}] {feature_str} is functional with feature disabled"
                    f" in VBT for {panel.port}")
                logging.error(f"FAIL: {feature_str} is functional on {panel.port}(PIPE_{panel.pipe})= NOT EXPECTED")
                return False

        if vbt_aggr_level == 1:
            if current_status:
                error_title = "{0} is functional with VBT AggressivenessLevel= 1 (Not Expected)". \
                    format(feature_str, vbt_aggr_level)
                logging.error(f"FAIL: {error_title}")
                gdhm.report_driver_bug_pc(f"[PowerCons][{feature_str}] {error_title}")
                return False
            logging.info("PASS: {1} is NOT functional with AggressivenessLevel= {0} (Expected)".format(
                vbt_aggr_level, feature_str))
        else:
            if current_status:
                logging.info(
                    "PASS: {1} is functional with AggressivenessLevel= {0} (Expected)".format(
                        vbt_aggr_level, feature_str))
            else:
                logging.error(
                    "PASS: {1} is NOT functional with AggressivenessLevel= {0} (Expected)".format(
                        vbt_aggr_level, feature_str))
                return False
    return True


##
# @brief        API to get histogram data from DiAna
# @param[in]    json_data json, json output from DiAna
# @return       bool, True if pass, False otherwise
def get_histogram_list(json_data):
    html.step_start("Get Histogram values from DiAna")
    current_histogram = []
    event_name = "DpstReadHistogram"
    field_name = "Histogram"
    for msg in json_data['ReportQueue']:
        if event_name + '(' in msg['Header']:
            for event in [msg['Header']]:
                ind = event.index(field_name + "= ")
                arr = (event[ind + len(field_name + "= "):]).split(',')

                # Total number of bin should always be 32
                if len(arr) != 32:
                    logging.error(f"Total number of Histogram Bins does not match: Expected= {32}, Actual= {len(arr)}")
                    html.step_end()
                    return current_histogram

                histogram_list = []
                for a in arr[0:32]:
                    histogram_list.append(int(a))
                current_histogram.append(histogram_list)

    html.step_end()
    return current_histogram


##
# @brief        API to verify image size and histogram count
# @param[in]    histogram_list list output from DiAna
# @param[in]    panel object, Panel
# @param[in]    count total number of iterations
# @param[in]    total_images total number of images
# @return       bool, True if pass, False otherwise and image_size
def verify_histogram_count_and_image_size(panel, histogram_list, total_images, count):
    status = True
    html.step_start("Verifying Histogram count and Image size")
    image_size = panel.current_mode.HzRes * panel.current_mode.VtRes
    gdhm_message = set()
    if len(histogram_list) != count * total_images:
        logging.error("Total number of histogram does not match with the image iteration."
                      f"Expected= {len(histogram_list)}, Actual= {count * total_images}")
        gdhm_message.add("[XPST] Total number of histogram does not match with the image iteration.")
        status = False

    # Total number of pixel count in each bin should be equal to the image size.
    for each_bin in histogram_list:
        pixel_count = 0
        pixel_count += sum(each_bin)
        if pixel_count != image_size:
            logging.error("Total pixel count does not match the image size."
                          f"Expected= {image_size}, Actual= {pixel_count}")
            status = False

    if status:
        logging.info("Total pixel count match the image size")
    else:
        logging.error("Total pixel count does not match the image size")
        gdhm_message.add(f"[XPST] Total pixel count does not match the image size.")

    for message in gdhm_message:
        gdhm.report_driver_bug_pc(message)

    html.step_end()
    return status, image_size


##
# @brief        Exposed API to get polling offsets for HW SFSU DPST and RGB Coefficients
# @param[in]     adapter object, Adapter
# @param[in]    feature XpstFeature
# @return       offsets list
def get_polling_offsets(adapter: Adapter, feature: XpstFeature):
    offsets = []
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        return offsets

    for panel in adapter.panels.values():
        if not panel.is_lfp:
            continue
        if XpstFeature.OPST == feature:
            offsets.append(
                MMIORegister.get_instance(
                    "DPST_PROG_COEF_REGISTER", "DPST_PROG_COEF_" + panel.pipe, adapter.name).offset)

        offsets.append(MMIORegister.get_instance("DPST_CTL_REGISTER", "DPST_CTL_" + panel.pipe, adapter.name).offset)
        offsets.append(
            MMIORegister.get_instance("DPST_SF_SEG_REGISTER", "DPST_SF_SEG_" + panel.pipe, adapter.name).offset)
        offsets.append(
            MMIORegister.get_instance("DPST_SF_CTL_REGISTER", "DPST_SF_CTL_" + panel.pipe, adapter.name).offset)

        if adapter.name not in common.PRE_GEN_16_PLATFORMS:
            offsets.append(
                MMIORegister.get_instance("DPST_GUARD2_REGISTER", "DPST_GUARD2_" + panel.pipe, adapter.name).offset)

    return offsets


##
# @brief        API to check XPST supported for the panel using IGCL
# @param[in]    panel object, Panel
# @return       dpst_status, boolean, True if supported, False otherwise
def igcl_is_xpst_supported(panel: Panel):
    dpst_flag = control_api_args.ctl_power_optimization_flags_v.DPST.value
    power_caps = control_api_args.ctl_power_optimization_caps_t()
    power_caps.Size = ctypes.sizeof(power_caps)

    if control_api_wrapper.get_power_caps(power_caps, panel.target_id) is False:
        logging.error("FAILED to get Power Optimization caps via Control Library")
        return None

    dpst_status = (dpst_flag == (power_caps.SupportedFeatures.value & dpst_flag))
    logging.info(f"DPST via Control Library, support= {dpst_status}")
    return dpst_status


##
# @brief         Exposed API to set DPST EPSM(Enhanced Power Saving Mode) using IGCL
# @param[in]     panel object, Panel
# @param[in]     enable_epsm boolean, True to enable, False to disable
# @param[in]     power_source enum, from display_power PowerSource
# @param[in]     power_scheme enum, from display_power PowerScheme
# @return        status Boolean, True success & restart required, None success & no restart required, False otherwise
def igcl_set_epsm(panel, enable_epsm, power_source: display_power.PowerSource,
                  power_scheme: display_power.PowerScheme):
    html.step_start(f"Configure EPSM status to {enable_epsm}")

    igcl_power_source = __igcl_map_power_source(power_source)
    igcl_power_plan = __igcl_map_power_plan(power_scheme)
    if igcl_power_source is None or igcl_power_plan is None:
        html.step_end()
        return False

    bklt_flag = control_api_args.ctl_power_optimization_dpst_flags_v.BKLT.value
    epsm_flag = control_api_args.ctl_power_optimization_dpst_flags_v.EPSM.value

    dpst_status = igcl_is_xpst_supported(panel)
    if dpst_status is not True:
        if dpst_status is False:
            logging.error(f"DPST is NOT supported for {panel.port}")
        html.step_end()
        return False

    # init dpst structure and get the complete args in dpst_args
    dpst_args = __igcl_init_dpst_structure(igcl_power_source, igcl_power_plan)
    if control_api_wrapper.get_dpst(dpst_args, panel.target_id) is False:
        logging.error("FAILED to Get DPST via Control Library")
        html.step_end()
        return False

    current_epsm_status = (epsm_flag == (dpst_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value & epsm_flag))
    if current_epsm_status == enable_epsm:
        logging.error(f"EPSM status is already {enable_epsm} for {panel.port}")
        html.step_end()
        return True

    # use dpst_args and change epsm flag
    logging.info("Setting DPST args via Control Library")
    dpst_args.FeatureSpecificData.DPSTInfo.EnabledFeatures = bklt_flag
    if enable_epsm:
        dpst_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value |= epsm_flag

    # set dpst with CAPI
    if control_api_wrapper.set_dpst(dpst_args, panel.target_id) is False:
        logging.error("FAILED to set DPST via Control Library")
        html.step_end()
        return False
    logging.info("Successfully Set DPST via Control Library")

    # Verify the value is Set using Get DPST
    logging.info("Getting DPST args via Control Library to verify applied values")
    # init structure for getting dpst
    get_dpst = __igcl_init_dpst_structure(igcl_power_source, igcl_power_plan)
    if control_api_wrapper.get_dpst(get_dpst, panel.target_id) is False:
        logging.error("FAILED to Get DPST via Control Library")
        html.step_end()
        return False
    logging.info("Successfully Get DPST via Control Library")

    epsm_status = (epsm_flag == (get_dpst.FeatureSpecificData.DPSTInfo.EnabledFeatures.value & epsm_flag))
    logging.info(f"EPSM status after SET= {epsm_status}")
    if epsm_status != enable_epsm:
        logging.error(f"FAILED to configure EPSM for {panel.port}. Expected= {enable_epsm}, Actual= {epsm_status}")
        html.step_end()
        return False

    logging.info(f"Successfully configured EPSM for {panel.port}. Expected= {enable_epsm}, Actual= {epsm_status}")
    html.step_end()
    return True


##
# @brief         Exposed API to set dpst aggressiveness Level using IGCL
# @param[in]     panel object, Panel object
# @param[in]     level int, value for aggressiveness Level
# @param[in]     power_source enum, from display_power PowerSource
# @param[in]     power_scheme enum, from display_power PowerScheme
# @return        status Boolean, True success & restart required, None success & no restart required, False otherwise
def igcl_set_aggressiveness_level(panel: Panel, level: int,
                                  power_source: display_power.PowerSource, power_scheme: display_power.PowerScheme):
    html.step_start(f"Set DPST Aggressiveness Level to value {level}")

    igcl_power_source = __igcl_map_power_source(power_source)
    igcl_power_plan = __igcl_map_power_plan(power_scheme)
    if igcl_power_source is None or igcl_power_plan is None:
        return False

    dpst_status = igcl_is_xpst_supported(panel)
    if dpst_status is not True:
        if dpst_status is False:
            logging.error(f"\tDPST is NOT supported for {panel.port}")
        html.step_end()
        return False

    # init dpst structure and get the complete args in dpst_args
    dpst_args = __igcl_init_dpst_structure(igcl_power_source, igcl_power_plan)
    if control_api_wrapper.get_dpst(dpst_args, panel.target_id) is False:
        logging.error("\tFAILED to Get DPST via Control Library")
        html.step_end()
        return False

    current_level = (level == dpst_args.FeatureSpecificData.DPSTInfo.Level)
    if current_level == level:
        logging.error(f"\tAggressiveness Level is already {current_level} for {panel.port}")
        html.step_end()
        return True

    # use dpst_args and change aggressiveness level
    dpst_args.FeatureSpecificData.DPSTInfo.Level = level

    # set dpst with CAPI
    if control_api_wrapper.set_dpst(dpst_args, panel.target_id) is False:
        logging.error("\tFAILED to set DPST via Control Library")
        html.step_end()
        return False
    logging.info("\tSuccessfully Set DPST via Control Library")

    # Verify the value is Set using Get DPST
    logging.info("\tValidating that required aggressiveness level is set")
    # init structure for getting dpst
    get_dpst = __igcl_init_dpst_structure(igcl_power_source, igcl_power_plan)
    if control_api_wrapper.get_dpst(get_dpst, panel.target_id) is False:
        logging.error("FAILED to Get DPST via Control Library")
        html.step_end()
        return False
    logging.info("\tSuccessfully Get DPST via Control Library")

    aggressiveness_level = get_dpst.FeatureSpecificData.DPSTInfo.Level
    logging.info(f"\tAggressiveness Level= {aggressiveness_level}")
    if aggressiveness_level != level:
        logging.error(f"FAILED to set Aggressiveness Level for {panel.port}. "
                      f"Expected= {level}, Actual= {aggressiveness_level}")
        html.step_end()
        return False

    logging.info(f"Successfully set Aggressiveness Level for {panel.port}. "
                 f"Expected= {level}, Actual= {aggressiveness_level}")
    html.step_end()
    return True


def __igcl_map_power_plan(power_plan: display_power.PowerScheme):
    igcl_power_plan = None
    if power_plan == display_power.PowerScheme.BALANCED:
        igcl_power_plan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
    elif power_plan == display_power.PowerScheme.POWER_SAVER:
        igcl_power_plan = control_api_args.ctl_power_optimization_plan_v.POWER_SAVER.value
    elif power_plan == display_power.PowerScheme.HIGH_PERFORMANCE:
        igcl_power_plan = control_api_args.ctl_power_optimization_plan_v.HIGH_PERFORMANCE.value
    else:
        logging.error(f"No IGCL mapping found for PowerPlan= {power_plan.name}")

    return igcl_power_plan


def __igcl_map_power_source(power_source: display_power.PowerSource):
    igcl_power_source = None
    if power_source == display_power.PowerSource.DC:
        igcl_power_source = control_api_args.ctl_power_source_v.DC.value
    elif power_source == display_power.PowerSource.AC:
        igcl_power_source = control_api_args.ctl_power_source_v.AC.value
    else:
        logging.error(f"No IGCL mapping found for PowerSource= {power_source.name}")

    return igcl_power_source


##
# @brief        API to initialize DPST structure for IGCL
# @param[in]    igcl_power_source enum, control_api_args.ctl_power_source_v
# @param[in]    igcl_power_plan enum, control_api_args.ctl_power_optimization_plan_v
# @return       dpst_status, boolean, True if supported, False otherwise
def __igcl_init_dpst_structure(igcl_power_source: control_api_args.ctl_power_source_v,
                               igcl_power_plan: control_api_args.ctl_power_optimization_plan_v):
    dpst_flag = control_api_args.ctl_power_optimization_flags_v.DPST.value
    dpst_args = control_api_args.ctl_power_optimization_settings_t()
    dpst_args.Size = ctypes.sizeof(dpst_args)
    dpst_args.PowerOptimizationFeature = dpst_flag
    dpst_args.PowerOptimizationPlan = igcl_power_plan
    dpst_args.PowerSource = igcl_power_source
    return dpst_args


##
# @brief        API to verify IGCL values
# @param[in]    adapter object, Adapter object from DUT
# @param[in]    panel object, Panel object from DUT
# @param[in]    feature enum, XpstFeature (DPST/ OPST)
# @param[in]    expected_status bool, status of the feature
# @param[in]    expected_lvl int, Aggressiveness level of the feature
# @return       status, boolean, True if successful, False otherwise
def verify_igcl_values(adapter: Adapter, panel: Panel, feature: XpstFeature, expected_status: bool, expected_lvl: int):
    html.step_start(f"Verifying IGCL values (Status & Levels) for {feature.name}")
    status = True

    # CAPI is supported from Gen13+
    if adapter.name in common.PRE_GEN_13_PLATFORMS:
        logging.info(f"\tCAPI is not supported for {adapter.name}. Skipping...")
        html.step_end()
        return True

    power_source = display_power.DisplayPower().get_current_powerline_status()
    power_scheme = display_power.DisplayPower().get_current_power_scheme()
    ftr_params = get_status(panel.target_id, power_source, power_scheme)

    if ftr_params is None:
        logging.error(f"FAILED to GET status from IGCL for {panel.port}")
        html.step_end()
        return False

    if feature == XpstFeature.OPST:
        igcl_status = (ftr_params.is_opst_enabled and ftr_params.is_opst_supported)
    else:
        igcl_status = (ftr_params.is_dpst_enabled and ftr_params.is_dpst_supported)
    igcl_cur_level = ftr_params.current_level

    if expected_status == igcl_status:
        logging.info(f"\tStatus value is matched. Expected= {expected_status}, Actual= {igcl_status}")
    else:
        logging.error(f"\tStatus value is mismatched. Expected= {expected_status}, Actual= {igcl_status}")
        status = False

    sku_name = None
    if adapter.name in ['ADLP']:
        sku_name = machine_info.SystemInfo().get_sku_name(adapter.gfx_index)

    expected_min_level = 1
    if expected_status:
        # For OPST and DPST v8(MTL+, and TWL), Max level is 3,
        if adapter.name not in common.PRE_GEN_14_PLATFORMS or feature == XpstFeature.OPST:
            expected_max_level = 3
        elif sku_name in ['TwinLake']:
            expected_max_level = 3
        else:
            expected_max_level = 6
    else:
        expected_min_level = 0
        expected_lvl = 0
        expected_max_level = 0

    if expected_lvl == ftr_params.current_level:
        logging.info(f"\tCUR Level value is matched. Expected= {expected_lvl}, Actual= {igcl_cur_level}")
    else:
        logging.error(f"\tCUR Level value is mismatched. Expected= {expected_lvl}, Actual= {igcl_cur_level}")
        status = False

    if expected_min_level == ftr_params.min_level:
        logging.info(f"\tIGCL MIN level is matched. Expected= {expected_min_level}, Actual= {ftr_params.min_level}")
    else:
        logging.error(f"\tIGCL MIN level is mismatched. Expected= {expected_min_level}, Actual= {ftr_params.min_level}")
        status = False

    if expected_max_level == ftr_params.max_level:
        logging.info(f"\tIGCL MAX Level is matched. Expected= {expected_max_level}, Actual= {ftr_params.max_level}")
    else:
        logging.error(f"\tIGCL MAX Level is mismatched. Expected= {expected_max_level}, Actual= {ftr_params.max_level}")
        status = False

    logging.info(f"\tIGCL EPSM Params.Supported= {ftr_params.is_epsm_supported}, Enabled= {ftr_params.is_epsm_enabled}")

    sku_name = None
    if adapter.name in ['ADLP']:
        sku_name = machine_info.SystemInfo().get_sku_name(adapter.gfx_index)

    is_default_epsm_expected = True
    if feature != XpstFeature.DPST or not expected_status or adapter.name not in common.PRE_GEN_14_PLATFORMS or sku_name in ['TwinLake']:
        is_default_epsm_expected = False

    # If DPST is supported, then EPSM is supported for DPST v6/ v7 but not enabled by default,
    # EPSM is not supported for V8 (TWL and MTL+)

    if is_default_epsm_expected:
        if ftr_params.is_epsm_supported is False or ftr_params.is_epsm_enabled is True:
            logging.error(f"\tIGCL EPSM default settings are invalid for DPST v6/v7. "
                          f"Expected Support= True and Enabled= False")
            status = False
    else:
        if ftr_params.is_epsm_supported or ftr_params.is_epsm_enabled:
            logging.error(f"\tIGCL EPSM default settings are invalid for DPST v8 or OPST. "
                          f"Expected Support= False and Enabled= False")
            status = False

    html.step_end()
    return status


##
# @brief        API to verify KEI for Min DPST Brightness
# @param[in]    adapter object, dut object
# @param[in]    panel object, dut object
# @param[in]    min_brightness int, Min DPST brightness (0-10_000)
# @return       status, boolean, True if successful, False otherwise
def verify_kei_min_brightness(adapter: Adapter, panel: Panel, min_brightness: int):
    html.step_start("Verifying KEI for Min DPST Brightness")
    status = True
    actual_brightness = []

    value_status, pwm_duty_output = __get_pwm_duty_values(adapter, panel)
    if value_status is False:
        return False

    value_status, pwm_freq_value = __get_pwm_freq(adapter, panel)
    if value_status is False:
        return False

    precision_factor = 100 if (panel.max_fall and panel.max_cll) == 0 else 1000

    # Iterating through DPST GUARD data
    for mmio_data in pwm_duty_output:
        brightness = math.ceil((mmio_data.Data * precision_factor * 100) / pwm_freq_value)
        actual_brightness.append(brightness)
        logging.debug(f"\tPWM_DUTY_CYCLE {hex(mmio_data.Offset)}= {mmio_data.Data} (BrightnessValue= {brightness})")
        if brightness < min_brightness:
            logging.error(f"\t\tAppliedBrightness= {brightness} is less than ExpectedBrightness= {min_brightness}")
            status = False
        else:
            logging.info(f"\t\tAppliedBrightness= {brightness} is more than ExpectedBrightness= {min_brightness}")

    if status is False:
        logging.error(f"\tFAIL: DPST Brightness is less than expected value {min_brightness}")
    else:
        logging.info(f"\tPASS: DPST brightness is not below expected value {min_brightness}")

    # Logging added for KEI Wiki
    logging.info(f"Applied Brightness List= {actual_brightness}")
    logging.info(f"\t\tXPST KEI Wiki Actual MinimumBrightness= {min(actual_brightness)}, "
                 f"Expected MinimumBrightness= {min_brightness}")

    html.step_end()
    return status


##
# @brief        API to verify KEI for Max Latency Phasing
# @param[in]    adapter object, dut object
# @param[in]    panel object, dut object
# @param[in]    feature enum, XpstFeature
# @param[in]    max_latency int, Max latency in ms
# @param[in]    time_stamps list, time_stamps of user setting/frame change
# @return       status, boolean, True if successful, False otherwise
def verify_kei_max_latency_phasing(adapter: Adapter, panel: Panel, feature: XpstFeature, max_latency: int, time_stamps):
    html.step_start("Verifying KEI for Max Latency Phasing [DPST Disable/Enable to IET Apply]")
    status = True
    actual_pwm_program_timestamp = []
    actual_iet_program_timestamp = []
    worst_program_timestamp = []
    timestamps_till_pwm = []
    timestamps_till_iet = []
    actual_latency = []

    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        dpst_bin = MMIORegister.get_instance("DPST_IE_BIN_REGISTER", "DPST_IE_BIN_" + panel.pipe, adapter.name)
    else:
        dpst_bin = MMIORegister.get_instance("DPST_BIN_REGISTER", "DPST_BIN_" + panel.pipe, adapter.name)

    dpst_bin_output = etl_parser.get_mmio_data(dpst_bin.offset, is_write=True)
    if dpst_bin_output is None:
        logging.warning(f"\tNo MMIO entry found for register DPST_BIN_REGISTER")
        return False

    # get ticks of ETL start
    etl_start_tick = etl_parser.get_event_data(etl_parser.Events.ETL_DETAILS)[0].SessionStartTime
    if etl_start_tick is None:
        logging.error("FAILED to get ETL start time")
        return False

    # convert ticks to python readable DateTime
    etl_start_time = datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=etl_start_tick // 10)

    # get iet program timestamps after user setting/ frame change
    for change_time in time_stamps:
        for iet in dpst_bin_output:
            # get time till iet program and convert to millisecond
            iet_time = (etl_start_time + datetime.timedelta(milliseconds=iet.TimeStamp))
            # compare time till pwm with user setting/frame change, if more, cache it
            if iet_time > change_time:
                timestamps_till_iet.append(iet_time)
                actual_iet_program_timestamp.append(iet.TimeStamp)
                # break the loop to go to next for loop because need to consider only first hit of IET
                break

    if feature == XpstFeature.OPST:
        worst_program_timestamp = timestamps_till_iet
    else:
        pwm_panel = "SBLC_PWM_DUTY" if panel.port == 'DP_A' else "SBLC_PWM_DUTY_2"
        pwm_duty = MMIORegister.get_instance("SBLC_PWM_DUTY_REGISTER", pwm_panel, adapter.name)
        pwm_duty_output = etl_parser.get_mmio_data(pwm_duty.offset, is_write=True)
        if pwm_duty_output is None:
            logging.warning(f"\tNo MMIO entry found for register {pwm_panel}")
            return False

        # get pwm program timestamps after user setting/ frame change
        for change_time in time_stamps:
            for pwm in pwm_duty_output:
                # get time till pwm program and convert to millisecond
                pwm_time = (etl_start_time + datetime.timedelta(milliseconds=pwm.TimeStamp))
                # compare time till pwm with user setting/frame change, if more, cache it
                if pwm_time > change_time:
                    timestamps_till_pwm.append(pwm_time)
                    actual_pwm_program_timestamp.append(pwm.TimeStamp)
                    # break the loop to go to next for loop because need to consider only first hit of PWM
                    break

        # get worst time from pwm or iet
        for pwm_time, iet_time in zip(timestamps_till_pwm, timestamps_till_iet):
            if pwm_time > iet_time:
                worst_program_timestamp.append(pwm_time)
            else:
                worst_program_timestamp.append(iet_time)

        logging.info(f"PWM Programming TimeStamp in ETL= {actual_pwm_program_timestamp}")
        logging.info(f"PWM Programming TimeStamp from Epoch to PWM= {timestamps_till_pwm}")
        logging.info(f"Worst time between first PWM and IET programming= {worst_program_timestamp}")

    logging.info(f"IET Programming TimeStamp in ETL= {actual_iet_program_timestamp}")
    logging.info(f"PWM Programming TimeStamp from Epoch to IET= {timestamps_till_iet}")
    logging.info(f"Time from Epoch to User setting/ frame change= {time_stamps}")
    logging.info(f"ETL start time= {etl_start_time}")

    # get program time in same unit of etl start time
    for program_time, user_time in zip(worst_program_timestamp, time_stamps):
        # till_program_time = etl_start_time + datetime.timedelta(milliseconds=program_time)
        # till_config_change = etl_start_time + datetime.timedelta(milliseconds=user_time)
        actual_latency.append(round((program_time - user_time).total_seconds() * 1000, 4))

    logging.info(f"Latency from User setting/frame change to first IET/PWM program= {actual_latency}")
    # calculate latency in programming value from xpst toggle
    for t, user in zip(actual_latency, time_stamps):
        if t > max_latency:
            logging.error(f"Time latency({t} ms) from UserEvent({user} ms) to "
                          f"Phasing Programming is more than Max latency ({max_latency} ms)")
            status = False
        else:
            logging.info(f"Time latency({t} ms) from UserEvent({user} ms) to "
                         f"Phasing Programming is NOT more than Max latency ({max_latency} ms)")

    if status is False:
        logging.error(f"FAIL: DPST maximum latency is greater than {max_latency}")
    else:
        logging.info(f"PASS: DPST maximum latency is less than {max_latency}")

    # Logging added for KEI Wiki
    logging.info(f"Time Latency list= {actual_latency}")
    logging.info(
        f"\t\tXPST KEI Wiki Actual MaximumLatency= {max(actual_latency)}, Expected MaximumLatency= {max_latency}")
    html.step_end()
    return status


def __get_kei_failure(json_file):
    status = True
    try:
        with open(json_file) as f:
            data = f.read()
            invalid_strings = re.findall('new Date\(\d+\)', data)
            for invalid_string in invalid_strings:
                data = data.replace(invalid_string, '"0"')
            d = json.loads(data)
            if "DPST_KEI_FAILURE" in data:
                for msg in d['TagStore'].get("DPST_KEI_FAILURE", []):
                    logging.error(f"(TimeStamp - {float(msg['TimeStamp']) / 1000} S): {msg['Details']}")
                    status = False
    except Exception as ex:
        logging.error(ex)
        return None

    return status


def __get_pwm_freq(adapter: Adapter, panel: Panel):
    pwm_freq_panel = "SBLC_PWM_FREQ" if panel.port == 'DP_A' else "SBLC_PWM_FREQ_2"
    pwm_freq = MMIORegister.get_instance("SBLC_PWM_FREQ_REGISTER", pwm_freq_panel, adapter.name)
    pwm_freq_output = etl_parser.get_mmio_data(pwm_freq.offset)
    if pwm_freq_output is None:
        logging.warning(f"\tNo MMIO entry found for register {pwm_freq_panel}")
        return False, 0
    return True, pwm_freq_output[-1].Data


def __get_pwm_duty_values(adapter: Adapter, panel: Panel):
    pwm_panel = "SBLC_PWM_DUTY" if panel.port == 'DP_A' else "SBLC_PWM_DUTY_2"
    pwm_duty = MMIORegister.get_instance("SBLC_PWM_DUTY_REGISTER", pwm_panel, adapter.name)
    pwm_duty_output = etl_parser.get_mmio_data(pwm_duty.offset)
    if pwm_duty_output is None:
        logging.warning(f"\tNo MMIO entry found for register {pwm_panel}")
        return False, 0
    return True, pwm_duty_output


def __get_phasing_region_from_event(panel: Panel, diana_file):
    phasing_region = []
    start_time = None
    with open(diana_file) as f:
        lines = f.readlines()
        for line in lines:
            if "DpstProcess" in line:
                if re.search("XPST_EVENT_DPST_PHASEOUT_STARTED", line) is not None and (
                        start_time is None and re.search(f"PIPE_{panel.pipe}", line)):
                    start_time = float(re.findall("[0-9]*\.[0-9]*", line)[0])
            elif "DpstRunAlgorithm" in line:
                if start_time is None and re.search(f"PIPE_{panel.pipe}", line):
                    start_time = float(re.findall("[0-9]*\.[0-9]*", line)[0])
            elif "Dpst7xPhaseCoordinatorApplyFinish" in line:
                if len(re.findall("ADJUST_DONE", line)) == 2 and re.search(f"PIPE_{panel.pipe}", line):
                    end_time = float(re.findall("[0-9]*\.[0-9]*", line)[0])
                    phasing_region.append((round(start_time * 1000, 4), round(end_time * 1000, 4)))
                    start_time = None

    logging.info(f"Phasing regions: {phasing_region} for {panel.pipe}")
    return None if phasing_region == [] else phasing_region


##
# @brief        API to verify KEI for Phasing Duration
# @param[in]    adapter object, dut object
# @param[in]    panel object, dut object
# @param[in]    log_file file, path of diana log
# @param[in]    feature enum, XpstFeature
# @param[in]    phasing_duration_range int, (Min, Max) in ms
# @param[in]    max_step_duration int, in ms
# @param[in]    max_step_variance int, in percent
# @param[in]    max_iet_miss_percent int, in percent
# @return       status, boolean, True if successful, False otherwise
def verify_kei_phasing_duration(adapter: Adapter, panel: Panel, log_file, feature: XpstFeature,
                                phasing_duration_range, max_step_duration, max_step_variance, max_iet_miss_percent):
    # Max(33, 1/currentRr)
    expected_interval = round(1000 / panel.current_mode.refreshRate, 4)
    max_step_variance = max(max_step_variance, expected_interval)
    phasing_duration_min = phasing_duration_range[0]
    phasing_duration_max = phasing_duration_range[1]
    status = True
    phasing_step_duration = []
    phasing_duration = []

    phasing_region_from_event = __get_phasing_region_from_event(panel, log_file)
    if phasing_region_from_event is None:
        return False

    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        dpst_bin = MMIORegister.get_instance("DPST_IE_BIN_REGISTER", "DPST_IE_BIN_" + panel.pipe, adapter.name)
    else:
        dpst_bin = MMIORegister.get_instance("DPST_BIN_REGISTER", "DPST_BIN_" + panel.pipe, adapter.name)

    pwm_panel = "SBLC_PWM_DUTY" if panel.port == 'DP_A' else "SBLC_PWM_DUTY_2"
    pwm_duty = MMIORegister.get_instance("SBLC_PWM_DUTY_REGISTER", pwm_panel, adapter.name)

    vbi_data = etl_parser.get_vbi_data(f"PIPE_{panel.pipe}")
    if vbi_data is None:
        logging.error(f"NO VBI data found for PIPE_{panel.pipe} in the ETL")
        return False
    first_vbi_time = vbi_data[0].TimeStamp

    # Iterating through all the phasing regions
    for start, end in phasing_region_from_event:
        pwm_step_duration_avg = 0
        pwm_total_time = 0
        last_bin_in_iteration = []
        vbi_after_last_bin = []
        temp_list = []

        # PWM programming happens for DPST only
        if feature == XpstFeature.DPST:
            temp_status, pwm_total_time = __get_pwm_phasing_data(pwm_duty.offset, start, end, max_step_variance)
            if temp_status is False:
                status = False

        # IET phasing region
        logging.info(f"Getting IET MMIO Programming between {start} and {end}")
        dpst_bin_output = etl_parser.get_mmio_data(dpst_bin.offset, True, start, end + 10)
        if dpst_bin_output is None:
            logging.error(f"\tNo MMIO entry found for DPST_BIN_REGISTER between {start} and {end + 10}")
            status = False
            continue

        # vbi time after iet start
        iet_start = dpst_bin_output[0].TimeStamp
        iet_end = dpst_bin_output[-1].TimeStamp

        # 33 mmio writes for each iteration
        step_count = len(dpst_bin_output) // 33
        logging.info(f"IET Programming Phasing Region(from MMIO)= ({iet_start}, {iet_end}), Steps= {step_count}")

        # check: phasing step duration variance (considering only IET)
        # get last bin of each iteration with 33 writes in each iteration
        for i in range(1, step_count + 1):
            last_bin_in_iteration.append(dpst_bin_output[i * 33 - 1])

        for index, bin_data in enumerate(last_bin_in_iteration):
            counter = 0
            while 1:
                # keeping +1 s threshold for expected interval to avoid float value check
                t2 = first_vbi_time + ((expected_interval + (expected_interval / 4)) * counter)
                counter += 1
                if t2 > bin_data.TimeStamp:
                    break
            vbi_after_last_bin.append(t2)

        vbi_duplicate_count = 0
        for vbi in vbi_after_last_bin:
            if vbi not in temp_list:
                temp_list.append(vbi)
            else:
                vbi_duplicate_count += 1

        logging.debug(f"TimeStamp of LastBin in Iteration= {[b.TimeStamp for b in last_bin_in_iteration]}")
        logging.debug(f"Timestamp of IET taking effect (with expected VBI)= {vbi_after_last_bin}")

        variance = round((vbi_duplicate_count / step_count) * 100, 4)
        logging.info("Check: Total number of IET programming (consider last bin time) between 2 VBI")

        # Disabling this check for LNL+ because with XPST_SMOOTHENING_PERIOD_DEFAULT macro change to 15ms, the delay
        # between the MMIO writes (0xC8258) should also be 15ms. In ETL, seeing in-consistency because programmatically
        # there is jitter due to OS scheduling/wait for active scanline.
        # The max duration is going around 32ms which means more that 100% error (considering 15ms).
        # Details in HSD: 16025631076

        if adapter.name in common.GEN_14_PLATFORMS:
            if variance > max_iet_miss_percent:
                logging.error(f"\tMore than 1 consecutive IET between VBI= {vbi_duplicate_count}. "
                              f"Percentage Expected= <{max_iet_miss_percent}%, Actual= {variance}%")
                status = False
            else:
                logging.info(f"\tMore than 1 consecutive IET between VBI= {vbi_duplicate_count}. "
                             f"Percentage Expected= <{max_iet_miss_percent}%, Actual= {variance}%")

        iet_total_time = vbi_after_last_bin[-1] - vbi_after_last_bin[0]
        iet_step_duration_avg = math.ceil(iet_total_time / step_count)
        total_time = round(max(iet_total_time, pwm_total_time), 4)
        phasing_duration.append(total_time)
        logging.info("Check: Total Phasing Duration (consider worst of PWM and IET)")
        logging.info(f"\tTotal IET Phasing Time= {iet_total_time} ms, PWM Phasing Time= {pwm_total_time} ms")
        if total_time > phasing_duration_max or total_time < phasing_duration_min:
            logging.error(f"\t\tPhasingDuration. Actual= {total_time}ms, Expected= {phasing_duration_range}ms")
            status = False
        else:
            logging.info(f"\t\tPhasingDuration. Actual= {total_time}ms, Expected= {phasing_duration_range}ms")

        logging.info("Check: StepDuration during Phasing (consider the worst step duration among IET and PWM)")
        max_step_time = max(pwm_step_duration_avg, iet_step_duration_avg)
        phasing_step_duration.append(max_step_time)
        if max_step_time > max_step_duration:
            logging.error(f"\t\tPhasingStepDuration. Actual= {max_step_time}ms, Expected= {max_step_duration}ms")
            status = False
        else:
            logging.info(f"\t\tPhasingStepDuration. Actual= {max_step_time}ms, Expected= {max_step_duration}ms")

    # Logging added for KEI Wiki
    logging.info(f"Phasing Duration= {phasing_duration}")
    logging.info(f"Phasing Step Duration List= {phasing_step_duration}")
    logging.info(f"\t\tXPST KEI Wiki Actual Maximum PhasingDuration= {max(phasing_duration)}, "
                 f"Expected Maximum PhasingDuration= {phasing_duration_range}")
    logging.info(f"\t\tXPST KEI Wiki Actual Maximum PhasingStepDuration= {max(phasing_step_duration)}, "
                 f"Expected Maximum PhasingStepDuration= {max_step_duration}")

    return status


##
# @brief        Exposed API to verify KEI where ETL would not have any Brightness or IET programming
# @param[in]    adapter object, dut object
# @param[in]    panel object, dut object
# @return       True if successful, False otherwise
def verify_kei_no_change(adapter: Adapter, panel: Panel):
    status = True
    # Check: Brightness is Max
    pwm_panel = "SBLC_PWM_DUTY" if panel.port == 'DP_A' else "SBLC_PWM_DUTY_2"
    pwm_duty = MMIORegister.get_instance("SBLC_PWM_DUTY_REGISTER", pwm_panel, adapter.name)
    pwm_duty_output = etl_parser.get_mmio_data(pwm_duty.offset, True)

    # PWM frequency
    pwm_freq_panel = "SBLC_PWM_FREQ" if panel.port == 'DP_A' else "SBLC_PWM_FREQ_2"
    pwm_freq = MMIORegister.read('SBLC_PWM_FREQ_REGISTER', pwm_freq_panel, adapter.name,
                                 gfx_index=adapter.gfx_index)

    precision_factor = 100 if (panel.max_fall and panel.max_cll) == 0 else 1000
    if pwm_duty_output is None:
        pwm_duty = MMIORegister.read('SBLC_PWM_DUTY_REGISTER', pwm_panel, adapter.name,
                                     gfx_index=adapter.gfx_index)
        brightness = math.ceil((pwm_duty.duty_cycle * precision_factor * 100) / pwm_freq.frequency)
        logging.debug(f"\tPWM_DUTY_CYCLE {hex(pwm_duty.offset)}= {pwm_duty.duty_cycle} (BrightnessValue= {brightness})")
        if brightness != 10000:
            logging.error(f"\t\tCurrentBrightness= {brightness} is NOT equal to ExpectedBrightness= 10000")
            status = False
        else:
            logging.info(f"\t\tCurrentBrightness= {brightness} is NOT equal to ExpectedBrightness= 10000")

    else:
        for pwm in pwm_duty_output:
            brightness = math.ceil((pwm.Data * precision_factor * 100) / pwm_freq.frequency)
            logging.debug(f"\tPWM_DUTY_CYCLE {hex(pwm.Offset)}= {pwm.Data} (BrightnessValue= {brightness})")
            # Max brightness value would be 10000
            if brightness != 10000:
                logging.error(f"\t\tCurrentBrightness= {brightness} is NOT equal to ExpectedBrightness= 10000")
                status = False
            else:
                logging.info(f"\t\tCurrentBrightness= {brightness} is NOT equal to ExpectedBrightness= 10000")

    # Check: DPST IET is 512
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        dpst_bin = MMIORegister.get_instance("DPST_IE_BIN_REGISTER", "DPST_IE_BIN_" + panel.pipe, adapter.name)
    else:
        dpst_bin = MMIORegister.get_instance("DPST_BIN_REGISTER", "DPST_BIN_" + panel.pipe, adapter.name)

    dpst_bin_output = etl_parser.get_mmio_data(dpst_bin.offset, is_write=True)
    if dpst_bin_output is None:
        logging.warning(f"\tNo MMIO entry found for register DPST_BIN_REGISTER")
        return False

    for bin_value in dpst_bin_output:
        logging.error(f"\tMMIO DPST_BIN_{panel.pipe}= {bin_value.Data} at {bin_value.TimeStamp} ms")
        # IET reset means 512 for each bin
        if bin_value.Data != 512:
            logging.error("\t\tBIN value is NOT 512 (Expected no change for DPST IET)")
            status = False
        else:
            logging.info("\t\tBIN value is 512 (Expected no change for DPST IET)")

    if status:
        logging.info("No Brightness or IET change is done in whole ETL (Expected)")
    else:
        logging.error("Brightness or IET change is done in whole ETL (Unexpected)")

    return status


##
# @brief      Exposed API to disable DPST via registry
# @param[in]  adapter object, Adapter
# @return     bool True is Successful, False is Failed or None if already disabled
def disable_dpst_in_regkey(adapter: Adapter):
    html.step_start(f"Disabling DPST for {adapter.name} via registry key")
    feature_tc = registry.FeatureTestControl(adapter.gfx_index)
    if feature_tc.dpst_disable == 1:
        logging.info("\tDPST is already disabled in registry")
        html.step_end()
        return None

    feature_tc.dpst_disable = 1
    status = feature_tc.update(adapter.gfx_index)
    if status is False:
        logging.error("\tFAILED to Disable DPST in registry")
        html.step_end()
        return False

    logging.info("\tSuccessfully Disabled DPST in registry")
    return True


##
# @brief      Exposed API to enable DPST via registry
# @param[in]  adapter object, Adapter
# @return     bool True is Successful, False is Failed or None if already enabled
def enable_dpst_in_regkey(adapter: Adapter):
    html.step_start(f"Enabling DPST for {adapter.name} via registry key")
    feature_tc = registry.FeatureTestControl(adapter.gfx_index)
    if feature_tc.dpst_disable == 0:
        logging.info("\tDPST is already enabled in registry")
        html.step_end()
        return None

    feature_tc.dpst_disable = 0
    status = feature_tc.update(adapter.gfx_index)
    if status is False:
        logging.error("\tFAILED to Enable DPST in registry")
        html.step_end()
        return False

    logging.info("\tSuccessfully Enabled DPST in registry")
    return True


##
# @brief      Exposed API to disable OPST via registry
# @param[in]  adapter object, Adapter
# @return     bool True is Successful, False is Failed or None if already disabled
def disable_opst_in_regkey(adapter: Adapter):
    html.step_start(f"Disabling OPST for {adapter.name} via registry key")
    display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
    if display_pc.DisableOpst == 1:
        logging.info("\tOPST is already disabled in registry")
        html.step_end()
        return None

    display_pc.DisableOpst = 1
    status = display_pc.update(adapter.gfx_index)
    if status is False:
        logging.error("\tFAILED to Disable OPST in registry")
        html.step_end()
        return False

    logging.info("\tSuccessfully Disabled OPST in registry")
    return True


##
# @brief      Exposed API to enable OPST via registry
# @param[in]  adapter object, Adapter
# @return     bool True is Successful, False is Failed or None if already enabled
def enable_opst_in_regkey(adapter: Adapter):
    html.step_start(f"Enabling OPST for {adapter.name} via registry key")
    display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
    if display_pc.DisableOpst == 0:
        logging.info("\tOPST is already enabled in registry")
        html.step_end()
        return None

    display_pc.DisableOpst = 0
    status = display_pc.update(adapter.gfx_index)
    if status is False:
        logging.error("\tFAILED to Enable OPST in registry")
        html.step_end()
        return False

    logging.info("\tSuccessfully Enabled OPST in registry")
    return True


##
# @brief      Exposed API to generate report for KEI
# @param[in]  etl_file file, file path to etl
# @return     status, file_path, True and path if Successful, False and None otherwise
def generate_report_kei(etl_file):
    if etl_file is None:
        return False, None

    file_name = f"{etl_file}_{time.time()}.txt"
    parser_cfg = etl_parser.EtlParserConfig()
    parser_cfg.mmioData = 1
    parser_cfg.vbiData = 1
    parser_cfg.commonData = 1
    logging.info(f"\tGenerating EtlParser Report for {etl_file}")
    if etl_parser.generate_report(etl_file, parser_cfg) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        html.step_end()
        return False, None
    logging.info("\tSuccessfully generated ETL Parser report")

    status = os.system(f"{__DIANA_EXE} {etl_file} -report info -dpst > {file_name}")
    logging.debug(f"Diana execution status = {bool(status)}")

    try:
        output_file = os.path.join(os.getcwd(), file_name)
        if not os.path.exists(output_file):
            logging.error(f"{output_file} NOT found (Test Issue)")
            return False, None
        file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        shutil.move(output_file, file_path)

    except Exception as ex:
        logging.error(ex)
        return False, None

    return True, file_path


def __get_pwm_phasing_data(pwm_offset, start, end, max_step_variance):
    # PWM phasing region
    logging.info(f"Getting PWM MMIO Programming between {start} and {end}")
    pwm_duty_output = etl_parser.get_mmio_data(pwm_offset, True, start, end + 10)
    if pwm_duty_output is None:
        logging.error(f"\tNo MMIO entry found for SBLC_PWM_DUTY_REGISTER between {start} and {end + 10}")
        return False, 0

    pwm_start = pwm_duty_output[0].TimeStamp
    pwm_end = pwm_duty_output[-1].TimeStamp

    logging.info(f"\tPWM Programming Phasing Region= ({pwm_start}, {pwm_end})")

    pwm_total_time = pwm_end - pwm_start
    # first entry of pwm_duty_output is skipped, hence decrementing step_count
    step_count = len(pwm_duty_output) - 1
    pwm_step_duration_avg = pwm_total_time // step_count

    # check: phasing step duration variance (considering only PWM)
    logging.info("Check: Phasing Step Duration Variance from PWM programming")
    t1 = 0
    temp_list = []
    for index, pwm_data in enumerate(pwm_duty_output):
        # skip first entry because that would be starting point
        if index == 0:
            t1 = pwm_data.TimeStamp
            continue

        t2 = pwm_data.TimeStamp
        temp_value = round(abs(abs(t2 - t1) - pwm_step_duration_avg) ** 2, 4)
        # get delta between t2 and t1, subtract with mean, square it and cache it
        logging.debug(f"\tt2= {t2}, t1= {t1}, Mean= {pwm_step_duration_avg}")
        temp_list.append(temp_value)
        t1 = pwm_data.TimeStamp

    # variance s = sqrt(sum(xi-mean)^2 / step_count - 1). Skip first entry so have 1 less step
    sample_variance = math.sqrt(sum(temp_list) / (step_count - 1))
    pwm_variance_percent = round((sample_variance / pwm_step_duration_avg) * 100, 4)
    logging.info(f"\tPWM Phasing Data: Start= {pwm_start}ms, End= {pwm_end}ms, Delta= {pwm_total_time}ms, "
                 f"Steps= {step_count}, SampleVariance= {sample_variance}, "
                 f"StepDurationAverage= {pwm_step_duration_avg}ms, Variance= {pwm_variance_percent}%")

    status = True
    logging.info("\tCheck: Phasing Step Duration Variance for PWM")
    if pwm_variance_percent > max_step_variance:
        logging.error(f"\t\tPhasingStepDuration variance. "
                      f"Actual= {pwm_variance_percent}%, Expected= {max_step_variance}%")
        status = False
    else:
        logging.info(f"\t\tPhasingStepDuration variance. "
                     f"Expected= {max_step_variance}%, Actual= {pwm_variance_percent}%")

    return status, pwm_total_time


##
# @brief        Exposed API to verify only HistogramRead and no WorkItemCallback
# @param[in]    diana_file string, path to diana parsed text file
# @param[in]    hist_read_count int, number of enable DPST, level change, EPSM enable will be config change
# @param[in]    work_item_count int, number of expected hw interrupt to driver
# @return       True if successful, False otherwise
def verify_hist_read_and_work_item_count(diana_file, hist_read_count, work_item_count):
    status = True
    actual_hist_read_count = 0
    actual_work_item_count = 0

    with open(diana_file) as f:
        lines = f.readlines()
        for line in lines:
            if "DpstReadHistogram" in line:
                actual_hist_read_count += 1
                logging.debug(f"DiAna Logging: {line}")
            elif "DpstWorkItemCallback" in line:
                actual_work_item_count += 1
                logging.debug(f"DiAna Logging: {line}")

    logging.info(f"Total HistogramRead count= {actual_hist_read_count}, WorkItemCallback= {actual_work_item_count}")

    if actual_work_item_count != work_item_count:
        logging.error(f"WorkItem callback count. Expected= {work_item_count}, Actual= {actual_work_item_count}")
        status = False

    if actual_hist_read_count != hist_read_count:
        logging.error(f"HistogramRead count. Expected= {hist_read_count}, Actual= {actual_hist_read_count}")
        status = False

    return status


##
# @brief        Exposed API to get max expected brightness
# @param[in]    adapter object, dut object
# @param[in]    xpst_data object, XpstStatus object
# @return       True if successful, False otherwise
def get_capped_dpst_brightness(adapter: Adapter, xpst_data: XpstStatus):
    epsm_weight = 100
    max_epsm_weight = 100
    dpst_8_max_brightness = {1: 9500, 2: 8500, 3: 8500}

    max_brightness = dpst_8_max_brightness[xpst_data.current_level]
    if xpst_data.is_epsm_enabled:
        value = registry.read(adapter.gfx_index, registry.RegKeys.DPST.EPSM_WEIGHT)
        if value is not None:
            epsm_weight = value
        max_brightness = max_brightness * (epsm_weight / max_epsm_weight)

    return math.ceil(max_brightness)


##
# @brief        Exposed API to check max dpst applied brightness
# @param[in]    panel object, dut object
# @param[in]    diana_file string, path to diana parsed text file
# @param[in]    max_dpst_brightness int
# @return       True if successful, False otherwise
def verify_dpst_brightness_capped(panel: Panel, diana_file, max_dpst_brightness):
    final_dpst_brightness = []
    status = True

    with open(diana_file) as f:
        lines = f.readlines()
        for line in lines:
            if "Dpst7xPhaseCoordinatorApplyFinish" in line:
                if len(re.findall("ADJUST_DONE", line)) == 2 and re.search(f"PIPE_{panel.pipe}", line):
                    matched_line = re.findall("DpstPhaseAdjustInfo\(State= ADJUST_DONE, Target= [0-9]*", line)
                    for l in matched_line:
                        final_dpst_brightness.append(l.split(" ")[-1])

    logging.info(f"Last DPST Brightness with adjustment done: {final_dpst_brightness} for {panel.pipe}")
    if len(final_dpst_brightness) == 0:
        logging.error("No data found for DPST brightness")
        return False

    logging.info(f"Checking DPST brightness is under capped brightness ({max_dpst_brightness})")
    for value in final_dpst_brightness:
        if int(value) > max_dpst_brightness:
            logging.error(f"\tFinal DPST Brightness. Expected= {max_dpst_brightness}, Actual= {value}")
            status = False
        else:
            logging.info(f"\tFinal DPST Brightness. Expected= {max_dpst_brightness}, Actual= {value}")

    return status


##
# @brief         Exposed API to delete persistence registry keys for xPST
# @param[in]     adapter object, Adapter
# @return        status Boolean, True success & restart required, None success & no restart required, False otherwise
def delete_persistence(adapter):
    do_driver_restart = None
    status = registry.delete(adapter.gfx_index, key=registry.RegKeys.DC_POWER_POLICY_DATA)
    if status is False:
        logging.error(f"FAILED to delete {registry.RegKeys.DC_POWER_POLICY_DATA}")
        return False
    logging.info(f"Successfully deleted {registry.RegKeys.DC_POWER_POLICY_DATA}")
    if status is True:
        do_driver_restart = True

    status = registry.delete(adapter.gfx_index, key=registry.RegKeys.AC_POWER_POLICY_DATA)
    if status is False:
        logging.error(f"FAILED to delete {registry.RegKeys.AC_POWER_POLICY_DATA}")
        return False
    logging.info(f"Successfully deleted {registry.RegKeys.AC_POWER_POLICY_DATA}")
    if status is True:
        do_driver_restart = True

    status = registry.delete(adapter.gfx_index, key=registry.RegKeys.POWER_PLAN_AWARE_SETTINGS)
    if status is False:
        logging.error(f"FAILED to delete {registry.RegKeys.POWER_PLAN_AWARE_SETTINGS}")
        return False
    logging.info(f"Successfully deleted {registry.RegKeys.POWER_PLAN_AWARE_SETTINGS}")
    if status is True:
        do_driver_restart = True

    status = registry.delete(adapter.gfx_index, key=registry.RegKeys.DC_USER_PREFERENCE_POLICY)
    if status is False:
        logging.error(f"FAILED to delete {registry.RegKeys.DC_USER_PREFERENCE_POLICY}")
        return False
    logging.info(f"Successfully deleted {registry.RegKeys.DC_USER_PREFERENCE_POLICY}")
    if status is True:
        do_driver_restart = True

    status = registry.delete(adapter.gfx_index, key=registry.RegKeys.AC_USER_PREFERENCE_POLICY)
    if status is False:
        logging.error(f"FAILED to delete {registry.RegKeys.AC_USER_PREFERENCE_POLICY}")
        return False
    logging.info(f"Successfully deleted {registry.RegKeys.AC_USER_PREFERENCE_POLICY}")
    if status is True:
        do_driver_restart = True

    return do_driver_restart
