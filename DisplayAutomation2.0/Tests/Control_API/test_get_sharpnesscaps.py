########################################################################################################################
# @file         test_get_sharpnesscaps.py
# @brief        Test calls for Get, Set Sharpness and Get Sharpness Caps through Control Library.
#                   * Get Sharpness API.
#                   * Set Sharpness API.
#                   * Get Sharpness Caps API.
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
from Tests.Control_API.control_api_base import testBase

##
# @brief - Verify Sharpness Caps API Control Library Test
class testSharpnessCapsAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Sharpness via Control Library")

        gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        gfx_adapter_index = 'gfx_0'
        adapter_info = gfx_adapter_dict[gfx_adapter_index]
        targetid = display_config.DisplayConfiguration().get_target_id(self.connected_list[0], self.enumerated_displays)

        SharpnessCaps = control_api_args.ctl_sharpness_caps()
        SharpnessCaps.Size = ctypes.sizeof(SharpnessCaps)

        logging.info("Step_1: Call Sharpness Caps")
        if control_api_wrapper.get_sharpness_caps(SharpnessCaps, targetid):
            logging.info("Pass: Sharpness Caps via Control Library")
        else:
            logging.error("Fail: Sharpness Caps via Control Library")
            gdhm.report_driver_bug_clib("Get Sharpness Failed via Control Library for "
                                        "Adapter: {0} TargetId: {1} SuportedFilter: {2}"
                                        .format(gfx_adapter_index,targetid,
                                                SharpnessCaps.SupportedFilterFlags))
            self.fail("Sharpness Caps Failed via Control Library")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Sharpness Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
