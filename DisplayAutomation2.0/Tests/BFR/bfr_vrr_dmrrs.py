########################################################################################################################
# @file         bfr_vrr_dmrrs.py
# @brief        Contains tests for BFR and concurrency of other RR features in dynamic RR mode
# @details      Basic functional tests are covering below scenarios:
#               * BFR verification in FULL SCREEN mode, DMRRS and VRR path also verified in Dynamic RR mode,
#                 Concurrency of these features in dynamic RR mode.
#               * All tests will be executed on VRR panel with VRR enabled. BFR is expected to be working in all above
#               scenarios.
#
# @author       Gopikrishnan R
########################################################################################################################
from Libs.Core import display_essential, enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PowerCons.Functional.DMRRS.dmrrs_basic import DmrrsBasic
from Tests.PowerCons.Functional.DMRRS import hrr
from Tests.BFR.bfr_base import *


##
# @brief        This class contains basic BFR tests and concurrency of other RR features in dynamic RR mode
#               This class inherits the BfrBase class.
class BfrVrrDmrrs(BfrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        BFR basic test that verifies basic BFR flow
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MAXIMIZED"], critical=False)
    # @endcond
    def t_11_bfr_basic(self):
        if not self.bfr_basic():
            self.fail(f"FAIL : Basic Test : BFR verification failed")

    ##
    # @brief        DMRRS verification with the specified refresh rate
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DMRRS"], critical=False)
    # @endcond
    def t_12_dmrrs(self):
        dmrrs_obj = DmrrsBasic()

        # todo VSDI-28161 Adding as DMRRS verificaiton is failing due to HRR
        for adapter in dut.adapters.values():
            hrr_status = hrr.disable(adapter)
            dut.refresh_panel_caps(adapter)
            if hrr_status is False:
                self.fail(f"FAILED to disable HRR on {adapter.name}")
            if hrr_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("\tFAILED to restart display driver after reg-key update")
            logging.info(f"PASS: Disabled HRR on {adapter.name}")
            dut.refresh_panel_caps(adapter)
            break

        if dmrrs_obj.verify_basic(self.media_refresh_rate, display_power.PowerSource.DC) is False:
            self.fail("FAIL : Basic Test : DMRRS verification failed")

        # todo VSDI-28161 Adding as DMRRS verificaiton is failing due to HRR
        for adapter in dut.adapters.values():
            hrr_status = hrr.enable(adapter)
            dut.refresh_panel_caps(adapter)
            if hrr_status is False:
                self.fail(f"FAILED to enable HRR back on {adapter.name}")
            if hrr_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("\tFAILED to restart display driver after reg-key update")
            logging.info(f"PASS: Enabled HRR back on {adapter.name}")

            break

    ##
    # @brief        VRR verification in WINDOWED mode with HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VRR"], critical=False)
    # @endcond
    def t_13_vrr(self):
        if self.validate_vrr() is False:
            self.fail("FAIL : Basic Test : VRR verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BfrVrrDmrrs))
    TestEnvironment.cleanup(test_result)
