########################################################################################################################
# @file         lobf_power_events.py
# @brief        Contains basic functional tests covering below scenarios:
#               * LOBF verification with CS/S3/S4
# @author       Bhargav Adigarla
########################################################################################################################
import time

from Libs.Core import display_power, enum
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.LOBF.lobf_base import *


##
# @brief        Contains basic LOBF tests
class LobfPowerEvents(LobfBase):
    ##
    # @brief        This function verifies LOBF with SD and Dual edp scenarios with CS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_10_cs(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
                    self.fail("CS is NOT supported on the system(Planning Issue)")
                if self.display_power_.invoke_power_event(display_power.PowerEvent.CS,
                                                          common.POWER_EVENT_DURATION_DEFAULT) is False:
                    self.fail('Failed to invoke power event CS')
                time.sleep(10)

                if lobf.is_alpm_supported(panel):
                    if lobf.verify_restrictions(adapter, panel) is False:
                        self.fail("LOBF restrictions failed in driver")
                    logging.info("LOBF restrictions satisfied, verifying LOBF")
                    if lobf.is_lobf_enabled_in_driver(adapter, panel) is False:
                        self.fail("LOBF is disabled in driver")
                    logging.info("LOBF Enabled in driver")

                else:
                    logging.info("ALPM is not supported in panel, verifying AUX wake LOBF")
                    if lobf.verify_auxwake(adapter, panel) is False:
                        self.fail("AUX wake LOBF disabled on non ALPM panel")
                    logging.info("AUX wake LOBF enabled")

    ##
    # @brief        This function verifies LOBF with SD and Dual edp scenarios with S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3"])
    # @endcond
    def t_11_s3(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
                    self.fail("S3 is NOT supported on the system(Planning Issue)")

                if self.display_power_.invoke_power_event(display_power.PowerEvent.S3,
                                                          common.POWER_EVENT_DURATION_DEFAULT) is False:
                    self.fail('Failed to invoke power event S3')
                time.sleep(10)
                if lobf.is_alpm_supported(panel):
                    if lobf.verify_restrictions(adapter, panel) is False:
                        self.fail("LOBF restrictions failed in driver")
                    logging.info("LOBF restrictions satisfied, verifying LOBF")
                    if lobf.is_lobf_enabled_in_driver(adapter, panel) is False:
                        self.fail("LOBF is disabled in driver")
                    logging.info("LOBF Enabled in driver")

                else:
                    logging.info("ALPM is not supported in panel, verifying AUX wake LOBF")
                    if lobf.verify_auxwake(adapter, panel) is False:
                        self.fail("AUX wake LOBF disabled on non ALPM panel")
                    logging.info("AUX wake LOBF enabled")

    ##
    # @brief        This function verifies LOBF with SD and Dual edp scenarios with S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_12_s4(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if self.display_power_.invoke_power_event(display_power.PowerEvent.S4,
                                                          common.POWER_EVENT_DURATION_DEFAULT) is False:
                    self.fail('Failed to invoke power event S4')
                time.sleep(10)
                if lobf.is_alpm_supported(panel):
                    if lobf.verify_restrictions(adapter, panel) is False:
                        self.fail("LOBF restrictions failed in driver")
                    logging.info("LOBF restrictions satisfied, verifying LOBF")
                    if lobf.is_lobf_enabled_in_driver(adapter, panel) is False:
                        self.fail("LOBF is disabled in driver")
                    logging.info("LOBF Enabled in driver")

                else:
                    logging.info("ALPM is not supported in panel, verifying AUX wake LOBF")
                    if lobf.verify_auxwake(adapter, panel) is False:
                        self.fail("AUX wake LOBF disabled on non ALPM panel")
                    logging.info("AUX wake LOBF enabled")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LobfPowerEvents))
    test_environment.TestEnvironment.cleanup(test_result)