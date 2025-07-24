########################################################################################################################
# @file         test_base.py
# @brief        Base class for Brightness Optimization verification test cases
# @author       Tulika
########################################################################################################################

import logging
import sys
import unittest

from Libs.Core.logger import html, gdhm
from Libs.Core import cmd_parser, display_essential, display_power
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.display_config import display_config

from Libs.Core.vbt import vbt
from Tests.BrightnessOptimization import brightness_optimization as brt
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Modules import common, dut, workload


##
# @brief       This class contains setup, teardown and test functions for Brightness Optimization test cases
class BrtOptimizationBase(unittest.TestCase):
    cmd_line_param = None
    feature_to_enable = {}
    display_power_ = display_power.DisplayPower()
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
        logging.info(" SETUP BRT_OPTIMIZATION_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        dut.prepare(power_source=workload.PowerSource.DC_MODE)

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                brt.optimization_params[panel.port] = brt.BrtOptParams()
                cls.feature_to_enable[panel.port] = []
                lfp = None
                if panel.port == 'DP_A' and panel.is_lfp and cls.cmd_line_param[0]['LFP1'] != 'NONE':
                    lfp = cls.cmd_line_param[0]['LFP1']

                if panel.port == 'DP_B' and panel.is_lfp and cls.cmd_line_param[0]['LFP2'] != 'NONE':
                    lfp = cls.cmd_line_param[0]['LFP2']

                if lfp is not None:
                    brt.optimization_params[panel.port].feature_1.name = lfp[0].upper().split("_L")[0]
                    brt.optimization_params[panel.port].feature_1.level = int(lfp[0].upper().split("_L")[1])
                    cls.feature_to_enable[panel.port].append(brt.optimization_params[panel.port].feature_1.name)

                    if len(cls.cmd_line_param[0]['LFP1']) > 1:
                        brt.optimization_params[panel.port].feature_2.name = lfp[1].upper().split("_L")[0]
                        brt.optimization_params[panel.port].feature_2.level = int(lfp[1].upper().split("_L")[1])
                        cls.feature_to_enable[panel.port].append(brt.optimization_params[panel.port].feature_2.name)
    ##
    # @brief        This function resets the changes done for execution of the Brightness Optimization tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: BRT_OPTIMIZATION_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        do_driver_restart = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                feature_list = [
                    brt.optimization_params[panel.port].feature_1.name,
                    brt.optimization_params[panel.port].feature_2.name
                ]
                status, do_driver_restart = brt.disable_feature_in_vbt(adapter, panel, feature_list)
                if status is False:
                    assert False, f"FAILED to disable {feature_list} in VBT"
            if do_driver_restart:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    logging.error("Failed to restart display driver after VBT update")
                    return False
            vbt.Vbt(adapter.gfx_index).reload()
        dut.reset()

    ################
    # Test Function
    ################

    ##
    # @brief       This tests check Brightness Optimization support in VBT, Panel and IGCL
    # @return      None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start("Verifying adapter and panel requirements for Brightness Optimization test")
        for adapter in dut.adapters.values():
            do_driver_restart = False
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"{panel}")
                logging.info(f"\t{panel.hdr_caps}")

                feature_list = [
                    brt.optimization_params[panel.port].feature_1.name,
                    brt.optimization_params[panel.port].feature_2.name
                    ]

                status, do_driver_restart = brt.enable_feature_in_vbt(adapter, panel, feature_list)
                if status is False:
                    self.fail(f"FAILED to enable {feature_list} in VBT")

            if do_driver_restart is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    logging.error("Failed to restart display driver after VBT update")
                    return False
            vbt.Vbt(adapter.gfx_index).reload()

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue

                # Check feature support in panel
                if brt.is_panel_supported(panel) is False:
                    self.fail("Feature is NOT supported by the panel")

                # Check feature support in IGCL
                f1 = brt.optimization_params[panel.port].feature_1.name
                f2 = brt.optimization_params[panel.port].feature_2.name

                if brt.is_feature_supported_in_igcl(panel, f1) is False:
                    self.fail(f"{f1} is NOT supported in IGCL")

                if brt.is_feature_supported_in_igcl(panel, f2) is False:
                    self.fail(f"{f2} is NOT supported in IGCL")

                status = True
                for f in self.feature_to_enable[panel.port]:
                    if f == brt.optimization_params[panel.port].feature_1.name:
                        level = brt.optimization_params[panel.port].feature_1.level
                        if brt.igcl_set_power_settings(panel, f, True, level) is False:
                            logging.error(f"FAILED to set Power settings with level {level}")
                            status = False
                        if brt.is_feature_supported_in_igcl(panel, f1) is False:
                            self.fail(f"{f1} is NOT Enabled in IGCL")
                    elif f == brt.optimization_params[panel.port].feature_2.name:
                        level = brt.optimization_params[panel.port].feature_2.level
                        if brt.igcl_set_power_settings(panel, f, True, level) is False:
                            logging.error(f"FAILED to set Power settings with level {level}")
                            status = False
                        if brt.is_feature_supported_in_igcl(panel, f1) is False:
                            self.fail(f"{f1} is NOT Enabled in IGCL")

                    if status is False:
                        gdhm.report_driver_bug_pc(f"[{f}] Failed to set {f} optimization level via IGCL")
                        self.fail(f"FAILED to set Power settings with level")
