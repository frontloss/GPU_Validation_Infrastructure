########################################################################################################################
# @file         Planes.py
# @brief        This script contains initialisation function to initialize Mpo3 Arguments
# @author       Shetty, Anjali N
########################################################################################################################
from Tests.MPO.Flip.GEN11.MPO3H.mpo3args import PlaneInfo

##
# @brief    MpoPlane class
class MPOPlane(object):
    """description of class"""

    ##
    # @brief            init function to initialize Mpo3 arguments
    # @param[in]        uiLayerIndex
    # @param[in]        eSBPixelFormat
    # @param[in]        eSurfaceMemType
    # @param[in]        MPOSrcRect
    # @param[in]        MPODstRect
    # @param[in]        MPOClipRect
    # @param[in]        eHWOrientation
    # @param[in]        eMPOBlend
    def __init__(self, uiLayerIndex, eSBPixelFormat, eSurfaceMemType, MPOSrcRect, MPODstRect, MPOClipRect,
                 eHWOrientation=0, eMPOBlend=0):
        self.planeInfo = PlaneInfo()
        self.planeInfo.iLayerIndex = uiLayerIndex
        self.planeInfo.eSBPixelFormat = eSBPixelFormat
        self.planeInfo.eSurfaceMemType = eSurfaceMemType
        self.planeInfo.MPOSrcRect = MPOSrcRect
        self.planeInfo.MPODstRect = MPODstRect
        self.planeInfo.MPOClipRect = MPOClipRect
        self.planeInfo.eHWOrientation = eHWOrientation
        self.planeInfo.stMPOBlend = eMPOBlend

        # Filling remaing default values
