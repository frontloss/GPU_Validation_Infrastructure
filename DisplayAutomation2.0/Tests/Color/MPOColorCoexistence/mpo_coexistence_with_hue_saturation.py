##############################################################################################
# \file
# \addtogroup       Test_Color
# \section          mpo_coexistence_with_hue_saturation
# \ref              mpo_coexistence_with_hue_saturation.py \n
# \remarks          This script performs color functionality such as applying hue and saturation
#                   while the video app is played and verifies for the plane CSC status.
# CommandLine:      python mpo_coexistence_with_hue_saturation.py -edp_a
# \author           Anjali Shetty
###############################################################################################
from random import randint

from Libs.Core import enum, registry_access, display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.winkb_helper import snap_right, snap_left
from Tests.Color import color_common_utility as color_utility
from Tests.Color.MPOColorCoexistence.mpo_coexistence_base import *


class MPOCoexistenceWithHueSaturation(MPOCoexistenceBase):
    def runTest(self):
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        ##
        # Disable xvYCC feature
        if registry_access.write(args=reg_args, reg_name="XVYCCFeatureEnable",
                                 reg_type=registry_access.RegDataType.DWORD, reg_value=0) is False:
            logging.error("Registry key add to disable XVYCC feature failed")
            self.fail()

        ##
        # Restart driver
        status, reboot_required = display_essential.restart_gfx_driver()
        each_disp = 0
        time.sleep(5)

        ##
        # Verify if Hue and Saturation are supported by all the plugged displays
        for each_disp in range(len(self.connected_list)):
            ##
            # Get the device id
            device_id = color_utility.get_device_id(self.connected_list[each_disp])

            ##
            # To Check if Hue and Saturation are supported
            hue_sat = cui_sdk.HueSatInfo(deviceID=device_id)
            sdk_status, hue_sat = cui_sdk.get_hue_sat_info(hue_sat)
            if sdk_status:
                if hue_sat.isFeatureSupported:
                    logging.info("Hue and Saturation supported on %s" % self.connected_list[each_disp])
                else:
                    logging.info("Hue and Saturation not supported on %s" % self.connected_list[each_disp])
                    self.fail()
            else:
                logging.error(f"SDK call failed: get_hue_sat_info() for device_id {device_id}")
                self.fail()

        hue_sat = cui_sdk.HueSatInfo(device_id=0, hue_value=0, sat_value=0)
        topology = enum.SINGLE
        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info("Successfully applied the configuration")

                hue_sat.deviceID = color_utility.get_device_id(self.connected_list[each_disp])

                press('WIN+M')

                ##
                # Opens media app and plays it in windowed mode
                self.play_media(False)

                ##
                # Play the video in snapmode
                snap_right()
                time.sleep(5)

                ##
                # Verify the registers
                plane_csc, plane_gamma, format_verify = verify_mpo_color_coexistence(
                    self.connected_list[display_index], 'PLANE_CTL_1', 'PLANE_COLOR_CTL_1',
                    self.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0]))

                ##
                # Check plane CSC and pixel format status
                if plane_csc == "disabled" or format_verify is False:
                    self.fail()

                target_id = self.config.get_target_id(self.connected_list[display_index], self.enumerated_displays)
                hue_sat.hueSettings.currentValue = randint(0, 360)
                logging.info("Trying to set Saturation Hue value of %s on %s" % (
                    hue_sat.hueSettings.currentValue, self.connected_list[display_index]))

                ##
                # Set the hue value
                result = cui_sdk.set_hue_sat_info(hue_sat)
                if not result:
                    logging.error(
                        f"SDK call failed: set_hue_sat_info() for device_id {self.connected_list[display_index]}")
                    self.fail()
                else:
                    ##
                    # Verify the registers
                    plane_csc, plane_gamma, format_verify = verify_mpo_color_coexistence(
                        self.connected_list[display_index], 'PLANE_CTL_1', 'PLANE_COLOR_CTL_1',
                        self.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0]))

                    ##
                    # Check plane CSC and pixel format status
                    if plane_csc == "disabled" or format_verify is False:
                        self.fail()

                hue_sat.saturationSettings.currentValue = randint(-100, 100)
                logging.info("Trying to set Saturation value of %s on %s" % (
                    hue_sat.saturationSettings.currentValue, self.connected_list[display_index]))

                ##
                # Set the saturation value
                result = cui_sdk.set_hue_sat_info(hue_sat)
                if not result:
                    logging.error(
                        f"SDK call failed: set_hue_sat_info() for device_id {self.connected_list[display_index]}")
                    self.fail()
                else:
                    ##
                    # Verify the registers
                    plane_csc, plane_gamma, format_verify = verify_mpo_color_coexistence(
                        self.connected_list[display_index], 'PLANE_CTL_1', 'PLANE_COLOR_CTL_1',
                        self.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0]))

                    ##
                    # Check plane CSC and pixel format status
                    if plane_csc == "disabled" or format_verify is False:
                        self.fail()

                time.sleep(5)
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 2, 2)

                ##
                # Disable the driver
                display_essential.disable_driver()

                ##
                # Close the media player
                close_media_player()

                ##
                # Enable the driver
                display_essential.enable_driver()

                ##
                # Opens media app and plays it in windowed mode
                self.play_media(False)

                ##
                # Play the video in snapmode
                snap_left()
                time.sleep(5)

                ##
                # Verify the registers
                plane_csc, plane_gamma, format_verify = verify_mpo_color_coexistence(
                    self.connected_list[display_index], 'PLANE_CTL_1', 'PLANE_COLOR_CTL_1',
                    self.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0]))

                ##
                # Check plane CSC and pixel format status
                if plane_csc == "disabled" or format_verify is False:
                    self.fail()

                ##
                # Set the default hue value
                hue_sat.hueSettings.currentValue = 0
                hue_sat.saturationSettings.currentValue = 0
                result = cui_sdk.set_hue_sat_info(hue_sat)
                if not result:
                    logging.error(
                        f"SDK call failed: set_hue_sat_info() for device_id {self.connected_list[display_index]}")
                    self.fail()

                ##
                # Close the media player
                close_media_player()

            else:
                logging.info("Failed to apply configuration")

        ##
        # Enable xvYCC feature
        if registry_access.write(args=reg_args, reg_name="XVYCCFeatureEnable",
                                 reg_type=registry_access.RegDataType.DWORD, reg_value=1) is False:
            logging.error("Registry key add to enable XVYCC feature failed")
            self.fail()
        status, reboot_required = display_essential.restart_gfx_driver()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
