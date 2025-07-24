################################################################################################################
# @file          sst_to_mst_to_sst_switching_full_topology.py
# @brief         Verify whether switching is proper from SST to MST to SST.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() that switches from SST topology to MST and again switches back to SST and
#               verifies the corresponding topology after each switch
class DPSSTtoMSTtoSSTSwitching(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It sets and verifies SST topology mentioned in the
    #               commandline.Then unplugs the SST topology and plugs MST topology mentioned in the commandline to the
    #               same port and verifies it.Now unplugs MST topology and plugs back SST topology and verifies it
    # @return       None
    def runTest(self):
        # Variable for DP Port Number Index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get SST XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type(MST) from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to hot-plug DP SST panel needed for SST <--> MST switching
        self.setnverifySST(port_type, topology_type, xml_file)

        # Function call to hot-unplug DP SST panel
        self.set_hpd(port_type, False)

        logging.info("Unplug SST")

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type2, xml_file2)

        logging.info("Unplug MST")

        # Function call to hot-unplug DP MST panel
        self.set_hpd(port_type, False)

        logging.info("Plug SST")

        # # Function call to hot-plug DP MST panel needed for SST <--> MST switching
        self.setnverifySST(port_type, topology_type, xml_file)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
