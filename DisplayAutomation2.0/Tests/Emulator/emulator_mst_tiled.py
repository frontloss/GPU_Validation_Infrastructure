#######################################################################################################################
# @file         emulator_mst_tiled.py
# @section      Tests
# @brief        Contains test cases to plug/unplug mst tiled display along with power events S3 and S4
# @details      Test Scenario:
#                   1. Plug all mst displays and verify tiled mode.Then unplug and plug back each mst display and verify
#                      tiled mode
#                   2. Verify Tiled mode for each of the 3 power event scenarios for S3 power state
#                   3. Verify Tiled mode for each of the 3 power event scenarios for S4 power state
# @author       Praburaj Krishnan
#######################################################################################################################
import logging
import time
import unittest
from typing import List

from Libs.Core import display_power, enum
from Libs.Core.test_env import test_environment

from Tests.Emulator.emulator_test_base import EmulatorTestBase
from Tests.PowerCons.Modules import common


##
# @brief        This class contains 3 tests, one to verify tiled mode for plug/unplug mst displays and other 2
#               tests to verify tiled mode for each of the 3 power event scenarios, for each power state S3 and S4
class TiledPlugUnplugWithPowerEvents(EmulatorTestBase):
    mst_tiled_dp_port_list: List[str] = []

    ##
    # @brief        Private Member Function to verify the target id's of connected mst displays before and after
    #               invoking power event is/are same, if same then verify the tiled mode
    # @param[in]    power_state: enum
    #                   Enum for mentioned power state
    # @return       None
    def _plug_unplug_with_power_event_scenario_1(self, power_state: display_power.PowerEvent, name: str) -> None:
        cls = TiledPlugUnplugWithPowerEvents

        target_id_dict_before_power_event = cls.get_port_target_id_dict(cls.mst_tiled_dp_port_list)
        target_id_list_before_power_event = cls.get_target_id_list_from_dict(target_id_dict_before_power_event)

        is_success = cls.display_power.invoke_power_event(power_state)
        self.assertTrue(is_success, "[Test Issue] - Failed To Invoke Power Event: {}".format(name))

        target_id_dict_after_power_event = cls.get_port_target_id_dict(cls.mst_tiled_dp_port_list)
        target_id_list_after_power_event = cls.get_target_id_list_from_dict(target_id_dict_after_power_event)

        self.assertEqual(target_id_list_before_power_event, target_id_list_after_power_event,
                         "Target ids are different before and after power event")

        is_success = cls.verify_tiled_mode(target_id_list_after_power_event)
        self.assertTrue(is_success, "[Driver Issue] - Tiled Mode Verification Failed")

        logging.info('Successfully Verified Tiled Modes for; {}'.format(cls.mst_tiled_dp_port_list))

    ##
    # @brief        Private Member Function to verify that no target id/id's is/are detected post the power event that
    #               is invoked after low power unplug of the displays
    # @param[in]    power_state: enum
    #                   Enum for mentioned power state
    # @return       None
    def _plug_unplug_with_power_event_scenario_2(self, power_state: display_power.PowerEvent, name: str) -> None:
        cls = TiledPlugUnplugWithPowerEvents

        target_id_dict_before_power_event = cls.get_port_target_id_dict(cls.mst_tiled_dp_port_list)
        logging.debug("Target id dict before power event: {}".format(target_id_dict_before_power_event))

        for port, target_id_list in target_id_dict_before_power_event.items():
            cls.she_utility.unplug_mst_tiled_display('gfx_0', port, 30)

        is_success = cls.display_power.invoke_power_event(power_state)
        self.assertTrue(is_success, "[Test Issue] - Failed To Invoke Power Event: {}".format(name))

        target_id_dict_after_power_event = cls.get_port_target_id_dict(cls.mst_tiled_dp_port_list)
        logging.debug('Target id dict after power event: {}'.format(target_id_dict_after_power_event))

        is_success = bool(target_id_dict_after_power_event)
        self.assertFalse(is_success, "Tiled Target id/ids is/are detected after power event")
        logging.info("All tiled displays are unplugged successfully")

    ##
    # @brief        Private Member Function to verify tiled mode post the power event that is invoked after plugging
    #               back each mst display
    # @param[in]    power_state: enum
    #                   Enum for mentioned power state
    # @return       None
    def _plug_unplug_with_power_event_scenario_3(self, power_state: display_power.PowerEvent, name: str) -> None:
        tiled_port_list = []
        cls = TiledPlugUnplugWithPowerEvents

        for port, tiled_panel_info in cls.mst_port_panel_dict.items():
            tiled_port_list.append(port)
            cls.she_utility.plug_mst_tiled_display('gfx_0', port, tiled_panel_info, 30)

            enumerated_displays = cls.display_config.get_enumerated_display_info()
            logging.info("Enumerated Displays: {}".format(enumerated_displays.to_string()))

            is_success = cls.display_power.invoke_power_event(power_state)
            self.assertTrue(is_success, "[Test Issue] - Failed To Invoke Power Event: {}".format(name))

            time.sleep(60)  # Wait for sometime before the display plugged in low power actually gets reflected.

            is_success = cls.apply_config(tiled_port_list)
            assert is_success, "[Driver Issue] - Applying Display Config Failed"

            port_target_id_dict = cls.get_port_target_id_dict(tiled_port_list)
            tiled_target_id_list = cls.get_target_id_list_from_dict(port_target_id_dict)

            is_success = cls.verify_tiled_mode(tiled_target_id_list)
            self.assertTrue(is_success, "[Driver Issue] - Tiled Mode Verification Failed")

            logging.info('Successfully Verified Tiled Modes for: {}'.format(tiled_port_list))

    ##
    # @brief        This test plugs all the mst displays, applies the suitable configuration(SINGLE/EXTENDED) and verify
    #               the Tiled mode.Then for each mst display, unplugs and plugs back the display(All displays connected
    #               should be detected and displays should come up with appropriate configuration without any corruption
    #               or blankout) and then verifies the Tiled mode.
    # @return       None
    # @cond
    @common.configure_test(selective=['PLUG_UNPLUG'])
    # @endcond
    def t_1_plug_unplug(self) -> None:
        cls = TiledPlugUnplugWithPowerEvents

        cls.mst_port_panel_dict = cls.emulator_command_parser.get_mst_port_panel_dict()
        cls.mst_tiled_dp_port_list = list(cls.mst_port_panel_dict.keys())

        enumerated_displays = cls.display_config.get_enumerated_display_info()
        logging.info("Enumerated Displays: {}".format(enumerated_displays.to_string()))

        for port, tiled_panel_info in cls.mst_port_panel_dict.items():
            cls.she_utility.plug_mst_tiled_display('gfx_0', port, tiled_panel_info)

        common.print_current_topology()
        enumerated_displays = cls.display_config.get_enumerated_display_info()
        logging.info("Enumerated Displays: {}".format(enumerated_displays.to_string()))

        is_success = cls.apply_config(cls.mst_tiled_dp_port_list)
        self.assertTrue(is_success, "[Driver Issue] - Applying Display Config Failed")

        port_target_id_dict = cls.get_port_target_id_dict(cls.mst_tiled_dp_port_list)
        tiled_target_id_list = cls.get_target_id_list_from_dict(port_target_id_dict)

        is_success = cls.verify_tiled_mode(tiled_target_id_list)
        self.assertTrue(is_success, "[Driver Issue] - Tiled Mode Verification Failed")
        logging.info('Successfully Verified Tiled Modes for: {}'.format(cls.mst_tiled_dp_port_list))

        for port, tiled_panel_info in cls.mst_port_panel_dict.items():
            cls.she_utility.unplug_mst_tiled_display('gfx_0', port)
            time.sleep(5)

            cls.she_utility.plug_mst_tiled_display('gfx_0', port, tiled_panel_info)

            port_target_id_dict = cls.get_port_target_id_dict([port])
            tiled_target_id_list = cls.get_target_id_list_from_dict(port_target_id_dict)

            is_success = cls.apply_config([port])
            self.assertTrue(is_success, "[Driver Issue] - Applying Display Config Failed")

            is_success = cls.verify_tiled_mode(tiled_target_id_list)
            self.assertTrue(is_success, "[Driver Issue] - Tiled Mode Verification Failed")
            logging.info('Successfully Verified Tiled Modes for: {}'.format(cls.mst_tiled_dp_port_list))

    ##
    # @brief        This test verifies all the 3 power event scenarios for power state S3
    # @note         Power state CS should not be supported
    # @return       None
    # @cond
    @common.configure_test(selective=['S3'])
    # @endcond
    def t_2_power_event_s3(self) -> None:
        cls = TiledPlugUnplugWithPowerEvents

        if cls.display_power.is_power_state_supported(display_power.PowerEvent.CS):
            self.fail("[Planning Issue] - CS Is Supported, Hence Cannot Execute S3.")

        self._plug_unplug_with_power_event_scenario_1(display_power.PowerEvent.S3, "S3")
        self._plug_unplug_with_power_event_scenario_2(display_power.PowerEvent.S3, "S3")
        self._plug_unplug_with_power_event_scenario_3(display_power.PowerEvent.S3, "S3")

    ##
    # @brief        This test verifies all the 3 power event scenarios for power state S4
    # @return       None
    # @cond
    @common.configure_test(selective=['S4'])
    # @endcond
    def t_3_power_event_s4(self) -> None:
        self._plug_unplug_with_power_event_scenario_1(display_power.PowerEvent.S4, "S4")
        self._plug_unplug_with_power_event_scenario_2(display_power.PowerEvent.S4, "S4")
        self._plug_unplug_with_power_event_scenario_3(display_power.PowerEvent.S4, "S4")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TiledPlugUnplugWithPowerEvents))
    test_environment.TestEnvironment.cleanup(test_result)
