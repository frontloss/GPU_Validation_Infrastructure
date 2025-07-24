################################################################################################################
# @file          tiled_2_inputs_different_mst_plug_unplug_during_power_event_nontiled_to_tiled.py
# @brief         Verify able to switch from Non-tiled to Tiled during hotplug/unplug with power events.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that initially has 2 mst tiled topologies plugged and then 2nd
#               topology is switched to 3rd mst tiled topology during power event
class DPTiledTwoInputDifferentMSTHotplugUnplugPowerEventsNonTiledtoTiled(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It plugs 1st MST tiled panel to 1st port, and 2nd MST
    #               tiled panel to 2nd port.Then 2nd mst tiled topology is unplugged and 3rd mst tiled topology is
    #               plugged to 1st port and supported power event(s3/cs) is invoked. After resuming from the power
    #               event max mode is applied and tiled display verification is performed
    # @return       None
    def runTest(self):

        # Variable for DP port number index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get MST XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Initialize DP object, parse/send topology and issue HPD to Gfx driver
        # Plug DP MST Tiled Panel here
        self.set_tiled_mode(port_type, topology_type, xml_file)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get the port type from available free DP ports
        port_type2 = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Initialize DP object, parse/send topology and issue HPD to driver with the configuration passed by the user
        # Master port_type is being plugged in and panel is another DP MST Tiled Panel
        self.set_tiled_mode(port_type2, topology_type2, xml_file2)

        # Unplug Slave port(DP MST panel)
        self.set_hpd(port_type2, False)

        # Set index pointing to 3rd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type from the command line
        topology_type3 = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file3 = self.get_xmlfile(dp_port_index)

        # Function call to set HPD Data during Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = PlugSink,
        # plug_unplug_atsource = True, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.PlugSink, True, topology_type3)

        # Send the SST XML Data to Gfx Simulation Driver
        self.parse_send_topology(port_type, topology_type3, xml_file3, True)

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

        # Set SD config and apply max mode
        self.set_config_apply_max_mode()

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        if is_tiled_display:
            logging.info("Tiled display(s) found %s" % tiled_target_ids_list)
            # Only one Tiled display is plugged and so it should be present at '0' index
            self.verify_tiled_display(True, True, True, tiled_target_ids_list[0])
        else:
            logging.error("[Driver Issue]: Tiled display not found! Exiting....")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Verification of tiled display failed",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
