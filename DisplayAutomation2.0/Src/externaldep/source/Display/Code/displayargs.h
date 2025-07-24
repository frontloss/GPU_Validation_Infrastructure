/*===========================================================================
;
;   Copyright (c) Intel Corporation (2017)
;
;   INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
;   ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
;   INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
;   ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
;   MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
;   OTHER WARRANTY.  Intel disclaims all liability, including liability for
;   infringement of any proprietary rights, relating to use of the code. No license,
;   express or implied, by estoppel or otherwise, to any intellectual property
;   rights is granted herein.
;
;--------------------------------------------------------------------------*/
/**
@file DisplayArgs.h
@brief This file contains definitions for display arguments shared outside of display.(KMD)
*/

#pragma once
#include "DisplayDefs.h"
#include <Chipsimc.h>
#include "DisplayErrorDef.h"
#include "OSDefs.h"
#include <iCP.h>
#include <iHDCP.h>
#include <iHDMI.h>
#include <dispComp.h>
#include <HAS_SIM.H>

#include "DisplaySharedHeader.h"

//#include"..\..\inc\common\MPO.h"
//#include "..\..\inc\common\iMIPI.h"
//#include "..\\..\\inc\\common\\Wpp.h"
#include "..\\..\\..\\..\\externaldep\\source\\inc\\common\\DisplaySharedHeader.h"

//----------------------------------------------------------------------------
//
// Generic CONSTANTS, ENUMS and MACROS - START
//
//----------------------------------------------------------------------------

#define INVALID_SCAN_LINE -1
#define DD_LINEAR_ALIGN 64
#define DD_GOP_PROGRAMMED_START_ADDRESS 0

//#define MAX_PLANES_PER_PIPE_GEN10   4
//#define MAX_PLANES_PER_PIPE_GEN11   5
#define MAX_PLANES_PER_PIPE MAX_PLANES_PER_PIPE_GEN11

typedef enum _DD_ACPI_PORT_TYPE
{
    DD_CRT_TYPE = 1,
    DD_DFP_TYPE = 3,
    DD_LFP_TYPE = 4,
} DD_ACPI_PORT_TYPE;

#define DD_GetDisplayType(Arg) (Arg >> 16)
#define MIPI_CONNECTOR 17
#define DD_IsMIPI(Arg) ((Arg >> 8 & 0x1F) == MIPI_CONNECTOR)
#define HDMI_CONNECTOR 6
#define DD_IsHDMI(Arg) (((Arg >> 8) & 0x1F) == HDMI_CONNECTOR)
#define ExtDP_CONNECTOR 14
#define DD_IsDP(Arg) (((Arg >> 8) & 0x1F) == ExtDP_CONNECTOR)
#define TPV_CONNECTOR 16
#define DD_IsTPV(Arg) 0 //(((Arg >> 8) & 0x1F) == TPV_CONNECTOR)
#define WIGIG_CONNECTOR 19
#define IS_WIGIG_DISPLAY(Arg) (((Arg >> 8) & 0x1F) == WIGIG_CONNECTOR)

#define DD_IS_LFP(TargetId) (((TargetId) & (1 << 23)) > 0)

#define DD_MAX_DP_MST_CONNECTOR_PER_PORT 3                                  // considering 3 MST max TODO: make variable
#define DD_MAX_SINK_CONTEXT_PER_PORT (DD_MAX_DP_MST_CONNECTOR_PER_PORT + 1) // considering dual mode config
#define DD_MAX_TARGET_PER_PORT (DD_MAX_DP_MST_CONNECTOR_PER_PORT + 1)       // considering dual mode config

#define DD_MAX_REGISTRY_PATH_LENGTH 256

#define MAX_ALS_DATA_POINTS 5

// Color related
#define CUI_PREFIX L"CUILut"
#define OS_PREFIX L"OSLut"
#define ABS_PREFIX L"AbsLut"
#define CSC_PREFIX L"RelCSC"
#define MIN_RGB_SCALE 0.3f // This is not a standard value, found after experimenting with OS gamma values
#define MAX_RGB_SCALE 3.0f // This is not a standard value, found after experimenting with OS gamma values
#define DEFAULT_SCALE 1.0f
#define MIN_RGB_OFFSET -100.0f // This is not a standard value, found after experimenting with OS gamma values
#define MAX_RGB_OFFSET 100.0f  // This is not a standard value, found after experimenting with OS gamma values
#define DEFAULT_OFFSET 0

// To encapsulate RS1 specific code, enabled as of today, TBD for disabling
#define RS1 1

typedef enum _DD_LOCK_RES_TYPE
{
    DD_LOCK_TYPE_NONE,
    DD_LOCK_MUTEX,    // for passive level calls
    DD_LOCK_SPINLOCK, // for all IRQLs
    DD_LOCK_TYPE_MAX
} DD_LOCK_RES_TYPE_EN;

typedef struct _DD_LOCKING_OBJ
{
    DD_LOCK_RES_TYPE_EN LockType;
    void *              pLock;
    DDS32               RefCount;
    DDU8                OldIrql;
    BOOLEAN             IsIrqlLevelRaised;
    HANDLE              ThreadID;
    DDU8                NumContendingClients; // debug purpose
} DD_LOCKING_OBJ_ST;

typedef struct _DD_ESCAPE
{
    DDU32 OpCode;
    DDU32 DataSize;
    void *EscapeData;
} DD_ESCAPE;

// PCI related
#define PCI_BUS_0 0
#define PCI_CTL_DEVICE 0
#define PCI_GFX_DEVICE 2
#define DEFAULT_FUNC_NUM 0xFF // Used for PCI calls only on PCI_GFX_DEVICE. Used to signal 'do not care whether the current HWDev is appropriate' during PCI calls.
#define GFX_FUNCTION_0 0x0
#define GFX_FUNCTION_1 0x1
#define PCI_CMD_OFFSET 0x4
#define PCI_COMMAND_REG_MEM_ENABLE_BIT 0x2
/*
typedef struct _GRM_PCI_CFG_DATA
{
    BOOLEAN         DDR3;          // DDR type
    DDU32           CoreFreq;           // GFX/GMCH core frequency in MHz
    DDU32           SystemMemFreq;      // System memory frequency in MHz
    DDU32           NumOfMemChannels;   // Number of memory channels
    DDU32           MaxPipeADotClock;   // Maximum Pipe A dotclock supported
    DDU32           FSBFrequency;       // FSB Frequency in Mhz
    DDU32           RenderFreq;         // GFX Render Clock Frequency
    DDU32           PlatformType;
} GRM_PCI_CFG_DATA;

typedef enum _GRM_STATUS
{
    GRM_OK = 0,
    GRM_FAIL = 1,
}GRM_STATUS;*/

// Lock related
// typedef enum _DD_SERIAL_LOCK_TYPE
//{
//    SERIALIZE_GAL_ACCESS = 1, // to serialize GAL access.
//    SERIALIZE_IOSF_DD_ACCESS = 11 // to serialize access to IOSF register access.Used for both Internal & external access request.
//} DD_SERIAL_LOCK_TYPE;

typedef enum _DD_PORT_TYPE
{
    DD_PORT_TYPE_UNKNOWN = -1,
    DD_PORT_TYPE_DIGITAL_PORT_A,
    DD_PORT_TYPE_DIGITAL_PORT_B,
    DD_PORT_TYPE_DIGITAL_PORT_C,
    DD_PORT_TYPE_DIGITAL_PORT_D,
    DD_PORT_TYPE_DIGITAL_PORT_E,
    DD_PORT_TYPE_DIGITAL_PORT_F,
    DD_PORT_TYPE_DSI_PORT_0,
    DD_PORT_TYPE_DSI_PORT_1,
    DD_PORT_TYPE_WIGIG_PORT,
    DD_PORT_TYPE_VIRTUAL_PORT,
    DD_PORT_TYPE_MAX
} DD_PORT_TYPE;

#define IS_VALID_PORT_TYPE(port) (((DD_PORT_TYPE)port) > DD_PORT_TYPE_UNKNOWN && ((DD_PORT_TYPE)port) < DD_PORT_TYPE_MAX)
#define IS_MIPI_PORT_TYPE(port) ((((DD_PORT_TYPE)port) == DD_PORT_TYPE_DSI_PORT_0) || (((DD_PORT_TYPE)port) == DD_PORT_TYPE_DSI_PORT_1))
// TODO: Add Ftr bit for MST
DD_INLINE BOOLEAN _DDIsPortMstCapable(DD_PORT_TYPE Port)
{
    BOOLEAN IsMST = FALSE;
    switch (Port)
    {
    case DD_PORT_TYPE_DIGITAL_PORT_B:
    case DD_PORT_TYPE_DIGITAL_PORT_C:
    case DD_PORT_TYPE_DIGITAL_PORT_D:
    case DD_PORT_TYPE_DIGITAL_PORT_F:
        IsMST = TRUE;
        break;
    default:
        IsMST = FALSE;
        break;
    }

    return IsMST;
}

typedef enum _DD_PORT_CONNECTOR_TYPE
{
    DD_PORT_CONNECTOR_NORMAL = 0,
    DD_PORT_CONNECTOR_TYPEC,
    DD_PORT_CONNECTOR_TBT,
} DD_PORT_CONNECTOR_TYPE;

typedef enum _DD_PORT_EVENT_TYPE
{
    DD_HOTPLUG_EVENT = 0,
    DD_SCDC_EVENT,
    DD_EVENT_MAX,
} DD_PORT_EVENT_TYPE;

// PixelFormat related Macros start here.
#define DD_PIXELFORMAT_GETMASK(PixelFormat) (1 << PixelFormat)

// Below function will be used when PixelFormatMask contains a single pixel format (only 1 bit set) @rsrivas2
// DD_INLINE DD_PIXELFORMAT DD_GET_PIXELFORMAT_FROM_MASK(DDU32 PixelFormatMask)
//{
//    DD_PIXELFORMAT PixelFormat;
//    for (DDU32 Count = 0; Count < DD_MAX_PIXELFORMAT; Count++)
//    {
//        if (DD_PIXELFORMAT_GETMASK(Count) & PixelFormatMask)
//        {
//            PixelFormat = (DD_PIXELFORMAT)Count;
//            return PixelFormat;
//        }
//    }
//    // this means that we didnt find a matching pixelformat
//    return DD_B8G8R8X8;
//}

#define DD_32_BPP_RGB_PIXELFORMAT_BITMASK                                                                                                                         \
    DD_PIXELFORMAT_GETMASK(DD_B8G8R8X8) | DD_PIXELFORMAT_GETMASK(DD_R8G8B8X8) | DD_PIXELFORMAT_GETMASK(DD_B10G10R10X2) | DD_PIXELFORMAT_GETMASK(DD_R10G10B10X2) | \
    DD_PIXELFORMAT_GETMASK(DD_R10G10B10X2_XR_BIAS)
#define DD_64_BPP_RGB_PIXELFORMAT_BITMASK DD_PIXELFORMAT_GETMASK(DD_R16G16B16X16F)
#define DD_32_64_BPP_RGB_PIXELFORMAT_BITMASK DD_32_BPP_RGB_PIXELFORMAT_BITMASK | DD_64_BPP_RGB_PIXELFORMAT_BITMASK

// DD_INLINE BOOLEAN DD_IS_RGB_PIXELFORMAT(DD_PIXELFORMAT PixelFormat) @rsrivas2
//{
//    BOOLEAN Rgb;
//    switch (PixelFormat)
//    {
//    case DD_8BPP_INDEXED:
//    case DD_B5G6R5X0:
//    case DD_B8G8R8X8:
//    case DD_R8G8B8X8:
//    case DD_B10G10R10X2:
//    case DD_R10G10B10X2:
//    case DD_R10G10B10X2_XR_BIAS:
//    case DD_R16G16B16X16F:
//        Rgb = TRUE;
//        break;
//    default:
//        Rgb = FALSE;
//        break;
//    }
//    return Rgb;
//}

#define DD_IS_YUV_PIXELFORMAT(PixelFormat) !DD_IS_RGB_PIXELFORMAT(PixelFormat)

// DD_INLINE BOOLEAN DD_IS_PLANAR_PIXELFORMAT(DD_PIXELFORMAT PixelFormat) @rsrivas2
//{
//    BOOLEAN PlanarFormat;
//    switch (PixelFormat)
//    {
//    case DD_NV12YUV420:
//    case DD_P010YUV420:
//    case DD_P012YUV420:
//    case DD_P016YUV420:
//        PlanarFormat = TRUE;
//        break;
//    default:
//        PlanarFormat = FALSE;
//        break;
//    }
//    return PlanarFormat;
//}
//
// DD_INLINE DDU8 DD_GetBPPfromPixelFormat(DD_PIXELFORMAT PixelFormat)
//{
//    DDU8 Bpp;
//    switch (PixelFormat)
//    {
//    case DD_8BPP_INDEXED:
//        Bpp = 8;
//        break;
//    case DD_NV12YUV420:
//        Bpp = 12;
//        break;
//    case DD_YUV422:
//    case DD_B5G6R5X0:
//        Bpp = 16;
//        break;
//    case DD_P010YUV420:
//    case DD_P012YUV420:
//    case DD_P016YUV420:
//        Bpp = 24;
//        break;
//    case DD_R16G16B16X16F:
//        Bpp = 64;
//        break;
//    default:
//        Bpp = 32; // default
//        break;
//    }
//    return Bpp;
//}

#define DD_IS_RGB_BPP_PIXELFORMAT(PixelFormat, Bpp) (DD_IS_RGB_PIXELFORMAT(PixelFormat) && (Bpp == DD_GetBPPfromPixelFormat(PixelFormat)))

// Macro to get bpc which could be used for the pipe in HW
// Note: For <= 32bpp case, this has to return 8 always
// This is because effective pipe data is of 8 minimum.
// This helps in back compatibility as well
// DD_INLINE DDU8 DD_GetBitsPerColor(DD_PIXELFORMAT PixelFormat)@rsrivas2
//{
//    DDU8 Bpc;
//
//    switch (PixelFormat)
//    {
//    case DD_R10G10B10X2:
//    case DD_B10G10R10X2:
//    case DD_R10G10B10X2_XR_BIAS:
//    case DD_P010YUV420:
//    case DD_YUV444_10:
//        Bpc = 10;
//        break;
//    case DD_R16G16B16X16F:
//    case DD_P016YUV420:
//        Bpc = 16;
//        break;
//    case DD_YUV422:
//    case DD_NV12YUV420:
//    case DD_8BPP_INDEXED:
//    case DD_B5G6R5X0:
//    case DD_B8G8R8X8:
//    case DD_R8G8B8X8:
//    default:
//        Bpc = 8; // default
//        break;
//    }
//    return Bpc;
//}
// PixelFormat related Macros end here.

typedef union _DD_DISPLAY_FEATURE_CONTROL_FLAGS {
    DDU32 Value;
    struct
    {
        DDU32 YTilingEnabledFlag : 1;           // Bit 0
        DDU32 MpoNv12EnabledFlag : 1;           // Bit 1
        DDU32 RendCompEnabledFlag : 1;          // Bit 2
        DDU32 GtTypeFusedEnabledFlag : 1;       // Bit 3
        DDU32 AllowDc9InMipiDsr : 1;            // Bit 4
        DDU32 MpoEnabledFlag : 1;               // Bit 5
        DDU32 MpoInMultiDisplayEnabledFlag : 1; // Bit 6
        DDU32 MpoYUY2EnabledFlag : 1;           // Bit 7
        DDU32 MpoYUY2ScalingEnabled : 1;        // Bit 8
        DDU32 DispFtrCtrlReserved : 23;         // Bits (9:31)
    };
} DD_DISPLAY_FEATURE_CONTROL_FLAGS;

// Cursor related constants
#define CURSOR_MAX_WIDTH_256_PIXEL (256)
#define CURSOR_MAX_HEIGHT_256_PIXEL (256)

#define MAX_CURSOR_PLANES 4

//----------------------------------------------------------------------------
//
// Generic CONSTANTS, ENUMS and MACROS - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// OPM/UMD Escape used structures -- START
//
//----------------------------------------------------------------------------

typedef struct _DD_GETDISPLAYINFO_ARGS
{
    DD_IN DDU32 Size; // Set to sizeof(DD_GETDISPLAYINFO_ARGS)

    DD_IN DDU32 DisplayUID; // Unique ID or Generic UID e.g DISPLAY_ANY_CRT

    DD_OUT BOOLEAN IsTPVDrivenEncoder; // Introduced for CUI..

    // Display device status information
    // DD_OUT DISPLAY_DEVICE_STATUS stDisplayDeviceStatus;

    // Device capability info
    // DD_OUT DISPLAY_DEVICE_CAPS stDisplayDeviceCaps;

    // Display Device BW related information
    // DD_OUT DD_DISPLAY_BANDWIDTH_INFO stDisplayBandWidthInfo;

    // Tiled display info
    DD_OUT DDU32 TileXRes;
    DD_OUT DDU32 TileYRes;
    DD_OUT DDU8 NoOfHTileDisplays;
    DD_OUT DDU8 NoOfVTileDisplays;

    // Flag Specifying the return of Mode Caps
    // Only GRM will be using this flag in the CSLBASE_GetDisplayInfo ().
    // This will be set by GRM to get the Mode Caps for non-CRT devices.
    // For CRT, GRM will still be getting the Display Caps
    DD_IN BOOLEAN ModeCaps;

    // DD_OUT ENCODER_RR_SWITCHING_CAPS stEncoderRrSwitchingCaps;   //Indicates the refresh-rate switching capabilities of the chipset

    DD_OUT BOOLEAN IsLsPconDonglePresent;

    DD_OUT BOOLEAN IsHDRSupported; // Sink supports HDR SMPTE 2084 EOTF
} DD_GETDISPLAYINFO_ARGS;

// Get Set parameters args structure
typedef struct _DD_GETSETPARAM_ARGS
{
    DD_IN DDU32 DisplayUID; // Unique display ID (cannot accept generic types)
    union {
        DD_IN_OUT HDCP_PARAMETERS HdcpParameters;
        DD_IN_OUT CP_PARAMETERS_T CPParameters;
    };
} DD_GETSETPARAM_ARGS;

typedef struct _DD_PLATFORM_INFO
{
    DDU8    GopVersion[0x20]; // GOP version
    BOOLEAN IsS0ixCapable;
} DD_PLATFORM_INFO;

typedef struct _DD_DISPLAY_INIT_ARG
{
    DD_IN BOOLEAN DodEnabled;
    DD_OUT DDU32 NumberOfVideoPresentSources;
    DD_OUT DDU32 NumberOfChildren;
    DD_OUT DD_PLATFORM_INFO PlatformInfo;
} DD_DISPLAY_INIT_ARG;

typedef struct _DD_OSL_INIT_ARG
{
    DD_IN BOOLEAN DodEnabled;
    DD_OUT DDU32 NumberOfChildren;
} DD_OSL_INIT_ARG;

//----------------------------------------------------------------------------
//
// OPM/UMDEscape used structures -- END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// Header with topology related  definitions - START
//
//----------------------------------------------------------------------------

#define DD_SOURCE_ID_UNINITIALIZED (DDU32) ~0
#define DD_TARGET_ID_UNINITIALIZED (DDU32) ~0
#define MAX_NUM_PATHS 3 // Max number of pipes is 3 hence three paths

// map of legacy SOURCE_MODE_FLAGS
typedef union _DD_SOURCE_MODE_FLAGS {
    DDU32 Flags;
    struct
    {
        unsigned S3DMode : 1;            // Bit Indicating whether the given mode is S3D
        unsigned Collage : 1;            // Bit indicating if given mode is Collage
        unsigned HorCollage : 1;         // bit indicating if given mode is horizontal Collage
        unsigned VerCollage : 1;         // bit indicating if given mode id vertical Collage
        unsigned RGBColorSeparation : 1; // bit indicating color separation support for the given mode
        unsigned TiledMode : 1;          // bit indicating tiled display mode is applicable
        unsigned Reserved : 26;          // Bits 1:27, Reserved
    };
} DD_SOURCE_MODE_FLAGS;

// DD_COPY_PROTECTION_TYPE - Enum Copy protection
typedef enum _DD_COPY_PROTECTION_TYPE
{
    /**Uninitialized */
    DD_CP_UNINITIALIZED = 0,
    /**No Protection */
    DD_CP_NO_PROTECTION = 1,
    /**APS Trigger supported */
    DD_CP_APS_TRIGGER = 2,
    /**Full protection supported*/
    DD_CP_FULL_PROTECTION = 3,
} DD_COPY_PROTECTION_TYPE;

// DD_COPY_PROTECTION - Copy Protection
typedef struct _DD_COPY_PROTECTION
{
    /**Copy protection values updated or not */
    BOOLEAN Updated;
    /**CP Type*/
    DD_COPY_PROTECTION_TYPE CpType;
    /**Asp Trigger Bits */
    DDU32 AspTriggerBits;
    // Place holder for OEM CP size !
} DD_COPY_PROTECTION;

// DD_ROTATION_SUPPORT - Rotation support set
typedef union _DD_ROTATION_SUPPORT {
    struct
    {
        DDU32 Identity : 1;
        DDU32 Rotate90 : 1;
        DDU32 Rotate180 : 1;
        DDU32 Rotate270 : 1;
        DDU32 Offset0 : 1;
        DDU32 Offset90 : 1;
        DDU32 Offset180 : 1;
        DDU32 Offset270 : 1;
        DDU32 Reserved : 24;
    };
    DDU32 RotationSupport;
} DD_ROTATION_SUPPORT;

typedef union _DD_DRIVER_FLAGS {
    struct
    {
        DDU32 PopulateSourceModeSet : 1;
        DDU32 PopulateTargetModeSet : 1;
        DDU32 IndexBasedTargetModeSetAccess : 1;
        DDU32 PopulateScaling : 1;
        DDU32 PopulateRotation : 1;
        DDU32 TargetModePinned : 1;
        DDU32 SourceModePinned : 1;
        DDU32 ReservedFlags : 25;
    };
    DDU32 DriverFlags;
} DD_DRIVER_FLAGS;

typedef union _DD_OS_FLAGS {
    struct
    {
        DDU32 SourceModePinned : 1;
        DDU32 SourcePivot : 1;
        DDU32 TargetModePinned : 1;
        DDU32 TargetPivot : 1;
        DDU32 ScalingPinned : 1;
        DDU32 ScalingPivot : 1;
        DDU32 RotationPinned : 1;
        DDU32 RotationPivot : 1;
        DDU32 ReservedFlags : 24;
    };
    DDU32 OsFlags;
} DD_OS_FLAGS;

typedef enum _DD_SCALING
{
    DD_SCALING_UNINITIALIZED          = 0,
    DD_SCALING_IDENTITY               = 1,
    DD_SCALING_CENTERED               = 2,
    DD_SCALING_STRETCHED              = 4,
    DD_SCALING_ASPECTRATIOCENTEREDMAX = 8,
    DD_SCALING_CUSTOM                 = 16,
    DD_SCALING_UNPINNED               = 254,
    DD_SCALING_UNSPECIFIED            = 255
} DD_SCALING;

/*typedef union _MACROVISIONCAPS
{
    DDU32   Value;
    struct
    {
        DDU32 APSTriggerSupported : 1;    // bit 0
        DDU32 MVFullsupported : 1;    // bit 1
        DDU32 NoProtection : 1;    // bit 2
        DDU32 Reserved : 29;    // bit 3 - 31
    };
}MACROVISIONCAPS;*/

typedef enum _DD_ROTATION_OFFSET
{
    DD_ROT_OFFSET_0   = 1,
    DD_ROT_OFFSET_90  = 2,
    DD_ROT_OFFSET_180 = 3,
    DD_ROT_OFFSET_270 = 4,
} DD_ROTATION_OFFSET;

// enum for values of bInterlacedType
/*aim3 // typedef enum _INTERLACED_TYPE_FLAGS
{
    INTERLACED_LVDS_VSYNC_SHIFT = 0,                    //0 = Interlaced LVDS using vertical sync shift
    INTERLACED_VSYNC_SHIFT,                             //1 = Interlaced using vertical sync shift
    INTERLACED_VSYNC_HSYNC_FIELD_LEGACY_VSYNC_SHIFT,    //2 = Interlaced with VSYNC/HSYNC Field indication
    //using legacy vertical sync shift
    INTERLACED_FIELD0_LEGACY_VSYNC_SHIFT,               //3 = Odd/Even Mode : DVO-C Even, DVO-B Odd
    INTERLACED_SDVO_VSYNC_SHIFT
} INTERLACED_TYPE_FLAGS;

*/

// Timing Info related definitions - END

typedef enum _PLANE_ORIENTATION DD_ROTATION;

#define DD_IS_PORTRAIT_ORIENTATION(PlaneOrientation) ((PlaneOrientation == ORIENTATION_90) || (PlaneOrientation == ORIENTATION_270))

#define DD_IS_LANDSCAPE_ORIENTATION(PlaneOrientation) ((PlaneOrientation == ORIENTATION_0) || (PlaneOrientation == ORIENTATION_180))

typedef struct _DD_SET_TIMING_PATH_FLAGS
{
    union {
        struct
        {
            DDU32 ProcessPath : 1;
            DDU32 Modified : 1;
            DDU32 Enabled : 1;
            DDU32 IgnoreConnectivity : 1;
            DDU32 PathHasSrcId : 1; // TRUE = Path identified by Source id (RS1), FALSE = Path identified by Target id (RS2 Disabled path)
            DDU32 PreserveBootDisplay : 1;
            DDU32 Reserved : 26;
        };
        DDU32 Value;
    };
} DD_SET_TIMING_PATH_FLAGS;

typedef struct _DD_DOD_RESOURCE_INFO
{
    DDU8 *pDodGmmBlock;
    DDU32 DodGfxHWAddress; /*PHYSICAL_ADDRESS*/
    DDU8 *pDodLinearFrameBufferAddress;
} DD_DOD_RESOURCE_INFO;

typedef union _DD_MACROVISIONCAPS // TODO: cleanup with legacy defn
{
    DDU32 Value;
    struct
    {
        DDU32 APSTriggerSupported : 1; // bit 0
        DDU32 MVFullsupported : 1;     // bit 1
        DDU32 NoProtection : 1;        // bit 2
        DDU32 Reserved : 29;           // bit 3 - 31
    };
} DD_MACROVISIONCAPS;
typedef struct _DD_PATH
{
    DDU32 SourceId;
    DDU32 TargetId;
    // DD_SOURCE_MODE_INFO            PinnedSourceMode; @rsrivas2
    // DD_TIMING_INFO              PinnedTargetMode; @rsrivas2
    DD_SCALING  Scaling;
    DD_ROTATION Rotation;
    // Below parameters are used by mode enumeration DxgkDdiEnumVidPnCofuncModality only.
    DD_OS_FLAGS     OsFlags;
    DD_DRIVER_FLAGS DriverFlags;
    DDU32           NumSourceModes;
    // DD_SOURCE_MODE_INFO            *pSourceModeSet; @rsrivas2
    DDU32 NumTargetModes;
    // DD_TIMING_INFO              *pTargetModeSet; @rsrivas2
    DDU8 *pTgtModeSetIndices;
    // DD_SCALING_SUPPORT          ScalingSupport;
    DD_ROTATION_SUPPORT RotationSupport;
    // Below parameters are used by DxgkDdiCommitVidPn only.
    DD_SET_TIMING_PATH_FLAGS SetTimingFlags;
    // Below paramters are used by DxgkDdiSetTimingsFromVidPn
    // DD_COLOR_PIXEL_DESC         OutputColorFormat;@rsrivas2
    // Below parameters are mostly Unused and can be removed at some point.
    DD_ROTATION_OFFSET RotationOffset;
    DD_MACROVISIONCAPS MvCaps;
    DD_COPY_PROTECTION CopyProtection;
    DDU32              ImportanceOrdinal;
} DD_PATH;

typedef struct _DD_TOPOLOGY
{
    DDU32 NumPaths;
    //    DD_PATH     Paths[MAX_POSSIBLE_PIPES];@rsrivas2
    void *hVidPn;
} DD_TOPOLOGY;

#define DD_TOPOLOGY_GETNUMPATHS(hTopology) (((DD_TOPOLOGY *)hTopology)->NumPaths)
#define DD_PATH_GETTARGETID(hPath) ((DD_PATH *)hPath)->TargetId

//----------------------------------------------------------------------------
//
// Header with topology related  definitions - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// Header required to convert OS DDI parameters into driver defined parameters - START
//
//----------------------------------------------------------------------------

typedef enum _DD_FIRMWARE_TYPE
{
    DD_FIRMWARE_TYPE_UNKNOWN,
    DD_FIRMWARE_TYPE_BIOS,
    DD_FIRMWARE_TYPE_EFI,
    DD_FIRMWARE_TYPE_MAX
} DD_FIRMWARE_TYPE;

typedef struct _DD_PREOS_TOPOLOGY_DATA
{
    DD_IN BOOLEAN BuildFullTopology;
    //    DD_OUT DD_TOPOLOGY *pTopology;@rsrivas2
    //    DD_OUT DD_BPC_SUPPORTED itsPerColor; @rsrivas2
} DD_PREOS_TOPOLOGY_DATA;

typedef enum _DD_PATH_UPDATE
{
    DD_PATH_UPDATE_UNMODIFIED = 0,
    DD_PATH_UPDATE_ADDED      = 1,
    DD_PATH_UPDATE_MODIFIED   = 2,
    DD_PATH_UPDATE_REMOVED    = 3
} DD_PATH_UPDATE;

typedef struct _DD_SET_TIMING_ARG
{
    DD_IN DD_TOPOLOGY *pTopology;

} DD_SET_TIMING_ARG;

typedef struct _DD_ACTIVE_PATH
{
    DDU32 TargetId;
    DDU32 VisibleScreenX;
    DDU32 VisibleScreenY;
    //    DD_PIXELFORMAT      PixelFormat; @rsrivas2
    void *pDodLinearFBAdd;
} DD_ACTIVE_PATH;

typedef struct _DD_ACTIVE_TOPOLOGY
{
    DDU32 ActivePathCount;
    //    DD_ACTIVE_PATH  PathView[DD_MAX_VIEWS]; @rsrivas2
} DD_ACTIVE_TOPOLOGY;

typedef struct _DD_PRESENT_DISPLAY_ONLY
{
    DDU32 SourceID;
    DDU64 PresentId;
} DD_PRESENT_DISPLAY_ONLY;

typedef struct _DD_CHECK_SEAMLESS_RR_CHANGE_SUPPORT_ARG
{
    DD_IN DDU32 VidPnSourceId;
    DD_IN DDU32 DesiredPresentDuration;
    DD_OUT DDU32 ClosestSmallerDuration;
    DD_OUT DDU32 ClosestLargerDuration;
} DD_CHECK_SEAMLESS_RR_CHANGE_SUPPORT_ARG;

// Video output technology (VOT) type
typedef enum _DD_VIDEO_OUTPUT_TECHNOLOGY
{
    DD_VOT_UNKNOWN = 0,
    DD_VOT_VGA,
    DD_VOT_DVI,
    DD_VOT_HDMI,
    DD_VOT_DISPLAYPORT_EXTERNAL,
    DD_VOT_DISPLAYPORT_EMBEDDED,
    DD_VOT_MIPI,
    DD_VOT_VIRTUAL,
    DD_VOT_WDE,
    DD_VOT_MIRACAST,

    DD_VOT_MAX = DD_VOT_MIRACAST
} DD_VIDEO_OUTPUT_TECHNOLOGY;

#define IS_DP_SINK_TYPE(Type) (Type == DD_VOT_DISPLAYPORT_EXTERNAL || Type == DD_VOT_DISPLAYPORT_EMBEDDED)
#define IS_HDMI_DVI_SINK_TYPE(Type) (Type == DD_VOT_HDMI || Type == DD_VOT_DVI)
#define IS_EDP_SINK_TYPE(Type) (Type == DD_VOT_DISPLAYPORT_EMBEDDED)
#define IS_EXT_DP_SINK_TYPE(Type) (Type == DD_VOT_DISPLAYPORT_EXTERNAL)
#define IS_HDMI_SINK_TYPE(Type) (Type == DD_VOT_HDMI)
#define IS_DVI_SINK_TYPE(Type) (Type == DD_VOT_DVI)

typedef enum _DD_CHILD_STATUS_TYPE
{
    DD_STATUS_UNINITIALIZED,
    DD_STATUS_CONNECTION,
    DD_STATUS_ROTATION,
    DD_STATUS_MIRACAST_CONNECTION,
} DD_CHILD_STATUS_TYPE;

typedef enum _DD_TARGET_DETECT_TYPE
{
    DD_TARGET_DETECT_UNINITIALIZED,
    DD_TARGET_ENABLE_HPD,
    DD_TARGET_DISABLE_HPD,
    DD_TARGET_DETECT_ONE,
    DD_TARGET_DETECT_ALL,
    DD_TARGET_DETECT_ALL_ON_PORT
} DD_TARGET_DETECT_TYPE;

typedef struct _DD_DISPLAY_DETECT_CONTROL_ARGS
{
    DD_IN DDU32 TargetId;
    DD_IN DD_TARGET_DETECT_TYPE DetectType;
    DD_IN BOOLEAN NonDestructiveOnly;
} DD_DISPLAY_DETECT_CONTROL_ARGS;

typedef struct _DD_CHILD_STATUS
{
    DD_CHILD_STATUS_TYPE Type;
    DDU32                ChildUid;
    union {
        struct
        {
            BOOLEAN Connected;
        } HotPlug;
        struct
        {
            DDU8 Angle;
        } Rotation;
        struct
        {
            BOOLEAN                    Connected;
            DD_VIDEO_OUTPUT_TECHNOLOGY MiracastMonitorType;
        } Miracast;
    };
} DD_CHILD_STATUS;

typedef struct _DD_ARG_QCS
{
    DD_IN DD_CHILD_STATUS ChildStatus;
    DD_IN BOOLEAN NonDestructiveOnly;
} DD_ARG_QCS;

typedef struct _DD_DEVICE_DESCRIPTOR
{
    DDU32 DescriptorOffset;
    DDU32 DescriptorLength;
    void *pDescriptorBuffer;
} DD_DEVICE_DESCRIPTOR;

typedef struct _DD_ARG_QDD
{
    DD_IN DDU32 ChildUid;
    DD_IN_OUT DD_DEVICE_DESCRIPTOR DeviceDescriptor;
} DD_ARG_QDD;

typedef struct _DD_ARG_QIDC
{
    DD_IN DDU32 ChildUid;
    // To query integrated display's colorimetry information
    // Color Primaries
    DD_OUT DDU32 RedX;
    DD_OUT DDU32 RedY;
    DD_OUT DDU32 GreenX;
    DD_OUT DDU32 GreenY;
    DD_OUT DDU32 BlueX;
    DD_OUT DDU32 BlueY;
    DD_OUT DDU32 WhiteX;
    DD_OUT DDU32 WhiteY;

    // Luminance Data
    DD_OUT DDU16 MinLuminance;
    DD_OUT DDU16 MaxLuminance;
    DD_OUT DDU16 MaxFullFrameLuminance;

    // To fill the color bit depth override and colorimetry flags, if any
    //    DD_OUT DD_BPC_SUPPORTED FormatBitDepth; @rsrivas2
    DD_OUT DDU32 ColorimetryFlags;
    DD_OUT BOOLEAN IsOverrideAvailable;
} DD_ARG_QIDC;

typedef struct _DD_FLIP_MPO_PLANE_ATTRIB_FLAGS
{
    union {
        struct
        {
            DDU32 VerticalFlip : 1;
            DDU32 HorizontalFlip : 1;
            DDU32 AlphaBlend : 1;
            DDU32 HighQualityStretch : 1;
            DDU32 Reserved : 28;
        };
        DDU32 Value;
    };
} DD_FLIP_MPO_PLANE_ATTRIB_FLAGS;

typedef struct _DD_RECT
{
    DDS32 Left;
    DDS32 Top;
    DDS32 Right;
    DDS32 Bottom;
} DD_RECT;

#define DD_RECT_WIDTH(Rect) (DDU32)((Rect).Right - (Rect).Left)
#define DD_RECT_HEIGHT(Rect) (DDU32)((Rect).Bottom - (Rect).Top)

typedef struct _DD_MPO_PLANE_RECTS
{
    DD_RECT Source;
    DD_RECT Dest;
    DD_RECT Clip;
} DD_MPO_PLANE_RECTS;

typedef struct _DD_FLIP_MPO_PLANE_ATTRIBUTES
{
    DD_FLIP_MPO_PLANE_ATTRIB_FLAGS Flags;
    DD_MPO_PLANE_RECTS             Rect;
    DD_ROTATION                    Rotation;
    //    DD_COLOR_PIXEL_DESC            ColorInfo;@rsrivas2
} DD_FLIP_MPO_PLANE_ATTRIBUTES;

typedef struct _DD_FLIP_MPO_IN_FLAGS
{
    union {
        struct
        {
            DDU32 ModeChange : 1;
            DDU32 FlipStereo : 1;
            DDU32 FlipStereoTemporaryMono : 1;
            DDU32 FlipStereoPreferRight : 1;
            DDU32 RetryAtLowerIrql : 1;
            DDU32 Reserved : 27;
        };
        DDU32 Value;
    };
} DD_FLIP_MPO_IN_FLAGS;

typedef struct _DD_FLIP_MPO_OUT_FLAGS
{
    union {
        struct
        {
            DDU32 PrePresentNeeded : 1;
            DDU32 Reserved : 31;
        };
        DDU32 Value;
    };
} DD_FLIP_MPO_OUT_FLAGS;

typedef struct _DD_FLIP_MPO_PLANE_IN_FLAGS
{
    union {
        struct
        {
            DDU32 Enabled : 1;
            DDU32 FlipImmediate : 1;
            DDU32 FlipOnNextVSync : 1;
            DDU32 SharedPrimaryTransition : 1;
            DDU32 IndependentFlipExclusive : 1;
            DDU32 Reserved : 27;
        };
        DDU32 Value;
    };
} DD_FLIP_MPO_PLANE_IN_FLAGS;

typedef struct _DD_FLIP_MPO_PLANE_OUT_FLAGS
{
    union {
        struct
        {
            DDU32 PostPresentNeeded : 1;
            DDU32 HsyncInterruptCompletion : 1;
            DDU32 FlipConvertedToImmediate : 1;
            DDU32 Reserved : 29;
        };
        DDU32 Value;
    };
} DD_FLIP_MPO_PLANE_OUT_FLAGS;

typedef struct _DD_FLIP_MPO_PLANE
{
    DDU32                        LayerIndex;
    DDU64                        PresentId;
    DD_FLIP_MPO_PLANE_IN_FLAGS   PlaneInFlags;
    DD_FLIP_MPO_PLANE_OUT_FLAGS  PlaneOutFlags;
    DDU32                        MaxImmediateFlipLine;
    DDU32                        AllocationSegment;
    DDU32                        AllocationAddress;
    HANDLE                       hAllocation;
    DD_FLIP_MPO_PLANE_ATTRIBUTES PlaneAttributes;
} DD_FLIP_MPO_PLANE;

typedef enum _DD_FLIP_TYPE
{
    DD_FLIP_TYPE_UNKNOWN = 0,
    DD_FLIP_NO_MPO,
    DD_FLIP_BASE_MPO,
    DD_FLIP_MPO_2,
    DD_FLIP_MPO_3
} DD_FLIP_TYPE;

typedef struct _DD_ARG_FLIP_MPO
{
    DD_IN DDU32 VidPnSourceId;
    DD_IN DD_FLIP_TYPE FlipType;
    DD_IN DD_FLIP_MPO_IN_FLAGS CommonInFlags;
    DD_OUT DD_FLIP_MPO_OUT_FLAGS CommonOutFlags;
    DD_IN DDU32 PlaneCount;
    DD_IN DD_FLIP_MPO_PLANE *pPlanes;
    DD_IN DDU32 Duration;
    // TBD - below to be added later.
    // DD_MULTIPLANE_OVERLAY_POST_COMPOSITION*pPostComposition;
    // DD_HDR_METADATA*pHDRMetaData;
} DD_ARG_FLIP_MPO;

typedef struct _DD_ARG_SYNC_FLIP_MPO
{
    DD_ARG_FLIP_MPO FlipMPO;
    void *          pHwDev;
} DD_ARG_SYNC_FLIP_MPO;

typedef struct _DD_MPO_CAPS
{
    union {
        struct
        {
            DDU32 Rotation : 1;                       // Full rotation
            DDU32 RotationWithoutIndependentFlip : 1; // Rotation, but without simultaneous IndependentFlip support
            DDU32 VerticalFlip : 1;                   // Can flip the data vertically
            DDU32 HorizontalFlip : 1;                 // Can flip the data horizontally
            DDU32 StretchRGB : 1;                     // Supports RGB formats
            DDU32 StretchYUV : 1;                     // Supports YUV formats
            DDU32 BilinearFilter : 1;                 // Blinear filtering
            DDU32 HighFilter : 1;                     // Better than bilinear filtering
            DDU32 Shared : 1;                         // MPO resources are shared across VidPnSources
            DDU32 Immediate : 1;                      // Immediate flip support
            DDU32 Plane0ForVirtualModeOnly : 1;       // Stretching plane 0 will also stretch the HW cursor and should only be used for virtual mode support
            DDU32 Reserved : 21;
        };
        DDU32 Value;
    };
} DD_MPO_CAPS;

typedef struct _DD_GET_MPO_CAPS_ARG
{
    DD_IN DDU32 VidPnSourceId;
    DD_IN DDU32 PipeId;
    DD_OUT DDU32 MaxPlanes;
    DD_OUT DDU32 MaxRgbPlanes;
    DD_OUT DDU32 MaxYuvPlanes;
    DD_OUT DD_MPO_CAPS OverlayCaps;
    DD_OUT DDU32 MaxStretchFactorMultBy100;
    DD_OUT DDU32 MaxShrinkFactorPlanarMultBy100;
    DD_OUT DDU32 MaxShrinkFactorNonPlanarMultBy100;
} DD_GET_MPO_CAPS_ARG;

// Args for CheckMPO
typedef struct DD_CHECK_MPO_OUT_FLAGS
{
    union {
        struct
        {
            DDU32 FailingView : 8;       // The 0 based index of the first view that could not be supported
            DDU32 FailingLayerIndex : 8; // The 0 based index of the first plane that could not be supported
            DDU32 TryAgain : 1;          // The configuration is not supported due to a transition condition, which should shortly go away
            DDU32 Reserved : 15;
        };
        DDU32 Value;
    };
} DD_CHECK_MPO_OUT_FLAGS;

typedef struct _DD_CHECK_MPO_VIEW_DETAILS
{
    DDU32             PlaneCount;
    DD_FLIP_MPO_PLANE Planes[MAX_PLANES_PER_PIPE];
    // TBD - below to be added later.
    // DD_MULTIPLANE_OVERLAY_POST_COMPOSITION*pPostComposition;
    // DD_HDR_METADATA*pHDRMetaData;
} DD_CHECK_MPO_VIEW_DETAILS;

typedef struct _DD_ARG_CHECK_MPO
{
    DD_IN DD_CHECK_MPO_VIEW_DETAILS *pViews;
    DD_OUT BOOLEAN Supported;
    DD_OUT DD_CHECK_MPO_OUT_FLAGS OutFlags;
} DD_ARG_CHECK_MPO;

typedef struct _DD_NOTIFY_FLIP_ARGS
{
    DD_IN PIPE_ID PipeId;
    DD_IN BOOLEAN AsyncFlip; // 1 = Async Flip, 0 = Sync Flip
    DD_OUT BOOLEAN VrrWasEnabled;
} DD_NOTIFY_FLIP_ARGS;

// Args for DxgkDdiSetVidPnSourceVisibility
typedef struct _DD_ARG_SSV
{
    DDU32   VidPnSourceId;
    BOOLEAN Visible;
} DD_ARG_SSV;

// Args for DxgkDdiRecommendMonitorModes
typedef struct _DD_COLOR_COEFF_DYNAMIC_RANGES
{
    DDU32 FirstChannel;
    DDU32 SecondChannel;
    DDU32 ThirdChannel;
    DDU32 FourthChannel;
} DD_COLOR_COEFF_DYNAMIC_RANGES;

typedef enum _DD_MONITOR_CAPABILITIES_ORIGIN
{
    DD_MCO_UNINITIALIZED                      = 0,
    DD_MCO_DEFAULTMONITORPROFILE              = 1,
    DD_MCO_MONITORDESCRIPTOR                  = 2,
    DD_MCO_MONITORDESCRIPTOR_REGISTRYOVERRIDE = 3,
    DD_MCO_SPECIFICCAP_REGISTRYOVERRIDE       = 4,
    DD_MCO_DRIVER                             = 5, //  + display adapter driver.
} DD_MONITOR_CAPABILITIES_ORIGIN;

typedef struct _DD_OS_MONITOR_MODE
{
    DDU32                          OsModeId;
    DD_TIMING_INFO                 TimingInfo;
    DD_COLOR_COEFF_DYNAMIC_RANGES  ColorCoeffDynamicRanges;
    DD_MONITOR_CAPABILITIES_ORIGIN Origin;
} DD_OS_MONITOR_MODE;

typedef struct _DD_GET_OS_ADDITIONAL_TARGET_MODE_ARG
{
    DD_IN DDU32 TargetId;
    DD_OUT DDU32 NumModes;
    DD_OUT DD_TIMING_INFO *pTimingInfo;
} DD_GET_OS_ADDITIONAL_TARGET_MODE_ARG;

typedef enum _DD_MONITOR_DESCRIPTOR_TYPE
{
    DD_MDT_UNINITIALIZED          = 0,
    DD_MDT_VESA_EDID_V1_BASEBLOCK = 1,
    DD_MDT_VESA_EDID_V1_BLOCKMAP  = 2,
    DD_MDT_OTHER                  = 255
} DD_MONITOR_DESCRIPTOR_TYPE;

typedef struct _DD_MONITOR_DESCRIPTOR
{
    DDU32                          Id;
    DD_MONITOR_DESCRIPTOR_TYPE     Type;
    DDU32                          DataSize;
    void *                         pData;
    DD_MONITOR_CAPABILITIES_ORIGIN Origin;
} DD_MONITOR_DESCRIPTOR;

// Target descriptor to be passed to protocol
typedef struct _DD_TARGET_DESCRIPTOR
{
    DD_PORT_TYPE               Port;
    DD_VIDEO_OUTPUT_TECHNOLOGY SinkType;
    DDU8                       SinkIndex; // starts with index 0 for each display type; non zero for DP MST or other multi-display scenarios on same port
} DD_TARGET_DESCRIPTOR;

typedef struct _DD_OVERRIDE_MONITOR_DESCRIPTOR_ARG
{
    IN DDU32 TargetId;
    IN DD_TARGET_DESCRIPTOR TargetDesc;
    OUT DDU8 NumMonitorDescriptor;
    OUT DD_MONITOR_DESCRIPTOR *pMonitorDescriptor;
    OUT BOOLEAN OverrideRequired;
} DD_OVERRIDE_MONITOR_DESCRIPTOR_ARG;

typedef struct _DD_ARG_RMM
{
    DD_IN DDU32 ChildId;
    DD_IN DDU32 NumOsMonitorModes;
    DD_IN DD_OS_MONITOR_MODE *pOsMonitorModes;
    DD_OUT DDU32 NumDriverMonitorModesToAdd;
    DD_OUT DD_OS_MONITOR_MODE *pDriverMonitorModesToAdd;
} DD_ARG_RMM;

// Args for DxgkDdiIsSupportedVidPn
typedef struct _DD_ARG_ISV
{
    DD_IN DD_TOPOLOGY *pTopology;
    DD_OUT BOOLEAN IsVidPnSupported;
} DD_ARG_ISV;

// Args for DxgkDdiEnumVidPnCofuncModality
typedef struct _DD_ARG_EVCM
{
    DD_IN DD_TOPOLOGY *pConstrainingTopology;
} DD_ARG_EVCM;

// Args for VSync Control Interrupt
typedef enum _DD_CRTC_VSYNC_STATE
{
    DD_VSYNC_ENABLE             = 0,
    DD_VSYNC_DISABLE_KEEP_PHASE = 1,
    DD_VSYNC_DISABLE_NO_PHASE   = 2,
} DD_CRTC_VSYNC_STATE;

typedef struct _DD_CTRL_VSYNC_INTERRUPT_ARG
{
    DD_CRTC_VSYNC_STATE CrtcVsyncState;
} DD_CTRL_VSYNC_INTERRUPT_ARG;

// Args for DxgkDdiSetPointerPosition
typedef struct _DD_ARG_SPP
{
    DDU32   VidPnSourceId;
    DDU32   X;
    DDU32   Y;
    BOOLEAN Visible;
} DD_ARG_SPP;

// Args for DxgkDdiSetPointerShape

typedef struct _DD_POINTER_FLAGS
{
    union {
        struct
        {
            DDU32 Monochrome : 1;
            DDU32 Color : 1;
            DDU32 MaskedColor : 1;
            DDU32 SoftwareCursor : 1;
            DDU32 Reserved : 28;
        };
        DDU32 Value;
    };
} DD_POINTER_FLAGS;

typedef struct _DD_ARG_SPS
{
    DDU32            VidPnSourceId;
    DDU32            Width;
    DDU32            Height;
    DDU32            Pitch;
    void *           pPixels;
    DDU32            XHot;
    DDU32            YHot;
    DD_POINTER_FLAGS Flags;
} DD_ARG_SPS;

// Args for DxgkDdiQueryChildRelations

typedef enum _DD_CHILD_DEVICE_TYPE
{
    DD_CD_TYPE_UNKNOWN,
    DD_CD_TYPE_VIDEO_OUTPUT,
    DD_CD_TYPE_OTHER,
    DD_CD_TYPE_INTEGRATED_DISPLAY
} DD_CHILD_DEVICE_TYPE;

typedef enum _DD_MONITOR_ORIENTATION_AWARENESS
{
    DD_MOA_UNINITIALIZED = 0,
    DD_MOA_NONE          = 1,
    DD_MOA_POLLED        = 2,
    DD_MOA_INTERRUPTIBLE = 3
} DD_MONITOR_ORIENTATION_AWARENESS;

typedef struct _DD_VIDEO_OUTPUT_CAPABILITIES
{
    DD_VIDEO_OUTPUT_TECHNOLOGY       InterfaceTechnology;
    BOOLEAN                          InternalDisplay;
    DD_MONITOR_ORIENTATION_AWARENESS MonitorOrientationAwareness;
    BOOLEAN                          SupportsSdtvModes;
} DD_VIDEO_OUTPUT_CAPABILITIES;

typedef enum _DD_CHILD_DEVICE_HPD_AWARENESS
{
    DD_CD_HPDA_UNKNONN          = 0,
    DD_CD_HPDA_ALWAYS_CONNECTED = 1,
    DD_CD_HPDA_NONE             = 2,
    DD_CD_HPDA_POLLED           = 3,
    DD_CD_HPDA_INTERRUPTIBLE    = 4
} DD_CHILD_DEVICE_HPD_AWARENESS;

typedef struct _DD_CHILD_CAPABILITIES
{
    union {
        // TypeVideoOutput
        DD_VIDEO_OUTPUT_CAPABILITIES VideoOutput;
        // TypeOther
        struct
        {
            DDU32 MustBeZero;
        } Other;
    } Type;

    DD_CHILD_DEVICE_HPD_AWARENESS HpdAwareness;
} DD_CHILD_CAPABILITIES;

typedef struct _DD_CHILD_DESCRIPTOR
{
    DD_CHILD_DEVICE_TYPE  ChildDeviceType;
    DD_CHILD_CAPABILITIES ChildCapabilities;
    DDU32                 AcpiUid;
    DDU32                 ChildUid;
} DD_CHILD_DESCRIPTOR;

typedef struct _DD_ARG_QCR
{
    DD_OUT DD_CHILD_DESCRIPTOR *pChildRelations;
    DD_IN_OUT DDU32 NumChildDescriptor;
} DD_ARG_QCR;

typedef struct _DD_SRC_VISIBILITY
{
    DD_IN DDU32 SourceID;
    DD_IN BOOLEAN Visibile;
    DD_IN PIPE_ID Pipe;
} DD_SRC_VISIBILITY;

// I2C MCCS interface
#define AB_HOST_ADDR 0x51
#define BYTES_SENT_FOR_DATA_LENGTH 0x02
#define MCCS_DEVICE_ADDR 0x6E
#define MAX_LUT_AUX_BUFSIZE 0x0200
typedef struct _DD_I2C_ARGS
{
    DDU32   ChildUid;
    BOOLEAN WriteI2C; // 0 - Read I2C, 1 - Write I2C
    DDU32   I2CAddress;
    DDU32   DataLength;
    void *  pData;
} DD_I2C_ARGS;

// Args for DxgkDdiNotifyAcpiEvent
typedef enum _DD_ACPI_EVENT_TYPE
{
    DD_ACPI_EVENT_TYPE_UNKNOWN = 0,
    DD_ACPI_EVENT_TYPE_ACPI_EVENT,
    DD_ACPI_EVENT_TYPE_POWER_STATE_EVENT,
    DD_ACPI_EVENT_TYPE_DOCKING_EVENT,
    DD_ACPI_EVENT_TYPE_CHAINED_EVENT,
} DD_ACPI_EVENT_TYPE;

typedef enum _DD_ACPI_EVENT
{
    DD_ACPI_EVENT_UNKNOWN = 0,
    DD_ACPI_EVENT_AC_DC_SWITCH,
    DD_ACPI_EVENT_PANEL_SWITCH,
    DD_ACPI_EVENT_LID_STATE_CHANGE,
    DD_ACPI_EVENT_DOCK_STATE_CHANGE,
    // unused
    /*
    DD_ACPI_EVENT_CYCLE_DISPLAY_HOTKEY,
    DD_ACPI_EVENT_DEVICE_HOTPLUG,
    DD_ACPI_EVENT_PANEL_SWITCH,
    DD_ACPI_EVENT_VIDEO_WAKEUP,
    */
} DD_ACPI_EVENT;

typedef enum _DD_ACPI_FLAGS
{
    ACPI_FLAGS_UNKNOWN = 0,
    ACPI_FLAGS_POLL_DISPLAY_CHILDREN,
    ACPI_FLAGS_CHANGE_DISPLAY_MODE,
} DD_ACPI_FLAGS;

typedef enum _DD_ADAPTER_STATE
{
    DD_ADAPTER_NOTREADY = 0,
    DD_ADAPTER_READY    = 1
} DD_ADAPTER_STATE;

typedef struct _DD_NOTIFY_ACPI_EVENT_ARGS
{
    DD_IN DD_ADAPTER_STATE AdapterState;
    DD_IN DD_ACPI_EVENT_TYPE AcpiEventType;
    DD_IN DD_ACPI_EVENT AcpiEvent;
    DD_IN DDU32 EventArg;
    DD_OUT DD_ACPI_FLAGS AcpiFlags;
} DD_NOTIFY_ACPI_EVENT_ARGS;

//  Arguments to get BLC levels from BIOS (got by evaluating _BLC)
typedef struct _DD_GET_ACPI_BCL_LEVELS
{
    DD_IN DDU32 BufferSize; // The size, in bytes, of the buffer that is passed in the BrightnessLevels parameter
    DD_IN_OUT   DDU8
    *pLevelCount; // A pointer to a variable that receives the number of brightness levels that the driver returns in the buffer that the BrightnessLevels parameter points to.
    DD_IN_OUT DDU8 *pBrightnessLevels; // A pointer to a buffer that receives the brightness levels that an integrated display panel supports.
} DD_GET_ACPI_BCL_LEVELS;

typedef enum _DD_BLC_OPERATION
{
    DISP_PC_BLC_OPERATION_GET_BRIGHTNESS = 0,
    DISP_PC_BLC_OPERATION_SET_BRIGHTNESS,
    DISP_PC_BLC_OPERATION_SET_AGGRESSIVE_LEVEL,
    DISP_PC_BLC_OPERATION_DPST_ADJUSTMENT,
} DD_BLC_OPERATION;

typedef struct _DD_BLC_DDI_PARAMS
{
    DD_BLC_OPERATION Operation;
    union {
        // DPST or ADT operation
        BOOLEAN FeatureActive;

        // Set Brightness operation
        DDU8 Percent; // Actual Backlight Setting (in percent)

        // Get Brightness operation
        DDU8 *pPercent; // Actual Backlight Setting (in percent)
        DDU8  Lux;      // ALS Lux value to override
    };
} DD_BLC_DDI_PARAMS;
typedef struct _DD_BACKLIGHT_INFO
{
    DDU16 BlcUserSetting;
    DDU16 BlcEffective;
} DD_BACKLIGHT_INFO;

typedef struct _DD_POST_DISPLAY_INFO
{
    DDU32          TargetID;
    DDU32          Width;
    DDU32          Height;
    DDU32          Pitch;
    DD_PIXELFORMAT ColorFormat;
    DDU32          AcpiId;
} DD_POST_DISPLAY_INFO;

//----------------------------------------------------------------------------
//
// Header required to convert OS DDI parameters into driver defined parameters - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// CCD data structures -- START
//
//----------------------------------------------------------------------------

// Tile widths to use with each of the above suface types
// For YF tiling, 8bpp has a different width than the others
// All tile widths are in bytes.
/*typedef enum _SURFACE_MEMORY_TILE_WIDTH
{
    SURFACE_MEMORY_TILE_WIDTH_DEFAULT = 64,
    SURFACE_MEMORY_TILE_WIDTH_LINEAR = SURFACE_MEMORY_TILE_WIDTH_DEFAULT,
    SURFACE_MEMORY_TILE_WIDTH_TILED = 512,
    SURFACE_MEMORY_TILE_WIDTH_X_TILED = SURFACE_MEMORY_TILE_WIDTH_TILED,
    SURFACE_MEMORY_TILE_WIDTH_Y_LEGACY_TILED = 128,
    SURFACE_MEMORY_TILE_WIDTH_Y_F_TILED_8BPP = 64,
    SURFACE_MEMORY_TILE_WIDTH_Y_F_TILED_NON_8BPP = 128
} SURFACE_MEMORY_TILE_WIDTH;*/

typedef enum _SURFACE_MEMORY_TYPE DD_SURFACE_MEMORY_TYPE; // TBD: Need to change this to DD_ defn.

#define DD_IS_Y_TILE_MEMORY(SurfaceMemType) ((SurfaceMemType == SURFACE_MEMORY_Y_LEGACY_TILED) || (SurfaceMemType == SURFACE_MEMORY_Y_F_TILED))
// Struct representing surface memory offset data (used in GMM)
/*typedef struct _SURFACE_MEM_OFFSET_INFO
{
    // Indicates surface memory type
    DD_IN  DD_SURFACE_MEMORY_TYPE SurfaceMemType;

    union
    {
        // Tiled offset
        struct
        {
            DD_IN  DDU32 TiledXOffset;
            DD_IN  DDU32 TiledYOffset;
            DD_IN  DDU32 TiledUVXOffset; // NV12 case
            DD_IN  DDU32 TiledUVYOffset; // NV12 case
            DD_IN  DDU64 BaseAddress;
            DD_IN  DDU64 UVBaseAddress;
        };
    };

    DD_IN DDU32 UvDistance;  // For NV12 surface, as of now nv12 cant come in normal flip path
    DD_IN DDU32 AuxDistance; // Control surface Aux Offset. Will be 0 for non unified allocations, MP is abstracted from it
} SURFACE_MEM_OFFSET_INFO;*/

// Args for ddReportFlipDone
typedef struct _DD_ARG_RFD
{
    BOOLEAN    FlipDoneEvent; // 0 - VBI, 1 - Flip Done Interrupt
    PIPE_ID    PipeId;
    PLANE_TYPE PlaneId; // This is valid only when Hsync = TRUE.
} DD_ARG_RFD;

typedef struct _DD_SURFACE_ATTRIBUTES
{
    DD_IN DD_PIXELFORMAT PixelFormat;
    DD_IN DD_SURFACE_MEMORY_TYPE SurfMemType;
    DD_IN DDU32 SurfStride;
    DD_IN DDU32 UvSurfDistance;
    DD_IN DDU32 UvSurfStride;
    struct
    {
        DD_IN DDU32 PlaneEncrypted : 1;
    };

    DD_IN DD_COLOR_PIXEL_DESC ColorInfo;
} DD_SURFACE_ATTRIBUTES;

typedef enum _DD_SURF_COMPRESSION_TYPE
{
    DD_SURF_UNCOMPRESSED,
    DD_SURF_RENDER_COMPRESSED,
    DD_SURF_MEDIA_COMPRESSED
} DD_SURF_COMPRESSION_TYPE;

typedef struct _DD_COMPRESSION_DETAILS
{
    DD_SURF_COMPRESSION_TYPE CompType;
    DDU32                    BaseCompMetaDataDistance;
    DDU32                    BaseCompMetaDataStride;
    DDU64                    BaseClearColorValue;
    DDU32                    UVCompMetaDataDistance;
    DDU32                    UVCompMetaDataStride;
    DDU64                    UVClearColorValue;
} DD_COMPRESSION_DETAILS;

typedef struct _DD_GET_COMPRESSION_DEATILS_ARGS
{
    DD_IN HANDLE hAllocation;
    DD_IN DD_ROTATION PlaneOrientation;
    DD_OUT DD_COMPRESSION_DETAILS *pCompDetails;
} DD_GET_COMPRESSION_DEATILS_ARGS;

typedef struct _DD_GET_SURF_ATTRIB_ARGS
{
    DD_IN HANDLE hAllocation;
    DD_IN DD_ROTATION PlaneOrientation;
    DD_IN BOOLEAN IsUVPlane; // TODO:
    DD_OUT DD_SURFACE_ATTRIBUTES *pPlaneSurfAttributes;
} DD_GET_SURF_ATTRIB_ARGS;

typedef struct _DD_GET_SURF_POSITION_ARGS
{
    DD_IN HANDLE hAllocation;
    DD_IN DD_ROTATION Rotation;
    DD_IN_OUT DDU32 PanningPosX;
    DD_IN_OUT DDU32 PanningPosY;
    DD_OUT DDU32 UvPanningPosX;
    DD_OUT DDU32 UvPanningPosY;
    DD_OUT DDU32 HwAddressBase;
    DD_OUT DDU32 HwAddressUv;
} DD_GET_SURF_POSITION_ARGS;

typedef struct _DD_GET_POSSIBLE_TILING_ARGS
{
    DD_IN DDU32 VidPnSourceId;
    DD_IN DDU32 HResolution;
    DD_IN DD_PIXELFORMAT PixelFormat;
    DD_IN DD_ROTATION Rotation;
    DD_OUT DDU32 MemFormats; // Mask of the suported Formats
} DD_GET_POSSIBLE_TILING_ARGS;

/**
@brief  Display connection related events to be reported to OS
*/
typedef enum _DD_DISPLAY_CONNECTION_EVENTS
{
    DD_DISP_CONN_UNKNOWN,
    DD_DISP_CONN_PLUG,   // display plugged in
    DD_DISP_CONN_UNPLUG, // display unplugged from connector
    DD_DISP_CONN_REPLUG, ///< display unplugged and then new display plugged in, both of same sink type. possible when switching SST/MST mode from panel settings; MST subtopology
                         ///< change etc.
    DD_DISP_CONN_MAX_EVENT
} DD_DISPLAY_CONNECTION_EVENTS;

#define DD_IS_DISPLAY_ATTACHED(ConnEvent) ((ConnEvent) == DD_DISP_CONN_PLUG || (ConnEvent) == DD_DISP_CONN_REPLUG)

typedef struct _DD_QUERY_CONNECTION_CHANGE
{
    DD_OUT DDU64 ConnectionChangeId;
    DD_OUT DDU32 TargetId;
    DD_OUT DD_DISPLAY_CONNECTION_EVENTS ConnectionStatus;
    DD_OUT DD_VIDEO_OUTPUT_TECHNOLOGY LinkTargetType;
    DD_OUT BOOLEAN ConnectionChangesPending;
} DD_QUERY_CONNECTION_CHANGE;

typedef struct _DD_CONNECTION_STATUS
{
    DDU32                        DisplayUid;
    DD_DISPLAY_CONNECTION_EVENTS Event;

    // BOOLEAN NotifyOPM;
    // BOOLEAN IsModesetRequired;
} DD_CONNECTION_STATUS;

typedef struct _DD_VSYNC_INFO
{
    DDU32                        LayerIndex;
    BOOLEAN                      Enabled;
    DDU64                        OsPresentId;
    DDU32                        OsAddress;
    DD_FLIP_MPO_PLANE_ATTRIBUTES PlaneAttribs;
} DD_VSYNC_INFO;

typedef struct _DD_CB_VSYNC_ARG
{
    DD_FLIP_TYPE  FlipType;
    BOOLEAN       FlipDoneEvent;
    DDU32         TargetId;
    DDU32         VsyncInfoCount;
    DD_VSYNC_INFO VsyncInfo[MAX_PLANES_PER_PIPE];
    void *        pPreAllocatedLocal;
} DD_CB_VSYNC_ARG;

typedef struct _DD_CB_PERIODICMONITOREDFENCE_ARG
{
    DDU32 NotificationId; // ID to return to OS
    DDU32 VidPnTargetId;  // VidPnTargetID to return to OS
} DD_CB_PERIODICMONITOREDFENCE_ARG;

//----------------------------------------------------------------------------
//
// CCD data structures -- END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// Power Manager data structures -- START
//
//----------------------------------------------------------------------------

typedef enum _DD_DEV_POWER_STATE
{
    DD_POWERSTATE_UNDEFINED = 0,
    DD_POWERSTATE_D0        = 1,
    DD_POWERSTATE_D1,
    DD_POWERSTATE_D2,
    DD_POWERSTATE_D3,
} DD_DEV_POWER_STATE;

typedef enum _DD_SYS_POWER_ACTION
{
    DD_POWERACTION_UNDEFINED = 0,
    DD_POWERACTION_NONE,
    DD_POWERACTION_SLEEP,
    DD_POWERACTION_HIBERNATE,
    DD_POWERACTION_SHUTDOWN,
    DD_POWERACTION_SHUTDOWNRESET,
    DD_POWERACTION_SHUTDOWNOFF,
} DD_SYS_POWER_ACTION;

typedef struct _DD_SET_ADAPTER_PWR_ARGS
{
    DD_DEV_POWER_STATE  DisplayDevPowerState;
    DD_SYS_POWER_ACTION DisplaySysPowerAction;
} DD_SET_ADAPTER_PWR_ARGS;

//----------------------------------------------------------------------------
//
// Power Manager data structures -- END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// TDR related data structures -- START
//
//----------------------------------------------------------------------------
typedef enum _DD_TDR_OPERATION
{
    DD_TDR_OPERATION_RESET = 1,              // Reset hardware
    DD_TDR_OPERATION_RESET_PRE_GDRST,        // Used to inform SB prior of GDRST
    DD_TDR_OPERATION_RESET_POST_GDRST,       // Used to inform SB post GDRST.
    DD_TDR_OPERATION_RESTART,                // Restart hardware
    DD_TDR_OPERATION_COLLECT_INFO_REGISTERS, // Dump registers into OCA report
    DD_TDR_OPERATION_COLLECT_INFO_STATE,     // Dump state info into OCA report
} DD_TDR_OPERATION;

typedef struct _DD_TDR_ARGS
{
    DD_TDR_OPERATION Operation; // TDR operation
    /*TBD: Not used as of now. Will decide later if needed
    void    *pOCABlobHdr;   // Pointer to OCA blob header
    void    *pDebugBuff; // pointer to debug buffer
    DDU32              DebugBufAvailSize; // Available size of the debug buffer
    DDU32              OutputSize;  // output size
    */
} DD_TDR_ARGS;

//----------------------------------------------------------------------------
//
// TDR related data structures -- END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// Data Structure for Interrupt operations -- START
//
//----------------------------------------------------------------------------
/*typedef enum _INTERRUPT_OPERATION
{
    ENABLE_INTERRUPT = 1,
    DISABLE_INTERRUPT = 2,
    MASK_INTERRUPT = 3,
    UNMASK_INTERRUPT = 4,
    GET_DISABLED_INTERRUPTS = 5 // Flag To Detect Disabled Interrupts also.
} INTERRUPT_OPERATION;*/

/*typedef enum _LID_STATE
{
    LID_OPENED = 0x0,
    LID_CLOSED = 0x1
} LID_STATE;*/

typedef enum _DOCK_STATE
{
    DOCK_OPENED = 0x0,
    DOCK_CLOSED = 0x1
} DOCK_STATE;

// Short Pulse Interrupt related Data Structure Definitions.
// The enum value specifies the type of operation to be performed on Event Objects.
#define DD_SPI_MAX_EVENT 2

typedef enum _DD_EVENTOBJ_FUNC_TYPE
{
    DD_SET_EVENT = 0,
    DD_CLEAR_EVENT,
    DD_READ_EVENT,
    DD_WAIT_EVENT,
    DD_INVALID_EVENT
} DD_EVENTOBJ_FUNC_TYPE;

typedef enum _DD_SPI_EVENT_OBJECT_INDEX
{
    DD_EVENT_UNIINITIALIZED    = -1,
    DD_DPB_WAIT_RI             = 0,
    DD_DPB_WAIT_KSV_FIFO       = 1,
    DD_DPC_WAIT_RI             = 2,
    DD_DPC_WAIT_KSV_FIFO       = 3,
    DD_DPD_WAIT_RI             = 4,
    DD_DPD_WAIT_KSV_FIFO       = 5,
    DD_DPB_WAIT_SIDEBAND_REPLY = 6,
    DD_DPC_WAIT_SIDEBAND_REPLY = 7,
    DD_DPD_WAIT_SIDEBAND_REPLY = 8,
    DD_MAX_SPI_EVENT_OBJECTS
} DD_SPI_EVENT_OBJECT_INDEX;

// Structure passed as parameter while performing different actions on an event object.
typedef struct _DD_EVENTOBJ_PARAMS
{
    DD_IN DD_EVENTOBJ_FUNC_TYPE FuncType; // Defines the type of operation.
    union {
        DD_IN DD_SPI_EVENT_OBJECT_INDEX EventObjIndex; // The index to SPI Event Object array on which
    };
    // operation has to be performed.
    DD_IN DDU32 TimeOut;   // The Time out value for Wait event. This will be looked only for Wait operation.
    DD_OUT DDS32 OpResult; // Return Value. Varies based on the operation.
} DD_EVENTOBJ_PARAMS;

// The enum type will define the type of link trainings that can be performed.
/*typedef enum _LINK_TRAINING_METHOD
{
    RETRAIN_LINK = 0,       // Retrain the link.with the existing data
    USE_LOW_BITRATE = 1,       // retrain the link with low bit rate
    USE_HIGH_BITRATE = 2,        // retrain the link with high bit rate
    INVALID_METHOD = 0xFF
} LINK_TRAINING_METHOD;*/

// The structure is used by Miniport when retraining the link. If reprogramming of pipe
// is needed for the display to be driven properly, SoftBIOS will set the bit accordingly.
typedef struct _DD_LINK_TRAINING_PARAMS
{
    DD_IN DDU32 DisplayUid;                 // DisplayUID of device which generated the Short Pulse Interrupt.
    DD_IN DD_OUT DDU8 LinkTrainingMethod;   // LINK_TRAINING_METHOD
    DD_OUT BOOLEAN IsNeedPipeReprogramming; // Tells Whether PipeReprogramming is needed or not.
} DD_LINK_TRAINING_PARAMS;

typedef enum _DD_SP_INT_ID
{
    DP_PORT_A_SPI  = 1,
    DP_PORT_B_SPI  = 2,
    DP_PORT_C_SPI  = 3,
    DP_PORT_D_SPI  = 4,
    DP_PORT_E_SPI  = 5,
    DP_PORT_F_SPI  = 6,
    WIGIG_PORT_SPI = 7,
    UNDEFINED_SPI
} DD_SP_INT_ID;

typedef struct _DD_SPI_EVENT_DATA
{
    DD_OUT DDU32 Port;
    DD_OUT DDU32 HandleEvent;                           // uses the ENUM SPI_EVENT_TYPE
    DD_OUT DD_SPI_EVENT_OBJECT_INDEX HDCPEventObjIndex; // Today its Valid only for eKSVFifoReady event..
    DD_OUT DDU8 ValidDisplayUidCount;
    DD_OUT DDU32 DisplayUidList[3]; // Display for which event is generated
} DD_SPI_EVENT_DATA;

typedef struct _DD_SPI_ALLEVENTS_DATA
{
    DD_SPI_EVENT_DATA SpiEventData[8 * 2]; // This is even to add even for HDMI related ports..
    DDU32             NumEventsDetected;   // Num Events actually Detected based on SPI..
    DDU32             MaxNumEvents;        // Maximum Events that can be actually detected. Should be initialized to MAX_DP_PORTS
} DD_SPI_ALLEVENTS_DATA;

typedef struct _DD_SPI_DATA
{
    DD_IN DDU32 NumSPIDetected; // Number of SPI's called during the worker thread..Should be always less than MAX_DP_PORTS
    DD_IN DD_SP_INT_ID    SpiDetected[8];
    DD_SPI_ALLEVENTS_DATA AllSPIEvents;
} DD_SPI_DATA;

//---------------------------------------------------------------------------------------------------------------------
//
//  NOTE: Any change in the interrrupt args structure below has to be reflected in the enum definitions above.
//
//---------------------------------------------------------------------------------------------------------------------
/*typedef enum _INTERRUPT_UNION_VALUE
{
    INTCRT = 0x1,
    RESERVED_TV = 0x2,
    SDVOB = 0x4,
    SDVOC = 0x8,
    INTDP_HDMIA = 0x10,
    INTDP_HDMIB = 0x20,
    INTDP_HDMIC = 0x40,
    INTDP_HDMID = 0x80,
    INTDP_HDMIA_SP = 0x100,
    INTDP_HDMIB_SP = 0x200,
    INTDP_HDMIC_SP = 0x400,
    INTDP_HDMID_SP = 0x800,
    REN_GEY_SWCMDCOMPLETE = 0x1000,
    REN_GEY_EVLFREQCHNG = 0x2000,
    REN_GEY_AVGBSYTHRESHOLD = 0x4000,
    REN_GEY_CNTBSYTHRESHOLD = 0x8000,
    REN_GEY_UPEVLINTERVAL = 0x10000,
    REN_GEY_DOWNEVLINTERVAL = 0x20000,
    REN_GEY_CNTRLDISABLESTATE = 0x40000,
    DBG_INTERRUPT = 0x80000,
    PIPECTRLNOTIFY = 0x100000,
    RENDERUSERINTERRUPT = 0x200000,
    RNDRMMIOSYNCFLUSHSTATUS = 0x400000,
    RNDRWATCHDOGCNTREXCD = 0x800000,
    RNDRASCNTXSWITCH = 0x1000000,
    RNDRPGFAULT = 0x2000000,
    VIDEOUSERINTERRUPT = 0x4000000,
    VIDEODECPIPELINECNTREXCD = 0x8000000,
    VIDEOMIFLUSHDWNTFY = 0x10000000,
    VIDEOMMIOSYNCFLUSH = 0x20000000,
    VIDEOASCNTXSWITCH = 0x40000000,
    VIDEOPAGEFAULT = 0x80000000
}INTERRUPT_UNION_VALUE;

typedef enum _INTERRUPT_UNION_VALUE_1
{
    LBPC_PIPEA = 0x1,
    LBPC_PIPEB = 0x2,
    DPST_HIST = 0x4,
    DPST_PHASEIN = 0x8,
    PCUMBEVENT = 0x10,
    PCRNDRFREQDOWNRC6TIMEOUT = 0x20,
    PC_RPFUPTHRESHOLD = 0x40,
    PC_RPFDOWNTHRESHOLD = 0x80,
    BLITTERASCNTXSWITCH = 0x100,
    BLITTERMIFLUSHDWNTFY = 0x200,
    BLITTERMMIOSYNCFLUSH = 0x400,
    BLITTERMIUSER = 0x800,
    BLITTERPGFAULT = 0x1000,
    VSYNCPIPEA = 0x2000,
    VSYNCPIPEB = 0x4000,
    VBLANKPIPEA = 0x8000,
    VBLANKPIPEB = 0x10000,
    GSESYSTEMLEVEL = 0x20000,
    VBLANKTPV = 0x40000,
    ASLEINTERRUPT = 0x80000,
    ALLFIRSTLEVEL = 0x100000,
    SPRITEPLANEAFLIPDONE = 0x200000,
    SPRITEPLANEBFLIPDONE = 0x400000,
    VSYNCPIPEC = 0x800000,
    VBLANKPIPEC = 0x1000000,
    SPRITEPLANECFLIPDONE = 0x2000000,
    AUDIOHDCPREQA = 0x4000000,
    AUDIOHDCPREQB = 0x8000000,
    AUDIOHDCPREQC = 0x10000000,
    AUDIOHDCPREQ = 0x20000000,
    PERFMONBUFFHALFFULL = 0x40000000,
    SPRITEPLANEDFLIPDONE = 0x80000000,
    SPRITEPLANEEFLIPDONE = 0xF,
    SPRITEPLANEFFLIPDONE = 0xF0,
}INTERRUPT_UNION_VALUE_1;

typedef enum _INTERRUPT_UNION_VALUE_2
{
    FIFO_UNDERRUN_PIPEA = 0x1,
    CRCERROR_PIPEA = 0x2,
    CRCDONE_PIPEA = 0x4,
    FIFO_UNDERRUN_PIPEB = 0x8,
    CRCERROR_PIPEB = 0x10,
    CRCDONE_PIPEB = 0x20,
    FIFO_UNDERRUN_PIPEC = 0x40,
    CRCERROR_PIPEC = 0x80,
    CRCDONE_PIPEC = 0x100,
    VEUSERINTERRUPT = 0x200,
    VEMMIOSYNCFLUSH = 0x400,
    VECMDPARSERMASTERERR = 0x800,
    VEMIFLUSHDWNOTIFY = 0x1000,
    RENDERPARITYERR = 0x2000,
    VIDEOPAVPATTACK = 0x4000,
    VIDEOUSERINT2 = 0x8000,
    VIDEODECPIPELINECNTREXCD2 = 0x10000,
    VIDEOMIFLUSHDWNTFY2 = 0x20000,
    VIDEOMMIOSYNCFLUSH2 = 0x40000,
    VIDEOASCNTXSWITCH2 = 0x80000,
    VIDEOPAGEFAULT2 = 0x100000,
    VIDEOPAVPATTACK2 = 0x200000,
    GUCSHIMERROR = 0x400000,
    GUCDMAINTERROR = 0x800000,
    GUCDMADONE = 0x1000000,
    GUCDOORBELLRANG = 0x2000000,
    GUCIOMMUSENTMSGGUC = 0x4000000,
    GUCSEMAPHORESIGNALED = 0x8000000,
    GUCDISPLAYEVENTRECIEVED = 0x10000000,
    GUCEXECUTIONERROR = 0x20000000,
    GUCINTERRUPTTOHOST = 0x40000000,
    CSTRINVALIDTILEDETECTION = 0x80000000,
}INTERRUPT_UNION_VALUE_2;

typedef enum _INTERRUPT_UNION_VALUE_3
{
    VECSCONTEXTSWITCHINT = 0x1,
    VECSWAITONSEMAPHORE = 0x2,
    WDBOXINTERRUPT = 0x4,
    DPST_HIST_PIPEB = 0x8,
    DPST_PHASEINT_PIPEB = 0x10,
    DPST_HIST_PIPEC = 0x20,
    DPST_PHASEINT_PIPEC = 0x40,
    PIPEA_PLANE1_FLIP_DONE_INT = 0x80,
    PIPEA_PLANE2_FLIP_DONE_INT = 0x100,
    PIPEA_PLANE3_FLIP_DONE_INT = 0x200,
    PIPEB_PLANE1_FLIP_DONE_INT = 0x400,
    PIPEB_PLANE2_FLIP_DONE_INT = 0x800,
    PIPEB_PLANE3_FLIP_DONE_INT = 0x1000,
    PIPEC_PLANE1_FLIP_DONE_INT = 0x2000,
    PIPEC_PLANE2_FLIP_DONE_INT = 0x4000,
    PIPEC_PLANE3_FLIP_DONE_INT = 0x8000,
    PIPEA_PLANE1_FLIP_QUEUE_EMPTY_INT = 0x10000,
    PIPEA_PLANE2_FLIP_QUEUE_EMPTY_INT = 0x20000,
    PIPEA_PLANE3_FLIP_QUEUE_EMPTY_INT = 0x40000,
    PIPEB_PLANE1_FLIP_QUEUE_EMPTY_INT = 0x80000,
    PIPEB_PLANE2_FLIP_QUEUE_EMPTY_INT = 0x100000,
    PIPEB_PLANE3_FLIP_QUEUE_EMPTY_INT = 0x200000,
    PIPEC_PLANE1_FLIP_QUEUE_EMPTY_INT = 0x400000,
    PIPEC_PLANE2_FLIP_QUEUE_EMPTY_INT = 0x800000,
    PIPEC_PLANE3_FLIP_QUEUE_EMPTY_INT = 0x1000000,
    DEMISCSVMWAITDESCCOMPLETE = 0x2000000,
    DEMISCSVMVTDFAULT = 0x4000000,
    DEMISCSVMPRQEVENT = 0x8000000,
    PIPEA_PLANE4_FLIP_DONE_INT = 0x10000000, // BXT
    PIPEB_PLANE4_FLIP_DONE_INT = 0x20000000, // BXT
    DEMISC_GTC_COMBINED_EVENT = 0x40000000,
    VECSWATCHDOGCNTREXCD = 0x80000000,
}INTERRUPT_UNION_VALUE_3;

typedef enum _INTERRUPT_UNION_VALUE_4
{
    // assigning values to match definition in INTERRUPT_ARGS
    MIPIA = 0x1,
    MIPIC = 0x2,
    LPE_PIPEA = 0x4,
    LPE_PIPEB = 0x8,
    ISP = 0x10,
    VED_BLOCK = 0x20,
    VED_POWER = 0x40,
    PIPEA_PLANE4_FLIP_QUEUE_EMPTY_INT = 0x80, // BXT
    PIPEB_PLANE4_FLIP_QUEUE_EMPTY_INT = 0x100, // BXT
    LPE_PIPEC = 0x200,
    CORE_TO_UNCORE_TRAP = 0x400,
    WDBOX_END_OF_FRAME_INTERRUPT = 0X800,
    INTDP_HDMIE = 0x1000,
    INTDP_HDMIE_SP = 0x2000,

    RENDERTDLRETRYINTR = 0x4000, //KBL

    PINNING_CONTEXT_SWITCH = 0x8000,
    PINNING_USER_INTR = 0x10000,
    DEMISC_WD_COMBINED_INTERRUPT = 0x20000,
    PIPEA_UNDERRUN = 0x40000,
    PIPEB_UNDERRUN = 0x80000,
    PIPEC_UNDERRUN = 0x100000,
    PIPEC_PLANE4_FLIP_DONE_INT = 0x200000,
    INVALID_GTT_PAGE_TABLE_ENTRY = 0x400000,
    INVALID_PAGE_TABLE_ENTRY_DATA = 0x800000,
    PIPED_VSYNC = 0x1000000,
    PIPED_VBLANK = 0x2000000,
    INTDP_HDMIF = 0x4000000,
    INTDP_HDMIF_SP = 0x8000000,
    WDBOX2INTERRUPT = 0x10000000,
    WDBOX2_END_OF_FRAME_INTERRUPT = 0x20000000,
    DEMISC_WD2_COMBINED_INTERRUPT = 0x40000000,
}INTERRUPT_UNION_VALUE_4;

typedef enum _INTERRUPT_UNION_VALUE_5
{
    // assigning values to match definition in INTERRUPT_ARGS
    PIPEA_PLANE1_GTT_FAULT_STATUS = 0x1,
    PIPEA_PLANE2_GTT_FAULT_STATUS = 0x2,
    PIPEA_PLANE3_GTT_FAULT_STATUS = 0x4,
    PIPEA_PLANE4_GTT_FAULT_STATUS = 0x8,
    PIPEA_CURSOR_GTT_FAULT_STATUS = 0x10,

    PIPEB_PLANE1_GTT_FAULT_STATUS = 0x20,
    PIPEB_PLANE2_GTT_FAULT_STATUS = 0x40,
    PIPEB_PLANE3_GTT_FAULT_STATUS = 0x80,
    PIPEB_PLANE4_GTT_FAULT_STATUS = 0x100,
    PIPEB_CURSOR_GTT_FAULT_STATUS = 0x200,

    PIPEC_PLANE1_GTT_FAULT_STATUS = 0x400,
    PIPEC_PLANE2_GTT_FAULT_STATUS = 0x800,
    PIPEC_PLANE3_GTT_FAULT_STATUS = 0x1000,
    PIPEC_PLANE4_GTT_FAULT_STATUS = 0x2000,
    PIPEC_CURSOR_GTT_FAULT_STATUS = 0x4000,
    INTDP_HDMIB_SCDC_INTERRUPT = 0x8000,
    INTDP_HDMIC_SCDC_INTERRUPT = 0x10000,
    INTDP_HDMID_SCDC_INTERRUPT = 0x20000,
    INTDP_HDMIE_SCDC_INTERRUPT = 0x40000,
    INTDP_HDMIF_SCDC_INTERRUPT = 0x80000,
    PIPEA_PLANE5_FLIP_DONE_INT = 0x100000,
    PIPEA_PLANE6_FLIP_DONE_INT = 0x200000,
    PIPEA_PLANE7_FLIP_DONE_INT = 0x400000,
    PIPEB_PLANE5_FLIP_DONE_INT = 0x800000,
    PIPEB_PLANE6_FLIP_DONE_INT = 0x1000000,
    PIPEB_PLANE7_FLIP_DONE_INT = 0x2000000,
    PIPEC_PLANE5_FLIP_DONE_INT = 0x4000000,
    PIPEC_PLANE6_FLIP_DONE_INT = 0x8000000,
    PIPEC_PLANE7_FLIP_DONE_INT = 0x10000000,
    PIPED_PLANE5_FLIP_DONE_INT = 0x20000000, // PIPED from Gen11.5
    PIPED_PLANE6_FLIP_DONE_INT = 0x40000000,
    PIPED_PLANE7_FLIP_DONE_INT = 0x80000000,
}INTERRUPT_UNION_VALUE_5;

typedef enum _INTERRUPT_UNION_VALUE_6
{
    // assigning values to match definition in INTERRUPT_ARGS
    PIPEA_PLANE5_GTT_FAULT_STATUS = 0x1,
    PIPEA_PLANE6_GTT_FAULT_STATUS = 0x2,
    PIPEA_PLANE7_GTT_FAULT_STATUS = 0x4,
    PIPEB_PLANE5_GTT_FAULT_STATUS = 0x8,
    PIPEB_PLANE6_GTT_FAULT_STATUS = 0x10,
    PIPEB_PLANE7_GTT_FAULT_STATUS = 0x20,
    PIPEC_PLANE5_GTT_FAULT_STATUS = 0x40,
    PIPEC_PLANE6_GTT_FAULT_STATUS = 0x80,
    PIPEC_PLANE7_GTT_FAULT_STATUS = 0x100,
    PIPED_PLANE5_GTT_FAULT_STATUS = 0x200,
    PIPED_PLANE6_GTT_FAULT_STATUS = 0x400,
    PIPED_PLANE7_GTT_FAULT_STATUS = 0x800,
    PIPED_PLANE1_FLIP_DONE_INT = 0x1000,
    PIPED_PLANE2_FLIP_DONE_INT = 0x2000,
    PIPED_PLANE3_FLIP_DONE_INT = 0x4000,
    PIPED_PLANE4_FLIP_DONE_INT = 0x8000,
    PIPED_PLANE1_GTT_FAULT_STATUS = 0x10000,
    PIPED_PLANE2_GTT_FAULT_STATUS = 0x20000,
    PIPED_PLANE3_GTT_FAULT_STATUS = 0x40000,
    PIPED_PLANE4_GTT_FAULT_STATUS = 0x80000,
    PIPED_CURSOR_GTT_FAULT_STATUS = 0x100000,
    PIPED_DPST_HIST = 0x200000,
    PIPED_CRCERROR = 0x400000,
    PIPED_CRCDONE = 0x800000,
    PIPED_UNDERRUN = 0x1000000,
    AUDIOHDCPREQD = 0x2000000,
    INTDP_HDMIA_SCDC_INTERRUPT = 0x4000000,  // Gen11.5
    PIPEA_VRRDOUBLEBUFFERUPDATE = 0x8000000,
    PIPEB_VRRDOUBLEBUFFERUPDATE = 0x10000000,
    PIPEC_VRRDOUBLEBUFFERUPDATE = 0x20000000,
    PIPED_VRRDOUBLEBUFFERUPDATE = 0x40000000,
}INTERRUPT_UNION_VALUE_6;

typedef enum _INTERRUPT_UNION_VALUE_7
{
    // assigning values to match definition in INTERRUPT_ARGS
    PIPEA_SCANLINE_EVENT = 0x1,
    PIPEB_SCANLINE_EVENT = 0x2,
    PIPEC_SCANLINE_EVENT = 0x4,
    PIPED_SCANLINE_EVENT = 0x8,
    // assigning values to match definition in INTERRUPT_ARGS
    KVMR_REQUESTDISPLAY_INTERRUPT = 0x10,
    KVMR_RELEASEDISPLAY_INTERRUPT = 0x20
}INTERRUPT_UNION_VALUE_7;

// Interrupt Args structure
typedef struct _DD_INTERRUPT_ARGS
{
    INTERRUPT_OPERATION Operation; // Data structure for interrupt operations
    DDU32 PrivateData; // Private Interrupt Data. This will not be used in ILK and GT since enabling/disabling of all interrupts has become much simpler..

    DDU32 PlatformUsesGen11InterruptArchitecture : 1; // Let Event handler code know that all non-display engines are handled by new Selector methods
    DDU32 SelectorInterruptsOccurred : 1; // New for Gen11+  ::  This bit means one of the hierarchical interrupts (has to use selector register) has occurred and needs to be
handled by GEN11+ handler DDU32 LegacyInterruptsOccurred : 1; // New for Gen11+  ::  This bit means use the IntArgs below for handling the interrupts

    DD_IN BOOLEAN HierarchicalInterruptService : 1; // This bit means request for Hirearchial Interrupt services

    DD_IN DDU32 EngineClass;                           // Can re-use ulValue in union
    DD_IN DDU32 EngineIntrpt;                          // Can re-use ulValue1 in union
    DD_PORT_CONNECTOR_TYPE  PortConnectorType;      // This field is valid only for HPD interrupt enabling

    union
    {
        DDU32 Value;
        struct
        {
            //1. Hot Plug Interrupts Definitions - Starts Here

            DDU32    IntegratedCRTInterrupt : 1;    // Bit 0
            DDU32    ReservedBit : 1;    // Bit 1
            DDU32    InterruptReserved1 : 1;    // Bit 2
            DDU32    InterruptReserved2 : 1;    // Bit 3 //From Gen6 onwards,no need to register for this event as sDVO on Port C is disabled..
            DDU32    IntDP_HDMIAInterrupt : 1;    // Bit 4  //New Introduction from ILK onwards
            DDU32    IntDP_HDMIBInterrupt : 1;    // Bit 5
            DDU32    IntDP_HDMICInterrupt : 1;    // Bit 6
            DDU32    IntDP_HDMIDInterrupt : 1;    // Bit 7
            DDU32    IntDP_HDMIA_SPInterrupt : 1;    // Bit 8 //New Introduction from ILK onwards
            DDU32    IntDP_HDMIB_SPInterrupt : 1;    // Bit 9
            DDU32    IntDP_HDMIC_SPInterrupt : 1;    // Bit 10
            DDU32    IntDP_HDMID_SPInterrupt : 1;    // Bit 11

            //1. Hot Plug Interrupts Definitions - Ends Here

            //2. Render Geyserville Interrupts Definitions - Starts Here

            //Render Geyserville Interrupts common till ILK Platform
            DDU32    Ren_Gey_SoftwareCommandCompleteInterrupt : 1; // bit 12 // Render GeyserVille Interrupt
            DDU32    Ren_Gey_EvaluatedFrequencyChangeInterrupt : 1; // bit 13 // Render GeyserVille Interrupt

            //New Render Geyserville Interrupts exists only in ILK
            DDU32    Ren_Gey_AvgBusyThreshold : 1; // bit 14 // Render GeyserVille Interrupt
            DDU32    Ren_Gey_ContinuousBusyThreshold : 1; // bit 15 // Render GeyserVille Interrupt

            //Render Geyserville Common between ILK and GT
            DDU32    Ren_Gey_UpEvaluationIntervalInterrupt : 1; // bit 16 // Render GeyserVille Interrupt
            DDU32    Ren_Gey_DownEvaluationIntervalInterrupt : 1; // bit 17 // Render GeyserVille Interrupt

            //Render Geyserville Introduced from GT
            DDU32    Ren_Gey_Controller_Disable_StateInterrupt : 1; // bit 18 // Render GeyserVille Interrupt

            //2. Render Geyserville Interrupts Definitions - Ends Here

            //3. Basic Render Interrupt Definitions - Starts Here

            DDU32    DebugInterrupt : 1; // Bit 19 Gen4 Onwards
            DDU32    PipeControlNotifyInterrupt : 1; // Bit 20 Gen4 Onwards
            DDU32    RenderUserInterrupt : 1; // Bit 21 Render Cmd UI
            DDU32    RenderMMIOSyncFlushStatus : 1; // Bit 22
            DDU32    RenderWatchDogCounterExcd : 1; // Bit 23 //ILK Onwards
            DDU32    RenderASContextSwitch : 1; // Bit 24 //ILK Onwards
            DDU32    RenderPageFault : 1; // Bit 25 //ILK Onwards

            //3. Basic Render Interrupt Definitions - Ends Here

            //4. Media/Video Interrupt Definitions - Starts Here
            DDU32    VideoUserInterrupt : 1; // Bit 26 Gen4 Onwards
            DDU32    VideoDecPipelineCntrExceed : 1; // Bit 27 Gen4 Onwards..Same as Video Command Streamer WatchDog Counter Exceeded in GT
            //Following are valid from GT
            DDU32    VideoMIFlush_DWNotify : 1; // Bit 28
            DDU32    VideoMMIOSyncFlushStatus : 1; // Bit 29
            DDU32    VideoASContextSwitch : 1; // Bit 30
            DDU32    VideoPageFault : 1; // Bit 31

            //4. Media/Video Interrupt Definitions - Ends Here
        };
    };

    union
    {
        DDU32 Value1;
        struct
        {
            //5. Remaining Power Conservation Interrupt Starts here
            DDU32    LBPC_PipeAInterrupt : 1;    // Bit 0 - crestline and after. Doesnt exist from ILK Onwards
            DDU32    LBPC_PipeBInterrupt : 1;    // Bit 1 - crestline and after. Doesnt exist from ILK Onwards
            DDU32    DPST_HistInterrupt : 1;    // Bit 2 - crestline and after
            DDU32    DPST_PhaseInInterrupt : 1;    // Bit 3 - crestline and after

            //Valid from GT Onwards
            DDU32    PCUDriverMBEvent : 1; // Bit 4
            DDU32    PCRenderFreqDownwardDuringRC6Timeout : 1; // Bit 5
            DDU32    PC_RPUpThresholdIntr : 1; // Bit 6
            DDU32    PC_RPDownThresholdIntr : 1; // Bit 7

            //5. Remaining Power Conservation Interrupt Ends here

            //6. Blitter Interrupts from GT Onwards Starts here

            DDU32    BlitterASContextSwitch : 1; // Bit 8
            DDU32    BlitterMIFlush_DWNotify : 1; // Bit 9
            DDU32    BlitterMMIOSyncFlushStatus : 1; // Bit 10
            DDU32    BlitterMI_User_Interrupt : 1; // Bit 11
            DDU32    BlitterPageFault : 1; // Bit 12
            //6. Blitter Interrupts from GT Onwards Ends here

            //7. Misc Interrupts Category Starts here
            DDU32    VSync_PipeAInterrupt : 1;    // Bit 13 //Not Required
            DDU32    VSync_PipeBInterrupt : 1;    // Bit 14 //Not Required
            DDU32    VBlank_PipeAInterrupt : 1;    // Bit 15
            DDU32    VBlank_PipeBInterrupt : 1;    // Bit 16
            DDU32    GSESystemLevel : 1;    // Bit 17  Valid from ILK Replacement for ASLE Interrupt
            DDU32    VblankTPV : 1;    // BIT 18 //Used for TPV Vblank Interrupt
            DDU32    ASLEInterrupt : 1;    // Bit 19  Need to remove Once MP Cleans up the ASLE INterrupt Stuff
            DDU32    AllFirstLevelInterrupts : 1;    // BIT 20 //Used for Enabling/Disabling of Interrupts..

            //7. Misc Interrupts Category Ends here

            //8. New added Interrupts
            DDU32    SpritePlaneAFlipDoneInterrupt : 1;    // BIT 21 //Used for Enabling/Disabling of Sprite Plane A Flip Done Interrupt..
            DDU32    SpritePlaneBFlipDoneInterrupt : 1;    // BIT 22 //Used for Enabling/Disabling of Sprite Plane B Flip Done Interrupt..

            DDU32    VSync_PipeCInterrupt : 1;    // BIT 23
            DDU32    VBlank_PipeCInterrupt : 1;    // BIT 24
            DDU32    SpritePlaneCFlipDoneInterrupt : 1;    // BIT 25

            DDU32    AudioHDCPRequestInterruptA : 1;    // BIT 26 //Audio HDCP request for transcoder A
            DDU32    AudioHDCPRequestInterruptB : 1;    // BIT 27 //Audio HDCP request for transcoder B
            DDU32    AudioHDCPRequestInterruptC : 1;    // BIT 28 //Audio HDCP request for transcoder C
            DDU32    AudioHDCPRequestInterruptD : 1;    // BIT 29 //Audio HDCP request for pre ilk platforms

            DDU32   PerfMonBufferHalfFullInterrupt : 1;    // BIT 30

            DDU32   Reserved_Bit31 : 1;    // Bit 31
        };
    };

    union
    {
        DDU32 Value2;
        struct
        {
            // This sections contains error/debug status bits
            DDU32 FIFOUnderrun_PipeAInterrupt : 1; // bit 0
            DDU32 CRC_Error_PipeAInterrupt : 1; // bit 1
            DDU32 CRC_Done_PipeAInterrupt : 1; // bit 2

            DDU32 FIFOUnderrun_PipeBInterrupt : 1; // bit 3
            DDU32 CRC_Error_PipeBInterrupt : 1; // bit 4
            DDU32 CRC_Done_PipeBInterrupt : 1; // bit 5

            DDU32 FIFOUnderrun_PipeCInterrupt : 1; // bit 6
            DDU32 CRC_Error_PipeCInterrupt : 1; // bit 7
            DDU32 CRC_Done_PipeCInterrupt : 1; // bit 8

            // VE (Video Enhancement) Interrupt Definitions - Starts Here - Valid from Gen7_5 (HSW+) onward
            DDU32 VEUserInterrupt : 1; // bit 9
            DDU32 VEMMIOSyncFlushStatus : 1; // bit 10
            DDU32 VECmdParserMasterError : 1; // bit 11
            DDU32 VEMIFlush_DWNotify : 1; // bit 12
            // VE (Video Enhancement) Interrupt Definitions - Ends Here

            // other interrupt bits that don't fit into the previous dwords
            DDU32 RenderParityError : 1; // Bit 13 Gen7 Onwards

            DDU32 VideoPavpUnsolicitedAttack : 1; // Bit 14 Gen7 Onwards

            //Below are valid from BDW
            DDU32 VideoUserInterrupt2 : 1; // Bit 15
            DDU32 VideoDecPipelineCntrExceed2 : 1; // Bit 16
            DDU32 VideoMIFlush_DWNotify2 : 1; // Bit 17
            DDU32 VideoMMIOSyncFlushStatus2 : 1; // Bit 18
            DDU32 VideoASContextSwitch2 : 1; // Bit 19
            DDU32 VideoPageFault2 : 1; // Bit 20
            DDU32 VideoPavpUnsolicitedAttack2 : 1; // Bit 21

            DDU32 GuCSHIMError : 1;    // bit 22
            DDU32 GuCDMAINTError : 1;    // bit 23
            DDU32 GuCDMADone : 1;    // bit 24
            DDU32 GuCDoorBellRang : 1;    // bit 25
            DDU32 GuCIOMMUSentMsgtoGuc : 1;    // bit 26
            DDU32 GuCSemaphoreSignaled : 1;    // bit 27
            DDU32 GuCDisplayEventRecieved : 1;    // bit 28
            DDU32 GuCExecutionError : 1;    // bit 29
            DDU32 GuCInterruptToHost : 1;    // bit 30

            DDU32 CSTRInvalidTileDetection : 1;    // bits 31
        };
    };

    union
    {
        DDU32 Value3;
        struct
        {
            // This sections contains VEC/WiDi interrupts
            DDU32 VECSContextSwitchInterrupt : 1; // bit 0
            DDU32 VECSWaitOnSemaphore : 1; // bit 1
            DDU32 WDBoxInterrupt : 1; // bit 2
            DDU32 DPST_HistInterruptPipeB : 1;// bit 3
            DDU32 DPST_PhaseInInterruptPipeB : 1; // bit 4
            DDU32 DPST_HistInterruptPipeC : 1;// bit 5
            DDU32 DPST_PhaseInInterruptPipeC : 1; // bit 6

            DDU32 PipeA_Plane1FlipDoneInterrupt : 1; //bit 7
            DDU32 PipeA_Plane2FlipDoneInterrupt : 1; //bit 8
            DDU32 PipeA_Plane3FlipDoneInterrupt : 1; //bit 9

            DDU32 PipeB_Plane1FlipDoneInterrupt : 1; //bit 10
            DDU32 PipeB_Plane2FlipDoneInterrupt : 1; //bit 11
            DDU32 PipeB_Plane3FlipDoneInterrupt : 1; //bit 12

            DDU32 PipeC_Plane1FlipDoneInterrupt : 1; //bit 13
            DDU32 PipeC_Plane2FlipDoneInterrupt : 1; //bit 14
            DDU32 PipeC_Plane3FlipDoneInterrupt : 1; //bit 15

            DDU32 PipeA_Plane1FlipQueueEmptyInterrupt : 1; //bit 16
            DDU32 PipeA_Plane2FlipQueueEmptyInterrupt : 1; //bit 17
            DDU32 PipeA_Plane3FlipQueueEmptyInterrupt : 1; //bit 18

            DDU32 PipeB_Plane1FlipQueueEmptyInterrupt : 1; //bit 19
            DDU32 PipeB_Plane2FlipQueueEmptyInterrupt : 1; //bit 20
            DDU32 PipeB_Plane3FlipQueueEmptyInterrupt : 1; //bit 21

            DDU32 PipeC_Plane1FlipQueueEmptyInterrupt : 1; //bit 22
            DDU32 PipeC_Plane2FlipQueueEmptyInterrupt : 1; //bit 23
            DDU32 PipeC_Plane3FlipQueueEmptyInterrupt : 1; //bit 24

            DDU32 DEMiscSVMWaitDescriptorCompleted : 1; // bit 25
            DDU32 DEMiscSVMVTDFault : 1; // bit 26
            DDU32 DEMiscSVMPRQEvent : 1; // bit 27

            DDU32 PipeA_Plane4FlipDoneInterrupt : 1; // bit 28
            DDU32 PipeB_Plane4FlipDoneInterrupt : 1; // bit 29
            DDU32 PSR2GTCLockLoss : 1; // bit 30
            DDU32 VECSWatchDogCounterExcd : 1; // bit 31
        };
    };
    union
    {
        DDU32 Value4;
        struct
        {
            DDU32 MIPIAInterrupt : 1; // bit 0
            DDU32 MIPICInterrupt : 1; // bit 1
            DDU32 LPEPipeAInterrupt : 1; // bit 2
            DDU32 LPEPipeBInterrupt : 1; // bit 3

            DDU32 ISPInterrupt : 1; // bit 4
            DDU32 VEDBlockInterrupt : 1; // bit 5
            DDU32 VEDPowerInterrupt : 1; // bit 6
            DDU32 PipeA_Plane4FlipQueueEmptyInterrupt : 1; // bit 7

            DDU32 PipeB_Plane4FlipQueueEmptyInterrupt : 1; // bit 8
            DDU32 LPEPipeCInterrupt : 1; // bit 9
            DDU32 GTPMCoreToUncoreTrapInterrupt : 1; //bit 10
            DDU32 WDBoxEndofFrameInterrupt : 1; //bit 11 corresponds to WDBOX_END_OF_FRAME_INTERRUPT = 0X800, in INTERRUPT_UNION_VALUE_4

            DDU32 IntDP_HDMIEInterrupt : 1; // Bit 12// skl ddi - e hot plug interrupt
            DDU32 IntDP_HDMIE_SPInterrupt : 1; // Bit 13
            DDU32 RenderTDLRetryInterrupt : 1; // bit 14
            DDU32 PinningContextSwitch : 1; // Bit 15
            DDU32 PinningUserInterrupt : 1; // Bit 16
            DDU32 DEMisc_WDCombinedInterrupt : 1; // bit 17 corresponds to DEMISC_WD_COMBINED_INTERRUPT  = 0x20000, in INTERRUPT_UNION_VALUE_4

            DDU32 PipeA_Underrun : 1; // bit 18
            DDU32 PipeB_Underrun : 1; // bit 19
            DDU32 PipeC_Underrun : 1; // bit 20
            DDU32 PipeC_Plane4FlipDoneInterrupt : 1; // bit 21
            DDU32 InvalidGTTPageTableEntry : 1; // bit 22
            DDU32 InvalidPageTableEntryData : 1; // bit 23
            DDU32 VSync_PipeDInterrupt : 1; // BIT 24
            DDU32 VBlank_PipeDInterrupt : 1; // BIT 25
            DDU32 IntDP_HDMIFInterrupt : 1; // Bit 26// ddi - f hot plug interrupt
            DDU32 IntDP_HDMIF_SPInterrupt : 1; // Bit 27
            DDU32 WDBox2Interrupt : 1; // bit 28
            DDU32 WDBox2EndofFrameInterrupt : 1; // bit 29
            DDU32 DEMisc_WD2CombinedInterrupt : 1; // bit 30
            DDU32 Reserved_Bits31_ulValue4 : 1; // bit 31
        };
    };
    union
    {
        DDU32 Value5;
        struct
        {
            DDU32 PipeA_Plane1GTTFaultStatus : 1; //bit 0
            DDU32 PipeA_Plane2GTTFaultStatus : 1; //bit 1
            DDU32 PipeA_Plane3GTTFaultStatus : 1; //bit 2
            DDU32 PipeA_Plane4GTTFaultStatus : 1; //bit 3
            DDU32 PipeA_CursorGTTFaultStatus : 1; //bit 4

            DDU32 PipeB_Plane1GTTFaultStatus : 1; //bit 5
            DDU32 PipeB_Plane2GTTFaultStatus : 1; //bit 6
            DDU32 PipeB_Plane3GTTFaultStatus : 1; //bit 7
            DDU32 PipeB_Plane4GTTFaultStatus : 1; //bit 8
            DDU32 PipeB_CursorGTTFaultStatus : 1; //bit 9

            DDU32 PipeC_Plane1GTTFaultStatus : 1; //bit 10
            DDU32 PipeC_Plane2GTTFaultStatus : 1; //bit 11
            DDU32 PipeC_Plane3GTTFaultStatus : 1; //bit 12
            DDU32 PipeC_Plane4GTTFaultStatus : 1; //bit 13
            DDU32 PipeC_CursorGTTFaultStatus : 1; //bit 14

            DDU32 IntDP_HDMIB_SCDCInterrupt : 1; //bit 15
            DDU32 IntDP_HDMIC_SCDCInterrupt : 1; //bit 16
            DDU32 IntDP_HDMID_SCDCInterrupt : 1; //bit 17
            DDU32 IntDP_HDMIE_SCDCInterrupt : 1; //bit 18
            DDU32 IntDP_HDMIF_SCDCInterrupt : 1; //bit 19

            DDU32 PipeA_Plane5FlipDoneInterrupt : 1; // bit 20
            DDU32 PipeA_Plane6FlipDoneInterrupt : 1; // bit 21
            DDU32 PipeA_Plane7FlipDoneInterrupt : 1; // bit 22
            DDU32 PipeB_Plane5FlipDoneInterrupt : 1; // bit 23
            DDU32 PipeB_Plane6FlipDoneInterrupt : 1; // bit 24
            DDU32 PipeB_Plane7FlipDoneInterrupt : 1; // bit 25
            DDU32 PipeC_Plane5FlipDoneInterrupt : 1; // bit 26
            DDU32 PipeC_Plane6FlipDoneInterrupt : 1; // bit 27
            DDU32 PipeC_Plane7FlipDoneInterrupt : 1; // bit 28
            DDU32 PipeD_Plane5FlipDoneInterrupt : 1; // bit 29
            DDU32 PipeD_Plane6FlipDoneInterrupt : 1; // bit 30
            DDU32 PipeD_Plane7FlipDoneInterrupt : 1; // bit 31
        };
    };
    union
    {
        DDU32 Value6;
        struct
        {
            DDU32 PipeA_Plane5GTTFaultStatus : 1; //bit 0
            DDU32 PipeA_Plane6GTTFaultStatus : 1; //bit 1
            DDU32 PipeA_Plane7GTTFaultStatus : 1; //bit 2
            DDU32 PipeB_Plane5GTTFaultStatus : 1; //bit 3
            DDU32 PipeB_Plane6GTTFaultStatus : 1; //bit 4
            DDU32 PipeB_Plane7GTTFaultStatus : 1; //bit 5
            DDU32 PipeC_Plane5GTTFaultStatus : 1; //bit 6
            DDU32 PipeC_Plane6GTTFaultStatus : 1; //bit 7
            DDU32 PipeC_Plane7GTTFaultStatus : 1; //bit 8
            DDU32 PipeD_Plane5GTTFaultStatus : 1; //bit 9
            DDU32 PipeD_Plane6GTTFaultStatus : 1; //bit 10
            DDU32 PipeD_Plane7GTTFaultStatus : 1; //bit 11
            DDU32 PipeD_Plane1FlipDoneInterrupt : 1; //bit 12
            DDU32 PipeD_Plane2FlipDoneInterrupt : 1; //bit 13
            DDU32 PipeD_Plane3FlipDoneInterrupt : 1; //bit 14
            DDU32 PipeD_Plane4FlipDoneInterrupt : 1; //bit 15
            DDU32 PipeD_Plane1GTTFaultStatus : 1; //bit 16
            DDU32 PipeD_Plane2GTTFaultStatus : 1; //bit 17
            DDU32 PipeD_Plane3GTTFaultStatus : 1; //bit 18
            DDU32 PipeD_Plane4GTTFaultStatus : 1; //bit 19
            DDU32 PipeD_CursorGTTFaultStatus : 1; //bit 20
            DDU32 PipeD_DPST_HistInterrupt : 1;// bit 21
            DDU32 CRC_Error_PipeDInterrupt : 1; // bit 22
            DDU32 CRC_Done_PipeDInterrupt : 1; // bit 23
            DDU32 PipeD_Underrun : 1; // bit 24
            DDU32 AudioHdcpRequestInterruptD : 1; // bit 25
            DDU32 IntDP_HDMIA_SCDCInterrupt : 1; // bit 26
            DDU32 PIPEA_VRRDoubleBufferUpdate : 1; // bit 27
            DDU32 PIPEB_VRRDoubleBufferUpdate : 1; // bit 28
            DDU32 PIPEC_VRRDoubleBufferUpdate : 1; // bit 29
            DDU32 PIPED_VRRDoubleBufferUpdate : 1; // bit 30
            DDU32 Reserved_Bits31_ulValue6 : 1; // bits 31
        };
    };
    union
    {
        DDU32 Value7;
        struct
        {
            DDU32 PipeA_ScanLineEvent : 1; //bit 0
            DDU32 PipeB_ScanLineEvent : 1; //bit 1
            DDU32 PipeC_ScanLineEvent : 1; //bit 2
            DDU32 PipeD_ScanLineEvent : 1; //bit 3
            DDU32 KVMR_RequestDisplayInterrupt : 1; // bit 4
            DDU32 KVMR_ReleaseDisplayInterrupt : 1; // bit 5
        };
    };
} DD_INTERRUPT_ARGS;*/

// Arrange Plane numbers in ascending order starting from Plane 1, they will be accessed using bitwise operation (1 << PlaneIndex) in HAL Plane.
typedef union _DD_FLIP_DONE_STATUS {
    DDU32 Value;
    struct
    {
        DDU32 Plane1FlipDoneStatus : 1;
        DDU32 Plane2FlipDoneStatus : 1;
        DDU32 Plane3FlipDoneStatus : 1;
        DDU32 Plane4FlipDoneStatus : 1;
        DDU32 Plane5FlipDoneStatus : 1;
        DDU32 Plane6FlipDoneStatus : 1;
        DDU32 Plane7FlipDoneStatus : 1;
    };
} DD_FLIP_DONE_STATUS;
typedef struct _SB_INTERRUPT_ARGS DD_INTERRUPT_ARGS;
//----------------------------------------------------------------------------
//
// Data Structure for Interrupt operations -- END
//
//----------------------------------------------------------------------------

#define PMIC_NAME L"PMICSPBTEST"
#define PMIC_SYMBOLIC_NAME L"\\DosDevices\\" PMIC_NAME

/*typedef struct _IOCTL_ARGS
{
    DDU32            *pInputBuffer;
    DDU32            InputBufferLength;
    DDU32            *pOutputBuffer;
    DDU32            OutputBufferLength;
    PDDWSTR          pDeviceName;
    DDU32            DesiredAccess;
    DDU32            FileAttributes;
    DDU32            CreateDisposition;
    DDU32            CreateOptions;
    DDU32            IoControlCode;
    DDU64_PTR        BytesReturned;
} IOCTL_ARGS;*/

typedef struct _DD_SURFACE_DIMENSION_INFO
{
    DDU32 YWidth;
    DDU32 YHeight;
    DDU32 UVWidth;
    DDU32 UVHeight;
} DD_SURFACE_DIMENSION_INFO;

// Based on DP1.2 Spec. Total Number of Links is 15
#define DD_MAX_LINK_COUNT 15

// As every Address for a link requires 4 Bits, therefore total 14 links (MAX_LINK_COUNT - 1, since for 1st link RAD is not required) would require 56 bits.
// Hence total 7 Bytes
#define DD_MAX_BYTES_RAD ((DD_MAX_LINK_COUNT) / 2)
typedef struct _DD_DP_RELATIVE_ADDRESS
{
    DDU8 TotalLinkCount;

    // If TotalLinkCount is 1 then Relative Address should have zero value at all the indexes..

    // If the TotalLinkCount is Even then index from 0 till (TotalLinkCount/2 - 1) (apart from the Upper Nibble of last index) is a Valid Address, .

    // If the TotalLinkCount is Odd then index from 0 till (TotalLinkCount)/2 - 1) will be a Valid Address

    // Hence for both odd/even TotalLinkCount, we can use Index from 0 till (TotalLinkCount/2 - 1)

    DDU8 Address[DD_MAX_BYTES_RAD];
} DD_DP_RELATIVE_ADDRESS;

#define DD_MAX_AUX_BUFSIZE 0x0200

// Based on DP1.2 Spec. Total Number of Links is 15
#define MAX_LINK_COUNT 15

// As every Address for a link requires 4 Bits, therefore total 14 links (MAX_LINK_COUNT - 1, since for 1st link RAD is not required) would require 56 bits.
// Hence total 7 Bytes
#define MAX_BYTES_RAD ((MAX_LINK_COUNT) / 2)

typedef enum _DD_AUX_I2C_OPERATIONS
{
    DD_OPERATION_UNKNOWN = 0,
    DD_NATIVE_AUX, // DPCD
    DD_I2C_AUX,
    DD_I2C,
    DD_ATOMICI2C,
    DD_REMOTE_DPCD,
    DD_I2C_MOT
} DD_AUX_I2C_OPERATIONS;

typedef struct _DD_I2C_AUX_ARGS
{
    DD_AUX_I2C_OPERATIONS Operation;
    BOOLEAN               Write; // 0-Read,1-Write
    DD_PORT_TYPE          Port;
    DDU32                 Address;                   // 7bit I2c address or DPCD address
    DDU32                 Index;                     // used in case of I2C [2byte Offset]
    DDU8                  RelAddress[MAX_BYTES_RAD]; // used only in case of Remote DPCD
    DDU32                 ReadBytes;                 // Bytes to read only in case of Atomic I2C
    DDU32                 WriteBytes;                // Bytes to write only in case of Atomic I2C
    DDU32                 DataLength;
    DDU8                  Data[DD_MAX_AUX_BUFSIZE];
} DD_I2C_AUX_ARGS;

typedef union _DD_RAD_BYTE_ST {
    DDU8 Data;
    struct
    {
        DDU8 LowerRAD : 4;
        DDU8 HigherRAD : 4;
    };
} DD_RAD_BYTE_ST;

typedef enum _DD_HDCP_AUTH_STATUS
{
    DD_HDCP2_UNAUTHENTICATED = 1,
    DD_HDCP2_AUTH_IN_PROGRESS,
    DD_HDCP2_AUTH_COMPLETE,
    DD_HDCP2_LINKINTEGRITY_FAILED,
} DD_HDCP_AUTH_STATUS;

typedef struct _DD_HDCP_AUTH_DATA
{
    DD_HDCP_AUTH_STATUS HDCPAuthStatus;               // indicates the current status of Authentication
    BOOLEAN             HDCPAuthenticationPass;       // indicates whether HDCP Auth is successfully done for the display or not. Valid only if is bHDCPSupported TRUE
    DDU8                ReceiverId[RECEIVER_ID_SIZE]; // 40 bit long receiver id extracted from CertRx
    // DDU8   ucVersion;                     //The HDCP version 2.0 or 2.1
    DDU8    MajorVersion;        // The HDCP version 2.0 or 2.1
    DDU8    MinorVersion;        // The HDCP version 2.0 or 2.1
    BOOLEAN Repeater;            // Boolean indicating whether the Remote Display is Repeater or not
    BOOLEAN HasHDCP2_0_Repeater; // BOOLEAN indicating whther the downstream topology has HDCP 2_0 Repeater
    BOOLEAN HasHDCP1_Device;     // BOOLEAN indicating whther the downstream topology has HDCP 1 Device
    DDU32   RepeaterDeviceCount; // Number of Repeaters in the down stream. Valid only if bRepeater is TRUE
    DDU8    ReceiverIDList[MAX_DEVICE_COUNT *
                        RECEIVER_ID_SIZE]; // List of Receiver Ids each of 40 bit long. Max number of repeaters can be 31 as per HDCP 2.0 spec. Valid only if bRepeater is TRUE
    DDU32   TypeStatus;                       // The last successful Type notification. Default value is 0
} DD_HDCP_AUTH_DATA;

// Structure to return EDID information of the TPV device along with with few other Device capabilities.
typedef struct _DD_HDCP_ARGS_
{
    DDU32             DisplayUid;
    BOOLEAN           IsHDCPSupported;
    DD_HDCP_AUTH_DATA HDCPAuthData;
} DD_HDCP_ARGS_;

typedef enum
{
    DD_HDCPSTATUS_LINKINTEGRITY, // To pass link integrity state to KMD
    DD_HDCPSTATUS_AUTH_PROGRESS, // To indicates if authentication is in prgress
    DD_HDCPSTATUS_AUTH_DATA      // To pass HDCP 2.0 authentication data
} DD_HDCP_STATUS_TYPE;

// typedef enum _HDCP_AUTH_LEVEL
//{
//    HDCP_NO_AUTH = 0,
//    HDCP_AUTH_TYPE_ZERO,
//    HDCP_AUTH_TYPE_ONE,
//    MAX_HDCP_AUTH_TYPE
//}HDCP_AUTH_LEVEL;

typedef enum _DD_HDCP_MSG_CMD
{
    DD_HDCP_MSG_CMD_NULL  = 0x0000, // Does no command
    DD_HDCP_MSG_CMD_READ  = 0x0001, // Reads Data from an HDCP Bus Device
    DD_HDCP_MSG_CMD_WRITE = 0x0002, // Writes Data out on the HDCP Bus Device
} DD_HDCP_MSG_CMD;

#define MAX_HDCP_MSG_SIZE 534    // Max message size in HDCP 2.2
typedef struct _DD_HDCP_MSG_ARGS // merge with DD_I2C args
{
    DDU32           ChildUid;
    DD_PORT_TYPE    Port; //
    DD_HDCP_MSG_CMD Command;
    DDU32           DataSize;
    DDU32           DataProcessed;
    union {
        DDU8 *pMsgID;
        DDU8 *pBuffer; // [MAX_HDCP_MSG_SIZE + 1];
    };
} DD_HDCP_MSG_ARGS;

typedef struct _DD_HDCP_RX_STATUS_ARGS
{
    DD_PORT_TYPE Port;
    DDU32        Protocol;
    BOOLEAN      IsLinkIntegrityFailed;
    BOOLEAN      IsReAuthRequired;
    BOOLEAN      RxReady;
} DD_HDCP_RX_STATUS_ARGS;

typedef struct _DD_HDCP_AUTH_STATUS_ARGS
{
    DDU32                ChildUid;
    DD_TARGET_DESCRIPTOR TgtDesc;
    PIPE_ID              Pipe;
    DDU32                Protocol;
    DD_HDCP_AUTH_DATA    AuthData;
} DD_HDCP_AUTH_STATUS_ARGS;

typedef enum _DD_HDCP_2_ADAPTATION
{
    INVALID_HDCP_2_ADAPTATION = 0,
    HDCP2_2_HDMI_ADAPTATION,
    HDCP2_2_DP_ADAPTATION,
    HDCP_2_2_IF_IND_ADAPTATION, // Interface Independent Adaptation used for WiGig and WiDi
    HDCP_2_2_EXT_SOLUTION,      // LSPCON, CPDP kind of external solutions

    MAX_HDCP_2_ADAPTATION
} DD_HDCP2_ADAPTATION;

typedef struct _DD_HDCP_SRVC_REQUEST
{
    DDU32               ChildUid; // Unique display ID (cannot accept generic types)
    DD_PORT_TYPE        Port;
    DD_HDCP2_ADAPTATION Protocol; // Which HDCP adaptation protocol to be used
    BOOLEAN             RepeaterAuth;
    DDU32               Level;
    DDU32               StreamCount;
} DD_HDCP_SRVC_REQUEST;

typedef struct _DD_NOTIFY_OPM_ARGS
{
    BOOLEAN IsAudioTrigger;
    DDU32   DisplayUID;
    BOOLEAN IsDisplayAttached;
    DDU32   PathIndex;
} DD_NOTIFY_OPM_ARGS;

typedef struct _DD_GET_VIDPN_DETAILS
{
    BOOLEAN QueryBasedOnPipe;
    PIPE_ID PipeId;
    DDU32   DisplayUID;
    DDU32   PathIndex;
} DD_GET_VIDPN_DETAILS;

// PERIODIC FRAME NOTIFY related
// Maintain a sorted ring of elements
#define DD_MAX_PERIOIDIC_FRAME_ELEMENTS 8 // Per Msft

typedef struct _DD_PERIODIC_FRAME_DATA
{
    DDU32 Scanline;       // Scanline number for trigger
    DDU32 NotificationId; // ID to return to OS
    DDU32 VidPnTargetId;  // VidPnTargetId to return to OS.
                          // Each element needs to contain the TargetID within it since during DxgkDdiDestroyPeriodicFrameNotification, \
                                             // we get only the pointer to the Element to be destroyed, and no separate TargetId
} DD_PERIODIC_FRAME_DATA;

typedef struct _DD_PERIODIC_FRAME_ELEM
{
    DD_PERIODIC_FRAME_DATA          Data;
    struct _DD_PERIODIC_FRAME_ELEM *pPrevElem; // Previous element in ring
    struct _DD_PERIODIC_FRAME_ELEM *pNextElem; // Next element in ring
} DD_PERIODIC_FRAME_ELEM;

typedef struct _DD_PERIOIDIC_FRAME_CURRENT_ELEM_PARAMS
{
    DD_PERIODIC_FRAME_ELEM *pCurrent;                       // The current element in Ring that will trigger the next interrupt
    BOOLEAN                 Invalid;                        // If set, it means that Current Elem was Destroyed and pCurrent points to Current Element's next Element
    DDU32                   ScanlineOfDestroyedCurrentElem; // To be looked at only if Invalid = 1,
                                          // since in that case pCurrent will point to pCurrent->pNextElem, original Current Element has been Destroyed on OS Request
} DD_PERIOIDIC_FRAME_CURRENT_ELEM_PARAMS;

typedef struct _DD_PERIODIC_FRAME_RING
{
    DD_PERIODIC_FRAME_ELEM *pHead;   // The "start" of the ring, really the element with min scanline
    DDU8                    NumElem; // Number of elements in Ring
} DD_PERIODIC_FRAME_RING;

typedef struct _DD_PERIODIC_FRAME_ELEM_CREATE_ARGS
{
    DDU32 TargetId;       // [in] The output that the notification will be attached to
    DDU64 TimeIn100ns;    // [in] Represents an offset before the VSync.
                          // The Time value may not be longer than a VSync interval.
                          // In units of 100ns.
    DDU32 NotificationId; // [in] Id that represents this instance of the notification
                          // used to identify which interrupt has fired.
    HANDLE hNotification; // [out] Handle to the notification object, later used to destroy
} DD_PERIODIC_FRAME_CREATE_ARGS;

typedef struct _DD_ACPI_DSM_INOUT_ARGS
{
    DD_IN DDU32 DsmFuncCode;          // DSM function code
    DD_IN DDU32 AcpiInputSize;        // DSM input argument size
    DD_IN void *pAcpiInputArgument;   // DSM input argument
    DD_IN DDU32  AcpiOutputSize;      // DSM output argument size
    DD_OUT void *pAcpiOutputArgument; // DSM output argument
} DD_ACPI_DSM_INOUT_ARGS;

typedef struct _DD_ACPI_BCL_INOUT_ARGS
{
    DD_IN DDU32 TargetId; // DSM input argument size
} DD_ACPI_BCL_INOUT_ARGS;

typedef enum _DD_ACPI_METHOD
{
    ACPI_METHOD_DOD = 0,
    ACPI_METHOD_BCL,
    ACPI_METHOD_DSM,
} DD_ACPI_METHOD;

typedef struct _DD_ACPI_EVAL_METHOD_INOUT_ARGS
{
    DD_IN DD_ACPI_METHOD MethodName;
    union {
        DD_IN DD_ACPI_DSM_INOUT_ARGS DsmInOutArgs; // DSM input args
        DD_IN DD_ACPI_BCL_INOUT_ARGS BclInOutArgs; // Backlight Control Method input args
    };

    DD_IN_OUT DDU32 Count;       // OUT param when pass 1, IN param when pass 2
    DD_OUT DDU32 Length;         // Valid in pass 2 case to calculate size of output buffer
    DD_IN_OUT DDU32 *pDataArray; // NULL when pass 1, non-NULL when pass 2
} DD_ACPI_EVAL_METHOD_INOUT_ARGS;
// Opregion defined error messages
typedef enum _OPREGION_NRDY_REASON
{
    ACPI_FAILURE_DRIVER_NOT_INITIALIZED = 0x00,
    ACPI_FAILURE_3D_APP_RUNNING,
    ACPI_FAILURE_OVERLAY_ACTIVE,
    ACPI_FAILURE_FSDOS_ACTIVE,
    ACPI_FALIURE_RESOURCE_IN_USE,
    ACPI_FALIURE_DRIVER_IN_LOW_POWER_TRANSITION,
    ACPI_FAILURE_EXTENDED_DESKTOP_ACTIVE,
    ACPI_FAILURE_FATAL,

    // Don't add driver defined err messages here!

    // Driver defined error messages
    ACPI_FAILURE_LVDS_PWR_STATE_CHANGE_FAILED = 0x101,
    ACPI_FAILURE_NO_CHANGE_IN_CONFIG,
    ACPI_FAILURE_GET_NEXT_CONFIG_FROM_EM_FAILED,
    ACPI_FAILURE_GET_EM_HOTKEY_LIST_FAILED,
    ACPI_FAILURE_TURN_OFF_ALL_DISPLAYS,
    ACPI_FAILURE_GET_DISP_INFO_FAILED,
    ACPI_FAILURE_INVALID_ASL_NOTIFICATION,
    ACPI_FAILURE_INVALID_BUFFER_SIZE,
    ACPI_FAILURE_EM_NOT_INITIALIZED,
    ACPI_FAILURE_TMM_ACTIVE
} OPREGION_NRDY_REASON;

// Color related
typedef enum _DD_COLOR_BLENDING_MODE
{
    DD_COLOR_BLENDING_MODE_UNKNOWN           = 0, // Unknown or unsupported blending with given plane configurations
    DD_COLOR_BLENDING_MODE_SRGB_NONLINEAR    = 1, // Legacy blending
    DD_COLOR_BLENDING_MODE_2020RGB_LINEAR    = 2, // BT2020 and HDR plane blending
    DD_COLOR_BLENDING_MODE_2020RGB_NONLINEAR = 3, // BT2020 and HDR plane blending
    DD_COLOR_BLENDING_MODE_SRGB_LINEAR       = 4, // Cases (rare) where blending in BT2020 space is not possible
    DD_COLOR_BLENDING_MODE_MAX
} DD_COLOR_BLENDING_MODE;

typedef enum _DD_CSC_RANGE_CONVERSION_TYPE
{
    DD_CSC_RANGE_CONVERSION_TYPE_NONE = 0,
    DD_CSC_RANGE_CONVERSION_RGB_LR_TO_RGB_FR, // LR: Limited Range, FR:Full Range
    DD_CSC_RANGE_CONVERSION_YCBCR_LR_TO_RGB_FR,
    DD_CSC_RANGE_CONVERSION_RGB_FR_TO_RGB_LR,
    DD_CSC_RANGE_CONVERSION_RGB_FR_TO_YCBCR_LR,
    DD_CSC_RANGE_CONVERSION_RGB_FR_TO_RGB_FR
} DD_CSC_RANGE_CONVERSION_TYPE;

typedef enum _DD_CSC_MODE_CONVERSION_TYPE
{
    DD_CSC_MODE_CONVERSION_NONE = 0,
    DD_CSC_MODE_CONVERSION_RGB_TO_YUV,
    DD_CSC_MODE_CONVERSION_YUV_TO_RGB,
    DD_CSC_MODE_CONVERSION_RGB_TO_RGB
} DD_CSC_MODE_CONVERSION_TYPE;

typedef enum _DD_BLENDING_MODE_TRIGGER
{
    DD_BLENDING_MODE_TRIGGER_UNKNOWN = 0,
    DD_BLENDING_MODE_TRIGGER_FLIP,
    DD_BLENDING_MODE_TRIGGER_MODESET
} DD_BLENDING_MODE_TRIGGER;

typedef struct _DD_TARGET_COLOR_CONTEXT
{
    DD_COLOR_BLENDING_MODE BlendingMode;
} DD_TARGET_COLOR_CONTEXT;

typedef struct _DD_COLOR_PIPE_CFG
{
    DDU32                  TargetId;
    DDU32                  SupportedPanelFeatures; // If there is a panel connected to current pipe. It is Read only.
    DDU32                  ActivePanelFeatures;    // If there is a panel connected to current pipe. It is Read only.
    DD_COLOR_BLENDING_MODE BlendingMode;
    DD_RGB_DDU8_24         PipeBottomColor;
    DD_COLOR_PIXEL_DESC    BlendingColorFormat;
    DD_COLOR_PIXEL_DESC    OutputColorFormat;
} DD_COLOR_PIPE_CFG;

typedef enum _DD_COLOR_SW_BASIC_FEATURES
{
    DD_COLOR_BASIC_FEATURE_NONE                             = 0,
    DD_COLOR_BASIC_FEATURE_RELMATRIX_CUI_RELLUT_CUIOS       = 1, // SKL+
    DD_COLOR_BASIC_FEATURE_RELMATRIX_CUIOS_RELLUT_CUIOS     = 2, // SKL+
    DD_COLOR_BASIC_FEATURE_RELMATRIXCUI_RELLUTCUIOS_3DLUT   = 3, // CNL+, RS1+
    DD_COLOR_BASIC_FEATURE_RELMATRIXCUIOS_RELLUTCUIOS_3DLUT = 4, // CNL+, RS3+
    DD_COLOR_BASIC_FEATURE_MAX
} DD_COLOR_SW_BASIC_FEATURES;

typedef enum _DD_COLOR_SW_ADVANCED_FEATURES
{
    DD_COLOR_ADV_FEATURE_NONE                       = 0,
    DD_COLOR_ADV_FEATURE_ABSLUT                     = 1,  // SKL+
    DD_COLOR_ADV_FEATURE_ABSLUT_YCBCR               = 2,  // SKL+
    DD_COLOR_ADV_FEATURE_ABSLUT_ABSMATRIX           = 3,  // SKL+
    DD_COLOR_ADV_FEATURE_ABSLUT_GAMUTMAP            = 4,  // SKL+        if WG/NG features are enabled
    DD_COLOR_ADV_FEATURE_ABSLUT_GAMUTMAP_BT2020     = 5,  // CNL+        WG for external panel, NG for internal panel
    DD_COLOR_ADV_FEATURE_ABSLUT_ABSMATRIX_BT2020    = 6,  // CNL+        GAMUT_MAP(WG/NG) can't coexist ABSMATRIX
    DD_COLOR_ADV_FEATURE_ABSLUT_YCBCR_BT2020        = 7,  // CNL+        GAMUT_MAP(WG/NG) or ABSMATRIX can't coexis with YCBCR pipe output
    DD_COLOR_ADV_FEATURE_ABSLUT_GAMUTMAP_HDR        = 8,  // ICL+        WG for external panel, NG for internal panel
    DD_COLOR_ADV_FEATURE_ABSLUT_YCBCR_GAMUTMAP_HDR  = 9,  // ICL+        WG for external panel, NG for internal panel
    DD_COLOR_ADV_FEATURE_ABSLUT_ABSMATRIX_HDR       = 10, // ICL+        GAMUT_MAP(WG/NG) can't coexist ABSMATRIX
    DD_COLOR_ADV_FEATURE_ABSLUT_YCBCR_ABSMATRIX_HDR = 11, // ICL+        GAMUT_MAP(WG/NG) can't coexist ABSMATRIX
    DD_COLOR_ADV_FEATURE_MAX
} DD_COLOR_SW_ADVANCED_FEATURES;

typedef struct _DD_COLOR_SW_FEATURES_ST
{
    DD_COLOR_SW_BASIC_FEATURES    SupportedBasicFeatures; // TODO: Indicate flag for indicating querying for activer values.
    DD_COLOR_SW_ADVANCED_FEATURES SupportedAdvancedFeatures;
    DD_COLOR_SW_BASIC_FEATURES    ActiveBasicFeatures;
    DD_COLOR_SW_ADVANCED_FEATURES ActiveAdvancedFeatures;
    DD_COLOR_SW_BASIC_FEATURES    DefaultBasicFeatures;
    DD_COLOR_SW_ADVANCED_FEATURES DefaultAdvancedFeatures;
} DD_COLOR_SW_FEATURES_ST;

typedef struct _DD_COLOR_PLATFORM_CFG
{
    DDU32                   Size;        // Size of this structure
    DDU32                   Reserved[2]; // For future use
    DDU32                   NumActivePipes;
    DD_COLOR_PIPE_CFG       PipeColorCfg[MAX_PHYSICAL_PIPES];
    DD_COLOR_SW_FEATURES_ST SwColorFtrCfg;
} DD_COLOR_PLATFORM_CFG;

// Reg keys for persistence
typedef enum _DD_COLOR_REG_KEY
{
    DD_COLOR_RANGE_TYPE_REG_KEY,
    DD_COLOR_MODEL_REG_KEY
} DD_COLOR_REG_KEY;

// VBT/Opregion PowerCons Data

// Used in case there are multiple instances of PWM that needs to be selected/enabled
typedef enum _DD_PWM_CTRL_NUM
{
    DD_PWM_NUM0 = 0,
    DD_PWM_NUM1,
    DD_PWM_NUM_MAX
} DD_PWM_CTRL_NUM;

typedef enum _DD_PWM_TYPE
{
    DD_TYPE_EXTERNAL = 0,
    DD_TYPE_I2C,
    DD_TYPE_EXTERNAL_INTERNAL,
    DD_TYPE_RESERVED
} DD_PWM_TYPE;

typedef enum _DD_PWM_CTRL_TYPE
{
    DD_PWM_CTRL_TYPE_UNDEFINED = -1,
    DD_PWM_CTRL_TYPE_PMIC,         // PWM source is from PMIC
    DD_PWM_CTRL_TYPE_SOC,          // PWM source is from LPSS/PMC module (non-IGD based)
    DD_PWM_CTRL_TYPE_INTERNAL_IGD, // PWM source is within display controller
    DD_PWM_CTRL_TYPE_PANEL_CABC,   // PWM source is on the display panel (CABC supported ones)
    DD_PWM_CTRL_TYPE_PANEL_DRIVER  // PWM source is through external Panel driver
} DD_PWM_CTRL_TYPE;

typedef enum _DD_DPST_BKLT_TYPE
{
    DD_BKLT_TYPE_UNDEFINED = 0,
    DD_CCFL_BACKLIGHT,
    DD_LED_BACKLIGHT,
    DD_MAX_BACKLIGHT_TYPE
} DD_DPST_BKLT_TYPE;

typedef enum _DD_DPST_AGGRESSIVENESS_LEVEL
{
    LEVEL_1 = 0x1,
    LEVEL_2,
    LEVEL_3,
    LEVEL_4,
    LEVEL_5,
    LEVEL_6
} DD_DPST_AGGRESSIVENESS_LEVEL;

typedef union _DD_ALS_DATA {
    DDU32 AlsData; // ALS data
    struct
    {
        DDU16 BkltAdjust; // Backlight Adjust
        DDU16 LuxValue;   // Lux Value
    };
} DD_ALS_DATA;

typedef enum _DD_DPS_PANEL_TYPE
{
    STATIC_DRRS = 0,
    D2PO        = 0,
    SEAMLESS_DRRS,
    RSVD_PANEL_TYPE,
} DD_DPS_PANEL_TYPE;

typedef struct _DD_BLC_FEATURES
{
    DD_PWM_CTRL_TYPE PwmType;               // PWM contrller type
    DD_PWM_CTRL_NUM  PwmCtrlNum;            // PWM controller number
    BOOLEAN          IsPwmPolarityInverted; // WM *polarity
    DDU32            PWMInverterFrequency;  // (100 * Ref clock frequency in MHz / 2) - 1.
    DDU8             MinBrightness;         // Minimum Brightness

    BOOLEAN                      IsADBSupported;               // Automatic DisplayBrightness (ADB)
    DD_ALS_DATA                  AlsData[MAX_ALS_DATA_POINTS]; // ALS data
    DD_DPST_AGGRESSIVENESS_LEVEL DPSTAggressivenessLevel;      // DPST agressiveness level

    DD_DPST_BKLT_TYPE BlcBkltType; // BLC controller type (CCFL/LED), mostly un-used
} DD_BLC_FEATURES;

typedef struct _DD_PC_FEATURES
{
    // BOOLEAN        IsValidBit;            // Bit to enable/disable PC feature set (described above)
    BOOLEAN IsRMPMEnabled;            // Rapid Memory Power Management (RMPM)
    BOOLEAN IsFBCEnabled;             // Frame Buffer Compression (Smart 2D Display Technology; S2DDT)
    BOOLEAN IsDxgkDdiBlcSupported;    // DxgkDDI Brightness Control Enable
    BOOLEAN IsCDClockChangeSupported; // Dynamic CD clock change support
    BOOLEAN IsDRRSEnabled;            // Dynamic Refresh Rate Switching (DRRS)
    BOOLEAN IsRSSupported;            // Graphics Render Standby (RS)
    BOOLEAN IsTurboBoostEnabled;      // Turbo Boost enable
    BOOLEAN IsDFPSEnabled;            // Dynamic Frames Per Second (DFPS)
    BOOLEAN IsDMRRSEnabled;           // Dynamic Media Refresh Rate Switching (DMRRS)
    BOOLEAN IsADT;                    // Assertive Display technology
    BOOLEAN IsWakeOnHPDSupported;     // This feature enables HPD events like Hotplug/unplug as a wake up source from S0ix/DC9 in supported platforms

    BOOLEAN           IsDPSTEnabled;    // Dynamic Power Saving Technology (DPST)
    DDU8              PwrConsAggrLevel; // DPST Aggressiveness Level of Type DPST_AGGRESSIVENESS_LEVEL
    DD_BLC_FEATURES   BlcParams;        // Backlight control Params from VBT
    DD_DPS_PANEL_TYPE DpsPanelType;     // DRRS panel type (static/seamless)
} DD_PC_FEATURES;

typedef enum _DD_CONNECTOR_TYPE
{
    DD_CONNECTOR_NONE,
    DD_CONNECTOR_EDP,
    DD_CONNECTOR_DP,
    DD_CONNECTOR_HDMI,
    DD_CONNECTOR_DVI,
    DD_CONNECTOR_MIPI
} DD_CONNECTOR_TYPE;

typedef struct _DD_CONNECTOR_INFO
{
    DD_CONNECTOR_TYPE          SupportedConnectors;
    DD_CONNECTOR_TYPE          AttachedConnectors;
    DD_CONNECTOR_TYPE          ActiveConnectors;
    DD_VIDEO_OUTPUT_TECHNOLOGY DongleDwnStreamPortType;
} DD_CONNECTOR_INFO;

typedef struct _DD_GET_CONNECTOR_INFO_ARGS
{
    DD_PORT_TYPE      Port;
    DD_CONNECTOR_INFO ConInfo;
} DD_GET_CONNECTOR_INFO_ARGS;

typedef enum _DD_GT_PC_NOTIFY_EVENT
{
    DD_MODE_CHANGE_EVENT,
    DD_PWR_SRC_EVENT,
    DD_FLIP_DONE_EVENT
} DD_GT_PC_NOTIFY_EVENT;

typedef enum _DD_PWR_SRC_EVENT_ARGS
{
    DD_PWR_UNKNOWN, // Set to unknown until power source is queried in DxgkDdiStartDevice call path
    DD_PWR_AC,
    DD_PWR_DC
} DD_PWR_SRC_EVENT_ARGS;

typedef struct _DD_MODE_EVENT_CONFIG
{
    DDU32               TargetId;
    PIPE_ID             PipeID;
    DD_SOURCE_MODE_INFO SourecMode;
    DD_TIMING_INFO      TimingInfo;
} DD_MODE_EVENT_CONFIG;

typedef struct _DD_MODE_CHANGE_EVENT_ARGS
{
    BOOLEAN              PreModeSet;
    DDU32                PathCount;
    DD_MODE_EVENT_CONFIG Config[MAX_PHYSICAL_PIPES];
} DD_MODE_CHANGE_EVENT_ARGS;

typedef struct _DD_FLIP_DONE_EVENT_ARGS
{
    PIPE_ID PipeId;
    DDU8    BitWiseSyncPlane;  // Planes with Sync Flip
    DDU8    BitWiseAsyncPlane; // Planes with Async flip
} DD_FLIP_DONE_EVENT_ARGS;

typedef struct _DD_GT_PC_NOTIFY_EVENT_ARGS
{
    DD_GT_PC_NOTIFY_EVENT EventType;
    union {
        DD_MODE_CHANGE_EVENT_ARGS DisplayModeChangeEventArgs;
        DD_PWR_SRC_EVENT_ARGS     PowerSourceEventArgs;
        DD_FLIP_DONE_EVENT_ARGS   FlipDoneEventArgs;
    };
} DD_GT_PC_NOTIFY_EVENT_ARGS;

DD_INLINE BOOLEAN IsYCbCrFormat(DD_COLOR_MODEL eColorModel)
{
    BOOLEAN retVal = FALSE;

    switch (eColorModel)
    {
    case DD_COLOR_MODEL_YCBCR_601:
    case DD_COLOR_MODEL_YCBCR_709:
    case DD_COLOR_MODEL_YCBCR_2020:
        retVal = TRUE;
        break;
    default:
        retVal = FALSE;
        break;
    }

    return retVal;
}

// Subsampled formats needs special blocks to be enabled e.g. CUS, scaler.
// It may require modeset when pipe output is subsampled
DD_INLINE BOOLEAN IsYCbCrSubSampledFormat(DD_COLOR_YCBCR_SUBSAMPLING eSubsampling)
{
    BOOLEAN retVal = FALSE;

    switch (eSubsampling)
    {
    case DD_COLOR_SUBSAMPLING_422_PACKED:
    case DD_COLOR_SUBSAMPLING_422_PLANAR:
    case DD_COLOR_SUBSAMPLING_420_PLANAR:
        retVal = TRUE;
        break;
    default:
        retVal = FALSE;
        break;
    }

    return retVal;
}

#define DD_IS_VIRTUAL_TARGET(DisplayID) ((DisplayID & 0xF) == DD_PORT_TYPE_VIRTUAL_PORT)
#define DD_GET_VIRTUAL_PIPE(DisplayID) ((DisplayID & 0xF00) >> 8)

//
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//----------------------------------------------------------------------------
//
// DO NOT DEFINE ANYTHING AFTER THIS !!!
//
//----------------------------------------------------------------------------
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
