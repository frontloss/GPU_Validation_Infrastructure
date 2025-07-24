#####################################################################################################################################
# @file     display_plane.py
# @brief    Python wrapper exposes interfaces for Display Plane
# @details  display_plane.py provides interface's to Verify Display Plane Configuration
#           for all connected displays.
#           Input:  For each plane to be verifed, pass targetID, planeID, TilingFormat,
#                  pixelFormat, HFLIP enable/disable, Rotation
#           Verified: plane enable/disable, pixel format, tiling, hflip, rotaion,
#                   plane gamma, plane size and position
# @note     Supported display interfaces are MIPI, EDP, DP, HDMI\n
#           Verfied on EDP, HDMI
# @todo     Mapping HSCALE,VSCALE scaling ratio to scaled size
# @author   Aafiya Kakeem
####################################################################################################################################

import logging
import math
import os
import time

from Libs import env_settings
from Libs.Core import enum
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core.system_utility import SystemUtility
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.vdsc.dsc_enum_constants import DSCEngine
from Libs.Core.machine_info import machine_info
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Planes.Common.planes_verification import check_layer_reordering
from registers.mmioregister import MMIORegister

# Pipe Ganged and Tiled modes have PIPEEXCESS added in Plane Source Size
PIPEEXCESS = 4

##
# @brief ICLLP PLANE PIXEL FORMAT
class ICLLP_PIXELFORMAT(object):
    YUV422_8BPC = 0
    YUV420_8BPC = 2
    RGB2101010 = 4
    YUV420_10BPC = 6
    RGB8888 = 8
    YUV420_12BPC = 10
    RGB16_FLOAT = 12
    YUV420_16BPC = 14
    YUV444_8BPC = 16
    RGB16_UINT = 18
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
# @brief GLK PLANE PIXEL FORMAT
class GLK_PIXELFORMAT(object):
    YUV422_8BPC = 0
    YUV420_8BPC = 1
    RGB2101010 = 2
    YUV420_10BPC = 3
    RGB8888 = 4
    YUV420_12BPC = 5
    RGB16_FLOAT = 6
    YUV420_16BPC = 7
    YUV444_8BPC = 8
    RGB16_UINT = 9
    RGB2101010_XRBIAS = 10
    INDEXED_8BIT = 12
    RGB565 = 13


##
# @brief PLANE TILING FORMAT
class TILING_FORMAT(object):
    LINEAR = 0
    TILE_X = 1
    TILE_Y = 4
    TILE_YF = 5
    TILE_4 = 5


##
# @brief PLANE ROTATION
class ROTATION(object):
    DEG_0 = 0
    DEG_90 = 1
    DEG_180 = 2
    DEG_270 = 3


##
# @brief DisplayPlane base class Has functions to verify Display Plane verification
class DisplayPlane(display_base.DisplayBase):

    ##
    # @brief Initializes Display Plane Object
    # @param[in] display_port display to create the object for
    # @param[in] planeID Plane ID of that plane
    # @param[in] planeheight height of the plane in pixels
    # @param[in] planewidth width of the plane in pixels
    # @param[in] planeposx horizontal position of the plane on the screen
    # @param[in] planeposy vertical position of the plane on the screen
    # @param[in] tiling tiling format
    # @param[in] pixelFormat RGB or YUV formats
    # @param[in] scalar scaling option
    # @param[in] rotation degree of rotation
    # @param[in] hflip 
    # @param[in] gfx_index
    def __init__(self, display_port=None, planeID=None, planeheight=None,
                 planewidth=None, planeposx=None, planeposy=None,
                 tiling=None, pixelFormat=None, scalar=None, rotation=None, hflip=None, gfx_index='gfx_0'):
        self.display_port = display_port
        self.planeID = planeID  # pass 1 for PLANE_1_X
        self.planeheight = planeheight
        self.planewidth = planewidth
        self.planeposx = planeposx
        self.planeposy = planeposy

        self.tiling = tiling  # class TILING_FORMAT
        self.pixelFormat = pixelFormat  # MapPixelFormat
        self.scalar = scalar  # 0/1
        self.rotation = rotation  # class ROTATION
        self.hflip = hflip  # 0/1
        display_base.DisplayBase.__init__(self, display_port, gfx_index=gfx_index)


logger_template = "{res:^5}: {feature:<60}: Expected: {exp:<20}  Actual: {act}"


##
# @brief Check the register mapping using values in ROTATION class.
# @param[in] rotation value as passed by user
# @return register bit value for passed rotation parameter
def MapRotation(rotation):
    if (rotation == 'DEG_0'):
        return ROTATION.DEG_0
    elif (rotation == 'DEG_90'):
        return ROTATION.DEG_90
    elif (rotation == 'DEG_180'):
        return ROTATION.DEG_180
    elif (rotation == 'DEG_270'):
        return ROTATION.DEG_270
    else:
        return -1


##
# @brief Check the register mapping using values in TILING_FORMAT class.
# @param[in] tiling value as passed by user
# @return register bit value for passed tiling parameter
def MapTiling(tiling):
    if (tiling == 'LINEAR'):
        return TILING_FORMAT.LINEAR
    elif (tiling == 'TILE_X'):
        return TILING_FORMAT.TILE_X
    elif (tiling == 'TILE_Y'):
        return TILING_FORMAT.TILE_Y
    elif (tiling == 'TILE_YF'):
        return TILING_FORMAT.TILE_YF
    elif (tiling == 'TILE_4'):
        return TILING_FORMAT.TILE_4
    else:
        return -1


##
# @brief Check the register mapping using values in PIXELFORMAT class.
# @param[in] planeObj plane object to verify
# @return register bit value for passed pixelFormat parameter
def MapPixelFormat(planeObj):
    pixelFormat = planeObj.pixelFormat
    if (planeObj.platform in ['GLK', 'SKL', 'KBL', 'CFL', 'CNL']):
        enum_value = GLK_PIXELFORMAT
    else:
        enum_value = ICLLP_PIXELFORMAT
    regFormat = 0
    if (pixelFormat == 'P010YUV420'):
        regFormat = enum_value.YUV420_10BPC
    elif (pixelFormat == 'P012YUV420'):
        regFormat = enum_value.YUV420_12BPC
    elif (pixelFormat == 'P016YUV420'):
        regFormat = enum_value.YUV420_16BPC
    elif (pixelFormat == 'NV12YUV420'):
        regFormat = enum_value.YUV420_8BPC
    elif (pixelFormat in ('B8G8R8A8', 'B8G8R8X8', 'R8G8B8A8', 'R8G8B8X8')):
        regFormat = enum_value.RGB8888
    elif (pixelFormat in ('B10G10R10A2', 'B10G10R10X2', 'R10G10B10A2', 'R10G10B10A2')):
        regFormat = enum_value.RGB2101010
    elif (pixelFormat == 'R10G10B10A2_XR_BIAS'):
        regFormat = enum_value.RGB2101010_XRBIAS
    elif (pixelFormat in ('R16G16B16A16F', 'R16G16B16X16F')):
        regFormat = enum_value.RGB16_FLOAT
    elif (pixelFormat == 'YUV422_8'):
        regFormat = enum_value.YUV422_8BPC
    elif (pixelFormat == '8BPP_INDEXED'):
        regFormat = enum_value.INDEXED_8BIT
    elif (pixelFormat == 'B5G6R5X0'):
        regFormat = enum_value.RGB565
    elif (pixelFormat == 'YUV422_10'):
        regFormat = enum_value.YUV422_10BPC
    elif (pixelFormat == 'YUV422_12'):
        regFormat = enum_value.YUV422_12BPC
    elif (pixelFormat == 'YUV422_16'):
        regFormat = enum_value.YUV422_16BPC
    elif (pixelFormat == 'YUV444_8'):
        regFormat = enum_value.YUV444_8BPC
    elif (pixelFormat == 'YUV444_10'):
        regFormat = enum_value.YUV444_10BPC
    elif (pixelFormat == 'YUV444_12'):
        regFormat = enum_value.YUV444_12BPC
    elif (pixelFormat == 'YUV444_16'):
        regFormat = enum_value.YUV444_16BPC
    return regFormat


##
# @brief PLANE_COLOR_CTL_REGISTER bit verification(plane_gamma)
# @param[in] planeObj PlaneStruct() object
# @param[in] plane_pipe plane and pipe suffix for register read
# @param[in] gfx_index graphics adapter
# @return return true if VerifyColorCtrl() is success, else false
def VerifyColorCtrl(planeObj, plane_pipe, gfx_index='gfx_0'):
    # TODO : Plane_gamma_disable check when CSC is enabled
    plane_color_ctl = MMIORegister.read("PLANE_COLOR_CTL_REGISTER",
                                        "PLANE_COLOR_CTL_%s" % (plane_pipe), planeObj.platform, gfx_index=gfx_index)
    logging.debug("PLANE_COLOR_CTL_%s" % (plane_pipe) + "--> Offset : "
                  + format(plane_color_ctl.offset, '08X') + " Value :" + format(plane_color_ctl.asUint, '08X'))
    if plane_color_ctl.plane_csc_enable:
        if not plane_color_ctl.plane_gamma_disable:
            logging.info(
                logger_template.format(res="PASS", feature="PLANE_COLOR_CLT_{} - Plane Gamma".format(plane_pipe),
                                       exp="0(ENABLED)", act=plane_color_ctl.plane_gamma_disable))
            return True
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][PLANE]: PLANE_COLOR_CLT_{0} - Plane Gamma check failed! Expected: "
                      "0(ENABLED) Actual: 1".format(plane_pipe),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                logger_template.format(res="FAIL", feature="PLANE_COLOR_CLT_{} - Plane Gamma".format(plane_pipe),
                                       exp="0(ENABLED)", act=plane_color_ctl.plane_gamma_disable))
            return False
    else:
        if plane_color_ctl.plane_gamma_disable:
            logging.info(
                logger_template.format(res="PASS", feature="PLANE_COLOR_CLT_{} - Plane Gamma".format(plane_pipe),
                                       exp="1(DISABLE)", act=plane_color_ctl.plane_gamma_disable))
            return True
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][PLANE]: PLANE_COLOR_CLT_{0} - Plane Gamma check failed! Expected: "
                      "1(DISABLED) Actual: 0".format(plane_pipe),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                logger_template.format(res="FAIL", feature="PLANE_COLOR_CLT_{} - Plane Gamma".format(plane_pipe),
                                       exp="1(DISABLE)", act=plane_color_ctl.plane_gamma_disable))
            return False


##
# @brief PLANE_CTL_REGISTER bit verification(plane_enable,pixel,tiling,hflip,rotation)
# @param[in] planeObj PlaneStruct() object
# @param[in] plane_pipe plane and pipe suffix for register read
# @param[in] gfx_index graphics adapter
# @return bool return true if VerifyPlaneCtrl() is success, else false
def VerifyPlaneCtrl(planeObj, plane_pipe, gfx_index='gfx_0'):
    tiling = hflip = rotation = pixelFormat = False

    plane_ctl_reg = MMIORegister.read("PLANE_CTL_REGISTER", "PLANE_CTL_%s" % (plane_pipe), planeObj.platform,
                                      gfx_index=gfx_index)
    logging.debug("PLANE_CTL_%s" % (plane_pipe) + "--> Offset : "
                  + format(plane_ctl_reg.offset, '08X') + " Value :" + format(plane_ctl_reg.asUint, '08X'))

    if not plane_ctl_reg.plane_enable:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PLANE]: PLANE_CTL_{0} - Plane NOT Enabled! Expected: "
                  "1(DISABLED) Actual: 0".format(plane_pipe),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(
            logger_template.format(res="FAIL", feature="PLANE_CTL_{} - Plane NOT Enabled".format(plane_pipe),
                                   exp="1(ENABLED)", act="0"))
        return False

    logging.info(logger_template.format(res="INFO", feature="PLANE_CTL_{} - Plane Enable".format(plane_pipe),
                                        exp="1(ENABLED)", act="1"))
    logging_flag = False

    if plane_ctl_reg.tiled_surface == MapTiling(planeObj.tiling):
        tiling = True
        logging_flag = True
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PLANE]: PLANE_CTL_{0} - Tiling values mis-matched! Expected: {1}({2}) "
                  "Actual: {3}".format(plane_pipe, MapTiling(planeObj.tiling), planeObj.tiling,
                                       plane_ctl_reg.tiled_surface),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(logger_template.format(res="FAIL", feature="PLANE_CTL_{} - Tiling".format(plane_pipe),
                                             exp="{}({})".format(MapTiling(planeObj.tiling), planeObj.tiling),
                                             act=plane_ctl_reg.tiled_surface))
    if (planeObj.platform != 'KBL') and (planeObj.platform != 'SKL') and (planeObj.platform != 'CFL'):
        hflip_val = "Enable" if planeObj.hflip == 1 else "Disable"
        if plane_ctl_reg.horizontal_flip == planeObj.hflip:
            hflip = True
            logging_flag = logging_flag and True
            logging.info(logger_template.format(res="PASS", feature="PLANE_CTL_{} - HFlip".format(plane_pipe),
                                                exp="{}({})".format(planeObj.hflip, hflip_val),
                                                act=plane_ctl_reg.horizontal_flip))
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][PLANE]:PLANE_CTL_{0} - HFlip values mis-matched! Expected: {1}({2})"
                      " Actual: {3}".format(plane_pipe, planeObj.hflip, hflip_val, plane_ctl_reg.horizontal_flip),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(logger_template.format(res="FAIL", feature="PLANE_CTL_{} - HFlip".format(plane_pipe),
                                                 exp="{}({})".format(planeObj.hflip, hflip_val),
                                                 act=plane_ctl_reg.horizontal_flip))
    else:
        hflip = True

    if plane_ctl_reg.plane_rotation == MapRotation(planeObj.rotation):
        rotation = True
        logging_flag = logging_flag and True
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PLANE]:PLANE_CTL_{0} - Rotation values mis-matched! Expected: {1}({2})"
                  " Actual: {3}".format(plane_pipe, MapRotation(planeObj.rotation), planeObj.rotation,
                                        plane_ctl_reg.plane_rotation),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(logger_template.format(res="FAIL", feature="PLANE_CTL_{} - Rotation".format(plane_pipe),
                                             exp="{}({})".format(MapRotation(planeObj.rotation), planeObj.rotation),
                                             act=plane_ctl_reg.plane_rotation))
    if logging_flag:
        logging.info(logger_template.format(res="PASS", feature="PLANE_CTL_{} - [Tiling,Rotation]".format(plane_pipe),
                                            exp="[{0}({1}),{2}({3})]".format(MapTiling(planeObj.tiling),
                                                                             planeObj.tiling,
                                                                             MapRotation(planeObj.rotation),
                                                                             planeObj.rotation),
                                            act=[int(plane_ctl_reg.tiled_surface), int(plane_ctl_reg.plane_rotation)]))
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PLANE]:PLANE_CTL_{0} - [Tiling,Rotation] values mis-matched! Expected: "
                  "[{1}({2}), {3}({4})] Actual: [{5},{6}]".format(plane_pipe, MapTiling(planeObj.tiling),
                                                                  planeObj.tiling, MapRotation(planeObj.rotation),
                                                                  planeObj.rotation, int(plane_ctl_reg.tiled_surface),
                                                                  int(plane_ctl_reg.plane_rotation)),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(logger_template.format(res="FAIL", feature="PLANE_CTL_{} - [Tiling,Rotation]".format(plane_pipe),
                                             exp="[{0}({1}),{2}({3})]".format(MapTiling(planeObj.tiling),
                                                                              planeObj.tiling,
                                                                              MapRotation(planeObj.rotation),
                                                                              planeObj.rotation),
                                             act=[int(plane_ctl_reg.tiled_surface), int(plane_ctl_reg.plane_rotation)]))

    if plane_ctl_reg.source_pixel_format == MapPixelFormat(planeObj):
        logging.info(logger_template.format(res="PASS", feature="PLANE_CTL_{} - Pixel Format".format(plane_pipe),
                                            exp="{}({})".format(MapPixelFormat(planeObj), planeObj.pixelFormat),
                                            act=plane_ctl_reg.source_pixel_format))
        pixelFormat = True
        if (planeObj.pixelFormat == 'P010YUV420' or planeObj.pixelFormat == 'P012YUV420' or
                planeObj.pixelFormat == 'P016YUV420' or planeObj.pixelFormat == 'NV12YUV420'):
            if plane_ctl_reg.planar_yuv420_component:
                logging.info(
                    logger_template.format(res="PASS", feature="PLANE_CTL_{} - Planar Format".format(plane_pipe),
                                           exp="1", act=plane_ctl_reg.planar_yuv420_component))
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][PLANE]:PLANE_CTL_{0} - Planar Format values mis-matched! "
                          "Expected: 1 Actual: {1}".format(plane_pipe, plane_ctl_reg.planar_yuv420_component),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    logger_template.format(res="FAIL", feature="PLANE_CTL_{} - Planar Format".format(plane_pipe),
                                           exp="1", act=plane_ctl_reg.planar_yuv420_component))
                pixelFormat = False
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PLANE]:PLANE_CTL_{0} - Pixel Format values mis-matched! Expected: "
                  "{1}({2}) Actual: {3}".format(plane_pipe, MapPixelFormat(planeObj), planeObj.pixelFormat,
                                                plane_ctl_reg.source_pixel_format),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(logger_template.format(res="FAIL", feature="PLANE_CTL_{} - Pixel Format".format(plane_pipe),
                                             exp="{}({})".format(MapPixelFormat(planeObj), planeObj.pixelFormat),
                                             act=plane_ctl_reg.source_pixel_format))
    if tiling and hflip and rotation and pixelFormat:
        logging.debug("PASS : VerifyPlaneCtrl Verification for " + planeObj.display_port)
        return True

    return False


##
# @brief Verify if Scalar is enabled, call VerifyPlaneSizePosition()
#          to validate PLANE SIZE and PLANE_POSITION for passed planeID
# @param[in] planeObj PlaneStruct() object
# @param[in] plane_pipe plane and pipe suffix for register read
# @param[in] gfx_index graphics adapter
# @return bool return true if VerifyPlaneScalar() is success, else false
def VerifyPlaneScalar(planeObj, plane_pipe, gfx_index='gfx_0'):
    connected_pipe = planeObj.pipe.split("PIPE_")
    PLATFORM = planeObj.platform
    scalar_flag = 0

    scalar1_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_1_%s" % (connected_pipe[1]), PLATFORM,
                                    gfx_index=gfx_index)
    logging.debug("PS_CTRL_1_" + connected_pipe[1] + "--> Offset : "
                  + format(scalar1_reg.offset, '08X') + " Value :" + format(scalar1_reg.asUint, '08X'))

    scalar2_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_2_%s" % (connected_pipe[1]), PLATFORM,
                                    gfx_index=gfx_index)
    logging.debug("PS_CTRL_2_" + connected_pipe[1] + "--> Offset : " + format(scalar2_reg.offset, '08X') + " Value :" +
                  format(scalar2_reg.asUint, '08X'))

    if planeObj.scalar != (scalar1_reg.enable_scaler or scalar2_reg.enable_scaler):
        scalar_val = "Enable" if planeObj.scalar == 1 else "Disable"
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PLANE]:PLANE_CTL_{0} - Plane Scalar values mis-matched! Expected: "
                  "{1}({2}) Actual: {3} or {4}".format(plane_pipe, planeObj.scalar, scalar_val,
                                                       scalar1_reg.enable_scaler, scalar2_reg.enable_scaler),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(logger_template.format(res="FAIL", feature="PLANE_CTL_{} - Plane Scalar".format(plane_pipe),
                                             exp="{}({})".format(planeObj.scalar, scalar_val),
                                             act=scalar1_reg.enable_scaler or scalar2_reg.enable_scaler))
    if scalar1_reg.enable_scaler:
        if scalar1_reg.scaler_binding == planeObj.planeID:  # Plane scalar enabled
            scalar_flag = 1
    elif scalar2_reg.enable_scaler:
        if scalar2_reg.scaler_binding == planeObj.planeID:  # Plane scalar enabled
            scalar_flag = 2
    else:
        logging.info("INFO : PS_CTRL_1_{} & PS_CTRL_2_{} - PLANE Scalar NOT Enabled".format(connected_pipe[1],
                                                                                            connected_pipe[1]))

    return VerifyPlaneSizePosition(planeObj, plane_pipe, scalar_flag, gfx_index)


##
# @brief Verify PLANE SIZE and PLANE_POSITION for passed planeID
# @param[in] planeObj PlaneStruct() object
# @param[in] plane_pipe plane and pipe suffix for register read along
# @param[in] scalar  scalar flag
# @param[in] gfx_index graphics adapter
# @return bool return true if VerifyPlaneSizePosition() is success, else false
def VerifyPlaneSizePosition(planeObj, plane_pipe, scalar, gfx_index='gfx_0'):
    pipe = plane_pipe.split("_")
    if scalar == 0:
        plane_size = MMIORegister.read("PLANE_SIZE_REGISTER", "PLANE_SIZE_%s" % (plane_pipe), planeObj.platform,
                                       gfx_index=gfx_index)
        logging.debug("PLANE_SIZE_%s" % (plane_pipe) + "--> Offset : "
                      + format(plane_size.offset, '08X') + " Value :" + format(plane_size.asUint, '08X'))

        plane_pos = MMIORegister.read("PLANE_POS_REGISTER", "PLANE_POS_%s" % (plane_pipe), planeObj.platform,
                                      gfx_index=gfx_index)
        logging.debug(
            "PLANE_POS_%s" % (plane_pipe) + "-->Offset :" + format(plane_pos.offset, '08X') + "Value: " + format(
                plane_pos.asUint, '08X'))

        plane_size.height = (plane_size.height) + (2 * plane_pos.y_position)
        plane_size.width = (plane_size.width) + (2 * plane_pos.x_position)

        if plane_size.height == 0 and plane_size.width == 0:
            ## WA: in pre-si sporadically plane size is coming as 1x1. Adding 5 sec of delay and rechecking again
            is_pre_si_environment = SystemUtility().get_execution_environment_type() in ["SIMENV_FULSIM",
                                                                                         "SIMENV_PIPE2D"]
            if is_pre_si_environment:
                # Reading plane size post 5 sec delay
                time.sleep(5)
                plane_size = MMIORegister.read("PLANE_SIZE_REGISTER", "PLANE_SIZE_%s" % (plane_pipe), planeObj.platform,
                                               gfx_index=gfx_index)
                logging.debug("PLANE_SIZE_%s" % (plane_pipe) + "--> Offset : "
                              + format(plane_size.offset, '08X') + " Value :" + format(plane_size.asUint, '08X'))

                plane_pos = MMIORegister.read("PLANE_POS_REGISTER", "PLANE_POS_%s" % (plane_pipe), planeObj.platform,
                                              gfx_index=gfx_index)
                logging.debug(
                    "PLANE_POS_%s" % (plane_pipe) + "-->Offset :" + format(plane_pos.offset,
                                                                           '08X') + "Value: " + format(
                        plane_pos.asUint, '08X'))

                plane_size.height = (plane_size.height) + (2 * plane_pos.y_position)
                plane_size.width = (plane_size.width) + (2 * plane_pos.x_position)

                if plane_size.height == 0 and plane_size.width == 0:
                    logging.warning(
                        "WARN: Skipping plane size verification as plane size is 1x1 even after 5 sec of delay")
                    return True
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][PLANE]:PLANE_SIZE_{0} - (Width x Height) values mis-matched! "
                          "Expected: {1}x{2} Actual: {3}x{4}".format(plane_pipe, planeObj.planewidth,
                                                                     planeObj.planeheight,
                                                                     plane_size.width + 1, plane_size.height + 1),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    logger_template.format(res="FAIL", feature="PLANE_SIZE_{} - (Width x Height)".format(plane_pipe),
                                           exp="{} x {}".format(planeObj.planewidth, planeObj.planeheight),
                                           act="{} x {}".format(plane_size.width + 1, plane_size.height + 1)))
                return False

        elif plane_size.height == (planeObj.planeheight - 1) and plane_size.width == (planeObj.planewidth - 1):

            logging.info(
                logger_template.format(res="PASS", feature="PLANE_SIZE_{} - (Width x Height)".format(plane_pipe),
                                       exp="{} x {}".format(planeObj.planewidth, planeObj.planeheight),
                                       act="{} x {}".format(plane_size.width + 1, plane_size.height + 1)))
            return True

        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][PLANE]:PLANE_SIZE_{0} - (Width x Height) values mis-matched! "
                      "Expected: {1}x{2} Actual: {3}x{4}".format(plane_pipe, planeObj.planewidth, planeObj.planeheight,
                                                                 plane_size.width + 1, plane_size.height + 1),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                logger_template.format(res="FAIL", feature="PLANE_SIZE_{} - (Width x Height)".format(plane_pipe),
                                       exp="{} x {}".format(planeObj.planewidth, planeObj.planeheight),
                                       act="{} x {}".format(plane_size.width + 1, plane_size.height + 1)))
            return False
    else:
        plane_scalar_size = MMIORegister.read("PS_WIN_SZ_REGISTER", "PS_WIN_SZ_%s_%s" % (scalar, pipe[1]),
                                              planeObj.platform, gfx_index=gfx_index)
        logging.debug("PS_WIN_SZ_%s_%s" % (scalar, pipe[1]) + "--> Offset : "
                      + format(plane_scalar_size.offset, '08X') + " Value :" + format(plane_scalar_size.asUint, '08X'))

        if (plane_scalar_size.xsize == planeObj.planewidth) and (plane_scalar_size.ysize == planeObj.planeheight):
            logging.info(
                logger_template.format(res="PASS", feature="PS_WIN_SZ_{}_{} - (Width x Height)".format(scalar, pipe[1]),
                                       exp="{} x {}".format(planeObj.planewidth, planeObj.planeheight),
                                       act="{} x {}".format(plane_scalar_size.xsize, plane_scalar_size.ysize)))
            plane_scalar_pos = MMIORegister.read("PS_WIN_POS_REGISTER", "PS_WIN_POS_%s_%s" % (scalar, pipe[1]),
                                                 planeObj.platform, gfx_index=gfx_index)
            logging.debug("PS_WIN_POS_%s_%s" % (scalar, pipe[1]) + "--> Offset : "
                          + format(plane_scalar_pos.offset, '08X') + " Value :" + format(plane_scalar_pos.asUint,
                                                                                         '08X'))

            if (plane_scalar_pos.xpos == planeObj.planeposx and plane_scalar_pos.ypos == planeObj.planeposy):
                logging.info(logger_template.format(res="PASS",
                                                    feature="PS_WIN_POS_{}_{} - (X,Y-Position)".format(scalar, pipe[1]),
                                                    exp="{} x {}".format(planeObj.planeposx, planeObj.planeposy),
                                                    act="{} x {}".format(plane_scalar_pos.xpos, plane_scalar_pos.ypos)))
                return True
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][PLANE]:PS_WIN_POS_{0}_{1} - (X,Y-Position) values mis-matched! "
                          "Expected: {2}x{3} Actual: {4}x{5}".format(scalar, pipe[1], planeObj.planeposx,
                                                                     planeObj.planeposy, plane_scalar_pos.xpos,
                                                                     plane_scalar_pos.ypos),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(logger_template.format(res="FAIL",
                                                     feature="PS_WIN_POS_{}_{} - (X,Y-Position)".format(scalar,
                                                                                                        pipe[1]),
                                                     exp="{} x {}".format(planeObj.planeposx, planeObj.planeposy),
                                                     act="{} x {}".format(plane_scalar_pos.xpos,
                                                                          plane_scalar_pos.ypos)))
                return False
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][PLANE]:PS_WIN_SZ_{0}_{1} - (Width x Height) values mis-matched! "
                      "Expected: {2}x{3} Actual: {4}x{5}".format(scalar, pipe[1], planeObj.planewidth,
                                                                 planeObj.planeheight, plane_scalar_size.xsize,
                                                                 plane_scalar_size.ysize),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                logger_template.format(res="FAIL", feature="PS_WIN_SZ_{}_{} - (Width x Height)".format(scalar, pipe[1]),
                                       exp="{} x {}".format(planeObj.planewidth, planeObj.planeheight),
                                       act="{} x {}".format(plane_scalar_size.xsize, plane_scalar_size.ysize)))
            return False


##
# @brief Fill PlaneStruct() structure for Non-MPO scenario
# @param[in] planeObj plane parameters passed by user
# @param[in] gfx_index graphics adapter
# @return return PlaneStruct() object
def FillPlaneStruct(planeObj, gfx_index='gfx_0'):
    config = display_config.DisplayConfiguration()

    pipe_suffix = planeObj.pipe.split("PIPE_")
    scalar1_reg = None
    scalar2_reg = None

    display_and_adapter_info = config.get_display_and_adapter_info_ex(planeObj.display_port, gfx_index)
    if type(display_and_adapter_info) is list:
        display_and_adapter_info = display_and_adapter_info[0]

    is_pipe_joiner_required, no_of_pipe_required = DisplayClock.is_pipe_joiner_required(gfx_index,
                                                                                        planeObj.display_port)
    if is_pipe_joiner_required:
        logging.debug("Pipe Joiner is Enabled on Port".format(planeObj.display_port))

    if (planeObj.planewidth is None) or (planeObj.planeheight is None):
        scalar1_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_1_%s" % (pipe_suffix[1]), planeObj.platform,
                                        gfx_index=gfx_index)
        logging.debug(
            "PS_CTRL_1_" + pipe_suffix[1] + "--> Offset : " + format(scalar1_reg.offset, '08X') + " Value :" + format(
                scalar1_reg.asUint, '08X'))

        scalar2_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_2_%s" % (pipe_suffix[1]), planeObj.platform,
                                        gfx_index=gfx_index)
        logging.debug(
            "PS_CTRL_2_" + pipe_suffix[1] + "--> Offset : " + format(scalar2_reg.offset, '08X') + " Value :" + format(
                scalar2_reg.asUint, '08X'))

    source_mode = config.get_current_mode(display_and_adapter_info)
    if (scalar1_reg.enable_scaler and scalar1_reg.scaler_binding == 0) or (
            scalar2_reg.enable_scaler and scalar2_reg.scaler_binding == 0):
        logging.info("Pipe Scalar Enabled")
        # Pipe Scalar enabled
        target_mode = config.get_display_timings(display_and_adapter_info)
        if is_pipe_joiner_required:
            s_h_active, t_h_active = source_mode.HzRes, target_mode.hActive
            planeObj.planewidth = get_plane_width(gfx_index, planeObj, no_of_pipe_required, s_h_active, t_h_active, True,
                                                  source_mode.scaling)
        else:
            planeObj.planewidth = source_mode.HzRes
        planeObj.planeheight = source_mode.VtRes
    elif (scalar1_reg.enable_scaler and scalar1_reg.scaler_binding != 0) or (
            scalar2_reg.enable_scaler and scalar2_reg.scaler_binding != 0):
        logging.info("Plane Scalar Enabled")
        # Plane Scalar Enabled
        plane_info = get_plane_size_pos_info(display_and_adapter_info)
        if plane_info['status']:
            if is_pipe_joiner_required:
                s_h_active, t_h_active = plane_info['width'], plane_info['width']
                planeObj.planewidth = get_plane_width(gfx_index, planeObj, no_of_pipe_required, s_h_active, t_h_active, True,
                                                      source_mode.scaling)
            else:
                planeObj.planewidth = plane_info['width']
            planeObj.planeheight = plane_info['height']
            planeObj.planeposx = plane_info['posx']
            planeObj.planeposy = plane_info['posy']
    else:
        # Scalar not enabled
        target_mode = config.get_display_timings(display_and_adapter_info)
        if is_pipe_joiner_required:
            s_h_active, t_h_active = target_mode.hActive, target_mode.hActive
            planeObj.planewidth = get_plane_width(gfx_index, planeObj, no_of_pipe_required, s_h_active, t_h_active, False,
                                                  source_mode.scaling)
        else:
            planeObj.planewidth = target_mode.hActive
        planeObj.planeheight = target_mode.vActive

    if (planeObj.planeID is None):
        if check_layer_reordering(gfx_index):
            planeObj.planeID = 1  # Non-MPO, only plane_1 valid
        else:
            planeObj.planeID = 3  # Non-MPO, only plane_3 valid from LNL+
    if (planeObj.pixelFormat is None):
        planeObj.pixelFormat = "R8G8B8A8"
    if (planeObj.tiling is None):
        if env_settings.is_dod_driver_path() is True:
            planeObj.tiling = "LINEAR"
        elif planeObj.platform in ['MTL', 'DG2', 'ELG', 'LNL', 'PTL', 'NVL', 'CLS']:
            planeObj.tiling = "TILE_4"
        else:
            planeObj.tiling = "TILE_Y"
    if planeObj.rotation is None:
        planeObj.rotation = "DEG_0"
    if planeObj.hflip is None:
        planeObj.hflip = 0
    if (planeObj.planeposx is None) or (planeObj.planeposy is None):
        planeObj.planeposx = 0
        planeObj.planeposy = 0
    if planeObj.scalar is None:
        planeObj.scalar = (scalar1_reg.enable_scaler or scalar2_reg.enable_scaler)


##
# @brief        Helper function to calculate the plane width in pipe joiner cases.
# @param[in]    gfx_index: str
#                   Contains the Graphics adapter index in which the display is plugged.
# @param[in]    plane_object: DisplayPlane
#                   Contains the pipe programming related data for the plugged display.
# @param[in]    no_of_pipe_required: int
#                   Contains the no of pipes required to driver the display at current resolution.
# @param[in]    s_h_active: int
#                   Indicates plane source horizontal active width.
# @param[in]    t_h_active: int
#                   Indicates plane target horizontal active width.
# @param[in]    is_scalar_enabled: bool
#                   True if scalar is enabled for the current mode, False otherwise.
# @param[in]    scaling_mode: enum
#                   Tells the scaling of the current mode.
# @return       plane_width: int
#                   Returns the expected plane width based on bspec calculation for pipe joiner cases.
def get_plane_width(gfx_index, plane_object, no_of_pipe_required, s_h_active, t_h_active, is_scalar_enabled,
                    scaling_mode) -> int:
    is_dsc_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, plane_object.display_port)

    # Uncompressed Pipe Joiner case
    if is_dsc_enabled is False:
        plane_width = s_h_active / no_of_pipe_required

        if is_scalar_enabled and scaling_mode not in [enum.MDS, enum.CI]:
            plane_width = plane_width + PIPEEXCESS

        return plane_width

    # Reading the register directly since slice width will be verified in the DSC programming.
    r_offset = 'PPS3_' + str(DSCEngine.LEFT.value) + '_' + plane_object.pipe_suffix
    dsc_pps3 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_3", r_offset, plane_object.platform, gfx_index=gfx_index)
    slice_count = math.ceil(t_h_active / dsc_pps3.slice_width)
    no_of_slice_per_pipe = slice_count / no_of_pipe_required

    # Pixel Replication logic is supported from ELG
    # Basically calculates the pipe width along with the pixels that has to be replicated to make it even.
    if plane_object.platform in ["ELG"]:
        plane_width = (int(math.ceil(s_h_active / slice_count) * no_of_slice_per_pipe + 1) & ~1)

        # Planes won't have the replicated pixels, so for the last plane we need to remove the replicated pixels.
        if (
                (no_of_pipe_required == 4 and plane_object.pipe_suffix == 'D') or
                (no_of_pipe_required == 2 and plane_object.pipe_suffix == 'B')
        ):
            no_of_pixels_replicated = (dsc_pps3.slice_width * slice_count) - t_h_active
            plane_width = plane_width - no_of_pixels_replicated
    else:
        # Prior to ELG there is no pixel replication logic in HW. Driver also doesn't handle this case as there is no
        # standard modes that will result in odd slice width when dividing 8 slice. Modeset will fail if such resolution
        # is applied. Ideally driver should prune this mode if such case arises.
        # E.g 4500x2160, 4500/8 = 562.5 (pic width not evenly divisible by slice width case)
        plane_width = (s_h_active / slice_count) * no_of_slice_per_pipe

    # Pipe excess is added only when scalar is enabled and when scaling is not MDS or CI
    if is_scalar_enabled is True and scaling_mode not in [enum.MDS, enum.CI]:
        # For Ultra Pipe Joiner PIPE B and PIPE C will have excess pixels added on both sides.
        # Hence, pipe excess is multiplied by 2 only for those two pipes
        if no_of_pipe_required == 4 and plane_object.pipe_suffix in ['B', 'C']:
            plane_width = plane_width + (2 * PIPEEXCESS)
        else:
            plane_width = plane_width + PIPEEXCESS


    return plane_width


##
# @brief     Get GetCurrentMode Ex and identify applied plane size and plane position
# @param[in] display_and_adapter_info of active display
# @return  return Dict
def get_plane_size_pos_info(display_and_adapter_info):
    config = display_config.DisplayConfiguration()
    plane_info = {'status': False, 'height': None, 'width': None, 'posx': None, 'posy': None}

    mode_info_ex = config.query_display_config(display_and_adapter_info)
    if mode_info_ex.status == enum.DISPLAY_CONFIG_SUCCESS:
        plane_scaling = None
        di_source = mode_info_ex.desktopImageInfo.PathSourceSize
        di_region = mode_info_ex.desktopImageInfo.DesktopImageRegion
        di_clip_size = mode_info_ex.desktopImageInfo.DesktopImageClip

        # Determine Scaling to get plane Size
        if di_region.top == 0 and di_region.left == 0:
            # Maintain Display Scaling or Full Screen
            if (di_source.x == di_clip_size.right) and (di_source.y == di_clip_size.bottom):
                plane_scaling = "MDS"
            else:
                plane_scaling = "FS / MAR"
            plane_info['width'] = di_region.right + di_region.left
            plane_info['height'] = di_region.bottom + di_region.top
            plane_info['status'] = True
        elif di_region.top == 0 or di_region.left == 0:
            # Maintain Aspect Ratio
            plane_scaling = "MAR"
            plane_info['width'] = di_region.right - di_region.left
            plane_info['height'] = di_region.bottom - di_region.top
            plane_info['posx'] = di_region.left
            plane_info['posy'] = di_region.top
            plane_info['status'] = True
        elif di_region.top > 0 and di_region.left > 0:
            # Center Image
            plane_scaling = "CI"
            plane_info['width'] = di_region.right + di_region.left
            plane_info['height'] = di_region.bottom + di_region.top
            plane_info['status'] = True
        else:
            # Top/Left value is Invalid
            plane_info['status'] = False

        logging.info(
            "INFO : DesktopImageInfo SourceSize=({0}x{1}) ImageRegion=(L{3},T{2})x(R{5},B{4}) ImageClipSize=(L{7},T{6})x(R{9},B{8}) Scaling={10}".format(
                di_source.x, di_source.y, di_region.top, di_region.left, di_region.bottom, di_region.right,
                di_clip_size.top, di_clip_size.left, di_clip_size.bottom, di_clip_size.right, plane_scaling))
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][PLANE]:Failed to get CurrentModeEx",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("Get CurrentModeEx is Failed")

    return plane_info


##
# @brief Verify PLANE_CTL(plane enable/disable, pixel format, tiling, hflip, rotation) 
#        PLANE_COLOR_CTL(plane gamma), PLANE SIZE and PLANE_POSITION for passed planeID
# @param[in] plane_list PlaneStruct() object list
# @param[in] gfx_index graphics adapter
# @return bool return true if VerifyPlaneProgramming() is success, else false
def VerifyPlaneProgramming(plane_list, gfx_index='gfx_0'):
    status = fail_count = False

    for planeObj in plane_list:
        if planeObj.pipe is None:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][PLANE]:ERROR : {} port is NOT Connected to any Pipe".format(
                    planeObj.display_port),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(planeObj.display_port + " NOT Connected to any Pipe. Check if it is Connected")
            return False
        logging.info(
            "******* PLANE Verification for " + planeObj.display_port + " (Target ID : {}) - {} Connected to {},{} *******".format(
                planeObj.targetId,
                planeObj.display_port, planeObj.pipe, planeObj.ddi))
        FillPlaneStruct(planeObj, gfx_index)
        suffix = str(planeObj.planeID) + "_" + planeObj.pipe_suffix

        # WA: in pre-si sporadically plane is not enable, adding check to verify plane if plane enable
        plane_ctl_reg = MMIORegister.read("PLANE_CTL_REGISTER", "PLANE_CTL_%s" % suffix, planeObj.platform,
                                          gfx_index=gfx_index)
        logging.debug("PLANE_CTL_%s" % suffix + "--> Offset : "
                      + format(plane_ctl_reg.offset, '08X') + " Value :" + format(plane_ctl_reg.asUint, '08X'))

        if not plane_ctl_reg.plane_enable:
            is_pre_si_environment = SystemUtility().get_execution_environment_type() in ["SIMENV_FULSIM",
                                                                                         "SIMENV_PIPE2D"]
            if is_pre_si_environment:
                # Retry is needed bec there is delay in enabling plane after modeset or display switch (Yangra driver speci)
                time.sleep(5)
                plane_ctl_reg = MMIORegister.read("PLANE_CTL_REGISTER", "PLANE_CTL_%s" % suffix, planeObj.platform,
                                                  gfx_index=gfx_index)
                logging.warning("WARN : Rechecking after 5sec delay since plane is not enabled. PLANE_CTL_%s" % suffix +
                                "--> Offset : " + format(plane_ctl_reg.offset, '08X') + " Value :" +
                                format(plane_ctl_reg.asUint, '08X'))
                if not plane_ctl_reg.plane_enable:
                    logging.warning("WARN: Skipping plane verification as plane is disable after 5sec delay also")
                    return True
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][PLANE]:PLANE_CTL_{0} - Plane NOT Enabled.Expected: "
                          "1(ENABLED) Actual: {1}".format(suffix, plane_ctl_reg.plane_enable),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    logger_template.format(res="FAIL",
                                           feature="PLANE_CTL_{} - Plane NOT Enabled".format(suffix),
                                           exp="1(ENABLED)", act=plane_ctl_reg.plane_enable))
                return False
        status = VerifyPlaneCtrl(planeObj, suffix, gfx_index)

        if status is False:
            fail_count = True

        if (planeObj.platform != 'KBL') and (planeObj.platform != 'SKL') and (planeObj.platform != 'CFL'):
            status = VerifyColorCtrl(planeObj, suffix, gfx_index)
            if status is False:
                fail_count = True

        status = VerifyPlaneScalar(planeObj, suffix, gfx_index)
        if status is False:
            fail_count = True

    if fail_count:
        return False
    else:
        return status


if __name__ == "__main__":
    scriptName = os.path.basename(__file__).replace(".py", "")
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=FORMAT,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=scriptName + '.log',
                        filemode='w')

    plane_list = []
    plane_list.append(DisplayPlane("DP_A", 1, 1080, 1920, 0, 0, "TILE_Y", "R8G8B8A8", 1, "DEG_0", 0))
    # plane_list.append(DisplayPlane("DP_A"))

    result = VerifyPlaneProgramming(plane_list, 'gfx_0')
    if result is False:
        # GDHM handled in verifyPlaneProgramming(plane_list, gfx_index)
        logging.error("FAIL : verifyPlaneProgramming")
    else:
        logging.info("PASS : verifyPlaneProgramming")
