########################################################################################################################
# @file         vrr_workload.py
# @brief        Contains workload tests for VRR
#
# @author       Rohit Kumar
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VRR.vrr_base import *


##
# @brief        This class contains different workload tests . This class inherits the VrrBase class.
class TestWorkload(VrrBase):

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for workload test cases. Helps to initialize some of
    #               the parameters required for testing different workloads.
    # @return       None
    @classmethod
    def setUpClass(cls):
        # VRR Workload tests are only meant for 19H1+ OS
        if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_19H1:
            assert False, "VRR Workload tests are only meant for 19H1+ OS(Planning Issue)"

        super(TestWorkload, cls).setUpClass()

        # Workload tests are only applicable for Classic3DCube app
        cls.app = workload.Apps.Classic3DCubeApp

    ############################
    # Test Functions
    ############################

    ##
    # @brief        Test function to verify VRR when drawing text over active async flip window
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["TEXT_OVERLAY"])
    # @endcond
    def t_41_text_over_game(self):
        app_config = workload.Classic3DCubeAppConfig()
        app_config.gdi_compatible = True
        if self.verify_vrr(True, app_config=app_config, vmax_flipline_foreachflip=False) is False:
            self.fail("VRR text overlay test failed")
        logging.info("\tPASS: VRR verification passed successfully")

    ##
    # @brief        Test function to verify VRR when Changing flip present interval
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["INTERVAL"])
    # @endcond
    def t_42_interval(self):
        for interval in [2, 3, 4, 5]:
            app_config = workload.Classic3DCubeAppConfig()
            app_config.interval = interval
            if self.verify_vrr(True, app_config=app_config) is False:
                self.fail("VRR verification failed for interval= {0}".format(interval))
            logging.info("\tPASS: VRR verification passed successfully")

    ##
    # @brief        Test function to verify VRR while Opening and closing game window multiple times in a very
    #               short period of time
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOW_CLOSE"])
    # @endcond
    def t_43_window_close(self):
        app_config = workload.Classic3DCubeAppConfig()
        app_config.test_window_device_destruction = True
        if self.verify_vrr(True, app_config=app_config) is False:
            self.fail("VRR window device destruction test failed")
        logging.info("\tPASS: VRR verification passed successfully")

    ##
    # @brief        Test function to verify VRR by Switching between full screen and windowed mode multiple times
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN_SWITCH"])
    # @endcond
    def t_44_full_screen_switch(self):
        app_config = workload.Classic3DCubeAppConfig()
        app_config.test_full_screen = True
        if self.verify_vrr(True, app_config=app_config) is False:
            self.fail("VRR full screen switch test failed")
        logging.info("\tPASS: VRR verification passed successfully")

    ##
    # @brief        Test function to verify VRR by Opening multiple game windows at the same time
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MULTI_WINDOW"])
    # @endcond
    def t_45_multi_window(self):
        app_config = workload.Classic3DCubeAppConfig()
        app_config.window_count = 2
        if self.verify_vrr(True, app_config=app_config, vmax_flipline_foreachflip=False) is False:
            self.fail("VRR multi window test failed")
        logging.info("\tPASS: VRR verification passed successfully")

    ##
    # @brief        VmaxReached bit verification in VRRStatus in LOW_HIGH_FPS with FPS > maxRR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FPS_OUTSIDE_RR_RANGE", "FPS_MORE_THAN_MAX_RR"])
    # @endcond
    def t_46_fps_more_than_maxRR(self):
        self.app = workload.Apps.FlipAt
        app_config = workload.FlipAtAppConfig()
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in [panel for panel in adapter.panels.values() if
                          panel.vrr_caps.is_vrr_supported and panel.is_active]:
                app_config.pattern_1 = app_config.pattern_2 = vrr.get_fps_pattern(panel.max_rr)
                if self.verify_vrr(True, app_config=app_config) is False:
                    self.fail("VRR verification failed in FPS more than MaxRR mode with LOW_HIGH_FPS setting")
                logging.info("\tPASS: VRR verification passed successfully")
                if not vrr.check_vrr_status_vmax_reached(adapter, panel, flag_set_expected=False):
                    self.fail("FAIL: VmaxReached bit set was not expected with fps more than maxRR")
                logging.info("PASS: VmaxReached bit was set to 0 as expected")

    ##
    # @brief        VmaxReached bit verification in VRRStatus in LOW_HIGH_FPS with FPS < minRR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FPS_OUTSIDE_RR_RANGE", "FPS_LESS_THAN_MIN_RR"])
    # @endcond
    def t_47_fps_less_than_minRR(self):
        self.app = workload.Apps.FlipAt
        app_config = workload.FlipAtAppConfig()
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in [panel for panel in adapter.panels.values() if panel.vrr_caps.is_vrr_supported]:
                app_config.pattern_1 = app_config.pattern_2 = vrr.get_fps_pattern(panel.min_rr, False)
                if self.verify_vrr(True, app_config=app_config) is False:
                    self.fail("VRR verification failed in FPS less than MinRR mode with LOW_HIGH_FPS setting")
                logging.info("\tPASS: VRR verification passed successfully")
                if not vrr.check_vrr_status_vmax_reached(adapter, panel, flag_set_expected=True):
                    self.fail("FAIL: VmaxReached bit set was expected with fps less than minRR")
                logging.info("PASS: VmaxReached bit was set to 1 as expected")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestWorkload))
    TestEnvironment.cleanup(test_result)
