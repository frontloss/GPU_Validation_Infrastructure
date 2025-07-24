#######################################################################################################################
# @file         port_sync_base.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        This file contains common setUp and tearDown steps for all port sync tests.
#               Also contains the dynamic pipe allocation method
# @author       Bhargav Adigarla
#######################################################################################################################

import unittest
import logging
import sys

from Libs.Core import enum
from Libs.Core import cmd_parser, display_power, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.sw_sim import driver_interface
from registers.mmioregister import MMIORegister
from Tests.PowerCons.Modules import common, dut, desktop_controls
from Libs.Feature.powercons import registry
from Libs.Core import registry_access
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Core.vbt.vbt import Vbt
from Tests.PowerCons.Functional.CMTG import cmtg
from Tests.PowerCons.Functional.PORTSYNC import port_sync


##
# @brief        Exposed Class to write portsync tests. Any new port sync test can inherit this class common setUp
#               and tearDown functions.
class PortSyncBase(unittest.TestCase):
    cmd_line_param = None
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    lfp_panels = []
    ext_panels = []
    driver_interface_ = driver_interface.DriverInterface()
    symmetric_panels = False

    ############################
    # Default UnitTest Functions
    ############################
    ##
    # @brief        This class method is the entry point for any port sync test case. Helps to initialize some of the
    #               parameters required for port sync test execution.
    # @details      This function checks for feature support and initialises parameters to handle
    #               multi-adapter scenarios in test cases
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info(" SETUP: PORT_SYNC ".center(common.MAX_LINE_WIDTH, "*"))
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        dut.prepare()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is True:
                    cls.lfp_panels.append(panel)
                else:
                    cls.ext_panels.append(panel)

    ##
    # @brief        This method is the exit point for all port sync test cases. This resets the environment changes done
    #               for the port sync tests
    # @return       None
    @classmethod
    def TearDownClass(cls):
        dut.reset()

    ##
    # @brief        Test function is to configure port sync in VBT for port sync
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        gfx_vbt = Vbt()
        set_vbt = False
        self.panel1_index = gfx_vbt.block_40.PanelType
        panel1_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (1 << self.panel1_index)) >> \
                               self.panel1_index
        if panel1_port_sync_bit != 1:
            gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
                gfx_vbt.block_42.DualLfpPortSyncEnablingBits | (1 << self.panel1_index)
            set_vbt = True
        else:
            logging.info("Port sync enabled in VBT for panel1")

        if len(self.lfp_panels) == 2:
            self.panel2_index = gfx_vbt.block_40.PanelType2
            panel2_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (
                    1 << self.panel2_index)) >> self.panel2_index
            if panel2_port_sync_bit != 1:
                gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
                    gfx_vbt.block_42.DualLfpPortSyncEnablingBits | (1 << self.panel2_index)
                set_vbt = True
            else:
                logging.info("Port sync enabled in VBT for panel2")

        if set_vbt is True:
            if gfx_vbt.apply_changes() is False:
                self.fail('Setting VBT block 52 failed')
            else:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("Failed to restart driver")
                gfx_vbt.reload()
                logging.info("Port sync enabled in VBT for panel1")
                logging.info("Port sync enabled in VBT for panel2")

        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail("Failed to restart driver")

    ##
    # @brief        Update pipe details in panel object
    # @param[in]    config: panels as config list
    # @return       None
    def update_dynamic_pipe(self, config):
        panels = dut.adapters['gfx_0'].panels.values()
        for panel in panels:
            if panel.port in config:
                display_base_obj = DisplayBase(panel.port)
                trans, pipe = display_base_obj.get_transcoder_and_pipe(panel.port)
                panel.transcoder = 'EDP' if trans == 0 else chr(int(trans) + 64)
                panel.pipe = chr(int(pipe) + 65)
                logging.info("updated pipe {0} for panel {1}".format(panel.pipe, panel.port))