########################################################################################################################
# @file         edp_flt_display_switch.py
# @brief        This file contains test for EDP FLT with display switch event
# @author       Tulika
########################################################################################################################
import logging
import time

from Libs.Core import enum
from Libs.Core.test_env import test_environment
from Tests.EDP.FLT.flt_base import *
from Tests.PowerCons.Modules import common, dut, workload
from Libs.Feature.voltage_swing import voltage_swing_dp as vswing


##
# @brief        This class contains tests for EDP FLT with display switch event
class EdpFltDisplaySwitch(EdpFltBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This test verifies EDP FLT with display switch event
    # @details      The internal displays are switched off for modeset and display configuration is applied after which
    #               link training and voltage swing programming is verified
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_display_switch(self):
        self.lfp_panels = []
        self.external_panels = []

        if workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeDisplaySwitch") is False:
            self.fail("FAILED to stop and start ETL")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    self.lfp_panels.append(panel.port)
                else:
                    self.external_panels.append(panel.port)

            if len(self.external_panels) == 0:
                self.fail("External panel not found (Planning Issue)")

            config_list = [
                        (enum.SINGLE, [self.external_panels[0]]),
                        (enum.SINGLE, [self.lfp_panels[0]])
                        ]

            for config in config_list:
                if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                    self.fail(f"FAILED to apply display config")
                common.print_current_topology("\t")

            status, etl_file = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuringDisplaySwitch")

            if status is None:
                self.fail("FAILED to get ETL during Power Event")

            if self.is_phy_test is False:
                for panel in adapter.panels.values():
                    if panel.is_lfp is False:
                        continue
                    if flt.verify(panel, etl_file, self.is_flt_enabled, True) is False:
                        self.fail(f"FAIL: FLT verification failed after display switch for {panel.port} ")
                    logging.info(f"PASS: FLT verification Successful after display switch for {panel.port}")

            # Verify voltage swing programming
            if self.is_phy_test:
                if vswing.is_platform_supported(adapter.name) is False:
                    self.fail(f"FAIL: Platform NOT added in Voltage Swing Programming file")
                for panel in adapter.panels.values():
                    if panel.is_lfp is False:
                        continue
                    if vswing.verify_voltage_swing(panel.port) is False:
                        self.fail(f"FAIL: PHY programming verification failed for {panel.port}")
                    logging.info(f"PASS: PHY programming Verification Successful for {panel.port}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(EdpFltDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)

