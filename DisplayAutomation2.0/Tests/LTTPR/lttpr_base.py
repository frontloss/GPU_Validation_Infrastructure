######################################################################################
# @file          lttpr_base.py
# @brief         It contains setUp, tearDown and helper methods for all LTTPR tests
#
# @author        Neha Kumari
######################################################################################

import logging
import sys
import unittest

from Libs.Core.logger import gdhm
from Libs.Core import cmd_parser, display_utility, enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import html


##
# @brief This class has the base functions like setUp, process_cmdline, parse_xml_and_plug, plug_display, compare_modes, tearDown functions
class LttprBase(unittest.TestCase):
    topology = None
    display_edid_dpcd = {}
    platform_dict = {}
    sku = ""
    display_config = DisplayConfiguration()
    system_utility = SystemUtility()
    machine_info = SystemInfo()

    ##
    # @brief  Unit-test setup function. Parse the command line and XML file, Plug EDID/DPCD.
    # @return None
    def setUp(self):
        self.pre_si = False

        logging.info("************** LTTPR VERIFICATION TEST START **************")

        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, None)

        gfx_display_hwinfo_list = self.machine_info.get_gfx_display_hardwareinfo()
        for gfx_display_hwinfo in gfx_display_hwinfo_list:
            self.platform_dict[gfx_display_hwinfo.gfxIndex] = gfx_display_hwinfo.DisplayAdapterName

        environment_type = self.system_utility.get_execution_environment_type()
        if environment_type in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            self.pre_si = True

        if type(self.cmd_line_param) is not list:
            self.cmd_line_param = [self.cmd_line_param]

        self.topology = eval(f"enum.{self.get_cmd_line_param_values('CONFIG')}")

        # get_sorted_display_list() will now always return a list of dictionaries for both SA and MA case
        # E.g [{'gfx_1': 'DP_F'}, {'gfx_1': 'DP_G'}, {'gfx_0': 'DP_C'}]
        self.cmd_line_displays = cmd_parser.get_sorted_display_list(self.cmd_line_param)
        logging.info(f"Cmd Line Displays: {self.cmd_line_displays}")

        # Details of Distinct adapters present in the system
        self.cmd_line_adapters = test_context.TestContext.get_gfx_adapter_details()

        for adapter_display_dict in self.cmd_line_displays:
            [(gfx_index, port)] = adapter_display_dict.items()
            # Perform plug operation only for non lfp panels
            if display_utility.get_vbt_panel_type(port, gfx_index) not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                port_type = self.get_cmd_line_param_values('connector_port_type', gfx_index, port)
                logging.info(f"port type : {port_type}")

                # Getting the edid and dpcd for each panel
                edid_val = self.get_cmd_line_param_values('edid_name', gfx_index, port)
                dpcd_val = self.get_cmd_line_param_values('dpcd_name', gfx_index, port)
                logging.debug(f"Edid value : {edid_val}, DPCD value : {dpcd_val}")
                self.display_edid_dpcd[port] = [gfx_index, edid_val, dpcd_val]

    ##
    # @brief        This method fetches the value of field requested, from cmd_line_param which is list of dictionaries,
    #               one for each adapter mentioned in command line. All non port specific fields will have same key
    #               value pair across all adapter dictionaries.
    # @param[in]    field: str
    #                   name of the field whose values has to be fetched
    # @param[in]    gfx_index: str
    #                   adapter index with default value set to gfx_0 as we don't need to pass gfx_index value for
    #                   non-port specific fields.E.g gfx_0, gfx_1
    # @param[in]    port: str
    #                   optional argument with default value set to None. Name of port is needed to fetch values of
    #                   port specific fields from command_line_param
    # @return       value: str
    #                   value of the requested field
    def get_cmd_line_param_values(self, field, gfx_index=None, port=None):
        value = ''
        if port is None:
            # Non-port specific fields have same values across adapter dictionaries, hence fetch it from 1st dictionary
            if field in self.cmd_line_param[0].keys():
                value = self.cmd_line_param[0][field]
            else:
                # Port name has to be passed to fetch port specific fields as display can be connected to different
                # ports of different adapters
                gdhm.report_driver_bug_di(f"[Interfaces][LTTPR] Port name is not provided in command line in {gfx_index}")
                self.fail("Please provide port name for port specific fields")
        else:
            gfx_index_num = int(gfx_index[-1])

            # Add NATIVE to the port name if the key is not found. E.g. When cmd has HDMI_F_NATIVE, the port arg will
            # contain only the port name (HDMI_F) but the cmd dict will have HDMI_F_NATIVE as the key.
            if self.cmd_line_param[gfx_index_num].get(port) is None:
                port = port + "_" + "NATIVE"

            if field in self.cmd_line_param[gfx_index_num][port]:
                value = self.cmd_line_param[gfx_index_num][port][field]
            else:
                gdhm.report_driver_bug_di("[Interfaces][LTTPR] Invalid field name passed by user in command line.")
                # If field name is neither a generic field nor port specific then it is invalid
                self.fail("Invalid field name passed by user")

        return value
         
    ##
    # @brief        teardown function
    # @details      Unplugs all the displays connected in the test
    # @return       None
    def tearDown(self):
        html.step_start("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        enumerated_displays = self.display_config.get_enumerated_display_info()
        total_displays_connected = enumerated_displays.Count
        if enumerated_displays == None:
            gdhm.report_driver_bug_di(f"[Interfaces][LTTPR] Enumerated display is None.")
            self.fail("Enumerated_displays is None")

        for count in range(enumerated_displays.Count):
            connector_port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[count].ConnectorNPortType).name
            gfx_index = enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            connector_type = enumerated_displays.ConnectedDisplays[count].PortType
            if display_utility.get_vbt_panel_type(connector_port, gfx_index) not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI] and \
                    connector_port not in ['DispNone','VIRTUALDISPLAY'] and \
                    enumerated_displays.ConnectedDisplays[count].FriendlyDeviceName != "Raritan CIM":
                display_utility.unplug(connector_port, False, connector_type, gfx_index= gfx_index)
            else:
                continue
            enumerated_displays_updated = self.display_config.get_enumerated_display_info()
            logging.debug(f"Enumerated Displays after unplug of {connector_port} :\n {enumerated_displays_updated.to_string()}")

            if not disp_cfg.is_display_attached(enumerated_displays_updated, connector_port, gfx_index):
                logging.info(f"Successfully unplugged display {connector_port}")
            else:
                # WA for DG platforms to not check unplug status due to OS behavior
                platform = self.platform_dict[gfx_index]
                if count + 1 == total_displays_connected and platform in ['DG1', 'DG2', 'ELG']:
                    logging.warning("WARN: Display {} reported as still Attached. Sometimes OS doesnot update Unplug Status for last display, in case where "
                                    "Virtual Display not plugged by driver. Ignoring unplug status for such cases".format(connector_port))
                else:
                    gdhm.report_driver_bug_di(f"[Interfaces][LTTPR] Display is still attached on port {connector_port} even after unplug")
                    self.fail(f"Unable to unplug display {connector_port}")
                        
        enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.debug(f"Enumerated Displays after unplug of all:{enumerated_displays.to_string()}")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
