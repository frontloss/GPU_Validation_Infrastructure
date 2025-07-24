########################################################################################################################
# @file         cabc_base.py
# @brief        Base class for CABC verification test cases
# @author       Tulika
########################################################################################################################

import logging
import sys
import unittest

from Libs.Core.wrapper import control_api_wrapper

from Libs.Core import cmd_parser, display_essential, display_power, registry_access
from Libs.Core.display_config import display_config
from Libs.Core.logger import html, gdhm
from Libs.Core.vbt import vbt
from Libs.Core.vbt.vbt import Vbt
from Tests.CABC import cabc
from Tests.PowerCons.Modules import common, dut, workload
from Tests.PowerCons.Functional.DPST.dpst import delete_persistence

##
# @brief       This class contains setup, teardown and test functions for CABC test cases
class CabcBase(unittest.TestCase):
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
        logging.info(" SETUP CABC_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        dut.prepare(power_source=workload.PowerSource.DC_MODE)

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                cabc.optimization_params[panel.port] = cabc.CabcParams()
                cls.feature_to_enable[panel.port] = []
                lfp = None
                if panel.port == 'DP_A' and panel.is_lfp and cls.cmd_line_param[0]['LFP1'] != 'NONE':
                    lfp = cls.cmd_line_param[0]['LFP1']

                if panel.port == 'DP_B' and panel.is_lfp and cls.cmd_line_param[0]['LFP2'] != 'NONE':
                    lfp = cls.cmd_line_param[0]['LFP2']

                cls.co_exist = None
                if cls.cmd_line_param[0]['CO_EXIST'] != 'NONE':
                    cls.co_exist = cls.cmd_line_param[0]['CO_EXIST'][0]

                cls.os_option = None
                if cls.cmd_line_param[0]['OS_OPTION'] != 'NONE':
                    cls.os_option = cls.cmd_line_param[0]['OS_OPTION'][0]

                if lfp is not None:
                    cabc.optimization_params[panel.port].feature_1.name = lfp[0].upper().split("_L")[0]
                    cabc.optimization_params[panel.port].feature_1.level = int(lfp[0].upper().split("_L")[1])
                    cls.feature_to_enable[panel.port].append(cabc.optimization_params[panel.port].feature_1.name)

                    if len(cls.cmd_line_param[0]['LFP1']) > 1:
                        cabc.optimization_params[panel.port].feature_2.name = lfp[1].upper().split("_L")[0]
                        cabc.optimization_params[panel.port].feature_2.level = int(lfp[1].upper().split("_L")[1])
                        cls.feature_to_enable[panel.port].append(cabc.optimization_params[panel.port].feature_2.name)

    ##
    # @brief        This function resets the changes done for execution of the CABC tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: CABC_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        if cls.cmd_line_param[0]['OS_OPTION'] != 'NONE':
            reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                     reg_path=r"System\CurrentControlSet")
            registry_access.delete(args=reg_args, reg_name="CABCOption", sub_key=r"Control\GraphicsDrivers")
        for adapter in dut.adapters.values():
            status = delete_persistence(adapter)
            if status is False:
                assert False, "FAILED to delete persistence registry keys"
        dut.reset()
        vbt = Vbt()
        if vbt.reset() is False:
            assert False, "Failed to restore VBT from driver"
        logging.info("Successfully restored VBT from driver")
        status, reboot_required = display_essential.restart_gfx_driver()
        assert status, "Failed to restart driver"
        logging.info("Successfully restarted driver")
        logging.info("Test Cleanup Completed")

    ################
    # Test Function
    ################

    ##
    # @brief       This tests check CABC support in VBT, Panel and IGCL
    # @return      None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start("Verifying adapter and panel requirements for CABC test")
        for adapter in dut.adapters.values():
            do_driver_restart = False
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"{panel}")
                logging.info(f"\t{panel.hdr_caps}")

                feature_list = [
                    cabc.optimization_params[panel.port].feature_1.name,
                    cabc.optimization_params[panel.port].feature_2.name
                ]

                # Enable Co-Existence
                if self.co_exist == 'TRUE':
                    status, do_driver_restart = cabc.enable_coexistence_with_xpst(adapter, panel)
                    if status is False:
                        self.fail(f"FAILED to enable co-existence in VBT")
                    if do_driver_restart is True:
                        status, reboot_required = display_essential.restart_gfx_driver()

                status, do_driver_restart = cabc.enable_feature_in_vbt(adapter, panel, feature_list)
                if status is False:
                    self.fail(f"FAILED to enable {feature_list} in VBT")

                # Enable OS setting (AlwaysOn, On_Battery, OFF)
                if self.os_option is not None:
                    cabc.toggle_os_cabc_option(cabc.OsCabcOption[self.os_option])
                    do_driver_restart = True

            if do_driver_restart is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    logging.error("Failed to restart display driver after VBT update")
                    return False
            vbt.Vbt(adapter.gfx_index).reload()

            # @todo to remove later once re-init is handled in infra
            # Need to re-init as due to driver restart happened
            if not control_api_wrapper.configure_control_api(flag=False):
                self.fail("\tFailed to close Control API")

            if not control_api_wrapper.configure_control_api(flag=True):
                self.fail("\tFailed to re-init Control API")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue

                # Check feature support in panel
                if cabc.is_panel_supported(panel) is False:
                    self.fail("Feature is NOT supported by the panel")

                # Check feature support in IGCL
                f1 = cabc.optimization_params[panel.port].feature_1.name
                f2 = cabc.optimization_params[panel.port].feature_2.name

                if cabc.is_feature_supported_in_igcl(panel, f1) is False:
                    self.fail(f"{f1} is NOT supported in IGCL")

                if cabc.is_feature_supported_in_igcl(panel, f2) is False:
                    self.fail(f"{f2} is NOT supported in IGCL")


                status, level = cabc.set_optimization_level(self.feature_to_enable[panel.port], existing_level=True)
                if status is False:
                    gdhm.report_driver_bug_pc(f" Failed to set {level} optimization level via IGCL")
                    self.fail(f"FAILED to set Power settings with level")
