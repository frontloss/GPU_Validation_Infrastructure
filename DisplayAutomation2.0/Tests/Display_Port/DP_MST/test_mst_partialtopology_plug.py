################################################################################################################
# @file         test_mst_partialtopology_plug.py
# @brief        Verify Sub topology Plug functionality
# @author       Veena, Veluru
################################################################################################################
import sys
import logging
import unittest

from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase


##
# @brief        This class has basic test to verify MST sub topopology plug 
class TestDpMSTPartialTopology(DisplayPortMSTBase):

    ##
    # @brief        Basic test case to verify if A branch/display's plug over an existing mst topology
    # @return       None
    def runTest(self) -> None:
        dp_port_index = 0

         # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)
        
        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        display_config = eval(f"enum.{self.config}")

        display_and_adapter_info_list = self.display_config.get_display_and_adapter_info_ex(port_type, 'gfx_0')
        if type(display_and_adapter_info_list) != list:
            display_and_adapter_info_list = [display_and_adapter_info_list]
        num_of_displays_mst_topo = len(display_and_adapter_info_list)

        modeset_status = self.display_config.set_display_configuration_ex(display_config, display_and_adapter_info_list)
        self.assertTrue(modeset_status, "FAIL: Failed to apply display configuration before partial topology plug")

        # Get Topology XML file from command line
        dp_port_index = dp_port_index + 1
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Construct RAD object for the subtopology to plug
        node_rad_obj = self.construct_node_rad(dp_port_index)

        # Connect MST branch/leaf to original Topology
        self.set_partial_topology(port_type, True, node_rad_obj, xml_file2)

        display_and_adapter_info_list = self.display_config.get_display_and_adapter_info_ex(port_type, 'gfx_0')
        if type(display_and_adapter_info_list) != list:
            display_and_adapter_info_list = [display_and_adapter_info_list]
        num_of_displays_after_partial_plug = len(display_and_adapter_info_list)

        if num_of_displays_after_partial_plug == num_of_displays_mst_topo + 1:
            logging.info(f'PASS: Partial Topology successfully got plugged in MST Topology')
        else:
            gdhm.report_test_bug_di("[MST] Partial Topology Plug is not successful")
            self.fail(f'FAIL: MST Partial Topology Plug is not successful')

        self.config = "EXTENDED"
        display_config = eval(f"enum.{self.config}")
        modeset_status = self.display_config.set_display_configuration_ex(display_config, display_and_adapter_info_list)
        self.assertTrue(modeset_status, "FAIL: Failed to apply display configuration after partial topology plug")      
       

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
