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
# @file Gen13DklPhyRegs.py
# @brief contains Gen13DklPhyRegs.py related register definitions

import ctypes
from enum import Enum


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


class OFFSET_DKL_TX_PMD_LANE_SUS_LN0:
    DKL_TX_PMD_LANE_SUS_LN0 = 0xD00


class _DKL_TX_PMD_LANE_SUS_LN0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dummy', ctypes.c_uint32, 32),
    ]


class REG_DKL_TX_PMD_LANE_SUS_LN0(ctypes.Union):
    value = 0
    offset = 0

    Dummy = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_TX_PMD_LANE_SUS_LN0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_TX_PMD_LANE_SUS_LN0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_TX_PMD_LANE_SUS_LN1:
    DKL_TX_PMD_LANE_SUS_LN1 = 0xD00


class _DKL_TX_PMD_LANE_SUS_LN1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dummy', ctypes.c_uint32, 32),
    ]


class REG_DKL_TX_PMD_LANE_SUS_LN1(ctypes.Union):
    value = 0
    offset = 0

    Dummy = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_TX_PMD_LANE_SUS_LN1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_TX_PMD_LANE_SUS_LN1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_FBDIV_INTGR_7_0(Enum):
    CFG_I_FBDIV_INTGR_7_0_CFG_I_FBDIV_INTGR_7_0_DEFAULTRESET = 0x82


class ENUM_CFG_I_FBPREDIV_3_0(Enum):
    CFG_I_FBPREDIV_3_0_CFG_I_FBPREDIV_3_0_DEFAULTRESET = 0x2


class ENUM_CFG_I_PROP_COEFF_3_0(Enum):
    CFG_I_PROP_COEFF_3_0_CFG_I_PROP_COEFF_3_0_DEFAULTRESET = 0x3


class ENUM_CFG_I_INT_COEFF_4_0(Enum):
    CFG_I_INT_COEFF_4_0_CFG_I_INT_COEFF_4_0_DEFAULTRESET = 0x7


class ENUM_CFG_I_GAINCTRL_2_0(Enum):
    CFG_I_GAINCTRL_2_0_CFG_I_GAINCTRL_2_0_DEFAULTRESET = 0x1


class ENUM_CFG_I_DIVRETIMEREN(Enum):
    CFG_I_DIVRETIMEREN_CFG_I_DIVRETIMEREN_DEFAULTRESET = 0x0


class ENUM_CFG_I_AFC_STARTUP_2_0(Enum):
    CFG_I_AFC_STARTUP_2_0_CFG_I_AFC_STARTUP_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_EARLYLOCK_CRITERIA_1_0(Enum):
    CFG_I_EARLYLOCK_CRITERIA_1_0_CFG_I_EARLYLOCK_CRITERIA_1_0_DEFAULTRESET = 0x3


class ENUM_CFG_I_TRUELOCK_CRITERIA_1_0(Enum):
    CFG_I_TRUELOCK_CRITERIA_1_0_CFG_I_TRUELOCK_CRITERIA_1_0_DEFAULTRESET = 0x1


class OFFSET_DKLP_PLL0_DIV0:
    DKLP_PLL0_DIV0 = 0x180


class _DKLP_PLL0_DIV0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Fbdiv_Intgr_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbprediv_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Prop_Coeff_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Int_Coeff_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Gainctrl_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Divretimeren', ctypes.c_uint32, 1),
        ('Cfg_I_Afc_Startup_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Earlylock_Criteria_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Truelock_Criteria_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKLP_PLL0_DIV0(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Fbdiv_Intgr_7_0 = 0  # bit 0 to 8
    Cfg_I_Fbprediv_3_0 = 0  # bit 8 to 12
    Cfg_I_Prop_Coeff_3_0 = 0  # bit 12 to 16
    Cfg_I_Int_Coeff_4_0 = 0  # bit 16 to 21
    Cfg_I_Gainctrl_2_0 = 0  # bit 21 to 24
    Cfg_I_Divretimeren = 0  # bit 24 to 25
    Cfg_I_Afc_Startup_2_0 = 0  # bit 25 to 28
    Cfg_I_Earlylock_Criteria_1_0 = 0  # bit 28 to 30
    Cfg_I_Truelock_Criteria_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_DIV0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_DIV0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_TDCTARGETCNT_7_0(Enum):
    CFG_I_TDCTARGETCNT_7_0_CFG_I_TDCTARGETCNT_7_0_DEFAULTRESET = 0x11


class ENUM_CFG_I_LOCKTHRESH_3_0(Enum):
    CFG_I_LOCKTHRESH_3_0_CFG_I_LOCKTHRESH_3_0_DEFAULTRESET = 0x5


class ENUM_CFG_I_DCODITHER_CONFIG(Enum):
    CFG_I_DCODITHER_CONFIG_CFG_I_DCODITHER_CONFIG_DEFAULTRESET = 0x0


class ENUM_CFG_I_BIASCAL_EN_H(Enum):
    CFG_I_BIASCAL_EN_H_CFG_I_BIASCAL_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_BIAS_FILTER_EN(Enum):
    CFG_I_BIAS_FILTER_EN_CFG_I_BIAS_FILTER_EN_DEFAULTRESET = 0x1


class ENUM_CFG_I_BIASFILTER_EN_DELAY(Enum):
    CFG_I_BIASFILTER_EN_DELAY_CFG_I_BIASFILTER_EN_DELAY_DEFAULTRESET = 0x1


class ENUM_CFG_I_IREFTRIM_4_0(Enum):
    CFG_I_IREFTRIM_4_0_CFG_I_IREFTRIM_4_0_DEFAULTRESET = 0x1C


class ENUM_CFG_I_BIAS_R_PROGRAMABILITY_1_0(Enum):
    CFG_I_BIAS_R_PROGRAMABILITY_1_0_CFG_I_BIAS_R_PROGRAMABILITY_1_0_DEFAULTRESET = 0x2


class ENUM_CFG_I_FASTLOCK_INTERNAL_RESET(Enum):
    CFG_I_FASTLOCK_INTERNAL_RESET_CFG_I_FASTLOCK_INTERNAL_RESET_DEFAULTRESET = 0x1


class ENUM_CFG_I_CTRIM_4_0(Enum):
    CFG_I_CTRIM_4_0_CFG_I_CTRIM_4_0_DEFAULTRESET = 0xC


class ENUM_CFG_I_BIAS_CALIB_STEPSIZE_1_0(Enum):
    CFG_I_BIAS_CALIB_STEPSIZE_1_0_CFG_I_BIAS_CALIB_STEPSIZE_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BW_AMPMEAS_WINDOW(Enum):
    CFG_I_BW_AMPMEAS_WINDOW_CFG_I_BW_AMPMEAS_WINDOW_DEFAULTRESET = 0x0


class OFFSET_DKLP_PLL0_DIV1:
    DKLP_PLL0_DIV1 = 0x184


class _DKLP_PLL0_DIV1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Tdctargetcnt_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Lockthresh_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Dcodither_Config', ctypes.c_uint32, 1),
        ('Cfg_I_Biascal_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Bias_Filter_En', ctypes.c_uint32, 1),
        ('Cfg_I_Biasfilter_En_Delay', ctypes.c_uint32, 1),
        ('Cfg_I_Ireftrim_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Bias_R_Programability_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Fastlock_Internal_Reset', ctypes.c_uint32, 1),
        ('Cfg_I_Ctrim_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Bias_Calib_Stepsize_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Bw_Ampmeas_Window', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL0_DIV1(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Tdctargetcnt_7_0 = 0  # bit 0 to 8
    Cfg_I_Lockthresh_3_0 = 0  # bit 8 to 12
    Cfg_I_Dcodither_Config = 0  # bit 12 to 13
    Cfg_I_Biascal_En_H = 0  # bit 13 to 14
    Cfg_I_Bias_Filter_En = 0  # bit 14 to 15
    Cfg_I_Biasfilter_En_Delay = 0  # bit 15 to 16
    Cfg_I_Ireftrim_4_0 = 0  # bit 16 to 21
    Cfg_I_Bias_R_Programability_1_0 = 0  # bit 21 to 23
    Cfg_I_Fastlock_Internal_Reset = 0  # bit 23 to 24
    Cfg_I_Ctrim_4_0 = 0  # bit 24 to 29
    Cfg_I_Bias_Calib_Stepsize_1_0 = 0  # bit 29 to 31
    Cfg_I_Bw_Ampmeas_Window = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_DIV1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_DIV1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_TDC_OFFSET_LOCK_1_0(Enum):
    CFG_I_TDC_OFFSET_LOCK_1_0_CFG_I_TDC_OFFSET_LOCK_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BBTHRESH1_2_0(Enum):
    CFG_I_BBTHRESH1_2_0_CFG_I_BBTHRESH1_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BBTHRESH2_2_0(Enum):
    CFG_I_BBTHRESH2_2_0_CFG_I_BBTHRESH2_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_DCOAMPOVRDEN_H(Enum):
    CFG_I_DCOAMPOVRDEN_H_CFG_I_DCOAMPOVRDEN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_DCOAMP_3_0(Enum):
    CFG_I_DCOAMP_3_0_CFG_I_DCOAMP_3_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BW_LOWERBOUND_2_0(Enum):
    CFG_I_BW_LOWERBOUND_2_0_CFG_I_BW_LOWERBOUND_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BW_UPPERBOUND_2_0(Enum):
    CFG_I_BW_UPPERBOUND_2_0_CFG_I_BW_UPPERBOUND_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BW_MODE_1_0(Enum):
    CFG_I_BW_MODE_1_0_CFG_I_BW_MODE_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_FT_MODE_SEL_2_0(Enum):
    CFG_I_FT_MODE_SEL_2_0_CFG_I_FT_MODE_SEL_2_0_DEFAULTRESET = 0x2


class ENUM_CFG_I_BWPHASE_4_0(Enum):
    CFG_I_BWPHASE_4_0_CFG_I_BWPHASE_4_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_PLLLOCK_SEL_1_0(Enum):
    CFG_I_PLLLOCK_SEL_1_0_CFG_I_PLLLOCK_SEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_AFC_DIVRATIO(Enum):
    CFG_I_AFC_DIVRATIO_CFG_I_AFC_DIVRATIO_DEFAULTRESET = 0x0


class OFFSET_DKLP_PLL0_LF:
    DKLP_PLL0_LF = 0x188


class _DKLP_PLL0_LF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Tdc_Offset_Lock_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Bbthresh1_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bbthresh2_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Dcoampovrden_H', ctypes.c_uint32, 1),
        ('Cfg_I_Dcoamp_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Bw_Lowerbound_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bw_Upperbound_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bw_Mode_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Ft_Mode_Sel_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bwphase_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Plllock_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Afc_Divratio', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL0_LF(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Tdc_Offset_Lock_1_0 = 0  # bit 0 to 2
    Cfg_I_Bbthresh1_2_0 = 0  # bit 2 to 5
    Cfg_I_Bbthresh2_2_0 = 0  # bit 5 to 8
    Cfg_I_Dcoampovrden_H = 0  # bit 8 to 9
    Cfg_I_Dcoamp_3_0 = 0  # bit 9 to 13
    Cfg_I_Bw_Lowerbound_2_0 = 0  # bit 13 to 16
    Cfg_I_Bw_Upperbound_2_0 = 0  # bit 16 to 19
    Cfg_I_Bw_Mode_1_0 = 0  # bit 19 to 21
    Cfg_I_Ft_Mode_Sel_2_0 = 0  # bit 21 to 24
    Cfg_I_Bwphase_4_0 = 0  # bit 24 to 29
    Cfg_I_Plllock_Sel_1_0 = 0  # bit 29 to 31
    Cfg_I_Afc_Divratio = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_LF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_LF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_INIT_CSELAFC_7_0(Enum):
    CFG_I_INIT_CSELAFC_7_0_CFG_I_INIT_CSELAFC_7_0_DEFAULTRESET = 0x6A


class ENUM_CFG_I_MAX_CSELAFC_7_0(Enum):
    CFG_I_MAX_CSELAFC_7_0_CFG_I_MAX_CSELAFC_7_0_DEFAULTRESET = 0x3F


class ENUM_CFG_I_FLLAFC_LOCKCNT_2_0(Enum):
    CFG_I_FLLAFC_LOCKCNT_2_0_CFG_I_FLLAFC_LOCKCNT_2_0_DEFAULTRESET = 0x4


class ENUM_CFG_I_FLLAFC_GAIN_3_0(Enum):
    CFG_I_FLLAFC_GAIN_3_0_CFG_I_FLLAFC_GAIN_3_0_DEFAULTRESET = 0x8


class ENUM_CFG_I_FASTLOCK_EN_H(Enum):
    CFG_I_FASTLOCK_EN_H_CFG_I_FASTLOCK_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_BB_GAIN1_2_0(Enum):
    CFG_I_BB_GAIN1_2_0_CFG_I_BB_GAIN1_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BB_GAIN2_2_0(Enum):
    CFG_I_BB_GAIN2_2_0_CFG_I_BB_GAIN2_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_CML2CMOSBONUS_1_0(Enum):
    CFG_I_CML2CMOSBONUS_1_0_CFG_I_CML2CMOSBONUS_1_0_DEFAULTRESET = 0x0


class OFFSET_DKLP_PLL0_FRAC_LOCK:
    DKLP_PLL0_FRAC_LOCK = 0x18C


class _DKLP_PLL0_FRAC_LOCK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Init_Cselafc_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Max_Cselafc_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fllafc_Lockcnt_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Fllafc_Gain_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Fastlock_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Bb_Gain1_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bb_Gain2_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Cml2Cmosbonus_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKLP_PLL0_FRAC_LOCK(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Init_Cselafc_7_0 = 0  # bit 0 to 8
    Cfg_I_Max_Cselafc_7_0 = 0  # bit 8 to 16
    Cfg_I_Fllafc_Lockcnt_2_0 = 0  # bit 16 to 19
    Cfg_I_Fllafc_Gain_3_0 = 0  # bit 19 to 23
    Cfg_I_Fastlock_En_H = 0  # bit 23 to 24
    Cfg_I_Bb_Gain1_2_0 = 0  # bit 24 to 27
    Cfg_I_Bb_Gain2_2_0 = 0  # bit 27 to 30
    Cfg_I_Cml2Cmosbonus_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_FRAC_LOCK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_FRAC_LOCK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_INIT_DCOAMP_5_0(Enum):
    CFG_I_INIT_DCOAMP_5_0_CFG_I_INIT_DCOAMP_5_0_DEFAULTRESET = 0x3F


class ENUM_CFG_I_BIAS_GB_SEL_1_0(Enum):
    CFG_I_BIAS_GB_SEL_1_0_CFG_I_BIAS_GB_SEL_1_0_DEFAULTRESET = 0x3


class ENUM_CFG_I_SSCFLLEN_H(Enum):
    CFG_I_SSCFLLEN_H_CFG_I_SSCFLLEN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_SSCEN_H(Enum):
    CFG_I_SSCEN_H_CFG_I_SSCEN_H_DEFAULTRESET = 0x1


class ENUM_CFG_I_SSC_OPENLOOP_EN_H(Enum):
    CFG_I_SSC_OPENLOOP_EN_H_CFG_I_SSC_OPENLOOP_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_SSCSTEPNUM_2_0(Enum):
    CFG_I_SSCSTEPNUM_2_0_CFG_I_SSCSTEPNUM_2_0_DEFAULTRESET = 0x4


class ENUM_CFG_I_SSCFLL_UPDATE_SEL_1_0(Enum):
    CFG_I_SSCFLL_UPDATE_SEL_1_0_CFG_I_SSCFLL_UPDATE_SEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_SSCSTEPLENGTH_7_0(Enum):
    CFG_I_SSCSTEPLENGTH_7_0_CFG_I_SSCSTEPLENGTH_7_0_DEFAULTRESET = 0x13


class ENUM_CFG_I_SSCINJ_EN_H(Enum):
    CFG_I_SSCINJ_EN_H_CFG_I_SSCINJ_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_SSCINJ_ADAPT_EN_H(Enum):
    CFG_I_SSCINJ_ADAPT_EN_H_CFG_I_SSCINJ_ADAPT_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_SSCSTEPNUM_OFFSET_2_0(Enum):
    CFG_I_SSCSTEPNUM_OFFSET_2_0_CFG_I_SSCSTEPNUM_OFFSET_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_IREF_NDIVRATIO_2_0(Enum):
    CFG_I_IREF_NDIVRATIO_2_0_CFG_I_IREF_NDIVRATIO_2_0_DEFAULTRESET = 0x2


class OFFSET_DKLP_PLL0_SSC:
    DKLP_PLL0_SSC = 0x190


class _DKLP_PLL0_SSC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Init_Dcoamp_5_0', ctypes.c_uint32, 6),
        ('Cfg_I_Bias_Gb_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Sscfllen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Ssc_Openloop_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscstepnum_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Sscfll_Update_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Sscsteplength_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Sscinj_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscinj_Adapt_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscstepnum_Offset_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Iref_Ndivratio_2_0', ctypes.c_uint32, 3),
    ]


class REG_DKLP_PLL0_SSC(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Init_Dcoamp_5_0 = 0  # bit 0 to 6
    Cfg_I_Bias_Gb_Sel_1_0 = 0  # bit 6 to 8
    Cfg_I_Sscfllen_H = 0  # bit 8 to 9
    Cfg_I_Sscen_H = 0  # bit 9 to 10
    Cfg_I_Ssc_Openloop_En_H = 0  # bit 10 to 11
    Cfg_I_Sscstepnum_2_0 = 0  # bit 11 to 14
    Cfg_I_Sscfll_Update_Sel_1_0 = 0  # bit 14 to 16
    Cfg_I_Sscsteplength_7_0 = 0  # bit 16 to 24
    Cfg_I_Sscinj_En_H = 0  # bit 24 to 25
    Cfg_I_Sscinj_Adapt_En_H = 0  # bit 25 to 26
    Cfg_I_Sscstepnum_Offset_2_0 = 0  # bit 26 to 29
    Cfg_I_Iref_Ndivratio_2_0 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_SSC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_SSC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_SSCINJ_STEPSIZE_7_0(Enum):
    CFG_I_SSCINJ_STEPSIZE_7_0_CFG_I_SSCINJ_STEPSIZE_7_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_FBDIV_FRAC_7_0(Enum):
    CFG_I_FBDIV_FRAC_7_0_CFG_I_FBDIV_FRAC_7_0_DEFAULTRESET = 0x55


class ENUM_CFG_I_FBDIV_FRAC_15_8(Enum):
    CFG_I_FBDIV_FRAC_15_8_CFG_I_FBDIV_FRAC_15_8_DEFAULTRESET = 0x55


class ENUM_CFG_I_FBDIV_FRAC_21_16(Enum):
    CFG_I_FBDIV_FRAC_21_16_CFG_I_FBDIV_FRAC_21_16_DEFAULTRESET = 0xD


class ENUM_CFG_I_FRACNEN_H(Enum):
    CFG_I_FRACNEN_H_CFG_I_FRACNEN_H_DEFAULTRESET = 0x1


class ENUM_CFG_I_TDC_FINE_RES(Enum):
    CFG_I_TDC_FINE_RES_CFG_I_TDC_FINE_RES_DEFAULTRESET = 0x1


class OFFSET_DKLP_PLL0_BIAS:
    DKLP_PLL0_BIAS = 0x194


class _DKLP_PLL0_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Sscinj_Stepsize_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_15_8', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_21_16', ctypes.c_uint32, 6),
        ('Cfg_I_Fracnen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Tdc_Fine_Res', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL0_BIAS(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Sscinj_Stepsize_7_0 = 0  # bit 0 to 8
    Cfg_I_Fbdiv_Frac_7_0 = 0  # bit 8 to 16
    Cfg_I_Fbdiv_Frac_15_8 = 0  # bit 16 to 24
    Cfg_I_Fbdiv_Frac_21_16 = 0  # bit 24 to 30
    Cfg_I_Fracnen_H = 0  # bit 30 to 31
    Cfg_I_Tdc_Fine_Res = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_FEEDFWRDGAIN_7_0(Enum):
    CFG_I_FEEDFWRDGAIN_7_0_CFG_I_FEEDFWRDGAIN_7_0_DEFAULTRESET = 0x1C


class ENUM_CFG_I_SSCSTEPSIZE_7_0(Enum):
    CFG_I_SSCSTEPSIZE_7_0_CFG_I_SSCSTEPSIZE_7_0_DEFAULTRESET = 0x13


class ENUM_CFG_I_DCOCOARSE_7_0(Enum):
    CFG_I_DCOCOARSE_7_0_CFG_I_DCOCOARSE_7_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_TRIBUFCTRLEXT_4_0(Enum):
    CFG_I_TRIBUFCTRLEXT_4_0_CFG_I_TRIBUFCTRLEXT_4_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_CLOADCTRLLEXT_4_2(Enum):
    CFG_I_CLOADCTRLLEXT_4_2_CFG_I_CLOADCTRLLEXT_4_2_DEFAULTRESET = 0x0


class OFFSET_DKLP_PLL0_TDC_COLDST_BIAS:
    DKLP_PLL0_TDC_COLDST_BIAS = 0x198


class _DKLP_PLL0_TDC_COLDST_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Feedfwrdgain_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Sscstepsize_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Dcocoarse_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Tribufctrlext_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Cloadctrllext_4_2', ctypes.c_uint32, 3),
    ]


class REG_DKLP_PLL0_TDC_COLDST_BIAS(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Feedfwrdgain_7_0 = 0  # bit 0 to 8
    Cfg_I_Sscstepsize_7_0 = 0  # bit 8 to 16
    Cfg_I_Dcocoarse_7_0 = 0  # bit 16 to 24
    Cfg_I_Tribufctrlext_4_0 = 0  # bit 24 to 29
    Cfg_I_Cloadctrllext_4_2 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_TDC_COLDST_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_TDC_COLDST_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_DIV0:
    DKLP_PLL1_DIV0 = 0x200


class _DKLP_PLL1_DIV0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Fbdiv_Intgr_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbprediv_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Prop_Coeff_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Int_Coeff_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Gainctrl_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Divretimeren', ctypes.c_uint32, 1),
        ('Cfg_I_Afc_Startup_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Earlylock_Criteria_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Truelock_Criteria_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKLP_PLL1_DIV0(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Fbdiv_Intgr_7_0 = 0  # bit 0 to 8
    Cfg_I_Fbprediv_3_0 = 0  # bit 8 to 12
    Cfg_I_Prop_Coeff_3_0 = 0  # bit 12 to 16
    Cfg_I_Int_Coeff_4_0 = 0  # bit 16 to 21
    Cfg_I_Gainctrl_2_0 = 0  # bit 21 to 24
    Cfg_I_Divretimeren = 0  # bit 24 to 25
    Cfg_I_Afc_Startup_2_0 = 0  # bit 25 to 28
    Cfg_I_Earlylock_Criteria_1_0 = 0  # bit 28 to 30
    Cfg_I_Truelock_Criteria_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_DIV0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_DIV0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_DIV1:
    DKLP_PLL1_DIV1 = 0x204


class _DKLP_PLL1_DIV1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Tdctargetcnt_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Lockthresh_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Dcodither_Config', ctypes.c_uint32, 1),
        ('Cfg_I_Biascal_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Bias_Filter_En', ctypes.c_uint32, 1),
        ('Cfg_I_Biasfilter_En_Delay', ctypes.c_uint32, 1),
        ('Cfg_I_Ireftrim_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Bias_R_Programability_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Fastlock_Internal_Reset', ctypes.c_uint32, 1),
        ('Cfg_I_Ctrim_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Bias_Calib_Stepsize_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Bw_Ampmeas_Window', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL1_DIV1(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Tdctargetcnt_7_0 = 0  # bit 0 to 8
    Cfg_I_Lockthresh_3_0 = 0  # bit 8 to 12
    Cfg_I_Dcodither_Config = 0  # bit 12 to 13
    Cfg_I_Biascal_En_H = 0  # bit 13 to 14
    Cfg_I_Bias_Filter_En = 0  # bit 14 to 15
    Cfg_I_Biasfilter_En_Delay = 0  # bit 15 to 16
    Cfg_I_Ireftrim_4_0 = 0  # bit 16 to 21
    Cfg_I_Bias_R_Programability_1_0 = 0  # bit 21 to 23
    Cfg_I_Fastlock_Internal_Reset = 0  # bit 23 to 24
    Cfg_I_Ctrim_4_0 = 0  # bit 24 to 29
    Cfg_I_Bias_Calib_Stepsize_1_0 = 0  # bit 29 to 31
    Cfg_I_Bw_Ampmeas_Window = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_DIV1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_DIV1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_LF:
    DKLP_PLL1_LF = 0x208


class _DKLP_PLL1_LF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Tdc_Offset_Lock_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Bbthresh1_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bbthresh2_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Dcoampovrden_H', ctypes.c_uint32, 1),
        ('Cfg_I_Dcoamp_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Bw_Lowerbound_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bw_Upperbound_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bw_Mode_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Ft_Mode_Sel_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bwphase_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Plllock_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Afc_Divratio', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL1_LF(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Tdc_Offset_Lock_1_0 = 0  # bit 0 to 2
    Cfg_I_Bbthresh1_2_0 = 0  # bit 2 to 5
    Cfg_I_Bbthresh2_2_0 = 0  # bit 5 to 8
    Cfg_I_Dcoampovrden_H = 0  # bit 8 to 9
    Cfg_I_Dcoamp_3_0 = 0  # bit 9 to 13
    Cfg_I_Bw_Lowerbound_2_0 = 0  # bit 13 to 16
    Cfg_I_Bw_Upperbound_2_0 = 0  # bit 16 to 19
    Cfg_I_Bw_Mode_1_0 = 0  # bit 19 to 21
    Cfg_I_Ft_Mode_Sel_2_0 = 0  # bit 21 to 24
    Cfg_I_Bwphase_4_0 = 0  # bit 24 to 29
    Cfg_I_Plllock_Sel_1_0 = 0  # bit 29 to 31
    Cfg_I_Afc_Divratio = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_LF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_LF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_FRAC_LOCK:
    DKLP_PLL1_FRAC_LOCK = 0x20C


class _DKLP_PLL1_FRAC_LOCK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Init_Cselafc_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Max_Cselafc_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fllafc_Lockcnt_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Fllafc_Gain_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Fastlock_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Bb_Gain1_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bb_Gain2_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Cml2Cmosbonus_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKLP_PLL1_FRAC_LOCK(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Init_Cselafc_7_0 = 0  # bit 0 to 8
    Cfg_I_Max_Cselafc_7_0 = 0  # bit 8 to 16
    Cfg_I_Fllafc_Lockcnt_2_0 = 0  # bit 16 to 19
    Cfg_I_Fllafc_Gain_3_0 = 0  # bit 19 to 23
    Cfg_I_Fastlock_En_H = 0  # bit 23 to 24
    Cfg_I_Bb_Gain1_2_0 = 0  # bit 24 to 27
    Cfg_I_Bb_Gain2_2_0 = 0  # bit 27 to 30
    Cfg_I_Cml2Cmosbonus_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_FRAC_LOCK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_FRAC_LOCK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_SSC:
    DKLP_PLL1_SSC = 0x210


class _DKLP_PLL1_SSC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Init_Dcoamp_5_0', ctypes.c_uint32, 6),
        ('Cfg_I_Bias_Gb_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Sscfllen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Ssc_Openloop_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscstepnum_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Sscfll_Update_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Sscsteplength_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Sscinj_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscinj_Adapt_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscstepnum_Offset_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Iref_Ndivratio_2_0', ctypes.c_uint32, 3),
    ]


class REG_DKLP_PLL1_SSC(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Init_Dcoamp_5_0 = 0  # bit 0 to 6
    Cfg_I_Bias_Gb_Sel_1_0 = 0  # bit 6 to 8
    Cfg_I_Sscfllen_H = 0  # bit 8 to 9
    Cfg_I_Sscen_H = 0  # bit 9 to 10
    Cfg_I_Ssc_Openloop_En_H = 0  # bit 10 to 11
    Cfg_I_Sscstepnum_2_0 = 0  # bit 11 to 14
    Cfg_I_Sscfll_Update_Sel_1_0 = 0  # bit 14 to 16
    Cfg_I_Sscsteplength_7_0 = 0  # bit 16 to 24
    Cfg_I_Sscinj_En_H = 0  # bit 24 to 25
    Cfg_I_Sscinj_Adapt_En_H = 0  # bit 25 to 26
    Cfg_I_Sscstepnum_Offset_2_0 = 0  # bit 26 to 29
    Cfg_I_Iref_Ndivratio_2_0 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_SSC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_SSC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_BIAS:
    DKLP_PLL1_BIAS = 0x214


class _DKLP_PLL1_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Sscinj_Stepsize_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_15_8', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_21_16', ctypes.c_uint32, 6),
        ('Cfg_I_Fracnen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Tdc_Fine_Res', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL1_BIAS(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Sscinj_Stepsize_7_0 = 0  # bit 0 to 8
    Cfg_I_Fbdiv_Frac_7_0 = 0  # bit 8 to 16
    Cfg_I_Fbdiv_Frac_15_8 = 0  # bit 16 to 24
    Cfg_I_Fbdiv_Frac_21_16 = 0  # bit 24 to 30
    Cfg_I_Fracnen_H = 0  # bit 30 to 31
    Cfg_I_Tdc_Fine_Res = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_TDC_COLDST_BIAS:
    DKLP_PLL1_TDC_COLDST_BIAS = 0x218


class _DKLP_PLL1_TDC_COLDST_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Feedfwrdgain_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Sscstepsize_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Dcocoarse_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Tribufctrlext_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Cloadctrllext_4_2', ctypes.c_uint32, 3),
    ]


class REG_DKLP_PLL1_TDC_COLDST_BIAS(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Feedfwrdgain_7_0 = 0  # bit 0 to 8
    Cfg_I_Sscstepsize_7_0 = 0  # bit 8 to 16
    Cfg_I_Dcocoarse_7_0 = 0  # bit 16 to 24
    Cfg_I_Tribufctrlext_4_0 = 0  # bit 24 to 29
    Cfg_I_Cloadctrllext_4_2 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_TDC_COLDST_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_TDC_COLDST_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_OD_CLKTOP1_HSDIV_EN_H(Enum):
    CFG_OD_CLKTOP1_HSDIV_EN_H_CFG_OD_CLKTOP1_HSDIV_EN_H_DEFAULTRESET = 0x1


class ENUM_CFG_RESERVED500(Enum):
    CFG_RESERVED500_CFG_RESERVED500_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_DSDIV_EN_H(Enum):
    CFG_OD_CLKTOP1_DSDIV_EN_H_CFG_OD_CLKTOP1_DSDIV_EN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_H_OVRD(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_H_OVRD_CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_H_OVRD_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_H_OVRD(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_H_OVRD_CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_H_OVRD_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_DED_H_OVRD(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_DED_H_OVRD_CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_DED_H_OVRD_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_DED_H_OVRD(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_DED_H_OVRD_CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_DED_H_OVRD_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_OVERRIDEEN(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_OVERRIDEEN_CFG_OD_CLKTOP1_TLINEDRV_OVERRIDEEN_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_DSDIV_DIVRATIO_3_0(Enum):
    CFG_OD_CLKTOP1_DSDIV_DIVRATIO_3_0_CFG_OD_CLKTOP1_DSDIV_DIVRATIO_3_0_DEFAULTRESET = 0xA


class ENUM_CFG_OD_CLKTOP1_HSDIV_DIVRATIO_1_0(Enum):
    CFG_OD_CLKTOP1_HSDIV_DIVRATIO_1_0_CFG_OD_CLKTOP1_HSDIV_DIVRATIO_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_CLKSEL_1_0(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_CLKSEL_1_0_CFG_OD_CLKTOP1_TLINEDRV_CLKSEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLK_INPUTSEL(Enum):
    CFG_OD_CLKTOP1_CORECLK_INPUTSEL_CFG_OD_CLKTOP1_CORECLK_INPUTSEL_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED503(Enum):
    CFG_RESERVED503_CFG_RESERVED503_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_OUTCLK_BYPASSEN_H(Enum):
    CFG_OD_CLKTOP1_OUTCLK_BYPASSEN_H_CFG_OD_CLKTOP1_OUTCLK_BYPASSEN_H_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED502(Enum):
    CFG_RESERVED502_CFG_RESERVED502_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CLKTOP1_VHFCLK_TESTEN_H_1_0(Enum):
    CFG_OD_CLKTOP1_CLKTOP1_VHFCLK_TESTEN_H_1_0_CFG_OD_CLKTOP1_CLKTOP1_VHFCLK_TESTEN_H_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED501(Enum):
    CFG_RESERVED501_CFG_RESERVED501_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CLK2OBS_EN_H(Enum):
    CFG_OD_CLKTOP1_CLK2OBS_EN_H_CFG_OD_CLKTOP1_CLK2OBS_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CLKOBS_MUXSEL_1_0(Enum):
    CFG_OD_CLKTOP1_CLKOBS_MUXSEL_1_0_CFG_OD_CLKTOP1_CLKOBS_MUXSEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED504(Enum):
    CFG_RESERVED504_CFG_RESERVED504_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD0:
    DKLP_CMN_ANA_CMN_ANA_DWORD0 = 0x0C0


class _DKLP_CMN_ANA_CMN_ANA_DWORD0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Od_Clktop1_Hsdiv_En_H', ctypes.c_uint32, 1),
        ('Cfg_Reserved500', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Dsdiv_En_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Tlinedrv_Enright_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Tlinedrv_Enleft_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Tlinedrv_Enright_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Tlinedrv_Enleft_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Tlinedrv_Overrideen', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Dsdiv_Divratio_3_0', ctypes.c_uint32, 4),
        ('Cfg_Od_Clktop1_Hsdiv_Divratio_1_0', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop1_Tlinedrv_Clksel_1_0', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop1_Coreclk_Inputsel', ctypes.c_uint32, 1),
        ('Cfg_Reserved503', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Outclk_Bypassen_H', ctypes.c_uint32, 1),
        ('Cfg_Reserved502', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Clktop1_Vhfclk_Testen_H_1_0', ctypes.c_uint32, 2),
        ('Cfg_Reserved501', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop1_Clk2Obs_En_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Clkobs_Muxsel_1_0', ctypes.c_uint32, 2),
        ('Cfg_Reserved504', ctypes.c_uint32, 5),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD0(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Od_Clktop1_Hsdiv_En_H = 0  # bit 0 to 1
    Cfg_Reserved500 = 0  # bit 1 to 2
    Cfg_Od_Clktop1_Dsdiv_En_H = 0  # bit 2 to 3
    Cfg_Od_Clktop1_Tlinedrv_Enright_H_Ovrd = 0  # bit 3 to 4
    Cfg_Od_Clktop1_Tlinedrv_Enleft_H_Ovrd = 0  # bit 4 to 5
    Cfg_Od_Clktop1_Tlinedrv_Enright_Ded_H_Ovrd = 0  # bit 5 to 6
    Cfg_Od_Clktop1_Tlinedrv_Enleft_Ded_H_Ovrd = 0  # bit 6 to 7
    Cfg_Od_Clktop1_Tlinedrv_Overrideen = 0  # bit 7 to 8
    Cfg_Od_Clktop1_Dsdiv_Divratio_3_0 = 0  # bit 8 to 12
    Cfg_Od_Clktop1_Hsdiv_Divratio_1_0 = 0  # bit 12 to 14
    Cfg_Od_Clktop1_Tlinedrv_Clksel_1_0 = 0  # bit 14 to 16
    Cfg_Od_Clktop1_Coreclk_Inputsel = 0  # bit 16 to 17
    Cfg_Reserved503 = 0  # bit 17 to 18
    Cfg_Od_Clktop1_Outclk_Bypassen_H = 0  # bit 18 to 19
    Cfg_Reserved502 = 0  # bit 19 to 20
    Cfg_Od_Clktop1_Clktop1_Vhfclk_Testen_H_1_0 = 0  # bit 20 to 22
    Cfg_Reserved501 = 0  # bit 22 to 24
    Cfg_Od_Clktop1_Clk2Obs_En_H = 0  # bit 24 to 25
    Cfg_Od_Clktop1_Clkobs_Muxsel_1_0 = 0  # bit 25 to 27
    Cfg_Reserved504 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_RESERVED507(Enum):
    CFG_RESERVED507_CFG_RESERVED507_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKA_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKA_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKA_DIVRETIMEREN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_CORECLKA_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKA_BYPASS_CFG_OD_CLKTOP1_CORECLKA_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED506(Enum):
    CFG_RESERVED506_CFG_RESERVED506_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKB_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKB_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKB_DIVRETIMEREN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_CORECLKB_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKB_BYPASS_CFG_OD_CLKTOP1_CORECLKB_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_ON_PLL12CORECLKA_SELECT(Enum):
    CFG_ON_PLL12CORECLKA_SELECT_CFG_ON_PLL12CORECLKA_SELECT_DEFAULTRESET = 0x0


class ENUM_CFG_ON_PLL12CORECLKD_SELECT(Enum):
    CFG_ON_PLL12CORECLKD_SELECT_CFG_ON_PLL12CORECLKD_SELECT_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKA_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP1_CORECLKA_DIVRATIO_7_0_CFG_OD_CLKTOP1_CORECLKA_DIVRATIO_7_0_DEFAULTRESET = 0x14


class ENUM_CFG_OD_CLKTOP1_CORECLKB_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP1_CORECLKB_DIVRATIO_7_0_CFG_OD_CLKTOP1_CORECLKB_DIVRATIO_7_0_DEFAULTRESET = 0x8


class ENUM_CFG_RESERVED510(Enum):
    CFG_RESERVED510_CFG_RESERVED510_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKC_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKC_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKC_DIVRETIMEREN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_CORECLKC_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKC_BYPASS_CFG_OD_CLKTOP1_CORECLKC_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED509(Enum):
    CFG_RESERVED509_CFG_RESERVED509_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKD_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKD_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKD_DIVRETIMEREN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_CORECLKD_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKD_BYPASS_CFG_OD_CLKTOP1_CORECLKD_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED508(Enum):
    CFG_RESERVED508_CFG_RESERVED508_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD1:
    DKLP_CMN_ANA_CMN_ANA_DWORD1 = 0x0C4


class _DKLP_CMN_ANA_CMN_ANA_DWORD1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Reserved507', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclka_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclka_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved506', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkb_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkb_Bypass', ctypes.c_uint32, 1),
        ('Cfg_On_Pll12Coreclka_Select', ctypes.c_uint32, 1),
        ('Cfg_On_Pll12Coreclkd_Select', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclka_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Od_Clktop1_Coreclkb_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Reserved510', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkc_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkc_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved509', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkd_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkd_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved508', ctypes.c_uint32, 2),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD1(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Reserved507 = 0  # bit 0 to 1
    Cfg_Od_Clktop1_Coreclka_Divretimeren_H = 0  # bit 1 to 2
    Cfg_Od_Clktop1_Coreclka_Bypass = 0  # bit 2 to 3
    Cfg_Reserved506 = 0  # bit 3 to 4
    Cfg_Od_Clktop1_Coreclkb_Divretimeren_H = 0  # bit 4 to 5
    Cfg_Od_Clktop1_Coreclkb_Bypass = 0  # bit 5 to 6
    Cfg_On_Pll12Coreclka_Select = 0  # bit 6 to 7
    Cfg_On_Pll12Coreclkd_Select = 0  # bit 7 to 8
    Cfg_Od_Clktop1_Coreclka_Divratio_7_0 = 0  # bit 8 to 16
    Cfg_Od_Clktop1_Coreclkb_Divratio_7_0 = 0  # bit 16 to 24
    Cfg_Reserved510 = 0  # bit 24 to 25
    Cfg_Od_Clktop1_Coreclkc_Divretimeren_H = 0  # bit 25 to 26
    Cfg_Od_Clktop1_Coreclkc_Bypass = 0  # bit 26 to 27
    Cfg_Reserved509 = 0  # bit 27 to 28
    Cfg_Od_Clktop1_Coreclkd_Divretimeren_H = 0  # bit 28 to 29
    Cfg_Od_Clktop1_Coreclkd_Bypass = 0  # bit 29 to 30
    Cfg_Reserved508 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_OD_CLKTOP1_CORECLKC_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP1_CORECLKC_DIVRATIO_7_0_CFG_OD_CLKTOP1_CORECLKC_DIVRATIO_7_0_DEFAULTRESET = 0xA


class ENUM_CFG_OD_CLKTOP1_CORECLKD_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP1_CORECLKD_DIVRATIO_7_0_CFG_OD_CLKTOP1_CORECLKD_DIVRATIO_7_0_DEFAULTRESET = 0x4


class ENUM_CFG_RESERVED513(Enum):
    CFG_RESERVED513_CFG_RESERVED513_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKE_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKE_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKE_DIVRETIMEREN_H_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKE_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKE_BYPASS_CFG_OD_CLKTOP1_CORECLKE_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED512(Enum):
    CFG_RESERVED512_CFG_RESERVED512_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKF_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKF_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKF_DIVRETIMEREN_H_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKF_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKF_BYPASS_CFG_OD_CLKTOP1_CORECLKF_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED511(Enum):
    CFG_RESERVED511_CFG_RESERVED511_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKE_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP1_CORECLKE_DIVRATIO_7_0_CFG_OD_CLKTOP1_CORECLKE_DIVRATIO_7_0_DEFAULTRESET = 0x19


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD2:
    DKLP_CMN_ANA_CMN_ANA_DWORD2 = 0x0C8


class _DKLP_CMN_ANA_CMN_ANA_DWORD2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Od_Clktop1_Coreclkc_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Od_Clktop1_Coreclkd_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Reserved513', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclke_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclke_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved512', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkf_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkf_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved511', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop1_Coreclke_Divratio_7_0', ctypes.c_uint32, 8),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD2(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Od_Clktop1_Coreclkc_Divratio_7_0 = 0  # bit 0 to 8
    Cfg_Od_Clktop1_Coreclkd_Divratio_7_0 = 0  # bit 8 to 16
    Cfg_Reserved513 = 0  # bit 16 to 17
    Cfg_Od_Clktop1_Coreclke_Divretimeren_H = 0  # bit 17 to 18
    Cfg_Od_Clktop1_Coreclke_Bypass = 0  # bit 18 to 19
    Cfg_Reserved512 = 0  # bit 19 to 20
    Cfg_Od_Clktop1_Coreclkf_Divretimeren_H = 0  # bit 20 to 21
    Cfg_Od_Clktop1_Coreclkf_Bypass = 0  # bit 21 to 22
    Cfg_Reserved511 = 0  # bit 22 to 24
    Cfg_Od_Clktop1_Coreclke_Divratio_7_0 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_OD_CLKTOP2_HSDIV_EN_H(Enum):
    CFG_OD_CLKTOP2_HSDIV_EN_H_CFG_OD_CLKTOP2_HSDIV_EN_H_DEFAULTRESET = 0x1


class ENUM_CFG_RESERVED520(Enum):
    CFG_RESERVED520_CFG_RESERVED520_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_DSDIV_EN_H(Enum):
    CFG_OD_CLKTOP2_DSDIV_EN_H_CFG_OD_CLKTOP2_DSDIV_EN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD_CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD_CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD_CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD_CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_OVERRIDEEN(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_OVERRIDEEN_CFG_OD_CLKTOP2_TLINEDRV_OVERRIDEEN_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_DSDIV_DIVRATIO_3_0(Enum):
    CFG_OD_CLKTOP2_DSDIV_DIVRATIO_3_0_CFG_OD_CLKTOP2_DSDIV_DIVRATIO_3_0_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP2_HSDIV_DIVRATIO_1_0(Enum):
    CFG_OD_CLKTOP2_HSDIV_DIVRATIO_1_0_CFG_OD_CLKTOP2_HSDIV_DIVRATIO_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_CLKSEL_1_0(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_CLKSEL_1_0_CFG_OD_CLKTOP2_TLINEDRV_CLKSEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLK_INPUTSEL(Enum):
    CFG_OD_CLKTOP2_CORECLK_INPUTSEL_CFG_OD_CLKTOP2_CORECLK_INPUTSEL_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED523(Enum):
    CFG_RESERVED523_CFG_RESERVED523_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_OUTCLK_BYPASSEN_H(Enum):
    CFG_OD_CLKTOP2_OUTCLK_BYPASSEN_H_CFG_OD_CLKTOP2_OUTCLK_BYPASSEN_H_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED522(Enum):
    CFG_RESERVED522_CFG_RESERVED522_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_VHFCLK_TESTEN_H_1_0(Enum):
    CFG_OD_CLKTOP2_VHFCLK_TESTEN_H_1_0_CFG_OD_CLKTOP2_VHFCLK_TESTEN_H_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED521(Enum):
    CFG_RESERVED521_CFG_RESERVED521_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CLK2OBS_EN_H(Enum):
    CFG_OD_CLKTOP2_CLK2OBS_EN_H_CFG_OD_CLKTOP2_CLK2OBS_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CLKOBS_INPUTSEL_1_0(Enum):
    CFG_OD_CLKTOP2_CLKOBS_INPUTSEL_1_0_CFG_OD_CLKTOP2_CLKOBS_INPUTSEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED524(Enum):
    CFG_RESERVED524_CFG_RESERVED524_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD5:
    DKLP_CMN_ANA_CMN_ANA_DWORD5 = 0x0D4


class _DKLP_CMN_ANA_CMN_ANA_DWORD5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Od_Clktop2_Hsdiv_En_H', ctypes.c_uint32, 1),
        ('Cfg_Reserved520', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Dsdiv_En_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Tlinedrv_Enright_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Tlinedrv_Enleft_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Tlinedrv_Enright_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Tlinedrv_Enleft_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Tlinedrv_Overrideen', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Dsdiv_Divratio_3_0', ctypes.c_uint32, 4),
        ('Cfg_Od_Clktop2_Hsdiv_Divratio_1_0', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop2_Tlinedrv_Clksel_1_0', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop2_Coreclk_Inputsel', ctypes.c_uint32, 1),
        ('Cfg_Reserved523', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Outclk_Bypassen_H', ctypes.c_uint32, 1),
        ('Cfg_Reserved522', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Vhfclk_Testen_H_1_0', ctypes.c_uint32, 2),
        ('Cfg_Reserved521', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop2_Clk2Obs_En_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Clkobs_Inputsel_1_0', ctypes.c_uint32, 2),
        ('Cfg_Reserved524', ctypes.c_uint32, 5),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD5(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Od_Clktop2_Hsdiv_En_H = 0  # bit 0 to 1
    Cfg_Reserved520 = 0  # bit 1 to 2
    Cfg_Od_Clktop2_Dsdiv_En_H = 0  # bit 2 to 3
    Cfg_Od_Clktop2_Tlinedrv_Enright_H_Ovrd = 0  # bit 3 to 4
    Cfg_Od_Clktop2_Tlinedrv_Enleft_H_Ovrd = 0  # bit 4 to 5
    Cfg_Od_Clktop2_Tlinedrv_Enright_Ded_H_Ovrd = 0  # bit 5 to 6
    Cfg_Od_Clktop2_Tlinedrv_Enleft_Ded_H_Ovrd = 0  # bit 6 to 7
    Cfg_Od_Clktop2_Tlinedrv_Overrideen = 0  # bit 7 to 8
    Cfg_Od_Clktop2_Dsdiv_Divratio_3_0 = 0  # bit 8 to 12
    Cfg_Od_Clktop2_Hsdiv_Divratio_1_0 = 0  # bit 12 to 14
    Cfg_Od_Clktop2_Tlinedrv_Clksel_1_0 = 0  # bit 14 to 16
    Cfg_Od_Clktop2_Coreclk_Inputsel = 0  # bit 16 to 17
    Cfg_Reserved523 = 0  # bit 17 to 18
    Cfg_Od_Clktop2_Outclk_Bypassen_H = 0  # bit 18 to 19
    Cfg_Reserved522 = 0  # bit 19 to 20
    Cfg_Od_Clktop2_Vhfclk_Testen_H_1_0 = 0  # bit 20 to 22
    Cfg_Reserved521 = 0  # bit 22 to 24
    Cfg_Od_Clktop2_Clk2Obs_En_H = 0  # bit 24 to 25
    Cfg_Od_Clktop2_Clkobs_Inputsel_1_0 = 0  # bit 25 to 27
    Cfg_Reserved524 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_RESERVED527(Enum):
    CFG_RESERVED527_CFG_RESERVED527_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKA_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP2_CORECLKA_DIVRETIMEREN_H_BYPASS_THE_RETIMER_PATH = 0x0  # This is POR.
    CFG_OD_CLKTOP2_CORECLKA_DIVRETIMEREN_H_ENABLE_THE_RETIMER_PATH = 0x1


class ENUM_CFG_RESERVED526(Enum):
    CFG_RESERVED526_CFG_RESERVED526_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKB_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP2_CORECLKB_DIVRETIMEREN_H_BYPASS_THE_RETIMER_PATH = 0x0


class ENUM_CFG_RESERVED525(Enum):
    CFG_RESERVED525_CFG_RESERVED525_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKA_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP2_CORECLKA_DIVRATIO_7_0_CFG_OD_CLKTOP2_CORECLKA_DIVRATIO_7_0_DEFAULTRESET = 0x5


class ENUM_CFG_OD_CLKTOP2_CORECLKB_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP2_CORECLKB_DIVRATIO_7_0_CFG_OD_CLKTOP2_CORECLKB_DIVRATIO_7_0_DEFAULTRESET = 0x8


class ENUM_CFG_RESERVED530(Enum):
    CFG_RESERVED530_CFG_RESERVED530_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKC_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP2_CORECLKC_DIVRETIMEREN_H_CFG_OD_CLKTOP2_CORECLKC_DIVRETIMEREN_H_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKC_BYPASS(Enum):
    CFG_OD_CLKTOP2_CORECLKC_BYPASS_CFG_OD_CLKTOP2_CORECLKC_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED529(Enum):
    CFG_RESERVED529_CFG_RESERVED529_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKD_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP2_CORECLKD_DIVRETIMEREN_H_CFG_OD_CLKTOP2_CORECLKD_DIVRETIMEREN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP2_CORECLKD_BYPASS(Enum):
    CFG_OD_CLKTOP2_CORECLKD_BYPASS_CFG_OD_CLKTOP2_CORECLKD_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED528(Enum):
    CFG_RESERVED528_CFG_RESERVED528_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD6:
    DKLP_CMN_ANA_CMN_ANA_DWORD6 = 0x0D8


class _DKLP_CMN_ANA_CMN_ANA_DWORD6(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Reserved527', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclka_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclka_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved526', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkb_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkb_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved525', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop2_Coreclka_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Od_Clktop2_Coreclkb_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Reserved530', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkc_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkc_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved529', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkd_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkd_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved528', ctypes.c_uint32, 2),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD6(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Reserved527 = 0  # bit 0 to 1
    Cfg_Od_Clktop2_Coreclka_Divretimeren_H = 0  # bit 1 to 2
    Cfg_Od_Clktop2_Coreclka_Bypass = 0  # bit 2 to 3
    Cfg_Reserved526 = 0  # bit 3 to 4
    Cfg_Od_Clktop2_Coreclkb_Divretimeren_H = 0  # bit 4 to 5
    Cfg_Od_Clktop2_Coreclkb_Bypass = 0  # bit 5 to 6
    Cfg_Reserved525 = 0  # bit 6 to 8
    Cfg_Od_Clktop2_Coreclka_Divratio_7_0 = 0  # bit 8 to 16
    Cfg_Od_Clktop2_Coreclkb_Divratio_7_0 = 0  # bit 16 to 24
    Cfg_Reserved530 = 0  # bit 24 to 25
    Cfg_Od_Clktop2_Coreclkc_Divretimeren_H = 0  # bit 25 to 26
    Cfg_Od_Clktop2_Coreclkc_Bypass = 0  # bit 26 to 27
    Cfg_Reserved529 = 0  # bit 27 to 28
    Cfg_Od_Clktop2_Coreclkd_Divretimeren_H = 0  # bit 28 to 29
    Cfg_Od_Clktop2_Coreclkd_Bypass = 0  # bit 29 to 30
    Cfg_Reserved528 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD6),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD6, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_OD_REFCLKIN1_REFCLKMUX_2_0(Enum):
    CFG_OD_REFCLKIN1_REFCLKMUX_2_0_CFG_OD_REFCLKIN1_REFCLKMUX_2_0_DEFAULTRESET = 0x1


class ENUM_CFG_OD_REFCLKIN1_REFCLKINJMUX(Enum):
    CFG_OD_REFCLKIN1_REFCLKINJMUX_CFG_OD_REFCLKIN1_REFCLKINJMUX_DEFAULTRESET = 0x0


class ENUM_CFG_OD_PLL10G_REFCLKIN_GENLOCK_REFCLKSEL(Enum):
    CFG_OD_PLL10G_REFCLKIN_GENLOCK_REFCLKSEL_CFG_OD_PLL10G_REFCLKIN_GENLOCK_REFCLKSEL_DEFAULTRESET = 0x0


class ENUM_CFG_OD_PLL10P3G_REFCLKIN_GENLOCK_REFCLKSEL(Enum):
    CFG_OD_PLL10P3G_REFCLKIN_GENLOCK_REFCLKSEL_CFG_OD_PLL10P3G_REFCLKIN_GENLOCK_REFCLKSEL_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED586(Enum):
    CFG_RESERVED586_CFG_RESERVED586_DEFAULTRESET = 0x0


class ENUM_CFG_OD_REFCLKIN2_REFCLKMUX_2_0(Enum):
    CFG_OD_REFCLKIN2_REFCLKMUX_2_0_CFG_OD_REFCLKIN2_REFCLKMUX_2_0_DEFAULTRESET = 0x3


class ENUM_CFG_OD_REFCLKIN2_REFCLKINJMUX(Enum):
    CFG_OD_REFCLKIN2_REFCLKINJMUX_CFG_OD_REFCLKIN2_REFCLKINJMUX_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED587(Enum):
    CFG_RESERVED587_CFG_RESERVED587_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED588(Enum):
    CFG_RESERVED588_CFG_RESERVED588_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED589(Enum):
    CFG_RESERVED589_CFG_RESERVED589_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD27:
    DKLP_CMN_ANA_CMN_ANA_DWORD27 = 0x12C


class _DKLP_CMN_ANA_CMN_ANA_DWORD27(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Od_Refclkin1_Refclkmux_2_0', ctypes.c_uint32, 3),
        ('Cfg_Od_Refclkin1_Refclkinjmux', ctypes.c_uint32, 1),
        ('Cfg_Od_Pll10G_Refclkin_Genlock_Refclksel', ctypes.c_uint32, 1),
        ('Cfg_Od_Pll10P3G_Refclkin_Genlock_Refclksel', ctypes.c_uint32, 1),
        ('Cfg_Reserved586', ctypes.c_uint32, 2),
        ('Cfg_Od_Refclkin2_Refclkmux_2_0', ctypes.c_uint32, 3),
        ('Cfg_Od_Refclkin2_Refclkinjmux', ctypes.c_uint32, 1),
        ('Cfg_Reserved587', ctypes.c_uint32, 4),
        ('Cfg_Reserved588', ctypes.c_uint32, 8),
        ('Cfg_Reserved589', ctypes.c_uint32, 8),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD27(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Od_Refclkin1_Refclkmux_2_0 = 0  # bit 0 to 3
    Cfg_Od_Refclkin1_Refclkinjmux = 0  # bit 3 to 4
    Cfg_Od_Pll10G_Refclkin_Genlock_Refclksel = 0  # bit 4 to 5
    Cfg_Od_Pll10P3G_Refclkin_Genlock_Refclksel = 0  # bit 5 to 6
    Cfg_Reserved586 = 0  # bit 6 to 8
    Cfg_Od_Refclkin2_Refclkmux_2_0 = 0  # bit 8 to 11
    Cfg_Od_Refclkin2_Refclkinjmux = 0  # bit 11 to 12
    Cfg_Reserved587 = 0  # bit 12 to 16
    Cfg_Reserved588 = 0  # bit 16 to 24
    Cfg_Reserved589 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD27),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD27, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


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


class OFFSET_DPLL_CFGCR0:
    DPLL0_CFGCR0 = 0x164284
    DPLL1_CFGCR0 = 0x16428C
    DPLL4_CFGCR0 = 0x164294
    TBTPLL_CFGCR0 = 0x16429C


class _DPLL_CFGCR0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DcoInteger', ctypes.c_uint32, 10),
        ('DcoFraction', ctypes.c_uint32, 15),
        ('Reserved25', ctypes.c_uint32, 7),
    ]


class REG_DPLL_CFGCR0(ctypes.Union):
    value = 0
    offset = 0

    DcoInteger = 0  # bit 0 to 10
    DcoFraction = 0  # bit 10 to 25
    Reserved25 = 0  # bit 25 to 32

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

