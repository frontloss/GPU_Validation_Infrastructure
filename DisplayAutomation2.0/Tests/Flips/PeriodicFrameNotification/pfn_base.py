########################################################################################################################
# @file         pfn_base.py
# @brief        The script implements unittest default functions for setUp and tearDown, and  common helper functions
#               given below:
#               * Plug the displays.
#               * Interface to run WHCK tool.
#               * Parser for WHCK.
#               * Interface to play media/3d applications.
#               * Unplug the displays.
# @author       Ilamparithi Mahendran
########################################################################################################################
import codecs
import logging
import os
import re
import sys
import time
import unittest

import win32api
import win32con

from Libs.Core import cmd_parser, enum
from Libs.Core import display_utility
from Libs.Core import window_helper
from Libs.Core import winkb_helper
from Libs.Feature.app import AppMedia
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Core.logger import gdhm

##
# @brief    Base class for periodic frame notification
class PeriodicFrameNotificationBase(unittest.TestCase):
    connected_list = []
    display_config = DisplayConfiguration()
    flip_test_store = os.path.join(test_context.TEST_STORE_FOLDER, "TestSpecificBin", "Flips")

    @property

    ##
    # @brief            Get the path from where media file needs to be fetched
    # @return           path to media file
    def media_file(self):
        return os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_1920_1080_avc.mp4")


    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        # Initialize the artifacts path
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        ##
        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        if len(self.connected_list) <= 0:
            gdhm.report_bug(
                title="[PFN]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.error("Minimum 1 display is required to run the test")
            self.fail()

        ##
        # Get the OS Info
        machine_info = SystemInfo()
        self.os_info = machine_info.get_os_info()

        self.display_config_list = []

        self.display_config_list.append((enum.SINGLE, [self.connected_list[0]]))
        if len(self.connected_list) >= 2:
            self.display_config_list.append((enum.EXTENDED, [self.connected_list[0], self.connected_list[1]]))
            # self.display_config_list.append((enum.EXTENDED, [self.connected_list[1], self.connected_list[0]]))
        if len(self.connected_list) >= 3:
            self.display_config_list.append(
                (enum.CLONE, [self.connected_list[0], self.connected_list[1], self.connected_list[2]]))

    ##
    # @brief            To parse log file
    # @return           status of the WHCK test
    def parse_log_file(self):
        log_file = codecs.open('%s\periodic_frame_notification.log' % test_context.TestContext.logs_folder(), 'r',
                               encoding='utf-16')
        for input_line in log_file:
            if input_line.startswith('Error'):
                logging.debug(input_line)
            if input_line.startswith('EndGroup: PeriodicFrameNotification::TestPeriodicFrameNotification'):
                return re.search('\[.*\]', input_line).group(0)
    ##
    # @brief            To parse rs4 log file
    # @return           passed or failed
    def parse_rs4_log_file(self):
        status = '[Passed]'
        functional_test1, functional_test2, functional_test3 = None, None, None
        # performance_test1, performance_test2, performance_test3, performance_test4, performance_test5 = None, None, None, None, None
        log_file = codecs.open('%s\periodic_frame_notification.log' % test_context.TestContext.logs_folder(), 'r',
                               encoding='utf-16')
        for input_line in log_file:
            if input_line.startswith('Error'):
                logging.debug(input_line)

            if input_line.startswith('EndGroup: PeriodicFrameNotification::TestPeriodicFrameNotification'):
                bad_test = re.search('\[.*\]', input_line).group(0)

            elif input_line.startswith('EndGroup: PeriodicFrameNotification::TestInvalidParameters'):
                functional_test1 = re.search('\[.*\]', input_line).group(0)
                logging.info("Functional Test PeriodicFrameNotification::TestInvalidParameters %s" % functional_test1)
            elif input_line.startswith('EndGroup: PeriodicFrameNotification::TestModeChange'):
                functional_test2 = re.search('\[.*\]', input_line).group(0)
                logging.info("Functional Test PeriodicFrameNotification::TestModeChange %s" % functional_test2)
            elif input_line.startswith('EndGroup: PeriodicFrameNotification::TestModeChangeGPU'):
                functional_test3 = re.search('\[.*\]', input_line).group(0)
                logging.info("Functional Test PeriodicFrameNotification::TestModeChangeGPU %s" % functional_test3)

            elif input_line.startswith('EndGroup: PeriodicFrameNotification::TestMultipleFramesAheadNotification'):
                performance_test1 = re.search('\[.*\]', input_line).group(0)
            elif input_line.startswith('EndGroup: PeriodicFrameNotification::TestVeryCloseNotifications'):
                performance_test2 = re.search('\[.*\]', input_line).group(0)
            elif input_line.startswith('EndGroup: PeriodicFrameNotification::TestNearMissNotifications'):
                performance_test3 = re.search('\[.*\]', input_line).group(0)
            elif input_line.startswith('EndGroup: PeriodicFrameNotification::TestPrecision'):
                performance_test4 = re.search('\[.*\]', input_line).group(0)
            elif input_line.startswith('EndGroup: PeriodicFrameNotification::TestSimultaneousActiveNotifications'):
                performance_test5 = re.search('\[.*\]', input_line).group(0)

        if functional_test1 == '[Failed]' or functional_test2 == '[Failed]' or functional_test3 == '[Failed]':
            status = '[Failed]'
            return status

        # if performance_test1 == '[Failed]' or performance_test2 == '[Failed]' or performance_test3 == '[Failed]' or performance_test4 == '[Failed]' or performance_test5 == '[Failed]':
        #     status = 're-run'
        #     return status

        return status

    ##
    # @brief            To run the test tool
    # @return           void
    def run_test_tool(self):
        os.system("%s\DxgkTests\\te.exe %s\DxgkTests\PeriodicFrameNotification.dll > %s\periodic_frame_notification.log"
                  % (self.flip_test_store, self.flip_test_store, test_context.TestContext.logs_folder()))


    ##
    # @brief            To play media in windowed or fullscreen mode based on input parameter
    # @param[in]        bfullscreen; if true fullscreen else windowed
    # @return           void
    def play_media(self, bfullscreen):

        app_media = AppMedia(self.media_file)
        app_media.open_app(bfullscreen, minimize=True)
        media_window_handle = app_media.instance

        return media_window_handle


    ##
    # @brief            To verify periodic frame notification
    # @return           True if log file parsing is passed else false
    def verify_periodic_frame_notification(self):
        if self.os_info.BuildNumber <= '16299':
            result = self.parse_log_file()
        else:
            result = self.parse_rs4_log_file()
        if result == '[Passed]':
            return True
        else:
            return False


    ##
    # @brief            Get Display Configuration
    # @param[in]        connected_port_list
    # @return           port configuration string
    def get_display_configuration(self, connected_port_list):
        port_config_str = ""
        for each_port in connected_port_list:
            target_id = self.display_config.get_target_id(each_port, self.enumerated_displays)
            mode = self.display_config.get_current_mode(target_id)
            port_config_str = port_config_str + "\n" + mode.to_string(self.enumerated_displays)
        return port_config_str

    ##
    # @brief            Helper function to report GDHM bug when Periodic Frame Notification failed
    # @return           void
    def report_to_gdhm_periodic_frame_notification_failure(self):
        gdhm.report_bug(
        title="[PFN]Periodic Frame Notification Test failed",
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
        )


    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            if not display_utility.unplug(display):
                self.fail("Unplug of display %s failed" % display)


if __name__ == '__main__':
    PeriodicFrameNotificationBase().parse_log_file()
