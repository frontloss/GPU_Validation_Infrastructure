################################################################################################################
# @file          mst_sst_plug_sst_unplug_plug_mst.py
# @brief         To verify for plug of MST and SST followed by SST unplug and hot plug MST
#                This test case covers MST - SST plug unplug test scenario of SST transcoder
#                getting re-assigned to MST slave display
#
#                i)  Plug MST monitor to Port D & enable display
#                ii) Plug SST monitor to Port E & Enable display
#               iii) Unplug SST monitor in Port E
#                iv) Plug a new child display to MST Monitor on Port D
#                   and enable the new display as well. (i.e now Port D has 2
#                   displays in MST daisy chained mode)
# @author        Saradaa
################################################################################################################

import sys
import unittest
import logging
import time
from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core import display_utility
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase, DELAY_1000_MILLISECONDS, \
    DELAY_5000_MILLISECONDS


##
# @brief        This class contains runTest() method that verifies the partial topology created
#               after attaching a display and a branch to original MST topology
class DPMSTPartialTopologyDispBranchConnect(DisplayPortMSTBase):
    ##
    # @brief        This method executes the actual test steps.MST - SST plug unplug
    #               test to cover scenario of SST transcoder getting re-assigned to MST slave display
    #
    # @return       None
    def runTest(self):
        cls = DisplayPortMSTBase
        # Variable for DP Port Number Index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type1 = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST) from the command line
        topology_type1 = self.get_topology_type(dp_port_index)

        # Get Topology XML files from command line
        xml_file1 = self.get_xmlfile(dp_port_index)
        xml_file2 = self.get_xmlfile(dp_port_index + 1)

        # Function call to verify MST topology
        self.setnverifyMST(port_type1, topology_type1, xml_file1)
        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1
        # Get Topology Type(SST) from the command line
        port_type2 = self.get_dp_port_from_availablelist(dp_port_index)
        # Get RAD details and branch and display connected information
        rad = self.get_topology_rad(port_type1)
        logging.info("Number of Branches %s, Number of Displays %s" % (rad.NumBranches, rad.NumDisplays))
        for index in range(rad.NumDisplays):
            logging.info("DISPLAY %s" % index)

        # Unplug one display from MST
        logging.info("Unplug 1 display from MST")
        self.set_partial_topology(port_type1, False, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, None)

        # Plug SST display
        logging.info("Plug SST display")
        display_utility.plug(port_type2)

        # Apply Extended on MST+SST
        logging.info("Apply extended config on MST + SST ")
        display_and_adapter_info_list = cls.get_current_display_and_adapter_info_list(is_lfp_info_required=False)
        is_success = cls.display_config.set_display_configuration_ex(enum.EXTENDED, display_and_adapter_info_list)
        self.assertTrue(is_success, "Set Display Configuration: Extended config on MST + SST Failed")

        # Hot unplug to Graphics driver for SST display
        logging.info("Unplug SST display")
        is_success = display_utility.unplug(port_type2)
        self.assertTrue(is_success, "SST unplug failure")

        # Connect Display(MST) to the original MST Topology
        logging.info("Hot Plug of display to MST")
        self.set_partial_topology(port_type1, True, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, xml_file2)

        rad = self.get_topology_rad(port_type1)
        logging.info("Number of Branches %s, Number of Displays %s" % (rad.NumBranches, rad.NumDisplays))
        for index in range(rad.NumDisplays):
            logging.info("DISPLAY %s" % index)

        # Enable the displays
        logging.info("Set config extended with 2 MST displays and confirm ")
        display_and_adapter_info_list = cls.get_current_display_and_adapter_info_list(is_lfp_info_required=False)
        is_success = cls.display_config.set_display_configuration_ex(enum.EXTENDED, display_and_adapter_info_list)
        self.assertTrue(is_success, "Set Display Configuration : Extended on MST displays Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
