################################################################################################################
# @file         sst_mst_slave_sst_switch.py
# @brief        Verify whether switching happens from sst to mst slave transcoder
#               usage : sst_mst_slave_sst_switch.py -edp_a -dp_c
#               -plug_topologies MST_1B2M SST_TP_1 -dp_e -loglevel debug
# @author       Saradaa
################################################################################################################
import sys
import unittest
import logging
from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase


##
# @brief        The class contains runtest() method that sets and verifies the transcoder switch
#               happens between SST to MST Slave in a MST+SST topology

class DPSSTMSTSlaveSSTSwitch(DisplayPortMSTBase):
    ##
    # @brief        This method executes the actual test steps.It checks if requested port is present in free port list
    #               and fetches port type, topology type, xmlfile for 2 ports index and then applies and verifies the
    #               MST topology. Also applies the extended display configuration on displays
    #               given in commandline on all the displays to check transcoder re-assigment to MST Slave
    # @return       None
    def runTest(self):
        # Variable for DP Port Number Index from command line
        dp_port_index = 0
        cls = DisplayPortMSTBase

        # Get the port type from available free DP ports
        port_type1 = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        port_type2 = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(SST) from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get SST XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type1, topology_type, xml_file)

        # Function call to hot-plug DP SST panel needed for MST <--> SST switching
        self.setnverifySST(port_type2, topology_type2, xml_file2)

        # Get the display adaptor info list for both the ports
        display_and_adapter_info_list1 = cls.display_config.get_display_and_adapter_info_ex(port_type1, "gfx_0")
        display_and_adapter_info_sst = cls.display_config.get_display_and_adapter_info_ex(port_type2, "gfx_0")

        # Apply Extended on MST master and SST
        is_success = cls.display_config.set_display_configuration_ex(
            enum.EXTENDED, [display_and_adapter_info_list1[0], display_and_adapter_info_sst])
        self.assertTrue(is_success, "Set Display Configuration: EXTENDED config on MST master and SST Failed")

        # Apply Extended on MST master and MST Slave
        is_success = cls.display_config.set_display_configuration_ex(enum.EXTENDED, display_and_adapter_info_list1)
        self.assertTrue(is_success, "Set Display Configuration: EXTENDED config on MST Failed")

        # Apply Extended on MST master and SST
        is_success = cls.display_config.set_display_configuration_ex(
            enum.EXTENDED, [display_and_adapter_info_list1[0], display_and_adapter_info_sst])
        self.assertTrue(is_success, "Set Display Configuration: EXTENDED config on MST master and SST Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
