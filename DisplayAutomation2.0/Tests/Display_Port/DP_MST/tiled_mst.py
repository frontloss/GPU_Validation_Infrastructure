################################################################################################################
# @file          tiled_mst.py
# @brief         Verify able to apply basic MST tiled mode
# @author        C, Diwakar
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that verifies application of basic MST tiled mode
class DPMSTTiledBasic(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It plugs MST tiled panel to 1st port,applies max mode and
    #               performs tiled display verification
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
        # to set one MST branch to which SST master tile only attached
        self.set_tiled_mode(port_type, topology_type, xml_file)

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        # Set SD config and set mode
        self.set_config_apply_max_mode()

        if is_tiled_display:
            # Only one Tiled display is plugged and so it should be present at '0' index
            # Verify tiled display function accepts arguments - is_mst, mst_status, is_sst_master_only, tiled_target_id
            # in order
            self.verify_tiled_display(True, True, False, tiled_target_ids_list[0])
        else:
            logging.error("[Driver Issue]: Tiled display not found! Exiting....")
            gdhm.report_bug(
                "title=[Interfaces][DP_MST] Verification of tiled display failed",
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
