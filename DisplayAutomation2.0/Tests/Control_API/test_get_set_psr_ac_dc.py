########################################################################################################################
# @file         test_get_set_psr_ac_dc.py
# @brief        Test calls for Get, Set PSR and Get Power Caps with AC, DC switch through Control Library.
#                   * Get PSR API.
#                   * Set PSR API.
# @author       Prateek Joshi
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core import display_power
from Libs.Core.test_env import test_context
from Tests.Control_API.control_api_base import testBase

##
# @brief - Verify Get-Set PSR API Control Library Test
class testPsrAPIAcDc(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Get-Set PSR witb AC, DC Switch via Control Library")

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
                                        "actual feature support: {0}".format(getPowerCaps.SupportedFeatures))
            self.fail("Get PSR Failed via Control Library")

        if getPowerCaps.SupportedFeatures and control_api_args.ctl_power_optimization_flags_v.PSR.value:
            getPsr = control_api_args.ctl_power_optimization_settings_t()
            getPsr.Size = ctypes.sizeof(getPsr)

            logging.info("Step_1: Get PSR Status")
            if control_api_wrapper.get_psr(getPsr, targetid):
                logging.info("Pass: PSR status - {} via Control Library".format(getPsr.Enable))
                logging.info("PSR Version - {} ".format(getPsr.FeatureSpecificData.PSRInfo.PSRVersion))
                logging.info("FullFetchUpdate - {} ".format(getPsr.FeatureSpecificData.PSRInfo.FullFetchUpdate))
            else:
                logging.error("Fail: Get PSR via Control Library")
                gdhm.report_driver_bug_clib("Get PSR Failed via Control Library - "
                                            "PSR Status: {0} FullFetchUpdate: {1}"
                                            .format(getPsr.Enable, getPsr.FeatureSpecificData.PSRInfo.FullFetchUpdate))
                self.fail("Get PSR Failed via Control Library")

            if not getPsr.Enable:
                setPsr = control_api_args.ctl_power_optimization_settings_t()
                setPsr.Size = ctypes.sizeof(setPsr)
                setPsr.Enable = True

                logging.info("Step_2: Set PSR Feature")
                if control_api_wrapper.set_psr(setPsr, targetid):
                    logging.info("Pass: Set PSR via Control Library")
                else:
                    logging.error("Fail: Set PSR via Control Library")
                    gdhm.report_driver_bug_clib("Set PSR Failed via Control Library - "
                                                "PSR status: {0} FeatureSpecificData: {1}"
                                                .format(setPsr.Enable, setPsr.FeatureSpecificData.PSRInfo.FullFetchUpdate))
                    self.fail("Set PSR Failed via Control Library")

            # Checking current power line status and if it is not DC, then changing it to DC
            if display_power.DisplayPower().enable_disable_simulated_battery(True):
                logging.info("Enabled Simulated Battery successfully")
                power_line_status = self.display_power.get_current_powerline_status()
                if power_line_status != display_power.PowerSource.DC:
                    logging.debug(f"Current powerline status is not in {power_line_status} setting it to DC")
                    result = self.display_power.set_current_powerline_status(display_power.PowerSource.DC)
                    self.assertEquals(result, True, "Aborting the test as switching to DC mode failed")
                logging.info("Switched power line to DC successfully")
                logging.info("Step_3: Get PSR Status in DC state")
                if control_api_wrapper.get_psr(getPsr, targetid):
                    logging.info("Pass: PSR status - {} via Control Library".format(getPsr.Enable))
                    logging.info("PSR Version - {} ".format(getPsr.FeatureSpecificData.PSRInfo.PSRVersion))
                    logging.info("FullFetchUpdate - {} ".format(getPsr.FeatureSpecificData.PSRInfo.FullFetchUpdate))
                else:
                    logging.error("Fail: Get PSR in DC mode via Control Library")
                    gdhm.report_driver_bug_clib("Get PSR in DC mode Failed via Control Library - "
                                                "Power Source: {0} PSR status: {1}"
                                                .format(getPsr.PowerSource, getPsr.Enable))
                    self.fail("Get PSR in DC mode Failed via Control Library")
            else:
                logging.error("Failed to enable simulated battery")

            # Checking current power line status and if it is not AC, then changing it to AC
            power_line_status = self.display_power.get_current_powerline_status()
            if power_line_status != display_power.PowerSource.AC:
                result = self.display_power.set_current_powerline_status(display_power.PowerSource.AC)
                self.assertEquals(result, True, "Aborting the test as switching to DC mode failed")

            logging.info("Step_4: Get PSR Status in AC state")
            if control_api_wrapper.get_psr(getPsr, targetid):
                logging.info("Pass: PSR status - {} via Control Library".format(getPsr.Enable))
                logging.info("PSR Version - {} ".format(getPsr.FeatureSpecificData.PSRInfo.PSRVersion))
                logging.info("FullFetchUpdate - {} ".format(getPsr.FeatureSpecificData.PSRInfo.FullFetchUpdate))
            else:
                logging.error("Fail: Get PSR in AC mode via Control Library")
                gdhm.report_driver_bug_clib("Get PSR in AC Mode Failed via Control Library for "
                                            "Power Source: {0} PSR status: {1}"
                                            .format(getPsr.PowerSource, getPsr.Enable))
                self.fail("Get PSR in AC mode Failed via Control Library")
        else:
            logging.warning("PSR Feature is not supported due to feature disabled in Registry "
                            "/ Non-PSR Panel is connected to System")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Get/Set PSR Verification with AC, DC switch')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)