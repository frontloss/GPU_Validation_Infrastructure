################################################################################################################
# @file          tiled_1_input_sst_1_input_mst_plug_unplug_nontiled_to_tiled.py
# @brief         Verify able to unplug SST tiled panel and able to plug back MST panel at the same port during power
#                events.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that plugs SST tiled panel to master port and MST tiled panel to
#               slave port and verifies tiled mode. And then unplugs the MST tiled panel from slave port and plugs SST
#               tiled panel to the same port and performs tiled display verification
class DPMSTTiledOneInputSSTOneInputMSTHotplugUnplugNonTiledtoTiled(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps. It first plugs the DP SST Tiled Panel mentioned as 1st
    #               plug_topologies argument in commandline to master port and then plugs DP MST Tiled panel mentioned
    #               as 2nd plug_topologies argument in commandline to slave port. And then applies max mode and performs
    #               tiled display verification.It then unplugs MST tiled display topology from slave port and to the
    #               same slave port it plugs the other DP SST tiled display mentioned as 3rd plug_topology argument in
    #               commandline. Then it applies max mode and performs tiled display verification
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
        # Plug DP SST Panel here
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
        # Slave port_type is being plugged in and panel is DP MST Tiled panel
        self.set_tiled_mode(port_type2, topology_type2, xml_file2, True)

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        # Set SD config and apply max mode
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

        # Unplug Slave port(DP MST Tiled Panel)
        self.set_hpd(port_type2, False, True)

        # Set index pointing to 3rd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type(SST) from the command line
        topology_type3 = self.get_topology_type(dp_port_index)

        # Get SST XML file from command line
        xml_file3 = self.get_xmlfile(dp_port_index)

        # Initialize DP object, parse/send topology and issue HPD to driver with the configuration passed by the user
        # Slave port_type is being plugged in with different DP SST panel
        self.set_tiled_mode(port_type2, topology_type3, xml_file3, True)

        # Set SD config and apply max mode
        self.set_config_apply_max_mode()

        # Get tiled displays list
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


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
