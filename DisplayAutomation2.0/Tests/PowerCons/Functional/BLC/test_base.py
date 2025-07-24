########################################################################################################################
# @file         test_base.py
# @brief        Contains base class for BLC and CABC tests for Vesa and Custom DPCD supported Panel
# @author       Simran Setia
########################################################################################################################

import logging
import sys
import unittest
from enum import IntEnum

from Libs.Core.wrapper import control_api_wrapper
from Libs.Core import cmd_parser, display_essential, reboot_helper, registry_access
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core import display_power
from Libs.Core.logger import html, gdhm
from Libs.Core.system_utility import SystemUtility
from Tests.PowerCons.Functional.BLC import blc
from Tests.PowerCons.Modules import common, dut, windows_brightness, dpcd, workload
from Tests.CABC import cabc
from Tests.PowerCons.Functional.DPST.dpst import delete_persistence
from Libs.Core.vbt.vbt import Vbt
from Libs.Core.vbt import vbt


# Note: do ULT of all scenarios when there is change in number of elements or brightness change in below list
BRIGHTNESS_LIST = [1, 61, 47, 0, 100, 30, 89]


##
# @brief   VBT Power Source Selection
class VbtPwmSourceSelection(IntEnum):
    VESA = 6
    DEFAULT = 2


##
# @brief        Exposed Class to write Blc tests. Any new Blc test class can inherit this class to use common setUp
#               and tearDown functions.
class TestBase(unittest.TestCase):
    cmd_line_param = None
    system_utility_ = SystemUtility()
    display_config_ = DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    lfp_type = cmd_test_name = None
    is_inf_nit_range = nit_ranges = disable_boost_nit_ranges = None
    is_pwm_based = {'DP_A': False, 'DP_B': False}
    hdr_state = {}
    is_hdr_panel = {}
    lfp1_port = None
    initial_brightness = 100
    test_scenario: blc.Scenario = None
    test_adapter: dut.adapters = None
    feature_to_enable = {}
    co_exist = None
    os_option = None
    vbt_option = None


    ##
    # @brief        This class method is the entry point for Blc test cases. Helps to initialize some
    #               parameters required for Blc test execution. It is defined in unittest framework and being
    #               overridden here.
    # @details      This function checks for feature support and initialize parameters to handle
    #               multi-adapter scenarios, clears display time-out for AC/DC, Enables Simulated Battery for
    #               AC/DC switch
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info(" SETUP TEST_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS + ['-BRIGHTNESS']
                                                      + ['-TRANSITION_TIME'])

        # To handle multi-adapter scenario
        if not isinstance(self.cmd_line_param, list):
            self.cmd_line_param = [self.cmd_line_param]

        self.cmd_test_name = self.cmd_line_param[0]['FILENAME'].split("\\")[-1].split(".")[0]
        self.is_inf_nit_range = self.cmd_line_param[0]['NIT_RANGES'] != 'NONE'
        self.disable_boost_nit_ranges = self.cmd_line_param[0]['NIT_RANGES_FFFF'] != 'NONE'
        if self.is_inf_nit_range:
            if self.is_inf_nit_range:
                self.nit_ranges = self.cmd_line_param[0]['NIT_RANGES'][0].split("_")
            if self.nit_ranges is None:
                self.fail("NO Nits ranges are provided (command-line issue)")
            self.nit_ranges = blc.create_nit_ranges(self.nit_ranges)

        if self.cmd_line_param[0]['CO_EXIST'] != 'NONE':
            self.co_exist = self.cmd_line_param[0]['CO_EXIST'][0]

        if self.cmd_line_param[0]['OS_OPTION'] != 'NONE':
            self.os_option = self.cmd_line_param[0]['OS_OPTION'][0]

        dut.prepare(power_source=workload.PowerSource.DC_MODE)
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                cabc.optimization_params[panel.port] = cabc.CabcParams()
                self.feature_to_enable[panel.port] = []
                self.lfp = None

                if panel.port == 'DP_A' and panel.is_lfp and self.cmd_line_param[0]['LFP1'] != 'NONE':
                    self.lfp_type = self.cmd_line_param[0]['LFP1'][0]
                    self.vbt = self.cmd_line_param[0]['LFP1'][1]
                    self.vbt_option = getattr(VbtPwmSourceSelection, self.vbt, None)
                    self.hdr = self.cmd_line_param[0]['LFP1'][2]
                    self.lfp = self.cmd_line_param[0]['LFP1'][3:]
                    self.lfp1_port = panel.port

                if self.lfp:
                    cabc.optimization_params[panel.port].feature_1.name = self.lfp[0].upper().split("_L")[0]
                    cabc.optimization_params[panel.port].feature_1.level = int(self.lfp[0].upper().split("_L")[1])
                    self.feature_to_enable[panel.port].append(cabc.optimization_params[panel.port].feature_1.name)

                    if len(self.lfp) > 1:
                        cabc.optimization_params[panel.port].feature_2.name = self.lfp[1].upper().split("_L")[0]
                        cabc.optimization_params[panel.port].feature_2.level = int(self.lfp[1].upper().split("_L")[1])
                        self.feature_to_enable[panel.port].append(cabc.optimization_params[panel.port].feature_2.name)

                if panel.port == 'DP_B' and panel.is_lfp and self.cmd_line_param[0]['LFP2'] != 'NONE':
                    self.lfp_type = self.cmd_line_param[0]['LFP2'][0]
                    self.vbt = self.cmd_line_param[0]['LFP2'][1]
                    self.vbt_option = getattr(VbtPwmSourceSelection, self.vbt, None)
                    self.hdr = self.cmd_line_param[0]['LFP2'][2]

        self.verify_default_settings()
        self.setup_vbt_and_regkey()


    ##
    # @brief        This method is the exit point for Blc test cases. This resets the  changes done
    #               for execution of Blc tests
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        html.step_start("TEARDOWN PHASE")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if self.is_inf_nit_range and panel.port == self.lfp1_port:
                    blc.delete_lfp_nit_ranges(adapter, panel)
                if panel.hdr_caps.is_hdr_supported:
                    os_aware = self.cmd_test_name.upper() != "BLC_AC_DC"
                    # HDR won't be enabled by default for DC mode so using INF approach for AC_DC test
                    status = blc.disable_hdr(adapter, panel, os_aware)
                    if status is False:
                        self.fail("FAILED to disable HDR")
                if self.disable_boost_nit_ranges:
                    status = blc.delete_boost_nit_ranges(adapter)
                    if status is False:
                        self.fail("Deleting boost nit ranges failed")
                if self.os_option:
                    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                             reg_path=r"System\CurrentControlSet")
                    registry_access.delete(args=reg_args, reg_name="CABCOption", sub_key=r"Control\GraphicsDrivers")
                status = delete_persistence(adapter)
                if status is False:
                    self.fail('FAILED to delete persistence registry keys')
            dut.reset()
            vbt_reset = Vbt()
            if vbt_reset.reset() is False:
                assert False, "Failed to restore VBT from driver"
            logging.info("Successfully restored VBT from driver")
            html.step_start("Disabling Simulated Battery and clearing Display time-out")
            result, reboot_required = display_essential.restart_gfx_driver()
            if result is False:
                self.fail(f"\tFAILED to restart the display-driver for {adapter.gfx_index}")
            logging.info(f"\tSuccessfully restarted the display-driver for {adapter.gfx_index}")

        html.step_end()

        # apply 75% brightness at the end of the test as per default on GTAx OS
        # If we cache brightness at the start of the test, then also it is not guaranteed on the default value
        # As big number of tests are running on GTAx OS, considering GTAx OS default
        # No major impact to any tests except BLC/ DPST and no return status check is needed
        if windows_brightness.set_current_brightness(75, 1):
            logging.info("Successfully applied 75% brightness")
        else:
            logging.error("FAILED to apply 75% brightness")


    ############################
    # Helper Functions
    ############################

    ##
    # @brief        This method will verify default  VBT and IGCL settings
    # @return       None
    def verify_default_settings(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                gfx_vbt = Vbt(adapter.gfx_index)
                panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
                logging.info("DEFAULT VBT & IGCL Settings Verifications".center(common.MAX_LINE_WIDTH, "*"))

                # Verify default VBT PWM Source Selection
                if gfx_vbt.block_43.BrightnessControlMethodEntry[
                    panel_index].PwmSourceSelection != VbtPwmSourceSelection.DEFAULT:
                    self.fail('PWM Source Selection is not set to PWM from Display Engine')

                #Verify by default Coexistence should be false
                if bool((gfx_vbt.block_44.TconBasedBacklightOptimizationCoExistenceWithXPST[0] & (
                        1 << panel_index)) >> panel_index) is True:
                    self.fail('Coexistence is not False By default')

                #Verify Default CABC level is 6
                if (gfx_vbt.block_44.AgressivenessProfile4[panel_index] & 0xf0) >> 4 != 6:
                    self.fail('CABC level is not 6 by default')

                #Verify Default XPST level is 2
                if (gfx_vbt.block_44.AgressivenessProfile4[panel_index] & 0x0f) != 2:
                    self.fail('XPST level is not 2 by default')

                #Verify default CABC feature Support in IGCL
                if cabc.is_feature_supported_in_igcl(panel, cabc.Feature.CABC) is True:
                    self.fail('CABC support is TRUE by default in IGCL')

                # Verify default XPST feature Support in IGCL
                if cabc.is_feature_supported_in_igcl(panel, cabc.Feature.OPST) is True:
                    self.fail('XPST support is TRUE by default in IGCL')

                logging.info("PASS:Default Vbt & IGCL settings Verification Passed")

    ##
    # @brief        This method will do the VBT and Regkey Settings
    # @return       None
    # @endcond
    def setup_vbt_and_regkey(self):
        html.step_start("Setting VBT and RegKey for test")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                #Setting VBT
                if self.vbt != 'DEFAULT':
                    blc.set_blc_control_method_in_vbt(adapter, panel, self.vbt_option)
                logging.info(" BLC TEST_BASE ".center(common.MAX_LINE_WIDTH, "*"))
                if self.is_inf_nit_range is False:
                    edp_rev = dpcd.get_edp_revision(panel.target_id)
                    is_vesa_based = True if (
                            self.vbt_option == VbtPwmSourceSelection.VESA or edp_rev ==
                            dpcd.EdpDpcdRevision.EDP_DPCD_1_5) else False
                    self.nit_ranges = blc.get_nit_ranges(panel, is_vesa_based)

                if self.lfp1_port is None:
                    self.lfp1_port = panel.port

                if panel.port == self.lfp1_port:
                    logging.info("Creating fresh state by removing/disabling INFs for Brightness feature")
                    if blc.delete_lfp_nit_ranges(adapter, panel) is False:
                        self.fail("FAILED to delete LFP Nits Ranges")
                    if blc.disable_hdr(adapter, panel, os_aware=False) is False:
                        self.fail("FAILED to disable HDR")

                    if self.is_inf_nit_range:
                        if blc.add_lfp_nit_ranges(adapter, panel, self.nit_ranges) is False:
                            self.fail("FAILED to add Nit ranges")

                if self.disable_boost_nit_ranges:
                    if blc.disable_boost_nit_ranges(adapter) is False:
                        self.fail("FAILED to disable Boost Nit Ranges(80:20 -> 100)")

                if self.lfp_type == 'PWM':
                    self.is_pwm_based[panel.port] = True
                    if panel.port == self.lfp1_port:
                            if blc.disable_hdr(adapter, panel, os_aware=False) is False:
                                self.fail("FAILED to disable HDR")

                elif self.lfp_type == 'AUX':
                    self.is_pwm_based[panel.port] = False
                    if panel.port in self.hdr_state and self.hdr_state[panel.port]:
                        os_aware = self.cmd_test_name.upper() != "BLC_AC_DC"
                        # HDR needs additional OS setting for DC mode so using INF approach for AC_DC test
                        if blc.enable_hdr(adapter, panel, os_aware) is False:
                            self.fail("FAILED to enable HDR")
                else:
                    self.fail(f"Panel type {self.lfp_type} is invalid (command-line issue)")

                if self.lfp:
                    logging.info("CABC TEST_BASE ".center(common.MAX_LINE_WIDTH, "*"))
                    # Check feature support in panel
                    edp_rev = dpcd.get_edp_revision(panel.target_id)
                    if edp_rev == dpcd.EdpDpcdRevision.EDP_DPCD_1_5 or self.vbt == VbtPwmSourceSelection.VESA:
                        if cabc.is_vesa_dpcd_supported_by_panel(panel) is False:
                            self.fail("CABC is NOT supported by the panel")
                    else:
                        if cabc.is_panel_supported(panel) is False:
                            self.fail("CABC is NOT supported by the panel")

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
                            if status is False:
                                self.fail('Failed to restart display driver after VBT update')

                    status, do_driver_restart = cabc.enable_feature_in_vbt(adapter, panel, feature_list)
                    if status is False:
                        self.fail(f"FAILED to enable {feature_list} in VBT")

                    # Enable OS setting (AlwaysOn, On_Battery, OFF)
                    if self.os_option is not None:
                        cabc.toggle_os_cabc_option(cabc.OsCabcOption[self.os_option])

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

                # Check feature support in IGCL
                f1 = cabc.optimization_params[panel.port].feature_1.name
                f2 = cabc.optimization_params[panel.port].feature_2.name

                if cabc.is_feature_supported_in_igcl(panel, f1) is False:
                    self.fail(f"{f1} is NOT supported in IGCL")

                if cabc.is_feature_supported_in_igcl(panel, f2) is False:
                    self.fail(f"{f2} is NOT supported in IGCL")

                status, level = cabc.set_optimization_level(self.feature_to_enable[panel.port],
                                                            existing_level=True)
                if status is False:
                    gdhm.report_driver_bug_pc(f" Failed to set {level} optimization level via IGCL")
                    self.fail(f"FAILED to set Power settings with level")


    ##
    # @brief        Exposed API to verify the BLC & CABC feature
    # @param[in]    scenario
    # @return       None
    def verify_blc_and_cabc(self, scenario: blc.Scenario = None):
        brightness_args = [
            self.is_pwm_based, self.nit_ranges, False,
            self.hdr_state, BRIGHTNESS_LIST, self.lfp1_port, self.disable_boost_nit_ranges,
            False, False, False
        ]
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                # BLC verification
                workload_status = blc.run_workload(adapter, scenario, brightness_args)
                if workload_status[1] is False:
                    self.fail("FAILED to run the workload")
                if workload_status[0] is None:
                    self.fail("ETL file not found")
                logging.info("BLC_VERIFICATION".center(common.MAX_LINE_WIDTH, "*"))
                blc_status = blc.verify(adapter, self.cmd_test_name, workload_status[0], brightness_args)
                if blc_status is None:
                    self.fail("FAILED to get DiAna result (Test Issue)")
                if blc_status is False:
                    self.fail("FAIL: Brightness persistence is NOT maintained")
                logging.info("PASS: Brightness persistence is maintained")

                # Pre-ARL + eDP1.5 Custom AUX: no VBT settings -> Custom DPCD programming RCR:[VSRI-6768]
                # Pre-ARL + eDP1.5 VESA AUX: no VBT settings -> Misconfig (negative) RCR:[VSRI-6768] -> UTF
                # ARL+ + eDP1.4(Custom), Default VBT -> Custom DPCD programming   RCR:[VSDI-13598]
                # ARL+ + eDP1.4(VESA), Default VBT -> Misconfig   RCR:[VSDI-13598] -> UTF
                # ARL+ + eDP1.4(VESA), VESA VBT -> VESA DPCD programming   RCR:[VSDI-13598]
                # ARL+ + eDP1.5(VESA), Don't care VBT -> VESA DPCD programming   RCR:[VSDI-13598]
                # ARL+ + eDP1.5(Custom), Don't care VBT -> Misconfig   RCR:[VSDI-13598] -> UTF

                if self.lfp_type == 'AUX':
                    # Custom AUX programming verification
                    if (( self.vbt_option == VbtPwmSourceSelection.DEFAULT and panel.edp_caps.edp_revision ==
                          dpcd.EdpDpcdRevision.EDP_DPCD_1_4_B)
                         or adapter.name in common.PRE_GEN_14_PLATFORMS):
                        blc_status = blc.verify_custom_aux_programming(adapter, panel, self.cmd_test_name,
                                                                       workload_status[0])

                        if blc_status is None:
                            self.fail("FAILED to get DiAna result (Test Issue)")
                        if blc_status is False:
                            self.fail("FAIL: Custom Aux Programming Verification Failed")
                        logging.info("PASS:  Custom Aux Programming Verification Passed")

                    # VESA AUX programming Verification
                    else:
                        blc_status = blc.verify_vesa_aux_programming(adapter, panel, self.cmd_test_name,
                                                                     workload_status[0])
                        if blc_status is None:
                            self.fail("FAILED to get DiAna result (Test Issue)")
                        if blc_status is False:
                            self.fail("FAIL: Vesa Aux Programming Verification Failed")
                        logging.info("PASS:  Vesa Aux Programming Verification Passed")

                if self.lfp:
                    logging.info("CABC_VERIFICATION".center(common.MAX_LINE_WIDTH, "*"))
                    is_vesa_based = True if (self.vbt_option == VbtPwmSourceSelection.VESA or panel.edp_caps.edp_revision
                                == dpcd.EdpDpcdRevision.EDP_DPCD_1_5) else False
                    test_status = True
                    skip_igcl_for_cabc = False
                    if (cabc.optimization_params[panel.port].feature_2.level is not None and
                            cabc.optimization_params[panel.port].feature_1.level != cabc.optimization_params[
                                panel.port].feature_2.level):
                        skip_igcl_for_cabc = True
                    if self.os_option is not None:
                        for trial in range(2):
                            toggle_status, pwr_src = cabc.toggle_power_source()
                            if toggle_status is False:
                                self.fail(f"FAILED to toggle power source")
                            status, new_level = cabc.set_optimization_level(self.feature_to_enable[panel.port])
                            if status is False:
                                gdhm.report_driver_bug_pc(f" Failed to set {new_level} optimization level via IGCL")
                                self.fail(f"FAILED to set Optimization level")
                            # In AC mode we have XPST as level 1, IGCL get call will always have OPST level due to existing bug
                            level_in_ac_mode = 1
                            if cabc.optimization_params[
                                panel.port].feature_2.name is not None and pwr_src == display_power.PowerSource.AC:
                                new_level = level_in_ac_mode
                            test_status &= cabc.verify(adapter, panel,
                                                       cabc.optimization_params[panel.port].feature_1.name,
                                                       new_level, skip_igcl_for_cabc, self.os_option, pwr_src,
                                                       is_vesa_based)
                            test_status &= cabc.verify(adapter, panel,
                                                       cabc.optimization_params[panel.port].feature_2.name,
                                                       new_level, skip_igcl_for_cabc, self.os_option, pwr_src,
                                                       is_vesa_based)
                    else:

                        expected_level_feature_1 = cabc.optimization_params[panel.port].feature_1.level
                        expected_level_feature_2 = cabc.optimization_params[panel.port].feature_2.level
                        display_power_ = display_power.DisplayPower()
                        pwr_src = display_power_.get_current_powerline_status()
                        # In AC mode we have XPST as level 1, IGCL get call will always have OPST level due to existing bug
                        level_in_ac_mode = 1
                        if cabc.optimization_params[
                            panel.port].feature_2.name is not None and pwr_src == display_power.PowerSource.AC:
                            expected_level_feature_1 = expected_level_feature_2 = level_in_ac_mode

                        test_status &= cabc.verify(adapter, panel,
                                                   cabc.optimization_params[panel.port].feature_1.name,
                                                   expected_level_feature_1,
                                                   skip_igcl_for_cabc,
                                                   self.os_option, pwr_src, is_vesa_based)
                        test_status &= cabc.verify(adapter, panel,
                                                   cabc.optimization_params[panel.port].feature_2.name,
                                                   expected_level_feature_2,
                                                   skip_igcl_for_cabc,
                                                   self.os_option, pwr_src, is_vesa_based)

                    if test_status is False:
                        self.fail(f"FAIL: CABC feature verification failed")
                    logging.info(f"PASS:  CABC feature verification passed")
