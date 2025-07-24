#######################################################################################################################
# @file         dut.py
# @brief        Contains helper APIs for multi-adapter tests
#
# @author       Rohit Kumar
#######################################################################################################################

import csv
import copy
import logging
import math
import os
import platform
import re
import subprocess
import sys
import time

from DisplayRegs.DisplayOffsets import TransDDiCtl2OffsetsValues
from Libs.Core import cmd_parser, app_controls, display_utility, display_power, driver_escape, display_essential, \
    registry_access
from Libs.Core import enum
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.display_config import display_config_struct as cfg_struct
from Libs.Core.logger import html, gdhm
from Libs.Core.sw_sim.driver_interface import DriverInterface
from Libs.Core.test_env import test_context
from Libs.Core.vbt.vbt import Vbt
from Libs.Core.wrapper import control_api_wrapper, control_api_args
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.hdmi.hf_vsdb_block import HdmiForumVendorSpecificDataBlock
from Libs.Feature.mipi import mipi_helper
from Libs.Feature.powercons import registry
from Tests.PowerCons.Modules import dpcd, common
from Tests.PowerCons.Modules.dut_context import *

ARC_SYNC_PROFILE = control_api_args.ctl_intel_arc_sync_profile_v


adapters: Dict[str, Adapter] = {
    gfx_index: Adapter(gfx_index, adapter_info)
    for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
}
__FRAME_UPDATE_PATH = os.path.join(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "PowerCons"), "FrameUpdate.exe")
NEGATIVE_VRR_PNP_ID = ["26cd7061000000000000", "05e3022200000000001d", "410c1d09b5690f002d1b", "21690000000000000000",
                       "05e30222b5690f00011f", "05e3022400000000001d", "05e3022400000000001e", "05e3022700000000001d",
                       "05e3022700000000011e", "0Ce3922400000000011e", "0Ce3922700000000011e", "25e4c24301000000011f",
                       "25e4bc4301000000011f", "25e4111901000000011d", "25e40f1901000000011d", "410c500900000000011e",
                       "410c51c200000000011e", "410c660900000000011e", "410c2909b5690f00151c", "410c430900000000001d",
                       "410c440900000000001d", "410c450900000000001d", "410c19c200000000001d", "410c10c200000000001d",
                       "410c4f0900000000001d", "410c400900000000001d", "410c1ac200000000001d", "410c0fc200000000001d",
                       "410c1bc200000000001d"]
__display_power = display_power.DisplayPower()


##
# @brief        Helper API to check for multi-RR panels
# @param[in]    panel, Panel
# @return       status, Boolean, True if panel is multi-RR, False otherwise
def __is_multi_rr(panel: Panel) -> bool:
    # Conditions for multi-RR
    # 1. 2 DTD with different pixel clocks
    # 2. 1 DTD + MRL
    if len(panel.pixel_clocks) > 1:
        return True

    edid_flag, edid_data, _ = driver_escape.get_edid_data(panel.display_info.DisplayAndAdapterInfo)
    if not edid_flag:
        status, reboot_required = display_essential.restart_gfx_driver()
        edid_flag, edid_data, _ = driver_escape.get_edid_data(panel.display_info.DisplayAndAdapterInfo)
        if not edid_flag:
            logging.error(f"Failed to get EDID data for target_id : {panel.target_id}")
            assert edid_flag, "Failed to get EDID data"
        assert edid_data

    index = 54  # start of 1st 18 byte descriptor
    while index < 126:
        if edid_data[index + 3] == 0xFD:  # 0xFD is display range limits block
            return True
        index += 18

    return False


##
# @brief        Helper API to check for getting VBT data and map with feature
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       None
def __init_vbt_data(adapter: Adapter, panel: Panel):
    gfx_vbt = Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)

    if panel.is_lfp:
        # get psr status
        if gfx_vbt.version > 227:
            panel.psr_caps.is_enabled_in_vbt = (gfx_vbt.block_44.PsrEnable[0] & (1 << panel_index)) >> panel_index == 1


##
# @brief        Helper API to get panels from command line
# @param[in]    adapter Adapter object
# @param[in]    cmd_line_params list
# @return       None
def __get_panels(adapter: Adapter, cmd_line_params):
    sorted_display_list = cmd_parser.get_sorted_display_list(cmd_line_params)
    adapter.lfp_count = 0
    for display_info in sorted_display_list:
        if adapter.gfx_index not in display_info.keys():
            continue

        # Get other display parameters from parsed command line output based on gfx_index and display port
        d_info = cmd_line_params[adapter.index][display_info[adapter.gfx_index]]

        panel_data = display_utility.get_panel_edid_dpcd_info(
            d_info['connector_port'], d_info['panel_index'], d_info['is_lfp'])
        if panel_data is None:
            raise Exception("Invalid panel index found: {0}".format(d_info['panel_index']))

        if 'HDMI' in d_info['connector_port']:
            edid_path = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'HDMI', panel_data['edid'])
            assert os.path.exists(edid_path)
            panel_data['edid'] = edid_path
        elif 'DP' in d_info['connector_port']:
            if os.path.exists(os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'eDP_DPSST', panel_data['edid'])):
                panel_data['edid'] = os.path.join(
                    test_context.PANEL_INPUT_DATA_FOLDER, 'eDP_DPSST', panel_data['edid'])
                panel_data['dpcd'] = os.path.join(
                    test_context.PANEL_INPUT_DATA_FOLDER, 'eDP_DPSST', panel_data['dpcd'])
            elif os.path.exists(
                    os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'DP_MST_TILE', panel_data['edid'])):
                panel_data['edid'] = os.path.join(
                    test_context.PANEL_INPUT_DATA_FOLDER, 'DP_MST_TILE', panel_data['edid'])
                panel_data['dpcd'] = os.path.join(
                    test_context.PANEL_INPUT_DATA_FOLDER, 'DP_MST_TILE', panel_data['dpcd'])
            else:
                raise Exception(
                    "EDID file {0} given for {1} doesn't exist in [eDP_DPSST, DP_MST_TILE] directories".format(
                        panel_data['edid'], d_info['connector_port']))
        panel = Panel(
            gfx_index=adapter.gfx_index,
            port=d_info['connector_port'],
            port_type=d_info['connector_port_type'],
            is_lfp=d_info['is_lfp'],
            panel_index=d_info['panel_index'],
            edid_path=panel_data['edid'],
            dpcd_path=panel_data['dpcd'],
            description=panel_data['desc']
        )
        adapter.panels[panel.port] = panel
        if panel.is_lfp:
            adapter.lfp_count += 1


##
# @brief        Helper API to get EDP caps for given panel
# @param[in]    panel Panel
def __get_edp_caps(panel: Panel):
    panel.edp_caps.edp_revision = dpcd.get_edp_revision(panel.target_id)

    caps = dpcd.EdpGeneralCapsReg(panel.target_id)
    panel.edp_caps.is_set_power_capable = (caps.set_power_capable == 1)

    if panel.edp_caps.edp_revision > dpcd.EdpDpcdRevision.EDP_DPCD_1_1_OR_LOWER:
        caps = dpcd.EdpConfigurationSet(panel.target_id)
        panel.edp_caps.is_assr_supported = (caps.alternate_scrambler_reset_enable == 1)

    caps = dpcd.EdpMsoCaps(panel.target_id)
    panel.edp_caps.mso_segments = caps.no_of_links


##
# @brief        Helper API to get VESA caps for given panel
# @param[in]    panel Panel
# @return       None
def __get_vesa_caps(panel: Panel):
    caps = dpcd.EdpGeneralCapability2(panel.target_id)
    if caps.PanelLuminanceControlCapable:
        panel.vesa_caps.is_nits_brightness_supported = True
    if caps.SmoothBrightnessCapable:
        panel.vesa_caps.is_smooth_brightness_supported = True
    if caps.VariableBrightnessControlCapable and caps.VariableBrightnessStrengthControlCapable:
        panel.vesa_caps.is_variable_brightness_supported = True


##
# @brief        Helper API to get HDR caps for given panel
# @param[in]    panel Panel object
# @return       None
def __get_hdr_static_metadata(panel: Panel):
    caps = dpcd.HdrCaps(panel.target_id)
    rx_feature_support = dpcd.RxFeatureList(panel.target_id)
    hdr_params = dpcd.HdrCtlParams(panel.target_id)
    panel.hdr_caps.enable_sdp_override_aux = hdr_params.enable_sdp_override_aux
    if caps.aux_only_brightness_for_sdr_hdr:
        panel.hdr_caps.is_aux_only_brightness = True
    if caps.support_sdp_for_colorimetry:
        panel.hdr_caps.colorimetry_with_sdp_supported = True
    if caps.support_brightness_optimization:
        panel.hdr_caps.brightness_optimization_supported = True
    if caps.support_brightness_ctrl_in_nits_level_using_Aux:
        panel.hdr_caps.brightness_ctrl_in_nits_level_using_Aux_supported = True
        # For EDP panel, both 2210h BIT 3 and 341h BIT 6 should be set for colorimetry support
    panel.hdr_caps.colorimetry_support = rx_feature_support.vsc_sdp_extension_for_colorimetry_supported and \
                                         panel.hdr_caps.colorimetry_with_sdp_supported

    edid_flag, edid_data, _ = driver_escape.get_edid_data(panel.display_info.DisplayAndAdapterInfo)
    if not edid_flag:
        logging.error(f"Failed to get EDID data for target_id : {panel.target_id}")
        assert edid_flag, "Failed to get EDID data"
    assert edid_data
    extension_blocks = edid_data[126]
    if extension_blocks >= 1:
        for block in range(1, extension_blocks + 1):
            # Extension tag and revision for CEA header
            if edid_data[block * 128] == 0x2 and edid_data[block * 129] in [0x01, 0x03]:
                index = (block * 128) + 4  # 4 bytes for header
                data_block = edid_data[index]
                while data_block:
                    length = data_block & 0x1f
                    # HDR static meta data block (7 bytes)
                    # Byte 0 : Tag code = 07h (Bit 7-5) | length of data block(in bytes)  (Bit 4-0)
                    # Byte 1 : extended tag = 06h
                    # Byte 4 : Desired Content Max Luminance data (8 bits) - MaxCll
                    # Byte 5 : Desired Content Max Frame-average Luminance data (8 bits) - MaxFall
                    # Byte 6 : Desired Content Min Luminance data (8 bits) - MinCll
                    # MaxFall = MaxCll = 50 * 2^(CV/32)
                    if (data_block >> 5) == 0x7 and edid_data[index + 1] == 0x6:
                        panel.max_cll = math.floor(50 * pow(2, (edid_data[index + 4] / 32)))
                        panel.max_fall = math.floor(50 * pow(2, (edid_data[index + 5] / 32)))
                        # MinCll = MaxCll * (CV/255)^2 / 100
                        panel.min_cll = round(panel.max_cll * pow((edid_data[index + 6] / 255), 2) / 100)
                        if panel.hdr_caps.is_hdr_supported is False and caps.supports_2084_decode and \
                                caps.supports_2020_gamut and caps.support_brightness_ctrl_in_nits_level_using_Aux:
                            panel.hdr_caps.is_hdr_supported = True
                        break
                    else:
                        index += length + 1
                        data_block = edid_data[index]


##
# @brief        Helper API to get LRR caps for given panel
# @param[in]    panel Panel object
# @return       None
def __get_rr_switching_caps(panel: Panel):
    adapter = adapters[panel.gfx_index]
    __get_psr_caps(panel)
    __get_vrr_caps(panel)
    caps = dpcd.LrrUbrrCaps(panel.target_id)
    value = None
    psr_disabled = False

    if panel.pnp_id is not None:
        key = registry.RegKeys.LRR.LRR_VERSION_CAPS_OVERRIDE + '_' + panel.pnp_id
        value = registry.read(adapter.gfx_index, key)
        if value is not None:
            if value == registry.RegValues.LRR.LRR_VERSION_1_0:
                caps.source_pixel_clock_based = 1
                caps.t_con_based = 0
                caps.source_v_total_based = 0
                panel.vrr_caps.is_vrr_supported = False
            elif value == registry.RegValues.LRR.LRR_VERSION_2_0:
                caps.source_pixel_clock_based = 0
                caps.t_con_based = 1
                caps.source_v_total_based = 0
            elif value == registry.RegValues.LRR.LRR_VERSION_2_5:
                caps.source_pixel_clock_based = 0
                caps.t_con_based = 1
                caps.source_v_total_based = 1

    panel.drrs_caps.min_rr = panel.min_rr
    panel.drrs_caps.max_rr = panel.max_rr
    panel.drrs_caps.actual_min_rr = panel.actual_min_rr
    panel.drrs_caps.actual_max_rr = panel.actual_max_rr

    # If MRL is present, RR range will be considered from MRL
    if (panel.vrr_caps.min_rr != 0) and (panel.vrr_caps.max_rr != 0):
        panel.drrs_caps.min_rr = panel.vrr_caps.min_rr
        panel.drrs_caps.max_rr = panel.vrr_caps.max_rr

    panel.drrs_caps.min_pixel_clock = min(panel.pixel_clocks)
    panel.drrs_caps.max_pixel_clock = max(panel.pixel_clocks)

    # Check if PSR is disabled
    feature_test_control = registry.FeatureTestControl(adapter.gfx_index)
    if feature_test_control.psr_disable == 1:
        psr_disabled = True

    # BFR support
    # If HRR is enabled and 2*minRR > MaxRR, BFR is not supported. RCR: VSDI-36283
    # 1. HRR is not supported on PSR1 panels
    # 2. HRR will not be enabled when OS FlipQ is enabled only on ADLP/RPLP
    # 3. HRR will not be enabled if disabled in registry key
    # BFR is supported only from TGL
    panel.bfr_caps.is_bfr_supported = False
    if panel.vrr_caps.is_vrr_supported and (adapter.name not in PRE_GEN_12_PLATFORMS + ['DG1']):
        display_fc2 = registry.DisplayFeatureControl2(adapter.gfx_index)
        if display_fc2.DisableVirtualRefreshRateSupport == 0:
            panel.bfr_caps.is_bfr_supported = True

    # Only DMRRS is supported on DP VRR panels from Gen11+
    # Only VTotal H/W based RR switching is supported on external panels.
    if panel.is_lfp is False:
        if panel.vrr_caps.is_vrr_supported and adapter.is_yangra:
            panel.drrs_caps.is_dmrrs_supported = True
            panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW

        # LRR and DRRS are not supported on external panels. No need to continue further.
        return

    if adapter.name not in common.PRE_GEN_12_PLATFORMS and caps.value != 0 and \
            value != registry.RegValues.LRR.LRR_VERSION_INVALID:
        # Gen12+
        if __is_multi_rr(panel) is False:
            # No LRR
            # DRRS/DMRRS available using pixel clock switching technique (if panel supports 2 Refresh Rates)
            if len(panel.rr_list) > 1:
                panel.drrs_caps.is_drrs_supported = True
                panel.drrs_caps.min_rr = panel.min_rr
                panel.drrs_caps.max_rr = panel.max_rr
                panel.lrr_caps.rr_switching_method = RrSwitchingMethod.CLOCK
        else:
            if panel.psr_caps.is_psr2_supported or panel.pr_caps.is_pr_supported:
                if panel.vrr_caps.is_vrr_supported:
                    if adapter.name in common.PRE_GEN_14_PLATFORMS:
                        if caps.source_v_total_based:
                            if caps.t_con_based and (panel.drrs_caps.min_rr > 24):
                                # VRR + PSR2 + 314H Bit2 = 1 + Bit1 = 1 + MinRR > 24
                                # LRR2.5
                                # Idle - PSR2 SU
                                # Media PB - PSR2 disable -> Change RR via VTotal -> Enable PSR2 SU mode
                                panel.lrr_caps.is_lrr_supported = True
                                panel.lrr_caps.is_lrr_2_5_supported = True
                                panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_SW
                                panel.drrs_caps.is_drrs_supported = True

                        if caps.t_con_based and (panel.drrs_caps.min_rr <= 24):
                            # VRR + PSR2 + 314 Bit2 = DC + Bit1 = 1 + MinRR <= 24
                            # LRR2.0
                            # Idle - No source driven RR switch. Remain in PSR2 idle mode. TCON to switch to the lowest RR.
                            # Media PB - Switch to 24Hz/48Hz. No PSR.
                            panel.lrr_caps.is_lrr_supported = True
                            panel.lrr_caps.is_lrr_2_0_supported = True
                            panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
                            panel.drrs_caps.is_drrs_supported = True
                    else:
                        if caps.source_v_total_based:
                            # VRR + PSR2 + DMRRS -> HW VRR based switch from D14+
                            panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
                            panel.lrr_caps.is_lrr_supported = True
                            panel.lrr_caps.is_lrr_2_5_supported = True
                            panel.lrr_caps.is_lrr_2_0_supported = True
                            panel.drrs_caps.is_drrs_supported = True
                        else:
                            # VRR + PSR2 + No 314h -> fixed RR not supported
                            panel.lrr_caps.is_lrr_supported = False
                            panel.lrr_caps.is_lrr_2_5_supported = False
                            panel.lrr_caps.is_lrr_2_0_supported = False
                            if psr_disabled:
                                panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
                                panel.drrs_caps.is_drrs_supported = True
                            else:
                                panel.lrr_caps.rr_switching_method = RrSwitchingMethod.UNSUPPORTED
                                panel.drrs_caps.is_drrs_supported = False
                else:
                    if caps.source_pixel_clock_based and (panel.drrs_caps.min_rr >= 30):
                        # NoVRR + PSR2 + Bit0 = 1 + MinRR >= 30
                        # LRR1.0
                        # Switch to lower RR using pixel clock when in idle/media playback.
                        panel.lrr_caps.is_lrr_supported = True
                        panel.lrr_caps.is_lrr_1_0_supported = True
                        panel.lrr_caps.rr_switching_method = RrSwitchingMethod.CLOCK
                        panel.drrs_caps.is_drrs_supported = True
            else:
                if panel.vrr_caps.is_vrr_supported and (panel.drrs_caps.min_rr <= 48):
                    # Basic Adaptive Sync panel
                    # Vtotal based RR change. No PSR.
                    panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
                    panel.drrs_caps.is_drrs_supported = True
    else:
        # Pre-Gen12: LRR1 is supported on Non-VRR + PSR2 + Multi-RR panels
        # Gen12+: if DPCD 314H is 0, LRR1 can be supported on above panel
        if panel.vrr_caps.is_vrr_supported is False:
            if __is_multi_rr(panel) and panel.psr_caps.is_psr2_supported:
                # LRR1.0
                # Switch to lower RR using pixel clock when in idle/media playback.
                panel.lrr_caps.is_lrr_supported = True
                panel.lrr_caps.is_lrr_1_0_supported = True
                panel.lrr_caps.rr_switching_method = RrSwitchingMethod.CLOCK
                panel.drrs_caps.is_drrs_supported = True
            else:
                # No LRR
                # PSR enabled if panel supports it.
                # DRRS/DMRRS available using pixel clock switching technique (if panel supports 2 RRs)
                if len(panel.rr_list) > 1:
                    panel.drrs_caps.is_drrs_supported = True
                    panel.lrr_caps.rr_switching_method = RrSwitchingMethod.CLOCK
        else:
            if panel.psr_caps.is_psr2_supported:
                if adapter.name in common.PRE_GEN_14_PLATFORMS:
                    # LRR2.0
                    # Idle - No source driven RR switch. Remain in PSR2 idle mode. TCON to switch to the lowest RR.
                    # Media PB - Switch to 24Hz/48Hz. No PSR.
                    panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
                    panel.lrr_caps.is_lrr_supported = True
                    panel.lrr_caps.is_lrr_2_0_supported = True
                    panel.drrs_caps.is_drrs_supported = True
                else:
                    # VRR + PSR2 + No 314h -> fixed RR not supported
                    panel.lrr_caps.is_lrr_supported = False
                    panel.lrr_caps.is_lrr_2_5_supported = False
                    panel.lrr_caps.is_lrr_2_0_supported = False
                    if psr_disabled:
                        panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
                        panel.drrs_caps.is_drrs_supported = True
                    else:
                        panel.lrr_caps.rr_switching_method = RrSwitchingMethod.UNSUPPORTED
                        panel.drrs_caps.is_drrs_supported = False
            else:
                # Basic Adaptive Sync panel
                # Vtotal based RR change. No PSR.
                panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
                panel.drrs_caps.is_drrs_supported = True

    panel.drrs_caps.is_dmrrs_supported = panel.drrs_caps.is_drrs_supported
    if registry.read(adapter.gfx_index, registry.RegKeys.PSR.PSR2_DRRS_ENABLE) == 0:
        panel.lrr_caps.is_lrr_supported = False


##
# @brief        Helper API to get MSO caps for given panel
# @param[in]    panel Panel
# @return       None
def __get_mso_caps(panel: Panel):
    caps = dpcd.EdpMsoCaps(panel.target_id)
    if caps.no_of_links in [2, 4]:
        panel.mso_caps.is_mso_supported = True
        panel.mso_caps.no_of_segments = caps.no_of_links


##
# @brief        Helper API to get PSR caps for given panel
# @param[in]    panel, Panel
# @return       None
def __get_psr_caps(panel: Panel):
    # Edp DPCD version
    if panel.edp_caps.edp_revision == dpcd.EdpDpcdRevision.EDP_UNKNOWN:
        return

    # Check SET_POWER_CAPABLE. This bit must have a value of 1 if PSR is supported
    if panel.edp_caps.is_set_power_capable is False:
        return

    # Get eDP supported PSR version
    psr_ver = dpcd.get_psr_version(panel.target_id)
    if psr_ver == dpcd.EdpPsrVersion.EDP_PSR_UNKNOWN:
        logging.error("\tFailed to get eDP PSR version")
        return

    # PSR1 is supported only on eDP 1.3+ panels
    if (panel.edp_caps.edp_revision >= dpcd.EdpDpcdRevision.EDP_DPCD_1_3) and (psr_ver >= dpcd.EdpPsrVersion.EDP_PSR_1):
        panel.psr_caps.is_psr_supported = True
        panel.psr_caps.psr_version = 0x1
    # Get granularity support
    psr_capability = dpcd.PsrCapability(panel.target_id)
    panel.psr_caps.setup_time = psr_capability.psr_setup_time

    # PSR2 is supported only on eDP 1.4+ panels
    if panel.edp_caps.edp_revision >= dpcd.EdpDpcdRevision.EDP_DPCD_1_4:
        if panel.psr_caps.alpm_caps and (psr_ver >= dpcd.EdpPsrVersion.EDP_PSR_2):
            panel.psr_caps.is_psr2_supported = True
            panel.psr_caps.psr_version = 0x2
    if panel.psr_caps.is_psr2_supported:
        panel.psr_caps.y_coordinate_required = psr_capability.Y_coordinate_required_for_psr2_su
        panel.psr_caps.su_granularity_supported = bool(psr_capability.psr2_su_granularity_required)
        psr_granularity = dpcd.PsrGranularity(panel.target_id)
        panel.psr_caps.su_y_granularity = psr_granularity.su_y_granularity
        psr_config = dpcd.SinkPsrConfiguration(panel.target_id)
        panel.psr_caps.early_transport_supported = bool(psr_config.su_region_early_transport_enable)


##
# @brief        Helper API to get PR caps for given panel
# @param[in]    panel, Panel
# @return       None
def __get_pr_caps(panel: Panel):
    # Get PR support
    pr_support = dpcd.PanelReplayCapsSupported(panel.target_id)
    pr_capability = dpcd.PanelReplayCaps(panel.target_id)
    pr_granularity = dpcd.PrGranularity(panel.target_id)
    panel.pr_caps.su_y_granularity = pr_granularity.su_y_granularity
    panel.pr_caps.pr_su_granularity_needed = bool(pr_capability.pr_su_granularity_needed)
    panel.pr_caps.early_transport_supported = bool(pr_support.early_transport_support)
    if panel.is_lfp is False:
        panel.pr_caps.is_pr_supported = bool(pr_support.panel_replay_support)
        return
    # Check for DPCD 0x2Eh (ALPM Caps) for Aux_wake/Aux-less support
    alpm_caps = dpcd.AlpmCaps(panel.target_id)
    panel.psr_caps.alpm_caps = alpm_caps.value
    panel.pr_caps.aux_less_alpm = bool(alpm_caps.aux_less_alpm_cap)
    # Check SET_POWER_CAPABLE
    # This bit must have a value of 1 if PR is supported
    if panel.edp_caps.is_set_power_capable != 1:
        return
    # PR is supported only on eDP 1.5+ panels
    if (panel.edp_caps.edp_revision >= dpcd.EdpDpcdRevision.EDP_DPCD_1_5) and pr_support.panel_replay_support:
        # BIT6 - MSA_TIMING_PAR_IGNORED should be set.
        msa_timing = dpcd.DownStreamPortCount(panel.target_id)
        # Adaptive Sync SDP support is mandatory for EDP PR
        as_sdp_caps = dpcd.AdaptiveSyncCapability(panel.target_id)
        if panel.psr_caps.alpm_caps and msa_timing.msa_timing_par_ignored and as_sdp_caps.adaptive_sync_sdp_supported:
            panel.pr_caps.is_pr_supported = True


##
# @brief        Helper API to get VDSC caps for given panel
# @param[in]    panel Panel
# @return       None
def __get_vdsc_caps(panel: Panel):
    if panel.port in ["MIPI_A", "MIPI_C"]:
        gfx_vbt = Vbt(panel.gfx_index)
        panel_index = gfx_vbt.block_40.PanelType if panel.port == "MIPI_A" else gfx_vbt.block_40.PanelType2
        panel.vdsc_caps.is_vdsc_supported = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[
                                                panel_index].CompressionEnable == 1
    else:
        caps = dpcd.DscSupport(panel.target_id)
        panel.vdsc_caps.is_vdsc_supported = caps.dsc_support == 1


##
# @brief        Helper API to get Pipe Joiner and Tiled caps for given panel
# @param[in]    panel Panel
# @return       None
def __get_pipe_joiner_tiled_caps(panel: Panel):
    panel.pipe_joiner_tiled_caps.is_pipe_joiner_require, _ = DisplayClock.is_pipe_joiner_required(panel.gfx_index,
                                                                                                  panel.port)
    panel.pipe_joiner_tiled_caps.is_tiled_panel = True if panel.target_id & 0x400000 else False
    panel.pipe_joiner_tiled_caps.master_pipe = panel.pipe
    logging.debug("Master pipe= PIPE_{}".format(panel.pipe_joiner_tiled_caps.master_pipe))
    if panel.pipe_joiner_tiled_caps.is_pipe_joiner_require:
        panel.pipe_joiner_tiled_caps.slave_pipe = chr(ord(panel.pipe) + 1)
        logging.debug("Slave pipe= PIPE_{}".format(panel.pipe_joiner_tiled_caps.slave_pipe))
    if panel.pipe_joiner_tiled_caps.is_tiled_panel:
        master_transcoder = ord(panel.pipe_joiner_tiled_caps.master_pipe) - 64
        for adapter in adapters.values():
            for _panel in adapter.panels.values():
                if _panel.port == panel.port:
                    continue
                transcoder_list = ["TRANSCODER_A", "TRANSCODER_B", "TRANSCODER_C", "TRANSCODER_D"]
                driver_interface = DriverInterface()
                for index in range(len(transcoder_list)):
                    trans_ddi_func_ctl2_offset = adapter.regs.get_trans_ddi_ctl2_offsets(transcoder_list[index])
                    data = driver_interface.mmio_read(trans_ddi_func_ctl2_offset.FuncCtrl2Reg, adapter.gfx_index)
                    trans_ddi_value = adapter.regs.get_trans_ddi_ctl2_info(transcoder_list[index],
                                                                           TransDDiCtl2OffsetsValues(FuncCtrl2Reg=data))
                    if trans_ddi_value.PortSyncModeEnable == 1:
                        if trans_ddi_value.PortSyncModeMasterSelect == master_transcoder:
                            panel.pipe_joiner_tiled_caps.slave_pipe = _panel.pipe = chr(int(index) + 65)
                            logging.info("Slave pipe using new method= PIPE_{}".format(chr(int(index) + 65)))
                        break


##
# @brief        Helper API to get VRR caps for given panel
# @param[in]    panel Panel
# @return       None
def __get_vrr_caps(panel: Panel):
    display_config_ = display_config.DisplayConfiguration()
    adapter = adapters[panel.gfx_index]
    if panel.is_lfp:
        gfx_vbt = Vbt(panel.gfx_index)
        if gfx_vbt.version >= 233:
            panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
            logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")
            if (gfx_vbt.block_44.VRR[0] & (1 << panel_index)) >> panel_index == 0:
                panel.vrr_caps.is_vrr_enabled_in_vbt = False
            else:
                panel.vrr_caps.is_vrr_enabled_in_vbt = True

    edid_flag, edid_data, _ = driver_escape.get_edid_data(panel.display_info.DisplayAndAdapterInfo)
    if not edid_flag:
        status, reboot_required = display_essential.restart_gfx_driver()
        edid_flag, edid_data, _ = driver_escape.get_edid_data(panel.display_info.DisplayAndAdapterInfo)
        if not edid_flag:
            logging.error(f"Failed to get EDID data after display driver restart for target_id : {panel.target_id}")
            assert edid_flag, "Failed to get EDID data"
        assert edid_data

    min_rr = 0
    max_rr = 0

    # From Gen16 onwards VRR CTL will be enabled for all Non VRR panels
    if adapter.name not in PRE_GEN_16_PLATFORMS:
        panel.vrr_caps.is_always_vrr_mode_on_non_vrr_panel = True

    # eDP/DP panel
    if not (panel.hdmi_2_1_caps.is_hdmi_2_1_pcon or panel.hdmi_2_1_caps.is_hdmi_2_1_native):
        # Get DOWN_STREAM_PORT_COUNT value from DPCD
        # Make sure MSA_TIMING_PAR_IGNORED is enabled in DPCD
        down_stream_port_count = dpcd.DownStreamPortCount(panel.target_id)
        if down_stream_port_count.msa_timing_par_ignored != 0x1:
            logging.debug("\tMsaTimingParIgnored is NOT enabled in DPCD for {0} at 0x00007".format(panel.port))
            # in case of DP and HDMI 2.1 PCON, MSA_TIMING_PAR_IGNORED can be present in extended address 0x2200h-0x22FFh
            if panel.is_lfp:
                return
            # Checking MsaTimingParIgnored in Extended DPCD range
            # Check for Extended receiver cap field
            extended_field_present = dpcd.ExtendedRxCapFieldPresent(panel.target_id)  # address 0x0E
            if extended_field_present.extended_receiver_capability_field_present != 0x1:
                logging.debug("Extended Receiver Cap Not present")
                return
            extended_down_stream_port_count = dpcd.ExtendedDownStreamPortCount(panel.target_id)
            if extended_down_stream_port_count.msa_timing_par_ignored != 0x1:
                logging.debug("\tMsaTimingParIgnored is NOT enabled in DPCD for {0} at 0x02207".format(panel.port))
                return

        # Make sure IsContinuousFreqSupported is true in EDID
        if edid_data[24] & 0x1 != 0x1:
            logging.debug("\tIsContinuousFreqSupported is NOT enabled in EDID for {0}".format(panel.port))
            if panel.is_lfp is False:
                panel.vrr_caps.is_vrr_supported = False
                return

        if panel.pnp_id in NEGATIVE_VRR_PNP_ID:
            logging.info(f"PNP ID is matching with MTK panels with NO VRR support, Updated VRR= False")
            panel.vrr_caps.is_vrr_supported = False
            return

        index = 54  # start of 1st 18 byte descriptor
        while index < 126:
            if edid_data[index + 3] == 0xFD:  # 0xFD is display range limits block
                vertical_rate_offset = edid_data[index + 4] & 0x3
                if 0 == vertical_rate_offset:
                    min_rr = edid_data[index + 5]
                    max_rr = edid_data[index + 6]
                elif 2 == vertical_rate_offset:
                    min_rr = edid_data[index + 5]
                    max_rr = edid_data[index + 6] + 255
                elif 3 == vertical_rate_offset:
                    min_rr = edid_data[index + 5] + 255
                    max_rr = edid_data[index + 6] + 255
                break
            index += 18
        # check for extension block present in EDID or not for DID2.0 panel.
        index = 126
        if edid_data[index] > 0:
            logging.debug("Extension block present in EDID, checking for extension block")
            number_of_extension_block = edid_data[index]  # number of extension block present at 126 byte in block 0
            index += 2  # increase index with 2 value to check start value of next block
            while number_of_extension_block > 0:
                # check if block is EDID block or not using first byte of block.
                if edid_data[index] != 0x70:  # EDID block First byte is 0x70
                    number_of_extension_block -= 1
                    index += 128
                    continue
                # checking for DID version and confirm it is DID 2.0
                if edid_data[index + 1] == 0x20:
                    temp_index = index + 5  # add header byte
                    while temp_index < index + 126:
                        if edid_data[temp_index] == 0x25:  # 0x25 is Dynamic Video Timing Range Limits Data Block
                            min_rr = edid_data[temp_index + 9]
                            max_rr = (edid_data[temp_index + 11] << 8 | edid_data[temp_index + 10]) & 0x3FF
                            if edid_data[temp_index + 11] & 0x80 is False:
                                logging.debug(
                                    "\tIsContinuousFreqSupported is NOT enabled in EDID for {0}".format(panel.port))
                                return
                            break
                        # 3 is header size of block and last byte in head represent number of payload in block
                        number_of_byte = edid_data[temp_index + 2] + 3

                        temp_index += number_of_byte  # checking for next value
                break
        if min_rr == 0 or max_rr == 0 or max_rr <= min_rr:
            logging.debug(
                "\tInvalid Refresh Rates found for {0}. MinRR= {1}, MaxRR= {2}".format(panel.port, min_rr, max_rr))
            return
    # DP->HDMI2.1 (PCON) or Native HDMI 2.1 use case
    else:
        hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
        if hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(panel.gfx_index, panel.port) is False:
            logging.debug("No VSDB block present in EDID")
            return
        min_rr = hf_vsdb_parser.vrr_min
        max_rr = hf_vsdb_parser.vrr_max
        # HDMI 2.1 panel can support Max RR value as Zero(0) in that case max RR of panel is vrr max value
        if max_rr == 0:
            logging.info("MaxRR= 0 for {0}, updating MaxRR with Current Mode RR".format(panel.port))
            current_mode = display_config_.get_current_mode(panel.target_id)
            max_rr = current_mode.refreshRate
        if min_rr == 0 or max_rr <= min_rr:
            logging.debug(
                "\tInvalid Refresh Rates found for {0}. MinRR= {1}, MaxRR= {2}".format(panel.port, min_rr, max_rr))
            return

    panel.vrr_caps.is_vrr_supported = True
    panel.vrr_caps.is_dc_balancing_enabled = True

    # always in vrr mode for VRR/ NonVRR DP and HDMI 2.1 panel for Gen13+ platform.
    if adapter.name not in PRE_GEN_13_PLATFORMS and panel.is_lfp is False:
        panel.vrr_caps.is_always_vrr_mode = True
        panel.vrr_caps.is_always_vrr_mode_on_non_vrr_panel = False

    # From Gen14 + ( MTL ) onwards VRR supported EDp panel is also in always VRR mode.
    if panel.vrr_caps.is_vrr_supported and adapter.name not in PRE_GEN_14_PLATFORMS and panel.is_lfp is True:
        panel.vrr_caps.is_always_vrr_mode = True

    panel.vrr_caps.min_rr = min_rr
    panel.vrr_caps.max_rr = max_rr

    panel.vrr_caps.vrr_max_rr = max_rr
    # with recent driver implementation PR:89743, min RR should not be less than 20 for vrr
    panel.vrr_caps.vrr_min_rr = max(min_rr, 20)

    # updating profile min and max rr based on recommended profile
    panel.vrr_caps.vrr_profile_min_rr = max(panel.vrr_caps.vrr_max_rr//2, panel.vrr_caps.vrr_min_rr)
    panel.vrr_caps.vrr_profile_max_rr = panel.vrr_caps.vrr_max_rr
    panel.vrr_caps.vrr_profile_sfdit = int((1.0 * 1000 * 1000) / panel.vrr_caps.vrr_profile_max_rr)
    panel.vrr_caps.vrr_profile_sfddt = int((1.0 * 1000 * 1000) / panel.vrr_caps.vrr_profile_max_rr)

    # VRR SDP support is applicable for DP->HDMI2.1 via DP SST
    if not panel.is_lfp and not panel.hdmi_2_1_caps.is_hdmi_2_1_native:
        mst_mode = dpcd.is_mst_mode(panel.target_id)

        # DPCD read failure(s)
        if mst_mode is None:
            logging.error("\tEncountered DPCD read failure(s) while getting MST/SST mode for {0}".format(panel.port))
            assert False, "Failed to read DPCD"

        # VRR SDP not supported in DP MST
        if mst_mode is True:
            logging.debug("\tMST mode is enabled in {0}, VRR SDP not supported in DP MST".format(panel.port))
            return

        # VRR SDP supports only in DP SST
        # Get DOWN_STREAM_PORT_PRESENT and qualify that down stream hdmi is present
        down_stream_port_present = dpcd.DownStreamPortPresent(panel.target_id)  # address 0x5
        if down_stream_port_present.dfp_present == 0x1 \
                and down_stream_port_present.detailed_cap_info_available == 0x1 \
                and down_stream_port_present.dfp_type == dpcd.DpBaseDfpType.DP_DWN_STREAM_PORT_HDMI:
            dp_down_stream_portx_bpc_caps = dpcd.DpDownStreamPortxBpcCaps(panel.target_id)  # address 0x82
            # Get ADAPTIVE_SYNC_CAPABILITY and check SDP support
            adaptive_sync_capability = dpcd.AdaptiveSyncCapability(panel.target_id)  # address 0x2214
            sdp_one_line_earlier = dpcd.AdaptiveSyncSdpTransmissionTimingConfig(panel.target_id)  # address 0x11B
            if dp_down_stream_portx_bpc_caps.pcon_source_control_mode_support != 0x0 and \
                    adaptive_sync_capability.adaptive_sync_sdp_supported == 0x1:
                panel.vrr_caps.is_vrr_sdp_supported = True


##
# @brief        Helper API to get is_HDMI_2_1 panel
# @param[in]    panel, Panel
def __get_hdmi_2_1_caps(panel: Panel):
    pcon_source_control_mode = None
    adapter = adapters[panel.gfx_index]
    hf_vsdb_block_present = False
    if adapter.name in common.PRE_GEN_13_PLATFORMS:
        return
    hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
    if hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(panel.gfx_index, panel.port) is True:
        hf_vsdb_block_present = True
    # Check for PCON supported in DPCD
    if panel.panel_type == "DP":
        down_stream_port_present = dpcd.DownStreamPortPresent(panel.target_id)  # address 0x5
        if down_stream_port_present.dfp_present == 0x1 \
                and down_stream_port_present.detailed_cap_info_available == 0x1 \
                and down_stream_port_present.dfp_type == dpcd.DpBaseDfpType.DP_DWN_STREAM_PORT_HDMI:
            dp_down_stream_portx_bpc_caps = dpcd.DpDownStreamPortxBpcCaps(panel.target_id)  # address 0x82
            pcon_source_control_mode = dp_down_stream_portx_bpc_caps.pcon_source_control_mode_support
        # check for FRL enable or not in EDID and PCON source control mode in DPCD
        panel.hdmi_2_1_caps.is_hdmi_2_1_pcon = hf_vsdb_block_present and pcon_source_control_mode
    if panel.panel_type == "HDMI":
        # check for FRL enable or not in EDID
        panel.hdmi_2_1_caps.is_hdmi_2_1_native = hf_vsdb_block_present
        # update if panel is tmds or frl mode.
        if panel.hdmi_2_1_caps.is_hdmi_2_1_native is True:
            # if panel is not frl and native then it will be tmds panel.
            panel.hdmi_2_1_caps.is_hdmi_2_1_tmds = not hf_vsdb_parser.is_frl_enable


##
# @brief        Helper API to get MIPI Video mode caps for given panel
# @param[in]    panel, Panel
def __get_mipi_video_mode_caps(panel: Panel):
    gfx_vbt = Vbt(panel.gfx_index)
    _mipi_helper = mipi_helper.MipiHelper(common.PLATFORM_NAME)
    # panel indexes
    panel_index = gfx_vbt.block_40.PanelType if panel.port == "MIPI_A" else gfx_vbt.block_40.PanelType2
    logging.debug("For port:{0}, panel index:{1}".format(panel.port, panel_index))

    panel.mipi_caps.is_video_mode_supported = _mipi_helper.get_mode_of_operation(panel_index) == 0
    panel.mipi_caps.is_dual_link = _mipi_helper.dual_link
    panel.mipi_caps.is_port_sync_enable = _mipi_helper.dual_LFP_MIPI_port_sync


##
# @brief        Helper API to get IDT caps for given panel
# @param[in]    panel, Panel
# @return       None
def __get_idt_caps(panel: Panel):
    caps = dpcd.LrrUbrrCaps(panel.target_id)

    if caps.ubzrr_supported:
        panel.idt_caps.is_ubzrr_supported = True

    if caps.ublrr_supported:
        panel.idt_caps.is_ublrr_supported = True

    if caps.alrr_supported:
        panel.idt_caps.is_alrr_supported = True

    if panel.hdr_caps.brightness_ctrl_in_nits_level_using_Aux_supported and \
            panel.hdr_caps.brightness_optimization_supported and panel.hdr_caps.is_aux_only_brightness:
        panel.idt_caps.is_pixoptix_supported = True


##
# @brief        Helper API to initialize panel capabilities
# @param[in] adapter Adapter
# @param[in]    panel Panel
# @param[in]    monitor_id [optional] Boolean
# @return       None
def __init_panel_caps(adapter: Adapter, panel: Panel, monitor_id=False, pruned_mode_list=True):
    display_config_ = display_config.DisplayConfiguration()

    # Add display_info, target_id, transcoder, pipe
    enumerated_displays = display_config_.get_enumerated_display_info()
    assert enumerated_displays

    for display_index in range(enumerated_displays.Count):
        display_info = enumerated_displays.ConnectedDisplays[display_index]
        port = cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
        if panel.port == port and panel.gfx_index == display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
            panel.display_info = copy.deepcopy(display_info)
            panel.target_id = display_info.TargetID
            panel.source_id = display_info.DisplayAndAdapterInfo.SourceID
            panel.is_active = True
            break

    if monitor_id:
        target_config = cfg_struct.DisplayConfig()
        target_config.topology = enum.SINGLE
        target_config.numberOfDisplays = 1
        target_config.displayPathInfo[0].targetId = panel.target_id
        target_config.displayPathInfo[0].displayAndAdapterInfo = panel.display_info.DisplayAndAdapterInfo

        current_config = display_config_.get_current_display_configuration()
        if target_config.equals(current_config) is False:
            display_config_.set_display_configuration(target_config)
            enumerated_displays = display_config_.get_enumerated_display_info()
            assert enumerated_displays

            current_config = display_config_.get_current_display_configuration()
            if target_config.equals(current_config) is False:
                logging.warning(
                    "Failed to set display configuration to {0}".format(target_config.to_string(enumerated_displays)))
                return False

        monitors = app_controls.get_enumerated_display_monitors()
        for m in monitors:
            monitor_info = app_controls.get_monitor_info(m[0])
            # Search for active panel
            if monitor_info.dwFlags == 1:
                panel.monitor_id = m[0]

    else:
        display_base_obj = DisplayBase(panel.port, gfx_index=panel.gfx_index)
        trans, pipe = display_base_obj.get_transcoder_and_pipe(panel.port, gfx_index=panel.gfx_index)

        # Get panel transcoder
        if trans == 0:
            panel.transcoder = 'EDP'
        elif trans == 5:
            panel.transcoder = 'DSI0'
        elif trans == 6:
            panel.transcoder = 'DSI1'
        else:
            panel.transcoder = chr(int(trans) + 64)

        panel.transcoder_type = TranscoderType(trans) if trans >= 0 else TranscoderType.TRANSCODER_NULL
        panel.pipe = chr(int(pipe) + 65)
        panel.pipe_type = PipeType(pipe) if pipe >= 0 else PipeType.PIPE_NULL
        panel.panel_type = panel.port.split("_")[0]

        rr_list = set()
        pixel_clocks = set()
        mode_with_max_rr = None

        all_supported_modes = display_config_.get_all_supported_modes([panel.display_info.DisplayAndAdapterInfo],
                                                                      pruned_mode_list=pruned_mode_list)
        for _, modes in all_supported_modes.items():
            for mode in modes:
                if mode_with_max_rr is None:
                    mode_with_max_rr = mode
                if mode.refreshRate > mode_with_max_rr.refreshRate:
                    mode_with_max_rr = mode
                rr_list.add(mode.refreshRate)
                pixel_clocks.add(mode.pixelClock_Hz)

        panel.rr_list = list(rr_list)
        panel.rr_list.sort()
        panel.max_rr = max(rr_list)
        panel.min_rr = min(rr_list)

        panel.pixel_clocks = list(pixel_clocks)
        panel.native_mode = mode_with_max_rr
        panel.current_mode = display_config_.get_current_mode(panel.target_id)

        max_pixel_clock = max(pixel_clocks)
        display_timings = display_config_.get_display_timings(panel.display_info.DisplayAndAdapterInfo)
        panel.actual_max_rr = round(max_pixel_clock / (display_timings.hTotal * display_timings.vTotal), 3)
        min_pixel_clock = min(pixel_clocks)
        panel.actual_min_rr = round(min_pixel_clock / (display_timings.hTotal * display_timings.vTotal), 3)

        try:
            frame_update = subprocess.Popen(__FRAME_UPDATE_PATH)
            time.sleep(3)
        except Exception as e:
            logging.error(e)
            frame_update = None

        if panel.panel_type == "MIPI":
            panel_data_entry = Vbt(panel.gfx_index).block_42.FlatPanelDataStructureEntry[0]
            mfg_name = panel_data_entry.IdMfgName.to_bytes(2, "little").hex()
            product = panel_data_entry.IdProductCode.to_bytes(2, "little").hex()
            sr_no = panel_data_entry.IDSerialNumber.to_bytes(4, "little").hex()
            week = hex(panel_data_entry.WeekOfMfg).lstrip("0x")
            year = hex(panel_data_entry.YearOfMfg).lstrip("0x")
            # handle specific cases for VBT values (week/year)
            #   "f"/"2" -> "0f"/"02", "" -> "00"
            if panel_data_entry.WeekOfMfg == 0:
                week = "00"
            elif panel_data_entry.WeekOfMfg < 16:
                week = "0" + week
            if panel_data_entry.YearOfMfg == 0:
                year = "00"
            elif panel_data_entry.YearOfMfg < 16:
                year = "0" + year
            panel.pnp_id = mfg_name + product + sr_no + week + year
            if panel.pnp_id is None:
                gdhm.report_bug(
                    title=f"[PowerCons][DUT] PNP ID is None for {panel.port}",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_POWERCONS,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )

            __get_mipi_video_mode_caps(panel)
            __get_vdsc_caps(panel)
        else:
            # Todo: control return value for EDID. Currently, API is returning data as it is.
            edid_flag, edid_data, _ = driver_escape.get_edid_data(panel.target_id)
            if not edid_flag:
                logging.error(f"Failed to get EDID data for target_id : {panel.target_id}")
                assert edid_flag, "Failed to get EDID data"
            bpc_info = edid_data[20] >> 4  # BPC information from first EDID block
            panel.bpc = ((bpc_info - 6) * 2) if 0x9 <= bpc_info <= 0xE else 0

            if panel.panel_type == "DP":
                panel.pnp_id = "".join(format(i, '02x') for i in edid_data[8:18])
                if panel.pnp_id is None:
                    gdhm.report_bug(
                        title=f"[PowerCons][DUT] PNP ID is None for {panel.port}",
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
            if panel.panel_type in ['DP']:
                panel.dpcd_version = dpcd.get(panel.target_id, dpcd.Offsets.DPCD_REV)
                panel.link_rate = dpcd.get_link_rate(panel.target_id, True)
                panel.max_lane_count = dpcd.MaxLaneCount(panel.target_id).max_lane_count
                __get_edp_caps(panel)
                __get_mso_caps(panel)
                __get_luminance_data(panel, edid_data) # get luminance data
                __get_hdr_static_metadata(panel)  # to get HDR support and additional data
                __get_pr_caps(panel)  # get panel replay caps for EDP/DP
                __get_vesa_caps(panel)
                if panel.is_lfp is False:
                    __get_hdmi_2_1_caps(panel)  # to get hdmi 2_1 caps, fill up hdmi caps to use in VRR caps
                __get_rr_switching_caps(panel)  # Get PSR/DRRS/DMRRS/LRR and VRR caps
                __get_vdsc_caps(panel)
                __get_pipe_joiner_tiled_caps(panel)
                if panel.is_lfp:
                    __get_idt_caps(panel)
            # update VRR caps in case of HDMI 2.1 Native panel
            if panel.panel_type in ['HDMI']:
                __get_hdmi_2_1_caps(panel)  # to get hdmi 2_1 caps, fill up hdmi caps to use in VRR caps
                __get_vrr_caps(panel)
                __get_pipe_joiner_tiled_caps(panel)

        try:
            if frame_update is not None:
                frame_update.kill()
        except Exception as e:
            logging.error(e)


##
# @brief        Helper API to plug given panel on given adapter
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @return       status, Boolean, True if plug operations is successful, False otherwise
def plug_wrapper(adapter: Adapter, panel: Panel):
    logging.info(
        "Plugging {0}{1} on {2}".format(
            panel.port, "" if panel.description is None else "(" + panel.description + ")", adapter.name))
    driver_interface = DriverInterface()
    if driver_interface.simulate_plug(
            adapter.adapter_info, panel.port, panel.edid_path, panel.dpcd_path, False, panel.port_type,
            panel.is_lfp) is False:
        return False

    time.sleep(10)
    enumerated_displays = display_config.DisplayConfiguration().get_enumerated_display_info()
    assert enumerated_displays

    if display_config.is_display_attached(enumerated_displays, panel.port, panel.gfx_index) is False:
        return False

    logging.info("\tPASS: Plugged {0} successfully".format(panel.port))
    return True


##
# @brief        Helper API to unplug given panel from given adapter
# @param[in]    adapter, Adapter
# @param[in]    panel, Panel
# @return       status, Boolean, True if unplug operation is successful, False otherwise
def __unplug_wrapper(adapter: Adapter, panel: Panel):
    if panel.is_lfp:
        return True

    enumerated_displays = display_config.DisplayConfiguration().get_enumerated_display_info()
    assert enumerated_displays

    if display_config.is_display_attached(enumerated_displays, panel.port, panel.gfx_index) is False:
        return True

    logging.info(
        "UnPlugging {0}{1} on {2}".format(
            panel.port, "" if panel.description is None else "(" + panel.description + ")", adapter.name))
    driver_interface = DriverInterface()
    if driver_interface.simulate_unplug(adapter.adapter_info, panel.port, False, panel.port_type) is False:
        logging.warning("\tUnable to unplug {0}".format(panel.port))
        return False

    time.sleep(10)
    enumerated_displays = display_config.DisplayConfiguration().get_enumerated_display_info()
    assert enumerated_displays

    if display_config.is_display_attached(enumerated_displays, panel.port, panel.gfx_index):
        logging.warning("\tUnable to unplug {0}".format(panel.port))
        return False

    logging.info("\tPASS: UnPlugged {0} successfully".format(panel.port))
    return True


##
# @brief        Helper API to get display config object based on command line parameters
# @param[in]    cmd_line_params, list
# @return       topology and adapter_info_list based on command line parameters
def __get_display_config(cmd_line_params):
    global adapters

    topology = eval("enum.%s" % cmd_line_params[0]['CONFIG'])
    display_and_adapter_info_list = []
    display_list = cmd_parser.get_sorted_display_list(cmd_line_params)
    for display in display_list:
        gfx_index = list(display)[0]
        port = display[gfx_index]
        assert gfx_index in adapters.keys(), "Invalid adapter index: {0}".format(gfx_index)
        assert port in adapters[gfx_index].panels.keys(), "Invalid panel for {0}: {1}".format(gfx_index, port)
        display_and_adapter_info_list.append(adapters[gfx_index].panels[port].display_info.DisplayAndAdapterInfo)

    assert display_and_adapter_info_list
    return topology, display_and_adapter_info_list


##
# @brief        Helper API to get Windows OS version
# @return       version of the windows if found, else UNKNOWN
def __get_win_os_version():
    output = os.popen('ver.exe').read().replace('\n', '')

    build_branch = dict()
    build_branch[WinOsVersion.WIN_NICKEL] = [10022367, 10099999]
    build_branch[WinOsVersion.WIN_COBALT] = [10021262, 10022367]
    build_branch[WinOsVersion.WIN_21H2] = [10019044, 10021262]
    build_branch[WinOsVersion.WIN_21H1] = [10019043, 10019044]
    build_branch[WinOsVersion.WIN_20H2] = [10019042, 10019043]
    build_branch[WinOsVersion.WIN_20H1] = [10019041, 10019042]
    build_branch[WinOsVersion.WIN_VIBRANIUM] = [10018849, 10099999]
    build_branch[WinOsVersion.WIN_19H1] = [10018282, 10018849]
    build_branch[WinOsVersion.WIN_RS5] = [10017627, 10018282]
    build_branch[WinOsVersion.WIN_RS4] = [10017134, 10017627]
    build_branch[WinOsVersion.WIN_RS3] = [10016299, 10017134]
    build_branch[WinOsVersion.WIN_RS2] = [10014870, 10016299]
    build_branch[WinOsVersion.WIN_RS1] = [10014310, 10014870]
    build_branch[WinOsVersion.WIN_TH2] = [10010586, 10014310]
    build_branch[WinOsVersion.WIN_TH1] = [10010240, 10010586]

    # Regular expression for grouping major, minor and build from build number
    os_version_pattern = r"^[a-zA-Z []+(?P<major>\d{2}).(?P<minor>\d).(?P<build>\d{5}).[0-9.]+\]$"
    ver_match = re.match(os_version_pattern, output)
    if ver_match is not None:
        # making build number 12.3.45678 as one number 12345678
        result = int(ver_match.group('build'))
        result += int(ver_match.group('minor')) * 100000
        result += int(ver_match.group('major')) * 1000000

        for key, value in build_branch.items():
            if value[0] <= result < value[1]:
                return key
    return WinOsVersion.WIN_UNKNOWN


WIN_OS_VERSION = __get_win_os_version()


##
# @brief        Get the cpu stepping
# @return       Stepping of the CPU
def __get_cpu_stepping():
    output = platform.processor()
    std_out = re.compile(r'[\r\n]').sub(" ", output)
    # search for the numbers after the match of "Stepping "
    match_output = re.match(r".*Stepping (?P<Stepping>[0-9]+)", std_out)
    if match_output is None:
        logging.error(f"FAILED to get info for CPU Stepping. Output= {output}")
        return None
    return match_output.group("Stepping")


##
# @brief        Exposed API to prepare DUT for testing
#               1. Plug displays given in command line.
#               2. Set display configuration given in command line.
#               3. Initialize panel capabilities for all connected panels.
#               4. Set the native mode for each panel.
#               5. [Optional] Set power source
# @param[in]    power_source
# @param[in]    pruned_mode_list bool, Optional flag to specify pruning mode list.
#                       False: Query all supported mode list.
#                       True: Pruning all supported mode list less than 10x7
# @param[in]    disable_psr_during_caps bool, Optional flag to specify disable psr
# @return       None
def prepare(power_source=None, pruned_mode_list=True) -> None:
    display_config_ = display_config.DisplayConfiguration()
    custom_tags = [custom_tag.upper() for custom_tag in sys.argv if custom_tag.startswith("-") and
                   cmd_parser.display_flag_pattern.match(custom_tag.upper()) is None and
                   custom_tag.upper() not in ["-CONFIG", "-LOGLEVEL", "-LFP_NONE"] and
                   not custom_tag.upper().startswith("-GFX_")]

    cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=custom_tags)

    # Handle multi-adapter scenario
    if not isinstance(cmd_line_param, list):
        cmd_line_param = [cmd_line_param]

    # Workaround for parse_cmdline and get_sorted_display_list
    # if EDP_A or DP_B_PLUS is present in command line then
    # parse_cmdline() API will give dict as {'EDP_A': {}, 'DP_B_PLUS': {}} - based on key present in command line
    # and
    # get_sorted_display_list() API will give list as ['DP_A', 'DP_B'] - based on connector_port
    # Not updating the cmd_parser.py as impact is huge
    index = 0
    for cmd in cmd_line_param:
        temp_cmd = copy.deepcopy(cmd)
        for display_port, display_info in cmd.items():
            if isinstance(display_info, dict) and 'connector_port' in display_info.keys():
                if display_info['connector_port'] != display_port:
                    temp_cmd[display_info['connector_port']] = cmd[display_port]
                    del temp_cmd[display_port]

        cmd_line_param[index] = temp_cmd
        index += 1

    html.step_start("Plug requested displays and set display configuration")
    # Plug required displays
    for adapter in adapters.values():
        # Add panels from command line to 'adapter'
        __get_panels(adapter, cmd_line_param)

        enumerated_displays = display_config_.get_enumerated_display_info()
        assert enumerated_displays
        for panel in adapter.panels.values():
            is_display_attached = display_config.is_display_attached(enumerated_displays, panel.port, panel.gfx_index)
            if is_display_attached:
                # work around to plug display only for discrete platform + external panel even panel comes as attached
                if adapter.name in ["DG1", "DG2", "ELG"] and not panel.is_lfp:
                    logging.info("Workaround for discrete platform, plug panel even its enumerated ")
                    assert display_utility.plug(port=panel.port, edid=panel.edid_path, dpcd=panel.dpcd_path,
                                                is_low_power=False, is_lfp= False, gfx_index=adapter.gfx_index), \
                        f"Failed to plug {panel.port} on {adapter.name}"
                    adapter.panels[panel.port] = panel
                    __init_panel_caps(adapter, panel, monitor_id=True, pruned_mode_list=pruned_mode_list)
                else:
                    adapter.panels[panel.port] = panel
                    __init_panel_caps(adapter, panel, monitor_id=True, pruned_mode_list=pruned_mode_list)
                    __init_vbt_data(adapter, panel)
            elif is_display_attached is False and "TILED" not in sys.argv:
                assert not panel.is_lfp, f"Required LFP panel {panel.port} is not attached to the system"
                assert plug_wrapper(adapter, panel), f"Failed to plug {panel.port} on {adapter.name}"
                adapter.panels[panel.port] = panel
                __init_panel_caps(adapter, panel, monitor_id=True, pruned_mode_list=pruned_mode_list)

    # Set required display configuration
    enumerated_displays = display_config_.get_enumerated_display_info()
    assert enumerated_displays

    if "TILED" not in sys.argv:
        topology, display_list = __get_display_config(cmd_line_param)
        target_config = cfg_struct.DisplayConfig()
        target_config.topology = topology
        target_config.numberOfDisplays = len(display_list)
        path = 0
        for display in display_list:
            target_config.displayPathInfo[path].targetId = display.TargetID
            target_config.displayPathInfo[path].displayAndAdapterInfo = display
            path += 1

        logging.info("Setting display configuration {0}".format(target_config.to_string(enumerated_displays)))
        current_config = display_config_.get_current_display_configuration()
        if target_config.equals(current_config) is False:
            display_config_.set_display_configuration(target_config)

            enumerated_displays = display_config_.get_enumerated_display_info()
            assert enumerated_displays

            current_config = display_config_.get_current_display_configuration()
            if target_config.equals(current_config) is False:
                raise Exception(
                    "Failed to set display configuration to {0}".format(target_config.to_string(enumerated_displays)))
            logging.info("\tPASS: Successfully applied display configuration")
        else:
            logging.info("\tPASS: Current Configuration is {0}".format(current_config.to_string(enumerated_displays)))

    cpu_stepping_str = __get_cpu_stepping()
    if cpu_stepping_str is None:
        raise Exception("Failed to get cpu stepping")

    for adapter in adapters.values():
        logging.info(f"Active panels on {adapter.name}")
        for panel in adapter.panels.values():
            if display_config.is_display_attached(enumerated_displays, panel.port, panel.gfx_index):
                __init_panel_caps(adapter, panel, pruned_mode_list=pruned_mode_list)
                logging.info("\t{0}".format(panel))
        adapter.cpu_stepping = int(cpu_stepping_str)

    # In clone mode, we can only apply common mode supported by both the panels.
    # But display config APIs do not care for this and return the full list of supported mode by the display
    # (and not by the full topology). This is causing failures while trying to apply unsupported modes.
    # Currently there is no impact by skipping this step for CLONE. This can be updated based on requirement.
    if "TILED" not in sys.argv and topology != enum.CLONE:
        for adapter in adapters.values():
            refresh_caps = False
            for panel in adapter.panels.values():
                current_mode = display_config_.get_current_mode(panel.target_id)
                if current_mode == panel.native_mode:
                    # There can be two modes with max RR with different pixel clocks. DisplayMode __eq__ does not
                    # compare pixel clocks. Override the native_mode with current_mode for such cases.
                    panel.native_mode = current_mode
                    continue
                refresh_caps = True
                if display_config_.set_display_mode([panel.native_mode], False) is False:
                    assert False, "Failed to set native display mode (Test Issue)"
                logging.info("\tSuccessfully applied native mode")
            if refresh_caps:
                refresh_panel_caps(adapter)

    html.step_end()
    if power_source is not None:
        if __display_power.enable_disable_simulated_battery(True) is False:
            raise Exception("Failed to enable SimulatedBattery")

        if not __display_power.set_current_powerline_status(power_source):
            raise Exception(f"Failed to switch power source to {power_source.name}")


##
# @brief        Exposed API to reset DUT after testing
# @return       None
@html.step("Unplug simulated displays after test")
def reset() -> None:
    for adapter in adapters.values():
        for panel in adapter.panels.values():
            __unplug_wrapper(adapter, panel)
    logging.info("\tUnplugged all the external displays")

    if __display_power.is_simulated_battery_enabled():
        logging.info("Disabling simulated battery")
        if __display_power.enable_disable_simulated_battery(False):
            logging.info("\tDisabled simulated battery successfully")


##
# @brief        Exposed API to refresh the panel capabilities
# @param[in]    adapter Adapter
# @return       None
def refresh_panel_caps(adapter: Adapter) -> None:
    for port, panel in adapter.panels.items():
        if display_config.is_display_active(panel.port, panel.gfx_index):
            __init_panel_caps(adapter, panel)
        else:
            panel.is_active = False


##
# @brief        Exposed API to refresh the VBT data
# @param[in]    adapter Adapter
# @return       None
def refresh_vbt_data(adapter: Adapter) -> None:
    for port, panel in adapter.panels.items():
        __init_vbt_data(adapter, panel)


##
# @brief        Exposed API to check whether any given feature is supported by any of the connected adapter or not
# @param[in]    feature string indicating if feature
# @return       status Boolean, True if supported, False otherwise
def is_feature_supported(feature: str) -> bool:
    feature_mapping = {
        'VRR': 'is_vrr_supported',
        'HRR': 'is_hrr_supported'
    }
    if feature not in feature_mapping:
        return False

    for adapter in adapters.values():
        if getattr(adapter, feature_mapping[feature]):
            return True
    return False


##
# @brief        Helper API to update BFR and HRR feature caps based on ETL
# @param[in]    adapter
# @param[in]    os_aware_flipq_enable Boolean, True if Enable , False if Disable
# @return       status, Boolean, True if update successful, False otherwise
def update_bfr_hrr_caps(adapter: Adapter, os_aware_flipq_enable):
    for panel in adapter.panels.values():
        #@todo update once QMS enable.
        if panel.panel_type in ['HDMI']:
            continue
        # HRR enabled condition
        display_feature_control = registry.DisplayFeatureControl(adapter.gfx_index)
        if panel.vrr_caps.is_vrr_supported and panel.psr_caps.psr_version != 1 and not os_aware_flipq_enable and \
                (display_feature_control.disable_hrr == 0):
            if (2 * panel.drrs_caps.min_rr) <= panel.drrs_caps.max_rr:
                panel.bfr_caps.is_bfr_supported = True
            else:
                panel.bfr_caps.is_bfr_supported = False


##
# @brief        Helper API to unplug given panel from given adapter
# @param[in]    adapter
# @param[in]    panel
# @return       status, Boolean, True if unplug operation is successful, False otherwise
def unplug_wrapper(adapter: Adapter, panel: Panel):
    if __unplug_wrapper(adapter, panel) is False:
        return False
    return True


##
# @brief        Update panel config
# @param[in]    panel : panel info
# @return       panel parameters
def update_panel_vrr_profile_config_from_table(panel):
    default_profile, profile_vmin, profile_vmax, profile_sfdit, profile_sfddt, profile_is_vrr = (
        search_monitor_profile_from_table(panel.pnp_id))
    logging.info(f"default profile: {default_profile},min: {profile_vmin},max: {profile_vmax},"
                 f"sfdit: {profile_sfdit},sfddt: {profile_sfddt},is_vrr_support: {profile_is_vrr}")
    if panel.vrr_caps.is_vrr_supported != profile_is_vrr and default_profile == ARC_SYNC_PROFILE.OFF:
        panel.vrr_caps.is_vrr_supported = profile_is_vrr
    if panel.vrr_caps.is_vrr_supported:
        if (profile_vmin != 0 and profile_vmin != panel.vrr_caps.vrr_profile_min_rr and
                profile_vmin > panel.vrr_caps.vrr_profile_min_rr):
            panel.vrr_caps.vrr_profile_min_rr = profile_vmin
        if (profile_vmax != 0 and profile_vmax != panel.vrr_caps.vrr_profile_max_rr and
                profile_vmax < panel.vrr_caps.vrr_profile_max_rr):
            panel.vrr_caps.vrr_profile_max_rr = profile_vmax
        if profile_sfdit != 0 and profile_sfdit != panel.vrr_caps.vrr_profile_sfdit:
            panel.vrr_caps.vrr_profile_sfdit = profile_sfdit
        if profile_sfddt != 0 and profile_sfddt != panel.vrr_caps.vrr_profile_sfddt:
            panel.vrr_caps.vrr_profile_sfddt = profile_sfddt
    else:
        panel.vrr_caps.vrr_profile_max_rr = panel.vrr_caps.vrr_profile_min_rr = 0
        panel.vrr_caps.vrr_profile_sfdit = panel.vrr_caps.vrr_profile_sfddt = 0


##
# @brief        Update panel config based on VRR profile set
# @param[in]    panel : panel info
# @param[in]    profile : profile name
# @param[in]    minrr : profile name
# @param[in]    maxrr : profile name
# @param[in]    maxframeincreaseinus : Max Frame time increase
# @param[in]    maxframedecreaseinus : Max Frame time decrease
# @return       panel parameters
def update_panel_vrr_profile_config_from_profile(panel, profile=None, minrr=None, maxrr=None,
                                                 maxframeincreaseinus=None, maxframedecreaseinus=None):

    if panel.vrr_caps.is_vrr_supported:
        logging.info("Update panel params based on profile set. ")
        if profile.value == ARC_SYNC_PROFILE.EXCELLENT:
            panel.vrr_caps.vrr_profile_min_rr = panel.vrr_caps.vrr_min_rr
            panel.vrr_caps.vrr_profile_max_rr = panel.vrr_caps.vrr_max_rr
            panel.vrr_caps.vrr_profile_sfdit = 0
            panel.vrr_caps.vrr_profile_sfddt = 0
        elif profile.value == ARC_SYNC_PROFILE.GOOD:
            panel.vrr_caps.vrr_profile_min_rr = panel.vrr_caps.vrr_min_rr
            panel.vrr_caps.vrr_profile_max_rr = panel.vrr_caps.vrr_max_rr
            panel.vrr_caps.vrr_profile_sfdit = int((1.2 * 1000 * 1000) / panel.vrr_caps.vrr_profile_max_rr)
            panel.vrr_caps.vrr_profile_sfddt = int((1.3 * 1000 * 1000) / panel.vrr_caps.vrr_profile_max_rr)
        elif profile.value == ARC_SYNC_PROFILE.COMPATIBLE or profile.value == ARC_SYNC_PROFILE.RECOMMENDED:
            panel.vrr_caps.vrr_profile_max_rr = panel.vrr_caps.vrr_max_rr
            panel.vrr_caps.vrr_profile_min_rr = max(panel.vrr_caps.vrr_profile_max_rr // 2, panel.vrr_caps.vrr_min_rr)
            panel.vrr_caps.vrr_profile_sfdit = int((1.0 * 1000 * 1000) / panel.vrr_caps.vrr_profile_max_rr)
            panel.vrr_caps.vrr_profiel_sfddt = int((1.0 * 1000 * 1000) / panel.vrr_caps.vrr_profile_max_rr)
        elif profile.value == ARC_SYNC_PROFILE.OFF:
            panel.vrr_caps.vrr_profile_min_rr = panel.vrr_caps.vrr_profile_max_rr
            panel.vrr_caps.vrr_profile_sfdit = 0
            panel.vrr_caps.vrr_profile_sfddt = 0
        elif profile.value == ARC_SYNC_PROFILE.VESA:
            panel.vrr_caps.vrr_profile_min_rr = panel.vrr_caps.vrr_min_rr
            panel.vrr_caps.vrr_profile_max_rr = panel.vrr_caps.vrr_max_rr
            panel.vrr_caps.vrr_profile_sfdit = 0
            panel.vrr_caps.vrr_profile_sfddt = 0
        elif profile.value == ARC_SYNC_PROFILE.CUSTOM:
            if minrr is not None:
                panel.vrr_caps.vrr_profile_min_rr = minrr
            if maxrr is not None:
                panel.vrr_caps.vrr_profile_max_rr = maxrr
            if maxframeincreaseinus is not None:
                panel.vrr_caps.vrr_profile_sfdit = maxframedecreaseinus
            else:
                panel.vrr_caps.vrr_profile_sfdit = 0
            if maxframedecreaseinus is not None:
                panel.vrr_caps.vrr_profile_sfddt = maxframedecreaseinus
            else:
                panel.vrr_caps.vrr_profile_sfddt = 0


##
# @brief        search_monitor_profile_from_table
# @param[in]    inp_pnp_id : pnp_id of the monitor
# @return       profile - profile of them monitor, if nothing is found in table return compatible
def search_monitor_profile_from_table(inp_pnp_id):
    panel_dict = {}

    with open(os.path.join(test_context.ROOT_FOLDER, "Tests\\VRR\\monitors.csv")) as f:
        table = csv.reader(f, delimiter=',', quotechar='"')
        first_row = True
        size = 0
        profile_name = control_api_args.ctl_intel_arc_sync_profile_v.COMPATIBLE
        profile_min_rr = profile_max_rr = profile_sfdit = profile_sfddt = profile_is_vrr = 0
        for row in table:
            # Skip the first row (header)
            if first_row:
                first_row = False
                continue
            elif len(row) < 10:
                raise Exception("Incorrect Parameters in CSV")
            size += 1
            id_ = row[1].split(",")
            pnp_id = id_[:2] + id_[3:]
            pnp_id_string = ''.join(x[2:].zfill(2) for x in pnp_id).lower()
            if pnp_id_string == inp_pnp_id:
                profile_name = row[4].strip()
                profile_min_rr = int(row[5].strip())
                profile_max_rr = int(row[6].strip())
                profile_sfdit = int(row[7].strip())
                profile_sfddt = int(row[8].strip())
                profile_is_vrr = int(row[9].strip())
                break

    return profile_name, profile_min_rr, profile_max_rr, profile_sfdit, profile_sfddt, profile_is_vrr


##
# @brief       The Function returns an Integer Value and ignores the fractional parts,
#              For non-zero exponents value is ((-1)*Signbit) x (2 ^ (exponent-15)) x ( 1.SignificantBitsInBinary)
# @param[in]    half_precision_floating_binary edid data
# @return       Brightness Value in Nits
def get_brightness_value(half_precision_floating_binary: int):
    #halfprecisonfloatingbinary - 16 bits total, 0-9bits - mantissa, 10-14 - exponent, 15th bit sign
    exponent = (half_precision_floating_binary & 0x7C00) >> 10
    mantissa = half_precision_floating_binary & 0x3FF

    #Use the delta value to avoid negative exponent
    power_factor = abs(exponent-15)
    #2^(|15-Exp|)
    exponent_factor = 1 << power_factor
    #Make the Value as 1.Factional_part
    mantissa_factor = mantissa | 0x0400

    if exponent > 15:
        decimal_value = int((exponent_factor * mantissa_factor)/1024.0)
    else:
        decimal_value = int(mantissa_factor/(exponent_factor*1024.0))

    return decimal_value

##
# @brief        Helper API to luminance data from edid
# @param[in]    panel Panel object
# @return       None
def __get_luminance_data(panel: Panel, edid_data):
    extension_blocks = edid_data[126]
    if extension_blocks < 2:
        logging.debug("EDID Extension blocks less than 2")
        return
    __get_luminance_data_from_did_2p1(panel, edid_data)
    __get_luminance_data_from_display_param(panel, edid_data)


##
# @brief        Helper API to get DID2.1 caps for given panel
# @param[in]    edid luminance data
# @param[in]    panel Panel object
# @return       None
def __get_luminance_data_from_did_2p1(panel: Panel, edid_data):
    try:
        did_2p1_min_cll_index = 206
        did_2p1_min_cll_value = int(f"{edid_data[did_2p1_min_cll_index + 1]:02x}{edid_data[did_2p1_min_cll_index]:02x}",
                                    16)
        panel.luminance_caps.min_cll_did_2p1 = get_brightness_value(did_2p1_min_cll_value)

        did_2p1_max_fall_index = 208
        did_2p1_max_fall_value = int(f"{edid_data[did_2p1_max_fall_index + 1]:02x}{edid_data[did_2p1_max_fall_index]:02x}",
                                     16)
        panel.luminance_caps.max_fall_did_2p1 = get_brightness_value(did_2p1_max_fall_value)

        did_2p1_max_cll_index = 210
        did_2p1_max_cll_value = int(f"{edid_data[did_2p1_max_cll_index + 1]:02x}{edid_data[did_2p1_max_cll_index]:02x}",
                                    16)
        panel.luminance_caps.max_cll_did_2p1 = get_brightness_value(did_2p1_max_cll_value)

    except IndexError:
        logging.error("Index is out of range for edid_data")




##
# @brief        Helper API to get Display Param caps for given panel
# @param[in]    edid luminance data
# @param[in]    panel Panel object
# @return       None
def __get_luminance_data_from_display_param(panel: Panel, edid_data):
    try:
        dp_min_cll_index = 161
        dp_min_cll_value = int(f"{edid_data[dp_min_cll_index + 1]:02x}{edid_data[dp_min_cll_index]:02x}", 16)
        panel.luminance_caps.min_cll_display_param = get_brightness_value(dp_min_cll_value)

        dp_max_fall_index = 157
        dp_max_fall_value = int(f"{edid_data[dp_max_fall_index + 1]:02x}{edid_data[dp_max_fall_index]:02x}", 16)
        panel.luminance_caps.max_fall_display_param = get_brightness_value(dp_max_fall_value)

        dp_max_cll_index = 159
        dp_max_cll_value = int(f"{edid_data[dp_max_cll_index + 1]:02x}{edid_data[dp_max_cll_index]:02x}", 16)
        panel.luminance_caps.max_cll_display_param = get_brightness_value(dp_max_cll_value)

    except IndexError:
        logging.error("Index is out of range for edid_data")
