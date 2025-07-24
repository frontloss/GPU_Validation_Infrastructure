########################################################################################################################
# @file         render_decomp_max_resolution.py
# @brief        This file contains test for MMIO verification for Render Decompression through ETL with setting high
#               resolution.
# @author       Prateek Joshi, Pai Vinayak1
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import winkb_helper
from Libs.Core.display_config import display_config
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Decompression.Playback import decomp_base
from Tests.Display_Decompression.Playback import decomp_verifier
from Tests.Display_Decompression.Playback.decomp_verifier import MAX_LINE_WIDTH


##
# @brief    This contains test for verifying MMIO for Render Decompression through ETL with setting high resolution
class RenderDecompHighResolution(decomp_base.DecompBase):
    display_config = display_config.DisplayConfiguration()

    ##
    # @brief        Test for verifying MMIO for Render Decompression with setting high resolution
    # @return       None
    def runTest(self):

        # Feature supported
        assert decomp_verifier.is_feature_supported('RENDER_DECOMP'), "Platform does not support Render " \
                                                                      "Decompression [Planning Issue]"

        # Get pixel format from command line
        self.pixel_format = decomp_verifier.get_pixel_format(self.pixel_format)

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                self.enumerated_displays = self.display_config.get_enumerated_display_info()
                supported_modes_dict = self.display_config.get_all_supported_modes([panel.target_id], sorting_flag=True)
                mode_list = supported_modes_dict[panel.target_id]
                max_mode = mode_list[-1]

                if self.display_config.set_display_mode([max_mode]) is False:
                    decomp_verifier.report_to_gdhm("Render","Failed to apply display mode Actual: {} "
                                  .format(max_mode.to_string(self.enumerated_displays)))
                    logging.error("Failed to apply display mode: {} "
                                  .format(max_mode.to_string(self.enumerated_displays)))
                    self.fail()
                logging.info("\tPASS: Successfully applied display mode: {} "
                             .format(max_mode.to_string(self.enumerated_displays)))

                if decomp_verifier.start_etl_capture() is False:
                    self.fail("GfxTrace failed to start")

                # Play App
                logging.info(
                    f"Invoke {'3D' if self.app == 'NONE' else self.app[0]} App with connected display {panel.connector_port_type}")
                if self.app != 'NONE':
                    app_instance = decomp_verifier.play_app(self.app[0], True)
                    app_name = decomp_verifier.get_app_name('DEFAULT')
                else:
                    app_instance = decomp_verifier.play_3d_app(True)
                    app_name = decomp_verifier.get_app_name(self.app)

                # Playback for 30s
                time.sleep(30)

                # Close the app
                if self.app != 'NONE':
                    app_instance.close_app()
                else:
                    app_instance.terminate()

                # Console to Main window
                winkb_helper.press('ALT+TAB')

                # Stop ETL Tracer
                playback_etl_file = decomp_verifier.stop_etl_capture(panel.connector_port_type)

                # Verify Render Decompression Programming
                if decomp_verifier.verify_render_decomp(panel, self.pixel_format, playback_etl_file, app_name):
                    logging.info("Pass: Verification of Render Decompression".center(MAX_LINE_WIDTH, "_"))
                    break
                else:
                    decomp_verifier.report_to_gdhm("Render")
                    logging.error("Fail: Verification of Render Decompression".center(MAX_LINE_WIDTH, "_"))
                    self.fail("Fail: Verification of Render Decompression")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
