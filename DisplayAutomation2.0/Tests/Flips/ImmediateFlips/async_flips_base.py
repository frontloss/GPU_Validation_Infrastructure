########################################################################################################################
# @file         async_flips_base.py
# @brief        The script implements unittest default functions for setUp and tearDown, and common helper functions
#               given below:
#               * Plugging the displays.
#               * Verify devices are correctly plugged and enumerated.
#               * Unplugging the displays.
# @author       Ilamparithi Mahendran
########################################################################################################################
import logging
import os
import sys
import unittest

from Libs.Core import cmd_parser
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.test_env import test_context
from Libs.Core.logger import gdhm

##
# @brief    Base class for Immediate flip
class AsyncFlipsBase(unittest.TestCase):
    connected_list = []
    display_config = DisplayConfiguration()
    display_config_list = []
    flip_stream_artifactory = os.getcwd()[:2] + "\SHAREDBINARY\926864574"

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
        # Parse the command line
        custom_tags = ['-stream']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags)

        if self.cmd_line_param['STREAM'] == 'None':
            gdhm.report_bug(
                title="[Immediate Flips]Invalid stream provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.error("No stream is selected")
            self.fail()

        ##
        # Verify and plug the display
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        if len(self.connected_list) <= 0:
            gdhm.report_bug(
                title="[Immediate Flips]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.error("Minimum 1 display is required to run the test")
            self.fail()

        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        self.display_config_list.append((enum.SINGLE, [self.connected_list[0]]))


    ##
    # @brief            Unittest tearDown function
    # @return           voi
    def tearDown(self):
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            if not display_utility.unplug(display):
                self.fail("Unplug of display %s failed" % display)
            logging.info("%s display is unplugged", display)
