################################################################################################################
# @file          mst_sst_to_mst_switching_over_all_depth.py
# @brief         Verify topology switching from MST to SST in all the depths of the given topology.
# @author        Praveen Bademi
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class has 2 methods , one to perform topology switch on a partial topology and verifies the
#               topology created and other method invokes it to perform switch at all depths
class DPMSTtoSSTtoMSTSwitchingAllDepths(DisplayPortMSTBase):

    ##
    # @brief        This method performs switch at given depth by detaching display from current MST topology and
    #               attaches the displays from 2nd topology and verifies the topology created.
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    index: int
    #                   index of the display to be detached or switched
    # @param[in]    rad: object
    #                   MST Relative address object
    # @param[in]    xmlfile: str
    #                   Path of the xml file
    # @return       None
    def switchtopology_mst_to_sst(self, port_type, index, rad, xmlfile):

        ##
        # Disconnect/Detach Display from the current MST Topology
        # Arguments foe below function are:(port_type, attach_dettach = False, noderad, xmlfile = None)
        self.set_partial_topology(port_type, False, rad.DisplayRADInfo[index].NodeRAD, None)

        ##
        # Switch panel to SST if previously detached panel is MST or
        # switch panel to MST if previously detached panel is SST
        # Arguments foe below function are:(port_type, attach_dettach = True, noderad, xmlfile = SubDisplaySST.xml)
        self.set_partial_topology(port_type, True, rad.DisplayRADInfo[index].NodeRAD, xmlfile)

        # Wait for the simulation driver to reflect the SST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

    ##
    # @brief        This method executes the actual test steps.It sets and verifies the first topology mentioned in the
    #               commandline and then calls switchtopology_mst_to_sst() to perform switch to other topology at all
    #               depths
    # @return       None
    def runTest(self):

        # Variable for DP Port Number Index fom command line
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file path from command line
        xml_file = self.get_xmlfile(dp_port_index)

        dp_port_index = dp_port_index + 1

        # Get SST Sub Display XML file path from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 MST topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        # Wait for the simulation driver to reflect the SST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Get the RAD Information of MST Topology
        rad = self.get_topology_rad(port_type)

        # Switch to SST/MST Panel for each MST/SST display present in the topology one after the other
        for index in range(rad.NumDisplays):
            # Detach SST panel and attache MST panel or
            # Detach MST panel and attache SST panel in sequence
            self.switchtopology_mst_to_sst(port_type, index, rad, xml_file2)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
