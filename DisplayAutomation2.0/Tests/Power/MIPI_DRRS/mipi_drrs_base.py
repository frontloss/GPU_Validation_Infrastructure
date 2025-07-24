########################################################################################################################
# @file         mipi_drrs_base.py
# @brief        This file contains base class for Mipi DRRS test, with setup, teardown and common functionality used by
#               Mipi DRRS tests. It contains setUp and tearDown methods of unittest framework.
# @details      In setUp, we parse command_line arguments and check MIPI panel's existence, plug displays
#               pre-Requisite Actions for DRRS tests like: Minimizing all the windows, hiding taskbar,
#               Enabling SIMBATT and Powerline=DC mode
#               In tearDown, the displays which were plugged during test will be unplugged, Taskbar show and
#               Disable SIMBATT, check whether TDR is detected or not
# @note         Do not modify this class without consent from the author.
# @authors      Kruti Vadhavaniya
########################################################################################################################

import logging
import os
import sys
import time
import unittest
from enum import IntEnum

from Libs.Core import app_controls, window_helper, enum, cmd_parser, display_utility
from Libs.Core import winkb_helper as kb
from Libs.Core.display_config import display_config
from Libs.Core.display_power import DisplayPower, PowerSource
from Libs.Core.machine_info import machine_info as mc_info
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env import test_context
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.clock.clock_helper import ClockHelper
from Libs.Feature.mipi.mipi_helper import MipiHelper
from Libs.Feature.mipi.mipi_helper import VbtMipiTimings
from registers.mmioregister import MMIORegister

TEST_VIDEOS_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos")
MIPI_DRRS_SUPPORTED_PLATFORMS = ["lkf1", "tgl", "adlp"]


##
# @brief      Enum for List of Power Events available
class DrrsType(IntEnum):
    SEAMLESS: 0
    MEDIA: 1
    NONE: 2


##
# @brief        This is the base class for Mipi DRRS tests with setup, teardown and common functions used in the
#               MIPI DRRS tests cases
class MipiDrrsBase(unittest.TestCase):
    ##
    # @brief        This method parses arguments, plug displays and check MIPI panel's existence,
    #               reads necessary VBT blocks
    # @details      This class method is the entry point for Mipi DRRS tests which are part of the class that inherits
    #               this class. This method initializes some of the parameters required for MIPI DRRS test execution.
    # @return       None
    def setUp(self):
        logging.info("Starting Test Setup")
        self.my_custom_tags = ['-media_fps']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)
        self.utility = SystemUtility()
        self.config = display_config.DisplayConfiguration()
        self.disp_power = DisplayPower()
        self.gfx_vbt = Vbt()
        self.machine_info = mc_info.SystemInfo()
        self.fail_count = 0
        self.panel_index = 0
        self.dual_LFP_MIPI = 0
        self.port_list = []
        self.dual_link = 0
        self.num_ports = 1
        self.platform = None
        self.teardown_flag = True
        self.displays_in_cmdline = []
        self.current_connected_displays_list = []
        self.media_fps = None
        self.supported_refresh_rates = []
        self.mipi_helper = None

        ##
        # check platform. Test is applicable only for LKF,TGL
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        gfx_index = 'gfx_0'
        self.platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName.lower()

        if self.platform not in MIPI_DRRS_SUPPORTED_PLATFORMS:
            self.fail("This test is applicable only for %s. Current platform is %s. Aborting test (Planning Issue)." % (
                MIPI_DRRS_SUPPORTED_PLATFORMS, self.platform))

        ##
        # Initialize MIPI verifier. This will contain helper functions
        self.mipi_helper = MipiHelper(self.platform)

        ##
        # process cmdline for display list and custom tags
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.displays_in_cmdline.append(value['connector_port'])
            if key == 'MEDIA_FPS':
                if value != "NONE":
                    self.media_fps = float(value[0])
        ##
        # Verify and plug the display.
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        ##
        # Checking for MIPI panel existence.
        self.port_list = []
        self.mipi_master_port = None
        if 'MIPI_A' in self.displays_in_cmdline:
            ret = display_config.is_display_attached(self.enumerated_displays, 'MIPI_A')
            if ret is True:
                self.port_list.append("_DSI0")
                self.mipi_master_port = 'MIPI_A'
            else:
                self.fail('MIPI_A is passed in cmdline but not attached')
        if 'MIPI_C' in self.displays_in_cmdline:
            ret = display_config.is_display_attached(self.enumerated_displays, 'MIPI_C')
            if ret is True:
                self.port_list.append("_DSI1")
                if self.mipi_master_port is None:
                    self.mipi_master_port = 'MIPI_C'
            else:
                self.fail('MIPI_C is passed in cmdline but not attached')
        if len(self.port_list) == 0:
            self.fail("None of the MIPI ports are connected. Aborting test (Execution Issue)")
        self.num_ports = len(self.port_list)

        self.mipi_helper.get_basic_mipi_caps()
        self.dual_LFP_MIPI = self.mipi_helper.dual_LFP_MIPI
        self.dual_link = self.mipi_helper.dual_link

        # List of all MIPI display
        if self.dual_LFP_MIPI:
            self.mipi_second_display = 'MIPI_C'
            self.current_connected_displays_list.extend([self.mipi_master_port, self.mipi_second_display])
        else:
            self.current_connected_displays_list.append(self.mipi_master_port)
        # panel indexes
        self.panel1_index = self.mipi_helper.get_panel_index_for_port("_DSI0")
        if self.dual_LFP_MIPI:
            self.panel2_index = self.mipi_helper.get_panel_index_for_port("_DSI1")

        if self.dual_LFP_MIPI:
            ##
            # apply DDE configuation
            result = self.config.set_display_configuration_ex(enum.CLONE,
                                                              [self.mipi_master_port, self.mipi_second_display],
                                                              self.enumerated_displays)
            self.assertNotEquals(result, False,
                                 "Applying DDE MIPIA + MIPIC display config failed.")
        else:
            ##
            # apply SD MIPI configuration.
            result = self.config.set_display_configuration_ex(enum.SINGLE, [self.mipi_master_port],
                                                              self.enumerated_displays)
            self.assertNotEquals(result, False, "Applying SD MIPI display config failed.")

        if self.dual_link == 1:
            # adding port_list explicitly, since OS will report only 1 target_id for MIPI; /
            # so is_display_attached for MIPIC will return false
            if (self.num_ports < 2) and (self.platform in MIPI_DRRS_SUPPORTED_PLATFORMS):
                self.port_list.append("_DSI1")
            self.num_ports = len(self.port_list)

        # Verify whether DRRS panel or not
        for port in self.port_list:
            self.panel_index = self.mipi_helper.get_panel_index_for_port(port)
            SeamlessDrrsMinRR = self.gfx_vbt.block_42.SeamlessDrrsMinRR[self.panel_index]

            if SeamlessDrrsMinRR == 0:
                self.fail("Current panel is not DRRS supported according to VBT. Aborting Test")

        for port in self.port_list:
            enumerated_displays = self.config.get_enumerated_display_info()
            port_name = "MIPI_A" if port == "_DSI0" else "MIPI_C"
            target_id = self.config.get_target_id(port_name, enumerated_displays)
            supported_mode_list = self.config.get_all_supported_modes([target_id], False)
            for key, values in supported_mode_list.items():
                for index in range(0, len(values)):
                    refreshRate = values[index].refreshRate
                    self.supported_refresh_rates.append(refreshRate)

            SeamlessDrrsMinRR = self.gfx_vbt.block_42.SeamlessDrrsMinRR[self.mipi_helper.get_panel_index_for_port(port)]
            self.supported_refresh_rates.append(SeamlessDrrsMinRR)

            supported_refresh_rate_list = list(set(self.supported_refresh_rates))
            logging.info("OS supported refresh rates with minRR are :{0}".format(supported_refresh_rate_list))

        # Enable Simbatt : Pre-Requisite for Enabling AC/DC
        simbatt_result = self.disp_power.enable_disable_simulated_battery(True)
        self.assertEquals(simbatt_result, True, "Aborting the test as enabling Simbatt failed.")

        # Setting the power line status to DC
        result_powerline_switch = self.disp_power.set_current_powerline_status(PowerSource.DC)
        self.assertEquals(result_powerline_switch, True, "Aborting the test due to power line switch to DC failed")

        logging.info("Test Setup Completed")

    ##
    # @brief        The displays which were plugged during test will be unplugged and checks for TDR will be done in
    #               this function.
    # @return       None
    def tearDown(self):
        logging.info("Starting Test Cleanup")

        ##
        # do Taskbar Show and Simbatt Disable
        if window_helper.toggle_task_bar(window_helper.Visibility.SHOW) is False:
            logging.warning('Aborting the test as Taskbar Show failed')

        if self.disp_power.enable_disable_simulated_battery(False) is False:
            logging.warning('Aborting the test as Simbatt Disable failed')

        if self.teardown_flag is True:
            ##
            # Unplug the displays and restore the configuration to the initial configuration
            for display in self.plugged_display:
                logging.info("Trying to unplug %s" % (display))
                if display_utility.unplug(display) is False:
                    logging.warning('Aborting the test as unplugging the display failed')

            ##
            # report test failure if fail_count>0
            if self.fail_count > 0:
                self.fail(
                    "Some checks in the test have failed. Check error logs. No. of failures= %d" % self.fail_count)

        logging.info("Test Cleanup Completed")

    # Some Generic Functions

    ##
    # @brief        This function is used to carry out the Pre-Requisite Actions to follow before DRRS tests like
    #               Minimization of  all windows, Hiding of the Taskbar
    # @return       None
    def do_idle_desktop(self):
        ideal_monitor = 0
        if (window_helper.minimize_all_windows() is True) and (
                window_helper.toggle_task_bar(window_helper.Visibility.HIDE) is True):
            logging.info("Monitor is ideal")
            ideal_monitor = 1
            time.sleep(5)
        else:
            logging.info("Monitor is not ideal.")
            ideal_monitor = 0
        return ideal_monitor

    ##
    # @brief        This function is used to verify DRRS status by comparing expected RR and Actual RR calculated
    #               from reg values
    # @param[in]    display_port string, port name
    # @param[in]    expected_rr [optional], number, expected refresh rate
    # @param[in]    media_fps [optional], string, port name
    # @return       None
    def check_drrs_status(self, display_port, expected_rr=60, media_fps=None):
        logging.info("********* Verifying DRRS for Port {} *********".format(display_port))
        drrs_check = True

        enumerated_displays = self.config.get_enumerated_display_info()
        target_id = self.config.get_target_id(display_port, enumerated_displays)

        port_name = "_DSI0" if (display_port == "MIPI_A") else "_DSI1"
        actual_refresh_rate = self.calculate_refresh_rate(display_port)

        if actual_refresh_rate == expected_rr:
            logging.info("PASS: Port: {0} Expected refresh rate : {1} and actual refresh rate: {2}".format(display_port,
                                                                                                           expected_rr,
                                                                                                           actual_refresh_rate))
        else:
            drrs_check = False
            logging.error(
                "FAIL: Port: {0} Expected refresh rate : {1} and actual refresh rate: {2}".format(display_port,
                                                                                                  expected_rr,
                                                                                                  actual_refresh_rate))
        return drrs_check

    ##
    # @brief        This function is used to calculate refresh rate from VBT
    # @param[in]    display_port string, port name
    # @return       None
    def calculate_refresh_rate_from_vbt(self, display_port):

        panel_index = self.mipi_helper.get_panel_index_for_port(display_port)
        vbt_mipi_timings = VbtMipiTimings()
        vbt_mipi_timings.get_vbt_mipi_timings(self.mipi_helper.gfx_vbt, panel_index)
        vbt_mipi_timings.adjust_timings_for_mipi_config(self.mipi_helper, panel_index)

        h_total = vbt_mipi_timings.htotal
        v_total = vbt_mipi_timings.vtotal

        # Getting pixel clock value
        pixel_rate = ClockHelper().get_pixel_rate(display_port)

        refresh_rate_hz = int(pixel_rate * (10 ** 6) / (h_total * v_total))

        logging.info(
            "H_TOTAL: {0}, V_TOTAL : {1}, Pixel rate: {2}, Refresh rate(Hz): {3}".format(h_total, v_total, pixel_rate,
                                                                                         refresh_rate_hz))
        return refresh_rate_hz

    ##
    # @brief        This function is used to calculate refresh rate from registers
    # @param[in]    display_port string, port name
    # @return       None
    def calculate_refresh_rate(self, display_port):

        port_name = "_DSI0" if display_port == "MIPI_A" else "_DSI1"

        reg_h_total = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL" + port_name, self.platform)
        reg_v_total = MMIORegister.read("TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL" + port_name, self.platform)

        h_total = reg_h_total.horizontal_total
        v_total = reg_v_total.vertical_total

        # Getting pixel clock value
        pixel_rate = ClockHelper().get_pixel_rate(display_port)

        refresh_rate_hz = int(pixel_rate * (10 ** 6) / (h_total * v_total))

        logging.info(
            "H_TOTAL: {0}, V_TOTAL : {1}, Pixel rate: {2}, Refresh rate(Hz): {3}".format(h_total, v_total, pixel_rate,
                                                                                         refresh_rate_hz))
        return refresh_rate_hz

    ##
    # @brief        This function is used to check DRRS with media playback
    # @details      This function will verify the basic scenario of entering the DRRS state during the playback and
    #               after the playback by launching the media file with and without full screen.
    # @param[in]    display_port string, port name
    # @param[in]    media_fps number, fps of the video
    # @returns      None
    def check_drrs_with_media_playback(self, display_port, media_fps):
        dmrrs_check = True
        logging.info("********* Verifying DMRRS for Port {} *********".format(display_port))
        # Verifying DRRS with media playback in Full screen
        logging.info("Launching the media playback with Full screen")
        self.launch_video(media_fps, True)

        logging.info("verifying the basic scenario of entering DRRS state : During media playback with Full screen")
        time.sleep(8)

        expected_refresh_rate = 60.0 if media_fps == 59.940 or media_fps == 29.970 else int(media_fps * 2)
        result_drrs_check = self.check_drrs_status(display_port, media_fps=media_fps, expected_rr=expected_refresh_rate)

        if result_drrs_check == 1:
            logging.info("PASS: DRRS check during media playback with full screen for port {0}".format(display_port))
        else:
            logging.error("FAIL: DRRS check during media playback with full screen for port {0}".format(display_port))
            dmrrs_check = False

        window_helper.close_media_player()

        logging.info("Closed the media playback")
        return dmrrs_check

    ##
    # @brief        This function is used to launch video. It will open the specified video file with or without full screen
    #               based on the input
    # @param[in]    media_fps number, fps of the video
    # @param[in]    fullscreen_opt Full screen control option, True = Full screen, False= Without full screen
    # @returns None
    def launch_video(self, media_fps, fullscreen_opt):

        kb.press('WIN+M')
        app_controls.launch_video(os.path.join(TEST_VIDEOS_PATH, "{0:.3f}.mp4".format(media_fps)), fullscreen_opt)
        logging.info("\tLaunching video playback of {0:.3f}.mp4 is successful".format(media_fps))
        time.sleep(2)
