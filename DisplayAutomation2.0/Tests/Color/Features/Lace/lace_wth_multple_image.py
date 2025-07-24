#################################################################################################
# @file         lace_with_dft_flip.py
# @brief        Test calls for get and set lace functionality with dft flip with basic tile verification
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
from Tests.Color.Common import color_constants, color_escapes
from Tests.Color.Features.Lace.lace_base import *
from Tests.Control_API.control_api_base import testBase
from Tests.Color.Verification import gen_verify_pipe, feature_basic_verify


##
# @brief - Get Lace Control Library Test
class testGetSetLaceAPI(LACEBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        self.lfp_pipe_ids = []
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    self.lfp_pipe_ids.append(panel.pipe)
                    IMAGE_FILE = "driveway.bmp"
                    LUX_VALUES = [20, 50, 70, 90]
                    iet_data_list = []

                    ##
                    # LACE enable
                    if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                              panel, True):
                        logging.info("Pass: Lace was enabled and verified successfully")
                    else:
                        self.fail("Lace enable/disable with verification failed")

                    ##
                    # Enable DFT
                    self.mpo.enable_disable_mpo_dft(True, 1)

                    ##
                    # Set Cursor Position to (500,500)
                    win32api.SetCursorPos((500, 500))

                    ##
                    # Flip image
                    for index in range(0, 4):
                        self.display_staticimage(IMAGE_FILE)
                        logging.info("Image Displayed !!")
                        if color_igcl_escapes.set_lace_config(self.triggerType, self.setOperation, LUX_VALUES[index],
                                                              panel.display_and_adapterInfo):

                            time.sleep(1)
                            ##
                            # verify_lace_feature
                            if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                        "LEGACY", panel.target_id) is False:
                                self.fail("Lace verification failed")

                        time.sleep(5)
                        # Disable IE enable bit before IET read
                        self.disable_ieenable_function()
                        time.sleep(2)
                        # Get IET from registers
                        for pipe in range(len(self.lfp_pipe_ids)):
                            iet_data = read_iet_from_registers_for_single_tile(pipe, 0, 0)
                            iet_data_list.append(iet_data)

                    ##
                    # Disable DFT
                    self.mpo.enable_disable_mpo_dft(False, 1)

                    ##
                    # Verify that successive IETs are not same for different images
                    for pipe in range(len(self.lfp_pipe_ids)):
                        low = 1 * (pipe + 1)
                        high = 4 * (pipe + 1)

                        for n in range(low, high):
                            if iet_data_list[n - 1] == iet_data_list[n]:
                                logging.info("List : %d --> %s \n  List : %d --> %s ", n - 1, str(iet_data_list[n - 1]),
                                             n,
                                             str(iet_data_list[n]))
                                logging.error(" Pipe : %s IET data remains same for two different buffers !!",
                                              chr(int(self.lfp_pipe_ids[pipe]) + 65))
                                self.fail()

                    if self.underrun.verify_underrun():
                        logging.error("Underrun Occured")

                    ##
                    # LACE disable
                    lux_val = 150
                    if color_escapes.configure_als_aggressiveness_level(port, panel.display_and_adapterInfo, lux=150,
                                                                        aggressiveness_level=1,
                                                                        aggressiveness_operation=True,
                                                                        lux_operation=True):
                        time.sleep(1)
                        ##
                        # verify_lace_feature
                        if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, False,
                                                                    "LEGACY", panel.target_id) is False:
                            self.fail("Lace verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library get lace API Verification with DC5 and DC6 persistence')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
