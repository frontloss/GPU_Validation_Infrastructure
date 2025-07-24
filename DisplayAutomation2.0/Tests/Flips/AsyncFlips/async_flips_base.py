########################################################################################################################
# @file         async_flips_base.py
# @brief        The script implements unittest default functions for setUp and tearDown, and  common helper functions
#               given below:
#               * Gets color space and pixel format string for a given pixel format.
#               * Function to perform flips.
# @author       Gaikwad, Suraj
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import cmd_parser, display_utility, enum
from Libs.Core import flip
from Libs.Core.system_utility import SystemUtility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.display_watermark.watermark import DisplayWatermark
from Tests.MPO.Flip.GEN11.MPO3H import register_verification
from Tests.Planes.Common.planes_verification import get_plane_id_from_layerindex
from Libs.Core.logger import gdhm

##
# @brief    Base class for Async Flips
class AsyncFlipsBase(unittest.TestCase):
    srcList = []
    destList = []
    currentMode = []
    sourceID = []
    color_space = []
    path = []
    blendingMode = []
    outputRange = []
    panelCaps = []
    hdrmetadata = []
    connected_list = []
    wm = DisplayWatermark()
    mpo = flip.MPO()
    is_ddrw = SystemUtility().is_ddrw()
    display_config = None
    stepCounter = 0
    pipe_id = []
    machine_info = SystemInfo()
    platform = None
    NoLayers = list()
    async_flip_flag = flip.MPO_PLANE_IN_FLAGS(0x2)
    sync_flip_flag = flip.MPO_PLANE_IN_FLAGS(0x1)
    pixel_format = [flip.SB_PIXELFORMAT.SB_R10G10B10A2, flip.SB_PIXELFORMAT.SB_R10G10B10A2]
    tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_X_TILED
    no_of_flips = 5


    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info(self.getStepInfo() + "****** TEST STARTS HERE ******************")
        self.test_name = sys.argv[0]
        my_tags = ['-pixelformat', '-tiling', '-count']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, my_tags)

        ##
        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        if self.cmd_line_param['TILING'] != "NONE":
            self.tiling = getattr(flip.SURFACE_MEMORY_TYPE, ''.join(self.cmd_line_param['TILING']))

        if self.cmd_line_param['COUNT'] != "NONE":
            self.no_of_flips = int(self.cmd_line_param['COUNT'][0])

        if len(self.connected_list) <= 0:
            gdhm.report_bug(
                title="[Async Flips]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.error("Minimum 1 display is required to run the test")
            self.fail()

        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        self.display_config = DisplayConfiguration()
        if self.display_config.set_display_configuration_ex(topology, self.connected_list) is False:
            self.fail('Failed to apply display configuration %s %s' %
                      (DisplayConfigTopology(topology).name, self.connected_list))

        logging.info('Successfully applied the display configuration as %s %s' %
                     (DisplayConfigTopology(topology).name, self.connected_list))

        self.underrun = UnderRunStatus()

        self.current_config = self.display_config.get_current_display_configuration()
        self.NoOfDisplays = self.current_config.numberOfDisplays
        for index in range(0, self.NoOfDisplays):
            # self.sourceID.append(self.current_config.displayPathInfo[index].sourceId)
            self.sourceID.append(index)
            display_base_obj = DisplayBase(self.connected_list[index])
            current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(self.connected_list[index])
            self.pipe_id.append(current_pipe)

        self.current_mode = self.display_config.get_current_mode(self.current_config.displayPathInfo[0].targetId)

        if self.current_mode.HzRes < self.current_mode.VtRes:
            self.srcList = [(360, 640), (540, 960), (720, 1280), (900, 1600), (1080, 1920), (1200, 1920)]
            self.destList1 = [(360, 640), (540, 960), (720, 1280), (900, 1600), (1080, 1920), (1200, 1920)]
        else:
            self.srcList = [(1024, 768), (1920, 1080), (2560, 1440), (3840, 2160), (4096, 2160)]
            self.destList1 = [(1024, 768), (1920, 1080), (2560, 1440), (3840, 2160), (4096, 2160)]

        for item in self.destList1:
            if item[0] <= self.current_mode.HzRes and item[1] <= self.current_mode.VtRes:
                self.destList.append(item)

        self.mpo.enable_disable_mpo_dft(True, 1)
        self.stepCounter = 0

        ##
        # Get the machine info
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break


    ##
    # @brief            Get the color space for provided pixel format
    # @param[in]        pixel_format; pixel format of the plane
    # @return           color space for the given pixel format
    def getColorSpaceForPixelFormat(self, pixel_format):
        if pixel_format < 14:
            color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709
        else:
            color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709

        return color_space


    ##
    # @brief            Get the step value for logging
    # @return           step count
    def getStepInfo(self):
        self.stepCounter = self.stepCounter + 1
        return "STEP-%d: " % self.stepCounter


    ##
    # @brief            Get the pixel format string for particular pixel format
    # @param[in]        pixel_format; pixel format of the plane
    # @return           pixel format string
    def getPixelFormatString(self, pixel_format):
        pixel_format_dict = {
            flip.SB_PIXELFORMAT.SB_8BPP_INDEXED: 'SB_8BPP_INDEXED',
            flip.SB_PIXELFORMAT.SB_B5G6R5X0: 'SB_B5G6R5X0',
            flip.SB_PIXELFORMAT.SB_B8G8R8X8: 'SB_B8G8R8X8',
            flip.SB_PIXELFORMAT.SB_B8G8R8A8: 'SB_B8G8R8A8',
            flip.SB_PIXELFORMAT.SB_R8G8B8X8: 'SB_R8G8B8X8',
            flip.SB_PIXELFORMAT.SB_R8G8B8A8: 'SB_R8G8B8A8',
            flip.SB_PIXELFORMAT.SB_R10G10B10X2: 'SB_R10G10B10X2',
            flip.SB_PIXELFORMAT.SB_R10G10B10A2: 'SB_R10G10B10A2',
            flip.SB_PIXELFORMAT.SB_B10G10R10X2: 'SB_B10G10R10X2',
            flip.SB_PIXELFORMAT.SB_B10G10R10A2: 'SB_B10G10R10A2',
            flip.SB_PIXELFORMAT.SB_R10G10B10A2_XR_BIAS: 'SB_R10G10B10A2_XR_BIAS',
            flip.SB_PIXELFORMAT.SB_R16G16B16X16F: 'SB_R16G16B16X16F',
            flip.SB_PIXELFORMAT.SB_R16G16B16A16F: 'SB_R16G16B16A16F',
            flip.SB_PIXELFORMAT.SB_MAX_PIXELFORMAT: 'SB_MAX_PIXELFORMAT',
        }
        if pixel_format <= getattr(flip.SB_PIXELFORMAT, 'SB_UNINITIALIZED') or \
                pixel_format > getattr(flip.SB_PIXELFORMAT, 'SB_MAXALL_PIXELFORMAT'):
            logging.error("Invalid pixel format")
            return " "
        else:
            return pixel_format_dict[pixel_format] + ", "


    ##
    # @brief            To perform Flips
    # @param[in]        planes ; details of planes
    # @return           void
    def performFlip(self, planes):

        scalar_enable = []
        plane_pixel_format = ""

        for index in range(0, planes.uiPlaneCount):
            pipe_id = self.pipe_id[planes.stPlaneInfo[index].iPathIndex]
            logging.info("Pipe : %d Plane : %d Src: (%d,%d,%d %d) , Dst : (%d,%d,%d,%d)  "
                         "Clip : (%d,%d,%d,%d) TileFormat: %s FlipType = %s",
                         pipe_id + 1,
                         int(self.NoLayers[pipe_id] - planes.stPlaneInfo[index].uiLayerIndex),
                         planes.stPlaneInfo[index].stMPOSrcRect.lLeft,
                         planes.stPlaneInfo[index].stMPOSrcRect.lTop,
                         planes.stPlaneInfo[index].stMPOSrcRect.lRight,
                         planes.stPlaneInfo[index].stMPOSrcRect.lBottom,
                         planes.stPlaneInfo[index].stMPODstRect.lLeft,
                         planes.stPlaneInfo[index].stMPODstRect.lTop,
                         planes.stPlaneInfo[index].stMPODstRect.lRight,
                         planes.stPlaneInfo[index].stMPODstRect.lBottom,
                         planes.stPlaneInfo[index].stMPOClipRect.lLeft,
                         planes.stPlaneInfo[index].stMPOClipRect.lTop,
                         planes.stPlaneInfo[index].stMPOClipRect.lRight,
                         planes.stPlaneInfo[index].stMPOClipRect.lBottom,
                         register_verification.mapSBTiling_RegisterFormat(planes.stPlaneInfo[index].eSurfaceMemType),
                         "Async" if planes.stPlaneInfo[index].stMPOPlaneInFlags == 0x2 else "Sync"
                         )

            plane_pixel_format += self.getPixelFormatString(planes.stPlaneInfo[index].ePixelFormat)

        plane_pixel_format = plane_pixel_format.strip()[:-1]

        logging.info(self.getStepInfo() + "Performing CheckMPO for %d planes with pixel format: %s"
                     % (planes.uiPlaneCount, plane_pixel_format))
        checkmpo_result = self.mpo.check_mpo3(planes)

        if checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
            logging.info("Performing flip for %d planes with pixel format: %s"
                         % (planes.uiPlaneCount, plane_pixel_format))
            ssa_result = self.mpo.set_source_address_mpo3(planes)
            if ssa_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
                for index in range(0, planes.uiPlaneCount):
                    if planes.stPlaneInfo[index].stMPOSrcRect.lRight != planes.stPlaneInfo[index].stMPODstRect.lRight \
                            or planes.stPlaneInfo[index].stMPOSrcRect.lBottom != planes.stPlaneInfo[
                        index].stMPODstRect.lBottom:
                        scalar_enable.append(1)

                logging.info(self.getStepInfo() + "Verifying watermark for %d planes with pixel format: %s"
                             % (planes.uiPlaneCount, plane_pixel_format))
                if self.wm.verify_watermarks() is not True:
                    self.fail("Watermark Error Observed after flip of %d planes with pixel format: %s"
                              % (planes.uiPlaneCount, plane_pixel_format))

                logging.info(self.getStepInfo() + "Verifying underrun for %d planes with pixel format: %s"
                             % (planes.uiPlaneCount, plane_pixel_format))
                if self.underrun.verify_underrun():
                    logging.error("Underrun Occurred after flip of %d planes with pixel format: %s"
                                  % (planes.uiPlaneCount, plane_pixel_format))

                logging.info(self.getStepInfo() + "Verifying Plane programming for %d planes with pixel format: %s"
                             % (planes.uiPlaneCount, plane_pixel_format))
                verify_result = True
                for index in range(0, planes.uiPlaneCount):
                    pipe_id = self.pipe_id[planes.stPlaneInfo[index].iPathIndex]
                    plane_id = get_plane_id_from_layerindex(self.NoLayers[pipe_id], planes.stPlaneInfo[index].uiLayerIndex, gfx_index='gfx_0')
                    verify_result = register_verification.verifyPlaneProgramming(pipe_id, plane_id,
                                                                                 planes.stPlaneInfo[index].ePixelFormat,
                                                                                 planes.stPlaneInfo[
                                                                                     index].eSurfaceMemType,
                                                                                 planes.stPlaneInfo[
                                                                                     index].stMPOClipRect.lLeft,
                                                                                 planes.stPlaneInfo[
                                                                                     index].stMPOClipRect.lTop,
                                                                                 planes.stPlaneInfo[
                                                                                     index].stMPOClipRect.lRight,
                                                                                 planes.stPlaneInfo[
                                                                                     index].stMPOClipRect.lBottom,
                                                                                 (planes.stPlaneInfo[
                                                                                      index].stMPOSrcRect.lRight -
                                                                                  planes.stPlaneInfo[
                                                                                      index].stMPOSrcRect.lLeft),
                                                                                 scalar_enable)

                if not verify_result:
                    gdhm.report_bug(
                        title="[Async Flips]Plane verification failed for {0} planes with pixel format {1}"
                            .format(planes.uiPlaneCount, plane_pixel_format),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for %d planes with pixel format %s"
                              % (planes.uiPlaneCount, plane_pixel_format))

                time.sleep(5)
            elif ssa_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                gdhm.report_bug(
                    title="[Async Flips]Resource creation failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Resource creation failed")
            else:
                gdhm.report_bug(
                    title="[Async Flips]Set source address failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Set source address failed")

        elif checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            gdhm.report_bug(
                title="[Async Flips]Resource creation failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Resource creation failed")
        else:
            logging.info("Driver did not meet the requirements")


    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        self.mpo.enable_disable_mpo_dft(False, 1)

        logging.info("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            display_utility.unplug(display)
        logging.info(self.getStepInfo() + "****** TEST ENDS HERE ******************")


if __name__ == '__main__':
    unittest.main()
