/**
 * @file PyPlanes.h
 * @addtogroup CDll_MPO
 * @brief DLL that checks for the hardware support for the planes, present multiple surfaces on the screen, check MPO capabilities.
 * @remarks
 * MPO  DLL that checks for the hardware support for the planes, present multiple surfaces on the screen, check MPO capabilities and MPO group capabilities. \n
 * \attention Do not modify this API without consent from the author
 * @author	Ilamparithi Mahendran
 */

/*************************************************************************
**                                                                      **
**                    I N T E L   C O N F I D E N T I A L               **
**       Copyright (c) 2016 Intel Corporation All Rights Reserved.      **
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
**  distributed, or disclosed in any way without Intel’s prior express  **
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
#ifndef _PYPLANES_H_
#define _PYPLANES_H_

#include <Windows.h>

#define PYPLANES_MAX_PLANES 21
#define PYPLANES_MAX_RESOURCE 2

/*HDR Metadata SB Strcture Eq*/
typedef struct _PYPLANES_HDR_STATIC_METADATA
{
    USHORT usEOTF;
    USHORT usDisplayPrimariesX[3];
    USHORT usDisplayPrimariesY[3];
    USHORT usWhitePointX;
    USHORT usWhitePointY;
    ULONG  usMaxDisplayMasteringLuminance;
    ULONG  usMinDisplayMasteringLuminance;
    ULONG  usMaxCLL;
    ULONG  usMaxFALL; // Maximum Frame Average Light Level
} PYPLANES_HDR_STATIC_METADATA, *PPYPLANES_HDR_STATIC_METADATA;

/*Source & Dest Rectangle*/
typedef struct _PYPLANES_M_RECT
{
    LONG left;
    LONG top;
    LONG right;
    LONG bottom;
} PYPLANES_M_RECT, *PPYPLANES_M_RECT;

/*Src Pixel Format*/
typedef enum _PYPLANES_PIXELFORMAT
{
    PYPLANES_PIXEL_FORMAT_UNINITIALIZED = 0,
    PYPLANES_PIXEL_FORMAT_8BPP_INDEXED, // for 8bpp
    PYPLANES_PIXEL_FORMAT_B5G6R5X0,     // for 16bpp
    PYPLANES_PIXEL_FORMAT_B8G8R8X8,     // for 32bpp (default)
    PYPLANES_PIXEL_FORMAT_B8G8R8A8,
    PYPLANES_PIXEL_FORMAT_R8G8B8X8,
    PYPLANES_PIXEL_FORMAT_R8G8B8A8,
    PYPLANES_PIXEL_FORMAT_R10G10B10X2,         // for 32bpp 10bpc
    PYPLANES_PIXEL_FORMAT_R10G10B10A2,         // for 32bpp 10bpc
    PYPLANES_PIXEL_FORMAT_B10G10R10X2,         // for 32bpp 10bpc
    PYPLANES_PIXEL_FORMAT_B10G10R10A2,         // for 32bpp 10bpc
    PYPLANES_PIXEL_FORMAT_R10G10B10A2_XR_BIAS, // for 32bpp 10bpc, XR BIAS format (used by Win7)
    PYPLANES_PIXEL_FORMAT_R16G16B16X16F,       // for 64bpp, 16bit floating
    PYPLANES_PIXEL_FORMAT_R16G16B16A16F,
    PYPLANES_PIXEL_FORMAT_MAX, // To match the driver structure
    PYPLANES_PIXEL_FORMAT_NV12YUV420,
    PYPLANES_PIXEL_FORMAT_YUV422,
    PYPLANES_PIXEL_FORMAT_P010YUV420,
    PYPLANES_PIXEL_FORMAT_P012YUV420,
    PYPLANES_PIXEL_FORMAT_P016YUV420,
    PYPLANES_PIXEL_FORMAT_YUV444_10,
    PYPLANES_PIXEL_FORMAT_YUV422_10,
    PYPLANES_PIXEL_FORMAT_YUV422_12,
    PYPLANES_PIXEL_FORMAT_YUV422_16,
    PYPLANES_PIXEL_FORMAT_YUV444_8,
    PYPLANES_PIXEL_FORMAT_YUV444_12,
    PYPLANES_PIXEL_FORMAT_YUV444_16,
    PYPLANES_PIXEL_FORMAT_MAXALL,
} PYPLANES_PIXELFORMAT;

#define GET_GEN9_2016_PIXELFORMAT(PixelFormat) ((PixelFormat == PYPLANES_PIXEL_FORMAT_NV12YUV420) || (PixelFormat == PYPLANES_PIXEL_FORMAT_YUV422)) ? PixelFormat - 1 : PixelFormat

/*Surface memory type*/
typedef enum _PYPLANES_SURFACE_MEMORY_TYPE
{
    PYPLANES_SURFACE_MEMORY_INVALID        = 0,
    PYPLANES_SURFACE_MEMORY_LINEAR         = 1,  // Surface uses linear memory
    PYPLANES_SURFACE_MEMORY_X_TILED        = 2,  // Surface uses X tiled memory
    PYPLANES_SURFACE_MEMORY_Y_LEGACY_TILED = 4,  // Surface uses Legacy Y tiled memory (Gen9+)
    PYPLANES_SURFACE_MEMORY_Y_F_TILED      = 8,  // Surface uses Y F tiled memory
    PYPLANES_SURFACE_MEMORY_TILE4          = 16, // Surface uses Tile4 memory from DG2
} PYPLANES_SURFACE_MEMORY_TYPE;

/*ENUM defintion for color space type in MPO3 flip*/
typedef enum _PYPLANES_MPO_COLOR_SPACE_TYPE
{
    PYPLANES_MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709           = 0,
    PYPLANES_MPO_COLOR_SPACE_RGB_FULL_G10_NONE_P709           = 1,
    PYPLANES_MPO_COLOR_SPACE_RGB_STUDIO_G22_NONE_P709         = 2,
    PYPLANES_MPO_COLOR_SPACE_RGB_STUDIO_G22_NONE_P2020        = 3,
    PYPLANES_MPO_COLOR_SPACE_RESERVED                         = 4,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_FULL_G22_NONE_P709_X601    = 5,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P601       = 6,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P601         = 7,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709       = 8,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P709         = 9,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P2020      = 10,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P2020        = 11,
    PYPLANES_MPO_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020        = 12,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G2084_LEFT_P2020    = 13,
    PYPLANES_MPO_COLOR_SPACE_RGB_STUDIO_G2084_NONE_P2020      = 14,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_TOPLEFT_P2020   = 15,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G2084_TOPLEFT_P2020 = 16,
    PYPLANES_MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P2020          = 17,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_GHLG_TOPLEFT_P2020  = 18,
    PYPLANES_MPO_COLOR_SPACE_YCBCR_FULL_GHLG_TOPLEFT_P2020    = 19,
    PYPLANES_MPO_COLOR_SPACE_CUSTOM                           = 0xFFFFFFFF
} PYPLANES_MPO_COLOR_SPACE_TYPE;

typedef enum _PYPLANES_MPO_PLANE_ORIENTATION
{
    PYPLANES_MPO_ORIENTATION_DEFAULT = 1,                                // Default value
    PYPLANES_MPO_ORIENTATION_0       = PYPLANES_MPO_ORIENTATION_DEFAULT, // 0 degree
    PYPLANES_MPO_ORIENTATION_90      = 2,                                // 90 degree, supported Gen9 onwards
    PYPLANES_MPO_ORIENTATION_180     = 3,                                // 180 degree
    PYPLANES_MPO_ORIENTATION_270     = 4,                                // 270 degree, supported Gen9 onwards
    PYPLANES_MPO_ORIENTATION_MAX     = 5
} PYPLANES_MPO_PLANE_ORIENTATION;

typedef enum _PLANES_ERROR_CODE
{
    PLANES_SUCCESS                   = 0,
    PLANES_FAILURE                   = 1,
    PLANES_RESOURCE_CREATION_FAILURE = 2
} PLANES_ERROR_CODE;

/*Blend Mode of the plane*/
typedef struct _PYPLANES_MPO_BLEND_VAL
{
    union {
        struct
        {
            UINT AlphaBlend : 1;
            UINT Reserved : 31;
        };
        UINT uiValue;
    };
} PYPLANES_MPO_BLEND_VAL, *PPYPLANES_MPO_BLEND_VAL;

/*MPO Flips flags*/
typedef struct _PYPLANES_MPO_FLIP_FLAGS
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
} PYPLANES_MPO_FLIP_FLAGS, *PPYPLANES_MPO_FLIP_FLAGS;

/*MPO Plane In flags*/
typedef struct _PYPLANES_MPO_PLANE_IN_FLAGS
{
    union {
        struct
        {
            UINT Enabled : 1;                  // 0x00000001
            UINT FlipImmediate : 1;            // 0x00000002
            UINT FlipOnNextVSync : 1;          // 0x00000004
            UINT SharedPrimaryTransition : 1;  // 0x00000008
            UINT IndependentFlipExclusive : 1; // 0x00000010
            UINT Reserved : 27;                // 0xFFFFFFE0
        };
        UINT uiValue;
    };
} PYPLANES_MPO_PLANE_IN_FLAGS, *PPYPLANES_MPO_PLANE_IN_FLAGS;

/*Resource Info*/
typedef struct _PYPLANES_RESOURCE_INFO_
{
    UINT64 pGmmBlock;
    UINT64 pUserVirtualAddress;
    UINT64 u64SurfaceSize;
    ULONG  ulPitch;
} PYPLANES_RESOURCE_INFO, *PPYPLANES_RESOURCE_INFO;

/*Attributes of the plane*/
typedef struct _PLANE_INFO
{
    INT                            iPathIndex;
    UINT                           uiLayerIndex;
    BOOL                           bEnabled;
    PYPLANES_PIXELFORMAT           ePixelFormat;
    PYPLANES_SURFACE_MEMORY_TYPE   eSurfaceMemType;
    PYPLANES_M_RECT                stMPOSrcRect;
    PYPLANES_M_RECT                stMPODstRect;
    PYPLANES_M_RECT                stMPOClipRect;
    LONG                           lWidth;
    LONG                           lHeight;
    PYPLANES_MPO_PLANE_ORIENTATION eHWOrientation;
    PYPLANES_MPO_BLEND_VAL         stMPOBlendVal;
    PYPLANES_RESOURCE_INFO         stResourceInfo[PYPLANES_MAX_RESOURCE];
    INT                            iResourceInUse;
    PYPLANES_MPO_COLOR_SPACE_TYPE  eColorSpace;
    CHAR *                         cpDumpFilePath;
    UINT                           uiYCbCrFlags;
    PYPLANES_MPO_FLIP_FLAGS        stMPOFlipFlags;
    PYPLANES_MPO_PLANE_IN_FLAGS    stMPOPlaneInFlags;
} PLANE_INFO, *PPLANE_INFO;

/*Plane data*/
typedef struct _PLANES_
{
    UINT                         uiPlaneCount;
    PLANE_INFO                   stPlaneInfo[PYPLANES_MAX_PLANES];
    PYPLANES_HDR_STATIC_METADATA stMPOHDRMetaData;
    ULONG64                      ulTargetFlipTimeInUs;
    ULONG64                      uldelay;
} _PLANES_, *PPLANES;

PPLANES pPreviouspPlanes;

#endif
