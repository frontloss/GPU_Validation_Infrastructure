########################################################################################################################
# @file         lace_basic.py
# @brief        Test calls for get and set lace functionality,
#               This is a custom script which can used to apply SINGLE/CLONE/EXTENDED display configurations
#               This scripts comprises of test_01_basic,  and test_02_stress, the function  will
#               perform below functionalities
#               1.To configure enable/disable lace for the display through command line for Basic scenario
#               2.To configure enable/disable lace for 5 iterations for Stress scenario
# @author       Pooja A
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Color.Common import color_constants
from Tests.Color.Features.Lace.lace_base import *
from Tests.Control_API.control_api_base import testBase

##
# Dictionary map for register bit and function parameter  0 or 1 to map Enable or Disable
BIT_MAP_DICT = {1: "enabled", 0: "disabled"}

##
# @brief - Get Lace Control Library Test
class testGetSetLaceAPI(LACEBase):

    ##
    # @brief        Providing flexibility in command line to enable/disable Lace
    # @return       None
    def setUp(self):
        self.custom_tags["-STATUS"] = None
        super().setUp()
        self.status = str(self.context_args.test.cmd_params.test_custom_tags["-STATUS"][0])
        if self.status == 'ENABLE':
            self.status = True
        else:
            self.status = False


    ##
    # @brief            test_01_basic() executes the actual test steps.
    # @return           void
    @unittest.skipIf(get_action_type() != "BASIC", "Skip the test step as the action type is not basic")
    def test_01_basic(self):

        # Enable/Disable Lace feature in all supported panels and verify through command line
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, configure_lace=self.status):
                            logging.info("PASS: Lace was {0} and verified successfully".format(BIT_MAP_DICT[int(self.status)]))
                        else:
                            self.fail("FAIL: Lace enable/disable with verification failed")

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}"
                                         .format(panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

    ##
    # @brief        test_02_stress() executes 5 iterations of enable/disable of Lace and performing register level verification.
    # @return       None
    @unittest.skipIf(get_action_type() != "STRESS", "Skip the test step as the action type is not stress")
    def test_02_stress(self):

        # Enable/Disable lace feature in all supported panels and verify
        for index in range(0, 5):
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.is_lfp:
                        if self.check_primary_display(port):
                            # enabling lace in every iteration
                            if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                      panel.display_and_adapterInfo, panel, configure_lace=True):
                                logging.info("PASS: Lace was enabled and verified successfully")
                            else:
                                self.fail("FAIL: Lace enable/disable with verification failed")

                            # disabling lace in every iteration
                            if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                      panel.display_and_adapterInfo, panel, configure_lace=False):
                                logging.info("PASS: Lace was disabled and verified successfully")
                            else:
                                self.fail("FAIL: Lace enable/disable with verification failed")

                        # Lace should not be enabled for 2nd LFP which is not set as primary
                        else:
                            if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                      panel.display_and_adapterInfo,
                                                      panel, False):
                                logging.info("Pass: Lace was disabled and verified successfully for second LFP on "
                                             "pipe_{0}".format(panel.pipe))
                            else:
                                self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

    ##
    # @brief        Teardown to skip the base class teardown to avoid Lace Disable
    # @return       None
    def tearDown(self):
        logging.info("----Lace Manual Test Operation completed----")

if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library get lace basic API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)