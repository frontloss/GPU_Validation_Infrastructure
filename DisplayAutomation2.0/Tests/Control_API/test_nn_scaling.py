########################################################################################################################
# @file         test_nn_scaling.py
# @brief        Test calls for Near Neighbour Scaling through Control Library and verifies return status of the API.
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
from Tests.Control_API.control_api_base import testBase


##
# @brief - Verify Get/Set Scaling API Control Library Test
class testNNScalingAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Get/Set Scaling via Control Library")

        if self.cmd_line_param['HW_MODESET'] is not None:
            if self.cmd_line_param['HW_MODESET'][0] == 'TRUE':
                self.hw_modeset = True
            elif self.cmd_line_param['HW_MODESET'][0] == 'FALSE':
                self.hw_modeset = False
        else:
            logging.error("Incorrect Command line: Test requires HW ModeSet True/False input")
            self.fail()

        getscalingargs = control_api_args.ctl_scaling_settings_t()
        getscalingargs.Size = ctypes.sizeof(getscalingargs)

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Get Scaling via Control Library")
            if control_api_wrapper.get_scaling(getscalingargs, targetid):
                logging.info("Pass:  Get Scaling via Control Library")
                logging.info("Get Scaling Enable - {}, Type - {}".format(getscalingargs.Enable,
                                                                         getscalingargs.ScalingType))
            else:
                logging.error("Fail: Get Scaling via Control Library")
                gdhm.report_driver_bug_clib("Get scaling Failed via Control Library for "
                                            "Scaling: {0} Modeset: {1} TargetId: {2}"
                                            .format(getscalingargs.ScalingType, getscalingargs.HardwareModeSet,
                                                    targetid))
                self.fail("Get Scaling Failed via Control Library")

        setscalingargs = control_api_args.ctl_scaling_settings_t()
        setscalingargs.Size = ctypes.sizeof(setscalingargs)
        setscalingargs.ScalingType = control_api_args.ctl_scaling_type_flags_v.IDENTITY.value
        setscalingargs.Enable = True
        setscalingargs.HardwareModeSet = self.hw_modeset

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_2: Set Scaling 8x8 via Control Library")
            if control_api_wrapper.set_scaling(setscalingargs, targetid):
                logging.info("Pass:  Set Scaling via Control Library")
                logging.info("Set Scaling Enable - {}, Type - {}".format(setscalingargs.Enable,
                                                                         setscalingargs.ScalingType))
            else:
                logging.error("Fail: Set Scaling via Control Library")
                gdhm.report_driver_bug_clib("Set scaling Failed via Control Library for "
                                            "CustomScaling: {0}x{1} ScalingType: {2} TargetId: {3}"
                                            .format(setscalingargs.CustomScalingX, setscalingargs.CustomScalingY,
                                                    setscalingargs.ScalingType, targetid))
                self.fail("Set Scaling Failed via Control Library")

        setscaleargs = control_api_args.ctl_scaling_settings_t()
        setscaleargs.Size = ctypes.sizeof(setscaleargs)
        setscaleargs.ScalingType = control_api_args.ctl_scaling_type_flags_v.IDENTITY.value
        setscaleargs.Enable = True
        setscaleargs.HardwareModeSet = self.hw_modeset

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_3: Set Scaling 10x8 via Control Library")
            if control_api_wrapper.set_scaling(setscaleargs, targetid):
                logging.info("Pass:  Set Scaling via Control Library")
                logging.info("Set Scaling Enable - {}, Type - {}".format(setscalingargs.Enable,
                                                                         setscalingargs.ScalingType))
            else:
                logging.error("Fail: Set Scaling via Control Library")
                gdhm.report_driver_bug_clib("Set scaling Failed via control library for "
                                            "CustomScaling: {0}x{1} ScalingType: {2} TargetId: {3}"
                                            .format(setscaleargs.CustomScalingX, setscaleargs.CustomScalingY,
                                                    setscaleargs.ScalingType, targetid))
                self.fail("Set Scaling Failed via Control Library")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control Library Get-Set Scaling Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
