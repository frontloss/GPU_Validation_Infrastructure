/*************************************************************************
**                                                                      **
**                    I N T E L   C O N F I D E N T I A L               **
**       Copyright (c) 2017 Intel Corporation All Rights Reserved.      **
**                                                                      **
**  The source code contained or described herein and all documents     **
**  related to the source code ("Material") are owned by Intel          **
**  Corporation or its suppliers or licensors. Title to the Material    **
**  remains with Intel Corporation or its suppliers and licensors. The  **
**  Material contains trade secrets and proprietary and confidential    **
**  information of Intel or its suppliers and licensors. The Material   **
**  is protected by worldwide copyright and trade secret laws and       **
**  treaty provisions. No part of the Material may be used, copied,     **
**  reproduced, modified, published, uploaded, posted, transmitted,     **
**  distributed, or disclosed in any way without Intel's prior express  **
**  written permission.                                                 **
**                                                                      **
**  No license under any patent, copyright, trade secret or other       **
**  intellectual property right is granted to or conferred upon you by  **
**  disclosure or delivery of the Materials, either expressly, by       **
**  implication, inducement, estoppel or otherwise. Any license under   **
**  such intellectual property rights must be express and approved by   **
**  Intel in writing.                                                   **
**                                                                      **
*************************************************************************/

/**
 * file name       Yangra_MPOArgs.h
 */

#ifndef YANGRA_MPO_ARGS_H
#define YANGRA_MPO_ARGS_H

#define MAX_PLANES_PER_PIPE 5
#define MAX_VIEWS 4 // MAX_PIPES

#define FILL_RGB_COLOR_INFO(pColorInfo, Gamut, RangeType, Model, GammaEncoding) \
    pColorInfo->ColorGamut     = Gamut;                                         \
    pColorInfo->ColorRangeType = RangeType;                                     \
    pColorInfo->ColorModel     = Model;                                         \
    pColorInfo->Encoding       = GammaEncoding;

// Args for CheckMPO

// Src Pixel Format.
// There is 1:1 maping between GVSTUB_PIXELFORMAT and SB_PIXELFORMAT. Any change in SB_PIXELFORMAT should be updated here also.
typedef enum _GVSTUB_PIXELFORMAT
{
    GVSTUB_PIXEL_FORMAT_UNINITIALIZED = 0,
    GVSTUB_PIXEL_FORMAT_8BPP_INDEXED, // for 8bpp
    GVSTUB_PIXEL_FORMAT_B5G6R5X0,     // for 16bpp
    GVSTUB_PIXEL_FORMAT_B8G8R8X8,     // for 32bpp (default)
    GVSTUB_PIXEL_FORMAT_B8G8R8A8,
    GVSTUB_PIXEL_FORMAT_R8G8B8X8,
    GVSTUB_PIXEL_FORMAT_R8G8B8A8,
    GVSTUB_PIXEL_FORMAT_R10G10B10X2,         // for 32bpp 10bpc
    GVSTUB_PIXEL_FORMAT_R10G10B10A2,         // for 32bpp 10bpc
    GVSTUB_PIXEL_FORMAT_B10G10R10X2,         // for 32bpp 10bpc
    GVSTUB_PIXEL_FORMAT_B10G10R10A2,         // for 32bpp 10bpc
    GVSTUB_PIXEL_FORMAT_R10G10B10A2_XR_BIAS, // for 32bpp 10bpc, XR BIAS format (used by Win7)
    GVSTUB_PIXEL_FORMAT_R16G16B16X16F,       // for 64bpp, 16bit floating
    GVSTUB_PIXEL_FORMAT_R16G16B16A16F,
    GVSTUB_PIXEL_FORMAT_MAX, // To match the driver structure
    GVSTUB_PIXEL_FORMAT_NV12YUV420,
    GVSTUB_PIXEL_FORMAT_YUV422,
    GVSTUB_PIXEL_FORMAT_P010YUV420,
    GVSTUB_PIXEL_FORMAT_P012YUV420,
    GVSTUB_PIXEL_FORMAT_P016YUV420,
    GVSTUB_PIXEL_FORMAT_YUV444_10,
    GVSTUB_PIXEL_FORMAT_YUV422_10,
    GVSTUB_PIXEL_FORMAT_YUV422_12,
    GVSTUB_PIXEL_FORMAT_YUV422_16,
    GVSTUB_PIXEL_FORMAT_YUV444_8,
    GVSTUB_PIXEL_FORMAT_YUV444_12,
    GVSTUB_PIXEL_FORMAT_YUV444_16,
    GVSTUB_PIXEL_FORMAT_MAXALL,
} GVSTUB_PIXELFORMAT;

typedef struct DD_CHECK_MPO_OUT_FLAGS
{
    union {
        struct
        {
            ULONG FailingView : 8;       // The 0 based index of the first view that could not be supported
            ULONG FailingLayerIndex : 8; // The 0 based index of the first plane that could not be supported
            ULONG TryAgain : 1;          // The configuration is not supported due to a transition condition, which should shortly go away
            ULONG Reserved : 15;
        };
        ULONG Value;
    };
} DD_CHECK_MPO_OUT_FLAGS;

typedef struct _DD_FLIP_MPO_IN_FLAGS
{
    union {
        struct
        {
            ULONG ModeChange : 1;
            ULONG FlipStereo : 1;
            ULONG FlipStereoTemporaryMono : 1;
            ULONG FlipStereoPreferRight : 1;
            ULONG RetryAtLowerIrql : 1;
            ULONG Reserved : 27;
        };
        ULONG Value;
    };
} DD_FLIP_MPO_IN_FLAGS;

typedef struct _DD_FLIP_MPO_OUT_FLAGS
{
    union {
        struct
        {
            ULONG PrePresentNeeded : 1;
            ULONG Reserved : 31;
        };
        ULONG Value;
    };
} DD_FLIP_MPO_OUT_FLAGS;

typedef struct _DD_FLIP_MPO_PLANE_IN_FLAGS
{
    union {
        struct
        {
            ULONG Enabled : 1;
            ULONG FlipImmediate : 1;
            ULONG FlipOnNextVSync : 1;
            ULONG SharedPrimaryTransition : 1;
            ULONG IndependentFlipExclusive : 1;
            ULONG Reserved : 27;
        };
        ULONG Value;
    };
} DD_FLIP_MPO_PLANE_IN_FLAGS;

typedef struct _DD_FLIP_MPO_PLANE_OUT_FLAGS
{
    union {
        struct
        {
            ULONG FlipConvertedToImmediate : 1;
            ULONG PostPresentNeeded : 1;
            ULONG HsyncInterruptCompletion : 1;
            ULONG Reserved : 29;
        };
        ULONG Value;
    };
} DD_FLIP_MPO_PLANE_OUT_FLAGS;

typedef struct _DD_RECT
{
    LONG lLeft;
    LONG lTop;
    LONG lRight;
    LONG lBottom;
} DD_RECT;

typedef struct _DD_MPO_PLANE_RECTS
{
    DD_RECT stSource;
    DD_RECT stDest;
    DD_RECT stClip;
} DD_MPO_PLANE_RECTS;

typedef enum _DD_ROTATION
{
    ORIENTATION_DEFAULT = 0,
    ORIENTATION_0       = ORIENTATION_DEFAULT,
    ORIENTATION_90,
    ORIENTATION_180,
    ORIENTATION_270,
    ORIENTATION_MAX,
    ORIENTATION_UNKNOWN
} DD_ROTATION;

typedef struct _DD_FLIP_MPO_PLANE_ATTRIB_FLAGS
{
    union {
        struct
        {
            ULONG VerticalFlip : 1;
            ULONG HorizontalFlip : 1;
            ULONG AlphaBlend : 1;
            ULONG HighQualityStretch : 1;
            ULONG Reserved : 28;
        };
        ULONG ulValue;
    };
} DD_FLIP_MPO_PLANE_ATTRIB_FLAGS;

typedef enum _DD_COLOR_MODEL
{
    DD_COLOR_MODEL_UNINITIALIZED   = 0,
    DD_COLOR_MODEL_RGB             = 1,
    DD_COLOR_MODEL_YCBCR_601       = 2,
    DD_COLOR_MODEL_YCBCR_709       = 3,
    DD_COLOR_MODEL_YCBCR_2020      = 4,
    DD_COLOR_MODEL_YCBCR_PREFERRED = 5,
    DD_COLOR_MODEL_SCRGB           = 6,
    DD_COLOR_MODEL_INTENSITY_ONLY  = 7,
    DD_COLOR_MODEL_CUSTOM          = 8,
    DD_COLOR_MODEL_MAX
} DD_COLOR_MODEL;

typedef enum _DD_COLOR_RANGE
{
    DD_COLOR_RANGE_FULL = 0,
    DD_COLOR_RANGE_8BIT_LIMITED, // 16 - 235
    DD_COLOR_RANGE_10BIT_LIMITED,
    DD_COLOR_RANGE_12BIT_LIMITED
} DD_COLOR_RANGE;

typedef enum _DD_COLOR_RANGE_TYPE
{
    DD_COLOR_RANGE_TYPE_DEFAULT = 0,
    DD_COLOR_RANGE_TYPE_LIMITED = 1,
    DD_COLOR_RANGE_TYPE_FULL    = 2,
    DD_COLOR_RANGE_TYPE_MAX
} DD_COLOR_RANGE_TYPE;

typedef enum _DD_MPO_HDR_METADATA_TYPE
{
    DD_MPO_HDR_METADATA_TYPE_NONE       = 0,
    DD_MPO_HDR_METADATA_TYPE_HDR10      = 1,
    DD_MPO_HDR_METADATA_TYPE_DEFAULT    = 2,
    DD_MPO_HDR_METADATA_TYPE_UMD_ESCAPE = 3 // Not handled currently.
} DD_MPO_HDR_METADATA_TYPE;

typedef enum _DD_COLOR_YCBCR_SUBSAMPLING
{
    DD_COLOR_SUBSAMPLING_UNKNOWN    = 0,
    DD_COLOR_SUBSAMPLING_444_PACKED = 1,
    DD_COLOR_SUBSAMPLING_422_PACKED = 2,
    DD_COLOR_SUBSAMPLING_422_PLANAR = 3,
    DD_COLOR_SUBSAMPLING_420_PLANAR = 4, // NV12, P0xx YCbCr formats
    DD_COLOR_SUBSAMPLING_MAX
} DD_COLOR_YCBCR_SUBSAMPLING;

typedef enum _DD_COLOR_ENCODING
{
    DD_COLOR_ENCODING_UNKNOWN = 0,
    DD_COLOR_ENCODING_LINEAR  = 1,
    DD_COLOR_ENCODING_SRGB    = 2,
    DD_COLOR_ENCODING_2084    = 3,
    DD_COLOR_ENCODING_HLG     = 4, // HLG - Hybrid Log Gamma
    DD_COLOR_ENCODING_MAX
} DD_COLOR_ENCODING;

typedef enum _DD_COLOR_GAMUT
{
    DD_COLOR_GAMUT_UNKNOWN = 0,
    DD_COLOR_GAMUT_601     = 1,
    DD_COLOR_GAMUT_709     = 2,
    DD_COLOR_GAMUT_2020    = 3,
    DD_COLOR_GAMUT_DCIP3   = 4,
    DD_COLOR_GAMUT_CUSTOM  = 5,
    DD_COLOR_GAMUT_MAX
} DD_COLOR_GAMUT;

typedef struct _DD_COLOR_CHROMATICITY
{
    ULONG CIE_xWhite;
    ULONG CIE_yWhite;
    ULONG CIE_xRed;
    ULONG CIE_yRed;
    ULONG CIE_xGreen;
    ULONG CIE_yGreen;
    ULONG CIE_xBlue;
    ULONG CIE_yBlue;
} DD_COLOR_CHROMATICITY;

typedef struct _DD_COLOR_OPTICAL_DESC
{
    ULONG                    MinLuminance;
    ULONG                    MaxLuminance;
    ULONG                    MaxFALL;
    ULONG                    MaxCLL;
    DD_MPO_HDR_METADATA_TYPE HdrMetadataType;
} DD_COLOR_OPTICAL_DESC;

typedef enum _DD_CONTENT_TYPE
{
    DD_CONTENT_TYPE_INVALID = 0,
    DD_CONTENT_TYPE_SDR     = 1,
    DD_CONTENT_TYPE_WCG     = 2,
    DD_CONTENT_TYPE_HDR     = 3
} DD_CONTENT_TYPE;

typedef struct _DD_COLOR_PIXEL_DESC
{
    DD_COLOR_MODEL             ColorModel;
    DD_COLOR_RANGE_TYPE        ColorRangeType;
    DD_COLOR_ENCODING          Encoding;
    DD_COLOR_GAMUT             ColorGamut;
    DD_COLOR_OPTICAL_DESC      OpticalDesc;
    UCHAR                      BitsPerColor;
    DD_COLOR_YCBCR_SUBSAMPLING YCbCrSubSampling;
    DD_COLOR_CHROMATICITY      Chromaticity;
    ULONG                      SdrContentLuminance;
    DD_CONTENT_TYPE            ContentType;
} DD_COLOR_PIXEL_DESC;

typedef struct _DD_FLIP_MPO_PLANE_ATTRIBUTES
{
    DD_FLIP_MPO_PLANE_ATTRIB_FLAGS stFlags;
    DD_MPO_PLANE_RECTS             stRect;
    DD_ROTATION                    eRotation;
    DD_COLOR_PIXEL_DESC            stColorInfo;
    DD_RECT                        stBoundedDirtyRect;
} DD_FLIP_MPO_PLANE_ATTRIBUTES;

typedef enum _DD_FLIP_TYPE
{
    DD_FLIP_TYPE_UNKNOWN = 0,
    DD_FLIP_NO_MPO,
    DD_FLIP_BASE_MPO,
    DD_FLIP_MPO_2,
    DD_FLIP_MPO_3
} DD_FLIP_TYPE;

typedef union _DD_LARGE_INTEGER {
    struct
    {
        ULONG LowPart;
        LONG  HighPart;
    };
    LONG64 QuadPart;
} DD_LARGE_INTEGER;

typedef struct _DD_FLIP_MPO_PLANE
{
    ULONG                        ulLayerIndex;
    ULONG64                      ulPresentId;
    DD_FLIP_MPO_PLANE_IN_FLAGS   stPlaneInFlags;
    DD_FLIP_MPO_PLANE_OUT_FLAGS  stPlaneOutFlags;
    ULONG                        ulMaxImmediateFlipLine;
    ULONG                        ulAllocationSegment;
    DD_LARGE_INTEGER             ulAllocationAddress;
    HANDLE                       hAllocation;
    DD_FLIP_MPO_PLANE_ATTRIBUTES stPlaneAttributes;
} DD_FLIP_MPO_PLANE;

typedef struct _DD_HDR_STATIC_METADATA
{
    USHORT EOTF;
    USHORT DisplayPrimariesX[3];
    USHORT DisplayPrimariesY[3];
    USHORT WhitePointX;
    USHORT WhitePointY;
    ULONG  MaxDisplayMasteringLuminance; // This is in milli nits.    //TODO Review: remove Display. Add milliNits to variable.
    ULONG  MinDisplayMasteringLuminance; // This is in milli nits.
    ULONG  MaxCLL;                       // This is in milli nits.
    ULONG  MaxFALL;                      // Maximum Frame Average Light Level. This is in milli nits.
} DD_HDR_STATIC_METADATA;

typedef struct _DD_MPO_HDR_METADATA
{
    DD_MPO_HDR_METADATA_TYPE HdrMetadataType;
    DD_HDR_STATIC_METADATA   HdrStaticMetaData;
} DD_MPO_HDR_METADATA;

typedef struct _DD_ARG_FLIP_MPO
{
    IN ULONG ulVidPnSourceId;
    IN DD_FLIP_TYPE eFlipType;
    IN DD_FLIP_MPO_IN_FLAGS stCommonInFlags;
    OUT DD_FLIP_MPO_OUT_FLAGS stCommonOutFlags;
    IN ULONG ulPlaneCount;
    IN DD_FLIP_MPO_PLANE *pPlanes;
    IN ULONG ulDuration;
    IN DD_MPO_HDR_METADATA HDRMetaData;
    IN ULONG64 TargetFlipTimeInUs;
    // TBD - below to be added later.
    // DD_MULTIPLANE_OVERLAY_POST_COMPOSITION* pPostComposition;
    // DD_HDR_METADATA* pHDRMetaData;
    IN BOOLEAN bStubCall;
} DD_ARG_FLIP_MPO;

typedef struct _DD_CHECK_MPO_VIEW_DETAILS
{
    ULONG             PlaneCount;
    DD_FLIP_MPO_PLANE Planes[MAX_PLANES_PER_PIPE];
    // TBD - below to be added later.
    // DD_MULTIPLANE_OVERLAY_POST_COMPOSITION* pPostComposition;
    // DD_HDR_METADATA* pHDRMetaData;
} DD_CHECK_MPO_VIEW_DETAILS;

typedef struct _DD_ARG_CHECK_MPO
{
    IN DD_CHECK_MPO_VIEW_DETAILS *pViews;
    OUT BOOLEAN Supported;
    OUT DD_CHECK_MPO_OUT_FLAGS OutFlags;
} DD_ARG_CHECK_MPO;

typedef struct _DD_MPO_CAPS
{
    union {
        struct
        {
            ULONG Rotation : 1;                       // Full rotation
            ULONG RotationWithoutIndependentFlip : 1; // Rotation, but without simultaneous IndependentFlip support
            ULONG VerticalFlip : 1;                   // Can flip the data vertically
            ULONG HorizontalFlip : 1;                 // Can flip the data horizontally
            ULONG StretchRGB : 1;                     // Supports RGB formats
            ULONG StretchYUV : 1;                     // Supports YUV formats
            ULONG BilinearFilter : 1;                 // Blinear filtering
            ULONG HighFilter : 1;                     // Better than bilinear filtering
            ULONG Shared : 1;                         // MPO resources are shared across VidPnSources
            ULONG Immediate : 1;                      // Immediate flip support
            ULONG Plane0ForVirtualModeOnly : 1;       // Stretching plane 0 will also stretch the HW cursor and should only be used for virtual mode support
            ULONG QueuedFlip : 1;                     // Queued flip support
            ULONG FlipQSupportParamChange : 1;        // Allow Queued flips with attribute changes or different set of enabled/disabled planes
            ULONG FlipQSupportFenceSync : 1;          // Capablity to monitor fence submitted to GPU and write the monitored fence when flip is visible
            ULONG Reserved : 18;
        };
        ULONG Value;
    };
} DD_MPO_CAPS;

typedef struct _DD_GET_MPO_CAPS_ARG
{
    IN ULONG VidPnSourceId;
    IN ULONG PipeId;
    OUT ULONG MaxPlanes;
    OUT ULONG MaxRgbPlanes;
    OUT ULONG MaxYuvPlanes;
    OUT DD_MPO_CAPS OverlayCaps;
    OUT ULONG MaxStretchFactorMultBy100;
    OUT ULONG MaxShrinkFactorPlanarMultBy100;
    OUT ULONG MaxShrinkFactorNonPlanarMultBy100;
    OUT ULONG MaxFlipQueues;     // Valid only for QueuedFlip
    OUT ULONG MaxFlipQueueDepth; // Valid only for QueuedFlip; Assuming symmetrical depth for each queue
} DD_GET_MPO_CAPS_ARG;

#endif // !YANGRA_MPO_ARGS_H
