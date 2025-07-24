########################################################################################################################
# @file         dc_state_base.py
# @brief        Contains base class for all DCSTATES tests
#
# @author       Vinod D S
########################################################################################################################

import logging
import sys
import time
import unittest

from Libs.Core import cmd_parser, enum, window_helper, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.display_power import DisplayPower, PowerSource
from Libs.Core.logger import html
from Libs.Core.sw_sim import driver_interface
from Libs.Core.vbt.vbt import Vbt
from Tests.PowerCons.Modules import common, desktop_controls, dut
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Functional.DCSTATES import dc_state
from registers.mmioregister import MMIORegister


##
# @brief        Exposed Class to write DC States tests. Any new DC States test can inherit this class common setUp
#               and tearDown functions. DCStatesBase also includes some functions used across all DC States tests.
class DCStatesBase(unittest.TestCase):
    feature = None
    cmd_line_param = None  # Used to store command line parameters
    driver_interface_ = driver_interface.DriverInterface()
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = DisplayPower()
    lfp_panels = []
    ext_panels = []
    dc_state = None

    ##
    # @brief        This class method is the entry point for any DC States test case. Helps to initialize some of the
    #               parameters required for DC States test execution.
    # @details      This function checks for feature support and initializes parameters to handle
    #               multi-adapter scenarios in test cases
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info(" SETUP: DC_STATE_BASE ".center(common.MAX_LINE_WIDTH, "*"))
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

        if common.IS_PRE_SI:
            cls.pre_si_setup()

        logging.info("Enabling Simulated Battery")
        assert cls.display_power_.enable_disable_simulated_battery(True), "Failed to enable Simulated Battery"
        logging.info("\tPASS: Expected Simulated Battery Status= ENABLED, Actual= ENABLED")

    ##
    # @brief        This method is the exit point for all DC States test cases. This resets the environment changes done
    #               for the DC States tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: DC_STATE_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        dut.reset()
        cls.display_power_.enable_disable_simulated_battery(False)

    ##
    # @brief        Test function puts DC states requirements
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start("Verify system and panel requirements for DC states")
        for adapter in dut.adapters.values():
            logging.info("Active panel capabilities for {0}".format(adapter.name))
            for panel in adapter.panels.values():
                logging.info("\t{0}".format(panel))
                logging.info("\t\t{0}".format(panel.psr_caps))
                logging.info("\t\t{0}".format(panel.vrr_caps))
        html.step_end()

    ##
    # @brief        Test function enables DC6v if disabled
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_01_dc6v_enable(self):
        for adapter in dut.adapters.values():
            if adapter.name in common.GEN_14_PLATFORMS:
                html.step_start(f"Enabling DC6v if not enabled on {adapter.name}")
                dc6v_status = dc_state.enable_dc6v(adapter)
                if dc6v_status is False:
                    self.fail("FAILED to enable DC6v in driver")
                if dc6v_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    assert status, "FAILED to restart the driver"
        html.step_end()

    ##
    # @brief        This is a helper function to setup the required configuration in pre-si for DC States tests
    # @return       None
    @classmethod
    def pre_si_setup(cls):
        # In case of Pre-Silicon, enable "change_mask_for_vblank_vsync_int" in PIPE_MISC_REGISTER
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                pipe_misc = MMIORegister.read(
                    "PIPE_MISC_REGISTER", "PIPE_MISC_" + panel.pipe, adapter.name, gfx_index=adapter.gfx_index)
                if pipe_misc.change_mask_for_vblank_vsync_int != 1:
                    pipe_misc.change_mask_for_vblank_vsync_int = 1
                    mmio_stat = cls.driver_interface_.mmio_write(pipe_misc.offset, pipe_misc.asUint,
                                                                 gfx_index=adapter.gfx_index)
                    assert mmio_stat, f"Failed to write MMIO Offset= {pipe_misc.offset}({panel.port})"
                    logging.info(f"\tPASS: Write MMIO Offset= {pipe_misc.offset}({panel.port}) successful")

        # Hiding the task-bar to make sure that there's no update on screen
        if window_helper.toggle_task_bar(window_helper.Visibility.HIDE):
            logging.info("TaskBar is hidden successfully")
        else:
            logging.error("Failed to hide TaskBar")

        # Clear OS display off timeout values
        if desktop_controls.set_time_out(desktop_controls.TimeOut(0), 0, PowerSource.AC) is False:
            logging.warning("Failed to reset display off timeout values in AC")
        if desktop_controls.set_time_out(desktop_controls.TimeOut(0), 0, PowerSource.DC) is False:
            logging.warning("Failed to reset display off timeout values in DC")

    ##
    # @brief        This is a helper function to enable port sync in vbt
    # @return       None
    def enable_port_sync_in_vbt(self):
        gfx_vbt = Vbt()
        is_vbt_modified = False
        self.panel1_index = gfx_vbt.block_40.PanelType
        panel1_port_sync = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (
                    1 << self.panel1_index)) >> self.panel1_index
        if panel1_port_sync != 1:
            gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
                gfx_vbt.block_42.DualLfpPortSyncEnablingBits | (1 << self.panel1_index)
            is_vbt_modified = True
        else:
            logging.info("Port sync enabled in VBT for panel1")

        if len(self.lfp_panels) == 2:
            self.panel2_index = gfx_vbt.block_40.PanelType2
            panel2_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (
                    1 << self.panel2_index)) >> self.panel2_index
            if panel2_port_sync_bit != 1:
                gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
                    gfx_vbt.block_42.DualLfpPortSyncEnablingBits | (1 << self.panel2_index)
                is_vbt_modified = True
            else:
                logging.info("Port sync enabled in VBT for panel2")

        # If required vbt modification is already exist, do not do anything
        if is_vbt_modified is False:
            return

        # Updated the vbt modification
        if gfx_vbt.apply_changes() is False:
            self.fail('Setting VBT block 52 failed')
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail("Failed to restart driver")
        gfx_vbt.reload()
        logging.info("Port sync enabled in VBT for panel1")
        if len(self.lfp_panels) == 2:
            logging.info("Port sync enabled in VBT for panel2")
