########################################################################################################################
# @file         test_concurrency.py
# @brief        Test for verifying PSR feature with DRRS, DMRRS, VRR, HRR, CFPS, LACE, Gamma
#
# @author       Chandrakanth Reddy
########################################################################################################################
import logging

from Libs.Core.wrapper import control_api_wrapper

from DisplayRegs import get_interface
from Libs.Core import display_power, display_utility
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.test_env import test_environment
from Libs.Core.test_env.test_context import TestContext
from Libs.Feature.vdsc import dsc_verifier
from Tests.BFR import bfr
from Tests.Color.Common import gamma_utility, color_constants
from Tests.Color.Common.common_utility import get_color_conversion_block
from Tests.Color.Common.gamma_utility import compare_ref_and_programmed_gamma_lut
from Tests.PlanesUI.Common import planes_ui_verification
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.CFPS import cfps
from Tests.PowerCons.Functional.DCSTATES import dc_state
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Functional.DMRRS import hrr
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.PSR.psr_base import *
from Tests.PowerCons.Modules import workload, dpcd
from Tests.VRR import vrr


##
# @brief        This class contains PSR concurrency Tests
class TestConcurrency(PsrBase):

    ##
    # @brief        This function validates PSR with AC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LACE"])
    # @endcond
    def t_11_psr_lace(self):
        # Enable Lace1.0 version support for ARL
        if SystemInfo().get_sku_name('gfx_0') == 'ARL' and self.lace1p0_status:
            if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                             reg_datatype=registry_access.RegDataType.DWORD, reg_value=10,
                                             driver_restart_required=True) is False:
                logging.error("Failed to enable Lace1.0 registry key")
                self.fail("Failed to enable Lace1.0 registry key")
            logging.info("Registry key add to enable Lace1.0 is successful")
        else:
            logging.info("Lace1.0 Registry Key is either not present or not enabled")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and (panel.pr_caps.is_pr_supported is False):
                    continue
                if adapter.name in ['TGL', 'DG1', 'DG2'] and panel.pipe == 'B':
                    logging.error("LACE is not supported on PIPE {0} on {1}".format(panel.pipe, panel.port))
                    continue
                try:
                    lace_enable_status, etl_file_during_lace_enable = pc_external.enable_disable_lace(adapter, panel, True, adapter.gfx_index)
                    if lace_enable_status is False:
                        self.fail(f"Failed to enable LACE in adapter {adapter.gfx_index}")

                    if self.validate_feature() is False:
                        self.fail(f"PSR verification failed with LACE on {panel.port}")

                    logging.info(f"STEP: Verifying LACE on {panel.port}")
                    if pc_external.get_lace_status(adapter, panel) is False:
                        self.fail("LACE verification failed")
                    logging.info(f"PASS: {self.feature_str} verification with LACE on {panel.port}")
                except Exception as e:
                    self.fail(e)
                finally:
                    # Disable LACE at the end of verification
                    lace_disable_status, etl_file_during_lace_disable = pc_external.enable_disable_lace(adapter, panel, False, adapter.gfx_index)
                    if lace_disable_status is False:
                        self.fail(f"Failed to disable LACE in adapter {adapter.gfx_index}")
                    logging.info(f"Successfully disabled LACE in adapter {adapter.gfx_index}")
                    time.sleep(2)

    ##
    # @brief        This function validates PSR with Gamma
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["GAMMA"])
    # @endcond
    def t_12_psr_gamma(self):
        reference_gamma_lut = color_constants.SRGB_ENCODE_515_SAMPLES_16BPC
        gamma_lut_size = 1024
        programmed_gamma_lut = []
        for adapter in dut.adapters.values():
            reg_interface = get_interface(adapter.name, adapter.gfx_index)
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and (panel.pr_caps.is_pr_supported is False):
                    continue
                if adapter.name in common.PRE_GEN_13_PLATFORMS:
                    lut_data = gamma_utility.get_pipe_gamma_lut_from_register_legacy(
                        adapter.gfx_index, reg_interface, False, panel.pipe, lut_size=gamma_lut_size)
                else:
                    cc_block = get_color_conversion_block(adapter.name, panel.pipe)
                    lut_data = gamma_utility.get_pipe_gamma_lut_from_register(
                        adapter.gfx_index, reg_interface, cc_block, panel.pipe, lut_size=gamma_lut_size)
                    # 2 Color blocks will be used from GEN13+. For CC2, it will be 513 samples
                    reference_gamma_lut = color_constants.SRGB_ENCODE_515_SAMPLES_16BPC
                    if cc_block != "CC1":
                        reference_gamma_lut = color_constants.SRGB_ENCODE_515_SAMPLES_16BPC[0:513]

                for index in range(0, len(lut_data), 3):
                    programmed_gamma_lut.append(lut_data[index])

                if compare_ref_and_programmed_gamma_lut(reference_gamma_lut, programmed_gamma_lut) is False:
                    self.fail(f"Gamma verification failed on {panel.port}")
                logging.info(f"PASS : GAMMA verification on {panel.port} panel is success")

    ##
    # @brief        This function validates PSR with 3D LUT
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["3D_LUT"])
    # @endcond
    def t_18_psr_3d_lut(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and (panel.pr_caps.is_pr_supported is False):
                    continue
                try:
                    res, etl_file = pc_external.verify_3dlut(adapter, panel)
                    if res is False:
                        self.fail("\t3D LUT verification Failed")
                except Exception as e:
                    self.fail(e)
                finally:
                    # Apply default bin before returning
                    pc_external.apply_default_bin(adapter, panel)
                logging.info(f"PASS : 3D LUT verification on {panel.port} panel is success")

    ##
    # @brief        This function validates PSR with RR features
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DRRS"])
    # @endcond
    def t_13_psr_drrs(self):
        status = True
        if not self.display_power_.set_current_powerline_status(display_power.PowerSource.DC):
            self.fail("Failed to switch power line status to DC (Test Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                if panel.drrs_caps.is_drrs_supported:
                    monitors = app_controls.get_enumerated_display_monitors()
                    monitor_ids = [_[0] for _ in monitors]
                    polling_args = psr.get_polling_offsets(self.feature)
                    etl_file_path, polling_data = workload.run(workload.SCREEN_UPDATE, [monitor_ids],
                                                               polling_args=[polling_args, psr.DEFAULT_POLLING_DELAY])
                    status &= drrs.verify(adapter, panel, etl_file_path)
                    if self.feature == psr.UserRequestedFeature.PSR_1 and status is False:
                        logging.info("PASS: DRRS is not enabled when PSR1 is active")
                        status = True
                    logging.info(f"STEP: verifying {self.feature} on {panel.port}")
                    if self.feature == psr.UserRequestedFeature.PSR_1:
                        status &= psr.verify_psr1(adapter, panel, polling_data)
                    elif self.feature == psr.UserRequestedFeature.PANEL_REPLAY:
                        status &= pr.verify_pr_hw_state(adapter, panel, etl_file_path)
                    else:
                        status &= psr.verify_psr2(adapter, panel, polling_data, method="VIDEO", pause_video=False,
                                                  is_basic_check=True)
                    if status is False:
                        self.fail(f"{self.feature_str} verification with DRRS on {panel.port} is failed")
                else:
                    self.fail(f"Panel {panel.port} doesn't support DRRS(Test Issue)")
                logging.info(f"PASS: {self.feature_str} verification with DRRS on {panel.port}")

    ##
    # @brief        This function validates PSR with DMRRS feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DMRRS"])
    # @endcond
    def t_14_psr_dmrrs(self):
        status = True
        if not self.display_power_.set_current_powerline_status(display_power.PowerSource.DC):
            self.fail("Failed to switch power line status to DC (Test Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if (panel.pr_caps.is_pr_supported is False) and (panel.psr_caps.is_psr_supported is False):
                    continue
                if panel.drrs_caps.is_dmrrs_supported is False:
                    self.fail(f"Panel {panel.port} doesn't support DMRRS(Test Issue)")
                polling_args = psr.get_polling_offsets(psr.UserRequestedFeature.PSR_1)
                etl_file_path, polling_data = workload.run(workload.VIDEO_PLAYBACK,
                                                           [psr.DEFAULT_MEDIA_FPS, psr.DEFAULT_PLAYBACK_DURATION],
                                                           polling_args=[polling_args, psr.DEFAULT_POLLING_DELAY])
                if self.feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    status &= pr.verify_pr_hw_state(adapter, panel, etl_file_path, method="VIDEO")
                else:
                    status &= psr.verify_psr_entry(adapter, panel, polling_data, method="VIDEO")
                status &= dmrrs.verify(adapter, panel, etl_file_path, psr.DEFAULT_MEDIA_FPS)
                if status is False:
                    self.fail(f"{self.feature_str} verification with DMRRS is failed")
                logging.info(f"PASS: {self.feature_str} verification with DMRRS on {panel.port}")

    ##
    # @brief        This function validates PSR with HRR feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HRR"])
    # @endcond
    def t_15_psr_hrr(self):
        assert dut.is_feature_supported('HRR'), "None of the adapter supports HRR"
        if not self.display_power_.set_current_powerline_status(display_power.PowerSource.DC):
            self.fail("Failed to switch power line status to DC (Test Issue)")
        for adapter in dut.adapters.values():
            hrr_status = hrr.enable(adapter)
            dut.refresh_panel_caps(adapter)
            if hrr_status is False:
                self.fail(f"Failed to enable HRR on {adapter.name}")
            if hrr_status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail("\tFAILED to restart display driver after reg-key update")
                logging.info(f"Successfully enabled HRR on {adapter.name}")

            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                if panel.drrs_caps.is_dmrrs_supported is False:
                    self.fail(f"Panel {panel.port} doesn't support DMRRS(Test Issue)")
                polling_args = psr.get_polling_offsets(psr.UserRequestedFeature.PSR_1)
                etl_file_path, polling_data = workload.run(workload.VIDEO_PLAYBACK,
                                                           [psr.DEFAULT_MEDIA_FPS, psr.DEFAULT_PLAYBACK_DURATION],
                                                           polling_args=[polling_args, psr.DEFAULT_POLLING_DELAY])
                logging.info(f"STEP: verify {self.feature_str} on {panel.port}")
                if self.feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    status = pr.verify_pr_hw_state(adapter, panel, etl_file_path, method="VIDEO")
                else:
                    status = psr.verify_psr_entry(adapter, panel, polling_data, method="VIDEO")
                status &= hrr.verify(adapter, panel, etl_file_path, psr.DEFAULT_MEDIA_FPS)
                # todo - Need to remove below code after HRR enable in driver
                hrr_status = hrr.disable(adapter)
                dut.refresh_panel_caps(adapter)
                if hrr_status is False:
                    self.fail(f"Failed to disable HRR on {adapter.name}")
                if hrr_status is True:
                    result, reboot_required = display_essential.restart_gfx_driver()
                    if result is False:
                        self.fail("\tFAILED to restart display driver after reg-key update")
                    logging.info(f"Successfully disabled HRR on {adapter.name}")
                if status is False:
                    self.fail(f"{self.feature_str} verification with HRR is failed")
                logging.info(f"PASS: {self.feature_str} verification HRR on {panel.port}")

    ##
    # @brief        This function validates PSR with VRR feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VRR"])
    # @endcond
    def t_16_psr_vrr(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                if not panel.vrr_caps.is_vrr_supported:
                    self.fail(f"Panel {panel.port} doesn't support VRR")
                polling_args = psr.get_polling_offsets(self.feature)
                etl_file, polling_data = workload.run(workload.GAME_PLAYBACK,
                                                      [workload.Apps.Classic3DCubeApp, 30, True],
                                                      polling_args=[polling_args, psr.DEFAULT_POLLING_DELAY])
                # Ensure async flips
                if vrr.async_flips_present(etl_file) is False:
                    etl_file, polling_data = workload.run(workload.GAME_PLAYBACK,
                                                          [workload.Apps.MovingRectangleApp, 30, True],
                                                          polling_args=[polling_args, psr.DEFAULT_POLLING_DELAY])
                    if vrr.async_flips_present(etl_file) is False:
                        self.fail("OS is NOT sending async flips")
                logging.info("Step: Verifying VRR for {0}".format(panel.port))
                status &= vrr.verify(adapter, panel, etl_file)
                logging.info(f"STEP: verify {self.feature_str} on {panel.port}")
                if self.feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    status &= pr.verify_pr_hw_state(adapter, panel, etl_file, method="GAME")
                else:
                    status &= psr.verify_psr_entry(adapter, panel, polling_data, method="GAME", feature=self.feature)
                if status is False:
                    self.fail(f"{self.feature_str} verification with VRR is failed")
                logging.info(f"PASS: {self.feature_str} verification VRR on {panel.port}")

    ##
    # @brief        This function validates PSR with CFPS feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CFPS"])
    # @endcond
    def t_17_psr_cfps(self):
        status = True
        for adapter in dut.adapters.values():
            if cfps.enable(adapter) is False:
                self.fail("FAILED to enable CFPS")
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                app_config = workload.FlipAtAppConfig()
                app_config.game_index = 2
                app_config.pattern_1 = vrr.get_fps_pattern(panel.max_rr)
                app_config.pattern_2 = vrr.get_fps_pattern(panel.max_rr)
                etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config])

                logging.info(f"STEP: Verifying CFPS on {panel.port}")
                status &= cfps.verify(adapter, etl_file)
                logging.info(f"STEP: Verify {self.feature_str} on {panel.port}")
                if self.feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    status &= pr.verify_pr_hw_state(adapter, panel, etl_file, method="GAME")
                else:
                    status &= psr.verify_psr_entry_via_etl(adapter, panel, etl_file, method="GAME", feature=self.feature)
                # When CFPS is enabled, VRR is disabled, so restoring VRR
                if adapter.is_vrr_supported is True:
                    if vrr.enable(adapter) is False:
                        self.fail("FAILED to enable VRR")
                if status is False:
                    self.fail(f"{self.feature_str} verification with CFPS is failed")
                logging.info(f"PASS: {self.feature_str} verification CFPS on {panel.port}")

    ##
    # @brief        This function validates PSR with HW rotation feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HW_ROTATION"])
    # @endcond
    def t_18_psr_rotation(self):
        rotation_list = [enum.ROTATE_270, enum.ROTATE_180, enum.ROTATE_90, enum.ROTATE_0]
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                current_mode = self.display_config_.get_current_mode(panel.target_id)
                # Apply each rotation and verify PSR
                for rotation in rotation_list:
                    current_mode.rotation = rotation
                    enumerated_displays = self.display_config_.get_enumerated_display_info()
                    logging.info(f"Applying mode : {current_mode.to_string(enumerated_displays)}")
                    result = self.display_config_.set_display_mode([current_mode])
                    self.assertEquals(result, True, "display mode set failed")
                    if adapter.name not in common.PRE_GEN_12_PLATFORMS and (
                            self.feature >= psr.UserRequestedFeature.PSR_2):
                        logging.info(f"STEP: Verifying {self.feature_str} with rotation {rotation}")
                        if panel.pr_caps.is_pr_supported:
                            pr_caps = dpcd.PanelReplayCapsSupported(panel.target_id)
                            if (pr_caps.selective_update_support == 0) and \
                                    sfsu.get_man_trk_status(adapter, panel) != sfsu.SuType.SU_CONTINUOUS_UPDATE:
                                self.fail("Selective Fetch is disabled")
                        else:
                            if sfsu.get_man_trk_status(adapter, panel) != sfsu.SuType.SU_PARTIAL_FRAME_UPDATE:
                                self.fail("Selective Fetch is disabled")
                    logging.info(f"PASS: {self.feature_str} verification with rotation {rotation} {panel.port}")

    ##
    # @brief        This function validates PSR with FLip Queue
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FLIP_QUEUE"])
    # @endcond
    def t_19_psr_with_flip_queue(self):
        status = True
        for adapter in dut.adapters.values():
            if adapter.name in common.PRE_GEN_13_PLATFORMS:
                logging.info("Skipping verification on PRE-GEN13 platforms")
                continue
            # Verify DC6V along with flip queue if enabled in INF
            display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
            check_dc6v = (display_pc.DisableDC6v == 0)
            for panel in adapter.panels.values():
                if panel.is_lfp is False or \
                        (panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False):
                    continue
                dc_state_en = MMIORegister.get_instance("DC_STATE_EN_REGISTER", "DC_STATE_EN", adapter.name)
                polling_args = psr.get_polling_offsets(self.feature)
                polling_args.append(dc_state_en.offset)
                etl_file, polling_data = workload.run(workload.VIDEO_PLAYBACK,
                                                      [psr.DEFAULT_MEDIA_FPS, psr.DEFAULT_PLAYBACK_DURATION],
                                                      polling_args=[polling_args, psr.DEFAULT_POLLING_DELAY])
                logging.info(f"Step: Verifying Flip Queue on {panel.port}")
                if planes_ui_verification.verify_flipq(etl_file, panel.pipe, panel.target_id, adapter.name) is False:
                    self.fail("FlipQ verification failed")
                logging.info("FlipQ verification successful")
                if self.feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    status &= pr.verify_pr_hw_state(adapter, panel, etl_file, method="VIDEO")
                elif self.feature >= psr.UserRequestedFeature.PSR_2:
                    status &= psr.verify_psr2(adapter, panel, polling_data, method="VIDEO", pause_video=False,
                                              is_basic_check=True)
                    pwr_src = self.display_power_.get_current_powerline_status()
                    dpst_enable = is_dpst_possible(panel, pwr_src)
                    feature, _ = self.get_feature(adapter)
                    status &= sfsu.verify_sfsu(adapter, panel, etl_file, self.method, feature, dpst_enable)
                if check_dc6v:
                    status &= dc_state.verify_dc6v_vbi(adapter, self.method, etl_file)
                if status is False:
                    self.fail(f"{self.feature_str} verification with FlipQueue is failed")
                logging.info(f"PASS: {self.feature_str} verification with FlipQueue on {panel.port}")

    ##
    # @brief        This function validates PSR2  with VDSC + FEC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VDSC"])
    # @endcond
    def t_20_psr_with_vdsc(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                # Check if panel supports VDSC. Fail if the  panel doesn't support VDSC
                if panel.vdsc_caps.is_vdsc_supported is False:
                    self.fail("VDSC panel is not connected (Planning Issue)")

                if self.validate_feature() is False:
                    self.fail(f"{self.feature_str} verification failed with VDSC on {panel.port}")

                if dsc_verifier.verify_dsc_programming(adapter.gfx_index, panel.port) is False:
                    self.fail(f"FAILED to verify DSC with PSR on {panel.port}")
                logging.info(f"Successfully verified DSC with {self.feature_str} on {panel.port}")

    ##
    # @brief        This function validates PSR2  with BFR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["BFR"])
    # @endcond
    def t_21_psr_with_bfr(self):
        status = True
        polling_data = None
        etl_file = None
        for adapter in dut.adapters.values():
            if adapter.name in common.PRE_GEN_12_PLATFORMS:
                self.fail(f"BFR is not supported on {adapter.name}")
            for panel in adapter.panels.values():
                if panel.bfr_caps.is_bfr_supported is False:
                    logging.info(f"BFR not supported on {panel.port}")
                    continue
                logging.info("Step: Enable Dynamic RR mode")
                if bfr.set_dynamic_rr(panel) is False:
                    self.fail("Unable to set Dynamic RR mode")
                polling_args = psr.get_polling_offsets(self.feature)
                for trial in range(3):
                    logging.info(f"Verifying BFR with attempt {trial + 1}")
                    # Run Workload
                    etl_file, polling_data = workload.run(workload.BOOSTED_APP,
                                                          [psr.DEFAULT_PLAYBACK_DURATION, panel, None],
                                                          polling_args=[polling_args, psr.DEFAULT_POLLING_DELAY])
                    status = bfr.verify(adapter, panel, etl_file)
                    if status:
                        break
                if self.feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    status &= pr.verify_pr_hw_state(adapter, panel, etl_file, method="APP")
                else:
                    status &= psr.verify_psr_entry(adapter, panel, polling_data, method="BOOSTED_APP", feature=self.feature)
                if status is False:
                    self.fail(f"{self.feature_str} verification with BFR is failed")
                logging.info(f"PASS: BFR Verification Successful with PSR panel on {panel.port}")

    ##
    # @brief        This function validates PR  with Tiled Display
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PR_TILED"])
    # @endcond
    def t_22_pr_with_Tiled(self):
        master_edid, master_dpcd, master_port = None, None, None
        slave_edid, slave_port = None, None
        panel_index = None
        self.display_port = DisplayPort()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.pr_caps.is_pr_supported is False:
                    continue
                if panel.is_lfp:
                    continue
                if panel_index is None:
                    master_edid = os.path.join(TestContext.panel_input_data(), 'DP_MST_TILE', 'DELL_U2715_M.EDID')
                    master_dpcd = os.path.join(TestContext.panel_input_data(), 'DP_MST_TILE', 'DELL_U2715_PR_DPCD.bin')
                    master_port = panel.port
                    panel_index = panel.panel_index
                else:
                    slave_edid = master_edid.replace('M.', 'S.')
                    slave_port = panel.port
                logging.info(f"Step:unplug display {panel.port}")
                if display_utility.unplug(panel.port) is False:
                    self.fail(f"Failed to unplug display {panel.port}")
                time.sleep(5)
                logging.info(f"Pass:{panel.port} display unplug success")
            if self.display_port.plug_unplug_tiled_display(True, True, master_port, slave_port, master_edid,
                                                           slave_edid,
                                                           master_dpcd, low_power=False,
                                                           gfx_index=adapter.gfx_index) is False:
                logging.error(f"Failed to plug PR DP Tiled Display")
                gdhm.report_driver_bug_di(f"Failed to plug DP Tiled display")
                self.fail(f"DP Tiled display Plug failed")

            for panel in adapter.panels.values():
                if panel.pr_caps.is_pr_supported is False:
                    continue
                if panel.is_lfp:
                    continue
                if pr.is_enabled_in_driver(adapter, panel):
                    logging.error(f"PR enabled on Tiled Display {panel.port}")
                    gdhm.report_driver_bug_pc(f"PR enabled on Tiled Display")
                    self.fail("PR enable check failed")
            logging.info(f"PASS: PR not enabled on Tiled Display -{master_port} and {slave_port}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestConcurrency))
    test_environment.TestEnvironment.cleanup(test_result)
