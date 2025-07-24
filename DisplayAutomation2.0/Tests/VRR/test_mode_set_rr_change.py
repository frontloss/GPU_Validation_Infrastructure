########################################################################################################################
# @file         test_mode_set_rr_change.py
# @brief        Contains modeset and RR change functional tests for VRR
# @details      Modeset functional tests are covering below scenarios:
#               * VRR verification in Windowed and Fullscreen modes with LOW_HIGH_FPS settings.
#               * All tests will be executed on VRR panel with VRR enabled. VRR is expected to be working in all above
#               scenarios.
#               * Cover Mode set and RR change during Workload running
#
# @author       Nainesh Doriwala
########################################################################################################################
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.test_env import test_context
from Tests.VRR.vrr_base import *


##
# @brief        This class contains Display modes functional tests. This class inherits the VrrBase class.
#               Tests verify VRR in WINDOWED and FULL_SCREEN mode with different FPS settings in different display
#               modes.
class TestModesetRRChange(VrrBase):
    display_mode_list = []

    ##
    # @brief        This class method is the entry point for test cases with different functional display modes.
    #               Helps to initialize some of the parameters required for testing display under different modes.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(TestModesetRRChange, cls).setUpClass()
        # VRR is not expected to work if active RR is equals to min RR. So, avoid applying min RR for positive test
        # cases.
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                if len(panel.rr_list) > 2:
                    logging.info("More than 2 RR supported on this panel")
                    cls.display_mode_list = common.get_display_mode(panel.target_id, panel.rr_list[-2], limit=2)
                    cls.display_mode_list.append(common.get_display_mode(panel.target_id, panel.rr_list[-1]))
                else:
                    logging.info("less than or equal to 2 RR supported on this panel")
                    cls.display_mode_list = common.get_display_mode(panel.target_id, panel.max_rr, limit=2)

    ############################
    # Test Function
    ############################

    ##
    # @brief        VRR verification in WINDOWED mode with LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED", "LOW_HIGH_FPS"])
    # @endcond
    def t_41_modeset_windowed(self):
        if self.verify_vrr_display_mode(False) is False:
            self.fail("VRR verification failed in WINDOWED mode with LOW_HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in WINDOWED mode")

    ##
    # @brief        VRR verification in Full Screen mode with LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "LOW_HIGH_FPS"])
    # @endcond
    def t_42_modeset_full_screen(self):
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
                mode = self.display_mode_list[0]
                # Step 1 - Apply Max Mode with max RR and verify VRR for modeset.

                # Stop ETL
                if etl_tracer.stop_etl_tracer() is False:
                    self.fail("Failed to stop ETL Tracer")
                if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
                    etl_file_path = os.path.join(
                        test_context.LOG_FOLDER, 'GfxTraceBeforeModeSet.' + str(time.time()) + '.etl')
                    os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

                # Start New ETL
                if etl_tracer.start_etl_tracer() is False:
                    self.fail("Failed to start ETL Tracer")
                # Apply Mode
                logging.info("Applying mode: {}x{} @ {}".format(mode.HzRes, mode.VtRes, mode.refreshRate))
                if self.display_config_.set_display_mode([self.display_mode_list[0]], False) is False:
                    self.fail("Failed to apply display mode")
                logging.info("\tSuccessfully applied the display mode")

                # Stop ETL and verify Modeset VRR programming.
                if etl_tracer.stop_etl_tracer() is False:
                    self.fail("Failed to stop ETL Tracer")
                if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
                    etl_file_path = os.path.join(
                        test_context.LOG_FOLDER, 'GfxTraceDuringModeSet.' + str(time.time()) + '.etl')
                    os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
                # verify VRR programming during modeset time.
                status &= self.verify_vrr_during_modeset(etl_file_path)

                # step 2 - Start workload -> Apply Different mode with same RR -> close workload -> verify vrr
                # Step 3 - Start workload -> Apply Different mode with different RR -> close workload -> verify vrr
                for index in range(1, len(self.display_mode_list)):
                    # Run workload and don't close workload
                    status, _ = workload.run(workload.GAME_PLAYBACK_WITH_CUSTOM_EVENTS,
                                             [self.app, self.duration, full_screen, False, True, None])
                    if not status:
                        gdhm.report_bug(
                            title="[OS Features][VRR] Failed to run gaming workload",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E3
                        )
                        self.fail("[OS Features][VRR] Failed to run gaming workload")
                    # Stop ETL
                    if etl_tracer.stop_etl_tracer() is False:
                        self.fail("Failed to stop ETL Tracer")
                    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
                        etl_file_path = os.path.join(
                            test_context.LOG_FOLDER, 'GfxTraceBeforeModeSet.' + str(time.time()) + '.etl')
                        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
                    # Start New ETL
                    if etl_tracer.start_etl_tracer() is False:
                        self.fail("Failed to start ETL Tracer")
                    # Change Resolution and not RR.
                    mode = self.display_mode_list[index]
                    logging.info("Applying mode: {}x{} @ {}".format(mode.HzRes, mode.VtRes, mode.refreshRate))
                    if self.display_config_.set_display_mode([self.display_mode_list[1]], False) is False:
                        self.fail("Failed to apply display mode")
                    logging.info("\tSuccessfully applied the display mode")
                    # wait for 20sec after modeset so workload can run with Latest mode
                    time.sleep(20)

                    # Close Running classic3d Application
                    status, etl_file = workload.run(workload.GAME_PLAYBACK_WITH_CUSTOM_EVENTS,
                                                    [self.app, self.duration, full_screen, True, False, None])

                    if not status or etl_file is None:
                        gdhm.report_bug(
                            title="[OS Features][VRR]Failed to close gaming workload or fail to generate etl file",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E3
                        )
                        self.fail("[OS Features][VRR]Failed to close gaming workload or fail to generate etl file")

                    # verify vrr for panel
                    is_os_aware_vrr = dut.WIN_OS_VERSION >= dut.WinOsVersion.WIN_19H1
                    expected_vrr = True if panel.vrr_caps.is_vrr_supported else False
                    negative = False if panel.vrr_caps.is_vrr_supported else True
                    if display_config.is_display_active(panel.port, panel.gfx_index) is False:
                        self.fail(f"Requested panel {panel.port} is not active")
                    status &= vrr.verify(adapter, panel, etl_file, None, negative, is_os_aware_vrr, expected_vrr,
                                         True)
        return status


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestModesetRRChange))
    TestEnvironment.cleanup(test_result)
