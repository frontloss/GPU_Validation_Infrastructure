################################################################################################################
# @file          tiled_disable_enable_2_pipe_to_1_pipe_tiled.py
# @brief         Verify able to unplug SST tiled panel and able to plug back SST Tiled panel at the same port.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that verifies switching from 2 pipe sst tiled mode to 1 pipe sst
#               tiled mode during driver disable/enable
class DPMSTTiledDisableEnableTwoPipeTiledtoOnePipeTiled(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It plugs 1st SST tiled panel to 1st port, and 2nd SST
    #               tiled panel to 2nd port.This will consume 2 pipes. It applies max mode and performs tiled display
    #               verification and then unplugs sst tiled topology from 2nd port.Now Driver is disabled and MST
    #               tiled topology from 3rd argument in commandline is plugged to 1st port.Now it is switched to single
    #               pipe.And then the driver is enabled, max mode is applied and tiled display verification is performed
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

        # Wait for the graphics driver to be enabled and reflect the changes in device manager
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Set SD config and set mode
        self.set_config_apply_max_mode()

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

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

        # Disable graphics driver
        disable_status = display_essential.disable_driver()

        # Wait for the graphics driver to be disabled and reflect the changes in device manager
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        if disable_status:
            logging.info("Graphics driver was disabled Successfully ....")
        else:
            logging.error("[Driver Issue]: Graphics driver failed to be disabled. Exiting !!!!")
            # Gdhm bug reporting handled in disable_driver()
            self.fail()

        # Set index pointing to 3rd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type(MST/SST) from the command line
        topology_type3 = self.get_topology_type(dp_port_index)

        # Get MST XML file from command line
        xml_file3 = self.get_xmlfile(dp_port_index)

        # Parse and send topology to plug MST Tiled panel
        # Initialize the DP Port
        self.initialize_dp(port_type, topology_type3)

        # Plug same topology with only one 1 input MST Tiled panel
        self.parse_send_topology(port_type, topology_type3, xml_file3)

        # Enable graphics driver
        enable_status = display_essential.enable_driver()

        # Wait for the graphics driver to be enabled and reflect the changes in device manager
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        if enable_status:
            logging.info("Graphics driver was enabled Successfully ....")
        else:
            logging.error("[Driver Issue]: Graphics driver failed to be enabled. Exiting !!!!")
            # Gdhm bug reporting handled in enable_driver()
            self.fail()

        # Set SD config and set mode
        self.set_config_apply_max_mode()

        # Get tiled displays list again and check the status
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        if is_tiled_display:
            # Only one Tiled display is plugged and so it should be present at '0' index
            # Verify tiled display function accepts arguments - is_mst, mst_status, is_sst_master_only, tiled_target_id
            # in order
            self.verify_tiled_display(True, True, False, tiled_target_ids_list[0])
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

        # TODO: DPCD register should be read to confirm DP SST/MST panel active or not. After Simulation driver
        # supports native/remove DPCD, we will add code here to verify DPCD registers


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
