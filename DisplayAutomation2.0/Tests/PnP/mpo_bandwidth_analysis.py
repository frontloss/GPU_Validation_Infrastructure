########################################################################################################################
# @file         mpo_bandwidth_analysis.py
# @brief        The test script measures the memory bandwidth during the video playback.
# @details      It collects the bandwidth data for the default format enabled in the driver
#               and for the RGB format and gives the delta between them.
#
#               CommandLine: python mpo_bandwidth_analysis.py -EDP_A -EXPECTED_PIXELFORMAT NV12_YUV_420
#
# @author       Anjali Shetty
########################################################################################################################
import logging
import os
import sys
import time
import unittest

from Libs.Core import winkb_helper, enum, window_helper, registry_access, display_essential
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature import socwatch
from Tests.MPO.mpo_ui_base import MPOUIBase


##
# @brief        MPOBandwidthAnalysis Class
class MPOBandwidthAnalysis(MPOUIBase):
    socwatch_path, socwatch_command, socwatch_logfile_path = None, None, None
    registry_path, registry_value = None, None
    ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')

    ##
    # @brief        Play Clip Calculate Bandwidth
    # @param[in]    display - display object
    # @param[in]    pixelformat - the pixel format
    # @return       memory_bandwidth - The memory bandwidth
    def play_clip_claculate_bandwidth(self, display, pixelformat):
        memory_bandwidth = 0

        ##
        # Minimize all the window
        winkb_helper.press('WIN+M')

        ##
        # Open Media app and plays it in maximized mode
        self.mpo_helper.play_media(self.media_file, True)

        ##
        # To enable 'Repeat' option in the Video App
        winkb_helper.press("CTRL+T")

        time.sleep(2)

        ##
        # Verify the plane format
        self.mpo_helper.verify_planes(display, 'PLANE_CTL_1', pixelformat)

        ##
        # Run the SoCWatch tool
        result = socwatch.run_socwatch(self.socwatch_path, self.socwatch_command)
        self.assertEqual(result, True, "Failed to run SoCWatch")
        logging.info("Started data collection using SoCWatch")
        ##
        # Parse the SoCWatch output
        result, socwatch_output = socwatch.parse_socwatch_output(self.socwatch_logfile_path)
        if result is False:
            logging.error("Failed to parse SoCWatch Output")
            self.fail()

        memory_bandwidth = socwatch_output[socwatch.SocWatchFields.TOTAL_BANDWIDTH]
        logging.info("Total memory bandwidth for %s playback is %s MB/s" % (pixelformat, memory_bandwidth))
        logging.info("Total GT request bandwidth for %s playback is %s MB/s" % (
            pixelformat, socwatch_output[socwatch.SocWatchFields.GT_REQUESTS]))
        logging.info("Total IA request bandwidth for %s playback is %s MB/s" % (
            pixelformat, socwatch_output[socwatch.SocWatchFields.IA_REQUESTS]))
        logging.info("Total IO request bandwidth for %s playback is %s MB/s" % (
            pixelformat, socwatch_output[socwatch.SocWatchFields.IO_REQUESTS]))

        ##
        # Close the Media app
        window_helper.close_media_player()

        return memory_bandwidth

    ##
    # @brief        Test run
    # @return       None
    def runTest(self):

        ##
        # SoCWatch path
        self.socwatch_path = os.path.join(test_context.TestContext.test_store(), "SocWatch")

        ##
        # SoCWatch command to collect bandwidth data for 60 seconds
        self.socwatch_command = "socwatch -t 60 -f ddr-bw"

        ##
        # SoCWatch log file path
        self.socwatch_logfile_path = os.path.join(os.getcwd(), "SOCWatchOutput.csv")

        pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])

        topology = enum.SINGLE

        if self.config.set_display_configuration_ex(topology, [self.connected_list[0]]) is True:
            logging.info("Successfully applied the configuration")

            time.sleep(2)

            ##
            # Open and close the media to overcome the OS issue where we are seeing the media not playing
            # in the expected format at very first time on few OS images.
            self.mpo_helper.play_media(self.media_file, True)
            time.sleep(20)
            window_helper.close_media_player()

            ##
            # Play the clip and parse the output
            memory_bandwidth = self.play_clip_claculate_bandwidth(self.connected_list[0], pixelformat)

            ##
            # Read the default value of DisplayFeatureControl registry
            self.registry_value, _ = registry_access.read(args=self.ss_reg_args, reg_name="DisplayFeatureControl")
            ##
            # Calculate registry value to play the clip in RGB format
            rgb_value_registry = self.registry_value & 0x37D

            ##
            # Modify the registry value
            registry_access.write(args=self.ss_reg_args, reg_name="DisplayFeatureControl",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=rgb_value_registry)

            ##
            # Restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()

            time.sleep(2)

            ##
            # Play the clip and parse the output
            memory_bandwidth_rgb = self.play_clip_claculate_bandwidth(self.connected_list[0],
                                                                      "source_pixel_format_RGB_8888")

            logging.info("The delta between RGB_8888 and %s is %s percent" % (
                pixelformat, ((memory_bandwidth / memory_bandwidth_rgb) * 100)))

            # if self.cmd_line_param['EXPECTED_PIXELFORMAT'][0] == "YUV_422_PACKED_8_BPC":
            #     if memory_bandwidth_rgb > (memory_bandwidth * 2):
            #         logging.info("%s is saving bandwidth" % self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
            #     else:
            #         logging.info("%s is not saving expected bandwidth" % self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
            #         self.fail()
            #
            # elif self.cmd_line_param['EXPECTED_PIXELFORMAT'][0] == "NV12_YUV_420":
            #     if memory_bandwidth_rgb > (memory_bandwidth * 2.66):
            #         logging.info("%s is saving bandwidth" % self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
            #     else:
            #         logging.info("%s is not saving expected bandwidth" % self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
            #         self.fail()

            ##
            # Set the default registry value
            registry_access.write(args=self.ss_reg_args, reg_name="DisplayFeatureControl",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=self.registry_value)

            ##
            # Restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()

        else:
            self.fail("Failed to apply Display Configuration")

    ##
    # @brief        Tear Down function
    # @return       None
    def tearDown(self):
        exc_tuple = sys.exc_info()

        ##
        # Check if there is any failure in the test
        if exc_tuple.count(None) != len(exc_tuple):
            ##
            # Set the default registry value if there is any failure
            registry_access.write(args=self.ss_reg_args, reg_name="DisplayFeatureControl",
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=self.registry_value)

            ##
            # Restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
