################################################################################################################
# @file          mst_sst_switching_during_power_event.py
# @brief         Verify topology switching from MST to SST at all depths during power Events.
# @author        Praveen Bademi
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() which verifies topology switching from MST to SST at all depths during
#               power Events
class DPMSTtoSSTSwitchingPowerEvetnsAllDepths(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.Applies and verifies 1st topology.Then at all depths it
    #               keeps detaching displays from current topology and plugs display from 2nd topology in the command
    #               line, invokes power event and verifies the topology created after resuming from power event.
    # @return       None
    def runTest(self):

        # Variable for DP Port Number Index fom command line
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file path from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type(SST) from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get SST Sub Display XML file path from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 MST topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        # Get the RAD Information of MST Topology
        rad = self.get_topology_rad(port_type)

        # Switch to SST/MST Panel for each MST/SST display resp in the topology one after the other
        for index in range(rad.NumDisplays):
            ##
            # Disconnect/Detach Display from the current MST Topology
            # Arguments for below function are:(port_type, attach_dettach = False, noderad, xmlfile = None)
            self.set_partial_topology(port_type, False, rad.DisplayRADInfo[index].NodeRAD, None)

            # Function call to set HPD Data during Low Power State
            # Arguments for below function are:num_of_ports  = 1, port_type, sink_plugreq = PlugSink,
            # plug_unplug_atsource = False, topology_after_resume = MST)
            self.set_low_power_state(1, port_type, enum.PlugSink, False, topology_type2)

            ##
            # Switch panel to SST if previously detached panel is MST or
            # switch panel to MST if previously detached panel is SST
            # Arguments for below function are:port_type, attach_dettach = True, noderad,
            # xmlfile = SubDisplaySST.xml/SubDisplayMST.xml, islowpower = True)
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

            # TODO: Verify the SST Panel through Version Register and DPCD Read for all depths

            # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP
            # topology page
            self.verifyTopology(port_type)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
