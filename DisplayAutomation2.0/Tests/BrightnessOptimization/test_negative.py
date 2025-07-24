########################################################################################################################
# @file         test_negative.py
# @brief        Test for BRT Optimization when BacklightOptimization disabled
# @author       Simran Setia
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.BrightnessOptimization.test_base import *


##
# @brief        This class contains Brightness Optimization verification when BacklightOptimization disabled
#               This class inherits the BrtOptimizationBase class.


class TestNegative(BrtOptimizationBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        Brightness verification when BacklightOptimization disabled
    # @return       None
    # @cond
    @common.configure_test(selective=["REGKEY_DISABLE"])
    # @endcond
    def t_11_disable_tcon_backlight(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                skip_igcl_for_elp = False
                if brt.optimization_params[panel.port].feature_1.level != brt.optimization_params[panel.port].feature_2.level:
                    skip_igcl_for_elp = True

                if not brt.disable_tcon_bklt_optimization(adapter):
                    self.fail(f"FAIL: Test ended due to failed to disable BacklightOptimization")

                # driver restart after disabling TCON Backlight Optimization
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("Failed to restart display driver post RegKey disable")
                vbt.Vbt(adapter.gfx_index).reload()
                if brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                              brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_elp):
                    self.fail(f"FAIL: Brightness OPTIMIZATION feature is working when disabled from INF")
                else:
                    logging.info(f"PASS: Brightness OPTIMIZATION feature is not working when disabled from INF")
    ##
    # @brief       This method is the exit point for brightness negative test cases. This re-sets the environment
    #              changes done for execution of negative tests
    # @return       None

    @classmethod
    def tearDownClass(cls):
        super(TestNegative, cls).tearDownClass()
        logging.info(" TEARDOWN: BRIGHTNESS_DISABLE_BACKLIGHT ".center(common.MAX_LINE_WIDTH, "*"))
        for adapter in dut.adapters.values():
            if not brt.enable_tcon_bklt_optimization(adapter):
                assert False, "FAILED to enable BacklightOptimization"
            # driver restart after enabling TCON Backlight Optimization
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                assert False, "Failed to restart display driver post RegKey enable"


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestNegative))
    test_environment.TestEnvironment.cleanup(test_result)
