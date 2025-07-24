########################################################################################################################
# @file         bfr_mode_enumeration.py
# @brief        Contains tests for BFR and concurrency of other RR features in dynamic RR mode
# @details      Basic functional tests are covering below scenarios:
#               * Check all modes sent by driver to OS
#               * Check if virtualRRsupport is reported along with mode
#
# @author       Gopikrishnan R
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.BFR.bfr_base import *
from Tests.PowerCons.Functional.DMRRS import hrr


##
# @brief        This class contains BFR basic test that verifies the modes enumerated has virtual RR support
#               This class inherits the BfrBase class.
class BfrModeEnumeration(BfrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        BFR basic test that verifies virtual RR support in the enumerated modes
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MODE_ENUMERATION"], critical=False)
    # @endcond
    def t_11_bfr_mode_enumeration(self):
        for adapter in dut.adapters.values():
            hrr.enable(adapter)
            dut.refresh_panel_caps(adapter)
            if not adapter.is_vrr_supported:
                continue
            for panel in adapter.panels.values():
                if panel.bfr_caps.is_bfr_supported:
                    if not bfr.check_bfr_mode_enumeration(adapter, panel):
                        self.fail("Check for Modes with VirtualRR support in the enumerated modes failed")

    ##
    # @brief        BFR basic test that verifies virtual RR support in the enumerated modes in negative scenarios
    #               Should be used only for panels where BFR caps is expected to be disabled
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["NEGATIVE_MODE_ENUMERATION"], critical=False)
    # @endcond
    def t_11_bfr_negative_mode_enumeration(self):
        for adapter in dut.adapters.values():
            if not adapter.is_vrr_supported:
                continue
            for panel in adapter.panels.values():
                if not bfr.check_bfr_mode_enumeration(adapter, panel, True):
                    self.fail("Modes with VirtualRR support was not expected")

    ##
    # @brief        unittest tearDown function
    # @return       None
    def tearDown(self):
        for adapter in dut.adapters.values():
            hrr_status = hrr.disable(adapter)
            dut.refresh_panel_caps(adapter)
            if hrr_status is False:
                self.fail(f"Failed to disable HRR on {adapter.name}")
            if hrr_status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail("\tFAILED to restart display driver after reg-key update")
        super(BfrModeEnumeration, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BfrModeEnumeration))
    TestEnvironment.cleanup(test_result)
