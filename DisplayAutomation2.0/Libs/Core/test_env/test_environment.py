########################################################################################################################
# @file         test_environment.py
# @brief        Contains APIs for test environment setup and cleanup
# @author       Amit Sau, Praburaj Krishnan, Kumar, Rohit
########################################################################################################################

import logging
import os
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime
from types import TracebackType
from unittest import TestResult

from Libs import env_settings
from Libs.Core import display_utility, reboot_helper, driver_escape
from Libs.Core import test_header
from Libs.Core.Verifier import common_verification
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.gta import gta_state_manager, bullseye_manager
from Libs.Core.logger import display_logger, html, gdhm
from Libs.Core.logger import etl_tracer
from Libs.Core.sw_sim import driver_interface
from Libs.Core.sw_sim import valsim_setup
from Libs.Core.test_env import state_machine_manager, verification_manager
from Libs.Core.test_env import test_context
from Libs.Core.vbt import vbt
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import dll_logger, cui_sdk_wrapper
from Libs.Core.wrapper import driver_escape_wrapper
from Libs.Core.wrapper import os_interfaces as os_interfaces_dll
from Libs.Core.wrapper import valsim_wrapper

traces_file_name = "Traces.7z"



##
# @brief        Test Environment
class TestEnvironment:

    ##
    # @brief        Initializes the test environment
    # @return       None
    @staticmethod
    def initialize() -> None:

        # Register global exception handler hook
        sys.excepthook = TestEnvironment.__global_exception_handler

        state_machine_manager.StateMachine().test_phase = state_machine_manager.TestPhase.SETUP

        TestEnvironment.load_dll_module()

        display_logger._initialize(console_logging=True)

        test_header.initialize(sys.argv)

        verification_manager.initialize()

        # Configure DLL modules
        cui_sdk_wrapper.configure_sdk(flag=True)
        control_api_wrapper.configure_control_api(flag=True)

        valsim_setup.verify_sim_drv_status()

        driver_interface.DriverInterface().init_driver_interface()

        # Check if gfx driver is running before test execution
        driver_status, valsim_status = driver_interface.DriverInterface().verify_graphics_driver_status()
        if driver_status is False:
            gdhm.report_bug(
                f"[TestEnvironment] Intel Graphics Driver is not running",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P1,
                gdhm.Exposure.E1
            )
            logging.error("Gfx driver(s) is not running during initialization")
        if valsim_status is False:
            gdhm.report_bug(
                f"[TestEnvironment] GfxValsim is not running",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P1,
                gdhm.Exposure.E1
            )
            logging.error("GfxValsim is not running during initialization")

        # Get graphics adapter details from test_context
        test_context.TestContext.get_gfx_adapter_details()

        if reboot_helper.is_reboot_scenario() is False:
            etl_tracer._register_trace_scripts()
            etl_tracer.start_etl_tracer()

            # test_header.initialize() overwrites the .log file with system info. All the logs getting logged before
            # this line will be overwritten. Keeping the step_start() here to avoid this.
            html.step_start("Test Environment Initialization")

            state_machine_manager.StateMachine().init_adapters_context()

            # initialize for common verification (under-run, TDR, Bspec violation)
            common_verification.initialize()

            gta_state_manager.create_gta_default_state()
            bullseye_manager.setup()
        else:
            html.step_start("Test Environment Initialization after reboot")
            common_verification.update_verifier_cfg()
            state_machine_manager.StateMachine().update_adapter_display_context()

        TestEnvironment.__configure_all_adapters_power_component(True)
        driver_interface.DriverInterface().initialize_all_efp_ports()
        TestEnvironment.__cleanup_simulated_emulated_display()
        html.step_end()
        state_machine_manager.StateMachine().test_phase = state_machine_manager.TestPhase.TEST

    ##
    # @brief        Cleanup Function
    # @param[in]    result - TestResult Object
    # @return       None
    @staticmethod
    @html.step("Test Environment Cleanup")
    def cleanup(result: TestResult) -> None:
        state_machine_manager.StateMachine().test_phase = state_machine_manager.TestPhase.TEARDOWN
        if reboot_helper.is_reboot_scenario() is True:
            return

        verification_manager.cleanup_test_config()

        TestEnvironment.__cleanup_simulated_emulated_display()
        TestEnvironment.__configure_all_adapters_power_component(False)

        etl_tracer.stop_etl_tracer()
        etl_tracer._unregister_trace_scripts()
        common_verification.verify(result)

        status = TestEnvironment.log_test_result(result)
        TestEnvironment.__dump_vbt_data()
        TestEnvironment.store_cleanup_logs(status)
        bullseye_manager.cleanup()
        common_verification.cleanup()
        TestEnvironment.__cleanup_dll_module()
        gta_state_manager.configure_tc(launch=True)  # Launch ThinClient at the end during cleanup


    ##
    # @brief        Compiles test result data
    # @param[in]    error_type - Test error type
    # @param[in]    error_list - Test result object based on test status
    # @return       result_str - Formatted test result string
    @staticmethod
    def __process_test_errors(error_type: str, error_list: list) -> str:
        idx = 1
        result_str = ""
        for test_result in error_list:
            item_count = 1
            test_name, test_error = test_result
            result_str += "\n\n"
            result_str += test_header.formatted_line_separator('=', test_header.DEFAULT_LINE_WIDTH)
            result_str += test_header.format_line(("%s %d : %s" % (error_type, idx, str(test_name))),
                                                  test_header.DEFAULT_LINE_WIDTH)
            result_str += test_header.formatted_line_separator('-', test_header.DEFAULT_LINE_WIDTH)
            result_str += test_header.format_line("%s" % test_error, test_header.DEFAULT_LINE_WIDTH)
            result_str += test_header.formatted_line_separator('-', test_header.DEFAULT_LINE_WIDTH)
            idx += 1
        return result_str



    ##
    # @brief        Obtain test execution time
    # @return       diff - Total execution time for test
    @staticmethod
    def __get_test_execution_time() -> str:
        file_handle, log_file_path = display_logger._get_file_handle()

        # Format in which the time will be manipulated.
        time_format = '%H:%M:%S'
        # Gets the file creation time as timestamp
        file_creation_time_stamp = os.path.getctime(log_file_path)

        # Converts timestamp to datetime and then converts the datetime to required time format.
        start_time = datetime.fromtimestamp(file_creation_time_stamp).strftime(time_format)
        start_time = datetime.strptime(start_time, time_format)

        # Gets the current time and converts to required time format.
        end_time = datetime.now().time().strftime(time_format)
        end_time = datetime.strptime(end_time, time_format)

        diff = end_time - start_time
        return diff

    ##
    # @brief        Parse Unittest Result object and log test result summary
    # @param[in]    result - TestResult object
    # @return       bool - True if no test failures found, False otherwise
    @staticmethod
    def log_test_result(result: TestResult) -> bool:
        test_count = result.testsRun
        fail_count = len(result.failures)
        error_count = len(result.errors)
        skip_count = len(result.skipped)
        pass_count = test_count - fail_count - error_count - skip_count

        test_errors = ""
        if skip_count:
            test_errors += TestEnvironment.__process_test_errors("SKIPPED TEST", result.skipped)
        if fail_count:
            test_errors += TestEnvironment.__process_test_errors("FAILED TEST", result.failures)
        if error_count:
            test_errors += TestEnvironment.__process_test_errors("ERORRED TEST", result.errors)

        test_summary = "Ran %d tests : Passed = %d, Failed = %d, Errored = %d and Skipped = %d" % (
            test_count, pass_count, fail_count, error_count, skip_count)
        test_result = test_header.format_line(test_summary.center(test_header.DEFAULT_LINE_WIDTH, ' '),
                                              test_header.DEFAULT_LINE_WIDTH)
        failures = fail_count + error_count

        if failures:
            test_result += test_header.format_line("Test Result: FAILED".center(test_header.DEFAULT_LINE_WIDTH, ' '),
                                                   test_header.DEFAULT_LINE_WIDTH)
        else:
            test_result += test_header.format_line("Test Result: PASSED".center(test_header.DEFAULT_LINE_WIDTH, ' '),
                                                   test_header.DEFAULT_LINE_WIDTH)

        msg = "Execution Time: {}".format(TestEnvironment.__get_test_execution_time())
        test_result += test_header.format_line(msg.center(
            test_header.DEFAULT_LINE_WIDTH, ' '), test_header.DEFAULT_LINE_WIDTH)

        test_report = "\n\n"
        test_report += test_header.formatted_line_separator()
        test_report += test_header.format_line("TEST SCRIPT EXECUTION END".center(test_header.DEFAULT_LINE_WIDTH, ' '))
        test_report += test_header.formatted_line_separator()

        test_report = "\n\n"
        test_report += test_header.formatted_line_separator('=', test_header.DEFAULT_LINE_WIDTH)
        test_report += test_header.format_line(
            "ANALYSE TEST RESULTS - START".center(test_header.DEFAULT_LINE_WIDTH, ' '))
        test_report += test_header.formatted_line_separator('=', test_header.DEFAULT_LINE_WIDTH)
        test_report += test_errors
        test_report += test_header.formatted_line_separator('=', test_header.DEFAULT_LINE_WIDTH)
        test_report += test_result
        test_report += test_header.format_line("ANALYSE TEST RESULTS - END".center(test_header.DEFAULT_LINE_WIDTH, '='))

        logging.info(test_report)
        status = True if failures == 0 else False
        try:
            path, file_name = os.path.split(sys.argv[0])
            log_file_name = file_name.replace('.py', '.log')
            log_file = os.path.join(test_context.LOG_FOLDER, log_file_name)
            html.process_logs(log_file, status)
        except Exception as e:
            logging.error(e)
        gta_state_manager.update_test_result(result, status)
        return status

    ##
    # @brief        To store cleanup logs
    # @param[in]    clear_logs - True if test failures are not observed, False otherwise
    # @return       None
    @staticmethod
    def store_cleanup_logs(clear_logs: bool) -> None:
        gdhm.copy_gdhm_logs()
        if not clear_logs:
            try:
                TestEnvironment.__copy_setupapi_logs()
                TestEnvironment.__dump_current_execution_states()
            except Exception as e:
                logging.error("Exception in test cleanup: {0}".format(e))
        if logging.getLogger().getEffectiveLevel() != logging.DEBUG and clear_logs and test_context.DiagnosticDetails().save_etl is False:
            for etl_file_name in os.listdir(test_context.LOG_FOLDER):
                if etl_file_name.endswith('.etl'):
                    os.remove(os.path.join(test_context.LOG_FOLDER, etl_file_name))
        TestEnvironment.__compress_trace_files(traces_file_name)

    ##
    # @brief        Cleanup method to handle exception causing scenario
    # @return       None
    @staticmethod
    @html.step("Post Processing")
    def __post_processing() -> None:
        state_machine_manager.StateMachine().test_phase = state_machine_manager.TestPhase.TEARDOWN
        verification_manager.cleanup_test_config()

        gta_state_manager.configure_tc(launch=True)  # Launching ThinClient ensuring gta communicates target

        TestEnvironment.__cleanup_simulated_emulated_display()
        TestEnvironment.__configure_all_adapters_power_component(False)
        result = TestResult()

        etl_tracer.stop_etl_tracer()
        etl_tracer._unregister_trace_scripts()
        common_verification.verify(result)

        result.errors.append((sys.argv[0], "Exception(s) occurred during test execution."))
        failures = TestEnvironment.log_test_result(result)
        TestEnvironment.store_cleanup_logs(failures)
        bullseye_manager.cleanup()
        common_verification.cleanup()
        TestEnvironment.__cleanup_dll_module()

    ##
    # @brief        Global Exception Handler
    # @param[in]    exception_type - exception category
    # @param[in]    value - Exception message
    # @param[in]    tb - traceback info
    # @return       None
    @staticmethod
    def __global_exception_handler(exception_type, value: str, tb: TracebackType) -> None:
        logging.error(value)
        logging.error(''.join(traceback.format_tb(tb)))
        logging.info(f"{'*' * 25} Exception Cleanup Start {'*' * 25}")
        TestEnvironment.__post_processing()
        logging.info(f"{'*' * 25} Exception Cleanup End {'*' * 25}")

    ##
    # @brief        Unplugs the stale external displays by using TestContext
    # @return       None
    @staticmethod
    def __cleanup_simulated_emulated_display() -> None:

        is_reboot_scenario = reboot_helper.is_reboot_scenario()
        simulation_type = env_settings.get('SIMULATION', 'simulation_type')

        if simulation_type not in ['NONE'] and is_reboot_scenario is False:
            enumerated_displays = display_config.DisplayConfiguration().get_enumerated_display_info()
            for count in range(enumerated_displays.Count):
                connector_port = CONNECTOR_PORT_TYPE(
                    enumerated_displays.ConnectedDisplays[count].ConnectorNPortType).name
                gfx_index = enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                port_type = enumerated_displays.ConnectedDisplays[count].PortType
                if display_utility.get_vbt_panel_type(connector_port, gfx_index) not in \
                        [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI] and \
                        connector_port not in ['DispNone', 'VIRTUALDISPLAY'] and \
                        enumerated_displays.ConnectedDisplays[count].FriendlyDeviceName != "Raritan CIM":
                    if display_utility.unplug(connector_port, port_type=port_type, gfx_index=gfx_index) is False:
                        logging.error(f"Unplug of {connector_port} Failed")
                    else:
                        logging.info(f"Unplug of {connector_port} is successful")

    ##
    # @brief        API to compress ETL Trace Files
    # @param[in]    file_name - Archive File name
    # @return       None
    @staticmethod
    def __compress_trace_files(file_name: str) -> None:
        exe_path = "C:\\Program Files\\7-Zip\\7z.exe"
        if not os.path.exists(exe_path):
            logging.error("{} doesn't exist.".format(exe_path))
            gdhm.report_bug(
                title=f"[TestEnvironment] Failed to compress trace files due to missing 7z asset.",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return

        files = [f for f in os.listdir(test_context.LOG_FOLDER) if f.endswith('.etl')]
        if len(files) > 0:
            disable_status = subprocess.call([exe_path, "a", file_name, "*.etl", "-sdel", "-mx=1"],
                                             cwd=test_context.LOG_FOLDER)
            if disable_status == 0:
                logging.debug("successfully compressed trace files.")
            else:
                logging.warning("Failed to compress trace files.")
                gdhm.report_bug(
                    title="[TestEnvironment] Failed to compress trace files",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )

    ##
    # @brief        API to load C-DLL Modules
    # @return       None
    @staticmethod
    def load_dll_module() -> None:
        dll_logger.load_library()
        # Initialize Os Interface wrapper
        os_interfaces_dll.load_library()
        # Initialize escape wrapper
        driver_escape_wrapper.load_library()
        # initialize cui sdk wrapper
        cui_sdk_wrapper.load_library()
        # Initialize valsim wrapper
        valsim_wrapper.load_library()
        # Initialize control api wrapper
        control_api_wrapper.load_library()

    ##
    # @brief        API to Cleanup DLL Modules
    # @return       None
    @staticmethod
    def __cleanup_dll_module() -> None:
        display_config.DisplayConfiguration().cleanup()
        cui_sdk_wrapper.configure_sdk(flag=False)
        control_api_wrapper.configure_control_api(flag=False)
        display_logger._cleanup()

    ##
    # @brief        Configure power component for all adapters
    # @param[in]    enable - True if Adapter to be configured is Active, False if Idle
    # @return       None
    @staticmethod
    def __configure_all_adapters_power_component(enable: bool) -> None:
        adapter_info_dict = test_context.TestContext.get_gfx_adapter_details()
        # Set power component to Active/Idle for all adapters before invoking power events
        for gfx_index in adapter_info_dict.keys():
            status = driver_escape.configure_adapter_power_component(gfx_index, enable)
            if status is None:
                logging.warning(f"Skipped for ({gfx_index}). Adapter LUID is 0")
            logging.info(
                f"{'PASS' if status is True else 'FAIL'}: Configuring {'Active' if enable else 'Idle'} status for {gfx_index} adapter")

    ##
    # @brief        Dump execution status details if test is failed in logs folder
    # @return       None
    @staticmethod
    def __dump_current_execution_states() -> None:
        cmdline_args = sys.argv
        log_folder_path = test_context.LOG_FOLDER
        path, file_name = os.path.split(cmdline_args[0])
        log_dat_file_name = file_name.replace('.py', '.dat')
        log_dmp_file_name = file_name.replace('.py', '.dmp')

        os.system("dispdiag -d")
        root_folder_path = test_context.ROOT_FOLDER
        file_list = [f for f in os.listdir(root_folder_path) if os.path.isfile(os.path.join(root_folder_path, f))]
        for file in file_list:
            if ".dat" in file:
                os.rename(file, log_dat_file_name)
                shutil.move(log_dat_file_name, log_folder_path)

            if ".dmp" in file:
                os.rename(file, log_dmp_file_name)
                shutil.move(log_dmp_file_name, log_folder_path)

    ##
    # @brief        Copy SetupAPI logs to Logs folder
    # @return       None
    @staticmethod
    def __copy_setupapi_logs() -> None:
        sr = os.environ.get('SystemRoot')
        if sr is None:
            logging.error("System root is None.")
        else:
            src_log_file = os.path.join(sr, "INF", "setupapi.dev.log")
            if os.path.exists(src_log_file):
                dest_log_file = os.path.join(test_context.LOG_FOLDER, "setupapi.dev" + str(time.time()) + ".log")
                shutil.copy2(src_log_file, dest_log_file)
            else:
                logging.info(f"{src_log_file} not found")

    ##
    # @brief        Dump VBT data
    # @return       None
    @staticmethod
    def __dump_vbt_data() -> None:
        try:
            path, file_name = os.path.split(sys.argv[0])

            # Gets the gfx adapter details from TestContext
            gfx_adapter_details_dict = test_context.TestContext.get_gfx_adapter_details()

            # Iterate through the list of gfx device and unplug the stale external displays if any for each gfx device.
            for gfx_index, gfx_adapter_info in gfx_adapter_details_dict.items():
                if len(gfx_index) == 0:
                    continue
                vbt_data = vbt.Vbt(gfx_index)

                # Create vbt file name using test name, vbr version and gfx_index
                file_name = file_name.replace('.py', '_vbt_dump_') + str(vbt_data.version) + '-' + gfx_index + '.bin'
                vbt_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
                vbt_data._dump(vbt_file_path)
        except Exception as e:
            logging.error(e)

