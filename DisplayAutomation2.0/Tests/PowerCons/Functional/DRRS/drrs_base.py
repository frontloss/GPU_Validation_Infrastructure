#################################################################################################################
# @file         drrs_base.py
# @section      DRRS_Tests
# @brief        Contains base class for DRRS tests
#
# @author       Rohit Kumar
#################################################################################################################

import logging
import sys
import time
import unittest

from Libs.Core import app_controls, cmd_parser, display_essential
from Libs.Core.display_power import DisplayPower
from Libs.Core.logger import html, gdhm
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import dut, common, workload
from Tests.PowerCons.Modules.workload import PowerSource


##
# @brief        Exposed Class to write DRRS tests. Any new DRRS test can inherit this class to use common setUp and
#               tearDown
#               functions.
class DrrsBase(unittest.TestCase):
    cmd_line_param = None
    display_power_ = DisplayPower()
    method = "IDLE"
    is_drrs_expected = True
    disable_lrr = False
    is_static_drrs = False

    ##
    # @brief        This class method is the entry point for any DRRS test cases. Helps to initialize few of the
    #               parameters required for the DRRS test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS + ['-STATIC_DRRS'])

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        if cls.cmd_line_param[0]['METHOD'] != 'NONE':
            cls.method = cls.cmd_line_param[0]['METHOD'][0]

        if cls.cmd_line_param[0]['FEATURE'] != 'NONE':
            cls.is_drrs_expected = cls.cmd_line_param[0]['FEATURE'][0] != 'NO_DRRS'

        if cls.cmd_line_param[0]['DISABLE_LRR'] != 'NONE':
            cls.disable_lrr = True

        if cls.cmd_line_param[0]['STATIC_DRRS'] != 'NONE':
            cls.is_static_drrs = True

        dut.prepare(PowerSource.DC_MODE)

    ##
    # @brief        This method is the exit point for all DRRS test cases. This resets the environment changes done for
    #               DRRS tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        dut.reset()

        # Enable back LRR/ PSR after est
        for adapter in dut.adapters.values():
            if cls.is_static_drrs:
                for panel in adapter.panels.values():
                    if drrs.configure_drrs_panel_type(adapter, panel, drrs.DrrsType.SEAMLESS_DRRS) is False:
                        assert False, f"FAILED to enable SEAMLESS DRRS for {panel.port} on {adapter.gfx_index}"

            if cls.disable_lrr is True:
                if lrr.enable(adapter) is False:
                    assert False, f"Failed to enable LRR on {adapter.name}"
            else:
                html.step_start("Enabling PSR back after test")
                psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)

            # Restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.error("Failed to restart display driver")
            else:
                logging.info("Successfully restarted display driver")
            html.step_end()

    ##
    # @brief        This method verifies adapter and panel requirements for DRRS
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start(f"Verifying adapter and panel requirements for DRRS")
        for adapter in dut.adapters.values():
            logging.info(f"\tDRRS is supported on {adapter.name}")

            is_drrs_panel_present = False

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
                logging.info(f"\t{panel}")
                logging.info(f"\t\t{panel.psr_caps}")
                logging.info(f"\t\t{panel.drrs_caps}")
                logging.info(f"\t\t{panel.vrr_caps}")
                logging.info(f"\t\t{panel.lrr_caps}")
                logging.info(f"\t\t{panel.mso_caps}")
                logging.info(f"\t\t{panel.bfr_caps}")

                is_drrs_panel_present |= panel.drrs_caps.is_drrs_supported

            if self.is_drrs_expected and is_drrs_panel_present is False:
                gdhm.report_test_bug_os("[OsFeatures][DRRS] Unsupported panels are being used for DRRS tests",gdhm.ProblemClassification.OTHER,gdhm.Priority.P3,
                    gdhm.Exposure.E3)
                self.fail(f"No DRRS supported panel is connected to {adapter.name}")
        html.step_end()

    ##
    # @brief        This method enables drrs on the adapter
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_10_enable_drrs(self):
        for adapter in dut.adapters.values():
            lrr_status = None
            psr_status = None
            if self.disable_lrr is True:
                lrr_status = lrr.disable(adapter)
                if lrr_status is False:
                    self.fail(f"Failed to disable LRR on {adapter.name}")
                dut.refresh_panel_caps(adapter)
            else:
                html.step_start(f"Disabling PSR on {adapter.name}")
                psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                if psr_status is False:
                    self.fail(f"FAILED to disable PSR for {adapter.name}")
                html.step_end()

            html.step_start(f"Enabling DRRS on {adapter.name}")
            drrs_status = drrs.enable(adapter)
            if drrs_status is False:
                self.fail(f"Failed to enable DRRS on {adapter.name}")
            html.step_end()

            if psr_status or drrs_status or lrr_status:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail(f"Failed to restart display driver for {adapter.name}")
                logging.info(f"Successfully to restart display driver for {adapter.name}")

            if self.is_static_drrs:
                for panel in adapter.panels.values():
                    if drrs.configure_drrs_panel_type(adapter, panel, drrs.DrrsType.STATIC_DRRS) is False:
                        self.fail(f"FAILED to enable STATIC DRRS for {panel.port} on {adapter.name}")

            dut.refresh_panel_caps(adapter)

    ##
    # @brief        This method verifies if RR switching is detected or not
    # @param[in]    vbt_disabled_panels list, consisting of tuple (adapter.gfx_index, panel.port)
    # @param[in]    verify_watermark boolean, to indicate if watermark verification is required during the workload
    # @param[in]    wm_during_rr_switch boolean, to verify Watermark programming during rr switching
    # @return       None
    def verify_drrs(self, vbt_disabled_panels=None, verify_watermark=False, wm_during_rr_switch=False):
        monitors = app_controls.get_enumerated_display_monitors()
        monitor_ids = [_[0] for _ in monitors]
        watermark_status = True
        wm_status_during_workload = None
        if vbt_disabled_panels is None:
            vbt_disabled_panels = []

        for adapter in dut.adapters.values():

            if self.method == 'IDLE':
                if verify_watermark:
                    etl_file, polling_data, wm_status_during_workload = workload.run(workload.IDLE_DESKTOP,
                                                                                     [30, False, adapter.gfx_index])
                else:
                    etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
            else:
                if verify_watermark:
                    etl_file, polling_data = workload.run(workload.SCREEN_UPDATE,
                                                          [monitor_ids, adapter.gfx_index])
                else:
                    etl_file, _ = workload.run(workload.SCREEN_UPDATE, [monitor_ids])

            for panel in adapter.panels.values():
                if panel.is_active is False:
                    logging.info(f"{panel.port} is not active panel. Skipping verification")
                    continue

                if panel.drrs_caps.is_drrs_supported is False or (adapter.gfx_index, panel.port) in vbt_disabled_panels:
                    if panel.drrs_caps.is_drrs_supported is False:
                        html.step_start(f"Verify no RR change for {panel.port} (Non-DRRS)")
                        title = "[PowerCons][DRRS] RR switching is happening on non-DRRS panel"
                    else:
                        html.step_start(f"Verify no RR change for {panel.port} (Disabled in VBT)")
                        title = "[PowerCons][DRRS] RR switching is happening when disabled from VBT"

                    # RR should not change for Non-DRRS panels
                    rr_change_status = drrs.is_rr_changing(adapter, panel, etl_file)
                    if rr_change_status is None:
                        self.fail(f"ETL report generation FAILED")

                    if rr_change_status is False:
                        if panel.drrs_caps.is_drrs_supported is False:
                            logging.info(f"\tPASS: No refresh rate switching detected on Non-DRRS panel {panel.port}")
                        else:
                            logging.info(f"\tPASS: NO refresh rate switching detected with DRRS disabled in VBT")
                    else:
                        gdhm.report_driver_bug_os(title)
                        if panel.drrs_caps.is_drrs_supported:
                            self.fail(f"RefreshRate switching is detected on {panel.port} with DRRS disabled in VBT")
                        self.fail(f"RefreshRate switching is happening on Non-DRRS panel {panel.port}")
                    html.step_end()
                else:
                    if drrs.verify(adapter, panel, etl_file) is False:
                        drrs.is_rr_changing(adapter, panel, etl_file)
                        self.fail(f"FAIL: DRRS verification for {panel.port}")
                    if wm_during_rr_switch:
                        watermark_status &= drrs.verify_watermark_during_rr_switch(adapter, panel, etl_file)

                    if watermark_status is False:
                        self.fail(f"FAIL: Watermark Verification with RR switch for {panel.port}")
