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
# @file Gen12DisplayPowerRegs.py
# @brief contains Gen12DisplayPowerRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_DC_STATE_SELECT(Enum):
    DC_STATE_SELECT_0 = 0x0
    DC_STATE_SELECT_1 = 0x1
    DC_STATE_SELECT_2 = 0x2
    DC_STATE_SELECT_3 = 0x3
    DC_STATE_SELECT_4 = 0x4
    DC_STATE_SELECT_5 = 0x5
    DC_STATE_SELECT_6 = 0x6
    DC_STATE_SELECT_7 = 0x7


class OFFSET_DC_STATE_SEL:
    DC_STATE_SEL = 0x45500


class _DC_STATE_SEL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DcStateSelect', ctypes.c_uint32, 3),
        ('Reserved3', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 28),
    ]


class REG_DC_STATE_SEL(ctypes.Union):
    value = 0
    offset = 0

    DcStateSelect = 0  # bit 0 to 3
    Reserved3 = 0  # bit 3 to 4
    Reserved4 = 0  # bit 4 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DC_STATE_SEL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DC_STATE_SEL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DYNAMIC_DC_STATE_ENABLE(Enum):
    DYNAMIC_DC_STATE_DISABLE = 0x0
    DYNAMIC_DC_STATE_ENABLE_UP_TO_DC5 = 0x1
    DYNAMIC_DC_STATE_ENABLE_UP_TO_DC6 = 0x2


class ENUM_DC9_ALLOW(Enum):
    DC9_ALLOW_DO_NOT_ALLOW = 0x0
    DC9_ALLOW_ALLOW = 0x1


class ENUM_MASK_POKE(Enum):
    MASK_POKE_UNMASK = 0x0
    MASK_POKE_MASK = 0x1


class ENUM_BLOCK_OUTBOUND_TRAFFIC(Enum):
    BLOCK_OUTBOUND_TRAFFIC_DO_NOT_BLOCK = 0x0
    BLOCK_OUTBOUND_TRAFFIC_BLOCK = 0x1


class ENUM_IN_CSR_FLOW(Enum):
    IN_CSR_FLOW_NOT_IN_CSR = 0x0
    IN_CSR_FLOW_IN_CSR = 0x1


class ENUM_DSI_PLLS_TURN_OFF_DISALLOWED(Enum):
    DSI_PLLS_TURN_OFF_DISALLOWED_DSI_PLLS_TURN_OFF_ALLOWED = 0x0
    DSI_PLLS_TURN_OFF_DISALLOWED_DSI_PLLS_TURN_OFF_DISALLOWED = 0x1


class ENUM_DISPLAY_DCCO_STATE_STATUS(Enum):
    DISPLAY_DCCO_STATE_STATUS_DMC_DCCO_EXIT_COMPLETED = 0x1


class ENUM_DISPLAY_CLOCK_OFF_ENABLE(Enum):
    DISPLAY_CLOCK_OFF_ENABLE_DCCO_IS_DISALLOWED = 0x0
    DISPLAY_CLOCK_OFF_ENABLE_DCCO_IS_ALLOWED = 0x1


class ENUM_MODE_SET_IN_PROGRESS(Enum):
    MODE_SET_IN_PROGRESS_CSR_START_GENERATION_NOT_GATED = 0x0
    MODE_SET_IN_PROGRESS_CSR_START_GENERATION_IS_GATED = 0x1


class OFFSET_DC_STATE_EN:
    DC_STATE_EN = 0x45504


class _DC_STATE_EN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DynamicDcStateEnable', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('Dc9Allow', ctypes.c_uint32, 1),
        ('MaskPoke', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 2),
        ('BlockOutboundTraffic', ctypes.c_uint32, 1),
        ('InCsrFlow', ctypes.c_uint32, 1),
        ('Reserved10', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 5),
        ('Reserved16', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 3),
        ('Reserved20', ctypes.c_uint32, 2),
        ('Reserved22', ctypes.c_uint32, 2),
        ('Reserved24', ctypes.c_uint32, 4),
        ('DsiPllsTurnOffDisallowed', ctypes.c_uint32, 1),
        ('DisplayDcCoStateStatus', ctypes.c_uint32, 1),
        ('DisplayClockOffEnable', ctypes.c_uint32, 1),
        ('ModeSetInProgress', ctypes.c_uint32, 1),
    ]


class REG_DC_STATE_EN(ctypes.Union):
    value = 0
    offset = 0

    DynamicDcStateEnable = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    Dc9Allow = 0  # bit 3 to 4
    MaskPoke = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 8
    BlockOutboundTraffic = 0  # bit 8 to 9
    InCsrFlow = 0  # bit 9 to 10
    Reserved10 = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 16
    Reserved16 = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 20
    Reserved20 = 0  # bit 20 to 22
    Reserved22 = 0  # bit 22 to 24
    Reserved24 = 0  # bit 24 to 28
    DsiPllsTurnOffDisallowed = 0  # bit 28 to 29
    DisplayDcCoStateStatus = 0  # bit 29 to 30
    DisplayClockOffEnable = 0  # bit 30 to 31
    ModeSetInProgress = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DC_STATE_EN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DC_STATE_EN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_MASK_CORES(Enum):
    MASK_CORES_DO_NOT_MASK = 0x0  # Wait until cores are idle before starting CSR
    MASK_CORES_MASK = 0x1  # Do not wait until cores are idle before starting CSR


class ENUM_MASK_MEMORY_UP(Enum):
    MASK_MEMORY_UP_DO_NOT_MASK = 0x0  # Wait until memory up is deasserted before starting CSR
    MASK_MEMORY_UP_MASK = 0x1  # Do not wait until memory up is deasserted before starting CSR


class OFFSET_DC_STATE_DEBUG:
    DC_STATE_DEBUG = 0x45520


class _DC_STATE_DEBUG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MaskCores', ctypes.c_uint32, 1),
        ('MaskMemoryUp', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 30),
    ]


class REG_DC_STATE_DEBUG(ctypes.Union):
    value = 0
    offset = 0

    MaskCores = 0  # bit 0 to 1
    MaskMemoryUp = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DC_STATE_DEBUG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DC_STATE_DEBUG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_POWER_WELL_1_STATE(Enum):
    POWER_WELL_1_STATE_DISABLED = 0x0
    POWER_WELL_1_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_1_REQUEST(Enum):
    POWER_WELL_1_REQUEST_DISABLE = 0x0
    POWER_WELL_1_REQUEST_ENABLE = 0x1


class ENUM_POWER_WELL_2_STATE(Enum):
    POWER_WELL_2_STATE_DISABLED = 0x0
    POWER_WELL_2_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_2_REQUEST(Enum):
    POWER_WELL_2_REQUEST_DISABLE = 0x0
    POWER_WELL_2_REQUEST_ENABLE = 0x1


class ENUM_POWER_WELL_3_STATE(Enum):
    POWER_WELL_3_STATE_DISABLED = 0x0
    POWER_WELL_3_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_3_REQUEST(Enum):
    POWER_WELL_3_REQUEST_DISABLE = 0x0
    POWER_WELL_3_REQUEST_ENABLE = 0x1


class ENUM_POWER_WELL_4_STATE(Enum):
    POWER_WELL_4_STATE_DISABLED = 0x0
    POWER_WELL_4_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_4_REQUEST(Enum):
    POWER_WELL_4_REQUEST_DISABLE = 0x0
    POWER_WELL_4_REQUEST_ENABLE = 0x1


class ENUM_POWER_WELL_5_STATE(Enum):
    POWER_WELL_5_STATE_DISABLED = 0x0
    POWER_WELL_5_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_5_REQUEST(Enum):
    POWER_WELL_5_REQUEST_DISABLE = 0x0
    POWER_WELL_5_REQUEST_ENABLE = 0x1


class OFFSET_PWR_WELL_CTL:
    PWR_WELL_CTL1 = 0x45400
    PWR_WELL_CTL2 = 0x45404
    PWR_WELL_CTL4 = 0x4540C


class _PWR_WELL_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PowerWell1State', ctypes.c_uint32, 1),
        ('PowerWell1Request', ctypes.c_uint32, 1),
        ('PowerWell2State', ctypes.c_uint32, 1),
        ('PowerWell2Request', ctypes.c_uint32, 1),
        ('PowerWell3State', ctypes.c_uint32, 1),
        ('PowerWell3Request', ctypes.c_uint32, 1),
        ('PowerWell4State', ctypes.c_uint32, 1),
        ('PowerWell4Request', ctypes.c_uint32, 1),
        ('PowerWell5State', ctypes.c_uint32, 1),
        ('PowerWell5Request', ctypes.c_uint32, 1),
        ('Reserved10', ctypes.c_uint32, 12),
        ('Reserved22', ctypes.c_uint32, 10),
    ]


class REG_PWR_WELL_CTL(ctypes.Union):
    value = 0
    offset = 0

    PowerWell1State = 0  # bit 0 to 1
    PowerWell1Request = 0  # bit 1 to 2
    PowerWell2State = 0  # bit 2 to 3
    PowerWell2Request = 0  # bit 3 to 4
    PowerWell3State = 0  # bit 4 to 5
    PowerWell3Request = 0  # bit 5 to 6
    PowerWell4State = 0  # bit 6 to 7
    PowerWell4Request = 0  # bit 7 to 8
    PowerWell5State = 0  # bit 8 to 9
    PowerWell5Request = 0  # bit 9 to 10
    Reserved10 = 0  # bit 10 to 22
    Reserved22 = 0  # bit 22 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PWR_WELL_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PWR_WELL_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_AUX_A_IO_POWER_STATE(Enum):
    AUX_A_IO_POWER_STATE_DISABLED = 0x0
    AUX_A_IO_POWER_STATE_ENABLED = 0x1


class ENUM_AUX_A_IO_POWER_REQUEST(Enum):
    AUX_A_IO_POWER_REQUEST_DISABLE = 0x0
    AUX_A_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_AUX_B_IO_POWER_STATE(Enum):
    AUX_B_IO_POWER_STATE_DISABLED = 0x0
    AUX_B_IO_POWER_STATE_ENABLED = 0x1


class ENUM_AUX_B_IO_POWER_REQUEST(Enum):
    AUX_B_IO_POWER_REQUEST_DISABLE = 0x0
    AUX_B_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_AUX_C_IO_POWER_STATE(Enum):
    AUX_C_IO_POWER_STATE_DISABLED = 0x0
    AUX_C_IO_POWER_STATE_ENABLED = 0x1


class ENUM_AUX_C_IO_POWER_REQUEST(Enum):
    AUX_C_IO_POWER_REQUEST_DISABLE = 0x0
    AUX_C_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_USBC1_IO_POWER_STATE(Enum):
    USBC1_IO_POWER_STATE_DISABLED = 0x0
    USBC1_IO_POWER_STATE_ENABLED = 0x1


class ENUM_USBC1_IO_POWER_REQUEST(Enum):
    USBC1_IO_POWER_REQUEST_DISABLE = 0x0
    USBC1_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_USBC2_IO_POWER_STATE(Enum):
    USBC2_IO_POWER_STATE_DISABLE = 0x0
    USBC2_IO_POWER_STATE_ENABLE = 0x1


class ENUM_USBC2_IO_POWER_REQUEST(Enum):
    USBC2_IO_POWER_REQUEST_DISABLE = 0x0
    USBC2_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_USBC3_IO_POWER_STATE(Enum):
    USBC3_IO_POWER_STATE_DISABLE = 0x0
    USBC3_IO_POWER_STATE_ENABLE = 0x1


class ENUM_USBC3_IO_POWER_REQUEST(Enum):
    USBC3_IO_POWER_REQUEST_DISABLE = 0x0
    USBC3_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_USBC4_IO_POWER_STATE(Enum):
    USBC4_IO_POWER_STATE_DISABLE = 0x0
    USBC4_IO_POWER_STATE_ENABLE = 0x1


class ENUM_USBC4_IO_POWER_REQUEST(Enum):
    USBC4_IO_POWER_REQUEST_DISABLE = 0x0
    USBC4_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_USBC5_IO_POWER_STATE(Enum):
    USBC5_IO_POWER_STATE_DISABLE = 0x0
    USBC5_IO_POWER_STATE_ENABLE = 0x1


class ENUM_USBC5_IO_POWER_REQUEST(Enum):
    USBC5_IO_POWER_REQUEST_DISABLE = 0x0
    USBC5_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_USBC6_IO_POWER_STATE(Enum):
    USBC6_IO_POWER_STATE_DISABLE = 0x0
    USBC6_IO_POWER_STATE_ENABLE = 0x1


class ENUM_USBC6_IO_POWER_REQUEST(Enum):
    USBC6_IO_POWER_REQUEST_DISABLE = 0x0
    USBC6_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_AUX_TBT1_IO_POWER_STATE(Enum):
    AUX_TBT1_IO_POWER_STATE_DISABLE = 0x0
    AUX_TBT1_IO_POWER_STATE_ENABLE = 0x1


class ENUM_AUX_TBT1_IO_POWER_REQUEST(Enum):
    AUX_TBT1_IO_POWER_REQUEST_DISABLE = 0x0
    AUX_TBT1_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_AUX_TBT2_IO_POWER_STATE(Enum):
    AUX_TBT2_IO_POWER_STATE_DISABLE = 0x0
    AUX_TBT2_IO_POWER_STATE_ENABLE = 0x1


class ENUM_AUX_TBT2_IO_POWER_REQUEST(Enum):
    AUX_TBT2_IO_POWER_REQUEST_DISABLE = 0x0
    AUX_TBT2_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_AUX_TBT3_IO_POWER_STATE(Enum):
    AUX_TBT3_IO_POWER_STATE_DISABLE = 0x0
    AUX_TBT3_IO_POWER_STATE_ENABLE = 0x1


class ENUM_AUX_TBT3_IO_POWER_REQUEST(Enum):
    AUX_TBT3_IO_POWER_REQUEST_DISABLE = 0x0
    AUX_TBT3_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_AUX_TBT4_IO_POWER_STATE(Enum):
    AUX_TBT4_IO_POWER_STATE_DISABLE = 0x0
    AUX_TBT4_IO_POWER_STATE_ENABLE = 0x1


class ENUM_AUX_TBT4_IO_POWER_REQUEST(Enum):
    AUX_TBT4_IO_POWER_REQUEST_DISABLE = 0x0
    AUX_TBT4_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_AUX_TBT5_IO_POWER_STATE(Enum):
    AUX_TBT5_IO_POWER_STATE_DISABLE = 0x0
    AUX_TBT5_IO_POWER_STATE_ENABLE = 0x1


class ENUM_AUX_TBT5_IO_POWER_REQUEST(Enum):
    AUX_TBT5_IO_POWER_REQUEST_DISABLE = 0x0
    AUX_TBT5_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_AUX_TBT6_IO_POWER_STATE(Enum):
    AUX_TBT6_IO_POWER_STATE_DISABLE = 0x0
    AUX_TBT6_IO_POWER_STATE_ENABLE = 0x1


class ENUM_AUX_TBT6_IO_POWER_REQUEST(Enum):
    AUX_TBT6_IO_POWER_REQUEST_DISABLE = 0x0
    AUX_TBT6_IO_POWER_REQUEST_ENABLE = 0x1


class OFFSET_PWR_WELL_CTL_AUX:
    PWR_WELL_CTL_AUX1 = 0x45440
    PWR_WELL_CTL_AUX2 = 0x45444
    PWR_WELL_CTL_AUX4 = 0x4544C


class _PWR_WELL_CTL_AUX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AuxAIoPowerState', ctypes.c_uint32, 1),
        ('AuxAIoPowerRequest', ctypes.c_uint32, 1),
        ('AuxBIoPowerState', ctypes.c_uint32, 1),
        ('AuxBIoPowerRequest', ctypes.c_uint32, 1),
        ('AuxCIoPowerState', ctypes.c_uint32, 1),
        ('AuxCIoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc1IoPowerState', ctypes.c_uint32, 1),
        ('Usbc1IoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc2IoPowerState', ctypes.c_uint32, 1),
        ('Usbc2IoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc3IoPowerState', ctypes.c_uint32, 1),
        ('Usbc3IoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc4IoPowerState', ctypes.c_uint32, 1),
        ('Usbc4IoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc5IoPowerState', ctypes.c_uint32, 1),
        ('Usbc5IoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc6IoPowerState', ctypes.c_uint32, 1),
        ('Usbc6IoPowerRequest', ctypes.c_uint32, 1),
        ('AuxTbt1IoPowerState', ctypes.c_uint32, 1),
        ('AuxTbt1IoPowerRequest', ctypes.c_uint32, 1),
        ('AuxTbt2IoPowerState', ctypes.c_uint32, 1),
        ('AuxTbt2IoPowerRequest', ctypes.c_uint32, 1),
        ('AuxTbt3IoPowerState', ctypes.c_uint32, 1),
        ('AuxTbt3IoPowerRequest', ctypes.c_uint32, 1),
        ('AuxTbt4IoPowerState', ctypes.c_uint32, 1),
        ('AuxTbt4IoPowerRequest', ctypes.c_uint32, 1),
        ('AuxTbt5IoPowerState', ctypes.c_uint32, 1),
        ('AuxTbt5IoPowerRequest', ctypes.c_uint32, 1),
        ('AuxTbt6IoPowerState', ctypes.c_uint32, 1),
        ('AuxTbt6IoPowerRequest', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PWR_WELL_CTL_AUX(ctypes.Union):
    value = 0
    offset = 0

    AuxAIoPowerState = 0  # bit 0 to 1
    AuxAIoPowerRequest = 0  # bit 1 to 2
    AuxBIoPowerState = 0  # bit 2 to 3
    AuxBIoPowerRequest = 0  # bit 3 to 4
    AuxCIoPowerState = 0  # bit 4 to 5
    AuxCIoPowerRequest = 0  # bit 5 to 6
    Usbc1IoPowerState = 0  # bit 6 to 7
    Usbc1IoPowerRequest = 0  # bit 7 to 8
    Usbc2IoPowerState = 0  # bit 8 to 9
    Usbc2IoPowerRequest = 0  # bit 9 to 10
    Usbc3IoPowerState = 0  # bit 10 to 11
    Usbc3IoPowerRequest = 0  # bit 11 to 12
    Usbc4IoPowerState = 0  # bit 12 to 13
    Usbc4IoPowerRequest = 0  # bit 13 to 14
    Usbc5IoPowerState = 0  # bit 14 to 15
    Usbc5IoPowerRequest = 0  # bit 15 to 16
    Usbc6IoPowerState = 0  # bit 16 to 17
    Usbc6IoPowerRequest = 0  # bit 17 to 18
    AuxTbt1IoPowerState = 0  # bit 18 to 19
    AuxTbt1IoPowerRequest = 0  # bit 19 to 20
    AuxTbt2IoPowerState = 0  # bit 20 to 21
    AuxTbt2IoPowerRequest = 0  # bit 21 to 22
    AuxTbt3IoPowerState = 0  # bit 22 to 23
    AuxTbt3IoPowerRequest = 0  # bit 23 to 24
    AuxTbt4IoPowerState = 0  # bit 24 to 25
    AuxTbt4IoPowerRequest = 0  # bit 25 to 26
    AuxTbt5IoPowerState = 0  # bit 26 to 27
    AuxTbt5IoPowerRequest = 0  # bit 27 to 28
    AuxTbt6IoPowerState = 0  # bit 28 to 29
    AuxTbt6IoPowerRequest = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PWR_WELL_CTL_AUX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PWR_WELL_CTL_AUX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DDI_A_IO_POWER_STATE(Enum):
    DDI_A_IO_POWER_STATE_DISABLED = 0x0
    DDI_A_IO_POWER_STATE_ENABLED = 0x1


class ENUM_DDI_A_IO_POWER_REQUEST(Enum):
    DDI_A_IO_POWER_REQUEST_DISABLE = 0x0
    DDI_A_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_DDI_B_IO_POWER_STATE(Enum):
    DDI_B_IO_POWER_STATE_DISABLED = 0x0
    DDI_B_IO_POWER_STATE_ENABLED = 0x1


class ENUM_DDI_B_IO_POWER_REQUEST(Enum):
    DDI_B_IO_POWER_REQUEST_DISABLE = 0x0
    DDI_B_IO_POWER_REQUEST_ENABLE = 0x1


class ENUM_DDI_C_IO_POWER_STATE(Enum):
    DDI_C_IO_POWER_STATE_DISABLED = 0x0
    DDI_C_IO_POWER_STATE_ENABLED = 0x1


class ENUM_DDI_C_IO_POWER_REQUEST(Enum):
    DDI_C_IO_POWER_REQUEST_DISABLE = 0x0
    DDI_C_IO_POWER_REQUEST_ENABLE = 0x1


class OFFSET_PWR_WELL_CTL_DDI:
    PWR_WELL_CTL_DDI1 = 0x45450
    PWR_WELL_CTL_DDI2 = 0x45454
    PWR_WELL_CTL_DDI4 = 0x4545C


class _PWR_WELL_CTL_DDI(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiAIoPowerState', ctypes.c_uint32, 1),
        ('DdiAIoPowerRequest', ctypes.c_uint32, 1),
        ('DdiBIoPowerState', ctypes.c_uint32, 1),
        ('DdiBIoPowerRequest', ctypes.c_uint32, 1),
        ('DdiCIoPowerState', ctypes.c_uint32, 1),
        ('DdiCIoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc1IoPowerState', ctypes.c_uint32, 1),
        ('Usbc1IoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc2IoPowerState', ctypes.c_uint32, 1),
        ('Usbc2IoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc3IoPowerState', ctypes.c_uint32, 1),
        ('Usbc3IoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc4IoPowerState', ctypes.c_uint32, 1),
        ('Usbc4IoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc5IoPowerState', ctypes.c_uint32, 1),
        ('Usbc5IoPowerRequest', ctypes.c_uint32, 1),
        ('Usbc6IoPowerState', ctypes.c_uint32, 1),
        ('Usbc6IoPowerRequest', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 5),
        ('Reserved23', ctypes.c_uint32, 9),
    ]


class REG_PWR_WELL_CTL_DDI(ctypes.Union):
    value = 0
    offset = 0

    DdiAIoPowerState = 0  # bit 0 to 1
    DdiAIoPowerRequest = 0  # bit 1 to 2
    DdiBIoPowerState = 0  # bit 2 to 3
    DdiBIoPowerRequest = 0  # bit 3 to 4
    DdiCIoPowerState = 0  # bit 4 to 5
    DdiCIoPowerRequest = 0  # bit 5 to 6
    Usbc1IoPowerState = 0  # bit 6 to 7
    Usbc1IoPowerRequest = 0  # bit 7 to 8
    Usbc2IoPowerState = 0  # bit 8 to 9
    Usbc2IoPowerRequest = 0  # bit 9 to 10
    Usbc3IoPowerState = 0  # bit 10 to 11
    Usbc3IoPowerRequest = 0  # bit 11 to 12
    Usbc4IoPowerState = 0  # bit 12 to 13
    Usbc4IoPowerRequest = 0  # bit 13 to 14
    Usbc5IoPowerState = 0  # bit 14 to 15
    Usbc5IoPowerRequest = 0  # bit 15 to 16
    Usbc6IoPowerState = 0  # bit 16 to 17
    Usbc6IoPowerRequest = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 23
    Reserved23 = 0  # bit 23 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PWR_WELL_CTL_DDI),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PWR_WELL_CTL_DDI, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_FUSE_PG5_DISTRIBUTION_STATUS(Enum):
    FUSE_PG5_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PG5_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PG4_DISTRIBUTION_STATUS(Enum):
    FUSE_PG4_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PG4_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PG3_DISTRIBUTION_STATUS(Enum):
    FUSE_PG3_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PG3_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PG2_DISTRIBUTION_STATUS(Enum):
    FUSE_PG2_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PG2_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PG1_DISTRIBUTION_STATUS(Enum):
    FUSE_PG1_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PG1_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PG0_DISTRIBUTION_STATUS(Enum):
    FUSE_PG0_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PG0_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_DOWNLOAD_STATUS(Enum):
    FUSE_DOWNLOAD_STATUS_NOT_DONE = 0x0
    FUSE_DOWNLOAD_STATUS_DONE = 0x1


class OFFSET_FUSE_STATUS:
    FUSE_STATUS = 0x42000


class _FUSE_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 6),
        ('FusePg5DistributionStatus', ctypes.c_uint32, 1),
        ('FusePg4DistributionStatus', ctypes.c_uint32, 1),
        ('FusePg3DistributionStatus', ctypes.c_uint32, 1),
        ('FusePg2DistributionStatus', ctypes.c_uint32, 1),
        ('FusePg1DistributionStatus', ctypes.c_uint32, 1),
        ('FusePg0DistributionStatus', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 3),
        ('FuseDownloadStatus', ctypes.c_uint32, 1),
    ]


class REG_FUSE_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 22
    FusePg5DistributionStatus = 0  # bit 22 to 23
    FusePg4DistributionStatus = 0  # bit 23 to 24
    FusePg3DistributionStatus = 0  # bit 24 to 25
    FusePg2DistributionStatus = 0  # bit 25 to 26
    FusePg1DistributionStatus = 0  # bit 26 to 27
    FusePg0DistributionStatus = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 31
    FuseDownloadStatus = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _FUSE_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_FUSE_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

