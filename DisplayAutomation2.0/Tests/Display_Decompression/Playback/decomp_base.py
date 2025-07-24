#######################################################################################################################
# @file         decomp_base.py
# @brief        This script contains TestCase class for Render and Media tests.
#               Validation Steps for Decompression
#                   1. Start ETL tracer
#                   2. Open the targeted DX App/Media file (D3D/Triangle).
#                   4. Close the app
#                   5. Stop ETL tracer
#                   6. Generate report from ETL file and verify below:
#                       * Render / Media Decompression Programming
# @author       Prateek Joshi, Pai Vinayak1
#######################################################################################################################
import logging
import unittest

from Tests.Display_Decompression.Playback import decomp_verifier
from Tests.test_base import TestBase


##
# @brief    This contains the base class and associated functions to be used in Render and Media tests.
class DecompBase(TestBase):
    pixel_format = None
    media_file_path = None
    app = None

    ##
    # @brief     setUp Function of DecompBase class
    # @return    None
    def setUp(self):

        logging.info(" TEST STARTS ".center(decomp_verifier.MAX_LINE_WIDTH, "*"))
        logging.info(" SETUP: DECOMP_BASE ".center(decomp_verifier.MAX_LINE_WIDTH, "*"))

        self.custom_tags['-PIXEL_FORMAT'] = ['YUV_420', 'RGB_8888']
        self.custom_tags['-APP'] = ['MEDIA', 'FLIPAT', 'D3D12FULLSCREEN', 'CLASSICD3D']
        super().setUp()
        self.pixel_format = self.context_args.test.cmd_params.test_custom_tags['-PIXEL_FORMAT']
        self.app = self.context_args.test.cmd_params.test_custom_tags['-APP']
        if self.pixel_format is 'NONE':
            logging.error(
                f"Incomplete command line, please provide pixel format"
                f" {decomp_verifier.RENDER_DECOMP_SUPPORTED_FORMATS + decomp_verifier.MEDIA_DECOMP_SUPPORTED_FORMATS}")
            self.fail()

        self.pixel_format = self.pixel_format[0]

        if self.pixel_format in decomp_verifier.RENDER_DECOMP_SUPPORTED_FORMATS:
            logging.info(f"{self.pixel_format} Pixel Format is supported by Render Decompression")
        elif self.pixel_format in decomp_verifier.MEDIA_DECOMP_SUPPORTED_FORMATS:
            logging.info(f"{self.pixel_format} Pixel Format is supported by Media Decompression")
        else:
            logging.error("Unsupported pixel format for Render / Media Decompression")
            self.fail(f"Unsupported pixel format {self.pixel_format} for Render / Media Decompression")

        # Check for master registry key - DisableE2ECompression and EnableDisableUnifiedCompression for presi
        if decomp_verifier.presi_reg_key_check() is False:
            self.fail()

        # Check for master registry key - DisableE2ECompression (TGL+)
        if decomp_verifier.postsi_reg_key_check() is False:
            self.fail()

    ##
    # @brief     tearDown Function of DecompBase class
    # @return    None
    def tearDown(self):
        logging.info(" TEARDOWN: DECOMP_BASE ".center(decomp_verifier.MAX_LINE_WIDTH, "*"))
        super().tearDown()
        logging.info(" TEST ENDS ".center(decomp_verifier.MAX_LINE_WIDTH, "*"))


if __name__ == '__main__':
    unittest.main()
