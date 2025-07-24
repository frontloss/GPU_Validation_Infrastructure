#################################################################################################
# @file         ycbcr_range_conversion.py
# @brief        This scripts comprises of basic test will perform below Scenarios
#               Ycbcr+Full range and ycbcr+ color model(601,709 and 2020)
#               1.test_01_color_model() - Will apply the mode and bpc will be set based on commandline
#               and  perform register verification for OCSC,Coeff,Pre/post off and quantization range
# @author       Vimalesh D
#################################################################################################
import json

from Libs.Core.display_power import PowerSource
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper.driver_escape_args import ColorModel
from Tests.Color.Common import common_utility, color_etl_utility
from Tests.Color.Common.color_enums import YuvSampling, ConversionType
from Tests.Color.Common.color_escapes import configure_aviinfo
from Tests.Color.Common.color_properties import FeatureCaps, update_ycbcr_caps_in_context
from Tests.Color.Features.Quantization.quantization_test_base import QuantizationTestBase
from Tests.Color.Features.YCbCr.ycbcr import enable_disable_ycbcr, verify
from Tests.Color.Features.YCbCr.ycbcr_test_base import YcbcrBase
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase
from Tests.test_base import *
from Tests.Color.Common.common_utility import get_modelist_subset, apply_mode, get_action_type
from Tests.Color.Verification import feature_basic_verify


##
# @brief - Ycbcr range conversion
class YcbcrRangeConversion(YcbcrBase,QuantizationTestBase):

    def setUp(self):
        self.custom_tags["-QUANTRANGE"] = ['DEFAULT', 'LIMITED', 'FULL']
        super().setUp()
        if str(self.context_args.test.cmd_params.test_custom_tags["-QUANTRANGE"][0]) is not None:
            self.set_range = (
                getattr(self.enum_quantization,
                        str(self.context_args.test.cmd_params.test_custom_tags["-QUANTRANGE"][0]))).value
        else:
            self.fail("Commandline error: Quantisation range should not be empty")

    ##
    # @brief         Wrapper to - configure avi infoframe and verify the register for ocsc, pre and post offsets and
    #                             quantization range
    # @param[in]     display_and_adapterInfo - display_and_adapter_info
    # @param[in]     platform - platform Info
    # @param[in]     pipe - pipe_info
    # @param[in]     plane - plane_info
    # @param[in]     transcoder - transcoder info
    # @param[in]     connector_port_type - HDMI or DP
    # @param[in]     configure_avi - True to configure and verify and False to perform only verify
    # @return        None
    def enable_disable_ycbcr_and_avi_info(self, display_and_adapterInfo,connector_port_type):


        # Enables YCbCr
        if enable_disable_ycbcr(connector_port_type, display_and_adapterInfo,True,YuvSampling.YUV444) is False:
            self.fail()

        # Enable Quantization

        self.expected_range = self.set_range

        if self.expected_range == self.enum_quantization.FULL.value:
            self.conv_type = ConversionType.FULL_TO_FULL
        if self.expected_range == self.enum_quantization.LIMITED.value:
            self.conv_type = ConversionType.FULL_TO_STUDIO

        if configure_aviinfo(connector_port_type,display_and_adapterInfo, self.set_range):
            logging.info("Successfully verified quantization range: {0} through escape".format(self.set_range))
        else:
            self.fail("verified quantization range: {0} through escape failed".format(self.set_range))


    ##
    # @brief        test_01_range_conversion() executes the test steps.
    # @return       None
    def runTest(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False and panel.connector_port_type != "VIRTUALDISPLAY":

                    self.enable_disable_ycbcr_and_avi_info(panel.display_and_adapterInfo, panel.connector_port_type)
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe, plane_id,
                              panel.transcoder, self.sampling, True, int(self.bpc),ColorModel.COLOR_MODEL_YCBCR_PREFERRED.value, self.conv_type) is False:
                        self.fail("Fail: Register verification for panel {0} on {1} failed ".format(panel.connector_port_type,
                                                                                                    gfx_index))

    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if configure_aviinfo(panel.connector_port_type,panel.display_and_adapterInfo, self.set_range):
                    logging.info("Successfully verified quantization range: {0} through escape".format(self.set_range))
                else:
                    self.fail("verified quantization range: {0} through escape failed".format(self.set_range))
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the ycbcr and quantization range and perform verification on all panels")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
