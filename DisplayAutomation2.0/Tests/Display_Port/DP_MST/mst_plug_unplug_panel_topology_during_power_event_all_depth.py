################################################################################################################
# @file          mst_plug_unplug_panel_topology_during_power_event_all_depth.py
# @brief         Verify whether topology detected properly during power events with addition/removal of displays and
#                branch for all depths
# @author        Praveen Bademi
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains methods that verifies the topology disconnecting/connecting different panel/topology
#               to the original topology at all depths during power event
class DPMSTDisconnectConnBranchDispDifferentPanelPowerEventsAllDepths(DisplayPortMSTBase):

    ##
    # @brief        This method disconnects a display/topology from original topology and connects display/topology
    #               passed to the function, invokes power events and verifies the topology
    # @param[in]    index: int
    #                   contains index of the port
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology_type: str
    #                   contains topology type Ex: SST, MST
    # @param[in]    rad: object
    #                   MST Relative address object
    # @param[in]    xml_file: str
    #                   path of the xml file to be parsed
    # @param[in]    isdisplay: bool
    #                   indicates if its a display or branch
    # @param[in]    power_state: str
    #                   indicates the power event to be invoked
    # @return       None
    def disconnect_connect_display_topology(self, index, port_type, topology_type, rad, xml_file, isdisplay,
                                            power_state):

        # Function call to set HPD Data during Low Power State
        # Arguments are: num_of_ports  = 1, port_type, sink_plugreq = UnplugSink,
        # plug_unplug_atsource = False, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.UnplugSink, False, topology_type)

        # Disconnect Display from the current MST Topology
        if isdisplay:
            # Arguments are:(port_type, attach_dettach = False, noderad, xmlfile = None, islowpower = True)
            self.set_partial_topology(port_type, False, rad.DisplayRADInfo[index].NodeRAD, None, True)
        # Disconnect Branch from the current MST Topology
        else:
            # Arguments are:(port_type, attach_dettach = False, noderad, xmlfile = None, islowpower = True)
            self.set_partial_topology(port_type, False, rad.BranchRADInfo[index].NodeRAD, None, True)

        # set DUT to Low Power State
        self.power_event(power_state, RESUME_TIME)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

        # Function call to set HPD Data during Low Power State
        # Arguments are:(num_of_ports  = 1, port_type, sink_plugreq = PlugSink,
        # plug_unplug_atsource = False, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.PlugSink, False, topology_type)

        # Connect Display to original Topology
        if isdisplay:
            # Arguments are:(port_type, attach_dettach = True, noderad, xmlfile = SubDisplay.xml, islowpower = True)
            self.set_partial_topology(port_type, True, rad.DisplayRADInfo[index].NodeRAD, xml_file, True)
        # Connect Branch subTopology to original Topology
        else:
            # Arguments are:(port_type, attach_dettach = True, noderad, xmlfile = SubTopology.xml, islowpower = True)
            self.set_partial_topology(port_type, True, rad.BranchRADInfo[index].NodeRAD, xml_file, True)

        # set DUT to Low Power State
        self.power_event(power_state, RESUME_TIME)

        # Verify the MST Topology being created by comparing the data provided by the user and seen in CUI DP topology
        # page
        self.verifyTopology(port_type)

        # TODO: Verify the DPCD READ 600h for each diaplsy

    ##
    # @brief        This method executes the actual test steps.It first sets and verifies the 1st MST topology mentioned
    #               in the commandline.Then disconnects display/topology from current topology in low_power state,
    #               invokes power event and verifies topology.Then connects display/topology from 2nd and 3rd topology
    #               respectively in low_power state, invokes power event and verifies topology.These operations are
    #               carried out at all depths of display/topologies
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

        # Set index pointing to 2nd set of arguments from command line
        dp_port_index = dp_port_index + 1

        # Get DisplayTopology XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        # Set index pointing to 3rd set of arguments from command line
        dp_port_index = dp_port_index + 1

        # Get SubTopology XML file from command line
        xml_file3 = self.get_xmlfile(dp_port_index)

        rad = self.get_topology_rad(port_type)
        logging.info("Number of Branches %s, Number of Displays %s" % (rad.NumBranches, rad.NumDisplays))

        '''
        # TODO: Currently whenever S4(Hibernate) and S5(reboot) is invoked, the GTA machine gets unresponsive.
        # Hence, commenting test steps related to S4(Hibernate) and S5(reboot).

        # Disconnect and Connect Display during Power Event: S4
        for index in range(rad.NumDisplays):
            logging.info("Performing Power event S4(Hibernate)")
            self.disconnect_connect_display_topology(index, port_type, topology_type, rad, xml_file2, True, 
            enum.POWER_STATE_S4)

            # Wait for the simulation driver to reflect the MST connection status in CUI
            time.sleep(DELAY_5000_MILLISECONDS/DELAY_1000_MILLISECONDS)

        # Disconnect and Connect Topology during Power Event: S4
        for index in range(rad.NumBranches):
            logging.info("Performing Power event S4(Hibernate)")
            # Function call to disconnect/connect branch during power events
            self.disconnect_connect_display_topology(index, port_type, topology_type, rad, xml_file3, False, 
            enum.POWER_STATE_S4)

            # Wait for the simulation driver to reflect the MST connection status in CUI
            time.sleep(DELAY_5000_MILLISECONDS/DELAY_1000_MILLISECONDS)

        # Disconnect and Connect Display during Power Event: S5
        for index in range(rad.NumDisplays):
            logging.info("Performing Power event S5(Reboot)")
            self.disconnect_connect_display_topology(index, port_type, topology_type, rad, xml_file2, True, 
            enum.POWER_STATE_S5)

            # Wait for the simulation driver to reflect the MST connection status in CUI
            time.sleep(DELAY_5000_MILLISECONDS/DELAY_1000_MILLISECONDS)

        # Disconnect and Connect Topology during Power Event: S5
        for index in range(rad.NumBranches):
            logging.info("Performing Power event S5(Reboot)")
            # Function call to disconnect/connect branch during power events
            self.disconnect_connect_display_topology(index, port_type, topology_type, rad, xml_file3, False, 
            enum.POWER_STATE_S5)

            # Wait for the simulation driver to reflect the MST connection status in CUI
            time.sleep(DELAY_5000_MILLISECONDS/DELAY_1000_MILLISECONDS)
        '''

        # Verifying whether system supports CS (ConnectedStandby).If yes,then we will validate CS entry/exit.
        # If not, then we will validate S3 entry/exit.
        cs_status = self.display_power.is_power_state_supported(display_power.PowerEvent.CS)

        # Disconnect and Connect Display during Power Event: CS/S3
        for index in range(rad.NumDisplays):
            if cs_status:
                logging.info("Performing Power event CS(ConnectedStandby)")
                # Function call to disconnect/connect display during power events
                self.disconnect_connect_display_topology(index, port_type, topology_type, rad, xml_file2, True,
                                                         display_power.PowerEvent.CS)

                # Wait for the simulation driver to reflect the MST connection status in CUI
                time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)
            else:
                logging.info("Performing Power event S3(Standby)")
                # Function call to disconnect/connect display during power events
                self.disconnect_connect_display_topology(index, port_type, topology_type, rad, xml_file2, True,
                                                         display_power.PowerEvent.S3)

                # Wait for the simulation driver to reflect the MST connection status in CUI
                time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Disconnect and Connect Topology during Power Event: CS/S3
        for index in range(rad.NumBranches - 1):
            if cs_status:
                logging.info("Performing Power event CS(ConnectedStandby)")
                # Function call to disconnect/connect branch during power events
                self.disconnect_connect_display_topology(index, port_type, topology_type, rad, xml_file3, False,
                                                         display_power.PowerEvent.CS)

                # Wait for the simulation driver to reflect the MST connection status in CUI
                time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)
            else:
                logging.info("Performing Power event S3(Standby)")
                # Function call to disconnect/connect branch during power events
                self.disconnect_connect_display_topology(index, port_type, topology_type, rad, xml_file3, False,
                                                         display_power.PowerEvent.S3)

                # Wait for the simulation driver to reflect the MST connection status in CUI
                time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
