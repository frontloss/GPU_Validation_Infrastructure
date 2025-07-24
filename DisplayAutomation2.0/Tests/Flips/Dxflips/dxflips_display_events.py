##
# @file         dxflips_display_events.py
# @brief        Test to verify Async flips related features functionality with app running during different display events.
#               Test consists of below scenarios:
#                   * Hotplug and unplug of displays
#                   * Display switch
#                   * S3/S4 power events
#                   * Display driver restart
#                   * Different mode switch
# @author       Sunaina Ashok

import itertools
import logging
import sys
import time
import unittest

from Libs.Core import display_essential, display_power
from Libs.Core import enum, winkb_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Tests.Flips import flip_helper
from Tests.Flips.Dxflips import dxflips_base


##
# @brief    Contains test functions to verify Speedframe with app running during different display events
class DxflipsDisplayEvents(dxflips_base.DxflipsBase):

    ##
    # @brief        Test function to verify Speedframe during hotplug and unplug while app is running
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') != "HOTPLUG_UNPLUG",
                     "Skip the test step as the action type is not hotplug unplug")
    # @endcond
    def test_01_hotplug_unplug(self):

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flip_helper.start_etl_capture("Before_hotplug_unplug_scenario") is False:
            self.fail("Failed to start ETL capture")

        if self.app == "FLIPAT" or self.app == "DOTA":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None

        ##
        # Open app and play it in maximized mode, by default flip type will be async
        flip_helper.play_app(self.app, True, fps_pattern, fps_pattern2)

        ##
        # The opened app will play for 1 minute
        time.sleep(60)

        for index in range(0, 10):
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.is_lfp is False and panel.connector_port_type != "VIRTUALDISPLAY":
                        if self.unplug_display(adapter.adapter_info, panel.connector_port_type, False,
                                               panel.port_type):
                            logging.info(f"Unplugged display {panel.port_type}")
                        else:
                            flip_helper.report_to_gdhm(self.feature, f"Failed to unplug display {panel.port_type}",
                                                       driver_bug=False)
                            self.fail(f"Failed to unplug display {panel.port_type}")
            time.sleep(5)

            ##
            # plug the display
            self.config.get_all_gfx_adapter_details()
            display_details_list = self.context_args.test.cmd_params.display_details
            self.plug_display(display_details_list)

        ##
        # Close the app
        flip_helper.close_app(self.app)

        logging.info(flip_helper.getStepInfo() + "Closed {0} App".format(self.app))

        ##
        # Stop ETL Trace
        etl_file = flip_helper.stop_etl_capture("After_hotplug_unplug_scenario")

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break

    ##
    # @brief        Test function to verify Speedframe during display switch while video is running
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') != "DISPLAY_SWITCH",
                     "Skip the test step as the action type is not display switch")
    # @endcond
    def test_02_display_switch(self):
        display_list = []
        config_list = []

        ##
        # Get enumerated display info
        self.config.get_enumerated_display_info()

        ##
        # Topology list to apply various configurations on the displays connected
        topology_list = [enum.SINGLE, enum.CLONE, enum.EXTENDED]

        ##
        # Get display details
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                display_list.append(panel.display_and_adapterInfo)

        ##
        # Creating a configuration list of various topologies and the displays connected
        # ex: SINGLE Disp1, CLONE Disp1+Disp 2, SINGLE Disp2, ...
        for i in range(2, len(display_list) + 1):
            for subset in itertools.permutations(display_list, i):
                for j in range(1, len(topology_list)):
                    config_list.append((topology_list[0], [subset[0]]))
                    config_list.append((topology_list[j], list(subset)))

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flip_helper.start_etl_capture("Before_display_switch_scenario") is False:
            self.fail("Failed to start ETL capture")

        if self.app == "FLIPAT" or self.app == "DOTA":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None
        ##
        # Open app and play it in maximized mode, by default flip type will be async
        flip_helper.play_app(self.app, False, fps_pattern, fps_pattern2)

        ##
        # The opened app will play for 1 minute
        time.sleep(60)

        ##
        # Applying each configuration across the displays connected
        for each_config in range(0, len(config_list)):
            if self.config.set_display_configuration_ex(config_list[each_config][0],
                                                        config_list[each_config][1]) is True:
                logging.info("Successfully applied display configuration {}".format(
                    DisplayConfigTopology(config_list[each_config][0]).name, ))

                # Wait for 10 seconds after display switch
                time.sleep(10)

            else:
                flip_helper.report_to_gdhm(self.feature,
                                           f"Failed to display configuration {DisplayConfigTopology(config_list[each_config][0]).name, config_list[each_config][1]}")
                self.fail("Failed to display configuration {}".format(
                    DisplayConfigTopology(config_list[each_config][0]).name, ))

        ##
        # Close the app
        flip_helper.close_app(self.app)

        logging.info(flip_helper.getStepInfo() + "Closed {0} App".format(self.app))

        ##
        # Stop ETL capture
        etl_file = flip_helper.stop_etl_capture("After_display_switch_scenario")

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

    ##
    # @brief        Test function to verify Speedframe during power events while app is running.
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') not in ["POWER_EVENT_S3", "POWER_EVENT_S4"],
                     "Skip the test step as the action type is not power event S3/S4")
    # @endcond
    def test_03_power_events(self):
        disp_power = display_power.DisplayPower()

        power_state_dict = {
            "POWER_EVENT_S3": display_power.PowerEvent.S3, "POWER_EVENT_S4": display_power.PowerEvent.S4}

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flip_helper.start_etl_capture("Before_power_event_scenario") is False:
            self.fail("Failed to start ETL capture")

        if self.app == "FLIPAT" or self.app == "DOTA":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None

        ##
        # Open app and play it in maximized mode, by default flip type will be async
        flip_helper.play_app(self.app, True, fps_pattern, fps_pattern2)

        ##
        # The opened app will play for 1 minute
        time.sleep(60)

        ##
        # Invoke power event
        if disp_power.invoke_power_event(power_state_dict[self.scenario], 60) is False:
            flip_helper.report_to_gdhm(self.feature, f"Failed to invoke power event {self.scenario}",
                                       driver_bug=False)
            self.fail("Failed to invoke power event {}".format(power_state_dict[self.scenario]))
        else:
            logging.info("Power event {} success".format(power_state_dict[self.scenario]))

        ##
        # Wait for 10 seconds after power event
        time.sleep(10)

        ##
        # Close the  app
        flip_helper.close_app(self.app)

        logging.info(flip_helper.getStepInfo() + "Closed {0} App".format(self.app))

        ##
        # Stop ETL Trace
        etl_file = flip_helper.stop_etl_capture("After_power_event_scenario")

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break

    ##
    # @brief        Test function to verify TDR/BSOD when Enable and disable driver is done while app is running
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') != "RESTART_DRIVER",
                     "Skip the  test step as the action type is not Restart driver")
    # @endcond
    def test_04_restart_display_driver(self):
        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flip_helper.start_etl_capture("Before_driver_restart_scenario") is False:
            self.fail("Failed to start ETL capture")

        if self.app == "FLIPAT" or self.app == "DOTA":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None

        ##
        # Open app and play it in maximized mode, by default flip type will be async
        flip_helper.play_app(self.app, False, fps_pattern, fps_pattern2)

        ##
        # The opened app will play for 30 seconds
        time.sleep(30)

        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail("Failed to restart display driver")
        else:
            logging.info("Successfully restarted display driver")

        ##
        # Wait for 10 seconds after display driver restart
        time.sleep(10)

        ##
        # Close the app
        flip_helper.close_app(self.app)

        logging.info(flip_helper.getStepInfo() + "Closed {0} App".format(self.app))

        ##
        # Stop ETL capture
        etl_file = flip_helper.stop_etl_capture("After_driver_restart_scenario")

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break

    ##
    # @brief        Test function to verify Speedframe functionality during mode switch while app is running.
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') != "MODE_SWITCH",
                     "Skip the test step as the action type is not mode switch")
    # @endcond
    def test_05_mode_switch(self):
        target_id_list = []

        ##
        # fetch the display configuration of all the displays connected
        display_info = self.config.get_all_display_configuration()

        ##
        # target_id_list is a list of all the target_ids of the displays connected
        for displays in range(display_info.numberOfDisplays):
            target_id_list.append(display_info.displayPathInfo[displays].targetId)

        ##
        # Get enumerated display info
        enumerated_displays = self.config.get_enumerated_display_info()

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flip_helper.start_etl_capture("Before_resolution_switch_scenario") is False:
            self.fail("Failed to start ETL capture")

        if self.app == "FLIPAT" or self.app == "DOTA":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None

        ##
        # Open app and play it in maximized mode, by default flip type will be async
        flip_helper.play_app(self.app, False, fps_pattern, fps_pattern2)

        ##
        # fetch all the modes supported by each of the displays connected
        supported_modes = self.config.get_all_supported_modes(target_id_list)
        for key, values in supported_modes.items():
            for mode in values:
                logging.info("Applying Display mode {}".format(mode.to_string(enumerated_displays)))
                ##
                # set all the supported modes
                self.config.set_display_mode([mode])

        ##
        # Close the app
        flip_helper.close_app(self.app)

        logging.info(flip_helper.getStepInfo() + "Closed {0} App".format(self.app))

        ##
        # Stop ETL capture
        etl_file = flip_helper.stop_etl_capture("After_resolution_switch_scenario")

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test Purpose: Test to verify Async flip related feature functionality while running the application during different display events")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)