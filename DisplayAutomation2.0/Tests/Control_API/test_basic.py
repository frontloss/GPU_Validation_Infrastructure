########################################################################################################################
# @file         test_basic.py
# @brief        Test calls for Control Library and verifies return status of the API.
#                   * Enumerate Display API.
#                   * Device Properties API.
# @author       Prateek Joshi
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Libs.Core import display_essential
from Tests.Control_API.control_api_base import testBase

##
# @brief - Verify Basic API calls Control Library Test
class testBasicAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Control Library Basic")

        displayProperties = control_api_args.ctl_display_properties_t()
        displayProperties.Size = ctypes.sizeof(control_api_args.ctl_display_properties_t)

        deviceProperties = control_api_args.ctl_device_adapter_properties()
        deviceProperties.Size = ctypes.sizeof(deviceProperties)

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)

            logging.info("Step_1: Get Display Properties")
            if control_api_wrapper.get_display_properties(displayProperties, targetid):
                logging.info("Pass: Get Display Properties")
                logging.info("Display Target ID {}"
                             .format(displayProperties.Os_display_encoder_handle.WindowsDisplayEncoderID))
                logging.info("DisplayConfigFlags {}".format(displayProperties.DisplayConfigFlags))
            else:
                logging.error("Fail: Get Display Properties")
                gdhm.report_driver_bug_clib("Get Display Properties Failed via Control Library for targerId: {0}"
                                            .format(targetid))
                self.fail("FAIL: Get Display Properties")

            logging.info("Step_2: Get Device Properties")
            if control_api_wrapper.get_device_properties(deviceProperties, targetid):
                logging.info("Pass: Device Properties")
                logging.info("Name {}".format(deviceProperties.name))
                logging.info("Vendor-ID {}".format(deviceProperties.pci_vendor_id))
                logging.info("Device-ID {}".format(deviceProperties.pci_device_id))
                logging.info("Rev-ID {}".format(deviceProperties.rev_id))
            else:
                logging.error("Fail: Device Properties")
                gdhm.report_driver_bug_clib("Get Display Properties Failed via Control Library for targerId: {0}"
                                            .format(targetid))
                self.fail("FAIL: Device Properties")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control basic Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
