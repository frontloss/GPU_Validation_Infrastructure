########################################################################################################################
# @file         planes_ui_stress.py
# @brief        The script consists of stress test scenarios
# @author       Pai, Vinayak1
########################################################################################################################
import itertools
import logging
import os
import random
import sys
import threading
import time
import unittest

from Libs.Core import enum
from Libs.Core.logger import etl_tracer
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PlanesUI import planes_ui_base
from Tests.PlanesUI.Common import planes_ui_helper
from Tests.PlanesUI.Common import stress_scenarios

dump_path = "C:\Windows\LiveKernelReports\WATCHDOG"


##
# @brief    Contains basic PlanesUI tests
class PlanesUIStress(planes_ui_base.PlanesUIBase):
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'STRESS',
                     "Skip the test step as the scenario type is not STRESS")
    ##
    # @brief        Test to execute stress scenarios
    # @return       None
    def __test_display_switch(self):
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
        # Applying each configuration across the displays connected
        for each_config in range(0, len(config_list)):
            if planes_ui_helper.set_display_config(config_list[each_config][0], config_list[each_config][1]) is True:
                logging.info("Successfully applied display configuration")
                # Wait for 10 seconds after display switch
                time.sleep(10)
            else:
                self.fail("Failed to display configuration")

    ##
    # @brief        Test to execute stress scenarios
    # @return       None
    def __test_hotplug_unplug(self):
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

    ##
    # @brief        Test to verify MPO functionality during mode switch/rotate while app(s) are running.
    # @return       None
    def __test_mode_switch(self):
        target_id_list = self.get_target_id_list(include_inactive=True)

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
    # @brief        Test to execute stress scenarios
    # @param[in]    scenario_sequence
    # @return       None
    def __stress_scenarios(self, scenario_sequence):
        for each_scenario in scenario_sequence:
            start_time = time.time()
            stress_scenarios.scenario_dict[each_scenario](self.app[0])
            end_time = time.time()
            files_in_dump_path = []
            if os.path.exists(dump_path):
                for files in os.listdir(dump_path):
                    if os.path.isfile(os.path.join(dump_path, files)):
                        files_in_dump_path.append(files)
                logging.info(f"Dump file {files_in_dump_path} in LiveKernelReports")
            logging.info(f"Start time for scenario {each_scenario} = {str(start_time)}s")
            logging.info(f"End time for scenario {each_scenario} = {str(end_time)}s")
            final_time = end_time - start_time
            logging.info(f"Total time for sceanrio {each_scenario} = {str(final_time)}s")

    ##
    # @brief        Test to execute youtube scenario
    # @return       None
    def __youtube_scenario(self):
        app_instance = planes_ui_helper.create_app_instance('YOUTUBE')
        app_instance.open_app()
        time.sleep(60)
        planes_ui_helper.enable_disable_auto_detect_proxy(planes_ui_helper.RegistryStatus.DISABLE)
        planes_ui_helper.enable_disable_first_run_experience(planes_ui_helper.RegistryStatus.DISABLE)
        app_instance.close_app()

    ##
    # @brief        Test to execute stress scenarios
    # @return       None
    def test_01_stress(self):
        etl_tracer.stop_etl_tracer()
        etl_tracer._unregister_trace_scripts()
        scenario_sequence = []
        iteration = int(self.iteration) if self.iteration is not None else sys.maxsize
        for i in range(0, iteration):
            x = random.randint(1, len(stress_scenarios.scenario_dict))
            scenario_sequence.append(x)
        logging.info(f"Sequence List : {scenario_sequence}")

        threads = [
            threading.Thread(target=self.__test_display_switch, daemon=True),
            threading.Thread(target=self.__test_hotplug_unplug, daemon=True),
            threading.Thread(target=self.__stress_scenarios, args=(scenario_sequence,), daemon=True),
            threading.Thread(target=self.__test_mode_switch, daemon=True),
            threading.Thread(target=self.__youtube_scenario(), daemon=True)
        ]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == '__main__':
    TestEnvironment.initialize()

    logging.info("Test Purpose: Basic test to execute stress scenarios")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
