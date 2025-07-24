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
# @file CmpPchInterruptRegs.py
# @brief contains CmpPchInterruptRegs.py related register definitions

import ctypes
from enum import Enum


class OFFSET_SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION:
    SDE_INTERRUPT_0 = 0xC4000
    SDE_INTERRUPT_1 = 0xC4004
    SDE_INTERRUPT_2 = 0xC4008
    SDE_INTERRUPT_3 = 0xC400C


class _SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 7),
        ('Reserved7', ctypes.c_uint32, 1),
        ('ScdcReadRequestInterruptPortB', ctypes.c_uint32, 1),
        ('ScdcReadRequestInterruptPortC', ctypes.c_uint32, 1),
        ('ScdcReadRequestInterruptPortD', ctypes.c_uint32, 1),
        ('ScdcReadRequestInterruptPortF', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 5),
        ('Gmbus', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 3),
        ('DdiBHotplug', ctypes.c_uint32, 1),
        ('DdiCHotplug', ctypes.c_uint32, 1),
        ('DdiDHotplug', ctypes.c_uint32, 1),
        ('DdiAHotplug', ctypes.c_uint32, 1),
        ('DdiEHotplug', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 5),
    ]


class REG_SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 7
    Reserved7 = 0  # bit 7 to 8
    ScdcReadRequestInterruptPortB = 0  # bit 8 to 9
    ScdcReadRequestInterruptPortC = 0  # bit 9 to 10
    ScdcReadRequestInterruptPortD = 0  # bit 10 to 11
    ScdcReadRequestInterruptPortF = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 17
    Gmbus = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 21
    DdiBHotplug = 0  # bit 21 to 22
    DdiCHotplug = 0  # bit 22 to 23
    DdiDHotplug = 0  # bit 23 to 24
    DdiAHotplug = 0  # bit 24 to 25
    DdiEHotplug = 0  # bit 25 to 26
    Reserved26 = 0  # bit 26 to 27
    Reserved27 = 0  # bit 27 to 32

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


class ENUM_DDI_B_HPD_STATUS(Enum):
    DDI_B_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDI_B_HPD_STATUS_SHORT_PULSE_HOT_PLUG_EVENT_DETECTED = 0x0
    DDI_B_HPD_STATUS_LONG_PULSE_HOT_PLUG_EVENT_DETECTED = 0x0


class ENUM_DDI_B_HPD_OUTPUT_DATA(Enum):
    DDI_B_HPD_OUTPUT_DATA_DRIVE_0 = 0x0
    DDI_B_HPD_OUTPUT_DATA_DRIVE_1 = 0x1


class ENUM_DDI_B_HPD_INPUT_ENABLE(Enum):
    DDI_B_HPD_INPUT_DISABLE = 0x0
    DDI_B_HPD_INPUT_ENABLE = 0x1


class ENUM_DDI_C_HPD_STATUS(Enum):
    DDI_C_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDI_C_HPD_STATUS_SHORT_PULSE_HOT_PLUG_EVENT_DETECTED = 0x0
    DDI_C_HPD_STATUS_LONG_PULSE_HOT_PLUG_EVENT_DETECTED = 0x0


class ENUM_DDI_C_HPD_OUTPUT_DATA(Enum):
    DDI_C_HPD_OUTPUT_DATA_DRIVE_0 = 0x0
    DDI_C_HPD_OUTPUT_DATA_DRIVE_1 = 0x1


class ENUM_DDI_C_HPD_INPUT_ENABLE(Enum):
    DDI_C_HPD_INPUT_DISABLE = 0x0
    DDI_C_HPD_INPUT_ENABLE = 0x1


class ENUM_DDI_D_HPD_STATUS(Enum):
    DDI_D_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDI_D_HPD_STATUS_SHORT_PULSE_HOT_PLUG_EVENT_DETECTED = 0x0
    DDI_D_HPD_STATUS_LONG_PULSE_HOT_PLUG_EVENT_DETECTED = 0x0


class ENUM_DDI_D_HPD_OUTPUT_DATA(Enum):
    DDI_D_HPD_OUTPUT_DATA_DRIVE_0 = 0x0
    DDI_D_HPD_OUTPUT_DATA_DRIVE_1 = 0x1


class ENUM_DDI_D_HPD_INPUT_ENABLE(Enum):
    DDI_D_HPD_INPUT_DISABLE = 0x0
    DDI_D_HPD_INPUT_ENABLE = 0x1


class ENUM_DDI_A_HPD_STATUS(Enum):
    DDI_A_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDI_A_HPD_STATUS_SHORT_PULSE_HOT_PLUG_EVENT_DETECTED = 0x0
    DDI_A_HPD_STATUS_LONG_PULSE_HOT_PLUG_EVENT_DETECTED = 0x0


class ENUM_DDI_A_HPD_OUTPUT_DATA(Enum):
    DDI_A_HPD_OUTPUT_DATA_DRIVE_0 = 0x0
    DDI_A_HPD_OUTPUT_DATA_DRIVE_1 = 0x1


class ENUM_DDI_A_HPD_INPUT_ENABLE(Enum):
    DDI_A_HPD_INPUT_DISABLE = 0x0
    DDI_A_HPD_INPUT_ENABLE = 0x1


class OFFSET_SHOTPLUG_CTL:
    SHOTPLUG_CTL = 0xC4030


class _SHOTPLUG_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiBHpdStatus', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('DdiBHpdOutputData', ctypes.c_uint32, 1),
        ('DdiBHpdInputEnable', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 3),
        ('DdiCHpdStatus', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 1),
        ('DdiCHpdOutputData', ctypes.c_uint32, 1),
        ('DdiCHpdInputEnable', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 3),
        ('DdiDHpdStatus', ctypes.c_uint32, 2),
        ('Reserved18', ctypes.c_uint32, 1),
        ('DdiDHpdOutputData', ctypes.c_uint32, 1),
        ('DdiDHpdInputEnable', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 3),
        ('DdiAHpdStatus', ctypes.c_uint32, 2),
        ('Reserved26', ctypes.c_uint32, 1),
        ('DdiAHpdOutputData', ctypes.c_uint32, 1),
        ('DdiAHpdInputEnable', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_SHOTPLUG_CTL(ctypes.Union):
    value = 0
    offset = 0

    DdiBHpdStatus = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    DdiBHpdOutputData = 0  # bit 3 to 4
    DdiBHpdInputEnable = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 8
    DdiCHpdStatus = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 11
    DdiCHpdOutputData = 0  # bit 11 to 12
    DdiCHpdInputEnable = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 16
    DdiDHpdStatus = 0  # bit 16 to 18
    Reserved18 = 0  # bit 18 to 19
    DdiDHpdOutputData = 0  # bit 19 to 20
    DdiDHpdInputEnable = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 24
    DdiAHpdStatus = 0  # bit 24 to 26
    Reserved26 = 0  # bit 26 to 27
    DdiAHpdOutputData = 0  # bit 27 to 28
    DdiAHpdInputEnable = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SHOTPLUG_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SHOTPLUG_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DDI_E_HPD_STATUS(Enum):
    DDI_E_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED = 0x0
    DDI_E_HPD_STATUS_SHORT_PULSE_HOT_PLUG_EVENT_DETECTED = 0x0
    DDI_E_HPD_STATUS_LONG_PULSE_HOT_PLUG_EVENT_DETECTED = 0x0


class ENUM_DDI_E_HPD_OUTPUT_DATA(Enum):
    DDI_E_HPD_OUTPUT_DATA_DRIVE_0 = 0x0
    DDI_E_HPD_OUTPUT_DATA_DRIVE_1 = 0x1


class ENUM_DDI_E_HPD_INPUT_ENABLE(Enum):
    DDI_E_HPD_INPUT_DISABLE = 0x0
    DDI_E_HPD_INPUT_ENABLE = 0x1


class OFFSET_SHOTPLUG_CTL2:
    SHOTPLUG_CTL2 = 0xC403C


class _SHOTPLUG_CTL2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiEHpdStatus', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('DdiEHpdOutputData', ctypes.c_uint32, 1),
        ('DdiEHpdInputEnable', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 4),
        ('Reserved9', ctypes.c_uint32, 23),
    ]


class REG_SHOTPLUG_CTL2(ctypes.Union):
    value = 0
    offset = 0

    DdiEHpdStatus = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    DdiEHpdOutputData = 0  # bit 3 to 4
    DdiEHpdInputEnable = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 9
    Reserved9 = 0  # bit 9 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SHOTPLUG_CTL2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SHOTPLUG_CTL2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

