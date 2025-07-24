#################################################################################################################
# @file         edp_flt_power_event.py
# @brief        This file contains EDP FLT test with power events and modeset
# @author       Tulika
#################################################################################################################

from Libs.Core import display_power, enum
from Libs.Core.test_env import test_environment
from Libs.Feature.voltage_swing import voltage_swing_dp as vswing
from Tests.EDP.FLT.flt_base import *
from Tests.PowerCons.Modules import common, dut, workload


##
# @brief        This class contains EDP FLT tests with power events and modeset
class EdpFltPowerEvent(EdpFltBase):
    display_mode_list = {}
    enumerated_displays = None
    display_power_ = display_power.DisplayPower()

    ############################
    # Test Function
    ############################

    ##
    # @brief        This test verifies EDP FLT with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_11_s4(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if common.is_simulated_panel(panel.target_id) is False:
                    self.fail("S4 test is NOT supported with physical panel for FLT (Planning Issue)")
                self.invoke_power_event_and_verify(display_power.PowerEvent.S4, self.is_flt_enabled, True)

    ##
    # @brief        This test verifies EDP FLT with CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_12_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("CS is NOT enabled in the system (Planning Issue)")
        self.invoke_power_event_and_verify(display_power.PowerEvent.CS, self.is_flt_enabled, True)

    ##
    # @brief        This test verifies EDP FLT with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3"])
    # @endcond
    def t_13_s3(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            self.fail("S3 is NOT enabled in the system (Planning Issue)")
        self.invoke_power_event_and_verify(display_power.PowerEvent.S3, self.is_flt_enabled, True)

    ############################
    # Helper Functions
    ############################

    ##
    # @brief        Helper function to invoke given power event and verify FLT or Full Link Training
    # @param[in]    power_event Enum, targeted power event
    # @param[in]    is_flt_enabled Boolean, True if FLT is expected after power event, False otherwise
    # @param[in]    is_flt_expected Boolean, True if FLT is expected after power event, False otherwise
    # @return       None
    def invoke_power_event_and_verify(self, power_event, is_flt_enabled, is_flt_expected):
        if workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforePowerEvent") is False:
            self.fail("FAILED to stop and start ETL")

        if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail(f"FAILED to invoke power event {display_power.PowerEvent(power_event)}")

        status, etl_file = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuringPowerEvent")

        if status is None:
            self.fail("FAILED to get ETL during Power Event")

        if self.is_phy_test is False:
            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    if panel.is_lfp is False:
                        continue
                    if flt.verify(panel, etl_file, is_flt_enabled, is_flt_expected) is False:
                        self.fail(f"FAIL: FLT verification after display switch for {panel.port}")
                    logging.info(f"PASS: FLT verification Successful after display switch for {panel.port}")

        # Verify voltage swing programming
        if self.is_phy_test:
            for adapter in dut.adapters.values():
                if vswing.is_platform_supported(adapter.name) is False:
                    self.fail(f"FAIL: Platform NOT added in Voltage Swing Programming file")
                for panel in adapter.panels.values():
                    if panel.is_lfp is False:
                        continue
                    if vswing.verify_voltage_swing(panel.port) is False:
                        self.fail(f"FAIL: PHY programming verification failed for {panel.port}")
                    logging.info(f"PASS: PHY programming verification passed successfully for {panel.port}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(EdpFltPowerEvent))
    test_environment.TestEnvironment.cleanup(test_result)

