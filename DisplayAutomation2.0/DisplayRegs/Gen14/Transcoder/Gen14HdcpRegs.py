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
# @file Gen14HdcpRegs.py
# @brief contains Gen14HdcpRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_KEY_LOAD(Enum):
    KEY_LOAD_DO_NOT_LOAD = 0x0
    KEY_LOAD_LOAD = 0x1


class ENUM_CLEAR_KEYS_TRIGGER(Enum):
    CLEAR_KEYS_TRIGGER_DO_NOT_CLEAR = 0x0
    CLEAR_KEYS_TRIGGER_CLEAR = 0x1


class ENUM_AKSV_SEND_TRIGGER(Enum):
    AKSV_SEND_TRIGGER_DO_NOT_SEND = 0x0
    AKSV_SEND_TRIGGER_SEND = 0x1


class OFFSET_HDCP_KEY_CONF:
    HDCP_KEY_CONF = 0x66C00


class _HDCP_KEY_CONF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 2),
        ('DebugSelect', ctypes.c_uint32, 2),
        ('Reserved4', ctypes.c_uint32, 4),
        ('KeyLoad', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 21),
        ('ClearKeysTrigger', ctypes.c_uint32, 1),
        ('AksvSendTrigger', ctypes.c_uint32, 1),
    ]


class REG_HDCP_KEY_CONF(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 2
    DebugSelect = 0  # bit 2 to 4
    Reserved4 = 0  # bit 4 to 8
    KeyLoad = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 30
    ClearKeysTrigger = 0  # bit 30 to 31
    AksvSendTrigger = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_KEY_CONF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_KEY_CONF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_KEY_LOAD_DONE(Enum):
    KEY_LOAD_DONE_NOT_DONE = 0x0
    KEY_LOAD_DONE_DONE = 0x1


class ENUM_KEY_LOAD_STATUS(Enum):
    KEY_LOAD_STATUS_FAIL = 0x0
    KEY_LOAD_STATUS_SUCCESS = 0x1


class ENUM_FUSE_DONE(Enum):
    FUSE_DONE_NOT_DONE = 0x0
    FUSE_DONE_DONE = 0x1


class ENUM_FUSE_ERROR(Enum):
    FUSE_ERROR_NOT_ERROR = 0x0
    FUSE_ERROR_ERROR = 0x1


class ENUM_FUSE_IN_PROGRESS(Enum):
    FUSE_IN_PROGRESS_NOT_IN_PROGRESS = 0x0
    FUSE_IN_PROGRESS_IN_PROGRESS = 0x1


class OFFSET_HDCP_KEY_STATUS:
    HDCP_KEY_STATUS = 0x66C04


class _HDCP_KEY_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('KeyLoadDone', ctypes.c_uint32, 1),
        ('KeyLoadStatus', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 3),
        ('FuseDone', ctypes.c_uint32, 1),
        ('FuseError', ctypes.c_uint32, 1),
        ('FuseInProgress', ctypes.c_uint32, 1),
        ('Reserved8', ctypes.c_uint32, 24),
    ]


class REG_HDCP_KEY_STATUS(ctypes.Union):
    value = 0
    offset = 0

    KeyLoadDone = 0  # bit 0 to 1
    KeyLoadStatus = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 5
    FuseDone = 0  # bit 5 to 6
    FuseError = 0  # bit 6 to 7
    FuseInProgress = 0  # bit 7 to 8
    Reserved8 = 0  # bit 8 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_KEY_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_KEY_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CONFIGURATION(Enum):
    CONFIGURATION_OFF = 0x0
    CONFIGURATION_CAPTURE_AN = 0x1
    CONFIGURATION_AUTHENTICATE_AND_ENCRYPT = 0x3


class OFFSET_HDCP_CONF:
    HDCP_CONF_TCA = 0x66400
    HDCP_CONF_TCB = 0x66500
    HDCP_CONF_TCC = 0x66600
    HDCP_CONF_TCD = 0x66700


class _HDCP_CONF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Configuration', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 30),
    ]


class REG_HDCP_CONF(ctypes.Union):
    value = 0
    offset = 0

    Configuration = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_CONF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_CONF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP_ANINIT:
    HDCP_ANINIT_TCA = 0x66404
    HDCP_ANINIT_TCB = 0x66504
    HDCP_ANINIT_TCC = 0x66604
    HDCP_ANINIT_TCD = 0x66704


class _HDCP_ANINIT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AnInitializationVector', ctypes.c_uint32, 32),
    ]


class REG_HDCP_ANINIT(ctypes.Union):
    value = 0
    offset = 0

    AnInitializationVector = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_ANINIT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_ANINIT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP_ANLO:
    HDCP_ANLO_TCA = 0x66408
    HDCP_ANLO_TCB = 0x66508
    HDCP_ANLO_TCC = 0x66608
    HDCP_ANLO_TCD = 0x66708


class _HDCP_ANLO(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AnLow', ctypes.c_uint32, 32),
    ]


class REG_HDCP_ANLO(ctypes.Union):
    value = 0
    offset = 0

    AnLow = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_ANLO),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_ANLO, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP_ANHI:
    HDCP_ANHI_TCA = 0x6640C
    HDCP_ANHI_TCB = 0x6650C
    HDCP_ANHI_TCC = 0x6660C
    HDCP_ANHI_TCD = 0x6670C


class _HDCP_ANHI(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AnHigh', ctypes.c_uint32, 32),
    ]


class REG_HDCP_ANHI(ctypes.Union):
    value = 0
    offset = 0

    AnHigh = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_ANHI),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_ANHI, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP_BKSVLO:
    HDCP_BKSVLO_TCA = 0x66410
    HDCP_BKSVLO_TCB = 0x66510
    HDCP_BKSVLO_TCC = 0x66610
    HDCP_BKSVLO_TCD = 0x66710


class _HDCP_BKSVLO(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BksvLow', ctypes.c_uint32, 32),
    ]


class REG_HDCP_BKSVLO(ctypes.Union):
    value = 0
    offset = 0

    BksvLow = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_BKSVLO),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_BKSVLO, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP_BKSVHI:
    HDCP_BKSVHI_TCA = 0x66414
    HDCP_BKSVHI_TCB = 0x66514
    HDCP_BKSVHI_TCC = 0x66614
    HDCP_BKSVHI_TCD = 0x66714


class _HDCP_BKSVHI(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BksvHigh', ctypes.c_uint32, 32),
    ]


class REG_HDCP_BKSVHI(ctypes.Union):
    value = 0
    offset = 0

    BksvHigh = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_BKSVHI),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_BKSVHI, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP_AKSV_LO:
    HDCP_AKSV_LO = 0x66C10


class _HDCP_AKSV_LO(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AksvLow', ctypes.c_uint32, 32),
    ]


class REG_HDCP_AKSV_LO(ctypes.Union):
    value = 0
    offset = 0

    AksvLow = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_AKSV_LO),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_AKSV_LO, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP_AKSV_HI:
    HDCP_AKSV_HI = 0x66C14


class _HDCP_AKSV_HI(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AksvHigh', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 24),
    ]


class REG_HDCP_AKSV_HI(ctypes.Union):
    value = 0
    offset = 0

    AksvHigh = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_AKSV_HI),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_AKSV_HI, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP_RPRIME:
    HDCP_RPRIME_TCA = 0x66418
    HDCP_RPRIME_TCB = 0x66518
    HDCP_RPRIME_TCC = 0x66618
    HDCP_RPRIME_TCD = 0x66718


class _HDCP_RPRIME(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RiPrime', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_HDCP_RPRIME(ctypes.Union):
    value = 0
    offset = 0

    RiPrime = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_RPRIME),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_RPRIME, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CIPHER_STATUS(Enum):
    CIPHER_STATUS_NOT_MATCH = 0x0
    CIPHER_STATUS_MATCH = 0x1


class ENUM_AN_READY_STATUS(Enum):
    AN_READY_STATUS_NOT_READY = 0x0
    AN_READY_STATUS_READY = 0x1


class ENUM_R0_READY_STATUS(Enum):
    R0_READY_STATUS_NOT_READY = 0x0
    R0_READY_STATUS_READY = 0x1


class ENUM_RI_PRIME_MATCH_STATUS(Enum):
    RI_PRIME_MATCH_STATUS_NOT_MATCH = 0x0
    RI_PRIME_MATCH_STATUS_MATCH = 0x1


class ENUM_LINK_ENCRYPTION_STATUS(Enum):
    LINK_ENCRYPTION_STATUS_NOT_ENCRYPTING = 0x0
    LINK_ENCRYPTION_STATUS_ENCRYPTING = 0x1


class ENUM_AUTHENTICATION_STATUS(Enum):
    AUTHENTICATION_STATUS_NOT_AUTHENTICATED = 0x0
    AUTHENTICATION_STATUS_AUTHENTICATED = 0x1


class ENUM_STREAM_ENCRYPTION_STATUS_D(Enum):
    STREAM_ENCRYPTION_STATUS_D_NOT_ENCRYPTING = 0x0
    STREAM_ENCRYPTION_STATUS_D_ENCRYPTING = 0x1


class ENUM_STREAM_ENCRYPTION_STATUS_C(Enum):
    STREAM_ENCRYPTION_STATUS_C_NOT_ENCRYPTING = 0x0
    STREAM_ENCRYPTION_STATUS_C_ENCRYPTING = 0x1


class ENUM_STREAM_ENCRYPTION_STATUS_B(Enum):
    STREAM_ENCRYPTION_STATUS_B_NOT_ENCRYPTING = 0x0
    STREAM_ENCRYPTION_STATUS_B_ENCRYPTING = 0x1


class ENUM_STREAM_ENCRYPTION_STATUS_A(Enum):
    STREAM_ENCRYPTION_STATUS_A_NOT_ENCRYPTING = 0x0
    STREAM_ENCRYPTION_STATUS_A_ENCRYPTING = 0x1


class OFFSET_HDCP_STATUS:
    HDCP_STATUS_TCA = 0x6641C
    HDCP_STATUS_TCB = 0x6651C
    HDCP_STATUS_TCC = 0x6661C
    HDCP_STATUS_TCD = 0x6671C


class _HDCP_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 8),
        ('FrameCount', ctypes.c_uint32, 8),
        ('CipherStatus', ctypes.c_uint32, 1),
        ('AnReadyStatus', ctypes.c_uint32, 1),
        ('R0ReadyStatus', ctypes.c_uint32, 1),
        ('RiPrimeMatchStatus', ctypes.c_uint32, 1),
        ('LinkEncryptionStatus', ctypes.c_uint32, 1),
        ('AuthenticationStatus', ctypes.c_uint32, 1),
        ('Reserved22', ctypes.c_uint32, 6),
        ('StreamEncryptionStatusD', ctypes.c_uint32, 1),
        ('StreamEncryptionStatusC', ctypes.c_uint32, 1),
        ('StreamEncryptionStatusB', ctypes.c_uint32, 1),
        ('StreamEncryptionStatusA', ctypes.c_uint32, 1),
    ]


class REG_HDCP_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 8
    FrameCount = 0  # bit 8 to 16
    CipherStatus = 0  # bit 16 to 17
    AnReadyStatus = 0  # bit 17 to 18
    R0ReadyStatus = 0  # bit 18 to 19
    RiPrimeMatchStatus = 0  # bit 19 to 20
    LinkEncryptionStatus = 0  # bit 20 to 21
    AuthenticationStatus = 0  # bit 21 to 22
    Reserved22 = 0  # bit 22 to 28
    StreamEncryptionStatusD = 0  # bit 28 to 29
    StreamEncryptionStatusC = 0  # bit 29 to 30
    StreamEncryptionStatusB = 0  # bit 30 to 31
    StreamEncryptionStatusA = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SHA1_CONTROL(Enum):
    SHA1_CONTROL_IDLE = 0x0
    SHA1_CONTROL_INPUT_32_BIT_TEXT = 0x1
    SHA1_CONTROL_COMPLETE_THE_HASHING = 0x2
    SHA1_CONTROL_INPUT_24_BIT_TEXT_AND_8_BIT_M0_INTERNAL_VALUE = 0x4
    SHA1_CONTROL_INPUT_16_BIT_TEXT_AND_16_BIT_M0_INTERNAL_VALUE = 0x5
    SHA1_CONTROL_INPUT_8_BIT_TEXT_AND_24_BIT_M0_INTERNAL_VALUE = 0x6
    SHA1_CONTROL_INPUT_32_BIT_M0_INTERNAL_VALUE = 0x7


class ENUM_SHA1_STATUS(Enum):
    SHA1_STATUS_IDLE = 0x0
    SHA1_STATUS_BUSY = 0x1
    SHA1_STATUS_READY_FOR_NEXT_DATA_INPUT = 0x2
    SHA1_STATUS_COMPLETE_WITH_V_AND_V_PRIME_MISMATCH = 0x4
    SHA1_STATUS_COMPLETE_WITH_V_AND_V_PRIME_MATCH = 0xC


class ENUM_SHA1_M0_SELECT(Enum):
    SHA1_M0_SELECT_TRANSCODER_A = 0x0
    SHA1_M0_SELECT_TRANSCODER_B = 0x2
    SHA1_M0_SELECT_TRANSCODER_C = 0x3
    SHA1_M0_SELECT_TRANSCODER_D = 0x4


class ENUM_TRANSCODER_D_REPEATER_PRESENT(Enum):
    TRANSCODER_D_REPEATER_PRESENT_NOT_REPEATER = 0x0
    TRANSCODER_D_REPEATER_PRESENT_REPEATER = 0x1


class ENUM_TRANSCODER_C_REPEATER_PRESENT(Enum):
    TRANSCODER_C_REPEATER_PRESENT_NOT_REPEATER = 0x0
    TRANSCODER_C_REPEATER_PRESENT_REPEATER = 0x1


class ENUM_TRANSCODER_B_REPEATER_PRESENT(Enum):
    TRANSCODER_B_REPEATER_PRESENT_NOT_REPEATER = 0x0
    TRANSCODER_B_REPEATER_PRESENT_REPEATER = 0x1


class ENUM_TRANSCODER_A_REPEATER_PRESENT(Enum):
    TRANSCODER_A_REPEATER_PRESENT_NOT_REPEATER = 0x0
    TRANSCODER_A_REPEATER_PRESENT_REPEATER = 0x1


class OFFSET_HDCP_REP_CONTROL:
    HDCP_REP_CONTROL = 0x66D00


class _HDCP_REP_CONTROL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('Sha1Control', ctypes.c_uint32, 3),
        ('Reserved4', ctypes.c_uint32, 12),
        ('Sha1Status', ctypes.c_uint32, 4),
        ('Sha1M0Select', ctypes.c_uint32, 3),
        ('Reserved23', ctypes.c_uint32, 5),
        ('TranscoderDRepeaterPresent', ctypes.c_uint32, 1),
        ('TranscoderCRepeaterPresent', ctypes.c_uint32, 1),
        ('TranscoderBRepeaterPresent', ctypes.c_uint32, 1),
        ('TranscoderARepeaterPresent', ctypes.c_uint32, 1),
    ]


class REG_HDCP_REP_CONTROL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    Sha1Control = 0  # bit 1 to 4
    Reserved4 = 0  # bit 4 to 16
    Sha1Status = 0  # bit 16 to 20
    Sha1M0Select = 0  # bit 20 to 23
    Reserved23 = 0  # bit 23 to 28
    TranscoderDRepeaterPresent = 0  # bit 28 to 29
    TranscoderCRepeaterPresent = 0  # bit 29 to 30
    TranscoderBRepeaterPresent = 0  # bit 30 to 31
    TranscoderARepeaterPresent = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_REP_CONTROL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_REP_CONTROL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP_SHA_VPRIME:
    HDCP_SHA_VPRIME = 0x66D04


class _HDCP_SHA_VPRIME(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VPrime0', ctypes.c_uint32, 32),
        ('VPrime1', ctypes.c_uint32, 32),
        ('VPrime2', ctypes.c_uint32, 32),
        ('VPrime3', ctypes.c_uint32, 32),
        ('VPrime4', ctypes.c_uint32, 32),
    ]


class REG_HDCP_SHA_VPRIME(ctypes.Union):
    value = 0
    offset = 0

    VPrime0 = 0  # bit 0 to 32
    VPrime1 = 0  # bit 0 to 32
    VPrime2 = 0  # bit 0 to 32
    VPrime3 = 0  # bit 0 to 32
    VPrime4 = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_SHA_VPRIME),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_SHA_VPRIME, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP_SHA_TEXT:
    HDCP_SHA_TEXT = 0x66D18


class _HDCP_SHA_TEXT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Sha1Text', ctypes.c_uint32, 32),
    ]


class REG_HDCP_SHA_TEXT(ctypes.Union):
    value = 0
    offset = 0

    Sha1Text = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP_SHA_TEXT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP_SHA_TEXT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_VBID_TYPE_SELECT(Enum):
    VBID_TYPE_SELECT_LINK_TYPE = 0x0  # VBID 8 bit value uses Link Type and Maud/Mvid uses Link Type
    VBID_TYPE_SELECT_MIXED = 0x2  # VBID 8 bit value uses Type 0 and Maud/Mvid uses Link Type
    VBID_TYPE_SELECT_TYPE_0 = 0x3  # VBID 8 bit value uses Type 0 and Maud/Mvid uses Type 0


class ENUM_LINK_ENCRYPTION_REQUEST(Enum):
    LINK_ENCRYPTION_REQUEST_ENCRYPTION_NOT_REQUESTED = 0x0
    LINK_ENCRYPTION_REQUEST_ENCRYPTION_REQUESTED = 0x1


class OFFSET_HDCP2_CTL:
    HDCP2_CTL_TCA = 0x664B0
    HDCP2_CTL_TCB = 0x665B0
    HDCP2_CTL_TCC = 0x666B0
    HDCP2_CTL_TCD = 0x667B0


class _HDCP2_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 29),
        ('VbidTypeSelect', ctypes.c_uint32, 2),
        ('LinkEncryptionRequest', ctypes.c_uint32, 1),
    ]


class REG_HDCP2_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 29
    VbidTypeSelect = 0  # bit 29 to 31
    LinkEncryptionRequest = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP2_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP2_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_LINK_AUTHENTICATION_STATUS(Enum):
    LINK_AUTHENTICATION_STATUS_NOT_AUTHENTICATED = 0x0
    LINK_AUTHENTICATION_STATUS_AUTHENTICATED = 0x1


class ENUM_LINK_TYPE_STATUS(Enum):
    LINK_TYPE_STATUS_TYPE_0 = 0x0
    LINK_TYPE_STATUS_TYPE_1 = 0x1


class OFFSET_HDCP2_STATUS:
    HDCP2_STATUS_TCA = 0x664B4
    HDCP2_STATUS_TCB = 0x665B4
    HDCP2_STATUS_TCC = 0x666B4
    HDCP2_STATUS_TCD = 0x667B4


class _HDCP2_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 20),
        ('LinkEncryptionStatus', ctypes.c_uint32, 1),
        ('LinkAuthenticationStatus', ctypes.c_uint32, 1),
        ('LinkTypeStatus', ctypes.c_uint32, 1),
        ('Reserved23', ctypes.c_uint32, 9),
    ]


class REG_HDCP2_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 20
    LinkEncryptionStatus = 0  # bit 20 to 21
    LinkAuthenticationStatus = 0  # bit 21 to 22
    LinkTypeStatus = 0  # bit 22 to 23
    Reserved23 = 0  # bit 23 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP2_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP2_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CLEAR_KEYS(Enum):
    CLEAR_KEYS_DO_NOT_CLEAR = 0x0
    CLEAR_KEYS_CLEAR = 0x1


class ENUM_FORCE_CLEAR_INPUTCTR(Enum):
    FORCE_CLEAR_INPUTCTR_DO_NOT_FORCE = 0x0
    FORCE_CLEAR_INPUTCTR_FORCE_CLEAR = 0x1


class ENUM_LINK_TYPE(Enum):
    LINK_TYPE_TYPE_0 = 0x0  # Type 0 content may be be transmitted to all HDCP receivers.
    LINK_TYPE_TYPE_1 = 0x1  # Type 1 content must not be transmitted to HDCP 1.x or HDCP 2.0 receivers.


class ENUM_LINK_AUTHENTICATED(Enum):
    LINK_AUTHENTICATED_NOT_AUTHENTICATED_ENCRYPTION_NOT_ALLOWED = 0x0
    LINK_AUTHENTICATED_AUTHENTICATED_ENCRYPTION_ALLOWED = 0x1


class OFFSET_HDCP2_AUTH:
    HDCP2_AUTH_TCA = 0x66498
    HDCP2_AUTH_TCB = 0x66598
    HDCP2_AUTH_TCC = 0x66698
    HDCP2_AUTH_TCD = 0x66798


class _HDCP2_AUTH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 18),
        ('ClearKeys', ctypes.c_uint32, 1),
        ('ForceClearInputctr', ctypes.c_uint32, 1),
        ('Reserved20', ctypes.c_uint32, 10),
        ('LinkType', ctypes.c_uint32, 1),
        ('LinkAuthenticated', ctypes.c_uint32, 1),
    ]


class REG_HDCP2_AUTH(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 18
    ClearKeys = 0  # bit 18 to 19
    ForceClearInputctr = 0  # bit 19 to 20
    Reserved20 = 0  # bit 20 to 30
    LinkType = 0  # bit 30 to 31
    LinkAuthenticated = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP2_AUTH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP2_AUTH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP2_INPUTCTR:
    HDCP2_INPUTCTR_TCA = 0x664B8
    HDCP2_INPUTCTR_TCB = 0x665B8
    HDCP2_INPUTCTR_TCC = 0x666B8
    HDCP2_INPUTCTR_TCD = 0x667B8


class _HDCP2_INPUTCTR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('InputctrLower', ctypes.c_uint32, 32),
    ]


class REG_HDCP2_INPUTCTR(ctypes.Union):
    value = 0
    offset = 0

    InputctrLower = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP2_INPUTCTR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP2_INPUTCTR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP2_RIV:
    HDCP2_RIV_TCA = 0x66490
    HDCP2_RIV_TCB = 0x66590
    HDCP2_RIV_TCC = 0x66690
    HDCP2_RIV_TCD = 0x66790


class _HDCP2_RIV(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RivDword0', ctypes.c_uint32, 32),
    ]


class REG_HDCP2_RIV(ctypes.Union):
    value = 0
    offset = 0

    RivDword0 = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP2_RIV),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP2_RIV, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HDCP2_SKEY:
    HDCP2_SKEY_TCA = 0x66480
    HDCP2_SKEY_TCB = 0x66580
    HDCP2_SKEY_TCC = 0x66680
    HDCP2_SKEY_TCD = 0x66780


class _HDCP2_SKEY(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SessionKeyDword0', ctypes.c_uint32, 32),
        ('SessionKeyDword1', ctypes.c_uint32, 32),
        ('SessionKeyDword2', ctypes.c_uint32, 32),
        ('SessionKeyDword3', ctypes.c_uint32, 32),
    ]


class REG_HDCP2_SKEY(ctypes.Union):
    value = 0
    offset = 0

    SessionKeyDword0 = 0  # bit 0 to 32
    SessionKeyDword1 = 0  # bit 0 to 32
    SessionKeyDword2 = 0  # bit 0 to 32
    SessionKeyDword3 = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP2_SKEY),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP2_SKEY, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_STREAM_TYPE_STATUS(Enum):
    STREAM_TYPE_STATUS_TYPE_1 = 0x1
    STREAM_TYPE_STATUS_TYPE_0 = 0x0


class ENUM_STREAM_ENCRYPTION_STATUS(Enum):
    STREAM_ENCRYPTION_STATUS_NOT_ENCRYPTING = 0x0
    STREAM_ENCRYPTION_STATUS_ENCRYPTING = 0x1


class OFFSET_HDCP2_STREAM_STATUS:
    HDCP2_STREAM_STATUS_TCA = 0x664C0
    HDCP2_STREAM_STATUS_TCB = 0x665C0
    HDCP2_STREAM_STATUS_TCC = 0x666C0
    HDCP2_STREAM_STATUS_TCD = 0x667C0


class _HDCP2_STREAM_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 30),
        ('StreamTypeStatus', ctypes.c_uint32, 1),
        ('StreamEncryptionStatus', ctypes.c_uint32, 1),
    ]


class REG_HDCP2_STREAM_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 30
    StreamTypeStatus = 0  # bit 30 to 31
    StreamEncryptionStatus = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDCP2_STREAM_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDCP2_STREAM_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

