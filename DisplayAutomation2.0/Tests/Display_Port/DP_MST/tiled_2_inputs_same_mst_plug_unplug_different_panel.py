################################################################################################################
# @file          tiled_2_inputs_same_mst_plug_unplug_different_panel.py
# @brief         Verify able to unplug SST tiled panel and able to plug back MST panel at the same port during power
#                events.
# @author        C Diwakar
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that initially has 2 sst tiled topologies plugged at 2 ports and
#               then 2nd topology is hot unplugged.To the same port mst tiled panel with mst disabled mode in osd is
#               plugged and tiled display verification is performed on all the panels except internal displays
class DPTTiled_Two_Inputs_SameMST_HotplugUnplug_different_Panel(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It plugs 1st SST tiled panel to 1st port, and 2nd SST
    #               tiled panel to 2nd port and applies max mode.Then 1st sst tiled topology is unplugged and to the
    #               same port mst tiled panel with mst disabled mode in osd is plugged and max mode is applied.Tiled
    #               display verification is performed on all the panels except internal displays
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

        # Initialize DP object,parse/send topology and issue HPD to driver with the configuration passed by the user
        # Master port_type is being plugged in
        self.set_tiled_mode(port_type, topology_type, xml_file)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get the port type from available free DP ports
        port_type2 = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get MST XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Initialize DP object,parse/send topology and issue HPD to driver with the configuration passed by the user
        # Slave port_type is being plugged in
        self.set_tiled_mode(port_type2, topology_type2, xml_file2, True)

        # Set SD config and set mode
        self.set_config_apply_max_mode()

        # Issue HPD (Hotplug interrupt) to graphics driver
        self.set_hpd(port_type, False)

        # Set index pointing to 3rd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type from the command line
        topology_type3 = self.get_topology_type(dp_port_index)

        # Get Topology XMl file from command line
        xml_file3 = self.get_xmlfile(dp_port_index)

        # Initialize DP object, parse/send topology and issue HPD to Gfx driver
        self.set_tiled_mode(port_type, topology_type3, xml_file3)

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
                self.verify_tiled_display(False, False, False, tiled_target_ids_list[index])

            # MST disabled tiled external display found
            else:
                self.verify_tiled_display(True, False, False, tiled_target_ids_list[index])


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
