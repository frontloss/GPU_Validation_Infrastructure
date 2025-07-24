########################################################################################################################
# @file         dmrrs_base.py
# @brief        Base class for all DMRRS tests
# @details      This file implements setUp and tearDown methods of unittest framework.
#               In setUp, command_line arguments are parsed, eDP panel's existence is checked, multi RR support is
#               checked in eDP and external displays passed through the commandline are plugged.
#               In tearDown method, the displays which were plugged in the setUp method are unplugged and TDR check is
#               done.
# @author       Vinod D S, Rohit Kumar
########################################################################################################################

import logging
import sys
import unittest

from Libs.Core import cmd_parser, display_essential, enum, window_helper
from Libs.Core.display_config import display_config
from Libs.Core import display_power
from Libs.Core.logger import html, gdhm
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Tests.PowerCons.Functional.DMRRS import dmrrs, hrr
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, dut
from Tests.PowerCons.Modules.dut_context import Adapter, Panel, RrSwitchingMethod


##
# @brief        Exposed Class to write DMRRS tests. Any new DMRRS test can inherit this class to use common setUp and
#               tearDown functions. DmrrsBase also includes some functions used across all VRR tests.
class DmrrsBase(unittest.TestCase):
    cmd_line_param = None
    is_fractional_rr = False
    is_hrr_test = False
    is_dmrrs_expected = True
    is_video_loop_expected = False
    disable_lrr = False
    with_psr = False
    FRACTIONAL_FPS = [23.976, 29.970, 59.940]
    NORMAL_FPS = [24, 25, 30]
    video_file = dmrrs.VIDEO_FILE_MAPPING['24']
    duration_in_seconds = 30

    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    under_run_monitor_ = UnderRunStatus()

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for any DMRRS test case. Helps to initialize some of the
    #               parameters required for DMRRS test execution.
    # @details      This function checks for feature support and initialises parameters to handle
    #               multi-adapter scenarios in test cases
    # @return       None
    @classmethod
    def setUpClass(cls):
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        cls.is_fractional_rr = cls.cmd_line_param[0]['FRACTIONAL_RR'] != 'NONE'
        cls.is_hrr_test = cls.cmd_line_param[0]['HRR'] != 'NONE'
        cls.is_video_loop_expected = cls.cmd_line_param[0]['LOOP_VIDEO'] != 'NONE'

        if cls.cmd_line_param[0]['FEATURE'] != 'NONE':
            if cls.cmd_line_param[0]['FEATURE'][0] == 'NO_DMRRS':
                cls.is_dmrrs_expected = False

        if cls.cmd_line_param[0]['DISABLE_LRR'] != 'NONE':
            cls.disable_lrr = True

        # Check for PSR sequence in HRR test. For that we need to keep PSR enable
        if cls.cmd_line_param[0]['WITH'] != 'NONE':
            if cls.cmd_line_param[0]['WITH'][0] == 'PSR':
                cls.with_psr = True

        # Check for feature support in active adapters
        if cls.is_hrr_test:
            assert dut.is_feature_supported('HRR'), "None of the adapter supports HRR"

        # Get Video and map the file
        if cls.cmd_line_param[0]['VIDEO'] != 'NONE':
            video = cls.cmd_line_param[0]['VIDEO'][0]
            assert video in dmrrs.VIDEO_FILE_MAPPING.keys(), f"{video} video is invalid/ unavailable (Commandline issue)"
            cls.video_file = dmrrs.VIDEO_FILE_MAPPING[video]

        if cls.cmd_line_param[0]['DURATION'] != 'NONE':
            cls.duration_in_seconds = int(cls.cmd_line_param[0]['DURATION'][0])

        dut.prepare(power_source=display_power.PowerSource.DC)

    ##
    # @brief        This method is the exit point for all DMRRS test cases. This resets the environment changes done
    #               for the DMRRS tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        dut.reset()
        window_helper.close_media_player()
        # Enable PSR back OR LRR back after test
        for adapter in dut.adapters.values():
            if cls.is_hrr_test is True:
                hrr.disable(adapter)
                hrr.disable_d13_hrr(adapter)
                dut.refresh_panel_caps(adapter)
            if cls.disable_lrr is True:
                if lrr.enable(adapter) is False:
                    assert False, f"Failed to enable LRR on {adapter.name}"
            else:
                html.step_start("Enabling PSR back after test")
                psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                if psr_status is False:
                    assert False, "FAILED to enable PSR through registry key"
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                assert False, "FAILED to restart driver"
        html.step_end()

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test function to make sure all the requirements are fulfilled before running other test functions.
    #               Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start(f"Verifying adapter and panel requirements for {'HRR' if self.is_hrr_test else 'DMRRS'}")
        for adapter in dut.adapters.values():
            # Check for adapter support
            if self.is_dmrrs_expected:
                if self.is_hrr_test and adapter.is_yangra is False:
                    logging.error(f"HRR is not supported on {adapter.name}")
                    gdhm.report_test_bug_os("[OsFeatures][HRR] HRR test is running on unsupported platform", gdhm.ProblemClassification.LOG_FAILURE,gdhm.Priority.P3,
                        gdhm.Exposure.E3)
                    self.fail(f"HRR is not supported on {adapter.name}")
                else:
                    logging.info(f"\t{'HRR' if self.is_hrr_test else 'DMRRS'} is supported on {adapter.name}")

            if self.disable_lrr is False:
                if adapter.name not in common.PRE_GEN_14_PLATFORMS:
                    psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                    if psr_status:
                        status, reboot_required = display_essential.restart_gfx_driver()
                        if status is False:
                            self.fail(f"Failed to restart display driver for {adapter.name}")
                        logging.info(f"\tSuccessfully restarted display driver for {adapter.name} after disabling PSR")

            dut.refresh_panel_caps(adapter)

            for panel in adapter.panels.values():
                logging.info("\t{0}".format(panel))
                logging.info("\t\t{0}".format(panel.psr_caps))
                logging.info("\t\t{0}".format(panel.drrs_caps))
                logging.info("\t\t{0}".format(panel.vrr_caps))
                logging.info("\t\t{0}".format(panel.lrr_caps))
                logging.info("\t\t{0}".format(panel.bfr_caps))

                if self.is_dmrrs_expected and panel.drrs_caps.is_dmrrs_supported is False:
                    self.fail(f"DMRRS is NOT supported on {panel.port}")

    ##
    # @brief        Test function to make sure all the requirements are fulfilled before running other test functions.
    # @details      Disabling PSR, Enabling Media Refresh Rate and Enabling HRR are
    #               Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_10_enable_dmrrs(self):
        for adapter in dut.adapters.values():
            lrr_status = None
            psr_status = None
            if self.with_psr is False:
                if self.disable_lrr is True:
                    lrr_status = lrr.disable(adapter)
                    if lrr_status is False:
                        self.fail(f"FAILED to disable LRR on {adapter.name}")
                else:
                    html.step_start(f"Disabling PSR on {adapter.name}")
                    psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                    if psr_status is False:
                        self.fail(f"FAILED to disable PSR on {adapter.name}")
                    html.step_end()

            html.step_start(f"Enabling DMRRS(MediaRefreshRateSupport) for {adapter.name}")
            dmrrs_status = dmrrs.enable(adapter)
            if dmrrs_status is False:
                self.fail("FAILED to enable DMRRS (Test Issue)")
            logging.info("\tPASS: Enabled DMRRS")
            html.step_end()

            if self.is_hrr_test:
                html.step_start("Enabling HRR for {0}".format(adapter.name))
                hrr_status = hrr.enable(adapter)
                dut.refresh_panel_caps(adapter)
                if hrr_status is False:
                    self.fail("Failed to enable HRR (Test Issue)")
                logging.info(f"\tPASS: Enabled HRR on {adapter.name}")
                html.step_end()
                d13_hrr_status = hrr.enable_d13_hrr(adapter)
                if d13_hrr_status is False:
                    self.fail("Failed to enable D13 HRR (Test Issue)")
            else:
                html.step_start("Disabling HRR for {0}".format(adapter.name))
                hrr_status = hrr.disable(adapter)
                dut.refresh_panel_caps(adapter)
                if hrr_status is False:
                    self.fail("Failed to disable HRR (Test Issue)")
                logging.info(f"\tPASS: Disabled HRR on {adapter.name}")
                html.step_end()
                d13_hrr_status = hrr.disable_d13_hrr(adapter)
                if d13_hrr_status is False:
                    self.fail("Failed to disable D13 HRR (Test Issue)")

            if psr_status or dmrrs_status or lrr_status or hrr_status or d13_hrr_status:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail(f"Failed to restart display driver for {adapter.name}")
                logging.info(f"\tSuccessfully to restart display driver for {adapter.name}")

            for panel in adapter.panels.values():
                # If PSR2 is disabled, RR switching method should be VTOTAL_HW
                if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.VTOTAL_SW:
                    if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2) is False:
                        logging.info("\tPSR2 is disabled. Updated RR_SWITCH METHOD from VTOTAL_SW to VTOTAL_HW")
                        panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW

    ##
    # @brief        Contains common steps for DMRRS/HRR verification used across tests
    # @param[in]    adapter Adapter
    # @param[in]    panel Panel
    # @param[in]    etl_file_path String, path to ETL file
    # @param[in]    media_fps float
    # @param[in]    is_disabled_in_vbt bool
    # @param[in]    wm_during_rr_switch bool, to verify watermark programming during rr switch
    # @return       None
    def dmrrs_hrr_verification(self, adapter: Adapter, panel: Panel, etl_file_path: str, media_fps: float,
                               is_disabled_in_vbt: bool = False, wm_during_rr_switch: bool = False):
        if self.is_dmrrs_expected is False or is_disabled_in_vbt:
            if self.is_dmrrs_expected is False:
                html.step_start(f"Verify no RR change on {panel.port} (Non-DMRRS)")
                title = "[PowerCons][DMRRS] RR switching is happening on non-DMRRS panel"
            else:
                html.step_start(f"Verify no RR change on {panel.port} (Disabled in VBT)")
                title = "[PowerCons][DMRRS] RR switching is happening when disabled from VBT"

            if dmrrs.is_dmrrs_changing_rr(adapter, panel, etl_file_path, media_fps):
                gdhm.report_driver_bug_os(title,gdhm.ProblemClassification.FUNCTIONALITY,gdhm.Priority.P3,
                    gdhm.Exposure.E3)
                reason = "when DMRRS is disabled in VBT" if is_disabled_in_vbt else "on Non-DMRRS panel"
                self.fail(f"Refresh Rate change due to DMRRS detected {reason}")
            logging.info("\tPASS: No Refresh Rate change detected")
            html.step_end()
            return

        dmrrs_status = True
        if not self.is_hrr_test:
            dmrrs_status &= dmrrs.verify(adapter, panel, etl_file_path, media_fps)

        dmrrs_exit_status = dmrrs.verify_dmrrs_exit(adapter, panel)
        hrr_status = True
        if self.is_hrr_test:
            hrr_status = hrr.verify(adapter, panel, etl_file_path, media_fps)

        if (not self.is_hrr_test) and (dmrrs_status is False):
            self.fail("DMRRS verification failed with media FPS= {0}".format(media_fps))

        if dmrrs_exit_status is False:
            self.fail("DMRRS Exit verification failed with media FPS= {0}".format(media_fps))

        if self.is_hrr_test and hrr_status is False:
            self.fail("HRR verification failed with media FPS= {0}".format(media_fps))

        if wm_during_rr_switch:
            if drrs.verify_watermark_during_rr_switch(adapter, panel, etl_file_path) is False:
                self.fail(f"FAIL: Watermark Verification with RR switch for {panel.port}")
