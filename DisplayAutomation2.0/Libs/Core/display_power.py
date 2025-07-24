#######################################################################################################################
# @file     display_power.py
# @brief    Python wrapper helper module provides multiple display power related functionality
# @author   Vinod D S
#######################################################################################################################


import ctypes
import logging
import os
import re
import shutil
import subprocess
import time
from Lib.enum import IntEnum  # @Todo: Override with Built-in python3 enum script path
from ctypes import wintypes

import win32api
import win32gui

from Libs.Core import enum, driver_escape
from Libs.Core.core_base import singleton
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import gdhm, html
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import state_machine_manager
from Libs.Core.test_env import test_context


WIN32API_MOUSEEVENTF_MOVE = 0x0001
WIN32GUI_SC_MONITORPOWER = 0xF170
WIN32GUI_WM_SYSCOMMAND = 0x0112
WIN32GUI_MONITOR_OFF = 2
DISPLAY_POWER_SIMBATT = os.path.join(test_context.COMMON_BIN_FOLDER, "SimulatedBattery_Control.vbs")
DISPLAY_POWER_PWRTEST = os.path.join(test_context.COMMON_BIN_FOLDER, "pwrtest.exe")


##
# @brief        PowerScheme Enum
# @details      List of all Power Schemes available
class PowerScheme(IntEnum):
    UNDEFINED = 0
    POWER_SAVER = 1
    BALANCED = 2
    HIGH_PERFORMANCE = 3


##
# @brief        PowerEvent Enum
# @details      List of Power Events available
class PowerEvent(IntEnum):
    CS = 0
    S3 = 1
    S4 = 2
    S5 = 3
    SHUTDOWN = 4
    MonitorPowerOffOn = 5


##
# @brief        MonitorPower Enum
# @details      List of Monitor Turnoff Events available
class MonitorPower(IntEnum):
    OFF_ON = 0
    OFF = 1
    ON = 2


##
# @brief        LidSwitchOption Enum
# @details      List of all Lid Switch Power States available
class LidSwitchOption(IntEnum):
    DO_NOTHING = 0
    SLEEP = 1
    HIBERNATE = 2
    SHUTDOWN = 3



##
# @brief        PowerSource Enum
# @details      List of Power Line status type available
class PowerSource(IntEnum):
    DC = 0
    AC = 1
    INVALID = 255


##
# @brief        WakeTimersStatus Enum
# @details      Allow wake timers status
class WakeTimersStatus(IntEnum):
    DISABLE = 0
    ENABLE = 1
    IMPORTANT_WAKE_TIMERS_ONLY = 2



##
# @brief        SystemPowerStatus Structure
class SystemPowerStatus(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
    ]


##
# @brief        DisplayPower class which exposes the multiple python APIs related to display power
@singleton
class DisplayPower(object):

    ##
    # @brief        API for getting the current power scheme
    # @details      Get the current power scheme Ex: Balanced or Power saver.
    # @return       pwr_scheme - PowerScheme enum
    def get_current_power_scheme(self):
        result = subprocess.check_output(['powercfg.exe', '/getactivescheme'], stderr=subprocess.STDOUT,
                                         universal_newlines=True)
        pwr_scheme = PowerScheme.UNDEFINED
        if "POWER SAVER" in result.upper():
            pwr_scheme = PowerScheme.POWER_SAVER
        elif "BALANCED" in result.upper():
            pwr_scheme = PowerScheme.BALANCED
        elif "HIGH PERFORMANCE" in result.upper():
            pwr_scheme = PowerScheme.HIGH_PERFORMANCE
        return pwr_scheme

    ##
    # @brief        API to switch the current power scheme
    # @details      Switch the power scheme Ex: Balanced or Power saver
    # @param[in]    pwr_scheme - Power scheme to be applied
    # @return       bool - True if the power scheme is set to the required
    def set_current_power_scheme(self, pwr_scheme):
        cur_pwr_scheme = self.get_current_power_scheme()
        if pwr_scheme == cur_pwr_scheme:
            return True

        if pwr_scheme == PowerScheme.POWER_SAVER:
            subprocess.check_output(['powercfg.exe', '/setactive', 'SCHEME_MAX'], stderr=subprocess.STDOUT,
                                    universal_newlines=True)
        elif pwr_scheme == PowerScheme.BALANCED:
            subprocess.check_output(['powercfg.exe', '/setactive', 'SCHEME_BALANCED'], stderr=subprocess.STDOUT,
                                    universal_newlines=True)
        elif pwr_scheme == PowerScheme.HIGH_PERFORMANCE:
            subprocess.check_output(['powercfg.exe', '/setactive', 'SCHEME_MIN'], stderr=subprocess.STDOUT,
                                    universal_newlines=True)
        return True

    ##
    # @brief            API to verify Windows Driver Testing Framework installation
    # @return           ret_val - True if Windows Driver Testing Framework installed, False otherwise
    def is_wdtf_installed(self):
        try:
            subprocess.check_output(['reg.exe', 'query', 'HKLM\Software\Microsoft\WDTF'], stderr=subprocess.STDOUT,
                                    universal_newlines=True)
            ret_val = True
        except subprocess.CalledProcessError as regexc:
            logging.debug("error code %s, %s" % (regexc.returncode, regexc.output))
            ret_val = False
        return ret_val

    ##
    # @brief        API to validate system support for specified power state
    # @param[in]    power_state - Power state to verify for support in current system
    # @return       bool - True if power state is supported, False otherwise
    def is_power_state_supported(self, power_state):
        if power_state == PowerEvent.S5 or power_state == PowerEvent.SHUTDOWN:
            return True

        result = subprocess.check_output(['powercfg.exe', '/a'], stderr=subprocess.STDOUT, universal_newlines=True)
        until_str = "The following sleep states are not available on this system:"
        result = result[0:result.find(until_str)]
        if (power_state == PowerEvent.CS) and ("standby (s0 low power idle)".upper() in result.upper()):
            return True
        elif (power_state == PowerEvent.S3) and ("standby (s3)".upper() in result.upper()):
            return True
        elif (power_state == PowerEvent.S4) and ("hibernate".upper() in result.upper()):
            return True

        return False

    ##
    # @brief        API for invoking power events.
    # @param[in]    power_state - Power state to be invoked
    # @param[in]    sleep_time - Sleep duration from resuming the system from power state
    # @return       bool - True if power event successful, False otherwise
    def invoke_power_event(self, power_state: PowerEvent, sleep_time=60):
        adapter_info_dict = test_context.TestContext.get_gfx_adapter_details()
        # Set power component to Idle for all adapters before invoking power events
        for gfx_index in adapter_info_dict.keys():
            status = driver_escape.configure_adapter_power_component(gfx_index, False)
            if status is None:
                logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
            logging.info(f"{'PASS' if status is True else 'FAIL'}: Configuring 'Idle' status for {gfx_index} adapter")
        if power_state == PowerEvent.S5 or power_state == PowerEvent.SHUTDOWN:
            if sleep_time == 0:
                html.step_start("Rebooting the system", True)
            else:
                html.step_start(f"Setting a reboot timer of {sleep_time} seconds", True)
                logging.info(f"System will be rebooted after {sleep_time} seconds")
            restart_flag = "/s"
            if power_state == PowerEvent.S5:
                restart_flag = "/r"
            cmd = f"shutdown.exe {restart_flag} /f /t {sleep_time} /d u:0:0"
            gta_state_manager.update_reboot_state(True)
            html.step_end()
            subprocess.check_output(cmd.split(" "), stderr=subprocess.STDOUT, universal_newlines=True)
            # Below code will be executed only in reboot failure cases
            # Added delay to stop python script from proceeding after shutdown command is issued to OS
            time.sleep(sleep_time + 30)
            evtx_logs = os.path.join(test_context.LOG_FOLDER, "evtx_logs")
            shutil.make_archive(evtx_logs, 'zip', "C:/Windows/System32/winevt/Logs")
            return False

        html.step_start(f"Invoking {power_state.name} for {sleep_time} seconds", True)
        if not os.path.exists(DISPLAY_POWER_PWRTEST):
            logging.error("File does not exist - %s" % DISPLAY_POWER_PWRTEST)
            html.step_end()
            return False

        if power_state == PowerEvent.S4:
            subprocess.check_output(['powercfg.exe', '/hibernate', 'on'], stderr=subprocess.STDOUT,
                                    universal_newlines=True)

        if self.is_power_state_supported(power_state) is False:
            logging.error("System does not support %s" % power_state.name)
            gdhm.report_bug(
                f"[DisplayPowerLib] {power_state.name} is not supported on system",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
            html.step_end()
            return False  # System doesn't support the power state

        cmd = ""
        if power_state == PowerEvent.CS:
            if self.is_wdtf_installed() is False:
                logging.error("Windows Driver Testing Framework is not installed")
                html.step_end()
                return False
            cmd = "%s /cs /c:1 /p:%s" % (DISPLAY_POWER_PWRTEST, sleep_time)
        elif power_state == PowerEvent.S3:
            cmd = "%s /sleep /s:3 /c:1 /p:%s" % (DISPLAY_POWER_PWRTEST, sleep_time)
        elif power_state == PowerEvent.S4:
            cmd = "%s /sleep /s:4 /c:1 /p:%s" % (DISPLAY_POWER_PWRTEST, sleep_time)

        gta_state_manager.configure_tc(launch=False)  # Kill ThinClient during powerevent. Can kill TC if already killed
        # Generates ==> pwrtestlog.log
        subprocess.check_output(cmd.split(" "), stderr=subprocess.STDOUT, universal_newlines=True)
        logging.info(f"\tResumed from {power_state.name} successfully")
        # Set power component to Active for all adapters after resuming
        for gfx_index in adapter_info_dict.keys():
            status = driver_escape.configure_adapter_power_component(gfx_index, True)
            if status is None:
                logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
            logging.info(f"{'PASS' if status is True else 'FAIL'}: Configuring 'Active' status for {gfx_index} adapter")
        html.step_end()
        state_machine_manager.StateMachine().update_adapter_display_context()
        driver_status, valsim_status = driver_interface.DriverInterface().verify_graphics_driver_status()
        ret_status = True
        if driver_status is False:
            gdhm.report_bug(
                f"[DisplayPowerLib] Intel Graphics Driver is not running after invoking {power_state.name}",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P1,
                gdhm.Exposure.E1
            )
            ret_status = False
            logging.error(f"Intel Graphics Driver is not running after invoking {power_state.name}")
        if valsim_status is False:
            gdhm.report_bug(
                f"[DisplayPowerLib] GfxValsim is not running after invoking {power_state.name}",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P1,
                gdhm.Exposure.E1
            )
            ret_status = False
            logging.error(f"GfxValsim is not running after invoking {power_state.name}")
        return ret_status

    ##
    # @brief        API for invoking monitor turnoff.
    # @param[in]    mt_state - Monitor turnoff state to be invoked
    # @param[in]    waiting_time - Sleep duration from turning on the monitor
    # @return       bool - True if monitor turnoff event successful, False otherwise
    def invoke_monitor_turnoff(self, mt_state, waiting_time=30):
        adapter_info_dict = test_context.TestContext.get_gfx_adapter_details()
        if mt_state in [MonitorPower.OFF_ON, MonitorPower.OFF]:
            html.step_start(f"Turning OFF the monitors for {waiting_time} seconds", highlight=True)
        else:
            html.step_start(f"Turning ON the monitors", highlight=True)

        # Verify whether system is CS enabled or not. If system is CS enabled, we should not perform monitor turn off.
        # Because once monitor is off, system will go to low power state and automation application can not resume
        # from CS state. So system will remain in CS state forever unless we manually do keyboard or mouse event.
        if self.is_power_state_supported(PowerEvent.CS) is True:
            logging.error("Monitor turnoff does not work in connected standby enabled system")
            gdhm.report_bug(
                f"[DisplayPowerLib] Monitor TurnOff event is being requested on CS system",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
            html.step_end()
            return False
        ret_status = True
        if mt_state == MonitorPower.OFF_ON or mt_state == MonitorPower.OFF:
            # Set power component to Idle for all adapters before invoking power events
            for gfx_index in adapter_info_dict.keys():
                status = driver_escape.configure_adapter_power_component(gfx_index, False)
                if status is None:
                    logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
                logging.info(
                    f"{'PASS' if status is True else 'FAIL'}: Configuring 'Idle' status for {gfx_index} adapter")
            hwnd = win32gui.FindWindow(None, None)
            win32gui.SendMessage(hwnd, WIN32GUI_WM_SYSCOMMAND, WIN32GUI_SC_MONITORPOWER, WIN32GUI_MONITOR_OFF)
            logging.info("\tTurned OFF the monitors successfully")
            time.sleep(waiting_time)
            state_machine_manager.StateMachine().update_inactive_display_in_context()

        if mt_state == MonitorPower.OFF_ON or mt_state == MonitorPower.ON:
            logging.info(f"Turning ON the monitors")
            # Set power component to Active for all adapters after resuming
            for gfx_index in adapter_info_dict.keys():
                status = driver_escape.configure_adapter_power_component(gfx_index, True)
                if status is None:
                    logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
                logging.info(
                    f"{'PASS' if status is True else 'FAIL'}: Configuring 'Active' status for {gfx_index} adapter")

            win32api.mouse_event(WIN32API_MOUSEEVENTF_MOVE, 0, 1, 0, 0)
            time.sleep(1)
            win32api.mouse_event(WIN32API_MOUSEEVENTF_MOVE, 0, 2, 0, 0)
            time.sleep(4)
            logging.info("\tTurned ON the monitors successfully")
            state_machine_manager.StateMachine().update_adapter_display_context()
            driver_status, valsim_status = driver_interface.DriverInterface().verify_graphics_driver_status()
            if driver_status is False:
                gdhm.report_bug(
                    f"[DisplayPowerLib] Intel Graphics Driver is not running after invoking {mt_state.name}",
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES,
                    gdhm.Priority.P1,
                    gdhm.Exposure.E1
                )
                ret_status = False
                logging.error(f"Intel Graphics Driver is not running after invoking {mt_state.name}")
            if valsim_status is False:
                gdhm.report_bug(
                    f"[DisplayPowerLib] GfxValsim is not running after invoking {mt_state.name}",
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES,
                    gdhm.Priority.P1,
                    gdhm.Exposure.E1
                )
                ret_status = False
                logging.error(f"GfxValsim is not running after invoking {mt_state.name}")

        html.step_end()
        return ret_status

    ##
    # @brief        API to get Lid switch support
    # @return       bool - True if Lid switch is supported, False otherwise
    def is_lid_present(self):
        out_dict = win32api.GetPwrCapabilities()
        return out_dict['LidPresent']

    ##
    # @brief        Exposed API for setting power state for lid switch
    # @param[in]    lid_switch_power_state - power state to be set for lid switch
    # @param[in]    power_plan - Power scheme to be applied
    #               If power_plan is not given, then lid switch power state of BALANCED power plan will be set
    # @param[in]    power_line - Power Line status to be applied
    #               If power_line is not given, then lid switch power state of the both AC and DC power line will be set
    # @return       bool - True if successful, False otherwise
    def set_lid_switch_power_state(self, lid_switch_power_state: LidSwitchOption, power_plan=PowerScheme.BALANCED,
                                   power_line=None):
        power_cfg_queries = None

        # Set power cfg query based on power line status
        if power_line is None:
            power_cfg_queries = [['powercfg.exe', '/setacvalueindex'], ['powercfg.exe', '/setdcvalueindex']]
        else:
            if power_line == PowerSource.AC:
                power_cfg_queries = [['powercfg.exe', '/setacvalueindex']]
            elif power_line == PowerSource.DC:
                power_cfg_queries = [['powercfg.exe', '/setdcvalueindex']]
            elif power_line == PowerSource.INVALID:
                logging.error("Invalid power line status")
                return False

        if power_plan == PowerScheme.POWER_SAVER:
            for query in power_cfg_queries:
                query.append('SCHEME_MAX')
        elif power_plan == PowerScheme.BALANCED:
            for query in power_cfg_queries:
                query.append('SCHEME_BALANCED')
        elif power_plan == PowerScheme.HIGH_PERFORMANCE:
            for query in power_cfg_queries:
                query.append('SCHEME_MIN')
        else:
            logging.error("Invalid power plan")
            return False

        # Set alias for buttons sub group and lid action settings
        for query in power_cfg_queries:
            query.append("SUB_BUTTONS LIDACTION {0}".format(lid_switch_power_state.value))

            # Execute the query
            subprocess.call(query, stderr=subprocess.STDOUT)

        return True

    ##
    # @brief        Exposed API for getting power state for lid switch.
    # @param[in]    power_plan - Power scheme used for querying.
    #               If power_plan is not given, then lid switch power state of current active power plan will be
    #               returned
    # @param[in]    power_line - Power Line status used for querying.
    #               If power_line is not given, then lid switch power state of the current active power line will be
    #               returned
    # @return       int - LidSwitchOption value if available, None otherwise
    def get_lid_switch_power_state(self, power_plan=PowerScheme.BALANCED, power_line=None):
        power_cfg_query = ['powercfg.exe', '/query']

        # Set alias for power scheme
        if power_plan == PowerScheme.POWER_SAVER:
            power_cfg_query.append('SCHEME_MAX')
        elif power_plan == PowerScheme.BALANCED:
            power_cfg_query.append('SCHEME_BALANCED')
        elif power_plan == PowerScheme.HIGH_PERFORMANCE:
            power_cfg_query.append('SCHEME_MIN')
        else:
            logging.error("Invalid power plan")
            return None

        # Set alias for buttons sub group and lid action settings
        power_cfg_query += ['SUB_BUTTONS', 'LIDACTION']

        # Execute the powercfg query and get the output
        power_cfg_query_output = subprocess.check_output(power_cfg_query, stderr=subprocess.STDOUT,
                                                         universal_newlines=True)
        if power_cfg_query_output == '' or power_cfg_query_output is None:
            return None

        # if power line is not passed, get the current power line status
        if power_line is None:
            power_line = self.get_current_powerline_status()

        if power_line == PowerSource.INVALID:
            logging.error("Invalid power line status")
            return None

        # Get lid switch power state
        match = None
        if power_line == PowerSource.AC:
            ac_pattern = r"Current AC Power Setting Index: 0x0000000[0-3]+"
            match = re.search(ac_pattern, power_cfg_query_output, re.I)
        elif power_line == PowerSource.DC:
            dc_pattern = r"Current DC Power Setting Index: 0x0000000[0-3]+"
            match = re.search(dc_pattern, power_cfg_query_output, re.I)

        if match is None:
            return None
        return LidSwitchOption(int(match.group(0)[-1])).value

    ##
    # @brief        API for getting the power line status.
    # @return       Enum - PowerSource
    def get_current_powerline_status(self):
        system_power_status_p = ctypes.POINTER(SystemPowerStatus)

        GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
        GetSystemPowerStatus.argtypes = [system_power_status_p]
        GetSystemPowerStatus.restype = wintypes.BOOL

        status = SystemPowerStatus()
        if not GetSystemPowerStatus(ctypes.pointer(status)):
            return PowerSource.INVALID
        return PowerSource(status.ACLineStatus)

    ##
    # @brief        API for enabling or disabling the simbatt.
    # @param[in]    enable_flag - True to enable simbatt, False to disable
    # @return       bool - True if successful, False otherwise
    def enable_disable_simulated_battery(self, enable_flag):
        if self.is_wdtf_installed() is False:
            logging.error("Windows Driver Testing Framework is NOT installed")
            return False

        if self.is_simulated_battery_enabled() == enable_flag:
            logging.warning("Simulated Battery is already {0}".format("ENABLED" if enable_flag else "DISABLED"))
            return True

        if not os.path.exists(DISPLAY_POWER_SIMBATT):
            logging.error("File does NOT exist - %s" % DISPLAY_POWER_SIMBATT)
            return False

        simbatt_cmd_1 = '/setup' if enable_flag else '/cleanup'
        simbatt_cmd_2 = '/cleanup' if enable_flag else '/setup'
        subprocess.check_output([DISPLAY_POWER_SIMBATT, simbatt_cmd_1], stderr=subprocess.STDOUT, shell=True,
                                universal_newlines=True)
        wait_time = 1
        while self.is_simulated_battery_enabled() != enable_flag:
            time.sleep(1)
            wait_time += 1
            if wait_time >= 75:
                gdhm.report_bug(
                    f"[DisplayPowerLib] Failed to {'enable' if enable_flag else 'disable'} Simulated Battery",
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES
                )
                return False
            if int(wait_time % 15) == 0:
                logging.warning(
                    "Failed to {0} Simulated Battery. Trying again.".format("enable" if enable_flag else "disable"))
                subprocess.check_output([DISPLAY_POWER_SIMBATT, simbatt_cmd_2], stderr=subprocess.STDOUT, shell=True,
                                        universal_newlines=True)
                time.sleep(1)
                if enable_flag is False:
                    time.sleep(15)
                subprocess.check_output([DISPLAY_POWER_SIMBATT, simbatt_cmd_1], stderr=subprocess.STDOUT, shell=True,
                                        universal_newlines=True)
        return True

    ##
    # @brief        API to verify simbatt is enabled
    # @return       bool - True if enabled, False otherwise
    def is_simulated_battery_enabled(self):
        if self.is_wdtf_installed() is False:
            logging.error("Windows Driver Testing Framework is NOT installed")
            return False

        cmd = f"pnputil /enum-devices /class Battery | Select-String -Pattern 'Simbatt' -Context 0,5"
        battery_status = subprocess.run(["powershell", "-Command", cmd], capture_output=True)

        if battery_status.returncode != 0:
            battery_status_stderr = battery_status.stderr.decode('utf-8', 'ignore').replace("\r\n", " | ")
            logging.error(f"Error fetching simbatt status: {battery_status_stderr}")
            return False

        battery_status_stdout = battery_status.stdout.decode('utf-8', 'ignore')
        # no matching device found
        if not battery_status_stdout:
            return False

        battery_status_stdout = battery_status_stdout.split('\r\n')
        for i in range(len(battery_status_stdout)):
            battery_instance = battery_status_stdout[i]
            if battery_instance.strip().startswith("Status") and battery_instance.split(":")[-1].strip() == "Started":
                return True
            else: # To check if "Status : Started" even if statement is not parsed correctly
                if battery_instance.strip().startswith("Status") and "Started" in battery_status_stdout[i + 1]:
                    return True
        return False

    ##
    # @brief        API for setting the power line status.
    # @param[in]    pwrline_state  -  Power line status to be applied
    # @return       bool - True if setting power line status is successful, False otherwise
    def set_current_powerline_status(self, pwrline_state: PowerSource):
        html.step_start(f"Setting Power Source to {pwrline_state.name}")
        if pwrline_state == PowerSource.INVALID:
            logging.error("Invalid powerline state provided")
            html.step_end()
            return False

        cur_pwrline_state = self.get_current_powerline_status()
        if cur_pwrline_state == pwrline_state:
            logging.info(f"Power Source is already set to {pwrline_state.name}")
            html.step_end()
            return True

        if self.is_wdtf_installed() is False:
            logging.error("Windows Driver Testing Framework is not installed")
            gdhm.report_bug("[DisplayPowerLib] Windows Driver Testing Framework is not installed",
                            gdhm.ProblemClassification.FUNCTIONALITY, gdhm.Component.Test.DISPLAY_INTERFACES,
                            gdhm.Priority.P3, gdhm.Exposure.E3)
            html.step_end()
            return False

        if self.is_simulated_battery_enabled() is False:
            logging.error("Simulated Battery is NOT enabled")
            gdhm.report_bug("[DisplayPowerLib] Simulated Battery is NOT enabled",
                            gdhm.ProblemClassification.FUNCTIONALITY, gdhm.Component.Test.DISPLAY_INTERFACES,
                            gdhm.Priority.P3, gdhm.Exposure.E3)
            html.step_end()
            return False

        if not os.path.exists(DISPLAY_POWER_SIMBATT):
            logging.error("File does not exist - %s" % DISPLAY_POWER_SIMBATT)
            html.step_end()
            return False

        if pwrline_state == PowerSource.DC:
            subprocess.check_output([DISPLAY_POWER_SIMBATT, '/dc'], stderr=subprocess.STDOUT, shell=True,
                                    universal_newlines=True)
        else:
            subprocess.check_output([DISPLAY_POWER_SIMBATT, '/ac'], stderr=subprocess.STDOUT, shell=True,
                                    universal_newlines=True)

        time.sleep(2)  # wait for 2 seconds
        cur_pwrline_state = self.get_current_powerline_status()
        result = cur_pwrline_state == pwrline_state
        if result is False:
            gdhm.report_bug(
                f"[DisplayPowerLib] Failed to set powerline status to {pwrline_state.name}",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
            logging.error(f"Failed to switch power source to {pwrline_state.name}")
            return result

        logging.info("\tPASS: Expected Power Source= {0}, Actual= {0}".format(pwrline_state.name))
        html.step_end()
        return result

    ##
    # @brief        Exposed API for setting wake timers
    # @param[in]    wake_timers_state - WakeTimersStatus enum
    # @param[in]    power_plan - Power scheme used for querying
    #               If power_plan is not given, then wake timers of current power plan will be set
    # @param[in]    power_line - Power Line status used for querying
    #               If power_line is not given, then wake timers of current power line will be set
    # @return       bool - True if applied successfully, False otherwise
    def set_wake_timers(self, wake_timers_state, power_plan=None, power_line=None):

        # Set power cfg query based on power line status
        if power_line is None:
            power_line = self.get_current_powerline_status()

        if power_line == PowerSource.INVALID:
            logging.error("Invalid power line status")
            return False

        if power_plan is None:
            power_plan = self.get_current_power_scheme()

        if power_plan == PowerScheme.UNDEFINED:
            logging.error("Invalid power plan")
            return False

        power_cfg_query = None
        if power_line == PowerSource.AC:
            power_cfg_query = ['powercfg.exe', '/setacvalueindex']
        elif power_line == PowerSource.DC:
            power_cfg_query = ['powercfg.exe', '/setdcvalueindex']

        # Set alias for power scheme
        if power_plan == PowerScheme.POWER_SAVER:
            power_cfg_query.append('SCHEME_MAX')
        elif power_plan == PowerScheme.BALANCED:
            power_cfg_query.append('SCHEME_BALANCED')
        elif power_plan == PowerScheme.HIGH_PERFORMANCE:
            power_cfg_query.append('SCHEME_MIN')

        # Set alias for sub group and wake timers settings
        power_cfg_query += ["SUB_SLEEP", "RTCWAKE", str(wake_timers_state)]

        # Execute the query
        subprocess.call(power_cfg_query, stderr=subprocess.STDOUT)

        return True

    ##
    # @brief        Exposed API for getting wake timers
    # @param[in]    power_plan - Power scheme used for querying
    #               If power_plan is not given, then wake timers of current power plan will be returned
    # @param[in]    power_line - Power Line status used for querying
    #               If power_line is not given, then wake timers of current power line will be returned
    # @return       wake_timer if executed correctly, otherwise None
    def get_wake_timers(self, power_plan=None, power_line=None):

        # Set power cfg query based on power line status
        if power_line is None:
            power_line = self.get_current_powerline_status()

        if power_line == PowerSource.INVALID:
            logging.error("Invalid power line status")
            return None

        if power_plan is None:
            power_plan = self.get_current_power_scheme()

        if power_plan == PowerScheme.UNDEFINED:
            logging.error("Invalid power plan")
            return None

        power_cfg_query = ['powercfg.exe', '/query']

        # Set alias for power scheme
        if power_plan == PowerScheme.POWER_SAVER:
            power_cfg_query.append('SCHEME_MAX')
        elif power_plan == PowerScheme.BALANCED:
            power_cfg_query.append('SCHEME_BALANCED')
        elif power_plan == PowerScheme.HIGH_PERFORMANCE:
            power_cfg_query.append('SCHEME_MIN')

        # Set alias for sub group and wake timers settings
        power_cfg_query += ['SUB_SLEEP', 'RTCWAKE']

        # Execute the powercfg query and get the output
        power_cfg_query_output = subprocess.check_output(power_cfg_query, stderr=subprocess.STDOUT,
                                                         universal_newlines=True)
        if power_cfg_query_output == '' or power_cfg_query_output is None:
            return None

        # Get lid switch power state
        match = None
        if power_line == PowerSource.AC:
            ac_pattern = r"Current AC Power Setting Index: 0x0000000[0-3]+"
            match = re.search(ac_pattern, power_cfg_query_output, re.I)
        elif power_line == PowerSource.DC:
            dc_pattern = r"Current DC Power Setting Index: 0x0000000[0-3]+"
            match = re.search(dc_pattern, power_cfg_query_output, re.I)

        if match is None:
            return None
        return WakeTimersStatus(int(match.group(0)[-1])).value
