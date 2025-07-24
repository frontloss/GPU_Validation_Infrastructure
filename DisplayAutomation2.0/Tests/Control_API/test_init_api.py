########################################################################################################################
# @file         test_init_api.py
# @brief        Test calls for Control API's and verifies return status of the API with below scenarios.
#                   * Ze Device API (Level0 API from Control API).
#                   * Driver Disable / Enable.
#                   * Cleanup Control API.
#                   * Initialize Control API.
#                   * Enumerate Display API Post driver restart scenario.
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
# @brief - Verify Init/Close Control Library Test
class testInitCloseAPI(testBase):

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
            logging.info("Step_1: Get Device Properties")
            if control_api_wrapper.get_device_properties(deviceProperties, targetid):
                logging.info("Pass: Device Properties")
            else:
                logging.error("Fail: Device Properties")
                gdhm.report_driver_bug_clib("Get Device Properties Failed via Control Library for "
                                            "TargetId: {0}".format(targetid))
                self.fail("FAIL: Device Properties via Control Library")

            logging.info("Step_2: Close Control Library")
            if control_api_wrapper.close_ctl_api():
                logging.info("Pass: Close Control Library")
            else:
                logging.error("Fail: Close Control Library")
                gdhm.report_driver_bug_clib("Close Control Library Failed for "
                                            "TargetId: {0}".format(targetid))
                self.fail("Close Control Library Failed")

            default_version = control_api_args.CTL_MAKE_VERSION(control_api_args.CTL_IMPL_MAJOR_VERSION,
                                                                control_api_args.CTL_IMPL_MINOR_VERSION)
            default_uid = \
                control_api_args.ctl_application_id_t(0x372464b5, 0xd1b4, 0x419d,
                                                      [0x82, 0xe7, 0xef, 0xe5, 0x1b, 0x84, 0xfd, 0x8b])
            initargs = control_api_args.ctl_init_args(default_version, default_uid)
            logging.info("Step_4: Init Control Library")
            if control_api_wrapper.init_ctl_api(initargs):
                logging.info("Pass: Init Control Library")
            else:
                logging.error("Fail: Init Control Library")
                gdhm.report_driver_bug_clib("Init Control Library Failed for "
                                            "Version: {0} UID: {1}".format(default_version, default_uid))
                self.fail("Init Control Library Failed")

            logging.info("Step_5: Get Display Properties")
            if control_api_wrapper.get_display_properties(displayProperties, targetid):
                logging.info("Pass: Get Display Properties")
            else:
                logging.error("Fail: Get Display Properties")
                gdhm.report_driver_bug_clib("Get Display Properties Failed via Control Library for "
                                            "TargetId: {0}".format(targetid))
                self.fail("FAIL: Get Display Properties via Control Library")

            logging.info("Step_6: Negative UID test for Init Control Library")

            if control_api_wrapper.close_ctl_api():
                logging.info("PASS: Close Control Library")

                wrong_uid = control_api_args.ctl_application_id_t(0x111111, 0x1111, 0x111,
                                                                  [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11])
                initargs = control_api_args.ctl_init_args(default_version, wrong_uid)

                logging.info("Init Control Library for Negative Test")

                if control_api_wrapper.init_ctl_api(initargs) is False:
                    logging.info("Pass: Negative UID Test for Init Control Library")
                else:
                    logging.error("Fail: Negative UID Test for Init Control Library")
                    gdhm.report_driver_bug_clib("Negative UID Test for Init Control Library Failed for "
                                                "Version: {0} UID: {1}".format(default_version, default_uid))
                    self.fail("Negative UID Test for Init Control Library Failed")
            else:
                logging.info("FAIL: Close Control Library")
                gdhm.report_driver_bug_clib("Init Control Library Failed for "
                                            "Version: {0} UID: {1}".format(default_version, default_uid))
                self.fail("Close Control Library Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control Init/Close Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
