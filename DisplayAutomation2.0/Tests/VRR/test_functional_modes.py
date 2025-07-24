########################################################################################################################
# @file         test_functional_modes.py
# @brief        Contains display modes functional tests for VRR
# @details      Display modes functional tests are covering below scenarios:
#               * VRR verification in WINDOWED and FULL SCREEN modes with NO_LOW_HIGH_FPS/LOW_FPS/HIGH_FPS/LOW_HIGH_FPS
#               settings in multiple display modes.
#               * All tests will be executed on VRR panel with VRR enabled. VRR is expected to be working in all above
#               scenarios.
#
# @author       Rohit Kumar
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.test_env import test_context
from Tests.VRR.vrr_base import *


##
# @brief        This class contains Display modes functional tests. This class inherits the VrrBase class.
#               Tests verify VRR in WINDOWED and FULL_SCREEN mode with different FPS settings in different display
#               modes.
class TestFunctionalModes(VrrBase):
    display_mode_list = []

    ##
    # @brief        This class method is the entry point for test cases with different functional display modes.
    #               Helps to initialize some of the parameters required for testing display under different modes.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(TestFunctionalModes, cls).setUpClass()
        # VRR is not expected to work if active RR is equals to min RR. So, avoid applying min RR for positive test
        # cases.
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                if len(panel.rr_list) > 2:
                    # filtering RR list with in MRL range. as if RR out of MRL range , VRR will not work.
                    rr_list = [rr for rr in panel.rr_list if rr in range(panel.vrr_caps.vrr_min_rr,
                                                                         panel.vrr_caps.vrr_max_rr + 1)]
                    cls.display_mode_list.append(common.get_display_mode(panel.target_id, rr_list[-2]))
                    cls.display_mode_list.append(common.get_display_mode(panel.target_id, rr_list[-1]))
                else:
                    cls.display_mode_list = common.get_display_mode(panel.target_id, panel.max_rr, limit=2)

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
        if self.verify_vrr_display_mode(False) is False:
            self.fail("VRR verification failed in WINDOWED mode with NO_LOW_HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in WINDOWED mode")

    ##
    # @brief        VRR verification in FULL_SCREEN mode with NO_LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "NO_LOW_HIGH_FPS"])
    # @endcond
    def t_12_full_screen(self):
        if self.verify_vrr_display_mode(True) is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with NO_LOW_HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in FULL_SCREEN mode")

    ##
    # @brief        VRR verification in WINDOWED mode with LOW_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "LOW_FPS"])
    # @endcond
    def t_21_windowed(self):
        if self.verify_vrr_display_mode(False) is False:
            self.fail("VRR verification failed in WINDOWED mode with LOW_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in WINDOWED mode")

    ##
    # @brief        VRR verification in FULL_SCREEN mode with LOW_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "LOW_FPS"])
    # @endcond
    def t_22_full_screen(self):
        if self.verify_vrr_display_mode(True) is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in FULL_SCREEN mode")

    ##
    # @brief        VRR verification in WINDOWED mode with HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "HIGH_FPS"])
    # @endcond
    def t_31_windowed(self):
        if self.verify_vrr_display_mode(False) is False:
            self.fail("VRR verification failed in WINDOWED mode with HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in WINDOWED mode")

    ##
    # @brief        VRR verification in FULL_SCREEN mode with HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "HIGH_FPS"])
    # @endcond
    def t_32_full_screen(self):
        if self.verify_vrr_display_mode(True) is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in FULL_SCREEN mode")

    ##
    # @brief        VRR verification in WINDOWED mode with LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "LOW_HIGH_FPS"])
    # @endcond
    def t_41_windowed(self):
        if self.verify_vrr_display_mode(False) is False:
            self.fail("VRR verification failed in WINDOWED mode with LOW_HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in WINDOWED mode")

    ##
    # @brief        VRR verification in FULL_SCREEN mode with LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "LOW_HIGH_FPS"])
    # @endcond
    def t_42_full_screen(self):
        if self.verify_vrr_display_mode(True) is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in FULL_SCREEN mode")

    ############################
    # Helper Functions
    ############################

    ##
    # @brief        This is a helper function used to apply a display mode and verify vrr
    # @param[in]    full_screen indicates if the video should be in full screen mode or not
    # @return       None
    def verify_vrr_display_mode(self, full_screen):
        status = True
        etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                for mode in self.display_mode_list:
                    current_mode = self.display_config_.get_current_mode(panel.target_id)
                    if current_mode == mode:
                        continue
                    etl_tracer.stop_etl_tracer()
                    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
                        etl_file_path = os.path.join(
                            test_context.LOG_FOLDER, 'GfxTraceBeforeModeSet.' + str(time.time()) + '.etl')
                        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

                    if etl_tracer.start_etl_tracer() is False:
                        logging.error("Failed to start ETL Tracer")
                        return False
                    logging.info("Applying mode: {}x{} @ {}".format(mode.HzRes, mode.VtRes, mode.refreshRate))
                    assert self.display_config_.set_display_mode([mode], False), "Failed to apply display mode"
                    logging.info("\tSuccessfully applied the display mode")
                    etl_tracer.stop_etl_tracer()
                    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
                        etl_file_path = os.path.join(
                            test_context.LOG_FOLDER, 'GfxTraceDuringModeSet.' + str(time.time()) + '.etl')
                        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
                    # refreshing panel caps after modeset.
                    dut.refresh_panel_caps(adapter=adapter)
                    logging.info("\t\t{0}".format(panel.pipe_joiner_tiled_caps))
                    status &= self.verify_vrr_during_modeset(etl_file_path)
                    if etl_tracer.start_etl_tracer() is False:
                        logging.error("Failed to start ETL Tracer")
                        return False
                    status &= self.verify_vrr(full_screen)

        return status


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestFunctionalModes))
    TestEnvironment.cleanup(test_result)
