#####################################################################################
# @file     dpcd_container.py
# @brief    Python helper script to encode DPCD data from file to registry
# @author   Beeresh Gopal
######################################################################################

import logging
import os
import re
import struct


##
# @brief        DPCD Mask class
class DPCDMask(object):
    offset = 0
    mask = 0

    ##
    # @brief        Overridden str method
    # @return       str - string representation of DPCD mask class
    def __str__(self):
        return "x%s:x%s" % (format(self.offset, 'x'), format(self.mask, 'x'))


##
# @brief        User API to parse current DPCD file format into array of bytes
# @param[in]    input_file - DPCD file to be parsed
# @return       dpcd_array - list of DPCD data
def _parse_dpcd_txt_file(input_file):
    DPCD_pattern = re.compile('\A0[xX][0-9a-fA-F]+:')

    with open(input_file, 'r') as  dpcd_file:
        dpcd_data = dpcd_file.readlines()

    dpcd_array = []
    for line in dpcd_data:
        if DPCD_pattern.match(line) is not None:
            line.strip('\n')
            line = line.replace('\n', '')
            address, values = line.split(':')
            values.strip('\n')
            values = values.replace('.', '')
            dpcd_values = values.split(',')

            address = int(address, 0)
            for value in dpcd_values:
                obj = DPCDMask()
                obj.offset = address
                obj.mask = int(value, 0)
                address += 1
                dpcd_array.append(obj)

    # print ('\n'.join(str(obj) for obj in dpcd_array))
    return dpcd_array


##
# @brief        Python API to convert DPCD file (.txt) to (.bin) format
# @details      Note: Do not use this method within tests or feature modules. 
# @param[in]    dpcd_file - DPCD file path
# @return       dpcd_bin - Converted DPCD bin file path
def _convert_dpcd_to_bin(dpcd_file):
    # Get the list of DPCD offset and value
    dpcd_array = _parse_dpcd_txt_file(dpcd_file)

    bin_file_name = os.path.splitext(os.path.basename(dpcd_file))[0] + ".bin"
    bin_file_path = os.path.dirname(dpcd_file)
    dpcd_bin = os.path.join(bin_file_path, bin_file_name)

    # To sort the list in place.
    dpcd_array.sort(key=lambda x: x.offset)

    # Find max offset to allocate data in the file
    max_dpcd_address = dpcd_array[len(dpcd_array) - 1].offset

    # 512 bytes padding to ensure ESC call size matches in YANGRA
    max_dpcd_address += 512
    data_bytes = bytearray()

    for dpcd_offset in range(0, max_dpcd_address + 1):
        search_result = list(filter(lambda dpcd_obj: dpcd_obj.offset == dpcd_offset, dpcd_array))
        if len(search_result) > 0:
            custom_dpcd = search_result[0]
            data_bytes.append(custom_dpcd.mask)
        else:
            data_bytes.append(0)

            # convert the dpcd_data_array to binary data and write to .bin file
    s = struct.pack('B' * len(data_bytes), *data_bytes)
    f = open(dpcd_bin, 'wb')
    f.write(s)
    f.close()

    if not os.path.isfile(dpcd_bin):
        logging.error("DPCD .txt to .bin conversion failed")
        return None
    return dpcd_bin
