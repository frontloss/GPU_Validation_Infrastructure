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
# @file Gen14PipeRegs.py
# @brief contains Gen14PipeRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_UV_HORZ_FILTER_SET_SEL_(Enum):
    UV_HORZ_FILTER_SET_SEL_SET_0 = 0x0
    UV_HORZ_FILTER_SET_SEL_SET_1 = 0x1


class ENUM_UV_VERT_FILTER_SET_SEL(Enum):
    UV_VERT_FILTER_SET_SEL_SET_0 = 0x0
    UV_VERT_FILTER_SET_SEL_SET_1 = 0x1


class ENUM_Y_HORZ_FILTER_SET_SEL_(Enum):
    Y_HORZ_FILTER_SET_SEL_SET_0 = 0x0
    Y_HORZ_FILTER_SET_SEL_SET_1 = 0x1


class ENUM_Y_VERT_FILTER_SET_SEL(Enum):
    Y_VERT_FILTER_SET_SEL_SET_0 = 0x0
    Y_VERT_FILTER_SET_SEL_SET_1 = 0x1


class ENUM_V_FILTER_BYPASS(Enum):
    V_FILTER_BYPASS_ENABLE = 0x0
    V_FILTER_BYPASS_BYPASS = 0x1


class ENUM_ALLOW_DB_STALL(Enum):
    ALLOW_DB_STALL_NOT_ALLOWED = 0x0
    ALLOW_DB_STALL_ALLOWED = 0x1


class ENUM_ERROR_INJECTION_FLIP_BITS(Enum):
    ERROR_INJECTION_FLIP_BITS_NO_ERRORS = 0x0  # No bits will be flipped
    ERROR_INJECTION_FLIP_BITS_FLIP_BIT_0 = 0x1  # Flip bit 0 of the static Data + ECC value. Should result in a Single 
                                                # bit error
    ERROR_INJECTION_FLIP_BITS_FLIP_BIT_1 = 0x2  # Flip bit 1of the static Data + ECC value. Should result in a Single b
                                                # it error
    ERROR_INJECTION_FLIP_BITS_FLIP_BITS_0_AND_1 = 0x3  # Flip bits 0 and 1 of the staticData + ECC value. Should result
                                                       #  in a Double bit error


class ENUM_ECC_ERROR_INJECTION_ENABLE(Enum):
    ECC_ERROR_INJECTION_DISABLED = 0x0
    ECC_ERROR_INJECTION_ENABLED = 0x1


class ENUM_PWRUP_IN_PROGRESS(Enum):
    PWRUP_IN_PROGRESS_POWERUP_COMPLETE = 0x0
    PWRUP_IN_PROGRESS_POWERUP_IN_PROGRESS = 0x1


class ENUM_PROGRAMMABLE_SCALE_FACTOR(Enum):
    PROGRAMMABLE_SCALE_FACTOR_DISABLE = 0x0
    PROGRAMMABLE_SCALE_FACTOR_ENABLE = 0x1


class ENUM_VERTICAL_INT_FIELD_INVERT(Enum):
    VERTICAL_INT_FIELD_INVERT_FIELD_1 = 0x0
    VERTICAL_INT_FIELD_INVERT_FIELD_0 = 0x1


class ENUM_PIPE_SCALER_LOCATION(Enum):
    PIPE_SCALER_LOCATION_AFTER_OUTPUT_CSC = 0x0  # This is a non-linear tap point
    PIPE_SCALER_LOCATION_AFTER_CSC = 0x1  # This is a linear tap point


class ENUM_ADAPTIVE_FILTER_SELECT(Enum):
    ADAPTIVE_FILTER_SELECT_MEDIUM = 0x0
    ADAPTIVE_FILTER_SELECT_EDGE_ENHANCE = 0x1


class ENUM_FILTER_SELECT(Enum):
    FILTER_SELECT_MEDIUM = 0x0
    FILTER_SELECT_PROGRAMMED = 0x1
    FILTER_SELECT_EDGE_ENHANCE = 0x2
    FILTER_SELECT_BILINEAR = 0x3


class ENUM_SCALER_BINDING(Enum):
    SCALER_BINDING_PIPE_SCALER = 0x0
    SCALER_BINDING_PLANE_1_SCALER = 0x1
    SCALER_BINDING_PLANE_2_SCALER = 0x2
    SCALER_BINDING_PLANE_3_SCALER = 0x3
    SCALER_BINDING_PLANE_4_SCALER = 0x4
    SCALER_BINDING_PLANE_5_SCALER = 0x5


class ENUM_ADAPTIVE_FILTERING(Enum):
    ADAPTIVE_FILTERING_DISABLE = 0x0
    ADAPTIVE_FILTERING_ENABLE = 0x1


class ENUM_SCALER_TYPE(Enum):
    SCALER_TYPE_NON_LINEAR = 0x0
    SCALER_TYPE_LINEAR = 0x1


class ENUM_ENABLE_SCALER(Enum):
    ENABLE_SCALER_DISABLE = 0x0
    ENABLE_SCALER_ENABLE = 0x1


class OFFSET_PS_CTRL:
    PS_CTRL_1_A = 0x68180
    PS_CTRL_2_A = 0x68280
    PS_CTRL_1_B = 0x68980
    PS_CTRL_2_B = 0x68A80
    PS_CTRL_1_C = 0x69180
    PS_CTRL_2_C = 0x69280
    PS_CTRL_1_D = 0x69980
    PS_CTRL_2_D = 0x69A80


class _PS_CTRL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('UvHorzFilterSetSel', ctypes.c_uint32, 1),
        ('UvVertFilterSetSel', ctypes.c_uint32, 1),
        ('YHorzFilterSetSel', ctypes.c_uint32, 1),
        ('YVertFilterSetSel', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 3),
        ('VFilterBypass', ctypes.c_uint32, 1),
        ('AllowDbStall', ctypes.c_uint32, 1),
        ('Reserved10', ctypes.c_uint32, 2),
        ('ErrorInjectionFlipBits', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 1),
        ('EccErrorInjectionEnable', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 1),
        ('PwrupInProgress', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 1),
        ('ProgrammableScaleFactor', ctypes.c_uint32, 1),
        ('VerticalIntFieldInvert', ctypes.c_uint32, 1),
        ('PipeScalerLocation', ctypes.c_uint32, 1),
        ('AdaptiveFilterSelect', ctypes.c_uint32, 1),
        ('FilterSelect', ctypes.c_uint32, 2),
        ('ScalerBinding', ctypes.c_uint32, 3),
        ('AdaptiveFiltering', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 1),
        ('ScalerType', ctypes.c_uint32, 1),
        ('EnableScaler', ctypes.c_uint32, 1),
    ]


class REG_PS_CTRL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    UvHorzFilterSetSel = 0  # bit 1 to 2
    UvVertFilterSetSel = 0  # bit 2 to 3
    YHorzFilterSetSel = 0  # bit 3 to 4
    YVertFilterSetSel = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 8
    VFilterBypass = 0  # bit 8 to 9
    AllowDbStall = 0  # bit 9 to 10
    Reserved10 = 0  # bit 10 to 12
    ErrorInjectionFlipBits = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 15
    EccErrorInjectionEnable = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 17
    PwrupInProgress = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 19
    ProgrammableScaleFactor = 0  # bit 19 to 20
    VerticalIntFieldInvert = 0  # bit 20 to 21
    PipeScalerLocation = 0  # bit 21 to 22
    AdaptiveFilterSelect = 0  # bit 22 to 23
    FilterSelect = 0  # bit 23 to 25
    ScalerBinding = 0  # bit 25 to 28
    AdaptiveFiltering = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 30
    ScalerType = 0  # bit 30 to 31
    EnableScaler = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_CTRL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_CTRL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PS_ECC_STAT:
    PS_ECC_STAT_1_A = 0x681D0
    PS_ECC_STAT_2_A = 0x682D0
    PS_ECC_STAT_1_B = 0x689D0
    PS_ECC_STAT_2_B = 0x68AD0
    PS_ECC_STAT_1_C = 0x691D0
    PS_ECC_STAT_2_C = 0x692D0
    PS_ECC_STAT_1_D = 0x699D0
    PS_ECC_STAT_2_D = 0x69AD0


class _PS_ECC_STAT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SingleErrorDetected', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 15),
        ('DoubleErrorDetected', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_PS_ECC_STAT(ctypes.Union):
    value = 0
    offset = 0

    SingleErrorDetected = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 16
    DoubleErrorDetected = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_ECC_STAT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_ECC_STAT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_UV_OR_RGB_INITIAL_HPHASE_TRIP(Enum):
    UV_OR_RGB_INITIAL_HPHASE_TRIP_ENABLE = 0x1
    UV_OR_RGB_INITIAL_HPHASE_TRIP_DISABLE = 0x0


class ENUM_Y_INITIAL_HPHASE_TRIP(Enum):
    Y_INITIAL_HPHASE_TRIP_ENABLE = 0x1
    Y_INITIAL_HPHASE_TRIP_DISABLE = 0x0


class OFFSET_PS_HPHASE:
    PS_HPHASE_1_A = 0x68194
    PS_HPHASE_2_A = 0x68294
    PS_HPHASE_1_B = 0x68994
    PS_HPHASE_2_B = 0x68A94
    PS_HPHASE_1_C = 0x69194
    PS_HPHASE_2_C = 0x69294
    PS_HPHASE_1_D = 0x69994
    PS_HPHASE_2_D = 0x69A94


class _PS_HPHASE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('UvOrRgbInitialHphaseTrip', ctypes.c_uint32, 1),
        ('UvOrRgbInitialHphaseFrac', ctypes.c_uint32, 13),
        ('UvOrRgbInitialHphaseInt', ctypes.c_uint32, 2),
        ('YInitialHphaseTrip', ctypes.c_uint32, 1),
        ('YInitialHphaseFrac', ctypes.c_uint32, 13),
        ('YInitialHphaseInt', ctypes.c_uint32, 2),
    ]


class REG_PS_HPHASE(ctypes.Union):
    value = 0
    offset = 0

    UvOrRgbInitialHphaseTrip = 0  # bit 0 to 1
    UvOrRgbInitialHphaseFrac = 0  # bit 1 to 14
    UvOrRgbInitialHphaseInt = 0  # bit 14 to 16
    YInitialHphaseTrip = 0  # bit 16 to 17
    YInitialHphaseFrac = 0  # bit 17 to 30
    YInitialHphaseInt = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_HPHASE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_HPHASE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PS_HSCALE:
    PS_HSCALE_1_A = 0x68190
    PS_HSCALE_2_A = 0x68290
    PS_HSCALE_1_B = 0x68990
    PS_HSCALE_2_B = 0x68A90
    PS_HSCALE_1_C = 0x69190
    PS_HSCALE_2_C = 0x69290
    PS_HSCALE_1_D = 0x69990
    PS_HSCALE_2_D = 0x69A90


class _PS_HSCALE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HscaleFrac', ctypes.c_uint32, 15),
        ('HscaleInt', ctypes.c_uint32, 3),
        ('Reserved18', ctypes.c_uint32, 14),
    ]


class REG_PS_HSCALE(ctypes.Union):
    value = 0
    offset = 0

    HscaleFrac = 0  # bit 0 to 15
    HscaleInt = 0  # bit 15 to 18
    Reserved18 = 0  # bit 18 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_HSCALE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_HSCALE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SLPEN_DELAY(Enum):
    SLPEN_DELAY_8_CDCLKS = 0x0
    SLPEN_DELAY_16_CDCLKS = 0x1
    SLPEN_DELAY_24_CDCLKS = 0x2
    SLPEN_DELAY_32_CDCLKS = 0x3


class ENUM_SETTLING_TIME(Enum):
    SETTLING_TIME_32_CDCLKS = 0x0
    SETTLING_TIME_64_CDCLKS = 0x1
    SETTLING_TIME_96_CDCLKS = 0x2
    SETTLING_TIME_128_CDCLKS = 0x3


class ENUM_DYNAMIC_PWR_GATE_DISABLE(Enum):
    DYNAMIC_PWR_GATE_DISABLE_DO_NOT_DISABLE = 0x0
    DYNAMIC_PWR_GATE_DISABLE = 0x1


class ENUM_PWR_GATE_DIS_OVERRIDE(Enum):
    PWR_GATE_DIS_OVERRIDE_NOT_OVERRIDE = 0x0  # Do not override power gating
    PWR_GATE_DIS_OVERRIDE_OVERRIDE = 0x1  # Override power gating to disabled


class OFFSET_PS_PWR_GATE:
    PS_PWR_GATE_1_A = 0x68160
    PS_PWR_GATE_2_A = 0x68260
    PS_PWR_GATE_1_B = 0x68960
    PS_PWR_GATE_2_B = 0x68A60
    PS_PWR_GATE_1_C = 0x69160
    PS_PWR_GATE_2_C = 0x69260
    PS_PWR_GATE_1_D = 0x69960
    PS_PWR_GATE_2_D = 0x69A60


class _PS_PWR_GATE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SlpenDelay', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('SettlingTime', ctypes.c_uint32, 2),
        ('DynamicPwrGateDisable', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 24),
        ('Reserved30', ctypes.c_uint32, 1),
        ('PwrGateDisOverride', ctypes.c_uint32, 1),
    ]


class REG_PS_PWR_GATE(ctypes.Union):
    value = 0
    offset = 0

    SlpenDelay = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    SettlingTime = 0  # bit 3 to 5
    DynamicPwrGateDisable = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 30
    Reserved30 = 0  # bit 30 to 31
    PwrGateDisOverride = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_PWR_GATE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_PWR_GATE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_UV_OR_RGB_INITIAL_VPHASE_TRIP(Enum):
    UV_OR_RGB_INITIAL_VPHASE_TRIP_USED = 0x1
    UV_OR_RGB_INITIAL_VPHASE_TRIP_NOT_USED = 0x0


class ENUM_Y_INITIAL_VPHASE_TRIP(Enum):
    Y_INITIAL_VPHASE_TRIP_USED = 0x1
    Y_INITIAL_VPHASE_TRIP_NOT_USED = 0x0


class OFFSET_PS_VPHASE:
    PS_VPHASE_1_A = 0x68188
    PS_VPHASE_2_A = 0x68288
    PS_VPHASE_1_B = 0x68988
    PS_VPHASE_2_B = 0x68A88
    PS_VPHASE_1_C = 0x69188
    PS_VPHASE_2_C = 0x69288
    PS_VPHASE_1_D = 0x69988
    PS_VPHASE_2_D = 0x69A88


class _PS_VPHASE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('UvOrRgbInitialVphaseTrip', ctypes.c_uint32, 1),
        ('UvOrRgbInitialVphaseFrac', ctypes.c_uint32, 13),
        ('UvOrRgbInitialVphaseInt', ctypes.c_uint32, 2),
        ('YInitialVphaseTrip', ctypes.c_uint32, 1),
        ('YInitialVphaseFrac', ctypes.c_uint32, 13),
        ('YInitialVphaseInt', ctypes.c_uint32, 2),
    ]


class REG_PS_VPHASE(ctypes.Union):
    value = 0
    offset = 0

    UvOrRgbInitialVphaseTrip = 0  # bit 0 to 1
    UvOrRgbInitialVphaseFrac = 0  # bit 1 to 14
    UvOrRgbInitialVphaseInt = 0  # bit 14 to 16
    YInitialVphaseTrip = 0  # bit 16 to 17
    YInitialVphaseFrac = 0  # bit 17 to 30
    YInitialVphaseInt = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_VPHASE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_VPHASE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PS_VSCALE:
    PS_VSCALE_1_A = 0x68184
    PS_VSCALE_2_A = 0x68284
    PS_VSCALE_1_B = 0x68984
    PS_VSCALE_2_B = 0x68A84
    PS_VSCALE_1_C = 0x69184
    PS_VSCALE_2_C = 0x69284
    PS_VSCALE_1_D = 0x69984
    PS_VSCALE_2_D = 0x69A84


class _PS_VSCALE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VscaleFrac', ctypes.c_uint32, 15),
        ('VscaleInt', ctypes.c_uint32, 3),
        ('Reserved18', ctypes.c_uint32, 14),
    ]


class REG_PS_VSCALE(ctypes.Union):
    value = 0
    offset = 0

    VscaleFrac = 0  # bit 0 to 15
    VscaleInt = 0  # bit 15 to 18
    Reserved18 = 0  # bit 18 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_VSCALE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_VSCALE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_INDEX_AUTO_INCREMENT(Enum):
    INDEX_AUTO_INCREMENT_NO_INCREMENT = 0x0  # Do not automatically increment the index value.
    INDEX_AUTO_INCREMENT_AUTO_INCREMENT = 0x1  # Increment the index value with each read or write to the data register
                                               # .


class OFFSET_PS_COEF_INDEX:
    PS_COEF_SET_0_INDEX_1_A = 0x68198
    PS_COEF_SET_1_INDEX_1_A = 0x681A0
    PS_COEF_SET_0_INDEX_2_A = 0x68298
    PS_COEF_SET_1_INDEX_2_A = 0x682A0
    PS_COEF_SET_0_INDEX_1_B = 0x68998
    PS_COEF_SET_1_INDEX_1_B = 0x689A0
    PS_COEF_SET_0_INDEX_2_B = 0x68A98
    PS_COEF_SET_1_INDEX_2_B = 0x68AA0
    PS_COEF_SET_0_INDEX_1_C = 0x69198
    PS_COEF_SET_1_INDEX_1_C = 0x691A0
    PS_COEF_SET_0_INDEX_2_C = 0x69298
    PS_COEF_SET_1_INDEX_2_C = 0x692A0
    PS_COEF_SET_0_INDEX_1_D = 0x69998
    PS_COEF_SET_1_INDEX_1_D = 0x699A0
    PS_COEF_SET_0_INDEX_2_D = 0x69A98
    PS_COEF_SET_1_INDEX_2_D = 0x69AA0


class _PS_COEF_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 4),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_PS_COEF_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 10
    IndexAutoIncrement = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_COEF_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_COEF_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PS_COEF_DATA:
    PS_COEF_SET_0_DATA_1_A = 0x6819C
    PS_COEF_SET_1_DATA_1_A = 0x681A4
    PS_COEF_SET_0_DATA_2_A = 0x6829C
    PS_COEF_SET_1_DATA_2_A = 0x682A4
    PS_COEF_SET_0_DATA_1_B = 0x6899C
    PS_COEF_SET_1_DATA_1_B = 0x689A4
    PS_COEF_SET_0_DATA_2_B = 0x68A9C
    PS_COEF_SET_1_DATA_2_B = 0x68AA4
    PS_COEF_SET_0_DATA_1_C = 0x6919C
    PS_COEF_SET_1_DATA_1_C = 0x691A4
    PS_COEF_SET_0_DATA_2_C = 0x6929C
    PS_COEF_SET_1_DATA_2_C = 0x692A4
    PS_COEF_SET_0_DATA_1_D = 0x6999C
    PS_COEF_SET_1_DATA_1_D = 0x699A4
    PS_COEF_SET_0_DATA_2_D = 0x69A9C
    PS_COEF_SET_1_DATA_2_D = 0x69AA4


class _PS_COEF_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Coefficient1', ctypes.c_uint32, 16),
        ('Coefficient2', ctypes.c_uint32, 16),
    ]


class REG_PS_COEF_DATA(ctypes.Union):
    value = 0
    offset = 0

    Coefficient1 = 0  # bit 0 to 16
    Coefficient2 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_COEF_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_COEF_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PS_ADAPTIVE_CTRL:
    PS_ADAPTIVE_CTRL_SET_0_1_A = 0x681A8
    PS_ADAPTIVE_CTRL_SET_1_1_A = 0x681AC
    PS_ADAPTIVE_CTRL_SET_0_2_A = 0x682A8
    PS_ADAPTIVE_CTRL_SET_1_2_A = 0x682AC
    PS_ADAPTIVE_CTRL_SET_0_1_B = 0x689A8
    PS_ADAPTIVE_CTRL_SET_1_1_B = 0x689AC
    PS_ADAPTIVE_CTRL_SET_0_2_B = 0x68AA8
    PS_ADAPTIVE_CTRL_SET_1_2_B = 0x68AAC
    PS_ADAPTIVE_CTRL_SET_0_1_C = 0x691A8
    PS_ADAPTIVE_CTRL_SET_1_1_C = 0x691AC
    PS_ADAPTIVE_CTRL_SET_0_2_C = 0x692A8
    PS_ADAPTIVE_CTRL_SET_1_2_C = 0x692AC
    PS_ADAPTIVE_CTRL_SET_0_1_D = 0x699A8
    PS_ADAPTIVE_CTRL_SET_1_1_D = 0x699AC
    PS_ADAPTIVE_CTRL_SET_0_2_D = 0x69AA8
    PS_ADAPTIVE_CTRL_SET_1_2_D = 0x69AAC


class _PS_ADAPTIVE_CTRL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Threshold1', ctypes.c_uint32, 8),
        ('Threshold2', ctypes.c_uint32, 8),
        ('Threshold3', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_PS_ADAPTIVE_CTRL(ctypes.Union):
    value = 0
    offset = 0

    Threshold1 = 0  # bit 0 to 8
    Threshold2 = 0  # bit 8 to 16
    Threshold3 = 0  # bit 16 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_ADAPTIVE_CTRL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_ADAPTIVE_CTRL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PS_WIN_SZ:
    PS_WIN_SZ_1_A = 0x68174
    PS_WIN_SZ_2_A = 0x68274
    PS_WIN_SZ_1_B = 0x68974
    PS_WIN_SZ_2_B = 0x68A74
    PS_WIN_SZ_1_C = 0x69174
    PS_WIN_SZ_2_C = 0x69274
    PS_WIN_SZ_1_D = 0x69974
    PS_WIN_SZ_2_D = 0x69A74


class _PS_WIN_SZ(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Ysize', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('Xsize', ctypes.c_uint32, 14),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PS_WIN_SZ(ctypes.Union):
    value = 0
    offset = 0

    Ysize = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    Xsize = 0  # bit 16 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_WIN_SZ),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_WIN_SZ, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PS_WIN_POS:
    PS_WIN_POS_1_A = 0x68170
    PS_WIN_POS_2_A = 0x68270
    PS_WIN_POS_1_B = 0x68970
    PS_WIN_POS_2_B = 0x68A70
    PS_WIN_POS_1_C = 0x69170
    PS_WIN_POS_2_C = 0x69270
    PS_WIN_POS_1_D = 0x69970
    PS_WIN_POS_2_D = 0x69A70


class _PS_WIN_POS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Ypos', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('Xpos', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PS_WIN_POS(ctypes.Union):
    value = 0
    offset = 0

    Ypos = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    Xpos = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PS_WIN_POS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PS_WIN_POS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_SRCSZ:
    PIPE_SRCSZ_A = 0x6001C
    PIPE_SRCSZ_B = 0x6101C
    PIPE_SRCSZ_C = 0x6201C
    PIPE_SRCSZ_D = 0x6301C


class _PIPE_SRCSZ(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VerticalSourceSize', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('HorizontalSourceSize', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PIPE_SRCSZ(ctypes.Union):
    value = 0
    offset = 0

    VerticalSourceSize = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    HorizontalSourceSize = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_SRCSZ),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_SRCSZ, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_SEAM_EXCESS:
    PIPE_SEAM_EXCESS_A = 0x60020
    PIPE_SEAM_EXCESS_B = 0x61020
    PIPE_SEAM_EXCESS_C = 0x62020
    PIPE_SEAM_EXCESS_D = 0x63020


class _PIPE_SEAM_EXCESS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LeftExcessAmount', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('RightExcessAmount', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PIPE_SEAM_EXCESS(ctypes.Union):
    value = 0
    offset = 0

    LeftExcessAmount = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    RightExcessAmount = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_SEAM_EXCESS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_SEAM_EXCESS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CURRENT_FIELD(Enum):
    CURRENT_FIELD_ODD = 0x0  # First field (odd field)
    CURRENT_FIELD_EVEN = 0x1  # Second field (even field)


class OFFSET_PIPE_SCANLINE:
    PIPE_SCANLINE_A = 0x70000
    PIPE_SCANLINE_B = 0x71000
    PIPE_SCANLINE_C = 0x72000
    PIPE_SCANLINE_D = 0x73000


class _PIPE_SCANLINE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LineCounterForDisplay', ctypes.c_uint32, 20),
        ('Reserved20', ctypes.c_uint32, 11),
        ('CurrentField', ctypes.c_uint32, 1),
    ]


class REG_PIPE_SCANLINE(ctypes.Union):
    value = 0
    offset = 0

    LineCounterForDisplay = 0  # bit 0 to 20
    Reserved20 = 0  # bit 20 to 31
    CurrentField = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_SCANLINE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_SCANLINE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PIPE_CSC_ENABLE(Enum):
    PIPE_CSC_DISABLE = 0x0
    PIPE_CSC_ENABLE = 0x1


class ENUM_PIPE_GAMMA_ENABLE(Enum):
    PIPE_GAMMA_DISABLE = 0x0
    PIPE_GAMMA_ENABLE = 0x1


class OFFSET_PIPE_BOTTOM_COLOR:
    PIPE_BOTTOM_COLOR_A = 0x70034
    PIPE_BOTTOM_COLOR_B = 0x71034
    PIPE_BOTTOM_COLOR_C = 0x72034
    PIPE_BOTTOM_COLOR_D = 0x73034


class _PIPE_BOTTOM_COLOR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('UBBottomColor', ctypes.c_uint32, 10),
        ('YGBottomColor', ctypes.c_uint32, 10),
        ('VRBottomColor', ctypes.c_uint32, 10),
        ('PipeCscEnable', ctypes.c_uint32, 1),
        ('PipeGammaEnable', ctypes.c_uint32, 1),
    ]


class REG_PIPE_BOTTOM_COLOR(ctypes.Union):
    value = 0
    offset = 0

    UBBottomColor = 0  # bit 0 to 10
    YGBottomColor = 0  # bit 10 to 20
    VRBottomColor = 0  # bit 20 to 30
    PipeCscEnable = 0  # bit 30 to 31
    PipeGammaEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_BOTTOM_COLOR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_BOTTOM_COLOR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_BFI_ENABLE(Enum):
    BFI_DISABLE = 0x0
    BFI_ENABLE = 0x1


class ENUM_DITHERING_TYPE(Enum):
    DITHERING_TYPE_SPATIAL = 0x0  # Spatial
    DITHERING_TYPE_ST1 = 0x1  # Spatio-Temporal 1
    DITHERING_TYPE_ST2 = 0x2  # Spatio-Temporal 2
    DITHERING_TYPE_TEMPORAL = 0x3  # Temporal


class ENUM_DITHERING_ENABLE(Enum):
    DITHERING_DISABLE = 0x0
    DITHERING_ENABLE = 0x1


class ENUM_PORT_OUTPUT_BPC(Enum):
    PORT_OUTPUT_BPC_8_BPC = 0x0  # 8 bits per color
    PORT_OUTPUT_BPC_10_BPC = 0x1  # 10 bits per color
    PORT_OUTPUT_BPC_6_BPC = 0x2  # 6 bits per color
    PORT_OUTPUT_BPC_12_BPC = 0x4  # 12 bits per color


class ENUM_PIXEL_ROUNDING(Enum):
    PIXEL_ROUNDING_ROUND_UP = 0x0
    PIXEL_ROUNDING_TRUNCATE = 0x1


class ENUM_PIXEL_EXTENSION(Enum):
    PIXEL_EXTENSION_MSB_EXTEND = 0x0
    PIXEL_EXTENSION_ZERO_EXTEND = 0x1


class ENUM_XVYCC_COLOR_RANGE_LIMIT(Enum):
    XVYCC_COLOR_RANGE_LIMIT_FULL = 0x0  # Do not limit the range
    XVYCC_COLOR_RANGE_LIMIT_LIMIT = 0x1  # Limit range


class ENUM_PIPE_OUTPUT_COLOR_SPACE_SELECT(Enum):
    PIPE_OUTPUT_COLOR_SPACE_SELECT_RGB = 0x0
    PIPE_OUTPUT_COLOR_SPACE_SELECT_YUV = 0x1


class ENUM_OLED_COMPENSATION(Enum):
    OLED_COMPENSATION_DISABLE = 0x0
    OLED_COMPENSATION_ENABLE = 0x1


class ENUM_ROTATION_INFO(Enum):
    ROTATION_INFO_NONE = 0x0  # No rotation on this pipe
    ROTATION_INFO_90 = 0x1  # 90 degree rotation on this pipe
    ROTATION_INFO_180 = 0x2  # 180 degree rotation on this pipe
    ROTATION_INFO_270 = 0x3  # 270 degree rotation on this pipe


class ENUM_OVERRIDE_BLUE_CHANNEL(Enum):
    OVERRIDE_BLUE_CHANNEL_BLUE_1S = 0x1  # Blue channel is all 1s when override enabled
    OVERRIDE_BLUE_CHANNEL_BLUE_0S = 0x0  # Blue channel is all 0s when override enabled


class ENUM_OVERRIDE_GREEN_CHANNEL(Enum):
    OVERRIDE_GREEN_CHANNEL_GREEN_1S = 0x1  # Green channel is all 1s when override enabled
    OVERRIDE_GREEN_CHANNEL_GREEN_0S = 0x0  # Green channel is all 0s when override enabled


class ENUM_OVERRIDE_RED_CHANNEL(Enum):
    OVERRIDE_RED_CHANNEL_RED_1S = 0x1  # Red channel is all 1s when override enabled
    OVERRIDE_RED_CHANNEL_RED_0S = 0x0  # Red channel is all 0s when override enabled


class ENUM_OVERRIDE_PIPE_OUTPUT(Enum):
    OVERRIDE_PIPE_OUTPUT_NO_OVERRIDE = 0x0
    OVERRIDE_PIPE_OUTPUT_OVERRIDE = 0x1


class ENUM_CHANGE_MASK_FOR_VBLANK_VSYNC_INT(Enum):
    CHANGE_MASK_FOR_VBLANK_VSYNC_INT_NOT_MASKED = 0x0
    CHANGE_MASK_FOR_VBLANK_VSYNC_INT_MASKED = 0x1


class ENUM_CHANGE_MASK_FOR_REGISTER_WRITE(Enum):
    CHANGE_MASK_FOR_REGISTER_WRITE_NOT_MASKED = 0x0
    CHANGE_MASK_FOR_REGISTER_WRITE_MASKED = 0x1


class ENUM_CHANGE_MASK_FOR_LDPST(Enum):
    CHANGE_MASK_FOR_LDPST_NOT_MASKED = 0x0
    CHANGE_MASK_FOR_LDPST_MASKED = 0x1


class ENUM_HDR_MODE(Enum):
    HDR_MODE_DISABLE = 0x0
    HDR_MODE_ENABLE = 0x1


class ENUM_PIPE_GAMMA_INPUT_CLAMP_DISABLE(Enum):
    PIPE_GAMMA_INPUT_CLAMP_ENABLE = 0x0
    PIPE_GAMMA_INPUT_CLAMP_DISABLE = 0x1


class ENUM_YUV420_MODE(Enum):
    YUV420_MODE_BYPASS = 0x0
    YUV420_MODE_FULL_BLEND = 0x1


class ENUM_YUV420_ENABLE(Enum):
    YUV420_DISABLE = 0x0
    YUV420_ENABLE = 0x1


class ENUM_STEREO_MASK_PIPE_RENDER(Enum):
    STEREO_MASK_PIPE_RENDER_MASK_NONE = 0x0  # No masking. Report both the left and right eye vertical events.
    STEREO_MASK_PIPE_RENDER_MASK_LEFT = 0x1  # Mask the left eye vertical events. Only report right eye events.
    STEREO_MASK_PIPE_RENDER_MASK_RIGHT = 0x2  # Mask the right eye vertical events. Only report left eye events.


class ENUM_STEREO_MASK_PIPE_INT(Enum):
    STEREO_MASK_PIPE_INT_MASK_NONE = 0x0  # No masking. Report both the left and right eye vertical events.
    STEREO_MASK_PIPE_INT_MASK_LEFT = 0x1  # Mask the left eye vertical events. Only report right eye events.
    STEREO_MASK_PIPE_INT_MASK_RIGHT = 0x2  # Mask the right eye vertical events. Only report left eye events.


class OFFSET_PIPE_MISC:
    PIPE_MISC_A = 0x70030
    PIPE_MISC_B = 0x71030
    PIPE_MISC_C = 0x72030
    PIPE_MISC_D = 0x73030


class _PIPE_MISC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BfiEnable', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 1),
        ('DitheringType', ctypes.c_uint32, 2),
        ('DitheringEnable', ctypes.c_uint32, 1),
        ('PortOutputBpc', ctypes.c_uint32, 3),
        ('PixelRounding', ctypes.c_uint32, 1),
        ('PixelExtension', ctypes.c_uint32, 1),
        ('XvyccColorRangeLimit', ctypes.c_uint32, 1),
        ('PipeOutputColorSpaceSelect', ctypes.c_uint32, 1),
        ('OledCompensation', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 1),
        ('RotationInfo', ctypes.c_uint32, 2),
        ('OverrideBlueChannel', ctypes.c_uint32, 1),
        ('OverrideGreenChannel', ctypes.c_uint32, 1),
        ('OverrideRedChannel', ctypes.c_uint32, 1),
        ('OverridePipeOutput', ctypes.c_uint32, 1),
        ('ChangeMaskForVblankVsyncInt', ctypes.c_uint32, 1),
        ('ChangeMaskForRegisterWrite', ctypes.c_uint32, 1),
        ('ChangeMaskForLdpst', ctypes.c_uint32, 1),
        ('HdrMode', ctypes.c_uint32, 1),
        ('AllowDbStall', ctypes.c_uint32, 1),
        ('PipeGammaInputClampDisable', ctypes.c_uint32, 1),
        ('Yuv420Mode', ctypes.c_uint32, 1),
        ('Yuv420Enable', ctypes.c_uint32, 1),
        ('StereoMaskPipeRender', ctypes.c_uint32, 2),
        ('StereoMaskPipeInt', ctypes.c_uint32, 2),
    ]


class REG_PIPE_MISC(ctypes.Union):
    value = 0
    offset = 0

    BfiEnable = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 2
    DitheringType = 0  # bit 2 to 4
    DitheringEnable = 0  # bit 4 to 5
    PortOutputBpc = 0  # bit 5 to 8
    PixelRounding = 0  # bit 8 to 9
    PixelExtension = 0  # bit 9 to 10
    XvyccColorRangeLimit = 0  # bit 10 to 11
    PipeOutputColorSpaceSelect = 0  # bit 11 to 12
    OledCompensation = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 14
    RotationInfo = 0  # bit 14 to 16
    OverrideBlueChannel = 0  # bit 16 to 17
    OverrideGreenChannel = 0  # bit 17 to 18
    OverrideRedChannel = 0  # bit 18 to 19
    OverridePipeOutput = 0  # bit 19 to 20
    ChangeMaskForVblankVsyncInt = 0  # bit 20 to 21
    ChangeMaskForRegisterWrite = 0  # bit 21 to 22
    ChangeMaskForLdpst = 0  # bit 22 to 23
    HdrMode = 0  # bit 23 to 24
    AllowDbStall = 0  # bit 24 to 25
    PipeGammaInputClampDisable = 0  # bit 25 to 26
    Yuv420Mode = 0  # bit 26 to 27
    Yuv420Enable = 0  # bit 27 to 28
    StereoMaskPipeRender = 0  # bit 28 to 30
    StereoMaskPipeInt = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_MISC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_MISC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ASFU_FLIP_EXCEPTION(Enum):
    ASFU_FLIP_EXCEPTION_MASK = 0x1  # Add exception for Flip for global register update event and Pipe register update 
                                    # event.
    ASFU_FLIP_EXCEPTION_NO_MASK = 0x0  # Do not add exception for Flip for global register update event and Pipe regist
                                       # er update event.


class ENUM_YUV_422_MODE(Enum):
    YUV_422_MODE_DISABLE = 0x0
    YUV_422_MODE_ENABLE = 0x1


class ENUM_UNDERRUN_REPLACEMENT_PIXEL_VALUE(Enum):
    UNDERRUN_REPLACEMENT_PIXEL_VALUE_ALL_COLOR_CHANNELS_0 = 0x0  # All color channels forced to all 0's value.
    UNDERRUN_REPLACEMENT_PIXEL_VALUE_RED_AND_GREEN_0_BLUE_1 = 0x1  # Red and Green color channels forced to all 0's val
                                                                   # ue. Blue forced to all 1's.
    UNDERRUN_REPLACEMENT_PIXEL_VALUE_RED_AND_BLUE_0_GREEN_1 = 0x2  # Red and Blue color channels forced to all 0's valu
                                                                   # e. Green forced to all 1's.
    UNDERRUN_REPLACEMENT_PIXEL_VALUE_RED_0_GREEN_AND_BLUE_1 = 0x3  # Red color channel forced to all 0's value. Green a
                                                                   # nd Blue forced to all 1's.
    UNDERRUN_REPLACEMENT_PIXEL_VALUE_GREEN_AND_BLUE_0_RED_1 = 0x4  # Green and Blue color channels forced to all 0's va
                                                                   # lue. Red forced to all 1's.
    UNDERRUN_REPLACEMENT_PIXEL_VALUE_GREEN_0_RED_AND_BLUE_1 = 0x5  # Green color channel forced to all 0's value. Red a
                                                                   # nd Blue forced to all 1's.
    UNDERRUN_REPLACEMENT_PIXEL_VALUE_RED_AND_GREEN_1_BLUE_0 = 0x6  # Red and Green color channels forced to all 1's val
                                                                   # ue. Blue forced to all 0's.
    UNDERRUN_REPLACEMENT_PIXEL_VALUE_ALL_COLOR_CHANNELS_1 = 0x7  # Red, Green and Blue color channels forced to all 1's
                                                                 #  value.


class ENUM_UNDERRUN_MANUAL_PIXEL_OVERRIDE(Enum):
    UNDERRUN_MANUAL_PIXEL_OVERRIDE_HW_OVERRIDE_PIXEL = 0x0
    UNDERRUN_MANUAL_PIXEL_OVERRIDE_SW_MANUAL_OVERRIDE_PIXEL = 0x1


class OFFSET_PIPE_MISC2:
    PIPE_MISC2_A = 0x7002C
    PIPE_MISC2_B = 0x7102C
    PIPE_MISC2_C = 0x7202C
    PIPE_MISC2_D = 0x7302C


class _PIPE_MISC2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FlipInfoPlaneSelect', ctypes.c_uint32, 3),
        ('Reserved3', ctypes.c_uint32, 1),
        ('ScanlinePlaneSelect', ctypes.c_uint32, 3),
        ('Reserved7', ctypes.c_uint32, 1),
        ('AsfuFlipException', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 2),
        ('Yuv422Mode', ctypes.c_uint32, 1),
        ('IpcDemoteReqChunkSize', ctypes.c_uint32, 4),
        ('UnderrunReplacementPixelValue', ctypes.c_uint32, 3),
        ('UnderrunManualPixelOverride', ctypes.c_uint32, 1),
        ('Reserved20', ctypes.c_uint32, 4),
        ('UnderrunBubbleCounter', ctypes.c_uint32, 8),
    ]


class REG_PIPE_MISC2(ctypes.Union):
    value = 0
    offset = 0

    FlipInfoPlaneSelect = 0  # bit 0 to 3
    Reserved3 = 0  # bit 3 to 4
    ScanlinePlaneSelect = 0  # bit 4 to 7
    Reserved7 = 0  # bit 7 to 8
    AsfuFlipException = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 11
    Yuv422Mode = 0  # bit 11 to 12
    IpcDemoteReqChunkSize = 0  # bit 12 to 16
    UnderrunReplacementPixelValue = 0  # bit 16 to 19
    UnderrunManualPixelOverride = 0  # bit 19 to 20
    Reserved20 = 0  # bit 20 to 24
    UnderrunBubbleCounter = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_MISC2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_MISC2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_FLIPCNT:
    PIPE_FLIPCNT_A = 0x70044
    PIPE_FLIPCNT_B = 0x71044
    PIPE_FLIPCNT_C = 0x72044
    PIPE_FLIPCNT_D = 0x73044


class _PIPE_FLIPCNT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PipeFlipCounter', ctypes.c_uint32, 32),
    ]


class REG_PIPE_FLIPCNT(ctypes.Union):
    value = 0
    offset = 0

    PipeFlipCounter = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_FLIPCNT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_FLIPCNT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_FRMCNT:
    PIPE_FRMCNT_A = 0x70040
    PIPE_FRMCNT_B = 0x71040
    PIPE_FRMCNT_C = 0x72040
    PIPE_FRMCNT_D = 0x73040


class _PIPE_FRMCNT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PipeFrameCounter', ctypes.c_uint32, 32),
    ]


class REG_PIPE_FRMCNT(ctypes.Union):
    value = 0
    offset = 0

    PipeFrameCounter = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_FRMCNT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_FRMCNT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_FRMTMSTMP:
    PIPE_FRMTMSTMP_A = 0x70048
    PIPE_FRMTMSTMP_B = 0x71048
    PIPE_FRMTMSTMP_C = 0x72048
    PIPE_FRMTMSTMP_D = 0x73048


class _PIPE_FRMTMSTMP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PipeFrameTimeStamp', ctypes.c_uint32, 32),
    ]


class REG_PIPE_FRMTMSTMP(ctypes.Union):
    value = 0
    offset = 0

    PipeFrameTimeStamp = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_FRMTMSTMP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_FRMTMSTMP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_FLIPTMSTMP:
    PIPE_FLIPTMSTMP_A = 0x7004C
    PIPE_FLIPTMSTMP_B = 0x7104C
    PIPE_FLIPTMSTMP_C = 0x7204C
    PIPE_FLIPTMSTMP_D = 0x7304C


class _PIPE_FLIPTMSTMP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PipeFlipTimeStamp', ctypes.c_uint32, 32),
    ]


class REG_PIPE_FLIPTMSTMP(ctypes.Union):
    value = 0
    offset = 0

    PipeFlipTimeStamp = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_FLIPTMSTMP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_FLIPTMSTMP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_FLIPDONETMSTMP:
    PIPE_FLIPDONETMSTMP_A = 0x70054
    PIPE_FLIPDONETMSTMP_B = 0x71054
    PIPE_FLIPDONETMSTMP_C = 0x72054
    PIPE_FLIPDONETMSTMP_D = 0x73054


class _PIPE_FLIPDONETMSTMP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PipeFlipDoneTimeStamp', ctypes.c_uint32, 32),
    ]


class REG_PIPE_FLIPDONETMSTMP(ctypes.Union):
    value = 0
    offset = 0

    PipeFlipDoneTimeStamp = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_FLIPDONETMSTMP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_FLIPDONETMSTMP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_WM_LINETIME:
    WM_LINETIME_A = 0x45270
    WM_LINETIME_B = 0x45274
    WM_LINETIME_C = 0x45278
    WM_LINETIME_D = 0x4527C


class _WM_LINETIME(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LineTime', ctypes.c_uint32, 9),
        ('Reserved9', ctypes.c_uint32, 23),
    ]


class REG_WM_LINETIME(ctypes.Union):
    value = 0
    offset = 0

    LineTime = 0  # bit 0 to 9
    Reserved9 = 0  # bit 9 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _WM_LINETIME),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_WM_LINETIME, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_RENDER_RESPONSE_DESTINATION(Enum):
    RENDER_RESPONSE_DESTINATION_CS = 0x0  # Send scan line event response to CS
    RENDER_RESPONSE_DESTINATION_BCS = 0x1  # Send scan line event response to BCS


class ENUM_COUNTER_SELECT(Enum):
    COUNTER_SELECT_TIMING_GENERATOR = 0x0  # Use the scanline count from the pipe timing generator
    COUNTER_SELECT_PLANE = 0x1  # Use the scanline count from plane selected in PIPE_MISC2.


class ENUM_INCLUSIVE_EXCLUSIVE_SELECT(Enum):
    INCLUSIVE_EXCLUSIVE_SELECT_EXCLUSIVE = 0x0  # Exclusive mode: trigger scan line event when inside the scan line win
                                                # dow
    INCLUSIVE_EXCLUSIVE_SELECT_INCLUSIVE = 0x1  # Inclusive mode: trigger scan line event when outside the scan line wi
                                                # ndow


class ENUM_INITIATE_COMPARE(Enum):
    INITIATE_COMPARE_DO_NOTHING = 0x0
    INITIATE_COMPARE_INITIATE_COMPARE = 0x1


class OFFSET_PIPE_SCANLINECOMP:
    PIPE_SCANLINECOMP_A = 0x70004
    PIPE_SCANLINECOMP_B = 0x71004
    PIPE_SCANLINECOMP_C = 0x72004
    PIPE_SCANLINECOMP_D = 0x73004


class _PIPE_SCANLINECOMP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EndScanLine', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 2),
        ('RenderResponseDestination', ctypes.c_uint32, 1),
        ('StartScanLine', ctypes.c_uint32, 13),
        ('CounterSelect', ctypes.c_uint32, 1),
        ('InclusiveExclusiveSelect', ctypes.c_uint32, 1),
        ('InitiateCompare', ctypes.c_uint32, 1),
    ]


class REG_PIPE_SCANLINECOMP(ctypes.Union):
    value = 0
    offset = 0

    EndScanLine = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 15
    RenderResponseDestination = 0  # bit 15 to 16
    StartScanLine = 0  # bit 16 to 29
    CounterSelect = 0  # bit 29 to 30
    InclusiveExclusiveSelect = 0  # bit 30 to 31
    InitiateCompare = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_SCANLINECOMP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_SCANLINECOMP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CGE_WEIGHT:
    CGE_WEIGHT_A = 0x49090
    CGE_WEIGHT_B = 0x49190
    CGE_WEIGHT_C = 0x49290
    CGE_WEIGHT_D = 0x49390


class _CGE_WEIGHT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CgeWeightIndex0', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 2),
        ('CgeWeightIndex1', ctypes.c_uint32, 6),
        ('Reserved14', ctypes.c_uint32, 2),
        ('CgeWeightIndex2', ctypes.c_uint32, 6),
        ('Reserved22', ctypes.c_uint32, 2),
        ('CgeWeightIndex3', ctypes.c_uint32, 6),
        ('Reserved30', ctypes.c_uint32, 2),
        ('CgeWeightIndex4', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 2),
        ('CgeWeightIndex5', ctypes.c_uint32, 6),
        ('Reserved14', ctypes.c_uint32, 2),
        ('CgeWeightIndex6', ctypes.c_uint32, 6),
        ('Reserved22', ctypes.c_uint32, 2),
        ('CgeWeightIndex7', ctypes.c_uint32, 6),
        ('Reserved30', ctypes.c_uint32, 2),
        ('CgeWeightIndex8', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 2),
        ('CgeWeightIndex9', ctypes.c_uint32, 6),
        ('Reserved14', ctypes.c_uint32, 2),
        ('CgeWeightIndex10', ctypes.c_uint32, 6),
        ('Reserved22', ctypes.c_uint32, 2),
        ('CgeWeightIndex11', ctypes.c_uint32, 6),
        ('Reserved30', ctypes.c_uint32, 2),
        ('CgeWeightIndex12', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 2),
        ('CgeWeightIndex13', ctypes.c_uint32, 6),
        ('Reserved14', ctypes.c_uint32, 2),
        ('CgeWeightIndex14', ctypes.c_uint32, 6),
        ('Reserved22', ctypes.c_uint32, 2),
        ('CgeWeightIndex15', ctypes.c_uint32, 6),
        ('Reserved30', ctypes.c_uint32, 2),
        ('CgeWeightIndex16', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 26),
    ]


class REG_CGE_WEIGHT(ctypes.Union):
    value = 0
    offset = 0

    CgeWeightIndex0 = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 8
    CgeWeightIndex1 = 0  # bit 8 to 14
    Reserved14 = 0  # bit 14 to 16
    CgeWeightIndex2 = 0  # bit 16 to 22
    Reserved22 = 0  # bit 22 to 24
    CgeWeightIndex3 = 0  # bit 24 to 30
    Reserved30 = 0  # bit 30 to 32
    CgeWeightIndex4 = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 8
    CgeWeightIndex5 = 0  # bit 8 to 14
    Reserved14 = 0  # bit 14 to 16
    CgeWeightIndex6 = 0  # bit 16 to 22
    Reserved22 = 0  # bit 22 to 24
    CgeWeightIndex7 = 0  # bit 24 to 30
    Reserved30 = 0  # bit 30 to 32
    CgeWeightIndex8 = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 8
    CgeWeightIndex9 = 0  # bit 8 to 14
    Reserved14 = 0  # bit 14 to 16
    CgeWeightIndex10 = 0  # bit 16 to 22
    Reserved22 = 0  # bit 22 to 24
    CgeWeightIndex11 = 0  # bit 24 to 30
    Reserved30 = 0  # bit 30 to 32
    CgeWeightIndex12 = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 8
    CgeWeightIndex13 = 0  # bit 8 to 14
    Reserved14 = 0  # bit 14 to 16
    CgeWeightIndex14 = 0  # bit 16 to 22
    Reserved22 = 0  # bit 22 to 24
    CgeWeightIndex15 = 0  # bit 24 to 30
    Reserved30 = 0  # bit 30 to 32
    CgeWeightIndex16 = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CGE_WEIGHT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CGE_WEIGHT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DSC_VERSION_MINOR(Enum):
    DSC_VERSION_MINOR_DSC_1_1_BACKWARD_COMPATIBLE = 0x1
    DSC_VERSION_MINOR_DSC_1_2 = 0x2


class ENUM_BLOCK_PRED_ENABLE(Enum):
    BLOCK_PRED_DISABLE = 0x0  # BP is not used to code any groups within the picture
    BLOCK_PRED_ENABLE = 0x1  # Decoder must select between BP and MMAP


class ENUM_CONVERT_RGB(Enum):
    CONVERT_RGB_YCBCR = 0x0  # Color space is YCbCr
    CONVERT_RGB_CONVERT_RGB = 0x1  # Encoder converts RGB to YCoCg-R, and decoder converts YCoCg-R to RGB.


class ENUM_ENABLE_422(Enum):
    ENABLE_422_444 = 0x0  # Input uses 4:4:4 sampling. Decoder does not drop samples to reconstruct a 4:2:2 picture
    ENABLE_422_422 = 0x1  # Input uses 4:2:2 sampling. Decoder drops samples to reconstruct a 4:2:2 picture.


class ENUM_VBR_ENABLE(Enum):
    VBR_DISABLE = 0x0  # 0 padding bits are stuffed at the end of a slice to ensure that the total number of bit
                              # s within the slice is equal to the slice bit budget.
    VBR_ENABLE = 0x1  # Bit stuffing is bypassed


class ENUM_ALT_ICH_SELECT(Enum):
    ALT_ICH_SELECT_SELECT_ALT_ICH = 0x1  # This alternateICH method can be used only when the subversion is not equal t
                                         # o '1'.
    ALT_ICH_SELECT_DESELECT_ALT_ICH = 0x0  # This ICH method is always used when the subversion is equal to '1'.


class ENUM_NATIVE_420(Enum):
    NATIVE_420_NATIVE_420_NOT_USED = 0x0  # Native 420 mode is not used.
    NATIVE_420_NATIVE_420_USED = 0x1  # Native 420 mode is used. DSC encoder input is 420. To support native 420 mode, 
                                      # DSC encoder algorithms must work with 420 subsampled input pixels. DSC standard
                                      # versions prior to 1.2a do not support this mode.


class ENUM_NATIVE_422(Enum):
    NATIVE_422_NATIVE_422_NOT_USED = 0x0  # Native 422 mode is not used.
    NATIVE_422_NATIVE_422_USED = 0x1  # Native 422 mode is used. DSC encoder input is 422. To support native 422 mode, 
                                      # DSC encoder algorithms must work with 422 subsampled input pixels. DSC standard
                                      # versions prior to 1.2a do not support this mode.


class ENUM_NATIVE_422_ZERO_PADDING_CONTROL(Enum):
    NATIVE_422_ZERO_PADDING_CONTROL_NO_PADDING = 0x0  # No padding in native_422 mode.
    NATIVE_422_ZERO_PADDING_CONTROL_PAD_4_LSBS = 0x1  # Pad least significant 4 bits of each channel.
    NATIVE_422_ZERO_PADDING_CONTROL_PAD_2_LSBS = 0x2  # Pad least significant 2 bits of each channel.


class OFFSET_DSC_PICTURE_PARAMETER_SET_0:
    DSC_PICTURE_PARAMETER_SET_0_DSC0_PA = 0x78070
    DSC_PICTURE_PARAMETER_SET_0_DSC1_PA = 0x78170
    DSC_PICTURE_PARAMETER_SET_0_DSC0_PB = 0x78270
    DSC_PICTURE_PARAMETER_SET_0_DSC1_PB = 0x78370
    DSC_PICTURE_PARAMETER_SET_0_DSC0_PC = 0x78470
    DSC_PICTURE_PARAMETER_SET_0_DSC1_PC = 0x78570
    DSC_PICTURE_PARAMETER_SET_0_DSC0_PD = 0x78670
    DSC_PICTURE_PARAMETER_SET_0_DSC1_PD = 0x78770


class _DSC_PICTURE_PARAMETER_SET_0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dsc_Version_Major', ctypes.c_uint32, 4),
        ('Dsc_Version_Minor', ctypes.c_uint32, 4),
        ('Bits_Per_Component', ctypes.c_uint32, 4),
        ('Linebuf_Depth', ctypes.c_uint32, 4),
        ('Block_Pred_Enable', ctypes.c_uint32, 1),
        ('Convert_Rgb', ctypes.c_uint32, 1),
        ('Enable_422', ctypes.c_uint32, 1),
        ('Vbr_Enable', ctypes.c_uint32, 1),
        ('Alt_Ich_Select', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 1),
        ('Native_420', ctypes.c_uint32, 1),
        ('Native_422', ctypes.c_uint32, 1),
        ('Native_422ZeroPaddingControl', ctypes.c_uint32, 2),
        ('Reserved26', ctypes.c_uint32, 5),
        ('AllowDbStall', ctypes.c_uint32, 1),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_0(ctypes.Union):
    value = 0
    offset = 0

    Dsc_Version_Major = 0  # bit 0 to 4
    Dsc_Version_Minor = 0  # bit 4 to 8
    Bits_Per_Component = 0  # bit 8 to 12
    Linebuf_Depth = 0  # bit 12 to 16
    Block_Pred_Enable = 0  # bit 16 to 17
    Convert_Rgb = 0  # bit 17 to 18
    Enable_422 = 0  # bit 18 to 19
    Vbr_Enable = 0  # bit 19 to 20
    Alt_Ich_Select = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 22
    Native_420 = 0  # bit 22 to 23
    Native_422 = 0  # bit 23 to 24
    Native_422ZeroPaddingControl = 0  # bit 24 to 26
    Reserved26 = 0  # bit 26 to 31
    AllowDbStall = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_1:
    DSC_PICTURE_PARAMETER_SET_1_DSC0_PA = 0x78074
    DSC_PICTURE_PARAMETER_SET_1_DSC1_PA = 0x78174
    DSC_PICTURE_PARAMETER_SET_1_DSC0_PB = 0x78274
    DSC_PICTURE_PARAMETER_SET_1_DSC1_PB = 0x78374
    DSC_PICTURE_PARAMETER_SET_1_DSC0_PC = 0x78474
    DSC_PICTURE_PARAMETER_SET_1_DSC1_PC = 0x78574
    DSC_PICTURE_PARAMETER_SET_1_DSC0_PD = 0x78674
    DSC_PICTURE_PARAMETER_SET_1_DSC1_PD = 0x78774


class _DSC_PICTURE_PARAMETER_SET_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Bits_Per_Pixel', ctypes.c_uint32, 10),
        ('Reserved10', ctypes.c_uint32, 10),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_1(ctypes.Union):
    value = 0
    offset = 0

    Bits_Per_Pixel = 0  # bit 0 to 10
    Reserved10 = 0  # bit 10 to 20
    Reserved20 = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_2:
    DSC_PICTURE_PARAMETER_SET_2_DSC0_PA = 0x78078
    DSC_PICTURE_PARAMETER_SET_2_DSC1_PA = 0x78178
    DSC_PICTURE_PARAMETER_SET_2_DSC0_PB = 0x78278
    DSC_PICTURE_PARAMETER_SET_2_DSC1_PB = 0x78378
    DSC_PICTURE_PARAMETER_SET_2_DSC0_PC = 0x78478
    DSC_PICTURE_PARAMETER_SET_2_DSC1_PC = 0x78578
    DSC_PICTURE_PARAMETER_SET_2_DSC0_PD = 0x78678
    DSC_PICTURE_PARAMETER_SET_2_DSC1_PD = 0x78778


class _DSC_PICTURE_PARAMETER_SET_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Pic_Height', ctypes.c_uint32, 16),
        ('Pic_Width', ctypes.c_uint32, 16),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_2(ctypes.Union):
    value = 0
    offset = 0

    Pic_Height = 0  # bit 0 to 16
    Pic_Width = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_3:
    DSC_PICTURE_PARAMETER_SET_3_DSC0_PA = 0x7807C
    DSC_PICTURE_PARAMETER_SET_3_DSC1_PA = 0x7817C
    DSC_PICTURE_PARAMETER_SET_3_DSC0_PB = 0x7827C
    DSC_PICTURE_PARAMETER_SET_3_DSC1_PB = 0x7837C
    DSC_PICTURE_PARAMETER_SET_3_DSC0_PC = 0x7847C
    DSC_PICTURE_PARAMETER_SET_3_DSC1_PC = 0x7857C
    DSC_PICTURE_PARAMETER_SET_3_DSC0_PD = 0x7867C
    DSC_PICTURE_PARAMETER_SET_3_DSC1_PD = 0x7877C


class _DSC_PICTURE_PARAMETER_SET_3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Slice_Height', ctypes.c_uint32, 16),
        ('Slice_Width', ctypes.c_uint32, 16),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_3(ctypes.Union):
    value = 0
    offset = 0

    Slice_Height = 0  # bit 0 to 16
    Slice_Width = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_4:
    DSC_PICTURE_PARAMETER_SET_4_DSC0_PA = 0x78080
    DSC_PICTURE_PARAMETER_SET_4_DSC1_PA = 0x78180
    DSC_PICTURE_PARAMETER_SET_4_DSC0_PB = 0x78280
    DSC_PICTURE_PARAMETER_SET_4_DSC1_PB = 0x78380
    DSC_PICTURE_PARAMETER_SET_4_DSC0_PC = 0x78480
    DSC_PICTURE_PARAMETER_SET_4_DSC1_PC = 0x78580
    DSC_PICTURE_PARAMETER_SET_4_DSC0_PD = 0x78680
    DSC_PICTURE_PARAMETER_SET_4_DSC1_PD = 0x78780


class _DSC_PICTURE_PARAMETER_SET_4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Initial_Xmit_Delay', ctypes.c_uint32, 10),
        ('Reserved10', ctypes.c_uint32, 6),
        ('Initial_Dec_Delay', ctypes.c_uint32, 16),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_4(ctypes.Union):
    value = 0
    offset = 0

    Initial_Xmit_Delay = 0  # bit 0 to 10
    Reserved10 = 0  # bit 10 to 16
    Initial_Dec_Delay = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_4),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_5:
    DSC_PICTURE_PARAMETER_SET_5_DSC0_PA = 0x78084
    DSC_PICTURE_PARAMETER_SET_5_DSC1_PA = 0x78184
    DSC_PICTURE_PARAMETER_SET_5_DSC0_PB = 0x78284
    DSC_PICTURE_PARAMETER_SET_5_DSC1_PB = 0x78384
    DSC_PICTURE_PARAMETER_SET_5_DSC0_PC = 0x78484
    DSC_PICTURE_PARAMETER_SET_5_DSC1_PC = 0x78584
    DSC_PICTURE_PARAMETER_SET_5_DSC0_PD = 0x78684
    DSC_PICTURE_PARAMETER_SET_5_DSC1_PD = 0x78784


class _DSC_PICTURE_PARAMETER_SET_5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Scale_Increment_Interval', ctypes.c_uint32, 16),
        ('Scale_Decrement_Interval', ctypes.c_uint32, 12),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_5(ctypes.Union):
    value = 0
    offset = 0

    Scale_Increment_Interval = 0  # bit 0 to 16
    Scale_Decrement_Interval = 0  # bit 16 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_6:
    DSC_PICTURE_PARAMETER_SET_6_DSC0_PA = 0x78088
    DSC_PICTURE_PARAMETER_SET_6_DSC1_PA = 0x78188
    DSC_PICTURE_PARAMETER_SET_6_DSC0_PB = 0x78288
    DSC_PICTURE_PARAMETER_SET_6_DSC1_PB = 0x78388
    DSC_PICTURE_PARAMETER_SET_6_DSC0_PC = 0x78488
    DSC_PICTURE_PARAMETER_SET_6_DSC1_PC = 0x78588
    DSC_PICTURE_PARAMETER_SET_6_DSC0_PD = 0x78688
    DSC_PICTURE_PARAMETER_SET_6_DSC1_PD = 0x78788


class _DSC_PICTURE_PARAMETER_SET_6(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Initial_Scale_Value', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 2),
        ('First_Line_Bpg_Offset', ctypes.c_uint32, 5),
        ('Reserved13', ctypes.c_uint32, 3),
        ('Flatness_Min_Qp', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 3),
        ('Flatness_Max_Qp', ctypes.c_uint32, 5),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_6(ctypes.Union):
    value = 0
    offset = 0

    Initial_Scale_Value = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 8
    First_Line_Bpg_Offset = 0  # bit 8 to 13
    Reserved13 = 0  # bit 13 to 16
    Flatness_Min_Qp = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 24
    Flatness_Max_Qp = 0  # bit 24 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_6),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_6, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_7:
    DSC_PICTURE_PARAMETER_SET_7_DSC0_PA = 0x7808C
    DSC_PICTURE_PARAMETER_SET_7_DSC1_PA = 0x7818C
    DSC_PICTURE_PARAMETER_SET_7_DSC0_PB = 0x7828C
    DSC_PICTURE_PARAMETER_SET_7_DSC1_PB = 0x7838C
    DSC_PICTURE_PARAMETER_SET_7_DSC0_PC = 0x7848C
    DSC_PICTURE_PARAMETER_SET_7_DSC1_PC = 0x7858C
    DSC_PICTURE_PARAMETER_SET_7_DSC0_PD = 0x7868C
    DSC_PICTURE_PARAMETER_SET_7_DSC1_PD = 0x7878C


class _DSC_PICTURE_PARAMETER_SET_7(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Slice_Bpg_Offset', ctypes.c_uint32, 16),
        ('Nfl_Bpg_Offset', ctypes.c_uint32, 16),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_7(ctypes.Union):
    value = 0
    offset = 0

    Slice_Bpg_Offset = 0  # bit 0 to 16
    Nfl_Bpg_Offset = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_7),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_7, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_8:
    DSC_PICTURE_PARAMETER_SET_8_DSC0_PA = 0x78090
    DSC_PICTURE_PARAMETER_SET_8_DSC1_PA = 0x78190
    DSC_PICTURE_PARAMETER_SET_8_DSC0_PB = 0x78290
    DSC_PICTURE_PARAMETER_SET_8_DSC1_PB = 0x78390
    DSC_PICTURE_PARAMETER_SET_8_DSC0_PC = 0x78490
    DSC_PICTURE_PARAMETER_SET_8_DSC1_PC = 0x78590
    DSC_PICTURE_PARAMETER_SET_8_DSC0_PD = 0x78690
    DSC_PICTURE_PARAMETER_SET_8_DSC1_PD = 0x78790


class _DSC_PICTURE_PARAMETER_SET_8(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Final_Offset', ctypes.c_uint32, 16),
        ('Initial_Offset', ctypes.c_uint32, 16),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_8(ctypes.Union):
    value = 0
    offset = 0

    Final_Offset = 0  # bit 0 to 16
    Initial_Offset = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_8),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_8, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_9:
    DSC_PICTURE_PARAMETER_SET_9_DSC0_PA = 0x78094
    DSC_PICTURE_PARAMETER_SET_9_DSC1_PA = 0x78194
    DSC_PICTURE_PARAMETER_SET_9_DSC0_PB = 0x78294
    DSC_PICTURE_PARAMETER_SET_9_DSC1_PB = 0x78394
    DSC_PICTURE_PARAMETER_SET_9_DSC0_PC = 0x78494
    DSC_PICTURE_PARAMETER_SET_9_DSC1_PC = 0x78594
    DSC_PICTURE_PARAMETER_SET_9_DSC0_PD = 0x78694
    DSC_PICTURE_PARAMETER_SET_9_DSC1_PD = 0x78794


class _DSC_PICTURE_PARAMETER_SET_9(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Rc_Model_Size', ctypes.c_uint32, 16),
        ('Rc_Edge_Factor', ctypes.c_uint32, 4),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_9(ctypes.Union):
    value = 0
    offset = 0

    Rc_Model_Size = 0  # bit 0 to 16
    Rc_Edge_Factor = 0  # bit 16 to 20
    Reserved20 = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_9),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_9, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_10:
    DSC_PICTURE_PARAMETER_SET_10_DSC0_PA = 0x78098
    DSC_PICTURE_PARAMETER_SET_10_DSC1_PA = 0x78198
    DSC_PICTURE_PARAMETER_SET_10_DSC0_PB = 0x78298
    DSC_PICTURE_PARAMETER_SET_10_DSC1_PB = 0x78398
    DSC_PICTURE_PARAMETER_SET_10_DSC0_PC = 0x78498
    DSC_PICTURE_PARAMETER_SET_10_DSC1_PC = 0x78598
    DSC_PICTURE_PARAMETER_SET_10_DSC0_PD = 0x78698
    DSC_PICTURE_PARAMETER_SET_10_DSC1_PD = 0x78798


class _DSC_PICTURE_PARAMETER_SET_10(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Rc_Quant_Incr_Limit0', ctypes.c_uint32, 5),
        ('Reserved5', ctypes.c_uint32, 3),
        ('Rc_Quant_Incr_Limit1', ctypes.c_uint32, 5),
        ('Reserved13', ctypes.c_uint32, 3),
        ('Rc_Tgt_Offset_Hi', ctypes.c_uint32, 4),
        ('Rc_Tgt_Offset_Lo', ctypes.c_uint32, 4),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_10(ctypes.Union):
    value = 0
    offset = 0

    Rc_Quant_Incr_Limit0 = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 8
    Rc_Quant_Incr_Limit1 = 0  # bit 8 to 13
    Reserved13 = 0  # bit 13 to 16
    Rc_Tgt_Offset_Hi = 0  # bit 16 to 20
    Rc_Tgt_Offset_Lo = 0  # bit 20 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_10),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_10, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_11:
    DSC_PICTURE_PARAMETER_SET_11_DSC0_PA = 0x7809C
    DSC_PICTURE_PARAMETER_SET_11_DSC1_PA = 0x7819C
    DSC_PICTURE_PARAMETER_SET_11_DSC0_PB = 0x7829C
    DSC_PICTURE_PARAMETER_SET_11_DSC1_PB = 0x7839C
    DSC_PICTURE_PARAMETER_SET_11_DSC0_PC = 0x7849C
    DSC_PICTURE_PARAMETER_SET_11_DSC1_PC = 0x7859C
    DSC_PICTURE_PARAMETER_SET_11_DSC0_PD = 0x7869C
    DSC_PICTURE_PARAMETER_SET_11_DSC1_PD = 0x7879C


class _DSC_PICTURE_PARAMETER_SET_11(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 32),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_11(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_11),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_11, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_12:
    DSC_PICTURE_PARAMETER_SET_12_DSC0_PA = 0x780A0
    DSC_PICTURE_PARAMETER_SET_12_DSC1_PA = 0x781A0
    DSC_PICTURE_PARAMETER_SET_12_DSC0_PB = 0x782A0
    DSC_PICTURE_PARAMETER_SET_12_DSC1_PB = 0x783A0
    DSC_PICTURE_PARAMETER_SET_12_DSC0_PC = 0x784A0
    DSC_PICTURE_PARAMETER_SET_12_DSC1_PC = 0x785A0
    DSC_PICTURE_PARAMETER_SET_12_DSC0_PD = 0x786A0
    DSC_PICTURE_PARAMETER_SET_12_DSC1_PD = 0x787A0


class _DSC_PICTURE_PARAMETER_SET_12(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 32),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_12(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_12),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_12, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_13:
    DSC_PICTURE_PARAMETER_SET_13_DSC0_PA = 0x780A4
    DSC_PICTURE_PARAMETER_SET_13_DSC1_PA = 0x781A4
    DSC_PICTURE_PARAMETER_SET_13_DSC0_PB = 0x782A4
    DSC_PICTURE_PARAMETER_SET_13_DSC1_PB = 0x783A4
    DSC_PICTURE_PARAMETER_SET_13_DSC0_PC = 0x784A4
    DSC_PICTURE_PARAMETER_SET_13_DSC1_PC = 0x785A4
    DSC_PICTURE_PARAMETER_SET_13_DSC0_PD = 0x786A4
    DSC_PICTURE_PARAMETER_SET_13_DSC1_PD = 0x787A4


class _DSC_PICTURE_PARAMETER_SET_13(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 32),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_13(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_13),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_13, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_14:
    DSC_PICTURE_PARAMETER_SET_14_DSC0_PA = 0x780A8
    DSC_PICTURE_PARAMETER_SET_14_DSC1_PA = 0x781A8
    DSC_PICTURE_PARAMETER_SET_14_DSC0_PB = 0x782A8
    DSC_PICTURE_PARAMETER_SET_14_DSC1_PB = 0x783A8
    DSC_PICTURE_PARAMETER_SET_14_DSC0_PC = 0x784A8
    DSC_PICTURE_PARAMETER_SET_14_DSC1_PC = 0x785A8
    DSC_PICTURE_PARAMETER_SET_14_DSC0_PD = 0x786A8
    DSC_PICTURE_PARAMETER_SET_14_DSC1_PD = 0x787A8


class _DSC_PICTURE_PARAMETER_SET_14(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 32),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_14(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_14),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_14, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_15:
    DSC_PICTURE_PARAMETER_SET_15_DSC0_PA = 0x780AC
    DSC_PICTURE_PARAMETER_SET_15_DSC1_PA = 0x781AC
    DSC_PICTURE_PARAMETER_SET_15_DSC0_PB = 0x782AC
    DSC_PICTURE_PARAMETER_SET_15_DSC1_PB = 0x783AC
    DSC_PICTURE_PARAMETER_SET_15_DSC0_PC = 0x784AC
    DSC_PICTURE_PARAMETER_SET_15_DSC1_PC = 0x785AC
    DSC_PICTURE_PARAMETER_SET_15_DSC0_PD = 0x786AC
    DSC_PICTURE_PARAMETER_SET_15_DSC1_PD = 0x787AC


class _DSC_PICTURE_PARAMETER_SET_15(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 32),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_15(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_15),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_15, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_PICTURE_PARAMETER_SET_16:
    DSC_PICTURE_PARAMETER_SET_16_DSC0_PA = 0x780B0
    DSC_PICTURE_PARAMETER_SET_16_DSC1_PA = 0x781B0
    DSC_PICTURE_PARAMETER_SET_16_DSC0_PB = 0x782B0
    DSC_PICTURE_PARAMETER_SET_16_DSC1_PB = 0x783B0
    DSC_PICTURE_PARAMETER_SET_16_DSC0_PC = 0x784B0
    DSC_PICTURE_PARAMETER_SET_16_DSC1_PC = 0x785B0
    DSC_PICTURE_PARAMETER_SET_16_DSC0_PD = 0x786B0
    DSC_PICTURE_PARAMETER_SET_16_DSC1_PD = 0x787B0


class _DSC_PICTURE_PARAMETER_SET_16(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Slice_Chunk_Size', ctypes.c_uint32, 16),
        ('Slice_Per_Line', ctypes.c_uint32, 3),
        ('Reserved19', ctypes.c_uint32, 1),
        ('Slice_Row_Per_Frame', ctypes.c_uint32, 12),
    ]


class REG_DSC_PICTURE_PARAMETER_SET_16(ctypes.Union):
    value = 0
    offset = 0

    Slice_Chunk_Size = 0  # bit 0 to 16
    Slice_Per_Line = 0  # bit 16 to 19
    Reserved19 = 0  # bit 19 to 20
    Slice_Row_Per_Frame = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_PICTURE_PARAMETER_SET_16),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_PICTURE_PARAMETER_SET_16, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_RC_BUF_THRESH_0:
    DSC_RC_BUF_THRESH_0_DSC0_PA = 0x78054
    DSC_RC_BUF_THRESH_0_DSC1_PA = 0x78154
    DSC_RC_BUF_THRESH_0_DSC0_PB = 0x78254
    DSC_RC_BUF_THRESH_0_DSC1_PB = 0x78354
    DSC_RC_BUF_THRESH_0_DSC0_PC = 0x78454
    DSC_RC_BUF_THRESH_0_DSC1_PC = 0x78554
    DSC_RC_BUF_THRESH_0_DSC0_PD = 0x78654
    DSC_RC_BUF_THRESH_0_DSC1_PD = 0x78754


class _DSC_RC_BUF_THRESH_0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Rc_Buf_Thresh_0', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_1', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_2', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_3', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_4', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_5', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_6', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_7', ctypes.c_uint32, 8),
    ]


class REG_DSC_RC_BUF_THRESH_0(ctypes.Union):
    value = 0
    offset = 0

    Rc_Buf_Thresh_0 = 0  # bit 0 to 8
    Rc_Buf_Thresh_1 = 0  # bit 8 to 16
    Rc_Buf_Thresh_2 = 0  # bit 16 to 24
    Rc_Buf_Thresh_3 = 0  # bit 24 to 32
    Rc_Buf_Thresh_4 = 0  # bit 0 to 8
    Rc_Buf_Thresh_5 = 0  # bit 8 to 16
    Rc_Buf_Thresh_6 = 0  # bit 16 to 24
    Rc_Buf_Thresh_7 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_RC_BUF_THRESH_0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_RC_BUF_THRESH_0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_RC_BUF_THRESH_1:
    DSC_RC_BUF_THRESH_1_DSC0_PA = 0x7805C
    DSC_RC_BUF_THRESH_1_DSC1_PA = 0x7815C
    DSC_RC_BUF_THRESH_1_DSC0_PB = 0x7825C
    DSC_RC_BUF_THRESH_1_DSC1_PB = 0x7835C
    DSC_RC_BUF_THRESH_1_DSC0_PC = 0x7845C
    DSC_RC_BUF_THRESH_1_DSC1_PC = 0x7855C
    DSC_RC_BUF_THRESH_1_DSC0_PD = 0x7865C
    DSC_RC_BUF_THRESH_1_DSC1_PD = 0x7875C


class _DSC_RC_BUF_THRESH_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Rc_Buf_Thresh_8', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_9', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_10', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_11', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_12', ctypes.c_uint32, 8),
        ('Rc_Buf_Thresh_13', ctypes.c_uint32, 8),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_DSC_RC_BUF_THRESH_1(ctypes.Union):
    value = 0
    offset = 0

    Rc_Buf_Thresh_8 = 0  # bit 0 to 8
    Rc_Buf_Thresh_9 = 0  # bit 8 to 16
    Rc_Buf_Thresh_10 = 0  # bit 16 to 24
    Rc_Buf_Thresh_11 = 0  # bit 24 to 32
    Rc_Buf_Thresh_12 = 0  # bit 0 to 8
    Rc_Buf_Thresh_13 = 0  # bit 8 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_RC_BUF_THRESH_1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_RC_BUF_THRESH_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_RC_RANGE_PARAMETERS_0:
    DSC_RC_RANGE_PARAMETERS_0_DSC0_PA = 0x78008
    DSC_RC_RANGE_PARAMETERS_0_DSC1_PA = 0x78108
    DSC_RC_RANGE_PARAMETERS_0_DSC0_PB = 0x78208
    DSC_RC_RANGE_PARAMETERS_0_DSC1_PB = 0x78308
    DSC_RC_RANGE_PARAMETERS_0_DSC0_PC = 0x78408
    DSC_RC_RANGE_PARAMETERS_0_DSC1_PC = 0x78508
    DSC_RC_RANGE_PARAMETERS_0_DSC0_PD = 0x78608
    DSC_RC_RANGE_PARAMETERS_0_DSC1_PD = 0x78708


class _DSC_RC_RANGE_PARAMETERS_0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Rc_Min_Qp_0', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_0', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_0', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_1', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_1', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_1', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_2', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_2', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_2', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_3', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_3', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_3', ctypes.c_uint32, 6),
    ]


class REG_DSC_RC_RANGE_PARAMETERS_0(ctypes.Union):
    value = 0
    offset = 0

    Rc_Min_Qp_0 = 0  # bit 0 to 5
    Rc_Max_Qp_0 = 0  # bit 5 to 10
    Rc_Bpg_Offset_0 = 0  # bit 10 to 16
    Rc_Min_Qp_1 = 0  # bit 16 to 21
    Rc_Max_Qp_1 = 0  # bit 21 to 26
    Rc_Bpg_Offset_1 = 0  # bit 26 to 32
    Rc_Min_Qp_2 = 0  # bit 0 to 5
    Rc_Max_Qp_2 = 0  # bit 5 to 10
    Rc_Bpg_Offset_2 = 0  # bit 10 to 16
    Rc_Min_Qp_3 = 0  # bit 16 to 21
    Rc_Max_Qp_3 = 0  # bit 21 to 26
    Rc_Bpg_Offset_3 = 0  # bit 26 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_RC_RANGE_PARAMETERS_0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_RC_RANGE_PARAMETERS_0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_RC_RANGE_PARAMETERS_1:
    DSC_RC_RANGE_PARAMETERS_1_DSC0_PA = 0x78010
    DSC_RC_RANGE_PARAMETERS_1_DSC1_PA = 0x78110
    DSC_RC_RANGE_PARAMETERS_1_DSC0_PB = 0x78210
    DSC_RC_RANGE_PARAMETERS_1_DSC1_PB = 0x78310
    DSC_RC_RANGE_PARAMETERS_1_DSC0_PC = 0x78410
    DSC_RC_RANGE_PARAMETERS_1_DSC1_PC = 0x78510
    DSC_RC_RANGE_PARAMETERS_1_DSC0_PD = 0x78610
    DSC_RC_RANGE_PARAMETERS_1_DSC1_PD = 0x78710


class _DSC_RC_RANGE_PARAMETERS_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Rc_Min_Qp_4', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_4', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_4', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_5', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_5', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_5', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_6', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_6', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_6', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_7', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_7', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_7', ctypes.c_uint32, 6),
    ]


class REG_DSC_RC_RANGE_PARAMETERS_1(ctypes.Union):
    value = 0
    offset = 0

    Rc_Min_Qp_4 = 0  # bit 0 to 5
    Rc_Max_Qp_4 = 0  # bit 5 to 10
    Rc_Bpg_Offset_4 = 0  # bit 10 to 16
    Rc_Min_Qp_5 = 0  # bit 16 to 21
    Rc_Max_Qp_5 = 0  # bit 21 to 26
    Rc_Bpg_Offset_5 = 0  # bit 26 to 32
    Rc_Min_Qp_6 = 0  # bit 0 to 5
    Rc_Max_Qp_6 = 0  # bit 5 to 10
    Rc_Bpg_Offset_6 = 0  # bit 10 to 16
    Rc_Min_Qp_7 = 0  # bit 16 to 21
    Rc_Max_Qp_7 = 0  # bit 21 to 26
    Rc_Bpg_Offset_7 = 0  # bit 26 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_RC_RANGE_PARAMETERS_1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_RC_RANGE_PARAMETERS_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_RC_RANGE_PARAMETERS_2:
    DSC_RC_RANGE_PARAMETERS_2_DSC0_PA = 0x78018
    DSC_RC_RANGE_PARAMETERS_2_DSC1_PA = 0x78118
    DSC_RC_RANGE_PARAMETERS_2_DSC0_PB = 0x78218
    DSC_RC_RANGE_PARAMETERS_2_DSC1_PB = 0x78318
    DSC_RC_RANGE_PARAMETERS_2_DSC0_PC = 0x78418
    DSC_RC_RANGE_PARAMETERS_2_DSC1_PC = 0x78518
    DSC_RC_RANGE_PARAMETERS_2_DSC0_PD = 0x78618
    DSC_RC_RANGE_PARAMETERS_2_DSC1_PD = 0x78718


class _DSC_RC_RANGE_PARAMETERS_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Rc_Min_Qp_8', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_8', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_8', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_9', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_9', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_9', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_10', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_10', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_10', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_11', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_11', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_11', ctypes.c_uint32, 6),
    ]


class REG_DSC_RC_RANGE_PARAMETERS_2(ctypes.Union):
    value = 0
    offset = 0

    Rc_Min_Qp_8 = 0  # bit 0 to 5
    Rc_Max_Qp_8 = 0  # bit 5 to 10
    Rc_Bpg_Offset_8 = 0  # bit 10 to 16
    Rc_Min_Qp_9 = 0  # bit 16 to 21
    Rc_Max_Qp_9 = 0  # bit 21 to 26
    Rc_Bpg_Offset_9 = 0  # bit 26 to 32
    Rc_Min_Qp_10 = 0  # bit 0 to 5
    Rc_Max_Qp_10 = 0  # bit 5 to 10
    Rc_Bpg_Offset_10 = 0  # bit 10 to 16
    Rc_Min_Qp_11 = 0  # bit 16 to 21
    Rc_Max_Qp_11 = 0  # bit 21 to 26
    Rc_Bpg_Offset_11 = 0  # bit 26 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_RC_RANGE_PARAMETERS_2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_RC_RANGE_PARAMETERS_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSC_RC_RANGE_PARAMETERS_3:
    DSC_RC_RANGE_PARAMETERS_3_DSC0_PA = 0x78020
    DSC_RC_RANGE_PARAMETERS_3_DSC1_PA = 0x78120
    DSC_RC_RANGE_PARAMETERS_3_DSC0_PB = 0x78220
    DSC_RC_RANGE_PARAMETERS_3_DSC1_PB = 0x78320
    DSC_RC_RANGE_PARAMETERS_3_DSC0_PC = 0x78420
    DSC_RC_RANGE_PARAMETERS_3_DSC1_PC = 0x78520
    DSC_RC_RANGE_PARAMETERS_3_DSC0_PD = 0x78620
    DSC_RC_RANGE_PARAMETERS_3_DSC1_PD = 0x78720


class _DSC_RC_RANGE_PARAMETERS_3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Rc_Min_Qp_12', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_12', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_12', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_13', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_13', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_13', ctypes.c_uint32, 6),
        ('Rc_Min_Qp_14', ctypes.c_uint32, 5),
        ('Rc_Max_Qp_14', ctypes.c_uint32, 5),
        ('Rc_Bpg_Offset_14', ctypes.c_uint32, 6),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_DSC_RC_RANGE_PARAMETERS_3(ctypes.Union):
    value = 0
    offset = 0

    Rc_Min_Qp_12 = 0  # bit 0 to 5
    Rc_Max_Qp_12 = 0  # bit 5 to 10
    Rc_Bpg_Offset_12 = 0  # bit 10 to 16
    Rc_Min_Qp_13 = 0  # bit 16 to 21
    Rc_Max_Qp_13 = 0  # bit 21 to 26
    Rc_Bpg_Offset_13 = 0  # bit 26 to 32
    Rc_Min_Qp_14 = 0  # bit 0 to 5
    Rc_Max_Qp_14 = 0  # bit 5 to 10
    Rc_Bpg_Offset_14 = 0  # bit 10 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_RC_RANGE_PARAMETERS_3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_RC_RANGE_PARAMETERS_3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_OVERFLOW_AVOID_CFG(Enum):
    OVERFLOW_AVOID_CFG_DSC_D1_8_DRAFT_IMPLEMENTATION = 0x0
    OVERFLOW_AVOID_CFG_VESA_PROPOSED_OPTION_2 = 0x2
    OVERFLOW_AVOID_CFG_VESA_PROPOSED_OPTION_3 = 0x3


class OFFSET_DSC_CHICKEN_1:
    DSC_CHICKEN_1_DSC0_PA = 0x78028
    DSC_CHICKEN_1_DSC1_PA = 0x78128
    DSC_CHICKEN_1_DSC0_PB = 0x78228
    DSC_CHICKEN_1_DSC1_PB = 0x78328
    DSC_CHICKEN_1_DSC0_PC = 0x78428
    DSC_CHICKEN_1_DSC1_PC = 0x78528
    DSC_CHICKEN_1_DSC0_PD = 0x78628
    DSC_CHICKEN_1_DSC1_PD = 0x78728


class _DSC_CHICKEN_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dsc_Noa', ctypes.c_uint32, 3),
        ('Spare3', ctypes.c_uint32, 1),
        ('Spare4', ctypes.c_uint32, 1),
        ('Spare5', ctypes.c_uint32, 1),
        ('Spare6', ctypes.c_uint32, 1),
        ('Spare7', ctypes.c_uint32, 1),
        ('Spare8', ctypes.c_uint32, 1),
        ('Spare9', ctypes.c_uint32, 1),
        ('Spare10', ctypes.c_uint32, 1),
        ('Spare11', ctypes.c_uint32, 1),
        ('Spare12', ctypes.c_uint32, 1),
        ('Spare13', ctypes.c_uint32, 1),
        ('Spare14', ctypes.c_uint32, 1),
        ('Spare15', ctypes.c_uint32, 1),
        ('Spare16', ctypes.c_uint32, 1),
        ('Spare17', ctypes.c_uint32, 1),
        ('Spare18', ctypes.c_uint32, 1),
        ('Spare19', ctypes.c_uint32, 1),
        ('Spare20', ctypes.c_uint32, 1),
        ('Spare21', ctypes.c_uint32, 1),
        ('Spare22', ctypes.c_uint32, 1),
        ('Spare23', ctypes.c_uint32, 1),
        ('Spare24', ctypes.c_uint32, 1),
        ('Spare25', ctypes.c_uint32, 1),
        ('Spare26', ctypes.c_uint32, 1),
        ('Spare27', ctypes.c_uint32, 1),
        ('Spare28', ctypes.c_uint32, 1),
        ('Spare29', ctypes.c_uint32, 1),
        ('OverflowAvoidCfg', ctypes.c_uint32, 2),
    ]


class REG_DSC_CHICKEN_1(ctypes.Union):
    value = 0
    offset = 0

    Dsc_Noa = 0  # bit 0 to 3
    Spare3 = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
    Spare7 = 0  # bit 7 to 8
    Spare8 = 0  # bit 8 to 9
    Spare9 = 0  # bit 9 to 10
    Spare10 = 0  # bit 10 to 11
    Spare11 = 0  # bit 11 to 12
    Spare12 = 0  # bit 12 to 13
    Spare13 = 0  # bit 13 to 14
    Spare14 = 0  # bit 14 to 15
    Spare15 = 0  # bit 15 to 16
    Spare16 = 0  # bit 16 to 17
    Spare17 = 0  # bit 17 to 18
    Spare18 = 0  # bit 18 to 19
    Spare19 = 0  # bit 19 to 20
    Spare20 = 0  # bit 20 to 21
    Spare21 = 0  # bit 21 to 22
    Spare22 = 0  # bit 22 to 23
    Spare23 = 0  # bit 23 to 24
    Spare24 = 0  # bit 24 to 25
    Spare25 = 0  # bit 25 to 26
    Spare26 = 0  # bit 26 to 27
    Spare27 = 0  # bit 27 to 28
    Spare28 = 0  # bit 28 to 29
    Spare29 = 0  # bit 29 to 30
    OverflowAvoidCfg = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSC_CHICKEN_1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSC_CHICKEN_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_UNCOMPRESSED_JOINER_SLAVE(Enum):
    UNCOMPRESSED_JOINER_SLAVE_NOT_SLAVE = 0x0
    UNCOMPRESSED_JOINER_SLAVE_SLAVE = 0x1


class ENUM_UNCOMPRESSED_JOINER_MASTER(Enum):
    UNCOMPRESSED_JOINER_MASTER_NOT_MASTER = 0x0
    UNCOMPRESSED_JOINER_MASTER_MASTER = 0x1


class ENUM_DUAL_LINK_MODE(Enum):
    DUAL_LINK_MODE_FRONTBACK_MODE = 0x0
    DUAL_LINK_MODE_INTERLEAVE_MODE = 0x1


class ENUM_SPLITTER_CONFIGURATION(Enum):
    SPLITTER_CONFIGURATION_2SEGMENT = 0x0
    SPLITTER_CONFIGURATION_4SEGMENT = 0x1


class ENUM_MASTER_BIG_JOINER_ENABLE(Enum):
    MASTER_BIG_JOINER_ENABLE_SLAVE = 0x0
    MASTER_BIG_JOINER_ENABLE_MASTER = 0x1


class ENUM_BIG_JOINER_ENABLE(Enum):
    BIG_JOINER_DISABLE = 0x0
    BIG_JOINER_ENABLE = 0x1


class ENUM_JOINER_ENABLE(Enum):
    JOINER_DISABLE = 0x0
    JOINER_ENABLE = 0x1


class ENUM_SPLITTER_ENABLE(Enum):
    SPLITTER_DISABLE = 0x0
    SPLITTER_ENABLE = 0x1


class OFFSET_PIPE_DSS_CTL1:
    PIPE_DSS_CTL1_PA = 0x78000
    PIPE_DSS_CTL1_PB = 0x78200
    PIPE_DSS_CTL1_PC = 0x78400
    PIPE_DSS_CTL1_PD = 0x78600


class _PIPE_DSS_CTL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LeftDlBufferTargetDepth', ctypes.c_uint32, 12),
        ('Reserved12', ctypes.c_uint32, 4),
        ('Overlap', ctypes.c_uint32, 4),
        ('UncompressedJoinerSlave', ctypes.c_uint32, 1),
        ('UncompressedJoinerMaster', ctypes.c_uint32, 1),
        ('Reserved22', ctypes.c_uint32, 2),
        ('DualLinkMode', ctypes.c_uint32, 1),
        ('SplitterConfiguration', ctypes.c_uint32, 2),
        ('VgaCenteringEnable', ctypes.c_uint32, 1),
        ('Master_Big_Joiner_Enable', ctypes.c_uint32, 1),
        ('Big_Joiner_Enable', ctypes.c_uint32, 1),
        ('JoinerEnable', ctypes.c_uint32, 1),
        ('SplitterEnable', ctypes.c_uint32, 1),
    ]


class REG_PIPE_DSS_CTL1(ctypes.Union):
    value = 0
    offset = 0

    LeftDlBufferTargetDepth = 0  # bit 0 to 12
    Reserved12 = 0  # bit 12 to 16
    Overlap = 0  # bit 16 to 20
    UncompressedJoinerSlave = 0  # bit 20 to 21
    UncompressedJoinerMaster = 0  # bit 21 to 22
    Reserved22 = 0  # bit 22 to 24
    DualLinkMode = 0  # bit 24 to 25
    SplitterConfiguration = 0  # bit 25 to 27
    VgaCenteringEnable = 0  # bit 27 to 28
    Master_Big_Joiner_Enable = 0  # bit 28 to 29
    Big_Joiner_Enable = 0  # bit 29 to 30
    JoinerEnable = 0  # bit 30 to 31
    SplitterEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_DSS_CTL1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_DSS_CTL1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_RIGHT_BRANCH_VDSC_ENABLE(Enum):
    RIGHT_BRANCH_VDSC_DISABLE = 0x0
    RIGHT_BRANCH_VDSC_ENABLE = 0x1


class ENUM_LEFT_BRANCH_VDSC_ENABLE(Enum):
    LEFT_BRANCH_VDSC_DISABLE = 0x0
    LEFT_BRANCH_VDSC_ENABLE = 0x1


class OFFSET_PIPE_DSS_CTL2:
    PIPE_DSS_CTL2_PA = 0x78004
    PIPE_DSS_CTL2_PB = 0x78204
    PIPE_DSS_CTL2_PC = 0x78404
    PIPE_DSS_CTL2_PD = 0x78604


class _PIPE_DSS_CTL2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RightDlBufferTargetDepth', ctypes.c_uint32, 12),
        ('Spare12', ctypes.c_uint32, 1),
        ('Spare13', ctypes.c_uint32, 1),
        ('Spare14', ctypes.c_uint32, 1),
        ('RightBranchVdscEnable', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 2),
        ('Reserved19', ctypes.c_uint32, 4),
        ('Reserved23', ctypes.c_uint32, 1),
        ('Spare24', ctypes.c_uint32, 1),
        ('Spare25', ctypes.c_uint32, 1),
        ('Spare26', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 3),
        ('Reserved30', ctypes.c_uint32, 1),
        ('LeftBranchVdscEnable', ctypes.c_uint32, 1),
    ]


class REG_PIPE_DSS_CTL2(ctypes.Union):
    value = 0
    offset = 0

    RightDlBufferTargetDepth = 0  # bit 0 to 12
    Spare12 = 0  # bit 12 to 13
    Spare13 = 0  # bit 13 to 14
    Spare14 = 0  # bit 14 to 15
    RightBranchVdscEnable = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 19
    Reserved19 = 0  # bit 19 to 23
    Reserved23 = 0  # bit 23 to 24
    Spare24 = 0  # bit 24 to 25
    Spare25 = 0  # bit 25 to 26
    Spare26 = 0  # bit 26 to 27
    Reserved27 = 0  # bit 27 to 30
    Reserved30 = 0  # bit 30 to 31
    LeftBranchVdscEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_DSS_CTL2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_DSS_CTL2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GAMMA_MODE(Enum):
    GAMMA_MODE_8_BIT = 0x0  # 8-bit Legacy Palette Mode
    GAMMA_MODE_10_BIT = 0x1  # 10-bit Precision Palette Mode
    GAMMA_MODE_12_BIT = 0x2  # 12-bit Interpolated Gamma Mode
    GAMMA_MODE_12_BIT_LOGARITHMIC = 0x3  # 12-bit Logarithmic Gamma Mode


class ENUM_GAMMA_MODE_CC2(Enum):
    GAMMA_MODE_CC2_10_BIT = 0x1  # 10-bit Precision Palette Mode
    GAMMA_MODE_CC2_12_BIT = 0x2  # 12-bit Interpolated Gamma Mode
    GAMMA_MODE_CC2_12_BIT_LOGARITHMIC = 0x3  # 12-bit Logarithmic Gamma Mode


class ENUM_PALETTE_ANTICOL_DIS(Enum):
    PALETTE_ANTICOL_DIS_ENABLE = 0x0
    PALETTE_ANTICOL_DIS_DISABLE = 0x1


class ENUM_POST_CSC_CC2_DITHERING_ENABLE(Enum):
    POST_CSC_CC2_DITHERING_DISABLED = 0x0
    POST_CSC_CC2_DITHERING_ENABLED = 0x1


class ENUM_POST_CSC_CC1_DITHERING_ENABLE(Enum):
    POST_CSC_CC1_DITHERING_DISABLED = 0x0
    POST_CSC_CC1_DITHERING_ENABLED = 0x1


class ENUM_POST_CSC_CC2_GAMMA_ENABLE(Enum):
    POST_CSC_CC2_GAMMA_ENABLE = 0x1
    POST_CSC_CC2_GAMMA_DISABLE = 0x0


class ENUM_PRE_CSC_CC2_GAMMA_ENABLE(Enum):
    PRE_CSC_CC2_GAMMA_ENABLE = 0x1
    PRE_CSC_CC2_GAMMA_DISABLE = 0x0


class ENUM_POST_CSC_GAMMA_ENABLE(Enum):
    POST_CSC_GAMMA_ENABLE = 0x1
    POST_CSC_GAMMA_DISABLE = 0x0


class ENUM_PRE_CSC_GAMMA_ENABLE(Enum):
    PRE_CSC_GAMMA_ENABLE = 0x1
    PRE_CSC_GAMMA_DISABLE = 0x0


class OFFSET_GAMMA_MODE:
    GAMMA_MODE_A = 0x4A480
    GAMMA_MODE_B = 0x4AC80
    GAMMA_MODE_C = 0x4B480
    GAMMA_MODE_D = 0x4BC80


class _GAMMA_MODE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaMode', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('GammaModeCc2', ctypes.c_uint32, 2),
        ('Reserved5', ctypes.c_uint32, 10),
        ('PaletteAnticolDis', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 9),
        ('PostCscCc2DitheringEnable', ctypes.c_uint32, 1),
        ('PostCscCc1DitheringEnable', ctypes.c_uint32, 1),
        ('PostCscCc2GammaEnable', ctypes.c_uint32, 1),
        ('PreCscCc2GammaEnable', ctypes.c_uint32, 1),
        ('AllowDbStall', ctypes.c_uint32, 1),
        ('PostCscGammaEnable', ctypes.c_uint32, 1),
        ('PreCscGammaEnable', ctypes.c_uint32, 1),
    ]


class REG_GAMMA_MODE(ctypes.Union):
    value = 0
    offset = 0

    GammaMode = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    GammaModeCc2 = 0  # bit 3 to 5
    Reserved5 = 0  # bit 5 to 15
    PaletteAnticolDis = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 25
    PostCscCc2DitheringEnable = 0  # bit 25 to 26
    PostCscCc1DitheringEnable = 0  # bit 26 to 27
    PostCscCc2GammaEnable = 0  # bit 27 to 28
    PreCscCc2GammaEnable = 0  # bit 28 to 29
    AllowDbStall = 0  # bit 29 to 30
    PostCscGammaEnable = 0  # bit 30 to 31
    PreCscGammaEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GAMMA_MODE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GAMMA_MODE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PAL_PREC_INDEX:
    PAL_PREC_INDEX_A = 0x4A400
    PAL_PREC_INDEX_B = 0x4AC00
    PAL_PREC_INDEX_C = 0x4B400
    PAL_PREC_INDEX_D = 0x4BC00


class _PAL_PREC_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 10),
        ('Reserved10', ctypes.c_uint32, 5),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_PAL_PREC_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 10
    Reserved10 = 0  # bit 10 to 15
    IndexAutoIncrement = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PAL_PREC_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PAL_PREC_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PAL_PREC_DATA:
    PAL_PREC_DATA_A = 0x4A404
    PAL_PREC_DATA_B = 0x4AC04
    PAL_PREC_DATA_C = 0x4B404
    PAL_PREC_DATA_D = 0x4BC04


class _PAL_PREC_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BluePrecisionPaletteEntry', ctypes.c_uint32, 10),
        ('GreenPrecisionPaletteEntry', ctypes.c_uint32, 10),
        ('RedPrecisionPaletteEntry', ctypes.c_uint32, 10),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PAL_PREC_DATA(ctypes.Union):
    value = 0
    offset = 0

    BluePrecisionPaletteEntry = 0  # bit 0 to 10
    GreenPrecisionPaletteEntry = 0  # bit 10 to 20
    RedPrecisionPaletteEntry = 0  # bit 20 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PAL_PREC_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PAL_PREC_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PAL_GC_MAX:
    PAL_GC_MAX_A = 0x4A410
    PAL_GC_MAX_CC2_A = 0x4A548
    PAL_GC_MAX_B = 0x4AC10
    PAL_GC_MAX_CC2_B = 0x4AD48
    PAL_GC_MAX_C = 0x4B410
    PAL_GC_MAX_D = 0x4BC10


class _PAL_GC_MAX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RedMaxGcPoint', ctypes.c_uint32, 17),
        ('Reserved17', ctypes.c_uint32, 15),
        ('GreenMaxGcPoint', ctypes.c_uint32, 17),
        ('Reserved17', ctypes.c_uint32, 15),
        ('BlueMaxGcPoint', ctypes.c_uint32, 17),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_PAL_GC_MAX(ctypes.Union):
    value = 0
    offset = 0

    RedMaxGcPoint = 0  # bit 0 to 17
    Reserved17 = 0  # bit 17 to 32
    GreenMaxGcPoint = 0  # bit 0 to 17
    Reserved17 = 0  # bit 17 to 32
    BlueMaxGcPoint = 0  # bit 0 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PAL_GC_MAX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PAL_GC_MAX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PAL_EXT_GC_MAX:
    PAL_EXT_GC_MAX_A = 0x4A420
    PAL_EXT_GC_MAX_B = 0x4AC20
    PAL_EXT_GC_MAX_C = 0x4B420
    PAL_EXT_GC_MAX_D = 0x4BC20


class _PAL_EXT_GC_MAX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RedExtMaxGcPoint', ctypes.c_uint32, 19),
        ('Reserved19', ctypes.c_uint32, 13),
        ('GreenExtMaxGcPoint', ctypes.c_uint32, 19),
        ('Reserved19', ctypes.c_uint32, 13),
        ('BlueExtMaxGcPoint', ctypes.c_uint32, 19),
        ('Reserved19', ctypes.c_uint32, 13),
    ]


class REG_PAL_EXT_GC_MAX(ctypes.Union):
    value = 0
    offset = 0

    RedExtMaxGcPoint = 0  # bit 0 to 19
    Reserved19 = 0  # bit 19 to 32
    GreenExtMaxGcPoint = 0  # bit 0 to 19
    Reserved19 = 0  # bit 19 to 32
    BlueExtMaxGcPoint = 0  # bit 0 to 19
    Reserved19 = 0  # bit 19 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PAL_EXT_GC_MAX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PAL_EXT_GC_MAX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PAL_EXT2_GC_MAX:
    PAL_EXT2_GC_MAX_A = 0x4A430
    PAL_EXT2_GC_MAX_B = 0x4AC30
    PAL_EXT2_GC_MAX_C = 0x4B430
    PAL_EXT2_GC_MAX_D = 0x4BC30


class _PAL_EXT2_GC_MAX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RedExtMaxGcPoint', ctypes.c_uint32, 19),
        ('Reserved19', ctypes.c_uint32, 13),
        ('GreenExtMaxGcPoint', ctypes.c_uint32, 19),
        ('Reserved19', ctypes.c_uint32, 13),
        ('BlueExtMaxGcPoint', ctypes.c_uint32, 19),
        ('Reserved19', ctypes.c_uint32, 13),
    ]


class REG_PAL_EXT2_GC_MAX(ctypes.Union):
    value = 0
    offset = 0

    RedExtMaxGcPoint = 0  # bit 0 to 19
    Reserved19 = 0  # bit 19 to 32
    GreenExtMaxGcPoint = 0  # bit 0 to 19
    Reserved19 = 0  # bit 19 to 32
    BlueExtMaxGcPoint = 0  # bit 0 to 19
    Reserved19 = 0  # bit 19 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PAL_EXT2_GC_MAX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PAL_EXT2_GC_MAX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PRE_CSC_GAMC_INDEX:
    PRE_CSC_GAMC_INDEX_A = 0x4A484
    PRE_CSC_GAMC_INDEX_B = 0x4AC84
    PRE_CSC_GAMC_INDEX_C = 0x4B484
    PRE_CSC_GAMC_INDEX_D = 0x4BC84


class _PRE_CSC_GAMC_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 2),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_PRE_CSC_GAMC_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 10
    IndexAutoIncrement = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PRE_CSC_GAMC_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PRE_CSC_GAMC_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PRE_CSC_GAMC_DATA:
    PRE_CSC_GAMC_DATA_A = 0x4A488
    PRE_CSC_GAMC_DATA_B = 0x4AC88
    PRE_CSC_GAMC_DATA_C = 0x4B488
    PRE_CSC_GAMC_DATA_D = 0x4BC88


class _PRE_CSC_GAMC_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaValue', ctypes.c_uint32, 27),
        ('Reserved27', ctypes.c_uint32, 5),
    ]


class REG_PRE_CSC_GAMC_DATA(ctypes.Union):
    value = 0
    offset = 0

    GammaValue = 0  # bit 0 to 27
    Reserved27 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PRE_CSC_GAMC_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PRE_CSC_GAMC_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CSC_COEFF:
    CSC_COEFF_A = 0x49010
    CSC_COEFF_B = 0x49110
    CSC_COEFF_C = 0x49210
    CSC_COEFF_D = 0x49310


class _CSC_COEFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Gy', ctypes.c_uint32, 16),
        ('Ry', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('By', ctypes.c_uint32, 16),
        ('Gu', ctypes.c_uint32, 16),
        ('Ru', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('Bu', ctypes.c_uint32, 16),
        ('Gv', ctypes.c_uint32, 16),
        ('Rv', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('Bv', ctypes.c_uint32, 16),
    ]


class REG_CSC_COEFF(ctypes.Union):
    value = 0
    offset = 0

    Gy = 0  # bit 0 to 16
    Ry = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    By = 0  # bit 16 to 32
    Gu = 0  # bit 0 to 16
    Ru = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    Bu = 0  # bit 16 to 32
    Gv = 0  # bit 0 to 16
    Rv = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    Bv = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_COEFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_COEFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CSC_PREOFF:
    CSC_PREOFF_A = 0x49030
    CSC_PREOFF_B = 0x49130
    CSC_PREOFF_C = 0x49230
    CSC_PREOFF_D = 0x49330


class _CSC_PREOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PrecscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PrecscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PrecscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_CSC_PREOFF(ctypes.Union):
    value = 0
    offset = 0

    PrecscHighOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PrecscMediumOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PrecscLowOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_PREOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_PREOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CSC_POSTOFF:
    CSC_POSTOFF_A = 0x49040
    CSC_POSTOFF_B = 0x49140
    CSC_POSTOFF_C = 0x49240
    CSC_POSTOFF_D = 0x49340


class _CSC_POSTOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PostcscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_CSC_POSTOFF(ctypes.Union):
    value = 0
    offset = 0

    PostcscHighOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PostcscMediumOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PostcscLowOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_POSTOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_POSTOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PIPE_CSC_CC2_ENABLE(Enum):
    PIPE_CSC_CC2_DISABLE = 0x0
    PIPE_CSC_CC2_ENABLE = 0x1


class OFFSET_CSC_MODE:
    CSC_MODE_A = 0x49028
    CSC_MODE_B = 0x49128
    CSC_MODE_C = 0x49228
    CSC_MODE_D = 0x49328


class _CSC_MODE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 28),
        ('PipeCscCC2Enable', ctypes.c_uint32, 1),
        ('AllowDbStall', ctypes.c_uint32, 1),
        ('PipeOutputCscEnable', ctypes.c_uint32, 1),
        ('PipeCscEnable', ctypes.c_uint32, 1),
    ]


class REG_CSC_MODE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 28
    PipeCscCC2Enable = 0  # bit 28 to 29
    AllowDbStall = 0  # bit 29 to 30
    PipeOutputCscEnable = 0  # bit 30 to 31
    PipeCscEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_MODE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_MODE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_OUTPUT_CSC_COEFF:
    OUTPUT_CSC_COEFF_A = 0x49050
    OUTPUT_CSC_COEFF_B = 0x49150
    OUTPUT_CSC_COEFF_C = 0x49250
    OUTPUT_CSC_COEFF_D = 0x49350


class _OUTPUT_CSC_COEFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Gy', ctypes.c_uint32, 16),
        ('Ry', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('By', ctypes.c_uint32, 16),
        ('Gu', ctypes.c_uint32, 16),
        ('Ru', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('Bu', ctypes.c_uint32, 16),
        ('Gv', ctypes.c_uint32, 16),
        ('Rv', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('Bv', ctypes.c_uint32, 16),
    ]


class REG_OUTPUT_CSC_COEFF(ctypes.Union):
    value = 0
    offset = 0

    Gy = 0  # bit 0 to 16
    Ry = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    By = 0  # bit 16 to 32
    Gu = 0  # bit 0 to 16
    Ru = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    Bu = 0  # bit 16 to 32
    Gv = 0  # bit 0 to 16
    Rv = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    Bv = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _OUTPUT_CSC_COEFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_OUTPUT_CSC_COEFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_OUTPUT_CSC_POSTOFF:
    OUTPUT_CSC_POSTOFF_A = 0x49074
    OUTPUT_CSC_POSTOFF_B = 0x49174
    OUTPUT_CSC_POSTOFF_C = 0x49274
    OUTPUT_CSC_POSTOFF_D = 0x49374


class _OUTPUT_CSC_POSTOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PostcscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_OUTPUT_CSC_POSTOFF(ctypes.Union):
    value = 0
    offset = 0

    PostcscHighOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PostcscMediumOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PostcscLowOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _OUTPUT_CSC_POSTOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_OUTPUT_CSC_POSTOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_NEW_LUT_READY(Enum):
    NEW_LUT_READY_NEW_LUT_NOT_READY = 0x0  # New LUT is not yet ready/hardware finished loading the LUT buffer in to in
                                           # ternal working RAM.
    NEW_LUT_READY_NEW_LUT_READY = 0x1  # New LUT is ready.


class ENUM_LUT_3D_ENABLE(Enum):
    LUT_3D_DISABLE = 0x0
    LUT_3D_ENABLE = 0x1


class OFFSET_LUT_3D_CTL:
    LUT_3D_CTL_A = 0x490A4
    LUT_3D_CTL_B = 0x491A4


class _LUT_3D_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 29),
        ('AllowDbStall', ctypes.c_uint32, 1),
        ('NewLutReady', ctypes.c_uint32, 1),
        ('Lut3DEnable', ctypes.c_uint32, 1),
    ]


class REG_LUT_3D_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 29
    AllowDbStall = 0  # bit 29 to 30
    NewLutReady = 0  # bit 30 to 31
    Lut3DEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LUT_3D_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LUT_3D_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LUT_3D_INDEX:
    LUT_3D_INDEX_A = 0x490A8
    LUT_3D_INDEX_B = 0x491A8


class _LUT_3D_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 13),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 18),
    ]


class REG_LUT_3D_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 13
    IndexAutoIncrement = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LUT_3D_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LUT_3D_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LUT_3D_DATA:
    LUT_3D_DATA_A = 0x490AC
    LUT_3D_DATA_B = 0x491AC


class _LUT_3D_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Lut3DEntry', ctypes.c_uint32, 30),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_LUT_3D_DATA(ctypes.Union):
    value = 0
    offset = 0

    Lut3DEntry = 0  # bit 0 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LUT_3D_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LUT_3D_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TILE_SIZE(Enum):
    TILE_SIZE_256X256 = 0x0
    TILE_SIZE_128X128 = 0x1


class ENUM_ENHANCEMENT_MODE(Enum):
    ENHANCEMENT_MODE_DIRECT = 0x0  # Direct look up Mode
    ENHANCEMENT_MODE_MULTIPLICATIVE = 0x1  # Multiplicative Mode


class ENUM_HIST_DISABLE_MODE(Enum):
    HIST_DISABLE_MODE_DISABLE = 0x0
    HIST_DISABLE_MODE_ENABLE = 0x1


class ENUM_ARBITRATION_OPTION(Enum):
    ARBITRATION_OPTION_1 = 0x0
    ARBITRATION_OPTION_2 = 0x1


class ENUM_MASK_DMC_TRIGGER(Enum):
    MASK_DMC_TRIGGER_DISABLE = 0x0
    MASK_DMC_TRIGGER_ENABLE = 0x1


class ENUM_HISTOGRAM_RAM_READBACK_RETURN(Enum):
    HISTOGRAM_RAM_READBACK_RETURN_DISABLE = 0x0
    HISTOGRAM_RAM_READBACK_RETURN_ENABLE = 0x1


class ENUM_FAST_ACCESS_MODE_ENABLE(Enum):
    FAST_ACCESS_MODE_DISABLE = 0x0
    FAST_ACCESS_MODE_ENABLE = 0x1


class ENUM_IE_BUFFER_ID(Enum):
    IE_BUFFER_ID_BANK0 = 0x0  # Reading correction factors from Bank 0
    IE_BUFFER_ID_BANK1 = 0x1  # Reading correction factors from Bank 0


class ENUM_HISTOGRAM_BUFFER_ID(Enum):
    HISTOGRAM_BUFFER_ID_BANK0 = 0x0  # Creating Histogram in Bank0
    HISTOGRAM_BUFFER_ID_BANK1 = 0x1  # Creating Histogram in Bank1


class ENUM_FRAME_HISTOGRAM_DONE(Enum):
    FRAME_HISTOGRAM_DONE_NOT_DONE = 0x0  # Histogram creation not done
    FRAME_HISTOGRAM_DONE_DONE = 0x1  # Histogram creation done


class ENUM_ORIENTATION(Enum):
    ORIENTATION_LANDSCAPE = 0x0  # 16x9 tile arrangement
    ORIENTATION_PORTRAIT = 0x1  # 9x16 tile arrangement


class ENUM_LOAD_IE(Enum):
    LOAD_IE_READY_DONE = 0x0
    LOAD_IE_LOADING = 0x1


class ENUM_IE_ENABLE(Enum):
    IE_DISABLE = 0x0  # Input pixels are routed to output with no modification
    IE_ENABLE = 0x1  # Input pixels will go through image enhancement before output


class ENUM_FUNCTION_ENABLE(Enum):
    FUNCTION_DISABLE = 0x0
    FUNCTION_ENABLE = 0x1


class OFFSET_DPLC_CTL:
    DPLC_CTL_A = 0x49400
    DPLC_CTL_B = 0x49480


class _DPLC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TileSize', ctypes.c_uint32, 1),
        ('HistBufferDelay', ctypes.c_uint32, 1),
        ('Spare2', ctypes.c_uint32, 1),
        ('Spare3', ctypes.c_uint32, 1),
        ('Spare4', ctypes.c_uint32, 1),
        ('Spare5', ctypes.c_uint32, 1),
        ('Spare6', ctypes.c_uint32, 1),
        ('Spare7', ctypes.c_uint32, 1),
        ('Spare8', ctypes.c_uint32, 1),
        ('Spare9', ctypes.c_uint32, 1),
        ('Spare10', ctypes.c_uint32, 1),
        ('Spare11', ctypes.c_uint32, 1),
        ('EnhancementMode', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 5),
        ('HistDisableMode', ctypes.c_uint32, 1),
        ('ArbitrationOption', ctypes.c_uint32, 1),
        ('MaskDmcTrigger', ctypes.c_uint32, 1),
        ('HistogramRamReadbackReturn', ctypes.c_uint32, 1),
        ('FastAccessModeEnable', ctypes.c_uint32, 1),
        ('AllowDbStall', ctypes.c_uint32, 1),
        ('IeBufferId', ctypes.c_uint32, 1),
        ('HistogramBufferId', ctypes.c_uint32, 1),
        ('FrameHistogramDone', ctypes.c_uint32, 1),
        ('Orientation', ctypes.c_uint32, 1),
        ('LoadIe', ctypes.c_uint32, 1),
        ('IeEnable', ctypes.c_uint32, 1),
        ('FunctionEnable', ctypes.c_uint32, 1),
    ]


class REG_DPLC_CTL(ctypes.Union):
    value = 0
    offset = 0

    TileSize = 0  # bit 0 to 1
    HistBufferDelay = 0  # bit 1 to 2
    Spare2 = 0  # bit 2 to 3
    Spare3 = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
    Spare7 = 0  # bit 7 to 8
    Spare8 = 0  # bit 8 to 9
    Spare9 = 0  # bit 9 to 10
    Spare10 = 0  # bit 10 to 11
    Spare11 = 0  # bit 11 to 12
    EnhancementMode = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 19
    HistDisableMode = 0  # bit 19 to 20
    ArbitrationOption = 0  # bit 20 to 21
    MaskDmcTrigger = 0  # bit 21 to 22
    HistogramRamReadbackReturn = 0  # bit 22 to 23
    FastAccessModeEnable = 0  # bit 23 to 24
    AllowDbStall = 0  # bit 24 to 25
    IeBufferId = 0  # bit 25 to 26
    HistogramBufferId = 0  # bit 26 to 27
    FrameHistogramDone = 0  # bit 27 to 28
    Orientation = 0  # bit 28 to 29
    LoadIe = 0  # bit 29 to 30
    IeEnable = 0  # bit 30 to 31
    FunctionEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_HIST_INDEX:
    DPLC_HIST_INDEX_A = 0x49404
    DPLC_HIST_INDEX_B = 0x49484


class _DPLC_HIST_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DwIndex', ctypes.c_uint32, 5),
        ('Reserved5', ctypes.c_uint32, 3),
        ('XIndex', ctypes.c_uint32, 5),
        ('Reserved13', ctypes.c_uint32, 3),
        ('YIndex', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DPLC_HIST_INDEX(ctypes.Union):
    value = 0
    offset = 0

    DwIndex = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 8
    XIndex = 0  # bit 8 to 13
    Reserved13 = 0  # bit 13 to 16
    YIndex = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_HIST_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_HIST_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_HIST_DATA:
    DPLC_HIST_DATA_A = 0x49408
    DPLC_HIST_DATA_B = 0x49488


class _DPLC_HIST_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Bin', ctypes.c_uint32, 17),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_DPLC_HIST_DATA(ctypes.Union):
    value = 0
    offset = 0

    Bin = 0  # bit 0 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_HIST_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_HIST_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_IE_INDEX:
    DPLC_IE_INDEX_A = 0x4940C
    DPLC_IE_INDEX_B = 0x4948C


class _DPLC_IE_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DwIndex', ctypes.c_uint32, 5),
        ('Reserved5', ctypes.c_uint32, 3),
        ('XIndex', ctypes.c_uint32, 5),
        ('Reserved13', ctypes.c_uint32, 3),
        ('YIndex', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DPLC_IE_INDEX(ctypes.Union):
    value = 0
    offset = 0

    DwIndex = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 8
    XIndex = 0  # bit 8 to 13
    Reserved13 = 0  # bit 13 to 16
    YIndex = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_IE_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_IE_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_IE_DATA:
    DPLC_IE_DATA_A = 0x49410
    DPLC_IE_DATA_B = 0x49490


class _DPLC_IE_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EvenPoint', ctypes.c_uint32, 12),
        ('Reserved12', ctypes.c_uint32, 4),
        ('OddPoint', ctypes.c_uint32, 12),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_DPLC_IE_DATA(ctypes.Union):
    value = 0
    offset = 0

    EvenPoint = 0  # bit 0 to 12
    Reserved12 = 0  # bit 12 to 16
    OddPoint = 0  # bit 16 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_IE_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_IE_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_IE_BUFFER_ID_STATE_RESTORE(Enum):
    IE_BUFFER_ID_STATE_RESTORE_BANK0 = 0x0  # Read Correction factors from Bank0
    IE_BUFFER_ID_STATE_RESTORE_BANK1 = 0x1  # Read Correction factors from Bank1


class OFFSET_DPLC_RESTORE:
    DPLC_RESTORE_A = 0x49420
    DPLC_RESTORE_B = 0x494A0


class _DPLC_RESTORE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IeBufferIdStateRestore', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 31),
    ]


class REG_DPLC_RESTORE(ctypes.Union):
    value = 0
    offset = 0

    IeBufferIdStateRestore = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_RESTORE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_RESTORE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_BIN_REGISTER_FUNCTION_SELECT(Enum):
    BIN_REGISTER_FUNCTION_SELECT_TC = 0x0  # Threshold Count. A read from the bin data register returns that bin's thre
                                           # shold value from the most recent vblank load event (guardband threshold
                                           # trip). Valid range for the Bin Index is 0 to 31.
    BIN_REGISTER_FUNCTION_SELECT_IE = 0x1  # Image Enhancement Value. Valid range for the Bin Index is 0 to 32


class ENUM_DPST_ENHANCEMENT_MODE(Enum):
    DPST_ENHANCEMENT_MODE_DIRECT = 0x0  # Direct look up mode
    DPST_ENHANCEMENT_MODE_ADDITIVE = 0x1  # Additive mode
    DPST_ENHANCEMENT_MODE_MULTIPLICATIVE = 0x2  # Multiplicative mode


class ENUM_IE_TABLE_VALUE_FORMAT(Enum):
    IE_TABLE_VALUE_FORMAT_1_9 = 0x0  # 1 integer and 9 fractional bits
    IE_TABLE_VALUE_FORMAT_2_8 = 0x1  # 2 integer and 8 fractional bits


class ENUM_HISTOGRAM_MODE_SELECT(Enum):
    HISTOGRAM_MODE_SELECT_YUV = 0x0  # YUV Luma Mode
    HISTOGRAM_MODE_SELECT_HSV = 0x1  # HSV Intensity Mode


class ENUM_IE_MODIFICATION_TABLE_ENABLE(Enum):
    IE_MODIFICATION_TABLE_DISABLE = 0x0
    IE_MODIFICATION_TABLE_ENABLE = 0x1


class ENUM_RESTORE_DPST(Enum):
    RESTORE_DPST_NO_RESTORE = 0x0
    RESTORE_DPST_RESTORE = 0x1


class ENUM_IE_HISTOGRAM_ENABLE(Enum):
    IE_HISTOGRAM_DISABLE = 0x0
    IE_HISTOGRAM_ENABLE = 0x1


class OFFSET_DPST_CTL:
    DPST_CTL_A = 0x490C0
    DPST_CTL_B = 0x491C0
    DPST_CTL_C = 0x492C0
    DPST_CTL_D = 0x493C0


class _DPST_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BinRegisterIndex', ctypes.c_uint32, 7),
        ('Reserved7', ctypes.c_uint32, 4),
        ('BinRegisterFunctionSelect', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 1),
        ('EnhancementMode', ctypes.c_uint32, 2),
        ('IeTableValueFormat', ctypes.c_uint32, 1),
        ('GuardbandInterruptDelayCounter', ctypes.c_uint32, 8),
        ('HistogramModeSelect', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 2),
        ('IeModificationTableEnable', ctypes.c_uint32, 1),
        ('RestoreDpst', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 2),
        ('IeHistogramEnable', ctypes.c_uint32, 1),
    ]


class REG_DPST_CTL(ctypes.Union):
    value = 0
    offset = 0

    BinRegisterIndex = 0  # bit 0 to 7
    Reserved7 = 0  # bit 7 to 11
    BinRegisterFunctionSelect = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 13
    EnhancementMode = 0  # bit 13 to 15
    IeTableValueFormat = 0  # bit 15 to 16
    GuardbandInterruptDelayCounter = 0  # bit 16 to 24
    HistogramModeSelect = 0  # bit 24 to 25
    Reserved25 = 0  # bit 25 to 27
    IeModificationTableEnable = 0  # bit 27 to 28
    RestoreDpst = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 31
    IeHistogramEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPST_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPST_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPST_BIN:
    DPST_BIN_A = 0x490C4
    DPST_BIN_B = 0x491C4
    DPST_BIN_C = 0x492C4
    DPST_BIN_D = 0x493C4


class _DPST_BIN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Data', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 7),
        ('BusyBit', ctypes.c_uint32, 1),
    ]


class REG_DPST_BIN(ctypes.Union):
    value = 0
    offset = 0

    Data = 0  # bit 0 to 24
    Reserved24 = 0  # bit 24 to 31
    BusyBit = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPST_BIN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPST_BIN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_HISTOGRAM_EVENT_STATUS(Enum):
    HISTOGRAM_EVENT_STATUS_NOT_OCCURRED = 0x0  # Histogram event has not occurred
    HISTOGRAM_EVENT_STATUS_OCCURED = 0x1  # Histogram event has occurred


class ENUM_HISTOGRAM_INTERRUPT_ENABLE(Enum):
    HISTOGRAM_INTERRUPT_DISABLE = 0x0  # Disabled
    HISTOGRAM_INTERRUPT_ENABLE = 0x1  # This generates a histogram interrupt once a Histogram event occurs.


class OFFSET_DPST_GUARD:
    DPST_GUARD_A = 0x490C8
    DPST_GUARD_B = 0x491C8
    DPST_GUARD_C = 0x492C8
    DPST_GUARD_D = 0x493C8


class _DPST_GUARD(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ThresholdGuardband', ctypes.c_uint32, 22),
        ('GuardbandInterruptDelay', ctypes.c_uint32, 8),
        ('HistogramEventStatus', ctypes.c_uint32, 1),
        ('HistogramInterruptEnable', ctypes.c_uint32, 1),
    ]


class REG_DPST_GUARD(ctypes.Union):
    value = 0
    offset = 0

    ThresholdGuardband = 0  # bit 0 to 22
    GuardbandInterruptDelay = 0  # bit 22 to 30
    HistogramEventStatus = 0  # bit 30 to 31
    HistogramInterruptEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPST_GUARD),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPST_GUARD, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_RTID_FIFO_WATERMARK(Enum):
    RTID_FIFO_WATERMARK_8_RTIDS = 0x0
    RTID_FIFO_WATERMARK_16_RTIDS = 0x1
    RTID_FIFO_WATERMARK_32_RTIDS = 0x2


class ENUM_ENABLE_IPC(Enum):
    ENABLE_IPC_DISABLE = 0x0
    ENABLE_IPC_ENABLE = 0x1


class OFFSET_ARB_HP_CTL:
    ARB_HP_CTL = 0x45004


class _ARB_HP_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RtidFifoWatermark', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('EnableIpc', ctypes.c_uint32, 1),
        ('IackThrottleMax', ctypes.c_uint32, 5),
        ('Reserved9', ctypes.c_uint32, 1),
        ('Abox0AtsRequestThrottle', ctypes.c_uint32, 5),
        ('Abox1AtsRequestThrottle', ctypes.c_uint32, 5),
        ('Reserved20', ctypes.c_uint32, 3),
        ('Reserved23', ctypes.c_uint32, 9),
    ]


class REG_ARB_HP_CTL(ctypes.Union):
    value = 0
    offset = 0

    RtidFifoWatermark = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    EnableIpc = 0  # bit 3 to 4
    IackThrottleMax = 0  # bit 4 to 9
    Reserved9 = 0  # bit 9 to 10
    Abox0AtsRequestThrottle = 0  # bit 10 to 15
    Abox1AtsRequestThrottle = 0  # bit 15 to 20
    Reserved20 = 0  # bit 20 to 23
    Reserved23 = 0  # bit 23 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _ARB_HP_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_ARB_HP_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_CLKGATE_DIS:
    PIPE_CLKGATE_DIS_A = 0x60110
    PIPE_CLKGATE_DIS_B = 0x61110
    PIPE_CLKGATE_DIS_C = 0x62110
    PIPE_CLKGATE_DIS_D = 0x63110


class _PIPE_CLKGATE_DIS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DoledGatingDis', ctypes.c_uint32, 1),
        ('DarpbGatingDis', ctypes.c_uint32, 1),
        ('Dprp4GatingDis', ctypes.c_uint32, 1),
        ('Dup4GatingDis', ctypes.c_uint32, 1),
        ('DplmGatingDis', ctypes.c_uint32, 1),
        ('Dups4GatingDis', ctypes.c_uint32, 1),
        ('DprcGatingDis', ctypes.c_uint32, 1),
        ('DpstGatingDis', ctypes.c_uint32, 1),
        ('DpfrGatingDis', ctypes.c_uint32, 1),
        ('DpfPipeBindingGatingDis', ctypes.c_uint32, 1),
        ('DpfGatingDis', ctypes.c_uint32, 1),
        ('DpbGatingDis', ctypes.c_uint32, 1),
        ('Dprp1GatingDis', ctypes.c_uint32, 1),
        ('Dup1GatingDis', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 1),
        ('Dups1GatingDis', ctypes.c_uint32, 1),
        ('Dprp2GatingDis', ctypes.c_uint32, 1),
        ('Dup2GatingDis', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 1),
        ('Dups2GatingDis', ctypes.c_uint32, 1),
        ('Dprp3GatingDis', ctypes.c_uint32, 1),
        ('Dup3GatingDis', ctypes.c_uint32, 1),
        ('Reserved22', ctypes.c_uint32, 1),
        ('Dups3GatingDis', ctypes.c_uint32, 1),
        ('DmuxGatingDis', ctypes.c_uint32, 1),
        ('DprsGatingDis', ctypes.c_uint32, 1),
        ('DpcebGatingDis', ctypes.c_uint32, 1),
        ('DarbsGatingDis', ctypes.c_uint32, 1),
        ('DcGatingDis', ctypes.c_uint32, 1),
        ('DdbGatingDis', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 1),
        ('DpccGatingDis', ctypes.c_uint32, 1),
    ]


class REG_PIPE_CLKGATE_DIS(ctypes.Union):
    value = 0
    offset = 0

    DoledGatingDis = 0  # bit 0 to 1
    DarpbGatingDis = 0  # bit 1 to 2
    Dprp4GatingDis = 0  # bit 2 to 3
    Dup4GatingDis = 0  # bit 3 to 4
    DplmGatingDis = 0  # bit 4 to 5
    Dups4GatingDis = 0  # bit 5 to 6
    DprcGatingDis = 0  # bit 6 to 7
    DpstGatingDis = 0  # bit 7 to 8
    DpfrGatingDis = 0  # bit 8 to 9
    DpfPipeBindingGatingDis = 0  # bit 9 to 10
    DpfGatingDis = 0  # bit 10 to 11
    DpbGatingDis = 0  # bit 11 to 12
    Dprp1GatingDis = 0  # bit 12 to 13
    Dup1GatingDis = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 15
    Dups1GatingDis = 0  # bit 15 to 16
    Dprp2GatingDis = 0  # bit 16 to 17
    Dup2GatingDis = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 19
    Dups2GatingDis = 0  # bit 19 to 20
    Dprp3GatingDis = 0  # bit 20 to 21
    Dup3GatingDis = 0  # bit 21 to 22
    Reserved22 = 0  # bit 22 to 23
    Dups3GatingDis = 0  # bit 23 to 24
    DmuxGatingDis = 0  # bit 24 to 25
    DprsGatingDis = 0  # bit 25 to 26
    DpcebGatingDis = 0  # bit 26 to 27
    DarbsGatingDis = 0  # bit 27 to 28
    DcGatingDis = 0  # bit 28 to 29
    DdbGatingDis = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 31
    DpccGatingDis = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_CLKGATE_DIS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_CLKGATE_DIS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SURFACE_ARMING_REQUIRED_SYNC(Enum):
    SURFACE_ARMING_REQUIRED_SYNC_NO_ARMING = 0x0
    SURFACE_ARMING_REQUIRED_SYNC_ARMING_REQUIRED = 0x1


class ENUM_MASK_FLIPS(Enum):
    MASK_FLIPS_NOT_MASKED = 0x0
    MASK_FLIPS_MASKED = 0x1


class ENUM_REVERT_BOTTOM_COLOR_PIXEL_FIX(Enum):
    REVERT_BOTTOM_COLOR_PIXEL_FIX_ENABLE_THE_FIX_ = 0x0
    REVERT_BOTTOM_COLOR_PIXEL_FIX_DISABLE_THE_FIX_ = 0x1


class ENUM__3D_LUT_ON_FIRST_FRAME(Enum):
    _3D_LUT_ON_FIRST_FRAME_ENABLE = 0x1
    _3D_LUT_ON_FIRST_FRAME_DISABLE = 0x0


class ENUM_DBUF_BLOCK_HASHING_DISABLE(Enum):
    DBUF_BLOCK_HASHING_ENABLE = 0x0
    DBUF_BLOCK_HASHING_DISABLE = 0x1


class ENUM_SCALER_PWR_GATE_EBBS(Enum):
    SCALER_PWR_GATE_EBBS_DISABLED = 0x0  # Power gating of EBB's is controlled by Scaler Enable (PS_CTRL)
    SCALER_PWR_GATE_EBBS_ENABLED = 0x1  # EBB's will be power gated regardless of Scaler Enable


class ENUM_DISABLE_DPST_WRITE_EXIT_PSR(Enum):
    DISABLE_DPST_WRITE_EXIT_PSR_ENABLE_DPST_WRITE_PSR_EXIT = 0x0
    DISABLE_DPST_WRITE_EXIT_PSR_DISABLE_DPST_WRITE_PSR_EXIT = 0x1


class ENUM_DISABLE_PIPE_UNDERRUN_RECOVERY(Enum):
    DISABLE_PIPE_UNDERRUN_RECOVERY_UNDERRUN_RECOVERY_IS_ENABLED = 0x0
    DISABLE_PIPE_UNDERRUN_RECOVERY_UNDERRUN_RECOVERY_IS_DISABLED = 0x1


class OFFSET_PIPE_CHICKEN:
    PIPE_CHICKEN_A = 0x70038
    PIPE_CHICKEN_B = 0x71038
    PIPE_CHICKEN_C = 0x72038
    PIPE_CHICKEN_D = 0x73038


class _PIPE_CHICKEN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare0', ctypes.c_uint32, 1),
        ('Spare1', ctypes.c_uint32, 1),
        ('Spare2', ctypes.c_uint32, 1),
        ('SurfaceArmingRequiredSync', ctypes.c_uint32, 1),
        ('Spare4', ctypes.c_uint32, 1),
        ('Spare5', ctypes.c_uint32, 1),
        ('Spare6', ctypes.c_uint32, 1),
        ('MaskFlips', ctypes.c_uint32, 1),
        ('Spare8', ctypes.c_uint32, 1),
        ('Spare9', ctypes.c_uint32, 1),
        ('Spare10', ctypes.c_uint32, 1),
        ('Spare11', ctypes.c_uint32, 1),
        ('Spare12', ctypes.c_uint32, 1),
        ('RevertBottomColorPixelFix', ctypes.c_uint32, 1),
        ('_3DLutOnFirstFrame', ctypes.c_uint32, 1),
        ('Spare15', ctypes.c_uint32, 1),
        ('Spare16', ctypes.c_uint32, 1),
        ('Spare17', ctypes.c_uint32, 1),
        ('DbufBlockHashingDisable', ctypes.c_uint32, 1),
        ('Spare19', ctypes.c_uint32, 1),
        ('Spare20', ctypes.c_uint32, 1),
        ('Spare21', ctypes.c_uint32, 1),
        ('ScalerPwrGateEbbs', ctypes.c_uint32, 1),
        ('Spare23', ctypes.c_uint32, 1),
        ('Spare24', ctypes.c_uint32, 1),
        ('Spare25', ctypes.c_uint32, 1),
        ('Spare26', ctypes.c_uint32, 1),
        ('Spare27', ctypes.c_uint32, 1),
        ('Spare28', ctypes.c_uint32, 1),
        ('DisableDpstWriteExitPsr', ctypes.c_uint32, 1),
        ('DisablePipeUnderrunRecovery', ctypes.c_uint32, 1),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_PIPE_CHICKEN(ctypes.Union):
    value = 0
    offset = 0

    Spare0 = 0  # bit 0 to 1
    Spare1 = 0  # bit 1 to 2
    Spare2 = 0  # bit 2 to 3
    SurfaceArmingRequiredSync = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
    MaskFlips = 0  # bit 7 to 8
    Spare8 = 0  # bit 8 to 9
    Spare9 = 0  # bit 9 to 10
    Spare10 = 0  # bit 10 to 11
    Spare11 = 0  # bit 11 to 12
    Spare12 = 0  # bit 12 to 13
    RevertBottomColorPixelFix = 0  # bit 13 to 14
    _3DLutOnFirstFrame = 0  # bit 14 to 15
    Spare15 = 0  # bit 15 to 16
    Spare16 = 0  # bit 16 to 17
    Spare17 = 0  # bit 17 to 18
    DbufBlockHashingDisable = 0  # bit 18 to 19
    Spare19 = 0  # bit 19 to 20
    Spare20 = 0  # bit 20 to 21
    Spare21 = 0  # bit 21 to 22
    ScalerPwrGateEbbs = 0  # bit 22 to 23
    Spare23 = 0  # bit 23 to 24
    Spare24 = 0  # bit 24 to 25
    Spare25 = 0  # bit 25 to 26
    Spare26 = 0  # bit 26 to 27
    Spare27 = 0  # bit 27 to 28
    Spare28 = 0  # bit 28 to 29
    DisableDpstWriteExitPsr = 0  # bit 29 to 30
    DisablePipeUnderrunRecovery = 0  # bit 30 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_CHICKEN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_CHICKEN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_PART_CTL:
    DPLC_PART_CTL_A = 0x49430
    DPLC_PART_CTL_B = 0x494B0


class _DPLC_PART_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PartAStartTileRow', ctypes.c_uint32, 5),
        ('PartAEndTileRow', ctypes.c_uint32, 5),
        ('Reserved10', ctypes.c_uint32, 6),
        ('PartBStartTileRow', ctypes.c_uint32, 5),
        ('PartBEndTileRow', ctypes.c_uint32, 5),
        ('Reserved26', ctypes.c_uint32, 6),
    ]


class REG_DPLC_PART_CTL(ctypes.Union):
    value = 0
    offset = 0

    PartAStartTileRow = 0  # bit 0 to 5
    PartAEndTileRow = 0  # bit 5 to 10
    Reserved10 = 0  # bit 10 to 16
    PartBStartTileRow = 0  # bit 16 to 21
    PartBEndTileRow = 0  # bit 21 to 26
    Reserved26 = 0  # bit 26 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_PART_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_PART_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_PTRCFG:
    DPLC_PTRCFG_PARTA_A = 0x49434
    DPLC_PTRCFG_PARTB_A = 0x49438
    DPLC_PTRCFG_PARTA_B = 0x494B4
    DPLC_PTRCFG_PARTB_B = 0x494B8


class _DPLC_PTRCFG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HistogramIndex', ctypes.c_uint32, 32),
    ]


class REG_DPLC_PTRCFG(ctypes.Union):
    value = 0
    offset = 0

    HistogramIndex = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_PTRCFG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_PTRCFG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_PTRCFG_LIVE:
    DPLC_PTRCFG_LIVE_PARTA_A = 0x49444
    DPLC_PTRCFG_LIVE_PARTB_A = 0x49448
    DPLC_PTRCFG_LIVE_PARTA_B = 0x494C4
    DPLC_PTRCFG_LIVE_PARTB_B = 0x494C8


class _DPLC_PTRCFG_LIVE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HistogramIndex', ctypes.c_uint32, 32),
    ]


class REG_DPLC_PTRCFG_LIVE(ctypes.Union):
    value = 0
    offset = 0

    HistogramIndex = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_PTRCFG_LIVE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_PTRCFG_LIVE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_RDLENGTH:
    DPLC_RDLENGTH_PARTA_A = 0x4943C
    DPLC_RDLENGTH_PARTB_A = 0x49440
    DPLC_RDLENGTH_PARTA_B = 0x494BC
    DPLC_RDLENGTH_PARTB_B = 0x494C0


class _DPLC_RDLENGTH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ReadLength', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_DPLC_RDLENGTH(ctypes.Union):
    value = 0
    offset = 0

    ReadLength = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_RDLENGTH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_RDLENGTH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_RDLENGTH_LIVE:
    DPLC_RDLENGTH_LIVE_PARTA_A = 0x4944C
    DPLC_RDLENGTH_LIVE_PARTB_A = 0x49450
    DPLC_RDLENGTH_LIVE_PARTA_B = 0x494CC
    DPLC_RDLENGTH_LIVE_PARTB_B = 0x494D0


class _DPLC_RDLENGTH_LIVE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ReadLength', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_DPLC_RDLENGTH_LIVE(ctypes.Union):
    value = 0
    offset = 0

    ReadLength = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_RDLENGTH_LIVE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_RDLENGTH_LIVE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_FA_SURF:
    DPLC_FA_SURF_PARTA_A = 0x49470
    DPLC_FA_SURF_PARTB_A = 0x49474
    DPLC_FA_SURF_PARTA_B = 0x494F0
    DPLC_FA_SURF_PARTB_B = 0x494F4


class _DPLC_FA_SURF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('SurfaceBaseAddress', ctypes.c_uint32, 20),
    ]


class REG_DPLC_FA_SURF(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    SurfaceBaseAddress = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_FA_SURF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_FA_SURF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_FA_SURF_LIVE:
    DPLC_FA_SURF_LIVE_PARTA_A = 0x49478
    DPLC_FA_SURF_LIVE_PARTB_A = 0x4947C
    DPLC_FA_SURF_LIVE_PARTA_B = 0x494F8
    DPLC_FA_SURF_LIVE_PARTB_B = 0x494FC


class _DPLC_FA_SURF_LIVE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('SurfaceBaseAddress', ctypes.c_uint32, 20),
    ]


class REG_DPLC_FA_SURF_LIVE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    SurfaceBaseAddress = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_FA_SURF_LIVE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_FA_SURF_LIVE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PART_A_HISTOGRAM_READY(Enum):
    PART_A_HISTOGRAM_READY_NOT_READY = 0x0
    PART_A_HISTOGRAM_READY_READY = 0x1


class ENUM_PART_A_LOAD_IE(Enum):
    PART_A_LOAD_IE_READY_DONE = 0x0
    PART_A_LOAD_IE_LOADING = 0x1


class ENUM_PART_A_HISTOGRAM_COPY_DONE(Enum):
    PART_A_HISTOGRAM_COPY_DONE_NOT_DONE = 0x0
    PART_A_HISTOGRAM_COPY_DONE_DONE = 0x1


class ENUM_PART_B_HISTOGRAM_READY(Enum):
    PART_B_HISTOGRAM_READY_NOT_READY = 0x0
    PART_B_HISTOGRAM_READY_READY = 0x1


class ENUM_PART_B_LOAD_IE(Enum):
    PART_B_LOAD_IE_READY_DONE = 0x0
    PART_B_LOAD_IE_LOADING = 0x1


class ENUM_PART_B_HISTOGRAM_COPY_DONE(Enum):
    PART_B_HISTOGRAM_COPY_DONE_NOT_DONE = 0x0
    PART_B_HISTOGRAM_COPY_DONE_DONE = 0x1


class OFFSET_DPLC_FA_STATUS:
    DPLC_FA_STATUS_A = 0x49460
    DPLC_FA_STATUS_B = 0x494E0


class _DPLC_FA_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PartAHistogramReady', ctypes.c_uint32, 1),
        ('PartALoadIe', ctypes.c_uint32, 1),
        ('PartAHistogramCopyDone', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 13),
        ('PartBHistogramReady', ctypes.c_uint32, 1),
        ('PartBLoadIe', ctypes.c_uint32, 1),
        ('PartBHistogramCopyDone', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 13),
    ]


class REG_DPLC_FA_STATUS(ctypes.Union):
    value = 0
    offset = 0

    PartAHistogramReady = 0  # bit 0 to 1
    PartALoadIe = 0  # bit 1 to 2
    PartAHistogramCopyDone = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 16
    PartBHistogramReady = 0  # bit 16 to 17
    PartBLoadIe = 0  # bit 17 to 18
    PartBHistogramCopyDone = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_FA_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_FA_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CSC_CC2_COEFF:
    CSC_CC2_COEFF_A = 0x4A518
    CSC_CC2_COEFF_B = 0x4AD18


class _CSC_CC2_COEFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Gy', ctypes.c_uint32, 16),
        ('Ry', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('By', ctypes.c_uint32, 16),
        ('Gu', ctypes.c_uint32, 16),
        ('Ru', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('Bu', ctypes.c_uint32, 16),
        ('Gv', ctypes.c_uint32, 16),
        ('Rv', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('Bv', ctypes.c_uint32, 16),
    ]


class REG_CSC_CC2_COEFF(ctypes.Union):
    value = 0
    offset = 0

    Gy = 0  # bit 0 to 16
    Ry = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    By = 0  # bit 16 to 32
    Gu = 0  # bit 0 to 16
    Ru = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    Bu = 0  # bit 16 to 32
    Gv = 0  # bit 0 to 16
    Rv = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    Bv = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_CC2_COEFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_CC2_COEFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CSC_CC2_PREOFF:
    CSC_CC2_PREOFF_A = 0x4A530
    CSC_CC2_PREOFF_B = 0x4AD30


class _CSC_CC2_PREOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PrecscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PrecscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PrecscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_CSC_CC2_PREOFF(ctypes.Union):
    value = 0
    offset = 0

    PrecscHighOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PrecscMediumOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PrecscLowOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_CC2_PREOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_CC2_PREOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CSC_CC2_POSTOFF:
    CSC_CC2_POSTOFF_A = 0x4A53C
    CSC_CC2_POSTOFF_B = 0x4AD3C


class _CSC_CC2_POSTOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PostcscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_CSC_CC2_POSTOFF(ctypes.Union):
    value = 0
    offset = 0

    PostcscHighOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PostcscMediumOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PostcscLowOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_CC2_POSTOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_CC2_POSTOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PRE_CSC_CC2_GAMC_INDEX:
    PRE_CSC_CC2_GAMC_INDEX_A = 0x4A500
    PRE_CSC_CC2_GAMC_INDEX_B = 0x4AD00


class _PRE_CSC_CC2_GAMC_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 2),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_PRE_CSC_CC2_GAMC_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 10
    IndexAutoIncrement = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PRE_CSC_CC2_GAMC_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PRE_CSC_CC2_GAMC_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PRE_CSC_CC2_GAMC_DATA:
    PRE_CSC_CC2_GAMC_DATA_A = 0x4A504
    PRE_CSC_CC2_GAMC_DATA_B = 0x4AD04


class _PRE_CSC_CC2_GAMC_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaValue', ctypes.c_uint32, 25),
        ('Reserved25', ctypes.c_uint32, 7),
    ]


class REG_PRE_CSC_CC2_GAMC_DATA(ctypes.Union):
    value = 0
    offset = 0

    GammaValue = 0  # bit 0 to 25
    Reserved25 = 0  # bit 25 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PRE_CSC_CC2_GAMC_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PRE_CSC_CC2_GAMC_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_POST_CSC_CC2_INDEX:
    POST_CSC_CC2_INDEX_A = 0x4A508
    POST_CSC_CC2_INDEX_B = 0x4AD08


class _POST_CSC_CC2_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 10),
        ('Reserved10', ctypes.c_uint32, 5),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_POST_CSC_CC2_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 10
    Reserved10 = 0  # bit 10 to 15
    IndexAutoIncrement = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _POST_CSC_CC2_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_POST_CSC_CC2_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_POST_CSC_CC2_DATA:
    POST_CSC_CC2_DATA_A = 0x4A50C
    POST_CSC_CC2_DATA_B = 0x4AD0C


class _POST_CSC_CC2_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BluePrecisionPaletteEntry', ctypes.c_uint32, 10),
        ('GreenPrecisionPaletteEntry', ctypes.c_uint32, 10),
        ('RedPrecisionPaletteEntry', ctypes.c_uint32, 10),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_POST_CSC_CC2_DATA(ctypes.Union):
    value = 0
    offset = 0

    BluePrecisionPaletteEntry = 0  # bit 0 to 10
    GreenPrecisionPaletteEntry = 0  # bit 10 to 20
    RedPrecisionPaletteEntry = 0  # bit 20 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _POST_CSC_CC2_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_POST_CSC_CC2_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_BW_CREDITS(Enum):
    BW_CREDITS_2_CREDITS = 0x0
    BW_CREDITS_6_CREDITS = 0x1
    BW_CREDITS_4_CREDITS = 0x2
    BW_CREDITS_8_CREDITS = 0x3


class ENUM_REGULATE_B2B_TRANSACTIONS(Enum):
    REGULATE_B2B_TRANSACTIONS_DISABLE = 0x0
    REGULATE_B2B_TRANSACTIONS_ENABLE = 0x1


class ENUM_STATUS(Enum):
    STATUS_DISABLED = 0x0
    STATUS_ENABLED = 0x1


class OFFSET_MBUS_DBOX_CTL:
    PIPE_MBUS_DBOX_CTL_A = 0x7003C
    PIPE_MBUS_DBOX_CTL_B = 0x7103C
    PIPE_MBUS_DBOX_CTL_C = 0x7203C
    PIPE_MBUS_DBOX_CTL_D = 0x7303C


class _MBUS_DBOX_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ACredits', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 1),
        ('ICredits', ctypes.c_uint32, 3),
        ('BCredits', ctypes.c_uint32, 5),
        ('Reserved13', ctypes.c_uint32, 1),
        ('BwCredits', ctypes.c_uint32, 2),
        ('RegulateB2BTransactions', ctypes.c_uint32, 1),
        ('B2BTransactionsDelay', ctypes.c_uint32, 3),
        ('B2BTransactionsMax', ctypes.c_uint32, 5),
        ('Reserved25', ctypes.c_uint32, 2),
        ('RingStopAddress', ctypes.c_uint32, 4),
        ('Status', ctypes.c_uint32, 1),
    ]


class REG_MBUS_DBOX_CTL(ctypes.Union):
    value = 0
    offset = 0

    ACredits = 0  # bit 0 to 4
    Reserved4 = 0  # bit 4 to 5
    ICredits = 0  # bit 5 to 8
    BCredits = 0  # bit 8 to 13
    Reserved13 = 0  # bit 13 to 14
    BwCredits = 0  # bit 14 to 16
    RegulateB2BTransactions = 0  # bit 16 to 17
    B2BTransactionsDelay = 0  # bit 17 to 20
    B2BTransactionsMax = 0  # bit 20 to 25
    Reserved25 = 0  # bit 25 to 27
    RingStopAddress = 0  # bit 27 to 31
    Status = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MBUS_DBOX_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MBUS_DBOX_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MBUS_UBOX_CTL:
    MBUS_UBOX_CTL0 = 0x4503C


class _MBUS_UBOX_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VgaBCredits', ctypes.c_uint32, 3),
        ('Reserved3', ctypes.c_uint32, 1),
        ('KvmSpriteACredits', ctypes.c_uint32, 3),
        ('Reserved7', ctypes.c_uint32, 9),
        ('RegulateB2BTransactions', ctypes.c_uint32, 1),
        ('B2BTransactionsDelay', ctypes.c_uint32, 3),
        ('B2BTransactionsMax', ctypes.c_uint32, 5),
        ('Reserved25', ctypes.c_uint32, 2),
        ('RingStopAddress', ctypes.c_uint32, 4),
        ('Status', ctypes.c_uint32, 1),
    ]


class REG_MBUS_UBOX_CTL(ctypes.Union):
    value = 0
    offset = 0

    VgaBCredits = 0  # bit 0 to 3
    Reserved3 = 0  # bit 3 to 4
    KvmSpriteACredits = 0  # bit 4 to 7
    Reserved7 = 0  # bit 7 to 16
    RegulateB2BTransactions = 0  # bit 16 to 17
    B2BTransactionsDelay = 0  # bit 17 to 20
    B2BTransactionsMax = 0  # bit 20 to 25
    Reserved25 = 0  # bit 25 to 27
    RingStopAddress = 0  # bit 27 to 31
    Status = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MBUS_UBOX_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MBUS_UBOX_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_MISC3:
    PIPE_MISC3_A = 0x7005C
    PIPE_MISC3_B = 0x7105C
    PIPE_MISC3_C = 0x7205C
    PIPE_MISC3_D = 0x7305C


class _PIPE_MISC3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HighestRecoveryCounterStatus', ctypes.c_uint32, 16),
        ('PipeSourceSizeExcess', ctypes.c_uint32, 8),
        ('TlbThrottle', ctypes.c_uint32, 5),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PIPE_MISC3(ctypes.Union):
    value = 0
    offset = 0

    HighestRecoveryCounterStatus = 0  # bit 0 to 16
    PipeSourceSizeExcess = 0  # bit 16 to 24
    TlbThrottle = 0  # bit 24 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_MISC3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_MISC3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PIPE_BINDING(Enum):
    PIPE_BINDING_SINGLE = 0x0  # Single pipe configuration.
    PIPE_BINDING_A_B = 0x3  # Pipes A and B are joined.
    PIPE_BINDING_A_C = 0x5  # Pipes A and C are joined.
    PIPE_BINDING_B_C = 0x6  # Pipes B and C are joined.
    PIPE_BINDING_A_D = 0x9  # Pipes A and D are joined.
    PIPE_BINDING_B_D = 0xA  # Pipes B and D are joined.
    PIPE_BINDING_C_D = 0xC  # Pipes C and D are joined.


class ENUM_CURRENT_PIPE_POSITION(Enum):
    CURRENT_PIPE_POSITION_FIRST_FROM_LEFT = 0x0
    CURRENT_PIPE_POSITION_SECOND_FROM_LEFT = 0x1


class OFFSET_PIPE_MISC4:
    PIPE_MISC4_A = 0x70060
    PIPE_MISC4_B = 0x71060
    PIPE_MISC4_C = 0x72060
    PIPE_MISC4_D = 0x73060


class _PIPE_MISC4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('RightFilterCoeff', ctypes.c_uint32, 7),
        ('Reserved8', ctypes.c_uint32, 1),
        ('CenterFilterCoeff', ctypes.c_uint32, 7),
        ('Reserved16', ctypes.c_uint32, 1),
        ('LeftFilterCoeff', ctypes.c_uint32, 7),
        ('PipeBinding', ctypes.c_uint32, 4),
        ('CurrentPipePosition', ctypes.c_uint32, 2),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PIPE_MISC4(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    RightFilterCoeff = 0  # bit 1 to 8
    Reserved8 = 0  # bit 8 to 9
    CenterFilterCoeff = 0  # bit 9 to 16
    Reserved16 = 0  # bit 16 to 17
    LeftFilterCoeff = 0  # bit 17 to 24
    PipeBinding = 0  # bit 24 to 28
    CurrentPipePosition = 0  # bit 28 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_MISC4),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_MISC4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPE_DMC_SCANLINE_CMP_UPPER:
    PIPE_DMC_SCANLINE_CMP_UPPER_A = 0x5F124
    PIPE_DMC_SCANLINE_CMP_UPPER_B = 0x5F524
    PIPE_DMC_SCANLINE_CMP_UPPER_C = 0x5F924
    PIPE_DMC_SCANLINE_CMP_UPPER_D = 0x5FD24


class _PIPE_DMC_SCANLINE_CMP_UPPER(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ScanLineUpper', ctypes.c_uint32, 21),
        ('Reserved21', ctypes.c_uint32, 11)
    ]


class REG_PIPE_DMC_SCANLINE_CMP_UPPER(ctypes.Union):
    value = 0
    offset = 0

    ScanLineUpper = 0  # bit 0 to 21
    Reserved21 = 0  # bit 21 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPE_DMC_SCANLINE_CMP_UPPER),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPE_DMC_SCANLINE_CMP_UPPER, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value