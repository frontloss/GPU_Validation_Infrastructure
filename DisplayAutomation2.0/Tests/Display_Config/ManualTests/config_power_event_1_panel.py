########################################################################################################################
# @file         config_power_event_1_panel.py
# @brief        This test aims at testing Single display configuration with power event for 1 Display
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3419873/
# @author       Chandrakanth Pabolu
########################################################################################################################
import logging
import time
import unittest

from Libs.Core import enum, display_power, reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from Tests.Display_Config.ManualTests.config_power_event_base import ConfigWithPowereventBase


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class ConfigWithPowereventSinglepanel(ConfigWithPowereventBase):
    display_pwr = display_power.DisplayPower()
    display_config = DisplayConfiguration()
    initial_config = None

    ##
    # @brief This step confirms from user if booted with all displays correctly.
    # @return None
    def test_1_step(self):
        user_msg = "[Expectation]:Ensure the system is booted with all planned panels.\n" \
                   "[CONFIRM]:Enter Yes if expectation met, else No."
        result = alert.confirm(user_msg)
        if not result:
            self.fail("Test is not started with planned panel. Rerun the test with planned panel.")
        else:
            logging.info("Test started with planned panel")

    ##
    # @brief This step sets single display and applies native resolution
    # @return None
    def test_2_step(self):
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        display1 = CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[0].ConnectorNPortType).name
        display_and_adapterinfo = enumerated_display.ConnectedDisplays[0].DisplayAndAdapterInfo
        if enumerated_display.Count > 1:
            self.fail("More than 1 display connected.")

        alert.info(f"Scenario:Setting Single - {display1}. Look for any corruption while applying config")
        logging.info(f"Step2: Setting Single - {display1}")

        status = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE, [display1])
        if not status:
            self.fail(f"Applying SD on port {display1} failed.")

        user_msg = "[Expectation]: No corruption should be seen. \n" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("No corruption was seen when single display Display1 applied")

        self.__class__.initial_config = self.__class__.display_config.get_current_display_configuration()

        if not self.apply_native_mode(display_and_adapterinfo):
            self.fail(f"Applying Native mode on port {display1} failed.")

        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step invokes power event CS/S3
    # @return None
    def test_3_step(self):
        power_state = display_power.PowerEvent.S3
        is_cs_supported = self.__class__.display_pwr.is_power_state_supported(display_power.PowerEvent.CS)

        if is_cs_supported:
            power_state = display_power.PowerEvent.CS

        alert.info(f"Scenario: Performing power event {power_state.name}")
        logging.info(f"Performing Power event {power_state.name}")
        time.sleep(2)

        if self.display_pwr.invoke_power_event(power_state, 30) is False:
            self.fail(f'Failed to invoke power event {power_state.name}')

        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step invokes power event S4
    # @return None
    def test_4_step(self):
        alert.info("Scenario: Performing power event S4.")
        logging.info("Step4: Power event S4")
        self.display_pwr.invoke_power_event(display_power.PowerEvent.S4, 30)

        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step invokes Monitor Turn off from panel
    # @return None
    def test_5_step(self):
        alert.info("Note: Step to be performed by user manually.\n"
                   "Scenario: Turn off monitor from Panel and Turn on after 30sec.")
        logging.info("User Turns off monitor from monitor Off button on panel and Turns it on after 30 sec.")
        time.sleep(35)
        logging.info("Waiting for user to turnon monitor")
        alert.info("Click Ok to resume the test.")

        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step invokes power event S5
    # @return None
    def test_6_step(self):
        data = {'initial_config': self.__class__.initial_config}
        alert.info("Scenario: Performing power event S5. Once system boots back to Desktop, rerun the test with same "
                   "commandline to continue execution.")
        logging.info("Step6: Power event S5")
        if reboot_helper.reboot(self, 'test_7_step', data=data) is False:
            self.fail("Failed to reboot the system")

        ##
        # @brief This function gets executed after reboot.
        # @return None

    def test_7_step(self):
        logging.info("Successfully resumed from power event S5.")
        data = reboot_helper._get_reboot_data()
        self.__class__.initial_config = data['initial_config']

        self.verify_config(self.__class__.initial_config)

        self.turn_off_monitors_os_page()
        self.verify_config(self.__class__.initial_config)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('ConfigWithPowereventSinglepanel'))
    TestEnvironment.cleanup(outcome)
