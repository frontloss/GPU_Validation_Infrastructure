###############################################################################
# \ref     register_hash_ult.py
# \brief   register_hash_ult.py tests redister_hash functionalities like capturing and comparing of registers' hash
# \author  agolwala
###############################################################################

import sys, os

from Libs.Core.winkb_helper import press
from TestUtilities.register_hash_tool.register_hash import capure_reg_hash, reg_hash_comparison

import unittest
import time
from win32api import *
from ctypes import *

from Libs.Core.enum import *
from Libs.Core.display_config.display_config import *
from Libs.Core.system_utility import *
from Libs.Core.test_env.test_environment import *
from Libs.Core.window_helper import *


class RegisterHashUlt(unittest.TestCase):
    sys_utility = SystemUtility()
    display_config = DisplayConfiguration()

    def setUp(self):

        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        self.assertNotEquals(self.enumerated_displays, None,
                             "get_enumerated_display_info() API call failed! Aborting the test")

        ## Getting all supported modes
        self.target_id = self.enumerated_displays.ConnectedDisplays[0].TargetID
        self.supported_mode_list = self.display_config.get_all_supported_modes([self.target_id])

        for key, values in self.supported_mode_list.items():
            self.mode = values[-1]

        ##
        # Setting cursor position to (150, 150)
        SetCursorPos((150, 150))
        show_desktop_bg_only(True)

    def runTest(self):

        reg_hash_file_before_mode_set = r'capture_reg_hash_before_mode_set.csv'
        capure_reg_hash(reg_hash_file_before_mode_set)

        logging.info("Applying %s", self.mode.to_string(self.enumerated_displays))
        result = self.display_config.set_display_mode([self.mode], False, self.enumerated_displays)
        self.assertEquals(result, True, "Aborting the test as applying the display mode failed")
        logging.info("mode applied successfully")

        reg_hash_file_after_mode_set = r'reg_hash_file_after_mode_set.csv'
        capure_reg_hash(reg_hash_file_after_mode_set)

        ret_val = reg_hash_comparison(reg_hash_file_before_mode_set, reg_hash_file_after_mode_set)
        if not ret_val:
            logging.info("Registers' state is not same before and after mode set")

    def tearDown(self):

        show_desktop_bg_only(False)
        press('SHIFT+WIN+M')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
