################################################################################################################
# @file          tiled_disable_enable_tiled_to_tiled.py
# @brief         Verifying  Sequence - Plug MST Tiled -> Unplug MST Tiled -> Restart Driver -> Plug SST Tiled -> Verify
# @author        Srinivas Kulkarni, Praburaj Krishnan
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *

##
# @brief        This class contains runTest() method that verifies switching from mst tiled topology to sst tiled at
#               same port during driver disable/enable
class TestMSTTiledToSSTTiled(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It plugs MST tiled panel from the first argument of plug
    #               topologies in the commandline to 1st port, applies max mode and performs tiled display verification.
    #               Then it unplugs MST tiled display and restarts the driver and plugs SST tiled display from 2nd
    #               argument of plug topologies in the commandline to the same port. It also plugs another SSt tiled
    #               display from 3rd plug topologies argument in the commandline to the second port.Max mode is applied
    #               and tiled display verification is performed
    # @return       None
    def runTest(self):

        # Points to the first display in the command line.
        dp_data_index = 0

        # Get First Free DP Port From the Free DP Port List.
        dp_port = self.get_dp_port_from_availablelist(0)

        # Get Topology Type(MST/SST) from the command line - MST
        topology_type = self.get_topology_type(dp_data_index)

        # Get xml file from the json file based on the index - MST Tiled Display
        xml_file = self.get_xmlfile(dp_data_index)

        # Tiled Display is being plugged in - MST Tiled Display.
        self.set_tiled_mode(dp_port, topology_type, xml_file)

        # Apply SD Config and Set Max Mode for the Tiled Display before verification - MST Tiled Display.
        self.set_config_apply_max_mode()

        # Get tiled displays list.
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()
        logging.info("Tiled Display List {}".format(tiled_target_ids_list))

        # Verify if the display is detected as Tiled Display - MST Tiled Display.
        if is_tiled_display:
            self.verify_tiled_display(True, True, True, tiled_target_ids_list[0])
        else:
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Verification of MST tiled display in tiled_disable_enable_"
                      "tiled_to_tiled test failed",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("MST Tiled Display Not Found! Exiting...")

        # Unplug the First Tiled Display - MST Tiled Display.
        self.set_hpd(dp_port, False)

        # Wait For the Graphics Driver to Reflect the Change in the Device Manager.
        time.sleep(15)

        # Restart the Driver After Unplug of First Tiled Display.
        is_success, reboot_required = display_essential.restart_gfx_driver()
        if is_success is True:
            logging.info('Successfully Disabled and Enabled Driver')
        else:
            self.fail('Failed to Disable and Enable Back the Driver.')
            # Gdhm bug reporting handled in restart_display_driver

        # Points to Second Display in the Command Line.
        dp_data_index = dp_data_index + 1

        # Get Topology Type(MST/SST) from the command line - SST.
        topology_type = self.get_topology_type(dp_data_index)

        # Get xml file from the json file based on the index - SST Master Tiled Display.
        xml_file = self.get_xmlfile(dp_data_index)

        # Tiled Display is being plugged in to the First Available Free DP Port - SST Master Tiled Display.
        # Plugging on the Same dp_port where MST Tiled Display was Previously Plugged.
        self.set_tiled_mode(dp_port, topology_type, xml_file)

        # Points to Third Display in the Command Line - SST Slave Tiled Display.
        dp_data_index = dp_data_index + 1

        # Get dp port from the free dp port list.
        dp_port = self.get_dp_port_from_availablelist(1)

        # Get Topology Type(MST/SST) from the command line - SST.
        topology_type = self.get_topology_type(dp_data_index)

        # Get xml file from the json file based on the index - SST Slave Tiled Display.
        xml_file = self.get_xmlfile(dp_data_index)

        # Tiled Display is being plugged in to the First Available Free DP Port - SST Slave Tiled Display.
        self.set_tiled_mode(dp_port, topology_type, xml_file, True)

        # Apply SD Config and Set Max Mode for the Tiled Display before verification - SST Tiled Display.
        self.set_config_apply_max_mode()

        # Get tiled displays list first - SST Tiled Display
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()
        logging.info("Tiled Display List {}".format(tiled_target_ids_list))

        # Verify if the display is detected as Tiled Display - SST Tiled Display.
        if is_tiled_display:
            self.verify_tiled_display(False, False, False, tiled_target_ids_list[0])
        else:
            logging.error("[Driver Issue]: SST Tiled Display Not Found! Exiting....")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Verification of SST tiled display in tiled_disable_enable_tiled_to_"
                      "tiled test failed",
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
