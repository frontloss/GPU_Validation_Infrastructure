#/****************************************************************************
** Copyright (c) Intel Corporation (2010).                                  *
**                                                                          *
** INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS    *
** LICENSED ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT,     *
** ASSISTANCE, INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT    *
** PROVIDE ANY UPDATES, ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY     *
** DISCLAIMS ANY WARRANTY OF MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR  *
** ANY PARTICULAR PURPOSE, OR ANY OTHER WARRANTY.  Intel disclaims all      *
** liability, including liability for infringement of any proprietary       *
** rights, relating to use of the code. No license, express or implied, by  *
** estoppel or otherwise, to any intellectual property rights is            *
** granted herein.                                                          *
*****************************************************************************
**
** File Name  : S3D.h
**
** Abstract   : This file contains all the structure definitions related to
**              Stereoscopic 3D
**
**------------------------------------------------------------------------ */

#pragma once
// S3D specific common definitions
#define MAX_S3D_MODES 30

typedef enum S3DSTATE_ENUM
{
    S3DSTATE_2D,         // Display is 2D
    S3DSTATE_3D_Request, // Someone has requested S3D display mode
    S3DSTATE_S3D,        // Display is 3D
    S3DSTATE_2D_Request, // Some has requested 2D display mode
    S3DSTATE_WIN8_S3D
} S3DSTATE;

#define S3D_FORMAT_MASK(eFormat) (1 << eFormat)

typedef enum _S3D_FORMAT
{
    // As per HDMI 1.4 spec
    eS3DFramePacking = 0,
    eS3DFieldAlternative,
    eS3DLineAlternative,
    eS3DSideBySideFull,
    eS3DLDepth,
    eS3DLDepthGraphicsGraphicsDeptch,
    eS3DTopBottom,
    eS3DSideBySideHalfHorizSubSampling,
    eS3DSideBySideHalfQuincunxSubSampling,

    // For 120Hz page flipping
    eS3DPageFlipping,

    eNonS3D = 31 // should be the last entry TODO: is this change needed, mainline 63
} S3D_FORMAT;

// EDID 1.4 indicated s3d format support by display DTD
typedef enum
{                                 // Bits  -- 6 5 0
    eNoStereo,                    // 0 or1 -- 0 0 x Normal display, no stereo. The value of bit 0 is "don't care"
    eFieldSequential_Right   = 2, // 2   -- 0 1 0 Field sequential stereo, right image when stereo sync. = 1
    eFieldSequential_Left    = 4, // 4   -- 1 0 0 Field sequential stereo, left image when stereo sync. = 1
    eInterleavedTwoWay_Right = 3, // 3   -- 0 1 1 2-way interleaved stereo, right image on even lines
    eInterleavedTwoWay_Left  = 5, // 5   -- 1 0 1 2-way interleaved stereo, left image on even lines
    eInterleavedFourWay      = 6, // 6   -- 1 1 0 4-way interleaved stereo
    eSBSInterleaved          = 7  // 7   -- 1 1 1 Side-by-Side interleaved stereo
} DISP_S3DFORMAT;
//
// Surface memory type
//
typedef enum _S3D_SURFACE_MEMORY_TYPE
{
    S3D_SURFACE_MEMORY_LINEAR = 0, // Surface uses linear momory
    S3D_SURFACE_MEMORY_TILED  = 1  // Surface uses tiled memory
} S3D_SURFACE_MEMORY_TYPE;

// S3D frame buffer formats for display
typedef enum _S3D_SOURCE_FORMAT
{
    eS3DSource_2D = 0,
    eS3DSource_SBS_Half,
    eS3DSource_SBS_Full,
    eS3DSource_TB_Half,
    eS3DSource_TB_Full
} S3D_SOURCE_FORMAT;

typedef struct _S3D_MODE_INFO
{
    ULONG      ulResWidth;
    ULONG      ulResHeight;
    ULONG      ulRefreshRate;
    ULONG      ulBlankRegionHeight;
    BOOLEAN    bInterlaced;
    UCHAR      ucBPP;
    int        ePixelFormat;
    S3D_FORMAT eS3DFormat;
} S3D_MODE_INFO, *PS3D_MODE_INFO;

typedef enum
{
    INVALID_DISPLAY = 0,
    S3D_HDMI,
    S3D_EDP,
    S3D_WIDI
} S3D_DISPLAY_TYPE;

typedef enum
{
    S3D_PROPRIETARY = 0,
    S3D_MISC,
    S3D_VSC
} S3D_SIGNAL_TYPE;

typedef enum
{
    eS3DHW_None         = 0,
    eS3DHW_FSAutoMode   = 1,
    eS3DHW_FSManualMode = 2,
    eS3DHW_StackedMode  = 3
} S3D_HW_MODE;

typedef struct _S3D_DATA
{
    ULONG                   ulDisplayUID;    // Target on which S3D is requested
    ULONG                   dwProcessId;     // If S3D is requested/enabled, this field tells which process has requested/enabled S3D
    S3D_MODE_INFO           stS3DMode;       // Requested/applied S3D mode
    S3D_DISPLAY_TYPE        eS3DDisplay;     // Indicates the  S3D display type
    S3D_SURFACE_MEMORY_TYPE eSurfaceMemType; // Surface type information
} S3D_DATA, *PS3D_DATA;

typedef struct _S3D_STATE_DATA
{
    S3DSTATE eS3DState;                 // Current State
    S3D_DATA stS3DData;                 // S3D specific data
    BOOLEAN  bCUIS3DRequest;            // Flag Legacy s3d turned on
    BOOLEAN  bHDMIandDPCloneS3DRequest; // Flag gets set when there is a request for enabling S3D in Clone with HDMI and DP Both
} S3D_STATE_DATA, *PS3D_STATE_DATA;

// Query S3D Details

typedef enum
{
    QUERY_S3D_DETAILS_FROM_VIDPN_SOURCE_ID = 1, // If any target attached on given Src has S3D enabled
    QUERY_S3D_DETAILS_FROM_VIDPN_TARGET_ID = 2, // If given target id has S3D enabled
    QUERY_S3D_STATE_OF_SYSTEM              = 3, // If any target has S3D enabled
    // Win8 Specific
    QUERY_S3D_DETAILS_FROM_VIDPN_SOURCE_MODE = 4
} QUERY_S3D_DETAILS_FROM;

typedef struct _QUERY_S3D_DETAILS_ARGS
{
    QUERY_S3D_DETAILS_FROM eQueryS3DDetailsFrom;
    union {
        ULONG ulVidPnSrcId;
        ULONG ulTargetId;
    } ulQuery;
    S3D_STATE_DATA stS3DStateData;
} QUERY_S3D_DETAILS_ARGS, *PQUERY_S3D_DETAILS_ARGS;

typedef enum
{
    CHANGE_S3D_STATE_APP_CRASH    = 1,
    CHANGE_S3D_STATE_BY_SOURCE_ID = 2,
    CHANGE_S3D_STATE_BY_TARGET_ID = 3
} CHANGE_S3D_STATE_REASON;

typedef struct _CHANGE_S3D_STATE_ARGS
{
    CHANGE_S3D_STATE_REASON eChangeS3DStateReason;
    union {
        ULONG ulVidPnSrcId;
        ULONG ulTargetId;
    } ulChangeS3DStateBy;
    S3DSTATE eNewS3DState;
} CHANGE_S3D_STATE_ARGS, *PCHANGE_S3D_STATE_ARGS;

/*
// Get Sprite details interface
typedef enum _SB_SPRITE_SOURCE_FORMAT_ENUM
{
    eSpriteInvalidFormat = 0,
    eSpriteRGBFormat = 1,
    eSpriteY422Format = 2,
    eSpriteRGBFP16Format = 3,
}SB_SPRITE_SOURCE_FORMAT;

typedef enum _SB_SPRITE_COLORSPACE_ENUM
{
    eSpriteInvalidColorSpace = 0,
    eBT601ColorSpace = 1,
    eBT709ColorSpace = 2
}SB_SPRITE_COLORSPACE_EN;

typedef struct _SB_SPRITE_DETAILS
{
    BOOLEAN                     bIsEnabled;
    SB_SPRITE_COLORSPACE_EN     eColorSpace;
    SB_SPRITE_SOURCE_FORMAT     eSourceFormat;
}SB_SPRITE_DETAILS, *PSB_SPRITE_DETAILS;
//
// Per color chromaticity corrdinat
//
typedef struct _SB_CHROMATICITY_COORDINATE
{
    // Valid values 0-1023
    // Actual floating value = SB returned value / 1024;
    // E.g. For a value of usXScaledBy1024 = 1001110001b (=625), actual X coordinate is 625/1024 (=0.6103515625)
    USHORT usXScaledBy1024;
    USHORT usYScaledBy1024;
}SB_CHROMATICITY_COORDINATE, *PSB_CHROMATICITY_COORDINATE;*/
//
//  Colorspace type
//
/*typedef enum _SB_COLORSPACE_TYPES
{
    eInvalidSpace = -1,
    eSRGB = 0, // default case, use 709 primaries for HD & 601 for SD
    // for future use only
    eYCrCb601, // YCrCb 601 output
    eYCrCb709, // YCrCb 709 output
    eYCrCb601_xvYCC, // extended, primaries are the same as non-xvYCC ones, for use with ILK
    eYCrCb709_xvYCC, // extended, primaries are the same as non-xvYCC ones, for use with ILK
    eYCrCb2020,
    eRGB2020,
    // Custom primaries
    eCustomColorSpace = 0xFF // HP RCR scenario
}SB_COLORSPACE_TYPES, *PSB_COLORSPACE_TYPES;*/
