########################################################################################################################
# @file         test_dc_state_concurrency.py
# @brief        Contains concurrency tests for DC State
# @details      Concurrency tests are covering below scenarios such as DRRS, DMRRS, CFPS, VRR, GAMMA
# @author       Tulika
########################################################################################################################

import logging
import unittest

from Libs.Core import enum
from DisplayRegs import get_interface
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.CFPS import cfps
from Tests.Color.Common import gamma_utility, color_constants
from Tests.Color.Common.common_utility import get_color_conversion_block
from Tests.Color.Common.gamma_utility import compare_ref_and_programmed_gamma_lut
from Tests.PowerCons.Functional.DCSTATES.dc_state import verify_dc6_vbi
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import DCStatesBase
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Modules import workload, dut, common
from Tests.VRR import vrr


##
# @brief        This class contains DC6 concurrency Tests
class TestConcurrency(DCStatesBase):

    ##
    # @brief        This function validates DC6 with RR features
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DRRS"])
    # @endcond
    def t_11_dc_state_drrs(self):
        status = True
        if workload.change_power_source(workload.PowerSource.DC_MODE) is False:
            self.fail("Failed to switch power line status to DC mode (Test Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                # PSR2 is requirement for DC6. DRRS on PSR2 panel is only possible on LRR1.0 panel.
                if panel.lrr_caps.is_lrr_1_0_supported is False:
                    self.fail(f"PSR2 supported panel {panel.port} does not support DRRS (Not LRR1.0 panel)")
                etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
                if etl_file is False:
                    self.fail("Failed to run the workload")
                logging.info(f"Step: Verifying DRRS on {panel.port}")
                status &= drrs.verify(adapter, panel, etl_file)
                logging.info(f"Step: Verifying DC6 on {panel.port}")
                status &= verify_dc6_vbi(etl_file)
                if status is False:
                    self.fail("FAIL: DC6 verification with DRRS")
                logging.info("PASS: DC6 verification with DRRS")

    ##
    # @brief        This function validates DC6 with DMRRS feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DMRRS"])
    # @endcond
    def t_12_dc_state_dmrrs(self):
        status = True
        if workload.change_power_source(workload.PowerSource.DC_MODE) is False:
            self.fail("Failed to switch power line status to DC mode (Test Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if panel.lrr_caps.is_lrr_supported is False:
                    self.fail(f"PSR2 supported panel {panel.port} does not support LRR, so no DMRRS")
                etl_file, _ = workload.run(workload.VIDEO_PLAYBACK, [dmrrs.MediaFps.FPS_24_000, 30], idle_after_wl=True)
                if etl_file is False:
                    self.fail("Failed to run the workload")
                logging.info(f"Step: Verifying DMRRS on {panel.port}")
                status &= dmrrs.verify(adapter, panel, etl_file, dmrrs.MediaFps.FPS_24_000)
                logging.info(f"Step: Verifying DC6 on {panel.port}")
                status &= verify_dc6_vbi(etl_file, psr_disable_expected=True)
                if status is False:
                    self.fail("FAIL: DC6 verification with DMRRS")
                logging.info("PASS: DC6 verification with DMRRS")

    ##
    # @brief        This function validates DC6 with CFPS feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CFPS"])
    # @endcond
    def t_13_dc_state_cfps(self):
        status = True
        for adapter in dut.adapters.values():
            if cfps.enable(adapter) is False:
                self.fail("FAILED to enable CFPS")
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if (panel.psr_caps.is_psr2_supported or panel.pr_caps.is_pr_supported) is False:
                    self.fail(f"Panel {panel.port} does not support PSR2/PR")
                etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.MovingRectangleApp, 30, True])
                # Ensure async flips
                if vrr.async_flips_present(etl_file) is False:
                    etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.Classic3DCubeApp, 30, True])
                    if vrr.async_flips_present(etl_file) is False:
                        self.fail("OS is NOT sending async flips")
                if etl_file is False:
                    self.fail("Failed to run the workload")
                logging.info(f"Step: Verifying CFPS for {panel.port}")
                status &= cfps.verify(adapter, etl_file)
                # When CFPS is enabled, VRR is disabled, so restoring VRR
                if adapter.is_vrr_supported is True:
                    if vrr.enable(adapter) is False:
                        self.fail("FAILED to enable VRR")
                logging.info(f"Step: Verifying DC6 for {panel.port}")
                status &= verify_dc6_vbi(etl_file)
                if status is False:
                    self.fail("FAIL: DC6 verification with CFPS")
                logging.info("PASS: DC6 verification with CFPS")

    ##
    # @brief        This function validates DC6 with VRR feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VRR"])
    # @endcond
    def t_14_dc_state_vrr(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if (panel.lrr_caps.is_lrr_2_0_supported or panel.lrr_caps.is_lrr_2_5_supported) is False:
                    self.fail(f"Panel {panel.port} doesn't support PSR2/VRR")
                etl_file, _ = workload.run(workload.GAME_PLAYBACK,
                                           [workload.Apps.Classic3DCubeApp, 30, True])
                # Ensure async flips
                if vrr.async_flips_present(etl_file) is False:
                    etl_file, _ = workload.run(workload.GAME_PLAYBACK,
                                               [workload.Apps.MovingRectangleApp, 30, True])
                    if vrr.async_flips_present(etl_file) is False:
                        self.fail("OS is NOT sending async flips")
                if etl_file is False:
                    self.fail("Failed to run the workload")
                logging.info(f"Step: Verifying VRR for {panel.port}")
                status &= vrr.verify(adapter, panel, etl_file)
                logging.info(f"Step: Verifying DC6 for {panel.port}")
                status &= verify_dc6_vbi(etl_file, psr_disable_expected=True)
                if status is False:
                    self.fail("FAIL: DC6 verification with VRR")
                logging.info("PASS: DC6 verification with VRR")

    ##
    # @brief        This function validates DC6 with Gamma
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["GAMMA"])
    # @endcond
    def t_15_dc_state_gamma(self):
        status = True
        reference_gamma_lut = color_constants.SRGB_ENCODE_515_SAMPLES_16BPC
        reference_gamma_lut = reference_gamma_lut[:-2]
        gamma_lut_size = 1024
        programmed_gamma_lut = []
        for adapter in dut.adapters.values():
            reg_interface = get_interface(adapter.name, adapter.gfx_index)
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue

                # Verify DC6
                logging.info(f"Step: Verifying DC6 for {panel.port}")
                etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
                if etl_file is False:
                    self.fail("Failed to run the workload")
                status &= verify_dc6_vbi(etl_file)

                # Verify Gamma
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
                logging.info(f"PASS: GAMMA verification on {panel.port} panel is success")
                if status is False:
                    self.fail("FAIL: DC6 verification with Gamma")
                logging.info("PASS: DC6 verification with Gamma")

    ##
    # @brief        This function validates DC6 with HW Rotation
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HW_ROTATION"])
    # @endcond
    def t_16_dc_state_hw_rotation(self):
        status = True
        rotation_list = [enum.ROTATE_270, enum.ROTATE_180, enum.ROTATE_90, enum.ROTATE_0]
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                current_mode = self.display_config_.get_current_mode(panel.target_id)

                try:
                    # Apply each rotation and verify DC6
                    for rotation in rotation_list:
                        current_mode.rotation = rotation
                        enumerated_displays = self.display_config_.get_enumerated_display_info()
                        logging.info(f"Step: Applying mode : {current_mode.to_string(enumerated_displays)}")
                        result = self.display_config_.set_display_mode([current_mode])
                        self.assertEquals(result, True, "Display mode set failed")
                        logging.info("\tPASS: Successfully applied mode")

                        # verify DC6 with HW Rotation
                        logging.info(f"Step: Verifying DC6 with rotation {rotation}")
                        etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
                        if etl_file is False:
                            self.fail("Failed to run the workload")
                        status &= verify_dc6_vbi(etl_file)
                        if status is False:
                            self.fail(f"\tFAIL: DC6 verification with HW ROTATION failed for {panel.port}")
                        logging.info(f"\tPASS: DC6 verification with HW ROTATION passed successfully for {panel.port} ")
                except Exception as e:
                    self.fail(e)
                finally:
                    current_mode = self.display_config_.get_current_mode(panel.target_id)
                    if current_mode.rotation == enum.ROTATE_0:
                        logging.info("HW_Rotation already set to zero")
                    else:
                        current_mode.rotation = enum.ROTATE_0
                        if self.display_config_.set_display_mode([current_mode], False) is False:
                            self.fail("FAILED to set display mode with Rotation 0")
                        logging.info("\tSuccessfully applied mode with Rotation 0")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestConcurrency))
    test_environment.TestEnvironment.cleanup(test_result)
