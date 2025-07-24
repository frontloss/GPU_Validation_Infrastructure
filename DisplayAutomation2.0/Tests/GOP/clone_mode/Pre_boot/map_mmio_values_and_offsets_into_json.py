########################################################################################################################
# @file         map_mmio_values_and_offsets_into_json.py
# @brief        Using the generated MMIO_raw_dump.txt and clone_mmio_offsets.json files, map the MMIO values with
#               their corresponding offsets and generated a final MMIO_dump.json file (final MMIO dump).
# @author       GOLI S V N LAKSHMI BHAVANI
########################################################################################################################

import json


##
# @brief        map the MMIO values with their corresponding offsets and generated a final MMIO_dump.json file.
# @param        dump, offsetsjson
# @return       None
def map_mmio_values_and_offsets_into_json(dump, offsetsjson):
    # Opening MMIO_raw_dump file
    try:
        with open(dump, 'r', encoding='utf-16le') as MMIO_raw_dump_file:
            mmio_raw_dump_list = [line.strip() for line in MMIO_raw_dump_file]
    except Exception as e:
        print(f"error: {e}")
    
    # Opening offsets json.
    try:
        with open(offsetsjson, 'r') as offsets_json:
            all_offsets = json.loads(offsets_json.read())
    except Exception as e:
        print(f"error: {e}")
    
    # Combining Offset, Offset_name and corresponding MMIO value to a single json.
    combined_data = []
    for (offset, name), MMIO_value in zip(all_offsets.items(), mmio_raw_dump_list):
        if offset == list(all_offsets.keys())[0]:
            combined_data.append({
                "MMIO Offset": offset,
                "Function Name": name,
                "Expected Output": MMIO_value[1:]
            })
        else:
            combined_data.append({
                "MMIO Offset": offset,
                "Function Name": name,
                "Expected Output": MMIO_value
            })
        
    try:
        with open('mmio_dump.json', 'w') as MMIO_dump_json:
            json.dump(combined_data, MMIO_dump_json, indent=4)
    except Exception as e:
        print(f"error: {e}")  


map_mmio_values_and_offsets_into_json('mmio_raw_dump.txt', 'clone_mmio_offsets.json')
