########################################################################################################################
# @file         planes_ui_display_events.py
# @brief        Basic test to verify MPO in different scenarios.
#                   * Exercise the below scenarios while running
#                     3D/Media app.
#                   * Verify the ETL's
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

from Libs.Core import display_essential, enum
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Libs.Core.display_power import DisplayPower, PowerEvent, PowerSource
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PlanesUI.Common import planes_ui_helper
from Tests.PlanesUI import planes_ui_base


##
# @brief    Contains PlanesUI display events tests
class MPOUIDisplayEvents(planes_ui_base.PlanesUIBase):
    ##
    # @brief        Test to verify MPO functionality during mode switch/rotate while app(s) are running.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'MODE_SWITCH',
                     "Skip the test step as the scenario type is not mode switch")
    def test_01_mode_switch(self):
        target_id_list = self.get_target_id_list(include_inactive=True)

        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play the app(s) in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None
        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)

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
                # set all the supported modes
                self.config.set_display_mode([mode])
                logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                    mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.source_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()

    ##
    # @brief        Test to verify MPO functionality during mode switch/rotate while app(s) are running.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'ROTATION',
                     "Skip the test step as the scenario type is not rotation")
    def test_02_rotate(self):
        target_id_list = self.get_target_id_list(include_inactive=True)

        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play the app(s) in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)

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
                    self.config.set_display_mode([mode])
                    logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                        mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()

    ##
    # @brief        Test to verify MPO functionality during display switch while apps are running.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'DISPLAY_SWITCH',
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
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play the app(s) in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)

        ##
        # Wait for a minute during video playback
        time.sleep(10)

        ##
        # Applying each configuration across the displays connected
        for each_config in range(0, len(config_list)):
            if planes_ui_helper.set_display_config(config_list[each_config][0], config_list[each_config][1]) is True:
                logging.info("Successfully applied display configuration")
                # Wait for 10 seconds after display switch
                time.sleep(10)
            else:
                self.fail("Failed to display configuration")

        ##
        # Close the app
        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify MPO functionality if hotplug and unplug is done while video is running.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'HOTPLUG_UNPLUG',
                     "Skip the test step as the scenario type is not hotplug unplug")
    def test_04_hotplug_unplug(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play the app(s) in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)
        time.sleep(30)

        for index in range(0, 10):
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.is_lfp is False and panel.connector_port_type != "VIRTUALDISPLAY":
                        if self.unplug_display(adapter.adapter_info, panel.connector_port_type, False,
                                               panel.port_type):
                            logging.info("Unplugged display {}".format(panel.port_type))
                        else:
                            self.fail("Failed to unplug display {}".format(panel.port_type))

            time.sleep(5)

            ##
            # plug the display
            gfx_adapter_details = self.config.get_all_gfx_adapter_details()
            display_details_list = self.context_args.test.cmd_params.display_details
            self.plug_display(display_details_list)

        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()
        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify MPO functionality during driver restart while video is running.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'RESTART_DRIVER',
                     "Skip the  test step as the scenario type is not Restart driver")
    def test_05_restart_display_driver(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play the app(s) in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)

        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail("Failed to restart display driver")
        else:
            logging.info("Successfully restarted display driver")

        ##
        # Wait for 10 seconds after display driver restart
        time.sleep(10)

        ##
        # Close media player
        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify MPO functionality during power events while video is running.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') not in ['POWER_EVENT_S3', 'POWER_EVENT_S4'],
                     "Skip the test step as the scenario type is not power event S3/S4")
    def test_06_power_events(self):
        disp_power = DisplayPower()

        power_state_dict = {
            "POWER_EVENT_S3": PowerEvent.S3, "POWER_EVENT_S4": PowerEvent.S4}

        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play the app(s) in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)

        ##
        # Wait for a minute during video playback
        time.sleep(60)

        ##
        # Invoke power event
        if disp_power.invoke_power_event(power_state_dict[self.scenario], 60) is False:
            self.fail("Failed to invoke power event {}".format(power_state_dict[self.scenario]))
        else:
            logging.info("Power event {} success".format(power_state_dict[self.scenario]))

        ##
        # Wait for 10 seconds after power event
        time.sleep(10)

        ##
        # Close media player
        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

    ##
    # @brief        Test to verify MPO functionality during TDR generation while video is running.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'GENERATE_TDR',
                     "Skip the test step as the scenario type is not generate tdr")
    def test_07_generate_tdr(self):
        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play the app(s) in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)

        ##
        # Generate & Verify TDR
        VerifierCfg.tdr = Verify.SKIP
        logging.debug("updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))
        logging.info("Generating TDR")
        if not display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True):
            self.fail("Failed to generate TDR")

        if display_essential.detect_system_tdr(gfx_index='gfx_0') is True:
            logging.info('TDR generated successfully')

        ##
        # Wait for 5 seconds after generating TDR
        time.sleep(5)

        ##
        # Close media player
        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")

        if display_essential.clear_tdr() is True:
            logging.info("TDR cleared successfully at end of MPOUI_GENERATE_TDR_Test")
        else:
            logging.error("Failed to clear TDR at end of MPOUI_GENERATE_TDR_Test")

    ##
    # @brief        Test to verify MPO functionality during AC/DC switch while video is running.
    # @return       None
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'AC_DC',
                     "Skip the test step as the scenario type is not AC/DC switch")
    def test_08_ac_dc_switch(self):
        disp_power = DisplayPower()

        ##
        # Start ETL capture
        if planes_ui_helper.start_etl_capture(f'Before_{self.scenario.lower()}_scenario') is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play the app(s) in windowed mode
        app_instance_1 = planes_ui_helper.create_app_instance(self.app[0])
        app_instance_1.open_app(is_full_screen=False, minimize=True)

        app_instance_2 = None

        if len(self.app) > 1:
            app_instance_2 = planes_ui_helper.create_app_instance(self.app[1])
            app_instance_2.open_app(is_full_screen=False)

        ##
        # Wait for 30 seconds during video playback
        time.sleep(30)

        ##
        # Switch the power source to DC Mode
        status = disp_power.set_current_powerline_status(PowerSource.DC)
        if status is False:
            self.fail()

        ##
        # Wait for 30 seconds after switching DC mode
        time.sleep(30)

        ##
        # Switch the power source to AC Mode
        status = disp_power.set_current_powerline_status(PowerSource.AC)
        if status is False:
            self.fail()

        ##
        # Wait for 30 seconds after switching AC mode
        time.sleep(30)

        ##
        # Close media player
        app_instance_1.close_app()
        if app_instance_2 is not None:
            app_instance_2.close_app()

        ##
        # Stop ETL capture
        etl_file = planes_ui_helper.stop_etl_capture(f'After_{self.scenario.lower()}_scenario')
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                   adapter) is False:
                    planes_ui_helper.report_to_gdhm(self.feature)
                    self.fail(f"Verification of {self.feature} failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test Purpose: Test to verify MPO functionality during display events while running single/multiple apps")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)