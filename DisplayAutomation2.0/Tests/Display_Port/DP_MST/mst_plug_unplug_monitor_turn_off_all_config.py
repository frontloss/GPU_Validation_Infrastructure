################################################################################################################
# @file          mst_plug_unplug_monitor_turn_off_all_config.py
# @brief         Verify whether topology detected properly for DP port with hotplug/unplug during monitor turnoff/on.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        Verify whether topology detected properly for DP port with hotplug/unplug during monitor turnoff/on.
class DPMSTSimpleTopologyHotplugUnplugMonitorTurnOffOn(DisplayPortMSTBase):

    ##
    # @brief        This method applies configuration and checks its persistence
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @return       None
    def set_allconfigs(self, port_type):
        ##
        # Get the enumerated displays from SystemUtility
        enumerated_displays = self.display_config.get_enumerated_display_info()

        # get the list of combinations of target id's
        display_config, config_combination_list = self.get_all_config_combinations()

        set_config = DisplayConfig()
        set_config.topology = display_config

        for current_config_list in range(len(config_combination_list)):
            targetId = config_combination_list[current_config_list]
            path = 0
            for index in range(len(targetId)):
                set_config.displayPathInfo[path].targetId = targetId[index]
                set_config.displayPathInfo[path].displayAndAdapterInfo = enumerated_displays.ConnectedDisplays[
                    index].DisplayAndAdapterInfo
                path += 1

            set_config.numberOfDisplays = path
            logging.info("Trying to Apply Display Configuration as : %s", set_config.to_string(enumerated_displays))
            ##
            # Apply display configuration
            self.display_config.set_display_configuration(set_config)

            ##
            # Getting current configuration
            get_config = self.display_config.get_current_display_configuration()
            logging.info("Current display configuration: %s", get_config.to_string(enumerated_displays))

            if get_config.equals(set_config):
                logging.info("Successfully applied display configuration")
            else:
                logging.error("[Driver Issue]: Failed to apply display configuration")
                self.set_default_config()
                # Gdhm bug reporting handled in set_display_configuration
                self.fail()

            # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP
            # topology page
            self.verifyTopology(port_type)

            # get the current display configuration
            get_config = self.display_config.get_current_display_configuration()
            # compare the applid and current display configuration
            if get_config.equals(set_config):
                logging.info("Applied Display Configuration is persistent across power events")
            else:
                logging.error(
                    "[Driver Issue]: Applied Display Configuration is not persistent across power events... Exiting...."
                )
                logging.error(
                    "Applied Display Configuration:%s Current Display Configuration:%s" \
                    % (set_config.to_string(enumerated_displays), get_config.to_string(enumerated_displays))
                )
                self.set_default_config()
                # Gdhm bug reporting handled in set_display_configuration
                self.fail()

    ##
    # @brief        runTest() executes the actual test steps.
    # @return       None
    def runTest(self):

        self.power_event = display_power.MonitorPower.OFF_ON

        # Variable for DP Port Number Index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        # Set config and verify the config applied
        self.set_allconfigs(port_type)

        # Function call to Unplug the panel connected Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = UnplugSink,
        # plug_unplug_atsource = True, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.UnplugSink, True, topology_type)

        # Send the SST XML Data to Gfx Simulation Driver
        self.parse_send_topology(port_type, topology_type, xml_file, True)

        # Invoke Monitor Turnoff
        result = self.display_power.invoke_monitor_turnoff(self.power_event, RESUME_TIME)
        self.assertEquals(result, True, '[Test Issue]: Failed to invoke power event %s' % self.power_event)

        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Function call to plug the panel connected Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = UnplugSink,
        # plug_unplug_atsource = True, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.PlugSink, True, topology_type)

        # Send the SST XML Data to Gfx Simulation Driver
        self.parse_send_topology(port_type, topology_type, xml_file, True)

        # Invoke Monitor Turnoff
        result = self.display_power.invoke_monitor_turnoff(self.power_event, RESUME_TIME)
        self.assertEquals(result, True, '[Test Issue]: Failed to invoke power event %s' % self.power_event)

        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

        # Set back the default config while returning back from test
        self.set_default_config()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
