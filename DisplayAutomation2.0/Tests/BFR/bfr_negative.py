########################################################################################################################
# @file         bfr_negative.py
# @brief        Contains negative tests for BFR
# @details      Basic functional tests are covering below scenarios:
#               * BFR verification for negative scenario
#
#
# @author       Gopikrishnan R
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.BFR.bfr_base import *
from Tests.PowerCons.Functional.DMRRS import dmrrs


##
# @brief        This class contains basic BFR tests
#               This class inherits the BfrBase class.
class BfrNegative(BfrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        BFR verification with DMRRS disabled, BFR shouldn't function in this case
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DMRRS_DISABLED"])
    # @endcond
    def t_11_dmrrs_disabled(self):
        for adapter in dut.adapters.values():
            status = dmrrs.disable(adapter)
            if status is False:
                self.fail("Unable to disable DMRRS")
            if status:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail("\tFailed to restart display driver after DMRRS disable update")

        result = self.bfr_basic(maximized=True, negative=True)

        for adapter in dut.adapters.values():
            status = dmrrs.enable(adapter)
            if status is False:
                self.fail("Unable to Enable DMRRS")
            if status:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail("\tFailed to restart display driver after DMRRS Enable update")

        if not result:
            self.fail(f"FAIL : Basic Test : BFR verification failed with negative configuration")

    ##
    # @brief        BFR feature disable with regkey. BFR shouldn't function in this case
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["BFR_DISABLED"])
    # @endcond
    def t_12_bfr_disabled(self):
        for adapter in dut.adapters.values():
            self.enable_disable_bfr_via_regkey(enable=False)
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                logging.info(f"\t{panel.bfr_caps}")

        result = self.bfr_basic(negative=True)

        if not result:
            self.fail(f"FAIL : Basic Test : BFR disable verification failed")

    ##
    # @brief        BFR Negative test for 314h source based VTotal DPCD value not present
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["NO_SOURCE_BASED_VTOTAL_DPCD"])
    # @endcond
    def t_13_no_bfr_dpcd(self):
        # BFR is expected not to work with panels of 314h Bit2 is not set
        # Enabling PSR to make sure BFR is not working.
        for adapter in dut.adapters.values():
            if psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1):
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail(f"Failed to restart display driver for {adapter.name}")
                logging.info(f"\tSuccessfully restarted display driver for {adapter.name} after enabling PSR")
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                logging.info(f"\t{panel.bfr_caps}")

        if not self.bfr_basic(negative=True):
            self.fail(f"FAIL : BFR is enabled with BFR unsupported panel")
        logging.info(f"PASS : BFR is not working with BFR unsupported panel")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BfrNegative))
    TestEnvironment.cleanup(test_result)
