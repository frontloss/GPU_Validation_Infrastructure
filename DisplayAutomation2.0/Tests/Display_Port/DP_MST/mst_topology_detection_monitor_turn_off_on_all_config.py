################################################################################################################
# @file          mst_topology_detection_monitor_turn_off_on_all_config.py
# @brief         Verify whether topology detected properly for DP port during monitor turnoff/on for each available
#                configurations.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains methods to verify whether topology detected properly for DP port during monitor
#               turnoff/on for each available
class DPMSTSimpleTopologyMonitorTurnOffOn(DisplayPortMSTBase):

    ##
    # @brief        This method applies all possible configuration combinations and invokes monitor turn off/on power
    #               event. After resuming from the power event it verifies the topology and checks the persistence of
    #               applied config
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @return       None
    def set_allconfig_power_events(self, port_type):
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

            power_event = display_power.MonitorPower.OFF_ON

            # Invoke Monitor Turnoff
            result = self.display_power.invoke_monitor_turnoff(power_event, RESUME_TIME)
            self.assertEquals(result, True, '[Test Issue]: Failed to invoke power event %s' % self.power_event)

            # Wait for the simulation driver to reflect the MST connection status in CUI
            time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

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
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] Driver applied configuration and current display config "
                          " are not matching across power events",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.set_default_config()
                self.fail()

    ##
    # @brief        This method executes the actual test steps.It sets and verifies the MST topology and calls
    #               set_allconfig_power_events() method to apply config mentioned in commandline to all possible
    #               combinations and check for its persistence during monitor turn off/on power event and verify
    #               the topology.It sets back to the default config at the end of the test
    # @return       None
    def runTest(self):

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

        self.set_allconfig_power_events(port_type)

        # Wait for the simulation driver to reflect the DP topology connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Set back the default config while returning back from test
        self.set_default_config()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
