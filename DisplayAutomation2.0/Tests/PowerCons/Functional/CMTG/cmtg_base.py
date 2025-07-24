#################################################################################################################
# @file         cmtg_base.py
# @brief        Contains base class for all CMTG tests
# @details      @ref cmtg_base.py <br>
#               This file implements unittest default functions for setUp and tearDown, common test functions used
#               across all cmtg tests, and helper functions.
#
# @author       Bhargav Adigarla
#################################################################################################################
import unittest
import logging
import sys

from Libs.Core import cmd_parser, display_essential, enum
from Libs.Core.display_power import DisplayPower
from Libs.Core.display_config import display_config
from Libs.Core.vbt.vbt import Vbt
from Tests.PowerCons.Modules import common, dut
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from DisplayRegs.DisplayArgs import TranscoderType
from Tests.PowerCons.Modules.dut_context import Adapter, Panel
from Tests.PowerCons.Functional.CMTG import cmtg


##
# @brief        Exposed Class to write CMTG tests. Any new CMTG test can inherit this class common setUp
#               and tearDown functions. CmtgBase also includes some functions used across all Cmtg tests.
class CmtgBase(unittest.TestCase):
    display_power_ = DisplayPower()
    display_config_ = display_config.DisplayConfiguration()
    cmd_line_param = None
    lfp_panels = []
    ext_panels = []
    method = 'GAME'

    ############################
    # Default UnitTest Functions
    ############################
    ##
    # @brief        This class method is the entry point for any CMTG test case. Helps to initialize some of the
    #               parameters required for CMTG test execution.
    # @details      This function checks for feature support and initialises parameters to handle
    #               multi-adapter scenarios in test cases
    # @return       None
    @classmethod
    def setUpClass(cls) -> None:
        logging.info(" SETUP: CMTG ".center(common.MAX_LINE_WIDTH, "*"))
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        if cls.cmd_line_param[0]['METHOD'] != 'NONE':
            cls.method = cls.cmd_line_param[0]['METHOD'][0].upper()

        dut.prepare()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is True:
                    cls.lfp_panels.append(panel)
                else:
                    cls.ext_panels.append(panel)

    ##
    # @brief        This method is the exit point for all CMTG test cases. This resets the environment changes done
    #               for the CMTG tests
    # @return       None
    @classmethod
    def tearDownClass(cls) -> None:
        dut.reset()

    # TODO: TO be enabled this after enabling port sync in driver
    ##
    # @brief        Test function is to configure port sync in VBT for port sync
    # @return       None
    # @cond
    # @common.configure_test(critical=True)
    # # @endcond
    # def t_00_requirements(self):
    #     gfx_vbt = Vbt()
    #     set_vbt = False
    #     self.panel1_index = gfx_vbt.block_40.PanelType
    #     panel1_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (1 << self.panel1_index)) >> \
    #                            self.panel1_index
    #     if panel1_port_sync_bit != 0:
    #         gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
    #             gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (0 << self.panel1_index)
    #         set_vbt = True
    #     else:
    #         logging.info("Port sync enabled in VBT for panel1")
    #
    #     if len(self.lfp_panels) == 2:
    #         self.panel2_index = gfx_vbt.block_40.PanelType2
    #         panel2_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (
    #                 1 << self.panel2_index)) >> self.panel2_index
    #         if panel2_port_sync_bit != 0:
    #             gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
    #                 gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (0 << self.panel2_index)
    #             set_vbt = True
    #         else:
    #             logging.info("Port sync enabled in VBT for panel2")
    #
    #     if set_vbt is True:
    #         if gfx_vbt.apply_changes() is False:
    #             self.fail('Setting VBT block 52 failed')
    #         else:
    #             if display_essential.restart_display_driver() is False:
    #                 self.fail("Failed to restart driver")
    #             gfx_vbt.reload()
    #             logging.info("Port sync enabled in VBT for panel1")
    #             logging.info("Port sync enabled in VBT for panel2")
    #
    #     if display_essential.restart_display_driver() is False:
    #         self.fail("Failed to restart driver")

    ##
    # @brief        This function is helper function for CMTG instance verification
    # @return       None
    def verify_cmtg(self):
        for adapter in dut.adapters.values():
            lfp_panels = []
            ext_panels  = []
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    if panel.port not in ["MIPI_A", "MIPI_C"]:
                        lfp_panels.append(panel)
                else:
                    ext_panels.append(panel)

            if len(lfp_panels) == 1:
                if lfp_panels[0].psr_caps.is_psr2_supported or lfp_panels[0].pr_caps.is_pr_supported:
                    if cmtg.verify(adapter, lfp_panels) is False:
                        self.fail("CMTG verification failed")
                    logging.info("CMTG verification successful")
                    if lfp_panels[0].vrr_caps.is_vrr_supported:
                        if cmtg.verify_cmtg_vrr(adapter,lfp_panels[0], self.method) is False:
                            self.fail("CMTG VRR sequence verification failed")
                        logging.info("CMTG VRR sequence verification successful")
                else:
                    status = cmtg.verify_cmtg_status(adapter)
                    if adapter.name in common.PRE_GEN_15_PLATFORMS:
                        if status:
                            self.fail("CMTG enabled in non-PSR2 panel")
                        logging.info("CMTG is not enabled in non PSR2 panel as expected")
                    # GEN15+ CMTG will be enabled on non-PSR panel as well
                    else:
                        if status is False:
                            self.fail("CMTG not enabled in non-PSR2 panel")
                        logging.info("CMTG enabled in non PSR2 panel as expected")

            if len(lfp_panels) == 2:
                for panel in lfp_panels:
                    if panel.psr_caps.is_psr2_supported or panel.pr_caps.is_pr_supported:
                        if self.display_config_.set_display_configuration_ex(enum.SINGLE, panel.port) is False:
                            self.fail("Applying Display config {0} Failed"
                                      .format(str(enum.SINGLE) + " " + " ".join(str(x) for x in panel.port)))
                        if cmtg.verify_cmtg_slave_status(adapter, panel) is True:
                            if cmtg.verify(adapter, [panel]) is False:
                                self.fail("CMTG verification failed")
                            logging.info("CMTG verification successful")
                            if panel.vrr_caps.is_vrr_supported:
                                if cmtg.verify_cmtg_vrr(adapter,panel, self.method) is False:
                                    self.fail("CMTG VRR sequence verification failed")
                                logging.info("CMTG VRR sequence verification successful")
                    else:
                        status = cmtg.verify_cmtg_status(adapter)
                        if adapter.name in common.PRE_GEN_15_PLATFORMS:
                            if status:
                                self.fail("CMTG enabled in non-PSR2 panel")
                            logging.info("CMTG is not enabled in non PSR2 panel as expected")
                        # GEN15+ CMTG will be enabled on non-PSR panel as well
                        else:
                            if status is False:
                                self.fail("CMTG not enabled in non-PSR2 panel")
                            logging.info("CMTG enabled in non PSR2 panel as expected")
