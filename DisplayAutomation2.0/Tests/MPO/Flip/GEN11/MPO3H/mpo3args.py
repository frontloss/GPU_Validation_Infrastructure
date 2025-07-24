########################################################################################################################
# @file         mpo3args.py
# @brief        This script contains structure of different mpo3 arguments
# @author       Shetty, Anjali N
########################################################################################################################
import ctypes

from Tests.MPO.Flip.GEN11.MPO3H import mpo3enums


##
# @brief    RESOURCE_INFO Structure
class RESOURCE_INFO(ctypes.Structure):
    _fields_ = [('pGmmBlock', ctypes.c_ulonglong),
                ('pUserVirtualAddress', ctypes.c_ulonglong),
                ('u64SurfaceSize', ctypes.c_ulonglong),
                ('ulPitch', ctypes.c_ulong)]

    ##
    # @brief    init function to initialize Resource info Class
    def __init__(self):
        self.pGmmBlock = 0
        self.pUserVirtualAddress = 0
        self.u64SurfaceSize = 0
        self.ulPitch = 0


##
# @brief    MPO_BLEND_VAL Structure
class MPO_BLEND_VAL(ctypes.Structure):
    _fields_ = [('uiValue', ctypes.c_uint)]
    '''
    Bit definitions:
    AlphaBlend      : 1
    Reserved        : 31
    '''
    ##
    # @brief    init function to initialize Mpo Blend Val Class
    def __init__(self):
        self.uiValue = 0


##
# @brief    RECT1 Structure
class RECT1(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long),
                ('top', ctypes.c_long),
                ('right', ctypes.c_long),
                ('bottom', ctypes.c_long)]

    ##
    # @brief    init function to initialize Rect1 Class
    def __init__(self):
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

    ##
    # @brief            init function to initialize Rect1 Class
    # @param[in]        left
    # @param[in]        top
    # @param[in]        right
    # @param[in]        bottom
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


##
# @brief    MPO_FLIP_FLAGS Structure
class MPO_FLIP_FLAGS(ctypes.Structure):
    _fields_ = [('uiValue', ctypes.c_uint)]

    ##
    # @brief    init function to initialize Mpo Flip Flags Class
    def __init__(self):
        self.uiValue = 0

    ##
    # @brief            init function to initialize Mpo Flip Flags Class
    # @param[in]        uimpo_flag
    def __init__(self, uimpo_flag):
        self.uiValue = uimpo_flag


##
# @brief    PlaneInfo Structure
class PlaneInfo(ctypes.Structure):
    _fields_ = [('SourceID', ctypes.c_int),
                ('iLayerIndex', ctypes.c_uint),
                ('bEnabled', ctypes.c_int),
                ('eSBPixelFormat', ctypes.c_int),
                ('eSurfaceMemType', ctypes.c_int),
                ('MPOSrcRect', RECT1),
                ('MPODstRect', RECT1),
                ('MPOClipRect', RECT1),
                ('lWidth', ctypes.c_long),
                ('lHeight', ctypes.c_long),
                ('eHWOrientation', ctypes.c_int),  # PLANE_ORIENTATION
                ('stMPOBlend', MPO_BLEND_VAL),
                ('stResourceInfo', (RESOURCE_INFO * 2)),
                ('iResourceUsed', ctypes.c_int),
                ('eColorSpace', ctypes.c_int),
                ('cImageFilePath', ctypes.c_char_p),
                ('cYCbCrFlags', ctypes.c_int),
                ('stMPOFlipFlags', MPO_FLIP_FLAGS)]

    ##
    # @brief    init function to initialize PlaneInfo Class
    def __init__(self):
        self.SourceID = -1
        self.iLayerIndex = -1
        self.bEnabled = 0
        self.eSBPixelFormat = mpo3enums.SB_PIXELFORMAT.SB_UNINITIALIZED
        self.eSurfaceMemType = mpo3enums.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_INVALID
        self.MPOSrcRect = RECT1()
        self.MPODstRect = RECT1()
        self.MPOClipRect = RECT1()
        self.lWidth = 0
        self.lHeight = 0
        self.eHWOrientation = mpo3enums.PLANE_ORIENTATION.ORIENTATION_DEFAULT
        self.stMPOBlend = MPO_BLEND_VAL()
        self.stResourceInfo[0] = RESOURCE_INFO()
        self.stResourceInfo[1] = RESOURCE_INFO()
        self.iResourceUsed = 0
        self.eColorSpace = 0
        self.cImageFilePath = None
        self.cYCbCrFlags = 0

    ##
    # @brief            init function to initialize PlaneInfo Class
    # @param[in]        SourceID
    # @param[in]        iLayerIndex
    # @param[in]        bEnabled
    # @param[in]        eSBPixelFormat
    # @param[in]        eSurfaceMemType
    # @param[in]        MPOSrcRect
    # @param[in]        MPODstRect
    # @param[in]        MPOClipRect
    # @param[in]        eHWOrientation
    # @param[in]        stMPOBlend
    # @param[in]        eColorSpace
    # @param[in]        cFilePath
    # @param[in]        cCSFlags
    def __init__(self, SourceID, iLayerIndex, bEnabled, eSBPixelFormat, eSurfaceMemType, MPOSrcRect, MPODstRect,
                 MPOClipRect, eHWOrientation, stMPOBlend, eColorSpace, cFilePath=None, cCSFlags=0):
        self.SourceID = SourceID
        self.iLayerIndex = iLayerIndex
        self.bEnabled = bEnabled
        self.eSBPixelFormat = eSBPixelFormat
        self.eSurfaceMemType = eSurfaceMemType
        self.MPOSrcRect = MPOSrcRect
        self.MPODstRect = MPODstRect
        self.MPOClipRect = MPOClipRect
        self.eHWOrientation = eHWOrientation
        self.stMPOBlend = stMPOBlend
        self.stResourceInfo[0] = RESOURCE_INFO()
        self.stResourceInfo[1] = RESOURCE_INFO()
        self.eColorSpace = eColorSpace
        self.cImageFilePath = cFilePath
        self.cYCbCrFlags = cCSFlags


##
# @brief    HDRInfo Structure
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

    ##
    # @brief    init function to initialize HDRInfo Class
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
    # @brief            init function to initialize HDRInfo Class
    # @param[in]        EOTF
    # @param[in]        DisplayPrimariesX
    # @param[in]        DisplayPrimariesY
    # @param[in]        WhitePointX
    # @param[in]        WhitePointY
    # @param[in]        MaxLuminance
    # @param[in]        MinLuminance
    # @param[in]        MaxCLL
    # @param[in]        MaxFALL
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


##
# @brief    PLANES Structure
class PLANES(ctypes.Structure):
    _fields_ = [('uiPlaneCount', ctypes.c_uint),
                ('stPlaneInfo', (PlaneInfo * mpo3enums.MAX_PLANES)),
                ('HDRMetadata', HDRInfo)]

    ##
    # @brief    init function to initialize Planes Class
    def __init__(self):
        self.uiPlaneCount = 0

    ##
    # @brief            init function to initialize Planes Class
    # @param[in]        pyPlanes
    # @param[in]        hdrMetadata
    def __init__(self, pyPlanes, hdrMetadata=None):
        self.uiPlaneCount = len(pyPlanes)
        if (hdrMetadata is None):
            hdrMetadata = HDRInfo(0, [0, 0, 0], [0, 0, 0, ], 0, 0, 0, 0, 0, 0)
        self.stPlaneInfo = (PlaneInfo * mpo3enums.MAX_PLANES)(*pyPlanes)
        self.HDRMetadata = hdrMetadata
