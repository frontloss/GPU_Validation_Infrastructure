########################################################################################################################
# @file         apply_display_config.py
# @brief        Python module to apply display configuration for connected displays
# @details      Applies provided display configuration from command line and invokes IGCL and DD Escape to fetch mode
#               table for active displays
#               Example:
#                   python TestUtilities\apply_display_config.py -gfx_0 -HDMI_B -DP_C -CONFIG CLONE
#                   python TestUtilities\apply_display_config.py -gfx_1 -EDP_A -CONFIG SINGLE
# @author       Kiran Kumar Lakshmanan
########################################################################################################################
import ctypes
import logging
import sys
import unittest

# Do not remove this import as it will be used by eval function to evaluate config enums
from Libs.Core import test_header, cmd_parser, enum
from Libs.Core.display_config import display_config, display_config_enums as cfg_enum
from Libs.Core.display_config import display_config_struct, adapter_info_struct
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import display_logger, etl_tracer
from Libs.Core.logger import html
from Libs.Core.test_env import test_environment, test_context
from Libs.Core.wrapper import control_api_args, control_api_wrapper


##
# @brief        Initialize function
# @return       None
@html.step("Script initialize")
def __initialize() -> None:
    test_environment.TestEnvironment.load_dll_module()

    display_logger._initialize(console_logging=True)

    control_api_wrapper.configure_control_api(flag=True)
    etl_tracer._register_trace_scripts()
    etl_tracer.start_etl_tracer()
    test_header.initialize(sys.argv)

    gta_state_manager.create_gta_default_state()


##
# @brief        Cleanup function
# @return       None
@html.step("Script cleanup")
def __cleanup(test_outcome: unittest.TestProgram) -> None:
    control_api_wrapper.configure_control_api(flag=False)
    etl_tracer.stop_etl_tracer()
    etl_tracer._unregister_trace_scripts()

    test_environment.TestEnvironment.log_test_result(test_outcome.result)
    # Always collect ETL and other logs
    test_environment.TestEnvironment.store_cleanup_logs(False)
    display_logger._cleanup()


##
# @brief        ApplyDisplayConfig  class
class ApplyDisplayConfig(unittest.TestCase):

    ##
    # @brief        This function parses the commandline and performs actions based on plug/unplug argument from cmdline
    # @return       None
    @html.step("PreTest: Command Line validation")
    def verify_cmdline(self) -> None:
        if len(sys.argv) <= 2:
            # <>: mandatory arguments, []: optional arguments
            logging.info(
                f"Usage: python apply_display_config.py <-gfx_index> <-HDMI_/-DP_> <-CONFIG <>>")
            logging.info("\tExample 1 python apply_display_config.py -gfx_0 -HDMI_B -DP_C -CONFIG CLONE")
            logging.info("\tExample 2 python apply_display_config.py -gfx_1 -DP_D_TC -CONFIG SINGLE")
            logging.info("\tExample 3 python apply_display_config.py -gfx_0 -EDP_A -HDMI_C EXTENDED")
        else:
            gfx_index = None
            if sys.argv[1].lower().startswith("gfx_"):
                gfx_index = sys.argv[1].lower()
            custom_tags = cmd_parser.get_custom_tag()
            cmd_line_args = cmd_parser.parse_cmdline(sys.argv, custom_tags)

            if isinstance(cmd_line_args, dict):
                cmd_line_args = [cmd_line_args]

            self.gfx_index = "gfx_0" if gfx_index is None else gfx_index

            gfx_index_num = int(self.gfx_index[-1])

            for output in cmd_line_args:
                for key, val in output.items():
                    if cmd_parser.display_key_pattern.match(key) is None:
                        continue
                    self.display_list.append({key: val})

            if 'CONFIG' in cmd_line_args[gfx_index_num].keys():
                self.topology = eval("enum.%s" % cmd_line_args[gfx_index_num]['CONFIG'])

            logging.info(f"Displays = {self.display_list}")
            if len(self.display_list) == 0:
                self.fail("No Displays passed for applying configuration")

            if self.topology is None:
                self.fail("Failed to get topology")

    ##
    # @brief        RunTest method
    # @return       None
    def runTest(self) -> None:
        self.topology = None
        self.display_list: list = []

        # Validate if -plug/-unplug is passed in commandline
        self.verify_cmdline()

        display_config_ = display_config.DisplayConfiguration()
        display_adapter_info = []
        enumerated_displays = display_config_.get_enumerated_display_info()
        expected_displays = []
        for disp in self.display_list:
            keys = list(disp.keys())[0]
            port_name = "_".join(keys.split("_")[:2])
            if port_name.startswith("EDP"):
                port_name = port_name.replace("EDP", "DP")
            expected_displays.append(port_name)

        logging.info(f"topology = {self.topology} expected_displays = {expected_displays}")
        for i in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[i]
            if display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex == self.gfx_index.lower() and \
                    cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name in expected_displays:
                ret = display_config_.get_display_and_adapter_info_ex(cfg_enum.CONNECTOR_PORT_TYPE(
                    display_info.ConnectorNPortType).name, self.gfx_index)
                display_adapter_info.append(ret)

        logging.info(f"Display and Adapter Info List = ")
        for adapter in display_adapter_info:
            logging.info(f"\t{adapter}")
        status = display_config_.set_display_configuration_ex(self.topology, display_adapter_info)

        if status:
            # Loop through active displays to fetch mode information
            enum_displays = display_config_.get_enumerated_display_info()
            logging.info(f"Enumerated Displays: {enum_displays.to_string()}")
            for gfx_index, adapter in test_context.TestContext.get_gfx_adapter_details().items():
                self.__invoke_igcl_escape_for_mode_table(adapter, enum_displays)
            logging.info(f"{'*' * 200}")
            for i in range(enum_displays.Count):
                current_display = enum_displays.ConnectedDisplays[i]
                if current_display.IsActive is not True:
                    logging.info(f"Display inactive. Skipping print of DDEscape mode table for "
                                 f"{current_display.DisplayAndAdapterInfo.adapterInfo.gfxIndex}:"
                                 f"0x{current_display.DisplayAndAdapterInfo.TargetID:X}")
                    continue
                self.__invoke_dd_escape_for_mode_table(current_display.DisplayAndAdapterInfo, enum_displays)
        else:
            self.fail(f"Failed to apply config {self.topology} for displays - {expected_displays}")

    ##
    # @brief        Invoke DD Escape to get mode table
    # @param[in]    panel_info - DisplayAndAdapterInfo object
    # @param[in]    enumerated_displays - EnumeratedDisplays object
    # @return       None
    @staticmethod
    @html.step("DD Escape Mode Table details")
    def __invoke_dd_escape_for_mode_table(panel_info: display_config_struct.DisplayAndAdapterInfo,
                                          enumerated_displays: display_config_struct.EnumeratedDisplays) -> None:
        display_config_ = display_config.DisplayConfiguration()
        logging.info("Printing data from DD Escape")
        logging.info(f"Fetching Mode list for 0x{panel_info.TargetID:X} on {panel_info.adapterInfo.gfxIndex}")
        supported_modes = display_config_.get_all_supported_modes([panel_info], False)
        count = 0
        for key, mode in supported_modes.items():
            logging.info(f"Number of supported display modes - {len(mode)}")
            for m in mode:
                logging.debug(f"Mode[{count}] 0x{key:X}: {m.to_string(enumerated_displays)}")
                count += 1

    ##
    # @brief        Invoke IGCL Escape to get mode table
    # @param[in]    adapter_info - GfxAdapterInfo object
    # @param[in]    enumerated_displays - EnumeratedDisplays object
    # @return       None
    @staticmethod
    @html.step("IGCL Escape Mode Table details")
    def __invoke_igcl_escape_for_mode_table(adapter_info: adapter_info_struct.GfxAdapterInfo,
                                            enumerated_displays: display_config_struct.EnumeratedDisplays) -> None:
        display_config_ = display_config.DisplayConfiguration()
        logging.info("Printing data from IGCL Escape")
        args = control_api_args.ctl_genlock_args_t()
        args.Size = ctypes.sizeof(args)
        args.Version = 0  # dummy value
        args.GenlockTopology.IsPrimaryGenlockSystem = True
        args.Operation = control_api_args.ctl_genlock_operation_v.GET_TIMING_DETAILS
        logging.info(f"Fetching Mode list for displays on Adapter:{adapter_info.gfxIndex}")
        status = control_api_wrapper.display_genlock_get_all_displays_timings(args, adapter_info)
        if status is True:
            logging.info(f"CAPI result = {status}")
            # @todo: Keeping this loop for time being. To be handled per targetID as part of phase 2 change
            try:
                for i in range(enumerated_displays.Count):
                    disp_info = enumerated_displays.ConnectedDisplays[i]
                    if disp_info.IsActive is not True:
                        logging.info(f"Display inactive. Skipping print of IGCL mode table for "
                                     f"{disp_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex}:"
                                     f"0x{disp_info.DisplayAndAdapterInfo.TargetID:X}")
                        continue
                    logging.info(f"Dumping Mode list for target: 0x{disp_info.DisplayAndAdapterInfo.TargetID:X}")
                    logging.info(f"Number of supported Genlock displays - {args.GenlockTopology.NumGenlockDisplays}")
                    modes = args.GenlockTopology.pGenlockModeList[i]
                    logging.info(f"Supported display modes - {modes.NumModes}")
                    logging.info(f"Handle for Display[{i}]: {modes.hDisplayOutput}")

                    result, handle = control_api_wrapper.get_target_display_handle(disp_info.DisplayAndAdapterInfo)
                    if result is True:
                        logging.info(f"Current display handle = {handle}")
                        if handle != modes.hDisplayOutput:
                            logging.warning("Could not map display handle for given panel with Genlock args")
                            continue

                    for m in range(modes.NumModes):
                        mode = modes.pTargetModes[m]
                        logging.info(f"Mode ({m}): {mode}")
                        logging.info(f"Applying Display Mode : {mode}")
                        status = display_config_.set_higher_pixel_clock_mode(disp_info.DisplayAndAdapterInfo, mode)
                        logging.info(f"Mode Set Status : {'PASSED' if status is True else 'FAILED'}")
            except Exception as ex:
                logging.error(f"[Can be ignored if genlock display count is 0] Exception occurred: {ex}")
        else:
            logging.error(f"CAPI result = {status}")


if __name__ == '__main__':
    __initialize()
    outcome = unittest.main(verbosity=2, argv=[sys.argv[0]], exit=False)
    __cleanup(outcome)
