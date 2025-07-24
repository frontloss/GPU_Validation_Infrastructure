#################################################################################################
# @file         override_bpc_encoding_range.py
# @brief        This is a custom script which can used to display configurations with supported bpc and encoding
#               will perform below functionalities
#               1.To configure bpc and encoding through escape
#               2.To perform register verification for bpc and encoding
# @author       Vimalesh D
#################################################################################################

from Tests.Color.Common import color_mmio_interface
from Tests.Color.Common.color_escapes import configure_aviinfo
from Tests.Color.Features.Quantization.quantization_test_base import *
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding_test_base import *
from Tests.Color.Features.OverrideBpcEncoding import override_bpc_encoding
from Tests.Color.Verification import gen_verify_pipe
class OverrideBpcEncodingRange(OverrideBpcEncodingBase):
    def setUp(self):
        self.custom_tags["-QUANTRANGE"] = None  # For concurrency test
        super().setUp()
        enum_quantization = color_enums.RgbQuantizationRange
        if str(self.context_args.test.cmd_params.test_custom_tags["-QUANTRANGE"][0]) is not None:
            self.set_range = (
                getattr(enum_quantization,
                        str(self.context_args.test.cmd_params.test_custom_tags["-QUANTRANGE"][0]))).value
        else:
            self.fail("Commandline error: Quantisation range should not be empty")
    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    def runTest(self):
        enum_quantization = color_enums.RgbQuantizationRange
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    Bpc_Encoding_caps = BpcEncoding()
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(panel.display_and_adapterInfo, adapter.platform_type)
                    Bpc_Encoding_caps.DefaultBpc = default_bpc
                    Bpc_Encoding_caps.DefaultEncoding = default_encoding
                    self.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

                    temp = False
                    bpc = None
                    encoding = None

                    if status:
                        for index in range(len(combo_bpc_encoding)):
                            bpc = str(combo_bpc_encoding[index][0])
                            encoding = str(combo_bpc_encoding[index][1])
                            if bpc == self.bpc and encoding == self.encoding:
                                status = set_bpc_encoding(panel.display_and_adapterInfo, bpc, encoding, adapter.platform_type, panel.is_lfp)
                                temp = True
                                break

                        if temp is False:
                            random.shuffle(combo_bpc_encoding)
                            bpc = str(combo_bpc_encoding[0][0])
                            encoding = str(combo_bpc_encoding[0][1])
                            status = set_bpc_encoding(panel.display_and_adapterInfo, bpc, encoding, adapter.platform_type, panel.is_lfp)


                        # Enable Quantization
                        self.expected_range = self.set_range

                        if self.expected_range == enum_quantization.FULL.value:
                            self.conv_type = ConversionType.FULL_TO_FULL
                        if self.expected_range == enum_quantization.LIMITED.value:
                            self.conv_type = ConversionType.FULL_TO_STUDIO

                        if configure_aviinfo(panel.connector_port_type, panel.display_and_adapterInfo, self.set_range):
                            logging.info("Successfully set quantization range: {0} through escape".format(
                                self.set_range))
                        else:
                            self.fail(
                                "Fail to set quantization range: {0} through escape failed".format(self.set_range))

                        if status:
                            ##
                            # verify bpc and encoding
                            mmio_interface = color_mmio_interface.ColorMmioInterface()
                            pipe_verification = gen_verify_pipe.get_pipe_verifier_instance(adapter.platform, gfx_index)

                            ##
                            # Verify the quantization range
                            plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                            if pipe_verification.verify_quantization_range(panel.transcoder, plane_id, panel.pipe,
                                                                           self.expected_range) is False:
                                self.fail()
                            if override_bpc_encoding.verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id,
                                                            panel.transcoder, bpc, encoding, self.conv_type) is False:
                                self.fail()
                        else:
                            logging.info("Fail: Failed to set the override bpc and encoding")
                    else:
                        logging.info("Failed to get bpc and encoding Mask")


    ##
    # If the test set quantization as Full, at the end need to reset to Limited
    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and (panel.is_lfp is False):
                    if configure_aviinfo(panel.connector_port_type, panel.display_and_adapterInfo, ConversionType.FULL_TO_STUDIO.value):
                        logging.info("Successfully set quantization range: {0} through escape".format(
                            ConversionType.FULL_TO_STUDIO.value))
                    else:
                        self.fail(
                            "Fail to set quantization range: {0} through escape failed".format(ConversionType.FULL_TO_STUDIO.value))
            super().tearDown()

if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the bpc and encoding for the panel and verify")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
