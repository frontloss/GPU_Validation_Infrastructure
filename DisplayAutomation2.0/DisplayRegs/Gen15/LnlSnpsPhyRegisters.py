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
# @file LnlSnpsPhyRegisters.py
# @brief contains Non Auto Generated register definitions for LNL external PHY (Synopsys PHY) registers.
# @details these registers are not in MMIO format. The register offsets are in 16-bit format, data width of SRAM
#           registers is 16-bit and data width of VDR registers is 8-bit. These register definitions are not given in
#           regular bspec xml format (like MMIO reg), but there are provided in tables in below bspec pages.
#           C10 PHY registers: https://gfxspecs.intel.com/Predator/Home/Index/68962?dstFilter=LNL&mode=Filter
#           C20 PHY registers: https://gfxspecs.intel.com/Predator/Home/Index/68962?dstFilter=LNL&mode=Filter

import ctypes


class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_10:
    CONTEXT_B = 0xCB44
    CONTEXT_A = 0xCB50


class _SRAM_GENERIC_MPLLB_CNTX_CFG_10(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HdmiDiv', ctypes.c_uint16, 3),
        ('HdmiPixelClkDiv', ctypes.c_uint16, 2),
        ('Reserved5', ctypes.c_uint16, 11),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_10(ctypes.Union):
    value = 0
    offset = 0

    HdmiDiv = 0             # bit 0 to 2
    HdmiPixelClkDiv = 0     # bit 3 to 4
    Reserved5 = 0           # bit 5 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_10),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_10, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_9:
    CONTEXT_B = 0xCB45
    CONTEXT_A = 0xCB51


class _SRAM_GENERIC_MPLLB_CNTX_CFG_9(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracRem', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_9(ctypes.Union):
    value = 0
    offset = 0

    FracRem = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_9),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_9, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_8:
    CONTEXT_B = 0xCB46
    CONTEXT_A = 0xCB52


class _SRAM_GENERIC_MPLLB_CNTX_CFG_8(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracQuot', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_8(ctypes.Union):
    value = 0
    offset = 0

    FracQuot = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_8),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_8, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_7:
    CONTEXT_B = 0xCB47
    CONTEXT_A = 0xCB53


class _SRAM_GENERIC_MPLLB_CNTX_CFG_7(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracDen', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_7(ctypes.Union):
    value = 0
    offset = 0

    FracDen = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_7),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_7, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_6:
    CONTEXT_B = 0xCB48
    CONTEXT_A = 0xCB54


class _SRAM_GENERIC_MPLLB_CNTX_CFG_6(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscPeak', ctypes.c_uint16, 4),
        ('SscStepSize', ctypes.c_uint16, 5),
        ('SscUpSpread', ctypes.c_uint16, 1),
        ('RefClkDiv', ctypes.c_uint16, 3),
        ('FracEn', ctypes.c_uint16, 1),
        ('Reserved14', ctypes.c_uint16, 2),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_6(ctypes.Union):
    value = 0
    offset = 0

    SscPeak = 0         # bit 0 to 3
    SscStepSize = 0     # bit 4 to 8
    SscUpSpread = 0     # bit 9 to 9
    RefClkDiv = 0       # bit 10 to 12
    FracEn = 0          # bit 13 to 13
    Reserved14 = 0      # bit 14 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_6),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_6, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_5:
    CONTEXT_B = 0xCB49
    CONTEXT_A = 0xCB55


class _SRAM_GENERIC_MPLLB_CNTX_CFG_5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscStepSize', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_5(ctypes.Union):
    value = 0
    offset = 0

    SscStepSize = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_5),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_4:
    CONTEXT_B = 0xCB4A
    CONTEXT_A = 0xCB56


class _SRAM_GENERIC_MPLLB_CNTX_CFG_4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscPeak', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_4(ctypes.Union):
    value = 0
    offset = 0

    SscPeak = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_4),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_3:
    CONTEXT_B = 0xCB4B
    CONTEXT_A = 0xCB57


class _SRAM_GENERIC_MPLLB_CNTX_CFG_3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CpIntGs', ctypes.c_uint16, 7),
        ('CpPropGs', ctypes.c_uint16, 7),
        ('V2i', ctypes.c_uint16, 2),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_3(ctypes.Union):
    value = 0
    offset = 0

    CpIntGs = 0     # bit 0 to 6
    CpPropGs = 0    # bit 7 to 13
    V2i = 0         # bit 14 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_3),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_2:
    CONTEXT_B = 0xCB4C
    CONTEXT_A = 0xCB58


class _SRAM_GENERIC_MPLLB_CNTX_CFG_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CpInt', ctypes.c_uint16, 7),
        ('CpProp', ctypes.c_uint16, 7),
        ('FreqVco', ctypes.c_uint16, 2),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_2(ctypes.Union):
    value = 0
    offset = 0

    CpInt = 0       # bit 0 to 6
    CpProp = 0      # bit 7 to 13
    FreqVco = 0     # bit 14 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_2),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_1:
    CONTEXT_B = 0xCB4D
    CONTEXT_A = 0xCB59


class _SRAM_GENERIC_MPLLB_CNTX_CFG_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DivMultiplier', ctypes.c_uint16, 8),
        ('WordClkDiv', ctypes.c_uint16, 2),
        ('CalDacCode', ctypes.c_uint16, 5),
        ('Reserved15', ctypes.c_uint16, 1),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_1(ctypes.Union):
    value = 0
    offset = 0

    DivMultiplier = 0   # bit 0 to 7
    WordClkDiv = 0      # bit 8 to 9
    CalDacCode = 0      # bit 10 to 14
    Reserved15 = 0      # bit 15 to 15


    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_1),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_0:
    CONTEXT_B = 0xCB4E
    CONTEXT_A = 0xCB5A


class _SRAM_GENERIC_MPLLB_CNTX_CFG_0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Multiplier', ctypes.c_uint16, 12),
        ('DivClkEn', ctypes.c_uint16, 1),
        ('TxClkDiv', ctypes.c_uint16, 3),
    ]


class REG_SRAM_GENERIC_MPLLB_CNTX_CFG_0(ctypes.Union):
    value = 0
    offset = 0

    Multiplier = 0  # bit 0 to 11
    DivClkEn = 0    # bit 12 to 12
    TxClkDiv = 0    # bit 13 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLB_CNTX_CFG_0),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLB_CNTX_CFG_0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_9:
    CONTEXT_B = 0xCCDC
    CONTEXT_A = 0xCCE7


class _SRAM_GENERIC_MPLLA_CNTX_CFG_9(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracRem', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLA_CNTX_CFG_9(ctypes.Union):
    value = 0
    offset = 0

    FracRem = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLA_CNTX_CFG_9),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLA_CNTX_CFG_9, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_8:
    CONTEXT_B = 0xCCDD
    CONTEXT_A = 0xCCE8


class _SRAM_GENERIC_MPLLA_CNTX_CFG_8(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracQuot', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLA_CNTX_CFG_8(ctypes.Union):
    value = 0
    offset = 0

    FracQuot = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLA_CNTX_CFG_8),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLA_CNTX_CFG_8, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_7:
    CONTEXT_B = 0xCCDE
    CONTEXT_A = 0xCCE9


class _SRAM_GENERIC_MPLLA_CNTX_CFG_7(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracDen', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLA_CNTX_CFG_7(ctypes.Union):
    value = 0
    offset = 0

    FracDen = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLA_CNTX_CFG_7),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLA_CNTX_CFG_7, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_6:
    CONTEXT_B = 0xCCDF
    CONTEXT_A = 0xCCEA


class _SRAM_GENERIC_MPLLA_CNTX_CFG_6(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscPeak', ctypes.c_uint16, 4),
        ('SscStepSize', ctypes.c_uint16, 5),
        ('SscUpSpread', ctypes.c_uint16, 1),
        ('RefClkDiv', ctypes.c_uint16, 3),
        ('LcFreqSel', ctypes.c_uint16, 1),
        ('FracEn', ctypes.c_uint16, 1),
        ('Reserved15', ctypes.c_uint16, 1),
    ]


class REG_SRAM_GENERIC_MPLLA_CNTX_CFG_6(ctypes.Union):
    value = 0
    offset = 0

    SscPeak = 0         # bit 0 to 3
    SscStepSize = 0     # bit 4 to 8
    SscUpSpread = 0     # bit 9 to 9
    RefClkDiv = 0       # bit 10 to 12
    LcFreqSel = 0       # bit 13 to 13
    FracEn = 0          # bit 14 to 14
    Reserved15 = 0      # bit 15 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLA_CNTX_CFG_6),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLA_CNTX_CFG_6, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_5:
    CONTEXT_B = 0xCCE0
    CONTEXT_A = 0xCCEB


class _SRAM_GENERIC_MPLLA_CNTX_CFG_5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscStepSize', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLA_CNTX_CFG_5(ctypes.Union):
    value = 0
    offset = 0

    SscStepSize = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLA_CNTX_CFG_5),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLA_CNTX_CFG_5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_4:
    CONTEXT_B = 0xCCE1
    CONTEXT_A = 0xCCEC


class _SRAM_GENERIC_MPLLA_CNTX_CFG_4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscPeak', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLA_CNTX_CFG_4(ctypes.Union):
    value = 0
    offset = 0

    SscPeak = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLA_CNTX_CFG_4),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLA_CNTX_CFG_4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_3:
    CONTEXT_B = 0xCCE2
    CONTEXT_A = 0xCCED


class _SRAM_GENERIC_MPLLA_CNTX_CFG_3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BwHigh', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLA_CNTX_CFG_3(ctypes.Union):
    value = 0
    offset = 0

    BwHigh = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLA_CNTX_CFG_3),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLA_CNTX_CFG_3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_2:
    CONTEXT_B = 0xCCE3
    CONTEXT_A = 0xCCEE


class _SRAM_GENERIC_MPLLA_CNTX_CFG_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BwLow', ctypes.c_uint16, 16),
    ]


class REG_SRAM_GENERIC_MPLLA_CNTX_CFG_2(ctypes.Union):
    value = 0
    offset = 0

    BwLow = 0  # bit 0 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLA_CNTX_CFG_2),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLA_CNTX_CFG_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_1:
    CONTEXT_B = 0xCCE4
    CONTEXT_A = 0xCCEF


class _SRAM_GENERIC_MPLLA_CNTX_CFG_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DivMultiplier', ctypes.c_uint16, 8),
        ('TxClkDiv', ctypes.c_uint16, 3),
        ('WordClkDiv', ctypes.c_uint16, 2),
        ('CtlBufBypass', ctypes.c_uint16, 1),
        ('BwThreshold', ctypes.c_uint16, 2),
    ]


class REG_SRAM_GENERIC_MPLLA_CNTX_CFG_1(ctypes.Union):
    value = 0
    offset = 0

    DivMultiplier = 0  # bit 0 to 7
    TxClkDiv = 0  # bit 8 to 10
    WordClkDiv = 0  # bit 11 to 12
    CtlBufBypass = 0  # bit 13 to 13
    BwThreshold = 0  # bit 14 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLA_CNTX_CFG_1),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLA_CNTX_CFG_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_0:
    CONTEXT_B = 0xCCE5
    CONTEXT_A = 0xCCF0


class _SRAM_GENERIC_MPLLA_CNTX_CFG_0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Multiplier', ctypes.c_uint16, 12),
        ('DivClkEn', ctypes.c_uint16, 1),
        ('FbClkDiv4En', ctypes.c_uint16, 1),
        ('Div16p5ClkEn', ctypes.c_uint16, 1),
        ('ShortLockEn', ctypes.c_uint16, 1),
    ]


class REG_SRAM_GENERIC_MPLLA_CNTX_CFG_0(ctypes.Union):
    value = 0
    offset = 0

    Multiplier = 0  # bit 0 to 11
    DivClkEn = 0  # bit 12 to 12
    FbClkDiv4En = 0  # bit 13 to 13
    Div16p5ClkEn = 0  # bit 14 to 14
    ShortLockEn = 0  # bit 15 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_MPLLA_CNTX_CFG_0),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_MPLLA_CNTX_CFG_0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_3:
    CONTEXT_B = 0xCDA2
    CONTEXT_A = 0xCDA7


class _SRAM_GENERIC_CMN_CNTX_CFG_3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SupProtocolId', ctypes.c_uint16, 10),
        ('Reserved10', ctypes.c_uint16, 6),
    ]


class REG_SRAM_GENERIC_CMN_CNTX_CFG_3(ctypes.Union):
    value = 0
    offset = 0

    SupProtocolId = 0  # bit 0 to 9
    Reserved10 = 0  # bit 10 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_CMN_CNTX_CFG_3),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_CMN_CNTX_CFG_3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_2:
    CONTEXT_B = 0xCDA3
    CONTEXT_A = 0xCDA8


class _SRAM_GENERIC_CMN_CNTX_CFG_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RxTermOffset', ctypes.c_uint16, 5),
        ('TxupTermOffset', ctypes.c_uint16, 9),
        ('Reserved14', ctypes.c_uint16, 2),
    ]


class REG_SRAM_GENERIC_CMN_CNTX_CFG_2(ctypes.Union):
    value = 0
    offset = 0

    RxTermOffset = 0  # bit 0 to 4
    TxupTermOffset = 0  # bit 5 to 13
    Reserved14 = 0  # bit 14 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_CMN_CNTX_CFG_2),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_CMN_CNTX_CFG_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_1:
    CONTEXT_B = 0xCDA4
    CONTEXT_A = 0xCDA9


class _SRAM_GENERIC_CMN_CNTX_CFG_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RxVrefCtrl', ctypes.c_uint16, 5),
        ('TxdnTermOffset', ctypes.c_uint16, 9),
        ('Reserved14', ctypes.c_uint16, 2),
    ]


class REG_SRAM_GENERIC_CMN_CNTX_CFG_1(ctypes.Union):
    value = 0
    offset = 0

    RxVrefCtrl = 0  # bit 0 to 4
    TxdnTermOffset = 0  # bit 5 to 13
    Reserved14 = 0  # bit 14 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_CMN_CNTX_CFG_1),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_CMN_CNTX_CFG_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_CMN_CNTX_CFG_0:
    CONTEXT_B = 0xCDA5
    CONTEXT_A = 0xCDAA


class _SRAM_GENERIC_CMN_CNTX_CFG_0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SupMisc', ctypes.c_uint16, 8),
        ('TxVboostLv', ctypes.c_uint16, 3),
        ('Reserved11', ctypes.c_uint16, 5),
    ]


class REG_SRAM_GENERIC_CMN_CNTX_CFG_0(ctypes.Union):
    value = 0
    offset = 0

    SupMisc = 0  # bit 0 to 7
    TxVboostLv = 0  # bit 8 to 10
    Reserved11 = 0  # bit 11 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_CMN_CNTX_CFG_0),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_CMN_CNTX_CFG_0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_TX_CNTX_CFG_2:
    CONTEXT_B = 0xCF28
    CONTEXT_A = 0xCF2C


class _SRAM_GENERIC_TX_CNTX_CFG_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LaneProtocolId', ctypes.c_uint16, 8),
        ('Reserved8', ctypes.c_uint16, 8),
    ]


class REG_SRAM_GENERIC_TX_CNTX_CFG_2(ctypes.Union):
    value = 0
    offset = 0

    LaneProtocolId = 0  # bit 0 to 7
    Reserved8 = 0  # bit 8 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_TX_CNTX_CFG_2),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_TX_CNTX_CFG_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_TX_CNTX_CFG_1:
    CONTEXT_B = 0xCF29
    CONTEXT_A = 0xCF2D


class _SRAM_GENERIC_TX_CNTX_CFG_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxXMisc', ctypes.c_uint16, 8),
        ('TxXDccCalDacCtrlRange', ctypes.c_uint16, 4),
        ('TxXDccBypass', ctypes.c_uint16, 1),
        ('TxXTermCtrl', ctypes.c_uint16, 3),
    ]


class REG_SRAM_GENERIC_TX_CNTX_CFG_1(ctypes.Union):
    value = 0
    offset = 0

    TxXMisc = 0                 # bit 0 to 7
    TxXDccCalDacCtrlRange = 0   # bit 8 to 11
    TxXDccBypass = 0            # bit 12 to 12
    TxXTermCtrl = 0             # bit 13 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_TX_CNTX_CFG_1),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_TX_CNTX_CFG_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_SRAM_GENERIC_TX_CNTX_CFG_0:
    CONTEXT_B = 0xCF2A
    CONTEXT_A = 0xCF2E


class _SRAM_GENERIC_TX_CNTX_CFG_0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxXRate', ctypes.c_uint16, 3),
        ('TxXWidth', ctypes.c_uint16, 3),
        ('TxXAlignWideXferEn', ctypes.c_uint16, 1),
        ('TxXMpllbSel', ctypes.c_uint16, 1),
        ('TxXVregdrvByp', ctypes.c_uint16, 1),
        ('TxXVboostEn', ctypes.c_uint16, 1),
        ('TxXIboostLvl', ctypes.c_uint16, 4),
        ('TxXDrvEnKr', ctypes.c_uint16, 1),
        ('TxXOffcanCont', ctypes.c_uint16, 1),
    ]


class REG_SRAM_GENERIC_TX_CNTX_CFG_0(ctypes.Union):
    value = 0
    offset = 0

    TxXRate = 0             # bit 0 to 2
    TxXWidth = 0            # bit 3 to 5
    TxXAlignWideXferEn = 0  # bit 6 to 6
    TxXMpllbSel = 0         # bit 7 to 7
    TxXVregdrvByp = 0       # bit 8 to 8
    TxXVboostEn = 0         # bit 9 to 9
    TxXIboostLvl = 0        # bit 10 to 13
    TxXDrvEnKr = 0          # bit 14 to 14
    TxXOffcanCont = 0       # bit 15 to 15

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRAM_GENERIC_TX_CNTX_CFG_0),
        ('value', ctypes.c_uint16)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRAM_GENERIC_TX_CNTX_CFG_0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_TX_CONTROL2:
    TX1 = 0x402
    TX2 = 0x602


class _PHY_TX_CONTROL2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxDeemph5To0', ctypes.c_uint8, 6),
        ('DisableSingleTx', ctypes.c_uint8, 1),
        ('Reserved7', ctypes.c_uint8, 1)
    ]


class REG_PHY_TX_CONTROL2(ctypes.Union):
    value = 0
    offset = 0

    TxDeemph5To0 = 0            # bit 0 to 5
    DisableSingleTx = 0     # bit 6 to 6
    Reserved7 = 0           # bit 7 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_TX_CONTROL2),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_TX_CONTROL2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_TX_CONTROL3:
    TX1 = 0x403
    TX2 = 0x603


class _PHY_TX_CONTROL3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxDeemph11To6', ctypes.c_uint8, 6),
        ('Reserved6', ctypes.c_uint8, 2)
    ]


class REG_PHY_TX_CONTROL3(ctypes.Union):
    value = 0
    offset = 0

    TxDeemph11To6 = 0       # bit 0 to 5
    Reserved6 = 0           # bit 6 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_TX_CONTROL3),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_TX_CONTROL3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_TX_CONTROL4:
    TX1 = 0x404
    TX2 = 0x604


class _PHY_TX_CONTROL4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxDeemph17To12', ctypes.c_uint8, 6),
        ('Reserved6', ctypes.c_uint8, 2)
    ]


class REG_PHY_TX_CONTROL4(ctypes.Union):
    value = 0
    offset = 0

    TxDeemph17To12 = 0      # bit 0 to 5
    Reserved6 = 0           # bit 6 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_TX_CONTROL4),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_TX_CONTROL4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_TX_CONTROL8:
    TX1 = 0x408
    TX2 = 0x608


class _PHY_TX_CONTROL8(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxMargin', ctypes.c_uint8, 3),
        ('TxSwing', ctypes.c_uint8, 1),
        ('Reserved4', ctypes.c_uint8, 4)
    ]


class REG_PHY_TX_CONTROL8(ctypes.Union):
    value = 0
    offset = 0

    TxMargin = 0            # bit 0 to 2
    TxSwing = 0             # bit 3 to 3
    Reserved4 = 0           # bit 4 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_TX_CONTROL8),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_TX_CONTROL8, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_CMN_CONTROL0:
    offset = 0x800


class _PHY_CMN_CONTROL0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EncodeDecodeBypass', ctypes.c_uint8, 1),
        ('MacTransmitLFPS', ctypes.c_uint8, 1),
        ('Reserved2', ctypes.c_uint8, 6)
    ]


class REG_PHY_CMN_CONTROL0(ctypes.Union):
    value = 0
    offset = 0

    EncodeDecodeBypass = 0            # bit 0
    MacTransmitLFPS = 0             # bit 1
    Reserved2 = 0           # bit 2 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_CMN_CONTROL0),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_CMN_CONTROL0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL0:
    offset = 0xC00


class _PHY_C10_VDR_PLL0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscEn', ctypes.c_uint8, 1),
        ('DivClkEn', ctypes.c_uint8, 1),
        ('Div5ClkEn', ctypes.c_uint8, 1),
        ('WordDiv2En', ctypes.c_uint8, 1),
        ('FracnEn', ctypes.c_uint8, 1),
        ('PmixEn', ctypes.c_uint8, 1),
        ('FreqVco', ctypes.c_uint8, 2),
    ]


class REG_PHY_C10_VDR_PLL0(ctypes.Union):
    value = 0
    offset = 0

    SscEn = 0       # bit 0 to 0
    DivClkEn = 0    # bit 1 to 1
    Div5ClkEn = 0   # bit 2 to 2
    WordDiv2En = 0  # bit 3 to 3
    FracnEn = 0     # bit 4 to 4
    PmixEn = 0      # bit 5 to 5
    FreqVco = 0     # bit 6 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL0),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL1:
    offset = 0xC01


class _PHY_C10_VDR_PLL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DivMultiplier', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL1(ctypes.Union):
    value = 0
    offset = 0

    DivMultiplier = 0       # bit 0 to 7


    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL1),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL2:
    offset = 0xC02


class _PHY_C10_VDR_PLL2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Multiplier', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL2(ctypes.Union):
    value = 0
    offset = 0

    Multiplier = 0       # bit 0 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL2),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL3:
    offset = 0xC03


class _PHY_C10_VDR_PLL3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Multiplier', ctypes.c_uint8, 4),
        ('SscPeak', ctypes.c_uint8, 4),
    ]


class REG_PHY_C10_VDR_PLL3(ctypes.Union):
    value = 0
    offset = 0

    Multiplier = 0      # bit 0 to 3
    SscPeak = 0         # bit 4 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL3),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL4:
    offset = 0xC04


class _PHY_C10_VDR_PLL4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscPeak', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL4(ctypes.Union):
    value = 0
    offset = 0

    SscPeak = 0       # bit 0 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL4),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL5:
    offset = 0xC05


class _PHY_C10_VDR_PLL5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscPeak', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL5(ctypes.Union):
    value = 0
    offset = 0

    SscPeak = 0       # bit 0 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL5),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL6:
    offset = 0xC06


class _PHY_C10_VDR_PLL6(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscStepsize', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL6(ctypes.Union):
    value = 0
    offset = 0

    SscStepsize = 0       # bit 0 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL6),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL6, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL7:
    offset = 0xC07


class _PHY_C10_VDR_PLL7(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscStepsize', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL7(ctypes.Union):
    value = 0
    offset = 0

    SscStepsize = 0       # bit 0 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL7),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL7, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL8:
    offset = 0xC08


class _PHY_C10_VDR_PLL8(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscStepsize', ctypes.c_uint8, 5),
        ('SscUpSpread', ctypes.c_uint8, 1),
        ('Reserved6', ctypes.c_uint8, 2),
    ]


class REG_PHY_C10_VDR_PLL8(ctypes.Union):
    value = 0
    offset = 0

    SscStepsize = 0     # bit 0 to 4
    SscUpSpread = 0     # bit 5 to 5
    Reserved6 = 0       # bit 6 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL8),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL8, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL9:
    offset = 0xC09


class _PHY_C10_VDR_PLL9(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracnDen', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL9(ctypes.Union):
    value = 0
    offset = 0

    FracnDen = 0       # bit 0 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL9),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL9, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL10:
    offset = 0xC0A


class _PHY_C10_VDR_PLL10(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracnDen', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL10(ctypes.Union):
    value = 0
    offset = 0

    FracnDen = 0       # bit 0 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL10),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL10, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL11:
    offset = 0xC0B


class _PHY_C10_VDR_PLL11(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracnQuot', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL11(ctypes.Union):
    value = 0
    offset = 0

    FracnQuot = 0       # bit 0 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL11),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL11, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL12:
    offset = 0xC0C


class _PHY_C10_VDR_PLL12(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracnQuot', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL12(ctypes.Union):
    value = 0
    offset = 0

    FracnQuot = 0       # bit 0 to 7


    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL12),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL12, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL13:
    offset = 0xC0D


class _PHY_C10_VDR_PLL13(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracnRem', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL13(ctypes.Union):
    value = 0
    offset = 0

    FracnRem = 0       # bit 0 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL13),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL13, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL14:
    offset = 0xC0E


class _PHY_C10_VDR_PLL14(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FracnRem', ctypes.c_uint8, 8),
    ]


class REG_PHY_C10_VDR_PLL14(ctypes.Union):
    value = 0
    offset = 0

    FracnRem = 0       # bit 0 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL14),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL14, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL15:
    offset = 0xC0F


class _PHY_C10_VDR_PLL15(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxClkDiv', ctypes.c_uint8, 3),
        ('HdmiDiv', ctypes.c_uint8, 3),
        ('HdmiPixelClkDiv', ctypes.c_uint8, 2),
    ]


class REG_PHY_C10_VDR_PLL15(ctypes.Union):
    value = 0
    offset = 0

    TxClkDiv = 0            # bit 0 to 2
    HdmiDiv = 0             # bit 3 to 5
    HdmiPixelClkDiv = 0     # bit 6 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL15),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL15, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL16:
    offset = 0xC10


class _PHY_C10_VDR_PLL16(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CpInt', ctypes.c_uint8, 7),
        ('CpIntGs', ctypes.c_uint8, 1),
    ]


class REG_PHY_C10_VDR_PLL16(ctypes.Union):
    value = 0
    offset = 0

    CpInt = 0       # bit 0 to 6
    CpIntGs = 0     # bit 7 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL16),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL16, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL17:
    offset = 0xC11


class _PHY_C10_VDR_PLL17(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CpIntGs', ctypes.c_uint8, 6),
        ('CpProp', ctypes.c_uint8, 2),
    ]


class REG_PHY_C10_VDR_PLL17(ctypes.Union):
    value = 0
    offset = 0

    CpIntGs = 0       # bit 0 to 5
    CpProp = 0        # bit 6 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL17),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL17, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL18:
    offset = 0xC12


class _PHY_C10_VDR_PLL18(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CpProp', ctypes.c_uint8, 5),
        ('CpPropGs', ctypes.c_uint8, 3),
    ]


class REG_PHY_C10_VDR_PLL18(ctypes.Union):
    value = 0
    offset = 0

    CpProp = 0       # bit 0 to 4
    CpPropGs = 0     # bit 5 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL18),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL18, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_PLL19:
    offset = 0xC13


class _PHY_C10_VDR_PLL19(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CpPropGs', ctypes.c_uint8, 4),
        ('V2i', ctypes.c_uint8, 2),
        ('Reserved6', ctypes.c_uint8, 2),
    ]


class REG_PHY_C10_VDR_PLL19(ctypes.Union):
    value = 0
    offset = 0

    CpPropGs = 0       # bit 0 to 3
    V2i = 0            # bit 4 to 5
    Reserved6 = 0      # bit 6 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_PLL19),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_PLL19, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_CMN0:
    offset = 0xC20


class _PHY_C10_VDR_CMN0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RefRange', ctypes.c_uint8, 5),
        ('RefClkMpllbDiv', ctypes.c_uint8, 3),
    ]


class REG_PHY_C10_VDR_CMN0(ctypes.Union):
    value = 0
    offset = 0

    RefRange = 0        # bit 0 to 4
    RefClkMpllbDiv = 0  # bit 5 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_CMN0),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_CMN0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_TX0:
    offset = 0xC30


class _PHY_C10_VDR_TX0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxWidthG1', ctypes.c_uint8, 2),
        ('TxWidthG2', ctypes.c_uint8, 2),
        ('TxMpllbSel', ctypes.c_uint8, 1),
        ('TxRateG1', ctypes.c_uint8, 3),
    ]


class REG_PHY_C10_VDR_TX0(ctypes.Union):
    value = 0
    offset = 0

    TxWidthG1 = 0       # bit 0 to 1
    TxWidthG2 = 0       # bit 2 to 3
    TxMpllbSel = 0      # bit 4 to 4
    TxRateG1 = 0        # bit 5 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_TX0),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_TX0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_CONTROL1:
    offset = 0xC70


class _PHY_C10_VDR_CONTROL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('UpdateConfigSettings', ctypes.c_uint8, 1),
        ('MasterLane', ctypes.c_uint8, 1),
        ('MsgBusAccessBit', ctypes.c_uint8, 1),
        ('Reserved3', ctypes.c_uint8, 5),
    ]


class REG_PHY_C10_VDR_CONTROL1(ctypes.Union):
    value = 0
    offset = 0

    UpdateConfigSettings = 0       # bit 0 to 0
    MasterLane = 0                 # bit 1 to 1
    MsgBusAccessBit = 0            # bit 2 to 2
    Reserved3 = 0                  # bit 3 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_CONTROL1),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_CONTROL1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_CUSTOM_SERDES:
    offset = 0xD00


class _PHY_C10_VDR_CUSTOM_SERDES(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ContextToggle', ctypes.c_uint8, 1),
        ('DpRateInCustomSerdes', ctypes.c_uint8, 4),
        ('HdmiPixelClkGate', ctypes.c_uint8, 1),
        ('IsDp', ctypes.c_uint8, 1),
        ('IsFrl', ctypes.c_uint8, 1),
    ]


class REG_PHY_C10_VDR_CUSTOM_SERDES(ctypes.Union):
    value = 0
    offset = 0

    ContextToggle = 0           # bit 0 to 0
    DpRateInCustomSerdes = 0    # bit 1 to 4
    HdmiPixelClkGate = 0        # bit 5 to 5
    IsDp = 0                    # bit 6 to 6
    IsFrl = 0                   # bit 7 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_CUSTOM_SERDES),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_CUSTOM_SERDES, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_C10_VDR_HDMI_RATE:
    offset = 0xD01


class _PHY_C10_VDR_HDMI_RATE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HdmiRate', ctypes.c_uint8, 2),
        ('Reserved2', ctypes.c_uint8, 6),
    ]


class REG_PHY_C10_VDR_HDMI_RATE(ctypes.Union):
    value = 0
    offset = 0

    HdmiRate = 0       # bit 0 to 1
    Reserved2 = 0      # bit 2 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_C10_VDR_HDMI_RATE),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_C10_VDR_HDMI_RATE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_VDR_CUSTOM_WIDTH:
    offset = 0xD02


class _PHY_VDR_CUSTOM_WIDTH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CustomWidth', ctypes.c_uint8, 2),
        ('Reserved2', ctypes.c_uint8, 6),
    ]


class REG_PHY_VDR_CUSTOM_WIDTH(ctypes.Union):
    value = 0
    offset = 0

    CustomWidth = 0         # bit 0 to 1
    Reserved2 = 0           # bit 2 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_VDR_CUSTOM_WIDTH),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_VDR_CUSTOM_WIDTH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_VDR_PRE_OVRD:
    TX1 = 0xD80
    TX2 = 0xD90


class _PHY_VDR_PRE_OVRD(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxEqPre', ctypes.c_uint8, 6),
        ('Reserved6_7', ctypes.c_uint8, 2)
    ]

class REG_PHY_VDR_PRE_OVRD(ctypes.Union):
    value = 0
    offset = 0

    TxEqPre = 0           # bit 0 to 5
    Reserved6_7 = 0       # bit 6 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_VDR_PRE_OVRD),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_VDR_PRE_OVRD, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_VDR_MAIN_OVRD:
    TX1 = 0xD81
    TX2 = 0xD91


class _PHY_VDR_MAIN_OVRD(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxEqMain', ctypes.c_uint8, 6),
        ('Reserved6_7', ctypes.c_uint8, 2)
    ]

class REG_PHY_VDR_MAIN_OVRD(ctypes.Union):
    value = 0
    offset = 0

    TxEqMain = 0          # bit 0 to 5
    Reserved6_7 = 0       # bit 6 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_VDR_MAIN_OVRD),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_VDR_MAIN_OVRD, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_VDR_POST_OVRD:
    TX1 = 0xD82
    TX2 = 0xD92


class _PHY_VDR_POST_OVRD(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxEqPost', ctypes.c_uint8, 6),
        ('Reserved6_7', ctypes.c_uint8, 2)
    ]

class REG_PHY_VDR_POST_OVRD(ctypes.Union):
    value = 0
    offset = 0

    TxEqPost = 0          # bit 0 to 5
    Reserved6_7 = 0       # bit 6 to 7

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_VDR_POST_OVRD),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_VDR_POST_OVRD, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


#####################################
class OFFSET_PHY_VDR_OVRD:
    offset = 0xD71


class _PHY_VDR_OVRD(ctypes.LittleEndianStructure):
    _fields_ = [
        ('bit0', ctypes.c_uint8, 1),
        ('Reserved1', ctypes.c_uint8, 1),
        ('bit2', ctypes.c_uint8, 1),
        ('Reserved3', ctypes.c_uint8, 1)
    ]

class REG_PHY_VDR_OVRD(ctypes.Union):
    value = 0
    offset = 0

    bit0 = 0        # bit 0
    Reserved1 = 0   # bit 1
    bit2 = 0        # bit 2
    Reserved3 = 0   # bit 3

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_VDR_OVRD),
        ('value', ctypes.c_uint8)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_VDR_OVRD, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value
