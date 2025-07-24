########################################################################################################################
# @file         display_config_enums.py
# @brief        Enums for Python Wrapper exposes interfaces for Display Config
# @author       Amit Sau, Chandrakanth Pabolu
########################################################################################################################
from Lib.enum import IntEnum, IntFlag  # @Todo: Override with Built-in python3 enum script path
from Libs.Core import enum


##
# @brief        Configuration topology for switching display configuration.
class DisplayConfigTopology(enum.Enum):
    _members_ = {
        'TOPOLOGY_NONE ': 0,
        'SINGLE': 1,
        'CLONE': 2,
        'EXTENDED': 3,
        'HYBRID': 4
    }


##
# @brief        Type of driver installed.
class DriverType(IntEnum):
    UNKNOWN = 0
    LEGACY  = 1
    YANGRA  = 2


##
# @brief        Display Configuration Error Code
class DisplayConfigErrorCode(enum.Enum):
    _members_ = {
        'DISPLAY_CONFIG_SUCCESS': 0,
        'DISPLAY_CONFIG_ERROR_INVALID_PARAMETER': 1,
        'DISPLAY_CONFIG_ERROR_NOT_SUPPORTED': 2,
        'DISPLAY_CONFIG_ERROR_ACCESS_DENIED': 3,
        'DISPLAY_CONFIG_ERROR_GEN_FAILURE': 4,
        'DISPLAY_CONFIG_ERROR_INSUFFICIENT_BUFFER': 5,
        'DISPLAY_CONFIG_ERROR_BAD_CONFIGURATION': 6,
        'DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED': 7,
        'DISPLAY_CONFIG_ERROR_SIZE_MISMATCH': 8,
        'DISPLAY_CONFIG_ERROR_TARGET_INACTIVE': 9,
        'DISPLAY_CONFIG_ERROR_INVALID_DEVICE_NAME': 10,
        'DISPLAY_CONFIG_ERROR_QUERY_MODE_FAILED': 11,
        'DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED': 12,
        'DISPLAY_CONFIG_ERROR_REGISTRY_ACCESS': 13,
        'DISPLAY_CONFIG_ERROR_MODE_VERIFICATION_FAILED': 14,
        'DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID': 15,
        'DISPLAY_CONFIG_ERROR_OS_API_CALL_FAILED': 16,
        'DISPLAY_CONFIG_ERROR_SUCCESS_RR_MISMATCH': 17,
        'DISPLAY_CONFIG_ERROR_VERIFICATION_FAILED': 18,
        'DISPLAY_CONFIG_ERROR_UNDEFINED': 255
    }


##
# @brief        Supported Display Rotation Angle.
class Rotation(enum.Enum):
    _members_ = {
        'ROTATE_UNSPECIFIED': 0,
        'ROTATE_0': 1,
        'ROTATE_90': 2,
        'ROTATE_180': 3,
        'ROTATE_270': 4
    }


##
# @brief        Supported Display Scanline Ordering Progressive or Interlaced.
class ScanlineOrdering(enum.Enum):
    _members_ = {
        'SCANLINE_ORDERING_UNSPECIFIED': 0,
        'PROGRESSIVE': 1,
        'INTERLACED': 2
    }


##
# @brief        Supported Pixel Format (BPP).
class PixelFormat(enum.Enum):
    _members_ = {
        'PIXELFORMAT_UNSPECIFIED': 0,
        'PIXELFORMAT_8BPP': 1,
        'PIXELFORMAT_16BPP': 2,
        'PIXELFORMAT_24BPP': 3,
        'PIXELFORMAT_32BPP': 4,
        'PIXELFORMAT_NONGDI': 5
    }


##
# @brief        Supported Scaling.
class Scaling(enum.Enum):
    _members_ = {
        'SCALING_UNSPECIFIED': 0,
        'CI': 1,
        'FS': 2,
        'MAR': 4,
        'CAR': 8,
        'MDS': 64
    }


##
# @brief        Scalar Type class
class SCALAR_TYPE(enum.Enum):
    _members_ = {
        'DEFAULT': 0,
        'FORCEPLANE': 1,
        'FORCEPIPE': 2
    }


##
# @brief        Connector Port Types.
class CONNECTOR_PORT_TYPE(enum.Enum):
    _members_ = {
        'DispNone': 0,
        'DP_A': 1,
        'MIPI_A': 2,
        'MIPI_C': 3,
        'CRT': 4,
        'DP_B': 5,
        'DP_C': 6,
        'DP_D': 7,
        'DP_E': 8,
        'DP_F': 9,
        'DP_G': 10,
        'DP_H': 11,
        'DP_I': 12,
        'DP_TYPE_C_B': 13,
        'DP_TYPE_C_C': 14,
        'DP_TYPE_C_D': 15,
        'DP_TYPE_C_E': 16,
        'DP_TYPE_C_F': 17,
        'DP_TYPE_C_G': 18,
        'DP_TYPE_C_H': 19,
        'DP_TYPE_C_I': 20,
        'DP_TBT_B': 21,
        'DP_TBT_C': 22,
        'DP_TBT_D': 23,
        'DP_TBT_E': 24,
        'DP_TBT_F': 25,
        'DP_TBT_G': 26,
        'DP_TBT_H': 27,
        'DP_TBT_I': 28,
        'HDMI_B': 29,
        'HDMI_C': 30,
        'HDMI_D': 31,
        'HDMI_E': 32,
        'HDMI_F': 33,
        'HDMI_G': 34,
        'HDMI_H': 35,
        'HDMI_I': 36,
        'DVI_B': 37,
        'DVI_C': 38,
        'DVI_D': 39,
        'DVI_E': 40,
        'DVI_F': 41,
        'DVI_G': 42,
        'DVI_H': 43,
        'DVI_I': 44,
        'VIRTUALDISPLAY': 45,
        'WIDI': 46,
        'WD_0': 47,
        'WD_1': 48,
        'HDMI_A': 49,
        'COLLAGE_0': 50
    }


##
# @brief        HDR error codes
class HDRErrorCode(enum.Enum):
    _members_ = {
        'ERROR_SUCCESS            ': 0,
        'ERROR_ACCESS_DENIED      ': 5,
        'ERROR_INVALID_ADAPTER_ID': 15,
        'ERROR_GEN_FAILURE        ': 31,
        'ERROR_NOT_SUPPORTED      ': 50,
        'ERROR_INVALID_PARAMETER  ': 87,
        'ERROR_INSUFFICIENT_BUFFER': 122
    }


##
# @brief        RR modes in displayMode
class RRMODE(enum.Enum):
    _members_ = {
        'LEGACY_RR': 0,
        'DYNAMIC_RR': 1
    }


##
# @brief        MSFT defined Query Display Config flags
class QdcFlag(IntFlag):
    QDC_ALL_PATHS = 0x00000001
    QDC_ONLY_ACTIVE_PATHS = 0x00000002
    QDC_DATABASE_CURRENT = 0x00000004
    QDC_VIRTUAL_MODE_AWARE = 0x00000010
    QDC_INCLUDE_HMD = 0x00000020


##
# @brief        MSFT defined Set Display Config flags
class SdcFlag(IntFlag):
    SDC_TOPOLOGY_INTERNAL = 0x00000001
    SDC_TOPOLOGY_CLONE = 0x00000002
    SDC_TOPOLOGY_EXTEND = 0x00000004
    SDC_TOPOLOGY_EXTERNAL = 0x00000008
    SDC_TOPOLOGY_SUPPLIED = 0x00000010
    SDC_USE_DATABASE_CURRENT = (
            SDC_TOPOLOGY_INTERNAL | SDC_TOPOLOGY_CLONE | SDC_TOPOLOGY_EXTEND | SDC_TOPOLOGY_EXTERNAL)
    SDC_USE_SUPPLIED_DISPLAY_CONFIG = 0x00000020
    SDC_VALIDATE = 0x00000040
    SDC_APPLY = 0x00000080
    SDC_NO_OPTIMIZATION = 0x00000100
    SDC_SAVE_TO_DATABASE = 0x00000200
    SDC_ALLOW_CHANGES = 0x00000400
    SDC_PATH_PERSIST_IF_REQUIRED = 0x00000800
    SDC_FORCE_MODE_ENUMERATION = 0x00001000
    SDC_ALLOW_PATH_ORDER_CHANGES = 0x00002000
    SDC_VIRTUAL_MODE_AWARE = 0x00008000


##
# @brief        Topology ID from Display Config
class DisplayConfigTopologyId(IntEnum):
    DISPLAYCONFIG_TOPOLOGY_INTERNAL = 0x00000001
    DISPLAYCONFIG_TOPOLOGY_CLONE = 0x00000002
    DISPLAYCONFIG_TOPOLOGY_EXTEND = 0x00000004
    DISPLAYCONFIG_TOPOLOGY_EXTERNAL = 0x00000008
    DISPLAYCONFIG_TOPOLOGY_FORCE_UINT32 = 0xFFFFFFFF


##
# @brief        Video Output Technology Enum from Display Config
class DisplayConfigVideoOutputTechnology(IntEnum):
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_OTHER = -1
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HD15 = 0
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SVIDEO = 1
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_COMPOSITE_VIDEO = 2
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_COMPONENT_VIDEO = 3
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DVI = 4
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HDMI = 5
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_LVDS = 6
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_D_JPN = 8
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SDI = 9
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EXTERNAL = 10
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EMBEDDED = 11
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_UDI_EXTERNAL = 12
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_UDI_EMBEDDED = 13
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SDTVDONGLE = 14
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_MIRACAST = 15
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INDIRECT_WIRED = 16
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INDIRECT_VIRTUAL = 17
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_USB_TUNNEL = 18
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL = 0x80000000
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_FORCE_UINT32 = 0xFFFFFFFF


##
# @brief        Display Rotation Enum from Display Config
class DisplayConfigRotation(IntEnum):
    DISPLAYCONFIG_ROTATION_IDENTITY = 1
    DISPLAYCONFIG_ROTATION_ROTATE90 = 2
    DISPLAYCONFIG_ROTATION_ROTATE180 = 3
    DISPLAYCONFIG_ROTATION_ROTATE270 = 4
    DISPLAYCONFIG_ROTATION_FORCE_UINT32 = 0xFFFFFFFF


##
# @brief        Display Scaling Enum from Display Config
class DisplayConfigScaling(IntEnum):
    DISPLAYCONFIG_SCALING_IDENTITY = 1
    DISPLAYCONFIG_SCALING_CENTERED = 2
    DISPLAYCONFIG_SCALING_STRETCHED = 3
    DISPLAYCONFIG_SCALING_ASPECTRATIOCENTEREDMAX = 4
    DISPLAYCONFIG_SCALING_CUSTOM = 5
    DISPLAYCONFIG_SCALING_PREFERRED = 128
    DISPLAYCONFIG_SCALING_FORCE_UINT32 = 0xFFFFFFFF


##
# @brief        Scanline Ordering Enum from Display Config
class DisplayConfigScanlineOrdering(IntEnum):
    DISPLAYCONFIG_SCANLINE_ORDERING_UNSPECIFIED = 0
    DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE = 1
    DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED = 2
    DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_UPPERFIELDFIRST = 2
    DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_LOWERFIELDFIRST = 3
    DISPLAYCONFIG_SCANLINE_ORDERING_FORCE_UINT32 = 0xFFFFFFFF


##
# @brief        Mode Info Type Enum from Display Config
class DisplayConfigModeInfoType(IntEnum):
    DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE = 1
    DISPLAYCONFIG_MODE_INFO_TYPE_TARGET = 2
    DISPLAYCONFIG_MODE_INFO_TYPE_DESKTOP_IMAGE = 3
    DISPLAYCONFIG_MODE_INFO_TYPE_FORCE_UINT32 = 0xFFFFFFFF


##
# @brief        Pixel Format Enum from Display Config
class DisplayConfigPixelFormat(IntEnum):
    DISPLAYCONFIG_PIXELFORMAT_8BPP = 1
    DISPLAYCONFIG_PIXELFORMAT_16BPP = 2
    DISPLAYCONFIG_PIXELFORMAT_24BPP = 3
    DISPLAYCONFIG_PIXELFORMAT_32BPP = 4
    DISPLAYCONFIG_PIXELFORMAT_NONGDI = 5
    DISPLAYCONFIG_PIXELFORMAT_FORCE_UINT32 = 0xffffffff
