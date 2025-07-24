########################################################################################################################
# @file         test_get_set_intel_arc_sync.py
# @brief        Test calls for Get InterArcSync Config for panel and get/set ArcSync profile for panels.
#                   * Get Intel Arc Sync Monitor Config
#                   * Get Intel Arc Sync Profile
#                   * Set Intel Arc Sync Profile
# @author       Gopikrishnan R
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Control_API.control_api_base import testBase
from Libs.Core.logger import html
from Tests.PowerCons.Modules.common import get_display_mode


##
# @brief - Verify Get-Set Intel Arc Sync Control Library test
class testIntelArcSync(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Get-Set Intel-Arc Sync via Control Library")
        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)

            monitor_info = control_api_args.ctl_intel_arc_sync_monitor_params_t()
            monitor_info.Version = 0
            monitor_info.Size = ctypes.sizeof(monitor_info)

            # Get Intel Arc Sync support for monitor
            html.step_start("Getting Monitor parameters")
            if control_api_wrapper.get_intel_arc_sync_info(monitor_info, targetid):
                logging.info("Pass: Get Monitor Info from Control Library")
                max_rr = monitor_info.MaximumRefreshRateInHz
                min_rr = monitor_info.MinimumRefreshRateInHz
                logging.info(f"get_intel_arc_sync_info : Min RR:{min_rr} MaxRR: {max_rr}")
            else:
                logging.error("Fail: Get Monitor Info via Control Library")
                gdhm.report_driver_bug_clib("Get Monitor Info Failed via Control Library for "
                                            "Arc Support: {0} TargetId: {1}"
                                            .format(monitor_info.IsIntelArcSyncSupported, targetid))
                self.fail("Get Monitor Info Failed via Control Library")
            html.step_end()
            # get mode with max RR and apply max RR
            display_mode_list = []
            display_mode_list = get_display_mode(targetid, max_rr, limit=2)
            for mode in display_mode_list:
                logging.info("Applying mode: {}x{} @ {}".format(mode.HzRes, mode.VtRes, mode.refreshRate))
                assert self.display_config.set_display_mode([mode], False), "Failed to apply display mode"
                logging.info("\tSuccessfully applied the display mode")
                break

            # Get Current profile info for monitor
            html.step_start("Getting current Profile Info")
            profile_params = control_api_args.ctl_intel_arc_sync_profile_params_t()
            profile_params.Size = ctypes.sizeof(profile_params)
            if control_api_wrapper.get_current_intel_arc_sync_profile(profile_params, targetid):
                logging.info(f"Pass: Current profile got from Control Library is : "
                             f"{profile_params.IntelArcSyncProfile} Control Library")
            else:
                logging.error("Fail: Get Monitor Info via Control Library")
                gdhm.report_driver_bug_clib("Get Monitor Info Failed via Control Library for "
                                            "Arc Profile: {0} TargetId: {1}"
                                            .format(profile_params.IntelArcSyncProfile, targetid))
                self.fail("Get Monitor Info Failed via Control Library")
            html.step_end()

            # Set Profile for monitor
            html.step_start(f"Setting profile to {control_api_args.ctl_intel_arc_sync_profile_v.EXCELLENT.name}")
            profile_params = control_api_args.ctl_intel_arc_sync_profile_params_t()
            profile_params.Size = ctypes.sizeof(profile_params)
            profile_params.IntelArcSyncProfile = control_api_args.ctl_intel_arc_sync_profile_v.EXCELLENT
            logging.info(f"Pass: Current profile got from Control Library is : "
                         f"{profile_params.IntelArcSyncProfile} Control Library")
            if control_api_wrapper.set_intel_arc_sync_profile(profile_params, targetid):
                logging.info("Pass: Set Monitor Info from Control Library")
            else:
                logging.error("Fail: Set Monitor Info via Control Library")
                gdhm.report_driver_bug_clib("Set Monitor Info Failed via Control Library for "
                                            "Arc Profile: {0} TargetId: {1}"
                                            .format(profile_params.IntelArcSyncProfile, targetid))
                self.fail("Set Monitor Info Failed via Control Library")

            profile_params = control_api_args.ctl_intel_arc_sync_profile_params_t()
            profile_params.Size = ctypes.sizeof(profile_params)
            if control_api_wrapper.get_current_intel_arc_sync_profile(profile_params, targetid):
                logging.info(f"Pass: Current profile got from Control Library is : "
                             f"{profile_params.IntelArcSyncProfile} Control Library")
                if profile_params.IntelArcSyncProfile.value != \
                        control_api_args.ctl_intel_arc_sync_profile_v.EXCELLENT.value:
                    gdhm.report_driver_bug_clib("Current profile not matching with passed value in set call "
                                                "EXPECTED: {0} ACTUAL: {1}"
                                                .format(profile_params.IntelArcSyncProfile.value,
                                                        control_api_args.ctl_intel_arc_sync_profile_v.EXCELLENT.value))
                    self.fail("Read profile value not same as what was passed in set call")
            else:
                logging.error("Fail: Get Monitor Info via Control Library")
                gdhm.report_driver_bug_clib("Get Monitor Info Failed via Control Library for "
                                            "Arc Profile: {0} TargetId: {1}"
                                            .format(profile_params.IntelArcSyncProfile, targetid))
                self.fail("Get Monitor Info Failed via Control Library")
            html.step_end()

            html.step_start(f"Setting Custom profile")
            # Set Custom parameters for monitor
            profile_params = control_api_args.ctl_intel_arc_sync_profile_params_t()
            profile_params.Size = ctypes.sizeof(profile_params)
            profile_params.IntelArcSyncProfile = control_api_args.ctl_intel_arc_sync_profile_v.CUSTOM
            profile_params.MaxRefreshRateInHz = max_rr - 10
            profile_params.MinRefreshRateInHz = min_rr + 10
            profile_params.MaxFrameTimeIncreaseInUs = 0
            profile_params.MaxFrameTimeDecreaseInUs = 0
            if control_api_wrapper.set_intel_arc_sync_profile(profile_params, targetid):
                logging.info(f"Pass: Set custom profile values in Control Library")
            else:
                logging.error("Fail: Set custom profile values in Control Library")
                gdhm.report_driver_bug_clib("Set Custom Profile values Failed via Control Library for "
                                            "Arc Profie: {0} Max RR: {1} Min RR: {2}"
                                            .format(profile_params.IntelArcSyncProfile,
                                                    profile_params.MaxRefreshRateInHz,
                                                    profile_params.MinRefreshRateInHz))
                self.fail("Set custom profile values in Control Library")

            profile_params = control_api_args.ctl_intel_arc_sync_profile_params_t()
            profile_params.Size = ctypes.sizeof(profile_params)
            if control_api_wrapper.get_current_intel_arc_sync_profile(profile_params, targetid):
                logging.info(
                    f"Pass: Get Current profile info from -{profile_params.IntelArcSyncProfile} Control Library")
                if (profile_params.MaxRefreshRateInHz, profile_params.MinRefreshRateInHz) != (max_rr - 10, min_rr + 10):
                    gdhm.report_driver_bug_clib("Current profile not matching with passed value in set call "
                                                "Max RR: {0} Min RR: {1}".format(profile_params.MaxRefreshRateInHz,
                                                                                 profile_params.MinRefreshRateInHz))
                    self.fail("Read profile value not same as what was passed in set call")
                logging.info("Read profile value is same as set")
            else:
                gdhm.report_driver_bug_clib("Get Monitor Info Failed via Control Library for "
                                            "Arc Profile: {0}".format(profile_params.IntelArcSyncProfile))
                self.fail("Fail: Get Monitor Info via Control Library")
            html.step_end()

            # Negative
            profile_params = control_api_args.ctl_intel_arc_sync_profile_params_t()
            profile_params.Size = ctypes.sizeof(profile_params)
            profile_params.IntelArcSyncProfile = control_api_args.ctl_intel_arc_sync_profile_v.CUSTOM
            profile_params.MaxRefreshRateInHz = max_rr + 10
            profile_params.MinRefreshRateInHz = min_rr - 10
            profile_params.MaxFrameTimeIncreaseInUs = 0
            profile_params.MaxFrameTimeDecreaseInUs = 0
            if not control_api_wrapper.set_intel_arc_sync_profile(profile_params, targetid):
                logging.info(f"Pass: Set custom profile values failed as expected for invalid value")

            # Set Profile for monitor as RECOMMENDED
            html.step_start(f"setting profile to {control_api_args.ctl_intel_arc_sync_profile_v.RECOMMENDED.name}")
            profile_params = control_api_args.ctl_intel_arc_sync_profile_params_t()
            profile_params.Size = ctypes.sizeof(profile_params)
            profile_params.IntelArcSyncProfile = control_api_args.ctl_intel_arc_sync_profile_v.RECOMMENDED
            logging.info(
                f"Pass: Current profile got from Control Library is : {profile_params.IntelArcSyncProfile} Control Library")
            if control_api_wrapper.set_intel_arc_sync_profile(profile_params, targetid):
                logging.info("Pass: Set Monitor Info from Control Library")
            else:
                gdhm.report_driver_bug_clib("Set Monitor Info Failed via Control Library for "
                                            "Arc Profile: {0}".format(profile_params.IntelArcSyncProfile))
                self.fail("Fail: Set Monitor Info via Control Library")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Intel Arc Sync Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
