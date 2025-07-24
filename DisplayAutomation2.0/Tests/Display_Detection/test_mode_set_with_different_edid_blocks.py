################################################################################################################
# @file         test_mode_set_with_different_edid_blocks.py
# @brief        Verify if modeset functionality is working as expected in presence of various EDID/DTD specifications
#              To-do: move the helper functions in this file to a new base file and have only the tests here.           
# @author       Veena, Veluru
################################################################################################################
import sys
import logging
import unittest
from xml.etree import ElementTree as ET

from Libs.Core import cmd_parser, reboot_helper, display_utility
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PowerCons.Modules import common


##
# @brief        This class has basic tests to verify various EDID block specifications
class TestDifferentEdidBlocks(unittest.TestCase):
    cmd_line_param = []
    adapter_list = []
    panel_index_list = {}
    input_display_list = []
    expected_native_resolution = {}

    config = display_config.DisplayConfiguration()

    ##
    # @brief        parse_cmdline Parse displays to plug from cmdline params
    # @return       None
    def parse_cmdline(self):

        cmdline_args = sys.argv
        self.cmd_line_param = cmd_parser.parse_cmdline(cmdline_args)

        if type(self.cmd_line_param) is not list:
            self.cmd_line_param = [self.cmd_line_param]

        for param in self.cmd_line_param:
            cmd_line_param_adapter = param
            for key, value in cmd_line_param_adapter.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if self.input_display_list.__contains__(value['connector_port']):
                            adapter = self.adapter_list[self.input_display_list.index(value['connector_port'])]
                        if not self.input_display_list.__contains__(value['connector_port']) or (
                                self.input_display_list.__contains__(value['connector_port']) and
                                adapter != value['gfx_index']):
                            if value['gfx_index'] is None:
                                value['gfx_index'] = 'gfx_0'
                            self.adapter_list.insert(value['index'], str(value['gfx_index']).lower())
                            self.input_display_list.insert(value['index'], value['connector_port'])

        logging.info("Current Display Config Topology : {}".format(self.config.get_current_display_configuration_ex()))
        logging.debug("Exit: setUpClass")

    ##
    # @brief        Parse edid_blocks_configs.xml and prepare panel, resolution dict
    # @param[in]    display_port display to plug
    # @return       None
    def prepare_panel_resolution_dict(self, display_port):

        self.expected_native_resolution = {}

        # Parse XML file
        tree = ET.parse("Tests\Display_Detection\edid_config_xmls\edid_blocks_configs.xml")
        display_list_root = tree.getroot()
        vfpdb_root = display_list_root.find('VFPDB')

        if str(display_port).__contains__('DP_'):
            display_list = vfpdb_root.find('DP')
        elif str(display_port).__contains__('HDMI_'):
            display_list = vfpdb_root.find('HDMI')
        else:
            logging.error("FAIL: Invalid case. Case not found in xml for Connector port".format(display_port))
            gdhm.report_test_bug_di(
                title="[Interfaces][Display_Detection]EDID BLOCK VALIDATION TEST - Invalid port passed in cmdline")
            self.fail()

        for display in display_list:
            panel_index_to_plug = display.get('panelindex')
            self.expected_native_resolution[str(panel_index_to_plug)] = {"HRes": display.get('hzRes'),
                                                                         "VRes": display.get('vtRes'),
                                                                         "RR": display.get('rr')}

        logging.info("Panel Dict {}".format(self.expected_native_resolution))

    ##
    # @brief        Basic test case to verify if driver prioritizes VFPDB block while marking preferred mode.
    # @return       None
    # @cond
    @common.configure_test(selective=["VFPDB"])
    # @endcond
    def test_vfpdb_block_test(self) -> None:
        self.parse_cmdline()

        for display_port, gfx_index in zip(self.input_display_list, self.adapter_list):
            # Ignore HPD request for Internal Displays
            if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                               display_utility.VbtPanelType.LFP_MIPI]:
                logging.debug(
                    "Skipping : Internal Display {} is not Pluggable Display on adapter {}".format(display_port,
                                                                                                   gfx_index))
                continue
            self.prepare_panel_resolution_dict(display_port)
            for panel_index, expected_resolution in self.expected_native_resolution.items():
                ret_status = display_utility.plug(port=display_port, panelindex=panel_index, gfx_index=gfx_index)
                self.assertTrue(ret_status, "Plug of Display {} Failed on adapter {}".format(display_port, gfx_index))

                display_adapter_info = self.config.get_display_and_adapter_info_ex(display_port, gfx_index)
                native_mode = self.config.get_native_mode(display_adapter_info)
                if native_mode is None:
                    self.fail(f"Failed to get native mode for {display_adapter_info}")

                edid_hzres = native_mode.hActive
                edid_vtres = native_mode.vActive
                edid_refreshrate = native_mode.refreshRate

                logging.info("Native Mode returned from OS: {}X{}@{}".format(edid_hzres, edid_vtres, edid_refreshrate))

                if edid_hzres == int(expected_resolution["HRes"]) and \
                        edid_vtres == int(expected_resolution["VRes"]) and \
                        edid_refreshrate == int(expected_resolution["RR"]):
                    logging.info("PASS: Driver marked preferred mode is the mode set in VFPDB Block of the EDID")
                else:
                    gdhm.report_driver_bug_di(
                        title="[Interfaces][Display_Detection]Driver is not marking the VFPDB Mode as preferred")
                    self.fail(
                        "Driver is not marking the VFPDB Mode as preferred. Native Mode returned is {}X{}@{}".format(
                            edid_hzres, edid_vtres, edid_refreshrate))

                # unplug the displays after verification
                ret_status = display_utility.unplug(display_port, gfx_index=gfx_index)
                self.assertTrue(ret_status, "Unplug of Display {} Failed on adapter {}".format(display_port, gfx_index))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('TestDifferentEdidBlocks'))
    TestEnvironment.cleanup(outcome)
