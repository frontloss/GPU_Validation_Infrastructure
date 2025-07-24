########################################################################################################################
# @file         bfr_base.py
# @brief        contains the base TestCase class for all bfr tests
# @details      @ref bfr_base.py New bfr tests can be created by inheriting this class and adding new test functions.
#               It implements the common setUp and tearDown functions.
#
#               For BFR validation, we are following below steps:
#                   1. Start ETL tracer
#                   2. Open the targeted app (Snip and Sketch Tool/Microsoft tool for boosting).
#                   3. Change the FPS by simulating keyboard key press events
#                   4. Close the app
#                   5. Stop ETL tracer
#                   6. Generate JSON reports from ETL file and verify below:
#                       * Boosted App gives flips in different duration parameters
#                       * VrrVmax / Vtotal programming immediately after Flip with different duration
#                       * Vbi Interval change after the RR is programmed
#                       * Unnecessary RR registers programming without trigger from OS
#                       * Under-run
#                       * TDR
#
#
# @author       Gopikrishnan R
########################################################################################################################

import logging
import sys
import unittest

from Libs.Core import cmd_parser, display_essential, display_power, enum
from Libs.Core.display_config import display_config
from Libs.Core.logger import html, gdhm
from Libs.Feature import crc_and_underrun_verification
from Libs.Feature.powercons import registry
from Tests.BFR import bfr
from Tests.PowerCons.Modules.dut_context import RrSwitchingMethod
from Tests.PowerCons.Modules import common, dut, workload
from Tests.VRR import vrr
from Tests.PowerCons.Functional.DMRRS.dmrrs import MediaFps
from Tests.LFP_Common.Concurrency.edp_feature_utility import verify_vrr
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Functional.DRRS import drrs

# negative cases avoided
SELECTIVE_LIST = ["WINDOWED", "MAXIMIZED", "S3", "S4", "CS", "AC", "VRR", "DMRRS", "STATIC_RR", "DC", "DISPLAY_SWITCH",
                  "MOUSE_MOVE", "WINDOWS_MOVEMENT", "BROWSER_SCROLL", "WORDPAD_SCROLL"]

# Skip straight to test, pre-requsite checks are not needed
DIRECT_TESTS = ["MODE_ENUMERATION", "NEGATIVE_MODE_ENUMERATION"]

##
# @brief    BFR base class
class BfrBase(unittest.TestCase):
    cmd_line_param = None

    is_concurrency_test = False
    is_negative_test = False

    duration = workload.DEFAULT_GAME_PLAYBACK_DURATION

    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    under_run_monitor_ = crc_and_underrun_verification.UnderRunStatus()
    feature_str = "BFR"

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

        # Get App from command line - TO BE IMPLEMENTED
        cls.vrr_app = workload.Apps.Classic3DCubeApp

        # Get game playback duration
        if cls.cmd_line_param[0]['DURATION'] != 'NONE':
            cls.duration = int(cls.cmd_line_param[0]['DURATION'][0]) * 60  # convert into seconds

        # Get refreshRate for DMRRS
        if cls.cmd_line_param[0]['MEDIA_RR'] != 'NONE':
            cls.media_refresh_rate = round(float(cls.cmd_line_param[0]['MEDIA_RR'][0]), 3)  # convert into fraction
        else:
            cls.media_refresh_rate = MediaFps.FPS_24_000


        cls.enable_disable_bfr_via_regkey(enable=True)

        dut.prepare(power_source=display_power.PowerSource.DC)

        # BFR tests need BFR supported platform and eDP panel
        assert dut.is_feature_supported('VRR'), "None of the adapter supports VRR(Planning Issue)"

    ##
    # @brief        Test function to check panel and adapter satisfies the criteria for BFR
    # @return       None
    # @cond
    @common.configure_test(critical=True, selective=SELECTIVE_LIST)
    # @endcond
    def t_00_requirements(self):
        html.step_start(f"Verifying adapter and panel requirements for BFR")

        if self.media_refresh_rate not in MediaFps.__dict__.values():
            gdhm.report_test_bug_os(f"Specified Media FPS {self.media_refresh_rate} is not available (Planning Issue)")
            self.fail(f"Specified Media FPS {self.media_refresh_rate} is not available (Planning Issue)")

        if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_VIBRANIUM:
            gdhm.report_test_bug_os(f"{self.feature_str} not supported on {dut.WIN_OS_VERSION} OS")
            self.fail(f"{self.feature_str} is not supported on {dut.WIN_OS_VERSION} OS")

        for adapter in dut.adapters.values():
            if adapter.name in common.PRE_GEN_12_PLATFORMS:
                gdhm.report_test_bug_os(f"{self.feature_str} is not supported on {adapter.name}")
                self.fail(f"{self.feature_str} is not supported on {adapter.name}")
            logging.info(f"BFR is supported on {adapter.name}")

            if adapter.name not in common.PRE_GEN_14_PLATFORMS:
                psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                if psr_status:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail(f"Failed to restart display driver for {adapter.name}")
                    logging.info(f"\tSuccessfully restarted display driver for {adapter.name} after disabling PSR")

            dut.refresh_panel_caps(adapter)            
            for panel in adapter.panels.values():
                # Multiple displays can be present in command line for display switching test, skip feature requirement
                # test for non-LFP panels
                if panel.bfr_caps.is_bfr_supported:
                    logging.info(f"{panel}:")
                    logging.info(f"\t{panel.psr_caps}")
                    logging.info(f"\t{panel.drrs_caps}")
                    logging.info(f"\t{panel.lrr_caps}")
                    logging.info(f"\t{panel.vrr_caps}")
                    logging.info(f"\t{panel.bfr_caps}")

                    if panel.lrr_caps.is_lrr_1_0_supported is True:
                        gdhm.report_test_bug_os(f"{self.feature_str} is not supported on LRR1.0 panel")
                        self.fail(f"{self.feature_str} is not supported on LRR1.0 panel {panel.port}")

                    if panel.vrr_caps.max_rr < 2 * panel.vrr_caps.min_rr:
                        gdhm.report_test_bug_os(
                            f"{self.feature_str} is not supported on panel with max RR < 2*Min RR")
                        self.fail(f"{self.feature_str} is not supported on panel with max RR < 2*Min RR {panel.port}")

                    elif panel.vrr_caps.max_rr < 60:
                        gdhm.report_test_bug_os(
                            f"{self.feature_str} is not supported on panel with panel <= 60Hz as max RR")
                        self.fail(
                            f"{self.feature_str} is not supported on panel with panel <= 60Hz as max RR {panel.port}")

                    elif panel.lrr_caps.rr_switching_method not in [RrSwitchingMethod.VTOTAL_SW,
                                                                    RrSwitchingMethod.VTOTAL_HW]:
                        gdhm.report_test_bug_os(f"{self.feature_str} is not supported on panel where RR switching "
                                                f"method is neither VTOTAL SW nor HW method")
                        self.fail(
                            f"{self.feature_str} is not supported on panel where RR switching method is neither "
                            f"VTOTAL SW nor "
                            "HW method")
                    # Enable regkey for enabling bfr in external panel
                    if not panel.is_lfp:
                        bfr.enable()
        html.step_end()

    ##
    # @brief        Test function to enable dynamic rr in the system
    # @return       None
    # @cond
    @common.configure_test(critical=True, selective=SELECTIVE_LIST)
    # @endcond
    def t_01_set_dynamic_rr(self):
        status = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.bfr_caps.is_bfr_supported:
                    if bfr.set_dynamic_rr(panel) is False:
                        logging.error("Unable to set to Dynamic RR mode")
                        if not bfr.check_bfr_mode_enumeration(adapter, panel):
                            self.fail("VirtualRR support is not enumerated for any display mode, Set Dynamic RR failed")
                        self.fail("Unable to set to Dynamic RR mode, despite enumerating VirtualRRSupport")
                    else:
                        status = True

            dut.refresh_panel_caps(adapter)
        if not status:
            logging.error("Unable to find eDP panel to apply Dynamic RR mode")

    ##
    # @brief        Test function to enable static rr in the system
    # @return       None
    # @cond
    @common.configure_test(critical=True, selective=["STATIC_RR"])
    # @endcond
    def t_02_set_static_rr(self):
        status = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.bfr_caps.is_bfr_supported:
                    if bfr.set_static_rr(panel) is False:
                        self.fail("Unable to set to Static RR from Dynamic RR")
                    status = True
                    break
        if not status:
            logging.error("Unable to find eDP panel to apply Static RR mode")

    ##
    # @brief        This method is the exit point for all VRR test cases. This resets the environment changes for the
    #               VRR tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        for adapter in dut.adapters.values():
            if adapter.name not in common.PRE_GEN_14_PLATFORMS:
                psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                if psr_status:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status:
                        logging.info(f"\tSuccessfully restarted display driver for {adapter.name} after enabling PSR")
        cls.enable_disable_bfr_via_regkey(enable=False)
        dut.reset()

    ##
    # @brief        BFR verification in WINDOWED/MAXIMIZED mode
    # @param[in]    maximized Maximized
    # @param[in]    power_event Power Event
    # @param[in]    power_source Power Source
    # @param[in]    negative Negative
    # @param[in]    target_ids Target ids
    # @return       Result : True/False
    def bfr_basic(self, maximized=True, power_event=None, power_source=None, negative=False, target_ids=None):
        max_trials = 3
        result = False
        for trial in range(max_trials):
            result = self.validate_bfr(duration=self.duration, maximized=maximized, power_event=power_event,
                                       power_source=power_source, negative=negative, target_ids=target_ids)[0]
            if result:
                break
        if not result:
            logging.error(f"FAIL : Basic Verification : BFR verification failed in all {max_trials} attempts")
        else:
            logging.info(f"\tPASS: BASIC Verification : BFR verification passed successfully")
        return result

    #
    ##
    # @brief        Helper function to run and verify VRR scenario
    # @return       status bool True if RR change is detected, False otherwise
    @staticmethod
    def validate_vrr():
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.bfr_caps.is_bfr_supported:
                    return verify_vrr(adapter, panel)

    ##
    # @brief        Helper function to run and verify BFR scenario
    # @param[in]    duration                : Duration for which the app has to be ran
    # @param[in]    maximized               : indicates if the video should be in full screen mode or not
    # @param[in]    power_event             : enum indicating the power state
    # @param[in]    power_source            : enum for AC / DC
    # @param[in]    negative                : boolean, True if test is a negative BFR test, False otherwise
    # @param[in]    target_ids Target ids
    # @return       status,etl_file         : status and etl file
    @staticmethod
    def validate_bfr(duration=30, maximized=True, power_event=None, power_source=None, negative=False, target_ids=None):
        status = True
        etl_file = None
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if (target_ids is not None and panel.target_id in target_ids) or \
                        (target_ids is None and panel.bfr_caps.is_bfr_supported):
                    if not bfr.is_dynamic_rr(panel) and not negative:
                        bfr.set_dynamic_rr(panel)
                    etl_file, _ = workload.run(
                        workload.BOOSTED_APP, [duration, panel, power_event, power_source, maximized, negative])
                    if not etl_file:
                        logging.error("ETL file is not present")
                        status = False
                        return status, None
                    status &= bfr.verify(adapter, panel, etl_file, power_event, negative)
        return status, etl_file

    ##
    # @brief        Disable/Enable BFR using regkey
    # @param[in]    enable : True if enable BFR, False otherwise
    # @return       Result : True/False
    @staticmethod
    def enable_disable_bfr_via_regkey(enable):
        for adapter in dut.adapters.values():
            display_fc2 = registry.DisplayFeatureControl2(adapter.gfx_index)
            e_bit = 0 if enable else 1
            if display_fc2.DisableVirtualRefreshRateSupport != e_bit:
                display_fc2.DisableVirtualRefreshRateSupport = e_bit
                status = display_fc2.update(adapter.gfx_index)
                if status is False:
                    logging.error(f"\tFailed to {'enable' if enable else 'disable'} BFR from DisplayFeatureControl2 "
                                  f"registry on {adapter.name}")
                    gdhm.report_driver_bug_os(f"[OsFeatures][BFR] Failed to {'enable' if enable else 'disable'} BFR "
                                              f"from DisplayFeatureControl2 registry")
                    return False
                if status:
                    result, reboot_required = display_essential.restart_gfx_driver()
                    if result is False:
                        logging.error(f"\tFailed to restart display driver after BFR {'enable' if enable else 'disable'}"
                                      f"update")
                        return False
                    logging.info(f"\tPASS: {'enable' if enable else 'disable'} BFR from DisplayFeatureControl2 registry"
                                 f"on {adapter.name}")
                    return True
