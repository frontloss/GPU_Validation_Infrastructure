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
@file DisplayArgsInternal.h
@brief display args -- Used to define structures/interfaces used by external non-display components
*/

#pragma once
#include "DisplayArgs.h"

#ifdef _DISPLAY_INTERNAL_

//----------------------------------------------------------------------------
//
// Generic CONSTANTS, ENUMS and MACROS - START
//
//----------------------------------------------------------------------------
#define MAX_PHYSICAL_PORTS_GEN10 4
#define MAX_PHYSICAL_PORTS_GEN11 6
#define MAX_PHYSICAL_PORTS MAX_PHYSICAL_PORTS_GEN11

#define DD_MAX_NUM_REFRESH_RATES 5

#define CONVERT_TO_ASYNC_SCANLINE_BUFFER 10
#define MAX_CURSOR_PLANES 4
#define DD_MAX_PLANES_PER_PIPE 4

#define MAX_COLOR_BPP 4 // 8, 16, 32 & 64 bpps (doesn't include 4bpp)
#define ALLCOLOR_BPP_MASK 0x1F
#define WINDOWS_COLOR_MASK 0x1E // doesn't have 4bpp

#define TMDS_CHAR_RATE_340MCSC 340000000 // High TMDS char rate
#define INVERSE_100_NANO_SEC 10000000

// Color related
#define CUI_PREFIX L"CUILut"
#define OS_PREFIX L"OSLut"
#define ABS_PREFIX L"AbsLut"
#define CSC_PREFIX L"RelCSC"
#define SELECT_BPC_FROM_REG_KEY L"SelectBPCFromRegistry"
#define REGISTRY_OVERRIDE_BPC_VALUE_KEY L"SelectBPC"
#define DD_MAX_VBT_ENCODERS 10

#define CUSTOM_DOWN_SCALE_PERCENT_X 7
#define CUSTOM_DOWN_SCALE_PERCENT_Y 7

typedef enum _DD_CDCLK_FREQ_VAL
{
    INVALID_CDCLK_FREQ = -1,
    CDCLK_FREQ_168MHZ, // CNL starts
    CDCLK_FREQ_336MHZ,
    CDCLK_FREQ_528MHZ,  // CNL ends
    CDCLK_FREQ_79_2MHZ, // GLK starts
    CDCLK_FREQ_158_4MHZ,
    CDCLK_FREQ_316_8MHZ, // GLK ends
    CDCLK_FREQ_307_2MHZ, // ICL start here
    CDCLK_FREQ_312_MHZ,
    CDCLK_FREQ_552_MHZ,
    CDCLK_FREQ_556_8MHZ,
    CDCLK_FREQ_648_MHZ,
    CDCLK_FREQ_652_8MHZ, // ICL clocks end here
    CDCLK_MAX
} DD_CDCLK_FREQ_VAL;

//----------------------------------------------------------------------------
//
// Generic CONSTANTS, ENUMS and MACROS - END
//
//----------------------------------------------------------------------------

// Used as a value for D3DDDI_VIDEO_PRESENT_SOURCE_ID and D3DDDI_VIDEO_PRESENT_TARGET_ID types to specify
// that the respective video present source/target ID hasn't been initialized.
//#define DD_TARGET_ID_UNINITIALIZED (DDU32)(~0)

typedef struct _DD_CURSOR_BUFFER_INFO
{
    void *  pCursorBufferLinearAddress;
    void *  pGmmBlock;
    DDU32   BaseAddress;
    BOOLEAN Allocated;
} DD_CURSOR_BUFFER_INFO;

typedef struct _DD_CURSOR_ATTRIB
{
    IN DDU32 CursorWidth;                  // Current cursor width
    IN DDU32 CursorHeight;                 // Current cursor height
    IN DDU32 CursorPitch;                  // Pitch of Cursor.
    IN DDU32 BitsPerPixel;                 // Bits per pixel for this cursor
    IN DDU32 BaseAddress;                  // Needed to trigger the update.
    IN PLANE_ORIENTATION PlaneOrientation; // ORIENTATION_DEFAULT,ORIENTATION_0 = ORIENTATION_DEFAULT,ORIENTATION_180
    IN DDU32 CursorSize;
} DD_CURSOR_ATTRIB;

typedef struct _DD_CURSOR_INFO
{
    IN DDU32 PipeIndex;              // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
    IN DD_POINTER_FLAGS CursorFlags; // use these flags to avoid b-spec violations
                                     // ex - 256x256 32bpp ARGB (not available for VGA use)
    DD_CURSOR_ATTRIB      CursorAttrib;
    DD_CURSOR_BUFFER_INFO CursorBufferInfo;
    DD_CURSOR_BUFFER_INFO CursorCopyBufferInfo;
    BOOLEAN               ShapeChanged;
} DD_CURSOR_INFO;

// Cursor args structure
typedef struct _DD_CURSOR_ARGS
{
    BOOLEAN Enable;
    PIPE_ID Pipe;
    IN DDS32 XPos;
    IN DDS32 YPos;
    IN DDU32 BaseAddress;            // Needed to trigger the update.
    IN DDU32 CursorWidth;            // Current cursor width
    IN DDU32 CursorHeight;           // Current cursor height
    IN DD_POINTER_FLAGS CursorFlags; // use these flags to avoid b-spec violations
    IN BOOLEAN ShapeChanged;
} DD_CURSOR_ARGS;

//----------------------------------------------------------------------------
//
// Cursor related constants and data structures -- END
//
//----------------------------------------------------------------------------

//////////////////////////////////////////////////////////////////////////////
//----------------------------------------------------------------------------
//
// OSL data structures - START
//
//----------------------------------------------------------------------------
//////////////////////////////////////////////////////////////////////////////

// typedef enum _DD_PIPE_ORIENTATION
//{
//    PIPE_ORIENTATION_UNDEFINED = 0,
//    PIPE_ORIENTATION_0,
//    PIPE_ORIENTATION_90,
//    PIPE_ORIENTATION_180,
//    PIPE_ORIENTATION_270,
//} DD_PIPE_ORIENTATION;

typedef enum _DD_MEDIA_RR_TYPE
{
    DD_MEDIA_RR_UNINITIALIZED = 0,
    DD_MEDIA_RR_FRACTIONAL    = 1,
    DD_MEDIA_RR_INTEGER       = 2,
    DD_MEDIA_RR_NONE          = 3
} DD_MEDIA_RR_TYPE;

// DDK/OS independent values defined from DD
typedef enum _DD_PIXEL_VALUE_ACCESS_MODE
{
    DD_PVAM_UNINITIALIZED   = 0,
    DD_PVAM_DIRECT          = 1,
    DD_PVAM_PRESETPALETTE   = 2,
    DD_PVAM_SETTABLEPALETTE = 3,
} DD_PIXEL_VALUE_ACCESS_MODE;

// CCD structures

typedef struct _DD_GET_LIVE_SURF_ADDRESS_ARGS
{
    DD_IN PIPE_ID PipeId;
    DD_OUT DDU32 LiveAddress[MAX_PLANES_PER_PIPE];
    DD_OUT BOOLEAN FlipDone[MAX_PLANES_PER_PIPE];
} DD_GET_LIVE_SURF_ADDRESS_ARGS;

typedef struct _DD_GET_CURSOR_LIVE_SURF_ADDRESS_ARGS
{
    DD_IN PIPE_ID PipeId;
    DD_OUT DDU32 LiveAddress;
} DD_GET_CURSOR_LIVE_SURF_ADDRESS_ARGS;
//----------------------------------------------------------------------------
//
//  ACPI related enums and data structures - START
//
//----------------------------------------------------------------------------

//  Arguments to evaluate _DOD.
#define DD_MAX_DIDS 0x8

typedef struct _DD_GET_ACPI_ID
{
    DD_IN DDU32 TargetId; // of type DD_TARGET_ID
    DD_OUT DDU32 AcpiId;  // of type ACPI30_DOD_ID
} DD_GET_ACPI_ID;

//----------------------------------------------------------------------------
//
//  ACPI related enums and data structures - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// MPO related data structures - START
//
//----------------------------------------------------------------------------
typedef struct _DD_SURFACE_SCANOUT_DETAILS
{
    DD_IN DDU32 PanningPosX;
    DD_IN DDU32 PanningPosY;
    DD_IN DDU32 UvPanningPosX;
    DD_IN DDU32 UvPanningPosY;
    DD_IN DDU32 ScanSurfSizeX;
    DD_IN DDU32 ScanSurfSizeY;
} DD_SURFACE_SCANOUT_DETAILS;

typedef struct _DD_SURFACE_TRANSFORM
{
    DD_IN DD_ROTATION PlaneOrientation;
    struct
    {
        DD_IN DDU32 VerticalFlip : 1;
        DD_IN DDU32 HorizontalFlip : 1;
        DD_IN DDU32 Scale : 1;
        DD_IN DDU32 HorzStretch : 1; // TRUE = STRETCH, FALSE = SHRINK, Valid only when 'Scale' = TRUE;
        DD_IN DDU32 VertStretch : 1;
        DD_IN DDU32 HighQualityStretch : 1;
    };
    DD_IN DDU32 HorzScaleFactorMultBy100;
    DD_IN DDU32 VertScaleFactorMultBy100;
    DD_IN DDU32 ScreenSurfSizeX;
    DD_IN DDU32 ScreenSurfSizeY;
} DD_SURFACE_TRANSFORM;

typedef struct _DD_2DREGION
{
    DDU32 Cx;
    DDU32 Cy;
} DD_2DREGION;

typedef struct _DD_PLANE_SURF
{
    DD_IN BOOLEAN AlphaBlend;
    DD_IN DD_SURFACE_ATTRIBUTES Attrib;
    DD_IN DD_SURFACE_SCANOUT_DETAILS ScanOutDetails;
    DD_IN DD_SURFACE_TRANSFORM Transform;
    DD_IN DDU32 ScreenPositionX;
    DD_IN DDU32 ScreenPositionY;
    DD_IN DD_COMPRESSION_DETAILS CompressionDetails;
} DD_PLANE_SURF;

typedef struct _DD_CHECK_MPO_PLANE_PARAMS
{
    DD_IN DDU32 HwPlaneId;
    DD_IN DD_PLANE_SURF PlaneSurf; // To be filled ONLY when programming all parameters
    DD_IN BOOLEAN AsyncFlip;
    DD_IN DDU32 LayerIndex;
} DD_CHECK_MPO_PLANE_PARAMS;

typedef struct _DD_PLANE_PARAMS
{
    DD_IN DDU8 HwPlaneId;              // REQUIRED FOR    ALL     FLIP TYPES
    DD_IN DDU32 HwStartAddressBase;    // REQUIRED FOR   ALL    FLIP TYPES
    DD_IN DDU32 HwStartAddressUv;      // REQUIRED FOR   ALL    FLIP TYPES
    DD_IN DDU32 MaxScanLineForAsync;   //     FLIP_TYPE_CONVERT_SYNC_TO_ASYNC  ONLY
    DD_OUT BOOLEAN *pConvertedToAsync; //    FLIP_TYPE_CONVERT_SYNC_TO_ASYNC  ONLY
    DD_IN BOOLEAN Enable;              // FLIP_TYPE_SYNC_ALL_PARAM ONLY
    DD_PLANE_SURF PlaneSurf;           // FLIP_TYPE_SYNC_ALL_PARAM ONLY
} DD_PLANE_PARAMS;

typedef enum _DD_VRR_STATUS
{
    DD_VRR_STATUS_UNKNOWN = 0,
    DD_VRR_STATUS_ENABLE_IN_PROGRESS,
    DD_VRR_STATUS_ENABLE,
    DD_VRR_STATUS_DISABLE_IN_PROGRESS,
    DD_VRR_STATUS_DISABLE
} DD_VRR_STATUS;

typedef enum _FLIP_TYPE
{
    FLIP_TYPE_ASYNC = 0,
    FLIP_TYPE_CONVERT_SYNC_TO_ASYNC,
    FLIP_TYPE_SYNC_ADDRESS_ONLY,
    FLIP_TYPE_SYNC_ALL_PARAM,
    FLIP_TYPE_MAX
} FLIP_TYPE;

typedef struct _DD_CHECK_MPO_PLANES_ARGS
{
    DD_IN DDU32 PipeIndex;
    DD_IN DDU32 NumPlanes;
    DD_IN DD_CHECK_MPO_PLANE_PARAMS PlaneParams[MAX_PLANES_PER_PIPE];
} DD_CHECK_MPO_PLANES_ARGS;

typedef struct _DD_PROGRAM_PLANES_ARGS
{
    DD_IN FLIP_TYPE FlipType;
    DD_IN DDU32 PipeIndex;
    DD_IN VRR_STATUS VrrStatus;
    DD_IN DDU32 NumPlanes;
    DD_IN DD_COLOR_BLENDING_MODE PipeBlendingMode;
    DD_IN DD_PLANE_PARAMS PlaneParams[MAX_PLANES_PER_PIPE];
} DD_PROGRAM_PLANES_ARGS;

typedef struct _DD_PLANE_DBUF_ARGS
{
    DD_IN DDU8 HwPlaneId;
    DD_IN DDU16 StartBlock;
    DD_IN DDU16 EndBlock;
} DD_PLANE_DBUF_ARGS;

typedef struct _DD_PIPE_DBUF_ARGS
{
    DD_IN DDU32 PipeIndex;
    DD_IN DDU32 NumPlanes;
    DD_IN BOOLEAN NeedTrigger;
    DD_IN BOOLEAN InSufficientDbuf;
    DD_IN BOOLEAN ClearDbuf;
    DD_IN DD_PLANE_DBUF_ARGS CursorDbuf;
    DD_IN DD_PLANE_DBUF_ARGS PlaneDBuf[MAX_PLANES_PER_PIPE];
} DD_PIPE_DBUF_ARGS;

typedef struct _DBUF_RE_ALLOC_WAIT_ORDER
{
    PIPE_ID PipeIndex;
    BOOLEAN NeedWaitForVbi;
} DBUF_RE_ALLOC_WAIT_ORDER;

typedef struct _DD_GET_CURRENT_SCAN_LINE_ARGS
{
    DD_IN DDU32 PipeIndex;
    DD_OUT DDU32 CurrScanLine;
    DD_OUT BOOLEAN InVerticalBlank;
} DD_GET_CURRENT_SCAN_LINE_ARGS;

// Set scan line compare Args Structure
typedef struct _DD_SET_SCAN_LINE_COMPARE_ARGS
{
    DD_IN DDU32 PipeIndex;                   // Pipe index
    DD_IN BOOLEAN InitiateCompare;           // initiate a scan line compare
    DD_IN BOOLEAN CompareInclusive;          // Trigger inside compare window, or outside window
    DD_IN BOOLEAN CounterSelectPrimaryPlane; // Set counter trigger Primary plane vs timing generator [ Plane vs Pipe scan line counter]
    DD_IN BOOLEAN RenderResponceBCS;         // Set Render Response BCS vs CS
    DD_IN DDU32 StartScanLine;               // Scan line that start the window
    DD_IN DDU32 EndScanLine;                 // Scan line that ends the window
} DD_SET_SCAN_LINE_COMPARE_ARGS;

typedef struct _DD_CHECK_MPO_PIPE_DETAILS
{
    DDU32                    SourceSizeX;
    DDU32                    SourceSizeY;
    DD_TIMING_INFO           TimingInfo;
    DD_CHECK_MPO_PLANES_ARGS FlipParams;
    DD_OUT DDU32 FailingHwPlaneId;
} DD_CHECK_MPO_PIPE_DETAILS;

typedef struct _DD_CHECK_MPO_RM_ARGS
{
    DD_IN DD_CHECK_MPO_PIPE_DETAILS PipeDetails[MAX_PHYSICAL_PIPES];
    DD_OUT PIPE_ID FailingPipe;
} DD_CHECK_MPO_RM_ARGS;

#define NUM_WM_PER_PLANE 8
#define BYTES_PER_BLOCK 512
#define DBUF_TILE_X 8
#define DBUF_MIN_DBLOCK_SIZE 512
#define WM_MEMORY_READ_LATENCY 2
#define MIN_DBUF_FOR_WIGIG 202
#define LATENCY_INCREMENT_IPC 4

typedef struct _DD_COMPUTE_PIPE_DBUF_ARGS
{
    DD_IN DD_TIMING_INFO TimingInfo;
    DD_IN DD_PIXELFORMAT PixelFormat;
    DD_IN DD_SURFACE_MEMORY_TYPE SurfMemType;
} DD_COMPUTE_PIPE_DBUF_ARGS;

typedef struct _DD_COMPUTE_DBUF_ARGS
{
    DDU32          SourceSizeX;
    DDU32          SourceSizeY;
    DD_TIMING_INFO TimingInfo;
    // DD_ENABLE_DISABLE_PLANES_ARGS FlipParams;
} DD_COMPUTE_DBUF_ARGS;

//
typedef struct _DD_WM_DATA
{
    DD_OUT BOOLEAN WmEnable;
    DD_OUT BOOLEAN IgnoreLines;
    DD_OUT DDU16 WmLines;
    DD_OUT DDU16 WmBlocks;
} DD_WM_DATA;

typedef struct _DBUF_ALLOC_INFO
{
    DDU16 DBufAllocated;
    DDU16 StartBlock;
    DDU16 EndBlock;
} DBUF_ALLOC_INFO;

typedef struct _DBUF_WM_OUT_DATA
{
    // OUT Params for the WM DBUf computations
    DD_OUT DBUF_ALLOC_INFO DBufAllocation;
    DD_OUT DD_WM_DATA LPWm[NUM_WM_PER_PLANE];
    DD_OUT DD_WM_DATA TransWm;
} DBUF_WM_OUT_DATA;
typedef struct _DD_PLANE_DATA_FOR_WM_DBUF
{
    DD_IN DDU8 HwPlaneId;
    DD_IN DDU32 SurfWidth;
    DD_IN DDU32 SurfHeight;
    DD_IN DD_PIXELFORMAT PixelFormat;
    DD_IN DD_SURFACE_MEMORY_TYPE SurfMemType;
    DD_IN DD_ROTATION PlaneOrientation;
    DD_IN DDU32 PlaneBytePerPixel;
    DD_IN DDU32 CustomPlaneScalingValue;
    DD_IN DDU32 DBufAllocatedOnPlane;

} DD_PLANE_DATA_FOR_WM_DBUF;

typedef struct _DD_ENABLED_PLANE_DATA_ARGS
{
    PIPE_ID                   PipeId;
    DDU32                     NumEnabledPlanes;
    DD_PLANE_DATA_FOR_WM_DBUF PlaneDataForWM[MAX_PLANES_PER_PIPE];
    DBUF_WM_OUT_DATA          DbufWMResult[MAX_PLANES_PER_PIPE];
    BOOLEAN                   SkipUpdate;
    BOOLEAN                   WaitForVBlank;
} DD_ENABLED_PLANE_DATA_ARGS;

typedef struct _DD_ENABLED_CURSOR_DATA_ARGS
{
    PIPE_ID                   PipeId;
    DD_PLANE_DATA_FOR_WM_DBUF PlaneDataForWM;
    BOOLEAN                   WaitForVBlank;
} DD_ENABLED_CURSOR_DATA_ARGS;

typedef struct _DD_TRANS_LP_WM_DATA
{
    DDU32      Level;
    DD_WM_DATA LPWm;
    DD_WM_DATA TransWm;
    DDU32      LineTime;
} DD_TRANS_LP_WM_DATA;

typedef struct _DD_PLANE_WM_PROGRAM_DATA
{
    DDU32      PipeIndex;
    DDU8       HwPlaneId;
    DD_WM_DATA LPWm[NUM_WM_PER_PLANE];
    DD_WM_DATA TransWm;
} DD_WM_PROGRAM_DATA;

typedef struct _DD_COMPUTE_WM_ARGS
{
    DD_IN DDU32 Level;
    DD_IN DD_PLANE_DATA_FOR_WM_DBUF PlaneDataForWM;

    DD_IN DDU32 HTotal;
    DD_IN DDU32 DotClockInKHz;
    DD_IN BOOLEAN IsInterlaced;
    DD_IN DDU32 CustomPipeScalingValue;
    DD_IN BOOLEAN IsCursorPlane;
    DD_IN BOOLEAN IsWMCalcForDbuf;

    DD_OUT DD_WM_DATA LPWm;
    DD_OUT DD_WM_DATA TransWm;
} DD_COMPUTE_WM_ARGS;

typedef struct _DD_WM_COMPUTE_INTERMEDIATE_DATA
{
    DDU32 LPLatency;
    DDU32 DBufAllocatedOnPlane;
    DDU32 AdjustedPixelRateInKHz;
    DDU32 PlaneBytePerPixel;
    DDU32 YTileMinLines;
    DDU32 Method1In100;
    DDU32 Method2In100;
    DDU32 YTileMinIn100;
    DDU32 PlaneBlocksPerLineIn100;
    // DDU32 SelectedResultBlocksIn100;
    DDU32 BytesPerLineIn100;
    DDU32 DBufBlockSize;
} DD_WM_COMPUTE_INTERMEDIATE_DATA;

//----------------------------------------------------------------------------
//
// MPO related data structures - END
//
//----------------------------------------------------------------------------

//////////////////////////////////////////////////////////////////////////////
//----------------------------------------------------------------------------
//
// OSL data structures - END
//
//----------------------------------------------------------------------------
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
//----------------------------------------------------------------------------
//
// Protocol data structures - START
//
//----------------------------------------------------------------------------
//////////////////////////////////////////////////////////////////////////////

typedef enum _DD_PROTOCOL_TYPE
{
    DD_PROTOCOL_UNKNOWN = 0,
    DD_PROTOCOL_HDMI,
    DD_PROTOCOL_DVI,
    DD_PROTOCOL_DISPLAYPORT_SST,
    DD_PROTOCOL_DISPLAYPORT_EMBEDDED,
    DD_PROTOCOL_DISPLAYPORT_MST,
    DD_PROTOCOL_MIPI,
    DD_PROTOCOL_WDE, // wigig
    DD_PROTOCOL_VIRTUAL,

    // PROTOCOL_MAX = PROTOCOL_VIRTUAL
} DD_PROTOCOL_TYPE;
#define IS_DP_PROTOCOL(proto) ((proto >= DD_PROTOCOL_DISPLAYPORT_SST) && (proto <= DD_PROTOCOL_DISPLAYPORT_MST))
#define IS_HDMI_PROTOCOL(proto) (proto == DD_PROTOCOL_HDMI)
#define IS_MIPI_PROTOCOL(proto) (proto == DD_PROTOCOL_MIPI)

typedef enum _DD_PORT_CONFIG_TYPE
{
    PORT_CONFIG_NONE = 0,
    PORT_CONFIG_DVI,
    PORT_CONFIG_HDMI,
    PORT_CONFIG_DISPLAYPORT_EXTERNAL,
    PORT_CONFIG_DISPLAYPORT_EMBEDDED,
    PORT_CONFIG_DISPLAYPORT_DUAL_MODE_HDMI,
    PORT_CONFIG_DISPLAYPORT_DUAL_MODE_DVI,
    PORT_CONFIG_MIPI,
    PORT_CONFIG_VIRTUAL,

    PORT_CONFIG_MAX
} DD_PORT_CONFIG_TYPE;

typedef enum _DD_LFP_NUM
{
    DD_LFP_0,
    DD_LFP_1,
    DD_LFP_MAX
} DD_LFP_NUM;

// port config related
#define IS_PORT_CFG_DP_COMPATIBLE(cfg)                                                                                                                  \
    (((cfg) == PORT_CONFIG_DISPLAYPORT_EXTERNAL) || ((cfg) == PORT_CONFIG_DISPLAYPORT_EMBEDDED) || ((cfg) == PORT_CONFIG_DISPLAYPORT_DUAL_MODE_HDMI) || \
     ((cfg) == PORT_CONFIG_DISPLAYPORT_DUAL_MODE_DVI))
#define IS_PORT_CFG_EXT_DP_COMPATIBLE(cfg) \
    (((cfg) == PORT_CONFIG_DISPLAYPORT_EXTERNAL) || ((cfg) == PORT_CONFIG_DISPLAYPORT_DUAL_MODE_HDMI || (cfg) == PORT_CONFIG_DISPLAYPORT_DUAL_MODE_DVI))
#define IS_PORT_CFG_DVI_COMPATIBLE(cfg) (((cfg) == PORT_CONFIG_DISPLAYPORT_DUAL_MODE_DVI) || ((cfg) == PORT_CONFIG_DVI))
#define IS_PORT_CFG_HDMI_COMPATIBLE(cfg) (((cfg) == PORT_CONFIG_DISPLAYPORT_DUAL_MODE_HDMI) || ((cfg) == PORT_CONFIG_HDMI))
#define IS_PORT_CFG_VIRTUAL(cfg) ((cfg) == PORT_CONFIG_VIRTUAL) // Add Write back as well during the write back enabling

typedef struct _DD_GET_SET_VIRTUAL_LIVE_SURF_ADDRESS
{
    DD_IN PIPE_ID PipeId;
    // DD_IN DD_TARGET_DESCRIPTOR  *pTargetDescriptor;
    DD_IN BOOLEAN IsFLip;
    DD_IN_OUT DDU32 LiveAddress;
} DD_GET_SET_VIRTUAL_LIVE_SURF_ADDRESS;
typedef enum _DD_VIRTUAL_SRC_MODE_REQUEST
{
    DD_VIRTUAL_SRC_MODE_QUERY,
    DD_VIRTUAL_SRC_MODE_ADDITION,
    DD_VIRTUAL_SRC_MODE_REMOVAL,
    DD_VIRTUAL_SRC_MODE_REQUEST_MAX
} DD_VIRTUAL_SRC_MODE_REQUEST;
#define DD_MAX_VIRTUAL_SRC_MODES 20
#define DD_VIRTUAL_DISP_DEFAULT_X_RES 1920
#define DD_VIRTUAL_DISP_DEFAULT_Y_RES 1080
#define DD_VIRTUAL_DISP_DEFAULT_RR 60
#define DD_VIRTUAL_DISP_SCANNER_PERIOD 15 // Should be 16.667 for perfect 60 Hz. Slecting 15 for better timer accuracy

typedef struct _DD_GET_SET_VIRTUAL_SRC_MODES
{
    DD_IN DD_TARGET_DESCRIPTOR *pTargetDescriptor;
    DD_IN DD_VIRTUAL_SRC_MODE_REQUEST RequestType;
    DD_IN_OUT DDU8 NumModes;
    DD_IN_OUT DD_2DREGION SrcModes[DD_MAX_VIRTUAL_SRC_MODES];
} DD_GET_SET_VIRTUAL_SRC_MODES;

typedef struct _DD_SCANNER_PIPE_STATUS
{
    PIPE_ID PipeId;
    BOOLEAN Enabled;
    DDU32   StartAddress;
} DD_SCANNER_PIPE_STATUS;

// HDCP related
typedef enum _DD_HDCP_VERSION
{
    DD_INVALIDHDCPVERSION = 0,
    DD_HDCP1_4            = 1,
    DD_HDCP2_2            = 2,
} DD_HDCP_VERSION;

// typedef enum _DD_ENCRYPTION_TYPE
//{
//    /**no ecnryption */
//    NO_ENCRYPTION = 0,
//    /**PAVP encrypted*/
//    PAVP_PLANE_ENCRYPTED = 1,
//    /**Isolated decode*/
//    ISOLATED_DECODE = 2,
//}DD_ENCRYPTION_TYPE;

typedef enum _DD_HDCP_PORT_ACCESS
{
    DD_HDCP_PORT_ACCESS_UNKNOWN = 0,
    DD_HDCP_PORT_GET_VERSION,
    // HDCP 2.2 Specific data
    DD_HDCP_PORT_GET_RX_STATUS,
    // Generic for HDMI HDCP2 messages
    DD_HDCP_PORT_SEND_HDCP2,
    DD_HDCP_PORT_RECEIVE_HDCP2,
    // DP HDCP2 specific
    // HDCP 1.4 Specific Data Reads
    DD_HDCP_PORT_READ_BKSV,
    DD_HDCP_PORT_READ_BCAPS,
    DD_HDCP_PORT_READ_BSTATUS,
    DD_HDCP_PORT_READ_KSVLIST,
    DD_HDCP_PORT_READ_PRIMEV,
    DD_HDCP_PORT_READ_RI,
    DD_HDCP_PORT_READ_BINFO,
    // HDCP 1.4 specific Data Writes
    DD_HDCP_PORT_SEND_AN,
    DD_HDCP_PORT_SEND_AKSV,
    DD_HDCP_PORT_ACCESS_MAX
} DD_HDCP_PORT_ACCESS;

typedef struct _DD_HDCP_PORT_ACCESS_ARGS
{
    DD_PORT_TYPE        Port;
    DD_HDCP_PORT_ACCESS RequestType;
    DDU8 *              pBuffer;
    DDU32               BufferSize;
} DD_HDCP_PORT_ACCESS_ARGS;

typedef struct _DD_HDMI_GET_SET_INFOFRAME_ARGS
{
    DD_COLOR_PIXEL_DESC *pPipeOutputColorFormat;
    HDMI_PARAMETERS *    pHdmiParams;
} DD_HDMI_GET_SET_INFOFRAME_ARGS;

//----------------------------------------------------------------------------
//
// Display detection and HPD/SPI related structures - START
//
//----------------------------------------------------------------------------

// struct DD_DEVICE_ATTACHED_ARGS: used with IsOutputDeviceAttached
typedef struct _DD_DEVICE_ATTACHED_ARGS
{
    DD_IN DD_PORT_TYPE Port;
    DD_IN DD_PORT_CONNECTOR_TYPE PortConnectorType;
    DD_OUT BOOLEAN IsDisplayAttached;
} DD_DEVICE_ATTACHED_ARGS;
#define DD_DEVICE_ATTACHED_ARGS_DEFAULT \
    {                                   \
        DD_PORT_TYPE_UNKNOWN, FALSE     \
    }

typedef struct _DD_DISPLAY_ACTIVE
{
    DD_TARGET_DESCRIPTOR TgtDesc;
    BOOLEAN              IsActive;
    DD_BPC_SUPPORTED     BitsPerColor;
    DD_SOURCE_MODE_INFO  SourceDetails;
    DD_TIMING_INFO       TimingDetails;
} DD_DISPLAY_ACTIVE;

typedef struct _DD_GET_ACTIVE_DISPLAY_ARGS
{
    // The structure is used for getting the boot config. Only Intel pipes are valid here
    DD_DISPLAY_ACTIVE DisplayActive[MAX_PHYSICAL_PIPES];
} DD_GET_ACTIVE_DISPLAY_ARGS;

// Hot plug Event Args
#define DD_HOTPLUG_EVENT_NONE 0x0
#define DD_HOTPLUG_EVENT_SHORT_PULSE BIT0
#define DD_HOTPLUG_EVENT_LONG_PULSE BIT1

typedef struct _DD_DETECT_HOTPLUG_EVENT_ARGS
{
    DD_IN DD_PORT_TYPE Port;
    DD_IN DD_PORT_CONNECTOR_TYPE PortConnectorType;
    DD_OUT DDU8 HotplugEventFlags; // Bit 0: Short pulse, bit 1: Long pulse
} DD_DETECT_HOTPLUG_EVENT_ARGS_ST;

typedef struct _DD_DISPLAY_DETECT_ARGS
{
    DD_IN DD_TARGET_DESCRIPTOR Target;
    DD_IN BOOLEAN IsActiveDetection;          // Used in case of Hotplug event for first target on that port (LPI/SPI)
    DD_IN BOOLEAN IsPartialTopologyDetection; // called from IRQ Hotplug path, short pulse event
    DD_OUT BOOLEAN HasStatusChanged;          // used in case of hotplug detection to notify to OS
    DD_OUT DD_DISPLAY_CONNECTION_EVENTS ConnectionEvent;
} DD_DISPLAY_DETECT_ARGS;

typedef struct _DD_DETECTED_TARGETS
{
    DD_TARGET_DESCRIPTOR         TargetDescriptor;
    DD_DISPLAY_CONNECTION_EVENTS ConnectionEvent;
} DD_DETECTED_TARGETS;

typedef struct _DD_DISPLAY_ACTIVE_DETECT_ON_PORT_ARGS
{
    DD_IN DD_PORT_CONFIG_TYPE Port;
    DD_IN BOOLEAN IsPartialTopologyDetection; // called from IRQ Hotplug path, short pulse event
    DD_OUT DDU32 NumOfTargets;
    DD_OUT DD_DETECTED_TARGETS *pDetectedTargets;
} DD_DISPLAY_ACTIVE_DETECT_ON_PORT_ARGS;

typedef struct _DD_GET_EDID_ARGS
{
    DD_IN DD_TARGET_DESCRIPTOR TargetDesc;
    DD_IN DDU32 EdidOffset;
    DD_IN_OUT DDU32 EdidLengthInBytes;
    DD_OUT DDU8 *pEdid; // edid buffer
} DD_GET_EDID_ARGS;

// enum DD_SPI_EVENTS: List of Short Pulse HPD events
typedef enum _DD_SPI_EVENTS
{
    DD_SPI_NONE,
    DD_SPI_CONNECTION_EVENT,
    DD_SPI_LINK_LOSS_EVENT, // DP link retraining event, handled by OSL
    DD_SPI_ATR_EVENT,
    DD_SPI_PARTIAL_DETECTION_EVENT, // MST CSN
    DD_SPI_CP_EVENT,                // TODO: check if needed
    DD_SPI_CRC_ERROR_EVENT,         // To CRC error in PSR
    DD_SPI_MAX_EVENTS
} DD_SPI_EVENTS;

// struct DD_GET_SPI_DATA: Returns events for Short pulse HPD
typedef struct _DD_GET_SPI_DATA
{
    DD_IN DD_PORT_TYPE Port;
    DD_OUT DD_SPI_EVENTS Event;
} DD_GET_SPI_DATA;

#define DD_VDISP_MAX_EDID_BLOCKS 2

typedef struct _DD_VIRTUAL_DISP_HPD_ARGS
{
    BOOLEAN                    IsDisplayAttached;
    DD_VIDEO_OUTPUT_TECHNOLOGY OutputTechnology; // TBD
    DDU8                       SinkIndex;
    DDU8                       EdidSize;
    DDU8                       Edid[EDID_BLOCK_SIZE * DD_VDISP_MAX_EDID_BLOCKS];
    DD_2DREGION                NativeResolution;
} DD_VIRTUAL_DISP_HPD_ARGS;

//----------------------------------------------------------------------------
//
// Display detection and HPD/SPI related structures - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
//  InfoFrame related data structures -- START
//
//----------------------------------------------------------------------------
#define INFOFRAME_HEADER_SIZE 4

// InfoFrame Payload Length in bytes
// These are defined in iHDMI.h as well as iDP.h as well.
// Re-defining here to combine them
typedef enum _DD_INFOFRAME_LENGTH
{
    VS_LENGTH         = 27,  // Vendor Specific (VS), including IEEE reg ID, InfoFrame Payload Length
    AVI_LENGTH        = 13,  // Auxiliary Video Information (AVI) InfoFrame Payload Length
    GMP_LENGTH        = 28,  // Gamut MetaData Packet (GMP) InfoFrame Payload Length
    SPD_LENGTH        = 25,  // Source Product Description (SPD) InfoFrame Payload Length
    GCP_LENGTH        = 4,   // General Control Packet (GCP)InfoFrame Payload Length
    AUDIO_LENGTH      = 10,  // Audio InfoFrame Payload Length
    MS_LENGTH         = 10,  // MPEG Source InfoFrame Payload Length
    PR_PE_LENGTH      = 4,   // Length of PR_PE_TYPE
    AUDIO_CAPS_LENGTH = 4,   // Length of AUDIO_CAPS_TYPE
    PSR1_VSC_LENGTH   = 8,   // PSR1 Video Stream Configuration (VSC) SDP Packet max length
    PSR2_VSC_LENGTH   = 16,  // PSR2 VSC SDP Packet max length
    HDR_VSC_LENGTH    = 32,  // HDR VSC SDP Packet max length
    PPS_LENGTH        = 128, // Picture Parameter Set Max length
} DD_INFOFRAME_LENGTH;

// Data Island pkt type
// DIP_GCP is handled within setmode
typedef enum _DD_DIP_TYPE
{
    DIP_NONE = 0,
    DIP_AVI,
    DIP_VS,
    DIP_GMP,
    DIP_SPD,
    DIP_VSC,
    DIP_PPS,
    DIP_ALL = 31
} DD_DIP_TYPE;

// GCP Data
typedef union _DD_GCP_DATA {
    DDU32 Value;
    struct
    {
        DDU32 AvMute : 1;             // GCP_AV_MUTE
        DDU32 IndicateColorDepth : 1; // GCP_COLOR_INDICATION
        DDU32 Reserved : 30;          // Reserved
    };
} DD_GCP_DATA;

typedef enum _DD_AVI_INFO_OPERATION
{
    DD_SET_AVI_CUSTOM_INFO = 0,
    DD_GET_AVI_CUSTOM_INFO = 1,
    DD_SET_AVI_COLOR_INFO  = 2
} DD_AVI_INFO_OPERATION;

typedef struct _DD_AVI_INFO_ARGS
{
    DD_AVI_INFO_OPERATION OperationType;
    union {
        DD_COLOR_PIXEL_DESC * pOutputPixelFormat;
        AVI_INFOFRAME_CUSTOM *pCustomAviInfoFrame;
    };
    DD_TARGET_DESCRIPTOR TgtDesc;
} DD_AVI_INFO_ARGS;

typedef struct _DD_INFO_FRAME_ARGS
{
    BOOLEAN          Enable;
    DD_PORT_TYPE     Port;
    DDU32            Pipe;
    DD_PROTOCOL_TYPE Protocol;
    DD_DIP_TYPE      DipType;
    DDU32            DipSize;
    DDU8 *           pDipData;
} DD_INFO_FRAME_ARGS;

typedef struct _DD_DIP_ENABLE_ARGS
{
    DD_PORT_TYPE     Port;
    DDU32            Pipe;
    DD_PROTOCOL_TYPE Protocol;
    DD_DIP_TYPE      DipType;
    BOOLEAN          Enable;
} DD_DIP_ENABLE_ARGS;
//----------------------------------------------------------------------------
//
//  InfoFrame related data structures -- START
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// Static encoder data structures: Related enums and structures - START
//
//----------------------------------------------------------------------------

// Vendor and Product Identification: 10 bytes
typedef union _DD_PNP_ID {
    DDU8 VendorProductID[10]; // Vendor / Product identification
    struct
    {
        DDU8 ManufacturerID[2]; // Bytes 8, 9: Manufacturer ID
        DDU8 ProductID[2];      // Bytes 10, 11: Product ID
        DDU8 SerialNumber[4];   // Bytes 12 - 15: Serial numbers
        DDU8 WeekOfManufacture; // Byte 16: Week of manufacture
        DDU8 YearOfManufacture; // Byte 17: Year of manufacture
    };
} DD_PNP_ID;

//----------------------------------------------------------------------------
//
// DP/eDP encoder data related definitions
//
//----------------------------------------------------------------------------

#define DD_EDP_MAX_SUPPORTED_LINK_RATES 8

// DP/EDP supported LinkRates in MHZ
#define DP_LINKRATE_162_MHZ 162
#define DP_LINKRATE_216_MHZ 216
#define DP_LINKRATE_270_MHZ 270
#define DP_LINKRATE_324_MHZ 324
#define DP_LINKRATE_432_MHZ 432
#define DP_LINKRATE_540_MHZ 540
#define DP_LINKRATE_810_MHZ 810

typedef enum _DD_LANE_WIDTH
{
    LANE_UNDEFINED = 0,
    LANE_X1        = 1,
    LANE_X2        = 2,
    LANE_X3        = 3, // used only for MIPI
    LANE_X4        = 4,
} DD_LANE_WIDTH;

typedef enum _DD_DP_TRAINING_PATTERN
{
    DP_PAT_TRAINING_NOT_IN_PROGRESS = 0,
    DP_TRAINING_PAT_1               = 1,
    DP_TRAINING_PAT_2               = 2,
    DP_TRAINING_PAT_3               = 3,
    DP_PAT_D10_2_WITHOUT_SCRAMBLING = 4,
    DP_PAT_SYMBOL_ERR_MSR_CNT       = 5,
    DP_PAT_PRBS7                    = 6,
    DP_PAT_IDLE                     = 7,
    DP_PAT_SCRAMBLING               = 8,
    DP_PAT_HBR2_EYE_COMPLIANCE      = 9,
    DP_PAT_BITS80_CUSTOM            = 10,
    DP_PAT_PCT                      = 11,
    DP_TRAINING_PAT_4               = 12,
} DD_DP_TRAINING_PATTERN;

typedef enum _DD_PORT_SYNC_SUPPORT_STATUS
{
    DD_PORT_SYNC_NONE = 0,
    DD_PORT_SYNC_SW,
    DD_PORT_SYNC_HW
} DD_PORT_SYNC_SUPPORT_STATUS;

typedef enum _DD_DP_LINK_OPERATION_TYPE
{
    DP_OP_NONE = 0,
    DP_OP_PREPARE_FOR_LINK_TRAINING,
    DP_OP_ENABLE_PORT,
    DP_OP_SET_LINK_PATTERN,
    DP_OP_ADJ_DRIVE_SETTINGS,
    DP_OP_DISABLE_PORT_PLL,
} DD_DP_LINK_OPERATION_TYPE;

typedef enum _DD_DP_AUX_CHANNEL_TYPE
{
    AUX_CHANNEL_UNDEFINED = -1,
    AUX_CHANNEL_A,
    AUX_CHANNEL_B,
    AUX_CHANNEL_C,
    AUX_CHANNEL_D,
    AUX_CHANNEL_E,
    AUX_CHANNEL_F,
    AUX_CHANNEL_MAX,
} DD_DP_AUX_CHANNEL_TYPE;

typedef enum _DD_DP_VOLTAGE_SWING_LEVEL
{
    DP_VSWING_INVALID = -1,
    DP_VSWING_0_4     = 0,
    DP_VSWING_0_6     = 1,
    DP_VSWING_0_8     = 2,
    DP_VSWING_1_2     = 3,
    DP_VSWING_MAX     = 4,
} DD_DP_VOLTAGE_SWING_LEVEL;

typedef enum _DD_DP_PREEMPHASIS_LEVEL
{
    DP_PREEMP_INVALID        = -1,
    DP_PREEMP_NO_PREEMPHASIS = 0,
    DP_PREEMP_3_5DB          = 1,
    DP_PREEMP_6DB            = 2,
    DP_PREEMP_9_5DB          = 3,
    DP_PREEMP_MAX            = 4,
} DD_DP_PREEMPHASIS_LEVEL;

typedef struct _DD_DP_DRIVE_SETTING
{
    DD_DP_VOLTAGE_SWING_LEVEL SwingLevel;
    DD_DP_PREEMPHASIS_LEVEL   PreEmpLevel;
} DD_DP_DRIVE_SETTING;

typedef struct _DD_DP_REDRIVER_PARAMS
{
    BOOLEAN             IsDockablePort;           // EFP display is routed through Dock?
    BOOLEAN             IsOnBoardRedriverPresent; // Onboard Redriver Present
    DD_DP_DRIVE_SETTING OnBoardRedriverSettings;  // Onboard Redriver settings
    BOOLEAN             IsOnDockRedriverPresent;  // OnDock Redriver Present
    DD_DP_DRIVE_SETTING OnDockRedriverSettings;   // OnDock Redriver settings
} DD_DP_REDRIVER_PARAMS;

typedef struct _DD_MST_BW_DATA
{
    // DP MST data
    DDU8                   StreamId;
    DD_DP_RELATIVE_ADDRESS RAD; // RAD of the target device
    DDU8                   VcPayloadTableStartIdx;
    DDU8                   VcPayloadTableNumSlots; // number of VC payload table slots
    BOOLEAN                EnableMSTMode;          // MSTMode
    // This will indicate how much PBN will be actually needed
    DDU32 ActualPBN;
    // This will indicate how much PBN will be allocated based on
    // the number of slots, Link Rate &  Number Of Lanes
    DDU32 AllocatedPBN;
} DD_MST_BW_DATA;

// DP Data/Link M/N TU data
typedef struct _DD_M_N_CONFIG
{
    DDU32 DataM;
    DDU32 DataN;
    DDU32 LinkM;
    DDU32 LinkN;
    DDU32 DataTU;
} DD_M_N_CONFIG;

typedef struct _DD_M_N_CONFIG_ARGS
{
    DD_PORT_TYPE  Port;
    DDU32         Pipe;
    DD_M_N_CONFIG MNTUData;
} DD_M_N_CONFIG_ARGS;

typedef struct _DD_LINK_BW_DATA
{
    DDU32         LinkRateMHz;  ///< M Symbols per sec
    DDU32         DotClock;     ///< In hZ
    BOOLEAN       EnableSpread; ///< Enable down spreading
    DDU8          BitsPerPixel; ///< Bits per pixel. For compression supported panel, it will be output compression BPP.
    DD_M_N_CONFIG MNTUData;     ///< M/N TU data

    /**
    Port width selection for DP sink alone
    X1/X2/X4 mode. Default is X1
    enum used DP_PORT_WIDTH
    **/
    DD_LANE_WIDTH DpLaneWidthSelection;
    BOOLEAN       IsFecEnabled; ///< Boolean flag indicating whether FEC is to be enabled or not (Used in case of external DP compression.)
} DD_LINK_BW_DATA;

typedef enum DD_MSA_MISC1_BIT2_BIT1
{
    PIPE_S3D_DISABLED    = 0x00,
    PIPE_S3D_RIGHT_FRAME = 0x01,
    PIPE_S3D_LEFT_FRAME  = 0x03
} DD_MSA_MISC1_BIT2_BIT1;

typedef union _DD_MSA_MISC {
    DDU32 Value;
    struct
    {
        // ulMSA_Misc0                  : 8; // bits 7:0
        DDU32 SyncClock : 1;        // bit 0 (0-asysnchronous , 1- synchronous)
        DDU32 ComponentFormat : 2;  //  bits 2:1 (00 - RGB, 01 YCbCr 4:2:2, 10 YCbCr 4:4:4, 11 -reserved)
        DDU32 Range : 1;            // bit 3 (0- vesa, 1- cea)
        DDU32 YCbCrColorimetry : 1; // bit 4 (0 - ITU-R BT601-5, 1 - ITU-R BT709-5)
        DDU32 ColorDepth : 3;       // bit 7:5 (000 - 6 bits, 001 - 8 bits, 010 - 10 bits, 011 - 12 bits, 100 = 16 bits)

        // ulMSA_Misc1                  : 8; // bit 15:8
        DDU32                  MSA_Misc1_bit0 : 1;   // bit 0
        DD_MSA_MISC1_BIT2_BIT1 MSA_Misc1_bit2_1 : 2; //  bits 2:1
        DDU32                  MSA_Misc1_bit5_3 : 3; // bits 5:3
        DDU32                  MSA_Misc1_bit6 : 1;   // bit 6 VSC SDP to be used for sending colorimetry information.
        DDU32                  MSA_Misc1_bit7 : 1;   // bit 7

        DDU32 UNIQUENAME(Reserved) : 16; // bit 31:16
    };
} DD_MSA_MISC;

// DP Link specific information
typedef enum _DD_DP_LINK_STATE
{
    DD_DP_LINK_STATE_UNKNOWN = 0,
    DD_DP_LINK_TRAINING_REQUIRED,
    // DD_DP_LINK_RETRAINING_REQUIRED,
    DD_DP_LINK_TRAINED
} DD_DP_LINK_STATE;

typedef struct _DP_LINK_DATA
{
    DD_PORT_TYPE           Port;
    DD_LINK_BW_DATA        LinkBwData;
    DD_DP_DRIVE_SETTING    CurrentDriveSetting;
    BOOLEAN                EnhancedFramingEnable;
    BOOLEAN                ASSRSupport;
    BOOLEAN                EnableScrambling;
    DD_DP_LINK_STATE       LinkState; //!< Used in enable path to decide on Link Cfg requirement.
    BOOLEAN                IsFastLinkTrainingPossible;
    DD_DP_TRAINING_PATTERN ChanEqTrainingPat;
    DD_MST_BW_DATA         MstBwData;
    DD_MSA_MISC            MsaMisc;
    // BOOLEAN        IsLQAFailure;
    DD_DP_AUX_CHANNEL_TYPE AuxChannel;
} DP_LINK_DATA;

typedef struct _DD_PORT_SYNC_CAPS
{
    DD_PORT_SYNC_SUPPORT_STATUS Capability;
    DDU32                       MasterPipe; // used to indicate master pipe when PORT_SYNC_HW is used
    DDU32                       SlavePipe;  // used to indicate slave pipe when PORT_SYCH_HW is used
} DD_PORT_SYNC_CAPS;

//----------------------------------------------------------------------------
//
// DP/eDP encoder data related definitions - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// HDMI related enums/structures - START
//
//----------------------------------------------------------------------------

typedef enum _DD_HDMI_DATARATE
{
    DATARATE_MAX       = 0,
    DATARE_2_97_GT_S   = 1,
    DATARATE_1_65_GT_S = 2,
} DD_HDMI_DATARATE;

#define HDMI_DATARATE_165 165000000
#define HDMI_DATARATE_297 297000000
#define HDMI_DATARATE_594 594000000

// HDMI specfic information
typedef struct _HDMI_LINK_DATA
{
    DD_PORT_TYPE Port;
    DDU32        DotClock;
    BOOLEAN      EnableScrambling;
} HDMI_LINK_DATA;

//----------------------------------------------------------------------------
//
// HDMI related enums/structures - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// eDP and PSR related enums/structures - START
//
//----------------------------------------------------------------------------

typedef enum _DD_EDP_SWING_TABLE
{
    LOW_POWER_SWING_TABLE = 0,
    DEFAULT_SWING_TABLE
} DD_EDP_SWING_TABLE;

typedef enum _DD_LINES_TO_WAIT
{
    LINES_TO_WAIT_0 = 0,
    LINES_TO_WAIT_2,
    LINES_TO_WAIT_4,
    LINES_TO_WAIT_8
} DD_LINES_TO_WAIT;

typedef enum _DD_TP1_WAKEUPTIME
{
    TP1_WAKEUP_TIME_500_US = 0,
    TP1_WAKEUP_TIME_100_US,
    TP1_WAKEUP_TIME_2P5_MS,
    TP1_WAKEUP_TIME_0_SKIP,
} DD_TP1_WAKEUPTIME;

typedef enum _DD_TP2_WAKEUPTIME
{
    TP2_WAKEUP_TIME_500_US = 0,
    TP2_WAKEUP_TIME_100_US,
    TP2_WAKEUP_TIME_2P5_MS,
    TP2_WAKEUP_TIME_0_SKIP,
} DD_TP2_WAKEUPTIME;

typedef struct _DD_PSR_DISPLAY_CAPS
{
    // VBT Sepcific
    BOOLEAN           IsPSREnabled;
    BOOLEAN           IsLinkinStandbySupported;
    BOOLEAN           IsSkipHandShakeOnExit;
    DDU8              IdleFramesNum;
    DD_LINES_TO_WAIT  LinesNeededForLinkStandby;
    DD_TP1_WAKEUPTIME TP1WakeUpTime;
    DD_TP2_WAKEUPTIME TP2TP3WakeUpTime;

    // Port Specific Psr Details
    union {
        DDU8 PSRPortDetails;
        struct
        {
            DDU8 IsPSRSupported : 1; // PSR
            DDU8 IsSUSupported : 1;  // PSR2 Support
            DDU8 IsSfuSupported : 1; // MBO support
            DDU8 ReservedForPort : 5;
        };
    };

    // Sink Specific PSR Details
    union {
        DDU16 PSRSinkDetails;
        struct
        {
            DDU16 IsSinkPSRCapable : 1;
            DDU16 IsNoLinkTraingRequiredOnExit : 1; // 0 (default) - Link training is required
            DDU16 IsMaskMemUp : 1;                  // 1 - Mask Memory Up event
            DDU16 IsMaskMaxSleep : 1;               // 1 - Mask Max Sleep Time Out event
            DDU16 IsMaskHotPlug : 1;                // 1 - Mask Hot plug event
            DDU16 IsLinkinStandby : 1;
            DDU16 IsTP3Supported : 1;       // 1 for TPS3, 0 for TPS2
            DDU16 IsTP4Supported : 1;       // 1 for TPS4, 0 for TPS2
            DDU16 IsYcordRequiredInVSC : 1; // Y cordinate in VSC
            DDU16 IsFrameSyncRequired : 1;
            DDU16 ReservedForSink : 6;
        };
    };

    DDU8    MaxPSRSleepTime;
    BOOLEAN IsPSRInitialized; // For First time initialization of PSR Capabilities

} DD_PSR_DISPLAY_CAPS;

typedef struct _DD_EDP_FLT_PARAMS
{
    DDU32                     LinkRateMHz;        // Link Rate in M Symbols ps
    DD_LANE_WIDTH             NumOfLanesInUse;    // Lane Count to be used of type DD_LANE_WIDTH
    DD_DP_PREEMPHASIS_LEVEL   CurrentPreEmpLevel; // Pre-Emphasis to be used of type DD_DP_PREEMPHASIS_LEVEL
    DD_DP_VOLTAGE_SWING_LEVEL CurrentSwingLevel;  // Vswing to be used of type DD_DP_VOLTAGE_SWING_LEVEL
} DD_EDP_FLT_PARAMS;

typedef struct _DD_APICAL_IP_TABLE
{
    DDU32 PanelIeeeOui;        // Apical IP specific field for Panel OUI
    DDU32 DpcdBaseAddress;     // Apical IP specific field for DPCD Base address
    DDU32 DpcdIrdidixControl0; // Apical IP specific field for DPCD Idridix Control 0
    DDU32 DpcdOptionSelect;    // Apical IP specific field for DPCD option select
    DDU32 DpcdBacklight;       // Apical IP specific field for DPCD backlight
    DDU32 AmbientLight;        // Apical IP specific field for Ambient light
    DDU32 BacklightScale;      // Apical IP specific field for Backlight scale
} DD_APICAL_TABLE;

typedef struct _DD_EDP_APICAL_PARAMS
{
    DDU16           ApicalAsrtDispIpEnable; // Apical Assertive Display IP Enable
    DD_APICAL_TABLE ApicalTable;            // Apical Assertive Display IP Table
} DD_EDP_APICAL_PARAMS;
//----------------------------------------------------------------------------
//
// eDP and PSR related enums/structures - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// Mipi related enums/structures - START
//
//----------------------------------------------------------------------------

typedef struct _DD_DPHY_PARAMS
{
    DDU8  TClkPrepare;         // TClkPrepare value
    DDU8  TClkTrail;           // ucTClkTrail value
    DDU16 TClkPrepare_ClkZero; // usTClkPrepare + ClkZero value

    DDU8  THSPrepare;        // THSPrepare Value
    DDU16 THSPrepare_HSZero; // ucTHSPrepare + HSZero value
    DDU8  THSTrail;          // THSTrail Value
    DDU8  TLpx;
} DD_DPHY_PARAMS;

typedef enum _DD_MIPI_MODE
{
    MIPI_VIDEO_MODE_NON_BURST_SYNC_PULSE = 1,
    MIPI_VIDEO_MODE_NON_BURST_SYNC_EVENTS,
    MIPI_VIDEO_MODE_BURST,
    MIPI_COMMAND_MODE
} DD_MIPI_MODE;

typedef enum _DD_MIPI_LINK_CONFIG
{
    MIPI_SINGLE_LINK = 0,
    MIPI_DUAL_LINK_FRONT_BACK,
    MIPI_DUAL_LINK_PIXEL_ALTERNATIVE
} DD_MIPI_LINK_CONFIG;

typedef enum _DD_LP_BYTECLK_SEL
{
    CLOCK_20MHZ = 0,
    CLOCK_10MHZ,
    CLOCK_5MHZ
} DD_LP_BYTECLK_SEL;

typedef enum _DD_SEQUENCE_TYPE
{
    SEQ_UNDEFINED = 0,
    SEQ_ASSERT_RESET,
    SEQ_SEND_DCS,
    SEQ_DISPLAY_ON,
    SEQ_DISPLAY_OFF,
    SEQ_DE_ASSERT_RESET,
    SEQ_BKLT_ON,
    SEQ_BKLT_OFF,
    SEQ_TEAR_ON,
    SEQ_TEAR_OFF,
    SEQ_POWER_ON,
    SEQ_POWER_OFF,
    SEQ_MAX
} DD_SEQUENCE_TYPE;

typedef enum _DD_SEQ_OP_BYTE
{
    SEQ_OP_UNDEFINED = 0,
    SEQ_OP_SEND_PACKET,
    SEQ_OP_DELAY,
    SEQ_OP_PROG_GPIO,
    SEQ_OP_PROG_I2C,
    SEQ_OP_PROG_SPI,
    SEQ_OP_PROG_PMIC,
    SEQ_OP_MAX
} DD_SEQ_OP_BYTE;

#pragma pack(1)

typedef struct _DD_SEQ_GPIO_FLAGS
{
    union {
        DDU8 GpioFlags;
        struct
        {
            DDU8 GPIOVal : 1;              // Bit0 GPIO pin state [0 - Pull GPIO pin to low; 1 - PullGPIO Pin to high]
            DDU8 UNIQUENAME(Reserved) : 7; // Bits [7:1] - Reserved
        };
    };
} DD_SEQ_GPIO_FLAGS;

typedef struct _DD_SEQ_GPIO_PROG
{
    DDU8              SeqOperationType;
    DDU8              SizeOfDelay;
    DDU8              GpioResourceIndex;
    DDU8              GpioNumber;
    DD_SEQ_GPIO_FLAGS GPIOFlags;
} DD_SEQ_GPIO_PROG;

typedef struct _DD_SENDPKT_CMD_FLAG
{
    union {
        DDU8 CmdFlag;
        struct
        {
            DDU8 PktTransmissionMode : 1; // 0 - Low Power Mode, 1 - High Speed Mode
            DDU8 VirtualChannel : 2;      // Virtual channel # (0 - 3)
            DDU8 PortType : 2;            // 00 - Mipi - A, 01 - Mipi - C
            DDU8 Rsvd : 3;                // Reserved
        };
    };
} DD_SEQ_CMD_FLAG;

typedef enum _DD_SENDPKT_DATA_TYPE
{
    DATA_TYPE_GENERIC_SHORT_WRITE_NO_PARAMETERS_BXT                         = 0x3,
    DATA_TYPE_GENERIC_READ_NO_PARAMETERS_BXT                                = 0x4,
    DATA_TYPE_MANUFACTURER_DCS_SHORT_WRITE_NO_PARAMETER_BXT                 = 0x5,
    DATA_TYPE_MANUFACTURER_DCS_READ_NO_PARAMETER_BXT                        = 0x6,
    DATA_TYPE_COMPRESSION_MODE_DATA_TYPE_WRITE_SHORT_WRITE_2_PARAMETERS_BXT = 0x7,
    DATA_TYPE_PPS_LONG_WRITE_BXT                                            = 0xA,
    DATA_TYPE_GENERIC_SHORT_WRITE_1_PARAMETER_BXT                           = 0x13,
    DATA_TYPE_GENERIC_READ_1_PARAMETER_BXT                                  = 0x14,
    DATA_TYPE_MANUFACTURER_DCS_SHORT_WRITE_1_PARAMETER_BXT                  = 0x15,
    DATA_TYPE_GENERIC_SHORT_WRITE_2_PARAMETERS_BXT                          = 0x23,
    DATA_TYPE_GENERIC_READ_2_PARAMETER_BXT                                  = 0x24,
    DATA_TYPE_GENERIC_LONG_WRITE_BXT                                        = 0x29,
    DATA_TYPE_MANUFACTURER_DCS_LONG_WRITE_BXT                               = 0x39,
} DD_SENDPKT_DATA_TYPE;

typedef struct _DD_SEQ_SEND_PACKET_HEADER
{
    DDU8            SeqOperationType;
    DDU8            SizeOfSendPkt; // 4 + N bytes
    DD_SEQ_CMD_FLAG SendPktCmdFlag;
    DDU8            SendPktDataType; // Of type DD_SENDPKT_DATA_TYPE
    DDU16           WordCount;       // Word count
} DD_SEQ_SEND_PACKET_HEADER;

typedef struct _DD_MIPI_PACKET
{
    DD_SENDPKT_DATA_TYPE DataType;            // Type of MIPI data: Short/Long/with param
    DDU8                 VirtualChannel;      // Virtual channel
    BOOLEAN              PktTransmissionMode; // LP or HS. HS = 1
    DDU16                WordCount;           // Number of bytes to be sent
    DDU8 *               pData;               // Can have multi-byte data for long write
    DD_PORT_TYPE         PortType;            // MIPI port the command needs to be sent to
} DD_MIPI_PACKET;

typedef struct _DD_SEQ_DELAY
{
    DDU8  SeqOperationType;
    DDU8  SizeOfDelay;
    DDU32 Delay; // Delay value
} DD_SEQ_DELAY;

typedef struct _DD_GPIO_FLAG
{
    union {
        DDU8 GpioFlag;
        struct
        {
            DDU8 PullDirection : 1; // 0 - Pull GPIO Low, 1 - Pull GPIO high
            DDU8 Rsvd : 7;          // Reserved
        };
    };
} DD_GPIO_FLAG;

typedef struct _DD_SEQ_PROG_I2C
{
    DDU8 SeqOperationType;
    DDU8 SizeOfProgI2c; // 7 + N bytes

    DDU8  I2cFlag;          // Rsvd for future
    DDU8  I2cResourceIndex; // For Windows, this comes as part of I2C resource ACPI enumeration from OS
    DDU8  I2cBusNumber;     // Un-used in Windows
    DDU16 I2cSlaveAddress;  // Un-used in Windows (10-bit slave address)
    DDU8  I2cRegOffset;     // Register offset
    DDU8  I2cPayloadSize;   // Size of Data to be sent over I2C
} DD_SEQ_PROG_I2C;

typedef struct _DD_SEQ_PROG_SPI
{
    DDU8 SeqOperationType;
    DDU8 SizeOfProgSPI; // 6 + N bytes

    DDU8 SpiFlag;          // Rsvd for future
    DDU8 SpiResourceIndex; // For Windows, this comes as part of SPI resource ACPI enumeration from OS
    DDU8 SpiBusNumber;     // Un-used in Windows
    DDU8 SpiSlaveAddress;  // Un-used in Windows (10-bit slave address)
    DDU8 SpiRegOffset;     // Register offset
    DDU8 SpiPayloadSize;   // Size of Data to be sent over I2C
} DD_SEQ_PROG_SPI;

typedef struct _DD_SEQ_PROG_PMIC
{
    DDU8  SeqOperationType;
    DDU8  SizeOfProgPmic;   // 15 bytes
    DDU8  PmicFlag;         // Rsvd for future
    DDU16 PmicSlaveAddress; // PMIC slave address
    DDU32 PmicRegOffset;    // PMIC register offset
    DDU32 PmicRegData;      // PMIC register value to be written
    DDU32 PmicRegDataMask;  // PMIC register Mask
} DD_SEQ_PROG_PMIC;

#pragma pack()

//----------------------------------------------------------------------------
//
// Mipi related enums/structures - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// LFP and PowerCons related definitions - START
//
//----------------------------------------------------------------------------

typedef struct _DD_CHROMA_AND_LUMA_DATA
{
    BOOLEAN OverrideLumaAvailable;
    BOOLEAN OverrideGammaAvailable;
    BOOLEAN OverrideChromaAvailable;

    // Color primaries data
    DDU16 RedX;
    DDU16 RedY;
    DDU16 GreenX;
    DDU16 GreenY;
    DDU16 BlueX;
    DDU16 BlueY;
    DDU16 WhiteX;
    DDU16 WhiteY;

    // Luminance data
    DDU16 MinLuminance;
    DDU16 MaxLuminance;
    DDU16 MaxFullFrameLuminance;

    // Gamma
    DDU8 Gamma;
} DD_CHROMA_AND_LUMA_DATA;

typedef struct _DD_PANEL_DIMENSIONS
{
    DDU16 PanelWidth;  // Panel Width as given in LVDS panel DTD
    DDU16 PanelHeight; // Panel Height as given in LVDS panel DTD
} DD_PANEL_DIMENSIONS;

typedef struct _DD_PPS_DELAY_TABLE
{
    DDU16 PowerOnDelay;           // T3 -  Power-Up delay.
    DDU16 PowerOnToBkltOnDelay;   // T8  - Power-On to Backlight Enable delay.
    DDU16 BkltOffToPowerOffDelay; // T9  - Backlight-Off to Power-Down delay.
    DDU16 PowerOffDelay;          // T10 - Power-Down delay.
    DDU16 PowerCycleDelay;        // T12 - Power cycle delay
    DDU16 PwmOnToBkltOnDelay;     // Tx -  PWM On to Bklt On Delay
    DDU16 BkltOffToPwmOffdelay;   // Ty  - Bklt OFF to PWM Off Delay
} DD_PPS_DELAY_TABLE;

// DPST Related
#define DPST_BIN_COUNT 32        // Total number of segments in DPST
#define DPST_DIET_ENTRY_COUNT 33 // Total number of DIET entries

typedef enum _DD_DPST_OPERATION
{
    DD_DPST_HISTOGRAM_ENABLE = 0,
    DD_DPST_HISTOGRAM_DISABLE,
    DD_DPST_HISTOGRAM_RESET,
    DD_DPST_HISTOGRAM_STATUS,
    DD_DPST_HISTOGRAM_UPDATE_GUARDBAND,
    DD_DPST_PROGRAM_DIET_REGS
} DD_DPST_OPERATION;

typedef struct _DD_DPST_HISTOGRAM
{
    DDU32 Status[DPST_BIN_COUNT]; // Current histogram segment values
    DDU32 Mask;                   // Mask used for reading histogram data
} DD_DPST_HISTOGRAM;

typedef struct _DD_DPST_ARGS
{
    PIPE_ID           PipeId;
    DD_DPST_OPERATION DpstOpReq; // Operation Request
    DD_DPST_HISTOGRAM Histogram;
    DDU32             GuardBandThreshold;
    DDU32             InterruptDelay;
    BOOLEAN           IsProgramDiet;
    DDU32             DietFactor[DPST_DIET_ENTRY_COUNT];
} DD_DPST_ARGS;
typedef enum _DD_GETSET_CABC_BLC_PARAMS
{
    DD_GET_BRIGHTNESS = 0,
    DD_SET_BRIGHTNESS,
    DD_SET_CABC_AGRESSIVENESS_LEVEL
} DD_GETSET_CABC_BLC_PARAMS;

typedef enum _SB_CABC_MODES
{
    CABC_OFF = 0,
    CABC_POWERSAVE_LOW,
    CABC_POWERSAVE_MEDIUM,
    CABC_POWERSAVE_HIGH
} SB_CABC_MODES;

typedef struct _SB_GETSET_CABC_BLC_ARGS
{
    DDU32                     DisplayUID;          // Display ID on which CABC has to be enabled
    DD_GETSET_CABC_BLC_PARAMS GetSetCABCBlcParams; // CABC BLC Operation to be performed
    DDU32                     BrightnessValue;     // Brightness value to get/set
    DDU32                     Maxbrightness;       // Max Brightness value to be used (Constant from PC)
    SB_CABC_MODES             CABCMode;            // CABC mode (Agressiveness level equivalant from OS)
    DD_PORT_TYPE              PortType;            // Port Type (Internal parameter to SB, not passed from PC)
} SB_GETSET_CABC_BLC_ARGS;

typedef enum _DD_PWM_POLARITY
{
    PWM_POLARITY_NORMAL = 0, // Normal polarity (0 = full off)
    PWM_POLARITY_INVERSE     // Inverse polarity (0 = full on)
} DD_PWM_POLARITY;

typedef enum _DD_CABC_MODE
{
    DD_CABC_OFF = 0,
    DD_CABC_POWERSAVE_LOW,
    DD_CABC_POWERSAVE_MEDIUM,
    DD_CABC_POWERSAVE_HIGH
} DD_CABC_MODE;

typedef struct _DD_BLC_PARAMS
{
    DD_BLC_OPERATION BlcOperation; // Set Brightness, Set Aggressiveness
    DD_PORT_TYPE     Port;
    DDU16            BrightnessPercent;
    DD_CABC_MODE     CabcMode;
} DD_BLC_PARAMS;
//----------------------------------------------------------------------------
//
// LFP and PowerCons related definitions - END
//
//----------------------------------------------------------------------------

// Static encoder Final data structures - START

typedef struct _DD_IBOOST_SETTINGS
{
    BOOLEAN IsIBoostEnabled; // iBoot feature
    DDU8    IBoostMagnitude; // iBoost Magnitude; Platform dependant enum
} DD_IBOOST_SETTINGS;

typedef struct _DD_DP_DATA
{
    DD_PORT_CONNECTOR_TYPE PortConnectorType;      // Port Connector Type Normal port/USB-C/Thunderbolt port
    DDU8                   DpPortTraceLength;      // DP port trace length; This field is platform specific, See Vbt Spec for definitions
    BOOLEAN                IsLSPCONPresent;        // LSCON *present
    BOOLEAN                IsSscEnabled;           // SSC enabled/disabled
    BOOLEAN                IsSscEnabledForDongles; // SSC enabled/disabled for dongles

    DD_DP_AUX_CHANNEL_TYPE AuxChannelNum; // derived from VBT AUX_CHANNEL_TYPE

    DD_DP_REDRIVER_PARAMS DpRedriverParams; // Redriver Settings

    DD_IBOOST_SETTINGS IBoostSettings; // I-boost settings

    BOOLEAN IsCompressionEnabled; // VESA DSC compression enabled?

    BOOLEAN IsDPCompatible;
    BOOLEAN IsHDMICompatible;
} DD_DP_DATA;

typedef struct _DD_HDMI_DATA
{
    DDU8  DdcPinPairIndex;  // GMBUS pin pair Index from VBT to read HDMI/DVI EDID/panel params. Values are platform independant from CNL
    DDU8  HDMILSIndexValue; // HDMI Level Shifter Index; Platform dependant structure
    DDU32 HDMIDataRate;     // HDMI data rate defines of type HDMI_DATARATE

    DD_IBOOST_SETTINGS IBoostSettings; // I-boost settings

    BOOLEAN IsDPCompatible;
    BOOLEAN IsHDMICompatible;
} DD_HDMI_DATA;

typedef struct _DD_EDP_DATA
{
    BOOLEAN      IsDualPipeEdpEnabled; // Dual pipe eDP support
    DD_PORT_TYPE SlavePortType;        // Slave eDP port type when Dual pipe eDP support is enabled

    DD_EDP_SWING_TABLE  EdpSwingTableSelector; // eDP Swing Table selection
    DD_PSR_DISPLAY_CAPS PsrParams;             // PSR config params from VBT

    BOOLEAN           IsFltParamsfromVbtUsed; // Option to indicate if to use eDP Fast Link Training params from VBT
    DD_EDP_FLT_PARAMS EdpFltParams;           // eDP FLT parameters

    BOOLEAN IsEdpT3OptimizationEnabled; // T3 optimization to be enbabled for eDP

    // BOOLEAN               IsEdpFullLTParamsUsed;  // Option to indicate if to use eDP Full Link Training start params from VBT
    // EDP_LT_START_PARAMS   steDPStartParams;       // eDP Full link training parameters
    DD_EDP_APICAL_PARAMS ApicalParams; // eDP apical display params
} DD_EDP_DATA;

typedef struct _DD_SEQBLOCK
{
    DDU8  SequenceBlockVersion;
    DDU32 SequenceBlockSize;
    DDU8 *pSequence[SEQ_MAX]; // Pointer array of all sequences
} DD_SEQBLOCK;

/**
 * @brief enum  DD_EDID_TYPE
 *
 * Describes the source of edid
 */
typedef enum _DD_EDID_TYPE
{
    DD_EDID_DEFAULT = 0,
    DD_EDID_INF,
    DD_EDID_FAKE,
    DD_EDID_OS_OVERRIDE,
    DD_EDID_VBT,
    DD_EDID_BIOS,
} DD_EDID_TYPE_EN;
#define MAX_MIPI_PORTS 2
#define MAX_EDID_EXTENSIONS_SUPPORTED 4

#define MONITOR_NAME_LENGTH 13 // Should be same as Edid_structs.h definition

typedef struct _DD_MIPI_DATA
{
    DD_MIPI_MODE        MipiMode;       // Video transfer mode
    DD_MIPI_LINK_CONFIG MipiLinkConfig; // DUal link caps
    BOOLEAN             CABCSupported;  // CABC support
    BOOLEAN             BTADisable;     // BTA feature enable/disable
    DDU8                LaneCount;      // Lane count of MIPI panel
    DD_BPC_SUPPORTED    PanelBpc;       // Panel color depth
    DDU32               DsiDataRate;
    BOOLEAN             FlipRGB;                           // Flip the order of sending of RGB data to panel
    DD_PORT_TYPE        CABCCtrlOnOffPort[MAX_MIPI_PORTS]; // Option to know CABC on/off commands to be sent to port-A/C or both
    DD_PORT_TYPE        CABCPwmOnOffPort[MAX_MIPI_PORTS];  //  Option to know CABC PWM on/off commands to be sent to port-A/C or both
    DDU32               RequiredBurstModeFreq;             // DSI frequency to be used in Command mode or when "Burst mode is selected in "ulVideoTransferMode"
    DD_LP_BYTECLK_SEL   LPByteClock;                       // Escape clock frequency to be used
    BOOLEAN             EoTDisable;                        // EoT to be disabled? (Can we remove this?)
    BOOLEAN             ClockStopEnable;                   // Clock stop feature enable/disable
    DD_DPHY_PARAMS      DPhyParams;                        // Dphy parameters
    BOOLEAN             CompressionEnabled;                // VESA DSC compression enabled?
    DD_SEQBLOCK         MipiSequenceBlock;                 // Mipi seuqence Block
    DDU8                PixelOverlapCount;
} DD_MIPI_DATA;

typedef struct _DD_LFP_DATA
{
    // Parameters required for Fake EDID/override EDID caps
    DDU8                    PanelName[MONITOR_NAME_LENGTH]; // Panel name string
    DD_PNP_ID               PnpID;                          // PnP ID for the panel
    DD_BPC_SUPPORTED        ColorDepth;                     // Panel color depth
    DD_CHROMA_AND_LUMA_DATA ChromaAndLumaData;              // Data for color primries and Luminance

    // For downscaling feature: Will re-check if this is needed during implementation
    BOOLEAN             IsDownScalingEnabled; // Panel downscaling enabled/disabled; Need to be evaluated
    DD_PANEL_DIMENSIONS PanelDimensions;      // Panel X/Y resolution; to be used if we support downscaling

    DD_PPS_DELAY_TABLE PpsDelayTable; // Panel Power sequencing Params from VBT
    DD_BLC_FEATURES    BlcParams;     // Backlight control Params from VBT

    DD_DPS_PANEL_TYPE DpsPanelType; // DRRS panel type (static/seamless)

    // BOOLEAN              ForceLCDVCCOnS0;           // Force LVD VCC RCR during monitor OFF; Need to be evaluated

    DDU8 PixelOverlapCount; // Pixel Overlap count (applicable for MIPI and eDP)

    union {
        DD_EDP_DATA  EdpData;  // EDP specific data
        DD_MIPI_DATA MipiData; // Mipi specific data
    };
} DD_LFP_DATA;

typedef struct _DD_ENCODER_INITIALIZATION_DATA
{
    DD_PORT_TYPE        Port;       // Derived from VBT_PORT_TYPE
    DD_PORT_CONFIG_TYPE PortConfig; // Derived from DEVICE_CLASS_DEFN

    BOOLEAN IsInternalDisplay;  // Derived from DEVICE_CLASS_DEFN
    BOOLEAN IsLaneReversed;     // Lane reversal; 0 - Disabled, 1 - Enabled
    BOOLEAN IsHPDSenseInverted; // HPD Sense Invert for Encoder; 0 - No Inversion needed, 1 - Inversion needed

    BOOLEAN        IsEdidSupportedPanel; // Is EDID supported panel?
    DD_TIMING_INFO TimingInfo;           // Timing Info if panel does not have EDID

    DD_DP_DATA   DpData;   // DP/eDP related static data
    DD_HDMI_DATA HdmiData; // HDMI related static data

    DD_LFP_DATA LfpData; // LFP encoder specific data
} DD_ENCODER_INITIALIZATION_DATA;

typedef struct _DD_GET_ENCODER_DATA
{
    DD_OUT DDU32 TotalNumIntEncoders;                        // Will return total number of integrated encoders in VBT when "pProtocolPortCtxData" is NULL
    DD_OUT DD_ENCODER_INITIALIZATION_DATA *pEncoderInitData; // Protocol Context Data for all the encoders (TotalNumIntEncoders)
    DD_OUT DDU32 TotalNumVirtEncoders;                       // Will return total number of integrated encoders in VBT when "pProtocolPortCtxData" is NULL
} DD_GET_ENCODER_DATA;

typedef struct _DD_TARGET_DETECT_ARGS
{
    DD_IN DD_TARGET_DETECT_TYPE TargetDetectType;
    DD_IN DDU32 TargetId;        // valid only if target detect type is DETECT_ONE
    DD_IN DD_PORT_TYPE PortType; // valid only if target detect type is DETECT_ALL_ON_PORT
    DD_IN BOOLEAN PartialDetection;
    DD_OUT BOOLEAN HasPhysicalDisplay;
} DD_TARGET_DETECT_ARGS;

typedef struct _DD_TARGET_LFP_INFO
{
    DD_TARGET_DESCRIPTOR LfpTargetDescriptor[DD_LFP_MAX];
    DDU8                 NumEnumeratedLfps;
} DD_TARGET_LFP_INFO;

// Static encoder Final data structures - END

//----------------------------------------------------------------------------
//
// Static encoder data structures: Related enums and structures - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// VBT/Opregion Interface structures - START
//
//----------------------------------------------------------------------------

//  VBT/Opregion Platform Parameters
typedef struct _DD_VBT_OPREGION_PLATFORM_PARAMS
{
    // Below data comes from VBT
    // BOOLEAN  bIgnoreStrapState;       // TBD: Is this needed anymore?
    BOOLEAN IsHeadlessSupportForKVMREnabled; //
    BOOLEAN Is180DegreeRotationEnabled;      //
    BOOLEAN IsEmbeddedPlatform;              //
    BOOLEAN IsDisplayDisabledPlatform;       //
    DDU8    VBIOSMinorVersion;               //
    DDU16   MaxBSModeXRes;                   // Max X resolution that can be supported by legacy displays (e.g. EDID less CRTs)
    DDU16   MaxBSModeYRes;                   // Max Y resolution that can be supported by legacy displays (e.g. EDID less CRTs)
    DDU8    MaxBSModeRRate;                  // Max RR that can be supported by legacy displays (e.g. EDID less CRTs)

    // Below data comes from Opregion
    DDU8    GopVersion[0x20]; // GOP version
    BOOLEAN IsS0ixCapable;
    BOOLEAN IsISCTCapable;
    BOOLEAN IsDGPUPresent;
    // DD_PLATFORM_CONFIG   PlatformConfig;         // Platform configuration
} DD_VBT_OPREGION_PLATFORM_PARAMS;

typedef enum _OPREGION_NOTIFY_STATUS
{
    NOTIFY_SUCCESS = 0x00,
    NOTIFY_FAILURE,
    NOTIFY_PENDING,
    NOTIFY_DISPATCHED
} OPREGION_NOTIFY_STATUS;

typedef enum _DD_OPREGION_EVENT
{
    OPREGION_EVENT_UNKNOWN = 0,
    OPREGION_HOTKEY_EVENT,
    OPREGION_LID_EVENT,
    OPREGION_DOCK_EVENT,
    OPREGION_GET_DUTY_MAPPING_TABLE,
    OPREGION_GET_BRIGHTNESS
} DD_OPREGION_EVENT;

typedef struct _DD_OPREGION_MB3_FIELD_ARGS
{
    void *pData;
    DDU32 DataSize;
} DD_OPREGION_MB3_FIELD_ARGS;

typedef struct _DD_GET_OPREGION_EVENT
{
    OPREGION_NOTIFY_STATUS     OpRegNotifyStatus;
    DD_OPREGION_EVENT          OpregionEvent;
    BOOLEAN                    IsLidOpen; // Lid Status
    BOOLEAN                    IsDocked;  // Dock Status
    DD_OPREGION_MB3_FIELD_ARGS Mb3FieldArgs;
} DD_GET_OPREGION_EVENT;

typedef struct _DD_GET_VBT
{
    DDU8 *pVbtData; // VBT Data from Opregion
} DD_GET_VBT;

typedef struct _DD_GET_EDID
{
    DDU8 *pEdidData; // EDID Data from Opregion
} DD_GET_EDID;

// Opregion Set Event
typedef enum _DD_OPREGION_SET_EVENT
{
    OPREGION_INDICATE_DRIVER_READY = 0,
    OPREGION_NOTIFY_DRIVER_STATUS,
    OPREGION_NOTIFY_STS_FAILURE_REASON,
    OPREGION_SET_ASL_SLEEP_TIMEOUT,
    OPREGION_SET_SUPPORTED_DISPLAYS,
    OPREGION_SET_BLC,
    OPREGION_SET_PFMB,
    OPREGION_SET_BRIGHTNESS,
} DD_OPREGION_SET_EVENT;

// Evant Values for different events above
#define ASL_TIME_OUT_VALUE 750 // As per ACPI Opregion SAS v0.6 Rev 0.3

typedef enum _OPREGION_DRDY_STATUS
{
    DRIVER_NOT_READY = 0,
    DRIVER_READY
} OPREGION_DRDY_STATUS;

////Opregion defined error messages
// typedef enum _OPREGION_NRDY_REASON
//{
//    ACPI_FAILURE_DRIVER_NOT_INITIALIZED = 0x00,
//    ACPI_FAILURE_3D_APP_RUNNING,
//    ACPI_FAILURE_OVERLAY_ACTIVE,
//    ACPI_FAILURE_FSDOS_ACTIVE,
//    ACPI_FALIURE_RESOURCE_IN_USE,
//    ACPI_FALIURE_DRIVER_IN_LOW_POWER_TRANSITION,
//    ACPI_FAILURE_EXTENDED_DESKTOP_ACTIVE,
//    ACPI_FAILURE_FATAL,
//
//    // Don't add driver defined err messages here!
//
//    //Driver defined error messages
//    ACPI_FAILURE_LVDS_PWR_STATE_CHANGE_FAILED = 0x101,
//    ACPI_FAILURE_NO_CHANGE_IN_CONFIG,
//    ACPI_FAILURE_GET_NEXT_CONFIG_FROM_EM_FAILED,
//    ACPI_FAILURE_GET_EM_HOTKEY_LIST_FAILED,
//    ACPI_FAILURE_TURN_OFF_ALL_DISPLAYS,
//    ACPI_FAILURE_GET_DISP_INFO_FAILED,
//    ACPI_FAILURE_INVALID_ASL_NOTIFICATION,
//    ACPI_FAILURE_INVALID_BUFFER_SIZE,
//    ACPI_FAILURE_EM_NOT_INITIALIZED,
//    ACPI_FAILURE_TMM_ACTIVE
//}OPREGION_NRDY_REASON;

typedef struct _DD_SET_OPREGION_EVENT
{
    DD_OPREGION_SET_EVENT      OpregionEvent;
    DDU32                      EventValue; // Value to write in Opregion, varies between every Set Event type
    DD_OPREGION_MB3_FIELD_ARGS Mb3FieldArgs;
} DD_SET_OPREGION_EVENT;

// BCLM Data Word
typedef struct _DD_MB3_BCLM_MAPPING_
{
    union {
        DDU16 BclmData;
        struct
        {
            DDU16 DutyCycle : 8; // Inverter Duty Cycle
            DDU16 Percent : 7;   // Brightness Percent
            DDU16 ValidBit : 1;  // Data Valid bit
        };
    };
} DD_MB3_BCLM_MAPPING;

// Brightness data
typedef struct _DD_MB3_BRIGHTNESS
{
    union {
        DDU32 Brightness;
        struct
        {
            DDU32 BlcValue : 16; // Backlight Brightness value in % format specified in bits[29:28]
            DDU32 Reseved : 12;  // Bits[27:16] - Reserved
            DDU32 BlcFormat : 2; // Backlight % format for bits[15:0]
            DDU32 Reseved1 : 1;  // Bit[30] - Reserved
            DDU32 ValidBit : 1;  // Data Valid bit
        };
    };
} DD_MB3_BRIGHTNESS;

#define DD_BLC_PRECISION_FACTOR 100
#define DD_BLC_MAPPING_ERROR_TOLERANCE 1
#define DD_MB3_BCLM_FIELD_SIZE 20
#define DD_MB2_BCLM_FIELD_SIZE 30

// DSM related definitions
typedef enum _DD_DSM_CB_TYPE
{
    DD_BIOS_DATA_FUNC_SUPPORT                       = 0x00, // function is supported
    DD_SYSTEM_BIOS_ADAPTER_POWER_STATE_NOTIFICATION = 0x01,
    DD_SYSTEM_BIOS_DISPLAY_POWER_STATE_NOTIFICATION = 0x02,
    DD_SYSTEM_BIOS_POST_COMPLETION_NOTIFICATION     = 0x03,
    DD_SYSTEM_BIOS_PRE_HIRES_SET_MODE               = 0x04,
    DD_SYSTEM_BIOS_POST_HIRES_SET_MODE              = 0x05,
    DD_SYSTEM_BIOS_SET_DISPLAY_DEVICE_NOTIFICATION  = 0x06,
    DD_SYSTEM_BIOS_SET_BOOT_DEVICE_PREFERENCE       = 0x07,
    DD_SYSTEM_BIOS_SET_PANEL_PREFERENCE             = 0x08,
    DD_SYSTEM_BIOS_FULL_SCREEN_DOS                  = 0x09,
    DD_SYSTEM_BIOS_APM_COMPLETE                     = 0x0A,
    DD_SYSTEM_BIOS_PLUG_UNPLUG_AUDIO                = 0x0B,
    DD_SYSTEM_BIOS_CDCLOCK_CHANGE_NOTIFICATION      = 0x0C,
    DD_SYSTEM_BIOS_GET_BOOT_DISPLAY_PREFERENCE      = 0x0D,
    DD_SYSTEM_BIOS_GET_PANEL_DETAILS                = 0x0E,
    DD_SYSTEM_BIOS_INTERNAL_GRAPHICS                = 0x0F,
    DD_SYSTEM_BIOS_GET_AKSV                         = 0x10,
    DD_SYSTEM_BIOS_ENABLE_S0IX_HPD                  = 0x11,
    DD_BIOS_DATA_RESERVED // LAST ENTRY
} DD_DSM_CB_TYPE;

typedef struct _DD_DSM_OUTPUT_PARAM
{
    DDU32 Value;
    DDU8  ExitResult;
} DD_DSM_OUTPUT_PARAM;

typedef struct _DD_DSM_CB_ARGS
{
    DD_DSM_CB_TYPE      DsmFunctionCode;
    DDU32               InputArgument;
    DD_DSM_OUTPUT_PARAM OutputArgument;
} DD_DSM_CB_ARGS;

//----------------------------------------------------------------------------
//
// VBT/Oprgion Interface structures - END
//
//----------------------------------------------------------------------------
#pragma pack(1) // memcmp used for this structure(s) hence packing is necessary
typedef struct _DD_VRR_PARAMS
{
    BOOLEAN RangeIsRR; // TRUE = RR, FALSE = Duration
    DDU32   MinRrOrDuration;
    DDU32   MaxRrOrDuration;
    DDU32   MaxIncr; // 0 means no restriction
    DDU32   MaxDecr; // 0 means no restriction
} DD_VRR_PARAMS;
#pragma pack()

typedef struct _DD_PROGRAM_VRR_ARGS
{
    BOOLEAN               Enable;
    PIPE_ID               Pipe;
    DD_TARGET_DESCRIPTOR  TgtDesc;
    const DD_TIMING_INFO *pTimingInfo;
    DD_VRR_PARAMS         VrrParams;
    DD_VRR_PARAMS         VrrPrevParams;
} DD_PROGRAM_VRR_ARGS;

typedef struct _DD_GET_VRR_STATUS_ARGS
{
    DD_IN PIPE_ID Pipe;
    DD_IN DD_TARGET_DESCRIPTOR TgtDesc;
    DD_OUT DD_VRR_STATUS VrrStatus;
} DD_GET_VRR_STATUS_ARGS;

// 22 bytes
typedef struct _DD_PERIODIC_FRAME_DISPLAY_CAPS
{
    DDU32 VTotal;
    DDU32 VSyncNum;
    DDU32 VSyncDen;
    DDU32 VSyncStart;
    DDU32 VSyncEnd;
    DDU16 MinL; // Minimum number of scan lines between elements
} DD_PERIODIC_FRAME_DISPLAY_CAPS;

//----------------------------------------------------------------------------
//
// DisplayInfo parser Interface structures - START
//
//----------------------------------------------------------------------------

// Indicates Scaling type for Tiled display
typedef enum _DD_TILED_SCALING
{
    TILED_SCALING_UNINITIALIZED = 0,
    TILED_SCALING_NO_STRETCH,
    TILED_SCALING_STRETCH_ENTIRE_DISPLAY,
    TILED_SCALING_CLONE_OTHER_DISPLAYS
} DD_TILED_SCALING;

// TBD: Need to review if all this data is used.
typedef struct _DD_TILED_DISPLAY_INFO_BLOCK
{
    BOOLEAN          IsValidBlock; // Is Block valid (0x18 bytes of data found)?
    BOOLEAN          InSinglePhysicalDisplayEnclosure;
    BOOLEAN          IsBezelInfoAvailable;
    DD_TILED_SCALING Scaling; // Tiled display scaling support of type TILED_SCALING_TYPE
    DDU8             TotalNumberOfHTiles;
    DDU8             TotalNumberOfVTiles;
    DDU8             HTileLocation;
    DDU8             VTileLocation;
    DDU32            HTileSizeInPixels;
    DDU32            VTileSizeInLines;
    DDU8             PixelMultiplier;
    union {
        DDU32 TileBezelInformation;
        struct
        {
            DDU8 TopBezelsize;    // Top Bezel in pixels = (Pixel Multiplier x Top Bezel Size x 0.1)
            DDU8 BottomBezelsize; // Bottom Bezel in pixels = (Pixel Multiplier x Bottom Bezel Size x 0.1)
            DDU8 RightBezelsize;  // Right Bezel in pixels = (Pixel Multiplier x Right Bezel Size x 0.1)
            DDU8 LeftBezelsize;   // Left Bezel in pixels = (Pixel Multiplier x Left Bezel Size x 0.1)
        };
    };
    DDU8 BlockRevision;
    DDU8 ManufacturerID[3]; // Tiled Display Vendor ID
    DDU8 ProductID[2];      // Tiled Display Product Code
    DDU8 SerialNumber[4];   // Tiled Display Serial Number
} DD_TILED_DISPLAY_INFO_BLOCK;

typedef struct _DD_HF_VSDB_INFO
{
    union {
        DDU8 Value;
        struct
        {
            DDU8 IsHFVSDBInfoValid : 1;
            DDU8 IsSCDCPresent : 1;
            DDU8 IsSCDCRRCapable : 1;
            DDU8 IsLTE_340Mcsc_Scramble : 1;
        };
    };
    DDU8 Version;
} DD_HF_VSDB_INFO;

// CE Colorimetry Block
typedef struct _DD_CE_COLORIMETRY_DATA
{
    DDU8 ColorimetryType;    // Uses Mask of CE_COLORIMETRY_TYPE
    DDU8 CeProfileSupported; // Used Mask of CE_PROFILE_SUPPORT
} DD_CE_COLORIMETRY_DATA;

typedef struct _DD_HDR_STATIC_META_DATA
{
    BOOLEAN HdrMetaDataBlockFound;
    DDU8    EOTFSupported;         // EOTF type supported
    DDU8    HdrStaticMetaDataType; // HDR Static meta Data type
    DDU8    DesiredMaxCLL;         // Max content luminance level
    DDU8    DesiredMaxFALL;        // Max frame avereage luminance level
    DDU8    DesiredMinCLL;         // Min content luminance level
} DD_HDR_STATIC_META_DATA;

typedef union _DD_VIDEO_CAP_INFO {
    DDU8 Value;
    struct
    {
        DDU8 CEScanBehavior : 2;         // Indicates scan behavior of CE mode, of type CEA_SCAN_BEHAVIOR
        DDU8 ITScanBehavior : 2;         // Indicates scan behavior of IT mode, of type CEA_SCAN_BEHAVIOR
        DDU8 PTScanBehavior : 2;         // Indicates scan behavior of Preferred mode, of type CEA_SCAN_BEHAVIOR
        DDU8 IsQuantRangeSelectable : 1; // Indicates if RGB Quantization Range can be overridden
        DDU8 VideoCapInfoReserved : 1;   // Reserved
    };
} DD_VIDEO_CAP_INFO;

typedef union _DD_CEA_EXT_CAPS {
    DDU8 Value;
    struct
    {
        DDU8 TotalNativeDTDs : 4;     // Total number of DTDs in extension block
        DDU8 SupportsYCBCR422 : 1;    // Indicates support for YCBCR 4:2:2
        DDU8 SupportsYCBCR444 : 1;    // Indicates support for YCBCR 4:4:4
        DDU8 SupportsBasicAudio : 1;  // Indicates support for Basic audio
        DDU8 UnderscansITFormats : 1; // Indicates underscan behavior of IT formats
    };
} DD_CEA_EXT_CAPS;

#define VIC_UNDEFINED 0xFF

#define IS_VALID_VICID(VicId) ((VicId <= 128) && (VicId != 0))

typedef enum _HDMI_VERSION
{
    HDMI_VERSION_NONE = 0, // DVI display
    HDMI_VERSION_1_4,      // HDMI 1.4
    HDMI_VERSION_2_0,      // HDMI 2.0
} HDMI_VERSION;

#pragma pack(1)
// Runtime data based on current state
// Current size of this strucre: 272 bytes
// TBD: Need help to group this data appropriately
typedef struct _DD_EDID_FTR_SUPPORTED
{
    BOOLEAN      IsDisplayIDData : 1; // 0 - EDID Data, 1 - Display ID data
    BOOLEAN      IsCEExtnDisplay : 1;
    BOOLEAN      IsVideoCapBlockBlockPresent : 1;
    BOOLEAN      IsYUV420VideoBlockPresent : 1;
    BOOLEAN      IsHFVSDBBlockPresent : 1;
    BOOLEAN      IsDVISupported : 1;
    HDMI_VERSION HdmiDisplayVersion;
    BOOLEAN      IsDisplayPortSupported : 1;
    BOOLEAN      IsAudioSupported : 1;
    BOOLEAN      IsContinuousFreqSupported : 1;
    BOOLEAN      IsGTFSupported : 1;
    BOOLEAN      IsCVTSupported : 1;
    BOOLEAN      IsCVTRedBlankSupported : 1;
    BOOLEAN      IsS3DLRFramesSupported : 1;
} DD_EDID_FTR_SUPPORTED;
#pragma pack()

typedef struct _DD_EDID_BASIC_DISPLAY_CAPS
{
    DDU8                    MonitorName[MONITOR_NAME_LENGTH];
    DDU8                    MonitorNameLength; // Used for EELD creation
    DD_PNP_ID               PnpID;
    DD_COLOR_MODEL          ColorModel;     // Used to report to UMD, DD_CB_SRGB or this
    DD_CHROMA_AND_LUMA_DATA ChromaLumaData; // Override data from VBT or EDID
    DDU8                    DisplayGamma;
    DD_BPC_SUPPORTED        BpcsSupportedForAllModes; // Valid only for EDID 1.4 displays, comes from base block and HDMI VSDB block
    DD_BPC_SUPPORTED        BpcsSupportedFor420Modes; // Valid only if HDMI display present and 420 Color depth, comes from HF VSDB block
    DDU32                   MaxDotClockSupportedInHz; // For DP its Max DotClock, for HDMI this is Max TMDS clock
    DDU8                    MinRR;
    DDU8                    MaxRR;
} DD_EDID_BASIC_DISPLAY_CAPS;

typedef struct _DD_EDID_CE_EXTN_CAPS
{
    AVI_IT_CONTENT_TYPE     ITContentCaps;
    DD_CEA_EXT_CAPS         CeaExtnCaps;
    DD_HF_VSDB_INFO         HFVsdbInfo;
    DD_HDR_STATIC_META_DATA HdrStaticMetaData;
    DD_CE_COLORIMETRY_DATA  CeColorimetryData;
    DD_VIDEO_CAP_INFO       CeVideoCapInfo;
} DD_EDID_CE_EXTN_CAPS;

// Audio/Speaker allocation blocks required for EELD cration
// This has data mostly from Audio Data block and Speaker allocation block
typedef struct _DD_EDID_AUDIO_CAPS
{
    BOOLEAN      IsLpcmSadFound;
    DDU8         NumSADBytes;
    CEA_861B_ADB LpcmSad;                // Keeping a seperate copy of LPCM SAD as it is used to prune Audio modes for EELD
    CEA_861B_ADB SadBlock[14];           // corresponding to 14 possible AUDIO_FORMAT_CODES. TBD: Old code had allocated 48bytes
    DDU8         SpeakerAllocationBlock; // Speaker allocation block
} DD_EDID_AUDIO_CAPS;

typedef struct _DD_VRR_DISPLAY_CAPS
{
    BOOLEAN MsaTimingParIgnored;
    DDU16   MaxInc;
    DDU16   MaxDec;
} DD_VRR_DISPLAY_CAPS;

// 104 bytes of data
typedef struct _DD_DISPLAY_CAPS
{
    DD_EDID_FTR_SUPPORTED       FtrSupport;       // 2 bytes; Features supported, These are 1-bit BOOLEAN fields
    DD_EDID_BASIC_DISPLAY_CAPS  BasicDisplayCaps; // 50 bytes
    DD_EDID_CE_EXTN_CAPS        CeExtnCaps;       // 13 bytes
    DD_EDID_AUDIO_CAPS          CeAudioCaps;      // 48 bytes
    DD_TILED_DISPLAY_INFO_BLOCK TiledDisplayInfo; // 40 bytes
    DD_VRR_DISPLAY_CAPS         VrrDisplayCaps;
    DD_PSR_DISPLAY_CAPS         PsrDisplayCaps;
} DD_DISPLAY_CAPS;

typedef struct _DD_DISPLAY_FTR_SUPPORTED
{
    BOOLEAN DrrsSupported : 1;
    BOOLEAN DmrrsSupported : 1;
    BOOLEAN YCbCr444Supported : 1;
} DD_DISPLAY_FTR_SUPPORTED;

// 52 bytes
typedef struct _DD_GET_DISPLAY_CAPS_ARGS
{
    IN DD_TARGET_DESCRIPTOR TargetDesc;
    OUT DD_EDID_FTR_SUPPORTED EdidFtrSupport;
    OUT DD_DISPLAY_FTR_SUPPORTED DisplayFtrSupport;
    OUT DD_EDID_BASIC_DISPLAY_CAPS BasicDisplayCaps;
    OUT DD_VRR_DISPLAY_CAPS VrrDisplayCaps;
    OUT DD_PSR_DISPLAY_CAPS PsrDisplayCaps;
    OUT DD_BLC_FEATURES BlcDisplayCaps;
} DD_GET_DISPLAY_CAPS_ARGS;

// S3D related definitions (Moved from S3D.h)
#define DD_S3D_FORMAT_MASK(eFormat) (1 << eFormat)

typedef enum _DD_S3D_FORMAT
{
    // As per HDMI 1.4 spec
    S3D_FRAME_PACKING = 0,
    S3D_FIELD_ALTERNATIVE,
    S3D_LINE_ALTERNATIVE,
    S3D_SIDE_BY_SIDE_FULL,
    S3D_LDEPTH,
    S3D_LDEPTH_GRAPHICS_DEPTH,
    S3D_TOP_BOTTOM,
    S3D_SIDEBYSIDE_HALF_HORIZ_SUBSAMPLING,
    S3DSIDEBYSIDE_HALF_QUINCUNX_SUBSAMPLING,

    // For 120Hz page flipping
    S3D_PAGE_FLIPPING,

    S3D_NON_S3D = 31 // should be the last entry
} DD_S3D_FORMAT;

// Interface structure definitions for DisplayInfoParser

typedef struct _DD_TABLE
{
    DDU32 TableSize;        // number of elements for which memory is allocated
    DDU32 NumEntries;       // number of valid entries in table
    DDU32 EntrySizeInBytes; // size of each entry in Bytes
    DDSTATUS (*pfnAddEntry)(void *pTable, const void *pEntryToAdd, BOOLEAN ForceAdd);
    BOOLEAN (*pfnMatchEntry)(const void *pEntry1, const void *pEntry2);
    void (*pfnReplaceEntry)(void *pEntryToReplace, const void *pNewEntry); // Optional - Check for NULL before using
    void *pEntry;                                                          // contains an array of entries
} DD_TABLE;

typedef struct _DD_CHECK_TIMING_SUPPORT_ARG
{
    DD_IN DD_TARGET_DESCRIPTOR TargetDesc;
    DD_IN DD_TIMING_INFO *pTimingInfo;
    DD_OUT BOOLEAN Supported;
} DD_CHECK_TIMING_SUPPORT_ARG;

typedef struct _DD_GET_EDID_CAPS
{
    DD_IN DDU8 *pEdidOrDisplayIDBuf; // EDID/Display ID Data (All EDID/Display Blocks are passed at once)
    DD_IN DDU32 BufSizeInBytes;      // EDID/Display ID Size (Total size, e.g. 1 block = 128bytes, 2 blocks = 256 bytes, etc...)
    DD_OUT DD_DISPLAY_CAPS *pData;   // Mode Table filled by parser with modes found in EDID
} DD_GET_EDID_CAPS;

typedef struct _DD_GET_EDID_MODES
{
    DD_IN DDU8 *pEdidOrDisplayIDBuf; // EDID/Display ID Data (All EDID/Display Blocks are passed at once)
    DD_IN DDU32 BufSizeInBytes;      // EDID/Display ID Size (Total size, e.g. 1 block = 128bytes, 2 blocks = 256 bytes, etc...)
    DD_OUT DD_TABLE *pModeTable;     // Mode Table filled by parser with modes found in EDID
} DD_GET_EDID_MODES;

typedef struct _DD_GET_DTD_MODES
{
    DD_IN DDU8 *pEdidOrDisplayIDBuf;                                 // EDID/Display ID Data (All EDID/Display Blocks are passed at once)
    DD_IN DDU32 BufSizeInBytes;                                      // EDID/Display ID Size (Total size, e.g. 1 block = 128bytes, 2 blocks = 256 bytes, etc...)
    DD_OUT DD_TIMING_INFO TimingInfo[MAX_EDID_EXTENSIONS_SUPPORTED]; // Mode Table filled by parser with modes found in EDID
} DD_GET_DTD_MODES;

typedef struct _DD_INIT_DISPLAY_ARGS
{
    DD_ENCODER_INITIALIZATION_DATA *pEncoderInitData;
} DD_INIT_DISPLAY_ARGS;

//----------------------------------------------------------------------------
//
// DisplayInfo parser Interface structures - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// VDSC related structures - START
//
//----------------------------------------------------------------------------

/**
Macro for maximum number of DSC Buffer RC range parameters
**/
#define DD_NUM_BUF_RANGES 15

typedef enum _DSC_INSTANCES
{
    DSC_INVALID = -1,
    DSC_0       = 0, ///< Applicable till Gen11 LP only. Will be unused from Gen11p5 or Gen11 HP onwards.
    DSC_1,           ///< Applicable till Gen11 LP only. Will be unused from Gen11p5 or Gen11 HP onwards.
    DSC_A0,          ///< Applicable from Gen11 HP onwards for pipe A VDSC engine 0.
    DSC_A1,          ///< Applicable from Gen11 HP onwards for pipe A VDSC engine 1.
    DSC_B0,          ///< Applicable from Gen11 LP onwards for pipe B VDSC engine 0.
    DSC_B1,          ///< Applicable from Gen11 LP onwards for pipe B VDSC engine 1.
    DSC_C0,          ///< Applicable from Gen11 LP onwards for pipe C VDSC engine 0.
    DSC_C1,          ///< Applicable from Gen11 LP onwards for pipe C VDSC engine 1.
    DSC_D0,          ///< Applicable from Gen11 HP onwards for pipe D VDSC engine 0.
    DSC_D1           ///< Applicable from Gen11 HP onwards for pipe D VDSC engine 1.
} DSC_INSTANCES;

#pragma pack(1)
/**
This structure stores the 128 byte PPS data.
**/
typedef struct _PICTURE_PARAMS_SET
{
    union {
        DDU8 DscVersion; // PPS0
        struct
        {
            DDU8 MinorVersion : 4; // Bit 0-3 Major version no
            DDU8 MajorVersion : 4; // Bit 4-7 Minor version no
        };
    };

    union {
        DDU16 PictureParamsSetIdentifier; // PPS 1 ,2
        struct
        {
            DDU16 PpsIdentifier : 8; // Bit 0-7 Application-specific  identifier that can be used to differentiate  between  different PPS table
            DDU16 Reserved1 : 8;     // Bit 8-15 Reserved
        };
    };

    union {
        DDU8 BPCandLBD; // PPS 3
        struct
        {
            DDU8 LineBufferDepth : 4;  //  Bit  0-3 [1000 = 8 bits, 1001 = 9 bits, 1010 = 10 bits, 1011 = 11 bits, 1100 = 12bits}
            DDU8 BitsPerComponent : 4; // Bits 4-7 [1000 = 8 bits per component,1010 = 10 bits per component,1100 = 12 bits per component]
        };
    };

    union {
        DDU16 GeneralPPSParams; // PPS 4,5
        struct
        {
            DDU16 BPPLow : 2;                // Bits 0-1 The target bits/pixel (bpp) rate that is used by the encoder, in steps of 1/16 of a bit per pixel
            DDU16 VBRMode : 1;               // Bit 2 [0 = VBR mode is disabled, 1 = VBR mode is enabled]
            DDU16 Enable422 : 1;             // Bit 3 [0 = 4:4:4 sampling, 1 = 4:2:2 sampling]
            DDU16 ConvertRGB : 1;            // Bit 4 [ 0 =  no conversion required, 1 =  need conversion from RGB to YCoCg-R during encoding]
            DDU16 BlockPredictionEnable : 1; // Bit 5 [0 =  If block prediction is not supported on the receiver,1 =  If block prediction is supported on the receiver]
            DDU16 Reserved2 : 2;             // Bit 6-7 Reserved
            DDU16 BPPHigh : 8;               // Bits 8-15  The target bits/pixel (bpp) rate that is used by the encoder, in steps of 1/16 of a bit per pixel
        };
    };

    DDU16 PictureHeight; // PPS 6,7 [2 bytes for pic height]
    DDU16 PictureWidth;  // PPS 8,9 [ 2 bytes for pic width]
    DDU16 SliceHeight;   // PPS 10,11 [2 bytes for slice height]
    DDU16 SliceWidth;    // PPS 12,13 [2 bytes for slice width]
    DDU16 ChunkSize;     // PPS 14, 15 [2 bytes for Chunk size]

    union {
        DDU16 InitialTransmissionDelay; // PPS 16,17
        struct
        {
            DDU16 TransmissionDelayLow : 2;  // Bit 0-1 Application-specific  identifier that can be used to differentiate  between  different PPS table
            DDU16 Reserved3 : 6;             // Bit 2-7 Reserved
            DDU16 TransmissionDelayHigh : 8; // Bit 8-15 Application-specific  identifier that can be used to differentiate  between  different PPS table
        };
    };

    /**
    PPS 18,19: 2 bytes for Decode delay.
    Specifies the number of pixel times that the decoder accumulates data in its rate buffer
    before starting to decode and output pixels.
    **/
    DDU16 IntialDecodeDelay;
    union {
        DDU16 InitialScaleValue; // PPS 20, 21
        struct
        {
            DDU16 Reserved4 : 8;    // Bit 0-7 Reserved
            DDU16 InitialScale : 6; // Bit 8-13 Specifies the initial rcXformScale factor value used at the beginning of a slice
            DDU16 Reserved5 : 2;    // Bit 14-15 Reserved
        };
    };

    DDU16 ScaleIncrementInterval; // PPS 22, 23 Specifies the number of group times between incrementing the rcXformScale factor at the end of a slice

    union {
        DDU16 ScaleDecrementInterval; // PPS 24, 25
        struct
        {
            DDU16 ScaleDecrementLow : 4;  // Bit  0-3 Specifies the number of group times between decrementing the rcXformScale factor at the beginning of a slice
            DDU16 Reserved6 : 4;          // Bit 4-7 Reserved
            DDU16 ScaleDecrementHigh : 8; // Bit 8-15 Specifies the number of group times between decrementing the rcXformScale factor at the beginning of a slice
        };
    };

    union {
        DDU16 FirstLineBPGOffset; // PPS 26, 27
        struct
        {
            DDU16 Reserved7 : 8; // Bit 0-7 Reserved
            DDU16 BPGOffset : 5; // Bit 8-12 Specifies the number of additional bits that are allocated for each group on the first line of a slice.
            DDU16 Reserved8 : 3; // Bit 13-15 Reserved
        };
    };

    /**
    PPS 28, 29
    Specifies the number of bits (including fractional bits) that are de-allocated for each group, for groups after the first line of a slice.
    If the first line has an additional bit budget, the additional bits that are allocated must come out of the budget for coding the remainder of the slice.
    **/
    DDU16 NflBpgOffset;

    /**
    PPS 30, 31
    Specifies the number of bits (including fractional bits) that are de-allocated for each group to enforce the slice constraint,
    while allowing a programmable initial_offset.
    **/
    DDU16 SliceBpgOffset;
    DDU16 InitialOffset; // PPS 32, 33
    DDU16 FinalOffset;   // PPS 34, 35

    union {
        DDU8 FlatnessMinQP; // PPS 36
        struct
        {
            DDU8 MinQP : 5;     // Bit 0-5 Major version no
            DDU8 Reserved9 : 3; // Bit 0-3 Reserved
        };
    };
    union {
        DDU8 FlatnessMaxQP; // PPS 37
        struct
        {
            DDU8 MaxQP : 5;      // Bit 0-5 Major version no
            DDU8 Reserved10 : 3; // Bit 0-3 Reserved
        };
    };

    DDU16 RCmodelSize; // PPS 38, 39 Specifies the number of bits within the�RC model,�

    union {
        DDU8 RCEdgeFactor; // PPS 40
        struct
        {
            DDU8 EdgeFactor : 4; // Bit 0-5 Major version no
            DDU8 Reserved11 : 4; // Bit 0-3 Reserved
        };
    };
    union {
        DDU8 RCQuanIncrLimit0; // PPS 41
        struct
        {
            DDU8 IncrLimit0 : 5; // Bit 0-5 Major version no
            DDU8 Reserved12 : 3; // Bit 0-3 Reserved
        };
    };
    union {
        DDU8 RCQuanIncrLimit1; // PPS 42
        struct
        {
            DDU8 IncrLimit1 : 5; // Bit 0-5 Major version no
            DDU8 Reserved13 : 3; // Bit 0-3 Reserved
        };
    };
    union {
        DDU8 RCTargetOffset; // PPS 43
        struct
        {
            DDU8 RCTargetOffsetLow : 4;  // Bit 0-5 Major version no
            DDU8 RCTargetOffsetHigh : 4; // Bit 0-3 Reserved
        };
    };

    DDU8 RCBufferThreshold0;  // PPS 44
    DDU8 RCBufferThreshold1;  // PPS 45
    DDU8 RCBufferThreshold2;  // PPS 46
    DDU8 RCBufferThreshold3;  // PPS 47
    DDU8 RCBufferThreshold4;  // PPS 48
    DDU8 RCBufferThreshold5;  // PPS 49
    DDU8 RCBufferThreshold6;  // PPS 50
    DDU8 RCBufferThreshold7;  // PPS 51
    DDU8 RCBufferThreshold8;  // PPS 52
    DDU8 RCBufferThreshold9;  // PPS 53
    DDU8 RCBufferThreshold10; // PPS 54
    DDU8 RCBufferThreshold11; // PPS 55
    DDU8 RCBufferThreshold12; // PPS 56
    DDU8 RCBufferThreshold13; // PPS 57

    union {
        DDU32 RCRangeParameterBlock1; // PPS 58, 59,60, 61
        struct
        {
            DDU32 RCRangeParameter0 : 16;
            DDU32 RCRangeParameter1 : 16;
        };
    };

    union {
        DDU32 RCRangeParameterBlock2; // PPS 62, 63, 64, 65
        struct
        {
            DDU32 RCRangeParameter2 : 16;
            DDU32 RCRangeParameter3 : 16;
        };
    };

    union {
        DDU32 RCRangeParameterBlock3; // PPS 66 ,67,  68, 69
        struct
        {
            DDU32 RCRangeParameter4 : 16;
            DDU32 RCRangeParameter5 : 16;
        };
    };

    union {
        DDU32 RCRangeParameterBlock4; // PPS  70, 71, 72 ,73
        struct
        {
            DDU32 RCRangeParameter6 : 16;
            DDU32 RCRangeParameter7 : 16;
        };
    };

    union {
        DDU32 RCRangeParameterBlock5; // PPS  74, 75, 76, 77
        struct
        {
            DDU32 RCRangeParameter8 : 16;
            DDU32 RCRangeParameter9 : 16;
        };
    };

    union {
        DDU32 RCRangeParameterBlock6; // PPS 78, 79, 80, 81
        struct
        {
            DDU32 RCRangeParameter10 : 16;
            DDU32 RCRangeParameter11 : 16;
        };
    };

    union {
        DDU32 RCRangeParameterBlock7; // PPS 82, 83, 84, 85
        struct
        {
            DDU32 RCRangeParameter12 : 16;
            DDU32 RCRangeParameter13 : 16;
        };
    };

    union {
        DDU32 RCRangeParameterBlock8; // PPS 86,87,88,89
        struct
        {
            DDU32 RCRangeParameter14 : 16;
            DDU32 Reserved14 : 16;
        };
    };

    DDU16 Reserved15; // PPS 90, 91
    DDU32 Reserved16; // PPS 92, 93, 94, 95
    DDU32 Reserved17; // PPS 96, 97, 98, 99
    DDU32 Reserved18; // PPS 100, 101, 102 , 103
    DDU32 Reserved19; // PPS 104, 105, 106 , 107
    DDU32 Reserved20; // PPS 108, 109, 110 , 111
    DDU32 Reserved21; // PPS 112, 113, 114 , 115
    DDU32 Reserved22; // PPS 116, 117, 118 , 119
    DDU32 Reserved23; // PPS 120, 121, 122 , 123
    DDU32 Reserved24; // PPS 124, 125, 126 , 127
} PICTURE_PARAMS_SET;

/**
This structure defines the full 132 byte PPS (header + data) packet.
**/
typedef union _PPS_SDP {
    DDU8 PpsDip[PPS_LENGTH + 4];

    struct
    {
        // 4 byte header.
        // As per eDP spec, the PPS header should contain four bytes as below:
        // 00, 10, 7F, 00
        IF_HEADER IfHeader;

        // Payload
        PICTURE_PARAMS_SET PpsPayload;
    };
} PPS_SDP;

/**
Configuration for a single RC model range.
**/
typedef struct _RC_RANGE_PARAMETERS
{
    DDU32 RangeMinQp;     ///< Min QP allowed for this range
    DDU32 RangeMaxQp;     ///< Max QP allowed for this range
    DDU32 RangeBpgOffset; ///< Bits/group offset to apply to target for this group
} RC_RANGE_PARAMETERS;

/**
This structure defines the RC range parameters to be computed for a given DSC configuration.
**/
typedef struct
{
    DDU32               InitialXmitDelay;
    DDU32               FirstLineBpgOffset;
    DDU32               InitialOffset;
    DDU32               FlatnessMinQp;
    DDU32               FlatnessMaxQp;
    DDU32               RcQuantIncrLimit0;
    DDU32               RcQuantIncrLimit1;
    RC_RANGE_PARAMETERS RcRangeParams[DD_NUM_BUF_RANGES];
} RC_PARAMETERS;

/**
This structure will contain all the information relevant to the PPS for VDSC.
We use this structure for the initial computation of PPS.
Reason for having separate structures for PPS (See :: PICTURE_PARAMETER_SET) and computation:
We will keep the parameters in DSC_CFG and compute the PPS for different values of slice height.
If we use a common structure then code becomes complex to save/restore original values for next round of computation.
**/
typedef struct _DSC_CFG
{
    BOOLEAN             DscEnabled;                           ///< DSC enabled/disabled
    DDU32               LineBufDepth;                         ///< Bits / component for previous reconstructed line buffer
    DDU32               RcbBits;                              ///< Rate control buffer size (in bits); not in PPS, used only in C model for checking overflow
    DDU32               BitsPerComponent;                     ///< Bits / component to code (must be 8, 10, or 12)
    BOOLEAN             ConvertRgb;                           ///< Flag indicating to do RGB - YCoCg conversion and back (should be 1 for RGB input)
    DDU32               SliceCount;                           ///< Slice count per line
    DDU32               SliceWidth;                           ///< Slice width
    DDU32               SliceHeight;                          ///< Slice height
    BOOLEAN             Enable422;                            ///< 4:2:2 enable mode (from PPS, 4:2:2 conversion happens outside of DSC encode/decode algorithm)
    DDU32               PicWidth;                             ///< Picture width
    DDU32               PicHeight;                            ///< Picture height
    DDU32               RcTgtOffsetHi;                        ///< Offset to bits/group used by RC to determine QP adjustment
    DDU32               RcTgtOffsetLo;                        ///< Offset to bits/group used by RC to determine QP adjustment
    DDU32               BitsPerPixel;                         ///< Bits/pixel target << 4 (ie., 4 fractional bits)
    DDU32               RcEdgeFactor;                         ///< Factor to determine if an edge is present based on the bits produced
    DDU32               RcQuantIncrLimit1;                    ///< Slow down incrementing once the range reaches this value
    DDU32               RcQuantIncrLimit0;                    ///< Slow down incrementing once the range reaches this value
    DDU32               InitialXmitDelay;                     ///< Number of pixels to delay the initial transmission
    DDU32               InitialDecDelay;                      ///< Number of pixels to delay the VLD on the decoder, not including SSM
    BOOLEAN             BlockPredEnable;                      ///< Block prediction range (in pixels)
    DDU32               FirstLineBpgOfs;                      ///< Bits/group offset to use for first line of the slice
    DDU32               InitialOffset;                        ///< Value to use for RC model offset at slice start
    DDU32               XStart;                               ///< X position in the picture of top-left corner of slice
    DDU32               YStart;                               ///< Y position in the picture of top-left corner of slice
    DDU32               RcBufThresh[DD_NUM_BUF_RANGES - 1];   ///< Thresholds defining each of the buffer ranges
    RC_RANGE_PARAMETERS RcRangeParameters[DD_NUM_BUF_RANGES]; ///< Parameters for each of the RC ranges
    DDU32               RcModelSize;                          ///< Total size of RC model
    DDU32               FlatnessMinQp;                        ///< Minimum QP where flatness information is sent
    DDU32               FlatnessMaxQp;                        ///< Maximum QP where flatness information is sent
    DDU32               FlatnessDetThresh;                    ///< MAX-MIN for all components is required to be <= this value for flatness to be used
    DDU32               InitialScaleValue;                    ///< Initial value for scale factor
    DDU32               ScaleDecrementInterval;               ///< Decrement scale factor every scale_decrement_interval groups
    DDU32               ScaleIncrementInterval;               ///< Increment scale factor every scale_increment_interval groups
    DDU32               NflBpgOffset;                         ///< Non-first line BPG offset to use
    DDU32               SliceBpgOffset;                       ///< BPG offset used to enforce slice bit constraDDU32
    DDU32               FinalOffset;                          ///< Final RC linear transformation offset value
    BOOLEAN             VbrEnable;                            ///< Enable on-off VBR (ie., disable stuffing bits)
    DDU32               MuxWordSize;                          ///< Mux word size (in bits) for SSM mode
    DDU32               ChunkSize;                            ///< The (max) size in bytes of the "chunks" that are used in slice multiplexing
    DDU32               PpsIdentifier;                        ///< Placeholder for PPS identifier
    DDU32               DscVersionMinor;                      ///< DSC minor version
    DDU32               DscVersionMajor;                      ///< DSC major version
    DDU32               NumVdscInstances;                     ///< number of VDSC engines
} DSC_CFG;

/**
Row index based on BPC for accessing RC range parameters as per VESA DSC model
**/
typedef enum
{
    ROW_INDEX_INVALID = -1,
    ROW_INDEX_6BPP    = 0,
    ROW_INDEX_8BPP,
    ROW_INDEX_12BPP,
    ROW_INDEX_15BPP,
    MAX_ROW_INDEX
} ROW_INDEX_BPP;

/**
Column index based on BPP for accessing RC range parameters as per VESA DSC model
**/
typedef enum
{
    COLUMN_INDEX_INVALID = -1,
    COLUMN_INDEX_8BPC    = 0,
    COLUMN_INDEX_10BPC,
    COLUMN_INDEX_12BPC,
    COLUMN_INDEX_14BPC,
    COLUMN_INDEX_16BPC,
    MAX_COLUMN_INDEX
} COLUMN_INDEX_BPC;

/**
Structure to be passed as argument for programming PPS regsiters of a single DSC Engine.
**/
typedef struct _PROGRAM_PPS_REGS_ARG
{
    PIPE_ID               PipeId;      ///< Will be used to determine DP VDSC engines
    DD_TARGET_DESCRIPTOR *pTgtDesc;    ///< Will be used for DP MST information and port to determine VDSC engines.
    DSC_INSTANCES         DscInstance; ///< DSC Instance to be programmed.
    DSC_CFG *             pDscCfg;     ///< DSC_CFG data to be programmed in the PPS registers.
} PROGRAM_PPS_REGS_ARG;

/**
Structure to be passed as argument for programming DSS_CTL of a single DSS unit.
**/
typedef struct _PROGRAM_DSS_CTL_ARG
{
    PIPE_ID               PipeId;          ///< Will be used to determine DP VDSC engines
    DD_TARGET_DESCRIPTOR *pTgtDesc;        ///< Will be used for DP MST information and port to determine VDSC engines.
    BOOLEAN               IsDualLinkMipi;  ///< To be used to determine if small joiner is to be enabled.
    DDU8                  NumVdscInstance; ///< To determine whether we are using 1 or 2 engines.
    BOOLEAN               IsChipOnGlass;   ///< To be used to determine if small joiner is to be enabled.
    BOOLEAN               Enable;          ///< Enable/disable flag
                                           // TODO: Add pipe ganged mode and slave/master pipe information for big joiner programming
} PROGRAM_DSS_CTL_ARG;

#pragma pack()

//----------------------------------------------------------------------------
//
// VDSC related structures - END
//
//----------------------------------------------------------------------------

//////////////////////////////////////////////////////////////////////////////
//----------------------------------------------------------------------------
//
// Protocol data structures - END
//
//----------------------------------------------------------------------------
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
//----------------------------------------------------------------------------
//
// HAL data structures - START
//
//----------------------------------------------------------------------------
//////////////////////////////////////////////////////////////////////////////

typedef struct _DD_INIT_HAL
{
    BOOLEAN                  Enable;
    DD_SET_ADAPTER_PWR_ARGS *pSetPwrStateArgs; // Power State Args passed to HAL
} DD_INIT_HAL;

typedef enum _DD_DC_PWR_STATE
{
    DC_PWR_STATE_SET_NONE,
    DC_PWR_STATE_SET_UPTO_DC5,
    DC_PWR_STATE_SET_UPTO_DC6,
    DC_PWR_STATE_SET_UPTO_DC9
} DD_DC_PWR_STATE;

//----------------------------------------------------------------------------
//
// Color related data structures - START
//
//----------------------------------------------------------------------------
typedef enum _COLOR_RANGE
{
    FULL_RANGE            = 0,
    COLOR_RANGE_16_TO_235 = 1
} COLOR_RANGE;

typedef union _DD_BPP_MASK {
    // Currently required color depth values : 8, 16, 32, 64
    // If in the future, a new color depth support is required, add it here.
    // In this case you should update MAX_COLOR_BPP & ALLCOLOR_BPP_MASK
    DDU8 BPPMask;
    struct
    {
        DDU8 Is4BPP : 1; // 1: Supported, 0 : no supported.
        DDU8 Is8BPP : 1;
        DDU8 Is16BPP : 1;
        DDU8 Is32BPP : 1;
        DDU8 Is64BPP : 1;
        DDU8 Reserved : 3;
    };
} DD_BPP_MASK;

//----------------------------------------------------------------------------
//
// Color related data structures - END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// Plane/Pipe/Pll/Port/Watermark related structures - START
//
//----------------------------------------------------------------------------

// PLL related
typedef enum _PLL_TYPE
{
    PLL_TYPE_NONE = 0,
    PLL_1         = 1,
    PLL_2         = 2,
    PLL_3         = 3,
    PLL_4         = 4,
} PLL_TYPE;

// Enum defining types of DPLL's supported in given platform
typedef enum _DPLL_TYPE
{
    DPLL_NONE = 0,

    LCPLL1,
    LCPLL2,
    SPLL,
    WRPLL1,
    WRPLL2,
    DPLL_C,
    DE_PLL,
    DSI_PLL,
    DPLL_0,
    DPLL_1,
    DPLL_2,
    DPLL_3,
    TBT_PLL,
    MG_PLL_1,
    MG_PLL_2,
    MG_PLL_3,
    MG_PLL_4
} DPLL_TYPE;

//// WM related
// typedef enum _SB_WATERMARK_RETURN_CODE
//{
//    SB_WM_SUCCESSFUL = 0,
//    SB_WM_ERROR_UNKNOWN,
//    SB_WM_ERROR_EXCEEDED_FIFO,
//    SB_WM_ERROR_UNUSED
//}SB_WATERMARK_RETURN_CODE;
/*
// Gen9 Specific Definitions
#define GEN9_NUM_WM_PER_PLANE 8

// Gen9 Watermark Data Struct
typedef struct _SB_GEN9_LP_WM_DATA
{
    DD_OUT BOOLEAN     WmEnable;                // DD_OUT: Whether the WM is enabled on this pipe
    DD_OUT BOOLEAN     IgnoreLines;             // DD_OUT: Ignore lines and use blocks
    DD_OUT DDU16      WmLines;                // DD_OUT: Num lines for this watermark
    DD_OUT DDU16      WmBlocks;               // DD_OUT: Num blocks for this watermark
} SB_GEN9_LP_WM_DATA;

// Gen9 Plane Parameters
//
typedef struct _SB_GEN9_WATERMARK_ARGS
{
    DD_IN DD_OUT DDU8                 Pipe; // TODO: remove this interface
    DD_IN DD_OUT DDU8                 PlaneType; // possible values: cursor or PLANE_OVERLAY. check for Z-order for PLANE_OVERLAY,
    DD_IN DD_OUT DDU8                 ZOrder;                            // The Zorder for the plane
    DD_IN DD_OUT SB_GEN9_LP_WM_DATA   PlaneLpWm[GEN9_NUM_WM_PER_PLANE]; // Block of LP WM information
    DD_OUT SB_WATERMARK_RETURN_CODE ReturnCode;                        // DD_OUT: Error code
} SB_GEN9_WATERMARK_ARGS;
*/
typedef enum _DD_MIPI_LINK_OPERATION_TYPE
{
    MIPI_OP_NONE = 0,
    MIPI_OP_ENABLE_IO,
    MIPI_OP_DISABLE_IO,
    MIPI_OP_ENABLE_PORT
} DD_MIPI_LINK_OPERATION_TYPE;

typedef struct _DD_MIPI_SET_LINK_CONFIG_ARGS
{
    DD_PORT_TYPE                Port;
    DD_MIPI_LINK_OPERATION_TYPE OpCode;
    DD_MIPI_DATA *              pMipiData;
} DD_MIPI_SET_LINK_CONFIG_ARGS;

/**
 * @brief Interface struct to be used for port, pll programming during link training.
 */
typedef struct _DD_DP_SET_LINK_CONFIG_ARGS
{
    DD_DP_LINK_OPERATION_TYPE OpCode;
    DD_PORT_TYPE              Port;
    DD_PORT_CONNECTOR_TYPE    PortConnectorType;

    union {
        struct
        {
            DP_LINK_DATA *      pLinkData;
            DD_PPS_DELAY_TABLE *pPpsDelayTable;
        } PrepareLTArg; //!< used with OpCode = DP_OP_PREPARE_FOR_LINK_TRAINING
        struct
        {
            DD_DP_TRAINING_PATTERN TrainingPattern;
        } SetTPArg; //!< used with OpCode = DP_OP_SET_LINK_PATTERN
        struct
        {
            DD_DP_DRIVE_SETTING DriveSettings;
        } AdjDrvArg; //!< used with OpCode = DP_OP_ADJ_DRIVE_SETTINGS
        struct
        {
            DP_LINK_DATA *pLinkData;
            BOOLEAN       Enable;
        } EnableDisableArg; //!< used with OpCode = DP_OP_DISABLE_PORT_PLL, DP_OP_ENABLE_PORT
    };
} DD_DP_SET_LINK_CONFIG_ARGS;

typedef struct _DD_SET_LINK_CONFIG_ARGS
{
    DD_PROTOCOL_TYPE Protocol;

    union {
        DD_DP_SET_LINK_CONFIG_ARGS *  pDpSetLinkConfigArgs;
        DD_MIPI_SET_LINK_CONFIG_ARGS *pMipiSetLinkConfigArgs;
    };
} DD_SET_LINK_CONFIG_ARGS;

typedef struct _ENABLE_TRANSCODER_DATA
{
    BOOLEAN Enable;
    // Transport type used by this transcoder
    DD_PROTOCOL_TYPE TransportTypeEnabled;
    // Color format: 6/8/10 bits per color (default is 8)
    // 6bpc is valid only for X1 mode
    // One may get this from EDID/CE blocks
    DDU8 ColorDepth;
    // Enable/Disable Dithering
    BOOLEAN EnableDithering;
    // Color range selection
    // Valid only when eSink is eHDMISink and
    // ucBitsPerColor == 8
    // HDMI encoder will set this when mode is
    // 480i, 576p, 576i, 240p or 288p
    // Enable/disable audio (can be enabled only for HDMI sink)
    BOOLEAN EnableAudio;
    BOOLEAN EnablePortSynch;

    union {
        DP_LINK_DATA   DpLinkData;
        HDMI_LINK_DATA HdmiLinkData;
        DD_MIPI_DATA   MipiData;
    };
} ENABLE_TRANSCODER_DATA;

typedef struct _DD_SUPPORTED_LINK_RATES
{
    DDU8  NumOfLinkRates;
    DDU32 LinkRateMhzList[8]; // Linkrate in MHz
} DD_SUPPORTED_LINK_RATES;

typedef struct _DD_SOURCE_COMPRESSION_CAPS
{
    BOOLEAN CompressionSupported;
    DDU8    CompressionBpc;
    DDU16   MaxPictureHeight;
    DDU16   MaxPictureWidth;
} DD_SOURCE_COMPRESSION_CAPS;

typedef struct _DD_EDP_DISPLAY_CAPS
{
    DD_SUPPORTED_LINK_RATES    SupportedLinkRates;    ///< Supported Link rates in the platform
    DD_SOURCE_COMPRESSION_CAPS SourceCompressionCaps; ///< Source supported compression capabilities
} DD_EDP_DISPLAY_CAPS;

typedef struct _SPRITE_PLANEPARAMS
{
    DDU32 StartAddress;   // Sprite Start Adress
    DDU32 ScanLineLength; // Sprite scan line length
    DDU32 SpriteXPos;
    DDU32 SpriteYPos;
    DDU32 SpriteXTiledOffset;
    DDU32 SpriteYTiledOffset;
    DDU32 SpriteWidth;
    DDU32 SpriteHeight;
} SPRITE_PLANEPARAMS;

typedef struct _PLANE_CAPABILITY
{
    DDU8 Rotation;
    DDU8 FlipMode;
    DDU8 SteroFormat;
    DDU8 StretchQuality;
    DDU8 FBC : 1;
    DDU8 S3DCompression : 1;
    DDU8 MediaCompression : 1;
    DDU8 NV12 : 1;
    DDU8 YUV : 1;
    DDU8 P0xx : 1;
    DDU8 HFlip : 1;
    DDU8 Reserved : 1;
} PLANE_CAPABILITY;

// READ-ONLY params
typedef struct _PLANE_PARAMS_RO
{
    DDU8             PipeID;          // Provides info on which plane this pipe can be assigned to
    PLANE_CAPABILITY PlaneCapability; // provides info on the capabilities of the plane, used Gen9 onwards
    PLANE_ZORDER     ZOrder;          // Z order of plane

    DDU8 MuxedWithCursor : 1;
    DDU8 Reserved2 : 4;
} PLANE_PARAMS_RO;

typedef struct _DD_PIPE_SOURCE_DETAILS
{
    DDU32          SrcSizeX;
    DDU32          SrcSizeY;
    DD_PIXELFORMAT SrcPixFormat;
} DD_PIPE_SOURCE_DETAILS;

typedef struct _DD_ASSIGN_PIPE_DETAILS
{
    DD_IN DD_TARGET_DESCRIPTOR TargetDesc;
    // A pointer to PipeId is being used below so that pipe id can directly get updated in CCD struct. Otherwise it is lot of reverse calculation to figure out where to update in
    // CCD struct.
    DD_IN_OUT PIPE_ID *pPipeId;
} DD_ASSIGN_PIPE_DETAILS;

typedef struct _DD_ASSIGN_PIPE_ARGS
{
    DD_IN DDU32            NumTarget;
    DD_ASSIGN_PIPE_DETAILS Target[MAX_PHYSICAL_PIPES];
} DD_ASSIGN_PIPE_ARGS;

// Args for Pipe modeset enable/disable sequence
typedef struct _DD_SETMODE_ARGS
{
    DD_IN BOOLEAN Enable;               // TRUE = Enable given Target Device, FALSE = Disable Target Device
    DD_IN DD_TARGET_DESCRIPTOR TgtDesc; // Target device identifier
    DD_IN PIPE_ID Pipe;                 // Pipe to be used for Enable/Disable
    // Below parameters required only when 'Enable = TRUE'
    DD_IN DD_PIPE_SOURCE_DETAILS SrcDetails;       // Pipe source mode details
    DD_IN DD_TIMING_INFO *pTimingInfo;             // Pipe Timing
    DD_IN DD_COLOR_PIXEL_DESC *pOutputColorFormat; // Pipe OutputColor format
    DD_IN DD_SCALING Scaling;
    DD_IN BOOLEAN VrrPossible; // Indicates whether VRR is possible for current configuration, if yes Target device needs to be setup accordingly (DPCD needs to be set)
    DD_IN ENABLE_TRANSCODER_DATA *pTranscoderData; // to be filled by protocol layer
    DD_IN DSC_CFG *pDscCfg;                        // DSC Config to be filled by protocol layer
    DD_IN_OUT BOOLEAN PreserveBootDisplay;
} DD_SETMODE_ARGS;

typedef struct _DD_DYNAMIC_RR_SWITCH_ARG
{
    IN PIPE_ID PipeId;
    IN DD_TARGET_DESCRIPTOR TargetDesc;
    IN DDU32 RrMultBy1000; // RR multiplied by 1000
} DD_DYNAMIC_RR_SWITCH_ARG;

typedef struct _DD_ASSIGN_DBUF_DETAILS
{
    PIPE_ID         PipeId;
    BOOLEAN         IsModified;
    DD_TIMING_INFO *pTimingInfo;
} DD_ASSIGN_DBUF_DETAILS;

typedef struct _DD_ASSIGN_DBUF_ARGS
{
    DDU32                  NumActivePipes;
    DD_ASSIGN_DBUF_DETAILS PipeDetails[MAX_PHYSICAL_PIPES];
} DD_ASSIGN_DBUF_ARGS;

/*
typedef struct _DD_ASSIGN_DBUF_ON_PIPE_ARGS
{
    PIPE_ID PipeId;
    DD_ENABLED_PLANE_DATA_ARGS EnabledPlaneData;
} DD_ASSIGN_DBUF_ON_PIPE_ARGS;
*/
typedef struct _DD_GET_TILE_FMT
{
    IN DDU32 HorizontalRes;
    IN DD_PIXELFORMAT PixelFormat;
    IN PLANE_ORIENTATION Rotation;
} DD_GET_TILE_FMT;

typedef struct _DD_MIN_DBUF_INPUT_PARAMS
{
    DDU32                  HorizontalRes;
    DD_SURFACE_MEMORY_TYPE MemFormat;
    DD_ROTATION            RotationAngle;
    DD_PIXELFORMAT         PixelFormat;
} DD_MIN_DBUF_INPUT_PARAMS;
//----------------------------------------------------------------------------
//
// Plane/Pipe/Pll/Port/Watermark related structures - END
//
//----------------------------------------------------------------------------

// Power well
typedef union _POWER_WELL_CONFIG {
    struct
    {
        DDU32 PowerWell1 : 1;         // 1 - enabled
        DDU32 PowerWell2 : 1;         // 1 - enabled
        DDU32 DdiAAndDdiEIoPower : 1; // 1 - enabled
        DDU32 DdiBIoPower : 1;        // 1 - enabled
        DDU32 DdiCIoPower : 1;        // 1 - enabled
        DDU32 DdiDIoPower : 1;        // 1 - enabled
        DDU32 MiscIoPower : 1;        // 1 - enabled
        DDU32 DdiEIoPower : 1;        // 1 - enabled
        DDU32 AuxAIoPower : 1;        // 1 - enabled
        DDU32 AuxBIoPower : 1;        // 1 - enabled
        DDU32 AuxCIoPower : 1;        // 1 - enabled
        DDU32 AuxDIoPower : 1;        // 1 - enabled
        DDU32 Reserved : 20;
    };
    DDU32 Value;
} POWER_WELL_CONFIG;

// PCU mailbox
// Avoiding new naming for same structure, hence copying same PWRCONS_PCU_MAILBOX_OPERATION struct for SB usage
typedef struct _DD_PCU_MAILBOX_OPERATION
{
    DDU32 MailBoxCmd; // Mailbox command - candidate defined in GEN6_PCU_CR_GTDRIVER_MAILBOX_CMD
    DDU32 CmdParam1;  // Mailbox parameter 1
    DDU32 CmdParam2;  // Mailbox parameter 2
    DDU32 CmdData;    // Mailbox command data  - 0x138128
    DDU32 CmdData1;   // Mailbox command data1 - 0x13812c
    DDU32 ReadResult; // Read result value
} DD_PCU_MAILBOX_OPERATION;

// PSR Protocol specific Parameters

typedef enum _DD_GTC_REQUEST
{
    GTC_DISABLE = 0,
    GTC_ENABLE,
    GTC_UPDATE_LOCK,
} DD_GTC_REQUEST;

// PSR event handler args structure
typedef enum _DD_PSR_COMMAND
{
    PSR_ENABLE = 0,
    PSR_DISABLE,
    PSR_ENABLE_SU,           // PSR2
    PSR_DISABLE_SU,          // PSR2
    PSR_MEDIA_PLAYBACK_MODE, // PSR2
    PSR_MAX_COMMAND
} DD_PSR_COMMAND;

typedef struct _DD_SETPSR_ARGS
{
    DD_PSR_COMMAND      PsrCmd; // PSR command type
    DD_PORT_TYPE        Port;   // needed to identify PIPE_EDP
    DDU32               PipeInUse;
    DDU32               RefreshRate;
    DDU8                IdleFramesNum;
    DDU8                SuIdleFrames;
    DD_PSR_DISPLAY_CAPS PsrDetails;
} DD_SETPSR_ARGS;

typedef struct _DD_PSR_ARGS
{
    IN DD_TARGET_DESCRIPTOR TargetDesc;
    IN DD_PSR_COMMAND PsrCommand; // PSR command type
    IN DDU8 IdenticalFramesCount; // Used for PSR_ENABLE and PSR_HW_MODE.
} DD_PSR_ARGS;

//----------------------------------------------------------------------------
//
// Plane/Pipe/Pll/Port/Watermark related structures - START
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// AUX/I2C Args -- START
//
//----------------------------------------------------------------------------

// I2C BUS request
typedef enum _DD_I2C_BUS_REQUEST
{
    DD_I2C_REQ_UNDEFINED      = 0,
    DD_I2C_REQ_AUTO_SELECT    = 1,
    DD_I2C_REQ_USE_BITBASHING = 2,
    DD_I2C_REQ_USE_GMBUS      = 3,
    DD_I2C_REQ_FORCE_NATIVE   = 4
} DD_I2C_BUS_REQUEST;

// I2C Commands
// Note: Use GET_DD_I2C_COMMAND to get the GMCH
// command value from a AIM3 flag value
typedef enum _DD_I2C_COMMAND
{
    DD_I2C_COMMAND_NULL   = 0x0000, // Does no command
    DD_I2C_COMMAND_READ   = 0x0001, // Reads Data from an I2C Bus Device
    DD_I2C_COMMAND_WRITE  = 0x0002, // Writes Data out on the I2C Bus Device
    DD_I2C_COMMAND_STATUS = 0x0003, // Effects I2C Bus State
    DD_I2C_COMMAND_RESET  = 0x0004, // Resets the I2C Bus
} DD_I2C_COMMAND;

// I2C Flags
// Note: Use GET_DD_I2C_FLAGS to get the GMCH
// flag value from a AIM3 flag value
typedef union _DD_I2C_FLAGS {
    DDU32 Value;
    struct
    {
        DDU32 Start : 1;     // Bit 0
        DDU32 Restart : 1;   // Bit 1
        DDU32 Stop : 1;      // Bit 2
        DDU32 Address : 1;   // Bit 3
        DDU32 Index : 1;     // Bit 4
        DDU32 Dword : 1;     // Bit 5
        DDU32 Word : 1;      // Bit 6
        DDU32 Slow : 1;      // Bit 7
        DDU32 Reserved : 24; // Bits 8:31
    };
} DD_I2C_FLAGS;

// I2C Destination
// Note: Use GET_DD_I2C_DEST_ADR to get the GMCH
// destination value from a AIM3 flag value
typedef enum _DD_I2C_DEST_ADR
{
    DD_I2C_DEST_CODEC     = 0x00, // Implies the Codec
    DD_I2C_DEST_CODEC2    = 0x01, // Implies 2nd Codec (e.g. for Dual-Channel)
    DD_I2C_DEST_SPD       = 0x02, // Implies the ADD SPD
    DD_I2C_DEST_CODEC_ADR = 0x03, // Targets an Address on the Codec Bus
    DD_I2C_DEST_DDC_ADR   = 0x04, // Targets an Address on the Monitor DDC Bus
} DD_I2C_DEST_ADR;

//----------------------------------------------------------------------------
//
// GMBUS_REQ_SPEED - Caller if required can select a different speed
// by providing a value other than GMBUS_REQ_SPEED_AUTO in
// DD_I2C_ARGUMENTS. Note that this request value is not the same
// as what get programmed in the HW register.
//
// Default Selection is as follows:
//
// GMBUS_REQ_SPEED_400KHZ:
//      DD_I2C_DEST_CODEC,
//      DD_I2C_DEST_CODEC2,
//      DD_I2C_DEST_SPD,
//      DD_I2C_DEST_CODEC_ADR
//
// GMBUS_REQ_SPEED_100KHZ:
//      DD_I2C_DEST_DDC_ADR
//
// GMBUS_REQ_SPEED_50KHZ: When DD_I2C_FLAGS_SLOW is selected
//
// In addition to this the rate will be changed internally based on
// the sDVO switch required. This will happen irrespective of the
// input requested speed. It's expected that they will match, but
// in case, if they don't SB will ASSERT.
// For switch following are the default speeds:
//  DDC-100KHz, REGS-1MHz, EPROM-400KHz
//
//----------------------------------------------------------------------------
typedef enum _GMBUS_REQ_SPEED
{
    GMBUS_REQ_SPEED_AUTO   = 0,
    GMBUS_REQ_SPEED_100KHZ = 1,
    GMBUS_REQ_SPEED_50KHZ  = 2,
    GMBUS_REQ_SPEED_400KHZ = 3,
} GMBUS_REQ_SPEED;

//----------------------------------------------------------------------------
//
// Macros to get GMCH/GAL I2C flags, command and
// destination values
//
//----------------------------------------------------------------------------
#define GET_DD_I2C_COMMAND(AIMI2CFlags) (AIMI2CFlags & 0x0000000F)
#define GET_DD_I2C_FLAGS(AIMI2CFlags) ((AIMI2CFlags & 0x0000FF00) >> 8)
#define GET_DD_I2C_DEST_ADR(AIMI2CFlags) ((AIMI2CFlags & 0x00FF0000) >> 16)
#define GET_DD_I2C_SLAVE_ADR(AIMI2CFlags) ((AIMI2CFlags & 0xFF000000) >> 24)

typedef struct _DD_I2C_ARGUMENTS
{
    DD_PORT_TYPE     Port;
    DD_PROTOCOL_TYPE Protocol;

    DDU8 DdcPinPairIndex; // GMBUS pin pair Index from VBT to read HDMI/DVI EDID/panel params. From CNL, values are platform independant

    DDU32 SlaveAddress; // Slave address (Final address to be used. e.g. for DDC on sDVO device this will be 0xA0 & not 0x70)
    DDU32 Index;        // Index
    DDU8 *pBuffer;      // Note: Always a byte pointer to data
    DDU32 BufferSize;   // Data size in bytes

    // Command, flags & destination type
    DD_I2C_COMMAND  Command;
    DD_I2C_FLAGS    I2CFlags;
    DD_I2C_DEST_ADR Destination;

    //
    // Parameters of importance to GMBus only
    //
    BOOLEAN         UseBitBashing;       // 1 - Use Bit bashing, Mostly used for MCCS
    GMBUS_REQ_SPEED RequestedGMBusSpeed; // (Default: GMBUS_REQ_SPEED_AUTO)
    BOOLEAN         MiddleOfTransaction; // caller can set this if it's middle of a transaction (ie., first transaction or re-start)

    // Flag to enable Aksv buffer selection
    BOOLEAN AksvBufferSelect; // FALSE => select default buffer stated by GMBUS3; TRUE => select AKSV buffer

    // Aux Channel Type
    DDU8 AuxChannelType;

    // HDCP 2.2
    BOOLEAN HDCP2_2_Message;

    DDU8 RetryCount; // 0 based. 0 - No retry, 1 - Retry once and so on...
    // Actual bytes Read/written
    DDU32 ActualBytesReadOrWritten;
} DD_I2C_ARGUMENTS;

// DD_ATOMICI2C_ARGUMENTS - Used by AtomicI2CAccess
typedef struct _DD_ATOMICI2C_ARGUMENTS
{
    DD_I2C_ARGUMENTS I2CArgs;

    // Extra params
    DDU32 ReadBytes;  // Bytes to read
    DDU32 WriteBytes; // Bytes to write
} DD_ATOMICI2C_ARGUMENTS;

// Args for read DDC operation
typedef struct _DD_READ_DDC_ARGUMENTS
{
    DD_PORT_TYPE     Port; // Of type PORT_TYPES
    DD_PROTOCOL_TYPE Protocol;

    DDU8 DdcPinPairIndex; // GMBUS pin pair Index from VBT to read HDMI/DVI EDID/panel params. From CNL, values are platform independant

    DDU32 SlaveAddress; // Slave address (Final address to be used. e.g. for DDC on sDVO device this will be 0xA0 & not 0x70)
    DDU16 BlockNumber;  // EDID block (0, 1, ...)
    DDU8 *pBuffer;      // Note: Always a byte pointer to data
    DDU32 BufferSize;   // Data size in bytes

    BOOLEAN UseBitBashing; // 1 - Use Bit bashing, Mostly used for any WAs/experiments
    // AUX Channel type
    DDU8 AuxChannelType;
} DD_READ_DDC_ARGUMENTS;

// The HAL accepts max 48 bytes as an atomic Aux transaction request, needed for DP Sideband Req
#define DD_NATIVE_AUX_MAX_REQ_SIZE 534 // RxCert size for HDCP 2.2

// Due to hardware limitations the max aux transaction size is limited to 16 bytes.
// This macro is used to divide the number of bytes into chunks of 16 bytes.
#define DD_AUX_MAX_SIZE 16

typedef enum _DD_AUX_OPERATIONS
{
    DD_AUX_OPERATION_UNKNOWN = 0,
    DD_AUX_READ,
    DD_AUX_WRITE,
    DD_AUX_I2C_READ,
    DD_AUX_I2C_WRITE,
} DD_AUX_OPERATIONS;

typedef struct _DD_AUX_ARGUMENTS
{
    DD_IN DD_PORT_TYPE DisplayPort;
    DD_IN DD_PORT_CONNECTOR_TYPE PortConnectorType; // Valid only for DP to indicate Type-C/Thunderbolt port
    DD_IN DD_AUX_OPERATIONS Operation;

    DD_IN DDU32 DPCDAddress;
    DD_IN_OUT DDU8 *pBuffer;        // Note: Format of data is little-endian only (usual Intel format)
    DD_IN_OUT DDU16 BufferSize;     // This is treated as DD_IN_OUT -> DD_OUT to send back the size in case of NACK, native aux max 48 bytes supported, I2C 16 bytes only
    DD_IN BOOLEAN AksvBufferSelect; // TO select AKSV buffer

    // > 1 for burst operation, here
    // DPCDAddress will indicate the starting address. Max possible size is 16 for native AUX

    // I2C on AUX specific arguments... (Note: Not complete yet)
    DD_IN BOOLEAN MiddleOfTransaction; // caller can set this if it's middle of a transaction (ie., first transaction or re-start)
    DD_IN BOOLEAN IssueWriteStatusRequest;
    DD_IN DDU8 I2CAddress; // 7-bit format I2C address

    DD_IN DDU8 AuxChannelType;

    DD_IN BOOLEAN StartTransaction;

    // Temp usage
    BOOLEAN IsCurrentChannelBusy;
} DD_AUX_ARGUMENTS;

//----------------------------------------------------------------------------
//
// AUX/I2C Args -- END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// HAL port context data structure to store static data from VBT/Opregion
// etc... which does not change in a given boot
//
//----------------------------------------------------------------------------
typedef struct _DD_PORT_INFO
{
    // DP capable port related data
    DD_PORT_CONNECTOR_TYPE PortConnectorType;
    DD_DP_AUX_CHANNEL_TYPE AuxChannel;
    BOOLEAN                IsLaneReversed;

    // HDMI capable port related data
    DDU8 HdmiLevelShifterIndex;

    // LFP related data
    DD_PWM_CTRL_TYPE PwmCtrlType;
    DD_PWM_CTRL_NUM  PwmCtrlNum;
    DDU32            PwmInverterFreq;
    BOOLEAN          IsPwmPolarityInverted;
    DDU16            BrightnessPercent;
} DD_PORT_INFO;

typedef struct _DD_UPDATE_PORTINFO_ARG
{
    DD_PORT_TYPE Port;
    DD_PORT_INFO PortInfo;
} DD_UPDATE_PORTINFO_ARG;

//////////////////////////////////////////////////////////////////////////////
//----------------------------------------------------------------------------
//
// HAL related data structures - END
//
//----------------------------------------------------------------------------
//////////////////////////////////////////////////////////////////////////////

//----------------------------------------------------------------------------
//
// Generic INLINES -- START
//
//----------------------------------------------------------------------------

DD_INLINE void SetShortFormatInI2CFlags(DD_I2C_FLAGS *pFlags)
{
    pFlags->Value   = 0;
    pFlags->Start   = 1;
    pFlags->Address = 1;
    pFlags->Index   = 1;
    pFlags->Stop    = 1;
    return;
}

DD_INLINE void SetCombinedFormatInI2CFlags(DD_I2C_FLAGS *pFlags)
{
    pFlags->Value   = 0;
    pFlags->Start   = 1;
    pFlags->Address = 1;
    pFlags->Index   = 1;
    pFlags->Restart = 1;
    pFlags->Stop    = 1;
    return;
}

DD_INLINE void SetCombinedFormatInI2CFlagsForMCCSRead(DD_I2C_FLAGS *pFlags)
{
    pFlags->Value   = 0;
    pFlags->Stop    = 1;
    pFlags->Address = 1;
    pFlags->Index   = 1;
    pFlags->Restart = 1;
    return;
}

DD_INLINE void SetCombinedFormatInI2CFlagsForMCCSWrite(DD_I2C_FLAGS *pFlags)
{
    pFlags->Value   = 0;
    pFlags->Start   = 1;
    pFlags->Address = 1;
    pFlags->Index   = 1;
    pFlags->Stop    = 1;
    return;
}

//----------------------------------------------------------------------------
//
// Generic INLINES -- END
//
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//
// To be cleaned up
//
//----------------------------------------------------------------------------

// Still used by PC code

/*
#define GRM_PIPEA_BIT 1
#define GRM_PIPEB_BIT 2
#define GRM_PIPEC_BIT 4

#define GRM_DISPLAYA_BIT 1
#define GRM_DISPLAYB_BIT 2
#define GRM_DISPLAYC_BIT 4
*/
// query display details args structure

// Display details flag enum
typedef enum _DD_DISPLAY_DETAILS_FLAG
{
    DD_QUERY_DISPLAYUID = 1,
    DD_QUERY_DISPLAYTYPE_INDEX
} DD_DISPLAY_DETAILS_FLAG;

typedef enum _DD_DISPLAY_TYPE
{
    // DONOT change the order of type definitions
    // Add new types just before MAX_DISPLAY_TYPES & increment value of MAX_DISPLAY_TYPES
    DD_DISPLAY_TYPE_NONE = 0,
    DD_DISPLAY_TYPE_CRT,
    DD_DISPLAY_TYPE_DFP,
    DD_DISPLAY_TYPE_LFP,
    DD_DISPLAY_TYPE_MAX = DD_DISPLAY_TYPE_LFP,
} DD_DISPLAY_TYPE;

typedef struct _DD_QUERY_DISPLAY_DETAILS_ARGS
{
    // eflag = QUERY_DISPLAYUID -> Indicates that Display Type & Index will be sent & we need to return DisplayUID & bExternalEncoderDriven
    // eflag = QUERY_DISPLAYTYPE_INDEX -> Indicates that DisplayUID will be sent & we need to return  Display Type ,Index & bExternalEncoderDriven
    DD_IN DD_DISPLAY_DETAILS_FLAG Flag;

    DD_IN_OUT DDU32 DisplayUID;
    //#ifndef _COMMON_PPA
    DD_IN_OUT DD_DISPLAY_TYPE Type;
    //#endif
    DD_IN_OUT DDU8 Index;

    // Is display ID driven by external encoder?
    DD_OUT BOOLEAN ExternalEncoderDriven; // Includes both sDVO and NIVO Displays

    DD_OUT BOOLEAN TPVDrivenEncoder;

    // Type of Port Used.
    DD_OUT DD_PORT_TYPE PortType;

    // This interprets logical port mapping for physical connector.
    // This indicates mapping multiple encoders to the same port
    DD_OUT DDU8 LogicalPortIndex;
} DD_QUERY_DISPLAY_DETAILS_ARGS;

typedef struct _DD_REG_MEDIA_REFRESH_RATE_SUPPORT
{
    union {
        DDU32 Value;
        struct
        {
            DDU32 Rr24 : 1;                  // Bit 0 - 24 Hz
            DDU32 Rr25 : 1;                  // Bit 1 - 25 Hz
            DDU32 Rr30 : 1;                  // Bit 2 - 30 Hz
            DDU32 Rr48 : 1;                  // Bit 3 - 48 Hz
            DDU32 Rr50 : 1;                  // Bit 4 - 50 Hz
            DDU32 Rr60 : 1;                  // Bit 5 - 60 Hz
            DDU32 Reserved1 : 9;             // Bit 6:14
            DDU32 FractionalRrSupported : 1; // Bit 15 - Fractional RR supported for all supported RRs
            DDU32 Reserved2 : 15;            // Bit 16:30
            DDU32 InfOverride : 1; // Bit 31 -> INF override bit, if set, this bit will override VBT DMRRS bit as well as EDID Monitor range / DTD block for RR range determination.
                                   // When this bit is set, only the INF will be read to determine supported media RRs
        };
    };
} DD_REG_MEDIA_REFRESH_RATE_SUPPORT;

typedef struct _DD_AUDIO_HDCP_PARAMS
{
    PIPE_ID PipeId;
    BOOLEAN IsGetEncryptionPref;
    BOOLEAN EncPreference;
    BOOLEAN CPStatus;
} DD_AUDIO_HDCP_PARAMS;

// Capability Mask
typedef union _DD_HDCP_CAP_MASK {
    DDU32 Value;
    struct
    {
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 2); // Unused bits
        DDU32 ProtectionTypeHDCP : DD_BITFIELD_BIT(3);        // HDCP capability
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(4);
        DDU32 ProtectionTypeHDCPTypeEnforcement : DD_BITFIELD_BIT(5); // HDCP Type enforcement capability
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(6, 31);        // Unused Bits
    };
} DD_HDCP_CAP_MASK;

typedef struct _DD_HDCP_KSV_LIST
{
    DDU32  KSVListLength; // Length of the  KSV list (set)
    PKSV_T pKSVList;      // List of KSVs (set)
} DD_HDCP_KSV_LIST;

typedef struct _DD_GET_HDCP_STATUS_ARGS
{
    DD_IN DD_TARGET_DESCRIPTOR TgtDesc;
    DD_IN PIPE_ID Pipe;
    DD_OUT DD_HDCP_CAP_MASK CapMask;
    DD_OUT DDU32 Level;
    DD_OUT BOOLEAN IsiHDCP2; // Not used if LSPCON
    DD_OUT BOOLEAN IsRepeater;
    // AKSV, BKSV, KSVList
    DD_OUT KSV_T AKSV;              // KSV of attached device
    DD_OUT KSV_T BKSV;              // KSV of attached device
    DD_IN DD_HDCP_KSV_LIST SRMData; // SRM revokation data
} DD_GET_HDCP_STATUS_ARGS;
typedef struct _DD_SET_HDCP_STATUS_ARGS
{
    DD_IN DD_TARGET_DESCRIPTOR TgtDesc;
    DD_IN PIPE_ID Pipe;
    DD_IN BOOLEAN IsSecondStep;
    DD_IN_OUT DDU32 Level;
    DD_IN_OUT DD_HDCP_KSV_LIST KSVFifo; // downstream KSV data
    // SRM Data
    DD_IN DD_HDCP_KSV_LIST SRMData;  // SRM revokation data
    DD_IN BOOLEAN Internal;          // Whethee to HDCP disable is initiated internally
    DD_IN BOOLEAN TriggerAuthToSrvc; // Whether an authentication trigger to be sent to Service.
} DD_SET_HDCP_STATUS_ARGS;
typedef struct _DD_HDCP_ENCRYPTION_STATUS_ARGS
{
    DD_IN PIPE_ID Pipe;
    DD_IN DD_PORT_TYPE Port;
    DD_IN DD_HDCP_VERSION HDCPVersion;
    DD_IN DD_PROTOCOL_TYPE Protocol;
    DD_IN_OUT DDU32 Level;
    // SRM Data
} DD_HDCP_ENCRYPTION_STATUS_ARGS;

typedef struct _DD_PORT_HDCP_ARGS
{
    DD_IN PIPE_ID Pipe;
    DD_IN DD_PORT_TYPE Port;
    DD_IN BOOLEAN Enable;
} DD_PORT_HDCP_ARGS;

typedef struct _DD_SET_HDCP_STREAM_STATUS_ARGS
{
    DD_IN DD_HDCP_VERSION HDCPVersion;
    DD_IN DD_PORT_HDCP_ARGS PortHdcp;
} DD_SET_HDCP_STREAM_STATUS_ARGS;

typedef enum _HDCP1_CIPHER_SRVC
{
    HDCP_KEY_LOAD_TRIGGER,
    HDCP_GET_STATUS,
    HDCP_SET_ENCRYPTION,
    HDCP1_GENERATE_AN,
    HDCP1_UPDATE_BKSV,
    HDCP1_WAIT_FOR_RI_READY,
    HDCP1_VERIFY_RI_PRIME,
    HDCP1_UPDATE_REPEATER_STATE,
    HDCP1_COMPUTE_V,
    HDCP1_VERIFY_V_PRIME,
    HDCP_SET_STREAM_ENCRYPTION,

} HDCP1_CIPHER_SRVC;
typedef struct _DD_HDCP_CIPHER_SRVC_ARGS
{
    DD_IN PIPE_ID Pipe;
    DD_IN DD_PORT_TYPE Port;
    DD_IN HDCP1_CIPHER_SRVC Service;
    DD_IN_OUT DDU8 *pBuffer;
    DD_IN_OUT DDU32 DataSize;
    // SRM Data
} DD_HDCP_CIPHER_SRVC_ARGS;
//
// BSTATUS
//
/*typedef union _HDCP_RX_BSTATUS
{
    DDU16 Value;
    struct
    {
        DDU16 DeviceCount : 7; // bit 6:0
        DDU16 MaxDevsExceeded : 1; // bit 7
        DDU16 Depth : 3; // bit 10:8
        DDU16 MaxCascadeExceeded : 1; // bit 11
        DDU16 RXInHDMIMode : 1; // bit 12
        DDU16 Rserved : 3; // bit 15:13
    };
}HDCP_RX_BSTATUS;*/

typedef struct _DD_HDCP1_COMPUTE_V_ARGS
{
    DD_IN DDU8 *pKSVList;
    DD_IN DDU32 KSVBufferSize;
    DD_IN DDU16 TopologyData;
} DD_HDCP1_COMPUTE_V_ARGS;

// Audio related interface structures

typedef struct _AUDIO_ENDPOINT_INDICATE_PARAMS
{
    BOOLEAN               IsEnable;
    void *                pELD;
    PIPE_ID               Pipe;
    DDU32                 DotClockHz;
    DD_TARGET_DESCRIPTOR *pTargetDesc;
} AUDIO_ENDPOINT_INDICATE_PARAMS;

// Color Related
// Color OSL-HAL structes
typedef struct _DD_COLOR_PIPE_MATRIX_ARGS
{
    DD_COLOR_BLENDING_MODE  BlendingMode;
    DD_COLOR_MATRIX_CONFIG *pMatrixConfig;
} DD_COLOR_PIPE_MATRIX_ARGS;

typedef struct _DD_COLOR_PIPE_LUT_ARGS
{
    DD_COLOR_BLENDING_MODE BlendingMode;
    DD_COLOR_1DLUT_CONFIG *p1DLUTConfig;
} DD_COLOR_PIPE_LUT_ARGS;

typedef struct _DD_COLOR_PIPE_OUTPUT_CONFIG_ARGS
{
    DD_COLOR_BLENDING_MODE       BlendingMode;
    DD_COLOR_PIPE_OUTPUT_CONFIG *pPipeOutputConfig;
} DD_COLOR_PIPE_OUTPUT_CONFIG_ARGS;

// TODO: check if used
typedef enum _SAMPLING_MODE
{
    SAMPLING_RGB = 0,
    SAMPLING_Y420_ONLY,
    SAMPLING_Y420_RGB
} SAMPLING_MODE;

#endif // _DISPLAY_INTERNAL_
