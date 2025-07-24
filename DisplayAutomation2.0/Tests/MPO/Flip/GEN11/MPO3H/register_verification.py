########################################################################################################################
# @file         register_verification.py
# @brief        This script contains functions to verify registers
# @author       Shetty, Anjali N
########################################################################################################################
import importlib
import logging

import Tests.MPO.Flip.GEN11.MPO3H.mpo3enums as Enums
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.system_utility import SystemUtility
from registers.mmioregister import MMIORegister

system_utility = SystemUtility()
machine_info = SystemInfo()
platform = None
gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
    break
reg_read = MMIORegister()

##
# @brief    enum for REGISTER_PIXELFORMAT
class REGISTER_PIXELFORMAT(object):
    YUV422_8BPC = 0
    YUV420_8BPC = 2
    RGB2101010 = 4
    YUV420_10BPC = 6
    RGB8888 = 8
    YUV420_12BPC = 10
    RGB16_FLOAT = 12
    YUV420_16BPC = 14
    YUV444_8BPC = 16  #####
    RGB16_UINT = 18  #####
    RGB2101010_XRBIAS = 20
    INDEXED_8BIT = 24
    RGB565 = 28
    YUV422_10BPC = 1
    YUV422_12BPC = 3
    YUV422_16BPC = 5
    YUV444_10BPC = 7
    YUV444_12BPC = 9
    YUV444_16BPC = 11

##
# @brief    enum for REGISTER_TILING
class REGISTER_TILING(object):
    LINEAR = 0
    TILEX = 1
    TILEYL = 4
    TILEYF = 5


##
# @brief            To read a MMIO register
# @param[in]        offset
# @return           reg_val
def regRead(offset):
    reg_val = driver_interface.DriverInterface().mmio_read(int(offset, 16), 'gfx_0')
    print(int(offset, 16), reg_val)
    return reg_val

##
# @brief            To map SBPixelFormat to RegisterFormat
# @param[in]        pixelFormat
# @return           regFormat
def mapSBPixelFormat_RegisterFormat(pixelFormat):
    regFormat = None
    if (pixelFormat is Enums.SB_PIXELFORMAT.SB_P010YUV420):
        regFormat = "source_pixel_format_P010_YUV_420_10_BIT"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_P012YUV420):
        regFormat = "source_pixel_format_P012_YUV_420_12_BIT"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_P016YUV420):
        regFormat = "source_pixel_format_P016_YUV_420_16_BIT"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_NV12YUV420):
        regFormat = "source_pixel_format_NV12_YUV_420"
    elif (pixelFormat in (Enums.SB_PIXELFORMAT.SB_B8G8R8A8, Enums.SB_PIXELFORMAT.SB_B8G8R8X8,
                          Enums.SB_PIXELFORMAT.SB_R8G8B8A8, Enums.SB_PIXELFORMAT.SB_R8G8B8X8)):
        regFormat = "source_pixel_format_RGB_8888"
    elif (pixelFormat in (Enums.SB_PIXELFORMAT.SB_B10G10R10A2, Enums.SB_PIXELFORMAT.SB_B10G10R10X2,
                          Enums.SB_PIXELFORMAT.SB_R10G10B10A2, Enums.SB_PIXELFORMAT.SB_R10G10B10A2)):
        regFormat = "source_pixel_format_RGB_2101010"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_R10G10B10A2_XR_BIAS):
        regFormat = "source_pixel_format_RGB_2101010_XR_BIAS"
    elif (pixelFormat in (Enums.SB_PIXELFORMAT.SB_R16G16B16A16F, Enums.SB_PIXELFORMAT.SB_R16G16B16X16F)):
        regFormat = "source_pixel_format_RGB_16161616_FLOAT"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_YUV422):
        regFormat = "source_pixel_format_YUV_422_PACKED_8_BPC"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_8BPP_INDEXED):
        regFormat = "source_pixel_format_INDEXED_8_BIT"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_B5G6R5X0):
        regFormat = "source_pixel_format_RGB_565"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_YUV422_10):
        regFormat = "source_pixel_format_YUV_422_PACKED_10_BPC"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_YUV422_12):
        regFormat = "source_pixel_format_YUV_422_PACKED_12_BPC"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_YUV422_16):
        regFormat = "source_pixel_format_YUV_422_PACKED_16_BPC"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_YUV444_8):
        regFormat = "source_pixel_format_YUV_444_PACKED_8_BPC"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_YUV444_10):
        regFormat = "source_pixel_format_YUV_444_PACKED_10_BPC"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_YUV444_12):
        regFormat = "source_pixel_format_YUV_444_PACKED_12_BPC"
    elif (pixelFormat is Enums.SB_PIXELFORMAT.SB_YUV444_16):
        regFormat = "source_pixel_format_YUV_444_PACKED_16_BPC"
    return regFormat

##
# @brief            To map SBTiling to RegisterFormat
# @param[in]        tiling
# @return           regTiling
def mapSBTiling_RegisterFormat(tiling):
    regTiling = 0
    if (tiling is Enums.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR):
        regTiling = "tiled_surface_LINEAR_MEMORY"
    elif (tiling in (Enums.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_X_TILED, Enums.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_TILED)):
        regTiling = "tiled_surface_TILE_X_MEMORY"
    elif (tiling is Enums.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED):
        regTiling = "tiled_surface_TILE_Y_LEGACY_MEMORY"
    elif (tiling is Enums.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_F_TILED):
        regTiling = "tiled_surface_TILE_Y_F_MEMORY"
    return regTiling

##
# @brief            To convert tile format to string
# @param[in]        tileformat
# @return           tile_format_map
def getProgrammedTileFormatString(tileformat):
    tile_format_map = {
        0: 'LINEAR',
        1: 'TILEX',
        4: 'TILEYL',
        5: 'TILEYF'
    }
    return tile_format_map.get(tileformat, 'Invalid Tile format')

##
# @brief            To convert integer pixel format value to string
# @param[in]        pixelFormat
# @return           pixel_format in string
def getProgrammedPixelFormatString(pixelFormat):
    pixel_format_map = {
        0: 'YUV422_8BPC',
        2: 'YUV420_8BPC',
        4: 'RGB2101010',
        6: 'YUV420_10BPC',
        8: 'RGB8888',
        10: 'YUV420_12BPC',
        12: 'RGB16_FLOAT',
        14: 'YUV420_16BPC',
        16: 'YUV444_8BPC',
        18: 'RGB16_UINT',
        20: 'RGB2101010_XRBIAS',
        24: 'INDEXED_8BIT',
        28: 'RGB565',
        1: 'YUV422_10BPC',
        3: 'YUV422_12BPC',
        5: 'YUV422_16BPC',
        7: 'YUV444_10BPC',
        9: 'YUV444_12BPC',
        11: 'YUV444_16BPC'
    }
    return pixel_format_map.get(pixelFormat, "Invalid Pixel format")

##
# @brief            To get programmed Planar YUV420 Component String
# @param[in]        YorUVComponent
# @return           planar_yuv420_component
def getProgrammedPlanarYUV420ComponentString(YorUVComponent):
    planar_yuv420_component = {
        0: "Planar_YUV420UV",
        1: "Planar_YUV420_Y"
    }
    return planar_yuv420_component.get(YorUVComponent, "Invalid Planar YUV Component")

##
# @brief            To get programmed scalar mode string
# @param[in]        scalar_mode
# @return           scalar_mode
def getProgrammedScalarModeString(scalar_mode):
    scalar_mode_map = {
        0: "Scalar Mode Normal",
        1: "Scalar Mode Planar"
    }
    return scalar_mode_map.get(scalar_mode, "Invalid Scalar Mode")

##
# @brief            To verify the PlaneCtrl register programming
# @param[in]        pipeID
# @param[in]        planeID
# @param[in]        pixelFormat
# @param[in]        tiling
# @param[in]        YorUVPlane
# @return           True if pixel format matches else False
def verifyPlaneCtlProgramming(pipeID, planeID, pixelFormat, tiling, YorUVPlane=0):
    # RGBOrder,YUV422ByteOrder,HW rotation - can be added
    plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % platform)

    current_pipe = chr(int(pipeID) + 65)

    plane_ctl_reg = 'PLANE_CTL_' + str(planeID) + '_' + current_pipe
    plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, platform, 0x0)

    plane_enable = plane_ctl_value.__getattribute__("plane_enable")

    if plane_enable == getattr(plane_ctl, "plane_enable_ENABLE"):
        logging.info("PASS: %s - Plane enable status Expected = ENABLE Actual = ENABLE" % plane_ctl_reg)
        # Pixel format
        source_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")
        expected_pixel_format = getattr(plane_ctl, mapSBPixelFormat_RegisterFormat(pixelFormat))
        if source_pixel_format != expected_pixel_format:
            logging.error('FAIL: %s - Pixel format not matching: Expected = %s, Actual = %s' % (
                plane_ctl_reg, getProgrammedPixelFormatString(expected_pixel_format),
                getProgrammedPixelFormatString(source_pixel_format)))
            return False
        else:
            logging.info('PASS: %s - Pixel format matching: Expected = %s, Actual = %s' % (
                plane_ctl_reg, getProgrammedPixelFormatString(expected_pixel_format),
                getProgrammedPixelFormatString(source_pixel_format)))

        # Tiling
        source_tile_format = plane_ctl_value.__getattribute__("tiled_surface")
        logging.info("%s - Tiling format: Expected = %s Programmed = %s" % (
            plane_ctl_reg, getProgrammedTileFormatString(tiling), getProgrammedTileFormatString(source_tile_format)))

        # RC
        # if(mapSBPixelFormat_RegisterFormat(pixelFormat) in (REGISTER_PIXELFORMAT.RGB2101010,REGISTER_PIXELFORMAT.RGB8888)):
        # RC = 1
        # else:
        # RC = 0
        # result , programmedValue = compareRegisterValue(regValue,RC,bitMaps['RC'])
        # if(result is False):
        # logging.error("Render Decompression not matching : Expected - %d Programmed - %d",RC,programmedValue)
        # Y or UV
        planar_yuv420_component = plane_ctl_value.__getattribute__("planar_yuv420_component")
        if planar_yuv420_component != YorUVPlane:
            logging.error("FAIL: %s - Planar YUV420 Component: Expected = %s Actual = %s", plane_ctl_reg,
                          getProgrammedPlanarYUV420ComponentString(YorUVPlane),
                          getProgrammedPlanarYUV420ComponentString(planar_yuv420_component))
            return False
        else:
            logging.info("PASS: %s - Planar YUV420 Component: Expected = %s Actual = %s", plane_ctl_reg,
                         getProgrammedPlanarYUV420ComponentString(YorUVPlane),
                         getProgrammedPlanarYUV420ComponentString(planar_yuv420_component))

    else:
        logging.error("FAIL: %s - Plane enable status Expected = ENABLE Actual = DISABLE" % plane_ctl_reg)
        return False

    return True

##
# @brief            To verify plane window programming
# @param[in]        pipeID
# @param[in]        planeID
# @param[in]        leftCoordinate
# @param[in]        topCoordinate
# @param[in]        rightCoordinate
# @param[in]        bottomCoordinate
# @param[in]        scalarEnable
# @return           True or False
def verifyPlaneWindowProgramming(pipeID, planeID, leftCoordinate, topCoordinate, rightCoordinate, bottomCoordinate,
                                 scalarEnable):
    plane_scaler_ctl = importlib.import_module("registers.%s.PS_CTRL_REGISTER" % platform)
    current_pipe = chr(int(pipeID) + 65)

    ps_ctrl_1_reg = "PS_CTRL_1_" + current_pipe
    ps_ctrl_2_reg = "PS_CTRL_2_" + current_pipe

    ps_ctrl_1_reg_value = reg_read.read('PS_CTRL_REGISTER', ps_ctrl_1_reg, platform, 0x0)
    ps_ctrl_2_reg_value = reg_read.read('PS_CTRL_REGISTER', ps_ctrl_2_reg, platform, 0x0)

    scalarID = 0

    if (getattr(plane_scaler_ctl, 'enable_scaler_ENABLE') == ps_ctrl_1_reg_value.__getattribute__(
            "enable_scaler")):  # Scalar1 enabled
        if ((planeID) == ps_ctrl_1_reg_value.__getattribute__("scaler_binding")):  # Scalar1 tied to planeID
            logging.debug("Scalar 1 Enabled")
            scalarID = 1
            # Scalar Type
            # result , programmedValue = compareRegisterValue(regValue1,scalarType,bitMaps['PS_TYPE'])
            # if(result is False) :
            # logging.error("ScalarType not matching Expected - %d Programmed - %d ", scalarType,programmedValue)
            # Scalar Mode
            # result , programmedValue = compareRegisterValue(regValue1,scalarMode,bitMaps['PS_MODE'])
            # if(result is False) :
            # logging.error("ScalarMode not matching Expected - %d Programmed - %d ", scalarType,programmedValue)
            # Scalar Window pos/size verification
            if not verifyScalarWindowPosition_Size(pipeID, planeID, scalarID, leftCoordinate, rightCoordinate,
                                                   topCoordinate, bottomCoordinate):
                return False

    elif (getattr(plane_scaler_ctl, 'enable_scaler_ENABLE') == ps_ctrl_2_reg_value.__getattribute__(
            "enable_scaler")):  # Scalar2 enabled
        if ((planeID) == ps_ctrl_2_reg_value.__getattribute__("scaler_binding")):  # Scalar2 tied to planeID
            logging.debug("Scalar 2 Enabled")
            scalarID = 2
            # result , programmedValue = compareRegisterValue(regValue2,scalarType,bitMaps['PS_TYPE'])
            # Scalar Type
            # if(result is False) :
            # logging.error("ScalarType not matching Expected - %d Programmed - %d ", scalarType,programmedValue)
            # Scalar Mode
            # result , programmedValue = compareRegisterValue(regValue2,scalarMode,bitMaps['PS_MODE'])
            # if(result is False) :
            # logging.error("ScalarMode not matching Expected - %d Programmed - %d ", scalarType,programmedValue)
            # Scalar Window pos/size verification
            if not verifyScalarWindowPosition_Size(pipeID, planeID, scalarID, leftCoordinate, rightCoordinate,
                                                   topCoordinate, bottomCoordinate):
                return False

    if scalarEnable == 1 and scalarID == -1:
        logging.debug("No Scalars enabled!!!")

        # Window pos/size verification
        if not verifyPlaneWindowPosition_Size(pipeID, planeID, leftCoordinate, rightCoordinate, topCoordinate,
                                              bottomCoordinate):
            return False

    return True

##
# @brief            To verify scalar window position size
# @param[in]        pipeID
# @param[in]        planeID
# @param[in]        scalarID
# @param[in]        leftCoordinate
# @param[in]        rightCoordinate
# @param[in]        topCoordinate
# @param[in]        bottomCoordinate
# @return           ret_value
def verifyScalarWindowPosition_Size(pipeID, planeID, scalarID, leftCoordinate, rightCoordinate, topCoordinate,
                                    bottomCoordinate):
    ps_win_position = importlib.import_module("registers.%s.PS_WIN_POS_REGISTER" % platform)
    ps_win_size = importlib.import_module("registers.%s.PS_WIN_SZ_REGISTER" % platform)
    current_pipe = chr(int(pipeID) + 65)
    ret_value = True

    ps_win_pos_reg = "PS_WIN_POS_" + str(scalarID) + '_' + current_pipe
    ps_win_position_value = reg_read.read('PS_WIN_POS_REGISTER', ps_win_pos_reg, platform, 0x0)

    # Window position
    if (leftCoordinate != ps_win_position_value.__getattribute__('xpos')):
        logging.error(
            'FAIL: %s - Scalar WindowXPos not matching: Expected = %d Actual = %d' % (ps_win_pos_reg, leftCoordinate,
                                                                                      ps_win_position_value.__getattribute__(
                                                                                          'xpos')))
        ret_value = False

    else:
        logging.info(
            'PASS: %s - Scalar WindowXPos matching: Expected = %d Actual = %d' % (ps_win_pos_reg, leftCoordinate,
                                                                                  ps_win_position_value.__getattribute__(
                                                                                      'xpos')))

    if (topCoordinate != ps_win_position_value.__getattribute__('ypos')):
        logging.error(
            'FAIL: %s - Scalar WindowYPos not matching: Expected = %d Actual = %d' % (ps_win_pos_reg, topCoordinate,
                                                                                      ps_win_position_value.__getattribute__(
                                                                                          'ypos')))
        ret_value = False

    else:
        logging.info(
            'PASS: %s - Scalar WindowYPos matching: Expected = %d Actual = %d' % (ps_win_pos_reg, topCoordinate,
                                                                                  ps_win_position_value.__getattribute__(
                                                                                      'ypos')))

    ps_win_sz_reg = "PS_WIN_SZ_" + str(scalarID) + '_' + current_pipe
    ps_win_size_value = reg_read.read('PS_WIN_SZ_REGISTER', ps_win_sz_reg, platform, 0x0)

    # Window Size
    if ((rightCoordinate - leftCoordinate) != ps_win_size_value.__getattribute__('xsize')):
        logging.error("FAIL: %s - Scalar WindowXSize not matching : Expected = %d Actual = %d", ps_win_sz_reg,
                      (rightCoordinate - leftCoordinate), ps_win_size_value.__getattribute__('xsize'))
        ret_value = False
    else:
        logging.info("PASS: %s - Scalar WindowXSize matching : Expected = %d Actual = %d", ps_win_sz_reg,
                     (rightCoordinate - leftCoordinate), ps_win_size_value.__getattribute__('xsize'))

    if (bottomCoordinate - topCoordinate) != ps_win_size_value.__getattribute__('ysize'):
        logging.error("FAIL: %s - Scalar WindowYSize not matching : Expected = %d Actual = %d", ps_win_sz_reg,
                      bottomCoordinate - topCoordinate, ps_win_size_value.__getattribute__('ysize'))
        ret_value = False
    else:
        logging.info("PASS: %s - Scalar WindowYSize matching : Expected = %d Actual = %d",
                     ps_win_sz_reg, bottomCoordinate - topCoordinate, ps_win_size_value.__getattribute__('ysize'))
    return ret_value

##
# @brief            To verify plane window position size
# @param[in]        pipeID
# @param[in]        planeID
# @param[in]        leftCoordinate
# @param[in]        rightCoordinate
# @param[in]        topCoordinate
# @param[in]        bottomCoordinate
# @return           ret_value
def verifyPlaneWindowPosition_Size(pipeID, planeID, leftCoordinate, rightCoordinate, topCoordinate, bottomCoordinate):
    plane_position = importlib.import_module("registers.%s.PLANE_POS_REGISTER" % platform)
    plane_size = importlib.import_module("registers.%s.PLANE_SIZE_REGISTER" % platform)
    current_pipe = chr(int(pipeID) + 65)
    ret_value = True

    plane_pos_reg = "PLANE_POS_" + str(planeID) + '_' + current_pipe
    plane_position_value = reg_read.read('PLANE_POS_REGISTER', plane_pos_reg, platform, 0x0)

    # Window position
    if (leftCoordinate != plane_position_value.__getattribute__('x_position')):
        logging.error("FAIL: %s - Plane WindowXPos not matching : Expected = %d Actual = %d", plane_pos_reg,
                      leftCoordinate, plane_position_value.__getattribute__('x_position'))
        ret_value = False
    else:
        logging.info("PASS: %s - Plane WindowXPos matching : Expected = %d Actual = %d", plane_pos_reg,
                     leftCoordinate, plane_position_value.__getattribute__('x_position'))

    if (topCoordinate != plane_position_value.__getattribute__('y_position')):
        logging.error("FAIL: %s - Plane WindowYPos not matching : Expected = %d Actual = %d", plane_pos_reg,
                      topCoordinate, plane_position_value.__getattribute__('y_position'))
        ret_value = False
    else:
        logging.info("PASS: %s - Plane WindowYPos matching : Expected = %d Actual = %d", plane_pos_reg,
                     topCoordinate, plane_position_value.__getattribute__('y_position'))

    plane_size_reg = "PLANE_SIZE_" + str(planeID) + '_' + current_pipe
    plane_size_value = reg_read.read('PLANE_SIZE_REGISTER', plane_size_reg, platform, 0x0)

    # Window Size
    if ((rightCoordinate - leftCoordinate) != plane_size_value.__getattribute__('width')):
        logging.error("FAIL: %s - Plane WindowXSize not matching : Expected = %d Actual = %d", plane_size_reg,
                      (rightCoordinate - leftCoordinate), plane_size_value.__getattribute__('width'))
        ret_value = False
    else:
        logging.error("PASS: %s - Plane WindowXSize matching : Expected = %d Actual = %d", plane_size_reg,
                      (rightCoordinate - leftCoordinate), plane_size_value.__getattribute__('width'))

    if ((bottomCoordinate - topCoordinate) != plane_size_value.__getattribute__('height')):
        logging.error("FAIL: %s - Plane WindowYSize not matching : Expected = %d Actual = %d", plane_size_reg,
                      (bottomCoordinate - topCoordinate), plane_size_value.__getattribute__('height'))
        ret_value = False
    else:
        logging.info("PASS: %s - Plane WindowYSize  matching : Expected = %d Actual = %d", plane_size_reg,
                     (bottomCoordinate - topCoordinate), plane_size_value.__getattribute__('height'))

    return ret_value

##
# @brief            To verify planar programming
# @param[in]        pipeID
# @param[in]        planeID
# @param[in]        pixelFormat
# @param[in]        tiling
# @param[in]        width
# @return           ret_value
def verifyPlanarProgramming(pipeID, planeID, pixelFormat, tiling, width):
    ret_value = True

    if platform in ["icllp", "lkf1", "jsl", "tgl", "dg1"]:
        y1, y2 = 6, 7
    else:
        y1, y2 = 4, 5

    if (planeID <= 3 and width <= 4096):
        plane_cus_ctl = importlib.import_module("registers.%s.PLANE_CUS_CTL_REGISTER" % platform)
        current_pipe = chr(int(pipeID) + 65)

        plane_cus_ctl_reg = "PLANE_CUS_CTL_" + str(planeID) + '_' + current_pipe
        plane_cus_ctl_value = reg_read.read('PLANE_CUS_CTL_REGISTER', plane_cus_ctl_reg, platform, 0x0)

        if (getattr(plane_cus_ctl, 'chroma_upsampler_enable_ENABLE') == plane_cus_ctl_value.__getattribute__(
                'chroma_upsampler_enable')):
            if (getattr(plane_cus_ctl, 'y_binding_PLANE_' + str(y1)) == plane_cus_ctl_value.__getattribute__(
                    'y_binding')):
                if not verifyPlaneCtlProgramming(pipeID, y1, pixelFormat, tiling, 1):
                    ret_value = False
            elif (getattr(plane_cus_ctl, 'y_binding_PLANE_' + str(y2)) == plane_cus_ctl_value.__getattribute__(
                    'y_binding')):
                if not verifyPlaneCtlProgramming(pipeID, y2, pixelFormat, tiling, 1):
                    ret_value = False
        else:
            logging.error("FAIL: %s - CUS not enabled for pixel format: %s : Expected = ENABLE Actual = DISABLE",
                          plane_cus_ctl_reg, mapSBPixelFormat_RegisterFormat(pixelFormat))
            ret_value = False
    else:
        plane_scaler_ctl = importlib.import_module("registers.%s.PS_CTRL_REGISTER" % platform)
        current_pipe = chr(int(pipeID) + 65)

        ps_ctrl_1_reg = "PS_CTRL_1_" + current_pipe
        ps_ctrl_2_reg = "PS_CTRL_2_" + current_pipe

        ps_ctrl_1_reg_value = reg_read.read('PS_CTRL_REGISTER', ps_ctrl_1_reg, platform, 0x0)
        ps_ctrl_2_reg_value = reg_read.read('PS_CTRL_REGISTER', ps_ctrl_2_reg, platform, 0x0)

        if (getattr(plane_scaler_ctl, 'enable_scaler_ENABLE') == ps_ctrl_1_reg_value.__getattribute__(
                "enable_scaler")):  # Scalar1 enabled
            if ((planeID) == ps_ctrl_1_reg_value.__getattribute__("scaler_binding")):  # Scalar1 tied to planeID
                # Scalar Mode
                if (getattr(plane_scaler_ctl, 'scaler_mode_PLANAR') != ps_ctrl_1_reg_value.__getattribute__(
                        'scaler_mode')):
                    logging.error("FAIL: %s - ScalarMode not matching Expected = %s Actual = %s ", ps_ctrl_1_reg,
                                  getProgrammedScalarModeString(getattr(plane_scaler_ctl, 'scaler_mode_PLANAR')),
                                  getProgrammedScalarModeString(ps_ctrl_1_reg_value.__getattribute__('scaler_mode')))
                    ret_value = False
                else:
                    if (getattr(plane_scaler_ctl, 'scaler_binding_y_PLANE_' + str(
                            y1) + '_SCALER') == ps_ctrl_1_reg_value.__getattribute__('scaler_binding_y')):
                        if not verifyPlaneCtlProgramming(pipeID, y1, pixelFormat, tiling, 1):
                            ret_value = False
                    elif (getattr(plane_scaler_ctl, 'scaler_binding_y_PLANE_' + str(
                            y2) + '_SCALER') == ps_ctrl_1_reg_value.__getattribute__('scaler_binding_y')):
                        if not verifyPlaneCtlProgramming(pipeID, y1, pixelFormat, tiling, 1):
                            ret_value = False

        elif (getattr(plane_scaler_ctl, 'enable_scaler_ENABLE') == ps_ctrl_2_reg_value.__getattribute__(
                "enable_scaler")):  # Scalar2 enabled
            if ((planeID) == ps_ctrl_2_reg_value.__getattribute__("scaler_binding")):  # Scalar2 tied to planeID
                # Scalar Mode
                if (getattr(plane_scaler_ctl, 'scaler_mode_PLANAR') != ps_ctrl_2_reg_value.__getattribute__(
                        'scaler_mode')):
                    logging.error("FAIL: %s - ScalarMode not matching Expected = %s Actual = %s ", ps_ctrl_2_reg,
                                  getProgrammedScalarModeString(getattr(plane_scaler_ctl, 'scaler_mode_PLANAR')),
                                  getProgrammedScalarModeString(ps_ctrl_2_reg_value.__getattribute__('scaler_mode')))
                    ret_value = False
                else:
                    if (getattr(plane_scaler_ctl, 'scaler_binding_y_PLANE_' + str(
                            y1) + '_SCALER') == ps_ctrl_2_reg_value.__getattribute__('scaler_binding_y')):
                        if not verifyPlaneCtlProgramming(pipeID, y1, pixelFormat, tiling, 1):
                            ret_value = False
                    elif (getattr(plane_scaler_ctl, 'scaler_binding_y_PLANE_' + str(
                            y2) + '_SCALER') == ps_ctrl_2_reg_value.__getattribute__('scaler_binding_y')):
                        if not verifyPlaneCtlProgramming(pipeID, y2, pixelFormat, tiling, 1):
                            ret_value = False
        else:
            logging.error("No Scalars enabled - CUS also not enabled!!!")
            ret_value = False

    return ret_value

##
# @brief            To verify plane programming
# @param[in]        pipeID
# @param[in]        planeID
# @param[in]        pixelFormat
# @param[in]        tiling
# @param[in]        leftCoordinate
# @param[in]        topCoordinate
# @param[in]        rightCoordinate
# @param[in]        bottomCoordinate
# @param[in]        srcWidth
# @param[in]        scalarEnable
# @return           ret_value
def verifyPlaneProgramming(pipeID, planeID, pixelFormat, tiling, leftCoordinate, topCoordinate, rightCoordinate,
                           bottomCoordinate, srcWidth, scalarEnable):
    ret_value = True

    if not verifyPlaneCtlProgramming(pipeID, planeID, pixelFormat, tiling):
        logging.debug("Verification of plane programming failed")
        ret_value = False

    if not verifyPlaneWindowProgramming(pipeID, planeID, leftCoordinate, topCoordinate, rightCoordinate,
                                        bottomCoordinate, scalarEnable):
        logging.debug("Verification of plane window programming failed")
        ret_value = False

    if (mapSBPixelFormat_RegisterFormat(pixelFormat) in ("source_pixel_format_NV12_YUV_420",
                                                         "source_pixel_format_P010_YUV_420_10_BIT"
                                                         "source_pixel_format_P010_YUV_420_12_BIT"
                                                         "source_pixel_format_P010_YUV_420_16_BIT")):
        if not verifyPlanarProgramming(pipeID, planeID, pixelFormat, tiling, srcWidth):
            logging.debug("Verification of planar programming failed")
            ret_value = False

    return ret_value
