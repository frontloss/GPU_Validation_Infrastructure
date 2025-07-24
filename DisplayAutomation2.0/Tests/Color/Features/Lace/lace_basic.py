########################################################################################################################
# @file         lace_basic.py
# @brief        Test calls for get and set lace functionality
# @author       Vimalesh
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
from Tests.Color.Common import color_igcl_escapes
from Tests.Color.Features.Lace.lace_base import *
from Tests.Control_API.control_api_base import testBase


##
# @brief - Get Lace Control Library Test
class testGetSetLaceAPI(LACEBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        logging.info("Step_1: get lace")
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: Lace was enabled and verified successfully for pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace enable with verification failed for pipe_{0}".format(panel.pipe))

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library get lace basic API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
