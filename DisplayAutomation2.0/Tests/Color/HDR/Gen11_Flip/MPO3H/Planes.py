from Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3args import *


class MPOPlane(object):
    """description of class"""

    def __init__(self, uiLayerIndex, eSBPixelFormat, eSurfaceMemType, MPOSrcRect, MPODstRect, MPOClipRect,
                 eHWOrientation=0, eMPOBlend=0):
        self.planeInfo = PlaneInfo()
        self.planeInfo.uiLayerIndex = uiLayerIndex
        self.planeInfo.eSBPixelFormat = eSBPixelFormat
        self.planeInfo.stSurfaceMemInfo.eSurfaceMemType = eSurfaceMemType
        self.planeInfo.stPlaneAttributes.MPOSrcRect = MPOSrcRect
        self.planeInfo.stPlaneAttributes.MPODstRect = MPODstRect
        self.planeInfo.stPlaneAttributes.MPOClipRect = MPOClipRect
        self.planeInfo.stPlaneAttributes.eHWOrientation = eHWOrientation
        self.planeInfo.stPlaneAttributes.eMPOBlend = eMPOBlend

        # Filling remaing default values
