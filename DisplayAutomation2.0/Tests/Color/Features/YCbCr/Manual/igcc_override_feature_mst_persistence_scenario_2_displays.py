########################################################################################################################
# @file         igcc_override_feature_mst_persistence_scenario_2_displays.py
# @brief        Manual Test to verify IGCC Override Feature
# Manual TI     https://gta.intel.com/procedures/#/procedures/TI-3554668/
# TI name       Override BPC: IGCC Override Feature + MST Persistence scenario 2 Displays (HDR eDP + HDR with YUV EFP + MST Dongle)
# @author       Golwala, Ami
########################################################################################################################
import logging
import os
import sys
import time
import unittest

from Libs.Core.wrapper.driver_escape_args import AviEncodingMode

from Libs.Core import enum, display_essential, display_power, reboot_helper, window_helper, cmd_parser
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import DisplayPower
from Libs.Core.test_env import context, test_context
from Libs.Core.test_env.context import CmdLineParams
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from Tests.Color.Common import hdr_utility, color_etl_utility
from Tests.Color.Common.color_escapes import get_bpc_encoding, set_bpc_encoding
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding import BpcEncoding


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class IgccOverrideFeatureMstPersistenceScenario2Displays(unittest.TestCase):
    is_dock_planned = False
    is_cs_supported = False
    test_params_from_cmd_line = CmdLineParams()
    ##
    # A dictionary of a list having bpc supported by each panel
    bpc_list = {}
    display_pwr = DisplayPower()
    display_config = DisplayConfiguration()
    context_args = context.Context()
    custom_tags = {'-DOCK_PLANNED': 'FALSE'}

    ##
    # A dictionary of all the properties related to the displays passed from command line
    # This dictionary have a tuple of gfx_index and connector_port_type as key
    # and the value contains tuple of  bpc and encoding BpcEncoding (Bpc='BPC_Value', Encoding='Encoding_Value')
    panel_props_dict = {}
    initial_panel_props_dict = {}

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        pass

    ##
    # @brief This step sets display config and enables HDR
    # @return None
    def test_01_step(self):
        # Parse the command line
        cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.__class__.custom_tags.keys())

        # Handle multi-adapter scenario
        if not isinstance(cmd_line_param, list):
            cmd_line_param = [cmd_line_param]

        self.__class__.test_params_from_cmd_line = self.parse_param_from_command_line(cmd_line_param)
        self.__class__.context_args.init_test_context(self.__class__.test_params_from_cmd_line)
        self.__class__.is_dock_planned = self.__class__.context_args.test.cmd_params.test_custom_tags['-DOCK_PLANNED'][
            0]
        self.__class__.is_dock_planned = True if self.__class__.is_dock_planned == 'TRUE' \
            else False

        self.__class__.is_cs_supported = self.__class__.display_pwr.is_power_state_supported(
            display_power.PowerEvent.CS)

        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        #  Plug the all the displays planned in the grid
        user_msg = ("Note: Step to be done by user manually."
                    "\n[Expectation]: Plug the all the displays planned in the grid"
                    "\n[CONFIRM]: Enter Yes if expectations met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            alert.info("Fail: Please run test with displays planned in the grid")
            self.fail("Fail: Please run test with displays planned in the grid")
        else:
            logging.info("Step1: Test started with all planned panels connected")

        alert.info("Applying extended mode")
        enum_port_list = []
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count >= 2:
            for index in range(0, enumerated_display.Count):
                enum_port_list.append(
                    str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
            status = self.__class__.display_config.set_display_configuration_ex(enum.EXTENDED,
                                                                                enum_port_list)
            if not status:
                alert.info("Applying Extended mode failed")
                self.fail("Applying Extended mode failed")
            alert.info("Successfully applied extended mode")
        else:
            alert.info("Fail: Enumerated display count is less than 2, we can't apply extended mode")
            logging.error("Enumerated display count is is less than 2, we can't apply extended mode")

        logging.info("Enabling Simulated Battery")
        assert self.__class__.display_pwr.enable_disable_simulated_battery(True), "Failed to enable Simulated Battery"
        logging.info("PASS: Enabled Simulated Battery successfully")

        # Checking current power line status and if it is not AC, then changing it to AC
        power_line_status = self.__class__.display_pwr.get_current_powerline_status()
        if power_line_status != display_power.PowerSource.AC:
            alert.info("Changing power line to AC mode. Look at battery if it is changing or not")
            result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.AC)
            self.assertEquals(result, True, "Aborting the test as switching to AC mode failed")

            user_msg = "[Expectation]:Power line should switch to AC mode" \
                       "[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
            else:
                logging.info("Powerline changed to AC")
        else:
            alert.info("Powerline is in AC mode")
            logging.info("Powerline is in AC mode")

        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)

                    # Storing Initial encoding and BPC here to use in step17
                    Bpc_Encoding_caps = BpcEncoding()
                    Bpc_Encoding_caps.Bpc = default_bpc
                    Bpc_Encoding_caps.Encoding = default_encoding
                    Bpc_Encoding_caps.default_encoding = default_encoding
                    self.__class__.initial_panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

                    if not panel.is_lfp:
                        if default_bpc == "BPC8" and default_encoding in ["YCBCR444", "YCBCR422", "YCBCR420"]:
                            alert.info("Failing the test as for HDR, we shouldn't expect YUV with BPC8 for external "
                                       "displays. Current mode of EFP is YUV with BPC8")
                            self.fail("For HDR, we shouldn't expect YUV with BPC8 for external displays. "
                                      "Current mode of EFP is YUV with BPC8")

        alert.info("Enabling HDR on EFP. No Corruption, Screen Blankout should be visible.")
        logging.info("Enabling HDR on EFP")
        # Enable HDR on EFP
        # Below function returns false if any of the connected panels doesn't support HDR. This needs change from FO.
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            alert.info("Failed to enable HDR on EFP")
            logging.error("Enabling HDR on EFP failed")
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
    # @brief This step checks YcBCR Toggle Option based on platform
    # @return None
    def test_02_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        logging.info("Step 02: This step is not valid from Gen13+ as YCbCr toggle option is pruned out")

    ##
    # @brief This step applies Color Depth and format
    # @return None
    def test_03_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        alert.info("Applying all available color format one by one for each available color depth")
        logging.info("Applying all available color format one by one for each available color depth")
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)

                    for index in range(len(combo_bpc_encoding)):
                        color_format = str(combo_bpc_encoding[index][1])
                        bpc = combo_bpc_encoding[index][0]
                        alert.info(
                            f"Applying color format {color_format} for color depth {bpc} on {panel.connector_port_type}."
                            "\nNo TDR/Artifacts should observed.")
                        logging.info(
                            f"Applying color format {color_format} for color depth {bpc} on {panel.connector_port_type}")
                        if not set_bpc_encoding(panel.display_and_adapterInfo, bpc,
                                                color_format, adapter.platform_type, panel.is_lfp):
                            alert.info(f"Failed to set BPC and Encoding on {panel.connector_port_type}")
                            logging.error(
                                f"Fail: Failed to set the override bpc and encoding on {panel.connector_port_type}")
                        logging.info(f"Successfully set BPC and Encoding on {panel.connector_port_type}")

                        user_msg = "[Expectation]:No TDR/Artifacts should be observed" \
                                   "[CONFIRM]:Enter yes if expectation met, else enter no"
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                        else:
                            logging.info("No TDR/Artifacts was observed")

                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)

                    # Storing color depth and format to check the persistence of apply color depth and format later
                    Bpc_Encoding_caps = BpcEncoding()
                    Bpc_Encoding_caps.Bpc = default_bpc
                    Bpc_Encoding_caps.Encoding = default_encoding
                    Bpc_Encoding_caps.default_encoding = default_encoding
                    self.__class__.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

    ##
    # @brief This step performs power events
    # @return None
    def test_04_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        alert.info("Performing power event CS/S3")
        logging.info("Performing power event CS/S3")
        time.sleep(2)
        if self.__class__.is_cs_supported:
            if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.CS, 5) is False:
                self.fail(f'Failed to invoke power event CS')
        else:
            if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.S3, 5) is False:
                self.fail(f'Failed to invoke power event S3')

        alert.info("Successfully performed power event CS/S3")
        logging.info("Successfully performed power event CS/S3")

        # Check the persistence of apply color depth and format in previous step
        self.check_depth_and_format_persistence(self.__class__.panel_props_dict)

        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    # Storing color depth and format to check the persistence of apply color depth and format later
                    Bpc_Encoding_caps = BpcEncoding()
                    Bpc_Encoding_caps.Bpc = default_bpc
                    Bpc_Encoding_caps.Encoding = default_encoding
                    Bpc_Encoding_caps.default_encoding = default_encoding
                    self.__class__.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

        alert.info("Performing power event S4")
        logging.info("Performing power event S4")
        time.sleep(2)
        if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.S4, 5) is False:
            self.fail(f'Failed to invoke power event S4')
        logging.info("Successfully performed power event S4")

        # Check the persistence of apply color depth and format in previous step
        self.check_depth_and_format_persistence(self.__class__.panel_props_dict)
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    # Storing color depth and format to check the persistence of apply color depth and format later
                    Bpc_Encoding_caps = BpcEncoding()
                    Bpc_Encoding_caps.Bpc = default_bpc
                    Bpc_Encoding_caps.Encoding = default_encoding
                    Bpc_Encoding_caps.default_encoding = default_encoding
                    self.__class__.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

    ##
    # @brief This step performs hot plug/unplug
    # @return None
    def test_05_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        logging.info("Step 05: Perform Hot plug/unplug")
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        user_msg = ("Note: Step to be done by user manually."
                    "\nUnPlug external panel."
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Successfully unplugged external panel")

        updated_enum_port_list = []
        updated_enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if updated_enumerated_display.Count > 0:
            for index in range(0, updated_enumerated_display.Count):
                updated_enum_port_list.append(
                    str(CONNECTOR_PORT_TYPE(updated_enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
            if updated_enumerated_display.Count != enumerated_display.Count - 1:
                self.fail("After unplug of external panel, still number of enumerated displays are same as before")
        else:
            alert.info("Fail: Enumerated display count is 0")
            self.fail("Enumerated display count is 0")

        time.sleep(3)

        enumerated_display = self.__class__.display_config.get_enumerated_display_info()

        user_msg = "Hot Plug external panel." \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Successfully plugged external panel")

        updated_enum_port_list = []
        updated_enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if updated_enumerated_display.Count > 0:
            for index in range(0, updated_enumerated_display.Count):
                updated_enum_port_list.append(
                    str(CONNECTOR_PORT_TYPE(updated_enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
            if updated_enumerated_display.Count != enumerated_display.Count + 1:
                self.fail("After hot plug of external display, still number of enumerated displays are same as before")
        else:
            alert.info("Fail: Enumerated display count is 0")
            self.fail("Enumerated display count is 0")

        # Check the persistence of apply color depth and format in previous step
        self.check_depth_and_format_persistence(self.__class__.panel_props_dict)

    ##
    # @brief This step disables HDR
    # @return None
    def test_06_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        logging.info("Disabling HDR on both panels")
        alert.info("Disabling HDR on both panels")
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
            alert.info("Disabling HDR failed")
            logging.error("Disabling HDR on EFP failed")
        alert.info("Disabled HDR successfully")

        alert.info("Resetting color depth and color format")
        logging.info("Resetting color depth and color format")

        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    if not set_bpc_encoding(panel.display_and_adapterInfo, default_bpc,
                                            default_encoding, adapter.platform_type, panel.is_lfp):
                        alert.info("Failed to set default bpc and encoding")
                        logging.error("Fail: Failed to set the override bpc and encoding")
                    alert.info("Successfully set default bpc and encoding")
                    logging.info("Successfully set default bpc and encoding")

    ##
    # @brief This step sets the color pattern 10BPC image as background
    # @return None
    def test_07_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        alert.info("Setting the color pattern 10BPC image as background. Background should get changed")
        logging.info("Setting the color pattern 10BPC image as background")
        desktop_img_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "Color\HDR\Images\color_pattern_10bpc.png")
        window_helper.set_image_as_desktop_background(desktop_img_path)

        user_msg = "[Expectation]:Background should get changed." \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Background changed to 10BPC image.")

    ##
    # @brief This step sets 10BPC if supported by both the panels
    # @return None
    def test_08_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        # bpc_list is a list of list(each panel's supported bpc)
        self.__class__.bpc_list, max_bpc_supported = self.prepare_bpc_list(self.__class__.context_args)

        if self.is_bpc_supported_by_all_panels("BPC10", self.__class__.bpc_list):
            bpc_to_apply = "BPC10"
            alert.info("Setting 10BPC for both the panels. No TDR/Artifacts should observed on both display.")
        else:
            bpc_to_apply = "BPC8"
            alert.info("Setting 8BPC for both the panels as 10BPC is not supported by both the panels. No "
                       "TDR/Artifacts should observed on both display.")

        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)

                    if not set_bpc_encoding(panel.display_and_adapterInfo, bpc_to_apply,
                                            default_encoding, adapter.platform_type, panel.is_lfp):
                        alert.info("Failed to set the override bpc and encoding")
                        logging.error("Failed to set the override bpc and encoding")
                    else:
                        alert.info("Successfully set the override bpc and encoding")
                        logging.info("Successfully set the override bpc and encoding")

                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)

                    # Storing color depth and format to check the persistence of apply color depth and format later
                    Bpc_Encoding_caps = BpcEncoding()
                    Bpc_Encoding_caps.Bpc = default_bpc
                    Bpc_Encoding_caps.Encoding = default_encoding
                    Bpc_Encoding_caps.default_encoding = default_encoding
                    self.__class__.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

                    user_msg = "[Expectation]:Banding artifacts should be visible" \
                               "\n[CONFIRM]:Enter yes if expectation met, else enter no"
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                    else:
                        logging.info("Banding artifacts was visible.")

    ##
    # @brief This step performs power event CS
    # @return None
    def test_09_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        alert.info("Performing power event CS/S3")
        logging.info("Performing power event CS/S3")
        time.sleep(2)
        if self.__class__.is_cs_supported:
            if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.CS, 3) is False:
                self.fail(f'Failed to invoke power event CS')
        else:
            if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.S3, 3) is False:
                self.fail(f'Failed to invoke power event S3')

        logging.info("Successfully performed power event CS/S3")

        # Check the persistence of apply color depth and format in previous step
        self.check_depth_and_format_persistence(self.__class__.panel_props_dict)

        # Storing color depth and format to check the persistence of apply color depth and format later
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    Bpc_Encoding_caps = BpcEncoding()
                    Bpc_Encoding_caps.Bpc = default_bpc
                    Bpc_Encoding_caps.Encoding = default_encoding
                    Bpc_Encoding_caps.default_encoding = default_encoding
                    self.__class__.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

    ##
    # @brief This step restarts gfx driver
    # @return None
    def test_10_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        logging.info("Restarting graphics driver")
        alert.info("Restarting graphics driver")
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            alert.info("Failed to restart graphics driver")
            self.fail(f"FAILED to restart graphics driver")
        logging.info("Successfully restarted graphics driver")
        alert.info("Successfully restarted graphics driver")

        # Check the persistence of apply color depth and format in previous step
        self.check_depth_and_format_persistence(self.__class__.panel_props_dict)

    ##
    # @brief This step sets powerline to DC, updates battery settings and enables HDR
    # @return None
    def test_11_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        alert.info("Changing power line to DC mode. Look at battery if it is changing or not")
        logging.info("Switching to DC mode")

        result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.DC)
        self.assertEquals(result, True, "Aborting the test as switching to DC mode failed")
        user_msg = "[Expectation]:Power line should switch to DC mode" \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Power line changed to DC")

        # Display Setting --> HDR Page --> Battery Option --> Optimized for battery Life.
        alert.info("Note: Step to be done by user manually. Setting timeout of 1min to perform steps."
                   "Goto Display Setting --> HDR Page --> Battery Options. Select Optimized for battery Life")
        time.sleep(60)
        logging.info("Optimized for battery Life settings done")

        logging.info("Enabling HDR on both the displays")
        alert.info("Enabling HDR on both the displays")
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            alert.info("Fail: Failed to enable HDR")
            logging.error("Enabling HDR failed")
            alert.info("Step to be performed by user manually. \n Enable HDR on all supported panel "
                       "manually. Waiting for 2mins")
            time.sleep(120)
        else:
            alert.info("Enabled HDR on both the displays")
            logging.info("Enabled HDR on both the displays")

    ##
    # @brief This step sets the color pattern 12BPC image as background
    # @return None
    def test_12_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        alert.info("Setting the color pattern 12BPC image as background. Background should get changed")
        logging.info("Setting the color pattern 12BPC image as background")
        desktop_img_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "Color\HDR\Images\color_ramp_12bpc.png")
        window_helper.set_image_as_desktop_background(desktop_img_path)

        user_msg = "[Expectation]:Background should get changed." \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Background changed to 12BPC image.")

    ##
    # @brief This step switches to 12 BPC combination on external panel
    # @return None
    def test_13_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        # bpc_list is a list of list(each panel's supported bpc)
        self.__class__.bpc_list, max_bpc_supported = self.prepare_bpc_list(self.__class__.context_args)

        if self.is_bpc_supported_by_all_panels("BPC12", self.__class__.bpc_list):
            bpc_to_apply = "BPC12"
            alert.info("Setting 12BPC for both the panels. No TDR/Artifacts should observed on both display.")
        else:
            bpc_to_apply = "BPC8"
            alert.info("Setting 8BPC for both the panels as 12BPC is not supported by both the panels. No "
                       "TDR/Artifacts should observed on both display.")

        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and not panel.is_lfp:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)

                    if not set_bpc_encoding(panel.display_and_adapterInfo, bpc_to_apply,
                                            default_encoding, adapter.platform_type, panel.is_lfp):
                        alert.info("Failed to set the override bpc and encoding")
                        logging.error("Failed to set the override bpc and encoding")
                    else:
                        alert.info("Successfully set the override bpc and encoding")
                        logging.info("Successfully set the override bpc and encoding")

                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)

                    # Storing color depth and format to check the persistence of apply color depth and format later
                    Bpc_Encoding_caps = BpcEncoding()
                    Bpc_Encoding_caps.Bpc = default_bpc
                    Bpc_Encoding_caps.Encoding = default_encoding
                    Bpc_Encoding_caps.default_encoding = default_encoding
                    self.__class__.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

                    user_msg = "[Expectation]:No TDR/Artifacts should observed on both display." \
                               "\n[CONFIRM]:Enter yes if expectation met, else enter no"
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                    else:
                        logging.info("No TDR/Artifacts should observed on both display.")
        time.sleep(5)

    ##
    # @brief This step performs power event S4
    # @return None
    def test_14_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        alert.info("Performing power event S4. No TDR/Artifacts should be observed")
        logging.info("Performing power event S4")
        time.sleep(2)
        if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.S4, 3) is False:
            self.fail(f'Failed to invoke power event S4')
        logging.info("Successfully performed power event S4")

        # Check the persistence of apply color depth and format in previous step
        self.check_depth_and_format_persistence(self.__class__.panel_props_dict)

        # Storing color depth and format to check the persistence of apply color depth and format later
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    Bpc_Encoding_caps = BpcEncoding()
                    Bpc_Encoding_caps.Bpc = default_bpc
                    Bpc_Encoding_caps.Encoding = default_encoding
                    Bpc_Encoding_caps.default_encoding = default_encoding
                    self.__class__.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

        user_msg = "[Expectation]:No TDR/Artifacts should be observed" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No TDR/Artifacts was observed")

    ##
    # @brief This step reboots the system
    # @return None
    def test_15_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        logging.info("Rebooting the system")
        alert.info("Rebooting the system. Rerun same commandline once booted to Desktop to continue the test")

        data = {'panel_props_dict': self.__class__.panel_props_dict,
                'is_dock_planned': self.__class__.is_dock_planned,
                'initial_panel_props_dict': self.__class__.initial_panel_props_dict}
        if reboot_helper.reboot(self, 'test_16_step', data=data) is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief This step disables the HDR from the setting for both the panel.
    # @return None
    def test_16_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        logging.info("Successfully applied power event S5")
        data = reboot_helper._get_reboot_data()
        self.__class__.panel_props_dict = data['panel_props_dict']
        self.__class__.is_dock_planned = data['is_dock_planned']
        self.__class__.initial_panel_props_dict = data['initial_panel_props_dict']

        # Check the persistence of apply color depth and format in previous step
        self.check_depth_and_format_persistence(self.__class__.panel_props_dict)

        user_msg = "[Expectation]:No TDR/Artifacts should be observed" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No TDR/Artifacts was observed")

        logging.info("Disabling HDR for both the panels")
        alert.info("Disabling HDR for both the panels")
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
            alert.info("Failed to disable HDR on both the panels")
            logging.error("Disabling HDR failed")
            alert.info("Step to be performed by user manually. \n Disable HDR on all supported panel "
                       "manually. Waiting for 2mins")
            time.sleep(120)

        alert.info("Successfully disabled HDR")
        logging.info("Successfully disabled HDR")

    ##
    # @brief This step switches to higher BPC combination on both the panels.
    # @return None
    def test_17_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        self.__class__.bpc_list, max_bpc_supported = self.prepare_bpc_list(self.__class__.context_args)
        # Switch to higher BPC combination on both the panel
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    alert.info(f"Setting color depth to max BPC supported by {panel.connector_port_type}. No "
                               f"TDR/Artifacts should be observed")
                    logging.info(f"Setting color depth to max BPC supported by {panel.connector_port_type}.")
                    if not set_bpc_encoding(panel.display_and_adapterInfo, max_bpc_supported[panel.connector_port_type],
                                            default_encoding, adapter.platform_type, panel.is_lfp):
                        alert.info(f"Failed to set max BPC supported by {panel.connector_port_type}")
                        self.fail(f"Fail: Failed to set max BPC supported by {panel.connector_port_type}")
                    alert.info(f"Successfully set max BPC supported by {panel.connector_port_type}")
                    logging.info(f"Successfully set max BPC supported by {panel.connector_port_type}")

        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    alert.info(f"Setting color depth to default for {panel.connector_port_type}. No TDR/Artifacts "
                               f"should be observed")
                    logging.info(f"Setting color depth to default for {panel.connector_port_type}.")
                    if not set_bpc_encoding(panel.display_and_adapterInfo, default_bpc,
                                            default_encoding, adapter.platform_type, panel.is_lfp):
                        alert.info(f"Failed to set default bpc and encoding for {panel.connector_port_type}")
                        logging.error(
                            f"Fail: Failed to set the override bpc and encoding for {panel.connector_port_type}")
                    alert.info(f"Successfully set default bpc and encoding for {panel.connector_port_type}")
                    logging.info(f"Successfully set default bpc and encoding for {panel.connector_port_type}")

                    user_msg = "[Expectation]:No TDR/Artifacts should be observed" \
                               "\n[CONFIRM]:Enter yes if expectation met, else enter no"
                    result = alert.confirm(user_msg)
                    if not result:
                        msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                        logging.error(f"User observations: {msg['Message']}")
                    else:
                        logging.info("No TDR/Artifacts was observed")

        # Checking persistence of apply color depth and format with the ones in step01
        self.check_depth_and_format_persistence(self.__class__.initial_panel_props_dict)

    ##
    # @brief This step sets the Gradient image as background.
    # @return None
    def test_18_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        alert.info("Setting gradient pattern image as background. Background should get changed")
        logging.info("Setting gradient pattern image as background")
        desktop_img_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "Color\Lace\Images\gradient_pattern.png")
        window_helper.set_image_as_desktop_background(desktop_img_path)

        user_msg = "[Expectation]:Background should get changed." \
                   "[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Background changed to gradient pattern image.")

    ##
    # @brief This step enables HDR
    # @return None
    def test_19_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        logging.info("Enabling HDR on both the displays")
        alert.info("Enabling HDR on both the displays")
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            alert.info("Failed to enable HDR")
            logging.error("Enabling HDR failed")
            alert.info("Step to be performed by user manually. \n Enable HDR on all supported panel "
                       "manually. Waiting for 2mins")
            time.sleep(120)

        logging.info("Enabled HDR on both the displays")
        alert.info("Enabled HDR on both the displays")

    ##
    # @brief This step disables HDR
    # @return None
    def test_20_step(self):
        if self.__class__.is_dock_planned:
            self.skipTest("Test is planned with dock.")

        # Switch to higher BPC on both the displays
        self.__class__.bpc_list, max_bpc_supported = self.prepare_bpc_list(self.__class__.context_args)

        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    alert.info(f"Setting color depth to max BPC supported by {panel.connector_port_type}. No "
                               f"TDR/Artifacts should be observed")
                    logging.info(f"Setting color depth to max BPC supported by {panel.connector_port_type}.")
                    if not set_bpc_encoding(panel.display_and_adapterInfo, max_bpc_supported[panel.connector_port_type],
                                            default_encoding, adapter.platform_type, panel.is_lfp):
                        alert.info(f"Failed to set max BPC supported by {panel.connector_port_type}")
                        self.fail(f"Fail: Failed to set max BPC supported by {panel.connector_port_type}")
                    alert.info(f"Successfully set max BPC supported by {panel.connector_port_type}")
                    logging.info(f"Successfully set max BPC supported by {panel.connector_port_type}")

                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)

                    # Storing encoding and BPC to check persistence later
                    Bpc_Encoding_caps = BpcEncoding()
                    Bpc_Encoding_caps.Bpc = default_bpc
                    Bpc_Encoding_caps.Encoding = default_encoding
                    Bpc_Encoding_caps.default_encoding = default_encoding
                    self.__class__.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

        logging.info("Disabling HDR on both panels")
        alert.info("Disabling HDR on both panels. No TDR/Artifacts should be observed")
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
            alert.info("Disabling HDR failed")
            logging.error("Disabling HDR on EFP failed")
            alert.info("Step to be performed by user manually. \n Disable HDR on all supported panel "
                       "manually. Waiting for 2mins")
            time.sleep(120)

        alert.info("Disabled HDR successfully")

        user_msg = "[Expectation]:No TDR/Artifacts should be observed" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No TDR/Artifacts was observed")

        # Check the persistence of apply color depth and format
        self.check_depth_and_format_persistence(self.__class__.panel_props_dict)

    ##
    # @brief This step connects dock to system if planned and apply extended mode
    # @return None
    def test_21_step(self):
        if not self.__class__.is_dock_planned:
            self.skipTest("Test is not planned with dock.")

        user_msg = ("Note: Step to be done by user manually."
                    "\nBoot with VNC connected."
                    "\nConnect the external display to MST dongle as planned in the grid. Do not connect dongle to "
                    "system."
                    "[CONFIRM]:Enter yes once performed above step, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Connected external display to MST dongle as planned in the grid")

        user_msg = "Note: Step to be done by user manually.\nConnect the dongle to the system." \
                   "[CONFIRM]:Enter yes once performed above step, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Connected dongle to the system")
        time.sleep(2)

        enum_port_list = []
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        if enumerated_display.Count > 0:
            for index in range(0, enumerated_display.Count):
                enum_port_list.append(
                    str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))

            if len(enum_port_list) == 1:
                status = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE,
                                                                                    enum_port_list)
            else:
                status = self.__class__.display_config.set_display_configuration_ex(enum.EXTENDED, enum_port_list)

            if not status:
                alert.info("Set display config failed.")
                self.fail("Set display config failed")
            alert.info("Successfully set display config")
        else:
            alert.info("Fail: Enumerated display count is 0")
            logging.error("Enumerated display count is 0")

        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and not panel.is_lfp:
                    native_mode = self.__class__.display_config.get_native_mode(panel.target_id)
                    if native_mode is None:
                        alert.info(f"Failed to get native mode for {panel.target_id}")
                        self.fail(f"Failed to get native mode for {panel.target_id}")

                    current_mode = self.__class__.display_config.get_current_mode(panel.target_id)
                    current_mode.HzRes = native_mode.hActive
                    current_mode.VtRes = native_mode.vActive
                    current_mode.refreshRate = native_mode.refreshRate
                    alert.info("Applying native mode on external display")
                    logging.info("Applying native mode on external display")

                    if not self.__class__.display_config.set_mode(current_mode):
                        alert.info(f"Failed to set native mode for {panel.target_id}")
                        self.fail(f"Failed to set native mode for {panel.target_id}")

                    alert.info("Successfully Set native mode for external panel")
                    logging.info("Successfully Set native mode for external panel")

        # In display advance setting page, check the YUV/YCBCR as color format/encoding should be available.
        if not self.is_yuv_color_format_supported():
            alert.info("Fail: External panel doesn't support YUV color format")
            self.fail("External panel doesn't support YUV color format")
        else:
            logging.info("External panel supports YUV color format")

    ##
    # @brief This step performs power event CS/S3 if dock is planned
    # @return None
    def test_22_step(self):
        if not self.__class__.is_dock_planned:
            self.skipTest("Test is not planned with dock.")

        logging.info("Performing power event CS/S3")
        alert.info("Performing power event CS/S3. No TDR/Artifacts should be observed")
        time.sleep(2)

        if self.__class__.is_cs_supported:
            if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.CS, 3) is False:
                self.fail(f'Failed to invoke power event CS')
        else:
            if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.S3, 3) is False:
                self.fail(f'Failed to invoke power event S3')

        logging.info("Successfully performed power event CS/S3")

        user_msg = "[Expectation]:No TDR/Artifacts should be observed" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No TDR/Artifacts was observed")

        # In display advance setting page, check the YUV/YCBCR as color format/encoding should be available.
        if not self.is_yuv_color_format_supported():
            alert.info("Fail: External panel doesn't support YUV color format")
            self.fail("External panel doesn't support YUV color format")
        else:
            logging.info("External panel supports YUV color format")

    ##
    # @brief This step performs power event S4 if dock is planned
    # @return None
    def test_23_step(self):
        if not self.__class__.is_dock_planned:
            self.skipTest("Test is not planned with dock.")

        alert.info("Performing power event S4. No TDR/Artifacts should be observed")
        logging.info("Performing power event S4")
        time.sleep(2)
        if self.__class__.display_pwr.invoke_power_event(display_power.PowerEvent.S4, 3) is False:
            self.fail(f'Failed to invoke power event S4')
        logging.info("Successfully performed power event S4")

        user_msg = "[Expectation]:No TDR/Artifacts should be observed" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No TDR/Artifacts was observed")

        # In display advance setting page, check the YUV/YCBCR as color format/encoding should be available.
        if not self.is_yuv_color_format_supported():
            alert.info("Fail: External panel doesn't support YUV color format")
            self.fail("External panel doesn't support YUV color format")
        else:
            logging.info("External panel supports YUV color format")

    ##
    # @brief This step unplugs/plugs MST dongle if dock is planned
    # @return None
    def test_24_step(self):
        if not self.__class__.is_dock_planned:
            self.skipTest("Test is not planned with dock.")

        logging.info("Unplug/plug of MST dongle")

        user_msg = ("\n Note: Step to be done by user manually.[Expectation]: Unplug the MST dongle where EFP is "
                    "connected. No TDR/Artifacts should be observed"
                    "\n[CONFIRM]: Enter Yes if expectations met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Unplugged MST dongle")

        user_msg = "[Expectation]:No TDR/Artifacts should be observed" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No TDR/Artifacts was observed")

        user_msg = ("Note: Step to be done by user manually.\n[Expectation]: Plug the MST dongle with EFP connected. "
                    "No TDR/Artifacts should be observed"
                    "\n[CONFIRM]: Enter Yes if expectations met, else enter No")
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("Plugged MST dongle")

        user_msg = "[Expectation]:No TDR/Artifacts should be observed" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No TDR/Artifacts was observed")

        # In display advance setting page, check the YUV/YCBCR as color format/encoding should be available.
        if not self.is_yuv_color_format_supported():
            alert.info("Fail:External panel doesn't support YUV color format")
            self.fail("External panel doesn't support YUV color format")
        else:
            logging.info("External panel supports YUV color format")

    ##
    # @brief This step reboots the system if dock is planned
    # @return None
    def test_25_step(self):
        if not self.__class__.is_dock_planned:
            self.skipTest("Test is not planned with dock.")

        logging.info("Rebooting the system")
        alert.info("Rebooting the system. Rerun same commandline once booted to Desktop to continue the test. No "
                   "TDR/Artifacts should be observed")
        if reboot_helper.reboot(self, 'verify_post_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief This step verifies color format post reboot if dock is planned
    # @return None
    def verify_post_reboot(self):
        user_msg = "[Expectation]:No TDR/Artifacts should be observed" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
        else:
            logging.info("No TDR/Artifacts was observed")

        # In display advance setting page, check the YUV/YCBCR as color format/encoding should be available.
        if not self.is_yuv_color_format_supported():
            alert.info("Fail:External panel doesn't support YUV color format")
            self.fail("External panel doesn't support YUV color format")
        else:
            logging.info("External panel supports YUV color format")

    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass

    ##
    # @brief        This method checks if given bpc is supported by all the panels
    # @param[in]    bpc: str
    # @param[in]    bpc_list: bpc_list is a list of list(each panel's supported bpc)
    # @return       is_bpc_supported : bool. Return True if all panels support bpc_value, else False
    def is_bpc_supported_by_all_panels(self, bpc, bpc_list):
        is_bpc_supported = False
        for key, value in bpc_list.items():
            if bpc in bpc_list[key]:
                is_bpc_supported = True
            else:
                return False
        return is_bpc_supported

    ##
    # @brief        This method prepares list of list(each panel's supported bpc)
    # @param[in]    context_args: Context Class object
    # @return       bpc_list: bpc_list is a list of list(each panel's supported bpc)
    # @return       bpc_list: max_bpc_supported is a dictionary having maximum BPC supported by panel
    def prepare_bpc_list(self, context_args):
        # bpc_list is a dictionary of list(each panel's supported bpc)
        bpc_list = {}
        # max_bpc_supported is a dictionary having maximum BPC supported by panel.
        max_bpc_supported = {}

        for gfx_index, adapter in context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)

                    bpc_of_panel = []
                    for index in range(len(combo_bpc_encoding)):
                        bpc = str(combo_bpc_encoding[index][0])
                        if bpc not in bpc_of_panel:
                            bpc_of_panel.append(bpc)
                    bpc_list[panel.connector_port_type] = bpc_of_panel

                    if 'BPC12' in bpc_of_panel:
                        max_bpc_supported[panel.connector_port_type] = 'BPC12'
                    elif 'BPC10' in bpc_of_panel:
                        max_bpc_supported[panel.connector_port_type] = 'BPC10'
                    else:
                        max_bpc_supported[panel.connector_port_type] = 'BPC8'
        return bpc_list, max_bpc_supported

    ##
    # @brief        This method prepares list of list(each panel's supported bpc)
    # @param[in]    None
    # @return       is_yuv_format: bool, return True if encoding is YUV else False
    def is_yuv_color_format_supported(self):
        is_yuv_format = False
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and not panel.is_lfp:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    expected_encoding = ["YCBCR422", "YCBCR444", "YCBCR420"]
                    for encoding in expected_encoding:
                        if hdr_utility.verify_pixel_encoding(gfx_index, adapter.platform, plane_id, panel.pipe,
                                                             AviEncodingMode[encoding].value):
                            is_yuv_format = True
        return is_yuv_format

    ##
    # @brief    This method checks the persistence of apply color depth and format
    # @param[in]  panel_props_dict: A dictionary of all the properties related to the displays passed from
    #             command line. This dictionary have a tuple of gfx_index and connector_port_type as key
    #             and the value contains tuple of bpc and encoding BpcEncoding
    #             (Bpc='BPC_Value', Encoding='Encoding_Value')
    # @return     None
    def check_depth_and_format_persistence(self, panel_props_dict):
        # Check the persistence of apply color depth and format in previous step
        for gfx_index, adapter in self.__class__.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo, adapter.platform_type)
                    if (panel_props_dict[adapter.gfx_index, panel.connector_port_type].Encoding == default_encoding
                            and panel_props_dict[adapter.gfx_index, panel.connector_port_type].Bpc == default_bpc):
                        logging.info(f"Persistence of color depth and format is met for {panel.connector_port_type}")
                    else:
                        alert.info(f"Persistence of color depth and format is not met for {panel.connector_port_type}")
                        self.fail(f"Persistence of color depth and format is not met for {panel.connector_port_type}")

    ##
    # @brief        Helper function to prepare parameters required by the test
    # @param[in]    cmd_line_param - command line arguments from which parameters such as
    #               scenario, topology, required displays are parsed and prepared
    # @return        test_params - test param object of type CmdLineParams
    def parse_param_from_command_line(self, cmd_line_param):
        test_params = context.CmdLineParams()
        for index in range(0, len(cmd_line_param)):
            for key, value in cmd_line_param[index].items():
                for custom_key, custom_value in self.__class__.custom_tags.items():
                    test_params.test_custom_tags[custom_key] = cmd_line_param[index][custom_key.strip('-')]
                test_params.topology = eval("enum.%s" % (cmd_line_param[index]['CONFIG']))
                test_params.file_name = cmd_line_param[index]['FILENAME']
                test_params.log_level = cmd_line_param[index]['LOGLEVEL']
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        disp_details_obj = context.CmdLineDisplayAttributes(
                            index=value['index'], connector_port=value['connector_port'], edid_name=value['edid_name'],
                            dpcd_name=value['dpcd_name'], panel_index=value['panel_index'], is_lfp=value['is_lfp'],
                            connector_port_type=value['connector_port_type'], gfx_index=value['gfx_index'].lower())
                        test_params.display_details.append(disp_details_obj)
        return test_params


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('IgccOverrideFeatureMstPersistenceScenario2Displays'))
    TestEnvironment.cleanup(outcome)
