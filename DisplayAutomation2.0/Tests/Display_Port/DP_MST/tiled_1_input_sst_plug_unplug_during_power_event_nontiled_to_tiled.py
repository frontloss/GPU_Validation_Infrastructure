################################################################################################################
# @file          tiled_1_input_sst_plug_unplug_during_power_event_nontiled_to_tiled.py
# @brief         Verify able to switch from Non-tiled to Tiled during hotplug/unplug and with power events.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that switches from one SST tiled panel to other sst tiled panel on
#               the same port during power event
class DPTiledOneInputSSTHotplugUnplugNonTiledtoTiledDuringPowerEvents(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It plugs SST tiled panel to master port, applies max mode
    #               and performs tiled display verification.Now 1st sst tiled display is unplugged and 2nd sst tiled
    #               display from the commandline is plugged to same port and supported power event(s3/cs) is invoked.
    #               After resuming from the power event max mode is applied and tiled display verification is performed
    # @return       None
    def runTest(self):

        # Variable for DP port number index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get SST XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Initialize DP object, parse/send topology and issue HPD to Gfx driver
        # Plug DP SST Master Tiled Panel here
        self.set_tiled_mode(port_type, topology_type, xml_file)

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        # Set SD config and apply Maximum mode supported
        self.set_config_apply_max_mode()

        if is_tiled_display:
            logging.info("Tiled display(s) found %s" % tiled_target_ids_list)
            # Only one Tiled display is plugged and so it should be present at '0' index
            self.verify_tiled_display(False, False, True, tiled_target_ids_list[0])
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

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get Topology XMl file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to set HPD Data during Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = UnPlugOldPlugNew,
        # plug_unplug_atsource = True, topology_after_resume = SST)
        self.set_low_power_state(1, port_type, enum.UnPlugOldPlugNew, True, topology_type2)

        # Send the SST XML Data to Gfx Simulation Driver
        self.parse_send_topology(port_type, topology_type2, xml_file2, True)

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

        # Set SD config and apply Maximum mode supported
        self.set_config_apply_max_mode()

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        if is_tiled_display:
            logging.info("Tiled display(s) found %s" % tiled_target_ids_list)
            # Only one Tiled display is plugged and so it should be present at '0' index
            self.verify_tiled_display(False, False, True, tiled_target_ids_list[0])
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
