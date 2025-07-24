########################################################################################################################
# @file         package_residency_48hz.py
# @brief       The test script collects C2 and C8 residency values during 24fps video playback
#               in 60Hz and 48Hz mode and checks if the value is within threshold.
#
# CommandLine:  python package_residency_48hz.py -EDP_A -CONFIG SINGLE -EXPECTED_PIXELFORMAT NV12_YUV_420
#
# @author       Anjali Shetty
########################################################################################################################
import logging
import math
import os
import sys
import time
import unittest

from Libs.Core import winkb_helper, window_helper, enum, driver_escape
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature import socwatch
from Tests.MPO.mpo_ui_base import MPOUIBase


##
# @brief        PackageResidency48Mhz Class
class PackageResidency48Hz(MPOUIBase):
    socwatch_path, socwatch_command, socwatch_logfile_path = None, None, None
    registry_path, registry_value = None, None

    ##
    # @brief        Collect Package residency
    # @param[in]    display - display object
    # @param[in]    pixelformat - Pixel Format
    # @return       socwatch_output - Array Value
    def collect_package_residency(self, display, pixelformat):
        ##
        # Minimize all the window
        winkb_helper.press('WIN+M')

        ##
        # Open Media app and plays it in maximized mode
        self.mpo_helper.play_media(self.media_file, True)
        logging.info(self.mpo_helper.getStepInfo() + "Playing a 24fps video in fullscreen mode")

        ##
        # To enable 'Repeat' option in the Video App
        winkb_helper.press("CTRL+T")

        time.sleep(30)

        ##
        # Verify the Plane Format
        self.mpo_helper.verify_planes(display, 'PLANE_CTL_1', pixelformat)

        ##
        # Verify Watermark
        if self.wm.verify_watermarks(is_48hz_test=True) is not True:
            self.fail("Error Observed in watermark verification")
        else:
            logging.info("Watermark verification passed")

        ##
        # Run the SoCWatch tool
        logging.info(self.mpo_helper.getStepInfo() + "Started data collection using SoCWatch")
        result = socwatch.run_socwatch(self.socwatch_path, self.socwatch_command)
        self.assertEqual(result, True, "Failed to run SoCWatch")

        ##
        # Parse the SoCWatch output
        result, socwatch_output = socwatch.parse_socwatch_output(self.socwatch_logfile_path)
        if result is False:
            logging.error("Failed to parse SoCWatch Output")
            self.fail()

        ##
        # Close the Media app
        window_helper.close_media_player()
        logging.info(self.mpo_helper.getStepInfo() + "Closed media player")

        return socwatch_output[socwatch.SocWatchFields.PACKAGE_C2], socwatch_output[socwatch.SocWatchFields.PACKAGE_C8]

    ##
    # @brief        Check refresh rate support
    # @return       None
    def check_refresh_rate_support(self):
        ##
        # Get target id.
        self.target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)

        ##
        # Get EDID data of the panel.
        edid_flag, edid_data, _ = driver_escape.get_edid_data(self.target_id)
        if not edid_flag:
            logging.error(f"Failed to get EDID data for target_id : {self.target_id}")
            self.fail()

        ##
        # Extract the first timing information from the EDID
        pixel_clock1 = (edid_data[55] << 8) | edid_data[54]  # in 10kHz
        pixel_clock1 = int(float(pixel_clock1) / 100)  # in MHz
        self.h_active1 = ((edid_data[58] & 0xF0) << 4) | edid_data[56]
        h_blank1 = ((edid_data[58] & 0xF) << 8) | edid_data[57]
        self.v_active1 = ((edid_data[61] & 0xF0) << 4) | edid_data[59]
        v_blank1 = ((edid_data[61] & 0xF) << 8) | edid_data[60]
        rr = float(pixel_clock1 * 1000000) / float((self.h_active1 + h_blank1) * (self.v_active1 + v_blank1))
        self.refresh_rate1 = int(math.ceil(rr))
        self.assertNotEquals(self.refresh_rate1, 0, "First refresh rate from EDID is 0")
        logging.info("First Timing Info = %sHz",
                     (str(self.h_active1) + "x" + str(self.v_active1) + "@" + str(self.refresh_rate1)))

        ##
        # Extract the second timing information from the EDID
        pixel_clock2 = (edid_data[73] << 8) | edid_data[72]  # in 10kHz
        pixel_clock2 = int(float(pixel_clock2) / 100)  # in MHz
        self.h_active2 = ((edid_data[76] & 0xF0) << 4) | edid_data[74]
        h_blank2 = ((edid_data[76] & 0xF) << 8) | edid_data[75]
        self.v_active2 = ((edid_data[79] & 0xF0) << 4) | edid_data[77]
        v_blank2 = ((edid_data[79] & 0xF) << 8) | edid_data[78]
        rr = float(pixel_clock2 * 1000000) / float((self.h_active2 + h_blank2) * (self.v_active2 + v_blank2))
        self.refresh_rate2 = int(math.ceil(rr))
        self.assertNotEquals(self.refresh_rate2, 0, "Second refresh rate from EDID is 0")
        self.assertEquals(self.refresh_rate2, 48, "Panel does not support 48Hz")
        logging.info("Second Timing Info = %sHz",
                     (str(self.h_active2) + "x" + str(self.v_active2) + "@" + str(self.refresh_rate2)))

    ##
    # @brief        Test Run
    # @return       None
    def runTest(self):
        logging.info(
            "Test script collects C2 and C8 residency values during 24fps video playback in 60Hz and 48Hz mode and checks if the value is within threshold")

        ##
        # Check if only Single Display is connected.
        if len(self.connected_list) != 1:
            self.fail("Test can run only on Single eDP display")

        ##
        # Check if the Display connected id EDP.
        if 'DP_A' not in self.connected_list:
            self.fail("EDP should be part of display list to run this test")

        ##
        # Get the SoCWatch Path.
        self.socwatch_path = os.path.join(test_context.TestContext.test_store(), "SocWatch")

        ##
        # SoCWatch Command to collect System Information.
        self.socwatch_command = "socwatch -t 480 -f sys"

        ##
        # Get the SoCWatch log file path.
        self.socwatch_logfile_path = os.path.join(os.getcwd(), "SOCWatchOutput.csv")

        ##
        # Expected Pixel Format.
        pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])

        ##
        # Config to be applied.
        topology = enum.SINGLE

        ##
        # Apply Display Configuration.
        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info("Successfully applied Display Configuration as %s %s" % (
                DisplayConfigTopology(topology).name, self.connected_list))

            ##
            # Check if the Panel supports 2 Refresh Rates.
            logging.info(self.mpo_helper.getStepInfo() + "Check if the connected panel supports both 60Hz and 48Hz Refresh Rate")
            self.check_refresh_rate_support()

            ##
            # Get supported mode list.
            supported_mode = self.config.get_all_supported_modes([self.target_id])

            ##
            # Get Native mode.
            for key, values in supported_mode.items():
                for mode in values:
                    mode_str = mode.to_string(self.enumerated_displays)
                    if (str(self.h_active1) in mode_str and str(self.v_active1) in mode_str
                            and str(self.refresh_rate1) in mode_str and 'MDS' in mode_str):
                        self.native_mode = mode
                        break
            self.assertNotEquals(self.native_mode, None, "Getting native mode failed")
            logging.debug("Native mode = %s", self.native_mode.to_string(self.enumerated_displays))

            ##
            # Apply Native mode.
            result = self.config.set_display_mode([self.native_mode])
            self.assertEquals(result, True, "Applying native mode failed")
            logging.info(self.mpo_helper.getStepInfo() + "Mode applied = %s", self.native_mode.to_string(self.enumerated_displays))

            ##
            # Collect Package Residency values for 24fps Video Playback in Native mode.
            residency_c2_60, residency_c8_60 = self.collect_package_residency(self.connected_list[0], pixelformat)

            logging.info("C2 and C8 Package C-State Residency values for 60Hz is {}% and {}%".format(residency_c2_60,
                                                                                                     residency_c8_60))

            for key, values in supported_mode.items():
                for mode in values:
                    mode_str = mode.to_string(self.enumerated_displays)
                    if (str(self.h_active2) in mode_str and str(self.v_active2) in mode_str
                            and str(self.refresh_rate2) in mode_str and 'MDS' in mode_str):
                        self.mode_48hz = mode
                        break
            self.assertNotEquals(self.mode_48hz, None, "Getting the 48Hz mode failed")
            logging.debug("48Hz mode = %s", self.mode_48hz.to_string(self.enumerated_displays))

            result = self.config.set_display_mode([self.mode_48hz])
            self.assertEquals(result, True, "Applying the 48Hz mode failed")
            logging.info(self.mpo_helper.getStepInfo() + "Mode applied = %s", self.mode_48hz.to_string(self.enumerated_displays))

            residency_c2_48, residency_c8_48 = self.collect_package_residency(self.connected_list[0], pixelformat)

            logging.info(
                "C2 and C8 Package C-State Package Residency values for 48Hz is {}% and {}%".format(residency_c2_48,
                                                                                                    residency_c8_48))

            ##
            # Calculate 5% of the Residency values.
            delta_c2_48 = (float(residency_c2_48) / 100) * 10
            delta_c8_48 = (float(residency_c8_48) / 100) * 5

            ##
            # Check if the C2 residency value is within the specified range
            if ((residency_c2_60 >= (residency_c2_48 - delta_c2_48)) and (
                    residency_c2_60 <= (residency_c2_48 + delta_c2_48))):
                logging.info(
                    "C2 Package C-State Residency value for 60Hz is within the 10%({}%: range {}% <-> {}%) of 48Hz".format(
                        delta_c2_48, (residency_c2_48 - delta_c2_48), (residency_c2_48 + delta_c2_48)))
            else:
                logging.error(
                    "C2 Package C-State Residency value for 60Hz is not within the 10%({}%: range {}% <-> {}%) of 48Hz".format(
                        delta_c2_48, (residency_c2_48 - delta_c2_48), (residency_c2_48 + delta_c2_48)))
                self.fail(
                    "C2 Package C-State Residency value for 60Hz is not within the 10%({}: range {}% <-> {}%) of 48Hz".format(
                        delta_c2_48, (residency_c2_48 - delta_c2_48), (residency_c2_48 + delta_c2_48)))

            ##
            # Check if the C8 residency value is within the specified range
            if ((residency_c8_60 >= (residency_c8_48 - delta_c8_48)) and (
                    residency_c8_60 <= (residency_c8_48 + delta_c8_48))):
                logging.info(
                    "C8 Package C-State Residency value for 60Hz is within the 5%({}%: range {}% <-> {}%) of 48Hz".format(
                        delta_c8_48, (residency_c8_48 - delta_c8_48), (residency_c8_48 + delta_c8_48)))
            else:
                logging.error(
                    "C8 Package C-State Residency value for 60Hz is not within the 5%({}%: range {}% <-> {}%) of 48Hz".format(
                        delta_c8_48, (residency_c8_48 - delta_c8_48), (residency_c8_48 + delta_c8_48)))
                self.fail(
                    "C8 Package C-State Residency value for 60Hz is not within the 5%({}%: range {}% <-> {}%) of 48Hz".format(
                        delta_c8_48, (residency_c8_48 - delta_c8_48), (residency_c8_48 + delta_c8_48)))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
