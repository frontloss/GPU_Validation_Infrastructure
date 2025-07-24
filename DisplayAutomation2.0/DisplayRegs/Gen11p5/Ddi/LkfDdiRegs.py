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
# @file LkfDdiRegs.py
# @brief contains LkfDdiRegs.py related register definitions

import ctypes
from enum import Enum


class OFFSET_HIP_INDEX_REG0:
    HIP_INDEX_REG0 = 0x1010A0


class _HIP_INDEX_REG0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hip_168_Index', ctypes.c_uint32, 8),
        ('Hip_169_Index', ctypes.c_uint32, 8),
        ('Hip_16A_Index', ctypes.c_uint32, 8),
        ('Hip_16B_Index', ctypes.c_uint32, 8),
    ]


class REG_HIP_INDEX_REG0(ctypes.Union):
    value = 0
    offset = 0

    Hip_168_Index = 0  # bit 0 to 8
    Hip_169_Index = 0  # bit 8 to 16
    Hip_16A_Index = 0  # bit 16 to 24
    Hip_16B_Index = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HIP_INDEX_REG0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HIP_INDEX_REG0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_TX_DPCNTL0_L:
    DKL_TX_DPCTRL0_L_TX1LN0 = 0x2C0


class _DKL_TX_DPCNTL0_L(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VswingControl_Tx1', ctypes.c_uint32, 3),
        ('Cursor_Control_Tx1', ctypes.c_uint32, 5),
        ('De_Emphasis_Control_L0_Tx1', ctypes.c_uint32, 5),
        ('PreshootControlL0', ctypes.c_uint32, 5),
        ('Shunt_Cp_Tx1', ctypes.c_uint32, 5),
        ('Shunt_Cm_Tx1', ctypes.c_uint32, 5),
        ('Slow_Trim_Enable_Tx1', ctypes.c_uint32, 1),
        ('Pipe_Select_Tx1', ctypes.c_uint32, 1),
        ('Trainingen_Tx1', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_DKL_TX_DPCNTL0_L(ctypes.Union):
    value = 0
    offset = 0

    VswingControl_Tx1 = 0  # bit 0 to 3
    Cursor_Control_Tx1 = 0  # bit 3 to 8
    De_Emphasis_Control_L0_Tx1 = 0  # bit 8 to 13
    PreshootControlL0 = 0  # bit 13 to 18
    Shunt_Cp_Tx1 = 0  # bit 18 to 23
    Shunt_Cm_Tx1 = 0  # bit 23 to 28
    Slow_Trim_Enable_Tx1 = 0  # bit 28 to 29
    Pipe_Select_Tx1 = 0  # bit 29 to 30
    Trainingen_Tx1 = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_TX_DPCNTL0_L),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_TX_DPCNTL0_L, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_TX_DPCNTL1_L:
    DKL_TX_DPCNTL1_L_TX2LN0 = 0x2C4


class _DKL_TX_DPCNTL1_L(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VswingControl_Tx2', ctypes.c_uint32, 3),
        ('Cursor_Control_Tx2', ctypes.c_uint32, 5),
        ('De_Emphasis_Control_L0_Tx2', ctypes.c_uint32, 5),
        ('PreshootControlL0', ctypes.c_uint32, 5),
        ('Shunt_Cp_Tx2', ctypes.c_uint32, 5),
        ('Shunt_Cm_Tx2', ctypes.c_uint32, 5),
        ('Slow_Trim_Enable_Tx2', ctypes.c_uint32, 1),
        ('Pipe_Select_Tx2', ctypes.c_uint32, 1),
        ('Trainingen_Tx2', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_DKL_TX_DPCNTL1_L(ctypes.Union):
    value = 0
    offset = 0

    VswingControl_Tx2 = 0  # bit 0 to 3
    Cursor_Control_Tx2 = 0  # bit 3 to 8
    De_Emphasis_Control_L0_Tx2 = 0  # bit 8 to 13
    PreshootControlL0 = 0  # bit 13 to 18
    Shunt_Cp_Tx2 = 0  # bit 18 to 23
    Shunt_Cm_Tx2 = 0  # bit 23 to 28
    Slow_Trim_Enable_Tx2 = 0  # bit 28 to 29
    Pipe_Select_Tx2 = 0  # bit 29 to 30
    Trainingen_Tx2 = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_TX_DPCNTL1_L),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_TX_DPCNTL1_L, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_TX_DPCNTL2:
    DKL_TX_DPCNTL2_TX2LN0 = 0x2C8


class _DKL_TX_DPCNTL2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Rate8Boverride', ctypes.c_uint32, 1),
        ('Rate8Boverrideen', ctypes.c_uint32, 1),
        ('Dp20Bitmode', ctypes.c_uint32, 1),
        ('Loadgenselect_Tx1', ctypes.c_uint32, 2),
        ('Loadgenselect_Tx2', ctypes.c_uint32, 2),
        ('Reserved7', ctypes.c_uint32, 25),
    ]


class REG_DKL_TX_DPCNTL2(ctypes.Union):
    value = 0
    offset = 0

    Rate8Boverride = 0  # bit 0 to 1
    Rate8Boverrideen = 0  # bit 1 to 2
    Dp20Bitmode = 0  # bit 2 to 3
    Loadgenselect_Tx1 = 0  # bit 3 to 5
    Loadgenselect_Tx2 = 0  # bit 5 to 7
    Reserved7 = 0  # bit 7 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_TX_DPCNTL2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_TX_DPCNTL2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_DP_MODE:
    DKL_DP_MODE_LN0_ACU = 0x0A0


class _DKL_DP_MODE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Suspwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Gaonpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Digpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Clnpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Trpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Tr2Pwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Dp_X1_Mode', ctypes.c_uint32, 1),
        ('Cfg_Dp_X2_Mode', ctypes.c_uint32, 1),
        ('Cfg_Rawpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Digpwr_Req_Override', ctypes.c_uint32, 1),
        ('Cfg_Rawpwr_Req_Override', ctypes.c_uint32, 1),
        ('Cfg_Susclk_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Laneclkreq_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Laneclkreq_Force', ctypes.c_uint32, 1),
        ('Cfg_Cri_Digpwr_Req', ctypes.c_uint32, 1),
        ('Cfg_Corepwr_Ack_With_Pcs_Pwrreq', ctypes.c_uint32, 1),
        ('Cfg_Ldo_Powerup_Timer_8', ctypes.c_uint32, 1),
        ('Cfg_Vr_Pulldwn2Gnd_Tr', ctypes.c_uint32, 1),
        ('Cfg_Vr_Pulldwn2Gnd_Tr2', ctypes.c_uint32, 1),
        ('Cfg_Crireg_Cold_Boot_Done', ctypes.c_uint32, 1),
        ('Cfg_Dig_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Cl_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Tr_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Tr2_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Ldo_Powerup_Timer', ctypes.c_uint32, 8),
    ]


class REG_DKL_DP_MODE(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Suspwr_Gating_Ctrl = 0  # bit 0 to 1
    Cfg_Gaonpwr_Gating_Ctrl = 0  # bit 1 to 2
    Cfg_Digpwr_Gating_Ctrl = 0  # bit 2 to 3
    Cfg_Clnpwr_Gating_Ctrl = 0  # bit 3 to 4
    Cfg_Trpwr_Gating_Ctrl = 0  # bit 4 to 5
    Cfg_Tr2Pwr_Gating_Ctrl = 0  # bit 5 to 6
    Cfg_Dp_X1_Mode = 0  # bit 6 to 7
    Cfg_Dp_X2_Mode = 0  # bit 7 to 8
    Cfg_Rawpwr_Gating_Ctrl = 0  # bit 8 to 9
    Cfg_Digpwr_Req_Override = 0  # bit 9 to 10
    Cfg_Rawpwr_Req_Override = 0  # bit 10 to 11
    Cfg_Susclk_Gating_Ctrl = 0  # bit 11 to 12
    Cfg_Laneclkreq_Gating_Ctrl = 0  # bit 12 to 13
    Cfg_Laneclkreq_Force = 0  # bit 13 to 14
    Cfg_Cri_Digpwr_Req = 0  # bit 14 to 15
    Cfg_Corepwr_Ack_With_Pcs_Pwrreq = 0  # bit 15 to 16
    Cfg_Ldo_Powerup_Timer_8 = 0  # bit 16 to 17
    Cfg_Vr_Pulldwn2Gnd_Tr = 0  # bit 17 to 18
    Cfg_Vr_Pulldwn2Gnd_Tr2 = 0  # bit 18 to 19
    Cfg_Crireg_Cold_Boot_Done = 0  # bit 19 to 20
    Cfg_Dig_Pwrgate_Timer_Bypass = 0  # bit 20 to 21
    Cfg_Cl_Pwrgate_Timer_Bypass = 0  # bit 21 to 22
    Cfg_Tr_Pwrgate_Timer_Bypass = 0  # bit 22 to 23
    Cfg_Tr2_Pwrgate_Timer_Bypass = 0  # bit 23 to 24
    Ldo_Powerup_Timer = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_DP_MODE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_DP_MODE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_MASK_LP_IDLE_IN_FILL_DONE(Enum):
    MASK_LP_IDLE_IN_FILL_DONE_MASK_IS_DISABLED = 0x0  # Both hp idle and lp idle will be considered in Fill done
    MASK_LP_IDLE_IN_FILL_DONE_MASK_IS_ENABLED = 0x1  # Only hp idle will be considered in Fill done.


class ENUM_COUNTER_COMPARE(Enum):
    COUNTER_COMPARE_COUNTER_11US = 0xB  # Value to compare 1Mhz counter which counts from Memup internal signal going l
                                        # ow to all inflight transactions completion.


class ENUM_OPEN_MIPI_DPHY_LATCHES(Enum):
    OPEN_MIPI_DPHY_LATCHES_DO_NOT_OVERRIDE_THE_DPHY_LATCHES = 0x0
    OPEN_MIPI_DPHY_LATCHES_OVERRIDE_THE_DPHY_LATCHES = 0x1


class OFFSET_CHICKEN_DCPR_2:
    CHICKEN_DCPR_2 = 0x46434


class _CHICKEN_DCPR_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MaskLpIdleInFillDone', ctypes.c_uint32, 1),
        ('CounterCompare', ctypes.c_uint32, 5),
        ('StickyForPhase1Counter', ctypes.c_uint32, 1),
        ('DisablePhase1Counter', ctypes.c_uint32, 1),
        ('StickyForPhase2Counter', ctypes.c_uint32, 1),
        ('DisablePhase2Counter', ctypes.c_uint32, 1),
        ('MasksNo_Lp_PendingInMemup', ctypes.c_uint32, 1),
        ('MaskNo_Lp_PendingInFill', ctypes.c_uint32, 1),
        ('IpcDemoteOverride', ctypes.c_uint32, 1),
        ('OpenMipiDphyLatches', ctypes.c_uint32, 1),
        ('SpareChicken151', ctypes.c_uint32, 10),
        ('DelayIsolationCounter', ctypes.c_uint32, 8),
    ]


class REG_CHICKEN_DCPR_2(ctypes.Union):
    value = 0
    offset = 0

    MaskLpIdleInFillDone = 0  # bit 0 to 1
    CounterCompare = 0  # bit 1 to 6
    StickyForPhase1Counter = 0  # bit 6 to 7
    DisablePhase1Counter = 0  # bit 7 to 8
    StickyForPhase2Counter = 0  # bit 8 to 9
    DisablePhase2Counter = 0  # bit 9 to 10
    MasksNo_Lp_PendingInMemup = 0  # bit 10 to 11
    MaskNo_Lp_PendingInFill = 0  # bit 11 to 12
    IpcDemoteOverride = 0  # bit 12 to 13
    OpenMipiDphyLatches = 0  # bit 13 to 14
    SpareChicken151 = 0  # bit 14 to 24
    DelayIsolationCounter = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_DCPR_2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_DCPR_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

