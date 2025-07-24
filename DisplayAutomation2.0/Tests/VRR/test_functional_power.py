########################################################################################################################
# @file         test_functional_power.py
# @brief        Contains power event functional tests for VRR
# @details      Power event functional tests are covering below scenarios:
#               * VRR verification in WINDOWED and FULL SCREEN modes with NO_LOW_HIGH_FPS/LOW_FPS/HIGH_FPS/LOW_HIGH_FPS
#               settings after CS/S3/S4 power events
#               * VRR verification in WINDOWED and FULL SCREEN modes with NO_LOW_HIGH_FPS/LOW_FPS/HIGH_FPS/LOW_HIGH_FPS
#               settings in AC/DC power source modes
#               * All tests will be executed on VRR panel with VRR enabled. VRR is expected to be working in all above
#               scenarios.
#
# @author       Rohit Kumar
########################################################################################################################

from Libs.Core import enum
from typing import Dict, List
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VRR.vrr_base import *
from Libs.Feature.powercons import registry


##
# @brief        This class contains VRR tests for different power events with setup and teardown functions.
#               This class inherits the VrrBase class.
class VrrPowerEvents(VrrBase):

    ##
    # @brief        This class method is the entry point for any VRR power event cases. Helps to initialize some of
    #               the parameters required for the test execution in this file.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(VrrPowerEvents, cls).setUpClass()
        # Enable Simulated Battery
        logging.info("Enabling Simulated Battery")
        assert cls.display_power_.enable_disable_simulated_battery(True), "Failed to enable Simulated Battery"
        logging.info("\tPASS: Expected Simulated Battery Status= ENABLED, Actual= ENABLED")

    ##
    # @brief        This class method is the executed after the VRR power event test cases. Helps to disable the
    #               the settings created for the execution of the power event test cases
    # @return       None
    @classmethod
    def tearDownClass(cls):
        super(VrrPowerEvents, cls).tearDownClass()
        # Disable Simulated Battery
        logging.info("Disabling Simulated Battery")
        if cls.display_power_.enable_disable_simulated_battery(False) is False:
            logging.error("Failed to disable Simulated Battery")
        else:
            logging.info("\tPASS: Expected Simulated Battery Status= DISABLED, Actual= DISABLED")

    ############################
    # Test Function
    ############################

    ##
    # @brief        VRR verification after S4 in WINDOWED mode, NO_LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "S4", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_11_vrr_s4_windowed(self):
        if self.verify_vrr_power_event(False, power_event=display_power.PowerEvent.S4) is False:
            self.fail("VRR verification failed after S4 in WINDOWED mode")

    ##
    # @brief        VRR verification after S4 in FULL_SCREEN mode, NO_LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "S4", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_12_vrr_s4_full_screen(self):
        if self.verify_vrr_power_event(True, power_event=display_power.PowerEvent.S4) is False:
            self.fail("VRR verification failed after S4 in FULL_SCREEN mode")

    ##
    # @brief        VRR verification of WINDOWED mode in S3 power state, NO_LOW_HIGH_FPS
    # @return       None2
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "CS", "S3", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_13_vrr_cs_s3_windowed(self):
        power_state = display_power.PowerEvent.S3
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_state = display_power.PowerEvent.CS
        if self.verify_vrr_power_event(False, power_event=power_state) is False:
            self.fail("VRR verification failed after {0} in WINDOWED mode".format(power_state.name))

    ##
    # @brief        VRR verification of FULL_SCREEN mode in S4 power state, NO_LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "CS", "S3", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_14_vrr_cs_s3_full_screen(self):
        power_state = display_power.PowerEvent.S3
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_state = display_power.PowerEvent.CS
        if self.verify_vrr_power_event(True, power_event=power_state) is False:
            self.fail("VRR verification failed after {0} in FULL_SCREEN mode".format(
                power_state.name))

    ##
    # @brief        VRR verification of FULL_SCREEN mode in S4 power state, NO_LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "AC_DC", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_15_vrr_ac_windowed(self):
        if self.verify_vrr(False, power_source=display_power.PowerSource.AC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_AC in WINDOWED mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_AC in FULL_SCREEN mode,NO_LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "AC_DC", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_16_vrr_ac_full_screen(self):
        if self.verify_vrr(True, power_source=display_power.PowerSource.AC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_AC in FULL_SCREEN mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_DC in WINDOWED mode, NO_LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "AC_DC", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_17_vrr_dc_windowed(self):
        if self.verify_vrr(False, power_source=display_power.PowerSource.DC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_DC in WINDOWED mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_DC in FULL_SCREEN mode, NO_LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "AC_DC", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_18_vrr_dc_full_screen(self):
        if self.verify_vrr(True, power_source=display_power.PowerSource.DC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_DC in FULL_SCREEN mode")

    ##
    # @brief        VRR verification after S4 in WINDOWED mode, LOW_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "S4", "LOW_FPS"])
    # @endcond
    def t_21_vrr_s4_windowed(self):
        if self.verify_vrr_power_event(False, power_event=display_power.PowerEvent.S4) is False:
            self.fail("VRR verification failed after S4 in WINDOWED mode")

    ##
    # @brief        VRR verification after S4 in FULL_SCREEN mode, LOW_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "S4", "LOW_FPS"])
    # @endcond
    def t_22_vrr_s4_full_screen(self):
        if self.verify_vrr_power_event(True, power_event=display_power.PowerEvent.S4) is False:
            self.fail("VRR verification failed after S4 in FULL_SCREEN mode")

    ##
    # @brief        VRR verification after S3/CS in WINDOWED mode, LOW_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "CS", "S3", "LOW_FPS"])
    # @endcond
    def t_23_vrr_cs_s3_windowed(self):
        power_state = display_power.PowerEvent.S3
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_state = display_power.PowerEvent.CS
        if self.verify_vrr_power_event(False, power_event=power_state) is False:
            self.fail("VRR verification failed after {0} in WINDOWED mode".format(
                power_state.name))

    ##
    # @brief        VRR verification after S3/CS in FULL_SCREEN mode, LOW_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "CS", "S3", "LOW_FPS"])
    # @endcond
    def t_24_vrr_cs_s3_full_screen(self):
        power_state = display_power.PowerEvent.S3
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_state = display_power.PowerEvent.CS
        if self.verify_vrr_power_event(True, power_event=power_state) is False:
            self.fail("VRR verification failed after {0} in FULL_SCREEN mode".format(
                power_state.name))

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_AC in WINDOWED mode, LOW_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "AC_DC", "LOW_FPS"])
    # @endcond
    def t_25_vrr_ac_windowed(self):
        if self.verify_vrr(False, power_source=display_power.PowerSource.AC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_AC in WINDOWED mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_AC in FULL_SCREEN mode, LOW_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "AC_DC", "LOW_FPS"])
    # @endcond
    def t_26_vrr_ac_full_screen(self):
        if self.verify_vrr(True, power_source=display_power.PowerSource.AC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_AC in FULL_SCREEN mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_DC in WINDOWED mode, LOW_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "AC_DC", "LOW_FPS"])
    # @endcond
    def t_27_vrr_dc_windowed(self):
        if self.verify_vrr(False, power_source=display_power.PowerSource.DC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_DC in WINDOWED mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_DC in FULL_SCREEN mode, LOW_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "AC_DC", "LOW_FPS"])
    # @endcond
    def t_28_vrr_dc_full_screen(self):
        if self.verify_vrr(True, power_source=display_power.PowerSource.DC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_DC in FULL_SCREEN mode")

    ##
    # @brief        VRR verification after S4 in WINDOWED mode, HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "S4", "HIGH_FPS"])
    # @endcond
    def t_31_vrr_s4_windowed(self):
        if self.verify_vrr_power_event(False, power_event=display_power.PowerEvent.S4) is False:
            self.fail("VRR verification failed after S4 in WINDOWED mode")

    ##
    # @brief        VRR verification after S4 in FULL_SCREEN mode, HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "S4", "HIGH_FPS"])
    # @endcond
    def t_32_vrr_s4_full_screen(self):
        if self.verify_vrr_power_event(True, power_event=display_power.PowerEvent.S4) is False:
            self.fail("VRR verification failed after S4 in FULL_SCREEN mode")

    ##
    # @brief        VRR verification after S3/CS in WINDOWED mode, HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "CS", "S3", "HIGH_FPS"])
    # @endcond
    def t_33_vrr_cs_s3_windowed(self):
        power_state = display_power.PowerEvent.S3
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_state = display_power.PowerEvent.CS
        if self.verify_vrr_power_event(False, power_event=power_state) is False:
            self.fail("VRR verification failed after {0} in WINDOWED mode".format(
                power_state.name))

    ##
    # @brief        VRR verification after S3/CS in FULL_SCREEN mode, HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "CS", "S3", "HIGH_FPS"])
    # @endcond
    def t_34_vrr_cs_s3_full_screen(self):
        power_state = display_power.PowerEvent.S3
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_state = display_power.PowerEvent.CS
        if self.verify_vrr_power_event(True, power_event=power_state) is False:
            self.fail("VRR verification failed after {0} in FULL_SCREEN mode".format(
                power_state.name))

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_AC in WINDOWED mode, HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "AC_DC", "HIGH_FPS"])
    # @endcond
    def t_35_vrr_ac_windowed(self):
        if self.verify_vrr(False, power_source=display_power.PowerSource.AC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_AC in WINDOWED mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_AC in FULL_SCREEN mode, HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "AC_DC", "HIGH_FPS"])
    # @endcond
    def t_36_vrr_ac_full_screen(self):
        if self.verify_vrr(True, power_source=display_power.PowerSource.AC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_AC in FULL_SCREEN mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_DC in WINDOWED mode, HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "AC_DC", "HIGH_FPS"])
    # @endcond
    def t_37_vrr_dc_windowed(self):
        if self.verify_vrr(False, power_source=display_power.PowerSource.DC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_DC in WINDOWED mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_DC in FULL_SCREEN mode, HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "AC_DC", "HIGH_FPS"])
    # @endcond
    def t_38_vrr_dc_full_screen(self):
        if self.verify_vrr(True, power_source=display_power.PowerSource.DC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_DC in FULL_SCREEN mode")

    ##
    # @brief        VRR verification after S4 in WINDOWED mode, LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "S4", "LOW_HIGH_FPS"])
    # @endcond
    def t_41_vrr_s4_windowed(self):
        if self.verify_vrr_power_event(False, power_event=display_power.PowerEvent.S4) is False:
            self.fail("VRR verification failed after S4 in WINDOWED mode")

    ##
    # @brief        VRR verification after S4 in FULL_SCREEN mode, LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "S4", "LOW_HIGH_FPS"])
    # @endcond
    def t_42_vrr_s4_full_screen(self):
        if self.verify_vrr_power_event(True, power_event=display_power.PowerEvent.S4) is False:
            self.fail("VRR verification failed after S4 in FULL_SCREEN mode")

    ##
    # @brief        VRR verification after S3/CS in WINDOWED mode, LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "CS", "S3", "LOW_HIGH_FPS"])
    # @endcond
    def t_43_vrr_cs_s3_windowed(self):
        power_state = display_power.PowerEvent.S3
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_state = display_power.PowerEvent.CS
        if self.verify_vrr_power_event(False, power_event=power_state) is False:
            self.fail("VRR verification failed after {0} in WINDOWED mode".format(
               power_state.name))

    ##
    # @brief        VRR verification after S3/CS in FULL_SCREEN mode, LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "CS", "S3", "LOW_HIGH_FPS"])
    # @endcond
    def t_44_vrr_cs_s3_full_screen(self):
        power_state = display_power.PowerEvent.S3
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_state = display_power.PowerEvent.CS
        if self.verify_vrr_power_event(True, power_event=power_state) is False:
            self.fail("VRR verification failed after {0} in FULL_SCREEN mode".format(
               power_state.name))

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_AC in WINDOWED mode, LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "AC_DC", "LOW_HIGH_FPS"])
    # @endcond
    def t_45_vrr_ac_windowed(self):
        if self.verify_vrr(False, power_source=display_power.PowerSource.AC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_AC in WINDOWED mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_AC in FULL_SCREEN mode, LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "AC_DC", "LOW_HIGH_FPS"])
    # @endcond
    def t_46_vrr_ac_full_screen(self):
        if self.verify_vrr(True, power_source=display_power.PowerSource.AC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_AC in FULL_SCREEN mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_DC in WINDOWED mode, LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "AC_DC", "LOW_HIGH_FPS"])
    # @endcond
    def t_47_vrr_dc_windowed(self):
        if self.verify_vrr(False, power_source=display_power.PowerSource.DC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_DC in WINDOWED mode")

    ##
    # @brief        VRR verification after POWER_LINE_STATUS_DC in FULL_SCREEN mode, LOW_HIGH_FPS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "AC_DC", "LOW_HIGH_FPS"])
    # @endcond
    def t_48_vrr_dc_full_screen(self):
        if self.verify_vrr(True, power_source=display_power.PowerSource.DC) is False:
            self.fail("VRR verification failed after POWER_LINE_STATUS_DC in FULL_SCREEN mode")

    ##
    # @brief        This is a helper function used to apply a display mode and verify vrr
    # @param[in]    full_screen indicates if the video should be in full screen mode or not
    # @param[in]    power_event - Power event CS/S4/S3
    # @return       status - boolean True if passed, False otherwise
    def verify_vrr_power_event(self, full_screen, power_event=None):
        # fetch current value of regkeys
        regkey_with_values = {}
        registry_keys = [registry.RegKeys.VRR.VRR_ADAPTIVE_VSYNC_ENABLE,
                         registry.RegKeys.VRR.VRR_ADAPTIVE_VSYNC_USER_SETTING]
        for adapter in dut.adapters.values():
            regkey_with_values = common.get_regkey_value(adapter, registry_keys)

        if None in regkey_with_values.values():
            logging.error(f"{regkey_with_values} one of regkey doesn't exist")
            return False

        status = self.verify_vrr(full_screen, power_event)
        logging.info(f"Post verifying VRR status is : {status}")

        # Verify regkey persistence after power event
        for adapter in dut.adapters.values():
            status &= common.verify_regkey_persistence(adapter, regkey_with_values)

        return status


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(VrrPowerEvents))
    TestEnvironment.cleanup(test_result)
