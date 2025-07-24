################################################################################################################
# @file          tiled_plug_unplug_during_power_events_tiled_nontiled_switching.py
# @brief         Verify able to unplug SST tiled panel and able to plug back MST panel at the same port during power
#                events.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that verifies switching from SST tiled panel to MST tiled panel at
#               the same port during power events
class DPTTiledHotPlugUnPlugDuringPowerEventsTiledtoNonTiled(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It plugs 1st SST tiled panel to 1st port, and 2nd SST
    #               tiled panel to 2nd port.Applies max mode and performs tiled display verification and unplugs 2nd
    #               SST topology from 2nd port.It then unplugs 1st SST topology from 1st port and plugs 3rd topology(MST
    #               Tiled) at the same port, invokes s3 power event. After resuming from power event, it applies the max
    #               mode
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

        # Initialize DP object, parse/send topology and issue HPD to driver with the configuration passed by the user
        # Master port_type is being plugged in
        self.set_tiled_mode(port_type, topology_type, xml_file)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get the port type from available free DP ports
        port_type2 = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get Topology XMl file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Initialize DP object, parse/send topology and issue HPD to driver with the configuration passed by the user
        # Slave port_type is being plugged in, here we pass is_slave as TRUE since we are plugging slave.
        self.set_tiled_mode(port_type2, topology_type2, xml_file2, True)

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        # Set SD config and set mode
        self.set_config_apply_max_mode()

        if is_tiled_display:

            logging.info("Tiled display(s) found %s" % tiled_target_ids_list)
            # Only one Tiled display is plugged and so it should be present at '0' index
            self.verify_tiled_display(False, False, False, tiled_target_ids_list[0])
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

        # Unplug Slave port
        self.set_hpd(port_type2, False, True)

        # Get tiled displays list again after unplugging slave, this time returned target id would be non tiled one
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        ##
        # supported_modes[] is a list of modes supported by the display
        supported_modes = self.display_config.get_all_supported_modes(tiled_target_ids_list)
        for key, values in supported_modes.items():
            # Apply the last mode(i.e. values[-1]) from the supported_modes[] which will be having the maximum
            # resolution
            values = sorted(values, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
            modes_flag = self.display_config.set_display_mode([values[-1]])
            if modes_flag is False:
                logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                # Gdhm bug reporting handled in set_display_mode
                self.fail()

            # self.verify_tiled_nontiled_mode(targetId[index],True,False)

        # Set index pointing to 3rd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type(MST/SST) from the command line
        topology_type3 = self.get_topology_type(dp_port_index)

        # Get MST XML file from command line
        xml_file3 = self.get_xmlfile(dp_port_index)

        # Function call to set HPD Data during Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = UnPlugOldPlugNew,
        # plug_unplug_atsource = True, topology_after_resume = MST)
        self.set_low_power_state(1, port_type, enum.UnPlugOldPlugNew, True, topology_type3)

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

        # Set SD config and set mode
        self.set_config_apply_max_mode()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
