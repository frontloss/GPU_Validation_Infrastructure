###################################################################################################################
# @file     display_collage.py
# @brief    Python wrapper exposes API's related to DisplayPort DLL
# @author   Praveen Bademi
##########################################################################################################################

import ctypes
import os

from Libs.Core import system_utility
from Libs.Core.core_base import singleton
from Libs.Core.test_env import test_context

MAX_VALID_CONFIG = 500
MAX_MONITORS_PER_ADAPTER = 6
MAX_MULTIPLE_DISPLAYS = 16
MAX_NUMBER_OF_MODES = 500

IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_HORZCOLLAGE = 0x6  # Dual Horizontal Collage
GFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_VERTCOLLAGE = 0x7  # Dual Vertical Collage
IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_HORZCOLLAGE = 0x8  # Tri Horizontal Collage
IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_VERTCOLLAGE = 0x9  # Tri Vertical Collage


##
# @brief        Structure Definition to Config Data
class IGFX_CONFIG_DATA_EX(ctypes.Structure):
    _fields_ = [('dwOperatingMode', ctypes.c_ulong),  # Operating Mode
                ('dwNDisplays', ctypes.c_ulong),  # Number of displays
                ('dwPriDevUID', ctypes.c_ulong),
                # Device on Primary Display( For Single Pipe Simultaneous mode, both devices are here )
                ('dwSecDevUID', ctypes.c_ulong),  # Device on Secondary Display
                ('dwThirdDevUID', ctypes.c_ulong),  # Device on Third Display
                ('dwFourthDevUID', ctypes.c_ulong)]  # Device on Fourth Display


##
# @brief        Structure Definition to Version Header
class IGFX_VERSION_HEADER(ctypes.Structure):
    _fields_ = [('dwVersion', ctypes.c_ulong),
                ('dwReserved', ctypes.c_ulong)]


##
# @brief        Structure Definition to Get Valid Supported COnfigurations.
class IGFX_TEST_CONFIG_EX(ctypes.Structure):
    _fields_ = [('versionHeader', IGFX_VERSION_HEADER),
                ('dwNumTotalCfg', ctypes.c_ulong),  # Total of validation configuration in the following array
                ('dwReserved1', ctypes.c_ulong),
                ('dwReserved2', ctypes.c_ulong),
                ('ConfigList', IGFX_CONFIG_DATA_EX * MAX_VALID_CONFIG)]  # Valid device combinations, upto 7 devices


##
# @brief        Structure Definition to Get Display Resolution.
class IGFX_DISPLAY_RESOLUTION_EX(ctypes.Structure):
    _fields_ = [('dwHzRes', ctypes.c_ulong),  # Horizontal Resolution
                ('dwVtRes', ctypes.c_ulong),  # Vertical Resolution
                ('dwRR', ctypes.c_ulong),  # Refresh Rate
                ('dwBPP', ctypes.c_ulong),  # Color Depth
                ('dwSupportedStandard', ctypes.c_bool),
                ('dwPreferredStandard', ctypes.c_ulong),
                ('InterlaceFlag', ctypes.c_ushort)]


##
# @brief        Structure Definition to Get Display Position
class IGFX_DISPLAY_POSITION(ctypes.Structure):
    _fields_ = [('iLeft', ctypes.c_int),  # Position - Left
                ('iRight', ctypes.c_int),  # Position - Right
                ('iTop', ctypes.c_int),  # Position - Top
                ('iBottom', ctypes.c_int)]  # Position - Bottom


##
# @brief        Structure Definition to Get Display Data(Extended).
class IGFX_DISPLAY_CONFIG_DATA_EX(ctypes.Structure):
    _fields_ = [('dwDisplayUID', ctypes.c_ulong),  # Display Device UID for this display
                ('Resolution', IGFX_DISPLAY_RESOLUTION_EX),  # Display Mode
                ('Position', IGFX_DISPLAY_POSITION),  # Display Position
                ('dwTvStandard', ctypes.c_ulong),
                ('bIsHDTV', ctypes.c_bool),
                ('dwOrientation', ctypes.c_ulong),  # Orientation
                ('dwScaling', ctypes.c_ulong),
                ('dwFlags', ctypes.c_ulong)]


##
# @brief        Structure Definition to Get display data to apply collage
class IGFX_SYSTEM_CONFIG_DATA_N_VIEW(ctypes.Structure):
    _fields_ = [('dwOpMode', ctypes.c_ulong),  # Operating Mode
                ('dwFlags', ctypes.c_ulong),
                ('uiSize', ctypes.c_uint),  # size of input buffer
                ('uiNDisplays', ctypes.c_uint),  # number of displays
                ('DispCfg', IGFX_DISPLAY_CONFIG_DATA_EX * MAX_MULTIPLE_DISPLAYS)]  # Array of Display Data


##
# @brief        Structure Definition to Get Display Resolution.
class IGFX_DISPLAY_RESOLUTION_EX(ctypes.Structure):
    _fields_ = [('dwHzRes', ctypes.c_ulong),  # Horizontal Resolution
                ('dwVtRes', ctypes.c_ulong),  # Vertical Resolution
                ('dwRR', ctypes.c_ulong),  # Refresh Rate
                ('dwBPP', ctypes.c_ulong),  # Bits per pixel
                ('dwSupportedStandard', ctypes.c_ulong),
                ('dwPreferredStandard', ctypes.c_ulong),
                ('InterlaceFlag', ctypes.c_ushort)]


##
# @brief        Structure Definition to Get list of modes supported.
class IGFX_VIDEO_MODE_LIST_EX(ctypes.Structure):
    _fields_ = [('versionHeader', IGFX_VERSION_HEADER),  # header version
                ('dwOpMode', ctypes.c_ulong),  # Operating Mode
                ('uiNDisplays', ctypes.c_uint),  # Number of displays
                ('DispCfg', IGFX_DISPLAY_CONFIG_DATA_EX * MAX_MONITORS_PER_ADAPTER),  # array fo display data
                ('dwDeviceID', ctypes.c_ulong),  # device id to which mode to be applied
                ('dwFlags', ctypes.c_ulong),
                ('vmlNumModes', ctypes.c_ushort),
                ('dwReserved', ctypes.c_ulong),
                ('vmlModes',
                 IGFX_DISPLAY_RESOLUTION_EX * MAX_NUMBER_OF_MODES)]  # array of supported modes for targetted device id


##
# @brief        Collage Class
@singleton
class Collage(object):

    ##
    # @brief    Display Port constructor.
    def __init__(self):
        # Load DisplayPort C library.
        self.display_port_dll = ctypes.cdll.LoadLibrary(
            os.path.join(test_context.TestContext.bin_store(), 'DisplayPort.dll'))

        ##
        # Create SystemUtility object
        self.system_utility = system_utility.SystemUtility()

    ##
    # @brief    Exposed API to get the collage feature support information
    # @return   retStatus - bool
    def get_collage_info(self):
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool)
        func = prototype(('GetCollageInfo', self.display_port_dll))
        retStatus = func()
        return retStatus

    ##
    # @brief    Exposed API to verify if collage is enabled.
    # @return   retStatus
    def is_collage_enabled(self):
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool)
        func = prototype(('IsCollageEnabled', self.display_port_dll))
        retStatus = func()
        return retStatus

    ##
    # @brief        Exposed API to set the collage mode
    # @param[in]    system_config_ex_data - System config ex Data
    # @return       retStatus
    def apply_collage_mode(self, system_config_ex_data):
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(IGFX_SYSTEM_CONFIG_DATA_N_VIEW))
        func = prototype(('ApplyCollage', self.display_port_dll))
        retStatus = func(ctypes.byref(system_config_ex_data))
        return retStatus

    ##
    # @brief        Exposed API to get the all supported configurations for connected displays
    # @return       (retStatus,config_ex)
    def get_supported_config(self):
        config_ex = IGFX_TEST_CONFIG_EX()
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(IGFX_TEST_CONFIG_EX))
        func = prototype(('GetSupportedConfig', self.display_port_dll))
        retStatus = func(ctypes.byref(config_ex))
        return retStatus, config_ex

    ##
    # @brief        Exposed API to get all the supported modes for applied config
    # @param[in]    system_config_ex_data - System config ex Data
    # @param[in]    display_index - Display Index to be used
    # @return       (retStatus,mode_list) - (bool,list)
    def get_supported_modes_collage(self, system_config_ex_data, display_index):
        mode_list = IGFX_VIDEO_MODE_LIST_EX()
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(IGFX_SYSTEM_CONFIG_DATA_N_VIEW), ctypes.c_uint,
                                      ctypes.POINTER(IGFX_VIDEO_MODE_LIST_EX))
        func = prototype(('Collage_GetSupportedModes', self.display_port_dll))
        retStatus = func(ctypes.byref(system_config_ex_data), display_index, ctypes.byref(mode_list))
        return retStatus, mode_list
