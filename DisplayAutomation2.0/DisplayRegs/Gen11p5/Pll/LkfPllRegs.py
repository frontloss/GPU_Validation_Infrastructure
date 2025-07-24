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
# @file LkfPllRegs.py
# @brief contains LkfPllRegs.py related register definitions

import ctypes
from enum import Enum


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


class OFFSET_DKL_PLL_DIV0_L:
    DKL_PLL1_DIV0_L = 0x200


class _DKL_PLL_DIV0_L(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Fbdiv_Intgr', ctypes.c_uint32, 8),
        ('I_Fbdiv_Frac', ctypes.c_uint32, 22),
        ('I_Fracnen_H', ctypes.c_uint32, 1),
        ('I_Direct_Pin_If_En', ctypes.c_uint32, 1),
    ]


class REG_DKL_PLL_DIV0_L(ctypes.Union):
    value = 0
    offset = 0

    I_Fbdiv_Intgr = 0  # bit 0 to 8
    I_Fbdiv_Frac = 0  # bit 8 to 30
    I_Fracnen_H = 0  # bit 30 to 31
    I_Direct_Pin_If_En = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_PLL_DIV0_L),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_PLL_DIV0_L, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_PLL_DIV1_L:
    DKL_PLL1_DIV1_L = 0x204


class _DKL_PLL_DIV1_L(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Fbprediv', ctypes.c_uint32, 4),
        ('I_Ndivratio', ctypes.c_uint32, 4),
        ('I_Dutycyccorr_En_H', ctypes.c_uint32, 1),
        ('I_Pllc_Reg_Fbclkext_Sel', ctypes.c_uint32, 1),
        ('I_Pllc_Reg_Longloopclk_Sel', ctypes.c_uint32, 1),
        ('I_Divretimer_En', ctypes.c_uint32, 1),
        ('I_Dither_Div', ctypes.c_uint32, 2),
        ('I_M1_Longloop_Sel', ctypes.c_uint32, 1),
        ('Reserved15', ctypes.c_uint32, 1),
        ('I_Bonus_Iref_Ndivratio', ctypes.c_uint32, 3),
        ('Reserved19', ctypes.c_uint32, 5),
        ('I_Rodiv_Sel', ctypes.c_uint32, 4),
        ('I_Dfx_Div_Clko', ctypes.c_uint32, 2),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_DKL_PLL_DIV1_L(ctypes.Union):
    value = 0
    offset = 0

    I_Fbprediv = 0  # bit 0 to 4
    I_Ndivratio = 0  # bit 4 to 8
    I_Dutycyccorr_En_H = 0  # bit 8 to 9
    I_Pllc_Reg_Fbclkext_Sel = 0  # bit 9 to 10
    I_Pllc_Reg_Longloopclk_Sel = 0  # bit 10 to 11
    I_Divretimer_En = 0  # bit 11 to 12
    I_Dither_Div = 0  # bit 12 to 14
    I_M1_Longloop_Sel = 0  # bit 14 to 15
    Reserved15 = 0  # bit 15 to 16
    I_Bonus_Iref_Ndivratio = 0  # bit 16 to 19
    Reserved19 = 0  # bit 19 to 24
    I_Rodiv_Sel = 0  # bit 24 to 28
    I_Dfx_Div_Clko = 0  # bit 28 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_PLL_DIV1_L),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_PLL_DIV1_L, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_PLL_LF_L:
    DKL_PLL_LF_L = 0x208


class _DKL_PLL_LF_L(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Prop_Coeff', ctypes.c_uint32, 4),
        ('I_Fll_Int_Coeff', ctypes.c_uint32, 4),
        ('I_Int_Coeff', ctypes.c_uint32, 5),
        ('I_Fll_En_H', ctypes.c_uint32, 1),
        ('I_Tdc_Fine_Res', ctypes.c_uint32, 1),
        ('I_Dcofine_Resolution', ctypes.c_uint32, 1),
        ('I_Gainctrl', ctypes.c_uint32, 3),
        ('I_Afc_Divratio', ctypes.c_uint32, 1),
        ('I_Afccntsel', ctypes.c_uint32, 1),
        ('I_Afc_Startup', ctypes.c_uint32, 2),
        ('Reserved23', ctypes.c_uint32, 1),
        ('I_Tdctargetcnt', ctypes.c_uint32, 8),
    ]


class REG_DKL_PLL_LF_L(ctypes.Union):
    value = 0
    offset = 0

    I_Prop_Coeff = 0  # bit 0 to 4
    I_Fll_Int_Coeff = 0  # bit 4 to 8
    I_Int_Coeff = 0  # bit 8 to 13
    I_Fll_En_H = 0  # bit 13 to 14
    I_Tdc_Fine_Res = 0  # bit 14 to 15
    I_Dcofine_Resolution = 0  # bit 15 to 16
    I_Gainctrl = 0  # bit 16 to 19
    I_Afc_Divratio = 0  # bit 19 to 20
    I_Afccntsel = 0  # bit 20 to 21
    I_Afc_Startup = 0  # bit 21 to 23
    Reserved23 = 0  # bit 23 to 24
    I_Tdctargetcnt = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_PLL_LF_L),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_PLL_LF_L, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_PLL_FRAC_LOCK_L:
    DKL_PLL1_FRAC_LOCK_L = 0x20C


class _DKL_PLL_FRAC_LOCK_L(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Feedfwrdgain', ctypes.c_uint32, 8),
        ('I_Feedfwrdcal_En', ctypes.c_uint32, 1),
        ('I_Feedfwrdcal_Pause_Hi', ctypes.c_uint32, 1),
        ('I_Dcoditheren_H', ctypes.c_uint32, 1),
        ('I_Lockthresh', ctypes.c_uint32, 4),
        ('I_Dcodither_Config', ctypes.c_uint32, 1),
        ('I_Earlylock_Criterion', ctypes.c_uint32, 2),
        ('I_Truelock_Criterion', ctypes.c_uint32, 2),
        ('I_Lf_Half_Cyc_En', ctypes.c_uint32, 1),
        ('I_Dither_Ovrd', ctypes.c_uint32, 1),
        ('I_Pllc_Restore_Reg', ctypes.c_uint32, 1),
        ('I_Pllc_Restore_Mode_Ctrl', ctypes.c_uint32, 1),
        ('I_Pllrampen_H', ctypes.c_uint32, 1),
        ('I_Fbdiv_Strobe_H', ctypes.c_uint32, 1),
        ('I_Ovc_Snapshot_H', ctypes.c_uint32, 1),
        ('I_Dither_Value', ctypes.c_uint32, 5),
    ]


class REG_DKL_PLL_FRAC_LOCK_L(ctypes.Union):
    value = 0
    offset = 0

    I_Feedfwrdgain = 0  # bit 0 to 8
    I_Feedfwrdcal_En = 0  # bit 8 to 9
    I_Feedfwrdcal_Pause_Hi = 0  # bit 9 to 10
    I_Dcoditheren_H = 0  # bit 10 to 11
    I_Lockthresh = 0  # bit 11 to 15
    I_Dcodither_Config = 0  # bit 15 to 16
    I_Earlylock_Criterion = 0  # bit 16 to 18
    I_Truelock_Criterion = 0  # bit 18 to 20
    I_Lf_Half_Cyc_En = 0  # bit 20 to 21
    I_Dither_Ovrd = 0  # bit 21 to 22
    I_Pllc_Restore_Reg = 0  # bit 22 to 23
    I_Pllc_Restore_Mode_Ctrl = 0  # bit 23 to 24
    I_Pllrampen_H = 0  # bit 24 to 25
    I_Fbdiv_Strobe_H = 0  # bit 25 to 26
    I_Ovc_Snapshot_H = 0  # bit 26 to 27
    I_Dither_Value = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_PLL_FRAC_LOCK_L),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_PLL_FRAC_LOCK_L, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_REFCLKIN_CTL:
    DKL_REFCLKIN_CTL = 0x12C


class _DKL_REFCLKIN_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Od_Refclkin1_Refclkmux', ctypes.c_uint32, 3),
        ('Od_Refclkin1_Refclkinjmux', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 4),
        ('Od_Refclkin2_Refclkmux', ctypes.c_uint32, 3),
        ('Od_Refclkin2_Refclkinjmux', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 20),
    ]


class REG_DKL_REFCLKIN_CTL(ctypes.Union):
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
        ('bitMap', _DKL_REFCLKIN_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_REFCLKIN_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_OD_CLKTOP2_HSDIV_EN_H(Enum):
    OD_CLKTOP2_HSDIV_EN_H_DISABLE = 0x0
    OD_CLKTOP2_HSDIV_EN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP2_DSDIV_EN_H(Enum):
    OD_CLKTOP2_DSDIV_EN_H_DISABLE = 0x0
    OD_CLKTOP2_DSDIV_EN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD(Enum):
    OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD_DISABLE = 0x0
    OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD(Enum):
    OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD_DISABLE = 0x0
    OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD(Enum):
    OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD_DISABLE = 0x0
    OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD(Enum):
    OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD_DISABLE = 0x0
    OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP2_TLINEDRV_OVERRIDEEN(Enum):
    OD_CLKTOP2_TLINEDRV_OVERRIDEEN_DISABLE = 0x0
    OD_CLKTOP2_TLINEDRV_OVERRIDEEN_ENABLE = 0x1


class ENUM_OD_CLKTOP2_DSDIV_DIVRATIO(Enum):
    OD_CLKTOP2_DSDIV_DIVRATIO_NO_DIVISION = 0x0
    OD_CLKTOP2_DSDIV_DIVRATIO_NO_DIV = 0x1
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_2 = 0x2
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_3 = 0x3
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_4 = 0x4
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_5 = 0x5
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_6 = 0x6
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_7 = 0x7
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_8 = 0x8
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_9 = 0x9
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_10 = 0xA


class ENUM_OD_CLKTOP2_HSDIV_DIVRATIO(Enum):
    OD_CLKTOP2_HSDIV_DIVRATIO_DIVIDE_BY_2 = 0x0
    OD_CLKTOP2_HSDIV_DIVRATIO_DIVIDE_BY_3 = 0x1
    OD_CLKTOP2_HSDIV_DIVRATIO_DIVIDE_BY_5 = 0x2
    OD_CLKTOP2_HSDIV_DIVRATIO_DIVIDE_BY_7 = 0x3


class ENUM_OD_CLKTOP2_TLINEDRV_CLKSEL(Enum):
    OD_CLKTOP2_TLINEDRV_CLKSEL_HSCLKDIV_OUTPUT = 0x0
    OD_CLKTOP2_TLINEDRV_CLKSEL_ICLK_BYPASS_INPUT_FROM_OTHER_CLKTOP = 0x1
    OD_CLKTOP2_TLINEDRV_CLKSEL_DSDIV_OUTPUT_CLOCK = 0x2
    OD_CLKTOP2_TLINEDRV_CLKSEL_NONDIVIDED_PLL_CLOCK = 0x3


class ENUM_OD_CLKTOP2_CORECLK_INPUTSEL(Enum):
    OD_CLKTOP2_CORECLK_INPUTSEL_HSDIV_OUTPUT = 0x0
    OD_CLKTOP2_CORECLK_INPUTSEL_DSDIV_OUTPUT = 0x1


class ENUM_OD_CLKTOP2_OUTCLK_BYPASSEN_H(Enum):
    OD_CLKTOP2_OUTCLK_BYPASSEN_H_DISABLE = 0x0
    OD_CLKTOP2_OUTCLK_BYPASSEN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP2_CLK2OBS_EN_H(Enum):
    OD_CLKTOP2_CLK2OBS_EN_H_DISABLE = 0x0
    OD_CLKTOP2_CLK2OBS_EN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP2_CLKOBS_INPUTSEL(Enum):
    OD_CLKTOP2_CLKOBS_INPUTSEL_HSDIV_OUTPUT_CLOCK = 0x0
    OD_CLKTOP2_CLKOBS_INPUTSEL_ICLK_BYPASS_INPUT_FROM_OTHER_CLKTOP = 0x1
    OD_CLKTOP2_CLKOBS_INPUTSEL_DSDIV_OUTPUT_CLOCK = 0x2
    OD_CLKTOP2_CLKOBS_INPUTSEL_NONDIVIDED_PLL_CLOCK = 0x3


class OFFSET_DKL_CLKTOP2_HSCLKCTL:
    DKL_CLKTOP2_HSCLKCTL = 0x0D4


class _DKL_CLKTOP2_HSCLKCTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Od_Clktop2_Hsdiv_En_H', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 1),
        ('Od_Clktop2_Dsdiv_En_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Tlinedrv_Enright_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop2_Tlinedrv_Enleft_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop2_Tlinedrv_Enright_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop2_Tlinedrv_Enleft_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop2_Tlinedrv_Overrideen', ctypes.c_uint32, 1),
        ('Od_Clktop2_Dsdiv_Divratio', ctypes.c_uint32, 4),
        ('Od_Clktop2_Hsdiv_Divratio', ctypes.c_uint32, 2),
        ('Od_Clktop2_Tlinedrv_Clksel', ctypes.c_uint32, 2),
        ('Od_Clktop2_Coreclk_Inputsel', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 1),
        ('Od_Clktop2_Outclk_Bypassen_H', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 1),
        ('Od_Clktop2_Clktop_Vhfclk_Testen_H', ctypes.c_uint32, 2),
        ('Reserved22', ctypes.c_uint32, 2),
        ('Od_Clktop2_Clk2Obs_En_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Clkobs_Inputsel', ctypes.c_uint32, 2),
        ('Reserved27', ctypes.c_uint32, 5),
    ]


class REG_DKL_CLKTOP2_HSCLKCTL(ctypes.Union):
    value = 0
    offset = 0

    Od_Clktop2_Hsdiv_En_H = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 2
    Od_Clktop2_Dsdiv_En_H = 0  # bit 2 to 3
    Od_Clktop2_Tlinedrv_Enright_H_Ovrd = 0  # bit 3 to 4
    Od_Clktop2_Tlinedrv_Enleft_H_Ovrd = 0  # bit 4 to 5
    Od_Clktop2_Tlinedrv_Enright_Ded_H_Ovrd = 0  # bit 5 to 6
    Od_Clktop2_Tlinedrv_Enleft_Ded_H_Ovrd = 0  # bit 6 to 7
    Od_Clktop2_Tlinedrv_Overrideen = 0  # bit 7 to 8
    Od_Clktop2_Dsdiv_Divratio = 0  # bit 8 to 12
    Od_Clktop2_Hsdiv_Divratio = 0  # bit 12 to 14
    Od_Clktop2_Tlinedrv_Clksel = 0  # bit 14 to 16
    Od_Clktop2_Coreclk_Inputsel = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 18
    Od_Clktop2_Outclk_Bypassen_H = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 20
    Od_Clktop2_Clktop_Vhfclk_Testen_H = 0  # bit 20 to 22
    Reserved22 = 0  # bit 22 to 24
    Od_Clktop2_Clk2Obs_En_H = 0  # bit 24 to 25
    Od_Clktop2_Clkobs_Inputsel = 0  # bit 25 to 27
    Reserved27 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_CLKTOP2_HSCLKCTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_CLKTOP2_HSCLKCTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_CLKTOP2_CORECLKCTL1:
    DKL_CLKTOP2_CORECLKCTL1 = 0x0D8


class _DKL_CLKTOP2_CORECLKCTL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclka_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclka_Bypass', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkb_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkb_Bypass', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 2),
        ('Od_Clktop2_Coreclka_Divratio', ctypes.c_uint32, 8),
        ('Od_Clktop2_Coreclkb_Divratio', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkc_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkc_Bypass', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkd_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkd_Bypass', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_DKL_CLKTOP2_CORECLKCTL1(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    Od_Clktop2_Coreclka_Divretimeren_H = 0  # bit 1 to 2
    Od_Clktop2_Coreclka_Bypass = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 4
    Od_Clktop2_Coreclkb_Divretimeren_H = 0  # bit 4 to 5
    Od_Clktop2_Coreclkb_Bypass = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 8
    Od_Clktop2_Coreclka_Divratio = 0  # bit 8 to 16
    Od_Clktop2_Coreclkb_Divratio = 0  # bit 16 to 24
    Reserved24 = 0  # bit 24 to 25
    Od_Clktop2_Coreclkc_Divretimeren_H = 0  # bit 25 to 26
    Od_Clktop2_Coreclkc_Bypass = 0  # bit 26 to 27
    Reserved27 = 0  # bit 27 to 28
    Od_Clktop2_Coreclkd_Divretimeren_H = 0  # bit 28 to 29
    Od_Clktop2_Coreclkd_Bypass = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_CLKTOP2_CORECLKCTL1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_CLKTOP2_CORECLKCTL1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_CMN_ANA_DW28:
    DKL_CMN_ANA_DW28 = 0x130


class _DKL_CMN_ANA_DW28(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Clktop1_Plldivby2_2Dmon_En_H', ctypes.c_uint32, 1),
        ('Clktop1_Divby2Clk_Bypass_En', ctypes.c_uint32, 1),
        ('Clktop1_Vga_Clk_Sel', ctypes.c_uint32, 1),
        ('Clktop1_Vga_Clk2Dl_En', ctypes.c_uint32, 1),
        ('Clktop2_Plldivby2_2Dmon_En_H', ctypes.c_uint32, 1),
        ('Clktop2_Divby2Clk_Bypass_En', ctypes.c_uint32, 1),
        ('Clktop2_Vga_Clk_Sel', ctypes.c_uint32, 1),
        ('Clktop2_Vga_Clk2Dl_En', ctypes.c_uint32, 1),
        ('Refclkin1_Refclk_Dlane_Sel', ctypes.c_uint32, 2),
        ('Refclkin1_Refclk_Sel', ctypes.c_uint32, 1),
        ('Refclkin1_Refclk_Dlane_En', ctypes.c_uint32, 1),
        ('Refclkin2_Refclk_Dlane_Sel', ctypes.c_uint32, 2),
        ('Refclkin2_Refclk_Sel', ctypes.c_uint32, 1),
        ('Refclkin2_Refclk_Dlane_En', ctypes.c_uint32, 1),
        ('Clktop1_Id_Vga_Chpmp_Ck_Divratio', ctypes.c_uint32, 4),
        ('Clktop1_Id_Vga_Chpmp_Div_En_H', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 3),
        ('Clktop2_Id_Vga_Chpmp_Ck_Divratio', ctypes.c_uint32, 4),
        ('Clktop2_Id_Vga_Chpmp_Div_En_H', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_DKL_CMN_ANA_DW28(ctypes.Union):
    value = 0
    offset = 0

    Clktop1_Plldivby2_2Dmon_En_H = 0  # bit 0 to 1
    Clktop1_Divby2Clk_Bypass_En = 0  # bit 1 to 2
    Clktop1_Vga_Clk_Sel = 0  # bit 2 to 3
    Clktop1_Vga_Clk2Dl_En = 0  # bit 3 to 4
    Clktop2_Plldivby2_2Dmon_En_H = 0  # bit 4 to 5
    Clktop2_Divby2Clk_Bypass_En = 0  # bit 5 to 6
    Clktop2_Vga_Clk_Sel = 0  # bit 6 to 7
    Clktop2_Vga_Clk2Dl_En = 0  # bit 7 to 8
    Refclkin1_Refclk_Dlane_Sel = 0  # bit 8 to 10
    Refclkin1_Refclk_Sel = 0  # bit 10 to 11
    Refclkin1_Refclk_Dlane_En = 0  # bit 11 to 12
    Refclkin2_Refclk_Dlane_Sel = 0  # bit 12 to 14
    Refclkin2_Refclk_Sel = 0  # bit 14 to 15
    Refclkin2_Refclk_Dlane_En = 0  # bit 15 to 16
    Clktop1_Id_Vga_Chpmp_Ck_Divratio = 0  # bit 16 to 20
    Clktop1_Id_Vga_Chpmp_Div_En_H = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 24
    Clktop2_Id_Vga_Chpmp_Ck_Divratio = 0  # bit 24 to 28
    Clktop2_Id_Vga_Chpmp_Div_En_H = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_CMN_ANA_DW28),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_CMN_ANA_DW28, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_DFX_DPSO_L:
    DKL_DFX_DPSO_L = 0x22C


class _DKL_DFX_DPSO_L(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Init_Cselafc', ctypes.c_uint32, 8),
        ('I_Max_Cselafc', ctypes.c_uint32, 8),
        ('I_Fllafc_Lockcnt', ctypes.c_uint32, 3),
        ('I_Fllafc_Gain', ctypes.c_uint32, 4),
        ('I_Fastlock_En_H', ctypes.c_uint32, 1),
        ('I_Bb_Gain1', ctypes.c_uint32, 3),
        ('I_Bb_Gain2', ctypes.c_uint32, 3),
        ('I_Cml2Cmosbonus', ctypes.c_uint32, 2),
    ]


class REG_DKL_DFX_DPSO_L(ctypes.Union):
    value = 0
    offset = 0

    I_Init_Cselafc = 0  # bit 0 to 8
    I_Max_Cselafc = 0  # bit 8 to 16
    I_Fllafc_Lockcnt = 0  # bit 16 to 19
    I_Fllafc_Gain = 0  # bit 19 to 23
    I_Fastlock_En_H = 0  # bit 23 to 24
    I_Bb_Gain1 = 0  # bit 24 to 27
    I_Bb_Gain2 = 0  # bit 27 to 30
    I_Cml2Cmosbonus = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_DFX_DPSO_L),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_DFX_DPSO_L, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_SSC_L:
    DKL_SSC_L = 0x210


class _DKL_SSC_L(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Sscstepsize_7_0', ctypes.c_uint32, 8),
        ('I_Sscstepsize_9_8', ctypes.c_uint32, 2),
        ('I_Sscstepnum', ctypes.c_uint32, 3),
        ('Reserved13', ctypes.c_uint32, 3),
        ('I_Sscsteplength_7_0', ctypes.c_uint32, 8),
        ('I_Sscsteplength_9_8', ctypes.c_uint32, 2),
        ('I_Ssctype', ctypes.c_uint32, 2),
        ('I_Sscen_H', ctypes.c_uint32, 1),
        ('I_Rampafc_Sscen_H', ctypes.c_uint32, 1),
        ('I_Ssc_Strobe_H', ctypes.c_uint32, 1),
        ('I_Ssc_Openloop_En_H', ctypes.c_uint32, 1),
    ]


class REG_DKL_SSC_L(ctypes.Union):
    value = 0
    offset = 0

    I_Sscstepsize_7_0 = 0  # bit 0 to 8
    I_Sscstepsize_9_8 = 0  # bit 8 to 10
    I_Sscstepnum = 0  # bit 10 to 13
    Reserved13 = 0  # bit 13 to 16
    I_Sscsteplength_7_0 = 0  # bit 16 to 24
    I_Sscsteplength_9_8 = 0  # bit 24 to 26
    I_Ssctype = 0  # bit 26 to 28
    I_Sscen_H = 0  # bit 28 to 29
    I_Rampafc_Sscen_H = 0  # bit 29 to 30
    I_Ssc_Strobe_H = 0  # bit 30 to 31
    I_Ssc_Openloop_En_H = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_SSC_L),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_SSC_L, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_ANA_BONUS:
    DKL_ANA_BONUS = 0x24C


class _DKL_ANA_BONUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Pllc_Ana_Bonus_7_0', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 24),
    ]


class REG_DKL_ANA_BONUS(ctypes.Union):
    value = 0
    offset = 0

    I_Pllc_Ana_Bonus_7_0 = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_ANA_BONUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_ANA_BONUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_CNTR_BIST:
    DKL_CNTR_BIST = 0x244


class _DKL_CNTR_BIST(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Irefgen_Settlingtime_Cntr_7_0', ctypes.c_uint32, 8),
        ('I_Bonus_Irefgen_Settling_Time_Ro_Standby_1_0', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 5),
        ('I_Plllock_Sel_1_0', ctypes.c_uint32, 2),
        ('I_Plllock_Cnt_6_0', ctypes.c_uint32, 7),
        ('I_Plllock_Cnt_10_7', ctypes.c_uint32, 4),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_DKL_CNTR_BIST(ctypes.Union):
    value = 0
    offset = 0

    I_Irefgen_Settlingtime_Cntr_7_0 = 0  # bit 0 to 8
    I_Bonus_Irefgen_Settling_Time_Ro_Standby_1_0 = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 15
    I_Plllock_Sel_1_0 = 0  # bit 15 to 17
    I_Plllock_Cnt_6_0 = 0  # bit 17 to 24
    I_Plllock_Cnt_10_7 = 0  # bit 24 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_CNTR_BIST),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_CNTR_BIST, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_BIAS_L:
    DKL_BIAS_L = 0x214


class _DKL_BIAS_L(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Ireftrim_4_0', ctypes.c_uint32, 5),
        ('I_Vref_Rdac_2_0', ctypes.c_uint32, 3),
        ('I_Bonus_Ctrim_4_0', ctypes.c_uint32, 5),
        ('I_Bonus_Iref_Refclk_Mode_1_0', ctypes.c_uint32, 2),
        ('I_Biascal_En_H', ctypes.c_uint32, 1),
        ('I_Bias_Bonus_7_0', ctypes.c_uint32, 8),
        ('I_Init_Dcomp_5_0', ctypes.c_uint32, 6),
        ('I_Bias_Gb_Sel_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKL_BIAS_L(ctypes.Union):
    value = 0
    offset = 0

    I_Ireftrim_4_0 = 0  # bit 0 to 5
    I_Vref_Rdac_2_0 = 0  # bit 5 to 8
    I_Bonus_Ctrim_4_0 = 0  # bit 8 to 13
    I_Bonus_Iref_Refclk_Mode_1_0 = 0  # bit 13 to 15
    I_Biascal_En_H = 0  # bit 15 to 16
    I_Bias_Bonus_7_0 = 0  # bit 16 to 24
    I_Init_Dcomp_5_0 = 0  # bit 24 to 30
    I_Bias_Gb_Sel_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_BIAS_L),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_BIAS_L, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_TDC_COLDST_BIAS:
    DKL_TDC_COLDST_BIAS = 0x218


class _DKL_TDC_COLDST_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Feedfwdgain_7_0', ctypes.c_uint32, 8),
        ('I_Sscstepsize_7_0', ctypes.c_uint32, 8),
        ('I_Dcocoarse_7_0', ctypes.c_uint32, 8),
        ('I_Tribufctrlext_4_0', ctypes.c_uint32, 5),
        ('I_Cloadctrlext_4_2', ctypes.c_uint32, 3),
    ]


class REG_DKL_TDC_COLDST_BIAS(ctypes.Union):
    value = 0
    offset = 0

    I_Feedfwdgain_7_0 = 0  # bit 0 to 8
    I_Sscstepsize_7_0 = 0  # bit 8 to 16
    I_Dcocoarse_7_0 = 0  # bit 16 to 24
    I_Tribufctrlext_4_0 = 0  # bit 24 to 29
    I_Cloadctrlext_4_2 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_TDC_COLDST_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_TDC_COLDST_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

