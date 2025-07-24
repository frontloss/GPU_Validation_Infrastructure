#######################################################################################################################
# @file          mst_power_event_all_config.py
# @brief         Verify whether applied modes are persistent duirng power event
# @author        Praveen Bademi
########################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains methods that applies given configs across all the displays and check for its
#               persistence during various power event scenarios
class DPMSTAllConfigPowerEvents(DisplayPortMSTBase):

    ##
    # @brief        This method applies all display config combinations,and for each combination it invokes given
    #               power event and checks its persistence after resuming from the power event
    # @param[in]    power_state: str
    #                   power state to be applied EX: s3, s4, cs, s5
    # @return       None
    def set_allconfig_power_events(self, power_state):
        ##
        # Get the enumerated displays from SystemUtility
        enumerated_displays = self.display_config.get_enumerated_display_info()

        display_config, config_combination_list = self.get_all_config_combinations()

        set_config = DisplayConfig()
        set_config.topology = display_config

        for current_config_list in range(len(config_combination_list)):
            targetId = config_combination_list[current_config_list]
            path = 0
            for index in range(len(targetId)):
                set_config.displayPathInfo[path].targetId = targetId[index]
                set_config.displayPathInfo[path].displayAndAdapterInfo = enumerated_displays.ConnectedDisplays[index]. \
                    DisplayAndAdapterInfo
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
                # Gdhm bug reporting handled in set_display_configuration
                self.fail()

            # set DUT to Low Power State
            self.power_event(power_state, RESUME_TIME)

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
                          " are not matching",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

    ##
    # @brief        This method executes the actual test steps.It sets and verifies MST topology mentioned in the
    #               command line and calls set_allconfig_power_events() for various supported power events to verify the
    #               persistence of the applied configs during these power events
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

        ##
        # set the configuration on all the displays as given in the cmd line
        # and verify its persistence
        '''
        # TODO: Currently whenever S4(Hibernate) and S5(reboot) is invoked, the GTA machine gets unresponsive.
        # Hence, commenting test steps related to S4(Hibernate) and S5(reboot)
        self.set_allconfig_power_events(enum.POWER_STATE_S4)
        self.set_allconfig_power_events(enum.POWER_STATE_S5)
        '''
        # Verifying whether system supports CS (ConnectedStandby).If yes,then we will validate CS entry/exit.
        # If not, then we will validate S3 entry/exit.
        if self.display_power.is_power_state_supported(display_power.PowerEvent.CS):
            self.set_allconfig_power_events(display_power.PowerEvent.CS)
        else:
            self.set_allconfig_power_events(display_power.PowerEvent.S3)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
