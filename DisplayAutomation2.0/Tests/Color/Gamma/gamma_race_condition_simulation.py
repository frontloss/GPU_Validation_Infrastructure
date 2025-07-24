##############################################################################################
# @file             gamma_race_condition_simulation.py
# @addtogroup       Test_Color
# @section          gamma_race_condition_simulation
# @ref              gamma_race_condition_simulation.py \n
# @remarks          This is a custom script which simulates the race condition of gamma
#                   by using CUI Brighntess slider and OS Brightness slider
# CommandLine:       python gamma_race_condition_simulation.py -edp_a
# @author           Smitha B
###############################################################################################
import logging
import os
import sys
import time
import unittest
from multiprocessing import Process

from Libs.Core import cmd_parser, display_utility, enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import cui_sdk_wrapper as cui_sdk
from Tests.Color import color_common_utility as color_utility


##
# @brief Function to set CUI Brightness slider with levels
# @param[in] - VOID



def set_cui_brightness_with_default_contrast(device_id, default_contrast):
    brightness_values = [-60, -40, -20, 0, 20, 40, 60, 80, 100]
    for index in range(0, len(brightness_values)):
        set_desktop_gamma = cui_sdk.DesktopGammaArgs(device_id=device_id, gamma=4,
                                                     brightness=brightness_values[index], contrast=default_contrast)
        sdk_status = cui_sdk.set_desktop_gamma_color(desktop_gamma_args=set_desktop_gamma)
        if not sdk_status:
            logging.error(f"SDK call failed: set_desktop_gamma_color() for device_id {device_id}")
            assert False, f"SDK call failed: set_desktop_gamma_color() for device_id {device_id}"
        else:
            get_desktop_gamma = cui_sdk.DesktopGammaArgs(device_id=device_id)
            sdk_status, get_desktop_gamma = cui_sdk.get_desktop_gamma_color(desktop_gamma_args=get_desktop_gamma)
            if not sdk_status:
                logging.error(f"SDK call failed: get_desktop_gamma_color() for device_id {device_id}")
                assert False, f"SDK call failed: set_desktop_gamma_color() for device_id {device_id}"
            else:
                if set_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] == get_desktop_gamma.gammaValues[
                    cui_sdk.RED_GAMMA] and set_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] == \
                        get_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] and set_desktop_gamma.gammaValues[
                    cui_sdk.RED_GAMMA] == get_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA]:
                    logging.info(f"Set Default Brightness and Contrast Successfully.")
                    status = True
                else:
                    logging.error("Failed to set CUI brightness")
                    color_utility.gdhm_report_app_color(title="[Color][gamma_race_condition_simulation]Failed to set default brightness and contrast values")
                    unittest.TestCase().fail("Failed to set CUI brightness")
        logging.info("CUI brightness setted Successfully")
        time.sleep(2)


##
# @brief Function invokes the SetMonitorBrightness app which moves the OS Brightness slider continuously from Min
# to Max and vice-versa in a loop
# @param[in] - VOID
def set_os_brightness():
    executable = 'SetMonitorBrightness.exe'
    commandline = executable + ' --loop'
    currentdir = os.getcwd()
    os.chdir(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'HDR'))
    os.system(commandline)
    os.chdir(currentdir)
    logging.info("OS_brightness setted Successfully")


class GammaRaceConditionSimulation(unittest.TestCase):
    connected_list = []
    device_id = 0
    default_brightness = 0
    default_contrast = 0
    config = DisplayConfiguration()

    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        for cmd_line_key, cmd_line_value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(cmd_line_key) is not None:
                if cmd_line_value['connector_port'] is not None:
                    self.connected_list.insert(cmd_line_value['index'], cmd_line_value['connector_port'])

        ##
        # Verify and plug the display
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail("Minimum 1 display is required to run the test")

        else:
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

    def get_default_brightness_contrast_values(self):
        default_brightness_contrast_values = cui_sdk.DesktopGammaArgs(device_id=self.device_id)
        sdk_status, get_brightness_contrast = cui_sdk.get_desktop_gamma_color(
            desktop_gamma_args=default_brightness_contrast_values)
        if not sdk_status:
            logging.info(f"SDK call failed: get_desktop_gamma_color() for device_id {self.device_id}")
            self.fail()
        else:
            if get_brightness_contrast.gammaValues[cui_sdk.RED_BRIGHTNESS] == \
                    default_brightness_contrast_values.gammaValues[cui_sdk.RED_BRIGHTNESS] and \
                    get_brightness_contrast.gammaValues[cui_sdk.BLUE_BRIGHTNESS] == \
                    default_brightness_contrast_values.gammaValues[cui_sdk.BLUE_BRIGHTNESS] and \
                    get_brightness_contrast.gammaValues[cui_sdk.GREEN_BRIGHTNESS] == \
                    default_brightness_contrast_values.gammaValues[cui_sdk.GREEN_BRIGHTNESS] and \
                    get_brightness_contrast.gammaValues[cui_sdk.RED_CONTRAST] == \
                    default_brightness_contrast_values.gammaValues[cui_sdk.RED_CONTRAST] and \
                    get_brightness_contrast.gammaValues[cui_sdk.GREEN_CONTRAST] == \
                    default_brightness_contrast_values.gammaValues[cui_sdk.GREEN_CONTRAST] and \
                    get_brightness_contrast.gammaValues[cui_sdk.BLUE_CONTRAST] == \
                    default_brightness_contrast_values.gammaValues[cui_sdk.BLUE_CONTRAST]:
                return default_brightness_contrast_values.gammaValues[cui_sdk.RED_BRIGHTNESS], \
                       default_brightness_contrast_values.gammaValues[cui_sdk.RED_CONTRAST]
            else:
                logging.error("Failed to get default brightness and contrast values")
                color_utility.gdhm_report_app_color(title="[Color][gamma_race_condition_simulation]Failed to get default brightness and contrast values")
                self.fail("Failed to get default brightness and contrast values")

    def runTest(self):
        ##
        # Apply Single Display Configuration on eDP
        topology = enum.SINGLE
        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info("Successfully applied Single Display configuration on %s" % self.connected_list)

            self.device_id = color_utility.get_device_id(self.connected_list[0])
            self.default_brightness, self.default_contrast = self.get_default_brightness_contrast_values()
            logging.info("Successfully get the default value for brightness and contrast")
            ##
            # Invoking Multiprocessing to set the OS Brightness and CUI Brightness sliders simultaneously
            cui_process = Process(
                target=set_cui_brightness_with_default_contrast(self.device_id, self.default_contrast))
            cui_process.start()
            set_brightness_process = Process(target=set_os_brightness())
            set_brightness_process.start()
            cui_process.join()
            set_brightness_process.join()
            ##
            # Restore the default brightness and contrast value
            set_desktop_gamma = cui_sdk.DesktopGammaArgs(device_id=self.device_id, gamma=4,
                                                         brightness=self.default_brightness,
                                                         contrast=self.default_contrast)

            sdk_status = cui_sdk.set_desktop_gamma_color(desktop_gamma_args=set_desktop_gamma)
            if not sdk_status:
                logging.error(f"SDK call failed: set_desktop_gamma_color() for device_id {self.device_id}")
                self.fail()
            else:
                get_desktop_gamma = cui_sdk.DesktopGammaArgs(device_id=self.device_id)
                sdk_status, get_desktop_gamma = cui_sdk.get_desktop_gamma_color(desktop_gamma_args=get_desktop_gamma)
                if not sdk_status:
                    logging.error(f"SDK call failed: get_desktop_gamma_color() for device_id {self.device_id}")
                    self.fail()
                else:
                    if set_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] == get_desktop_gamma.gammaValues[
                        cui_sdk.RED_GAMMA] and set_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] == \
                            get_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA] and set_desktop_gamma.gammaValues[
                        cui_sdk.RED_GAMMA] == get_desktop_gamma.gammaValues[cui_sdk.RED_GAMMA]:
                        logging.info(f"Set Default Brightness and Contrast Successfully.")
                    else:
                        logging.error("Failed to set default brightness and contrast")
                        self.fail("Failed to set default brightness and contrast")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
