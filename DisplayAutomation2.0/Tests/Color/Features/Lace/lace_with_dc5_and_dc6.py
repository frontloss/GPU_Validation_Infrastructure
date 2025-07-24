#################################################################################################
# @file         lace_with_dc5_and_dc6.py
# @brief        Test calls for get and set lace functionality with dc5 and dc6 persistence
# @author       Vimalesh D
#################################################################################################

import ctypes
import sys
import unittest
import logging
import time

from Libs.Core import display_essential
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Color.Common import color_constants
from Tests.Color.Features.Lace.lace_base import *
from Tests.Control_API.control_api_base import testBase


##
# @brief - Get Lace Control Library Test
class testGetSetLaceAPI(LACEBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        gfx_adapter_index = 'gfx_0'
        adapter_info = gfx_adapter_dict[gfx_adapter_index]
        driver_interface_ = driver_interface.DriverInterface()
        dc5_offset_values = []
        dc6_offset_values = []

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        logging.info("Step_1: get lace")
                        dc5_offset_values.append(driver_interface_.mmio_read(0x8F054, 'gfx_0'))
                        dc6_offset_values.append(driver_interface_.mmio_read(0x8F058, 'gfx_0'))
                        logging.info("Before Enabling Lace:")
                        logging.info("-------DC5 Offset Values")
                        logging.info(dc5_offset_values)
                        logging.info("-------DC6 Offset Values")
                        logging.info(dc6_offset_values)

                        time.sleep(2)
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: lace enabled and verified successfully")
                        else:
                            logging.error("Fail: Failed to enable and verify Lace")

                        time.sleep(1)  # breather after escape

                        for i in range(0, 5):
                            time.sleep(1)
                            dc5_offset_values.append(driver_interface_.mmio_read(0x8F054, 'gfx_0'))
                            dc6_offset_values.append(driver_interface_.mmio_read(0x8F058, 'gfx_0'))
                        for i in range(0, len(dc5_offset_values) - 1):
                            if dc5_offset_values[i + 1] < dc5_offset_values[i]:
                                self.fail("DC5 Counters not incremented")
                            if dc6_offset_values[i + 1] < dc6_offset_values[i]:
                                self.fail("DC5 Counters not incremented")

                        logging.info("Pass: Lace with DC5 and DC6 was persisted")

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info(
                                "Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(
                                    panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library get lace API Verification with DC5 and DC6 persistence')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
