######################################################################################################
# @file         color_etl_utility.py
# @brief        This script contains helper functions that help in parsing the ETL events used in color feature
#               Events include :
#               1. HDR_DISPLAY_CAPS
#               2. OS_GIVEN_1D_LUT
#               3. SET_ADJUSTED_COLORIMETRY_INFO
#               4. DISPLAY_BRIGHTNESS3 and TRANSITION_TIME
#               5. DSB_HDR_GAMMA
#               6. DEFAULT_HDR_METADATA
#               7. OS_3x4_COLOR_TRANSFORMS_MATRIX
#               The script also includes helper functions which help in decoding the binary data
#               fetched from the ETL in case of OS OneDLUT and the 3x4ColorTransforms Matrix
# @author       Smitha B
######################################################################################################
import logging
import os
import time
from Libs.Core import etl_parser
from Libs.Core.test_env import test_context
from Libs.Core.logger import etl_tracer
from Tests.Color.Common import common_utility
from Tests.Color.Common import color_properties
from Tests.Planes.Common import planes_verification
from Libs.Core.logger import gdhm



##
# @brief        Helper function to fetch the HDR Caps of the port provided and
#               verify whether the display supports HDR
# @param[in]    port - portType of the display
# @return       HDRDisplayCaps
def get_hdr_caps_from_etl(port: str):
    hdr_caps_obj = color_properties.HDRDisplayCaps()
    etl_hdr_display_caps = etl_parser.get_event_data(etl_parser.Events.HDR_DISPLAY_CAPS)
    if etl_hdr_display_caps is None:
        logging.info("No HDRDisplayCaps event found in ETLs")
        hdr_caps_obj.isHDRSupported = False
    else:
        hdr_display_caps_list = []
        for each_display_caps in range(len(etl_hdr_display_caps)):
            hdr_display_caps_list.append(etl_hdr_display_caps[each_display_caps])

        for index in range(len(hdr_display_caps_list)):
            if port == hdr_display_caps_list[index].Port:
                if hdr_display_caps_list[index].HDRMetadataBlockFound and hdr_display_caps_list[index].EOTFSupported > 4 \
                        and hdr_display_caps_list[index].HdrStaticMetaDataType == 1:
                    hdr_caps_obj.is_hdr_supported = True
                else:
                    hdr_caps_obj.is_hdr_supported = False
                hdr_caps_obj.desired_max_cll = hdr_display_caps_list[index].DesiredMaxCLL
                hdr_caps_obj.desired_max_fall = hdr_display_caps_list[index].DesiredMaxFALL
                hdr_caps_obj.desired_min_cll = hdr_display_caps_list[index].DesiredMinCLL
                logging.info(
                    "Port : {0} - MetadataBlockFound : {1}, EOTFSupported : {2}, HDRStaticMetadataType : {3}".format(
                        port, hdr_display_caps_list[index].HDRMetadataBlockFound, hdr_display_caps_list[index].EOTFSupported,
                        hdr_display_caps_list[index].HdrStaticMetaDataType))
                logging.debug("Port : {0} - DesiredMaxCLL :{1} ; DesiredMaxFALL :{2}; DesiredMinCLL : {3}".format(port,
                    hdr_display_caps_list[index].DesiredMaxCLL, hdr_display_caps_list[index].DesiredMaxFALL,
                    hdr_display_caps_list[index].DesiredMinCLL))
        return hdr_caps_obj


##
# @brief        Helper function to verify if OS has issued a HDR modeset
# @param[in]    pipe - pipe attached to the display
# @param[in]    feature - str value denoting the feature to be verified. By default HDR, can be used for WCG
# @return       Status, BPC - bool, int
def fetch_feature_modeset_details_from_os(pipe_id: str, feature: str = 'HDR'):
    pipe_id = 'PIPE_' + pipe_id
    set_timing_list = []
    set_timing_color_event = etl_parser.get_event_data(etl_parser.Events.SET_TIMING_COLOR)
    if set_timing_color_event is None:
        logging.error("No {0} Modeset from OS captured in ETL".format(feature))
        return False, 8
    for each_event in range(len(set_timing_color_event)):
        set_timing_list.append(set_timing_color_event[each_event])

    for index in range(len(set_timing_list)):
        if set_timing_list[index].Pipe == pipe_id:
            if feature == 'HDR':
                if (set_timing_list[index].Encoding == 'DD_COLOR_ENCODING_ST2084' and
                        set_timing_list[index].Gamut == 'DD_COLOR_GAMUT_2020' and
                        set_timing_list[index].ContentType == 'DD_CONTENT_TYPE_HDR'):
                    return True, set_timing_list[index].BPC
            else:
                if set_timing_list[index].ContentType == 'DD_CONTENT_TYPE_WCG':
                    return True, set_timing_list[index].BPC
            logging.debug("Modeset from OS received with Encoding {0} Gamut {1} ContentType {2} BPC {3}".format(
                set_timing_list[index].Encoding, set_timing_list[index].Gamut, set_timing_list[index].ContentType,
                set_timing_list[index].BPC))
    return False, 8


##
# @brief        Helper function to fetch the OneDLUTData given by OS which is a relative LUT
# @param[in]    target_id - TargetID of the display
# @return       os_relative_lut_per_target_id - List of all the OneDLUTData for the target_id
def get_os_one_d_lut_from_etl(target_id: int):
    os_relative_lut_per_target_id = []
    os_given_1d_lut = etl_parser.get_event_data(etl_parser.Events.OS_GIVEN_1D_LUT)
    if os_given_1d_lut is None:
        logging.error("No OSGiven1DLUT event found in ETLs")
    else:
        os_given_1d_lut_list = []
        for each_lut in range(len(os_given_1d_lut)):
            os_given_1d_lut_list.append(os_given_1d_lut[each_lut])

        for index in range(len(os_given_1d_lut_list)):
            if os_given_1d_lut_list[index].TargetId == target_id:
                os_relative_lut_per_target_id.append(__decode_os_one_d_lut(os_given_1d_lut_list[index].GammaLUTData))

    return os_relative_lut_per_target_id


##
# @brief        Helper function to fetch the CSC Data given by OS
# @param[in]    target_id - TargetID of the display
# @return       os_relative_csc_per_target_id - List of all the CSCData for the target_id
def get_color_transforms_csc_from_etl(target_id: int):
    os_relative_csc_per_target_id = []
    gamma_ramp_type = None
    os_csc_data_lut = etl_parser.get_event_data(etl_parser.Events.OS_GIVEN_CSC)
    if os_csc_data_lut is None:
        logging.error("No OSGivenCSCData event found in ETLs")
        common_utility.gdhm_report_app_color(title="OSGivenCSCData event not found in ETLs")
    else:
        os_csc_list = []
        for each_lut in range(len(os_csc_data_lut)):
            os_csc_list.append(os_csc_data_lut[each_lut])

        for index in range(len(os_csc_list)):
            if os_csc_list[index].TargetId == target_id:
                os_relative_csc_per_target_id.append(__decode_os_csc_data(os_csc_list[index].Matrix3x4Data))
                gamma_ramp_type = os_csc_list[index].GammaRampType
    return os_relative_csc_per_target_id, gamma_ramp_type


##
# @brief        Helper function to fetch the Gamma Ramp Type given by OS
# @param[in]    target_id - TargetID of the display
# @return       gamma_ramp_type - List of all the Gamma Ramp type details for the target_id
def get_gamma_ramp_type_from_etl(target_id: int):
    gamma_ramp_type = None
    os_oned_lut_param = etl_parser.get_event_data(etl_parser.Events.OS_1D_LUT_PARAM)
    if os_oned_lut_param is None:
        logging.error("No OSOneDLUTParam event found in ETLs")
        common_utility.gdhm_report_app_color(title="OSOneDLUTParam event not found in ETLs")
    else:
        os_onedlut_param_list = []
        for each_lut in range(len(os_oned_lut_param)):
            os_onedlut_param_list.append(os_oned_lut_param[each_lut])

        for index in range(len(os_onedlut_param_list)):
            if os_onedlut_param_list[index].TargetID == target_id:
                gamma_ramp_type = os_onedlut_param_list[index].Type
    return gamma_ramp_type


##
# @brief        Helper function to fetch the SDRWhiteLevel given by OS in Nits
# @param[in]    target_id - TargetID of the display
# @return       sdr_white_level_per_target_id - SDRWhiteLevel for the targetID in Nits
def get_sdr_white_level_from_etl(target_id: int):
    return 80
    # Hardcoding to 80 as it doesnt change today, below etl event depricated in Display provider
    # Todo: below event moved to GFX provider, need to parse the same and set
    # sdr_white_level_data = etl_parser.get_event_data(etl_parser.Events.SET_ADJUSTED_COLORIMETRY_INFO)

    # sdr_white_level_per_target_id = -1
    # sdr_white_level_data = etl_parser.get_event_data(etl_parser.Events.SET_ADJUSTED_COLORIMETRY_INFO)
    # etl_parser.get_event_data(etl_parser.Events.SET_ADJUSTED_COLORIMETRY_INFO)
    # if sdr_white_level_data is None:
    #     logging.error("No SetAdjustedColorimetry event found in ETLs (OS Issue)")
    # else:
    #     sdr_white_level_list = []
    #     for each_sdr_white_level_entry in range(len(sdr_white_level_data)):
    #         sdr_white_level_list.append(sdr_white_level_data[each_sdr_white_level_entry])

    #     for index in range(len(sdr_white_level_list)):
    #         if target_id == sdr_white_level_list[index].TargetId:
    #             sdr_white_level_per_target_id = sdr_white_level_list[index].SdrWhiteLevel
    # return sdr_white_level_per_target_id


##
# @brief        Helper function to fetch the Brightness3 value in MilliNits given by OS and
#               returns the Brightness value after converting to Nits for a particular TargetID
# @param[in]    target_id - TargetID of the display
# @return       get_brightness3_in_nits_from_etl, transition_time_in_milli_nits
#               - Tuple of Brightnessvalue in Nits and TransitionTime in MilliNits for the targetID
def get_brightness3_in_nits_and_transition_time_from_etl(target_id: int):
    brightness_value_per_target_id = -1
    transition_time_in_milli_nits = -1
    brightness_list = []
    __edp_hdr_brightness3_data = etl_parser.get_event_data(etl_parser.Events.DISPLAY_BRIGHTNESS3)
    if __edp_hdr_brightness3_data is None:
        logging.error("No Brightness3 event found in ETLs (OS Issue)")
        common_utility.gdhm_report_app_color(title="Brightness3 event not found in ETLs")
    else:
        for each_entry_in_brightness3 in range(len(__edp_hdr_brightness3_data)):
            brightness_list.append(__edp_hdr_brightness3_data[each_entry_in_brightness3])

        for brightness_index in range(len(brightness_list)):
            if target_id == brightness_list[brightness_index].TargetId:
                brightness_value_per_target_id = brightness_list[brightness_index].BrightnessMillinits / 1000
                transition_time_in_milli_nits = brightness_list[brightness_index].TransitionTimeMs
    return brightness_value_per_target_id, transition_time_in_milli_nits


##
# @brief        Helper function to fetch DSB Gamma Dump from the ETL
# @param[in]    pipe_id - pipeID of the display
# @param[in]    is_smooth_brightness - Default is False
# @param[in]    total_steps - Default is 1, In case of Smooth Brightness Verification,
#               signifies the total no. of Gamma calls for a change in slider value
# @param[in]    step_index - Default is 0, In case of Smooth Brightness Verification,
#               signifies the particular gamma entry in the list
# @return       hdr_gamma_list - List of all the DSB Gamma calls in the ETL
def get_dsb_pipe_post_csc_gamma_from_etl(pipe_id: str, is_smooth_brightness=False, total_steps=1, step_index=0):
    hdr_gamma_list = []
    pipe_id = 'PIPE_' + pipe_id
    pipe_post_csc_gamma_list = []
    dsb_hdr_gamma_data = etl_parser.get_event_data(etl_parser.Events.DSB_HDR_GAMMA)
    if dsb_hdr_gamma_data is None:
        logging.error("No DSB Initialize event in the ETLs(Driver Issue)")
        gdhm.report_driver_bug_os("DSB events are not found in ETL")
        return pipe_post_csc_gamma_list
    else:
        for each_entry_in_dsb_hdr_gamma in range(len(dsb_hdr_gamma_data)):
            hdr_gamma_list.append(dsb_hdr_gamma_data[each_entry_in_dsb_hdr_gamma])

        dsb_event_counter = 0
        for index in range(0, len(hdr_gamma_list)):
            if pipe_id == hdr_gamma_list[index].PipeID:
                if is_smooth_brightness:
                    if total_steps != len(hdr_gamma_list):
                        logging.error(
                            "Expected Gamma Calls : %s Actual Gamma Calls : %s" % (total_steps, len(hdr_gamma_list)))
                        return False
                    ##
                    # Fetch Gamma LUT for the particular step
                    pipe_post_csc_gamma_list = hdr_gamma_list[step_index].BufferData
                    break
                else:
                    pipe_post_csc_gamma_list.append(hdr_gamma_list[index].BufferData)
            else:
                dsb_event_counter += 1
                if dsb_event_counter > len(hdr_gamma_list):
                    logging.error("No DSB Initialize event in the ETLs for the Pipe {0}".format(pipe_id))
                    return pipe_post_csc_gamma_list
    return pipe_post_csc_gamma_list


##
# @brief        Helper function to fetch HDR Static Metadata from the ETLs
# @param[in]    target_id - target_id of the display
# @return       hdr_metadata_list - List of all the HDR Static Metadata for a targetID in the ETL
def get_default_hdr_metadata_from_etl(target_id: int):
    status = False
    hdr_metadata_list = []
    default_hdr_metadata = []
    hdr_metadata_dump = etl_parser.get_event_data(etl_parser.Events.DEFAULT_HDR_METADATA)
    metadata_scenario = color_properties.HDRMetadataScenario()

    if hdr_metadata_dump is None:
        if (metadata_scenario.reboot == 1) or (metadata_scenario.hotplug == 1) or (metadata_scenario.brightness_change == 1):
            logging.error("No Default HDR Metadata event in the ETLs")
            gdhm.report_driver_bug_os("HDR Metadata event is not available in the ETL")
        return status, default_hdr_metadata
    else:
        for each_entry_in_hdr_metadata_dump in range(len(hdr_metadata_dump)):
            hdr_metadata_list.append(hdr_metadata_dump[each_entry_in_hdr_metadata_dump])

        for index in range(0, len(hdr_metadata_list)):
            if target_id == hdr_metadata_list[index].TargetID:
                prog_metadata = color_properties.HDRStaticMetadata(hdr_metadata_list[index].EOTF,
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesX0),
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesX1),
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesX2),
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesY0),
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesY1),
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesY2),
                                                                   __metadata_correction(hdr_metadata_list[index].WhitePointX),
                                                                   __metadata_correction(hdr_metadata_list[index].WhitePointY),
                                                                   __metadata_correction(
                                                                       hdr_metadata_list[index].MaxMasteringLuminance),
                                                                   __metadata_correction(hdr_metadata_list[index].MinMasteringluminance),
                                                                   __metadata_correction(hdr_metadata_list[index].MaxCLL),
                                                                   __metadata_correction(hdr_metadata_list[index].MaxFALL))
                hdr_metadata_info = color_properties.OSHdrMetadata(target_id, hdr_metadata_list[index].HDRType,
                                                                   prog_metadata)
                default_hdr_metadata.append(hdr_metadata_info)
        if default_hdr_metadata.__len__() == 0:
            logging.error("No Default Metadata found for {0}".format(target_id))
            return status, default_hdr_metadata
        status = True
    return status, default_hdr_metadata


##
# @brief        Helper function to fetch HDR Static Metadata from the ETLs
# @param[in]    target_id - target_id of the display
# @return       hdr_metadata_list - List of all the HDR Static Metadata for a targetID in the ETL
def get_flip_hdr_metadata_from_etl(target_id: int):
    status = False
    hdr_metadata_list = []
    flip_hdr_metadata = []
    hdr_metadata_dump = etl_parser.get_event_data(etl_parser.Events.FLIP_HDR_METADATA)
    if hdr_metadata_dump is None:
        logging.error("No Flip HDR Metadata event in the ETLs")
        common_utility.gdhm_report_app_color(title="Flip HDR Metadata event not found in ETLs")
    else:
        for each_entry_in_hdr_metadata_dump in range(len(hdr_metadata_dump)):
            hdr_metadata_list.append(hdr_metadata_dump[each_entry_in_hdr_metadata_dump])
        for index in range(0, len(hdr_metadata_list)):
            if target_id == hdr_metadata_list[index].TargetID:
                prog_metadata = color_properties.HDRStaticMetadata(hdr_metadata_list[index].EOTF,
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesX0),
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesX1),
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesX2),
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesY0),
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesY1),
                                                                   __metadata_correction(hdr_metadata_list[index].DisplayPrimariesY2),
                                                                   __metadata_correction(hdr_metadata_list[index].WhitePointX),
                                                                   __metadata_correction(hdr_metadata_list[index].WhitePointY),
                                                                   __metadata_correction(hdr_metadata_list[index].MaxMasteringLuminance),
                                                                   __metadata_correction(hdr_metadata_list[index].MinMasteringluminance),
                                                                   __metadata_correction(hdr_metadata_list[index].MaxCLL),
                                                                   __metadata_correction(hdr_metadata_list[index].MaxFALL))
                hdr_metadata_info = color_properties.OSHdrMetadata(target_id, hdr_metadata_list[index].HDRType,
                                                                   prog_metadata)
                flip_hdr_metadata.append(hdr_metadata_info)
        status = True
    return status, flip_hdr_metadata


##
# @brief        Helper function to fetch Optimization Level issued by OS
# @param[in]    target_id - target id of the display
# @return       True if OS has issued the DDI and the Optimization Level
def get_blc_ddi3_optimization(target_id: int):
    blc_ddi3_optimization = etl_parser.get_event_data(etl_parser.Events.BLC_DDI3_OPTIMIZATION)
    if blc_ddi3_optimization is None:
        logging.error("No BlcDdi3Optimization event in the ETLs")
        return False, 0

    for index in range(len(blc_ddi3_optimization)):
        if target_id == blc_ddi3_optimization[index].TargetId:
            return True, blc_ddi3_optimization[index].OptimizationLevel


##
# @brief        Helper function to stop any ETL Capture
# @param[in]    custom_etl_name - Custom ETL Name
# @return       etl_file_path - Path of the ETL Captured
def stop_etl_capture(custom_etl_name: str):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTrace_' + custom_etl_name + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if os.path.exists(etl_tracer.GFX_BOOT_TRACE_ETL_FILE):
        file_name = 'GfxTrace_' + custom_etl_name + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_BOOT_TRACE_ETL_FILE, etl_file_path)

    return etl_file_path


##
# @brief        Helper function to stop any ETL Capture
# @return       result - Bool value indicating the result of the start_etl_tracer
def start_etl_capture():
    result = False
    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start Gfx Tracer")
        return result
    result = True
    return result


#####################################################################################################
################################### Misc helper functions ###########################################
#####################################################################################################
##
# @brief        Helper function to decode the OneDLut given by OS
# @param[in]    os_given_1d_lut - Binary data from the ETL
# @return       one_d_lut_in_single_prec_format - OneDLUT in single precision float format
def __decode_os_one_d_lut(os_given_1d_lut):
    one_d_lut = []
    one_d_lut_in_single_prec_format = []
    for index in range(0, len(os_given_1d_lut)):
        ##
        # Just to make sure that only 32 bits/Uint32 is being considered
        val = int(os_given_1d_lut[index]) & 0xFFFFFFFF
        one_d_lut.append(val)

    for index in range(0, len(one_d_lut)):
        one_d_lut_in_single_prec_format.append(__convert_int_to_float(one_d_lut[index]))
    return one_d_lut_in_single_prec_format


##
# @brief        Helper function to get the mantissa value
# @param[in]    bin_mantissa - binary value
# @return       sum - mantissa value
def __get_mantissa(bin_mantissa):
    sum = 1.0
    i = 22
    while i >= 0:
        bit = bin_mantissa >> i & 1
        power = pow(2, i - 23)
        sum += power * bit
        i = i - 1
    return sum


##
# @brief        Helper function to convert integer to single precision float
# @param[in]    bin_expo - binary value
# @return       exponent - Exponent value
def __get_exponent(bin_expo):
    exponent = 0.0
    i = 7
    while i >= 0:
        bit = bin_expo >> i & 1
        power = pow(2, i)
        exponent += power * bit
        i -= 1
    return (exponent - 127)


##
# @brief        Helper function to convert integer to single precision float
# @param[in]    int_value - integer value
# @return       float_val - Single precision float value
#               (https://en.wikipedia.org/wiki/Single-precision_floating-point_format)
def __convert_int_to_float(int_value):
    sign_mask = 0x80000000
    expo_mask = 0x7F800000
    mantissa_mask = 0x7FFFFF
    mantissa = int_value & mantissa_mask
    expo = (int_value & expo_mask) >> 23
    sign = (int_value & sign_mask) >> 31
    isign = -1 if sign == 0b1 else 1
    float_val = isign * __get_mantissa(mantissa) * pow(2, __get_exponent(expo))
    return float_val


##
# Decoding the OneDLut given by OS
def __decode_os_csc_data(os_csc_data):
    csc_lut, csc_lut_in_single_prec_format, flat_matrix = [], [], []
    for index in range(0, len(os_csc_data), 4):
        ##
        # Just to make sure that only one byte is being considered
        val1 = int(os_csc_data[index]) & 0xFF
        val2 = int(os_csc_data[index + 1]) & 0xFF
        val3 = int(os_csc_data[index + 2]) & 0xFF
        val4 = int(os_csc_data[index + 3]) & 0xFF
        value = val4 << 24 | val3 << 16 | val2 << 8 | val1
        csc_lut.append(value)

    for index in range(0, len(csc_lut)):
        csc_lut_in_single_prec_format.append(__convert_int_to_float(csc_lut[index]))

    ##
    # Create a 3x4 matrix from a flat matrix
    csc_lut = [csc_lut_in_single_prec_format[i:i + 4] for i in range(0, len(csc_lut_in_single_prec_format), 4)]
    ##
    # Considering only 3x3 matrix and discarding the 3x1 matrix
    for i in range(0, 3):
        for j in range(0, 3):
            flat_matrix.append(csc_lut[i][j])
    csc_data = [flat_matrix[i:i + 3] for i in range(0, len(flat_matrix), 3)]

    return csc_data


##
# WA for converting numbers greater than 2^15 which are getting translated as negative numbers
# when parsed from the ETLs
def __metadata_correction(metadata_value):
    return int(format(metadata_value if metadata_value >= 0 else (1 << 16) + metadata_value, '016b'), 2)


def get_plane_id(pipe, gfx_index):
    flip_data = etl_parser.get_flip_data(f'PIPE_{pipe}')
    if planes_verification.check_layer_reordering(gfx_index):
        plane_id = []
        if flip_data is None:
            return 1  # Default Plane ID, For VPB scenario need to update. # mtl - vpb = 2 and lnl - vpb = 2
        for flip in flip_data:
            for flip_id in flip.FlipAddressList:
                plane_id.append(flip_id.PlaneID)

        unique_plane_ids = list(set(plane_id))
        if not unique_plane_ids:  # Check if the list is empty
            return 1  # Default Plane ID if the list is empty
        else:
            logging.info("Unique Plane IDs: %s", unique_plane_ids)
            return str(unique_plane_ids[-1] + 1)

    else:
        plane_id = []
        if flip_data is None:
            return 3  # Default Plane ID, For VPB scenario Need to update.# mtl - vpb = 2 and lnl - vpb = 2
        for flip in flip_data:
            for flip_id in flip.FlipAddressList:
                plane_id.append(flip_id.PlaneID)
                # logging.info(flip.PlaneCount)
                
        unique_plane_ids = list(set(plane_id))
        if not unique_plane_ids:  # Check if the list is empty
            return 3  # Default Plane ID if the list is empty
        else:
            logging.info("Unique Plane IDs: %s", unique_plane_ids)
            return str(unique_plane_ids[0] + 1)


