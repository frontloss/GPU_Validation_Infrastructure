########################################################################################################################
# @file         test_get_set_dpst.py
# @brief        Test calls for Get, Set DPST and Get Power Caps through Control Library.
#                   * Get DPST API.
#                   * Set DPST API.
#                   * Get Power Caps API.
# @author       Prateek Joshi
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core import enum, registry_access, display_essential
from Libs.Core.logger import gdhm
from Libs.Core import display_power
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Tests.Control_API.control_api_base import testBase

# Current Platform name
PLATFORM_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName
PRE_MTL = machine_info.PRE_GEN_14_PLATFORMS + ['DG3']
POST_MTL = ['MTL', 'ELG'] + machine_info.GEN_15_PLATFORMS + machine_info.GEN_16_PLATFORMS


##
# @brief - Verify Get-Set DPST API Control Library Test
class testDpstAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Get-Set DPST via Control Library")

        if self.cmd_line_param['POWER_PLAN'] is not None:
            if self.cmd_line_param['POWER_PLAN'][0] == 'BALANCED':
                self.power_plan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
            elif self.cmd_line_param['POWER_PLAN'][0] == 'HIGH_PERFORMANCE':
                self.power_plan = control_api_args.ctl_power_optimization_plan_v.HIGH_PERFORMANCE.value
            elif self.cmd_line_param['POWER_PLAN'][0] == 'POWER_SAVER':
                self.power_plan = control_api_args.ctl_power_optimization_plan_v.POWER_SAVER.value
        else:
            logging.error("Incorrect Command line: Test requires power plan input")
            self.fail()

        # Enabling Simulated Battery
        logging.info("Enabling Simulated Battery")
        assert self.display_power.enable_disable_simulated_battery(True), "Failed to enable Simulated Battery"
        logging.info("PASS: Enabled Simulated Battery successfully")

        # Checking current power line status and if it is not DC, then changing it to DC
        power_line_status = self.display_power.get_current_powerline_status()
        if power_line_status != display_power.PowerSource.DC:
            result = self.display_power.set_current_powerline_status(display_power.PowerSource.DC)
            self.assertEquals(result, True, "Aborting the test as switching to DC mode failed")

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            dpst_flag = control_api_args.ctl_power_optimization_flags_v.DPST.value
            getPowerCaps = control_api_args.ctl_power_optimization_caps_t()
            getPowerCaps.Size = ctypes.sizeof(getPowerCaps)

            logging.info("Step_1: Get Power Caps to get current feature Status")
            if control_api_wrapper.get_power_caps(getPowerCaps, targetid):
                logging.info("Pass: DPST status - {} via Control Library"
                             .format(getPowerCaps.SupportedFeatures and dpst_flag))
            else:
                logging.error("Fail: Get DPST via Control Library")
                gdhm.report_driver_bug_clib("Get DPST Failed via Control Library for "
                                            "DPST flag: {0} SupportedFeature: {1} TargetId: {2}"
                                            .format(dpst_flag, getPowerCaps.SupportedFeatures, targetid))
                self.fail("Get DPST Failed via Control Library")

            if getPowerCaps.SupportedFeatures and dpst_flag:
                getDpst = control_api_args.ctl_power_optimization_settings_t()
                getDpst.Size = ctypes.sizeof(getDpst)
                getDpst.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.DPST.value
                getDpst.PowerOptimizationPlan = self.power_plan
                getDpst.PowerSource = control_api_args.ctl_power_source_v.DC.value
                getDpst.FeatureSpecificData.DPSTInfo.EnabledFeatures = \
                    control_api_args.ctl_power_optimization_dpst_flags_v.BKLT.value

                logging.info("Step_2: Get DPST Status")
                if control_api_wrapper.get_dpst(getDpst, targetid):
                    logging.info("Pass: DPST status - {} via Control Library".format(getDpst.Enable))
                    logging.info("Power Source - {} ".format(getDpst.PowerSource))
                    logging.info("Power Optimization Plan - {}".format(getDpst.PowerOptimizationPlan))
                    logging.info("MinLevel - {} ".format(getDpst.FeatureSpecificData.DPSTInfo.MinLevel))
                    logging.info("MaxLevel - {} ".format(getDpst.FeatureSpecificData.DPSTInfo.MaxLevel))
                    logging.info("Level - {} ".format(getDpst.FeatureSpecificData.DPSTInfo.Level))
                    logging.info("SupportedFeatures - {} ".format(
                        getDpst.FeatureSpecificData.DPSTInfo.SupportedFeatures.value))
                    logging.info("EnabledFeatures - {} ".format(getDpst.FeatureSpecificData.DPSTInfo.EnabledFeatures.value))
                else:
                    logging.error("Fail: Get DPST via Control Library")
                    gdhm.report_driver_bug_clib("Get DPST Failed via Control Library for "
                                                "DPST support: {0} DPST enabled feature: {1} TargetId: {2}"
                                                .format(getDpst.FeatureSpecificData.DPSTInfo.SupportedFeatures.value,
                                                getDpst.FeatureSpecificData.DPSTInfo.EnabledFeatures.value,targetid))
                    self.fail("Get DPST Failed via Control Library")

                setDpst = control_api_args.ctl_power_optimization_settings_t()
                setDpst.Size = ctypes.sizeof(setDpst)
                setDpst.Enable = True
                setDpst.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
                setDpst.PowerSource = control_api_args.ctl_power_source_v.DC.value
                setDpst.FeatureSpecificData.DPSTInfo.Level = 3
                setDpst.FeatureSpecificData.DPSTInfo.EnabledFeatures = \
                    control_api_args.ctl_power_optimization_dpst_flags_v.BKLT.value

                logging.info("Step_3: Set DPST Feature")
                if control_api_wrapper.set_dpst(setDpst, targetid):
                    if setDpst.Enable:
                        logging.info("Pass: Set DPST via Control Library")
                    else:
                        logging.error("Fail: DPST is not enabled in Set Call")
                        gdhm.report_driver_bug_clib("Set DPST Failed via Control Library for "
                                                "DPST Enable: {0} TargetId: {1}"
                                                .format(setDpst.Enable,targetid))
                        self.fail()
                else:
                    logging.error("Fail: Set DPST Call via Control Library")
                    gdhm.report_driver_bug_clib("Set DPST Failed via control library for "
                                                "DPST Enabled Feature: {0} TargetId: {1}"
                                                .format(setDpst.FeatureSpecificData.DPSTInfo.EnabledFeatures,targetid))
                    self.fail("Set DPST Call Failed via Control Library")

                getDpstData = control_api_args.ctl_power_optimization_settings_t()
                getDpstData.Size = ctypes.sizeof(getDpstData)
                getDpstData.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
                getDpstData.PowerSource = control_api_args.ctl_power_source_v.DC.value
                getDpstData.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.DPST.value
                getDpstData.FeatureSpecificData.DPSTInfo.EnabledFeatures = \
                    control_api_args.ctl_power_optimization_dpst_flags_v.BKLT.value

                logging.info("Step_4: Get DPST Status Post Set Call")
                if control_api_wrapper.get_dpst(getDpstData, targetid):
                    if getDpstData.Enable and getDpstData.FeatureSpecificData.DPSTInfo.Level == 3:
                        logging.info("Pass: DPST status - {} via Control Library".format(getDpstData.Enable))
                        logging.info("Power Source - {} ".format(getDpstData.PowerSource))
                        logging.info("Power Optimization Plan - {}".format(getDpstData.PowerOptimizationPlan))
                        logging.info("MinLevel - {} ".format(getDpstData.FeatureSpecificData.DPSTInfo.MinLevel))
                        logging.info("MaxLevel - {} ".format(getDpstData.FeatureSpecificData.DPSTInfo.MaxLevel))
                        logging.info("Level - {} ".format(getDpstData.FeatureSpecificData.DPSTInfo.Level))
                        logging.info("SupportedFeatures - {} ".format(
                            getDpstData.FeatureSpecificData.DPSTInfo.SupportedFeatures.value))
                        logging.info("EnabledFeatures - {} ".format(
                            getDpstData.FeatureSpecificData.DPSTInfo.EnabledFeatures.value))
                    else:
                        logging.error("DPST is not enabled in Get DPST Call")
                        gdhm.report_driver_bug_clib("Get DPST Failed Post Set Call via Control Library for "
                                                    "DPST Enable: {0} DPST Level: {1} TargetId: {2}"
                                                    .format(getDpstData.Enable,getDpstData.FeatureSpecificData.DPSTInfo.Level,
                                                    targetid))
                        self.fail("DPST is not enabled post Set DPST Call")
                else:
                    logging.error("Fail: Get DPST via Control Library")
                    gdhm.report_driver_bug_clib("Get DPST Failed via control library for "
                                                "DPST Enabled Feature: {0} TargetId: {1}"
                                                .format(getDpstData.FeatureSpecificData.DPSTInfo.EnabledFeatures,targetid))
                    self.fail("Get DPST Failed via Control Library")

                # Restart driver
                logging.info("Test: Disable/Enable driver")
                status, reboot_required = display_essential.restart_gfx_driver()
                self.assertEqual(status, True,
                                 "Aborting the test as driver restart failed")
                logging.info("PASS: Driver restart successfull")
                if getDpstData.Enable:
                    setDpst = control_api_args.ctl_power_optimization_settings_t()
                    setDpst.Size = ctypes.sizeof(setDpst)
                    setDpst.Enable = False
                    setDpst.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
                    setDpst.PowerSource = control_api_args.ctl_power_source_v.DC
                    setDpst.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.DPST.value
                    setDpst.FeatureSpecificData.DPSTInfo.EnabledFeatures = \
                        control_api_args.ctl_power_optimization_dpst_flags_v.BKLT.value

                    logging.info("Step_5: Disable DPST Feature")
                    if control_api_wrapper.set_dpst(setDpst, targetid):
                        logging.info("Pass: Set DPST False via Control Library")
                    else:
                        logging.error("Fail: Set DPST False via Control Library")
                        gdhm.report_driver_bug_clib("Set DPST call Passed Post Disabling via Control Library for "
                                                    "Enable: {0} Enabled Features: {1} TargetId: {2}"
                                                    .format(setDpst.Enable, setDpst.FeatureSpecificData.DPSTInfo.EnabledFeatures,
                                                    targetid))
                        self.fail("Disable DPST Failed via Control Library")
                else:
                    logging.info("DPST is already disabled in System - {}".format(getDpstData.Enable))

                logging.info("Step_6: Get DPST Status Post Disable Call")
                getDpstData = control_api_args.ctl_power_optimization_settings_t()
                getDpstData.Size = ctypes.sizeof(getDpstData)
                getDpstData.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
                getDpstData.PowerSource = control_api_args.ctl_power_source_v.DC.value
                getDpstData.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.DPST.value
                getDpstData.FeatureSpecificData.DPSTInfo.EnabledFeatures = \
                    control_api_args.ctl_power_optimization_dpst_flags_v.BKLT.value
                if control_api_wrapper.get_dpst(getDpstData, targetid):
                    logging.info("Pass: DPST feature - {} is Disabled via Control Library".format(getDpstData.Enable))
                    logging.info("Pass: DPST feature - {} is Disabled via Control Library".format(getDpstData.Enable))
                    logging.info("Power Source - {} ".format(getDpstData.PowerSource))
                    logging.info("Power Optimization Plan - {}".format(getDpstData.PowerOptimizationPlan))
                    logging.info("MinLevel - {} ".format(getDpstData.FeatureSpecificData.DPSTInfo.MinLevel))
                    logging.info("MaxLevel - {} ".format(getDpstData.FeatureSpecificData.DPSTInfo.MaxLevel))
                    logging.info("Level - {} ".format(getDpstData.FeatureSpecificData.DPSTInfo.Level))
                    logging.info("SupportedFeatures - {} ".format(
                        getDpstData.FeatureSpecificData.DPSTInfo.SupportedFeatures.value))
                    logging.info("EnabledFeatures - {} ".format(
                        getDpstData.FeatureSpecificData.DPSTInfo.EnabledFeatures.value))
                    if not getDpstData.Enable:
                        logging.info("Pass: DPST feature - {} is Disabled via Control Library".format(getDpstData.Enable))
                    else:
                        logging.error("DPST is not disabled in Set DPST Call")
                        gdhm.report_driver_bug_clib("DPST is not disabled post Set Call via Control Library for "
                                                    "Enable: {0} TargetId: {1}".format(getDpstData.Enable, targetid))
                        self.fail("DPST is not disabled post Set DPST Call")
                else:
                    logging.error("Fail: Get DPST Call via Control Library Post Disable DPST")
                    gdhm.report_driver_bug_clib("Get DPST Failed Post Disable DPST via control library for "
                                                "Enabled Feature: {0} TargetId: {1}".format(getDpstData.FeatureSpecificData.DPSTInfo.EnabledFeatures, targetid))
                    self.fail("Get DPST Failed via Control Library Post Disable DPST")

                logging.info("Step_7: Negative verification to test DPST feature")

                setDpst = control_api_args.ctl_power_optimization_settings_t()
                setDpst.Size = ctypes.sizeof(setDpst)
                setDpst.Enable = True
                setDpst.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
                setDpst.PowerSource = control_api_args.ctl_power_source_v.DC.value
                setDpst.FeatureSpecificData.DPSTInfo.Level = 8
                setDpst.FeatureSpecificData.DPSTInfo.EnabledFeatures = \
                    control_api_args.ctl_power_optimization_dpst_flags_v.BKLT.value

                if control_api_wrapper.set_dpst(setDpst, targetid):
                    if setDpst.Enable:
                        logging.info("Pass: Set DPST via Control Library")
                        getDpstData = control_api_args.ctl_power_optimization_settings_t()
                        getDpstData.Size = ctypes.sizeof(getDpstData)
                        getDpstData.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.POWER_SAVER.value
                        getDpstData.PowerSource = control_api_args.ctl_power_source_v.DC.value
                        getDpstData.PowerOptimizationFeature = control_api_args.ctl_power_optimization_flags_v.DPST.value
                        getDpstData.FeatureSpecificData.DPSTInfo.EnabledFeatures = \
                            control_api_args.ctl_power_optimization_dpst_flags_v.BKLT.value
                        if control_api_wrapper.get_dpst(getDpstData, targetid):
                            if getDpstData.FeatureSpecificData.DPSTInfo.Level == 6 and PLATFORM_NAME in PRE_MTL:
                                logging.info(
                                    f"Pass: Negative Test to set DPST via Control Library for {PLATFORM_NAME}, "
                                    f"DPST_level: {getDpstData.FeatureSpecificData.DPSTInfo.Level}, Target_Id: "
                                    f"{targetid}")
                            elif getDpstData.FeatureSpecificData.DPSTInfo.Level == 3 and PLATFORM_NAME in POST_MTL:
                                logging.info(
                                    f"Pass: Negative Test to set DPST via Control Library for {PLATFORM_NAME}, "
                                    f"DPST_level: {getDpstData.FeatureSpecificData.DPSTInfo.Level}, Target_Id: "
                                    f"{targetid}")
                            else:
                                logging.error("Fail: Negative verification to set DPST via Control Library")
                                gdhm.report_driver_bug_clib("DPST negative verification failed - Expected: {0} "
                                                            "Actual: {1} for Platform: {2}".format
                                                            (6 if PLATFORM_NAME in PRE_MTL else 3,
                                                             getDpstData.FeatureSpecificData.DPSTInfo.Level,
                                                             PLATFORM_NAME))
            else:
                logging.error("DPST Feature is not supported due to feature disabled in Registry "
                              "/ Non-DPST Panel is connected to System")
                gdhm.report_driver_bug_clib("DPST Feature is not supported due to feature disabled in Registry/ "
                                            "Non-DPST Panel is connected to System - "
                                            "Supported Feature: {0} DPST_Flag: {1}"
                                            .format(getPowerCaps.SupportedFeatures, dpst_flag))
                self.fail()

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info(" TEARDOWN: testDpstAPI ")

        # Disable Simulated Battery
        if self.display_power.enable_disable_simulated_battery(False):
            logging.info("Successfully disabled simulated battery")
        else:
            logging.warning("Failed to disable Simulated Battery")

        super(testDpstAPI, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Get/Set DPST Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)