################################################################################################################
# @file          sst_unplug_mst_plug_full_topology.py
# @brief         Verify whether able to hotunplug SST display and plug back MST topology on same port
# @author        Diwakar C
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() that plugs and verifies SST topology, then unplugs it and plugs MST
#               topology on the same port and verifies it
class DPSSTUnplugToMSTPlug(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It sets and verifies SST topology mentioned in the
    #               commandline.Then unplugs the SST topology and plugs MST topology mentioned in the commandline to the
    #               same port and verifies it.
    # @return       None
    def runTest(self):
        # Variable for DP Port index in command line
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type (SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get SST XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Set index pointing to 2nd set of arguments
        dp_port_index = 1

        # Get Topology Type (MST) from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to plug SST panel
        self.setnverifySST(port_type, topology_type, xml_file)

        # Function call to hot-unplug DP SST panel
        self.set_hpd(port_type, False)

        # Function call to hot-plug DP MST topology
        self.setnverifyMST(port_type, topology_type2, xml_file2)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
