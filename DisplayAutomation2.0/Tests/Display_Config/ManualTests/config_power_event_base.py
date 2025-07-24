########################################################################################################################
# @file         config_power_event_base.py
# @brief        Has base functions to be used by config and power event semi-auto tests
# @author       Chandrakanth Pabolu
########################################################################################################################
import logging
import time
import unittest

from Libs.Core import enum, reboot_helper
from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from Tests.PowerCons.Modules import desktop_controls


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class ConfigWithPowereventBase(unittest.TestCase):
    # display_pwr = display_power.DisplayPower()
    # display_config = DisplayConfiguration()
    # initial_config = None

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        pass

    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass

    ##
    # @brief This step invokes Monitor Turn off from panel
    # @return None
    def turn_off_monitors_os_page(self):
        # if self.__class__.is_cs_supported:
        #     logging.info(
        #        "Monitor turnoff does not work in connected standby enabled system,hence skipping monitor turnoff_on.")

        alert.info("Scenario: Setting Monitor turn off from system with 1min timeout.")
        logging.info("Setting display time-out to 1 minute")
        if desktop_controls.set_time_out(desktop_controls.TimeOut.TIME_OUT_DISPLAY, 1) is False:
            self.fail("Failed to set display time-out to 1 minute (Test Issue)")
        logging.info("\tSet display time-out to 1 minute successful.")

        alert.info("Note: Step to be done by user manually.\n"
                   "Once the monitor turns off, wait for 10sec and Resume from MTO by moving mouse or keyboard press.")

        logging.info("Waiting for 1min..")
        time.sleep(60)

        logging.info("Waiting for user to turnon monitor")
        user_msg = "[Expectation]: Monitor should have turned off and turned back on.\n " \
                   "Ensure No Visual artifacts/ corruption/ TDR/ BSOD should occur.\n" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Monitor turned off and turned back on without any issues.")

    ##
    # @brief Helper function to verify display configuration
    # @return None
    def verify_config(self, expected_config):
        if expected_config is None:
            alert.info("FAIL: expected config is None which is not expected.")
            self.fail("Passed config is None. Failing...")
        current_config = self.__class__.display_config.get_current_display_configuration()
        enumerated_displays = self.__class__.display_config.get_enumerated_display_info()
        if expected_config.equals(current_config) is False:
            logging.error(f"Display configuration doesn't match. expected: "
                          f"{expected_config.to_string(enumerated_displays)} "
                          f"observed: {current_config.to_string(enumerated_displays)}")
            self.fail(f"Display configuration doesn't match.")
        else:
            logging.info(f"Display configuration matches: {current_config.to_string(enumerated_displays)}")

        user_msg = "[Expectation]:Make sure that display comes in previous configuration. \n " \
                   "Ensure No Visual artifacts/ corruption/ TDR/ BSOD should occur.\n" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

    def apply_native_mode(self, display_and_adapterinfo: DisplayAndAdapterInfo):
        status = False

        mode = self.__class__.display_config.get_current_mode(display_and_adapterinfo)
        if mode is None:
            logging.error(f"Failed to get current mode for {display_and_adapterinfo.TargetID}")
            return False

        native_mode = self.__class__.display_config.get_native_mode(display_and_adapterinfo.TargetID)
        if native_mode is None:
            logging.error(f"Failed to get native mode for {display_and_adapterinfo.TargetID}")
            return False

        logging.info("Applying native mode")
        mode.HzRes, mode.VtRes = native_mode.hActive, native_mode.vActive
        mode.refreshRate, mode.scaling = native_mode.refreshRate, enum.MDS

        result = self.__class__.display_config.set_display_mode([mode])

        if result:
            current_mode = self.__class__.display_config.get_current_mode(display_and_adapterinfo)
            if (current_mode.HzRes == mode.HzRes and current_mode.VtRes == mode.VtRes and
                    current_mode.refreshRate == mode.refreshRate and current_mode.scaling == mode.scaling):
                logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3}".format(
                    current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, current_mode.scaling))
                status = True
        return status


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('ConfigWithPowereventSinglepanel'))
    TestEnvironment.cleanup(outcome)
