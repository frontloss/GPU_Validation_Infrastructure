########################################################################################################################
# @file         test_get_set_psr.py
# @brief        Test calls for Get, Set PSR and Get Power Caps through Control Library.
#                   * Get PSR API.
#                   * Set PSR API.
#                   * Get Power Caps API.
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
# @brief - Verify Get-Set PSR API Control Library Test
class testPsrAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Get-Set PSR via Control Library")

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
            logging.error("Fail: Get PSR via Control Library")
            gdhm.report_driver_bug_clib("Get PSR Failed via Control Library - "
                                        "PSR status: {0}".format(getPowerCaps.SupportedFeatures))
            self.fail("Get PSR Failed via Control Library")

        if getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.PSR.value:
            getPsr = control_api_args.ctl_power_optimization_settings_t()
            getPsr.Size = ctypes.sizeof(getPsr)
            getPsr.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.PSR.value

            logging.info("Step_2: Get PSR Status")
            if control_api_wrapper.get_psr(getPsr, targetid):
                logging.info("Pass: PSR status - {} via Control Library".format(getPsr.Enable))
                # TODO Note: PSR Version and FullFetchUpdate fields are not populated from Control Library DLL
                logging.info("PSR Version - {} ".format(getPsr.FeatureSpecificData.PSRInfo.PSRVersion))
                logging.info("FullFetchUpdate - {} ".format(getPsr.FeatureSpecificData.PSRInfo.FullFetchUpdate))
            else:
                logging.error("Fail: Get PSR via Control Library")
                gdhm.report_driver_bug_clib("Get PSR Failed via Control Library - "
                                            "PSR status: {0} FeatureSpecificData: {1}"
                                            .format(getPsr.Enable, getPsr.FeatureSpecificData))
                self.fail("Get PSR Failed via Control Library")

            if not getPsr.Enable:
                setPsr = control_api_args.ctl_power_optimization_settings_t()
                setPsr.Size = ctypes.sizeof(setPsr)
                setPsr.Enable = True

                logging.info("Step_3: Set PSR Feature")
                if control_api_wrapper.set_psr(setPsr, targetid):
                    logging.info("Pass: Set PSR via Control Library")
                else:
                    logging.error("Fail: Set PSR via Control Library")
                    gdhm.report_driver_bug_clib("Set PSR Failed via Control Library - "
                                                "PSR status: {0} FeatureSpecificData: {1}"
                                                .format(setPsr.Enable, setPsr.FeatureSpecificData))
                    self.fail("Set PSR Failed via Control Library")
            else:
                logging.info("PSR is already enabled in System PSR - {}".format(getPsr.Enable))

            getPsrData = control_api_args.ctl_power_optimization_settings_t()
            getPsrData.Size = ctypes.sizeof(getPsrData)
            getPsrData.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.PSR.value

            logging.info("Step_4: Get PSR Status Post Set Call")
            if control_api_wrapper.get_psr(getPsrData, targetid):
                if getPsrData.Enable:
                    logging.info("Pass: PSR status - {} via Control Library".format(getPsrData.Enable))
                    logging.info("PSR Version - {} ".format(getPsrData.FeatureSpecificData.PSRInfo.PSRVersion))
                    logging.info("FullFetchUpdate - {} ".format(getPsrData.FeatureSpecificData.PSRInfo.FullFetchUpdate))
                else:
                    logging.error("PSR is not enabled in Set PSR Call")
                    gdhm.report_driver_bug_clib("PSR not enabled post Set PSR call - "
                                                "PSR status: {0}".format(getPsrData.Enable))
                    self.fail("PSR is not enabled post Set PSR Call")
            else:
                logging.error("Fail: Get PSR via Control Library")
                gdhm.report_driver_bug_clib("Get PSR Failed via Control Library - "
                                            "PSR status: {0}".format(getPsrData.Enable))
                self.fail("Get PSR Failed via Control Library")

            if getPsrData.Enable:
                setPsr = control_api_args.ctl_power_optimization_settings_t()
                setPsr.Size = ctypes.sizeof(setPsr)
                setPsr.Enable = False

                logging.info("Step_5: Disable PSR Feature")
                if control_api_wrapper.set_psr(setPsr, targetid):
                    logging.info("Pass: Set PSR False via Control Library")
                else:
                    logging.error("Fail: Set PSR False via Control Library")
                    gdhm.report_driver_bug_clib("Set PSR Failed via Control Library - "
                                                "PSR status: {0}".format(setPsr.Enable))
                    self.fail("Disable PSR Failed via Control Library")
            else:
                logging.info("PSR is already disabled in System PSR - {}".format(getPsrData.Enable))

            logging.info("Step_6: Get PSR Status Post Disable Call")
            if control_api_wrapper.get_psr(getPsrData, targetid):
                if not getPsrData.Enable:
                    logging.info("Pass: PSR feature - {} is Disabled via Control Library".format(getPsrData.Enable))
                    logging.info("PSR Version - {} ".format(getPsrData.FeatureSpecificData.PSRInfo.PSRVersion))
                    logging.info("FullFetchUpdate - {} ".format(getPsrData.FeatureSpecificData.PSRInfo.FullFetchUpdate))
                else:
                    logging.error("PSR is not disabled in Set PSR Call")
                    gdhm.report_driver_bug_clib("PSR is not disabled via Set PSR call - "
                                                "PSR status: {0}".format(getPsrData.Enable))
                    self.fail("PSR is not disabled post Set PSR Call")
            else:
                logging.error("Fail: Get PSR Call via Control Library Post Disable PSR")
                gdhm.report_driver_bug_clib("Get PSR Call Failed via Control Library Post Disable call - PSR Params: "
                                            "Status: {0} FullFetchUpdate: {1}"
                                            .format(getPsrData.Enable, getPsrData.FeatureSpecificData.PSRInfo.FullFetchUpdate))
                self.fail("Get PSR Failed via Control Library Post Disable PSR")

            getPsrData = control_api_args.ctl_power_optimization_settings_t()
            getPsrData.Size = ctypes.sizeof(getPsrData)
            getPsrData.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.PSR.value

            logging.info("Step_7: Enable PSR at the end of verification")
            if not getPsrData.Enable:
                setPsr = control_api_args.ctl_power_optimization_settings_t()
                setPsr.Size = ctypes.sizeof(setPsr)
                setPsr.Enable = True

                logging.info("Step_8: Enable PSR Feature")
                if control_api_wrapper.set_psr(setPsr, targetid):
                    logging.info("Pass: Enable PSR via Control Library")
                else:
                    logging.error("Fail: Enable PSR via Control Library")
                    gdhm.report_driver_bug_clib("PSR is not enabled via Control Library - "
                                                "PSR status: {0}".format(setPsr.Enable))
                    self.fail("Enable PSR Failed via Control Library")
            else:
                logging.info(f"PSR is already enabled in System PSR - {getPsrData.Enable}")
        else:
            logging.warning("PSR Feature is not supported due to feature disabled in Registry "
                            "/ Non-PSR Panel is connected to System")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Get/Set PSR Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)