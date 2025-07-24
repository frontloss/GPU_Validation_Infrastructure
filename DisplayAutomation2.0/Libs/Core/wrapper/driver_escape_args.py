########################################################################################################################
# @file         driver_escape_args.py
# @brief        Contains wrapper constants, structures and enums calling CDLL exposed APIs
# @author       Kiran Kumar Lakshmanan, Amit Sau
########################################################################################################################
import ctypes
import re
from enum import Enum

DPCD_BUFFER_SIZE = 512  # buffer size for DPCD read escape call
MAX_STRING_SIZE = 256  # memory size required for platform info strings
EDID_BLOCK_SIZE = 128  # block size for EDID data
WB_EDID_BLOCK_SIZE = 256  # block size for writeback EDID
MAX_EDID_BLOCK = 8  # maximum EDID blocks
MAX_WRITEBACK_DEVICE = 2  # maximum wb devices
MAX_PHYSICAL_PIPES = 4  # Collage max physical pipes
MAX_LUT_DATA = 19652  # Color HW LUT Max lut data
ESC_COLOR_MATRIX_NUM_COEFFICIENTS = 9
ESC_COLOR_MATRIX_NUM_OFFSET = 3


##
# @brief                MiscEscProductFamily enum
class MiscEscProductFamily(Enum):
    UNKNOWN = 0
    GRANTSDALE_G = 1
    ALVISO_G = 2
    LAKEPORT_G = 3
    CALISTOGA_G = 4
    BROADWATER_G = 5
    CRESTLINE_G = 6
    BEARLAKE_G = 7
    CANTIGA_G = 8
    CEDARVIEW_G = 9
    EAGLELAKE_G = 10
    IRONLAKE_G = 11
    GT = 12
    IVYBRIDGE = 13
    HASWELL = 14
    VALLEYVIEW = 15
    BROADWELL = 16
    CHERRYVIEW = 17
    SKYLAKE = 18
    KABYLAKE = 19
    COFFEELAKE = 20
    WILLOWVIEW = 21
    BROXTON = 22
    GEMINILAKE = 23
    GLENVIEW = 24
    GOLDWATERLAKE = 25
    CANNONLAKE = 26
    CNX_G = 27
    ICELAKE = 28
    ICELAKE_LP = 29
    LAKEFIELD = 30
    JASPERLAKE = 31
    TIGERLAKE_LP = 32
    TIGERLAKE_HP = 33
    RYEFIELD = 34
    DG1 = 35
    ROCKETLAKE = 36
    DG2 = 37
    MAX_PRODUCT = 38
    GENNEXT = 0x7ffffffe
    FORCE_ULONG = 0x7fffffff


##
# @brief                 MiscEscPlatformType Enum
class MiscEscPlatformType(Enum):
    NONE = 0
    DESKTOP = 1
    MOBILE = 2
    TABLET = 3
    ALL = 255  # flag used for applying any feature/WA for All platform types


##
# @brief                 MiscEscCpuType Enum
class MiscEscCpuType(Enum):
    UNDEFINED = 0
    CORE_I3 = 1
    CORE_I5 = 2
    CORE_I7 = 3
    PENTIUM = 4
    CELERON = 5
    CORE = 6
    VPRO = 7
    SUPER_SKU = 8
    ATOM = 9
    CORE1 = 10
    CORE2 = 11
    WS = 12
    SERVER = 13
    CORE_I5_I7 = 14
    COREX1_4 = 15
    ULX_PENTIUM = 16
    MB_WORKSTATION = 17
    DT_WORKSTATION = 18
    M3 = 19
    M5 = 20
    M7 = 21
    MEDIA_SERVER = 22  # Added for KBL


##
# @brief                 MiscEscGtType Enum
class MiscEscGtType(Enum):
    GT1 = 0
    GT2 = 1
    GT2_FUSED_TO_GT1 = 2
    GT2_FUSED_TO_GT1_6 = 3
    GTL = 4
    GTM = 5
    GTH = 6
    GT1_5 = 7
    GT1_75 = 8
    GT3 = 9
    GT4 = 10
    GT0 = 11
    GTA = 12
    GTC = 13
    GTX = 14
    GT2_5 = 15
    GT3_5 = 16
    GT0_5 = 17
    UNDEFINED = 18


##
# @brief                 DppHwLutOperation Enum
class DppHwLutOperation(Enum):
    UNKNOWN = 0
    APPLY_LUT = 1
    DISABLE_LUT = 2
    MAX_LUT = 3


##
# @brief                 3DLUTStatus Enum
class Color3DLUTStatus(Enum):
    HW_3DLUT_SUCCESS = 0
    HW_3DLUT_INVALID_PIPE = 1
    HW_3DLUT_INVALID_DATA = 2
    HW_3DLUT_NOT_SUPPORTED_IN_HDR = 3
    HW_3DLUT_INVALID_OPERATION = 4
    HW_3DLUT_UNSUCCESS = 5


##
# @brief                 AviInfoOperation Enum
class AviInfoOperation(Enum):
    GET = 0
    SET = 1
    RESTORE_DEFAULT = 2


##
# @brief                 PixelFormat Enum
class PixelFormat(Enum):
    INDEXED_8BPP = 0
    B5G6R5X0 = 1
    B8G8R8X8 = 2
    R8G8B8X8 = 3
    B10G10R10X2 = 4
    R10G10B10X2 = 5
    R10G10B10X2_XR_BIAS = 6
    R16G16B16X16F = 7
    YUV422_8 = 8
    YUV422_10 = 9
    YUV422_12 = 10
    YUV422_16 = 11
    YUV444_8 = 12
    YUV444_10 = 13
    YUV444_12 = 14
    YUV444_16 = 15
    NV12YUV420 = 16
    P010YUV420 = 17
    P012YUV420 = 18
    P016YUV420 = 19
    MAX_PIXELFORMAT = 20


##
# @brief                 SurfaceMemoryType Enum
class SurfaceMemoryType(Enum):
    INVALID = 0
    LINEAR = 1  # Surface uses linear memory
    TILED = 2  # Surface uses tiled memory
    X_TILED = TILED
    Y_LEGACY_TILED = 4  # Surface uses Legacy Y tiled memory (Gen9+)
    Y_F_TILED = 8  # Surface uses Y F tiled memory


##
# @brief                 WbOperationMode Enum
class WbOperationMode(Enum):
    OS_MODE = 0
    DFT_MODE = 1


##
# @brief         VrrOperation Enum
class VrrOperation(Enum):
    GET_INFO = 0  # Get details of VRR support and current status
    ENABLE = 1  # Enable VRR
    DISABLE = 2  # Disable VRR
    LOW_FPS_ENABLE = 3  # Enable Low FPS VRR
    LOW_FPS_DISABLE = 4  # Disable Low FPS VRR
    HIGH_FPS_ENABLE = 5  # Enable High FPS VRR -> Async Flip Enabling
    HIGH_FPS_DISABLE = 6  # Disable High FPS VRR


##
# @brief         CappedFpsState Enum
class CappedFpsState(Enum):
    DISABLE = 0  # Disable RRC_ASYNC_FLIPS
    ENABLE = 1  # Enable RRC_ASYNC_FLIPS
    AUTO = 2  # Auto RRC_ASYNC_FLIPS based on Plan and Power source


##
# @brief         CappedFpsOpcode Enum
class CappedFpsOpcode(Enum):
    GET_CAPPED_FPS = 0
    SET_CAPPED_FPS = 1


##
# @brief         ScalingOperation Enum
class ScalingOperation(Enum):
    GET_NN_SCALING_STATE = 0  # get NN scaling state
    SET_NN_SCALING_STATE = 1  # Set NN scaling state


##
# @brief         NNScalingState Enum
class NNScalingState(Enum):
    NN_SCALING_DISABLE = 0  # Disable NN Scaling
    NN_SCALING_ENABLE = 1  # Enable NN Scaling
    FORCE_INTEGER_SCALING_ENABLE = 2  # Force Integer Scaling


##
# @brief         CollageOperation Enum
class CollageOperation(Enum):
    GET_COLLAGE = 0
    VALIDATE_COLLAGE = 1
    ENABLE_COLLAGE = 2
    DISABLE_COLLAGE = 3
    BEZEL_UPDATE_COLLAGE = 4
    UNKNOWN = 5


##
# @brief         CollageType Enum
class CollageType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    COLLAGE_2_X_2 = 2


##
# @brief         IGCCSupportedEncoding Enum
# @details       This class contains enum variables for IGCC supported encoding
class IGCCSupportedEncoding(Enum):
    NOTSUPPORTED = 0
    DEFAULT = 1
    RGB = 2
    YCBCR420 = 4
    YCBCR422 = 8
    YCBCR444 = 16


##
# @brief         IGCCSupportedBpc Enum
# @details       This class contains enum variables for IGCC supported bpc
class IGCCSupportedBpc(Enum):
    NOTSUPPORTED = 0
    BPCDEFAULT = 1
    BPC6 = 2
    BPC8 = 4
    BPC10 = 8
    BPC12 = 16


##
# @brief         AviEncodingMode Enum
class AviEncodingMode(Enum):
    RGB = 0
    YCBCR422 = 1
    YCBCR444 = 2
    YCBCR420 = 3
    FUTURE = 4


##
# @brief         CuiEscOperationType Enum
class CuiEscOperationType(Enum):
    UNKNOWN = 0
    GET = 1
    SET = 2
    SET_PERSISTENCE = 3
    NUM_OF_CUI_OPTYPE = 4


##
# @brief        IgccEscOverrideOperation Enum
class IgccEscOverrideOperation(Enum):
    GET = 0
    SET = 1


##
# @brief         PwrSrcEventArgs Enum
class PwrSrcEventArgs(Enum):
    PWR_UNKNOWN = 0
    PWR_AC = 1
    PWR_DC = 2


##
# @brief        LinearCscOperation Enum
class LinearCscOperation(Enum):
    GET = 0
    SET = 1


##
# @brief         PwrConsUserPowerPlan Enum
class ColorModel(Enum):
    COLOR_MODEL_UNINITIALIZED = 0
    COLOR_MODEL_RGB = 1
    COLOR_MODEL_YCBCR_601 = 2
    COLOR_MODEL_YCBCR_709 = 3
    COLOR_MODEL_YCBCR_2020 = 4
    COLOR_MODEL_YCBCR_PREFERRED = 5
    COLOR_MODEL_SCRGB = 6
    COLOR_MODEL_INTENSITY_ONLY = 7
    COLOR_MODEL_CUSTOM = 8
    COLOR_MODEL_MAX = 9


##
# @brief        PwrConsUserPowerPlan ENum
class PwrConsUserPowerPlan(Enum):
    PWRCONS_PLAN_CURRENT = 0  # Current user power plan if get operation
    PWRCONS_PLAN_BEST_POWER_SAVINGS = 1  # PC ignores other input parameters, adjust for enabled features only
    PWRCONS_PLAN_BETTER_POWER_SAVINGS = 2  # PC ignores other input parameters, adjust for enabled features only
    PWRCONS_PLAN_GOOD_POWER_SAVINGS = 3  # PC ignores other input parameters, adjust for enabled features only
    PWRCONS_PLAN_DISABLE_POWER_SAVINGS = 4  # PC ignores other input parameters, disables all power savings features
    PWRCONS_PLAN_CUSTOM = 5  # PC uses all input parameters for power savings adjustment
    NUM_OF_PWRCONS_USER_PLANS = 6


##
# @brief         PwrConsOperation Enum
class PwrConsOperation(Enum):
    PWRCONS_OP_UNKNOWN = 0  # Invalid operation
    PWRCONS_OP_FEATURE_SETTINGS = 1  # User Feature Setting operation
    PWRCONS_OP_BACKLIGHT_SETTINGS = 2  # User BackLight Setting operation
    PWRCONS_OP_POWER_PLAN_SETTINGS = 3  # User Power Plan Setting operation
    PWRCONS_OP_TURBO_SETTINGS = 4  # Turbo Settings
    PWRCONS_OP_TURBO_OC_SETTINGS = 5  # Turbo Over-clocking Settings
    PWRCONS_OP_ALS_SETTINGS = 6  # ALS lux value from CUI for assertive display and LACE
    NUM_OF_PWRCONS_OPERATION = 7


##
# @brief         PwrConsOperationStatus Enum
class PwrConsOperationStatus(Enum):
    OPERATION_STATUS_UNKNOWN = 0  # Unknown return status
    OPERATION_STATUS_SUCCESS = 1  # Success
    OPERATION_STATUS_FAILURE = 2  # Failure
    OPERATION_INVALID_PARAMETERS = 3  # Invalid Parameters
    OPERATION_STATUS_INVALID_INVERTER_TYPE = 4  # Invalid Inverter Type, BackLight OP
    OPERATION_STATUS_INVALID_PWM_FREQUENCY = 5  # Invalid PWM Frequency, BackLight OP
    OPERATION_STATUS_NOT_SUPPORTED = 6  # Operation not supported under system configuration


##
# @brief         MiscEscOsInfo Structure
class MiscEscOsInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('wddmVer', ctypes.c_ulong),  # OS version (hexadecimal)
                ('vmsSupport',
                 ctypes.c_ubyte)]  # Virtual mode set support reported by driver to OS in query adapter ( Win10 )


##
# @brief         MiscEscDvmtMemSize Structure
class MiscEscDvmtMemSize(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('minVidMemSize', ctypes.c_ulong),  # Mini Memory Size( Pre-allocated/Fixed Size )
                ('maxVidMemSize', ctypes.c_ulong),  # Max  Memory Size( Possible Video Memory size )
                ('inUseVidMemSize', ctypes.c_ulong),  # Committed Video Memory Size
                ('systemMemTotal', ctypes.c_ulong)]


##
# @brief         MiscEscPlatformInfo Structure
class MiscEscPlatformInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('productFamily', ctypes.c_int),
                ('platformType', ctypes.c_int),
                ('cpuType', ctypes.c_int),
                ('deviceID', ctypes.c_ulong),
                ('gtType', ctypes.c_int),
                ('revID', ctypes.c_ushort),
                ('adapterString', ctypes.c_wchar * MAX_STRING_SIZE),
                ('chipTypeString', ctypes.c_wchar * MAX_STRING_SIZE),
                ('maxSupportedPipes', ctypes.c_ubyte)]


##
# @brief         MiscEscGetSystemInfoArgs Structure
class MiscEscGetSystemInfoArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('featureList', ctypes.c_ulong),
                ('platformInfo', MiscEscPlatformInfo),
                ('dvmtMemSize', MiscEscDvmtMemSize),
                ('osInfo', MiscEscOsInfo),
                ('gopVersion', ctypes.c_ubyte * 32),
                ('isS0ixCapable', ctypes.c_ubyte),
                ('isHASActive', ctypes.c_ubyte)]

    ##
    # @brief        Get GOP Version
    # @return       string - String representation of gop version
    def get_gop_version(self):
        string = ""
        for i in range(len(self.gopVersion)):
            if re.match(r'[0-9.-:_]', chr(self.gopVersion[i])):
                string += chr(self.gopVersion[i])
        return string


##
# @brief         DppHwLutInfo Structure
class DppHwLutInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('displayID', ctypes.c_ulong),
                ('opType', ctypes.c_int),
                ('depth', ctypes.c_ulong),
                ('lutData', ctypes.c_ubyte * MAX_LUT_DATA),
                ('status', ctypes.c_int)]

    ##
    # @brief        Constructor
    # @param[in]    display_id - Target ID of display
    # @param[in]    op_type - LUT operation Type
    # @param[in]    depth - Color depth
    def __init__(self, display_id, op_type, depth):
        super().__init__()
        self.displayID = display_id
        self.opType = op_type
        self.depth = depth
        self.status = Color3DLUTStatus.HW_3DLUT_INVALID_OPERATION.value

    ##
    # @brief         Helper API to convert LUT data from bin file
    # @param[in]     path - LUT data file path
    # @return        bin_file_exists - True if bin file exists, False otherwise
    def convert_lut_data(self, path):
        bin_file_exists = True
        try:
            with open(path.encode(), 'rb') as fp:
                data = fp.read()
                for index in range(len(data)):
                    self.lutData[index] = data[index]
        except FileNotFoundError:
            bin_file_exists = False
        return bin_file_exists


##
# @brief         CSCPipeMatrixParams Structure
class CSCPipeMatrixParams(ctypes.Structure):
    _fields_ = [('bEnable', ctypes.c_int),
                ('coefficients', ctypes.c_int * ESC_COLOR_MATRIX_NUM_COEFFICIENTS),
                ('pre_offsets', ctypes.c_int * ESC_COLOR_MATRIX_NUM_OFFSET),
                ('post_offsets', ctypes.c_int * ESC_COLOR_MATRIX_NUM_OFFSET)]

    ##
    # @brief        Constructor
    def __init__(self):
        self.bEnable = 0

    ##
    # @brief        Constructor
    # @param[in]    enable - enable True to enable CSC, False otherwise
    # @param[in]    coeff - Coefficient Value
    def __init__(self, enable, coeff):
        self.bEnable = enable
        for index in range(0, 9):
            self.coefficients[index] = coeff[index]
        for index in range(0, 3):
            self.pre_offsets[index] = 0
        for index in range(0, 3):
            self.post_offsets[index] = 0


##
# @brief         VrrInfo Structure
class VrrInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('targetId', ctypes.c_ulong),
        ('minRr', ctypes.c_ulong),
        ('maxRr', ctypes.c_ulong)
    ]


##
# @brief         VrrArgs Structure
class VrrArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('operation', ctypes.c_int),
        ('vrrSupported', ctypes.c_bool),
        ('vrrEnabled', ctypes.c_bool),
        ('vrrHighFpsSolnEnabled', ctypes.c_bool),
        ('vrrLowFpsSolnEnabled', ctypes.c_bool),
        ('numDisplays', ctypes.c_ulong),
        ('escVrrInfo', VrrInfo * 8)
    ]


##
# @brief         Region2D Structure
class Region2D(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('cX', ctypes.c_ulong),
        ('cY', ctypes.c_ulong)
    ]

    ##
    # @brief        Constructor
    # @param[in]    res_x - X coordinate
    # @param[in]    res_y - Y coordinate
    def __init__(self, res_x, res_y):
        self.cX = res_x
        self.cY = res_y


##
# @brief         Guid Structure
class Guid(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Data1', ctypes.c_ulong),
        ('Data2', ctypes.c_ushort),
        ('Data3', ctypes.c_ushort),
        ('Data4', ctypes.c_ubyte * 8)
    ]


##
# @brief         ItContentCaps Structure
class ItContentCaps(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('GraphicsContent', ctypes.c_ubyte),
        ('PhotoContent', ctypes.c_ubyte),
        ('CinemaContent', ctypes.c_ubyte),
        ('GameContent', ctypes.c_ubyte)
    ]


##
# @brief         AviInfoFrameCustom Structure
class AviInfoFrameCustom(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Guid', Guid),
        ('Command', ctypes.c_ulong),
        ('Flags', ctypes.c_ulong),
        ('TypeCode', ctypes.c_ulong),
        ('Length', ctypes.c_ulong),
        ('ITContent', ctypes.c_ubyte),
        ('BarInfo', ctypes.c_ubyte * 8),
        ('AspectRatio', ctypes.c_ulong),
        ('QuantRange', ctypes.c_ulong),
        ('ScanInfo', ctypes.c_ulong),
        ('ITContentType', ctypes.c_ulong),
        ('ITContentCaps', ItContentCaps)
    ]


##
# @brief         AVIInfoFrameArgs Structure
class AviInfoFrameArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('TargetID', ctypes.c_ulong),
        ('Operation', ctypes.c_int),
        ('AVIInfoFrame', AviInfoFrameCustom)
    ]


##
# @brief         WritebackHpd Structure
class WritebackHpd(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('hotPlug', ctypes.c_ubyte),
        ('deviceID', ctypes.c_ulong),
        ('resolution', Region2D),
        ('wbSurfaceHandle', ctypes.c_void_p),
        ('notifyScreenCaptureEvent', ctypes.c_void_p),
        ('overrideDefaultEdid', ctypes.c_ubyte),
        ('edidData', ctypes.c_ubyte * WB_EDID_BLOCK_SIZE)
    ]

    ##
    # @brief        Constructor
    # @param[in]    is_hotplug - True to detect HPD for Plug, False for unplug
    # @param[in]    device_id - Target ID
    # @param[in]    res_x - X Coordinate
    # @param[in]    res_y - Y Coordinate
    # @param[in]    override_default_edid - True to override default EDID data, False otherwise
    def __init__(self, is_hotplug, device_id, res_x, res_y, override_default_edid):
        self.hotPlug = is_hotplug
        self.deviceID = device_id
        self.resolution = Region2D(res_x, res_y)
        self.wbSurfaceHandle = None
        self.notifyScreenCaptureEvent = None
        self.overrideDefaultEdid = override_default_edid


##
# @brief         WbBufferInfo Structure
class WbBufferInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('resolution', Region2D),
        ('pixelFormat', ctypes.c_int),
        ('memoryFormat', ctypes.c_int)
    ]

    ##
    # @brief        Constructor
    def __init__(self):
        self.resolution = Region2D(0, 0)
        self.pixelFormat = 0
        self.memoryFormat = 0


##
# @brief         WbQueryArgs Structure
class WbQueryArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('isWbFeatureEnabled', ctypes.c_ubyte),
        ('wbPluggedIn', ctypes.c_ubyte * MAX_WRITEBACK_DEVICE),
        ('deviceID', ctypes.c_ulong * MAX_WRITEBACK_DEVICE),
        ('currentResolution', Region2D * MAX_WRITEBACK_DEVICE),
        ('maxResolution', Region2D),
        ('operationMode', ctypes.c_int)
    ]


##
# @brief         CappedFpsArgs Structure
class CappedFpsArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('opCode', ctypes.c_int),
        ('cappedFpsState', ctypes.c_int),
        ('cappedFpsSupport', ctypes.c_bool)
    ]


##
# @brief         NNScalingSupport Structure
class NNScalingSupport(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('isNNScalingSupport', ctypes.c_bool),
        ('forceIntegerScalingSupport', ctypes.c_bool)
    ]

    ##
    # @brief        Constructor
    def __init__(self):
        super().__init__()
        self.isNNScalingSupport = False
        self.forceIntegerScalingSupport = False


##
# @brief         NNArgs Structure
class NNArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('opCode', ctypes.c_int),
        ('NNScalingState', ctypes.c_int),
        ('NNScalingSupport', NNScalingSupport)
    ]

    ##
    # @brief        Constructor
    def __init__(self):
        super().__init__()
        self.opCode = ScalingOperation.GET_NN_SCALING_STATE.value
        self.NNScalingState = NNScalingState.NN_SCALING_DISABLE.value
        self.NNScalingSupport = NNScalingSupport()


##
# @brief         BezelSize Structure
class BezelSize(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('topBezelSize', ctypes.c_ubyte),
        ('bottomBezelSize', ctypes.c_ubyte),
        ('rightBezelSize', ctypes.c_ubyte),
        ('leftBezelSize', ctypes.c_ubyte)
    ]

    ##
    # @brief        Constructor
    # @param[in]    top_bezel - Top bezel Size
    # @param[in]    bottom_bezel - bottom bezel Size
    # @param[in]    right_bezel - right bezel Size
    # @param[in]    left_bezel - left bezel Size
    def __init__(self, top_bezel, bottom_bezel, right_bezel, left_bezel):
        super().__init__()
        self.topBezelSize = top_bezel
        self.bottomBezelSize = bottom_bezel
        self.rightBezelSize = right_bezel
        self.leftBezelSize = left_bezel

    ##
    # @brief        Overridden str method
    # @return       bazel_size_str - String representation of BezelSize class
    def __str__(self):
        bezel_size_str = "Bezel Size:\n"
        bezel_size_str += "\t TopBezelsize: " + str(self.topBezelSize) + "\n"
        bezel_size_str += "\t BottomBezelsize: " + str(self.bottomBezelSize) + "\n"
        bezel_size_str += "\t RightBezelsize: " + str(self.rightBezelSize) + "\n"
        bezel_size_str += "\t LeftBezelsize: " + str(self.leftBezelSize) + "\n"

        return bezel_size_str


##
# @brief         CollageBezelInfo Union
class CollageBezelInfo(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ('tileBezelInformation', ctypes.c_ulong),
        ('bezelSize', BezelSize)
    ]

    ##
    # @brief        Constructor
    # @param[in]    tile_bezel_info - BezelSize object value
    # @param[in]    bezel_size - BezelSize object
    def __init__(self, tile_bezel_info=0, bezel_size=BezelSize(0, 0, 0, 0)):
        super().__init__()
        self.tileBezelInformation = tile_bezel_info
        self.bezelSize = bezel_size

    ##
    # @brief        Overridden str method
    # @return       bezel_info_str - String representation of CollageBezelInfo class
    def __str__(self):
        bezel_info_str = "BezelInformation:\n"
        bezel_info_str += "\t TileBezelInformation: " + str(self.tileBezelInformation) + "\n"
        bezel_info_str += "\t BezelSize: " + self.bezelSize.__str__()

        return bezel_info_str


##
# @brief         CollageTileInfo Structure
class CollageTileInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('childID', ctypes.c_ulong),
        ('hTileLocation', ctypes.c_ubyte),
        ('vTileLocation', ctypes.c_ubyte),
        ('tileBezelInfo', CollageBezelInfo)
    ]

    ##
    # @brief        Constructor
    # @param[in]    child_id - Child Instance ID
    # @param[in]    h_tile_location - Horizontal Tile Location
    # @param[in]    v_tile_location - Vertical Tile Location
    # @param[in]    bezel_info - CollageBezelInfo object
    def __init__(self, child_id, h_tile_location, v_tile_location, bezel_info=CollageBezelInfo()):
        super().__init__()
        self.childID = child_id
        self.hTileLocation = h_tile_location
        self.vTileLocation = v_tile_location
        self.tileBezelInfo = bezel_info

    ##
    # @brief        Overridden str method
    # @return       collage_tile_info_str - String representation of CollageTileInfo class
    def __str__(self):
        collage_tile_info_str = ""
        collage_tile_info_str += "ChildId: " + str(self.childID) + "\n"
        collage_tile_info_str += "HTileLocation: " + str(self.hTileLocation) + "\n"
        collage_tile_info_str += "VTileLocation: " + str(self.vTileLocation) + "\n"
        collage_tile_info_str += self.tileBezelInfo.__str__() + "\n"

        return collage_tile_info_str


##
# @brief         CollageTopology Structure
class CollageTopology(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('totalNumberOfHTiles', ctypes.c_ubyte),
        ('totalNumberOfVTiles', ctypes.c_ubyte),
        ('collageChildInfo', CollageTileInfo * MAX_PHYSICAL_PIPES),
    ]

    ##
    # @brief        Constructor
    # @param[in]    total_no_of_h_tiles - Total number of Horizontal Tiles
    # @param[in]    total_no_of_v_tiles - Total number of Vertical Tiles
    # @param[in]    child_info_list - Child collage info list
    def __init__(self, total_no_of_h_tiles=0, total_no_of_v_tiles=0, child_info_list=None):
        super().__init__()
        self.totalNumberOfHTiles = total_no_of_h_tiles
        self.totalNumberOfVTiles = total_no_of_v_tiles

        if child_info_list is None:
            child_info_list = []

        for child_index, child_info in enumerate(child_info_list):
            self.collageChildInfo[child_index] = child_info

    ##
    # @brief         Overridden str method
    # @return        collage_topology_str - String representation of CollageTopology class
    def __str__(self):
        collage_topology_str = ""
        collage_topology_str += "TotalNumberOfHTiles: " + str(self.totalNumberOfHTiles) + "\n"
        collage_topology_str += "TotalNumberOfVTiles: " + str(self.totalNumberOfVTiles) + "\n\n"
        for child_index in range(MAX_PHYSICAL_PIPES):
            collage_topology_str += "CollageChildInfo[" + str(child_index) + "]:" + "\n"
            collage_topology_str += self.collageChildInfo[child_index].__str__() + "\n"

        return collage_topology_str


##
# @brief         CollageModeArgs Structure
class CollageModeArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('operation', ctypes.c_int),
        ('collageTopology', CollageTopology),
        ('collageSupported', ctypes.c_bool),
        ('collageConfigPossible', ctypes.c_bool)
    ]

    ##
    # @brief        Constructor
    # @param[in]    operation - Collage operation
    # @param[in]    c_topology - CollageTopology object
    # @param[in]    collage_supported - True if collage supported, False otherwise
    # @param[in]    collage_config_possible - True if Collage configuration is possible, False otherwise
    def __init__(self, operation, c_topology=CollageTopology(), collage_supported=False, collage_config_possible=False):
        super().__init__()
        self.operation = operation
        self.collageTopology = c_topology
        self.collageSupported = collage_supported
        self.collageConfigPossible = collage_config_possible

    ##
    # @brief        Overridden str method
    # @return       get_set_collage_mode_args_str - String representation of CollageModeArgs class
    def __str__(self):
        get_set_collage_mode_args_str = ""
        get_set_collage_mode_args_str += "Collage Operation: " + CollageOperation(self.operation).name + "\n"
        get_set_collage_mode_args_str += "CollageSupported: " + str(self.collageSupported) + "\n"
        get_set_collage_mode_args_str += "CollageConfigPossible: " + str(self.collageConfigPossible) + "\n"
        get_set_collage_mode_args_str += self.collageTopology.__str__()

        return get_set_collage_mode_args_str


##
# @brief         CuiDeepColorInfo Structure
class CuiDeepColorInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('opType', ctypes.c_int),
                ('display_id', ctypes.c_int),
                ('overrideBpcValue', ctypes.c_int),
                ('supportedBpcMask', ctypes.c_int),
                ('overrideEncodingFormat', ctypes.c_int),
                ('supportedEncodingMask', ctypes.c_int),
                ('reserved', ctypes.c_ulong)]


##
# @brief         CustomScalingState Enum
class CustomScalingState(Enum):
    CUSTOM_SCALING_DISABLE = 0  # Disable Custom Scaling
    CUSTOM_SCALING_ENABLE = 1  # Enable Custom Scaling


##
# @brief         CustomScalingOperation Enum
class CustomScalingOperation(Enum):
    GET_STATE = 1  # get Custom scaling state
    SET_STATE = 0  # Set Custom scaling state


##
# @brief         CustomScalingArgs Structure
class CustomScalingArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('getScaling', ctypes.c_ubyte),
        ('target_id', ctypes.c_ulong),
        ('scalingSupported', ctypes.c_ubyte),
        ('scalingEnabled', ctypes.c_ubyte),
        ('customScalingX', ctypes.c_ubyte),
        ('customScalingY', ctypes.c_ubyte)
    ]

    ##
    # @brief        Constructor
    # @param[in]    xPercent - X percent scaling
    # @param[in]    yPercent - Y percent scaling
    # @param[in]    target_id Target id of the display
    # @param[in]    get Scaling operation
    def __init__(self, xPercent, yPercent, target_id=None, get=0):
        super().__init__()
        self.target_id = target_id
        self.getScaling = get
        if get == CustomScalingOperation.SET_STATE.value:
            self.customScalingX = xPercent
            self.customScalingY = yPercent
            self.scalingEnabled = CustomScalingState.CUSTOM_SCALING_ENABLE.value


##
# @brief         PwrConsFeatures Structure
class PwrConsFeatures(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Reserved', ctypes.c_uint16, 1),
        ('Dpst', ctypes.c_uint16, 1),  # DPST
        ('Lace', ctypes.c_uint16, 1),  # LACE
        ('Cxsr', ctypes.c_uint16, 1),  # Rapid Memory Management
        ('Fbc', ctypes.c_uint16, 1),  # Smart 2D
        ('Gsv', ctypes.c_uint16, 1),  # Graphics P States
        ('Dps', ctypes.c_uint16, 1),  # DRRS
        ('Rs', ctypes.c_uint16, 1),  # Graphics Render Standby
        ('Psr', ctypes.c_uint16, 1),  # Panel PSR
        ('Ips', ctypes.c_uint16, 1),  # Intermediate Pixel Storage
        ('Ss', ctypes.c_uint16, 1),  # Slice ShutDown
        ('Dfps', ctypes.c_uint16, 1),  # Dynamic FPS
        ('Adt', ctypes.c_uint16, 1),  # Assertive Display
        ('Pvqc', ctypes.c_uint16, 1),  # ARC (Adaptive Rendering Control), a.k.a PVQC
        ('Dcc', ctypes.c_uint16, 1),  # Duty Cycle Control
        ('Slpm', ctypes.c_uint16, 1)  # Single-loop Power Management
    ]


##
# @brief         PwrConsFeaturePolicyFields Structure
class PwrConsFeaturePolicyFields(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Enabled', PwrConsFeatures),
        ('Supported', PwrConsFeatures)
    ]


##
# @brief         PwrConsFeaturePolicyParams Structure
class PwrConsFeaturePolicyParams(ctypes.Union):
    _anonymous_ = ("PwrConsFeaturePolicyFields",)
    _fields_ = [
        ('FeaturesPolicy', ctypes.c_uint32),
        ('PwrConsFeaturePolicyFields', PwrConsFeaturePolicyFields)
    ]


##
# @brief         PwrConsFeaturePolicy Structure
class PwrConsFeaturePolicy(ctypes.Structure):
    _anonymous_ = ("PwrConsFeaturePolicyParams",)
    _fields_ = [
        ('FeaturesTiedToPowerPlan', PwrConsFeatures),
        ('PwrConsFeaturePolicyParams', PwrConsFeaturePolicyParams)
    ]


##
# @brief         PwrConsGfxPState Structure
class PwrConsGfxPState(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('NumOfAvailablePStates', ctypes.c_uint16),
        ('userMaximumPState', ctypes.c_uint16)
    ]


##
# @brief         PwrConsDpstParam Structure
class PwrConsDpstParam(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('NumOfAvailableAggrLevel', ctypes.c_uint32),
        ('UserMaximumAggrLevel', ctypes.c_uint32),
        ('IsEPSMEnabled', ctypes.c_bool),
        ('IsEPSMSupported', ctypes.c_bool)
    ]


##
# @brief         PwrConsDpsParam Structure
class PwrConsDpsParam(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('IsMfd', ctypes.c_bool),  # OUT-set by PC to indicate whether or not MFD panel
        ('IsSupportForStaticDrrs', ctypes.c_bool),
        # OUT-to indicate Static DRRS is supported on seamless-switching platforms
        ('NumOfRefreshRates', ctypes.c_uint32),
        # OUT-to reflect the number of RRs to expose in the minimum drop-down menu
        ('DpsRefreshRate', ctypes.c_uint32),
        # OUT-to reflect list of possible RRs to expose in the minimum drop-down menu
        ('LastUserSelectedModeSetRR', ctypes.c_uint32),  # OUT-to reflect the last user-selected mode set refresh rate
        ('BaseLowRefreshRate', ctypes.c_uint32),  # IN-Last user-selected Base Lo refresh rate
        ('DpsParamsReturnCode', ctypes.c_uint32)
    ]


##
# @brief         PwrConsOpFeatureSettingsParam Structure
class PwrConsOpFeatureSettingsParam(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('PowerSourceType', ctypes.c_int),
        ('Policy', PwrConsFeaturePolicy),
        ('PowerPlan', ctypes.c_int),
        ('DpstParam', PwrConsDpstParam),
        ('GfxPstatesParam', PwrConsGfxPState),
        ('DpsParam', PwrConsDpsParam)
    ]


##
# @brief         PwrConsBackLightInverterType Structure
class PwrConsBackLightInverterType(Enum):
    BACKLIGHT_INVERTER_UNKNOWN = 0,
    BACKLIGHT_INVERTER_I2C = 1,
    BACKLIGHT_INVERTER_PWM = 2,
    NUM_OF_BACKLIGHT_INVERTER_TYPE = 3


##
# @brief        PwrConsOpBackLightParam Structure
# @details      Back light operation parameters definition
class PwrConsOpBackLightParam(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('InverterType', ctypes.c_int),
        ('PwmInverterFrequency', ctypes.c_uint32)
    ]


##
# @brief        PwrConsOpPowerPlanParam Structure
class PwrConsOpPowerPlanParam(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('UserPowerPlan', ctypes.c_int),
        ('Policy', PwrConsFeaturePolicy),
        ('DpstParam', PwrConsDpstParam),
        ('GfxPstatesParam', PwrConsGfxPState),
        ('DpsParam', PwrConsDpsParam)
    ]


##
# @brief          PwrConsOpTurboParam Structure
# @details        PC operation turbo settings data ctypes.Structure definition
class PwrConsOpTurboParam(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('IsTurboSupported', ctypes.c_bool),
        ('TurboEnabled', ctypes.c_bool),
        ('GfxInTurboState', ctypes.c_bool),
        ('Bias', ctypes.c_uint32)
    ]


##
# @brief          PwrConsOpTurboOcParam Structure
# @details        PC operation turbo OverClocking settings data ctypes.Structure definition
class PwrConsOpTurboOcParam(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('IsTurboOcSupported', ctypes.c_bool),
        ('OcMaxFrequency', ctypes.c_uint32),
        ('OcMaxVoltageOffset', ctypes.c_uint32),
        ('OcMinFrequency', ctypes.c_uint32),
        ('TurboOcEnabled', ctypes.c_bool),
        ('OcFrequency', ctypes.c_uint32),
        ('OcVoltageOffset', ctypes.c_uint32)
    ]


##
# @brief         PwrConsOpAmbientLightParamFields Structure
class PwrConsOpAmbientLightParamFields(ctypes.Structure):
    _fields_ = [
        ('LuxOperation', ctypes.c_uint16, 1),
        ('AggressivenessLevelOperation', ctypes.c_uint16, 1),
        ('Reserved', ctypes.c_uint16, 14)
    ]


##
# @brief         PwrConsOpAmbientLightParam Union
class PwrConsOpAmbientLightParam(ctypes.Union):
    _anonymous_ = ("PwrConsOpAmbientLightParamFields",)
    _fields_ = [
        ('AlsOperation', ctypes.c_uint16),
        ('PwrConsOpAmbientLightParamFields', PwrConsOpAmbientLightParamFields)
    ]


##
# @brief         PwrConsOpAmbientLight Structure
class PwrConsOpAmbientLight(ctypes.Structure):
    _anonymous_ = ("PwrConsOpAmbientLightParam",)
    _fields_ = [
        ('Lux', ctypes.c_uint32),
        ('Kelvin', ctypes.c_uint32),
        ('DefaultAggressivenessLevel', ctypes.c_uint),
        ('AggressivenessLevelFromCUI', ctypes.c_uint),
        ('PwrConsOpAmbientLightParam', PwrConsOpAmbientLightParam)
    ]


##
# @brief         PwrConsOpParameters Union
class PwrConsOpParameters(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ('FeatureSettingsParam', PwrConsOpFeatureSettingsParam),
        ('BackLightParam', PwrConsOpBackLightParam),
        ('PowerPlanParam', PwrConsOpPowerPlanParam),
        ('TurboParam', PwrConsOpTurboParam),
        ('TurboOcParam', PwrConsOpTurboOcParam),
        ('AmbientLightParam', PwrConsOpAmbientLightParam)
    ]


##
# @brief         ComEscPowerConservationArgs Structure
class ComEscPowerConservationArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('OldVersion', ctypes.c_bool),
        ('OpType', ctypes.c_int),
        ('PowerSourceType', ctypes.c_int),
        ('Operation', ctypes.c_int),
        ('OpStatus', ctypes.c_int),
        ('OpParameters', PwrConsOpParameters)
    ]


##
# @brief         DdTimingInfo Structure
class DdTimingInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('dotClock', ctypes.c_uint32),
        ('hTotal', ctypes.c_uint32),
        ('hActive', ctypes.c_uint32),
        ('hRefresh', ctypes.c_uint32),
        ('vTotal', ctypes.c_uint32),
        ('vActive', ctypes.c_uint32),
        ('vRoundedRR', ctypes.c_uint32),
        ('isInterlaced', ctypes.c_bool),
        ('flags', ctypes.c_ubyte * 13),
        ('modeId', ctypes.c_uint32)
    ]


##
# @brief         CapiTiming Structure
class CapiTiming(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('PixelClock', ctypes.c_uint64),
        ('HActive', ctypes.c_uint32),
        ('VActive', ctypes.c_uint32),
        ('HTotal', ctypes.c_uint32),
        ('VTotal', ctypes.c_uint32),
        ('HBlank', ctypes.c_uint32),
        ('VBlank', ctypes.c_uint32),
        ('HSync', ctypes.c_uint32),
        ('VSync', ctypes.c_uint32),
        ('RefreshRate', ctypes.c_float),
        ('SignalStandard', ctypes.c_uint32),
        ('VicId', ctypes.c_uint8)
    ]


# Genlock escape structures

##
# @brief         DdCapiEscGenlockOperation Structure
class DdCapiEscGenlockOperation(Enum):
    DD_CAPI_ESC_GENLOCK_OPERATION_GET_TIMING_DETAILS = 0  # Get details of GENLOCK support and timing information
    DD_CAPI_ESC_GENLOCK_OPERATION_VALIDATE = 1  # Driver to verify that the topology is Genlock capable
    DD_CAPI_ESC_GENLOCK_OPERATION_ENABLE = 2  # Enable GENLOCK
    DD_CAPI_ESC_GENLOCK_OPERATION_DISABLE = 3  # Disable GENLOCK
    DD_CAPI_ESC_GENLOCK_OPERATION_GET_TOPOLOGY = 4  # Get details of the current Genlock topology that is applied


##
# @brief         DdCapiEscGenlockDisplayInfo Structure
class DdCapiEscGenlockDisplayInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('TargetId', ctypes.c_uint32),
        ('IsMaster', ctypes.c_bool),
        ('VBlankTimeStamp', ctypes.c_uint64),
        ('LinkRateMbps', ctypes.c_uint32),
        ('DpLaneWidthSelection', ctypes.c_ubyte)
    ]


##
# @brief         DdGenlockTargetModeList Structure
class DdGenlockTargetModeList(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('TargetId', ctypes.c_uint32),
        ('NumModes', ctypes.c_uint32),
        ('pTargetModes', ctypes.POINTER(CapiTiming))
    ]


##
# @brief         DdGenlockDisplayTopology Structure
class DdGenlockDisplayTopology(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('NumGenlockDisplays', ctypes.c_ubyte),
        ('IsMasterGenlockSystem', ctypes.c_bool),
        ('CommonTargetModeTiming', CapiTiming),
        ('GenlockDisplayInfo', DdCapiEscGenlockDisplayInfo * MAX_PHYSICAL_PIPES),
        ('GenlockModeList', DdGenlockTargetModeList * MAX_PHYSICAL_PIPES)
    ]


##
# @brief         DdCapiEscGetSetGenlockArgs Structure
class DdCapiEscGetSetGenlockArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Operation', ctypes.c_uint32),
        ('GenlockTopology', DdGenlockDisplayTopology),
        ('IsGenlockSupported', ctypes.c_bool),
        ('IsGenlockEnabled', ctypes.c_bool),
        ('IsGenlockPossible', ctypes.c_bool),
        ('LdaAdapterIndex', ctypes.c_uint32)
    ]


##
# @brief         DdCapiGetVblankTimestampForTarget Structure
class DdCapiGetVblankTimestampForTarget(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('TargetID', ctypes.c_uint32),
        ('NumOfTargets', ctypes.c_uint8),
        ('VblankTS', ctypes.c_uint64)
    ]


##
# @brief         CustomModeOperation Enum
class CustomModeOperation(Enum):
    CUSTOM_MODE_GET_MODES = 0
    CUSTOM_MODE_ADD_MODES = 1
    CUSTOM_MODE_REMOVE_MODES = 2


##
# @brief         CustomModeErrorCodes Enum
class CustomModeErrorCodes(Enum):
    CUSTOM_MODE_NO_ERROR = 0
    CUSTOM_MODE_INVALID_PARAMETER = 1
    CUSTOM_MODE_STANDARD_MODE_EXISTS = 2
    CUSTOM_MODE_NON_CUSTOM_MATCHING_MODE_EXISTS = 3
    CUSTOM_MODE_INSUFFICIENT_MEMORY = 4
    CUSTOM_MODE_GENERIC_ERROR_CODE = 5


##
# @brief         CustomSourceArgs Structure
class CustomSourceArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('SourceX', ctypes.c_uint32),
        ('SourceY', ctypes.c_uint32)
    ]


##
# @brief         CustomModeArgs Structure
class CustomModeArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('target_id', ctypes.c_uint32),
        ('ModeOperation', ctypes.c_uint),
        ('ModeErrorCode', ctypes.c_uint),
        ('NumOfModes', ctypes.c_ubyte),
        ('XRes', CustomSourceArgs * 3)
    ]
