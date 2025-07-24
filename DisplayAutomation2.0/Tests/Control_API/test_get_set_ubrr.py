########################################################################################################################
# @file         test_get_set_ubrr.py
# @brief        Test calls for Get, Set UBRR and Get Power Caps through Control Library.
#                   * Get UBRR API.
#                   * Set UBRR API.
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
# @brief - Verify Get-Set UBRR API Control Library Test
class testPsrAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Get-Set UBRR via Control Library")

        gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        gfx_adapter_index = 'gfx_0'
        adapter_info = gfx_adapter_dict[gfx_adapter_index]
        targetid = display_config.DisplayConfiguration().get_target_id(self.connected_list[0], self.enumerated_displays)

        getPowerCaps = control_api_args.ctl_power_optimization_caps_t()
        getPowerCaps.Size = ctypes.sizeof(getPowerCaps)

        logging.info("Step_1: Get Power Caps to get current feature status")
        if control_api_wrapper.get_power_caps(getPowerCaps, targetid):
            logging.info("Pass: Supported Features - {} via Control Library".format(getPowerCaps.SupportedFeatures))
            LRR_Support = getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.LRR.value
            PSR_Support = getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.PSR.value
            FBC_Support = getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.FBC.value
            DPST_Support = getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.DPST.value
            logging.info("PowerCaps: Supported Features LRR - {}, PSR - {}, FBC - {} DPST - {} via Control Library"
                         .format(LRR_Support, PSR_Support, FBC_Support, DPST_Support))

        else:
            logging.error("Fail: Get Power Caps via Control Library")
            gdhm.report_driver_bug_clib("Get Power Caps Failed via Control Library for "
                                        "LRR: {0} PSR: {1} FBC: {2} DPST: {3}"
                                        .format(getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.LRR.value,
                                                getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.PSR.value,
                                                getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.FBC.value,
                                                getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.DPST.value))
            self.fail("Get Power Caps via Control Library")

        if getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.LRR.value:
            getLrr = control_api_args.ctl_power_optimization_settings_t()
            getLrr.Size = ctypes.sizeof(getLrr)
            getLrr.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.LRR.value

            logging.info("Step_2: Get UBRR Status")
            if control_api_wrapper.get_ubrr(getLrr, targetid):
                logging.info("Pass: UBRR status - {} via Control Library".format(getLrr.Enable))
                logging.info("SupportedLRRTypes - {} ".format(getLrr.FeatureSpecificData.LRRInfo.SupportedLRRTypes))
                logging.info("CurrentLRRTypes - {} ".format(getLrr.FeatureSpecificData.LRRInfo.CurrentLRRTypes))
                logging.info("bRequirePSRDisable - {} ".format(getLrr.FeatureSpecificData.LRRInfo.bRequirePSRDisable))
                logging.info("LowRR - {} ".format(getLrr.FeatureSpecificData.LRRInfo.LowRR))
            else:
                logging.error("Fail: Get LRR via Control Library")
                gdhm.report_driver_bug_clib("Get LRR Failed via Contrl Library - "
                                            "SupportedLRRTypes: {0} CurrentLRRTypes: {1}"
                                            .format(getLrr.FeatureSpecificData.LRRInfo.SupportedLRRTypes,
                                                    getLrr.FeatureSpecificData.LRRInfo.CurrentLRRTypes))
                self.fail("Get LRR Failed via Control Library")

            if not getLrr.Enable:
                setUbrr = control_api_args.ctl_power_optimization_settings_t()
                setUbrr.Size = ctypes.sizeof(setUbrr)
                setUbrr.Enable = True
                setUbrr.FeatureSpecificData.LRRInfo.CurrentLRRTypes = \
                    control_api_args.ctl_power_optimization_lrr_flags_v.UBLRR.value

                logging.info("Step_3: Set UBRR Feature")
                if control_api_wrapper.set_ubrr(setUbrr, targetid):
                    logging.info("Pass: Set UBRR via Control Library")
                else:
                    logging.error("Fail: Set UBRR via Control Library")
                    gdhm.report_driver_bug_clib("Set UBRR Failed via Control Library - "
                                                "UBBR status: {0} FeatureSpecificData: {1}"
                                                .format(setUbrr.Enable, 
                                                setUbrr.FeatureSpecificData.LRRInfo.CurrentLRRTypes))
                    self.fail("Set UBRR Failed via Control Library")
            else:
                logging.info("UBRR is already enabled in System UBRR - {}".format(getLrr.Enable))

            getUbrrData = control_api_args.ctl_power_optimization_settings_t()
            getUbrrData.Size = ctypes.sizeof(getUbrrData)
            getUbrrData.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.LRR.value

            logging.info("Step_4: Get UBRR Status Post Set Call")
            if control_api_wrapper.get_ubrr(getUbrrData, targetid):
                if getUbrrData.Enable:
                    logging.info("Pass: UBRR status - {} via Control Library".format(getLrr.Enable))
                    logging.info("SupportedLRRTypes - {} ".format(getLrr.FeatureSpecificData.LRRInfo.SupportedLRRTypes))
                    logging.info("CurrentLRRTypes - {} ".format(getLrr.FeatureSpecificData.LRRInfo.CurrentLRRTypes))
                    logging.info(
                        "bRequirePSRDisable - {} ".format(getLrr.FeatureSpecificData.LRRInfo.bRequirePSRDisable))
                    logging.info("LowRR - {} ".format(getLrr.FeatureSpecificData.LRRInfo.LowRR))
                else:
                    logging.error("UBRR is not enabled in Set UBRR Call")
                    gdhm.report_driver_bug_clib("UBRR is not enabled in Set UBRR Call - "
                                                "Enable: {0} PowerOptimizationFeature: {1}"
                                                .format(getUbrrData.Enable, getUbrrData.PowerOptimizationFeature))
                    self.fail("UBRR is not enabled post Set UBRR Call")
            else:
                logging.error("Fail: Get UBRR via Control Library")
                gdhm.report_driver_bug_clib("Get UBRR Failed via Control Library - "
                                            "Enable: {0}".format(getUbrrData.Enable))
                self.fail("Get UBRR Failed via Control Library")
        else:
            logging.warning("UBRR Feature is not supported due to feature disabled in Registry "
                            "/ Non-UBRR Panel is connected to System")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Get/Set UBRR Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
