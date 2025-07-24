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
# @file JslDdiRegs.py
# @brief contains JslDdiRegs.py related register definitions

import ctypes
from enum import Enum


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
    O_EDP4K2K_MODE_OVRD_VAL_EDP_4K_2K = 0x1
    O_EDP4K2K_MODE_OVRD_VAL_DP_MIPI_EDP_8K = 0x0


class ENUM_STATIC_POWER_DOWN(Enum):
    STATIC_POWER_DOWN_POWER_UP_ALL_LANES = 0x0  # Enable x4
    STATIC_POWER_DOWN_POWER_DOWN_LANES_3_2 = 0xC  # Enable x2
    STATIC_POWER_DOWN_POWER_DOWN_LANES_3_2_1 = 0xE  # Enable x1
    STATIC_POWER_DOWN_POWER_DOWN_LANES_1_0 = 0x3  # Enable x2 Reversed
    STATIC_POWER_DOWN_POWER_DOWN_LANES_2_1_0 = 0x7  # Enable x1 Reversed


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
        ('Spare3116', ctypes.c_uint32, 16),
    ]


class REG_PORT_TX_DW2(ctypes.Union):
    value = 0
    offset = 0

    RcompScalar = 0  # bit 0 to 8
    Frclatencyoptim = 0  # bit 8 to 11
    Swing_SelLower = 0  # bit 11 to 14
    Cmnmode_Sel = 0  # bit 14 to 15
    Swing_SelUpper = 0  # bit 15 to 16
    Spare3116 = 0  # bit 16 to 32

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
    PORT_PCS_DW1_AUX_C = 0x160304
    PORT_PCS_DW1_GRP_C = 0x160604
    PORT_PCS_DW1_LN0_C = 0x160804
    PORT_PCS_DW1_LN1_C = 0x160904
    PORT_PCS_DW1_LN2_C = 0x160A04
    PORT_PCS_DW1_LN3_C = 0x160B04
    PORT_PCS_DW1_AUX_A = 0x162304
    PORT_PCS_DW1_GRP_A = 0x162604
    PORT_PCS_DW1_LN0_A = 0x162804


class _PORT_PCS_DW1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Soft_Reset_N', ctypes.c_uint32, 1),
        ('Softreset_Enable', ctypes.c_uint32, 1),
        ('Latencyoptim', ctypes.c_uint32, 2),
        ('Txdeemp', ctypes.c_uint32, 1),
        ('Txfifo_Rst_Master_Ovrd', ctypes.c_uint32, 1),
        ('Txfifo_Rst_Master_Ovrden', ctypes.c_uint32, 1),
        ('Tbc_As_Symbclk', ctypes.c_uint32, 1),
        ('Clkreq', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 2),
        ('Txhigh', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 2),
        ('Dcc', ctypes.c_uint32, 6),
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
    Txfifo_Rst_Master_Ovrd = 0  # bit 5 to 6
    Txfifo_Rst_Master_Ovrden = 0  # bit 6 to 7
    Tbc_As_Symbclk = 0  # bit 7 to 8
    Clkreq = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 12
    Txhigh = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 16
    Dcc = 0  # bit 16 to 22
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
    PORT_PCS_DW9_AUX_C = 0x160324
    PORT_PCS_DW9_GRP_C = 0x160624
    PORT_PCS_DW9_LN0_C = 0x160824
    PORT_PCS_DW9_LN1_C = 0x160924
    PORT_PCS_DW9_LN2_C = 0x160A24
    PORT_PCS_DW9_LN3_C = 0x160B24
    PORT_PCS_DW9_AUX_A = 0x162324
    PORT_PCS_DW9_GRP_A = 0x162624
    PORT_PCS_DW9_LN0_A = 0x162824


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


class ENUM_ULPS_ACTIVE(Enum):
    ULPS_ACTIVE_LANES_ARE_NOT_IN_ULPS = 0x0
    ULPS_ACTIVE_LANES_ARE_IN_ULPS = 0x1


class ENUM_AFE_ULPS_OVERRIDE(Enum):
    AFE_ULPS_OVERRIDE_DSI_COMPLEX_SAMPLES_AFE_ULPS_ACTIVE = 0x0
    AFE_ULPS_OVERRIDE_DSI_COMPLEX_SAMPLES_ULPS_ACTIVE_FROM_THIS_REGISTER = 0x1


class ENUM_CLOCK_GATING_DISABLE(Enum):
    CLOCK_GATING_DISABLE_CLOCK_GATING_ENABLED = 0x0
    CLOCK_GATING_DISABLE_CLOCK_GATING_DISABLED = 0x1


class ENUM_AFE_LP_BYPASS(Enum):
    AFE_LP_BYPASS_AFE_LP_BYPASS_DISABLED = 0x0
    AFE_LP_BYPASS_AFE_LP_BYPASS_ENABLED = 0x1


class ENUM_LOCAL_BDT_SM_DISABLE(Enum):
    LOCAL_BDT_SM_DISABLE_LOCAL_BDT_SM_ENABLED = 0x0
    LOCAL_BDT_SM_DISABLE_LOCAL_BDT_SM_DISABLED = 0x1


class ENUM_DISABLE_HS_TRANSFER_ENABLE_PPI_SIGNALING(Enum):
    DISABLE_HS_TRANSFER_ENABLE_PPI_SIGNALING_ENABLED = 0x0
    DISABLE_HS_TRANSFER_ENABLE_PPI_SIGNALING_DISABLED = 0x1


class ENUM_AFE_OVER_PPI_STRAP(Enum):
    AFE_OVER_PPI_STRAP_PPI_SIGNALING_OVER_PPI = 0x0
    AFE_OVER_PPI_STRAP_AFE_SIGNALING_OVER_PPI = 0x1


class OFFSET_DPHY_CHKN_REG0:
    DPHY_CHKN_REG0_1 = 0x6C194
    DPHY_CHKN_REG0_0 = 0x162194


class _DPHY_CHKN_REG0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('UlpsActive', ctypes.c_uint32, 1),
        ('AfeUlpsOverride', ctypes.c_uint32, 1),
        ('ClockGatingDisable', ctypes.c_uint32, 1),
        ('AfeLpBypass', ctypes.c_uint32, 1),
        ('LocalBdtSmDisable', ctypes.c_uint32, 1),
        ('Spare5', ctypes.c_uint32, 1),
        ('DisableHsTransferEnablePpiSignaling', ctypes.c_uint32, 1),
        ('AfeOverPpiStrap', ctypes.c_uint32, 1),
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
        ('Spare30', ctypes.c_uint32, 1),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_DPHY_CHKN_REG0(ctypes.Union):
    value = 0
    offset = 0

    UlpsActive = 0  # bit 0 to 1
    AfeUlpsOverride = 0  # bit 1 to 2
    ClockGatingDisable = 0  # bit 2 to 3
    AfeLpBypass = 0  # bit 3 to 4
    LocalBdtSmDisable = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    DisableHsTransferEnablePpiSignaling = 0  # bit 6 to 7
    AfeOverPpiStrap = 0  # bit 7 to 8
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
    Spare30 = 0  # bit 30 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPHY_CHKN_REG0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPHY_CHKN_REG0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PHY_MISC:
    PHY_MISC_A = 0x64C00
    PHY_MISC_B = 0x64C04


class _PHY_MISC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 20),
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

    Reserved0 = 0  # bit 0 to 20
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

