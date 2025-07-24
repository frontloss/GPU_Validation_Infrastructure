########################################################################################################################
# @file         etl_tracer.py
# @brief        Python wrapper exposes APIs to capture ETL Trace
# @author       Rohit Kumar, Chandrakanth Pabolu
########################################################################################################################

import enum
import logging
import os
import re
import shutil
from subprocess import run

from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context

TEST_STORE_TRACER_PATH = os.path.join(test_context.TEST_STORE_FOLDER, "CommonBin", "GfxEvents")
GTA_TRACER_PATH = os.path.join(os.getcwd()[:3], "SHAREDBINARY", "920697932", "GfxEvents")
TRACER_PATH = GTA_TRACER_PATH if os.path.exists(GTA_TRACER_PATH) else TEST_STORE_TRACER_PATH
CUSTOM_TRACER_PATH = os.path.join(test_context.TEST_STORE_FOLDER, "CommonBin", "CustomTraceEvents")
XPERF_EXE = os.path.join(test_context.TEST_STORE_FOLDER, "CommonBin", "xperf", "xperf.exe")

PROGRAM_FILES_PATH = os.path.join(os.environ['ProgramFiles'], "Intel", "Graphics")
GFX_TRACE_ETL_FILE = os.path.join(test_context.LOG_FOLDER, "GfxTrace.etl")
GFX_BOOT_TRACE_ETL_FILE = os.path.join(test_context.LOG_FOLDER, "GfxBootTrace.etl")
ANALYZER_LOG_FILE = os.path.join(test_context.LOG_FOLDER, "etl_analyzer_logs.txt")

LOGGER_DLL_PATH = os.path.join(test_context.BIN_FOLDER, 'Logger.dll')
PROVIDER_PATH = os.path.join("C:\\Program Files\\Intel\\Graphics")

TRACE_LOGGER = "GfxTrace"
BOOT_TRACE_LOGGER = "Intel-Gfx-BootTrace"

# This path is hard coded since the same path is hard coded in Registry file
BOOT_TRACE_ETL = os.path.join("C:", "Windows", "System32", "LogFiles", "WMI", "GfxBootTrace.etl")


##
# @brief        Enum definition for tracing option information
class TraceType(enum.Enum):
    TRACE_ALL = f"{XPERF_EXE} -start {TRACE_LOGGER} -on Intel-Gfx-Driver+Intel-Gfx-Display-External+" \
                f"Intel-Gfx-Driver-Display+Intel-Gfx-Display-ValSim-Driver+DisplayAutomation-Test+" \
                f"Intel-Gfx-Control-Library -BufferSize 1024 -MinBuffers 64 -MaxBuffers 128"
    TRACE_LITE = f"{XPERF_EXE} -start {TRACE_LOGGER} -on Intel-Gfx-Driver:0x0:0x01:0x01+" \
                 f"Intel-Gfx-Driver-Display+Intel-Gfx-Display-External+Intel-Gfx-Display-ValSim-Driver+" \
                  f"DisplayAutomation-Test+Intel-Gfx-Control-Library"
    DDI_TRACE = f"{XPERF_EXE} -start {TRACE_LOGGER} -on Intel-Gfx-Driver:0x01:0x04:0x01" \
                f"+Intel-Gfx-Display-ValSim-Driver+DisplayAutomation-Test+Intel-Gfx-Control-Library"
    DXGKRNL_TRACE = f"{XPERF_EXE} -start {TRACE_LOGGER} -on Intel-Gfx-Driver+Intel-Gfx-Driver-Display+" \
                    f"Intel-Gfx-Display-External+Microsoft-Windows-DxgKrnl:0x01+Intel-Gfx-Display-ValSim-Driver+" \
                     f"DisplayAutomation-Test+Intel-Gfx-Control-Library -BufferSize 1024"
    TRACE_WITH_BOOT = f"reg import {CUSTOM_TRACER_PATH}\\Reg\\GfxBootTraceStart.reg"
    TRACE_PC_ONLY = f"{XPERF_EXE} -start {TRACE_LOGGER} -on Intel-Gfx-Driver:0x8:0x05+" \
                    f"Intel-Gfx-Driver-Display:0x800:0x05 -BufferSize 1024 -MinBuffers 64 -MaxBuffers 128"
    TRACE_WITH_BOOT_PC_ONLY = f"reg import {CUSTOM_TRACER_PATH}\\Reg\\GfxPcBootTrace.reg"


##
# @brief        The Register Trace Scripts
# @return       status - ETL tracer registration status
def _register_trace_scripts():
    # GfxDriver ETL trace setup
    logging.debug("Registering ETL Tracer.")
    install_cmd = os.path.join(TRACER_PATH, "install.bat")
    status = __run_command(install_cmd, cwd=TRACER_PATH)
    # Run this command after Install.bat, Otherwise File will be removed by Install.bat
    shutil.copy2(LOGGER_DLL_PATH, PROVIDER_PATH)

    # Test ETL trace setup
    reg_file = os.path.join(CUSTOM_TRACER_PATH, "Reg", "EventRegistration_test_guid.reg")
    reg_merger = f"reg import {reg_file}"
    status &= __run_command(reg_merger)

    if status is False:
        logging.error("Failed to register ETL Tracer.")
        gdhm.report_bug(
            "[EtlTracerLib] Failed to register ETL Tracer",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
    else:
        logging.debug("Successfully Registered Trace scripts.")
    return status


##
# @brief        ETL trace teardown
# @return       status - ETL tracer un-registration status
def _unregister_trace_scripts():
    status = True
    logging.info("Unregistering ETL Tracer.")
    reg_file = os.path.join(TRACER_PATH, "Reg", "EventsUnRegistration.reg")
    reg_merger = f"reg import {reg_file}"
    status = __run_command(reg_merger)

    reg_file = os.path.join(CUSTOM_TRACER_PATH, "Reg", "EventUnRegistration_test_guid.reg")
    reg_merger = f"reg import {reg_file}"
    status &= __run_command(reg_merger)

    boot_reg_path = os.path.join(CUSTOM_TRACER_PATH, "Reg", "GfxBootTraceStop.reg")
    stop_boot_trace_cmd = f"reg import {boot_reg_path}"
    status &= __run_command(stop_boot_trace_cmd)

    if status is False:
        logging.error("Failed to unregister ETL Tracer.")
        gdhm.report_bug(
            "[EtlTracerLib] Failed to unregister ETL Tracer",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
    else:
        # Removing existing events
        if os.path.exists(PROGRAM_FILES_PATH):
            shutil.rmtree(PROGRAM_FILES_PATH)
        logging.debug("Unregistration of Trace Scripts Completed")
    return status


##
# @brief        This API starts ETL tracing. In case of TRACE_WITH_BOOT, it is caller's responsibility to invoke
#               reboot event.
# @param[in]    tracing_options - tracing level, default is TRACE_ALL
# @return       status - True if operation is successful, False otherwise
def start_etl_tracer(tracing_options=TraceType.TRACE_ALL):
    if __is_tracer_running(TRACE_LOGGER) or __is_tracer_running(BOOT_TRACE_LOGGER):
        logging.info(f"ETL Tracer already started, skipping {tracing_options.name}.")
        return True

    if os.path.exists(BOOT_TRACE_ETL):
        os.remove(BOOT_TRACE_ETL)

    status = __run_command(tracing_options.value)

    if status is False:
        logging.error("Failed to start ETL Tracer.")
        gdhm.report_bug(
            "[EtlTracerLib] Failed to start ETL Tracer",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
    else:
        logging.info(f"ETL Tracing Started with {tracing_options.name}")

    return status


##
# @brief        This API stops ETL tracing.
# @return       status - True if operation is successful, False if fails. None in case of exception.
def stop_etl_tracer():
    status = True

    if __is_tracer_running(BOOT_TRACE_LOGGER):
        logging.info("Stopping Boot ETL Tracer.")
        xperf_command = f"{XPERF_EXE} -stop {BOOT_TRACE_LOGGER} -d {GFX_BOOT_TRACE_ETL_FILE}"
        status &= __run_command(xperf_command)

    if __is_tracer_running(TRACE_LOGGER):
        logging.info("Stopping ETL Tracer.")
        xperf_command = f"{XPERF_EXE} -stop {TRACE_LOGGER} -d {GFX_TRACE_ETL_FILE}"
        status = __run_command(xperf_command)

    if status:
        logging.info("ETL Tracer Stopped Successfully")
    else:
        logging.error("Failed to stop ETL Tracer.")
        gdhm.report_bug(
            "[EtlTracerLib] Failed to stop ETL Tracer",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
    return status


##
# @brief        To check if tracer is running
# @param[in]    trace_instance - The instance of the tracer to check its running status
# @return       bool - True if tracer is running, False otherwise
def __is_tracer_running(trace_instance):
    command = f"{XPERF_EXE} -loggers {trace_instance}"

    output = run(command, capture_output=True)
    std_out = re.compile(r'[\r\n]').sub(" ", output.stdout.decode())
    std_err = re.compile(r'[\r\n]').sub(" ", output.stderr.decode())
    if output.returncode != 0:
        logging.error(f"Failed to run: {command}. returncode: {output.returncode}")
        logging.error(f"Stdout: {std_out}, Stderr:{std_err}")
    else:
        if "No Selected Active Loggers" not in std_out:
            return True
    return False


##
# @brief        Run Command
# @param[in]    command - The run command
# @param[in]    cwd - Current Working directory
# @return       bool - True if Output return code is 0, else False
def __run_command(command, cwd=None):
    output = run(command, cwd=cwd, capture_output=True)
    if output.returncode != 0:
        logging.error(f"Failed to run: {command}. returncode: {output.returncode}")
        std_out = re.compile(r'[\r\n]').sub(" ", output.stdout.decode())
        std_err = re.compile(r'[\r\n]').sub(" ", output.stderr.decode())
        logging.error(f"Stdout: {std_out}, Stderr:{std_err}")
        return False
    else:
        return True
