#######################################################################################################################
# @file         ubrr_base.py
# @brief        Contains the base TestCase class for all UBRR tests, New UBRR tests can be created by inheriting this
#               class and adding new test functions.
#
# @author       Vinod D S
#######################################################################################################################
import logging
import os
import sys
import time
import unittest
from Libs.Core import cmd_parser
from Libs.Core.logger import etl_tracer, html
from Libs.Core.test_env import test_context
from Tests.PowerCons.Modules import common, dut
from Tests.IDT.UBRR import ubrr


##
# @brief        Exposed Class to write UBRR tests. Any new test can inherit this class to use common setUp and tearDown
#               functions.
class UbrrBase(unittest.TestCase):
    cmd_line_param = None
    requested_ubrr_type = ubrr.UbrrType.NONE

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

        cls.requested_ubrr_type = ubrr.UbrrType.UBALL
        if cls.cmd_line_param[0]['UBZRR'] != 'NONE':
            cls.requested_ubrr_type = ubrr.UbrrType.UBZRR
        if cls.cmd_line_param[0]['UBLRR'] != 'NONE':
            cls.requested_ubrr_type = ubrr.UbrrType.UBLRR

        dut.prepare()

    ##
    # @brief        This method is the exit point for all UBRR test cases. This resets the environment changes for the
    #               UBRR tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if cls.cmd_line_param[0]['SELECTIVE2'] != 'NONE' \
                        and cls.cmd_line_param[0]['SELECTIVE2'][0] == 'ENABLE_IN_IGCL':
                    continue
                ubrr.disable(adapter, panel)
        dut.reset()

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test function is to verify system and panel requirements for UBRR test
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start("Verify system and panel requirements for UBRR test")
        for adapter in dut.adapters.values():
            logging.info(f"Active panel capabilities for {adapter.name}")
            for panel in adapter.panels.values():
                logging.info(f"\t{panel}")
                if panel.is_lfp is False:
                    continue
                logging.info(f"\t\t{panel.psr_caps}")
                logging.info(f"\t\t{panel.idt_caps}")
        html.step_end()

    ##
    # @brief        Test function to clear UBRR if enabled before starting the test
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_10_clear(self):
        html.step_start("Disabling UBRR if enabled before starting the test")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                ubrr.disable(adapter, panel)
        html.step_end()

    ##
    # @brief        Test function to make sure VRR is disabled
    # @param[in]    adapter - object of Adapter
    # @param[in]    panel - object of Panel
    # @param[in]    skip_disable whether to disable UBRR at the end or not
    # @return       None
    def validate_ubrr(self, adapter, panel, skip_disable=False):
        if adapter.name in common.PRE_GEN_13_PLATFORMS + ["DG2"]:
            logging.info("\tUBRR is not supported on pre-ADLP platform, skipping verification..")
            return

        if panel.is_lfp is False:
            logging.info("\tUBRR is not supported on external panel, skipping verification..")
            return

        etl_tracer.stop_etl_tracer()
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            etl_file_path = os.path.join(test_context.LOG_FOLDER, 'GfxTraceBeforeTest.' + str(time.time()) + '.etl')
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

        # Negative cases
        test_seq = [self.requested_ubrr_type]
        if self.requested_ubrr_type == ubrr.UbrrType.UBALL:
            test_seq = [ubrr.UbrrType.UBLRR, ubrr.UbrrType.UBZRR]

        # Positive cases
        if panel.idt_caps.is_ubzrr_supported and self.requested_ubrr_type == ubrr.UbrrType.UBZRR:
            test_seq = [ubrr.UbrrType.UBZRR, ubrr.UbrrType.NONE]
        if panel.idt_caps.is_ublrr_supported and self.requested_ubrr_type == ubrr.UbrrType.UBLRR:
            test_seq = [ubrr.UbrrType.UBLRR, ubrr.UbrrType.NONE]
        if panel.idt_caps.is_ubzrr_supported and panel.idt_caps.is_ublrr_supported \
                and self.requested_ubrr_type == ubrr.UbrrType.UBALL:
            test_seq = [ubrr.UbrrType.UBZRR, ubrr.UbrrType.UBLRR, ubrr.UbrrType.NONE,
                        ubrr.UbrrType.UBLRR, ubrr.UbrrType.UBZRR, ubrr.UbrrType.NONE]

        negative = (ubrr.UbrrType.NONE not in test_seq)
        if skip_disable is True and negative is False:
            # Remove all the occurrences of ubrr.UBRR.NONE
            test_seq = list(filter(ubrr.UbrrType.NONE.__ne__, test_seq))

        status = True
        for test_step in test_seq:
            if etl_tracer.start_etl_tracer() is False:
                self.fail("FAILED to start ETL Tracer")

            if test_step == ubrr.UbrrType.NONE:
                state = ubrr.disable(adapter, panel)
            else:
                state = ubrr.enable(adapter, panel, test_step)

            if state is False:
                self.fail("FAILED to enable/disable UBRR via Control API")

            etl_tracer.stop_etl_tracer()
            etl_file_path = 'GfxTrace' + panel.port + (
                'DISABLE' if test_step == ubrr.UbrrType.NONE else test_step.name) + '.' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, etl_file_path)
            if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
                os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

            if ubrr.verify(adapter, panel, etl_file_path, test_step, negative) is False:
                logging.error(f"\tFAILED to verify "
                              f"UBRR {'DISABLE' if test_step == ubrr.UbrrType.NONE else test_step.name} "
                              f"programming in DPCD on {panel.port} on {adapter.name}")
                status = False
            else:
                logging.info(f"\tUBRR {'DISABLE' if test_step == ubrr.UbrrType.NONE else test_step.name} "
                             f"programming is verified in DPCD on {panel.port} on {adapter.name}")

            # time to wait before applying next
            time.sleep(5)

        if status is False:
            self.fail(f"FAILED to verify UBRR on {panel.port} on {adapter.name}")
        logging.info(f"\tUBRR verification is successful on {panel.port} on {adapter.name}")
