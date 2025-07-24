########################################################################################################################
# @file         test_functional_basic.py
# @brief        Contains basic functional tests covering below scenarios:
#               * VRR verification in WINDOWED and FULL SCREEN modes with NO_LOW_HIGH_FPS/LOW_FPS/HIGH_FPS/LOW_HIGH_FPS
#               settings.
#               * All tests will be executed on VRR panel with VRR enabled. VRR is expected to be working in all above
#               scenarios.
#
# @author       Rohit Kumar
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VRR.vrr_base import *


##
# @brief        This class contains basic VRR tests for different modes and FPS settings.
#               This class inherits the VrrBase class.
class TestFunctionalBasic(VrrBase):

    ##
    # @brief        This class method is the entry point for test cases of basic functional check.
    #               Helps to initialize some parameters required for testing display vrr feature.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(TestFunctionalBasic, cls).setUpClass()
        # VRR is not expected to work if active RR is not in range of VRR range.
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                # filtering RR list with in MRL range. as if RR out of MRL range , VRR will not work.
                rr_list = [rr for rr in panel.rr_list if rr in range(panel.vrr_caps.vrr_min_rr,
                                                                     panel.vrr_caps.vrr_max_rr + 1)]
                if rr_list is None:
                    assert rr_list, "No RR support in MRL range of panel"

                # Skipping mode set if current refresh rate is within panel's VRR MIN-VRR MAX range
                current_mode = cls.display_config_.get_current_mode(panel.target_id)
                if current_mode.refreshRate not in range(panel.vrr_caps.vrr_min_rr,
                                                                     panel.vrr_caps.vrr_max_rr):
                    apply_mode = common.get_display_mode(panel.target_id, rr_list[-1])
                    if not cls.display_config_.set_display_mode([apply_mode], False):
                        logging.error(f"Failed to apply display mode "
                                      f"{apply_mode.HzRes}x{apply_mode.VtRes}@ {apply_mode.refreshRate}")
                    logging.info(f"Applying mode: {apply_mode.HzRes}x{apply_mode.VtRes}@ {apply_mode.refreshRate}")


    ############################
    # Test Function
    ############################

    ##
    # @brief        VRR verification in WINDOWED mode with NO_LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_11_windowed(self):
        if self.verify_vrr(False) is False:
            self.fail("VRR verification failed in WINDOWED mode with NO_LOW_HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in WINDOWED mode")

    ##
    # @brief        VRR verification in FULL_SCREEN mode with NO_LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_12_full_screen(self):
        if self.verify_vrr(True) is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with NO_LOW_HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in FULL_SCREEN mode")

    ##
    # @brief        VRR verification in WINDOWED mode with LOW_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "LOW_FPS"])
    # @endcond
    def t_21_windowed(self):
        if self.verify_vrr(False) is False:
            self.fail("VRR verification failed in WINDOWED mode with LOW_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in WINDOWED mode")

    ##
    # @brief        VRR verification in FULL_SCREEN mode with LOW_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "LOW_FPS"])
    # @endcond
    def t_22_full_screen(self):
        if self.verify_vrr(True) is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in FULL_SCREEN mode")

    ##
    # @brief        VRR verification in WINDOWED mode with HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "HIGH_FPS"])
    # @endcond
    def t_31_windowed(self):
        if self.verify_vrr(False) is False:
            self.fail("VRR verification failed in WINDOWED mode with HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in WINDOWED mode")

    ##
    # @brief        VRR verification in FULL_SCREEN mode with HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "HIGH_FPS"])
    # @endcond
    def t_32_full_screen(self):
        if self.verify_vrr(True) is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in FULL_SCREEN mode")

    ##
    # @brief        VRR verification in WINDOWED mode with LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "LOW_HIGH_FPS"])
    # @endcond
    def t_41_windowed(self):
        if self.verify_vrr(False) is False:
            self.fail("VRR verification failed in WINDOWED mode with LOW_HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in WINDOWED mode")

    ##
    # @brief        VRR verification in FULL_SCREEN mode with LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "LOW_HIGH_FPS"])
    # @endcond
    def t_42_full_screen(self):
        if self.verify_vrr(True) is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in FULL_SCREEN mode")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestFunctionalBasic))
    TestEnvironment.cleanup(test_result)
