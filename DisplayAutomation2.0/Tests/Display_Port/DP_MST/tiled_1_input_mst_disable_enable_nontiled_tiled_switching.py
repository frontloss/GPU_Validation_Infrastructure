################################################################################################################
# @file          tiled_1_input_mst_disable_enable_nontiled_tiled_switching.py
# @brief         Verify able to switch from Non-tiled to Tiled during hotplug/unplug.
# @author        Srinivas Kulkarni
################################################################################################################
import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() that plugs and verifies switch from Non-tiled to Tiled during
#               hotplug/unplug and with disable/enable of driver
class DPTiledOneInputMSTDisableEnableNonTiledtoTiled(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It first plugs MST Non-tiled panel and apply max mode.It
    #               fails the test if any tiled display is found.Then non-tiled MST panel is unplugged and display
    #               driver is disabled.Now MST tiled panel is plugged and display driver is enabled and once again apply
    #               max mode and perform tiled display verification.
    # @return - None
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
        # Plug DP MST Non-Tiled Panel here
        self.set_tiled_mode(port_type, topology_type, xml_file)

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        # Set SD config and apply Maximum mode supported
        self.set_config_apply_max_mode()

        if is_tiled_display:
            logging.error("[Driver Issue]: Tiled display not found! Exiting....")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Verification of tiled display failed",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        # Wait for the DP MST Tiled Panel to be unplugged
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get Topology XMl file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Disable graphics driver
        disable_status = display_essential.disable_driver()

        # Wait for the graphics driver to be disabled and reflect the changes in device manager
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        if disable_status:
            logging.info("Graphics driver was disabled Successfully ....")
        else:
            logging.error("[Driver Issue]: Graphics driver failed to be disabled. Exiting !!!!")
            # Gdhm bug reporting handled in disable_driver
            self.fail()

        # Parse and send topology to plug MST Tiled panel
        # Initialize the DP Port
        self.initialize_dp(port_type, topology_type2)

        # Parse and Send Topology details to Gfx Sim driver from user
        self.parse_send_topology(port_type, topology_type2, xml_file2)

        # Enable graphics driver
        enable_status = display_essential.enable_driver()

        # Wait for the graphics driver to be enabled and reflect the changes in device manager
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        if enable_status:
            logging.info("Graphics driver was enabled Successfully ....")
        else:
            logging.error("[Driver Issue]: Graphics driver failed to be enabled. Exiting !!!!")
            # Gdhm bug reporting handled in disable_driver
            self.fail()

        # Set SD config and apply Maximum mode supported
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
