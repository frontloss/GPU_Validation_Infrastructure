################################################################################################################
# @file          mst_plug_unplug_panel_topology_during_power_event.py
# @brief         Verify whether topology detected properly during power events with addition/removal of displays and
#                branch.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains 3 methods one to disconnect and connect display along with power event, other to
#               disconnect and connect topology along with power event and runTest() method to call the other two
#               methods consecutively and verify the topology in each case.
class DPMSTDisconnectConnBranchDispDifferentPanel(DisplayPortMSTBase):

    ##
    # @brief        This function call is to disconnect a display from current MST topology in low_power state, invoke
    #               power event and verify the topology. Then connect different display to the original topology in
    #               low_power state, invoke power event and verify the topology again.
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology_type: str
    #                   contains topology type Ex: SST, MST
    # @param[in]    rad: object
    #                   MST Relative address object
    # @param[in]    xml_file: str
    #                   path of the xml file to be parsed
    # @return       None
    def disconnect_connect_display(self, port_type, topology_type, rad, xml_file):
        # Function call to set HPD Data during Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = UnplugSink,
        # plug_unplug_atsource = False, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.UnplugSink, False, topology_type)

        ##
        # Disconnect Display from the current MST Topology
        self.set_partial_topology(port_type, False, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, None, True)

        # set DUT to Low Power State
        self.power_event(display_power.PowerEvent.S3, RESUME_TIME)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

        # Function call to set HPD Data during Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = PlugSink,
        # plug_unplug_atsource = False, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.PlugSink, False, topology_type)

        ##
        # Connect Display to original Topology
        self.set_partial_topology(port_type, True, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, xml_file, True)

        ##
        # Verifying whether system supports CS (ConnectedStandby).If yes,then we will validate CS entry/exit.
        # If not, then we will validate S3 entry/exit.
        cs_status = self.display_power.is_power_state_supported(display_power.PowerEvent.CS)
        ##
        # if CS is enabled in the system then go to CS(ConnectedStandby) and hotplug/unplug displays
        if cs_status is True:
            logging.info("Performing Power event CS(ConnectedStandby)")
            # Invoke power event CS(ConnectedStandby)
            self.power_event(display_power.PowerEvent.CS, RESUME_TIME)
        else:
            logging.info("Performing Power event S3(Standby)")
            # Invoke power event S3(Standby)
            self.power_event(display_power.PowerEvent.S3, RESUME_TIME)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

    ##
    # @brief        This function call is to disconnect a sub-topology from current MST topology in low_power state,
    #               invoke power event and verify the topology. Then connect different sub-topology to the original
    #               topology in low_power state, invoke power event and verify the topology again.
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology_type: str
    #                   contains topology type Ex: SST, MST
    # @param[in]    rad: object
    #                   MST Relative address object
    # @param[in]    xml_file: str
    #                   path of the xml file to be parsed
    # @return       None
    def disconnect_connect_topology(self, port_type, topology_type, rad, xml_file):
        # Function call to set HPD Data during Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = UnplugSink,
        # plug_unplug_atsource = False, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.UnplugSink, False, topology_type)

        ##
        # Disconnect Branch from the current MST Topology
        self.set_partial_topology(port_type, False, rad.BranchRADInfo[rad.NumBranches - 1].NodeRAD, None, True)

        # set DUT to Low Power State
        self.power_event(display_power.PowerEvent.S3, RESUME_TIME)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

        # Function call to set HPD Data during Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = PlugSink,
        # plug_unplug_atsource = False, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.PlugSink, False, topology_type)

        ##
        # Connect Branch subTopology to original Topology
        self.set_partial_topology(port_type, True, rad.BranchRADInfo[rad.NumBranches - 1].NodeRAD, xml_file, True)

        # set DUT to Low Power State
        self.power_event(display_power.PowerEvent.S3, RESUME_TIME)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

    ##
    # @brief        This method executes the actual test steps.It first applies and verifies 1st MST topology, then
    #               disconnects display from current topology and connects display from 2nd topology mentioned in the
    #               commandline in low_power states along with power event and verifies the topology.Then  disconnects
    #               sub-topology from current topology and connects 3rd topology mentioned in the commandline in
    #               low_power state along with power event and verifies the topology
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

        # Function call to disconnect/connect display during power events
        self.disconnect_connect_display(port_type, topology_type, rad, xml_file2)

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Function call to disconnect/connect branch during power events
        self.disconnect_connect_topology(port_type, topology_type, rad, xml_file3)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
