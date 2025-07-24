########################################################################################################################
# @file         lobf_psr2_enable_disable.py
# @brief        Contains basic functional tests covering below scenarios:
#               * LOBF verification in with PSR disable and enable in SD EDP and Dual eDP combinations
# @author       Bhargav Adigarla
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.LOBF.lobf_base import *
from Tests.PowerCons.Functional.PSR import psr


##
# @brief        Contains basic LOBF tests
class LobfPsrDisable(LobfBase):
    ##
    # @brief        This function verifies LOBF with SD and Dual edp scenarios
    # @return       None
    def t_10_basic(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported and psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1) is False:
                    self.fail("Failed to disable PSR1")

                if lobf.is_alpm_supported(panel):
                    if lobf.verify_restrictions(adapter, panel) is False:
                        self.fail("LOBF restrictions failed in driver")
                    logging.info("LOBF restrictions satisfied, verifying LOBF")
                    if lobf.is_lobf_enabled_in_driver(adapter, panel) is False:
                        self.fail("LOBF is disabled in driver")
                    logging.info("LOBF enabled in driver")

                else:
                    logging.info("ALPM is not supported in panel, verifying AUX wake LOBF")
                    if lobf.verify_auxwake(adapter, panel) is False:
                        self.fail("AUX wake LOBF enabled on non ALPM panel")
                    logging.info("AUX wake LOBF disabled")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LobfPsrDisable))
    test_environment.TestEnvironment.cleanup(test_result)
