########################################################################################################################
# @file             flip.py
# @brief            Python Wrapper that exposes the interface for DFT Flips
# @details          Python Wrapper that provides interface to get the hardware support for planes,
#                   present multiple surfaces on the screen, check MPO capabilities.
# @author           Anjali Shetty
########################################################################################################################
# @copyright  INTEL CONFIDENTIAL
# Copyright 2016 Intel Corporation All Rights Reserved.
# The source code contained or described herein and all documents related
# to the source code ("Material") are owned by Intel Corporation or its
# suppliers or licensors. Title to the Material remains with Intel Corporation
# or its suppliers and licensors. The Material contains trade secrets and
# proprietary and confidential information of Intel or its suppliers and
# licensors. The Material is protected by worldwide copyright and trade secret
# laws and treaty provisions. No part of the Material may be used, copied,
# reproduced, modified, published, uploaded, posted, transmitted, distributed,
# or disclosed in any way without Intel's prior express written permission.
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be express
# and approved by Intel in writing.
#
#################################################################################

import ctypes
import logging
import os
import subprocess
import time
import win32api
import win32con
from Libs.Core import system_utility, enum, registry_access, display_essential, window_helper
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo, SystemDriverType
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from ctypes.wintypes import HANDLE
from Libs.Core.logger import gdhm

GDHM_FLIP = '[FLIP]'


MAX_PLANES = 21
MAX_RESOURCE = 2
MAX_PIPES = 4

VBIEnableExe = os.path.join(test_context.BIN_FOLDER, "VBIEnable.exe")

##
# @brief        PIXEL_FORMAT class
class PIXEL_FORMAT(object):
    PIXEL_FORMAT_UNINITIALIZED = 0
    PIXEL_FORMAT_8BPP_INDEXED = 1
    PIXEL_FORMAT_B5G6R5X0 = 2
    PIXEL_FORMAT_B8G8R8X8 = 3
    PIXEL_FORMAT_B8G8R8A8 = 4
    PIXEL_FORMAT_R8G8B8X8 = 5
    PIXEL_FORMAT_R8G8B8A8 = 6
    PIXEL_FORMAT_R10G10B10X2 = 7
    PIXEL_FORMAT_R10G10B10A2 = 8
    PIXEL_FORMAT_B10G10R10X2 = 9
    PIXEL_FORMAT_B10G10R10A2 = 10
    PIXEL_FORMAT_R10G10B10A2_XR_BIAS = 11
    PIXEL_FORMAT_R16G16B16X16F = 12
    PIXEL_FORMAT_R16G16B16A16F = 13
    PIXEL_FORMAT_MAX = 14
    PIXEL_FORMAT_NV12YUV420 = 15
    PIXEL_FORMAT_YUV422 = 16
    PIXEL_FORMAT_P010YUV420 = 17
    PIXEL_FORMAT_P012YUV420 = 18
    PIXEL_FORMAT_P016YUV420 = 19
    PIXEL_FORMAT_YUV444_10 = 20
    PIXEL_FORMAT_YUV422_10 = 21
    PIXEL_FORMAT_YUV422_12 = 22
    PIXEL_FORMAT_YUV422_16 = 23
    PIXEL_FORMAT_YUV444_8 = 24
    PIXEL_FORMAT_YUV444_12 = 25
    PIXEL_FORMAT_YUV444_16 = 26
    PIXEL_FORMAT_MAX_PIXELFORMAT = 27


##
# @brief        SB_PIXELFORMAT class
class SB_PIXELFORMAT(object):
    SB_UNINITIALIZED = 0
    SB_8BPP_INDEXED = 1
    SB_B5G6R5X0 = 2
    SB_B8G8R8X8 = 3
    SB_B8G8R8A8 = 4
    SB_R8G8B8X8 = 5
    SB_R8G8B8A8 = 6
    SB_R10G10B10X2 = 7
    SB_R10G10B10A2 = 8
    SB_B10G10R10X2 = 9
    SB_B10G10R10A2 = 10
    SB_R10G10B10A2_XR_BIAS = 11
    SB_R16G16B16X16F = 12
    SB_R16G16B16A16F = 13
    SB_MAX_PIXELFORMAT = 14
    SB_NV12YUV420 = 15
    SB_YUV422 = 16
    SB_P010YUV420 = 17
    SB_P012YUV420 = 18
    SB_P016YUV420 = 19
    SB_YUV444_10 = 20
    SB_YUV422_10 = 21
    SB_YUV422_12 = 22
    SB_YUV422_16 = 23
    SB_YUV444_8 = 24
    SB_YUV444_12 = 25
    SB_YUV444_16 = 26
    SB_MAXALL_PIXELFORMAT = 27


##
# @brief        SURFACE_MEMORY_TYPE class
class SURFACE_MEMORY_TYPE(object):
    SURFACE_MEMORY_INVALID = 0
    SURFACE_MEMORY_LINEAR = 1
    SURFACE_MEMORY_X_TILED = 2
    SURFACE_MEMORY_Y_LEGACY_TILED = 4
    SURFACE_MEMORY_Y_F_TILED = 8
    SURFACE_MEMORY_TILE4 = 16


##
# @brief        MPO_PLANE_ORIENTATION class
class MPO_PLANE_ORIENTATION(object):
    MPO_ORIENTATION_DEFAULT = 1
    MPO_ORIENTATION_90 = 2
    MPO_ORIENTATION_180 = 3
    MPO_ORIENTATION_270 = 4


##
# @brief        MPO_COLOR_SPACE_TYPE class
class MPO_COLOR_SPACE_TYPE(object):
    MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709 = 0
    MPO_COLOR_SPACE_RGB_FULL_G10_NONE_P709 = 1
    MPO_COLOR_SPACE_RGB_STUDIO_G22_NONE_P709 = 2
    MPO_COLOR_SPACE_RGB_STUDIO_G22_NONE_P2020 = 3
    MPO_COLOR_SPACE_RESERVED = 4
    MPO_COLOR_SPACE_YCBCR_FULL_G22_NONE_P709_X601 = 5
    MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P601 = 6
    MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P601 = 7
    MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709 = 8
    MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P709 = 9
    MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P2020 = 10
    MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P2020 = 11
    MPO_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020 = 12
    MPO_COLOR_SPACE_YCBCR_STUDIO_G2084_LEFT_P2020 = 13
    MPO_COLOR_SPACE_RGB_STUDIO_G2084_NONE_P2020 = 14
    MPO_COLOR_SPACE_YCBCR_STUDIO_G22_TOPLEFT_P2020 = 15
    MPO_COLOR_SPACE_YCBCR_STUDIO_G2084_TOPLEFT_P2020 = 16
    MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P2020 = 17
    MPO_COLOR_SPACE_CUSTOM = 0xFFFFFFFF

##
# @brief        FLIP_DURATION class
class FLIP_DURATION(object):
    VRR = 0xFFFFFFFF
    # Eg : for 48Hz call duration_from_rr(48)
    duration_from_rr = lambda rr:10**6//rr
##
# @brief        PLANES_ERROR_CODE class
class PLANES_ERROR_CODE(object):
    PLANES_SUCCESS = 0
    PLANES_FAILURE = 1
    PLANES_RESOURCE_CREATION_FAILURE = 2


##
# @brief        MPO_RECT Structure
class MPO_RECT(ctypes.Structure):
    _fields_ = [('lLeft', ctypes.c_long),
                ('lTop', ctypes.c_long),
                ('lRight', ctypes.c_long),
                ('lBottom', ctypes.c_long)]

    ##
    # @brief        constructor
    def __init__(self):
        self.lLeft = 0
        self.lTop = 0
        self.lRight = 0
        self.lBottom = 0

    ##
    # @brief        constructor
    # @param[in]    lleft - origin X co-ordinate
    # @param[in]    ltop - origin Y co-ordinate
    # @param[in]    lright - horizontal width co-ordinate
    # @param[in]    lbottom - vertical height co-ordinate
    def __init__(self, lleft, ltop, lright, lbottom):
        self.lLeft = lleft
        self.lTop = ltop
        self.lRight = lright
        self.lBottom = lbottom


##
# @brief        MPO_BLEND_VAL Structure
class MPO_BLEND_VAL(ctypes.Structure):
    _fields_ = [('uiValue', ctypes.c_uint)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.uiValue = 0

    ##
    # @brief        Constructor
    # @param[in]    uiblend_val - blend value
    def __init__(self, uiblend_val):
        self.uiValue = uiblend_val


##
# @brief        MPO_RESOURCE_INFO Structure
class MPO_RESOURCE_INFO(ctypes.Structure):
    _fields_ = [('ullpGmmBlock', ctypes.c_ulonglong),
                ('ullpUserVirtualAddress', ctypes.c_ulonglong),
                ('ullSurfaceSize', ctypes.c_ulonglong),
                ('ulPitch', ctypes.c_ulong)]

    ##
    # @brief    Constructor
    def __init__(self):
        self.ullpGmmBlock = 0
        self.ullpUserVirtualAddress = 0
        self.ullSurfaceSize = 0
        self.ulPitch = 0


##
# @brief        MPO_FLIP_FLAGS Structure
class MPO_FLIP_FLAGS(ctypes.Structure):
    _fields_ = [('uiValue', ctypes.c_uint)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.uiValue = 0

    ##
    # @brief        Constructor
    # @param[in]    uimpo_flag - MPO flag value
    def __init__(self, uimpo_flag):
        self.uiValue = uimpo_flag

##
# @brief        FLIP_MPO_PLANE_INPUT_FLAGS Structure
class FLIP_MPO_PLANE_INPUT_FLAGS():
    ENABLED = 0x1
    FLIPIMMEDIATE = 0x2
    FLIPONNEXTVSYNC = 0x4
    SHAREDPRIMARYTRANSITION = 0x8
    INDEPENDANTFLIPEXCLUSIVE = 0x10
    STEREOFLIP = 0x20
    FLIPIMMEDIATENOTEARING = 0x40


##
# @brief        MPO_PLANE_IN_FLAGS Structure
class MPO_PLANE_IN_FLAGS(ctypes.Structure):
    _fields_ = [('uiValue', ctypes.c_uint)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.uiValue = 1  # Default value as 0x1 (Plane Enable)

    ##
    # @brief        Constructor
    # @param[in]    uimpo_plane_in_flag - MPO plane value
    def __init__(self, uimpo_plane_in_flag):
        self.uiValue = uimpo_plane_in_flag


##
# @brief        MPO_FLIP_DELAY_ARGS Structure
class MPO_FLIP_DELAY_ARGS(ctypes.Structure):
    _fields_ = [('uiWaitForFlipDone', ctypes.c_bool),
                ('uiWaitForScanline', ctypes.c_bool),
                ('uiScanLineToWait', ctypes.c_uint32),
                ('uiScanlineCountOffset', ctypes.c_ulong),
                ('uiFrameCountOffset', ctypes.c_uint64)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.uiWaitForFlipDone = False  # Default value as 0x1 (Wait for Flipdone)
        self.uiWaitForScanline = False
        self.uiScanLineToWait = 0
        self.uiScanlineCountOffset = 0
        self.uiFrameCountOffset = 0

    ##
    # @brief        Constructor
    # @param[in]    uimpo_wait_for_flip_done_flag - Wait for flipDone/Not
    # @param[in]    uiWaitForScanline - Wait For scanline flag
    # @param[in]    uiScanLineToWait - Scanline to wait
    # @param[in]    uiScanlineCountOffset - scanline count offset to read from
    # @param[in]    uiFrameCountOffset - Frame count offset to read
    def __init__(self, uimpo_wait_for_flip_done_flag=False, uiWaitForScanline=False, uiScanLineToWait=0,
                 uiScanlineCountOffset=0, uiFrameCountOffset=0):
        self.uiWaitForFlipDone = uimpo_wait_for_flip_done_flag
        self.uiWaitForScanline = uiWaitForScanline
        self.uiScanLineToWait = uiScanLineToWait
        self.uiScanlineCountOffset = uiScanlineCountOffset
        self.uiFrameCountOffset = uiFrameCountOffset


##
# @brief        PLANE_INFO Structure
# @details      Attributes of the plane
class PLANE_INFO(ctypes.Structure):
    _fields_ = [('iPathIndex', ctypes.c_uint),
                ('uiLayerIndex', ctypes.c_uint),
                ('bEnabled', ctypes.c_bool),
                ('ePixelFormat', ctypes.c_int),
                ('eSurfaceMemType', ctypes.c_int),
                ('stMPOSrcRect', MPO_RECT),
                ('stMPODstRect', MPO_RECT),
                ('stMPOClipRect', MPO_RECT),
                ('stMPODirtyRect', MPO_RECT),
                ('lWidth', ctypes.c_long),
                ('lHeight', ctypes.c_long),
                ('eHWOrientation', ctypes.c_int),
                ('stMPOBlend', MPO_BLEND_VAL),
                ('stResourceInfo', (MPO_RESOURCE_INFO * MAX_RESOURCE)),
                ('iResourceInUse', ctypes.c_uint),
                ('eColorSpace', ctypes.c_uint),
                ('cpDumpFilePath', ctypes.c_char_p),
                ('uiMPOYCbCrFlags', ctypes.c_uint),
                ('stMPOFlipFlags', MPO_FLIP_FLAGS),
                ('stMPOPlaneInFlags', MPO_PLANE_IN_FLAGS),
                ('ulMaxImmediateFlipLine', ctypes.c_ulong)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.iPathIndex = -1
        self.uiLayerIndex = -1
        self.bEnabled = 0
        self.ePixelFormat = getattr(PIXEL_FORMAT, "PIXEL_FORMAT_UNINITIALIZED")
        self.eSurfaceMemType = getattr(SURFACE_MEMORY_TYPE, "SURFACE_MEMORY_INVALID")
        self.stMPOSrcRect = MPO_RECT()
        self.stMPODstRect = MPO_RECT()
        self.stMPOClipRect = MPO_RECT()
        self.stMPODirtyRect = MPO_RECT()
        self.lWidth = 0
        self.lHeight = 0
        self.eHWOrientation = getattr(MPO_PLANE_ORIENTATION, "MPO_ORIENTATION_DEFAULT")
        self.stMPOBlend = MPO_BLEND_VAL()
        self.stResourceInfo = (MPO_RESOURCE_INFO * MAX_RESOURCE)()
        self.iResourceInUse = 0
        self.eColorSpace = 0
        self.cpDumpFilePath = None
        self.uiMPOYCbCrFlags = 0
        self.stMPOFlipFlags = MPO_FLIP_FLAGS()
        self.stMPOPlaneInFlags = MPO_PLANE_IN_FLAGS()
        self.ulMaxImmediateFlipLine = -1


    ##
    # @brief        Constructor
    # @param[in]    ipath_index - path index
    # @param[in]    uilayer_index - layer index
    # @param[in]    benabled - plane enabled flag
    # @param[in]    epixel_format - PIXEL_FORMAT object
    # @param[in]    esurface_mem_type - SURFACE_MEMORY_TYPE object
    # @param[in]    stmpo_src_rect - source MPO_RECT object
    # @param[in]    stmpo_dst_rect - destination MPO_RECT object
    # @param[in]    st_mpo_clip_rect - clipped MPO_RECT object
    # @param[in] st_mpo_dirty_rect - Dirty rectangle MPO_RECT object
    # @param[in]    ehw_orientation - MPO_PLANE_ORIENTATION object
    # @param[in]    stmpo_blend - MPO_BLEND_VAL object
    # @param[in]    ecolor_space - color space value
    # @param[in]    cpdump_file_path - dump file path
    # @param[in]    uimpo_ycbcr_flags - ycbcr flag
    # @param[in]    stmpo_flip_flag - MPO_FLIP_FLAGS object
    # @param[in]    stmpo_plane_in_flag - MPO_PLANE_IN_FLAGS object
    # @param[in]    ulmax_immediate_flipLine - Max Immediate FlipLine
    def __init__(self, ipath_index, uilayer_index, benabled, epixel_format, esurface_mem_type, stmpo_src_rect,
                 stmpo_dst_rect, st_mpo_clip_rect, ehw_orientation, stmpo_blend, ecolor_space=0, cpdump_file_path=None,
                 uimpo_ycbcr_flags=0, stmpo_flip_flag=MPO_FLIP_FLAGS(0), stmpo_plane_in_flag=MPO_PLANE_IN_FLAGS(0),
                 st_mpo_dirty_rect=None, ulmax_immediate_flipLine=-1):
        self.iPathIndex = ipath_index
        self.uiLayerIndex = uilayer_index
        self.bEnabled = benabled
        self.ePixelFormat = epixel_format
        self.eSurfaceMemType = esurface_mem_type
        self.stMPOSrcRect = stmpo_src_rect
        self.stMPODstRect = stmpo_dst_rect
        self.stMPOClipRect = st_mpo_clip_rect
        self.stMPODirtyRect = st_mpo_dirty_rect if st_mpo_dirty_rect else stmpo_src_rect
        self.lWidth = stmpo_src_rect.lRight - stmpo_src_rect.lLeft
        self.lHeight = stmpo_src_rect.lBottom - stmpo_src_rect.lTop
        self.eHWOrientation = ehw_orientation
        self.stMPOBlend = stmpo_blend
        self.stResourceInfo = (MPO_RESOURCE_INFO * MAX_RESOURCE)()
        self.iResourceInUse = 0
        self.eColorSpace = ecolor_space
        self.cpDumpFilePath = None if cpdump_file_path is None else cpdump_file_path.encode()
        self.uiMPOYCbCrFlags = uimpo_ycbcr_flags
        self.stMPOFlipFlags = stmpo_flip_flag
        self.stMPOPlaneInFlags = stmpo_plane_in_flag
        self.ulMaxImmediateFlipLine = ulmax_immediate_flipLine

    ##
    # @brief        Get name of the variable from the value
    # @param[in]    var - class name
    # @param[in]    var_value - class member value
    # @return       str - member object name
    def get_name(self, var, var_value):
        var_list = dir(var)
        value = var_value
        return list(filter(lambda x: value == getattr(var, x), var_list))[0]

    ##
    # @brief       Overridden str method
    # @return      str - String representation of PLANE_INFO class
    def __str__(self):
        return " Path Index: " + str(self.iPathIndex) + \
               " Layer Index: " + str(self.uiLayerIndex) + \
               " Enabled: " + str(self.bEnabled) + \
               " Pixel Format: " + self.get_name(PIXEL_FORMAT, self.ePixelFormat) + \
               " Tile Format: " + self.get_name(SURFACE_MEMORY_TYPE, self.eSurfaceMemType) + \
               " Source Rect: " + (str(self.stMPOSrcRect.lLeft) + "," + str(self.stMPOSrcRect.lTop) + "," + str(
            self.stMPOSrcRect.lRight) + "," + str(self.stMPOSrcRect.lBottom)) + \
               " Destination Rect: " + (str(self.stMPODstRect.lLeft) + "," + str(self.stMPODstRect.lTop) + "," + str(
            self.stMPODstRect.lRight) + "," + str(self.stMPODstRect.lBottom)) + \
               " Clip Rect: " + (str(self.stMPOClipRect.lLeft) + "," + str(self.stMPOClipRect.lTop) + "," + str(
            self.stMPOClipRect.lRight) + "," + str(self.stMPOClipRect.lBottom)) + \
               " Hardware Orientation: " + self.get_name(MPO_PLANE_ORIENTATION, self.eHWOrientation) + \
               " Blend Value: " + str(self.stMPOBlend.uiValue) + " Max Immediate Flipline: " \
               + str(self.ulmaxImmediateFlipLine)


##
# @brief        HDR_INFO Structure
class HDR_INFO(ctypes.Structure):
    _fields_ = [('EOTF', ctypes.c_short),
                ('DisplayPrimariesX', ctypes.c_short * 3),
                ('DisplayPrimariesY', ctypes.c_short * 3),
                ('WhitePointX', ctypes.c_short),
                ('WhitePointY', ctypes.c_short),
                ('MaxLuminance', ctypes.c_ulong),
                ('MinLuminance', ctypes.c_ulong),
                ('MaxCLL', ctypes.c_ulong),
                ('MaxFALL', ctypes.c_ulong)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.EOTF = 0
        self.DisplayPrimariesX[0] = 0
        self.DisplayPrimariesX[1] = 0
        self.DisplayPrimariesX[2] = 0
        self.DisplayPrimariesY[0] = 0
        self.DisplayPrimariesY[1] = 0
        self.DisplayPrimariesY[2] = 0
        self.WhitePointX = 0
        self.WhitePointY = 0
        self.MaxLuminance = 0
        self.MinLuminance = 0
        self.MaxCLL = 0
        self.MaxFALL = 0

    ##
    # @brief        constructor
    # @param[in]    EOTF - EOTF Value
    # @param[in]    DisplayPrimariesX - Display Primaries X list
    # @param[in]    DisplayPrimariesY - Display Primaries Y list
    # @param[in]    WhitePointX - White Point X value
    # @param[in]    WhitePointY - White Point Y value
    # @param[in]    MaxLuminance - Maximum Luminance
    # @param[in]    MinLuminance - Minimum Luminance
    # @param[in]    MaxCLL - Max CLL Value
    # @param[in]    MaxFALL - Max FALL Value
    def __init__(self, EOTF=0, DisplayPrimariesX=[0, 0, 0], DisplayPrimariesY=[0, 0, 0], WhitePointX=0, WhitePointY=0,
                 MaxLuminance=0, MinLuminance=0, MaxCLL=0, MaxFALL=0):
        self.EOTF = EOTF
        self.DisplayPrimariesX[0] = DisplayPrimariesX[0]
        self.DisplayPrimariesX[1] = DisplayPrimariesX[1]
        self.DisplayPrimariesX[2] = DisplayPrimariesX[2]
        self.DisplayPrimariesY[0] = DisplayPrimariesY[0]
        self.DisplayPrimariesY[1] = DisplayPrimariesY[1]
        self.DisplayPrimariesY[2] = DisplayPrimariesY[2]
        self.WhitePointX = WhitePointX
        self.WhitePointY = WhitePointY
        self.MaxLuminance = MaxLuminance
        self.MinLuminance = MinLuminance
        self.MaxCLL = MaxCLL
        self.MaxFALL = MaxFALL


##
# @brief        PLANE Structure
class PLANE(ctypes.Structure):
    _fields_ = [('uiPlaneCount', ctypes.c_uint),
                ('stPlaneInfo', (PLANE_INFO * MAX_PLANES)),
                ('HDRMetadata', HDR_INFO),
                ('ulTargetFlipTime', ctypes.c_ulonglong),
                ('ulDelay', ctypes.c_ulonglong),
                ('uDuration', ctypes.c_uint),
                ('stMpoFlipDelayArgs', (MPO_FLIP_DELAY_ARGS * MAX_PIPES))]

    ##
    # @brief        Constructor
    def __init__(self):
        self.uiPlaneCount = 0
        self.ulTargetFlipTime = 0
        self.ulDelay = 0
        self.uDuration = 0
        self.stMpoFlipDelayArgs = (MPO_FLIP_DELAY_ARGS * MAX_PIPES)()

    ##
    # @brief        Constructor
    # @param[in]    pplanes - PLANE_INFO object list
    # @param[in]    hdrMetadata - HDR_INFO object
    # @param[in]    target_flip_time - Target Flip time
    # @param[in]    duration - Flip duration
    # @param[in]    stMpoFlipDelayArgs - MPO delay args
    def __init__(self, pplanes, hdrMetadata=HDR_INFO(), target_flip_time=0, duration=0,
                 stMpoFlipDelayArgs=None):
        self.uiPlaneCount = len(pplanes)
        self.stPlaneInfo = (PLANE_INFO * MAX_PLANES)(*pplanes)
        self.HDRMetadata = hdrMetadata
        self.ulTargetFlipTime = target_flip_time
        self.uDuration = duration
        self.stMpoFlipDelayArgs = (MPO_FLIP_DELAY_ARGS * MAX_PIPES)(*stMpoFlipDelayArgs) if stMpoFlipDelayArgs \
            else (MPO_FLIP_DELAY_ARGS * MAX_PIPES)()


##
# @brief        MPO_CAPS Structure
class MPO_CAPS(ctypes.Structure):
    _fields_ = [('uiMaxPlanes', ctypes.c_uint),
                ('uiNumCapabilityGroups', ctypes.c_uint)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.uiMaxPlanes = 0
        self.uiNumCapabilityGroups = 0


##
# @brief        MPO_CAPS_ARGS Structure
class MPO_CAPS_ARGS(ctypes.Structure):
    _fields_ = [('ulSourceID', ctypes.c_ulong),
                ('stMPOCaps', MPO_CAPS)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.ulSourceID = -1
        self.stMPOCaps = MPO_CAPS()

    ##
    # @brief        Constructor
    # @param[in]    ulsource_id - source ID
    def __init__(self, ulsource_id):
        self.ulSourceID = ulsource_id
        self.stMPOCaps = MPO_CAPS()


##
# @brief        MPO_CAPS_DDRW Structure
class MPO_CAPS_DDRW(ctypes.Structure):
    _fields_ = [('ulvalue', ctypes.c_ulong)]
    '''
    Bit definitions:
    Rotation                        :1
    RotationWithoutIndependentFlip  :1
    VerticalFlip                    :1
    HorizontalFlip                  :1
    StretchRGB                      :1
    StretchYUV                      :1
    BilinearFilter                  :1
    HighFilter                      :1
    Shared                          :1
    Immediate                       :1
    Plane0ForVirtualModeOnly        :1
    QueuedFlip                      :1
    FlipQSupportParamChange         :1
    FlipQSupportFenceSync           :1
    Reserved                        :18     
    '''

    ##
    # @brief        Constructor
    def __init__(self):
        self.ulvalue = 0


##
# @brief        MPO_CAPS_ARGS_DDRW Structure
class MPO_CAPS_ARGS_DDRW(ctypes.Structure):
    _fields_ = [('VidPnSourceId', ctypes.c_ulong),
                ('MaxPlanes', ctypes.c_ulong),
                ('MaxRgbPlanes', ctypes.c_ulong),
                ('MaxYuvPlanes', ctypes.c_ulong),
                ('OverlayCaps', MPO_CAPS_DDRW),
                ('MaxStretchFactorMultBy100', ctypes.c_ulong),
                ('MaxShrinkFactorPlanarMultBy100', ctypes.c_ulong),
                ('MaxShrinkFactorNonPlanarMultBy100', ctypes.c_ulong),
                ('MaxFlipQueues', ctypes.c_ulong),
                ('MaxFlipQueueDepth', ctypes.c_ulong),
                ('MaxPlaneOffset', ctypes.c_ulong)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.VidPnSourceId = -1
        self.MaxPlanes = 0
        self.MaxRgbPlanes = 0
        self.MaxYuvPlanes = 0
        self.OverlayCaps = MPO_CAPS_DDRW()
        self.MaxStretchFactorMultBy100 = -1
        self.MaxShrinkFactorPlanarMultBy100 = -1
        self.MaxShrinkFactorNonPlanarMultBy100 = -1
        self.MaxFlipQueues = 0
        self.MaxFlipQueueDepth = 0
        self.MaxPlaneOffset = 0

    ##
    # @brief        Constructor
    # @param[in]    vidpnsource_id - source ID
    # @param[in]    pipe_id - pipe ID
    def __init__(self, vidpnsource_id, pipe_id):
        self.VidPnSourceId = vidpnsource_id
        self.MaxPlanes = 0
        self.MaxRgbPlanes = 0
        self.MaxYuvPlanes = 0
        self.OverlayCaps = MPO_CAPS_DDRW()
        self.MaxStretchFactorMultBy100 = -1
        self.MaxShrinkFactorPlanarMultBy100 = -1
        self.MaxShrinkFactorNonPlanarMultBy100 = -1
        self.MaxFlipQueues = 0
        self.MaxFlipQueueDepth = 0
        self.MaxPlaneOffset = 0


##
# @brief        MPO_GROUP_CAPS Structure
class MPO_GROUP_CAPS(ctypes.Structure):
    _fields_ = [('uiMaxPlanes', ctypes.c_uint),
                ('uiMaxStretchFactorNum', ctypes.c_uint),
                ('uiMaxStretchFactorDenm', ctypes.c_uint),
                ('uiMaxShrinkFactorNum', ctypes.c_uint),
                ('uiMaxShrinkFactorDenm', ctypes.c_uint),
                ('uiOverlayFtrCaps', ctypes.c_uint),
                ('uiStereoCaps', ctypes.c_uint)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.uiMaxPlanes = 0
        self.uiMaxStretchFactorNum = 0
        self.uiMaxStretchFactorDenm = 0
        self.uiMaxShrinkFactorNum = 0
        self.uiMaxShrinkFactorDenm = 0
        self.uiOverlayFtrCaps = 0
        self.uiStereoCaps = 0


##
# @brief        MPO_GROUP_CAPS_ARGS Structure
class MPO_GROUP_CAPS_ARGS(ctypes.Structure):
    _fields_ = [('ulSourceID', ctypes.c_ulong),
                ('stMPOGroupCaps', MPO_GROUP_CAPS)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.ulSourceID = -1
        self.stMPOGroupCaps = MPO_GROUP_CAPS()

    ##
    # @brief        Constructor
    # @param[in]    ulsource_id - source ID
    def __init__(self, ulsource_id):
        self.ulSourceID = ulsource_id
        self.stMPOGroupCaps = MPO_GROUP_CAPS()


##
# @brief        MPO class
class MPO(object):

    ##
    # @brief        Constructor
    def __init__(self):

        ## Load MPO C library
        self.mpo_interface = ctypes.cdll.LoadLibrary(
            os.path.join(test_context.TestContext.bin_store(), 'GfxValSim.dll'))
        self.system_utility = system_utility.SystemUtility()
        self.machine_info = SystemInfo()
        self.is_ddrw = self.system_utility.is_ddrw('gfx_0')
        self.driver_info = self.machine_info.get_driver_info(SystemDriverType.GFX)
        self.platform_name = None
        self.os_info = self.machine_info.get_os_info()
        self.gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        self.gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        self.os_flipq_enabled = False
        self.vbi_enable_status = False
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(self.gfx_display_hwinfo)):
            self.platform_name = str(self.gfx_display_hwinfo[i].DisplayAdapterName).upper()
            break

    ##
    # @brief        Enable and disable DFT framework and feature
    # @param[in]	benable  - True to enable DFT, False to disable DFT
    # @param[in]	efeature - To enable a specific feature
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		None
    def enable_disable_mpo_dft(self, benable, efeature, gfx_adapter_index='gfx_0'):
        exec_env = self.system_utility.get_execution_environment_type()
        if exec_env == 'POST_SI_ENV' and benable:
            self.enable_disble_os_flipq(benable)
            self.enable_disable_pci_segment(benable)
            if self.platform_name not in ['ICLLP', 'ICL', 'TGL', 'LKF1', 'JSL', 'DG1', 'RKL']:
                self.enable_disable_kmd_managed_dpt(benable)

            ##
            # Restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.error("Failed to restart display driver")
                raise Exception("Failed to restart display driver")

            time.sleep(2)

        if benable:
            win32api.ShellExecute(None, "open", VBIEnableExe, None, None, win32con.SW_NORMAL)
            logging.info("VBIEnable Exe executed successfully")
            self.vbi_enable_status = True

        driver_version_major_minor = self.driver_info.DriverInfo[0].DriverVersion.split('.')
        self.gfxvalsim_handle = driver_interface.DriverInterface().get_driver_handle()
        if self.gfxvalsim_handle is None:
            logging.error("Failed to get valsim handle")
        self.is_ddrw = self.system_utility.is_ddrw(gfx_adapter_index)
        if self.is_ddrw:
            self.mpo_interface.DDRW_EnableDisableMPOSimulation.argtypes = [ctypes.POINTER(GfxAdapterInfo), HANDLE,
                                                                           ctypes.c_bool]
            self.mpo_interface.DDRW_EnableDisableMPOSimulation.restype = ctypes.c_bool
            self.mpo_interface.DDRW_EnableDisableMPOSimulation(self.gfx_adapter_dict[gfx_adapter_index],
                                                               self.gfxvalsim_handle, benable)
        else:
            self.mpo_interface.mainline_EnableDisableMPODFT.argtypes = [ctypes.POINTER(GfxAdapterInfo), HANDLE,
                                                                        ctypes.c_bool,
                                                                        ctypes.c_int]
            self.mpo_interface.mainline_EnableDisableMPODFT.restype = ctypes.c_bool
            self.mpo_interface.mainline_EnableDisableMPODFT(self.gfx_adapter_dict[gfx_adapter_index],
                                                            self.gfxvalsim_handle,
                                                            benable, efeature)

        if self.vbi_enable_status and not benable:
            status = window_helper.kill_process_by_name('VBIEnable.exe')
            if status:
                logging.info("VBIEnable application is closed")
            else:
                self.fail("VBIEnable application is not closed")
            self.vbi_enable_status = False

        if exec_env == 'POST_SI_ENV' and not benable:
            self.enable_disble_os_flipq(benable)
            self.enable_disable_pci_segment(benable)
            if self.platform_name not in ['ICLLP', 'ICL', 'TGL', 'LKF1', 'JSL', 'DG1', 'RKL', 'ADLS']:
                self.enable_disable_kmd_managed_dpt(benable)

            ##
            # Restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.error("Failed to restart display driver")
                raise Exception("Failed to restart display driver")

        ##
        # Disable Plane0 as without Plane re-ordering there is possibility that Plane0 will remain active
        # while test is not programing anything on Plane0. This can create issues during test execution.
        if benable:
            plane = []
            display_config = DisplayConfiguration()
            current_config = display_config.get_current_display_configuration()

            current_mode = display_config.get_current_mode(current_config.displayPathInfo[0].targetId)
            rect = MPO_RECT(0, 0, current_mode.HzRes, current_mode.VtRes)
            blend = MPO_BLEND_VAL(0)

            no_of_displays = current_config.numberOfDisplays
            for index in range(0, no_of_displays):
                plane0 = PLANE_INFO(index, 0, 0, SB_PIXELFORMAT.SB_B8G8R8A8,
                                    SURFACE_MEMORY_TYPE.SURFACE_MEMORY_TILE4,
                                    rect, rect, rect, MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                    MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709)
                plane.append(plane0)

            pplanes = PLANE(plane)

            resource_creation = self.create_resource(pplanes)
            planes = []
            if resource_creation:
                for plane_index in range(0, pplanes.uiPlaneCount):
                    planes.append(
                        pplanes.stPlaneInfo[plane_index].stResourceInfo[
                            pplanes.stPlaneInfo[plane_index].iResourceInUse])
                    logging.info("GMM Block {} Virtual address {} Surface size {} Pitch {}"
                                 .format(pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                             pplanes.stPlaneInfo[plane_index].iResourceInUse].ullpGmmBlock,
                                         pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                             pplanes.stPlaneInfo[
                                                 plane_index].iResourceInUse].ullpUserVirtualAddress,
                                         pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                             pplanes.stPlaneInfo[plane_index].iResourceInUse].ullSurfaceSize,
                                         pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                             pplanes.stPlaneInfo[plane_index].iResourceInUse].ulPitch))
            else:
                gdhm.report_driver_bug_os(
                    f"{GDHM_FLIP} Failed to create resource"
                )
                raise Exception("Failed to create resource")

            checkmpo_result = self.flipq_check_mpo3(pplanes)

            if checkmpo_result == PLANES_ERROR_CODE.PLANES_SUCCESS:
                ssa_result = self.flipq_set_source_address_mpo3(pplanes)
                if ssa_result == PLANES_ERROR_CODE.PLANES_SUCCESS:
                    logging.info("Successfully disabled Plane 0")
                else:
                    logging.error("Failed to disable Plane 0")

            for plane_index in range(0, pplanes.uiPlaneCount):
                free = self.free_resource(
                    pplanes.stPlaneInfo[plane_index].stResourceInfo[
                        pplanes.stPlaneInfo[plane_index].iResourceInUse])
                if free:
                    logging.info("Successfully freed the resource")
                else:
                    gdhm.report_driver_bug_os(
                        f'{GDHM_FLIP} Failed to free resource'
                    )
                    raise Exception("Failed to free resource")

    ##
    # @brief        Disable and restore OS FlipQ registry value
    # @param[in]	benable  - True to disable FlipQ, False to restore default value
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		None
    def enable_disble_os_flipq(self, benable, gfx_adapter_index='gfx_0'):
        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_adapter_index)

        ##
        # Read the default value of DisplayFeatureControl2 registry
        registry_value, registry_type = \
            registry_access.read(args=ss_reg_args, reg_name="DisplayFeatureControl2")

        if benable:
            if registry_value is not None:
                ##
                # Check if OS FlipQ is enabled and disable for DFT
                if registry_value & (1 << 0):
                    value = registry_value & 0xFFFFFFFE
                    self.os_flipq_enabled = True
                else:
                    return
            else:
                return
        else:
            ##
            # Restore default registry value
            if self.os_flipq_enabled:
                value = registry_value | 0x1
            else:
                return

        ##
        # Modify the registry value to disable and restore OS FlipQ.
        registry_access.write(args=ss_reg_args, reg_name="DisplayFeatureControl2",
                              reg_type=registry_access.RegDataType.DWORD, reg_value=value)
        logging.info(f"{'Disabling' if benable else 'Enabling'} FlipQ in registry")

    ##
    # @brief        To enable and disable KMD managed DPT
    # @param[in]    benable A boolean value to indicate addition or deletion of reg key
    # @param[in]    gfx_adapter_index Adapter index
    # @return       None
    def enable_disable_kmd_managed_dpt(self, benable, gfx_adapter_index='gfx_0'):
        exec_env = self.system_utility.get_execution_environment_type()
        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_adapter_index)
        legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                        reg_path=r"SOFTWARE\Intel")

        if exec_env == 'POST_SI_ENV':
            if benable:
                KmdManagedDPTPages = 0x1

                if registry_access.write(args=legacy_reg_args, reg_name="KmdManagedDPTPages",
                                         reg_type=registry_access.RegDataType.DWORD,
                                         reg_value=KmdManagedDPTPages, sub_key="GMM"):
                    logging.debug("Successfully added KMD Managed DPT reg key")
                else:
                    logging.error("Writing to the KmdManagedDPTPages Registry Failed")
                    raise Exception("Writing to the KmdManagedDPTPages Registry Failed")
                if registry_access.write(args=ss_reg_args, reg_name="KmdManagedDPTPages",
                                         reg_type=registry_access.RegDataType.DWORD,
                                         reg_value=KmdManagedDPTPages, sub_key="GMM"):
                    logging.debug("Added KMD Managed DPT reg key in driver path")
                else:
                    logging.error("Writing to the KmdManagedDPTPages Registry under GMM subkey Failed")
                    raise Exception("Writing to the KmdManagedDPTPages Registry under GMM subkey Failed")
            else:
                if registry_access.delete(args=legacy_reg_args, reg_name="KmdManagedDPTPages",
                                          sub_key="GMM"):
                    logging.debug("Successfully deleted KMD Managed DPT reg key")
                else:
                    logging.error("Deleting the KmdManagedDPTPages Registry Failed")
                    raise Exception("Deleting the KmdManagedDPTPages Registry Failed")
                if registry_access.delete(args=ss_reg_args, reg_name="KmdManagedDPTPages", sub_key="GMM"):
                    logging.debug("Deleted KmdManagedDPTPages reg key in driver path")
                else:
                    logging.error("Deleting the KmdManagedDPTPages Registry under GMM subkey Failed")
                    raise Exception("Deleting the KmdManagedDPTPages Registry under GMM subkey Failed")

    ##
    # @brief        To enable and disable PCI segment addition
    # @param[in]    benable - value to indicate addition or deletion PCI segment
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return       None
    def enable_disable_pci_segment(self, benable, gfx_adapter_index='gfx_0'):
        exec_env = self.system_utility.get_execution_environment_type()
        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_adapter_index)
        legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                        reg_path=r"SOFTWARE\Intel")
        if exec_env == 'POST_SI_ENV':

            if benable:
                NonPciMappedSegmentExtraBytes = 0x10000000

                if registry_access.write(args=legacy_reg_args, reg_name="NonPciMappedSegmentExtraBytes",
                                         reg_type=registry_access.RegDataType.DWORD,
                                         reg_value=NonPciMappedSegmentExtraBytes, sub_key="GMM"):
                    logging.debug("Added Non PCI Segment reg key in GMM path")
                else:
                    logging.error("Writing to the NonPciMappedSegmentExtraBytes Registry Failed")
                    raise Exception("Writing to the NonPciMappedSegmentExtraBytes Registry Failed")
                if registry_access.write(args=ss_reg_args, reg_name="NonPciMappedSegmentExtraBytes",
                                         reg_type=registry_access.RegDataType.DWORD,
                                         reg_value=NonPciMappedSegmentExtraBytes, sub_key="GMM"):
                    logging.debug("Added Non PCI Segment reg key in driver path")
                else:
                    logging.error("Writing to the NonPciMappedSegmentExtraBytes Registry under GMM subkey Failed")
            else:
                if registry_access.delete(args=legacy_reg_args, reg_name="NonPciMappedSegmentExtraBytes",
                                          sub_key="GMM"):
                    logging.debug("Deleted Non PCI Segment reg key in GMM path")
                else:
                    logging.error("Deleting the NonPciMappedSegmentExtraBytes Registry Failed")
                    raise Exception("Deleting the NonPciMappedSegmentExtraBytes Registry Failed")
                if registry_access.delete(args=ss_reg_args, reg_name="NonPciMappedSegmentExtraBytes", sub_key="GMM"):
                    logging.debug("Deleted Non PCI Segment reg key in driver path")
                else:
                    logging.error("Deleting the NonPciMappedSegmentExtraBytes Registry under GMM subkey Failed")
                    raise Exception("Deleting the NonPciMappedSegmentExtraBytes Registry under GMM subkey Failed")

    ##
    # @brief        Check the details of hardware support for multiplane overlays
    # @param[in]	pplanes - Pointer to structure containing the plane info
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		result - 0(Success) if hardware supports the passed plane info,
    #               else 1 for check MPO failure and 2 for resource allocation failure
    def check_mpo(self, pplanes, gfx_adapter_index='gfx_0'):
        result = False
        driver_version_major_minor = self.driver_info.DriverInfo[0].DriverVersion.split('.')
        ##
        # For platform above KBL, RS2 will be on WDD2.2 path
        if self.platform_name not in ['IVB', 'HSW', 'VLV', 'BDW', 'APL', 'CHV', 'SKL', 'BXT'] and \
                self.os_info.BuildNumber > '14393':
            result = self.check_mpo3(pplanes, gfx_adapter_index)
        else:
            self.print_plane_details(pplanes, gfx_adapter_index)
            self.mpo_interface.mainline_CheckForMultiPlaneOverlaySupport.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                                     ctypes.POINTER(PLANE)]
            self.mpo_interface.mainline_CheckForMultiPlaneOverlaySupport.restype = ctypes.c_uint
            result = self.mpo_interface.mainline_CheckForMultiPlaneOverlaySupport(
                self.gfx_adapter_dict[gfx_adapter_index],
                pplanes)
        return result

    ##
    # @brief        Present the multiple surfaces on the screen
    # @param[in]	pplanes - Pointer to structure containing the plane info
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		result - Returns 1 for SSA MPO failure and 2 for resource allocation failure; else 0(Success)
    def set_source_address_mpo(self, pplanes, gfx_adapter_index='gfx_0'):
        result = False
        driver_version_minor = self.driver_info.DriverInfo[0].DriverVersion.split('.')
        ##
        # For platform above KBL, RS2 will be on WDD2.2 path
        if self.platform_name not in ['IVB', 'HSW', 'VLV', 'BDW', 'APL', 'CHV', 'SKL', 'BXT'] and \
                self.os_info.BuildNumber > '14393':
            result = self.set_source_address_mpo3(pplanes, gfx_adapter_index)
        else:
            self.mpo_interface.mainline_SetSourceAddressForMultiPlaneOverlay.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                                         ctypes.POINTER(PLANE)]
            self.mpo_interface.mainline_SetSourceAddressForMultiPlaneOverlay.restype = ctypes.c_uint
            result = self.mpo_interface.mainline_SetSourceAddressForMultiPlaneOverlay(
                self.gfx_adapter_dict[gfx_adapter_index],
                pplanes)

        return result

    ##
    # @brief            Check the basic overlay plane capabilities
    # @param[in]		pmpo_caps_args - Pointer to structure to get MPO caps for specific source id
    # @param[in]        gfx_adapter_index - Graphics Adapter Index
    # @return			result - True if success , False otherwise
    def get_mpo_caps(self, pmpo_caps_args, gfx_adapter_index='gfx_0'):
        result = False
        driver_version_minor = self.driver_info.DriverInfo[0].DriverVersion.split('.')
        self.is_ddrw = self.system_utility.is_ddrw(gfx_adapter_index)
        if self.is_ddrw:
            self.mpo_interface.DDRW_GetMPOCaps.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                           ctypes.POINTER(MPO_CAPS_ARGS_DDRW)]
            self.mpo_interface.DDRW_GetMPOCaps.restype = ctypes.c_uint
            result = self.mpo_interface.DDRW_GetMPOCaps(self.gfx_adapter_dict[gfx_adapter_index], pmpo_caps_args)
        else:
            self.mpo_interface.mainline_GetMPOCaps.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                               ctypes.POINTER(MPO_CAPS_ARGS)]
            self.mpo_interface.mainline_GetMPOCaps.restype = ctypes.c_uint
            result = self.mpo_interface.mainline_GetMPOCaps(self.gfx_adapter_dict[gfx_adapter_index], pmpo_caps_args)
        return result

    ##
    # @brief            Check the group of overlay plane capabilities
    # @param[in]		uigroup_index - group index of the no of capable groups
    # @param[in]		pmpo_group_caps - Pointer to structure to get MPO caps for specific source id and group index
    # @return			result - 0(False) on function failure; else 1(True)
    def get_mpo_group_caps(self, pmpo_group_caps, uigroup_index):
        self.mpo_interface.GetMPOGroupCaps.argtypes = [ctypes.POINTER(MPO_GROUP_CAPS_ARGS)]
        self.mpo_interface.GetMPOGroupCaps.restype = ctypes.c_bool
        result = self.mpo_interface.GetMPOGroupCaps(pmpo_group_caps, uigroup_index)
        return result

    ##
    # @brief        Check the details of hardware support for multiplane overlays
    # @param[in]	pplanes - Pointer to structure containing the plane info
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		result - 0(Success) if hardware supports the passed plane info,
    #               else 1 for check MPO failure and 2 for resource allocation failure
    def check_mpo3(self, pplanes, gfx_adapter_index='gfx_0'):
        result = False
        driver_version_minor = self.driver_info.DriverInfo[0].DriverVersion.split('.')
        self.print_plane_details(pplanes, gfx_adapter_index)
        self.is_ddrw = self.system_utility.is_ddrw(gfx_adapter_index)
        if self.is_ddrw:
            self.mpo_interface.DDRW_CheckForMultiPlaneOverlaySupport3.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                                  ctypes.POINTER(PLANE)]
            self.mpo_interface.DDRW_CheckForMultiPlaneOverlaySupport3.restype = ctypes.c_uint
            result = self.mpo_interface.DDRW_CheckForMultiPlaneOverlaySupport3(self.gfx_adapter_dict[gfx_adapter_index],
                                                                               pplanes)
        else:
            self.mpo_interface.mainline_CheckForMultiPlaneOverlaySupport3.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                                      ctypes.POINTER(PLANE)]
            self.mpo_interface.mainline_CheckForMultiPlaneOverlaySupport3.restype = ctypes.c_uint
            result = self.mpo_interface.mainline_CheckForMultiPlaneOverlaySupport3(
                self.gfx_adapter_dict[gfx_adapter_index], pplanes)
        return result

    ##
    # @brief        Present the multiple surfaces on the screen
    # @param[in]	pplanes Pointer to structure containing the plane info
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		result - 1 for SSA MPO failure and 2 for resource allocation failure; else 0(Success)
    def set_source_address_mpo3(self, pplanes, gfx_adapter_index='gfx_0'):
        result = False
        driver_version_minor = self.driver_info.DriverInfo[0].DriverVersion.split('.')
        self.is_ddrw = self.system_utility.is_ddrw(gfx_adapter_index)
        if self.is_ddrw:
            self.mpo_interface.DDRW_SetSourceAddressForMultiPlaneOverlay3.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                                      ctypes.POINTER(PLANE)]
            self.mpo_interface.DDRW_SetSourceAddressForMultiPlaneOverlay3.restype = ctypes.c_uint
            result = self.mpo_interface.DDRW_SetSourceAddressForMultiPlaneOverlay3(
                self.gfx_adapter_dict[gfx_adapter_index],
                pplanes)
        else:
            self.mpo_interface.mainline_SetSourceAddressForMultiPlaneOverlay3.argtypes = [
                ctypes.POINTER(GfxAdapterInfo),
                ctypes.POINTER(PLANE)]
            self.mpo_interface.mainline_SetSourceAddressForMultiPlaneOverlay3.restype = ctypes.c_uint
            result = self.mpo_interface.mainline_SetSourceAddressForMultiPlaneOverlay3(
                self.gfx_adapter_dict[gfx_adapter_index], pplanes)
        return result

    ##
    # @brief        Enable and disable DFT framework and feature
    # @param[in]	benable - True if DFT is enabled, False otherwise
    # @param[in]	efeature - enable a specific feature
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		None
    def enable_disable_dft_flipq(self, benable, efeature, gfx_adapter_index='gfx_0'):
        exec_env = self.system_utility.get_execution_environment_type()
        if exec_env == 'POST_SI_ENV' and benable:
            self.enable_disble_os_flipq(benable)
            self.enable_disable_pci_segment(benable)
            if self.platform_name not in ['ICLLP', 'ICL', 'TGL', 'LKF1', 'JSL', 'DG1', 'RKL']:
                self.enable_disable_kmd_managed_dpt(benable)

            ##
            # Restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.error("Failed to restart display driver")
                raise Exception("Failed to restart display driver")

            time.sleep(2)
            win32api.ShellExecute(None, "open", VBIEnableExe, None, None, win32con.SW_NORMAL)
            logging.info("VBIEnable Exe executed successfully")

        self.gfxvalsim_handle = driver_interface.DriverInterface().get_driver_handle()
        if self.gfxvalsim_handle is None:
            logging.error("Failed to get valsim handle")
        self.mpo_interface.FlipQEnableDisableMPOSimulation.argtypes = [ctypes.POINTER(GfxAdapterInfo), HANDLE,
                                                                       ctypes.c_bool]
        self.mpo_interface.FlipQEnableDisableMPOSimulation.restype = ctypes.c_bool
        self.mpo_interface.FlipQEnableDisableMPOSimulation(self.gfx_adapter_dict[gfx_adapter_index],
                                                           self.gfxvalsim_handle, benable)

        if exec_env == 'POST_SI_ENV' and not benable:
            status = window_helper.kill_process_by_name('VBIEnable.exe')
            if status:
                logging.info("VBIEnable application is closed")
            else:
                self.fail("VBIEnable application is not closed")
            self.enable_disble_os_flipq(benable)
            self.enable_disable_pci_segment(benable)
            if self.platform_name not in ['ICLLP', 'ICL', 'TGL', 'LKF1', 'JSL', 'DG1', 'RKL', 'ADLS']:
                self.enable_disable_kmd_managed_dpt(benable)

            ##
            # Restart display driver
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.error("Failed to restart display driver")
                raise Exception("Failed to restart display driver")

        ##
        # Disable Plane0 as without Plane re-ordering there is possibility that Plane0 will remain active
        # while test is not programing anything on Plane0. This can create issues during test execution.
        if benable:
            plane = []
            display_config = DisplayConfiguration()
            current_config = display_config.get_current_display_configuration()

            current_mode = display_config.get_current_mode(current_config.displayPathInfo[0].targetId)
            rect = MPO_RECT(0, 0, current_mode.HzRes, current_mode.VtRes)
            blend = MPO_BLEND_VAL(0)

            no_of_displays = current_config.numberOfDisplays
            for index in range(0, no_of_displays):
                plane0 = PLANE_INFO(index, 0, 0, SB_PIXELFORMAT.SB_B8G8R8A8, SURFACE_MEMORY_TYPE.SURFACE_MEMORY_TILE4,
                                    rect, rect, rect, MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                    MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709)
                plane.append(plane0)

            pplanes = PLANE(plane)

            resource_creation = self.create_resource(pplanes)
            planes = []
            if resource_creation:
                for plane_index in range(0, pplanes.uiPlaneCount):
                    planes.append(
                        pplanes.stPlaneInfo[plane_index].stResourceInfo[
                            pplanes.stPlaneInfo[plane_index].iResourceInUse])
                    logging.info("GMM Block {} Virtual address {} Surface size {} Pitch {}"
                                 .format(pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                             pplanes.stPlaneInfo[plane_index].iResourceInUse].ullpGmmBlock,
                                         pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                             pplanes.stPlaneInfo[plane_index].iResourceInUse].ullpUserVirtualAddress,
                                         pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                             pplanes.stPlaneInfo[plane_index].iResourceInUse].ullSurfaceSize,
                                         pplanes.stPlaneInfo[plane_index].stResourceInfo[
                                             pplanes.stPlaneInfo[plane_index].iResourceInUse].ulPitch))
            else:
                gdhm.report_driver_bug_os(
                    f"{GDHM_FLIP} Failed to create resource"
                )
                raise Exception("Failed to create resource")

            checkmpo_result = self.flipq_check_mpo3(pplanes)

            if checkmpo_result == PLANES_ERROR_CODE.PLANES_SUCCESS:
                ssa_result = self.flipq_set_source_address_mpo3(pplanes)
                if ssa_result == PLANES_ERROR_CODE.PLANES_SUCCESS:
                    logging.info("Successfully disabled Plane 0")
                else:
                    logging.error("Failed to disable Plane 0")

            for plane_index in range(0, pplanes.uiPlaneCount):
                free = self.free_resource(
                    pplanes.stPlaneInfo[plane_index].stResourceInfo[pplanes.stPlaneInfo[plane_index].iResourceInUse])
                if free:
                    logging.info("Successfully freed the resource")
                else:
                    gdhm.report_driver_bug_os(
                        f'{GDHM_FLIP} Failed to free resource'
                    )
                    raise Exception("Failed to free resource")

    ##
    # @brief        Check the details of hardware support for multiplane overlays
    # @param[in]	pplanes - Pointer to structure containing the plane info
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		result - 0(Success) if hardware supports the passed plane info,
    #               else 1 for check MPO failure
    def flipq_check_mpo3(self, pplanes, gfx_adapter_index='gfx_0'):
        self.print_plane_details(pplanes, gfx_adapter_index)
        self.mpo_interface.FlipQCheckForMultiPlaneOverlaySupport3.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                              ctypes.POINTER(PLANE)]
        self.mpo_interface.FlipQCheckForMultiPlaneOverlaySupport3.restype = ctypes.c_uint
        result = self.mpo_interface.FlipQCheckForMultiPlaneOverlaySupport3(self.gfx_adapter_dict[gfx_adapter_index],
                                                                           pplanes)
        return result

    ##
    # @brief        Present the multiple surfaces on the screen
    # @param[in]	pplanes - Pointer to structure containing the plane info
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		result - 1 for SSA MPO failure and 0  for Success
    def flipq_set_source_address_mpo3(self, pplanes, gfx_adapter_index='gfx_0'):
        self.mpo_interface.FlipQSetSourceAddressForMultiPlaneOverlay3.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                                  ctypes.POINTER(PLANE)]
        self.mpo_interface.FlipQSetSourceAddressForMultiPlaneOverlay3.restype = ctypes.c_uint
        result = self.mpo_interface.FlipQSetSourceAddressForMultiPlaneOverlay3(
            self.gfx_adapter_dict[gfx_adapter_index], pplanes)
        return result

    ##
    # @brief        Create resource for FlipQ planes
    # @param[in]	pplanes - Pointer to structure containing the plane info
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		result - True for successfully creating the resource and False on failure
    def create_resource(self, pplanes, gfx_adapter_index='gfx_0'):
        self.mpo_interface.FlipQDFTCreateResource.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                              ctypes.POINTER(PLANE)]
        self.mpo_interface.FlipQDFTCreateResource.restype = ctypes.c_bool
        result = self.mpo_interface.FlipQDFTCreateResource(
            self.gfx_adapter_dict[gfx_adapter_index], pplanes)
        return result

    ##
    # @brief        Free resource for FlipQ planes
    # @param[in]	presource - Pointer to structure containing the resource info
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		result - True for successfully freeing the resource and False on failure
    def free_resource(self, presource, gfx_adapter_index='gfx_0'):
        self.mpo_interface.DDRW_DFTFreeResource.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                            ctypes.POINTER(MPO_RESOURCE_INFO)]
        self.mpo_interface.DDRW_DFTFreeResource.restype = ctypes.c_bool
        result = self.mpo_interface.DDRW_DFTFreeResource(
            self.gfx_adapter_dict[gfx_adapter_index], presource)
        return result

    ##
    # @brief        Utility method to print plane details
    # @param[in]	pplanes - Pointer to structure containing the plane info
    # @param[in]    gfx_adapter_index - Graphics Adapter Index
    # @return		None
    def print_plane_details(self, pplanes, gfx_adapter_index):
        logging.info(
            "---------------------------------------------------------------------------------------------------------------------------------------------------")
        for plane_index in range(pplanes.uiPlaneCount):
            logging.info(
                "Flip on Gfx Adpter: %s: %s Src (%s, %s, %s, %s), Dest (%s, %s, %s, %s), DestClip (%s, %s, %s, %s), "
                "Pixel Format = %s, Tile Format = %s, FlipType = %s, DirtyRect (%s, %s, %s, %s)"
                % (gfx_adapter_index.upper(),
                   "Enabled" if pplanes.stPlaneInfo[plane_index].bEnabled else "Disabled",
                   pplanes.stPlaneInfo[plane_index].stMPOSrcRect.lLeft,
                   pplanes.stPlaneInfo[plane_index].stMPOSrcRect.lTop,
                   pplanes.stPlaneInfo[plane_index].stMPOSrcRect.lRight,
                   pplanes.stPlaneInfo[plane_index].stMPOSrcRect.lBottom,
                   pplanes.stPlaneInfo[plane_index].stMPODstRect.lLeft,
                   pplanes.stPlaneInfo[plane_index].stMPODstRect.lTop,
                   pplanes.stPlaneInfo[plane_index].stMPODstRect.lRight,
                   pplanes.stPlaneInfo[plane_index].stMPODstRect.lBottom,
                   pplanes.stPlaneInfo[plane_index].stMPOClipRect.lLeft,
                   pplanes.stPlaneInfo[plane_index].stMPOClipRect.lTop,
                   pplanes.stPlaneInfo[plane_index].stMPOClipRect.lRight,
                   pplanes.stPlaneInfo[plane_index].stMPOClipRect.lBottom,
                   pplanes.stPlaneInfo[plane_index].ePixelFormat,
                   pplanes.stPlaneInfo[plane_index].eSurfaceMemType,
                   "Async" if pplanes.stPlaneInfo[plane_index].stMPOPlaneInFlags.uiValue == 0x2 else "Sync",
                   pplanes.stPlaneInfo[plane_index].stMPODirtyRect.lLeft,
                   pplanes.stPlaneInfo[plane_index].stMPODirtyRect.lTop,
                   pplanes.stPlaneInfo[plane_index].stMPODirtyRect.lRight,
                   pplanes.stPlaneInfo[plane_index].stMPODirtyRect.lBottom
                   )
            )
        logging.info(
            "---------------------------------------------------------------------------------------------------------------------------------------------------")
