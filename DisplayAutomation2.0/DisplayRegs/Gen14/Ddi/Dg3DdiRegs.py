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
# @file Dg3DdiRegs.py
# @brief contains Dg3DdiRegs.py related register definitions

import ctypes
from enum import Enum


class OFFSET_PHY_MISC:
    PHY_MISC_A = 0x64C00
    PHY_MISC_B = 0x64C04
    PHY_MISC_C = 0x64C08
    PHY_MISC_D = 0x64C0C
    PHY_MISC_TC1 = 0x64C14


class _PHY_MISC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 4),
        ('Dp_Tx3_Pstate', ctypes.c_uint32, 2),
        ('Dp_Tx2_Pstate', ctypes.c_uint32, 2),
        ('Dp_Tx1_Pstate', ctypes.c_uint32, 2),
        ('Dp_Tx0_Pstate', ctypes.c_uint32, 2),
        ('Reserved12', ctypes.c_uint32, 8),
        ('Spare20', ctypes.c_uint32, 1),
        ('Spare21', ctypes.c_uint32, 1),
        ('Dp_Tx1_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx0_Ack', ctypes.c_uint32, 1),
        ('IoToDeMisc', ctypes.c_uint32, 4),
        ('Dp_Tx3_Req', ctypes.c_uint32, 1),
        ('Dp_Tx2_Req', ctypes.c_uint32, 1),
        ('Dp_Tx1_Req', ctypes.c_uint32, 1),
        ('DeToIoMisc', ctypes.c_uint32, 4),
        ('Dp_Tx0_Req', ctypes.c_uint32, 1),
    ]


class REG_PHY_MISC(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 4
    Dp_Tx3_Pstate = 0  # bit 4 to 6
    Dp_Tx2_Pstate = 0  # bit 6 to 8
    Dp_Tx1_Pstate = 0  # bit 8 to 10
    Dp_Tx0_Pstate = 0  # bit 10 to 12
    Reserved12 = 0  # bit 12 to 20
    Spare20 = 0  # bit 20 to 21
    Spare21 = 0  # bit 21 to 22
    Dp_Tx1_Ack = 0  # bit 22 to 23
    Dp_Tx0_Ack = 0  # bit 23 to 24
    IoToDeMisc = 0  # bit 24 to 28
    Dp_Tx3_Req = 0  # bit 28 to 29
    Dp_Tx2_Req = 0  # bit 29 to 30
    Dp_Tx1_Req = 0  # bit 30 to 31
    DeToIoMisc = 0  # bit 28 to 32
    Dp_Tx0_Req = 0  # bit 31 to 32

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


class OFFSET_SNPS_PHY_TX_EQ:
    SNPS_PHY_TX_EQ_LN0_PORT_A = 0x168300
    SNPS_PHY_TX_EQ_LN1_PORT_A = 0x168310
    SNPS_PHY_TX_EQ_LN2_PORT_A = 0x168320
    SNPS_PHY_TX_EQ_LN3_PORT_A = 0x168330
    SNPS_PHY_TX_EQ_LN0_PORT_B = 0x169300
    SNPS_PHY_TX_EQ_LN1_PORT_B = 0x169310
    SNPS_PHY_TX_EQ_LN2_PORT_B = 0x169320
    SNPS_PHY_TX_EQ_LN3_PORT_B = 0x169330
    SNPS_PHY_TX_EQ_LN0_PORT_C = 0x16A300
    SNPS_PHY_TX_EQ_LN1_PORT_C = 0x16A310
    SNPS_PHY_TX_EQ_LN2_PORT_C = 0x16A320
    SNPS_PHY_TX_EQ_LN3_PORT_C = 0x16A330
    SNPS_PHY_TX_EQ_LN0_PORT_D = 0x16B300
    SNPS_PHY_TX_EQ_LN1_PORT_D = 0x16B310
    SNPS_PHY_TX_EQ_LN2_PORT_D = 0x16B320
    SNPS_PHY_TX_EQ_LN3_PORT_D = 0x16B330
    SNPS_PHY_TX_EQ_LN0_PORT_TC1 = 0x16C300
    SNPS_PHY_TX_EQ_LN1_PORT_TC1 = 0x16C310
    SNPS_PHY_TX_EQ_LN2_PORT_TC1 = 0x16C320
    SNPS_PHY_TX_EQ_LN3_PORT_TC1 = 0x16C330


class _SNPS_PHY_TX_EQ(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 2),
        ('Dp_Tx_Eq_Pre', ctypes.c_uint32, 6),
        ('Reserved8', ctypes.c_uint32, 2),
        ('Dp_Tx_Eq_Post', ctypes.c_uint32, 6),
        ('Reserved16', ctypes.c_uint32, 2),
        ('Dp_Tx_Eq_Main', ctypes.c_uint32, 6),
        ('Reserved24', ctypes.c_uint32, 7),
        ('Dp_Tx_Bypass_Eq_Calc', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_TX_EQ(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 2
    Dp_Tx_Eq_Pre = 0  # bit 2 to 8
    Reserved8 = 0  # bit 8 to 10
    Dp_Tx_Eq_Post = 0  # bit 10 to 16
    Reserved16 = 0  # bit 16 to 18
    Dp_Tx_Eq_Main = 0  # bit 18 to 24
    Reserved24 = 0  # bit 24 to 31
    Dp_Tx_Bypass_Eq_Calc = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_TX_EQ),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_TX_EQ, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DP_TX_WIDTH(Enum):
    DP_TX_WIDTH_8BIT = 0x0
    DP_TX_WIDTH_10BIT = 0x1
    DP_TX_WIDTH_16BIT = 0x2
    DP_TX_WIDTH_20BIT = 0x3


class ENUM_DP_TX_RATE(Enum):
    DP_TX_RATE_BAUD = 0x0
    DP_TX_RATE_BAUD_2 = 0x1
    DP_TX_RATE_BAUD_4 = 0x2


class OFFSET_SNPS_PHY_TX_REQ:
    SNPS_PHY_TX_REQ_PORT_A = 0x168200
    SNPS_PHY_TX_REQ_PORT_B = 0x169200
    SNPS_PHY_TX_REQ_PORT_C = 0x16A200
    SNPS_PHY_TX_REQ_PORT_D = 0x16B200
    SNPS_PHY_TX_REQ_PORT_TC1 = 0x16C200


class _SNPS_PHY_TX_REQ(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 2),
        ('Dp_Tx_Width', ctypes.c_uint32, 2),
        ('Reserved4', ctypes.c_uint32, 8),
        ('Dp_Tx3_Lpd', ctypes.c_uint32, 1),
        ('Dp_Tx2_Lpd', ctypes.c_uint32, 1),
        ('Dp_Tx1_Lpd', ctypes.c_uint32, 1),
        ('Dp_Tx0_Lpd', ctypes.c_uint32, 1),
        ('Dp_Tx_Rate', ctypes.c_uint32, 3),
        ('Reserved19', ctypes.c_uint32, 11),
        ('LaneDisablePowerStateInPsr', ctypes.c_uint32, 2),
    ]


class REG_SNPS_PHY_TX_REQ(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 2
    Dp_Tx_Width = 0  # bit 2 to 4
    Reserved4 = 0  # bit 4 to 12
    Dp_Tx3_Lpd = 0  # bit 12 to 13
    Dp_Tx2_Lpd = 0  # bit 13 to 14
    Dp_Tx1_Lpd = 0  # bit 14 to 15
    Dp_Tx0_Lpd = 0  # bit 15 to 16
    Dp_Tx_Rate = 0  # bit 16 to 19
    Reserved19 = 0  # bit 19 to 30
    LaneDisablePowerStateInPsr = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_TX_REQ),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_TX_REQ, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SNPS_PHY_TX_COMMON:
    SNPS_PHY_TX_COMMON_PORT_A = 0x168100
    SNPS_PHY_TX_COMMON_PORT_B = 0x169100
    SNPS_PHY_TX_COMMON_PORT_C = 0x16A100
    SNPS_PHY_TX_COMMON_PORT_D = 0x16B100
    SNPS_PHY_TX_COMMON_PORT_TC1 = 0x16C100


class _SNPS_PHY_TX_COMMON(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 26),
        ('Dp_Tx_Vregdrv_Byp', ctypes.c_uint32, 1),
        ('Dp_Tx_Term_Ctrl', ctypes.c_uint32, 3),
        ('Dp_Tx_Invert', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_TX_COMMON(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 26
    Dp_Tx_Vregdrv_Byp = 0  # bit 26 to 27
    Dp_Tx_Term_Ctrl = 0  # bit 27 to 30
    Dp_Tx_Invert = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_TX_COMMON),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_TX_COMMON, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DPALT_DP4(Enum):
    DPALT_DP4_2_LANES_ACCESSIBLE = 0x0
    DPALT_DP4_4_LANES_ACCESSIBLE = 0x1


class OFFSET_SNPS_PHY_TYPEC_STATUS:
    SNPS_PHY_TYPEC_STATUS_PORT_A = 0x168400
    SNPS_PHY_TYPEC_STATUS_PORT_B = 0x169400
    SNPS_PHY_TYPEC_STATUS_PORT_C = 0x16A400
    SNPS_PHY_TYPEC_STATUS_PORT_D = 0x16B400
    SNPS_PHY_TYPEC_STATUS_PORT_TC1 = 0x16C400


class _SNPS_PHY_TYPEC_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 28),
        ('Dpalt_Disable_Ack', ctypes.c_uint32, 1),
        ('Dpalt_Dp4', ctypes.c_uint32, 1),
        ('Dpalt_Disable_Ack_Status', ctypes.c_uint32, 1),
        ('Dpalt_DisableLiveStatus', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_TYPEC_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 28
    Dpalt_Disable_Ack = 0  # bit 28 to 29
    Dpalt_Dp4 = 0  # bit 29 to 30
    Dpalt_Disable_Ack_Status = 0  # bit 30 to 31
    Dpalt_DisableLiveStatus = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_TYPEC_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_TYPEC_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SB_CLOCK_OVERRIDE(Enum):
    SB_CLOCK_OVERRIDE_DO_NOT_OVERRIDE = 0x0  # SB clock shuts down when DE Shim is in idle state.
    SB_CLOCK_OVERRIDE_OVERRIDE = 0x1  # SB clock continues to run when DE Shim is in idle state.


class ENUM_PHYTX_CLOCKGATE_DISABLE(Enum):
    PHYTX_CLOCKGATE_DISABLE = 0x0  # Clock gating controlled by unit enabling logic.
    PHYTX_CLOCKGATE_ENABLE = 0x1  # Disable clock gating function.


class ENUM_DETX_CLOCKGATE_DISABLE(Enum):
    DETX_CLOCKGATE_DISABLE = 0x0  # Clock gating controlled by unit enabling logic.
    DETX_CLOCKGATE_ENABLE = 0x1  # Disable clock gating function.


class ENUM_CHASSIS_CLOCK_REQUEST_DURATION(Enum):
    CHASSIS_CLOCK_REQUEST_DURATION_13_CLOCKS = 0x9


class OFFSET_SNPS_PHY_CHKN:
    SNPS_PHY_CHKN_PORT_A = 0x168410
    SNPS_PHY_CHKN_PORT_B = 0x169410
    SNPS_PHY_CHKN_PORT_C = 0x16A410
    SNPS_PHY_CHKN_PORT_D = 0x16B410
    SNPS_PHY_CHKN_PORT_TC1 = 0x16C410


class _SNPS_PHY_CHKN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare0', ctypes.c_uint32, 1),
        ('Spare1', ctypes.c_uint32, 1),
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
        ('Spare12', ctypes.c_uint32, 1),
        ('Spare13', ctypes.c_uint32, 1),
        ('Spare14', ctypes.c_uint32, 1),
        ('Spare15', ctypes.c_uint32, 1),
        ('Spare16', ctypes.c_uint32, 1),
        ('Spare17', ctypes.c_uint32, 1),
        ('Spare18', ctypes.c_uint32, 1),
        ('Spare19', ctypes.c_uint32, 1),
        ('Spare20', ctypes.c_uint32, 1),
        ('SbClockOverride', ctypes.c_uint32, 1),
        ('PhytxClockgateDisable', ctypes.c_uint32, 1),
        ('DetxClockgateDisable', ctypes.c_uint32, 1),
        ('ChassisClockRequestDuration', ctypes.c_uint32, 4),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_SNPS_PHY_CHKN(ctypes.Union):
    value = 0
    offset = 0

    Spare0 = 0  # bit 0 to 1
    Spare1 = 0  # bit 1 to 2
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
    Spare12 = 0  # bit 12 to 13
    Spare13 = 0  # bit 13 to 14
    Spare14 = 0  # bit 14 to 15
    Spare15 = 0  # bit 15 to 16
    Spare16 = 0  # bit 16 to 17
    Spare17 = 0  # bit 17 to 18
    Spare18 = 0  # bit 18 to 19
    Spare19 = 0  # bit 19 to 20
    Spare20 = 0  # bit 20 to 21
    SbClockOverride = 0  # bit 21 to 22
    PhytxClockgateDisable = 0  # bit 22 to 23
    DetxClockgateDisable = 0  # bit 23 to 24
    ChassisClockRequestDuration = 0  # bit 24 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_CHKN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_CHKN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_NEN_RTERM(Enum):
    NEN_RTERM_TERMINATION_IS_ENABLED = 0x0  # EnableAUX differential termination, weak pre-bias to a common-mode voltag
                                            # e, and protection for plug transients. Use for all functional modes.
    NEN_RTERM_TERMINATION_IS_DISABLED = 0x1  # Disable on-die termination and weak common-mode drive. Use for pin leaka
                                             # ge testing.


class ENUM_AUX_DP_DN_SWAP(Enum):
    AUX_DP_DN_SWAP_PADP_POSITIVE_AND_PADN_NEGATIVE = 0x0
    AUX_DP_DN_SWAP_PADN_POSITIVE_AND_PADP_NEGATIVE = 0x1


class ENUM_ALL_POWER_OK(Enum):
    ALL_POWER_OK_NOT_WITHIN_TARGET_VALUE = 0x0
    ALL_POWER_OK_WITHIN_TARGET_VALUE = 0x1


class ENUM_AUX_MODE_ENABLE(Enum):
    AUX_MODE_ENABLE_PHY_NOT_CONFIGURED_AS_AUX = 0x0
    AUX_MODE_ENABLE_PHY_CONFIGURED_AS_AUX = 0x1


class OFFSET_SNPS_PHY_AUX_CNFG:
    SNPS_PHY_AUX_CNFG_PORT_A = 0x168180
    SNPS_PHY_AUX_CNFG_PORT_B = 0x169180
    SNPS_PHY_AUX_CNFG_PORT_C = 0x16A180
    SNPS_PHY_AUX_CNFG_PORT_D = 0x16B180
    SNPS_PHY_AUX_CNFG_PORT_TC1 = 0x16C180


class _SNPS_PHY_AUX_CNFG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 22),
        ('Aux_Hys_Tune', ctypes.c_uint32, 2),
        ('Aux_Vod_Tune', ctypes.c_uint32, 2),
        ('Nen_Rterm', ctypes.c_uint32, 1),
        ('Aux_Dp_Dn_Swap', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 2),
        ('AllPowerOk', ctypes.c_uint32, 1),
        ('AuxModeEnable', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_AUX_CNFG(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 22
    Aux_Hys_Tune = 0  # bit 22 to 24
    Aux_Vod_Tune = 0  # bit 24 to 26
    Nen_Rterm = 0  # bit 26 to 27
    Aux_Dp_Dn_Swap = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 30
    AllPowerOk = 0  # bit 30 to 31
    AuxModeEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_AUX_CNFG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_AUX_CNFG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_I2C_VIL_VIH_TUNE(Enum):
    I2C_VIL_VIH_TUNE_SCHMIT_BASED = 0x0  # Schimt based receiver is used to improve the VIL/VIH value.
    I2C_VIL_VIH_TUNE_COMPARATOR_BASED = 0x1  # Comparator based receiver is used to improve the VIL/VIH value.


class ENUM_I2CPADN_PD(Enum):
    I2CPADN_PD_PULL_DOWN_DISABLE = 0x0
    I2CPADN_PD_PULL_DOWN_ENABLE = 0x1


class ENUM_I2CPADP_PD(Enum):
    I2CPADP_PD_PULL_DOWN_DISABLE = 0x0
    I2CPADP_PD_PULL_DOWN_ENABLE = 0x1


class ENUM_I2C_MODE_ENABLE(Enum):
    I2C_MODE_ENABLE_PHY_NOT_CONFIGURED_AS_I2C = 0x0
    I2C_MODE_ENABLE_PHY_CONFIGURED_AS_I2C = 0x1


class OFFSET_SNPS_PHY_I2C_CNFG:
    SNPS_PHY_I2C_CNFG_PORT_A = 0x168184
    SNPS_PHY_I2C_CNFG_PORT_B = 0x169184
    SNPS_PHY_I2C_CNFG_PORT_C = 0x16A184
    SNPS_PHY_I2C_CNFG_PORT_D = 0x16B184
    SNPS_PHY_I2C_CNFG_PORT_TC1 = 0x16C184


class _SNPS_PHY_I2C_CNFG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 26),
        ('I2C_Ctrl', ctypes.c_uint32, 1),
        ('I2C_Vil_Vih_Tune', ctypes.c_uint32, 1),
        ('I2Cpadn_Pd', ctypes.c_uint32, 1),
        ('I2Cpadp_Pd', ctypes.c_uint32, 1),
        ('AllPowerOk', ctypes.c_uint32, 1),
        ('I2CModeEnable', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_I2C_CNFG(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 26
    I2C_Ctrl = 0  # bit 26 to 27
    I2C_Vil_Vih_Tune = 0  # bit 27 to 28
    I2Cpadn_Pd = 0  # bit 28 to 29
    I2Cpadp_Pd = 0  # bit 29 to 30
    AllPowerOk = 0  # bit 30 to 31
    I2CModeEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_I2C_CNFG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_I2C_CNFG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GENLOCK_DIRECTION_ENABLE_PIN_VALUE(Enum):
    GENLOCK_DIRECTION_ENABLE_PIN_VALUE_ENABLE_MOTHERBOARD_GENLOCK_CIRCUIT = 0x1
    GENLOCK_DIRECTION_ENABLE_PIN_VALUE_DISABLE_MOTHERBOARD_GENLOCK_CIRCUIT = 0x0


class ENUM_GENLOCK_DIRECTION_SELECT_PIN_VALUE(Enum):
    GENLOCK_DIRECTION_SELECT_PIN_VALUE_GENLOCK_SLAVE = 0x1
    GENLOCK_DIRECTION_SELECT_PIN_VALUE_GENLOCK_MASTER = 0x0


class ENUM_GENLOCK_DIRECTION_IO_SELECT(Enum):
    GENLOCK_DIRECTION_IO_SELECT_GENLOCK = 0x1
    GENLOCK_DIRECTION_IO_SELECT_BACKLIGHT = 0x0


class ENUM_BACKLIGHT_POLARITY(Enum):
    BACKLIGHT_POLARITY_ACTIVE_HIGH = 0x0
    BACKLIGHT_POLARITY_ACTIVE_LOW = 0x1


class ENUM_PWM_ENABLE(Enum):
    PWM_DISABLE = 0x0
    PWM_ENABLE = 0x1


class OFFSET_SBLC_PWM_CTL1:
    SBLC_PWM_CTL1 = 0xC8250
    SBLC_PWM_CTL1 = 0xC8250
    SBLC_PWM_CTL1_2 = 0xC8350


class _SBLC_PWM_CTL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GenlockDirectionEnablePinValue', ctypes.c_uint32, 1),
        ('GenlockDirectionSelectPinValue', ctypes.c_uint32, 1),
        ('GenlockDirectionIoSelect', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 26),
        ('BacklightPolarity', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 1),
        ('PwmEnable', ctypes.c_uint32, 1),
    ]


class REG_SBLC_PWM_CTL1(ctypes.Union):
    value = 0
    offset = 0

    GenlockDirectionEnablePinValue = 0  # bit 0 to 1
    GenlockDirectionSelectPinValue = 0  # bit 1 to 2
    GenlockDirectionIoSelect = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 29
    BacklightPolarity = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 31
    PwmEnable = 0  # bit 31 to 32

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


class ENUM_MICROSECOND_COUNTER_FRACTION_NUMERATOR(Enum):
    MICROSECOND_COUNTER_FRACTION_NUMERATOR_0 = 0x0  # No fraction
    MICROSECOND_COUNTER_FRACTION_NUMERATOR_1 = 0x1  # Numerator 1
    MICROSECOND_COUNTER_FRACTION_NUMERATOR_2 = 0x2  # Numerator 2


class ENUM_MICROSECOND_COUNTER_DIVIDER(Enum):
    MICROSECOND_COUNTER_DIVIDER_38_MHZ = 0x25


class ENUM_MICROSECOND_COUNTER_FRACTION_DENOMINATOR(Enum):
    MICROSECOND_COUNTER_FRACTION_DENOMINATOR_5 = 0x4  # Denominator 5
    MICROSECOND_COUNTER_FRACTION_DENOMINATOR_0 = 0x0  # No fraction


class ENUM_MICROSECOND_COUNTER_HOLD(Enum):
    MICROSECOND_COUNTER_HOLD_HOLD = 0x1  # Test - Hold the microsecond counter in a reset state
    MICROSECOND_COUNTER_HOLD_RUN = 0x0  # Let the microsecond counter run


class OFFSET_RAWCLK_FREQ:
    RAWCLK_FREQ = 0xC6204
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


class ENUM_PPS_IDLE(Enum):
    PPS_IDLE_IMPROVED_PPS_IDLE_DETECTION = 0x1
    PPS_IDLE_ORIGINAL_PPS_IDLE_DETECTION = 0x0


class ENUM_PPS_LOAD_FIX_DISABLE(Enum):
    PPS_LOAD_FIX_DISABLE_FIX_FOR_PPS_DELAY_LOADING = 0x1
    PPS_LOAD_FIX_ENABLE_FIX_FOR_PPS_DELAY_LOADING = 0x0


class ENUM_FORCE_PPS_IDLE(Enum):
    FORCE_PPS_IDLE_FORCE_IDLE = 0x1
    FORCE_PPS_IDLE_AUTOMATIC_IDLE = 0x0


class ENUM_INVERT_DDIA_HPD(Enum):
    INVERT_DDIA_HPD_INVERT = 0x1
    INVERT_DDIA_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_DDIB_HPD(Enum):
    INVERT_DDIB_HPD_INVERT = 0x1
    INVERT_DDIB_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_DDIC_HPD(Enum):
    INVERT_DDIC_HPD_INVERT = 0x1
    INVERT_DDIC_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_DDID_HPD(Enum):
    INVERT_DDID_HPD_INVERT = 0x1
    INVERT_DDID_HPD_DO_NOT_INVERT = 0x0


class ENUM_INVERT_TC1_HPD(Enum):
    INVERT_TC1_HPD_INVERT = 0x1
    INVERT_TC1_HPD_DO_NOT_INVERT = 0x0


class ENUM_WAKE_PIN_VALUE_OVERRIDE(Enum):
    WAKE_PIN_VALUE_OVERRIDE_OVERRIDE_TO_0 = 0x2
    WAKE_PIN_VALUE_OVERRIDE_OVERRIDE_TO_1 = 0x3


class ENUM_WAKE_PIN_ENABLE_OVERRIDE(Enum):
    WAKE_PIN_ENABLE_OVERRIDE_OVERRIDE_TO_DISABLE = 0x2
    WAKE_PIN_ENABLE_OVERRIDE_OVERRIDE_TO_ENABLE = 0x3


class OFFSET_SCHICKEN_1:
    SCHICKEN_1 = 0xC2000
    SCHICKEN_1 = 0xC2000


class _SCHICKEN_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PpsIdle', ctypes.c_uint32, 1),
        ('PpsLoadFixDisable', ctypes.c_uint32, 1),
        ('Spare2', ctypes.c_uint32, 1),
        ('ForcePpsIdle', ctypes.c_uint32, 1),
        ('Spare4', ctypes.c_uint32, 1),
        ('Spare5', ctypes.c_uint32, 1),
        ('Spare6', ctypes.c_uint32, 1),
        ('SbClkRunWithRefClkDis', ctypes.c_uint32, 1),
        ('ChassisClockRequestDuration', ctypes.c_uint32, 4),
        ('Spare12', ctypes.c_uint32, 1),
        ('Spare13', ctypes.c_uint32, 1),
        ('Spare14', ctypes.c_uint32, 1),
        ('InvertDdiaHpd', ctypes.c_uint32, 1),
        ('InvertDdibHpd', ctypes.c_uint32, 1),
        ('InvertDdicHpd', ctypes.c_uint32, 1),
        ('InvertDdidHpd', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 4),
        ('InvertTc1Hpd', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 4),
        ('WakePinValueOverride', ctypes.c_uint32, 2),
        ('WakePinEnableOverride', ctypes.c_uint32, 2),
    ]


class REG_SCHICKEN_1(ctypes.Union):
    value = 0
    offset = 0

    PpsIdle = 0  # bit 0 to 1
    PpsLoadFixDisable = 0  # bit 1 to 2
    Spare2 = 0  # bit 2 to 3
    ForcePpsIdle = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
    SbClkRunWithRefClkDis = 0  # bit 7 to 8
    ChassisClockRequestDuration = 0  # bit 8 to 12
    Spare12 = 0  # bit 12 to 13
    Spare13 = 0  # bit 13 to 14
    Spare14 = 0  # bit 14 to 15
    InvertDdiaHpd = 0  # bit 15 to 16
    InvertDdibHpd = 0  # bit 16 to 17
    InvertDdicHpd = 0  # bit 17 to 18
    InvertDdidHpd = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 23
    InvertTc1Hpd = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 28
    WakePinValueOverride = 0  # bit 28 to 30
    WakePinEnableOverride = 0  # bit 30 to 32

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
    GPIO_CTL_1 = 0xC5014
    GPIO_CTL_2 = 0xC5018
    GPIO_CTL_2 = 0xC5018
    GPIO_CTL_3 = 0xC501C
    GPIO_CTL_3 = 0xC501C
    GPIO_CTL_4 = 0xC5020
    GPIO_CTL_4 = 0xC5020
    GPIO_CTL_5 = 0xC5024
    GPIO_CTL_9 = 0xC5034
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

