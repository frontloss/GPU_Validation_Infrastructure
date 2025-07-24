#######################################################################################################################
# @file         pc_external.py
# @brief        Contains  user interface for external feature verification
#
#
# @author       Chandrakanth Reddy
#######################################################################################################################

import importlib
import logging
import os
import platform
import re
import subprocess
import time
from Libs.Core import enum, flip, driver_escape, registry_access, display_essential, etl_parser, system_utility
from Libs.Core import winkb_helper as kb
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config import configure_hdr
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.flip import MPO
from Libs.Core.logger import etl_tracer
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import control_api_args
from Libs.Core.wrapper.driver_escape_args import DppHwLutInfo, DppHwLutOperation
from Tests.Color.Common import color_igcl_escapes
from Tests.Color.HDR.OSHDR import os_hdr_verification
from Tests.Planes.Common import planes_verification
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister
from Libs.Feature.presi.presi_crc import start_plane_processing
from Tests.Planes.Common import planes_helper

display_config_ = display_config.DisplayConfiguration()

__BIN_PATH = r"Color\\Hw3DLUT\\CustomLUT"
__DIRECTX_APP_LOCATION = os.path.join(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "PowerCons"),
                                      "MultiAnimation")
__directx_args_dict = {
    'fullscreen': '-fullscreen',
    'windowed': '',
    'vsync': '-forcevsync:1',
    'async': '-forcevsync:0'
}

PIXEL_FORMAT = {
    "PIXEL_FORMAT_B8G8R8A8": (4, 8),
    "PIXEL_FORMAT_NV12YUV420": (15, 2),
    "PIXEL_FORMAT_R16G16B16X16F": (12, 12),
    "PIXEL_FORMAT_YUV422": (16, 0),
    "PIXEL_FORMAT_YUV444_8": (24, 16)
}


##
# @brief        helper function to extract bits from value
# @param[in]    value, int
# @param[in]    start, int , starting bit position for extracting value
# @param[in]    end , int ,  ending bit position for extracting value
# @return       True if enabled else False
def __get_value(value, start, end):
    ret_value = (value << (31 - end)) & 0xFFFFFFFF
    ret_value = (ret_value >> (31 - end + start)) & 0xFFFFFFFF
    return ret_value


##
# @brief        This is a helper function to enable/disable LACE
# @param[in]    adapter Adapter Object
# @param[in]    panel Panel Object
# @param[in]    enable boolean register data
# @param[in]    gfx_index String, adapter index
# @return       True if enabled else False
def enable_disable_lace(adapter, panel, enable, gfx_index='gfx_0'):
    status_str = "Enable" if enable else "Disable"
    if adapter.name.upper() not in machine_info.PRE_GEN_13_PLATFORMS:
        # Use IGCL to enable/disable LACE for Post-Gen13 platforms
        if __start_capture() is False:
            return False, None
        aggr_percent = 100 if enable else 0
        trigger_type = control_api_args.ctl_lace_operation_mode_type_v.CTL_LACE_TRIGGER_FLAG_FIXED_AGGRESSIVENESS.value
        set_operation = control_api_args.ctl_lace_set_operation_code_type_v.CAPI_OPERATION_SET_CUSTOM
        logging.info(f"{status_str} LACE via IGCL")
        if color_igcl_escapes.set_lace_config(trigger_type, set_operation, aggr_percent, panel.target_id) is False:
            logging.error(f"Failed to {status_str} LACE via IGCL")
            return False, None
        time.sleep(5)

        etl_file = __end_capture(f"During_LACE_{status_str}")
        return True, etl_file

    lux = 1000
    aggr_level = 1
    val = 1 if enable else 0
    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.LOCAL_MACHINE, r"SOFTWARE\Intel\Display")
    regkey_write_status = registry_access.write(reg_args, "BKPDisplayLACE", registry_access.RegDataType.DWORD, val, r"igfxcui\MISC")
    if regkey_write_status is False:
        logging.error(f"Failed to update RegKey BKPDisplayLACE with value {val}")
        gdhm.report_test_bug_os(f"[OsFeatures][LACE] Failed to update RegKey BKPDisplayLACE with value {val} in adapter {adapter.gfx_index}")

        return False, None
    logging.info(f"Successfully updated RegKey BKPDisplayLACE with value {val}")
    driver_restart_status, is_reboot_required = display_essential.restart_gfx_driver()
    if driver_restart_status is False:
        logging.error("FAILED to restart display driver")
        return False, None
    if __start_capture() is False:
        return False, None
    if enable:
        logging.info(f"Enabling LACE on PIPE_{panel.pipe} with LUX= {lux} and Moderate Aggressiveness level")
        if driver_escape.als_aggressiveness_level_override(panel.target_id, lux, True, aggr_level, True) is False:
            logging.error("\tFAILED to set LUX and Aggressiveness level")
            return False, None
        time.sleep(10)
    etl_file = __end_capture(f"During_LACE_{status_str}")
    return True, etl_file


##
# @brief        Verify LACE is enabled in driver
# @param[in]    adapter object
# @param[in]    panel object
# @return       True if enabled else False
def get_lace_status(adapter, panel):
    dplc_ctl_reg_value = MMIORegister.read('DPLC_CTL_REGISTER', 'DPLC_CTL' + '_' + panel.pipe, common.PLATFORM_NAME,
                                           gfx_index=adapter.gfx_index)
    return dplc_ctl_reg_value.function_enable == 1


##
# @brief        Verify 3D LUT is enabled in driver
# @param[in]    adapter object
# @param[in]    panel object
# @return       status, etl_file tuple, True if enabled else False with etl_file
def verify_3dlut(adapter, panel):
    driver_interface_ = driver_interface.DriverInterface()
    hw_3d_lut_status = False
    hw_lut_buffer_status = False

    # start etl_capture
    if __start_capture() is False:
        return False, None
    bin_file = "CustomLUT_no_R.bin"
    bin_file_path = os.path.join(__BIN_PATH, bin_file)
    path = os.path.join(test_context.SHARED_BINARY_FOLDER, bin_file_path)
    cui_dpp_hw_lut_info = DppHwLutInfo(panel.target_id, DppHwLutOperation.UNKNOWN.value, 0)
    result, cui_dpp_hw_lut_info = driver_escape.get_dpp_hw_lut(adapter.gfx_index, cui_dpp_hw_lut_info)
    if result is False:
        logging.error(f'Escape call failed: get_dpp_hw_lut() for {panel.target_id}')
        return False, None
    logging.info(f"Color depth:{cui_dpp_hw_lut_info.depth}")

    cui_dpp_hw_lut_info = DppHwLutInfo(panel.target_id, DppHwLutOperation.APPLY_LUT.value, cui_dpp_hw_lut_info.depth)
    if cui_dpp_hw_lut_info.convert_lut_data(path) is False:
        logging.error(f'Invalid bin file path provided : {path}!')
        return False, None
    result = driver_escape.set_dpp_hw_lut(adapter.gfx_index, cui_dpp_hw_lut_info)
    if result is False:
        logging.error(f'Escape call failed : set_dpp_hw_lut() for {panel.target_id}')
        return False, None

    lut_3d_ctl_reg = 'LUT_3D_CTL' + '_' + panel.pipe
    instance = MMIORegister.get_instance('LUT_3D_CTL_REGISTER', lut_3d_ctl_reg, common.PLATFORM_NAME)
    lut_3d_ctl_reg_offset = instance.offset

    lut_3d_enable = (driver_interface_.mmio_read(lut_3d_ctl_reg_offset, gfx_index=adapter.gfx_index) >> 31)
    if lut_3d_enable == 1:
        logging.info("Hw 3D LUT is enabled on pipe %c", panel.pipe)
        hw_3d_lut_status = True
        time.sleep(1)
        new_lut_ready = (driver_interface_.mmio_read(lut_3d_ctl_reg_offset, gfx_index=adapter.gfx_index) >> 30) & 1
        if new_lut_ready == 0:
            logging.info("Hardware finished loading the lut buffer into internal working RAM")
            hw_lut_buffer_status = True
        else:
            logging.error("Hardware did not load the lut buffer into internal working RAM")
            gdhm.report_bug(
                title="[COLOR][3D_LUT] H/W failed to load LUT buffer into internal working RAM",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )

            etl_file = __end_capture('3d_lut')
            return hw_lut_buffer_status, etl_file
    else:
        logging.error("Hw 3D LUT is disabled on pipe %s", panel.pipe)
        etl_file = __end_capture('3d_lut')
        return hw_3d_lut_status, etl_file

    etl_file = __end_capture('3d_lut')
    if hw_3d_lut_status is True and hw_lut_buffer_status is True:
        return True, etl_file
    return False, etl_file


##
# @brief        This function is to apply default LUT binary
# @param[in]    adapter object
# @param[in]    panel object
# @return       True if enabled else False
def apply_default_bin(adapter, panel):
    default_bin = 'CustomLUT_default.bin'
    default_bin_path = os.path.join(__BIN_PATH, default_bin)
    path = os.path.join(test_context.SHARED_BINARY_FOLDER, default_bin_path)
    cui_dpp_hw_lut_info = DppHwLutInfo(panel.target_id, DppHwLutOperation.UNKNOWN.value, 0)
    result, cui_dpp_hw_lut_info = driver_escape.get_dpp_hw_lut(adapter.gfx_index, cui_dpp_hw_lut_info)
    if result is False:
        logging.error(f'Escape call failed : get_dpp_hw_lut() for {panel.target_id}')
        return False
    # Apply default bin before returning
    cui_dpp_hw_lut_info = DppHwLutInfo(panel.target_id, DppHwLutOperation.APPLY_LUT.value, cui_dpp_hw_lut_info.depth)
    if cui_dpp_hw_lut_info.convert_lut_data(path) is False:
        logging.error(f'Invalid bin file path provided : {path}!')

    result = driver_escape.set_dpp_hw_lut(adapter.gfx_index, cui_dpp_hw_lut_info)
    if result is False:
        logging.error(f'Escape call failed : set_dpp_hw_lut() for {panel.target_id}')
        return False
    return True


##
# @brief        helper function for 3d lut verification
# @param[in]    lut values
# @param[in]    bin file, custom bin file name
# @return       True if enabled else False
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
            return False
        index += 1


##
# @brief        helper function for Applying plane format
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    no_of_displays Number of displays
# @param[in]    source_id source_id of the plane
# @param[in]    enable_mpo
# @param[in]    pixel_format [(int, int), (int, int), (int, int)] (Color format value to apply for the planes, value to be compared from MMIO register)
# @param[in]    width of the plane
# @param[in]    height of the plane
# @param[in]    is_custom_plane_size_test Specifies whether test is custom plane size test
# @param[in]    rect_data Dirty rectangle update on the screen(Top scanline, bottom scanline)
# @return       True if enabled False is disabled. None if resolution is not valid
def plane_format(adapter, panel, no_of_displays, source_id, enable_mpo=None, pixel_format=[None, None, None], width=None,
                 height=None, is_custom_plane_size_test=False, rect_data=None):
    # pixel_format[0], pixel_format[1], pixel_format[2] - Expectation :-
    # pixel_format[0] - Plane-1 Pixel Format, pixel_format[1] - Plane-2 Pixel Format, pixel_format[2] - Plane-3 Pixel Format
    # If there is no specific input for all three pixel_formats in the command line (All pixel_format[0], pixel_format[1], pixel_format[2] are None),
    # Test will generate flip on Plane-1 with RGB Pixel format by default
    # If we need to enable multiple planes, we have to explicitly specify pixel formats for second and third plane(Based on the requirement) in the command line
    # We can also specify the pixel format for Plane-1 if we need to use any other pixel format apart from RGB. The value will

    status = True
    disable = False
    current_mode = display_config_.get_current_mode(panel.target_id)
    p1_layer_index = 0
    p2_layer_index = 0
    p3_layer_index = 0

    if enable_mpo is None:
        enable_mpo = flip.MPO()
        ##
        # Enable the DFT framework and feature
        enable_mpo.enable_disable_mpo_dft(True, 1, gfx_adapter_index=adapter.gfx_index)
        disable = True

    # For Custom plane size tests, plane's width and height will be passed explicitly during plane generation
    # Custom plane test Plane Sizes (Fixed) - Plane1 - 500x500 , Plane2 - 192x30, Plane3 - 500x500
    if not is_custom_plane_size_test:
        if width is None:
            width = current_mode.HzRes
        if height is None:
            height = current_mode.VtRes

        if width is not None and height is not None:
            # Check if restriction is valid for the current resolution
            valid_resolution = current_mode.HzRes >= width and current_mode.VtRes >= height
            if not valid_resolution:
                logging.warning(f"Skipping Current Resolution : ({current_mode.HzRes} x {current_mode.VtRes}) < ({width} x {height})")
                return None

    # Keep layer index for the planes based on platform and number of planes
    if adapter.name not in machine_info.PRE_GEN_15_PLATFORMS:
        # pixel_format[2] and pixel_format[1] will be not None only when the Pixel Formats are explicitly specified for -
        # Plane-2 and Plane-3 in the command line in fbc_plane_resize.py test
        # Following assignment is done to use right layer index for the planes based on test requirement
        if pixel_format[1] is not None:
            p1_layer_index = 0
            p2_layer_index = 1

        if pixel_format[2] is not None:
            p1_layer_index = 0
            p2_layer_index = 1
            p3_layer_index = 2

    if not is_custom_plane_size_test:
        source_rect_coordinates = flip.MPO_RECT(0, 0, width, height)
        destination_rect_coordinates = flip.MPO_RECT(0, 0, width, height)
        clip_rect_coordinates = flip.MPO_RECT(0, 0, width, height)

    if adapter.name not in (set(common.PRE_GEN_15_PLATFORMS) - {'DG2', 'DG3', 'MTL', 'LNL', 'ELG'}):
        surface_memory_type = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_TILE4
    else:
        surface_memory_type = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED
    
    # Fill dirty rectangle data will full frame value by default
    if rect_data is None:
        dirty_rect = flip.MPO_RECT(0, 0, width, height)
    else:
        dirty_rect = flip.MPO_RECT(0, rect_data[0], width, rect_data[1])

    # If pixel format for Plane-1 is not explicitly specified in the test command line, by default B8G8R8X8 will be considered
    if pixel_format[0] is None:
        pixel_format[0] = (flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8, 8)

    planes = []
    if not is_custom_plane_size_test:
        for index in range(0, no_of_displays):
            if pixel_format[2] is not None:
                plane_3_attributes = flip.PLANE_INFO(source_id[index], p3_layer_index, 1, pixel_format[2][0],
                                            surface_memory_type, source_rect_coordinates, destination_rect_coordinates,
                                            clip_rect_coordinates, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, 
                                            flip.MPO_BLEND_VAL(0), st_mpo_dirty_rect=dirty_rect)
                planes.append(plane_3_attributes)

            if adapter.name not in machine_info.PRE_GEN_15_PLATFORMS and pixel_format[1] is not None:
                plane_2_attributes = flip.PLANE_INFO(source_id[index], p2_layer_index, 1, pixel_format[1][0],
                                                surface_memory_type, source_rect_coordinates,
                                                destination_rect_coordinates,
                                                clip_rect_coordinates, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                                flip.MPO_BLEND_VAL(0), st_mpo_dirty_rect=dirty_rect)
                planes.append(plane_2_attributes)

            plane_1_attributes = flip.PLANE_INFO(source_id[index], p1_layer_index, 1, pixel_format[0][0],
                                            surface_memory_type, source_rect_coordinates, destination_rect_coordinates,
                                            clip_rect_coordinates, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, 
                                            flip.MPO_BLEND_VAL(0), st_mpo_dirty_rect=dirty_rect)
            planes.append(plane_1_attributes)
    else:
        if adapter.name not in machine_info.PRE_GEN_15_PLATFORMS:
            p3_source_rect_coordinates = flip.MPO_RECT(0, 0, 500, 500)
            p3_destination_rect_coordinates = flip.MPO_RECT(0, 0, 500, 500)
            p3_clip_rect_coordinates = flip.MPO_RECT(0, 0, 500, 500)

            p2_source_rect_coordinates = flip.MPO_RECT(0, 0, 195, 32)
            p2_destination_rect_coordinates = flip.MPO_RECT(0, 0, 195, 32)
            p2_clip_rect_coordinates = flip.MPO_RECT(0, 0, 195, 32)

            p1_source_rect_coordinates = flip.MPO_RECT(0, 0, 500, 500)
            p1_destination_rect_coordinates = flip.MPO_RECT(0, 0, 500, 500)
            p1_clip_rect_coordinates = flip.MPO_RECT(0, 0, 500, 500)

            for index in range(0, no_of_displays):
                if pixel_format[2] is not None:
                    plane_3_attributes = flip.PLANE_INFO(source_id[index], p3_layer_index, 1, pixel_format[2][0],
                                                surface_memory_type, p3_source_rect_coordinates, p3_destination_rect_coordinates,
                                                p3_clip_rect_coordinates, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                                flip.MPO_BLEND_VAL(0), st_mpo_dirty_rect=dirty_rect)
                    planes.append(plane_3_attributes)

                plane_2_attributes = flip.PLANE_INFO(source_id[index], p2_layer_index, 1, pixel_format[1][0],
                                                surface_memory_type, p2_source_rect_coordinates,
                                                p2_destination_rect_coordinates,
                                                p2_clip_rect_coordinates, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                                flip.MPO_BLEND_VAL(0), st_mpo_dirty_rect=dirty_rect)
                planes.append(plane_2_attributes)

                plane_1_attributes = flip.PLANE_INFO(source_id[index], p1_layer_index, 1, pixel_format[0][0],
                                                surface_memory_type, p1_source_rect_coordinates, p1_destination_rect_coordinates,
                                                p1_clip_rect_coordinates, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                                flip.MPO_BLEND_VAL(0), st_mpo_dirty_rect=dirty_rect)
                planes.append(plane_1_attributes)
        else:
            logging.error("Custom test scenario will not work in PRE-GEN15 platforms")
            return False

    pplanes = flip.PLANE(planes)
    plane_count = len(planes)
    # Check the hardware support for the plane
    supported = enable_mpo.check_mpo3(pplanes, gfx_adapter_index=adapter.gfx_index)

    # Present the planes on the screen
    if supported == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
        result = enable_mpo.set_source_address_mpo3(pplanes, gfx_adapter_index=adapter.gfx_index)
        if result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
            logging.info(f"Successfully generated flip on {panel.port} on adapter {adapter.gfx_index}")
        elif result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            logging.error("Failed to create resource")
            status = False
        else:
            logging.error(f"Failed to generate the flip on {panel.port} on adapter {adapter.gfx_index}")
            status = False
    elif supported == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
        logging.error("Failed to create resource")
        status = False
    else:
        logging.error("Hardware does not support plane parameters on adapter {0} with Error code:{1}"
                      .format(adapter.gfx_index, supported))
        gdhm.report_bug(
            title="[DFT_Framework][FLIP]Failed to generate FLIP with error {}".format(supported),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        status = False

    if status is True:
        sys_util = system_utility.SystemUtility()
        exec_env = sys_util.get_execution_environment_type()
        if exec_env == 'SIMENV_FULSIM' and planes_helper.get_flipq_status(gfx_adapter_index=adapter.gfx_index):
            start_plane_processing()
        time.sleep(5)
        # Check whether the planes were generated succesfully
        for layer_id in ['0', '1', '2']:
            if layer_id == '1' and pixel_format[1] is None:
                continue
            if layer_id == '2' and pixel_format[2] is None:
                continue

            plane_id = planes_verification.get_plane_id_from_layerindex(plane_count, int(layer_id), adapter.gfx_index)
            plane_id = str(plane_id)
            plane_ctl = MMIORegister.read('PLANE_CTL_REGISTER', 'PLANE_CTL_' + plane_id + '_' + panel.pipe, adapter.name,
                                        gfx_index=adapter.gfx_index)

            # Check for Plane enable
            if plane_ctl.plane_enable == 0:
                logging.error(f"Plane_{plane_id}_{panel.pipe} is disabled after generation")
                status &= False
                continue

            # Check whether flip got generated with expected pixel format
            if layer_id == '0' and plane_ctl.source_pixel_format != pixel_format[0][1]:
                logging.error(f"Test Failed to generate a flip with Pixel format {pixel_format[0][1]} on Plane_{plane_id}_{panel.pipe} on {panel.port}")
                status &= False
                continue
            elif layer_id == '1' and plane_ctl.source_pixel_format != pixel_format[1][1]:
                logging.error(f"Test Failed to generate a flip with Pixel format {pixel_format[1][1]} on Plane_{plane_id}_{panel.pipe} on {panel.port}")
                status &= False
                continue
            elif layer_id == '2' and plane_ctl.source_pixel_format != pixel_format[2][1]:
                logging.error(f"Test Failed to generate a flip with Pixel format {pixel_format[2][1]} on Plane_{plane_id}_{panel.pipe} on {panel.port}")
                status &= False
                continue

            logging.info(f"Succesfully verified Pixel Format and Plane Enable after generating flip on Plane_{plane_id}_{panel.pipe}")

    if disable:
        # Disable the DFT framework and feature
        enable_mpo.enable_disable_mpo_dft(False, 1, gfx_adapter_index=adapter.gfx_index)
        logging.info("\tDisable the DFT framework success")
    return status


##
# @brief        This is a helper function to trigger Short Pulse Interrupt (SPI)
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    duration indicates sleep duration  in ms
# @param[in]    count int, indicates number of times the SPI should be triggered
# @return       False if failed to trigger SPI, True otherwise
def trigger_spi(adapter, panel, duration, count):
    logging.info("STEP : Triggering SPI for the port {}".format(panel.port))
    # if valsim_.init_lfp_ports(adapter.adapter_info, [panel.port]) is False:
    #     logging.error("\tFailed to initialize the port {}".format(panel.port))
    #     return False
    for _ in range(count):
        if driver_interface.DriverInterface().set_spi(adapter.adapter_info, panel.port, 'NATIVE'):
            logging.info("STEP : Check for Visual corruption")
            if duration > 0:
                time.sleep(duration)
        else:
            logging.error("\tFailed to Trigger SPI")
            return False
    return True


##
# @brief        This is a helper function to capture ETL. It starts the etl tracer
# @return       True if ETL tracer starts successfully, False otherwise
def __start_capture():
    etl_tracer.stop_etl_tracer()
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTraceBefore_workload.' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return False
    return True


##
# @brief        This is a helper function to run 3D workload
# @param[in]    sync_mode Sync/Async Flip
# @param[in]    window_size indicates if the window has to be full screen
# @param[in]    adapter Adapter Object
# @param[in]    panel Panel Object
# @return       etl_file_path string  path to etl file if ETL capture ends successfully
def run_3d_workload(sync_mode, window_size, adapter, panel):
    app_handle = None
    directx_app = os.path.join(__DIRECTX_APP_LOCATION, 'MultiAnimation.exe')
    app_args = [directx_app, __directx_args_dict[sync_mode], __directx_args_dict[window_size]]

    logging.info("Launching 3D {} {} WORKLOAD".format(window_size.upper(), sync_mode.upper()))
    try:
        kb.press('WIN+M')
        # Launch the DirectX app with the arguments
        app_handle = subprocess.Popen(app_args)
        time.sleep(6)
        # start etl_capture
        if __start_capture() is False:
            return False, None
        if sync_mode == 'async' and window_size == 'fullscreen':
            fields_expected_value = 'async_address_update_enable_ASYNC'
        else:
            fields_expected_value = 'async_address_update_enable_SYNC'
        plane_ctl = MMIORegister.read('PLANE_CTL_REGISTER', 'PLANE_CTL_1_' + panel.pipe, adapter.name,
                                      gfx_index=adapter.gfx_index)
        plane_ctl_value = importlib.import_module("registers.{}.PLANE_CTL_REGISTER".format(adapter.name.lower()))
        if plane_ctl.__getattribute__('async_address_update_enable') != getattr(plane_ctl_value, fields_expected_value):
            gdhm.report_bug(
                title="[PowerCons][FeatureLib]Failed to generate {0} FLIP in {1} with 3D APP".format(sync_mode,
                                                                                                     window_size),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            assert False, "Failed to generate {} flips".format(sync_mode)
        time.sleep(10)
        etl_file = __end_capture('3d_workload')
    except Exception as e:
        assert False, e
    finally:
        if app_handle is not None:
            app_handle.terminate()
        logging.info("Closed the Directx 3D APP")

    return True, etl_file


##
# @brief        This is a helper function to run D3D12 app
# @param[in]    full_screen bool
# @param[in]    is_multi_instance bool
# @return       status, etl_file_path string  path to etl file if ETL capture ends successfully
def run_d3d_app(full_screen=False, is_multi_instance=False):
    app_instance_1 = None
    app_instance_2 = None
    try:
        kb.press('WIN+M')
        app_instance_1 = subprocess.Popen(os.getcwd()[:2] +
                                          r'/SHAREDBINARY/920697932/MPO/D3D12FullScreen/D3D12Fullscreen.exe',
                                          cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))
        if full_screen:
            kb.press('ALT_ENTER')
            time.sleep(2)

        if is_multi_instance:
            app_instance_2 = subprocess.Popen(os.getcwd()[:2] +
                                              r'/SHAREDBINARY/920697932/MPO/D3D12FullScreen/D3D12Fullscreen.exe',
                                              cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))
        time.sleep(5)
        if is_multi_instance:
            kb.press('WIN+RIGHT')
            kb.press('ENTER')
        # start etl_capture
        if __start_capture() is False:
            return False, None
        logging.info("Launched D3D App successfully ")

        time.sleep(20)
        etl_file = __end_capture('3d_workload')

    except Exception as e:
        assert False, e
    finally:
        if app_instance_1 is not None:
            app_instance_1.terminate()
        if app_instance_2 is not None:
            app_instance_2.terminate()
        logging.info("Closed the D3D APP successfully")

    return True, etl_file


##
# @brief        Exposed API to enable/disable HDR using OS API
# @param[in]    port_list list, ['DP_A']
# @param[in]    enable_flag Boolean, true - enable HDR, false-disable HDR
# @return       True if operation successful, False otherwise
def enable_disable_hdr(port_list, enable_flag):
    hdr_instance = os_hdr_verification.OSHDRVerification()
    enumerated_displays = display_config_.get_enumerated_display_info()
    enable = 'ENABLE' if enable_flag else "DISABLE"
    for display_index in range(enumerated_displays.Count):
        port_type = str(CONNECTOR_PORT_TYPE(
            enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
        if port_type in port_list:
            if enumerated_displays.ConnectedDisplays[display_index].IsActive:
                hdr_return_status = configure_hdr(
                    enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo, enable=enable_flag)
                # Decode HDR Error Code and Verify
                if hdr_instance.is_error("OS_HDR", hdr_return_status, enable) is False:
                    return False
                time.sleep(5)
                # Verify PIPE_MISC for register verification
                if hdr_instance.verify_hdr_mode(port_type, enable, common.PLATFORM_NAME.lower()) is False:
                    return False
            else:
                logging.error("Plugged display {} is inactive".format(port_type))
                return False
    return True


##
# @brief        This is a helper function to capture ETL. It ends the etl tracer
# @param[in]    method verification method(video/cursor/app)
# @return       etl_file_path string  path to etl file if ETL capture ends successfully
def __end_capture(method):
    etl_tracer.stop_etl_tracer()
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTrace_' + str(method) + '_' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
    return etl_file_path


##
# @brief        Helper Function to verify co-existence with MPO
# @param[in]    adapter Adapter Object
# @param[in]    panel Panel Object
# @param[in]    etl_file etl file path
# @return       None
def verify_mpo(adapter, panel, etl_file):
    time_stamp = 0
    if etl_parser.generate_report(etl_file) is False:
        return False
    # Check for Layer Reordering in case of supported platforms
    if not planes_verification.check_layer_reordering(adapter.gfx_index):
        plane = "3"
    else:
        plane = "1"
    plane_ctl = MMIORegister.get_instance("PLANE_CTL_REGISTER", "PLANE_CTL_" + plane + "_" + panel.pipe,
                                          adapter.name)

    plane_data = etl_parser.get_mmio_data(plane_ctl.offset)
    for val in plane_data:
        plane_ctl.asUint = val.Data
        if plane_ctl.plane_enable:
            logging.info(f"Plane #{plane} enabled at {val.TimeStamp}")
            time_stamp = val.TimeStamp
            break
    if time_stamp == 0:
        logging.error(f"Plane #{plane} is not enabled")
        return False
    return True


##
# @brief        This is a helper function to update panel DPCD at run time for the given offset & val
# @param[in]    gfx_index gfx_0/gfx_1
# @param[in]    port DP_A/DP_B
# @param[in]    offset dpcd offset
# @param[in]    value dpcd val
# @return       False if failed to update dpcd, True otherwise
def update_panel_dpcd(gfx_index, port, offset, value):
    logging.info(f"STEP : Updating dpcd offset {hex(offset)}h  with val {value} on {port}")
    if driver_interface.DriverInterface().set_panel_dpcd(gfx_index, port, offset, value) is not True:
        logging.error("\tFailed to update panel Dpcd")
        return False
    return True


##
# @brief        Get the cpu stepping
# @return       Stepping of the CPU
def get_cpu_stepping():
    output = platform.processor()
    std_out = re.compile(r'[\r\n]').sub(" ", output)
    # search for the numbers after the match of "Stepping "
    match_output = re.match(r".*Stepping (?P<Stepping>[0-9]+)", std_out)
    if match_output is None:
        logging.error(f"FAILED to get info for CPU Stepping. Output= {output}")
        return None
    return match_output.group("Stepping")

