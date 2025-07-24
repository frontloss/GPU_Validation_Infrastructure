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
# @file IclPchRegs.py
# @brief contains IclPchRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_RAW_FREQUENCY(Enum):
    RAW_FREQUENCY_19_2_MHZ = 0x0
    RAW_FREQUENCY_24_MHZ = 0x1


class OFFSET_SFUSE_STRAP:
    SFUSE_STRAP = 0xC2014


class _SFUSE_STRAP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 5),
        ('Reserved5', ctypes.c_uint32, 3),
        ('RawFrequency', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 23),
    ]


class REG_SFUSE_STRAP(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 8
    RawFrequency = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SFUSE_STRAP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SFUSE_STRAP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_INTERNAL_SEQUENCE_STATE(Enum):
    INTERNAL_SEQUENCE_STATE_POWER_OFF_IDLE_S0_0 = 0x0
    INTERNAL_SEQUENCE_STATE_POWER_OFF_WAIT_FOR_CYCLE_DELAY_S0_1 = 0x1
    INTERNAL_SEQUENCE_STATE_POWER_OFF_S0_2 = 0x2
    INTERNAL_SEQUENCE_STATE_POWER_OFF_S0_3 = 0x3
    INTERNAL_SEQUENCE_STATE_POWER_ON_IDLE_S1_0 = 0x8
    INTERNAL_SEQUENCE_STATE_POWER_ON_S1_1 = 0x9
    INTERNAL_SEQUENCE_STATE_POWER_ON_S1_2 = 0xA
    INTERNAL_SEQUENCE_STATE_POWER_ON_WAIT_FOR_CYCLE_DELAY_S1_3 = 0xB
    INTERNAL_SEQUENCE_STATE_RESET = 0xF


class ENUM_POWER_CYCLE_DELAY_ACTIVE(Enum):
    POWER_CYCLE_DELAY_ACTIVE_NOT_ACTIVE = 0x0
    POWER_CYCLE_DELAY_ACTIVE_ACTIVE = 0x1


class ENUM_POWER_SEQUENCE_PROGRESS(Enum):
    POWER_SEQUENCE_PROGRESS_NONE = 0x0  # Panel is not in a power sequence
    POWER_SEQUENCE_PROGRESS_POWER_UP = 0x1  # Panel is in a power up sequence (may include power cycle delay)
    POWER_SEQUENCE_PROGRESS_POWER_DOWN = 0x2  # Panel is in a power down sequence


class ENUM_PANEL_POWER_ON_STATUS(Enum):
    PANEL_POWER_ON_STATUS_OFF = 0x0  # Panel power down has completed. A power cycle delay may be currently active.
    PANEL_POWER_ON_STATUS_ON = 0x1  # Panel is currently powered up or is currently in the power down sequence.


class OFFSET_PP_STATUS:
    PP_STATUS = 0xC7200
    PP_STATUS_2 = 0xC7300


class _PP_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('InternalSequenceState', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 23),
        ('PowerCycleDelayActive', ctypes.c_uint32, 1),
        ('PowerSequenceProgress', ctypes.c_uint32, 2),
        ('Reserved30', ctypes.c_uint32, 1),
        ('PanelPowerOnStatus', ctypes.c_uint32, 1),
    ]


class REG_PP_STATUS(ctypes.Union):
    value = 0
    offset = 0

    InternalSequenceState = 0  # bit 0 to 4
    Reserved4 = 0  # bit 4 to 27
    PowerCycleDelayActive = 0  # bit 27 to 28
    PowerSequenceProgress = 0  # bit 28 to 30
    Reserved30 = 0  # bit 30 to 31
    PanelPowerOnStatus = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PP_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PP_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_POWER_STATE_TARGET(Enum):
    POWER_STATE_TARGET_OFF = 0x0  # If panel power is currently on, the power off sequence starts immediately. If a pow
                                  # er on sequence is currently in progress, the power off sequence starts after the
                                  # power on state is reached, which may include a power cycle delay.
    POWER_STATE_TARGET_ON = 0x1  # If panel power is currently off, the power on sequence starts immediately. If a powe
                                 # r off sequence is currently in progress, the power on sequence starts after the
                                 # power off state is reached and the power cycle delay is met.


class ENUM_POWER_DOWN_ON_RESET(Enum):
    POWER_DOWN_ON_RESET_DO_NOT_RUN_POWER_DOWN_ON_RESET = 0x0
    POWER_DOWN_ON_RESET_RUN_POWER_DOWN_ON_RESET = 0x1


class ENUM_BACKLIGHT_ENABLE(Enum):
    BACKLIGHT_DISABLE = 0x0
    BACKLIGHT_ENABLE = 0x1


class ENUM_VDD_OVERRIDE(Enum):
    VDD_OVERRIDE_NOT_FORCE = 0x0
    VDD_OVERRIDE_FORCE = 0x1


class ENUM_POWER_CYCLE_DELAY(Enum):
    POWER_CYCLE_DELAY_NO_DELAY = 0x0
    POWER_CYCLE_DELAY_400_MS = 0x5


class OFFSET_PP_CONTROL:
    PP_CONTROL = 0xC7204
    PP_CONTROL_2 = 0xC7304


class _PP_CONTROL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PowerStateTarget', ctypes.c_uint32, 1),
        ('PowerDownOnReset', ctypes.c_uint32, 1),
        ('BacklightEnable', ctypes.c_uint32, 1),
        ('VddOverride', ctypes.c_uint32, 1),
        ('PowerCycleDelay', ctypes.c_uint32, 5),
        ('Reserved9', ctypes.c_uint32, 7),
        ('Spare3116', ctypes.c_uint32, 16),
    ]


class REG_PP_CONTROL(ctypes.Union):
    value = 0
    offset = 0

    PowerStateTarget = 0  # bit 0 to 1
    PowerDownOnReset = 0  # bit 1 to 2
    BacklightEnable = 0  # bit 2 to 3
    VddOverride = 0  # bit 3 to 4
    PowerCycleDelay = 0  # bit 4 to 9
    Reserved9 = 0  # bit 9 to 16
    Spare3116 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PP_CONTROL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PP_CONTROL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PP_ON_DELAYS:
    PP_ON_DELAYS = 0xC7208
    PP_ON_DELAYS_2 = 0xC7308


class _PP_ON_DELAYS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PowerOnToBacklightOn', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('PowerUpDelay', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PP_ON_DELAYS(ctypes.Union):
    value = 0
    offset = 0

    PowerOnToBacklightOn = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    PowerUpDelay = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PP_ON_DELAYS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PP_ON_DELAYS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PP_OFF_DELAYS:
    PP_OFF_DELAYS = 0xC720C
    PP_OFF_DELAYS_2 = 0xC730C


class _PP_OFF_DELAYS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BacklightOffToPowerDown', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('PowerDownDelay', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PP_OFF_DELAYS(ctypes.Union):
    value = 0
    offset = 0

    BacklightOffToPowerDown = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    PowerDownDelay = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PP_OFF_DELAYS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PP_OFF_DELAYS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_MICROSECOND_COUNTER_FRACTION_NUMERATOR(Enum):
    MICROSECOND_COUNTER_FRACTION_NUMERATOR_0 = 0x0  # No fraction
    MICROSECOND_COUNTER_FRACTION_NUMERATOR_1 = 0x1  # Numerator 1
    MICROSECOND_COUNTER_FRACTION_NUMERATOR_2 = 0x2  # Numerator 2


class ENUM_MICROSECOND_COUNTER_DIVIDER(Enum):
    MICROSECOND_COUNTER_DIVIDER_24_MHZ = 0x18
    MICROSECOND_COUNTER_DIVIDER_19_MHZ = 0x13


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


class ENUM_BACKLIGHT_POLARITY(Enum):
    BACKLIGHT_POLARITY_ACTIVE_HIGH = 0x0
    BACKLIGHT_POLARITY_ACTIVE_LOW = 0x1


class ENUM_PWM_PCH_ENABLE(Enum):
    PWM_PCH_DISABLE = 0x0
    PWM_PCH_ENABLE = 0x1


class OFFSET_SBLC_PWM_CTL1:
    SBLC_PWM_CTL1 = 0xC8250
    SBLC_PWM_CTL1_2 = 0xC8350


class _SBLC_PWM_CTL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 29),
        ('BacklightPolarity', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 1),
        ('PwmPchEnable', ctypes.c_uint32, 1),
    ]


class REG_SBLC_PWM_CTL1(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 29
    BacklightPolarity = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 31
    PwmPchEnable = 0  # bit 31 to 32

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


class OFFSET_SBLC_PWM_FREQ:
    SBLC_PWM_FREQ = 0xC8254
    SBLC_PWM_FREQ_2 = 0xC8354


class _SBLC_PWM_FREQ(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Frequency', ctypes.c_uint32, 32),
    ]


class REG_SBLC_PWM_FREQ(ctypes.Union):
    value = 0
    offset = 0

    Frequency = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SBLC_PWM_FREQ),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SBLC_PWM_FREQ, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SBLC_PWM_DUTY:
    SBLC_PWM_DUTY = 0xC8258
    SBLC_PWM_DUTY_2 = 0xC8358


class _SBLC_PWM_DUTY(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DutyCycle', ctypes.c_uint32, 32),
    ]


class REG_SBLC_PWM_DUTY(ctypes.Union):
    value = 0
    offset = 0

    DutyCycle = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SBLC_PWM_DUTY),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SBLC_PWM_DUTY, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PARTITION_LEVEL_CLOCK_GATING_DISABLE(Enum):
    PARTITION_LEVEL_CLOCK_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    PARTITION_LEVEL_CLOCK_GATING_DISABLE = 0x1  # Disable clock gating function


class ENUM_PWM_CGE_GATING_DISABLE(Enum):
    PWM_CGE_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    PWM_CGE_GATING_DISABLE = 0x1  # Disable clock gating function


class ENUM_CPUNIT_GATING_DISABLE(Enum):
    CPUNIT_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    CPUNIT_GATING_DISABLE = 0x1  # Disable clock gating function


class ENUM_DPMGUNIT_GATING_DISABLE(Enum):
    DPMGUNIT_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    DPMGUNIT_GATING_DISABLE = 0x1  # Disable clock gating function


class ENUM_DRPOUNIT_GATING_DISABLE(Enum):
    DRPOUNIT_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    DRPOUNIT_GATING_DISABLE = 0x1  # Disable clock gating function


class ENUM_SECOND_PWM_CGE_GATING_DISABLE(Enum):
    SECOND_PWM_CGE_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    SECOND_PWM_CGE_GATING_DISABLE = 0x1  # Disable clock gating function


class ENUM_SECOND_DPLS_GATING_DISABLE(Enum):
    SECOND_DPLS_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    SECOND_DPLS_GATING_DISABLE = 0x1  # Disable clock gating function


class ENUM_DPIOUNIT_GATING_DISABLE(Enum):
    DPIOUNIT_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    DPIOUNIT_GATING_DISABLE = 0x1  # Disable clock gating function


class ENUM_DPLSUNIT_GATING_DISABLE(Enum):
    DPLSUNIT_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    DPLSUNIT_GATING_DISABLE = 0x1  # Disable clock gating function


class ENUM_DSBE_GATING_DISABLE(Enum):
    DSBE_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    DSBE_GATING_DISABLE = 0x1  # Disable clock gating function


class ENUM_GMBUSUNIT_GATING_DISABLE(Enum):
    GMBUSUNIT_GATING_ENABLE = 0x0  # Clock gating controlled by unit enabling logic
    GMBUSUNIT_GATING_DISABLE = 0x1  # Disable clock gating function


class OFFSET_SCLKGATE_DIS:
    SCLKGATE_DIS = 0xC2020


class _SCLKGATE_DIS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('PartitionLevelClockGatingDisable', ctypes.c_uint32, 1),
        ('PwmCgeGatingDisable', ctypes.c_uint32, 1),
        ('CpunitGatingDisable', ctypes.c_uint32, 1),
        ('DpmgunitGatingDisable', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 1),
        ('DrpounitGatingDisable', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 8),
        ('SecondPwmCgeGatingDisable', ctypes.c_uint32, 1),
        ('SecondDplsGatingDisable', ctypes.c_uint32, 1),
        ('DpiounitGatingDisable', ctypes.c_uint32, 1),
        ('DplsunitGatingDisable', ctypes.c_uint32, 1),
        ('DsbeGatingDisable', ctypes.c_uint32, 1),
        ('GmbusunitGatingDisable', ctypes.c_uint32, 1),
    ]


class REG_SCLKGATE_DIS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    PartitionLevelClockGatingDisable = 0  # bit 12 to 13
    PwmCgeGatingDisable = 0  # bit 13 to 14
    CpunitGatingDisable = 0  # bit 14 to 15
    DpmgunitGatingDisable = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 17
    DrpounitGatingDisable = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 26
    SecondPwmCgeGatingDisable = 0  # bit 26 to 27
    SecondDplsGatingDisable = 0  # bit 27 to 28
    DpiounitGatingDisable = 0  # bit 28 to 29
    DplsunitGatingDisable = 0  # bit 29 to 30
    DsbeGatingDisable = 0  # bit 30 to 31
    GmbusunitGatingDisable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SCLKGATE_DIS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SCLKGATE_DIS, self).__init__()
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


class ENUM_PPS_IDLE(Enum):
    PPS_IDLE_IMPROVED_PPS_IDLE_DETECTION = 0x1
    PPS_IDLE_ORIGINAL_PPS_IDLE_DETECTION = 0x0


class ENUM_PPS_LOAD_FIX_DISABLE(Enum):
    PPS_LOAD_FIX_DISABLE_FIX_FOR_PPS_DELAY_LOADING = 0x1
    PPS_LOAD_FIX_ENABLE_FIX_FOR_PPS_DELAY_LOADING = 0x0


class ENUM_SECOND_PPS_IO_SELECT(Enum):
    SECOND_PPS_IO_SELECT_SELECT_SECOND_PPS = 0x1
    SECOND_PPS_IO_SELECT_SELECT_DDIC_GPIO_AND_HPD = 0x0


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


class ENUM_INVERT_TC1_HPD(Enum):
    INVERT_TC1_HPD_INVERT = 0x1
    INVERT_TC1_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_TC2_HPD(Enum):
    INVERT_TC2_HPD_INVERT = 0x1
    INVERT_TC2_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_TC3_HPD(Enum):
    INVERT_TC3_HPD_INVERT = 0x1
    INVERT_TC3_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_TC4_HPD(Enum):
    INVERT_TC4_HPD_INVERT = 0x1
    INVERT_TC4_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_TC5_HPD(Enum):
    INVERT_TC5_HPD_INVERT = 0x1
    INVERT_TC5_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_TC6_HPD(Enum):
    INVERT_TC6_HPD_INVERT = 0x1
    INVERT_TC6_HPD_DO_NOT_INVERT = 0x0


class OFFSET_SCHICKEN_1:
    SCHICKEN_1 = 0xC2000


class _SCHICKEN_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PpsIdle', ctypes.c_uint32, 1),
        ('PpsLoadFixDisable', ctypes.c_uint32, 1),
        ('SecondPpsIoSelect', ctypes.c_uint32, 1),
        ('ForcePpsIdle', ctypes.c_uint32, 1),
        ('Spare4', ctypes.c_uint32, 1),
        ('Spare5', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 1),
        ('SbClkRunWithRefClkDis', ctypes.c_uint32, 1),
        ('ChassisClockRequestDuration', ctypes.c_uint32, 4),
        ('Reserved12', ctypes.c_uint32, 3),
        ('InvertDdiaHpd', ctypes.c_uint32, 1),
        ('InvertDdibHpd', ctypes.c_uint32, 1),
        ('InvertDdicHpd', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 5),
        ('InvertTc1Hpd', ctypes.c_uint32, 1),
        ('InvertTc2Hpd', ctypes.c_uint32, 1),
        ('InvertTc3Hpd', ctypes.c_uint32, 1),
        ('InvertTc4Hpd', ctypes.c_uint32, 1),
        ('InvertTc5Hpd', ctypes.c_uint32, 1),
        ('InvertTc6Hpd', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_SCHICKEN_1(ctypes.Union):
    value = 0
    offset = 0

    PpsIdle = 0  # bit 0 to 1
    PpsLoadFixDisable = 0  # bit 1 to 2
    SecondPpsIoSelect = 0  # bit 2 to 3
    ForcePpsIdle = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 7
    SbClkRunWithRefClkDis = 0  # bit 7 to 8
    ChassisClockRequestDuration = 0  # bit 8 to 12
    Reserved12 = 0  # bit 12 to 15
    InvertDdiaHpd = 0  # bit 15 to 16
    InvertDdibHpd = 0  # bit 16 to 17
    InvertDdicHpd = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 23
    InvertTc1Hpd = 0  # bit 23 to 24
    InvertTc2Hpd = 0  # bit 24 to 25
    InvertTc3Hpd = 0  # bit 25 to 26
    InvertTc4Hpd = 0  # bit 26 to 27
    InvertTc5Hpd = 0  # bit 27 to 28
    InvertTc6Hpd = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 32

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

