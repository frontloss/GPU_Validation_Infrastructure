#################################################################################################
# @file         override_bpc_encoding_range.py
# @brief        This is a custom script which can used to display configurations with supported bpc and encoding
#               will perform below functionalities
#               1.To configure bpc and encoding through escape
#               2.To perform register verification for bpc and encoding
# @author       Vimalesh D
#################################################################################################

from Tests.Color.Common import color_mmio_interface, color_igcl_escapes
from Tests.Color.Common.color_escapes import configure_aviinfo
from Tests.Color.Features.Quantization.quantization_test_base import *
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding_test_base import *
from Tests.Color.Features.OverrideBpcEncoding import override_bpc_encoding
from Tests.Color.Verification import gen_verify_pipe


class OverrideBpcEncodingIgcl(OverrideBpcEncodingBase):

    def setUp(self):
        super().setUp()

    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    def runTest(self):
        enum_quantization = color_enums.RgbQuantizationRange
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    Bpc_Encoding_caps = BpcEncoding()
                    # argsGetSetWireFormat = control_api_args.ctl_get_set_wireformat()
                    for index in range(0, 4):
                        status = False
                        encoding_value_list = ["RGB", "YCBCR420", "YCBCR422", "YCBCR444"]
                        color_model_set_via_default = ""
                        for encoding_value in range(0, len(encoding_value_list)):
                            if requested_encoding is None:
                                encoding_value = requested_encoding
                            status, color_model_set_via_default = self.default_set_encoding(gfx_index, platform,
                                                                                            pipe, transcoder,
                                                                                            encoding_value_list[
                                                                                                encoding_value],
                                                                                            displayAndAdapterInfo,
                                                                                            encoding_value)
                            if status is None:
                                continue
                            if status is False:
                                self.fail("Failed to set default encoding")
                            if status:
                                self.apply_supported_via_igcl(gfx_index, platform, pipe, transcoder,
                                                              color_model_set_via_default, displayAndAdapterInfo, False)

                            if requested_encoding is not None:
                                encoding_value = requested_encoding
                            status, color_model_set_via_default = self.default_set_encoding(gfx_index, platform,
                                                                                            pipe, transcoder,
                                                                                            encoding_value_list[
                                                                                                encoding_value],
                                                                                            displayAndAdapterInfo,
                                                                                            encoding_value)
                            if status is None:
                                continue
                            if status is False:
                                self.fail("Failed to set default encoding")
                            if status:
                                self.apply_supported_via_igcl(gfx_index, platform, pipe, transcoder,
                                                              color_model_set_via_default, displayAndAdapterInfo, False)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the bpc and encoding for the panel and verify")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)