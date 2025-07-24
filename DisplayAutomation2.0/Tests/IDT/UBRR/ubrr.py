#######################################################################################################################
# @file         ubrr.py
# @brief        APIs to enable, disable and verify UBRR
#
# @author       Vinod D S
#######################################################################################################################
import ctypes
import logging
from enum import IntEnum
from Libs.Core import etl_parser
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Tests.PowerCons.Modules import dpcd
from Tests.PowerCons.Modules.dut_context import Adapter, Panel
from Tests.PowerCons.Functional.PSR import psr


##
# @brief        Exposed object for UBRR types
class UbrrType(IntEnum):
    NONE = 0
    UBZRR = 1
    UBLRR = 2
    UBALL = 3


##
# @brief         Exposed object of UBRR status
class UbrrStatus(object):
    ##
    # @brief       Initializer for UbrrStatus instances
    def __init__(self):
        self.ub_zrr_supported = False
        self.ub_lrr_supported = False
        self.enabled = False
        self.enabled_type = UbrrType.NONE
        self.psr_disable_required = False

    ##
    # @brief       Function to get the string format of UbrrStatus object
    # @return      string representation of the UbrrStatus object
    def __repr__(self):
        return f"UbrrStatus (UbZrrSupported={self.ub_zrr_supported}, UbLrrSupported={self.ub_lrr_supported}, " \
               f"Enabled={self.enabled}, EnabledType={self.enabled_type.name}, " \
               f"PsrDisableRequired={self.psr_disable_required})"


##
# @brief        Exposed API to get UBRR status
# @param[in]    adapter - object of Adapter
# @param[in]    panel - object of Panel
# @return       Object of UbrrStatus if operation is successful, None otherwise
def status(adapter: Adapter, panel: Panel):
    logging.info(f"\tGetting UBRR status on {panel.port} on {adapter.name}")
    power_opt_caps = control_api_args.ctl_power_optimization_caps_t()
    power_opt_caps.Size = ctypes.sizeof(power_opt_caps)
    if control_api_wrapper.get_power_caps(power_opt_caps, panel.target_id) is False:
        logging.error(f"\t\tFAILED to get Power Optimization Caps via Control API on {panel.port}")
        return None
    logging.debug(f"\t\tPower Optimization Caps on {panel.port} - {power_opt_caps.SupportedFeatures}")
    lrr_support = power_opt_caps.SupportedFeatures.value & control_api_args.ctl_power_optimization_flags_v.LRR.value
    lrr_support = (lrr_support == control_api_args.ctl_power_optimization_flags_v.LRR.value)
    logging.info(f"\t\tUBRR Status : LRR support - {lrr_support}")

    ubrr_status = UbrrStatus()
    if lrr_support:
        power_opt_settings = control_api_args.ctl_power_optimization_settings_t()
        power_opt_settings.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.LRR.value
        power_opt_settings.Size = ctypes.sizeof(power_opt_settings)

        # Not checking the return type to avoid the noise during when PSR2 is supported, but not enabled
        psr.enable_disable_psr_via_igcl(panel, enable_psr=False)
        ret_val = control_api_wrapper.get_ubrr(power_opt_settings, panel.target_id)
        psr.enable_disable_psr_via_igcl(panel, enable_psr=True)

        if ret_val is False:
            logging.error(f"\t\tFAILED to get Power Optimization Setting via Control API on {panel.port}")
            return None
        logging.debug(f"\t\tPower Optimization Settings: "
                      f"SupportedLRRTypes= {power_opt_settings.FeatureSpecificData.LRRInfo.SupportedLRRTypes}, "
                      f"Enable= {power_opt_settings.Enable}, "
                      f"CurrentLRRTypes= {power_opt_settings.FeatureSpecificData.LRRInfo.CurrentLRRTypes}, "
                      f"PsrDisableRequired= {power_opt_settings.FeatureSpecificData.LRRInfo.bRequirePSRDisable}")

        ubzrr_bitmap = control_api_args.ctl_power_optimization_lrr_flags_v.UBZRR.value
        ublrr_bitmap = control_api_args.ctl_power_optimization_lrr_flags_v.UBLRR.value

        ubzrr_support = power_opt_settings.FeatureSpecificData.LRRInfo.SupportedLRRTypes.value & ubzrr_bitmap
        ubrr_status.ub_zrr_supported = (ubzrr_support == ubzrr_bitmap)

        ublrr_support = power_opt_settings.FeatureSpecificData.LRRInfo.SupportedLRRTypes.value & ublrr_bitmap
        ubrr_status.ub_lrr_supported = (ublrr_support == ublrr_bitmap)

        ubrr_status.enabled = power_opt_settings.Enable
        ubrr_status.psr_disable_required = power_opt_settings.FeatureSpecificData.LRRInfo.bRequirePSRDisable

        ubrr_status.enabled_type = UbrrType.NONE
        ubzrr_enabled = power_opt_settings.FeatureSpecificData.LRRInfo.CurrentLRRTypes.value & ubzrr_bitmap
        if ubzrr_enabled == ubzrr_bitmap:
            ubrr_status.enabled_type = UbrrType.UBZRR
        ublrr_enabled = power_opt_settings.FeatureSpecificData.LRRInfo.CurrentLRRTypes.value & ublrr_bitmap
        if ublrr_enabled == ublrr_bitmap:
            ubrr_status.enabled_type = UbrrType.UBLRR

    logging.info(f"\t\t{ubrr_status}")
    return ubrr_status


##
# @brief        Exposed API to enable UBZRR/ UBLRR
# @param[in]    adapter - object of Adapter
# @param[in]    panel - object of Panel
# @param[in]    ubrr_type - object of UBRR
# @return       True if operation is successful, False otherwise
def enable(adapter: Adapter, panel: Panel, ubrr_type: UbrrType):
    logging.info(f"\tEnabling UBRR {ubrr_type.name} on {panel.port} on {adapter.name}")
    if ubrr_type not in [UbrrType.UBZRR, UbrrType.UBLRR]:
        logging.error(f"\t\tWrong UBRR type {ubrr_type.name} requested to enable on {panel.port}")
        return False

    current_status = status(adapter, panel)
    if current_status is None:
        logging.error(f"\t\tFAILED to get UBRR status on {panel.port}")
        return False
    if current_status.enabled is True and current_status.enabled_type == ubrr_type:
        logging.info(f"\t\tRequested UBRR {ubrr_type.name} is already enabled on {panel.port}")
        return True

    if current_status.psr_disable_required:
        # Below this will return error if queries in D3 (During CS)
        # Currently no verification done when system is in D3, need to consider only if anything added
        if psr.enable_disable_psr_via_igcl(panel, enable_psr=False) is False:
            return False

    ret_status = True
    try:
        power_opt_settings = control_api_args.ctl_power_optimization_settings_t()
        power_opt_settings.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.LRR.value
        power_opt_settings.FeatureSpecificData.LRRInfo.CurrentLRRTypes = eval(
            "control_api_args.ctl_power_optimization_lrr_flags_v.%s.value" % ubrr_type.name)
        power_opt_settings.Enable = True
        power_opt_settings.Size = ctypes.sizeof(power_opt_settings)

        if control_api_wrapper.set_ubrr(power_opt_settings, panel.target_id) is False:
            logging.error(f"\t\tFAILED to set UBRR {ubrr_type.name} on {panel.port}")
            ret_status = False
            return False
        logging.info(f"\t\tUBRR is set successfully to {ubrr_type.name} on {panel.port}")

    finally:
        if current_status.psr_disable_required:
            if psr.enable_disable_psr_via_igcl(panel, enable_psr=True) is False:
                return False

    return ret_status


##
# @brief        Exposed API to disable UBZRR/ UBLRR
# @param[in]    adapter - object of Adapter
# @param[in]    panel - object of Panel
# @return       True if operation is successful, False otherwise
def disable(adapter: Adapter, panel: Panel):
    logging.info(f"\tDisabling UBRR on {panel.port} on {adapter.name}")
    current_status = status(adapter, panel)
    if current_status is None:
        logging.error(f"\t\tFAILED to get UBRR status on {panel.port}")
        return False
    if current_status.enabled is False and current_status.enabled_type == UbrrType.NONE:
        logging.info(f"\t\tUBRR is already disabled on {panel.port}")
        return True
    logging.info(f"\t\tCurrently enabled UBRR - {current_status.enabled_type.name}")

    if current_status.psr_disable_required:
        if psr.enable_disable_psr_via_igcl(panel, enable_psr=False) is False:
            return False

    ret_status = True
    try:
        power_opt_settings = control_api_args.ctl_power_optimization_settings_t()
        power_opt_settings.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.LRR.value
        power_opt_settings.FeatureSpecificData.LRRInfo.CurrentLRRTypes = eval(
            "control_api_args.ctl_power_optimization_lrr_flags_v.%s.value" % current_status.enabled_type.name)
        power_opt_settings.Enable = False
        power_opt_settings.Size = ctypes.sizeof(power_opt_settings)

        if control_api_wrapper.set_ubrr(power_opt_settings, panel.target_id) is False:
            logging.error(f"\t\tFAILED to disable UBRR {current_status.enabled_type.name} on {panel.port}")
            ret_status = False
            return False
        logging.info(f"\t\tUBRR {current_status.enabled_type.name} is disabled successfully on {panel.port}")

    finally:
        if current_status.psr_disable_required:
            if psr.enable_disable_psr_via_igcl(panel, enable_psr=True) is False:
                return False

    return ret_status


##
# @brief        Exposed API to verify UBRR
# @param[in]    adapter - object of Adapter
# @param[in]    panel - object of Panel
# @param[in]    etl_file String
# @param[in]    ubrr_type - object of UBRR
# @param[in]    negative Boolean - True if UBRR should not work, False otherwise
# @return       True if operation is successful, False otherwise
def verify(adapter: Adapter, panel: Panel, etl_file: str, ubrr_type: UbrrType, negative=False):
    etl_parser_config = etl_parser.EtlParserConfig()
    etl_parser_config.dpcdData = 1
    if etl_parser.generate_report(etl_file, etl_parser_config) is False:
        logging.error(f"\tFAILED to generate EtlParser report {etl_file}")
        return False
    logging.info(f"\tSuccessfully generated EtlParser report for {etl_file}")

    dpcd_data = etl_parser.get_dpcd_data(dpcd.Offsets.ALRR_UBRR_CONFIG, is_write=True)
    if dpcd_data is None:
        if negative is True:
            logging.debug("\tNo UBRR DPCD programming found which is expected in negative case")
            return True
        logging.error("\tNo UBRR DPCD programming found which is not expected")
        return False

    if negative is True:
        logging.error("\tUBRR DPCD programming found which is not expected in negative case")
        return False

    status_val = True
    for dpcd_entry in dpcd_data:
        # Convert from byte to little indian uint8
        b = bytearray.fromhex(dpcd_entry.Data.replace('-', ''))
        dpcd_val = int.from_bytes(b, byteorder='little')
        ubrr_config_dpcd = dpcd.AlrrUbrrConfig(panel.target_id, dpcd_val)
        if ubrr_config_dpcd.enable_ubrr == dpcd.UbrrStatus.UBRR_DISABLE and ubrr_type == UbrrType.NONE:  # Disable
            logging.debug(f"\tUBRR programmed to disable in DPCD for port {panel.port} on {adapter.name}")
        elif ubrr_config_dpcd.enable_ubrr == dpcd.UbrrStatus.UBZRR_ENABLE and ubrr_type == UbrrType.UBZRR:  # UB-ZRR
            logging.debug(f"\tUBRR programmed to enable UBZRR in DPCD for port {panel.port} on {adapter.name}")
        elif ubrr_config_dpcd.enable_ubrr == dpcd.UbrrStatus.UBLRR_ENABLE and ubrr_type == UbrrType.UBLRR:  # UB-LRR
            logging.debug(f"\tUBRR programmed to enable UBLRR in DPCD for port {panel.port} on {adapter.name}")
        else:
            logging.error(f"\tMismatch seen in UBRR programming in DPCD Status={ubrr_config_dpcd.enable_ubrr}, "
                          f"Type={'DISABLE' if ubrr_type == UbrrType.NONE else ubrr_type.name}")
            status_val = False
    return status_val
