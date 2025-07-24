#######################################################################################################################
# @file         dmrrs_negative.py
# @addtogroup   PowerCons
# @section      DMRRS_Tests
# @brief        Contains DMRRS negative tests
#
# @author       Ashish Tripathi, Vinod
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DMRRS.dmrrs import VIDEO_FPS_MAPPING
from Tests.PowerCons.Functional.DMRRS.dmrrs_base import *
from Tests.PowerCons.Modules import workload
from Tests.VRR import vrr

##
# @brief        This class contains negative tests to verify DMRRS


class DmrrsNegativeTest(DmrrsBase):
    display_config_ = display_config.DisplayConfiguration()

    ##
    # @brief        This function checks DMRRS behavior with MIN RR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MIN_RR"])
    # @endcond
    def t_11_min_rr(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                html.step_start(f"Switching to {panel.min_rr} Hz(Min RR) for {panel.port}", True)
                mode = common.get_display_mode(panel.target_id, panel.min_rr)
                logging.info(f"\tApplying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("\tSuccessfully applied display mode")

            dut.refresh_panel_caps(adapter)
            html.step_end()

        etl_file, _ = workload.run(
            workload.VIDEO_PLAYBACK_USING_FILE, [self.video_file, self.duration_in_seconds, False])

        if etl_file is False:
            self.fail("FAILED to run the workload")

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.drrs_caps.is_dmrrs_supported is False:
                    continue
                status = dmrrs.verify_dmrrs_with_min_rr(adapter, panel, etl_file)

        # set to default max-rr post test completion
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                mode = common.get_display_mode(panel.target_id, panel.max_rr)
                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("\tSuccessfully applied display mode")
                html.step_end()

            dut.refresh_panel_caps(adapter)

        if status is False:
            self.fail("DMRRS negative verification failed with Min RR")
        logging.info("DMRRS negative verification passed with Min RR")

    ##
    # @brief        Test function to verify DMRRS negative
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["NO_MRL"])
    # @endcond
    def t_12_no_mrl(self):
        etl_file, _ = workload.run(
            workload.VIDEO_PLAYBACK_USING_FILE, [self.video_file, self.duration_in_seconds, False])

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    status = True
                    logging.info(f"Step: Verifying No Non-Zero duration is present for {panel.port}")
                    if dmrrs.is_non_zero_duration_flip_present(panel, etl_file):
                        logging.error(f"Non-zero duration flip present with Min RR for {panel.port}")
                        status = False
                    else:
                        logging.info(f"Non-zero duration flip is NOT present with Min RR for {panel.port}")

                    logging.info(f"Step: Verifying No RR change happened for {panel.port}")
                    rr_change_status = drrs.is_rr_changing(adapter, panel, etl_file)
                    if rr_change_status is None:
                        logging.error("\tETL report generation FAILED")
                        status = False
                    elif rr_change_status is False:
                        logging.info("\tRefresh rate is NOT changing during workload")
                    else:
                        logging.error("\tRefresh rate is changing during workload")
                        status = False

                    if status is False:
                        self.fail("DMRRS negative verification failed with No MRL")
                    logging.info("DMRRS negative verification passed with No MRL")
                else:
                    self.dmrrs_hrr_verification(adapter, panel, etl_file, dmrrs.VIDEO_FPS_MAPPING[self.video_file])

    ##
    # @brief        This function checks DMRRS behavior after DISABLE_GAMING_VRR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DISABLE_GAMING_VRR"])
    # @endcond
    def t_13_disable_gaming_vrr(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if (panel.vrr_caps.is_vrr_supported and panel.drrs_caps.is_dmrrs_supported) is False:
                    self.fail("FAILED: Panel does not support VRR/DMRRS {Planning Issue}")
                if vrr.disable(adapter) is False:
                    self.fail("FAILED to disable Gaming VRR using Escape call")
                logging.info("Successfully disabled Gaming VRR")
        try:
            etl_file, _ = workload.run(
                workload.VIDEO_PLAYBACK_USING_FILE, [self.video_file, self.duration_in_seconds, False])
            if etl_file is None:
                self.fail("FAILED to run the workload")
            media_fps = VIDEO_FPS_MAPPING[self.video_file]
            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    logging.info(f"Step: Verifying DMRRS after disabling Gaming VRR for {panel.port}")
                    if dmrrs.verify(adapter, panel, etl_file, media_fps) is False:
                        self.fail("DMRRS is not Functional after disabling Gaming VRR")
                    logging.info("DMRRS is Functional after disabling Gaming VRR")
        except Exception as e:
            self.fail(e)
        finally:
            for adapter in dut.adapters.values():
                if vrr.enable(adapter) is False:
                    self.fail("FAILED to enable Gaming VRR")
                logging.info("Successfully enabled Gaming VRR")

    ##
    # @brief        This function checks if DMRRS is disabled with MTK panels
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["NO_VRR_MTK"])
    # @endcond
    def t_14_no_dmrrs(self):
        # DMRRS is expected not to work with VRR MTK panels
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                etl_file, _ = workload.run(workload.VIDEO_PLAYBACK,
                                                [dmrrs.MediaFps.FPS_24_000, 30, False, False, None, None, True])
                if etl_file is None:
                    self.fail("FAILED to run the workload")
                if dmrrs.is_dmrrs_changing_rr(adapter, panel, etl_file, dmrrs.MediaFps.FPS_24_000):
                    self.fail(f"FAIL: Refresh rate change is seen when DMRRS is disabled")
                logging.info("\tPASS: No Refresh Rate change detected when DMRRS is disabled")

    ##
    # @brief        DMRRS Negative test for 314h source based VTotal DPCD value not present
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["NO_SOURCE_BASED_VTOTAL_DPCD"])
    # @endcond
    def t_15_no_dmrrs_dpcd(self):
        # DMRRS is expected not to work with panels of 314h Bit2 is not set
        # Enabling PSR to make sure DRRS is not working.
        for adapter in dut.adapters.values():
            if psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1):
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail(f"Failed to restart display driver for {adapter.name}")
                logging.info(f"\tSuccessfully restarted display driver for {adapter.name} after enabling PSR")
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                logging.info(f"\t{panel.drrs_caps}")
                etl_file, _ = workload.run(workload.VIDEO_PLAYBACK,
                                                [dmrrs.MediaFps.FPS_24_000, 30, False, False, None, None, True])
                if etl_file is None:
                    self.fail("FAILED to run the workload")
                if dmrrs.is_dmrrs_changing_rr(adapter, panel, etl_file, dmrrs.MediaFps.FPS_24_000):
                    self.fail(f"FAIL: Refresh rate change is seen when DMRRS is not supported")
                logging.info("\tPASS: No Refresh Rate change detected when DMRRS is not supported")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DmrrsNegativeTest))
    test_environment.TestEnvironment.cleanup(test_result)
