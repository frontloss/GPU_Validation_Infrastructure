########################################################################################################################
# @file         test_get_gamma_api.py
# @brief        Test calls for Pixel Transformation API through Control Library and verifies return status of the API.
#                   * Get Pixel Transformation of Gamma API.
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
# @brief - Get Gamma Pixel Transformation Control Library Test
class testGetGammaAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        argsGetGammaArgs = control_api_args.ctl_pixtx_pipe_get_config_t()
        argsGetGammaArgs.Size = ctypes.sizeof(argsGetGammaArgs)
        argsGetGammaArgs.QueryType = control_api_args.ctl_pixtx_config_query_type_v.CURRENT.value

        argsLutConfig = control_api_args.ctl_pixtx_block_config_t()
        argsLutConfig.Size = ctypes.sizeof(argsLutConfig)

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)

            logging.info("Step_1: Get Gamma Pixel Transformation")
            if control_api_wrapper.get_gamma(argsGetGammaArgs, argsLutConfig, targetid):
                logging.info("Pass: Get Pixel Transformation")
            else:
                logging.error("Fail: Get Gamma Pixel Transformation")
                gdhm.report_driver_bug_clib("Get Gamma Pixel Transformation Failed via Control Library for "
                                            "Query Type: {0} TargetId: {1}"
                                            .format(argsGetGammaArgs.QueryType, targetid))
                self.fail("Get Gamma Pixel Transformation Failed")

        argsGetCaps = control_api_args.ctl_pixtx_pipe_get_config_t()
        argsGetCaps.Size = ctypes.sizeof(argsGetCaps)
        argsGetCaps.QueryType = control_api_args.ctl_pixtx_config_query_type_v.CAPABILITY.value

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)

            logging.info("Step_2: Get Capability Pixel Transformation")
            if control_api_wrapper.get_color_capability(argsGetCaps, targetid):
                logging.info("Pass: Get Capability Transformation")
                logging.info(" Input Pixel Format - {}".format(argsGetCaps.InputPixelFormat))
                logging.info(" Output Pixel Format - {}".format(argsGetCaps.OutputPixelFormat))
                logging.info(" Number of Blocks - {}".format(argsGetCaps.NumBlocks))
                logging.info(" BlockId - {}".format(argsGetCaps.pBlockConfigs.BlockId))
                logging.info(" BlockType - {}".format(argsGetCaps.pBlockConfigs.BlockType))
                logging.info(" NumSamplesPerChannel - {}"
                             .format(argsGetCaps.pBlockConfigs.Config.OneDLutConfig.NumSamplesPerChannel))
                logging.info(" NumChannels - {}".format(argsGetCaps.pBlockConfigs.Config.OneDLutConfig.NumChannels))
            else:
                logging.error("Fail: Get Capability Pixel Transformation")
                gdhm.report_driver_bug_clib("Get Capability Pixel Transformation Failed via Control Library for "
                                            "Query Type: {0} TargetId: {1}"
                                            .format(argsGetCaps.QueryType, targetid))
                self.fail("Get Capability Pixel Transformation Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Get Gamma API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)