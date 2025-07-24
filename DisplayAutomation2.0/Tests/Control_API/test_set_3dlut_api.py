########################################################################################################################
# @file         test_set_3dlut_api.py
# @brief        Test calls for Pixel Transformation API through Control Library and verifies return status of the API.
#                   * Set Pixel Transformation of 3DLUT API.
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
from Tests.Color.Common import color_constants
from Tests.Control_API.control_api_base import testBase

##
# @brief - Set 3DLUT Pixel Transformation Control Library Test
class testSet3DLUTAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        argsSet3dlutArgs = control_api_args.ctl_pixtx_pipe_set_config_t()
        argsSet3dlutArgs.Size = ctypes.sizeof(argsSet3dlutArgs)
        argsSet3dlutArgs.OpertaionType = control_api_args.ctl_pixtx_config_opertaion_type_v.SET_CUSTOM.value

        argsLutConfig = control_api_args.ctl_pixtx_block_config_t()
        argsLutConfig.Size = ctypes.sizeof(argsLutConfig)
        argsLutConfig.BlockType = control_api_args.ctl_pixtx_block_type_v._3D_LUT.value

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Set 3DLUT Pixel Transformation")
            if control_api_wrapper.set_3dlut(argsSet3dlutArgs, argsLutConfig, targetid):
                logging.info("Pass: Set 3DLUT Pixel Transformation")
            else:
                logging.error("Fail: Set 3DLUT Pixel Transformation")
                gdhm.report_driver_bug_clib("Set 3DLUT Pixel Transformation Failed via Control Library for "
                                            "BlockType: {0} Config: {1} TargetId: {2}"
                                            .format(argsLutConfig.BlockType,argsLutConfig.Config,targetid))
                self.fail("Set 3DLUT Pixel Transformation Failed")

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info(" TEARDOWN: testSet3DLUTAPI ")

        argsRestoreDefaultArgs = control_api_args.ctl_pixtx_pipe_set_config_t()
        argsRestoreDefaultArgs.Size = ctypes.sizeof(argsRestoreDefaultArgs)
        argsRestoreDefaultArgs.OpertaionType = control_api_args.ctl_pixtx_config_opertaion_type_v.RESTORE_DEFAULT.value

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Restore Default Values for Color API")
            if control_api_wrapper.restore_default(argsRestoreDefaultArgs, targetid):
                logging.info("Restore Default Values for Color API Successfull")
            else:
                logging.error("Restore Default Values for Color API Failed")

        super(testSet3DLUTAPI, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Set 3DLUT API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)