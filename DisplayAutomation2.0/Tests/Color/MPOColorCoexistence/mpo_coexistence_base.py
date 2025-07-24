################################################################################################################
# \file         mpo_coexistence_base.py
# \remarks      This script contains helper functions that will be used by MPO Color Co-existence test scripts
# \author       Anjali Shetty
################################################################################################################
import sys
import unittest

import win32api
import win32con

from Libs.Core import cmd_parser, display_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.system_utility import SystemUtility
from Libs.Core.window_helper import get_window, close_media_player
from Libs.Core.winkb_helper import press, perform_double_click
from Tests.Color.color_verification import *


class MPOCoexistenceBase(unittest.TestCase):
    connected_list = []
    utility = SystemUtility()
    config = DisplayConfiguration()
    machine_info = SystemInfo()
    mytags = ['-expected_pixelformat']

    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.mytags)

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
        # Get the OS Info
        self.os_info = self.machine_info.get_os_info()

        self.media_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_1920_1080_avc.mp4")

    def play_media(self, bfullscreen):
        win32api.ShellExecute(None, "open", self.media_file, None, None, win32con.SW_NORMAL)
        time.sleep(5)

        ##
        # WA for delay in launching Apps in GTA OS
        if '15063' < self.os_info.BuildNumber <= '16299':  # check only for RS3
            time.sleep(60)

        ##
        # WA for skipping the first run dialog box on RS4; Extending the WA for RS5 & 19H1
        if self.os_info.BuildNumber > '16299':

            if get_window('Let Movies & TV access your videos library?', True):
                logging.info("Popup is opened")
                press("ENTER")
                time.sleep(2)

            press('ESC')
            time.sleep(5)
            press('ESC')
            time.sleep(5)

        media_window_handle = get_window('Movies & TV', True)
        if media_window_handle is None:  # If Movies & TV not present, then check for Films & TV
            media_window_handle = get_window('Films & TV', True)
        if media_window_handle is None:
            self.fail("Application didnt open")
        media_window_handle.set_foreground()

        mode = self.config.get_current_mode(
            self.config.get_all_display_configuration().displayPathInfo[0].targetId)
        clip_size_hor = 1920 if mode.HzRes > 1920 else mode.HzRes
        clip_size_ver = 1080 if mode.VtRes > 1080 else mode.VtRes
        media_window_handle.set_position(0, 0, clip_size_hor, clip_size_ver)
        time.sleep(5)
        if (bfullscreen):
            perform_double_click(clip_size_hor / 2, clip_size_ver / 2)
            time.sleep(2)
        return media_window_handle

    def get_pixel_format(self, pixel_format):
        return {'YUV_422_PACKED_8_BPC': 'source_pixel_format_YUV_422_PACKED_8_BPC',
                'NV12_YUV_420': 'source_pixel_format_NV12_YUV_420',
                'RGB_2101010': 'source_pixel_format_RGB_2101010',
                'P010_YUV_420_10_BIT': 'source_pixel_format_P010_YUV_420_10_BIT',
                'RGB_8888': 'source_pixel_format_RGB_8888',
                'P012_YUV_420_12_BIT': 'source_pixel_format_P012_YUV_420_12_BIT',
                'RGB_16161616_FLOAT': 'source_pixel_format_RGB_16161616_FLOAT',
                'P016_YUV_420_16_BIT': 'source_pixel_format_P016_YUV_420_16_BIT',
                'YUV_444_PACKED_8_BPC': 'source_pixel_format_YUV_444_PACKED_8_BPC',
                'RGB_64_BIT_16161616_FLOAT': 'source_pixel_format_RGB_64_BIT_16161616_FLOAT',
                'RGB_2101010_XR_BIAS': 'source_pixel_format_RGB_2101010_XR_BIAS',
                'INDEXED_8_BIT': 'source_pixel_format_INDEXED_8_BIT',
                'RGB_565': 'source_pixel_format_RGB_565'
                }[pixel_format]

    def tearDown(self):
        logging.info("Test Clean Up")

        ##
        # Close the media player
        close_media_player()

        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            display_utility.unplug(display)


if __name__ == '__main__':
    unittest.main()
