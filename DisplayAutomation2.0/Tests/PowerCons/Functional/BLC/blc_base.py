########################################################################################################################
# @file         blc_base.py
# @brief        Contains base class for all BLC tests
# @details      @ref blc_base.py <br>
#               This file implements unittest default functions for setUp and tearDown, common test functions used
#               across all BLC tests, and helper functions.
#
# @author       Ashish Tripathi
########################################################################################################################

import logging
import sys
import unittest

import win32api

from Libs.Core import cmd_parser, enum, winkb_helper, display_essential, reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core import display_power
from Libs.Core.logger import html
from Libs.Core.system_utility import SystemUtility
from Tests.PowerCons.Functional.BLC import blc
from Tests.PowerCons.Modules import common, desktop_controls, dut, windows_brightness

# Note: do ULT of all scenarios when there is change in number of elements or brightness change in below list

if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
    # Before Cobalt brightness is restoring to 100 after power event
    BRIGHTNESS_LIST = [1, 61, 47, 100, 0, 30, 89]
else:
    BRIGHTNESS_LIST = [1, 61, 47, 0, 100, 30, 89]

# length of below list is in ms and should be same as above BRIGHTNESS_LIST. Used for IBLC
TRANSITION_TIME_LIST = [100, 500, 1000, 0, 200, 700, 900]

##
# @brief        Exposed Class to write Blc tests. Any new Blc test class can inherit this class to use common setUp
#               and tearDown functions.
class BlcBase(unittest.TestCase):
    cmd_line_param = None
    system_utility_ = SystemUtility()
    display_config_ = DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    lfp_type = cmd_test_name = None
    is_inf_nit_range = is_high_precision = nit_ranges = disable_boost_nit_ranges = disable_nits_brightness = None
    is_pwm_based = {'DP_A': False, 'DP_B': False}
    hdr_state = {}
    is_hdr_panel = {}
    lfp1_port = None
    initial_brightness = 100
    is_invalid_inf_nit_range = None
    test_scenario: blc.Scenario = None
    test_adapter: dut.adapters = None
    independent_brightness = False

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
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS + ['-BRIGHTNESS']
                                                      + ['-TRANSITION_TIME'])

        # To handle multi-adapter scenario
        if not isinstance(self.cmd_line_param, list):
            self.cmd_line_param = [self.cmd_line_param]

        self.cmd_test_name = self.cmd_line_param[0]['FILENAME'].split("\\")[-1].split(".")[0]

        self.is_high_precision = self.cmd_line_param[0]['HIGH_PRECISION'] != 'NONE'
        self.is_inf_nit_range = self.cmd_line_param[0]['NIT_RANGES'] != 'NONE'
        self.is_invalid_inf_nit_range = self.cmd_line_param[0]['INVALID_NIT_RANGES'] != 'NONE'
        self.disable_boost_nit_ranges = self.cmd_line_param[0]['NIT_RANGES_FFFF'] != 'NONE'
        self.disable_nits_brightness = self.cmd_line_param[0]['DISABLE_NITS_BRIGHTNESS'] != 'NONE'
        if self.cmd_line_param[0]['INDEPENDENT_BRIGHTNESS'] != 'NONE':
            self.independent_brightness = True
        if self.is_inf_nit_range or self.is_invalid_inf_nit_range:
            if self.is_inf_nit_range:
                self.nit_ranges = self.cmd_line_param[0]['NIT_RANGES'][0].split("_")
            elif self.is_invalid_inf_nit_range:
                self.nit_ranges = self.cmd_line_param[0]['INVALID_NIT_RANGES'][0].split("_")
            if self.nit_ranges is None:
                self.fail("NO Nits ranges are provided (command-line issue)")
            self.nit_ranges = blc.create_nit_ranges(self.nit_ranges)
        dut.prepare()

        # Clear OS display off timeout values
        html.step_start("Enabling Simulated Battery and setting display time-out to 0")
        for power_line_state in [display_power.PowerSource.DC, display_power.PowerSource.AC]:
            logging.info(f"\tClearing display time-out for state")
            if desktop_controls.set_time_out(desktop_controls.TimeOut.TIME_OUT_DISPLAY, 0, power_line_state) is False:
                logging.warning(f"FAILED to clear display time-out for {power_line_state.name}")

        # Enable Simulated Battery for AC/DC switch
        if self.display_power_.enable_disable_simulated_battery(True) is False:
            self.fail("FAILED to enable Simulated Battery")
        logging.info("\tSuccessfully enabled simulated battery")
        html.step_end()

        # WA for 14010407547 - make brightness work after disable/enable gfx-driver (fix will be in build 19575)
        if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
            blc.restart_display_service()

    ##
    # @brief        This method is the exit point for Blc test cases. This resets the  changes done
    #               for execution of Blc tests
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        html.step_start("TEARDOWN PHASE")
        do_driver_restart = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if self.is_inf_nit_range and panel.port == self.lfp1_port:
                    do_driver_restart = True
                    blc.delete_lfp_nit_ranges(adapter, panel)
                elif self.is_high_precision:
                    do_driver_restart = True
                    blc.disable_high_precision(adapter)
                if panel.hdr_caps.is_hdr_supported:
                    os_aware = self.cmd_test_name.upper() != "BLC_AC_DC"
                    # HDR won't be enabled by default for DC mode so using INF approach for AC_DC test
                    status = blc.disable_hdr(adapter, panel, os_aware)
                    if status is False:
                        self.fail("FAILED to disable HDR")
                    do_driver_restart = True if status is True else do_driver_restart
                if self.disable_boost_nit_ranges:
                    status = blc.delete_boost_nit_ranges(adapter)
                    if status is False:
                        self.fail("Deleting boost nit ranges failed")
                    do_driver_restart = True if status is True else do_driver_restart
                if self.disable_nits_brightness:
                    status = blc.delete_disable_brightness3_inf(adapter)
                    if status is False:
                        self.fail("Deleting disable brightness3 INF failed")
                    do_driver_restart = True if status is True else do_driver_restart

            if do_driver_restart is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail(f"\tFAILED to restart the display-driver for {adapter.gfx_index}")
                logging.info(f"\tSuccessfully restarted the display-driver for {adapter.gfx_index}")

        dut.reset()

        html.step_start("Disabling Simulated Battery and clearing Display time-out")
        # Disable Simulated Battery
        if self.display_power_.enable_disable_simulated_battery(False):
            logging.info("\tSuccessfully disabled simulated battery")
        else:
            logging.warning("FAILED to disable Simulated Battery")

        # Clear OS display off timeout values
        for power_line_state in [display_power.PowerSource.DC, display_power.PowerSource.AC]:
            logging.info(f"\tSuccessfully cleared display time-out for {power_line_state.name}")
            if desktop_controls.set_time_out(desktop_controls.TimeOut.TIME_OUT_DISPLAY, 0, power_line_state) is False:
                logging.warning("FAILED to clear display time-out for {0}".format(power_line_state.name))
        # Move mouse to make sure display is in ON state before exiting the test
        win32api.SetCursorPos((400, 400))
        winkb_helper.press('ESC')
        html.step_end()

        # WA for 14010407547 - make brightness work after disable/enable gfx-driver (fix will be in build 19575)
        if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
            blc.restart_display_service()

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
    # @brief        This method will do the setup phase and scenario for BLC
    # @param[in]    scenario Scenario (MTO/TDR/AC_DC/MODE_SET/DISPLAY_CONFIG/CS/S3/S4)
    # @return       None
    def setup_and_validate_blc(self, scenario:blc.Scenario = None):
        count = 1
        html.step_start("SETUP PHASE")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue

                if count == 1 and (self.cmd_line_param[0]['LFP1'] != 'NONE'):
                    self.lfp_type = self.cmd_line_param[0]['LFP1'][0]
                    if self.lfp1_port is None:
                        self.lfp1_port = panel.port

                if count == 2 and (self.cmd_line_param[0]['LFP2'] != 'NONE'):
                    self.lfp_type = self.cmd_line_param[0]['LFP2'][0]

                logging.info(f"{self.lfp_type} based brightness requested on {panel.port}(PIPE_{panel.pipe})")

                self.is_hdr_panel[panel.port] = panel.hdr_caps.is_hdr_supported
                if self.cmd_line_param[0]['HDR'] != 'NONE':
                    self.hdr_state[panel.port] = self.cmd_line_param[0]['HDR'][0] == 'TRUE'
                    if self.lfp_type == 'AUX':
                        if panel.port in ['MIPI_A', 'MIPI_C']:
                            self.fail(f"{panel.port} cannot have HDR support")
                        if self.is_hdr_panel[panel.port] is False:
                            self.fail(f"{panel.port} does not support HDR on PIPE_{panel.pipe}")

                if panel.port == self.lfp1_port:
                    logging.info("Creating fresh state by removing/disabling INFs for Brightness feature")
                    if blc.delete_lfp_nit_ranges(adapter, panel) is False:
                        self.fail("FAILED to delete LFP Nits Ranges")
                    if blc.disable_hdr(adapter, panel, os_aware=False) is False:
                        self.fail("FAILED to disable HDR")
                    if blc.disable_high_precision(adapter) is False:
                        self.fail("FAILED to disable high precision")

                    if self.is_inf_nit_range or self.is_invalid_inf_nit_range:
                        if blc.add_lfp_nit_ranges(adapter, panel, self.nit_ranges) is False:
                            self.fail("FAILED to add Nit ranges")

                if self.disable_boost_nit_ranges:
                    if blc.disable_boost_nit_ranges(adapter) is False:
                        self.fail("FAILED to disable Boost Nit Ranges(80:20 -> 100)")

                if self.disable_nits_brightness:
                    if blc.disable_brightness3(adapter) is False:
                        self.fail("FAILED to disable nits brightness")

                self.is_pwm_based[panel.port] = True
                if self.lfp_type == 'PWM':
                    if panel.port == self.lfp1_port:
                        if self.is_high_precision:
                            if blc.enable_high_precision(adapter) is False:
                                self.fail("FAILED to enable high precision")
                        elif self.is_hdr_panel[panel.port]:
                            if panel.hdr_caps.is_aux_only_brightness is True:
                                self.fail(f"PWM cannot be supported on {panel.port} as it is AUX only")
                            if blc.disable_hdr(adapter, panel, os_aware=False) is False:
                                self.fail("FAILED to disable HDR")

                elif self.lfp_type == 'AUX':
                    self.is_pwm_based[panel.port] = False
                    if self.is_hdr_panel[panel.port] and (panel.port in self.hdr_state and self.hdr_state[panel.port]):
                        os_aware = self.cmd_test_name.upper() != "BLC_AC_DC"
                        # HDR needs additional OS setting for DC mode so using INF approach for AC_DC test
                        if blc.enable_hdr(adapter, panel, os_aware) is False:
                            self.fail("FAILED to enable HDR")
                else:
                    self.fail(f"Panel type {self.lfp_type} is invalid (command-line issue)")
                count += 1

            status, is_reboot_needed = display_essential.restart_gfx_driver()
            if status is False:
                self.fail("\tFAILED to restart the display-driver")
            self.test_scenario = scenario
            logging.info(f"\tSuccessfully restarted the display-driver for {adapter.gfx_index}")
            if is_reboot_needed:
                data = list(dut.adapters.values())
                status = reboot_helper.reboot(self, 'validate_blc', data=data)
                if status is False:
                    self.fail("Failed to reboot the system")
            else:
                self.validate_blc(is_reboot_needed)

    ##
    # @brief        Exposed API to validate the BLC feature
    # @param[in]    reboot_happened - Default True, otherwise False based on restart display driver
    # @return       None
    def validate_blc(self, reboot_happened=True):

        workload_status = None
        if reboot_happened:
            data = reboot_helper._get_reboot_data()
            self.test_adapter = data
        else:
            self.test_adapter = dut.adapters.values()

        brightness_args = [
            self.is_pwm_based, self.nit_ranges, self.is_high_precision,
            self.hdr_state, BRIGHTNESS_LIST, self.lfp1_port, self.disable_boost_nit_ranges,
            self.is_invalid_inf_nit_range, self.disable_nits_brightness, self.independent_brightness
        ]

        if self.test_scenario != None:
            for adapter in self.test_adapter:
                workload_status = blc.run_workload(adapter, self.test_scenario, brightness_args)

            if workload_status[1] is False:
                self.fail("FAILED to run the workload")

            if workload_status[0] is None:
                self.fail("ETL file not found")

            html.step_start("VERIFICATION PHASE")

            for adapter in self.test_adapter:
                if self.is_invalid_inf_nit_range:
                    blc_status = blc.is_lfp_nit_range_valid(adapter, self.cmd_test_name, workload_status[0])
                    if blc_status is False:
                        self.fail("FAIL: LfpNitranges are valid and brightness will change on panel")
                    if blc_status is None:
                        self.fail("FAIL: Failed to Generate ETL/JSON File")
                    logging.info("PASS: LfpNitranges are invalid and brightness will NOT change on panel")
                else:
                    blc_status = blc.verify(adapter, self.cmd_test_name, workload_status[0], brightness_args)
                    if blc_status is None:
                        self.fail("FAILED to get DiAna result (Test Issue)")

                    if blc_status is False:
                        self.fail("FAIL: Brightness persistence is NOT maintained")
                    logging.info("PASS: Brightness persistence is maintained")
            html.step_end()
