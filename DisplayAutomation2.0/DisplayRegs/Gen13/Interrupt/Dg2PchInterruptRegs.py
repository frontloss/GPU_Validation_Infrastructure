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
# @file Dg2PchInterruptRegs.py
# @brief contains Dg2PchInterruptRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_DDIA_HPD_STATUS(Enum):
    DDIA_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDIA_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    DDIA_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    DDIA_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_DDIA_HPD_OUTPUT_DATA(Enum):
    DDIA_HPD_OUTPUT_DATA_DRIVE_0 = 0x0
    DDIA_HPD_OUTPUT_DATA_DRIVE_1 = 0x1


class ENUM_DDIA_HPD_ENABLE(Enum):
    DDIA_HPD_DISABLE = 0x0
    DDIA_HPD_ENABLE = 0x1


class ENUM_DDIB_HPD_STATUS(Enum):
    DDIB_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDIB_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    DDIB_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    DDIB_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_DDIB_HPD_OUTPUT_DATA(Enum):
    DDIB_HPD_OUTPUT_DATA_DRIVE_0 = 0x0
    DDIB_HPD_OUTPUT_DATA_DRIVE_1 = 0x1


class ENUM_DDIB_HPD_ENABLE(Enum):
    DDIB_HPD_DISABLE = 0x0
    DDIB_HPD_ENABLE = 0x1


class ENUM_DDIC_HPD_STATUS(Enum):
    DDIC_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDIC_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    DDIC_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    DDIC_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_DDIC_HPD_OUTPUT_DATA(Enum):
    DDIC_HPD_OUTPUT_DATA_DRIVE_0 = 0x0
    DDIC_HPD_OUTPUT_DATA_DRIVE_1 = 0x1


class ENUM_DDIC_HPD_ENABLE(Enum):
    DDIC_HPD_DISABLE = 0x0
    DDIC_HPD_ENABLE = 0x1


class ENUM_DDID_HPD_STATUS(Enum):
    DDID_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDID_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    DDID_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    DDID_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_DDID_HPD_OUTPUT_DATA(Enum):
    DDID_HPD_OUTPUT_DATA_DRIVE_0 = 0x0
    DDID_HPD_OUTPUT_DATA_DRIVE_1 = 0x1


class ENUM_DDID_HPD_ENABLE(Enum):
    DDID_HPD_DISABLE = 0x0
    DDID_HPD_ENABLE = 0x1


class OFFSET_SHOTPLUG_CTL_DDI:
    SHOTPLUG_CTL_DDI = 0xC4030


class _SHOTPLUG_CTL_DDI(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiaHpdStatus', ctypes.c_uint32, 2),
        ('DdiaHpdOutputData', ctypes.c_uint32, 1),
        ('DdiaHpdEnable', ctypes.c_uint32, 1),
        ('DdibHpdStatus', ctypes.c_uint32, 2),
        ('DdibHpdOutputData', ctypes.c_uint32, 1),
        ('DdibHpdEnable', ctypes.c_uint32, 1),
        ('DdicHpdStatus', ctypes.c_uint32, 2),
        ('DdicHpdOutputData', ctypes.c_uint32, 1),
        ('DdicHpdEnable', ctypes.c_uint32, 1),
        ('DdidHpdStatus', ctypes.c_uint32, 2),
        ('DdidHpdOutputData', ctypes.c_uint32, 1),
        ('DdidHpdEnable', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_SHOTPLUG_CTL_DDI(ctypes.Union):
    value = 0
    offset = 0

    DdiaHpdStatus = 0  # bit 0 to 2
    DdiaHpdOutputData = 0  # bit 2 to 3
    DdiaHpdEnable = 0  # bit 3 to 4
    DdibHpdStatus = 0  # bit 4 to 6
    DdibHpdOutputData = 0  # bit 6 to 7
    DdibHpdEnable = 0  # bit 7 to 8
    DdicHpdStatus = 0  # bit 8 to 10
    DdicHpdOutputData = 0  # bit 10 to 11
    DdicHpdEnable = 0  # bit 11 to 12
    DdidHpdStatus = 0  # bit 12 to 14
    DdidHpdOutputData = 0  # bit 14 to 15
    DdidHpdEnable = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SHOTPLUG_CTL_DDI),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SHOTPLUG_CTL_DDI, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TC1_HPD_STATUS(Enum):
    TC1_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    TC1_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    TC1_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    TC1_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_TC1_HPD_OUTPUT_DATA(Enum):
    TC1_HPD_OUTPUT_DATA_DRIVE_0 = 0x0
    TC1_HPD_OUTPUT_DATA_DRIVE_1 = 0x1


class ENUM_TC1_HPD_ENABLE(Enum):
    TC1_HPD_DISABLE = 0x0
    TC1_HPD_ENABLE = 0x1


class OFFSET_SHOTPLUG_CTL_TC:
    SHOTPLUG_CTL_TC = 0xC4034


class _SHOTPLUG_CTL_TC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Tc1HpdStatus', ctypes.c_uint32, 2),
        ('Tc1HpdOutputData', ctypes.c_uint32, 1),
        ('Tc1HpdEnable', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 28),
    ]


class REG_SHOTPLUG_CTL_TC(ctypes.Union):
    value = 0
    offset = 0

    Tc1HpdStatus = 0  # bit 0 to 2
    Tc1HpdOutputData = 0  # bit 2 to 3
    Tc1HpdEnable = 0  # bit 3 to 4
    Reserved4 = 0  # bit 4 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SHOTPLUG_CTL_TC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SHOTPLUG_CTL_TC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SHORTPULSE_COUNT(Enum):
    SHORTPULSE_COUNT_2_000_MICROSECONDS_FOR_DISPLAYPORT = 0x7CE
    SHORTPULSE_COUNT_100_000_MICROSECONDS_FOR_HDMI_OR_DVI = 0x1869E


class OFFSET_SHPD_PULSE_CNT:
    SHPD_PULSE_CNT_DDIA = 0xC4050
    SHPD_PULSE_CNT_DDIB = 0xC4054
    SHPD_PULSE_CNT_DDIC = 0xC4058
    SHPD_PULSE_CNT_DDID = 0xC405C
    SHPD_PULSE_CNT_TC1 = 0xC4070


class _SHPD_PULSE_CNT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ShortpulseCount', ctypes.c_uint32, 17),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_SHPD_PULSE_CNT(ctypes.Union):
    value = 0
    offset = 0

    ShortpulseCount = 0  # bit 0 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SHPD_PULSE_CNT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SHPD_PULSE_CNT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_HPD_FILTER_COUNT(Enum):
    HPD_FILTER_COUNT_500_MICROSECONDS = 0x1F2


class OFFSET_SHPD_FILTER_CNT:
    SHPD_FILTER_CNT = 0xC4038


class _SHPD_FILTER_CNT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HpdFilterCount', ctypes.c_uint32, 17),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_SHPD_FILTER_CNT(ctypes.Union):
    value = 0
    offset = 0

    HpdFilterCount = 0  # bit 0 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SHPD_FILTER_CNT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SHPD_FILTER_CNT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION:
    SDE_INTERRUPT_0 = 0xC4000
    SDE_INTERRUPT_1 = 0xC4004
    SDE_INTERRUPT_2 = 0xC4008
    SDE_INTERRUPT_3 = 0xC400C


class _SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ScdcDdia', ctypes.c_uint32, 1),
        ('ScdcDdib', ctypes.c_uint32, 1),
        ('ScdcDdic', ctypes.c_uint32, 1),
        ('ScdcDdid', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 5),
        ('ScdcTypecPort1', ctypes.c_uint32, 1),
        ('Reserved10', ctypes.c_uint32, 6),
        ('HotplugDdia', ctypes.c_uint32, 1),
        ('HotplugDdib', ctypes.c_uint32, 1),
        ('HotplugDdic', ctypes.c_uint32, 1),
        ('HotplugDdid', ctypes.c_uint32, 1),
        ('Reserved20', ctypes.c_uint32, 3),
        ('Gmbus', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 1),
        ('HotplugTypecPort1', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 5),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION(ctypes.Union):
    value = 0
    offset = 0

    ScdcDdia = 0  # bit 0 to 1
    ScdcDdib = 0  # bit 1 to 2
    ScdcDdic = 0  # bit 2 to 3
    ScdcDdid = 0  # bit 3 to 4
    Reserved4 = 0  # bit 4 to 9
    ScdcTypecPort1 = 0  # bit 9 to 10
    Reserved10 = 0  # bit 10 to 16
    HotplugDdia = 0  # bit 16 to 17
    HotplugDdib = 0  # bit 17 to 18
    HotplugDdic = 0  # bit 18 to 19
    HotplugDdid = 0  # bit 19 to 20
    Reserved20 = 0  # bit 20 to 23
    Gmbus = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 25
    HotplugTypecPort1 = 0  # bit 25 to 26
    Reserved26 = 0  # bit 26 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

