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
# @file Dg1PchRegs.py
# @brief contains Dg1PchRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_GENLOCK_DIRECTION_ENABLE_PIN_VALUE(Enum):
    GENLOCK_DIRECTION_ENABLE_PIN_VALUE_ENABLE_MOTHERBOARD_GENLOCK_CIRCUIT = 0x1
    GENLOCK_DIRECTION_ENABLE_PIN_VALUE_DISABLE_MOTHERBOARD_GENLOCK_CIRCUIT = 0x0


class ENUM_GENLOCK_DIRECTION_SELECT_PIN_VALUE(Enum):
    GENLOCK_DIRECTION_SELECT_PIN_VALUE_GENLOCK_SLAVE = 0x1
    GENLOCK_DIRECTION_SELECT_PIN_VALUE_GENLOCK_MASTER = 0x0


class ENUM_GENLOCK_DIRECTION_IO_SELECT(Enum):
    GENLOCK_DIRECTION_IO_SELECT_GENLOCK = 0x1
    GENLOCK_DIRECTION_IO_SELECT_BACKLIGHT = 0x0


class ENUM_BACKLIGHT_POLARITY(Enum):
    BACKLIGHT_POLARITY_ACTIVE_HIGH = 0x0
    BACKLIGHT_POLARITY_ACTIVE_LOW = 0x1


class ENUM_PWM_ENABLE(Enum):
    PWM_DISABLE = 0x0
    PWM_ENABLE = 0x1


class OFFSET_SBLC_PWM_CTL1:
    SBLC_PWM_CTL1 = 0xC8250


class _SBLC_PWM_CTL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GenlockDirectionEnablePinValue', ctypes.c_uint32, 1),
        ('GenlockDirectionSelectPinValue', ctypes.c_uint32, 1),
        ('GenlockDirectionIoSelect', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 26),
        ('BacklightPolarity', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 1),
        ('PwmEnable', ctypes.c_uint32, 1),
    ]


class REG_SBLC_PWM_CTL1(ctypes.Union):
    value = 0
    offset = 0

    GenlockDirectionEnablePinValue = 0  # bit 0 to 1
    GenlockDirectionSelectPinValue = 0  # bit 1 to 2
    GenlockDirectionIoSelect = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 29
    BacklightPolarity = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 31
    PwmEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SBLC_PWM_CTL1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SBLC_PWM_CTL1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_MICROSECOND_COUNTER_FRACTION_NUMERATOR(Enum):
    MICROSECOND_COUNTER_FRACTION_NUMERATOR_0 = 0x0  # No fraction
    MICROSECOND_COUNTER_FRACTION_NUMERATOR_1 = 0x1  # Numerator 1
    MICROSECOND_COUNTER_FRACTION_NUMERATOR_2 = 0x2  # Numerator 2


class ENUM_MICROSECOND_COUNTER_DIVIDER(Enum):
    MICROSECOND_COUNTER_DIVIDER_38_MHZ = 0x25


class ENUM_MICROSECOND_COUNTER_FRACTION_DENOMINATOR(Enum):
    MICROSECOND_COUNTER_FRACTION_DENOMINATOR_5 = 0x4  # Denominator 5
    MICROSECOND_COUNTER_FRACTION_DENOMINATOR_0 = 0x0  # No fraction


class ENUM_MICROSECOND_COUNTER_HOLD(Enum):
    MICROSECOND_COUNTER_HOLD_HOLD = 0x1  # Test - Hold the microsecond counter in a reset state
    MICROSECOND_COUNTER_HOLD_RUN = 0x0  # Let the microsecond counter run


class OFFSET_RAWCLK_FREQ:
    RAWCLK_FREQ = 0xC6204


class _RAWCLK_FREQ(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 11),
        ('MicrosecondCounterFractionNumerator', ctypes.c_uint32, 3),
        ('Reserved14', ctypes.c_uint32, 2),
        ('MicrosecondCounterDivider', ctypes.c_uint32, 10),
        ('MicrosecondCounterFractionDenominator', ctypes.c_uint32, 4),
        ('Reserved30', ctypes.c_uint32, 1),
        ('MicrosecondCounterHold', ctypes.c_uint32, 1),
    ]


class REG_RAWCLK_FREQ(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 11
    MicrosecondCounterFractionNumerator = 0  # bit 11 to 14
    Reserved14 = 0  # bit 14 to 16
    MicrosecondCounterDivider = 0  # bit 16 to 26
    MicrosecondCounterFractionDenominator = 0  # bit 26 to 30
    Reserved30 = 0  # bit 30 to 31
    MicrosecondCounterHold = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _RAWCLK_FREQ),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_RAWCLK_FREQ, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PPS_IDLE(Enum):
    PPS_IDLE_IMPROVED_PPS_IDLE_DETECTION = 0x1
    PPS_IDLE_ORIGINAL_PPS_IDLE_DETECTION = 0x0


class ENUM_PPS_LOAD_FIX_DISABLE(Enum):
    PPS_LOAD_FIX_DISABLE_FIX_FOR_PPS_DELAY_LOADING = 0x1
    PPS_LOAD_FIX_ENABLE_FIX_FOR_PPS_DELAY_LOADING = 0x0


class ENUM_FORCE_PPS_IDLE(Enum):
    FORCE_PPS_IDLE_FORCE_IDLE = 0x1
    FORCE_PPS_IDLE_AUTOMATIC_IDLE = 0x0


class ENUM_CHASSIS_CLOCK_REQUEST_DURATION(Enum):
    CHASSIS_CLOCK_REQUEST_DURATION_13_CLOCKS = 0x9


class ENUM_INVERT_DDIA_HPD(Enum):
    INVERT_DDIA_HPD_INVERT = 0x1
    INVERT_DDIA_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_DDIB_HPD(Enum):
    INVERT_DDIB_HPD_INVERT = 0x1
    INVERT_DDIB_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_DDIC_HPD(Enum):
    INVERT_DDIC_HPD_INVERT = 0x1
    INVERT_DDIC_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_DDID_HPD(Enum):
    INVERT_DDID_HPD_INVERT = 0x1
    INVERT_DDID_HPD_DO_NOT_INVERT = 0x0


class ENUM_WAKE_PIN_VALUE_OVERRIDE(Enum):
    WAKE_PIN_VALUE_OVERRIDE_OVERRIDE_TO_0 = 0x2
    WAKE_PIN_VALUE_OVERRIDE_OVERRIDE_TO_1 = 0x3


class ENUM_WAKE_PIN_ENABLE_OVERRIDE(Enum):
    WAKE_PIN_ENABLE_OVERRIDE_OVERRIDE_TO_DISABLE = 0x2
    WAKE_PIN_ENABLE_OVERRIDE_OVERRIDE_TO_ENABLE = 0x3


class OFFSET_SCHICKEN_1:
    SCHICKEN_1 = 0xC2000


class _SCHICKEN_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PpsIdle', ctypes.c_uint32, 1),
        ('PpsLoadFixDisable', ctypes.c_uint32, 1),
        ('Spare2', ctypes.c_uint32, 1),
        ('ForcePpsIdle', ctypes.c_uint32, 1),
        ('Spare4', ctypes.c_uint32, 1),
        ('Spare5', ctypes.c_uint32, 1),
        ('Spare6', ctypes.c_uint32, 1),
        ('SbClkRunWithRefClkDis', ctypes.c_uint32, 1),
        ('ChassisClockRequestDuration', ctypes.c_uint32, 4),
        ('Spare12', ctypes.c_uint32, 1),
        ('Spare13', ctypes.c_uint32, 1),
        ('Spare14', ctypes.c_uint32, 1),
        ('InvertDdiaHpd', ctypes.c_uint32, 1),
        ('InvertDdibHpd', ctypes.c_uint32, 1),
        ('InvertDdicHpd', ctypes.c_uint32, 1),
        ('InvertDdidHpd', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 4),
        ('Reserved23', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 4),
        ('WakePinValueOverride', ctypes.c_uint32, 2),
        ('WakePinEnableOverride', ctypes.c_uint32, 2),
    ]


class REG_SCHICKEN_1(ctypes.Union):
    value = 0
    offset = 0

    PpsIdle = 0  # bit 0 to 1
    PpsLoadFixDisable = 0  # bit 1 to 2
    Spare2 = 0  # bit 2 to 3
    ForcePpsIdle = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
    SbClkRunWithRefClkDis = 0  # bit 7 to 8
    ChassisClockRequestDuration = 0  # bit 8 to 12
    Spare12 = 0  # bit 12 to 13
    Spare13 = 0  # bit 13 to 14
    Spare14 = 0  # bit 14 to 15
    InvertDdiaHpd = 0  # bit 15 to 16
    InvertDdibHpd = 0  # bit 16 to 17
    InvertDdicHpd = 0  # bit 17 to 18
    InvertDdidHpd = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 23
    Reserved23 = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 28
    WakePinValueOverride = 0  # bit 28 to 30
    WakePinEnableOverride = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SCHICKEN_1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SCHICKEN_1, self).__init__()
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
    GPIO_CTL_2 = 0xC5018
    GPIO_CTL_3 = 0xC501C
    GPIO_CTL_4 = 0xC5020


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

