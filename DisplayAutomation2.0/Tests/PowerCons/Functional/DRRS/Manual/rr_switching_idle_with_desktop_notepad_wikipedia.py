########################################################################################################################
# @file           rr_switching_idle_with_desktop_notepad_wikipedia.py
# @brief          To verify RR switching with Idle Desktop, notepad and wikipedia.
# Manual of       https://gta.intel.com/procedures/#/procedures/TI-3421163/ TI
# Manual TI name  RR Switching: IDLE with Desktop_Notepad_Wikipedia
# Manual of       https://gta.intel.com/procedures/#/procedures/TI-3557577/ TI
# Manual TI name  RR Switching: IDLE with Desktop_Notepad_Wikipedia_PSR2_Disable
# @author         Golwala, Ami
########################################################################################################################
import ctypes
import logging
import random
import subprocess
import sys
import time
import unittest

import win32gui

from Libs.Core import display_power, enum, winkb_helper, window_helper, cmd_parser, display_essential, display_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import dut, workload, common


##
# @brief        This class contains Setup, test and teardown methods of unittest framework.
class RrSwitchingIdleWithDesktopNotepadWikipedia(unittest.TestCase):
    enum_port_list = []
    updated_enum_port_list = []
    display_pwr = display_power.DisplayPower()
    display_config = DisplayConfiguration()
    is_psr2_disable = False
    my_custom_tags = ['-psr2_disable']
    cmd_line_param = None
    WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Wikipedia"
    display1 = None

    ##
    # @brief        This class method is the entry point for test.
    # @return       None
    @classmethod
    def setUpClass(cls):
        pass

    ##
    # @brief        This step helps to initialize parameters required for testing display DRRS manual test.
    # @return       None
    def t_00_step(self):
        status = True
        self.__class__.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.__class__.my_custom_tags)

        if type(self.__class__.cmd_line_param) is not list:
            self.__class__.cmd_line_param = [self.__class__.cmd_line_param]

        for index in self.__class__.cmd_line_param:
            self.__class__.cmd_line_param_adapter = index
            for key, value in self.__class__.cmd_line_param_adapter.items():
                if key == 'PSR2_DISABLE':
                    if value != "NONE":
                        self.__class__.is_psr2_disable = True if value[0] == "TRUE" else False
        dut.prepare()
        if self.__class__.is_psr2_disable:
            alert.info("PSR2 will be disabled as requested by test")
            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    if panel.is_lfp is False:
                        continue
                    logging.info(f"Panel caps before disabling PSR2 : {panel}")
                    # Disable complete PSR2 using PSR2Disable
                    logging.info("Disabling PSR2 via reg key (PSR2Disable)")
                    psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                    if psr_status is False:
                        self.fail(f"FAILED to disable PSR2 for {panel.port}")
                    else:
                        ret_val, reboot_required = display_essential.restart_gfx_driver()
                        if ret_val is False:
                            self.fail(f"FAILED to restart display driver for {adapter.name}")
                        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                                   "[CONFIRM]:Enter yes if expectation met, else enter no"
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                            status = False
                        else:
                            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")
        if not status:
            self.fail("test_00_step failed")

    ##
    # @brief        This test verifies booted displays and enables DC state
    # @return       None
    def t_01_step(self):
        status = True
        user_msg = ("[Expectation]:Boot the system with planned eDP."
                    "\n[CONFIRM]:Enter yes if expectation met, else enter no")
        result = alert.confirm(user_msg)
        if not result:
            self.fail("Test is not started with planned panel. Rerun the test with planned panel.")
        else:
            logging.info("Step1: Test started with planned eDP")

        # Enabling Simulated Battery
        alert.info("Enabling simulated battery. No Visual artifacts/ corruption/ TDR/ BSOD should occur during this "
                   "process")
        logging.info("Enabling Simulated Battery")
        assert self.__class__.display_pwr.enable_disable_simulated_battery(True), "Failed to enable Simulated Battery"
        logging.info("Enabled Simulated Battery successfully")

        # Checking current power line status and if it is not DC, then changing it to DC
        power_line_status = self.__class__.display_pwr.get_current_powerline_status()
        if power_line_status != display_power.PowerSource.DC:
            alert.info("Changing power line to DC mode. Look at battery if it is changing or not")
            result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.DC)
            self.assertEquals(result, True, "Aborting the test as switching to DC mode failed")
        user_msg = "[Expectation]:Power line should switch to DC mode" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        time.sleep(1)
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Power line changed to DC")

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_01_step failed")

    ##
    # @brief        This step opens Notepad
    # @return       None
    def t_02_step(self):
        status = True
        alert.info("Application Notepad will be opened. No Visual artifacts/ corruption/ TDR/ BSOD should occur")
        winkb_helper.press('WIN+M')
        logging.info("Step2: Opening notepad in windowed mode")
        subprocess.Popen("notepad")
        time.sleep(2)

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_02_step failed")

    ##
    # @brief        This step moves cursor
    # @return       None

    def t_03_step(self):
        status = True
        alert.info("Cursor should blink on Notepad")
        logging.info("Step 3: Cursor movement")
        time.sleep(5)
        user_msg = "[Expectation]:cursor/caret blink will be started on the notepad" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("cursor/caret blink started on the notepad")

        for i in range(5):
            alert.info("Pressing Windows key.Cursor should not blink on Notepad")
            winkb_helper.press('LWIN')
            time.sleep(2)
            winkb_helper.press('LWIN')
            user_msg = "[Expectation]:cursor/caret blink will be stopped on the notepad" \
                       "\n[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("cursor/caret blink stopped on the notepad")

            alert.info("Cursor should blink on Notepad")
            time.sleep(2)

            user_msg = "[Expectation]:cursor/caret blink will be started on the notepad" \
                       "\n[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("cursor/caret blink started on the notepad")

        winkb_helper.press('WIN+D')

        # Checking current power line status and if it is not DC, then changing it to DC
        power_line_status = self.__class__.display_pwr.get_current_powerline_status()
        if power_line_status != display_power.PowerSource.DC:
            self.fail("System is not in DC mode")

        time.sleep(5)
        alert.info("Notepad will be set in foreground and random mouse movements will happen")
        self.hwnd = window_helper.get_window_handle('NOTEPAD')
        if self.hwnd is None:
            logging.error("Notepad is not open")
            status = False

        winkb_helper.press('WIN+D')
        time.sleep(30)

        start_time = time.time()
        while time.time() - start_time < 5:
            # Generate a random position within the screen resolution.
            x = random.randint(0, 1024)
            y = random.randint(0, 768)
            ctypes.windll.user32.SetCursorPos(x, y)
            # Sleep for a random amount of time.
            time.sleep(random.uniform(0, 1))

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should be seen" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_03_step failed")

    ##
    # @brief        This step goes to Desktop and verifies if any corruptions
    # @return       None

    def t_04_step(self):
        status = True
        alert.info("Going to Desktop after 30 sec and verify if any corruptions")
        logging.info("Step 4: Go to Desktop")
        time.sleep(30)
        window_helper.press('WIN+M')
        winkb_helper.press('WIN+D')
        time.sleep(5)

        window_helper.kill_process_by_name('Notepad.exe')

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_04_step failed")

    ##
    # @brief        This step does AC/DC switching
    # @return       None
    def t_05_step(self):
        status = True
        alert.info("Performing AC/DC switch for 10 times and verifies if any corruption")
        logging.info("Step 5: AC/DC switch")

        for i in range(10):
            alert.info("Changing power line to AC mode. Look at battery if it is changing or not")
            result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.AC)
            self.assertEquals(result, True, "Aborting the test as switching to AC mode failed")
            time.sleep(5)
            user_msg = "[Expectation]:Power line should switch to AC mode" \
                       "\n[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("Power line changed to AC")

            alert.info("Changing power line to DC mode. Look at battery if it is changing or not")
            result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.DC)
            self.assertEquals(result, True, "Aborting the test as switching to DC mode failed")
            time.sleep(1)
            user_msg = "[Expectation]:Power line should switch to DC mode" \
                       "\n[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("Power line changed to DC")

        # Checking current power line status and if it is not DC, then changing it to DC
        power_line_status = self.__class__.display_pwr.get_current_powerline_status()
        if power_line_status != display_power.PowerSource.DC:
            self.fail("System is not in DC mode")

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_05_step failed")

    ##
    # @brief        This step opens Notepad
    # @return       None
    def t_06_step(self):
        status = True
        alert.info("Opens Notepad and set it in the foreground")
        subprocess.Popen("notepad")
        time.sleep(2)

        self.hwnd = window_helper.get_window_handle('NOTEPAD')
        if self.hwnd is None:
            self.fail("Application Notepad is not open")

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_06_step failed")

    ##
    # @brief        This step does AC/DC switch
    # @return       None
    def t_07_step(self):
        status = True
        alert.info("Performing AC/DC switch for 10 times and verifies if any corruption")
        logging.info("Step 7: AC/DC switch")

        for i in range(10):
            alert.info("Changing power line to AC mode. Look at battery if it is changing or not")
            result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.AC)
            time.sleep(5)
            if not result:
                window_helper.kill_process_by_name('Notepad.exe')
                self.fail("Aborting the test as switching to AC mode failed")
            user_msg = "[Expectation]:Power line should switch to AC mode" \
                       "\n[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("Power line changed to AC")

            alert.info("Changing power line to DC mode. Look at battery if it is changing or not")
            result = self.__class__.display_pwr.set_current_powerline_status(display_power.PowerSource.DC)
            if not result:
                window_helper.kill_process_by_name('Notepad.exe')
                self.fail("Aborting the test as switching to DC mode failed")
            time.sleep(1)
            user_msg = "[Expectation]:Power line should switch to DC mode" \
                       "\n[CONFIRM]:Enter yes if expectation met, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("Power line changed to DC")

        # Checking current power line status is in DC or not
        power_line_status = self.__class__.display_pwr.get_current_powerline_status()
        if power_line_status != display_power.PowerSource.DC:
            window_helper.kill_process_by_name('Notepad.exe')
            self.fail("System is not in DC mode")

        time.sleep(20)
        window_helper.kill_process_by_name('Notepad.exe')

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_07_step failed")

    ##
    # @brief        This step Opens Wikipedia from Browser
    # @return       None
    def t_08_step(self):
        status = True
        alert.info("Opening wikipedia and setting browser in foreground and verifies if any corruption")
        logging.info("Step 8: Open Wikipedia from Browser")
        workload.WinAppActivities.launch(True, workload.AppType.BROWSER, self.__class__.WIKIPEDIA_URL)
        time.sleep(1)

        self.hwnd = window_helper.get_window_handle('EDGE')
        if self.hwnd is None:
            self.fail("Application wikipedia is not open")
        window_helper.set_app_in_foreground(self.hwnd)

        alert.info("Click ok once wikipedia is loaded")
        time.sleep(10)
        winkb_helper.press('CTRL+R')

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_08_step failed")

    ##
    # @brief        This step does page Up/Down
    # @return       None

    def t_09_step(self):
        status = True
        alert.info("Performs page up/down in browser and verifies if any corruption")
        self.hwnd = window_helper.get_window_handle('EDGE')
        if self.hwnd is None:
            self.fail("Application wikipedia is not open")
        window_helper.set_app_in_foreground(self.hwnd)

        logging.info("Step 9: Page Up/Down")
        winkb_helper.press('PAGEDOWN')
        time.sleep(0.5)
        winkb_helper.press('PAGEDOWN')
        time.sleep(10)

        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        if None in (left, top, right, bottom):
            return False
        window_helper.mouse_wheel_scroll(top // 2, bottom // 2, 30)
        time.sleep(10)

        start_time = time.time()
        while time.time() - start_time < 2:
            winkb_helper.press('PAGEUP')
            time.sleep(0.5)
        time.sleep(2)

        while time.time() - start_time < 2:
            winkb_helper.press('PAGEUP')
            time.sleep(0.5)
        time.sleep(30)

        window_helper.kill_process_by_name('msedge.exe')

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_09_step failed")

    ##
    # @brief        This step applies Low RR
    # @return       None
    def t_10_step(self):
        status = True
        alert.info("Applies low RR and verifies if any corruption")
        logging.info("Step 10: Apply Low RR")
        # Checking current power line status is in DC or not
        power_line_status = self.__class__.display_pwr.get_current_powerline_status()
        if power_line_status != display_power.PowerSource.DC:
            self.fail("System is not in DC mode")
        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                logging.info(f"Panel caps in step10 : {panel}")
                mode_list = common.get_display_mode(panel.target_id, panel.min_rr, limit=2)
                if mode_list is None:
                    self.fail("Failed to get Display mode")
                logging.info(
                    f"Applying display mode {mode_list[0].HzRes}x{mode_list[0].VtRes}@{mode_list[0].refreshRate}Hz")
                if self.__class__.display_config.set_display_mode([mode_list[0]]) is False:
                    self.fail("Failed to set display mode with Minimum RR")

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_10_step failed")

    ##
    # @brief        This step launches Notepad
    # @return       None
    def t_11_step(self):
        status = True
        alert.info("Launches notepad and presses WIN key and verifies if any corruption")
        logging.info("Step 11: launch Notepad")
        subprocess.Popen("notepad")
        time.sleep(1)
        self.hwnd = window_helper.get_window_handle('NOTEPAD')
        if self.hwnd is None:
            self.fail("Application Notepad is not open")

        time.sleep(5)
        for i in range(5):
            winkb_helper.press('LWIN')
            time.sleep(2)

        winkb_helper.press('LWIN')
        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_11_step failed")

    ##
    # @brief        This step applies high RR
    # @return       None
    def t_12_step(self):
        status = True
        alert.info("Applies high RR and verifies if any corruption")
        if not window_helper.is_process_running("Notepad.exe"):
            self.fail("Notepad app is not running")
        logging.info("Step 12: Apply high RR")
        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                logging.info(f"Panel caps in step12 : {panel}")
                mode_list = common.get_display_mode(panel.target_id, panel.max_rr, limit=2)
                if mode_list is None:
                    self.fail("Failed to get Display mode")
                logging.info(
                    f"Applying display mode {mode_list[0].HzRes}x{mode_list[0].VtRes}@{mode_list[0].refreshRate}Hz")
                if self.__class__.display_config.set_display_mode([mode_list[0]]) is False:
                    window_helper.kill_process_by_name('Notepad.exe')
                    self.fail("Failed to set display mode with Maximum RR")
        time.sleep(30)

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_12_step failed")

    ##
    # @brief        This step opens paint
    # @return       None
    def t_13_step(self):
        status = True
        alert.info(
            "User is expected to open paint, perform operation requested in paint and verifies if any corruption")
        logging.info("Step 13: Open Paint")
        # Checking current power line status is in DC or not
        power_line_status = self.__class__.display_pwr.get_current_powerline_status()
        if power_line_status != display_power.PowerSource.DC:
            self.fail("System is not in DC mode")

        user_msg = "Open Paint and Draw a Rectangle with black color" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Drawing a Rectangle with black color on Paint completed")
        time.sleep(10)

        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        for index in range(0, enumerated_display.Count):
            self.__class__.enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        self.__class__.display1 = self.__class__.enum_port_list[0]

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_13_step failed")

    ##
    # @brief        This step plugs/unplugs panel
    # @return       None

    def t_14_step(self):
        status = True
        user_msg = "Hot plug ANY DP panel." \
                   "\n[CONFIRM]:Enter yes if Display is plugged, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Step14: Hot plugged Display2")

        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        for index in range(0, enumerated_display.Count):
            self.__class__.updated_enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        if len(self.__class__.updated_enum_port_list) <= len(self.__class__.enum_port_list):
            window_helper.kill_process_by_name('Notepad.exe')
            window_helper.kill_process_by_name('mspaint.exe')
            self.fail("After hot plug of display2, still number of enumerated displays are same as before")
        self.__class__.enum_port_list = self.__class__.updated_enum_port_list

        for disp in self.__class__.enum_port_list:
            if disp is not self.__class__.display1:
                ret_val = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE, [disp])
                if not ret_val:
                    window_helper.kill_process_by_name('Notepad.exe')
                    window_helper.kill_process_by_name('mspaint.exe')
                    self.fail(f"Applying SD on port {disp} failed.")

        if not window_helper.is_process_running("Notepad.exe"):
            logging.error("Notepad app is not running")
            status = False

        if not window_helper.is_process_running("mspaint.exe"):
            logging.error("MSFT paint app is not running")
            status = False

        time.sleep(10)
        ret_val = self.__class__.display_config.set_display_configuration_ex(enum.EXTENDED,
                                                                            self.__class__.enum_port_list)
        if not ret_val:
            window_helper.kill_process_by_name('Notepad.exe')
            window_helper.kill_process_by_name('mspaint.exe')
            self.fail("Applying Extended mode failed")
        time.sleep(10)

        if not window_helper.is_process_running("Notepad.exe"):
            logging.error("Notepad app is not running")
            status = False

        if not window_helper.is_process_running("mspaint.exe"):
            logging.error("MSFT paint app is not running")
            status = False

        user_msg = "Hot unplug EFP." \
                   "\n[CONFIRM]:Enter yes if Display is unplugged, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Hot unplugged EFP")

        self.__class__.updated_enum_port_list = []
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        for index in range(0, enumerated_display.Count):
            self.__class__.updated_enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        if len(self.__class__.updated_enum_port_list) >= len(self.__class__.enum_port_list):
            window_helper.kill_process_by_name('Notepad.exe')
            window_helper.kill_process_by_name('mspaint.exe')
            self.fail("After unplug of external panel, still number of enumerated displays are same as before")
        self.__class__.enum_port_list = self.__class__.updated_enum_port_list

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_14_step failed")

    ##
    # @brief        This step opens file explorer
    # @return       None

    def t_15_step(self):
        status = True
        alert.info("Opens file explorer and verifies if any corruption")
        logging.info("Step 15: Open file explorer")
        winkb_helper.press('WIN+E')
        time.sleep(10)

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        if not status:
            self.fail("test_15_step failed")

    ##
    # @brief        This step plugs/unplugs panel
    # @return       None

    def t_16_step(self):
        status = True
        user_msg = "Plug any DP VRR external panel" \
                   "\n[CONFIRM]:Enter yes if Display is plugged, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Hot plugged DP VRR external panel")

        self.__class__.updated_enum_port_list = []
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        for index in range(0, enumerated_display.Count):
            self.__class__.updated_enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        if len(self.__class__.updated_enum_port_list) <= len(self.__class__.enum_port_list):
            window_helper.kill_process_by_name('Notepad.exe')
            window_helper.kill_process_by_name('mspaint.exe')
            window_helper.kill_process_by_name('explorer.exe')
            self.fail("After hot plug of EFP, still number of enumerated displays are same as before")
        self.__class__.enum_port_list = self.__class__.updated_enum_port_list

        logging.info("Applying SD eDP")
        ret_val = False
        for display_index in range(enumerated_display.Count):
            gfx_index = enumerated_display.ConnectedDisplays[
                display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            display = str(
                CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[display_index].ConnectorNPortType))
            if enumerated_display.ConnectedDisplays[display_index].IsActive and \
                    display_utility.get_vbt_panel_type(display, gfx_index) is display_utility.VbtPanelType.LFP_DP:
                ret_val = self.__class__.display_config.set_display_configuration_ex(enum.SINGLE, [display])
        if not ret_val:
            window_helper.kill_process_by_name('Notepad.exe')
            window_helper.kill_process_by_name('mspaint.exe')
            window_helper.kill_process_by_name('explorer.exe')
            self.fail("Applying SD eDP failed.")

        if not window_helper.is_process_running("Notepad.exe"):
            logging.error("Notepad app is not running")
            status = False

        if not window_helper.is_process_running("mspaint.exe"):
            logging.error("MSFT paint app is not running")
            status = False

        if not window_helper.is_process_running("explorer.exe"):
            logging.error("MSFT paint app is not running")
            status = False

        user_msg = "Hot unplug external panel." \
                   "\n[CONFIRM]:Enter yes if Display is unplugged, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("Hot unplugged external panel")

        self.__class__.updated_enum_port_list = []
        enumerated_display = self.__class__.display_config.get_enumerated_display_info()
        for index in range(0, enumerated_display.Count):
            self.__class__.updated_enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        if len(self.__class__.updated_enum_port_list) >= len(self.__class__.enum_port_list):
            window_helper.kill_process_by_name('Notepad.exe')
            window_helper.kill_process_by_name('mspaint.exe')
            window_helper.kill_process_by_name('explorer.exe')
            self.fail("After unplug of external panel, still number of enumerated displays are same as before")
        self.__class__.enum_port_list = self.__class__.updated_enum_port_list

        for i in range(5):
            user_msg = "Plug any DP VRR external panel" \
                       "\n[CONFIRM]:Enter yes if Display is plugged, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("Hot plugged DP VRR external panel")

            self.__class__.updated_enum_port_list = []
            enumerated_display = self.__class__.display_config.get_enumerated_display_info()
            for index in range(0, enumerated_display.Count):
                self.__class__.updated_enum_port_list.append(
                    str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
            if len(self.__class__.updated_enum_port_list) <= len(self.__class__.enum_port_list):
                window_helper.kill_process_by_name('Notepad.exe')
                window_helper.kill_process_by_name('mspaint.exe')
                window_helper.kill_process_by_name('explorer.exe')
                self.fail("After hot plug of EFP, still number of enumerated displays are same as before")
            self.__class__.enum_port_list = self.__class__.updated_enum_port_list

            time.sleep(5)
            user_msg = "Hot unplug external panel." \
                       "\n[CONFIRM]:Enter yes if Display is unplugged, else enter no"
            result = alert.confirm(user_msg)
            if not result:
                msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                logging.error(f"User observations: {msg['Message']}")
                status = False
            else:
                logging.info("Hot unplugged external panel")

            self.__class__.updated_enum_port_list = []
            enumerated_display = self.__class__.display_config.get_enumerated_display_info()
            for index in range(0, enumerated_display.Count):
                self.__class__.updated_enum_port_list.append(
                    str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
            if len(self.__class__.updated_enum_port_list) >= len(self.__class__.enum_port_list):
                window_helper.kill_process_by_name('Notepad.exe')
                window_helper.kill_process_by_name('mspaint.exe')
                window_helper.kill_process_by_name('explorer.exe')
                self.fail("After unplug of external panel, still number of enumerated displays are same as before")
            self.__class__.enum_port_list = self.__class__.updated_enum_port_list

        time.sleep(10)

        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                   "\n[CONFIRM]:Enter yes if expectation met, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            status = False
        else:
            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

        window_helper.kill_process_by_name('Notepad.exe')
        window_helper.kill_process_by_name('mspaint.exe')
        window_helper.kill_process_by_name('explorer.exe')

        if not status:
            self.fail("test_16_step failed")

    ##
    # @brief        This step enables PSR2 through registry
    # @return       None

    def t_17_step(self):
        if self.__class__.is_psr2_disable:
            status = True
            alert.info("Enables PSR2 regkey as requested by test")
            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    if panel.is_lfp is False:
                        continue
                    logging.info(f"Panel caps before enabling PSR2  : {panel}")
                    # Re-enable complete PSR2 using PSR2Disable
                    logging.info("Enabling PSR2 via reg key (PSR2Disable)")
                    psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                    if psr_status is False:
                        self.fail(f"FAILED to enable PSR2 for {panel.port}")
                    else:
                        ret_val, reboot_required = display_essential.restart_gfx_driver()
                        if ret_val is False:
                            self.fail(f"FAILED to restart display driver for {adapter.name}")
                        user_msg = "[Expectation]:No Visual artifacts/ corruption/ TDR/ BSOD should occur" \
                                   "[CONFIRM]:Enter yes if expectation met, else enter no"
                        result = alert.confirm(user_msg)
                        if not result:
                            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
                            logging.error(f"User observations: {msg['Message']}")
                            status = False
                        else:
                            logging.info("No Visual artifacts/ corruption/ TDR/ BSOD observed")

            if not status:
                self.fail("test_17_step failed")

    ##
    # @brief        This method is the exit point for test.
    # @return       None
    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class, verbosity=2)
    test_result = runner.run(common.get_test_suite(RrSwitchingIdleWithDesktopNotepadWikipedia))
    TestEnvironment.cleanup(test_result)
