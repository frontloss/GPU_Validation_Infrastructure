################################################################################################################
# @file         mst_apply_all_config.py
# @brief        Verify whether all configurations are applied for the displays.
# @author       Praveen Bademi
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        The class contains runtest() method that sets and verifies the MST topology and display configuration
#               mentioned in the commandline on all the displays
class DPMSTApplyAllConfigs(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It checks if requested port is present in free port list
    #               and fetches port type, topology type, xmlfile for 1st port index and then applies and verifies the
    #               MST topology. Also applies the display configuration given in commandline on all the displays
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
        self.set_display_config()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
