########################################################################################################################
# @file         test_set_huesaturation_api.py
# @brief        Test calls for Pixel Transformation API through Control Library and verifies return status of the API.
#                   * Set Pixel Transformation of Hue Saturation API.
# @author       Prateek Joshi
########################################################################################################################

import ctypes
import sys
import unittest
import logging
from copy import deepcopy

from Libs.Core import display_essential
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Control_API.control_api_base import testBase

##
# @brief - Set Hue Saturation Pixel Transformation Control Library Test
class testSetHueSatAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        argsSetCSCArgs = control_api_args.ctl_pixtx_pipe_set_config_t()
        argsSetCSCArgs.Size = ctypes.sizeof(argsSetCSCArgs)
        argsSetCSCArgs.OpertaionType = control_api_args.ctl_pixtx_config_opertaion_type_v.SET_CUSTOM.value

        blk_cfg = control_api_args.ctl_pixtx_block_config_t()
        blk_cfg.Config.BlockType = control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX.value

        logging.info("Matrix info {}".format(self.matrix_info))

        for row in range(0, 3):
            for column in range(0, 3):
                blk_cfg.Config.MatrixConfig.Matrix[row][column] = self.matrix_info[row][column]

        for row in range(0, 3):
            for column in range(0, 3):
                logging.info("Matrix {}".format(blk_cfg.Config.MatrixConfig.Matrix[row][column]))

        hue, sat = ctypes.c_double(28.0), ctypes.c_double(50.0)

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Set Hue Saturation for Hue=28, Sat=50")
            if control_api_wrapper.set_hue_saturation(argsSetCSCArgs, blk_cfg, hue, sat, targetid):
                logging.info("Pass: Set Hue Saturation Pixel Transformation")
            else:
                logging.error("Fail: Set Hue Saturation Pixel Transformation")
                gdhm.report_driver_bug_clib("Set Hue Saturation Pixel Transformation Failed via Control Library for "
                                            "OperationType: {0} Hue: {1} Sat: {2} TargetId: {3}"
                                            .format(argsSetCSCArgs.OpertaionType, hue, sat, targetid))
                self.fail("Set Hue Saturation Pixel Transformation Failed")

        hue, sat = ctypes.c_double(0.0), ctypes.c_double(100.0)

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Set Hue Saturation for Hue=0, Sat=100")
            if control_api_wrapper.set_hue_saturation(argsSetCSCArgs, blk_cfg, hue, sat, targetid):
                logging.info("Pass: Set Hue Saturation Pixel Transformation")
            else:
                logging.error("Fail: Set Hue Saturation Pixel Transformation")
                gdhm.report_driver_bug_clib("Set Hue Saturation Pixel Transformation Failed via Control Library for "
                                            "OperationType: {0} Hue: {1} Sat: {2} TargetId: {3}"
                                            .format(argsSetCSCArgs.OpertaionType, hue, sat, targetid))
                self.fail("Set Hue Saturation Pixel Transformation Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Set Hue Saturation API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
