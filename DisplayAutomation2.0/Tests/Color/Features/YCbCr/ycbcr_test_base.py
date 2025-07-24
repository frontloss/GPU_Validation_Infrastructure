#################################################################################################
# @file         ycbcr_test_base.py
# @brief        This scripts comprises of below functions.
#               1.setUp() -  To apply the display config and update the feature caps based on panel capabilities
#               2.tearDown() - To unplug the display and restore to default for updated the feature caps
# @author       Vimalesh D
#################################################################################################
import logging
import sys
import unittest

from Tests.Color.Verification import feature_basic_verify
from Tests.test_base import TestBase
from Libs.Core import registry_access, window_helper
from Libs.Core.test_env.context import GfxDriverType
from Libs.Core.machine_info.machine_info import SystemInfo
from DisplayRegs.DisplayArgs import TranscoderType
from Tests.Color.Common import color_escapes, common_utility, color_enums, color_etl_utility
from Tests.Color.Common.color_enums import YuvSampling, SamplingMode
from Tests.Color.Features.YCbCr.ycbcr import verify, enable_disable_ycbcr
from Tests.Color.Common.color_properties import update_ycbcr_caps_in_context
from Libs.Core.logger import gdhm

##
# @brief get_action_type
# @param[in] None
# @return argument value
def get_action_type():
    tag_list = [custom_tag.strip().upper() for custom_tag in sys.argv]
    if '-SCENARIO' in tag_list:
        for i in range(0, len(tag_list)):
            if tag_list[i] == '-SCENARIO':
                if str(tag_list[i + 1]).startswith("-") is False:
                    return sys.argv[i + 1]
    else:
        assert False, "Wrong Commandline!! Usage: Test_name.py -SCENARIO SCENARIO_NAME -SAMPLING SAMPLING_TYPE"


##
# @brief - To perform setUp and tearDown functions
class YcbcrBase(TestBase):
    scenario = None
    sampling = None
    bpc = None

    ##
    # @brief Unittest Setup function
    # @param[in] self
    # @return None
    def setUp(self):
        ycbcr_panel_count = 0
        self.custom_tags["-SAMPLING"] = ['YUV420', 'YUV422', 'YUV444']
        self.custom_tags["-BPC"] = None
        super().setUp()
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        self.sampling = (getattr(YuvSampling, str(self.context_args.test.cmd_params.test_custom_tags["-SAMPLING"][0])))
        self.bpc = str(self.context_args.test.cmd_params.test_custom_tags["-BPC"][0])
        if self.sampling is None:
            self.fail("Wrong Commandline!! Usage: Test_name.py -SCENARIO SCENARIO_NAME -SAMPLING SAMPLING_TYPE")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                             self.context_args.adapters[gfx_index].panels[port])
                if panel.is_active and panel.FeatureCaps.YCbCrSupport and panel.is_lfp is False:
                    ycbcr_panel_count += 1

        if ycbcr_panel_count < 1:
            self.fail("Fail: None of the panel support ycbcr")

    ##
    # @brief Feature Enable and verify function
    # @param[in] self
    # @return None
    def enable_and_verify(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                    if self.bpc in [10, 12]:
                        bpc = "BPC12" if self.bpc == 12 else "BPC10"
                        if color_escapes.set_bpc_encoding(panel.display_and_adapterInfo, bpc, "RGB",
                                                          GfxDriverType.YANGRA, panel.is_lfp) is False:
                            self.fail(f"Fail: Failed to set the override bpc and encoding for {panel.target_id}")
                        if feature_basic_verify.verify_transcoder_bpc(adapter.gfx_index, adapter.platform,
                                                                      panel.transcoder, self.bpc) is False:
                            self.fail("Fail: Register verification for transcoder BPC failed")
                        logging.info("Pass: Register verification for BPC")
                    # Enables YCbCr
                    ycbcr_enable_status = enable_disable_ycbcr(port, panel.display_and_adapterInfo,
                                                               True, self.sampling)
                    if not ycbcr_enable_status:
                        self.fail("Failed to enable YCbCr")
                    else:
                        logging.info("Pass: Successfully enabled YCbCr")
                    ##
                    # Verify the registers
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe, plane_id,
                              panel.transcoder, self.sampling, True):
                        logging.info(
                            "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format(
                                panel.connector_port_type, adapter.gfx_index))
                    else:
                        self.fail("Register verification for YCbCr panel {0} on {1} failed".format(
                                panel.connector_port_type,
                                adapter.gfx_index))

    ##
    # @brief unittest TearDown function
    # @param[in] self
    # @return None
    def tearDown(self):
        ##
        # Disables YCbCr
        logging.info("Disabling YCbCr")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if self.sampling == color_enums.YuvSampling.YUV420:
                    ##
                    # Apply non-yuv420 mode
                    if common_utility.apply_mode(panel.display_and_adapterInfo,sampling_mode=SamplingMode.RGB.value):
                        logging.info("Applied NON-YUV420 mode")

                update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                             self.context_args.adapters[gfx_index].panels[port])

                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                    # Delete registry
                    if self.bpc in [10, 12]:
                        if color_escapes.set_bpc_encoding(panel.display_and_adapterInfo, "BPC8", "RGB",
                                                          GfxDriverType.YANGRA, panel.is_lfp) is False:
                            self.fail(f"Fail: Failed to set the override bpc and encoding for {panel.target_id}")
                    disable_status = enable_disable_ycbcr(port, panel.display_and_adapterInfo, False,
                                                          self.sampling)
                    if not disable_status:
                        self.fail("Failed to disable YCbCr")
                    else:
                        logging.info("Pass: Successfully disabled YCbCr")

                    if self.sampling == color_enums.YuvSampling.YUV422:
                        # TODO Need to be modify to delete registry once OS aware YUV422 enabled in IGCC
                        if common_utility.write_registry(gfx_index="GFX_0", reg_name="ForceApplyYUV422Mode",
                                                         reg_datatype=registry_access.RegDataType.DWORD, reg_value=0,
                                                         display_and_adapterInfo=panel.display_and_adapterInfo):
                            logging.info("PASS: Registry write to disable YUV422")
                        else:
                            logging.error("FAIL : Registry write to disable YUV422")

        super().tearDown()
