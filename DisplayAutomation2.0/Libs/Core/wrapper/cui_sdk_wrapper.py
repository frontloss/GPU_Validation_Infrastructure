########################################################################################################################
# @file         cui_sdk_wrapper.py
# @brief        Contains wrapper functions calling Cui Sdk CDLL exposed APIs only.
# @author       Amit Sau , Kasthuri R, Kiran Kumar Lakshmanan
########################################################################################################################
import ctypes
import logging
import os

from Libs.Core.test_env.test_context import BIN_FOLDER

DISPLAY_DATA = 16
MAX_VALID_CONFIG = 500
GAMMA_VALUE = 9
CSC_COEFFICIENTS = 3
MAX_MONITORS_PER_ADAPTER = 6

RED_GAMMA = 0x00
GREEN_GAMMA = 0x01
BLUE_GAMMA = 0x02
RED_BRIGHTNESS = 0x03
GREEN_BRIGHTNESS = 0x04
BLUE_BRIGHTNESS = 0x05
RED_CONTRAST = 0x06
GREEN_CONTRAST = 0x07
BLUE_CONTRAST = 0x08

_cuisdk_dll = None


##
# @brief        ColorData Structure
class ColorData(ctypes.Structure):
    _fields_ = [
        ('currentValue', ctypes.c_float),
        ('defaultValue', ctypes.c_float),
        ('minValue', ctypes.c_float),
        ('maxValue', ctypes.c_float),
        ('stepValue', ctypes.c_float)
    ]

    ##
    # @brief        Constructor
    # @param[in]    current_value - Current Value of Color Data
    def __init__(self, current_value=0):
        self.currentValue = 0
        self.defaultValue = 0
        self.minValue = 0
        self.maxValue = 0
        self.stepValue = 0


##
# @brief        VersionHeader Structure
class VersionHeader(ctypes.Structure):
    _fields_ = [
        ('version', ctypes.c_ulong),
        ('reserved', ctypes.c_ulong)
    ]

    ##
    # @brief        Constructor
    # @param[in]    version - version number
    def __init__(self, version=0):
        self.version = version


##
# @brief        DesktopGammaArgs Structure
class DesktopGammaArgs(ctypes.Structure):
    _fields_ = [
        ('deviceID', ctypes.c_ulong),
        ('flags', ctypes.c_ulong),
        ('gammaValues', (ctypes.c_long * GAMMA_VALUE))
    ]

    ##
    # @brief        constructor
    # @param[in]    device_id - Target ID of panel
    # @param[in]    gamma - RGB gamma value
    # @param[in]    brightness - brightness value
    # @param[in]    contrast - contrast value
    def __init__(self, device_id, gamma=4, brightness=0, contrast=50):
        self.deviceID = device_id
        self.gammaValues[RED_GAMMA] = gamma
        self.gammaValues[GREEN_GAMMA] = gamma
        self.gammaValues[BLUE_GAMMA] = gamma
        self.gammaValues[RED_BRIGHTNESS] = brightness
        self.gammaValues[GREEN_BRIGHTNESS] = brightness
        self.gammaValues[BLUE_BRIGHTNESS] = brightness
        self.gammaValues[RED_CONTRAST] = contrast
        self.gammaValues[GREEN_CONTRAST] = contrast
        self.gammaValues[BLUE_CONTRAST] = contrast


##
# @brief        HueSatInfo Structure
class HueSatInfo(ctypes.Structure):
    _fields_ = [
        ('isFeatureSupported', ctypes.c_int),
        ('isRGB', ctypes.c_int),
        ('deviceID', ctypes.c_ulong),
        ('hueSettings', ColorData),
        ('saturationSettings', ColorData),
        ('flags', ctypes.c_ulong)
    ]

    ##
    # @brief        Constructor
    # @param[in]    device_id - Target ID of Panel
    # @param[in]    hue_value - HUE value
    # @param[in]    sat_value - SAT Value
    def __init__(self, device_id=0, hue_value=0, sat_value=0):
        self.isFeatureSupported = 0
        self.isRGB = 0
        self.deviceID = device_id
        self.hueSettings = ColorData(current_value=hue_value)
        self.saturationSettings = ColorData(current_value=sat_value)
        self.flags = 0


##
# @brief        GamutExpansion Structure
class GamutExpansion(ctypes.Structure):
    _fields_ = [
        ('versionHeader', VersionHeader),
        ('deviceID', ctypes.c_ulong),
        ('isFeatureSupported', ctypes.c_int),
        ('gamutExpansionLevel', ctypes.c_ulong),
        ('useCustomerCsc', ctypes.c_int),
        ('customCscMatrix', ctypes.c_float * CSC_COEFFICIENTS * CSC_COEFFICIENTS),
        ('reserved', ctypes.c_ulong)
    ]

    ##
    # @brief        Constructor
    # @param[in]    device_id - Device ID
    # @param[in]    gamut_expansion_level - Gamma Expansion level of RGB
    def __init__(self, device_id=0, gamut_expansion_level=0):
        self.versionHeader = VersionHeader(version=1)
        self.deviceID = device_id
        self.isFeatureSupported = 0
        self.gamutExpansionLevel = gamut_expansion_level
        self.useCustomerCsc = 0


##
# @brief        Gamut Structure
class Gamut(ctypes.Structure):
    _fields_ = [
        ('versionHeader', VersionHeader),
        ('deviceID', ctypes.c_ulong),
        ('isFeatureSupported', ctypes.c_int),
        ('enableDisable', ctypes.c_int),
        ('reserved', ctypes.c_ulong)
    ]

    ##
    # @brief        Constructor
    # @param[in]    device_id - Device ID
    # @param[in]    enable_disable - Enable and Disable Function
    def __init__(self, device_id=0, enable_disable=0):
        self.versionHeader = VersionHeader(version=1)
        self.deviceID = device_id
        self.isFeatureSupported = 0
        self.enableDisable = enable_disable


##
# @brief        CollageStatus Structure
class CollageStatus(ctypes.Structure):
    _fields_ = [
        ('versionHeader', VersionHeader),
        ('isCollageModeSupported', ctypes.c_bool),
        ('defaultCollageStatus', ctypes.c_bool),
        ('isCollageModeEnabled', ctypes.c_bool)
    ]


##
# @brief        DisplayPositionInfo Structure
class DisplayPositionInfo(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_int),
        ('right', ctypes.c_int),
        ('top', ctypes.c_int),
        ('bottom', ctypes.c_int)
    ]


##
# @brief        DisplayResolutionInfo Structure
class DisplayResolutionInfo(ctypes.Structure):
    _fields_ = [
        ('horizontalResolution', ctypes.c_ulong),
        ('verticalResolution', ctypes.c_ulong),
        ('refreshRate', ctypes.c_ulong),
        ('bitsPerPixel', ctypes.c_ulong),
        ('supportedStandard', ctypes.c_ulong),
        ('preferredStandard', ctypes.c_ulong),
        ('interlaceFlag', ctypes.c_ushort)
    ]


##
# @brief        DisplayConfigInfo Structure
class DisplayConfigInfo(ctypes.Structure):
    _fields_ = [
        ('displayID', ctypes.c_ulong),
        ('displayResolution', DisplayResolutionInfo),
        ('displayPosition', DisplayPositionInfo),
        ('tvStandard', ctypes.c_ulong),
        ('isHDTV', ctypes.c_bool),
        ('orientation', ctypes.c_ulong),
        ('scaling', ctypes.c_ulong),
        ('flags', ctypes.c_ulong)
    ]


##
# @brief        SystemConfigData Structure
class SystemConfigData(ctypes.Structure):
    _fields_ = [
        ('operatingMode', ctypes.c_ulong),
        ('flags', ctypes.c_ulong),
        ('size', ctypes.c_uint),
        ('noOfDisplays', ctypes.c_uint),
        ('displayConfigInfo', DisplayConfigInfo * DISPLAY_DATA)
    ]


##
# @brief        ConfigData Structure
class ConfigData(ctypes.Structure):
    _fields_ = [
        ('opMode', ctypes.c_ulong),
        ('numberOfDisplays', ctypes.c_ulong),
        ('primaryDeviceUID', ctypes.c_ulong),
        ('secondaryDeviceUID', ctypes.c_ulong),
        ('thirdDeviceUID', ctypes.c_ulong),
        ('fourthdeviceUID', ctypes.c_ulong)
    ]


##
# @brief        TestConfigData Structure
class TestConfigData(ctypes.Structure):
    _fields_ = [
        ('versionHeader', VersionHeader),
        ('totalConfig', ctypes.c_ulong),
        ('reserved1', ctypes.c_ulong),
        ('reserved2', ctypes.c_ulong),
        ('configData', ConfigData * MAX_VALID_CONFIG)
    ]


##
# @brief        VideoModeList Structure
class VideoModeList(ctypes.Structure):
    _fields_ = [
        ('versionHeader', VersionHeader),
        ('opMode', ctypes.c_ulong),
        ('numberOfDisplays', ctypes.c_uint),
        ('displayConfigData', DisplayConfigInfo * MAX_MONITORS_PER_ADAPTER),
        ('deviceID', ctypes.c_ulong),
        ('flags', ctypes.c_ulong),
        ('vmlNumberModes', ctypes.c_ushort),
        ('reserved', ctypes.c_ulong),
        ('displayResolution', DisplayResolutionInfo * 1)
    ]


##
# @brief        Cui_SDK load library.
# @return       None
def load_library():
    global _cuisdk_dll
    try:
        _cuisdk_dll = ctypes.cdll.LoadLibrary(os.path.join(BIN_FOLDER, 'CuiSdk.dll'))
    except IOError as error:
        # captures both File not Found error and LoadLibrary failed errors.
        raise Exception(f'Failed to Load CuiSdk Library : {error}')


##
# @brief        Initialize or Uninitialze CUI SDK
# @param[in]    flag - True to Initialize CUI SDK, False to uninitialize CUI SDK
# @return       None
def configure_sdk(flag: bool) -> None:
    if flag:
        if init_sdk():
            logging.info("---------------------Initialized CUI SDK---------------------")
    else:
        if uninit_sdk():
            logging.info("--------------------Uninitialized CUI SDK--------------------")


##
# @brief        Initialize CUI SDK
# @return       result - True if CUI SDK initialized successfully, False otherwise
def init_sdk() -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool)
    func = prototype(('InitializeCUISDKN', _cuisdk_dll))
    result = func()
    return result


##
# @brief        UnInitialize CUI SDK
# @return       result - True if CUI SDK uninitialized successfully, False otherwise
def uninit_sdk() -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool)
    func = prototype(('UninitializeCUISDKN', _cuisdk_dll))
    result = func()
    return result


##
# @brief         Get Desktop Gamma Color Info
# @param[in]     desktop_gamma_args - Pointer to structure DesktopGammaArgs
# @result        (result, desktop_gamma_args) - (Escape call status , DesktopGamma args info)
def get_desktop_gamma_color(desktop_gamma_args: DesktopGammaArgs) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DesktopGammaArgs))
    func = prototype(('GetDesktopGammaColor', _cuisdk_dll))
    result = func(ctypes.byref(desktop_gamma_args))
    return result, desktop_gamma_args


##
# @brief         Set Desktop Gamma Color info
# @param[in]     desktop_gamma_args - Pointer to structure DesktopGammaArgs
# @result        result - Escape call status
def set_desktop_gamma_color(desktop_gamma_args: DesktopGammaArgs) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DesktopGammaArgs))
    func = prototype(('SetDesktopGammaColor', _cuisdk_dll))
    result = func(ctypes.byref(desktop_gamma_args))
    return result


##
# @brief        Get Narrow Gamut info
# @param[in]    gamut_args - Pointer to structure Gamut
# @result       (result, gamut_args) - (Escape call status , Gamut args info)
def get_narrow_gamut(gamut_args: Gamut) -> (bool, Gamut):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(Gamut))
    func = prototype(('GetNarrowGamut', _cuisdk_dll))
    result = func(ctypes.byref(gamut_args))
    return result, gamut_args


##
# @brief        API to Configure Color Accuracy
# @param[in]    gamut - Object of type Gamut
# @return       result - Escape call status
def configure_color_accuracy(gamut: Gamut) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(Gamut))
    func = prototype(('ConfigureColorAccuracy', _cuisdk_dll))
    result = func(ctypes.byref(gamut))
    return result


##
# @brief         Get Hue and saturation information through HueSatInfo
# @param[in]     hue_sat_info - HueSatInfo object
# @result        (result, hue_sat_info) - (Escape call status , HueSatInfo args info)
def get_hue_sat_info(hue_sat_info: HueSatInfo) -> (bool, HueSatInfo):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(HueSatInfo))
    func = prototype(('GetHueSaturation', _cuisdk_dll))
    result = func(ctypes.byref(hue_sat_info))
    return result, hue_sat_info


##
# @brief         To set Hue and Saturation information
# @param[in]     hue_sat_info - Pointer to HueSatInfo Structure
# @result        result - Escape call status
def set_hue_sat_info(hue_sat_info: HueSatInfo) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(HueSatInfo))
    func = prototype(('SetHueSaturation', _cuisdk_dll))
    result = func(ctypes.byref(hue_sat_info))
    return result


##
# @brief         To GET Wide Gamut Expansion
# @param[in]     gamut_expansion - Pointer to GamutExpansion Structure
# @result        (result,gamut_expansion) - (Escape call status ,GamutExpansion args info)
def get_wide_gamut_expansion(gamut_expansion: GamutExpansion) -> (bool, GamutExpansion):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GamutExpansion))
    func = prototype(('GetWideGamutExpansion', _cuisdk_dll))
    result = func(ctypes.byref(gamut_expansion))
    return result, gamut_expansion


##
# @brief         To SET Wide Gamut Expansion
# @param[in]     gamut_expansion - Pointer to GamutExpansion Structure
# @result        result - Boolean Escape call status
def set_wide_gamut_expansion(gamut_expansion: GamutExpansion) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GamutExpansion))
    func = prototype(('SetWideGamutExpansion', _cuisdk_dll))
    result = func(ctypes.byref(gamut_expansion))
    return result


##
# @brief         To check if Collage is Enabled or Disabled
# @param[in]     collage_status - Pointer to CollageStatus
# @result        (result, collage_status) - (Escape call status , collage_status args info)
def is_collage_enabled(collage_status: CollageStatus) -> (bool, CollageStatus):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(CollageStatus))
    func = prototype(('IsCollageEnabled', _cuisdk_dll))
    result = func(ctypes.byref(collage_status))
    return result, collage_status


##
# @brief         To check if Collage is supported or not in the platform
# @param[in]     get_collage_info - Pointer to structure  CollageStatus
# @result        (result, get_collage_info) - (Escape call status , get_collage_info args info)
def get_collage_info(get_collage_info: CollageStatus) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(CollageStatus))
    func = prototype(('GetCollageInfo', _cuisdk_dll))
    result = func(ctypes.byref(get_collage_info))
    return result, get_collage_info


##
# @brief        To set the Collage Mode for the selected Displays
# @param[in]    system_config_data - Pointer to SystemConfigData Structure
# @result       result -Boolean Escape call status
def apply_collage(system_config_data: SystemConfigData) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(SystemConfigData))
    func = prototype(('ApplyCollage', _cuisdk_dll))
    result = func(ctypes.byref(system_config_data))
    return result


##
# @brief        Get all the supported Config, For Example: SD,DD CLone, Tri Clone, Tri ED, Dual Hor Collage, etc
# @param[in]    test_config_data - Pointer to TestConfigData Structure
# @result       result - Boolean Escape call status
def get_supported_config(test_config_data: TestConfigData) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(TestConfigData))
    func = prototype(('GetSupportedConfig', _cuisdk_dll))
    result = func(ctypes.byref(test_config_data))
    return result


##
# @brief         Get all the supported modes for the applied collage config
# @param[in]     size - Size to be allocated
# @param[in]     video_mode_list - VideoModeList object
# @result        (result, video_mode_list) - (Escape call status , VideoModeList args info)
def collage_get_supported_modes(size: int, video_mode_list: VideoModeList) -> (bool, VideoModeList):
    prototype = ctypes.PYFUNCTYPE((ctypes.c_bool, ctypes.c_ulong, ctypes.POINTER(VideoModeList)))
    func = prototype(('CollageGetSupportedModes', _cuisdk_dll))
    result = func(size, ctypes.byref(video_mode_list))
    return result, video_mode_list


##
# @brief         Verify whether expected and applied MST topologies are identical or not
# @param[in]     port_number - port number to verify the MST topology
# @result        result - Escape call status
def verfiy_mst_topology(port_number: int) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.c_ulong)
    func = prototype(('VerifyMstTopology', _cuisdk_dll))
    result = func(port_number)
    return result
