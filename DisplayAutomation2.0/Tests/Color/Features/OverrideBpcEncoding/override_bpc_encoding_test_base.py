#################################################################################################
# @file         override_bpc_encoding_test_base.py
# @brief        This scripts comprises of below functions.
#               1.setUp() -  To apply the display config and update the custom tags.
#               2.tearDown() - To unplug the display and restore to default bpc and encoding.
#               3.enable_and_verify() - Will configure the bpc and pixel encoding and verify the registers
# @author       Vimalesh D
#################################################################################################
import sys
import time
import random
import ctypes
import unittest
import logging
import itertools

import DisplayRegs
from DisplayRegs.DisplayOffsets import TransDDiOffsetsValues
from Libs.Core import enum
from Libs.Core import cmd_parser, registry_access
from Libs.Core import enum, window_helper
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper.driver_escape_args import IGCCSupportedBpc, IGCCSupportedEncoding
from Tests.Color.Common import common_utility, color_properties, color_enums, csc_utility, color_mmio_interface, \
    color_igcl_escapes
from Libs.Core.display_power import PowerSource
from Tests.Color.Common import color_etl_utility
from Tests.Color.Common.common_utility import invoke_power_event, get_action_type
from Tests.Color.Common.color_enums import ConversionType, RgbQuantizationRange
from Tests.Color.Common.color_escapes import get_bpc_encoding, set_bpc_encoding
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding import verify, BpcEncoding
from Tests.Color.Verification import feature_basic_verify
from Tests.test_base import TestBase
from Libs.Core.logger import gdhm


##
# @brief - To perform setUp and tearDown functions
class OverrideBpcEncodingBase(TestBase):
    ##
    # A dictionary of all the properties related to the displays passed from command line
    # This dictionary have a tuple of gfx_index and connector_port_type as key
    # and the value contains tuple of  bpc and encoding BpcEncoding (Bpc='BPC_Value', Encoding='Encoding_Value')
    panel_props_dict = {}
    conv_type = None
    is_cea = True
    enable_regkey_dithering = False
    enable_igcl = False


    ##
    # @brief Unittest Setup function
    # @param[in] self
    # @return None
    def setUp(self):
        self.custom_tags["-BPC"] = None
        self.custom_tags["-ENCODING"] = None
        self.custom_tags['-ENABLE_REGKEY_DITHERING'] = False
        self.custom_tags['-ENABLE_IGCL'] = False
        super().setUp()
        self.bpc = str(self.context_args.test.cmd_params.test_custom_tags["-BPC"][0])
        self.encoding = str(self.context_args.test.cmd_params.test_custom_tags["-ENCODING"][0])
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        if len(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_REGKEY_DITHERING"][0]) > 1:
            self.enable_regkey_dithering = bool(
                self.context_args.test.cmd_params.test_custom_tags["-ENABLE_REGKEY_DITHERING"][0])
        else:
            self.enable_regkey_dithering = False
        if len(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_IGCL"][0]) > 1:
            self.enable_igcl = bool(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_IGCL"][0])
        else:
            self.enable_igcl = False

        if self.enable_regkey_dithering:
            for gfx_index, adapter in self.context_args.adapters.items():
                reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)

                key_name = "ForceDitheringEnable"
                value = 1
                if registry_access.write(args=reg_args, reg_name=key_name, reg_type=registry_access.RegDataType.DWORD,
                                         reg_value=value) is False:
                    self.fail("Registry key add to enable SelectBPC  failed")
                logging.info(" ForceDitheringEnable set to 1 on GFX_{0}".format(gfx_index))
                ##
                # restart display driver for regkey to take effect.
                status, reboot_required = common_utility.restart_display_driver(gfx_index)
                if status is False:
                    self.fail('Fail: Failed to Restart Display driver')

    ##
    # @brief         Wrapper to - configure bpc and encoding based on parameter and verify the register
    # @param[in]     gfx_index - gfx_0 or gfx_1
    # @param[in]     display_and_adapterInfo - display_and_adapter_info
    # @param[in]     pipe - pipe_info
    # @param[in]     transcoder - transcoder info
    # @param[in]     platform - platform Info
    # @param[in]     platform_type - LEGACY or YANGRA
    # @param[in]     is_lfp - True or False
    # @param[in]     port - PortType
    def enable_and_verify(self, gfx_index: str, displayAndAdapterInfo, pipe: str, transcoder: str, platform: str,
                          platform_type: str, port: str, is_lfp: bool, connector_port_type: str, escape="dd_escape",
                          requested_encoding=None):

        if self.enable_igcl:
            for index in range(0, 4):
                status = False
                encoding_value_list = ["RGB", "YCBCR420", "YCBCR422", "YCBCR444"]
                logging.info("Iteration:"+str(index))
                logging.info(encoding_value_list[index])
                status, color_model_set_via_default = self.default_set_encoding(gfx_index, platform,
                                                                                pipe, transcoder,
                                                                                encoding_value_list[index],
                                                                                displayAndAdapterInfo,
                                                                                index)
        else:
            Bpc_Encoding_caps = BpcEncoding()
            mmio_interface = color_mmio_interface.ColorMmioInterface()
            conv_type = ConversionType.FULL_TO_FULL
            status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(displayAndAdapterInfo,
                                                                                         platform_type)

            # Store the default bpc and encodng in panel dict
            Bpc_Encoding_caps.DefaultBpc = default_bpc
            Bpc_Encoding_caps.DefaultEncoding = default_encoding
            self.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps

            temp = False
            if status:
                for index in range(len(combo_bpc_encoding)):
                    bpc = str(combo_bpc_encoding[index][0])
                    encoding = str(default_encoding)
                    if bpc == self.bpc:
                        status = set_bpc_encoding(displayAndAdapterInfo, bpc, encoding, platform_type, is_lfp)
                        temp = True
                        break

                if temp is False:
                    random.shuffle(combo_bpc_encoding)
                    bpc = str(combo_bpc_encoding[0][0])
                    encoding = str(default_encoding)
                    status = set_bpc_encoding(displayAndAdapterInfo, bpc, encoding, platform_type, is_lfp)

            status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(displayAndAdapterInfo,
                                                                                         platform_type)

            bpc = None
            encoding = None
            quant_range = None
            temp = False
            if status:
                for index in range(len(combo_bpc_encoding)):
                    bpc = str(combo_bpc_encoding[index][0])
                    encoding = str(combo_bpc_encoding[index][1])

                    if bpc == self.bpc and encoding == self.encoding:

                        status = set_bpc_encoding(displayAndAdapterInfo, bpc, encoding, platform_type, is_lfp)
                        temp = True
                        break

                if temp is False:
                    random.shuffle(combo_bpc_encoding)
                    bpc = str(combo_bpc_encoding[0][0])
                    encoding = str(combo_bpc_encoding[0][1])
                    status = set_bpc_encoding(displayAndAdapterInfo, bpc, encoding, platform_type, is_lfp)

                ##
                # Wait for registers to take effect after setting the bpc and encoding

                if status:

                    if "HDMI" in connector_port_type:
                        # Check the previous color space before set escape and encoding applied in set escape
                        if self.panel_props_dict[gfx_index, port].DefaultEncoding == "RGB" and encoding == "RGB":
                            conv_type = ConversionType.FULL_TO_FULL
                            plane_id = color_etl_utility.get_plane_id(pipe, gfx_index)
                            output_range = csc_utility.get_output_range(gfx_index, platform, plane_id,
                                                                        pipe, transcoder, mmio_interface)
                            if output_range == color_enums.RgbQuantizationRange.LIMITED.value:
                                conv_type = ConversionType.FULL_TO_STUDIO
                        else:
                            conv_type = ConversionType.FULL_TO_STUDIO
                    plane_id = color_etl_utility.get_plane_id(pipe, gfx_index)
                    if verify(gfx_index, platform, pipe, plane_id, transcoder, bpc, encoding, conv_type):
                        # For persistence scenario commandline will have one value for BPC and Encoding
                        logging.info("Pass: Register verification for override BPC and Encodng")

                        # Update in panel context for bpc and encoding.
                        Bpc_Encoding_caps.Bpc = bpc
                        Bpc_Encoding_caps.Encoding = encoding
                        self.panel_props_dict[gfx_index, port] = Bpc_Encoding_caps
                    else:
                        self.fail("Fail: Failed to verify override bpc and encoding")
                else:
                    self.fail("Fail: Failed to set the override bpc and encoding")
            else:
                self.fail("Fail: Failed to get the override bpc and encoding")

    def default_set_encoding(self, gfx_index, platform, pipe, transcoder, color_model, display_and_adapterInfo, index):
        if common_utility.apply_mode(display_and_adapterInfo):
            argsGetSetWireFormat = color_igcl_escapes.get_wireformat_config(display_and_adapterInfo)
            bpc_mask_value_dict = {"BPC6": 0, "BPC8": 0, "BPC10": 0, "BPC12": 0}
            encoding_value_dict = {"RGB": 0, "YCBCR420": 0, "YCBCR422": 0, "YCBCR444": 0}
            bpc_mask = argsGetSetWireFormat.SupportedWireFormat[index].ColorDepth.value
            if bpc_mask == 0:
                logging.info("encoding_str"+str(color_model))
                logging.info("No Available bpc mask for encoding, returning in native resolution")
                return None, color_model
            encoding_str = color_enums.IgclColorModel(argsGetSetWireFormat.WireFormat.ColorModel.value).name
            # Get encoding_str index
            ##
            # Get mask value from bits
            # Based on mask , set bit value to do set_call:
            bit_index = 0
            for bpc, bit_value in bpc_mask_value_dict.items():
                mask_value = common_utility.get_bit_value(bpc_mask, bit_index, bit_index)
                logging.info(mask_value)
                if mask_value == 1:
                    bpc_mask_value_dict[bpc] = 1
                bit_index = bit_index + 1
            bit_index = 0
            for enc, bit_value in encoding_value_dict.items():
                if enc == color_model:
                    encoding_value_dict[enc] = 1
                bit_index = bit_index + 1

            bpc_mask_list = [i for i, j in bpc_mask_value_dict.items() if j == 1]
            encoding_mask_list = [i for i, j in encoding_value_dict.items() if j == 1]
            combo_bpc_encoding = list(itertools.product(bpc_mask_list, encoding_mask_list))
            logging.info("Combo bpc_encoding pair list %s" % combo_bpc_encoding)

            for index in range(len(combo_bpc_encoding)):
                bpc = str(combo_bpc_encoding[index][0])
                curr_encoding_str = str(combo_bpc_encoding[index][1])
                color_model = getattr(control_api_args.ctl_wire_format_color_depth_flags_v,curr_encoding_str).value
                color_depth= getattr(control_api_args.ctl_wire_format_color_model_v,bpc).value
                color_igcl_escapes.set_wireformat_config(color_model, color_depth, display_and_adapterInfo)
                plane_id = color_etl_utility.get_plane_id(pipe, gfx_index)

                if verify(gfx_index, platform, pipe, plane_id, transcoder, bpc, curr_encoding_str):
                    logging.info("Pass: Register verification for override BPC and Encodng")

        return True, color_model


    # For additional support - if need for explicit
    def apply_supported_via_igcl(self, gfx_index, platform, pipe, transcoder, color_model, display_and_adapterInfo,
                                 default_set):
        bpc_check_list = ["BPC6", "BPC8", "BPC10", "BPC12"]
        for index in range(0, len(bpc_check_list)):
            argsGetSetWireFormat = color_igcl_escapes.get_wireformat_config(display_and_adapterInfo)
            bpc_mask_value_dict = {"BPC6": 0, "BPC8": 0, "BPC10": 0, "BPC12": 0}
            encoding_value_dict = {"RGB": 0, "YCBCR420": 0, "YCBCR422": 0, "YCBCR444": 0}
            bpc_mask = argsGetSetWireFormat.SupportedWireFormat[index].ColorDepth.value
            encoding_str = color_enums.IgclColorModel(argsGetSetWireFormat.WireFormat.ColorModel.value).name
            if (encoding_str == color_model) and (bpc_mask != 0):
                ##
                # Get mask value from bits
                # Based on mask , set bit value to do set_call:
                bit_index = 0
                for bpc, bit_value in bpc_mask_value_dict.items():
                    mask_value = common_utility.get_bit_value(bpc_mask, bit_index, bit_index)
                    logging.info(mask_value)
                    if mask_value == 1:
                        bpc_mask_value_dict[bpc] = 1
                    bit_index = bit_index + 1
                print("bpc_mask_value_dict")
                bit_index = 0
                for enc, bit_value in encoding_value_dict.items():

                    if enc == encoding_str:
                        encoding_value_dict[enc] = 1
                    bit_index = bit_index + 1
                print("bpc_mask_value_dict")
                bpc_mask_list = [i for i, j in bpc_mask_value_dict.items() if j == 1]
                encoding_mask_list = [i for i, j in encoding_value_dict.items() if j == 1]
                combo_bpc_encoding = list(itertools.product(bpc_mask_list, encoding_mask_list))
                logging.info("Combo bpc_encoding pair list %s" % combo_bpc_encoding)

                for index in range(len(combo_bpc_encoding)):
                    bpc = str(combo_bpc_encoding[index][0])
                    encoding = str(combo_bpc_encoding[index][1])

                    color_igcl_escapes.set_wireformat_config(color_model, bpc, display_and_adapterInfo)

                    plane_id = color_etl_utility.get_plane_id(pipe, gfx_index)
                    # return True, color_model
                    if verify(gfx_index, platform, pipe, plane_id, transcoder, bpc, encoding):
                        # For persistence scenario commandline will have one value for BPC and Encoding
                        logging.info("Pass: Register verification for override BPC and Encodng")
                        #

    ##
    # @brief unittest TearDown function
    # @param[in] self
    # @return None
    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            if self.enable_regkey_dithering:
                if common_utility.write_registry(gfx_index=gfx_index, reg_name="ForceDitheringEnable",
                                                 reg_datatype=registry_access.RegDataType.DWORD, reg_value=0,
                                                 driver_restart_required=True) is False:
                    logging.error("Failed to enable ForceDitheringEnable registry key")
                    self.fail("Failed to disable ForceDitheringEnable registry key")
                logging.info("Registry key add to disable ForceDitheringEnable is successful")

        mmio_interface = color_mmio_interface.ColorMmioInterface()
        for gfx_index, adapter in self.context_args.adapters.items():
            panel_count = 0
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if self.enable_igcl:
                        argsGetSetWireFormat = control_api_args.ctl_get_set_wireformat()
                        argsGetSetWireFormat.Size = ctypes.sizeof(argsGetSetWireFormat)
                        argsGetSetWireFormat.Operation = control_api_args.ctl_wire_format_operation_type_v.CTL_RESTORE_DEFAULT.value
                        if control_api_wrapper.set_wireformat(argsGetSetWireFormat,
                                                              panel.display_and_adapterInfo) is False:
                            logging.info("Set BPC and Encoding to default")
                        else:
                            logging.info("Set BPC and Encoding to default")

                    else:
                        # If test initially failed, make default to BPC8 and RGB
                        if ((self.panel_props_dict[gfx_index, port].DefaultBpc != "") and
                                (self.panel_props_dict[gfx_index, port].DefaultEncoding != "")):
                            bpc = self.panel_props_dict[gfx_index, port].DefaultBpc
                            encoding = self.panel_props_dict[gfx_index, port].DefaultEncoding
                        else:
                            bpc = "BPC8"
                            encoding = "RGB"
                        panel_count += 1
                        if set_bpc_encoding(panel.display_and_adapterInfo, bpc, encoding, adapter.platform_type,
                                            panel.is_lfp):
                            # Need to check the logic for explicit quantization range
                            conv_type = ConversionType.FULL_TO_FULL
                            plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                            if "HDMI" in panel.connector_port_type:
                                output_range = csc_utility.get_output_range(adapter.gfx_index, adapter.platform,
                                                                            plane_id,
                                                                            panel.pipe, panel.transcoder,
                                                                            mmio_interface)
                                if output_range == color_enums.RgbQuantizationRange.LIMITED.value:
                                    conv_type = ConversionType.FULL_TO_STUDIO
                                else:
                                    conv_type = ConversionType.FULL_TO_FULL
                            if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id, panel.transcoder, bpc,
                                      encoding, conv_type):
                                logging.info("Pass: Register verification for override BPC and Encodng")
                            else:
                                self.fail("Fail: Failed to verify override bpc and encoding")
                        else:
                            self.fail("Fail: Failed to set the default bpc and encoding")

        super().tearDown()
