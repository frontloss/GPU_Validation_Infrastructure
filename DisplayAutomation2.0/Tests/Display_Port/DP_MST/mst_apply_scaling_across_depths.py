################################################################################################################
# @file         mst_apply_scaling_across_depths.py
# @brief        Verify whether all scaling options are applied on the configuration across depths
# @author       Praveen Bademi
################################################################################################################
import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runtest() method sets and verifies all the scaling options after applying mentioned
#               MST topology and display configuration
class DPMSTApplyScaling(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It checks if requested port is present in free port list
    #               and fetches port type, topology type, xmlfile for 1st port index and then applies and verifies the
    #               MST topology. Also applies display configuration mentioned in cmdline and sets and verifies min,max
    #               and mid modes with all scaling options
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
        # and apply min, max and mid modes for that configuration with all the scaling options
        self.set_display_scaling()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
