########################################################################################################################
# @file         mpo_tiled_sst_base.py
# @brief        The script implements unittest default functions for setUp and tearDown, and common helper functions
#               given below:
#               * Gets color space for a given pixel format.
#               * Function that checks hardware support and flips content.
#               * To calculate source width and height.
#               * To set the boundary values of the plane.
#               * Resize the plane according to the given direction.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import cmd_parser
from Libs.Core import flip
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import gdhm
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Tests.Display_Port.DP_Tiled import display_port_base
from Tests.Planes.Common import planes_verification
from Tests.Planes.Common import tiled_helper

##
# @brief    Base class for MPO Tile Base SST
class MPOTiledBaseSST(unittest.TestCase):
    config = DisplayConfiguration()
    display_port = DisplayPort()
    mpo = flip.MPO()
    sst_base = display_port_base.DisplayPortBase()
    tiled_display_helper = tiled_helper.TiledDisplayHelper()
    my_tags = ['-input_pixelformat', '-input_tileformat']
    dst_list = []
    color_space = []
    pixel_format = []
    tile_format = []
    step = 0

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info("************** TEST  STARTS HERE*************************")

        ##
        # Parse command line
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_tags)

        ##
        # Get the config details
        topology = self.cmd_line_param['CONFIG']

        ##
        # Get the DP panel details from the command line
        self.tiled_display_helper.process_command_line(self.cmd_line_param)

        ##
        # Plug tiled display
        self.sst_base.tiled_display_helper("Plug")

        ##
        # Set display configuration
        self.sst_base.set_config(topology)

        ##
        # Set tiled max mode
        self.sst_base.apply_tiled_max_modes()

        ##
        # Get current display config from DisplayConfig
        current_config = self.config.get_all_display_configuration()
        self.displays = current_config.numberOfDisplays

        for index in range(self.displays):
            tile_info = self.display_port.get_tiled_display_information(current_config.displayPathInfo[index].targetId)

            if tile_info.TiledStatus:
                ##
                # Get current applied mode.
                self.current_mode = self.config.get_current_mode(current_config.displayPathInfo[index].targetId)

        if self.current_mode:
            ##
            # Source list and destination list for portrait and landscape panels.
            self.src_list = [(1024, 768), (1920, 1080), (2560, 1440), (3840, 2160), (4096, 2160), (5120, 2880),
                             (7680, 4320)]
            ##
            # currently only fullscreen scaling is enabled
            self.dest_list = [(self.current_mode.HzRes, self.current_mode.VtRes)]

            for res in self.dest_list:
                if res[0] <= self.current_mode.HzRes and res[1] <= self.current_mode.VtRes:
                    self.dst_list.append(res)
        else:
            logging.error("Failed to fetch current mode")

        self.no_of_displays = self.displays - 1

        ##
        # Enable DFT.
        self.mpo.enable_disable_mpo_dft(True, 1)

    ##
    # @brief            Get the color space for provided pixel format
    # @param[in]        pixel_format; pixel format of the plane
    # @return           Color space for the given pixel format
    def get_color_space_for_pixel_format(self, pixel_format):
        if pixel_format < 14:
            color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709
        else:
            color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709

        return color_space

    ##
    # @brief            Get the step value for logging
    # @return           Step count
    def get_step_info(self):
        self.step = self.step + 1
        return self.step

    ##
    # @brief        Check for hardware support and flip content
    # @param[in]    pplanes; Plane parameters
    # @return       void
    def perform_flip(self, pplanes):
        format = ""

        logging.info("Step %s: Checking for the hardware support for plane parameters" % self.get_step_info())

        ##
        # Check for the hardware support for plane parameters
        checkmpo_result = self.mpo.check_mpo3(pplanes)

        if checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
            logging.info("Step %s: Flipping the planes and verifying the planes" % self.get_step_info())
            ##
            # Flip the content
            ssa_result = self.mpo.set_source_address_mpo3(pplanes)
            if ssa_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
                logging.info("*****************Plane verification started*****************")
                for index in range(0, pplanes.uiPlaneCount):
                    plane_count = pplanes.uiPlaneCount
                    pipe_id = pplanes.stPlaneInfo[index].iPathIndex
                    plane_id = planes_verification.get_plane_id_from_layerindex(plane_count, pplanes.stPlaneInfo[index].uiLayerIndex, gfx_index='gfx_0')
                    pixel_format = pplanes.stPlaneInfo[index].ePixelFormat
                    tile_format = pplanes.stPlaneInfo[index].eSurfaceMemType
                    width = pplanes.stPlaneInfo[index].stMPOSrcRect.lRight - pplanes.stPlaneInfo[
                        index].stMPOSrcRect.lLeft
                    if (pplanes.stPlaneInfo[index].stMPOSrcRect.lRight != pplanes.stPlaneInfo[index].stMPODstRect.lRight
                            or pplanes.stPlaneInfo[index].stMPOSrcRect.lBottom != pplanes.stPlaneInfo[
                                index].stMPODstRect.lBottom
                            or pplanes.stPlaneInfo[index].stMPOSrcRect.lLeft != pplanes.stPlaneInfo[
                                index].stMPODstRect.lLeft
                            or pplanes.stPlaneInfo[index].stMPOSrcRect.lTop != pplanes.stPlaneInfo[
                                index].stMPODstRect.lTop):
                        scalar_enable = 1
                    else:
                        scalar_enable = 0

                    format += planes_verification.get_register_string_from_pixel_format(pixel_format)[20:]

                    if not planes_verification.verify_planes_tiled(plane_id, pixel_format, tile_format,
                                                                   pplanes.stPlaneInfo[index].bEnabled):
                        gdhm.report_bug(
                            title="[MPO]Plane verification failed for Plane: {} Pixel format: {} Tile format: {}"
                                .format(plane_id,
                                        planes_verification.get_register_string_from_pixel_format(pixel_format)[20:],
                                        planes_verification.get_register_string_from_tile_format(tile_format)[14:]),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail(
                            "Plane verification failed for Plane: {} Pixel format: {} Tile format: {}" .format(plane_id,
                                        planes_verification.get_register_string_from_pixel_format(pixel_format)[20:],
                                        planes_verification.get_register_string_from_tile_format(tile_format)[14:]))
                    else:
                        logging.info(
                            "Plane verification passed for Plane: {} Pixel format: {} Tile format: {}" .format(plane_id,
                                        planes_verification.get_register_string_from_pixel_format(pixel_format)[20:],
                                        planes_verification.get_register_string_from_tile_format(tile_format)[14:]))

                logging.info("*****************Plane verification ended*****************")

            elif ssa_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                gdhm.report_bug(
                    title="[MPO]Resource creation failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Resource creation failed")
            else:
                gdhm.report_bug(
                    title="[MPO]Resource creation failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Set source address failed")
        elif checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            gdhm.report_bug(
                title="[MPO]Resource creation failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Resource creation failed")
        else:
            logging.info("Driver did not meet the plane requirements")

    ##
    # @brief            Calculate the source width and height
    # @param[in]        plane_info; The plane whose width and height should be calculated
    # @return           void
    def source_rect(self, plane_info):
        self.source_width = plane_info.stMPOSrcRect.lRight - plane_info.stMPOSrcRect.lLeft
        self.source_height = plane_info.stMPOSrcRect.lBottom - plane_info.stMPOSrcRect.lTop

    ##
    # @brief            Set the boundary values of the plane
    # @param[in]        hres; Horizontal boundary
    # @param[in]        vres; Vertical boundary
    # @return           void
    def set_bounds(self, hres, vres):
        self.source_bound = flip.MPO_RECT(0, 0, hres, vres)
        self.destination_bound = flip.MPO_RECT(0, 0, hres, vres)
        self.clip_bound = flip.MPO_RECT(0, 0, hres, vres)

    ##
    # @brief            Resize the plane according to the given direction
    # @param[in]        plane_info; The plane to be resized
    # @param[in]        cdirection; The direction in which the plane has to be resized
    # @param[in]        ivalue; The value to resize the plane
    # @return           Returns 1(True) on resizing the plane; else 0(False)
    def resize(self, plane_info, cdirection, ivalue):
        shrink_factor = 3

        if (cdirection == "Right"):
            plane_info.stMPODstRect.lRight = plane_info.stMPODstRect.lRight + ivalue
            plane_info.stMPOClipRect.lRight = plane_info.stMPOClipRect.lRight + ivalue
            if (plane_info.stMPODstRect.lRight > self.destination_bound.lRight
                    or plane_info.stMPODstRect.lRight <= plane_info.stMPODstRect.lLeft):
                plane_info.stMPODstRect.lRight = plane_info.stMPODstRect.lRight - ivalue
                plane_info.stMPOClipRect.lRight = plane_info.stMPOClipRect.lRight - ivalue
                return False

            ldst_width = plane_info.stMPODstRect.lRight - plane_info.stMPODstRect.lLeft
            if shrink_factor >= (self.source_width / ldst_width):
                plane_info.stMPOSrcRect.lRight = plane_info.stMPODstRect.lRight

            if (plane_info.stMPODstRect.lRight > self.clip_bound.lRight):
                plane_info.stMPOClipRect.lRight = self.clip_bound.lRight

        elif (cdirection == "Left"):
            plane_info.stMPODstRect.lLeft = plane_info.stMPODstRect.lLeft + ivalue
            plane_info.stMPOClipRect.lLeft = plane_info.stMPOClipRect.lLeft + ivalue
            if (plane_info.stMPODstRect.lLeft < self.destination_bound.lLeft
                    or plane_info.stMPODstRect.lLeft >= plane_info.stMPODstRect.lRight):
                plane_info.stMPODstRect.lLeft = plane_info.stMPODstRect.lLeft - ivalue
                plane_info.stMPOClipRect.lLeft = plane_info.stMPOClipRect.lLeft - ivalue
                return False

            ldst_width = plane_info.stMPODstRect.lRight - plane_info.stMPODstRect.lLeft
            if shrink_factor >= (self.source_width / ldst_width):
                plane_info.stMPOSrcRect.lLeft = plane_info.stMPODstRect.lLeft

            if (plane_info.stMPODstRect.lLeft < self.clip_bound.lLeft):
                plane_info.stMPOClipRect.lLeft = self.clip_bound.lLeft

        elif (cdirection == "Bottom"):
            plane_info.stMPODstRect.lBottom = plane_info.stMPODstRect.lBottom + ivalue
            plane_info.stMPOClipRect.lBottom = plane_info.stMPOClipRect.lBottom + ivalue
            if (plane_info.stMPODstRect.lBottom > self.destination_bound.lBottom
                    or plane_info.stMPODstRect.lBottom <= plane_info.stMPODstRect.lTop):
                plane_info.stMPODstRect.lBottom = plane_info.stMPODstRect.lBottom - ivalue
                plane_info.stMPOClipRect.lBottom = plane_info.stMPOClipRect.lBottom - ivalue
                return False

            ldst_height = plane_info.stMPODstRect.lBottom - plane_info.stMPODstRect.lTop
            if shrink_factor >= (self.source_height / ldst_height):
                plane_info.stMPOSrcRect.lBottom = plane_info.stMPODstRect.lBottom

            if (plane_info.stMPODstRect.lBottom > self.clip_bound.lBottom):
                plane_info.stMPOClipRect.lBottom = self.clip_bound.lBottom

        elif (cdirection == "Top"):
            plane_info.stMPODstRect.lTop = plane_info.stMPODstRect.lTop + ivalue
            plane_info.stMPOClipRect.lTop = plane_info.stMPOClipRect.lTop + ivalue
            if (plane_info.stMPODstRect.lTop < self.destination_bound.lTop
                    or plane_info.stMPODstRect.lTop >= plane_info.stMPODstRect.lBottom):
                plane_info.stMPODstRect.lTop = plane_info.stMPODstRect.lTop - ivalue
                plane_info.stMPOClipRect.lTop = plane_info.stMPOClipRect.lTop - ivalue
                return False

            ldst_height = plane_info.stMPODstRect.lBottom - plane_info.stMPODstRect.lTop
            if shrink_factor >= (self.source_height / ldst_height):
                plane_info.stMPOSrcRect.lTop = plane_info.stMPODstRect.lTop

            if (plane_info.stMPODstRect.lTop < self.clip_bound.lTop):
                plane_info.stMPOClipRect.lTop = self.clip_bound.lTop

        return True

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info("Test cleanup")

        ##
        # Disable DFT.
        self.mpo.enable_disable_mpo_dft(False, 1)

        enumerated_displays = self.config.get_enumerated_display_info()
        ##
        # is_internal_display_connected() tells whether an internal display is connected or not.
        internal_display_list = self.config.get_internal_display_list(enumerated_displays)
        if enumerated_displays.Count >= 2 and len(internal_display_list) != 0:
            ##
            # unplug tiled display
            self.sst_base.tiled_display_helper("Unplug")

        logging.info("****************TEST ENDS HERE********************************")


if __name__ == '__main__':
    unittest.main()
