########################################################################################################################
# @file         cfps_concurrency.py
# @brief        Contains concurrency tests for CFPS
# @details      Concurrency tests are covering below scenarios:
#               * CFPS and HDR
#               * CFPS and FBC
#               * CFPS and Render Compression
#               * CFPS and MPO
#               * CFPS and FlipQ
#               * CFPS and HW Rotation
#               * CFPS and Pipe Scaling
#
# @author       Pai,Vinayak1
########################################################################################################################
from operator import attrgetter

from Libs.Core import registry_access
from Libs.Core.display_config import display_config
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Decompression.Playback.decomp_verifier import is_feature_supported, INTEL_GMM_PATH
from Tests.PowerCons.Functional.CFPS.cfps_base import *
from Tests.PowerCons.Functional.FBC.fbc_base import check_fbc_support


##
# @brief        Exposed Class to write CFPS concurrency tests. This class inherits the CfpsBase class.
#               Any new concurrency test can inherit this class to use common setUp and tearDown functions.
class CfpsConcurrency(CfpsBase):

    ############################
    # Test Functions
    ############################

    ##
    # @brief        Test function to check if CFPS is working with FBC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FBC"])
    # @endcond
    def t_41_fbc(self):
        fbc_support = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if check_fbc_support(adapter, panel) is False:
                    continue
                fbc_support = True

                status = self.validate_cfps(True, None, cfps.Feature.FBC)
                if status is False:
                    self.fail("FAIL: CFPS feature verification with FBC")
                logging.info("PASS: CFPS feature verification with FBC")

        if fbc_support is False:
            self.fail("\tFAIL: None of the panels support FBC(Planning Issue)")

    ##
    # @brief        Test function to check if CFPS is working with Render Compression
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["RENDER_DECOMPRESSION"])
    # @endcond
    def t_42_render_decompression(self):
        render_compression_support = False
        for adapter in dut.adapters.values():
            if is_feature_supported("RENDER_DECOMP") is False:
                continue
            render_compression_support = True
            for panel in adapter.panels.values():
                # Verify Render Decompression
                logging.info(f"\tStep: Verifying Render Decompression")
                if self.get_e2e_compression_status(adapter) is False:
                    self.fail("\tFAIL: E2ECompression is disabled")
                status = self.validate_cfps(True, None, cfps.Feature.RENDER_DECOMPRESSION)
                if status is False:
                    self.fail("FAIL: CFPS feature verification with RENDER DECOMPRESSION")
                logging.info("PASS: CFPS feature verification with RENDER DECOMPRESSION")

        if render_compression_support is False:
            self.fail("\tFAIL: None of the adapter support Render DeCompression(Planning Issue)")

    ##
    # @brief        Test function to check if CFPS is working with MPO Formats
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MPO"])
    # @endcond
    def t_43_mpo(self):
        etl_file, _ = cfps.run_workload(False, None)
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status = self.validate_cfps(True, None, cfps.Feature.MPO)
                if status is False:
                    self.fail("FAIL: CFPS feature verification with MPO")
                logging.info("PASS: CFPS feature verification with MPO")

    ##
    # @brief        Test function to check if CFPS is working with HDR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HDR"])
    # @endcond
    def t_44_hdr(self):
        # Check Powerline status
        if self.display_power_.set_current_powerline_status(display_power.PowerSource.AC) is False:
            self.fail("\tFAIL: Failed to switch power line status to AC (Test Issue)")

        hdr_support = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.hdr_caps.is_hdr_supported is False:
                    continue
                hdr_support = True

                # Enable HDR
                logging.info(f"Step: Enable HDR on {panel.port}")
                if pc_external.enable_disable_hdr([panel.port], True) is False:
                    self.fail(f"\tFAIL: Failed to enable HDR on {panel.port}")

                status = self.validate_cfps(True, None, cfps.Feature.HDR)
                if status is False:
                    self.fail("FAIL: CFPS feature verification with HDR")
                logging.info("PASS: CFPS feature verification with HDR")

                # Disable HDR
                logging.info(f"Step : Disable HDR on {panel.port}")
                if pc_external.enable_disable_hdr([panel.port], False) is False:
                    self.fail(f"\tFAIL: Failed to disable HDR on {panel.port}")
                logging.info(f"PASS: HDR disable success on {panel.port}")

        if hdr_support is False:
            self.fail("None of the panels support HDR(Planning Issue)")

    ##
    # @brief        Test function to check if CFPS is working with HW Rotation
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HW_ROTATION"])
    # @endcond
    def t_45_hw_rotation(self):
        rotation_list = [enum.ROTATE_270, enum.ROTATE_180, enum.ROTATE_90, enum.ROTATE_0]
        etl_file, _ = cfps.run_workload(True, None)
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                current_mode = self.display_config_.get_current_mode(panel.target_id)

                # Apply each rotation and verify CFPS
                for rotation in rotation_list:
                    current_mode.rotation = rotation
                    enumerated_displays = self.display_config_.get_enumerated_display_info()
                    logging.info(f"Step: Applying mode : {current_mode.to_string(enumerated_displays)}")
                    result = self.display_config_.set_display_mode([current_mode])
                    self.assertEquals(result, True, "display mode set failed")
                    logging.info("\tPASS: Successfully applied mode")

                    # verify CFPS with HW Rotation
                    logging.info(f"Step: Verifying CFPS with rotation {rotation}")
                    if cfps.verify(adapter, etl_file) is False:
                        self.fail(f"\tFAIL: CFPS verification on {panel.port}")
                    logging.info(f"\tPASS: CFPS verification with HW ROTATION passed successfully on {panel.port} ")

    ##
    # @brief        Test function to check if CFPS is working with FlipQ
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FLIPQ"])
    # @endcond
    def t_46_flipq(self):
        status = self.validate_cfps(True, None, cfps.Feature.FLIPQ)
        if status is False:
            self.fail("FAIL: CFPS feature verification with FLIPQ")
        logging.info("PASS: CFPS feature verification with FLIPQ")

    ##
    # @brief        Test function to check if CFPS is working with Pipe scaling
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PIPE_SCALAR"])
    # @endcond
    def t_47_scaling(self):
        status = True
        display_config_ = display_config.DisplayConfiguration()
        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                all_supported_modes = display_config_.get_all_supported_modes([panel.target_id])
                mode_with_mar = None
                for _, modes in all_supported_modes.items():
                    modes = sorted(modes, key=attrgetter('HzRes', 'refreshRate'))
                    for mode in modes:
                        if mode.scaling == enum.MAR:
                            mode_with_mar = mode
                            break

                if mode_with_mar is None:
                    logging.error(f"FAILED to get supported mode with MAR for {panel.port}")
                    status &= False
                    continue
                logging.info(f"Native mode with MAR for {panel.port}= {mode_with_mar.HzRes}x{mode_with_mar.VtRes}")
                status &= display_config_.set_display_mode([mode_with_mar], False)
                status &= self.validate_cfps(True, None, cfps.Feature.PIPE_SCALAR)
                status &= common.set_native_mode(panel)
                if status is False:
                    self.fail("FAIL: CFPS feature verification with PIPE SCALAR")
                logging.info("PASS: CFPS feature verification with PIPE SCALAR")

    ############################
    # Helper Functions
    ############################

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
    test_result = runner.run(common.get_test_suite(CfpsConcurrency))
    TestEnvironment.cleanup(test_result)