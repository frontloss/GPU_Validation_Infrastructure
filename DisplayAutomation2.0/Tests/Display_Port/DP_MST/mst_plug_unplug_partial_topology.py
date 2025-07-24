################################################################################################################
# @file          mst_plug_unplug_partial_topology.py
# @brief         Verify whether display/topology were detached properly or not.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that verifies the partial topology created after detaching a
#               display and a branch from original MST topology
class DPMSTPartialTopologyDispBranchDisconnect(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It first sets and verifies the MST topology mentioned in
    #               the commandline.Then detaches a display from original topology and verifies the partial topology
    #               created.And then detaches a branch from the current topology and again verifies the partial topology
    #               created
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

        rad = self.get_topology_rad(port_type)
        logging.info("Number of Branches %s, Number of Displays %s" % (rad.NumBranches, rad.NumDisplays))
        for index in range(rad.NumDisplays):
            logging.info("DISPLAY %s" % index)

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Disconnect Display(MST/SST) from the original MST Topology
        self.set_partial_topology(port_type, False, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, None)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

        # Disconnect sub-topology from the original MST Topology
        self.set_partial_topology(port_type, False, rad.BranchRADInfo[rad.NumBranches - 1].NodeRAD, None)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
