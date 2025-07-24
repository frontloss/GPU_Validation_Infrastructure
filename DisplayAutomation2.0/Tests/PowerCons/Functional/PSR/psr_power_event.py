#######################################################################################################################
# @file             psr_power_event.py
# @brief            PSR Tests with power events
# @details          Test for PSR in power events scenarios CS, S3, S4 with AC and DC power source
#
# @author           Rohit Kumar
#######################################################################################################################

from Libs.Core import display_power
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.PSR.psr_base import *


##
# @brief        Contains PSR tests in power event scenarios
class TestPowerEvent(PsrBase):

    ##
    # @brief        Test function to verify PSR in CS and S4 power events with AC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC", "CS", "S4"])
    # @endcond
    def t_11_power_cs_s4_ac(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("CS is NOT supported on the system(Planning Issue)")
        self.validate_feature(display_power.PowerSource.AC, display_power.PowerEvent.CS)
        self.validate_feature(display_power.PowerSource.AC, display_power.PowerEvent.S4)

    ##
    # @brief        Test function to verify PSR in CS and S4 power events with DC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC", "CS", "S4"])
    # @endcond
    def t_12_power_cs_s4_dc(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("CS is NOT supported on the system(Planning Issue)")
        self.validate_feature(display_power.PowerSource.DC, display_power.PowerEvent.CS)
        self.validate_feature(display_power.PowerSource.DC, display_power.PowerEvent.S4)

    ##
    # @brief        Test function to verify PSR in S3 and S4 power events with AC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC", "S3", "S4"])
    # @endcond
    def t_13_power_s3_s4_ac(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            self.fail("S3 is NOT supported on the system(Planning Issue)")
        self.validate_feature(display_power.PowerSource.AC, display_power.PowerEvent.S3)
        self.validate_feature(display_power.PowerSource.AC, display_power.PowerEvent.S4)

    ##
    # @brief        Test function to verify PSR in S3 and S4 power events with DC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC", "S3", "S4"])
    # @endcond
    def t_14_power_s3_s4_dc(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            self.fail("S3 is NOT supported on the system(Planning Issue)")
        self.validate_feature(display_power.PowerSource.DC, display_power.PowerEvent.S3)
        self.validate_feature(display_power.PowerSource.DC, display_power.PowerEvent.S4)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestPowerEvent))
    test_environment.TestEnvironment.cleanup(test_result)
