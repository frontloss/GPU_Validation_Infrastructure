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
# @file RklcPllRegs.py
# @brief contains RklcPllRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_DDIA_CLOCK_SELECT(Enum):
    DDIA_CLOCK_SELECT_DPLL0 = 0x0
    DDIA_CLOCK_SELECT_DPLL1 = 0x1
    DDIA_CLOCK_SELECT_DPLL4 = 0x2


class ENUM_DDIB_CLOCK_SELECT(Enum):
    DDIB_CLOCK_SELECT_DPLL0 = 0x0
    DDIB_CLOCK_SELECT_DPLL1 = 0x1
    DDIB_CLOCK_SELECT_DPLL4 = 0x2


class ENUM_DDIC_CLOCK_SELECT(Enum):
    DDIC_CLOCK_SELECT_DPLL0 = 0x0
    DDIC_CLOCK_SELECT_DPLL1 = 0x1
    DDIC_CLOCK_SELECT_DPLL4 = 0x2


class ENUM_DDIA_CLOCK_OFF(Enum):
    DDIA_CLOCK_OFF_ON = 0x0
    DDIA_CLOCK_OFF_OFF = 0x1


class ENUM_DDIB_CLOCK_OFF(Enum):
    DDIB_CLOCK_OFF_ON = 0x0
    DDIB_CLOCK_OFF_OFF = 0x1


class ENUM_DDIC_CLOCK_OFF(Enum):
    DDIC_CLOCK_OFF_ON = 0x0
    DDIC_CLOCK_OFF_OFF = 0x1


class ENUM_DDID_CLOCK_OFF(Enum):
    DDID_CLOCK_OFF_ON = 0x0
    DDID_CLOCK_OFF_OFF = 0x1


class ENUM_DPLL0_INVERSE_REF(Enum):
    DPLL0_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL0_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL1_INVERSE_REF(Enum):
    DPLL1_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL1_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL4_INVERSE_REF(Enum):
    DPLL4_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL4_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL0_ENABLE_OVERRIDE(Enum):
    DPLL0_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL0_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_DPLL1_ENABLE_OVERRIDE(Enum):
    DPLL1_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL1_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_DPLL4_ENABLE_OVERRIDE(Enum):
    DPLL4_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL4_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_DDID_CLOCK_SELECT(Enum):
    DDID_CLOCK_SELECT_DPLL0 = 0x0
    DDID_CLOCK_SELECT_DPLL1 = 0x1
    DDID_CLOCK_SELECT_DPLL4 = 0x2


class ENUM_IREF_INVERSE_REF(Enum):
    IREF_INVERSE_REF_NOT_INVERSE = 0x0
    IREF_INVERSE_REF_INVERSE = 0x1


class OFFSET_DPCLKA_CFGCR0:
    DPCLKA_CFGCR0 = 0x164280


class _DPCLKA_CFGCR0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiaClockSelect', ctypes.c_uint32, 2),
        ('DdibClockSelect', ctypes.c_uint32, 2),
        ('DdicClockSelect', ctypes.c_uint32, 2),
        ('Reserved6', ctypes.c_uint32, 4),
        ('DdiaClockOff', ctypes.c_uint32, 1),
        ('DdibClockOff', ctypes.c_uint32, 1),
        ('DdicClockOff', ctypes.c_uint32, 1),
        ('DdidClockOff', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 1),
        ('Dpll0InverseRef', ctypes.c_uint32, 1),
        ('Dpll1InverseRef', ctypes.c_uint32, 1),
        ('Dpll4InverseRef', ctypes.c_uint32, 1),
        ('Dpll0EnableOverride', ctypes.c_uint32, 1),
        ('Dpll1EnableOverride', ctypes.c_uint32, 1),
        ('Dpll4EnableOverride', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 6),
        ('DdidClockSelect', ctypes.c_uint32, 2),
        ('Reserved29', ctypes.c_uint32, 1),
        ('IrefInverseRef', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_DPCLKA_CFGCR0(ctypes.Union):
    value = 0
    offset = 0

    DdiaClockSelect = 0  # bit 0 to 2
    DdibClockSelect = 0  # bit 2 to 4
    DdicClockSelect = 0  # bit 4 to 6
    Reserved6 = 0  # bit 6 to 10
    DdiaClockOff = 0  # bit 10 to 11
    DdibClockOff = 0  # bit 11 to 12
    DdicClockOff = 0  # bit 12 to 13
    DdidClockOff = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 15
    Dpll0InverseRef = 0  # bit 15 to 16
    Dpll1InverseRef = 0  # bit 16 to 17
    Dpll4InverseRef = 0  # bit 17 to 18
    Dpll0EnableOverride = 0  # bit 18 to 19
    Dpll1EnableOverride = 0  # bit 19 to 20
    Dpll4EnableOverride = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 27
    DdidClockSelect = 0  # bit 27 to 29
    Reserved29 = 0  # bit 29 to 30
    IrefInverseRef = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPCLKA_CFGCR0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPCLKA_CFGCR0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CD_FREQUENCY_DECIMAL(Enum):
    CD_FREQUENCY_DECIMAL_168_MHZ_CD = 0x14E  # This value is default, but not valid.
    CD_FREQUENCY_DECIMAL_172_8_MHZ_CD = 0x158
    CD_FREQUENCY_DECIMAL_179_2_MHZ_CD = 0x164
    CD_FREQUENCY_DECIMAL_180_MHZ_CD = 0x166
    CD_FREQUENCY_DECIMAL_192_MHZ_CD = 0x17E
    CD_FREQUENCY_DECIMAL_307_2_MHZ_CD = 0x264
    CD_FREQUENCY_DECIMAL_312_MHZ_CD = 0x26E
    CD_FREQUENCY_DECIMAL_324_MHZ_CD = 0x286
    CD_FREQUENCY_DECIMAL_326_4MHZ_CD = 0x28B
    CD_FREQUENCY_DECIMAL_480MHZ_CD = 0x3BE
    CD_FREQUENCY_DECIMAL_552_MHZ_CD = 0x44E
    CD_FREQUENCY_DECIMAL_556_8_MHZ_CD = 0x458
    CD_FREQUENCY_DECIMAL_648_MHZ_CD = 0x50E
    CD_FREQUENCY_DECIMAL_652_8_MHZ_CD = 0x518


class ENUM_SSA_PRECHARGE_ENABLE(Enum):
    SSA_PRECHARGE_DISABLE = 0x0


class ENUM_OVERRIDE_TO_CRYSTAL(Enum):
    OVERRIDE_TO_CRYSTAL_NORMAL = 0x0
    OVERRIDE_TO_CRYSTAL_OVERRIDE = 0x1


class ENUM_OVERRIDE_TO_SLOW_CLOCK(Enum):
    OVERRIDE_TO_SLOW_CLOCK_NORMAL = 0x0
    OVERRIDE_TO_SLOW_CLOCK_OVERRIDE = 0x1


class ENUM_CD2X_PIPE_SELECT(Enum):
    CD2X_PIPE_SELECT_PIPE_A = 0x0
    CD2X_PIPE_SELECT_PIPE_B = 0x2
    CD2X_PIPE_SELECT_PIPE_C = 0x4
    CD2X_PIPE_SELECT_NONE = 0x7  # Double buffer enable is tied to 1 so that writes to the CD2X Divider Select will tak
                                 # e effect immediately.


class ENUM_CD2X_DIVIDER_SELECT(Enum):
    CD2X_DIVIDER_SELECT_DIVIDE_BY_1 = 0x0
    CD2X_DIVIDER_SELECT_DIVIDE_BY_1_5 = 0x1
    CD2X_DIVIDER_SELECT_DIVIDE_BY_2 = 0x2
    CD2X_DIVIDER_SELECT_DIVIDE_BY_4 = 0x3


class OFFSET_CDCLK_CTL:
    CDCLK_CTL = 0x46000


class _CDCLK_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CdFrequencyDecimal', ctypes.c_uint32, 11),
        ('Reserved11', ctypes.c_uint32, 4),
        ('Reserved15', ctypes.c_uint32, 1),
        ('SsaPrechargeEnable', ctypes.c_uint32, 1),
        ('OverrideToCrystal', ctypes.c_uint32, 1),
        ('OverrideToSlowClock', ctypes.c_uint32, 1),
        ('Cd2XPipeSelect', ctypes.c_uint32, 3),
        ('Cd2XDividerSelect', ctypes.c_uint32, 2),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_CDCLK_CTL(ctypes.Union):
    value = 0
    offset = 0

    CdFrequencyDecimal = 0  # bit 0 to 11
    Reserved11 = 0  # bit 11 to 15
    Reserved15 = 0  # bit 15 to 16
    SsaPrechargeEnable = 0  # bit 16 to 17
    OverrideToCrystal = 0  # bit 17 to 18
    OverrideToSlowClock = 0  # bit 18 to 19
    Cd2XPipeSelect = 0  # bit 19 to 22
    Cd2XDividerSelect = 0  # bit 22 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CDCLK_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CDCLK_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DDI0_USED(Enum):
    DDI0_USED_NOT_USED = 0x0
    DDI0_USED_USED = 0x1


class ENUM_HDMI_DP0(Enum):
    HDMI_DP0_DP = 0x0
    HDMI_DP0_HDMI = 0x1


class ENUM_DDI1_USED(Enum):
    DDI1_USED_NOT_USED = 0x0
    DDI1_USED_USED = 0x1


class ENUM_HDMI_DP1(Enum):
    HDMI_DP1_DP = 0x0
    HDMI_DP1_HDMI = 0x1


class ENUM_DDI2_USED(Enum):
    DDI2_USED_NOT_USED = 0x0
    DDI2_USED_USED = 0x1


class ENUM_HDMI_DP2(Enum):
    HDMI_DP2_DP = 0x0
    HDMI_DP2_HDMI = 0x1


class ENUM_DDI3_USED(Enum):
    DDI3_USED_NOT_USED = 0x0
    DDI3_USED_USED = 0x1


class ENUM_HDMI_DP3(Enum):
    HDMI_DP3_DP = 0x0
    HDMI_DP3_HDMI = 0x1


class ENUM_DPLL0_USED(Enum):
    DPLL0_USED_NOT_USED = 0x0
    DPLL0_USED_USED = 0x1


class ENUM_DPLL1_USED(Enum):
    DPLL1_USED_NOT_USED = 0x0
    DPLL1_USED_USED = 0x1


class ENUM_DPLL2_USED(Enum):
    DPLL2_USED_NOT_USED = 0x0
    DPLL2_USED_USED = 0x1


class ENUM_DPLL3_USED(Enum):
    DPLL3_USED_NOT_USED = 0x0
    DPLL3_USED_USED = 0x1


class OFFSET_HDPORT_STATE:
    HDPORT_STATE = 0x45050


class _HDPORT_STATE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hdport_En', ctypes.c_uint32, 1),
        ('Ddi0_Used', ctypes.c_uint32, 1),
        ('Hdmi_Dp0', ctypes.c_uint32, 1),
        ('Ddi1_Used', ctypes.c_uint32, 1),
        ('Hdmi_Dp1', ctypes.c_uint32, 1),
        ('Ddi2_Used', ctypes.c_uint32, 1),
        ('Hdmi_Dp2', ctypes.c_uint32, 1),
        ('Ddi3_Used', ctypes.c_uint32, 1),
        ('Hdmi_Dp3', ctypes.c_uint32, 1),
        ('Spare_9', ctypes.c_uint32, 1),
        ('Spare_10', ctypes.c_uint32, 1),
        ('Spare_11', ctypes.c_uint32, 1),
        ('Dpll0_Used', ctypes.c_uint32, 1),
        ('Dpll1_Used', ctypes.c_uint32, 1),
        ('Dpll2_Used', ctypes.c_uint32, 1),
        ('Dpll3_Used', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_HDPORT_STATE(ctypes.Union):
    value = 0
    offset = 0

    Hdport_En = 0  # bit 0 to 1
    Ddi0_Used = 0  # bit 1 to 2
    Hdmi_Dp0 = 0  # bit 2 to 3
    Ddi1_Used = 0  # bit 3 to 4
    Hdmi_Dp1 = 0  # bit 4 to 5
    Ddi2_Used = 0  # bit 5 to 6
    Hdmi_Dp2 = 0  # bit 6 to 7
    Ddi3_Used = 0  # bit 7 to 8
    Hdmi_Dp3 = 0  # bit 8 to 9
    Spare_9 = 0  # bit 9 to 10
    Spare_10 = 0  # bit 10 to 11
    Spare_11 = 0  # bit 11 to 12
    Dpll0_Used = 0  # bit 12 to 13
    Dpll1_Used = 0  # bit 13 to 14
    Dpll2_Used = 0  # bit 14 to 15
    Dpll3_Used = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDPORT_STATE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDPORT_STATE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

