################################################################################################################
# @file          mst_sst_switching_full_topology.py
# @brief         Verify full topology switching from MST to SST is proper or not.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that performs full topology switch from MST to SST and verifies it
class DPMSTtoSSTSwitching(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.Test commands are designed such that 1st topology
    #               mentioned in commandline is always MST and 2nd is SST.It first sets MST topology and verifies it.
    #               After the verification, entire topology is unplugged. Now it sets SST topology mentioned in command
    #               line and verifies it.
    # @return       None
    def runTest(self):
        # Variable for DP Port Number Index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type(SST) from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get SST XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        # Function call to hot-unplug DP MST panel
        self.set_hpd(port_type, False)

        logging.info("MST Topology is Unplugged")

        # Function call to hot-plug DP SST panel needed for MST <--> SST switching
        self.setnverifySST(port_type, topology_type2, xml_file2)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
