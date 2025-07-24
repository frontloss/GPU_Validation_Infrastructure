#################################################################################################
# @file         quantization_test_base.py
# @brief        This scripts comprises of below functions.
#               1.setUp() -  To apply the display config and update the feature caps based on panel capabilities
#               2.tearDown() - To unplug the display and restore to default for updated the feature caps
#               3.enable_and_verify() - Will configure the aviinfo and verify the registers
# @author       Vimalesh D
#################################################################################################
import os
import sys
import json
import logging
from Libs.Core import enum, window_helper
from Libs.Core.test_env import test_context
from Libs.Core.test_env.context import GfxDriverType
from DisplayRegs.DisplayArgs import TranscoderType
from Tests.Color.Common.color_enums import ConversionType
from Tests.test_base import TestBase
from Tests.Color.Common import color_etl_utility
from Tests.Color.Common import color_enums, common_utility, color_escapes
from Tests.Color.Common.color_escapes import configure_aviinfo
from Tests.Color.Features.Quantization.quantization import verify


##
# @brief get_action_type
# @param[in] None
# @return argument value
def get_action_type():
    tag_list = [custom_tag.strip().upper() for custom_tag in sys.argv]
    if '-SCENARIO' in tag_list and '-QUANTRANGE' in tag_list:
        for i in range(0, len(tag_list)):
            if tag_list[i] == '-SCENARIO':
                if str(tag_list[i + 1]).startswith("-") is False:
                    return sys.argv[i + 1]
    else:
        assert False, "Wrong Commandline!! Usage: Test_name.py -SCENARIO SCENARIO_NAME -QUANTRANGE QUANTISATION_RANGE"


##
# @brief - To perform setUp and tearDown functions
class QuantizationTestBase(TestBase):
    scenario = None
    set_range = None
    bpc = None
    expected_range = None
    conv_type = None
    is_cea = True
    enum_quantization = color_enums.RgbQuantizationRange

    ##
    # @brief Unittest Setup function
    # @param[in] self
    # @return None
    def setUp(self):

        self.custom_tags["-QUANTRANGE"] = ['DEFAULT', 'LIMITED', 'FULL']
        self.custom_tags["-BPC"] = None

        super().setUp()

        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        if str(self.context_args.test.cmd_params.test_custom_tags["-QUANTRANGE"][0]) is not None:
            self.set_range = (
                getattr(self.enum_quantization,
                        str(self.context_args.test.cmd_params.test_custom_tags["-QUANTRANGE"][0]))).value
        else:
            self.fail("Commandline error: Quantisation range should not be empty")
        self.bpc = int(self.context_args.test.cmd_params.test_custom_tags["-BPC"][0])

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
    def enable_and_verify(self, display_and_adapterInfo, platform, pipe, plane, transcoder,
                          connector_port_type, configure_avi: bool = False):
        gfx_index = display_and_adapterInfo.adapterInfo.gfxIndex
        self.get_expected_range(display_and_adapterInfo)

        if self.expected_range is None:
            logging.debug("Mode not found in JSON hence changing the range to be applied to limited")
            self.set_range = self.expected_range = self.enum_quantization.LIMITED.value

        if self.expected_range == self.enum_quantization.FULL.value:
            self.conv_type = ConversionType.FULL_TO_FULL
        if self.expected_range == self.enum_quantization.LIMITED.value:
            self.conv_type = ConversionType.FULL_TO_STUDIO

        if configure_avi:
            if configure_aviinfo(connector_port_type, display_and_adapterInfo, self.set_range):
                logging.info("Successfully verified quantization range: {0} through escape".format(self.set_range))
            else:
                self.fail("verified quantization range: {0} through escape failed".format(self.set_range))

        if verify(gfx_index, platform, pipe, plane, transcoder, self.bpc, self.conv_type, self.expected_range):
            logging.info(
                "Pass: Register verification for quantization range {0} on {1} panel on {2} passed".format(
                    self.set_range, connector_port_type, gfx_index))
        else:
            self.fail("Fail: Register verification for panel {0} on {1} failed ".format(connector_port_type, gfx_index))

    ##
    # @brief         Wrapper to get expected range from the function if the quantization range to set is DEFAULT.
    # @param[in]     display_and_adapterInfo - display_and_adapter_info
    # @return        None
    def get_expected_range(self, display_and_adapterInfo):
        quant_range = None

        if self.set_range != self.enum_quantization.DEFAULT.value:
            self.expected_range = self.set_range
            return
        else:
            input_json_path = os.path.join(test_context.ROOT_FOLDER,
                                           "Tests\\Color\\Features\\Quantization\\modes_timing_info.json")
            with open(input_json_path) as f:
                quantization_mode_data = json.load(f)
            mode = self.config.get_current_mode(display_and_adapterInfo)
            for index in range(0, len(quantization_mode_data)):
                if mode.HzRes == quantization_mode_data[index]["HzRes"] and mode.VtRes == quantization_mode_data[index][
                    "VtRes"] and mode.scaling == enum.MDS and mode.refreshRate == quantization_mode_data[index]["RR"]:
                    if self.set_range == self.enum_quantization.DEFAULT.value:
                        quant_range = self.enum_quantization.LIMITED.value if quantization_mode_data[index][
                            "isCEA"] else self.enum_quantization.FULL.value
                        break
            self.expected_range = quant_range
        return self.expected_range

    ##
    # @brief unittest TearDown function
    # @param[in] self
    # @return None
    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False:
                    if self.bpc in [10, 12]:
                        if color_escapes.set_bpc_encoding(panel.display_and_adapterInfo, "BPC8", "RGB",
                                                          GfxDriverType.YANGRA, panel.is_lfp) is False:
                            self.fail(f"Fail: Failed to set the override bpc and encoding for {panel.target_id}")
                    if not configure_aviinfo(panel.connector_port_type, panel.display_and_adapterInfo,
                                             self.enum_quantization.DEFAULT.value):
                        self.fail("verified quantization range: {0} through escape failed".format(self.set_range))
        super().tearDown()
