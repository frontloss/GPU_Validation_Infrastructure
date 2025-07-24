########################################################################################################################
# @file         test_ze_api.py
# @brief        Test calls for Ze Device (level0 Api) from Control API and verifies return status of the API.
#                   * Ze Device API (Level0 API from Control API).
#                   * Driver Disable / Enable.
#                   * Cleanup Control API.
#                   * Initialize Control API.
#                   * Ze Device API (Level0 API from Control API).
# @author       Prateek Joshi
########################################################################################################################

import sys
import unittest
import logging

from Libs.Core import display_essential
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Control_API.control_api_base import testBase

##
# @brief - Ze Device Control Library Test
class testZeDeviceAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        zeDevice = control_api_args.ze_device_module_properties_t()

        logging.info("Step_1: Get Ze Device Properties")
        if control_api_wrapper.get_zedevice(zeDevice):
            if zeDevice.spirvVersionSupported == 65538:
                logging.info("ZeDevice Properties {}".format(zeDevice.spirvVersionSupported))
                logging.info("Pass: Ze Device Properties")
            elif zeDevice.spirvVersionSupported == 0:
                logging.info("ZeDevice Properties is unsupported {}".format(zeDevice.spirvVersionSupported))
        else:
            logging.error("Fail: Ze Device Properties")
            gdhm.report_driver_bug_clib("Get Ze Device Properties Failed via Control Library for "
                                        "Flags: {0} Stype: {1}".format(zeDevice.flags,zeDevice.stype))
            self.fail("Ze Device Properties Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test Purpose: Test Control Ze Device Library Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
