#################################################################################################################
# @file         assr_power_events_mode_set.py
# @addtogroup   EDP_ASSR
# @section      Tests
# @brief        assr_power_events_mode_set.py <br> contains ASSR tests for display
#               mode set, power event S3 and power event S4 for both ASSR enabled and ASSR disabled scenario.
#
# @author       Vinod D S, Rohit Kumar
################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.EDP.ASSR.assr_base import *


##
# @brief        This class contains ASSR tests with power events, modeset
class AssrPowerEventsModeSet(AssrBase):

    ############################
    # Test Functions
    ############################

    ##
    # @brief        Test Specific requirements are verified
    # @return       None
    # @cond
    @common.configure_test(selective=["AC_DC", "POST_SI"], critical=True)
    # @endcond
    def t_01_requirements(self):
        ##
        # Enable Simulated Battery
        logging.info("Enabling Simulated Battery")
        result = self.display_power_.enable_disable_simulated_battery(True)
        if result is False:
            self.fail("Failed to enable Simulated Battery")
        logging.info("\tPASS: Expected Simulated Battery Status= ENABLED, Actual= ENABLED")

    ##
    # @brief        This test, with ASSR enabled, verifies ASSR after each display mode set
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_assr_modes(self):
        self.verify_assr_with_mode_set(True)

    ##
    # @brief        This test, with ASSR enabled, verifies ASSR after S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3", "POST_SI"])
    # @endcond
    def t_12_assr_s3(self):
        self.verify_assr_with_power_event(display_power.PowerEvent.S3, True)

    ##
    # @brief        This test, with ASSR enabled, verifies ASSR after S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS", "POST_SI"])
    # @endcond
    def t_13_assr_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("POWER_STATE_CS is not supported (Planning Issue)")
        self.verify_assr_with_power_event(display_power.PowerEvent.CS, True)

    ##
    # @brief        # @brief        This test, with ASSR enabled, verifies ASSR after S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4", "POST_SI"])
    # @endcond
    def t_14_assr_s4(self):
        self.verify_assr_with_power_event(display_power.PowerEvent.S4, True)

    ##
    # @brief        This test verifies ASSR with DC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC_DC", "POST_SI"])
    # @endcond
    def t_15_assr_dc(self):
        self.verify_assr_with_power_source(display_power.PowerSource.DC, True)

    ##
    # @brief        This test verifies ASSR with AC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC_DC", "POST_SI"])
    # @endcond
    def t_15_assr_ac(self):
        self.verify_assr_with_power_source(display_power.PowerSource.AC, True)

    ##
    # @brief        This test, with ASSR disabled, verifies ASSR after each display mode set
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LEGACY", "BLOCKED"])
    # @endcond
    def t_21_assr_modes(self):
        self.verify_assr_with_mode_set(False)

    ##
    # @brief        This test, with ASSR disabled, verifies ASSR after S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3", "LEGACY", "BLOCKED", "POST_SI"])
    # @endcond
    def t_22_assr_s3(self):
        self.verify_assr_with_power_event(display_power.PowerEvent.S3, False)

    ##
    # @brief        This test, with ASSR disabled, verifies ASSR after CS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS", "LEGACY", "BLOCKED", "POST_SI"])
    # @endcond
    def t_23_assr_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("POWER_STATE_CS is not supported (Planning Issue)")
        self.verify_assr_with_power_event(display_power.PowerEvent.CS, False)

    ##
    # @brief        This test, with ASSR disabled, verifies ASSR after S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4", "LEGACY", "BLOCKED", "POST_SI"])
    # @endcond
    def t_24_assr_s4(self):
        self.verify_assr_with_power_event(display_power.PowerEvent.S4, False)

    ##
    # @brief        This test verifes ASSR with DC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC_DC", "LEGACY", "BLOCKED", "POST_SI"])
    # @endcond
    def t_25_assr_dc(self):
        self.verify_assr_with_power_source(display_power.PowerSource.DC, False)

    ##
    # @brief        This test verifes ASSR with AC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC_DC", "LEGACY", "BLOCKED", "POST_SI"])
    # @endcond
    def t_26_assr_ac(self):
        self.verify_assr_with_power_source(display_power.PowerSource.AC, False)

    ##
    # @brief        Test specific cleanup is done
    # @return       None
    # @cond
    @common.configure_test(selective=["AC_DC", "POST_SI"])
    # @endcond
    def t_30_cleanup(self):
        ##
        # Disable Simulated Battery
        logging.info("Disabling Simulated Battery")
        result = self.display_power_.enable_disable_simulated_battery(False)
        if result is False:
            logging.error("Failed to disable Simulated Battery")
        logging.info("\tPASS: Expected Simulated Battery Status= DISABLED, Actual= DISABLED")

    ############################
    # Helper Functions
    ############################

    ##
    # @brief        This is a helper function to check ASSR with display mode set
    # @param[in]    enabled boolean, indicates expected Driver ASSR status
    # @return       None
    def verify_assr_with_mode_set(self, enabled):
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        if enumerated_displays is None:
            self.fail("API get_enumerated_display_info() FAILED (Test Issue)")

        ##
        # Apply all supported resolutions on each edp and check ASSR
        test_status = True
        for edp_panel in self.edp_panels:
            rr_list = common.get_supported_refresh_rates(self.edp_target_ids[edp_panel])
            if len(rr_list) > 1:
                mode_list = []
                for rr in rr_list:
                    mode_list.append(common.get_display_mode(self.edp_target_ids[edp_panel], rr))
            else:
                mode_list = common.get_display_mode(self.edp_target_ids[edp_panel], limit=2)

            for mode in mode_list:
                ##
                # Skip to next mode if current and target modes are same
                current_mode = self.display_config_.get_current_mode(self.edp_target_ids[edp_panel])
                if current_mode == mode:
                    continue

                if self.display_config_.set_display_mode([mode], False) is False:
                    logging.error("\tFailed to apply display mode")
                    test_status = False
                    continue

                current_mode = self.display_config_.get_current_mode(self.edp_target_ids[edp_panel])
                logging.info(
                    "\tApplied mode on {0}=  {1}".format(edp_panel, current_mode.to_string(enumerated_displays)))

                ##
                # Check ASSR
                if self.verify_assr(edp_panel, enabled) is False:
                    test_status = False

        self.assertEquals(test_status, True, "ASSR verification failed after ModeSet operation")

    ##
    # @brief        This is a helper function to check ASSR with power event
    # @param[in]    power_event_type member of enum PowerEvent
    # @param[in]    enabled boolean, indicates expected Driver ASSR status
    # @return       None
    def verify_assr_with_power_event(self, power_event_type, enabled):
        # Invoke power event
        if self.display_power_.invoke_power_event(power_event_type, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event {0}(Test Issue)'.format(power_event_type.name))

        # Check ASSR
        test_status = True
        for edp_panel in self.edp_panels:
            if self.verify_assr(edp_panel, enabled) is False:
                test_status = False
        self.assertEquals(test_status, True, "ASSR verification failed after PowerEvent operation")

    ##
    # @brief        Helper function to check ASSR with power source
    # @param[in]    power_source member of enum PowerLineStatus
    # @param[in]    enabled boolean, indicates expected Driver ASSR status
    # @return       None
    def verify_assr_with_power_source(self, power_source, enabled):
        ##
        # Set current power line status to DC
        if not self.display_power_.set_current_powerline_status(power_source):
            self.fail("Failed to switch power line status to {0}(Test Issue)".format(power_source.name))

        ##
        # Check ASSR
        test_status = True
        for edp_panel in self.edp_panels:
            result = self.verify_assr(edp_panel, enabled)
            if result is False:
                test_status = False
        self.assertEquals(test_status, True, "ASSR verification failed after PowerLine switch")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(
        common.get_test_suite(AssrPowerEventsModeSet, ['0', '1', '2', '3']))
    test_environment.TestEnvironment.cleanup(test_result)
