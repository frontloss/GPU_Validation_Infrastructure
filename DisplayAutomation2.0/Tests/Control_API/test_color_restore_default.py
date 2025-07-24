########################################################################################################################
# @file         test_color_restore_default.py
# @brief        Test calls for Pixel Transformation API through Control Library and verifies return status of the API.
#                   * Restore Default value for 1DLUT, CSC, 3DLUT API.
# @author       Prateek Joshi
########################################################################################################################

import ctypes
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
# @brief - Restore Default Color value Control Library Test
class testColorRestoreDefault(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        argsRestoreDefaultArgs = control_api_args.ctl_pixtx_pipe_set_config_t()
        argsRestoreDefaultArgs.Size = ctypes.sizeof(argsRestoreDefaultArgs)
        argsRestoreDefaultArgs.OpertaionType = control_api_args.ctl_pixtx_config_opertaion_type_v.RESTORE_DEFAULT.value

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Restore Default Values for 1DLUT, CSC and 3DLUT Color API")
            if control_api_wrapper.restore_default(argsRestoreDefaultArgs, targetid):
                logging.info("Pass: Restore Default Values for 1DLUT, CSC and 3DLUT Color API")
            else:
                logging.error("Fail: Restore Default Values for 1DLUT, CSC and 3DLUT Color API")
                gdhm.report_driver_bug_clib("Restore Default Values failed for 1DLUT, CSC and 3DLUT "
                                            "Color API via Control Library, Operation Type: {0} for TargetId: {1}"
                                            .format(argsRestoreDefaultArgs.OpertaionType,targetid))
                self.fail("Restore Default Values for 1DLUT, CSC and 3DLUT Color API Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Restore Default for Color API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
