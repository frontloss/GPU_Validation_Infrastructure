######################################################################################################
# @file         color_properties.py
# @brief        Contains class definitiions of Color Features specific properties to be added to Test Context.
# @author       Smitha B
######################################################################################################
from dataclasses import dataclass, field
from typing import List
import logging
import random
import math
import time
from Libs.Core import driver_escape, registry_access
from Libs.Core import etl_parser
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Tests.Color.Common import color_etl_utility, color_escapes, common_utility
from Tests.Color.Common.color_enums import SamplingMode
from Tests.Color.Common.common_utility import read_registry, get_psr_caps
from Tests.Color.Verification import feature_basic_verify
from Tests.PowerCons.Modules import windows_brightness
from Tests.PowerCons.Modules import dpcd


##
# @brief FeatureCaps supported by a Panel
@dataclass
class FeatureCaps:
    HDRSupport: bool = False
    YCbCrSupport: bool = False
    WCGSupport: bool = False
    ELPSupport: bool = False
    PSRSupport: bool = False
    PSRVersion: int = 0


#######################################################################################################
###################################### All Data related to HDR ########################################
#######################################################################################################


##
# @brief HDRDisplayCaps supported by a HDR supported Panel
@dataclass
class HDRDisplayCaps:
    is_hdr_supported: bool = False
    is_aux: bool = False
    desired_max_cll: int = 0
    desired_max_fall: int = 0
    desired_min_cll: int = 0

@dataclass
class HDRMetadataScenario:
    reboot: int = 0
    hotplug: int = 0
    brightness_change: int = 0


##
# @brief HDRStaticMetadata, CTypes Structure for Metadata
@dataclass
class HDRStaticMetadata:
    EOTF: int = 0
    DisplayPrimariesX0: int = 0
    DisplayPrimariesX1: int = 0
    DisplayPrimariesX2: int = 0
    DisplayPrimariesY0: int = 0
    DisplayPrimariesY1: int = 0
    DisplayPrimariesY2: int = 0
    WhitePointX: int = 0
    WhitePointY: int = 0
    MaxLuminance: int = 0
    MinLuminance: int = 0
    MaxCLL: int = 0
    MaxFALL: int = 0


##
# @brief OSHdrMetadata, to be fetched from ETL\MMIO for each Panel
@dataclass
class OSHdrMetadata:
    target_id: int = 0
    hdr_metadata_type: str = ""
    programmed_metadata: HDRStaticMetadata = None


##
# @brief HDRProperties of a Panel
@dataclass
class HDRProperties:
    b3_value: int = 0
    sdr_white_level: int = 0
    pixel_boost: float = 1.0
    b3_transition_time: int = 200
    os_relative_lut: List[int] = field(default_factory=list)
    gamma_ramp_type: int = 0
    oned_lut_param_type: int = 0
    dsb_gamma_dump: List[int] = field(default_factory=list)
    os_relative_csc: List[int] = field(default_factory=list)
    default_metadata: OSHdrMetadata = None
    flip_metadata: OSHdrMetadata = None
    bpc = None


def perform_exponent_encoding(sign, exponent, fraction):
    significand_base2 = fraction / pow(2, 10)
    native_luma = 0
    if exponent == 0:
        native_luma = pow(-1, sign) * pow(2, -14) * significand_base2
    if exponent != 0x1F or exponent == 0:
        significand_base2 = 1 + significand_base2
        exponent_val = exponent - 15
        native_luma = pow(-1, sign) * pow(2, exponent_val) * significand_base2
    if exponent == 0x1F:
        native_luma = -1
    return native_luma


##
# Parse the EDID_extension blocks
def parse_edid_extension_block(target_id, display_and_adapter_info):
    cta_max_cll, cta_max_fall, cta_min_cll = 0, 0, 0
    did_max_cll, did_max_fall, did_min_cll = 0, 0, 0
    cta_hdr_support, did_hdr_support = False, False
    edid_flag, edid_data, _ = driver_escape.get_edid_data(display_and_adapter_info)
    prd_identification_blk, display_intrface_blk, display_param_blk, type_vii_timing_blk, \
    supported_eotf_is_2084, is_having_valid_did_block = False, False, False, False, False, False
    prd_blk_index, disp_intrf_index, disp_param_index, type_vii_timing_index = 0, 0, 0, 0

    if not edid_flag:
        logging.error(f"Failed to get EDID data for target_id : {target_id}")
        assert edid_flag, "Failed to get EDID data"
    assert edid_data
    index = 126
    extension_blocks = edid_data[index]
    logging.info("Number of Extension Blocks are {0}".format(extension_blocks))
    if extension_blocks >= 1:
        index += 2 # increase index with 2 value to check start value of next block
        temp_index = index + 5  # add header byte
        for block in range(1, extension_blocks + 1):
            ##
            # Add all the details regarding DID2.0
            ##
            # EDID Extension Block Tag
            logging.debug("EDID Extension Block Tag {0}".format(edid_data[index]))
            if edid_data[index] == 0x70:
                # DisplayID Structure Version/ Revision
                if edid_data[index + 1] == 0x20:
                    logging.debug("Got the DisplayID Structure Version/ Revision")
                    while temp_index < index + 126:
                        ##
                        # The first sub-block must be a valid Product Identification Sub-Block
                        # Block tag 0x20 represents the Product Identification Sub-Block
                        if edid_data[temp_index] == 0x20:
                            logging.debug("Product Identification Sub-Block is Present")
                            prd_identification_blk = True
                            prd_blk_index = temp_index
                            logging.debug("Temp Index during Prod Identification Sub-Block is {0}".format(temp_index))

                        ##
                        # There must be at least one Type VII timing sub-block
                        # Block tag 0x22 represents the Type VII Timing - Detailed Timing Data Block
                        if edid_data[temp_index] == 0x22:
                            logging.debug("Type VII Timing - Detailed Timing Data Block is present")
                            type_vii_timing_blk = True
                            type_vii_timing_index = temp_index

                        ##
                        # Block Tag 0x26 represents the Display Interfaces Data Block
                        # where the support for HDR is present
                        if edid_data[temp_index] == 0x26:
                            logging.debug("Display Interfaces Data Block is present")
                            display_intrface_blk = True
                            disp_intrf_index = temp_index
                            supported_eotf_is_2084 = edid_data[temp_index + 9] >> 6
                            logging.debug("Temp Index during Display Interfaces Data Block is {0}".format(temp_index))

                        ##
                        # Block Tag 0x21 represents the Display Parameters Data Block
                        # where the native luminance related values are present
                        if edid_data[temp_index] == 0x21:
                            logging.debug("Display Parameters Data Block is present")
                            disp_param_index = temp_index
                            logging.debug("Temp Index during Display Parameters Data Block is {0}".format(temp_index))
                            display_param_blk = True
                            ##
                            # Native Luminance related fields are encoded in IEEE 754
                            # half-precision binary floating point format
                            # Formula to decode the values are defined in
                            # https://en.wikipedia.org/wiki/Half-precision_floating-point_format
                            max_fall_lsb = int(edid_data[temp_index + 24]) & 0xFF
                            max_fall_msb = int(edid_data[temp_index + 25]) & 0xFF
                            max_fall = max_fall_msb << 8 | max_fall_lsb

                            max_fall_sign = common_utility.get_bit_value(max_fall, 15, 15)
                            max_fall_exponent = common_utility.get_bit_value(max_fall, 10, 14)
                            max_fall_fraction = common_utility.get_bit_value(max_fall, 0, 9)  # mantissa
                            logging.debug(
                                "Sign is {0} Exponent is {1} Fraction is {2}".format(max_fall_sign, max_fall_exponent,
                                                                                     max_fall_fraction))
                            did_max_fall = perform_exponent_encoding(max_fall_sign, max_fall_exponent, max_fall_fraction)

                            ##
                            # MaxCLL Value calculation
                            max_cll_lsb = int(edid_data[temp_index + 26]) & 0xFF
                            max_cll_msb = int(edid_data[temp_index + 27]) & 0xFF
                            max_cll = max_cll_msb << 8 | max_cll_lsb

                            max_cll_sign = common_utility.get_bit_value(max_cll, 15, 15)
                            max_cll_exponent = common_utility.get_bit_value(max_cll, 10, 14)
                            max_cll_fraction = common_utility.get_bit_value(max_cll, 0, 9)  # mantissa
                            logging.debug(
                                "Sign is {0} Exponent is {1} Fraction is {2}".format(max_cll_sign, max_cll_exponent,
                                                                                     max_cll_fraction))
                            did_max_cll = perform_exponent_encoding(max_cll_sign, max_cll_exponent, max_cll_fraction)

                            ##
                            # MinCLL
                            min_cll_lsb = int(edid_data[temp_index + 28]) & 0xFF
                            min_cll_msb = int(edid_data[temp_index + 29]) & 0xFF
                            min_cll = min_cll_msb << 8 | min_cll_lsb

                            min_cll_sign = common_utility.get_bit_value(min_cll, 15, 15)
                            min_cll_exponent = common_utility.get_bit_value(min_cll, 10, 14)
                            min_cll_fraction = common_utility.get_bit_value(min_cll, 0, 9)  # mantissa
                            logging.debug(
                                "Sign is {0} Exponent is {1} Fraction is {2}".format(min_cll_sign, min_cll_exponent,
                                                                                     min_cll_fraction))
                            did_min_cll = perform_exponent_encoding(min_cll_sign, min_cll_exponent,
                                                                min_cll_fraction)

                        if prd_identification_blk and display_intrface_blk and display_param_blk and type_vii_timing_blk:
                            ##
                            # First Block should be Product Identification Block
                            if prd_blk_index < disp_intrf_index and prd_blk_index < disp_param_index and prd_blk_index < type_vii_timing_index:
                                if supported_eotf_is_2084:
                                    did_hdr_support = True
                                    is_having_valid_did_block = True
                                    break
                                else:
                                    logging.error("DID is qualified, however,HDR support is not present in the DID "
                                                  "Block")
                                    break
                            else:
                                logging.error("DID is not qualified as per OS Policy")
                                break

                        else:
                            number_of_byte = edid_data[temp_index + 2] + 3

                            temp_index += number_of_byte  # checking for next value
                            is_having_valid_did_block = False
                            continue

            ##
            # If there is a valid DID 2.0 block, then the OS will ignore the CTA block;
            else:
                if is_having_valid_did_block is False:
                    # Extension tag and revision for CEA header
                    if edid_data[block * 128] == 0x2 and edid_data[block * 129] in [0x01, 0x03]:
                        index = (block * 128) + 4  # 4 bytes for header
                        data_block = edid_data[index]
                        while data_block:
                            length = data_block & 0x1f
                            # HDR static meta data block (7 bytes)
                            # Byte 0 : Tag code = 07h (Bit 7-5) | length of data block(in bytes)  (Bit 4-0)
                            # Byte 1 : extended tag = 06h
                            # Byte 4 : Desired Content Max Luminance data (8 bits) - MaxCll
                            # Byte 5 : Desired Content Max Frame-average Luminance data (8 bits) - MaxFall
                            # Byte 6 : Desired Content Min Luminance data (8 bits) - MinCll
                            # MaxFall = MaxCll = 50 * 2^(CV/32)
                            if (data_block >> 5) == 0x7 and edid_data[index + 1] == 0x6:
                                logging.info("HDR Static Metadata Block Found in the EDID Data")
                                # Byte 2 : Supported EOTF - Bits 0 to 5 identify the EOTF supported by Sink
                                supported_eotf_is_2084 = edid_data[index + 2] >> 2
                                # Byte 3 : Supported Static Metadata Type - Bit 0 indicated Static Metadata Type 1
                                supported_static_metadata_type = edid_data[index + 3]
                                # When n > 3, each of Bytes 5 to 7 which are indicated to be present in the HDR Static
                                # Metadata Data Block may be set to zero. This value indicates that the data for the relevant
                                # Desired MaxCLL, Desired MaxFALL or Desired MinCLL is not indicated
                                if length > 3:
                                    cta_max_cll = math.floor(50 * pow(2, (edid_data[index + 4] / 32)))
                                    cta_max_fall = math.floor(50 * pow(2, (edid_data[index + 5] / 32)))
                                    cta_min_cll = round(cta_max_cll * pow((edid_data[index + 6] / 255), 2) / 100)
                                else:
                                    logging.info(
                                        "Length of data block is {0}. Desired MaxCLL, MaxFALL and MinCLL are not "
                                        "indicated".format(
                                            length))
                                logging.info("2084 {0} Static Metadata {1}".format(supported_eotf_is_2084, supported_static_metadata_type))
                                if supported_eotf_is_2084 and supported_static_metadata_type:
                                    cta_hdr_support = True
                                    logging.info("Found a CTA Block with HDR support;"
                                                 " Further checking if there is a DID Block with HDR support too")
                                    break
                            else:
                                logging.info("Got into the Else condition")
                                index += length + 1
                                data_block = edid_data[index]
            logging.info("Entered the end parts*****************")
            index += 126

    ##
    # If a valid DID block and a valid CTA block with HDR support in both the blocks are present,
    # then OS would choose the DID block over the CTA block from SV2 OS onwards.
    if did_hdr_support:
        logging.debug(
            "HDR Support {0}; MaxCLL {1} MaxFall {2} MinCLL {3}".format(did_hdr_support, did_max_cll, did_max_fall,
                                                                        did_min_cll))
        return did_hdr_support, did_max_cll, did_max_fall, did_min_cll

    if cta_hdr_support:
        logging.debug(
            "HDR Support {0}; MaxCLL {1} MaxFall {2} MinCLL {3}".format(cta_hdr_support, cta_max_cll, cta_max_fall,
                                                                        cta_min_cll))
        return cta_hdr_support, cta_max_cll, cta_max_fall, cta_min_cll
    else:
        logging.info("Warning : The EDID does not report support for HDR")
        return 0, 0, 0, 0


##
# @brief Update HDR feature support for panels
# @param[in] context_args
# @return number of HDR supported panels and dynamically updates the panels' support for HDR in the ContextArgs
def update_feature_caps_in_context(context_args):
    num_of_hdr_supported_panels = 0
    for gfx_index, adapter in context_args.adapters.items():
        for port, panel in adapter.panels.items():
            feature_caps = FeatureCaps()
            feature_caps = get_psr_caps(panel.target_id, feature_caps)
            hdr_support, max_cll, max_fall, min_cll = parse_edid_extension_block(panel.target_id,
                                                                                 panel.display_and_adapterInfo)

            if hdr_support:
                hdr_feature_caps = HDRDisplayCaps()
                hdr_feature_caps.is_hdr_supported = True
                hdr_feature_caps.desired_max_fall = max_fall
                hdr_feature_caps.desired_max_cll = max_cll
                hdr_feature_caps.desired_min_cll = min_cll
                feature_caps.HDRSupport = True
                ##
                # Dynamically adding HDRDisplayCaps Attribute to the Panel details in the context_args object
                setattr(context_args.adapters[gfx_index].panels[port], "HDRDisplayCaps",
                        hdr_feature_caps)
                ##
                # Dynamically adding FeatureCaps Attribute to the Panel details in the context_args object
                setattr(context_args.adapters[gfx_index].panels[port], "FeatureCaps",
                        feature_caps)
                num_of_hdr_supported_panels += 1
            else:
                feature_caps.HDRSupport = False
                ##
                # Dynamically adding FeatureCaps Attribute with HDRSupport as False for SDR Panels
                # to the Panel details in the context_args object
                setattr(context_args.adapters[gfx_index].panels[port], "FeatureCaps",
                        feature_caps)
    return num_of_hdr_supported_panels


##
# @brief Function to initialize the Color Properties related to each panel, both SDR and HDR
# In case of external HDR/ SDR panels, OS Relative LUT is extracted from the ETLs.
# along with Relative CSC, Default and Flip Metadata
# @param[in] target_id, int
# @param[in] current_pipe, str
# @param[in] gfx_index, str
# @param[in] panel_props, HDRProperties
# @return status, bool
def initialize_panel_color_properties(target_id: int, current_pipe: str, gfx_index: str, panel_props: HDRProperties):
    ##
    # Fetch the OSOneDLUT after enabling HDR for a HDR supported panel
    os_relative_lut = color_etl_utility.get_os_one_d_lut_from_etl(target_id)

    if os_relative_lut.__len__() == 0:
        logging.debug("No new OS OneDLUT from OS after setting the Brightness Slider")
        logging.debug("Considering the OSOneDLUT already available in the context")
        if panel_props.os_relative_lut.__len__() == 0:
            logging.error("OSOneDLUT is not available in the context and no new OS OneDLUT is available")
            gdhm.report_driver_bug_os(f"OS 1DLUT event is not available in the context for Adapter: {gfx_index} TargetId: {target_id}")
            return False
        else:
            logging.info("Considering the OSOneDLUT already available in the context")
    else:
        logging.info("OS has issued OSOneDLUT, hence overriding the LUT available in context")
        panel_props.os_relative_lut = os_relative_lut[-1]

    ##
    # Collecting the DSB Event
    # Currently DSB for Gamma is enabled on TGL;
    reg_args = registry_access.StateSeparationRegArgs(gfx_index)
    reg_value, reg_type = registry_access.read(args=reg_args, reg_name="DisplayFeatureControl")
    gamma_register_write_using_mmio = common_utility.get_bit_value(reg_value, 22, 22)
    if gamma_register_write_using_mmio == 0:
        dsb_gamma_dump = color_etl_utility.get_dsb_pipe_post_csc_gamma_from_etl(current_pipe)
        if dsb_gamma_dump.__len__() == 0:
            logging.info("No DSB event from Driver after event for Pipe {0}".format(current_pipe))
            if panel_props.dsb_gamma_dump.__len__() == 0:
                logging.error(
                    "DSB is not available in the context and no new DSB is available for {0}".format(current_pipe))
                gdhm.report_driver_bug_os("DSB is not available in the context for Pipe: {0}"
                                            " Adapter: {1} TargetId: {2}".format(current_pipe, gfx_index, target_id))
                return False
            else:
                logging.info("Considering the DSB Gamma already available in the context for Pipe {0}".format(current_pipe))
        else:
            panel_props.dsb_gamma_dump = dsb_gamma_dump
            logging.info("New DSB Gamma Dump updated for Pipe {0}".format(current_pipe))

    oned_lut_param = color_etl_utility.get_gamma_ramp_type_from_etl(target_id)
    if oned_lut_param is None:
        logging.debug("No New OneDLut Param Call after the event")
        logging.debug("Considering the OneDLut Param already available in the context")
        if panel_props.oned_lut_param_type is None:
            logging.error("OneDLutParam is not available in the content and no new Param is available for {0}".format(
                current_pipe))
            return False
        else:
            logging.info("Considering the OneDLut Param already available in the context")
            panel_props.oned_lut_param_type = panel_props.oned_lut_param_type
    else:
        logging.info("OS has issued new OneDLUT Param, hence overriding the Gamma Ramp Type available in context")
        if oned_lut_param == 'UNINITIALISED':
            panel_props.oned_lut_param_type = panel_props.oned_lut_param_type
        else:
            panel_props.oned_lut_param_type = oned_lut_param

    os_relative_csc, gamma_ramp_type = color_etl_utility.get_color_transforms_csc_from_etl(target_id)

    if os_relative_csc.__len__() == 0:
        logging.debug("No new CSC from OS after setting the Brightness Slider")
        logging.debug("Considering the CSC already available in the context")
        if panel_props.gamma_ramp_type is None:
            logging.error("OneDLutGammaRampType is not available in the content and no new Param is available for {0}".format(
                current_pipe))
            return False
        else:
            logging.info("Considering the OneDLutGammaRamp Type already available in the context")
            if panel_props.os_relative_lut.__len__() == 0:
                logging.error("CSC is not available in the context and no new OS CSC is available")
                gdhm.report_driver_bug_os("CSC is not available in the context for Adapter: {0}"
                                        " TargetId: {1}".format(gfx_index,target_id))
                return False
            else:
                logging.info("Considering the CSC already available in the context")
                panel_props.os_relative_csc = panel_props.os_relative_csc
                panel_props.gamma_ramp_type = panel_props.gamma_ramp_type
    else:
        logging.info("OS has issued new CSC, hence overriding the CSC Matrix available in context")
        panel_props.os_relative_csc = os_relative_csc[-1]
        panel_props.gamma_ramp_type = gamma_ramp_type

    ##
    # Fetch the Default Metadata from the ETL for the particular target-id
    status, default_metadata = color_etl_utility.get_default_hdr_metadata_from_etl(target_id)
    if status is False:
        logging.debug("No new Default Metadata issued by OS")
        if panel_props.flip_metadata is None:
            logging.error("Flip Metadata is not available in the context and no new Flip Metadata is available")
        logging.debug("Considering the Default Metadata already available in the context")
    else:
        logging.info("OS has issued new Default Metadata, hence overriding the Default Metadata available in context")
        ##
        # Take the latest Default Metadata from the list of metadata available
        panel_props.default_metadata = default_metadata[-1]

    ##
    # Fetch the Flip Metadata from the ETL for the particular target-id
    status, flip_metadata = color_etl_utility.get_flip_hdr_metadata_from_etl(target_id)
    if status is False:
        logging.debug("No new Flip Metadata issued by OS")
        if panel_props.flip_metadata is None:
            logging.error("Flip Metadata is not available in the context for TargetId: {0}".format(target_id))
        logging.debug("Considering the Flip Metadata already available in the context")
    else:
        logging.info("OS has issued new Flip Metadata, hence overriding the Flip Metadata available in context")
        panel_props.flip_metadata = flip_metadata

    return True


# @brief - The function which set the OS Brightness slider to a certain value
# @param[in] b3_val Brightness3 value input by the user; If None, will set a random value
# @param[in] panel_props
# @return status
def set_b3_slider(b3_val: str):
    ##
    # Set the brightness slider given as an input from command line
    # If the input is not specified, then query the Current Brightness and set a random value other than Current value
    if b3_val == 'NONE' or b3_val is None:
        logging.info("B3 Slider value is not mentioned by the user; Hence setting a random value")
        current_brightness = windows_brightness.get_current_brightness()
        if current_brightness is None:
            logging.error("FAILED to get current brightness")
        else:
            logging.info("Current Brightness is {0}".format(current_brightness))
            while True:
                b3_val = random.randint(0, 100)
                if current_brightness != b3_val:
                    break

    ##
    # Set the OS Brightness Slider to the level iterating through the list
    if common_utility.set_os_brightness(b3_val, delay=0) is False:
        return False


# @brief - The function to initialize the color properties specific to eDP HDR
#          Properties such as OSOneDLUT, SDRWhiteLevel, Brightness Value in Nits, Default and Flip Metadata
#          are updated to the context
# @param[in] target_id Target ID of the display
# @param[in] panel_props
# @param[in] wcg_support
# @return status
def initialize_edp_hdr_props(target_id: int, panel_props: HDRProperties, wcg_support:bool = False):
    ##
    # Fetch the OSOneDLUT after enabling HDR for a HDR supported panel
    os_relative_lut_after_b3 = color_etl_utility.get_os_one_d_lut_from_etl(target_id)
    if os_relative_lut_after_b3.__len__() == 0:
        logging.info("No new OS OneDLUT from OS after setting the Brightness Slider")
        logging.info("Considering the OSOneDLUT already available in the context")
        if panel_props.os_relative_lut.__len__() == 0:
            logging.error("OSOneDLUT is not available in the context and no new OS OneDLUT is available")
            return False
    else:
        logging.info("OS has issued new OSOneDLUT, hence overriding the LUT available in context")
        panel_props.os_relative_lut = os_relative_lut_after_b3[-1]

    # #
    # Note : Currently there are no APIs to set the SDRWhiteLevel Slider.
    #        Hence considering only the default value given by OS.
    sdr_white_level_in_nits = color_etl_utility.get_sdr_white_level_from_etl(target_id)
    if sdr_white_level_in_nits <= 0 and (wcg_support is False):
        logging.info("Fetching the SDRWhiteLevel if already available in the context")
        if panel_props.sdr_white_level <= 0 and (wcg_support is False):
            logging.error("SDRWhiteLevel is not available in the context and no new DDI Call with new SDRWhiteLevel "
                          "is available")
            return False
        else:
            logging.info("SDRWhiteLevel slider will not listed in SDR Capable displays,using from context [Expected]")
    else:
        logging.info("SDRWhiteLevel slider will not listed in SDR Capable displays [Expected]")
        panel_props.sdr_white_level = sdr_white_level_in_nits


    logging.info("SDRWhiteLevel is %s" % panel_props.sdr_white_level)

    brightness_val_in_nits, transition_time_in_milli_nits = color_etl_utility.get_brightness3_in_nits_and_transition_time_from_etl(
        target_id)
    if brightness_val_in_nits < 0:
        logging.info("Fetching the Brightness Value if already available in the context")
        if panel_props.b3_value < 0:
            logging.error(
                "Brightness Value is not available in the context and no new DDI Call with new Brightness Value is "
                "available")
            gdhm.report_driver_bug_os("Brightness Value is not available in the context for TargetId: {0}".format(target_id))
            return False
    else:
        logging.info("BrightnessValueInNits is %s" % brightness_val_in_nits)
        panel_props.b3_value = brightness_val_in_nits
        panel_props.b3_transition_time = transition_time_in_milli_nits
    panel_props.pixel_boost = panel_props.b3_value / panel_props.sdr_white_level

    ##
    # Fetch the Default Metadata from the ETL for the particular target-id
    status, default_metadata = color_etl_utility.get_default_hdr_metadata_from_etl(target_id)
    if status is False:
        logging.info("No new Default Metadata issued by OS")
        if panel_props.default_metadata is None:
            logging.error("Default Metadata is not available in the context and no new Default Metadata is available")
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
        if panel_props.flip_metadata is None:
            logging.error("Flip Metadata is not available in the context and no new Flip Metadata is available")
        logging.info("Considering the Flip Metadata already available in the context")
    else:
        panel_props.flip_metadata = flip_metadata

    return True


##
# @brief        Update ycbcr feature support for panels
# @param[in]    port_type  ConnectorNPortType of the display
# @param[in]    display_and_adapterInfo - display_and_adapter_info
# @param[in]    context_args - context based variables
# @return None
def update_ycbcr_caps_in_context(port_type, display_and_adapterInfo, context_args):

    ##
    # If panel supports YCbCr
    ycbcr_feature_caps = FeatureCaps()
    current_mode = display_config.DisplayConfiguration().get_current_mode(display_and_adapterInfo)

    # Only for Yangra
    reg_args = registry_access.StateSeparationRegArgs(gfx_index=display_and_adapterInfo.adapterInfo.gfxIndex)
    reg_value, reg_type = registry_access.read(args=reg_args, reg_name="ForceApplyYUV422Mode")

    if (color_escapes.ycbcr_support(port_type, display_and_adapterInfo)) or ("DP" in port_type) or \
            (current_mode.samplingMode.yuv420 == 1):
        ycbcr_feature_caps.YCbCrSupport = True
    else:
        ycbcr_feature_caps.YCbCrSupport = False

    setattr(context_args, "FeatureCaps", ycbcr_feature_caps)


##
# Initialize all the generic Color Properties related to a panel first time after enabling HDR by parsing ETL
# Properties include : OSRelativeLUT, OSRelativeCSC, Default and Flip Metadata in case of HDR Panels
# Properties include : OSRelativeLUT, OSRelativeCSC in case of SDR Panels
def initialize_common_color_props(context_args, panel_props_dict):
    for gfx_index, adapter in context_args.adapters.items():
        for port, panel in adapter.panels.items():
            panel_props = panel_props_dict[gfx_index, port]
            if panel.is_active:
                logging.info("")
                logging.info(
                    "Initializing all color properties for Panel : {0} on Adapter : {1} attached to Pipe : {2}".format(
                        port, gfx_index, panel.pipe))
                if initialize_panel_color_properties(panel.target_id, panel.pipe, gfx_index,
                                                                      panel_props) is False:
                    return False
                panel_props_dict[gfx_index, port] = panel_props


##
# Update all the generic Color Properties related to a panel after performing an event
# Properties include : OSRelativeLUT, OSRelativeCSC, Default and Flip Metadata in case of HDR Panels
# Properties include : OSRelativeLUT, OSRelativeCSC in case of SDR Panels
def update_common_color_props(after_event, target_id, current_pipe, platform, panel_props):
    if after_event is not None:
        init_etl = "After_Performing_" + after_event + "_" + "TimeStamp_"
        init_etl_path = color_etl_utility.stop_etl_capture(init_etl)
        time.sleep(20)
        if etl_parser.generate_report(init_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            return False
        else:
            ##
            # Start the ETL again for capturing other events
            if color_etl_utility.start_etl_capture() is False:
                logging.error("Failed to Start Gfx Tracer")
                return False
    if initialize_panel_color_properties(target_id, current_pipe, platform, panel_props) is False:
        return False


##
# Update all the generic Color Properties related to a panel after performing an event
# Properties include : OSRelativeLUT, OSRelativeCSC, Default and Flip Metadata in case of HDR Panels
# Properties include : OSRelativeLUT, OSRelativeCSC in case of SDR Panels
def update_common_color_props_for_all(context_args, panel_props_dict,  after_event):
    if after_event is not None:
        init_etl = "After_Performing_" + after_event + "_" + "TimeStamp_"
        init_etl_path = color_etl_utility.stop_etl_capture(init_etl)

        if etl_parser.generate_report(init_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            return False
        else:
            ##
            # Start the ETL again for capturing other events.
            if color_etl_utility.start_etl_capture() is False:
                logging.error("Failed to Start Gfx Tracer")
                return False

    for gfx_index, adapter in context_args.adapters.items():
        for port, panel in adapter.panels.items():
            panel_props = panel_props_dict[gfx_index, port]
            if initialize_panel_color_properties(panel.target_id, panel.pipe, gfx_index,
                                                                  panel_props) is False:
                return False
