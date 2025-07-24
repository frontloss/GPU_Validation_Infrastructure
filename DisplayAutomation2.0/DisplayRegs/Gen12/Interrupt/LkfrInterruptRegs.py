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
# @file LkfrInterruptRegs.py
# @brief contains LkfrInterruptRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_PART_A_HISTOGRAM_LATE(Enum):
    PART_A_HISTOGRAM_LATE_NOT_LATE = 0x0
    PART_A_HISTOGRAM_LATE_LATE = 0x1


class ENUM_PART_A_HISTOGRAM_OVERLAP(Enum):
    PART_A_HISTOGRAM_OVERLAP_NOT_OVERLAP = 0x0
    PART_A_HISTOGRAM_OVERLAP_OVERLAP = 0x1


class ENUM_PART_A_IET_LATE(Enum):
    PART_A_IET_LATE_NOT_LATE = 0x0
    PART_A_IET_LATE_LATE = 0x1


class ENUM_PART_A_IET_OVERLAP(Enum):
    PART_A_IET_OVERLAP_NOT_LATE = 0x0
    PART_A_IET_OVERLAP_LATE = 0x1


class ENUM_PART_A_HISTOGRAM_READY(Enum):
    PART_A_HISTOGRAM_READY_NOT_READY = 0x0
    PART_A_HISTOGRAM_READY_READY = 0x1


class ENUM_PART_A_LOAD_IE(Enum):
    PART_A_LOAD_IE_READY_DONE = 0x0
    PART_A_LOAD_IE_LOADING = 0x1


class ENUM_PART_A_HISTOGRAM_COPY_DONE(Enum):
    PART_A_HISTOGRAM_COPY_DONE_NOT_DONE = 0x0
    PART_A_HISTOGRAM_COPY_DONE_DONE = 0x1


class ENUM_PART_B_HISTOGRAM_LATE(Enum):
    PART_B_HISTOGRAM_LATE_NOT_LATE = 0x0
    PART_B_HISTOGRAM_LATE_LATE = 0x1


class ENUM_PART_B_HISTOGRAM_OVERLAP(Enum):
    PART_B_HISTOGRAM_OVERLAP_NOT_OVERLAP = 0x0
    PART_B_HISTOGRAM_OVERLAP_OVERLAP = 0x1


class ENUM_PART_B_IET_LATE(Enum):
    PART_B_IET_LATE_NOT_LATE = 0x0
    PART_B_IET_LATE_LATE = 0x1


class ENUM_PART_B_IET_OVERLAP(Enum):
    PART_B_IET_OVERLAP_NOT_LATE = 0x0
    PART_B_IET_OVERLAP_LATE = 0x1


class ENUM_PART_B_HISTOGRAM_READY(Enum):
    PART_B_HISTOGRAM_READY_NOT_READY = 0x0
    PART_B_HISTOGRAM_READY_READY = 0x1


class ENUM_PART_B_LOAD_IE(Enum):
    PART_B_LOAD_IE_READY_DONE = 0x0
    PART_B_LOAD_IE_LOADING = 0x1


class ENUM_PART_B_HISTOGRAM_COPY_DONE(Enum):
    PART_B_HISTOGRAM_COPY_DONE_NOT_DONE = 0x0
    PART_B_HISTOGRAM_COPY_DONE_DONE = 0x1


class OFFSET_DPLC_FA_IIR:
    DPLC_FA_IIR_A = 0x49468
    DPLC_FA_IIR_B = 0x494E8


class _DPLC_FA_IIR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PartAHistogramLate', ctypes.c_uint32, 1),
        ('PartAHistogramOverlap', ctypes.c_uint32, 1),
        ('PartAIetLate', ctypes.c_uint32, 1),
        ('PartAIetOverlap', ctypes.c_uint32, 1),
        ('PartAHistogramReady', ctypes.c_uint32, 1),
        ('PartALoadIe', ctypes.c_uint32, 1),
        ('PartAHistogramCopyDone', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 9),
        ('PartBHistogramLate', ctypes.c_uint32, 1),
        ('PartBHistogramOverlap', ctypes.c_uint32, 1),
        ('PartBIetLate', ctypes.c_uint32, 1),
        ('PartBIetOverlap', ctypes.c_uint32, 1),
        ('PartBHistogramReady', ctypes.c_uint32, 1),
        ('PartBLoadIe', ctypes.c_uint32, 1),
        ('PartBHistogramCopyDone', ctypes.c_uint32, 1),
        ('Reserved23', ctypes.c_uint32, 9),
    ]


class REG_DPLC_FA_IIR(ctypes.Union):
    value = 0
    offset = 0

    PartAHistogramLate = 0  # bit 0 to 1
    PartAHistogramOverlap = 0  # bit 1 to 2
    PartAIetLate = 0  # bit 2 to 3
    PartAIetOverlap = 0  # bit 3 to 4
    PartAHistogramReady = 0  # bit 4 to 5
    PartALoadIe = 0  # bit 5 to 6
    PartAHistogramCopyDone = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 16
    PartBHistogramLate = 0  # bit 16 to 17
    PartBHistogramOverlap = 0  # bit 17 to 18
    PartBIetLate = 0  # bit 18 to 19
    PartBIetOverlap = 0  # bit 19 to 20
    PartBHistogramReady = 0  # bit 20 to 21
    PartBLoadIe = 0  # bit 21 to 22
    PartBHistogramCopyDone = 0  # bit 22 to 23
    Reserved23 = 0  # bit 23 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_FA_IIR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_FA_IIR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PART_A_HISTOGRAM_LATE_MASK(Enum):
    PART_A_HISTOGRAM_LATE_MASK_UNMASK = 0x0
    PART_A_HISTOGRAM_LATE_MASK_MASK = 0x1


class ENUM_PART_A_HISTOGRAM_OVERLAP_MASK(Enum):
    PART_A_HISTOGRAM_OVERLAP_MASK_UNMASK = 0x0
    PART_A_HISTOGRAM_OVERLAP_MASK_MASK = 0x1


class ENUM_PART_A_IET_LATE_MASK(Enum):
    PART_A_IET_LATE_MASK_UNMASK = 0x0
    PART_A_IET_LATE_MASK_MASK = 0x1


class ENUM_PART_A_IET_OVERLAP_MASK(Enum):
    PART_A_IET_OVERLAP_MASK_UNMASK = 0x0
    PART_A_IET_OVERLAP_MASK_MASK = 0x1


class ENUM_PART_A_HISTOGRAM_READY_MASK(Enum):
    PART_A_HISTOGRAM_READY_MASK_UNMASK = 0x0
    PART_A_HISTOGRAM_READY_MASK_MASK = 0x1


class ENUM_PART_A_LOAD_IE_MASK(Enum):
    PART_A_LOAD_IE_MASK_UNMASK = 0x0
    PART_A_LOAD_IE_MASK_MASK = 0x1


class ENUM_PART_A_HISTOGRAM_COPY_DONE_MASK(Enum):
    PART_A_HISTOGRAM_COPY_DONE_MASK_UNMASK = 0x0
    PART_A_HISTOGRAM_COPY_DONE_MASK_MASK = 0x1


class ENUM_PART_B_HISTOGRAM_LATE_MASK(Enum):
    PART_B_HISTOGRAM_LATE_MASK_UNMASK = 0x0
    PART_B_HISTOGRAM_LATE_MASK_MASK = 0x1


class ENUM_PART_B_HISTOGRAM_OVERLAP_MASK(Enum):
    PART_B_HISTOGRAM_OVERLAP_MASK_UNMASK = 0x0
    PART_B_HISTOGRAM_OVERLAP_MASK_MASK = 0x1


class ENUM_PART_B_IET_LATE_MASK(Enum):
    PART_B_IET_LATE_MASK_UNMASK = 0x0
    PART_B_IET_LATE_MASK_MASK = 0x1


class ENUM_PART_B_IET_OVERLAP_MASK(Enum):
    PART_B_IET_OVERLAP_MASK_UNMASK = 0x0
    PART_B_IET_OVERLAP_MASK_MASK = 0x1


class ENUM_PART_B_HISTOGRAM_READY_MASK(Enum):
    PART_B_HISTOGRAM_READY_MASK_UNMASK = 0x0
    PART_B_HISTOGRAM_READY_MASK_MASK = 0x1


class ENUM_PART_B_LOAD_IE_MASK(Enum):
    PART_B_LOAD_IE_MASK_UNMASK = 0x0
    PART_B_LOAD_IE_MASK_MASK = 0x1


class ENUM_PART_B_HISTOGRAM_COPY_DONE_MASK(Enum):
    PART_B_HISTOGRAM_COPY_DONE_MASK_UNMASK = 0x0
    PART_B_HISTOGRAM_COPY_DONE_MASK_MASK = 0x1


class OFFSET_DPLC_FA_IMR:
    DPLC_FA_IMR_A = 0x49464
    DPLC_FA_IMR_B = 0x494E4


class _DPLC_FA_IMR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PartAHistogramLateMask', ctypes.c_uint32, 1),
        ('PartAHistogramOverlapMask', ctypes.c_uint32, 1),
        ('PartAIetLateMask', ctypes.c_uint32, 1),
        ('PartAIetOverlapMask', ctypes.c_uint32, 1),
        ('PartAHistogramReadyMask', ctypes.c_uint32, 1),
        ('PartALoadIeMask', ctypes.c_uint32, 1),
        ('PartAHistogramCopyDoneMask', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 9),
        ('PartBHistogramLateMask', ctypes.c_uint32, 1),
        ('PartBHistogramOverlapMask', ctypes.c_uint32, 1),
        ('PartBIetLateMask', ctypes.c_uint32, 1),
        ('PartBIetOverlapMask', ctypes.c_uint32, 1),
        ('PartBHistogramReadyMask', ctypes.c_uint32, 1),
        ('PartBLoadIeMask', ctypes.c_uint32, 1),
        ('PartBHistogramCopyDoneMask', ctypes.c_uint32, 1),
        ('Reserved23', ctypes.c_uint32, 9),
    ]


class REG_DPLC_FA_IMR(ctypes.Union):
    value = 0
    offset = 0

    PartAHistogramLateMask = 0  # bit 0 to 1
    PartAHistogramOverlapMask = 0  # bit 1 to 2
    PartAIetLateMask = 0  # bit 2 to 3
    PartAIetOverlapMask = 0  # bit 3 to 4
    PartAHistogramReadyMask = 0  # bit 4 to 5
    PartALoadIeMask = 0  # bit 5 to 6
    PartAHistogramCopyDoneMask = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 16
    PartBHistogramLateMask = 0  # bit 16 to 17
    PartBHistogramOverlapMask = 0  # bit 17 to 18
    PartBIetLateMask = 0  # bit 18 to 19
    PartBIetOverlapMask = 0  # bit 19 to 20
    PartBHistogramReadyMask = 0  # bit 20 to 21
    PartBLoadIeMask = 0  # bit 21 to 22
    PartBHistogramCopyDoneMask = 0  # bit 22 to 23
    Reserved23 = 0  # bit 23 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_FA_IMR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_FA_IMR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

