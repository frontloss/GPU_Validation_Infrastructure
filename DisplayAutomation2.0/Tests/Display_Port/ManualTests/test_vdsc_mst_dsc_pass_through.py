########################################################################################################################
# @file         test_vdsc_mst_dsc_pass_through.py
# @brief        Manual test to verify VDSC Passthrough scenarios.
#               This test uses static configuration, i.e. dock and all displays to be connected are
#               mentioned in Grid
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3420923/
#               Manual test name: test_vdsc_mst_dsc_pass_through
# @author       Chandrakanth Pabolu
########################################################################################################################
import logging
import os
import sys
import time
import unittest
from collections import OrderedDict

from Libs.Core import display_power, enum, cmd_parser, reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import DisplayPower
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from Libs.manual.modules import mode_xml_parser
from Tests.PowerCons.Modules import desktop_controls

XML_PATH = os.path.join(test_context.ROOT_FOLDER, "Tests\\Display_Port\\ManualTests\\config_xmls")


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class VdscMstDscPassthrough(unittest.TestCase):
    my_custom_tags = ['-xml']
    xml_file = None
    is_initial_display_connected = False
    # display_dictionary = {
    #     'Display1': {'panel': 'DELL 3219Q', 'Connector': 'Type-C', 'HActive': 1024, 'VActive': 768, 'RefreshRate': 60,
    #               'Scaling': 'MDS'},
    #     'Display2': {'panel': 'BENQ SW320', 'Connector': 'DP', 'HActive': 1920, 'VActive': 1080, 'RefreshRate': 60,
    #               'Scaling': 'MDS'}}
    display_dictionary = OrderedDict()
    display_to_targetID_map = {}
    display_pwr = DisplayPower()
    display_config = DisplayConfiguration()
    expected_config = None

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        VdscMstDscPassthrough.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, VdscMstDscPassthrough.my_custom_tags)

        if 'XML' not in VdscMstDscPassthrough.cmd_line_param.keys():
            alert.info("Aborting the test as xml file is not provided in command-line")
            self.fail("Aborting the test as xml file is not provided in command-line")
        VdscMstDscPassthrough.xml_file = VdscMstDscPassthrough.cmd_line_param['XML'][0]

    ##
    # @brief        This step boots the system if display is planned and connects the dock
    # @return       None
    def test_01_step(self):
        user_msg = ("[Expectation]:System should be booted with eDP if planned, else using VNC."
                    "No corruption/blankout/flicker/BSOD should be seen on all the displays."
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            self.fail("Test is not started with planned panel. Rerun the test with planned panel.")
        else:
            logging.info("Test started with planned panels")

    ##
    # @brief        This step plugs the planned dock to the system.
    # @return       None
    def test_02_step(self):
        alert.info("Note: Step to be done by user manually.\n"
                   "Scenario:Plug the planned Dock to the system.")
        user_msg = ("[Expectation]: No corruption/blankout/flicker/BSOD should be seen on all the displays.\n"
                    "[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Dock is plugged to the system. Corruption/blankout/flicker/BSOD was not seen.")

    ##
    # @brief        This step plugs displays to dock, applies extended config.
    # @return       None
    def test_03_step(self):
        alert.info("Step3: This step involves plugging planned displays to Dock and applies extended Config.")
        xml_file_path = os.path.join(XML_PATH, VdscMstDscPassthrough.xml_file)
        VdscMstDscPassthrough.display_dictionary = mode_xml_parser.parse_xml(xml_file_path)
        self.plug_displays_to_dock()
        self.verify_generic()

        VdscMstDscPassthrough.expected_config = VdscMstDscPassthrough.display_config.get_current_display_configuration()

    ##
    # @brief        This step applies maximum resolution for planned displays
    # @return       None
    def test_04_step(self):
        alert.info("Step3: This step involves applying max resolution to planned displays.")
        self.apply_max_resolution_to_displays()
        self.verify_generic()

    ##
    # @brief This step invokes power event CS/S3 and verifies config and display mode
    # @return None
    def test_05_step(self):
        power_state = display_power.PowerEvent.S3
        is_cs_supported = VdscMstDscPassthrough.display_pwr.is_power_state_supported(display_power.PowerEvent.CS)

        if is_cs_supported:
            power_state = display_power.PowerEvent.CS

        alert.info(f"Performing power event {power_state.name}")
        logging.info(f"Performing Power event {power_state.name}")
        time.sleep(2)

        if self.display_pwr.invoke_power_event(power_state, 30) is False:
            self.fail(f'Failed to invoke power event {power_state.name}')
        time.sleep(2)
        self.verify_config(VdscMstDscPassthrough.expected_config)
        self.verify_current_mode()
        self.verify_generic()

    ##
    # @brief This step invokes power event S4 and verifies config
    # @return None
    def test_4_step(self):
        alert.info("Performing power event S4.")
        logging.info("Step4: Power event S4")
        self.display_pwr.invoke_power_event(display_power.PowerEvent.S4, 30)

        self.verify_config(VdscMstDscPassthrough.expected_config)
        self.verify_current_mode()
        self.verify_generic()

    ##
    # @brief        This step reboots the system and verifies config and display mode.
    # @return       None
    def test_07_step(self):
        alert.info("Rebooting the system. Rerun same commandline once booted to Desktop to continue the test")
        logging.info("Rebooting the system")
        data = {'display_to_targetID_map': VdscMstDscPassthrough.display_to_targetID_map,
                'display_dictionary': VdscMstDscPassthrough.display_dictionary,
                'expected_config': VdscMstDscPassthrough.expected_config}
        if reboot_helper.reboot(self, 'test_08_step', data=data) is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This step verifies config and mode post S5. Also, performs MTO from OS page.
    # @return       None
    def test_08_step(self):
        data = reboot_helper._get_reboot_data()
        VdscMstDscPassthrough.display_dictionary = data['display_dictionary']
        VdscMstDscPassthrough.display_to_targetID_map = data['display_to_targetID_map']
        VdscMstDscPassthrough.expected_config = data['expected_config']

        alert.info(f"Successfully booted back to OS. Verifying Config and display mode.")
        self.verify_config(VdscMstDscPassthrough.expected_config)
        self.verify_current_mode()
        self.verify_generic()

        alert.info("Scenario: Setting Monitor turn off from system with 1min timeout.")
        logging.info("Setting display time-out to 1 minute")
        if desktop_controls.set_time_out(desktop_controls.TimeOut.TIME_OUT_DISPLAY, 1) is False:
            self.fail("Failed to set display time-out to 1 minute (Test Issue)")
        logging.info("\tSet display time-out to 1 minute successful.")

        alert.info("Note: Step to be done by user manually.\n"
                   "Once the monitor turns off, wait for 10sec and Resume from MTO by moving mouse or keyboard press.")

        logging.info("Waiting for 1min..")
        time.sleep(60)

        logging.info("Waiting for user to turnon monitor.")
        user_msg = "[Expectation]: Monitor should have turned off and turned back on.\n " \
                   "Ensure No Visual artifacts/ corruption/ TDR/ BSOD should occur.\n" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Monitor turned off and turned back on without any issues.")
        self.verify_config(VdscMstDscPassthrough.expected_config)
        self.verify_current_mode()

    ##
    # @brief        This step performs MTO from Panel and verifies Config and display mode.
    # @return       None
    def test_09_step(self):
        alert.info("Note: Step to be performed by user manually.\n"
                   "Scenario: Turn off monitor from Panel and Turn on after 30sec.")
        logging.info("User Turns off monitor from monitor Off button on panel and Turns it on after 30 sec.")
        time.sleep(35)
        logging.info("Waiting for user for Monitor Turn on.")
        alert.info("Ensure the monitor is turned back ON. Click Ok to resume the test.")

        self.verify_config(VdscMstDscPassthrough.expected_config)
        self.verify_current_mode()
        self.verify_generic()

    ##
    # @brief        To plug display to dock one by one, post plug apply extended mode between
    #               all the connected displays and then do modeset with desired mode for each display
    # @return       None
    def plug_displays_to_dock(self):
        display_adapter_info_list = []
        VdscMstDscPassthrough.display_to_targetID_map = {}
        enumerated_display = VdscMstDscPassthrough.display_config.get_enumerated_display_info()
        # Adding already connected display and adapter info to the list
        if enumerated_display.Count != 0:
            for i in range(0, enumerated_display.Count):
                display_adapter_info_list.append(
                    enumerated_display.ConnectedDisplays[i].DisplayAndAdapterInfo)
                tid = enumerated_display.ConnectedDisplays[i].DisplayAndAdapterInfo.TargetID
                port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[i].ConnectorNPortType))
                VdscMstDscPassthrough.display_to_targetID_map[port_type] = tid
                if port_type != "VIRTUALDISPLAY":
                    VdscMstDscPassthrough.is_initial_display_connected = True

        for key, value in VdscMstDscPassthrough.display_dictionary.items():
            updated_enum_port_list = []
            enumerated_display = VdscMstDscPassthrough.display_config.get_enumerated_display_info()
            if enumerated_display.Count != 0:
                for i in range(0, enumerated_display.Count):
                    port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[i].ConnectorNPortType))
                    if port_type == "VIRTUALDISPLAY":
                        enumerated_display.Count -= 1

            alert.info(f"Note: Step to be done by user manually."
                       f"\nPlug {value['panel']} panel on {value['Connector']} port.\n"
                       f"Plugged display should come up without any issues (corruption / flicker/ blankout.)")
            logging.info(f"User Plugs {value['panel']} panel on {value['Connector']} port.")
            time.sleep(5)
            user_msg = (
                f"Active displays should come up without corruption / flicker/ blankout and"
                f" audio endpoint should be loaded for the display which is connected."
                "\n[CONFIRM]:Enter yes if expectation met, else enter no")
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
            else:
                logging.info(f"Plug of {value['panel']} panel is successful")

            time.sleep(2)
            updated_enumerated_display = VdscMstDscPassthrough.display_config.get_enumerated_display_info()
            if updated_enumerated_display.Count > 0:
                if updated_enumerated_display.Count == 1:
                    port_type = str(CONNECTOR_PORT_TYPE
                                    (updated_enumerated_display.ConnectedDisplays[0].ConnectorNPortType))
                    if port_type == "VIRTUALDISPLAY":
                        self.fail("Same number of displays post plug")
                if updated_enumerated_display.Count != enumerated_display.Count + 1:
                    alert.info("Fail: same number of displays")
                    self.fail("Same number of displays post plug")

                for i in range(0, updated_enumerated_display.Count):
                    tid = updated_enumerated_display.ConnectedDisplays[i].DisplayAndAdapterInfo.TargetID
                    if tid not in VdscMstDscPassthrough.display_to_targetID_map.values():
                        VdscMstDscPassthrough.display_to_targetID_map[key] = tid
                    updated_enum_port_list.append(updated_enumerated_display.ConnectedDisplays[i].DisplayAndAdapterInfo)
            else:
                alert.info("Enumerated displays count is 0")
                self.fail("Enumerated displays count is 0")

            # To apply extended mode, we need minimum 2 displays.
            # checking this condition to skip modeset when only 1 display is connected.
            if updated_enumerated_display.Count >= 2:
                alert.info("Applying extended mode")
                logging.info("Applying extended mode")
                status = VdscMstDscPassthrough.display_config.set_display_configuration_ex(enum.EXTENDED,
                                                                                    updated_enum_port_list)
                if not status:
                    alert.info("Applying Extended mode failed")
                    self.fail("Applying Extended mode failed")
            else:
                alert.info("Only 1 display is present. Skipping applying extended mode")
                logging.info("Only 1 display is present. Skipping applying extended mode")

    ##
    # @brief        Applies max supported resolution for the planned displays
    # @return       None
    def apply_max_resolution_to_displays(self):
        for disp, val in VdscMstDscPassthrough.display_to_targetID_map.items():
            if "Display" not in disp:
                continue
            mode = VdscMstDscPassthrough.display_config.get_current_mode(VdscMstDscPassthrough.display_to_targetID_map[disp])
            mode.HzRes = int(VdscMstDscPassthrough.display_dictionary[disp]['HActive'])
            mode.VtRes = int(VdscMstDscPassthrough.display_dictionary[disp]['VActive'])
            mode.refreshRate = int(VdscMstDscPassthrough.display_dictionary[disp]['RefreshRate'])
            mode.scaling = eval("enum.%s" % (VdscMstDscPassthrough.display_dictionary[disp]['Scaling']))

            logging.info(f"Setting desired mode on {VdscMstDscPassthrough.display_dictionary[disp]['panel']} display")
            if not VdscMstDscPassthrough.display_config.set_mode(mode):
                alert.info("Fail: Failed to set desired mode")
                self.fail("Failed to apply mode")
            logging.info(
                f"Successfully set desired mode on {VdscMstDscPassthrough.display_dictionary[disp]['panel']} display")

    ##
    # @brief        Helper function to verify display configuration
    # @param[in]    expected_config: Object of DisplayConfig()
    # @return       None
    def verify_config(self, expected_config):
        if expected_config is None:
            alert.info("FAIL: expected config is None which is not expected.")
            self.fail("Passed config is None. Failing...")
        current_config = VdscMstDscPassthrough.display_config.get_current_display_configuration()
        enumerated_displays = VdscMstDscPassthrough.display_config.get_enumerated_display_info()
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
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

    ##
    # @brief        To verify if current mode is same as desired mode from xml
    # @return       None
    def verify_current_mode(self):
        for disp, val in VdscMstDscPassthrough.display_to_targetID_map.items():
            if "Display" not in disp:
                continue
            mode = VdscMstDscPassthrough.display_config.get_current_mode(VdscMstDscPassthrough.display_to_targetID_map[disp])
            if (mode.HzRes == int(VdscMstDscPassthrough.display_dictionary[disp]['HActive'])
                    and mode.VtRes == int(VdscMstDscPassthrough.display_dictionary[disp]['VActive'])
                    and mode.refreshRate == int(VdscMstDscPassthrough.display_dictionary[disp]['RefreshRate'])):
                alert.info(f"Mode is same as desired mode for {VdscMstDscPassthrough.display_dictionary[disp]['panel']}")
                logging.info(f"Mode is same as desired mode for {VdscMstDscPassthrough.display_dictionary[disp]['panel']}")
            else:
                alert.info(
                    f"Fail: Mode is not same as desired mode for {VdscMstDscPassthrough.display_dictionary[disp]['panel']}")
                logging.error(f"Mode is not same as desired mode for "
                              f"{VdscMstDscPassthrough.display_dictionary[disp]['panel']}")

    def verify_generic(self):
        user_msg = ("[Expectation]: No corruption/blankout/flicker/BSOD should be seen on all the displays.\n"
                    "[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Corruption/blankout/flicker/BSOD was not seen.")

    ##
    # @brief        This method is the exit point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('VdscMstDscPassthrough'))
    TestEnvironment.cleanup(outcome)
