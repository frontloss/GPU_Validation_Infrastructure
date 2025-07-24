########################################################################################################################
# @file         flt_base.py
# @brief        Base class for eDP FLT verification test cases
# @author       Tulika
########################################################################################################################

import logging
import sys
import unittest

from Libs.Core import display_essential, cmd_parser
from Libs.Core.display_config import display_config
from Libs.Core.logger import html
from Libs.Core.vbt.vbt import Vbt
from Tests.EDP.FLT import flt
from Tests.PowerCons.Modules import common, dut


##
# @brief       This class contains setup, teardown and test functions for FLT test cases
class EdpFltBase(unittest.TestCase):
    vbt = None
    cmd_line_param = None
    flt_params = {}
    is_flt_enabled = True
    is_phy_test = False
    vswing_table = None

    display_config_ = display_config.DisplayConfiguration()

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This method initializes and prepares the setup required for execution of tests in this class
    # @details      It parses the command line, checks for eDP connections and sets display configuration
    # @return       None
    @classmethod
    def setUpClass(cls):

        logging.info(" SETUP: FLT_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        if cls.cmd_line_param['FLT'] != 'NONE' and cls.cmd_line_param['FLT'][0] == 'FALSE':
            cls.is_flt_enabled = False

        if cls.cmd_line_param['PHY'] != 'NONE' and cls.cmd_line_param['PHY'][0] == 'TRUE':
            cls.is_phy_test = True

        if cls.cmd_line_param['VSWING_TABLE'] != 'NONE':
            cls.vswing_table = cls.cmd_line_param['VSWING_TABLE'][0]

        dut.prepare()

    ##
    # @brief        This function resets the changes done for execution of the EDP FLT tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: FLT_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        dut.reset()
        cls.vbt = Vbt()
        logging.info("Resetting VBT")
        if Vbt().reset() is False:
            logging.warning("\tResetting VBT failed")
        else:
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.warning("\tFAILED to restart display driver post VBT reset")
            logging.info("Successfully restarted driver post VBT reset")

    ################
    # Test Function
    ################

    ##
    # @brief       This tests check FLT support in VBT and set Vswing table for physical panel
    # @return      None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start("Verifying adapter and panel requirements for FLT")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info(f"{panel.edp_caps}")
                if panel.is_lfp is False:
                    continue
                vbt = Vbt(adapter.gfx_index)
                panel_index = vbt.get_lfp_panel_type(panel.port)
                if self.is_flt_enabled and not flt.is_supported_in_panel(panel):
                    html.step_end()
                    self.fail(f"FAIL: FastLinkTraining is NOT supported on {panel.port}")
                if self.is_flt_enabled:
                    logging.info("PASS: FastLinkTraining status Expected= SUPPORTED, Actual= SUPPORTED")

                vbt_vswing_table = vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)]

                logging.info(f"VSwingPreEmphasisTableSelection[{int(panel_index / 2)}]= {hex(vbt_vswing_table)}")

                if self.is_phy_test is True:
                    # @Todo add the below check VSDI-34785, the deployed cmdlines with -phy tag needs to be disabled
                    # if common.is_simulated_panel(panel.target_id) is True:
                    #    self.fail(f"FAIL: Simulated panel not supported (Planning Issue)")
                    if self.vswing_table is not None:
                        flt.set_vswing_table(panel_index, table=self.vswing_table)
                    else:
                        flt.set_vswing_table(panel_index, table='LOW' if vbt_vswing_table == 0 else 'DEFAULT')
        html.step_end()

    ##
    # @brief        This test Enables/Disables FLT settings in VBT and verifies it for eDP panels
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_10_enable_flt(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                vbt = Vbt(adapter.gfx_index)
                panel_index = vbt.get_lfp_panel_type(panel.port)
                if self.is_flt_enabled:
                    html.step_start(f"Enabling FastLinkTraining in VBT for {panel.port}")
                    self.flt_params[panel] = flt.enable(panel, panel_index)
                    if self.flt_params[panel] is None:
                        self.fail(f"FAILED to enable FLT on {panel.port}")
                    logging.info(f"Successfully enabled FastLinkTraining in VBT for {panel.port}")
                    html.step_end()
                else:
                    # If expected FLT enabled is False, check the panel support for FLT. If FLT is not supported, Skip
                    # If FLT is supported, disable it in VBT
                    if flt.is_supported_in_panel(panel):
                        html.step_start(f"Disabling FastLinkTraining in VBT for {panel.port}")
                        if flt.disable(panel_index) is False:
                            self.fail(f"FAILED to disable FastLinkTraining in VBT for {panel.port}")
                        logging.info(f"Successfully disabled FastLinkTraining in VBT for {panel.port}")
                        html.step_end()

