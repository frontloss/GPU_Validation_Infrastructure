#######################################################################################################################
# @file             psr_hotplug_unplug.py
# @brief            PSR Tests with hot plug/unplug
# @details          This file contains tests for following scenarios
#                   * Test for verifying PSR with hotplug & unplug external display
#                   * Test to unplug external display during FullScreen VPB and verify PSR2
#
# @author           Chandrakanth Reddy
#######################################################################################################################

from Libs.Core import display_utility, app_controls
from Libs.Core.test_env import test_environment
from Libs.Core.logger import html
from Tests.PowerCons.Functional.PSR.psr_base import *
from Tests.PowerCons.Modules import workload


##
# @brief        This class contains tests to verify PSR with hotplug and unplug of external display. This class inherits
#               PsrBase class
class HotplugUnplug(PsrBase):
    ##
    # @brief        This function verifies PSR2 verification after hotplug unplug of display after  basic checks
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_hot_plug_unplug(self):
        if self.cmd_line_param[0]['SELECTIVE'] != 'NONE':
            return
        if self.feature < psr.UserRequestedFeature.PSR_2:
            self.fail("Invalid feature name passed in cmd-line. Expected = PSR2/PR Actual = {}".format(self.feature_str))
        for adapter in dut.adapters.values():
            lfp_panels = []
            ext_panels = []
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    ext_panels.append(panel.port)
                    continue
                if panel.psr_caps.is_psr_supported is False and (panel.is_lfp and panel.pr_caps.is_pr_supported is False):
                    continue
                lfp_panels.append(panel)
            assert lfp_panels, "PSR2/PR supported panel is not connected"
            # unplug the external panel
            if len(ext_panels):
                for ext_panel in ext_panels:
                    logging.info("Step:unplug display {}".format(ext_panel))
                    if display_utility.unplug(ext_panel) is False:
                        self.fail("Failed to unplug display {}".format(ext_panel))
                    logging.info("Pass:{} display unplug success".format(ext_panel))

                # verify PSR/PR with only LFP connected
                self.validate_feature()
                logging.info(f"\tPASS: {self.feature_str} verification on {lfp_panels}")

                time.sleep(30)

                # Hot plug external display during PSR deep sleep state
                for ext_panel in ext_panels:
                    logging.info("Step:plug display {}".format(ext_panel))
                    if display_utility.plug(ext_panel) is False:
                        self.fail("Failed to plug display {}".format(ext_panel))
                    logging.info("Pass:{} display plug success".format(ext_panel))
                # verify PSR with external panel connected
                self.validate_feature()
                logging.info(f"\tPASS: {self.feature_str} verification on {lfp_panels + ext_panels}")
            else:
                self.fail("At least one external display is required for Hot plug test (Command Line Issue)")


    ##
    # @brief        This function verifies PSR2 with 
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_12_unplug_during_vpb(self):
        # Test steps are as follows
        #   - Plug external display and set display mode to extended (Will be done in DUT prepare phase)
        #   - Launch video in EDP screen and switch to FullScreen
        #   - Unplug external display
        #   - Re-Plug External display
        #   - Verify PSR2 during the process
        if 'UNPLUG_DURING_VPB' not in self.cmd_line_param[0]['SELECTIVE']:
            return
        html.step_start("Verifying external monitor unplug during VPB scenario")
        ext_panels = []
        lfp_panels = []
        offsets = psr.get_polling_offsets(self.feature)
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    ext_panels.append(panel.port)
                    continue
                if panel.psr_caps.is_psr_supported is False and (panel.is_lfp and panel.pr_caps.is_pr_supported is False):
                    continue
                lfp_panels.append(panel)

        # Hiding the task-bar to make sure that there's no update on screen
        logging.info("STEP: Hiding the task-bar")
        assert window_helper.toggle_task_bar(window_helper.Visibility.HIDE), "FAILED to hide the task-bar"
        logging.info("\tSuccessfully hidden the task-bar")
        for adapter in dut.adapters.values():
            feature, feature_str = self.get_feature(adapter)
            # Start ETL tracer
            etl_status, _ = workload.etl_tracer_stop_existing_and_start_new("GfxTraceBeforeVideoPlayback")
            if not etl_status:
                self.fail("Failed to stop ETL tracer")

            # Launch video in FullScreen mode and start polling
            logging.info(f"Video playback has been started with {psr.DEFAULT_MEDIA_FPS} FPS")
            app_controls.launch_video(os.path.join(common.TEST_VIDEOS_PATH, "{0:.3f}.mp4".format(psr.DEFAULT_MEDIA_FPS)), is_full_screen=True)

            logging.info(f"\tPolling started. Delay= {psr.DEFAULT_POLLING_DELAY}, Offsets= {offsets}")
            polling.start(offsets, psr.DEFAULT_POLLING_DELAY)

            time.sleep(10)
            # Unplug and re-plug all the external panels during VPB
            for ext_panel in ext_panels:
                # Unplug external display
                if display_utility.unplug(ext_panel) is False:
                    window_helper.close_media_player()
                    logging.info("\tClosing video playback")
                    self.fail("Failed to unplug External display during VPB")
                logging.info("Successfully unplugged External Display during VPB")
                time.sleep(6)

                # Re-plug external display
                if display_utility.plug(ext_panel) is False:
                    window_helper.close_media_player()
                    logging.info("\tClosing video playback")
                    self.fail("Failed to re-plug External display during VPB")
                logging.info("Successfully Re-plugged External Display during VPB")
                time.sleep(5)

            # Stop polling, collect the polling data and Close media player
            polling_timeline, polling_time_stamps = polling.stop()
            polling_data = (polling_timeline, polling_time_stamps, None, None)
            logging.info("\tPolling stopped")

            window_helper.close_media_player()
            logging.info("\tClosing video playback")

            # Stop ETL tracer to collect ETL during the above process
            etl_status, etl_file = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuringVideoPlayback")
            if not etl_status:
                self.fail("Failed to stop ETL tracer")
            html.step_end()

            # Verify PSR/PR HW status
            if psr.verify(adapter, lfp_panels[0], feature, etl_file, polling_data, self.method,
                            self.is_pause_video_test, is_vsync_disable_expected=True) is False:
                self.fail(f"\tFAIL: {feature_str} verification when display was unplugged during VPB")
            logging.info(f"\tPASS: {feature_str} verification with Video playback")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(HotplugUnplug))
    test_environment.TestEnvironment.cleanup(test_result)
