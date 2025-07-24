#################################################################################################################
# @file         lrr_base.py
# @brief        Contains base class for LRR tests
#
# @author       Rohit Kumar
#################################################################################################################

import logging
import sys
import unittest

from Libs.Core import cmd_parser, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.logger import html, gdhm
from Tests.PowerCons.Functional.DMRRS import hrr
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.LRR.lrr import LrrVersion, Method, VIDEO_FILE_MAPPING
from Tests.PowerCons.Modules import dut, common
from Tests.PowerCons.Modules.dut_context import RrSwitchingMethod
from Tests.PowerCons.Modules.workload import PowerSource


##
# @brief        Exposed Class to write LRR tests. Any new LRR test can inherit this class to use common setUp and
#               tearDown functions. LrrBase also includes some functions used across all LRR tests.
class LrrBase(unittest.TestCase):
    cmd_line_param = None
    feature = LrrVersion.LRR1_0
    is_feature_override = False
    method = Method.IDLE
    is_hrr_test = False
    video_file = VIDEO_FILE_MAPPING['24']
    duration_in_seconds = 30
    polling_delay_in_seconds = 0.01
    rr_switching_method = RrSwitchingMethod.UNSUPPORTED

    ##
    # @brief        This class method is the entry point for LRR test cases. Helps to initialize few of the
    #               parameters required for LRR test execution.
    # @details      This function checks for feature support and initializes parameters to handle
    #               multi-adapter scenarios in test cases
    # @return       None
    @classmethod
    def setUpClass(cls):
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        # Get LRR version and populate RR switching method
        if cls.cmd_line_param[0]['FEATURE'] != 'NONE':
            if cls.cmd_line_param[0]['FEATURE'][0] == 'LRR1':
                cls.feature = LrrVersion.LRR1_0
                cls.rr_switching_method = RrSwitchingMethod.CLOCK
            elif cls.cmd_line_param[0]['FEATURE'][0] == 'LRR2':
                cls.feature = LrrVersion.LRR2_0
                cls.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
            elif cls.cmd_line_param[0]['FEATURE'][0] == 'LRR2.5':
                cls.feature = LrrVersion.LRR2_5
                if common.PLATFORM_NAME in common.PRE_GEN_14_PLATFORMS:
                    cls.rr_switching_method = RrSwitchingMethod.VTOTAL_SW
                else:
                    cls.rr_switching_method = RrSwitchingMethod.VTOTAL_HW
            elif cls.cmd_line_param[0]['FEATURE'][0] == 'NO_LRR':
                cls.feature = LrrVersion.NO_LRR
                cls.rr_switching_method = RrSwitchingMethod.UNSUPPORTED

            if len(cls.cmd_line_param[0]['FEATURE']) > 1:
                if cls.cmd_line_param[0]['FEATURE'][1] == 'OVERRIDE':
                    cls.is_feature_override = True

        # Check HRR verification required
        cls.is_hrr_test = cls.cmd_line_param[0]['HRR'] != 'NONE'

        # Get Method of workload
        if cls.cmd_line_param[0]['METHOD'] != 'NONE':
            if cls.cmd_line_param[0]['METHOD'][0] == "IDLE":
                cls.method = Method.IDLE
            elif cls.cmd_line_param[0]['METHOD'][0] == "VIDEO":
                cls.method = Method.VIDEO
            else:
                assert False, f"Method {cls.cmd_line_param[0]['METHOD'][0]} is Invalid (Commandline issue)"

        # Get Video and map the file
        if cls.cmd_line_param[0]['VIDEO'] != 'NONE':
            video = cls.cmd_line_param[0]['VIDEO'][0]
            if video not in VIDEO_FILE_MAPPING.keys():
                assert False, f"{cls.video_file} video is invalid/ unavailable (Commandline issue)"
            cls.video_file = VIDEO_FILE_MAPPING[video]

        if cls.cmd_line_param[0]['DURATION'] != 'NONE':
            cls.duration_in_seconds = int(cls.cmd_line_param[0]['DURATION'][0])

        if cls.method == Method.IDLE:
            logging.info(f"Workload= {cls.method}, Duration= {cls.duration_in_seconds} s")
        elif cls.method == Method.VIDEO:
            logging.info(f"Workload= {cls.method}, Video= {cls.video_file}, Duration= {cls.duration_in_seconds} s")

        dut.prepare(power_source=PowerSource.DC_MODE)

    ##
    # @brief        This method is the exit point for LRR test cases. This resets the environment changes done
    #               for execution of LRR tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        display_config_ = display_config.DisplayConfiguration()
        for adapter in dut.adapters.values():
            refresh_caps = False
            for panel in adapter.panels.values():
                current_mode = display_config_.get_current_mode(panel.target_id)
                if current_mode == panel.native_mode:
                    # There can be two modes with max RR with different pixel clocks. DisplayMode __eq__ does not
                    # compare pixel clocks. Override the native_mode with current_mode for such cases.
                    panel.native_mode = current_mode
                    continue
                refresh_caps = True
                display_config_.set_display_mode([panel.native_mode], False)
            if refresh_caps:
                dut.refresh_panel_caps(adapter)
        if cls.is_hrr_test:
            for adapter in dut.adapters.values():
                hrr_status = hrr.disable(adapter)
                dut.refresh_panel_caps(adapter)
                if hrr_status is False:
                    assert False, "FAILED to disable HRR (Test Issue)"
                logging.info(f"\tPASS: Disabled HRR on {adapter.name}")
                if hrr_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        assert False, f"Failed to restart display driver for {adapter.name}"
                    logging.info(f"Successfully to restart display driver for {adapter.name}")
        dut.reset()

    ##
    # @brief        Test function to make sure all the requirements are fulfilled before running other LRR test
    #               functions. Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start(f"Verifying adapter and panel requirements for LRR")
        for adapter in dut.adapters.values():
            # Check for adapter support
            if self.feature != LrrVersion.NO_LRR:
                if (self.feature == LrrVersion.LRR2_5 and adapter.name in common.PRE_GEN_12_PLATFORMS) or \
                        (self.feature == LrrVersion.LRR2_0 and adapter.is_yangra is False):
                    logging.error(f"{self.feature.name} is not supported on {adapter.name}")
                    gdhm.report_test_bug_os("[OsFeatures][LRR] Unsupported LRR version is requested by test",
                                            gdhm.ProblemClassification.LOG_FAILURE, gdhm.Priority.P4, gdhm.Exposure.E4)
                    self.fail("Unsupported LRR version is requested by test")
                logging.info(f"{self.feature.name} is supported on {adapter.name}")

            for panel in adapter.panels.values():
                # Multiple displays can be present in command line for display switching test, skip feature requirement
                # test for non-LFP panels
                if panel.is_lfp is False:
                    continue

                logging.info(f"{panel}")
                logging.info(f"\t{panel.psr_caps}")
                logging.info(f"\t{panel.drrs_caps}")
                logging.info(f"\t{panel.lrr_caps}")
                logging.info(f"\t{panel.vrr_caps}")

                if self.feature == LrrVersion.LRR1_0 and panel.lrr_caps.is_lrr_1_0_supported is False:
                    gdhm.report_test_bug_os(
                        f"[OsFeatures][LRR] Incorrect panel is being used for {self.feature.name} tests",
                        gdhm.ProblemClassification.LOG_FAILURE, gdhm.Priority.P3, gdhm.Exposure.E3)
                    self.fail(f"LRR1.0 is not supported on {panel.port}")

                if self.feature == LrrVersion.LRR2_0 and panel.lrr_caps.is_lrr_2_0_supported is False:
                    gdhm.report_test_bug_os(
                        f"[OsFeatures][LRR] Incorrect panel is being used for {self.feature.name} tests",
                        gdhm.ProblemClassification.LOG_FAILURE, gdhm.Priority.P3, gdhm.Exposure.E3)
                    self.fail(f"LRR2.0 is not supported on {panel.port}")

                if self.feature == LrrVersion.LRR2_5 and panel.lrr_caps.is_lrr_2_5_supported is False:
                    gdhm.report_test_bug_os(
                        f"[OsFeatures][LRR] Incorrect panel is being used for {self.feature.name} tests",
                        gdhm.ProblemClassification.LOG_FAILURE, gdhm.Priority.P3,
                        gdhm.Exposure.E3)
                    self.fail(f"LRR2.5 is not supported on {panel.port}")

                if self.feature == LrrVersion.NO_LRR and panel.lrr_caps.is_lrr_supported is True:
                    gdhm.report_test_bug_os(f"[OsFeatures][LRR] Incorrect panel is being used for negative LRR tests",
                                            gdhm.ProblemClassification.LOG_FAILURE, gdhm.Priority.P3,
                                            gdhm.Exposure.E3)
                    self.fail(f"LRR is supported on {panel.port}")

    ##
    # @brief        Test function to make sure all the requirements like HRR enabling are fulfilled before running
    #               LRR test functions involving HRR verification. Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_01_requirements(self):
        # Check for HRR feature support in active adapters and enable
        if self.is_hrr_test:
            if dut.is_feature_supported('HRR') is False:
                self.fail("None of the adapter supports HRR")
            for adapter in dut.adapters.values():
                if getattr(adapter, 'is_hrr_supported'):
                    html.step_start(f"Enabling HRR on {adapter.name}")
                    hrr_status = hrr.enable(adapter)
                    dut.refresh_panel_caps(adapter)
                    if hrr_status is False:
                        self.fail("FAILED to enable HRR (Test Issue)")
                    logging.info(f"\tPASS: Enabled HRR on {adapter.name}")
                    if hrr_status is True:
                        status, reboot_required = display_essential.restart_gfx_driver()
                        if status is False:
                            self.fail(f"Failed to restart display driver for {adapter.name}")
                        logging.info(f"Successfully to restart display driver for {adapter.name}")

    ##
    # @brief        Function to enable lrr
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_10_enable_lrr(self):
        for adapter in dut.adapters.values():
            logging.info(f"Step: Enabling {self.feature.name} on {adapter.name}")
            lrr_status = lrr.enable(adapter)
            if lrr_status is False:
                self.fail(f"FAILED to enable {self.feature.name} on {adapter.name}")

            if lrr_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail(f"Failed to restart display driver for {adapter.name}")
                logging.info(f"Successfully to restart display driver for {adapter.name}")
