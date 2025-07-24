################################################################################################################
# @file          mst_plug_unplug_diff_panel_power_event.py
# @brief         Verify whether SST/MST panel switching is working properly during power events.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *

##
# @brief        This class contains runTest() method that verifies is sst/mst panel switching is working properly during
#               power events
class DPSSTHotplugSSTHotPlugDifferentPowerEvents(DisplayPortMSTBase):

    ##
    # @brief        This runTest() executes the actual test steps.Set and verify the first topology which can be SST or
    #               MST. Then unplug the old topology and plug the 2nd topology from the commandline in low_power state
    #               and apply it.Invoke the power event and after resuming verify if the (2nd)current topology is SST
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

        # Get Topology Type from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to hotplug and verify SST Panel
        if topology_type == 'SST':
            self.setnverifySST(port_type, topology_type, xml_file)
        else:
            self.setnverifyMST(port_type, topology_type, xml_file)

        # Function call to set HPD Data during Low Power State
        # set_low_power_state(num_of_ports  = 1, port_type, sink_plugreq = UnPlugOldPlugNew,
        # plug_unplug_atsource = True, topology_after_resume = MST)
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

        ##
        # Read the DPCD 00h & check the HPD status
        #
        nativeDPCDRead = True
        dpcd_length = 1

        ##
        # Read the DPCD 00h for verifying Version of Panel
        dpcd_address = DPCD_VERSION_OFFSET

        # Function call to hotplug and verify SST Panel
        if topology_type == 'SST':
            version_reg_value = self.dpcd_read(port_type, nativeDPCDRead, dpcd_length, dpcd_address, None,
                                               action="VERSION")
            if version_reg_value == DPCD_VERSION_11:
                logging.info("The Connected Display is a SST Display")
            else:
                logging.error("[Test Issue]: The Connected Display is not a SST Display")
                self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
