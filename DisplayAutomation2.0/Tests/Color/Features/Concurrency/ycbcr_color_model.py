#################################################################################################
# @file         ycbcr_color_model.py
# @brief        This scripts comprises of basic test will perform below Scenarios
#               Ycbcr+Full range and ycbcr+ color model(601,709 and 2020)
#               1.test_01_color_model() - Will apply the mode and bpc will be set based on commandline
#               and  perform register verification for OCSC,Coeff,Pre/post off and quantization range
# @author       Vimalesh D
#################################################################################################
import json

from Libs.Core import display_power
import DisplayRegs
from DisplayRegs.DisplayOffsets import TransDDiOffsetsValues
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper.driver_escape_args import ColorModel
from Tests.Color.Common import common_utility, color_enums, color_properties, color_mmio_interface
from Tests.Color.Common.color_enums import ConversionType, YuvSampling
from Tests.Color.Common.color_escapes import configure_aviinfo
from Tests.Color.Common.color_properties import FeatureCaps
from Tests.Color.Common import color_etl_utility
from Tests.Color.Features.YCbCr.ycbcr import enable_disable_ycbcr, verify
from Tests.Color.Features.YCbCr.ycbcr_test_base import YcbcrBase
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase
from Tests.test_base import *
from Tests.Color.Common.common_utility import get_modelist_subset, apply_mode, get_action_type
from Tests.Color.Verification import feature_basic_verify


##
# @brief - Ycbcr color model
class YcbcrColorModel(YcbcrBase):

    def setUp(self):
        self.custom_tags["-COLOR_MODEL"] = None
        self.custom_tags["-HDR"] = None
        super().setUp()
        self.hdr = self.context_args.test.cmd_params.test_custom_tags["-HDR"][0]
        self.color_model = getattr(ColorModel,
                                   str(self.context_args.test.cmd_params.test_custom_tags["-COLOR_MODEL"][0])).value
        if self.hdr == "ENABLE":
            if self.color_model != ColorModel.COLOR_MODEL_YCBCR_2020.value:
                self.fail()

    ##
    # @brief        test_01_color_model() executes the test steps.
    # @return       None
    def runTest(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                # Check virtual display incase single display hotplug-unplug scenario
                if panel.is_active and panel.is_lfp is False and panel.connector_port_type != "VIRTUALDISPLAY":
                    bpc_dict = {0: "BPC8", 1: "BPC10", 2: "BPC6", 3: "BPC12"}
                    regs = DisplayRegs.get_interface(adapter.platform, gfx_index)
                    # HDR to support color model 2020
                    if self.hdr == "ENABLE":

                        feature_caps = FeatureCaps()
                        feature_caps.HDRSupport = True
                        setattr(self.context_args.adapters[gfx_index].panels[port], "FeatureCaps", feature_caps)

                        # Verify if the Power Mode is in DC and switch to AC
                        # This is to override the OS Policy to disable HDR
                        # when running Windows HD Color content on battery Power for battery optimization
                        status = common_utility.apply_power_mode(display_power.PowerSource.AC)
                        if status is False:
                            self.fail()

                        ##
                        # Enable the HDR
                        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
                            self.fail()


                    # Enables YCbCr
                    if enable_disable_ycbcr(panel.connector_port_type, panel.display_and_adapterInfo, True, YuvSampling.YUV444,
                                            self.color_model) is False:
                        self.fail()

                    transcoder = DisplayRegs.DisplayRegsInterface.TranscoderType(panel.transcoder).name
                    trans_ddi_func_offset = regs.get_trans_ddi_offsets(transcoder)
                    data = color_mmio_interface.ColorMmioInterface().read(gfx_index, trans_ddi_func_offset.FuncCtrlReg)
                    trans_ddi_value = regs.get_trans_ddi_info(transcoder, TransDDiOffsetsValues(FuncCtrlReg=data))

                    ##
                    # Compare transcoder BPC and Expected BPC
                    # As regkey way to apply select bpc got removed, there is chance of appyling different bpc based on
                    # capable so fetching the current bpc and update the same.
                    self.bpc = bpc_dict[trans_ddi_value.BitsPerColor].split("BPC")[1]

                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe, plane_id,
                              panel.transcoder, self.sampling, True, int(self.bpc), self.color_model) is False:
                        self.fail("Fail: Register verification for panel {0} on {1} failed ".format(panel.connector_port_type,
                                                                                                gfx_index))
        ##
        # Disable the HDR
        if self.hdr == "ENABLE":
            if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
                self.fail()

    ##
    # If the test enables HDR and fails in between, then HDR has to be disabled
    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe):
                    if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
                        self.fail()

        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the ycbcr and quantization range and perform verification on all panels")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
