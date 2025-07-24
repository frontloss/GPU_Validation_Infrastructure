#################################################################################################
# @file         lace_with_gfx_events.py
# @brief        Test calls for get and set lace functionality with gfx events persistence
# @author       Vimalesh D
#################################################################################################

import time
import sys
import unittest
from Libs.Core import display_power, enum
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common.common_utility import invoke_power_event, apply_power_mode
from Tests.Color.Features.Lace.lace_base import *
from Tests.Control_API.control_api_base import testBase

from Tests.Color.Common.common_utility import get_modelist_subset, apply_mode
from Tests.Color.Verification import gen_verify_pipe, feature_basic_verify


##
# @brief - To perform persistence verification for BPC and Encoding
class LacePersistenceGfxEvents(LACEBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief test_01_power events function - Function to perform
    #                                        power events S3,CS,S4 and perform register verification on all panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() not in ["POWER_EVENT_S3", "POWER_EVENT_S4", "POWER_EVENT_CS"],
                     "Skip the  test step as the action type is not power event S3/CS/S4")
    def test_01_power_events(self):

        power_state_dict = {
            "POWER_EVENT_S3": display_power.PowerEvent.S3, "POWER_EVENT_CS": display_power.PowerEvent.CS,
            "POWER_EVENT_S4": display_power.PowerEvent.S4}

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        logging.info("Step_1: get lace")
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: Lace was enabled and verified successfully for pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace enable with verification failed for pipe_{0}".format(panel.pipe))

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

        ##
        # Invoke power event
        if invoke_power_event(power_state_dict[self.scenario]) is False:
            self.fail(" Fail: Failed to invoke power event {0}".format(power_state_dict[self.scenario]))
        else:
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.is_lfp and self.check_primary_display(port):
                        if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                    "LEGACY") is False:
                            self.fail("Lace verification failed")

    ##
    # @brief test_02_restart display driver function - Function to perform restart display driver and perform register
    #                                                  verification on all supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "RESTART_DRIVER",
                     "Skip the  test step as the action type is not Restart driver")
    def test_02_restart_display_driver(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        logging.info("Step_1: get lace")
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: Lace was enabled and verified successfully for pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace enable with verification failed for pipe_{0}".format(panel.pipe))

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

            time.sleep(5)
            ##
            # restart display driver
            status, reboot_required = common_utility.restart_display_driver(adapter.gfx_index)
            if status is False:
                self.fail('Fail: Failed to Restart Display driver')
            else:
                for gfx_index, adapter in self.context_args.adapters.items():
                    for port, panel in adapter.panels.items():
                        if panel.is_active and panel.is_lfp and self.check_primary_display(port):
                            if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                        "LEGACY") is False:
                                self.fail("Lace verification failed")

    ##
    # @brief test_03_monitor_turnoffon function - Function to perform monitor turnoff_on and perform register
    #                                             verification on all supported panels
    #                                                  .
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "MONITOR_TURNOFFON",
                     "Skip the  test step as the action type is not Monitor Turnoff_on")
    def test_03_monitor_turnoffon(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        logging.info("Step_1: get lace")
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: Lace was enabled and verified successfully for pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace enable with verification failed for pipe_{0}".format(panel.pipe))

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

        ##
        # monitor turn off-on
        if common_utility.invoke_monitor_turnoffon() is False:
            self.fail("Failed to Turned Off-On Monitor event")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and self.check_primary_display(port):
                    if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                "LEGACY") is False:
                        self.fail("Lace verification failed")

    ##
    # @brief test_04_ac_dc_switch function - Function to perform ac to dc switch and perform register
    #                                        verification on all supported panels
    #                                                  .
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "AC_DC",
                     "Skip the  test step as the action type is not Monitor Turnoff_on")
    def test_04_ac_dc(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        logging.info("Step_1: get lace")
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: Lace was enabled and verified successfully for pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace enable with verification failed for pipe_{0}".format(panel.pipe))

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

        ##
        # AC switch
        status = apply_power_mode(display_power.PowerSource.AC)
        if status is False:
            self.fail()

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and self.check_primary_display(port):
                    if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                "LEGACY") is False:
                        self.fail("Lace verification failed")

        ##
        # DC switch
        status = apply_power_mode(display_power.PowerSource.DC)
        if status is False:
            self.fail()

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and self.check_primary_display(port):
                    if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                "LEGACY") is False:
                        self.fail("Lace verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure Lace and verify the persistence with gfx events")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
