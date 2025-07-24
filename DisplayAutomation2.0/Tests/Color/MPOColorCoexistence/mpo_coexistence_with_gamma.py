##############################################################################################
# \file
# \addtogroup       Test_Color
# \section          mpo_coexistence_with_gamma
# \ref              mpo_coexistence_with_gamma.py \n
# \remarks          This script performs color functionality such as applying gamma
#                   while the video app is played and verifies for the plane gamma status.
# CommandLine:      python mpo_coexistence_with_gamma.py -edp_a
# \author           Anjali Shetty
###############################################################################################
from random import randint

from Libs.Core import enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.winkb_helper import snap_right
from Tests.Color import color_common_utility as color_utility
from Tests.Color.MPOColorCoexistence.mpo_coexistence_base import *


class MPOCoexistenceWithGamma(MPOCoexistenceBase):
    def runTest(self):

        topology = enum.SINGLE
        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info("Successfully applied the configuration")

                ##
                # Get the device id
                device_id = color_utility.get_device_id(self.connected_list[display_index])

                press('WIN+M')

                ##
                # Opens media app and plays it in windowed mode
                self.play_media(False)

                ##
                # To enable 'Repeat' option in the Video App
                press("CTRL+T")

                ##
                # Play the video in snapmode
                snap_right()
                time.sleep(5)

                ##
                # Verify the registers
                plane_csc, plane_gamma, format_verify = verify_mpo_color_coexistence(
                    self.connected_list[display_index], 'PLANE_CTL_1', 'PLANE_COLOR_CTL_1',
                    self.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0]))

                if plane_gamma == "enabled" or format_verify is False:
                    self.fail()

                gamma = cui_sdk.DesktopGammaArgs(device_id=device_id)
                sdk_status, gamma = cui_sdk.get_desktop_gamma_color(desktop_gamma_args=gamma)
                if not sdk_status:
                    logging.error(f"SDK call failed: get_desktop_gamma_color() for device_id {device_id}")
                    self.fail()
                # Get_default = 1
                default_val = gamma.gammaValues[cui_sdk.RED_GAMMA]
                logging.info("default value: %s" % default_val)
                color_val = 0
                for i in range(0, 5):
                    color_val = randint(4, 50)

                    ##
                    # Set the gamma value
                    set_desktop_gamma = cui_sdk.DesktopGammaArgs(device_id=device_id, gamma=color_val)
                    sdk_status = cui_sdk.set_desktop_gamma_color(desktop_gamma_args=set_desktop_gamma)
                    if not sdk_status:
                        logging.error(f"SDK call failed: set_desktop_gamma_color() for device_id {device_id}")
                        self.fail()
                    else:
                        gamma_args2 = cui_sdk.DesktopGammaArgs(device_id=device_id)
                        sdk_status, gamma_args2 = cui_sdk.get_desktop_gamma_color(desktop_gamma_args=gamma_args2)
                        if not sdk_status:
                            logging.error(f"SDK call failed: get_desktop_gamma_color() for device_id {device_id}")
                            self.fail()
                        else:
                            if set_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] == gamma_args2.gammaValues[
                                cui_sdk.RED_GAMMA] and set_desktop_gamma.gammaValues[cui_sdk.GREEN_GAMMA] == \
                                    gamma_args2.gammaValues[cui_sdk.GREEN_GAMMA] and set_desktop_gamma.gammaValues[
                                cui_sdk.BLUE_GAMMA] == gamma_args2.gammaValues[cui_sdk.BLUE_GAMMA]:
                                ##
                                # Verify the registers
                                plane_csc, plane_gamma, format_verify = verify_mpo_color_coexistence(
                                    self.connected_list[display_index], 'PLANE_CTL_1', 'PLANE_COLOR_CTL_1',
                                    self.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0]))

                                if format_verify is False:
                                    self.fail()
                            else:
                                logging.error("Failed to set gamma value")
                                self.fail()

                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 2, 2)

                brightness_val = randint(-60, 100)
                contrast_val = randint(40, 100)

                ##
                # Set the brightness and contrast value
                set_desktop_gamma = cui_sdk.DesktopGammaArgs(device_id=device_id, gamma=color_val,
                                                               brightness=brightness_val, contrast=contrast_val)
                sdk_status = cui_sdk.set_desktop_gamma_color(desktop_gamma_args=set_desktop_gamma)
                if not sdk_status:
                    logging.error(f"SDK call failed: set_desktop_gamma_color() for device_id {device_id}")
                    self.fail()
                else:
                    desktop_gamma_args2 = cui_sdk.DesktopGammaArgs(device_id=device_id)
                    sdk_status, desktop_gamma_args2 = cui_sdk.get_desktop_gamma_color(
                        desktop_gamma_args=desktop_gamma_args2)
                    if not sdk_status:
                        logging.error(f"SDK call failed: get_desktop_gamma_color() for device_id {device_id}")
                        self.fail()
                    else:
                        if set_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] == desktop_gamma_args2.gammaValues[
                            cui_sdk.RED_GAMMA] and set_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] == \
                                desktop_gamma_args2.gammaValues[cui_sdk.RED_GAMMA] and set_desktop_gamma.gammaValues[
                            cui_sdk.RED_GAMMA] == desktop_gamma_args2.gammaValues[cui_sdk.RED_GAMMA]:
                            logging.info(f"Set Brightness and Contrast Successfully.")
                        else:
                            logging.error("Failed to set brightness and contrast")
                            self.fail()

                ##
                # Close the media player
                close_media_player()

                ##
                # Set the default gamma, brightness and contrast value
                set_desktop_gamma = cui_sdk.DesktopGammaArgs(device_id=device_id, gamma=default_val,
                                                               brightness=0, contrast=50)
                sdk_status = cui_sdk.set_desktop_gamma_color(desktop_gamma_args=set_desktop_gamma)
                if not sdk_status:
                    logging.error(f"SDK call failed: set_desktop_gamma_color() for device_id {device_id}")
                    self.fail()
                else:
                    desktop_gamma_args2 = cui_sdk.DesktopGammaArgs(device_id=device_id)
                    sdk_status, desktop_gamma_args2 = cui_sdk.get_desktop_gamma_color(
                        desktop_gamma_args=desktop_gamma_args2)
                    if not sdk_status:
                        logging.error(f"SDK call failed: get_desktop_gamma_color() for device_id {device_id}")
                        self.fail()
                    else:
                        if set_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] == desktop_gamma_args2.gammaValues[
                            cui_sdk.RED_GAMMA] and set_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] == \
                                desktop_gamma_args2.gammaValues[cui_sdk.RED_GAMMA] and set_desktop_gamma.gammaValues[
                            cui_sdk.RED_GAMMA] == desktop_gamma_args2.gammaValues[cui_sdk.RED_GAMMA]:
                            logging.info(f"Set Default Brightness and Contrast Successfully.")
                        else:
                            logging.error("Failed to set default brightness and contrast")
                            self.fail()
            else:
                logging.info("Failed to apply display configuration")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
