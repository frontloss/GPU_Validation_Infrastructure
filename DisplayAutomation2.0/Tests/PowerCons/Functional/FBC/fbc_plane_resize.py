########################################################################################################################
# @file         fbc_plane_resize.py
# @brief        Test for verifying FBC restriction check with different plane size.
#
# @author       Gowtham K L
########################################################################################################################
import time
from Libs.Core import flip
from Libs.Core.logger import html, gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.FBC.fbc_base import *

##
# FBC should be enabled for plane size between (200,30) and (4095, 4095), both inclusive
FBC_PLANE_SIZE_VERIFICATION_LIST = [(195, 30),  # (X, Y)
                                    (195, 32),
                                    (200, 32),  # (Min X, Min Y)
                                    (200, 30),
                                    (500, 500),
                                    (4095, 4095)  # (Max X, Max Y)
                                    ]

##
# @brief        This class contains FBC Plane Resize tests
class FbcPlaneResize(FbcBase):
    enable_mpo = flip.MPO()

    ##
    # @brief FBC restriction check with different plane size
    # @return None
    def runTest(self):
        status = True
        pixel_format = [None, None, None]

        if self.pixel_format_p1 is not None:
            pixel_format[0] = pc_external.PIXEL_FORMAT[self.pixel_format_p1]
        if self.pixel_format_p2 is not None:
            pixel_format[1] = pc_external.PIXEL_FORMAT[self.pixel_format_p2]
        if self.pixel_format_p3 is not None:
            pixel_format[2] = pc_external.PIXEL_FORMAT[self.pixel_format_p3]

        dut.prepare()
        for adapter in dut.adapters.values():
            gfx_index = adapter.gfx_index

            # Enable DFT framework and feature
            self.enable_mpo.enable_disable_mpo_dft(True, 1, gfx_adapter_index=gfx_index)
            logging.info(f"\tEnabled the DFT framework on {gfx_index}")
            for panel in adapter.panels.values():
                if not self.is_custom_plane_size_test:
                    for plane_size in FBC_PLANE_SIZE_VERIFICATION_LIST:
                        width = plane_size[0]
                        height = plane_size[1]
                        html.step_start(f"FBC with PLANE SIZE Width={width} & Height={height}) on {panel.port} on {gfx_index}")

                        # Generate flip of the required size on all adapters
                        status &= self.generate_flip_and_verify_fbc(adapter, panel, width, height, pixel_format)
                else:
                    # Generate flip of the required size on all adapters
                    status = self.generate_flip_and_verify_fbc(adapter, panel, None, None, pixel_format)

            # Disable the DFT framework and feature
            self.enable_mpo.enable_disable_mpo_dft(False, 1, gfx_adapter_index=gfx_index)
            logging.info("\tDisable the DFT framework success")

            time.sleep(2)

        if status is False:
                gdhm.report_driver_bug_pc("[PowerCons][FBC] Failed to verify FBC with different plane size restrictions")
                self.fail(f"FAIL : FBC verification with different plane sizes")
        logging.info(f"PASS : Succesfully verified FBC with different plane sizes")


    ##
    # @brief        Helper function to generate required flip and verify FBC
    # @param[in]    adapter object
    # @param[in]    panel object
    # @param[in]    width of the plane
    # @param[in]    height of the plane
    # @param[in]    pixel_format [(int, int), (int, int), (int, int)] (Color format value to apply for the planes, value to be compared from MMIO register)
    # @return       True for verification success False for failure.
    def generate_flip_and_verify_fbc(self, adapter, panel, width, height, pixel_format):
        fbc_result = False
        # Generate flip of the required size on all adapters
        generate_flip = pc_external.plane_format(adapter, panel, self.no_of_displays, self.source_id, self.enable_mpo, pixel_format,
                                                 width, height, self.is_custom_plane_size_test)
        if generate_flip is None:
            # Skip the flip generation on current plane size if plane size restrictions are failed
            logging.info(f"Skipping the flip generation on {width} x {height} as the resolution is invalid")
            return True
        if generate_flip is False:
            # Try to generate flip again, if it fails for the first time.
            if pc_external.plane_format(adapter, panel, self.no_of_displays, self.source_id, self.enable_mpo, pixel_format, width, height, 
                                        self.is_custom_plane_size_test) is False:
                # Disable the DFT framework and feature
                self.enable_mpo.enable_disable_mpo_dft(False, 1, gfx_adapter_index=adapter.gfx_index)
                logging.info("\tDisable the DFT framework success")
                time.sleep(2)
                logging.error(f"Test failed to generate the required flip on {panel.port} on {adapter.gfx_index}")
                gdhm.report_test_bug_os(f"[Display_OS_Features][Display_Flips] Test failed to generate the required flip")
                self.fail(f"FAIL : FBC verification with different plane sizes")

        # verify fbc on all adapters
        fbc_result = fbc.verify_fbc(adapter.gfx_index, is_display_engine_test=False)

        if fbc_result is False:
            logging.error(f"FAIL : FBC verification with flips generated in {width} x {height} resolution on {panel.port} on {adapter.gfx_index}")
        else:
            logging.info(f"PASS : FBC verification with flips generated in {width} x {height} resolution on {panel.port} on {adapter.gfx_index}")

        return fbc_result

if __name__ == '__main__':
    TestEnvironment.initialize()
    suite = unittest.TestLoader().loadTestsFromTestCase(FbcPlaneResize)
    result = unittest.TextTestRunner().run(suite)
    TestEnvironment.cleanup(result)
