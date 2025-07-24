#################################################################################################
# @file         override_bpc_encoding_basic.py
# @brief        This is a custom script which can used to display configurations with supported bpc and encoding
#               will perform below functionalities
#               1.To configure bpc and encoding through escape
#               2.To perform register verification for bpc and encoding
# @author       Vimalesh D
#################################################################################################
import time
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding_test_base import *


##
# @brief - To perform basic verification with all supported BPC and Encoding
class OverrideBpcEncoding(OverrideBpcEncodingBase):
    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    @unittest.skipIf(get_action_type() != "BASIC", "Skip the  test step as the action type is not basic")
    def test_01_basic(self):
        mmio_interface = color_mmio_interface.ColorMmioInterface()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if self.enable_igcl:
                        self.enable_and_verify(adapter.gfx_index,panel.display_and_adapterInfo,panel.pipe, panel.transcoder
                                               ,adapter.platform, adapter.platform_type,port,panel.is_lfp,panel.connector_port_type)
                    else:
                        Bpc_Encoding_caps = BpcEncoding()
                        default_bpc_list = []
                        # For panel supported BPC. set each BPC with default encoding to get the Mask value correctly
                        status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(panel.display_and_adapterInfo, adapter.platform_type)
                        Bpc_Encoding_caps.DefaultBpc = default_bpc
                        Bpc_Encoding_caps.Encoding = default_encoding
                        Bpc_Encoding_caps.DefaultEncoding = default_encoding
                        self.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps
                        if status:
                            for index in range(len(combo_bpc_encoding)):
                                bpc = str(combo_bpc_encoding[index][0])
                                default_bpc_list.append(bpc)

                            # remove duplicates in list, keep only unique as BPC8,BPC10,BPC12
                            default_bpc_lists = list(set(default_bpc_list))
                            for iterate_default_bpc in default_bpc_lists:
                                status = set_bpc_encoding(panel.display_and_adapterInfo, iterate_default_bpc,
                                                          default_encoding,adapter.platform_type, panel.is_lfp)
                                if status:
                                    logging.info("Bpc and default encoding set successfully")
                                    # Here the for mask value will get via escape for current bpc with default encoding
                                    # For Example: For SamsungJS9500_HDR panel, BPC10 as current BPC and RGBas default encoding.
                                    # get call() will return  the combination of pairs will be(BPC10,RGB)(BPC10,YCBCR444)
                                    # and during iteration it will set one by one pair accordingly.
                                    status, combo_bpc_encoding, default_bpc, default_encoding = \
                                        get_bpc_encoding(panel.display_and_adapterInfo, adapter.platform_type)
                                    # Update the current default encoding
                                    Bpc_Encoding_caps.Bpc = default_bpc
                                    # To set the current encoding
                                    Bpc_Encoding_caps.Encoding = default_encoding
                                    # For Usage of Default Encoding in teardown place
                                    Bpc_Encoding_caps.default_encoding = default_encoding
                                    self.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

                                    if status:
                                        for index in range(len(combo_bpc_encoding)):
                                            bpc = str(combo_bpc_encoding[index][0])
                                            encoding = str(combo_bpc_encoding[index][1])
                                            if bpc == iterate_default_bpc:
                                                status = set_bpc_encoding(panel.display_and_adapterInfo, bpc, encoding,
                                                                          adapter.platform_type,panel.is_lfp)
                                                conv_type = ConversionType.FULL_TO_FULL
                                                if "HDMI" in panel.connector_port_type:
                                                    # Check the previous color space before set escape and encoding applied in set escape
                                                    if self.panel_props_dict[adapter.gfx_index, panel.connector_port_type].Encoding == "RGB" and encoding == "RGB":
                                                        conv_type = ConversionType.FULL_TO_FULL
                                                        plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                                                        output_range = csc_utility.get_output_range(adapter.gfx_index,
                                                                                                    adapter.platform, plane_id,
                                                                                                    panel.pipe,
                                                                                                    panel.transcoder,
                                                                                                    mmio_interface)
                                                        if output_range == color_enums.RgbQuantizationRange.LIMITED.value:
                                                            conv_type = ConversionType.FULL_TO_STUDIO
                                                    else:
                                                        conv_type = ConversionType.FULL_TO_STUDIO
                                                if status:
                                                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                                                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id,
                                                              panel.transcoder,bpc,encoding, conv_type) is False:
                                                        self.fail("Fail: Failed to verify the override bpc and encoding")
                                                    else:
                                                        # Update the current Encoding for to compute the conv type
                                                        Bpc_Encoding_caps.Encoding = encoding
                                                        self.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps
                                                else:
                                                    self.fail("Fail: Failed to set the override bpc and encoding")
                                    else:
                                        self.fail("Fail: Failed to get the override bpc and encoding")
                                else:
                                    self.fail("Fail: Failed to set the override bpc and encoding")
                        else:
                            self.fail("Fail: Failed to get the override bpc and encoding")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the bpc and encoding for the panel and verify")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)