################################################################################################################
# @file          mst_unplug_panel_plug_topology_after_power_event.py
# @brief         Verify whether topology detected properly with addition/removal of displays and
#                branch after power events.
# @author        Veena Veluru
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() that verifies if topology is detected properly or not after unplugging a
#               display from original MST topology and connecting subtopology/branch to it after the power event
class DPMSTDisplayDisconnectTopologyConnectAfterPowerEvents(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps. It sets and verifies 1st MST topology mentioned in the
    #               commandline.Then it invokes power event and resumes from it. It then disconnects a display from it and verifies the topology. 
    #               It also verifies num of displays in mst topology before and after power event. It then invokes and resumes from power event again.
    #               Then it Connects the 2nd topology/branch mentioned in the commandline to the current MST topolog. It verifies the topology.
    #               It also verifies num of displays in mst topology before and after power event.
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

        display_and_adapter_info_list = self.display_config.get_display_and_adapter_info_ex(port_type, 'gfx_0')
        if type(display_and_adapter_info_list) != list:
            display_and_adapter_info_list = [display_and_adapter_info_list]
        num_of_displays_before_pe = len(display_and_adapter_info_list)

        # Set index pointing to 2nd set of arguments from command line
        dp_port_index = dp_port_index + 1

        # Get Topology2 XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Get the RAD Information
        rad = self.get_topology_rad(port_type)

        # Set DUT to Low Power State
        self.power_event(display_power.PowerEvent.S4, RESUME_TIME)

        ##
        # Disconnect Display from the original MST Topology
        self.set_partial_topology(port_type, False, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, None, True)

        # Wait for the simulation driver to reflect the SST connection status in CUI
        time.sleep(25)

        display_and_adapter_info_list = self.display_config.get_display_and_adapter_info_ex(port_type, 'gfx_0')
        if type(display_and_adapter_info_list) != list:
            display_and_adapter_info_list = [display_and_adapter_info_list]
        num_of_displays_after_pe = len(display_and_adapter_info_list)
        
        if num_of_displays_after_pe == num_of_displays_before_pe -1:
            logging.info("Display successfully Unplugged after power event")
        else:
            self.fail("Display is not unplugged from MST Topology after Power event")

        num_of_displays_before_pe = num_of_displays_after_pe
        # set DUT to Low Power State
        self.power_event(display_power.PowerEvent.S4, RESUME_TIME)

        ##
        # Connect Subtopology to the Original MST Topology
        self.set_partial_topology(port_type, True, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, xml_file2, True)

        display_and_adapter_info_list = self.display_config.get_display_and_adapter_info_ex(port_type, 'gfx_0')
        if type(display_and_adapter_info_list) != list:
            display_and_adapter_info_list = [display_and_adapter_info_list]
        num_of_displays_after_pe = len(display_and_adapter_info_list)

        if num_of_displays_after_pe == num_of_displays_before_pe + 1:
            logging.info("Display successfully got Plugged after power event")
        else:
            self.fail("Display is not plugged to MST Topology after Power event")

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology page
        self.verifyTopology(port_type)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
