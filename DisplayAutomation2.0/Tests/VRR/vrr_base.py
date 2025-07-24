########################################################################################################################
# @file         vrr_base.py
# @brief        Contains the base TestCase class for all VRR tests, New VRR tests can be created by inheriting this 
#               class and adding new test functions.
#               For VRR validation, we are following below steps:
#                   1. Start ETL tracer
#                   2. Open the targeted app (AngryBots/Rectangle/Triangle/Cube). Default is Rectangle.
#                   3. Change the FPS by simulating keyboard key press events
#                   4. Close the app
#                   5. Stop ETL tracer
#                   6. Generate JSON reports from ETL file and verify below:
#                       * Number of incoming async flips should not be zero for positive tests
#                       * If HIGH_FPS setting is disabled, number of submitted async flips should be zero
#                       * If HIGH_FPS setting is enabled and FPS was greater than applied max RR, number of submitted
#                         flips should not be zero
#                       * VRR Enable and VRR Disable trace events should be present in ETL
#                       * Number of VRR enabling should be equals to number of disabling
#                       * Total number of VRR enabling/disabling should not be abnormally high
#                       * VRR Vmin, Vmax, FlipLine, VrrCtl, VrrStatus, TransPush registers Programming
#                       * VRR should not get enabled if there is no incoming Async flip
#                       * Under-run
#                       * TDR
#               Above verification is done in multiple scenarios, i.e. different displays modes, with power events etc.
#
# @author       Rohit Kumar, Gopikrishnan R
########################################################################################################################

import logging
import os
import sys
import time
import unittest
from Libs.Core import cmd_parser, display_power, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.logger import etl_tracer, html
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Libs.Feature import crc_and_underrun_verification
from operator import attrgetter
from Tests.PowerCons.Modules import common, dut, workload
from Tests.VRR import vrr
from Tests.PowerCons.Modules.dut_context import Adapter, Panel, PRE_GEN_13_PLATFORMS

ARC_SYNC_PROFILE = control_api_args.ctl_intel_arc_sync_profile_v

SELECTIVE_LIST = ["WINDOWED", "FULL_SCREEN", "S3", "S4", "CS", "AC_DC", "DEFAULT_PROFILE_CHECK"]


##
# @brief        Exposed Class to write VRR tests. Any new test can inherit this class to use common setUp and tearDown
#               functions. VrrBase also includes some functions used across all VRR tests.
class VrrBase(unittest.TestCase):
    cmd_line_param = None

    is_concurrency_test = False
    is_negative_test = False

    app = None
    game = 1
    pattern = [6, 3, 18, 1, 100]
    duration = workload.DEFAULT_GAME_PLAYBACK_DURATION

    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    under_run_monitor_ = crc_and_underrun_verification.UnderRunStatus()

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for any VRR test case. Helps to initialize some of the
    #               parameters required for VRR test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]
        if cls.cmd_line_param[0]['RR_PROFILE'] != "NONE":
            profile = cls.cmd_line_param[0]['RR_PROFILE'][0]
            assert profile in ARC_SYNC_PROFILE.__members__, "Passed profile is not defined"
            cls.profile = ARC_SYNC_PROFILE[profile.upper()]
        else:
            cls.profile = None

        # Get App from command line
        if cls.cmd_line_param[0]['APP'] != 'NONE':
            if cls.cmd_line_param[0]['APP'][0] == 'RECTANGLE':
                cls.app = workload.Apps.MovingRectangleApp
            if cls.cmd_line_param[0]['APP'][0] == 'CUBE':
                cls.app = workload.Apps.Classic3DCubeApp
            if cls.cmd_line_param[0]['APP'][0] == 'ANGRYBOTS':
                cls.app = workload.Apps.AngryBotsGame
            if cls.cmd_line_param[0]['APP'][0] == 'FLIPAT':
                cls.app = workload.Apps.FlipAt
        else:
            # If App is not present in command line, set default apps for present OS
            if dut.WIN_OS_VERSION >= dut.WinOsVersion.WIN_19H1:
                cls.app = workload.Apps.Classic3DCubeApp
            else:
                cls.app = workload.Apps.MovingRectangleApp

        # Get Game for FlipAt app
        if cls.cmd_line_param[0]['GAME'] != 'NONE':
            cls.game = workload.FLIP_AT_GAME_ARGUMENT_MAPPING.get(cls.cmd_line_param[0]['GAME'][0], 1)

        # Get manual FPS pattern for FlipAt app
        if cls.cmd_line_param[0]['PATTERN'] != 'NONE':
            cls.pattern = cls.cmd_line_param[0]['PATTERN']

        # Get game playback duration
        if cls.cmd_line_param[0]['DURATION'] != 'NONE':
            cls.duration = int(cls.cmd_line_param[0]['DURATION'][0]) * 60  # convert into seconds

        # VRR tests need at least one VRR supported platform
        assert dut.is_feature_supported('VRR'), "None of the adapter supports VRR(Planning Issue)"

        dut.prepare()
        # @todo need to remove this code check once implemented vrr check during active time
        # Currently, angry Bot game is lunching with 4k and DPS043 panel recommended config is 25X16. due to that
        # test case is failing for angrybots game.
        if cls.app == workload.Apps.AngryBotsGame:
            for adapter in dut.adapters.values():
                if adapter.is_vrr_supported is False:
                    continue
                for panel in adapter.panels.values():
                    if not panel.is_lfp:
                        all_supported_modes = cls.display_config_.get_all_supported_modes([panel.target_id])
                        for _, modes in all_supported_modes.items():
                            modes = sorted(modes, key=attrgetter('HzRes', 'refreshRate'), reverse=True)
                            logging.info("Applying mode: {}x{} @ {}".format(modes[0].HzRes, modes[0].VtRes,
                                                                            modes[0].refreshRate))
                            assert cls.display_config_.set_display_mode([modes[0]], False), \
                                "Failed to apply display mode"
                            logging.info("\tSuccessfully applied the display mode")
                            break



    ##
    # @brief        This method is the exit point for all VRR test cases. This resets the environment changes for the
    #               VRR tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            # Make sure PSR2 is restored
            if "psr1" in sys.argv or "PSR1" in sys.argv:
                from Tests.PowerCons.Functional.PSR import psr
                logging.info("Step: Enabling PSR2 for {0}".format(adapter.name))
                psr2_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                if psr2_status is False:
                    assert False, "FAILED to enable PSR2 through registry key"
                logging.info("Re-enable Psr2,  PSR2 status Expected= ENABLED, Actual= ENABLED")
                if psr2_status:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        assert False, "FAILED to restart the driver"
            if adapter.name in PRE_GEN_13_PLATFORMS:
                continue
            for panel in adapter.panels.values():
                if panel.vrr_caps.is_vrr_supported:
                    vrr.set_profile(panel, ARC_SYNC_PROFILE.RECOMMENDED)
        dut.reset()

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test function is to verify system and panel requirements for VRR test
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start("Verify system and panel requirements for VRR test")
        for adapter in dut.adapters.values():
            logging.info("Active panel capabilities for {0}".format(adapter.name))
            for panel in adapter.panels.values():
                logging.info("\t{0}".format(panel))
                logging.info("\t\t{0}".format(panel.psr_caps))
                logging.info("\t\t{0}".format(panel.drrs_caps))
                logging.info("\t\t{0}".format(panel.vrr_caps))
                logging.info("\t\t{0}".format(panel.pipe_joiner_tiled_caps))
        html.step_end()

    ##
    # @brief        Test function to make sure VRR got enabled successfully
    # @return       None
    # @cond
    @common.configure_test(selective=(["NO_LOW_HIGH_FPS"] + SELECTIVE_LIST), critical=True)
    # @endcond
    def t_10_enable_vrr(self):
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            html.step_start("Enabling VRR with NO_LOW_HIGH_FPS solution for {0}".format(adapter.name))
            assert vrr.enable(adapter), "Failed to enable VRR"
            logging.info("\tPASS: Enabled VRR successfully")
            # Update panel caps after enabling feature
            dut.refresh_panel_caps(adapter)
            html.step_end()

    ##
    # @brief        Test function to make sure VRR is enabled with Low FPS solution
    # @return       None
    # @cond
    @common.configure_test(selective=(["LOW_FPS"] + SELECTIVE_LIST), critical=True)
    # @endcond
    def t_20_enable_vrr_low_fps(self):
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            html.step_start("Enabling VRR with LOW_FPS solution for {0}".format(adapter.name))
            assert vrr.enable(adapter, is_low_fps=True), "Failed to enable VRR with LOW FPS solution"
            logging.info("\tPASS: Enabled VRR successfully")
            # Update panel caps after enabling feature
            dut.refresh_panel_caps(adapter)
            html.step_end()

    ##
    # @brief        Test function to make sure VRR is enabled with High FPS solution
    # @return       None
    # @cond
    @common.configure_test(selective=(["HIGH_FPS"] + SELECTIVE_LIST), critical=True)
    # @endcond
    def t_30_enable_vrr_high_fps(self):
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            html.step_start("Enabling VRR with HIGH_FPS solution for {0}".format(adapter.name))
            assert vrr.enable(adapter, is_high_fps=True), "Failed to enable VRR with HIGH_FPS solution"
            logging.info("\tPASS: Enabled VRR successfully")
            # Update panel caps after enabling feature
            dut.refresh_panel_caps(adapter)
            html.step_end()

    ##
    # @brief        Test function to make sure VRR is enabled with both Low and High FPS solution
    # @return       None
    # @cond
    @common.configure_test(selective=(["LOW_HIGH_FPS"] + SELECTIVE_LIST), critical=True)
    # @endcond
    def t_40_enable_vrr_low_high_fps(self):
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            html.step_start("Enabling VRR with LOW & HIGH FPS solution for {0}".format(adapter.name))
            assert vrr.enable(adapter, True, True), "Failed to enable VRR with LOW & HIGH FPS solution"
            logging.info("\tPASS: Enabled VRR successfully")
            # Update panel caps after enabling feature
            dut.refresh_panel_caps(adapter)
            if self.profile is not None and adapter.name not in dut.PRE_GEN_13_PLATFORMS:
                for panel in adapter.panels.values():
                    if panel.is_active and panel.vrr_caps.is_vrr_supported:
                        vrr.set_profile(panel, self.profile)
            html.step_end()

    ##
    # @brief        Test function to make sure VRR is disabled
    # @return       None
    # @cond
    @common.configure_test(selective=["VRR"], critical=True)
    # @endcond
    def t_50_disable_vrr(self):
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            html.step_start("Disabling VRR for {0}".format(adapter.name))
            assert vrr.disable(adapter), "Failed to disable VRR(Test Issue)"
            logging.info("\tPASS: Disabled VRR successfully")
            html.step_end()

    ##
    # @brief        Test function to make sure VRR is disabled
    # @param[in]    full_screen             : indicates if the video should be in full screen mode or not
    # @param[in]    power_event             : enum indicating the power state
    # @param[in]    power_source            : enum for AC/DC
    # @param[in]    app_config              : app configuration for workload tests
    # @param[in]    negative                : boolean, True if test is a negative VRR test, False otherwise
    # @param[in]    return_etl              : boolean, True if caller wants ETL to be returned, False otherwise
    # @param[in]    expected_vrr            : boolean, True if caller expects VRR to be enabled, False otherwise
    # @param[in]    is_dc_balancing_enabled : boolean, True if dc balancing is enabled, False otherwise
    # @param[in]    optical_sensor_args     : optical sensor arguments
    # @param[in]    vmax_flipline_foreachflip : boolean, True if verification is required, False otherwise
    # @return       status                  : tuple of boolean and string
    def verify_vrr(
            self, full_screen, power_event=None, power_source=None, app_config=None, negative=False, return_etl=False,
            expected_vrr=True, is_dc_balancing_enabled=False, optical_sensor_args=None,
            vmax_flipline_foreachflip=True):
        is_os_aware_vrr = dut.WIN_OS_VERSION >= dut.WinOsVersion.WIN_19H1
        is_prev_vtotal_check_require = False
        vmax_flipline_for_each_flip = vmax_flipline_foreachflip
        # Run workload
        if optical_sensor_args is None:
            etl_file, _ = workload.run(
                workload.GAME_PLAYBACK, [self.app, self.duration, full_screen, power_event, power_source, app_config])
            optical_sensor_samples = None
        else:
            etl_file, _, optical_sensor_samples = workload.run(
                workload.GAME_PLAYBACK, [self.app, self.duration, full_screen, power_event, power_source, app_config],
                None, optical_sensor_args)

        # Ensure async flips
        if vrr.async_flips_present(etl_file) is False:
            if self.app == workload.Apps.FlipAt:
                self.fail("OS is NOT sending async flips")
            logging.info(f"Async flip not observed with {self.app}")
            self.app = workload.Apps.FlipAt
            app_config = workload.FlipAtAppConfig()
            app_config.game_index = 2
            etl_file, _ = workload.run(
                workload.GAME_PLAYBACK, [self.app, self.duration, full_screen, power_event, power_source, app_config])
            if vrr.async_flips_present(etl_file) is False:
                self.fail("OS is NOT sending async flips")

        enumerated_displays = self.display_config_.get_enumerated_display_info()
        assert enumerated_displays, "Failed to get enumerated display information"

        if self.app == workload.Apps.FlipAt:
            is_prev_vtotal_check_require = True

        if self.app in [workload.Apps.MovingRectangleApp, workload.Apps.AngryBotsGame]:
            vmax_flipline_for_each_flip = False

        # verify
        status = True
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                if "TILED" in sys.argv:
                    if display_config.is_display_attached(enumerated_displays, panel.port, panel.gfx_index):
                        status &= vrr.verify(adapter, panel, etl_file, power_event, negative, is_os_aware_vrr,
                                             expected_vrr, is_prev_vtotal_check_require=is_prev_vtotal_check_require,
                                             vmax_flipline_for_each_flip=vmax_flipline_for_each_flip)
                else:
                    status &= vrr.verify(adapter, panel, etl_file, power_event, negative, is_os_aware_vrr, expected_vrr,
                                         is_prev_vtotal_check_require=is_prev_vtotal_check_require,
                                         vmax_flipline_for_each_flip=vmax_flipline_for_each_flip)

        # Verify Optical Sensor Data
        if optical_sensor_args is not None:
            status &= vrr.verify_optical_sensor_data(optical_sensor_samples)

        if return_etl:
            return status, etl_file
        return status

    ##
    # @brief        Test function to make sure VRR is disabled
    # @param[in]    etl_path                : etl file path
    # @return       status                  : tuple of boolean
    def verify_vrr_during_modeset(self, etl_path=None):
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        assert enumerated_displays, "Failed to get enumerated display information"

        # verify
        status = True
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            for panel in adapter.panels.values():
                if "TILED" in sys.argv:
                    if display_config.is_display_attached(enumerated_displays, panel.port, panel.gfx_index):
                        status &= vrr.verify_modeset(adapter, panel, etl_path)
                else:
                    status &= vrr.verify_modeset(adapter, panel, etl_path)
        return status
