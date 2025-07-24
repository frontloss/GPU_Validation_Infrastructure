#######################################################################################################################
# @file         hf_vsdb_data_mappers.py
# @brief        This file contains mappers to map the byte data to useful information tha can be used in verification
#
# @author       Praburaj Krishnan
#######################################################################################################################

from typing import Tuple, Dict

# Key: Byte Data From the EDID
# Value: Tuple[Link Rate, Lane Count]
DSC_FRL_RATE_MAPPING: Dict[int, Tuple[int, int]] = {
    0x0: (0, 0),
    0x1: (3, 3),
    0x2: (6, 3),
    0x3: (6, 4),
    0x4: (8, 4),
    0x5: (10, 4),
    0x6: (12, 4)
}

# Key: Byte Data From the EDID
# Value: Tuple[Link Rate, Lane Count]
FRL_RATE_MAPPING: Dict[int, Tuple[int, int]] = {
    0x0: (0, 0),
    0x1: (3, 3),
    0x2: (6, 3),
    0x3: (6, 4),
    0x4: (8, 4),
    0x5: (10, 4),
    0x6: (12, 4)
}

# Key: Byte Data From the EDID
# Value: Tuple[Slice Supported, Pixel Clock Per Slice]
DSC_MAX_SLICES_MAPPING: Dict[int, Tuple[int, int]] = {
    0x0: (0, 0),
    0x1: (1, 340),
    0x2: (2, 340),
    0x3: (4, 340),
    0x4: (8, 340),
    0x5: (8, 400),
    0x6: (12, 400),
    0x7: (16, 400)
}

# Key: Byte Data From the EDID
# Value: Tuple[Link Rate, Lane Count]
FRL_RATE_MAPPING: Dict[int, Tuple[int, int]] = {
    0x0: (0, 0),
    0x1: (3, 3),
    0x2: (6, 3),
    0x3: (6, 4),
    0x4: (8, 4),
    0x5: (10, 4),
    0x6: (12, 4)
}
