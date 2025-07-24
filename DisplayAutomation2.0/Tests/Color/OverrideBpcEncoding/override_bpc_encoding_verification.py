import itertools
import logging

from Libs.Core.sw_sim import driver_interface
from Tests.Color import color_common_utility
from registers.mmioregister import MMIORegister


##
# @brief get_bpc_encoding_pair() Generate combo list from bpc and encoding mask
# @param[in] - cui_override_deep_color_info_set args
# @return - cui_override_deep_color_info_set args, combo_bpc_encoding_list
def get_bpc_encoding_pair(cui_override_deep_color_info_set):
    bpc_mask = int(cui_override_deep_color_info_set.supportedBpcMask)
    encoding_mask = int(cui_override_deep_color_info_set.supportedEncodingMask)

    bpc_mask_value_dict = {"BPCDEFAULT": 0, "BPC6": 0, "BPC8": 0, "BPC10": 0, "BPC12": 0}
    encoding_mask_value_dict = {"DEFAULT": 0, "RGB": 0, "YCBCR420": 0, "YCBCR422": 0, "YCBCR444": 0}

    ##
    # Get mask value from bits
    # Based on mask ,set bit value to do set_call:
    bit_index = 0
    for bpc, bit_value in bpc_mask_value_dict.items():
        mask_value = color_common_utility.get_bit_value(bpc_mask, bit_index, bit_index)
        if mask_value == 1:
            bpc_mask_value_dict[bpc] = 1
        bit_index = bit_index + 1

    bit_index = 0
    for encoding, bit_value in encoding_mask_value_dict.items():
        mask_value = color_common_utility.get_bit_value(encoding_mask, bit_index, bit_index)
        if mask_value == 1:
            encoding_mask_value_dict[encoding] = 1
        bit_index = bit_index + 1

    bpc_mask_list = [i for i, j in bpc_mask_value_dict.items() if j == 1]
    encoding_mask_list = [i for i, j in encoding_mask_value_dict.items() if j == 1]

    combo_bpc_encoding_list = list(itertools.product(bpc_mask_list, encoding_mask_list))
    logging.info("Combo bpc_encoding pair list %s" % combo_bpc_encoding_list)
    return combo_bpc_encoding_list


##
# @brief verify_bpc_pixel_encoding_register_programming() verify registers for bpc and pixel encoding
# @param[in] - pipe
# @param[in] - platform
# @param[in] - avi_encoding_mode
# @return - applied_bpc, current_pixel_encoding
def verify_bpc_pixel_encoding_register_programming(pipe, platform, avi_encoding_mode, expected_bpc, expected_encoding):
    programmed_bpc = ""
    ##
    # Register verification for BPC and Pixel encoding
    bpc_list = [(0, "BPC8"), (1, "BPC10"), (2, "BPC6"), (3, "BPC12")]

    # get the applied bpc
    trans_ddi_func_reg = 'TRANS_DDI_FUNC_CTL_' + pipe
    trans_ddi_func_reg_ctl = MMIORegister.read('TRANS_DDI_FUNC_CTL_REGISTER', trans_ddi_func_reg,
                                               platform)
    bpc_value = trans_ddi_func_reg_ctl.__getattribute__("bits_per_color")
    for index in range(len(bpc_list)):
        bit_value = bpc_list[index][0]
        if bit_value == bpc_value:
            programmed_bpc = str(bpc_list[index][1])
    logging.info("Color Format: %s BPC" % programmed_bpc)

    # get pixel encoding
    base = MMIORegister.get_instance("VIDEO_DIP_AVI_HEADER_BYTE_REGISTER", "VIDEO_DIP_AVI_DATA_%s_0" % pipe, platform)
    offset = base.offset + 4
    reg_value = driver_interface.DriverInterface().mmio_read(offset, 'gfx_0')
    applied_encoding = color_common_utility.get_bit_value(reg_value, 13, 15)

    ##
    # Decode based on value based on enum
    programmed_encoding = avi_encoding_mode(applied_encoding).name
    logging.info("Current pixel encoding %s" % programmed_encoding)
    if expected_bpc == programmed_bpc and programmed_encoding == expected_encoding:

        logging.info("Pass: Expected BPC ={0} and Actual BPC ={1}".format(expected_bpc, programmed_bpc))
        logging.info("Pass: Expected Encoding ={0} and Actual Encoding ={1}".format(
            expected_encoding, programmed_encoding))
        return True
    else:
        logging.error("Fail: Expected BPC ={0} and Actual BPC ={1}".format(expected_bpc, programmed_bpc))
        logging.error("Fail: Expected Encoding ={0} and Actual Encoding ={1}".format(
            expected_encoding, programmed_encoding))
        return False
