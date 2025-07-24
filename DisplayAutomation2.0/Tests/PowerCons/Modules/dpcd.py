    #######################################################################################################################
# @file         dpcd.py
# @brief        Contains DPCD offsets, Enums, structures with bit wise definitions based on DP spec and common functions
#               to access DPCD
# @details      @ref dpcd.py is a common library for all DPCD related operations. It provides below generic functions to
#               read DPCD:
#                   1. read()   : to read the DPCD value directly from Panel
#                   2. get()    : get the value from cache if present, otherwise read from panel and store in cache
#               Apart from above two functions, this library contains some feature specific DPCD helper functions given
#               below:
#                   1. get_edp_revision()   : to get eDP revision from DPCD
#                   2. get_psr_version()    : to get PSR version from DPCD
#
# @author       Rohit Kumar
#######################################################################################################################

import ctypes
import logging

from enum import IntEnum

from Libs.Core import enum, driver_escape
from Libs.Core.display_config import display_config
from Libs.Core.wrapper import driver_escape_args

__MAX_POLL_COUNT = 2
__DSC_CAPS_SIZE = 11


##
# @brief        Exposed enum for DPCD offsets
class Offsets(IntEnum):
    DPCD_REV = 0x0
    MAX_LINK_RATE = 0x1
    MAX_LANE_COUNT = 0x2
    MAX_DOWNSPREAD = 0x3
    DOWN_STREAM_PORT_PRESENT = 0x5
    DOWN_STREAM_PORT_COUNT = 0x7
    EDP_CONFIGURATION_CAP = 0xD
    EXTENDED_RECEIVER_CAPABILITY_FIELD_PRESENT = 0xE
    MSTM_CAP = 0x21
    ALPM_CAP = 0x2E
    DSC_SUPPORT = 0x60
    DSC_VERSION = 0x61
    DSC_RC_BUFFER_BLOCK_SIZE = 0x62
    DSC_RC_BUFFER_SIZE = 0x63
    DSC_SLICE_CAPABILITIES_1 = 0x64
    DSC_LINE_BUFFER_DEPTH = 0x65
    DSC_BLOCK_PREDICTION_SUPPORT = 0x66
    DSC_MAX_BPP_SUPPORTED_SINK_1 = 0x67
    DSC_MAX_BPP_SUPPORTED_SINK_2 = 0x68
    DSC_COLOUR_SUPPORTED = 0x69
    DSC_BPC_SUPPORT = 0x6A
    DSC_PEAK_DSC_THROUGHPUT = 0x6B
    DSC_MAX_SLICE_WIDTH = 0x6C
    DSC_SLICE_CAPABILITIES_2 = 0x6D
    DSC_BPP_INCREMENT = 0x6F
    PSR_CAPS_SUPPORTED_AND_VERSION = 0x70
    PANEL_SELF_REFRESH_CAPABILITIES = 0x71
    PSR2_Y_GRANULARITY_CAPABILITY = 0x74
    AUX_FRAME_SYNC_SUPPORT = 0x7F
    DOWN_STREAM_PORTX_BPC_CAPS = 0x82
    PANEL_REPLAY_CAPABILITY_SUPPORTED = 0xB0
    PANEL_REPLAY_CAPABILITY = 0xB1
    PR_Y_GRANULARITY_CAPABILITY = 0xB4
    LINK_BW_SET = 0x100
    LANE_COUNT_SET = 0x101
    TRAINING_LANE0_SET = 0x103
    DOWN_SPREAD_CTL = 0x107
    EDP_CONFIGURATION_SET = 0x10A
    MSTM_CTRL = 0x111
    LINK_RATE_SET = 0x115
    ADAPTIVE_SYNC_SDP_TRANSMISSION_TIMING_CONFIG = 0x11B
    DSC_SINK_CONFIG = 0x160
    PSR_CONFIGURATION = 0x170
    PANEL_REPLAY_ENABLE_AND_CONFIGURATION = 0x1B0
    ADAPTIVE_SYNC_MAX_SHIFT = 0x310
    LRR_UBRR_CAPS = 0x314
    ALRR_UBRR_CONFIG = 0x316
    EDP_HDR_CAPS = 0x341
    EDP_HDR_GET_SET_CTRL_PARAMS = 0x344
    EDP_BRIGHTNESS_NITS = 0x354
    EDP_BRIGHTNESS_OPTIMIZATION = 0x358
    DPCD_VER = 0x700
    EDP_GENERAL_CAPS_REG = 0x701
    EDP_GENERAL_CAPABILITY_2 = 0x703
    EDP_BACKLIGHT_MODE_SET = 0x721
    EDP_DISPLAY_CONTROL_2 = 0x730
    PANEL_TARGET_LUMINANCE_VALUE = 0x734
    EDP_MSO_CAPS = 0x7A4
    PSR2_ERROR_STATUS = 0x2006
    SINK_DEVICE_PSR_STATUS = 0x2008
    SINK_AUX_FRAME_SYNC_STATUS = 0x2010
    PANEL_REPLAY_ERROR_STATUS = 0x2020
    DOWN_STREAM_PORT_COUNT_EXTENDED = 0x2207
    DP_RX_FEATURE_ENUMERATION_LIST = 0x2210
    ADAPTIVE_SYNC_CAPABILITY = 0x2214


##
# @brief        Exposed enum for DPCD revision
class DpcdRevision(IntEnum):
    DPCD_1_0 = 0x10
    DPCD_1_1 = 0x11
    DPCD_1_2 = 0x12
    DPCD_1_3 = 0x13
    DPCD_1_4 = 0x14


##
# @brief        Exposed enum for eDP DPCD revision
class EdpDpcdRevision(IntEnum):
    EDP_DPCD_1_1_OR_LOWER = 0
    EDP_DPCD_1_2 = 1
    EDP_DPCD_1_3 = 2
    EDP_DPCD_1_4 = 3
    EDP_DPCD_1_4_A = 4
    EDP_DPCD_1_4_B = 5
    EDP_DPCD_1_5 = 6
    EDP_DPCD_MAX = 7
    EDP_UNKNOWN = 10


##
# @brief        Exposed enum for eDP PSR version
class EdpPsrVersion(IntEnum):
    EDP_PSR_NONE = 0
    EDP_PSR_1 = 1
    EDP_PSR_2 = 2
    EDP_PSR_2_Y = 3
    EDP_PSR_2_ET = 4
    EDP_PSR_MAX = 5
    EDP_PSR_UNKNOWN = 10

    # ##
    # # @brief       This function is used to get the enumeration member with the given name
    # # @param[in]   name string name of the enum member to be returned
    # # @return      enum member for the given name
    # @classmethod
    # def get(cls, name):
    #     for k, v in cls._members_.items():
    #         if k == name:
    #             return v
    #     raise ValueError("No enumeration member with name %r" % name)


##
# @brief        Exposed enum for DP DSC version
class DpDscVersion(IntEnum):
    DP_DSC_NONE = 0
    DP_DSC_1_1 = 1
    DP_DSC_1_2 = 2


##
# @brief        Exposed enum for system power state
class PowerState(IntEnum):
    AC_MODE = 1
    DC_MODE = 0


##
# @brief        Exposed enum for ideal capability for TCON usage
class IdealCapability(IntEnum):
    UNKNOWN = 0
    DESKTOP = 1
    FULL_SCREEN_MEDIA = 2
    FULL_SCREEN_GAMING = 3


##
# @brief        Exposed enum for DP_BASE_DFP_TYPE_ENUM
class DpBaseDfpType(IntEnum):
    DP_DWN_STREAM_PORT_DP = 0x0
    DP_DWN_STREAM_PORT_VGA = 0x1
    DP_DWN_STREAM_PORT_HDMI = 0x2
    DP_DWN_STREAM_PORT_OTHER = 0x3


##
# @brief        Exposed enum for UBRR Config Status
class UbrrStatus(IntEnum):
    UBRR_DISABLE = 0x0
    UBZRR_ENABLE = 0x1
    UBLRR_ENABLE = 0x2
    UBRR_INVALID = 0x3


##
# @brief        Exposed enum for ALRR Config Status
class AlrrStatus(IntEnum):
    DISABLE = 0x0
    ENABLE = 0x1


##
# @brief        Exposed enum for PixOptix Config Status
class PixOptixStatus(IntEnum):
    DISABLE = 0x0
    ENABLE = 0x1


##
# @brief        Exposed Structure for Max Lane Count Fields
#               MAX_LANE_COUNT 0x00002
class MaxLaneCountFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("max_lane_count", ctypes.c_uint8, 5),
        ("reserved_1", ctypes.c_uint8, 1),
        ("tps3_supported", ctypes.c_uint8, 1),
        ("enhanced_frame_cap", ctypes.c_uint8, 1)
    ]


##
# @brief        Exposed union for Max Lane Counts
class MaxLaneCount(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MaxLaneCountFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values to get the register values for MaxLaneCount Union
    # @param[in]    target_id target id of the panel
    def __init__(self, target_id):
        super(MaxLaneCount, self).__init__()
        self.value = get(target_id, Offsets.MAX_LANE_COUNT)


##
# @brief        class structure for max down spread fields
# @details      MAX_DOWNSPREAD 0x00003
#               MAX_DOWNSPREAD: used to get FastLinkTraining capability of connected panel
#               bits 6    -   0: Fast Link training not supported
#               1: Fast Link Training is supported
class MaxDownSpreadFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("max_downspread", ctypes.c_uint8, 1),
        ("reserved_1", ctypes.c_uint8, 5),
        ("no_aux_handshake_link_training", ctypes.c_uint8, 1),
        ("tps4_supported", ctypes.c_uint8, 1)
    ]


##
# @brief        Exposed union for max down spread
class MaxDownSpread(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MaxDownSpreadFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for Max Down Spread Union
    # @param[in]    target_id target id of the panel
    def __init__(self, target_id):
        super(MaxDownSpread, self).__init__()
        self.value = get(target_id, Offsets.MAX_DOWNSPREAD)


##
# @brief        Exposed Structure for Down Stream Port Present Fields
#               DOWN_STREAM_PORT_PRESENT 0x00005
class DownStreamPortPresentFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dfp_present", ctypes.c_uint8, 1),  # Bit 0
        ("dfp_type", ctypes.c_uint8, 2),  # Bit 2:1
        ("format_conversion", ctypes.c_uint8, 1),  # Bit 3
        ("detailed_cap_info_available", ctypes.c_uint8, 1),  # Bit 4
        ("reserved", ctypes.c_uint8, 3)  # Bit 7:5
    ]


##
# @brief       Exposed union for Down Stream Port Present
class DownStreamPortPresent(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DownStreamPortPresentFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DownStreamPortPresent Union
    # @param[in]    target_id target id of the panel
    def __init__(self, target_id):
        super(DownStreamPortPresent, self).__init__()
        self.value = get(target_id, Offsets.DOWN_STREAM_PORT_PRESENT)


##
# @brief       Exposed Structure for Down Stream Port Count Fields
#              DOWN_STREAM_PORT_COUNT 0x00007/0x02207
class DownStreamPortCountFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("port_count", ctypes.c_uint8, 4),  # Bit 0:3 The number of downstream ports.
        ("reserved_2", ctypes.c_uint8, 2),  # Bit 4:5
        ("msa_timing_par_ignored", ctypes.c_uint8, 1),  # Bit 6
        ("oui_support", ctypes.c_uint8, 1)  # Bit 7
    ]


##
# @brief       Exposed Union for Down Stream Port Count
class DownStreamPortCount(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DownStreamPortCountFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DownStreamPortCount Union
    # @param[in]    target_id target id of the panel
    def __init__(self, target_id):
        super(DownStreamPortCount, self).__init__()
        self.value = get(target_id, Offsets.DOWN_STREAM_PORT_COUNT)


##
# @brief       Exposed Union for Extended Down Stream Port Count
class ExtendedDownStreamPortCount(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DownStreamPortCountFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for ExtendedDownStreamPortCount Union
    # @param[in]    target_id target id of the panel
    def __init__(self, target_id):
        super(ExtendedDownStreamPortCount, self).__init__()
        self.value = get(target_id, Offsets.DOWN_STREAM_PORT_COUNT_EXTENDED)


##
# @brief       Exposed Structure for Extended Receiver Capability Filed present
#              EXTENDED_RECEIVER_CAPABILITY_FIELD_PRESENT 0x0000E
class ExtendedReceiverCapFieldPresentField(ctypes.LittleEndianStructure):
    _fields_ = [
        ("training_aux_rd_interval", ctypes.c_uint8, 7),  # Bit 0:6 The number of downstream ports.
        ("extended_receiver_capability_field_present", ctypes.c_uint8, 1)  # Bit 7
    ]


##
# @brief       Exposed Union for Down Stream Port Count
class ExtendedRxCapFieldPresent(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", ExtendedReceiverCapFieldPresentField),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DownStreamPortCount Union
    # @param[in]    target_id target id of the panel
    def __init__(self, target_id):
        super(ExtendedRxCapFieldPresent, self).__init__()
        self.value = get(target_id, Offsets.EXTENDED_RECEIVER_CAPABILITY_FIELD_PRESENT)


##
# @brief       Exposed Structure for Edp Configuration Cap Fields
# EDP_CONFIGURATION_CAP 0x0000D
class EdpConfigurationCapFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("alternate_scrambler_reset_capable", ctypes.c_uint8, 1),  # Bit 0
        ("reserved_1", ctypes.c_uint8, 1),
        ("reserved_2", ctypes.c_uint8, 1),
        ("dpcd_display_control_capable", ctypes.c_uint8, 1),
        ("reserved_3", ctypes.c_uint8, 4)
    ]


##
# @brief       Exposed class for Down Stream Port Count
class EdpConfigurationCap(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", EdpConfigurationCapFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for EdpConfigurationCap Union
    # @param[in]    target_id target id of the panel
    def __init__(self, target_id):
        super(EdpConfigurationCap, self).__init__()
        self.value = get(target_id, Offsets.EDP_CONFIGURATION_CAP)


##
# @brief       Exposed Structure for Psr Caps Supported And VersionFields
#              PSR_CAPS_SUPPORTED_AND_VERSION 0x00070
class PsrCapsSupportedAndVersionFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("psr_support_and_version", ctypes.c_uint8, 8)  # Bit 0:7
    ]


##
# @brief       Exposed Union for Psr Caps Supported And VersionFields
class PsrCapsSupportedAndVersion(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PsrCapsSupportedAndVersionFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for PsrCapsSupportedAndVersion Union
    # @param[in]    target_id target id of the panel
    def __init__(self, target_id):
        super(PsrCapsSupportedAndVersion, self).__init__()
        self.value = get(target_id, Offsets.PSR_CAPS_SUPPORTED_AND_VERSION)


##
# @brief       Exposed Structure for Dp DownStream Portx Bpc Caps Fields
class DpDownStreamPortxBpcCapsFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("down_stream_portx_bpc", ctypes.c_uint8, 2),  # Bit 1:0
        ("pcon_max_encoded_link_bw", ctypes.c_uint8, 3),  # Bit 4:2
        ("pcon_source_control_mode_support", ctypes.c_uint8, 1),  # Bit 5
        ("pcon_concurrent_or_sequential_mode_support", ctypes.c_uint8, 1),  # Bit 6
        ("reserved", ctypes.c_uint8, 1)  # Bit 7
    ]


##
# @brief       Exposed Union for Dp DownStream Portx Bpc Caps
class DpDownStreamPortxBpcCaps(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpDownStreamPortxBpcCapsFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for Dp DownStreamPortxBpcCaps Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DpDownStreamPortxBpcCaps, self).__init__()
        self.value = get(target_id, Offsets.DOWN_STREAM_PORTX_BPC_CAPS)


##
# @brief       Exposed Structure for Lane Count Set Fields
#              LANE_COUNT_SET 0x00101
class LaneCountSetFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("lane_count_set", ctypes.c_uint8, 5),
        ("post_lt_adj_req_granted", ctypes.c_uint8, 1),
        ("reserved_1", ctypes.c_uint8, 1),
        ("enhanced_frame_cap", ctypes.c_uint8, 1)
    ]


##
# @brief       Exposed Union for Lane Count Set
class LaneCountSet(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", LaneCountSetFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for LaneCountSet Union
    # @param[in]    target_id target id of the panel
    def __init__(self, target_id):
        super(LaneCountSet, self).__init__()
        self.value = get(target_id, Offsets.LANE_COUNT_SET)


##
# @brief       Exposed Structure for Lane Count Set
# @details     TRAINING_LANE0_SET: voltage swing and pre-emphasis values
#              bits 1:0  -   voltage swing level (0, 1, 2, 3)
#              bits 4:3  -   pre-emphasis level (0, 1, 2, 3)
class TrainingLane0SetFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("voltage_swing_level", ctypes.c_uint8, 2),
        ("pre_emphasis_level", ctypes.c_uint8, 2),
        ("reserved_1", ctypes.c_uint8, 4)
    ]


##
# @brief       Exposed Union for Lane0 Set
class TrainingLane0Set(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TrainingLane0SetFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for TrainingLane0Set Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(TrainingLane0Set, self).__init__()
        self.value = read(target_id, Offsets.TRAINING_LANE0_SET)


##
# @brief       Exposed Structure for Down Spread Ctl Fields
#              DOWN_SPREAD_CTL 0x00107
class DownSpreadCtlFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_1", ctypes.c_uint8, 7),  # Bit 0:6
        ("msa_timing_par_ignored_en", ctypes.c_uint8, 1)  # Bit 7
    ]


##
# @brief       Exposed Union for Down Spread Ctl
class DownSpreadCtl(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DownSpreadCtlFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DownSpreadCtl Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DownSpreadCtl, self).__init__()
        self.value = get(target_id, Offsets.DOWN_SPREAD_CTL)


##
# @brief       Exposed Structure for Edp Configuration Set Fields
#              EDP_CONFIGURATION_SET 0x0010A
class EdpConfigurationSetFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("alternate_scrambler_reset_enable", ctypes.c_uint8, 1),  # Bit 0
        ("reserved_1", ctypes.c_uint8, 6),
        ("panel_self_test_enable", ctypes.c_uint8, 1)
    ]


##
# @brief       Exposed Union for Edp Configuration Set
class EdpConfigurationSet(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", EdpConfigurationSetFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for EdpConfigurationSet Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(EdpConfigurationSet, self).__init__()
        self.value = read(target_id, Offsets.EDP_CONFIGURATION_SET)


##
# @brief       Exposed Structure for AdaptiveSync MaxShift Fields
#              DPCD_ADAPTIVE_SYNC_MAX_SHIFT 0x00310
class AdaptiveSyncMaxShiftFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("increment", ctypes.c_uint32, 14),
        ("reserved_2", ctypes.c_uint32, 2),
        ("decrement", ctypes.c_uint32, 14),
        ("reserved_2", ctypes.c_uint32, 2)
    ]


##
# @brief       Exposed Union for AdaptiveSync MaxShift
class AdaptiveSyncMaxShift(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", AdaptiveSyncMaxShiftFields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief       Initializer to get the register values for AdaptiveSyncMaxShift Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(AdaptiveSyncMaxShift, self).__init__()
        dpcd_bytes = get(target_id, Offsets.ADAPTIVE_SYNC_MAX_SHIFT, size=4)
        self.value = int(('0x' + ''.join('{:02x}'.format(x) for x in dpcd_bytes[::-1])), 16)


##
# @brief       Exposed Structure for Lrr Ubrr Caps Fields
#              LRR_UBRR_CAPS 0x00314
class LrrUbrrCapsFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("source_pixel_clock_based", ctypes.c_uint8, 1),
        ("t_con_based", ctypes.c_uint8, 1),  # RR switch done by TCON in idle case
        ("source_v_total_based", ctypes.c_uint8, 1),  # TCON supports VTOTAL change between PSR entry/exit
        ("ubzrr_supported", ctypes.c_uint8, 1),  # UB-ZRR
        ("ublrr_supported", ctypes.c_uint8, 1),  # UB-LRR
        ("alrr_supported", ctypes.c_uint8, 1),
        ("reserved", ctypes.c_uint8, 2)
    ]


##
# @brief       Exposed Union for Lrr Ubrr Caps
class LrrUbrrCaps(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", LrrUbrrCapsFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for LrrUbrrCaps Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(LrrUbrrCaps, self).__init__()
        self.value = get(target_id, Offsets.LRR_UBRR_CAPS)


##
# @brief       Exposed Structure for Alrr Ubrr Config Fields
#              ALRR_UBRR_CONFIG 0x00316
class AlrrUbrrConfigFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("enable_ubrr", ctypes.c_uint8, 2),  # 00-Disable, 01-Enable UBZRR, 10-Enable UBLRR
        ("enable_alrr", ctypes.c_uint8, 1),
        ("reserved", ctypes.c_uint8, 5)
    ]


##
# @brief       Exposed Union for Alrr Ubrr Config
class AlrrUbrrConfig(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", AlrrUbrrConfigFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for AlrrUbrrConfig Union
    # @param[in]   target_id target id of the panel
    # @param[in]   dpcd_value to be used in the definition (Value in little endian uint8)
    def __init__(self, target_id, dpcd_value=None):
        super(AlrrUbrrConfig, self).__init__()
        self.value = get(target_id, Offsets.ALRR_UBRR_CONFIG) if dpcd_value is None else dpcd_value


##
# @brief       Exposed Structure for Edp General Caps Reg Fields
#              EDP_GENERAL_CAPS_REG 0x00701
class EdpGeneralCapsRegFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("t_con_backlight_adjustment_capable", ctypes.c_uint8, 1),
        ("backlight_pin_enable_capable", ctypes.c_uint8, 1),
        ("backlight_aux_enable_capable", ctypes.c_uint8, 1),
        ("panel_self_test_pin_enable_capable", ctypes.c_uint8, 1),
        ("panel_self_test_aux_enable_capable", ctypes.c_uint8, 1),
        ("frc_enable_capable", ctypes.c_uint8, 1),
        ("color_engine_capable", ctypes.c_uint8, 1),
        ("set_power_capable", ctypes.c_uint8, 1)
    ]


##
# @brief       Exposed Union for Edp General Caps Reg
class EdpGeneralCapsReg(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", EdpGeneralCapsRegFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for EdpGeneralCapsReg Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(EdpGeneralCapsReg, self).__init__()
        self.value = get(target_id, Offsets.EDP_GENERAL_CAPS_REG)


##
# @brief       Exposed Structure for Dsc Caps Fields
#              DSC_CAPS_REG 0x00060
class DscCapsFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dsc_support", ctypes.c_ubyte, 1),  # 0 to 0  #DPCD 60
        ("reserved", ctypes.c_ubyte, 7)
    ]


##
# @brief       Exposed Union for Dsc Support
class DscSupport(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscCapsFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscSupport Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscSupport, self).__init__()
        self.value = get(target_id, Offsets.DSC_SUPPORT)


##
# @brief       Exposed Union for Dsc Sink Config Fields
#              DSC_SINK_CONFIG 0x00160
class DscSinkConfigFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("decompression_enable", ctypes.c_ubyte, 1),  # 0 to 0  #DPCD 60
        ("reserved", ctypes.c_ubyte, 7)
    ]


##
# @brief       Exposed Union for Dsc Sink Config
class DscSinkConfig(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscSinkConfigFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscSinkConfig Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscSinkConfig, self).__init__()
        self.value = get(target_id, Offsets.DSC_SINK_CONFIG)


##
# @brief       Exposed Structure for Dsc Version Fields
#              DSC_VERSION = 0x61
class DscVersionFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dsc_version_major", ctypes.c_ubyte, 4),
        ("dsc_version_minor", ctypes.c_ubyte, 4)
    ]


##
# @brief       Exposed Union for Dsc Version
class DscVersion(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscVersionFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscVersion Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscVersion, self).__init__()
        self.value = get(target_id, Offsets.DSC_VERSION)


##
# @brief       Exposed Structure for RC Buffer Block Size Fields
#              DSC_RC_BUFFER_BLOCK_SIZE = 0x62
class RCBufferBlockSizeFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_buffer_block_size", ctypes.c_ubyte, 2),  # 0 to 1 # DPCD 62
        ("reserved_2", ctypes.c_ubyte, 6),  # 2 to 7
    ]


##
# @brief       Exposed Union for RC Buffer Block Size
class DpRCBufferBlockSize(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", RCBufferBlockSizeFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DpRCBufferBlockSize Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DpRCBufferBlockSize, self).__init__()
        self.value = get(target_id, Offsets.DSC_RC_BUFFER_BLOCK_SIZE)


##
# @brief       Exposed Structure for RC Buffer Size Fields
#              DSC_RC_BUFFER_SIZE = 0x63
class RCBufferSizeFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("each_rate_buffer_size_in_units_of_blocks", ctypes.c_ubyte, 8)]


##
# @brief       Exposed Union for RC Buffer Size
class RCBufferSize(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", RCBufferSizeFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for RCBufferSize Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(RCBufferSize, self).__init__()
        self.value = get(target_id, Offsets.DSC_RC_BUFFER_SIZE)


##
# @brief       Exposed Structure for Dsc Slice Capabilities1 Fields
#              DSC_SLICE_CAPABILITIES_1 = 0x64
class DscSliceCapabilities1Fields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("one_slice_per_line", ctypes.c_ubyte, 1),  # 0 to 0
        ("two_slice_per_line", ctypes.c_ubyte, 1),  # 1 to 1
        ("reserved_3", ctypes.c_ubyte, 1),  # 2 to 2
        ("four_slice_per_line", ctypes.c_ubyte, 1),  # 3 to 3
        ("six_slice_per_line", ctypes.c_ubyte, 1),  # 4 to 4 Not part of Standard slice value number set
        ("eight_slice_per_line", ctypes.c_ubyte, 1),  # 5 to 5
        ("ten_slice_per_line", ctypes.c_ubyte, 1),  # 6 to 6 Not part of Standard slice value number set
        ("twelve_slice_per_line", ctypes.c_ubyte, 1),  # 7 to 7
    ]


##
# @brief       Exposed Union for Dsc Slice Capabilities1
class DscSliceCapabilities1(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscSliceCapabilities1Fields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscSliceCapabilities1 Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscSliceCapabilities1, self).__init__()
        self.value = get(target_id, Offsets.DSC_SLICE_CAPABILITIES_1)


##
# @brief       Exposed Structure for Dsc Line Buffer Depth Fields
#              DSC_LINE_BUFFER_DEPTH = 0x65
class DscLineBufferDepthFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("line_buffer_bit_depth", ctypes.c_ubyte, 3),  # 0 to 2
        ("reserved_5", ctypes.c_ubyte, 5),  # 3 to 7
    ]


##
# @brief       Exposed Union for Dsc Line Buffer Depth Fields
class DscLineBufferDepth(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscLineBufferDepthFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscLineBufferDepth Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscLineBufferDepth, self).__init__()
        self.value = get(target_id, Offsets.DSC_LINE_BUFFER_DEPTH)


##
# @brief       Exposed Structure for Dsc Block Prediction Support Fields
#              DSC_BLOCK_PREDICTION_SUPPORT = 0x66
class DscBlockPredictionSupportFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("block_prediction_support", ctypes.c_ubyte, 1),  # 0 to 0 # DPCD 66
        ("reserved_6", ctypes.c_ubyte, 7),  # 1 to 7
    ]


##
# @brief       Exposed Union for Dsc Block Prediction Support
class DscBlockPredictionSupport(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscBlockPredictionSupportFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscBlockPredictionSupport Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscBlockPredictionSupport, self).__init__()
        self.value = get(target_id, Offsets.DSC_BLOCK_PREDICTION_SUPPORT)


##
# @brief       Exposed Structure for Dsc Max Bpp Supported Sink Fields
#              DSC_MAX_BPP_SUPPORTED_SINK = 0x67, 0x68
class DscMaxBppSupportedSinkFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("maximum_bpp_support_decompressor", ctypes.c_uint16, 10),  # DPCD 67,68
        ("reserved_7", ctypes.c_uint16, 6),
    ]


##
# @brief       Exposed Union for Dsc Max Bpp Supported Sink
class DscMaxBppSupportedSink(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscMaxBppSupportedSinkFields),
        ("value", ctypes.c_uint16)
    ]

    ##
    # @brief       Initializer to get the register values for DscMaxBppSupportedSink Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscMaxBppSupportedSink, self).__init__()
        byte_value = get(target_id, Offsets.DSC_MAX_BPP_SUPPORTED_SINK_1, 2)  # reading 2 Bytes
        # 0x68 - 0:1 Represents the Most Significant 2 Bits
        # 0x67 - 0:7 Represents the Least Significant 8 bits
        self.value = int('{:x}'.format(0b00000011 & byte_value[-1]) + '{:x}'.format(byte_value[0]), 16)


##
# @brief       Exposed Structure for Dsc Color Supported Fields
#              DSC_COLOUR_SUPPORTED = 0x69
class DscColorSupportedFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rgb_support", ctypes.c_ubyte, 1),  # 0 to 0
        ("ycbcr", ctypes.c_ubyte, 1),  # 1 to 1
        ("ycbcr_4_2_2_support", ctypes.c_ubyte, 1),  # 2 to 2
        ("reserved_8", ctypes.c_ubyte, 5),  # 3 to 7
    ]


##
# @brief       Exposed Union for Dsc Color Supported
class DscColorSupported(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscColorSupportedFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscColorSupported Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscColorSupported, self).__init__()
        self.value = get(target_id, Offsets.DSC_COLOUR_SUPPORTED)


##
# @brief       Exposed Structure for Dsc Bpc Support Fields
#              DSC_BPC_SUPPORT = 0x6A
class DscBpcSupportFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_9", ctypes.c_ubyte, 1),  # 0 to 0
        ("bits_per_color_support_8", ctypes.c_ubyte, 1),  # 1 to 1
        ("bits_per_color_support_10", ctypes.c_ubyte, 1),  # 2 to 2
        ("bits_per_color_support_12", ctypes.c_ubyte, 1),  # 3 to 3
        ("reserved_10", ctypes.c_ubyte, 4),  # 4 to 7
    ]


##
# @brief       Exposed Union for Dsc Bpc Support
class DscBpcSupport(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscBpcSupportFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscBpcSupport Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscBpcSupport, self).__init__()
        self.value = get(target_id, Offsets.DSC_BPC_SUPPORT)


##
# @brief       Exposed Structure for Dsc Peak Dsc Throughput Fields
#              DSC_PEAK_DSC_THROUGHPUT = 0x6B
class DscPeakDscThroughputFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("throughput_mode_0", ctypes.c_ubyte, 4),  # 0 to 3
        ("throughput_mode_1", ctypes.c_ubyte, 4)  # 4 to 7
    ]


##
# @brief       Exposed Union for Dsc Peak Dsc Throughput
class DscPeakDscThroughput(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscPeakDscThroughputFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscPeakDscThroughput Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscPeakDscThroughput, self).__init__()
        self.value = get(target_id, Offsets.DSC_PEAK_DSC_THROUGHPUT)  # reading 2 Bytes


##
# @brief       Exposed Union for Dsc Slice Capabilities2 Fields
#              DSC_SLICE_CAPABILITIES_2 = 0x6D
class DscSliceCapabilities2Fields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("sixteen_slice_per_line", ctypes.c_ubyte, 1),  # 0 to 0
        ("twenty_slice_per_line", ctypes.c_ubyte, 1),  # 1 to 1
        ("twenty_four_slice_per_line", ctypes.c_ubyte, 1),  # 2 to 2
        ("reserved_5", ctypes.c_ubyte, 5),  # 4 to 7
    ]


##
# @brief       Exposed Union for Dsc Slice Capabilities2
class DscSliceCapabilities2(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscSliceCapabilities2Fields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscSliceCapabilities2 Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscSliceCapabilities2, self).__init__()
        self.value = get(target_id, Offsets.DSC_SLICE_CAPABILITIES_2)  # reading 2 Bytes


##
# @brief       Exposed Structure for Dsc Bpp Increment Fields
#              DSC_BPP_INCREMENT = 0x6F
class DscBppIncrementFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dsc_bpp_increment", ctypes.c_ubyte, 1),  # 0 to 2
        ("reserved_5", ctypes.c_ubyte, 4),  # 3 to 7
    ]


##
# @brief       Exposed Union for Dsc Bpp Increment
class DscBppIncrement(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscBppIncrementFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for DscBppIncrement Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(DscBppIncrement, self).__init__()
        self.value = get(target_id, Offsets.DSC_BPP_INCREMENT)  # reading 2 Bytes


##
# @brief       Exposed Structure for Edp Mso Caps Fields
#              EDP_MSO_CAPS  = 0x7A4
class EdpMsoCapsFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("no_of_links", ctypes.c_ubyte, 3),  # 0 to 2
        ("independent_link_bit", ctypes.c_ubyte, 1),  # 4
        ("reserved_6", ctypes.c_ubyte, 4),  # 4 to 7
    ]


##
# @brief       Exposed Union for Edp Mso Caps
class EdpMsoCaps(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", EdpMsoCapsFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for EdpMsoCaps Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(EdpMsoCaps, self).__init__()
        self.value = get(target_id, Offsets.EDP_MSO_CAPS)  # reading 2 Bytes


##
# @brief       Exposed Structure for Edp Hdr Caps Fields
# @details     Reports TCON capabilities
#              EDP_HDR_CAPS  = 0x341 to 0x343
class EdpHdrCapsFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("supports_2084_decode", ctypes.c_uint16, 1),  # 0
        ("supports_2020_gamut", ctypes.c_uint16, 1),  # 1
        ("support_panel_tone mapping", ctypes.c_uint16, 1),  # 2
        # Not applicable for OLED
        ("support_segmented_backlight", ctypes.c_uint16, 1),  # 3
        ("support_brightness_ctrl_in_nits_level_using_Aux", ctypes.c_uint16, 1),  # 4
        ("support_brightness_optimization", ctypes.c_uint16, 1),  # 5
        ("support_sdp_for_colorimetry", ctypes.c_uint16, 1),  # 6
        # useful for wide gamut panels with SDR desktop
        ("supports_sRGB_Panel_gamut_conversion", ctypes.c_uint16, 1),  # 7
        ("aux_only_brightness_for_sdr_hdr", ctypes.c_uint16, 1),  # 8
        ("reserved", ctypes.c_uint16, 7)  # 9 to 15
    ]


##
# @brief       Exposed Union for Hdr Caps
class HdrCaps(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", EdpHdrCapsFields),
        ("value", ctypes.c_uint16)
    ]

    ##
    # @brief       Initializer to get the register values for HdrCaps Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(HdrCaps, self).__init__()
        dpcd_bytes = get(target_id, Offsets.EDP_HDR_CAPS, size=2)
        self.value = 0
        if dpcd_bytes:
            self.value = int(('0x' + ''.join('{:02x}'.format(x) for x in dpcd_bytes[::-1])), 16)


##
# @brief       Exposed Structure for Edp Brightness Optimization Fields
# @details     Inform TCON of usage so that TCON can enable ideal capabilities
#              EDP_BRIGHTNESS_OPTIMIZATION = 0x358
class EdpBrightnessOptimizationFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("ideal_capabilities", ctypes.c_ubyte, 4),  # 0 to 3
        ("system_power_state", ctypes.c_ubyte, 1),  # 4
        ("optimization_strength", ctypes.c_ubyte, 3),  # 5 to 7
        #   Byte 1 - reserved
    ]


##
# @brief       Exposed Union for Edp Brightness Optimization
class EdpBrightnessOptimization(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", EdpBrightnessOptimizationFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for EdpBrightnessOptimization Union
    # @param[in]   target_id target id of the panel
    # @param[in]   dpcd_value to be used in the definition (Value in little endian uint8)
    def __init__(self, target_id, dpcd_value=None):
        super(EdpBrightnessOptimization, self).__init__()
        self.value = get(target_id, Offsets.EDP_BRIGHTNESS_OPTIMIZATION) if dpcd_value is None else dpcd_value


##
# @brief       Exposed Structure for Psr2 Error Status Fields
#              PSR2_ERROR_STATUS = 0x2006
class Psr2ErrorStatusFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("link_crc_error", ctypes.c_ubyte, 1),  # 0
        ("rfb_storage_error", ctypes.c_ubyte, 1),  # 1
        ("vsc_sdp_uncorrectable_error", ctypes.c_ubyte, 1),  # 2
        ("reserved", ctypes.c_ubyte, 5),  # 3:7
    ]


##
# @brief       Exposed Union for Psr2 Error Status
class Psr2ErrorStatus(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", Psr2ErrorStatusFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for Psr2 Error Status Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(Psr2ErrorStatus, self).__init__()
        self.value = get(target_id, Offsets.PSR2_ERROR_STATUS)


##
# @brief       Exposed Structure for Sink Device Psr Status Fields
#              SINK_DEVICE_PSR_STATUS = 0x2008
class SinkDevicePsrStatusFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("sink_device_self_refresh_status", ctypes.c_ubyte, 3),  # 0:2
        ("reserved", ctypes.c_ubyte, 5),  # 3:7
    ]


##
# @brief       Exposed Union for Sink Device Psr Status
class SinkDevicePsrStatus(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SinkDevicePsrStatusFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for SinkDevicePsrStatus Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(SinkDevicePsrStatus, self).__init__()
        self.value = get(target_id, Offsets.SINK_DEVICE_PSR_STATUS)


##
# @brief       Exposed Structure for Sink Aux Frame Sync Status Fields
#              SINK_AUX_FRAME_SYNC_STATUS = 0x200c
class SinkAuxFrameSyncStatusFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("aux_frame_sync_lock_error", ctypes.c_ubyte, 1),  # 0
        ("reserved", ctypes.c_ubyte, 7),  # 1:7
    ]


##
# @brief       Exposed Union for Sink Aux Frame Sync Status
class SinkAuxFrameSyncStatus(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SinkAuxFrameSyncStatusFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for SinkAuxFrameSyncStatus Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(SinkAuxFrameSyncStatus, self).__init__()
        self.value = get(target_id, Offsets.SINK_AUX_FRAME_SYNC_STATUS)


##
# @brief       Exposed Structure for AdaptiveSync Capability Fields
#              ADAPTIVE_SYNC_CAPABILITY 0x2214
class AdaptiveSyncCapabilityFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("adaptive_sync_sdp_supported", ctypes.c_uint8, 1),  # Bit 0
        ("as_sdp_first_half_line", ctypes.c_uint8, 1),  # Bit 1
        ("reserved", ctypes.c_uint8, 6)  # Bit 7:2
    ]


##
# @brief       Exposed Union for AdaptiveSync Capability
class AdaptiveSyncCapability(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", AdaptiveSyncCapabilityFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for AdaptiveSyncCapability Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(AdaptiveSyncCapability, self).__init__()
        self.value = get(target_id, Offsets.ADAPTIVE_SYNC_CAPABILITY)


##
# @brief       Exposed Structure for AdaptiveSync Capability Fields
#              ADAPTIVE_SYNC_SDP_TRANSMISSION_TIMING_CONFIG 0x11B
class AdaptiveSyncSdpTransmissionTimingConfigFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved", ctypes.c_uint8, 7),  # Bit 6:0
        ("as_sdp_one_line_earlier_enable", ctypes.c_uint8, 1)  # Bit 7
    ]


##
# @brief       Exposed Union for AdaptiveSync Capability
class AdaptiveSyncSdpTransmissionTimingConfig(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", AdaptiveSyncSdpTransmissionTimingConfigFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for AdaptiveSyncCapability Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(AdaptiveSyncSdpTransmissionTimingConfig, self).__init__()
        self.value = get(target_id, Offsets.ADAPTIVE_SYNC_SDP_TRANSMISSION_TIMING_CONFIG)


##
# @brief       Exposed Structure for Sink Psr Configuration Fields
#              PSR_CONFIGURATION = 0x170
class SinkPsrConfigurationFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("psr_enable_in_sink", ctypes.c_ubyte, 1),  # 0
        ("source_state", ctypes.c_ubyte, 1),  # 1
        ("crc_verify", ctypes.c_ubyte, 1),  # 2
        ("frame_capture_indication", ctypes.c_ubyte, 1),  # 3
        ("su_region_scan_line_capture", ctypes.c_ubyte, 1),  # 4
        ("irq_hpd_with_link_crc_errors", ctypes.c_ubyte, 1),  # 5
        ("enable_psr1_psr2_protocol", ctypes.c_ubyte, 2),  # 6
        ("su_region_early_transport_enable", ctypes.c_ubyte, 2),  # 7
    ]


##
# @brief       Exposed Union for Sink Psr Configuration Fields
class SinkPsrConfiguration(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SinkPsrConfigurationFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for SinkPsrConfiguration Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(SinkPsrConfiguration, self).__init__()
        self.value = get(target_id, Offsets.PSR_CONFIGURATION)


display_config_ = display_config.DisplayConfiguration()
__dpcd_cache = {}  # {target_id: {offset: value}}


##
# @brief        Exposed API to read DPCD offset from panel
# @param[in]    target_id id of the attached panel for DPCD read
# @param[in]    dpcd_offset offset at which the value has to be fetched
# @param[in]    size [optional], number of bytes to be read
# @return       DPCD value if successful, None otherwise
#               if size is greater than 1, output will be a list of bytes
def read(target_id, dpcd_offset, size=1):
    global __dpcd_cache

    # Validate parameters
    if target_id < 1 or size < 1 or size > driver_escape_args.DPCD_BUFFER_SIZE or dpcd_offset < 0:
        logging.error("\tInvalid arguments: target_id= {0}, dpcd_offset= {1}, size= {2}".format(
            target_id, dpcd_offset, size))
        return None

    # Make sure target panel is active before reading DPCD
    enumerated_displays = display_config_.get_enumerated_display_info()
    if enumerated_displays is None:
        logging.error("\tAPI get_enumerated_display_info() FAILED (Test Issue)")
        return None

    display_active_status = False
    for display_index in range(enumerated_displays.Count):
        if enumerated_displays.ConnectedDisplays[display_index].TargetID == target_id \
                and enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
            display_active_status = True
            break

    if display_active_status is False:
        logging.error("\tDisplay {0} is not active".format(target_id))
        return None

    # Read DPCD
    poll_count = 0
    dpcd_value = None
    while poll_count < __MAX_POLL_COUNT:
        dpcd_flag, dpcd_value = driver_escape.read_dpcd(target_id, dpcd_offset)
        if dpcd_flag:
            break
        poll_count += 1

    if poll_count == __MAX_POLL_COUNT:
        logging.error("\tDPCD read failed for target id= {0} (Poll Count= {1})".format(target_id, poll_count))
        return None

    # Warn if poll count is greater than 1
    if poll_count != 0:
        logging.warning("\tDPCD read passed for target id= {0} (Poll Count= {1})".format(target_id, poll_count))

    # Store the value in cache
    if target_id not in __dpcd_cache.keys():
        __dpcd_cache.update({target_id: {dpcd_offset: dpcd_value[:size]}})
    else:
        __dpcd_cache[target_id].update({dpcd_offset: dpcd_value[:size]})

    if size == 1:
        logging.debug("DPCD Read: Offset={0}, Size=1 byte, Data= {1}".format(hex(dpcd_offset), hex(dpcd_value[0])))
        return dpcd_value[0]
    logging.debug("DPCD Read: Offset={0}, Size={1} bytes, Data= {2}".format(
        hex(dpcd_offset), size, ' '.join([str(hex(v)) for v in dpcd_value[:size]])))
    return dpcd_value[:size]


##
# @brief        Exposed API to get DPCD offset value from cache. If value is not present in cache, it will be read from
#               DPCD
# @param[in]    target_id id of the panel
# @param[in]    dpcd_offset_type of type Offsets enum for which the value has to be fetched
# @param[in]    size [optional] number of bytes to be read
# @return       DPCD value if successful, None otherwise
#               if size is greater than 1, output will be a list of bytes
def get(target_id, dpcd_offset_type: Offsets, size=1):
    dpcd_offset = dpcd_offset_type.value
    # Validate parameters
    if target_id < 1 or size < 1 or size > driver_escape_args.DPCD_BUFFER_SIZE or dpcd_offset < 0:
        logging.error("\tInvalid arguments: target_id= {0}, dpcd_offset= {1}, size= {2}".format(
            target_id, dpcd_offset, size))
        return None

    # Search the offset in cache, if present return from there
    if target_id in __dpcd_cache.keys() and dpcd_offset in __dpcd_cache[target_id].keys():
        if size == 1:
            if not type(__dpcd_cache[target_id][dpcd_offset]) is list:
                return __dpcd_cache[target_id][dpcd_offset]
        else:
            if type(__dpcd_cache[target_id][dpcd_offset]) is list and len(__dpcd_cache[target_id][dpcd_offset]) == size:
                return __dpcd_cache[target_id][dpcd_offset]

    # If not found in cache, read from DPCD
    return read(target_id, dpcd_offset, size)


##
# @brief        Exposed API to get eDP DPCD Revision.
# @param[in]    target_id
# @return       Returns eDP DPCD revision of type EdpDpcdRevision
def get_edp_revision(target_id) -> EdpDpcdRevision:
    dpcd_value = get(target_id, Offsets.DPCD_VER)
    if dpcd_value is None or dpcd_value >= EdpDpcdRevision.EDP_DPCD_MAX:
        logging.debug("EDP(TargetId= {0}) DPCD Revision= UNKNOWN".format(target_id))
        return EdpDpcdRevision.EDP_UNKNOWN
    logging.debug("EDP(TargetId= {0}) DPCD Revision= {1}".format(target_id, EdpDpcdRevision(dpcd_value).name))
    return EdpDpcdRevision(dpcd_value)


##
# @brief        Exposed API to get eDP PSR version
# @param[in]    target_id
# @return       Returns eDP PSR version of type EdpPsrVersion
def get_psr_version(target_id) -> EdpPsrVersion:
    dpcd_value = get(target_id, Offsets.PSR_CAPS_SUPPORTED_AND_VERSION)
    if dpcd_value is None or dpcd_value >= EdpPsrVersion.EDP_PSR_MAX:
        logging.debug("EDP(TargetId= {0}) PSR Version= UNKNOWN".format(target_id))
        return EdpPsrVersion.EDP_PSR_UNKNOWN

    logging.debug("EDP(TargetId= {0}) PSR Version= {1}".format(target_id, EdpPsrVersion(dpcd_value).name))
    return EdpPsrVersion(dpcd_value)


##
# @brief        Exposed API to get AUX Frame Sync Support
# @param[in]    target_id
# @return       Return Aux frame sync support if successful, None otherwise
def get_aux_frame_sync_support(target_id):
    dpcd_value = get(target_id, Offsets.AUX_FRAME_SYNC_SUPPORT)
    if dpcd_value is None:
        return None
    if dpcd_value & 0x01 == 0x01:
        logging.debug("EDP(TargetId= {0}) Aux Frame Sync Support= {1}".format(target_id, True))
        return True
    logging.debug("EDP(TargetId= {0}) Aux Frame Sync Support= {1}".format(target_id, False))
    return False


##
# @brief        Exposed API to get Link Rate
# @param[in]    target_id target id of the panel
# @param[in]    is_edp_panel boolean indicating if the panel is an edp
# @return       link_rate, Double
def get_link_rate(target_id, is_edp_panel):
    link_bw_set = read(target_id, Offsets.LINK_BW_SET)
    link_bw_set *= 0.27

    if is_edp_panel:
        dpcd_rev = get_edp_revision(target_id)
    else:
        dpcd_rev = get(target_id, Offsets.DPCD_REV)

    # intermediate link rate is supported only for DPCD rev 1.3 and edp DPCD rev >= 1.4
    if dpcd_rev == DpcdRevision.DPCD_1_3 or (is_edp_panel and dpcd_rev > EdpDpcdRevision.EDP_DPCD_1_3):
        max_link_rate = get(target_id, Offsets.MAX_LINK_RATE)
        max_link_rate *= 0.27

        dpcd_inter_address = dict([(0x00010, 0x00011),
                                   (0x00012, 0x00013),
                                   (0x00014, 0x00015),
                                   (0x00016, 0x00017),
                                   (0x00018, 0x00019),
                                   (0x0001A, 0x0001B),
                                   (0x0001C, 0x0001D),
                                   (0x0001E, 0x0001F)])
        link_rate_set = read(target_id, Offsets.LINK_RATE_SET)
        intermediate_link_rate_lsb = list(dpcd_inter_address)[link_rate_set:link_rate_set + 1][0]
        intermediate_link_rate_usb = list(dpcd_inter_address.values())[link_rate_set:link_rate_set + 1][0]
        reg_value = read(target_id, intermediate_link_rate_lsb)
        ilr_lsb = str(hex(reg_value).lstrip("0x").rstrip("L"))
        reg_value = read(target_id, intermediate_link_rate_usb)
        ilr_usb = str(hex(reg_value).lstrip("0x").rstrip("L"))
        ilr_s = ilr_usb + ilr_lsb
        if ilr_s != '':
            return int(ilr_s, 16) * 200 / 1000000.0

    return link_bw_set


##
# @brief        Exposed API to get whether the display is MST or not
# @param[in]    target_id
# @return       Return True for MST, False for SST if successful, None otherwise
def is_mst_mode(target_id):
    mstm_cap_value = get(target_id, Offsets.MSTM_CAP)
    mstm_ctrl_value = read(target_id, Offsets.MSTM_CTRL)
    # If either of the dpcd read failed, then return None
    if mstm_cap_value is None or mstm_ctrl_value is None:
        return None
    status = ((mstm_cap_value & 0x01 == 0x01) and (mstm_ctrl_value & 0x01 == 0x01))
    logging.debug("DP(TargetId= {0}) MST MODE= {1}".format(target_id, status))
    return status


##
# PANEL_SELF_REFRESH_CAPABILITIES 0x00071
# BIT 5 - Psr2_su_granularity is newly added in EDP 1.4b
class PsrCapabilityFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("link_training_required_on_psr_exit", ctypes.c_uint8, 1),  # Bit 0
        ("psr_setup_time", ctypes.c_uint8, 3),  # Bit 1 to 3
        ("Y_coordinate_required_for_psr2_su", ctypes.c_uint8, 1),  # Bit 4
        ("psr2_su_granularity_required", ctypes.c_uint8, 1),  # Bit 5
        ("reserved_6", ctypes.c_uint8, 2),  # Bit 6 to 7
    ]


##
# @brief       Exposed Union for Psr Capabilities Fields
class PsrCapability(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PsrCapabilityFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for PsrCapability Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(PsrCapability, self).__init__()
        self.value = get(target_id, Offsets.PANEL_SELF_REFRESH_CAPABILITIES)


##
# @brief        Exposed Structure for PSR2_Y_GRANULARITY_CAPABILITY 0x00074
#               Newly added in EDP 1.4b
class PsrGranularityFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("su_y_granularity", ctypes.c_uint8, 8)  # Bit 0:7
    ]


##
# @brief       Exposed Union for Psr Granularity Fields
class PsrGranularity(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PsrGranularityFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for PsrGranularity Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(PsrGranularity, self).__init__()
        self.value = get(target_id, Offsets.PSR2_Y_GRANULARITY_CAPABILITY)


##
# @brief        Exposed Structure for EDP_HDR_GET_SET_CTRL_PARAMS 0x00344
class HdrCtlParamsFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("enable_2084_decode", ctypes.c_uint8, 1),  # Bit 0
        ("enable_2020_gamut", ctypes.c_uint8, 1),  # Bit 1
        ("enable_tcon_tone_mapping", ctypes.c_uint8, 1),  # Bit 2
        ("enable_segmented_bkl", ctypes.c_uint8, 1),  # Bit 3
        ("enable_aux_brightness_control", ctypes.c_uint8, 1),  # Bit 4
        ("enable_srgb_to_panel_gamut_conversion", ctypes.c_uint8, 1),  # Bit 5
        ("reserved_6", ctypes.c_uint8, 1),  # Bit 6
        ("enable_sdp_override_aux", ctypes.c_uint8, 1),  # Bit 7
    ]


##
# @brief       Exposed Union for HDR get_set ctl param Fields
class HdrCtlParams(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HdrCtlParamsFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for HDR ctl params Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(HdrCtlParams, self).__init__()
        self.value = get(target_id, Offsets.EDP_HDR_GET_SET_CTRL_PARAMS)


##
# @brief        Exposed Structure for DP_RX_FEATURE_ENUMERATION_LIST 0x02210
class RxFeatureListFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("gtc_cap", ctypes.c_uint8, 1),  # Bit 0
        ("sst_split_sdp_cap", ctypes.c_uint8, 1),  # Bit 1
        ("av_sync_cap", ctypes.c_uint8, 1),  # Bit 2
        ("vsc_sdp_extension_for_colorimetry_supported", ctypes.c_uint8, 1),  # Bit 3
        ("vsc_ext_vesa_sdp_supported", ctypes.c_uint8, 1),  # Bit 4
        ("vsc_ext_vesa_sdp_chaining_supported", ctypes.c_uint8, 1),  # Bit 5
        ("vsc_ext_cea_sdp_supported", ctypes.c_uint8, 1),  # Bit 6
        ("vsc_ext_cea_sdp_chaining_supported", ctypes.c_uint8, 1),  # Bit 7
    ]


##
# @brief       Exposed Union for DP_RX_FEATURE_ENUMERATION_LIST Fields
class RxFeatureList(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", RxFeatureListFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for RX Feature List Union
    # @param[in]   target_id target id of the panel
    def __init__(self, target_id):
        super(RxFeatureList, self).__init__()
        self.value = get(target_id, Offsets.DP_RX_FEATURE_ENUMERATION_LIST)


##
# @brief       Exposed Structure for Panel Replay Caps Supported Fields
#              PANEL_REPLAY_CAPS_SUPPORTED_AND_VERSION 0x000B0
class PanelReplayCapsSupportedFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("panel_replay_support", ctypes.c_uint8, 1),  # Bit 0
        ("selective_update_support", ctypes.c_uint8, 1),  # Bit 1
        ("early_transport_support", ctypes.c_uint8, 1),  # Bit 2 for EDP only , reserved for DP
        ("reserved", ctypes.c_uint8, 5)  # Bit 3:7
    ]


##
# @brief       Exposed Union for Panel Replay Caps Supported Fields
class PanelReplayCapsSupported(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PanelReplayCapsSupportedFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       init method of of PanelReplayCapsSupported
    # @param[in]   target_id panel target_id
    def __init__(self, target_id=None):
        super(PanelReplayCapsSupported, self).__init__()
        self.offset = Offsets.PANEL_REPLAY_CAPABILITY_SUPPORTED
        self.value = 0
        if target_id:
            self.value = get(target_id, Offsets.PANEL_REPLAY_CAPABILITY_SUPPORTED)


##
# @brief       Exposed Structure for Sink Panel Replay Enable and Configuration Fields
#              PANEL_REPLAY_ENABLE_AND_CONFIGURATION = 0x1B0
class SinkPanelReplayEnableAndConfigurationFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("panel_replay_enable_in_sink", ctypes.c_uint8, 1),  # Bit 0
        ("vsc_sdp_with_panel_replay_crc_en", ctypes.c_uint8, 1),  # Bit 1
        ("irq_hpd_with_adaptive_sync_sdp_missing", ctypes.c_uint8, 1),  # Bit 2 for EDP only, reserved for DP
        ("irq_hpd_with_vsc_sdp_for_pr_unrecoverable_errors", ctypes.c_uint8, 1),  # Bit 3
        ("irq_hpd_with_rfb_storage_errors", ctypes.c_uint8, 1),  # Bit 4
        ("irq_hpd_with_active_frame_crc_errors", ctypes.c_uint8, 1),  # Bit 5
        ("selective_update_enable", ctypes.c_uint8, 1),  # Bit 6
        ("su_region_early_transport_enable", ctypes.c_uint8, 1)  # Bit 7 for EDP only, reserved for DP
    ]


##
# @brief       Exposed Union for Sink PanelReplay Enable And Configuration Fields
class SinkPanelReplayEnableAndConfiguration(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SinkPanelReplayEnableAndConfigurationFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       init method of of SinkPanelReplayEnableAndConfiguration
    # @param[in]   target_id panel target_id
    def __init__(self, target_id=None):
        super(SinkPanelReplayEnableAndConfiguration, self).__init__()
        self.offset = Offsets.PANEL_REPLAY_ENABLE_AND_CONFIGURATION
        self.value = 0
        if target_id is not None:
            self.value = get(target_id, Offsets.PANEL_REPLAY_ENABLE_AND_CONFIGURATION)


##
# @brief       Exposed Structure for Sink ALPM caps Fields for EDP 1.5 rev
#              ALPM = 0x2E
class AlpmCapsFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("aux_wake_alpm_cap", ctypes.c_uint8, 1),  # Bit 0
        ("pm_state_2a_support", ctypes.c_uint8, 1),  # Bit 1
        ("aux_less_alpm_cap", ctypes.c_uint8, 1),  # Bit 2
        ("reserved", ctypes.c_uint8, 5)  # Bit 3:7
    ]


##
# @brief       Exposed Union for Sink ALPM caps Fields
class AlpmCaps(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", AlpmCapsFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       init method of of Sink ALPM caps
    # @param[in]   target_id panel target_id
    def __init__(self, target_id=None):
        super(AlpmCaps, self).__init__()
        self.offset = Offsets.ALPM_CAP
        if target_id:
            self.value = get(target_id, Offsets.ALPM_CAP)
        else:
            self.value = 0


##
# @brief       Exposed Structure for panel replay error status fields
#              PANEL_REPLAY_ERROR_STATUS = 0x2020
class PanelReplayErrorStatusFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("active_frame_crc_error", ctypes.c_uint8, 1),  # Bit 0
        ("rfb_storage_error", ctypes.c_uint8, 1),  # Bit 1
        ("vsc_sdp_for_pr_uncorrectable_error", ctypes.c_uint8, 1),  # Bit 2
        ("adaptive_sync_sdp_missing_and_not_disabled", ctypes.c_uint8, 1),  # Bit 3 EDP specific, reserved for DP
        ("reserved", ctypes.c_uint8, 4)  # Bit 4:7
    ]


##
# @brief       Exposed Union for Sink ALPM caps Fields
class PanelReplayErrorStatus(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PanelReplayErrorStatusFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       init method of of Sink PR error status
    # @param[in]   target_id panel target_id
    def __init__(self, target_id):
        super(PanelReplayErrorStatus, self).__init__()
        self.offset = Offsets.PANEL_REPLAY_ERROR_STATUS
        self.value = get(target_id, Offsets.PANEL_REPLAY_ERROR_STATUS)


##
# @brief       Exposed Structure for panel replay granularity fields
#              PR_Y_GRANULARITY_CAPABILITY = 0xB4
class PrGranularityFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("su_y_granularity", ctypes.c_uint8, 7)  # Bit 0:7
    ]


##
# @brief       Exposed Union for Sink PR Y-granularity Fields
class PrGranularity(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PrGranularityFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       init method of of Sink PR Granularity status
    # @param[in]   target_id panel target_id
    def __init__(self, target_id):
        super(PrGranularity, self).__init__()
        self.offset = Offsets.PR_Y_GRANULARITY_CAPABILITY
        self.value = get(target_id, Offsets.PR_Y_GRANULARITY_CAPABILITY)


##
# @brief       Exposed Structure for panel replay capability fields
#              PANEL_REPLAY_CAPABILITY = 0xB1
class PanelReplayCapsFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved", ctypes.c_uint8, 5),  # Bit 0:4
        ("pr_su_granularity_needed", ctypes.c_uint8, 1),  # Bit 5
        ("su_y_granularity_extended_caps_supported", ctypes.c_uint8, 1),  # Bit 6 EDP specific , Reserved for DP
        ("reserved", ctypes.c_uint8, 1)  # Bit 7
    ]


##
# @brief       Exposed Union for Sink PR caps Fields
class PanelReplayCaps(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PanelReplayCapsFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       init method of of Sink PR caps
    # @param[in]   target_id panel target_id
    def __init__(self, target_id):
        super(PanelReplayCaps, self).__init__()
        self.offset = Offsets.PANEL_REPLAY_CAPABILITY
        self.value = get(target_id, Offsets.PANEL_REPLAY_CAPABILITY)


##
# @brief       Exposed Structure for Sink Panel Replay Enable and Configuration Fields
#              ALPM_CAP = 0x2E
class ALPMConfigurationFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved", ctypes.c_uint8, 2),  # Bit 0:1
        ("aux_less_alpm", ctypes.c_uint8, 1),  # Bit 2
        ("reserved", ctypes.c_uint8, 5)  # Bit 3:7
    ]


##
# @brief       Exposed Union for ALPM Caps Fields
class ALPMConfiguration(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", ALPMConfigurationFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       init method of of ALPMConfiguration
    # @param[in]   value default value to assign
    def __init__(self, value=None):
        super(ALPMConfiguration, self).__init__()
        self.offset = Offsets.ALPM_CAP
        if value is not None:
            self.value = value


##
# @brief       Exposed Structure for Edp Brightness Nits Fields
#              EDP_BRIGHTNESS_OPTIMIZATION = 0x354 to 0x357
class EdpBrightnessNitsFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("lsb_nits", ctypes.c_ubyte, 8),  # Bit 0:7
        ("msb_nits", ctypes.c_ubyte, 8),  # Bit 8:15
        ("frame_count", ctypes.c_ubyte, 8),  # Bit 16:23
        ("per_frame_steps", ctypes.c_ubyte, 8),  # Bit 24:31
    ]


##
# @brief       Exposed Union for Edp Brightness Nits
class EdpBrightnessNits(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", EdpBrightnessNitsFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for EdpBrightnessNits Union
    # @param[in]   target_id target id of the panel
    # @param[in]   dpcd_value to be used in the definition (Value in little endian uint8)
    def __init__(self, target_id, dpcd_value=None):
        super(EdpBrightnessNits, self).__init__()
        self.value = get(target_id, Offsets.EDP_BRIGHTNESS_NITS) if dpcd_value is None else dpcd_value


##
# @brief       Exposed Structure for EdpGeneralCapability2 Fields
#              EDP_GENERAL_CAPABILITY_2 = 0x703
class EdpGeneralCapability2Fields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("OverdriveEngineEnabled", ctypes.c_ubyte, 1),  # 0
        ("reserved", ctypes.c_ubyte, 3),  # Bit 1:3
        ("PanelLuminanceControlCapable", ctypes.c_ubyte, 1),  # 4
        ("VariableBrightnessControlCapable", ctypes.c_ubyte, 1),  # 5
        ("SmoothBrightnessCapable", ctypes.c_ubyte, 1),  # 6
        ("VariableBrightnessStrengthControlCapable", ctypes.c_ubyte, 1),  # 7
    ]


##
# @brief       Exposed Union for EdpGeneralCapability2
class EdpGeneralCapability2(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", EdpGeneralCapability2Fields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for EdpGeneralCapability2 Union
    # @param[in]   target_id target id of the panel
    # @param[in]   dpcd_value to be used in the definition (Value in little endian uint8)
    def __init__(self, target_id, dpcd_value=None):
        super(EdpGeneralCapability2, self).__init__()
        self.value = get(target_id, Offsets.EDP_GENERAL_CAPABILITY_2) if dpcd_value is None else dpcd_value


##
# @brief       Exposed Structure for EdpBacklightModeset Fields
#              EDP_BACKLIGHT_MODE_SET = 0x721
class EdpBacklightModesetFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved", ctypes.c_ubyte, 7),  # Bit 0:6
        ("PanelLuminanceControlEnable", ctypes.c_ubyte, 1),  # 7
    ]


##
# @brief       Exposed Union for EdpBacklightModeset
class EdpBacklightModeset(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", EdpBacklightModesetFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for EdpBacklightModeset Union
    # @param[in]   target_id target id of the panel
    # @param[in]   dpcd_value to be used in the definition (Value in little endian uint8)
    def __init__(self, target_id, dpcd_value=None):
        super(EdpBacklightModeset, self).__init__()
        self.value = get(target_id, Offsets.EDP_BACKLIGHT_MODE_SET) if dpcd_value is None else dpcd_value


##
# @brief       Exposed Structure for EdpDisplayControl2 Fields
#              EDP_DISPLAY_CONTROL_2 = 0x730
class EdpDisplayControl2Fields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("SmoothBrightnessEnable", ctypes.c_ubyte, 1),  # 0
        ("VariableBrightnessStrength", ctypes.c_ubyte, 2),  # Bit 1:2
        ("reserved", ctypes.c_ubyte, 5),  # Bit 3:7
    ]


##
# @brief       Exposed Union for EdpDisplayControl2
class EdpDisplayControl2(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", EdpDisplayControl2Fields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for EdpDisplayControl2 Union
    # @param[in]   target_id target id of the panel
    # @param[in]   dpcd_value to be used in the definition (Value in little endian uint8)
    def __init__(self, target_id, dpcd_value=None):
        super(EdpDisplayControl2, self).__init__()
        self.value = get(target_id, Offsets.EDP_DISPLAY_CONTROL_2) if dpcd_value is None else dpcd_value


##
# @brief       Exposed Structure for PanelTargetLuminanaceValue Fields
#              PANEL_TARGET_LUMINANCE_VALUE = 0x734 to 0x736
class PanelTargetLuminanaceValueFields(ctypes.LittleEndianStructure):
    _fields_ = [
        ("Paneltargetluminancevalue7To0", ctypes.c_ubyte, 8),  # Bit 0:7
        ("Paneltargetluminancevalue15To8", ctypes.c_ubyte, 8),  # Bit 8:15
        ("Paneltargetluminancevalue23To16", ctypes.c_ubyte, 8),  # Bit 16:23
    ]


##
# @brief       Exposed Union for PanelTargetLuminanaceValue
class PanelTargetLuminanaceValue(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PanelTargetLuminanaceValueFields),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief       Initializer to get the register values for PanelTargetLuminanaceValue Union
    # @param[in]   target_id target id of the panel
    # @param[in]   dpcd_value to be used in the definition (Value in little endian uint8)
    def __init__(self, target_id, dpcd_value=None):
        super(PanelTargetLuminanaceValue, self).__init__()
        self.value = get(target_id, Offsets.PANEL_TARGET_LUMINANCE_VALUE) if dpcd_value is None else dpcd_value

