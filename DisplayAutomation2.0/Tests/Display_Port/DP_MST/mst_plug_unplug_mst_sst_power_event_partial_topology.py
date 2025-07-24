################################################################################################################
# @file          mst_plug_unplug_mst_sst_power_event_partial_topology.py
# @brief         Verify whether topology switched properly from MST to SST at all depths in the partial topology during
#                power events.
# @author        Praveen Bademi
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() that verifies whether topology switched properly from MST to SST at all
#               depths in the partial topology
class DPMSTHotUnplugSSTHotPlugPowerEventsPartialTopology(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It first applies the first MST topology and verifies it.
    #               Then it keeps detaching each MST display from topology one after the other and attaches SST display
    #               from 2nd topology in low_power state and invokes power event. It then verifies if SST displays are
    #               connected successfully for all depths after resuming from the power event
    # @return       None
    def runTest(self):

        # Variable for DP Port Number Index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        # Get the RAD Information of Topology
        rad = self.get_topology_rad(port_type)

        for index in range(rad.NumDisplays):
            ##
            # Disconnect Display from the current MST Topology
            self.set_partial_topology(port_type, False, rad.DisplayRADInfo[index].NodeRAD, None)

            # Function call to set HPD Data during Low Power State
            # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = PlugSink,
            # plug_unplug_atsource = False, topology_after_resume = MST)
            self.set_low_power_state(1, port_type, enum.PlugSink, False, topology_type2)

            ##
            # Connect SST(DP 1.1)Display to original Topology
            self.set_partial_topology(port_type, True, rad.DisplayRADInfo[index].NodeRAD, xml_file2, True)

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

            # TODO: Verify the SST through Version Register and DPCD Read for all depths


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
