########################################################################################################################
# @file     dispdiag_verification_args.py
# @brief    Contains Display Diagnostics Enum and Structure details
# @details  Structures and Enum details required for Display Diagnostics Verification.
#           Structures:
#               DxgkDisplayStateIntrusive
#               DxgkDisplayStateNonIntrusive
#           Enums for display states:
#               Intrusive States - DxgkDiagMonitorState, DxgkDiagDisplayScanoutState, DxgkDiagDisplayScanoutBufferCrc
#                                  DxgkDiagDisplayHardwareErrorState, DxgkDiagDisplayHardwareBandwidth
#               Nonintrusive States - DxgkDiagDisplayConnectivity, DxgkDiagDisplayLidState, DxgkDiagDisplayLinkState,
#                                     DxgkDiagBasicDisplayTopology, DxgkDiagDisplayModeSet,
#                                     DxgkDiagGetDisplayStateSubstatusFlags
# @author   Prateek Joshi
########################################################################################################################
import ctypes
from enum import Enum

MAX_DISPLAY_FOR_DIAGNOSTICS = 16
MAX_NUM_OF_GAMMA_SAMPLES_FOR_DIAGNOSTICS = 16


##
# @brief        DisplayDiagType Enum
class DisplayDiagType(Enum):
    NONE = 0
    NONINTRUSIVE = 1
    INTRUSIVE = 2


##
# @brief        DxgkDiagMonitorState Enum
class DxgkDiagMonitorState(Enum):
    DXGK_DIAG_MONITOR_STATE_UNINITIALIZED = 0
    DXGK_DIAG_MONITOR_READY = 1
    DXGK_DIAG_MONITOR_NOT_READY = 2
    DXGK_DIAG_MONITOR_READY_NOTAPPLICABLE = 3


##
# @brief        DxgkDiagDisplayScanoutState Enum
class DxgkDiagDisplayScanoutState(Enum):
    DXGK_DIAG_DISPLAY_SCANOUT_STATE_UNINITIALIZED = 0
    DXGK_DIAG_DISPLAY_SCANOUT_DISABLED = 1
    DXGK_DIAG_DISPLAY_SCANOUT_ACTIVE = 2
    DXGK_DIAG_DISPLAY_SCANOUT_ACTIVE_BLACK = 3


##
# @brief        DxgkDiagDisplayScanoutBufferCrc Enum
class DxgkDiagDisplayScanoutBufferCrc(Enum):
    DXGK_DIAG_DISPLAY_SCANOUT_BUFFER_CRC_UNINITIALIZED = 0
    DXGK_DIAG_DISPLAY_SCANOUT_BUFFER_CRC_BLACK = 1
    DXGK_DIAG_DISPLAY_SCANOUT_BUFFER_CRC_NON_BLACK = 2
    DXGK_DIAG_DISPLAY_SCANOUT_BUFFER_CRC_ERROR = 3
    DXGK_DIAG_DISPLAY_SCANOUT_BUFFER_CRC_UNKNOWN = 4


##
# @brief        DxgkDiagDisplayHardwareErrorState Enum
class DxgkDiagDisplayHardwareErrorState(Enum):
    DXGK_DIAG_DISPLAY_HARDWARE_ERROR_STATE_UNINITIALIZED = 0
    DXGK_DIAG_DISPLAY_HARDWARE_ERROR_NONE = 1
    DXGK_DIAG_DISPLAY_HARDWARE_ERROR_SCANOUT_UNDERFLOW = 2
    DXGK_DIAG_DISPLAY_HARDWARE_ERROR_TDRNORECOVERY = 3
    DXGK_DIAG_DISPLAY_HARDWARE_ERROR_UNSPECIFIED = 4


##
# @brief        DxgkDiagDisplayHardwareBandwidth Enum
class DxgkDiagDisplayHardwareBandwidth(Enum):
    DXGK_DIAG_DISPLAY_HARDWARE_BANDWIDTH_UNINITIALIZED = 0
    DXGK_DIAG_DISPLAY_HARDWARE_BANDWIDTH_SUFFICIENT = 1
    DXGK_DIAG_DISPLAY_HARDWARE_LINK_BANDWIDTH_LIMITED = 2
    DXGK_DIAG_DISPLAY_HARDWARE_SOC_BANDWIDTH_LIMITED = 3
    DXGK_DIAG_DISPLAY_HARDWARE_BANDWIDTH_ERROR = 4
    DXGK_DIAG_DISPLAY_HARDWARE_BANDWIDTH_UNKNOWN = 5


##
# @brief        DxgkDiagDisplayConnectivity Enum
class DxgkDiagDisplayConnectivity(Enum):
    DXGK_DIAG_DISPLAY_CONNECTIVITY_UNINITIALIZED = 0
    DXGK_DIAG_DISPLAY_NOT_CONNECTED = 1
    DXGK_DIAG_DISPLAY_CONNECTED = 2


##
# @brief        DxgkDiagDisplayLidState Enum
class DxgkDiagDisplayLidState(Enum):
    DXGK_DIAG_DISPLAY_LID_STATE_UNINITIALIZED = 0
    DXGK_DIAG_DISPLAY_LID_STATE_NOTAPPLICABLE = 1
    DXGK_DIAG_DISPLAY_LID_STATE_OPEN = 2
    DXGK_DIAG_DISPLAY_LID_STATE_CLOSE = 3
    DXGK_DIAG_DISPLAY_LID_STATE_UNKNOWN = 4


##
# @brief        DxgkDiagBasicDisplayTopology Enum
class DxgkDiagBasicDisplayTopology(Enum):
    DXGK_DIAG_BASIC_DISPLAY_TOPOLOGY_UNINITIALIZED = 0
    DXGK_DIAG_DISPLAY_CONNECTED_DIRECTLY = 1
    DXGK_DIAG_DISPLAY_CONNECTED_INDIRECTLY_CONVERTOR = 2
    DXGK_DIAG_DISPLAY_CONNECTED_INDIRECTLY_HUB = 3
    DXGK_DIAG_DISPLAY_CONNECTED_INDIRECTLY = 4
    DXGK_DIAG_DISPLAY_CONNECTED_UNKNOWN = 5


##
# @brief        DxgkDiagDisplayLinkState Enum
class DxgkDiagDisplayLinkState(Enum):
    DXGK_DIAG_DISPLAY_LINK_STATE_UNINITIALIZED = 0
    DXGK_DIAG_DISPLAY_LINK_STATE_NOTAPPLICABLE = 1
    DXGK_DIAG_DISPLAY_LINK_STATE_STABLE = 2
    DXGK_DIAG_DISPLAY_LINK_STATE_FAILED = 3
    DXGK_DIAG_DISPLAY_LINK_STATE_CONTINUOUS_TRAINING = 4
    DXGK_DIAG_DISPLAY_LINK_STATE_CONTINUOUS_TRAINING_STABLE = 5
    DXGK_DIAG_DISPLAY_LINK_STATE_CONTINUOUS_TRAINING_FAILED = 6


##
# @brief        DxgkDiagDisplayModeSet Enum
class DxgkDiagDisplayModeSet(Enum):
    DXGK_DIAG_DISPLAY_MODE_SET_UNINITIALIZED = 0
    DXGK_DIAG_DISPLAY_MODE_SET_NO = 1
    DXGK_DIAG_DISPLAY_MODE_SET_YES = 2


##
# @brief        DxgkDiagGetDisplayStateSubstatusFlags Enum
class DxgkDiagGetDisplayStateSubstatusFlags(Enum):
    DXGK_DIAG_GETDISPLAYSTATE_SUCCESS = 0
    DXGK_DIAG_GETDISPLAYSTATE_CAUSED_GLITCH = 1
    DXGK_DIAG_GETDISPLAYSTATE_CHANGED_DISPLAY_STATE = 2
    DXGK_DIAG_GETDISPLAYSTATE_MONITOR_NOT_CONNECTED = 4
    DXGK_DIAG_GETDISPLAYSTATE_TIMEOUT = 8
    DXGK_DIAG_GETDISPLAYSTATE_ERROR_HARDWARE = 16
    DXGK_DIAG_GETDISPLAYSTATE_ERROR_DRIVER = 32
    DXGK_DIAG_GETDISPLAYSTATE_VIDPNTARGETID_NOT_FOUND = 64


##
# @brief        DxgkDisplayStateIntrusive Structure
class DxgkDisplayStateIntrusive(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('VidPnTargetId', ctypes.c_int),
        ('MonitorState', ctypes.c_ulong),
        ('DisplayScanoutState', ctypes.c_ulong),
        ('DisplaySampledGamma', ctypes.c_ulong),
        ('DisplayBufferContent', ctypes.c_ulong),
        ('DisplayErrorState', ctypes.c_ulong),
        ('DisplayBandwidth', ctypes.c_ulong),
        ('ReturnSubStatus', ctypes.c_ulong),
    ]


##
# @brief        DisplayStateIntrusive Structure
class DisplayStateIntrusive(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('NumOfTargets', ctypes.c_int),
        ('IntrusiveData', DxgkDisplayStateIntrusive * MAX_DISPLAY_FOR_DIAGNOSTICS),
    ]


##
# @brief        DxgkDisplayStateNonIntrusive Structure
class DxgkDisplayStateNonIntrusive(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('VidPnTargetId', ctypes.c_int),
        ('DisplayConnectivity', ctypes.c_ulong),
        ('DisplayLidState', ctypes.c_ulong),
        ('DisplayTopology', ctypes.c_ulong),
        ('DisplayLinkState', ctypes.c_ulong),
        ('DisplayModeSet', ctypes.c_ulong),
        ('ReturnSubStatus', ctypes.c_ulong),
    ]


##
# @brief        DisplayStateNonIntrusive Structure
class DisplayStateNonIntrusive(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('NumOfTargets', ctypes.c_int),
        ('NonIntrusiveData', DxgkDisplayStateNonIntrusive * MAX_DISPLAY_FOR_DIAGNOSTICS),
    ]


##
# @brief        DxgkDiagDisplayScanoutBufferHistogram Structure
class DxgkDiagDisplayScanoutBufferHistogram(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('MinPixelValue', ctypes.c_ulong),
        ('MaxPixelValue', ctypes.c_ulong),
    ]


##
# @brief        DxgkDiagDisplayScanoutBufferContent Structure
class DxgkDiagDisplayScanoutBufferContent(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('ScanoutBufferCrc', ctypes.c_ulong),
        ('ScanoutBufferHistogram', ctypes.c_ulong),
    ]


##
# @brief        DxgkDiagDisplaySampledGamma Structure
class DxgkDiagDisplaySampledGamma(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Red', ctypes.c_float * MAX_NUM_OF_GAMMA_SAMPLES_FOR_DIAGNOSTICS),
        ('Green', ctypes.c_float * MAX_NUM_OF_GAMMA_SAMPLES_FOR_DIAGNOSTICS),
        ('Blue', ctypes.c_float * MAX_NUM_OF_GAMMA_SAMPLES_FOR_DIAGNOSTICS),
        ('ColorMatrix', ctypes.c_float * 3 * 3),  # Color Matrix [3][3]
    ]
