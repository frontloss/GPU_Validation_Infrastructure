#################################################################################################################
# @file         drrs_negative.py
# @addtogroup   PowerCons
# @section      DRRS_Tests
# @brief        Contains DRRS negative tests
#
# @author       Rohit Kumar
#################################################################################################################

from Libs.Core import etl_parser
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DRRS.drrs_base import *
from Tests.PowerCons.Modules import workload
from Tests.VRR import vrr


##
# @brief        This class contains negative tests to verify DRRS
class DrrsNegativeTest(DrrsBase):
    display_config_ = display_config.DisplayConfiguration()

    ##
    # @brief        This function checks if RR changes on DRRS unsupported panels
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MIN_RR"])
    # @endcond
    def t_11_min_rr(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                mode = common.get_display_mode(panel.target_id, panel.min_rr)
                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("Failed to set display mode")
                html.step_end()

            dut.refresh_panel_caps(adapter)

        etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.drrs_caps.is_drrs_supported is False:
                    continue

                logging.info("Step: Verifying RR changes for {0}".format(panel.port))
                rr_change_status = drrs.is_rr_changing(adapter, panel, etl_file)
                if rr_change_status is None:
                    logging.error("\tETL report generation FAILED")
                    status = False
                elif rr_change_status is False:
                    logging.info("\tPASS: Active refresh rate is not changing during workload")
                else:
                    gdhm.report_driver_bug_os("[OsFeatures][DRRS] Refresh rate is changing in Min RR")
                    logging.error("\tFAIL: RR change detected with minimum RR")
                    status = False

        if status is False:
            self.fail("DRRS negative verification failed with min RR")

    ##
    # @brief        This function contains DRRS negative verification with video playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO"])
    # @endcond
    def t_12_video(self):
        etl_file, _ = workload.run(workload.VIDEO_PLAYBACK, [24, 30, False, True])

        if etl_parser.generate_report(etl_file, drrs.ETL_PARSER_CONFIG) is False:
            self.fail("Failed to generate ETL report")

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.drrs_caps.is_drrs_supported is False:
                    continue

                logging.info("Step: Verifying VBI during a video playback for {0}".format(panel.port))
                interrupt_data = etl_parser.get_interrupt_data(
                    etl_parser.Ddi.DDI_CONTROLINTERRUPT2, etl_parser.InterruptType.CRTC_VSYNC)
                if interrupt_data is None:
                    logging.info("\tPASS: VBI is not getting disabled during video playback")
                    continue

                for interrupt in interrupt_data:
                    if interrupt.CrtVsyncState in [etl_parser.CrtcVsyncState.ENABLE,
                                                   etl_parser.CrtcVsyncState.DISABLE_KEEP_PHASE]:
                        continue

                    logging.error(
                        "\tFAIL: VBI_DISABLE interrupt found during video playback {0}".format(interrupt.TimeStamp))
                    status = False

        if status is False:
            self.fail("DRRS negative verification failed with video playback")

    ##
    # @brief        This function checks DRRS behavior after DISABLE_GAMING_VRR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DISABLE_GAMING_VRR"])
    # @endcond
    def t_13_disable_gaming_vrr(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if (panel.vrr_caps.is_vrr_supported and panel.drrs_caps.is_drrs_supported) is False:
                    self.fail("FAILED: Panel does not support VRR/DRRS (Planning Issue)")
                if not panel.is_lfp:
                    continue
                if vrr.disable(adapter) is False:
                    self.fail("FAILED to disable Gaming VRR using Escape call")
                logging.info("Successfully disabled Gaming VRR")
        try:
            etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
            if etl_file is None:
                self.fail("FAILED to run the workload")
            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    logging.info(f"Step: Verifying DRRS after disabling Gaming VRR for {panel.port}")
                    if not panel.is_lfp:
                        continue
                    if drrs.verify(adapter, panel, etl_file) is False:
                        self.fail("DRRS is Functional after disabling Gaming VRR")
                    logging.info("DRRS is not Functional after disabling Gaming VRR")
        except Exception as e:
            self.fail(e)
        finally:
            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    if not panel.is_lfp:
                        continue
                    if vrr.enable(adapter) is False:
                        self.fail("FAILED to enable Gaming VRR")
                    logging.info("Successfully enabled Gaming VRR")

    ##
    # @brief        DRRS Negative test for 314h source based VTotal DPCD value not present
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["NO_SOURCE_BASED_VTOTAL_DPCD"])
    # @endcond
    def t_14_no_drrs_dpcd(self):
        # Enabling PSR to make sure DRRS is not working.
        for adapter in dut.adapters.values():
            if psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1):
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail(f"Failed to restart display driver for {adapter.name}")
                logging.info(f"\tSuccessfully restarted display driver for {adapter.name} after enabling PSR")
            dut.refresh_panel_caps(adapter)

        etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info(f"\t{panel.drrs_caps}")
                
                logging.info("Step: Verifying if RR changes for {0}".format(panel.port))
                if drrs.is_rr_changing(adapter, panel, etl_file):
                    gdhm.report_driver_bug_os("[OsFeatures][DRRS] Refresh rate is changing with DRRS unsupported panel")
                    logging.error("\tFAIL: RR change detected with DRRS unsupported panel")
                    self.fail("\tFAIL: RR change detected with DRRS unsupported panel")
                logging.info("\tPASS: Refresh rate is not changing during workload with DRRS unsupported panel")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DrrsNegativeTest))
    test_environment.TestEnvironment.cleanup(test_result)
