######################################################################################
# @file         apply_scaling_sd.py
# @brief        http://gta.intel.com/procedures/#/procedures/TI-400843/
#               Verify each modes with different scaling options supported by driver
#               in an iterative fashion on all connected displays
# @author       Venkatesh, Bharath
######################################################################################
# Manual to auto pilot
# TI-400843

import logging
import sys
import unittest

from Libs.Core import cmd_parser, display_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import action, alert

##
# @brief ApplyScaling Base class : To be used in Apply Scaling tests
class ApplyScaling(unittest.TestCase):
    enum_port_list = []
    test_result = True

    ##
    # @brief setUp() Executed before the runTest
    # @return None
    def setUp(self):
        # Get the config before the start of the test
        self.original_config = DisplayConfiguration().get_current_display_configuration()

        display_config = DisplayConfiguration()
        cmd_line_args = cmd_parser.parse_cmdline(sys.argv, ['-DISPLAY1', '-DISPLAY2', '-DISPLAY3'])

        ##
        # Unplug all external panels before starting the test
        # Todo: if required panels are already connected skip this step
        status = True
        while status is True:
            status = False
            enumerated_displays = display_config.get_enumerated_display_info()
            for display_index in range(enumerated_displays.Count):
                display = enumerated_displays.ConnectedDisplays[display_index]
                gfx_index = display.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                if display_utility.get_vbt_panel_type(CONNECTOR_PORT_TYPE(display.ConnectorNPortType.name), gfx_index) \
                        not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                    if action.unplug(CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name) is False:
                        self.fail("Failed to unplug external panel")
                    status = True

        ##
        # Plug required external panels
        # Todo: if required panels are already connected skip this step
        if cmd_line_args['DISPLAY1'] != 'NONE':
            if cmd_line_args['DISPLAY1'][0] != 'EDP':
                if action.plug(cmd_line_args['DISPLAY1'][0]) is False:
                    self.fail("Failed to plug {0} panel".format(cmd_line_args['DISPLAY1'][0]))

        if cmd_line_args['DISPLAY2'] != 'NONE':
            if cmd_line_args['DISPLAY2'][0] != 'EDP':
                if action.plug(cmd_line_args['DISPLAY2'][0]) is False:
                    self.fail("Failed to plug {0} panel".format(cmd_line_args['DISPLAY2'][0]))

        if cmd_line_args['DISPLAY3'] != 'NONE':
            if cmd_line_args['DISPLAY3'][0] != 'EDP':
                if action.plug(cmd_line_args['DISPLAY3'][0]) is False:
                    self.fail("Failed to plug {0} panel".format(cmd_line_args['DISPLAY3'][0]))
    ##
    # @brief This test is planned for 2 display tests
    # @return None
    def test_1(self):
        enumerated_display = DisplayConfiguration().get_enumerated_display_info()
        for index in range(0, enumerated_display.Count):
            self.enum_port_list.append(
                str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType)))
        alert.info("Starting ApplyScaling SD test with : {0}".format(self.enum_port_list))
        for port in self.enum_port_list:
            self.apply_single_display(port)

    ##
    # @brief Unit-test teardown function.
    # @return None
    def tearDown(self):
        # Set the same config as it was before the start of the test
        DisplayConfiguration().set_display_configuration(self.original_config)
        if not self.test_result:
            alert.error("Test failed, analyze logs for more details on failure")
            self.fail("Test failed, analyze logs for more details on failure")

    ##
    # @brief Get eDP, mipi, DP, HDMI count in the passed port_list
    # @param[in] port_list EDP_A/DP_B etc
    # @return edp_count, mipi_count, dp_count, hdmi_count
    def get_panel_count(self, port_list):
        edp_count = 0
        mipi_count = 0
        dp_count = 0
        hdmi_count = 0

        for port in port_list:
            if 'eDP' in port:
                edp_count += 1
            elif 'MIPI' in port:
                mipi_count += 1
            elif display_utility.get_vbt_panel_type(port, 'gfx_0') == display_utility.VbtPanelType.LFP_DP:
                edp_count += 1
            elif display_utility.get_vbt_panel_type(port, 'gfx_0') == display_utility.VbtPanelType.LFP_MIPI:
                mipi_count += 1
            elif 'DP' in port:
                dp_count += 1
            elif 'HDMI' in port:
                hdmi_count += 1

        return edp_count, mipi_count, dp_count, hdmi_count

    ##
    # @brief Method to apply single display configuration on requested port
    # @param[in] port DP_A/DP_B etc
    # @return None
    def apply_single_display(self, port):
        enumerated_display = DisplayConfiguration().get_enumerated_display_info()
        alert.info('Press Ok to apply single display on PORT : {}'.format(port))
        status = DisplayConfiguration().set_display_configuration_ex(1, [port])
        result = alert.confirm('Was single display on PORT : {} applied?'.format(port))
        if not status or not result:
            logging.error("Applying SD on port {0} failed.".format(port))
            alert.warning("Applying SD on port {0} failed.".format(port))
            self.test_result = False
        else:
            logging.info("Successfully applied SD on port {0}.".format(port))
            current_config = DisplayConfiguration().get_current_display_configuration()
            logging.info("Current display config {}".format(current_config.to_string(enumerated_display)))
            target_id = DisplayConfiguration().get_target_id(port, enumerated_display)
            self.set_all_supported_modes(target_id)

    ##
    # @brief method to set each of the supported modes by requested target_id
    # @param[in] target_id Target ID of the display
    # @return None
    def set_all_supported_modes(self, target_id):
        supported_modes = DisplayConfiguration().get_all_supported_modes([target_id], sorting_flag=True)
        enumerated_display = DisplayConfiguration().get_enumerated_display_info()
        mode_count = 1
        pruned_mode_list = list()

        for target, mode_list in supported_modes.items():
            # Pruning the mode list to max, mid and min from sorted list of supported modes
            pruned_mode_list.append(mode_list[0])
            pruned_mode_list.append(mode_list[len(mode_list) // 2])
            pruned_mode_list.append(mode_list[-1])

            for mode in pruned_mode_list:
                alert.info('Display mode {0} of {1} \nPress Ok to apply mode {2}'.format(
                    mode_count, len(pruned_mode_list), mode.to_string(enumerated_display)))
                mode_status = DisplayConfiguration().set_display_mode([mode])
                result = alert.confirm('Display mode {0} of {1} \nWas mode {2} applied?'.format(
                    mode_count, len(pruned_mode_list), mode.to_string(enumerated_display)))
                if not mode_status or not result:
                    logging.error("Failed to apply mode {}".format(mode.to_string(enumerated_display)))
                    self.test_result = False
                    result_1 = alert.confirm('Press Yes to continue to next mode, Press No to stop the test')
                    if not result_1:
                        alert.fail("Applying mode failed, exiting the test upon user request")
                        self.fail("Applying mode failed, exiting the test upon user request")
                else:
                    logging.info("Successfully applied mode {}".format(mode.to_string(enumerated_display)))
                mode_count += 1


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
