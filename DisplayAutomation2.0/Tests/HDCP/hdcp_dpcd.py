#######################################################################################################################
# @file         hdcp_dpcd.py
# @brief        HDCP related DPCD & I2C offsets register definition
# @details      Contains DPCD & I2C offsets, Enums, structures with bit wise definitions based on HDCP 1.4 & 2.2 spec
#
# @author       chandrakanth Reddy y
#######################################################################################################################


import ctypes
import enum

MAX_DP_HDCP_RETRY = 3
DP_MST_CAPS = 0x21
I2C_RX_SLAVE_ADDRESS = 0x74  # HDCP Port I2C Address


# HDCP 1.4
KSV_SIZE = 5
MAX_DP_KSV_FIFO_READ_SIZE = 15
RI_PRIME_SIZE = 2
HDCP1_R0_READ_TIMEOUT_IN_MS = 100
HDCP1_REPEATER_STEP_TIMEOUT_IN_MS = 5000
HDCP1_RI_PRIME_READ_TIMEOUT_IN_MS = 2000
HDCP1_RI_PRIME_READ_MAX_TIMEOUT_IN_MS = HDCP1_RI_PRIME_READ_TIMEOUT_IN_MS + 1500  # 2secs + 1.5 secs
HDCP1_MAX_DOWNSTREAM_DEVICES = 127
HDCP1_MAX_DEPTH = 7
HDCP1_MAX_RI_RETRY = 3
HDCP_WAIT_TIME_FOR_ENCRYPTION_ENABLE_IN_MS = 200
# HDCP 2.2
HDCP2_AKE_INIT_WRITE_TIMEOUT_IN_MS = 10000
HDCP2_COMMON_AUTHENTICATION_STEP_TIMEOUT = 5000
HDCP2_RX_CERT_READ_TIMEOUT_IN_MS = 100
HDCP2_NO_STORED_KM_H_PRIME_READ_TIMEOUT_IN_MS = 1000
HDCP2_STORED_KM_H_PRIME_READ_TIMEOUT_IN_MS = 200
HDCP2_PAIRING_INFO_READ_TIMEOUT_IN_MS = 200
HDCP2_DP_ERRATA_TYPE_WRITE_TIMEOUT_IN_MS = 200
HDCP2_L_PRIME_READ_TIMEOUT_IN_MS = 20
HDCP2_RECEIVER_IDS_READ_TIMEOUT_IN_MS = 3000
HDCP2_REPEATER_AUTH_READ_TIMEOUT_IN_MS = 2000
HDCP2_REPEATER_AUTH_SEND_ACK_TIMEOUT_IN_MS = 1000
HDCP2_REPEATER_AUTH_STREAM_READY_READ_TIMEOUT_IN_MS = 100
HDCP2_RECEIVER_IDS_MAX_LEN = 5 * 31
HDCP2_MAX_DOWNSTREAM_DEVICES = 32
HDCP2_MAX_DEPTH = 4

NIBBLE_PER_BYTE = 2


##
# @brief Exposed Enum Class for SHA 1 DDI value select
class SHA1_M0_SELECT_GEN11(enum.IntEnum):
    SHA1_M0_SELECT_DDI_B = 0x1
    SHA1_M0_SELECT_DDI_A = 0x2
    SHA1_M0_SELECT_DDI_C = 0x3
    SHA1_M0_SELECT_DDI_D = 0x4
    SHA1_M0_SELECT_DDI_F = 0x5
    SHA1_M0_SELECT_DDI_E = 0x6


##
# @brief Exposed Enum Class for SHA 1 Transcoder value select
class SHA1_M0_SELECT(enum.IntEnum):
    SHA1_M0_SELECT_TRANSCODER_A = 0x0
    SHA1_M0_SELECT_TRANSCODER_B = 0x2
    SHA1_M0_SELECT_TRANSCODER_C = 0x3
    SHA1_M0_SELECT_TRANSCODER_D = 0x4


M0_SELECT_GEN11 = {
    SHA1_M0_SELECT_GEN11.SHA1_M0_SELECT_DDI_B: 'B',
    SHA1_M0_SELECT_GEN11.SHA1_M0_SELECT_DDI_A: 'A',
    SHA1_M0_SELECT_GEN11.SHA1_M0_SELECT_DDI_C: 'C',
    SHA1_M0_SELECT_GEN11.SHA1_M0_SELECT_DDI_D: 'D',
    SHA1_M0_SELECT_GEN11.SHA1_M0_SELECT_DDI_F: 'F',
    SHA1_M0_SELECT_GEN11.SHA1_M0_SELECT_DDI_E: 'E'
}

M0_SELECT = {
    SHA1_M0_SELECT.SHA1_M0_SELECT_TRANSCODER_A: 'A',
    SHA1_M0_SELECT.SHA1_M0_SELECT_TRANSCODER_B: 'B',
    SHA1_M0_SELECT.SHA1_M0_SELECT_TRANSCODER_C: 'C',
    SHA1_M0_SELECT.SHA1_M0_SELECT_TRANSCODER_D: 'D'
}


##
# @brief Exposed Class for HDCP 1.4 DP offsets
class HDCP_1_4_DP_OFFSETS:
    BKSV = 0x68000
    RI_PRIME = 0x68005
    AKSV = 0x68007
    BCAPS = 0x68028
    BSTATUS = 0x68029
    KSV_FIFO = 0x6802c
    BINFO = 0x6802A


##
# @brief Exposed Class for HDCP 1.4 HDMI offsets
class HDCP_1_4_HDMI_OFFSETS:
    BKSV = 0x00
    RI_PRIME = 0x08
    AKSV = 0x10
    BCAPS = 0x40
    BSTATUS = 0x41
    KSV_FIFO = 0x43


##
# @brief Exposed Class for HDCP 1.4 HDMI register Bit field definition
class HDMI_BSTATUS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DeviceCount', ctypes.c_uint16, 7),  # bit 0 to bit 6
        ('MaxDevsExceeded', ctypes.c_uint16, 1),  # bit 7
        ('Depth', ctypes.c_uint16, 3),  # bit 8 to bit 10
        ('MaxCascadeExceeded', ctypes.c_uint16, 1),  # bit 11
        ('RXInHDMIMode', ctypes.c_uint16, 1),  # bit 12
        ('Reserved3', ctypes.c_uint16, 3),  # bit 13 to bit 15
    ]


##
# @brief Exposed Class for HDCP register definition
class HDMI_BSTATUS_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDMI_BSTATUS_REG),
        ("value", ctypes.c_uint16)]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(HDMI_BSTATUS_REGISTER, self).__init__()
        self.offset = HDCP_1_4_HDMI_OFFSETS.BSTATUS
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 1.4 HDMI register Bit field definition
class HDMI_BCAPS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FastReAuthentication', ctypes.c_uint8, 1),  # bit 0
        ('B1_1FeaturesSupported', ctypes.c_uint8, 1),  # bit 1
        ('Reserved2', ctypes.c_uint8, 2),  # bit 2 to bit 3
        ('FastTransfer', ctypes.c_uint8, 1),  # bit 4  ( 1  = transfer speed at 400 kHz,  0 = transfer speed at 100 Khz)
        ('KSVFifoReady', ctypes.c_uint8, 1),  # bit 5
        ('IsRepeater', ctypes.c_uint8, 1),  # bit 6
        ('Reserved7', ctypes.c_uint8, 1),  # bit 7
    ]


##
# @brief Exposed Class for HDCP 1.4 HDMI register definition
class HDMI_BCAPS_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDMI_BCAPS_REG),
        ("value", ctypes.c_uint8)]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(HDMI_BCAPS_REGISTER, self).__init__()
        self.offset = HDCP_1_4_HDMI_OFFSETS.BCAPS
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 1.4 DP register Bit field definition
class DP_BCAPS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HDCPCapable', ctypes.c_uint8, 1),  # bit 0
        ('IsRepeater', ctypes.c_uint8, 1),  # bit 1
        ('Reserved3', ctypes.c_uint8, 6),  # bit 2 to bit 7
    ]


##
# @brief Exposed Class for HDCP 1.4 DP register definition
class DP_BCAPS_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DP_BCAPS_REG),
        ("value", ctypes.c_uint8)]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(DP_BCAPS_REGISTER, self).__init__()
        self.offset = HDCP_1_4_DP_OFFSETS.BCAPS
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 1.4 DP register Bit field definition
class DP_BSTATUS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('KSVFifoReady', ctypes.c_uint8, 1),  # bit 0
        ('RiAvailable', ctypes.c_uint8, 1),  # bit 1
        ('LinkIntegrityFailed', ctypes.c_uint8, 1),  # bit 2
        ('Reserved5', ctypes.c_uint8, 5),  # bit 3 to bit 7
    ]


##
# @brief Exposed Class for HDCP 1.4 DP register definition
class DP_BSTATUS_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DP_BSTATUS_REG),
        ("value", ctypes.c_uint8)]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(DP_BSTATUS_REGISTER, self).__init__()
        self.offset = HDCP_1_4_DP_OFFSETS.BSTATUS
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 1.4 DP register Bit field definition
class DP_BINFO_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DeviceCount', ctypes.c_uint16, 7),  # bit 0 to bit 6
        ('MaxDevsExceeded', ctypes.c_uint16, 1),  # bit 7
        ('Depth', ctypes.c_uint16, 3),  # bit 8 to bit 10
        ('MaxCascadeExceeded', ctypes.c_uint16, 1),  # bit 11
        ('Reserved4', ctypes.c_uint16, 4),  # bit 12 to bit 15
    ]


##
# @brief Exposed Class for HDCP 1.4 DP register definition
class DP_BINFO_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DP_BINFO_REG),
        ("value", ctypes.c_uint16)
    ]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(DP_BINFO_REGISTER, self).__init__()
        self.offset = HDCP_1_4_DP_OFFSETS.BINFO
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 2.2 DP offsets
class HDCP2_DP_OFFSETS:
    HDCP2_DP_RTX = 0x69000
    HDCP2_DP_TXCAPS = 0x69008
    HDCP2_DP_CERT_RX = 0x6900B
    HDCP2_DP_RRX = 0x69215
    HDCP2_DP_RXCAPS = 0x6921D
    HDCP2_DP_EKPUB_KM = 0x69220
    HDCP2_DP_EKH_KM_TX = 0x692A0
    HDCP2_DP_M_TX = 0x692B0
    HDCP2_DP_HPRIME = 0x692C0
    HDCP2_DP_EKH_KM_RX = 0x692E0
    HDCP2_DP_RN = 0x692F0
    HDCP2_DP_LPRIME = 0x692F8
    HDCP2_DP_EDKEY_KS = 0x69318
    HDCP2_DP_RIV = 0x69328
    HDCP2_DP_RXINFO = 0x69330
    HDCP2_DP_SEQ_NUM_V = 0x69332
    HDCP2_DP_V_RX = 0x69335
    HDCP2_DP_RCVR_ID_LST = 0x69345
    HDCP2_DP_V_TX = 0x693E0
    HDCP2_DP_SEQ_NUM_M = 0x693F0
    HDCP2_DP_K = 0x693F3
    HDCP2_DP_STRMID_TYPE = 0x693F5
    HDCP2_DP_M_RX = 0x69473
    HDCP2_DP_RXSTATUS = 0x69493
    HDCP2_DP_ERRATA_TYPE = 0x69494


##
# @brief Exposed Class for HDCP 2.2 HDMI offsets
class HDCP2_HDMI_OFFSETS:
    HDCP2_HDMI_VERSION = 0x50
    HDCP2_HDMI_WRITE_OFFSET = 0x60
    HDCP2_HDMI_RXSTATUS = 0x70
    HDCP2_HDMI_READ_OFFSET = 0x80


##
# @brief Exposed Class for HDCP 2.2 DP register Bit field definition
class HDCP2_DP_RX_STATUS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Ready', ctypes.c_uint8, 1),  # bit 0
        ('Havailable', ctypes.c_uint8, 1),  # bit 1
        ('PairingAvailable', ctypes.c_uint8, 1),  # bit 2
        ('ReauthReq', ctypes.c_uint8, 1),  # bit 3
        ('LinkIntegrityFailure', ctypes.c_uint8, 1),  # bit 4
        ('Reserved3', ctypes.c_uint8, 3),  # bit 5 to bit 7

    ]


##
# @brief Exposed Class for HDCP 2.2 DP register
class HDCP2_DP_RX_STATUS_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDCP2_DP_RX_STATUS_REG),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(HDCP2_DP_RX_STATUS_REGISTER, self).__init__()
        self.offset = HDCP2_DP_OFFSETS.HDCP2_DP_RXSTATUS
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 2.2 HDMI register Bit field definition
class HDCP2_HDMI_RX_STATUS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MessageSize', ctypes.c_uint16, 10),  # bit 0 to bit 9
        ('Ready', ctypes.c_uint16, 1),  # bit 10
        ('ReauthReq', ctypes.c_uint16, 1),  # bit 11
        ('Reserved12', ctypes.c_uint16, 4),  # bit 12 to bit 15

    ]


##
# @brief Exposed Class for HDCP 2.2 HDMI register definition
class HDCP2_HDMI_RX_STATUS_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDCP2_HDMI_RX_STATUS_REG),
        ("value", ctypes.c_uint16)]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(HDCP2_HDMI_RX_STATUS_REGISTER, self).__init__()
        self.offset = HDCP2_HDMI_OFFSETS.HDCP2_HDMI_RXSTATUS
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 2.2 DP register Bit field definition
class HDCP2_DP_RX_INFO_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hdcp1DeviceDownstream', ctypes.c_uint16, 1),  # bit 0
        ('Hdcp2LegacyDeviceDownstream', ctypes.c_uint16, 1),  # bit 1
        ('MaxCascadeExceeded', ctypes.c_uint16, 1),  # bit 2
        ('MaxDeviceExceeded', ctypes.c_uint16, 1),  # bit 3
        ('DeviceCount', ctypes.c_uint16, 5),   # bit 4 to bit 8
        ('Depth', ctypes.c_uint16, 3),  # bit 9 to bit 11
        ('Reserved12', ctypes.c_uint16, 4),  # bit 12 to bit 15

    ]


##
# @brief Exposed Class for HDCP 2.2 DP register definition
class HDCP2_DP_RX_INFO_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDCP2_DP_RX_INFO_REG),
        ("value", ctypes.c_uint16)
    ]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(HDCP2_DP_RX_INFO_REGISTER, self).__init__()
        self.offset = HDCP2_DP_OFFSETS.HDCP2_DP_RXINFO
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 2.2 DP register Bit field definition
class HDCP2_DP_TX_CAPS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TrasmitterCapabilityMask', ctypes.c_uint32, 16),  # bit 0 to bit 15
        ('Version', ctypes.c_uint32, 8),  # bit 16 to bit 23
        ('Reserved24', ctypes.c_uint32, 8),  # bit 24 to bit 31

    ]


##
# @brief Exposed Class for HDCP 2.2 DP register
class HDCP2_DP_TX_CAPS_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDCP2_DP_TX_CAPS_REG),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(HDCP2_DP_TX_CAPS_REGISTER, self).__init__()
        self.offset = HDCP2_DP_OFFSETS.HDCP2_DP_TXCAPS
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 2.2 DP register Bit field definition
class HDCP2_DP_RX_CAPS_REG(ctypes.LittleEndianStructure):
    _fields_ = [

        ('Repeater', ctypes.c_uint32, 1),  # bit 0
        ('HdcpCapable', ctypes.c_uint32, 1),  # bit 1
        ('ReceiverCapabilityMask', ctypes.c_uint32, 14),  # bit 2 to bit 15
        ('Version', ctypes.c_uint32, 8),  # bit 16 to bit 23 , must be 0x2
        ('Reserved24', ctypes.c_uint32, 8),  # bit 24 to bit 31

    ]


##
# @brief Exposed Class for HDCP 2.2 DP register definition
class HDCP2_DP_RX_CAPS_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDCP2_DP_RX_CAPS_REG),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(HDCP2_DP_RX_CAPS_REGISTER, self).__init__()
        self.offset = HDCP2_DP_OFFSETS.HDCP2_DP_RXCAPS
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 2.2 HDMI register Bit field definition
class HDCP2_HDMI_RX_CAPS_REG(ctypes.LittleEndianStructure):
    _fields_ = [

        ('Repeater', ctypes.c_uint32, 1),  # bit 0
        ('Reserved1', ctypes.c_uint32, 1),  # bit 1
        ('ReceiverCapabilityMask', ctypes.c_uint32, 14),  # bit 2 to bit 15
        ('Version', ctypes.c_uint32, 8),  # bit 16 to bit 23 , must be 0x2
        ('Reserved24', ctypes.c_uint32, 8),  # bit 24 to bit 31

    ]


##
# @brief Exposed Class for HDCP 1.4 HDMI register definition
class HDCP2_HDMI_RX_CAPS_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDCP2_HDMI_RX_CAPS_REG),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(HDCP2_HDMI_RX_CAPS_REGISTER, self).__init__()
        self.offset = HDCP2_HDMI_OFFSETS.HDCP2_HDMI_RXSTATUS
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 2.2 HDMI register Bit field definition
class HDCP2_HDMI_VERSION_REG(ctypes.LittleEndianStructure):
    _fields_ = [

        ('Reserved1', ctypes.c_uint8, 2),  # bit 0 to bit 1
        ('Version', ctypes.c_uint8, 1),  # bit 2
        ('Reserved3', ctypes.c_uint8, 5),  # bit 3 to bit 7

    ]


##
# @brief Exposed Class for HDCP 2.2 HDMI register definition
class HDCP2_HDMI_VERSION_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDCP2_HDMI_VERSION_REG),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(HDCP2_HDMI_VERSION_REGISTER, self).__init__()
        self.offset = HDCP2_HDMI_OFFSETS.HDCP2_HDMI_VERSION
        if value is not None:
            self.value = value


##
# @brief Exposed Class for HDCP 2.2 HDMI register Bit field definition
class HDCP2_HDMI_RX_INFO_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hdcp1DeviceDownstream', ctypes.c_uint16, 1),  # bit 0
        ('Hdcp2LegacyDeviceDownstream', ctypes.c_uint16, 1),  # bit 1
        ('MaxCascadeExceeded', ctypes.c_uint16, 1),  # bit 2
        ('MaxDeviceExceeded', ctypes.c_uint16, 1),  # bit 3
        ('DeviceCount', ctypes.c_uint16, 5),   # bit 4 to bit 8
        ('Depth', ctypes.c_uint16, 3),  # bit 9 to bit 11
        ('Reserved12', ctypes.c_uint16, 4),  # bit 12 to bit 15

    ]


##
# @brief Exposed Class for HDCP 2.2 HDMI register definition
class HDCP2_HDMI_RX_INFO_REGISTER(ctypes.Union):
    value = 0
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HDCP2_HDMI_RX_INFO_REG),
        ("value", ctypes.c_uint16)
    ]

    ##
    # @brief      init method of HDCP register definition
    # @param[in]  value default value to assign
    def __init__(self, value=None):
        super(HDCP2_HDMI_RX_INFO_REGISTER, self).__init__()
        self.offset = HDCP2_HDMI_OFFSETS.HDCP2_HDMI_READ_OFFSET
        if value is not None:
            self.value = value
