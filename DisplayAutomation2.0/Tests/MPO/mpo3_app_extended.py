########################################################################################################################
# @file         mpo3_app_extended.py
# @brief        MPO App to test MPO basic functionality.
#               * Plug the displays.
#               * Verify devices are correctly plugged and enumerated.
#               * Enable the DFT framework and feature.
#               * Submit 2 flips one with RGB format and tiled surface Y and another with NV12 format and tiled surface linear.
#               * Disable the DFT framework and feature.
#               * Unplug the displays.
# @author       Shetty, Anjali N
########################################################################################################################
import importlib
import logging
import sys
import time
import unittest

from Libs.Core import cmd_parser, display_utility, flip, enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env.test_environment import TestEnvironment
from registers.mmioregister import MMIORegister
from Libs.Core.logger import gdhm

##
# @brief    Contains unittest default functions for setUp and tearDown function to test MPO basic functionality
class MPOApp(unittest.TestCase):
    enable_mpo = None
    platform = None
    connected_list = []
    reg_read = MMIORegister()
    config = DisplayConfiguration()
    machine_info = SystemInfo()

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        ##
        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        if len(self.connected_list) <= 0:
            gdhm.report_bug(
                title="[MPO]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.error("Minimum 1 display is required to run the test")
            self.fail()

        self.enable_mpo = flip.MPO()

        ##
        # Get the gfx display hardware info
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        ##
        # Enable the DFT framework and feature
        self.enable_mpo.enable_disable_mpo_dft(True, 1)

    ##
    # @brief            Verify the register programming
    # @param[in]        plane_ctl_reg; The name of the register
    # @param[in]        expected_pixel_format;  The pixel format
    # @param[in]        expected_tile_format;  The tile format
    # @return           void
    def verify_planes(self, plane_ctl_reg, expected_pixel_format, expected_tile_format):

        logging.info("=============================Plane Verification=============================")

        plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % (self.platform))

        plane_ctl_value = self.reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, self.platform, 0x0)

        plane_enable = plane_ctl_value.__getattribute__("plane_enable")
        if (plane_enable == getattr(plane_ctl, "plane_enable_DISABLE")):
            gdhm.report_bug(
                title="[MPO]Plane is not enabled",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.critical("Plane is not enabled")
            self.fail("Plane is not enabled")

        source_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")
        logging.info("%s [PIXEL FORMAT] Actual Value: %s Expected Value: %s" % (
            plane_ctl_reg, source_pixel_format, getattr(plane_ctl, expected_pixel_format)))
        if (source_pixel_format == getattr(plane_ctl, expected_pixel_format)):
            logging.info("Pixel format register verification passed")
        else:
            gdhm.report_bug(
                title="[MPO]Pixel format register verification failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.critical("Pixel format register verification failed")
            self.fail("Pixel format register verification failed")

        source_tile_format = plane_ctl_value.__getattribute__("tiled_surface")
        logging.info("%s [TILE FORMAT] Actual Value: %s Expected Value: %s" % (
            plane_ctl_reg, source_tile_format, getattr(plane_ctl, expected_tile_format)))
        if (source_tile_format == getattr(plane_ctl, expected_tile_format)):
            logging.info("Tile format register verification passed")
        else:
            gdhm.report_bug(
                title="[MPO]Tile format register verification failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.info("Tile format register verification failed")
            self.fail("Tile format register verification failed")

        logging.info("============================================================================")

    ##
    # @brief            To perform flips
    # @param[in]        pplanes; details of the planes
    # @param[in]        pixelformat;  The pixel format
    # @param[in]        tileformat;  The tile format
    # @return           void
    def perform_flip(self, pplanes, pixelformat, tileformat):
        ##
        # Check the hardware support for the plane
        supported = self.enable_mpo.check_mpo3(pplanes)

        if (supported):
            ##
            # Present the planes on the screen
            result = self.enable_mpo.set_source_address_mpo3(pplanes)
            if not result:
                gdhm.report_bug(
                    title="[MPO]Set source address failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("Set Source Address MPO Failed")
                self.fail()
            else:
                time.sleep(5)
                self.verify_planes('PLANE_CTL_1_A', pixelformat, tileformat)
        else:
            gdhm.report_bug(
                title="[MPO]Check MPO failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Check MPO failed")
            self.fail()

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        planes = []

        topology = enum.SINGLE
        if self.config.set_display_configuration_ex(topology, self.connected_list) is False:
            self.fail('Failed to apply display configuration %s %s' % (
                DisplayConfigTopology(topology).name, self.connected_list))

        logging.info('Successfully applied the display configuration as %s %s' % (
            DisplayConfigTopology(topology).name, self.connected_list))

        ##
        # Get the target id of the display
        target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)

        ##
        # Get current mode
        resolution = self.config.get_current_mode(target_id)

        logging.info("RGB Plane with Scaling and Blending scenario")
        source_rect_coordinates = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
        destination_rect_coordinates = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
        clip_rect_coordinates = flip.MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)

        plane1_attributes = flip.PLANE_INFO(0, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                            flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED,
                                            source_rect_coordinates, destination_rect_coordinates,
                                            clip_rect_coordinates,
                                            flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, flip.MPO_BLEND_VAL(0))

        source2_rect_coordinates = flip.MPO_RECT(0, 0, 1024, 768)
        plane2_attributes = flip.PLANE_INFO(0, 1, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                            flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED,
                                            source2_rect_coordinates, destination_rect_coordinates,
                                            clip_rect_coordinates,
                                            flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, flip.MPO_BLEND_VAL(0))

        planes.append(plane1_attributes)
        planes.append(plane2_attributes)

        pplanes = flip.PLANE(planes)

        self.perform_flip(pplanes, 'source_pixel_format_RGB_8888', 'tiled_surface_TILE_Y_LEGACY_MEMORY')

        logging.info("NV12 Plane with Linear Format")
        pplanes.stPlaneInfo[1].ePixelFormat = flip.PIXEL_FORMAT.PIXEL_FORMAT_NV12YUV420
        pplanes.stPlaneInfo[1].eSurfaceMemType = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR

        self.perform_flip(pplanes, 'source_pixel_format_NV12_YUV_420', 'tiled_surface_LINEAR_MEMORY')

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info("Test Clean Up")
        ##
        # Disable the DFT framework and feature
        self.enable_mpo.enable_disable_mpo_dft(False, 1)

        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            display_utility.unplug(display)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
