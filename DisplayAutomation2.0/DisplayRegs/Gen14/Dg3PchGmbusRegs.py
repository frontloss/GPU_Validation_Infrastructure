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
# @file Dg3PchGmbusRegs.py
# @brief contains Dg3PchGmbusRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_PIN_PAIR_SELECT(Enum):
    PIN_PAIR_SELECT_NONE_DISABLED = 0x0
    PIN_PAIR_SELECT_PIN_PAIR_1 = 0x1
    PIN_PAIR_SELECT_PIN_PAIR_2 = 0x2
    PIN_PAIR_SELECT_PIN_PAIR_3 = 0x3
    PIN_PAIR_SELECT_PIN_PAIR_4 = 0x4
    PIN_PAIR_SELECT_PIN_PAIR_9 = 0x9


class ENUM_BYTE_COUNT_OVERRIDE(Enum):
    BYTE_COUNT_OVERRIDE_DISABLE = 0x0
    BYTE_COUNT_OVERRIDE_ENABLE = 0x1


class ENUM_GMBUS_RATE_SELECT(Enum):
    GMBUS_RATE_SELECT_100_KHZ = 0x0
    GMBUS_RATE_SELECT_50_KHZ = 0x1
    GMBUS_RATE_SELECT_TEST = 0x3


class ENUM_AKSV_SELECT(Enum):
    AKSV_SELECT_USE_GMBUS = 0x0  # Use the GMBUS data buffer (GMBUS3) for data transmission
    AKSV_SELECT_USE_HDCP = 0x1  # Use HDCP internal Aksv for data transmission


class OFFSET_GMBUS0:
    GMBUS0 = 0xC5100
    GMBUS0 = 0xC5100


class _GMBUS0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PinPairSelect', ctypes.c_uint32, 5),
        ('Reserved5', ctypes.c_uint32, 1),
        ('ByteCountOverride', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 1),
        ('GmbusRateSelect', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 1),
        ('AksvSelect', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 2),
        ('ClockStopDisable', ctypes.c_uint32, 1),
        ('HoldtimeSelect', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_GMBUS0(ctypes.Union):
    value = 0
    offset = 0

    PinPairSelect = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 6
    ByteCountOverride = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 8
    GmbusRateSelect = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 11
    AksvSelect = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 14
    ClockStopDisable = 0  # bit 14 to 15
    HoldtimeSelect = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GMBUS0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GMBUS0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GPIO_CLOCK_DIRECTION_MASK(Enum):
    GPIO_CLOCK_DIRECTION_MASK_DOT_NOT_WRITE = 0x0
    GPIO_CLOCK_DIRECTION_MASK_WRITE = 0x1


class ENUM_GPIO_CLOCK_DIRECTION_VALUE(Enum):
    GPIO_CLOCK_DIRECTION_VALUE_INPUT = 0x0
    GPIO_CLOCK_DIRECTION_VALUE_OUTPUT = 0x1


class ENUM_GPIO_CLOCK_DATA_MASK(Enum):
    GPIO_CLOCK_DATA_MASK_DOT_NOT_WRITE = 0x0
    GPIO_CLOCK_DATA_MASK_WRITE = 0x1


class ENUM_GPIO_CLOCK_DATA_IN(Enum):
    GPIO_CLOCK_DATA_IN_UNDEFINED_READ_ONLY_DEPENDS_ON_I_O_PIN = 0x0


class ENUM_GPIO_DATA_DIRECTION_MASK(Enum):
    GPIO_DATA_DIRECTION_MASK_DOT_NOT_WRITE = 0x0
    GPIO_DATA_DIRECTION_MASK_WRITE = 0x1


class ENUM_GPIO_DATA_DIRECTION_VALUE(Enum):
    GPIO_DATA_DIRECTION_VALUE_INPUT = 0x0
    GPIO_DATA_DIRECTION_VALUE_OUTPUT = 0x1


class ENUM_GPIO_DATA_MASK(Enum):
    GPIO_DATA_MASK_DOT_NOT_WRITE = 0x0
    GPIO_DATA_MASK_WRITE = 0x1


class ENUM_GPIO_DATA_IN(Enum):
    GPIO_DATA_IN_UNDEFINED_READ_ONLY_DEPENDS_ON_I_O_PIN = 0x0


class OFFSET_GPIO_CTL:
    GPIO_CTL_1 = 0xC5014
    GPIO_CTL_1 = 0xC5014
    GPIO_CTL_2 = 0xC5018
    GPIO_CTL_2 = 0xC5018
    GPIO_CTL_3 = 0xC501C
    GPIO_CTL_3 = 0xC501C
    GPIO_CTL_4 = 0xC5020
    GPIO_CTL_4 = 0xC5020
    GPIO_CTL_5 = 0xC5024
    GPIO_CTL_9 = 0xC5034
    GPIO_CTL_9 = 0xC5034
    GPIO_CTL_10 = 0xC5038
    GPIO_CTL_11 = 0xC503C
    GPIO_CTL_12 = 0xC5040
    GPIO_CTL_13 = 0xC5044
    GPIO_CTL_14 = 0xC5048


class _GPIO_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GpioClockDirectionMask', ctypes.c_uint32, 1),
        ('GpioClockDirectionValue', ctypes.c_uint32, 1),
        ('GpioClockDataMask', ctypes.c_uint32, 1),
        ('GpioClockDataValue', ctypes.c_uint32, 1),
        ('GpioClockDataIn', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 3),
        ('GpioDataDirectionMask', ctypes.c_uint32, 1),
        ('GpioDataDirectionValue', ctypes.c_uint32, 1),
        ('GpioDataMask', ctypes.c_uint32, 1),
        ('GpioDataValue', ctypes.c_uint32, 1),
        ('GpioDataIn', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_GPIO_CTL(ctypes.Union):
    value = 0
    offset = 0

    GpioClockDirectionMask = 0  # bit 0 to 1
    GpioClockDirectionValue = 0  # bit 1 to 2
    GpioClockDataMask = 0  # bit 2 to 3
    GpioClockDataValue = 0  # bit 3 to 4
    GpioClockDataIn = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 8
    GpioDataDirectionMask = 0  # bit 8 to 9
    GpioDataDirectionValue = 0  # bit 9 to 10
    GpioDataMask = 0  # bit 10 to 11
    GpioDataValue = 0  # bit 11 to 12
    GpioDataIn = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GPIO_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GPIO_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

