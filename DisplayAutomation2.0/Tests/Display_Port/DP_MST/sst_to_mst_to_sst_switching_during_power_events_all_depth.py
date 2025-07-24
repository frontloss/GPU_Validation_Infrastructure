################################################################################################################
# @file          sst_to_mst_to_sst_switching_during_power_events_all_depth.py
# @brief         Verify topology switching from SST to MST to SST during power Events.
# @note          Currently only MST to SST switching is present
# @author        Praveen Bademi
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains methods that Verifies topology switching from SST to MST to SST during power Events
#               at all depths.
# @note         Currently only MST to SST switching is present
class DPSSTtoMSTtoSSTSwitchingPowerEvetnsAllDepths(DisplayPortMSTBase):

    ##
    # @brief        This method performs switch to SST panel if previously detached panel is MST and vice-versa, during
    #               power event, at given depth and verifies the topology created
    # @param[in]    index: int
    #                   index of the display to be detached or switched
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology: str
    #                   MST or SST
    # @param[in]    xmlfilepath: str
    #                   Path of the xml file
    # @param[in]    rad: object
    #                   MST Relative address object
    # @note         Currently only MST to SST switching is present
    # @return       None
    def switchtopology_power_events(self, index, port_type, topology, xmlfilepath, rad):

        # Disconnect/Detach Display from the current Topology
        # Arguments for below function are:(port_type, attach_dettach = False, noderad, xmlfile = None)
        self.set_partial_topology(port_type, False, rad.DisplayRADInfo[index].NodeRAD, None)

        # Function call to set HPD Data during Low Power State
        # Arguments for below function are:(num_of_ports  = 1, port_type, sink_plugreq = PlugSink,
        # plug_unplug_atsource = False, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.PlugSink, False, topology)

        ##
        # Switch panel to SST if previously detached panel is MST or
        # switch panel to MST if previously detached panel is SST
        # set_partial_topology(port_type, attach_dettach = True, noderad, xmlfile = SubDisplaySST.xml/SubDisplayMST.xml,
        # islowpower = True)
        self.set_partial_topology(port_type, True, rad.DisplayRADInfo[index].NodeRAD, xmlfilepath, True)

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

        # TODO: Verify the Display through Version Register and DPCD Read for all depths

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

    ##
    # @brief        This method executes the actual test steps.It sets and verifies 1st topology mentioned in the
    #               command line.Then at each depth during power event it switches to SST panel from 2nd topology in
    #               commandline if previously detached panel is MST, and it switches to MST panel from 3rd topology in
    #               the commandline if previously detached panel is SST, and verifies the topology created.
    # @note         Currently only MST to SST switching is present
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

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type(SST) from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get SST Sub Display XML file path from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Set index pointing to 3rd set of arguments
        dp_port_index = dp_port_index + 1

        # Get SST Sub Display XML file path from command line
        xml_file3 = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 MST topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        # Get the RAD Information of MST Topology
        rad = self.get_topology_rad(port_type)

        # Switch to SST/MST Panel for each MST/SST display resp in the topology one after the other
        for index in range(rad.NumDisplays):
            # Detach SST panel and attache MST panel or
            # Detach MST panel and attache SST panel in sequence
            self.switchtopology_power_events(index, port_type, topology_type2, xml_file2, rad)

            self.switchtopology_power_events(index, port_type, topology_type2, xml_file3, rad)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
