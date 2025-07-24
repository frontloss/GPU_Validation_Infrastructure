#######################################################################################################################
# @file                 cabc.py
# @brief                This is a helper utility which encapsulates the verification functionalities used by CABC tests
# @author               Tulika
#######################################################################################################################
import ctypes
import logging
import random
from enum import IntEnum
from typing import List

from Libs.Core.wrapper import control_api_args, control_api_wrapper

from Libs.Core import display_power, registry_access
from Libs.Core.logger import gdhm, html
from Libs.Core.vbt import vbt
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Modules import dpcd, dut, workload
from Tests.PowerCons.Modules.dut_context import Adapter, Panel

optimization_params = dict()


##
# @brief    CABC features
class Feature:
    CABC = "CABC"
    DPST = "DPST"
    OPST = "OPST"
    NONE = "None"


##
# @brief    PanelType
class PanelType(IntEnum):
    LCD = 0
    OLED = 1


##
# @brief    CabcOption
class OsCabcOption(IntEnum):
    OFF = 0
    ALWAYS_ON = 1
    ON_BATTERY = 2


##
# @brief    Class for storing params feature wise
class CabcParams:
    ##
    # @brief       Initialize for CABC Params
    def __init__(self):
        self.feature_1 = FeatureParams()
        self.feature_2 = FeatureParams()


##
# @brief         Exposed object of CABC cmdline params
class FeatureParams:
    ##
    # @brief       Initialize Feature Params
    def __init__(self):
        self.name = None
        self.level = None


##
# @brief        This function set CABC and XPST level in the VBT
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

    if gfx_vbt.version < 257:
        logging.error(f"VBT version of XPST Expected: >257 and current:{gfx_vbt.version}")
        return False

    if feature == Feature.CABC:
        # Fetching the level for 4:7 bit TCON Aggressiveness
        if (gfx_vbt.block_44.AgressivenessProfile4[panel_index] & 0xf0) >> 4 == level - 1:
            logging.info(f"Current aggressiveness level is same as requested. (Level= {level}")
        else:
            gfx_vbt.block_44.AgressivenessProfile4[panel_index] = (level - 1 << 4)
            do_driver_restart = True

    elif feature in [Feature.DPST or Feature.OPST]:
        # Fetching the level for 0:3 bit XPST Aggressiveness
        if (gfx_vbt.block_44.AgressivenessProfile4[panel_index] & 0x0f) == level - 1:
            logging.info(f"Current aggressiveness level is same as requested. (Level= {level}")
        else:
            gfx_vbt.block_44.AggressivenessProfile3[panel_index] = level - 1
            do_driver_restart = True

    if do_driver_restart:
        if gfx_vbt.apply_changes() is False:
            logging.error(f"{feature} Feature changes failed in VBT")
            return False, do_driver_restart

    return True, do_driver_restart


##
# @brief        This function verify CABC and XPST status in the VBT and enable requested feature
# @param[in]    adapter
# @param[in]    panel
# @param[in]    feature_list
# @return       status, do_driver_restart (True/false) if driver restart is required
def enable_feature_in_vbt(adapter: Adapter, panel: Panel, feature_list: List[Feature]):
    do_driver_restart = False

    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    html.step_start(f"Enabling {feature_list} feature in VBT for {panel.port}")

    if gfx_vbt.version < 257:
        logging.error(f"FAIL: VBT version Expected: >257 and current:{gfx_vbt.version}")
        html.step_end()
        return False, do_driver_restart

    if Feature.CABC in feature_list:
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.TconBasedBacklightOptimization[0] & (1 << panel_index)) >> panel_index) is True:
            logging.info(f"{Feature.CABC} feature already enabled in VBT ")
            html.step_end()
        else:
            gfx_vbt.block_44.TconBasedBacklightOptimization[0] |= (1 << panel_index)
            do_driver_restart = True

    if Feature.DPST in feature_list:
        # Fetching the initial VBT status
        if gfx_vbt.block_44.PanelIdentification[panel_index] == PanelType.LCD:
            logging.info(f"{Feature.DPST} feature already enabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.PanelIdentification[panel_index] = PanelType.LCD
            do_driver_restart = True

    if Feature.OPST in feature_list:
        # Fetching the initial VBT status
        if gfx_vbt.block_44.PanelIdentification[panel_index] == PanelType.OLED:
            logging.info(f"{Feature.OPST} feature already enabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.PanelIdentification[panel_index] = PanelType.OLED
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
# @brief        This function verify CABC and XPST status in the VBT and disables the requested feature
# @param[in]    panel
# @param[in]    adapter
# @param[in]    feature_list
# @return       status, do_driver_restart (True/false) if driver restart is required
def disable_feature_in_vbt(adapter, panel, feature_list: List[Feature]):
    do_driver_restart = True
    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    html.step_start(f"Disabling {feature_list} feature in VBT for {panel.port}")
    if gfx_vbt.version < 257:
        logging.error(f"VBT version Expected: >257 and current:{gfx_vbt.version}")
        html.step_end()
        return False, do_driver_restart

    if Feature.CABC in feature_list:
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.TconBasedBacklightOptimization[0] & (1 << panel_index)) >> panel_index) is False:
            logging.info(f"{Feature.CABC} feature already disabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.TconBasedBacklightOptimization[0] &= (0 << panel_index)
            do_driver_restart = True

    if Feature.DPST in feature_list:
        # Fetching the initial VBT status
        if gfx_vbt.block_44.PanelIdentification[panel_index] == PanelType.LCD:
            logging.info(f"{Feature.DPST} feature already disabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.PanelIdentification[panel_index] = PanelType.LCD
            do_driver_restart = True

    if Feature.OPST in feature_list:
        # Fetching the initial VBT status
        if gfx_vbt.block_44.PanelIdentification[panel_index] == PanelType.OLED:
            logging.info(f"{Feature.OPST} feature already disabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.PanelIdentification[panel_index] = PanelType.OLED
            do_driver_restart = True

    if do_driver_restart:
        if gfx_vbt.apply_changes() is False:
            logging.error(f"{feature_list} Feature changes failed in VBT")
            html.step_end()
            return False, do_driver_restart

    html.step_end()
    return True, do_driver_restart


##
# @brief        This function verify and enable CABC co-existence status in the VBT
# @param[in]    panel
# @param[in]    adapter
# @return       status, do_driver_restart (True/false) if driver restart is required
def enable_coexistence_with_xpst(adapter, panel):
    do_driver_restart = True
    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    html.step_start(f"Enabling Co-Existence in VBT for {panel.port}")

    if gfx_vbt.version < 257:
        logging.error(f"VBT version Expected: >257 and current:{gfx_vbt.version}")
        html.step_end()
        return False, do_driver_restart

    # Fetching the initial VBT status
    if bool((gfx_vbt.block_44.TconBasedBacklightOptimizationCoExistenceWithXPST[0] & (
            1 << panel_index)) >> panel_index) is True:
        logging.info(f"Co-Existence already enabled in VBT ")
        html.step_end()
    else:
        gfx_vbt.block_44.TconBasedBacklightOptimizationCoExistenceWithXPST[0] |= (1 << panel_index)
        do_driver_restart = True

    if do_driver_restart:
        if gfx_vbt.apply_changes() is False:
            logging.error(f"Enabling Co-existence failed in VBT")
            html.step_end()
            return False, do_driver_restart

    html.step_end()
    return True, do_driver_restart


##
# @brief        This function verify and disable CABC co-existence status in the VBT
# @param[in]    panel
# @param[in]    adapter
# @return       status, do_driver_restart (True/false) if driver restart is required
def disable_coexistence_with_xpst(adapter, panel):
    do_driver_restart = True
    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    html.step_start(f"Disabling Co-Existence in VBT for {panel.port}")

    if gfx_vbt.version < 257:
        logging.error(f"VBT version Expected: >257 and current:{gfx_vbt.version}")
        html.step_end()
        return False, do_driver_restart

    # Fetching the initial VBT status
    if bool((gfx_vbt.block_44.TconBasedBacklightOptimizationCoExistenceWithXPST[0] & (
            1 << panel_index)) >> panel_index) is False:
        logging.info(f"Co-Existence already disabled in VBT")
        html.step_end()
    else:
        gfx_vbt.block_44.TconBasedBacklightOptimizationCoExistenceWithXPST[0] &= (0 << panel_index)
        do_driver_restart = True

    if do_driver_restart:
        if gfx_vbt.apply_changes() is False:
            logging.error(f"Disabling Co-existence failed in VBT")
            html.step_end()
            return False, do_driver_restart

    html.step_end()
    return True, do_driver_restart


##
# @brief       API to initialize CABC structure for IGCL
# @return      igcl_args
def __igcl_init_cabc_structure():
    display_power_ = display_power.DisplayPower()
    pwr_src = display_power_.get_current_powerline_status()
    igcl_pwr_src = 1 if pwr_src == display_power.PowerSource.DC else 0

    igcl_args = control_api_args.ctl_power_optimization_settings_t()
    igcl_args.Size = ctypes.sizeof(igcl_args)
    igcl_args.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.DPST.value
    igcl_args.PowerSource = igcl_pwr_src
    igcl_args.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
    return igcl_args


##
# @brief       Set call to set_power_ftr via Control Api
# @param[in]   feature class, Feature
# @param[in]   enable bool, to enable or disable
# @param[in]   level int, optimization level
# @return      igcl_args
def __create_igcl_set_args(feature: Feature, enable: bool, level: int):
    igcl_args = __igcl_init_cabc_structure()
    igcl_args.Enable = enable
    igcl_args.FeatureSpecificData.DPSTInfo.Level = level

    if feature == Feature.CABC:
        igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures = 2
    elif feature == Feature.DPST:
        igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures = 1
    elif feature == Feature.OPST:
        igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures = 4
    return igcl_args


##
# @brief       Set call to set parameters via Control Api
# @param[in]   panel object, Panel
# @param[in]   feature class, Feature
# @param[in]   enable bool, to enable or disable
# @param[in]   level int, optimization level
# @return      bool True or False, power capability for CABC
def igcl_set_power_settings(panel: Panel, feature: Feature, enable: bool, level: int):
    if feature == Feature.NONE:
        return None

    html.step_start(f"Setting {feature} feature Status= {enable} for {panel.port}")
    get_args = igcl_get_power_settings(panel)
    if get_args is False:
        return False

    feature_flag = control_api_args.ctl_power_optimization_dpst_flags_v.PANEL_CABC.value
    if feature == Feature.DPST:
        feature_flag = control_api_args.ctl_power_optimization_dpst_flags_v.BKLT.value
    elif feature == Feature.OPST:
        feature_flag = control_api_args.ctl_power_optimization_dpst_flags_v.OPST.value

    if feature_flag != (feature_flag & get_args.FeatureSpecificData.DPSTInfo.SupportedFeatures.value):
        logging.error(f"{feature} feature is not supported for {panel.port}")
        html.step_end()
        return False

    set_args = __create_igcl_set_args(feature, enable, level)

    if control_api_wrapper.set_dpst(set_args, panel.target_id) is False:
        logging.error(f"FAIL : IGCL Escape call to Set the power setting")
        html.step_end()
        return False

    logging.info(f"PASS : IGCL Escape call to Set the power setting")
    html.step_end()
    return True


##
# @brief       Get call to verify support via Control Api
# @param[in]   panel
# @return      bool True or False, power capability for CABC
def igcl_get_power_settings(panel: Panel):
    get_power_settings = __igcl_init_cabc_structure()
    if control_api_wrapper.get_dpst(get_power_settings, panel.target_id) is False:
        logging.error(f"FAIL : IGCL Escape call to Get the Power Settings")
        return False

    logging.info(f"PASS : IGCL Escape call to Get the Power Settings")
    return get_power_settings


##
# @brief       This function verifies panel support via Control Api
# @param[in]   panel object, Panel
# @param[in]   feature class, Feature
# @return      bool True or False
def is_feature_supported_in_igcl(panel: Panel, feature: Feature):
    if feature is None:
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

    if feature == Feature.CABC:
        panel_cabc_flag = control_api_args.ctl_power_optimization_dpst_flags_v.PANEL_CABC.value
        if panel_cabc_flag == (panel_cabc_flag & igcl_args.FeatureSpecificData.DPSTInfo.SupportedFeatures.value):
            logging.info(f"CABC is supported for {panel.port}")
            logging.info(
                f"CABC Status= {bool(panel_cabc_flag & igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value)}")
            html.step_end()
            return True

        logging.error(f"CABC is NOT supported for {panel.port}")
        html.step_end()
        return False

    if feature == Feature.DPST:
        dpst_flag = control_api_args.ctl_power_optimization_dpst_flags_v.BKLT.value
        if dpst_flag == (dpst_flag & igcl_args.FeatureSpecificData.DPSTInfo.SupportedFeatures.value):
            logging.info(f"DPST is supported for {panel.port}")
            logging.info(
                f"DPST status = {bool(dpst_flag & igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value)}")
            html.step_end()
            return True

    if feature == Feature.OPST:
        opst_flag = control_api_args.ctl_power_optimization_dpst_flags_v.OPST.value
        if opst_flag == (opst_flag & igcl_args.FeatureSpecificData.DPSTInfo.SupportedFeatures.value):
            logging.info(f"OPST is supported for {panel.port}")
            logging.info(
                f"OPST status = {bool(opst_flag & igcl_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value)}")
            html.step_end()
            return True

        logging.info(f"OPST is NOT supported for {panel.port}")
        return False
    return True


##
# @brief      This function verifies panel support for CABC by parsing specific DPCD values of the panel
# @param[in]  panel
# @return     bool True or False
def is_panel_supported(panel):
    if panel.hdr_caps.is_hdr_supported:
        return panel.hdr_caps.brightness_optimization_supported
    return panel.hdr_caps.is_aux_only_brightness and panel.hdr_caps.brightness_optimization_supported


##
# @brief     This function verify whether the Optimization Level is matching with the expected value via Control api
# @param[in] panel
# @param[in] expected_opt_level
# @return    bool True or False
def __verify_opt_level_in_igcl(panel, expected_opt_level):
    html.step_start(f"Verifying Optimization Level in IGCL")

    get_current_cabc_args = igcl_get_power_settings(panel)

    if get_current_cabc_args is False:
        logging.error(f"FAIL: IGCL Escape call for Get CABC failed for Target_ID {panel.target_id}")
        gdhm.report_driver_bug_pc(f"[BrightnessOptimization] IGCL Escape call is FAILED to get Power Settings")
        html.step_end()
        return False

    current_level = get_current_cabc_args.FeatureSpecificData.DPSTInfo.Level
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
# @param[in]  option
# @return     bool True or False
def __verify_opt_level_in_dpcd(panel, expected_level, option, pwr_src):
    html.step_start(f"Verifying Optimization Level in DPCD")

    offset_value = dpcd.EdpBrightnessOptimization(panel.target_id)
    optimization_strength = offset_value.optimization_strength

    expected_level = __get_expected_level(expected_level, pwr_src, option)

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
# @brief      This function verifies CABC via Control Api and in the DPCD 0x358
# @param[in]  adapter object, Adapter
# @param[in]  panel object, Panel
# @param[in]  feature class, Feature
# @param[in]  level int, optimization level
# @param[in]  skip_igcl_for_cabc bool, skip CABC if opst and cabc levels are different
# @param[in]  option enum, os option for OFF, ON_BATTERY, ALWAYS_ON
# @param[in]  pwr_src optional
# @param[in]    is_vesa_based True: Vesa, False: Custom
# @return     bool True or False
def verify(adapter: Adapter, panel: Panel, feature: Feature, level: int, skip_igcl_for_cabc: bool,
           option: OsCabcOption = None, pwr_src=display_power.PowerSource.DC, is_vesa_based=False):
    if feature is None:
        return True
    html.step_start(f"Verifying {feature} feature for {panel.port}", True)
    html.step_end()

    if feature == Feature.CABC:
        # In case OPST and CABC levels are different; Ex : CABC= L6 and OPST= L3,
        # IGCL call will always have XPST level due to existing bug
        if skip_igcl_for_cabc is False:
            if __verify_opt_level_in_igcl(panel, level) is False:
                return False
        if is_vesa_based:
            if __verify_cabc_opt_level_in_vesa_dpcd(panel, level, option, pwr_src) is False:
                return False
        else:
            if __verify_opt_level_in_dpcd(panel, level, option, pwr_src) is False:
                return False

    if feature == Feature.OPST:
        etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL)
        status = dpst.verify(adapter, panel, etl_file, feature=dpst.XpstFeature.OPST)
        if status and pwr_src == display_power.PowerSource.AC:
            return False
        if status is False and pwr_src == display_power.PowerSource.DC:
            return False

    return True


##
# @brief        Helper function to enable brightness based on content
# @param[in]    value : Enum OsCabcOption
# @return       None
def toggle_os_cabc_option(value: OsCabcOption):
    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                             reg_path=r"System\CurrentControlSet")
    registry_access.write(args=reg_args, reg_name="CABCOption", reg_type=registry_access.RegDataType.DWORD,
                          reg_value=value, sub_key=r"Control\GraphicsDrivers")


##
# @brief        Helper function to set Optimization level
# @param[in]    feature_to_enable : Enum Enable or Disable
# @param[in]    existing_level : Enum Enable or Disable
# @return       status, optimization level
def set_optimization_level(feature_to_enable, existing_level=False):
    level = None
    for adapter in dut.adapters.values():
        for panel in adapter.panels.values():
            get_args = igcl_get_power_settings(panel)
            if get_args is False:
                return False, None
            current_level = get_args.FeatureSpecificData.DPSTInfo.Level
            for f in feature_to_enable:
                if f == optimization_params[panel.port].feature_1.name:
                    if existing_level is True:
                        level = optimization_params[panel.port].feature_1.level
                    else:
                        max_value = 6 if f == Feature.CABC else 3
                        while True:
                            random_level = random.randint(1, max_value)
                            if random_level != current_level:
                                level = random_level
                                break
                    logging.info(f"Current Level to be set using IGCL: {level}")
                    if igcl_set_power_settings(panel, f, True, level) is False:
                        logging.error(f"FAILED to set Power settings with level {level}")
                        return False, None
                if f == optimization_params[panel.port].feature_2.name:
                    if existing_level is True:
                        level = optimization_params[panel.port].feature_2.level
                    else:
                        max_value = 6 if f == Feature.CABC else 3
                        while True:
                            random_level = random.randint(1, max_value)
                            if random_level != current_level:
                                level = random_level
                                break
                    logging.info(f"Current Level to be set using IGCL: {level}")
                    if igcl_set_power_settings(panel, f, True, level) is False:
                        logging.error(f"FAILED to set Power settings with level {level}")
                        return False, None
    return True, level


##
# @brief        Helper function to toggle power source
# @return       status, set_pwr_src
def toggle_power_source():
    display_power_ = display_power.DisplayPower()
    pwr_src = display_power_.get_current_powerline_status()
    set_pwr_src = display_power.PowerSource.DC
    if pwr_src == display_power.PowerSource.DC:
        set_pwr_src = display_power.PowerSource.AC
    return workload.change_power_source(set_pwr_src), set_pwr_src


##
# @brief      This function returns expected level as per power source and Os option
# @param[in]  expected_level
# @param[in]  option
# @return     expected_level
def __get_expected_level(expected_level, pwr_src, option=None):

    logging.debug(f"Verifying {expected_level}, {pwr_src}, {option}")

    # Expected level should be zero for AC mode with default OS Option
    if option is None and pwr_src == display_power.PowerSource.AC:
        expected_level = 0

    # Expected level should be zero for both AC and DC mode if OS option is OFF
    if option == OsCabcOption.OFF.name:
        if pwr_src in [display_power.PowerSource.DC, display_power.PowerSource.AC]:
            expected_level = 0

    # Expected level should be zero for AC mode if OS option is ON_BATTERY
    elif option == OsCabcOption.ON_BATTERY.name:
        if pwr_src == display_power.PowerSource.AC:
            expected_level = 0

    # Rest for all cases expected level should be as requested in test
    return expected_level


##
# @brief      This function verifies panel support for CABC by parsing Vesa DPCD values of the panel
# @param[in]  panel
# @return     bool True or False
def is_vesa_dpcd_supported_by_panel(panel):
    return panel.vesa_caps.is_variable_brightness_supported


##
# @brief      This function verifies if the specified optimization level has been successfully updated in the DPCD 0x730
# @param[in]  panel
# @param[in]  expected_level
# @param[in]  option
# @return     bool True or False
def __verify_cabc_opt_level_in_vesa_dpcd(panel, expected_level, option, pwr_src):
    html.step_start(f"Verifying Optimization Level in DPCD")

    offset_value = dpcd.EdpDisplayControl2(panel.target_id)
    optimization_strength = offset_value.VariableBrightnessStrength

    expected_level = __get_expected_level(expected_level, pwr_src, option)

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
# @brief        Helper function to set Optimization level in igcl for vesa Supported cabc level(1-3), OPST level (1-3)
# @param[in]    feature_to_enable : Enum Enable or Disable
# @param[in]    existing_level : Enum Enable or Disable
# @return       status, optimization level
def vesa_set_optimization_level_in_igcl(feature_to_enable, existing_level=False):
    level = None
    for adapter in dut.adapters.values():
        for panel in adapter.panels.values():
            get_args = igcl_get_power_settings(panel)
            if get_args is False:
                return False, None
            current_level = get_args.FeatureSpecificData.DPSTInfo.Level
            for f in feature_to_enable:
                if existing_level is True:
                    level = optimization_params[panel.port].f.level
                else:
                    while True:
                        random_level = random.randint(1, 3)
                        if random_level != current_level:
                            level = random_level
                            break
                logging.info(f"Current Level to be set using IGCL: {level}")
                if igcl_set_power_settings(panel, f, True, level) is False:
                    logging.error(f"FAILED to set Power settings with level {level}")
                    return False, None
    return True, level
