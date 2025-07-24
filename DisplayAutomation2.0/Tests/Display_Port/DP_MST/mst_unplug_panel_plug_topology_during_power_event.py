################################################################################################################
# @file          mst_unplug_panel_plug_topology_during_power_event.py
# @brief         Verify whether topology detected properly during power events with addition/removal of displays and
#                branch.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() that verifies if topology is detected properly or not after unplugging a
#               display from original MST topology and connecting subtopology/branch to it during the power event
class DPMSTDisplayDisconnectTopologyConnectDuringPowerEvents(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It sets and verifies 1st MST topology mentioned in the
    #               commandline.Then it disconnects a display from it and invokes power event.After resuming from power
    #               event it verifies the topology.It then connects the 2nd topology/branch mentioned in the command
    #               line to the current MST topology and invokes power event.After resuming from the power event it
    #               verifies the topology
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

        # Set index pointing to 2nd set of arguments from command line
        dp_port_index = dp_port_index + 1

        # Get Topology2 XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Get the RAD Information
        rad = self.get_topology_rad(port_type)

        # Function call to set HPD Data during Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = UnplugSink,
        # plug_unplug_atsource = False, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.UnplugSink, False, topology_type)

        ##
        # Disconnect Display from the original MST Topology
        self.set_partial_topology(port_type, False, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, None, True)

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

        # Function call to set HPD Data during Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = PlugSink,
        # plug_unplug_atsource = False, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.PlugSink, False, topology_type)

        ##
        # Connect Subtopology to the Original MST Topology
        self.set_partial_topology(port_type, True, rad.DisplayRADInfo[rad.NumDisplays - 1].NodeRAD, xml_file2, True)

        # set DUT to Low Power State
        self.power_event(display_power.PowerEvent.S3, RESUME_TIME)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
