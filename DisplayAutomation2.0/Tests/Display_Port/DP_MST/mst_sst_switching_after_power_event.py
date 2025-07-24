################################################################################################################
# @file          mst_sst_switching_after_power_event.py
# @brief         Verify topology switching from MST to SST during power events is proper or not.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from  Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method which verifies the topology switch from MST to SST and vice-versa
#               after resuming from power event
class DPMSTtoSSTSwitchingPowerEvents(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It first applies the MST topology mentioned in the
    #               command line and verifies it.It invokes power event and then switches to SST topology mentioned in
    #               the command line after resuming from power event.Then hotunplug is issued to disconnect all the SST
    #               displays.Now it applies the SST topology and verifies it, invokes power event and then switches to
    #               MST topology and verifies it after resuming from power event.
    # @return       None
    def runTest(self):
        # Variable for DP Port Number Index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type(SST) from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get SST XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)

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

        # Function call to hot-plug DP SST panel needed for MST <--> SST switching
        self.setnverifySST(port_type, topology_type2, xml_file2)

        # Disconnect DP SST display(s) by issuing HPD
        self.set_hpd(port_type, False)

        # Function call to hot-plug DP SST panel needed for MST <--> SST switching
        self.setnverifySST(port_type, topology_type2, xml_file2)

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

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
