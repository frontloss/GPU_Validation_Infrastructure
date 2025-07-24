########################################################################################################################
# @file         render_negative_formats.py
# @brief        This file contains test for MMIO verification for Render Decompression through ETL for Negative formats.
# @author       Prateek Joshi, Pai Vinayak1
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import winkb_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Decompression.Playback import decomp_base
from Tests.Display_Decompression.Playback import decomp_verifier
from Tests.Display_Decompression.Playback.decomp_verifier import MAX_LINE_WIDTH


##
# @brief    This contains test for verifying MMIO for Render Decompression for Negative formats
class RenderDecompNegativeFormats(decomp_base.DecompBase):
    ##
    # @brief        Test for verifying MMIO for Render Decompression for Negative formats
    # @return       None
    def runTest(self):

        assert decomp_verifier.is_feature_supported('RENDER_DECOMP'), "Platform does not support Render " \
                                                                      "Decompression [Planning Issue]"

        # Get pixel format from command line
        self.pixel_format = decomp_verifier.get_pixel_format(self.pixel_format)

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():

                # Play Video App
                logging.info(f"Invoke Media player with display {panel.connector_port_type}")
                media_instance = decomp_verifier.play_app("MEDIA", True)
                app_name = decomp_verifier.get_app_name('MEDIA')

                # Start ETL Tracer
                if decomp_verifier.start_etl_capture() is False:
                    self.fail("GfxTrace failed to start")

                # Switch between fullscreen and windowed mode
                decomp_verifier.media_window_switch()

                # Stop ETL Tracer
                playback_etl_file = decomp_verifier.stop_etl_capture(panel.connector_port_type)

                # Close the app
                media_instance.close_app()

                # Console to Main window
                winkb_helper.press('ALT+TAB')

                # Verify Render Decompression Programming
                if decomp_verifier.verify_negative_render_decomp(panel, self.pixel_format, playback_etl_file, app_name):
                    logging.info(" Pass: Negative Verification of Render Decompression ".center(MAX_LINE_WIDTH, "_"))
                    break
                else:
                    decomp_verifier.report_to_gdhm("Render")
                    logging.error("Fail: Negative Verification of Render Decompression ".center(MAX_LINE_WIDTH, "_"))
                    self.fail("Fail: Negative Verification of Render Decompression")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
