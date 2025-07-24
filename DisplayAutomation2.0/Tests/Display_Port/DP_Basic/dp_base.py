#######################################################################################################################
# @file         dp_base.py
# @brief        This file contains DP BASIC base class which should be inherited by dp_linkrate_lanecount test.
# @details      dp_base.py contains DpBase class which implements setUp method to parse the comand line and
#               tearDown method required dp_linrate_lanecount. dp_plug to plug/unplug the display.
#               set_ssc method to enable/disable SSC in VBT.
# @author       Ap Kamal, Golwala Ami
#######################################################################################################################

import logging
import sys
import unittest

from Libs.Core import cmd_parser, display_essential
from Libs.Core import display_utility
from Libs.Core import reboot_helper
from Libs.Core import system_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt.vbt import Vbt


##
# @brief        A class which has to be inherited by dp_linkrate_lanecount test and contains some class methods, test
#               methods to set the environment required and also contains helper methods to be used by dp_linkrate_lanecount test
class DpBase(unittest.TestCase):
    utility = system_utility.SystemUtility()
    config = DisplayConfiguration()
    machine_info = SystemInfo()

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for dp linkrate lanecount test.
    #               It initialises the object and process the cmd line parameters.
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.plugged_dp_list = []
        self.cmd_line_param = {}
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=['-SSC'])
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    if ((value['edid_name'] is None) or (value['dpcd_name'] is None)):
                        self.fail("[Test Issue]: Aborting the test as edid/dpcd file is not provided in input")
                    self.plugged_dp_list.append((key, value))

    ##
    # @brief        This class method is the exit point for dp linkrate lanecount test.
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass

    ##
    # @brief        A class method to unplug existing DP & Plug new DP.
    # @param[in]    action: str
    #                   plug or unplug action
    # @param[in]    port: str
    #                   Port name for which display is to be plugged
    # @param[in]    dp_edid: str
    #                   EDID to be plugged
    # @param[in]    dp_dpcd: str
    #                   DPCD to be plugged
    # @return       None
    def dp_plug_unplug(self, action, port, dp_edid=None, dp_dpcd=None):
        action = action.upper()

        if action == "PLUG":
            if (True == display_utility.plug(port, dp_edid, dp_dpcd)):
                logging.info("INFO : Plug Success")
            else:
                logging.error("ERROR : Plug Failed")
                self.fail()

        elif action == "UNPLUG":
            if (True == display_utility.unplug(port)):
                logging.info("INFO : UnPlug Success")
            else:
                logging.error("ERROR : UnPlug Failed")
                self.fail()

    ##
    # @brief        A class method to enable/disable SSC in VBT
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    enable: str
    #                   Flag to be passed to enable/disable SSC in VBT
    # @return       starus: boolean
    # @return       reboot_required : Boolean
    def set_ssc(self, gfx_index='gfx_0', enable=True):
        status = False
        reboot_required = False
        logging.info("Set SSC called with flag as {}".format(enable))
        vbt_obj = Vbt(gfx_index)
        vbt_obj.block_1.IntegratedDisplaysSupported.DP_SSC_Enable = 1 if enable is True else 0
        if vbt_obj.apply_changes() is True:
            status, reboot_required = display_essential.restart_gfx_driver()

        return status, reboot_required


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
