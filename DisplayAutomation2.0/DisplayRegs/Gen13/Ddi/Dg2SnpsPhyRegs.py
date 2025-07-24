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
# @file Dg2SnpsPhyRegs.py
# @brief contains Dg2SnpsPhyRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_POWER_STATE(Enum):
    POWER_STATE_DISABLED = 0x0
    POWER_STATE_ENABLED = 0x1


class ENUM_POWER_ENABLE(Enum):
    POWER_DISABLE = 0x0
    POWER_ENABLE = 0x1


class ENUM_PLL_LOCK(Enum):
    PLL_LOCK_NOT_LOCKED_OR_NOT_ENABLED = 0x0
    PLL_LOCK_LOCKED = 0x1


class ENUM_PLL_ENABLE(Enum):
    PLL_DISABLE = 0x0
    PLL_ENABLE = 0x1


class OFFSET_DPLL_ENABLE:
    PORTA_PLL_ENABLE = 0x46010
    PORTB_PLL_ENABLE = 0x46014
    PORTC_PLL_ENABLE = 0x46018
    PORTD_PLL_ENABLE = 0x4601C
    PORTTC1_PLL_ENABLE = 0x46030


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
        ('Dp_Tx3_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx2_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx1_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx0_Ack', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 4),
        ('Dp_Tx3_Req', ctypes.c_uint32, 1),
        ('Dp_Tx2_Req', ctypes.c_uint32, 1),
        ('Dp_Tx1_Req', ctypes.c_uint32, 1),
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
    Dp_Tx3_Ack = 0  # bit 20 to 21
    Dp_Tx2_Ack = 0  # bit 21 to 22
    Dp_Tx1_Ack = 0  # bit 22 to 23
    Dp_Tx0_Ack = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 28
    Dp_Tx3_Req = 0  # bit 28 to 29
    Dp_Tx2_Req = 0  # bit 29 to 30
    Dp_Tx1_Req = 0  # bit 30 to 31
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


class OFFSET_SNPS_PHY_MPLLB_CP:
    SNPS_PHY_MPLLB_CP_PORT_A = 0x168000
    SNPS_PHY_MPLLB_CP_PORT_B = 0x169000
    SNPS_PHY_MPLLB_CP_PORT_C = 0x16A000
    SNPS_PHY_MPLLB_CP_PORT_D = 0x16B000
    SNPS_PHY_MPLLB_CP_PORT_TC1 = 0x16C000


class _SNPS_PHY_MPLLB_CP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Cp_Prop_Gs', ctypes.c_uint32, 7),
        ('Reserved8', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Cp_Prop', ctypes.c_uint32, 7),
        ('Reserved16', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Cp_Int_Gs', ctypes.c_uint32, 7),
        ('Reserved24', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Cp_Int', ctypes.c_uint32, 7),
    ]


class REG_SNPS_PHY_MPLLB_CP(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    Dp_Mpllb_Cp_Prop_Gs = 0  # bit 1 to 8
    Reserved8 = 0  # bit 8 to 9
    Dp_Mpllb_Cp_Prop = 0  # bit 9 to 16
    Reserved16 = 0  # bit 16 to 17
    Dp_Mpllb_Cp_Int_Gs = 0  # bit 17 to 24
    Reserved24 = 0  # bit 24 to 25
    Dp_Mpllb_Cp_Int = 0  # bit 25 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_CP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_CP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DP_SHIM_DIV32_CLK_SEL(Enum):
    DP_SHIM_DIV32_CLK_SEL_DIV32 = 0x1
    DP_SHIM_DIV32_CLK_SEL_DIV20 = 0x0


class ENUM_DP_MPLLB_TX_CLK_DIV(Enum):
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_1 = 0x0
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_2 = 0x1
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_4 = 0x2
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_8 = 0x3
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_3 = 0x4
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_5 = 0x5
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_6 = 0x6
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_0 = 0x7


class ENUM_DP2_MODE(Enum):
    DP2_MODE_DP2_0_NOT_SELECTED = 0x0
    DP2_MODE_DP2_0_SELECTED = 0x1


class OFFSET_SNPS_PHY_MPLLB_DIV:
    SNPS_PHY_MPLLB_DIV_PORT_A = 0x168004
    SNPS_PHY_MPLLB_DIV_PORT_B = 0x169004
    SNPS_PHY_MPLLB_DIV_PORT_C = 0x16A004
    SNPS_PHY_MPLLB_DIV_PORT_D = 0x16B004
    SNPS_PHY_MPLLB_DIV_PORT_TC1 = 0x16C004


class _SNPS_PHY_MPLLB_DIV(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dp_Shim_Div32_Clk_Sel', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 4),
        ('Dp_Mpllb_Tx_Clk_Div', ctypes.c_uint32, 3),
        ('Dp_Mpllb_Word_Div2_En', ctypes.c_uint32, 1),
        ('Dp2_Mode', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Pmix_En', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 5),
        ('Dp_Mpllb_Div_Multiplier', ctypes.c_uint32, 8),
        ('Dp_Mpllb_Freq_Vco', ctypes.c_uint32, 2),
        ('Dp_Mpllb_V2I', ctypes.c_uint32, 2),
        ('Dp_Mpllb_Init_Cal_Disable', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Div5_Clk_En', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Div_Clk_En', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Force_En', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_MPLLB_DIV(ctypes.Union):
    value = 0
    offset = 0

    Dp_Shim_Div32_Clk_Sel = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 5
    Dp_Mpllb_Tx_Clk_Div = 0  # bit 5 to 8
    Dp_Mpllb_Word_Div2_En = 0  # bit 8 to 9
    Dp2_Mode = 0  # bit 9 to 10
    Dp_Mpllb_Pmix_En = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 16
    Dp_Mpllb_Div_Multiplier = 0  # bit 16 to 24
    Dp_Mpllb_Freq_Vco = 0  # bit 24 to 26
    Dp_Mpllb_V2I = 0  # bit 26 to 28
    Dp_Mpllb_Init_Cal_Disable = 0  # bit 28 to 29
    Dp_Mpllb_Div5_Clk_En = 0  # bit 29 to 30
    Dp_Mpllb_Div_Clk_En = 0  # bit 30 to 31
    Dp_Mpllb_Force_En = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_DIV),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_DIV, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SNPS_PHY_MPLLB_DIV2:
    SNPS_PHY_MPLLB_DIV2_PORT_A = 0x16801C
    SNPS_PHY_MPLLB_DIV2_PORT_B = 0x16901C
    SNPS_PHY_MPLLB_DIV2_PORT_C = 0x16A01C
    SNPS_PHY_MPLLB_DIV2_PORT_D = 0x16B01C
    SNPS_PHY_MPLLB_DIV2_PORT_TC1 = 0x16C01C


class _SNPS_PHY_MPLLB_DIV2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dp_Mpllb_Mulitplier', ctypes.c_uint32, 12),
        ('Dp_Ref_Clk_Mpllb_Div', ctypes.c_uint32, 3),
        ('Hdmi_Mpllb_Hdmi_Div', ctypes.c_uint32, 3),
        ('Hdmi_Mpllb_Hdmi_Pixel_Clk_Div', ctypes.c_uint32, 2),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_SNPS_PHY_MPLLB_DIV2(ctypes.Union):
    value = 0
    offset = 0

    Dp_Mpllb_Mulitplier = 0  # bit 0 to 12
    Dp_Ref_Clk_Mpllb_Div = 0  # bit 12 to 15
    Hdmi_Mpllb_Hdmi_Div = 0  # bit 15 to 18
    Hdmi_Mpllb_Hdmi_Pixel_Clk_Div = 0  # bit 18 to 20
    Reserved20 = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_DIV2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_DIV2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DP_MPLLB_SSC_EN(Enum):
    DP_MPLLB_SSC_EN_DISABLE = 0x0
    DP_MPLLB_SSC_EN_ENABLE = 0x1


class OFFSET_SNPS_PHY_MPLLB_SSCEN:
    SNPS_PHY_MPLLB_SSCEN_PORT_A = 0x168014
    SNPS_PHY_MPLLB_SSCEN_PORT_B = 0x169014
    SNPS_PHY_MPLLB_SSCEN_PORT_C = 0x16A014
    SNPS_PHY_MPLLB_SSCEN_PORT_D = 0x16B014
    SNPS_PHY_MPLLB_SSCEN_PORT_TC1 = 0x16C014


class _SNPS_PHY_MPLLB_SSCEN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 10),
        ('Dp_Mpllb_Ssc_Peak', ctypes.c_uint32, 20),
        ('Dp_Mpllb_Ssc_Up_Spread', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Ssc_En', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_MPLLB_SSCEN(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 10
    Dp_Mpllb_Ssc_Peak = 0  # bit 10 to 30
    Dp_Mpllb_Ssc_Up_Spread = 0  # bit 30 to 31
    Dp_Mpllb_Ssc_En = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_SSCEN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_SSCEN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SNPS_PHY_MPLLB_FRACN1:
    SNPS_PHY_MPLLB_FRACN1_PORT_A = 0x168008
    SNPS_PHY_MPLLB_FRACN1_PORT_B = 0x169008
    SNPS_PHY_MPLLB_FRACN1_PORT_C = 0x16A008
    SNPS_PHY_MPLLB_FRACN1_PORT_D = 0x16B008
    SNPS_PHY_MPLLB_FRACN1_PORT_TC1 = 0x16C008


class _SNPS_PHY_MPLLB_FRACN1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dp_Mpllb_Fracn_Den', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 14),
        ('Dp_Mpllb_Fracn_Cfg_Update_En', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Fracn_En', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_MPLLB_FRACN1(ctypes.Union):
    value = 0
    offset = 0

    Dp_Mpllb_Fracn_Den = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 30
    Dp_Mpllb_Fracn_Cfg_Update_En = 0  # bit 30 to 31
    Dp_Mpllb_Fracn_En = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_FRACN1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_FRACN1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SNPS_PHY_MPLLB_FRACN2:
    SNPS_PHY_MPLLB_FRACN2_PORT_A = 0x16800C
    SNPS_PHY_MPLLB_FRACN2_PORT_B = 0x16900C
    SNPS_PHY_MPLLB_FRACN2_PORT_C = 0x16A00C
    SNPS_PHY_MPLLB_FRACN2_PORT_D = 0x16B00C
    SNPS_PHY_MPLLB_FRACN2_PORT_TC1 = 0x16C00C


class _SNPS_PHY_MPLLB_FRACN2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dp_Mpllb_Fracn_Quot', ctypes.c_uint32, 16),
        ('Dp_Mpllb_Fracn_Rem', ctypes.c_uint32, 16),
    ]


class REG_SNPS_PHY_MPLLB_FRACN2(ctypes.Union):
    value = 0
    offset = 0

    Dp_Mpllb_Fracn_Quot = 0  # bit 0 to 16
    Dp_Mpllb_Fracn_Rem = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_FRACN2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_FRACN2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SNPS_PHY_MPLLB_SSCSTEP:
    SNPS_PHY_MPLLB_SSCSTEP_PORT_A = 0x168018
    SNPS_PHY_MPLLB_SSCSTEP_PORT_B = 0x169018
    SNPS_PHY_MPLLB_SSCSTEP_PORT_C = 0x16A018
    SNPS_PHY_MPLLB_SSCSTEP_PORT_D = 0x16B018
    SNPS_PHY_MPLLB_SSCSTEP_PORT_TC1 = 0x16C018


class _SNPS_PHY_MPLLB_SSCSTEP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 11),
        ('Dp_Mpllb_Ssc_Stepsize', ctypes.c_uint32, 21),
    ]


class REG_SNPS_PHY_MPLLB_SSCSTEP(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 11
    Dp_Mpllb_Ssc_Stepsize = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_SSCSTEP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_SSCSTEP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_HW_SEQ_STATE(Enum):
    HW_SEQ_STATE_PHY_INIT = 0x0
    HW_SEQ_STATE_PLL_OFF = 0x1
    HW_SEQ_STATE_REQ_PLL_ON = 0x2
    HW_SEQ_STATE_PLL_ON_P3 = 0x3
    HW_SEQ_STATE_LANE_RST = 0x4
    HW_SEQ_STATE_REQ_P0 = 0x5
    HW_SEQ_STATE_LANES_OUT_OF_RST_P0 = 0x6
    HW_SEQ_STATE_REQ_P3 = 0x7
    HW_SEQ_STATE_WAIT_FOR_PLL_OFF_ACK = 0x8
    HW_SEQ_STATE_DRIVE_DPALT_DISABLE_SIGNALS = 0x9
    HW_SEQ_STATE_REQ_PSR_PSTATE = 0xA
    HW_SEQ_STATE_PSR_STATE = 0xB


class OFFSET_SNPS_PHY_MPLLB_STATUS:
    SNPS_PHY_MPLLB_STATUS_PORT_A = 0x168010
    SNPS_PHY_MPLLB_STATUS_PORT_B = 0x169010
    SNPS_PHY_MPLLB_STATUS_PORT_C = 0x16A010
    SNPS_PHY_MPLLB_STATUS_PORT_D = 0x16B010
    SNPS_PHY_MPLLB_STATUS_PORT_TC1 = 0x16C010


class _SNPS_PHY_MPLLB_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hw_Seq_State', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 19),
        ('Dp_Tx0_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx0_Req', ctypes.c_uint32, 1),
        ('Dp_Tx1_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx1_Req', ctypes.c_uint32, 1),
        ('Dp_Tx2_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx2_Req', ctypes.c_uint32, 1),
        ('Dp_Tx3_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx3_Req', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_MPLLB_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Hw_Seq_State = 0  # bit 0 to 4
    Reserved4 = 0  # bit 4 to 23
    Dp_Tx0_Ack = 0  # bit 23 to 24
    Dp_Tx0_Req = 0  # bit 24 to 25
    Dp_Tx1_Ack = 0  # bit 25 to 26
    Dp_Tx1_Req = 0  # bit 26 to 27
    Dp_Tx2_Ack = 0  # bit 27 to 28
    Dp_Tx2_Req = 0  # bit 28 to 29
    Dp_Tx3_Ack = 0  # bit 29 to 30
    Dp_Tx3_Req = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_FILTER_PLL_INPUT_MUX_SELECT(Enum):
    FILTER_PLL_INPUT_MUX_SELECT_NONGENLOCK = 0x0
    FILTER_PLL_INPUT_MUX_SELECT_GENLOCK = 0x1


class ENUM_FILTER_PLL_LOCK(Enum):
    FILTER_PLL_LOCK_NOT_LOCKED_OR_NOT_ENABLED = 0x0
    FILTER_PLL_LOCK_LOCKED = 0x1


class ENUM_FILTER_PLL_ENABLE(Enum):
    FILTER_PLL_DISABLE = 0x0  # Filter PLL disabled.
    FILTER_PLL_ENABLE = 0x1  # Filter PLL enabled.


class ENUM_REFCLK_MUX_SELECT(Enum):
    REFCLK_MUX_SELECT_100_MHZ = 0x1  # PHY is configured for native DP and HDMI connections.
    REFCLK_MUX_SELECT_38_4_MHZ = 0x0  # PHY is configured for type-C connections.


class ENUM_DP_REF_CLK_REQ(Enum):
    DP_REF_CLK_REQ_REF_CLOCK_CAN_BE_DISABLED = 0x0
    DP_REF_CLK_REQ_REF_CLOCK_CANNOT_BE_DISABLED = 0x1


class ENUM_DP_REF_CLK_EN(Enum):
    DP_REF_CLK_EN_REF_CLOCK_IS_NOT_ENABLED = 0x0
    DP_REF_CLK_EN_REF_CLOCK_IS_ENABLED = 0x1


class OFFSET_SNPS_PHY_REF_CONTROL:
    SNPS_PHY_REF_CONTROL_PORT_A = 0x168188
    SNPS_PHY_REF_CONTROL_PORT_B = 0x169188
    SNPS_PHY_REF_CONTROL_PORT_C = 0x16A188
    SNPS_PHY_REF_CONTROL_PORT_D = 0x16B188
    SNPS_PHY_REF_CONTROL_PORT_TC1 = 0x16C188


class _SNPS_PHY_REF_CONTROL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 13),
        ('FilterPllInputMuxSelect', ctypes.c_uint32, 1),
        ('FilterPllLock', ctypes.c_uint32, 1),
        ('FilterPllEnable', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 8),
        ('RefclkMuxSelect', ctypes.c_uint32, 1),
        ('Dp_Ref_Clk_Req', ctypes.c_uint32, 1),
        ('Dp_Ref_Clk_En', ctypes.c_uint32, 1),
        ('Ref_Range', ctypes.c_uint32, 5),
    ]


class REG_SNPS_PHY_REF_CONTROL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 13
    FilterPllInputMuxSelect = 0  # bit 13 to 14
    FilterPllLock = 0  # bit 14 to 15
    FilterPllEnable = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 24
    RefclkMuxSelect = 0  # bit 24 to 25
    Dp_Ref_Clk_Req = 0  # bit 25 to 26
    Dp_Ref_Clk_En = 0  # bit 26 to 27
    Ref_Range = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_REF_CONTROL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_REF_CONTROL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

