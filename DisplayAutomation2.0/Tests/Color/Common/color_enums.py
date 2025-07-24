#################################################################################################
# @file         color_enums.py
# @brief        Contains enums for color_escapes
# @author       Vimalesh D
#################################################################################################
from enum import Enum


class RgbQuantizationRange(Enum):
    DEFAULT = 0
    LIMITED = 1
    FULL = 2


class CscMatrixType(Enum):
    LINEAR_CSC = 0
    NON_LINEAR_CSC = 1


class ColorSpace(Enum):
    RGB = 0
    YUV = 1


class ConversionType(Enum):
    FULL_TO_STUDIO = 0
    STUDIO_TO_FULL = 1
    STUDIO_TO_STUDIO = 2
    FULL_TO_FULL = 3


class YuvSampling(Enum):
    YUV444 = "YUV444"
    YUV422 = "YUV422"
    YUV420 = "YUV420"


class PixelEncoding(Enum):
    RGB = 0
    YUV422 = 1
    YUV444 = 2
    YUV420 = 3
    Y_ONLY = 4
    RAW = 5


class ColorimetryYUV(Enum):
    ITU_R_BT601 = 0
    ITU_R_BT709 = 1
    sYCC_601 = 4
    Adobe_YCC601 = 5
    ITU_R_BT2020_Y_CC_BCC_RC = 6
    ITU_R_BT2020_Y_C_BC_R = 7


class ColorimetryRGB(Enum):
    sRGB = 0
    Widegamut_FixedPoint = 1
    Widegamut_FloatingPoint = 2
    Adobe = 3
    DCIP3 = 4
    CustomColorProfile = 5
    ITU_R_BT2020_RGB = 6


class BlendingMode(object):
    SRGB_NON_LINEAR = 0
    BT2020_NON_LINEAR = 1
    BT2020_LINEAR = 2


class PanelCaps(object):
    SDR_709_RGB = 0
    SDR_709_YUV420 = 1
    SDR_BT2020_RGB = 2
    SDR_BT2020_YUV420 = 3
    HDR_BT2020_RGB = 4
    HDR_BT2020_YUV420 = 5
    HDR_DCIP3_RGB = 6
    HDR_DCIP3_YUV420 = 7


class EdpHDRDPCDOffsets(Enum):
    EDP_HDR_CAPS_BYTE1 = 0x341
    EDP_HDR_TCON_CAP_FOR_AUX_BRIGHTNESS = 0x342
    EDP_HDR_GET_SET_CTRL_PARAMS_BYTE0 = 0x344
    EDP_HDR_CONTENT_LUMINANCE_BYTE0 = 0x346
    EDP_HDR_PANEL_LUMINANCE_OVERRIDE = 0x34A
    EDP_HDR_PANEL_LUMINANCE_OVERRIDE_BYTE0 = 0x34C
    EDP_BRIGHTNESS_NITS_BYTE0_LSB = 0x354
    EDP_BRIGHTNESS_NITS_BYTE1_MSB = 0x355
    EDP_BRIGHTNESS_NITS_BYTE_PER_FRAME_STEPS = 0x356
    EDP_BRIGHTNESS_OPTIMIZATION = 0x358

class DP1p4VscExtSdpDPCDOffset(Enum):
    VSC_EXT_SDP_DPCD = 0x2210


class SamplingMode(Enum):
    RGB = 1
    YUV420 = 2


class aggr_level(Enum):
    AGGR_LEVEL_LOW = 0
    AGGR_LEVEL_MODERATE = 1
    AGGR_LEVEL_HIGH = 2


class ColorMode(Enum):
    SDR = 0
    HDR = 1
    WCG = 2

class IgclColorModel(Enum):
    RGB = 0
    YUV420 = 1
    YUV422 = 2
    YUV444 = 3
