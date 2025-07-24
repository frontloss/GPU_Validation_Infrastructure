#######################################################################################################################
# @file             psr_escape.py
# @addtogroup       PowerCons
# @section          PSR_Tests
# @brief           Test for verifying PSR Status and Psr enable/disable using Escape call
#
# @author           Chandrakanth Reddy
#######################################################################################################################

import ctypes

from Libs.Core import display_power
from Libs.Core.driver_escape import get_set_display_pc_feature_state
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_environment
from Libs.Core.wrapper import control_api_wrapper, control_api_args
from Libs.Core.wrapper.driver_escape_args import PwrSrcEventArgs, PwrConsUserPowerPlan, PwrConsOperation, \
    CuiEscOperationType, ComEscPowerConservationArgs

from Tests.PowerCons.Functional.PSR.psr_base import *

##
# @brief           This class contains tests for verifying PSR Status and Psr enable/disable using Escape call
class PsrEscape(PsrBase):
    ##
    # @brief           This tests verifies PSR Status and Psr enable/disable using Escape call with a powerline switch
    #                  to AC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC"])
    # @endcond
    def t_11_psr_escape_ac(self):
        igcl_power_plan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
        if not self.display_power_.set_current_powerline_status(display_power.PowerSource.AC):
            self.fail("Failed to switch power line status to AC (Test Issue)")
        for adapter in dut.adapters.values():
            if not verify_psr_escape_call(self, adapter, PwrSrcEventArgs.PWR_AC.value, igcl_power_plan):
                self.fail("FAIL : PSR Escape Call verification")
            logging.info("PASS: PSR escape call verification")


    ##
    # @brief        This tests verifies PSR Status and Psr enable/disable using Escape call with a powerline switch
    #               to DC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC"])
    # @endcond
    def t_11_psr_escape_dc(self):
        igcl_power_plan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
        if not self.display_power_.set_current_powerline_status(display_power.PowerSource.DC):
            self.fail("Failed to switch power line status to DC Test Issue)")
        for adapter in dut.adapters.values():
            if not verify_psr_escape_call(self, adapter, PwrSrcEventArgs.PWR_DC.value, igcl_power_plan):
                self.fail("FAIL : PSR Escape Call verification")
            logging.info("PASS: PSR escape call verification")

##
# @brief        API to verify PSR through Escape call
# @param[in]    adapter Adapter object
# @param[in]    power_source PwrSrcEventArgs, AC/DC
# @param[in]    igcl_power_plan IGCL Power Plan
# @return       True if verification is successful, False otherwise
def verify_psr_escape_call(self, adapter, power_source, igcl_power_plan):
    feature, feature_str = self.get_feature(adapter)
    for panel in adapter.panels.values():
        if adapter.name in machine_info.PRE_GEN_13_PLATFORMS:
            if get_set_psr_via_cui_sdk(adapter, panel, feature, power_source) is False:
                logging.error("FAIL : PSR Escape call verification via CUI")
                return False
        else:
            if power_source == PwrSrcEventArgs.PWR_AC.value:
                power_source = control_api_args.ctl_power_source_v.AC.value
            elif power_source == PwrSrcEventArgs.PWR_DC.value:
                power_source = control_api_args.ctl_power_source_v.DC.value
            if not get_set_psr_via_igcl(adapter, panel, feature, power_source, igcl_power_plan):
                # get_set_psr_via_igcl API returns False even when PSR is not supported in the panel
                # Test should continue to next panel(if present) if this happens
                if not psr.is_feature_supported_in_panel(panel.target_id, feature):
                    logging.warning(f"{feature_str} is not supported in the panel. Skipping escape call verification via IGCL")
                    continue
                logging.error("FAIL : PSR escape call verification via IGCL")
                return False
    return True


##
# @brief        API to verify Psr Enable & support using CUI based escape call
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    feature UserRequestedFeature, PSR version to be verified
# @param[in]    power_source PwrSrcEventArgs, AC/DC
# @return       status, Boolean, True, if verification successful, False otherwise
def get_set_psr_via_cui_sdk(adapter, panel, feature, power_source):
    if __get_psr_via_cui_sdk(adapter, panel, feature, power_source) is False:
        logging.error("PSR status verification failed")
        return False
    if __set_psr_via_cui_sdk(adapter, panel, feature, power_source) is False:
        logging.error("PSR enable/disable using escape call failed")
        return False
    return True

##
# @brief        API to verify Psr Enable & support using escape call
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    feature UserRequestedFeature, PSR version to be verified
# @param[in]    power_source PwrSrcEventArgs, AC/DC
# @return       status, Boolean, True, if verification successful, False otherwise
def __get_psr_via_cui_sdk(adapter, panel, feature, power_source):
    if not panel.psr_caps.is_psr_supported:
        logging.info("SKIP : PSR status check on Non-PSR Panel")
        return True
    feature_args = ComEscPowerConservationArgs()
    feature_args.OldVersion = False
    feature_args.Operation = PwrConsOperation.PWRCONS_OP_FEATURE_SETTINGS.value
    feature_args.OpType = CuiEscOperationType.GET.value
    feature_args.PowerSourceType = power_source
    feature_args.OpParameters.PowerPlanParam.UserPowerPlan = PwrConsUserPowerPlan.PWRCONS_PLAN_CURRENT.value
    status, feature_args = get_set_display_pc_feature_state(adapter.gfx_index, feature_args)
    if status is False:
        logging.error("Escape call failed")
        psr.report_gdhm('Escape call failed', feature)
        return False
    enable = bool(feature_args.OpParameters.FeatureSettingsParam.Policy.PwrConsFeaturePolicyParams.\
        PwrConsFeaturePolicyFields.Enabled.Psr)
    supported = bool(feature_args.OpParameters.FeatureSettingsParam.Policy.PwrConsFeaturePolicyParams.\
        PwrConsFeaturePolicyFields.Supported.Psr)
    if panel.psr_caps.is_psr_supported or panel.psr_caps.is_psr2_supported:
        psr_status = bool(psr.is_psr_enabled_in_driver(adapter, panel, feature))
        if not enable and psr_status:
            logging.error("FAIL: PSR escape call reported PSR is disabled")
            psr.report_gdhm('PSR escape call reported PSR is disabled', feature)
            return False
        if enable and psr_status is False:
            logging.error("FAIL: PSR is disabled in driver but still escape call reported as enabled")
            psr.report_gdhm('PSR is disabled in driver but still escape call has reported as enabled', feature)
            return False
        logging.info(f"PASS: PSR enable status Expected = {enable} Actual = {psr_status}")
        if not supported:
            logging.error(f"FAIL: {panel.port} supports PSR but still escape call reported as PSR not supported")
            psr.report_gdhm('Panel supports PSR but still escape call reported as PSR not supported', feature)
            return False
        logging.info(f"PASS: PSR support status Expected = {supported} Actual = True")
    else:
        if supported:
            logging.error(f"FAIL: {panel.port} does not support PSR but still escape call reported as PSR supported")
            psr.report_gdhm('Panel does not support PSR but still escape call has reported as PSR supported', feature)
            return False
        logging.info(f"PASS: PSR support status on non-psr panel Expected = {supported == 0} Actual = False")
        if enable:
            logging.error(f"FAIL: {panel.port} does not support PSR but still escape call reported as PSR enabled")
            psr.report_gdhm('Panel does not support PSR but still escape call has reported as PSR enabled', feature)
            return False
        logging.info(f"PASS: PSR enable status on non-psr panel Expected = {enable == 1} Actual = False")
    return True


##
# @brief        Exposed API to verify Psr with enable and disable using escape call
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    feature UserRequestedFeature, PSR version to be verified
# @param[in]    power_source PwrSrcEventArgs, AC/DC
# @return       status, Boolean, True, if verification successful, False otherwise
def __set_psr_via_cui_sdk(adapter, panel, feature, power_source):
    if not (panel.psr_caps.is_psr_supported or panel.psr_caps.is_psr2_supported):
        logging.info("SKIP : PSR enable/disable on Non-PSR Panel")
        return True
    feature_args = ComEscPowerConservationArgs()
    feature_args.OldVersion = False
    feature_args.Operation = PwrConsOperation.PWRCONS_OP_FEATURE_SETTINGS.value
    feature_args.OpType = CuiEscOperationType.SET.value
    feature_args.PowerSourceType = power_source
    feature_args.OpParameters.PowerPlanParam.UserPowerPlan = PwrConsUserPowerPlan.PWRCONS_PLAN_CURRENT.value
    feature_args.OpParameters.FeatureSettingsParam.Policy.PwrConsFeaturePolicyParams. \
        PwrConsFeaturePolicyFields.Enabled.Psr = 0

    # Skip the verification for Port B
    if panel.port != 'DP_A':
        logging.info(f"SKIP : PSR enable/disable on {panel.port}")
        return True
    logging.info("Step : Disabling PSR using escape call")
    status, feature_args = get_set_display_pc_feature_state(adapter.gfx_index, feature_args)
    if status is False:
        logging.error("Escape call failed")
        psr.report_gdhm('Escape call failed', feature)
        return False
    psr_status = psr.is_psr_enabled_in_driver(adapter, panel, feature)
    if psr_status:
        logging.error("\tFAIL: PSR is not disabled in driver")
        psr.report_gdhm('PSR is not disabled in driver after disabling through Escape call', feature)
        return False

    logging.info("\tPASS: PSR disabled successfully")
    # Enable PSR using escape call
    logging.info("STEP : Enabling PSR using escape call")
    feature_args.OpParameters.FeatureSettingsParam.Policy.PwrConsFeaturePolicyParams. \
        PwrConsFeaturePolicyFields.Enabled.Psr = 1
    status, feature_args = get_set_display_pc_feature_state(adapter.gfx_index, feature_args)
    if status is False:
        logging.error("Escape call failed")
        psr.report_gdhm('Escape call failed', feature)
        return False
    psr_status = psr.is_psr_enabled_in_driver(adapter, panel, feature)
    if psr_status is False:
        logging.error("\tFAIL: PSR is not enabled in driver")
        psr.report_gdhm('PSR is not enabled in driver after enabling through Escape call', feature)
        return False

    logging.info("\tPASS:PSR Enabled successfully")
    return True


##
# @brief        API to verify PSR enable disable using IGCL based escape call
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    feature PSR Feature
# @param[in]    pwr_src
# @param[in]    igcl_power_plan
# @return       None
def get_set_psr_via_igcl(adapter, panel, feature, pwr_src=None, igcl_power_plan= None):
    get_pwr_caps = control_api_args.ctl_power_optimization_caps_t()
    get_pwr_caps.Size = ctypes.sizeof(get_pwr_caps)
    logging.info("Step : Get Power Caps to get current feature Status")
    if not control_api_wrapper.get_power_caps(get_pwr_caps, panel.target_id):
        logging.error("\t\tFail: Get PSR via IGCL")
        psr.report_gdhm('Failed to get current PSR status via IGCL', feature)
        return False
    logging.info(f"\t\tPass: PSR status = {get_pwr_caps.SupportedFeatures} via IGCL")

    if not get_pwr_caps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.PSR.value:
        logging.error("PSR Feature is not supported due to feature disabled in Registry "
                        "/ Non-PSR Panel is connected to System")
        return False

    logging.info("Step: Get PSR Status via IGCL before PSR Disable/Enable")
    psr_enabled = psr.get_status_via_igcl(panel, feature, pwr_src, igcl_power_plan)
    if psr_enabled is None:
        return False

    psr_stat_str_dict = { True: "Enabling", False: "Disabling"}
    logging.info(f"\t\tPASS: PSR status = {'Enabled' if psr_enabled else 'Disabled'} via IGCL")

    # Enable/Disable PSR based on initial PSR status
    # If PSR is Enabled in the start, Disable PSR - Check disable Status - Toggle the PSR status - Continue to Enable PSR
    # If PSR is Disabled in the start, Enable PSR - Check Enable Status - Toggle the PSR status - Continue to Disable PSR
    # Final step should enable PSR
    count = 1
    while count <= 2 or not psr_enabled:
        # Negating psr_enabled for enabling/disabling PSR in each iteration as we need to toggle the initial status
        logging.info(f"Step : {psr_stat_str_dict[not psr_enabled]} PSR via IGCL")
        if psr.enable_disable_psr_via_igcl(panel, not psr_enabled, pwr_src, igcl_power_plan) is False:
            psr.report_gdhm('Failed %s PSR via IGCL' % {psr_stat_str_dict[not psr_enabled]}, feature)
            return False
        logging.info(f"Step : Get PSR Status via IGCL after PSR {psr_stat_str_dict[not psr_enabled]}")

        psr_enabled_in_igcl = psr.get_status_via_igcl(panel, feature, pwr_src, igcl_power_plan)
        # PSR status after enable/disable and psr_enabled cannot be same as we are negating psr_enable -
        # - for enabling/disabling in each iteration
        if psr_enabled_in_igcl == psr_enabled:
            psr.report_gdhm('Failed %s PSR via IGCL' % {psr_stat_str_dict[not psr_enabled]}, feature)
            return False
        logging.info(f"\t\tPASS: PSR status = {not psr_enabled} after {psr_stat_str_dict[not psr_enabled]} PSR via IGCL")

        # Toggle the psr_enabled after get/set PSR to get the current status of PSR
        psr_enabled = psr_enabled_in_igcl

        # Verify PHY power state programming after PSR Disable/Enable
        # BSpec Link - https://gfxspecs.intel.com/Predator/Home/Index/49274
        # TODO : Remove the PHY Power state check from here after https://jira.devtools.intel.com/browse/VSDI-33417 is implemented
        if not psr_enabled:
            if adapter.name in ['DG2']:
                snps_power_state = MMIORegister.read("SNPS_PHY_REGISTER", "SNPS_PHY_TX_REQ_PORT_" + panel.transcoder, adapter.name)
                if snps_power_state.LaneDisablePowerStateInPsr != 0x03:
                    logging.error("Invalid SNPS Power state value")
                    return False
                logging.info("SNPS Power state value is programmed as expected after PSR Disable")
        else:
            if adapter.name in ['DG2']:
                snps_power_state = MMIORegister.read("SNPS_PHY_REGISTER", "SNPS_PHY_TX_REQ_PORT_" + panel.transcoder, adapter.name)
                if snps_power_state.LaneDisablePowerStateInPsr != 0x02:
                    logging.error("Invalid SNPS Power state value")
                    return False
                logging.info("SNPS Power state value is programmed as expected after PSR Enable")
        count += 1
    if feature > psr.UserRequestedFeature.PSR_1:
        man_trk = MMIORegister.read("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder,
                                             adapter.name, gfx_index=adapter.gfx_index)
        if man_trk.sf_partial_frame_enable == 0:
            logging.error("Mantrk not Enabled after PSR Enable")
            return False
    return True


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PsrEscape))
    test_environment.TestEnvironment.cleanup(test_result)
