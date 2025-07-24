########################################################################################################################
# @file         test_psr_enable_disable.py
# @brief        Test for DC state in PSR enable/Disable scenario
#
# @author       Vinod D S
########################################################################################################################


from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains DC States tests with PSR enable/disable
class TestPsrEnableDisable(DCStatesBase):

    ##
    # @brief        This is a helper function to restart psr for DC States tests
    # @param[in]    adapter Adapter
    # @param[in]    version number representing the PSR version
    # @return       None
    def _restart_psr(self, adapter, version):
        status = True
        if psr.disable(adapter.gfx_index, version) is True:
            status, reboot_required = display_essential.restart_gfx_driver()
        time.sleep(3)
        if psr.enable(adapter.gfx_index, version) is True:
            status, reboot_required = display_essential.restart_gfx_driver()
        return status

    ##
    # @brief        This function verifies DC5/6 with PSR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC5", "DC6"])
    # @endcond
    def t_10_state_dc5_dc6(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if panel.psr_caps.is_psr2_supported is True:
                    # Verify DC states after PSR disable/enable
                    self._restart_psr(adapter, psr.UserRequestedFeature.PSR_2)
                elif panel.psr_caps.is_psr_supported is True:
                    # Verify DC states after PSR disable/enable
                    self._restart_psr(adapter, psr.UserRequestedFeature.PSR_1)
                logging.info("Step: Verifying DC5/6 with Idle desktop")
                if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                    self.fail("DC5/6 verification with idle failed")
                logging.info("\tDC5/6 verification with idle is successful")

    ##
    # @brief        This function verifies DC6v with PSR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V"])
    # @endcond
    def t_11_state_dc6v(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if panel.psr_caps.is_psr2_supported is False:
                    self.fail("DC6v works with PSR2 only (Planning Issue)")
                # Verify DC states after PSR disable/enable
                self._restart_psr(adapter, psr.UserRequestedFeature.PSR_2)

                logging.info("Step: Verifying DC6v with App")
                if dc_state.verify_dc6v(adapter, method='APP') is False:
                    self.fail("DC6v verification with app failed")
                logging.info("\tDC6v verification with app is successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestPsrEnableDisable))
    test_environment.TestEnvironment.cleanup(test_result)
