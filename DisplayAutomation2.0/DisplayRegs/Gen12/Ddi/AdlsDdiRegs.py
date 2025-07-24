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
# @file AdlsDdiRegs.py
# @brief contains AdlsDdiRegs.py related register definitions

import ctypes
from enum import Enum


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
    PORT_COMP_DW0_D = 0x161100
    PORT_COMP_DW0_A = 0x162100
    PORT_COMP_DW0_E = 0x16B100


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
    PORT_COMP_DW1_D = 0x161104
    PORT_COMP_DW1_A = 0x162104
    PORT_COMP_DW1_E = 0x16B104


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
    PORT_COMP_DW3_D = 0x16110C
    PORT_COMP_DW3_A = 0x16210C
    PORT_COMP_DW3_E = 0x16B10C


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
    PORT_COMP_DW8_D = 0x161120
    PORT_COMP_DW8_A = 0x162120
    PORT_COMP_DW8_E = 0x16B120


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
    PORT_COMP_DW9_D = 0x161124
    PORT_COMP_DW9_A = 0x162124
    PORT_COMP_DW9_E = 0x16B124


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
    PORT_COMP_DW10_D = 0x161128
    PORT_COMP_DW10_A = 0x162128
    PORT_COMP_DW10_E = 0x16B128


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
    PORT_CL_DW5_D = 0x161014
    PORT_CL_DW5_A = 0x162014
    PORT_CL_DW5_E = 0x16B014


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
    PORT_CL_DW10_D = 0x161028
    PORT_CL_DW10_A = 0x162028
    PORT_CL_DW10_E = 0x16B028


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
    PORT_CL_DW12_D = 0x161030
    PORT_CL_DW12_A = 0x162030
    PORT_CL_DW12_E = 0x16B030


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
    PORT_CL_DW15_D = 0x16103C
    PORT_CL_DW15_A = 0x16203C
    PORT_CL_DW15_E = 0x16B03C


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


class OFFSET_PORT_CL_DW16:
    PORT_CL_DW16_B = 0x6C040
    PORT_CL_DW16_C = 0x160040
    PORT_CL_DW16_D = 0x161040
    PORT_CL_DW16_A = 0x162040
    PORT_CL_DW16_E = 0x16B040


class _PORT_CL_DW16(ctypes.LittleEndianStructure):
    _fields_ = [
        ('O_Cri_Wake_Ovrden', ctypes.c_uint32, 1),
        ('O_Cri_Wake_Ovrd', ctypes.c_uint32, 1),
        ('O_Comp_Pwrdown_Ovrden', ctypes.c_uint32, 1),
        ('O_Comp_Pwrdown_Ovrd', ctypes.c_uint32, 1),
        ('Ospare_Cri30', ctypes.c_uint32, 4),
        ('Reserved8', ctypes.c_uint32, 2),
        ('O_Hd_Ddid_Sel_Ovrd', ctypes.c_uint32, 1),
        ('O_Hd_Ddid_Sel_Ovrden', ctypes.c_uint32, 1),
        ('O_Hd_Ddic_Sel_Ovrd', ctypes.c_uint32, 1),
        ('O_Hd_Ddic_Sel_Ovrden', ctypes.c_uint32, 1),
        ('O_Hd_Ddib_Sel_Ovrd', ctypes.c_uint32, 1),
        ('O_Hd_Ddib_Sel_Ovrden', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_PORT_CL_DW16(ctypes.Union):
    value = 0
    offset = 0

    O_Cri_Wake_Ovrden = 0  # bit 0 to 1
    O_Cri_Wake_Ovrd = 0  # bit 1 to 2
    O_Comp_Pwrdown_Ovrden = 0  # bit 2 to 3
    O_Comp_Pwrdown_Ovrd = 0  # bit 3 to 4
    Ospare_Cri30 = 0  # bit 4 to 8
    Reserved8 = 0  # bit 8 to 10
    O_Hd_Ddid_Sel_Ovrd = 0  # bit 10 to 11
    O_Hd_Ddid_Sel_Ovrden = 0  # bit 11 to 12
    O_Hd_Ddic_Sel_Ovrd = 0  # bit 12 to 13
    O_Hd_Ddic_Sel_Ovrden = 0  # bit 13 to 14
    O_Hd_Ddib_Sel_Ovrd = 0  # bit 14 to 15
    O_Hd_Ddib_Sel_Ovrden = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CL_DW16),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CL_DW16, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_TX_DW1:
    PORT_TX_DW1_AUX_B = 0x6C384
    PORT_TX_DW1_GRP_B = 0x6C684
    PORT_TX_DW1_LN0_B = 0x6C884
    PORT_TX_DW1_LN1_B = 0x6C984
    PORT_TX_DW1_LN2_B = 0x6CA84
    PORT_TX_DW1_LN3_B = 0x6CB84
    PORT_TX_DW1_AUX_C = 0x160384
    PORT_TX_DW1_GRP_C = 0x160684
    PORT_TX_DW1_LN0_C = 0x160884
    PORT_TX_DW1_LN1_C = 0x160984
    PORT_TX_DW1_LN2_C = 0x160A84
    PORT_TX_DW1_LN3_C = 0x160B84
    PORT_TX_DW1_AUX_D = 0x161384
    PORT_TX_DW1_GRP_D = 0x161684
    PORT_TX_DW1_LN0_D = 0x161884
    PORT_TX_DW1_LN1_D = 0x161984
    PORT_TX_DW1_LN2_D = 0x161A84
    PORT_TX_DW1_LN3_D = 0x161B84
    PORT_TX_DW1_AUX_A = 0x162384
    PORT_TX_DW1_GRP_A = 0x162684
    PORT_TX_DW1_LN0_A = 0x162884
    PORT_TX_DW1_LN1_A = 0x162984
    PORT_TX_DW1_LN2_A = 0x162A84
    PORT_TX_DW1_LN3_A = 0x162B84
    PORT_TX_DW1_AUX_E = 0x16B384
    PORT_TX_DW1_GRP_E = 0x16B684
    PORT_TX_DW1_LN0_E = 0x16B884
    PORT_TX_DW1_LN1_E = 0x16B984
    PORT_TX_DW1_LN2_E = 0x16BA84
    PORT_TX_DW1_LN3_E = 0x16BB84


class _PORT_TX_DW1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('O_Vref_Nom_En', ctypes.c_uint32, 1),
        ('O_Vref_Hi_En', ctypes.c_uint32, 1),
        ('O_Vref_Low_En', ctypes.c_uint32, 1),
        ('O_Tx_Slew_Ctrl', ctypes.c_uint32, 2),
        ('O_Iref_Ctrl', ctypes.c_uint32, 2),
        ('O_Iref_Config', ctypes.c_uint32, 1),
        ('Reserved8', ctypes.c_uint32, 24),
    ]


class REG_PORT_TX_DW1(ctypes.Union):
    value = 0
    offset = 0

    O_Vref_Nom_En = 0  # bit 0 to 1
    O_Vref_Hi_En = 0  # bit 1 to 2
    O_Vref_Low_En = 0  # bit 2 to 3
    O_Tx_Slew_Ctrl = 0  # bit 3 to 5
    O_Iref_Ctrl = 0  # bit 5 to 7
    O_Iref_Config = 0  # bit 7 to 8
    Reserved8 = 0  # bit 8 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW1, self).__init__()
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
    PORT_TX_DW2_AUX_D = 0x161388
    PORT_TX_DW2_GRP_D = 0x161688
    PORT_TX_DW2_LN0_D = 0x161888
    PORT_TX_DW2_LN1_D = 0x161988
    PORT_TX_DW2_LN2_D = 0x161A88
    PORT_TX_DW2_LN3_D = 0x161B88
    PORT_TX_DW2_AUX_A = 0x162388
    PORT_TX_DW2_GRP_A = 0x162688
    PORT_TX_DW2_LN0_A = 0x162888
    PORT_TX_DW2_LN1_A = 0x162988
    PORT_TX_DW2_LN2_A = 0x162A88
    PORT_TX_DW2_LN3_A = 0x162B88
    PORT_TX_DW2_AUX_E = 0x16B388
    PORT_TX_DW2_GRP_E = 0x16B688
    PORT_TX_DW2_LN0_E = 0x16B888
    PORT_TX_DW2_LN1_E = 0x16B988
    PORT_TX_DW2_LN2_E = 0x16BA88
    PORT_TX_DW2_LN3_E = 0x16BB88


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
    PORT_TX_DW4_AUX_D = 0x161390
    PORT_TX_DW4_GRP_D = 0x161690
    PORT_TX_DW4_LN0_D = 0x161890
    PORT_TX_DW4_LN1_D = 0x161990
    PORT_TX_DW4_LN2_D = 0x161A90
    PORT_TX_DW4_LN3_D = 0x161B90
    PORT_TX_DW4_AUX_A = 0x162390
    PORT_TX_DW4_GRP_A = 0x162690
    PORT_TX_DW4_LN0_A = 0x162890
    PORT_TX_DW4_LN1_A = 0x162990
    PORT_TX_DW4_LN2_A = 0x162A90
    PORT_TX_DW4_LN3_A = 0x162B90
    PORT_TX_DW4_AUX_E = 0x16B390
    PORT_TX_DW4_GRP_E = 0x16B690
    PORT_TX_DW4_LN0_E = 0x16B890
    PORT_TX_DW4_LN1_E = 0x16B990
    PORT_TX_DW4_LN2_E = 0x16BA90
    PORT_TX_DW4_LN3_E = 0x16BB90


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
    PORT_TX_DW5_AUX_D = 0x161394
    PORT_TX_DW5_GRP_D = 0x161694
    PORT_TX_DW5_LN0_D = 0x161894
    PORT_TX_DW5_LN1_D = 0x161994
    PORT_TX_DW5_LN2_D = 0x161A94
    PORT_TX_DW5_LN3_D = 0x161B94
    PORT_TX_DW5_AUX_A = 0x162394
    PORT_TX_DW5_GRP_A = 0x162694
    PORT_TX_DW5_LN0_A = 0x162894
    PORT_TX_DW5_LN1_A = 0x162994
    PORT_TX_DW5_LN2_A = 0x162A94
    PORT_TX_DW5_LN3_A = 0x162B94
    PORT_TX_DW5_AUX_E = 0x16B394
    PORT_TX_DW5_GRP_E = 0x16B694
    PORT_TX_DW5_LN0_E = 0x16B894
    PORT_TX_DW5_LN1_E = 0x16B994
    PORT_TX_DW5_LN2_E = 0x16BA94
    PORT_TX_DW5_LN3_E = 0x16BB94


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


class OFFSET_PORT_TX_DW6:
    PORT_TX_DW6_AUX_B = 0x6C398
    PORT_TX_DW6_GRP_B = 0x6C698
    PORT_TX_DW6_LN0_B = 0x6C898
    PORT_TX_DW6_LN1_B = 0x6C998
    PORT_TX_DW6_LN2_B = 0x6CA98
    PORT_TX_DW6_LN3_B = 0x6CB98
    PORT_TX_DW6_AUX_C = 0x160398
    PORT_TX_DW6_GRP_C = 0x160698
    PORT_TX_DW6_LN0_C = 0x160898
    PORT_TX_DW6_LN1_C = 0x160998
    PORT_TX_DW6_LN2_C = 0x160A98
    PORT_TX_DW6_LN3_C = 0x160B98
    PORT_TX_DW6_AUX_D = 0x161398
    PORT_TX_DW6_GRP_D = 0x161698
    PORT_TX_DW6_LN0_D = 0x161898
    PORT_TX_DW6_LN1_D = 0x161998
    PORT_TX_DW6_LN2_D = 0x161A98
    PORT_TX_DW6_LN3_D = 0x161B98
    PORT_TX_DW6_AUX_A = 0x162398
    PORT_TX_DW6_GRP_A = 0x162698
    PORT_TX_DW6_LN0_A = 0x162898
    PORT_TX_DW6_LN1_A = 0x162998
    PORT_TX_DW6_LN2_A = 0x162A98
    PORT_TX_DW6_LN3_A = 0x162B98
    PORT_TX_DW6_AUX_E = 0x16B398
    PORT_TX_DW6_GRP_E = 0x16B698
    PORT_TX_DW6_LN0_E = 0x16B898
    PORT_TX_DW6_LN1_E = 0x16B998
    PORT_TX_DW6_LN2_E = 0x16BA98
    PORT_TX_DW6_LN3_E = 0x16BB98


class _PORT_TX_DW6(ctypes.LittleEndianStructure):
    _fields_ = [
        ('O_Ldo_Bypass_Cri', ctypes.c_uint32, 1),
        ('O_Ldo_Ref_Sel_Cri', ctypes.c_uint32, 6),
        ('O_Func_Ovrd_En', ctypes.c_uint32, 1),
        ('Reserved8', ctypes.c_uint32, 24),
    ]


class REG_PORT_TX_DW6(ctypes.Union):
    value = 0
    offset = 0

    O_Ldo_Bypass_Cri = 0  # bit 0 to 1
    O_Ldo_Ref_Sel_Cri = 0  # bit 1 to 7
    O_Func_Ovrd_En = 0  # bit 7 to 8
    Reserved8 = 0  # bit 8 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW6),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW6, self).__init__()
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
    PORT_TX_DW7_AUX_D = 0x16139C
    PORT_TX_DW7_GRP_D = 0x16169C
    PORT_TX_DW7_LN0_D = 0x16189C
    PORT_TX_DW7_LN1_D = 0x16199C
    PORT_TX_DW7_LN2_D = 0x161A9C
    PORT_TX_DW7_LN3_D = 0x161B9C
    PORT_TX_DW7_AUX_A = 0x16239C
    PORT_TX_DW7_GRP_A = 0x16269C
    PORT_TX_DW7_LN0_A = 0x16289C
    PORT_TX_DW7_LN1_A = 0x16299C
    PORT_TX_DW7_LN2_A = 0x162A9C
    PORT_TX_DW7_LN3_A = 0x162B9C
    PORT_TX_DW7_AUX_E = 0x16B39C
    PORT_TX_DW7_GRP_E = 0x16B69C
    PORT_TX_DW7_LN0_E = 0x16B89C
    PORT_TX_DW7_LN1_E = 0x16B99C
    PORT_TX_DW7_LN2_E = 0x16BA9C
    PORT_TX_DW7_LN3_E = 0x16BB9C


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


class ENUM_ODCC_CLK_DIV_SEL(Enum):
    ODCC_CLK_DIV_SEL_DIV4 = 0x2
    ODCC_CLK_DIV_SEL_DIV8 = 0x3


class OFFSET_PORT_TX_DW8:
    PORT_TX_DW8_AUX_B = 0x6C3A0
    PORT_TX_DW8_GRP_B = 0x6C6A0
    PORT_TX_DW8_LN0_B = 0x6C8A0
    PORT_TX_DW8_LN1_B = 0x6C9A0
    PORT_TX_DW8_LN2_B = 0x6CAA0
    PORT_TX_DW8_LN3_B = 0x6CBA0
    PORT_TX_DW8_AUX_C = 0x1603A0
    PORT_TX_DW8_GRP_C = 0x1606A0
    PORT_TX_DW8_LN0_C = 0x1608A0
    PORT_TX_DW8_LN1_C = 0x1609A0
    PORT_TX_DW8_LN2_C = 0x160AA0
    PORT_TX_DW8_LN3_C = 0x160BA0
    PORT_TX_DW8_AUX_D = 0x1613A0
    PORT_TX_DW8_GRP_D = 0x1616A0
    PORT_TX_DW8_LN0_D = 0x1618A0
    PORT_TX_DW8_LN1_D = 0x1619A0
    PORT_TX_DW8_LN2_D = 0x161AA0
    PORT_TX_DW8_LN3_D = 0x161BA0
    PORT_TX_DW8_AUX_A = 0x1623A0
    PORT_TX_DW8_GRP_A = 0x1626A0
    PORT_TX_DW8_LN0_A = 0x1628A0
    PORT_TX_DW8_LN1_A = 0x1629A0
    PORT_TX_DW8_LN2_A = 0x162AA0
    PORT_TX_DW8_LN3_A = 0x162BA0
    PORT_TX_DW8_AUX_E = 0x16B3A0
    PORT_TX_DW8_GRP_E = 0x16B6A0
    PORT_TX_DW8_LN0_E = 0x16B8A0
    PORT_TX_DW8_LN1_E = 0x16B9A0
    PORT_TX_DW8_LN2_E = 0x16BAA0
    PORT_TX_DW8_LN3_E = 0x16BBA0


class _PORT_TX_DW8(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Odcc_Upper_Limit', ctypes.c_uint32, 5),
        ('Idcc_Code_Therm_2_0', ctypes.c_uint32, 3),
        ('Idcc_Code', ctypes.c_uint32, 5),
        ('Idcc_Code_Therm_4_3', ctypes.c_uint32, 2),
        ('Reserved15', ctypes.c_uint32, 1),
        ('Odcc_Lower_Limit', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 1),
        ('Odccfuse_En', ctypes.c_uint32, 1),
        ('Odcc_Code_Ovrd_En', ctypes.c_uint32, 1),
        ('Odcc_Code_Ovrd', ctypes.c_uint32, 5),
        ('Odcc_Clk_Div_Sel', ctypes.c_uint32, 2),
        ('Odcc_Clksel', ctypes.c_uint32, 1),
    ]


class REG_PORT_TX_DW8(ctypes.Union):
    value = 0
    offset = 0

    Odcc_Upper_Limit = 0  # bit 0 to 5
    Idcc_Code_Therm_2_0 = 0  # bit 5 to 8
    Idcc_Code = 0  # bit 8 to 13
    Idcc_Code_Therm_4_3 = 0  # bit 13 to 15
    Reserved15 = 0  # bit 15 to 16
    Odcc_Lower_Limit = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 22
    Odccfuse_En = 0  # bit 22 to 23
    Odcc_Code_Ovrd_En = 0  # bit 23 to 24
    Odcc_Code_Ovrd = 0  # bit 24 to 29
    Odcc_Clk_Div_Sel = 0  # bit 29 to 31
    Odcc_Clksel = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW8),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW8, self).__init__()
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
    PORT_PCS_DW1_AUX_D = 0x161304
    PORT_PCS_DW1_GRP_D = 0x161604
    PORT_PCS_DW1_LN0_D = 0x161804
    PORT_PCS_DW1_LN1_D = 0x161904
    PORT_PCS_DW1_LN2_D = 0x161A04
    PORT_PCS_DW1_LN3_D = 0x161B04
    PORT_PCS_DW1_AUX_A = 0x162304
    PORT_PCS_DW1_GRP_A = 0x162604
    PORT_PCS_DW1_LN0_A = 0x162804
    PORT_PCS_DW1_LN1_A = 0x162904
    PORT_PCS_DW1_LN2_A = 0x162A04
    PORT_PCS_DW1_LN3_A = 0x162B04
    PORT_PCS_DW1_AUX_E = 0x16B304
    PORT_PCS_DW1_GRP_E = 0x16B604
    PORT_PCS_DW1_LN0_E = 0x16B804
    PORT_PCS_DW1_LN1_E = 0x16B904
    PORT_PCS_DW1_LN2_E = 0x16BA04
    PORT_PCS_DW1_LN3_E = 0x16BB04


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
    PORT_PCS_DW9_AUX_D = 0x161324
    PORT_PCS_DW9_GRP_D = 0x161624
    PORT_PCS_DW9_LN0_D = 0x161824
    PORT_PCS_DW9_LN1_D = 0x161924
    PORT_PCS_DW9_LN2_D = 0x161A24
    PORT_PCS_DW9_LN3_D = 0x161B24
    PORT_PCS_DW9_AUX_A = 0x162324
    PORT_PCS_DW9_GRP_A = 0x162624
    PORT_PCS_DW9_LN0_A = 0x162824
    PORT_PCS_DW9_LN1_A = 0x162924
    PORT_PCS_DW9_LN2_A = 0x162A24
    PORT_PCS_DW9_LN3_A = 0x162B24
    PORT_PCS_DW9_AUX_E = 0x16B324
    PORT_PCS_DW9_GRP_E = 0x16B624
    PORT_PCS_DW9_LN0_E = 0x16B824
    PORT_PCS_DW9_LN1_E = 0x16B924
    PORT_PCS_DW9_LN2_E = 0x16BA24
    PORT_PCS_DW9_LN3_E = 0x16BB24


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

