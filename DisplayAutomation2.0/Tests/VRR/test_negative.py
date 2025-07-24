########################################################################################################################
# @file         test_negative.py
# @brief        Contains negative tests for VRR
# @details      Negative tests are covering below scenarios:
#               * With VRR reg keys enabled, VRR should not get enabled on Non-VRR panel
#               * With VRR reg keys enabled, VRR should not get enabled on only sync flips
#               * With VRR reg keys enabled, With Active RR = Min RR, VRR should not get enabled
#               * With VRR reg keys disabled, VRR should not get enabled on Async/VRR flips
#               * Check for Under-run and TDR in all above scenarios
#
# @author       Rohit Kumar
########################################################################################################################
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VRR.vrr_base import *


##
# @brief        This class contains negative VRR tests. This class inherits the VrrBase class.
class TestNegative(VrrBase):

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        Verification with Non-VRR panel
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["NON_VRR"])
    # @endcond
    def t_41_non_vrr_panel(self):
        if self.verify_vrr(True, negative=True, expected_vrr=False) is False:
            self.fail("Negative VRR verification failed with Non-VRR panel")

    logging.info("\tPASS: Negative VRR verification passed successfully with Non-VRR panel")

    ##
    # @brief        Verification with Sync Flips
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VRR", "SYNC_FLIPS"])
    # @endcond
    def t_42_sync_flips(self):
        is_os_aware_vrr = dut.WIN_OS_VERSION >= dut.WinOsVersion.WIN_19H1

        # 15 seconds normal activity on desktop for sync flips
        etl_file, _ = workload.run(workload.IDLE_DESKTOP, [15])

        # verify
        status = True
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                status &= vrr.verify(
                    adapter, panel, etl_file, negative=True, os_aware_vrr=is_os_aware_vrr, expected_vrr=False)

        if status is False:
            self.fail("Negative VRR verification failed with Sync flips")
        logging.info("\tPASS: Negative VRR verification passed successfully with Sync Flips")

    ##
    # @brief        Verification for switch between min RR and max RR in Full Screen
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VRR", "MIN_RR"])
    # @endcond
    def t_43_min_rr(self):
        # Switch to min RR
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                mode = common.get_display_mode(panel.target_id, panel.min_rr)
                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("\tSuccessfully applied display mode")
                html.step_end()
            dut.refresh_panel_caps(adapter)

        status = self.verify_vrr(True, negative=True, expected_vrr=False)

        # Switch back to max RR
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                mode = common.get_display_mode(panel.target_id, panel.max_rr)
                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("\tSuccessfully applied display mode")
            dut.refresh_panel_caps(adapter)

        if status is False:
            self.fail("\tFAIL: Negative VRR verification failed with min RR")
        logging.info("\tPASS: Negative VRR verification passed successfully with min RR")

    ##
    # @brief        Verification for switch between min RR and max RR in Fullscreen
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MINRR_BETWEEN_PANELMIN_AND_MRLMIN"])
    # @endcond
    def t_44_min_rr_between_panel_min_and_mrl_min(self):
        # Switch to min RR
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                for rr in common.get_supported_refresh_rates(panel.target_id):
                    if rr in range(panel.min_rr+1, panel.vrr_caps.vrr_min_rr):
                        rr_mode = common.get_display_mode(panel.target_id, rr)
                        current_mode = common.display_config_.get_current_mode(panel.display_info.DisplayAndAdapterInfo)
                        if (rr_mode.HzRes, rr_mode.VtRes) != (current_mode.HzRes, rr_mode.VtRes):
                            continue
                        if self.display_config_.set_display_mode([rr_mode], False) is False:
                            assert False, "Failed to apply display mode (Test Issue)"
                        break
        logging.info("\tPASS: Successfully applied display mode")

        status = self.verify_vrr(True, negative=True, expected_vrr=False)
        if status is True:
            logging.info("\tPASS: Negative VRR verification passed successfully with min RR")

        # Switch back to max RR
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                max_rr_mode = common.get_display_mode(panel.target_id, panel.max_rr)
                if self.display_config_.set_display_mode([max_rr_mode], False) is False:
                    assert False, "Failed to apply display mode (Test Issue)"
                logging.info("\tPASS: Successfully applied display mode")

        if status is False:
            self.fail("Negative VRR verification failed with min RR")

    ##
    # @brief        Verification for VRR working in case of MRL max RR less than panel Max RR in Fullscreen
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MAX_RR_MRL_LESS"])
    # @endcond
    def t_45_max_rr(self):
        # Switch max RR
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                if panel.max_rr <= panel.vrr_caps.vrr_max_rr:
                    self.fail("Panel Max RR should be greater than MRL Max RR for this test")
                max_rr_mode = common.get_display_mode(panel.target_id, panel.max_rr)
                if self.display_config_.set_display_mode([max_rr_mode], False) is False:
                    assert False, "Failed to apply display mode (Test Issue)"
                logging.info("\tPASS: Successfully applied display mode")

                if panel.hdmi_2_1_caps.is_hdmi_2_1_pcon or panel.hdmi_2_1_caps.is_hdmi_2_1_native:
                    status = self.verify_vrr(True, negative=False, expected_vrr=True)
                    if status is False:
                        self.fail("Positive VRR verification failed with max RR greater than MRL max RR")
                    logging.info(
                        "\tPASS: positive VRR verification passed successfully with max RR greater than MRL Max RR")
                else:
                    status = self.verify_vrr(True, negative=True, expected_vrr=False)
                    if status is False:
                        self.fail("Negative VRR verification failed with max RR greater than MRL max RR")
                    logging.info(
                        "\tPASS: Negative VRR verification passed successfully with max RR greater than MRL Max RR")

    ##
    # @brief        Verification for switch between min RR and max RR in Windowed mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MIN_RR_WINDOWED"])
    # @endcond
    def t_46_min_rr(self):
        # Switch to min RR
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                mode = common.get_display_mode(panel.target_id, panel.min_rr)
                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("\tSuccessfully applied display mode")
                html.step_end()

        status = self.verify_vrr(False, negative=True, expected_vrr=False)

        # Switch back to max RR
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                mode = common.get_display_mode(panel.target_id, panel.max_rr)
                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("\tSuccessfully applied display mode")

        if status is False:
            self.fail("\tFAIL: Negative VRR verification failed with min RR")
        logging.info("\tPASS: Negative VRR verification passed successfully with min RR")

    ##
    # @brief        Verification for switch between min RR and max RR in Windowed mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MINRR_BETWEEN_PANELMIN_AND_MRLMIN_WINDOWED"])
    # @endcond
    def t_47_min_rr_between_panel_min_and_mrl_min(self):
        # Switch to min RR
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                for rr in common.get_supported_refresh_rates(panel.target_id):
                    if rr in range(panel.min_rr+1, panel.vrr_caps.vrr_min_rr):
                        rr_mode = common.get_display_mode(panel.target_id, rr)
                        current_mode = common.display_config_.get_current_mode(panel.display_info.DisplayAndAdapterInfo)
                        if (rr_mode.HzRes, rr_mode.VtRes) != (current_mode.HzRes, rr_mode.VtRes):
                            continue
                        if self.display_config_.set_display_mode([rr_mode], False) is False:
                            assert False, "Failed to apply display mode (Test Issue)"
                        break
        logging.info("\tPASS: Successfully applied display mode")

        status = self.verify_vrr(False, negative=True, expected_vrr=False)
        if status is True:
            logging.info("\tPASS: Negative VRR verification passed successfully with min RR")

        # Switch back to max RR
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                max_rr_mode = common.get_display_mode(panel.target_id, panel.max_rr)
                if self.display_config_.set_display_mode([max_rr_mode], False) is False:
                    assert False, "Failed to apply display mode (Test Issue)"
                logging.info("\tPASS: Successfully applied display mode")

        if status is False:
            self.fail("Negative VRR verification failed with min RR")

    ##
    # @brief        Verification for VRR working in case of MRL max RR less than panel Max RR in windowed mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MAX_RR_MRL_LESS_WINDOWED"])
    # @endcond
    def t_48_max_rr(self):
        # Switch max RR
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                if panel.max_rr <= panel.vrr_caps.vrr_max_rr:
                    self.fail("Panel Max RR should be greater than MRL Max RR for this test")
                max_rr_mode = common.get_display_mode(panel.target_id, panel.max_rr)
                if self.display_config_.set_display_mode([max_rr_mode], False) is False:
                    assert False, "Failed to apply display mode (Test Issue)"
                logging.info("\tPASS: Successfully applied display mode")

                if panel.hdmi_2_1_caps.is_hdmi_2_1_pcon or panel.hdmi_2_1_caps.is_hdmi_2_1_native:
                    status = self.verify_vrr(False, negative=False, expected_vrr=True)
                    if status is False:
                        self.fail("positive VRR verification failed with max RR greater than MRL max RR")
                    logging.info(
                        "\tPASS: positive VRR verification passed successfully with max RR greater than MRL Max RR")
                else:
                    status = self.verify_vrr(True, negative=True, expected_vrr=False)
                    if status is False:
                        self.fail("Negative VRR verification failed with max RR greater than MRL max RR")
                    logging.info(
                        "\tPASS: Negative VRR verification passed successfully with max RR greater than MRL Max RR")

    ##
    # @brief        Verification for VRR panel without MRL block
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["NO_MRL"])
    # @endcond
    def t_49_no_mrl(self):
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                # VRR should work for NoMRL for LFP, and should not for external display
                if panel.is_lfp is True:
                    if self.verify_vrr(True, negative=False, expected_vrr=True) is False:
                        self.fail("VRR verification failed with No MRL eDP panel")
                    logging.info("\tPASS: VRR verification passed successfully with No MRL eDP Panel")
                else:
                    if self.verify_vrr(True, negative=True, expected_vrr=False) is False:
                        self.fail("Negative VRR verification failed with No MRL")
                    logging.info("\tPASS: Negative VRR verification passed successfully with No MRL")

    ##
    # @brief        Intel Arc Sync verification on non VRR panel
    # @return       None
    # @cond
    @common.configure_test(selective=["NON_VRR"])
    # @endcond
    def t_49_arc_sync_non_vrr_panel(self):
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            if adapter.name in PRE_GEN_13_PLATFORMS:
                continue
            for panel in adapter.panels.values():
                # Verification intended only for Non VRR panels
                if panel.vrr_caps.is_vrr_supported:
                    continue
                panel_args = vrr.get_arc_sync_config(panel)
                if not panel_args:
                    self.fail("Get Monitor config failed for Non-VRR panel")
                if panel_args.IsIntelArcSyncSupported:
                    gdhm.report_driver_bug_os("VRR support showing True in Non-VRR panel from Arc Sync config call")
                    self.fail("VRR support showing True in Non-VRR panel from Arc Sync config call")
                if (vrr.get_current_profile(panel, expected_fail=True) or
                        vrr.set_profile(panel, profile=ARC_SYNC_PROFILE.EXCELLENT, expected_fail=True)):
                    self.fail("Get profile and set profile calls not expected to pass for non VRR panel")
        logging.info("\tPASS: Negative VRR verification passed successfully with Non-VRR panel")

    ##
    # @brief        VRR verification with VRR disabled
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VRR", "ASYNC_FLIPS"])
    # @endcond
    def t_51_async_flips(self):
        if self.verify_vrr(True, negative=True, expected_vrr=False) is False:
            self.fail("Negative VRR verification failed with VRR disabled")

        logging.info("\tPASS: Negative VRR verification passed successfully with VRR disabled")

    ##
    # @brief        Intel Arc Sync verification on VRR panel with disable VRR
    # @return       None
    # @cond
    @common.configure_test(selective=["VRR"])
    # @endcond
    def t_52_arc_sync_non_vrr_panel(self):
        vrr_panel_planned = False
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False or adapter.name in PRE_GEN_13_PLATFORMS:
                continue
            for panel in adapter.panels.values():
                if panel.vrr_caps.is_vrr_supported:
                    vrr_panel_planned = True
            if vrr_panel_planned is False:
                logging.error("At least one VRR panel require for this test case, planned at least one VRR panel")
                self.fail("At least one VRR panel require for this test case, planned at least one VRR panel")
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False or adapter.name in PRE_GEN_13_PLATFORMS:
                continue
            for panel in adapter.panels.values():
                # Verification intended only for VRR panels
                if not panel.vrr_caps.is_vrr_supported:
                    logging.info(f"Ignoring {panel.port} for Non VRR panel")
                    continue
                # get current profile
                current_profile = vrr.get_current_profile(panel)
                if current_profile is False:
                    logging.error(f"Failed to get current profile for {panel.port}")
                    self.fail("Failed to get current profile")
                if current_profile.IntelArcSyncProfile.value != ARC_SYNC_PROFILE.OFF:
                    logging.error(f"Profile is not set to OFF for VRR panel after disable VRR")
                    gdhm.report_driver_bug_os(f"[OsFeatures][VRR] Profile is not set to OFF for VRR panel "
                                              f"after disable VRR")
                    self.fail("Profile is not set to OFF")
                # set profile to excellent
                if vrr.set_profile(panel, profile=ARC_SYNC_PROFILE.EXCELLENT) is False:
                    logging.error(f"Failed to set Excellent profile for {panel.port}")
                    self.fail(f"Failed to set Excellent profile for {panel.port}")
                # after setting profile as well, in case of disable we should get off profile.
                current_profile = vrr.get_current_profile(panel)
                if current_profile is False:
                    logging.error(f"Failed to get current profile for {panel.port}")
                    self.fail(f"Failed to get current profile for {panel.port}")
                if current_profile.IntelArcSyncProfile.value != ARC_SYNC_PROFILE.OFF:
                    logging.error(f"Profile is not set to OFF for {panel.port}")
                    gdhm.report_driver_bug_os(f"[OsFeatures][VRR] Profile is not set to OFF for VRR panel after "
                                              f"disable VRR")
                    self.fail(f"Profile is not set to OFF for {panel.port}")
        logging.info("\tPASS: Negative VRR verification passed successfully for VRR panel with VRR disable")

    ##
    # @brief        Intel Arc Sync verification on NON-VRR panel with disable VRR
    # @return       None
    # @cond
    @common.configure_test(selective=["NON_VRR"])
    # @endcond
    def t_53_arc_sync_non_vrr_panel(self):
        non_vrr_panel_planned = False
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            if adapter.name in PRE_GEN_13_PLATFORMS:
                continue
            for panel in adapter.panels.values():
                if not panel.vrr_caps.is_vrr_supported:
                    non_vrr_panel_planned = True
            if non_vrr_panel_planned is False:
                logging.error("At least one Non-VRR panel require for this test case, planned at least one Non-VRR panel")
                self.fail("At least one VRR panel require for this test case, planned at least one Non-VRR panel")
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            if adapter.name in PRE_GEN_13_PLATFORMS:
                continue
            for panel in adapter.panels.values():
                # Verification intended only for VRR panels
                if panel.vrr_caps.is_vrr_supported:
                    logging.info(f"Ignoring {panel.port} for VRR panel")
                    continue
                panel_args = vrr.get_arc_sync_config(panel)
                if not panel_args:
                    self.fail("Get Monitor config failed for Non-VRR panel")
                elif panel_args.IsIntelArcSyncSupported:
                    gdhm.report_driver_bug_os("[OsFeatures][VRR] VRR support showing True in Non-VRR panel from "
                                              "Arc Sync config call after VRR disable")
                    self.fail("VRR support showing True in Non-VRR panel from Arc Sync config call after VRR disable")
                elif (vrr.get_current_profile(panel,expected_fail=True) or
                      vrr.set_profile(panel, profile=ARC_SYNC_PROFILE.EXCELLENT, expected_fail=True)):
                    gdhm.report_driver_bug_os("[OsFeatures][VRR] Get profile and set profile calls not expected to "
                                              "pass for NonVRR panel")
                    self.fail("Get profile and set profile calls not expected to pass for non VRR panel")
        logging.info("\tPASS: Negative VRR verification passed successfully for Non VRR panel with VRR disable")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestNegative))
    TestEnvironment.cleanup(test_result)
