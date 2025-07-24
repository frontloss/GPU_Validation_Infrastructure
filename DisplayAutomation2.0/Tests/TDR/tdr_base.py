##
# @file tdr_base.py
# @brief The script contain base class of TDR test case along with setup and teardown
#        * The script takes input as require panel and apply display configuration
# @author Patel, Ankurkumar G, Doriwala, Nainesh P

import logging
import sys
import unittest

from Libs.Core import cmd_parser, registry_access
from Libs.Core import display_essential
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core import reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus

# Dump path
dump_path = "C:\Windows\LiveKernelReports\WATCHDOG"


##
# @brief It contains setUp and tearDown methods of Unittest framework
class TDRBase(unittest.TestCase):
    display_list = []
    input_display_list = []
    enumerated_display = None
    config = DisplayConfiguration()
    underrun = UnderRunStatus()
    cmd_config = enum.SINGLE
    is_teardown_required = False

    ##
    # @brief Setup function for test
    # @return None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("SetUp of TDR base")
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        self.input_display_list[:] = []
        # input_display_list[] is a list of Port Names from user args
        # Handle multi-adapter scenario
        if not isinstance(self.cmd_line_param, list):
            self.cmd_line_param = [self.cmd_line_param]

        for index in range(len(self.cmd_line_param)):
            adapter_dict = self.cmd_line_param[index]
            for key, value in iter(adapter_dict.items()):
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if value['gfx_index'] is not None:
                            self.input_display_list.append((value['connector_port'], value['gfx_index']))

                if key == 'CONFIG':
                    if value:
                        self.cmd_config = eval('enum.%s' % value)
                    else:
                        self.cmd_config = enum.SINGLE

        # Verify and plug the display
        self.plugged_display = self.plug_require_display()
        self.enumerated_display = self.config.get_enumerated_display_info()
        self.assertNotEquals(self.enumerated_display, None, "Aborting the test as enumerated_displays are None.")

        # enumerated_display is a list of plugged displays, verify for match in both list
        if len([item for item in self.plugged_display if item not in self.input_display_list]) != 0:
            self.is_teardown_required = True
            self.fail("Required displays are not enumerated")

        self.assertNotEqual(self.enumerated_display.Count, 0, "Aborting the test as enumerated display count is zero")
        display_adapter_info_list = []
        for item in self.input_display_list:
            logging.info("0: {}, 1: {}".format(item[0], item[1]))
            display_adapter_info_list.append(self.config.get_display_and_adapter_info_ex(item[0], item[1]))
        self.assertEqual(self.config.set_display_configuration_ex(self.cmd_config, display_adapter_info_list,
                                                                  self.config.get_enumerated_display_info()),
                         True, "failed to apply display configuration")

        # Clearing all existing Dumps from LiveKernelReport Directory
        display_essential.clear_tdr()
        logging.info("cleared TDR from LiveKernelReport directory pre TDR generate")

        ##
        # From RS5 onwards dumps file automatically deleted from live kernel Report folder.
        # Creating/ Adding registry to keep(Not delete) live kernel dumps from Live kernel Reports folder.
        reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                 reg_path=r"SYSTEM\CurrentControlSet\Control\CrashControl\LiveKernelReports")
        registry_access.write(args=reg_args, reg_name="DeleteLiveMiniDumps", reg_type=registry_access.RegDataType.DWORD,
                              reg_value=0)

    ##
    # @brief plug required display as given in command line parameter.
    # @return plugged_display_list - list of plug displays
    def plug_require_display(self):
        plugged_display_list = []
        for index in range(len(self.cmd_line_param)):
            adapter_dict = self.cmd_line_param[index]
            for key, value in adapter_dict.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if value['gfx_index'] is not None and value['is_lfp'] is False:
                            if display_utility.plug(port=value['connector_port'],
                                                    gfx_index=value['gfx_index'].lower()) is True:
                                logging.info("{} Display plug on adapter {}".
                                             format(value['connector_port'], value['gfx_index']))
                                plugged_display_list.append((value['connector_port'], value['gfx_index']))
                            else:
                                self.fail("failed to plug {} display on adapter {}"
                                          .format(value['connector_port'], value['gfx_index']))

        return plugged_display_list

    ##
    # @brief tearDown Function for TDR
    # @return None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.debug("CleanUp of TDR base, teardown_requried status:{}".format(self.is_teardown_required))
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        if self.is_teardown_required:
            for display in self.plugged_display:
                logging.info("Trying to unplug %s", display)
                self.assertEquals(display_utility.unplug(display), True, "Aborting the test as display unplug failed")
                logging.info("Successfully  unplugged %s", display)
        else:
            logging.info("Unplug of displays not required")
