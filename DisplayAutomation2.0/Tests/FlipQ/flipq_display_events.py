##
# @file         flipq_display_events.py
# @brief        Test to verify FlipQ functionality with video playback during different display events.
#               Test consists of below scenarios:
#                   * Hotplug and unplug of displays
#                   * Display switch
#                   * S3/S4 power events
#                   * Display driver restart
#                   * Different mode switch
#                   * Generate TDR
# @author       Anjali Shetty

import itertools
import logging
import sys
import time
import unittest

from Libs.Core import display_essential, display_power, enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Tests.FlipQ import flipq_base
from Tests.FlipQ import flipq_helper


##
# @brief    FlipQ tests to verify FlipQ functionality during various display events
class FlipQDisplayEvents(flipq_base.FlipQBase):

    ##
    # @brief        test_01_hotplug_unplug Test to verify FlipQ functionality during
    #                                      hotplug and unplug while video is running.
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "HOTPLUG_UNPLUG",
                     "Skip the test step as the action type is not hotplug unplug")
    def test_01_hotplug_unplug(self):
        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_hotplug_unplug_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        flipq_helper.play_close_media(True, False)

        ##
        # Wait for a minute during video playback
        time.sleep(60)

        for index in range(0, 10):
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.is_lfp is False and panel.connector_port_type != "VIRTUALDISPLAY":
                        if self.unplug_display(adapter.adapter_info, panel.connector_port_type, False,
                                               panel.port_type):
                            logging.info("Unplugged display {}".format(panel.port_type))
                        else:
                            flipq_helper.report_to_gdhm(f"Failed to unplug display {panel.port_type}")
                            self.fail("Failed to unplug display {}".format(panel.port_type))

            time.sleep(5)

            ##
            # plug the display
            gfx_adapter_details = self.config.get_all_gfx_adapter_details()
            display_details_list = self.context_args.test.cmd_params.display_details
            self.plug_display(display_details_list)

        ##
        # Close media player
        flipq_helper.play_close_media(False)

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_hotplug_unplug_scenario")

        ##
        # Verify FlipQ
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flipq_helper.verify_flipq(etl_file, panel.pipe, adapter.platform):
                    logging.info("FlipQ verification passed")
                else:
                    flipq_helper.report_to_gdhm()
                    self.fail("FlipQ verification failed")

    ##
    # @brief        test_02_display_switch Test to verify FlipQ functionality during
    #                                      display switch while video is running.
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "DISPLAY_SWITCH",
                     "Skip the test step as the action type is not display switch")
    def test_02_display_switch(self):
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
        if flipq_helper.start_etl_capture("Before_display_switch_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        flipq_helper.play_close_media(True, False)

        ##
        # Wait for a minute during video playback
        time.sleep(60)

        ##
        # Applying each configuration across the displays connected
        for each_config in range(0, len(config_list)):
            if self.config.set_display_configuration_ex(config_list[each_config][0],
                                                        config_list[each_config][1]) is True:
                logging.info("Successfully applied display configuration {}".format(
                    DisplayConfigTopology(config_list[each_config][0]).name, config_list[each_config][1]))

                ##
                # Wait for 10 seconds after display switch
                time.sleep(10)

            else:
                flipq_helper.report_to_gdhm(f"Failed to apply configuration "
                                            f"{DisplayConfigTopology(config_list[each_config][0]).name} "
                                            f"{config_list[each_config][1]}")
                self.fail("Failed to apply  configuration {}".format(
                    DisplayConfigTopology(config_list[each_config][0]).name, config_list[each_config][1]))

        ##
        # Close media player
        flipq_helper.play_close_media(False)

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_display_switch_scenario")

        ##
        # Verify FlipQ
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flipq_helper.verify_flipq(etl_file, panel.pipe, adapter.platform):
                    logging.info("FlipQ verification passed")
                else:
                    flipq_helper.report_to_gdhm()
                    self.fail("FlipQ verification failed")

    ##
    # @brief        test_03_power_events Test to verify FlipQ functionality during
    #                                    power events while video is running.
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') not in ["POWER_EVENT_S3", "POWER_EVENT_S4"],
                     "Skip the test step as the action type is not power event S3/S4")
    def test_03_power_events(self):
        disp_power = display_power.DisplayPower()

        power_state_dict = {
            "POWER_EVENT_S3": display_power.PowerEvent.S3, "POWER_EVENT_S4": display_power.PowerEvent.S4}

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_power_event_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        flipq_helper.play_close_media(True, False)

        ##
        # Wait for a minute during video playback
        time.sleep(60)

        ##
        # Invoke power event
        if disp_power.invoke_power_event(power_state_dict[self.scenario], 60) is False:
            flipq_helper.report_to_gdhm(f"Failed to invoke power event {power_state_dict[self.scenario]}")
            self.fail("Failed to invoke power event {}".format(power_state_dict[self.scenario]))
        else:
            logging.info("Power event {} success".format(power_state_dict[self.scenario]))

        ##
        # Wait for 10 seconds after power event
        time.sleep(10)

        ##
        # Close media player
        flipq_helper.play_close_media(False)

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_power_event_scenario")

        ##
        # Verify FlipQ
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flipq_helper.verify_flipq(etl_file, panel.pipe, adapter.platform):
                    logging.info("FlipQ verification passed")
                else:
                    flipq_helper.report_to_gdhm()
                    self.fail("FlipQ verification failed")

    ##
    # @brief        test_04_restart_display_driver Test to verify FlipQ functionality during
    #                                              driver restart while video is running.
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "RESTART_DRIVER",
                     "Skip the  test step as the action type is not Restart driver")
    def test_04_restart_display_driver(self):
        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_driver_restart_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        flipq_helper.play_close_media(True, False)
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
        flipq_helper.play_close_media(False)

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_driver_restart_scenario")

        ##
        # Verify FlipQ
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flipq_helper.verify_flipq(etl_file, panel.pipe, adapter.platform):
                    logging.info("FlipQ verification passed")
                else:
                    flipq_helper.report_to_gdhm()
                    self.fail("FlipQ verification failed")

    ##
    # @brief        test_05_mode_switch Test to verify FlipQ functionality during
    #                                   mode switch while video is running.
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "MODE_SWITCH",
                     "Skip the test step as the action type is not mode switch")
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
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_resolution_switch_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        flipq_helper.play_close_media(True, False)

        ##
        # fetch all the modes supported by each of the displays connected
        supported_modes = self.config.get_all_supported_modes(target_id_list)
        for key, values in supported_modes.items():
            for mode in values:
                logging.info("Applying Display mode {}" .format(mode.to_string(enumerated_displays)))
                ##
                # set all the supported modes
                self.config.set_display_mode([mode])

        ##
        # Close media player
        flipq_helper.play_close_media(False)

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_resolution_switch_scenario")

        ##
        # Verify FlipQ
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flipq_helper.verify_flipq(etl_file, panel.pipe, adapter.platform):
                    logging.info("FlipQ verification passed")
                else:
                    flipq_helper.report_to_gdhm()
                    self.fail("FlipQ verification failed")

    ##
    # @brief        test_06_generate_tdr Test to verify FlipQ functionality during
    #                                    TDR generation while video is running.
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "GENERATE_TDR",
                     "Skip the test step as the action type is not generate tdr")
    def test_06_generate_tdr(self):

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_tdr_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        flipq_helper.play_close_media(True, False)

        ##
        # Generate & Verify TDR
        VerifierCfg.tdr = Verify.SKIP
        logging.debug("updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))
        logging.info("Generating TDR")
        if not display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True):
            flipq_helper.report_to_gdhm("Failed to genrate TDR")
            self.fail("Failed to generate TDR")

        if display_essential.detect_system_tdr(gfx_index='gfx_0') is True:
            logging.info('TDR generated successfully')
        else:
            flipq_helper.report_to_gdhm("TDR not detected", driver_bug=False)
            self.fail("TDR not detected")

        ##
        # Wait for 5 seconds after generating TDR
        time.sleep(5)

        ##
        # Close media player
        flipq_helper.play_close_media(False)

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_tdr_scenario")

        if display_essential.clear_tdr() is True:
            logging.info("TDR cleared successfully at end of FLipQ test")
        else:
            logging.error("Failed to clear TDR at the end of FlipQ test")

        ##
        # Verify FlipQ
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flipq_helper.verify_flipq(etl_file, panel.pipe, adapter.platform):
                    logging.info("FlipQ verification passed")
                else:
                    flipq_helper.report_to_gdhm()
                    self.fail("FlipQ verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Test to verify FlipQ functionality with video playback during different display events")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
