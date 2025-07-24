########################################################################################################################
# @file         mpo_ui_basic.py
# @brief        Basic test method for validating common test base
# @author       Gurusamy, Balaji
########################################################################################################################
import sys
import os
import logging
import unittest

from Libs.Core.logger import gdhm
from Tests.test_base import *
from Tests.MPO import mpo_ui_helper
from Libs.Core.test_env import test_context
from Libs.Core.system_utility import SystemUtility
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Feature.display_watermark.watermark import DisplayWatermark
from Libs.Core import cmd_parser, display_utility, enum, window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration


##
# @brief     MPOUIBase Base Class
class MPOUIBase(TestBase):
    display_list = []  # List of Dict. Ex: [{'DP_A': {'gfx_index': 'gfx_0'}}, {'DP_A': {'gfx_index': 'gfx_1'}}]
    custom_tags = {'-SCENARIO': ['BASIC', 'STRESS', 'DISPLAY_SWITCH', 'MONITOR_TURNOFF', 'HOTPLUG_UNPLUG',
                                 'POWER_EVENT_S3', 'POWER_EVENT_S4', 'POWER_EVENT_CS',  'POWER_EVENT_S5',
                                 'VIDEO_PLAYBACK',  'SNAP_MODE'],
                   '-ACTION': ['MAX_MIN', 'CLOSE_OPEN', 'WINDOW_SWITCH', 'PLAY_PAUSE', 'RESIZE', 'MOVE_WINDOW'],
                   '-MEDIA_CONTENT': ['2K_CLIP', '4K_CLIP'],
                   '-APP': '',
                   '-EXPECTED_PIXELFORMAT': ''
                   }
    expected_pixel_format = None
    action = None
    app = None
    scenario = None
    media_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\\mpo_1920_1080_avc.mp4")
    media_4k_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\\mpo_3840_2160_avc.mp4")

    ##
    # @brief     Base class setup method
    # @return           None
    def setUp(self):
        logging.info("{0} TEST STARTS HERE {0}".format('*' * 25))

        super().setUp()

        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.display_list.append({value['connector_port']: value})

        if len(self.display_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            # ToDo: Add gdhm logging

        self.wm_obj = DisplayWatermark()
        self.machine_info = SystemInfo()
        self.system_utility = SystemUtility()
        self.display_config = DisplayConfiguration()
        self.mpo_helper = mpo_ui_helper.MPOUIHelper()

    ##
    # @brief     Base class teardown method
    # @return           None
    def tearDown(self):
        logging.info("{0} TEST ENDS HERE {0}".format('*' * 26))
        super().tearDown()
