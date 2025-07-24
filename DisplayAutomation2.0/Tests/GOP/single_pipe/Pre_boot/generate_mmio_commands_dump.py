########################################################################################################################
# @file         generate_mmio_commands_dump.py
# @brief        a. To change the last bit of 10h offest that we dumped to the tenh_offset.txt file to '0'. This
#                   gives the base address.
# 		        b. After getting the base address, adding each offset from the single_mmio_offsets.json to the base
# 		            address and the resulted values are stored in a list.
#               c. Using the values in the above resulted list, generate a MMIO_dump_commands_nsh.nsh file.
# @author       GOLI S V N LAKSHMI BHAVANI
########################################################################################################################

import json


##
# @brief        Change the last bit of 10h offest to '0', add each offset from the single_mmio_offsets.json
#               to the base address and generate a MMIO_dump_commands_nsh.nsh file
# @param        tenh_offset_file
# @return       None
def add_base_offset_generate_mmio_commands_dump(tenh_offset_file):
    try:
        with open(tenh_offset_file, 'r', encoding='utf-16le') as tenh_offset_file:
            # Tenh Offset read from the file.
            tenh_offset_read = tenh_offset_file.readline().strip()
            tenh_offset_split = list(tenh_offset_read)
            
            # Changing last value to 0 and converting it to hex -> to get base address.
            tenh_offset_split[-1] = '0'
            tenh_offset_string = ''.join(tenh_offset_split)
            base_address = int(tenh_offset_string[6:], 16)
            base_address = int(tenh_offset_string[6:], 16)
    except Exception as e:
        print(f"error: {e}")

    # Opening Predefined JSON that has offsets of eDP, HDMI, DP and their respective names.
    try:
        with open('single_mmio_offsets.json', 'r') as offsetsjson:
            all_offsets = json.load(offsetsjson)
    except Exception as e:
        print(f"error: {e}")

    # Generating MMIO_dump_commands_nsh file by adding base_address and offsets.
    for each_offset in all_offsets:
        offset = int(each_offset, 16)
        base_plus_offset = base_address + offset
        hex_base_plus_offset = hex(base_plus_offset)
        
        if each_offset == list(all_offsets.keys())[0]:
            try:
                with open('mmio_dump_commands_nsh.nsh', 'w') as MMIO_dump_commands_nsh_first_value:
                    MMIO_dump_commands_nsh_first_value.write(f'mm -w 4 {hex_base_plus_offset} > mmio_raw_dump.txt\n')
            except Exception as e:
                print(f"error: {e}")
        else:
            try:
                with open('mmio_dump_commands_nsh.nsh', 'a') as MMIO_dump_commands_nsh:
                    MMIO_dump_commands_nsh.write(f'mm -w 4 {hex_base_plus_offset} >> mmio_raw_dump.txt\n')
            except Exception as e:
                print(f"error: {e}")


add_base_offset_generate_mmio_commands_dump('tenh_offset.txt')
