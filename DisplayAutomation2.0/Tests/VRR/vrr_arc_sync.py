########################################################################################################################
# @file         vrr_arc_sync.py
# @brief        Contains basic functional tests covering below scenarios:
#               * VRR verification in WINDOWED and FULL SCREEN modes with LOW_HIGH_FPS settings
#               * All tests will be executed on VRR panel with VRR enabled. VRR is expected to be working in all above
#               scenarios.
#
# @author       Gopikrishnan R
########################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper.control_api_args import ctl_intel_arc_sync_profile_v as flickerprofiles
from Tests.VRR.vrr_base import *


##
# @brief        This class contains basic VRR tests for different modes and FPS settings.
#               This class inherits the VrrBase class.
class VrrArcSync(VrrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test function to check default arc sync profile for the panel
    # @return       None
    # @cond
    @common.configure_test(critical=True, selective=["DEFAULT_PROFILE_CHECK"])
    # @endcond
    def t_41_check_default_profile(self):
        for gfx_index, adapter in dut.adapters.items():
            if adapter.is_vrr_supported is False or adapter.name in dut.PRE_GEN_13_PLATFORMS:
                continue
            for panel in [panel for panel in adapter.panels.values() if panel.is_active]:
                arc_sync_config = vrr.get_arc_sync_config(panel)
                logging.info(
                    f"Panel Arc Sync Params MinRR:{arc_sync_config.MinimumRefreshRateInHz} "
                    f"MaxRR:{arc_sync_config.MaximumRefreshRateInHz}")
                default_profile, vmin, vmax, sfdit, sfddt, is_vrr = dut.search_monitor_profile_from_table(panel.pnp_id)
                if not vrr.is_profile_applied(panel, default_profile):
                    self.fail("Intel ARC Sync - Monitor Profile is not set as expected")
                else:
                    logging.info(f"PASS: Monitor profile {default_profile} is set as per expected")

    ##
    # @brief        Test function to check default arc sync monitor params for the panel
    # @return       None
    # @cond
    @common.configure_test(critical=True, selective=["PROFILE_PARAMETERS_CHECK"])
    # @endcond
    def t_42_check_arc_sync_params(self):
        for gfx_index, adapter in dut.adapters.items():
            if adapter.is_vrr_supported is False or adapter.name in dut.PRE_GEN_13_PLATFORMS:
                continue
            for panel in [panel for panel in adapter.panels.values() if (panel.is_active and
                                                                         panel.vrr_caps.is_vrr_supported)]:
                dut.update_panel_vrr_profile_config_from_table(panel)
                arc_sync_params = vrr.get_arc_sync_config(panel)
                current_profile = vrr.get_current_profile(panel)
                if ((panel.vrr_caps.is_vrr_supported, panel.vrr_caps.vrr_max_rr,panel.vrr_caps.vrr_min_rr) !=
                        (arc_sync_params.IsIntelArcSyncSupported, int(arc_sync_params.MaximumRefreshRateInHz),
                         int(arc_sync_params.MinimumRefreshRateInHz))):
                    logging.error(f"FAIL: actual: {arc_sync_params.IsIntelArcSyncSupported},"
                                  f"{int(arc_sync_params.MaximumRefreshRateInHz)},"
                                  f"{int(arc_sync_params.MinimumRefreshRateInHz)}, "
                                  f"expected: {panel.vrr_caps.is_vrr_supported},{panel.vrr_caps.vrr_max_rr},"
                                  f"{panel.vrr_caps.vrr_min_rr}")
                    self.fail("panel caps not reported correctly by getarcsyncconfig capi")
                else:
                    logging.info(f"PASS: actual: {arc_sync_params.IsIntelArcSyncSupported},"
                                 f"{int(arc_sync_params.MaximumRefreshRateInHz)},"
                                 f"{int(arc_sync_params.MinimumRefreshRateInHz)}, "
                                 f"expected: {panel.vrr_caps.is_vrr_supported},{panel.vrr_caps.vrr_max_rr},"
                                 f"{panel.vrr_caps.vrr_min_rr}")
                    logging.info("panel caps reported correctly by get_arc_sync_config capi")
                if ((panel.vrr_caps.is_vrr_supported, panel.vrr_caps.vrr_profile_max_rr,
                     panel.vrr_caps.vrr_profile_min_rr, panel.vrr_caps.vrr_profile_sfdit,
                     panel.vrr_caps.vrr_profile_sfddt) != (arc_sync_params.IsIntelArcSyncSupported,
                                                           int(current_profile.MaxRefreshRateInHz),
                                                           int(current_profile.MinRefreshRateInHz),
                                                           int(current_profile.MaxFrameTimeIncreaseInUs),
                                                           int(current_profile.MaxFrameTimeDecreaseInUs))):
                    logging.error(f"FAIL: actual: {arc_sync_params.IsIntelArcSyncSupported},"
                                  f"{int(current_profile.MaxRefreshRateInHz)},"
                                  f"{int(current_profile.MinRefreshRateInHz)}, "
                                  f"{int(current_profile.MaxFrameTimeIncreaseInUs)}, "
                                  f"{int(current_profile.MaxFrameTimeDecreaseInUs)}"
                                  f"expected: {panel.vrr_caps.is_vrr_supported},{panel.vrr_caps.vrr_profile_max_rr},"
                                  f"{panel.vrr_caps.vrr_profile_min_rr},{panel.vrr_caps.vrr_profile_sfdit},"
                                  f"{panel.vrr_caps.vrr_profile_sfddt}")
                    self.fail("panel caps not reported correctly by get current config capi")
                else:
                    logging.info(f"PASS: actual: {arc_sync_params.IsIntelArcSyncSupported},"
                                 f"{int(current_profile.MaxRefreshRateInHz)},"
                                 f"{int(current_profile.MinRefreshRateInHz)}, "
                                 f"{int(current_profile.MaxFrameTimeIncreaseInUs)}, "
                                 f"{int(current_profile.MaxFrameTimeDecreaseInUs)}"
                                 f"expected: {panel.vrr_caps.is_vrr_supported},{panel.vrr_caps.vrr_profile_max_rr},"
                                 f"{panel.vrr_caps.vrr_profile_min_rr},{panel.vrr_caps.vrr_profile_sfdit},"
                                 f"{panel.vrr_caps.vrr_profile_sfddt}")
                    logging.info("panel caps reported correctly by get current config capi")

    ##
    # @brief        VRR verification in FULL_SCREEN mode with LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "LOW_HIGH_FPS"])
    # @endcond
    def t_43_full_screen(self):
        fail_dict = {}
        for profile in flickerprofiles:
            # set custom profile
            if profile == flickerprofiles.INVALID:
                continue
            app_config = workload.FlipAtAppConfig()
            for adapter in dut.adapters.values():
                if adapter.is_vrr_supported is False:
                    continue
                for panel in adapter.panels.values():
                    app_config.pattern_1 = vrr.get_fps_pattern(panel.max_rr)
                    app_config.pattern_2 = vrr.get_fps_pattern(panel.min_rr, False)
                    if profile == flickerprofiles.CUSTOM:
                        vrr.set_profile(panel, profile=profile, minrr=panel.min_rr + 10, maxrr=panel.max_rr - 10)
                        dut.refresh_panel_caps(adapter)
                        dut.update_panel_vrr_profile_config_from_profile(panel, profile, panel.min_rr+10,
                                                                         panel.max_rr-10)
                    else:
                        vrr.set_profile(panel, profile=profile)
                        dut.refresh_panel_caps(adapter)
                        dut.update_panel_vrr_profile_config_from_profile(panel, profile)
                    current_profile = vrr.get_current_profile(panel)
                    if ((panel.vrr_caps.vrr_profile_max_rr, panel.vrr_caps.vrr_profile_min_rr,
                         panel.vrr_caps.vrr_profile_sfdit) !=
                            (int(current_profile.MaxRefreshRateInHz),
                             int(current_profile.MinRefreshRateInHz), int(current_profile.MaxFrameTimeIncreaseInUs))):
                        logging.error(f"FAIL: actual: {int(current_profile.MaxRefreshRateInHz)},"
                                      f"{int(current_profile.MinRefreshRateInHz)}, "
                                      f"{int(current_profile.MaxFrameTimeIncreaseInUs)}, "
                                      f"{int(current_profile.MaxFrameTimeDecreaseInUs)}"
                                      f"expected: {panel.vrr_caps.is_vrr_supported},"
                                      f"{panel.vrr_caps.vrr_profile_max_rr},{panel.vrr_caps.vrr_profile_min_rr},"
                                      f"{panel.vrr_caps.vrr_profile_sfdit},{panel.vrr_caps.vrr_profile_sfddt}")
                        continue
                    logging.info(f"Info: Get_Arc_sync_params: "
                                 f"{int(current_profile.MaxRefreshRateInHz)},"
                                 f"{int(current_profile.MinRefreshRateInHz)}, "
                                 f"{int(current_profile.MaxFrameTimeIncreaseInUs)}, "
                                 f"{int(current_profile.MaxFrameTimeDecreaseInUs)}"
                                 f": Panel params {panel.vrr_caps.is_vrr_supported},"
                                 f"{panel.vrr_caps.vrr_profile_max_rr},{panel.vrr_caps.vrr_profile_min_rr},"
                                 f"{panel.vrr_caps.vrr_profile_sfdit},{panel.vrr_caps.vrr_profile_sfddt}")

                    fail_dict[profile] = self.verify_vrr(True, app_config=app_config)
                    if not fail_dict[profile]:
                        logging.error(
                            f"VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting in "
                            f"{flickerprofiles(profile).name} profile")
                    else:
                        logging.info(
                            f"PASS: VRR verification passed successfully in FULL_SCREEN mode for "
                            f"{flickerprofiles(profile).name} profile")

        if False in fail_dict.values():
            self.fail(f"VRR Verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(VrrArcSync))
    TestEnvironment.cleanup(test_result)
