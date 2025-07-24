########################################################################################################################
# @file         drrs_concurrency.py
# @brief        Test for DRRS with concurrent features
#
# @author       Karthik Kurella
########################################################################################################################
from enum import IntEnum

from Libs.Core import enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.test_env import test_environment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Feature.vdsc import dsc_verifier
from Tests.PowerCons.Modules.dut_context import Adapter, Panel
from Tests.PowerCons.Modules import workload
from Tests.PlanesUI.Common import planes_ui_verification
from Tests.Flips import flip_verification
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.BLC import blc
from Tests.PowerCons.Functional.CFPS import cfps
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Functional.PSR.psr import UserRequestedFeature
from Tests.VRR import vrr
from Tests.PowerCons.Functional.DRRS.drrs_base import *


##
# @brief        Enum maintained to have list of features to be used for respective concurrency test.
class Feature(IntEnum):
    NONE = 0
    FBC = 1
    HDR = 2
    LACE = 3
    CFPS = 5
    VDSC = 6
    MPO = 7
    VRR = 8
    ASYNC = 9
    DMRRS = 10
    FLIPQ = 11
    HW_ROTATION = 12


##
# @brief        This class contains basic test cases for DRRS
class DrrsConcurrency(DrrsBase):
    ##
    # @brief        This function verifies DRRS with VDSC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VDSC"])
    # @endcond
    def t_11_drrs_vdsc(self):
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
                            self.fail(f"FAILED to disable PSR2 for {panel.port}")
                        if psr_status is True:
                            status, reboot_required = display_essential.restart_gfx_driver()
                            if status is False:
                                self.fail(f"FAILED to restart display driver for {adapter.name}")

                etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])

                test_status &= drrs.verify(adapter, panel, etl_path=etl_file)

                test_status &= validate_concurrency(adapter, panel, etl_file, Feature.VDSC)

        if test_status is False:
            self.fail("FAIL: DRRS feature verification with VDSC")
        logging.info("PASS: DRRS feature verification with VDSC")

    ##
    # @brief        This function verifies DRRS with HDR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HDR"])
    # @endcond
    def t_12_drrs_hdr(self):
        hdr_support = False
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if panel.drrs_caps.is_drrs_supported is False:
                    self.fail("DRRS supported panel is not connected (Planning Issue)")
                if panel.hdr_caps.is_hdr_supported is False:
                    logging.info(f"HDR is not supported on {panel.port}")
                    continue
                hdr_support = True
                logging.info(f"STEP: Verify DRRS with HDR enable on {panel.port}")
                # Enable HDR
                if blc.enable_hdr(adapter) is False:
                    self.fail(f"FAILED to enable HDR on {panel.port}")

                logging.info(f"Step: Verify DRRS with HDR enable for {panel.port}")

                monitors = app_controls.get_enumerated_display_monitors()
                monitor_ids = [_[0] for _ in monitors]
                if self.method == 'IDLE':
                    etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
                else:
                    etl_file, _ = workload.run(workload.SCREEN_UPDATE, [monitor_ids])

                if etl_file is False:
                    self.fail("FAILED to run the workload")

                test_status &= drrs.verify(adapter, panel, etl_file)

                logging.info(f"Step: Disabling HDR for {panel.port}")
                # Disable HDR
                if blc.disable_hdr(adapter, panel) is False:
                    self.fail(f"FAILED to disable HDR on {panel.port}")
                logging.info(f"PASS: HDR disable success on {panel.port}")
        if hdr_support is False:
            self.fail("None of the panels support HDR(Planning Issue)")

        if test_status is False:
            self.fail(f"FAIL : DRRS verification with HDR")
        logging.info(f"PASS : DRRS verification with HDR")

    ##
    # @brief        Function to verify co-existence of DRRS with MPO scenario
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['MPO'])
    # @endcond
    def t_13_drrs_mpo(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30, False, False, True])
                test_status &= drrs.verify(adapter, panel, etl_path=etl_file)

                test_status &= validate_concurrency(adapter, panel, etl_file, Feature.MPO)

        if test_status is False:
            self.fail("FAIL: DRRS feature verification with MPO")
        logging.info("PASS: DRRS feature verification with MPO")

    ##
    # @brief        This function validates DRRS with CFPS feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CFPS"])
    # @endcond
    def t_14_drrs_cfps(self):
        test_status = True
        for adapter in dut.adapters.values():
            if cfps.enable(adapter) is False:
                self.fail(f"Failed to enable CFPS on {adapter.name}")
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                etl_file, status = cfps.run_workload(full_screen=True)
                if status is False:
                    self.fail("FAILED to run the workload for CFPS")
                # Game-playback will include ControlInterrupt2 Enable/ Disable
                test_status &= drrs.verify(adapter, panel, etl_path=etl_file)
                test_status &= validate_concurrency(adapter, panel, etl_file, Feature.CFPS)

            # When CFPS is enabled, VRR is disabled, so restoring VRR state to default
            if adapter.is_vrr_supported is True:
                if vrr.enable(adapter) is False:
                    self.fail("FAILED to enable VRR")

        if test_status is False:
            self.fail("FAILED to verify DRRS with CFPS")
        logging.info("Successfully verified DRRS with CFPS")

    ##
    # @brief        This function validates DRRS with VRR feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VRR"])
    # @endcond
    def t_15_drrs_vrr(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if not panel.vrr_caps.is_vrr_supported:
                    self.fail(f"Panel {panel.port} doesn't support VRR")
                etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
                test_status &= drrs.verify(adapter, panel, etl_path=etl_file)
                test_status &= validate_concurrency(adapter, panel, etl_file, Feature.VRR)
        if test_status is False:
            self.fail("FAIL: DRRS feature verification with VRR")
        logging.info("PASS: DRRS feature verification with VRR")

    ##
    # @brief        This function validates DRRS with ASYNC feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["ASYNC"])
    # @endcond
    def t_16_drrs_async(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])

                test_status &= drrs.verify(adapter, panel, etl_path=etl_file)
                test_status &= validate_concurrency(adapter, panel, etl_file, Feature.ASYNC)

        if test_status is False:
            self.fail("FAIL: DRRS feature verification with Async")
        logging.info("PASS: DRRS feature verification with Async")

    ##
    # @brief        This function validates DRRS with DMRRS feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DMRRS"])
    # @endcond
    def t_16_drrs_dmrrs(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if panel.drrs_caps.is_dmrrs_supported:
                    etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
                    test_status &= drrs.verify(adapter, panel, etl_file)
                    test_status &= validate_concurrency(adapter, panel, etl_file, Feature.DMRRS)
                else:
                    self.fail(f"Panel {panel.port} doesn't support DMRRS(Test Issue)")
        if test_status is False:
            self.fail("FAIL: DRRS feature verification with DMRRS")
        logging.info("PASS: DRRS feature verification with DMRRS")

    ##
    # @brief        This function validates DRRS with FLIPQ feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FLIPQ"])
    # @endcond
    def t_16_drrs_flipq(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
                test_status &= drrs.verify(adapter, panel, etl_file)
                test_status &= validate_concurrency(adapter, panel, etl_file, Feature.FLIPQ)

        if test_status is False:
            self.fail("FAIL: DRRS feature verification with FLIPQ")
        logging.info("PASS: DRRS feature verification with FLIPQ")

    ##
    # @brief        This function validates DRRS with HW_ROTATION feature
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HW_ROTATION"])
    # @endcond
    def t_17_drrs_hw_rotation(self):
        test_status = True
        rotation_list = [enum.ROTATE_270, enum.ROTATE_180, enum.ROTATE_90, enum.ROTATE_0]
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                display_config_ = DisplayConfiguration()
                current_mode = display_config_.get_current_mode(panel.target_id)
                # Apply each rotation and verify DRRS
                for rotation in rotation_list:
                    current_mode.rotation = rotation
                    enumerated_displays = display_config_.get_enumerated_display_info()
                    logging.info(f"STEP: Applying mode : {current_mode.to_string(enumerated_displays)}")
                    result = display_config_.set_display_mode([current_mode])
                    self.assertEquals(result, True, "display mode set failed")
                    logging.info("PASS: Successfully applied mode")
                    # verify DRRS with HW Rotation
                    logging.info(f"STEP: Verifying DDRS with rotation {rotation}")

                    etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
                    test_status &= drrs.verify(adapter, panel, etl_file)

        if test_status is False:
            self.fail(f"FAIL: DRRS verification with HW_ROTATION")
        logging.info(f"PASS: DRRS verification with HW_ROTATION")


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
    if concurrent_feature == Feature.LACE:
        feature_status &= pc_external.get_lace_status(adapter, panel)
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
    elif concurrent_feature == Feature.MPO:
        feature_status &= pc_external.verify_mpo(adapter, panel, etl_path)
    elif concurrent_feature == Feature.VRR:
        etl_file_path, _ = workload.run(workload.GAME_PLAYBACK,
                                        [workload.Apps.Classic3DCubeApp, 30, True])
        # The above workload with Classic3DCubeApp was seen a sporadic failures on OS
        # The workload with MovingRectangleApp is used as latest to ensure asyncflip from OS[double check].
        # Ensure async flips
        if vrr.async_flips_present(etl_file_path) is False:
            etl_file_path, _ = workload.run(workload.GAME_PLAYBACK,
                                            [workload.Apps.MovingRectangleApp, 30, True])
        if vrr.async_flips_present(etl_file_path) is False:
            logging.error("OS is NOT sending async flips")
        logging.info("Step: Verifying VRR for {0}".format(panel.port))
        feature_status &= vrr.verify(adapter, panel, etl_file_path)
    elif concurrent_feature == Feature.DMRRS:
        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [dmrrs.MediaFps.FPS_24_000, 30, False, False,
                                                                  None, None, True])
        feature_status &= dmrrs.verify(adapter, panel, etl_file_path, dmrrs.MediaFps.FPS_24_000)
    logging_str = f"{concurrent_feature_name} verification for {panel.port}(PIPE_{panel.pipe})"
    if feature_status is False:
        logging.error(f"FAIL: {logging_str}")
        return False
    else:
        logging.info(f"PASS: {logging_str}")

        return True


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DrrsConcurrency))
    test_environment.TestEnvironment.cleanup(test_result)
