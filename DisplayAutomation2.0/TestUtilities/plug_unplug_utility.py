########################################################################################################################
# @file         plug_unplug_utility.py
# @brief        Python module to perform plug and unplug displays for simulation
# @details      Always pass the -plug/-unplug as 2nd argument to the test followed by display and their respective EDID
#               and DPCD. Pass the displays to be plugged/unplugged prefixed with hyphen such as -DP_B -HDMI_C in
#               commandline. Verification of display enumeration is not done within this script. For this, make use of
#               the enumerated_displays data logged before and after running the test.
#               Example:
#                   python TestUtilities\plug_unplug_utility.py -plug -gfx_0 -HDMI_B -DP_C
#                   python TestUtilities\plug_unplug_utility.py -plug -gfx_0 -DP_D_TC -gfx_1 -DP_A
# @author       Kiran Kumar Lakshmanan
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import cmd_parser, display_utility, test_header, gfx_assistant
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import etl_tracer, display_logger
from Libs.Core.logger import html
from Libs.Core.sw_sim import valsim_setup, driver_interface
from Libs.Core.test_env import test_environment
from Libs.Core.test_env.test_context import TestContext

supported_ports = ["DP_", "HDMI_"]


##
# @brief        Initialize function
# @return       None
@html.step("Script initialize")
def __initialize() -> None:
    test_environment.TestEnvironment.load_dll_module()

    display_logger._initialize(console_logging=True)
    valsim_setup.verify_sim_drv_status()

    etl_tracer._register_trace_scripts()
    etl_tracer.start_etl_tracer()
    test_header.initialize(sys.argv)

    driver_interface.DriverInterface().init_driver_interface()
    driver_interface.DriverInterface().initialize_all_efp_ports()

    gta_state_manager.create_gta_default_state()


##
# @brief        Cleanup function
# @return       None
@html.step("Script cleanup")
def __cleanup(test_outcome: unittest.TestProgram) -> None:
    etl_tracer.stop_etl_tracer()
    etl_tracer._unregister_trace_scripts()
    status = test_environment.TestEnvironment.log_test_result(test_outcome.result)
    test_environment.TestEnvironment.store_cleanup_logs(status)
    display_logger._cleanup()


##
# @brief        PlugUtility class
class PlugUtility(unittest.TestCase):

    ##
    # @brief        This function parses the commandline and performs actions based on plug/unplug argument from cmdline
    # @return       None
    @html.step("PreTest: Command Line validation")
    def verify_cmdline(self) -> None:
        if len(sys.argv) <= 2:
            # <>: mandatory arguments, []: optional arguments
            logging.info(
                f"Usage: python plug_unplug_utility.py <-plug/-unplug> [-gfx_index] <-HDMI_/-DP_> [EDID] [DPCD]")
            logging.info("Example 1 (Plug in gfx_0): python plug_unplug_utility.py -plug -HDMI_B -DP_C")
            logging.info("Example 2 (Plug in MA): python plug_unplug_utility.py -plug -gfx_0 -DP_D_TC -gfx_1 -DP_A")
            logging.info(
                "Example 3 (Plug in gfx_0 with EDID/DPCD): python plug_unplug_utility.py -plug "
                "-DP_B Acer_CB240HYK_DP.bin Acer_CB240HYK_DPCD.txt -HDMI_C Acer_CB240HYK_HDMI.bin")
            logging.error("Example 4 (Unplug in gfx_0): python plug_unplug_utility.py -unplug -HDMI_B -DP_D")
            logging.error("Example 5 (Unplug in MA): python plug_unplug_utility.py -unplug -gfx_0 -DP_D -gfx_1 -DP_A")
            self.fail("Invalid commandline passed.")
        else:
            if sys.argv[1].lower() in ["-plug", "-unplug"]:
                self.action = sys.argv[1].replace("-", "").lower()
                custom_tags = cmd_parser.get_custom_tag()
                cmd_line_args = cmd_parser.parse_cmdline(sys.argv, custom_tags)

                if isinstance(cmd_line_args, dict):
                    cmd_line_args = [cmd_line_args]

                for output in cmd_line_args:
                    for key, val in output.items():
                        for port_type in supported_ports:
                            if port_type in key.upper():
                                self.display_list.append({key: val})

                logging.info(f"Generated Display list to be {self.action}ged : {self.display_list}")
                if len(self.display_list) == 0:
                    self.fail("No Displays passed to be simulated")
            else:
                self.fail(f"Invalid commandline. Pass the action to be performed '-plug'/'-unplug'")

    def runTest(self):
        self.display_list: list = []
        self.action: str = ""
        display_config_ = display_config.DisplayConfiguration()

        for i, o in enumerate(sys.argv):
            if o.lower() == "-gas_id":
                gfx_assistant.add_simulation_files(TestContext.panel_input_data(), sys.argv[i + 1])
                break

        # Validate if -plug/-unplug is passed in commandline
        self.verify_cmdline()

        logging.info(f"{'=' * 150}")
        enum_displays = display_config_.get_enumerated_display_info()
        logging.info(f"Initial Enum Displays: {enum_displays.to_string()}")
        logging.info(f"{'=' * 150}")

        if self.action == "plug":
            self.plug_displays()
        elif self.action == "unplug":
            self.unplug_displays()

        logging.info(f"{'=' * 150}")
        enum_displays = display_config_.get_enumerated_display_info()
        logging.info(f"Enumerated Displays: {enum_displays.to_string()}")
        logging.info(f"{'=' * 150}")

    ##
    # @brief        This function plugs the displays provided in the commandline
    # @return       None
    @html.step("Plug Displays")
    def plug_displays(self) -> None:
        for display in self.display_list:
            for key, val in display.items():
                port = val["connector_port"]
                edid = val["edid_name"]
                dpcd = val["dpcd_name"]
                panel_index = val["panel_index"]
                gfx_index = val["gfx_index"].lower()
                connector_port_type = val["connector_port_type"]
                is_lfp = val["is_lfp"]

                # Skip LFPs passed
                if connector_port_type == "EMBEDDED" or is_lfp is True:
                    logging.warning("This script doesn't support LFP plug!!")
                    continue

                # unplug existing displays on that port
                if self.is_display_enumerated(port_name=port, display=val):
                    logging.info(f"Unplugging connected display on port {port}")
                    unplug_status = display_utility.unplug(port, port_type=connector_port_type, is_lfp=False,
                                                           gfx_index=gfx_index)
                    logging.info(f"Unplug status for {gfx_index}:{port}={unplug_status}")

                # perform plug for EFPs only
                if panel_index is not None and panel_index != "":
                    logging.info(f"Display Plug on {port} with PanelIndex:{panel_index}")
                    result = display_utility.plug(gfx_index=gfx_index, port=port, panelindex=panel_index,
                                                  port_type=connector_port_type)
                    logging.info(f"{'PASS' if result else 'FAIL'}: Plug of {gfx_index}:{port} with PanelIndex")
                elif edid is None or edid == "":
                    logging.warning("No EDID passed to plug display, using default EDID/DPCD for current platform")
                    result = display_utility.plug(gfx_index=gfx_index, port=port, port_type=connector_port_type)
                    logging.info(f"{'PASS' if result else 'FAIL'}: Plug of {gfx_index}:{port} with DEFAULT EDID/DPCD")
                else:
                    logging.info(f"Display Plug on {port} with EDID:{edid}, DPCD:{dpcd}")
                    result = display_utility.plug(gfx_index=gfx_index, port=port, edid=edid, dpcd=dpcd,
                                                  port_type=connector_port_type)
                    logging.info(f"{'PASS' if result else 'FAIL'}: Plug of {gfx_index}:{port} with EDID/DPCD")

                assert result, f"Failed to plug display on {gfx_index}:{port}"

    ##
    # @brief        This function unplugs the displays provided in the commandline
    # @return       None
    @html.step("Unplug Displays")
    def unplug_displays(self) -> None:
        for display in self.display_list:
            for key, val in display.items():
                port = val["connector_port"]
                gfx_index = val["gfx_index"].lower()
                connector_port_type = val["connector_port_type"]
                if self.is_display_enumerated(port_name=port, display=val):
                    logging.info(f"Unplugging display: ({port}, {connector_port_type}) on gfx ({gfx_index})")
                    result = display_utility.unplug(gfx_index=gfx_index, port=port, port_type=connector_port_type)
                    logging.info(f"{'PASS' if result else 'FAIL'}: Unplug of {gfx_index}:{port}")
                    assert result, f"Failed to unplug display from {gfx_index}:{port}"
                else:
                    logging.error(f"No display is present to be unplugged from port ({port})")

    ##
    # @brief        This function checks if the display to be plugged/unplugged is enumerated or not
    # @param[in]    port_name represents port which has to be plugged
    # @param[in]    display represents the parsed display information from commandline for current port_name
    # @return       Boolean: True if display is present, False if display is not present
    @staticmethod
    @html.step("Enumerated Displays")
    def is_display_enumerated(port_name: str, display: dict) -> bool:
        status = False
        display_config_ = display_config.DisplayConfiguration()
        enum_displays = display_config_.get_enumerated_display_info()
        logging.info(f"Verifying Enum Displays: {enum_displays.to_string()}")
        for i in range(enum_displays.Count):
            current_display = enum_displays.ConnectedDisplays[i]
            if current_display.DisplayAndAdapterInfo.adapterInfo.gfxIndex.lower() == display["gfx_index"].lower() and \
                    cfg_enum.CONNECTOR_PORT_TYPE(current_display.ConnectorNPortType).name == port_name:
                status = True
                logging.info(f"Current Display {display} is Enumerated as {display['connector_port_type']}.")
                break
        return status


if __name__ == '__main__':
    __initialize()
    outcome = unittest.main(verbosity=2, argv=[sys.argv[0]], exit=False)
    __cleanup(outcome)
