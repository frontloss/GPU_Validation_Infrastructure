######################################################################################
# \file         color_common_base.py
# \section      color_common_base
# \remarks      This script contains helper functions that will be used commonly by
#               Color test scripts. Further modifications to this file will be restricted
# \ref          color_common_base.py \n
# \author       Smitha B
######################################################################################
import sys
import unittest
import logging
from Libs.Core import cmd_parser, reboot_helper,system_utility, display_utility, enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.display_config.display_config import DisplayConfiguration
from Tests.Color import color_parse_etl_events
from Libs.Core import etl_parser
from Tests.Color.color_common_utility import get_platform_info


class ColorCommonBase(unittest.TestCase):
    connected_list = []
    config = DisplayConfiguration()
    cmd_line_param = None
    platform = None
    enumerated_displays = None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        ##
        # Verify and plug the display
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail()
        else:
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        ##
        # Set display configuration
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.config.set_display_configuration_ex(topology, self.connected_list) is False:
            self.fail('Failed to apply display configuration %s %s' % (DisplayConfigTopology(topology).name,
                                                                       self.connected_list))

        logging.info('Successfully applied the display configuration %s %s' % (DisplayConfigTopology(topology).name,
                                                                               self.connected_list))

        ##
        # Get the enumerated display info after plugging the displays and applying the required configuration
        self.enumerated_displays = self.config.get_enumerated_display_info()
        ##
        # Cache the platform information
        self.platform = get_platform_info()

    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.debug("Trying to unplug %s", display)
            display_utility.unplug(display)
