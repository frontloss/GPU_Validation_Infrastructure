########################################################################################################################
# @file         display_detect_basic_power_event.py
# @brief        This test aims to check display detection with basic power events.
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3429642/
# @author       Chandrakanth Pabolu
########################################################################################################################
import logging
import time
import unittest

from Libs.Core import enum, display_power, reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE, DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from Tests.Display_Config.ManualTests.config_power_event_base import ConfigWithPowereventBase


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class DisplayDetectBasicPowerEvent(ConfigWithPowereventBase):
    display_pwr = display_power.DisplayPower()
    display_config = DisplayConfiguration()
    initial_config = None

    ##
    # @brief This step confirms from user if booted with all displays correctly.
    # @return None
    def test_1_step(self):
        user_msg = "[Expectation]:Ensure the system is booted with all planned panels.\n" \
                   "Generic expectation: No corruption/blankout/flicker/BSOD should be seen on all the displays.\n" \
                   "[CONFIRM]:Enter Yes if expectation met, else enter No"
        result = alert.confirm(user_msg)
        if not result:
            self.fail("Test is not started with planned panel. Rerun the test with planned panel.")
        else:
            logging.info("Test started with planned panel")

    ##
    # @brief This step sets single/Extended display config on displays planned and ask user to apply max resolution.
    # @return None
    def test_2_step(self):
        config_to_be_applied = enum.SINGLE
        enum_port_list = []
        enumerated_displays = self.__class__.display_config.get_enumerated_display_info()
        for i in range(0, enumerated_displays.Count):
            enum_port_list.append(str(CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[i].ConnectorNPortType)))
        if enumerated_displays.Count > 1:
            config_to_be_applied = enum.EXTENDED

        alert.info(f"Applying {DisplayConfigTopology(config_to_be_applied).name} display configuration.")
        logging.info(f"Step2: Applying {DisplayConfigTopology(config_to_be_applied).name} display configuration.")
        status = self.__class__.display_config.set_display_configuration_ex(config_to_be_applied, enum_port_list)
        if not status:
            self.fail(f"Applying {DisplayConfigTopology(config_to_be_applied).name} display configuration failed.")

        user_msg = "[Expectation]:Make sure Display configuration applied successfully. \n " \
                   "Ensure No Visual artifacts/ corruption/ TDR/ BSOD should occur.\n" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        self.__class__.initial_config = self.__class__.display_config.get_current_display_configuration()

        # ToDo: Apply max resolution on all the panels in this configuration
        alert.info("Note: Step to be performed by user manually.\n"
                   "Scenario: Apply max resolutions on all the panels and verify from below wiki.\n"
                   "https://wiki.ith.intel.com/pages/viewpage.action?pageId=2642702387#TestExpectationsResolutionv/sConfigInformation-4.Display_Detect_Basic_with_Power_Event")
        time.sleep(10)
        logging.info("User applies max resolutions on all the panels and verify from below wiki.\n"
                   "https://wiki.ith.intel.com/pages/viewpage.action?pageId=2642702387#TestExpectationsResolutionv/sConfigInformation-4.Display_Detect_Basic_with_Power_Event")
        user_msg = "[Expectation]:Make sure Max resolutions applied as per wiki.\n " \
                   "https://wiki.ith.intel.com/pages/viewpage.action?pageId=2642702387#TestExpectationsResolutionv/sConfigInformation-4.Display_Detect_Basic_with_Power_Event" \
                   "\nEnsure No Visual artifacts/ corruption/ TDR/ BSOD should occur.\n" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

    ##
    # @brief This step invokes power event CS/S3 and verifies config
    # @return None
    def test_3_step(self):
        power_state = display_power.PowerEvent.S3
        is_cs_supported = self.__class__.display_pwr.is_power_state_supported(display_power.PowerEvent.CS)

        if is_cs_supported:
            power_state = display_power.PowerEvent.CS

        alert.info(f"Performing power event {power_state.name}")
        logging.info(f"Performing Power event {power_state.name}")
        time.sleep(2)

        if self.display_pwr.invoke_power_event(power_state, 30) is False:
            self.fail(f'Failed to invoke power event {power_state.name}')

        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step invokes power event S4 and verifies config
    # @return None
    def test_4_step(self):
        alert.info("Performing power event S4.")
        logging.info("Step4: Power event S4")
        self.display_pwr.invoke_power_event(display_power.PowerEvent.S4, 30)

        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step invokes power event S5 and verifies config
    # @return None
    def test_5_step(self):
        data = {'initial_config': self.__class__.initial_config}
        alert.info("Performing power event S5.\nOnce system boots back to Desktop, rerun the test again to continue.")
        logging.info("Step5: Power event S5")
        if reboot_helper.reboot(self, 'test_6_step', data=data) is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief This step invokes Monitor Turn off from panel and OS page and verifies config
    # @return None
    def test_6_step(self):
        logging.info("Successfully resumed from power event S5.")
        data = reboot_helper._get_reboot_data()
        self.__class__.initial_config = data['initial_config']
        self.verify_config(self.__class__.initial_config)

        self.turn_off_monitors_os_page()
        self.verify_config(self.__class__.initial_config)

        alert.info("Note: Step to be performed by user manually.\n"
                   "Scenario: Turn off monitor from Panel and Turn on after 30sec.")
        logging.info("User Turns off monitor from monitor Off button on panel and Turns it on after 30 sec.")
        time.sleep(35)
        logging.info("Waiting for user for Monitor Turn on.")
        alert.info("Ensure the monitor is turned back ON. Click Ok to resume the test.")

        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step performs unplug dock/dongle in power event CS/S3 and plug back post resume
    # @return None
    def test_7_step(self):
        power_state = display_power.PowerEvent.S3
        is_cs_supported = self.__class__.display_pwr.is_power_state_supported(display_power.PowerEvent.CS)

        if is_cs_supported:
            power_state = display_power.PowerEvent.CS

        alert.info(f"Step7:\n"
                   f"Note: Plug/unplug to be performed by user manually during power events.\n"
                   f"Scenario: Unplug the dock/displays when system entered to {power_state.name}.\n"
                   f"Plug dock/displays back post resume.\n"
                   f"Expectation: System shouldn't resume as dock/displays unplugged.")
        logging.info(f"Unplug the dock/displays in {power_state.name}. Plug it back post resume")
        time.sleep(2)

        if self.display_pwr.invoke_power_event(power_state, 30) is False:
            self.fail(f'Failed to invoke power event {power_state.name}')

        alert.info("Plug dock/displays if not yet plugged. Post that,Click Ok to resume the test.")
        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step performs unplug dock/dongle in power event S4 and plug back post resume
    # @return None
    def test_8_step(self):
        alert.info(f"Step8:\n"
                   f"Note: Plug/unplug to be performed by user manually during power events.\n"
                   f"Scenario: Unplug the dock/displays when system entered to S4.\n Plug it back post resume.\n"
                   f"Expectation: System shouldn't resume as dock/displays unplugged.")
        time.sleep(2)

        logging.info("Step8: Unplug the dock/displays in S4.\n Plug it back post resume")
        self.display_pwr.invoke_power_event(display_power.PowerEvent.S4, 30)
        alert.info("Plug dock/displays if not yet plugged. Post that,Click Ok to resume the test.")
        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step invokes Unplug in Monitor Turn off and plug post resume
    # @return None
    def test_9_step(self):
        alert.info(f"Step9:\n"
                   f"Note: Plug/unplug to be performed by user manually during Monitor Turnoff.\n"
                   f"Scenario: 1) Unplug the dock/displays once Monitors are Turned off.\n"
                   f"2) Resume from Monitor turnoff by moving Mouse or keyboard press.\n"
                   f"3) Plug back dock/displays post resume.\n"
                   f"Expectation: System shouldn't resume as dock/displays unplugged.")
        time.sleep(2)
        logging.info("Step9: Unplug dock/displays in OS MonitorTurnoff options with 1min. Plug it back post resume.")
        self.turn_off_monitors_os_page()
        alert.info("Plug dock/displays. Post that,Click Ok to resume the test.")
        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step performs unplug dock/displays and performs plug in power event CS/S3
    # @return None
    def test_10_step(self):
        power_state = display_power.PowerEvent.S3
        is_cs_supported = self.__class__.display_pwr.is_power_state_supported(display_power.PowerEvent.CS)

        if is_cs_supported:
            power_state = display_power.PowerEvent.CS

        alert.info(f"Step10:\n"
                   f"Note: Below all steps to be performed by user manually.\n"
                   f"Scenario:"
                   f"1) Unplug the dock/displays.\n"
                   f"2) Go to {power_state.name} and wait for 30 sec\n"
                   f"3) Plug the dock/displays back when system in {power_state.name}.\n"
                   f"4) Resume from Power state.\n"
                   f"Expectation: System shouldn't wake from {power_state.name} during plug.\n"
                   f"Dock/displays display should get detected post resume too.")

        logging.info(f"Step10: dock/displays will be unplugged. System goes to {power_state.name}."
                     f"Dock/displays will be plugged during low power state. System will be resumed.")
        time.sleep(5)

        alert.info("Click Ok to resume the test.")
        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step performs unplug dock/displays and performs plug in power event S4
    # @return None
    def test_11_step(self):
        alert.info(f"Step11:\n"
                   f"Note: Below all steps to be performed by user manually.\n"
                   f"Scenario:\n"
                   f"1) Unplug the dock/displays.\n"
                   f"2) Go to S4 and wait for 30 sec\n"
                   f"3) Plug the dock/displays back when system in S4.\n"
                   f"4) Resume from Power state.\n"
                   f"Expectation: System shouldn't wake from S4 during plug.\n"
                   f"Dock/displays display should get detected post resume too.")

        logging.info("Step11: Dock/displays will be unplugged. System goes to S4. "
                     "Dock/displays will be plugged during low power state. System will be resumed.")
        time.sleep(5)

        alert.info("Click Ok to resume the test.")
        self.verify_config(self.__class__.initial_config)

    ##
    # @brief This step performs unplug dock/displays and performs plug in MonitorTurnoff
    # @return None
    def test_12_step(self):
        alert.info(f"Step12:\n"
                   f"Note: Below steps to be done by user manually.\n"
                   f"Scenario:\n"
                   f"1) Unplug the dock/displays.\n"
                   f"2) Wait for 1min for monitors to be turned off(incase of eDP).\n"
                   f"3) Plug the dock/displays back .\n"
                   f"4) Resume from MonitorTurnoff by moving mouse or clicking keyboard.\n"
                   f"Expectation: Dock/displays should get detected post resume too.")

        alert.info(f"Unplug dock/displays during configuration of Monitor Turnoff.")
        self.turn_off_monitors_os_page()

        logging.info(
            "Step12: Dock/displays will be unplugged. MonitorTurnoff is set to 1min. "
            "Dock/displays will be plugged. System will be resumed from Low Powerstate.")
        time.sleep(5)
        alert.info("Click Ok to resume the test.")
        self.verify_config(self.__class__.initial_config)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DisplayDetectBasicPowerEvent'))
    TestEnvironment.cleanup(outcome)
