########################################################################################################################
# @file         display_config_struct.py
# @brief        Defines Structures for display_config.py
# @author       Amit Sau, Raghupathy
########################################################################################################################
from __future__ import annotations

import ctypes
import logging
from ctypes import wintypes
from typing import List

from Libs.Core.display_config import adapter_info_struct as adapter_struct
from Libs.Core.display_config import display_config_enums as cfg_enum

MAX_SUPPORTED_DISPLAYS = 16
DEVICE_NAME_SIZE = 64


##
# @brief        Target ID Structure
# @details      DDRW encodes Port type and Sink type in Target ID Structure in below fashion
class _TARGET_ID(ctypes.Structure):
    _fields_ = [
        ("PortType", ctypes.c_uint32, 4),  # 0 to 3
        ("SinkType", ctypes.c_uint32, 4),  # 4 to 7
        ("SinkIndex", ctypes.c_uint32, 4),  # 8 to 11
        ("UniqueIndex", ctypes.c_uint32, 5),  # 12 to 16
        ("Reserved", ctypes.c_uint32, 3),  # 17 to 19
        ("CollageDisplay", ctypes.c_uint32, 1),  # 20
        ("VirtualDisplay", ctypes.c_uint32, 1),  # 21
        ("TiledDisplay", ctypes.c_uint32, 1),  # 22
        ("InternalDisplay", ctypes.c_uint32, 1),  # 23
        ("ReservedForOS", ctypes.c_uint32, 8),  # 24 to 31
    ]


##
# @brief        Complete Target ID Union stored as value
class TARGET_ID(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _TARGET_ID),
        ("Value", ctypes.c_uint32)
    ]


##
# @brief        Structure Definition for Display Timings.
class DisplayTimings(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('targetId', ctypes.c_uint),  # [out] Windows Monitor ID ( Might have to Remove after sometime - TBD)
        ('hActive', ctypes.c_ulong),  # [out] Hactive value
        ('vActive', ctypes.c_ulong),  # [out] VActive value
        ('hSyncNumerator', ctypes.c_ulonglong),  # [out] Hsync numerator value
        ('hSyncDenominator', ctypes.c_ulonglong),  # [out] Hsync denominator value
        ('targetPixelRate', ctypes.c_ulonglong),  # [out] target pixel rate value
        ('hTotal', ctypes.c_ulong),  # [out] Htotal value
        ('vTotal', ctypes.c_ulong),  # [out] Vtotal value
        ('vSyncNumerator', ctypes.c_ulonglong),  # [out] Vsync numerator value
        ('vSyncDenominator', ctypes.c_ulonglong),  # [out] Vsync denominator value
        ('isPrefferedMode', ctypes.c_uint),  # [out] is Given Timing is from Preferred Mode
        ('status', ctypes.c_int),  # [out] Error Code of type DISPLAY_CONFIG_ERROR_CODE
        ('scanlineOrdering', ctypes.c_int),
        ('refreshRate', ctypes.c_int)
    ]

    ##
    # @brief         Overridden str method.
    # @return        string formatted DisplayTimings
    def __str__(self):
        return str(self.hActive) + 'x' + str(self.vActive) + '@' + str(self.refreshRate)

    ##
    # @brief        String representation of Display Timings
    # @return       mode_str - String representation DisplayTimings structure
    def to_string(self) -> str:
        mode_str = f"Target 0x{self.targetId:X} HActive {self.hActive} VActive {self.vActive} @RR {self.refreshRate}Hz "
        mode_str += f"PixelRate {self.targetPixelRate} Hz HTotal {self.hTotal} VTotal {self.vTotal} "
        mode_str += f"HSync Numerator {self.hSyncNumerator} Denominator {self.hSyncDenominator} "
        mode_str += f"VSync Numerator {self.vSyncNumerator} Denominator {self.vSyncDenominator} "
        mode_str += f"ScanlineOrdering {self.scanlineOrdering} IsPreferredMode {self.isPrefferedMode}"
        return mode_str

##
# @brief        Display and AdapterInfo Structure
# @details      Contains Target ID and Complete Adapter ID details
class DisplayAndAdapterInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('SourceID', ctypes.c_int),  # [Out] Source device ID
        ('TargetID', ctypes.c_uint32),  # Windows monitor ID
        ('adapterInfo', adapter_struct.GfxAdapterInfo),  # GFX Adapter Information
        ('Version', ctypes.c_uint),  # Version -> Legacy: 1, OS_Library_Rewrite:2
        ('DriverBranch', ctypes.c_int),  # V2 -> Legacy/Yangra/Unknown
        ('ConnectorNPortType', ctypes.c_int),  # V2 -> Connected Display Type (DP_A/HDMI_B/MIPI_C)
        ('ViewGdiDeviceName', ctypes.c_wchar * 32),  # V2 -> Display Device Name (Ex: \\.\DISPLAY1)
        ('MonitorFriendlyDeviceName', ctypes.c_wchar * 128),  # Display Name (eg Digital Display / Built-in Display)
        ('OsPreferredMode', DisplayTimings),  # V2 -> Os Preferred Mode
    ]

    ##
    # @brief         Overridden str method.
    # @return        string formatted DisplayAndAdapterInfo
    def __str__(self):
        return f"DisplayAndAdapterInfo - Source: {self.SourceID}, Target: {self.TargetID}, Version: {self.Version} " \
               f"DriverBranch: {self.DriverBranch}, " \
               f"ConnectorNPortType: {cfg_enum.CONNECTOR_PORT_TYPE(self.ConnectorNPortType).name}, " \
               f"{self.adapterInfo.to_string()}"


##
# @brief        Display Info Structure
# @details      Contains enumerated display Information
class DisplayInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('ConnectorNPortType', ctypes.c_int),  # Connected Display Type (DP_A/HDMI_B/MIPI_C)
        ('TargetID', ctypes.c_uint32),  # Windows monitor ID
        ('FriendlyDeviceName', ctypes.c_wchar * 128),  # Display Name (eg Digital Display / Built-in Display)
        ('IsActive', ctypes.c_bool),  # Display device is active or not
        ('PortType', ctypes.c_wchar * 128),  # Display is TC/TBT/Native
        ('DisplayAndAdapterInfo', DisplayAndAdapterInfo)  # Display Adapter ID Details
    ]


##
# @brief        Enumerated Displays Structure
class EnumeratedDisplays(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Size', ctypes.c_int),  # Size of ENUMERATED_DISPLAYS
        ('ConnectedDisplays', DisplayInfo * MAX_SUPPORTED_DISPLAYS),  # Connected Display List
        ('Count', ctypes.c_int)  # No of connected display (active and inactive)
    ]

##
# @brief        Structure Definition for Display Configuration
class MultiDisplayAndAdapterInfo(ctypes.Structure):
    _fields_ = [
        ('size', ctypes.c_int),  # [In] Size of DisplayConfig
        ('displayAndAdapterInfo', DisplayAndAdapterInfo * MAX_SUPPORTED_DISPLAYS),  # [Inout] DisplayAndAdapterInfo List
        ('Count', ctypes.c_int),  # Count of displays
        ('status', ctypes.c_int)  # [Out] Error Code
    ]

##
# @brief        Structure Definition for Sampling Mode Information.
class _SamplingMode(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('rgb', ctypes.c_ubyte, 1),
        ('yuv420', ctypes.c_ubyte, 1),
        ('yuv422', ctypes.c_ubyte, 1),
        ('yuv444', ctypes.c_ubyte, 1),
        ('reserved', ctypes.c_ubyte, 4)
    ]


##
# @brief        Union Definition for Sampling Mode Information.
class SamplingMode(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _SamplingMode),
        ("Value", ctypes.c_ubyte)
    ]


##
# @brief        Structure Definition for Display Mode (Resolution) Information.
class DisplayMode(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('targetId', ctypes.c_int),  # [Inout] Windows Monitor ID
        ('displayAndAdapterInfo', DisplayAndAdapterInfo),  # [Inout] Adapter Details
        ('HzRes', ctypes.c_int),  # [Inout] Horizontal Resolution
        ('VtRes', ctypes.c_int),  # [Inout] Vertical Resolution
        ('rotation', ctypes.c_int),  # [Inout] Display Rotation ( 0 Degree, 90 Degree, 180 Degree, 270 Degree)
        ('refreshRate', ctypes.c_int),  # [Inout] Refresh Rate
        ('BPP', ctypes.c_int),  # [Inout] Bit per pixel
        ('scanlineOrdering', ctypes.c_int),  # [Inout] Scan line Ordering (PROGRESSIVE or INTERLACED)
        ('scaling', ctypes.c_int),  # [Inout] Scaling for particular display mode
        ('samplingMode', SamplingMode),  # [Inout] Sampling Mode (1 - RGB, 2 - YUV420, 4 - YUV422, 8 - YUV444)
        ('pixelClock_Hz', ctypes.c_ulonglong),  # [Out] Pixel Clock (Hz)
        ('rrMode', ctypes.c_int),  # # [Out] RR Mode (0-Legacy 1-Dynamic)
        ('status', ctypes.c_int)  # [Out] Error Code of type DISPLAY_CONFIG_ERROR_CODE
    ]

    ##
    # @brief         Overridden eq method.
    # @param[in]     mode - display mode to be compared with self object
    # @return        is_equal - True or False, based on comparison values
    def __eq__(self, mode: DisplayMode) -> bool:
        is_equal: bool = False

        if isinstance(mode, DisplayMode) is True:
            # TODO: Sampling Mode Needs to be Included For Comparison. Since Mode Enumeration Doesn't have this Field
            #       Defined in the XML, Ignoring it for Now.
            if (self.status == cfg_enum.enum.DISPLAY_CONFIG_SUCCESS and self.status == mode.status
                    and self.targetId == mode.targetId and self.HzRes == mode.HzRes
                    and self.VtRes == mode.VtRes and self.rotation == mode.rotation
                    and self.refreshRate == mode.refreshRate
                    and self.BPP == mode.BPP
                    and self.scanlineOrdering == mode.scanlineOrdering and self.scaling == mode.scaling):
                is_equal = True
            elif (
                    self.status == cfg_enum.enum.DISPLAY_CONFIG_ERROR_SUCCESS_RR_MISMATCH
                    and cfg_enum.enum.DISPLAY_CONFIG_SUCCESS == mode.status
                    and self.targetId == mode.targetId and self.HzRes == mode.HzRes
                    and self.VtRes == mode.VtRes and self.rotation == mode.rotation
                    and self.BPP == mode.BPP
                    and self.scanlineOrdering == mode.scanlineOrdering and self.scaling == mode.scaling):
                logging.warning("Comparison Successful by Skipping RR. WA ( Fix - TBD from Driver)")
                is_equal = True

        return is_equal

    ##
    # @brief        Overriden hash method
    # @return       hash_value - Hash Value for current Sampling Mode
    def __hash__(self) -> int:
        # TODO: Sampling Mode Needs to be Included For Creating Hash Code. Since DSC Mode Enumeration Doesn't have this
        #       Field Defined in the XML, Ignoring it for Now.
        hash_value: int = hash((self.status, self.targetId, self.HzRes, self.VtRes, self.rotation, self.refreshRate,
                                self.BPP, self.scanlineOrdering, self.scaling))

        return hash_value

    ##
    # @brief         Overridden str method.
    # @return        string formatted Mode Resolution and Refresh rate
    def __str__(self):
        return "(" + str(self.HzRes) + "x" + str(self.VtRes) + "@" + str(self.refreshRate) + ")"

    ##
    # @brief        String representation of Display Mode
    # @param[in]    enumerated_displays - list of type EnumeratedDisplaysEx
    # @param[in]    full_details - print complete details otherwise pixelclock details not be present
    # @return       mode_str - String representation DisplayMode structure
    def to_string(self, enumerated_displays, full_details=True):
        mode_str = ""
        for eachDisplay in range(enumerated_displays.Count):
            if self.targetId == enumerated_displays.ConnectedDisplays[eachDisplay].TargetID:
                mode_str = (cfg_enum.CONNECTOR_PORT_TYPE(
                    enumerated_displays.ConnectedDisplays[eachDisplay].ConnectorNPortType)).name
                mode_str += ":" + " HzRes " + str(self.HzRes) + " VtRes " + str(self.VtRes) + " Orientation " + (
                    cfg_enum.Rotation(self.rotation)).name
                mode_str += " RR " + str(self.refreshRate) + "Hz" + " Scaling " + (
                    cfg_enum.Scaling(self.scaling)).name + " BPP " + (cfg_enum.PixelFormat(self.BPP)).name
                mode_str += " ScanlineOrdering " + (cfg_enum.ScanlineOrdering(self.scanlineOrdering)).name
                mode_str += " Sampling Mode " + str(self.samplingMode.Value)
                # if full_details is True:
                mode_str += " PixelClock " + str(self.pixelClock_Hz) + " Hz"
        return mode_str


##
# @brief        Structure for Screen Capture
class ScreenCaptureArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('HzRes', ctypes.c_int),  # [Inout] Horizontal Resolution
        ('VtRes', ctypes.c_int),  # [Inout] Vertical Resolution
        ('BPP', ctypes.c_int),  # [Inout] Bit per pixel
    ]


##
# @brief        Structure Definition for Desktop_Image_Info (OS API).
class DisplayConfigDesktopImageInfo(ctypes.Structure):
    _fields_ = [
        ('PathSourceSize', wintypes.POINTL),  # [Inout] DesktopImageInfo PathSource Size
        ('DesktopImageRegion', wintypes.RECT),  # [Inout] DesktopImageInfo DesktopImageRegion
        ('DesktopImageClip', wintypes.RECT)  # [Inout] DesktopImageInfo DesktopImageClip
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Path Source Size : X={self.PathSourceSize.x}, y={self.PathSourceSize.y}," \
               f" Desktop Image Region : Left={self.DesktopImageRegion.left}, Top={self.DesktopImageRegion.top}," \
               f" Right={self.DesktopImageRegion.right}, Bottom={self.DesktopImageRegion.bottom}" \
               f" Desktop Image Clip : Left={self.DesktopImageClip.left}, Top={self.DesktopImageClip.top}," \
               f" Right={self.DesktopImageClip.right}, Bottom={self.DesktopImageClip.bottom}"


##
# @brief        Structure Definition for DisplayConfig Source Mode (OS API).
class DisplayConfigSourceMode(ctypes.Structure):
    _fields_ = [
        ('width', ctypes.c_uint32),  # [Inout]  SourceMode Width
        ('height', ctypes.c_uint32),  # [Inout]  SourceMode Height
        ('pixelFormat', ctypes.c_uint32),  # [Inout]  SourceMode Pixel Format
        ('position', wintypes.POINTL)  # [Inout] SourceMode position
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Width : {self.width}, Height : {self.height}, PixelFormat : {self.pixelFormat}," \
               f" Position :  X={self.position.x}, y={self.position.y}"


##
# @brief        Structure Definition for DisplayConfig_2DRegion in DisplayConfig_VideoSignalInfo (OS API).
class DisplayConfig2DRegion(ctypes.Structure):
    _fields_ = [
        ('cx', ctypes.c_uint32),  # [Inout]  TargetMode Active/Total X (Width)
        ('cy', ctypes.c_uint32)  # [Inout]  TargetMode Active/Total Y (Height)
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"2D Region - X: {self.cx}, Y: {self.cy}"


##
# @brief        Structure Definition for DisplayConfig_Rational in DisplayConfig_VideoSignalInfo (OS API).
class DisplayConfigRational(ctypes.Structure):
    _fields_ = [
        ('Numerator', ctypes.c_uint32),  # [Inout]  HSYNC / VSYNC Numerator
        ('Denominator', ctypes.c_uint32)  # [Inout]  HSYNC / VSYNC Denominator
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Rational - Numerator: {self.Numerator}, Denominator: {self.Denominator}"


##
# @brief        Structure Definition for DisplayConfig_Rational in DisplayConfig_VideoSignalInfo (OS API).
class AdditionalSignalInfo(ctypes.Structure):
    _fields_ = [
        ('videoStandard', ctypes.c_uint32, 16),  # [Inout]  Video Standard
        ('vSyncFreqDivider', ctypes.c_uint32, 6),  # [Inout]  VSync Frequency Divider
        ('reserved', ctypes.c_uint32, 10)  # [Inout]  Reserved
    ]


##
# @brief        Structure Definition for VideoStandard
class DummyUnionVideoStandard(ctypes.Union):
    _anonymous_ = ("AdditionalSignalInfo",)
    _fields_ = [
        ('videoStandard', ctypes.c_uint32),  # [Inout]  Video Standard
        ('AdditionalSignalInfo', AdditionalSignalInfo)  # [InOut] AdditionalSignalInfo structure
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Video Standard: {self.AdditionalSignalInfo.videoStandard}, " \
               f"VSync Freq Divider: {self.AdditionalSignalInfo.vSyncFreqDivider}"


##
# @brief        Structure Definition for DisplayConfig_VideoSignalInfo in DisplayConfig Target Mode (OS API).
class DisplayConfigVideoSignalInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('pixelRate', ctypes.c_uint64),  # [Inout]  Target Mode Pixel Rate
        ('hSyncFreq', DisplayConfigRational),  # [Inout]  Target Mode HSYNC Freq
        ('vSyncFreq', DisplayConfigRational),  # [Inout]  Target Mode VSYNC Freq
        ('activeSize', DisplayConfig2DRegion),  # [Inout]  Target Mode Active Size
        ('totalSize', DisplayConfig2DRegion),  # [Inout]  Target Mode Total Size
        ('videoStandard', DummyUnionVideoStandard),  # [Inout]  Target Mode Video Standard information
        ('scanlineOrdering', ctypes.c_uint32)  # [Inout]  Target Mode ScanLine Ordering
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Pixel Rate: {self.pixelRate}, HSync: {self.hSyncFreq}, VSync: {self.vSyncFreq}," \
               f" ActiveSize: {self.activeSize}, TotalSize: {self.totalSize}, SignalInfo: {self.videoStandard}," \
               f" Scanline Ordering: {self.scanlineOrdering}"


##
# @brief        Structure Definition for DISPLAYCONFIG_TARGET_MODE (OS API).
class DisplayConfigTargetMode(ctypes.Structure):
    _fields_ = [
        ('targetVideoSignalInfo', DisplayConfigVideoSignalInfo)  # [Inout]  VideoSignalInfo for Target timing
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"{self.targetVideoSignalInfo}"


##
# @brief        Structure Definition for DUMMYSTRUCTNAME_PATH_SOURCE_INFO (OS API).
class DummyStructNamePathSourceInfo(ctypes.Structure):
    _fields_ = [
        ('cloneGroupId', ctypes.c_uint32, 16),  # [InOut] PATH_SOURCE_INFO cloneGroupId
        ('sourceModeInfoIdx', ctypes.c_uint32, 16)  # [InOut] PATH_SOURCE_INFO sourceModeInfoIdx
    ]


##
# @brief        Union Definition for DUMMYUNIONNAME_PATH_SOURCE_INFO (OS API).
class DummyUnionNamePathSourceInfo(ctypes.Union):
    _anonymous_ = ("dummyStruct",)
    _fields_ = [
        ('modeInfoIdx', ctypes.c_uint32),  # [InOut] PATH_SOURCE_INFO modeInfoIdx
        ('dummyStruct', DummyStructNamePathSourceInfo),  # [InOut] PATH_SOURCE_INFO DUMMYSTRUCTNAME_PATH_SOURCE_INFO
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Clone Group ID: {self.dummyStruct.cloneGroupId}, " \
               f"Src Mode Info Index: {self.dummyStruct.sourceModeInfoIdx}"


##
# @brief        Structure Definition for DISPLAYCONFIG_PATH_SOURCE_INFO (OS API).
class DisplayConfigPathSourceInfo(ctypes.Structure):
    _fields_ = [
        ('adapterId', adapter_struct.LUID),  # [Inout]  PATH_SOURCE_INFO adapterId
        ('id', ctypes.c_uint32),  # [Inout]  PATH_SOURCE_INFO id
        ('dummyUnion', DummyUnionNamePathSourceInfo),  # [Inout]  PATH_SOURCE_INFO DUMMYSTRUCTNAME_PATH_SOURCE_INFO
        ('statusFlags', ctypes.c_uint32)  # [Inout]  PATH_SOURCE_INFO statusFlags
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Adapter LUID: {self.adapterId}, Source ID: {self.id}, Mode Info Index : {self.dummyUnion}," \
               f" Status Flags: {self.statusFlags}"


##
# @brief        Structure Definition for DUMMYSTRUCTNAME_PATH_TARGET_INFO (OS API).
class DummyStructNamePathTargetInfo(ctypes.Structure):
    _fields_ = [
        ('desktopModeInfoIdx', ctypes.c_uint32, 16),  # PATH_TARGET_INFO desktopModeInfoIdx
        ('targetModeInfoIdx', ctypes.c_uint32, 16)  # PATH_TARGET_INFO targetModeInfoIdx
    ]


##
# @brief        Union Definition for DUMMYUNIONNAME_PATH_TARGET_INFO (OS API).
class DummyUnionPathTargetInfo(ctypes.Union):
    _anonymous_ = ("dummyStruct",)
    _fields_ = [
        ('modeInfoIdx', ctypes.c_uint32),  # PATH_TARGET_INFO modeInfoIdx
        ('dummyStruct', DummyStructNamePathTargetInfo)  # PATH_TARGET_INFO DUMMYSTRUCTNAME_PATH_TARGET_INFO
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Desktop Mode Info Idx: {self.dummyStruct.desktopModeInfoIdx}, " \
               f"Target Mode Info Idx: {self.dummyStruct.targetModeInfoIdx}"


##
# @brief        Structure Definition for DISPLAYCONFIG_PATH_TARGET_INFO (OS API).
class DisplayConfigPathTargetInfo(ctypes.Structure):
    _fields_ = [
        ('adapterId', adapter_struct.LUID),  # [Inout] Target Mode adapterId
        ('id', ctypes.c_uint32),  # [Inout] Target Mode id
        ('dummyUnion', DummyUnionPathTargetInfo),  # [Inout] Target Mode IndexInfoStructures
        ('outputTechnology', ctypes.c_uint32),  # [Inout] Target Mode outputTechnology
        ('rotation', ctypes.c_uint32),  # [Inout] Target Mode rotation
        ('displayConfigScaling', ctypes.c_uint32),  # [Inout] Target Mode scaling
        ('refreshRate', DisplayConfigRational),  # [Inout] Target Mode refreshRate
        ('scanlineOrdering', ctypes.c_uint32),  # [Inout] Target Mode scanLineOrdering
        ('targetAvailable', ctypes.c_bool),  # [Inout] Target Mode targetAvailable
        ('statusFlags', ctypes.c_uint32)  # [Inout] Target Mode statusFlags
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Adapter LUID: {self.adapterId}, Target ID: {self.id}, Mode Info Index : {self.dummyUnion}," \
               f" OutputTech: {self.outputTechnology}, Rotation: {self.rotation}," \
               f" Scaling: {self.displayConfigScaling}, RR: {self.refreshRate}," \
               f" Scanline Ordering: {self.scanlineOrdering}, Target Active: {self.targetAvailable}," \
               f" Status Flags: {self.statusFlags}"


##
# @brief        Structure Definition for DISPLAYCONFIG_PATH_INFO (OS API).
class DisplayConfigPathInfo(ctypes.Structure):
    _fields_ = [
        ('sourceInfo', DisplayConfigPathSourceInfo),  # [Inout] DISPLAYCONFIG_PATH_SOURCE_INFO
        ('targetInfo', DisplayConfigPathTargetInfo),  # [Inout] DISPLAYCONFIG_PATH_TARGET_INFO
        ('flags', ctypes.c_uint32)  # [Inout] Flag
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Source: {self.sourceInfo}, Target: {self.targetInfo}, Flags: {self.flags}"


##
# @brief        Union Definition for DUMMYUNIONNAME_MODE_INFO (OS API).
class DummyUnionModeInfo(ctypes.Union):
    _fields_ = [
        ('targetMode', DisplayConfigTargetMode),
        ('sourceMode', DisplayConfigSourceMode),
        ('desktopImageInfo', DisplayConfigDesktopImageInfo),
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Target Mode: {self.targetMode}, Source Mode: {self.sourceMode}, " \
               f"Desktop Image Info : {self.desktopImageInfo}"


##
# @brief        Structure Definition for DISPLAYCONFIG_MODE_INFO (OS API).
class DisplayConfigModeInfo(ctypes.Structure):
    _fields_ = [
        ('infoType', ctypes.c_uint),
        ('id', ctypes.c_uint32),
        ('adapterId', adapter_struct.LUID),
        ('dummyUnion', DummyUnionModeInfo),
    ]

    ##
    # @brief        Overridden str method
    # @return       None
    def __str__(self):
        return f"Mode Info = Info Type: {self.infoType}, ID: {self.id}, Adapter LUID: {self.adapterId}," \
               f" Info - {self.dummyUnion}"


##
# @brief        Structure Definition for QueryDisplay.
class QueryDisplay(ctypes.Structure):
    _fields_ = [
        ('qdcFlag', ctypes.c_uint32),  # [Inout]  Flag for QueryDisplayConfig API
        ('targetId', ctypes.c_uint32),  # [Inout]  targetId of requested panel
        ('topologyId', ctypes.c_uint32),  # [Inout]  topology Current Topology information
        ('pathInfo', DisplayConfigPathInfo),  # [Inout] DISPLAYCONFIG_PATH_INFO
        ('targetModeInfo', DisplayConfigTargetMode),  # [InOut] DISPLAYCONFIG_TARGET_MODE
        ('sourceModeInfo', DisplayConfigSourceMode),  # [InOut] DISPLAYCONFIG_SOURCE_MODE
        ('desktopImageInfo', DisplayConfigDesktopImageInfo),  # [InOut] DISPLAYCONFIG_DESKTOP_IMAGE_INFO
        ('status', ctypes.c_ulong)  # [Inout] Status for QDC
    ]


##
# @brief        Structure Definition for supported display modes.
class DisplayModeList(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('targetId', ctypes.c_int),  # [Inout]  Windows Monitor ID
        ('pDisplayMode', ctypes.POINTER(DisplayMode)),  # [Inout] Supported Display Modes for particular target ID
        ('noOfDisplayModes', ctypes.c_int),  # [Inout] No of Display modes supported
        ('status', ctypes.c_int)  # [Out] Error Code of type DISPLAY_CONFIG_ERROR_CODE
    ]


##
# @brief        Structure definition for supported mode list for specified target ids.
class SupportedModeList(ctypes.Structure):
    _fields_ = [
        ('size', ctypes.c_int),  # [In] Size of SUPPORTED_MODE_LIST
        ('supportedDisplayModes', DisplayModeList * MAX_SUPPORTED_DISPLAYS),  # [Out] All active displays mode list
        ('noOfSupportedModes', ctypes.c_int),  # [Out] No of active display mode list
        ('status', ctypes.c_int)  # [Out] Error Code of type DISPLAY_CONFIG_ERROR_CODE
    ]


##
# @brief        Struct for all the ModeList
class ModeList(ctypes.Structure):
    _fields_ = [
        ('modeList', DisplayMode * MAX_SUPPORTED_DISPLAYS),  # [In] Display mode list
        ('count', ctypes.c_int),  # [In] No of display modes
        ('delay_Ms', ctypes.c_int),
        # [Inout_opt] Optional delay parameter (ms), after mode set wait for specified delay in ms
        ('status', ctypes.c_int)  # [Out] Error Code of type DISPLAY_CONFIG_ERROR_CODE
    ]


##
# @brief        Structure Definition for Display Mode (Resolution) Information.
class EnumeratedDisplayModes(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('size', ctypes.c_int),  # [In] Size of EnumeratedDisplayModes Structure
        ('pDisplayModes', ctypes.POINTER(DisplayMode)),  # [Out] POINTER of DisplayMode Structure
        ('noOfSupportedModes', ctypes.c_int),  # [Out] Number of Supported Modes
        ('status', ctypes.c_int)  # [Out] Error Status of type DISPLAY_CONFIG_ERROR_CODE
    ]


##
# @brief        Structure Definition for ACTIVE_DISPLAY_INFO Information.
class ActiveDisplayInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('targetId', ctypes.c_uint),
        ('sourceId', ctypes.c_uint),
        ('pathIndex', ctypes.c_uint),
        ('cloneGroupCount', ctypes.c_uint),
        ('extendedGroupCount', ctypes.c_uint),
        ('cloneGroupTargetIds', ctypes.c_uint * MAX_SUPPORTED_DISPLAYS),
        ('extendedGroupTargetIds', ctypes.c_uint * MAX_SUPPORTED_DISPLAYS),
        ('displayAndAdapterInfo', DisplayAndAdapterInfo)
    ]


##
# @brief        Structure Definition for ACTIVE_DISPLAY_INFO Information.
class ActiveDisplayConfig(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('size', ctypes.c_uint),
        ('topology', ctypes.c_uint),
        ('numberOfDisplays', ctypes.c_uint),
        ('displayInfo', ActiveDisplayInfo * MAX_SUPPORTED_DISPLAYS),
        ('status', ctypes.c_uint)
    ]


##
# @brief        Structure Definition to Get Enumerated Displays Information.
class EnumeratedDisplaysEx(ctypes.Structure):
    _fields_ = [('Size', ctypes.c_int),
                ('ConnectedDisplays', DisplayInfo * MAX_SUPPORTED_DISPLAYS),
                ('Count', ctypes.c_int)]

    ##
    # @brief        String representation of Enumerated displays
    # @return       enumerated_displays_str - Representation of EnumeratedDisplaysEx class
    def to_string(self):
        enumerated_displays_str = ""
        for display_index in range(self.Count):
            if display_index:
                enumerated_displays_str += "\n"
            enumerated_displays_str += (
                cfg_enum.CONNECTOR_PORT_TYPE(self.ConnectedDisplays[display_index].ConnectorNPortType)).name
            enumerated_displays_str += ": PortType " + str(self.ConnectedDisplays[display_index].PortType)
            enumerated_displays_str += " Target ID " + str(hex(self.ConnectedDisplays[display_index].TargetID))
            enumerated_displays_str += " Active " if self.ConnectedDisplays[
                                                         display_index].IsActive is True else " Inactive"
            enumerated_displays_str += " DisplayAdapter Target ID " + str(hex(
                self.ConnectedDisplays[display_index].DisplayAndAdapterInfo.TargetID))
            enumerated_displays_str += " DisplayAdapter Vendor ID " + str(
                self.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.vendorID)
            enumerated_displays_str += " DisplayAdapter Device ID " + str(
                self.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.deviceID)
            enumerated_displays_str += " DisplayAdapter Device Instance ID " + str(
                self.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.deviceInstanceID)
            enumerated_displays_str += " DisplayAdapter Index " + str(
                self.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex)
        return enumerated_displays_str


####################################################################################################################

##
# @brief        Structure Definition to Get Enumerated Displays Information.
class OsTopologyInfo(ctypes.Structure):
    _fields_ = [('TargetModeInfo', DisplayConfigTargetMode),
                ('SourceModeInfo', DisplayConfigSourceMode),
                ('DesktopImageInfo', DisplayConfigDesktopImageInfo),
                ('PathInfo', DisplayConfigPathInfo)]


##
# @brief        Display Path Information
class DisplayPathInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('pathIndex', ctypes.c_int),  # [Inout] Connector type (Display Type) connected to which path
        ('targetId', ctypes.c_uint),  # [Inout] Windows Monitor ID. Will be moved to DisplayAndAdapterInfo
        ('sourceId', ctypes.c_int),  # [Out] Source device ID
        ('isActive', ctypes.c_bool),  # [Inout_opt] Specify whether display is currently active or not
        ('displayAndAdapterInfo', DisplayAndAdapterInfo),
        ('CloneGroupCount', ctypes.c_uint),  #
        ('ExtendedGroupCount', ctypes.c_uint),  #
        ('CloneGroupPathIds', ctypes.c_uint * MAX_SUPPORTED_DISPLAYS),  #
        ('ExtendedGroupPathIds', ctypes.c_uint * MAX_SUPPORTED_DISPLAYS),  #
        ('OsTopologyInfo', OsTopologyInfo),  #
    ]


##
# @brief        Structure Definition for Display Configuration
class DisplayConfig(ctypes.Structure):
    _fields_ = [
        ('size', ctypes.c_int),  # [In] Size of DisplayConfig
        ('topology', ctypes.c_int),  # [Inout] Display Configuration topology (SINGLE/CLONE/EXTENDED)
        ('displayPathInfo', DisplayPathInfo * MAX_SUPPORTED_DISPLAYS),  # [Inout] List of DisplayPathInfo Structure
        ('numberOfDisplays', ctypes.c_int),  # [Inout] No of connected displays (active or inactive)
        ('status', ctypes.c_int)  # [Out] Error Code of type DISPLAY_CONFIG_ERROR_CODE
    ]

    ##
    # @brief        Get DisplayAndAdapterInfo object based on get_config
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    port_name - Connector port name
    # @return       display_and_adapter_info_list - List of DisplayAndAdapterInfo object
    def get_display_and_adapter_info(self, gfx_index: str, port_name: str) -> List[DisplayAndAdapterInfo]:
        display_and_adapter_info_list = []
        logging.info(f"Connected Displays Count - {self.numberOfDisplays}, in: {gfx_index} and {port_name}")
        for display_index in range(self.numberOfDisplays):
            if cfg_enum.CONNECTOR_PORT_TYPE(
                    self.displayPathInfo[display_index].displayAndAdapterInfo.ConnectorNPortType).name == port_name and \
                    self.displayPathInfo[display_index].displayAndAdapterInfo.adapterInfo.gfxIndex == gfx_index:
                display_and_adapter_info_list.append(self.displayPathInfo[display_index].displayAndAdapterInfo)
        return display_and_adapter_info_list

    ##
    # @brief        Get Driver Type
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       DriverBranch - DriverType Enum value
    def get_driver_type(self, gfx_index: str) -> int:
        driver_branch = cfg_enum.DriverType.UNKNOWN
        for display_index in range(self.numberOfDisplays):
            if self.displayPathInfo[display_index].displayAndAdapterInfo.adapterInfo.gfxIndex == gfx_index:
                return cfg_enum.DriverType(self.displayPathInfo[display_index].displayAndAdapterInfo.DriverBranch)
        # Invalid Driver Type
        return driver_branch

    ##
    # @brief        Compare display configurations.
    # @param[in]    config - Base configuration to be compared with current config
    # @return       bool - True if config matches else False
    def equals(self, config):
        if (self.status == cfg_enum.enum.DISPLAY_CONFIG_SUCCESS and self.status == config.status
                and self.topology == config.topology and self.numberOfDisplays == config.numberOfDisplays):
            for num_disp in range(0, config.numberOfDisplays):
                adapter_info = self.displayPathInfo[num_disp].displayAndAdapterInfo.adapterInfo
                config_adapter_info = config.displayPathInfo[num_disp].displayAndAdapterInfo.adapterInfo
                if (self.displayPathInfo[num_disp].targetId != config.displayPathInfo[num_disp].targetId or
                        adapter_info.busDeviceID != config_adapter_info.busDeviceID or
                        adapter_info.deviceInstanceID != config_adapter_info.deviceInstanceID):
                    return False
        else:
            return False
        return True

    ##
    # @brief        String representation of Display configuration
    # @param[in]    enumerated_displays - Enumerated displays info
    # @return       config_str - String representation of DisplayConfig object
    def to_string(self, enumerated_displays):
        config_str = (cfg_enum.DisplayConfigTopology(self.topology)).name + " :"
        for display_index in range(self.numberOfDisplays):
            for eachDisplay in enumerated_displays.ConnectedDisplays:
                adapter_info = self.displayPathInfo[display_index].displayAndAdapterInfo.adapterInfo
                enum_adapter_info = eachDisplay.DisplayAndAdapterInfo.adapterInfo
                if self.displayPathInfo[display_index].targetId == eachDisplay.TargetID and \
                        adapter_info.busDeviceID == enum_adapter_info.busDeviceID and \
                        adapter_info.deviceInstanceID == enum_adapter_info.deviceInstanceID:
                    config_str += " [" + (cfg_enum.CONNECTOR_PORT_TYPE(
                        eachDisplay.ConnectorNPortType)).name + "_" + eachDisplay.PortType + "]"
        return config_str

    ##
    # @brief        String representation of Display configuration
    # @param[in]    enumerated_displays - Enumerated displays info
    # @return       config_str - String representation of DisplayConfig object
    def to_string_with_target_id(self, enumerated_displays):
        config_str = (cfg_enum.DisplayConfigTopology(self.topology)).name + " :"
        for display_index in range(self.numberOfDisplays):
            for eachDisplay in enumerated_displays.ConnectedDisplays:
                adapter_info = self.displayPathInfo[display_index].displayAndAdapterInfo.adapterInfo
                enum_adapter_info = eachDisplay.DisplayAndAdapterInfo.adapterInfo
                if self.displayPathInfo[display_index].targetId == eachDisplay.TargetID and \
                        adapter_info.busDeviceID == enum_adapter_info.busDeviceID and \
                        adapter_info.deviceInstanceID == enum_adapter_info.deviceInstanceID:
                    config_str += " [" + (cfg_enum.CONNECTOR_PORT_TYPE(
                        eachDisplay.ConnectorNPortType)).name + "_" + eachDisplay.PortType \
                                  + ", " + str(eachDisplay.TargetID) + "]"
        return config_str

####################################################################################################################
