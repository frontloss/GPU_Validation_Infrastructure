########################################################################################################################
# @file         vrr_concurrency.py
# @brief        Contains concurrency tests for VRR
# @details      Concurrency tests are covering below scenarios:
#               * VRR and DPST should work together
#               * VRR and PSR1/PSR2 should not work together
#               * VRR and PipeJoiner
#               * VRR and Render Decompression
#               * VRR and HDR
#               * VRR and MPO
#               * VRR and FlipQ
#               * VRR and FBC
#               * VRR and HW_Rotation
#               * VRR and Gamma
#
# @author       Rohit Kumar
########################################################################################################################
import math

from DisplayRegs import get_interface
from DisplayRegs.DisplayOffsets import PsrOffsetValues
from Libs.Core import display_essential
from Libs.Core import enum, etl_parser, registry_access
from Libs.Core import winkb_helper as kb
from Libs.Core.display_power import PowerSource
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_fbc import fbc
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Core import app_controls, window_helper
from Tests.Color.Common import gamma_utility, color_constants
from Tests.Color.Common.common_utility import get_color_conversion_block
from Tests.Color.Common.gamma_utility import compare_ref_and_programmed_gamma_lut
from Tests.Color.Verification import feature_basic_verify
from Tests.Display_Decompression.Playback.decomp_verifier import is_feature_supported, get_pixel_format, \
    verify_render_decomp, INTEL_GMM_PATH, get_app_name
from Tests.Display_Port.DP_Pipe_Joiner.pipe_joiner_base import PipeJoinerBase
from Tests.PlanesUI.Common import planes_ui_verification
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Functional.FBC.fbc_base import check_fbc_support
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules.dut_context import Adapter, Panel
from Tests.VRR.vrr_base import *


##
# @brief        Exposed Class to write VRR concurrency tests. This class inherits the VrrBase class.
#               Any new concurrency test can inherit this class to use common setUp and tearDown functions.
class TestConcurrency(VrrBase):
    display_mode_list = []

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for any VRR concurrency test cases. Helps to initialize some of
    #               the parameters required for VRR the test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(TestConcurrency, cls).setUpClass()

        # Make sure DPST is enabled for DPST test
        if "dpst" in sys.argv or "DPST" in sys.argv:
            for adapter in dut.adapters.values():
                if adapter.is_vrr_supported is False:
                    continue

                logging.info("Step: Enabling DPST for {0}".format(adapter.name))
                dpst_status = dpst.enable(adapter, True)
                if dpst_status is False:
                    assert False, "FAILED to enable DPST"
                if dpst_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        assert False, "FAILED to restart the driver"
                logging.info("PASS: FeatureTestControl DPST status Expected= ENABLED, Actual= ENABLED")

            # Enable Simulated Battery
            logging.info("Step: Enabling Simulated Battery")
            if cls.display_power_.enable_disable_simulated_battery(True) is False:
                assert False, "Failed to enable Simulated Battery"
            logging.info("PASS: Expected Simulated Battery Status= ENABLED, Actual= ENABLED")

            # Set current power line status to DC
            if not cls.display_power_.set_current_powerline_status(display_power.PowerSource.DC):
                assert False, "Failed to switch power line status to DC(Test Issue)"

        # Make sure PSR1 is supported and is enabled in panel
        if "psr1" in sys.argv or "PSR1" in sys.argv:
            for adapter in dut.adapters.values():
                if adapter.is_vrr_supported is False:
                    continue

                for panel in adapter.panels.values():
                    assert panel.psr_caps.is_psr_supported, "PSR1 is NOT supported on {0}".format(panel.port)

                logging.info("Step: Enabling PSR1 for {0}".format(adapter.name))
                psr1_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                if psr1_status is False:
                    assert False, "FAILED to enable PSR1 through registry key"
                logging.info("PASS: PSR1 status Expected= ENABLED, Actual= ENABLED")
                psr2_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                if psr2_status is False:
                    assert False, "FAILED to disable PSR2 through registry key"
                logging.info("PASS: PSR2 status Expected= DISABLED, Actual= DISABLED")
                if psr1_status or psr2_status:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        assert False, "FAILED to restart the driver"

        # Make sure PSR2 is supported and is enabled in panel
        if "psr2" in sys.argv or "PSR2" in sys.argv:
            for adapter in dut.adapters.values():
                if adapter.is_vrr_supported is False:
                    continue

                for panel in adapter.panels.values():
                    assert panel.psr_caps.is_psr2_supported, "PSR2 is NOT supported on {0}".format(panel.port)

                logging.info("Step: Enabling PSR2 for {0}".format(adapter.name))
                psr2_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                if psr2_status is False:
                    assert False, "FAILED to enable PSR2 through registry key"
                logging.info("PASS: PSR2 status Expected= ENABLED, Actual= ENABLED")
                if psr2_status:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        assert False, "FAILED to restart the driver"

        # Make sure Pipe joiner is supported and is enabled in panel
        if "pipejoiner" in sys.argv or "PIPEJOINER" in sys.argv:
            for adapter in dut.adapters.values():
                if adapter.is_vrr_supported is False:
                    continue
                for panel in adapter.panels.values():
                    if len(panel.rr_list) > 1:
                        cls.display_mode_list.append(common.get_display_mode(panel.target_id, panel.rr_list[-2]))
                        cls.display_mode_list.append(common.get_display_mode(panel.target_id, panel.rr_list[-1]))
                    else:
                        cls.display_mode_list = common.get_display_mode(panel.target_id, panel.max_rr, limit=2)

        # Make sure Render Compression is supported on the platform
        if "render_compression" in sys.argv or "RENDER_COMPRESSION" in sys.argv:
            for adapter in dut.adapters.values():
                if adapter.is_vrr_supported is False:
                    continue
                logging.info("Step:Check platform support for Render Compression")
                if is_feature_supported("RENDER_DECOMP") is False:
                    assert False, "Render Decompression is not supported on {}".format(adapter.name)
                logging.info("PASS: Render Decompression is supported on {}".format(adapter.name))

        # Make sure HDR is supported in the panel
        if "hdr" in sys.argv or "HDR" in sys.argv:
            # Check Powerline status
            if cls.display_power_.set_current_powerline_status(display_power.PowerSource.AC) is False:
                assert False, "Failed to switch power line status to AC (Test Issue)"

            for adapter in dut.adapters.values():
                if adapter.is_vrr_supported is False:
                    continue
                for panel in adapter.panels.values():
                    if panel.hdr_caps.is_hdr_supported is False:
                        assert False, "Panel does not support HDR (Test Issue)"

        # Make sure FBC is supported in the panel
        if "fbc" in sys.argv or "FBC" in sys.argv:
            for adapter in dut.adapters.values():
                if adapter.is_vrr_supported is False:
                    continue
                for panel in adapter.panels.values():
                    logging.info("Step:Check platform support for FBC")
                    if check_fbc_support(adapter, panel) is False:
                        assert False, "FBC is not supported on {}".format(adapter.name)
                    logging.info("PASS: FBC  supported on {}".format(adapter.name))

    ############################
    # Test Functions
    ############################

    ##
    # @brief        Test function to check if VRR is working with DPST
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DPST"])
    # @endcond
    def t_41_dpst(self):
        status, etl_file = self.verify_vrr(True, return_etl=True)
        if status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

        # Verify DPST
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info("Step: Verifying DPST for {0}".format(panel.port))
                if dpst.verify(adapter, panel, etl_file) is False:
                    gdhm.report_bug(
                        title="DPST is not working with VRR",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("DPST is not working with VRR (Driver Issue)")
                logging.info("PASS: DPST verification with VRR passed successfully")

    ##
    # @brief        Test function to check if VRR is working with PSR1
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PSR1"])
    # @endcond
    def t_42_psr1(self):
        status, etl_file = self.verify_vrr(True, return_etl=True)
        if status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

        # Verify PSR1
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info("Step: Verifying PSR1 for {0}".format(panel.port))
                if TestConcurrency.check_psr_status(adapter, panel) is False:
                    self.fail("PSR verification failed")
        logging.info("PASS: PSR verification passed successfully")

    ##
    # @brief        Test function to check if VRR is working with PSR2
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PSR2"])
    # @endcond
    def t_43_psr2(self):
        status, etl_file = self.verify_vrr(True, return_etl=True)
        if status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

        # Verify PSR2
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info("Step: Verifying PSR2 for {0}".format(panel.port))
                if TestConcurrency.check_psr_status(adapter, panel, True) is False:
                    self.fail("PSR2 verification failed")
        logging.info("PASS: PSR2 verification passed successfully")

    ##
    # @brief        Test function to check if VRR is working with Pipe joiner
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PIPEJOINER", "LOW_HIGH_FPS"])
    # @endcond
    def t_44_pipejoiner(self):
        status = True
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                for mode in self.display_mode_list:
                    current_mode = self.display_config_.get_current_mode(panel.target_id)
                    if current_mode == mode:
                        continue
                    logging.info("Applying mode: {}x{} @ {}".format(mode.HzRes, mode.VtRes, mode.refreshRate))
                    assert self.display_config_.set_display_mode([mode], False), "Failed to apply display mode"
                    logging.info("\tSuccessfully applied the display mode")

                    # Refresh Panel Caps to get updated pipe and transcoder
                    dut.refresh_panel_caps(adapter)

                    # Verify VRR  and pipe joiner with applied mode in full screen mode
                    status &= self.verify_vrr(True)
                    if status is False:
                        self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
                    logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

                    # Verify VRR  and pipe joiner with applied mode in windowed mode
                    status &= self.verify_vrr(False)
                    if status is False:
                        self.fail("VRR verification failed in Windowed mode with LOW_HIGH_FPS setting")
                    logging.info("PASS: VRR verification passed successfully in Windowed mode")

                    # Verify Pipe Joiner
                    # Compress pipe joiner : if VDSC is require for current mode, then verify VDSC programming
                    # Uncompress pipe joiner: VDSC is not enable and pipe joiner require, then verify pipe joiner
                    if DSCHelper.is_vdsc_required(panel.gfx_index, panel.port):
                        if dsc_verifier.verify_dsc_programming(panel.gfx_index, panel.port) is True:
                            logging.info("VDSC verification for {} Expected = PASS Actual = PASS".format(panel.port))
                        else:
                            self.fail("[Driver Issue] - Incorrect DSC Programming For dsc display plugged at {}".format(
                                panel.port))
                    else:
                        is_pipe_joiner_required, _ = DisplayClock.is_pipe_joiner_required(panel.gfx_index, panel.port)
                        if is_pipe_joiner_required is True:
                            if PipeJoinerBase.verify_pipe_joined_display(panel.port) is True:
                                logging.info("Pipe Joiner Verification Successful for {} display".format(panel.port))
                            else:
                                self.fail("[Driver Issue] - Pipe Joiner Verification failed for {} display"
                                          .format(panel.port))
                        else:
                            logging.info(" Pipe joiner not require for current mode, skipped pipe joiner verification")
        logging.info("PASS: Pipe joiner verification passed successfully")

    ##
    # @brief        Test function to check if VRR is working with Render Compression
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["RENDER_COMPRESSION"])
    # @endcond
    def t_45_render_compression(self):
        status, etl_file = self.verify_vrr(True, return_etl=True)
        if status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                if self.get_e2e_compression_status(adapter) is False:
                    self.fail("E2ECompression is disabled")
                source_format = get_pixel_format('RGB_8888')
                if verify_render_decomp(panel, source_format, etl_file, get_app_name('FLIPAT')) is False:
                    self.fail("Render Decompression Failed")
                logging.info("PASS: Render DeCompression verification passed successfully")

    ##
    # @brief        Test function to check if VRR is working with FlipQ
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FLIPQ"])
    # @endcond
    def t_46_flipq(self):
        status, etl_file = self.verify_vrr(True, return_etl=True)
        if status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info(f"\tStep: Verifying FlipQ")
                if planes_ui_verification.verify_flipq(etl_file, panel.pipe, panel.target_id, adapter.name) is False:
                    self.fail("FAIL: FlipQ verification Failed")
                logging.info("PASS: VRR verification with FlipQ passed successfully")

    ##
    # @brief        Test function to check if VRR is working with MPO
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MPO"])
    # @endcond
    def t_47_mpo(self):
        status, etl_file = self.verify_vrr(True, return_etl=True)
        if status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info(f"\tStep: MPO verification on {panel.port}")
                if pc_external.verify_mpo(adapter, panel, etl_file) is False:
                    self.fail("FAIL: MPO verification Failed")
                logging.info("PASS: MPO verification with VRR passed successfully")

    ##
    # @brief        Test function to check if VRR is working with HDR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HDR"])
    # @endcond
    def t_48_hdr(self):
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info(f"Step: Enable HDR on {panel.port}")
                if pc_external.enable_disable_hdr([panel.port], True) is False:
                    self.fail(f"Failed to enable HDR on {panel.port}")

                # Verify VRR
                logging.info(f"\tStep: Verifying VRR")
                status, etl_file = self.verify_vrr(True, return_etl=True)
                if status is False:
                    self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
                logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

                # Verify HDR
                logging.info(f"\tStep: Verifying HDR")
                if feature_basic_verify.verify_hdr_feature(panel.gfx_index, adapter.name, panel.pipe,
                                                           enable=True) is False:
                    self.fail("HDR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
                logging.info("PASS: HDR verification passed successfully in FULL_SCREEN mode")

                # Disable HDR
                logging.info(f"Step: Disable HDR on {panel.port}")
                if pc_external.enable_disable_hdr([panel.port], False) is False:
                    self.fail(f"Failed to disable HDR on {panel.port}")
                logging.info(f"PASS: HDR disable success on {panel.port}")

    ##
    # @brief        Test function to check if VRR is working with FBC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FBC"])
    # @endcond
    def t_49_fbc(self):
        status, etl_file = self.verify_vrr(True, return_etl=True)
        if status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                logging.info(f"Step: Verifying FBC on {panel.port}")
                if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                    self.fail(f"FAIL : FBC verification on {panel.port}")
                logging.info("PASS: FBC verification with VRR passed successfully")

    ##
    # @brief        Test function to check if VRR is working with HW Rotation
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HW_ROTATION"])
    # @endcond
    def t_50_hw_rotation(self):
        status = True
        # checking only 180 and 0 rotation as 270/90 is not supporting & we will get only Sync flip from OS
        rotation_list = [enum.ROTATE_180, enum.ROTATE_0]
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                current_mode = self.display_config_.get_current_mode(panel.target_id)

                # Apply each rotation and verify VRR
                for rotation in rotation_list:
                    current_mode.rotation = rotation
                    enumerated_displays = self.display_config_.get_enumerated_display_info()
                    logging.info(f"Step: Applying mode : {current_mode.to_string(enumerated_displays)}")
                    result = self.display_config_.set_display_mode([current_mode])
                    self.assertEquals(result, True, "display mode set failed")
                    logging.info("PASS: Successfully applied mode")

                    # verify VRR with HW Rotation
                    logging.info(f"Step: Verifying VRR with rotation {rotation}")
                    status &= self.verify_vrr(True, return_etl=False)
                    if status is False:
                        self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
                    logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

    ##
    # @brief        Test function to check if VRR is working with Gamma
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["GAMMA"])
    # @endcond
    def t_51_gamma(self):
        reference_gamma_lut = color_constants.SRGB_ENCODE_515_SAMPLES_16BPC
        reference_gamma_lut = reference_gamma_lut[:-2]
        gamma_lut_size = 1024
        programmed_gamma_lut = []
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            reg_interface = get_interface(adapter.name, adapter.gfx_index)

            # Verify VRR
            logging.info(f"Step: Verifying VRR")
            status, etl_file = self.verify_vrr(True, return_etl=True)
            if status is False:
                self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
            logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode")

            for panel in adapter.panels.values():
                if adapter.name in common.PRE_GEN_13_PLATFORMS:
                    lut_data = gamma_utility.get_pipe_gamma_lut_from_register_legacy(adapter.gfx_index,
                                                                                     reg_interface,
                                                                                     False, panel.pipe,
                                                                                     lut_size=gamma_lut_size)
                else:
                    cc_block = get_color_conversion_block(adapter.name, panel.pipe)
                    lut_data = gamma_utility.get_pipe_gamma_lut_from_register(adapter.gfx_index, reg_interface,
                                                                              cc_block, panel.pipe,
                                                                              lut_size=gamma_lut_size)

                for index in range(0, len(lut_data), 3):
                    programmed_gamma_lut.append(lut_data[index])

                # Verify Gamma
                if compare_ref_and_programmed_gamma_lut(reference_gamma_lut, programmed_gamma_lut) is False:
                    self.fail(f"Gamma verification failed on {panel.port}")
                logging.info(f"PASS : GAMMA verification on {panel.port} panel is success")

    ##
    # @brief        Test function to check if VRR is working with game and video playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["GAME_VIDEO", "LOW_HIGH_FPS"])
    # @endcond
    def t_52_game_video(self):
        video_file = "24.000.mp4"
        status = None
        is_os_aware_vrr = dut.WIN_OS_VERSION >= dut.WinOsVersion.WIN_19H1
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                # Run game workload without closing
                status, _ = workload.run(workload.GAME_PLAYBACK_WITH_CUSTOM_EVENTS,
                                         [self.app, self.duration, False, False, True, None])
                if not status:
                    gdhm.report_bug(
                        title=f"[OSFeatures][VRR]Failed to run workload for Game Playback using {self.app}",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P3,
                        exposure=gdhm.Exposure.E3
                    )
                    self.fail(f"Failed to run workload for Game Playback using {self.app}")
                # launch new video
                logging.info(f"Launching {video_file} video in Windowed mode")
                app_controls.launch_video(
                    os.path.join(common.TEST_VIDEOS_PATH, f"{video_file}"), is_full_screen=False)
                logging.info(f"Pressing ALT+TAB to switch window to Game")
                kb.press('ALT+TAB')

                # Close the existing game workload
                status, etl_file = workload.run(workload.GAME_PLAYBACK_WITH_CUSTOM_EVENTS,
                                                [self.app, self.duration, False, True, False, None])
                window_helper.close_media_player()
                logging.info("\tClosing video playback")

                if not status:
                    gdhm.report_bug(
                        title=f"[OSFeatures][VRR]Failed to close workload for Game Playback using {self.app}",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P3,
                        exposure=gdhm.Exposure.E3
                    )
                    self.fail(f"Failed to close workload for Game Playback using {self.app}")

                # Verify VRR from the ETL file generated
                status &= vrr.verify(adapter, panel, etl_file, None, False, is_os_aware_vrr, True, False)
        if status is False:
            self.fail("VRR verification failed for Game+Video concurrency test with LOW_HIGH_FPS in WINDOWED mode")
        logging.info("PASS: VRR verification passed successfully for Game+Video concurrency test in WINDOWED mode")

    ############################
    # Helper Functions
    ############################

    ##
    # @brief        This function parses the etl to check if PSR was enabled during VRR active period
    # @param[in]    adapter Adapter target adapter object
    # @param[in]    panel  Panel, panel object of the targeted display
    # @param[in]    is_psr2  is boolean, indicates if psr2 was enabled before VRR
    # @return       True if PSR was not enabled during VRR active period, False otherwise
    @staticmethod
    def check_psr_status(adapter: Adapter, panel: Panel, is_psr2=False):
        psr_regs = adapter.regs.get_psr_offsets(panel.transcoder_type)
        psr_ctl_offset = psr_regs.Psr2CtrlReg if is_psr2 else psr_regs.SrdCtlReg

        mmio_output = etl_parser.get_mmio_data(psr_ctl_offset)
        if mmio_output is None:
            logging.error("\tNo MMIO entry found for PSR_CTL register")
            return False

        # Make sure PSR got enabled at least once during test (before running game, in between or after game)
        is_psr_enabled = False
        for mmio_data in mmio_output:
            if is_psr2:
                psr_info = adapter.regs.get_psr_info(panel.transcoder_type, PsrOffsetValues(Psr2CtrlReg=mmio_data.Data))
                if psr_info.Psr2Enable:
                    logging.info("PASS: PSR2 is enabled before VRR ({0})".format(mmio_data.TimeStamp))
                    is_psr_enabled = True
                    break
            else:
                psr_info = adapter.regs.get_psr_info(panel.transcoder_type, PsrOffsetValues(SrdCtlReg=mmio_data.Data))
                if psr_info.SrdEnable:
                    logging.info("PASS: PSR is enabled before VRR ({0})".format(mmio_data.TimeStamp))
                    is_psr_enabled = True
                    break

        if is_psr_enabled is False:
            logging.error("\tPSR is not getting enabled")
            return False

        # Make sure PSR is not getting enabled while VRR is active
        min_vrr_active_period = 2 * math.floor(1000.0 / 20)
        vrr_active_period = vrr.get_vrr_active_period(adapter, panel)
        if vrr_active_period is None:
            logging.error("\tNo VRR active period found")
            return False

        for vrr_active_start, vrr_active_end in vrr_active_period:
            # Skip if VRR active period is too short
            if (vrr_active_end - vrr_active_start) <= min_vrr_active_period:
                continue

            mmio_output = etl_parser.get_mmio_data(psr_ctl_offset, start_time=vrr_active_start, end_time=vrr_active_end)
            if mmio_output is None:
                logging.info(
                    "\tPASS: No PSR update found during VRR active period ({0}, {1})".format(
                        vrr_active_start, vrr_active_end))
                continue

            for mmio_data in mmio_output:
                if is_psr2:
                    psr_info = adapter.regs.get_psr_info(panel.transcoder_type,
                                                         PsrOffsetValues(Psr2CtrlReg=mmio_data.Data))
                    if psr_info.Psr2Enable:
                        logging.error(
                            "FAIL: PSR2 got enabled in VRR active period [{0}] (Driver Issue)".format(
                                mmio_data.TimeStamp))
                        return False
                else:
                    psr_info = adapter.regs.get_psr_info(panel.transcoder_type,
                                                         PsrOffsetValues(SrdCtlReg=mmio_data.Data))
                    if psr_info.SrdEnable:
                        logging.error(
                            "FAIL: PSR got enabled in VRR active period [{0}] (Driver Issue)".format(
                                mmio_data.TimeStamp))
                        return False

            logging.info(
                "PASS: PSR status during VRR Expected= DISABLED, Actual= DISABLED ({0}, {1})".format(
                    vrr_active_start, vrr_active_end))

        _, vrr_active_end = vrr_active_period[-1]
        mmio_output = etl_parser.get_mmio_data(psr_ctl_offset, start_time=vrr_active_end)
        if mmio_output is None:
            logging.warning("\tNo PSR update found after VRR active period ({0})".format(vrr_active_end))
        else:
            for mmio_data in mmio_output:
                if is_psr2:
                    psr_info = adapter.regs.get_psr_info(panel.transcoder_type,
                                                         PsrOffsetValues(Psr2CtrlReg=mmio_data.Data))
                    if psr_info.Psr2Enable:
                        logging.info("PASS: PSR2 is enabled after VRR ({0})".format(mmio_data.TimeStamp))
                        return True
                else:
                    psr_info = adapter.regs.get_psr_info(panel.transcoder_type,
                                                         PsrOffsetValues(SrdCtlReg=mmio_data.Data))
                    if psr_info.SrdEnable:
                        logging.info("PASS: PSR is enabled after VRR ({0})".format(mmio_data.TimeStamp))
                        return True
        return True

    ##
    # @brief        Verify E2E compression Reg key status
    # @param[in]    adapter object
    # @return       True if enabled else False
    @staticmethod
    def get_e2e_compression_status(adapter):
        if adapter.name not in common.PRE_GEN_12_PLATFORMS:
            legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                            reg_path=INTEL_GMM_PATH)
            registry_value, _ = registry_access.read(legacy_reg_args, "DisableE2ECompression", sub_key="GMM")
            if registry_value == 0:
                logging.info("E2ECompression is enabled")
            elif registry_value == 1:
                logging.error("E2ECompression is disabled")
                return False
            else:
                logging.debug(
                    f"E2ECompression Master Registry path/key is not available. Returned value - {registry_value}")
        return True


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestConcurrency))
    TestEnvironment.cleanup(test_result)
