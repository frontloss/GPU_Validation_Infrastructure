#######################################################################################################################
# @file         fast_lace_hw_histogramgeneration_verification.py
# @addtogroup   Test_Color
# @section      fast_lace_hw_histogramgeneration_verification.py
# @remarks      @ref fast_lace_hw_histogramgeneration_verification.py \n
#               The test script invokes Driver PCEscape call to enable LACE using Lux .
#               For a static image the Histogram generated by HW is compared against the golden histogram values
# @author       Soorya R
#######################################################################################################################
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
                    iet_data_firsttile_list = []
                    iet_data_lasttile_list = []
                    IMAGE_FILE = ["citylights.bmp", "earth.bmp", "mountains_partB.bmp", "oceansunrise.bmp"]

                    # LACE enable
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
                        self.display_staticimage(IMAGE_FILE[index])
                        logging.info("Image Displayed !!")
                        time.sleep(5)
                        # Disable IE enable bit before IET read
                        self.disable_ieenable_function()
                        # Get IET from registers
                        for pipe in range(len(self.lfp_pipe_ids)):
                            self.disable_ieenable_function()
                            # Get IET from registers
                            for pipe in range(len(self.lfp_pipe_ids)):
                                tile_x, tile_y = self.get_no_of_tiles(self.lfp_target_ids[pipe])
                                # Print this and check what is coming for each image
                                iet_data_firsttile_list.append([read_iet_from_registers_for_single_tile(pipe, 0, 0)])
                                iet_data_lasttile_list = read_iet_from_registers_for_single_tile(pipe, tile_x, tile_y)
                            time.sleep(8)

                    ##
                    # Disable DFT
                    self.mpo.enable_disable_mpo_dft(False, 1)

                    logging.info(" iet_data_firsttile_list is %s" % iet_data_firsttile_list)

                    ##
                    # Verify that successive IETs are not same for different images
                    for pipe in range(len(self.lfp_pipe_ids)):
                        iet_first_tile_pair = [(0, 1), (1, 2), (2, 3)]
                        iet_last_tile_pair = [(1, 2)]
                        for index in range(len(iet_first_tile_pair)):
                            previous_image = iet_first_tile_pair[index][0]
                            current_image = iet_first_tile_pair[index][1]
                            logging.debug("Previous Image IET Data :")
                            logging.debug(iet_data_firsttile_list[previous_image])
                            logging.debug("Current Image IET Data :")
                            logging.debug(iet_data_firsttile_list[current_image])
                            if iet_data_firsttile_list[previous_image] == iet_data_firsttile_list[current_image]:
                                logging.error(" Pipe : %s Part A  IET data remains same for two different buffers !!",
                                              chr(int(self.lfp_pipe_ids[pipe]) + 65))
                                self.fail()

                        # Part B
                        previous_image = iet_last_tile_pair[0][0]
                        current_image = iet_last_tile_pair[0][1]
                        if iet_data_lasttile_list[previous_image] == iet_data_lasttile_list[current_image]:
                            logging.error(" Pipe : %s Part B IET data remains same for two different buffers !!",
                                          chr(int(self.lfp_pipe_ids[pipe]) + 65))
                            self.fail()

                    # LACE disable
                    lux_val = 150
                    if color_igcl_escapes.set_lace_config(self.triggerType, self.setOperation, 0,
                                                          panel.display_and_adapterInfo):

                        time.sleep(1)
                        ##
                        # verify_lace_feature
                        if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                    "LEGACY", panel.target_id) is False:
                            self.fail("Lace verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library get lace API Verification with DC5 and DC6 persistence')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
