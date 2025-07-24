#######################################################################################################################
# @file                 elp.py
# @brief                This is a helper utility which encapsulates the verification functionalities used by the tests
# @author       Smitha B
#######################################################################################################################
import logging
from Libs.Core.wrapper import control_api_args
from Tests.Color.Common import common_utility, color_enums, color_properties
from Tests.Color.Common import color_igcl_escapes, color_escapes
from Tests.Color.Verification import feature_basic_verify
from Libs.Core.logger import gdhm


##
# @brief This function performs a Get VBT call to verify if ELP as already been enabled in the VBT; Otherwise enables it
# @param[in] gfx_index
# @param[in] gfx_vbt
# @param[in] port
# @param[in] enable_status
# @return bool True or False
def set_elp_feature_in_vbt(gfx_index, gfx_vbt, port, enable_status):
    status_str = "enabled" if enable_status else "disabled"
    panel_index = gfx_vbt.get_lfp_panel_type(port)
    logging.debug("Panel Index {0}".format(panel_index))
    ##
    # Fetching the initial VBT status for ELP
    logging.info(f"VBT Status of DPST - OPST - ELP before starting the test for PanelIndex {panel_index}")
    initial_vbt_status = common_utility.read_feature_status_in_vbt(gfx_vbt, "ELP", panel_index)

    if initial_vbt_status['ELP'] is enable_status:
        logging.info(f"ELP is already {status_str} in the VBT; Proceeding with the test for PanelIndex {panel_index}")
        return True

    logging.info(f"ELP is not {status_str} in the VBT; Updating VBT for PanelIndex {panel_index}")

    if common_utility.update_color_feature_status_in_vbt(gfx_index, gfx_vbt,panel_index,
                                                         feature="ELP", enable_status=enable_status) is False:
        return False

    current_vbt_status = common_utility.read_feature_status_in_vbt(gfx_vbt, "ELP", panel_index)
    if current_vbt_status['ELP'] is not enable_status:
        logging.error(f"FAILED to configure ELP in the VBT for PanelIndex {panel_index}")
        return False
    logging.info(f"Successfully configure ELP in VBT with {status_str} status")
    return True


##
# @brief This function performs a Get Call and verifies if the Optimization Level is matching with the expected value
# @param[in] target_id
# @param[in] expected_opt_level
# @return bool True or False
def get_elp_optimization_and_verify(target_id, expected_opt_level):
    status, get_current_elp_args = color_igcl_escapes.get_dpst_info(target_id)
    if status is False:
        logging.error("FAIL : IGCL Escape call for Get ELP failed for Target_ID {0}".format(target_id))
        gdhm.report_driver_bug_pc("IGCL Escape call for Get ELP failed for Target_ID {0}".format(target_id))
        return False

    if expected_opt_level != get_current_elp_args.FeatureSpecificData.DPSTInfo.Level:
        logging.error(
            "FAIL : Actual ELP Optimization Level {0} and Expected ELP Optimization Level {1} NOT matching".format(
                get_current_elp_args.FeatureSpecificData.DPSTInfo.Level, expected_opt_level))
        gdhm.report_driver_bug_pc("[ELP] Mismatch found between Actual and Expected ELP Optimization Level via IGCL")
        return False

    logging.info(
        "PASS : Expected ELP Optimization Level {0} and Actual ELP Optimization Level {1}".format(expected_opt_level,
                                                                                                  get_current_elp_args.FeatureSpecificData.DPSTInfo.Level))
    return True


##
# @brief Verify if the specified optimization level has been successfully updated in the DPCD 0x358
# @param[in] gfx_index
# @param[in] panel
# @param[in] port
# @param[in] expected_level
# @return bool True or False
def verify_opt_level_in_dpcd(gfx_index: str, panel, port: str, expected_level: int):
    dpcd_value_358 = color_escapes.fetch_dpcd_data(
        color_enums.EdpHDRDPCDOffsets.EDP_BRIGHTNESS_OPTIMIZATION.value, panel.display_and_adapterInfo)
    optimization_strength = common_utility.get_bit_value(dpcd_value_358, 5, 7)
    if optimization_strength != expected_level:
        logging.error(
            "FAIL : Requested Optimization Level {0} is NOT reflecting in the DPCD ;"
            " Actual value is {1} on Adapter {2} on {3} attached to pipe {4}".format(
                expected_level, optimization_strength, gfx_index, port, panel.pipe))
        gdhm.report_driver_bug_pc("[ELP] Requested optimization level is NOT reflecting in the DPCD")
        return False
    logging.info("Requested Optimization Level {0} is reflecting in the DPCD".format(expected_level))
    return True


##
# @brief Static function which helps in the mapping of the User Optimization levels to the levels in the DPCD
# @param[in] user_opt_level
# @return int expected_dpcd_level
def mapping_user_level_to_dpcd(user_opt_level):
    if user_opt_level == 0:
        expected_dpcd_level = 0
    elif user_opt_level == 1:
        expected_dpcd_level = 1
    elif user_opt_level == 2:
        expected_dpcd_level = 4
    elif user_opt_level == 3:
            expected_dpcd_level = 6
    else:
        logging.error("Invalid Optimization Level Requested")
        expected_dpcd_level = user_opt_level

    return expected_dpcd_level


##
# @brief Static function which helps in verifying the panel support for ELP by parsing specific DPCD values of the panel
# @param[in] display_and_adapterInfo
# @return bool True or False
def verify_panel_support_for_elp(context_args):
    num_of_elp_supportd_panels = 0
    for gfx_index, adapter in context_args.adapters.items():
        for port, panel in adapter.panels.items():
            # By checking Bit5 == 1 of DPCD address 0x341,
            # driver can identify that particular TCON can support brightness only using Aux
            # and Driver will apply brightness using Aux DPCD 0x354
            dpcd_value_341 = color_escapes.fetch_dpcd_data(color_enums.EdpHDRDPCDOffsets.EDP_HDR_CAPS_BYTE1.value,
                                                           panel.display_and_adapterInfo)
            brightness_optimization_support = common_utility.get_bit_value(dpcd_value_341, 5, 5)

            # By Checking Bit0 == 1 of DPCD address 0x342,
            # driver can identify if that panel support Brightness optimization(DPST)
            # and driver will program DPST strength in DPCD 0x358
            dpcd_value_342 = color_escapes.fetch_dpcd_data(
                color_enums.EdpHDRDPCDOffsets.EDP_HDR_TCON_CAP_FOR_AUX_BRIGHTNESS.value, panel.display_and_adapterInfo)
            tcon_support_for_aux = common_utility.get_bit_value(dpcd_value_342, 0, 0)

            ##
            # The Panel TCON needs to set both Brightness optimization support and Aux support
            # for the driver to apply brightness using Aux and to program Optimization strength
            if brightness_optimization_support and tcon_support_for_aux:
                logging.info(
                    "The Panel TCON support for Brightness Optimization : {0} and AUX for brightness control : {1}".format(
                        feature_basic_verify.BIT_MAP_DICT[
                            int(brightness_optimization_support)], feature_basic_verify.BIT_MAP_DICT[
                            int(tcon_support_for_aux)]))
                num_of_elp_supportd_panels += 1
                feature_caps = color_properties.FeatureCaps()
                feature_caps.ELPSupport = True
                ##
                # Dynamically adding FeatureCaps Attribute with HDRSupport as False for SDR Panels
                # to the Panel details in the context_args object
                setattr(context_args.adapters[gfx_index].panels[port], "FeatureCaps",
                        feature_caps)
            else:
                logging.error(
                    "The Panel TCON support for Brightness Optimization : {0} and AUX for brightness control : {1}! "
                    "Panel planning issue.".format(
                        feature_basic_verify.BIT_MAP_DICT[
                            int(brightness_optimization_support)], feature_basic_verify.BIT_MAP_DICT[
                            int(tcon_support_for_aux)]))
                gdhm.report_driver_bug_pc("[ELP] Verification failed for Panel TCON as Brightness Optimization : {0} and AUX: {1} is not supported"
                                        .format(feature_basic_verify.BIT_MAP_DICT[int(brightness_optimization_support)], 
                                        feature_basic_verify.BIT_MAP_DICT[int(tcon_support_for_aux)])
                                        )
    return num_of_elp_supportd_panels


##
# @brief Static function which helps in verifying the panel support for ELP by parsing specific DPCD values of the panel
# @param[in] display_and_adapterInfo
# @return bool True or False
def verify_power_caps_for_elp_support(target_id):
    ##
    # Performing a Get PowerCapability call
    pwr_ft = control_api_args.ctl_power_optimization_flags_v.DPST.value
    status, get_power_caps = color_igcl_escapes.get_power_caps(target_id, pwr_ft)
    if status is False:
        return False

    dpst_status, get_elp_args = color_igcl_escapes.get_dpst_info(target_id)
    if dpst_status is False:
        gdhm.report_driver_bug_pc("Get DPST Call via Control Library Failed for TargetId: {0}".format(target_id))
        return False

    logging.info("*** Supported Features in the GetPowerCaps ***")
    logging.info("PASS : Supported Feature is {0}".format(get_power_caps.SupportedFeatures))

    logging.info("***** Logging DPSTInfoStructure in GetPowerCaps Call *****")
    logging.info("Supported features {0}".format(get_elp_args.FeatureSpecificData.DPSTInfo.SupportedFeatures))
    logging.info("Enabled features {0}".format(get_elp_args.FeatureSpecificData.DPSTInfo.EnabledFeatures))

    ##
    # Verification of all the other parameters to be performed
    if get_elp_args.FeatureSpecificData.DPSTInfo.SupportedFeatures.value != control_api_args.ctl_power_optimization_dpst_flags_v.ELP.value:
        logging.error("ELP is not supported")
        gdhm.report_driver_bug_pc("[ELP] ELP is returned as not supported by IGCL")
        return False

    return True


##
# @brief Consolidated Static function which helps in verification of all the aspects specific to ELP.
#        Performs a Get IGCL call to verify the Level and also reads the DPCD to verify if the level is updated
# @param[in] gfx_index
# @param[in] panel
# @param[in] port
# @param[in] level
# @return bool True or False
def perform_elp_verification(gfx_index, panel, port, level):
    if get_elp_optimization_and_verify(panel.target_id, level) is False:
        return False

    ##
    # Invoke the verification function for verification of the DPCD values
    expected_dpcd_level = mapping_user_level_to_dpcd(level)
    if verify_opt_level_in_dpcd(gfx_index, panel, port, expected_dpcd_level) is False:
        return False

    return True
