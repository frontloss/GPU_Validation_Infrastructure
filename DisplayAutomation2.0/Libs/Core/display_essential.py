########################################################################################################################
# @file         display_essential.py
# @brief        Contains display essential functions for tdr
# @author       Doriwala Nainesh
########################################################################################################################
import json
import logging
import os
import re
import subprocess
import time

from Libs.Core import driver_escape, registry_access
from Libs.Core.logger import gdhm
from Libs.Core.test_env import state_machine_manager
from Libs.Core.test_env import test_context

# Dump path

dump_path = r"C:\Windows\LiveKernelReports\WATCHDOG"

RETRY_LIMIT = 1  # Restart Display Driver retry count


##
# @brief        Provide system TDR information.
# @param[in]    gfx_index - Graphics Adapter Index
# @return       status - True if TDR Trace is found, False otherwise
def detect_system_tdr(gfx_index):
    # This is to check whether dump is generated or not after TDR generation
    files_in_dump_path = []
    dump_status = False
    if os.path.exists(dump_path):
        for files in os.listdir(dump_path):
            if os.path.isfile(os.path.join(dump_path, files)):
                files_in_dump_path.append(files)
        logging.debug(f"Dump file {files_in_dump_path} in LiveKernelReports")
    for file in files_in_dump_path:
        if file.startswith('WATCHDOG'):
            dump_status = True
    status = False
    if is_discrete_graphics_driver(gfx_index=gfx_index) is True:
        adapter = "igfxnd"
    else:
        adapter = "igfx"
    logging.debug("Checking for TDR Trace in System Event via Get-WinEvent for gfx_index: {} adapter:{}"
                  .format(gfx_index, adapter))

    # The below mentioned code has Format-list is taken from powershell formatting options From Microsoft:
    # https://docs.microsoft.com/en-us/powershell/scripting/samples/using-format-commands-to-change-output-view?view=powershell-7.2

    detect_sys_tdr = subprocess.run(
        ["powershell.exe", "Get-WinEvent", "-FilterHashTable", "@{LogName='system'; ID=4101} | Format-List Message"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    std_out = re.compile(r'[\r\n]').sub(" ", detect_sys_tdr.stdout)
    std_err = re.compile(r'[\r\n]').sub(" ", detect_sys_tdr.stderr)
    if detect_sys_tdr.returncode != 0:
        logging.info(f"[{gfx_index}] Command failed with return code={detect_sys_tdr.returncode}, stdout: {std_out},"
                     f" stderr: {std_err}")
    elif adapter in std_out:
        logging.debug(f"Message: {std_out}")
        logging.info(f"PASS: Found TDR Trace in System Event log for {gfx_index}")
        status = True
    else:
        logging.error(f"FAIL: TDR Not found for {gfx_index}, adapter: {adapter},  stdout: {std_out} ,"
                      f" stderr: {std_err}")
    logging.debug(f"Dump Status : {dump_status}")
    return status or dump_status


##
# @brief        Generate TDR
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    is_displaytdr - True for VSYNC TDR, False for KMD TDR
# @return       result - True if TDR is generated, False otherwise
def generate_tdr(gfx_index, is_displaytdr):
    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                             reg_path=r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers")
    registry_access.write(args=reg_args, reg_name="TdrTestMode", reg_type=registry_access.RegDataType.DWORD,
                          reg_value=1)
    if is_displaytdr:
        result = driver_escape.generate_adapter_tdr(gfx_index=gfx_index, is_displaytdr=is_displaytdr)
        time.sleep(20)  # Sleep for 20 seconds for TDR to happen and logging of events
        logging.debug(f"TDR generation using Escape call : {result}")
        if not detect_system_tdr(gfx_index):
            # try generating TDR using Dxcap if normal escape call fails
            status = dx_cap_generate_tdr()
            logging.debug(f"TDR generation using Dxcap : {status}")
            return status
        return result


##
# @brief        Clear TDR dump from dump location
# @return       bool - True if cleanup successful, False otherwise
def clear_tdr():
    logging.info("Clear TDR dump from LiveKernelReports")
    if os.path.exists(dump_path):
        for files in os.listdir(dump_path):
            if os.path.isfile(os.path.join(dump_path, files)):
                logging.debug("Dump file %s in LiveKernelReports " % files)
                os.remove(os.path.join(dump_path, files))
                if os.path.isfile(os.path.join(dump_path, files)):
                    logging.warning("Dump file %s  not removed in LiveKernelReports " % files)
                    return False
                else:
                    logging.info("Dump file %s removed in LiveKernelReports " % files)
    # Clearing the system event log after detecting the TDR
    clear_system_log()
    return True


##
# @brief        API to identify given adapter if Discrete adapter
# @param[in]    gfx_index - Graphics Adapter Index
# @return       bool - True if discrete adapter, False otherwise
def is_discrete_graphics_driver(gfx_index):
    reg_args = registry_access.StateSeparationRegArgs(gfx_index)
    install_driver_type, _ = registry_access.read(args=reg_args, reg_name="InstallDrvType")
    logging.debug("{} driver type:{}".format(gfx_index, install_driver_type))
    if install_driver_type == 1:
        return True
    return False


##
# @brief        Clears system logs
# @return       bool - True on success, False otherwise
def clear_system_log():
    return_code = subprocess.call(
        ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "clear-eventlog", "system"])
    if return_code == 0:
        logging.info("Clearing the system logs is successful")
        return True
    else:
        logging.error("Failed to clear the system logs.")
        return False


##
# @brief        Helper API to file GDHM bug during failure scenarios
# @param[in]    gfx_index - Graphics Adapter index
# @param[in]    msg - GDHM bug title message
# @return       None
def __report_gdhm_bug(gfx_index: str, msg: str) -> None:
    logging.error(f"{gfx_index}: {msg}")
    gdhm.report_bug(
        f"[SystemUtilityLib] {gfx_index} : {msg}",
        gdhm.ProblemClassification.FUNCTIONALITY,
        gdhm.Component.Test.DISPLAY_INTERFACES
    )


##
# @brief        API to log GFX driver status for Given Adapter
# @param[in]    bus_id - Complete BusID of the driver to be Enabled or Disabled
# @return       driver_status - Possible values [OK or Error or Unknown or Degraded]
def __get_driver_status(bus_id: str) -> str:
    driver_status = ""
    pnputil_status = ""
    json_data = {}
    try:
        pnputil_cmd = f"pnputil /enum-devices /instanceid '{bus_id}'"
        logging.debug(f"Running pnputil command - {pnputil_cmd}")
        pnputil_status = subprocess.run(["powershell", "-Command", pnputil_cmd],
                                        capture_output=True)
        logging.info(f"Driver Status from pnputil: {pnputil_status}")

        pnp_cmd = f"Get-PnpDevice -InstanceId '{bus_id}' | Select-Object Status,InstanceId | ConvertTo-Json"
        logging.debug(f"Running Get-PnPDevice command - {pnp_cmd}")
        json_data = subprocess.getoutput(f"PowerShell -Command \"& {{{pnp_cmd}}}\"")
        driver_status = json.loads(json_data)["Status"]
        logging.info(f"Driver Status from Get-PnPDevice: {' '.join(json_data.split())}")
    except json.JSONDecodeError:
        logging.error(f"Driver Status Returned - {json_data}")
        # Handling when JSON data not decoded
        # TODO: Convert driver status strings to pre-defined enum(VSDI-37110)
        if pnputil_status.returncode == 0:
            pnputil_status.stdout.decode().replace('\r\n', ' | ')
            if re.search("Disabled", pnputil_status, re.IGNORECASE):
                driver_status = "Error"
            if re.search("Started", pnputil_status, re.IGNORECASE):
                driver_status = "OK"
        else:
            pnputil_stderr = pnputil_status.stderr.decode().replace('\r\n', ' | ')
            logging.error(f"Error while fetching driver status: {pnputil_stderr}")
    except Exception as e:
        logging.error(f"Unexpected exception while fetching driver status - {e}")
    return driver_status


##
# @brief        API to Disable Graphics Driver for Given Adapter if already Enabled.
# @param[in]    gfx_index - Graphics Adapter Index
# @return       status - True if driver is disabled , False otherwise
def disable_driver(gfx_index: str = 'gfx_0') -> bool:
    counter = 0
    disable_flag = False
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    if adapter_info.isActive:
        bus_id = f"{adapter_info.busDeviceID}\\{adapter_info.deviceInstanceID}"
        # Set power component to Idle for current adapter before disabling driver
        power_status = driver_escape.configure_adapter_power_component(gfx_index, False)
        if power_status is None:
            logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
        logging.info(f"{'PASS' if power_status is True else 'FAIL'}: Configuring 'Idle' status for {gfx_index} adapter")
        while counter <= RETRY_LIMIT:
            disable_command = f"pnputil /disable-device '{bus_id}'"
            logging.debug(f'Disable driver commandline - {disable_command}')
            disable_output = subprocess.run(["powershell", "-Command", disable_command], capture_output=True)
            disable_stdout = disable_output.stdout.decode().replace('\r\n', '|')
            disable_stderr = disable_output.stderr.decode().replace('\r\n', '|')
            logging.info(
                f"Operation : Disabling driver for {gfx_index}: {bus_id}. Returned status code : {disable_output.returncode}. Returned stdout : {disable_stdout}. Returned stderr : {disable_stderr} ")
            time.sleep(10)
            driver_status = __get_driver_status(bus_id)
            logging.info(f"Current Driver Status : {driver_status}")
            counter += 1
            if driver_status.upper() == "ERROR":
                disable_flag = True
                break
        if disable_flag:
            logging.info("{} driver Disabled Successfully".format(gfx_index))
            disable_adapter = 'disable'
            test_context.TestContext._update_gfx_active_status(gfx_index, disable_adapter)
            state_machine_manager.StateMachine().update_adapter_state_in_context(gfx_index, False)
            return True
        else:
            __report_gdhm_bug(gfx_index, "Failed to disable display driver")
            return False
    logging.info("{} driver Already Disabled".format(gfx_index))
    return True


##
# @brief        API to Enable Graphics Driver for Given Adapter if already Disabled.
# @param[in]    gfx_index - Graphics adapter Index
# @return       status - True if driver is enabled, False otherwise
def enable_driver(gfx_index: str = 'gfx_0') -> bool:
    counter = 0
    enable_flag = False
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    if adapter_info.isActive is False:
        bus_id = f"{adapter_info.busDeviceID}\\{adapter_info.deviceInstanceID}"
        while counter <= RETRY_LIMIT:
            enable_command = f"pnputil /enable-device '{bus_id}'"
            logging.debug(f'Enable driver commandline - {enable_command}')
            enable_output = subprocess.run(["powershell", "-Command", enable_command], capture_output=True)
            enable_stdout = enable_output.stdout.decode().replace('\r\n', '|')
            enable_stderr = enable_output.stderr.decode().replace('\r\n', '|')
            logging.info(
                f"Operation : Enabling driver for {gfx_index}: {bus_id}. Returned status code : {enable_output.returncode}. Returned stdout : {enable_stdout}. Returned stderr : {enable_stderr}")
            time.sleep(10)
            driver_status = __get_driver_status(bus_id)
            logging.info(f"Current Driver Status : {driver_status}")
            counter += 1
            if driver_status.upper() == "OK":
                enable_flag = True
                break
        if enable_flag:
            logging.info("{} driver Enabled Successfully".format(gfx_index))
            enable_adapter = 'enable'
            test_context.TestContext._update_gfx_active_status(gfx_index, enable_adapter)
            # context.Context().adapters[gfx_index].gfx_status = True
            state_machine_manager.StateMachine().update_adapter_state_in_context(gfx_index, True)
            # Set power component to Active for current adapter after enabling driver
            power_status = driver_escape.configure_adapter_power_component(gfx_index, True)
            if power_status is None:
                logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
            logging.info(
                f"{'PASS' if power_status is True else 'FAIL'}: Configuring 'Active' status for {gfx_index} adapter")
            return True
        else:
            __report_gdhm_bug(gfx_index, "Failed to enable display driver")
            assert False, "Gfx driver(s) is/are not running!"
    logging.info("{} driver is still Running".format(gfx_index))
    return True


##
# @brief        API to Disable and Enable Graphics driver for Given Adapter
# @param[in]    gfx_index - Graphics adapter Index (Default value is 'gfx_0' for handling Single Adapter Case)
# @return       status - True if driver restarted, False otherwise
def restart_display_driver(gfx_index: str = 'gfx_0') -> bool:
    disable_status = disable_driver(gfx_index)
    enable_status = enable_driver(gfx_index)
    return disable_status and enable_status


##
# @brief        API to restart all Graphics driver for all Adapters
# @return       (status, is_reboot_required) - (Returns True if restart successful False otherwise,
#               True if reboot of system is required, False otherwise)
def restart_gfx_driver() -> (bool, bool):
    status, is_reboot_required = False, False
    # restart_driver_cmd = "pnputil /restart-device /class Display" @Todo: To be updated once Pre-si is migrated to Nickel OS
    # Adapter details required to restart all gfx drivers
    adapter_info_dict = test_context.TestContext.get_gfx_adapter_details()

    disable_adapter = 'disable'
    for gfx_index in adapter_info_dict.keys():
        # Set power component to Idle for current adapter before disabling driver
        power_status = driver_escape.configure_adapter_power_component(gfx_index, False)
        if power_status is None:
            logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
        logging.info(f"{'PASS' if power_status is True else 'FAIL'}: Configuring 'Idle' status for {gfx_index} adapter")
        test_context.TestContext._update_gfx_active_status(gfx_index, disable_adapter)
        state_machine_manager.StateMachine().update_adapter_state_in_context(gfx_index, False)

    for adapter_info in adapter_info_dict.values():
        bus_id = f"{adapter_info.busDeviceID}\\{adapter_info.deviceInstanceID}"
        restart_driver_cmd = f"pnputil /restart-device '{bus_id}'"
        logging.debug(f'Restart driver commandline - {restart_driver_cmd}')
        cmd_output = subprocess.run(["powershell", "-Command", restart_driver_cmd], capture_output=True)
        cmd_output_stdout = cmd_output.stdout.decode().replace('\r\n', ' | ')
        cmd_output_stderr = cmd_output.stderr.decode().replace('\r\n', ' | ')
        logging.info(
            f"Restart Command Output for {bus_id}- Returned code : {cmd_output.returncode}. Returned stdout : {cmd_output_stdout}. Returned stderr : {cmd_output_stderr}")
        time.sleep(20)

        # Note: PnP Util will report this statement if system reboot is required
        # System reboot is needed to complete configuration operations!
        if "System reboot" in cmd_output_stdout:  # Restart failed and Reboot required
            # User needs to reboot the system for restart driver to take effect, as requested by OS.
            # Leaving the status variable as False.
            logging.warning("Found reboot requirement during driver restart!!")
            __report_gdhm_bug(adapter_info.gfxIndex,
                              "[WARNING] Found system reboot requirement during gfx driver restart")
            is_reboot_required |= True
        elif "restarted" in cmd_output_stdout:  # Restart success and Reboot not required
            logging.info("Restarted the driver successfully")
            status = True
        else:  # Restart failed and reboot not required
            __report_gdhm_bug(adapter_info.gfxIndex, "Failed to restart display driver")
            assert False, "Gfx driver(s) is/are not running!"
    if is_reboot_required:
        status = False

    enable_adapter = 'enable'
    if is_reboot_required or status:
        for gfx_index in adapter_info_dict.keys():
            test_context.TestContext._update_gfx_active_status(gfx_index, enable_adapter)
            state_machine_manager.StateMachine().update_adapter_state_in_context(gfx_index, True)
            # Set power component to Active for current adapter after enabling driver
            power_status = driver_escape.configure_adapter_power_component(gfx_index, True)
            if power_status is None:
                logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
            logging.info(
                f"{'PASS' if power_status is True else 'FAIL'}: Configuring 'Active' status for {gfx_index} adapter")
    return status, is_reboot_required


##
# @brief        API to check if the process is running
# @param[in]    process_name - process name like "exe_name.exe" Example: "OPMTester.exe"
# @return       status - True if process is running, False otherwise
def is_process_running(process_name):
    task_manager_out = subprocess.run('tasklist', capture_output=True)
    task_manager_lines = task_manager_out.stdout.decode()
    if task_manager_out.returncode != 0 or len(task_manager_lines) == 0:
        logging.error("Couldn't get tasklist.")
        return False

    for line in task_manager_lines.splitlines():
        try:
            if process_name in line:
                logging.info(f"{process_name} is running.")
                return True
        except Exception as e:
            logging.error(f"Exception occurred while fetching tasklist. {e}")

    logging.info(f"{process_name} is not running.")
    return False


##
# @brief        API to generate TDR using dxcap exe
# @param[in]    None
# @return       status - True if TDR generation successful, False otherwise
def dx_cap_generate_tdr():
    process_list = subprocess.run(["powershell", "-Command", "dxcap.exe -forcetdr"], capture_output=True)
    if process_list.returncode == 0:
        logging.info("TDR generation Successful")
        time.sleep(20)  # Sleep for 20 seconds for TDR to happen and logging of events
        return True
    else:
        logging.error(f"ERROR MESSAGE: {process_list.stderr}")
        gdhm.report_bug(
            title="[DisplayEssentials] : Failed to generate display TDR",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        return False
