###############################################################################
# @file     she_utility_ult.py
# @brief    she_utility_ult.py tests API's for she_utility.py
# @author   Reeju Srivastava, Beeresh, Sanehadeep Kaur
###############################################################################

import logging
import sys
import unittest

from Libs.Core import display_power
from Libs.Core.display_config.display_config import *
from Libs.Core.hw_emu.she_utility import SHE_UTILITY, LidSwitchState
from Libs.Core.test_env.test_environment import TestEnvironment

utility = SHE_UTILITY()
display_config = DisplayConfiguration()
enum_info = None
count_before_event = None
count_after_event = None


class sheutilityult(unittest.TestCase):

    def test_1_get_dll_version(self):
        logging.info(
            "***************************************** Test 1 started*******************************************")
        dll_version = utility.get_dll_version()
        logging.info("Version: %s " % dll_version)

    def test_2_is_she_device_connected(self):
        logging.info(
            "***************************************** Test 2 started*******************************************")
        return_status = utility.intialize()
        if return_status == 1:
            logging.info("SHE %s device connected " % return_status)
        elif return_status == 2:
            logging.info("SHE %s device connected " % return_status)
        self.assertTrue(return_status, "is_she_device_connected API failed !!")

    def test_3_issue_hotunplug(self):
        logging.info(
            "***************************************** Test 3 started*******************************************")
        delay = 0
        enum_info = display_config.get_enumerated_display_info()
        count_before_event = enum_info.Count
        logging.info("INFO : Number of Enumerated Display's : {}".format(enum_info.Count))
        return_status = utility.hot_plug_unplug(12, False, delay)
        logging.info("SHE device hot plug request returned %s" % return_status)
        self.assertTrue(return_status, "hot_unplug API failed !!")
        enum_info = display_config.get_enumerated_display_info()
        count_after_event = enum_info.Count
        self.assertEquals(count_after_event, count_before_event - 1, "hot_unplug API failed")

    def test_4_issue_hotplug(self):
        logging.info(
            "***************************************** Test 4 started*******************************************")
        delay = 0
        enum_info = display_config.get_enumerated_display_info()
        count_before_event = enum_info.Count
        logging.info("INFO : Number of Enumerated Display's : {}".format(enum_info.Count))
        return_status = utility.hot_plug_unplug(12, True, delay)
        logging.info("SHE device hot unplug request returned %s" % return_status)
        self.assertTrue(return_status, "hot_plug API failed !!")
        enum_info = display_config.get_enumerated_display_info()
        count_after_event = enum_info.Count
        self.assertEquals(count_after_event, count_before_event + 1, "hot_plug API failed")

    def test_5_switch_powerline(self):
        logging.info(
            "***************************************** Test 5 started*******************************************")
        delay = 0
        return_status = utility.switch_powerline(11, delay)
        logging.info("SHE device switch_powerline request returned %s" % return_status)
        self.assertTrue(return_status, "switch_powerline API failed !!")
        return_status = utility.switch_powerline(12, delay)
        logging.info("SHE device switch_powerline request returned %s" % return_status)
        self.assertTrue(return_status, "switch_powerline API failed !!")

    def test_6_lid_switch(self):
        logging.info(
            "***************************************** Test 6 started*******************************************")
        enum_info = display_config.get_enumerated_display_info()
        count_before_event = enum_info.Count
        logging.info("INFO : Number of Enumerated Display's : {}".format(enum_info.Count))
        return_status = utility.lid_switch_button_press(LidSwitchState.CLOSE, 20)
        logging.info("SHE device lid switch close request returned %s" % return_status)
        self.assertTrue(return_status, "lid_switch_button_press API failed !!")
        enum_info = display_config.get_enumerated_display_info()
        count_after_event = enum_info.Count
        self.assertTrue(count_after_event == count_before_event - 1, "lid_switch_button_press API failed")
        return_status = utility.lid_switch_button_press(LidSwitchState.OPEN, 20)
        logging.info("SHE device lid switch open request returned %s" % return_status)
        self.assertTrue(return_status, "lid_switch_button_press API failed !!")
        enum_info = display_config.get_enumerated_display_info()
        count_after_event = enum_info.Count
        self.assertTrue(count_after_event == count_before_event, "lid_switch_button_press API failed")

    def test_7_device_hibernate(self):
        logging.info(
            "***************************************** Test 7 started*******************************************")
        result = self.display_power_.set_lid_switch_power_state(display_power.LidSwitchOption.SLEEP)
        self.assertEquals(result, True, "Set lid switch state failed")
        logging.info("Set lid switch power state is successful for SLEEP")
        enum_info = display_config.get_enumerated_display_info()
        count_before_event = enum_info.Count
        logging.info("INFO : Number of Enumerated Display's : {}".format(enum_info.Count))
        return_status = utility.lid_switch(display_power.LidSwitchOption.SLEEP)
        logging.info("SHE device lid switch button Sleep request returned %s" % return_status)
        self.assertTrue(return_status, "lid_switch API failed !!")
        enum_info = display_config.get_enumerated_display_info()
        count_after_event = enum_info.Count
        self.assertTrue(count_after_event == count_before_event, "lid_switch API failed")
        result = self.display_power_.set_lid_switch_power_state(display_power.LidSwitchOption.HIBERNATE)
        self.assertEquals(result, True, "Set lid switch state failed")
        logging.info("Set lid switch power state is successful for HIBERNATE")
        return_status = utility.lid_switch(display_power.LidSwitchOption.HIBERNATE)
        logging.info("SHE device lid switch button hibernet request returned %s" % return_status)
        self.assertTrue(return_status, "lid_switch API failed !!")
        enum_info = display_config.get_enumerated_display_info()
        count_after_event = enum_info.Count
        self.assertTrue(count_after_event == count_before_event, "lid_switch API failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)