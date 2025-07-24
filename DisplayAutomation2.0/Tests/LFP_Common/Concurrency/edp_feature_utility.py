#######################################################################################################################
# @file         edp_feature_utility.py
# @brief        This file contains all feature related verification APIs or wrappers
#
# @author       Bhargav Adigarla
#######################################################################################################################
import logging, sys
import os
import time
import datetime
from Libs.Core import enum, driver_escape, registry_access, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper.driver_escape_args import DppHwLutInfo, DppHwLutOperation
from Libs.Feature.display_fbc import fbc
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Core import cmd_parser
from Tests.EDP.MSO import mso
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, workload
from Tests.VRR import vrr
from registers.mmioregister import MMIORegister
from Libs.Feature.mipi import mipi_helper
from Tests.MIPI.Verifiers import mipi_dual_link, mipi_timings, mipi_dphy_config, \
    mipi_link_related, mipi_status
from Tests.MIPI.Verifiers.mipi_video_mode import verify_video_mode_enable_bits


##
# @brief        Verify whether feature is supported in panel and pipe
# @param[in]    panel - Panel object
# @return       True if supported else False
def verify_feature_support(panel):
    if panel.feature == "PSR1":
        return panel.psr_caps.is_psr_supported
    elif panel.feature == "PSR2":
        if panel.pipe == 'A' and common.PLATFORM_NAME == 'TGL':
            return panel.psr_caps.is_psr2_supported
        elif panel.pipe in ['A', 'B']:
            return panel.psr_caps.is_psr2_supported
        return False
    elif panel.feature == "VDSC":
        if panel.port in ["MIPI_A", "MIPI_C"]:
            return True
        return panel.vdsc_caps.is_vdsc_supported
    elif panel.feature == "MSO":
        if panel.pipe == 'A':
            return panel.mso_caps.is_mso_supported
        return False
    elif panel.feature == "ASSR":
        return panel.edp_caps.is_assr_supported
    elif panel.feature in ["DRRS", "DMRRS"]:
        return panel.drrs_caps.is_drrs_supported
    elif panel.feature == "VRR":
        return panel.vrr_caps.is_vrr_supported
    elif panel.feature == "LRR1":
        return False  # @todo: Add for LRR1
    elif panel.feature == "LRR2":
        return False  # @todo: Add for LRR2
    elif panel.feature == "HDR":  # @todo: Add for HDR
        return False
    elif panel.feature == "FBC":
        if panel.pipe == 'A' and common.PLATFORM_NAME in ['TGL', 'ADLP']:
            return True
        elif panel.pipe in ['A', 'B']:
            return True
        return False
    elif panel.feature == "LACE":
        if panel.pipe == 'A' and common.PLATFORM_NAME == 'TGL':
            return True
        elif panel.pipe in ['A', 'B']:
            return True
        return False
    elif panel.feature in ["3DLUT", "DPST", "BLC"]:
        return True
    elif panel.feature == "VIDEO_MODE":
        if panel.mipi_caps.is_feature_swapped is True and panel.mipi_caps.is_video_mode_supported is False:
            return True
        return panel.mipi_caps.is_video_mode_supported
    else:
        logging.error("Invalid feature {0}".format(panel.feature))
        return False


##
# @brief        Verify whether feature is enabled in driver
# @param[in]    adapter - Adapter object
# @param[in]    panel - Panel object
# @param[in]    feature PSR1/PSR2 based on PSR2 restriction check else, None
# @return       bool - True if supported else False
def verify_feature_enabled_in_driver(adapter, panel, feature=None):
    if __verify_feature_support_in_config(adapter, panel) is False:
        return False
    if panel.feature == "PSR1":
        return psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_1)
    elif panel.feature == "PSR2":
        # Check PSR2 restriction return value
        if feature == psr.UserRequestedFeature.PSR_1:
            logging.info(f"PSR2 Restriction Failed, falling back to PSR1")
            return psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_1)
        else:
            return psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2)
    elif panel.feature == "VDSC":
        return dsc_verifier.verify_dsc_programming(adapter.gfx_index, panel.port)
    elif panel.feature == "MSO":
        return mso.verify(panel)
    elif panel.feature == "ASSR":
        return __verify_assr(panel)
    elif panel.feature == "DPST":
        return __verify_dpst(adapter, panel)
    elif panel.feature == "FBC":
        return fbc.verify_adapter_fbc(adapter.gfx_index)
    elif panel.feature == "LACE":
        return __get_lace_status(adapter, panel)
    elif panel.feature == "3DLUT":
        return __verify_3dlut(adapter, panel)
    elif panel.feature == "VRR":
        return verify_vrr(adapter, panel)
    elif panel.feature == "LRR1":
        return False  # @todo: Add for LRR1
    elif panel.feature == "LRR2":
        return False  # @todo: Add for LRR2
    elif panel.feature in ["DRRS", "DMRRS"]:  # @todo: Add for DRRS and DMRRS
        return False
    elif panel.feature == "HDR":  # @todo: Add for HDR
        return False
    elif panel.feature == "BLC":  # @todo: Add for BLC
        return False
    elif panel.feature == "VIDEO_MODE":
        return __verify_video_mode(panel)
    else:
        logging.error("\tInvalid feature {0}".format(panel.feature))
        return False


##
# @brief        This function is to get he lut ready status
# @param[in]    lut_reg - name of the register
# @param[in]    platform - name of the platform
# @return       new_lut_ready_status - lut ready status
def get_new_lut_ready_status(lut_reg, platform):
    instance = MMIORegister.get_instance('LUT_3D_CTL_REGISTER', lut_reg, platform)
    lut_3d_ctl_reg_offset = instance.offset
    new_lut_ready_status = (driver_interface.DriverInterface().mmio_read(lut_3d_ctl_reg_offset, 'gfx_0') >> 30) & 1
    return new_lut_ready_status


##
# @brief        This function is to verify the hardware reset status
# @param[in]    lut_3d_ctl_reg - register whose status if to be known
# @param[in]    platform - name of the platform
# @return       bool - True if H/W is reset, False otherwise
def verify_hw_reset_status(lut_3d_ctl_reg, platform):
    milliseconds = 0.005
    expected_resettime_limit = 15
    status = 1
    start_time = datetime.datetime.now()
    while status != 0:
        status = get_new_lut_ready_status(lut_3d_ctl_reg, platform)
        if status != 0:
            logging.debug(
                "Still H/W not resetted the new_lut_ready bit, will read the status again post 5 ms")
            time.sleep(milliseconds)
    end_time = datetime.datetime.now()
    total_time = (end_time - start_time).total_seconds() * 1000  # Convert seconds to milliseconds
    if total_time > expected_resettime_limit:
        logging.info(
            "Expected :less than 15 ms and Actual time taken: {0} ms -H\W failed to reset the new_lut_ready bit "
            "within 15 ms".format(total_time))
        gdhm.report_bug(
            title="[EDP][3DLUT] Hardware failed to reset the new_lut_ready bit within 15 ms",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
    else:
        logging.info("Expected: less than 15 ms and actual time taken: {0} ms - H\W resetted the new_lut_ready bit"
                     " within 15 ms".format(total_time))
    return status == 0


##
# @brief        API to enable feature in panel
# @param[in]    adapter - Adapter object
# @param[in]    panel - Panel object
# @param[in]    disable - number to indicate if feature has to be enabled
# @return       bool - True if enabled else False
def enable(adapter, panel, disable=0):
    enable = 1 if disable == 0 else 0
    if panel.feature == "DPST":
        if enable:
            dpst_status = dpst.enable(adapter, True)
        else:
            dpst_status = dpst.disable(adapter)
        if dpst_status is False:
            return False
        if dpst_status is True:
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                return False
        return True
    if panel.feature == "VDSC" and panel.vdsc_caps.is_vdsc_supported is True:
        # VDSC+PSR2 cannot co-exist for pre-gen13+DG2 platforms, so need to disable PSR2 to enable vdsc feature for edp
        # vdsc panel that supports psr2
        if panel.is_lfp is True and panel.port in ['DP_A','DP_B'] and panel.psr_caps.is_psr2_supported is True and \
                adapter.name.upper() in (common.PRE_GEN_13_PLATFORMS + ['DG2']):
            # To enable vdsc feature, disable psr2 feature
            return DSCHelper.enable_disable_psr2(adapter.gfx_index, False)
    if panel.feature == "FBC":
        if enable:
            fbc_status = fbc.enable(adapter.gfx_index)
        else:
            fbc_status = fbc.disable(adapter.gfx_index)
        if fbc_status is False:
            return False
        if fbc_status is True:
            driver_restart_status, system_reboot_required = display_essential.restart_gfx_driver()
            logging.info(f"Driver restart status = {driver_restart_status}, Reboot required = {system_reboot_required}")
            if driver_restart_status is False:
                logging.error("Failed to restart graphics driver")
                return False
        return True

    if panel.feature == "LACE":
        return enable_lace(adapter, panel)
    else:
        logging.error("\tInvalid feature {0}".format(panel.feature))
        return False


##
# @brief        Function to enable the LACE  in driver
# @param[in]    adapter - Adapter object
# @param[in]    panel - Panel object
# @return       bool - True if supported else False
def enable_lace(adapter, panel):
    lux = 600 # Lace will get trigger at lux value of 551 with default table of lux and aggr percent
    aggr_level = 1

    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.LOCAL_MACHINE, r"SOFTWARE\Intel\Display")
    registry_access.write(args=reg_args, reg_name="BKPDisplayLACE", reg_type=registry_access.RegDataType.DWORD,
                          reg_value=1, sub_key=r"igfxcui\MISC")
    status, reboot_required = display_essential.restart_gfx_driver()
    if status:
        reg_val, _ = registry_access.read(args=reg_args, reg_name="BKPDisplayLACE", sub_key=r"igfxcui\MISC")
        if reg_val:
            logging.info("BKPDisplayLACE is added successfully")

            logging.info(
                "Verifying LACE on pipe {0} with Lux = 501 and Moderate Aggressiveness level".format(panel.pipe))
            if driver_escape.als_aggressiveness_level_override(panel.target_id, lux, lux_operation=True,
                                                               aggressiveness_level=aggr_level,
                                                               aggressiveness_operation=True):
                logging.info("Lux and aggressiveness levels set successfully")
                return True
            else:
                gdhm.report_bug(
                    title="[EDP][LACE] Failed to set lace aggressiveness levels - Dual eDP",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("\tFailed to set lux and aggressiveness levels")
                logging.error("\tLux = %s AggressivenessLevel = %s" % (lux, aggr_level))
                return False

        else:
            logging.error("Failed to enable the LACE")
            return False
    else:
        logging.info("Failed to restart display driver")
        return False


##
# @brief        Verify whether ASSR is enabled in driver
# @param[in]    panel - Panel object
# @return       bool - True if supported else False
def __verify_assr(panel):
    ##
    # Check whether ASSR is enabled in the driver or not
    enabled = 1
    offset_name = "DP_TP_CTL_" + panel.pipe
    dp_tp_ctl = MMIORegister.read("DP_TP_CTL_REGISTER", offset_name, common.PLATFORM_NAME)
    return dp_tp_ctl.alternate_sr_enable == enabled


##
# @brief        Function to verify if DPST is enabled in driver
# @param[in]    adapter - Adapter object
# @param[in]    panel - Panel object
# @return       bool - True if enabled else False
def __verify_dpst(adapter, panel):
    etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL)
    return dpst.verify(adapter, panel, etl_file)


##
# @brief        Function to get the lace status
# @param[in]    adapter - Adapter object
# @param[in]    panel - Panel object
# @return       bool - True if enabled else False
def __get_lace_status(adapter, panel):

    enabled = 1
    lace_enable_status, etl_file = pc_external.enable_disable_lace(adapter, panel, enabled, adapter.gfx_index)
    if not lace_enable_status:
        return False
    logging.info("Succesfully enabled LACE")
    dplc_ctl_reg = 'DPLC_CTL' + '_' + panel.pipe
    dplc_ctl_reg_value = MMIORegister.read('DPLC_CTL_REGISTER', dplc_ctl_reg, common.PLATFORM_NAME)
    return dplc_ctl_reg_value.function_enable == enabled


##
# @brief        Function to verify if 3DLUT is enabled in driver
# @param[in]    adapter - Adapter object
# @param[in]    panel - Panel object
# @return       bool - True if enabled else False
def __verify_3dlut(adapter, panel):
    bin_file = "CustomLUT_no_R.bin"
    bin_file_path = "Color\\Hw3DLUT\\CustomLUT\\" + bin_file
    path = os.path.join(test_context.SHARED_BINARY_FOLDER, bin_file_path)
    cui_dpp_hw_lut_info = DppHwLutInfo(panel.target_id, DppHwLutOperation.UNKNOWN.value, 0)
    result, cui_dpp_hw_lut_info = driver_escape.get_dpp_hw_lut(adapter.gfx_index, cui_dpp_hw_lut_info)
    if result is False:
        logging.error(f'Escape call failed : get_dpp_hw_lut() for {panel.target_id}')

    cui_dpp_hw_lut_info = DppHwLutInfo(panel.target_id, DppHwLutOperation.APPLY_LUT.value, cui_dpp_hw_lut_info.depth)
    if cui_dpp_hw_lut_info.convert_lut_data(path) is False:
        logging.error(f'Invalid bin file path provided : {path}!')

    result = driver_escape.set_dpp_hw_lut(adapter.gfx_index, cui_dpp_hw_lut_info)
    if result is False:
        logging.error(f'Escape call failed : set_dpp_hw_lut() for {panel.target_id}')

    lut_3d_ctl_reg = 'LUT_3D_CTL' + '_' + panel.pipe
    instance = MMIORegister.get_instance('LUT_3D_CTL_REGISTER', lut_3d_ctl_reg, common.PLATFORM_NAME)
    lut_3d_ctl_reg_offset = instance.offset
    lut_3d_enable = (driver_interface.DriverInterface().mmio_read(lut_3d_ctl_reg_offset, 'gfx_0') >> 31)
    if lut_3d_enable == 1:
        hw_3d_lut_status = True
        logging.info("Hw 3D LUT is enabled on pipe %c", panel.pipe)
        hw_lut_buffer_status = verify_hw_reset_status(lut_3d_ctl_reg, common.PLATFORM_NAME)
        if hw_lut_buffer_status is False:
            logging.error("Hardware failed to reset the new_lut_ready bit  Dual eDP")
            gdhm.report_bug(
                title="[EDP][3DLUT] Hardware did not load the lut buffer into internal working RAM - Dual eDP",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False
    else:
        logging.error("Hw 3D LUT is disabled")
        return False
    if hw_3d_lut_status is True and hw_lut_buffer_status is True:
        return True
    return False


##
# @brief        This is a helper function for 3dlut verification
# @param[in]    prog_lut - lut values,
# @param[in]    input_file - name of bin file
# @return       bool - True if enabled else False
def __verify_lut_data(prog_lut, input_file):
    red_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                0x300, 0x340, 0x380, 0x3C0, 0x3FC]
    green_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                  0x300, 0x340, 0x380, 0x3C0, 0x3FC]
    blue_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                 0x300, 0x340, 0x380, 0x3C0, 0x3FC]
    ref_lut = []
    count = 0
    if input_file == "CustomLUT_no_R.bin":
        for i in range(0, 17):
            red_data[i] = 0
    elif input_file == "CustomLUT_no_G.bin":
        for i in range(0, 17):
            green_data[i] = 0
    elif input_file == "CustomLUT_no_B.bin":
        for i in range(0, 17):
            blue_data[i] = 0
    for i in range(0, 17):
        for j in range(0, 17):
            for k in range(0, 17):
                ref_lut.append(red_data[i])
                ref_lut.append(green_data[j])
                ref_lut.append(blue_data[k])
                count = count + 3
    index = 0
    for reg_val, ref_val in zip(prog_lut, ref_lut):
        if reg_val != ref_val:
            logging.error("\tLUT values not matching Index : %d ProgrammedVal : %d Expected val : %d ", index, reg_val,
                          ref_val)
            gdhm.report_bug(
                title="[EDP][3DLUT] LUT values not matching - Dual eDP",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False
        index += 1


##
# @brief        helper function to extract bits from value
# @param[in]    value - value in a register
# @param[in]    start - start of bits
# @param[in]    end - end of bits
# @return       ret_value - True if enabled else False
def __get_value(value, start, end):
    ret_value = (value << (31 - end)) & 0xFFFFFFFF
    ret_value = (ret_value >> (31 - end + start)) & 0xFFFFFFFF
    return ret_value


##
# @brief        helper function to verify vrr
# @param[in]    adapter - Adapter object
# @param[in]    panel - Panel object
# @return       bool - True if vrr verification successful, False otherwise
def verify_vrr(adapter, panel):
    display_config_ = display_config.DisplayConfiguration()
    current_config = display_config_.get_current_display_configuration()
    if current_config.topology != enum.SINGLE:
        logging.info("Skipping VRR verification in multi display config mode")
        return True
    etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.Classic3DCubeApp, 30, True])
    # Ensure async flips
    if vrr.async_flips_present(etl_file) is False:
        etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.MovingRectangleApp, 30, True])
        if vrr.async_flips_present(etl_file) is False:
            logging.warning("OS is NOT sending async flips")
            return False

    logging.info("Step: Verifying VRR for {0}".format(panel.port))
    return vrr.verify(adapter, panel, etl_file)


##
# @brief        helper function to verify feature support for a given config
# @param[in]    adapter - Adapter object
# @param[in]    panel - Panel object
# @return       bool - True if verification successful, False otherwise
def __verify_feature_support_in_config(adapter, panel):

    panels = list(adapter.panels.values())

    ##
    # Updating both panel features to align with command line
    cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)
    # Handle multi-adapter scenario
    if not isinstance(cmd_line_param, list):
        cmd_line_param = [cmd_line_param]
    panels[0].feature = cmd_line_param[0]['LFP1'][0].upper()
    panels[1].feature = cmd_line_param[0]['LFP2'][0].upper()

    if common.PLATFORM_NAME == "TGL":
        if panel.pipe == 'B' and panel.feature == 'PSR2':
            panel.feature = 'PSR1'
            logging.info("PSR2 won't support on pipe B. Fallback to PSR1")

        if panel.pipe == 'A' and panel.feature == "PSR1":
            panel.feature = 'PSR2'
            if verify_feature_support(panel) is True:
                logging.info("PSR2 capable panel connected. Upgraded to PSR2")
            else:
                panel.feature = "PSR1"

    if verify_feature_support(panel) is True:
        logging.info("{0} supported on {1} pipe {2}".format(panel.feature, panel.port, panel.pipe))
        return True
    panels[0].feature, panels[1].feature = panels[1].feature, panels[0].feature

    # If LACE,MSO,FBC requested on pipe A and PSR2 on B, following condition will be hit.
    if common.PLATFORM_NAME == "TGL":
        if panel.pipe == 'B' and panel.feature == 'PSR2':
            panel.feature = 'PSR1'
            logging.info("PSR2 won't support on pipe B. Fallback to PSR1")

    # Due to feature swap MIPI video mode verification can come to other pipe where VBT settings are not for MIPI display
    # In this condition need to skip video mode verification and verify other swapped feature on MIPI display.
    # Adding flag to pass information to video mode verification to skip this verification
    if panel.feature == 'VIDEO_MODE' and panel.mipi_caps.is_video_mode_supported is False:
        panel.mipi_caps.is_feature_swapped = True

    if verify_feature_support(panel) is True:
        logging.info("Updated feature due to dynamic pipe allocation")
        logging.info("{0} supported on {1} pipe {2}".format(panel.feature, panel.port, panel.pipe))
        return True
    logging.error("\t{0} Not supported on both panels (Planning Issue)".format(panel.feature))
    return False


##
# @brief        Verify Video mode for MIPI
# @param[in]    panel - adapter object, panel object
# @return       bool - True if enabled else False
def __verify_video_mode(panel):

    # Due to feature swap MIPI video mode verification can come to other pipe where VBT settings are not for MIPI display
    # In this condition need to skip video mode verification and verify other swapped feature on MIPI display.
    if panel.mipi_caps.is_feature_swapped is True and panel.mipi_caps.is_video_mode_supported is False:
        logging.info("Due to feature swap MIPI Video mode verification is getting skipped!!!")
        return True

    status = False

    _mipi_helper = mipi_helper.MipiHelper(common.PLATFORM_NAME.lower())
    port = "_DSI0" if panel.port == "MIPI_A" else "_DSI1"

    # MIPI Video mode enable bits verification
    logging.info('Step: MIPI video mode verification')
    verify_video_mode_enable_bits(_mipi_helper, port)

    # MIPI Dual link verification
    if panel.mipi_caps.is_dual_link:
        logging.info('Step: MIPI dual link verification')
        mipi_dual_link.verify_dual_link_config(_mipi_helper)

    # MIPI timings verification
    logging.info('Step: MIPI timings verification')
    mipi_timings.verify_timings(_mipi_helper, port)

    # MIPI DPHY verification
    logging.info('Step: MIPI DPHY verification')
    mipi_dphy_config.verify_dphy_config(_mipi_helper, port)

    # MIPI link related verification
    logging.info('Step: MIPI link related verification')
    mipi_link_related.verify_pixel_format_data_lanes(_mipi_helper, port)
    mipi_link_related.verify_link_config(_mipi_helper, port)
    mipi_link_related.verify_timeouts(_mipi_helper, port)

    # MIPI status bits verification
    logging.info('Step: MIPI status bits verification')
    if mipi_status.check_mipi_status_bits(_mipi_helper, [port]) is False:
        logging.error('MIPI status verification failed')
    else:
        logging.info('MIPI status verification Passed')

    # report test failure if fail_count>0
    if _mipi_helper.verify_fail_count > 0:
        logging.error("Some checks in the test have failed. Check error logs. No. of failures= "
                      "%d" % _mipi_helper.verify_fail_count)
        gdhm.report_bug(
            title="[MIPI][VIDEO_MODE] Video mode verification failed",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        return False
    return True
