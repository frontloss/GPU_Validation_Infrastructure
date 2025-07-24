########################################################################################################################
# @file         test_dp_2p1_hub_audio_playback.py
# @brief        Manual test to check if audio is working on displays connected to DP 2.1 MST hub.
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3644295/
#               Manual test name: test_dp_2p1_hub_audio_playback
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
from Libs.Feature.display_port import dpcd_helper

XML_PATH = os.path.join(test_context.ROOT_FOLDER, "Tests\\Display_Port\\ManualTests\\config_xmls")


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class Dp2p1HubAudioPlayback(unittest.TestCase):
    my_custom_tags = ['-xml']
    xml_file = None
    is_initial_display_connected = False
    # display_dictionary = {
    #     'Display1': {'panel': 'Asus XG27UQR', 'Connector': 'Type-C', 'HActive': 3840, 'VActive': 2160,
    #                  'RefreshRate': 144, 'Scaling': 'MDS', 'AudioChannels':2, 'AudioSampleRates':[32, 44.1, 48]},
    #     'Display2': {'panel': 'Asus PG43UQ', 'Connector': 'DP', 'HActive': 3840, 'VActive': 2160, 'RefreshRate': 144,
    #               'Scaling': 'MDS', 'AudioChannels':2, 'AudioSampleRates':[32, 44.1, 48]},
    #     'Display3': {'panel': 'Acer XB283K', 'Connector': 'DP', 'HActive': 3840, 'VActive': 2160,
    #                'RefreshRate': 144, 'Scaling': 'MDS', 'AudioChannels':2, 'AudioSampleRates':[32, 44.1, 48]},
    #     'Display4': {'panel': 'Dell G3223Q', 'Connector': 'HDMI2.1', 'HActive': 3840, 'VActive': 2160,
    #                'RefreshRate': 144, 'Scaling': 'MDS', 'AudioChannels':2, 'AudioSampleRates':[32, 44.1, 48]},}
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
        self.__class__.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.__class__.my_custom_tags)

        if 'XML' not in self.__class__.cmd_line_param.keys():
            alert.info("Aborting the test as xml file is not provided in command-line")
            self.fail("Aborting the test as xml file is not provided in command-line")
        self.__class__.xml_file = self.__class__.cmd_line_param['XML'][0]

    ##
    # @brief        This step boots the system with planned eDP or Headless
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
    # @brief        This step plugs dp2.1 hub to system, plugs displays and applies extended config and max mode.
    #               This step combines Manual test steps 2, 3 and 4.
    # @return       None
    def test_02_step(self):
        alert.info("Step2: Note: Step to be done by user manually.\n"
                   "Scenario:Plug the planned DP2.1 MST hub to the system without displays connected.")
        user_msg = ("[Expectation]: No corruption/blankout/flicker/BSOD should be seen.\n"
                    "[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Dock is plugged to the system. Corruption/blankout/flicker/BSOD was not seen.")

        alert.info("This step involves plugging planned displays to Dock, applies extended Config and verifies dpcd.")
        xml_file_path = os.path.join(XML_PATH, self.__class__.xml_file)
        self.__class__.display_dictionary = mode_xml_parser.parse_xml(xml_file_path)
        self.plug_displays_to_dock()

        self.__class__.expected_config = self.__class__.display_config.get_current_display_configuration()

    ##
    # @brief This step involves checking all supported Audio channels and Sample rates for all the panels.
    # @return None
    def test_05_step(self):
        alert.info("Step5:\n"
                   "Scenario: Under sound page, verifying all supported audio formats (channels and sample rates)")
        time.sleep(1)
        status = True

        for key, value in self.__class__.display_dictionary.items():
            alert.info(f"Note: Step to be done by user manually.\n"
                       f"For {value['panel']} panel, check if Audio Channels: {value['AudioChannels']} "
                       f"and Audio Sample rates :{value['AudioSampleRates']} are enumerated.\n")
            time.sleep(10)
            user_msg = (f"For {value['panel']} panel, confirm if Audio Channels: {value['AudioChannels']} and "
                        f"Audio Sample rates :{value['AudioSampleRates']} are enumerated.\n"
                        f"[CONFIRM]:Enter yes if expectation met, else enter no.")
            result = alert.confirm(user_msg)
            if not result:
                logging.error(f"For {value['panel']} Audio Channels: {value['AudioChannels']} "
                              f"and Audio Sample rates :{value['AudioSampleRates']} are not enumerated.")
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info(f"For {value['panel']} Audio Channels: {value['AudioChannels']} "
                             f"and Audio Sample rates :{value['AudioSampleRates']} are enumerated.")
        if status is False:
            self.fail("Audio channels/samples not enumerated correctly.")

    ##
    # @brief This step involves playing all supported Audio channels and Sample rates for all the panels.
    # @return None
    def test_06_step(self):
        alert.info("Step6: \n"
                   "Scenario: User has to play all supported audio formats (channels and sample rates).")
        time.sleep(2)

        for key, value in self.__class__.display_dictionary.items():
            alert.info(f"Note: Step to be done by user manually.\n"
                       f"For {value['panel']} panel, Play audio playback for Audio Channels: {value['AudioChannels']} "
                       f"and Audio Sample rates :{value['AudioSampleRates']}.\n")
            time.sleep(60)
            user_msg = (
                f"Make sure no corruption/glitches are heard while playing audio with all the formats.\n"
                f"[CONFIRM]:Enter yes if expectation met, else enter no.")
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                self.fail(f"User observations: {msg['Message']}")
            else:
                logging.info(f"{value['panel']}:No corruption/glitches heard while playing audio with all the formats.")

    ##
    # @brief        This step unplugs-plugs each display from dp2.1 mst hub, verifies Audio playback and verifies
    #               controller, codec entering to D3. Also, verifies 2ch 16bit 48KHz playback
    # @return       None
    def test_07_step(self):
        logging.info("Step 7:Unplug-plug each display from DP2.1 MST hub. Checks audio codec/controller entering to D3")
        alert.info("In following step, hot unplug and hot plug each display from the dock one-by-one."
                   "\nNote: plug the displays back to same port mentioned initially in last steps.")
        status = True
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        initial_display_count = enumerated_display.Count

        for key, value in self.__class__.display_dictionary.items():
            alert.info(f"Note: Step to be done by user manually.\n"
                       f"Scenario:Hot unplug Display{value['panel']} from dock.\n"
                       f"Make sure audio endpoint for the corresponding panel is removed")
            time.sleep(5)
            user_msg = (f"[Expectation]:Ensure, the display is unplugged and Audio endpoint removed for this panel.\n"
                        "[CONFIRM]:Enter yes if expectation met, else enter no")
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
            else:
                logging.info(f"Display {value['panel']} is unplugged from the dock")

            time.sleep(5)  # mandated in test to wait for 5sec

            alert.info(f"Note: Step to be done by user manually."
                       f"Scenario:Hot plug Display{value['panel']} to DP2.1 MST hub again..\n")
            time.sleep(5)
            user_msg = (f"[Expectation]:Ensure, the display is detected.\n"
                        "[CONFIRM]:Enter yes if expectation met, else enter no")
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info(f"Display{value['panel']} is plugged to the dock")

            updated_enumerated_display = self.__class__.display_config.get_enumerated_display_info()
            if initial_display_count != updated_enumerated_display.Count:
                logging.error(f"Displays are not detected post plug.")
                alert.info(f"Fail: Displays are not detected post plug.")
                status = False

            alert.info(f"Note: Step to be done by user manually."
                       f"Play the max audio supported by the panel.")
            time.sleep(5)
            user_msg = (f"[Expectation]:Make sure no audio corruption / glitches are heard.\n"
                        "[CONFIRM]:Enter yes if expectation met, else enter no")
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info(f"Max Audio played on {value['panel']} without issues.")

            alert.info(f"Note: Step to be done by user manually."
                       f"Wait for 60sec for the codec and controller to enter into D3.")
            time.sleep(60)
            user_msg = (f"[Expectation]:Make sure endpoint is listing and codec and "
                        f"audio controller are entering into D3 within 60 sec.\n"
                        "[CONFIRM]:Enter yes if expectation met, else enter no")
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info(f"Endpoint is listing and codec, audio controller entered into D3 within 60s.")

            alert.info(f"Note: Step to be done by user manually."
                       f"Play 2ch 16bit 48KHz audio playback.\n"
                       f"Make sure no audio corruption / glitches are heard Also, check codec, controller in D0 state.")
            time.sleep(10)
            user_msg = (f"[Expectation]:Make sure no audio corruption / glitches are heard.\n"
                        f"Also, check codec, controller in D0 state..\n"
                        "[CONFIRM]:Enter yes if expectation met, else enter no")
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info(f"For 2ch 16bit 48KHz audio playback, no audio corruption/glitches are heard."
                             f"Codec,controller entered to D0 state.")
        if status is False:
            self.fail("Audio end point verification failed.")
            

    ##
    # @brief        To plug display to dock one by one, post plug apply extended mode between
    #               all the connected displays and then do modeset with desired mode for each display
    # @return       None
    def plug_displays_to_dock(self):
        display_adapter_info_list = []
        self.__class__.display_to_targetID_map = {}
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        # Adding already connected display and adapter info to the list
        if enumerated_display.Count != 0:
            for i in range(0, enumerated_display.Count):
                display_adapter_info_list.append(
                    enumerated_display.ConnectedDisplays[i].DisplayAndAdapterInfo)
                tid = enumerated_display.ConnectedDisplays[i].DisplayAndAdapterInfo.TargetID
                port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[i].ConnectorNPortType))
                self.__class__.display_to_targetID_map[port_type] = tid
                if port_type != "VIRTUALDISPLAY":
                    self.__class__.is_initial_display_connected = True

        for key, value in self.__class__.display_dictionary.items():
            updated_enum_port_list = []
            enumerated_display = self.__class__.display_config.get_enumerated_display_info()
            if enumerated_display.Count != 0:
                for i in range(0, enumerated_display.Count):
                    port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[i].ConnectorNPortType))
                    if port_type == "VIRTUALDISPLAY":
                        enumerated_display.Count -= 1
            alert.info(f"Note: Step to be done by user manually."
                       f"\nPlug {value['panel']} panel on {value['Connector']} port.\n"
                       f"Plugged display should come up without any issues and "
                       f"audio endpoint should be loaded for the display which is connected.")
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
            updated_enumerated_display = self.__class__.display_config.get_enumerated_display_info()
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
                    if tid not in self.__class__.display_to_targetID_map.values():
                        self.__class__.display_to_targetID_map[key] = tid
                    updated_enum_port_list.append(updated_enumerated_display.ConnectedDisplays[i].DisplayAndAdapterInfo)
            else:
                alert.info("Enumerated displays count is 0")
                self.fail("Enumerated displays count is 0")

            # To apply extended mode, we need minimum 2 displays.
            # checking this condition to skip modeset when only 1 display is connected.
            if updated_enumerated_display.Count >= 2:
                alert.info("Applying extended mode")
                logging.info("Applying extended mode")
                status = self.__class__.display_config.set_display_configuration_ex(enum.EXTENDED,
                                                                                    updated_enum_port_list)
                if not status:
                    alert.info("Applying Extended mode failed")
                    self.fail("Applying Extended mode failed")

                for disp, val in self.__class__.display_to_targetID_map.items():
                    if "Display" not in disp:
                        continue
                    mode = self.__class__.display_config.get_current_mode(self.__class__.display_to_targetID_map[disp])
                    mode.HzRes = int(self.__class__.display_dictionary[disp]['HActive'])
                    mode.VtRes = int(self.__class__.display_dictionary[disp]['VActive'])
                    mode.refreshRate = int(self.__class__.display_dictionary[disp]['RefreshRate'])
                    mode.scaling = eval("enum.%s" % (self.__class__.display_dictionary[disp]['Scaling']))

                    logging.info(f"Setting desired mode on {self.__class__.display_dictionary[disp]['panel']} display")
                    if not self.__class__.display_config.set_mode(mode):
                        alert.info("Fail: Failed to set desired mode")
                        self.fail("Failed to apply mode")
                    logging.info(
                        f"Successfully set desired mode on {self.__class__.display_dictionary[disp]['panel']} display")
                    if not self.verify_dpcd(self.__class__.display_to_targetID_map[disp]):
                        alert.info(f"Fail:Failed to verify dpcd for {self.__class__.display_dictionary[disp]['panel']}")
                        self.fail(f"Fail:Failed to verify dpcd for {self.__class__.display_dictionary[disp]['panel']}")
                    logging.info(
                        f"Successfully verified dpcd for {self.__class__.display_dictionary[disp]['panel']}")
            else:
                alert.info("Only 1 display is present. Skipping applying extended mode")
                logging.info("Only 1 display is present. Skipping applying extended mode")

    ##
    # @brief        Helper function to verify display configuration
    # @param[in]    expected_config: Object of DisplayConfig()
    # @return       None
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
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

    ##
    # @brief        To verify if current mode is same as desired mode from xml
    # @return       None
    def verify_current_mode(self):
        for disp, val in self.__class__.display_to_targetID_map.items():
            if "Display" not in disp:
                continue
            mode = self.__class__.display_config.get_current_mode(self.__class__.display_to_targetID_map[disp])
            if (mode.HzRes == int(self.__class__.display_dictionary[disp]['HActive'])
                    and mode.VtRes == int(self.__class__.display_dictionary[disp]['VActive'])
                    and mode.refreshRate == int(self.__class__.display_dictionary[disp]['RefreshRate'])):
                alert.info(f"Mode is same as desired mode for {self.__class__.display_dictionary[disp]['panel']}")
                logging.info(f"Mode is same as desired mode for {self.__class__.display_dictionary[disp]['panel']}")
            else:
                alert.info(
                    f"Fail: Mode is not same as desired mode for {self.__class__.display_dictionary[disp]['panel']}")
                logging.error(f"Mode is not same as desired mode for "
                              f"{self.__class__.display_dictionary[disp]['panel']}")

    def verify_generic(self):
        user_msg = ("[Expectation]: No corruption/blankout/flicker/BSOD should be seen on all the displays.\n"
                    "[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            self.fail(f"User observations: {msg['Message']}")
        else:
            logging.info("Corruption/blankout/flicker/BSOD was not seen.")

    def verify_dpcd(self, target_id):
        link_rate: float = dpcd_helper.DPCD_getLinkRate(target_id)
        lane_count = dpcd_helper.DPCD_getNumOfLanes(target_id)
        if link_rate == 20.0 and lane_count == 4:
            logging.info(f"LinkRate:{link_rate}, Lanecount:{lane_count} programmed correctly for targetid:{target_id}.")
        else:
            logging.error(
                f"LinkRate:{link_rate}, Lanecount:{lane_count} incorrectly programmed for targetid:{target_id}.")
            return False
        return True

    ##
    # @brief        This method is the exit point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('Dp2p1HubAudioPlayback'))
    TestEnvironment.cleanup(outcome)