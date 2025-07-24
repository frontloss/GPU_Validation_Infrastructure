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
# @file Gen11p5DisplayPowerRegs.py
# @brief contains Gen11p5DisplayPowerRegs.py related register definitions

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
        ('Reserved3', ctypes.c_uint32, 29),
    ]


class REG_DC_STATE_SEL(ctypes.Union):
    value = 0
    offset = 0

    DcStateSelect = 0  # bit 0 to 3
    Reserved3 = 0  # bit 3 to 32

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
        ('Reserved10', ctypes.c_uint32, 22),
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
    Reserved10 = 0  # bit 10 to 32

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
        ('Reserved18', ctypes.c_uint32, 14),
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
    Reserved18 = 0  # bit 18 to 32

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
        ('Reserved0', ctypes.c_uint32, 22),
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

    Reserved0 = 0  # bit 0 to 22
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

