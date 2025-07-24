##
# @file         flipq_base.py
# @brief        The script consists of unittest setup and tear down classes for FlipQ.
#                   * Parse command line.
#                   * Plug and unplug of displays.
# @author       Anjali Shetty

import logging
import unittest
from Libs.Core import etl_parser, winkb_helper, registry_access, display_essential
from Tests.MPO import mpo_ui_helper
from Tests.test_base import TestBase


##
# @brief    To perform setUp and tearDown functions
class FlipQBase(TestBase):
    mpo_helper = mpo_ui_helper.MPOUIHelper()
    action = None
    app = None
    buffer = None
    content_type = None
    interval = None

    ##
    # @brief        Unittest Setup function
    # @param[in]    self
    # @return       None
    def setUp(self):
        logging.info("************** TEST  STARTS HERE*************************")

        self.custom_tags["-CONTENT_TYPE"] = ['24FPS', '60FPS']
        self.custom_tags["-INTERVAL"] = None
        self.custom_tags["-BUFFER"] = None
        self.custom_tags["-ACTION"] = ['MAX_MIN', 'CLOSE_OPEN', 'WINDOW_SWITCH', 'PLAY_PAUSE', 'RESIZE', 'MOVE_WINDOW']
        self.custom_tags["-SCENARIO"] = ["CANCEL_QUEUE"]
        super().setUp()
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        flip_base.content_type = str(self.context_args.test.cmd_params.test_custom_tags["-CONTENT_TYPE"][0])
        flip_base.interval = str(self.context_args.test.cmd_params.test_custom_tags["-INTERVAL"][0])
        flip_base.buffer = str(self.context_args.test.cmd_params.test_custom_tags["-BUFFER"][0])
        self.action = str(self.context_args.test.cmd_params.test_custom_tags["-ACTION"][0])

        ##
        # Get platform and OS details
        self.mpo_helper.get_platform_os()

    ##
    # @brief        unittest TearDown function
    # @param[in]    self
    # @return       None
    def tearDown(self):
        logging.info("****************TEST ENDS HERE***************************")
        super().tearDown()


flip_base = FlipQBase()

if __name__ == '__main__':
    unittest.main()
