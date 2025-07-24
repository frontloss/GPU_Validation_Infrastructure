#######################################################################################################################
# @file         pixoptix_base.py
# @brief        Contains the base TestCase class for all PIxOptix tests, New PixOptix tests can be
#               created by inheriting this class and adding new test functions.
#
# @author       Ravichandran M
#######################################################################################################################

import logging
import sys
import unittest
from Libs.Core import cmd_parser
from Libs.Core.logger import gdhm, html
from Tests.IDT.PixOptix import pixoptix
from Tests.PowerCons.Modules import common, dut, workload
from Libs.Core.vbt import vbt
from Libs.Core import display_essential


##
# @brief        Exposed Class to write PixOptix tests. Any new test can inherit this class to
#               use common setUp and tearDown functions.
class PixoptixBase(unittest.TestCase):
    cmd_line_param = None

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for any PixOptix test case. Helps to initialize some of the
    #               parameters required for PixOptix test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenarios
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]
        # Need to check if we need PixOptix command line tag or not.

        dut.prepare(power_source=workload.PowerSource.DC_MODE)

    ##
    # @brief        This method is the exit point for all PixOptix test cases. This resets the environment
    # changes for the PixOptix tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: PixOptix ".center(common.MAX_LINE_WIDTH, "*"))
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if pixoptix.disable_pixoptix_in_vbt(adapter, panel) is False:
                    assert False, "FAILED to disable PixOptix in VBT"
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                assert False, "Failed to restart display driver after VBT update"
            vbt.Vbt(adapter.gfx_index).reload()
        dut.reset()

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test function is to verify system and panel requirements for PixOptix test
    # @return       None
    # @cond

    @common.configure_test(critical=True)
    # @endcond
    def t_00_pixoptix_panel_requirements(self):
        html.step_start("Verify system and panel requirements for PixOptix test")
        for adapter in dut.adapters.values():
            logging.info(f"Active panel capabilities for {adapter.name}")
            for panel in adapter.panels.values():
                logging.info(f"\t{panel}")
                if panel.is_lfp is False:
                    continue
                logging.info(f"\t\t{panel.psr_caps}")
                logging.info(f"\t\t{panel.idt_caps}")
                if not panel.idt_caps.is_pixoptix_supported:
                    self.fail(f"Pixoptix is not supported on current panel {panel.port}")
                    gdhm.report_driver_bug_pc(
                        "[PowerCons][IDT-PixOptix] IDT requirement for PixOptix is not met from panel side")
        html.step_end()

    ################
    # Test Function
    ################

    ##
    # @brief       This tests check PixOptix support in VBT, Panel and IGCL
    # @return      None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_01_vbt_requirements(self):
        html.step_start("Enabling VBT changes for PixOptix Feature")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue

                if pixoptix.enable_pixoptix_in_vbt(adapter, panel) is False:
                    self.fail(f"FAILED to enable PixOptix  in VBT")

            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                self.fail("Failed to restart display driver after VBT update")
            vbt.Vbt(adapter.gfx_index).reload()
            for panel in adapter.panels.values():
                if pixoptix.is_enabled_in_igcl(panel.target_id) is not True:
                    self.fail("PixOptix feature is not supported/ enabled in IGCL")
                logging.info("PixOptix IGCL Get call status is successfull and feature is enabled")

    ##
    # @brief        Test function to make sure PixOptix is enabled
    # @param[in]    adapter - object of Adapter
    # @param[in]    panel - object of Panel
    # @param[in]    negative Boolean - True if PixOptix should not work, False otherwise
    # @return       None
    def validate_pixoptix(self, adapter, panel, negative=False):
        status = True
        if adapter.name in common.PRE_GEN_13_PLATFORMS + ["DG2"]:
            logging.info("\tPixOptix is not supported on pre-ADLP paltform, skipping verification..")
            return
        if panel.is_lfp is False:
            logging.info("\tPixOptix is not supported on external panel, skipping verification..")
            return

        status, etl_file_path = workload.etl_tracer_stop_existing_and_start_new(
            f"GfxTrace_{panel.port}_PixOptix_Enable")
        if status is False:
            self.fail("FAILED to get ETL during PixOptix Enable case")

        if pixoptix.verify(adapter, panel, etl_file_path, negative) is False:
            self.fail(f"\tFAILED to verify "
                      f"PixOptix {'DISABLE' if negative else 'ENABLE'} "
                      f"programming in DPCD on {panel.port} on {adapter.name}")

        logging.info(f"\tPixOptix {'DISABLE' if negative else 'ENABLE'} "
                     f"programming is verified in DPCD on {panel.port} on {adapter.name}")
