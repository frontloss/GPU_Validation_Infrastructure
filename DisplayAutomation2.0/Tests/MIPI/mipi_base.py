########################################################################################################################
# @file         mipi_base.py
# @brief        This file exposes base class for Mipi tests
# @details      It contains setUp and tearDown methods of unittest framework. In setUp, we parse
#               command_line arguments, plug displays and check MIPI panel's existence, read necessary VBT blocks.
#               In tearDown, the displays which were plugged during test will be unplugged.
#               checking whether TDR is detected or not
# @author       Sri Sumanth Geesala
########################################################################################################################
import logging
import os
import sys
import unittest

from Libs.Core import cmd_parser
from Libs.Core import display_essential
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core import reboot_helper
from Libs.Core import system_utility
from Libs.Core.display_config import display_config
from Libs.Core.display_power import DisplayPower
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Feature.mipi import mipi_helper


##
# @brief        Exposed base class for Mipi Test cases. Any class containing Mipi test cases can inherit this class to
#               to get the common setup and teardown functionality
class MipiBase(unittest.TestCase):
    utility = system_utility.SystemUtility()
    config = display_config.DisplayConfiguration()
    disp_power = DisplayPower()
    machine_info = SystemInfo()

    ##
    # @brief        This class method is the entry point for many Mipi test cases. Helps to initialize some of the
    #               parameters required for Mipi test case execution.
    # @details      This function parses the command line, performs checks and logs error if any
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):

        logging.info("Starting Test Setup")
        self.fail_count = 0
        self.my_custom_tags = ['-verify_crc', '-panel_sequence']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)

        # keep CRC verification disabled by default. If CRC verification required, we can pass "-verify_crc True"
        # from command line
        self.verify_crc = False
        self.mipi_pps_xml = None
        self.displays_in_cmdline = []
        self.platform = None
        self.supported_platforms = ['icl', 'lkf1', 'tgl', 'jsl', 'ryf', 'adlp']

        self.port_list = []
        self.mipi_master_port = None
        self.mipi_second_display = None
        self.num_ports = 0

        ##
        # check platform
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        if self.platform == 'icllp':
            self.platform = 'icl'
        if self.platform not in self.supported_platforms:
            self.fail("This test is applicable only for %s. Current platform is %s." % (
                self.supported_platforms, self.platform))

        ##
        # process cmdline for display list and custom tags
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.displays_in_cmdline.append(value['connector_port'])
            if key == 'VERIFY_CRC':
                self.verify_crc = True if value[0].lower() == 'true' else False
            if key == 'PANEL_SEQUENCE':
                self.mipi_pps_xml = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'MIPI\\pps_xml', value[0])

        ##
        # Initialize MIPI verifier. This will contain helper functions
        self.mipi_helper = mipi_helper.MipiHelper(self.platform)

        ##
        # Verify and plug the display.
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        ##
        # Checking for MIPI panel existence.
        if 'MIPI_A' in self.displays_in_cmdline:
            ret = display_config.is_display_attached(self.enumerated_displays, 'MIPI_A')
            if (ret is True):
                self.port_list.append("_DSI0")
                self.mipi_master_port = 'MIPI_A'
            else:
                self.fail('MIPI_A is passed in cmdline but not attached')
        if 'MIPI_C' in self.displays_in_cmdline:
            ret = display_config.is_display_attached(self.enumerated_displays, 'MIPI_C')
            if (ret is True):
                self.port_list.append("_DSI1")
                if (self.mipi_master_port is None):
                    self.mipi_master_port = 'MIPI_C'
            else:
                self.fail('MIPI_C is passed in cmdline but not attached')
        if (len(self.port_list) == 0):
            self.fail("None of the MIPI ports are connected. Aborting test")
        self.num_ports = len(self.port_list)

        if self.mipi_helper.dual_LFP_MIPI:
            self.mipi_second_display = 'MIPI_C'

        if (self.mipi_helper.dual_link == 1 and self.num_ports < 2):
            # adding explicitly, since OS will report only 1 target_id for MIPI; so is_display_attached for MIPIC will
            # return false
            self.port_list.append("_DSI1")
            self.num_ports = len(self.port_list)

        if (self.mipi_helper.dual_LFP_MIPI and self.num_ports < 2):
            self.mipi_helper.dual_LFP_MIPI = 0
            self.mipi_helper.dual_LFP_MIPI_port_sync = 0

        if self.mipi_helper.dual_LFP_MIPI:
            ##
            # apply ED MIPI LFP1 + MIPI LFP2, in case of dual LFP MIPI
            result = self.config.set_display_configuration_ex(enum.EXTENDED,
                                                              [self.mipi_master_port, self.mipi_second_display],
                                                              self.enumerated_displays)
            self.assertNotEquals(result, False, "Aborting the test as applying ED MIPI LFP1 + MIPI LFP2 config failed.")
        else:
            ##
            # apply SD MIPI configuration, in case single LFP MIPI
            result = self.config.set_display_configuration_ex(enum.SINGLE, [self.mipi_master_port],
                                                              self.enumerated_displays)
            self.assertNotEquals(result, False, "Aborting the test as applying SD MIPI display config failed.")

        # print current mipi configuration
        current_mipi_config = ''
        if self.mipi_helper.dual_LFP_MIPI:
            current_mipi_config += 'Dual LFP'
        elif self.mipi_helper.dual_link:
            current_mipi_config += 'Dual link'
        else:
            current_mipi_config += 'Single link'

        if self.mipi_helper.DSC_enabled:
            current_mipi_config += ' DSC'
        else:
            current_mipi_config += ' non-DSC'

        if self.mipi_helper.get_mode_of_operation(self.mipi_helper.panel1_index) == mipi_helper.VIDEO_MODE:
            current_mipi_config += ' Video mode'
        else:
            current_mipi_config += ' Command mode'

        logging.info('Current MIPI configuration is: ' + current_mipi_config)
        logging.info("Test Setup Completed")

    ##
    # @brief        This method is the exit point for Mipi test cases. This resets the environment changes done
    #               for the Mipi tests and checks for TDR.
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):

        logging.info("Starting Test Cleanup")
        ##
        # Unplug the displays and restore the configuration to the initial configuration.
        for display in self.plugged_display:
            logging.info("Trying to unplug %s" % (display))
            flag = display_utility.unplug(display)
            self.enumerated_displays = self.config.get_enumerated_display_info()
            self.assertNotEquals(self.enumerated_displays, None, "Aborting the test as enumerated_displays is None")

            result = display_config.is_display_attached(self.enumerated_displays, display)
            self.assertNotEquals(result, True, "Aborting the test as unplugging the display failed.")

        ##
        # Check TDR.
        result = display_essential.detect_system_tdr(gfx_index='gfx_0')
        self.assertNotEquals(result, True, "Aborting the test as TDR happened while executing the test")

        ##
        # If specified in command line, do CRC verification (only for video mode)
        if self.verify_crc is True and self.mipi_helper.get_mode_of_operation(
                self.mipi_helper.panel1_index) == mipi_helper.VIDEO_MODE:
            # skip CRC verification for pre-si
            if (self.utility.get_execution_environment_type() is not None and
                    self.utility.get_execution_environment_type() in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]):
                pass

        logging.info("Test Cleanup Completed")


if __name__ == '__main__':
    unittest.main()
