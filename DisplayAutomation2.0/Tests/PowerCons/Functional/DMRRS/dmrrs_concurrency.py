#######################################################################################################################
# @file         dmrrs_concurrency.py
# @brief        Test for DMRRS with concurrent features
#
# @author       Karthik Kurella
#######################################################################################################################
from enum import IntEnum

from Libs.Core.display_config import display_config_enums
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_environment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Feature.display_fbc import fbc
from Libs.Feature.vdsc import dsc_verifier
from Tests.PlanesUI.Common import planes_ui_verification
from Tests.Flips import flip_verification
from Tests.PowerCons.Modules import workload
from Tests.PowerCons.Functional.CFPS import cfps
from Tests.PowerCons.Functional.DMRRS.dmrrs_base import *
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Functional.PSR.psr import UserRequestedFeature
from Tests.PowerCons.Functional import pc_external
from Tests.VRR import vrr


##
# @brief        Enum maintained to have list of features to be used for respective concurrency test.
class Feature(IntEnum):
    NONE = 0
    FBC = 1
    LACE = 2
    VDSC = 3
    DPST = 4
    CFPS = 5
    ASYNC = 6
    FLIPQ = 7


##
# @brief        This class contains basic test cases for DMRRS
class DmrrsConcurrency(DmrrsBase):
    ##
    # @brief        This function verifies DMRRS with VDSC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VDSC"])
    # @endcond
    def t_11_dmrrs_vdsc(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.vdsc_caps.is_vdsc_supported is False:
                    self.fail("VDSC panel is not connected (Planning Issue)")
                if panel.psr_caps.is_psr2_supported:
                    if common.PLATFORM_NAME in common.PRE_GEN_13_PLATFORMS + ['DG2']:
                        logging.info("Target system is PreGen13+DG2. PSR2 needs to be disabled to enable VDSC")
                        psr_status = psr.disable(adapter.gfx_index, UserRequestedFeature.PSR_2)
                        if psr_status is False:
                            assert False, f"FAILED to disable PSR2 for {panel.port}"
                        if psr_status is True:
                            status, reboot_required = display_essential.restart_gfx_driver()
                            if status is False:
                                assert False, f"FAILED to restart display driver for {adapter.name}"

                media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000

                etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

                test_status &= dmrrs.verify(adapter, panel, etl_file_path, media_fps)
                test_status &= validate_concurrency(adapter, panel, etl_file_path, Feature.VDSC)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with VDSC")
        logging.info("PASS: DMRRS feature verification with VDSC")

    ##
    # @brief        This function verifies DMRRS with LACE
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LACE"])
    # @endcond
    def t_12_dmrrs_lace(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if adapter.name in ['TGL', 'DG1', 'DG2'] and panel.pipe == 'B':
                    logging.warning(f"LACE is not supported on PIPE {panel.pipe} on {panel.port}")
                    continue

                status, _ = pc_external.enable_disable_lace(adapter, panel, True, adapter.gfx_index)
                assert status, f"FAILED to enable LACE on {panel.pipe}"

                media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
                etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

                if etl_file_path is False:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file_path, media_fps)
                test_status &= validate_concurrency(adapter, panel, etl_file_path, Feature.LACE)

                status, _ = pc_external.enable_disable_lace(adapter, panel, False, adapter.gfx_index)
                assert status, f"FAILED to disable LACE on {panel.pipe}"

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with LACE")
        logging.info("PASS: DMRRS feature verification with LACE")

    ##
    # @brief        This function verifies DMRRS with HDR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HDR"])
    # @endcond
    def t_13_dmrrs_hdr(self):
        hdr_support = False
        test_status = True
        # HDR requires AC mode
        if workload.change_power_source(workload.PowerSource.AC_MODE) is False:
            self.fail("FAILED to switch power line status to AC (Test Issue)")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.hdr_caps.is_hdr_supported is False:
                    logging.info(f"HDR is not supported on {panel.port}")
                    continue
                hdr_support = True

                logging.info(f"Step: Verifying DMRRS with HDR enable on {panel.port}")
                # Enable HDR
                if pc_external.enable_disable_hdr([panel.port], True) is False:
                    self.fail(f"FAILED to enable HDR on {panel.port}")

                media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
                etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

                if etl_file_path is False:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file_path, media_fps)

        if hdr_support is False:
            self.fail("None of the panels support HDR(Planning Issue)")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.hdr_caps.is_hdr_supported is False:
                    continue
                logging.info(f"Step: Disable HDR on {panel.port}")
                # Disable HDR
                if pc_external.enable_disable_hdr([panel.port], False) is False:
                    self.fail(f"FAILED to disable HDR on {panel.port}")
                logging.info(f"PASS: HDR disable success on {panel.port}")

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with HDR")
        logging.info("PASS: DMRRS feature verification with HDR")

    ##
    # @brief        This function verifies DMRRS with FBC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FBC"])
    # @endcond
    def t_14_dmrrs_fbc(self):
        test_status = True

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000

                etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

                test_status &= dmrrs.verify(adapter, panel, etl_file_path, media_fps)
                test_status &= validate_concurrency(adapter, panel, etl_file_path, Feature.FBC)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with FBC")
        logging.info("PASS: DMRRS feature verification with FBC")

    ##
    # @brief        This function verifies DMRRS with DPST
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DPST"])
    # @endcond
    def t_15_dmrrs_dpst(self):
        test_status = True

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000

                etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

                test_status &= dmrrs.verify(adapter, panel, etl_file_path, media_fps)
                test_status &= validate_concurrency(adapter, panel, etl_file_path, Feature.DPST)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with DPST")
        logging.info("PASS: DMRRS feature verification with DPST")

    ##
    # @brief        This function validates DMRRS with CFPS feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CFPS"])
    # @endcond
    def t_16_dmrrs_cfps(self):
        test_status = True
        for adapter in dut.adapters.values():
            if cfps.enable(adapter) is False:
                self.fail("FAILED to enable CFPS")
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                etl_file_path, status = cfps.run_workload(full_screen=True)
                if status is False:
                    self.fail("FAILED to run the workload for CFPS")
                test_status &= validate_concurrency(adapter, panel, etl_file_path, Feature.CFPS)
                # DMRRS non-zero duration is not expected with Game playback
                if dmrrs.is_non_zero_duration_flip_present(panel, etl_file_path):
                    test_status &= False
                # When CFPS is enabled, VRR is disabled, so restoring VRR
                if adapter.is_vrr_supported is True:
                    if vrr.enable(adapter) is False:
                        self.fail("FAILED to enable VRR")

        if test_status is False:
            self.fail("FAIL:DMRRS feature verification with CFPS")
        logging.info("PASS: DMRRS feature verification with CFPS")

    ##
    # @brief        This function validates DMRRS with ASYNC feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["ASYNC"])
    # @endcond
    def t_17_dmrrs_async(self):
        test_status = True
        if workload.change_power_source(workload.PowerSource.DC_MODE) is False:
            self.fail("FAILED to switch power line status to DC (Test Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000

                etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])
                test_status &= dmrrs.verify(adapter, panel, etl_path=etl_file_path, media_fps=media_fps)
                test_status &= validate_concurrency(adapter, panel, etl_file_path, Feature.ASYNC)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with ASYNC")
        logging.info("PASS: DMRRS feature verification with ASYNC")

    ##
    # @brief        This function validates FBC with H/W Rotation
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HW_ROTATION"])
    # @endcond
    def t_18_dmrrs_rotation(self):
        rotation_list = [enum.ROTATE_270, enum.ROTATE_180, enum.ROTATE_90, enum.ROTATE_0]
        test_status = True

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                current_mode = self.display_config_.get_current_mode(panel.target_id)
                # Apply each rotation and verify DMRRS
                for rotation in rotation_list:
                    current_mode.rotation = rotation
                    enumerated_displays = self.display_config_.get_enumerated_display_info()
                    logging.info(f"Applying mode= {current_mode.to_string(enumerated_displays)}")
                    result = self.display_config_.set_display_mode([current_mode])
                    self.assertEquals(result, True, "display mode set failed")
                    logging.info("PASS: Successfully applied mode")
                    # verify DMRRS with HW Rotation
                    logging.info(f"Step: Verifying DMRRS with rotation {display_config_enums.Rotation(rotation).name}")

                    media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
                    etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])
                    test_status &= dmrrs.verify(adapter, panel, etl_path=etl_file_path, media_fps=media_fps)

        if test_status is False:
            self.fail(f"FAIL: DMRRS verification with HW Rotation")
        logging.info(f"PASS: FBC verification with HW Rotation")

    ##
    # @brief        This function validates DMRRS with FLIPQ feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FLIPQ"])
    # @endcond
    def t_19_dmrrs_flipq(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue

                media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
                etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])
                test_status &= dmrrs.verify(adapter, panel, etl_file_path, media_fps=media_fps)
                test_status &= validate_concurrency(adapter, panel, etl_file_path, Feature.FLIPQ)

        if test_status is False:
            self.fail("FAIL:DMRRS feature verification with FLIPQ")
        logging.info("PASS: DMRRS feature verification with FLIPQ")


##
# @brief        Helper function to validate the DMRRS With Concurrent features
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @param[in]    etl_path String path to etl file
# @param[in]    concurrent_feature enum, Feature to be verified for concurrency
# @return       True if successful, False otherwise
def validate_concurrency(adapter: Adapter, panel: Panel, etl_path: str,
                         concurrent_feature: Feature = Feature.NONE):

    concurrent_feature_name = Feature(concurrent_feature).name
    logging.info(f"Verifying {concurrent_feature_name} for "
                 f"{panel.port}(PIPE_{panel.pipe}) on {adapter.gfx_index}")
    feature_status = True
    if concurrent_feature == Feature.FBC:
        feature_status &= fbc.verify_adapter_fbc(adapter.gfx_index)
    elif concurrent_feature == Feature.LACE:
        feature_status &= pc_external.get_lace_status(adapter, panel)
    elif concurrent_feature == Feature.DPST:
        feature_status &= dpst.verify(adapter, panel, etl_path)
    elif concurrent_feature == Feature.VDSC:
        feature_status &= dsc_verifier.verify_dsc_programming(adapter.gfx_index, panel.port)
    elif concurrent_feature == Feature.CFPS:
        feature_status &= cfps.verify(adapter, etl_path)
    elif concurrent_feature == Feature.ASYNC:
        etl_file_path, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.MovingRectangleApp, 30, True])
        feature_status &= flip_verification.verify_asyncflips(etl_file_path, panel.pipe)
    elif concurrent_feature == Feature.FLIPQ:
        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [24, 30, True])
        feature_status &= planes_ui_verification.verify_flipq(etl_file_path, panel.pipe, panel.target_id, adapter.name)

    logging_str = f"{concurrent_feature_name} verification for {panel.port}(PIPE_{panel.pipe})"
    if feature_status is False:
        logging.error(f"FAIL: {logging_str}")
        return False
    logging.info(f"PASS: {logging_str}")

    return True


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DmrrsConcurrency))
    test_environment.TestEnvironment.cleanup(test_result)
