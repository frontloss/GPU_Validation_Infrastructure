########################################################################################################################
# @file         cfps_validate.py
# @brief        Contains functional tests for CFPS
#
# @author       Vinod D S
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.CFPS.cfps_base import *


##
# @brief        This class contains tests to verify Cfps.
class CfpsValidate(CfpsBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test function is to verify cfps with power saver scheme and DC power source in windowed mode
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "POWER_SAVER", "DC"])
    # @endcond
    def t_11a_windowed_power_saver_dc(self):
        self.validate_cfps_with(False, display_power.PowerScheme.POWER_SAVER, display_power.PowerSource.DC,
                                self.power_event)

    ##
    # @brief        Test function is to verify cfps with power saver scheme and AC power source in windowed mode
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "POWER_SAVER", "AC"])
    # @endcond
    def t_11b_windowed_power_saver_ac(self):
        self.validate_cfps_with(False, display_power.PowerScheme.POWER_SAVER, display_power.PowerSource.AC,
                                self.power_event)

    ##
    # @brief        Test function is to verify cfps with balanced power scheme and DC power source in windowed
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "BALANCED", "DC"])
    # @endcond
    def t_12a_windowed_balanced_dc(self):
        self.validate_cfps_with(False, display_power.PowerScheme.BALANCED, display_power.PowerSource.DC,
                                self.power_event)

    ##
    # @brief        Test function is to verify cfps with balanced power scheme and AC power source in windowed mode
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "BALANCED", "AC"])
    # @endcond
    def t_12b_windowed_balanced_ac(self):
        self.validate_cfps_with(False, display_power.PowerScheme.BALANCED, display_power.PowerSource.AC,
                                self.power_event)

    ##
    # @brief        Test function is to verify cfps with high performance power scheme and DC power source
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "HIGH_PERFORMANCE", "DC"])
    # @endcond
    def t_13a_windowed_high_performance_dc(self):
        self.validate_cfps_with(False, display_power.PowerScheme.HIGH_PERFORMANCE, display_power.PowerSource.DC,
                                self.power_event)

    ##
    # @brief        Test function is to verify cfps with high performance power scheme and AC power source
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "HIGH_PERFORMANCE", "AC"])
    # @endcond
    def t_13b_windowed_high_performance_ac(self):
        self.validate_cfps_with(False, display_power.PowerScheme.HIGH_PERFORMANCE, display_power.PowerSource.AC,
                                self.power_event)

    ##
    # @brief        Test function is to verify cfps with high performance power scheme and DC power source, in
    #               full screen mode
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "POWER_SAVER", "DC"])
    # @endcond
    def t_14a_fullscreen_power_saver_dc(self):
        self.validate_cfps_with(True, display_power.PowerScheme.POWER_SAVER, display_power.PowerSource.DC,
                                self.power_event)

    ##
    # @brief        Test function is to verify cfps with high performance power scheme and AC power source, in
    #               full screen mode
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "POWER_SAVER", "AC"])
    # @endcond
    def t_14b_fullscreen_power_saver_ac(self):
        self.validate_cfps_with(True, display_power.PowerScheme.POWER_SAVER, display_power.PowerSource.AC,
                                self.power_event)

    ##
    # @brief        Test function is to verify cfps with balanced power scheme and DC power source, in
    #               full screen mode
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "BALANCED", "DC"])
    # @endcond
    def t_15a_fullscreen_balanced_dc(self):
        self.validate_cfps_with(True, display_power.PowerScheme.BALANCED, display_power.PowerSource.DC, self.power_event)

    ##
    # @brief        Test function is to verify cfps with balanced power scheme and AC power source, in
    #               full screen mode
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "BALANCED", "AC"])
    # @endcond
    def t_15b_fullscreen_balanced_ac(self):
        self.validate_cfps_with(True, display_power.PowerScheme.BALANCED, display_power.PowerSource.AC, self.power_event)

    ##
    # @brief        Test function is to verify cfps with high performance power scheme and DC power source, in
    #               full screen mode
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "HIGH_PERFORMANCE", "DC"])
    # @endcond
    def t_16a_fullscreen_high_performance_dc(self):
        self.validate_cfps_with(True, display_power.PowerScheme.HIGH_PERFORMANCE, display_power.PowerSource.DC,
                                self.power_event)

    ##
    # @brief        Test function is to verify cfps with high performance power scheme and AC power source, in
    #               full screen mode
    # @note         Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "HIGH_PERFORMANCE", "AC"])
    # @endcond
    def t_16b_fullscreen_high_performance_ac(self):
        self.validate_cfps_with(True, display_power.PowerScheme.HIGH_PERFORMANCE, display_power.PowerSource.AC,
                                self.power_event)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CfpsValidate))
    test_environment.TestEnvironment.cleanup(test_result)
