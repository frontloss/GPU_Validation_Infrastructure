#######################################################################################################################
# @file                 brightness_optimization.py
# @brief                This is a helper utility which encapsulates the verification functionalities used by the tests
# @author               Tulika
#######################################################################################################################
import ctypes
import logging
from typing import List

from Libs.Core.wrapper import control_api_args, control_api_wrapper

from Libs.Core import display_power
from Libs.Core.vbt import vbt
from Libs.Core.logger import gdhm, html
from Libs.Feature.powercons import registry
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Modules import dpcd
from Tests.PowerCons.Modules.dut_context import Adapter, Panel

# DPCD optimization level mapping with IGCL optimization level
DPCD_IGCL_MAPPING = {1: 1, 2: 4, 3: 6}

optimization_params = dict()


##
# @brief    Brightness Optimization features
class Feature:
    APD = "APD"
    ELP = "ELP"
    OPST = "OPST"
    NONE = None


##
# @brief    Class for storing params feature wise
class BrtOptParams:
    ##
    # @brief       Initialize for Brightness Optimization Params
    def __init__(self):
        self.feature_1 = FeatureParams()
        self.feature_2 = FeatureParams()


##
# @brief         Exposed object of BRT cmdline params
class FeatureParams:
    ##
    # @brief       Initialize Feature Params
    def __init__(self):
        self.name = None
        self.level = None


##
# @brief        This function verify ELP and APD status in the VBT; If enabled nothing Otherwise enables it
# @param[in]    adapter
# @param[in]    panel
# @param[in]    feature
# @param[in]    level
# @return       status, do_driver_restart (True/false) if driver restart is required
def configure_level_in_vbt(adapter: Adapter, panel: Panel, feature: Feature, level: int):
    do_driver_restart = False
    if feature == Feature.NONE:
        return None, do_driver_restart

    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)

    if feature not in [Feature.ELP, Feature.APD]:
        logging.info(f"VBT enable changes not required for {feature}")
        return None, do_driver_restart

    if feature == Feature.ELP:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of ELP Expected: >247 and current:{gfx_vbt.version}")
            return False

        # Fetching the initial level for 4:7 bit
        # vbt level 0-1-2, driver level 1-2-3
        if (gfx_vbt.block_44.AgressivenessProfile2[panel_index] & 0xf0) >> 4 == level - 1:
            logging.info(f"Current aggressiveness level is same as requested. (Level= {level}")
            return None, do_driver_restart
        else:
            gfx_vbt.block_44.AgressivenessProfile2[panel_index] = (level - 1 << 4)
            do_driver_restart = True

    elif feature == Feature.APD:
        if gfx_vbt.version < 253:
            logging.error(f"VBT version of APD Expected: >253 and current:{gfx_vbt.version}")
            return False

        # Fetching the initial level for 0:3 bit
        # vbt level 0-1-2, driver level 1-2-3
        if (gfx_vbt.block_44.AggressivenessProfile3[panel_index] & 0x0f) == level - 1:
            logging.info(f"Current aggressiveness level is same as requested. (Level= {level}")
            return None, do_driver_restart
        else:
            gfx_vbt.block_44.AggressivenessProfile3[panel_index] = level - 1
            do_driver_restart = True

    if gfx_vbt.apply_changes() is False:
        logging.error(f"{feature} Feature changes failed in VBT")
        return False, do_driver_restart

    return True, do_driver_restart


##
# @brief        This function verify ELP and APD status in the VBT; If enabled nothing Otherwise enables it
# @param[in]    adapter
# @param[in]    panel
# @param[in]    feature_list
# @return       status, do_driver_restart (True/false) if driver restart is required
def enable_feature_in_vbt(adapter: Adapter, panel: Panel, feature_list: List[Feature]):
    do_driver_restart = False

    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    html.step_start(f"Enabling {feature_list} feature in VBT for {panel.port}")

    if Feature.ELP in feature_list:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of ELP Expected: >247 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.ELP[0] & (1 << panel_index)) >> panel_index) is True:
            logging.info(f"{Feature.ELP} feature already enabled in VBT ")
            html.step_end()
        else:
            gfx_vbt.block_44.ELP[0] |= (1 << panel_index)
            do_driver_restart = True

    if Feature.APD in feature_list:
        if gfx_vbt.version < 253:
            logging.error(f"VBT version of APD Expected: >253 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.APD[0] & (1 << panel_index)) >> panel_index) is True:
            logging.info(f"{Feature.APD} feature already enabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.APD[0] |= (1 << panel_index)
            do_driver_restart = True

    if Feature.OPST in feature_list:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of APD Expected: >247 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.OPST[0] & (1 << panel_index)) >> panel_index) is True:
            logging.info(f"{Feature.OPST} feature already enabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.OPST[0] |= (1 << panel_index)
            # With OPST enable, disable DPST in VBT
            gfx_vbt.block_44.DpstEnable[0] &= (0 << panel_index)
            do_driver_restart = True

    # apply VBT changes when any of the field is updated( i.e. do_driver_restart = True)
    if do_driver_restart:
        if gfx_vbt.apply_changes() is False:
            logging.error(f"{feature_list} Feature changes failed in VBT")
            html.step_end()
            return False, do_driver_restart

    html.step_end()
    return True, do_driver_restart


##
# @brief        This function verify ELP and APD status in the VBT; If enabled nothing Otherwise enables it
# @param[in]    panel
# @param[in]    adapter
# @param[in]    feature_list
# @return       status, do_driver_restart (True/false) if driver restart is required
def disable_feature_in_vbt(adapter, panel, feature_list: List[Feature]):
    do_driver_restart = True
    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    html.step_start(f"Disabling {feature_list} feature in VBT for {panel.port}")

    if Feature.ELP in feature_list:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of ELP Expected: >247 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.ELP[0] & (1 << panel_index)) >> panel_index) is False:
            logging.info(f"{Feature.ELP} feature already disabled in VBT")
            html.step_end()
            return None, do_driver_restart
        else:
            gfx_vbt.block_44.ELP[0] &= (0 << panel_index)
            do_driver_restart = True

    if Feature.APD in feature_list:
        if gfx_vbt.version < 253:
            logging.error(f"VBT version of APD Expected: >253 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.APD[0] & (1 << panel_index)) >> panel_index) is False:
            logging.info(f"{Feature.APD} feature already disabled in VBT")
            html.step_end()
            return None, do_driver_restart
        else:
            gfx_vbt.block_44.APD[0] &= (0 << panel_index)
            do_driver_restart = True

    if Feature.OPST in feature_list:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of APD Expected: >247 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.OPST[0] & (1 << panel_index)) >> panel_index) is False:
            logging.info(f"{Feature.OPST} feature already disabled in VBT")
            html.step_end()
            return None, do_driver_restart
        else:
            gfx_vbt.block_44.OPST[0] &= (0 << panel_index)
            # With OPST disable, Enable DPST
            gfx_vbt.block_44.DpstEnable[0] |= (1 << panel_index)
            do_driver_restart = True

    if gfx_vbt.apply_changes() is False:
        logging.error(f"{feature_list} Feature changes failed in VBT")
        html.step_end()
        return False, do_driver_restart

    html.step_end()
    return True, do_driver_restart


##
# @brief       Get call to get_power_ftr via Control Api
# @param[in]   pwr_ftr
# @return      bool True or False, power capability for ELP
def __create_igcl_get_args():
    igcl_args = control_api_args.ctl_power_optimization_settings_t()
    igcl_args.Size = ctypes.sizeof(igcl_args)
    igcl_args.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.DPST.value
    igcl_args.PowerSource = control_api_args.ctl_power_source_v.DC.value
    igcl_args.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
    return igcl_args


##
# @brief       Get call to get_power_ftr via Control Api
# @param[in]   pwr_ftr
# @return      bool True or False, power capability for ELP
def __create_igcl_set_args(feature: Feature, enable: bool, level: int):
    igcl_args = control_api_args.ctl_power_optimization_settings_t()
    igcl_args.Size = ctypes.sizeof(igcl_args)
    igcl_args.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.DPST.value
    igcl_args.Enable = enable
    igcl_args.FeatureSpecificData.DPSTInfo.Level = level
    igcl_args.PowerSource = control_api_args.ctl_power_source_v.DC.value
    igcl_args.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value

    if feature == Feature.ELP:
        igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures = 8
    elif feature == Feature.APD:
        igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures = 32
    elif feature == Feature.OPST:
        igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures = 4
    return igcl_args


##
# @brief       Set call to set ELP parameters via Control Api
# @param[in]   panel object, Panel
# @param[in]   feature class, Feature
# @param[in]   enable bool, to enable or disable
# @param[in]   level int, optimization level
# @return      bool True or False, power capability for ELP
def igcl_set_power_settings(panel: Panel, feature: Feature, enable: bool, level: int):
    if feature == Feature.NONE:
        return None

    html.step_start(f"Setting {feature} feature Status= {enable}, level= {level} for {panel.port}")
    get_args = igcl_get_power_settings(panel)
    if get_args is False:
        return False

    feature_flag = control_api_args.ctl_power_optimization_dpst_flags_v.ELP.value
    if feature == Feature.APD:
        feature_flag = control_api_args.ctl_power_optimization_dpst_flags_v.APD.value
    elif feature == Feature.OPST:
        feature_flag = control_api_args.ctl_power_optimization_dpst_flags_v.OPST.value

    if feature_flag != (feature_flag & get_args.FeatureSpecificData.DPSTInfo.SupportedFeatures.value):
        logging.error(f"\t{feature} feature is not supported for {panel.port}")
        html.step_end()
        return False

    current_status = get_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value & feature_flag
    current_level = get_args.FeatureSpecificData.DPSTInfo.Level
    logging.info(f"\t{feature} feature Current (Status= {feature_flag == current_status}, Level= {current_level})")

    set_args = __create_igcl_set_args(feature, enable, level)

    if control_api_wrapper.set_dpst(set_args, panel.target_id) is False:
        logging.error(f"\tFAIL : IGCL Escape call to Set the power setting")
        html.step_end()
        return False

    logging.info(f"\tPASS : IGCL Escape call to Set the power setting")
    html.step_end()
    return True


##
# @brief       Get call to verify support for ELP via Control Api
# @param[in]   panel
# @return      bool True or False, power capability for ELP
def igcl_get_power_settings(panel: Panel):
    get_power_settings = __create_igcl_get_args()
    if control_api_wrapper.get_dpst(get_power_settings, panel.target_id) is False:
        logging.error(f"FAIL : IGCL Escape call to Get the Power Settings")
        return False

    logging.info(f"PASS : IGCL Escape call to Get the Power Settings")
    return get_power_settings


##
# @brief       This function verifies panel support for BRT via Control Api
# @param[in]   panel object, Panel
# @param[in]   feature class, Feature
# @return      bool True or False
def is_feature_supported_in_igcl(panel: Panel, feature: Feature):
    if feature == Feature.NONE:
        return None

    html.step_start(f"Checking IGCL for {feature} feature support status for {panel.port}")

    global_optimization_flag = control_api_args.ctl_power_optimization_flags_v.DPST.value
    get_power_caps = control_api_args.ctl_power_optimization_caps_t()
    get_power_caps.Size = ctypes.sizeof(get_power_caps)
    if global_optimization_flag != (global_optimization_flag & get_power_caps.SupportedFeatures.value):
        logging.error("Global Power setting is not supported in IGCL")
        html.step_end()
        return False

    igcl_args = igcl_get_power_settings(panel)
    if igcl_args is False:
        html.step_end()
        return False

    if feature == Feature.ELP:
        elp_flag = control_api_args.ctl_power_optimization_dpst_flags_v.ELP.value
        if elp_flag == (elp_flag & igcl_args.FeatureSpecificData.DPSTInfo.SupportedFeatures.value):
            logging.info(f"\tELP is supported for {panel.port}")
            logging.info(f"\tELP Status= {bool(elp_flag & igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value)}")
            html.step_end()
            return True

        logging.error(f"\tELP is NOT supported for {panel.port}")
        html.step_end()
        return False

    if feature == Feature.APD:
        apd_flag = control_api_args.ctl_power_optimization_dpst_flags_v.APD.value
        if apd_flag == (apd_flag & igcl_args.FeatureSpecificData.DPSTInfo.SupportedFeatures.value):
            logging.info(f"\tAPD is supported for {panel.port}")
            logging.info(f"\tAPD status = {bool(apd_flag & igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value)}")
            html.step_end()
            return True

    if feature == Feature.OPST:
        opst_flag = control_api_args.ctl_power_optimization_dpst_flags_v.OPST.value
        if opst_flag == (opst_flag & igcl_args.FeatureSpecificData.DPSTInfo.SupportedFeatures.value):
            logging.info(f"\tOPST is supported for {panel.port}")
            logging.info(f"\tOPST status = {bool(opst_flag & igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value)}")
            html.step_end()
            return True

        logging.info(f"\tOPST is NOT supported for {panel.port}")
        return False
    return True


##
# @brief      This Function verifies panel support for BRT by parsing specific DPCD values of the panel
# @param[in]  panel
# @return     bool True or False
def is_panel_supported(panel):
    return panel.hdr_caps.is_aux_only_brightness and panel.hdr_caps.brightness_optimization_supported


##
# @brief        This function helps in the mapping of the BRT User Optimization levels to the levels in the DPCD
# @param[in]    user_opt_level
# @return
def map_igcl_level_with_dpcd(user_opt_level):
    if user_opt_level not in list(DPCD_IGCL_MAPPING.keys()):
        logging.error(f"No DPCD mapping found for IGCL Level= {user_opt_level}")
        return None

    dpcd_level = DPCD_IGCL_MAPPING[user_opt_level]
    logging.info(f"Optimization level for IGCL Level= {user_opt_level} is mapped with DPCD Level= {dpcd_level}")
    return dpcd_level


##
# @brief      Exposed API to enable complete TCON Backlight optimization via registry
# @param[in]  adapter object, Adapter
# @return     bool True is Successful, False is Failed or None if already disabled
def enable_tcon_bklt_optimization(adapter: Adapter):
    html.step_start(f"Enabling TCON Backlight Optimization for {adapter.name} via registry key")
    display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
    if display_pc.DisableTconBacklightOptimization == 0:
        logging.info("\tTcon BacklightOptimization is already enabled in registry")
        html.step_end()
        return None

    display_pc.DisableTconBacklightOptimization = 0
    status = display_pc.update(adapter.gfx_index)
    if status is False:
        logging.error("\tFAILED to Enable Tcon BacklightOptimization in registry")
        html.step_end()
        return False

    logging.info("\tSuccessfully Enabled Tcon BacklightOptimization in registry")
    html.step_end()
    return True


##
# @brief      Exposed API to disable complete TCON Backlight optimization via registry
# @param[in]  adapter object, Adapter
# @return     bool True is Successful, False is Failed or None if already disabled
def disable_tcon_bklt_optimization(adapter: Adapter):
    html.step_start(f"Disabling TCON Backlight Optimization for {adapter.name} via registry key")
    display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
    if display_pc.DisableTconBacklightOptimization == 1:
        logging.info("\tTcon BacklightOptimization is already disabled in registry")
        html.step_end()
        return None

    display_pc.DisableTconBacklightOptimization = 1
    status = display_pc.update(adapter.gfx_index)
    if status is False:
        logging.error("\tFAILED to Disable Tcon BacklightOptimization in registry")
        html.step_end()
        return False

    logging.info("\tSuccessfully Disabled Tcon BacklightOptimization in registry")
    return True


##
# @brief     This function verify whether the Optimization Level is matching with the expected value via Control api
# @param[in] panel
# @param[in] expected_opt_level
# @return    bool True or False
def __verify_opt_level_in_igcl(panel, expected_opt_level):
    html.step_start(f"Verifying Optimization Level in IGCL is same as Level {expected_opt_level}")

    get_current_elp_args = igcl_get_power_settings(panel)

    if get_current_elp_args is False:
        logging.error(f"FAIL: IGCL Escape call for Get ELP failed for Target_ID {panel.target_id}")
        gdhm.report_driver_bug_pc(f"[BrightnessOptimization] IGCL Escape call is FAILED to get Power Settings")
        html.step_end()
        return False

    current_level = get_current_elp_args.FeatureSpecificData.DPSTInfo.Level
    if expected_opt_level != current_level:
        logging.error(f"FAIL: Optimization Level NOT matched. Expected={expected_opt_level}, Actual= {current_level}")
        gdhm.report_driver_bug_pc(f"[BrightnessOptimization] Optimization Level NOT matched via IGCL")
        html.step_end()
        return False

    logging.info(f"PASS: Optimization Level matched. Expected={expected_opt_level}, Actual= {current_level}")
    html.step_end()
    return True


##
# @brief      This function verifies if the specified optimization level has been successfully updated in the DPCD 0x358
# @param[in]  panel
# @param[in]  expected_level
# @return     bool True or False
def __verify_opt_level_in_dpcd(panel, expected_level):
    html.step_start(f"Verifying Optimization Level in DPCD is same as Level {expected_level}")

    offset_value = dpcd.EdpBrightnessOptimization(panel.target_id)
    optimization_strength = offset_value.optimization_strength

    if optimization_strength != expected_level:
        logging.error(f"FAIL: Requested Optimization Level is NOT reflecting in the DPCD. "
                      f"Expected= {expected_level}, Actual= {optimization_strength}")
        gdhm.report_driver_bug_pc("[BrightnessOptimization] Requested optimization level is NOT reflecting in the DPCD")
        html.step_end()
        return False

    logging.info(f"Requested Optimization Level is updated in DPCD. "
                 f"Expected= {expected_level}, Actual= {optimization_strength}")
    html.step_end()
    return True


##
# @brief      This function verifies BRT via Control Api and in the DPCD 0x358
# @param[in]  adapter object, Adapter
# @param[in]  panel object, Panel
# @param[in]  feature class, Feature
# @param[in]  level int, optimization level
# @param[in]  skip_igcl_for_elp bool, skip elp if opst and elp levels are different
# @param[in]  pwr_src optional, PowerSource for using it in verification
# @return     bool True or False
def verify(adapter: Adapter, panel: Panel, feature: Feature, level: int, skip_igcl_for_elp: bool,
           pwr_src=display_power.PowerSource.DC):
    if feature == Feature.NONE:
        return True
    html.step_start(f"Verifying {feature} feature for {panel.port}", True)
    html.step_end()

    if feature in [Feature.ELP, Feature.APD]:
        if skip_igcl_for_elp is False:
            # Verify BRT via Control api.
            if __verify_opt_level_in_igcl(panel, level) is False:
                return False

        # Verify BRT with DPCD values
        expected_dpcd_level = map_igcl_level_with_dpcd(level)
        if expected_dpcd_level is None:
            return False

        # feature got disabled in AC mode
        if pwr_src == display_power.PowerSource.AC:
            expected_dpcd_level = 0

        if __verify_opt_level_in_dpcd(panel, expected_dpcd_level) is False:
            return False

    if feature in [Feature.OPST]:
        etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL)
        status = dpst.verify(adapter, panel, etl_file, feature=dpst.XpstFeature.OPST)
        if status and pwr_src == display_power.PowerSource.AC:
            return False
        if status is False and pwr_src == display_power.PowerSource.DC:
            return False

    return True
