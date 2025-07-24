######################################################################################################
# @file         hdr_utility.py
# @brief        Contains all the helper functions and the utilities used by DFT and E2E HDR tests
#               in both SDR and HDR modes
#               Functions present in this wrapper :
#               1.set_b3_slider_and_fetch_b3_info()
#               2.get_hdr_static_metadata()
#               3.parse_and_rearrange_prog_metadata
#               4.fetch_programmed_metadata
#               5.rearrange_default_metadata
# @author       Smitha B
######################################################################################################
import time
import logging, math
from dataclasses import dataclass, field
from typing import List
import DisplayRegs
from typing import Union
from Libs.Core import etl_parser
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Libs.Core.logger import gdhm
from Tests.Color.Common import color_etl_utility, common_utility, color_escapes, color_igcl_escapes, color_igcl_wrapper
from Tests.Color.Common import color_constants, color_properties, color_mmio_interface, color_enums
from Tests.Color.Verification import feature_basic_verify

@dataclass
class E2EPipeArgs:
    dglut_curve_type: str = None
    glut_curve_type: str = None
    is_smooth_brightness: bool = False
    step_index: int = 0
    pixel_boost: int = 1
    escape_dglut: List = field(default_factory=list)
    escape_csc: List = field(default_factory=list)
    escape_correction_glut: List = field(default_factory=list)
    escape_ocsc: List = field(default_factory=list)
    os_relative_lut: List = field(default_factory=list)
    os_relative_csc: List = field(default_factory=list)
    dsb_gamma_dump: List = field(default_factory=list)
    default_metadata: color_properties.OSHdrMetadata = None
    flip_metadata: color_properties.OSHdrMetadata = None
    desired_max_cll: int = 0
    desired_max_fall: int = 0
    bpc: int = 8


@dataclass
class DFTPipeArgs:
    reference_metadata: List = field(default_factory=list)
    panel_caps: color_enums.PanelCaps = None


@dataclass
class PlaneArgs:
    color_space: color_enums.ColorSpace
    pixel_format: int = 0
    gamma: int = 0
    gamut: str = ""
    range: str = ""

def fetch_enabled_mode(gfx_index, platform, pipe):
    feature = color_enums.ColorMode.SDR.value
    if feature_basic_verify.hdr_status(gfx_index, platform, pipe):
        feature = color_enums.ColorMode.HDR.value
    else:
        pass
        ##
        # ToDo : Add the capability for WCG
        # panel.FeatureCaps.WCGSupport = True
        # feature = "WCG"
    return feature


##
# Interface used by the test cases to Set the Brightness Slider level.
# The function invokes the respective ETL parsing functions for each of the components
# (OSRelativeLUT, Brightness, SDRWhiteLevel)
# Invokes the function to generate reference LUT, Programmed LUT and performs verification.
# Function returns the result, brightness_val_in_context, sdr_white_level_in_context, os_relative_lut_in_context
def set_b3_slider_and_fetch_b3_info(target_id, brightness_level, panel_props):
    panel_props.b3_value = 0
    panel_props.pixel_boost = 1
    ##
    # Set the OS Brightness Slider to the level iterating through the list
    if common_utility.set_os_brightness(brightness_level, delay=0) is False:
        return False

    ##
    # Due to smooth brightness, the brightness change will be applied in phases
    # depending on the Transition time and the active RR.
    # Currently OS is giving the Transition time as 200ms, hence waiting with a buffer added to it as 500ms
    time.sleep(0.005)

    brightness_level = "Setting_Brightness_level_to_" + str(brightness_level) + "_" + "TimeStamp_"
    brightness_file_path = color_etl_utility.stop_etl_capture(brightness_level)

    if etl_parser.generate_report(brightness_file_path) is False:
        logging.error("\tFailed to generate EtlParser report")
        return False
    else:
        ##
        # Start the ETL again for capturing other events
        if color_etl_utility.start_etl_capture() is False:
            logging.error("Failed to Start Gfx Tracer")
            return False

        ##
        # Fetch the OSOneDLUT after enabling HDR for a HDR supported panel
        os_relative_lut_after_b3 = color_etl_utility.get_os_one_d_lut_from_etl(target_id)
        if os_relative_lut_after_b3.__len__() == 0:
            logging.info("No new OS OneDLUT from OS after setting the Brightness Slider")
            logging.info("Considering the OSOneDLUT already available in the context")
            if panel_props.os_relative_lut.__len__() == 0:
                metadata_scenario = color_properties.HDRMetadataScenario()
                if metadata_scenario.reboot == 1:
                    # TO-DO update condition based on OS Provided LUT if changed.
                    logging.error("OSOneDLUT is not available in the context and no new OS OneDLUT is available")
                    gdhm.report_driver_bug_os(title="OSOneDLUT is not available in the context" ,priority="p3-medium", exposure="3-medium")
                return False
        else:
            logging.info("OS has issued new OSOneDLUT, hence overriding the LUT available in context")
            panel_props.os_relative_lut = os_relative_lut_after_b3[-1]

        # #
        # Note : Currently there are no APIs to set the SDRWhiteLevel Slider.
        #        Hence considering only the default value given by OS.
        sdr_white_level_in_nits = color_etl_utility.get_sdr_white_level_from_etl(target_id)
        if sdr_white_level_in_nits < 0:
            return False
        logging.info("SDRWhiteLevel is %s" % sdr_white_level_in_nits)
        panel_props.sdr_white_level = sdr_white_level_in_nits

        brightness_val_in_nits, transition_time_in_milli_nits = color_etl_utility.get_brightness3_in_nits_and_transition_time_from_etl(target_id)
        if brightness_val_in_nits < 0:
            return False
        else:
            logging.info("BrightnessValueInNits is %s" % brightness_val_in_nits)
            panel_props.b3_value = brightness_val_in_nits
            panel_props.b3_transition_time = transition_time_in_milli_nits / 1000
        panel_props.pixel_boost = panel_props.b3_value / panel_props.sdr_white_level

        ##
        # Fetch the Default Metadata from the ETL for the particular target-id
        status, default_metadata = color_etl_utility.get_default_hdr_metadata_from_etl(target_id)
        if status is False:
            logging.info("No new Default Metadata issued by OS")
            logging.info("Considering the Default Metadata already available in the context")
        else:
            ##
            # Take the latest Default Metadata from the list of metadata available
            panel_props.default_metadata = default_metadata[-1]

        ##
        # Fetch the Flip Metadata from the ETL for the particular target-id
        status, flip_metadata = color_etl_utility.get_flip_hdr_metadata_from_etl(target_id)
        if status is False:
            logging.info("No new Flip Metadata issued by OS")
            logging.info("Considering the Flip Metadata already available in the context")
        else:
            panel_props.flip_metadata = flip_metadata

    return True


##
# Parse the programmed metadata and re-arrange according to reference metadata
def parse_and_rearrange_prog_metadata(display, programmed_metadata, pcon=False):
    meta_data = []
    if display[:4] == 'HDMI':
        meta_data = [common_utility.get_bit_value(programmed_metadata[1], 8, 9),  # EOTF
                     (common_utility.get_bit_value(programmed_metadata[2], 0, 7) << 8) |
                     common_utility.get_bit_value(programmed_metadata[1], 24, 31),  # GreenPrimaries_0
                     common_utility.get_bit_value(programmed_metadata[2], 8, 23),  # GreenPrimaries_1

                     (common_utility.get_bit_value(programmed_metadata[3], 0, 7) << 8) |
                     common_utility.get_bit_value(programmed_metadata[2], 24, 31),  # Blue_0
                     common_utility.get_bit_value(programmed_metadata[3], 8, 23),  # Blue_1

                     (common_utility.get_bit_value(programmed_metadata[4], 0, 7) << 8) |
                     common_utility.get_bit_value(programmed_metadata[3], 24, 31),  # Red_0
                     common_utility.get_bit_value(programmed_metadata[4], 8, 23),  # Red_1

                     (common_utility.get_bit_value(programmed_metadata[5], 0, 7) << 8) |
                     common_utility.get_bit_value(programmed_metadata[4], 24, 31),  # WhitePoint_X
                     common_utility.get_bit_value(programmed_metadata[5], 8, 23),  # WhitePoint_Y

                     (common_utility.get_bit_value(programmed_metadata[6], 0, 7) << 8) |
                     common_utility.get_bit_value(programmed_metadata[5], 24, 31),  # MaxMasteringLuminance
                     common_utility.get_bit_value(programmed_metadata[6], 8, 23),  # MinMasteringLuminance
                     (common_utility.get_bit_value(programmed_metadata[7], 0, 7) << 8) |
                     common_utility.get_bit_value(programmed_metadata[6], 24, 31),  # MaxCLL
                     common_utility.get_bit_value(programmed_metadata[7], 8, 23),  # MaxFALL
                     ]

    elif display[:2] == 'DP' or pcon:
        meta_data = [
            common_utility.get_bit_value(programmed_metadata[1], 16, 17),
            common_utility.get_bit_value(programmed_metadata[2], 0, 15),
            common_utility.get_bit_value(programmed_metadata[2], 16, 31),
            common_utility.get_bit_value(programmed_metadata[3], 0, 15),
            common_utility.get_bit_value(programmed_metadata[3], 16, 31),
            common_utility.get_bit_value(programmed_metadata[4], 0, 15),
            common_utility.get_bit_value(programmed_metadata[4], 16, 31),
            common_utility.get_bit_value(programmed_metadata[5], 0, 15),
            common_utility.get_bit_value(programmed_metadata[5], 16, 31),
            common_utility.get_bit_value(programmed_metadata[6], 0, 15),
            common_utility.get_bit_value(programmed_metadata[6], 16, 31),
            common_utility.get_bit_value(programmed_metadata[7], 0, 15),
            common_utility.get_bit_value(programmed_metadata[7], 16, 31)
        ]
    logging.debug("After parsing and re-arranging the metadata %s" % meta_data)
    return meta_data


##
# Perform register level verification for Metadata
def fetch_programmed_metadata(gfx_index, platform, display, is_lfp, current_pipe, pcon=False):
    programmed_metadata = []
    import DisplayRegs

    regs = DisplayRegs.get_interface(platform, gfx_index)

    if display[:4] == 'HDMI':
        base_offset = regs.get_hdr_metadata_offsets("0", current_pipe).VideoDipDRMData
        for index in range(0, color_constants.METADATA_LENGTH):
            programmed_metadata.append(color_mmio_interface.ColorMmioInterface().read(gfx_index, base_offset))
            base_offset += 4

    ##
    # According to the new DIP Policy, for DP below is the logic
    if display[:2] == 'DP' or pcon:
        if pcon:
            ##
            # Proceed to reset the 31st bit, VSC extension SDP metadata enable
            # and then reset the 14th bit, Auto Incremement bit before reading the Data register
            vsc_ext_sdp_ctl_reg_offset = regs.get_hdr_metadata_offsets("0", current_pipe).VscExtSdpCtl
            vsc_sdp_ctrl_value = color_mmio_interface.ColorMmioInterface().read(gfx_index, vsc_ext_sdp_ctl_reg_offset)
            color_mmio_interface.ColorMmioInterface().write(gfx_index, vsc_ext_sdp_ctl_reg_offset,
                                                            vsc_sdp_ctrl_value & 0x7fffbfff)

            vsc_sdp_ctrl_value = color_mmio_interface.ColorMmioInterface().read(gfx_index, vsc_ext_sdp_ctl_reg_offset)
            logging.debug("After setting 31st bit to 0 in VSC SDP Control Value {0}".format(vsc_sdp_ctrl_value))
            poll_index = 0
            while True:
                if poll_index > 50:
                    logging.error("Completed Polling for the Buffer Empty for more than 50 times")
                    logging.error("Aborting the test")
                    logging.error("Poll Index is {0}".format(poll_index))
                    return []
                vsc_sdp_ctrl_value = color_mmio_interface.ColorMmioInterface().read(gfx_index, vsc_ext_sdp_ctl_reg_offset)
                buffer_empty = common_utility.get_bit_value(vsc_sdp_ctrl_value, 24, 24)
                if buffer_empty == 0:
                    break
                poll_index += 1

            base_offset = regs.get_hdr_metadata_offsets("0", current_pipe).VscExtSdpData
            for index in range(0, color_constants.METADATA_LENGTH):
                programmed_metadata.append(color_mmio_interface.ColorMmioInterface().read(gfx_index, base_offset))
        else:
            base_offset = regs.get_hdr_metadata_offsets("0", current_pipe).VideoDipGMPData
            for index in range(0, color_constants.METADATA_LENGTH):
                programmed_metadata.append(color_mmio_interface.ColorMmioInterface().read(gfx_index, base_offset))
                base_offset += 4

    return parse_and_rearrange_prog_metadata(display, programmed_metadata, pcon)


def rearrange_default_metadata(default_metadata: color_properties.HDRStaticMetadata):
    rearranged_metadata = [default_metadata.EOTF, default_metadata.DisplayPrimariesX0, default_metadata.DisplayPrimariesY0,
                           default_metadata.DisplayPrimariesX1, default_metadata.DisplayPrimariesY1,
                           default_metadata.DisplayPrimariesX2, default_metadata.DisplayPrimariesY2,
                           default_metadata.WhitePointX, default_metadata.WhitePointY,
                           round(default_metadata.MaxLuminance / 1000), default_metadata.MinLuminance * 10,
                           round(default_metadata.MaxCLL / 1000), round(default_metadata.MaxFALL / 1000)]
    return rearranged_metadata


##
# Verification of the default and flip metadata from the ETL
def verify_default_and_flip_metadata_from_etl(default_metadata, flip_metadata):
    # If type is None, Driver should program Default Metadata
    for index in range(0, len(flip_metadata)):
            if flip_metadata[index].hdr_metadata_type in ("DEFAULT", "NONE"):
                temp = [flip_metadata[index].programmed_metadata.EOTF,
                        flip_metadata[index].programmed_metadata.DisplayPrimariesX0,
                        flip_metadata[index].programmed_metadata.DisplayPrimariesX1,
                        flip_metadata[index].programmed_metadata.DisplayPrimariesX2,
                        flip_metadata[index].programmed_metadata.DisplayPrimariesY0,
                        flip_metadata[index].programmed_metadata.DisplayPrimariesY1,
                        flip_metadata[index].programmed_metadata.DisplayPrimariesY2,
                        flip_metadata[index].programmed_metadata.WhitePointX,
                        flip_metadata[index].programmed_metadata.WhitePointY,
                        flip_metadata[index].programmed_metadata.MaxLuminance,
                        flip_metadata[index].programmed_metadata.MinLuminance,
                        flip_metadata[index].programmed_metadata.MaxCLL,
                        flip_metadata[index].programmed_metadata.MaxFALL]
                if all(v == 0 for v in temp) is False:
                    logging.error(
                        "FAIL : Flip Metadata Type is {0}, Flip Metadata is not matching with Default Metadata"
                        .format(flip_metadata[index].hdr_metadata_type))
                    return False
            else:
                if default_metadata.programmed_metadata != flip_metadata[index].programmed_metadata:
                    logging.error("FAIL : Flip Metadata and Default Metadata are not matching")
                    return False
    ##
    # If type is HDR10, then compare Default and Flip
    logging.info("Default and Flip Metadata are matching")
    return True


##
# Fetch and verify pixel encoding for HDR modes
def verify_pixel_encoding(gfx_index: str, platform: str, plane: str, pipe: str, expected_pixel_encoding: int) -> bool:
    regs = DisplayRegs.get_interface(platform, gfx_index)
    avi_dip_offsets = regs.get_avi_info_offsets(plane, pipe)
    avi_dip_data = color_mmio_interface.ColorMmioInterface().read(gfx_index, avi_dip_offsets.QuantRange)

    prog_pixel_encoding = common_utility.get_bit_value(avi_dip_data, 13, 15)

    if prog_pixel_encoding != expected_pixel_encoding:
        logging.error(
            "FAIL : Pixel Encoding on Adapter:{0} Pipe:{1} Expected : {2} and Actual : {3}".format(gfx_index, pipe,
                                                                                               color_enums.PixelEncoding(expected_pixel_encoding).name,
                                                                                               color_enums.PixelEncoding(prog_pixel_encoding).name))
        gdhm.report_driver_bug_os("Verification of Pixel Encoding failed on Adapter:{0} Pipe:{1} Expected : {2} and Actual : {3}".format(gfx_index, pipe,
                                                                                           color_enums.PixelEncoding(expected_pixel_encoding).name,
                                                                                           color_enums.PixelEncoding(prog_pixel_encoding).name))
        return False
    logging.info(
        "PASS : Pixel Encoding on Adapter:{0} Pipe:{1} Expected : {2} and Actual : {3}".format(gfx_index, pipe,
                                                                                           color_enums.PixelEncoding(expected_pixel_encoding).name,
                                                                                           color_enums.PixelEncoding(prog_pixel_encoding).name))
    return True


##
# Fetch and verify pixel encoding for HDR modes
def verify_colorimetry(gfx_index: str, platform: str, plane: str, pipe: str, pixel_encoding: int) -> bool:
    regs = DisplayRegs.get_interface(platform, gfx_index)
    avi_dip_offsets = regs.get_avi_info_offsets(plane, pipe)
    avi_dip_data = color_mmio_interface.ColorMmioInterface().read(gfx_index, avi_dip_offsets.QuantRange)
    prog_colorimetry = common_utility.get_bit_value(avi_dip_data, 0, 3)
    is_hdr_enabled = feature_basic_verify.hdr_status(gfx_index, platform, pipe)
    if pixel_encoding == color_enums.PixelEncoding.RGB.value:
        if is_hdr_enabled:
            if color_enums.ColorimetryRGB(prog_colorimetry).name not in color_enums.ColorimetryRGB.ITU_R_BT2020_RGB.name:
                logging.error("FAIL : Colorimetry Info on Adapter : {0} Pipe : {1} Expected:{2} and Actual:{3}".format(gfx_index, pipe,
                                                                                                     color_enums.ColorimetryRGB.ITU_R_BT2020_RGB.name,
                                                                                                     prog_colorimetry))
                return False
            logging.info(
                "PASS : Colorimetry Info on Adapter:{0} Pipe:{1} Expected:{2} and Actual:{3}".format(gfx_index, pipe,
                                                                                                     color_enums.ColorimetryRGB.ITU_R_BT2020_RGB.name,
                                                                                                     prog_colorimetry))

        else:
            if color_enums.ColorimetryRGB(prog_colorimetry).name not in color_enums.ColorimetryRGB.sRGB.name:
                logging.info("FAIL : Colorimetry Info on Adapter:{0} Pipe:{1} Expected:{2} and Actual:{3}".format(gfx_index, pipe,
                                                                                                     color_enums.ColorimetryRGB.sRGB.name,
                                                                                                     prog_colorimetry))
                return False
            logging.info(
                "PASS : Colorimetry Info on Adapter:{0} Pipe:{1} Expected:{2} and Actual:{3}".format(gfx_index, pipe,
                                                                                                     color_enums.ColorimetryRGB.sRGB.name,
                                                                                                     prog_colorimetry))
    else:
        if is_hdr_enabled:
            if color_enums.ColorimetryYUV(prog_colorimetry).name not in color_enums.ColorimetryYUV.ITU_R_BT2020_Y_C_BC_R:
                logging.error(
                    "FAIL : Colorimetry Info on Adapter : {0} Pipe : {1} Expected:{2} and Actual:{3}".format(gfx_index,
                                                                                                             pipe,
                                                                                                             color_enums.ColorimetryYUV.ITU_R_BT2020_Y_C_BC_R.name,
                                                                                                             prog_colorimetry))
                return False
            logging.info(
                "PASS : Colorimetry Info on Adapter:{0} Pipe:{1} Expected:{2} and Actual:{3}".format(gfx_index, pipe,
                                                                                                     color_enums.ColorimetryYUV.ITU_R_BT2020_Y_C_BC_R.name,
                                                                                                     prog_colorimetry))

        else:
            if color_enums.ColorimetryYUV(prog_colorimetry).name not in color_enums.ColorimetryYUV.ITU_R_BT709.name:
                logging.error("FAIL : Colorimetry Info on Adapter:{0} Pipe:{1} Expected:{2} and Actual:{3}".format(gfx_index, pipe,
                                                                                                     color_enums.ColorimetryYUV.ITU_R_BT709.name,
                                                                                                     prog_colorimetry))
                return False
            logging.info(
                "PASS : Colorimetry Info on Adapter:{0} Pipe:{1} Expected:{2} and Actual:{3}".format(gfx_index, pipe,
                                                                                                     color_enums.ColorimetryYUV.ITU_R_BT709.name,
                                                                                                     prog_colorimetry))

    return True


def verify_metadata_aux_dpcd(display_and_adapter_info, expected_max_cll, expected_max_fall, target_nits, expected_po_max_cll, expected_po_max_fall):
    dpcd_lum = []
    edp_hdr_caps = color_escapes.fetch_dpcd_data(color_enums.EdpHDRDPCDOffsets.EDP_HDR_CAPS_BYTE1.value, display_and_adapter_info)

    edp_hdr_ctrl_params = color_escapes.fetch_dpcd_data(
        color_enums.EdpHDRDPCDOffsets.EDP_HDR_GET_SET_CTRL_PARAMS_BYTE0.value, display_and_adapter_info)
    content_luminance_base_address = color_enums.EdpHDRDPCDOffsets.EDP_HDR_CONTENT_LUMINANCE_BYTE0.value
    panel_override_base_address = color_enums.EdpHDRDPCDOffsets.EDP_HDR_PANEL_LUMINANCE_OVERRIDE_BYTE0.value

    for addr_index in range(0, 4):
        dpcd_lum.append(color_escapes.fetch_dpcd_data(content_luminance_base_address, display_and_adapter_info))
        content_luminance_base_address += 1

    max_cll_val = common_utility.get_bit_value(dpcd_lum[1], 0, 7) << 8 | common_utility.get_bit_value(dpcd_lum[0], 0, 7)

    if max_cll_val != expected_max_cll:
        logging.error("FAIL : Expected MaxCLL : %s; Actual MaxCLL : %s" % (expected_max_cll, max_cll_val))
        return False
    logging.info("PASS : Expected MaxCLL : %s; Actual MaxCLL : %s" % (expected_max_cll, max_cll_val))

    max_fall_val = common_utility.get_bit_value(dpcd_lum[3], 0, 7) << 8 | common_utility.get_bit_value(dpcd_lum[2],
                                                                               0, 7)
    if max_fall_val != expected_max_fall:
        logging.error("FAIL : Expected MaxFALL : %s; Actual MaxFALL : %s" % (expected_max_fall, max_fall_val))
        return False
    logging.info("PASS : Expected MaxFALL : %s; Actual MaxFALL : %s" % (expected_max_fall, max_fall_val))

    ##
    # Panel Override Luminance Verification
    for addr_index in range(0, 4):
        dpcd_lum.append(color_escapes.fetch_dpcd_data(panel_override_base_address, display_and_adapter_info))
        panel_override_base_address += 1

    max_cll_val = common_utility.get_bit_value(dpcd_lum[1], 0, 7) << 8 | common_utility.get_bit_value(dpcd_lum[0],
                                                                                                      0, 7)
    if max_cll_val != expected_po_max_cll:
        logging.error("FAIL : Expected MaxCLL : %s; Actual MaxCLL : %s" % (expected_po_max_cll, max_cll_val))
        return False
    logging.info("PASS : Expected MaxCLL : %s; Actual MaxCLL : %s" % (expected_po_max_cll, max_cll_val))

    max_fall_val = common_utility.get_bit_value(dpcd_lum[3], 0, 7) << 8 | common_utility.get_bit_value(dpcd_lum[2],
                                                                                                       0,
                                                                                                       7)
    if max_fall_val != expected_po_max_fall:
        logging.info("FAIL : Expected MaxFALL : %s; Actual MaxFALL : %s" % (expected_po_max_fall, max_fall_val))
        return False
    logging.info("PASS : Expected MaxFALL : %s; Actual MaxFALL : %s" % (expected_po_max_fall, max_fall_val))

    ##
    # If the display caps support panel tone mapping, driver should enable support for panel tone mapping
    if common_utility.get_bit_value(edp_hdr_caps, 2, 2) == color_constants.ENABLE_PANEL_TONE_MAPPING:
        logging.info("Display Caps ENABLE_PANEL_TONE_MAPPING - Expected : ENABLE; Actual : ENABLE")
        ##
        # Driver enables support for panel tone mapping only when target nits is greater than panel nits
        if target_nits > max_cll_val:
            if common_utility.get_bit_value(edp_hdr_ctrl_params, 3, 3) == color_constants.ENABLE_PANEL_TONE_MAPPING:
                logging.info("Driver support for ENABLE_PANEL_TONE_MAPPING - Expected : ENABLE; Actual : ENABLE")
            else:
                logging.error("Driver support for ENABLE_PANEL_TONE_MAPPING - Expected : ENABLE; Actual : DISABLE")
                return False
    else:
        logging.info("Display Caps ENABLE_PANEL_TONE_MAPPING - Expected : ENABLE; Actual : DISABLE")
        return False
    return True


##
# Perform DPCD verification for Aux based eDP HDR panels
def verify_edp_hdr_display_caps_and_ctrl_params(gfx_index: str, platform: str, display_and_adapter_info, pipe):

    edp_brightness_optimization = color_escapes.fetch_dpcd_data(
        color_enums.EdpHDRDPCDOffsets.EDP_BRIGHTNESS_OPTIMIZATION.value, display_and_adapter_info)
    # If AC Mode : 1 and DC Mode: 0 (default) -> Currently auto test executes in AC Mode.
    if common_utility.get_bit_value(edp_brightness_optimization, 4, 4) != 1:
        logging.error("EDP_BRIGHTNESS_OPTIMIZATION = 0")
    logging.info("EDP_BRIGHTNESS_OPTIMIZATION = %s" % 1)

    # 0 - USAGE UNKNOWN
    # 1 - DESKTOP
    # 2 - FULL SCREEN VIDEO
    # 3 - FULL SCREEN GAME
    # EXCEPT VIDEO PLAYBACK TEST CASE, REST ALL HDR TEST SCENARIO SHOULD HAVE DESKTOP 1
    # Logging error for now, since VPB scenario integration planned to take later.
    if common_utility.get_bit_value(edp_brightness_optimization, 0, 3) == 1:
        logging.error("EDP_BRIGHTNESS_OPTIMIZATION = 0")
    logging.info("EDP_BRIGHTNESS_OPTIMIZATION = %s" % 1)

    edp_brightness_nits_byte0_lsb = color_escapes.fetch_dpcd_data(
        color_enums.EdpHDRDPCDOffsets.EDP_BRIGHTNESS_NITS_BYTE0_LSB.value, display_and_adapter_info)
    edp_brightness_nits_byte1_msb = color_escapes.fetch_dpcd_data(
        color_enums.EdpHDRDPCDOffsets.EDP_BRIGHTNESS_NITS_BYTE1_MSB.value, display_and_adapter_info)

    nits_value = (edp_brightness_nits_byte1_msb << 8) | edp_brightness_nits_byte0_lsb
    logging.info("Nits Value in the DPCD is %s" % nits_value)

    per_frame_steps = color_escapes.fetch_dpcd_data(
        color_enums.EdpHDRDPCDOffsets.EDP_BRIGHTNESS_NITS_BYTE_PER_FRAME_STEPS.value, display_and_adapter_info)

    # This is specific to DPCD Programming for Nits or Aux based HDR Panel, where this will set to 1 by driver default.
    # Cases where HDR Enabled with brightness adjustment this was programmed to be expected.
    # If the Brightness DDI not received cases of persistence scenario ideally this DPCD verification will fail
    # all the test. so marking error for now.
    if per_frame_steps != 1:
        logging.error("Per Frame Steps =  %s" % per_frame_steps)
    logging.info("Per Frame Steps =  %s" % per_frame_steps)

    edp_hdr_caps = color_escapes.fetch_dpcd_data(color_enums.EdpHDRDPCDOffsets.EDP_HDR_CAPS_BYTE1.value,
                                                 display_and_adapter_info)
    edp_hdr_ctrl_params = color_escapes.fetch_dpcd_data(
        color_enums.EdpHDRDPCDOffsets.EDP_HDR_GET_SET_CTRL_PARAMS_BYTE0.value, display_and_adapter_info)
    ##
    # If the display caps support 2084 decode, then driver should enable 2084 decode in HDR Mode
    is_hdr_enabled = feature_basic_verify.hdr_status(gfx_index, platform, pipe)
    ##
    # If the display caps support segmented backlight, then driver should enable support for segmented backlight
    if common_utility.get_bit_value(edp_hdr_caps, 3, 3):
        logging.info("Display Caps ENABLE_SEGMENTED_BKLGHT - Expected : ENABLE; Actual : ENABLE")
        if common_utility.get_bit_value(edp_hdr_ctrl_params, 3, 3) == color_constants.ENABLE_SEGMENTED_BKLGHT:
            logging.info("Driver support for ENABLE_SEGMENTED_BKLGHT - Expected : ENABLE; Actual : ENABLE")
        else:
            logging.error("Driver support for ENABLE_SEGMENTED_BKLGHT - Expected : ENABLE; Actual : DISABLE")
            gdhm.report_driver_bug_os("[{0}] Verification failed with DPCD ENABLE_SEGMENTED_BKLGHT for Adapter: {1} "
                                        "TargetId: {2}- Expected : ENABLE; Actual : DISABLE"
                                        .format(platform, gfx_index, display_and_adapter_info.TargetID))
            return False

    ##
    # If the display caps support brightness control via aux,
    # then driver should enable support for brightness control via aux.
    if common_utility.get_bit_value(edp_hdr_caps, 4, 4):
        logging.info("Display Caps ENABLE_BRIGHTNESS_CONTROL_USING_AUX - Expected : ENABLE; Actual : ENABLE")
        if common_utility.get_bit_value(edp_hdr_ctrl_params, 4,
                                        4) == color_constants.ENABLE_BRIGHTNESS_CONTROL_USING_AUX:
            logging.info(
                "Driver support for ENABLE_BRIGHTNESS_CONTROL_USING_AUX - Expected : ENABLE; Actual : ENABLE")
        else:
            logging.error(
                "Driver support for ENABLE_BRIGHTNESS_CONTROL_USING_AUX - Expected : ENABLE; Actual : DISABLE")
            gdhm.report_driver_bug_os("[{0}] Verification failed with DPCD ENABLE_BRIGHTNESS_CONTROL_USING_AUX for Adapter: {1} "
                                        "TargetId: {2} - Expected : ENABLE; Actual : DISABLE"
                                        .format(platform,gfx_index,display_and_adapter_info.TargetID))
            return False


    ##
    # If the display caps support sdp support for colorimetry should be disabled,
    # then driver should enable support sdp support for colorimetry should be disabled
    if common_utility.get_bit_value(edp_hdr_caps, 6, 6) == color_constants.DISABLE_SDP_SUPPORT_FOR_COLORIMETRY:
        logging.info("Display Caps DISABLE_SDP_SUPPORT_FOR_COLORIMETRY - Expected : ENABLE; Actual : ENABLE")
        if common_utility.get_bit_value(edp_hdr_ctrl_params, 6,
                                        6) == color_constants.DISABLE_SDP_SUPPORT_FOR_COLORIMETRY:
            logging.info(
                "Driver support for DISABLE_SDP_SUPPORT_FOR_COLORIMETRY - Expected : ENABLE; Actual : ENABLE")
        else:
            logging.error(
                "Driver support for DISABLE_SDP_SUPPORT_FOR_COLORIMETRY - Expected : ENABLE; Actual : DISABLED")
            gdhm.report_driver_bug_os("[{0}] Verification failed with DPCD DISABLE_SDP_SUPPORT_FOR_COLORIMETRY for Adapter: {1} "
                                        "TargetId: {2} - Expected : ENABLE; Actual : DISABLED"
                                        .format(platform,gfx_index,display_and_adapter_info.TargetID))
            return False

    if common_utility.get_bit_value(edp_hdr_caps, 0, 0):
        logging.info("Display Caps ENABLE_2084_DECODE - Expected : ENABLE; Actual : ENABLE")
        if is_hdr_enabled:
            ##
            # In HDR mode, driver should enable 2084_DECODE
            if common_utility.get_bit_value(edp_hdr_ctrl_params, 0, 0) == color_constants.ENABLE_2084_DECODE:
                logging.info("Driver support for ENABLE_2084_DECODE - Expected : ENABLE; Actual : ENABLE")
            else:
                logging.error("Driver support for ENABLE_2084_DECODE - Expected : ENABLE; Actual : DISABLE")
        else:
            ##
            # In SDR Mode, driver should not enable 2084_DECODE
            if common_utility.get_bit_value(edp_hdr_ctrl_params, 0, 0) != color_constants.ENABLE_2084_DECODE:
                logging.info("Driver support for ENABLE_2084_DECODE - Expected : DISABLE; Actual : DISABLE")
            else:
                logging.error("Driver support for ENABLE_2084_DECODE - Expected : DISABLE; Actual : ENABLE")

    if common_utility.get_bit_value(edp_hdr_caps, 1, 1):
        if is_hdr_enabled:
            ##
            # In HDR mode, driver should enable Supports2020Gamut
            if common_utility.get_bit_value(edp_hdr_ctrl_params, 1, 1) == color_constants.ENABLE_2084_DECODE:
                logging.info("Driver support for ENABLE_2020_GAMUT - Expected : ENABLE; Actual : ENABLE")
            else:
                logging.error("Driver support for ENABLE_2020_GAMUT - Expected : ENABLE; Actual : DISABLE")
        else:
            ##
            # In SDR Mode, driver should not enable 2084_DECODE
            if common_utility.get_bit_value(edp_hdr_ctrl_params, 1, 1) != color_constants.ENABLE_2084_DECODE:
                logging.info("Driver support for ENABLE_2020_GAMUT - Expected : DISABLE; Actual : DISABLE")
            else:
                logging.error("Driver support for ENABLE_2020_GAMUT - Expected : DISABLE; Actual : ENABLE")
    ##
    # Supports sRGB Panel gamut conversion : This is needed only in SDR Mode, hence should be disabled in HDR Mode
    if common_utility.get_bit_value(edp_hdr_caps, 7, 7) == color_constants.DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION:
        logging.info("Display Caps DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : ENABLE; Actual : ENABLE ")
        ##
        # In HDR Mode, sRGB Panel Gamut conversion should be disabled
        if is_hdr_enabled:
            if common_utility.get_bit_value(edp_hdr_ctrl_params, 5,
                                            5) == color_constants.DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION:
                logging.info(
                    "Driver support for DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : ENABLE; Actual : ENABLE")
            else:
                logging.error(
                    "Driver support for DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : ENABLE; Actual : DISABLE")
        ##
        # In SDR Mode, sRGB Panel Gamut conversion should be enabled
        else:
            if common_utility.get_bit_value(edp_hdr_ctrl_params, 5,
                                            5) != color_constants.DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION:
                logging.info(
                    "Driver support for DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : ENABLE; Actual : ENABLE")
            else:
                logging.error(
                    "Driver support for DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : ENABLE; Actual : DISABLE")
    return True


##
# Decode Color Space enum value to obtain color_space, range, gamut and gamma
def decode_color_space_enum_value(color_space_enum):
    color_space, gamma, gamut, range = None, None, None, None
    # With reference to below structure
    # typedef enum D3DDDI_COLOR_SPACE_TYPE
    # {
    #    D3DDDI_COLOR_SPACE_RGB_FULL_G22_NONE_P709             = 0,
    #    D3DDDI_COLOR_SPACE_RGB_FULL_G10_NONE_P709             = 1,
    #    D3DDDI_COLOR_SPACE_RGB_STUDIO_G22_NONE_P709           = 2,
    #    D3DDDI_COLOR_SPACE_RGB_STUDIO_G22_NONE_P2020          = 3,
    #    D3DDDI_COLOR_SPACE_RESERVED                           = 4,
    #    D3DDDI_COLOR_SPACE_YCBCR_FULL_G22_NONE_P709_X601      = 5,..??
    #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P601         = 6,
    #    D3DDDI_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P601           = 7,
    #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709         = 8,
    #    D3DDDI_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P709           = 9,
    #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P2020        = 10,
    #    D3DDDI_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P2020          = 11,
    #    D3DDDI_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020          = 12,
    #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G2084_LEFT_P2020      = 13,
    #    D3DDDI_COLOR_SPACE_RGB_STUDIO_G2084_NONE_P2020        = 14,
    #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G22_TOPLEFT_P2020     = 15,
    #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G2084_TOPLEFT_P2020   = 16,
    #    D3DDDI_COLOR_SPACE_RGB_FULL_G22_NONE_P2020            = 17,
    #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_GHLG_TOPLEFT_P2020    = 18,
    #    D3DDDI_COLOR_SPACE_YCBCR_FULL_GHLG_TOPLEFT_P2020      = 19,
    #    D3DDDI_COLOR_SPACE_CUSTOM                             = 0xFFFFFFFF
    # } D3DDDI_COLOR_SPACE_TYPE;

    # colorSpace
    if color_space_enum in (0, 1, 2, 3, 12, 14, 17):
        color_space = "RGB"
    elif color_space_enum in (6, 7, 8, 9, 10, 11, 13, 15, 16):
        color_space = "YCBCR"
    else:
        logging.error("ColorSpace enum type not supported !!")
        return False

    # range
    if color_space_enum in (0, 1, 7, 9, 11, 12, 17):
        range = "FULL"
    elif color_space_enum in (2, 3, 6, 8, 10, 13, 14, 15, 16):
        range = "STUDIO"

    # gamma
    if color_space_enum in (0, 2, 3, 6, 7, 8, 9, 10, 11, 15, 17):
        gamma = "G22"
    elif color_space_enum in (12, 13, 14, 16):
        gamma = "G2084"
    elif color_space_enum == 1:
        gamma = "G10"

    # gamut
    if color_space_enum in (0, 1, 2, 8, 9):
        gamut = "P709"
    elif color_space_enum in (6, 7):
        gamut = "P601"
    elif color_space_enum in (3, 10, 11, 12, 13, 14, 15, 16, 17):
        gamut = "P2020"

    logging.info("Plane Color Attributes : Color Space : {0} Gamut : {1} Gamma : {2} Range : {3}".format(color_space, gamut, gamma, range))
    return color_space, gamut, gamma, range


##
# Simplified verification where only BPC, PixelEncoding, Colorimetry and Metadata verification are performed
def hdr_verification(pipe_args: Union[E2EPipeArgs, DFTPipeArgs], gfx_index, platform, port, panel, expected_bpc=0, pcon=False):
    from Tests.Color.Verification import gen_verify_pipe
    is_hdr_enabled = feature_basic_verify.hdr_status(gfx_index, platform, panel.pipe)
    pipe_verifier = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)
    psr_status = False
    if type(pipe_args) is E2EPipeArgs:
        #
        # Performing BPC verification
        logging.info("Performing Transcoder BPC Verification")
        if feature_basic_verify.verify_transcoder_bpc(gfx_index, platform, panel.transcoder, expected_bpc) is False:
            return False
        logging.info("Performing Pixel Encoding Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index, panel.pipe))
        if verify_pixel_encoding(gfx_index, platform, "0", panel.pipe,
                                             expected_pixel_encoding=color_enums.PixelEncoding.RGB.value) is False:
            return False

        if panel.FeatureCaps.PSRSupport:
            if color_igcl_escapes.get_power_caps(panel.target_id, control_api_args.ctl_power_optimization_flags_v.PSR.value):
                get_psr = color_igcl_wrapper.prepare_igcl_args_for_get_power_ftr(
                    control_api_args.ctl_power_optimization_flags_v.PSR.value)

                logging.info("Step_2: Performing IGCL Call to Get PSR Status")
                if control_api_wrapper.get_psr(get_psr, panel.target_id):
                    if get_psr.Enable:
                        psr_status = True
        if is_hdr_enabled:
            if pipe_verifier.verify_sdp_data(gfx_index, panel.display_and_adapterInfo, panel.is_lfp, panel.pipe,
                                             panel.FeatureCaps.HDRSupport, psr_status) is False:
                return False

        # logging.info("Performing Colorimetry Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index, panel.pipe))
        # if verify_colorimetry(gfx_index, platform, "0", panel.pipe,
        #                                   color_enums.PixelEncoding.RGB.value) is False:
        #
        #     return False
    if is_hdr_enabled:
        if panel.is_lfp:
            logging.info("Performing DPCD Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index, panel.pipe))
            if not verify_edp_hdr_display_caps_and_ctrl_params(gfx_index, platform,
                                                                           panel.display_and_adapterInfo, panel.pipe):
                return False
    logging.info("Performing Metadata Verification for {0} on Adapter : {1}  Pipe : {2}".format(port, gfx_index, panel.pipe))
    if pipe_verifier.verify_metadata(pipe_args, port, panel.is_lfp, panel.pipe,
                                    panel.display_and_adapterInfo, pcon) is False:
        pass
        ## @todo - Here observing an OS issue where the Min and Max Mastering Luminance have been swapped.
        # OS has updated that issue will be fixed in Ni build. Will comment out once the issue is fixed
        #return False
    return True


##
# Performing FP16 Normalizer Verification
# Status and the enable status
def verify_fp16_normalizer_enable_status(pixel_format, gfx_index, pipe, plane, pixel_normalizer_info, feature):
    status = False
    fp16_normalizer_enable = pixel_normalizer_info.NormalizerEnable
    if color_constants.source_pixel_format_dict[pixel_format].__contains__('RGB_16161616_FLOAT'):
        if feature == "HDR" or "WCG":
            if pixel_normalizer_info.NormalizerEnable:
                logging.info(
                    "PASS : FP16 normalizer enabled for plane with FP16 format on Adapter {0} Plane {1} Pipe {2}".format(
                        gfx_index, plane, pipe))
                status = True
                return status, fp16_normalizer_enable
            else:
                logging.error(
                    "FAIL : FP16 normalizer not enabled for plane with FP16 format on Adapter {0} Plane {1} Pipe {2}".format(
                        gfx_index, plane, pipe))
                gdhm.report_driver_bug_os(
                    "FP16 normalizer not enabled for plane with FP16 format on Adapter {0} Plane {1} Pipe {2}"
                                            .format(gfx_index, plane, pipe))
                return status, fp16_normalizer_enable
        else:
            if pixel_normalizer_info.NormalizerEnable:
                status = True
                return status, fp16_normalizer_enable
    else:
        if pixel_normalizer_info.NormalizerEnable:
            logging.error(
                "FAIL : FP16 normalizer enabled for a non-FP16 plane on Adapter {0} Plane {1} Pipe {2}".format(
                    gfx_index, plane, pipe))
            gdhm.report_driver_bug_os(
                "FP16 normalizer enabled for a non-FP16 plane on Adapter {0} Plane {1} Pipe {2}"
                                        .format(gfx_index, plane, pipe))
            return status, fp16_normalizer_enable
        else:
            logging.info(
                "PASS : FP16 normalizer is not enabled for a non-FP16 plane on Adapter {0} Plane {1} Pipe {2}".format(
                    gfx_index, plane, pipe))
            status = True
            return status, fp16_normalizer_enable


##
# Performing InputCSC Verification
def verify_input_csc_enable_status(pixel_format, output_range, gfx_index, pipe, plane, plane_color_ctl_info):
    status = False
    input_csc_enable = plane_color_ctl_info.PlaneInputCscEnable
    if color_constants.source_pixel_format_dict[pixel_format].__contains__('YUV') or output_range == "STUDIO":
        if plane_color_ctl_info.PlaneInputCscEnable is False:
            logging.error(
                "FAIL: Plane iCSC is not enabled on Adapter {0} Plane {1} with PixelFormat {2} on Pipe {3} Expected = ENABLE, Actual = DISABLE".format(
                    gfx_index, plane, color_constants.source_pixel_format_dict[pixel_format], pipe))
            gdhm.report_driver_bug_os("Verification failed as Plane iCSC is not enabled on Adapter {0} Plane {1} with PixelFormat {2} on Pipe {3} Expected = ENABLE, Actual = DISABLE".format(
                    gfx_index, plane, color_constants.source_pixel_format_dict[pixel_format], pipe))
            return status, input_csc_enable
        else:
            logging.info(
                "PASS: Plane iCSC is enabled on Adapter {0} Plane {1} with PixelFormat {2} Pipe {3} Expected = ENABLE, Actual = ENABLE".format(
                    gfx_index, plane, color_constants.source_pixel_format_dict[pixel_format],
                    pipe))
            status = True
            return status, input_csc_enable
    else:
        if plane_color_ctl_info.PlaneInputCscEnable:
            logging.error("FAIL: Plane iCSC is enabled for a non-YUV PixelFormat. Expected = DISABLE, Actual = ENABLE")
            gdhm.report_driver_bug_os("Verification failed as Plane iCSC is enabled for a non-YUV PixelFormat on Adapter: {0} Plane: {1} Pipe: {2}. Expected = DISABLE, Actual = ENABLE".format(
                gfx_index, plane, pipe
            ))
            return status, input_csc_enable
    logging.info(
        "PASS: Plane iCSC on Adapter {0} Plane {1} with PixelFormat {2} Pipe {3} Expected = DISABLE, Actual = DISABLE".format(
            gfx_index, plane, color_constants.source_pixel_format_dict[pixel_format],
            pipe))
    status = True
    return status, input_csc_enable


##
# Performing PreCSC Gamma Verification
def verify_pre_csc_gamma_enable_status(pixel_format, gfx_index, pipe, plane, plane_color_ctl_info):
    status = False
    plane_pre_csc_gamma_enable = plane_color_ctl_info.PlanePreCscGammaEnable
    if color_constants.source_pixel_format_dict[pixel_format] == 'RGB_16161616_FLOAT' or color_constants.source_pixel_format_dict[pixel_format] == 'RGB_2101010':
        if plane_color_ctl_info.PlanePreCscGammaEnable is False:
            logging.error(
                "FAIL: Plane PreCSC Gamma not enabled on Adapter {0} Plane {1} with PixelFormat {2} on Pipe {3}. "
                "Expected = ENABLE, Actual = DISABLE "
                    .format(gfx_index, plane, color_constants.source_pixel_format_dict[pixel_format], pipe))
            gdhm.report_driver_bug_os(
                "Verification failed as Plane PreCSC Gamma not enabled on Adapter {0} Plane {1} with PixelFormat {2} on Pipe {3}"
                "Expected = ENABLE, Actual = DISABLE "
                    .format(gfx_index, plane, color_constants.source_pixel_format_dict[pixel_format], pipe)
                )
            return status, plane_pre_csc_gamma_enable
        else:
            logging.info(
                "PASS: Plane PreCSC Gamma enabled on Adapter {0} Plane {1} with PixelFormat {2} on Pipe {3}. Expected "
                "= ENABLE, Actual = ENABLE "
                    .format(gfx_index, plane, color_constants.source_pixel_format_dict[pixel_format], pipe))
            status = True
            return status, plane_pre_csc_gamma_enable
    else:
        ##
        # ToDo : Return the status once the Precision WA is updated across the platforms
        if plane_color_ctl_info.PlanePreCscGammaEnable:
            logging.info(
                "Plane PreCSC Gamma enabled on Adapter {0} Plane {1} with PixelFormat {2} on Pipe {3}"
                    .format(gfx_index, plane, color_constants.source_pixel_format_dict[pixel_format], pipe))

    logging.info(
        "PASS: Plane PreCSC Gamma enabled on Adapter {0} Plane {1} with PixelFormat {2} on Pipe {3}. Expected = "
        "DISABLE, Actual = DISABLE "
            .format(gfx_index, plane, color_constants.source_pixel_format_dict[pixel_format], pipe))
    status = True
    return status, plane_pre_csc_gamma_enable


##
# Performing Plane PostCSC Verification
def verify_post_csc_gamma_enable_status(gfx_index, plane, pipe, plane_color_ctl_info, feature):
    status = False
    plane_post_csc_gamma_enable = plane_color_ctl_info.PlaneGammaDisable
    if feature == "HDR" or "WCG":
        if plane_color_ctl_info.PlaneGammaDisable:
            logging.info(
                "PASS: Plane PostCSC Gamma disabled on Adapter {0} Plane {1} on Pipe {2}. Expected = DISABLE, Actual = DISABLE"
                    .format(gfx_index, plane, pipe))
            status = True
            return status, plane_post_csc_gamma_enable
        else:
            logging.error(
                "FAIL: Plane PostCSC Gamma  enabled on Adapter {0} Plane {1} on Pipe {2}. Expected = DISABLE, Actual = ENABLE"
                    .format(gfx_index, plane, pipe))
            gdhm.report_driver_bug_os(
                "Plane PostCSC Gamma enabled on Adapter {0} Plane {1} on Pipe {2}. Expected = DISABLE, Actual = ENABLE"
                    .format(gfx_index, plane, pipe))
            return status, plane_post_csc_gamma_enable
    else:
        # Fp16 or PlaneCSC
        if not plane_color_ctl_info.PlaneGammaDisable:
            logging.error(
                "FAIL: Plane PostCSC Gamma enabled on Adapter {0} Plane {1} on Pipe {2}. Expected = DISABLE, Actual = ENABLE"
                    .format(gfx_index, plane, pipe))
            gdhm.report_driver_bug_os(
                "Plane PostCSC Gamma enabled on Adapter {0} Plane {1} on Pipe {2}. Expected = DISABLE, Actual = ENABLE"
                    .format(gfx_index, plane, pipe))
            return status, plane_post_csc_gamma_enable
    status = True
    return status, plane_post_csc_gamma_enable



##
# Performing Pipe PreCSC Gamma Enable
def verify_pipe_pre_csc_gamma_enable_status(gfx_index, pipe, gamma_mode_value, cc_block, feature):
    status = False
    if cc_block == "CC1":
        pipe_pre_csc_gamma_enable = gamma_mode_value.PreCscGammaEnable
    else:
        pipe_pre_csc_gamma_enable = gamma_mode_value.PreCscCc2GammaEnable
    logging.debug("CC1 DeGamma is {0}".format(feature_basic_verify.BIT_MAP_DICT[int(gamma_mode_value.PreCscGammaEnable)]))
    logging.debug("CC2 DeGamma is {0}".format(feature_basic_verify.BIT_MAP_DICT[int(gamma_mode_value.PreCscCc2GammaEnable)]))
    if feature == "HDR" or feature == "WCG":
        if pipe_pre_csc_gamma_enable:
            logging.error(
                "FAIL : Pipe PreCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                   pipe,
                                                                                                   feature_basic_verify.BIT_MAP_DICT[
                                                                                                       int(0)],
                                                                                                   feature_basic_verify.BIT_MAP_DICT[
                                                                                                       int(pipe_pre_csc_gamma_enable)]))
            gdhm.report_driver_bug_os("Pipe PreCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}"
                                    .format(gfx_index,pipe,feature_basic_verify.BIT_MAP_DICT[int(0)],
                                    feature_basic_verify.BIT_MAP_DICT[int(pipe_pre_csc_gamma_enable)]))
            return status, pipe_pre_csc_gamma_enable
        logging.info(
            "PASS : Pipe PreCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                               pipe,
                                                                                               feature_basic_verify.BIT_MAP_DICT[
                                                                                                   int(0)],
                                                                                               feature_basic_verify.BIT_MAP_DICT[
                                                                                                   int(
                                                                                                       pipe_pre_csc_gamma_enable)]))
        status = True
        return status, pipe_pre_csc_gamma_enable
    else:
        if pipe_pre_csc_gamma_enable == 0:
            logging.error(
                "FAIL : Pipe PreCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                   pipe,
                                                                                                   feature_basic_verify.BIT_MAP_DICT[
                                                                                                       int(1)],
                                                                                                   feature_basic_verify.BIT_MAP_DICT[
                                                                                                       int(pipe_pre_csc_gamma_enable)]))
            gdhm.report_driver_bug_os("Pipe PreCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}"
                                    .format(gfx_index,pipe,feature_basic_verify.BIT_MAP_DICT[int(1)],
                                    feature_basic_verify.BIT_MAP_DICT[int(pipe_pre_csc_gamma_enable)]))
            return status, pipe_pre_csc_gamma_enable
        logging.info(
            "PASS : Pipe PreCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                               pipe,
                                                                                               feature_basic_verify.BIT_MAP_DICT[
                                                                                                   int(1)],
                                                                                               feature_basic_verify.BIT_MAP_DICT[
                                                                                                   int(pipe_pre_csc_gamma_enable)]))
        status = True
        return status, pipe_pre_csc_gamma_enable


##
# Performing Pipe CSC Enable Verification
def verify_pipe_csc_enable_status(gfx_index, pipe, oned_lut_param_type, gamma_ramp_type, cc_block, color_ctl_values):
    status = False
    logging.debug("CC1 CSC is {0}".format(feature_basic_verify.BIT_MAP_DICT[int(color_ctl_values.PipeCscEnable)]))
    logging.debug("CC2 CSC is {0}".format(feature_basic_verify.BIT_MAP_DICT[int(color_ctl_values.PipeCscCC2Enable)]))
    if cc_block == "CC1":
        pipe_csc_enable = color_ctl_values.PipeCscEnable
    else:
        pipe_csc_enable = color_ctl_values.PipeCscCC2Enable
    ##
    # Pipe CSC verification to be performed only in case of GammaRampType from OS is 3x4Matrix
    if oned_lut_param_type == 'MATRIX_3x4':
        if gamma_ramp_type == 'MATRIX_3x4':
            if pipe_csc_enable == 0:
                logging.error(
                    "FAIL : Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                    pipe,
                                                                                                    feature_basic_verify.BIT_MAP_DICT[
                                                                                                        int(1)],
                                                                                                    feature_basic_verify.BIT_MAP_DICT[
                                                                                                        int(pipe_csc_enable)]))
                gdhm.report_driver_bug_os("Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}"
                                        .format(gfx_index,pipe,feature_basic_verify.BIT_MAP_DICT[int(1)],
                                            feature_basic_verify.BIT_MAP_DICT[int(pipe_csc_enable)]))
                return status, pipe_csc_enable
            logging.info(
                "PASS : Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                pipe,
                                                                                                feature_basic_verify.BIT_MAP_DICT[
                                                                                                    int(1)],
                                                                                                feature_basic_verify.BIT_MAP_DICT[
                                                                                                    int(pipe_csc_enable)]))
            status = True
            return status, pipe_csc_enable
        else:
            logging.info("Gamma Ramp Type is not 3x4 Matrix call from OS, hence Pipe CSC is not expected to be enabled")
            if pipe_csc_enable:
                logging.error(
                    "FAIL : Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                    pipe,
                                                                                                    feature_basic_verify.BIT_MAP_DICT[
                                                                                                        int(0)],
                                                                                                    feature_basic_verify.BIT_MAP_DICT[
                                                                                                        int(pipe_csc_enable)]))
                gdhm.report_driver_bug_os("Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}"
                                        .format(gfx_index,pipe,feature_basic_verify.BIT_MAP_DICT[int(0)],
                                            feature_basic_verify.BIT_MAP_DICT[int(pipe_csc_enable)]))
                return status, pipe_csc_enable
    else:
        logging.info("Gamma Ramp Type is not 3x4 Matrix call from OS, hence Pipe CSC is not expected to be enabled")
        if pipe_csc_enable:
            logging.error(
                "FAIL : Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                pipe,
                                                                                                feature_basic_verify.BIT_MAP_DICT[
                                                                                                    int(0)],
                                                                                                feature_basic_verify.BIT_MAP_DICT[
                                                                                                    int(pipe_csc_enable)]))
            gdhm.report_driver_bug_os("Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}"
                                    .format(gfx_index,pipe,feature_basic_verify.BIT_MAP_DICT[int(0)],
                                        feature_basic_verify.BIT_MAP_DICT[int(pipe_csc_enable)]))
            return status, pipe_csc_enable
        logging.info("PASS : Pipe CSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                pipe,
                                                                                                feature_basic_verify.BIT_MAP_DICT[
                                                                                                    int(0)],
                                                                                                feature_basic_verify.BIT_MAP_DICT[
                                                                                                    int(pipe_csc_enable)]))
    return True, pipe_csc_enable


##
# Performing Pipe Post CSC Gamma Enable Verification
def verify_pipe_post_csc_gamma_status(gfx_index, pipe, gamma_mode_value, cc_block):
    status = False
    logging.debug("CC1 Pipe Gamma is {0}".format(
        feature_basic_verify.BIT_MAP_DICT[int(gamma_mode_value.PostCscGammaEnable)]))
    logging.debug("CC2 Pipe Gamma is {0}".format(
        feature_basic_verify.BIT_MAP_DICT[int(gamma_mode_value.PostCscCc2GammaEnable)]))

    if cc_block == "CC1":
        pipe_post_csc_enable = gamma_mode_value.PostCscGammaEnable
    else:
        pipe_post_csc_enable = gamma_mode_value.PostCscCc2GammaEnable
    if pipe_post_csc_enable == 0:
        logging.error(
            "FAIL : Pipe PostCSC Gamma on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                                pipe,
                                                                                                feature_basic_verify.BIT_MAP_DICT[
                                                                                                    int(1)],
                                                                                                feature_basic_verify.BIT_MAP_DICT[
                                                                                                    int(pipe_post_csc_enable)]))

        gdhm.report_driver_bug_os("Pipe PostCSC Gamma on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}"
                                .format(gfx_index,pipe,feature_basic_verify.BIT_MAP_DICT[int(1)],
                                    feature_basic_verify.BIT_MAP_DICT[int(pipe_post_csc_enable)]))
        return status, pipe_post_csc_enable
    logging.info(
        "PASS : Pipe PostCSC Gamma on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3}".format(gfx_index,
                                                                                            pipe,
                                                                                            feature_basic_verify.BIT_MAP_DICT[
                                                                                                int(1)],
                                                                                            feature_basic_verify.BIT_MAP_DICT[
                                                                                                int(pipe_post_csc_enable)]))
    status = True
    return status, pipe_post_csc_enable


##
# Performing Pipe OutputCSC Enable Verification
def verify_pipe_output_status(gfx_index, pipe, color_ctl_value, gamma_mode_value, output_range):
    status = False
    output_csc_enable = color_ctl_value.PipeOutputCscEnable
    input, output, conv_type = None, None, None
    if color_ctl_value.PipeOutputColorSpaceSelect == color_enums.ColorSpace.YUV:
        if color_ctl_value.PipeOutputCscEnable:
            logging.info(
                "PASS : Pipe oCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3} when Pipe is in YUV ColorSpace".format(
                    gfx_index,
                    pipe,
                    feature_basic_verify.BIT_MAP_DICT[
                        int(1)],
                    feature_basic_verify.BIT_MAP_DICT[
                        int(color_ctl_value.PipeOutputCscEnable)]))
            input = color_enums.ColorSpace.RGB
            output = color_enums.ColorSpace.YUV
            conv_type = color_enums.ConversionType.FULL_TO_STUDIO
            status = True
            return status, output_csc_enable, input, output, conv_type
        else:
            logging.error(
                "FAIL : Pipe oCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3} when Pipe is in YUV ColorSpace".format(
                    gfx_index, pipe,
                    feature_basic_verify.BIT_MAP_DICT[
                        int(0)],
                    feature_basic_verify.BIT_MAP_DICT[int(
                        color_ctl_value.PipeOutputCscEnable)]))
            gdhm.report_driver_bug_os("Pipe oCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3} when "
                                    "Pipe is in YUV ColorSpace"
                                    .format(gfx_index, pipe,feature_basic_verify.BIT_MAP_DICT[int(0)],
                                    feature_basic_verify.BIT_MAP_DICT[int(color_ctl_value.PipeOutputCscEnable)]))
            return status, output_csc_enable, input, output, conv_type
    elif output_range == color_enums.RgbQuantizationRange.LIMITED.value:
        if color_ctl_value.PipeOutputCscEnable:
            logging.info(
                "PASS : Pipe oCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3} when OutputRange is STUDIO "
                "in RGB Mode".format(
                    gfx_index,
                    pipe,
                    feature_basic_verify.BIT_MAP_DICT[
                        int(1)],
                    feature_basic_verify.BIT_MAP_DICT[
                        int(color_ctl_value.PipeOutputCscEnable)]))
            input = color_enums.ColorSpace.RGB
            output = color_enums.ColorSpace.RGB
            conv_type = color_enums.ConversionType.FULL_TO_STUDIO
            status = True
            return status, output_csc_enable, input, output, conv_type
        else:
            logging.error(
                "FAIL : Pipe oCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3} when OutputRange is STUDIO "
                "in RGB Mode".format(
                    gfx_index, pipe,
                    feature_basic_verify.BIT_MAP_DICT[
                        int(1)],
                    feature_basic_verify.BIT_MAP_DICT[int(
                        color_ctl_value.PipeOutputCscEnable)]))
            gdhm.report_driver_bug_os("Pipe oCSC on Adapter : {0}  Pipe : {1} Expected {2} : Actual {3} when OutputRange is STUDIO "
                                    "in RGB Mode".format(gfx_index, pipe,feature_basic_verify.BIT_MAP_DICT[int(1)],
                                    feature_basic_verify.BIT_MAP_DICT[int(color_ctl_value.PipeOutputCscEnable)]))
            return status, output_csc_enable, input, output, conv_type
    else:
        # In-case of PipeOutputcsc already enabled, and there is conversion with same colorspace,
        # PipeOCscEnabled status is expected to be enabled
        if color_ctl_value.PipeOutputCscEnable:
            input = color_enums.ColorSpace.RGB
            output = color_enums.ColorSpace.RGB
            conv_type = color_enums.ConversionType.FULL_TO_FULL
            status = True
            return status, output_csc_enable, input, output, conv_type
        input = color_enums.ColorSpace.RGB
        output = color_enums.ColorSpace.RGB
        conv_type = color_enums.ConversionType.FULL_TO_STUDIO
        status = True
        return status, output_csc_enable, input, output, conv_type
