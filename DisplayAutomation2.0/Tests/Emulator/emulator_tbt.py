#######################################################################################################################
# @file         emulator_tbt.py
# @section      Tests
# @brief        Contains test cases that covers TBT over subscription, TBT Alt Mode Switching and TBT + Empty dongle
#               scenarios.
# @author       Praburaj Krishnan
#######################################################################################################################
from __future__ import annotations

import logging
import os
import time
from typing import List
from unittest import TextTestRunner

from Libs.Core import display_utility, display_essential
from Libs.Core.display_config import display_config_enums, display_config
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.display_config.display_config_struct import EnumeratedDisplaysEx, DisplayInfo
from Libs.Core import display_power
from Libs.Core.hw_emu.emulator_helper import HubDisplayInfo
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.test_env.test_context import TestContext
from Libs.Core.display_config.display_config_struct import DisplayMode

from Tests.Emulator import emulator_test_base
from Tests.Emulator.emulator_test_base import EmulatorTestBase
from Tests.PowerCons.Modules import common

from Libs.Core import enum


##
# @brief        Contains different test scenarios for TBT testing. Each of the test case can be invoked separately
#               by specifying the test scenario name in the command line by using selective tag.
class ThunderBoltTests(EmulatorTestBase):
    tbt_plug_failure_template = "Hot Plug Issued to Port={} Gfx Index={} Failed."
    tbt_plug_success_template = "Hot Plug Issued to Port={} Gfx Index={} Succeeded."
    tbt_unplug_failure_template = "Hot Un-plug Issued to Port={} Gfx Index={} Failed."
    tbt_unplug_success_template = "Hot Un-plug Issued to Port={} Gfx Index={} Succeeded."

    ##
    # @brief        Private Member Function to plug the displays to the TBT hub based on the command line inputs.
    # @param[in]    tbt_hub_port: str
    #                   Port name in which the TBT hub is plugged.
    # @param[in]    hub_port_display_info_list: List[HubDisplayInfo]
    #                   Contains information about the displays to be plugged to the TBT Hub.
    # @return       None
    def _plug_to_tbt_port_hub(self, tbt_hub_port: str, hub_port_display_info_list: List[HubDisplayInfo]) -> None:
        enumerated_displays = ThunderBoltTests.display_config.get_enumerated_display_info()
        logging.debug("Enumerated Displays: {}".format(enumerated_displays.to_string()))

        for hub_display_info in hub_port_display_info_list:
            is_success = self.she_utility.plug_display_to_tbt_hub('gfx_0', tbt_hub_port, hub_display_info)
            self.assertTrue(is_success, ThunderBoltTests.tbt_plug_failure_template.format(tbt_hub_port, 'gfx_0'))
            logging.info(ThunderBoltTests.tbt_plug_success_template.format(tbt_hub_port, 'gfx_0'))

        enumerated_displays = ThunderBoltTests.display_config.get_enumerated_display_info()
        logging.debug("Enumerated Displays: {}".format(enumerated_displays.to_string()))

    ##
    # @brief        Private Member Function to unplug the displays connected to the TBT hub using the command line
    #               inputs.
    # @return       None
    def _unplug_to_tbt_port_hub(self) -> None:
        enumerated_displays = ThunderBoltTests.display_config.get_enumerated_display_info()
        logging.debug("Enumerated Displays: {}".format(enumerated_displays.to_string()))

        for tbt_hub_port, hub_port_display_info_list in ThunderBoltTests.tbt_hub_port_display_info_dict.items():
            for hub_display_info in hub_port_display_info_list:
                is_success = self.she_utility.unplug_display_to_tbt_hub('gfx_0', tbt_hub_port, hub_display_info)
                self.assertTrue(is_success, ThunderBoltTests.tbt_unplug_failure_template.format(tbt_hub_port, 'gfx_0'))
                logging.info(ThunderBoltTests.tbt_unplug_success_template.format(tbt_hub_port, 'gfx_0'))

        enumerated_displays = ThunderBoltTests.display_config.get_enumerated_display_info()
        logging.debug("Enumerated Displays: {}".format(enumerated_displays.to_string()))

    ##
    # @brief        Test case to test the TBT Over Subscription Scenario.
    # @note         Link for manual procedure: https://gta.intel.com/procedures/#/procedures/TI-848944/
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["OVER_SUBSCRIPTION"])
    # @endcond
    def t_1_tbt_over_subscription(self) -> None:
        cls = ThunderBoltTests

        # Parse the command line get the TBT port and hub information
        cls.tbt_hub_port_display_info_dict = cls.emulator_command_parser.get_tbt_hub_display_info_dict()

        # Perform over subscription scenario for each of the tbt port present in the command line.
        for tbt_hub_port, hub_port_display_info_list in cls.tbt_hub_port_display_info_dict.items():
            # Plug the displays to the TBT hub.
            self._plug_to_tbt_port_hub(tbt_hub_port, hub_port_display_info_list)
            port_0, port_1 = emulator_test_base.tbt_port_pairs[common.PLATFORM_NAME][tbt_hub_port]

            # Apply Extended Config.
            is_success = cls.apply_config([port_0, port_1])
            self.assertTrue(is_success, "Set Display Configuration Failed")
            common.print_current_topology()

            # Get Panel Names of the displays plugged to TBT hub.
            panel_name_port_0_before_plug = cls.get_friendly_name('gfx_0', port_0)
            panel_name_port_1_before_plug = cls.get_friendly_name('gfx_0', port_1)

            # Get the Panel index for the display that has to be plugged to the port_1 of the TBT pair.
            port_type = "TC_TBT"
            panel_index = cls.emulator_command_parser.cmd_dict[port_1 + "_" + port_type]['panel_index']

            gfx_adapter_info = GfxAdapterInfo()
            gfx_adapter_info.gfxIndex = 'gfx_0'

            # Plug the display to port_1 of the TBT pair. This is done to see plugged display is not getting enumerated
            # since both ddi are already occupied.
            data = display_utility.get_panel_edid_dpcd_info(port=port_1, panel_index=panel_index)
            edid, dpcd = data['edid'], data['dpcd']
            edid_path = os.path.join(TestContext.panel_input_data(), 'eDP_DPSST', edid)
            dpcd_path = os.path.join(TestContext.panel_input_data(), 'eDP_DPSST', dpcd)
            cls.she_utility.plug(gfx_adapter_info, port_1, edid_path, dpcd_path, False, port_type)

            enumerated_displays = cls.display_config.get_enumerated_display_info()
            logging.debug("Enumerated Displays: {}".format(enumerated_displays.to_string()))

            # Get Panel Names of the displays plugged to TBT hub.
            panel_name_port_0_after_plug = cls.get_friendly_name('gfx_0', port_0)
            panel_name_port_1_after_plug = cls.get_friendly_name('gfx_0', port_1)

            logging.info(f"Panel Names Before Plug: {(panel_name_port_0_before_plug, panel_name_port_1_before_plug)}")
            logging.info(f"Panel Names After Plug: {(panel_name_port_0_after_plug, panel_name_port_1_after_plug)}")

            # Compare the panel names of the display before and after plug to check if the display plugged to port_1
            # of the TBT pair is enumerated. Fail if both are different.
            is_success = (panel_name_port_0_before_plug == panel_name_port_0_after_plug)
            is_success &= (panel_name_port_1_before_plug == panel_name_port_1_after_plug)
            self.assertTrue(is_success, f"[Driver Issue] - Plug to 2nd port={port_1} of the tbt "
                                        f"pair=({port_0, port_1}) is not ignored")
            logging.info(f"Plug to 2nd port={port_1} of the tbt pair=({port_0, port_1}) is ignored as expected.")

            is_success = cls.she_utility.unplug(gfx_adapter_info, port_1, False, port_type)
            self.assertTrue(is_success, "Un-plug Failed on port={}".format(port_1))
            self._unplug_to_tbt_port_hub()

    ##
    # @brief        Test case to test the TBT Alt Mode Scenario.
    # @note         Link for manual procedure: https://gta.intel.com/procedures/#/procedures/TI-848945/
    # @return       None
    # @cond
    @common.configure_test(selective=["ALT_MODE"])
    # @endcond
    def t_2_tbt_dp_alt_mode_switching(self) -> None:
        cls = ThunderBoltTests

        # Parse the command line and get the TBT port in which TBT hub is connected and displays that needs to be
        # plugged to the TBT hub
        cls.tbt_hub_port_display_info_dict = cls.emulator_command_parser.get_tbt_hub_display_info_dict()

        # Perform Alt Mode scenario for each of the tbt port present in the command line.
        for tbt_hub_port, hub_port_display_info_list in cls.tbt_hub_port_display_info_dict.items():
            # Plug the displays to the TBT hub.
            self._plug_to_tbt_port_hub(tbt_hub_port, hub_port_display_info_list)
            port_0, port_1 = emulator_test_base.tbt_port_pairs[common.PLATFORM_NAME][tbt_hub_port]

            # Apply Extended Config.
            is_success = cls.apply_config([port_0, port_1])
            self.assertTrue(is_success, "Set Display Configuration Failed")
            common.print_current_topology()

            # Unplug the display from port_0 of the TBT pair.
            self.she_utility.unplug_display_to_tbt_hub('gfx_0', port_0, hub_port_display_info_list[0])
            common.print_current_topology()

            # Check if display is enumerated after unplug from the TBT hub for port_0.
            is_display_enumerated = cls.is_displays_enumerated([port_0])
            self.assertFalse(is_display_enumerated, f"Unplugged display at port={port_0} of the tbt "
                                                    f"pair=({port_0, port_1}) is enumerated")
            logging.info(f"Unplugged display at port={port_0} of the tbt pair=({port_0, port_1}) is not enumerated")

            # Get the Panel index for the display that has to be plugged to the port_1 of the TBT pair.
            port_type = "TC_TBT"
            panel_index = cls.emulator_command_parser.cmd_dict[port_1 + "_" + port_type]['panel_index']

            gfx_adapter_info = GfxAdapterInfo()
            gfx_adapter_info.gfxIndex = 'gfx_0'

            # Plug the display to port_1 of the TBT pair. This is done to see if ddi switching is happening after unplug
            # from TBT hub.
            data = display_utility.get_panel_edid_dpcd_info(port=port_1, panel_index=panel_index)
            edid, dpcd = data['edid'], data['dpcd']
            edid_path = os.path.join(TestContext.panel_input_data(), 'eDP_DPSST', edid)
            dpcd_path = os.path.join(TestContext.panel_input_data(), 'eDP_DPSST', dpcd)
            is_success = cls.she_utility.plug(gfx_adapter_info, port_1, edid_path, dpcd_path, False, port_type)
            self.assertTrue(is_success, "Plug Failed on port={}".format(port_1))

            enumerated_displays = cls.display_config.get_enumerated_display_info()
            logging.info("Enumerated Displays: {}".format(enumerated_displays.to_string()))

            # Check if plugged displays are enumerated.
            is_displays_enumerated = cls.is_displays_enumerated([port_0, port_1])
            self.assertTrue(is_displays_enumerated, (f"Not all Panels Connected to the TBT Pair=({port_0, port_1}) are "
                                                     f"not enumerated."))
            logging.info(f"All Display Connected to the TBT Pair=({port_0, port_1}) are detected")

            # Apply Extended Config.
            is_success = cls.apply_config([port_0, port_1])
            self.assertTrue(is_success, "Set Display Configuration Failed")
            common.print_current_topology()

            is_success = cls.she_utility.unplug(gfx_adapter_info, port_1, False, port_type)
            self.assertTrue(is_success, "Un-plug Failed on port={}".format(port_1))

    ##
    # @brief        Test case to test the TBT Hub + Empty dongle Scenario.
    # @note         Link for manual procedure: https://gta.intel.com/procedures/#/procedures/TI-1229343/
    # @return       None
    # @cond
    @common.configure_test(selective=["EMPTY_DONGLE"])
    # @endcond
    def t_3_tbt_empty_dongle(self) -> None:
        cls = ThunderBoltTests

        # Parse the command line get the TBT port and hub information
        cls.tbt_hub_port_display_info_dict = cls.emulator_command_parser.get_tbt_hub_display_info_dict()

        # Check if displays are enumerated just by connecting the TBT hub and Apple MFD dongle
        is_displays_enumerated = cls.is_displays_enumerated(cls.emulator_command_parser.dp_port_list)
        self.assertFalse(is_displays_enumerated, "Displays are enumerated just by connecting empty dongle/hub")
        logging.info("No display is enumerated just by connecting empty dongle and TBT hub")

        for tbt_hub_port, hub_port_display_info_list in cls.tbt_hub_port_display_info_dict.items():
            # Plug the displays to the TBT hub.
            for hub_display_info in hub_port_display_info_list:
                is_success = self.she_utility.plug_display_to_tbt_hub('gfx_0', tbt_hub_port, hub_display_info)

                # Skipping the Plug Status Check for the 2nd Display Plugged to TBT Hub as Apple MFD dongle is
                # Connected to the 2nd port of the TBT Pair.
                if hub_display_info.port_index == 1:
                    logging.info("Skipping the Plug Status check for the 2nd display plugged to TBT Hub.")
                    continue

                self.assertTrue(is_success, ThunderBoltTests.tbt_plug_failure_template.format(tbt_hub_port, 'gfx_0'))
                logging.info(ThunderBoltTests.tbt_plug_success_template.format(tbt_hub_port, 'gfx_0'))

            # Apply Single Configuration.
            port_0, port_1 = emulator_test_base.tbt_port_pairs[common.PLATFORM_NAME][tbt_hub_port]
            is_success = cls.apply_config([port_0])
            self.assertTrue(is_success, "Set Display Configuration Failed")

            # TODO: Check if empty dongle/hub unplug is possible
            self._unplug_to_tbt_port_hub()

            # Check if displays are still enumerated after unplugging from the TBT hub.
            is_enumerated = cls.is_displays_enumerated(cls.emulator_command_parser.dp_port_list)
            self.assertFalse(is_enumerated, "Displays are enumerated after disconnecting displays from dongle/hub")
            logging.info("Displays are not enumerated after disconnecting displays from dongle/hub")

    ##
    # @brief        Test case to test the TBT two parallel HPDs from the TBT hub
    # @note         Link for manual procedure: https://gta.intel.com/procedures/#/procedures/TI-848948/
    # @return       None
    # @cond
    @common.configure_test(selective=["PARALLEL_HPD"])
    # @endcond
    def t_4_tbt_two_parallel_hpd(self) -> None:
        cls = ThunderBoltTests

        # Parse the command line get the TBT port and hub information
        cls.tbt_hub_port_display_info_dict = cls.emulator_command_parser.get_tbt_hub_display_info_dict()

        # Perform over subscription scenario for each of the tbt port present in the command line.
        for tbt_hub_port, hub_port_display_info_list in cls.tbt_hub_port_display_info_dict.items():
            # Plug the displays to the TBT hub.
            self._plug_to_tbt_port_hub(tbt_hub_port, hub_port_display_info_list)
            port_0, port_1 = emulator_test_base.tbt_port_pairs[common.PLATFORM_NAME][tbt_hub_port]

            # Apply Extended Config.
            is_success = cls.apply_config([port_0, port_1])
            self.assertTrue(is_success, "Set Display Configuration Failed")
            common.print_current_topology()

            # Restart the driver to simulate Two parallel HPDs from the TBT hub/dock.
            result, reboot_required = display_essential.restart_gfx_driver()
            time.sleep(5)

            is_displays_enumerated = cls.is_displays_enumerated([port_0, port_1])
            self.assertTrue(is_displays_enumerated, "Not all displays are enumerated after restarting display driver")

            # Apply Extended Config.
            is_success = cls.apply_config([port_0, port_1])
            self.assertTrue(is_success, "Set Display Configuration Failed")
            common.print_current_topology()

            # Applying Max mode
            port_target_id_dict = cls.get_port_target_id_dict([port_0, port_1])
            port_target_id_list = cls.get_target_id_list_from_dict(port_target_id_dict)
            res, applied_mode = cls.set_max_mode(port_target_id_list)
            if res is True:
                # for each display, check whether current mode is matching the native mode from EDID.
                for port_target_id in port_target_id_list:
                    exp_h_res, exp_v_res, exp_rr = 0, 0, 0
                    if port_target_id in applied_mode.keys():
                        exp_h_res, exp_v_res, exp_rr = applied_mode[port_target_id][0], applied_mode[port_target_id][1], applied_mode[port_target_id][2]
                    current_mode: DisplayMode = cls.display_config.get_current_mode(port_target_id)
                    actual_h_res, actual_v_res, actual_rr = current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate

                    if actual_h_res == exp_h_res and actual_v_res == exp_v_res and actual_rr == exp_rr:
                        logging.info(
                            "Current Mode [Driver Enumerated] = {0}x{1}@{2}hz and Applied Mode = "
                            "{0}x{1}@{3}hz are identical".format(
                                actual_h_res, actual_v_res, actual_rr, exp_rr
                            ))
                    else:
                        self.fail(
                            "[Driver Issue] - Current Mode [Driver Enumerated]= {}x{}@{}hz and Applied Mode = "
                            "{}x{}@{}hz are different".format(
                                actual_h_res, actual_v_res, actual_rr, exp_h_res, exp_v_res, exp_rr
                            ))
            # Verifying TBT displays after power event S3/CS
            power_state = display_power.PowerEvent.S3
            if cls.display_power.is_power_state_supported(display_power.PowerEvent.CS) is True:
                power_state = display_power.PowerEvent.CS

            is_power_event_invoked = cls.display_power.invoke_power_event(power_state, 30)
            self.assertTrue(is_power_event_invoked, f"Failed to invoke {power_state.name}")
            logging.info(f"Successfully invoked {power_state.name}")
            for connector_port in ([port_0, port_1]):
                is_display_active = display_config.is_display_active(connector_port)
                self.assertTrue(is_display_active, f"TBT Display {connector_port} is not active, "
                                                   f"after {power_state.name}")
                logging.info(f"TBT Display {connector_port} is active, after {power_state.name}")

    ##
    # @brief        A class method to get the Panel Name of the display plugged to the port.
    # @param[in]    gfx_index: str
    #                   Graphics adapter index to which the panel is connected.
    # @param[in]    port: str
    #                   Port name for which the panel name has to be retrieved.
    # @return       panel_name: str
    #                   Panel name of the display plugged to specified port.
    @classmethod
    def get_friendly_name(cls, gfx_index: str, port: str) -> str:
        panel_name = ""

        enumerated_displays: EnumeratedDisplaysEx = cls.display_config.get_enumerated_display_info()
        logging.info("Enumerated Displays: {}".format(enumerated_displays.to_string()))

        for each_display in range(enumerated_displays.Count):
            display_info: DisplayInfo = enumerated_displays.ConnectedDisplays[each_display]
            current_port_name = display_config_enums.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
            current_gfx_index = display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if (current_gfx_index == gfx_index) and (current_port_name == port):
                panel_name = display_info.FriendlyDeviceName
                break

        logging.debug("Panel name of the display connected to the port {} is {}".format(port, panel_name))
        return panel_name

    ##
    # @brief        A class method to check if the displays are enumerated for the specified ports.
    # @param[in]    dp_port_list: List[str]
    #                   List of port names to verify if displays are enumerated on those ports.
    # @return       is_enumerated: bool
    #                   Returns True if all the displays connected to the specified ports are enumerated False otherwise
    @classmethod
    def is_displays_enumerated(cls, dp_port_list) -> bool:
        port_target_id_dict = cls.get_port_target_id_dict(dp_port_list)
        is_enumerated = set(list(port_target_id_dict.keys())) == set(dp_port_list)

        logging.info('Function is_displays_enumerated status: {}'.format(is_enumerated))
        return is_enumerated


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(ThunderBoltTests))
    TestEnvironment.cleanup(test_result)
