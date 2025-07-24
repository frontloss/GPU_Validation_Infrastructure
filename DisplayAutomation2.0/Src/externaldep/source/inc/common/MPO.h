/*===========================================================================
; MPO.h
;----------------------------------------------------------------------------
;	Copyright (c) 2013-2014  Intel Corporation.
;	All Rights Reserved.  Copyright notice does not imply publication.
;	This software is protected as an unpublished work.  This software
;	contains the valuable trade secrets of Intel Corporation, and must
;	and must be maintained in confidence.
;
; File Description:
;	This file defines MPO related structures for LP platforms
;
;--------------------------------------------------------------------------*/

#ifndef _MPO_H_
#define _MPO_H_

//#ifndef _WINDEF_
//#include<windef.h>
//#endif

#ifdef _COMMON_PPA
#include "OMPTool.h"
#endif

#ifndef BOOL
typedef int BOOL, *PBOOL;
#endif

#define MAX_DIRTY_RECTS 8

// Includes only in headers which need to define ULONG, UINT typedefs.
// Definitions based on functionality..
/**************** CAPS Reporting *****************************/
// MPO Caps
typedef struct _MPO_CAPS
{
    UINT uiMaxPlanes;
    UINT uiNumCapabilityGroups;
    UINT uiColorSpaceSupported;
} MPO_CAPS, *PMPO_CAPS;

// MPO Group Caps
typedef enum _MPO_FEATURE_CAPS
{
    MPO_FTR_CAPS_ROTN_WITHOUT_IFLIP = 0x1,
    MPO_FTR_CAPS_VER_FLIP           = 0x2,
    MPO_FTR_CAPS_HOR_FLIP           = 0x4,
    MPO_FTR_CAPS_DEINTERLACE        = 0x8,
    MPO_FTR_CAPS_STEREO             = 0x10, // This is Dx11 Specific
    // For Dx9, the below enum values are respectively 0x10, 0x20, 0x40 and 0x80 is missing, so for MPO_FTR_CAPS_HIGH value is 0x100.
    MPO_FTR_CAPS_RGB                          = 0x20,
    MPO_FTR_CAPS_YUV                          = 0x40,
    MPO_FTR_CAPS_BILINEAR_FILTER              = 0x80,
    MPO_FTR_CAPS_HIGH_FILTER                  = 0x100,
    MPO_FTR_CAPS_ROTN                         = 0x200, // valid only for >=win10
    MPO_FTR_CAPS_FULLSCREEN_POST_COMPOSITION  = 0x400,
    MPO_FTR_RESERVED1                         = 0x800,
    MPO_FTR_CAPS_SHARED                       = 0x1000,
    MPO_FTR_CAPS_IMMEDIATE                    = 0x2000,
    MPO_FTR_CAPS_PLANE0_FOR_VIRTUAL_MODE_ONLY = 0x4000,
} MPO_FEATURE_CAPS,
*PMPO_FEATURE_CAPS;

#define MPO_FEATURE_CAPS_WIN_8_1                                                                                                                                              \
    (MPO_FTR_CAPS_ROTN_WITHOUT_IFLIP | MPO_FTR_CAPS_VER_FLIP | MPO_FTR_CAPS_HOR_FLIP | MPO_FTR_CAPS_DEINTERLACE | MPO_FTR_CAPS_STEREO | MPO_FTR_CAPS_RGB | MPO_FTR_CAPS_YUV | \
     MPO_FTR_CAPS_BILINEAR_FILTER | MPO_FTR_CAPS_HIGH_FILTER)

#define MPO_FEATURE_CAPS_WIN_TH (MPO_FEATURE_CAPS_WIN_8_1 | MPO_FTR_CAPS_ROTN)

#define MPO_FEATURE_CAPS_WIN_RS \
    (MPO_FEATURE_CAPS_WIN_TH | MPO_FTR_CAPS_FULLSCREEN_POST_COMPOSITION | MPO_FTR_CAPS_SHARED | MPO_FTR_CAPS_IMMEDIATE | MPO_FTR_CAPS_PLANE0_FOR_VIRTUAL_MODE_ONLY)
// Dx11 Specific..
typedef enum _MPO_STEREO_CAPS
{
    MPO_FTR_CAPS_SEPARATE        = 0x1,
    MPO_FTR_CAPS_ROW_INTERLEAVED = 0x4, //???? 0x2 is missing
    MPO_FTR_CAPS_COL_INTERLEAVED = 0x8,
    MPO_FTR_CAPS_CHECKERBOARD    = 0x10,
    MPO_FTR_CAPS_FLIP_MODE       = 0x20
} MPO_STEREO_CAPS,
*PMPO_STEREO_CAPS;

// This enum is removed in Dx11 Spec while in Dx9 it is kept though Stretching attribute is removed even in Dx9 as it is captured in a different way..
typedef enum _MPO_FILTER_TYPE
{
    MPO_FTR_CAPS_FILTER_CAPS_BRIGHTNESS = 0x1,
    MPO_FTR_CAPS_FILTER_CAPS_CONTRAST   = 0x2,
    MPO_FTR_CAPS_FILTER_CAPS_HUE        = 0x4,
    MPO_FTR_CAPS_FILTER_CAPS_SATURATION = 0x8,
} MPO_FILTER_TYPE,
*PMPO_FILTER_TYPE;

typedef enum _MPO_COLOR_SPACE_TYPE
{
    MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709           = 0,
    MPO_COLOR_SPACE_RGB_FULL_G10_NONE_P709           = 1,
    MPO_COLOR_SPACE_RGB_STUDIO_G22_NONE_P709         = 2,
    MPO_COLOR_SPACE_RGB_STUDIO_G22_NONE_P2020        = 3,
    MPO_COLOR_SPACE_RESERVED                         = 4,
    MPO_COLOR_SPACE_YCBCR_FULL_G22_NONE_P709_X601    = 5,
    MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P601       = 6,
    MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P601         = 7,
    MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709       = 8,
    MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P709         = 9,
    MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P2020      = 10,
    MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P2020        = 11,
    MPO_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020        = 12,
    MPO_COLOR_SPACE_YCBCR_STUDIO_G2084_LEFT_P2020    = 13,
    MPO_COLOR_SPACE_RGB_STUDIO_G2084_NONE_P2020      = 14,
    MPO_COLOR_SPACE_YCBCR_STUDIO_G22_TOPLEFT_P2020   = 15,
    MPO_COLOR_SPACE_YCBCR_STUDIO_G2084_TOPLEFT_P2020 = 16,
    MPO_COLOR_SPACE_CUSTOM                           = 0xFFFFFFFF
} MPO_COLOR_SPACE_TYPE;

// Since the parent OS structure defines floating point variables in below structure, Driver will have to do //save\restore of floating point state to return this every time. To
// avoid this, Driver is going to return the //floating point value as numerator and denominator. UMD can calculate it as floating point value.
typedef struct _MPO_GROUP_CAPS
{
    UINT uiMaxPlanes;
    UINT uiMaxStretchFactorNum;
    UINT uiMaxStretchFactorDenm;
    UINT uiMaxShrinkFactorNum;
    UINT uiMaxShrinkFactorDenm;
    UINT uiMaxPlanarShrinkFactorNum;
    UINT uiMaxPlanarShrinkFactorDenm;
    UINT uiOverlayFtrCaps;
    UINT uiStereoCaps;
} MPO_GROUP_CAPS, *PMPO_GROUP_CAPS;

// This structure has been removed from Spec but if we want to give Hue\Saturation info, OS should know the ranges and eventually this might come back. Hence, grayed out currently,
// can be had as commented structure in header.
typedef struct _MPO_FILTER_RANGE
{
    INT   iMinimum;
    INT   iMaximum;
    INT   iDefault;
    float fMultiplier;
} MPO_FILTER_RANGE, *PMPO_FILTER_RANGE;

/**************************** Check MPO Support ***********************************/
// Use the below definition..
typedef struct _MPO_FLIP_FLAGS
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
} MPO_FLIP_FLAGS, *PMPO_FLIP_FLAGS;

// Use the below definition..
typedef struct _MPO_BLEND_VAL
{
    union {
        struct
        {
            UINT AlphaBlend : 1; // 0x00000001
            UINT Reserved : 31;  // 0xFFFFFFFE
        };
        UINT uiValue;
    };
} MPO_BLEND_VAL, *PMPO_BLEND_VAL;

typedef struct _MPO_YCbCr_FLAGS
{
    union {
        struct
        {
            UINT NominalRange : 1; // 0x00000001
            UINT Bt709 : 1;        // 0x00000002
            UINT xvYCC : 1;        // 0x00000004
            UINT Reserved : 1;     // 0xFFFFFFF8
        };
        UINT uiValue;
    };
} MPO_YCbCr_FLAGS, *PMPO_YCbCr_FLAGS;

/* Color space constants
 */
/*--ColorFormat-*/
#define MPO_CS_RGB 0
#define MPO_CS_YCBCR 1
/*--ColorRange-*/
#define MPO_CS_FULL 0
#define MPO_CS_NOMINAL 1
#define MPO_CS_XR_BIAS 2
#define MPO_CS_XVYCC 3
/*--ColorSpace-*/
#define MPO_CS_BT601 0
#define MPO_CS_BT709 1
#define MPO_CS_BT2020 2
/*--Gamma-*/
#define MPO_CS_G10 0 //??TO Check
#define MPO_CS_G22 1
#define MPO_CS_G2084 2

#define MPO_CS_SPACE_BITPOS 1
#define MPO_CS_FORMAT_BITPOS 3
#define MPO_CS_GAMMA_BITPOS 4
#define MPO_CS_MAX_VALUE 2 ^ 5

#define MPO_CS_DATA(format, range, gamma, space) ((gamma << MPO_CS_GAMMA_BITPOS) | (format << MPO_CS_FORMAT_BITPOS) | (space << MPO_CS_SPACE_BITPOS) | range)

typedef struct _MPO_COLORSPACE_FLAGS
{
    union {
        struct
        {
            UINT NominalRange : 1; // 0-Default Range; 1-Limited Range
            UINT Space : 2;        // 0- BT601, 1-BT709, 2- BT2020
            UINT Format : 1;       // 0- RGB 1-YCbCr
            UINT Gamma : 2;        // 0 - G10 , 1- G22 ,2-ST2084
            UINT Reserved : 26;    // 0xFFFFFF70
        };
        UINT uiValue;
    };
} MPO_COLORSPACE_FLAGS, *PMPO_COLORSPACE_FLAGS;

typedef struct _MPO_MULTIPLANEOVERLAYCAPS
{
    union {
        struct
        {
            UINT Rotation : 1;                       // Full rotation
            UINT RotationWithoutIndependentFlip : 1; // Rotation, but without simultaneous IndependentFlip support
            UINT VerticalFlip : 1;                   // Can flip the data vertically
            UINT HorizontalFlip : 1;                 // Can flip the data horizontally
            UINT StretchRGB : 1;                     // Supports RGB formats
            UINT StretchYUV : 1;                     // Supports YUV formats
            UINT BilinearFilter : 1;                 // Blinear filtering
            UINT HighFilter : 1;                     // Better than bilinear filtering
            UINT Shared : 1;                         // MPO resources are shared across VidPnSources
            UINT Immediate : 1;                      // Immediate flip support
            UINT Plane0ForVirtualModeOnly : 1;       // Stretching plane 0 will also stretch the HW cursor and should only be used for virtual mode support
            UINT Reserved : 21;
        };
        UINT Value;
    };
} MPO_MULTIPLANEOVERLAYCAPS;

typedef struct _MPO_GETMULTIPLANEOVERLAYCAPS
{
    UINT                      VidPnSourceId;    // [in]
    UINT                      MaxPlanes;        // [out] Total number of planes supported (including the DWM's primary)
    UINT                      MaxRGBPlanes;     // [out] Maximum number of RGB planes supported (including the DWM's primary)
    UINT                      MaxYUVPlanes;     // [out] Maximum number of YUV planes supported
    MPO_MULTIPLANEOVERLAYCAPS OverlayCaps;      // [out] Plane capabilities
    float                     MaxStretchFactor; // [out]
    float                     MaxShrinkFactor;  // [out]
} MPO_GETMULTIPLANEOVERLAYCAPS;

// This is forward declaration. Actaul enum is defined in SbArgs.h
typedef enum _PLANE_ORIENTATION PLANE_ORIENTATION;

// This structure has been removed from Spec but if we want to give Hue\Saturation info, OS should know the ranges and eventually this might come back. Hence, grayed out currently,
// can be had as commented structure in header. Matches the Kernel Flip also..
typedef struct _MPO_FILTER_VAL
{
    MPO_FILTER_TYPE stMPOFilterType;
    BOOLEAN         bEnabled;
    INT             iValue;
} MPO_FILTER_VAL, *PMPO_FILTER_VAL;

// Not in Dx9 spec
// Matches Kernel flip attribute.
typedef enum _MPO_VIDEO_FRAME_FORMAT
{
    MPO_VIDEO_FRAME_FORMAT_PROGRESSIVE                   = 0x0,
    MPO_VIDEO_FRAME_FORMAT_INTERLACED_TOP_FIELD_FIRST    = 0x1,
    MPO_VIDEO_FRAME_FORMAT_INTERLACED_BOTTOM_FIELD_FIRST = 0x2
} MPO_VIDEO_FRAME_FORMAT,
*PMPO_VIDEO_FRAME_FORMAT;

// Not in Dx9 Spec
// Matches Kernel flip attribute.
typedef enum _MPO_STEREO_FORMAT
{
    MPO_FORMAT_MONO               = 0,
    MPO_FORMAT_HOR                = 1,
    MPO_FORMAT_VER                = 2,
    MPO_FORMAT_SEPARATE           = 3,
    MPO_FORMAT_ROW_INTERLEAVED    = 5, //??????? 4 is missing ?????
    MPO_FORMAT_COLUMN_INTERLEAVED = 6,
    MPO_FORMAT_CHECKBOARD         = 7
} MPO_STEREO_FORMAT,
*PMPO_STEREO_FORMAT;

// Not in Dx9 Spec
// Matches Kernel flip attribute.
typedef enum _MPO_STEREO_FLIP_MODE
{
    MPO_FLIP_NONE   = 0,
    MPO_FLIP_FRAME0 = 1,
    MPO_FLIP_FRAME1 = 2
} MPO_STEREO_FLIP_MODE,
*PMPO_STEREO_FLIP_MODE;

typedef enum _MPO_STRETCH_QUALITY
{
    MPO_STRETCH_QUALITY_BILINEAR = 0x1, // Bilinear
    MPO_STRETCH_QUALITY_HIGH     = 0x2  // Maximum
} MPO_STRETCH_QUALITY,
*PMPO_STRETCH_QUALITY;

typedef struct _M_RECT
{
    LONG left;
    LONG top;
    LONG right;
    LONG bottom;
} M_RECT, *PM_RECT;

#define RECT_WIDTH(rect) ((rect).right - (rect).left)
#define RECT_HEIGHT(rect) ((rect).bottom - (rect).top)
#define SET_RECT(rect, l, t, r, b) \
    {                              \
        (rect).left   = l;         \
        (rect).top    = t;         \
        (rect).right  = r;         \
        (rect).bottom = b;         \
    }

typedef struct _MPO_YPLANE_RECTS
{
    M_RECT MPOSrcRect;
    M_RECT MPODstRect;
    M_RECT MPOClipRect;
    M_RECT MPOSrcClipRect;
} MPO_YPLANE_RECTS, *PMPO_YPLANE_RECTS;
// Matches Kernel Flip Attribute..
typedef struct _MPO_PLANE_ATTRIBUTES
{
    MPO_FLIP_FLAGS    stMPOFlags;
    M_RECT            MPOSrcRect;
    M_RECT            MPODstRect;
    M_RECT            MPOClipRect;
    M_RECT            MPOSrcClipRect;
    PLANE_ORIENTATION eHWOrientation; // HW rotation eg: independent rotation
    MPO_BLEND_VAL     eMPOBlend;
    // Commenting the filters part as of now since it is not in latest Spec but it might come //back, so it can be commented out for now.
    // UINT	uiMPONumFilters;
    // MPO_FILTER_VAL	stFilterVal[MAX_FILTERS];
    MPO_VIDEO_FRAME_FORMAT eMPOVideoFormat;
    union {
        UINT                 uiMPOYCbCrFlags;
        MPO_COLORSPACE_FLAGS stMPOCSFlags;
    };

    // Not in Dx9 Spec
    MPO_STEREO_FORMAT    eMPOStereoFormat;
    BOOL                 bMPOLeftViewFrame0; //? Do we want to keep bool
    BOOL                 bMPOBaseViewFrame0; //? Do we want to keep bool
    MPO_STEREO_FLIP_MODE eMPOStereoFlipMode;
    MPO_STRETCH_QUALITY  eStretchQuality;
    MPO_COLOR_SPACE_TYPE eColorSpace; // ColorSpace passed from OS. BT2020/709 etc.
    // Currently Driver may not use this info.
    UINT             uiDirtyRectCount;
    M_RECT           DIRTYRECTS[MAX_DIRTY_RECTS]; // Making it an array as sending as //pointer is not possible.
    MPO_YPLANE_RECTS stYPlaneRects;
} MPO_PLANE_ATTRIBUTES, *PMPO_PLANE_ATTRIBUTES;

typedef struct _MPO_POST_COMPOSITION
{
    MPO_FLIP_FLAGS    stMPOFlags;
    M_RECT            MPOSrcRect;
    M_RECT            MPODstRect;
    PLANE_ORIENTATION eHWOrientation;
} MPO_POST_COMPOSITION, *PMPO_POST_COMPOSITION;

typedef struct _CHECKMPOSUPPORT_RETURN_INFO
{
    union {
        struct
        {
            UINT uiFailingPlane : 4; // 0 based index of first plane that is //causing the CheckMPOSupport to fail.
            UINT TryAgain : 1;       // Configuration not supported due to hw in //transition condition, this should shortly go away.
        };
        UINT uiValue;
    };
} CHECKMPOSUPPORT_RETURN_INFO, *PCHECKMPOSUPPORT_RETURN_INFO;

typedef struct _MPO_CHECKMPOSUPPORT_OS_PLANE_INFO
{
    UINT                 uiLayerIndex;
    ULONG                ulSourceID;
    HANDLE               hAllocation;
    BOOL                 bEnabled;
    MPO_PLANE_ATTRIBUTES stPlaneAttributes;
} MPO_CHECKMPOSUPPORT_OS_PLANE_INFO, *PMPO_CHECKMPOSUPPORT_OS_PLANE_INFO;

typedef enum _MPO_HDR_METADATA_TYPE
{
    MPO_HDR_METADATA_TYPE_NONE  = 0,
    MPO_HDR_METADATA_TYPE_HDR10 = 1,
} MPO_HDR_METADATA_TYPE;

typedef struct _MPO_HDR_METADATA
{
    MPO_HDR_METADATA_TYPE stType;
    UINT                  uiSize;
    VOID *                pMetaData;
} MPO_HDR_METADATA, *PMPO_HDR_METADATA;

typedef struct _MPO_SETVIDPNSOURCEADDRESS_INPUT_FLAGS
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
} MPO_SETVIDPNSOURCEADDRESS_INPUT_FLAGS;

typedef struct _MPO_SETVIDPNSOURCEADDRESS_OUTPUT_FLAGS
{
    union {
        struct
        {
            UINT PrePresentNeeded : 1;
            UINT Reserved : 31; // 0xFFFFFFFE
        };
        UINT Value;
    };
} MPO_SETVIDPNSOURCEADDRESS_OUTPUT_FLAGS;

typedef struct _MPO_PLANE_SPECIFIC_INPUT_FLAGS
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
} MPO_PLANE_SPECIFIC_INPUT_FLAGS;

typedef struct _MPO_PLANE_SPECIFIC_OUTPUT_FLAGS
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
} MPO_PLANE_SPECIFIC_OUTPUT_FLAGS, *PMPO_PLANE_SPECIFIC_OUTPUT_FLAGS;

typedef struct _MPO_FLIP_PLANE_INFO
{
    ULONG                           ulSourceId;
    UINT                            uiLayerIndex;
    BOOLEAN                         bEnabled;
    BOOLEAN                         bAffected;
    MPO_PLANE_SPECIFIC_INPUT_FLAGS  stInputFlags;
    MPO_PLANE_SPECIFIC_OUTPUT_FLAGS stOutputFlags;
    UINT                            uiAllocationSegment;
    ULONG                           AllocationAddress;
    HANDLE                          hAllocation;
    UINT                            uiMaxImmediateFlipLine;
    UINT                            uiOSLayerIndex;
    ULONGLONG                       ulPresentID;
    MPO_PLANE_ATTRIBUTES            stPlaneAttributes;
} MPO_FLIP_PLANE_INFO, *PMPO_FLIP_PLANE_INFO;

/*************** VBlank Interrupt Handling *********************************/
typedef struct _MPO_VSYNC_INFO
{
    DWORD                dwLayerIndex;
    BOOLEAN              bEnabled;
    LARGE_INTEGER        sttGfxAddress;
    MPO_PLANE_ATTRIBUTES stPlaneAttribute;
} MPO_VSYNC_INFO, *PMPO_VSYNC_INFO;

typedef struct _MPO_NOTIFY_VSYNC_INTERRUPT_DATA
{
    DWORD          dwVidpnTargetID;
    UINT           uiMPOVsyncInfoCount;
    MPO_VSYNC_INFO stMPOVsyncInfo[MAX_PLANES_PER_PIPE];
} MPO_NOTIFY_VSYNC_INTERRUPT_DATA, *PMPO_NOTIFY_VSYNC_INTERRUPT_DATA;

/*+++++++++++++++++++++++++++++++ MPO.h Ends +++++++++++++++++++++++++++++++++++++++++++++++*/
#endif
