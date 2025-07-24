########################################################################################################################
# @file         test_retro_scaling.py
# @brief        Test calls for Retro Integer Scaling through Control Library and verifies return status of the API.
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
# @brief - Verify Get/Set Retro Scaling API Control Library Test
class testRetroIntegerScalingAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Get/Set Retro Scaling via Control Library")

        getRetroScalingArgs = control_api_args.ctl_retro_scaling_settings_t()
        getRetroScalingArgs.Size = ctypes.sizeof(getRetroScalingArgs)
        getRetroScalingArgs.Enable = True
        getRetroScalingArgs.RetroScalingType = control_api_args.ctl_retro_scaling_type_flags_v.INTEGER.value

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Get Retro Scaling via Control Library")
            if control_api_wrapper.get_set_retro_scaling(getRetroScalingArgs, targetid):
                logging.info("Pass:  Get Retro Scaling via Control Library")
                logging.info("Get Retro Scaling Enable - {}, Type - {}".format(getRetroScalingArgs.Enable,
                                                                               getRetroScalingArgs.RetroScalingType))
            else:
                logging.error("Fail: Get Retro Scaling via Control Library")
                gdhm.report_driver_bug_clib("Get Retro Scaling Failed via Control library for "
                                            "RetroScaling: {0} Enable: {1} TargetId: {2}"
                                            .format(getRetroScalingArgs.RetroScalingType,
                                            getRetroScalingArgs.Enable,targetid))
                self.fail("Get Retro Scaling Failed via Control Library")

        setRetroScalingArgs = control_api_args.ctl_retro_scaling_settings_t()
        setRetroScalingArgs.Size = ctypes.sizeof(setRetroScalingArgs)
        setRetroScalingArgs.Enable = True
        setRetroScalingArgs.RetroScalingType = control_api_args.ctl_retro_scaling_type_flags_v.INTEGER.value

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)

            logging.info("Step_2: Set Retro Scaling via Control Library")
            if control_api_wrapper.get_set_retro_scaling(getRetroScalingArgs, targetid):
                logging.info("Pass:  Set Retro Scaling via Control Library")
                logging.info("Set Retro Scaling Enable - {}, Type - {}".format(setRetroScalingArgs.Enable,
                                                                               setRetroScalingArgs.RetroScalingType))
            else:
                logging.error("Fail: Set Retro Scaling via Control Library")
                gdhm.report_driver_bug_clib("Set Retro Scaling Failed via Control Library for "
                                            "RetroScaling: {0} Enable: {1} TargetId: {2}"
                                            .format(setRetroScalingArgs.RetroScalingType,
                                            setRetroScalingArgs.Enable, targetid))
                self.fail("Set Retro Scaling Failed via Control Library")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control Library Get-Set Retro Scaling Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
