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
# @file Gen14NonAutoGenRegs.py
# @brief contains Non Auto Generated register definitions for Gen 14

import ctypes
from enum import Enum


class OFFSET_DDI_CLK_VALFREQ:
    DDI_CLK_VALFREQ_A = 0X64030
    DDI_CLK_VALFREQ_B = 0X64130
    DDI_CLK_VALFREQ_USB1 = 0X64330
    DDI_CLK_VALFREQ_USB2 = 0X64430
    DDI_CLK_VALFREQ_USB3 = 0X64530
    DDI_CLK_VALFREQ_USB4 = 0X64630


class _DDI_CLK_VALFREQ(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiValidationFrequency', ctypes.c_uint32, 32),
    ]


class REG_DDI_CLK_VALFREQ(ctypes.Union):
    value = 0
    offset = 0

    DdiValidationFrequency = 0 #  Bit 0 to 31



    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DDI_CLK_VALFREQ),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DDI_CLK_VALFREQ, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_M2P_MSGBUS_CTL:
    PORT_M2P_MSGBUS_CTL_LN0_A = 0x64040
    PORT_M2P_MSGBUS_CTL_LN0_B = 0x64140
    PORT_M2P_MSGBUS_CTL_LN0_USBC1 = 0x16F240
    PORT_M2P_MSGBUS_CTL_LN0_USBC2 = 0x16F440
    PORT_M2P_MSGBUS_CTL_LN0_USBC3 = 0x16F640
    PORT_M2P_MSGBUS_CTL_LN0_USBC4 = 0x16F840

    PORT_M2P_MSGBUS_CTL_LN1_A = 0x64044
    PORT_M2P_MSGBUS_CTL_LN1_B = 0x64144
    PORT_M2P_MSGBUS_CTL_LN1_USBC1 = 0x16F244
    PORT_M2P_MSGBUS_CTL_LN1_USBC2 = 0x16F444
    PORT_M2P_MSGBUS_CTL_LN1_USBC3 = 0x16F644
    PORT_M2P_MSGBUS_CTL_LN1_USBC4 = 0x16F844


class _PORT_M2P_MSGBUS_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Address',             ctypes.c_uint32, 12),   # 0 to 11
        ('Reserved12',          ctypes.c_uint32, 3),    # 12 to 14
        ('ResetMessageBus',     ctypes.c_uint32, 1),    # 15 to 15
        ('Data',                ctypes.c_uint32, 8),    # 16 to 23
        ('Reserved24',          ctypes.c_uint32, 3),    # 24 to 26
        ('CommandType',         ctypes.c_uint32, 4),    # 27 to 30
        ('TransactionPending',  ctypes.c_uint32, 1),    # 31 to 31
    ]


class REG_PORT_M2P_MSGBUS_CTL(ctypes.Union):
    value = 0
    offset = 0

    Address = 0  # 0 to 11
    Reserved12 = 0  # 12 to 14
    ResetMessageBus = 0  # 15 to 15
    Data = 0  # 16 to 23
    Reserved24 = 0  # 24 to 26
    CommandType = 0  # 27 to 30
    TransactionPending = 0  # 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_M2P_MSGBUS_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_M2P_MSGBUS_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_P2M_MSGBUS_STATUS:
    PORT_P2M_MSGBUS_STATUS_LN0_A = 0x64048
    PORT_P2M_MSGBUS_STATUS_LN0_B = 0x64148
    PORT_P2M_MSGBUS_STATUS_LN0_USBC1 = 0x16F248
    PORT_P2M_MSGBUS_STATUS_LN0_USBC2 = 0x16F448
    PORT_P2M_MSGBUS_STATUS_LN0_USBC3 = 0x16F648
    PORT_P2M_MSGBUS_STATUS_LN0_USBC4 = 0x16F848

    PORT_P2M_MSGBUS_STATUS_LN1_A = 0x6404C
    PORT_P2M_MSGBUS_STATUS_LN1_B = 0x6414C
    PORT_P2M_MSGBUS_STATUS_LN1_USBC1 = 0x16F24C
    PORT_P2M_MSGBUS_STATUS_LN1_USBC2 = 0x16F44C
    PORT_P2M_MSGBUS_STATUS_LN1_USBC3 = 0x16F64C
    PORT_P2M_MSGBUS_STATUS_LN1_USBC4 = 0x16F84C


class _PORT_P2M_MSGBUS_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0',          ctypes.c_uint32, 15),    # 0 to 14
        ('ErrorSet',            ctypes.c_uint32, 1),    # 15 to 15
        ('Data',                ctypes.c_uint32, 8),    # 16 to 23
        ('Reserved24',          ctypes.c_uint32, 3),    # 24 to 26
        ('CommandType',         ctypes.c_uint32, 4),    # 27 to 30
        ('ResponseReady',       ctypes.c_uint32, 1),    # 31 to 31
    ]


class REG_PORT_P2M_MSGBUS_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # 0 to 14
    ErrorSet = 0  # 15 to 15
    Data = 0  # 16 to 23
    Reserved24 = 0  # 24 to 26
    CommandType = 0  # 27 to 30
    ResponseReady = 0  # 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_P2M_MSGBUS_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_P2M_MSGBUS_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_GENLOCK_PLL_ENABLE:
    GENLOCK_PLL_ENABLE = 0x46020


class _GENLOCK_PLL_ENABLE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0',           ctypes.c_uint32, 30),    # 0 to 29
        ('PllLock',             ctypes.c_uint32, 1),    # 30 to 30
        ('PllEnable',           ctypes.c_uint32, 1),    # 31 to 31
    ]


class REG_GENLOCK_PLL_ENABLE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # 0 to 29
    PllLock = 0  # 30 to 30
    PllEnable = 0  # 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GENLOCK_PLL_ENABLE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GENLOCK_PLL_ENABLE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SPIN_MISC_CTL:
    SPIN_MISC_CTL = 0xC2040


class _SPIN_MISC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GenlockBoardDirectionPinEnable',      ctypes.c_uint32, 1),  # 0 to 0
        ('GenlockBoardDirectionPinData',        ctypes.c_uint32, 1),  # 1 to 1
        ('GenlockBoardEnablePinEnable',         ctypes.c_uint32, 1),  # 2 to 2
        ('GenlockBoardEnablePinData',           ctypes.c_uint32, 1),  # 3 to 3
        ('Reserved4',                           ctypes.c_uint32, 4),  # 4 to 7
        ('Misc1PinOutputEnable',                ctypes.c_uint32, 1),  # 8 to 8
        ('Misc1PinOutputData',                  ctypes.c_uint32, 1),  # 9 to 9
        ('Misc2PinOutputEnable',                ctypes.c_uint32, 1),  # 10 to 10
        ('Misc2PinOutputData',                  ctypes.c_uint32, 1),  # 11 to 11
        ('Misc3PinOutputEnable',                ctypes.c_uint32, 1),  # 12 to 12
        ('Misc3PinOutputData',                  ctypes.c_uint32, 1),  # 13 to 13
        ('Misc4PinOutputEnable',                ctypes.c_uint32, 1),  # 14 to 14
        ('Misc4PinOutputData',                  ctypes.c_uint32, 1),  # 15 to 15
        ('Reserved16',                          ctypes.c_uint32, 30),  # 16 to 31
    ]


class REG_SPIN_MISC_CTL(ctypes.Union):
    value = 0
    offset = 0

    GenlockBoardDirectionPinEnable = 0  # 0 to 0
    GenlockBoardDirectionPinData = 0  # 1 to 1
    GenlockBoardEnablePinEnable = 0  # 2 to 2
    GenlockBoardEnablePinData = 0  # 3 to 3
    Reserved4 = 0  # 4 to 7
    Misc1PinOutputEnable = 0  # 8 to 8
    Misc1PinOutputData = 0  # 9 to 9
    Misc2PinOutputEnable = 0  # 10 to 10
    Misc2PinOutputData = 0  # 11 to 11
    Misc3PinOutputEnable = 0  # 12 to 12
    Misc3PinOutputData = 0  # 13 to 13
    Misc4PinOutputEnable = 0  # 14 to 14
    Misc4PinOutputData = 0  # 15 to 15
    Reserved16 = 0  # 16 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SPIN_MISC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SPIN_MISC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value
