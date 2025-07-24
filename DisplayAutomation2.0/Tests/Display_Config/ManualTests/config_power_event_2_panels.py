########################################################################################################################
# @file         config_power_event_2_panels.py
# @brief        This test aims at testing Extended display configuration with power event for 2 Displays
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3419874/
# @author       Chandrakanth Pabolu
########################################################################################################################
import logging
import unittest

from Libs.Core import enum, reboot_helper
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from Tests.Display_Config.ManualTests.config_power_event_1_panel import ConfigWithPowereventSinglepanel


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class ConfigWithPowerEventMultiplePanels(ConfigWithPowereventSinglepanel):

    ##
    # @brief This step confirms from user if booted with all displays correctly.
    # @return None
    def test_1_step(self):
        super().test_1_step()

    ##
    # @brief This step sets Extended display configuration with connected displays.
    # @return None
    def test_2_step(self):
        alert.info("Scenario: Applying extended display configuration with connected displays.")
        enum_port_list = []
        logging.info("Step2: Applying Extended Display Configuration.")
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count == 0:
            self.fail("FAIL: Enumerated displays is 0")
        for i in range(0, enumerated_display.Count):
            enum_port_list.append(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[i].ConnectorNPortType).name)
        status = self.__class__.display_config.set_display_configuration_ex(enum.EXTENDED, enum_port_list)
        if not status:
            self.fail("Applying Extended mode failed.")

        user_msg = "[Expectation]:Make sure Extended configuration applied successfully. \n " \
                   "Ensure No Visual artifacts/ corruption/ TDR/ BSOD should occur.\n" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        self.__class__.initial_config = self.__class__.display_config.get_current_display_configuration()

    ##
    # @brief This step invokes power event CS/S3
    # @return None
    def test_3_step(self):
        super().test_3_step()

    ##
    # @brief This step invokes power event S4
    # @return None
    def test_4_step(self):
        super().test_4_step()

    ##
    # @brief This step invokes Monitor Turn off from panel and from OS settings
    # @return None
    def test_5_step(self):
        super().test_5_step()

        self.turn_off_monitors_os_page()

        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step invokes power event S5
    # @return None
    def test_6_step(self):
        super().test_6_step()

    ##
    # @brief This function gets executed after reboot. Unplug Display
    # @return None
    def test_7_step(self):
        logging.info("Successfully resumed from power event S5.")
        data = reboot_helper._get_reboot_data()
        self.__class__.initial_config = data['initial_config']

        self.verify_config(self.__class__.initial_config)

        # Unplug Display1
        enumerated_displays = self.__class__.display_config.get_enumerated_display_info()
        displays_before_unplug = enumerated_displays.Count
        user_msg = "Hot Unplug display1." \
                   "\n[CONFIRM]:Enter yes if Display is Unplugged, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Hot unplugged display1")

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        enumerated_displays = self.__class__.display_config.get_enumerated_display_info()
        displays_after_unplug = enumerated_displays.Count

        if displays_after_unplug >= displays_before_unplug:
            self.fail("After unplug of external panel, still number of enumerated displays are same as before")

        self.__class__.initial_config = self.__class__.display_config.get_current_display_configuration()

    ##
    # @brief This step invokes power event CS/S3
    # @return None
    def test_8_step(self):
        self.test_3_step()

    ##
    # @brief This step invokes power event S4
    # @return None
    def test_9_step(self):
        self.test_4_step()

    ##
    # @brief This step invokes Monitor Turn off from panel and from OS settings
    # @return None
    def test_10_step(self):
        self.test_5_step()

    ##
    # @brief This step invokes power event S5
    # @return None
    def test_11_step(self):
        data = {'initial_config': self.__class__.initial_config}
        alert.info("Performing power event S5. Once system boots back to Desktop, rerun the test with same "
                   "commandline to continue execution")
        logging.info("Step11: Power event S5")
        if reboot_helper.reboot(self, 'test_12_step', data=data) is False:
            self.fail("Failed to reboot the system")

        ##
        # @brief This function gets executed after reboot.
        # @return None

    def test_12_step(self):
        logging.info("Successfully resumed from power event S5.")
        data = reboot_helper._get_reboot_data()
        self.__class__.initial_config = data['initial_config']

        self.verify_config(self.__class__.initial_config)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('ConfigWithPowerEventMultiplePanels'))
    TestEnvironment.cleanup(outcome)
