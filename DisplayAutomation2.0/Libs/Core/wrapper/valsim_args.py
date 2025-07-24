########################################################################################################################
# @file         valsim_args.py
# @brief        Contains wrapper constants, structures and enums calling CDLL exposed APIs
# @author       Pabolu, Chandrakanth, Amit Sau
########################################################################################################################


import ctypes
from enum import Enum, unique, IntEnum

MAX_BUFFER_SIZE = 256
MAX_TEST_MMIO_OFFSETS = 10


##
# @brief        ValSimSink Enum
class ValSimSink(Enum):
    INVALID = 0
    DP = 1
    HDMI = 2
    MAX = 3


##
# @brief        ValSimPort Enum
class ValSimPort(Enum):
    DispNone = -1
    ANALOG = 0
    DVO_A = 1
    DVO_B = 2
    DVO_C = 3
    DVO_D = 4
    LVDS = 5
    DP_E = 6
    HDMI_B = 7
    HDMI_C = 8
    HDMI_D = 9
    DVI = 10
    DP_A = 11
    DP_B = 12
    DP_C = 13
    DP_D = 14
    TPV = 15
    MIPI_A = 16
    MIPI_C = 17
    WIGIG = 18
    DVO_F = 19
    HDMI_F = 20
    DP_F = 21
    DVO_E = 22
    HDMI_E = 23
    DP_G = 24
    DVO_G = 25
    HDMI_G = 26
    DP_H = 27
    DVO_H = 28
    HDMI_H = 29
    DP_I = 30
    DVO_I = 31
    HDMI_I = 32
    HDMI_A = 33
    MAX_PORTS = 34


##
# @brief        PortPhyType Enum
class PortPhyType(Enum):
    NATIVE = 0
    TC = 1
    TBT = 2


##
# @brief        DongleType enum
# @details      Specifies the type of Dongle
class DongleType(IntEnum):
    Default = 0  # Type2Adapter
    Type1Adapter = 1
    Type2Adapter = 2
    DviAdapter = 3
    LsPconAdapter = 4
    Type2Adapter_PS8469 = 5


##
# @brief        GfxPlatform Enum
@unique
class GfxPlatform(Enum):
    IGFX_UNKNOWN = 0
    IGFX_GRANTSDALE_G = 1
    IGFX_ALVISO_G = 2
    IGFX_LAKEPORT_G = 3
    IGFX_CALISTOGA_G = 4
    IGFX_BROADWATER_G = 5
    IGFX_CRESTLINE_G = 6
    IGFX_BEARLAKE_G = 7
    IGFX_CANTIGA_G = 8
    IGFX_CEDARVIEW_G = 9
    IGFX_EAGLELAKE_G = 10
    IGFX_IRONLAKE_G = 11
    IGFX_GT = 12
    IGFX_IVYBRIDGE = 13
    IGFX_HASWELL = 14
    IGFX_VALLEYVIEW = 15
    IGFX_BROADWELL = 16
    IGFX_CHERRYVIEW = 17
    IGFX_SKYLAKE = 18
    IGFX_KABYLAKE = 19
    IGFX_COFFEELAKE = 20
    IGFX_WILLOWVIEW = 21
    IGFX_BROXTON = 22
    IGFX_GEMINILAKE = 23
    IGFX_GLENVIEW = 24
    IGFX_GOLDWATERLAKE = 25
    IGFX_CANNONLAKE = 26
    IGFX_CNX_G = 27
    IGFX_ICELAKE = 28
    IGFX_ICELAKE_LP = 29
    IGFX_LAKEFIELD = 30
    IGFX_JASPERLAKE = 31
    IGFX_LAKEFIELD_R = 32
    IGFX_TIGERLAKE_LP = 33
    IGFX_RYEFIELD = 34
    IGFX_ROCKETLAKE = 35
    IGFX_ALDERLAKE_S = 36
    IGFX_ALDERLAKE_P = 37
    IGFX_DG100 = 1210
    IGFX_TIGERLAKE_HP = 1250
    IGFX_DG2 = 1270
    IGFX_PVC = 1271
    IGFX_METEORLAKE = 1272
    IGFX_WAVE2_5 = 1273
    IGFX_LUNARLAKE = 1274
    IGFX_ARROWLAKE = 1275
    IGFX_ALDERLAKE_N = 1276
    IGFX_PTL = 1300
    IGFX_CLS = 1310
    IGFX_NVL_XE3G = 1340
    IGFX_FCS = 1350
    IGFX_NVL = 1360
    IGFX_NVL_AX = 1365
    IGFX_MAX_PRODUCT = 1366

    IGFX_GENNEXT = 0x7ffffffe
    PRODUCT_FAMILY_FORCE_ULONG = 0x7fffffff


##
# @brief        GfxPchFamily Enum
@unique
class GfxPchFamily(Enum):
    PCH_UNKNOWN = 0
    PCH_IBX = 1  # Ibexpeak
    PCH_CPT = 2  # Cougarpoint=
    PCH_CPTR = 3  # Cougarpoint Refresh=
    PCH_PPT = 4  # Panther Point
    PCH_LPT = 5  # Lynx Point
    PCH_LPTR = 6  # Lynx Point Refresh
    PCH_WPT = 7  # Wildcat point
    PCH_SPT = 8  # Sunrise point
    PCH_KBP = 9  # Kabylake PCH
    PCH_CNP_LP = 10  # Cannonlake LP PCH
    PCH_CNP_H = 11  # Cannonlake Halo PCH
    PCH_ICP_LP = 12  # ICL LP PCH
    PCH_ICP_N = 13  # ICL N PCH
    PCH_ICP_HP = 14  # ICL HP PCH
    PCH_LKF = 15  # LKF PCH
    PCH_TGL_LP = 16  # TGL LP PCH
    PCH_TGL_H = 17  # TGL H PCH
    PCH_CMP_LP = 18  # CML LP PCH
    PCH_CMP_H = 19  # CML Halo PCH
    PCH_CMP_V = 20  # CML V PCH
    PCH_EHL = 21  # MCC (Mule Creek Canyon) IOTG PCH IDs for Elkhart Lake
    PCH_JSP_N = 22  # JSL N PCH Device IDs for JSL+ Rev02
    PCH_ADL_S = 23  # ADL_S PCH
    PCH_ADL_P = 24  # ADL_P PCH
    PCH_ADL_N = 25  # ADL_N PCH
    PCH_MTL = 26  # MTL PCH
    PCH_RPL_S = 27  # RPL_S PCH
    PCH_ARL = 28  # ARL PCH
    PCH_DONT_CARE = 0x7ffffffe  # PCH information not needed post Gen13+ platforms, Need to keep this as +ve number as there are checks for < PCH_UNKNOWN
    PCH_PRODUCT_FAMILY_FORCE_ULONG = 0x7fffffff


##
# @brief        DriverWA Enum
class DriverWa(Enum):
    Wa_None = 0
    # Wa_22010492432 : TGL Display combo PHY DPLL and thunderbolt PLL fractional divider error
    Wa_22010492432 = 1
    # Wa_14010527661 : CoG + PSR xclkfifo not dropping dummy pixel for ODD segment resolution in COG 2x2 or 4x1
    Wa_14010527661 = 2
    # Wa_14013475917 : Vsc_framedone flag not clearing on PSR entry
    Wa_14013475917 = 3
    # Wa_22012278275 : D13ADL PSR2 IO/Fast wake times not matching with programming
    Wa_22012278275 = 4
    # Wa_22012279113 : D13ADL PSR2 No SU seen when start line is 0 and SDP scanline bit is set to 1
    Wa_22012279113 = 5
    # Wa_14014971492 : MSO+PSR2 can result in underflow if vblank is synchronized after hblank to cdclk
    Wa_14014971492 = 6
    # Wa_16012604467 : D13ADL Underrun on Pipe A&B observed when PSR2 disabled in CAPTURE frame and SU in next frame
    Wa_16012604467 = 7
    # Wa_16011303918 : CLONE: RKL: Underflow and screen shift when PSR2 enable/disable during update frames
    Wa_16011303918 = 8
    # Wa_16014451276 : [ADL-P/M] Default setting for all POR BOM - X-granularity as 1-based
    Wa_16014451276 = 9


##
# @brief        SpiEventType Enum
class SpiEventType(IntEnum):
    DD_SPI_NONE = 0
    DD_SPI_CONNECTION_EVENT = 1
    DD_SPI_LINK_LOSS_EVENT = 2  # DP link retraining event, handled by OSL
    DD_SPI_ATR_EVENT = 3
    DD_SPI_PARTIAL_DETECTION_EVENT = 4  # MST CSN
    DD_SPI_CP_EVENT = 5
    DD_SPI_CRC_ERROR_EVENT = 6  # To CRC error in PSR
    DD_SPI_RESOURCE_CHANGE_EVENT = 7  # set by TBT tunnel BW manager
    DD_SPI_PSR_CAPS_CHANGE_EVENT = 8  # Set when PSR caps change from PSR to PSR2 or vice versa
    DD_SPI_MAX_EVENTS = 9


##
# @brief        GmdId Structure
class GmdId(ctypes.Structure):
    _fields_ = [
        ("RevisionID", ctypes.c_uint32, 6),  # 0 to 5
        ("Reserved", ctypes.c_uint32, 8),  # 6 to 13
        ("GmdRelease", ctypes.c_uint32, 8),  # 14 to 21
        ("GmdArch", ctypes.c_uint32, 10),  # 22  to 31
    ]


##
# @brief        GfxGmdId Union
class GfxGmdId(ctypes.Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', GmdId),
        ('Value', ctypes.c_uint32)
    ]


##
# @brief        ValSimPlatformInfo Structure
class ValSimPlatformInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('GfxPlatform', ctypes.c_ulong),
        ('GfxPchFamily', ctypes.c_ulong),
        ('GfxGmdId', GfxGmdId),
    ]


##
# @brief        ValsimPortHpdArgs Structure
class ValsimPortHpdArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('PortNum', ctypes.c_ulong),
        ('AttachorDetach', ctypes.c_ubyte),
        ('PortConnectorInfo', ctypes.c_ubyte),
    ]

##
# @brief        ValsimPortHpdArgs Structure
class ValsimTestMmioData(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('ulMMIOOffset', ctypes.c_ulong),
        ('ulMMIOData', ctypes.c_ulong),
    ]

##
# @brief        ValsimPortHpdArgs Structure
class ValsimTestMmmioInitArgs(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('ulNumRegisters', ctypes.c_ulong),
        ('stMMIOList', ValsimTestMmioData * MAX_TEST_MMIO_OFFSETS),
    ]