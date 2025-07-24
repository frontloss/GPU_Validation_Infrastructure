################################################################################################################
# @file          mst_tiled_1_input_sst_plug_unplug_panel.py
# @brief         Verify able to unplug SST tiled panel and able to plug back MST panel (MST disabled in OSD)
#                at the same port.
# @author        C, Diwakar
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that first applies and verifies SST tiled display mentioned in 1st
#               topology of commandline. Then unplugs it and plugs 2nd topology mentioned(MST) in the command line and
#               verify tiled mode for each of the MST panel.
class DPMSTTiledOneInputSSTHotplugUnplugDifferentPanel(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It initializes DP object, parse/send first topology in
    #               the commandline and issue HPD to Gfx driver.Fetches the list of all tiled display's target ids
    #               attached to the system.Here the list will have single item as only 1 tiled display is plugged.It
    #               applies the given config and max-mode and verifies if the tiled display is plugged properly or not
    #               and then unplugs it. Now it performs same steps for each of the MST panel present in 2nd topology
    #               mentioned in command line.
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
        self.set_tiled_mode(port_type, topology_type, xml_file)

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        # Set SD config and set mode
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

        # Issue HPD unplug (Hotplug interrupt) to graphics driver
        self.set_hpd(port_type, False)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get Topology XMl file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Initialize DP object, parse/send topology and issue HPD to Gfx driver
        self.set_tiled_mode(port_type, topology_type2, xml_file2)

        # Set SD config and set mode
        self.set_config_apply_max_mode()

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        for index in range(len(tiled_target_ids_list)):

            # TODO: Figure-out a way to ignore internal display (eDP/MIPI) for plug/unplug. For now,
            # hard-coded to target id of internal display

            if tiled_target_ids_list[index] in self.internal_display_target_id_list:
                # Internal display (MIPI/eDP) found! Ignore and proceed with next display in the list
                continue

            if is_tiled_display:
                # Verify tiled display function accepts arguments - is_mst, mst_status, is_sst_master_only,
                # tiled_target_id in order
                self.verify_tiled_display(False, False, True, tiled_target_ids_list[index])

            # MST disabled tiled external display found
            else:
                self.verify_tiled_display(True, False, False, tiled_target_ids_list[index])
                self.fail()

        # TODO: DPCD register should be read to confirm DP SST/MST panel active or not. After Simulation driver
        # supports native/remove DPCD, we will add code here to verify DPCD registers


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
