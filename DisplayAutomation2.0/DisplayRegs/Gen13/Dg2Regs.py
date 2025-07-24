# ===========================================================================
#
#    Copyright (c) Intel Corporation (2000 - 2020)
#
#    INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
#    ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
#    INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
#    ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
#    MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
#    OTHER WARRANTY.  Intel disclaims all liability, including liability for
#    infringement of any proprietary rights, relating to use of the code. No license,
#    express or implied, by estoppel or otherwise, to any intellectual property
#    rights is granted herein.
#
# --------------------------------------------------------------------------
#
# @file Dg2Regs.py
# @brief contains Dg2Regs.py related register definitions

import ctypes
from enum import Enum


class OFFSET_DFHASH:
    DFHASH = 0x51090


class _DFHASH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hash_Idi_Mask', ctypes.c_uint32, 4),
        ('Hash_Mc_Base_Bit', ctypes.c_uint32, 10),
        ('Hash_Sq_Base_Bit', ctypes.c_uint32, 10),
        ('Hash_Dev_Mem_En', ctypes.c_uint32, 8),
        ('Hash_Spare', ctypes.c_uint32, 2),
        ('Hash_Mem_L3_En', ctypes.c_uint32, 4),
        ('Hash_L3_Mode', ctypes.c_uint32, 2),
        ('Hash_L3_Bank_Exclude_Mask', ctypes.c_uint32, 3),
        ('Hash_L3_Node_Exclude_Mask', ctypes.c_uint32, 3),
        ('Hash_Mc_Xor', ctypes.c_uint32, 18),
    ]


class REG_DFHASH(ctypes.Union):
    value = 0
    offset = 0

    Hash_Idi_Mask = 0  # bit 0 to 4
    Hash_Mc_Base_Bit = 0  # bit 4 to 14
    Hash_Sq_Base_Bit = 0  # bit 14 to 24
    Hash_Dev_Mem_En = 0  # bit 24 to 32
    Hash_Spare = 0  # bit 0 to 2
    Hash_Mem_L3_En = 0  # bit 2 to 6
    Hash_L3_Mode = 0  # bit 6 to 8
    Hash_L3_Bank_Exclude_Mask = 0  # bit 8 to 11
    Hash_L3_Node_Exclude_Mask = 0  # bit 11 to 14
    Hash_Mc_Xor = 0  # bit 14 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DFHASH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DFHASH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

