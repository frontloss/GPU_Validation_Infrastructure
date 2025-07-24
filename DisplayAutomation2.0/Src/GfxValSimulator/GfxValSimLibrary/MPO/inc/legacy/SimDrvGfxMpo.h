/*===========================================================================
; SIMDRV_GFX_COMMON.h
;----------------------------------------------------------------------------
;   Copyright (c) 2017-2018  Intel Corporation.
;   All Rights Reserved.  Copyright notice does not imply publication.
;   This software is protected as an unpublished work.  This software
;   contains the valuable trade secrets of Intel Corporation, and must
;   and must be maintained in confidence.
;
; File Description:
;   Interface definitions common between IGD and Simulation Driver
;--------------------------------------------------------------------------*/

#ifndef __SIMDRV_GFX_COMMON__
#define __SIMDRV_GFX_COMMON__

#define SIMDRIVER_MAX_PIPES 4
#define SIMDRIVER_MAX_PLANES 21
#define SIMDRIVER_MAX_DIRTY_RECTS 8

#define IN_OUT _Inout_
#define RESERVED _Reserved_
#define IN_OUT_OPT _Inout_opt_

// Error codes used by Gfx and Validation Driver to indicate the operation success/failure in this layer
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_SUCCESS 0x00000000
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_FAILURE 0x00000001
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_FW_NOT_ENABLED 0x00000002
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_FEATURE_NOT_ENABLED 0x00000004
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_SIZE_MISMATCH 0x00000008
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_INVALID_FEATURE 0x00000010
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_INVALID_PARAMETER 0x00000020
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_PARAM_NULL_POINTER 0x00000040
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_FUNC_NULL_POINTER 0x00000080
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_MEMORY_ALLOCATION 0x00000100
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_DEV_SIM_ATTACH_ON_ATTACH 0x00000200
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_DEV_SIM_DETACH_WITHOUT_ATTACH 0x00000400
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_NO_DPCD_DATA 0x00000800
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_NO_MEMORY 0x00001000
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_ERROR_INTERNAL 0x00000016 // Internal API errors
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_VBT_REQUESTED_SIZE_EXCEEDS_6K_FAILURE 0x00002000
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_REGISTRY_WRITE_FAILURE 0x00004000
#define SIMDRIVER_DISPLAY_FEATURE_STATUS_VBT_FETCH_FAILURE 0x00008000

#pragma pack(1)

/////////////////////////////////////////////////////////
// MPO Structures and Enums.
/////////////////////////////////////////////////////////

// Enum specifying Features supported by the framework
typedef enum _SIMDRIVER_DISPLAY_FEATURE_REQUEST_TYPE
{
    SIMDRIVER_ENABLE_DISABLE_MPO,      // Enable Disable the feature in ULT
    SIMDRIVER_CREATE_RESOURCE,         // Allocate the Surface
    SIMDRIVER_FREE_RESOURCE,           // Freeup the allocated resource
    SIMDRIVER_GET_MPO_CAPS,            // Get the MPO capability
    SIMDRIVER_GET_MPO_GROUP_CAPS,      // Get the MPO Group caps
    SIMDRIVER_CHECK_MPO,               // Check MPO DDI
    SIMDRIVER_SET_SRC_ADD_MPO,         // MPO flips
    SIMDRIVER_CHECK_MPO3,              // Check MPO3 DDI
    SIMDRIVER_SET_SOURCE_ADDRESS_MPO3, // MPO3 Flips
    // MAX_SIMDRIVER_FW_FUNCTIONS should be the last value in this enum
    MAX_SIMDRIVER_FW_FUNCTIONS
} SIMDRIVER_DISPLAY_FEATURE_REQUEST_TYPE;

/* Enum for features*/
typedef enum _SIMDRIVER_FEATURE_TYPE
{
    SIMDRIVER_FEATURE_UNDEFINED = 0,
    SIMDRIVER_GENERIC_GFX_ACCESS,
    SIMDRIVER_THUNK_ESCAPE,
    SIMDRIVER_FEATURE_DISPLAY,
    SIMDRIVER_FEATURE_KMRENDER,
    SIMDRIVER_FEATURE_PWRCONS,
    SIMDRIVER_FEATURE_GMM,
    SIMDRIVER_FEATURE_PINNING,
    SIMDRIVER_FEATURE_MAX
} SIMDRIVER_FEATURE_TYPE;

//
// Specifies the types of features for Display Framework
//
typedef enum _SIMDRIVER_DISPLAY_FEATURE
{
    SIMDRIVER_FEATURE_PRIVATE_FLIP,
    SIMDRIVER_FEATURE_PRIVATE_MPOFLIP
} SIMDRIVER_DISPLAY_FEATURE;

typedef enum _SIMDRIVER_MPO_PLANE_ORIENTATION
{
    SIMDRIVER_MPO_ORIENTATION_DEFAULT = 0,                                 // Default value
    SIMDRIVER_MPO_ORIENTATION_0       = SIMDRIVER_MPO_ORIENTATION_DEFAULT, // 0 degree
    SIMDRIVER_MPO_ORIENTATION_90      = 1,                                 // 90 degree, supported Gen9 onwards
    SIMDRIVER_MPO_ORIENTATION_180     = 2,                                 // 180 degree
    SIMDRIVER_MPO_ORIENTATION_270     = 3,                                 // 270 degree, supported Gen9 onwards
    SIMDRIVER_MPO_ORIENTATION_MAX     = 4
} SIMDRIVER_MPO_PLANE_ORIENTATION;

// ----- "SIMDRIVER_CREATE_RESOURCE" -----
// Src Pixel Format.
// There is 1:1 maping between SIMDRIVER_PIXELFORMAT and SB_PIXELFORMAT. Any change in SB_PIXELFORMAT should be updated here also.
typedef enum _SIMDRIVER_PIXELFORMAT
{
    SIMDRIVER_PIXEL_FORMAT_UNINITIALIZED = 0,
    SIMDRIVER_PIXEL_FORMAT_8BPP_INDEXED, // for 8bpp
    SIMDRIVER_PIXEL_FORMAT_B5G6R5X0,     // for 16bpp
    SIMDRIVER_PIXEL_FORMAT_B8G8R8X8,     // for 32bpp (default)
    SIMDRIVER_PIXEL_FORMAT_B8G8R8A8,
    SIMDRIVER_PIXEL_FORMAT_R8G8B8X8,
    SIMDRIVER_PIXEL_FORMAT_R8G8B8A8,
    SIMDRIVER_PIXEL_FORMAT_R10G10B10X2,         // for 32bpp 10bpc
    SIMDRIVER_PIXEL_FORMAT_R10G10B10A2,         // for 32bpp 10bpc
    SIMDRIVER_PIXEL_FORMAT_B10G10R10X2,         // for 32bpp 10bpc
    SIMDRIVER_PIXEL_FORMAT_B10G10R10A2,         // for 32bpp 10bpc
    SIMDRIVER_PIXEL_FORMAT_R10G10B10A2_XR_BIAS, // for 32bpp 10bpc, XR BIAS format (used by Win7)
    SIMDRIVER_PIXEL_FORMAT_R16G16B16X16F,       // for 64bpp, 16bit floating
    SIMDRIVER_PIXEL_FORMAT_R16G16B16A16F,
    SIMDRIVER_PIXEL_FORMAT_MAX, // To match the driver structure
    SIMDRIVER_PIXEL_FORMAT_NV12YUV420,
    SIMDRIVER_PIXEL_FORMAT_YUV422,
    SIMDRIVER_PIXEL_FORMAT_P010YUV420,
    SIMDRIVER_PIXEL_FORMAT_P012YUV420,
    SIMDRIVER_PIXEL_FORMAT_P016YUV420,
    SIMDRIVER_PIXEL_FORMAT_YUV444_10,
    SIMDRIVER_PIXEL_FORMAT_YUV422_10,
    SIMDRIVER_PIXEL_FORMAT_YUV422_12,
    SIMDRIVER_PIXEL_FORMAT_YUV422_16,
    SIMDRIVER_PIXEL_FORMAT_YUV444_8,
    SIMDRIVER_PIXEL_FORMAT_YUV444_12,
    SIMDRIVER_PIXEL_FORMAT_YUV444_16,
    SIMDRIVER_PIXEL_FORMAT_MAXALL,
} SIMDRIVER_PIXELFORMAT;

// Surface memory type
typedef enum _SIMDRIVER_SURFACE_MEMORY_TYPE
{
    SIMDRIVER_SURFACE_MEMORY_INVALID        = 0,
    SIMDRIVER_SURFACE_MEMORY_LINEAR         = 1, // Surface uses linear momory
    SIMDRIVER_SURFACE_MEMORY_TILED          = 2, // Surface uses tiled memory
    SIMDRIVER_SURFACE_MEMORY_X_TILED        = SIMDRIVER_SURFACE_MEMORY_TILED,
    SIMDRIVER_SURFACE_MEMORY_Y_LEGACY_TILED = 4, // Surface uses Legacy Y tiled memory (Gen9+)
    SIMDRIVER_SURFACE_MEMORY_Y_F_TILED      = 8, // Surface uses Y F tiled memory
} SIMDRIVER_SURFACE_MEMORY_TYPE;

// Not in Dx9 spec
// Matches Kernel flip attribute.
typedef enum _SIMDRIVER_MPO_VIDEO_FRAME_FORMAT
{
    SIMDRIVER_MPO_VIDEO_FRAME_FORMAT_PROGRESSIVE                   = 0x0,
    SIMDRIVER_MPO_VIDEO_FRAME_FORMAT_INTERLACED_TOP_FIELD_FIRST    = 0x1,
    SIMDRIVER_MPO_VIDEO_FRAME_FORMAT_INTERLACED_BOTTOM_FIELD_FIRST = 0x2
} SIMDRIVER_MPO_VIDEO_FRAME_FORMAT;

// Not in Dx9 Spec
// Matches Kernel flip attribute.
typedef enum _SIMDRIVER_MPO_STEREO_FORMAT
{
    SIMDRIVER_MPO_FORMAT_MONO               = 0,
    SIMDRIVER_MPO_FORMAT_HOR                = 1,
    SIMDRIVER_MPO_FORMAT_VER                = 2,
    SIMDRIVER_MPO_FORMAT_SEPARATE           = 3,
    SIMDRIVER_MPO_FORMAT_ROW_INTERLEAVED    = 5, //??????? 4 is missing ?????
    SIMDRIVER_MPO_FORMAT_COLUMN_INTERLEAVED = 6,
    SIMDRIVER_MPO_FORMAT_CHECKBOARD         = 7
} SIMDRIVER_MPO_STEREO_FORMAT;

// Not in Dx9 Spec
// Matches Kernel flip attribute.
typedef enum _SIMDRIVER_MPO_STEREO_FLIP_MODE
{
    SIMDRIVER_MPO_FLIP_NONE   = 0,
    SIMDRIVER_MPO_FLIP_FRAME0 = 1,
    SIMDRIVER_MPO_FLIP_FRAME1 = 2
} SIMDRIVER_MPO_STEREO_FLIP_MODE;

typedef enum _SIMDRIVER_MPO_STRETCH_QUALITY
{
    SIMDRIVER_MPO_STRETCH_QUALITY_BILINEAR = 0x1, // Bilinear
    SIMDRIVER_MPO_STRETCH_QUALITY_HIGH     = 0x2  // Maximum
} SIMDRIVER_MPO_STRETCH_QUALITY;

typedef enum _SIMDRIVER_MPO_COLOR_SPACE_TYPE
{
    SIMDRIVER_MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709           = 0,
    SIMDRIVER_MPO_COLOR_SPACE_RGB_FULL_G10_NONE_P709           = 1,
    SIMDRIVER_MPO_COLOR_SPACE_RGB_STUDIO_G22_NONE_P709         = 2,
    SIMDRIVER_MPO_COLOR_SPACE_RGB_STUDIO_G22_NONE_P2020        = 3,
    SIMDRIVER_MPO_COLOR_SPACE_RESERVED                         = 4,
    SIMDRIVER_MPO_COLOR_SPACE_YCBCR_FULL_G22_NONE_P709_X601    = 5,
    SIMDRIVER_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P601       = 6,
    SIMDRIVER_MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P601         = 7,
    SIMDRIVER_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709       = 8,
    SIMDRIVER_MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P709         = 9,
    SIMDRIVER_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P2020      = 10,
    SIMDRIVER_MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P2020        = 11,
    SIMDRIVER_MPO_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020        = 12,
    SIMDRIVER_MPO_COLOR_SPACE_YCBCR_STUDIO_G2084_LEFT_P2020    = 13,
    SIMDRIVER_MPO_COLOR_SPACE_RGB_STUDIO_G2084_NONE_P2020      = 14,
    SIMDRIVER_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_TOPLEFT_P2020   = 15,
    SIMDRIVER_MPO_COLOR_SPACE_YCBCR_STUDIO_G2084_TOPLEFT_P2020 = 16,
    SIMDRIVER_MPO_COLOR_SPACE_CUSTOM                           = 0xFFFFFFFF
} SIMDRIVER_MPO_COLOR_SPACE_TYPE;

// ----- "SIMDRIVER_HDR_METADATA_TYPE" -------
typedef enum _SIMDRIVER_HDR_METADATA_TYPE
{
    SIMDRIVER_HDR_METADATA_TYPE_NONE  = 0,
    SIMDRIVER_HDR_METADATA_TYPE_HDR10 = 1,
} SIMDRIVER_HDR_METADATA_TYPE;

/*
ENUM definition for Pipe corresponding to MPO flip
*/
typedef enum _SIMDRIVER_PIPE_ID
{
    SIMDRIVER_NULL_PIPE       = 0x7F,
    SIMDRIVER_PIPE_ANY        = 0x7E,
    SIMDRIVER_PIPE_A          = 0,
    SIMDRIVER_PIPE_B          = 1,
    SIMDRIVER_PIPE_C          = 2,
    SIMDRIVER_PIPE_D          = 3,
    SIMDRIVER_MAX_INTEL_PIPES = 4
} SIMDRIVER_PIPE_ID;

//
// Structure for enable or Disable a particular feature.
//
typedef struct _SIMDRIVER_ENABLE_DISABLE_FEATURE_ARGS
{
    IN BOOLEAN bEnableFeature;                   // Enable/Disable the Specific Feature in ULT
    IN SIMDRIVER_DISPLAY_FEATURE eFeatureEnable; //  Enum indicating which feature to enable
} SIMDRIVER_ENABLE_DISABLE_FEATURE_ARGS, *PSIMDRIVER_ENABLE_DISABLE_FEATURE_ARGS;

typedef struct _SIMDRIVER_CREATE_RES_ARGS
{
    IN SIMDRIVER_PIXELFORMAT eFormat; // Surface format
    IN BOOLEAN bAuxSurf;              // Flag to indicate req for aux surface
    struct
    {
        ULONG ulLinear : 1;
        ULONG ulTiledW : 1;
        ULONG ulTiledX : 1;
        ULONG ulTiledY : 1;
        ULONG ulTiledYf : 1;
        ULONG ulTiledYs : 1;
        ULONG Reserved : 26;
    } Info;
    IN ULONG ulBaseWidth;           // Surface Width
    IN ULONG ulBaseHeight;          // Surface Height
                                    // Out parameters
    OUT UINT64 pGmmBlock;           // To be used in the Setsource address calls
    OUT UINT64 pUserVirtualAddress; // For the app to access the ubuffer using CPU
    OUT UINT64 u64SurfaceSize;      // For app to copy the private framebuffer content
    OUT ULONG ulPitch;
} SIMDRIVER_CREATE_RES_ARGS, *PSIMDRIVER_CREATE_RES_ARGS;

//----- SIMDRIVER_FREE_RESOURCE -----
typedef struct _SIMDRIVER_FREE_RES_ARGS
{
    IN UINT64 pGmmBlock;
} SIMDRIVER_FREE_RES_ARGS, *PSIMDRIVER_FREE_RES_ARGS;

// ------ "SIMDRIVER_GET_MPO_CAPS" -----
typedef struct _SIMDRIVER_MPO_CAPS
{
    UINT uiMaxPlanes;
    UINT uiNumCapabilityGroups;
} SIMDRIVER_MPO_CAPS, *PSIMDRIVER_MPO_CAPS;

typedef struct _SIMDRIVER_MPO_CAPS_ARGS
{
    IN ULONG ulVidpnSourceID;
    OUT SIMDRIVER_MPO_CAPS stMPOCaps;
} SIMDRIVER_MPO_CAPS_ARGS, *PSIMDRIVER_MPO_CAPS_ARGS;

// ------ "SIMDRIVER_MPO_GROUP_CAPS" -----
typedef struct _SIMDRIVER_MPO_GROUP_CAPS
{
    UINT uiMaxPlanes;
    UINT uiMaxStretchFactorNum;
    UINT uiMaxStretchFactorDenm;
    UINT uiMaxShrinkFactorNum;
    UINT uiMaxShrinkFactorDenm;
    UINT uiOverlayFtrCaps;
    UINT uiStereoCaps;
} SIMDRIVER_MPO_GROUP_CAPS, *PSIMDRIVER_MPO_GROUP_CAPS;

typedef struct _SIMDRIVER_MPO_GROUP_CAPS_ARGS
{
    // Need not Escape code inside this as UMD_GENERAL_ESCAPE_BUFFER of which this structure //would be part will have it.
    IN ULONG ulVidpnSourceID;
    IN UINT uiGroupIndex;
    OUT SIMDRIVER_MPO_GROUP_CAPS stMPOGroupCaps;
} SIMDRIVER_MPO_GROUP_CAPS_ARGS, *PSIMDRIVER_MPO_GROUP_CAPS_ARGS;

// ------ "SIMDRIVER_CHECK_MPO" -----
typedef struct _SIMDRIVER_M_RECT
{
    LONG left;
    LONG top;
    LONG right;
    LONG bottom;
} SIMDRIVER_M_RECT, *PSIMDRIVER_M_RECT;

typedef struct _SIMDRIVER_MPO_YPLANE_RECTS
{
    SIMDRIVER_M_RECT stMPOSrcRect;
    SIMDRIVER_M_RECT stMPODstRect;
    SIMDRIVER_M_RECT stMPOClipRect;
    SIMDRIVER_M_RECT stMPOSrcClipRect;
} SIMDRIVER_MPO_YPLANE_RECTS, *PSIMDRIVER_MPO_YPLANE_RECTS;

typedef struct _SIMDRIVER_MPO_FLIP_FLAGS
{
    union {
        struct
        {
            UINT VerticalFlip : 1;   // 0x00000001
            UINT HorizontalFlip : 1; // 0x00000002
            UINT Reserved : 30;      // 0xFFFFFFFC
        };
        UINT uiValue;
    };
} SIMDRIVER_MPO_FLIP_FLAGS, *PSIMDRIVER_MPO_FLIP_FLAGS;

typedef struct _SIMDRIVER_MPO_BLEND_VAL
{
    union {
        struct
        {
            UINT AlphaBlend : 1;
            UINT Reserved : 31;
        };
        UINT uiValue;
    };
} SIMDRIVER_MPO_BLEND_VAL, *PSIMDRIVER_MPO_BLEND_VAL;

typedef struct _SIMDRIVER_MPO_COLORSPACE_FLAGS
{
    union {
        struct
        {
            UINT NominalRange : 1; // 0-Default Range; 1-Limited Range
            UINT Space : 2;        // 0- BT601, 1-BT709, 2- BT2020
            UINT Format : 1;       // 0- RGB 1-YCbCr
            UINT Gamma : 2;        // 0 - G10 , 1- G22 ,2-ST2084
            UINT Reserved : 27;    // 0xFFFFFFF8
        };
        UINT uiValue;
    };
} SIMDRIVER_MPO_COLORSPACE_FLAGS, *PSIMDRIVER_MPO_COLORSPACE_FLAGS;

typedef struct _SIMDRIVER_MPO_PLANE_ATTRIBUTES
{
    SIMDRIVER_MPO_FLIP_FLAGS         stMPOFlags;
    SIMDRIVER_M_RECT                 stMPOSrcRect;
    SIMDRIVER_M_RECT                 stMPODstRect;
    SIMDRIVER_M_RECT                 stMPOClipRect;
    SIMDRIVER_M_RECT                 stMPOSrcClipRect;
    SIMDRIVER_MPO_PLANE_ORIENTATION  eHWOrientation;
    SIMDRIVER_MPO_BLEND_VAL          stMPOBlend;
    SIMDRIVER_MPO_VIDEO_FRAME_FORMAT eMPOVideoFormat;
    union {
        UINT                           uiMPOYCbCrFlags;
        SIMDRIVER_MPO_COLORSPACE_FLAGS stMPOCSFlags;
    };

    // Not in Dx9 Spec
    SIMDRIVER_MPO_STEREO_FORMAT    eMPOStereoFormat;
    BOOL                           bMPOLeftViewFrame0;
    BOOL                           bMPOBaseViewFrame0;
    SIMDRIVER_MPO_STEREO_FLIP_MODE eMPOStereoFlipMode;
    SIMDRIVER_MPO_STRETCH_QUALITY  eStretchQuality;
    SIMDRIVER_MPO_COLOR_SPACE_TYPE eColorSpace;
    // Currently Driver may not use this info.
    UINT                       uiDirtyRectCount;
    SIMDRIVER_M_RECT           DIRTYRECTS[SIMDRIVER_MAX_DIRTY_RECTS];
    SIMDRIVER_MPO_YPLANE_RECTS stYPlaneRects;
} SIMDRIVER_MPO_PLANE_ATTRIBUTES, *PSIMDRIVER_MPO_PLANE_ATTRIBUTES;

// Struct representing surface memory offset data
typedef struct _SIMDRIVER_SURFACE_MEM_OFFSET_INFO
{
    IN SIMDRIVER_SURFACE_MEMORY_TYPE eSurfaceMemType;
    union {
        IN ULONG ulLinearOffset;

        struct
        {
            IN ULONG ulTiledXOffset;
            IN ULONG ulTiledYOffset;
            IN ULONG ulTiledUVXOffset; // NV12 case
            IN ULONG ulTiledUVYOffset; // NV12 case
        };
    };

    IN ULONG ulUVDistance;  // For NV12 surface
    IN ULONG ulAuxDistance; // Control surface Aux Offset.
} SIMDRIVER_SURFACE_MEM_OFFSET_INFO, *PSIMDRIVER_SURFACE_MEM_OFFSET_INFO;

// SIMDRIVER_PIXELFORMAT is defined in SIMDRIVER_CREATE_RESOURCE escape structures/enums section of header.
typedef struct _SIMDRIVER_MPO_CHECKMPOSUPPORT_PLANE_INFO
{
    UINT                              uiLayerIndex;
    ULONG                             ulSize;          // adding for 2LM, this indicates the mem size
    UINT                              uiOSPlaneNumber; // This is the plane number that OS assigned for this plane. This is returned if we fail checkMPO due to this plane.
    BOOLEAN                           bIsDWMPlane;
    BOOLEAN                           bEnabled;
    BOOLEAN                           bIsAsyncMMIOFlip; // Not be used currently for MPO as it is always Synchronous flips..
    HANDLE                            hAllocation;
    SIMDRIVER_MPO_PLANE_ATTRIBUTES    stPlaneAttributes;
    SIMDRIVER_SURFACE_MEM_OFFSET_INFO stSurfaceMemInfo;
    SIMDRIVER_PIXELFORMAT             eULTPixelFormat;
} SIMDRIVER_MPO_CHECKMPOSUPPORT_PLANE_INFO, *PSIMDRIVER_MPO_CHECKMPOSUPPORT_PLANE_INFO;

typedef struct _SIMDRIVER_MPO_POST_COMPOSITION
{
    SIMDRIVER_MPO_FLIP_FLAGS        stMPOFlags;
    SIMDRIVER_M_RECT                stMPOSrcRect;
    SIMDRIVER_M_RECT                stMPODstRect;
    SIMDRIVER_MPO_PLANE_ORIENTATION eHWOrientation;
} SIMDRIVER_MPO_POST_COMPOSITION, *PSIMDRIVER_MPO_POST_COMPOSITION;

typedef struct _SIMDRIVER_MPO_CHECKMPOSUPPORT_PATH_INFO
{
    IN UINT uiPlaneCount;
    IN SIMDRIVER_MPO_CHECKMPOSUPPORT_PLANE_INFO stMPOPlaneInfo[SIMDRIVER_MAX_PLANES];
    IN UCHAR ucPipeIndex;
    IN ULONG ulDisplayUID;                                  // Only Pipe index should be sufficient but let's fill this also for implementation ease in SoftBIOS.
    IN BOOLEAN bHDREnabled;                                 // This flag will be set by MP based on OS commit. If OS enabled HDR then this will be set.
    IN SIMDRIVER_MPO_POST_COMPOSITION stMPOPostComposition; // this is filled if driver has to enable Pipe panel fitter.
} SIMDRIVER_MPO_CHECKMPOSUPPORT_PATH_INFO, *PSIMDRIVER_MPO_CHECKMPOSUPPORT_PATH_INFO;

typedef struct _SIMDRIVER_CHECKMPOSUPPORT_RETURN_INFO
{
    union {
        struct
        {
            UINT uiFailingPlane : 4; // 0 based index of first plane that is //causing the CheckMPOSupport to fail.
            UINT TryAgain : 1;       // Configuration not supported due to hw in //transition condition, this should shortly go away.
        };
        UINT uiValue;
    };
} SIMDRIVER_CHECKMPOSUPPORT_RETURN_INFO, *PSIMDRIVER_CHECKMPOSUPPORT_RETURN_INFO;

typedef struct _SIMDRIVER_CHECK_MPO_ARG
{
    IN SIMDRIVER_MPO_CHECKMPOSUPPORT_PATH_INFO stCheckMPOPathInfo[SIMDRIVER_MAX_PIPES];
    IN ULONG ulNumPaths;
    IN ULONG ulConfig;
    OUT BOOLEAN bSupported;
    OUT BOOLEAN bSecureSpriteBWExceeds;
    OUT ULONG ulFailureReason;
    OUT SIMDRIVER_CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo;
} SIMDRIVER_CHECK_MPO_ARGS, *PSIMDRIVER_CHECK_MPO_ARGS;

// ----- "SIMDRIVER_MPO_PLANE_SPECIFIC_INPUT_FLAGS" -------
typedef struct _SIMDRIVER_MPO_PLANE_SPECIFIC_INPUT_FLAGS
{
    union {
        struct
        {
            UINT Enabled : 1;                  // 0x00000001
            UINT FlipImmediate : 1;            // 0x00000002
            UINT FlipOnNextVSync : 1;          // 0x00000004
            UINT SharedPrimaryTransition : 1;  // 0x00000008 We are transitioning to or away from a shared managed primary allocation
            UINT IndependentFlipExclusive : 1; // 0x00000010
            UINT Reserved : 27;                // 0xFFFFFFE0
        };
        UINT Value;
    };
} SIMDRIVER_MPO_PLANE_SPECIFIC_INPUT_FLAGS, *PSIMDRIVER_MPO_PLANE_SPECIFIC_INPUT_FLAGS;

// ----- "SIMDRIVER_MPO_PLANE_SPECIFIC_OUTPUT_FLAGS" -------
typedef struct _SIMDRIVER_MPO_PLANE_SPECIFIC_OUTPUT_FLAGS
{
    union {
        struct
        {
            UINT FlipConvertedToImmediate : 1; // 0x00000001
            UINT PostPresentNeeded : 1;        // 0x00000002 Should only be set for immediate flips if driver requires a postpresent call on this plane
            UINT
                 HsyncInterruptCompletion : 1; // 0x00000004 Should be set for immediate flips that are completed on Hsync interrupt notification and not upon the return from the DDI.
            UINT Reserved : 29;                // 0xFFFFFFF8
        };
        UINT Value;
    };
} SIMDRIVER_MPO_PLANE_SPECIFIC_OUTPUT_FLAGS, *PSIMDRIVER_MPO_PLANE_SPECIFIC_OUTPUT_FLAGS;

// ----- ULT Escape - "SIMDRIVER_SET_SRC_ADD_MPO" -----
// SIMDRIVER_MPO_PLANE_ATTRIBUTES is defined in SIMDRIVER_CHECK_MPO escape structures/enums section of header.
typedef struct SIMDRIVER_MPO_FLIP_PLANE_INFO
{
    ULONG                                     ulSourceId;
    UINT                                      uiLayerIndex;
    BOOLEAN                                   bEnabled;
    BOOLEAN                                   bAffected;
    SIMDRIVER_MPO_PLANE_SPECIFIC_INPUT_FLAGS  stInputFlags;
    SIMDRIVER_MPO_PLANE_SPECIFIC_OUTPUT_FLAGS stOutputFlags;
    UINT                                      uiAllocationSegment;
    ULONG                                     AllocationAddress;
    HANDLE                                    hAllocation;
    UINT                                      uiMaxImmediateFlipLine;
    UINT                                      uiOSLayerIndex;
    ULONGLONG                                 ulPresentID;
    SIMDRIVER_MPO_PLANE_ATTRIBUTES            stPlaneAttributes;
} SIMDRIVER_MPO_FLIP_PLANE_INFO, *PSIMDRIVER_MPO_FLIP_PLANE_INFO;

// ----- "SIMDRIVER_MPO_SETVIDPNSOURCEADDRESS_OUTPUT_FLAGS" -------
typedef struct _SIMDRIVER_MPO_SETVIDPNSOURCEADDRESS_OUTPUT_FLAGS
{
    union {
        struct
        {
            UINT PrePresentNeeded : 1;
            UINT Reserved : 31; // 0xFFFFFFFE
        };
        UINT Value;
    };
} SIMDRIVER_MPO_SETVIDPNSOURCEADDRESS_OUTPUT_FLAGS;

typedef struct _SIMDRIVER_HDR_METADATA
{
    SIMDRIVER_HDR_METADATA_TYPE Type;
    UINT                        Size;
    VOID *                      pMetaData;
} SIMDRIVER_HDR_METADATA, *PSIMDRIVER_MPO_HDR_METADATA;

// ----- "SIMDRIVER_MPO_SETVIDPNSOURCEADDRESS_INPUT_FLAGS" -------
typedef struct _SIMDRIVER_MPO_SETVIDPNSOURCEADDRESS_INPUT_FLAGS
{
    union {
        struct
        {
            UINT FlipStereo : 1;              // 0x00000001 This is a flip from a stereo alloc. Used in addition to FlipImmediate or FlipOnNextVSync.
            UINT FlipStereoTemporaryMono : 1; // 0x00000002 This is a flip from a stereo alloc. The left image should used. Used in addition to FlipImmediate or FlipOnNextVSync.
            UINT FlipStereoPreferRight : 1;   // 0x00000004 This is a flip from a stereo alloc. The right image should used when cloning to a mono monitor. Used in addition to
                                              // FlipImmediate or FlipOnNextVSync.
            UINT RetryAtLowerIrql : 1;        // 0x00000008 This is called at lower IRQL after receiving a PrePresent request.
            UINT Reserved : 28;               // 0xFFFFFFF8
        };
        UINT Value;
    };
} SIMDRIVER_MPO_SETVIDPNSOURCEADDRESS_INPUT_FLAGS;

// SIMDRIVER_SETVIDPNSOURCEADDRESS_FLAGS is defined in SIMDRIVER_SET_SRC_ADDRESS escape structures/enums section of header.
typedef struct _SIMDRIVER_SET_SRC_ADD_MPO_ARGS
{
    SIMDRIVER_MPO_FLIP_PLANE_INFO                    stDxgkMPOPlaneArgs[SIMDRIVER_MAX_PLANES];
    ULONG                                            ulNumPlanes;
    DWORD                                            dwSourceID;
    SIMDRIVER_MPO_SETVIDPNSOURCEADDRESS_INPUT_FLAGS  stInputFlags;
    SIMDRIVER_MPO_SETVIDPNSOURCEADDRESS_OUTPUT_FLAGS stOutputFlags;
    PSIMDRIVER_MPO_HDR_METADATA                      pHDRMetaData;
    SIMDRIVER_PIPE_ID                                ePipeID;
    SIMDRIVER_MPO_POST_COMPOSITION                   stMPOPostComposition;
    BOOL                                             bULTCall;
} SIMDRIVER_SET_SRC_ADD_MPO_ARGS, *PSIMDRIVER_SET_SRC_ADD_MPO_ARGS;

typedef struct _SIMDRIVER_DISPLAY_FEATURE_ARGS
{
    IN ULONG ulSize;
    IN SIMDRIVER_DISPLAY_FEATURE_REQUEST_TYPE eServiceType;
    IN_OUT PVOID pMpoArgs;
    OUT ULONG ulStatus;
} SIMDRIVER_DISPLAY_FEATURE_ARGS, *PSIMDRIVER_DISPLAY_FEATURE_ARGS;

#pragma pack()

#endif // ! __SIMDRV_GFX_COMMON__
