########################################################################################################################
# @file         display_dock_sanity_unplug_plug_power_event_audio_video_hdr.py
# @brief        Manual sanity test to verify display driver when using different functionalities of a Dock.
#               This test uses static configuration, i.e. dock and all displays to be connected are
#               mentioned in Grid
# Manual of     https://gta.intel.com/procedures/#/procedures/TI-3494775/ TI.
#               Manual test name: Display_Dock_Sanity_Unplug_Plug_Power_Event_Audio_Video_HDR_Test
# @author       Golwala, Ami
########################################################################################################################
import logging
import os
import sys
import time
import unittest
from collections import OrderedDict

from Libs.Core import display_power, enum, window_helper, cmd_parser, reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import DisplayPower
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from Libs.manual.modules import mode_xml_parser
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase
from Tests.PowerCons.Modules import common, desktop_controls

XML_PATH = os.path.join(test_context.ROOT_FOLDER, "Tests\\Display_Port\\ManualTests\\config_xmls")


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class DisplayDockSanityUnplugPlugPowerEventAudioVideoHDR(unittest.TestCase):
    my_custom_tags = ['-xml']
    xml_file = None
    is_initial_display_connected = False
    is_virtual_display_connected = False
    is_cs_supported = False
    # display_dictionary = {
    #     'Display1': {'panel': 'DELL 3219Q', 'Connector': 'Type-C', 'HActive': 1024, 'VActive': 768, 'RefreshRate': 60,
    #               'Scaling': 'MDS'},
    #     'Display2': {'panel': 'BENQ SW320', 'Connector': 'DP', 'HActive': 1920, 'VActive': 1080, 'RefreshRate': 60,
    #               'Scaling': 'MDS'}}
    display_dictionary = OrderedDict()
    display_to_targetID_map = {}
    enum_port_list = []
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
    # @brief        This step boots the system if display is planned and connects the dock
    # @return       None
    def test_01_step(self):
        self.__class__.is_cs_supported = self.__class__.display_pwr.is_power_state_supported(
            display_power.PowerEvent.CS)
        if self.__class__.is_cs_supported:
            logging.info("System Supports CS.")
        else:
            logging.info("System Supports S3.")

        user_msg = ("Note: Step to be done by user manually."
                    "\n[Expectation]:Connect eDP if planned, else Boot the system using VNC."
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            self.fail("Test is not started with planned panel. Rerun the test with planned panel.")
        else:
            logging.info("Test started with planned panels")

        user_msg = ("Note: Step to be done by user manually."
                    "\n[Expectation]:Plug the Dock planned to the planned TBT port on the system. No "
                    "corruption/blankout/flicker/BSOD should be seen on all the displays."
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Dock is plugged to the system. No corruption/blankout/flicker/BSOD was seen on all the "
                         "displays.")

    ##
    # @brief        This step plugs displays to dock, applies extended mode and applies mentioned mode
    # @return       None
    def test_02_step(self):
        xml_file_path = os.path.join(XML_PATH, self.__class__.xml_file)
        self.__class__.display_dictionary = mode_xml_parser.parse_xml(xml_file_path)
        self.plug_displays_to_dock()

    ##
    # @brief        This step unplugs-plugs each display from dock
    # @return       None
    def test_03_step(self):
        logging.info("Step 03: Unplug-plug each display from dock")
        self.__class__.expected_config = self.__class__.display_config.get_current_display_configuration()
        enumerated_displays = self.__class__.display_config.get_enumerated_display_info()
        logging.error(f"Current Display configuration: {self.__class__.expected_config.to_string_with_target_id(enumerated_displays)}")
        for iteration in range(3):
            self.plug_unplug_display_to_dock()

    ##
    # @brief        This step unplugs-plugs dock to the system
    # @return       None
    def test_04_step(self):
        # self.__class__.expected_config = self.__class__.display_config.get_current_display_configuration()

        user_msg = (f"Note: Step to be done by user manually."
                    f"\n[Expectation]:With all displays still connected to dock, hot unplug the dock "
                    f"input connection from RVP. \nThere shouldn't be any hang or BSOD when hot unplug is done."
                    f"\nIf eDP is in planned displays, eDP should become active after dock is unplugged. eDP display "
                    f"should come up without corruption / flicker/ blankout."
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info(f"Dock is unplugged from RVP")

        time.sleep(2)

        user_msg = (f"Note: Step to be done by user manually."
                    f"\n[Expectation]:With all displays still connected to dock, hot plug the dock "
                    f"input connection to RVP. \nAfter plug, all displays should be detected and active displays "
                    f"should come up without corruption / flicker/ blankout. "
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info(f"Dock is plugged to RVP")

        time.sleep(2)
        self.verify_config(self.__class__.expected_config)
        self.verify_current_mode()

    ##
    # @brief        This step reboots the system
    # @return       None
    def test_05_step(self):
        # self.__class__.expected_config = self.__class__.display_config.get_current_display_configuration()
        alert.info("Rebooting the system. Rerun same commandline once booted to Desktop to continue the test")
        logging.info("Rebooting the system")
        data = {'display_to_targetID_map': self.__class__.display_to_targetID_map,
                'display_dictionary': self.__class__.display_dictionary,
                'is_initial_display_connected': self.__class__.is_initial_display_connected,
                'is_cs_supported': self.__class__.is_cs_supported,
                'expected_config': self.__class__.expected_config}
        if reboot_helper.reboot(self, 'test_06_step', data=data) is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This step unplugs-plugs each display from dock.
    # @return       None
    def test_06_step(self):
        data = reboot_helper._get_reboot_data()
        self.__class__.display_dictionary = data['display_dictionary']
        self.__class__.display_to_targetID_map = data['display_to_targetID_map']
        self.__class__.is_initial_display_connected = data['is_initial_display_connected']
        self.__class__.is_cs_supported = data['is_cs_supported']
        self.__class__.expected_config = data['expected_config']

        user_msg = (f"[Expectation]:After booted back to OS, displays should be detected and active displays "
                    f"should come up without corruption / flicker/ blankout."
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info(f"System Successfully rebooted ")

        self.verify_config(self.__class__.expected_config)
        self.verify_current_mode()

        self.plug_unplug_display_to_dock()

        alert.info(
            "With Dock connected and all displays still connected, going to CS/S3. "
            "Look for any corruption / flicker/ blankout.")
        logging.info("With Dock connected and all displays still connected, going to CS/S3.")
        time.sleep(2)
        if self.__class__.is_cs_supported:
            if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.CS, 60) is False:
                self.fail(f'Failed to invoke power event CS')
            logging.info("Successfully performed power event CS")
            alert.info("Successfully performed power event CS")
        else:
            if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.S3, 60) is False:
                self.fail(f'Failed to invoke power event S3')
            logging.info("Successfully performed power event S3")
            alert.info("Successfully performed power event S3")

        user_msg = (f"[Expectation]:After resume from CS/S3, displays should be detected and active displays "
                    f"should come up without corruption / flicker/ blankout."
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info(f"System Successfully resumed from CS/S3")

        self.verify_config(self.__class__.expected_config)
        self.verify_current_mode()

        self.plug_unplug_display_to_dock()

        # self.__class__.expected_config = self.__class__.display_config.get_current_display_configuration()
        alert.info(
            "With Dock connected and all displays still connected, going to S4.Look for any corruption / flicker/ "
            "blankout. During resume, there shouldn't be any POST logo corruption")
        logging.info("With Dock connected and all displays still connected, going to S4.")
        time.sleep(2)
        if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.S4, 60) is False:
            self.fail(f'Failed to invoke power event S4')
        logging.info("Successfully performed power event S4")

        user_msg = (f"[Expectation]:After resume from S4, displays should be detected and active displays "
                    f"should come up without corruption / flicker/ blankout. During resume, there shouldn't be any "
                    f"POST logo corruption."
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info(f"System Successfully resumed from S4")

        self.verify_config(self.__class__.expected_config)
        self.verify_current_mode()
        self.plug_unplug_display_to_dock()

    ##
    # @brief        This step does video playback and drags playback to each display
    # @return       None
    def test_07_step(self):
        alert.info("Launching 24 FPS video")
        logging.info("Launching 24 FPS video")
        window_helper.open_uri(os.path.join(common.TEST_VIDEOS_PATH, '24.000.mp4'))
        time.sleep(5)
        logging.info("Launched 24 FPS video successfully.")

        alert.info("Note: Step to be done by user manually."
                   "\nDrag playback window to each display. Keeping timeout of 2min to complete this."
                   "\nThere shouldn't be any corruption / "
                   f"flicker/ blankout on the display during video playback. Video playback should be smooth.")
        logging.info("Dragging playback window to each display.")
        time.sleep(120)

        alert.info("Closing media player")
        window_helper.close_media_player()
        logging.info("Closed media player")

        user_msg = (f"[Expectation]: There shouldn't be any corruption flicker/ blankout on the display during video "
                    f"playback. Video playback should be smooth."
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info(f"No corruption flicker/ blankout on the display during video playback")

    ##
    # @brief        This step plays audio clip on each audio capable panel
    # @return       None
    def test_08_step(self):
        logging.info("Playing audio clip using the display audio on first plugged display which supports audio. "
                     "Repeating for every audio capable display connected (select audio playback device to this "
                     "display).")

        alert.info(f"Note: Step to be done by user manually. Keeping 5min of timeout from test to perform this."
                   f"\n[Expectation]:Play any audio clip using the display audio on first plugged display which "
                   f"supports audio. Repeat for every audio capable display connected (select audio playback device "
                   f"to this display). \nAudio playback should be smooth without any corruption or audio issue. There "
                   f"shouldn't be any corruption / flicker/ blankout on the display during audio clip "
                   f"playback.\nExpected number of audio channels: On whichever display audio playback is done, "
                   f"max audio channels should work")
        time.sleep(300)

        user_msg = (f"[Expectation]:Audio playback should be smooth without any corruption or audio issue. There "
                    f"shouldn't be any corruption / flicker/ blankout on the display during audio clip "
                    f"playback.\nExpected number of audio channels: On whichever display audio playback is done, "
                    f"max audio channels should work."
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info(f"Successfully performed audio verification")

    ##
    # @brief        This step enables HDR on supported panel
    # @return       None
    def test_09_step(self):
        alert.info("Enabling HDR on all supported displays. No Corruption, Screen Blankout should be visible.")
        logging.info("Enabling HDR on all supported displays.")

        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            # TODO: Currently above function returns False if any of the panels doesn't support HDR. This needs fix
            #  from above function.
            alert.info("Failed to enable HDR on all supported panels")
            logging.error("Enabling HDR on all supported panels failed")
            alert.info("Step to be performed by user manually. \n Enable HDR on all supported panel "
                       "manually. Waiting for 2mins")
            time.sleep(120)

        user_msg = "[Expectation]:No Corruption, Screen Blankout should be visible while enabling HDR" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No Corruption, Screen Blankout was visible while enabling HDR")

    ##
    # @brief        This step unplugs/plugs displays and performs power event CS
    # @return       None
    def test_10_step(self):
        user_msg = ("Note: Step to be done by user manually."
                    "\n[Expectation]:Unplug all the Displays"
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Successfully unplugged all the displays")

        self.plug_displays_to_dock()

        if self.__class__.is_cs_supported:
            self.plug_unplug_during_power_event(display_power.PowerEvent.CS)
        else:
            self.plug_unplug_during_power_event(display_power.PowerEvent.S3)

    ##
    # @brief        This step unplugs/plugs displays and performs power event S4
    # @return       None
    def test_11_step(self):
        user_msg = "[Expectation]:Unplug all the Displays" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Successfully unplugged all the displays")

        self.plug_displays_to_dock()
        self.plug_unplug_during_power_event(display_power.PowerEvent.S4)

    ##
    # @brief        This step unplugs/plugs displays and performs power event S4
    # @return       None
    def test_12_step(self):
        user_msg = "[Expectation]:Unplug all the Displays" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Successfully unplugged all the displays")

        self.plug_displays_to_dock()

        alert.info("Scenario: Setting Monitor turn off from system with 1min timeout.")
        logging.info("Setting display time-out to 1 minute")
        # self.__class__.expected_config = self.__class__.display_config.get_current_display_configuration()
        if desktop_controls.set_time_out(desktop_controls.TimeOut.TIME_OUT_DISPLAY, 1) is False:
            self.fail("Failed to set display time-out to 1 minute (Test Issue)")
        logging.info("\tSet display time-out to 1 minute successful.")

        alert.info("Note: Step to be done by user manually."
                   "Once the monitor turns off, unplug all dock displays. Resume from MTO by moving mouse or keyboard "
                   "press.")

        logging.info("Waiting for 1min..")
        time.sleep(60)

        logging.info("Waiting for user to turn on monitor")
        user_msg = ("[Expectation]: Monitor should have turned off and turned back on.\n "
                    "plug back all the Displays.\n"
                    "Ensure No Visual artifacts/ corruption/ TDR/ BSOD should occur.\n"
                    "[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Monitor turned off and turned back on without any issues. All displays were plugged back")

        self.verify_config(self.__class__.expected_config)
        self.verify_current_mode()

    ##
    # @brief        This method unplugs/plugs displays and performs power event
    # @param[in]    power_state: Power state to be invoked
    #                   power state to be applied EX: CS, s3, s4, s5
    # @return       None
    def plug_unplug_during_power_event(self, power_state: display_power.PowerEvent):
        expected_config = self.__class__.display_config.get_current_display_configuration()
        logging.info("Unplugging all the displays except any one dock display")

        alert.info(f"Test is invoking {power_state.name} for 90 seconds. "
                   f"\nNote: Step to be done by user manually."
                   f"\nWhile in sleep mode, unplug all dock displays except any one dock display")
        logging.info(f"Invoking {power_state.name}. While in sleep mode, unplugging all dock displays except any one "
                     f"dock display")
        time.sleep(2)
        if self.__class__.display_pwr.invoke_power_event(power_state, 90) is False:
            self.fail(f'Failed to invoke {power_state.name}')
        logging.info(f"Successfully performed {power_state.name}")
        alert.info(f"Successfully performed {power_state.name}")

        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if self.__class__.is_initial_display_connected:
            if enumerated_display.Count != 2:
                alert.info("Fail: We expect 2 displays to be connected including eDP")
                self.fail("We expect 2 displays to be connected including eDP")
        else:
            if enumerated_display.Count != 1:
                alert.info("Fail: We expect 1 display to be connected")
                self.fail("We expect 1 display to be connected")

        user_msg = (f"Note: Step to be done by user manually."
                    f"\n[Expectation]: Unplug the last dock display"
                    f"\n[CONFIRM]:Enter yes if expectation met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info(f"Unplugged last dock display successfully")

        alert.info(f"Test is invoking{power_state.name} for 90 seconds. "
                   f"\nNote: Step to be done by user manually."
                   f"\nWhile in sleep mode, plug all displays in order in which they were unplugged")
        logging.info(f"Invoking {power_state.name}. While in sleep mode, plugging all displays in order")
        time.sleep(2)
        if self.__class__.display_pwr.invoke_power_event(power_state, 90) is False:
            self.fail(f'Failed to invoke {power_state.name}')
        logging.info(f"Successfully performed {power_state.name}")
        alert.info(f"Successfully performed {power_state.name}")

        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if self.__class__.is_initial_display_connected:
            if enumerated_display.Count != len(self.__class__.display_dictionary) + 1:
                alert.info(f"Fail: We expect {len(self.__class__.display_dictionary) + 1} displays to be connected "
                           f"including eDP")
                self.fail(
                    f"We expect {len(self.__class__.display_dictionary) + 1} displays to be connected including eDP")
        else:
            if enumerated_display.Count != len(self.__class__.display_dictionary):
                alert.info(f"Fail: We expect {len(self.__class__.display_dictionary)} displays to be connected")
                self.fail(f"We expect {len(self.__class__.display_dictionary)} displays to be connected")

        # Checking if config and resolution persisted
        self.verify_config(expected_config)
        self.verify_current_mode()

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

            user_msg = (
                f"Note: Step to be done by user manually."
                f"\nPlug {value['panel']} panel on {value['Connector']} port. Newly plugged displays should be "
                f"detected and active displays should come up without corruption / flicker/ blankout."
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
            else:
                alert.info("Only 1 display is present. Skipping applying extended mode")
                logging.info("Only 1 display is present. Skipping applying extended mode")

    ##
    # @brief        To unplug and plug back each Display one by one
    # @return       None
    def plug_unplug_display_to_dock(self):
        alert.info("In following step, hot unplug and hot plug each display from the dock one-by-one."
                   "\nNote: plug the displays back to same port mentioned initially in last steps.")

        for key, value in self.__class__.display_dictionary.items():
            enumerated_display = self.__class__.display_config.get_enumerated_display_info()
            user_msg = (f"Note: Step to be done by user manually."
                        f"\n[Expectation]:Hot unplug Display{value['panel']} from dock."
                        "\n[CONFIRM]:Enter yes if expectation met, else enter no")
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
            else:
                logging.info(f"Display{value['panel']} is unplugged from the dock")

            time.sleep(2)
            updated_enumerated_display = self.__class__.display_config.get_enumerated_display_info()
            if updated_enumerated_display.Count == 1:
                for i in range(0, updated_enumerated_display.Count):
                    port_type = str(
                        CONNECTOR_PORT_TYPE(updated_enumerated_display.ConnectedDisplays[i].ConnectorNPortType))
                    if port_type == "VIRTUALDISPLAY":
                        enumerated_display.Count += 1

            if updated_enumerated_display.Count != enumerated_display.Count - 1:
                alert.info(f"Fail: After unplug of Display{value['panel']}, still number of enumerated displays are "
                           f"same as before")
                self.fail(f"After unplug of Display{value['panel']}, still number of enumerated displays are same as "
                          f"before")

        for key, value in self.__class__.display_dictionary.items():
            enumerated_display = self.__class__.display_config.get_enumerated_display_info()
            if enumerated_display.Count == 1:
                for i in range(0, enumerated_display.Count):
                    port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[i].ConnectorNPortType))
                    if port_type == "VIRTUALDISPLAY":
                        enumerated_display.Count -= 1

            user_msg = (f"Note: Step to be done by user manually."
                        f"\n[Expectation]:Hot plug Display{value['panel']} to dock."
                        f"\nDisplay should be detected and active displays should come up without corruption / "
                        f"flicker/ blankout"
                        "\n[CONFIRM]:Enter yes if expectation met, else enter no")
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
            else:
                logging.info(f"Display{value['panel']} is plugged back to the dock")

            time.sleep(2)
            updated_enumerated_display = self.__class__.display_config.get_enumerated_display_info()
            if updated_enumerated_display.Count != enumerated_display.Count + 1:
                alert.info(f"Fail: After plug of Display{value['panel']}, still number of enumerated displays are "
                           f"same as before")
                self.fail(f"After plug of Display{value['panel']}, still number of enumerated displays are same as "
                          f"before")

            # Checking persistence of config and mode. For extended mode, minimum 2 displays should be connected.
            if updated_enumerated_display.Count >= 2:
                get_config = self.__class__.display_config.get_current_display_configuration()
                if get_config.topology != enum.EXTENDED:
                    alert.info(f"Fail: After hot plug of {value['panel']} , config is not in extended mode. "
                               f"Current config is {get_config.topology}")
                    logging.error(f"Fail: After hot plug of {value['panel']}, config is not in extended mode. "
                                  f"Current config is {get_config.topology}")

            for i in range(0, updated_enumerated_display.Count):
                tid = updated_enumerated_display.ConnectedDisplays[i].DisplayAndAdapterInfo.TargetID
                mode = self.__class__.display_config.get_current_mode(tid)
                for disp, val in self.__class__.display_to_targetID_map.items():
                    if "Display" not in disp:
                        continue
                    if self.__class__.display_to_targetID_map[disp] == tid:
                        if (mode.HzRes == int(self.__class__.display_dictionary[disp]['HActive'])
                                and mode.VtRes == int(self.__class__.display_dictionary[disp]['VActive'])
                                and mode.refreshRate == int(self.__class__.display_dictionary[disp]['RefreshRate'])):
                            logging.info(f"Mode is same as desired mode for "
                                         f"{self.__class__.display_dictionary[disp]['panel']}")
                        else:
                            alert.info(
                                f"Fail: Mode is not same as desired mode for "
                                f"{self.__class__.display_dictionary[disp]['panel']}")
                            logging.error(f"Mode is not same as desired mode for "
                                          f"{self.__class__.display_dictionary[disp]['panel']}")

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
                          f"{expected_config.to_string_with_target_id(enumerated_displays)} "
                          f"observed: {current_config.to_string_with_target_id(enumerated_displays)}")
            self.fail(f"Display configuration doesn't match.")
        else:
            logging.info(f"Display configuration matches: {current_config.to_string_with_target_id(enumerated_displays)}")

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
            expected_HzRes = int(self.__class__.display_dictionary[disp]['HActive'])
            expected_VtRes = int(self.__class__.display_dictionary[disp]['VActive'])
            expected_rr = int(self.__class__.display_dictionary[disp]['RefreshRate'])
            if mode.HzRes == expected_HzRes and mode.VtRes == expected_VtRes \
                    and abs(mode.refreshRate - expected_rr) <= 1:  # WA for RR mismatch like 60 vs 59
                alert.info(f"Mode is same as desired mode for {self.__class__.display_dictionary[disp]['panel']}")
                logging.info(f"Mode is same as desired mode for {self.__class__.display_dictionary[disp]['panel']}")
            else:
                alert.info(
                    f"Fail: Mode is not same as desired mode for {self.__class__.display_dictionary[disp]['panel']}")
                logging.info(f"Expected:{mode.HzRes}x{mode.VtRes}@{mode.refreshRate},"
                             f" Observed:{expected_HzRes}x{expected_VtRes}@{expected_rr}")
                logging.error(f"Mode is not same as desired mode for "
                              f"{self.__class__.display_dictionary[disp]['panel']}")

    ##
    # @brief        This method is the exit point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('DisplayDockSanityUnplugPlugPowerEventAudioVideoHDR'))
    TestEnvironment.cleanup(outcome)
