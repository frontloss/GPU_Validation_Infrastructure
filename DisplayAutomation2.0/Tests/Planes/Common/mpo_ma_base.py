########################################################################################################################
# @file         mpo_ma_base.py
# @brief        The script implements unittest default functions for setUp and tearDown, and common helper functions
#               given below:
#               * To create display adapter list
#               * Gets color space for a given pixel format.
#               * Gets the number of planes created for given source id.
#               * Function to perform flips.
# @author       Shetty, Anjali N
########################################################################################################################
import sys
import unittest
import logging
from collections import OrderedDict

from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_watermark.watermark import DisplayWatermark
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core import flip
from Libs.Core import cmd_parser, display_utility
from Tests.Planes.Common import planes_verification
from Libs.Core.logger import gdhm

##
# @brief    Base class for MPO multi adapter
class MPOMABase(unittest.TestCase):
    connected_list = []
    source_id = []
    pixel_format = []
    color_space = []
    tile_format = []
    dst_list = []
    current_mode = []
    display_details = OrderedDict()
    no_of_displays = 0
    step = 0
    display_config = disp_cfg.DisplayConfiguration()
    underrun = UnderRunStatus()
    wm = DisplayWatermark()
    mpo = flip.MPO()

    ##
    # @brief            To create display adapter list
    # @param[in]        key;
    # @param[in]        value
    # @return           void
    def create_display_adapter_list(self, key, value):
        if not bool(self.display_details):
            self.display_details[key] = []
            self.display_details[key].append(value)
        else:
            if key in self.display_details.keys():
                self.display_details[key].append(value)
            else:
                self.display_details[key] = []
                self.display_details[key].append(value)



    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        ##
        # Custom tags for input pixel format and tile format.
        my_tags = ['-input_pixelformat', '-input_tileformat', '-input_xml']

        ##
        # Parse the command line.
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, my_tags)

        ##
        # Obtain display port and adapter list from the command line.
        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        self.connected_list.insert(value['index'], value['connector_port'])
                        self.create_display_adapter_list(value['gfx_index'], value['connector_port'])

        ##
        # Verify and plug the display.
        if len(self.connected_list) >= 2:
            for key, value in self.display_details.items():
                if len(value) <= 0:
                    gdhm.report_bug(
                        title="[MPO]Invalid displays provided in command line",
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P3,
                        exposure=gdhm.Exposure.E3
                    )
                    self.fail("Minimum 1 display is required per adapter")

            for index in range(0, len(self.cmd_line_param)):
                for key, value in self.cmd_line_param[index].items():
                    if cmd_parser.display_key_pattern.match(key) is not None:
                        if value['connector_port'] is not None:
                            display_utility.plug_display(value['connector_port'], self.cmd_line_param[index])
        else:
            gdhm.report_bug(
                title="[MPO]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail("Minimum 2 displays are required for the test")

        ##
        # Get enumerated display details.
        enumerated_displays = self.display_config.get_enumerated_display_info()

        ##
        # Get current display configuration.
        topology, connector_port, display_and_adapter_info_list = self.display_config.get_current_display_configuration_ex(
            enumerated_displays)

        ##
        # Apply SINGLE display configuration across adapters.
        topology = enum.SINGLE
        if self.display_config.set_display_configuration_ex(topology, display_and_adapter_info_list) is False:
            self.fail('Step %s Failed to apply display configuration %s %s' %
                      (self.get_step_info(), DisplayConfigTopology(topology).name, connector_port))
        else:
            logging.info('Step %s Successfully applied the display configuration as %s %s' %
                         (self.get_step_info(), DisplayConfigTopology(topology).name, connector_port))

        ##
        # Get current applied mode across adapters.
        for display_and_adapter_info in display_and_adapter_info_list:
            self.current_mode.append(self.display_config.get_current_mode(display_and_adapter_info))

        ##
        # Source list and destination list for portrait and landscape panels.
        for mode in self.current_mode:
            if mode.HzRes < mode.VtRes:
                self.src_list = [(360, 640), (540, 960), (720, 1280), (900, 1600), (1080, 1920), (1200, 1920)]
                self.dest_list = [(360, 640), (540, 960), (720, 1280), (900, 1600), (1080, 1920), (1200, 1920)]
            else:
                self.src_list = [(1024, 768), (1920, 1080), (2560, 1440), (3840, 2160), (4096, 2160), (5120, 2880)]
                self.dest_list = [(1024, 768), (1920, 1080), (2560, 1440), (3840, 2160), (4096, 2160), (5120, 2880)]

            for res in self.dest_list:
                if (res[0] <= mode.HzRes and res[1] <= mode.VtRes):
                    self.dst_list.append(res)

        ##
        # Start underrun monitor.
        self.underrun.clear_underrun_registry()

        ##
        # Enable DFT for all the adapters.
        for key, value in self.display_details.items():
            self.mpo.enable_disable_mpo_dft(True, 1, key.lower())

    ##
    # @brief            Get the color space for provided pixel format
    # @param[in]        pixel_format; pixel format of the plane
    # @return           Color space for the given pixel format
    def get_color_space_for_pixel_format(self, pixel_format):
        if (pixel_format < 14):
            color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709
        else:
            color_space = flip.MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709

        return color_space

    ##
    # @brief            Get the no of planes created for given source id
    # @param[in]	    source_id; Source id of the plane
    # @param[in]	    pplanes; Pointer to structure containing the plane info
    # @return		    Plane count for the given source id
    def get_plane_count_for_source_id(self, source_id, pplanes):
        plane_count = 0
        for index in range(0, pplanes.uiPlaneCount):
            if source_id == pplanes.stPlaneInfo[index].iPathIndex:
                plane_count = plane_count + 1

        return plane_count

    ##
    # @brief        Get the step value for logging
    # @return       Step count
    def get_step_info(self):
        self.step = self.step + 1
        return self.step

    ##
    # @brief            To perform flips
    # @param[in]        pplanes; Plane parameters
    # @param[in]        gfx_adapter_index; graphics adapter index
    # @return           void
    def perform_flip(self, pplanes, gfx_adapter_index):
        format = ""

        logging.info("Step %s: Checking for the hardware support for plane parameters" % self.get_step_info())

        ##
        # Check for the hardware support for plane parameters
        supported = self.mpo.check_mpo3(pplanes, gfx_adapter_index)

        if supported:
            logging.info("Step %s: Flipping the planes and verifying the planes" % self.get_step_info())
            ##
            # Flip the content
            result = self.mpo.set_source_address_mpo3(pplanes, gfx_adapter_index)
            if result:
                logging.info("*****************Plane verification started*****************")
                for index in range(0, pplanes.uiPlaneCount):
                    plane_count = self.get_plane_count_for_source_id(pplanes.stPlaneInfo[index].iPathIndex, pplanes)
                    pipe_id = pplanes.stPlaneInfo[index].iPathIndex
                    plane_id = planes_verification.get_plane_id_from_layerindex(plane_count, pplanes.stPlaneInfo[index].uiLayerIndex, gfx_adapter_index)
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

                    if pplanes.stPlaneInfo[index].bEnabled:
                        if not planes_verification.verify_planes(pipe_id, plane_id, pixel_format, tile_format, width, scalar_enable,
                                             pplanes.stPlaneInfo[index].stMPOClipRect.lLeft,
                                             pplanes.stPlaneInfo[index].stMPOClipRect.lRight,
                                             pplanes.stPlaneInfo[index].stMPOClipRect.lTop,
                                             pplanes.stPlaneInfo[index].stMPOClipRect.lBottom,
                                             pplanes.stPlaneInfo[index].bEnabled, gfx_adapter_index):
                            gdhm.report_bug(
                                title="[MPO]Plane verification failed for Adapter: {} Pipe: {} Plane: {} Pixel format: {} "
                                      "Tile format: {}"
                                    .format(gfx_adapter_index, pipe_id, plane_id, planes_verification.get_register_string_from_pixel_format(pixel_format)[20:],
                                            planes_verification.get_register_string_from_tile_format(tile_format)[14:]),
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail(
                                "Plane verification failed for Adapter: {} Pipe: {} Plane: {} Pixel format: {} Tile format: {}"
                                    .format(gfx_adapter_index, pipe_id, plane_id,
                                            planes_verification.get_register_string_from_pixel_format(pixel_format)[20:],
                                            planes_verification.get_register_string_from_tile_format(tile_format)[14:]))
                        else:
                            logging.info(
                                "Plane verification passed for Adapter: {} Pipe: {} Plane: {} Pixel format: {} Tile format: {}"
                                    .format(gfx_adapter_index, pipe_id, plane_id,
                                            planes_verification.get_register_string_from_pixel_format(pixel_format)[20:],
                                            planes_verification.get_register_string_from_tile_format(tile_format)[14:]))
                    else:
                        if not planes_verification.verify_plane_status(pipe_id, plane_id, pplanes.stPlaneInfo[index].bEnabled):
                            gdhm.report_bug(
                                title="[MPO]Plane status verification failed for Pipe: {} Plane: {}"
                                    .format(pipe_id, plane_id),
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane status verification failed for Pipe: {} Plane: {}"
                                      .format(pipe_id, plane_id))
                        else:
                            logging.info("Plane status verification passed for Pipe: {} Plane {}"
                                         .format(pipe_id, plane_id))

                logging.info("*****************Plane verification ended*****************")

                if not self.wm.verify_watermarks():
                    self.fail("Fail: Watermark verification failed for {} planes with pixel formats {} on Adapter: {}"
                              .format(pplanes.uiPlaneCount, format, gfx_adapter_index))

                if self.underrun.verify_underrun():
                    logging.error("Fail: Underrun occurred after flipping {} planes with pixel formats {} on Adapter: {}"
                              .format(pplanes.uiPlaneCount, format, gfx_adapter_index))
        else:
            logging.info("Driver did not meet the plane requirements for Adapter: {}".format(gfx_adapter_index))

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info("Test cleanup")

        ##
        # Disable DFT and Unplug the displays and restore the configuration to the initial configuration.
        for key, value in self.display_details.items():
            self.mpo.enable_disable_mpo_dft(False, 1, key.lower())

            for display in value:
                if display != 'DP_A':
                    logging.info("Trying to unplug %s", display)
                    display_utility.unplug(display, gfx_index=key.lower())


if __name__ == '__main__':
    unittest.main()
