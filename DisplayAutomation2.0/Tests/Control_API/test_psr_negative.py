########################################################################################################################
# @file         test_psr_negative.py
# @brief        Test calls for Get PSR and Get Power Caps through Control Library.
#                   * Get PSR API.
#                   * Get Power Caps API.
# @author       Prateek Joshi
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core.logger import gdhm
from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Control_API.control_api_base import testBase
from Tests.PowerCons.Functional.PSR import psr

##
# @brief - Verify Get-Set PSR API Control Library Test
class testPsrAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: PSR Negative via Control Library")

        if self.cmd_line_param['PSR_VERSION'] is not None:
            if self.cmd_line_param['PSR_VERSION'][0] == 'PSR_1':
                self.feature = psr.UserRequestedFeature.PSR_1
            elif self.cmd_line_param['PSR_VERSION'][0] == 'PSR_2':
                self.feature = psr.UserRequestedFeature.PSR_2
        else:
            logging.error("Incorrect Command line: Test requires PSR version input to verify PSR Negative testing")
            self.fail()

        gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        gfx_adapter_index = 'gfx_0'
        adapter_info = gfx_adapter_dict[gfx_adapter_index]
        targetid = display_config.DisplayConfiguration().get_target_id(self.connected_list[0], self.enumerated_displays)

        getPowerCaps = control_api_args.ctl_power_optimization_caps_t()
        getPowerCaps.Size = ctypes.sizeof(getPowerCaps)

        logging.info("Step_1: Get Power Caps to get current feature Status")
        if control_api_wrapper.get_power_caps(getPowerCaps, targetid):
            logging.info("Pass: PSR status - {} via Control Library".format(getPowerCaps.SupportedFeatures))
        else:
            logging.error("Fail: Get PSR Call via Control Library")
            gdhm.report_driver_bug_clib("Get PSR Call Failed via Control Library - "
                                        "SuportedFeature: {0} TargetId: {1}"
                                        .format(getPowerCaps.SupportedFeatures, targetid))
            self.fail("Get PSR Call Failed via Control Library")

        if getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.PSR.value:
            getPsr = control_api_args.ctl_power_optimization_settings_t()
            getPsr.Size = ctypes.sizeof(getPsr)
            getPsr.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.PSR.value

            psr_status = psr.disable(gfx_adapter_index, self.feature)
            if psr_status is False:
                logging.error("FAILED to disable PSR through registry key")
                gdhm.report_driver_bug_clib("Disable PSR Failed through registry key for "
                                            "Adapter: {0} Feature: {1}".format(gfx_adapter_index,self.feature))
                self.fail()
            if psr_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("FAILED to restart the driver")
            logging.info(f"{self.feature.name} is disabled from Display FeatureTestControl Registry")

            logging.info("Step_2: Get PSR Status in Feature Disabled Case")
            if control_api_wrapper.get_psr(getPsr, targetid):
                if not getPsr.Enable:
                    logging.info("PSR is disabled and verified through Control Library Escape Call")
                else:
                    logging.error("PSR is still enabled post disabling through Registry")
                    gdhm.report_driver_bug_clib("PSR still enabled post disabling through Registry for "
                                                "TargetId: {0}".format(targetid))
                    self.fail()
            else:
                logging.error("Fail: Get PSR Call via Control Library")
                gdhm.report_driver_bug_clib("Get PSR call Failed via Control Library for "
                                            "TargetId: {0}".format(targetid))
                self.fail()

            psr_status = psr.enable(gfx_adapter_index, self.feature)
            if psr_status is False:
                logging.error("FAILED to enable PSR through registry key")
                self.fail()
            if psr_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("FAILED to restart the driver")
            logging.info(f"{self.feature.name} is enabled from Display FeatureTestControl registry")

            logging.info("Step_3: Get PSR Status in Feature Enabled Case")
            if control_api_wrapper.get_psr(getPsr, targetid):
                logging.info("PSR status - {} via Control Library".format(getPsr.Enable))
                if getPsr.Enable:
                    logging.info("PSR is enabled and verified through Control Library Escape Call")
                else:
                    logging.error("PSR is still disabled post enabling through Registry")
                    gdhm.report_driver_bug_clib("PSR is still disabled post enabling through Registry for "
                                                "TargetId: {0}".format(targetid))
                    self.fail()
            else:
                logging.error("Fail: Get PSR Call via Control Library")
                gdhm.report_driver_bug_clib("Get PSR call Failed via Control Library for "
                                            "TargetId: {0}".format(targetid))
                self.fail()
        else:
            logging.warning("PSR Feature is not supported due to feature disabled in Registry "
                            "/ Non-PSR Panel is connected to System")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library PSR Negative Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)