######################################################################################################
# @file         color_igcl_escapes.py
# @brief        Contains APIs which interfaces between the test and the IGCL wrapper
#               1.get_lace_config
#               2.set_lace_config
#               3.get_power_caps
#               4.get_dpst_info
#               5.set_dpst_info
#               6.get_current_elp_opt_level
#               7.set_igcl_color_feature
#               8.get_color_capability
# @author       Vimalesh D, Smitha B
######################################################################################################
import ctypes
import logging
from Libs.Core.wrapper.control_api_args import *
from Libs.Core.wrapper import control_api_args, control_api_wrapper

from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Tests.Color.Common import color_igcl_wrapper
from Libs.Core.logger import gdhm
from Tests.Color.Verification import feature_basic_verify


def get_lace_config(operation_type, disp_adapter):
    argsGetLaceArgs = control_api_args.ctl_lace_config_t()
    argsGetLaceArgs.Size = ctypes.sizeof(argsGetLaceArgs)
    logging.info(argsGetLaceArgs.Size)
  
    if operation_type == 0:
        argsGetLaceArgs.OpTypeGet = control_api_args. \
            ctl_lace_get_operation_code_type_v.CTL_OPERATION_QUERY_CURRENT.value
    if operation_type == 1:
        argsGetLaceArgs.OpTypeGet = control_api_args. \
            ctl_lace_get_operation_code_type_v.CTL_OPERATION_QUERY_DEFAULT.value
    if operation_type == 2:
        argsGetLaceArgs.OpTypeGet = control_api_args. \
            ctl_lace_get_operation_code_type_v.CTL_OPERATION_QUERY_CAPABILITY.value

    control_api_wrapper.get_lace(argsGetLaceArgs, disp_adapter)


def set_lace_config(trigger_type, set_operation, aggr_percent, disp_adapter):
    SetLaceConfigSettings = control_api_args.ctl_lace_config_t()
    SetLaceConfigSettings.Size = ctypes.sizeof(SetLaceConfigSettings)
    SetLaceConfigSettings.Enabled = True
    SetLaceConfigSettings.Version = 0
    if int(set_operation) == 0:
        SetLaceConfigSettings.OpTypeSet = control_api_args. \
            ctl_lace_set_operation_code_type_v.CAPI_OPERATION_RESTORE_DEFAULT
    if int(set_operation) == 1:
        SetLaceConfigSettings.OpTypeSet = control_api_args.ctl_lace_set_operation_code_type_v.CAPI_OPERATION_SET_CUSTOM

    if int(
            trigger_type) == control_api_args.ctl_lace_operation_mode_type_v.CTL_LACE_TRIGGER_FLAG_FIXED_AGGRESSIVENESS.value:
        # Fixed Aggr Mode

        SetLaceConfigSettings.Trigger = control_api_args. \
            ctl_lace_operation_mode_type_v.CTL_LACE_TRIGGER_FLAG_FIXED_AGGRESSIVENESS
        SetLaceConfigSettings.LaceConfig.FixedAggressivenessLevelPercent = aggr_percent

    elif trigger_type == control_api_args.ctl_lace_operation_mode_type_v.CTL_LACE_TRIGGER_FLAG_AMBIENT_LIGHT.value:
        SetLaceConfigSettings.Trigger = control_api_args. \
            ctl_lace_operation_mode_type_v.CTL_LACE_TRIGGER_FLAG_AMBIENT_LIGHT

    if control_api_wrapper.set_lace(SetLaceConfigSettings, disp_adapter):
        logging.info("Pass: set lace control api wrapper call")
        return True
    else:
        return False


def get_wireformat_config(disp_adapter):
    argsGetSetWireFormat = control_api_args.ctl_get_set_wireformat()
    argsGetSetWireFormat.Size = ctypes.sizeof(argsGetSetWireFormat)

    argsGetSetWireFormat.Operation = control_api_args.ctl_wire_format_operation_type_v.WIRE_FORMAT_GET.value

    control_api_wrapper.get_wireformat(argsGetSetWireFormat, disp_adapter)

    return argsGetSetWireFormat


def set_wireformat_config(color_model, color_depth, disp_adapter):
    SetWireFormatConfigSettings = control_api_args.ctl_get_set_wireformat()
    SetWireFormatConfigSettings.Size = ctypes.sizeof(SetWireFormatConfigSettings)
    SetWireFormatConfigSettings.Operation = control_api_args.ctl_wire_format_operation_type_v.WIRE_FORMAT_SET.value
    SetWireFormatConfigSettings.WireFormat.ColorModel = color_model
    SetWireFormatConfigSettings.WireFormat.ColorDepth = color_depth
    control_api_wrapper.set_wireformat(SetWireFormatConfigSettings, disp_adapter)
    return SetWireFormatConfigSettings


def get_power_caps(target_id, pwr_ft):
    get_power_caps = color_igcl_wrapper.prepare_igcl_args_for_power_caps()
    if control_api_wrapper.get_power_caps(get_power_caps, target_id) is False:
        logging.error("FAIL: Get Feature support via Control Library failed")
        gdhm.report_driver_bug_os("FAILED to get PowerCaps via IGCL")
        return False, get_power_caps

    ##
    # Verification of the Capability for DPST
    if (get_power_caps.SupportedFeatures and pwr_ft) is False:
        logging.error("FAIL : Requested feature is not Supported")
        gdhm.report_driver_bug_os("Requested feature is not Supported Expected: {0} Actual: {1}"
                                  .format(pwr_ft, get_power_caps.SupportedFeatures))
        return False, get_power_caps

    return True, get_power_caps


def get_dpst_info(target_id):
    ##
    # Prepare the parameters to perform a Get call to verify support for ELP from IGCL
    status = True
    get_elp_args = color_igcl_wrapper.prepare_igcl_get_args_for_elp()
    if control_api_wrapper.get_dpst(get_elp_args, target_id) is False:
        logging.error("Get DPST Call Failed")
        status = False

    return status, get_elp_args


def set_dpst_info(level, target_id):
    status = True
    set_elp_optimization_args = color_igcl_wrapper.prepare_igcl_set_args_for_elp(level, True)

    if control_api_wrapper.set_dpst(set_elp_optimization_args, target_id) is False:
        logging.error(
            "FAIL : IGCL Escape call to Set the ELP optimization level to {0} failed".format(level))
        status = False

    logging.info("PASS : IGCL Escape call to Set the ELP optimization level to {0} is successful".format(
        level))
    return status


##
# @brief Static function used internally in the Base class to fetch the current
# @param[in] target_id
# @return int The ELP optimization level returned by IGCL
def get_current_elp_opt_level(target_id):
    get_power_settings = color_igcl_wrapper.prepare_igcl_get_args_for_elp()
    control_api_wrapper.get_dpst(get_power_settings, target_id)
    return get_power_settings.FeatureSpecificData.DPSTInfo.Level


##
# @brief        Wrapper API to Set Pixel Transformation (Set the Color Blocks)
# @param[in]    igcl_set_args - Pixel Transformation Pipe Config Args
# @param[in]    igcl_get_caps - Pixel Transformation Block Config Args
# @param[in]    target_id - target-id / display_and_adapter_info structure
# @param[in]    user_req_blk - Number of blocks to be set
# @param[in]    mode - to identify whether it is SDR/HDR/WCG modes
# @return       result - True if get call is successfully, False otherwise
def set_igcl_color_feature(igcl_set_args, igcl_get_caps, target_id, user_req_blk, mode) -> bool:
    if control_api_wrapper.set_igcl_color_feature(igcl_set_args, igcl_get_caps, target_id,
                                                  user_req_blk, mode) is False:

        logging.error("FAIL : Pixel Transformation set is unsuccessful")
        gdhm.report_driver_bug_os("Set Pixel Transformation is unsuccessful for TargetId: {0}"
                                  .format(target_id))
        return False
    else:
        logging.info("PASS : Pixel Transformation set is successful")
        return True


##
# @brief        Wrapper API to fetch the capabilities supported by a panel in a specific mode
# @param[in]    igcl_args_get_caps - Pixel Transformation Pipe Config Args
# @param[in]    display_and_adapter_info - Display and Adapter Info
# @return       result - True if get call is successfully, False otherwise
def get_color_capability(igcl_args_get_caps, display_and_adapter_info):
    if control_api_wrapper.get_color_capability(igcl_args_get_caps, display_and_adapter_info) is False:
        return False
    return True


##
# @brief        Wrapper API to perform a restore default of all the blocks
# @param[in]    igcl_esc_restore_default - Pixel Transformation Pipe Config Args
# @param[in]    target_id - Target ID of the display
# @return       result - True if restore default call is successfully, False otherwise
def perform_restore_default(igcl_esc_restore_default, target_id):
    if control_api_wrapper.restore_default(igcl_esc_restore_default, target_id) is False:
        return False
    return True


##
# @brief        Exposed API to enable/disable PSR via IGCL
# @param[in]    panel - object of Panel
# @param[in]    enable_psr - Boolean
# @return       True for success, False for failed
def enable_disable_psr_via_igcl(target_id, port, enable):
    psr_pwr_opt_settings = control_api_args.ctl_power_optimization_settings_t()
    psr_pwr_opt_settings.Size = ctypes.sizeof(psr_pwr_opt_settings)
    psr_pwr_opt_settings.Enable = enable
    psr_pwr_opt_settings.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.PSR.value
    if control_api_wrapper.set_psr(psr_pwr_opt_settings, target_id) is False:
        logging.error(f"\t\tFAILED to {'enable' if enable else 'disable'} PSR via IGCL on {port}")
        return False
    logging.info(f"\t\tPSR {'enabled' if enable else 'disabled'} successfully via IGCL on {port}")
    return True


##
# @brief        Exposed API to get PSR status via IGCL
# @param[in]    target_id Target_ID
# @param[in]    expected_status boolean
# @return       True if Pass, False if Failed based on Expected_status
def get_psr_status_via_igcl(target_id, expected_status: bool = False):
    get_psr = control_api_args.ctl_power_optimization_settings_t()
    get_psr.Size = ctypes.sizeof(get_psr)
    get_psr.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.PSR.value

    if not control_api_wrapper.get_psr(get_psr, target_id):
        logging.error("\t\tFail: Get PSR status via IGCL")
        return False
    logging.info(f"PSR from IGCL : Version = {get_psr.FeatureSpecificData.PSRInfo.PSRVersion}")
    logging.info(f"PSR Status = {get_psr.Enable} ")
    if get_psr.Enable != expected_status:
        return False
    return True


##
# @brief        Exposed API to get 3DLUT Enable/Disable status via IGCL
def enable_verify_3d_lut_via_igcl(adapter, gfx_index, panel, bin_file_path: str):
    
                # The dictionary is designed as it uses existing igcl color escape api for preparing the args
                igcl_color_ftr_data = {'3DLUT': None, 'DGLUT': None, 'CSC': None, 'GLUT': None, 'oCSC': None}
                igcl_color_ftr_index = {'3DLUT': None, 'DGLUT': None, 'CSC': None, 'GLUT': None, 'oCSC': None}
                
                user_req_color_blk = color_igcl_wrapper.IgclColorBlocks.HW3DLUT.value
                
                igcl_get_caps = color_igcl_wrapper.prepare_igcl_color_esc_args_for_get_caps()
                get_color_capability(igcl_get_caps, panel.target_id)
                
                hw_3dlut_supported = False
                
                # Check if 3DLut block exists
                for index in range(0, igcl_get_caps.NumBlocks):
                    if igcl_get_caps.pBlockConfigs[index].BlockType.value == control_api_args.ctl_pixtx_block_type_v._3D_LUT.value:
                        hw_3dlut_supported = True
                        logging.info("PASS : IGCL Support for {0} has been reported by the driver on {1} connected to "
                                     "Pipe {2} on adapter {3} ".format(control_api_args.ctl_pixtx_block_type_v._3D_LUT.name, panel.connector_port_type, panel.pipe, gfx_index))
                
                if hw_3dlut_supported is False:
                    logging.error("FAIL : IGCL Support for {0} has not been reported by the driver on {1} connected "
                                  "to Pipe {2} on adapter {3} "
                                  .format(color_igcl_wrapper.IgclColorBlocks(user_req_color_blk).name,
                                          panel.connector_port_type, panel.pipe, gfx_index))
                    return False
                if "R.BIN" in bin_file_path:
                    sample_lut_name = "NO_RED"
                elif "G.BIN" in bin_file_path:
                    sample_lut_name = "NO_GREEN"
                else:
                    sample_lut_name = "NO_BLUE"
                
                igcl_color_ftr_data['3DLUT'] = str(sample_lut_name)
                igcl_set_args = color_igcl_wrapper.prepare_igcl_color_escapes_args_for_set(gfx_index, adapter.platform,
                                                                                           panel.connector_port_type,
                                                                                           panel.pipe,
                                                                                           igcl_get_caps,
                                                                                           user_req_color_blk,
                                                                                           1,
                                                                                           igcl_color_ftr_data,
                                                                                           igcl_color_ftr_index)
                argsLutConfig = color_igcl_wrapper.prepare_igcl_set_args_for_3dlut(igcl_get_caps,
                                                                                   igcl_color_ftr_index['3DLUT'])
                igcl_set_args.pBlockConfigs = igcl_get_caps.pBlockConfigs
                if control_api_wrapper.set_3dlut(igcl_set_args, argsLutConfig, panel.target_id):
                    logging.info("Set HW_3DLUT feature is successful")
                    status = True
                else:
                    logging.error("Set HW_3DLUT feature is failure")
                    return False
                
                return status
