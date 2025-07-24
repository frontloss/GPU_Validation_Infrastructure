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
# @file Gen13DdiRegs.py
# @brief contains Gen13DdiRegs.py related register definitions

import ctypes
from enum import Enum


class OFFSET_TCSS_DDI_STATUS:
    TCSS_DDI_STATUS_1 = 0x161500
    TCSS_DDI_STATUS_2 = 0x161504
    TCSS_DDI_STATUS_3 = 0x161508
    TCSS_DDI_STATUS_4 = 0x16150C


class _TCSS_DDI_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hpd_Live_Status_Alt', ctypes.c_uint32, 1),
        ('Hpd_Live_Status_Tbt', ctypes.c_uint32, 1),
        ('Ready', ctypes.c_uint32, 1),
        ('Sss', ctypes.c_uint32, 1),
        ('Src_Port_Num', ctypes.c_uint32, 4),
        ('Hpd_In_Progress', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 23),
    ]


class REG_TCSS_DDI_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Hpd_Live_Status_Alt = 0  # bit 0 to 1
    Hpd_Live_Status_Tbt = 0  # bit 1 to 2
    Ready = 0  # bit 2 to 3
    Sss = 0  # bit 3 to 4
    Src_Port_Num = 0  # bit 4 to 8
    Hpd_In_Progress = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TCSS_DDI_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TCSS_DDI_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DP_PORT_WIDTH_SELECTION(Enum):
    DP_PORT_WIDTH_SELECTION_X1 = 0x0  # x1 Mode
    DP_PORT_WIDTH_SELECTION_X2 = 0x1  # x2 Mode
    DP_PORT_WIDTH_SELECTION_X4 = 0x3  # x4 Mode


class ENUM_TYPEC_PHY_OWNERSHIP(Enum):
    TYPEC_PHY_OWNERSHIP_RELEASE_OWNERSHIP = 0x0
    TYPEC_PHY_OWNERSHIP_TAKE_OWNERSHIP = 0x1


class ENUM_DDI_IDLE_STATUS(Enum):
    DDI_IDLE_STATUS_BUFFER_NOT_IDLE = 0x0
    DDI_IDLE_STATUS_BUFFER_IDLE = 0x1


class ENUM_PORT_REVERSAL(Enum):
    PORT_REVERSAL_NOT_REVERSED = 0x0
    PORT_REVERSAL_REVERSED = 0x1


class ENUM_PHY_LANE_WIDTH(Enum):
    PHY_LANE_WIDTH_10BIT = 0x0  # This value is used for DP 1.4x and HDMI 2.0 link rates.
    PHY_LANE_WIDTH_20BIT = 0x1
    PHY_LANE_WIDTH_40BIT = 0x2  # This value is used for DP 2.0 (128b/132b) link rates.


class ENUM_PHY_LINK_RATE(Enum):
    PHY_LINK_RATE_1_62 = 0x0  # If the port is HDMI, this value indicates link rate between 0Gbps and 9Gbps
    PHY_LINK_RATE_2_70 = 0x1
    PHY_LINK_RATE_5_40 = 0x2
    PHY_LINK_RATE_8_10 = 0x3
    PHY_LINK_RATE_2_16 = 0x4
    PHY_LINK_RATE_2_43 = 0x5
    PHY_LINK_RATE_3_24 = 0x6
    PHY_LINK_RATE_4_32 = 0x7
    PHY_LINK_RATE_10_0 = 0x8  # If the port is HDMI, this value indicates 10Gbps link rate.
    PHY_LINK_RATE_13_5 = 0x9  # If the port is HDMI, this value indicates 12Gbps link rate.
    PHY_LINK_RATE_20_0 = 0xA


class ENUM_PHY_PARAM_ADJUST(Enum):
    PHY_PARAM_ADJUST_ENABLE = 0x1
    PHY_PARAM_ADJUST_DISABLE = 0x0


class ENUM_OVERRIDE_TRAINING_ENABLE(Enum):
    OVERRIDE_TRAINING_ENABLE_OVERRIDE = 0x1
    OVERRIDE_TRAINING_DISABLE_OVERRIDE = 0x0


class ENUM_DDI_BUFFER_ENABLE(Enum):
    DDI_BUFFER_DISABLE = 0x0
    DDI_BUFFER_ENABLE = 0x1


class OFFSET_DDI_BUF_CTL:
    DDI_BUF_CTL_A = 0x64000
    DDI_BUF_CTL_B = 0x64100
    DDI_BUF_CTL_C = 0x64200
    DDI_BUF_CTL_USBC1 = 0x64300
    DDI_BUF_CTL_USBC2 = 0x64400
    DDI_BUF_CTL_USBC3 = 0x64500
    DDI_BUF_CTL_USBC4 = 0x64600
    DDI_BUF_CTL_D = 0x64700
    DDI_BUF_CTL_E = 0x64800


class _DDI_BUF_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('DpPortWidthSelection', ctypes.c_uint32, 3),
        ('Reserved4', ctypes.c_uint32, 2),
        ('TypecPhyOwnership', ctypes.c_uint32, 1),
        ('DdiIdleStatus', ctypes.c_uint32, 1),
        ('UsbTypeCDpLaneStaggeringDelay', ctypes.c_uint32, 8),
        ('PortReversal', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 1),
        ('PhyLaneWidth', ctypes.c_uint32, 2),
        ('PhyLinkRate', ctypes.c_uint32, 4),
        ('Reserved24', ctypes.c_uint32, 4),
        ('PhyParamAdjust', ctypes.c_uint32, 1),
        ('OverrideTrainingEnable', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 1),
        ('DdiBufferEnable', ctypes.c_uint32, 1),
    ]


class REG_DDI_BUF_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    DpPortWidthSelection = 0  # bit 1 to 4
    Reserved4 = 0  # bit 4 to 6
    TypecPhyOwnership = 0  # bit 6 to 7
    DdiIdleStatus = 0  # bit 7 to 8
    UsbTypeCDpLaneStaggeringDelay = 0  # bit 8 to 16
    PortReversal = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 18
    PhyLaneWidth = 0  # bit 18 to 20
    PhyLinkRate = 0  # bit 20 to 24
    Reserved24 = 0  # bit 24 to 28
    PhyParamAdjust = 0  # bit 28 to 29
    OverrideTrainingEnable = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 31
    DdiBufferEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DDI_BUF_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DDI_BUF_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PHY_MISC:
    PHY_MISC_A = 0x64C00
    PHY_MISC_B = 0x64C04
    PHY_MISC_C = 0x64C08


class _PHY_MISC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 8),
        ('Reserved12', ctypes.c_uint32, 8),
        ('Spare20', ctypes.c_uint32, 1),
        ('Spare21', ctypes.c_uint32, 1),
        ('Spare22', ctypes.c_uint32, 1),
        ('DeToIoCompPwrDown', ctypes.c_uint32, 1),
        ('IoToDeMisc', ctypes.c_uint32, 4),
        ('DeToIoMisc', ctypes.c_uint32, 4),
    ]


class REG_PHY_MISC(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 4
    Reserved4 = 0  # bit 4 to 12
    Reserved12 = 0  # bit 12 to 20
    Spare20 = 0  # bit 20 to 21
    Spare21 = 0  # bit 21 to 22
    Spare22 = 0  # bit 22 to 23
    DeToIoCompPwrDown = 0  # bit 23 to 24
    IoToDeMisc = 0  # bit 24 to 28
    DeToIoMisc = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_MISC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_MISC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PERIODIC_COMP_COUNTER(Enum):
    PERIODIC_COMP_COUNTER_1_25MS = 0x5F  # Period of ~ 1.25ms w.r.t sus clock frequency of 19.2MHz.
    PERIODIC_COMP_COUNTER_10US = 0x1  # Period of ~10us w.r.t sus clock frequency of 19.2MHz.


class OFFSET_PORT_COMP_DW0:
    PORT_COMP_DW0_B = 0x6C100
    PORT_COMP_DW0_C = 0x160100
    PORT_COMP_DW0_A = 0x162100


class _PORT_COMP_DW0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 8),
        ('PeriodicCompCounter', ctypes.c_uint32, 12),
        ('Reserved20', ctypes.c_uint32, 3),
        ('ProcmonClockSel', ctypes.c_uint32, 1),
        ('CompSpare', ctypes.c_uint32, 2),
        ('TxDrvswCtl', ctypes.c_uint32, 1),
        ('TxDrvswOn', ctypes.c_uint32, 2),
        ('TxSlewCtl', ctypes.c_uint32, 2),
        ('CompInit', ctypes.c_uint32, 1),
    ]


class REG_PORT_COMP_DW0(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 8
    PeriodicCompCounter = 0  # bit 8 to 20
    Reserved20 = 0  # bit 20 to 23
    ProcmonClockSel = 0  # bit 23 to 24
    CompSpare = 0  # bit 24 to 26
    TxDrvswCtl = 0  # bit 26 to 27
    TxDrvswOn = 0  # bit 27 to 29
    TxSlewCtl = 0  # bit 29 to 31
    CompInit = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_COMP_DW1:
    PORT_COMP_DW1_B = 0x6C104
    PORT_COMP_DW1_C = 0x160104
    PORT_COMP_DW1_A = 0x162104


class _PORT_COMP_DW1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Nlvt_Ref_Lowval98', ctypes.c_uint32, 2),
        ('Nlvt_Ref_Highval98', ctypes.c_uint32, 2),
        ('Plvt_Ref_Lowval98', ctypes.c_uint32, 2),
        ('Plvt_Ref_Highval98', ctypes.c_uint32, 2),
        ('Nhvt_Ref_Lowval98', ctypes.c_uint32, 2),
        ('Nhvt_Ref_Highval98', ctypes.c_uint32, 2),
        ('Phvt_Ref_Lowval98', ctypes.c_uint32, 2),
        ('Phvt_Ref_Highval98', ctypes.c_uint32, 2),
        ('N_Ref_Lowval98', ctypes.c_uint32, 2),
        ('N_Ref_Highval98', ctypes.c_uint32, 2),
        ('P_Ref_Lowval98', ctypes.c_uint32, 2),
        ('P_Ref_Highval98', ctypes.c_uint32, 2),
        ('Rcomp_En', ctypes.c_uint32, 1),
        ('Fcomp_Polaritysel', ctypes.c_uint32, 1),
        ('Fcomp_Inputsel_Ovrd', ctypes.c_uint32, 2),
        ('Fcomp_Bias_Sel', ctypes.c_uint32, 1),
        ('Fcomp_Capratio', ctypes.c_uint32, 1),
        ('Fcomp_Ovrd_En', ctypes.c_uint32, 1),
        ('Ldo_Bypass', ctypes.c_uint32, 1),
    ]


class REG_PORT_COMP_DW1(ctypes.Union):
    value = 0
    offset = 0

    Nlvt_Ref_Lowval98 = 0  # bit 0 to 2
    Nlvt_Ref_Highval98 = 0  # bit 2 to 4
    Plvt_Ref_Lowval98 = 0  # bit 4 to 6
    Plvt_Ref_Highval98 = 0  # bit 6 to 8
    Nhvt_Ref_Lowval98 = 0  # bit 8 to 10
    Nhvt_Ref_Highval98 = 0  # bit 10 to 12
    Phvt_Ref_Lowval98 = 0  # bit 12 to 14
    Phvt_Ref_Highval98 = 0  # bit 14 to 16
    N_Ref_Lowval98 = 0  # bit 16 to 18
    N_Ref_Highval98 = 0  # bit 18 to 20
    P_Ref_Lowval98 = 0  # bit 20 to 22
    P_Ref_Highval98 = 0  # bit 22 to 24
    Rcomp_En = 0  # bit 24 to 25
    Fcomp_Polaritysel = 0  # bit 25 to 26
    Fcomp_Inputsel_Ovrd = 0  # bit 26 to 28
    Fcomp_Bias_Sel = 0  # bit 28 to 29
    Fcomp_Capratio = 0  # bit 29 to 30
    Fcomp_Ovrd_En = 0  # bit 30 to 31
    Ldo_Bypass = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_VOLTAGE_INFO(Enum):
    VOLTAGE_INFO_0_85V = 0x0
    VOLTAGE_INFO_0_95V = 0x1
    VOLTAGE_INFO_1_05 = 0x2


class ENUM_PROCESS_INFO(Enum):
    PROCESS_INFO_DOT0 = 0x0
    PROCESS_INFO_DOT1 = 0x1
    PROCESS_INFO_DOT4 = 0x2


class OFFSET_PORT_COMP_DW3:
    PORT_COMP_DW3_B = 0x6C10C
    PORT_COMP_DW3_C = 0x16010C
    PORT_COMP_DW3_A = 0x16210C


class _PORT_COMP_DW3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MipiLpdnCode', ctypes.c_uint32, 6),
        ('LpdnCodeMinout', ctypes.c_uint32, 1),
        ('LpdnCodeMaxout', ctypes.c_uint32, 1),
        ('IcompCode', ctypes.c_uint32, 7),
        ('Reserved15', ctypes.c_uint32, 4),
        ('IcompCodeMinout', ctypes.c_uint32, 1),
        ('IcompCodeMaxout', ctypes.c_uint32, 1),
        ('ProcmonDone', ctypes.c_uint32, 1),
        ('FirstCompDone', ctypes.c_uint32, 1),
        ('PllDdiPwrAck', ctypes.c_uint32, 1),
        ('VoltageInfo', ctypes.c_uint32, 2),
        ('ProcessInfo', ctypes.c_uint32, 3),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PORT_COMP_DW3(ctypes.Union):
    value = 0
    offset = 0

    MipiLpdnCode = 0  # bit 0 to 6
    LpdnCodeMinout = 0  # bit 6 to 7
    LpdnCodeMaxout = 0  # bit 7 to 8
    IcompCode = 0  # bit 8 to 15
    Reserved15 = 0  # bit 15 to 19
    IcompCodeMinout = 0  # bit 19 to 20
    IcompCodeMaxout = 0  # bit 20 to 21
    ProcmonDone = 0  # bit 21 to 22
    FirstCompDone = 0  # bit 22 to 23
    PllDdiPwrAck = 0  # bit 23 to 24
    VoltageInfo = 0  # bit 24 to 26
    ProcessInfo = 0  # bit 26 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PRDIC_ICOMP_DIS(Enum):
    PRDIC_ICOMP_DIS_ENABLE = 0x0
    PRDIC_ICOMP_DIS_DISABLE = 0x1


class ENUM_IREFGEN(Enum):
    IREFGEN_ENABLE = 0x1
    IREFGEN_DISABLE = 0x0


class OFFSET_PORT_COMP_DW8:
    PORT_COMP_DW8_B = 0x6C120
    PORT_COMP_DW8_C = 0x160120
    PORT_COMP_DW8_A = 0x162120


class _PORT_COMP_DW8(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 14),
        ('Prdic_Icomp_Dis', ctypes.c_uint32, 1),
        ('Reserved15', ctypes.c_uint32, 9),
        ('Irefgen', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 7),
    ]


class REG_PORT_COMP_DW8(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 14
    Prdic_Icomp_Dis = 0  # bit 14 to 15
    Reserved15 = 0  # bit 15 to 24
    Irefgen = 0  # bit 24 to 25
    Reserved25 = 0  # bit 25 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW8),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW8, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_COMP_DW9:
    PORT_COMP_DW9_B = 0x6C124
    PORT_COMP_DW9_C = 0x160124
    PORT_COMP_DW9_A = 0x162124


class _PORT_COMP_DW9(ctypes.LittleEndianStructure):
    _fields_ = [
        ('P_Ref_Highval70', ctypes.c_uint32, 8),
        ('P_Ref_Lowval70', ctypes.c_uint32, 8),
        ('N_Ref_Highval70', ctypes.c_uint32, 8),
        ('N_Ref_Lowval70', ctypes.c_uint32, 8),
    ]


class REG_PORT_COMP_DW9(ctypes.Union):
    value = 0
    offset = 0

    P_Ref_Highval70 = 0  # bit 0 to 8
    P_Ref_Lowval70 = 0  # bit 8 to 16
    N_Ref_Highval70 = 0  # bit 16 to 24
    N_Ref_Lowval70 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW9),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW9, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_COMP_DW10:
    PORT_COMP_DW10_B = 0x6C128
    PORT_COMP_DW10_C = 0x160128
    PORT_COMP_DW10_A = 0x162128


class _PORT_COMP_DW10(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Plvt_Ref_Highval70', ctypes.c_uint32, 8),
        ('Plvt_Ref_Lowval70', ctypes.c_uint32, 8),
        ('Nlvt_Ref_Highval70', ctypes.c_uint32, 8),
        ('Nlvt_Ref_Lowval70', ctypes.c_uint32, 8),
    ]


class REG_PORT_COMP_DW10(ctypes.Union):
    value = 0
    offset = 0

    Plvt_Ref_Highval70 = 0  # bit 0 to 8
    Plvt_Ref_Lowval70 = 0  # bit 8 to 16
    Nlvt_Ref_Highval70 = 0  # bit 16 to 24
    Nlvt_Ref_Lowval70 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW10),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW10, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CL_POWER_DOWN_ENABLE(Enum):
    CL_POWER_DOWN_DISABLE = 0x0
    CL_POWER_DOWN_ENABLE = 0x1


class OFFSET_PORT_CL_DW5:
    PORT_CL_DW5_B = 0x6C014
    PORT_CL_DW5_C = 0x160014
    PORT_CL_DW5_A = 0x162014


class _PORT_CL_DW5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SusClockConfig', ctypes.c_uint32, 2),
        ('PhyPowerAckOverride', ctypes.c_uint32, 1),
        ('CriClockSelect', ctypes.c_uint32, 1),
        ('ClPowerDownEnable', ctypes.c_uint32, 1),
        ('PgStaggeringControlDisable', ctypes.c_uint32, 1),
        ('EnablePortStaggering', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 1),
        ('DlBroadcastEnable', ctypes.c_uint32, 1),
        ('IosfClkdivSel', ctypes.c_uint32, 3),
        ('Reserved12', ctypes.c_uint32, 1),
        ('IosfPdCount', ctypes.c_uint32, 2),
        ('Reserved15', ctypes.c_uint32, 1),
        ('CriClockCountMax', ctypes.c_uint32, 4),
        ('FuseRepull', ctypes.c_uint32, 1),
        ('FusevalidOverride', ctypes.c_uint32, 1),
        ('FusevalidReset', ctypes.c_uint32, 1),
        ('Reserved23', ctypes.c_uint32, 1),
        ('Force', ctypes.c_uint32, 8),
    ]


class REG_PORT_CL_DW5(ctypes.Union):
    value = 0
    offset = 0

    SusClockConfig = 0  # bit 0 to 2
    PhyPowerAckOverride = 0  # bit 2 to 3
    CriClockSelect = 0  # bit 3 to 4
    ClPowerDownEnable = 0  # bit 4 to 5
    PgStaggeringControlDisable = 0  # bit 5 to 6
    EnablePortStaggering = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 8
    DlBroadcastEnable = 0  # bit 8 to 9
    IosfClkdivSel = 0  # bit 9 to 12
    Reserved12 = 0  # bit 12 to 13
    IosfPdCount = 0  # bit 13 to 15
    Reserved15 = 0  # bit 15 to 16
    CriClockCountMax = 0  # bit 16 to 20
    FuseRepull = 0  # bit 20 to 21
    FusevalidOverride = 0  # bit 21 to 22
    FusevalidReset = 0  # bit 22 to 23
    Reserved23 = 0  # bit 23 to 24
    Force = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CL_DW5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CL_DW5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_O_RTERM100EN_H_OVRD_VAL(Enum):
    O_RTERM100EN_H_OVRD_VAL_150_OHMS = 0x0
    O_RTERM100EN_H_OVRD_VAL_100_OHMS = 0x1


class ENUM_O_EDP4K2K_MODE_OVRD_VAL(Enum):
    O_EDP4K2K_MODE_OVRD_VAL_OPTIMIZED = 0x1
    O_EDP4K2K_MODE_OVRD_VAL_NONOPTIMIZED = 0x0


class ENUM_O_EDP4K2K_MODE_OVRD_EN(Enum):
    O_EDP4K2K_MODE_OVRD_EN_ENABLE = 0x1
    O_EDP4K2K_MODE_OVRD_EN_DISABLE = 0x0


class ENUM_STATIC_POWER_DOWN(Enum):
    STATIC_POWER_DOWN_POWER_UP_ALL_LANES = 0x0  # Enable x4
    STATIC_POWER_DOWN_POWER_DOWN_LANES_3_2 = 0xC  # Enable x2
    STATIC_POWER_DOWN_POWER_DOWN_LANES_3_2_1 = 0xE  # Enable x1
    STATIC_POWER_DOWN_POWER_DOWN_LANES_1_0 = 0x3  # Enable x2 Reversed
    STATIC_POWER_DOWN_POWER_DOWN_LANES_2_1_0 = 0x7  # Enable x1 Reversed
    STATIC_POWER_DOWN_POWER_DOWN_LANES_3_1_0 = 0xB  # Enable DSI x1
    STATIC_POWER_DOWN_POWER_DOWN_LANES_3_1 = 0xA  # Enable DSI x2
    STATIC_POWER_DOWN_POWER_DOWN_LANE_3 = 0x8  # Enable DSI x3


class ENUM_PG_SEQ_DELAY_OVERRIDE_ENABLE(Enum):
    PG_SEQ_DELAY_OVERRIDE_DISABLE = 0x0
    PG_SEQ_DELAY_OVERRIDE_ENABLE = 0x1


class OFFSET_PORT_CL_DW10:
    PORT_CL_DW10_B = 0x6C028
    PORT_CL_DW10_C = 0x160028
    PORT_CL_DW10_A = 0x162028


class _PORT_CL_DW10(ctypes.LittleEndianStructure):
    _fields_ = [
        ('O_Rterm100En_H_Ovrd_Val', ctypes.c_uint32, 1),
        ('O_Rterm100En_H_Ovrd_En', ctypes.c_uint32, 1),
        ('O_Edp4K2K_Mode_Ovrd_Val', ctypes.c_uint32, 1),
        ('O_Edp4K2K_Mode_Ovrd_En', ctypes.c_uint32, 1),
        ('StaticPowerDown', ctypes.c_uint32, 4),
        ('Spare8', ctypes.c_uint32, 1),
        ('Spare9', ctypes.c_uint32, 1),
        ('Spare10', ctypes.c_uint32, 1),
        ('Spare11', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 4),
        ('Ospare_Cri_Ret', ctypes.c_uint32, 6),
        ('Spare22', ctypes.c_uint32, 1),
        ('Ohvpg_Ctrl_Mipia', ctypes.c_uint32, 1),
        ('PgSeqDelayOverrideEnable', ctypes.c_uint32, 1),
        ('PgSeqDelayOverride', ctypes.c_uint32, 2),
        ('Reserved27', ctypes.c_uint32, 5),
    ]


class REG_PORT_CL_DW10(ctypes.Union):
    value = 0
    offset = 0

    O_Rterm100En_H_Ovrd_Val = 0  # bit 0 to 1
    O_Rterm100En_H_Ovrd_En = 0  # bit 1 to 2
    O_Edp4K2K_Mode_Ovrd_Val = 0  # bit 2 to 3
    O_Edp4K2K_Mode_Ovrd_En = 0  # bit 3 to 4
    StaticPowerDown = 0  # bit 4 to 8
    Spare8 = 0  # bit 8 to 9
    Spare9 = 0  # bit 9 to 10
    Spare10 = 0  # bit 10 to 11
    Spare11 = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 16
    Ospare_Cri_Ret = 0  # bit 16 to 22
    Spare22 = 0  # bit 22 to 23
    Ohvpg_Ctrl_Mipia = 0  # bit 23 to 24
    PgSeqDelayOverrideEnable = 0  # bit 24 to 25
    PgSeqDelayOverride = 0  # bit 25 to 27
    Reserved27 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CL_DW10),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CL_DW10, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_LANE_ENABLE_AUX(Enum):
    LANE_ENABLE_AUX_DISABLE = 0x0
    LANE_ENABLE_AUX_ENABLE = 0x1


class ENUM_PWR_REQ_OVERRIDE_ENABLE_AUX(Enum):
    PWR_REQ_OVERRIDE_ENABLE_AUX_DISABLE = 0x0
    PWR_REQ_OVERRIDE_ENABLE_AUX_ENABLE = 0x1


class ENUM_MIPI_LANE_ENABLE(Enum):
    MIPI_LANE_DISABLE = 0x0
    MIPI_LANE_ENABLE = 0x1


class OFFSET_PORT_CL_DW12:
    PORT_CL_DW12_B = 0x6C030
    PORT_CL_DW12_C = 0x160030
    PORT_CL_DW12_A = 0x162030


class _PORT_CL_DW12(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LaneEnableAux', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 3),
        ('PowerAckAux', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 1),
        ('PhyStatusAux', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 3),
        ('PwrReqOverrideEnableAux', ctypes.c_uint32, 1),
        ('PwrReqOverrideAux', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 14),
        ('MipiModeOverride', ctypes.c_uint32, 1),
        ('MipiModeOverrideEnable', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 1),
        ('MipiLaneEnable', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PORT_CL_DW12(ctypes.Union):
    value = 0
    offset = 0

    LaneEnableAux = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 4
    PowerAckAux = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 6
    PhyStatusAux = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 10
    PwrReqOverrideEnableAux = 0  # bit 10 to 11
    PwrReqOverrideAux = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 26
    MipiModeOverride = 0  # bit 26 to 27
    MipiModeOverrideEnable = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 29
    MipiLaneEnable = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CL_DW12),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CL_DW12, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_CL_DW15:
    PORT_CL_DW15_B = 0x6C03C
    PORT_CL_DW15_C = 0x16003C
    PORT_CL_DW15_A = 0x16203C


class _PORT_CL_DW15(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 17),
        ('PowerAckAux', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 3),
        ('PowerReqAux', ctypes.c_uint32, 1),
        ('Reserved22', ctypes.c_uint32, 5),
        ('PowerAckMipi', ctypes.c_uint32, 1),
        ('HvpgEnableStatus', ctypes.c_uint32, 1),
        ('HvpgPowerAck', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PORT_CL_DW15(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 17
    PowerAckAux = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 21
    PowerReqAux = 0  # bit 21 to 22
    Reserved22 = 0  # bit 22 to 27
    PowerAckMipi = 0  # bit 27 to 28
    HvpgEnableStatus = 0  # bit 28 to 29
    HvpgPowerAck = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CL_DW15),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CL_DW15, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_TX_DW2:
    PORT_TX_DW2_AUX_B = 0x6C388
    PORT_TX_DW2_GRP_B = 0x6C688
    PORT_TX_DW2_LN0_B = 0x6C888
    PORT_TX_DW2_LN1_B = 0x6C988
    PORT_TX_DW2_LN2_B = 0x6CA88
    PORT_TX_DW2_LN3_B = 0x6CB88
    PORT_TX_DW2_AUX_C = 0x160388
    PORT_TX_DW2_GRP_C = 0x160688
    PORT_TX_DW2_LN0_C = 0x160888
    PORT_TX_DW2_LN1_C = 0x160988
    PORT_TX_DW2_LN2_C = 0x160A88
    PORT_TX_DW2_LN3_C = 0x160B88
    PORT_TX_DW2_AUX_A = 0x162388
    PORT_TX_DW2_GRP_A = 0x162688
    PORT_TX_DW2_LN0_A = 0x162888
    PORT_TX_DW2_LN1_A = 0x162988
    PORT_TX_DW2_LN2_A = 0x162A88
    PORT_TX_DW2_LN3_A = 0x162B88


class _PORT_TX_DW2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RcompScalar', ctypes.c_uint32, 8),
        ('Frclatencyoptim', ctypes.c_uint32, 3),
        ('Swing_SelLower', ctypes.c_uint32, 3),
        ('Cmnmode_Sel', ctypes.c_uint32, 1),
        ('Swing_SelUpper', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_PORT_TX_DW2(ctypes.Union):
    value = 0
    offset = 0

    RcompScalar = 0  # bit 0 to 8
    Frclatencyoptim = 0  # bit 8 to 11
    Swing_SelLower = 0  # bit 11 to 14
    Cmnmode_Sel = 0  # bit 14 to 15
    Swing_SelUpper = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_TX_DW4:
    PORT_TX_DW4_AUX_B = 0x6C390
    PORT_TX_DW4_GRP_B = 0x6C690
    PORT_TX_DW4_LN0_B = 0x6C890
    PORT_TX_DW4_LN1_B = 0x6C990
    PORT_TX_DW4_LN2_B = 0x6CA90
    PORT_TX_DW4_LN3_B = 0x6CB90
    PORT_TX_DW4_AUX_C = 0x160390
    PORT_TX_DW4_GRP_C = 0x160690
    PORT_TX_DW4_LN0_C = 0x160890
    PORT_TX_DW4_LN1_C = 0x160990
    PORT_TX_DW4_LN2_C = 0x160A90
    PORT_TX_DW4_LN3_C = 0x160B90
    PORT_TX_DW4_AUX_A = 0x162390
    PORT_TX_DW4_GRP_A = 0x162690
    PORT_TX_DW4_LN0_A = 0x162890
    PORT_TX_DW4_LN1_A = 0x162990
    PORT_TX_DW4_LN2_A = 0x162A90
    PORT_TX_DW4_LN3_A = 0x162B90


class _PORT_TX_DW4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CursorCoeff', ctypes.c_uint32, 6),
        ('PostCursor2', ctypes.c_uint32, 6),
        ('PostCursor1', ctypes.c_uint32, 6),
        ('RtermLimit', ctypes.c_uint32, 5),
        ('BsCompOvrd', ctypes.c_uint32, 1),
        ('Spare', ctypes.c_uint32, 7),
        ('LoadgenSelect', ctypes.c_uint32, 1),
    ]


class REG_PORT_TX_DW4(ctypes.Union):
    value = 0
    offset = 0

    CursorCoeff = 0  # bit 0 to 6
    PostCursor2 = 0  # bit 6 to 12
    PostCursor1 = 0  # bit 12 to 18
    RtermLimit = 0  # bit 18 to 23
    BsCompOvrd = 0  # bit 23 to 24
    Spare = 0  # bit 24 to 31
    LoadgenSelect = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW4),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_COEFF_POLARITY(Enum):
    COEFF_POLARITY_ENABLE = 0x0
    COEFF_POLARITY_DISABLE = 0x1


class ENUM_CURSOR_PROGRAM(Enum):
    CURSOR_PROGRAM_ENABLE = 0x0
    CURSOR_PROGRAM_DISABLE = 0x1


class ENUM_DISABLE_3TAP(Enum):
    DISABLE_3TAP_ENABLE = 0x0
    DISABLE_3TAP_DISABLE = 0x1


class ENUM_DISABLE_2TAP(Enum):
    DISABLE_2TAP_ENABLE = 0x0
    DISABLE_2TAP_DISABLE = 0x1


class ENUM_TX_TRAINING_ENABLE(Enum):
    TX_TRAINING_ENABLE = 0x1
    TX_TRAINING_DISABLE = 0x0


class OFFSET_PORT_TX_DW5:
    PORT_TX_DW5_AUX_B = 0x6C394
    PORT_TX_DW5_GRP_B = 0x6C694
    PORT_TX_DW5_LN0_B = 0x6C894
    PORT_TX_DW5_LN1_B = 0x6C994
    PORT_TX_DW5_LN2_B = 0x6CA94
    PORT_TX_DW5_LN3_B = 0x6CB94
    PORT_TX_DW5_AUX_C = 0x160394
    PORT_TX_DW5_GRP_C = 0x160694
    PORT_TX_DW5_LN0_C = 0x160894
    PORT_TX_DW5_LN1_C = 0x160994
    PORT_TX_DW5_LN2_C = 0x160A94
    PORT_TX_DW5_LN3_C = 0x160B94
    PORT_TX_DW5_AUX_A = 0x162394
    PORT_TX_DW5_GRP_A = 0x162694
    PORT_TX_DW5_LN0_A = 0x162894
    PORT_TX_DW5_LN1_A = 0x162994
    PORT_TX_DW5_LN2_A = 0x162A94
    PORT_TX_DW5_LN3_A = 0x162B94


class _PORT_TX_DW5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare20', ctypes.c_uint32, 3),
        ('RtermSelect', ctypes.c_uint32, 3),
        ('Spare106', ctypes.c_uint32, 5),
        ('CrScalingCoef', ctypes.c_uint32, 5),
        ('DecodeTimerSel', ctypes.c_uint32, 2),
        ('ScalingModeSel', ctypes.c_uint32, 3),
        ('Reserved21', ctypes.c_uint32, 3),
        ('Spare24', ctypes.c_uint32, 1),
        ('CoeffPolarity', ctypes.c_uint32, 1),
        ('CursorProgram', ctypes.c_uint32, 1),
        ('Spare2827', ctypes.c_uint32, 2),
        ('Disable3Tap', ctypes.c_uint32, 1),
        ('Disable2Tap', ctypes.c_uint32, 1),
        ('TxTrainingEnable', ctypes.c_uint32, 1),
    ]


class REG_PORT_TX_DW5(ctypes.Union):
    value = 0
    offset = 0

    Spare20 = 0  # bit 0 to 3
    RtermSelect = 0  # bit 3 to 6
    Spare106 = 0  # bit 6 to 11
    CrScalingCoef = 0  # bit 11 to 16
    DecodeTimerSel = 0  # bit 16 to 18
    ScalingModeSel = 0  # bit 18 to 21
    Reserved21 = 0  # bit 21 to 24
    Spare24 = 0  # bit 24 to 25
    CoeffPolarity = 0  # bit 25 to 26
    CursorProgram = 0  # bit 26 to 27
    Spare2827 = 0  # bit 27 to 29
    Disable3Tap = 0  # bit 29 to 30
    Disable2Tap = 0  # bit 30 to 31
    TxTrainingEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_TX_DW7:
    PORT_TX_DW7_AUX_B = 0x6C39C
    PORT_TX_DW7_GRP_B = 0x6C69C
    PORT_TX_DW7_LN0_B = 0x6C89C
    PORT_TX_DW7_LN1_B = 0x6C99C
    PORT_TX_DW7_LN2_B = 0x6CA9C
    PORT_TX_DW7_LN3_B = 0x6CB9C
    PORT_TX_DW7_AUX_C = 0x16039C
    PORT_TX_DW7_GRP_C = 0x16069C
    PORT_TX_DW7_LN0_C = 0x16089C
    PORT_TX_DW7_LN1_C = 0x16099C
    PORT_TX_DW7_LN2_C = 0x160A9C
    PORT_TX_DW7_LN3_C = 0x160B9C
    PORT_TX_DW7_AUX_A = 0x16239C
    PORT_TX_DW7_GRP_A = 0x16269C
    PORT_TX_DW7_LN0_A = 0x16289C
    PORT_TX_DW7_LN1_A = 0x16299C
    PORT_TX_DW7_LN2_A = 0x162A9C
    PORT_TX_DW7_LN3_A = 0x162B9C


class _PORT_TX_DW7(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare230', ctypes.c_uint32, 24),
        ('NScalar', ctypes.c_uint32, 7),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_PORT_TX_DW7(ctypes.Union):
    value = 0
    offset = 0

    Spare230 = 0  # bit 0 to 24
    NScalar = 0  # bit 24 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW7),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW7, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SOFTRESET_ENABLE(Enum):
    SOFTRESET_ENABLE = 0x1
    SOFTRESET_DISABLE = 0x0


class ENUM_DCC_MODE_SELECT(Enum):
    DCC_MODE_SELECT_RUN_DCC_ONCE = 0x0
    DCC_MODE_SELECT_RUN_DCC_EVERY_100US = 0x1
    DCC_MODE_SELECT_RUN_DCC_EVERY_1MS = 0x2
    DCC_MODE_SELECT_RUN_DCC_CONTINUOSLY = 0x3


class ENUM_CMNKEEPER_ENABLE(Enum):
    CMNKEEPER_ENABLE = 0x1
    CMNKEEPER_DISABLE = 0x0


class ENUM_PG_PWRDOWNEN(Enum):
    PG_PWRDOWNEN_ENABLE = 0x1
    PG_PWRDOWNEN_DISABLE = 0x0


class ENUM_CMNKEEPER_ENABLE_IN_PG(Enum):
    CMNKEEPER_ENABLE_IN_PG_ENABLE = 0x1
    CMNKEEPER_ENABLE_IN_PG_DISABLE = 0x0


class OFFSET_PORT_PCS_DW1:
    PORT_PCS_DW1_AUX_B = 0x6C304
    PORT_PCS_DW1_GRP_B = 0x6C604
    PORT_PCS_DW1_LN0_B = 0x6C804
    PORT_PCS_DW1_LN1_B = 0x6C904
    PORT_PCS_DW1_LN2_B = 0x6CA04
    PORT_PCS_DW1_LN3_B = 0x6CB04
    PORT_PCS_DW1_AUX_C = 0x160304
    PORT_PCS_DW1_GRP_C = 0x160604
    PORT_PCS_DW1_LN0_C = 0x160804
    PORT_PCS_DW1_LN1_C = 0x160904
    PORT_PCS_DW1_LN2_C = 0x160A04
    PORT_PCS_DW1_LN3_C = 0x160B04
    PORT_PCS_DW1_AUX_A = 0x162304
    PORT_PCS_DW1_GRP_A = 0x162604
    PORT_PCS_DW1_LN0_A = 0x162804
    PORT_PCS_DW1_LN1_A = 0x162904
    PORT_PCS_DW1_LN2_A = 0x162A04
    PORT_PCS_DW1_LN3_A = 0x162B04


class _PORT_PCS_DW1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Soft_Reset_N', ctypes.c_uint32, 1),
        ('Softreset_Enable', ctypes.c_uint32, 1),
        ('Latencyoptim', ctypes.c_uint32, 2),
        ('Txdeemp', ctypes.c_uint32, 1),
        ('Txfifo_Rst_Main_Ovrd', ctypes.c_uint32, 1),
        ('Txfifo_Rst_Main_Ovrden', ctypes.c_uint32, 1),
        ('Tbc_As_Symbclk', ctypes.c_uint32, 1),
        ('Clkreq', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 2),
        ('Txhigh', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 2),
        ('Reserved16', ctypes.c_uint32, 1),
        ('Tx_Dcc_Calib_Enable', ctypes.c_uint32, 1),
        ('Reg_Dcc_Calib_Wake_En', ctypes.c_uint32, 1),
        ('Reg_Dcc_Bypass', ctypes.c_uint32, 1),
        ('DccModeSelect', ctypes.c_uint32, 2),
        ('Reserved22', ctypes.c_uint32, 2),
        ('Cmnkeep_Biasctr', ctypes.c_uint32, 2),
        ('Cmnkeeper_Enable', ctypes.c_uint32, 1),
        ('Pg_Pwrdownen', ctypes.c_uint32, 1),
        ('Cmnkeeper_Enable_In_Pg', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PORT_PCS_DW1(ctypes.Union):
    value = 0
    offset = 0

    Soft_Reset_N = 0  # bit 0 to 1
    Softreset_Enable = 0  # bit 1 to 2
    Latencyoptim = 0  # bit 2 to 4
    Txdeemp = 0  # bit 4 to 5
    Txfifo_Rst_Main_Ovrd = 0  # bit 5 to 6
    Txfifo_Rst_Main_Ovrden = 0  # bit 6 to 7
    Tbc_As_Symbclk = 0  # bit 7 to 8
    Clkreq = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 12
    Txhigh = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 16
    Reserved16 = 0  # bit 16 to 17
    Tx_Dcc_Calib_Enable = 0  # bit 17 to 18
    Reg_Dcc_Calib_Wake_En = 0  # bit 18 to 19
    Reg_Dcc_Bypass = 0  # bit 19 to 20
    DccModeSelect = 0  # bit 20 to 22
    Reserved22 = 0  # bit 22 to 24
    Cmnkeep_Biasctr = 0  # bit 24 to 26
    Cmnkeeper_Enable = 0  # bit 26 to 27
    Pg_Pwrdownen = 0  # bit 27 to 28
    Cmnkeeper_Enable_In_Pg = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_PCS_DW1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_PCS_DW1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_PCS_DW9:
    PORT_PCS_DW9_AUX_B = 0x6C324
    PORT_PCS_DW9_GRP_B = 0x6C624
    PORT_PCS_DW9_LN0_B = 0x6C824
    PORT_PCS_DW9_LN1_B = 0x6C924
    PORT_PCS_DW9_LN2_B = 0x6CA24
    PORT_PCS_DW9_LN3_B = 0x6CB24
    PORT_PCS_DW9_AUX_C = 0x160324
    PORT_PCS_DW9_GRP_C = 0x160624
    PORT_PCS_DW9_LN0_C = 0x160824
    PORT_PCS_DW9_LN1_C = 0x160924
    PORT_PCS_DW9_LN2_C = 0x160A24
    PORT_PCS_DW9_LN3_C = 0x160B24
    PORT_PCS_DW9_AUX_A = 0x162324
    PORT_PCS_DW9_GRP_A = 0x162624
    PORT_PCS_DW9_LN0_A = 0x162824
    PORT_PCS_DW9_LN1_A = 0x162924
    PORT_PCS_DW9_LN2_A = 0x162A24
    PORT_PCS_DW9_LN3_A = 0x162B24


class _PORT_PCS_DW9(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Stagger', ctypes.c_uint32, 5),
        ('StaggerOverride', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 2),
        ('StaggerMult', ctypes.c_uint32, 3),
        ('Reserved11', ctypes.c_uint32, 5),
        ('StrongCmCountOvrd', ctypes.c_uint32, 12),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_PORT_PCS_DW9(ctypes.Union):
    value = 0
    offset = 0

    Stagger = 0  # bit 0 to 5
    StaggerOverride = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 8
    StaggerMult = 0  # bit 8 to 11
    Reserved11 = 0  # bit 11 to 16
    StrongCmCountOvrd = 0  # bit 16 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_PCS_DW9),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_PCS_DW9, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_TX_DFLEXDPPMS:
    PORT_TX_DFLEXDPPMS_FIA1 = 0x163890
    PORT_TX_DFLEXDPPMS_FIA2 = 0x16E890


class _PORT_TX_DFLEXDPPMS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare', ctypes.c_uint32, 32),
    ]


class REG_PORT_TX_DFLEXDPPMS(ctypes.Union):
    value = 0
    offset = 0

    Spare = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXDPPMS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXDPPMS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7_ML30 = 0xF


class OFFSET_PORT_TX_DFLEXDPMLE1:
    PORT_TX_DFLEXDPMLE1_FIA1 = 0x1638C0
    PORT_TX_DFLEXDPMLE1_FIA2 = 0x16E8C0


class _PORT_TX_DFLEXDPMLE1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayportMainLinkEnableForTypeCConnector0', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector1', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector2', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector3', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector4', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector5', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector6', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector7', ctypes.c_uint32, 4),
    ]


class REG_PORT_TX_DFLEXDPMLE1(ctypes.Union):
    value = 0
    offset = 0

    DisplayportMainLinkEnableForTypeCConnector0 = 0  # bit 0 to 4
    DisplayportMainLinkEnableForTypeCConnector1 = 0  # bit 4 to 8
    DisplayportMainLinkEnableForTypeCConnector2 = 0  # bit 8 to 12
    DisplayportMainLinkEnableForTypeCConnector3 = 0  # bit 12 to 16
    DisplayportMainLinkEnableForTypeCConnector4 = 0  # bit 16 to 20
    DisplayportMainLinkEnableForTypeCConnector5 = 0  # bit 20 to 24
    DisplayportMainLinkEnableForTypeCConnector6 = 0  # bit 24 to 28
    DisplayportMainLinkEnableForTypeCConnector7 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXDPMLE1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXDPMLE1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_TX_DFLEXDPCSSS:
    PORT_TX_DFLEXDPCSSS_FIA1 = 0x163894
    PORT_TX_DFLEXDPCSSS_FIA2 = 0x16E894


class _PORT_TX_DFLEXDPCSSS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare', ctypes.c_uint32, 32),
    ]


class REG_PORT_TX_DFLEXDPCSSS(ctypes.Union):
    value = 0
    offset = 0

    Spare = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXDPCSSS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXDPCSSS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0(Enum):
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX0 = 0x1
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX1 = 0x2
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX10 = 0x3
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX2 = 0x4
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX2_TX0 = 0x5
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX3 = 0x8
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX32 = 0xC
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX30 = 0xF


class ENUM_DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1(Enum):
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX0 = 0x1
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX1 = 0x2
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX10 = 0x3
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX2 = 0x4
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX2_TX0 = 0x5
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX3 = 0x8
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX32 = 0xC
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX30 = 0xF


class ENUM_IOM_FW_VERSION(Enum):
    IOM_FW_VERSION_OLD_IOM_FW = 0x0
    IOM_FW_VERSION_IOM_FW_WITH_MFD_GEN2_SUPPORT = 0x1


class ENUM_DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2(Enum):
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX0 = 0x1
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX1 = 0x2
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX10 = 0x3
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX2 = 0x4
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX2_TX0 = 0x5
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX3 = 0x8
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX32 = 0xC
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX30 = 0xF


class ENUM_DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3(Enum):
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX0 = 0x1
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX1 = 0x2
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX10 = 0x3
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX2 = 0x4
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX2_TX0 = 0x5
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX3 = 0x8
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX32 = 0xC
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX30 = 0xF


class OFFSET_PORT_TX_DFLEXDPSP:
    PORT_TX_DFLEXDPSP1_FIA1 = 0x1638A0
    PORT_TX_DFLEXDPSP2_FIA1 = 0x1638A4
    PORT_TX_DFLEXDPSP3_FIA1 = 0x1638A8
    PORT_TX_DFLEXDPSP4_FIA1 = 0x1638AC
    PORT_TX_DFLEXDPSP1_FIA2 = 0x16E8A0
    PORT_TX_DFLEXDPSP2_FIA2 = 0x16E8A4
    PORT_TX_DFLEXDPSP3_FIA2 = 0x16E8A8
    PORT_TX_DFLEXDPSP4_FIA2 = 0x16E8AC


class _PORT_TX_DFLEXDPSP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector0', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 3),
        ('Reserved7', ctypes.c_uint32, 1),
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector1', ctypes.c_uint32, 4),
        ('IomFwVersion', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 2),
        ('Reserved15', ctypes.c_uint32, 1),
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector2', ctypes.c_uint32, 4),
        ('Reserved20', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 2),
        ('Reserved23', ctypes.c_uint32, 1),
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector3', ctypes.c_uint32, 4),
        ('Reserved28', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 2),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_PORT_TX_DFLEXDPSP(ctypes.Union):
    value = 0
    offset = 0

    DisplayPortX4TxLaneAssignmentForTypeCConnector0 = 0  # bit 0 to 4
    Reserved4 = 0  # bit 4 to 7
    Reserved7 = 0  # bit 7 to 8
    DisplayPortX4TxLaneAssignmentForTypeCConnector1 = 0  # bit 8 to 12
    IomFwVersion = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 15
    Reserved15 = 0  # bit 15 to 16
    DisplayPortX4TxLaneAssignmentForTypeCConnector2 = 0  # bit 16 to 20
    Reserved20 = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 23
    Reserved23 = 0  # bit 23 to 24
    DisplayPortX4TxLaneAssignmentForTypeCConnector3 = 0  # bit 24 to 28
    Reserved28 = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXDPSP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXDPSP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0(Enum):
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_NO_PIN_ASSIGNMENT_FOR_NON_TYPEC_DP = 0x0
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_A = 0x1
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_B = 0x2
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C = 0x3
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_D = 0x4
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_E = 0x5
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_F = 0x6


class OFFSET_PORT_TX_DFLEXPA1:
    PORT_TX_DFLEXPA1_FIA1 = 0x163880
    PORT_TX_DFLEXPA1_FIA2 = 0x16E880


class _PORT_TX_DFLEXPA1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayportPinAssignmentForTypeCConnector0', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector1', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector2', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector3', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector4', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector5', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector6', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector7', ctypes.c_uint32, 4),
    ]


class REG_PORT_TX_DFLEXPA1(ctypes.Union):
    value = 0
    offset = 0

    DisplayportPinAssignmentForTypeCConnector0 = 0  # bit 0 to 4
    DisplayportPinAssignmentForTypeCConnector1 = 0  # bit 4 to 8
    DisplayportPinAssignmentForTypeCConnector2 = 0  # bit 8 to 12
    DisplayportPinAssignmentForTypeCConnector3 = 0  # bit 12 to 16
    DisplayportPinAssignmentForTypeCConnector4 = 0  # bit 16 to 20
    DisplayportPinAssignmentForTypeCConnector5 = 0  # bit 20 to 24
    DisplayportPinAssignmentForTypeCConnector6 = 0  # bit 24 to 28
    DisplayportPinAssignmentForTypeCConnector7 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXPA1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXPA1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_TX_DFLEXPA2:
    PORT_TX_DFLEXPA2_FIA1 = 0x163884
    PORT_TX_DFLEXPA2_FIA2 = 0x16E884


class _PORT_TX_DFLEXPA2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayportPinAssignmentForTypeCConnector8', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector9', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector10', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector11', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector12', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector13', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector14', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector15', ctypes.c_uint32, 4),
    ]


class REG_PORT_TX_DFLEXPA2(ctypes.Union):
    value = 0
    offset = 0

    DisplayportPinAssignmentForTypeCConnector8 = 0  # bit 0 to 4
    DisplayportPinAssignmentForTypeCConnector9 = 0  # bit 4 to 8
    DisplayportPinAssignmentForTypeCConnector10 = 0  # bit 8 to 12
    DisplayportPinAssignmentForTypeCConnector11 = 0  # bit 12 to 16
    DisplayportPinAssignmentForTypeCConnector12 = 0  # bit 16 to 20
    DisplayportPinAssignmentForTypeCConnector13 = 0  # bit 20 to 24
    DisplayportPinAssignmentForTypeCConnector14 = 0  # bit 24 to 28
    DisplayportPinAssignmentForTypeCConnector15 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXPA2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXPA2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


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


class OFFSET_HIP_INDEX_REG1:
    HIP_INDEX_REG1 = 0x1010A4


class _HIP_INDEX_REG1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hip_16C_Index', ctypes.c_uint32, 8),
        ('Hip_16D_Index', ctypes.c_uint32, 8),
        ('Hip_16E_Index', ctypes.c_uint32, 8),
        ('Hip_16F_Index', ctypes.c_uint32, 8),
    ]


class REG_HIP_INDEX_REG1(ctypes.Union):
    value = 0
    offset = 0

    Hip_16C_Index = 0  # bit 0 to 8
    Hip_16D_Index = 0  # bit 8 to 16
    Hip_16E_Index = 0  # bit 16 to 24
    Hip_16F_Index = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HIP_INDEX_REG1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HIP_INDEX_REG1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_VSWING_CONTROL_TX1(Enum):
    CFG_VSWING_CONTROL_TX1_CFG_VSWING_CONTROL_TX1_DEFAULTRESET = 0x7


class ENUM_CFG_CURSOR_CONTROL_TX1(Enum):
    CFG_CURSOR_CONTROL_TX1_CFG_CURSOR_CONTROL_TX1_DEFAULTRESET = 0x0


class ENUM_CFG_DE_EMPHASIS_CONTROL_L0_TX1(Enum):
    CFG_DE_EMPHASIS_CONTROL_L0_TX1_CFG_DE_EMPHASIS_CONTROL_L0_TX1_DEFAULTRESET = 0x0


class ENUM_CFG_PRESHOOT_CONTROL_L0_TX1(Enum):
    CFG_PRESHOOT_CONTROL_L0_TX1_CFG_PRESHOOT_CONTROL_L0_TX1_DEFAULTRESET = 0x0


class ENUM_CFG_SHUNT_CP_TX1(Enum):
    CFG_SHUNT_CP_TX1_CFG_SHUNT_CP_TX1_DEFAULTRESET = 0x0


class ENUM_CFG_SHUNT_CM_TX1(Enum):
    CFG_SHUNT_CM_TX1_CFG_SHUNT_CM_TX1_DEFAULTRESET = 0x0


class ENUM_CFG_SLOW_TRIM_ENABLE_TX1(Enum):
    CFG_SLOW_TRIM_ENABLE_TX1_CFG_SLOW_TRIM_ENABLE_TX1_DEFAULTRESET = 0x1


class ENUM_CFG_PIPE_SELECT_TX1(Enum):
    CFG_PIPE_SELECT_TX1_CFG_PIPE_SELECT_TX1_DEFAULTRESET = 0x0


class ENUM_CFG_TRAININGEN_TX1(Enum):
    CFG_TRAININGEN_TX1_CFG_TRAININGEN_TX1_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED_TX1(Enum):
    CFG_RESERVED_TX1_CFG_RESERVED_TX1_DEFAULTRESET = 0x0


class OFFSET_DKLP_PCS_GLUE_TX_DPCNTL0:
    DKLP_PCS_GLUE_TX_DPCNTL0 = 0x2C0


class _DKLP_PCS_GLUE_TX_DPCNTL0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Vswing_Control_Tx1', ctypes.c_uint32, 3),
        ('Cfg_Cursor_Control_Tx1', ctypes.c_uint32, 5),
        ('Cfg_De_Emphasis_Control_L0_Tx1', ctypes.c_uint32, 5),
        ('Cfg_Preshoot_Control_L0_Tx1', ctypes.c_uint32, 5),
        ('Cfg_Shunt_Cp_Tx1', ctypes.c_uint32, 5),
        ('Cfg_Shunt_Cm_Tx1', ctypes.c_uint32, 5),
        ('Cfg_Slow_Trim_Enable_Tx1', ctypes.c_uint32, 1),
        ('Cfg_Pipe_Select_Tx1', ctypes.c_uint32, 1),
        ('Cfg_Trainingen_Tx1', ctypes.c_uint32, 1),
        ('Cfg_Reserved_Tx1', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PCS_GLUE_TX_DPCNTL0(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Vswing_Control_Tx1 = 0  # bit 0 to 3
    Cfg_Cursor_Control_Tx1 = 0  # bit 3 to 8
    Cfg_De_Emphasis_Control_L0_Tx1 = 0  # bit 8 to 13
    Cfg_Preshoot_Control_L0_Tx1 = 0  # bit 13 to 18
    Cfg_Shunt_Cp_Tx1 = 0  # bit 18 to 23
    Cfg_Shunt_Cm_Tx1 = 0  # bit 23 to 28
    Cfg_Slow_Trim_Enable_Tx1 = 0  # bit 28 to 29
    Cfg_Pipe_Select_Tx1 = 0  # bit 29 to 30
    Cfg_Trainingen_Tx1 = 0  # bit 30 to 31
    Cfg_Reserved_Tx1 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PCS_GLUE_TX_DPCNTL0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PCS_GLUE_TX_DPCNTL0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_VSWING_CONTROL_TX2(Enum):
    CFG_VSWING_CONTROL_TX2_CFG_VSWING_CONTROL_TX2_DEFAULTRESET = 0x7


class ENUM_CFG_CURSOR_CONTROL_TX2(Enum):
    CFG_CURSOR_CONTROL_TX2_CFG_CURSOR_CONTROL_TX2_DEFAULTRESET = 0x0


class ENUM_CFG_DE_EMPHASIS_CONTROL_L0_TX2(Enum):
    CFG_DE_EMPHASIS_CONTROL_L0_TX2_CFG_DE_EMPHASIS_CONTROL_L0_TX2_DEFAULTRESET = 0x0


class ENUM_CFG_PRESHOOT_CONTROL_L0_TX2(Enum):
    CFG_PRESHOOT_CONTROL_L0_TX2_CFG_PRESHOOT_CONTROL_L0_TX2_DEFAULTRESET = 0x0


class ENUM_CFG_SHUNT_CP_TX2(Enum):
    CFG_SHUNT_CP_TX2_CFG_SHUNT_CP_TX2_DEFAULTRESET = 0x0


class ENUM_CFG_SHUNT_CM_TX2(Enum):
    CFG_SHUNT_CM_TX2_CFG_SHUNT_CM_TX2_DEFAULTRESET = 0x0


class ENUM_CFG_SLOW_TRIM_ENABLE_TX2(Enum):
    CFG_SLOW_TRIM_ENABLE_TX2_CFG_SLOW_TRIM_ENABLE_TX2_DEFAULTRESET = 0x1


class ENUM_CFG_PIPE_SELECT_TX2(Enum):
    CFG_PIPE_SELECT_TX2_CFG_PIPE_SELECT_TX2_DEFAULTRESET = 0x0


class ENUM_CFG_TRAININGEN_TX2(Enum):
    CFG_TRAININGEN_TX2_CFG_TRAININGEN_TX2_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED_TX2(Enum):
    CFG_RESERVED_TX2_CFG_RESERVED_TX2_DEFAULTRESET = 0x0


class OFFSET_DKLP_PCS_GLUE_TX_DPCNTL1:
    DKLP_PCS_GLUE_TX_DPCNTL1 = 0x2C4


class _DKLP_PCS_GLUE_TX_DPCNTL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Vswing_Control_Tx2', ctypes.c_uint32, 3),
        ('Cfg_Cursor_Control_Tx2', ctypes.c_uint32, 5),
        ('Cfg_De_Emphasis_Control_L0_Tx2', ctypes.c_uint32, 5),
        ('Cfg_Preshoot_Control_L0_Tx2', ctypes.c_uint32, 5),
        ('Cfg_Shunt_Cp_Tx2', ctypes.c_uint32, 5),
        ('Cfg_Shunt_Cm_Tx2', ctypes.c_uint32, 5),
        ('Cfg_Slow_Trim_Enable_Tx2', ctypes.c_uint32, 1),
        ('Cfg_Pipe_Select_Tx2', ctypes.c_uint32, 1),
        ('Cfg_Trainingen_Tx2', ctypes.c_uint32, 1),
        ('Cfg_Reserved_Tx2', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PCS_GLUE_TX_DPCNTL1(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Vswing_Control_Tx2 = 0  # bit 0 to 3
    Cfg_Cursor_Control_Tx2 = 0  # bit 3 to 8
    Cfg_De_Emphasis_Control_L0_Tx2 = 0  # bit 8 to 13
    Cfg_Preshoot_Control_L0_Tx2 = 0  # bit 13 to 18
    Cfg_Shunt_Cp_Tx2 = 0  # bit 18 to 23
    Cfg_Shunt_Cm_Tx2 = 0  # bit 23 to 28
    Cfg_Slow_Trim_Enable_Tx2 = 0  # bit 28 to 29
    Cfg_Pipe_Select_Tx2 = 0  # bit 29 to 30
    Cfg_Trainingen_Tx2 = 0  # bit 30 to 31
    Cfg_Reserved_Tx2 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PCS_GLUE_TX_DPCNTL1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PCS_GLUE_TX_DPCNTL1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_RATE8BOVERRIDE(Enum):
    CFG_RATE8BOVERRIDE_CFG_RATE8BOVERRIDE_DEFAULTRESET = 0x0


class ENUM_CFG_RATE8BOVERRIDE_ENABLE(Enum):
    CFG_RATE8BOVERRIDE_ENABLE_CFG_RATE8BOVERRIDE_ENABLE_DEFAULTRESET = 0x0


class ENUM_CFG_DP20BITMODE(Enum):
    CFG_DP20BITMODE_CFG_DP20BITMODE_DEFAULTRESET = 0x0


class ENUM_CFG_LOADGENSELECT_TX1(Enum):
    CFG_LOADGENSELECT_TX1_CFG_LOADGENSELECT_TX1_DEFAULTRESET = 0x0


class ENUM_CFG_LOADGENSELECT_TX2(Enum):
    CFG_LOADGENSELECT_TX2_CFG_LOADGENSELECT_TX2_DEFAULTRESET = 0x0


class ENUM_CFG_DP_2UI_4UI_MODE_EN(Enum):
    CFG_DP_2UI_4UI_MODE_EN_CFG_DP_2UI_4UI_MODE_EN_DEFAULTRESET = 0x0


class ENUM_CFG_DP_FIFO_DEPTH_TX2(Enum):
    CFG_DP_FIFO_DEPTH_TX2_CFG_DP_FIFO_DEPTH_TX2_DEFAULTRESET = 0x0


class ENUM_CFG_DP_FIFO_DEPTH_TX1(Enum):
    CFG_DP_FIFO_DEPTH_TX1_CFG_DP_FIFO_DEPTH_TX1_DEFAULTRESET = 0x0


class ENUM_USB3_GEN1_2UI_MODE_EN(Enum):
    USB3_GEN1_2UI_MODE_EN_ENABLE = 0x1
    USB3_GEN1_2UI_MODE_EN_DISABLE = 0x0


class ENUM_CFG_DP_MODE_CG_ENABLE(Enum):
    CFG_DP_MODE_CG_ENABLE = 0x1
    CFG_DP_MODE_CG_DISABLE = 0x0


class ENUM_LOADGEN_SHARING_PMD_DISABLE(Enum):
    LOADGEN_SHARING_PMD_DISABLE = 0x0
    LOADGEN_SHARING_PMD_ENABLE = 0x1


class ENUM_CFG_RESERVED_DP3(Enum):
    CFG_RESERVED_DP3_CFG_RESERVED_DP3_DEFAULTRESET = 0x0


class OFFSET_DKLP_PCS_GLUE_TX_DPCNTL2:
    DKLP_PCS_GLUE_TX_DPCNTL2 = 0x2C8


class _DKLP_PCS_GLUE_TX_DPCNTL2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Rate8Boverride', ctypes.c_uint32, 1),
        ('Cfg_Rate8Boverride_Enable', ctypes.c_uint32, 1),
        ('Cfg_Dp20Bitmode', ctypes.c_uint32, 1),
        ('Cfg_Loadgenselect_Tx1', ctypes.c_uint32, 2),
        ('Cfg_Loadgenselect_Tx2', ctypes.c_uint32, 2),
        ('Cfg_Dp_2Ui_4Ui_Mode_En', ctypes.c_uint32, 1),
        ('Cfg_Dp_Fifo_Depth_Tx2', ctypes.c_uint32, 1),
        ('Cfg_Dp_Fifo_Depth_Tx1', ctypes.c_uint32, 1),
        ('Usb3_Gen1_2Ui_Mode_En', ctypes.c_uint32, 1),
        ('Cfg_Dp_Mode_Cg_Enable', ctypes.c_uint32, 1),
        ('Loadgen_Sharing_Pmd_Disable', ctypes.c_uint32, 1),
        ('Cfg_Reserved_Dp3', ctypes.c_uint32, 19),
    ]


class REG_DKLP_PCS_GLUE_TX_DPCNTL2(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Rate8Boverride = 0  # bit 0 to 1
    Cfg_Rate8Boverride_Enable = 0  # bit 1 to 2
    Cfg_Dp20Bitmode = 0  # bit 2 to 3
    Cfg_Loadgenselect_Tx1 = 0  # bit 3 to 5
    Cfg_Loadgenselect_Tx2 = 0  # bit 5 to 7
    Cfg_Dp_2Ui_4Ui_Mode_En = 0  # bit 7 to 8
    Cfg_Dp_Fifo_Depth_Tx2 = 0  # bit 8 to 9
    Cfg_Dp_Fifo_Depth_Tx1 = 0  # bit 9 to 10
    Usb3_Gen1_2Ui_Mode_En = 0  # bit 10 to 11
    Cfg_Dp_Mode_Cg_Enable = 0  # bit 11 to 12
    Loadgen_Sharing_Pmd_Disable = 0  # bit 12 to 13
    Cfg_Reserved_Dp3 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PCS_GLUE_TX_DPCNTL2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PCS_GLUE_TX_DPCNTL2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_XTENSA_OK4_CG(Enum):
    CFG_XTENSA_OK4_CG_CFG_XTENSA_OK4_CG_DEFAULTRESET = 0x0


class ENUM_CFG_XTENSA_OK4_PLL_DISABLE(Enum):
    CFG_XTENSA_OK4_PLL_DISABLE_CFG_XTENSA_OK4_PLL_DISABLE_DEFAULTRESET = 0x0


class ENUM_CFG_ANASAVE_AT_PM_REQ(Enum):
    CFG_ANASAVE_AT_PM_REQ_CFG_ANASAVE_AT_PM_REQ_DEFAULTRESET = 0x1


class ENUM_CFG_XTENSA_INT_RESTORE_DONE(Enum):
    CFG_XTENSA_INT_RESTORE_DONE_CFG_XTENSA_INT_RESTORE_DONE_DEFAULTRESET = 0x0


class ENUM_CFG_XTENSA_PHY_CLK_SWITCH_ACK(Enum):
    CFG_XTENSA_PHY_CLK_SWITCH_ACK_CFG_XTENSA_PHY_CLK_SWITCH_ACK_DEFAULTRESET = 0x0


class ENUM_CFG_XTENSA_PHY_CL_COREWELL_PG_OK(Enum):
    CFG_XTENSA_PHY_CL_COREWELL_PG_OK_CFG_XTENSA_PHY_CL_COREWELL_PG_OK_DEFAULTRESET = 0x1


class ENUM_CFG_XTENSA_PHY_PLLCLK_CHANGE_ACK(Enum):
    CFG_XTENSA_PHY_PLLCLK_CHANGE_ACK_CFG_XTENSA_PHY_PLLCLK_CHANGE_ACK_DEFAULTRESET = 0x0


class ENUM_CFG_XTENSA_PHY_SB_TRIGGER_REQ(Enum):
    CFG_XTENSA_PHY_SB_TRIGGER_REQ_CFG_XTENSA_PHY_SB_TRIGGER_REQ_DEFAULTRESET = 0x0


class ENUM_CFG_XTENSA_PHY_BLOCK_ACK(Enum):
    CFG_XTENSA_PHY_BLOCK_ACK_CFG_XTENSA_PHY_BLOCK_ACK_DEFAULTRESET = 0x1


class ENUM_CFG_XTENSA_PHY_SEND_BLOCK_NAK(Enum):
    CFG_XTENSA_PHY_SEND_BLOCK_NAK_CFG_XTENSA_PHY_SEND_BLOCK_NAK_DEFAULTRESET = 0x0


class ENUM_CFG_XCLKGATEDSTAT_CLR(Enum):
    CFG_XCLKGATEDSTAT_CLR_CFG_XCLKGATEDSTAT_CLR_DEFAULTRESET = 0x0


class ENUM_CFG_FORCEPWRPOK_ACK(Enum):
    CFG_FORCEPWRPOK_ACK_CFG_FORCEPWRPOK_ACK_DEFAULTRESET = 0x0


class ENUM_CFG_RESEVERD_DW27_1(Enum):
    CFG_RESEVERD_DW27_1_CFG_RESEVERD_DW27_1_DEFAULTRESET = 0x0


class ENUM_CFG_UC_HEALTH(Enum):
    CFG_UC_HEALTH_CFG_UC_HEALTH_DEFAULTRESET = 0x0


class ENUM_CFG_TRIGGER_XTENSA_TO_START_RESTORE(Enum):
    CFG_TRIGGER_XTENSA_TO_START_RESTORE_CFG_TRIGGER_XTENSA_TO_START_RESTORE_DEFAULTRESET = 0x1


class ENUM_CFG_PHY_XTENSA_CLK_SWITCH_REQ(Enum):
    CFG_PHY_XTENSA_CLK_SWITCH_REQ_CFG_PHY_XTENSA_CLK_SWITCH_REQ_DEFAULTRESET = 0x0


class ENUM_CFG_PHY_XTENSA_SB_TRIGGER_ACK(Enum):
    CFG_PHY_XTENSA_SB_TRIGGER_ACK_CFG_PHY_XTENSA_SB_TRIGGER_ACK_DEFAULTRESET = 0x0


class ENUM_CFG_PHY_XTENSA_CL_COREWELL_WAKE(Enum):
    CFG_PHY_XTENSA_CL_COREWELL_WAKE_CFG_PHY_XTENSA_CL_COREWELL_WAKE_DEFAULTRESET = 0x0


class ENUM_CFG_PHY_XTENSA_BLOCK_REQ(Enum):
    CFG_PHY_XTENSA_BLOCK_REQ_CFG_PHY_XTENSA_BLOCK_REQ_DEFAULTRESET = 0x0


class ENUM_CFG_PHY_XTENSA_PLLCLK_CHANGE_REQ(Enum):
    CFG_PHY_XTENSA_PLLCLK_CHANGE_REQ_CFG_PHY_XTENSA_PLLCLK_CHANGE_REQ_DEFAULTRESET = 0x0


class ENUM_CFG_PHY_XTENSA_ANA_SAVE_DONE(Enum):
    CFG_PHY_XTENSA_ANA_SAVE_DONE_CFG_PHY_XTENSA_ANA_SAVE_DONE_DEFAULTRESET = 0x0


class ENUM_CFG_UC_XCLKGATEDSTAT(Enum):
    CFG_UC_XCLKGATEDSTAT_CFG_UC_XCLKGATEDSTAT_DEFAULTRESET = 0x0


class ENUM_CFG_PHY_XTENSA_UNBLOCK_REQ(Enum):
    CFG_PHY_XTENSA_UNBLOCK_REQ_CFG_PHY_XTENSA_UNBLOCK_REQ_DEFAULTRESET = 0x0


class ENUM_CFG_PHY_XTENSA_UNBLOCK_ACK(Enum):
    CFG_PHY_XTENSA_UNBLOCK_ACK_CFG_PHY_XTENSA_UNBLOCK_ACK_DEFAULTRESET = 0x0


class ENUM_CFG_PHY_XTENSA_ANA_RESTORE_DONE(Enum):
    CFG_PHY_XTENSA_ANA_RESTORE_DONE_CFG_PHY_XTENSA_ANA_RESTORE_DONE_DEFAULTRESET = 0x0


class ENUM_CFG_FORCEPWRPOK_REQ(Enum):
    CFG_FORCEPWRPOK_REQ_CFG_FORCEPWRPOK_REQ_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED_DW27_2(Enum):
    CFG_RESERVED_DW27_2_CFG_RESERVED_DW27_2_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_UC_CMN_UC_DWORD27:
    DKLP_CMN_UC_CMN_UC_DWORD27 = 0x36C


class _DKLP_CMN_UC_CMN_UC_DWORD27(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Xtensa_Ok4_Cg', ctypes.c_uint32, 1),
        ('Cfg_Xtensa_Ok4_Pll_Disable', ctypes.c_uint32, 1),
        ('Cfg_Anasave_At_Pm_Req', ctypes.c_uint32, 1),
        ('Cfg_Xtensa_Int_Restore_Done', ctypes.c_uint32, 1),
        ('Cfg_Xtensa_Phy_Clk_Switch_Ack', ctypes.c_uint32, 1),
        ('Cfg_Xtensa_Phy_Cl_Corewell_Pg_Ok', ctypes.c_uint32, 1),
        ('Cfg_Xtensa_Phy_Pllclk_Change_Ack', ctypes.c_uint32, 2),
        ('Cfg_Xtensa_Phy_Sb_Trigger_Req', ctypes.c_uint32, 1),
        ('Cfg_Xtensa_Phy_Block_Ack', ctypes.c_uint32, 1),
        ('Cfg_Xtensa_Phy_Send_Block_Nak', ctypes.c_uint32, 1),
        ('Cfg_Xclkgatedstat_Clr', ctypes.c_uint32, 1),
        ('Cfg_Forcepwrpok_Ack', ctypes.c_uint32, 1),
        ('Cfg_Reseverd_Dw27_1', ctypes.c_uint32, 2),
        ('Cfg_Uc_Health', ctypes.c_uint32, 1),
        ('Cfg_Trigger_Xtensa_To_Start_Restore', ctypes.c_uint32, 1),
        ('Cfg_Phy_Xtensa_Clk_Switch_Req', ctypes.c_uint32, 1),
        ('Cfg_Phy_Xtensa_Sb_Trigger_Ack', ctypes.c_uint32, 1),
        ('Cfg_Phy_Xtensa_Cl_Corewell_Wake', ctypes.c_uint32, 1),
        ('Cfg_Phy_Xtensa_Block_Req', ctypes.c_uint32, 1),
        ('Cfg_Phy_Xtensa_Pllclk_Change_Req', ctypes.c_uint32, 2),
        ('Cfg_Phy_Xtensa_Ana_Save_Done', ctypes.c_uint32, 1),
        ('Cfg_Uc_Xclkgatedstat', ctypes.c_uint32, 1),
        ('Cfg_Phy_Xtensa_Unblock_Req', ctypes.c_uint32, 1),
        ('Cfg_Phy_Xtensa_Unblock_Ack', ctypes.c_uint32, 1),
        ('Cfg_Phy_Xtensa_Ana_Restore_Done', ctypes.c_uint32, 1),
        ('Cfg_Forcepwrpok_Req', ctypes.c_uint32, 1),
        ('Cfg_Reserved_Dw27_2', ctypes.c_uint32, 3),
    ]


class REG_DKLP_CMN_UC_CMN_UC_DWORD27(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Xtensa_Ok4_Cg = 0  # bit 0 to 1
    Cfg_Xtensa_Ok4_Pll_Disable = 0  # bit 1 to 2
    Cfg_Anasave_At_Pm_Req = 0  # bit 2 to 3
    Cfg_Xtensa_Int_Restore_Done = 0  # bit 3 to 4
    Cfg_Xtensa_Phy_Clk_Switch_Ack = 0  # bit 4 to 5
    Cfg_Xtensa_Phy_Cl_Corewell_Pg_Ok = 0  # bit 5 to 6
    Cfg_Xtensa_Phy_Pllclk_Change_Ack = 0  # bit 6 to 8
    Cfg_Xtensa_Phy_Sb_Trigger_Req = 0  # bit 8 to 9
    Cfg_Xtensa_Phy_Block_Ack = 0  # bit 9 to 10
    Cfg_Xtensa_Phy_Send_Block_Nak = 0  # bit 10 to 11
    Cfg_Xclkgatedstat_Clr = 0  # bit 11 to 12
    Cfg_Forcepwrpok_Ack = 0  # bit 12 to 13
    Cfg_Reseverd_Dw27_1 = 0  # bit 13 to 15
    Cfg_Uc_Health = 0  # bit 15 to 16
    Cfg_Trigger_Xtensa_To_Start_Restore = 0  # bit 16 to 17
    Cfg_Phy_Xtensa_Clk_Switch_Req = 0  # bit 17 to 18
    Cfg_Phy_Xtensa_Sb_Trigger_Ack = 0  # bit 18 to 19
    Cfg_Phy_Xtensa_Cl_Corewell_Wake = 0  # bit 19 to 20
    Cfg_Phy_Xtensa_Block_Req = 0  # bit 20 to 21
    Cfg_Phy_Xtensa_Pllclk_Change_Req = 0  # bit 21 to 23
    Cfg_Phy_Xtensa_Ana_Save_Done = 0  # bit 23 to 24
    Cfg_Uc_Xclkgatedstat = 0  # bit 24 to 25
    Cfg_Phy_Xtensa_Unblock_Req = 0  # bit 25 to 26
    Cfg_Phy_Xtensa_Unblock_Ack = 0  # bit 26 to 27
    Cfg_Phy_Xtensa_Ana_Restore_Done = 0  # bit 27 to 28
    Cfg_Forcepwrpok_Req = 0  # bit 28 to 29
    Cfg_Reserved_Dw27_2 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_UC_CMN_UC_DWORD27),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_UC_CMN_UC_DWORD27, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_CFG_SUSPWR_GATING_CTRL(Enum):
    CFG_CFG_SUSPWR_GATING_CTRL_CFG_CFG_SUSPWR_GATING_CTRL_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_GAONPWR_GATING_CTRL(Enum):
    CFG_CFG_GAONPWR_GATING_CTRL_CFG_CFG_GAONPWR_GATING_CTRL_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_DIGPWR_GATING_CTRL(Enum):
    CFG_CFG_DIGPWR_GATING_CTRL_CFG_CFG_DIGPWR_GATING_CTRL_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_CLNPWR_GATING_CTRL(Enum):
    CFG_CFG_CLNPWR_GATING_CTRL_CFG_CFG_CLNPWR_GATING_CTRL_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_TRPWR_GATING_CTRL(Enum):
    CFG_CFG_TRPWR_GATING_CTRL_CFG_CFG_TRPWR_GATING_CTRL_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_TR2PWR_GATING_CTRL(Enum):
    CFG_CFG_TR2PWR_GATING_CTRL_CFG_CFG_TR2PWR_GATING_CTRL_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_DP_X1_MODE(Enum):
    CFG_CFG_DP_X1_MODE_CFG_CFG_DP_X1_MODE_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_DP_X2_MODE(Enum):
    CFG_CFG_DP_X2_MODE_CFG_CFG_DP_X2_MODE_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_RAWPWR_GATING_CTRL(Enum):
    CFG_CFG_RAWPWR_GATING_CTRL_CFG_CFG_RAWPWR_GATING_CTRL_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_DIGPWR_REQ_OVERRIDE(Enum):
    CFG_CFG_DIGPWR_REQ_OVERRIDE_CFG_CFG_DIGPWR_REQ_OVERRIDE_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_RAWPWR_REQ_OVERRIDE(Enum):
    CFG_CFG_RAWPWR_REQ_OVERRIDE_CFG_CFG_RAWPWR_REQ_OVERRIDE_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_SUSCLK_GATING_CTRL(Enum):
    CFG_CFG_SUSCLK_GATING_CTRL_CFG_CFG_SUSCLK_GATING_CTRL_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_LANECLKREQ_GATING_CTRL(Enum):
    CFG_CFG_LANECLKREQ_GATING_CTRL_CFG_CFG_LANECLKREQ_GATING_CTRL_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_LANECLKREQ_FORCE(Enum):
    CFG_CFG_LANECLKREQ_FORCE_CFG_CFG_LANECLKREQ_FORCE_DEFAULTRESET = 0x1


class ENUM_CFG_CFG_CRI_DIGPWR_REQ(Enum):
    CFG_CFG_CRI_DIGPWR_REQ_CFG_CFG_CRI_DIGPWR_REQ_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_COREPWR_ACK_WITH_PCS_PWRREQ(Enum):
    CFG_CFG_COREPWR_ACK_WITH_PCS_PWRREQ_CFG_CFG_COREPWR_ACK_WITH_PCS_PWRREQ_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_LDO_POWERUP_TIMER_8(Enum):
    CFG_CFG_LDO_POWERUP_TIMER_8_CFG_CFG_LDO_POWERUP_TIMER_8_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_VR_PULLDWN2GND_TR(Enum):
    CFG_CFG_VR_PULLDWN2GND_TR_CFG_CFG_VR_PULLDWN2GND_TR_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_VR_PULLDWN2GND_TR2(Enum):
    CFG_CFG_VR_PULLDWN2GND_TR2_CFG_CFG_VR_PULLDWN2GND_TR2_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_CRIREG_COLD_BOOT_DONE(Enum):
    CFG_CFG_CRIREG_COLD_BOOT_DONE_CFG_CFG_CRIREG_COLD_BOOT_DONE_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_DIG_PWRGATE_TIMER_BYPASS(Enum):
    CFG_CFG_DIG_PWRGATE_TIMER_BYPASS_CFG_CFG_DIG_PWRGATE_TIMER_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_CL_PWRGATE_TIMER_BYPASS(Enum):
    CFG_CFG_CL_PWRGATE_TIMER_BYPASS_CFG_CFG_CL_PWRGATE_TIMER_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_TR_PWRGATE_TIMER_BYPASS(Enum):
    CFG_CFG_TR_PWRGATE_TIMER_BYPASS_CFG_CFG_TR_PWRGATE_TIMER_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_CFG_TR2_PWRGATE_TIMER_BYPASS(Enum):
    CFG_CFG_TR2_PWRGATE_TIMER_BYPASS_CFG_CFG_TR2_PWRGATE_TIMER_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_LDO_POWERUP_TIMER(Enum):
    CFG_LDO_POWERUP_TIMER_CFG_LDO_POWERUP_TIMER_DEFAULTRESET = 0x2


class OFFSET_DKLP_ACU_ACU_DWORD8:
    DKLP_ACU_ACU_DWORD8 = 0x0A0


class _DKLP_ACU_ACU_DWORD8(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Cfg_Suspwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Gaonpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Digpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Clnpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Trpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Tr2Pwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Dp_X1_Mode', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Dp_X2_Mode', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Rawpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Digpwr_Req_Override', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Rawpwr_Req_Override', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Susclk_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Laneclkreq_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Laneclkreq_Force', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Cri_Digpwr_Req', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Corepwr_Ack_With_Pcs_Pwrreq', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Ldo_Powerup_Timer_8', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Vr_Pulldwn2Gnd_Tr', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Vr_Pulldwn2Gnd_Tr2', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Crireg_Cold_Boot_Done', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Dig_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Cl_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Tr_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Cfg_Tr2_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Ldo_Powerup_Timer', ctypes.c_uint32, 8),
    ]


class REG_DKLP_ACU_ACU_DWORD8(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Cfg_Suspwr_Gating_Ctrl = 0  # bit 0 to 1
    Cfg_Cfg_Gaonpwr_Gating_Ctrl = 0  # bit 1 to 2
    Cfg_Cfg_Digpwr_Gating_Ctrl = 0  # bit 2 to 3
    Cfg_Cfg_Clnpwr_Gating_Ctrl = 0  # bit 3 to 4
    Cfg_Cfg_Trpwr_Gating_Ctrl = 0  # bit 4 to 5
    Cfg_Cfg_Tr2Pwr_Gating_Ctrl = 0  # bit 5 to 6
    Cfg_Cfg_Dp_X1_Mode = 0  # bit 6 to 7
    Cfg_Cfg_Dp_X2_Mode = 0  # bit 7 to 8
    Cfg_Cfg_Rawpwr_Gating_Ctrl = 0  # bit 8 to 9
    Cfg_Cfg_Digpwr_Req_Override = 0  # bit 9 to 10
    Cfg_Cfg_Rawpwr_Req_Override = 0  # bit 10 to 11
    Cfg_Cfg_Susclk_Gating_Ctrl = 0  # bit 11 to 12
    Cfg_Cfg_Laneclkreq_Gating_Ctrl = 0  # bit 12 to 13
    Cfg_Cfg_Laneclkreq_Force = 0  # bit 13 to 14
    Cfg_Cfg_Cri_Digpwr_Req = 0  # bit 14 to 15
    Cfg_Cfg_Corepwr_Ack_With_Pcs_Pwrreq = 0  # bit 15 to 16
    Cfg_Cfg_Ldo_Powerup_Timer_8 = 0  # bit 16 to 17
    Cfg_Cfg_Vr_Pulldwn2Gnd_Tr = 0  # bit 17 to 18
    Cfg_Cfg_Vr_Pulldwn2Gnd_Tr2 = 0  # bit 18 to 19
    Cfg_Cfg_Crireg_Cold_Boot_Done = 0  # bit 19 to 20
    Cfg_Cfg_Dig_Pwrgate_Timer_Bypass = 0  # bit 20 to 21
    Cfg_Cfg_Cl_Pwrgate_Timer_Bypass = 0  # bit 21 to 22
    Cfg_Cfg_Tr_Pwrgate_Timer_Bypass = 0  # bit 22 to 23
    Cfg_Cfg_Tr2_Pwrgate_Timer_Bypass = 0  # bit 23 to 24
    Cfg_Ldo_Powerup_Timer = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_ACU_ACU_DWORD8),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_ACU_ACU_DWORD8, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

