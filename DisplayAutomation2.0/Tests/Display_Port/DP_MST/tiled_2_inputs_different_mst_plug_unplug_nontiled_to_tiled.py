################################################################################################################
# @file          tiled_2_inputs_different_mst_plug_unplug_nontiled_to_tiled.py
# @brief         Verify able to switch from Non-tiled to Tiled during hotplug/unplug.
# @author        Srinivas Kulkarni
################################################################################################################

import sys

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that initially has 2 mst tiled topologies plugged and then 2nd
#               topology is hot unplugged and 3rd mst tiled topology is hot plugged to same port
class DPTiledTwoInputDifferentMSTHotplugUnplugNonTiledtoTiled(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It plugs 1st MST tiled panel to 1st port, and 2nd MST
    #               tiled panel to 2nd port.Then 2nd mst tiled topology is unplugged and 3rd mst tiled topology from
    #               commandline is plugged to 1st port. Max mode is applied and tiled display verification is performed
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
        # Master port_type is being plugged in and panel is another DP MST Tiled Panel
        self.set_tiled_mode(port_type2, topology_type2, xml_file2)

        # Unplug Second port(DP MST Tiled Panel)
        self.set_hpd(port_type2, False)

        # Set index pointing to 3rd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type from the command line
        topology_type3 = self.get_topology_type(dp_port_index)

        # Get Topology XMl file from command line
        xml_file3 = self.get_xmlfile(dp_port_index)

        # Initialize DP object, parse/send topology and issue HPD to driver with the configuration passed by the user
        # Master port_type is being plugged in and panel is another DP MST panel
        self.set_tiled_mode(port_type, topology_type3, xml_file3)

        # Set SD config and apply max mode
        self.set_config_apply_max_mode()

        # Get tiled displays list first
        is_tiled_display, tiled_target_ids_list = self.get_tiled_displays_list()

        if is_tiled_display:
            logging.info("Tiled display(s) found %s" % tiled_target_ids_list)
            # Only one Tiled display is plugged and so it should be present at '0' index
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
