########################################################################################################################
# @file         lace_set_fixed_mode.py
# @brief        Test calls for get and set lace functionality with OEM regkey
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
from Libs.Core import driver_escape
from Tests.Color.Features.Lace.lace_base import *
from Tests.Control_API.control_api_base import testBase
from Libs.Core import driver_escape, registry_access


##
# @brief - Test Set OEM regkey with value and perform Lace verification
class LaceSetFixedMode(LACEBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        logging.info("OEM Regkey Setting the Aggressiveness Percent as 80 to verify the Fixed Aggressive Mode")
        if registry_access.write(args=reg_args, reg_name="LaceAggrTrigger",
                                 reg_type=registry_access.RegDataType.DWORD, reg_value=0x1400001) is False:
            logging.error("Registry key add to LaceAggrTrigger Data failed")
            self.fail()

        display_essential.restart_display_driver()

        lace_aggr_trigger = registry_access.read(reg_args, "LaceAggrTrigger")
        logging.info("LaceAggrTrigger value set in the registry is {0}".format(lace_aggr_trigger))

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_lfp:
                    ##
                    # verify_lace_feature
                    if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                "LEGACY") is False:
                        self.fail("Lace verification failed")
                    else:
                        logging.info("Pass: Verification of Lace passed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Set OEM regkey and perform lace basic API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)