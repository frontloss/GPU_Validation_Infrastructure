######################################################################################
# \file
# \section color_parse_etl_events
# \remarks
# \ref color_parse_etl_events.py \n
# This script contains helper functions that help in parsing the ETL events
# Events include HDR_DISPLAY_CAPS, OS_GIVEN_1D_LUT, SET_ADJUSTED_COLORIMETRY_INFO
# DISPLAY_BRIGHTNESS3, DSB_HDR_GAMMA
#
# \author   Smitha B
######################################################################################
import logging
from Libs.Core import etl_parser
from Tests.Color import color_common_utility


##
# Function fetches the HDR Caps of the port provided and verifies of the display supports HDR
def fetch_and_verify_hdr_caps_from_etl():
    logging.info("*************************** DISPLAY CAPS INFORMATION ***************************")
    etl_hdr_display_caps = etl_parser.get_event_data(etl_parser.Events.HDR_DISPLAY_CAPS)
    if etl_hdr_display_caps is None:
        logging.error("\tNo HDRDisplayCaps event found in ETLs")
        return False
    else:
        hdr_display_caps_list = []
        for each_display_caps in range(len(etl_hdr_display_caps)):
            hdr_display_caps_list.append(etl_hdr_display_caps[each_display_caps])

        for index in range(len(hdr_display_caps_list)):
            if hdr_display_caps_list[index].HDRMetadataBlockFound:
                logging.info("HDRMetadataBlock is FOUND")
            else:
                logging.error("HDRMetadataBlock is NOT FOUND")
                color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]HDRMetadataBlock is NOT FOUND")
                return False
            if hdr_display_caps_list[index].EOTFSupported > 4:
                logging.info("Panel supports SMPTE_ST2084 EOTF")
            else:
                logging.error("Panel does NOT support SMPTE_ST2084 EOTF")
                color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Panel does NOT support SMPTE_ST2084 EOTF")
                return False

            if hdr_display_caps_list[index].HdrStaticMetaDataType == 1:
                logging.info("HDRStaticMetadata type supported is TYPE1")
            else:
                logging.error("TYPE1 HDRStaticMetadata type is NOT supported")
                color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]TYPE1 HDRStaticMetadata type is NOT supported")
                return False
            logging.info("DesiredMaxCLL : %s; DesiredMaxFALL : %s; DesiredMinCLL : %s Port %s" % (
            hdr_display_caps_list[index].DesiredMaxCLL, hdr_display_caps_list[index].DesiredMaxFALL,
            hdr_display_caps_list[index].DesiredMinCLL, hdr_display_caps_list[index].Port))
        logging.info("****************************************************************************")
        return True


##
# Function fetches the OneDLUTData given by OS which is a relative LUT
def get_os_one_d_lut_from_etl(target_id):
    os_relative_lut_per_target_id = []
    os_given_1d_lut = etl_parser.get_event_data(etl_parser.Events.OS_GIVEN_1D_LUT)
    if os_given_1d_lut is None:
        logging.error("\tNo OSGiven1DLUT event found in ETLs")
        return False
    else:
        os_given_1d_lut_list = []
        for each_lut in range(len(os_given_1d_lut)):
            os_given_1d_lut_list.append(os_given_1d_lut[each_lut])

        for index in range(len(os_given_1d_lut_list)):
            if os_given_1d_lut_list[index].TargetId == target_id:
                os_relative_lut_per_target_id = color_common_utility.decode_os_one_d_lut(os_given_1d_lut_list[index].GammaLUTData)

        logging.debug("OS Reference LUT")
        logging.debug(os_relative_lut_per_target_id)
        return os_relative_lut_per_target_id


##
# Function fetches the OneDLUTData given by OS which is a relative LUT
def get_os_csc_from_etl(target_id):
    os_relative_csc_per_target_id = []
    os_csc_data_lut = etl_parser.get_event_data(etl_parser.Events.OS_GIVEN_CSC)
    if os_csc_data_lut is None:
        logging.error("\tNo OSGivenCSCData event found in ETLs")
        color_common_utility.gdhm_report_app_color(title="[COLOR]OSGivenCSCData event not found in ETLs")
        return False
    else:
        os_csc_list = []
        for each_lut in range(len(os_csc_data_lut)):
            os_csc_list.append(os_csc_data_lut[each_lut])

        for index in range(len(os_csc_list)):
            if os_csc_list[index].TargetId == target_id:
                os_relative_csc_per_target_id = color_common_utility.decode_os_csc_data(os_csc_list[index].Matrix3x4Data)

        logging.debug("OS Reference CSC")
        logging.debug(os_relative_csc_per_target_id)
        return os_relative_csc_per_target_id


##
# Function fetches the SDRWhiteLevel given by OS in Nits
def get_sdr_white_level_from_etl(target_id):
    return 80
    # Hardcoding to 80 as it doesnt change today, below etl event depricated in Display provider
    # Todo: below event moved to GFX provider, need to parse the same and set
    # sdr_white_level_data = etl_parser.get_event_data(etl_parser.Events.SET_ADJUSTED_COLORIMETRY_INFO)

    # sdr_white_level_per_target_id = False
    # sdr_white_level_data = etl_parser.get_event_data(etl_parser.Events.SET_ADJUSTED_COLORIMETRY_INFO)
    # if sdr_white_level_data is None:
    #     logging.error("\tNo SetAdjustedColorimetry event found in ETLs (OS Issue)")
    #     return False
    # else:
    #     sdr_white_level_list = []
    #     for each_sdr_white_level_entry in range(len(sdr_white_level_data)):
    #         sdr_white_level_list.append(sdr_white_level_data[each_sdr_white_level_entry])

    #     for index in range(len(sdr_white_level_list)):
    #         if target_id == sdr_white_level_list[index].TargetId:
    #             sdr_white_level_per_target_id = sdr_white_level_list[index].SdrWhiteLevel
    #     return sdr_white_level_per_target_id


##
# Fetches the Brightness3 value in MilliNits given by OS and
# returns the Brightness value after converting to Nits for a particular TargetID
def get_brightness3_in_nits_from_etl(target_id):
    brightness_value_per_target_id = False
    brightness_list = []
    edp_hdr_brightness3_data = etl_parser.get_event_data(etl_parser.Events.DISPLAY_BRIGHTNESS3)
    if edp_hdr_brightness3_data is None:
        logging.error("\tNo Brightness3 event found in ETLs (OS Issue)")
        return False
    else:
        for each_entry_in_brightness3 in range(len(edp_hdr_brightness3_data)):
            brightness_list.append(edp_hdr_brightness3_data[each_entry_in_brightness3])

        for brightness_index in range(len(brightness_list)):
            if target_id == brightness_list[brightness_index].TargetId:
                brightness_value_per_target_id = brightness_list[brightness_index].BrightnessMillinits / 1000
    return brightness_value_per_target_id


##
# Fetches the Transition time in MilliNits given by OS for a particular TargetID
def get_smooth_brightness_transition_time_from_etl(target_id):
    transition_time_in_milli_nits = 0
    brightness_list = []
    edp_hdr_brightness3_data = etl_parser.get_event_data(etl_parser.Events.DISPLAY_BRIGHTNESS3)
    if edp_hdr_brightness3_data is None:
        logging.error("\tNo Brightness3 event found in ETLs (OS Issue)")
        return False
    else:
        for each_entry_in_brightness3 in range(len(edp_hdr_brightness3_data)):
            brightness_list.append(edp_hdr_brightness3_data[each_entry_in_brightness3])

        for brightness_index in range(len(brightness_list)):
                if target_id == brightness_list[brightness_index].TargetId:
                    transition_time_in_milli_nits = brightness_list[brightness_index].TransitionTimeMs
        return transition_time_in_milli_nits


##
# Fetches the DSB Gamma Dump from the ETL
def get_dsb_gamma_from_etl(pipe_id, is_smooth_brightness=False, total_steps=1, step_index=0):
    hdr_gamma_list = []
    gamma_lut = False
    dsb_hdr_gamma_data = etl_parser.get_event_data(etl_parser.Events.DSB_HDR_GAMMA)
    if dsb_hdr_gamma_data is None:
        logging.error("\tNo DSB Initialize event in the ETLs(Driver Issue)")
        return False
    else:
        for each_entry_in_dsb_hdr_gamma in range(len(dsb_hdr_gamma_data)):
            hdr_gamma_list.append(dsb_hdr_gamma_data[each_entry_in_dsb_hdr_gamma])
        for index in range(0, len(hdr_gamma_list)):
            if pipe_id == hdr_gamma_list[index].PipeID:
                if is_smooth_brightness:
                    if total_steps != len(hdr_gamma_list):
                        logging.error("Expected Gamma Calls : %s Actual Gamma Calls : %s" %(total_steps, len(hdr_gamma_list)))
                        return False
                    ##
                    # Fetch Gamma LUT for the particular step
                    gamma_lut = hdr_gamma_list[step_index].BufferData
                    break
                ##
                # Fetch Gamma LUT for the final step_index
                gamma_lut = hdr_gamma_list[len(hdr_gamma_list) - 1].BufferData
                break
    return gamma_lut