########################################################################################################################
# @file         test_endurance_gaming.py
# @brief        Test calls for Endurance Gaming through Control Library and verifies return status of the API.
# @author       Anjali Shetty
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
# @brief - Test for endurance gaming
class TestEnduranceGamingAPI(testBase):

    ##
    # @brief            To get EG control values
    # @param[in]        eg_control; EG control string
    # @return           EG control value for passed command line parameter
    def get_eg_control_value(self, eg_control):
        return {
            'TURN_OFF': 0,
            'TURN_ON': 1,
            'AUTO': 2
        }[eg_control]

    ##
    # @brief            To get EG mode values
    # @param[in]        eg_mode; EG mode string
    # @return           EG control value for passed command line parameter
    def get_eg_mode_value(self, eg_mode):
        return {
            'BETTER_PERFORMANCE': 0,
            'BALANCED': 1,
            'MAXIMUM_BATTERY': 2
        }[eg_mode]

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Endurance Gaming with Control Library")

        if self.cmd_line_param['EG_CONTROL'] != 'NONE':
            eg_control = self.cmd_line_param['EG_CONTROL'][0]
            if eg_control == "AUTO" and self.cmd_line_param['EG_MODE'] == 'NONE':
                eg_mode = "BALANCED"
            elif self.cmd_line_param['EG_MODE'] != 'NONE':
                eg_mode = self.cmd_line_param['EG_MODE'][0]
            else:
                self.fail("Incorrect command line argument Endurance Gaming mode is not provided")
        else:
            self.fail("Incorrect Command line argument. Endurance Gaming control is not provided")

        argsSet3DFeature = control_api_args.ctl_3d_feature_getset_t()
        argsSet3DFeature.bSet = True

        setEnduranceGamingArgs = control_api_args.ctl_endurance_gaming_t()

        setEnduranceGamingArgs.EGControl = self.get_eg_control_value(eg_control)
        setEnduranceGamingArgs.EGMode = self.get_eg_mode_value(eg_mode)

        logging.info("EG Control {} EG Mode {}".format(setEnduranceGamingArgs.EGControl, setEnduranceGamingArgs.EGMode))

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Set Endurance Gaming via Control Library")
            if control_api_wrapper.get_set_endurance_gaming(argsSet3DFeature, setEnduranceGamingArgs, targetid):
                logging.info("Pass:  Set Endurance Gaming via Control Library")
            else:
                logging.error("Fail: Set Endurance Gaming via Control Library")
                gdhm.report_driver_bug_clib("Set Endurance Gaming Failed via Control Library for "
                                            "EGControl: {0} EGMode: {1} TargetId: {2}"
                                            .format(setEnduranceGamingArgs.EGControl,setEnduranceGamingArgs.EGMode,targetid))
                self.fail("Set Endurance Gaming Failed via Control Library")

        getEnduranceGamingArgs = control_api_args.ctl_endurance_gaming_t()

        argsGet3DFeature = control_api_args.ctl_3d_feature_getset_t()
        argsGet3DFeature.bSet = False

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_2: Get Endurance Gaming via Control Library")
            if control_api_wrapper.get_set_endurance_gaming(argsGet3DFeature, getEnduranceGamingArgs, targetid):
                logging.info("Pass:  Get Endurance Gaming via Control Library")
            else:
                logging.error("Fail: Get Endurance Gaming via Control Library")
                gdhm.report_driver_bug_clib("Get Endurance Gaming Failed via Control Library for "
                                            "targetid: {0}".format(targetid))
                self.fail("Get Endurance Gaming Failed via Control Library")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control Library Get-Set Endurance Gaming API')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)