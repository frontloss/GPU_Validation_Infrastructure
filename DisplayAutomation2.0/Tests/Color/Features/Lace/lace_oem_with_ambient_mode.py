########################################################################################################################
# @file         lace_oem_with_ambient_mode.py
# @brief        Test calls for get lace functionality with OEM regkey verification
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
from Tests.Color.Features.Lace.lace_base import *
from Tests.Control_API.control_api_base import testBase
from Libs.Core import driver_escape, registry_access


##
# @brief - Test Set OEM regkey with value and perform Lace verification
class LaceOEMAmbientMode(LACEBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        lux_aggr_map_100_50_1000_100 = [0x64, 0x00, 0x00, 0x00, 0x32, 0xe8, 0x03, 0x00, 0x00, 0x64]

        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if registry_access.write(args=reg_args, reg_name="LaceAggrTrigger",
                                 reg_type=registry_access.RegDataType.DWORD, reg_value=0x40) is False:
            logging.error("Registry key add to LaceAggrTrigger Data failed")
            self.fail()

        lace_aggr_trigger = registry_access.read(reg_args, "LaceAggrTrigger")
        logging.info("LaceAggrTrigger Value from RegKey is {0}".format(lace_aggr_trigger))

        if registry_access.write(args=reg_args, reg_name="LaceLuxAggrMap",
                                 reg_type=registry_access.RegDataType.BINARY, reg_value=bytes(lux_aggr_map_100_50_1000_100)) is False:
            logging.error("Registry key add to LaceAggrTrigger Data failed")
            self.fail()

        display_essential.restart_display_driver()

        time.sleep(5)

        lux_aggr_map = registry_access.read(reg_args, "LaceLuxAggrMap")
        logging.info("Map Values is {0}".format(lux_aggr_map))

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_lfp:
                    color_igcl_escapes.get_lace_config(0, panel.display_and_adapterInfo)

                    if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=panel.target_id, lux=5000,
                                                                       lux_operation=True,
                                                                       aggressiveness_level=1,
                                                                       aggressiveness_operation=True):
                        logging.info("Lux and aggressiveness levels set successfully")

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
