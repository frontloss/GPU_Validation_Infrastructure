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
# @file MtlPchInterruptRegs.py
# @brief contains MtlPchInterruptRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_DDIA_HPD_STATUS(Enum):
    DDIA_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDIA_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    DDIA_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    DDIA_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_DDIA_HPD_ENABLE(Enum):
    DDIA_HPD_DISABLE = 0x0
    DDIA_HPD_ENABLE = 0x1


class ENUM_DDIB_HPD_STATUS(Enum):
    DDIB_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDIB_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    DDIB_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    DDIB_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_DDIB_HPD_ENABLE(Enum):
    DDIB_HPD_DISABLE = 0x0
    DDIB_HPD_ENABLE = 0x1


class ENUM_DDIC_HPD_STATUS(Enum):
    DDIC_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDIC_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    DDIC_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    DDIC_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_DDIC_HPD_ENABLE(Enum):
    DDIC_HPD_DISABLE = 0x0
    DDIC_HPD_ENABLE = 0x1


class ENUM_DDID_HPD_STATUS(Enum):
    DDID_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDID_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    DDID_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    DDID_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_DDID_HPD_ENABLE(Enum):
    DDID_HPD_DISABLE = 0x0
    DDID_HPD_ENABLE = 0x1


class ENUM_DDIE_HPD_STATUS(Enum):
    DDIE_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDIE_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    DDIE_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    DDIE_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_DDIE_HPD_ENABLE(Enum):
    DDIE_HPD_DISABLE = 0x0
    DDIE_HPD_ENABLE = 0x1


class OFFSET_SHOTPLUG_CTL_DDI:
    SHOTPLUG_CTL_DDI = 0xC4030


class _SHOTPLUG_CTL_DDI(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiaHpdStatus', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('DdiaHpdEnable', ctypes.c_uint32, 1),
        ('DdibHpdStatus', ctypes.c_uint32, 2),
        ('Reserved6', ctypes.c_uint32, 1),
        ('DdibHpdEnable', ctypes.c_uint32, 1),
        ('DdicHpdStatus', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 1),
        ('DdicHpdEnable', ctypes.c_uint32, 1),
        ('DdidHpdStatus', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 1),
        ('DdidHpdEnable', ctypes.c_uint32, 1),
        ('DdieHpdStatus', ctypes.c_uint32, 2),
        ('Reserved18', ctypes.c_uint32, 1),
        ('DdieHpdEnable', ctypes.c_uint32, 1),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_SHOTPLUG_CTL_DDI(ctypes.Union):
    value = 0
    offset = 0

    DdiaHpdStatus = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    DdiaHpdEnable = 0  # bit 3 to 4
    DdibHpdStatus = 0  # bit 4 to 6
    Reserved6 = 0  # bit 6 to 7
    DdibHpdEnable = 0  # bit 7 to 8
    DdicHpdStatus = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 11
    DdicHpdEnable = 0  # bit 11 to 12
    DdidHpdStatus = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 15
    DdidHpdEnable = 0  # bit 15 to 16
    DdieHpdStatus = 0  # bit 16 to 18
    Reserved18 = 0  # bit 18 to 19
    DdieHpdEnable = 0  # bit 19 to 20
    Reserved20 = 0  # bit 20 to 32

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


class ENUM_TC1_HPD_ENABLE(Enum):
    TC1_HPD_DISABLE = 0x0
    TC1_HPD_ENABLE = 0x1


class ENUM_TC2_HPD_STATUS(Enum):
    TC2_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    TC2_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    TC2_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    TC2_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_TC2_HPD_ENABLE(Enum):
    TC2_HPD_DISABLE = 0x0
    TC2_HPD_ENABLE = 0x1


class ENUM_TC3_HPD_STATUS(Enum):
    TC3_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    TC3_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    TC3_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    TC3_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_TC3_HPD_ENABLE(Enum):
    TC3_HPD_DISABLE = 0x0
    TC3_HPD_ENABLE = 0x1


class ENUM_TC4_HPD_STATUS(Enum):
    TC4_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    TC4_HPD_STATUS_SHORT_PULSE_DETECTED = 0x1
    TC4_HPD_STATUS_LONG_PULSE_DETECTED = 0x2
    TC4_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED = 0x3


class ENUM_TC4_HPD_ENABLE(Enum):
    TC4_HPD_DISABLE = 0x0
    TC4_HPD_ENABLE = 0x1


class OFFSET_SHOTPLUG_CTL_TC:
    SHOTPLUG_CTL_TC = 0xC4034


class _SHOTPLUG_CTL_TC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Tc1HpdStatus', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('Tc1HpdEnable', ctypes.c_uint32, 1),
        ('Tc2HpdStatus', ctypes.c_uint32, 2),
        ('Reserved6', ctypes.c_uint32, 1),
        ('Tc2HpdEnable', ctypes.c_uint32, 1),
        ('Tc3HpdStatus', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 1),
        ('Tc3HpdEnable', ctypes.c_uint32, 1),
        ('Tc4HpdStatus', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 1),
        ('Tc4HpdEnable', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_SHOTPLUG_CTL_TC(ctypes.Union):
    value = 0
    offset = 0

    Tc1HpdStatus = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    Tc1HpdEnable = 0  # bit 3 to 4
    Tc2HpdStatus = 0  # bit 4 to 6
    Reserved6 = 0  # bit 6 to 7
    Tc2HpdEnable = 0  # bit 7 to 8
    Tc3HpdStatus = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 11
    Tc3HpdEnable = 0  # bit 11 to 12
    Tc4HpdStatus = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 15
    Tc4HpdEnable = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 24
    Reserved24 = 0  # bit 24 to 32

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
        ('Reserved3', ctypes.c_uint32, 5),
        ('ScdcTc1', ctypes.c_uint32, 1),
        ('ScdcTc2', ctypes.c_uint32, 1),
        ('ScdcTc3', ctypes.c_uint32, 1),
        ('ScdcTc4', ctypes.c_uint32, 1),
        ('ScdcTc5', ctypes.c_uint32, 1),
        ('ScdcTc6', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 2),
        ('HotplugDdia', ctypes.c_uint32, 1),
        ('HotplugDdib', ctypes.c_uint32, 1),
        ('HotplugDdic', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 4),
        ('Gmbus', ctypes.c_uint32, 1),
        ('HotplugTypecPort1', ctypes.c_uint32, 1),
        ('HotplugTypecPort2', ctypes.c_uint32, 1),
        ('HotplugTypecPort3', ctypes.c_uint32, 1),
        ('HotplugTypecPort4', ctypes.c_uint32, 1),
        ('HotplugTypecPort5', ctypes.c_uint32, 1),
        ('HotplugTypecPort6', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 1),
        ('PicaInterrupt', ctypes.c_uint32, 1),
    ]


class REG_SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION(ctypes.Union):
    value = 0
    offset = 0

    ScdcDdia = 0  # bit 0 to 1
    ScdcDdib = 0  # bit 1 to 2
    ScdcDdic = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 8
    ScdcTc1 = 0  # bit 8 to 9
    ScdcTc2 = 0  # bit 9 to 10
    ScdcTc3 = 0  # bit 10 to 11
    ScdcTc4 = 0  # bit 11 to 12
    ScdcTc5 = 0  # bit 12 to 13
    ScdcTc6 = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 16
    HotplugDdia = 0  # bit 16 to 17
    HotplugDdib = 0  # bit 17 to 18
    HotplugDdic = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 23
    Gmbus = 0  # bit 23 to 24
    HotplugTypecPort1 = 0  # bit 24 to 25
    HotplugTypecPort2 = 0  # bit 25 to 26
    HotplugTypecPort3 = 0  # bit 26 to 27
    HotplugTypecPort4 = 0  # bit 27 to 28
    HotplugTypecPort5 = 0  # bit 28 to 29
    HotplugTypecPort6 = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 31
    PicaInterrupt = 0  # bit 31 to 32

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

