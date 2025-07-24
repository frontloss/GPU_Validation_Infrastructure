########################################################################################################################
# @file         fbc_dirty_rectangle.py
# @brief        Test for verifying FBC dirty rectangle programming
#               Test steps are as follows 
#               1. Generate a the following dirty rectangle updates using DFT
#                   a. First half of the screen
#                   b. Second half of the screen
#                   c. Last 10 scanlines
#               2. Verify whether driver is programming FBC dirty rectangle co-ordinates according to
#                  generated updates
# @author       Gowtham K L
########################################################################################################################
import unittest
import time

from Libs.Core.flip import MPO
from Libs.Core.test_env import test_environment
from Libs.Feature.display_fbc import fbc
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.FBC.fbc_base import *
from Tests.PowerCons.Modules import common


##
# @brief        This class contains FBC Dirty Rectangle Test
class FbcDirtyRectangleTest(FbcBase):
    ##
    # @brief FBC dirty rectangle programming check
    # @return None
    def runTest(self):
        DIRTY_RECT = []
        source_id = []
        for index in range(0, self.no_of_displays):
            source_id.append(index)
        pixel_format = [None, None, None]

        if self.pixel_format_p1 is not None:
            pixel_format[0] = pc_external.PIXEL_FORMAT[self.pixel_format_p1]
        if self.pixel_format_p2 is not None:
            pixel_format[1] = pc_external.PIXEL_FORMAT[self.pixel_format_p2]
        if self.pixel_format_p3 is not None:
            pixel_format[2] = pc_external.PIXEL_FORMAT[self.pixel_format_p3]

        for adapter in dut.adapters.values():
            enable_mpo = MPO()
            # Enable the DFT framework and feature
            enable_mpo.enable_disable_mpo_dft(True, 1, gfx_adapter_index=adapter.gfx_index)
            for panel in adapter.panels.values():
                current_mode = self.display_config_.get_current_mode(panel.target_id)
                # Full Frame update
                DIRTY_RECT.append((0, current_mode.VtRes))
                # Update only bottom half of the plane till last-1 scanline
                DIRTY_RECT.append((current_mode.VtRes//2, current_mode.VtRes - 1))
                # Update only last 10 scan lines of the frame
                DIRTY_RECT.append((current_mode.VtRes - 10, current_mode.VtRes))
                logging.info(f"Dirty Rectangle data list = {DIRTY_RECT}")

                for rect_data in DIRTY_RECT:
                    if pc_external.plane_format(adapter, panel, self.no_of_displays, source_id, enable_mpo, pixel_format, width=None, height=None, 
                                                is_custom_plane_size_test=False, rect_data=rect_data) is False:
                        enable_mpo.enable_disable_mpo_dft(False, 1, gfx_adapter_index=adapter.gfx_index)
                        logging.info("\tDisable the DFT framework success")
                        self.fail(f"Failed to generate FLIP with DirtyRect Top= {rect_data[0]} Bottom= {rect_data[1]}")

                    time.sleep(3)
                    if fbc.verify_fbc_dirty_rectangle(adapter, panel, rect_data) is False:
                        enable_mpo.enable_disable_mpo_dft(False, 1, gfx_adapter_index=adapter.gfx_index)
                        logging.info("\tDisable the DFT framework success")
                        self.fail("FBC Dirty Rectangle verification failed")
                    logging.info("PASS : FBC Dirty Rectangle verification")
                   
            # Disable the DFT framework and feature
            enable_mpo.enable_disable_mpo_dft(False, 1, gfx_adapter_index=adapter.gfx_index)
            logging.info("\tDisable the DFT framework success")
            time.sleep(2)
    
        logging.info(f"PASS : FBC Dirty Rectangle verification successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(FbcDirtyRectangleTest))
    test_environment.TestEnvironment.cleanup(test_result)