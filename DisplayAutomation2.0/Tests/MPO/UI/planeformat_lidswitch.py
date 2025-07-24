########################################################################################################################
# @file         planeformat_lidswitch.py
# @brief        Basic test to verify plane format getting enabled with no corruption while video is played and during
#               the lid events.
#               * Apply display configuration.
#               * Open media app and play it in full screen mode.
#               * Verify the plane format.
#               * Perform Watermark verification at different scenarios as mentioned below:
#                   * WM verification before Lid switch close.
#                   * WM verification during Lid switch close.
#                   * WM verification after Lid switch open.
#               * Close the media app.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import os
import sys
import time
import unittest

from Libs.Core import cmd_parser, display_utility, window_helper, winkb_helper, enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.display_power import DisplayPower, LidSwitchOption
from Libs.Core.hw_emu.hotplug_emulator_utility import HotPlugEmulatorUtility
from Libs.Core.hw_emu.she_utility import LidSwitchState
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_watermark.watermark import DisplayWatermark
from Tests.MPO import mpo_ui_helper


##
# @brief    Contains function to check plane format getting enabled with no corruption during the lid events
class PlaneformatLidSwitch(unittest.TestCase):
    connector_port_list = []
    hotplug_emulator_utility = HotPlugEmulatorUtility()
    under_run_status = UnderRunStatus()
    machine_info = SystemInfo()
    wm = DisplayWatermark()
    mpo_helper = mpo_ui_helper.MPOUIHelper()
    stepCounter = 0

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info("********* TEST STARTS HERE*****************")
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connector_port_list.insert(value['index'], value['connector_port'])

        if len(self.connector_port_list) <= 0:
            gdhm.report_bug(
                title="[MPO][Plane concurrency]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.error("Minimum 1 display is required to run the test")
            self.fail()

        ##
        # Get the OS Info
        system_utility = SystemUtility()
        self.os_info = self.machine_info.get_os_info()

        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        self.media_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_1920_1080_avc.mp4")

        self.under_run_status.clear_underrun_registry()

        self.stepCounter = 0

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        config = DisplayConfiguration()
        disp_power = DisplayPower()

        plane1_pixelformat = "source_pixel_format_RGB_8888"

        topology = enum.CLONE

        ##
        # Apply display configuration
        if config.set_display_configuration_ex(topology, self.connector_port_list) is True:
            logging.info(
                "Successfully applied the configuration as %s for %s" % (DisplayConfigTopology(topology).name,
                                                                         self.connector_port_list))
            winkb_helper.press('WIN+M')

            ##
            # Opens media app and plays it in full screen mode
            self.mpo_helper.play_media(self.media_file, True)

            ##
            # To enable 'Repeat' option in the Video App
            winkb_helper.press("CTRL+T")

            ##
            # Verify the plane format
            logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback application")
            if not self.mpo_helper.verify_planes(self.connector_port_list[0], 'PLANE_CTL_1', plane1_pixelformat):
                gdhm.report_bug(
                    title="[MPO][Plane concurrency]Plane verification for media playback application failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Plane verification for media playback application failed")

            time.sleep(25)
            ##
            # WM verification before Lid switch close
            logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
            if self.wm.verify_watermarks() is not True:
                self.fail("Error Observed in watermark verification")
            else:
                logging.info("Watermark verification passed")

            time.sleep(15)

            ##
            # Set the lid action to do nothing
            logging.info(self.mpo_helper.getStepInfo() + "Setting lid switch power state to LIDSWITCH_DONOTHING")
            lid_state = disp_power.set_lid_switch_power_state(LidSwitchOption.DO_NOTHING)
            if not lid_state:
                gdhm.report_bug(
                    title="[MPO][Plane concurrency]Setting the lid switch state failed",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Setting the lid switch state failed")

            ##
            # Perform lid close
            logging.info(self.mpo_helper.getStepInfo() + "Performing lid CLOSE")
            lid_close = self.hotplug_emulator_utility.lid_switch(LidSwitchState.CLOSE, 0)
            if not lid_close:
                gdhm.report_bug(
                    title="[MPO][Plane concurrency]Failed to close the lid",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Failed to close the lid")
            else:
                logging.info("Lid event successful")

            ##
            # Verify the plane format
            logging.info(
                self.mpo_helper.getStepInfo() + "Verifying plane for media playback application after lid events")
            if not self.mpo_helper.verify_planes(self.connector_port_list[1], 'PLANE_CTL_1',
                                                 "source_pixel_format_NV12_YUV_420"):
                gdhm.report_bug(
                    title="[MPO][Plane concurrency]Plane verification failed for media playback after lid events",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Plane verification failed for media playback after lid events")

            ##
            # The media app will play for 1 minute after lid close
            time.sleep(60)

            ##
            # WM verification during Lid switch close
            logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
            if self.wm.verify_watermarks() is not True:
                self.fail("Error Observed in watermark verification")
            else:
                logging.info("Watermark verification passed")

            ##
            # Close the media app
            window_helper.close_media_player()
            logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")

            ##
            # Opens media app and plays it in full screen mode
            self.mpo_helper.play_media(self.media_file, True)

            ##
            # To enable 'Repeat' option in the Video App
            winkb_helper.press("CTRL+T")

            ##
            # Verify the plane format
            logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback application")
            if not self.mpo_helper.verify_planes(self.connector_port_list[1], 'PLANE_CTL_1',
                                                 "source_pixel_format_NV12_YUV_420"):
                gdhm.report_bug(
                    title="[MPO][Plane concurrency]Plane verification failed for media playback application",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Plane verification failed for media playback application")

            ##
            # The media app will play for 1 minute
            time.sleep(25)

            ##
            # WM verification during Lid switch close
            logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
            if self.wm.verify_watermarks() is not True:
                self.fail("Error Observed in watermark verification")
            else:
                logging.info("Watermark verification passed")

            time.sleep(15)

            ##
            # Perform lid open
            logging.info(self.mpo_helper.getStepInfo() + "Performing lid  OPEN")
            lid_open = self.hotplug_emulator_utility.lid_switch(LidSwitchState.OPEN, 0)
            if not lid_open:
                gdhm.report_bug(
                    title="[MPO][Plane concurrency]Failed to open the lid",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Failed to open the lid")

            ##
            # The media app will play for 1 minute after opening the lid
            time.sleep(60)

            ##
            # Verify the plane format
            logging.info(
                self.mpo_helper.getStepInfo() + "Verifying plane for media playback application after lid set to OPEN state")
            if not self.mpo_helper.verify_planes(self.connector_port_list[0], 'PLANE_CTL_1', plane1_pixelformat):
                gdhm.report_bug(
                    title="[MPO][Plane concurrency]Plane verification failed for media playback application "
                          "after lid set to OPEN state",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Plane verification failed for media playback application after lid set to OPEN state")

            time.sleep(5)
            ##
            # WM verification after Lid switch open
            logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
            if self.wm.verify_watermarks() is not True:
                self.fail("Error Observed in watermark verification")
            else:
                logging.info("Watermark verification passed")

            time.sleep(5)

            ##
            # Close the media app
            window_helper.close_media_player()
            logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")

        else:
            self.fail("Failed to apply the configuration as %s for %s" % (DisplayConfigTopology(topology).name,
                                                                          self.connector_port_list))

    ##
    # @brief            Unittest runTest function
    # @return           void
    def tearDown(self):
        logging.info("Test Clean Up")
        window_helper.close_media_player()

        if self.under_run_status.verify_underrun() is True:
            logging.error("Underrun seen in the test")
        logging.info("********* TEST ENDS HERE*****************")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Verifies if MPO is getting enabled during video playback with lid events")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
