########################################################################################################################
# @file         fbc_concurrency.py
# @brief        Test for verifying FBC feature with HDR
#
# @author       Chandrakanth Reddy y
########################################################################################################################

import os
import time

from Libs.Core import display_power
from Libs.Core import enum, window_helper, winkb_helper, app_controls, registry_access, display_utility
from Libs.Core.flip import MPO
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.test_env import test_context
from Libs.Core.test_env import test_environment
from Libs.Core.test_env.test_context import TestContext
from Tests.Display_Decompression.Playback import decomp_verifier
from Tests.PlanesUI.Common import planes_ui_verification
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.FBC.fbc_base import *
from Tests.PowerCons.Modules import common
from Tests.PowerCons.Modules import workload

SCAN_OUT_APP = r'C:/Program Files (x86)/Microsoft DirectX SDK ' \
               r'(June 2010)/Samples/C++/Direct3D10/Bin/x64/10BitScanout10.exe'


##
# @brief        This class contains FBC feature concurrency tests
class FbcConcurrency(FbcBase):
    display_power_ = display_power.DisplayPower()

    ##
    # @brief        This function validates FBC with HDR enable
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HDR"])
    # @endcond
    def t_11_fbc_hdr(self):
        hdr_support = False
        # HDR requires AC mode
        if self.display_power_.set_current_powerline_status(display_power.PowerSource.AC) is False:
            self.fail("Failed to switch power line status to AC (Test Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.hdr_caps.is_hdr_supported is False:
                    logging.info(f"HDR is not supported on {panel.port}")
                    continue
                hdr_support = True
                if check_fbc_support(adapter, panel) is False:
                    logging.info(f"SKIP: FBC is not supported on pipe {panel.pipe} on {adapter.name}")
                    continue
                logging.info(f"STEP: Verify FBC with HDR enable on {panel.port}")
                # Enable HDR
                if pc_external.enable_disable_hdr([panel.port], True) is False:
                    self.fail(f"Failed to enable HDR on {panel.port}")
                # verify FBC with HDR enable
                if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                    self.fail(f"FAIL : FBC verification on {panel.port}")
                logging.info(f"PASS: FBC verification with HDR on {panel.port}")
        if hdr_support is False:
            self.fail("None of the panels support HDR(Planning Issue)")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.hdr_caps.is_hdr_supported is False:
                    continue
                logging.info(f"STEP: Disable HDR on {panel.port}")
                # Disable HDR
                if pc_external.enable_disable_hdr([panel.port], False) is False:
                    self.fail(f"Failed to disable HDR on {panel.port}")
                logging.info(f"PASS: HDR disable success on {panel.port}")

    ##
    # @brief        This function validates FBC with H/W Rotation
    # @return       None
    # @cond

    @common.configure_test(repeat=True, selective=["HW_ROTATION"])
    # @endcond
    def t_12_fbc_rotation(self):
        rotation_list = [enum.ROTATE_270, enum.ROTATE_180, enum.ROTATE_90, enum.ROTATE_0]
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if check_fbc_support(adapter, panel) is False:
                    logging.info(f"SKIP: FBC is not supported on pipe {panel.pipe} on {adapter.name}")
                    continue
                current_mode = self.display_config_.get_current_mode(panel.target_id)
                # Apply each rotation and verify FBC
                for rotation in rotation_list:
                    current_mode.rotation = rotation
                    enumerated_displays = self.display_config_.get_enumerated_display_info()
                    logging.info(f"STEP: Applying mode : {current_mode.to_string(enumerated_displays)}")
                    result = self.display_config_.set_display_mode([current_mode])
                    self.assertEquals(result, True, "display mode set failed")
                    logging.info("PASS: Successfully applied mode")
                    # verify FBC with HW Rotation
                    logging.info(f"STEP: Verifying FBC with rotation {rotation}")
                    if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                        self.fail(f"FAIL : FBC verification on {panel.port}")
                    logging.info(f"PASS: FBC verification on {panel.port}")

    ##
    # @brief        This function validates FBC with FLip Queue
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FLIP_QUEUE"])
    # @endcond
    def t_13_fbc_flip_queue(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if check_fbc_support(adapter, panel) is False:
                    logging.info(f"SKIP: FBC is not supported on pipe {panel.pipe} on {adapter.name}")
                    continue
                polling_args = get_fbc_reg_instance(adapter, panel)
                etl_file, polling_data = workload.run(workload.VIDEO_PLAYBACK, [24, 60],
                                                      polling_args=[[polling_args.offset], 0.01])
                logging.info(f"Step: Verifying Flip Queue on {panel.port}")
                if planes_ui_verification.verify_flipq(etl_file, panel.pipe, panel.target_id, adapter.name):
                    logging.info("FlipQ verification successful")
                else:
                    self.fail("FlipQ verification failed")
                logging.info("Step: Verify FBC disable with FlipQ")
                status = verify_fbc_with_flip_queue(adapter, panel, polling_data)
                if status is False:
                    gdhm.report_driver_bug_pc("[PowerCons][FBC] Failed to verify FBC with Flip_Queue")
                    self.fail("FBC verification with FlipQueue is failed")
                logging.info(f"PASS: FBC verification with FlipQueue on {panel.port}")

    ##
    # @brief        This function validates FBC with DP MST Panel
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DP_MST"])
    # @endcond
    def t_14_fbc_mst(self):
        xml_file = os.path.join(TestContext.panel_input_data(), 'DP_MST_TILE', 'DPMST_1Branch_1MSTDisplay.xml')
        display_port = DisplayPort()
        for adapter in dut.adapters.values():
            logging.info(f"STEP: Verifying FBC on adapter {adapter.gfx_index}")
            if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                self.fail(f"FAIL : FBC verification")
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    continue
                logging.info(f"Step:unplug display {panel.port}")
                if display_utility.unplug(panel.port) is False:
                    self.fail(f"Failed to unplug display {panel.port}")
                time.sleep(2)
                logging.info(f"Pass:{panel.port} display unplug success")
                logging.info(f"STEP: PLugging MST panel on port {panel.port}")
                if display_port.init_dp(panel.port, "MST", adapter.gfx_index) is False:
                    self.fail("DP initialization is failed")
                if display_port.parse_send_topology(panel.port, "MST", xml_file, lowpower=False) is False:
                    self.fail("DP topology parsing failed")
                if display_port.set_hpd(panel.port, True) is False:
                    self.fail("DP MST Panel plug failed")
                logging.info(f"DP MST Plug successful")
                logging.info("Additional 20 secs delay after plug for MST config")
                time.sleep(20)
                if self.display_config_.set_display_configuration_ex(enum.SINGLE, [panel.port]) is False:
                    self.fail("Failed to apply display configuration(Test Issue)")
                dut.refresh_panel_caps(adapter)
                if check_fbc_support(adapter, panel) is False:
                    logging.info(f"SKIP: FBC is not supported on pipe {panel.pipe} on {adapter.name}")
                    continue
                # verify FBC with MST Panel
                logging.info(f"STEP: Verifying FBC with MST Panel")
                if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                    self.fail(f"FAIL : FBC verification")
                logging.info(f"PASS: FBC verification on {panel.port}")

    ##
    # @brief        This function validates FBC with different MPO formats
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PLANE_FORMAT"])
    # @endcond
    def t_15_fbc_mpo_formats(self):
        for adapter in dut.adapters.values():
            enable_mpo = MPO()
            ##
            # Enable the DFT framework and feature
            enable_mpo.enable_disable_mpo_dft(True, 1, gfx_adapter_index=adapter.gfx_index)
            logging.info(f"\tEnabled the DFT framework on {adapter.gfx_index}")
            for panel in adapter.panels.values():
                if check_fbc_support(adapter, panel) is False:
                    logging.info(f"SKIP: FBC is not supported on pipe {panel.pipe} on {adapter.name}")
                    continue
                if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                    self.fail(f"FAIL : FBC verification on {panel.port}")
                for pixel_frmt in list(pc_external.PIXEL_FORMAT.values()):
                    pixel_format = [pixel_frmt, None, None]
                    if pc_external.plane_format(adapter, panel, self.no_of_displays, self.source_id, enable_mpo,
                                                pixel_format=pixel_format) is False:
                        gdhm.report_test_bug_os(f"[PowerCons][FBC] Failed to generate FLIP on {pixel_frmt[0]}")
                        self.fail(f"Failed to generate FLIP {pixel_frmt[0]}")
                    if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                        self.fail(f"FAIL : FBC verification on {panel.port}")
                    logging.info(f"PASS: FBC verification on {panel.port}")
            ##
            # Disable the DFT framework and feature
            enable_mpo.enable_disable_mpo_dft(False, 1, gfx_adapter_index=adapter.gfx_index)
            logging.info(f"\tDisabled the DFT framework on {adapter.gfx_index}")
            time.sleep(2)

    ##
    # @brief        This function validates FBC with Render compression
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["RENDER_COMPRESSION"])
    # @endcond
    def t_16_fbc_render_compression(self):
        for adapter in dut.adapters.values():
            if decomp_verifier.is_feature_supported("RENDER_DECOMP") is False:
                logging.info(f"SKIP: Render DeCompression is not supported on {adapter.name}")
                continue
            for panel in adapter.panels.values():
                if check_fbc_support(adapter, panel) is False:
                    logging.info(f"SKIP: FBC is not supported on pipe {panel.pipe} on {adapter.name}")
                    continue
                if get_e2e_compression_status(adapter) is False:
                    self.fail("E2E compression check failed")
                etl_file, status = get_workload_traces(adapter, panel, method='GAME')
                if status is False:
                    self.fail(f"FBC verification failed on {panel.port}")
                source_format = decomp_verifier.get_pixel_format('RGB_8888')
                if decomp_verifier.verify_render_decomp(panel, source_format, etl_file,
                                                        decomp_verifier.get_app_name('FLIPAT')) is False:
                    self.fail("Render Decompression Failed")
                logging.info(f"PASS: FBC verification on {panel.port}")

    ##
    # @brief        This function validates FBC with Media compression
    # @return       None
    # @cond

    @common.configure_test(repeat=True, selective=["MEDIA_COMPRESSION"])
    # @endcond
    def t_17_fbc_media_compression(self):
        for adapter in dut.adapters.values():
            if decomp_verifier.is_feature_supported("MEDIA_DECOMP") is False:
                logging.info(f"SKIP: Media DeCompression is not supported on {adapter.name}")
                continue
            for panel in adapter.panels.values():
                if check_fbc_support(adapter, panel) is False:
                    logging.info(f"SKIP: FBC is not supported on pipe {panel.pipe} on {adapter.name}")
                    continue
                etl_file, status = get_workload_traces(adapter, panel, method='VIDEO')
                if status is False:
                    self.fail(f"FBC verification failed on {panel.port}")
                source_format = decomp_verifier.get_pixel_format('YUV_420')
                if decomp_verifier.verify_media_decomp(panel, source_format, etl_file,
                                                       decomp_verifier.get_app_name('MEDIA')) is False:
                    self.fail("Media Decompression Failed")
                logging.info(f"PASS: FBC verification on {panel.port}")


##
# @brief        Verify E2E compression Reg key status
# @param[in]    adapter object
# @return       True if enabled else False
def get_e2e_compression_status(adapter):
    if adapter.name not in common.PRE_GEN_12_PLATFORMS:
        legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                        reg_path=decomp_verifier.INTEL_GMM_PATH)
        registry_value, _ = registry_access.read(legacy_reg_args, "DisableE2ECompression", sub_key="GMM")
        if registry_value is not None:
            if registry_value != 0:
                logging.error("E2ECompression is disabled")
                gdhm.report_driver_bug_pc(f"[Powercons][FBC] E2ECompression is disabled in registry key")
                return False
            logging.info("E2ECompression is enabled")
        else:
            logging.info(f"E2ECompression Master Registry path/key is not available. Returned value - "
                         f"{registry_value}")
    return True


##
# @brief        Run the given workload and verify FBC
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    method VIDEO/GAME
# @param[in]    full_screen True/False
# @return       True if enabled else False
def get_workload_traces(adapter, panel, method='VIDEO', full_screen=True):
    status = True
    # Stop the ETL before workload
    etl_status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceBefore{method}Workload")
    if etl_status is False:
        status = False

    # Minimize all windows before playback
    winkb_helper.press('WIN+M')

    if method == 'VIDEO':
        # Play MTA App
        logging.info("Invoking Movies & TV Media player")
        media_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "MediaDecomp\Media Clip.mp4")
        app_controls.launch_video(media_file, is_full_screen=full_screen)
        # Playback for 30s
        time.sleep(30)
        if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
            status = False
        # Close the media player
        window_helper.close_media_player()
        time.sleep(5)

        # Console to Main window
        winkb_helper.press('ALT+TAB')
    elif method == 'GAME':
        mode = "full screen mode " if full_screen else "windowed mode"
        app_config = workload.FlipAtAppConfig()
        app_config.v_sync = False
        logging.info(f"Launching FlipAt Application in {mode}")

        # Open the FlipAt App
        if workload.open_gaming_app(workload.Apps.FlipAt, full_screen, 0, app_config):
            time.sleep(5)
        else:
            logging.error(f"\tFailed to open {workload.Apps.FlipAt} app(Test Issue)")
            status = False

        logging.info(f"Launched FlipAt Application Successfully in {mode}")
        if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
            logging.error(f"FAIL : FBC verification on {panel.port}")
            status = False

        # Close the APP
        if workload.close_gaming_app():
            time.sleep(5)
        else:
            logging.error(f"\tFailed to open {workload.Apps.FlipAt} app(Test Issue)")
            status = False

    # Collect ETL araces during workload
    etl_status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceDuring{method}Workload")
    if etl_status is False:
        status = False

    return etl_file, status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(FbcConcurrency))
    test_environment.TestEnvironment.cleanup(test_result)
