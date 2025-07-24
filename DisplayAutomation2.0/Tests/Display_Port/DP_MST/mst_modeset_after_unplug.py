########################################################################################################################
# @file         mst_modeset_after_unplug.py
# @brief        Test to check if driver is able to gracefully exit if modeset calls comes on an unplugged panel
# @details      Test Scenario:
#               1. Plug MST Panel and apply SD config.
#               2. Unplug the MST Panel.
#               3. Apply SD Config on the unplugged panel.
#
# @author       Praburaj Krishnan
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase


##
# @brief        This class contains runtest() method that performs negative testing to verify if SD config is applied
#               for unplugged MST panel
class DPMSTModesetOnUnpluggedPanel(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It applies and verifies the MST topology mentioned in the
    #               command line and applies SD config to the MST panel.Then unplugs the MST panel and tries to apply SD
    #               config to the unplugged panel to perform negative testing and fails the test if successful.
    # @return       None
    def runTest(self):
        cls = DisplayPortMSTBase

        # Variable for DP Port Number Index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        display_and_adapter_info_list = cls.get_current_display_and_adapter_info_list(is_lfp_info_required=False)

        is_success = cls.display_config.set_display_configuration_ex(enum.SINGLE, display_and_adapter_info_list)
        self.assertTrue(is_success, "Set Display Configuration Failed")

        self.set_hpd(port_type, False)

        # Fail the test case if applying Single Display config on an unplugged display is succeeding.
        logging.info("Applying Single Display config on display plugged at {}".format(port_type))
        status = cls.display_config.set_display_configuration_ex(enum.SINGLE, display_and_adapter_info_list)
        self.assertFalse(status, "[Test Issue] - Applying SD config on unplugged display at {} succeeded".format(port_type))
        logging.info("[Expected Behaviour] - SetTiming Failure is expected on an unplugged display")
        time.sleep(4) #WA - HSD:16024268525


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
