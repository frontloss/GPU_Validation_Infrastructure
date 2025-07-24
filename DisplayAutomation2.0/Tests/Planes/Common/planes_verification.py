########################################################################################################################
# @file         planes_verification.py
# @brief        This script contains function that are used for register verification for planes.
# @author       Shetty, Anjali N
########################################################################################################################
import importlib
import logging

from Libs.Core import flip, registry_access
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.machine_info import machine_info
from Libs.Core.system_utility import SystemUtility
from registers.mmioregister import MMIORegister
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Feature.clock.display_clock import DisplayClock

reg_read = MMIORegister()
system_info = SystemInfo()
platform = []
display_config = DisplayConfiguration()

gfx_display_hwinfo = system_info.get_gfx_display_hardwareinfo()
for i in range(len(gfx_display_hwinfo)):
    platform.append(str(gfx_display_hwinfo[i].DisplayAdapterName).lower())

PLANE_MAX = 3


##
# @brief            Check plane reordering status from DFC2
# @param[in]	    gfx_adapter_index; gfx_index
# @return		    layer_reordering_enable; True if layer reordering is enabled else false
def check_layer_reordering(gfx_adapter_index='gfx_0'):
    index = gfx_adapter_index.split('_')
    gfx_index = int(index[1])

    if platform[gfx_index].upper() in machine_info.PRE_GEN_15_PLATFORMS:
        layer_reordering_enable = True
    else:
        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        registry_value, registry_type = \
            registry_access.read(args=ss_reg_args, reg_name="DisplayFeatureControl2")

        ##
        # Some platforms will not have DisplayFeatureControl2 by default, making the value
        # 0 if registry value read is none
        registry_value = registry_value if registry_value is not None else 0

        ##
        # bit7 in DFC2 will be set if Plane reordering is enabled. Plane reordering is disabled from LNL.
        layer_reordering_enable = True if registry_value & (1 << 7) else False

    return layer_reordering_enable


##
# @brief            Get the register string for pixel format
# @param[in]	    pixel_format; Pixel format of the plane
# @return		    Register string for the given pixel format
def get_register_string_from_pixel_format(pixel_format):
    return {
        1: 'source_pixel_format_INDEXED_8_BIT',
        2: 'source_pixel_format_RGB_565',
        3: 'source_pixel_format_RGB_8888',
        4: 'source_pixel_format_RGB_8888',
        5: 'source_pixel_format_RGB_8888',
        6: 'source_pixel_format_RGB_8888',
        7: 'source_pixel_format_RGB_2101010',
        8: 'source_pixel_format_RGB_2101010',
        9: 'source_pixel_format_RGB_2101010',
        10: 'source_pixel_format_RGB_2101010',
        11: 'source_pixel_format_RGB_2101010_XR_BIAS',
        12: 'source_pixel_format_RGB_16161616_FLOAT',
        13: 'source_pixel_format_RGB_16161616_FLOAT',
        15: 'source_pixel_format_NV12_YUV_420',
        16: 'source_pixel_format_YUV_422_PACKED_8_BPC',
        17: 'source_pixel_format_P010_YUV_420_10_BIT',
        18: 'source_pixel_format_P012_YUV_420_12_BIT',
        19: 'source_pixel_format_P016_YUV_420_16_BIT',
        20: 'source_pixel_format_YUV_444_PACKED_10_BPC',
        21: 'source_pixel_format_YUV_422_PACKED_10_BPC',
        22: 'source_pixel_format_YUV_422_PACKED_12_BPC',
        23: 'source_pixel_format_YUV_422_PACKED_16_BPC',
        24: 'source_pixel_format_YUV_444_PACKED_8_BPC',
        25: 'source_pixel_format_YUV_444_PACKED_12_BPC',
        26: 'source_pixel_format_YUV_444_PACKED_16_BPC'
    }[pixel_format]


##
# @brief            Get the pixel format string for logging
# @param[in]	    pixel_format; Pixel format of the plane
# @return		    Pixel format string for the given pixel format
def get_pixel_format_string(pixel_format):
    return {
        0: 'YUV422_8BPC',
        1: 'YUV422_10BPC',
        2: 'YUV420_8BPC',
        3: 'YUV422_12BPC',
        4: 'RGB2101010',
        5: 'YUV422_16BPC',
        6: 'YUV420_10BPC',
        7: 'YUV444_10BPC',
        8: 'RGB8888',
        9: 'YUV444_12BPC',
        10: 'YUV420_12BPC',
        11: 'YUV444_16BPC',
        12: 'RGB16_FLOAT',
        14: 'YUV420_16BPC',
        16: 'YUV444_8BPC',
        18: 'RGB16_UINT',
        20: 'RGB2101010_XRBIAS',
        24: 'INDEXED_8BIT',
        28: 'RGB565'
    }[pixel_format]


##
# @brief            Get the pixel format string for legacy platforms for logging
# @param[in]	    pixel_format; Pixel format of the plane
# @return		    Pixel format; string for the given pixel format
def get_pixel_format_string_legacy(pixel_format):
    return {
        0: 'YUV422_8BPC',
        1: 'YUV420_8BPC',
        2: 'RGB2101010',
        3: 'YUV420_10BPC',
        4: 'RGB8888',
        5: 'YUV420_12BPC',
        6: 'RGB16_FLOAT',
        7: 'YUV420_16BPC',
        8: 'YUV444_8BPC',
        9: 'RGB16_UINT',
        10: 'RGB2101010_XRBIAS',
        12: 'INDEXED_8BIT',
        14: 'RGB565'
    }[pixel_format]


##
# @brief            Get the register string for tile format
# @param[in]	    tile_format; Tile format of the plane
# @return		    Register string for the given tile format
def get_register_string_from_tile_format(tile_format):
    return {
        1: 'tiled_surface_LINEAR_MEMORY',
        2: 'tiled_surface_TILE_X_MEMORY',
        4: 'tiled_surface_TILE_Y_LEGACY_MEMORY',
        16: 'tiled_surface_TILE_4_MEMORY'
    }[tile_format]


##
# @brief            Get the tile format string for logging
# @param[in]	    tile_format; Tile format of the plane
# @return		    Tile format string for the given tile format
def get_tile_format_string(tile_format):
    return {
        0: 'Linear',
        1: 'X Tile',
        4: 'Y Tile',
        5: 'Tile4'
    }[tile_format]


##
# @brief            Get the scalar mode string
# @param[in]	    scalar_mode; Scalar mode of the plane
# @return		    Scalar mode string for the given scalar mode
def get_programmed_scalar_mode_string(scalar_mode):
    return {
        0: 'Scalar Mode Normal',
        1: 'Scalar Mode Planar'
    }[scalar_mode]


##
# @brief            To get plane status in string
# @param[in]        plane_status; boolean value (0/1)
# @return           plane status string for given plane status
def get_plane_status_string(plane_status):
    return {
        0: 'Plane disabled',
        1: "Plane enabled"
    }[plane_status]


##
# @brief            To get pipe details
# @param[in]        value; integer value
# @return           The name of the pipe
def get_pipe_details(value):
    return {
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'D'
    }[value]


##
# @brief            Verification of plane enable status
# @param[in]	    pipe_id; Source id of the plane
# @param[in]	    plane_id; Plane Ctl id of the plane
# @param[in]        enable
# @param[in]        gfx_adapter_index; graphic adapter index
# @return		    Return 1(True) for successful verification of plane enable status, else 0(False)
def verify_plane_status(pipe_id, plane_id, enable, gfx_adapter_index='gfx_0'):
    system_utility = SystemUtility()
    is_ddrw = system_utility.is_ddrw(gfx_adapter_index)

    index = gfx_adapter_index.split('_')
    gfx_index = int(index[1])

    ##
    # Import PLANE_CTL_REGISTER module.
    plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % platform[gfx_index])

    current_pipe = chr(int(pipe_id) + 65)
    plane_ctl_reg = 'PLANE_CTL_' + str(plane_id) + '_' + current_pipe

    ##
    # Read PLANE_CTL_REGISTER values.
    plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, platform[gfx_index], 0x0)

    ##
    # Programmed value of plane enable bit.
    plane_enable = plane_ctl_value.__getattribute__("plane_enable")

    ##
    # Check plane status.
    if plane_enable == enable:
        logging.info("PASS: {} Plane enable status - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                     get_plane_status_string(enable),
                                                                                     get_plane_status_string(
                                                                                         plane_enable)))
        return True
    else:
        logging.error("FAIL: {} Plane enable status - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                      get_plane_status_string(enable),
                                                                                      get_plane_status_string(
                                                                                          plane_enable)))
        return False


##
# @brief            Verification of plane programming with respect to PLANE_CTL register
# @param[in]	    pipe_id; Source id of the plane
# @param[in]	    plane_id; Plane Ctl id of the plane
# @param[in]	    pixel_format; Pixel format of the plane
# @param[in]	    tile_format; Tile format of the plane
# @param[in]        gfx_index; graphic index
# @param[in]        enable
# @return		    Return 1(True) for successful verification of plane programming, else 0(False)
def verify_plane_ctl_programming(pipe_id, plane_id, pixel_format, tile_format, gfx_index, enable):
    ##
    # Import PLANE_CTL_REGISTER module.
    plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % platform[gfx_index])

    current_pipe = chr(int(pipe_id) + 65)
    plane_ctl_reg = 'PLANE_CTL_' + str(plane_id) + '_' + current_pipe

    ##
    # Read PLANE_CTL_REGISTER values.
    plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, platform[gfx_index], 0x0)

    ##
    # Programmed value of plane enable bit.
    plane_enable = plane_ctl_value.__getattribute__("plane_enable")

    ##
    # Check if the Plane is enabled.
    if plane_enable == enable:
        logging.info("PASS: {} Plane enable status - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                     get_plane_status_string(enable),
                                                                                     get_plane_status_string(
                                                                                         plane_enable)))

        ##
        # Programmed value of source pixel format.
        programmed_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")

        ##
        # Expected value of pixel format to be programmed.
        expected_pixel_format = getattr(plane_ctl, get_register_string_from_pixel_format(pixel_format))
        if programmed_pixel_format != expected_pixel_format:
            logging.error("Fail: {} Pixel Format - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                   get_pixel_format_string(
                                                                                       expected_pixel_format),
                                                                                   get_pixel_format_string(
                                                                                       programmed_pixel_format)))
            return False
        else:
            logging.info("Pass: {} Pixel Format - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                  get_pixel_format_string(
                                                                                      expected_pixel_format),
                                                                                  get_pixel_format_string(
                                                                                      programmed_pixel_format)))

            if pixel_format in [flip.SB_PIXELFORMAT.SB_NV12YUV420, flip.SB_PIXELFORMAT.SB_P010YUV420,
                                flip.SB_PIXELFORMAT.SB_P012YUV420, flip.SB_PIXELFORMAT.SB_P016YUV420]:
                planar_yuv420_component = plane_ctl_value.__getattribute__("planar_yuv420_component")

                if planar_yuv420_component:
                    logging.debug("{} Y Plane".format(plane_ctl_reg))
                else:
                    logging.debug("{} UV Plane".format(plane_ctl_reg))

        programmed_tile_format = plane_ctl_value.__getattribute__("tiled_surface")
        expected_tile_format = getattr(plane_ctl, get_register_string_from_tile_format(tile_format))
        logging.info("{} Tile Format - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                       get_tile_format_string(
                                                                           expected_tile_format),
                                                                       get_tile_format_string(
                                                                           programmed_tile_format)))

    else:
        logging.error("FAIL: {} Plane enable status - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                      get_plane_status_string(enable),
                                                                                      get_plane_status_string(
                                                                                          plane_enable)))
        return False

    return True


##
# @brief            Verification of planar programming for planar formats
# @param[in]	    pipe_id; Source id of the plane
# @param[in]	    plane_id; Plane Ctl id of the plane
# @param[in]	    pixel_format; Pixel format of the plane
# @param[in]	    tile_format; Tile format of the plane
# @param[in]        width; Width of the plane
# @param[in]        gfx_index; graphic index
# @param[in]        enable
# @return		    Return 1(True) for successful verification of planar programming, else 0(False).
def verify_planar_programming(pipe_id, plane_id, pixel_format, tile_format, width, gfx_index, enable):
    if platform[gfx_index] in ['icllp', 'tgl', 'lkf1', 'dg1', 'jsl']:
        y1, y2 = 6, 7
    else:
        y1, y2 = 4, 5

    if plane_id < 3 and 8 <= width <= 4096:
        ##
        # Import PLANE_CUS_CTL_REGISTER module.
        plane_cus_ctl = importlib.import_module("registers.%s.PLANE_CUS_CTL_REGISTER" % platform[gfx_index])
        current_pipe = chr(int(pipe_id) + 65)
        plane_cus_ctl_reg = "PLANE_CUS_CTL_" + str(plane_id) + '_' + current_pipe

        ##
        # Read PLANE_CUS_CTL_REGISTER values.
        plane_cus_ctl_value = reg_read.read('PLANE_CUS_CTL_REGISTER', plane_cus_ctl_reg, platform[gfx_index], 0x0)

        if (getattr(plane_cus_ctl, 'chroma_upsampler_enable_ENABLE') == plane_cus_ctl_value.__getattribute__(
                'chroma_upsampler_enable')):
            logging.info("Pass: Chroma Up Sampler is enabled for the format {}".format(
                get_register_string_from_pixel_format(pixel_format)))
            if (getattr(plane_cus_ctl, 'y_binding_PLANE_' + str(y1)) == plane_cus_ctl_value.__getattribute__(
                    'y_binding')):
                if not verify_plane_ctl_programming(pipe_id, y1, pixel_format, tile_format, gfx_index, enable):
                    return False
            elif (getattr(plane_cus_ctl, 'y_binding_PLANE_' + str(y2)) == plane_cus_ctl_value.__getattribute__(
                    'y_binding')):
                if not verify_plane_ctl_programming(pipe_id, y2, pixel_format, tile_format, gfx_index, enable):
                    return False
        else:
            logging.error("Fail: Chroma Up Sampler is not enabled for the format {}".format(
                get_register_string_from_pixel_format(pixel_format)))
            return False
    else:
        plane_scaler_ctl = importlib.import_module("registers.%s.PS_CTRL_REGISTER" % platform[gfx_index])
        current_pipe = chr(int(pipe_id) + 65)

        ps_ctrl_1_reg = "PS_CTRL_1_" + current_pipe
        ps_ctrl_2_reg = "PS_CTRL_2_" + current_pipe

        ps_ctrl_1_reg_value = reg_read.read('PS_CTRL_REGISTER', ps_ctrl_1_reg, platform[gfx_index], 0x0)
        ps_ctrl_2_reg_value = reg_read.read('PS_CTRL_REGISTER', ps_ctrl_2_reg, platform[gfx_index], 0x0)

        ##
        # Scalar1
        if (getattr(plane_scaler_ctl, 'enable_scaler_ENABLE') == ps_ctrl_1_reg_value.__getattribute__("enable_scaler")):
            if (plane_id == ps_ctrl_1_reg_value.__getattribute__("scaler_binding")):
                if (getattr(plane_scaler_ctl, 'scaler_mode_PLANAR') != ps_ctrl_1_reg_value.__getattribute__(
                        'scaler_mode')):
                    logging.error("Fail: {} Scalar mode is not matching - Expected: {} Actual: {}"
                                  .format(ps_ctrl_1_reg,
                                          get_programmed_scalar_mode_string(
                                              getattr(plane_scaler_ctl, 'scaler_mode_PLANAR')),
                                          get_programmed_scalar_mode_string(
                                              ps_ctrl_1_reg_value.__getattribute__('scaler_mode'))))
                    return False
                else:
                    if (getattr(plane_scaler_ctl, 'scaler_binding_y_PLANE_' + str(y1) + '_SCALER') ==
                            ps_ctrl_1_reg_value.__getattribute__('scaler_binding_y')):
                        if not verify_plane_ctl_programming(pipe_id, y1, pixel_format, tile_format, gfx_index):
                            return False
                    elif (getattr(plane_scaler_ctl, 'scaler_binding_y_PLANE_' + str(y2) + '_SCALER') ==
                          ps_ctrl_1_reg_value.__getattribute__('scaler_binding_y')):
                        if not verify_plane_ctl_programming(pipe_id, y2, pixel_format, tile_format, gfx_index):
                            return False

        elif (getattr(plane_scaler_ctl, 'enable_scaler_ENABLE') == ps_ctrl_2_reg_value.__getattribute__(
                "enable_scaler")):
            if (plane_id == ps_ctrl_2_reg_value.__getattribute__("scaler_binding")):
                if (getattr(plane_scaler_ctl,
                            'scaler_mode_PLANAR') != ps_ctrl_2_reg_value.__getattribute__(
                    'scaler_mode')):
                    logging.error("Fail: {} Scalar mode is not matching - Expected: {} Actual: {}"
                                  .format(ps_ctrl_2_reg,
                                          get_programmed_scalar_mode_string(
                                              getattr(plane_scaler_ctl, 'scaler_mode_PLANAR')),
                                          get_programmed_scalar_mode_string(
                                              ps_ctrl_2_reg_value.__getattribute__('scaler_mode'))))
                    return False
                else:
                    if (getattr(plane_scaler_ctl, 'scaler_binding_y_PLANE_' + str(y1) + '_SCALER') ==
                            ps_ctrl_2_reg_value.__getattribute__('scaler_binding_y')):
                        if not verify_plane_ctl_programming(pipe_id, y1, pixel_format,
                                                            tile_format, gfx_index):
                            return False
                    elif (getattr(plane_scaler_ctl, 'scaler_binding_y_PLANE_' + str(y2) + '_SCALER') ==
                          ps_ctrl_2_reg_value.__getattribute__('scaler_binding_y')):
                        if not verify_plane_ctl_programming(pipe_id, y2, pixel_format,
                                                            tile_format, gfx_index):
                            return False
        else:
            logging.error("Fail: No Up sampler enabled for pixel format {}".format(
                get_register_string_from_pixel_format(pixel_format)))
            return False

    return True


##
# @brief            Verification of scalar plane window and position programming
# @param[in]	    pipe_id; Source id of the plane
# @param[in]	    scalar_id; Scalar id of the plane
# @param[in]	    left; Left co-ordinate of the plane
# @param[in]	    right; Right co-ordinate of the plane
# @param[in]	    top; Top co-ordinate of the plane
# @param[in]	    bottom; Bottom co-ordinate of the plane
# @param[in]        gfx_index; graphics index
# @return		    Return 1(True) for successful verification of planar programming, else 0(False)
def verify_scalar_window_position_size(pipe_id, scalar_id, left, right, top, bottom, gfx_index):
    ps_win_position = importlib.import_module("registers.%s.PS_WIN_POS_REGISTER" % platform[gfx_index])
    ps_win_size = importlib.import_module("registers.%s.PS_WIN_SZ_REGISTER" % platform[gfx_index])
    current_pipe = chr(int(pipe_id) + 65)

    ps_win_pos_reg = "PS_WIN_POS_" + str(scalar_id) + '_' + current_pipe
    ps_win_position_value = reg_read.read('PS_WIN_POS_REGISTER', ps_win_pos_reg, platform[gfx_index], 0x0)

    ##
    ## Verify window position
    if (left != ps_win_position_value.__getattribute__('xpos')):
        logging.error('FAIL: {} Scalar WindowXPos not matching -  Expected: {} Actual: {}'
                      .format(ps_win_pos_reg, left, ps_win_position_value.__getattribute__('xpos')))
        return False
    else:
        logging.info('PASS: {} Scalar WindowXPos matching - Expected: {} Actual: {}'
                     .format(ps_win_pos_reg, left, ps_win_position_value.__getattribute__('xpos')))

    if (top != ps_win_position_value.__getattribute__('ypos')):
        logging.error('FAIL: {} Scalar WindowYPos not matching -  Expected: {} Actual: {}'
                      .format(ps_win_pos_reg, top, ps_win_position_value.__getattribute__('ypos')))
        return False
    else:
        logging.info('PASS: {} Scalar WindowYPos matching - Expected: {} Actual: {}'
                     .format(ps_win_pos_reg, top, ps_win_position_value.__getattribute__('ypos')))

    ps_win_sz_reg = "PS_WIN_SZ_" + str(scalar_id) + '_' + current_pipe
    ps_win_size_value = reg_read.read('PS_WIN_SZ_REGISTER', ps_win_sz_reg, platform[gfx_index], 0x0)

    ##
    # Verify Window size
    if ((right - left) != ps_win_size_value.__getattribute__('xsize')):
        logging.error("FAIL: {} Scalar WindowXSize not matching - Expected {} Actual {}"
                      .format(ps_win_sz_reg, (right - left), ps_win_size_value.__getattribute__('xsize')))
        return False
    else:
        logging.info("PASS: {} Scalar WindowXSize matching - Expected {} Actual {}"
                     .format(ps_win_sz_reg, (right - left), ps_win_size_value.__getattribute__('xsize')))

    if ((bottom - top) != ps_win_size_value.__getattribute__('ysize')):
        logging.error("FAIL: {} Scalar WindowYSize not matching - Expected {} Actual {}"
                      .format(ps_win_sz_reg, (bottom - top), ps_win_size_value.__getattribute__('ysize')))
        return False
    else:
        logging.info("PASS: {} Scalar WindowYSize matching - Expected {} Actual {}"
                     .format(ps_win_sz_reg, (bottom - top), ps_win_size_value.__getattribute__('ysize')))

    return True


##
# @brief            Verification of plane window and position programming
# @param[in]	    pipe_id; Source id of the plane
# @param[in]	    plane_id; Plane Ctl id of the plane
# @param[in]	    left; Left co-ordinate of the plane
# @param[in]	    right; Right co-ordinate of the plane
# @param[in]	    top; Top co-ordinate of the plane
# @param[in]	    bottom; Bottom co-ordinate of the plane
# @param[in]        gfx_index; graphic index
# @return		    Return 1(True) for successful verification of planar programming, else 0(False)
def verify_plane_window_position_size(pipe_id, plane_id, left, right, top, bottom, gfx_index):
    plane_position = importlib.import_module("registers.%s.PLANE_POS_REGISTER" % platform[gfx_index])
    plane_size = importlib.import_module("registers.%s.PLANE_SIZE_REGISTER" % platform[gfx_index])
    current_pipe = chr(int(pipe_id) + 65)

    plane_pos_reg = "PLANE_POS_" + str(plane_id) + '_' + current_pipe
    plane_position_value = reg_read.read('PLANE_POS_REGISTER', plane_pos_reg, platform[gfx_index], 0x0)

    ##
    # Verify window position
    if (left != plane_position_value.__getattribute__('x_position')):
        logging.error("FAIL: {} Plane WindowXPos not matching - Expected {} Actual {}"
                      .format(plane_pos_reg, left, plane_position_value.__getattribute__('x_position')))
        return False
    else:
        logging.info("PASS: {} Plane WindowXPos is matching - Expected {} Actual {}"
                     .format(plane_pos_reg, left, plane_position_value.__getattribute__('x_position')))

    if (top != plane_position_value.__getattribute__('y_position')):
        logging.error("FAIL: {} Plane WindowYPos not matching - Expected {} Actual {}"
                      .format(plane_pos_reg, top, plane_position_value.__getattribute__('y_position')))
        return False
    else:
        logging.info("PASS: {} Plane WindowYPos is matching - Expected {} Actual {}"
                     .format(plane_pos_reg, top, plane_position_value.__getattribute__('y_position')))

    plane_size_reg = "PLANE_SIZE_" + str(plane_id) + '_' + current_pipe
    plane_size_value = reg_read.read('PLANE_SIZE_REGISTER', plane_size_reg, platform[gfx_index], 0x0)

    ##
    # Verify window size
    if ((right - left) != (plane_size_value.__getattribute__('width') + 1)):
        logging.error("FAIL: {} Plane WindowXSize not matching - Expected {} Actual {}"
                      .format(plane_size_reg, (right - left), (plane_size_value.__getattribute__('width') + 1)))
        return False
    else:
        logging.info("PASS: {} Plane WindowXSize is matching - Expected {} Actual {}"
                     .format(plane_size_reg, (right - left), (plane_size_value.__getattribute__('width') + 1)))

    if ((bottom - top) != (plane_size_value.__getattribute__('height') + 1)):
        logging.error("FAIL: {} Plane WindowYSize not matching - Expected {} Actual {}"
                      .format(plane_size_reg, (bottom - top), (plane_size_value.__getattribute__('height') + 1)))
        return False
    else:
        logging.info("PASS: {} Plane WindowYSize is matching - Expected {} Actual {}"
                     .format(plane_size_reg, (bottom - top), (plane_size_value.__getattribute__('height') + 1)))

    return True


##
# @brief            Verification of plane window programming
# @param[in]	    pipe_id; Source id of the plane
# @param[in]	    plane_id; Plane Ctl id of the plane
# @param[in]        scalar_enable; Expected value for plane scalar to be enabled or disabled
# @param[in]	    left; Left co-ordinate of the plane
# @param[in]	    right; Right co-ordinate of the plane
# @param[in]	    top; Top co-ordinate of the plane
# @param[in]	    bottom; Bottom co-ordinate of the plane
# @param[in]        gfx_index; graphic index
# @return		    Return 1(True) for successful verification of planar programming, else 0(False)
def verify_plane_window_programming(pipe_id, plane_id, scalar_enable, left, right, top, bottom, gfx_index):
    scalar_id = 0
    plane_scaler_ctl = importlib.import_module("registers.%s.PS_CTRL_REGISTER" % platform[gfx_index])
    current_pipe = chr(int(pipe_id) + 65)

    ps_ctrl_1_reg = "PS_CTRL_1_" + current_pipe
    ps_ctrl_2_reg = "PS_CTRL_2_" + current_pipe

    ps_ctrl_1_reg_value = reg_read.read('PS_CTRL_REGISTER', ps_ctrl_1_reg, platform[gfx_index], 0x0)
    ps_ctrl_2_reg_value = reg_read.read('PS_CTRL_REGISTER', ps_ctrl_2_reg, platform[gfx_index], 0x0)

    if (getattr(plane_scaler_ctl, 'enable_scaler_ENABLE') == ps_ctrl_1_reg_value.__getattribute__("enable_scaler")):
        if (plane_id == ps_ctrl_1_reg_value.__getattribute__("scaler_binding")):
            logging.info("Pass: {} Scalar 1 is enabled".format(ps_ctrl_1_reg))
            scalar_id = 1

    if (getattr(plane_scaler_ctl, 'enable_scaler_ENABLE') == ps_ctrl_2_reg_value.__getattribute__("enable_scaler")):
        if (plane_id == ps_ctrl_2_reg_value.__getattribute__("scaler_binding")):
            logging.info("Pass: {} Scalar 2 is enabled".format(ps_ctrl_2_reg))
            scalar_id = 2

    if scalar_id == 1 or scalar_id == 2:
        if not verify_scalar_window_position_size(pipe_id, scalar_id, left, right, top, bottom, gfx_index):
            return False

    if scalar_enable == 0 and scalar_id == 0:
        if not verify_plane_window_position_size(pipe_id, plane_id, left, right, top, bottom, gfx_index):
            return False

    if scalar_enable == 1 and scalar_id == 0:
        logging.error("Scalar is not enabled")
        return False

    return True


##
# @brief            Verification of plane programming with respect to PLANE_CTL register
# @param[in]	    pipe_id; Source id of the plane
# @param[in]	    plane_id; Plane Ctl id of the plane
# @param[in]	    pixel_format; Pixel format of the plane
# @param[in]	    tile_format; Tile format of the plane
# @param[in]        gfx_index; graphic index
# @return		    Return 1(True) for successful verification of plane programming, else 0(False)
def verify_legacy_plane_ctl_programming(pipe_id, plane_id, pixel_format, tile_format, gfx_index):
    ##
    # Import PLANE_CTL_REGISTER module.
    plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % platform[gfx_index])

    current_pipe = chr(int(pipe_id) + 65)
    plane_ctl_reg = 'PLANE_CTL_' + str(plane_id) + '_' + current_pipe

    ##
    # Read PLANE_CTL_REGISTER values.
    plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, platform[gfx_index], 0x0)

    ##
    # Programmed value of plane enable bit.
    plane_enable = plane_ctl_value.__getattribute__("plane_enable")

    ##
    # Check if the Plane is enabled.
    if plane_enable == getattr(plane_ctl, "plane_enable_ENABLE"):
        logging.info("PASS: {} Plane enable status - Expected: ENABLE Actual: ENABLE".format(plane_ctl_reg))

        ##
        # Programmed value of source pixel format.
        programmed_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")

        ##
        # Expected value of pixel format to be programmed.
        expected_pixel_format = getattr(plane_ctl, get_register_string_from_pixel_format(pixel_format))
        if programmed_pixel_format != expected_pixel_format:
            logging.error("Fail: {} Pixel Format - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                   get_pixel_format_string(
                                                                                       expected_pixel_format),
                                                                                   get_pixel_format_string(
                                                                                       programmed_pixel_format)))
            return False
        else:
            logging.info("Pass: {} Pixel Format - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                  get_pixel_format_string(
                                                                                      expected_pixel_format),
                                                                                  get_pixel_format_string(
                                                                                      programmed_pixel_format)))
    else:
        logging.error("FAIL: {} Plane enable status - Expected: ENABLE Actual: DISABLE".format(plane_ctl_reg))
        return False

    return True


##
# @brief            Verification of plane programming
# @param[in]	    pipe_id; Source id of the plane
# @param[in]	    plane_id; Plane Ctl id of the plane
# @param[in]	    pixel_format; Pixel format of the plane
# @param[in]	    tile_format; Tile format of the plane
# @param[in]        width; Width of the plane
# @param[in]        scalar_enable; Expected value for scalar to be enabled or disabled
# @param[in]	    left; Left co-ordinate of the plane
# @param[in]	    right; Right co-ordinate of the plane
# @param[in]	    top; Top co-ordinate of the plane
# @param[in]	    bottom; Bottom co-ordinate of the plane
# @param[in]        enable
# @param[in]        gfx_adapter_index; graphics adapter information
# @return		    Return 1(True) for successful verification of plane programming, else 0(False)
def verify_planes(pipe_id, plane_id, pixel_format, tile_format, width, scalar_enable, left, right, top, bottom, enable,
                  gfx_adapter_index='gfx_0'):
    system_utility = SystemUtility()
    is_ddrw = system_utility.is_ddrw(gfx_adapter_index)

    index = gfx_adapter_index.split('_')
    gfx_index = int(index[1])
    enumerated_displays = display_config.get_enumerated_display_info()

    for display_index in range(enumerated_displays.Count):
        display = cfg_enum.CONNECTOR_PORT_TYPE(
            enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType).name
        port_type = enumerated_displays.ConnectedDisplays[display_index].PortType

    is_pipe_joiner_required, no_of_pipes_required = DisplayClock.is_pipe_joiner_required(gfx_adapter_index, display)

    if is_ddrw:
        if not verify_plane_ctl_programming(pipe_id, plane_id, pixel_format, tile_format, gfx_index, enable):
            logging.error("Plane Ctl verification failed")
            return False
        else:
            logging.debug("Plane Ctl verification passed")

        if pixel_format in [flip.SB_PIXELFORMAT.SB_NV12YUV420, flip.SB_PIXELFORMAT.SB_P010YUV420,
                            flip.SB_PIXELFORMAT.SB_P012YUV420, flip.SB_PIXELFORMAT.SB_P016YUV420]:
            if not verify_planar_programming(pipe_id, plane_id, pixel_format, tile_format, width, gfx_index, enable):
                logging.error("Planar programming verification failed")
                return False
            else:
                logging.debug("Planar programming verification passed")

        if is_pipe_joiner_required is not True:
            if not verify_plane_window_programming(pipe_id, plane_id, scalar_enable, left, right, top, bottom,
                                                   gfx_index):
                logging.error("Plane window verification failed")
                return False
            else:
                logging.info("Plane window verification passed")

        return True
    else:
        if not verify_legacy_plane_ctl_programming(pipe_id, plane_id, pixel_format, tile_format, gfx_index, enable):
            logging.error("Plane Ctl verification failed")
            return False
        else:
            logging.debug("Plane Ctl verification passed")


##
# @brief            Verification of plane programming
# @param[in]	    plane_count; No of planes currently enabled
# @param[in]	    layerindex; layerIndex
# @param[in]	    gfx_index; gfx_index
# @return		    plane_id; plane_id for the corresponding layer index
def get_plane_id_from_layerindex(plane_count, layerindex, gfx_index):
    if not check_layer_reordering(gfx_index):
        plane_id = PLANE_MAX - layerindex
    else:
        plane_id = plane_count - layerindex
    return plane_id


##
##
# @brief            To verify tiled planes
# @param[in]        plane_id; Plane Ctl id of the plane
# @param[in]        pixel_format; expected pixel format
# @param[in]        tile_format; expected tile format
# @param[in]        enable;
# @param[in]        gfx_adapter_index; graphic adapter index
# @return           Return 1(True) for successful verification of plane programming, else 0(False).
def verify_planes_tiled(plane_id, pixel_format, tile_format, enable, gfx_adapter_index='gfx_0'):
    index = gfx_adapter_index.split('_')
    gfx_index = int(index[1])

    reg_read = MMIORegister()

    ##
    # Pipe list
    pipe_list = ['A', 'B', 'C', 'D']

    verify_list = []

    dp_sst = 0b010

    for pipe in pipe_list:

        trans_ddi_reg = 'TRANS_DDI_FUNC_CTL_' + pipe
        trans_ddi2_reg = 'TRANS_DDI_FUNC_CTL2_' + pipe
        ##
        # Read TRANS_DDI_FUNC_CTL_REGISTER values.
        trans_ddi_ctl_value = reg_read.read('TRANS_DDI_FUNC_CTL_REGISTER', trans_ddi_reg, platform[gfx_index], 0x0)

        ##
        # Read TRANS_DDI_FUNC_CTL2_REGISTER values.
        trans_ddi_ctl2_value = reg_read.read('TRANS_DDI_FUNC_CTL2_REGISTER', trans_ddi2_reg, platform[gfx_index], 0x0)

        ##
        # Programmed value of plane enable bit.
        trans_enable = trans_ddi_ctl_value.__getattribute__("trans_ddi_function_enable")

        ##
        # Programmed value of port sync mode.
        port_sync_enable = trans_ddi_ctl2_value.__getattribute__("port_sync_mode_enable")

        ##
        # Port sync master
        master_select = trans_ddi_ctl2_value.__getattribute__("port_sync_mode_master_select")

        if trans_enable and dp_sst == trans_ddi_ctl_value.__getattribute__("trans_ddi_mode_select"):
            if port_sync_enable:
                verify_list.append(pipe)
            if master_select:
                verify_list.append(get_pipe_details(master_select))

    if verify_list:
        ##
        # Import PLANE_CTL_REGISTER module.
        plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % platform[gfx_index])

        for pipe in verify_list:
            ##
            # Plane to be verified
            plane_ctl_reg = 'PLANE_CTL_' + str(plane_id) + '_' + pipe

            ##
            # Read PLANE_CTL_REGISTER values.
            plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, platform[gfx_index], 0x0)

            ##
            # Programmed value of plane enable bit.
            plane_enable = plane_ctl_value.__getattribute__("plane_enable")

            ##
            # Verify if plane is enabled
            if plane_enable:
                logging.info("PASS: {} Plane enable status - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                             get_plane_status_string(
                                                                                                 enable),
                                                                                             get_plane_status_string(
                                                                                                 plane_enable)))

                ##
                # Programmed value of source pixel format.
                programmed_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")

                ##
                # Expected value of pixel format to be programmed.
                expected_pixel_format = getattr(plane_ctl, get_register_string_from_pixel_format(pixel_format))
                if programmed_pixel_format != expected_pixel_format:
                    logging.error("Fail: {} Pixel Format - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                           get_pixel_format_string(
                                                                                               expected_pixel_format),
                                                                                           get_pixel_format_string(
                                                                                               programmed_pixel_format)))
                    return False
                else:
                    logging.info("Pass: {} Pixel Format - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                          get_pixel_format_string(
                                                                                              expected_pixel_format),
                                                                                          get_pixel_format_string(
                                                                                              programmed_pixel_format)))

                    if pixel_format in [flip.SB_PIXELFORMAT.SB_NV12YUV420, flip.SB_PIXELFORMAT.SB_P010YUV420,
                                        flip.SB_PIXELFORMAT.SB_P012YUV420, flip.SB_PIXELFORMAT.SB_P016YUV420]:
                        planar_yuv420_component = plane_ctl_value.__getattribute__("planar_yuv420_component")

                        if planar_yuv420_component:
                            logging.debug("{} Y Plane".format(plane_ctl_reg))
                        else:
                            logging.debug("{} UV Plane".format(plane_ctl_reg))

                programmed_tile_format = plane_ctl_value.__getattribute__("tiled_surface")
                expected_tile_format = getattr(plane_ctl, get_register_string_from_tile_format(tile_format))
                logging.info("{} Tile Format - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                               get_tile_format_string(
                                                                                   expected_tile_format),
                                                                               get_tile_format_string(
                                                                                   programmed_tile_format)))

            else:
                logging.error("FAIL: {} Plane enable status - Expected: {} Actual: {}".format(plane_ctl_reg,
                                                                                              get_plane_status_string(
                                                                                                  enable),
                                                                                              get_plane_status_string(
                                                                                                  plane_enable)))
                return False

        return True
    else:
        logging.error("Pipes are not enabled")
        return False
