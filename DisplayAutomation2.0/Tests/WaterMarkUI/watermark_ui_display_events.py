########################################################################################################################
# @file         watermark_ui_display_events.py
# @brief        Basic test to verify watermarks in different scenarios.
#                   * Verify Watermarks for the below scenarios
#                       1. Switch between different modes in all connected displays
#                       2. Rotate the displays in all possible combinations for all the above modes.
#                       3. Switch between different display configurations
#                       4. Hotplug unplug
#                       5. Restart Driver
#                       6. Display Power events
#                            S3 / S4
#                       7. Generate TDR
#                       8. AC/DC switch
# @author       Gopikrishnan R
########################################################################################################################

import itertools
import logging
import sys
import time
import unittest

from Libs.Core import display_essential, display_power, enum
from Libs.Core.display_power import DisplayPower, PowerEvent, PowerSource
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PlanesUI.Common import planes_ui_helper as watermark_helper
from Tests.WaterMarkUI import watermark_ui_base


##
# @brief    Contains Watermark display events tests
class WatermarkUIDisplayEvents(watermark_ui_base.WatermarkUIBase):
    ##
    # @brief        Test to verify MPO functionality during mode switch/rotate while app(s) are running.
    # @return       None
    @unittest.skipIf(watermark_helper.get_config_type('-SCENARIO') != 'MODE_SWITCH',
                     "Skip the test step as the scenario type is not mode switch")
    def test_01_mode_switch(self):
        target_id_list = self.get_target_id_list(include_inactive=True)

        ##
        # Start ETL capture
        if watermark_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # fetch all the modes supported by each of the displays connected
        supported_modes = self.config.get_all_supported_modes(target_id_list)

        for key, values in supported_modes.items():
            modes_count = len(values)
            # Trim the modes to be tested if the count is more than 30, additional logic to include all supported
            # scaling parameters in the list of modes to be tested.
            if modes_count > 30:
                temp_values = values[:10] + values[(modes_count // 2 - 5):(modes_count // 2 + 5)] + values[-10:]
                excluded_values = values[10:(modes_count // 2 - 5)] + values[(modes_count // 2 + 5): -10]
                scaling_params = list({x.scaling: 0 for x in temp_values}.keys())
                for val in excluded_values:
                    if val.scaling not in scaling_params:
                        temp_values.append(val)
                        scaling_params.append(val.scaling)
                values = temp_values

            for mode in values:
                ##
                logging.info(f"Applying display mode from test - {mode}")
                # set all the supported modes
                self.config.set_display_mode([mode], virtual_mode_set_aware=False, force_modeset=True)
                logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                    mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))
                time.sleep(10)
                if self.wm.verify_watermarks() is not True:
                    logging.error("Error Observed in watermark verification for display mode {0} X {1}"
                                  .format(mode.HzRes, mode.VtRes))
                    self.fail("Watermark verification failed for display mode {0} X {1}"
                              .format(mode.HzRes, mode.VtRes))
                else:
                    logging.info("Watermark verification passed for display mode {0} X {1}"
                                 .format(mode.HzRes, mode.VtRes))

        ##
        # Stop ETL capture
        etl_file = watermark_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

    ##
    # @brief        Test to verify MPO functionality during mode switch/rotate while app(s) are running.
    # @return       None
    @unittest.skipIf(watermark_helper.get_config_type('-SCENARIO') != 'ROTATION',
                     "Skip the test step as the scenario type is not rotation")
    def test_02_rotate(self):
        target_id_list = self.get_target_id_list(include_inactive=True)

        ##
        # Start ETL capture
        if watermark_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # fetch all the modes supported by each of the displays connected
        supported_modes = self.config.get_all_supported_modes(target_id_list)

        rotations = [enum.ROTATE_90, enum.ROTATE_180, enum.ROTATE_270, enum.ROTATE_0]

        for key, values in supported_modes.items():
            modes_count = len(values)
            values = [values[0], values[(modes_count // 2)], values[-1]]

            for mode in values:
                for rotation in rotations:
                    mode.rotation = rotation
                    ##
                    # set all the supported modes
                    self.config.set_display_mode([mode], virtual_mode_set_aware=False, force_modeset=True)
                    logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                        mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))

                    time.sleep(10)
                    if self.wm.verify_watermarks() is not True:
                        self.fail("Error Observed in watermark verification")
                    else:
                        logging.info("Watermark verification passed for rotation : {0}".format(mode.rotation))


        ##
        # Stop ETL capture
        etl_file = watermark_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

    ##
    # @brief        Test to verify MPO functionality during display switch while apps are running.
    # @return       None
    @unittest.skipIf(watermark_helper.get_config_type('-SCENARIO') != 'DISPLAY_SWITCH',
                     "Skip the test step as the scenario type is not display switch")
    def test_03_display_switch(self):
        display_list = []
        config_list = []

        ##
        # Get enumerated display info
        enumerated_displays = self.config.get_enumerated_display_info()

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
        # Start ETL capture
        if watermark_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Applying each configuration across the displays connected
        for each_config in range(0, len(config_list)):
            if watermark_helper.set_display_config(config_list[each_config][0], config_list[each_config][1]) is True:
                logging.info("Successfully applied display configuration")
                # Wait for 10 seconds after display switch
                time.sleep(10)
                if self.wm.verify_watermarks() is not True:
                    self.fail("Error Observed in watermark verification")
                else:
                    logging.info(f"Watermark verification passed post {self.scenario.lower()}")
            else:
                self.fail("Failed to display configuration")

        ##
        # Stop ETL capture
        etl_file = watermark_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

    ##
    # @brief        Test to verify watermarks for hotplug and unplug is done
    # @return       None
    @unittest.skipIf(watermark_helper.get_config_type('-SCENARIO') != 'HOTPLUG_UNPLUG',
                     "Skip the test step as the scenario type is not hotplug unplug")
    def test_04_hotplug_unplug(self):
        ##
        # Start ETL capture
        if watermark_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        for index in range(0, 10):
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.is_lfp is False and panel.connector_port_type != "VIRTUALDISPLAY":
                        if self.unplug_display(adapter.adapter_info, panel.connector_port_type, False,
                                               panel.port_type):
                            logging.info("Unplugged display {}".format(panel.port_type))
                            if self.wm.verify_watermarks() is not True:
                                self.fail("Error Observed in watermark verification")
                            else:
                                logging.info("Watermark verification passed")
                        else:
                            self.fail("Failed to unplug display {}".format(panel.port_type))

            time.sleep(5)

            ##
            # plug the display
            gfx_adapter_details = self.config.get_all_gfx_adapter_details()
            display_details_list = self.context_args.test.cmd_params.display_details
            self.plug_display(display_details_list)
            if self.wm.verify_watermarks() is not True:
                self.fail("Error Observed in watermark verification")
            else:
                logging.info(f"Watermark verification passed post {self.scenario.lower()}")

        ##
        # Stop ETL capture
        etl_file = watermark_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

    ##
    # @brief        Test to verify watermarks after restarting the driver
    # @return       None
    @unittest.skipIf(watermark_helper.get_config_type('-SCENARIO') != 'RESTART_DRIVER',
                     "Skip the  test step as the scenario type is not Restart driver")
    def test_05_restart_display_driver(self):
        ##
        # Start ETL capture
        if watermark_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        status, reboot_required = display_essential.restart_gfx_driver()

        if status is False:
            self.fail("Failed to restart display driver")
        else:
            logging.info("Successfully restarted display driver")

        if self.wm.verify_watermarks() is not True:
            self.fail("Error Observed in watermark verification")
        else:
            logging.info("Watermark verification passed post display driver restart")

        ##
        # Wait for 10 seconds after display driver restart
        time.sleep(10)

        ##
        # Stop ETL capture
        etl_file = watermark_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

    ##
    # @brief        Test to verify watermarks after power events
    # @return       None
    @unittest.skipIf(watermark_helper.get_config_type('-SCENARIO') not in ['POWER_EVENT_S3', 'POWER_EVENT_S4'],
                     "Skip the test step as the scenario type is not power event S3/S4")
    def test_06_power_events(self):
        disp_power = DisplayPower()

        power_state_dict = {
            "POWER_EVENT_S3": PowerEvent.S3, "POWER_EVENT_S4": PowerEvent.S4}

        ##
        # Start ETL capture
        if watermark_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        time.sleep(5)

        ##
        # Invoke power event
        if disp_power.invoke_power_event(power_state_dict[self.scenario], 60) is False:
            self.fail("Failed to invoke power event {}".format(power_state_dict[self.scenario]))
        else:
            logging.info("Power event {} success".format(power_state_dict[self.scenario]))

        time.sleep(10)
        # Verify Watermarks
        if self.wm.verify_watermarks() is not True:
            self.fail("Error Observed in watermark verification")
        else:
            logging.info(f"Watermark verification passed post {self.scenario.lower()}")

        ##
        # Wait for 10 seconds after power event
        time.sleep(10)

        ##
        # Stop ETL capture
        etl_file = watermark_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')

    ##
    # @brief        Test to verify watermarks during AC/DC switch.
    # @return       None
    @unittest.skipIf(watermark_helper.get_config_type('-SCENARIO') != 'AC_DC',
                     "Skip the test step as the scenario type is not AC/DC switch")
    def test_08_ac_dc_switch(self):
        disp_power = DisplayPower()

        ##
        # Start ETL capture
        if watermark_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        # Checking current power line status and if it is not DC, then changing it to DC
        if disp_power.enable_disable_simulated_battery(True):
            logging.info("Enabled Simulated Battery successfully")
            power_line_status = disp_power.get_current_powerline_status()
            if power_line_status != PowerSource.DC:
                logging.debug(f"Current powerline status is not in {power_line_status} setting it to DC")
                result = disp_power.set_current_powerline_status(PowerSource.DC)
                if not result:
                    self.fail("Aborting the test as switching to DC mode failed")
            logging.info("Switched power line to DC successfully")
        else:
            logging.error("Failed to enable simulated battery")

        time.sleep(10)
        # Verify Watermarks
        if self.wm.verify_watermarks() is not True:
            self.fail("Error Observed in watermark verification")
        else:
            logging.info("Watermark verification passed post DC Switch")

        # Checking current power line status and if it is not AC, then changing it to AC
        power_line_status = disp_power.get_current_powerline_status()
        if power_line_status != PowerSource.AC:
            result = disp_power.set_current_powerline_status(PowerSource.AC)
            if not result:
                self.fail("Aborting the test as switching to AC mode failed")

        ##
        # Wait for 30 seconds after switching AC mode
        time.sleep(5)

        # Verify Watermarks
        if self.wm.verify_watermarks() is not True:
            self.fail("Error Observed in watermark verification")
        else:
            logging.info("Watermark verification passed post AC Switch")

        ##
        # Stop ETL capture
        etl_file = watermark_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test Purpose: Test to verify WM functionality during display events while running on single/multiple displays")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
