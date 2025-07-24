################################################################################################################
# @file          tiled_2_inputs_same_mst_disable_enable_nontiled_tiled_switching.py
# @brief         Verify able to switch from Non-tiled to Tiled during disable/enable of graphics driver.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that initially has 2 mst tiled topologies plugged at 2 ports and
#               then 2nd topology is hot unplugged and 3rd mst tiled topology is hot plugged to same port during driver
#               disable/enable
class DPTiledTwoInputMSTDisableEnableNonTiledtoTiled(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It plugs 1st MST tiled panel to 1st port, and 2nd MST
    #               tiled panel to 2nd port.Then 2nd mst tiled topology is unplugged and driver disable/enable is
    #               invoked. Once driver restart is successful, it plugs the 3rd mst tiled topology to the 1st port.Max
    #               mode is applied and tiled display verification is performed
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
        # Master port_type is being plugged in and panel is another DP MST panel
        self.set_tiled_mode(port_type2, topology_type2, xml_file2)

        # Unplug second port(DP MST Tiled Panel)
        self.set_hpd(port_type2, False)

        # Set index pointing to 3rd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type from the command line
        topology_type3 = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file3 = self.get_xmlfile(dp_port_index)

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

        # Parse and send topology to plug MST Tiled panel
        # Initialize the DP Port
        self.initialize_dp(port_type2, topology_type3)

        # Parse and Send Topology details to Gfx Sim driver from user
        self.parse_send_topology(port_type2, topology_type3, xml_file3)

        # Set SD config and apply max mode
        self.set_config_apply_max_mode()

        # Get tiled displays list again and check the status
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        if is_tiled_display:
            # Only one Tiled display is plugged and so it should be present at '0' index
            # Verify tiled display function accepts arguments - is_mst, mst_status, is_sst_master_only, tiled_target_id
            # in order
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
