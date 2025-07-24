########################################################################################################################
# @file         mpo_3d_app_tiled_mst.py
# @brief        Basic test to verify register programming and also check for underrun while running a 3D application on
#               Tiled display.
#               * Get the port type from available free DP ports.
#               * Plug the tiled display.
#               * Set display configuration and apply max mode.
#               * Get tiled displays list.
#               * Verify if the display is detected as Tiled Display - MST Tiled Display.
#               * Run 3D application.
#               * Verify plane programming.
#               * Close 3D application.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import winkb_helper
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ui_tiled_mst_base

##
# @brief    Contains function to check register programming and underrun while running a 3D application on Tiled display
class MPO3DAppTiledMSTBase(mpo_ui_tiled_mst_base.MPOUITiledMSTBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        ##
        # Expected pixel format
        pixel_format = self.mpo_helper.get_pixel_format_value('RGB8888')

        ##
        # Variable for DP Port Number Index
        dp_port_index = 0

        ##
        # Requested ports should be present in free port list
        if not set(self.mst_base.dp_ports_to_plug).issubset(set(self.free_port_list)):
            self.fail("Not Enough free ports available. Exiting")

        ##
        # Get the port type from available free DP ports
        port_type = self.mst_base.get_dp_port_from_availablelist(dp_port_index)

        ##
        # Get Topology Type from the command line
        topology_type = self.mst_base.get_topology_type(dp_port_index)

        ##
        # Get Topology XML file from command line
        xml_file = self.mst_base.get_xmlfile(dp_port_index)

        ##
        # Tiled Display is being plugged in - MST Tiled Display.
        self.mst_base.set_tiled_mode(port_type, topology_type, xml_file)

        ##
        # Set display config and apply max mode
        self.mst_base.set_config_apply_max_mode()

        ##
        # Get tiled displays list.
        is_tiled_display, tiled_target_ids_list = self.mst_base.get_tiled_displays_list()
        logging.info("Tiled Display List {}".format(tiled_target_ids_list))

        # Verify if the display is detected as Tiled Display - MST Tiled Display.
        if is_tiled_display:
            self.mst_base.verify_tiled_display(True, True, True, tiled_target_ids_list[0])
        else:
            self.fail("MST Tiled display not found")

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Run 3D application
        self.mpo_helper.play_3d_app(True)

        time.sleep(60)

        ##
        # Verify plane programming
        logging.info("************************Plane verification started************************")
        if not self.mpo_helper.verify_planes_mst(pixel_format, 'PLANE_CTL_1'):
            gdhm.report_bug(
                title="[MPO]Plane verification failed while playing 3D application on Tiled display",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Plane verification failed while playing 3D application on Tiled display")
        else:
            logging.info("Plane verification passed while running 3D application on Tiled display")
        logging.info("*************************Plane verification ended*************************")

        ##
        # Close 3D application
        self.mpo_helper.app3d.close_app()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify for register programming and also check for underrun"
                 "while running a 3D application on Tiled Display")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)