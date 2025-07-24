########################################################################################################################
# @file         test_get_panel_descriptor.py
# @brief        Test calls for Get Panel Descriptor through Control Library.
#                   * Get Panel Descriptor API.
#                   * Get Panel Descriptor for extension blocks.
# @author       Prateek Joshi
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core import driver_escape
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Control_API.control_api_base import testBase


##
# @brief - Verify Panel Descriptor EDID/Display ID API Control Library Test
class testPanelDescriptorAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Panel Descriptor Access via Control Library")

        panelDescriptorArgs = control_api_args.ctl_panel_descriptor_access_args_t()
        panelDescriptorArgs.Size = ctypes.sizeof(panelDescriptorArgs)
        panelDescriptorArgs.OpType = control_api_args.ctl_operation_type.READ.value
        panelDescriptorArgs.BlockNumber = 0

        extPanelDespArgs = control_api_args.ctl_panel_descriptor_access_args_t()
        extPanelDespArgs.Size = ctypes.sizeof(extPanelDespArgs)
        extPanelDespArgs.OpType = control_api_args.ctl_operation_type.READ.value

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Call Panel Descriptor Data from Control Library")
            status, igcl_edid_data = control_api_wrapper.get_panel_descriptor(panelDescriptorArgs, extPanelDespArgs,
                                                                              targetid)
            if status is True:
                logging.info("Pass: Panel Descriptor via Control Library")
            else:
                logging.error("Fail: Panel Descriptor via Control Library")
                gdhm.report_driver_bug_clib("Get Panel Descriptor Failed via Control Library for "
                                            "TargetId: {0}"/format(targetid))
                self.fail("Panel Descriptor Read Failed via Control Library")

            for data_index in range(0, (panelDescriptorArgs.DescriptorDataSize + extPanelDespArgs.DescriptorDataSize)):
                logging.debug("Data: EDID Data {}".format(hex(igcl_edid_data[data_index])))

            edid_flag, driver_escape_edid_data, _ = driver_escape.get_edid_data(targetid)
            if edid_flag is True:
                for dataindex in range(0, 255):
                    if driver_escape_edid_data[dataindex] == igcl_edid_data[dataindex]:
                        logging.debug("EDID Data from IGCL - {} and Escape call - {} verified".format(
                            igcl_edid_data[dataindex], driver_escape_edid_data[dataindex]))
                logging.debug("EDID Data from IGCL and Escape call verified")
            else:
                logging.error("Failed to get EDID Data from Driver Escape Call for targetID {}".format(targetid))
                self.fail("Failed to get EDID Data from Driver Escape Call")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Panel Descriptor Access Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
