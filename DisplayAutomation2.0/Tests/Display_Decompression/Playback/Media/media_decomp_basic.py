########################################################################################################################
# @file         media_decomp_basic.py
# @brief        This script contains test which verifies MMIO for Media Decompression through ETL.
# @author       Prateek Joshi, Pai Vinayak1
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import winkb_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Decompression.Playback import decomp_base
from Tests.Display_Decompression.Playback import decomp_verifier
from Tests.Display_Decompression.Playback.decomp_verifier import MAX_LINE_WIDTH


##
# @brief    This contains test for verifying MMIO for Media Decompression
class MediaDecompMmioVerification(decomp_base.DecompBase):
    ##
    # @brief        Test for verifying MMIO for Media Decompression
    # @return       None
    def runTest(self):

        assert decomp_verifier.is_feature_supported('MEDIA_DECOMP'), "Platform does not support Media " \
                                                                     "Decompression [Planning Issue]"

        # Get pixel format from command line
        self.pixel_format = decomp_verifier.get_pixel_format(self.pixel_format)

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if decomp_verifier.start_etl_capture() is False:
                    self.fail("GfxTrace failed to start")

                # Play Video App
                logging.info(f"Invoke Media player with display {panel.connector_port_type}")
                media_instance = decomp_verifier.play_app("MEDIA", True)
                app_name = decomp_verifier.get_app_name('MEDIA')

                # Playback for 30s
                time.sleep(30)

                # Close the media player
                media_instance.close_app()

                # Console to Main window
                winkb_helper.press('ALT+TAB')

                # Stop ETL Tracer
                playback_etl_file = decomp_verifier.stop_etl_capture(panel.connector_port_type)

                # Verify Media Decompression Programming
                if decomp_verifier.verify_media_decomp(panel, self.pixel_format, playback_etl_file, app_name):
                    logging.info("Pass: Verification of Media Decompression".center(MAX_LINE_WIDTH, "_"))
                    break
                else:
                    decomp_verifier.report_to_gdhm("Media")
                    logging.error("Fail: Verification of Media Decompression".center(MAX_LINE_WIDTH, "_"))
                    self.fail("Fail: Verification of Media Decompression")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)