########################################################################################################################
# @file         mpo_ma_ui_base.py
# @brief        The script implements unittest default functions for setUp and tearDown
#               that will be used by MPO test scipts
# @author       Sunaina Ashok
########################################################################################################################

import logging
import os
import sys
import unittest
from collections import OrderedDict

from Libs.Core import cmd_parser, display_utility, enum, window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env import test_context
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_watermark.watermark import DisplayWatermark
from Libs.Core.logger import gdhm
from Tests.Planes.Common import plug_display_wrapper
from Libs.Core.display_config import display_config as disp_cfg
from Tests.MPO import mpo_ui_helper


##
# @brief    Contains unittest default functions for setUp and tearDown function
class MPOMAUIBase(unittest.TestCase):
    display_details = OrderedDict()
    connected_list = []
    pixel_format = []
    display_config = disp_cfg.DisplayConfiguration()
    machine_info = SystemInfo()
    wm = DisplayWatermark()
    mpo_helper = mpo_ui_helper.MPOUIHelper()

    ##
    # @brief            To create display adapter list
    # @param[in]        key adapter index
    # @param[in]        value displays
    # @return           void
    def create_display_adapter_list(self, key, value):
        if not bool(self.display_details):
            self.display_details[key] = []
            self.display_details[key].append(value)
        else:
            if key in self.display_details.keys():
                self.display_details[key].append(value)
            else:
                self.display_details[key] = []
                self.display_details[key].append(value)

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):

        ##
        # Get platform and OS details
        self.mpo_helper.get_platform_os()

        ##
        # Custom tags for input pixel format and tile format.
        my_tags = ['-expected_pixelformat']

        ##
        # Parse the command line.
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, my_tags)

        ##
        # Obtain display port and adapter list from the command line.
        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        self.connected_list.insert(value['index'], value['connector_port'])
                        self.create_display_adapter_list(value['gfx_index'], value['connector_port'])

        ##
        # Verify and plug the display.
        if len(self.connected_list) >= 2:
            for key, value in self.display_details.items():
                if len(value) <= 0:
                    gdhm.report_bug(
                        title="[MPO]Invalid displays provided in command line",
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P3,
                        exposure=gdhm.Exposure.E3
                    )
                    self.fail("Minimum 1 display is required per adapter")

            for index in range(0, len(self.cmd_line_param)):
                for key, value in self.cmd_line_param[index].items():
                    if cmd_parser.display_key_pattern.match(key) is not None:
                        if value['connector_port'] is not None:
                            plug_display_wrapper.plug_display(value['connector_port'], self.cmd_line_param[index])
        else:
            gdhm.report_bug(
                title="[MPO]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail("Minimum 2 displays are required for the test")

        self.media_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_1920_1080_avc.mp4")
        window_helper.close_media_player()
        self.under_run_status = UnderRunStatus()
        self.under_run_status.clear_underrun_registry()

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        status = False
        system_utility = SystemUtility()
        window_helper.close_media_player()

        if self.mpo_helper.app3d is not None:
            self.mpo_helper.app3d.close_app()

        if self.under_run_status.verify_underrun() is True:
            logging.error("Underrun seen in the test")

        for key, value in self.display_details.items():
            for display in value:
                if display != 'DP_A':
                    logging.info("Trying to unplug %s", display)
                    display_utility.unplug(display, gfx_index=key.lower())

        logging.info("****************TEST ENDS HERE********************************")

if __name__ == '__main__':
    unittest.main()
