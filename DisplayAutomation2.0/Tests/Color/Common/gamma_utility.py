######################################################################################################
# @file         gamma_utility.py
# @brief        Contains all the helper functions and the utilities used for Plane and Pipe Gamma verification
#               which could be utilized by the DFT and the E2E test scripts in both SDR and HDR modes
#               Entry functions for verification wrapper :
#               Common functions between Legacy and Gen13+ - MMIO
#               1.get_plane_degamma_lut_from_register()
#               2.get_plane_gamma_lut_from_register
#
#               Legacy(Gen11 and Gen12) - MMIO
#               1.get_pipe_degamma_lut_from_register_legacy
#               2.get_pipe_gamma_lut_from_register_legacy()
#
#               Legacy(Gen11 and Gen12) - ETL
#               1. get_programmed_mmio_pipe_gamma_data_from_etl_legacy()
#               2. get_programmed_dsb_pipe_gamma_data_from_etl_legacy()
#
#               Gen13+ - MMIO
#               1.get_pipe_degamma_lut_from_register()
#               2.get_pipe_gamma_lut_from_register()
#
#               Gen13+ - ETL
#               1.get_programmed_mmio_pipe_gamma_data_from_etl()
#               2.get_programmed_dsb_pipe_gamma_data_from_etl()
#
#
# @author       Smitha B
######################################################################################################
import os
import logging
import math
from Libs.Core.test_env import test_context
from Libs.Core import etl_parser
from Tests.Color.Common import color_etl_utility
from Tests.Color.Common import common_utility, color_mmio_interface, color_constants
from Tests.Color import color_common_constants as const

m1 = 0.1593017578125
m2 = 78.84375
c1 = 0.8359375
c2 = 18.8515625
c3 = 18.6875


######################################################################################
############################# All Gamma Helpers ######################################
######################################################################################
##
# @brief        Exposed API to combine two luts
# @param[in]    lut, list, reference lut on which interpolation is applied
# @param[in]    num_of_samples, int, samples in the reference lut
# @param[in]    input_value, int, input value to look up in the reference lut
# @return       output - float, interpolated value
def combine_luts(lut: list, num_of_samples: int, input_value: float) -> float:
    temp = input_value * (num_of_samples - 1)
    x1 = int(math.floor(temp))
    x2 = x1 if (x1 == (num_of_samples - 1)) else x1 + 1
    y1 = lut[x1]
    y2 = lut[x2]
    x = temp
    if x2 == x1:
        output = y1
    else:
        y = y1 + (((x - x1) * (y2 - y1)) / (x2 - x1))
        output = y

    return output


##
# @brief        Exposed API to To apply to 2084 OETF curve for the given input values
# @param[in]    input_val, float
# @return       output - float
def oetf_2084(input_val: float, src_max_luminance: float = 10000.0) -> float:
    output = 0.0
    if input_val != 0.0:
        cf = src_max_luminance / 10000.0
        input_val = input_val * cf
        output = pow(((c1 + (c2 * pow(input_val, m1))) / (1 + (c3 * pow(input_val, m1)))), m2)
    return output


##
# @brief        Exposed API to apply gamma with scale factors of choice of the three R-G-B channels
# @param[in]    r_factor, float
# @param[in]    g_factor, float
# @param[in]    b_factor, float
def eotf_2084(input_value):
    output = 0.0

    if input != 0.0:
        output = pow(((max((pow(input_value, (1.0 / m2)) - c1), 0)) / (c2 - (c3 * pow(input_value, (1.0 / m2))))),
                     (1.0 / m1))

    return output


##
# @brief        Exposed API to apply gamma with scale factors of choice of the three R-G-B channels
# @param[in]    r_factor, float
# @param[in]    g_factor, float
# @param[in]    b_factor, float
def convert_encoded_code_word_to_brightness(lut_data, max_value):
    final_lut = []
    for index in range(0, len(lut_data)):
        normalized_input = lut_data[index] / (65536 - 1)
        ##
        # In HDR, the normalized 1.0 value is equal to 10000 Nits according to the spec
        eotf_val = 10000 * eotf_2084(normalized_input)
        if eotf_val > max_value:
            eotf_val = max_value
        final_lut.append((eotf_val))
    return final_lut


##
# @brief        Exposed API to apply gamma with scale factors of choice of the three R-G-B channels
# @param[in]    r_factor, float
# @param[in]    g_factor, float
# @param[in]    b_factor, float
def apply_gamma(r_factor: float = 1.0, g_factor: float = 1.0, b_factor: float = 1.0):
    logging.info(
        "Applying Gamma LUT with R_ScaleFactor : {0}, G_ScaleFactor : {1}, B_ScaleFactor : {2}".format(r_factor,
                                                                                                       g_factor,
                                                                                                       b_factor))
    executable = 'UnityGamma.exe' + ' ' + '-r' + ' ' + repr(r_factor) + ' ' + '-g' + ' ' + repr(
        g_factor) + ' ' + '-b' + ' ' + repr(b_factor)
    current_dir = os.getcwd()
    os.chdir(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'HDR'))
    os.system(executable)
    os.chdir(current_dir)
    logging.info(
        "Successfully applied Gamma LUT with R_ScaleFactor : {0}, G_ScaleFactor : {1}, B_ScaleFactor : {2}".format(
            r_factor, g_factor, b_factor))


##
# @brief        Exposed API to get the standard SRGB Encoding for a given input value
# @param[in]    input_value, float
def get_srgb_encoding(input_value: float) -> float:
    if input_value <= 0.0031308:
        output = input_value * 12.92
    else:
        output = (1.055 * pow(input_value, 1.0 / 2.4)) - 0.055
    return output


##
# @brief        Exposed API to get the standard SRGB Decoding for a given input value
# @param[in]    input_value, float
def get_srgb_decoding(input_value: float) -> float:
    if input_value <= 0.04045:
        output = input_value / 12.92
    else:
        output = pow(((input_value + 0.055) / 1.055), 2.4)
    return output


##
# @brief        Exposed API to generate the standard SRGB Encoding lut of required lut size
# @param[in]    lut_size, int
# @param[in]    output_lut, list
def generate_srgb_encoding_lut(lut_size: int) -> list:
    output_lut = []
    for i in range(0, lut_size):
        input_value = (i / (lut_size - 1))
        output_lut.append(get_srgb_encoding(input_value))
    return output_lut


##
# @brief        Exposed API to generate the standard SRGB Decoding lut of required lut size
# @param[in]    lut_size, int
# @return        output_lut, list
def generate_srgb_decoding_lut(lut_size: int) -> list:
    output_lut = []
    for i in range(0, lut_size):
        input_value = (i / (lut_size - 1))
        bit_value = min(get_srgb_decoding(input_value) * 16777216, 16777216)
        output_lut.append(bit_value)
    return output_lut


def generate_unity_lut(samples, max_val):
    lut_data = []
    for index in range(0, samples):
        normalized_input = index / (samples - 1)
        val = math.ceil(max_val * normalized_input)
        print("Val :", val, "MaxVal :", max_val)
        if val > max_val:
            lut_data.append(max_val)
        else:
            lut_data.append(val)
    return lut_data


def generate_unity_lut_val(normalized_input, max_val):
    val = math.ceil(max_val * normalized_input)
    if val > max_val:
        return max_val
    return val


##
# @brief        Exposed API to generate a reference gamma _lut with scaled R-G-B factors
# @param[in]    gamma_lut, list
# @param[in]    r_factor, float, values ranging between 0.5 to 1.0
# @param[in]    g_factor, float, values ranging between 0.5 to 1.0
# @param[in]    b_factor, float, values ranging between 0.5 to 1.0
# @return        gamma_lut_scaled, list
def generate_scaled_gamma_lut(gamma_lut: list, r_factor: float = 1.0, g_factor: float = 1.0,
                              b_factor: float = 1.0) -> list:
    gamma_lut_scaled = []
    for index in range(0, len(gamma_lut)):
        gamma_lut_scaled.append(min((gamma_lut[index] * b_factor), 65535))
        gamma_lut_scaled.append(min((gamma_lut[index] * g_factor), 65535))
        gamma_lut_scaled.append(min((gamma_lut[index] * r_factor), 65535))
    return gamma_lut_scaled


##
# @brief        Exposed API to decode the gamma block for all three channels
# @param[in]    gamma_data, list
# @param[in]    lut_size, int
# @return       GammaDataInfo
def __decode_gamma_data_block(gamma_data: list, lut_size: int) -> list:
    programmed_gamma_lut = []
    for index in range(0, lut_size, 2):
        ##
        # Decoding for Blue Channel
        lsb_for_blue = common_utility.get_bit_value(gamma_data[index], 4, 9)
        msb_for_blue = common_utility.get_bit_value(gamma_data[index + 1], 0, 9)
        blue_value = (msb_for_blue << 6) | lsb_for_blue
        programmed_gamma_lut.append(blue_value)

        ##
        # Decoding for Green Channel
        lsb_for_green = common_utility.get_bit_value(gamma_data[index], 14, 19)
        msb_for_green = common_utility.get_bit_value(gamma_data[index + 1], 10, 19)
        green_value = (msb_for_green << 6) | lsb_for_green
        programmed_gamma_lut.append(green_value)

        ##
        # Decoding for Red Channel
        lsb_for_red = common_utility.get_bit_value(gamma_data[index], 24, 29)
        msb_for_red = common_utility.get_bit_value(gamma_data[index + 1], 20, 29)
        red_value = (msb_for_red << 6) | lsb_for_red
        programmed_gamma_lut.append(red_value)

    return programmed_gamma_lut


def __prepare_ref_lut_interpolation_and_conversion_to_16_bit(blue_channel, green_channel, red_channel, base_val,
                                                             reference_pipe_gamma_lut):
    combined_val_b = combine_luts(blue_channel, 4096, base_val)
    combined_val_g = combine_luts(green_channel, 4096, base_val)
    combined_val_r = combine_luts(red_channel, 4096, base_val)

    convert_to_16_bit_b = min(round(65535.0 * combined_val_b), 65535)
    convert_to_16_bit_g = min(round(65535.0 * combined_val_g), 65535)
    convert_to_16_bit_r = min(round(65535.0 * combined_val_r), 65535)

    reference_pipe_gamma_lut.append(convert_to_16_bit_b)
    reference_pipe_gamma_lut.append(convert_to_16_bit_g)
    reference_pipe_gamma_lut.append(convert_to_16_bit_r)

    return reference_pipe_gamma_lut


##
# @brief       Exposed API to multiply the Pixel Boost values with the Input Values and apply OETF 2084 on the Lut
# @param[in]   lut_input_val - Static Input_Lut values created
# @param[in]   pixel_boost - In case of eDP, pixel_boost value to be considered.
#                             For external panels, pixel_boost = 1.0
# @param[in]  os_relative_lut - Relative LUT given by OS
# @param[in]  num_of_samples -  No. of samples in relative LUT given by OS
# @return     reference_pipe_gamma_lut -
def generate_reference_pipe_gamma_lut_with_pixel_boost(base_lut: list, pixel_boost: float,
                                                       os_relative_lut: list) -> list:
    reference_pipe_gamma_lut = []
    blue_channel = []
    green_channel = []
    red_channel = []
    ##
    # Creating three separate LUTs for three channels from the OS relative LUT
    for index in range(0, len(os_relative_lut), 3):
        red_channel.append(os_relative_lut[index])
        green_channel.append(os_relative_lut[index + 1])
        blue_channel.append(os_relative_lut[index + 2])

    for index in range(0, len(base_lut)):
        pixel_boosted_val = (base_lut[index] * pixel_boost) / 16777216
        base_val = oetf_2084(pixel_boosted_val)
        if base_val > 1.0:
            base_val = 1.0

        reference_pipe_gamma_lut = __prepare_ref_lut_interpolation_and_conversion_to_16_bit(blue_channel, green_channel,
                                                                                            red_channel, base_val,
                                                                                            reference_pipe_gamma_lut)

    return reference_pipe_gamma_lut


def prepare_full_reference_gamma_lut(os_relative_lut, lut_size, gamma_curve_type):
    reference_pipe_gamma_lut = []
    blue_channel = []
    green_channel = []
    red_channel = []

    for index in range(0, len(os_relative_lut), 3):
        red_channel.append(os_relative_lut[index])
        green_channel.append(os_relative_lut[index + 1])
        blue_channel.append(os_relative_lut[index + 2])

    for index in range(0, lut_size):
        input_val = index / lut_size
        if input_val > 1.0:
            input_val = 1.0
        if gamma_curve_type == "SRGB_GAMMA_CURVE":
            input_val = get_srgb_encoding(input_val)
        if gamma_curve_type == "SRGB_DEGAMMA_CURVE":
            input_val = get_srgb_decoding(input_val)
        if gamma_curve_type == "UNITY_LUT":
            input_val = input_val

        reference_pipe_gamma_lut = __prepare_ref_lut_interpolation_and_conversion_to_16_bit(blue_channel, green_channel,
                                                                                            red_channel, input_val,
                                                                                            reference_pipe_gamma_lut)

    return reference_pipe_gamma_lut


def prepare_reference_gamma_lut_for_correction_lut_in_sdr_mode(igcl_lut, os_relative_lut, lut_size):
    reference_pipe_gamma_lut = []
    blue_channel = []
    green_channel = []
    red_channel = []
    for index in range(0, len(os_relative_lut), 3):
        red_channel.append(os_relative_lut[index])
        green_channel.append(os_relative_lut[index + 1])
        blue_channel.append(os_relative_lut[index + 2])

    for index in range(0, lut_size):
        input_val = index / lut_size
        if input_val > 1.0:
            input_val = 1.0
        input_val = get_srgb_encoding(input_val)

        correction_lut_combined_with_srgb_gamma = combine_luts(igcl_lut, 2048, input_val)
        if correction_lut_combined_with_srgb_gamma > 1.0:
            correction_lut_combined_with_srgb_gamma = 1.0

        reference_pipe_gamma_lut = __prepare_ref_lut_interpolation_and_conversion_to_16_bit(blue_channel, green_channel,
                                                                                            red_channel,
                                                                                            correction_lut_combined_with_srgb_gamma,
                                                                                            reference_pipe_gamma_lut)

    return reference_pipe_gamma_lut


def prepare_reference_gamma_lut_for_decrement_curve(os_relative_lut, lut_size):
    logging.info("DECREMENT_CURVE GAMMA Block")
    reference_pipe_gamma_lut = []
    blue_channel = []
    green_channel = []
    red_channel = []
    for index in range(0, len(os_relative_lut), 3):
        red_channel.append(os_relative_lut[index])
        green_channel.append(os_relative_lut[index + 1])
        blue_channel.append(os_relative_lut[index + 2])

    for index in range(lut_size, -1, -1):
        input_val = index / (lut_size - 1)
        if input_val > 1.0:
            input_val = 1.0
        input_val = get_srgb_decoding(input_val)
        reference_pipe_gamma_lut = __prepare_ref_lut_interpolation_and_conversion_to_16_bit(blue_channel, green_channel,
                                                                                            red_channel,
                                                                                            input_val,
                                                                                            reference_pipe_gamma_lut)

    return reference_pipe_gamma_lut


def prepare_reference_correction_gamma_lut_with_hdr_mode(base_lut, igcl_lut, os_relative_lut, pixel_boost):
    logging.info("PixelBoost is {0}".format(pixel_boost))
    reference_pipe_gamma_lut = []
    blue_channel = []
    green_channel = []
    red_channel = []
    ##
    # Creating three separate LUTs for three channels from the OS relative LUT
    for index in range(0, len(os_relative_lut), 3):
        red_channel.append(os_relative_lut[index])
        green_channel.append(os_relative_lut[index + 1])
        blue_channel.append(os_relative_lut[index + 2])

    for index in range(0, len(base_lut)):
        pixel_boosted_val = (base_lut[index] * pixel_boost) / 16777216
        base_val = oetf_2084(pixel_boosted_val)
        if base_val > 1.0:
            base_val = 1.0

        if igcl_lut is None:
            igcl_combined_with_pixel_boost = base_val
        else:
            igcl_combined_with_pixel_boost = combine_luts(igcl_lut, 2048, base_val)

        reference_pipe_gamma_lut = __prepare_ref_lut_interpolation_and_conversion_to_16_bit(blue_channel, green_channel,
                                                                                            red_channel,
                                                                                            igcl_combined_with_pixel_boost,
                                                                                            reference_pipe_gamma_lut)

    return reference_pipe_gamma_lut


def prepare_full_ref_gamma_lut_in_sdr_mode(os_relative_lut, lut_size, gamma_curve_type="SRGB_GAMMA_CURVE"):
    reference_pipe_gamma_lut = prepare_full_reference_gamma_lut(os_relative_lut, lut_size, gamma_curve_type)

    return reference_pipe_gamma_lut


def prepare_correction_ref_gamma_lut_in_sdr_mode(correction_lut, os_relative_lut, lut_size):
    reference_pipe_gamma_lut = prepare_reference_gamma_lut_for_correction_lut_in_sdr_mode(correction_lut,
                                                                                          os_relative_lut, lut_size)

    return reference_pipe_gamma_lut


def prepare_correction_ref_gamma_lut_in_hdr_mode(base_lut, correction_lut, os_relative_lut, pixel_boost):
    reference_pipe_gamma_lut = prepare_reference_correction_gamma_lut_with_hdr_mode(base_lut, correction_lut,
                                                                                    os_relative_lut,
                                                                                    pixel_boost)
    return reference_pipe_gamma_lut


##
# @brief        Exposed API to Compare the reference and programmed data
#               If the difference is greater than 0, then the error percentage is calculated
#               An error percentage of
#               0.005 is acceptable due to 16bit precision.
# @param[in]    ref_pipe_gamma_lut, list
# @param[in]    programmed_gamma_lut, list
# @return       result, bool
def compare_ref_and_programmed_gamma_log_lut(ref_pipe_gamma_lut: list, programmed_gamma_lut: list) -> bool:
    result = False
    if len(ref_pipe_gamma_lut) != len(programmed_gamma_lut):
        logging.debug(
            "FAIL : Reference LUT size {0} is not matching Programmed LUT size {1}".format(len(ref_pipe_gamma_lut),
                                                                                           len(programmed_gamma_lut)))

    reference_brightness_in_nits = convert_encoded_code_word_to_brightness(ref_pipe_gamma_lut, 65536)
    programmed_brightness_in_nits = convert_encoded_code_word_to_brightness(programmed_gamma_lut, 65536)
    for index in range(3, len(programmed_gamma_lut)):
        diff_value = abs(ref_pipe_gamma_lut[index] - programmed_gamma_lut[index])
        if diff_value > 0:
            error_in_code_word = (diff_value / ref_pipe_gamma_lut[index])
            if error_in_code_word > 0.005:
                ##
                # The Lowest Value that is specified in the VESA HDR True black certification is 0.5 mNits.
                # For Higher Levels the % delta is less than 1%
                diff_in_nits = abs(reference_brightness_in_nits[index] - programmed_brightness_in_nits[index])
                error_in_nits = (diff_in_nits / reference_brightness_in_nits[index])
                if abs(reference_brightness_in_nits[index] - programmed_brightness_in_nits[
                    index]) < 0.005 or error_in_nits < 0.01:
                    logging.debug("At Index {0} : Absolute Delta in Nits is {1}; Error Percentage is {2}".format(index,
                                                                                                                 abs(
                                                                                                                     reference_brightness_in_nits[
                                                                                                                         index] -
                                                                                                                     programmed_brightness_in_nits[
                                                                                                                         index]),
                                                                                                                 error_in_nits))
                else:
                    logging.debug(
                        "At Index {0} : Error Percentage is {1} ;Absolute Delta in Nits is {2}".format(index,
                                                                                                       error_in_nits,
                                                                                                       abs(
                                                                                                           reference_brightness_in_nits[
                                                                                                               index] -
                                                                                                           programmed_brightness_in_nits[
                                                                                                               index])))
                    return False
            else:
                logging.debug(
                    "Error Percentage is {0} @ Index: {1}; Expected : {2}; Programmed :{3}".format(error_in_code_word,
                                                                                                   index,
                                                                                                   ref_pipe_gamma_lut[
                                                                                                       index],
                                                                                                   programmed_gamma_lut[
                                                                                                       index]))
    return True


def compare_ref_and_programmed_gamma_lut(ref_pipe_gamma_lut: list, programmed_gamma_lut: list) -> bool:
    result = False
    if len(ref_pipe_gamma_lut) != len(programmed_gamma_lut):
        logging.error(
            "FAIL : Reference LUT size {0} is not matching Programmed LUT size {1}".format(len(ref_pipe_gamma_lut),
                                                                                           len(programmed_gamma_lut)))
        return result

    for index in range(1, len(programmed_gamma_lut)):
        diff_value = abs(ref_pipe_gamma_lut[index] - programmed_gamma_lut[index])
        if diff_value > 0:
            ref_pipe_lut = ref_pipe_gamma_lut[index]
            error_percentage = 100
            if ref_pipe_lut != 0:
                error_percentage = (diff_value / ref_pipe_lut ) / 100
            if error_percentage > 0.005:
                logging.error(
                    "Error Percentage is {0} @ Index: {1}; Expected : {2}; Programmed :{3}".format(error_percentage,
                                                                                                   index,
                                                                                                   ref_pipe_gamma_lut[
                                                                                                       index],
                                                                                                   programmed_gamma_lut[
                                                                                                       index]))
                #return False
            else:
                logging.debug(
                    "Error Percentage is {0} @ Index: {1}; Expected : {2}; Programmed :{3}".format(error_percentage,
                                                                                                   index,
                                                                                                   ref_pipe_gamma_lut[
                                                                                                       index],
                                                                                                   programmed_gamma_lut[
                                                                                                       index]))
    return True


##################################################################################################################
########################## Plane Gamma MMIO Utilities Common between Legacy and Gen13+ ###########################
##################################################################################################################
##
# @brief        Exposed API to fetch plane degamma lut from registers
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    plane, str
# @param[in]    current_pipe, str
# @param[in]    lut_size, int
# @return       lut_data, list
def get_plane_degamma_lut_from_register(gfx_index: str, reg_interface, plane: str, current_pipe: str,
                                        lut_size: int) -> list:
    lut_data = reg_interface.get_plane_degamma_data_info(plane, current_pipe, lut_size).LutData
    return lut_data


##
# @brief        Exposed API to fetch plane gamma lut from registers
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    plane, str
# @param[in]    current_pipe, str
# @param[in]    lut_size, int
# @return       lut_data, list
def get_plane_gamma_lut_from_register(reg_interface, plane: str, current_pipe: str,
                                      lut_size: int) -> list:
    lut_data = reg_interface.get_plane_gamma_data_info(plane, current_pipe, lut_size).LutData
    return lut_data


##
# @brief        Exposed API to combine the all the segments of gamma fetched from the ETL to create the full lut
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    gamma_lut, list
# @param[in]    is_ext_registers_available, bool
# @return       lut_data, list
def __combine_gamma_segments_from_etl(reg_interface, current_pipe: str, gamma_lut: list,
                                      is_ext_registers_available: bool = False) -> list:
    ext_gamma_lut = []
    if is_ext_registers_available:
        ext_gamma_lut = reg_interface.get_pipe_gamma_ext_reg_info(current_pipe)
        logging.debug(ext_gamma_lut)
    gamma_lut = gamma_lut + ext_gamma_lut.LutData
    return gamma_lut


##################################################################################################################
############################## All Gamma MMIO/ETL Utilities for Legacy (Gen11 to Gen12) ##########################
##################################################################################################################
##
# @brief        Exposed API to fetch pipe degamma lut from registers
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    lut_size, int
# @return       lut_data, list
def get_pipe_degamma_lut_from_register_legacy(reg_interface, current_pipe: str, lut_size: int) -> list:
    lut_data = reg_interface.get_pipe_degamma_data_info(current_pipe, lut_size).LutData
    return lut_data


##
# @brief        Exposed API to fetch pipe gamma lut from registers
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    lut_size, int
# @return       lut_data, list
def get_pipe_gamma_lut_from_register_legacy(gfx_index: str, reg_interface, is_hdr_enabled: bool, current_pipe: str,
                                            lut_size: int) -> list:
    mutli_segment_lut = []
    # On Post-Si, read operation on the HW Gamma Data register is broken.
    # A WA suggested by HW team was set the Gamma Mode register to 0 before reading the GammaData register
    # and restore the Gamma Mode register once the read operation is completed.
    gamma_mode_offset = reg_interface.get_color_ctrl_offsets(current_pipe).GammaMode
    ##
    # Caching the Gamma Mode register value before setting to 0
    gamma_mode_reg_value_before_resetting = color_mmio_interface.ColorMmioInterface().read(gfx_index, gamma_mode_offset)
    logging.debug("Before Resetting {0}".format(gamma_mode_reg_value_before_resetting))

    ##
    # Setting the Gamma Mode register to 0
    if color_mmio_interface.ColorMmioInterface().write(gfx_index, gamma_mode_offset, 0):
        logging.debug("Successfully set GammaMode register to 0")
    else:
        logging.error("Failed set GammaMode register to 0")
        return []

    if is_hdr_enabled:
        mutli_segment_lut = reg_interface.get_pipe_gamma_multi_segment_info(current_pipe, 18).LutData

    pal_prec_data = reg_interface.get_pipe_pal_prec_data_info(current_pipe, lut_size).LutData
    ext_gamma_lut = reg_interface.get_pipe_gamma_ext_reg_info(current_pipe)
    gamma_lut = mutli_segment_lut + pal_prec_data + ext_gamma_lut.LutData

    ##
    # Restore GammaMode register
    if color_mmio_interface.ColorMmioInterface().write(gfx_index, gamma_mode_offset,
                                                       gamma_mode_reg_value_before_resetting):
        logging.debug("Successfully restored GammaMode register")
    else:
        logging.error("Failed to restore GammaMode register")
        return []
    return gamma_lut


##
# @brief        Exposed API to dump all the gamma mmio data based on SDR/HDR Mode
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    hdr_mode, bool
# @param[in]    lut_size, int
# @return       lut_data, list
# @todo : Currently the function can return Gamma LUT for SDR mode and after SDR-HDR modeset
#         To handle the HDR-SDR transition, the timestamp to track transition is required and needs to be explored
def get_all_gamma_mmio_dump_from_etl_legacy(reg_interface, current_pipe: str, hdr_mode: bool,
                                            lut_size: int) -> list:
    multi_segment_data, pipe_gamma_lut, programmed_gamma_data, temp_data = [], [], [], []
    if hdr_mode:
        multi_seg_data_offset = reg_interface.get_pipe_gamma_offsets(current_pipe).PalPrecMultiSegmentData
        mmio_output_multi_seg_data = etl_parser.get_mmio_data(multi_seg_data_offset)
        for index in range(0, len(mmio_output_multi_seg_data)):
            temp_data.append(mmio_output_multi_seg_data[index].Data)
        ##
        # Partitioning the whole dump of multi-segment gamma into list of lut-size 18 each
        multi_segment_data = [temp_data[i * const.MULTI_SEGMENT_LUT_SIZE:(i + 1) * const.MULTI_SEGMENT_LUT_SIZE] for i
                              in range(
                (len(temp_data) + const.MULTI_SEGMENT_LUT_SIZE - 1) // const.MULTI_SEGMENT_LUT_SIZE)]
        multi_segment_data.reverse()

    temp_data.clear()  # Flushing out the data if any
    pal_prec_data_offset = reg_interface.get_pipe_gamma_offsets(current_pipe).PalPrecData
    mmio_output_pal_data = etl_parser.get_mmio_data(pal_prec_data_offset)
    for index in range(0, len(mmio_output_pal_data)):
        temp_data.append(mmio_output_pal_data[index].Data)
    pal_prec_data = [temp_data[i * lut_size:(i + 1) * lut_size] for i in
                     range((len(temp_data) + lut_size - 1) // lut_size)]

    # SDR - Pipe gamma lut values will be captured in the PAL_PREC_DATA in the ETL dump
    # HDR -  When SDR to HDR modeset transition is performed, both Multi-Segment and PAL_PREC_DATA
    # will be programmed. To differentiate between the SDR and HDR Luts, performing a reverse operation and
    # fetching PAL_PREC_DATA event same as the length of Multi segment events for HDR mode
    # Finally Performing a reverse operation again  at the end to get the Gamma LUTs in the proper order
    if hdr_mode:
        pal_prec_data.reverse()
        for index in range(0, len(multi_segment_data)):
            pipe_gamma_lut.append(multi_segment_data[index] + pal_prec_data[index])
        pipe_gamma_lut.reverse()

    for index in range(0, len(pipe_gamma_lut)):
        temp_data = __decode_gamma_data_block(pipe_gamma_lut[index], len(pipe_gamma_lut[index]))
        programmed_gamma_data.append(temp_data)

    return programmed_gamma_data


##
# @brief        Exposed API to dump the final gamma mmio data based on SDR/HDR Mode
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    hdr_mode, bool
# @param[in]    lut_size, int
# @return       lut_data, list
def fetch_pipe_gamma_mmio_data_from_etl_legacy(reg_interface, current_pipe: str, hdr_mode: bool,
                                               lut_size: int) -> list:
    lut = get_all_gamma_mmio_dump_from_etl_legacy(reg_interface, current_pipe, hdr_mode, lut_size)
    final_lut = lut[-1]
    return final_lut


##
# @brief        Exposed API to dump gamma mmio data for a specific step index for Smooth Brightness
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    step_index, int
# @param[in]    lut_size, int
# @return       lut_data, list
def fetch_pipe_gamma_mmio_data_from_etl_for_smooth_brightness_legacy(reg_interface, current_pipe: str,
                                                                     step_index: int, hdr_mode: bool,
                                                                     lut_size: int) -> list:
    lut = get_all_gamma_mmio_dump_from_etl_legacy(reg_interface, current_pipe, hdr_mode, lut_size)
    final_lut = lut[step_index]
    return final_lut


##
# @brief        Exposed API to get the entired programmed gamma lut. This API is to be utilized by the tests directly
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    step_index, int
# @param[in]    lut_size, int
# @return       lut_data, list
def get_programmed_mmio_pipe_gamma_data_from_etl_legacy(reg_interface, current_pipe: str,
                                                        is_hdr_supported: bool, lut_size: int,
                                                        is_smooth_brightness: bool = False,
                                                        step_index: int = 0) -> list:
    if is_smooth_brightness:
        programmed_gamma_data = fetch_pipe_gamma_mmio_data_from_etl_for_smooth_brightness_legacy(reg_interface,
                                                                                                 current_pipe,
                                                                                                 step_index,
                                                                                                 is_hdr_supported,
                                                                                                 lut_size)
    else:
        programmed_gamma_data = fetch_pipe_gamma_mmio_data_from_etl_legacy(reg_interface, current_pipe,
                                                                           is_hdr_supported,
                                                                           lut_size)
    gamma_data = __combine_gamma_segments_from_etl(reg_interface, current_pipe, programmed_gamma_data,
                                                   is_ext_registers_available=True)
    return gamma_data


##
# @brief        Exposed API to decode the Gamma values from the ETL from DSB
#               The Gamma dump will be of the form (value, offset) pair.
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    dsb_gamma_lut, list
# @param[in]    hdr_mode, bool
# @return       lut_data, list
def get_all_dsb_pipe_gamma_lut_from_etl_legacy(reg_interface, current_pipe: str, dsb_gamma_dump,
                                               hdr_mode: bool) -> list:
    multi_seg_data_offset, pal_prec_data_offset = None, None
    multi_seg_cntr = 0
    programmed_multi_seg_gamma, programmed_gamma_lut = [], []
    ##
    # Verify if the DSB Gamma Dump is available in the ETL
    if dsb_gamma_dump.__len__() == 0:
        logging.error("There is no DSB Gamma Dump for {0}".format(current_pipe))
        return dsb_gamma_dump
    if hdr_mode:
        multi_seg_data_offset = reg_interface.get_pipe_gamma_offsets(current_pipe).PalPrecMultiSegmentData

    logging.info("Length of the Gamma DSb Dump is {0}".format(dsb_gamma_dump.__len__()))

    pal_prec_data_offset = reg_interface.get_pipe_gamma_offsets(current_pipe).PalPrecData
    for each_dsb_event in dsb_gamma_dump:
        temp_data = []
        for index1 in range(0, len(each_dsb_event), 4):
            ##
            # In the ETL Parser, the byte array is converted as an Int array,
            # where each byte is stored within 4 4 byte value.
            # Only the 1st byte will have meaningful data,
            # hence extracting the LSB Byte and concatinating it to form a 32bit value
            val1 = each_dsb_event[index1] & 0xFF
            val2 = each_dsb_event[index1 + 1] & 0xFF
            val3 = each_dsb_event[index1 + 2] & 0xFF
            val4 = each_dsb_event[index1 + 3] & 0xFF

            value = val4 << 24 | val3 << 16 | val2 << 8 | val1
            temp_data.append(value)

        ##
        # First two bytes dont have any Gamma data, hence ignoring it.
        multi_seg_data, pal_prec_data = [], []
        for index in range(3, len(temp_data)):
            val = common_utility.get_bit_value(temp_data[index], 0, 19)
            if hdr_mode:
                if val == multi_seg_data_offset:
                    multi_seg_data.append(temp_data[index - 1])
                    multi_seg_cntr += 1
            if val == pal_prec_data_offset:
                pal_prec_data.append(temp_data[index - 1])

            index += 1
        if hdr_mode:
            if multi_seg_data.__len__() == 0:
                logging.debug("No Mutlisegment Gamma Info available in the ETLs for Pipe {0}".format(current_pipe))
            else:
                programmed_multi_seg_gamma = __decode_gamma_data_block(multi_seg_data, const.MULTI_SEGMENT_LUT_SIZE)

        programmed_pal_prec_gamma = __decode_gamma_data_block(pal_prec_data, const.PAL_PREC_LUT_SIZE)
        programmed_gamma_data = programmed_multi_seg_gamma + programmed_pal_prec_gamma
        decoded_gamma_lut = __combine_gamma_segments_from_etl(reg_interface, current_pipe, programmed_gamma_data,
                                                              is_ext_registers_available=True)
        programmed_gamma_lut.append(decoded_gamma_lut)
    return programmed_gamma_lut


##
# @brief        Exposed API to dump the final gamma dsb data based on SDR/HDR Mode
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    hdr_mode, bool
# @param[in]    lut_size, int
# @return       lut_data, list
def fetch_pipe_gamma_dsb_data_from_etl_legacy(reg_interface, current_pipe: str, dsb_gamma_dump,
                                              hdr_mode: bool) -> list:
    lut = get_all_dsb_pipe_gamma_lut_from_etl_legacy(reg_interface, current_pipe, dsb_gamma_dump, hdr_mode)
    if lut.__len__() == 0:
        logging.error("No DSB Gamma LUT available in the context")
        return lut
    final_lut = lut[-1]
    return final_lut


##
# @brief        Exposed API to dump gamma dsb data for a specific step index for Smooth Brightness
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    step_index, int
# @param[in]    lut_size, int
# @return       lut_data, list
def fetch_pipe_gamma_dsb_data_from_etl_for_smooth_brightness_legacy(reg_interface, current_pipe: str, dsb_gamma_dump,
                                                                    step_index, hdr_mode) -> list:
    lut = get_all_dsb_pipe_gamma_lut_from_etl_legacy(reg_interface, current_pipe, dsb_gamma_dump, hdr_mode)
    final_lut = lut[step_index]
    return final_lut


##
# @brief        Exposed API to get the entire programmed gamma lut by DSB.
#               This API is to be utilized by the tests directly for TGL
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    step_index, int
# @param[in]    lut_size, int
# @return       lut_data, list
def get_programmed_dsb_pipe_gamma_data_from_etl_legacy(reg_interface, current_pipe: str, dsb_gamma_dump,
                                                       lut_size: int, hdr_mode: bool,
                                                       is_smooth_brightness: bool = False,
                                                       step_index: int = 0) -> list:
    if is_smooth_brightness:
        gamma_data = fetch_pipe_gamma_dsb_data_from_etl_for_smooth_brightness_legacy(reg_interface, current_pipe,
                                                                                     dsb_gamma_dump, step_index,
                                                                                     lut_size)
    else:
        gamma_data = fetch_pipe_gamma_dsb_data_from_etl_legacy(reg_interface, current_pipe, dsb_gamma_dump, hdr_mode)
    return gamma_data


##################################################################################################################
################################### All Gamma MMIO/ETL Utilities Gen13+ ##########################################
##################################################################################################################
##
# @brief        Exposed API to fetch pipe degamma lut from registers
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    cc_block, str
# @param[in]    current_pipe, str
# @param[in]    lut_size, int
# @return       lut_data, list
def get_pipe_degamma_lut_from_register(reg_interface, cc_block: str, current_pipe: str,
                                       lut_size: int) -> list:
    if cc_block == "CC1":
        lut_data = reg_interface.get_pipe_degamma_data_info_for_cc1(current_pipe, lut_size).LutData
    else:
        lut_data = reg_interface.get_pipe_degamma_data_info_for_cc2("CC2_" + current_pipe, lut_size).LutData
    return lut_data


##
# @brief        Exposed API to fetch pipe gamma lut from registers
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    cc_block, str
# @param[in]    current_pipe, str
# @param[in]    lut_size, int
# @return       lut_data, list
def get_pipe_gamma_lut_from_register(gfx_index: str, reg_interface, cc_block: str, current_pipe: str,
                                     lut_size: int) -> list:
    # On Post-Si, read operation on the HW Gamma Data register is broken.
    # A WA suggested by HW team was set the Gamma Mode register to 0 before reading the GammaData register
    # and restore the Gamma Mode register once the read operation is completed.
    gamma_mode_offset = reg_interface.get_color_ctrl_offsets(current_pipe).GammaMode
    ##
    # Caching the Gamma Mode register value before setting to 0
    gamma_mode_reg_value_before_resetting = color_mmio_interface.ColorMmioInterface().read(gfx_index, gamma_mode_offset)

    ##
    # Setting the Gamma Mode register to 0
    if color_mmio_interface.ColorMmioInterface().write(gfx_index, gamma_mode_offset, 0):
        logging.debug("Successfully set GammaMode register to 0")
    else:
        logging.error("Failed set GammaMode register to 0")
        return []

    if cc_block == "CC1":
        lut_data = reg_interface.get_pipe_gamma_data_info_for_cc1(current_pipe, lut_size).LutData
        ext_registers = reg_interface.get_pipe_gamma_ext_reg_info(current_pipe)
        lut_data += ext_registers.LutData

    else:
        lut_data = reg_interface.get_pipe_gamma_data_info_for_cc2("CC2_" + current_pipe, lut_size).LutData
        ext_registers = reg_interface.get_pipe_gamma_ext_reg_cc2_info("CC2_" + current_pipe).LutData
        ##
        # Consider only values until 1.0 and discard 3.0 and 7.0 values of all three channels
        ext_registers_1_0 = ext_registers[0:3]
        lut_data += ext_registers_1_0

    ##
    # Restore GammaMode register
    if color_mmio_interface.ColorMmioInterface().write(gfx_index, gamma_mode_offset,
                                                       gamma_mode_reg_value_before_resetting):
        logging.debug("Successfully restored GammaMode register")
    else:
        logging.error("Failed to restore GammaMode register")
        return []

    return lut_data


##
# @brief        Exposed API to all the gamma mmio dump from the ETLs
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    cc_block, str
# @param[in]    current_pipe, str
# @param[in]    lut_size, int
# @return       lut_data, list
def get_all_gamma_mmio_dump_from_etl(reg_interface, current_pipe: str, cc_block: str,
                                     lut_size: int) -> list:
    programmed_gamma_data, ext_registers, mmio_data_dump, final_lut = [], [], [], []

    if cc_block == "CC1":
        ##
        # Gen13 platforms like DG2, ADLP, in HDR Mode, use Logarithmic LUT, which is of size 510 samples (PalPrec)
        pal_prec_data_offset = reg_interface.get_pipe_gamma_offsets(current_pipe).PalPrecData
        mmio_output_pal_data = etl_parser.get_mmio_data(pal_prec_data_offset)
        for index in range(0, len(mmio_output_pal_data)):
            mmio_data_dump.append(mmio_output_pal_data[index].Data)

        ##
        # Reversing to get the HDR related data in the beginning to perform a proper division into chunks of data
        # The ETL contains both SDR and HDR MMIO Data hence reversal is required
        mmio_data_dump.reverse()

        ##
        # Dividing into chunks of [510*3] samples -
        new_data_lut_after_reversal = [mmio_data_dump[i * lut_size:(i + 1) * lut_size] for i in
                                       range((len(mmio_data_dump) + lut_size - 1) // lut_size)]

        for each_lut in new_data_lut_after_reversal:
            ##
            # After dividing into chunks, the list again has to be reversed to get the data in the increasing order
            each_lut.reverse()
            final_lut.append(each_lut)

        # # In case of CC1 blocks, in both SDR and HDR Modes, extended values for 1.0, 3.0 and 7.0 also have to be
        # considered
        ext_registers = reg_interface.get_pipe_gamma_ext_reg_info(current_pipe)
        for index in range(0, len(final_lut)):
            temp_data = __decode_gamma_data_block(final_lut[index], len(final_lut[index]))
            temp_data += ext_registers.LutData
            programmed_gamma_data.append(temp_data)

    else:
        post_csc_cc2_data_offset = reg_interface.get_pipe_gamma_cc2_offsets("CC2_" + current_pipe).PostCscCC2Data
        logging.info("Offset is {0}".format(post_csc_cc2_data_offset))
        mmio_cc2_pipe_gamma_data = etl_parser.get_mmio_data(post_csc_cc2_data_offset)

        for index in range(0, len(mmio_cc2_pipe_gamma_data)):
            mmio_data_dump.append(mmio_cc2_pipe_gamma_data[index].Data)

        ##
        # Reversing to get the HDR related data in the beginning to perform a proper division into chunks of data
        # The ETL contains both SDR and HDR MMIO Data hence reversal is required
        mmio_data_dump.reverse()

        cc2_pipe_gamma_dump = [mmio_data_dump[i * lut_size:(i + 1) * lut_size] for i in
                               range((len(mmio_data_dump) + lut_size - 1) // lut_size)]

        for each_lut in cc2_pipe_gamma_dump:
            ##
            # After dividing into chunks, the list again has to be reversed to get the data in the increasing order
            each_lut.reverse()
            final_lut.append(each_lut)

        ##
        # In case of CC2 blocks, in both SDR and HDR Modes, extended values for 1.0 only has to be considered
        # 3.0 and 7.0 values has to be discarded
        ext_registers = reg_interface.get_pipe_gamma_ext_reg_cc2_info("CC2_" + current_pipe).LutData

        ext_registers_1_0 = ext_registers[0:3]
        for index in range(0, len(final_lut)):
            temp_data = __decode_gamma_data_block(final_lut[index], len(final_lut[index]))
            temp_data += ext_registers_1_0
            programmed_gamma_data.append(temp_data)

    return programmed_gamma_data


##
# @brief        Exposed API to dump the final gamma mmio data based on SDR/HDR Mode
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    hdr_mode, bool
# @param[in]    lut_size, int
# @return       lut_data, list
def fetch_pipe_gamma_mmio_data_from_etl(reg_interface, current_pipe: str, cc_block: str,
                                        lut_size: int) -> list:
    lut = get_all_gamma_mmio_dump_from_etl(reg_interface, current_pipe, cc_block, lut_size)
    final_lut = lut[0]
    return final_lut


##
# @brief        Exposed API to dump gamma mmio data for a specific step index for Smooth Brightness
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    step_index, int
# @param[in]    lut_size, int
# @return       lut_data, list
def fetch_pipe_gamma_mmio_data_from_etl_for_smooth_brightness(reg_interface, current_pipe: str,
                                                              cc_block: str, step_index, lut_size) -> list:
    lut = get_all_gamma_mmio_dump_from_etl(reg_interface, current_pipe, cc_block, lut_size)
    final_lut = lut[step_index]
    return final_lut


##
# @brief        Exposed API to get the entired programmed gamma lut. This API is to be utilized by the tests directly
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    step_index, int
# @param[in]    lut_size, int
# @return       lut_data, list
def get_programmed_mmio_pipe_gamma_data_from_etl(reg_interface, current_pipe: str, cc_block: str,
                                                 lut_size: int, is_smooth_brightness: bool = False,
                                                 step_index: int = 0) -> list:
    if is_smooth_brightness:
        gamma_data = fetch_pipe_gamma_mmio_data_from_etl_for_smooth_brightness(reg_interface, current_pipe,
                                                                               cc_block, step_index, lut_size)
    else:
        gamma_data = fetch_pipe_gamma_mmio_data_from_etl(reg_interface, current_pipe, cc_block, lut_size)
    return gamma_data


##
# @brief        Exposed API to fetch and decode all the DSB Gamma values from the ETL
#               The Gamma dump will be of the form (value, offset) pair.
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    dsb_gamma_lut, list
# @param[in]    hdr_mode, bool
# @return       lut_data, list
def get_all_dsb_pipe_gamma_lut_from_etl(reg_interface, current_pipe: str, cc_block: str, dsb_gamma_dump,
                                        lut_size: int) -> list:
    pal_prec_multi_seg_data_offset, pal_prec_data_offset, post_csc_cc2_data_offset = None, None, None
    programmed_gamma_lut, decoded_gamma_lut = [], []

    ##
    # Verify if the DSB Gamma Dump is available in the ETL
    if dsb_gamma_dump.__len__() == 0:
        logging.error("There is no DSB Gamma Dump for {0}".format(current_pipe))
        return dsb_gamma_dump

    ##
    # Verify if the DSB Gamma Dump is available in the ETL
    if cc_block == "CC1":
        pal_prec_data_offset = reg_interface.get_pipe_gamma_offsets(current_pipe).PalPrecData
    else:
        post_csc_cc2_data_offset = reg_interface.get_pipe_gamma_cc2_offsets("CC2_" + current_pipe).PostCscCC2Data

    final_lut = []
    for each_dsb_event in dsb_gamma_dump:
        pal_prec_data, gamma_cc2_data, temp_data = [], [], []
        gamma_count = 0
        for index in range(0, len(each_dsb_event), 4):
            ##
            # In the ETL Parser, the byte array is converted as an Int array,
            # where each byte is stored within 4 bytes.
            # Only the 1st byte will have meaningful data,
            # hence extracting the LSB Byte and concatinating it to form a 32bit value
            val1 = each_dsb_event[index] & 0xFF
            val2 = each_dsb_event[index + 1] & 0xFF
            val3 = each_dsb_event[index + 2] & 0xFF
            val4 = each_dsb_event[index + 3] & 0xFF

            value = val4 << 24 | val3 << 16 | val2 << 8 | val1
            temp_data.append(value)
        ##
        # First two bytes dont have any Gamma data, hence ignoring it.
        for index in range(3, len(temp_data)):
            val = common_utility.get_bit_value(temp_data[index], 0, 19)
            # (4A50C:offset, values:353,453,234.....)
            if cc_block == "CC1":
                if val == pal_prec_data_offset:
                    pal_prec_data.append(temp_data[index: - 1])
                    break
            else:
                if val == post_csc_cc2_data_offset:
                    gamma_cc2_data.append(temp_data[index: -1])
                    break

            index += 1

        else:
            if cc_block == "CC1":
                if pal_prec_data.__len__() == 0:
                    gamma_count += 1
                else:
                    programmed_pal_prec_gamma = __decode_gamma_data_block(pal_prec_data, lut_size)
                    decoded_gamma_lut = __combine_gamma_segments_from_etl(reg_interface, current_pipe,
                                                                          programmed_pal_prec_gamma,
                                                                          is_ext_registers_available=True)
            else:
                if gamma_cc2_data.__len__() == 0:
                    gamma_count += 1
                else:
                    decoded_gamma_lut = __decode_gamma_data_block(gamma_cc2_data, lut_size)

            programmed_gamma_lut.append(decoded_gamma_lut)
        if gamma_count > len(dsb_gamma_dump):
            return []

        final_lut.append(programmed_gamma_lut)
    return programmed_gamma_lut


##
# @brief        Exposed API to dump the final gamma dsb data based on SDR/HDR Mode
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    hdr_mode, bool
# @param[in]    lut_size, int
# @return       lut_data, list
def fetch_pipe_gamma_dsb_data_from_etl(reg_interface, current_pipe: str, cc_block: str, dsb_gamma_dump,
                                       lut_size: int) -> list:
    final_lut = []
    try:
        lut = get_all_dsb_pipe_gamma_lut_from_etl(reg_interface, current_pipe, cc_block, dsb_gamma_dump, lut_size)
        if lut.__len__() == 0:
            logging.error("No DSB Gamma LUT available in the context")
            return lut
        final_lut = lut[-1]
        return final_lut
    except Exception as e:
        logging.error(f"Exception occurred. {e}")
        return final_lut


##
# @brief        Exposed API to dump gamma dsb data for a specific step index for Smooth Brightness
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    step_index, int
# @param[in]    lut_size, int
# @return       lut_data, list
def fetch_pipe_gamma_dsb_data_from_etl_for_smooth_brightness(reg_interface, current_pipe: str,
                                                             cc_block: str, dsb_gamma_dump, step_index,
                                                             lut_size) -> list:
    final_lut = []
    try:
        lut = get_all_dsb_pipe_gamma_lut_from_etl(reg_interface, current_pipe, cc_block, dsb_gamma_dump, lut_size)
        step_index = 11 - step_index
        final_lut = lut[step_index]
        return final_lut
    except Exception as e:
        logging.error(f"Exception occurred {e}")
        return final_lut

##
# @brief        Exposed API to get the entire programmed gamma lut by DSB.
#               This API is to be utilized by the tests directly
# @param[in]    gfx_index, str
# @param[in]    platform, str
# @param[in]    current_pipe, str
# @param[in]    step_index, int
# @param[in]    lut_size, int
# @return       lut_data, list
def get_programmed_dsb_pipe_gamma_data_from_etl(reg_interface, current_pipe: str, cc_block: str, dsb_gamma_dump,
                                                lut_size: int, is_smooth_brightness: bool = False,
                                                step_index: int = 0) -> list:
    if is_smooth_brightness:

        gamma_data = fetch_pipe_gamma_dsb_data_from_etl_for_smooth_brightness(reg_interface, current_pipe,
                                                                              cc_block, dsb_gamma_dump, step_index,
                                                                              lut_size)
    else:
        gamma_data = fetch_pipe_gamma_dsb_data_from_etl(reg_interface, current_pipe, cc_block, dsb_gamma_dump, lut_size)
    return gamma_data


##
# @brief        Exposed API to get the entire programmed gamma lut by DSB.
#               This API is to be utilized by the tests directly
# @param[in]    reg_interface
# @param[in]    plane, str
# @param[in]    current_pipe, str
# @param[in]    lut_size, int
# @return       plane_gamma_lut, list
def get_plane_degamma_lut_from_reg(reg_interface, plane: str, current_pipe: str, lut_size: int) -> list:
    plane_gamma_lut = reg_interface.get_plane_degamma_data_info(plane, current_pipe, lut_size).LutData
    plane_gamma_lut.sort()
    return plane_gamma_lut


##
# @brief        Exposed API to get the entire programmed gamma lut by DSB.
#               This API is to be utilized by the tests directly
# @param[in]    reg_interface
# @param[in]    plane, str
# @param[in]    current_pipe, str
# @param[in]    lut_size, int
# @return       plane_gamma_lut, list
def get_plane_gamma_lut_from_reg(reg_interface, plane: str, current_pipe: str, lut_size: int) -> list:
    plane_gamma_lut = reg_interface.get_plane_degamma_data_info(plane, current_pipe, lut_size).LutData
    plane_gamma_lut.sort()
    return plane_gamma_lut
