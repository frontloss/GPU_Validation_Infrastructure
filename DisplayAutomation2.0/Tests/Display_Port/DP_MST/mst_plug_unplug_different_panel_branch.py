################################################################################################################
# @file          mst_plug_unplug_different_panel_branch.py
# @brief         Verify whether topology detected properly for DP port after plug/unplug of different panel/branch.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() that verifies if topology is detected properly or not after plug/unplug
#               of different panel/branch
class DPMSTPartialTopologyDisconnectConnBranchDispDifferentPanel(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.Applies and verifies 1st MST topology.Then disconnect
    #               display from the topology and connect display from 2nd topology to the original topology and verify.
    #               Then disconnect branch from current topology and connect branch from 3rd topology to the original
    #               topology and verify
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

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get DisplayTopology XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        # Set index pointing to 3rd set of arguments
        dp_port_index = dp_port_index + 1

        # Get SubTopology XML file from command line
        xml_file3 = self.get_xmlfile(dp_port_index)

        # Get the RAD Information
        rad = self.get_topology_rad(port_type)

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        ##
        # Disconnect Display from the current MST Topology
        self.set_partial_topology(port_type, False, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, None)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

        ##
        # Connect Display to original Topology
        self.set_partial_topology(port_type, True, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, xml_file2)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

        ##
        # Disconnect Branch from the current MST Topology
        self.set_partial_topology(port_type, False, rad.BranchRADInfo[rad.NumBranches - 1].NodeRAD, None)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

        ##
        # Connect Branch subTopology to original Topology
        self.set_partial_topology(port_type, True, rad.BranchRADInfo[rad.NumBranches - 1].NodeRAD, xml_file3)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
