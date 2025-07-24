########################################################################################################################
# @file         fbc.py
# @addtogroup   PyLibs_DisplayFBC
# @brief        Contains exposed API for FBC verification for all the platforms
#               Exposed APIs:
#               1) enable_fbc(gfx_index) : Enables FBC in FeatureTestControl for given adapter
#               2) verify_adapter_fbc(gfx_index) : Verifies FBC programming for given adapter
#               3) verify_fbc() : Verify FBC for all connected adapters
#
# @author       Rohit Kumar
########################################################################################################################

import importlib
import logging
import platform
import re
import time

from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core import system_utility
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_psr import DisplayPsr, DriverPsrVersion
from Libs.Feature.powercons import registry
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Planes.Common import planes_verification
from Tests.PowerCons.Functional.PSR import sfsu

from registers.mmioregister import MMIORegister

__display_config = display_config.DisplayConfiguration()
__display_psr = DisplayPsr()
##
# Platform details for all connected adapters
PLATFORM_INFO = {
    gfx_index: {
        'gfx_index': gfx_index,
        'name': adapter_info.get_platform_info().PlatformName
    }
    for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
}
IS_PRE_SI = system_utility.SystemUtility().get_execution_environment_type() in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]


##
# @brief        Helper API to check fbc is enabled or not
# @param[in]    gfx_index:  String, adapter index
# @param[in]    pipe: string, pipe name
# @return       True if fbc is enabled , False if disabled, None if FBC is not supported
def get_fbc_enable_status(gfx_index, pipe='A'):
    gfx_index = gfx_index.lower()
    platform_name = PLATFORM_INFO[gfx_index]['name']
    if (platform_name in machine_info.GEN_14_PLATFORMS and pipe in ['A', 'B']) or \
            platform_name not in machine_info.PRE_GEN_15_PLATFORMS:
        reg_name = 'FBC_CTL_' + pipe
    elif platform_name in machine_info.PRE_GEN_14_PLATFORMS and pipe == 'A':
        reg_name = 'FBC_CTL'
    else:
        logging.info(f"FBC is not supported on {platform_name} on Pipe-{pipe}")
        return None

    fbc_ctl = MMIORegister.read('FBC_CTL_REGISTER', reg_name, platform_name, gfx_index=gfx_index)
    return fbc_ctl.enable_fbc == 0x1


##
# @brief        Helper API to check interlaced mode on port connected to pipe A
# @param[in]    gfx_index: String, adapter index
# @param[in]    pipe: string, pipe name
# @return       True if current mode is interlaced, False otherwise
def __is_interlaced_mode(gfx_index, pipe):
    port = [key for key, value in display_base.get_port_to_pipe(gfx_index=gfx_index).items() if value == 'PIPE_' + pipe][0]
    display_and_adapter_info = __display_config.get_display_and_adapter_info_ex(port, gfx_index)
    if type(display_and_adapter_info) is list:
        display_and_adapter_info = display_and_adapter_info[0]

    if display_and_adapter_info is None:
        raise Exception("Failed to get DisplayAndAdapterInfo for {0} on {1}".format(port, gfx_index))
    current_mode = __display_config.get_current_mode(display_and_adapter_info)
    return current_mode.scanlineOrdering == enum.INTERLACED


##
# @brief        Helper API to check FBC restriction for plane orientation 0 and 180 degree
# @param[in]    plane_ctl_register: Module, PLANE_CTL_REGISTER module
# @param[in]    plane_ctl: Union, PLANE_CTL register instance
# @param[in]    pipe: Sting, Panel Pipe that is being used for verifictaion
# @param[in]    plane: Sting, Plane that is being used for verification
# @param[in]    platform_name: Sting, Platform name
# @return       Restriction verification status, Restrictions list
def __get_plane_ctl_status(plane_ctl_register, plane_ctl, pipe, plane, platform_name):
    status = True
    restrictions = []
    pixel_format = 'None'
    if plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_RGB_8888:
        pixel_format = 'RGB_8888'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_RGB_565:
        pixel_format = 'RGB_565'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_YUV_422_PACKED_8_BPC:
        pixel_format = 'YUV_422_PACKED_8_BPC'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_NV12_YUV_420:
        pixel_format = 'NV12_YUV_420'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_RGB_2101010:
        pixel_format = 'RGB_2101010'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_P010_YUV_420_10_BIT:
        pixel_format = 'P010_YUV_420_10_BIT'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_P012_YUV_420_12_BIT:
        pixel_format = 'P012_YUV_420_12_BIT'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_RGB_16161616_FLOAT:
        pixel_format = 'RGB_16161616_FLOAT'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_P016_YUV_420_16_BIT:
        pixel_format = 'P016_YUV_420_16_BIT'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_YUV_444_PACKED_8_BPC:
        pixel_format = 'YUV_444_PACKED_8_BPC'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_RGB_64_BIT_16161616_UINT:
        pixel_format = 'RGB_64_BIT_16161616_UINT'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_RGB_2101010_XR_BIAS:
        pixel_format = 'RGB_2101010_XR_BIAS'
    elif plane_ctl.source_pixel_format == plane_ctl_register.source_pixel_format_INDEXED_8_BIT:
        pixel_format = 'INDEXED_8_BIT'

    logging.info(
        "FBC_CONDITION_5: {0:25} Expected= {1:25} Actual= {2}".format(
            "PixelFormat", "[RGB_8888, RGB_565],", pixel_format))

    fbc_supported_pixel_formats = []
    if platform_name not in machine_info.PRE_GEN_17_PLATFORMS + ['CLS']:
        fbc_supported_pixel_formats = [plane_ctl_register.source_pixel_format_RGB_8888,
                                       plane_ctl_register.source_pixel_format_RGB_565,
                                       plane_ctl_register.source_pixel_format_RGB_16161616_FLOAT]
    else:
        fbc_supported_pixel_formats = [plane_ctl_register.source_pixel_format_RGB_8888,
                                       plane_ctl_register.source_pixel_format_RGB_565]

    # FBC is supported only with RGB pixel format (only 16/32 bpp color format)
    if plane_ctl.source_pixel_format not in fbc_supported_pixel_formats:
        status = False
        restrictions.append(f'PIXEL_FORMAT_{plane}_{pipe}')

    ##
    # FBC is supported only with Sync flips.
    flip_type = "None"
    if plane_ctl.async_address_update_enable == plane_ctl_register.async_address_update_enable_ASYNC:
        flip_type = "ASYNC"
        status = False
        restrictions.append(f'ASYNC_FLIP_{plane}_{pipe}')
    elif plane_ctl.async_address_update_enable == plane_ctl_register.async_address_update_enable_SYNC:
        flip_type = "SYNC"

    logging.info("FBC_CONDITION_6: {0:25} Expected= {1:25} Actual= {2}".format("FlipType", "SYNC,", flip_type))

    plane_rotation = "0 DEGREE"
    if plane_ctl.plane_rotation == plane_ctl_register.plane_rotation_90_DEGREE_ROTATION:
        plane_rotation = "90 DEGREE"
    elif plane_ctl.plane_rotation == plane_ctl_register.plane_rotation_180_DEGREE_ROTATION:
        plane_rotation = "180 DEGREE"
    elif plane_ctl.plane_rotation == plane_ctl_register.plane_rotation_270_DEGREE_ROTATION:
        plane_rotation = "270 DEGREE"

    logging.info(
        "FBC_CONDITION_7: {0:25} Expected= {1:25} Actual= {2}".format(
            "PlaneRotation", "[0 DEGREE, 180 DEGREE],", plane_rotation))

    ##
    # FBC is supported only with plane orientation 0 and 180 degree.
    if plane_ctl.plane_rotation in [plane_ctl_register.plane_rotation_90_DEGREE_ROTATION,
                                    plane_ctl_register.plane_rotation_270_DEGREE_ROTATION]:
        status = False
        restrictions.append(f'PLANE_ROTATION_{plane}_{pipe}')

    return status, restrictions, pixel_format


##
# @brief        Helper API to check FBC restriction for plane size
# @param[in]    gfx_index: String, adapter index
# @param[in]    min_plane_size_x: Number
# @param[in]    min_plane_size_y: Number
# @param[in]    max_plane_size_x: Number
# @param[in]    max_plane_size_y: Number
# @param[in]     plane_size: instance
# @return       status, Boolean, True if active plane size is valid for FBC, False otherwise
def __get_plane_size_status(gfx_index, min_plane_size_x, min_plane_size_y, max_plane_size_x, max_plane_size_y, pipe,
                            plane_size):
    platform_name = PLATFORM_INFO[gfx_index]['name']
    status = True

    pipe_size = MMIORegister.read('PIPE_SRCSZ_REGISTER', 'PIPE_SRCSZ_' + pipe, platform_name, gfx_index=gfx_index)

    # Plane size (x,y) size restriction check
    plane_size_x = plane_size.width + 1
    plane_size_y = plane_size.height + 1
    logging.info('PlaneSize: MIN= ({0}, {1}), MAX= ({2}, {3}), Actual= ({4}, {5})'.format(
        min_plane_size_x, min_plane_size_y, max_plane_size_x, max_plane_size_y, plane_size_x, plane_size_y))

    # Expected FBC disable if plane size not in specified range
    if plane_size_x < min_plane_size_x or plane_size_x > max_plane_size_x or \
            plane_size_y < min_plane_size_y or plane_size_y > max_plane_size_y:
        status = False

    # Plane and pipe size should in sync
    pipe_size_x = pipe_size.horizontal_source_size + 1
    pipe_size_y = pipe_size.vertical_source_size + 1

    logging.info(
        'PlaneSize: Expected <= {0}x{1}(PipeSize), Actual= {2}x{3}'.format(
            pipe_size_x, pipe_size_y, plane_size_x, plane_size_y))

    if plane_size_x > pipe_size_x or plane_size_y > pipe_size_y:
        status = False
    return status


##
# @brief        Exposed API for FBC verification for given adapter
# @param[in]    gfx_index: String, adapter index
# @return       True if FBC verification is passed, False otherwise
def verify_adapter_fbc(gfx_index):
    # Validate arguments
    if gfx_index is None or not isinstance(gfx_index, str) or not gfx_index.lower().startswith('gfx_'):
        raise Exception("Invalid arguments: gfx_index= {0}".format(gfx_index))

    gfx_index = gfx_index.lower()
    platform_name = PLATFORM_INFO[gfx_index]['name']
    status = True

    # HSD-1607897130 : FBC is not supported on Multi display in SKL
    if platform_name in ['SKL']:
        current_display_config = __display_config.get_current_display_configuration()
        if current_display_config.numberOfDisplays > 1:
            logging.info("FBC is not supported on Multi display in SKL")
            return True

    # Get actual FBC status
    plane_ctl_register = importlib.import_module('registers.{0}.PLANE_CTL_REGISTER'.format(platform_name.lower()))
    pipes = ['A']

    if platform_name not in machine_info.PRE_GEN_14_PLATFORMS:
        pipes.append('B')
    if platform_name not in machine_info.PRE_GEN_15_PLATFORMS:
        pipes.append('C')
        pipes.append('D')

    # Make sure FBC is not disabled in FeatureTestControl registry key
    feature_test_control = registry.FeatureTestControl(gfx_index)
    logging.info("FBC_CONDITION_1: {0:25} Expected= {1:25} Actual= {2}".format(
        "FeatureTestControl: FBC", "ENABLED,", "DISABLED" if feature_test_control.fbc_disable else "ENABLED"))
    if feature_test_control.fbc_disable == 1:
        logging.error("FBC is not enabled in FeatureTestControl Regkey")
    else:
        # check fbc disable
        # if fbc disable in driver on both pipe A and pipe B return true else false
        for pipe in pipes:
            status &=  __verify_restrictions(gfx_index, plane_ctl_register, pipe=pipe)
    return status


##
# @brief        Helper API to check plane restrictions
# @param[in]    gfx_index: String, adapter index
# @param[in]    platform_name: String, Platform Name
# @param[in]    pipe: string, pipe
# @param[in]    plane_ctl_register: instance
# @return       Plane restrictions list
def verify_plane_params(gfx_index, platform_name, pipe, plane_ctl_register):
    min_plane_size_x = 200
    min_plane_size_y = 32
    max_plane_size_y = 4088 # Limit due to HW underrun issue. VSDI-53030
    max_plane_size_x = 5120
    actual_restriction_list = []
    all_plane_restriction_list = []
    plane_size_restriction_list = []
    enabled_layers = []
    plane_ctl_restriction_count = 0
    enabled_plane_count = 0
    possible_restriction_list = ['PIXEL_FORMAT', 'ASYNC_FLIP', 'PLANE_ROTATION', 'PLANE_SIZE', 'PLANE_STRIDE_LARGER_THAN_DISPLAY_STRIDE', 'PLANE_LARGER_THAN_SCREEN_RESOLUTION']
    topmost_rgb_plane = 0

    # Set the fbc parameters based on platform
    if platform_name in machine_info.PRE_GEN_11_PLATFORMS:
        max_plane_size_x = 4088

    if platform_name not in machine_info.PRE_GEN_16_PLATFORMS:
        max_plane_size_x = 6144

    # Find the number of enabled planes
    for plane in ['1', '2', '3']:
        plane_ctl_for_count = MMIORegister.read('PLANE_CTL_REGISTER', f'PLANE_CTL_{plane}_{pipe}', platform_name, gfx_index=gfx_index)
        if plane_ctl_for_count.plane_enable == plane_ctl_register.plane_enable_ENABLE:
            enabled_plane_count += 1

    # Find out which layers are enabled and store in a list
    # Logic : Loop through the possible layers, get the respective plane index and check for plane enable
    for layer in [0, 1, 2]:
        plane_id = planes_verification.get_plane_id_from_layerindex(enabled_plane_count, layer, gfx_index=gfx_index)
        # As we are blindly looping through the possible layers,
        # keeping a check below to avoid the verification on invalid plane indices(0, -1 etc)
        if plane_id <= 0:
            continue
        plane_ctl_for_layer = MMIORegister.read('PLANE_CTL_REGISTER', f'PLANE_CTL_{plane_id}_{pipe}', platform_name, gfx_index=gfx_index)
        if plane_ctl_for_layer.plane_enable == plane_ctl_register.plane_enable_ENABLE:
            enabled_layers.append(layer)

    logging.info(f"Number of enabled planes : {enabled_plane_count}")
    logging.info(f"Currently enabled layer indices : {enabled_layers}")
    # Check and append the Plane restrictions to the list accordingly
    for layer_id in enabled_layers:
        plane_id = planes_verification.get_plane_id_from_layerindex(enabled_plane_count, int(layer_id), gfx_index)
        plane_register = 'PLANE_CTL_' + str(plane_id) + '_'

        # Driver will always consider Plane_CTL_1 for FBC in Pre-Gen15 platforms as FBC is supported only on single plane
        # FBC is supported on 2 Pipes in Gen14 platforms. Hence restricting the FBC verification for PLANE_CTL_1 for Pre-Gen15 platforms
        if platform_name in machine_info.PRE_GEN_15_PLATFORMS and "PLANE_CTL_1" not in plane_register:
            continue

        logging.info(f"Checking Plane restrictions for {plane_register}{pipe} (LayerId-{str(layer_id)})")

        # Check for plane enable
        plane_ctl = MMIORegister.read('PLANE_CTL_REGISTER', plane_register + pipe, platform_name, gfx_index=gfx_index)
        if plane_ctl.plane_enable != plane_ctl_register.plane_enable_ENABLE:
            logging.info(f"FBC_CONDITION_3: PLANE_{str(plane_id)}_{pipe} is DISABLED")
        else:
            # Check for Plane CTL restrictions
            plane_status, plane_ctl_restrictions, pixel_format = __get_plane_ctl_status(plane_ctl_register, plane_ctl, pipe, str(plane_id), platform_name)
            if plane_status is False:
                all_plane_restriction_list.extend(plane_ctl_restrictions)

            # Fetch the top-most RGB plane to check FBC Plane Binding. EX : PLANE_1_RGB_888
            # Logic - RGB plane with highest PlaneId is the top-most plane(Eg. PLANE_1_RGB_888, PLANE_2_RGB_888 - Top-most is Plane 2)
            if 'RGB' in pixel_format and plane_id > topmost_rgb_plane:
                topmost_rgb_plane = plane_id

            # Check Plane Size restrictions
            plane_size = MMIORegister.read('PLANE_SIZE_REGISTER', 'PLANE_SIZE_' + str(plane_id) + '_' + pipe, platform_name, gfx_index=gfx_index)
            if __get_plane_size_status(gfx_index, min_plane_size_x, min_plane_size_y, max_plane_size_x, max_plane_size_y, pipe,
                    plane_size) is False:
                plane_size_string = 'PLANE_SIZE_' + str(plane_id) + '_' + pipe
                plane_size_restriction_list.append(plane_size_string)
                all_plane_restriction_list.append(plane_size_string)

            # Check FBC Stride - Plane stride should be lesser than FBC stride
            # Currently making the check specific to BMG. Scope to be expanded as part of the JIRA : https://jira.devtools.intel.com/browse/VSDI-45249
            if platform_name in ['ELG']:
                stride_rstn_list = __verify_fbc_stride(pipe, gfx_index, pixel_format, platform_name, plane_id, plane_ctl)
                all_plane_restriction_list.extend(stride_rstn_list)

            # Check Plane Size vs Screen Resolution - Plane Size should be less than Screen Resolution
            pipe_rstn_lst = __verify_fbc_pipe_size(gfx_index, pipe, plane_size)
            all_plane_restriction_list.extend(pipe_rstn_lst)

    logging.info(f'All Plane restrictions list : {all_plane_restriction_list}')

    # Atleast one plane should be enabled. If no planes are enabled, append PLANE_DISABLE as a restriction
    if enabled_plane_count == 0:
        actual_restriction_list.append('PLANE_DISABLE')

    for rstn_str in possible_restriction_list:
        plane_restn_lst = [rstn for rstn in all_plane_restriction_list if rstn_str in rstn]
        plane_ctl_restriction_count = len(plane_restn_lst)
        # From Gen-15 onwards, FBC is supported on 3 planes. So, FBC will be disabled there only if all planes are having restrictions
        if platform_name not in machine_info.PRE_GEN_15_PLATFORMS and enabled_plane_count != plane_ctl_restriction_count:
            continue
        if plane_ctl_restriction_count != 0:
            actual_restriction_list.extend(plane_restn_lst)

    return actual_restriction_list, topmost_rgb_plane


##
# @brief        Internal API to check FBC restrictions for given adapter and pipe
# @param[in]    gfx_index: String, adapter index
# @param[in]    plane_ctl_register: instance
# @param[in]    max_plane_size_x: int, plane size
# @param[in]    pipe: string, pipe
# @return       True if FBC verification is passed, False otherwise
def __verify_restrictions(gfx_index, plane_ctl_register, pipe='A'):
    platform_name = PLATFORM_INFO[gfx_index]['name']
    actual_fbc_status = True
    fbc_stride = None
    status = True
    restriction_list = []

    logging.info(f"Verifying Restrictions on PIPE_{pipe}")

    # Make sure Pipe is active
    if 'PIPE_' + pipe not in display_base.get_port_to_pipe(gfx_index=gfx_index).values():
        logging.info(
            "FBC_CONDITION_2: {0:25} Expected= {1:25} Actual= {2}".format("PIPE_" + pipe, "ENABLED,", "DISABLED"))
        restriction_list.append('PIPE_'+ pipe + ' _NOT_ACTIVE')
        return True

    logging.info(
        "FBC_CONDITION_2: {0:25} Expected= {1:25} Actual= {2}".format("PIPE_" + pipe, "ENABLED,", "ENABLED"))

    plane_ctl = MMIORegister.read('PLANE_CTL_REGISTER', 'PLANE_CTL_1_' + pipe, platform_name, gfx_index=gfx_index)
    # Check for PLANE restrictions
    plane_restriction_list, topmost_rgb_plane = verify_plane_params(gfx_index, platform_name, pipe, plane_ctl_register)

    if plane_restriction_list:
        restriction_list.extend(plane_restriction_list)

    # FBC is supported only with Progressive mode
    if __is_interlaced_mode(gfx_index, pipe):
        logging.info(
            "FBC_CONDITION_4: {0:25} Expected= {1:25} Actual= {2}".format(
                "DisplayScanLine", "PROGRESSIVE,", "INTERLACED"))
        restriction_list.append('INTERLACED_MODE')
    else:
        logging.info(
            "FBC_CONDITION_4: {0:25} Expected= {1:25} Actual= {2}".format(
                "DisplayScanLine", "PROGRESSIVE,", "PROGRESSIVE"))

    # Check whether PSR1/PSR2 is supported
    # FBC and PSR co-existence is allowed from Gen15+ platforms
    # Bit 26 in DisplayPcFeatureControl regkey will be set to 1 if FBC needs to get disabled in PSR2 panels
    # @todo : Add CFF check with FBC enable for Post-Gen15 platforms : JIRA : https://jira.devtools.intel.com/browse/VSDI-40528
    port = [key for key, value in display_base.get_port_to_pipe(gfx_index=gfx_index).items() if
             value == 'PIPE_' + pipe][0]
    vbt_panel_type = display_utility.get_vbt_panel_type(port, gfx_index)
    fbc_psr2_coexistence_status = True
    logging.info(f"FBC PSR2 co-existence status in DisplayPcFeatureCtrlDbg regkey : {fbc_psr2_coexistence_status}")
    rstn_list = []
    pr_panel = __display_psr.is_pr_supported_in_panel(edp_port=port)
    if vbt_panel_type in [display_utility.VbtPanelType.LFP_DP]:
        psr1_panel = __display_psr.is_psr_supported_in_panel(DriverPsrVersion.PSR_1, edp_port=port)
        psr2_panel = __display_psr.is_psr_supported_in_panel(DriverPsrVersion.PSR_2, edp_port=port)
        is_psr_supported = psr1_panel or psr2_panel
        transcoder = __get_transcoder(port, gfx_index)
        if (is_psr_supported or pr_panel) and len(restriction_list) == 0:
            status, rstn_list = check_fbc_psr_pr_concurrency(plane_ctl_register, platform_name, gfx_index, pipe, transcoder, fbc_psr2_coexistence_status)
            if not status:
                return False
            restriction_list.extend(rstn_list)

    expected_fbc_status = False
    # DPCD read will launch screen update app. Adding 10 sec delay to ensure app is closed and desktop plane is enabled back
    time.sleep(10)
    if get_fbc_enable_status(gfx_index, pipe) is False:
        actual_fbc_status = False

    if len(restriction_list) == 0:
        expected_fbc_status = True
        # WA - https://hsdes.intel.com/appstore/article/#/16023588340 : FBC will be disabled for BMG G21. G31 is expected to have the fix
        cpu_stepping = __get_cpu_stepping()
        if platform_name in ['ELG'] and cpu_stepping <= '2':
            expected_fbc_status = False

        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for index in adapter_dict.keys():
            logging.info(f"Device ID: {adapter_dict[index].deviceID}")
            if (platform_name in ['ELG']) and (adapter_dict[index].deviceID in ["E221", "E222", "E223", "E220"]):
                expected_fbc_status = True

        if platform_name in machine_info.PRE_GEN_15_PLATFORMS and expected_fbc_status:
            # HSD - 22011775174 - WA: The driver needs to always enable the override stride
            platform_name = PLATFORM_INFO[gfx_index]['name']
            if platform_name in machine_info.PRE_GEN_12_PLATFORMS:
                fbc_stride = MMIORegister.read('FBC_STRIDE_REGISTER', 'FBC_STRIDE', platform_name, gfx_index=gfx_index)
            elif platform_name in machine_info.PRE_GEN_15_PLATFORMS:
                fbc_stride = MMIORegister.read('FBC_STRIDE_REGISTER', 'FBC_STRIDE_' + pipe, platform_name, gfx_index=gfx_index)

            if fbc_stride:
                logging.info(f"FBC Stride override Expected = 1 Actual= {fbc_stride.override_stride_enable}")
                if fbc_stride.override_stride_enable == 0:
                    gdhm.report_driver_bug_pc(f"FBC Stride override Expected = 1 Actual = {fbc_stride.override_stride_enable}")
                    status = False

        # Extra verifications for Gen15+ platforms
        # As FBC is supported in multi-planes from Gen15 onmwards, FBC has to get enabled on top-most RGB plane in Gen15+ platforms
        # Criteria for FBC enable - If screen update >= 25% FBC will get enabled with Continuous Full Fetch
        # If screen update < 25%, Selective Fetch is preffered
        # Below verification checks CFF enable whenever FBC is enabled in Gen15+ platforms
        if platform_name not in machine_info.PRE_GEN_15_PLATFORMS and actual_fbc_status == True:
            # Verify FBC plane binding
            fbc_ctl = MMIORegister.read('FBC_CTL_REGISTER', 'FBC_CTL_' + pipe, platform_name,
                                            gfx_index=gfx_index)
            plane_binding_value = int(fbc_ctl.plane_binding) + 1
            if plane_binding_value not in [1, 2, 3]:
                logging.error("Invalid plane binding value")
                gdhm.report_driver_bug_pc("[Powercons][FBC] Invalid plane binding value")
                return False
            logging.info(f'Topmost enabled RGB Plane ID : {topmost_rgb_plane}')

            if plane_binding_value != topmost_rgb_plane:
                logging.error(f"FBC is not enabled on the top-most RGB plane. Expected Plane binding = {topmost_rgb_plane} Actual = {plane_binding_value}")
                gdhm.report_driver_bug_pc("[Powercons][FBC] FBC is not enabled on the top-most RGB plane")
                return False
            logging.info("PASS : FBC is enabled on the top-most RGB plane")

    if expected_fbc_status != actual_fbc_status:
        logging.error(
            "FAIL: FBC status Expected= {0}, Actual= {1}, Restrictions= {2}".format(
                "ENABLED" if expected_fbc_status else "DISABLED",
                "ENABLED" if actual_fbc_status else "DISABLED", restriction_list))
        gdhm.report_driver_bug_pc(title="[PowerCons][FBC] FBC status in Driver with restrictions= {0}: Expected= {1} & Actual= {2}"
                  "".format(restriction_list, "ENABLED" if expected_fbc_status else "DISABLED",
                            "ENABLED" if actual_fbc_status else "DISABLED"))
        status = False
    if status:
        logging.info("PASS: FBC status Expected= {0}, Actual= {0}, Restrictions= {1}".format(
            "ENABLED" if actual_fbc_status else "DISABLED", restriction_list))
    else:
        logging.error("FAIL: FBC verification failed")
    return status


##
# @brief        Exposed API for FBC verification for all adapters
# @param[in]    gfx_index: String, adapter index
# @param[in]    is_display_engine_test: Boolean, If the test is D-Engine test
# @return       True if FBC verification is passed, False otherwise
def verify_fbc(gfx_index='gfx_0', is_display_engine_test=True):
    # Workaround
    # In pre-si Fulsim, we are getting sporadic 'single' async flip, and disabling FBC because of this. The next flip
    # is coming with sync flag without any parameter change, hence FBC enabling path is not getting called, in address
    # only update. Issue is observed majorly in EHL and TGL pre-si platforms, but it's possible for this to happen in
    # other pre-si platforms also.
    # Disabling the FBC verification for pre-si platforms for now.
    # Sighting: 1607779683
    if IS_PRE_SI and is_display_engine_test:
        return True

    ##
    # FBC is not supported for 10/12 in driver. We need to skip this verification.
    bpc = DSCHelper.get_bpc_from_registry(gfx_index)
    if bpc == 10 or bpc == 12:
        logging.info("BPC value from registry is %s. Skipping FBC verification as FBC not supported for 10/12 BPC", bpc)
        return True

    return verify_adapter_fbc(gfx_index)


##
# @brief        Exposed API to enable FBC for given adapter
# @param[in]    gfx_index: String, adapter index
# @return       True if FBC enable is successful, False if FBC enable is failed, None if FBC is already enabled
def enable(gfx_index):
    # Validate arguments
    if gfx_index is None or not isinstance(gfx_index, str) or not gfx_index.lower().startswith('gfx_'):
        raise Exception("Invalid arguments: gfx_index= {0}".format(gfx_index))

    gfx_index = gfx_index.lower()
    feature_test_ctl = registry.FeatureTestControl(gfx_index)

    # Return if FBC is already enabled
    if feature_test_ctl.fbc_disable == 0:
        logging.info("FBC is already enabled")
        return None

    # Enable FBC via FeatureTestControl RegKey
    feature_test_ctl.fbc_disable = 0
    if feature_test_ctl.update(gfx_index) is False:
        logging.error("\tFailed to enable FBC in FeatureTestControl")
        gdhm.report_test_bug_pc("[Powercons][FBC] Failed to enable FBC in FeatureTestControl")
        return False
    logging.info("Successfully enabled FBC via RegKey")
    return True


##
# @brief        Exposed API to disable FBC for given adapter
# @param[in]    gfx_index: String, adapter index
# @return       True if FBC disable is successful, False if FBC disable is failed, None if FBC is already disabled
def disable(gfx_index):
    # Validate arguments
    if gfx_index is None or not isinstance(gfx_index, str) or not gfx_index.lower().startswith('gfx_'):
        raise Exception("Invalid arguments: gfx_index= {0}".format(gfx_index))

    gfx_index = gfx_index.lower()
    feature_test_ctl = registry.FeatureTestControl(gfx_index)

    # Return if FBC is already disabled
    if feature_test_ctl.fbc_disable == 1:
        logging.info("FBC is already disabled")
        return None

    # Disable FBC via FeatureTestControl RegKey
    feature_test_ctl.fbc_disable = 1
    if feature_test_ctl.update(gfx_index) is False:
        logging.error("\tFailed to disable FBC in FeatureTestControl")
        gdhm.report_test_bug_pc("[Powercons][FBC] Failed to disable FBC in FeatureTestControl")
        return False
    logging.info("Successfully disabled FBC via RegKey")
    return True


##
# @brief        Exposed API to check PSR and FBC concurrency
# @param[in]    plane_ctl_register plane_ctl_register
# @param[in]    platform_name platform_name
# @param[in]    gfx_index gfx_index
# @param[in]    pipe pipe
# @param[in]    transcoder transcoder
# @param[in]    fbc_psr2_coexistence_status FBC PSR2 co-existence status in RegKey
# @return       status - True if verification is successful. False otherwise. rstn_list - Restriction list
def check_fbc_psr_pr_concurrency(plane_ctl_register, platform_name, gfx_index, pipe, transcoder, fbc_psr2_coexistence_status):
    enabled_plane_count = 0
    cff_ctl = None
    is_pr_enabled = False
    rstn_list = []
    # Find out the number of enabled planes for verification
    for plane in ['1', '2', '3']:
        plane_ctl_for_cnt = MMIORegister.read('PLANE_CTL_REGISTER', f'PLANE_CTL_{plane}_{pipe}', platform_name, gfx_index=gfx_index)
        if plane_ctl_for_cnt.plane_enable == plane_ctl_register.plane_enable_ENABLE:
            enabled_plane_count += 1

    srd_ctl_reg = MMIORegister.read('SRD_CTL_REGISTER', f'SRD_CTL_{transcoder}', platform_name, gfx_index=gfx_index)
    psr2_ctl_reg = MMIORegister.read('PSR2_CTL_REGISTER', f'PSR2_CTL_{transcoder}', platform_name, gfx_index=gfx_index)
    if platform_name not in machine_info.PRE_GEN_15_PLATFORMS:
        cff_ctl = MMIORegister.read("CFF_CTL_REGISTER", f"CFF_CTL_{pipe}", platform_name, gfx_index=gfx_index)
        pr_ctl = MMIORegister.read('TRANS_DP2_CTL_REGISTER', 'TRANS_DP2_CTL_' + transcoder, platform_name,
                                   gfx_index=gfx_index)
        is_pr_enabled = pr_ctl.pr_enable == 1

    current_fbc_status_in_driver = get_fbc_enable_status(gfx_index, pipe)
    port = [key for key, value in display_base.get_port_to_pipe(gfx_index=gfx_index).items() if
                    value == 'PIPE_' + pipe][0]
    psr1_panel = __display_psr.is_psr_supported_in_panel(DriverPsrVersion.PSR_1, edp_port=port)
    psr2_panel = __display_psr.is_psr_supported_in_panel(DriverPsrVersion.PSR_2, edp_port=port)
    pr_panel = __display_psr.is_pr_supported_in_panel(edp_port=port)
    is_psr1_only_supported = psr1_panel and not psr2_panel
    is_psr1_enabled = srd_ctl_reg.srd_enable == 1
    is_psr2_enabled = psr2_ctl_reg.psr2_enable == 1

    logging.info(f"PSR1 enable status : {is_psr1_enabled}")
    logging.info(f"PSR2 enable status : {is_psr2_enabled}")
    logging.info(f"PR enable status : {is_pr_enabled}")

    if platform_name in machine_info.PRE_GEN_15_PLATFORMS and (not pr_panel):
        psr_line_time_rstn_status = False
        cpu_stepping = __get_cpu_stepping()
        if psr2_panel:
            psr_line_time_rstn_status = __display_psr.check_psr_line_time(port, transcoder, gfx_index)
        is_psr1_only_supported = (psr1_panel and not psr2_panel) or (psr2_panel and not psr_line_time_rstn_status)
        sku_name = machine_info.SystemInfo().get_sku_name(gfx_index)
        is_fbc_psr1_possible = (platform_name in ['MTL'] and cpu_stepping >= '4') or (platform_name in ['MTL'] and sku_name in ['ARL'])

        # PSR1 + FBC is supported on MTL C0 stepping and ARL
        if not(is_psr1_only_supported and is_fbc_psr1_possible):
            # PSR might get disabled due to setup time restriction for some platforms
            psr_setup_time_rstn_status = False
            psr_disable = False
            if platform_name not in machine_info.GEN_11_PLATFORMS + ['TGL', 'RKL', 'DG1'] and platform_name in machine_info.PRE_GEN_15_PLATFORMS:
                psr_setup_time_rstn_status = __display_psr.check_psr_setup_time(gfx_index, port, transcoder, platform_name)
                if psr_setup_time_rstn_status is None:
                    return False, rstn_list

            feature_test_control = registry.FeatureTestControl(gfx_index)
            if feature_test_control.psr_disable == 1:
                psr_disable = True
            if not psr_setup_time_rstn_status and not psr_disable:
                rstn_list.append('PSR_PANEL')
        return True, rstn_list

    # For PSR2, FBC+PSR2 co-existence is allowed. Driver enables FBC+PSR2 whenever based on RegKey
    # FBC+PSR2 will be allowed whenever Bit26 is set to 0 in DisplayPcFeatureControl RegKey
    if is_psr1_only_supported:
        if not current_fbc_status_in_driver:
            gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC is not enabled for PSR1 panel")
            logging.error("FBC is not enabled for PSR1 panel")
            return False, rstn_list
        logging.info("FBC is enabled for PSR1 panel")
        return True, rstn_list
    restriction = 'PR_PANEL' if pr_panel else 'PSR_PANEL'
    if not fbc_psr2_coexistence_status:
        rstn_list.append(restriction)
        return True, rstn_list

    # FBC is expected to get disabled for single plane scenarios
    if enabled_plane_count == 1:
        if current_fbc_status_in_driver:
            gdhm.report_driver_bug_pc(f"[PowerCons][FBC] FBC is enabled with single plane in {restriction}")
            logging.error(f"FBC is enabled with single plane in {restriction}")
            return False, rstn_list
        logging.info(f"PASS : FBC is disabled with single plane in {restriction}")
        rstn_list.append(restriction)
    elif enabled_plane_count > 1:
        # When more than 2 planes are enabled and there are no FBC restrictions, whenever FBC gets enabled,
        # it has to get enabled with PSR2 Continuous Full Fetch
        if current_fbc_status_in_driver:
            is_cff, _ = sfsu.verify_su_mode(platform_name, None, cff_ctl,
                                            requested_su_mode=[sfsu.SuType.SU_CONTINUOUS_UPDATE])
            if not is_cff:
                gdhm.report_driver_bug_pc("[PowerCons][FBC] FBC is not enabled with CFF")
                logging.error("FBC is not enabled with CFF")
                return False, rstn_list
            logging.info("PASS : FBC has got enabled with CFF")
    return True, rstn_list

##
# @brief        API to verify FBC dirty rectangle programming
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    rect_data Dirty rectangle update on the screen(Top scanline, bottom scanline)
# @return       True if verification is successful. False otherwise
def verify_fbc_dirty_rectangle(adapter, panel, rect_data):
    fbc_dirty_ctl = MMIORegister.read("FBC_DIRTY_CTL_REGISTER", f"FBC_DIRTY_CTL_{panel.pipe}", adapter.name, gfx_index=adapter.gfx_index)
    fbc_dirty_rect_reg = MMIORegister.read("FBC_DIRTY_RECTANGLE_REGISTER", f"FBC_DIRTY_RECTANGLE_{panel.pipe}", adapter.name, gfx_index=adapter.gfx_index)
    expected_dirty_rect_top = rect_data[0]
    expected_dirty_rect_bottom = rect_data[1]
    actual_dirty_rect_top = fbc_dirty_rect_reg.start_line
    actual_dirty_rect_bottom = fbc_dirty_rect_reg.end_line

    if fbc_dirty_ctl.dirty_rectangle_enable != 1:
        logging.error(f"FBC Dirty CTL is not enabled from driver for screen update Top = {expected_dirty_rect_top} Bottom = {expected_dirty_rect_bottom}")
        gdhm.report_driver_bug_pc("[Powercons][FBC] FBC Dirty CTL is not enabled from driver")
        return False
    logging.info(f"FBC Dirty CTL is enabled from driver for screen update Top = {expected_dirty_rect_top} Bottom = {expected_dirty_rect_bottom}")

    if expected_dirty_rect_top != actual_dirty_rect_top or (expected_dirty_rect_bottom-1) != actual_dirty_rect_bottom:
        logging.error(f"FAIL : Expected Dirty rectangle values(Top, Bottom) : ({expected_dirty_rect_top}, {expected_dirty_rect_bottom}). "
                      f"Actual({actual_dirty_rect_top}, {actual_dirty_rect_bottom}) :")
        gdhm.report_driver_bug_pc("[Powercons][FBC] Unexpected FBC dirty rectangle programming from driver")
        return False
    logging.info(f"PASS : Expected Dirty rectangle values(Top, Bottom) : ({expected_dirty_rect_top}, {expected_dirty_rect_bottom-1}). "
                 f"Actual({actual_dirty_rect_top}, {actual_dirty_rect_bottom}) :")
    return True

##
# @brief        API to get bpp value by pixel format
# @param[in]    pixel_format Pixel format
# @return       Bpp Value
def get_BPP_from_pixel_format(pixel_format):
    bpp_value = None
    if pixel_format == "DD_8BPP_INDEXED":
        bpp_value = 8
    elif pixel_format == "DD_NV12YUV420":
        bpp_value = 12
    elif pixel_format in ["DD_YUV422_8", "DD_B5G6R5X0"]:
        bpp_value = 16
    elif pixel_format in ["DD_P010YUV420", "DD_P012YUV420", "DD_P016YUV420"]:
        bpp_value = 24
    elif pixel_format in ["DD_B8G8R8X8", "DD_R8G8B8X8", "DD_B10G10R10X2", "DD_R10G10B10X2", "DD_R10G10B10X2_XR_BIAS",
                         "DD_YUV422_10", "DD_YUV422_12", "DD_YUV422_16", "DD_YUV444_8", "DD_YUV444_10"]:
        bpp_value = 32
    elif pixel_format in ["DD_YUV444_12", "DD_YUV444_16", "DD_R16G16B16X16F"]:
        bpp_value = 64
    else:
        print("Unexpected Pixel Format:", pixel_format)
        bpp_value = 32  # default
    return bpp_value


##
# @brief        API to align a particular value with another value
# @param[in]    value_to_align Value to align
# @param[in]    value_to_be_aligned_with Value to be aligned with
# @return       Aligned value
def DD_ALIGN(value_to_align, value_to_be_aligned_with):
    return ((value_to_align + (value_to_be_aligned_with - 1)) - ((value_to_align + (value_to_be_aligned_with - 1)) & (value_to_be_aligned_with - 1)))


##
# @brief        API to verify the status of display stride vs plane stride
# @param[in]    pipe Pipe
# @param[in]    gfx_index Gfx Index
# @param[in]    pixel_format Plane pixel format
# @param[in]    platform_name Platform/Adapter name
# @param[in]    plane_id HW Plane ID
# @param[in]    plane_ctl Plane CTL register instance
# @return       stride_rstn_list Restriction string list if Plane stride > Display stride. Empty list otherwise
def __verify_fbc_stride(pipe, gfx_index, pixel_format, platform_name, plane_id, plane_ctl):
    stride_rstn_list = []
    plane_stride_in_bytes = 0
    port = [key for key, value in display_base.get_port_to_pipe(gfx_index=gfx_index).items() if
             value == 'PIPE_' + pipe][0]

    bpp_value = get_BPP_from_pixel_format(pixel_format)
    display_and_adapter_info = __display_config.get_display_and_adapter_info_ex(port, gfx_index)
    if type(display_and_adapter_info) is list:
        display_and_adapter_info = display_and_adapter_info[0]

    if display_and_adapter_info is None:
        raise Exception("Failed to get DisplayAndAdapterInfo for {0} on {1}".format(port, gfx_index))

    current_mode = __display_config.get_current_mode(display_and_adapter_info)

    display_stride_in_bytes = DD_ALIGN(int(current_mode.HzRes * (bpp_value / 8)), 512)
    plane_stride_reg = MMIORegister.read("PLANE_STRIDE_REGISTER", f"PLANE_STRIDE_{str(plane_id)}_{pipe}", platform_name, gfx_index=gfx_index)

    if plane_ctl.tiled_surface == 5:
        plane_stride_in_bytes = plane_stride_reg.stride * 128
    elif plane_ctl.tiled_surface == 1:
        plane_stride_in_bytes = plane_stride_reg.stride * 512
    else:
        plane_stride_in_bytes = plane_stride_reg.stride * 64

    logging.debug(f"Tiled surface : {plane_ctl.tiled_surface}")
    logging.debug(f"BPP value : {bpp_value}")
    logging.info(f"Display Stride in bytes : {display_stride_in_bytes}")
    logging.info(f"Plane Stride in bytes : {plane_stride_reg.stride} ({plane_stride_in_bytes}bytes)")

    if plane_stride_in_bytes <= display_stride_in_bytes:
        logging.info("FBC CONDITION SUCCESS : Plane stride is not more than Display stride")
    else:
        logging.info("FBC CONDITION FAILED : Plane stride is larger than Display stride")
        stride_rstn_list.append("PLANE_STRIDE_LARGER_THAN_DISPLAY_STRIDE")
    return stride_rstn_list



##
# @brief        API to verify the status of Plane size vs FBC Pipe size
# @param[in]    gfx_index Gfx Index
# @param[in]    pipe Pipe
# @param[in]    plane_size_reg Plane Size register instance
# @return       pipe_rstn_lst Restriction string list if FBC Pipe size is less than Plane Size. Empty list otherwise
def __verify_fbc_pipe_size(gfx_index, pipe, plane_size_reg):
    pipe_rstn_lst = []
    port = [key for key, value in display_base.get_port_to_pipe(gfx_index=gfx_index).items() if
             value == 'PIPE_' + pipe][0]
    display_and_adapter_info = __display_config.get_display_and_adapter_info_ex(port, gfx_index)
    if display_and_adapter_info is None:
        raise Exception("Failed to get DisplayAndAdapterInfo for {0} on {1}".format(port, gfx_index))

    # Fetch Pipe and Plane sizes
    current_mode = __display_config.get_current_mode(display_and_adapter_info)
    fbc_pipe_size = current_mode.HzRes * current_mode.VtRes
    plane_size_x = plane_size_reg.width + 1
    plane_size_y = plane_size_reg.height + 1

    #  To enable Fbc, (PlaneResX*PlaneResY) <= FbcPipeSize. FbcPipeSize is calculated based on Source size. Same SourceSizeX is cached in PipeContext in pipe joiner mode.
    #  Ex: For 38x21 pipe joiner mode, SourceX in PipeContext for both the pipes in pipe joiner mode is 3840. So, FbcPipeSize calculated based on SourceX needs to be divided by NumberOfPipes.
    is_pipe_joiner_required, no_of_pipe_required = DisplayClock.is_pipe_joiner_required(
                                gfx_index, port)
    if is_pipe_joiner_required:
        fbc_pipe_size /= no_of_pipe_required

    logging.info(f"Plane Size (X * Y) : {(plane_size_x * plane_size_y)}")
    logging.info(f"FBC Pipe Size : {fbc_pipe_size}")

    if (plane_size_x * plane_size_y) <= fbc_pipe_size:
        logging.info("FBC CONDITION SUCCESS : FBC Pipe Size is less than Plane size")
    else:
        logging.info("FBC CONDITION FAILED : FBC Pipe Size is greater than Plane size")
        pipe_rstn_lst.append("PLANE_LARGER_THAN_SCREEN_RESOLUTION")
    return pipe_rstn_lst


def __get_transcoder(port, gfx_index):
    display_base_obj = display_base.DisplayBase(port, gfx_index=gfx_index)
    trans, _ = display_base_obj.get_transcoder_and_pipe(port, gfx_index)
    if trans == 0:
        transcoder = 'EDP'
    elif trans == 5:
        transcoder = 'DSI0'
    elif trans == 6:
        transcoder = 'DSI1'
    else:
        transcoder = chr(int(trans) + 64)
    return transcoder

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

