######################################################################################
# \file
# \section color_base
# \remarks
# \ref color_base.py \n
# This script contains helper functions that will be used by Color test scripts
#
# \author   Anjali Shetty, Smitha B
######################################################################################
import logging
import sys
import unittest

import pythoncom

from Libs.Core import reboot_helper, cmd_parser, display_utility, driver_escape
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_power import DisplayPower
from Libs.Core.system_utility import SystemUtility
from registers.mmioregister import MMIORegister


class Offset(object):
    VIDEO_DIP_CTL_A = 0x60200
    VIDEO_DIP_CTL_B = 0x61200
    VIDEO_DIP_CTL_C = 0x62200

    PIPE_MISC_A = 0x70030
    PIPE_MISC_B = 0x71030
    PIPE_MISC_C = 0x72030

    DSP_CNTR_A = 0x70180
    DSP_CNTR_B = 0x71180
    DSP_CNTR_C = 0x72180

    PIPE_BOTTOM_COLOR_A = 0x70034
    PIPE_BOTTOM_COLOR_B = 0x71034
    PIPE_BOTTOM_COLOR_C = 0x72034
    PIPE_BOTTOM_COLOR_D = 0x73034


class ColorBase(unittest.TestCase):
    connected_list = []
    plugged_display = []
    config = DisplayConfiguration()
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    utility = SystemUtility()
    pythoncom.CoUninitialize()
    reg_read = MMIORegister()
    platform = None
    display_power = DisplayPower()
    app, xvycc_enable_status, ycbcr_enable_status, target_id, ycbcr_supported, xvycc_supported, display = None, 0, 0, 0, 0, 0, None
    stepCounter = 0
    custom_tags = ["-check_crc"]
    crc_verification_enabled = False

    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("************** TEST  STARTS HERE*************************")

        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)
        ##
        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail()

    def getStepInfo(self):
        self.stepCounter = self.stepCounter + 1
        return "STEP-%d: " % self.stepCounter

    def get_display_configuration(self, connected_port_list):
        port_config_str = ""
        for each_port in connected_port_list:
            target_id = self.config.get_target_id(each_port, self.enumerated_displays)
            mode = self.config.get_current_mode(target_id)
            port_config_str = port_config_str + "\n" + mode.to_string(self.enumerated_displays)
        return port_config_str

    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Test Clean Up")

        ##
        # Terminate the overlay application
        if self.app is not None:
            self.app.terminate()

        ##
        # Disable YCbCr or xvYCC
        if self.ycbcr_enable_status:
            driver_escape.configure_ycbcr(self.target_id, False)
        elif self.xvycc_enable_status:
            driver_escape.configure_xvycc(self.target_id, False)

        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.connected_list:
            if display != 'DP_A':
                logging.info("Trying to unplug %s", display)
                display_utility.unplug(display)

        logging.info("****************TEST ENDS HERE********************************")
