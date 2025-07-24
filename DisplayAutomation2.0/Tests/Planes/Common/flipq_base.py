########################################################################################################################
# @file         flipq_base.py
# @brief        The script consists of unittest setup and tear down classes for flipQ.
#               * Parse command line.
#               * Plug and unplug of displays.
#               * Apply display configuration.
#               * Enable and disable DFT.
# @author       Shetty, Anjali N
########################################################################################################################

import logging
import sys
import unittest

from Libs.Core import enum, display_utility, cmd_parser, registry_access, display_essential
from Libs.Core.logger import gdhm
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core import flip
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus

##
# @brief    Base class for FlipQ
class FlipQBase(unittest.TestCase):
    connected_list = []
    color_space = []
    pixel_format = []
    source_id = []
    tile_format = []
    display_config = DisplayConfiguration()
    mpo = flip.MPO()
    underrun = UnderRunStatus()
    registry_value = None
    ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
    ##
    # SB_PIXELFORMAT values for planar formats
    planar_formats = [15, 17, 18, 19]

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        ##
        # Custom tags for input pixel format and tile format.
        my_tags = ['-input_pixelformat', '-input_tileformat', '-flipcount']

        ##
        # Parse the command line.
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, my_tags)

        ##
        # Obtain display port list from the command line.
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        ##
        # Verify and plug the display.
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            gdhm.report_bug(
                title="[MPO]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail()
        else:
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        ##
        # Apply display configuration as specified in the command line.
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.connected_list) is False:
            self.fail('Failed to apply display configuration %s %s' %
                      (DisplayConfigTopology(topology).name, self.connected_list))
        else:
            logging.info('Successfully applied the display configuration as %s %s' %
                         (DisplayConfigTopology(topology).name, self.connected_list))

        ##
        # Get current display configuration.
        current_config = self.display_config.get_current_display_configuration()
        self.no_of_displays = current_config.numberOfDisplays

        ##
        # Source id of the display.
        for index in range(0, self.no_of_displays):
            self.source_id.append(index)

        ##
        # Get current applied mode.
        self.current_mode = self.display_config.get_current_mode(current_config.displayPathInfo[0].targetId)
        self.refresh_rate = self.current_mode.refreshRate

        ##
        # Read the default value of DisplayFeatureControl2 registry
        self.registry_value, registry_type = \
            registry_access.read(args=self.ss_reg_args, reg_name="DisplayFeatureControl2")

        ##
        # Value to enable bit 1 for enabling FlipQ for DFT
        if self.registry_value is not None:
            flipq_enable = self.registry_value | 0x2
        else:
            flipq_enable = 0x2

        ##
        # Modify the registry value to enable FlipQ for DFT.
        registry_access.write(args=self.ss_reg_args, reg_name="DisplayFeatureControl2",
                              reg_type=registry_access.RegDataType.DWORD, reg_value=flipq_enable)

        ##
        # Restart display driver
        status, reboot_required = display_essential.restart_gfx_driver()

        ##
        # Start underrun monitor.
        self.underrun.clear_underrun_registry()

        ##
        # Enable DFT.
        self.mpo.enable_disable_dft_flipq(True, 1)

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info("Test cleanup")

        ##
        # Disable DFT.
        self.mpo.enable_disable_dft_flipq(False, 1)

        ##
        # Read the default value of DisplayFeatureControl2 registry
        self.registry_value, registry_type = \
            registry_access.read(args=self.ss_reg_args, reg_name="DisplayFeatureControl2")

        ##
        # Value to disable DFT FlipQ
        if self.registry_value is not None:
            flipq_disable = self.registry_value & 0xFFFFFFFD
        else:
            flipq_disable = 0x0

        ##
        # Restore default value for DisplayFeatureControl2
        registry_access.write(args=self.ss_reg_args, reg_name="DisplayFeatureControl2",
                              reg_type=registry_access.RegDataType.DWORD, reg_value=flipq_disable)

        ##
        # Restart display driver
        status, reboot_required = display_essential.restart_gfx_driver()

        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            display_utility.unplug(display)


if __name__ == '__main__':
    unittest.main()