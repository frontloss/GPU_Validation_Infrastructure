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
# @file JslPllRegs.py
# @brief contains JslPllRegs.py related register definitions

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

