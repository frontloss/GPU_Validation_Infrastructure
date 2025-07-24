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
# @file NonAutoGenRegs.py
# @brief contains Platform Common Non Auto Generated register definitions

import ctypes
from enum import Enum


class OFFSET_SWF06:
    SW06 = 0x4F018

class _SWF06(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MaxCdClockSupported', ctypes.c_uint32, 11),
        ('Reserved21', ctypes.c_uint32, 21),
    ]


class REG_SWF06(ctypes.Union):
    value = 0
    offset = 0

    MaxCdClockSupported = 0 # bit 0 to bit 11
    Reserved21 = 0 # bit 12 to bit 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SWF06),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SWF06, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SWF_32:
    SWF_32 = 0x4F080


class _SWF_32(ctypes.LittleEndianStructure):
    _fields_ = [
        ("software_flags", ctypes.c_uint32, 32),  # 0 to 31
    ]


class REG_SWF_32(ctypes.Union):
    value = 0
    offset = 0

    software_flags = 0   # bit 0 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SWF_32),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SWF_32, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value
