########################################################################################################################
# @file         test_set_gamma_api.py
# @brief        Test calls for Pixel Transformation API through Control Library and verifies return status of the API.
#                   * Set Pixel Transformation of Gamma API.
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
# @brief - Set Gamma Pixel Transformation Control Library Test
class testSetGammaAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        gfx_adapter_index = 'gfx_0'
        adapter_info = gfx_adapter_dict[gfx_adapter_index]

        argsSetGammaArgs = control_api_args.ctl_pixtx_pipe_set_config_t()
        argsSetGammaArgs.Size = ctypes.sizeof(argsSetGammaArgs)
        argsSetGammaArgs.OpertaionType = control_api_args.ctl_pixtx_config_opertaion_type_v.SET_CUSTOM.value
        gamma_lut_values = color_constants.SRGB_ENCODE_515_SAMPLES_16BPC

        argsBlkCfg = control_api_args.ctl_pixtx_block_config_t()
        argsBlkCfg.Size = ctypes.sizeof(argsBlkCfg)
        argsBlkCfg.BlockType = control_api_args.ctl_pixtx_block_type_v._1D_LUT.value

        output_sample_values = (ctypes.c_double * len(gamma_lut_values))()
        ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

        for ind in range(0, len(gamma_lut_values)):
            output_sample_values[ind] = min(1.2 * gamma_lut_values[ind], 1.0)

        for index in range(0, len(gamma_lut_values)):
            output_sample_values[index] = min(1.2 * gamma_lut_values[index], 1.0)
            argsBlkCfg.Config.OneDLutConfig.pSampleValues[3 * index] = output_sample_values[index]
            argsBlkCfg.Config.OneDLutConfig.pSampleValues[3 * index + 1] = output_sample_values[index]
            argsBlkCfg.Config.OneDLutConfig.pSampleValues[3 * index + 2] = output_sample_values[index]

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Set Gamma Pixel Transformation")
            if control_api_wrapper.set_gamma(argsSetGammaArgs, argsBlkCfg, targetid):
                logging.info("Pass: Set Gamma Pixel Transformation")
            else:
                logging.error("Fail: Set Gamma Pixel Transformation")
                gdhm.report_driver_bug_clib("Set Gamma Pixel Transformation Failed via Control Library for "
                                            "OperationType: {0} TargetId: {1}"
                                            .format(argsSetGammaArgs.OpertaionType,targetid))
                self.fail("Set Gamma Pixel Transformation Failed")

            argsGetGammaArgs = control_api_args.ctl_pixtx_pipe_get_config_t()
            argsGetGammaArgs.Size = ctypes.sizeof(argsGetGammaArgs)
            argsGetGammaArgs.QueryType = control_api_args.ctl_pixtx_config_query_type_v.CURRENT.value

            argsLutConfig = control_api_args.ctl_pixtx_block_config_t()
            argsLutConfig.Size = ctypes.sizeof(argsLutConfig)

            logging.info("Step_2: Get Gamma Pixel Transformation")
            if control_api_wrapper.get_gamma(argsGetGammaArgs, argsLutConfig, targetid):
                logging.info("Pass: Get Pixel Transformation")
                for index in range(0, len(gamma_lut_values)):
                    logging.debug("pSampleValues {} ".format(argsLutConfig.Config.OneDLutConfig.pSampleValues[index]))
            else:
                logging.error("Fail: Get Gamma Pixel Transformation")
                gdhm.report_driver_bug_clib("Get Gamma Pixel Transformation Failed via Control Library for "
                                            "QueryType: {0} TargetId: {1}".format(
                                                argsGetGammaArgs.QueryType,targetid
                                            ))
                self.fail("Get Gamma Pixel Transformation Failed")

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info(" TEARDOWN: testSetGammaAPI ")

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

        super(testSetGammaAPI, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Set Gamma API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)