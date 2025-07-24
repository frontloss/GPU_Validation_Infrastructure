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
# @file Gen11PllRegs.py
# @brief contains Gen11PllRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_DISPLAYPORT_A_PRESENT(Enum):
    DISPLAYPORT_A_PRESENT_NOT_PRESENT = 0x0  # Port not present
    DISPLAYPORT_A_PRESENT_PRESENT = 0x1  # Port present


class ENUM_PART_IS_SOC(Enum):
    PART_IS_SOC_NOT_SOC = 0x0
    PART_IS_SOC_SOC = 0x1


class ENUM_PAVP_GT_GEN_SELECT(Enum):
    PAVP_GT_GEN_SELECT_GEN11_AND_ONWARDS = 0x0
    PAVP_GT_GEN_SELECT_GEN10_AND_EARLIER = 0x1


class ENUM_WD_VIDEO_FAULT_CONTINUE(Enum):
    WD_VIDEO_FAULT_CONTINUE_STOP_WRITES = 0x0
    WD_VIDEO_FAULT_CONTINUE_CONTINUE_WRITES = 0x1


class ENUM_REFERENCE_FREQUENCY(Enum):
    REFERENCE_FREQUENCY_24_MHZ = 0x0
    REFERENCE_FREQUENCY_19_2_MHZ = 0x1
    REFERENCE_FREQUENCY_38_4_MHZ = 0x2
    REFERENCE_FREQUENCY_25_MHZ_TEST = 0x3


class OFFSET_DSSM:
    DSSM = 0x51004


class _DSSM(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayportAPresent', ctypes.c_uint32, 1),
        ('PartIsSoc', ctypes.c_uint32, 1),
        ('PavpGtGenSelect', ctypes.c_uint32, 1),
        ('WdVideoFaultContinue', ctypes.c_uint32, 1),
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
        ('ReferenceFrequency', ctypes.c_uint32, 3),
    ]


class REG_DSSM(ctypes.Union):
    value = 0
    offset = 0

    DisplayportAPresent = 0  # bit 0 to 1
    PartIsSoc = 0  # bit 1 to 2
    PavpGtGenSelect = 0  # bit 2 to 3
    WdVideoFaultContinue = 0  # bit 3 to 4
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
    ReferenceFrequency = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSSM),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSSM, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PLL_RATIO(Enum):
    PLL_RATIO_28_DEFAULT = 0x1C  # Default value. Refer to the Clocks page for valid ratios to program.


class ENUM_PLL_LOCK(Enum):
    PLL_LOCK_NOT_LOCKED_OR_NOT_ENABLED = 0x0
    PLL_LOCK_LOCKED = 0x1


class ENUM_PLL_ENABLE(Enum):
    PLL_DISABLE = 0x0
    PLL_ENABLE = 0x1


class OFFSET_CDCLK_PLL_ENABLE:
    CDCLK_PLL_ENABLE = 0x46070


class _CDCLK_PLL_ENABLE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PllRatio', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 3),
        ('Reserved11', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 10),
        ('Reserved22', ctypes.c_uint32, 2),
        ('Reserved24', ctypes.c_uint32, 2),
        ('Reserved26', ctypes.c_uint32, 2),
        ('Reserved28', ctypes.c_uint32, 2),
        ('PllLock', ctypes.c_uint32, 1),
        ('PllEnable', ctypes.c_uint32, 1),
    ]


class REG_CDCLK_PLL_ENABLE(ctypes.Union):
    value = 0
    offset = 0

    PllRatio = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 11
    Reserved11 = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 22
    Reserved22 = 0  # bit 22 to 24
    Reserved24 = 0  # bit 24 to 26
    Reserved26 = 0  # bit 26 to 28
    Reserved28 = 0  # bit 28 to 30
    PllLock = 0  # bit 30 to 31
    PllEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CDCLK_PLL_ENABLE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CDCLK_PLL_ENABLE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CD_FREQUENCY_DECIMAL(Enum):
    CD_FREQUENCY_DECIMAL_168_MHZ_CD = 0x14E  # This value is default, but not valid.
    CD_FREQUENCY_DECIMAL_172_8_MHZ_CD = 0x158
    CD_FREQUENCY_DECIMAL_180_MHZ_CD = 0x166
    CD_FREQUENCY_DECIMAL_192_MHZ_CD = 0x17E
    CD_FREQUENCY_DECIMAL_307_2_MHZ_CD = 0x264
    CD_FREQUENCY_DECIMAL_312_MHZ_CD = 0x26E
    CD_FREQUENCY_DECIMAL_324MHZ_CD = 0x286
    CD_FREQUENCY_DECIMAL_326_4MHZ_CD = 0x28B
    CD_FREQUENCY_DECIMAL_552_MHZ_CD = 0x44E
    CD_FREQUENCY_DECIMAL_556_8_MHZ_CD = 0x458
    CD_FREQUENCY_DECIMAL_648_MHZ_CD = 0x50E
    CD_FREQUENCY_DECIMAL_652_8_MHZ_CD = 0x518


class ENUM_PAR0_CD_DIVMUX_OVERRIDE(Enum):
    PAR0_CD_DIVMUX_OVERRIDE_NORMAL = 0x0  # Par0 CD source selected by hardware
    PAR0_CD_DIVMUX_OVERRIDE_OVERRIDE_TO_DIVMUX = 0x1  # Debug override Par0 CD source to Divmux output


class ENUM_SSA_PRECHARGE_ENABLE(Enum):
    SSA_PRECHARGE_DISABLE = 0x0


class ENUM_DIVMUX_CD_OVERRIDE(Enum):
    DIVMUX_CD_OVERRIDE_NORMAL = 0x0  # Divmux CD source selected by hardware
    DIVMUX_CD_OVERRIDE_OVERRIDE_TO_NONSPREAD = 0x1  # Debug override Divmux CD source to non-spread reference


class ENUM_PAR0_CD_SOURCE_OVERRIDE(Enum):
    PAR0_CD_SOURCE_OVERRIDE_NORMAL = 0x0  # Par0 CD source selected by hardware
    PAR0_CD_SOURCE_OVERRIDE_OVERRIDE_TO_NONSPREAD = 0x1  # Debug override Par0 CD source to non-spread reference


class ENUM_CD2X_PIPE_SELECT(Enum):
    CD2X_PIPE_SELECT_PIPE_A = 0x0
    CD2X_PIPE_SELECT_PIPE_B = 0x2
    CD2X_PIPE_SELECT_PIPE_C = 0x6
    CD2X_PIPE_SELECT_NONE = 0x7  # Double buffer enable is tied to 1 so that writes to the CD2X Divider Select will tak
                                 # e effect immediately.


class ENUM_CD2X_DIVIDER_SELECT(Enum):
    CD2X_DIVIDER_SELECT_DIVIDE_BY_1 = 0x0
    CD2X_DIVIDER_SELECT_DIVIDE_BY_2 = 0x2


class OFFSET_CDCLK_CTL:
    CDCLK_CTL = 0x46000


class _CDCLK_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CdFrequencyDecimal', ctypes.c_uint32, 11),
        ('Reserved11', ctypes.c_uint32, 4),
        ('Par0CdDivmuxOverride', ctypes.c_uint32, 1),
        ('SsaPrechargeEnable', ctypes.c_uint32, 1),
        ('DivmuxCdOverride', ctypes.c_uint32, 1),
        ('Par0CdSourceOverride', ctypes.c_uint32, 1),
        ('Cd2XPipeSelect', ctypes.c_uint32, 3),
        ('Cd2XDividerSelect', ctypes.c_uint32, 2),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_CDCLK_CTL(ctypes.Union):
    value = 0
    offset = 0

    CdFrequencyDecimal = 0  # bit 0 to 11
    Reserved11 = 0  # bit 11 to 15
    Par0CdDivmuxOverride = 0  # bit 15 to 16
    SsaPrechargeEnable = 0  # bit 16 to 17
    DivmuxCdOverride = 0  # bit 17 to 18
    Par0CdSourceOverride = 0  # bit 18 to 19
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


class ENUM_POWER_STATE(Enum):
    POWER_STATE_DISABLED = 0x0
    POWER_STATE_ENABLED = 0x1


class ENUM_POWER_ENABLE(Enum):
    POWER_DISABLE = 0x0
    POWER_ENABLE = 0x1


class OFFSET_DPLL_ENABLE:
    DPLL0_ENABLE = 0x46010
    DPLL1_ENABLE = 0x46014
    TBT_PLL_ENABLE = 0x46020
    MGPLL1_ENABLE = 0x46030
    MGPLL2_ENABLE = 0x46034
    MGPLL3_ENABLE = 0x46038
    MGPLL4_ENABLE = 0x4603C
    MGPLL5_ENABLE = 0x46040
    MGPLL6_ENABLE = 0x46044
    MGPLL7_ENABLE = 0x46048
    MGPLL8_ENABLE = 0x4604C


class _DPLL_ENABLE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 11),
        ('Reserved11', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 14),
        ('PowerState', ctypes.c_uint32, 1),
        ('PowerEnable', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 1),
        ('PllLock', ctypes.c_uint32, 1),
        ('PllEnable', ctypes.c_uint32, 1),
    ]


class REG_DPLL_ENABLE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 11
    Reserved11 = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 26
    PowerState = 0  # bit 26 to 27
    PowerEnable = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 30
    PllLock = 0  # bit 30 to 31
    PllEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLL_ENABLE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLL_ENABLE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SSC_ENABLE(Enum):
    SSC_DISABLE = 0x0
    SSC_ENABLE = 0x1


class OFFSET_DPLL_CFGCR0:
    DPLL0_CFGCR0 = 0x164000
    DPLL1_CFGCR0 = 0x164080
    TBTPLL_CFGCR0 = 0x164100
    DPLL4_CFGCR0 = 0x164200


class _DPLL_CFGCR0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DcoInteger', ctypes.c_uint32, 10),
        ('DcoFraction', ctypes.c_uint32, 15),
        ('SscEnable', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 6),
    ]


class REG_DPLL_CFGCR0(ctypes.Union):
    value = 0
    offset = 0

    DcoInteger = 0  # bit 0 to 10
    DcoFraction = 0  # bit 10 to 25
    SscEnable = 0  # bit 25 to 26
    Reserved26 = 0  # bit 26 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLL_CFGCR0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLL_CFGCR0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CENTRAL_FREQUENCY(Enum):
    CENTRAL_FREQUENCY_9600_MHZ = 0x0
    CENTRAL_FREQUENCY_9000_MHZ = 0x1
    CENTRAL_FREQUENCY_8400_MHZ = 0x3


class ENUM_PDIV(Enum):
    PDIV_2 = 0x1
    PDIV_3 = 0x2
    PDIV_5 = 0x4
    PDIV_7 = 0x8


class ENUM_KDIV(Enum):
    KDIV_1 = 0x1
    KDIV_2 = 0x2
    KDIV_3 = 0x4


class ENUM_QDIV_MODE(Enum):
    QDIV_MODE_DISABLE = 0x0  # Q divider = 1
    QDIV_MODE_ENABLE = 0x1  # Q divider = Qdiv Ratio


class OFFSET_DPLL_CFGCR1:
    DPLL0_CFGCR1 = 0x164004
    DPLL1_CFGCR1 = 0x164084
    TBTPLL_CFGCR1 = 0x164104
    DPLL4_CFGCR1 = 0x164204


class _DPLL_CFGCR1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CentralFrequency', ctypes.c_uint32, 2),
        ('Pdiv', ctypes.c_uint32, 4),
        ('Kdiv', ctypes.c_uint32, 3),
        ('QdivMode', ctypes.c_uint32, 1),
        ('QdivRatio', ctypes.c_uint32, 8),
        ('Reserved18', ctypes.c_uint32, 14),
    ]


class REG_DPLL_CFGCR1(ctypes.Union):
    value = 0
    offset = 0

    CentralFrequency = 0  # bit 0 to 2
    Pdiv = 0  # bit 2 to 6
    Kdiv = 0  # bit 6 to 9
    QdivMode = 0  # bit 9 to 10
    QdivRatio = 0  # bit 10 to 18
    Reserved18 = 0  # bit 18 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLL_CFGCR1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLL_CFGCR1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


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


class ENUM_TC1_CLOCK_OFF(Enum):
    TC1_CLOCK_OFF_ON = 0x0
    TC1_CLOCK_OFF_OFF = 0x1


class ENUM_TC2_CLOCK_OFF(Enum):
    TC2_CLOCK_OFF_ON = 0x0
    TC2_CLOCK_OFF_OFF = 0x1


class ENUM_TC3_CLOCK_OFF(Enum):
    TC3_CLOCK_OFF_ON = 0x0
    TC3_CLOCK_OFF_OFF = 0x1


class ENUM_DPLL0_INVERSE_REF(Enum):
    DPLL0_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL0_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL1_INVERSE_REF(Enum):
    DPLL1_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL1_INVERSE_REF_INVERSE = 0x1


class ENUM_TBTPLL_INVERSE_REF(Enum):
    TBTPLL_INVERSE_REF_NOT_INVERSE = 0x0
    TBTPLL_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL0_ENABLE_OVERRIDE(Enum):
    DPLL0_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL0_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_DPLL1_ENABLE_OVERRIDE(Enum):
    DPLL1_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL1_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_TBTPLL_ENABLE_OVERRIDE(Enum):
    TBTPLL_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    TBTPLL_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_TC4_CLOCK_OFF(Enum):
    TC4_CLOCK_OFF_ON = 0x0
    TC4_CLOCK_OFF_OFF = 0x1


class ENUM_TC5_CLOCK_OFF(Enum):
    TC5_CLOCK_OFF_ON = 0x0
    TC5_CLOCK_OFF_OFF = 0x1


class ENUM_TC6_CLOCK_OFF(Enum):
    TC6_CLOCK_OFF_ON = 0x0
    TC6_CLOCK_OFF_OFF = 0x1


class ENUM_DDIC_CLOCK_OFF(Enum):
    DDIC_CLOCK_OFF_ON = 0x0
    DDIC_CLOCK_OFF_OFF = 0x1


class ENUM_DPLL3_INVERSE_REF(Enum):
    DPLL3_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL3_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL4_INVERSE_REF(Enum):
    DPLL4_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL4_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL4_ENABLE_OVERRIDE(Enum):
    DPLL4_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL4_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_IREF_INVERSE_REF(Enum):
    IREF_INVERSE_REF_NOT_INVERSE = 0x0
    IREF_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL3_ENABLE_OVERRIDE(Enum):
    DPLL3_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL3_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class OFFSET_DPCLKA_CFGCR0:
    DPCLKA_CFGCR0 = 0x164280


class _DPCLKA_CFGCR0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiaClockSelect', ctypes.c_uint32, 2),
        ('DdibClockSelect', ctypes.c_uint32, 2),
        ('DdicClockSelect', ctypes.c_uint32, 2),
        ('MipiaHvmSel', ctypes.c_uint32, 2),
        ('MipicHvmSel', ctypes.c_uint32, 2),
        ('DdiaClockOff', ctypes.c_uint32, 1),
        ('DdibClockOff', ctypes.c_uint32, 1),
        ('Tc1ClockOff', ctypes.c_uint32, 1),
        ('Tc2ClockOff', ctypes.c_uint32, 1),
        ('Tc3ClockOff', ctypes.c_uint32, 1),
        ('Dpll0InverseRef', ctypes.c_uint32, 1),
        ('Dpll1InverseRef', ctypes.c_uint32, 1),
        ('TbtpllInverseRef', ctypes.c_uint32, 1),
        ('Dpll0EnableOverride', ctypes.c_uint32, 1),
        ('Dpll1EnableOverride', ctypes.c_uint32, 1),
        ('TbtpllEnableOverride', ctypes.c_uint32, 1),
        ('Tc4ClockOff', ctypes.c_uint32, 1),
        ('Tc5ClockOff', ctypes.c_uint32, 1),
        ('Tc6ClockOff', ctypes.c_uint32, 1),
        ('DdicClockOff', ctypes.c_uint32, 1),
        ('Dpll3InverseRef', ctypes.c_uint32, 1),
        ('Dpll4InverseRef', ctypes.c_uint32, 1),
        ('Dpll4EnableOverride', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 1),
        ('HvmIndependentMipiEnable', ctypes.c_uint32, 1),
        ('IrefInverseRef', ctypes.c_uint32, 1),
        ('Dpll3EnableOverride', ctypes.c_uint32, 1),
    ]


class REG_DPCLKA_CFGCR0(ctypes.Union):
    value = 0
    offset = 0

    DdiaClockSelect = 0  # bit 0 to 2
    DdibClockSelect = 0  # bit 2 to 4
    DdicClockSelect = 0  # bit 4 to 6
    MipiaHvmSel = 0  # bit 6 to 8
    MipicHvmSel = 0  # bit 8 to 10
    DdiaClockOff = 0  # bit 10 to 11
    DdibClockOff = 0  # bit 11 to 12
    Tc1ClockOff = 0  # bit 12 to 13
    Tc2ClockOff = 0  # bit 13 to 14
    Tc3ClockOff = 0  # bit 14 to 15
    Dpll0InverseRef = 0  # bit 15 to 16
    Dpll1InverseRef = 0  # bit 16 to 17
    TbtpllInverseRef = 0  # bit 17 to 18
    Dpll0EnableOverride = 0  # bit 18 to 19
    Dpll1EnableOverride = 0  # bit 19 to 20
    TbtpllEnableOverride = 0  # bit 20 to 21
    Tc4ClockOff = 0  # bit 21 to 22
    Tc5ClockOff = 0  # bit 22 to 23
    Tc6ClockOff = 0  # bit 23 to 24
    DdicClockOff = 0  # bit 24 to 25
    Dpll3InverseRef = 0  # bit 25 to 26
    Dpll4InverseRef = 0  # bit 26 to 27
    Dpll4EnableOverride = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 29
    HvmIndependentMipiEnable = 0  # bit 29 to 30
    IrefInverseRef = 0  # bit 30 to 31
    Dpll3EnableOverride = 0  # bit 31 to 32

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


class ENUM_CLOCK_SELECT(Enum):
    CLOCK_SELECT_NONE = 0x0  # Nothing selected. Clock is disabled for this DDI.
    CLOCK_SELECT_MG = 0x8  # MG PLL output
    CLOCK_SELECT_TBT_162 = 0xC  # Thunderbolt 162 MHz
    CLOCK_SELECT_TBT_270 = 0xD  # Thunderbolt 270 MHz
    CLOCK_SELECT_TBT_540 = 0xE  # Thunderbolt 540 MHz
    CLOCK_SELECT_TBT_810 = 0xF  # Thunderbolt 810 MHz


class OFFSET_DDI_CLK_SEL:
    DDI_CLK_SEL_C = 0x46108
    DDI_CLK_SEL_D = 0x4610C
    DDI_CLK_SEL_E = 0x46110
    DDI_CLK_SEL_F = 0x46114
    DDI_CLK_SEL_G = 0x46118
    DDI_CLK_SEL_H = 0x4611C


class _DDI_CLK_SEL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 28),
        ('ClockSelect', ctypes.c_uint32, 4),
    ]


class REG_DDI_CLK_SEL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 28
    ClockSelect = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DDI_CLK_SEL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DDI_CLK_SEL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_ESC_CLK_DIV:
    DSI_ESC_CLK_DIV_0 = 0x6B090
    DSI_ESC_CLK_DIV_1 = 0x6B890


class _DSI_ESC_CLK_DIV(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EscapeClockDividerM', ctypes.c_uint32, 9),
        ('Reserved9', ctypes.c_uint32, 7),
        ('ByteClocksPerEscapeClock', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DSI_ESC_CLK_DIV(ctypes.Union):
    value = 0
    offset = 0

    EscapeClockDividerM = 0  # bit 0 to 9
    Reserved9 = 0  # bit 9 to 16
    ByteClocksPerEscapeClock = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_ESC_CLK_DIV),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_ESC_CLK_DIV, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPHY_ESC_CLK_DIV:
    DPHY_ESC_CLK_DIV_1 = 0x6C190
    DPHY_ESC_CLK_DIV_0 = 0x162190


class _DPHY_ESC_CLK_DIV(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EscapeClockDividerM', ctypes.c_uint32, 9),
        ('Reserved9', ctypes.c_uint32, 7),
        ('ByteClocksPerEscapeClock', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DPHY_ESC_CLK_DIV(ctypes.Union):
    value = 0
    offset = 0

    EscapeClockDividerM = 0  # bit 0 to 9
    Reserved9 = 0  # bit 9 to 16
    ByteClocksPerEscapeClock = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPHY_ESC_CLK_DIV),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPHY_ESC_CLK_DIV, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_I_FRACNEN_H(Enum):
    I_FRACNEN_H_DISABLE = 0x0
    I_FRACNEN_H_ENABLE = 0x1


class ENUM_I_DIRECT_PIN_IF_EN(Enum):
    I_DIRECT_PIN_IF_EN_REGISTER_IF = 0x0
    I_DIRECT_PIN_IF_EN_DIRECT_PIN_IF = 0x1


class OFFSET_MG_PLL_DIV0:
    MG_PLL1_DIV0_PORT1 = 0x168A00
    MG_PLL1_DIV0_PORT2 = 0x169A00
    MG_PLL1_DIV0_PORT3 = 0x16AA00
    MG_PLL1_DIV0_PORT4 = 0x16BA00


class _MG_PLL_DIV0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Fbdiv_Intgr', ctypes.c_uint32, 8),
        ('I_Fbdiv_Frac', ctypes.c_uint32, 22),
        ('I_Fracnen_H', ctypes.c_uint32, 1),
        ('I_Direct_Pin_If_En', ctypes.c_uint32, 1),
    ]


class REG_MG_PLL_DIV0(ctypes.Union):
    value = 0
    offset = 0

    I_Fbdiv_Intgr = 0  # bit 0 to 8
    I_Fbdiv_Frac = 0  # bit 8 to 30
    I_Fracnen_H = 0  # bit 30 to 31
    I_Direct_Pin_If_En = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_PLL_DIV0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_PLL_DIV0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_I_FBPREDIV(Enum):
    I_FBPREDIV_DIV2 = 0x2
    I_FBPREDIV_DIV4 = 0x4


class ENUM_I_NDIVRATIO(Enum):
    I_NDIVRATIO_DIV1 = 0x0
    I_NDIVRATIO_DIV1DEFAULT = 0x1
    I_NDIVRATIO_DIV2 = 0x2
    I_NDIVRATIO_DIV3 = 0x3
    I_NDIVRATIO_DIV5 = 0x5
    I_NDIVRATIO_DIV7 = 0x7


class ENUM_I_DUTYCYCCORR_EN_H(Enum):
    I_DUTYCYCCORR_EN_H_DISABLE = 0x0
    I_DUTYCYCCORR_EN_H_ENABLE = 0x1


class ENUM_I_PLLLC_REG_FBCLKEXT_SEL(Enum):
    I_PLLLC_REG_FBCLKEXT_SEL_FBCLK_FROM_PLL_CORE = 0x0
    I_PLLLC_REG_FBCLKEXT_SEL_EXTFBCLK = 0x1


class ENUM_I_PLLLC_REG_LONGLOOPCLK_SEL(Enum):
    I_PLLLC_REG_LONGLOOPCLK_SEL_DCO_CLK_FROM_PLL_CORE_FOR_TIGHT_LOOP = 0x0
    I_PLLLC_REG_LONGLOOPCLK_SEL_EXTERNAL_DIVIDED_DCO_CLOCK_FOR_LONG_LOOP = 0x1


class ENUM_I_DIVRETIMEREN(Enum):
    I_DIVRETIMEREN_DISABLE = 0x0
    I_DIVRETIMEREN_ENABLE = 0x1


class ENUM_I_DITHER_DIV(Enum):
    I_DITHER_DIV_1 = 0x0
    I_DITHER_DIV_2 = 0x1
    I_DITHER_DIV_4 = 0x2
    I_DITHER_DIV_8 = 0x3


class ENUM_I_IREF_NDIVRATIO(Enum):
    I_IREF_NDIVRATIO_DIV1 = 0x1
    I_IREF_NDIVRATIO_DIV2 = 0x2
    I_IREF_NDIVRATIO_DIV4 = 0x4


class ENUM_I_DFX_DIV_CKLO(Enum):
    I_DFX_DIV_CKLO_2 = 0x0
    I_DFX_DIV_CKLO_3 = 0x1
    I_DFX_DIV_CKLO_5 = 0x2
    I_DFX_DIV_CKLO_7 = 0x3


class ENUM_I_DFX_DIV_CKHI(Enum):
    I_DFX_DIV_CKHI_2 = 0x0
    I_DFX_DIV_CKHI_3 = 0x1
    I_DFX_DIV_CKHI_5 = 0x2
    I_DFX_DIV_CKHI_7 = 0x3


class OFFSET_MG_PLL_DIV1:
    MG_PLL1_DIV1_PORT1 = 0x168A04
    MG_PLL1_DIV1_PORT2 = 0x169A04
    MG_PLL1_DIV1_PORT3 = 0x16AA04
    MG_PLL1_DIV1_PORT4 = 0x16BA04


class _MG_PLL_DIV1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Fbprediv', ctypes.c_uint32, 4),
        ('I_Ndivratio', ctypes.c_uint32, 4),
        ('I_Dutycyccorr_En_H', ctypes.c_uint32, 1),
        ('I_Plllc_Reg_Fbclkext_Sel', ctypes.c_uint32, 1),
        ('I_Plllc_Reg_Longloopclk_Sel', ctypes.c_uint32, 1),
        ('I_Divretimeren', ctypes.c_uint32, 1),
        ('I_Dither_Div', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 2),
        ('I_Iref_Ndivratio', ctypes.c_uint32, 3),
        ('Reserved19', ctypes.c_uint32, 5),
        ('I_Rodiv_Sel', ctypes.c_uint32, 4),
        ('I_Dfx_Div_Cklo', ctypes.c_uint32, 2),
        ('I_Dfx_Div_Ckhi', ctypes.c_uint32, 2),
    ]


class REG_MG_PLL_DIV1(ctypes.Union):
    value = 0
    offset = 0

    I_Fbprediv = 0  # bit 0 to 4
    I_Ndivratio = 0  # bit 4 to 8
    I_Dutycyccorr_En_H = 0  # bit 8 to 9
    I_Plllc_Reg_Fbclkext_Sel = 0  # bit 9 to 10
    I_Plllc_Reg_Longloopclk_Sel = 0  # bit 10 to 11
    I_Divretimeren = 0  # bit 11 to 12
    I_Dither_Div = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 16
    I_Iref_Ndivratio = 0  # bit 16 to 19
    Reserved19 = 0  # bit 19 to 24
    I_Rodiv_Sel = 0  # bit 24 to 28
    I_Dfx_Div_Cklo = 0  # bit 28 to 30
    I_Dfx_Div_Ckhi = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_PLL_DIV1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_PLL_DIV1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_I_FEEDFWRDCAL_EN_H(Enum):
    I_FEEDFWRDCAL_EN_H_DISABLE = 0x0
    I_FEEDFWRDCAL_EN_H_ENABLE = 0x1


class ENUM_I_FEEDFWRDCAL_PAUSE_H(Enum):
    I_FEEDFWRDCAL_PAUSE_H_DISABLE = 0x0
    I_FEEDFWRDCAL_PAUSE_H_ENABLE = 0x1


class ENUM_I_DCODITHEREN_H(Enum):
    I_DCODITHEREN_H_DISABLE = 0x0
    I_DCODITHEREN_H_ENABLE = 0x1


class ENUM_I_DCODITHER_CONFIG(Enum):
    I_DCODITHER_CONFIG_NO_FLOATING_DITHER = 0x0
    I_DCODITHER_CONFIG_FLOATING_DITHER = 0x1


class ENUM_I_EARLYLOCK_CRITERIA(Enum):
    I_EARLYLOCK_CRITERIA_16 = 0x0
    I_EARLYLOCK_CRITERIA_32 = 0x1
    I_EARLYLOCK_CRITERIA_48 = 0x2
    I_EARLYLOCK_CRITERIA_64 = 0x3


class ENUM_I_TRUELOCK_CRITERIA(Enum):
    I_TRUELOCK_CRITERIA_16 = 0x0
    I_TRUELOCK_CRITERIA_32 = 0x1
    I_TRUELOCK_CRITERIA_48 = 0x2
    I_TRUELOCK_CRITERIA_64 = 0x3


class ENUM_I_DITHER_OVRD(Enum):
    I_DITHER_OVRD_DISABLE = 0x0
    I_DITHER_OVRD_ENABLE = 0x1


class ENUM_I_PLLLC_RESTORE_MODE_CTRL(Enum):
    I_PLLLC_RESTORE_MODE_CTRL_DIRECT_PIN_IF = 0x0
    I_PLLLC_RESTORE_MODE_CTRL_REGISTER_IF = 0x1


class ENUM_I_PLLRAMPEN_H(Enum):
    I_PLLRAMPEN_H_DISABLE = 0x0
    I_PLLRAMPEN_H_ENABLE = 0x1


class OFFSET_MG_PLL_FRAC_LOCK:
    MG_PLL1_FRAC_LOCK_PORT1 = 0x168A0C
    MG_PLL1_FRAC_LOCK_PORT2 = 0x169A0C
    MG_PLL1_FRAC_LOCK_PORT3 = 0x16AA0C
    MG_PLL1_FRAC_LOCK_PORT4 = 0x16BA0C


class _MG_PLL_FRAC_LOCK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Feedfwrdgain', ctypes.c_uint32, 8),
        ('I_Feedfwrdcal_En_H', ctypes.c_uint32, 1),
        ('I_Feedfwrdcal_Pause_H', ctypes.c_uint32, 1),
        ('I_Dcoditheren_H', ctypes.c_uint32, 1),
        ('I_Lockthresh', ctypes.c_uint32, 4),
        ('I_Dcodither_Config', ctypes.c_uint32, 1),
        ('I_Earlylock_Criteria', ctypes.c_uint32, 2),
        ('I_Truelock_Criteria', ctypes.c_uint32, 2),
        ('I_Lf_Half_Cyc_En', ctypes.c_uint32, 1),
        ('I_Dither_Ovrd', ctypes.c_uint32, 1),
        ('I_Plllc_Restore_Reg', ctypes.c_uint32, 1),
        ('I_Plllc_Restore_Mode_Ctrl', ctypes.c_uint32, 1),
        ('I_Pllrampen_H', ctypes.c_uint32, 1),
        ('I_Fbdiv_Strobe_H', ctypes.c_uint32, 1),
        ('I_Ovc_Snapshot_H', ctypes.c_uint32, 1),
        ('I_Dither_Value', ctypes.c_uint32, 5),
    ]


class REG_MG_PLL_FRAC_LOCK(ctypes.Union):
    value = 0
    offset = 0

    I_Feedfwrdgain = 0  # bit 0 to 8
    I_Feedfwrdcal_En_H = 0  # bit 8 to 9
    I_Feedfwrdcal_Pause_H = 0  # bit 9 to 10
    I_Dcoditheren_H = 0  # bit 10 to 11
    I_Lockthresh = 0  # bit 11 to 15
    I_Dcodither_Config = 0  # bit 15 to 16
    I_Earlylock_Criteria = 0  # bit 16 to 18
    I_Truelock_Criteria = 0  # bit 18 to 20
    I_Lf_Half_Cyc_En = 0  # bit 20 to 21
    I_Dither_Ovrd = 0  # bit 21 to 22
    I_Plllc_Restore_Reg = 0  # bit 22 to 23
    I_Plllc_Restore_Mode_Ctrl = 0  # bit 23 to 24
    I_Pllrampen_H = 0  # bit 24 to 25
    I_Fbdiv_Strobe_H = 0  # bit 25 to 26
    I_Ovc_Snapshot_H = 0  # bit 26 to 27
    I_Dither_Value = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_PLL_FRAC_LOCK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_PLL_FRAC_LOCK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_I_FLL_EN_H(Enum):
    I_FLL_EN_H_DISABLE = 0x0
    I_FLL_EN_H_ENABLE = 0x1


class ENUM_I_TDC_FINE_RES(Enum):
    I_TDC_FINE_RES_COARSE_RESOLUTION_DIV_8 = 0x0
    I_TDC_FINE_RES_COARSE_RESOLUTION_DIV_4 = 0x1


class ENUM_I_AFC_DIVRATIO(Enum):
    I_AFC_DIVRATIO_DCO_DIV_4 = 0x0
    I_AFC_DIVRATIO_DCO_DIV_8 = 0x1


class ENUM_I_AFCCNTSEL(Enum):
    I_AFCCNTSEL_256 = 0x0
    I_AFCCNTSEL_512 = 0x1


class ENUM_I_AFC_STARTUP(Enum):
    I_AFC_STARTUP_MID = 0x0
    I_AFC_STARTUP_UPPER_3_4 = 0x1
    I_AFC_STARTUP_UPPER_1_4 = 0x2
    I_AFC_STARTUP_LOWER_1_4 = 0x3


class OFFSET_MG_PLL_LF:
    MG_PLL1_LF_PORT1 = 0x168A08
    MG_PLL1_LF_PORT2 = 0x169A08
    MG_PLL1_LF_PORT3 = 0x16AA08
    MG_PLL1_LF_PORT4 = 0x16BA08


class _MG_PLL_LF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Prop_Coeff', ctypes.c_uint32, 4),
        ('I_Fll_Int_Coeff', ctypes.c_uint32, 4),
        ('I_Int_Coeff', ctypes.c_uint32, 5),
        ('I_Fll_En_H', ctypes.c_uint32, 1),
        ('I_Tdc_Fine_Res', ctypes.c_uint32, 1),
        ('Reserved15', ctypes.c_uint32, 1),
        ('I_Gainctrl', ctypes.c_uint32, 3),
        ('I_Afc_Divratio', ctypes.c_uint32, 1),
        ('I_Afccntsel', ctypes.c_uint32, 1),
        ('I_Afc_Startup', ctypes.c_uint32, 2),
        ('I_Dcofine_Resolution', ctypes.c_uint32, 1),
        ('I_Tdctargetcnt', ctypes.c_uint32, 8),
    ]


class REG_MG_PLL_LF(ctypes.Union):
    value = 0
    offset = 0

    I_Prop_Coeff = 0  # bit 0 to 4
    I_Fll_Int_Coeff = 0  # bit 4 to 8
    I_Int_Coeff = 0  # bit 8 to 13
    I_Fll_En_H = 0  # bit 13 to 14
    I_Tdc_Fine_Res = 0  # bit 14 to 15
    Reserved15 = 0  # bit 15 to 16
    I_Gainctrl = 0  # bit 16 to 19
    I_Afc_Divratio = 0  # bit 19 to 20
    I_Afccntsel = 0  # bit 20 to 21
    I_Afc_Startup = 0  # bit 21 to 23
    I_Dcofine_Resolution = 0  # bit 23 to 24
    I_Tdctargetcnt = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_PLL_LF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_PLL_LF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_OD_CLKTOP_CORECLKA_DIVRETIMEREN_H(Enum):
    OD_CLKTOP_CORECLKA_DIVRETIMEREN_H_ODD_DIV_RATIO = 0x0
    OD_CLKTOP_CORECLKA_DIVRETIMEREN_H_EVEN_DIV_RATIO = 0x1


class ENUM_OD_CLKTOP_CORECLKA_BYPASS(Enum):
    OD_CLKTOP_CORECLKA_BYPASS_DISABLE = 0x0
    OD_CLKTOP_CORECLKA_BYPASS_ENABLE = 0x1


class ENUM_OD_CLKTOP_CORECLKB_DIVRETIMEREN_H(Enum):
    OD_CLKTOP_CORECLKB_DIVRETIMEREN_H_ODD_DIV_RATIO = 0x0
    OD_CLKTOP_CORECLKB_DIVRETIMEREN_H_EVEN_DIV_RATIO = 0x1


class ENUM_OD_CLKTOP_CORECLKB_BYPASS(Enum):
    OD_CLKTOP_CORECLKB_BYPASS_DISABLE = 0x0
    OD_CLKTOP_CORECLKB_BYPASS_ENABLE = 0x1


class ENUM_OD_CLKTOP_CORECLKC_DIVRETIMEREN_H(Enum):
    OD_CLKTOP_CORECLKC_DIVRETIMEREN_H_ODD_DIV_RATIO = 0x0
    OD_CLKTOP_CORECLKC_DIVRETIMEREN_H_EVEN_DIV_RATIO = 0x1


class ENUM_OD_CLKTOP_CORECLKC_BYPASS(Enum):
    OD_CLKTOP_CORECLKC_BYPASS_DISABLE = 0x0
    OD_CLKTOP_CORECLKC_BYPASS_ENABLE = 0x1


class ENUM_OD_CLKTOP_CORECLKD_DIVRETIMEREN_H(Enum):
    OD_CLKTOP_CORECLKD_DIVRETIMEREN_H_ODD_DIV_RATIO = 0x0
    OD_CLKTOP_CORECLKD_DIVRETIMEREN_H_EVEN_DIV_RATIO = 0x1


class ENUM_OD_CLKTOP_CORECLKD_BYPASS(Enum):
    OD_CLKTOP_CORECLKD_BYPASS_DISABLE = 0x0
    OD_CLKTOP_CORECLKD_BYPASS_ENABLE = 0x1


class OFFSET_MG_CLKTOP_CORECLKCTL1:
    MG_CLKTOP2_CORECLKCTL1_PORT1 = 0x1688D8
    MG_CLKTOP2_CORECLKCTL1_PORT2 = 0x1698D8
    MG_CLKTOP2_CORECLKCTL1_PORT3 = 0x16A8D8
    MG_CLKTOP2_CORECLKCTL1_PORT4 = 0x16B8D8


class _MG_CLKTOP_CORECLKCTL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('Od_Clktop_Coreclka_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop_Coreclka_Bypass', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 1),
        ('Od_Clktop_Coreclkb_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop_Coreclkb_Bypass', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 2),
        ('Od_Clktop_Coreclka_Divratio', ctypes.c_uint32, 8),
        ('Od_Clktop_Coreclkb_Divratio', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 1),
        ('Od_Clktop_Coreclkc_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop_Coreclkc_Bypass', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 1),
        ('Od_Clktop_Coreclkd_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop_Coreclkd_Bypass', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_MG_CLKTOP_CORECLKCTL1(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    Od_Clktop_Coreclka_Divretimeren_H = 0  # bit 1 to 2
    Od_Clktop_Coreclka_Bypass = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 4
    Od_Clktop_Coreclkb_Divretimeren_H = 0  # bit 4 to 5
    Od_Clktop_Coreclkb_Bypass = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 8
    Od_Clktop_Coreclka_Divratio = 0  # bit 8 to 16
    Od_Clktop_Coreclkb_Divratio = 0  # bit 16 to 24
    Reserved24 = 0  # bit 24 to 25
    Od_Clktop_Coreclkc_Divretimeren_H = 0  # bit 25 to 26
    Od_Clktop_Coreclkc_Bypass = 0  # bit 26 to 27
    Reserved27 = 0  # bit 27 to 28
    Od_Clktop_Coreclkd_Divretimeren_H = 0  # bit 28 to 29
    Od_Clktop_Coreclkd_Bypass = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_CLKTOP_CORECLKCTL1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_CLKTOP_CORECLKCTL1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_OD_CLKTOP_HSDIV_EN_H(Enum):
    OD_CLKTOP_HSDIV_EN_H_DISABLE = 0x0
    OD_CLKTOP_HSDIV_EN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP_DSDIV_EN_H(Enum):
    OD_CLKTOP_DSDIV_EN_H_DISABLE = 0x0
    OD_CLKTOP_DSDIV_EN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP_TLINEDRV_ENRIGHT_H_OVRD(Enum):
    OD_CLKTOP_TLINEDRV_ENRIGHT_H_OVRD_DISABLE = 0x0
    OD_CLKTOP_TLINEDRV_ENRIGHT_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP_TLINEDRV_ENLEFT_H_OVRD(Enum):
    OD_CLKTOP_TLINEDRV_ENLEFT_H_OVRD_DISABLE = 0x0
    OD_CLKTOP_TLINEDRV_ENLEFT_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP_TLINEDRV_ENRIGHT_DED_H_OVRD(Enum):
    OD_CLKTOP_TLINEDRV_ENRIGHT_DED_H_OVRD_DISABLE = 0x0
    OD_CLKTOP_TLINEDRV_ENRIGHT_DED_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP_TLINEDRV_ENLEFT_DED_H_OVRD(Enum):
    OD_CLKTOP_TLINEDRV_ENLEFT_DED_H_OVRD_DISABLE = 0x0
    OD_CLKTOP_TLINEDRV_ENLEFT_DED_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP_TLINEDRV_OVERRIDEEN(Enum):
    OD_CLKTOP_TLINEDRV_OVERRIDEEN_DISABLE = 0x0
    OD_CLKTOP_TLINEDRV_OVERRIDEEN_ENABLE = 0x1


class ENUM_OD_CLKTOP_DSDIV_DIVRATIO(Enum):
    OD_CLKTOP_DSDIV_DIVRATIO_DIVIDE_BY_2 = 0x2
    OD_CLKTOP_DSDIV_DIVRATIO_DIVIDE_BY_3 = 0x3
    OD_CLKTOP_DSDIV_DIVRATIO_DIVIDE_BY_4 = 0x4
    OD_CLKTOP_DSDIV_DIVRATIO_DIVIDE_BY_5 = 0x5
    OD_CLKTOP_DSDIV_DIVRATIO_DIVIDE_BY_6 = 0x6
    OD_CLKTOP_DSDIV_DIVRATIO_DIVIDE_BY_7 = 0x7
    OD_CLKTOP_DSDIV_DIVRATIO_DIVIDE_BY_8 = 0x8
    OD_CLKTOP_DSDIV_DIVRATIO_DIVIDE_BY_9 = 0x9
    OD_CLKTOP_DSDIV_DIVRATIO_DIVIDE_BY_10 = 0xA


class ENUM_OD_CLKTOP_HSDIV_DIVRATIO(Enum):
    OD_CLKTOP_HSDIV_DIVRATIO_DIVIDE_BY_2 = 0x0
    OD_CLKTOP_HSDIV_DIVRATIO_DIVIDE_BY_3 = 0x1
    OD_CLKTOP_HSDIV_DIVRATIO_DIVIDE_BY_5 = 0x2
    OD_CLKTOP_HSDIV_DIVRATIO_DIVIDE_BY_7 = 0x3


class ENUM_OD_CLKTOP_TLINEDRV_CLKSEL(Enum):
    OD_CLKTOP_TLINEDRV_CLKSEL_HSCLKDIV_OUTPUT = 0x0
    OD_CLKTOP_TLINEDRV_CLKSEL_ICLK_BYPASS_INPUT_FROM_OTHER_CLKTOP = 0x1
    OD_CLKTOP_TLINEDRV_CLKSEL_DSDIV_OUTPUT_CLOCK = 0x2
    OD_CLKTOP_TLINEDRV_CLKSEL_NONDIVIDED_PLL_CLOCK = 0x3


class ENUM_OD_CLKTOP_CORECLK_INPUTSEL(Enum):
    OD_CLKTOP_CORECLK_INPUTSEL_HSDIV_OUTPUT = 0x0
    OD_CLKTOP_CORECLK_INPUTSEL_DSDIV_OUTPUT = 0x1


class ENUM_OD_CLKTOP_OUTCLK_BYPASSEN_H(Enum):
    OD_CLKTOP_OUTCLK_BYPASSEN_H_DISABLE = 0x0
    OD_CLKTOP_OUTCLK_BYPASSEN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP_CLK2OBS_EN_H(Enum):
    OD_CLKTOP_CLK2OBS_EN_H_DISABLE = 0x0
    OD_CLKTOP_CLK2OBS_EN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP_CLKOBS_MUXSEL(Enum):
    OD_CLKTOP_CLKOBS_MUXSEL_HSDIV_OUTPUT_CLOCK = 0x0
    OD_CLKTOP_CLKOBS_MUXSEL_ICLK_BYPASS_INPUT_FROM_OTHER_CLKTOP = 0x1
    OD_CLKTOP_CLKOBS_MUXSEL_DSDIV_OUTPUT_CLOCK = 0x2
    OD_CLKTOP_CLKOBS_MUXSEL_NONDIVIDED_PLL_CLOCK = 0x3


class OFFSET_MG_CLKTOP_HSCLKCTL:
    MG_CLKTOP2_HSCLKCTL_PORT1 = 0x1688D4
    MG_CLKTOP2_HSCLKCTL_PORT2 = 0x1698D4
    MG_CLKTOP2_HSCLKCTL_PORT3 = 0x16A8D4
    MG_CLKTOP2_HSCLKCTL_PORT4 = 0x16B8D4


class _MG_CLKTOP_HSCLKCTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Od_Clktop_Hsdiv_En_H', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 1),
        ('Od_Clktop_Dsdiv_En_H', ctypes.c_uint32, 1),
        ('Od_Clktop_Tlinedrv_Enright_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop_Tlinedrv_Enleft_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop_Tlinedrv_Enright_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop_Tlinedrv_Enleft_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop_Tlinedrv_Overrideen', ctypes.c_uint32, 1),
        ('Od_Clktop_Dsdiv_Divratio', ctypes.c_uint32, 4),
        ('Od_Clktop_Hsdiv_Divratio', ctypes.c_uint32, 2),
        ('Od_Clktop_Tlinedrv_Clksel', ctypes.c_uint32, 2),
        ('Od_Clktop_Coreclk_Inputsel', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 1),
        ('Od_Clktop_Outclk_Bypassen_H', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 1),
        ('Od_Clktop_Clktop_Vhfclk_Testen_H', ctypes.c_uint32, 2),
        ('Reserved22', ctypes.c_uint32, 2),
        ('Od_Clktop_Clk2Obs_En_H', ctypes.c_uint32, 1),
        ('Od_Clktop_Clkobs_Muxsel', ctypes.c_uint32, 2),
        ('Reserved27', ctypes.c_uint32, 5),
    ]


class REG_MG_CLKTOP_HSCLKCTL(ctypes.Union):
    value = 0
    offset = 0

    Od_Clktop_Hsdiv_En_H = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 2
    Od_Clktop_Dsdiv_En_H = 0  # bit 2 to 3
    Od_Clktop_Tlinedrv_Enright_H_Ovrd = 0  # bit 3 to 4
    Od_Clktop_Tlinedrv_Enleft_H_Ovrd = 0  # bit 4 to 5
    Od_Clktop_Tlinedrv_Enright_Ded_H_Ovrd = 0  # bit 5 to 6
    Od_Clktop_Tlinedrv_Enleft_Ded_H_Ovrd = 0  # bit 6 to 7
    Od_Clktop_Tlinedrv_Overrideen = 0  # bit 7 to 8
    Od_Clktop_Dsdiv_Divratio = 0  # bit 8 to 12
    Od_Clktop_Hsdiv_Divratio = 0  # bit 12 to 14
    Od_Clktop_Tlinedrv_Clksel = 0  # bit 14 to 16
    Od_Clktop_Coreclk_Inputsel = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 18
    Od_Clktop_Outclk_Bypassen_H = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 20
    Od_Clktop_Clktop_Vhfclk_Testen_H = 0  # bit 20 to 22
    Reserved22 = 0  # bit 22 to 24
    Od_Clktop_Clk2Obs_En_H = 0  # bit 24 to 25
    Od_Clktop_Clkobs_Muxsel = 0  # bit 25 to 27
    Reserved27 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_CLKTOP_HSCLKCTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_CLKTOP_HSCLKCTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MG_REFCLKIN_CTL:
    MG_REFCLKIN_CTL_PORT1 = 0x16892C
    MG_REFCLKIN_CTL_PORT2 = 0x16992C
    MG_REFCLKIN_CTL_PORT3 = 0x16A92C
    MG_REFCLKIN_CTL_PORT4 = 0x16B92C


class _MG_REFCLKIN_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Od_Refclkin1_Refclkmux', ctypes.c_uint32, 3),
        ('Od_Refclkin1_Refclkinjmux', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 4),
        ('Od_Refclkin2_Refclkmux', ctypes.c_uint32, 3),
        ('Od_Refclkin2_Refclkinjmux', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 20),
    ]


class REG_MG_REFCLKIN_CTL(ctypes.Union):
    value = 0
    offset = 0

    Od_Refclkin1_Refclkmux = 0  # bit 0 to 3
    Od_Refclkin1_Refclkinjmux = 0  # bit 3 to 4
    Reserved4 = 0  # bit 4 to 8
    Od_Refclkin2_Refclkmux = 0  # bit 8 to 11
    Od_Refclkin2_Refclkinjmux = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_REFCLKIN_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_REFCLKIN_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MG_PLL_SSC:
    MG_PLL1_SSC_PORT1 = 0x168A10
    MG_PLL1_SSC_PORT2 = 0x169A10
    MG_PLL1_SSC_PORT3 = 0x16AA10
    MG_PLL1_SSC_PORT4 = 0x16BA10


class _MG_PLL_SSC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Sscstepsize', ctypes.c_uint32, 8),
        ('I_Afc_Startup2', ctypes.c_uint32, 1),
        ('I_S_Sscfll_En_H', ctypes.c_uint32, 1),
        ('I_Sscstepnum', ctypes.c_uint32, 3),
        ('Reserved13', ctypes.c_uint32, 3),
        ('I_Sscsteplength', ctypes.c_uint32, 10),
        ('I_Ssctype', ctypes.c_uint32, 2),
        ('I_Sscen_H', ctypes.c_uint32, 1),
        ('I_Rampafc_Sscen_H', ctypes.c_uint32, 1),
        ('I_Ssc_Strobe_H', ctypes.c_uint32, 1),
        ('I_Ssc_Openloop_En_H', ctypes.c_uint32, 1),
    ]


class REG_MG_PLL_SSC(ctypes.Union):
    value = 0
    offset = 0

    I_Sscstepsize = 0  # bit 0 to 8
    I_Afc_Startup2 = 0  # bit 8 to 9
    I_S_Sscfll_En_H = 0  # bit 9 to 10
    I_Sscstepnum = 0  # bit 10 to 13
    Reserved13 = 0  # bit 13 to 16
    I_Sscsteplength = 0  # bit 16 to 26
    I_Ssctype = 0  # bit 26 to 28
    I_Sscen_H = 0  # bit 28 to 29
    I_Rampafc_Sscen_H = 0  # bit 29 to 30
    I_Ssc_Strobe_H = 0  # bit 30 to 31
    I_Ssc_Openloop_En_H = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_PLL_SSC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_PLL_SSC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MG_PLL_TDC_COLDST_BIAS:
    MG_PLL1_TDC_COLDST_BIAS_PORT1 = 0x168A18
    MG_PLL1_TDC_COLDST_BIAS_PORT2 = 0x169A18
    MG_PLL1_TDC_COLDST_BIAS_PORT3 = 0x16AA18
    MG_PLL1_TDC_COLDST_BIAS_PORT4 = 0x16BA18


class _MG_PLL_TDC_COLDST_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Tdcsel', ctypes.c_uint32, 2),
        ('I_Tdcovccorr_En_H', ctypes.c_uint32, 1),
        ('I_Tdcdc_En_H', ctypes.c_uint32, 1),
        ('I_Tdc_Offset_Lock', ctypes.c_uint32, 2),
        ('I_Swcap_Irefgen_Clkmode', ctypes.c_uint32, 2),
        ('I_Bb_Gain', ctypes.c_uint32, 3),
        ('I_Bbthresh', ctypes.c_uint32, 4),
        ('I_Bbinlock_H', ctypes.c_uint32, 1),
        ('I_Coldstart', ctypes.c_uint32, 1),
        ('I_Irefbias_Startup_Pulse_Width', ctypes.c_uint32, 2),
        ('I_Dco_Settling_Time_Cntr', ctypes.c_uint32, 4),
        ('I_Irefbias_Startup_Pulse_Bypass', ctypes.c_uint32, 1),
        ('I_Bias_Calib_Stepsize', ctypes.c_uint32, 2),
        ('I_Irefext_En', ctypes.c_uint32, 1),
        ('I_Irefint_En', ctypes.c_uint32, 1),
        ('I_Vgsbufen', ctypes.c_uint32, 1),
        ('I_Digdftswep', ctypes.c_uint32, 1),
        ('I_Irefdigdften', ctypes.c_uint32, 1),
        ('I_Iref_Refclk_Inv_En', ctypes.c_uint32, 1),
    ]


class REG_MG_PLL_TDC_COLDST_BIAS(ctypes.Union):
    value = 0
    offset = 0

    I_Tdcsel = 0  # bit 0 to 2
    I_Tdcovccorr_En_H = 0  # bit 2 to 3
    I_Tdcdc_En_H = 0  # bit 3 to 4
    I_Tdc_Offset_Lock = 0  # bit 4 to 6
    I_Swcap_Irefgen_Clkmode = 0  # bit 6 to 8
    I_Bb_Gain = 0  # bit 8 to 11
    I_Bbthresh = 0  # bit 11 to 15
    I_Bbinlock_H = 0  # bit 15 to 16
    I_Coldstart = 0  # bit 16 to 17
    I_Irefbias_Startup_Pulse_Width = 0  # bit 17 to 19
    I_Dco_Settling_Time_Cntr = 0  # bit 19 to 23
    I_Irefbias_Startup_Pulse_Bypass = 0  # bit 23 to 24
    I_Bias_Calib_Stepsize = 0  # bit 24 to 26
    I_Irefext_En = 0  # bit 26 to 27
    I_Irefint_En = 0  # bit 27 to 28
    I_Vgsbufen = 0  # bit 28 to 29
    I_Digdftswep = 0  # bit 29 to 30
    I_Irefdigdften = 0  # bit 30 to 31
    I_Iref_Refclk_Inv_En = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_PLL_TDC_COLDST_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_PLL_TDC_COLDST_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MG_PLL_BIAS:
    MG_PLL1_BIAS_PORT1 = 0x168A14
    MG_PLL1_BIAS_PORT2 = 0x169A14
    MG_PLL1_BIAS_PORT3 = 0x16AA14
    MG_PLL1_BIAS_PORT4 = 0x16BA14


class _MG_PLL_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Ireftrim', ctypes.c_uint32, 5),
        ('I_Vref_Rdac', ctypes.c_uint32, 3),
        ('I_Ctrim', ctypes.c_uint32, 5),
        ('I_Iref_Refclk_Mode', ctypes.c_uint32, 2),
        ('I_Biascal_En_H', ctypes.c_uint32, 1),
        ('I_Bias_Bonus', ctypes.c_uint32, 8),
        ('I_Init_Dcoamp', ctypes.c_uint32, 6),
        ('I_Bias_Gb_Sel', ctypes.c_uint32, 2),
    ]


class REG_MG_PLL_BIAS(ctypes.Union):
    value = 0
    offset = 0

    I_Ireftrim = 0  # bit 0 to 5
    I_Vref_Rdac = 0  # bit 5 to 8
    I_Ctrim = 0  # bit 8 to 13
    I_Iref_Refclk_Mode = 0  # bit 13 to 15
    I_Biascal_En_H = 0  # bit 15 to 16
    I_Bias_Bonus = 0  # bit 16 to 24
    I_Init_Dcoamp = 0  # bit 24 to 30
    I_Bias_Gb_Sel = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_PLL_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_PLL_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

