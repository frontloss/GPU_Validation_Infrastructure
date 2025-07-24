import ctypes

from Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3enums import PLANE_ORIENTATION, MAX_PLANES, MAX_PIPES
from Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3enums import SB_PIXELFORMAT, SURFACE_MEMORY_TYPE


class RESOURCE_INFO(ctypes.Structure):
    _fields_ = [('pGmmBlock', ctypes.c_ulonglong),
                ('pUserVirtualAddress', ctypes.c_ulonglong),
                ('u64SurfaceSize', ctypes.c_ulonglong),
                ('ulPitch', ctypes.c_ulong)]

    def __init__(self):
        self.pGmmBlock = 0
        self.pUserVirtualAddress = 0
        self.u64SurfaceSize = 0
        self.ulPitch = 0


class MPO_BLEND_VAL(ctypes.Structure):
    _fields_ = [('uiValue', ctypes.c_uint)]
    '''
    Bit definitions:
    AlphaBlend      : 1
    Reserved        : 31
    '''

    def __init__(self):
        self.uiValue = 0


class RECT1(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long),
                ('top', ctypes.c_long),
                ('right', ctypes.c_long),
                ('bottom', ctypes.c_long)]

    def __init__(self):
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


##
# MPO Flip Flags
class MPO_FLIP_FLAGS(ctypes.Structure):
    _fields_ = [('uiValue', ctypes.c_uint)]

    def __init__(self):
        self.uiValue = 0

    def __init__(self, uimpo_flag):
        self.uiValue = uimpo_flag


##
# MPO Plane IN Flags
class MPO_PLANE_IN_FLAGS(ctypes.Structure):
    _fields_ = [('uiValue', ctypes.c_uint)]

    def __init__(self):
        self.uiValue = 1  # Default value as 0x1 (Plane Enable)

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


class PlaneInfo(ctypes.Structure):
    _fields_ = [('SourceID', ctypes.c_int),
                ('iLayerIndex', ctypes.c_uint),
                ('bEnabled', ctypes.c_int),
                ('eSBPixelFormat', ctypes.c_int),
                ('eSurfaceMemType', ctypes.c_int),
                ('MPOSrcRect', RECT1),
                ('MPODstRect', RECT1),
                ('MPOClipRect', RECT1),
                ('MPODirtyRect', RECT1),
                ('lWidth', ctypes.c_long),
                ('lHeight', ctypes.c_long),
                ('eHWOrientation', ctypes.c_int),  # PLANE_ORIENTATION
                ('stMPOBlend', MPO_BLEND_VAL),
                ('stResourceInfo', (RESOURCE_INFO * 2)),
                ('iResourceUsed', ctypes.c_int),
                ('eColorSpace', ctypes.c_int),
                ('cImageFilePath', ctypes.c_char_p),
                ('cYCbCrFlags', ctypes.c_int),
                ('stMPOFlipFlags', MPO_FLIP_FLAGS),
                ('stMPOPlaneInFlags', MPO_PLANE_IN_FLAGS),
                ('ulMaxImmediateFlipLine', ctypes.c_ulong)]

    def __init__(self):
        self.SourceID = -1
        self.iLayerIndex = -1
        self.bEnabled = 0
        self.eSBPixelFormat = SB_PIXELFORMAT.SB_UNINITIALIZED
        self.eSurfaceMemType = SURFACE_MEMORY_TYPE.SURFACE_MEMORY_INVALID
        self.MPOSrcRect = RECT1()
        self.MPODstRect = RECT1()
        self.MPOClipRect = RECT1()
        self.MPODirtyRect = RECT1()
        self.lWidth = 0
        self.lHeight = 0
        self.eHWOrientation = PLANE_ORIENTATION.ORIENTATION_DEFAULT
        self.stMPOBlend = MPO_BLEND_VAL()
        self.stResourceInfo[0] = RESOURCE_INFO()
        self.stResourceInfo[1] = RESOURCE_INFO()
        self.iResourceUsed = 0
        self.eColorSpace = 0
        self.cImageFilePath = None
        self.cYCbCrFlags = 0
        self.ulMaxImmediateFlipLine = -1

    def __init__(self, SourceID, iLayerIndex, bEnabled, eSBPixelFormat, eSurfaceMemType, MPOSrcRect, MPODstRect,
                 MPOClipRect, eHWOrientation, stMPOBlend, eColorSpace, cFilePath=None, cCSFlags=0, MPODirtyRect=None,
                 ulmax_immediate_flipLine=-1):
        self.SourceID = SourceID
        self.iLayerIndex = iLayerIndex
        self.bEnabled = bEnabled
        self.eSBPixelFormat = eSBPixelFormat
        self.eSurfaceMemType = eSurfaceMemType
        self.MPOSrcRect = MPOSrcRect
        self.MPODstRect = MPODstRect
        self.MPOClipRect = MPOClipRect
        self.MPODirtyRect = MPODirtyRect if MPODirtyRect else MPOSrcRect
        self.eHWOrientation = eHWOrientation
        self.stMPOBlend = stMPOBlend
        self.stResourceInfo[0] = RESOURCE_INFO()
        self.stResourceInfo[1] = RESOURCE_INFO()
        self.eColorSpace = eColorSpace
        self.cImageFilePath = cFilePath
        self.cYCbCrFlags = cCSFlags
        self.ulMaxImmediateFlipLine = ulmax_immediate_flipLine


class HDRInfo(ctypes.Structure):
    _fields_ = [('EOTF', ctypes.c_short),
                ('DisplayPrimariesX', ctypes.c_short * 3),
                ('DisplayPrimariesY', ctypes.c_short * 3),
                ('WhitePointX', ctypes.c_short),
                ('WhitePointY', ctypes.c_short),
                ('MaxLuminance', ctypes.c_ulong),
                ('MinLuminance', ctypes.c_ulong),
                ('MaxCLL', ctypes.c_ulong),
                ('MaxFALL', ctypes.c_ulong)]

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

    def __init__(self, EOTF, DisplayPrimariesX, DisplayPrimariesY, WhitePointX, WhitePointY, MaxLuminance, MinLuminance,
                 MaxCLL, MaxFALL):
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


class PLANES(ctypes.Structure):
    _fields_ = [('uiPlaneCount', ctypes.c_uint),
                ('stPlaneInfo', (PlaneInfo * MAX_PLANES)),
                ('HDRMetadata', HDRInfo),
                ('ulTargetFlipTimeInUs', ctypes.c_ulonglong),
                ('ulDelay', ctypes.c_ulonglong),
                ('stMpoFlipDelayArgs', (MPO_FLIP_DELAY_ARGS * MAX_PIPES))]

    def __init__(self):
        self.uiPlaneCount = 0
        self.ulTargetFlipTimeInUs = 0
        self.ulDelay = 0
        self.stMpoFlipDelayArgs = (MPO_FLIP_DELAY_ARGS * MAX_PIPES)()

    def __init__(self, pyPlanes, hdrMetadata=None, stMpoFlipDelayArgs=None):
        self.uiPlaneCount = len(pyPlanes)
        if (hdrMetadata is None):
            hdrMetadata = HDRInfo(0, [0, 0, 0], [0, 0, 0, ], 0, 0, 0, 0, 0, 0)
        self.stPlaneInfo = (PlaneInfo * MAX_PLANES)(*pyPlanes)
        self.HDRMetadata = hdrMetadata
        self.stMpoFlipDelayArgs = (MPO_FLIP_DELAY_ARGS * MAX_PIPES)(*stMpoFlipDelayArgs) if stMpoFlipDelayArgs \
            else (MPO_FLIP_DELAY_ARGS * MAX_PIPES)()
