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
@file DisplaySharedHeader.h
@brief This file contains definitions for display arguments shared between Display and others also within display layers.
It shares definitions between legacy Softbios and new display code as well.
*/

#pragma once

#include "../../Display/Code/DisplayDefs.h"
#ifndef IN_OUT
#define IN_OUT
#endif
#ifndef BOOL
typedef int BOOL;
#endif

#ifndef WORD
typedef unsigned short WORD, *PWORD, *LPWORD;
#endif

#ifndef UINT
typedef unsigned int UINT;
#endif

#ifndef DWORD
typedef ULONG DWORD, *LPDWORD;
#endif
// temp includes TODO: need to refactor
#include "Chipsimc.h"
#include "itvout.h"
#include "iLFP.h"
#include "iCP.h"
#include "iHDCP.h"
#include "VbtArgs.h"
#include "iHDMI.h"
#include "dispComp.h"
#include "Aim3Ex.h"
#include "HAS_SIM.H"
#include "OCA.h"
#include "LHDM/S3D.h"

#include "MPO.h"
#include "iMIPI.h"
// NO OTHER HEADER TO BE INCLUDED

// Mode related
// Increased the MAX_NUM_IDENTITY_TARGET_MODE_PER_SOURCE_MODE value to 32 after testing with Samsung 4K panel which
// has RRs - 23,24,25,29,30,50,60. Also, YUV420 Preferred mode gets added seperately in the mode table.
#define MAX_NUM_IDENTITY_TARGET_MODE_PER_SOURCE_MODE 32
// No interlaced modes allowed for scaling, hence using Identity modes / 2
#define MAX_NUM_SCALED_TARGET_MODE_PER_SOURCE_MODE (MAX_NUM_IDENTITY_TARGET_MODE_PER_SOURCE_MODE / 2)
#define MAX_NUM_TARGET_MODE_PER_SOURCE_MODE (MAX_NUM_IDENTITY_TARGET_MODE_PER_SOURCE_MODE + MAX_NUM_SCALED_TARGET_MODE_PER_SOURCE_MODE)
#define MAX_TARGET_MODES 50
#define DD_MAX_VIEWS 4
#define MAX_EDID_BLOCKS 255 // According to E-EDID Standard doc.
#define EDID_BLOCK_SIZE (128)
#define DDRW_VER 1
// Color related
#define MAX_PALETTE_TABLE_SIZE 1024
#define MAX_OS_PALETTE_TABLE_SIZE 256
#define DD_COLOR_1DLUT_MAX_NUM_SAMPLES 1025
#define DD_COLOR_MATRIX_NUM_COEFFICIENTS 9
#define DD_MIN_CSC -262144 //-4*2^16
#define DD_MAX_CSC 261632  // 3.9921875*2^16
#define DD_COLOR_3D_LUT_DEPTH 17
#define DD_COLOR_3DLUT_NUM_SAMPLES 4913           //(17*17*17) which is 17 samples per RGB channel
#define DD_COLOR_3D_LUT_VALIDATION_THRESHOLD 0.33 // 33 %

#define MAX_PHYSICAL_PIPES_GEN10 3
#define MAX_PHYSICAL_PIPES_GEN11 3
#define MAX_PHYSICAL_PIPES_GEN12 4

#define MAX_POSSIBLE_PIPES DD_MAX(MAX_PHYSICAL_PIPES, 8) // // Hard coding 8 till MAX_VIRTUAL_PIPES is moving to 8 in Yangra implementation
#define MAX_PLANES 21                                    // VGA, 12 Display Planes for CNL, 15 planes for ICL_LP, 20 planes for ICL_HP
#define MAX_SPRITE_PLANES_PER_PIPE (MAX_PLANES_PER_PIPE - 1)
#define MAX_MPO_PLANE_GROUPS 3 // update when more group scenario comes up

#define MAX_CURSOR_PLANES 4
#define GFX_IS_DISPLAYPC(pHwDev) (pHwDev->DisplayPC ? TRUE : FALSE)
#define MAX_TILES_SUPPORTED (MAX_PHYSICAL_PIPES)

BOOLEAN SB_IsTPV(DDU32 TargetID);
BOOLEAN SB_IsLFP(DDU32 TargetID);
BOOLEAN SB_IsDFP(DDU32 TargetID);
BOOLEAN SB_IsCRT(DDU32 TargetID);

// keeping all struct under CUI packing, TODO: remove kernel mode shared structs to different file.
//#pragma pack(push, CUIREGPACK)
//#pragma pack(1)

// Enum added for the updating of plane pixel format
// DDK/OS independent values defined from DD
// Union of all supported source pixel formats of GMCH
// Only non-alpha formats (ones with X) are valid for set mode operation with >8bpp
typedef enum _DD_PIXELFORMAT
{
    // IF ANY NEW FORMAT IS ADDED HERE, PLEASE UPDATE ALL THE BELOW MACORS.
    DD_8BPP_INDEXED = 0,
    DD_B5G6R5X0,
    DD_B8G8R8X8,
    DD_R8G8B8X8,
    DD_B10G10R10X2,
    DD_R10G10B10X2,
    DD_R10G10B10X2_XR_BIAS,
    DD_R16G16B16X16F,
    DD_YUV422,
    DD_YUV444_8,
    DD_YUV444_10,
    DD_NV12YUV420,
    DD_P010YUV420,
    DD_P012YUV420,
    DD_P016YUV420,
    DD_MAX_PIXELFORMAT
    // IF ANY NEW FORMAT IS ADDED HERE, PLEASE UPDATE ALL THE BELOW MACORS.
} DD_PIXELFORMAT;
// Pixel format is being stored in the form of a 32 bit bask in source mode. Therefore we would need updates there if Max pixel format were to increase beyond 32.
// There are other places also where we go by this assumption that 'pixel format <= 32' (such as in DD_SOURCE_MODE_ID), so look for all usages of DD_PIXELFORMAT when making such an
// update.
C_ASSERT(DD_MAX_PIXELFORMAT <= (sizeof(DDU32) * 8));

typedef union _DD_SCALING_SUPPORT {
    struct
    {
        DDU32 Identity : 1;
        DDU32 Centered : 1;
        DDU32 Stretched : 1;
        DDU32 AspectRatioCenteredMax : 1;
        DDU32 Custom : 1;
        DDU32 Reserved : 27;
    };
    DDU32 ScalingSupport;
} DD_SCALING_SUPPORT;

typedef union _DD_SOURCE_MODE_ID {
    DDU32 Value;
    struct
    {
        DD_PIXELFORMAT PixelFormat : 8; // Pixel format range is (0-31) so should not exceed 5 bits.
        DDU32          TgtUniqueIndex : 8;
        DDU32          Index : 16;
    };
} DD_SOURCE_MODE_ID;

typedef struct _DD_SOURCE_MODE_INFO
{
    DD_SOURCE_MODE_ID ModeId;
    DDU32             VisibleScreenX;
    DDU32             VisibleScreenY;
    DDU32             PixelFormatMask;
    DDU32             S3DFormat; // Mask of DD_S3D_FORMAT
    DDU8              NumMappedTgtModes;
    DDU8              MappedTgtModeIndex[MAX_NUM_TARGET_MODE_PER_SOURCE_MODE];
} DD_SOURCE_MODE_INFO;

typedef union _DD_CE_ASPECT_RATIO {
    DDU8 Value;
    struct
    {
        DDU8 Is_Avi_Par_4_3 : 1;
        DDU8 Is_Avi_Par_16_9 : 1;
        DDU8 Is_Avi_Par_64_27 : 1;
        DDU8 ReservedCePar : 5;
    };
} DD_CE_ASPECT_RATIO;

typedef union _DD_SAMPLING_MODE {
    DDU8 Value;
    struct
    {
        DDU8 Rgb : 1;
        DDU8 Yuv420 : 1;
        DDU8 Reserved : 6;
    };
} DD_SAMPLING_MODE;

typedef struct _DD_CE_DATA
{
    union {
        DDU8 Value;
        struct
        {
            DDU8 PixelReplication : 5; // Pixel replication associated with the timing, 0=non-replicated timing
            DDU8 ReservedCeData : 3;   // Reserved for Future use
        };
    };

    DD_SAMPLING_MODE   SamplingMode;                                 // SamplingMode is of format DD_SAMPLING_MODE associated with the timing
    DD_CE_ASPECT_RATIO Par[MAX_PARS_POSSIBLE_WITH_1_VIC];            // AspectRatio corresponding to per VIC stored for same timing
    BOOLEAN            IsNativeFormat[MAX_PARS_POSSIBLE_WITH_1_VIC]; // Native Format bit extracted from SVD/420 block which is per VIC
    DDU8               VicId[MAX_PARS_POSSIBLE_WITH_1_VIC];          // Valid VicID 1 - 127. 0XFF - Vic not defined for mode
    DDU8               VicId4k2k;                                    // 4kx2k mode VicID 1 - 4. Valid only if VicId[0] == 0 (HDMI 4kx2k modes in VSDB block)
} DD_CE_DATA;

typedef enum _MSO_NUMLINKS
{
    NON_SEGMENTED  = 0,
    TWO_SST_LINKS  = 2,
    FOUR_SST_LINKS = 4
} MSO_NUMLINKS;

typedef union _DD_BPC_SUPPORTED {
    DDU16 ColorDepthMask;
    struct
    {
        DDU16 SupportsRGB565Color : 1;
        DDU16 Supports6BitsPerColor : 1;
        DDU16 Supports6BitsLooselyPackedColor : 1;
        DDU16 Supports8BitsPerColor : 1;
        DDU16 Supports10BitsPerColor : 1;
        DDU16 Supports12BitsPerColor : 1;
        DDU16 Supports14BitsPerColor : 1;
        DDU16 Supports16BitsPerColor : 1;
        DDU16 SupportsCompressedBits : 1;
        DDU16 ColordepthReserved : 7;
    };
} DD_BPC_SUPPORTED;

// TIMING_FLAGS used in the TIMING_INFO structure
typedef struct _DD_TIMING_FLAGS
{
    DD_CE_DATA       CeData;
    DDU32            PreferredMode : 1; // 1 - Preferred Mode
    MSO_NUMLINKS     NumLinks : 3;      // NumLinks used for MSO in pipe-Timing programming
    DD_BPC_SUPPORTED SupportedBPCMask;  // Indicates the Supported BPC.This is used for mode enumeration only.
} DD_TIMING_FLAGS;

typedef union _DD_TAREGT_MODE_ID {
    DDU32 Value;
    struct
    {
        DDU32 TgtUniqueIndex : 8;
        DDU32 Index : 24;
    };
} DD_TAREGT_MODE_ID;

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

// MODE_TYPE - Various type of modes
typedef enum _DD_MODE_TYPE
{
    DD_MODE_TYPE_UNKNOWN,
    DD_EDID_MODE, // General monitor specific modes
    DD_NO_EDID_DEFAULT_MODE,
    DD_MEDIA_RR_MODE,
    DD_OS_ADDL_MODE,
    DD_JOINED_MODE,
#if 0
    DD_OEM_CUSTOM_MODE,     // OEM customizable modes
    DD_USER_STANDARD_CUSTOM_MODE, // Custom modes added through CUI's Standard Custom Mode page.
    DD_USER_DETAILED_CUSTOM_MODE // Custom modes added through CUI's Detailed Custom Mode page
#endif // 0
} DD_MODE_TYPE;

typedef enum _DD_SIGNAL_STANDARD
{
    DD_SIGNAL_UNKNOWN = 0,
    DD_VESA_DMT       = 1,
    DD_VESA_GTF       = 2,
    DD_VESA_CVT       = 3,
    DD_CEA_861B,

    // Need to add TV related standards here.
} DD_SIGNAL_STANDARD;

typedef enum _DD_COLOR_RANGE_TYPE
{
    DD_COLOR_RANGE_TYPE_DEFAULT = 0,
    DD_COLOR_RANGE_TYPE_LIMITED = 1,
    DD_COLOR_RANGE_TYPE_FULL    = 2,
    DD_COLOR_RANGE_TYPE_MAX
} DD_COLOR_RANGE_TYPE;

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
    DD_COLOR_ENCODING_LINEAR_GAMMA = 0,
    DD_COLOR_ENCODING_SRGB_GAMMA   = 1,
    DD_COLOR_ENCODING_ST2084       = 2,
    DD_COLOR_ENCODING_HLG          = 3, // HLG - Hybrid Log Gamma
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
    DDU32 CIE_xWhite;
    DDU32 CIE_yWhite;
    DDU32 CIE_xRed;
    DDU32 CIE_yRed;
    DDU32 CIE_xGreen;
    DDU32 CIE_yGreen;
    DDU32 CIE_xBlue;
    DDU32 CIE_yBlue;
} DD_COLOR_CHROMATICITY;

typedef struct _DD_COLOR_OPTICAL_DESC
{
    DDU32 MinDisplayLuminance; // This is in milli nits.
    DDU32 MaxDisplayLuminance; // This is in milli nits.
    DDU32 MaxFALL;             // This is in milli nits.
    DDU32 MaxCLL;              // This is in milli nits.
} DD_COLOR_OPTICAL_DESC;

typedef struct _DD_TONE_MAPPING_PARAMS
{
    DDU32 MinOutputLuminance; // This is in nits in sync with tone mapping algorithm.
    DDU32 MaxOutputLuminance; // This is in nits in sync with tone mapping algorithm.
    DDU32 MinInputLuminance;  // This is in nits in sync with tone mapping algorithm.
    DDU32 MaxInputLuminance;  // This is in nits in sync with tone mapping algorithm.
} DD_TONE_MAPPING_PARAMS;

typedef struct _DD_COLOR_PIXEL_DESC
{
    DD_COLOR_MODEL             ColorModel;
    DD_COLOR_RANGE_TYPE        ColorRangeType;
    DD_COLOR_ENCODING          Encoding;
    DD_COLOR_GAMUT             ColorGamut;
    DD_COLOR_OPTICAL_DESC      OpticalDesc;
    DDU8                       BitsPerColor;
    DD_COLOR_YCBCR_SUBSAMPLING YCbCrSubSampling;
    DD_COLOR_CHROMATICITY      Chromaticity;
} DD_COLOR_PIXEL_DESC;

//  TIMING_INFO data structure (previous in aim3.h)
typedef struct _DD_TIMING_INFO
{
    DDU32              DotClock;      // Pixel clock in Hz
    DDU32              HTotal;        // Horizontal total in pixels
    DDU32              HActive;       // Active in pixels
    DDU32              HBlankStart;   // From start of active in pixels
    DDU32              HBlankEnd;     // From start of active in pixels
    DDU32              HSyncStart;    // From start of active in pixels
    DDU32              HSyncEnd;      // From start of active in pixels
    DDU32              HRefresh;      // Refresh Rate
    DDU32              VTotal;        // Vertical total in lines
    DDU32              VActive;       // Active lines
    DDU32              VBlankStart;   // From start of active lines
    DDU32              VBlankEnd;     // From start of active lines
    DDU32              VSyncStart;    // From start of active lines
    DDU32              VSyncEnd;      // From start of active lines
    DDU32              VRoundedRR;    // Refresh Rate
    BOOLEAN            IsInterlaced;  // 1 = Interlaced Mode
    BOOLEAN            HSyncPolarity; // 1 = H. Sync Polarity is Negative going pulse
    BOOLEAN            VSyncPolarity; // 1 = V. Sync Polarity is Negative going pulse
    DD_TIMING_FLAGS    Flags;         // Timing Flags
    DD_MODE_TYPE       ModeType;
    DD_SIGNAL_STANDARD SignalStandard; // Signal standard
    DDU32              S3DFormat;      // Mask of DD_S3D_FORMAT
    DD_TAREGT_MODE_ID  ModeId;         // Keep it at bottom as upper struct maps to pre defined timings values.
} DD_TIMING_INFO;

typedef enum _DD_VERSION_TYPE
{
    DD_VBIOS_VERSION = 0,
    DD_GOP_VERSION
} DD_VERSION_TYPE;

// Get ROM BIOS info args structure
typedef struct _DD_GETROMBIOSINFO_ARGS
{
    DD_OUT DDU8 BuildNum[32]; // Build number for BIOS
                              // VBIOS version will be sent by BIOS as a number(4 Bytes).
                              // GOP version will be sent by BIOS as a string.
                              // RCR # 1024086
                              // Variable added for Minor Version of VBIOS.
    DD_OUT DDU8 MinorVersion;
    // Variable added for indicating that the minor version number is invalid
    DD_OUT BOOLEAN InvalidMinorVersion;
    DD_OUT DD_VERSION_TYPE VersionType;
} DD_GETROMBIOSINFO_ARGS;

typedef struct _DD_DISPLAY_LIST
{
    DDU32 Displays;
    DDU32 DisplayUID[MAX_POSSIBLE_PIPES];
    DDU32 DeviceConfig; // device configuration (Usefull for dual display)
    DDU8  ConnectorIndex;
} DD_DISPLAY_LIST;

typedef enum _DD_PLATFORM_TYPE
{
    DD_PLATFORM_NONE    = 0x00,
    DD_PLATFORM_DESKTOP = 0x01,
    DD_PLATFORM_MOBILE  = 0x02,
    DD_PLATFORM_TABLET  = 0X03,
    DD_PLATFORM_ALL     = 0xff, // flag used for applying any feature/WA for All platform types
} DD_PLATFORM_TYPE;

typedef enum _DD_PRODUCT_FAMILY
{
    DD_IGFX_UNKNOWN    = 0,
    DD_IGFX_GEMINILAKE = 22,
    DD_IGFX_GLENVIEW,
    DD_IGFX_GOLDWATERLAKE,
    DD_IGFX_CANNONLAKE,
    DD_IGFX_CNX_G,
    DD_IGFX_ICELAKE,
    DD_IGFX_ICELAKE_LP,
    DD_IGFX_TIGERLAKE_LP,
    DD_IGFX_COFFEELAKE,
    DD_IGFX_MAX_PRODUCT,

    DD_IGFX_GENNEXT               = 0x7ffffffe,
    DD_PRODUCT_FAMILY_FORCE_DDU32 = 0x7fffffff
} DD_PRODUCT_FAMILY;
/*
typedef struct PLATFORM_INFO
{
    DD_PRODUCT_FAMILY  ChipsetFamily;
    DD_PLATFORM_TYPE PlatformType;
    DDU32 CpuType; //Driver would fill this variable with one of values in enum CPUTYPE.
    DDU32 GTType;
    DDU32 DevId;
    WCHAR AdpterName[256];//Driver would fill this variable with adapter name.
} PLATFORM_INFO;
*/
typedef struct _DD_SIM_ENV
{
    union {
        struct
        {
            DDU8 SimEnv_Fulsim : 1;    // Bit 0 - Fulsim environment
            DDU8 SimEnv_Fulchip : 1;   // Bit 1 - Fulchip environment
            DDU8 SimEnv_Pipe3d : 1;    // Bit 2 - Pipe3d environment
            DDU8 SimEnv_Pipe2d : 1;    // Bit 3 - Pipe2d environment
            DDU8 SimEnv_PipeMedia : 1; // Bit 4 - PipeMedia environment
            DDU8 SimEnv_Net : 1;       // Bit 5 - Net environment
            DDU8 SimEnv_Xen : 1;       // Bit 6 - Xen environment
        };

        DDU8 Value; // Bitfield value
    };

} DD_SIM_ENV;

typedef enum _DD_ESCAPE_FUNC
{
    DD_ESC_QUERY_MODE_TABLE = 0,
    DD_ESC_DETECT_DEVICE,
    DD_ESC_GET_INVALID_DISP_COMBO,
    DD_ESC_SET_CUSTOM_SCALING,
    DD_ESC_CUSTOM_MODES,
    DD_ESC_POWER_CONSERVATION,
    DD_ESC_S3D,              // TODO
    DD_ESC_COLLAGE,          // TODO
    DD_ESC_GET_CURSOR_SHAPE, // TODO
    DD_ESC_VIRTUAL_DISPLAY,  // TODO
    DD_ESC_GET_SET_VRR,
    DD_ESC_ROTATION_FOR_KVM, // TODO
    DD_ESC_DISP_PWR_MAX,
    // Color Escapes
    DD_ESC_SET_CSC,
    DD_ESC_GET_SET_GAMMA,
    DD_ESC_GET_SET_COLOR_MODEL,
    DD_ESC_SET_3D_LUT,
    DD_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME,

    // Tool Escapes
    DD_ESC_GET_VERSION = 100,
    DD_ESC_AUX_I2C_ACCESS,
    DD_ESC_GET_EDID,
    DD_ESC_QUERY_DISPLAY_DETAILS,

    // This is for development use only
    DD_ESC_EXPERIMENT,
    // Add before this
    DD_ESC_MAX
} DD_ESCAPE_FUNC;

typedef enum _DD_ESCAPE_STATUS
{
    DD_ESCAPE_STATUS_SUCCESS = 0,
    DD_ESCAPE_AUX_ERROR_DEFER,
    DD_ESCAPE_AUX_ERROR_TIMEOUT,
    DD_ESCAPE_AUX_ERROR_INCOMPLETE_WRITE,
    DD_ESCAPE_COLOR_3DLUT_INVALID_PIPE,
    DD_ESCAPE_STATUS_UNKNOWN
} DD_ESCAPE_STATUS;

typedef enum _DD_COLOR_OPERATION
{
    DD_COLOR_OPERATION_GET             = 0, // Get currently applied configuration
    DD_COLOR_OPERATION_SET             = 1, // Set given configuration
    DD_COLOR_OPERATION_RESTORE_DEFAULT = 2, // Restore driver to default settings,
    DD_COLOR_OPERATION_MAX
} DD_COLOR_OPERATION;

// The below structure is used for gamma LUT values.
// Format is 8.24 format. This is doen to avoid Floating point caluclations in driver.
// Gamma cannot be negative hence this is unsigned
// This gives 24 bit precision which is good enough for most of OS like windows(16bpc), Linux(24bpc)
typedef union _DDU8_24 {
    DDU32 Value;
    struct
    {
        DDU32 Fraction : DD_BITFIELD_RANGE(0, 23);
        DDU32 Integer : DD_BITFIELD_RANGE(24, 31);
    };
} DDU8_24;

typedef union _DDU40_24 {
    DDU64 Value;
    struct
    {
        DDU64 Fraction : DD_BITFIELD_RANGE(0, 23);
        DDU64 Integer : DD_BITFIELD_RANGE(24, 63);
    };
} DDU40_24;

// The below structure is used for CSC values.
// Format is 15.16 format. This is done to avoid Floating point caluclations in driver.
// CSC values can be negative hence this is signed
typedef union _DDI15_16 {
    DDS32 Value;
    struct
    {
        DDU32 Fraction : DD_BITFIELD_RANGE(0, 15);
        DDU32 Integer : DD_BITFIELD_RANGE(16, 30);
        DDU32 Sign : DD_BITFIELD_BIT(31);
    };
} DDI15_16;

typedef struct _DD_RGB_DDU8_24 // Similar to D3DDDI_DXGI_RGB
{
    DDU8_24 Red;   // In U8.24 fixed point format
    DDU8_24 Green; // In U8.24 fixed point format
    DDU8_24 Blue;  // In U8.24 fixed point format
} DD_RGB_DDU8_24;

typedef enum _DD_COLOR_CONFIG_FLAGS
{
    DD_COLOR_CONFIG_FLAG_RELATIVE_TRANSFORM = 0,
    DD_COLOR_CONFIG_FLAG_ABSOLUTE_TRANSFORM
} DD_COLOR_CONFIG_FLAGS;

typedef struct _DD_COLOR_PIPE_1DLUT_PARAMS
{
    DD_COLOR_CONFIG_FLAGS Flags;
    DDU32                 NumSamples;
    BOOLEAN               Enable;
    DD_RGB_DDU8_24        LUTData[DD_COLOR_1DLUT_MAX_NUM_SAMPLES];
} DD_COLOR_PIPE_1DLUT_PARAMS;

typedef struct _DD_COLOR_PIPE_MATRIX_PARAMS
{
    DD_COLOR_CONFIG_FLAGS Flags;
    BOOLEAN               Enable;
    DDI15_16              Coefficients[DD_COLOR_MATRIX_NUM_COEFFICIENTS]; // In 8.24 format. Valid when COLOR_CONFIG_FLAG_CUSTOM_MATRIX is used
    DDI15_16              PreOffsets[3];
    DDI15_16              PostOffsets[3];
} DD_COLOR_PIPE_MATRIX_PARAMS;

typedef enum _DD_GAMMA_CLIENT
{
    DD_GAMMA_CLIENT_OS  = 0,
    DD_GAMMA_CLIENT_CUI = 1,
} DD_GAMMA_CLIENT;

// This is used for get/set post matrix gamma functionality. Caller must get before set.
// CUI structure is same as Driver Structure here. No conversion is required.
// OS structure needs to be converted to Driver structure before calling HAL.

typedef struct _DD_COLOR_1DLUT_CONFIG
{
    DDU32                      Size;     // Size of this structure
    DDU32                      TargetId; // TagetId when communicating with user mode. Pipe id inside KMD.
    DDU32                      NumPipes;
    DDU32                      PipeId[MAX_TILES_SUPPORTED];
    DDU32                      Reserved[2]; // For future use
    DD_COLOR_OPERATION         Operation;
    DD_COLOR_PIPE_1DLUT_PARAMS PipeLUTParams;
} DD_COLOR_1DLUT_CONFIG;

typedef struct _DD_COLOR_1DLUT_CONFIG_ARGS
{
    DD_COLOR_1DLUT_CONFIG ColorParams;
    DD_GAMMA_CLIENT       Client;
} DD_COLOR_1DLUT_CONFIG_ARGS;

// This is used for relative/absolute matrix or gamut mapping. Caller must get before set.
typedef struct _DD_COLOR_MATRIX_CONFIG
{
    DDU32                       Size;     // Size of this structure
    DDU32                       TargetId; // TagetId when communicating with user mode.
    DDU32                       NumPipes;
    DDU32                       PipeId[MAX_TILES_SUPPORTED]; // Pipe id inside KMD.
    DDU32                       Reserved[2];                 // For future use
    DD_COLOR_OPERATION          Operation;
    DD_COLOR_PIPE_MATRIX_PARAMS PipeMatrix;
} DD_COLOR_MATRIX_CONFIG;

typedef struct _DD_COLOR_PIPE_OUTPUT_CONFIG
{
    DDU32                 Size;     // Size of this structure
    DDU32                 TargetId; // TagetId when communicating with user mode.
    DDU32                 NumPipes;
    DDU32                 PipeId[MAX_TILES_SUPPORTED]; // Pipe id is used only by KMD.
    DD_COLOR_CONFIG_FLAGS Flags;
    DDU32                 Enabled;
    DD_COLOR_OPERATION    Operation;
    DD_COLOR_PIXEL_DESC   PipeOutColorFormat; // CUI specific structure is needed.
} DD_COLOR_PIPE_OUTPUT_CONFIG;

// Value to be used in info-frame
typedef enum _DD_EOTF_TYPE_INFOFRAME
{
    DD_EOTF_INFORFRAME_TYPE_TRADITIONAL_GAMMA_SDR = 0x0,
    DD_EOTF_INFORFRAME_TYPE_TRADITIONAL_GAMMA_HDR = 0x1,
    DD_EOTF_INFORFRAME_TYPE_ST2084                = 0x2, // This is to be used for HDMI HDR.
    DD_EOTF_INFORFRAME_TYPE_FUTURE_EOTF           = 0x3
} DD_EOTF_TYPE_INFOFRAME;

typedef enum _DD_COLOR_PRIMARY_INDEX
{
    DD_COLOR_PRIMARY_GREEN_INDEX = 0,
    DD_COLOR_PRIMARY_BLUE_INDEX  = 1,
    DD_COLOR_PRIMARY_RED_INDEX   = 2
} DD_COLOR_PRIMARY_INDEX;

typedef struct _DD_HDR_STATIC_METADATA
{
    DDU16 EOTF;
    DDU16 DisplayPrimariesX[3];
    DDU16 DisplayPrimariesY[3];
    DDU16 WhitePointX;
    DDU16 WhitePointY;
    DDU32 MaxDisplayMasteringLuminance; // This is in milli nits.    //TODO Review: remove Display. Add milliNits to variable.
    DDU32 MinDisplayMasteringLuminance; // This is in milli nits.
    DDU32 MaxCLL;                       // This is in milli nits.
    DDU32 MaxFALL;                      // Maximum Frame Average Light Level. This is in milli nits.
} DD_HDR_STATIC_METADATA;

typedef enum _DD_MPO_HDR_METADATA_TYPE
{
    DD_MPO_HDR_METADATA_TYPE_NONE       = 0,
    DD_MPO_HDR_METADATA_TYPE_HDR10      = 1,
    DD_MPO_HDR_METADATA_TYPE_DEFAULT    = 2,
    DD_MPO_HDR_METADATA_TYPE_UMD_ESCAPE = 3 // Not handled currently.
} DD_MPO_HDR_METADATA_TYPE;

typedef struct _DD_MPO_HDR_METADATA
{
    DD_MPO_HDR_METADATA_TYPE Type;
    DD_HDR_STATIC_METADATA   HdrStaticMetaData;
} DD_MPO_HDR_METADATA;

// Panel Capability Flags
//
typedef struct _DD_PANEL_COLOR_CAPABILITY_FLAGS
{
    DDU32 YCbCr4 : 1;
    DDU32 YCbCr420 : 1;
    DDU32 YCbCr422 : 1;
    DDU32 FROutput : 1;
    DDU32 LROutput : 1;
    DDU32 Bpc10Output : 1;
    DDU32 Bpc12Output : 1;
    DDU32 EOTFG22 : 1;
    DDU32 EOTF2084 : 1;
    DDU32 EOTFHLG : 1;
    DDU32 Gamut709 : 1;
    DDU32 GamutDCIP3 : 1;
    DDU32 GamutBT2020 : 1;
    DDU32 GamutCustom : 1; // Chromacities of the panel is significantly different from known gamuts
    DDU32 YCbCrMatrixBT2020 : 1;
    DDU32 YCbCrMatrixBT709 : 1;
    DDU32 YCnCrMatrixBT601 : 1;
} DD_PANEL_COLOR_CAPABILITY_FLAGS;

typedef enum DD_COLOR_CHANNEL
{
    DD_COLOR_CHANNEL_RED   = 1,
    DD_COLOR_CHANNEL_GREEN = 2,
    DD_COLOR_CHANNEL_BLUE  = 4,
    DD_COLOR_CHANNEL_ALL   = (DD_COLOR_CHANNEL_RED | DD_COLOR_CHANNEL_GREEN | DD_COLOR_CHANNEL_BLUE)
} DD_COLOR_CHANNEL;

// 3d lut Color related
typedef union _DD_RGB_1010102 {
    DDU32 Value;
    struct
    {
        DDU32 Red : DD_BITFIELD_RANGE(0, 9);
        DDU32 Green : DD_BITFIELD_RANGE(10, 19);
        DDU32 Blue : DD_BITFIELD_RANGE(20, 29);
        DDU32 Reserved : DD_BITFIELD_RANGE(30, 31);
    };
} DD_RGB_1010102;

typedef enum _DD_COLOR_3DLUT_STATUS
{
    DD_COLOR_3DLUT_SUCCESS,
    DD_COLOR_3DLUT_INVALID_PIPE,
    DD_COLOR_3DLUT_INVALID_DATA
} DD_COLOR_3DLUT_STATUS;

// This is used for pipe 3D LUT functionality.
typedef struct _DD_COLOR_3DLUT_CONFIG
{
    DDU32                 Size;     // Size of this structure
    DDU32                 TargetId; // TagetId when communicating with user mode.
    DDU32                 NumPipes;
    DDU32                 PipeId[MAX_TILES_SUPPORTED]; // Pipe id is used only by KMD.
    BOOLEAN               Enable;
    DD_COLOR_CONFIG_FLAGS Flags;
    DD_COLOR_OPERATION    Operation;
    DD_COLOR_3DLUT_STATUS Status;
    DD_RGB_1010102        LutData[DD_COLOR_3DLUT_NUM_SAMPLES];
} DD_COLOR_3DLUT_CONFIG;
typedef enum _INTERRUPT_UNION_VALUE
{
    INTCRT                    = 0x1,
    RESERVED_TV               = 0x2,
    SDVOB                     = 0x4,
    SDVOC                     = 0x8,
    INTDP_HDMIA               = 0x10,
    INTDP_HDMIB               = 0x20,
    INTDP_HDMIC               = 0x40,
    INTDP_HDMID               = 0x80,
    INTDP_HDMIA_SP            = 0x100,
    INTDP_HDMIB_SP            = 0x200,
    INTDP_HDMIC_SP            = 0x400,
    INTDP_HDMID_SP            = 0x800,
    REN_GEY_SWCMDCOMPLETE     = 0x1000,
    REN_GEY_EVLFREQCHNG       = 0x2000,
    REN_GEY_AVGBSYTHRESHOLD   = 0x4000,
    REN_GEY_CNTBSYTHRESHOLD   = 0x8000,
    REN_GEY_UPEVLINTERVAL     = 0x10000,
    REN_GEY_DOWNEVLINTERVAL   = 0x20000,
    REN_GEY_CNTRLDISABLESTATE = 0x40000,
    DBG_INTERRUPT             = 0x80000,
    PIPECTRLNOTIFY            = 0x100000,
    RENDERUSERINTERRUPT       = 0x200000,
    RNDRMMIOSYNCFLUSHSTATUS   = 0x400000,
    RNDRWATCHDOGCNTREXCD      = 0x800000,
    RNDRASCNTXSWITCH          = 0x1000000,
    RNDRPGFAULT               = 0x2000000,
    VIDEOUSERINTERRUPT        = 0x4000000,
    VIDEODECPIPELINECNTREXCD  = 0x8000000,
    VIDEOMIFLUSHDWNTFY        = 0x10000000,
    VIDEOMMIOSYNCFLUSH        = 0x20000000,
    VIDEOASCNTXSWITCH         = 0x40000000,
    VIDEOPAGEFAULT            = 0x80000000
} INTERRUPT_UNION_VALUE;

typedef enum _INTERRUPT_UNION_VALUE_1
{
    LBPC_PIPEA               = 0x1,
    LBPC_PIPEB               = 0x2,
    DPST_HIST                = 0x4,
    DPST_PHASEIN             = 0x8,
    PCUMBEVENT               = 0x10,
    PCRNDRFREQDOWNRC6TIMEOUT = 0x20,
    PC_RPFUPTHRESHOLD        = 0x40,
    PC_RPFDOWNTHRESHOLD      = 0x80,
    BLITTERASCNTXSWITCH      = 0x100,
    BLITTERMIFLUSHDWNTFY     = 0x200,
    BLITTERMMIOSYNCFLUSH     = 0x400,
    BLITTERMIUSER            = 0x800,
    BLITTERPGFAULT           = 0x1000,
    VSYNCPIPEA               = 0x2000,
    VSYNCPIPEB               = 0x4000,
    VBLANKPIPEA              = 0x8000,
    VBLANKPIPEB              = 0x10000,
    GSESYSTEMLEVEL           = 0x20000,
    VBLANKTPV                = 0x40000,
    ASLEINTERRUPT            = 0x80000,
    ALLFIRSTLEVEL            = 0x100000,
    SPRITEPLANEAFLIPDONE     = 0x200000,
    SPRITEPLANEBFLIPDONE     = 0x400000,
    VSYNCPIPEC               = 0x800000,
    VBLANKPIPEC              = 0x1000000,
    SPRITEPLANECFLIPDONE     = 0x2000000,
    AUDIOHDCPREQA            = 0x4000000,
    AUDIOHDCPREQB            = 0x8000000,
    AUDIOHDCPREQC            = 0x10000000,
    AUDIOHDCPREQ             = 0x20000000,
    PERFMONBUFFHALFFULL      = 0x40000000,
    SPRITEPLANEDFLIPDONE     = 0x80000000,
    SPRITEPLANEEFLIPDONE     = 0xF,
    SPRITEPLANEFFLIPDONE     = 0xF0,
} INTERRUPT_UNION_VALUE_1;

typedef enum _INTERRUPT_UNION_VALUE_2
{
    FIFO_UNDERRUN_PIPEA       = 0x1,
    CRCERROR_PIPEA            = 0x2,
    CRCDONE_PIPEA             = 0x4,
    FIFO_UNDERRUN_PIPEB       = 0x8,
    CRCERROR_PIPEB            = 0x10,
    CRCDONE_PIPEB             = 0x20,
    FIFO_UNDERRUN_PIPEC       = 0x40,
    CRCERROR_PIPEC            = 0x80,
    CRCDONE_PIPEC             = 0x100,
    VEUSERINTERRUPT           = 0x200,
    VEMMIOSYNCFLUSH           = 0x400,
    VECMDPARSERMASTERERR      = 0x800,
    VEMIFLUSHDWNOTIFY         = 0x1000,
    RENDERPARITYERR           = 0x2000,
    VIDEOPAVPATTACK           = 0x4000,
    VIDEOUSERINT2             = 0x8000,
    VIDEODECPIPELINECNTREXCD2 = 0x10000,
    VIDEOMIFLUSHDWNTFY2       = 0x20000,
    VIDEOMMIOSYNCFLUSH2       = 0x40000,
    VIDEOASCNTXSWITCH2        = 0x80000,
    VIDEOPAGEFAULT2           = 0x100000,
    VIDEOPAVPATTACK2          = 0x200000,
    GUCSHIMERROR              = 0x400000,
    GUCDMAINTERROR            = 0x800000,
    GUCDMADONE                = 0x1000000,
    GUCDOORBELLRANG           = 0x2000000,
    GUCIOMMUSENTMSGGUC        = 0x4000000,
    GUCSEMAPHORESIGNALED      = 0x8000000,
    GUCDISPLAYEVENTRECIEVED   = 0x10000000,
    GUCEXECUTIONERROR         = 0x20000000,
    GUCINTERRUPTTOHOST        = 0x40000000,
    CSTRINVALIDTILEDETECTION  = 0x80000000,
} INTERRUPT_UNION_VALUE_2;

typedef enum _INTERRUPT_UNION_VALUE_3
{
    VECSCONTEXTSWITCHINT              = 0x1,
    VECSWAITONSEMAPHORE               = 0x2,
    WDBOXINTERRUPT                    = 0x4,
    DPST_HIST_PIPEB                   = 0x8,
    DPST_PHASEINT_PIPEB               = 0x10,
    DPST_HIST_PIPEC                   = 0x20,
    DPST_PHASEINT_PIPEC               = 0x40,
    PIPEA_PLANE1_FLIP_DONE_INT        = 0x80,
    PIPEA_PLANE2_FLIP_DONE_INT        = 0x100,
    PIPEA_PLANE3_FLIP_DONE_INT        = 0x200,
    PIPEB_PLANE1_FLIP_DONE_INT        = 0x400,
    PIPEB_PLANE2_FLIP_DONE_INT        = 0x800,
    PIPEB_PLANE3_FLIP_DONE_INT        = 0x1000,
    PIPEC_PLANE1_FLIP_DONE_INT        = 0x2000,
    PIPEC_PLANE2_FLIP_DONE_INT        = 0x4000,
    PIPEC_PLANE3_FLIP_DONE_INT        = 0x8000,
    PIPEA_PLANE1_FLIP_QUEUE_EMPTY_INT = 0x10000,
    PIPEA_PLANE2_FLIP_QUEUE_EMPTY_INT = 0x20000,
    PIPEA_PLANE3_FLIP_QUEUE_EMPTY_INT = 0x40000,
    PIPEB_PLANE1_FLIP_QUEUE_EMPTY_INT = 0x80000,
    PIPEB_PLANE2_FLIP_QUEUE_EMPTY_INT = 0x100000,
    PIPEB_PLANE3_FLIP_QUEUE_EMPTY_INT = 0x200000,
    PIPEC_PLANE1_FLIP_QUEUE_EMPTY_INT = 0x400000,
    PIPEC_PLANE2_FLIP_QUEUE_EMPTY_INT = 0x800000,
    PIPEC_PLANE3_FLIP_QUEUE_EMPTY_INT = 0x1000000,
    DEMISCSVMWAITDESCCOMPLETE         = 0x2000000,
    DEMISCSVMVTDFAULT                 = 0x4000000,
    DEMISCSVMPRQEVENT                 = 0x8000000,
    PIPEA_PLANE4_FLIP_DONE_INT        = 0x10000000, // BXT
    PIPEB_PLANE4_FLIP_DONE_INT        = 0x20000000, // BXT
    DEMISC_GTC_COMBINED_EVENT         = 0x40000000,
    VECSWATCHDOGCNTREXCD              = 0x80000000,
} INTERRUPT_UNION_VALUE_3;

typedef enum _INTERRUPT_UNION_VALUE_4
{
    // assigning values to match definition in INTERRUPT_ARGS
    MIPIA                             = 0x1,
    MIPIC                             = 0x2,
    LPE_PIPEA                         = 0x4,
    LPE_PIPEB                         = 0x8,
    ISP                               = 0x10,
    VED_BLOCK                         = 0x20,
    VED_POWER                         = 0x40,
    PIPEA_PLANE4_FLIP_QUEUE_EMPTY_INT = 0x80,  // BXT
    PIPEB_PLANE4_FLIP_QUEUE_EMPTY_INT = 0x100, // BXT
    LPE_PIPEC                         = 0x200,
    CORE_TO_UNCORE_TRAP               = 0x400,
    WDBOX_END_OF_FRAME_INTERRUPT      = 0X800,
    INTDP_HDMIE                       = 0x1000,
    INTDP_HDMIE_SP                    = 0x2000,

    RENDERTDLRETRYINTR = 0x4000, // KBL

    PINNING_CONTEXT_SWITCH        = 0x8000,
    PINNING_USER_INTR             = 0x10000,
    DEMISC_WD_COMBINED_INTERRUPT  = 0x20000,
    PIPEA_UNDERRUN                = 0x40000,
    PIPEB_UNDERRUN                = 0x80000,
    PIPEC_UNDERRUN                = 0x100000,
    PIPEC_PLANE4_FLIP_DONE_INT    = 0x200000,
    INVALID_GTT_PAGE_TABLE_ENTRY  = 0x400000,
    INVALID_PAGE_TABLE_ENTRY_DATA = 0x800000,
    VSYNCPIPED                    = 0x1000000,
    VBLANKPIPED                   = 0x2000000,
    INTDP_HDMIF                   = 0x4000000,
    INTDP_HDMIF_SP                = 0x8000000,
    WDBOX2INTERRUPT               = 0x10000000,
    WDBOX2_END_OF_FRAME_INTERRUPT = 0x20000000,
    DEMISC_WD2_COMBINED_INTERRUPT = 0x40000000,
} INTERRUPT_UNION_VALUE_4;

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
    INTDP_HDMIB_SCDC_INTERRUPT    = 0x8000,
    INTDP_HDMIC_SCDC_INTERRUPT    = 0x10000,
    INTDP_HDMID_SCDC_INTERRUPT    = 0x20000,
    INTDP_HDMIE_SCDC_INTERRUPT    = 0x40000,
    INTDP_HDMIF_SCDC_INTERRUPT    = 0x80000,
    PIPEA_PLANE5_FLIP_DONE_INT    = 0x100000,
    PIPEA_PLANE6_FLIP_DONE_INT    = 0x200000,
    PIPEA_PLANE7_FLIP_DONE_INT    = 0x400000,
    PIPEB_PLANE5_FLIP_DONE_INT    = 0x800000,
    PIPEB_PLANE6_FLIP_DONE_INT    = 0x1000000,
    PIPEB_PLANE7_FLIP_DONE_INT    = 0x2000000,
    PIPEC_PLANE5_FLIP_DONE_INT    = 0x4000000,
    PIPEC_PLANE6_FLIP_DONE_INT    = 0x8000000,
    PIPEC_PLANE7_FLIP_DONE_INT    = 0x10000000,
    PIPED_PLANE5_FLIP_DONE_INT    = 0x20000000, // PIPED from Gen11.5
    PIPED_PLANE6_FLIP_DONE_INT    = 0x40000000,
    PIPED_PLANE7_FLIP_DONE_INT    = 0x80000000,
} INTERRUPT_UNION_VALUE_5;

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
    PIPED_PLANE1_FLIP_DONE_INT    = 0x1000,
    PIPED_PLANE2_FLIP_DONE_INT    = 0x2000,
    PIPED_PLANE3_FLIP_DONE_INT    = 0x4000,
    PIPED_PLANE4_FLIP_DONE_INT    = 0x8000,
    PIPED_PLANE1_GTT_FAULT_STATUS = 0x10000,
    PIPED_PLANE2_GTT_FAULT_STATUS = 0x20000,
    PIPED_PLANE3_GTT_FAULT_STATUS = 0x40000,
    PIPED_PLANE4_GTT_FAULT_STATUS = 0x80000,
    PIPED_CURSOR_GTT_FAULT_STATUS = 0x100000,
    PIPED_DPST_HIST               = 0x200000,
    PIPED_CRCERROR                = 0x400000,
    PIPED_CRCDONE                 = 0x800000,
    PIPED_UNDERRUN                = 0x1000000,
    AUDIOHDCPREQD                 = 0x2000000,
    INTDP_HDMIA_SCDC_INTERRUPT    = 0x4000000, // Gen11.5
    PIPEA_VRRDOUBLEBUFFERUPDATE   = 0x8000000,
    PIPEB_VRRDOUBLEBUFFERUPDATE   = 0x10000000,
    PIPEC_VRRDOUBLEBUFFERUPDATE   = 0x20000000,
    PIPED_VRRDOUBLEBUFFERUPDATE   = 0x40000000,
} INTERRUPT_UNION_VALUE_6;

typedef enum _INTERRUPT_UNION_VALUE_7
{
    // assigning values to match definition in INTERRUPT_ARGS
    PIPEA_SCANLINE_EVENT = 0x1,
    PIPEB_SCANLINE_EVENT = 0x2,
    PIPEC_SCANLINE_EVENT = 0x4,
    PIPED_SCANLINE_EVENT = 0x8,
    // assigning values to match definition in INTERRUPT_ARGS
    KVMR_REQUESTDISPLAY_INTERRUPT = 0x10,
    KVMR_RELEASEDISPLAY_INTERRUPT = 0x20,
    INTDP_HDMIG                   = 0x40,
    INTDP_HDMIG_SP                = 0x80,
    INTDP_HDMIH                   = 0x100,
    INTDP_HDMIH_SP                = 0x200,
    INTDP_HDMII                   = 0x400,
    INTDP_HDMII_SP                = 0x800,
    INTDP_HDMIG_SCDC_INTERRUPT    = 0x1000,
    INTDP_HDMIH_SCDC_INTERRUPT    = 0x2000,
    INTDP_HDMII_SCDC_INTERRUPT    = 0x4000
} INTERRUPT_UNION_VALUE_7;

// Data Structure for Interrupt operations
typedef enum _INTERRUPT_OPERATION
{
    ENABLE_INTERRUPT        = 1,
    DISABLE_INTERRUPT       = 2,
    MASK_INTERRUPT          = 3,
    UNMASK_INTERRUPT        = 4,
    GET_DISABLED_INTERRUPTS = 5 // Flag To Detect Disabled Interrupts also.
} INTERRUPT_OPERATION;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// NOTE: Any change in the interrrupt args structure below has to be reflected in the enum definitions above.
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Interrupt Args structure
typedef struct _SB_INTERRUPT_ARGS
{
    INTERRUPT_OPERATION eOperation;    // Data structure for interrupt operations
    DDU32               ulPrivateData; // Private Interrupt Data. This will not be used in ILK and GT since enabling/disabling of all interrupts has become much simpler..

    DDU32 PlatformUsesGen11InterruptArchitecture : 1; // Let Event handler code know that all non-display engines are handled by new Selector methods
    DDU32 SelectorInterruptsOccurred : 1; // New for Gen11+  ::  This bit means one of the hierarchical interrupts (has to use selector register) has occurred and needs to be
                                          // handled by GEN11+ handler
    DDU32 LegacyInterruptsOccurred : 1;   // New for Gen11+  ::  This bit means use the IntArgs below for handling the interrupts

    IN BOOLEAN HierarchicalInterruptService : 1; // This bit means request for Hirearchial Interrupt services

    IN DDU32 ulEngineClass;  // Can re-use ulValue in union
    IN DDU32 ulEngineIntrpt; // Can re-use ulValue1 in union

    union {
        DDU32 ulValue; // temp code for SB compilation
        DDU32 Value;
        struct
        {
            // 1. Hot Plug Interrupts Definitions - Starts Here

            DDU32 bIntegratedCRTInterrupt : 1;  // Bit 0
            DDU32 ulReservedBit : 1;            // Bit 1
            DDU32 bInterruptReserved1 : 1;      // Bit 2
            DDU32 bInterruptReserved2 : 1;      // Bit 3 //From Gen6 onwards,no need to register for this event as sDVO on Port C is disabled..
            DDU32 bIntDP_HDMIAInterrupt : 1;    // Bit 4  //New Introduction from ILK onwards
            DDU32 bIntDP_HDMIBInterrupt : 1;    // Bit 5
            DDU32 bIntDP_HDMICInterrupt : 1;    // Bit 6
            DDU32 bIntDP_HDMIDInterrupt : 1;    // Bit 7
            DDU32 bIntDP_HDMIA_SPInterrupt : 1; // Bit 8 //New Introduction from ILK onwards
            DDU32 bIntDP_HDMIB_SPInterrupt : 1; // Bit 9
            DDU32 bIntDP_HDMIC_SPInterrupt : 1; // Bit 10
            DDU32 bIntDP_HDMID_SPInterrupt : 1; // Bit 11

            // 1. Hot Plug Interrupts Definitions - Ends Here

            // 2. Render Geyserville Interrupts Definitions - Starts Here

            // Render Geyserville Interrupts common till ILK Platform
            DDU32 bRen_Gey_SoftwareCommandCompleteInterrupt : 1;  // bit 12 // Render GeyserVille Interrupt
            DDU32 bRen_Gey_EvaluatedFrequencyChangeInterrupt : 1; // bit 13 // Render GeyserVille Interrupt

            // New Render Geyserville Interrupts exists only in ILK
            DDU32 bRen_Gey_AvgBusyThreshold : 1;        // bit 14 // Render GeyserVille Interrupt
            DDU32 bRen_Gey_ContinuousBusyThreshold : 1; // bit 15 // Render GeyserVille Interrupt

            // Render Geyserville Common between ILK and GT
            DDU32 bRen_Gey_UpEvaluationIntervalInterrupt : 1;   // bit 16 // Render GeyserVille Interrupt
            DDU32 bRen_Gey_DownEvaluationIntervalInterrupt : 1; // bit 17 // Render GeyserVille Interrupt

            // Render Geyserville Introduced from GT
            DDU32 bRen_Gey_Controller_Disable_StateInterrupt : 1; // bit 18 // Render GeyserVille Interrupt

            // 2. Render Geyserville Interrupts Definitions - Ends Here

            // 3. Basic Render Interrupt Definitions - Starts Here

            DDU32 bDebugInterrupt : 1;             // Bit 19 Gen4 Onwards
            DDU32 bPipeControlNotifyInterrupt : 1; // Bit 20 Gen4 Onwards
            DDU32 bRenderUserInterrupt : 1;        // Bit 21 Render Cmd UI
            DDU32 bRenderMMIOSyncFlushStatus : 1;  // Bit 22
            DDU32 bRenderWatchDogCounterExcd : 1;  // Bit 23 //ILK Onwards
            DDU32 bRenderASContextSwitch : 1;      // Bit 24 //ILK Onwards
            DDU32 bRenderPageFault : 1;            // Bit 25 //ILK Onwards

            // 3. Basic Render Interrupt Definitions - Ends Here

            // 4. Media/Video Interrupt Definitions - Starts Here
            DDU32 bVideoUserInterrupt : 1;         // Bit 26 Gen4 Onwards
            DDU32 bVideoDecPipelineCntrExceed : 1; // Bit 27 Gen4 Onwards..Same as Video Command Streamer WatchDog Counter Exceeded in GT
                                                   // Following are valid from GT
            DDU32 bVideoMIFlush_DWNotify : 1;      // Bit 28
            DDU32 bVideoMMIOSyncFlushStatus : 1;   // Bit 29
            DDU32 bVideoASContextSwitch : 1;       // Bit 30
            DDU32 bVideoPageFault : 1;             // Bit 31

            // 4. Media/Video Interrupt Definitions - Ends Here
        };
    };

    union {
        DDU32 ulValue1;
        DDU32 Value1;
        struct
        {
            // 5. Remaining Power Conservation Interrupt Starts here
            DDU32 bLBPC_PipeAInterrupt : 1;   // Bit 0 - crestline and after. Doesnt exist from ILK Onwards
            DDU32 bLBPC_PipeBInterrupt : 1;   // Bit 1 - crestline and after. Doesnt exist from ILK Onwards
            DDU32 bDPST_HistInterrupt : 1;    // Bit 2 - crestline and after
            DDU32 bDPST_PhaseInInterrupt : 1; // Bit 3 - crestline and after

            // Valid from GT Onwards
            DDU32 bPCUDriverMBEvent : 1;                     // Bit 4
            DDU32 bPCRenderFreqDownwardDuringRC6Timeout : 1; // Bit 5
            DDU32 bPC_RPUpThresholdIntr : 1;                 // Bit 6
            DDU32 bPC_RPDownThresholdIntr : 1;               // Bit 7

            // 5. Remaining Power Conservation Interrupt Ends here

            // 6. Blitter Interrupts from GT Onwards Starts here

            DDU32 bBlitterASContextSwitch : 1;     // Bit 8
            DDU32 bBlitterMIFlush_DWNotify : 1;    // Bit 9
            DDU32 bBlitterMMIOSyncFlushStatus : 1; // Bit 10
            DDU32 bBlitterMI_User_Interrupt : 1;   // Bit 11
            DDU32 bBlitterPageFault : 1;           // Bit 12
                                                   // 6. Blitter Interrupts from GT Onwards Ends here

            // 7. Misc Interrupts Category Starts here
            DDU32 bVSync_PipeAInterrupt : 1;    // Bit 13 //Not Required
            DDU32 bVSync_PipeBInterrupt : 1;    // Bit 14 //Not Required
            DDU32 bVBlank_PipeAInterrupt : 1;   // Bit 15
            DDU32 bVBlank_PipeBInterrupt : 1;   // Bit 16
            DDU32 bGSESystemLevel : 1;          // Bit 17  Valid from ILK Replacement for ASLE Interrupt
            DDU32 bVblankTPV : 1;               // BIT 18 //Used for TPV Vblank Interrupt
            DDU32 bASLEInterrupt : 1;           // Bit 19  Need to remove Once MP Cleans up the ASLE INterrupt Stuff
            DDU32 bAllFirstLevelInterrupts : 1; // BIT 20 //Used for Enabling/Disabling of Interrupts..

            // 7. Misc Interrupts Category Ends here

            // 8. New added Interrupts
            DDU32 bSpritePlaneAFlipDoneInterrupt : 1; // BIT 21 //Used for Enabling/Disabling of Sprite Plane A Flip Done Interrupt..
            DDU32 bSpritePlaneBFlipDoneInterrupt : 1; // BIT 22 //Used for Enabling/Disabling of Sprite Plane B Flip Done Interrupt..

            DDU32 bVSync_PipeCInterrupt : 1;          // BIT 23
            DDU32 bVBlank_PipeCInterrupt : 1;         // BIT 24
            DDU32 bSpritePlaneCFlipDoneInterrupt : 1; // BIT 25

            DDU32 bAudioHDCPRequestInterruptA : 1; // BIT 26 //Audio HDCP request for transcoder A
            DDU32 bAudioHDCPRequestInterruptB : 1; // BIT 27 //Audio HDCP request for transcoder B
            DDU32 bAudioHDCPRequestInterruptC : 1; // BIT 28 //Audio HDCP request for transcoder C
            DDU32 bAudioHDCPRequestInterrupt : 1;  // BIT 29 //Audio HDCP request for pre ilk platforms

            DDU32 bPerfMonBufferHalfFullInterrupt : 1; // BIT 30

            DDU32 ulReserved_Bit31 : 1; // Bit 31
        };
    };

    union {
        DDU32 ulValue2;
        DDU32 Value2;
        struct
        {
            // This sections contains error/debug status bits
            DDU32 bFIFOUnderrun_PipeAInterrupt : 1; // bit 0
            DDU32 bCRC_Error_PipeAInterrupt : 1;    // bit 1
            DDU32 bCRC_Done_PipeAInterrupt : 1;     // bit 2

            DDU32 bFIFOUnderrun_PipeBInterrupt : 1; // bit 3
            DDU32 bCRC_Error_PipeBInterrupt : 1;    // bit 4
            DDU32 bCRC_Done_PipeBInterrupt : 1;     // bit 5

            DDU32 bFIFOUnderrun_PipeCInterrupt : 1; // bit 6
            DDU32 bCRC_Error_PipeCInterrupt : 1;    // bit 7
            DDU32 bCRC_Done_PipeCInterrupt : 1;     // bit 8

            // VE (Video Enhancement) Interrupt Definitions - Starts Here - Valid from Gen7_5 (HSW+) onward
            DDU32 bVEUserInterrupt : 1;        // bit 9
            DDU32 bVEMMIOSyncFlushStatus : 1;  // bit 10
            DDU32 bVECmdParserMasterError : 1; // bit 11
            DDU32 bVEMIFlush_DWNotify : 1;     // bit 12
                                               // VE (Video Enhancement) Interrupt Definitions - Ends Here

            // other interrupt bits that don't fit into the previous dwords
            DDU32 bRenderParityError : 1; // Bit 13 Gen7 Onwards

            DDU32 bVideoPavpUnsolicitedAttack : 1; // Bit 14 Gen7 Onwards

            // Below are valid from BDW
            DDU32 bVideoUserInterrupt2 : 1;         // Bit 15
            DDU32 bVideoDecPipelineCntrExceed2 : 1; // Bit 16
            DDU32 bVideoMIFlush_DWNotify2 : 1;      // Bit 17
            DDU32 bVideoMMIOSyncFlushStatus2 : 1;   // Bit 18
            DDU32 bVideoASContextSwitch2 : 1;       // Bit 19
            DDU32 bVideoPageFault2 : 1;             // Bit 20
            DDU32 bVideoPavpUnsolicitedAttack2 : 1; // Bit 21

            DDU32 bGuCSHIMError : 1;            // bit 22
            DDU32 bGuCDMAINTError : 1;          // bit 23
            DDU32 bGuCDMADone : 1;              // bit 24
            DDU32 bGuCDoorBellRang : 1;         // bit 25
            DDU32 bGuCIOMMUSentMsgtoGuc : 1;    // bit 26
            DDU32 bGuCSemaphoreSignaled : 1;    // bit 27
            DDU32 bGuCDisplayEventRecieved : 1; // bit 28
            DDU32 bGuCExecutionError : 1;       // bit 29
            DDU32 bGuCInterruptToHost : 1;      // bit 30

            DDU32 bCSTRInvalidTileDetection : 1; // bits 31
        };
    };

    union {
        DDU32 ulValue3;
        DDU32 Value3;
        struct
        {
            // This sections contains VEC/WiDi interrupts
            DDU32 bVECSContextSwitchInterrupt : 1; // bit 0
            DDU32 bVECSWaitOnSemaphore : 1;        // bit 1
            DDU32 bWDBoxInterrupt : 1;             // bit 2
            DDU32 bDPST_HistInterruptPipeB : 1;    // bit 3
            DDU32 bDPST_PhaseInInterruptPipeB : 1; // bit 4
            DDU32 bDPST_HistInterruptPipeC : 1;    // bit 5
            DDU32 bDPST_PhaseInInterruptPipeC : 1; // bit 6

            DDU32 bPipeA_Plane1FlipDoneInterrupt : 1; // bit 7
            DDU32 bPipeA_Plane2FlipDoneInterrupt : 1; // bit 8
            DDU32 bPipeA_Plane3FlipDoneInterrupt : 1; // bit 9

            DDU32 bPipeB_Plane1FlipDoneInterrupt : 1; // bit 10
            DDU32 bPipeB_Plane2FlipDoneInterrupt : 1; // bit 11
            DDU32 bPipeB_Plane3FlipDoneInterrupt : 1; // bit 12

            DDU32 bPipeC_Plane1FlipDoneInterrupt : 1; // bit 13
            DDU32 bPipeC_Plane2FlipDoneInterrupt : 1; // bit 14
            DDU32 bPipeC_Plane3FlipDoneInterrupt : 1; // bit 15

            DDU32 bPipeA_Plane1FlipQueueEmptyInterrupt : 1; // bit 16
            DDU32 bPipeA_Plane2FlipQueueEmptyInterrupt : 1; // bit 17
            DDU32 bPipeA_Plane3FlipQueueEmptyInterrupt : 1; // bit 18

            DDU32 bPipeB_Plane1FlipQueueEmptyInterrupt : 1; // bit 19
            DDU32 bPipeB_Plane2FlipQueueEmptyInterrupt : 1; // bit 20
            DDU32 bPipeB_Plane3FlipQueueEmptyInterrupt : 1; // bit 21

            DDU32 bPipeC_Plane1FlipQueueEmptyInterrupt : 1; // bit 22
            DDU32 bPipeC_Plane2FlipQueueEmptyInterrupt : 1; // bit 23
            DDU32 bPipeC_Plane3FlipQueueEmptyInterrupt : 1; // bit 24

            DDU32 bDEMiscSVMWaitDescriptorCompleted : 1; // bit 25
            DDU32 bDEMiscSVMVTDFault : 1;                // bit 26
            DDU32 bDEMiscSVMPRQEvent : 1;                // bit 27

            DDU32 bPipeA_Plane4FlipDoneInterrupt : 1; // bit 28
            DDU32 bPipeB_Plane4FlipDoneInterrupt : 1; // bit 29
            DDU32 bPSR2GTCLockLoss : 1;               // bit 30
            DDU32 bVECSWatchDogCounterExcd : 1;       // bit 31
        };
    };
    union {
        DDU32 ulValue4;
        DDU32 Value4;
        struct
        {
            DDU32 bMIPIAInterrupt : 1;    // bit 0
            DDU32 bMIPICInterrupt : 1;    // bit 1
            DDU32 bLPEPipeAInterrupt : 1; // bit 2
            DDU32 bLPEPipeBInterrupt : 1; // bit 3

            DDU32 bISPInterrupt : 1;                        // bit 4
            DDU32 bVEDBlockInterrupt : 1;                   // bit 5
            DDU32 bVEDPowerInterrupt : 1;                   // bit 6
            DDU32 bPipeA_Plane4FlipQueueEmptyInterrupt : 1; // bit 7

            DDU32 bPipeB_Plane4FlipQueueEmptyInterrupt : 1; // bit 8
            DDU32 bLPEPipeCInterrupt : 1;                   // bit 9
            DDU32 bGTPMCoreToUncoreTrapInterrupt : 1;       // bit 10
            DDU32 bWDBoxEndofFrameInterrupt : 1;            // bit 11 corresponds to WDBOX_END_OF_FRAME_INTERRUPT = 0X800, in INTERRUPT_UNION_VALUE_4

            DDU32 bIntDP_HDMIEInterrupt : 1;       // Bit 12// skl ddi - e hot plug interrupt
            DDU32 bIntDP_HDMIE_SPInterrupt : 1;    // Bit 13
            DDU32 bRenderTDLRetryInterrupt : 1;    // bit 14
            DDU32 bPinningContextSwitch : 1;       // Bit 15
            DDU32 bPinningUserInterrupt : 1;       // Bit 16
            DDU32 bDEMisc_WDCombinedInterrupt : 1; // bit 17 corresponds to DEMISC_WD_COMBINED_INTERRUPT  = 0x20000, in INTERRUPT_UNION_VALUE_4

            DDU32 bPipeA_Underrun : 1;                // bit 18
            DDU32 bPipeB_Underrun : 1;                // bit 19
            DDU32 bPipeC_Underrun : 1;                // bit 20
            DDU32 bPipeC_Plane4FlipDoneInterrupt : 1; // bit 21
            DDU32 bInvalidGTTPageTableEntry : 1;      // bit 22
            DDU32 bInvalidPageTableEntryData : 1;     // bit 23
            DDU32 bVSync_PipeDInterrupt : 1;          // BIT 24
            DDU32 bVBlank_PipeDInterrupt : 1;         // BIT 25
            DDU32 bIntDP_HDMIFInterrupt : 1;          // Bit 26// ddi - f hot plug interrupt
            DDU32 bIntDP_HDMIF_SPInterrupt : 1;       // Bit 27
            DDU32 bWDBox2Interrupt : 1;               // bit 28
            DDU32 bWDBox2EndofFrameInterrupt : 1;     // bit 29
            DDU32 bDEMisc_WD2CombinedInterrupt : 1;   // bit 30
            DDU32 ulReserved_Bits31_ulValue4 : 1;     // bit 31
        };
    };
    union {
        DDU32 ulValue5;
        DDU32 Value5;
        struct
        {
            DDU32 PipeA_Plane1GTTFaultStatus : 1; // bit 0
            DDU32 PipeA_Plane2GTTFaultStatus : 1; // bit 1
            DDU32 PipeA_Plane3GTTFaultStatus : 1; // bit 2
            DDU32 PipeA_Plane4GTTFaultStatus : 1; // bit 3
            DDU32 PipeA_CursorGTTFaultStatus : 1; // bit 4

            DDU32 PipeB_Plane1GTTFaultStatus : 1; // bit 5
            DDU32 PipeB_Plane2GTTFaultStatus : 1; // bit 6
            DDU32 PipeB_Plane3GTTFaultStatus : 1; // bit 7
            DDU32 PipeB_Plane4GTTFaultStatus : 1; // bit 8
            DDU32 PipeB_CursorGTTFaultStatus : 1; // bit 9

            DDU32 PipeC_Plane1GTTFaultStatus : 1; // bit 10
            DDU32 PipeC_Plane2GTTFaultStatus : 1; // bit 11
            DDU32 PipeC_Plane3GTTFaultStatus : 1; // bit 12
            DDU32 PipeC_Plane4GTTFaultStatus : 1; // bit 13
            DDU32 PipeC_CursorGTTFaultStatus : 1; // bit 14

            DDU32 IntDP_HDMIB_SCDCInterrupt : 1; // bit 15
            DDU32 IntDP_HDMIC_SCDCInterrupt : 1; // bit 16
            DDU32 IntDP_HDMID_SCDCInterrupt : 1; // bit 17
            DDU32 IntDP_HDMIE_SCDCInterrupt : 1; // bit 18
            DDU32 IntDP_HDMIF_SCDCInterrupt : 1; // bit 19

            DDU32 bPipeA_Plane5FlipDoneInterrupt : 1; // bit 20
            DDU32 bPipeA_Plane6FlipDoneInterrupt : 1; // bit 21
            DDU32 bPipeA_Plane7FlipDoneInterrupt : 1; // bit 22
            DDU32 bPipeB_Plane5FlipDoneInterrupt : 1; // bit 23
            DDU32 bPipeB_Plane6FlipDoneInterrupt : 1; // bit 24
            DDU32 bPipeB_Plane7FlipDoneInterrupt : 1; // bit 25
            DDU32 bPipeC_Plane5FlipDoneInterrupt : 1; // bit 26
            DDU32 bPipeC_Plane6FlipDoneInterrupt : 1; // bit 27
            DDU32 bPipeC_Plane7FlipDoneInterrupt : 1; // bit 28
            DDU32 bPipeD_Plane5FlipDoneInterrupt : 1; // bit 29
            DDU32 bPipeD_Plane6FlipDoneInterrupt : 1; // bit 30
            DDU32 bPipeD_Plane7FlipDoneInterrupt : 1; // bit 31
        };
    };
    union {
        DDU32 ulValue6;
        DDU32 Value6;
        struct
        {
            DDU32 PipeA_Plane5GTTFaultStatus : 1;     // bit 0
            DDU32 PipeA_Plane6GTTFaultStatus : 1;     // bit 1
            DDU32 PipeA_Plane7GTTFaultStatus : 1;     // bit 2
            DDU32 PipeB_Plane5GTTFaultStatus : 1;     // bit 3
            DDU32 PipeB_Plane6GTTFaultStatus : 1;     // bit 4
            DDU32 PipeB_Plane7GTTFaultStatus : 1;     // bit 5
            DDU32 PipeC_Plane5GTTFaultStatus : 1;     // bit 6
            DDU32 PipeC_Plane6GTTFaultStatus : 1;     // bit 7
            DDU32 PipeC_Plane7GTTFaultStatus : 1;     // bit 8
            DDU32 PipeD_Plane5GTTFaultStatus : 1;     // bit 9
            DDU32 PipeD_Plane6GTTFaultStatus : 1;     // bit 10
            DDU32 PipeD_Plane7GTTFaultStatus : 1;     // bit 11
            DDU32 bPipeD_Plane1FlipDoneInterrupt : 1; // bit 12
            DDU32 bPipeD_Plane2FlipDoneInterrupt : 1; // bit 13
            DDU32 bPipeD_Plane3FlipDoneInterrupt : 1; // bit 14
            DDU32 bPipeD_Plane4FlipDoneInterrupt : 1; // bit 15
            DDU32 PipeD_Plane1GTTFaultStatus : 1;     // bit 16
            DDU32 PipeD_Plane2GTTFaultStatus : 1;     // bit 17
            DDU32 PipeD_Plane3GTTFaultStatus : 1;     // bit 18
            DDU32 PipeD_Plane4GTTFaultStatus : 1;     // bit 19
            DDU32 PipeD_CursorGTTFaultStatus : 1;     // bit 20
            DDU32 PipeD_DPST_HistInterrupt : 1;       // bit 21
            DDU32 bCRC_Error_PipeDInterrupt : 1;      // bit 22
            DDU32 bCRC_Done_PipeDInterrupt : 1;       // bit 23
            DDU32 bPipeD_Underrun : 1;                // bit 24
            DDU32 bAudioHDCPRequestInterruptD : 1;    // bit 25
            DDU32 IntDP_HDMIA_SCDCInterrupt : 1;      // bit 26
            DDU32 PIPEA_VRRDoubleBufferUpdate : 1;    // bit 27
            DDU32 PIPEB_VRRDoubleBufferUpdate : 1;    // bit 28
            DDU32 PIPEC_VRRDoubleBufferUpdate : 1;    // bit 29
            DDU32 PIPED_VRRDoubleBufferUpdate : 1;    // bit 30
            DDU32 ulReserved_Bits31_ulValue6 : 1;     // bits 31
        };
    };
    union {
        DDU32 ulValue7;
        DDU32 Value7;
        struct
        {
            DDU32 bPipeA_ScanLineEvent : 1;          // bit 0
            DDU32 bPipeB_ScanLineEvent : 1;          // bit 1
            DDU32 bPipeC_ScanLineEvent : 1;          // bit 2
            DDU32 bPipeD_ScanLineEvent : 1;          // bit 3
            DDU32 bKVMR_RequestDisplayInterrupt : 1; // bit 4
            DDU32 bKVMR_ReleaseDisplayInterrupt : 1; // bit 5
            DDU32 bIntDP_HDMIGInterrupt : 1;         // Bit 6// ddi - g hot plug interrupt
            DDU32 bIntDP_HDMIG_SPInterrupt : 1;      // Bit 7
            DDU32 bIntDP_HDMIHInterrupt : 1;         // Bit 8// ddi - h hot plug interrupt
            DDU32 bIntDP_HDMIH_SPInterrupt : 1;      // Bit 9
            DDU32 bIntDP_HDMIIInterrupt : 1;         // Bit 10// ddi - i hot plug interrupt
            DDU32 bIntDP_HDMII_SPInterrupt : 1;      // Bit 11
            DDU32 IntDP_HDMIG_SCDCInterrupt : 1;     // Bit 12
            DDU32 IntDP_HDMIH_SCDCInterrupt : 1;     // Bit 13
            DDU32 IntDP_HDMII_SCDCInterrupt : 1;     // Bit 14
            DDU32 ulReserved_Bits_ulValue7 : 17;     // bits 15 to 31
        };
    };
} SB_INTERRUPT_ARGS, *PSB_INTERRUPT_ARGS;

// TODO: C_ASSERT(sizeof(SB_INTERRUPT_ARGS) == (15 * sizeof(DDU32)));  // Ensure no one added too many bits in one of the DDU32 fields

//
// Surface memory type
//
typedef enum _SURFACE_MEMORY_TYPE
{
    SURFACE_MEMORY_INVALID        = 0,
    SURFACE_MEMORY_LINEAR         = 1, // Surface uses linear memory
    SURFACE_MEMORY_TILED          = 2, // Surface uses tiled memory
    SURFACE_MEMORY_X_TILED        = SURFACE_MEMORY_TILED,
    SURFACE_MEMORY_Y_LEGACY_TILED = 4, // Surface uses Legacy Y tiled memory (Gen9+)
    SURFACE_MEMORY_Y_F_TILED      = 8, // Surface uses Y F tiled memory
} SURFACE_MEMORY_TYPE;

typedef enum _PLANE_ORIENTATION
{
    ORIENTATION_DEFAULT = 0,                   // Default value
    ORIENTATION_0       = ORIENTATION_DEFAULT, // 0 degree
    ORIENTATION_90      = 1,                   // 90 degree, supported Gen9 onwards
    ORIENTATION_180     = 2,                   // 180 degree
    ORIENTATION_270     = 3,                   // 270 degree, supported Gen9 onwards
    ORIENTATION_MAX     = 4,
} PLANE_ORIENTATION;

// Cursor position
typedef struct _CURSOR_POS
{
    // X and Y position for Cursor
    DDU16 Xpos;
    DDU16 YPos;
} CURSOR_POS;

// Cursor ID
typedef enum _CURSOR_ID
{
    CURSOR_INVALID = 0,
    CURSOR_A       = 1,
    CURSOR_B       = 2,
    CURSOR_C       = 3,
    CURSOR_D       = 4,
    CURSOR_TPV
} CURSOR_ID;

typedef enum _IGFX_ENCRYPTION_TYPE
{
    /**no ecnryption */
    NO_ENCRYPTION = 0,
    /**PAVP encrypted*/
    PAVP_PLANE_ENCRYPTED = 1,
    /**Isolated decode*/
    ISOLATED_DECODE = 2,
} IGFX_ENCRYPTION_TYPE;

typedef enum _PIPE_ORIENTATION
{
    PIPE_ORIENTATION_UNDEFINED = 0,
    PIPE_ORIENTATION_0,
    PIPE_ORIENTATION_90,
    PIPE_ORIENTATION_180,
    PIPE_ORIENTATION_270,
} PIPE_ORIENTATION;

typedef enum _DISPLAY_PIPE_ID
{
    DISPLAY_PIPE_A = 0,
    DISPLAY_PIPE_B,
    DISPLAY_PIPE_C,
    DISPLAY_PIPE_D
} DISPLAY_PIPE_ID,
*PDISPLAY_PIPE_ID;

// Enum added for the updating of plane pixel format
// DDK/OS independent values defined from SB
// Union of all supported source pixel formats of GMCH
// Order is LSB-->MSB (as in bspec)
// Only non-alpha formats (ones with X) are valid for set mode operation with >8bpp
typedef enum _SB_PIXELFORMAT
{
    SB_UNINITIALIZED = 0, // use default pixel format in this case for setmode (e.g. XP might always set this)
    // SB_8BPP_INDEXED for 8bpp, SB_B5G6R5X0 for 16bpp, SB_B8G8R8X8 for 32bpp
    // Keep in the order of increasing BPP
    // Update min, max below if any other format is added
    SB_8BPP_INDEXED, // for 8bpp
    // Keep in the order of increasing BPP
    // Update min, max below if any other format is added
    SB_B5G6R5X0, // for 16bpp
    // Keep in the order of increasing BPP
    // Update min, max below if any other format is added
    SB_B8G8R8X8, // for 32bpp (default)
    SB_B8G8R8A8,
    SB_R8G8B8X8,
    SB_R8G8B8A8,
    SB_R10G10B10X2, // for 32bpp 10bpc
    SB_R10G10B10A2, // for 32bpp 10bpc
    SB_B10G10R10X2, // for 32bpp 10bpc
    SB_B10G10R10A2, // for 32bpp 10bpc

    SB_R10G10B10A2_XR_BIAS, // for 32bpp 10bpc, XR BIAS format (used by Win7)
    // Keep in the order of increasing BPP
    // Update min, max below if any other format is added
    SB_R16G16B16X16F, // for 64bpp, 16bit floating
    SB_R16G16B16A16F, // for 64bpp, 16bit floating
    // Keep in the order of increasing BPP
    // Update min, max below if any other format is added
    // Adding formats used ONLY for MPO, adding at the last to reduce impact
    // Macros below will be updated for them only where it is really required
    SB_MAX_PIXELFORMAT, // Last one - just for internal bitmask usage

    SB_NV12YUV420,
    SB_YUV422,
    SB_P010YUV420,
    SB_P012YUV420,
    SB_P016YUV420,
    SB_YUV444_10,

    SB_YUV422_10,
    SB_YUV422_12,
    SB_YUV422_16,
    SB_YUV444_8,
    SB_YUV444_12,
    SB_YUV444_16,
    SB_MAXALL_PIXELFORMAT,
} SB_PIXELFORMAT,
*PSB_PIXELFORMAT;

// SB watermark argument data structures used by PC
//

typedef enum _SB_WATERMARK_RETURN_CODE
{
    SB_WM_SUCCESSFUL = 0,
    SB_WM_ERROR_UNKNOWN,
    SB_WM_ERROR_EXCEEDED_FIFO,
    SB_WM_ERROR_UNUSED
} SB_WATERMARK_RETURN_CODE;

// GEN6 Watermark Data structure
typedef enum _WATERMARK_TYPE_GEN6
{
    WATERMARK_MAIN = 0,
    WATERMARK_LP1,
    WATERMARK_LP2,
    WATERMARK_LP3,

    WATERMARK_LP_MAX
} WATERMARK_TYPE_GEN6;

// Gen9 Specific Definitions
//
#define GEN9_NUM_WM_PER_PLANE 8

// Gen9 Watermark Data Struct
//
typedef struct _SB_GEN9_LP_WM_DATA
{
    OUT BOOLEAN bWmEnable;    // OUT: Whether the WM is enabled on this pipe
    OUT BOOLEAN bIgnoreLines; // OUT: Ignore lines and use blocks
    OUT DDU16 ulWmLines;      // OUT: Num lines for this watermark
    OUT DDU16 ulWmBlocks;     // OUT: Num blocks for this watermark
} SB_GEN9_LP_WM_DATA;

// Gen9 Plane Parameters
//
typedef struct _SB_GEN9_WATERMARK_ARGS
{
    IN OUT UCHAR ucPipe;                                          // TODO: remove this interface
    IN OUT UCHAR ucPlaneType;                                     // possible values: cursor or PLANE_OVERLAY. check for Z-order for PLANE_OVERLAY,
    IN OUT UCHAR ucZOrder;                                        // The Zorder for the plane
    IN OUT SB_GEN9_LP_WM_DATA stPlaneLpWm[GEN9_NUM_WM_PER_PLANE]; // Block of LP WM information
    OUT SB_WATERMARK_RETURN_CODE eReturnCode;                     // OUT: Error code
} SB_GEN9_WATERMARK_ARGS;

typedef struct _SB_GEN11_WATERMARK_ARGS
{
    IN OUT BOOLEAN CxSRStatus;
    OUT SB_WATERMARK_RETURN_CODE eReturnCode; // OUT: Error code
} SB_GEN11_WATERMARK_ARGS;

typedef struct _SB_GEN6_WATERMARK_ARGS
{
    IN WATERMARK_TYPE_GEN6 WatermarkType;    // Main/LP1/LP2/LP3
    IN PLANE_TYPE eEnabledPlanes[PLANE_ALL]; // Array of enabled or to be enabled plane
    IN UCHAR ucMaxEnabledPlanes;
    IN DDU32 ulDependencyStatus; // Bit0 – FBC enabled

    OUT DDU32 ulDisplayWatermark;    // Main/LP1/LP2/LP3
    OUT DDU32 ulCursorWatermark;     // Main/LP1/LP2/LP3
    OUT DDU32 ulSpriteWatermark;     // Main/LP1/LP2/LP3
    OUT DDU32 ulFBCWatermark;        // LP1/LP2/LP3
    OUT DDU32 ulLatency_MemoryLevel; // LP1/LP2/LP3

    // Error codeSB_WATERMARK_ARGS
    OUT SB_WATERMARK_RETURN_CODE eReturnCode;
} SB_GEN6_WATERMARK_ARGS, *PSB_GEN6_WATERMARK_ARGS;

// GEN4/GEN5 watermark data structure
typedef struct _SB_GEN4_WATERMARK_ARGS
{
    IN PLANE_TYPE ePlaneType;
    IN BOOLEAN bIsHPLLDisabled;

    IN DDU32 ulPipeIndex;     // SB will use this to get current dotclock & HTotal
    IN DDU32 ulBytesPerPixel; // Caller has to fill the properly
    IN DDU32 ulSurfaceWidth;  // Surface/source width of ePlaneType
    IN PLANE_TYPE eEnabledPlanes[PLANE_ALL];
    IN UCHAR ucMaxEnabledPlanes;
    OUT DDU32 ulWatermark;    // return value
                              // Corresponding SR_FBC    or SR_FBC_HPLL value for
                              // display plane, else 0.
    OUT DDU32 ulFBCWatermark; // return value

    // Error code
    OUT SB_WATERMARK_RETURN_CODE eReturnCode;
} SB_GEN4_WATERMARK_ARGS, *PSB_GEN4_WATERMARK_ARGS;

typedef struct _SB_WATERMARK_ARGS
{
    union {
        SB_GEN4_WATERMARK_ARGS  Gen4Watermarks;
        SB_GEN6_WATERMARK_ARGS  Gen6Watermarks;
        SB_GEN9_WATERMARK_ARGS  Gen9Watermarks;
        SB_GEN11_WATERMARK_ARGS Gen11Watermarks;
    };
} SB_WATERMARK_ARGS, *PSB_WATERMARK_ARGS;

typedef union _SOURCE_MODE_FLAGS {
    DDU32 ulFlags;
    struct
    {
        unsigned bS3DMode : 1;            // Bit Indicating whether the given mode is S3D
        unsigned bCollage : 1;            // Bit indicating if given mode is Collage
        unsigned bHorCollage : 1;         // bit indicating if given mode is horizontal Collage
        unsigned bVerCollage : 1;         // bit indicating if given mode id vertical Collage
        unsigned bRGBColorSeparation : 1; // bit indicating color separation support for the given mode
        unsigned bTiledMode : 1;          // bit indicating tiled display mode is applicable
        unsigned bPipeGangedMode : 1;     // bit indicating pipe ganged display mode is applicable
        unsigned bReserved : 25;          // Bits 0:24, Reserved
    };
} SOURCE_MODE_FLAGS, *PSOURCE_MODE_FLAGS;

// DDK/OS independent values defined from SB
typedef enum _SB_COLOR_BASIS
{
    SB_CB_UNINITIALIZED = 0,
    SB_CB_INTENSITY     = 1,
    SB_CB_SRGB          = 2,
    SB_CB_SCRGB         = 3,
    SB_CB_YCBCR         = 4,
    SB_CB_YPBPR         = 5,
} SB_COLOR_BASIS,
*PSB_COLOR_BASIS;

// DDK/OS independent values defined from SB
typedef enum _SB_PIXEL_VALUE_ACCESS_MODE
{
    SB_PVAM_UNINITIALIZED   = 0,
    SB_PVAM_DIRECT          = 1,
    SB_PVAM_PRESETPALETTE   = 2,
    SB_PVAM_SETTABLEPALETTE = 3,
} SB_PIXEL_VALUE_ACCESS_MODE,
*PPIXEL_VALUE_ACCESS_MODE;

typedef struct _BPP_INFO
{
    DDU32 ulBPP;
    // The DDU32 below for pixel format is a Multi-Select Bit Mask. The individual values are defined as:
    // SB_PIXELFORMAT
    DDU32                      ulSBPixelFormatMask;
    SB_COLOR_BASIS             eSBColorBasis;
    SB_PIXEL_VALUE_ACCESS_MODE eSBPvam;
    DDU32                      ScreenStride;
} BPP_INFO, *PBPP_INFO;
#define MAX_COLOR_BPP 4 // 8, 16, 32 & 64 bpps (doesn't include 4bpp)

typedef enum _MONITOR_MODE_SUPPORT
{
    MONITOR_SUPPORT_UNKNOWN = 0,
    MONITOR_SUPPORTED_MODE,  // Mode supported by the monitor
    MONITOR_UNSUPPORTED_MODE // Mode unsupported by monitor and supported by adapter only
} MONITOR_MODE_SUPPORT,
*PMONITOR_MODE_SUPPORT;

// Enum for scan line order
typedef enum _SCAN_LINE_ORDER
{
    SCANORDER_UNKNOWN = 0,
    PROGRESSIVEORDER  = 1,
    INTERLACEDORDER   = 2
} SCAN_LINE_ORDER;

// Enum for various signal standards
typedef enum _SIGNAL_STANDARD
{
    SIGNAL_UNKNOWN_SIGNAL = 0,
    VESA_DMT_SIGNAL       = 1,
    VESA_GTF_SIGNAL       = 2,
    VESA_CVT_SIGNAL       = 3
    // Need to add TV related standards here.
} SIGNAL_STANDARD;

//////////////////////////////////////////////
// MODE_TYPE - Various type of modes
//////////////////////////////////////////////
typedef enum _MODE_TYPE
{
    // VGA_STD_MODE,         // Standard VGA modes
    VESA_STD_DMTS_MODE,        // VESA DMTS timing modes
    VESA_GTF_MODE,             // VESA GTF timing modes
    OEM_CUSTOM_MODE,           // OEM customizable modes
    EDID_STD_MODE,             // EDID Standard timing modes
    EDID_DTD_MODE,             // General monitor specific modes
                               // PREFERRED_DTD_MODE,   // Monitor preferred timing mode
                               // BASIC_STATIC_MODE,    // VESA DMTS modes in basic static mode list
                               // LOW_RES_MODE,         // Supported low resolution modes
    EDID_CE_SHORT_DESC_MODE,   // CE xtn Short Video Descriptor mode
    EDID_HDTV_UNDER_SCAN_MODE, // HDTV Under Scan mode
    EDID_VTB_CVT_MODE,         // VTB Ext CVT Timing mode
    FAKE_INTERLACED_MODE,      // Fake Interlaced Mode, will be used for HDMI displays.
    ENCODER_MODE,              // This to indicate that these	modes are added by the Encoder during addmodes.
    USER_STANDARD_CUSTOM_MODE, // Custom modes added through CUI's Standard Custom Mode page.
    USER_DETAILED_CUSTOM_MODE, // Custom modes added through CUI's Detailed Custom Mode page
    MEDIA_SRC_MODE,            // This is to indicate that these modes are added through inf for Media Scaling
    MEDIA_REFRESH_RATE_MODE,   // Mode added for getting media refresh rates like 59.94Hz with modified vtotal
    OS_ADDED_MODE,
    OS_INF_OVR_ADDED_MODE,
    VESA_CVT_MODE,
    S3D_MODE,
    EDID_4K_2K_MODE,
    SEAMLESS_MEDIA_RR_MODE,
    DOWNSCALED_MODE,
    COLOR_SEPERATED_MODE,
    TILED_MODE,
    COG_MODE,
    PIPE_GANGED_MODE
} MODE_TYPE;

// Data Structure used by modes manager.
typedef struct _MONITOR_MODE_INFO
{
    DDU32                ulVSyncNumerator;   // Vsync numerator value
    DDU32                ulVSyncDenominator; // Vsync denominator value
    DDU32                ulVRefresh;         // Refresh Rate in integer format
    DDU32                ulHSyncNumerator;   // Hsync numerator value
    DDU32                ulHSyncDenominator; // Hsync denominator value
    DDU32                ulPixelRate;        // pixel rate value
    DDU32                ulHTotal;           // Htotal value
    DDU32                ulHActive;          // Hactive value
    DDU32                ulHBlankStart;      // From start of active in pixels
    DDU32                ulHBlankEnd;        // From start of active in pixels
    DDU32                ulHSyncStart;       // From start of active in pixels
    DDU32                ulHSyncEnd;         // From start of active in pixels
    DDU32                ulVTotal;           // Vtotal value
    DDU32                ulVActive;          // VActive value
    DDU32                ulVBlankStart;      // From start of active lines
    DDU32                ulVBlankEnd;        // From start of active lines
    DDU32                ulVSyncStart;       // From start of active lines
    DDU32                ulVSyncEnd;         // From start of active lines
    BOOLEAN              bPreferred;         // flag indicating mode preferred or not
    SCAN_LINE_ORDER      eScanLineOrder;     // scan line order (progressive or interlaced)
    SIGNAL_STANDARD      eSignalStandard;    // signal standard
    BOOLEAN              bHSyncPolarity;
    BOOLEAN              bVSyncPolarity;
    MONITOR_MODE_SUPPORT eMonitorModeSupport;
    MODE_TYPE            eModeType;
    DDU32                ulVSyncFreqDivider;
    BOOLEAN              bRGBColorSeparated;
    DDU32                ulSupportedBPCForTiming;
    UCHAR                ucWireFormat;
    UCHAR                ucColorFormat;
    DDU32                ulSupportedBpcForY420Mode;
} MONITOR_MODE_INFO, *PMONITOR_MODE_INFO;

typedef struct _SOURCE_MODE_INFO
{
    DDU32                VisScreenWidth;
    DDU32                VisScreenHeight;
    BPP_INFO             stBPPInfo[MAX_COLOR_BPP];
    MONITOR_MODE_SUPPORT eMonitorModeSupport;
    SOURCE_MODE_FLAGS    stSrcModeFlags;
} SOURCE_MODE_INFO, *PSOURCE_MODE_INFO; // legacy path

// Enum added for distinguishing various display types
#ifndef _COMMON_PPA
typedef enum
{
    // DONOT change the order of type definitions
    // Add new types just before MAX_DISPLAY_TYPES & increment value of MAX_DISPLAY_TYPES
    NULL_DISPLAY_TYPE = 0,
    CRT_TYPE,
    RESERVED_TYPE,
    DFP_TYPE,
    LFP_TYPE,
    MAX_DISPLAY_TYPES = LFP_TYPE
} DISPLAY_TYPE;
#endif
//  Display port type enumeration
typedef enum
{
    NULL_PORT_TYPE = -1,
    ANALOG_PORT    = 0,
    DVOA_PORT,
    DVOB_PORT,
    DVOC_PORT,
    DVOD_PORT,
    LVDS_PORT,
    INTDPE_PORT,
    INTHDMIB_PORT,
    INTHDMIC_PORT,
    INTHDMID_PORT,
    INT_DVI_PORT, // NA
    INTDPA_PORT,  // Embedded DP For ILK
    INTDPB_PORT,
    INTDPC_PORT,
    INTDPD_PORT,
    TPV_PORT, // This is for all the TPV Ports..
    INTMIPIA_PORT,
    INTMIPIC_PORT,
    WIGIG_PORT,
    DVOF_PORT,
    INTHDMIF_PORT,
    INTDPF_PORT,
    DVOE_PORT,     // For Gen11, DDIE can be used for HDMI
    INTHDMIE_PORT, // For Gen11, DDIE can be used for HDMI
    INTDPG_PORT,   // Gen11P5 onwards
    DVOG_PORT,
    INTHDMIG_PORT,
    INTDPH_PORT,
    DVOH_PORT,
    INTHDMIH_PORT,
    INTDPI_PORT,
    DVOI_PORT,
    INTHDMII_PORT,
    MAX_PORTS
} PORT_TYPES,
*PPORT_TYPES;
#define MAX_DISPLAYS (MAX_PORTS * 1) // Allows for combo codecs
//
//#pragma pack(push, CUIREGPACK)
//#pragma pack(1)
//  Display device list data structure
typedef struct _DISPLAY_LIST
{
    DDU32 nDisplays;
    DDU32 ulDisplayUID[MAX_DISPLAYS];
    DDU32 ulDeviceConfig; // device configuration (Usefull for dual display)
    UCHAR ucConnectorIndex;
} DISPLAY_LIST, *PDISPLAY_LIST;

typedef struct _SB_VRR_DATA
{
    BOOLEAN bVRRCurrentMode;
    BOOLEAN bVRRDefaultMode;
} SB_VRR_DATA;

//#pragma pack(pop, CUIREGPACK)

typedef enum _VRR_STATUS
{
    VRR_STATUS_UNKNOWN      = 0x7F,
    VRR_DISABLED            = 0,
    VRR_ENABLED             = 1,
    VRR_DISABLE_IN_PROGRESS = 2
} VRR_STATUS;

typedef struct _SB_VRR_INFO
{
    DDU32      ulPipeID;
    VRR_STATUS eVRRStatus;
} SB_VRR_INFO, *PSB_VRR_INFO;

// ELD Type
// Enum defining ELD and EELD
typedef enum _ELD_DATA_TYPE
{
    NORMAL_ELD   = 1,
    ENHANCED_ELD = 2
} ELD_DATA_TYPE;

typedef enum _COMPRESSION_TYPE
{
    UNCOMPRESSED_SURF      = 0,
    RENDER_COMPRESSED_SURF = 1,
    MEDIA_COMPRESSED_SURF  = 2
} COMPRESSION_TYPE;

// Tile widths to use with each of the above suface types
// For YF tiling, 8bpp has a different width than the others
// All tile widths are in Bytes.
typedef enum _SURFACE_MEMORY_TILE_WIDTH
{
    SURFACE_MEMORY_TILE_WIDTH_DEFAULT            = 64,
    SURFACE_MEMORY_TILE_WIDTH_LINEAR             = SURFACE_MEMORY_TILE_WIDTH_DEFAULT,
    SURFACE_MEMORY_TILE_WIDTH_TILED              = 512,
    SURFACE_MEMORY_TILE_WIDTH_X_TILED            = SURFACE_MEMORY_TILE_WIDTH_TILED,
    SURFACE_MEMORY_TILE_WIDTH_Y_LEGACY_TILED     = 128,
    SURFACE_MEMORY_TILE_WIDTH_Y_F_TILED_8BPP     = 64,
    SURFACE_MEMORY_TILE_WIDTH_Y_F_TILED_NON_8BPP = 128
} SURFACE_MEMORY_TILE_WIDTH;

//
//  Colorspace type
//
typedef enum _SB_COLORSPACE_TYPES
{
    eInvalidSpace = -1,
    eSRGB         = 0, // default case, use 709 primaries for HD & 601 for SD
    // for future use only
    eYCrCb601,       // YCrCb 601 output
    eYCrCb709,       // YCrCb 709 output
    eYCrCb601_xvYCC, // extended, primaries are the same as non-xvYCC ones, for use with ILK
    eYCrCb709_xvYCC, // extended, primaries are the same as non-xvYCC ones, for use with ILK
    eYCrCb2020,
    eRGB2020,
    eMaxColorSpace,
    // Custom primaries
    eCustomColorSpace = 0xFF // HP RCR scenario
} SB_COLORSPACE_TYPES,
*PSB_COLORSPACE_TYPES;

// Struct representing surface memory offset data
// Used by SB_SETDISPLAYSTART_ARGS
typedef struct _SURFACE_MEM_OFFSET_INFO
{
    // Indicates surface memory type
    // Note: Based on this param SB will read & program
    // linear/tiled offset values
    // Indicates surface memory type
    IN SURFACE_MEMORY_TYPE eSurfaceMemType;

    union {
        // Gen4 linear offset
        IN DDU32 ulLinearOffset;

        // Gen4 tiled offset
        struct
        {
            IN DDU32 ulTiledXOffset;
            IN DDU32 ulTiledYOffset;
            IN DDU32 ulTiledUVXOffset; // NV12 case
            IN DDU32 ulTiledUVYOffset; // NV12 case
            IN DDU64 ullBaseAddress;
            IN DDU64 ullUVBaseAddress;
        };
    };

    IN DDU32 ulUVDistance;  // For NV12 surface, as of now nv12 cant come in normal flip path
    IN DDU32 ulAuxDistance; // Control surface Aux Offset. Will be 0 for non unified allocations, MP is abstracted from it
    IN DDU64 ullCCValue;    // Clear color value gen11.5+
    IN COMPRESSION_TYPE eCompType;
} SURFACE_MEM_OFFSET_INFO, *PSURFACE_MEM_OFFSET_INFO;

typedef struct _SURFACE_DIMENSION_INFO
{
    DDU32 ulYWidth;
    DDU32 ulYHeight;
    DDU32 ulUVWidth;
    DDU32 ulUVHeight;
} SURFACE_DIMENSION_INFO, *PSURFACE_DIMENSION_INFO;

// escape shared code
typedef enum _COM_ESC_REG_LOC
{
    GENERIC = 0, // Absolute Path
    MEDIA,       //\\Registry\\Machine\\Software\\INTEL\\Display\\igfxcui\\MediaKeys
    D3D_REG,     //\\Registry\\Machine\\Software\\INTEL\\Display\\igfxcui\\3D .
    DPP,         // Software\\Intel\\IGFX\\DPP
    MISC,        //\\Registry\\Machine\\Software\\INTEL\\Display\\igfxcui\\MISC,
    WIN10XVP,    //\\Registry\\Machine\\Software\\Microsoft\\Windows Media Foundation\\Platform\\XVP, for enable Win10 Metro mode auto processing, request from UMD Media driver
    WIN10WOW64XVP, //\\Registry\\Machine\\Software\\Wow6432Node\\Microsoft\\Windows Media Foundation\\Platform\\XVP, for enable Win10 Metro mode auto processing, request from UMD Media driver
    MAX_LOC
} COM_ESC_REG_LOC;

// I2C Open -----------------------------------------------------------------

// I2C device details structure
typedef struct _I2C_DEVICE
{
    IN DDU32 ulDisplayUID;
    IN struct
    {
        DDU32 bDDC : 1;         // Bit 0
        DDU32 bI2C : 1;         // Bit 1, not valid for CRT
        DDU32 bBlc : 1;         // Bit 2, for BLC I2C Inverter Support.
        DDU32 bD_Connector : 1; // bit 3, for d-connector testing
        DDU32 bReserved : 28;   // Bit[4:31] are reserved.
    };
} I2C_DEVICE;

#define I2COpen_FuncCode (0x5F26)

// I2C open args structure
typedef struct _SB_I2COPEN_ARGS
{
    IN DDU32 ulOpenClose;      // 1 = Open, 0 = Close
    IN I2C_DEVICE stI2CDevice; // See above definition
} SB_I2COPEN_ARGS, *PSB_I2COPEN_ARGS;

// Due to hardware limitations the max aux transaction size is limited to 16 Bytes.
// This macro is used to divide the number of Bytes into chunks of 16 Bytes.
#define MAX_AUX_TXN_SIZE 0x10

// I2C Access - 5F26 --------------------------------------------------------

#define I2CAccess_FuncCode (0x5F26)
#define MAX_AUX_BUFSIZE 0x0080
#define MAX_LUT_AUX_BUFSIZE 0x0200

// I2C access args structure
typedef struct _SB_I2CACCESS_ARGS
{
    IN DDU32 flFlagsCommand;   // Flags | Commands
    IN DDU32 ulSize;           // Valid sizes are 0 - 4 only
    IN DDU32 ulIndex;          // DDU8, Word or Dword sized
    IN_OUT DDU32 ulAddress;    // I2C slave address
    IN I2C_DEVICE stI2CDevice; // See above definition
    IN DDU8 DataBufr[MAX_AUX_BUFSIZE];
} SB_I2CACCESS_ARGS, *PSB_I2CACCESS_ARGS;

// Atomic I2C Access-5f38 ------------------------------------------------------

#define AtomicI2CAccess_FuncCode (0x5F38)

// Atomic I2C access args structure
typedef struct _SB_ATOMICI2CACCESS_ARGS
{
    IN DDU32 flFlagsCommand;   // Flags | Commands
    IN DDU32 ulSize;           // Valid sizes are 0 - 4 only
    IN DDU32 ulIndex;          // DDU8, Word or Dword sized
    IN_OUT DDU32 ulAddress;    // I2C slave address
    IN I2C_DEVICE stI2CDevice; // See above definition
    IN DDU32 ulReadBytes;
    IN DDU32 ulWriteBytes;
    IN DDU8 Data[MAX_AUX_BUFSIZE];
} SB_ATOMICI2CACCESS_ARGS, *PSB_ATOMICI2CACCESS_ARGS;

// These error types are used to notify various error scenarios for Aux Communication

typedef enum _SB_AUX_ERROR_TYPE
{
    SB_AUX_NOERROR = 0,
    SB_AUX_CORRUPT_BUFFER,
    SB_AUX_INVALID_AUX_DEVICE,
    SB_AUX_INVALID_OPERATION_TYPE,
    SB_AUX_INVALID_AUX_DATA_SIZE,
    SB_AUX_INVALID_AUX_ADDRESS,
    SB_AUX_ERROR_DEFER,
    SB_AUX_ERROR_TIMEOUT,
    SB_AUX_ERROR_INCOMPLETE_WRITE,
    SB_AUX_ERROR_UNKNOWN,
    SB_MAX_ERRORS
} SB_AUX_ERROR_TYPE;

//
// Command definitions
//
typedef enum _SBAUX_REQUEST_COMMAND_TYPES
{
    // I2C on AUX
    eSB_I2CAUXWrite,              // 0000
    eSB_I2CAUXRead,               // 0001
    eSB_I2CAUXWriteStatusReq,     // 0010
    eNO_Command1,                 // No command for value 3
                                  // I2C with MOT set
    eSB_I2CAUXWrite_MOT,          // 0100
    eSB_I2CAUXRead_MOT,           // 0101
    eSB_I2CAUXWriteStatusReq_MOT, // 0110
    eNO_Command2,                 // No command for value 7
                                  // Native AUX
    eSB_AUXWrite,                 // 1000
    eSB_AUXRead,                  // 1001
    eSB_RemoteDPCDWrite,          // 1010
    eSB_RemoteDPCDRead,           // 1011
    eSB_RemoteI2CWrite,           // 1100
    eSB_RemoteI2CRead,            // 1101
    eMAX_SB_Commands
} SBAUX_REQUEST_COMMAND_TYPES;

typedef enum _SBI2C_REQUEST_COMMAND_TYPES
{
    eSB_I2C_COMMAND_NULL   = 0x0000, // Does no command
    eSB_I2C_COMMAND_READ   = 0x0001, // Reads Data from an I2C Bus Device
    eSB_I2C_COMMAND_WRITE  = 0x0002, // Writes Data out on the I2C Bus Device
    eSB_I2C_COMMAND_STATUS = 0x0003, // Effects I2C Bus State
    eSB_I2C_COMMAND_RESET  = 0x0004, //
} SBI2C_REQUEST_COMMAND_TYPES;

#define MAX_DP_PORTS 6
// DP1.2
// CUI Interface Related Details..
// Adding DP12 Topology - Funcode --------------------------------
#define DPTOPOLOGY_FuncCode (0x5F99)

// Func used for getting complete topology for all Ports
// Use SB_GET_DP_COMPLETE_TOPOLOGY_BUFHDR Struct
#define GetComplete_DPTOPOLOGY_SubFuncCode (0x00)

// Func used for getting detailed info for a particular Leaf
// Use SB_GET_DP_DETAILED_LEAF_INFO Struct
#define GetDetailedInfoForLeaf_DPTOPOLOGY_SubFuncCode (0x01)

// Func used for getting timing for particular custom mode, user has specified
// Use SB_SET_DP_COMPLETE_TOPOLOGY_BUFHDR Struct
#define SetLeafListForEachPort_DPTOPOLOGY_SubFuncCode (0x02)

// Func used for sending Simulated DP1.2 topology
#define Simulate_DPTOPOLOGY_SubFuncCode (0x03)

// Based on DP1.2 Spec. Total Number of Links is 15
#define MAX_LINK_COUNT 15

// As every Address for a link requires 4 Bits, therefore total 14 links (MAX_LINK_COUNT - 1, since for 1st link RAD is not required) would require 56 bits.
// Hence total 7 Bytes
#define MAX_BYTES_RAD ((MAX_LINK_COUNT) / 2)

//#pragma pack(1)
typedef struct _RELATIVEADDRESS
{
    UCHAR ucTotalLinkCount;

    // If ucTotalLinkCount is 1 then Relative ucAddress should have zero value at all the indexes..

    // If the ucTotalLinkCount is Even then index from 0 till (ucTotalLinkCount/2 - 1) (apart from the Upper Nibble of last index) is a Valid Address, .

    // If the ucTotalLinkCount is Odd then index from 0 till (ucTotalLinkCount)/2 - 1) will be a Valid Address

    // Hence for both odd/even ucTotalLinkCount, we can use Index from 0 till (ucTotalLinkCount/2 - 1)

    UCHAR ucAddress[MAX_BYTES_RAD];
} RELATIVEADDRESS, *PRELATIVEADDRESS;

typedef enum _SB_LEAFTYPE
{
    eSB_InValidType  = 0,
    eSB_DPType       = 1,
    eSB_DVI_HDMIType = 2,
    eSB_VGAType      = 3,
} SB_LEAFTYPE;

typedef struct _SB_LEAFDEVICEINFO
{
    RELATIVEADDRESS RelativeAddress;
    DDU32           ulParentBranchIndex;
    BOOLEAN         bOSAwareDisplay;
    BOOLEAN         bActiveDisplay;
    BOOLEAN         bHasInbuiltBridge;
} SB_LEAFDEVICEINFO, *PSB_LEAFDEVICEINFO;

typedef struct _SB_BRANCHDEVICEINFO
{
    RELATIVEADDRESS RelativeAddress;
    DDU32           ulParentBranchIndex;
    BOOLEAN         bLoopDetected;
} SB_BRANCHDEVICEINFO, *PSB_BRANCHDEVICEINFO;

typedef struct _SB_LEAFDEVICESLIST
{
    PSB_LEAFDEVICEINFO pLeafList;
    DDU32              ulNumLeavesList;
} SB_LEAFDEVICESLIST, *PSB_LEAFDEVICESLIST;

typedef struct _SB_BRANCHDEVICESLIST
{
    PSB_BRANCHDEVICEINFO pBranchList;
    DDU32                ulNumBranchesList;
} SB_BRANCHDEVICESLIST, *PSB_BRANCHDEVICESLIST;

// DPTOPOLOGY : used in Softbios
typedef struct _DPTOPOLOGY
{
    PORT_TYPES           ePortType;
    UCHAR                ucNumberOfStreamsSupported;
    SB_BRANCHDEVICESLIST stBranchDevicesList;
    SB_LEAFDEVICESLIST   stLeafDevicesList;
} DPTOPOLOGY, *PDPTOPOLOGY;

// DP_GET_COMPLETE_TOPOLOGY: used in Softbios
typedef struct _DP_GET_COMPLETE_TOPOLOGY
{
    DDU32      ulNumValidDPPorts;
    DPTOPOLOGY stDPTopology[MAX_DP_PORTS];
} DP_GET_COMPLETE_TOPOLOGY, *PDP_GET_COMPLETE_TOPOLOGY;

// SB_GET_DPCOMPLETE_TOPOLOGY_ARGS: used in DRIVER only
typedef struct _SB_GET_DPCOMPLETE_TOPOLOGY_ARGS
{
    IN DDU32                 Cmd; // DPTOPOLOGY_FuncCode + GetComplete_DPTOPOLOGY_SubFuncCode
    DP_GET_COMPLETE_TOPOLOGY stDPGetTopology;
} SB_GET_DPCOMPLETE_TOPOLOGY_ARGS, *PSB_GET_DPCOMPLETE_TOPOLOGY_ARGS;

typedef struct _SB_GET_DP_DETAILED_LEAF_INFO
{
    SB_LEAFDEVICEINFO stLeafDevice;
    PORT_TYPES        eQueriedPortType;
    UCHAR             ucMonitorName[13];
    BOOLEAN           bMonitorNameExists;
    // Display Type
    SB_LEAFTYPE eLeafType;
} SB_GET_DP_DETAILED_LEAF_INFO, *PSB_GET_DP_DETAILED_LEAF_INFO;

// DP_SET_COMPLETE_TOPOLOGY : used inside Softbios
typedef struct _DP_SET_COMPLETE_TOPOLOGY
{
    PORT_TYPES         ePortType;
    SB_LEAFDEVICESLIST stLeafDevicesList;
} DP_SET_COMPLETE_TOPOLOGY, *PDP_SET_COMPLETE_TOPOLOGY;

// SB_SET_DP_TOPOLOGY_ARGS: used in DRIVER only
typedef struct _SB_SET_DP_TOPOLOGY_ARGS
{
    IN DDU32                 Cmd; // DPTOPOLOGY_FuncCode + SetLeafListForEachPort_DPTOPOLOGY_SubFuncCode
    DP_SET_COMPLETE_TOPOLOGY stDPSetTopology;
} SB_SET_DP_TOPOLOGY_ARGS, *PSB_SET_DP_TOPOLOGY_ARGS;
//#pragma pack()

#define AuxAccess_FuncCode (0x5F39)
// I2C access args structure
//#pragma pack(1)
typedef struct _SB_AUXCACCESS_ARGS
{
    OUT SB_AUX_ERROR_TYPE eSBAuxErrorType;
    IN PORT_TYPES portType;
    IN RELATIVEADDRESS relativeAddress;
    IN DDU32 ulDeviceUID;    // Display UID
    IN DDU32 Command;        // Commands (0- Read, 1-Write)
    IN BOOLEAN bUsePortType; // 0 - Use DeviceID, 1 - Use Port Type
    IN_OUT DDU32 ulSize;     // Valid sizes are 0 - 16 only
    IN_OUT DDU8 Data[MAX_LUT_AUX_BUFSIZE];
    IN DDU32 ulAddress; // 20-bit format AUX Address OR 7-bit I2C address
} SB_AUXACCESS_ARGS, *PSB_AUXACCESS_ARGS;
//#pragma pack()

typedef enum _HAS_REQUEST_TYPE
{
    HAS_GETCONFIG = 0,
    HAS_SETCONFIG,
    HAS_SETDPCD,
} HAS_REQUEST_TYPE;
typedef struct _HASARGS
{
    HAS_REQUEST_TYPE   eService;
    DDU64              ulHASConfig;
    PSB_AUXACCESS_ARGS pAuxArgs;
} HASARGS, *PHASARGS;

//  Pipe-display association data structure
//
//  Usage model for this structure
//
//  1. Single Intel pipe A only
//      Set bIntelPipeSelectList[PIPE_A] = TRUE;
//      Set stIntelDisplayList[0] for pipe A.
//      Set bIntelPipeSelectList[PIPE_B] = FALSE;
//      If we have TPV Pipes Supported then, we need to allocate memory for pTPVPipeSelect & pTPVDisplayList with Max_NumTPV Pipes...
//      Fill the variable ulMaxTPVPipes
//      Fill for each of the TPV Pipes pTPVPipeSelect[0] = FALSE,pTPVPipeSelect[1] = FALSE, pTPVPipeSelect[ulMaxTPVPipes-1] = FALSE

//  2. Single TPV_PIPE(0) only
//      Set bIntelPipeSelectList[PIPE_A] = FALSE &  Set bIntelPipeSelectList[PIPE_B] = FALSE;
//      we need to allocate memory for pTPVPipeSelect & pTPVDisplayList with Max_NumTPV Pipes...
//      Fill the variable ulMaxTPVPipes
//      Fill for pTPVPipeSelect[0] = TRUE,
//      For remaining each of the TPV Pipes pTPVPipeSelect[1] = FALSE, pTPVPipeSelect[ulMaxTPVPipes-1] = FALSE

//  3. Dual Intel pipe A and Intel pipe B
//      Set bIntelPipeSelectList[PIPE_A] = TRUE;
//      Set stIntelDisplayList[0] for pipe A.
//      Set bIntelPipeSelectList[PIPE_B] = TRUE;
//      Set stIntelDisplayList[1] for pipe B.
//      If we have TPV Pipes Supported then, we need to allocate memory for pTPVPipeSelect & pTPVDisplayList with Max_NumTPV Pipes...
//      Fill the variable ulMaxTPVPipes
//      Fill for each of the TPV Pipes pTPVPipeSelect[0] = FALSE,pTPVPipeSelect[1] = FALSE, pTPVPipeSelect[ulMaxTPVPipes-1] = FALSE

//
//  4. To enable, PIPE A & TPV_PIPE(0), we need to
//      Set bIntelPipeSelectList[PIPE_A] = TRUE;
//      Set stIntelDisplayList[0] for pipe A.
//      Set bIntelPipeSelectList[PIPE_B] = FALSE;
//      we need to allocate memory for pTPVPipeSelect & pTPVDisplayList with Max_NumTPV Pipes...
//      Fill the variable ulMaxTPVPipes
//      Initialize pTPVPipeSelect[0..ulMaxTPVPipes-1] all to FALSE
//      Initialize pTPVPipeSelect[0] to TRUE
//      Initialize pTPVDisplayList[0..ulMaxTPVPipes-1] all to Zero
//      Fill in pTPVDisplayList[0] to relevant Displays

typedef struct _TPV_PIPE_DISPLAYS_LIST
{
    DDU32 ulMaxTPVPipes;           // This will indicate the number of TPV Pipes that can exist.
                                   // The belowe Pointers pPipeSelect & pDisplayList will be used as array ranging from 0 to (ulMaxTPVPipes - 1)
    PBOOLEAN      pTPVPipeSelect;  // This will indicate which of the TPV Pipes are selected...
    PDISPLAY_LIST pTPVDisplayList; // This will indicate the Display List per TPV Pipe
} TPV_PIPE_DISPLAYS_LIST, *PTPV_PIPE_DISPLAYS_LIST;

typedef struct _PIPE_DISPLAYS
{
    BOOLEAN                bIntelPipeSelectList[MAX_PHYSICAL_PIPES];
    DISPLAY_LIST           stIntelDisplayList[MAX_PHYSICAL_PIPES];
    TPV_PIPE_DISPLAYS_LIST stTPVPipeDisplayList;
} PIPE_DISPLAYS, *PPIPE_DISPLAYS;

// Executes a SoftBios Service by it's Function Code .

#define ByFuncCode_FuncCode (0xFFFFFFFF)
#define ByFuncCode_SubFunc (0xFFFFFFFF)

// Structure for SB function details
typedef struct _SB_FUNC_DATABUF
{
    DDU32 Func_ID; // SoftBIOS function ID, including function number and sub-function number
    DDU32 Arg[1];  // Variable length parameters
} SB_FUNC_DATABUF, *LP_SB_FUNC_DATABUF;

typedef struct _SB_BYFUNCCODE_ARGS
{
    IN DDU32 ulSize;                    // Size of this data structure
    IN DDU32 ulDataBufSize;             // Size of the data buffer
    IN_OUT LP_SB_FUNC_DATABUF pDataBuf; // Pointer to data buffer
} SB_BYFUNCCODE_ARGS, *PSB_BYFUNCCODE_ARGS;

// 0x00 - Set Mode Parameters -----------------------------------------------

typedef struct _SB_SF_INFO
{
    BOOLEAN bSFSupported;    // SF supported in sku and enabled in inf
    BOOLEAN bSFEnable;       // SF enable/disable request
    BOOLEAN bPFPreferForLFP; // inf set for reserving highest capable PF for LFP
    PIPE_ID eLFPPipe;        // Pipe id assigned to LFP
} SB_SF_INFO, *PSB_SF_INFO;

typedef struct _SB_SF_CHECK_ARGS
{
    DDU32 ulVersion;
} SB_SF_CHECK_ARGS, *PSB_SF_CHECK_ARGS;

typedef enum _PORT_SYNC_SUPPORT_STATUS
{
    PORT_SYNC_NOT_SUPPORTED = 0,
    PORT_SYNC_SW,
    PORT_SYNC_HW
} PORT_SYNC_SUPPORT_STATUS;
typedef struct _PORT_SYNC_CAPS
{
    PORT_SYNC_SUPPORT_STATUS eCapability;
    DDU32                    ulMasterPipe; // used to indicate master pipe when PORT_SYNC_HW is used
    DDU32                    ulSlavePipe;  // used to indicate slave pipe when PORT_SYCH_HW is used
} PORT_SYNC_CAPS, *PPORT_SYNC_CAPS;

// Future Display Topology
typedef struct _SB_FUTURE_DISPLAY_CONFIG_INFO
{
    IN BOOLEAN bValid; // Indicates if valid data has been filled in this structure

    IN PIPE_DISPLAYS stPipeDisplays;

    // display Planes asscociated with a pipe
    IN UCHAR ucDisplayPlaneToPipe[MAX_PHYSICAL_PIPES];

    // Flag Added for indicating power state transitions
    IN UCHAR bPowerStateTransition;
} SB_FUTURE_DISPLAY_CONFIG_INFO, *PSB_FUTURE_DISPLAY_CONFIG_INFO;
//#pragma pack(1)
// Set display device args structure
typedef struct _SB_SETDISPLAYDEV_ARGS
{
    IN DDU32 ulSize; // Fixed size of Args !

    IN union {
        UCHAR ucOptions;
        struct
        {
            IN UCHAR ucForceExecute : 1;           // Bit0
            IN UCHAR ucDoNotTurnOffPanelPower : 1; // Bit1
            UCHAR    ucReserved : 6;               // Bits 2..7
        };
    };

    IN PIPE_DISPLAYS stPipeDisplays;

    // Display Planes asscociated with a pipe
    IN UCHAR ucDisplayPlaneToPipe[MAX_PHYSICAL_PIPES];

    IN SB_FUTURE_DISPLAY_CONFIG_INFO stFutureTopologyInfo;

    IN BOOLEAN bUpdateScratchPadRegs;
} SB_SETDISPLAYDEV_ARGS, *PSB_SETDISPLAYDEV_ARGS;
//#pragma pack()

//  MODE_FLAGS structure used by MODE_INFO structure
typedef union _MODE_FLAGS {
    DDU32 ulFlags;
    struct
    {
        unsigned bInterlaced : 1;            // Bit 0, 1 = Interlaced mode
        unsigned bDoubleWideMode : 1;        // Bit 1, 1 = Double-wide mode
        unsigned ucUnsupportedMode : 2;      // Bits 3:2, Non-monitor supported special mode
                                             // e.g. GTF modes for non-GTF supported monitor
                                             // 0 = Supported on Both
                                             // 1 = Not supported on Primary UID
                                             // 2 = Not supported on Non-Primary UID
                                             // 3 = Not supported on Both
        unsigned ucListIntersection : 2;     // Bits 5:4, Mode occurs in mode tables for
                                             // DISPLAY_LIST display devices
                                             // 0 = Occurs on both with same timing
                                             // 1 = Occurs on Primary UID
                                             // 2 = Occurs on Non-Primary UID
                                             // 3 = Occurs on Both, but with different timings
        unsigned bAboveMaxRes : 1;           // Bit 6, 1 = Mode resolution is above
                                             // monitor's maximum resolution
        unsigned bBelowMinRes : 1;           // Bit 7, 1 = Mode resolution is below
                                             // monitor's minimum resolution
        unsigned bModeInEdid : 1;            // Mode present in Display's Edid
        unsigned bModeIsPreferred : 1;       // Mode is a Preferred Mode if Set
        unsigned bIsTimingFromOEM : 1;       // Mode is OEM customized & got via INF/VBT.
        unsigned bModeAddedbyOS : 1;         // Mode added by OS
        unsigned bModeAddedOnlybyOS : 1;     // Mode exclusively added by OS
        unsigned bS3DFramePackedMode : 1;    // S3D mode in frame packed format as per HDMI 1.4/DP1.2
        unsigned bS3DSideBySideHalfMode : 1; // S3D mode in page flipping format
        unsigned bS3DTopBottomMode : 1;      // S3D mode in page flipping format
        unsigned bS3DSideBySideFullMode : 1; // S3D mode in page flipping format
        unsigned bS3DMode : 1;               // Bit Indicating whether the given mode is S3D
        unsigned bReserved : 14;             // Bits 15:31, Reserved
    };
} MODE_FLAGS, *PMODE_FLAGS;

//  MODE_INFO data structure
typedef struct _MODE_INFO
{
    DDU16      usXResolution; // X resolution in pixels
    DDU16      usYResolution; // Y resolution in pixels
    DDU16      usColorBPP;    // Color depth in bits/pixel
    DDU16      usRefreshRate; // Vertical refresh rate in Hz
    MODE_FLAGS flFlags;       // Mode flags

    IN_OUT SB_PIXELFORMAT eSourcePixelFormat; // Pixel format for this mode
    DDU16                 usBlankActiveLines; // valid iff flFlags.bS3DFramePackedMode is set
} MODE_INFO, *PMODE_INFO;
#define SetMode_FuncCode (0x0000)
// Note: Currently set mode args doesn't take care of
// cursor plane, in future it needs to be also sent as
// part of setmode
// Set Mode cannot be used to set on Two Pipes at One shot. Caller should call two set Modes for each of the pipes he wants to enable..
typedef struct _SB_SETMODE_ARGS
{
    IN MODE_INFO ModeInfo;
    IN DDU32 ulPipeIndex;         // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
    IN DDU32 ulRequestedOSModeX;  // Actual GDI mode X
    IN DDU32 ulRequestedOSModeY;  // Actual GDI mode Y
    IN DDU32 ulRequestedOSModeRR; // For future use in case if required
    IN DDU32 ulScanLineLength;    // Scan line length/Pitch
                                  //
                                  // Gen4+ specific parametes
                                  // Note: Called has to set these parameters properly
                                  //

    // Orientation information
    PLANE_ORIENTATION eOrientation;

    // Pipe Orientation  Information
    PIPE_ORIENTATION pipeOrientation;

    // Surface type information
    SURFACE_MEMORY_TYPE eSurfaceMemType;

    // Video Blanking Required during mode set.
    // If this variable is set to TRUE, then it will first disable the video, Complete the SetTiming and then enables the Video.
    // If this variable is set to FALSE, then it will just do a SetTiming.
    IN BOOLEAN bVideoBlankingReqd;
    // Used only for TPV displays
    IN DDU32 ulSourceID;
    // This variable will be used in SG Case when the Mux is still present with Discrete GPU but we are getting a Commit Vidpn Call. This is an interim WA until we get fix from TPV
    IN BOOLEAN bIgnoreAuxFailuresDuringSetMode;
    // bug: 3799044. dont enable plane in set mode if this flag is set till we get a explicit Blank Video (OFF) call..
    BOOLEAN bEnablePlaneCaching;
    // FASTMODESET enable/disable option
    BOOLEAN bUseFastModeSet;
    // IFFS Flashless Resume
    BOOLEAN bSkipEnablePlane;
    // Indicates SoftBIOS to delay Pipe Enabling till all paths are enabled.. Set for enabling Collage in Eizo monitors to avoid phase difference between VBlanks..
    BOOLEAN        bPipeLock;
    PORT_SYNC_CAPS stPortSyncCaps;
    // Indicates Hardware toggling and request for HDMI and DP Clone S3D request
    BOOLEAN    bUseS3DHardwareAutoToggle;
    SB_SF_INFO SFInfo;

    BOOLEAN bModeSetAtDriverUnload;
    BOOLEAN bInternalModesetContext;
#if LHDM || SB_NAPA_ULT
    IN MONITOR_MODE_INFO stMonitorModeInfo;
    IN DDU32 ulScaling;
    BOOLEAN  bPrioritizeHDR; // As part of setmode, MP will set this based on OS request. MP will take care of seeing if panel supports HDR or not.
#endif
    IN UCHAR ucWireFormat;
    IN DDU32 ulBPCSupportedMask;
    IN UCHAR ucColorSpace;
    IN BOOLEAN bPreserveBootDisplay;
} SB_SETMODE_ARGS, *PSB_SETMODE_ARGS;

typedef struct _SB_PORT_SYNC_CAPABILITY_ARGS
{
    IN SB_SETDISPLAYDEV_ARGS stSetDisplayDeviceArgs;
    IN SB_SETMODE_ARGS stSbSetModeArg[MAX_PHYSICAL_PIPES];
    IN DDU32 ulPipeIndex[MAX_PHYSICAL_PIPES];
    IN DDU32 ulDispConfig;
    IN BOOLEAN bIsCollageEnabled;
    OUT PORT_SYNC_CAPS stPortSyncCaps;
} SB_PORT_SYNC_ARGS, *PSB_PORT_SYNC_ARGS;

// 0x1C00 - Get Save / Restore State Buffer Size ---------------------------

#define StateBufferSize_FuncCode (0x1C00)

// Save - Restore options structure
typedef struct
{
    DDU32 bMemoryMappedRegState : 1; // Bit0
    DDU32 bHWState : 1;              // Bit1
    DDU32 bDACState : 1;             // Bit2
    DDU32 bPlaneState : 1;           // Bit3

    // The following should all be reserved fields, no longer supported in
    // PC14.  Left here for backward compatibility, should be removed if
    // miniport removes reference to these fields.
    DDU32 bBIOSDataState : 1;     // Bit4
    DDU32 bReInitLocalMemory : 1; // Bit5
    DDU32 bChildDevice : 1;       // Bit6
    DDU32 bExtRegState : 1;       // Bit7
    DDU32 bTV : 1;                // Bit8
    DDU32 bDFP : 1;               // Bit9
    DDU32 bLFP : 1;               // Bit10
    DDU32 bReserved : 21;         // Bit[11:31]
} SAVE_RESTORE_OPTS;

// State buffer size args structure
typedef struct _SB_STATEBUFFERSIZE_ARGS
{
    IN union {
        DDU32             ulSaveRestoreOptions; // Save/restore Options
        SAVE_RESTORE_OPTS Options;
    };
    OUT DDU32 ulStateBufferSize; // Save/restore buffer size
} SB_STATEBUFFERSIZE_ARGS, *PSB_STATEBUFFERSIZE_ARGS;

// 0x1C01 - Save the Adapter State -------------------------------------------

#define SaveState_FuncCode (0x1C01)

// save state args structure
typedef struct _SB_SAVESTATE_ARGS
{
    IN PVOID pSaveBuffer; // Save Buffer Pointer
    IN union {
        DDU32             ulSaveRestoreOptions; // Save/restore Options
        SAVE_RESTORE_OPTS Options;
    };
} SB_SAVESTATE_ARGS, *PSB_SAVESTATE_ARGS;

// 0x1C02 - Restore Adapter State -------------------------------------------

#define RestoreState_FuncCode (0x1C02)

// Restore state args structure
typedef struct _SB_RESTORESTATE_ARGS
{
    IN PVOID pRestoreBuffer;
    IN union {
        DDU32             ulSaveRestoreOptions; // Save/restore Options
        SAVE_RESTORE_OPTS Options;
    };
} SB_RESTORESTATE_ARGS, *PSB_RESTORESTATE_ARGS;

// 0x4F07, 0x00 - Set Display Start -----------------------------------------

#define SetDisplayStart_FuncCode (0x4F07)

typedef struct _SB_HDR_STATIC_METADATA
{
    DDU16 usEOTF;
    DDU16 usDisplayPrimariesX[3];
    DDU16 usDisplayPrimariesY[3];
    DDU16 usWhitePointX;
    DDU16 usWhitePointY;
    DDU16 usMaxDisplayMasteringLuminance;
    DDU16 usMinDisplayMasteringLuminance;
    DDU16 usMaxCLL;
    DDU16 usMaxFALL; // Maximum Frame Average Light Level
} SB_HDR_STATIC_METADATA, *PSB_HDR_STATIC_METADATA;

typedef struct _SB_HDR_SURFACE_DESC
{
    SB_HDR_STATIC_METADATA metadata;
    SB_COLORSPACE_TYPES    gamut; // YUVBT2020 or RGBBT2020
} SB_HDR_SURFACE_DESC, *PSB_HDR_SURFACE_DESC;
typedef struct _SB_SET_HDR_META_DATA
{
    SB_HDR_SURFACE_DESC hdrSurfInfo;
    DDU32               hAllocation;
} SB_SET_HDR_META_DATA, *PSB_SET_HDR_META_DATA;

// Structure for SetDisplayStart function
typedef struct _SB_SETDISPLAYSTART_ARGS
{
    // For setmode on all platforms: Base address
    IN DDU32 ulDisplayStart;
    IN DDU32 ulPlane;
    IN PLANE_ORIENTATION ePlaneOrientation; // HW rotation
    IN BOOLEAN bIsASynchMMIOFlip; // This is to indicate if its a Sync Flip. From Cantiga onwards, async Flip is handled in a more elegant way. Refer BSpec for more details.
    IN BOOLEAN bIsAsyncMMIOFlipWaitNeeded; // Needed to distinguish RS2 and other OS builds in SB
    IN SURFACE_MEM_OFFSET_INFO stSurfaceMemInfo;
    IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
    IN DDU32 ulScanLineLength;
    IN DDU32 ulAuxScanLineLength;
    IN SB_PIXELFORMAT ePixelFormat; // To be used for DirectFlip
    IN BOOLEAN bIsPlaneEncrypted;
    IN IGFX_ENCRYPTION_TYPE bEncryptiontype;
    IN PSB_HDR_SURFACE_DESC pHDRSurfInfo;
} SB_SETDISPLAYSTART_ARGS, *PSB_SETDISPLAYSTART_ARGS;

#define ON 1
#define OFF 0

// MBM Related Structure defines

typedef enum _MBM_PLANE_SEL
{
    eNoPlane               = 0,
    eDisplayPlane          = 2,
    eSpritePlane           = 1,
    eDisplayAndSpritePlane = 3,
} MBM_PLANE_SEL;

typedef struct _SB_AUDIO_ENABLE_PARAMS
{
    BOOLEAN bEnableAudioDevice;
    BOOLEAN bWaitforAudioUp;
} SB_AUDIO_ENABLE_PARAMS, *PSB_AUDIO_ENABLE_PARAMS;

typedef struct _SB_AUDIOPW_PARAMS
{
    BOOLEAN bEnableAudioPW;
} SB_AUDIOPW_PARAMS, *PSB_AUDIOPW_PARAMS;

typedef struct _HWSYNCH_QUERY_ARGS
{
    IN SB_SETMODE_ARGS stSbSetModeArgs[MAX_PHYSICAL_PIPES];
    IN DDU32 ulMasterDispId;
    IN DDU32 ulSlaveDispId;
    OUT BOOLEAN bCanSupportHwSynch;
} * PSB_HWSYNCH_QUERY_ARGS, SB_HWSYNCH_QUERY_ARGS;

// 0x4F06, 0x02 - Set Scan Line Length in Bytes -----------------------------

#define SetScanLineLength_FuncCode (0x4F06)

typedef struct _SB_SETSCANLINELENGTH_ARGS
{
    IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
    IN_OUT DDU32 ulScanLineLength;
    IN DDU32 ulAuxScanLineLength; // For Unified allocations, this corresponds to Pitch of Control surface.
} SB_SETSCANLINELENGTH_ARGS, *PSB_SETSCANLINELENGTH_ARGS;

typedef struct _SB_GETSETFLIPDONEINTR_ARGS
{
    IN UCHAR ucPipeIndex;      // Can be one of the values PIPE_A, PIPE_B, PIPE_C
    IN DDU32 ulPlaneID;        // This will be planeIDs to identify the planes in a Pipe.
    BOOLEAN  bSet;             // This flag is to decide whether to update flipDoneIntr state or to get the current state.
    PBOOLEAN pbFlipDoneNeeded; // This pointer gets updated by the detail stored in the plane object.
} SB_GETSETFLIPDONEINTR_ARGS, *PSB_GETSETFLIPDONEINTR_ARGS;

// DSM Enums
// The following Enum is passed in the _DSM call as Arg2 to specify the Function Index.
typedef enum _BIOS_DATA_DSM_FUNCS
{
    BIOS_DATA_FUNC_SUPPORT                       = 0x00, // function is supported
    SYSTEM_BIOS_ADAPTER_POWER_STATE_NOTIFICATION = 0x01,
    SYSTEM_BIOS_DISPLAY_POWER_STATE_NOTIFICATION = 0x02,
    SYSTEM_BIOS_POST_COMPLETION_NOTIFICATION     = 0x03,
    SYSTEM_BIOS_PRE_HIRES_SET_MODE               = 0x04,
    SYSTEM_BIOS_POST_HIRES_SET_MODE              = 0x05,
    SYSTEM_BIOS_SET_DISPLAY_DEVICE_NOTIFICATION  = 0x06,
    SYSTEM_BIOS_SET_BOOT_DEVICE_PREFERENCE       = 0x07,
    SYSTEM_BIOS_SET_PANEL_PREFERENCE             = 0x08,
    SYSTEM_BIOS_FULL_SCREEN_DOS                  = 0x09,
    SYSTEM_BIOS_APM_COMPLETE                     = 0x0A,
    SYSTEM_BIOS_PLUG_UNPLUG_AUDIO                = 0x0B,
    SYSTEM_BIOS_CDCLOCK_CHANGE_NOTIFICATION      = 0x0C,
    SYSTEM_BIOS_GET_BOOT_DISPLAY_PREFERENCE      = 0x0D,
    SYSTEM_BIOS_GET_PANEL_DETAILS                = 0x0E,
    SYSTEM_BIOS_INTERNAL_GRAPHICS                = 0x0F,
    SYSTEM_BIOS_GET_AKSV                         = 0x10,
    SYSTEM_BIOS_ENABLE_S0ix_HPD                  = 0x11,
    BIOS_DATA_RESERVED // LAST ENTRY
} BIOS_DATA_DSM_FUNCS,
*PBIOS_DATA_DSM_FUNCS;

// Returns if GetBiosData Function is Supported.
// For any _DSM, bit 0 in field above denotes if Function of _DSM with this GUID is supported, bit 1 denotes if AdapterPowerStateNotification is supported and so on.
// definition of output bits
typedef union _DSM_SUPPORT_FIELDS_VECTOR {
    struct
    {
        DDU32 GetBiosDataFuncSuppt : 1;                 // BIT 0
        DDU32 AdapterPowerStateNotification : 1;        // Bit 1
        DDU32 DisplayPowerStateNotification : 1;        // Bit 2
        DDU32 SystemBIOSPOSTCompletionNotification : 1; // BIT 3
        DDU32 PreHiResSetMode : 1;                      // BIT 4
        DDU32 PostHiResSetMode : 1;                     // BIT 5
        DDU32 SetDisplayDeviceNotification : 1;         // BIT 6
        DDU32 SetBootDevicePreference : 1;              // BIT 7
        DDU32 SetPanelPreference : 1;                   // BIT 8
        DDU32 FullScreenDOS : 1;                        // BIT 9
        DDU32 APMComplete : 1;                          // BIT 10
        DDU32 UnplugPlugAudio : 1;                      // BIT 11
        DDU32 CDClockChangeNotification : 1;            // BIT 12
        DDU32 GetBootDisplayPreference : 1;             // BIT 13
        DDU32 GetPanelDetails : 1;                      // BIT 14
        DDU32 InternalGraphics : 1;                     // BIT 15
        DDU32 GetAKSV : 1;                              // BIT 16
        DDU32 Reserved : 15;                            // BITS 17:31
    };
    DDU32 ulValue;
} DSM_SUPPORT_FIELDS_VECTOR, *PDSM_SUPPORT_FIELDS_VECTOR;

typedef struct _SB_MBMINFO_ARGS
{
    DDU32         ulPipe;
    MBM_PLANE_SEL ePlaneSel;
    BOOLEAN       bMBMSupported;
    DDU32         ulFrameAddress;

    // If this is set to TRUE, SoftBIOS will use Linear/Tiled from stSurfaceMemInfo instead of using Source Plane Params and also Scanline
    BOOLEAN bUpdateSurfaceTypeandLength;
    IN SURFACE_MEM_OFFSET_INFO stSurfaceMemInfo;
    DDU32                      ulScanLineLength; // for stride DA02/DB02 (pitch)
} SB_MBMINFO_ARGS, *PSB_MBMINFO_ARGS;

// Structure added for updating the plane pixel format.
typedef struct _SB_UPDATEPLANEPIXELFORMAT_ARGS
{
    IN DDU32 ulPlane;
    IN SB_PIXELFORMAT ePixelFormat;
} SB_UPDATEPLANEPIXELFORMAT_ARGS, *PSB_UPDATEPLANEPIXELFORMAT_ARGS;

// 0x4F07, 0x01 - Get Display Start -----------------------------------------

#define GetDisplayStart_FuncCode (0x4F07)
#define GetDisplayStart_SubFunc (0x01)

// Structure for get display start
typedef struct _SB_GETDISPLAYSTART_ARGS
{
    IN DDU32 ulDisplayStart;
    IN       BOOLEAN
             bGetDoubleBufferedAddress; // From Cantiga onwards, SoftBIOS can get the Live Display Start Address. This is more to do whether u want to get Live or Double Buffered address.
    IN UCHAR ucPlaneIndex;
    IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
} SB_GETDISPLAYSTART_ARGS, *PSB_GETDISPLAYSTART_ARGS;

// 0x4F07, 0x03 - Schedule Stereoscopic Display Start -----------------------

#define SetStererStart_FuncCode (0x4F07)
#define SetStererStart_SubFunc (0x03)
// Set stereo start args structure
typedef struct _SB_SETSTEREOSTART_ARGS
{
    IN DDU32 ulLeftDisplayStart;
    IN DDU32 ulRightDisplayStart;
    IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
} SB_SETSTEREOSTART_ARGS, *PSB_SETSTEREOSTART_ARGS;

// 0x4F07, 0x04 - Get Scheduled Display Start Status ------------------------

#define GetStartStatus_FuncCode (0x4F07)
#define GetStartStatus_SubFunc (0x04)
// Get start status args structure
typedef struct _SB_GETSTARTSTATUS_ARGS
{
    OUT DDU32 ulStatus;
    IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
} SB_GETSTARTSTATUS_ARGS, *PSB_GETSTARTSTATUS_ARGS;

// 0x4F07, 0x05 - Set Stereoscopic Mode -------------------------------------

#define SetStereoMode_FuncCode (0x4F07)
#define SetStereoMode_SunFunc (0x05)

// Set stereo mode args structure
typedef struct _SB_SETSTEREOMODE_ARGS
{
    IN DDU32 ulStereoMode;
    IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
} SB_SETSTEREOMODE_ARGS, *PSB_SETSTEREOMODE_ARGS;

// 0x4F07, 0x06 - Swap Planes -------------------------------------
// Refer Bug# 1194675

#define SwapPlanes_FuncCode (0x4F07)

// swap planes args structure
typedef struct _SB_SWAPPLANES_ARGS
{
    union {
        DDU32 ulPlaneSwap;

        struct
        {
            DDU32 bSwapPlaneAToPlaneB : 1;
            DDU32 bSwapPlaneBToPlaneA : 1;
            DDU32 bDisablePlaneAAfterSwap : 1;
            DDU32 bDisablePlaneBAfterSwap : 1;
            DDU32 bReservedSwapFlags : 28;
        };
    };

    DDU32 ulReserved;
} SB_SWAPPLANES_ARGS, *PSB_SWAPPLANES_ARGS;

// 0x4F15, 0x00 - Get DDC Caps ----------------------------------------------

#define GetDDCCaps_FuncCode (0x4F15)
#define GetDDCCaps_SubFunc (0x00)

// VBE DDC CAPS structure
typedef struct _VBE_DDC_CAPS
{
    UCHAR bDDC1 : 1;          // DDC1 supported
    UCHAR bDDC2_A0 : 1;       // DDC2 supported at I2C address A0 (128 Bytes)
    UCHAR bScreenBlanked : 1; // Screen blanked during data transfer
    UCHAR bDDC2_A2 : 1;       // DDC2 supported at I2C address A2 (256 Bytes)
    UCHAR bDDC2_A6 : 1;       // DDC2 supported at I2C address A6 (256 Bytes)
    UCHAR bReserved : 2;
    UCHAR bMultiplePorts : 1; // Multiple video ports supported
} VBE_DDC_CAPS;

// Get DDC caps args structure
typedef struct _SB_GETDDCCAPS_ARGS
{
    IN PVOID pReserved; // ???? Do we really need this???
    OUT union {
        DDU32 ulDdcCaps;
        struct
        {
            VBE_DDC_CAPS VbeDdcCaps;
            UCHAR        ucXferTime;
        };
    };
    OUT PVOID pEdidOut;
} SB_GETDDCCAPS_ARGS, *PSB_GETDDCCAPS_ARGS;

// 0x4F15, 0x01 - Get DDC EDID ----------------------------------------------

#define GetDDCEdid_FuncCode (0x4F15)
#define GetDDCEdid_SubFunc (0x01)
#define GetCloneModeList_FuncCode (0x4F15)
#define GetCloneModeList_SubFunc (0x03)

#define EDID_BLOCK_SIZE (128)

typedef union _DISPLAY_EDID_POLICY_IN_CLONE // Used for DDC
{
    DDU16 usPolicy;
    struct
    {
        IN unsigned bActiveEDIDRead : 1;       // If 1 then EDID is read from DDC pin else read from cache.
        IN unsigned bX_Y_Bpp_Intersection : 1; // Policy : 1- X,Y,Bpp Intersection ; 0- X,Y,Bpp Union
        IN unsigned bRR_Intersection : 1;      // Policy : 1- RR Intersection ; 0- RR Union
        unsigned    bReserved : 13;
    };
} DISPLAY_EDID_POLICY_IN_CLONE;

// Get DDC EDID args structure
typedef struct _SB_GETDDCEDID_ARGS
{
    IN DDU32 ulDisplayUID;   // Unique display identifier
    IN BOOLEAN bForceRead;   // If TRUE, read DDC/EDID from device
                             // FALSE, return DDC/EDID from PAIM_DEVICE
    IN DDU32 ulEdidSize;     // EDID data size
    OUT BOOLEAN bFakeEdid;   // The edid sent is fake or not
    IN DDU32 ulAddress;      // For example, 0xA0, 0xA2,...
    IN DDU32 ulEdidBlockNum; // 0 = EDID Block
    IN_OUT UCHAR EdidData[EDID_BLOCK_SIZE];
} SB_GETDDCEDID_ARGS, *PSB_GETDDCEDID_ARGS;

// Get clone caps args structure
typedef struct _SB_GETCLONECAPS_ARGS
{
    IN DDU32 ulDisplay1UID;                           // Unique display identifier 1
    IN DDU32 ulDisplay2UID;                           // Unique display identifier 2
    IN DISPLAY_EDID_POLICY_IN_CLONE stDispEDIDPolicy; // Policy Definitions in EDID read
    IN_OUT DDU32 EdidSize;
    IN_OUT UCHAR EdidData[EDID_BLOCK_SIZE * 2];
} SB_GETCLONECAPS_ARGS, *PSB_GETCLONECAPS_ARGS;

// 0x5F00 - Get Controller Information --------------------------------------

#define GetControllerInfo_FuncCode (0x5F00)

// Get controller infor args structure
typedef struct _SB_GETCONTROLLERINFO_ARGS
{
    OUT DDU16 usChipDeviceID;      // Device ID of the controller
    OUT DDU16 usChipVendorID;      // Vendor ID of the controller
    OUT DDU16 usSubsystemDeviceID; // Subsystem Device ID of the controller
    OUT DDU16 usSubsystemVendorID; // Subsystem vendor ID of the controller
    OUT UCHAR ulChipRevisionID;    // Revision ID of the controller
                                   // OUT PVOID   pDeviceInfo;  // Not used by any one!
} SB_GETCONTROLLERINFO_ARGS, *PSB_GETCONTROLLERINFO_ARGS;

// 0x5F01 - Get ROM BIOS Information --------------------------------------

#define GetRomBIOSInfo_FuncCode (0x5F01)

typedef enum _SB_VERSION_TYPE
{
    SB_VBIOSVersion = 0,
    SB_GOPVersion
} SB_VERSION_TYPE;
// Get ROM BIOS info args structure
typedef struct _SB_GETROMBIOSINFO_ARGS
{
    OUT UCHAR ucBuildNum[32]; // Build number for BIOS
                              // VBIOS version will be sent by BIOS as a number(4 Bytes).
                              // GOP version will be sent by BIOS as a string.
                              // RCR # 1024086
                              // Variable added for Minor Version of VBIOS.
    OUT UCHAR ucMinorVersion;
    // Variable added for indicating that the minor version number is invalid
    OUT BOOLEAN bInvalidMinorVersion;
    OUT SB_VERSION_TYPE versionType;
} SB_GETROMBIOSINFO_ARGS, *PSB_GETROMBIOSINFO_ARGS;

// 0x5F05 - Get Supported Refresh Rates -------------------------------------

#define GetRefreshRate_FuncCode (0x5F05)

//  Maximum possible refresh rates for any given mode.
//  In the future, when this number is not enough, simply update it a larger
//  number and re-build the driver.
#define MAX_NUM_REFRESH_RATES 32

// Get refresh rate args structure
typedef struct _SB_GETREFRESHRATE_ARGS
{
    IN DDU32 ulDisplayUID; // Display Device UID
    IN MODE_INFO ModeInfo; // Mode info structure
    IN BOOLEAN bRetrieveSeamlessMediaMode;
    OUT DDU32 ulNumRefreshRates; // Number of refresh rates
    OUT UCHAR ucRefreshRates[MAX_NUM_REFRESH_RATES];
} SB_GETREFRESHRATE_ARGS, *PSB_GETREFRESHRATE_ARGS;

// 0x5F06 - Get Timing Info Data -------------------------------------

#define GetTimingInfo_FuncCode (0x5F06)
// MODE_TIMINGFLAGS used in the MODE_TIMINGINFO structure
typedef struct _MODE_TIMINGFLAGS
{
    union {
        DDU32 ulFlags;
        struct
        {
            unsigned bDoubleScan : 1;     // Bit 0, 1 = Graphics Mode is Double Scanned
            unsigned bInterlaced : 1;     // Bit 1, 1 = Interlaced Mode
            unsigned bHSyncPolarity : 1;  // Bit 2, 1 = H. Sync Polarity is Negative going pulse
            unsigned bVSyncPolarity : 1;  // Bit 3, 1 = V. Sync Polarity is Negative going pulse
            unsigned bCompatible : 1;     // Bit 4, Selects 1.xV (0) or 3.3V (1) mode
            unsigned bDoubleWideMode : 1; // Bit 5, 1 = Two ports used as one
            unsigned bOddEven : 2;        // Bit 6, For Double Wide Mode
                                          //  0 = Upper/Lower Mode : DVO-B High, DVO-C Low
                                          //  1 = Odd/Even Mode : DVO-B Even, DVO-C Odd
                                          //  2 = Upper/Lower Mode : DVO-B Low, DVO-C High
                                          //  3 = Odd/Even Mode : DVO-C Even, DVO-B Odd
            unsigned ucCharWidth : 8;     // Bit 8, Bits per Characters for Text Mode
            unsigned bStereo : 1;         // Bit 16, 1 = Stereo Buffer Flipping Enabled
            unsigned bStereoPolarity : 1; // Bit 17, 1 = Set Stereo Output Signal High on the First Frame
            unsigned bBypassMode : 1;     // Bit 18,
            unsigned bField : 1;          // Bit 19, Codec requires Field signal on DVO
            unsigned bStall : 1;          // Bit 20, Codec requires use of Stall signal
            unsigned bBlankPolarity : 1;  // Bit 21, Blank Polarity 1 = Active High, 0 = Active Low
            unsigned bDataOrder : 1;      // Bit 22, 1 = BGGR (i740 Ordering), 0 = RGGB DVOData Ordering
            unsigned bClockDouble : 1;    // Bit 23, 0 = 1x Multiplier, 1 = 2x Multiplier
            unsigned bClockSource : 1;    // Bit 24, 0 = GMCH generates dot clock, 1 = DVO codec supplies dot clock reference
            unsigned bClockSelection : 2; // Bit 25, Selects which one of a number of possible clocks
                                          //  0 = Standard
                                          //  1 = Spread-Spectrum 1
                                          //  2~3 = Reserved For Use
            unsigned ucStretching : 3;    // Bit 27, Panel Stretching
                                          //  0 = Don't update
                                          //  1 = Text modes only
                                          //  2 = Graphics mode modes only
                                          //  3 = Extended graphics modes only
                                          //  4 = VGA modes only
                                          //  5 = Extended modes only
            unsigned bPanning : 1;        // Bit 30, 1 = Panning enabled, 0 = disabled
            unsigned bDataSubOrder : 1;   // Bit 31, 1 = Reversed (GBRG), 0 = Normal (RGGB)
        };
    };
    union {
        DDU32 ulExtendedFlags;
        struct
        {
            unsigned ucPixelReplication : 5; // Pixel replication associated with the timing, 0=non-replicated timing
            unsigned bDeepColorTiming : 1;   // Will be set if the timing is updated for Deep color.
            unsigned ucY420Capability : 2;   // Bit 6, Y420 Capability
                                             //  0 = Not a Y420 Sampling Mode
                                             //  1 = Supports Only Y420 Sampling
                                             //  2 = Supports Y420 with other Sampling modes
            unsigned ulReserved : 24;        // Reserved bits
        };
    };
} MODE_TIMINGFLAGS;

typedef struct _MODE_UID
{
    UCHAR ucRefreshRate; // Refresh rate up to 256 Hz
    BOOL  bInterlaced;   // 1 = Interlaced mode; 0 = Non.
    DDU16 usYResolution; // Y/2 resolution up to 4096 pixels
    DDU16 usXResolution; // X/2 resolution up to 4096 pixels
} MODE_UID, *PMODE_UID;

//  Definition of _MODE_TIMINGINFO data structure
typedef struct _MODE_TIMINGINFO
{
    DDU32            dwSize;        // Size of the _TIMING_INFO Structure
    DDU32            dwDotClock;    // Pixel clock in Hz
    DDU32            dwHTotal;      // Horizontal total in pixels
    DDU32            dwHActive;     // Active in pixels
    DDU32            dwHBlankStart; // From start of active in pixels
    DDU32            dwHBlankEnd;   // From start of active in pixels
    DDU32            dwHSyncStart;  // From start of active in pixels
    DDU32            dwHSyncEnd;    // From start of active in pixels
    DDU32            dwHRefresh;    // Refresh Rate
    DDU32            dwVTotal;      // Vertical total in lines
    DDU32            dwVActive;     // Active lines
    DDU32            dwVBlankStart; // From start of active lines
    DDU32            dwVBlankEnd;   // From start of active lines
    DDU32            dwVSyncStart;  // From start of active lines
    DDU32            dwVSyncEnd;    // From start of active lines
    DDU32            dwVRefresh;    // Refresh Rate
    MODE_TIMINGFLAGS flFlags;       // Timing Flags e.g. Selects 1.xV or 3.3V mode
    UCHAR            ucEncMode;
    DDU32            ulSupportedBPCForY420Mode;
    DDU32            ulSupportedBPCForTiming;
} MODE_TIMINGINFO, *PMODE_TIMINGINFO;
typedef enum _SB_GETTIMINGINFO_OPTIONS
{
    SB_MODETABLE_TIMING = 0,
    SB_HW_TIMING
} SB_GETTIMINGINFO_OPTIONS,
*PSB_GETTIMINGINFO_OPTIONS;

// Get timing info args structure
typedef struct _SB_GETTIMINGINFO_ARGS
{
    IN DDU32 ulSize;                                // Size of this structure
    IN DDU32 ulDisplayUID;                          // Display device ID
    IN MODE_INFO ModeInfo;                          // Requested mode
    IN SB_GETTIMINGINFO_OPTIONS eTimingInfoOptions; // 0 - Timing based on Modes, 1 - Currently programmed GMCH Timing
    OUT MODE_TIMINGINFO stTimingInfo;               // Mode timing information
    OUT BOOLEAN bLowResMode;                        // Note this will hold good only if Encoder is active
                             // The two variables ulXRes_TimingSelected & ulYRes_TimingSelected below indicate the Timing Resolutions Selected for any of the Scaling Option
                             // e.g: if user applies 10 X 7 Centered on 12 X 10 Panel,
                             // Mode_Info will be 10 X 7,
                             // stTimingInfo will be Timings related to 12 X 10 but HActives and Vactives will be Replaced by 10 X 7
                             // Hence ulXRes_TimingSelected X ulYRes_TimingSelected will be 12 X 10..Valid only when SB_GMCH_TIMING is the eTimingInfoOptions
    OUT DDU32 ulXRes_TimingSelected;
    OUT DDU32 ulYRes_TimingSelected;

    OUT DDU32 ulCDClk;       // get current CD clock value in Hz
    OUT DDU32 ulAdjPixelClk; // adjusted pixel clock in Hz after Downscaling, PF_ID in case of SB_HW_TIMING info
} SB_GETTIMINGINFO_ARGS, *PSB_GETTIMINGINFO_ARGS;

// 0x5F07 - Get Closest Supported Mode --------------------------------

#define GetClosestSupportedMode_FuncCode (0x5F07)
// Value definitions for bPreference
#define PREFER_LARGER_SAME_RR 1
#define PREFER_SMALLER_SAME_RR 2
#define PREFER_LARGER 3
#define PREFER_SMALLER 4
#define PREFER_INTERLACED 5
#define PREFER_SAMEXY_SMALLER_RR 6
#define PREFER_SAMEXY_LARGER_RR 7

// get closest supported mode args structure
typedef struct _SB_GETCLOSESTSUPPORTEDMODE_ARGS
{
    IN DISPLAY_LIST stDisplayList; // Display device ID list
    IN_OUT MODE_INFO Mode_Info;    // In = Curr Mode
                                   // Out = Closest Mode
    IN struct
    { // Options;
        unsigned bNoDoubleWideModes : 1;
        unsigned bPreference : 3; // See value definitions above
        unsigned bReserved : 28;
    };
} SB_GETCLOSESTSUPPORTEDMODE_ARGS, *PSB_GETCLOSESTSUPPORTEDMODE_ARGS;

// 0x5F10 - Get Linear Buffer Data ------------------------------------------
//
// The direct and CPU register interfaces of this function do not have a one
// to one correspondence.

#define GetDisplayMemInfo_FuncCode (0x5F10)

// Get display memory details args structure
typedef struct _SB_GETDISPLAYMEM_ARGS
{
    OUT DDU32 ulAvailableMemSize; // Available memory size
    OUT DDU32 ulLocalMemSize;     // Local memory size
    OUT DDU32 ulTotalUMAMemSize;  // Total UMA memory size
} SB_GETDISPLAYMEM_ARGS, *PSB_GETDISPLAYMEM_ARGS;

// 0x5F11 - Set Video Memory Size available to VBIOS ------------------------

#define SetVBIOSVidMemSize_FuncCode (0x5F11)

// Set video memory size args structure
typedef struct _SB_SETVIDMEMSIZE_ARGS
{
    IN DDU32 ulVBIOSVidMemSize; // in 4K Bytes granularity
} SB_SETVIDMEMSIZE_ARGS, *PSB_SETVIDMEMSIZE_ARGS;

// 0x5F28 - Get mode support ------------------------------------------------

#define GetModeSupport_FuncCode (0x5F28)
typedef enum _PORTPAIR_TYPE
{
    PORTPAIR_UNDEFINED = -1,
    PORTPAIR_INACTIVE  = 0,
    PORTPAIR_ACTIVE    = 1
} PORTPAIR_TYPE,
*PPORTPAIR_TYPE;
//  Display enumeration policy data structure
typedef struct _DISPLAY_POLICY
{
    union {
        DDU16 usPolicy;
        struct
        {
            IN_OUT unsigned bEncoderOverridePolicy : 1;  // Policy : Ignore encoder, (e.g. Hot-Plug ADD2 Cards)
            IN_OUT unsigned bDisplayOveridePolicy : 1;   // Policy : Ignore detection, always pretend it's there
            OUT unsigned    bDisplayEnablePolicy : 1;    // Policy : can display be enabled e.g. Lid Switch
            IN_OUT unsigned bActiveDetectionPolicy : 1;  // Policy : Does actively detect display devices
            IN_OUT unsigned bLegacyDetectionPolicy : 1;  // Policy : Checks for CRT using Legacy Analog detection
            OUT unsigned    bNoPruneFrequency : 1;       // Policy : Indication to miniport that VIDEO_CHILD_NOPRUNE_FREQ should be
                                                         //          set in IOCTL_VIDEO_GET_CHILD_STATE call if OS is XP (out/read only)
            OUT unsigned bNoPruneSize : 1;               // Policy : Indication to miniport that VIDEO_CHILD_NOPRUNE_RES should be
                                                         //          set in IOCTL_VIDEO_GET_CHILD_STATE call if OS is XP (out/read only)
            IN unsigned bForceActiveDetectionPolicy : 1; // Policy : Does forceful active detection of display devices, used along with ActiveDetectionPolicy.
            IN unsigned bForceEDIDReadDetection : 1;     // Policy to do active detection through raw edid read ignoring live status

            IN unsigned bVirtualDVI : 1;

            unsigned bReserved2 : 6;
        };
    };

    PORTPAIR_TYPE ePortPairPolicy;
} DISPLAY_POLICY;

//  Display device status data structure
typedef struct _DISPLAY_DEVICE_STATUS
{
    union {
        DDU16 usStatus;
        struct
        {
            OUT unsigned bEncoderAttached : 1; // Encoder h/w is present
            OUT unsigned bDisplayAttached : 1; // Display Device detected attached to encoder
            OUT unsigned bDisplayActive : 1;   // Current state Active = TRUE, Inactive = FALSE
            OUT unsigned bHasEdid : 1;         // to inidcate EDID is retrieved or not.
            unsigned     bReserved1 : 12;      // Reserved bits
        };
    };

    DISPLAY_POLICY stPolicy;

    UCHAR ucEDIDHash; // Hash of EDID if present, else 0

    IN_OUT DDU32 ulDisplayUID;
} DISPLAY_DEVICE_STATUS, *PDISPLAY_DEVICE_STATUS;
typedef struct _TPV_PIPE_DISPLAYS_ESC_LIST
{
    DDU32 ulMaxTPVPipes;        // This will indicate the number of TPV Pipes that can exist.
                                // The belowe Pointers pPipeSelect & pDisplayList will be used as array ranging from 0 to (ulMaxTPVPipes - 1)
    DDU32 TPVPipeSelect;        // This will indicate which of the TPV Pipes are selected...
    DDU32 TPVDisplayListOffset; // This will indicate the Display List per TPV Pipe
} TPV_PIPE_DISPLAYS_ESC_LIST, *PTPV_PIPE_DISPLAYS_ESC_LIST;

typedef struct _PIPE_DISPLAYS_ESC
{
    BOOLEAN                    bIntelPipeSelectList[MAX_PHYSICAL_PIPES];
    DISPLAY_LIST               stIntelDisplayList[MAX_PHYSICAL_PIPES];
    TPV_PIPE_DISPLAYS_ESC_LIST stTPVPipeDisplayList;
} PIPE_DISPLAYS_ESC, *PPIPE_DISPLAYS_ESC;

// Get mode support args structure
typedef struct _SB_GETMODESUPPORT_ARGS
{
    IN MODE_INFO stIntelPipeMode[MAX_PHYSICAL_PIPES];
#if LHDM || SB_NAPA_ULT
    IN MONITOR_MODE_INFO stIntelPipeMonitorMode[MAX_PHYSICAL_PIPES];
#endif
    IN PMODE_INFO pTPVPipeMode; // Expeceted to be allocated by teh caller..
    IN OUT PIPE_DISPLAYS stPipeDisplay;
    IN DDU32 ulNumDisplays; // Valid entries in stDisplayDeviceStatus
    IN DISPLAY_DEVICE_STATUS stDisplayDeviceStatus[MAX_DISPLAYS];
    OUT UCHAR ucRequestedState;
    IN UCHAR ucValidateDevicesOnly;
    IN UCHAR ucScaling[MAX_PHYSICAL_PIPES]; // Scaling attribute for each of the Display
    OUT BOOLEAN bConfigChange;              // Config Change Requested
} SB_GETMODESUPPORT_ARGS, *PSB_GETMODESUPPORT_ARGS;

// Get mode support args structure
typedef struct _SB_GETMODESUPPORT_ESC_ARGS
{
    IN MODE_INFO stIntelPipeMode[MAX_PHYSICAL_PIPES];
#if LHDM || SB_NAPA_ULT
    IN MONITOR_MODE_INFO stIntelPipeMonitorMode[MAX_PHYSICAL_PIPES];
#endif
    IN OUT PIPE_DISPLAYS_ESC stPipeDisplay;
    IN DDU32 ulNumDisplays; // Valid entries in stDisplayDeviceStatus
    IN DISPLAY_DEVICE_STATUS stDisplayDeviceStatus[MAX_DISPLAYS];
    OUT UCHAR ucRequestedState;
    IN UCHAR ucValidateDevicesOnly;
    IN UCHAR ucScaling[MAX_PHYSICAL_PIPES]; // Scaling attribute for each of the Display
    OUT BOOLEAN bConfigChange;              // Config Change Requested
    IN MODE_INFO TPVPipeMode[1];            // Expeceted to be allocated by teh caller..
} SB_GETMODESUPPORT_ESC_ARGS, *PSB_GETMODESUPPORT_ESC_ARGS;

// 0x5F29 - Get mode information --------------------------------------------

#define GetModeInfo_FuncCode (0x5F29)

// Get mode info args structure
typedef struct _SB_GETMODEINFO_ARGS
{
    IN DISPLAY_LIST stDisplayList; // Display device ID list
    OUT DDU32 ulNumMode;           // Total number of modes
    union {
        DDU32 ulFlags;
        struct
        {
            IN DDU32 bDownScalarPrunning : 1;              // to prune as per Down Scalar logic in clone mode list for Vista only
            IN DDU32 bPruneCloneModeForNonEDIDDisplay : 1; // to prune as per device capability for non EDID CRT for Vista only
            IN DDU32 bEnumModesForPixelFormats : 1;        // to enum modes for all possible pixel formats
            IN DDU32 bEnumModesForHigherThan32Bpp : 1;     // to enum modes for Bpp more than 32bpp
            IN DDU32 bPruneModesbasedonMRL : 1;            // to prune modes if greater than display MRL
            IN DDU32 Reserved : 27;                        // Reserved for future use
        };
    };
    IN_OUT MODE_INFO stModeInfo[1];
} SB_GETMODEINFO_ARGS, *PSB_GETMODEINFO_ARGS;

// 0x5F61, 00 - Set Horizontal and Vertical Compensation -------------------

#define SetCompensation_FuncCode (0x5F61)

// SCALING SET OPTIONS - 'SET' INTERFACE.
//--------------------------------------

// The 'SET' interface is not similar to the 'GET' interface - since the set
// is usually performed on a particular display after it is enabled as part
// of a display configuration.
typedef SET_DISPLAY_COMPENSATION SB_SETCOMPENSATION_ARGS, *PSB_SETCOMPENSATION_ARGS;

/////////////////////////////// Lid State  /////////////////////////////
typedef enum _LID_STATE
{
    LID_OPENED = 0x0,
    LID_CLOSED = 0x1
} LID_STATE,
*PLID_STATE;

// get panel settings structure
typedef struct _SB_PANELSETTINGS_GET
{
    // Input panel index (0 by default)
    IN UCHAR ulPanelIndex; // 0 - Internal LVDS & 1 - sDVO LVDS (on mobile)
                           // 0 - sDVO LVDS (on desktop)

    // Lid Sate
    OUT LID_STATE eLidState;
} SB_PANELSETTINGS_GET, *PSB_PANELSETTINGS_GET;

// 0x5F61, 01 - Get Horizontal and Vertical Compensation -------------------

#define GetCompensation_FuncCode (0x5F61)
#define GetCompensation_SubFunc (0x01)

// SCALING GET OPTIONS - 'GET' INTERFACE.
//--------------------------------------
typedef GET_DISPLAY_COMPENSATION SB_GETCOMPENSATION_ARGS, *PSB_GETCOMPENSATION_ARGS;

// 0x5F63 - Adapter Power State ---------------------------------------------

#define AdapterPowerState_FuncCode (0x5F63)

typedef enum _DEVICE_STATE_CHANGE_REASON
{
    DEV_STATE_CHANGE_REASON_SYSTEM_STATE_CHANGE = 0x0,
    DEV_STATE_CHANGE_REASON_DC9_ENTRY,
    DEV_STATE_CHANGE_REASON_DC9_EXIT
} DEVICE_STATE_CHANGE_REASON;

// Adapter power state args structure
typedef struct _SB_ADAPTERPOWERSTATE_ARGS
{
    IN DDU32 ulPowerState; // See DEV_POWER_STATE for details
    IN DDU32 ulSystemState;
    IN DDU32 ulActionType; // This is needed to distinguish between Adapater CS call during monitor turn off(S0) and S3 call
    IN DEVICE_STATE_CHANGE_REASON eReason;
} SB_ADAPTERPOWERSTATE_ARGS, *PSB_ADAPTERPOWERSTATE_ARGS;

// 0x5F64, 0x00 - Set display device ----------------------------------------
//
#define SetDisplayDevice_FuncCode (0x5F64)

enum
{
    DISPLAY_PLANE_VGA = 0,
    DISPLAY_PLANE_A   = PLANE_A,
    DISPLAY_PLANE_B
};

typedef struct _SB_FUTURE_DISPLAY_CONFIG_INFO_ESC
{
    IN BOOLEAN bValid; // Indicates if valid data has been filled in this structure

    IN PIPE_DISPLAYS_ESC stPipeDisplays;

    // display Planes asscociated with a pipe
    IN UCHAR ucDisplayPlaneToPipe[MAX_PHYSICAL_PIPES];

    // Flag Added for indicating power state transitions
    IN UCHAR bPowerStateTransition;
} SB_FUTURE_DISPLAY_CONFIG_INFO_ESC, *PSB_FUTURE_DISPLAY_CONFIG_INFO_ESC;

typedef struct _SB_SETDISPLAYDEV_ESC_ARGS
{
    IN DDU32 ulSize; // Fixed size of Args !

    IN union {
        UCHAR ucOptions;
        struct
        {
            IN UCHAR ucForceExecute : 1;           // Bit0
            IN UCHAR ucDoNotTurnOffPanelPower : 1; // Bit1
            UCHAR    ucReserved : 6;               // Bits 2..7
        };
    };

    IN PIPE_DISPLAYS_ESC stPipeDisplays;

    // Display Planes asscociated with a pipe
    IN UCHAR ucDisplayPlaneToPipe[MAX_PHYSICAL_PIPES];

    IN SB_FUTURE_DISPLAY_CONFIG_INFO_ESC stFutureTopologyInfo;

    IN BOOLEAN bUpdateScratchPadRegs;
} SB_SETDISPLAYDEV_ESC_ARGS, *PSB_SETDISPLAYDEV_ESC_ARGS;

// 0x5F64, 0x01 - Get display device ----------------------------------------

#define GetDisplayDevice_FuncCode (0x5F64)
#define GetDisplayDevice_SubFunc (0x01)

// get display device args structure
typedef struct _SB_GETDISPLAYDEV_ARGS
{
    IN_OUT DDU32 ulSize; // Fixed size of Args !
    OUT PIPE_DISPLAYS stPipeDisplays;
    IN BOOLEAN bGMCHConfigOnly;
} SB_GETDISPLAYDEV_ARGS, *PSB_GETDISPLAYDEV_ARGS;

// get display device args structure
typedef struct _SB_GETDISPLAYDEV_ARGS_ESC
{
    IN_OUT DDU32 ulSize; // Fixed size of Args !
    OUT PIPE_DISPLAYS_ESC stPipeDisplays;
    IN BOOLEAN bGMCHConfigOnly;
} SB_GETDISPLAYDEV_ARGS_ESC, *PSB_GETDISPLAYDEV_ARGS_ESC;

// 0x5F64, 0x04 - Get display device detect ---------------------------------

#define GetDisplayDetect_FuncCode (0x5F64)
#define GetDisplayDetect_SubFunc (0x04)

// get display detect args structure
typedef struct _SB_GETDISPLAYDETECT_ARGS
{
    IN DDU32 ulSize;            // Fixed size of Args !
    IN_OUT DDU32 ulNumDisplays; // Valid entries in stDisplayDeviceStatus
    IN_OUT DISPLAY_DEVICE_STATUS stDisplayDeviceStatus[MAX_DISPLAYS];
    IN_OUT BOOLEAN bFakeCRT;         // Flag added for indicating fake CRT being reported by the driver.
    IN BOOLEAN bEnumOnlyTPVDisplays; // This works only when the ulNumDisplays is Set to Zero. Setting ulNumDisplays to Zero indicates that enumerate all Displays.
} SB_GETDISPLAYDETECT_ARGS, *PSB_GETDISPLAYDETECT_ARGS;

// 0x5F64, 0x05 - Get display device information ----------------------------

#define GetDisplayInfo_FuncCode (0x5F64)
#define GetDisplayInfo_SubFunc (0x05)

// Indicates the refresh-rate switching capabilities of the encoder for a given platform
typedef struct _ENCODER_RR_SWITCHING_CAPS
{
    BOOLEAN bIsHAMAMBasedDRRSSupported;      // HW based p<->p seamless switching in Big FIFO mode
    BOOLEAN bIsSWSeamlessBasedDRRSSupported; // SW based p<->p seamless switching
} ENCODER_RR_SWITCHING_CAPS, *PENCODER_RR_SWITCHING_CAPS;

typedef enum _SB_DP_VOLTAGE_SWING_LEVEL
{
    SB_e0_4 = 0,
    SB_e0_6,
    SB_e0_8,
    SB_e1_2
} SB_DP_VOLTAGE_SWING_LEVEL;

typedef enum _SB_DP_PREEMPHASIS_LEVEL
{
    SB_eNoPreEmphasis = 0,
    SB_e3_5dB,
    SB_e6dB,
    SB_e9_5dB
} SB_DP_PREEMPHASIS_LEVEL;

//#pragma pack (1)
typedef struct _CURRENT_CAPABILITIES_BLOCK
{
    unsigned bMaxFrameHeight : 16;
    unsigned bMaxFrameWidth : 16;
    unsigned bMaxFrameSize : 24;
    unsigned bMaxFrameRate : 8;
    unsigned bColorDepthSupportedRGB : 8;
    unsigned bColorDepthSupportedYCbCr : 16;
    unsigned bMaxPixelClock : 16;
    unsigned bMaxStreamsSupported : 7;
    unsigned bS3DFormatsSupported : 16;
    unsigned bOtherUnspecifiedCapabilityExists : 1;
    UCHAR    ucMinFrameRate;
} CURRENT_CAPABILITIES_BLOCK, *PCURRENT_CAPABILITIES_BLOCK;
//#pragma pack()

typedef struct _DISPLAY_PORT_BW_INFO_ST
{
    UCHAR                      ucMaxLinkRate;   // As reported by DPCD
    UCHAR                      ucMaxLaneCount;  // As reported by DPCD
    BOOLEAN                    bIsFLTSupported; // Only if true will the vswing and preemphasis values will be valid
    SB_DP_VOLTAGE_SWING_LEVEL  eFLTVswing;
    SB_DP_PREEMPHASIS_LEVEL    eFLTPremphasis;
    UCHAR                      bSpread;        // enable down spreading
    DDU32                      ulMaxStreamPBN; // Maximum PBN supported for One Stream
    DDU32                      ulMaxPortPBN;   // Maximum PBN Port can support
    UCHAR                      ucMaxBpc;       // Maximum BPC Supported
    CURRENT_CAPABILITIES_BLOCK stCCSBlock;
} DISPLAY_PORT_BW_INFO_ST, *PDISPLAY_PORT_BW_INFO_ST;

typedef union _SB_DISPLAY_BANDWIDTH_INFO {
    DISPLAY_PORT_BW_INFO_ST stDisplayPortDetails;
    // Add in future other port bw specific structures
} SB_DISPLAY_BANDWIDTH_INFO, *PSB_DISPLAY_BANDWIDTH_INFO;

// DISPLAY_DEVICE_CAPS_FLAG: Used by DISPLAY_DEVICE_CAPS struct
typedef union _DISPLAY_DEVICE_CAPS_FLAG {
    DDU16 ulDisplaysCaps;

    struct
    {
        OUT DDU16 bCEExtnDisplay : 1;               // Displays has CE Extentions
        OUT DDU16 bHDMIDisplay : 1;                 // Display has HDMI connector & is being driven by an HDMI enabled encoder
        OUT DDU16 bMultiRRDisplay : 1;              // LVDS supports multiple RRs
        OUT DDU16 bSeamlessDisplay : 1;             // LVDS supports Seamless multiple RRs
        OUT DDU16 bIsDPDisplay : 1;                 // Display has DP connector
        OUT DDU16 bIsAudioSupportedDisplay : 1;     // Display supports Audio
        OUT DDU16 bIsXVYCCSupportedDisplay : 1;     // Display supports Gamut profile transmission
        OUT DDU16 bIsCcflDisplay : 1;               // CCFL Display
        OUT DDU16 bIsLedDisplay : 1;                // LED Display
        OUT DDU16 bMSTEnabled : 1;                  // Boolean tells if Multistreaming is enabled
        OUT DDU16 ucSSTDongleDwnStreamPortType : 2; // 2-Bit BitMap to identify down stream port type in case of DP Dongles
        OUT DDU16 bAssertiveDisplay : 1;            // Indicates whether the display supports AD
        OUT DDU16 bIsTiledDisplay : 1;              // Indicates whether the display is Tiled Display
        OUT DDU16 bCustomModeSupported : 1;         // Indicates whether the display supports custom mode
        OUT DDU16 bHdrBT2020Display : 1;            // Indicates whether the display supports BT2020 HDR
                                                    // No reserved bits are available all 16 bits are used if needs to extend this structure need to be extended to DDU32
    };
} DISPLAY_DEVICE_CAPS_FLAG;

typedef struct _SB_UPDATE_ASSERTIVE_SETTINGS_ARGS
{
    IN DDU16 usLux;        // Luminance field used with the SB_AD_SET_LUMINANCE command
    IN DDU16 usBrightness; // Brightness field used with the SB_AD_SET_LUMINANCE command
} SB_UPDATE_ASSERTIVE_SETTINGS_ARGS, *PSB_UPDATE_ASSERTIVE_SETTINGS_ARGS;

// PSR CAP flags
typedef union _PSR_CAPS {
    DDU16 usPsrCaps;

    struct
    {
        OUT BOOLEAN bIsPsrDisplay : 1;   // PSR Support
        OUT BOOLEAN bIsSfuSupported : 1; // Single update supported
        OUT BOOLEAN bIsSUSupported : 1;  // PSR2 Capability
        OUT DDU16 bReserved : 13;
    };
} PSR_CAPS;

// VRR CAP flags
typedef struct _VRR_CAPS
{
    BOOLEAN bSupportsVRR;
    DDU32   ulRRmin;
    DDU32   ulRRmax;
    DDU32   ulVMaxShift;
} VRR_CAPS, *PVRR_CAPS;

// MIPI capability flags
typedef union _MIPI_CAPS {
    DDU16 usMipiCaps;
    struct
    {
        OUT BOOLEAN bIsMipiDIsplay : 1;   // Is MIPI display
        OUT BOOLEAN bIsPwmThroughSOC : 1; // Is PWM coming through SOC (default is through PMIC)
        OUT BOOLEAN bIsDualLinkMIPI : 1;  // Is Dual link MIPI panel
        OUT DDU16 bReserved : 13;
    };
} MIPI_CAPS;

typedef struct _COMPRESSION_CAPS
{
    OUT BOOLEAN bCompressionSupported;
    DDU16       usCompressionBPP;
} COMPRESSION_CAPS;

// Base Block edid display capabilities
// This gives the base block EDID caps
// In case of legacy it returns the max
// supported by legacy device
typedef struct _BASE_BLOCK_DEVICE_CAPS
{
    // Base block max caps
    OUT DDU16 usMaxBBVerticalRes;     // Maximum Base Block Vertical Res
    OUT DDU16 usMaxBBHorizontalRes;   // Maximum Base Block Horizontal Res
    OUT DDU16 usMaxBBRefreshRate;     // Maximum Base Block Refresh Rate
    OUT DDU32 ulMaxDotClockSupported; // Maximum Dot clock supported by the display.
    OUT DDU16 usMinBBRefreshRate;     // Min Base Block Refresh Rate
} BASE_BLOCK_DEVICE_CAPS, *PBASE_BLOCK_DEVICE_CAPS;

//
// Per color chromaticity corrdinat
//
typedef struct _SB_CHROMATICITY_COORDINATE
{
    // Valid values 0-1023
    // Actual floating value = SB returned value / 1024;
    // E.g. For a value of usXScaledBy1024 = 1001110001b (=625), actual X coordinate is 625/1024 (=0.6103515625)
    DDU16 usXScaledBy1024;
    DDU16 usYScaledBy1024;
} SB_CHROMATICITY_COORDINATE, *PSB_CHROMATICITY_COORDINATE;

//
// Display chormaticity details
//
typedef struct _SB_DISPLAY_CHROMATICITY_DETAILS
{
    // Narrow Gamut Enabled
    OUT BOOLEAN bNarrowGamutChromacitySupported;

    OUT BOOLEAN bOverrideEDIDChromaticityValues;
    // Indicates sRGB/601/709/xvYCC709/xvYCC601 etc.
    OUT SB_COLORSPACE_TYPES eDisplayColorSpace;

    // Chromaticity details for red/green/blue/white point
    // Valid iff eDisplayColorSpace != eInvalidSpace
    OUT SB_CHROMATICITY_COORDINATE Red;

    OUT SB_CHROMATICITY_COORDINATE Green;

    OUT SB_CHROMATICITY_COORDINATE Blue;

    OUT SB_CHROMATICITY_COORDINATE White; // white point
} SB_DISPLAY_CHROMATICITY_DETAILS, *PSB_DISPLAY_CHROMATICITY_DETAILS;

typedef enum _SB_PWM_TYPE
{
    PWM_TYPE_EXTERNAL = 0,
    PWM_TYPE_I2C,
    PWM_TYPE_EXTERNAL_INTERNAL,
    ePWM_TYPE_Reserved
} SB_PWM_TYPE,
*PSB_PWM_TYPE;

// The following enum is synchronized with GOP/VBIOS
// Any changes here needs to be made with corresponding changes to GOP/VBIOS
typedef enum _SB_PWM_CTRL_TYPE
{
    PWM_CTRL_TYPE_UNDEFINED = -1,
    PWM_CTRL_TYPE_PMIC,         // Unused: PWM source is from PMIC - Remove in GOP/VBIOS first
    PWM_CTRL_TYPE_SOC,          // Unused: PWM source is from LPSS/PMC module (non-IGD based) - Remove in GOP/VBIOS first
    PWM_CTRL_TYPE_INTERNAL_IGD, // PWM source is within display controller
    PWM_CTRL_TYPE_PANEL_CABC,   // PWM source is on the display panel (CABC supported ones)
    PWM_CTRL_TYPE_PANEL_DRIVER  // PWM source is through external Panel driver
} SB_PWM_CTRL_TYPE,
*PSB_PWM_CTRL_TYPE;

typedef enum _SB_PMIC_PWM_CTRL_NUM
{
    PWM_NUM0 = 0,
    PWM_NUM1,
    PWM_NUM2,
    PWM_NUM3
} SB_PWM_CTRL_NUM,
*PSB_PWM_CTRL_NUM;

typedef struct _SB_DISPLAY_PWM_CAPS
{
    OUT SB_PWM_TYPE ePWMType; // To be obsoleted. Same as ucBlcType
    OUT SB_PWM_CTRL_TYPE ePWMControllerType;
    OUT SB_PWM_CTRL_NUM ePWMControllerNumber;
    // UCHAR  ucBlcType;           // BLC Inverter Type // Same as ePWMType
    UCHAR ucBlcPolarity;   // BLC Inverter Polarity
    DDU16 usBlcFrequency;  // BLC Inverter Frequency (PWM)
    UCHAR ucMinBrightness; // Minimum Brightness, 0 - 255
} SB_DISPLAY_PWM_CAPS, *PSB_DISPLAY_PWM_CAPS;

//  Display device Capability data structure
typedef struct _DISPLAY_DEVICE_CAPS
{
    OUT DDU16 usVerticalRes;   // Maximum Vertical Res
    OUT DDU16 usHorizontalRes; // Maximum Horizontal Res
    OUT DDU16 usRefreshRate;   // Maximum Refresh Rate

    OUT DDU16 usNativeVRes;          // Native Vertical Res
    OUT DDU16 usNativeHRes;          // Native Horizontal Res
    OUT DDU16 usNativeRRate;         // Native Refresh Rate
    OUT BOOLEAN bIsNativeInterlaced; // Native Interlaced flag

    // down scalar data
    OUT BOOLEAN bIsDSSupported;  // if the flag is set CUI will read from usDSVerticalRes instead of usVerticalRes
    OUT DDU16 usDSVerticalRes;   // Maximum Vertical Res for DS (40% more than native res of the panel)
    OUT DDU16 usDSHorizontalRes; // Maximum Horizontal Res for DS (40% more than native res of the panel)

    // if underscan values are zero, miniport has to take the native
    // values for initial boot requirement
    OUT DDU16 usUnderScanVRes;           // Vertica Under scan mode for HDMI
    OUT DDU16 usUnderScanHRes;           // Harizontal Under scan mode for HDMI
    OUT DDU16 usUnderScanRRate;          // Refresh Rate for unders scan mode
    OUT BOOLEAN bIsUnderScanInterlaced;  // Under scan mode for Interlaced flag
    OUT BOOLEAN bIsDownScalingSupported; // Downscaling supported flag

    OUT DISPLAY_DEVICE_CAPS_FLAG stDisplayCapability; // Display capability info
    OUT PSR_CAPS stPsrCapability;                     // PSR capability info
    OUT VRR_CAPS stVRRCapability;
    // Device base edid block device caps
    // Will be 0's in case of legacy display
    OUT BASE_BLOCK_DEVICE_CAPS stBaseBlockEdidCaps;

    // Chromaticy details
    OUT SB_DISPLAY_CHROMATICITY_DETAILS stChromaticyDetails;

    // Luminance details
    OUT VBT_LUMINANCE_AND_GAMMA stLuminanceAndGamma;

    // Get Supported BPC
    OUT UCHAR ucBitsPerColor; // for the EDID less panel issue

    // Get Display Gamma
    OUT UCHAR ucGamma;

    OUT MIPI_CAPS stMipiCaps;

    OUT COMPRESSION_CAPS stCompressionCaps;

    OUT SB_DISPLAY_PWM_CAPS stDispPWMCaps;
} DISPLAY_DEVICE_CAPS, *PDISPLAY_DEVICE_CAPS;
//#pragma pack(1)
// get display info args structure
typedef struct _SB_GETDISPLAYINFO_ARGS
{
    IN DDU32 ulSize; // Set to sizeof(SB_GETDISPLAYINFO_ARGS)

    IN DDU32 ulDisplayUID; // Unique ID or Generic UID e.g DISPLAY_ANY_CRT

    OUT BOOLEAN bTPVDrivenEncoder; // Introduced for CUI..

    // Display device status information
    OUT DISPLAY_DEVICE_STATUS stDisplayDeviceStatus;

    // Device capability info
    OUT DISPLAY_DEVICE_CAPS stDisplayDeviceCaps;

    // Display Device BW related information
    OUT SB_DISPLAY_BANDWIDTH_INFO stDisplayBandWidthInfo;

    // Tiled display info
    OUT DDU32 ulTileXRes;
    OUT DDU32 ulTileYRes;
    OUT UCHAR ucNoOfHTileDisplays;
    OUT UCHAR ucNoOfVTileDisplays;

    // Flag Specifying the return of Mode Caps
    // Only GRM will be using this flag in the CSLBASE_GetDisplayInfo ().
    // This will be set by GRM to get the Mode Caps for non-CRT devices.
    // For CRT, GRM will still be getting the Display Caps
    IN BOOLEAN bModeCaps;

    OUT ENCODER_RR_SWITCHING_CAPS stEncoderRrSwitchingCaps; // Indicates the refresh-rate switching capabilities of the chipset

    OUT BOOLEAN bLSPCONDonglePresent;
} SB_GETDISPLAYINFO_ARGS, *PSB_GETDISPLAYINFO_ARGS;
//#pragma pack()

// Structure that returns
typedef struct _SB_MPO_SCALING_STATUS_ARGS
{
    IN UCHAR ucPipeIndex;
    OUT BOOLEAN bScaling;
} SB_MPO_SCALING_STATUS_ARGS, *PSB_MPO_SCALING_STATUS_ARGS;

// Structure added for doing plane rotation
typedef struct _SB_PLANEORIENTATION_ARGS
{
    IN DDU32 ulStartAddress;
    IN DDU32 ulPlane;
    IN PLANE_ORIENTATION ePlaneOrientation;
    IN BOOLEAN bIsASynchMMIOFlip; // This is to indicate if its a Sync Flip. From Cantiga onwards, async Flip is handled in a more elegant way. Refer BSpec for more details.
    IN BOOLEAN bIsAsyncMMIOFlipWaitNeeded;
    IN SURFACE_MEM_OFFSET_INFO stSurfaceMemInfo;
    IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
} SB_PLANEORIENTATION_ARGS, *PSB_PLANEORIENTATION_ARGS;

// Arguments for MIPI Panel Frame Buffer Update
typedef struct _SB_PANEL_FRAME_BUFFER_UPDATE_ARGS
{
    IN DDU32 ulPipeIndex;
    IN BOOLEAN bVBlankDisable;
} SB_PANEL_FRAME_BUFFER_UPDATE_ARGS, *PSB_PANEL_FRAME_BUFFER_UPDATE_ARGS;

// Arguments for checking if command mode is active on current pipe
typedef struct _SB_COMMAND_MODE_ARGS
{
    IN DDU32 ulDisplayUID;
    OUT BOOLEAN bIsCommandMode;
} COMMAND_MODE_ARGS, *PCOMMAND_MODE_ARGS;

typedef struct _DISPLAY_PORT_DETAILS
{
    DDU32 ulDisplayUID;
    UCHAR ucNumberOfLanesUsed;
    UCHAR ucLinkSymbolClock; // Link symbol clock value "0xa" corresponds to 270MHz and "0x6" corresponds to 162MHz
    UCHAR ucBPC;
} DISPLAY_PORT_DETAILS, *PDISPLAY_PORT_DETAILS;

// Get scan line info Args Structure
typedef struct _SB_UPDATE_ROTATION_INFO_ARGS
{
    DDU32            ulPipeIndex; // pipe index
    PIPE_ORIENTATION orientation;
} SB_UPDATE_ROTATION_INFO_ARGS, *PSB_UPDATE_ROTATION_INFO_ARGS;

// Adding Custom Mode - Funcode --------------------------------
#define Custom_Mode_FuncCode (0x5F83)
// Func used for adding custom modes
#define Add_Custom_Mode_Info_SubFuncCode (0x00)
// Func used for getting already added custom modes for a particular display
#define Get_Custom_Mode_Info_SubFuncCode (0x01)
// Func used for getting timing for particular custom mode, user has specified
#define Get_Custom_Mode_Timing_SubFuncCode (0x02)
// Func used for removing custom modes added for a particular display
#define Remove_Custom_Mode_Info_SubFuncCode (0x03)

/*===========================================================================
; Structures for Custom Mode Addition thro' CUI
;--------------------------------------------------------------------------*/
// This enum is used in STANDARD_CUSTOM_MODE struct to specify the timing standard of the mode to be added.
typedef enum _SB_CUSTOM_MODE_TIMING_STD
{
    GTF_STD = 1,
    CVT_STD,
    CVT_RB_STD,
    CEA_861_B,
    CEA_861_D // New timing standard added as part of RCR 1023435
} CUSTOM_MODE_TIMING_STD;

// This enum is used to specify the type of custom mode while adding a custom mode or when CUI wants the custom modes of a particular type.
typedef enum _CUSTOM_MODE_TYPE
{
    STANDARD_CUSTOM_MODE_TYPE = 1,
    DETAILED_CUSTOM_MODE_TYPE,
    ANY_CUSTOM_MODE_TYPE
} CUSTOM_MODE_TYPE;

// Struct: STANDARD_CUSTOM_MODE
// This structure is used for standard custom modes added thro' CUI.
typedef struct _STANDARD_CUSTOM_MODE
{
    DDU16                  usXRes;           // X-resolution   Should be even & CUI checks for it.
    DDU16                  usYRes;           // Y-resolution...Should be even & CUI checks for it.
    UCHAR                  ucRRValue;        // Refresh rate
    UCHAR                  ucBppMask;        // Bpp mask : BIT 1 - 8bpp, 2 - 16bpp, 3 - 32bpp. Bit0 is reserved.
    UCHAR                  ucUnderScanPerct; // % to calculate underscanned mode.
    CUSTOM_MODE_TIMING_STD eTimingStd;       // Timing standard to be used for custom modes.
    union {
        UCHAR ucScanTypeMask;
        struct
        {
            UCHAR bInterlaced : 1; // 0 -- Progressive. 1 -- Interlaced.
            UCHAR ucReserved1 : 7;
        };
    };
} STANDARD_CUSTOM_MODE, *PSTANDARD_CUSTOM_MODE;

// Struct: _DETAILED_CUSTOM_MODE
// This structure is used for detailed custom modes added thro' CUI
typedef struct _DETAILED_CUSTOM_MODE
{
    UCHAR ucBppMask; // Bpp mask :BIT 1 - 8bpp, 2 - 16bpp, 3 - 32bpp. Bit0 is reserved..
    union {
        UCHAR ucPolarityMask;
        struct
        {
            UCHAR bHSyncPolarity : 1; // 1- -Ve, 0- +Ve.
            UCHAR bVSyncPolarity : 1; // 1 - -Ve, 0 - +Ve.
            UCHAR ucReserved : 6;
        };
    };

    union {
        UCHAR ucScanTypeMask;
        struct
        {
            UCHAR bInterlaced : 1; // 0 -- Progressive. 1 -- Interlaced.
            UCHAR ucReserved1 : 7;
        };
    };

    DDU16 usHActive; // Should be even & CUI checks for it.
    DDU16 usHFrontPorch;
    DDU16 usHBackPorch;
    DDU16 usHSyncWidth;
    DDU16 usHScanRate;

    DDU16 usVActive; // Should be even & CUI checks for it.
    DDU16 usVFrontPorch;
    DDU16 usVBackPorch;
    DDU16 usVSyncWidth;
    DDU16 usVScanRate;
} DETAILED_CUSTOM_MODE, *PDETAILED_CUSTOM_MODE;

// These error types are used to notify various error scenarios to CUI.
typedef enum _CUSTOMMODE_ERRORCODES
{
    CUSTOMMODE_NO_ERROR = 0,
    CUSTOMMODE_INVALID_PARAMETER,
    CUSTOMMODE_STANDARD_CUSTOM_MODE_EXISTS,
    CUSTOMMODE_DETAILED_CUSTOM_MODE_EXISTS,
    CUSTOMMODE_NON_CUSTOM_MATCHING_MODE_EXISTS,
    CUSTOMMODE_INSUFFICIENT_MEMORY,
    CUSTOMMODE_UNSUPPORTED_REFRESH_RATE, // used for LFP
    CUSTOMMODE_UNSUPPORTED_TIMING,
    CUSTOMMODE_UNDEFINED_ERROR_CODE
} CUSTOMMODE_ERRORCODES;

// Struct: _SB_EXISTING_CUSTOM_MODES
// This structure is used to send the info of any (Standard/Detailed) customized mode to CUI.
typedef struct _SB_EXISTING_CUSTOM_MODES
{
    CUSTOM_MODE_TYPE      eCustomModeType;
    DDU32                 ulNumberOfCustomModes;
    DDU32                 ulDisplayID;
    CUSTOMMODE_ERRORCODES eReturnValue;
    STANDARD_CUSTOM_MODE  pCustomModelist[1];
} SB_EXISTING_CUSTOM_MODES, *PSB_EXISTING_CUSTOM_MODES;

// Struct: _SB_ADD_CUSTOM_MODE
// This structure has the details of the custom mode to be added.
typedef struct _SB_ADD_CUSTOM_MODE
{
    CUSTOM_MODE_TYPE eCustomModeType;
    DDU32            ulDisplayID;
    union {
        UCHAR ucFlags;
        struct
        {
            UCHAR bForcedAddition : 1; // if set to 1, custom mode will be added forcefully.
            UCHAR ucReserved : 7;
        };
    };

    CUSTOMMODE_ERRORCODES eReturnValue;
    union {
        STANDARD_CUSTOM_MODE stStandardCustomMode;
        DETAILED_CUSTOM_MODE stDetailedCustomMode;
    };
} SB_ADD_CUSTOM_MODE, *PSB_ADD_CUSTOM_MODE;

// Struct: _SB_GET_CUSTOM_MODE_TIMING
// This structure is used by CUI for getting timing for the detailed mode already added by User.
typedef struct _SB_GET_CUSTOM_MODE_TIMING
{
    DDU32                 ulDisplayID;
    CUSTOMMODE_ERRORCODES eReturnValue;
    DETAILED_CUSTOM_MODE  stDetailedCustomMode;
} SB_GET_CUSTOM_MODE_TIMING, *PSB_GET_CUSTOM_MODE_TIMING;

// Esc Routine to update DP Parameters via DP Applet (Func : 0x5F95)

// Choose the sub function
typedef enum _SUB_FUNC_TYPE
{
    // Override DP parameters.  Parameters: -> ucLaneCount, ucLinkRate, ucVoltage, ucPreemphasis, bSSC
    eSetDPParam = 0,
    // Set DP PHY layer Test patterns.
    eSetPHYPattern = 1,
    // Set DP output Voltage Swing and pre emphasis level without performing any Link Training.
    // Parameters: -> ucVoltage, ucPreemphasis
    eSetDPParamWithoutLT = 2,
    // Enable Compliance Mode of Operation. Used for PHY layer testing with Scope connected.
    // Disables hot plug detection so that we can connect a scope after mode set without
    // disabling pipe/port. It also disables AUX transactions as Scope does not support AUX.
    // Parameters: -> NONE.
    eOnCompliance = 3,
    // Disables Compliance Mode of Operation. Enable HPD and AUX. Parameters: -> NONE.
    eOnNormal = 4,
    // Get current DP parameters programmed. Parameters: -> ucVoltage, ucPreemphasis, ucLaneCount, ucLinkRate.
    eGetDPParam = 5,
    // Does an Internal Mode set. VLV specific WA to Enable/Disable Display on Pipe B.
    eSetMode = 6,
    // Set Display Device on Pipe B. VLV specific WA to Enable/Disable Display on Pipe B.
    eDisableDisplay = 7
} SUB_FUNC_TYPE;

// Pattern Type
typedef enum _SB_DP_TRAINING_PATTERN
{
    eSBTrainingNotInProgress  = 0,
    eSBTrainingPattern1       = 1,
    eSBTrainingPattern2       = 2,
    eSBTrainingPattern3       = 3,
    eSBD102WithoutScrambling  = 4,
    eSBSymbolErrMsrCnt        = 5,
    eSBPRBS7                  = 6,
    eSBIdlePattern            = 7,
    eSBScramblingDisable      = 8,
    eSBHBR2EyeCompliance      = 9,
    eSBBits80Custom           = 10,
    eSBPCTPattern             = 11,
    eSBManchesterEncoding     = 12,
    eSBTrainingPattern4       = 13,
    eSBInvalidTrainingPattern = 0xff
} SB_DP_TRAINING_PATTERN;

typedef struct _SB_SINK_CAPABILITIES
{
    UCHAR                  ucLinkRate;
    UCHAR                  ucLaneCount;
    UCHAR                  ucVoltage;
    UCHAR                  ucPreemphasis;
    BOOLEAN                bSSC;
    SB_DP_TRAINING_PATTERN eTrainingPattern;
    SUB_FUNC_TYPE          eSubFuncType;
    DDU32                  ulDisplayID;
    MODE_INFO              ModeInfo;
    MODE_TIMINGINFO        stMonitorModeInfo;
    DDU32                  ulPipeIndex;
    DDU32                  ulSourceID;
    DDU32                  Reserved;
} SB_SINK_CAPABILITIES, *PSB_SINK_CAPABILITIES;

// struct used for providing info to the app. The dotclock deviation-direction flags are taken from registry.
typedef union _SB_PNM_FLAGS {
    DDU32 ulPNMflags;
    struct
    {
        DDU32 bDownwardDeviation : 1;   // Bit 0 When set, means deviation is -ve.
        DDU32 bUpwardDeviation : 1;     // Bit 1 When set, means deviation is +ve.
        DDU32 bSSCEnabled : 1;          // Bit 2 When set, app will send adaptive clocks for both SSC enabled and disabled cases.
        DDU32 bDualChannel : 1;         // Bit 3  0-Single Channel.  1-Dual Channel.
        DDU32 ulSSCSpreadDirection : 2; // Bit 4,5
        DDU32 ulReserved : 2;           // Bit 6-7
        DDU32 ulSpreadPerct : 4;        // Bit 8-11
        DDU32 ePanelPortType : 1;       // Bit 12
        DDU32 ulReserved1 : 19;         // Bit 13-31
    };
} SB_PNM_FLAGS, *PSB_PNM_FLAGS;

#define GetSetCSC_FuncCode (0x5F88)

#define SB_NUM_CSC_COEFFICIENTS 9
#define SB_CSC_MAX_MATRICES 4
#define SB_NUM_GE_LUT_COEFFICIENTS 17
#define SB_NUM_POSTCSC_COEFFICIENTS 3
#define SB_NUM_PRECSC_COEFFICIENTS 3

#define SB_IS_COLORGAMUT_SUPPORTED(pArg)                                                                                                       \
    (((((pArg)->eMatrixType == eCustomWideGamutMatrixType || (pArg)->eMatrixType == eCustomGamutLUTMatrix) && (pArg)->bIsWGFeatureSuported) || \
      ((pArg)->eMatrixType == eCustomNarrowGamutMatrixType && (pArg)->bIsNarrowGamutFeatureSuported)) ?                                        \
     TRUE :                                                                                                                                    \
     FALSE)
// 3x3 RGB transformation matrix representation which get's programmed into the CSC hardware
//
//              | R1/Y1      G1/U1      B1/V1|
//              |                            |
// RGB[3x3] =    | R2/Y2      G2/U2      B2/V2|  and is always multiplied by the data which comes in a vector format [3x1]
//              |                            |
//              | R3/Y3      G3/U3      B3/V3|
// The vector to be operated upon will be
// V[3x1] = | R |       | Y |
//          | G | or    | U |
//          | B |       | V |

// This enum is used to specify the type of operaton that needs to be performed by softbios to service requests from CUI
typedef enum _SB_CSC_OPERATION_TYPE
{
    GET_CSC_PARAMETERS = 1,
    SET_CSC_PARAMETERS,
} CSC_OPERATION_TYPE;

// Various mode's CSC can be in
typedef enum _SB_CSC_MODE_TYPE_ENUM
{
    eCSC_NotActive = 0,
    eCSC_Rgb_Yuv   = 1,
    eCSC_Rgb_Rgb   = 2,
    eCSC_Yuv_Rgb   = 3
    // In future we can have YUV_YUV
} SB_CSC_COLOR_FORMAT_TYPE_EN;

// Matrix type definition
// Enum definition of custom wide gamut CSC matrix offset
typedef enum _SB_CSC_WG_MATRIX_OFFSET_ENUM
{
    eCustomRGB601MatrixOffset = 0,
    eCustomRGB709MatrixOffset = 1,
    eCustomYUV601MatrixOffset = 2,
    eCustomYUV709MatrixOffset = 3,
    eMaxCustomWGMatrix
} SB_CSC_WG_MATRIX_OFFSET_EN;

// definition of types of matrix supported by GETSETCSC interface
typedef enum _SB_CSC_MATRIX_TYPE_ENUM
{
    eHueAndSaturationMatrixType  = 0,
    eCustomWideGamutMatrixType   = 1,
    eCustomGamutLUTMatrix        = 2,
    eCustomNarrowGamutMatrixType = 3,
    eMaxCSCMatrixType
} SB_CSC_MATRIX_TYPE_EN;

typedef enum _SB_CSC_CUSTOM_FLAG_EN
{
    eEnCustomCSCForDesktop         = 1,
    eEnCustomCSCForVideo           = 2,
    eEnCustomCSCForDesktopAndVideo = 3
} SB_CSC_CUSTOM_FLAG_EN;

typedef enum _SB_FLAG_STATUS
{
    eDisabled = 0,
    eEnabled  = 1,
    eDontCare = 2
} SB_FLAG_STATUS;

// Format conversion pamerter structure defn
typedef struct _SB_CSCUNIT_CONFIG_PARAMS
{
    // If for Hue And Saturation number of matrix should be eMaxHueAndSatMatrix
    // If for Custome WG number of matrix should be eMaxCustomWGMatrix
    IN OUT float flCSCCoefecients[SB_NUM_CSC_COEFFICIENTS]; // Contains the coefficients in the order as per CSC_COEFF_OFFSET_EN
    IN OUT SB_CSC_COLOR_FORMAT_TYPE_EN eCSCMode;
} SB_CSCUNIT_CONFIG_PARAMS, *PSB_CSCUNIT_CONFIG_PARAMS;

typedef struct _SB_CSC_CUSTOM_WG_PARAMS
{
    IN BOOLEAN bEnable; // This when set to true enables the WG loading
    IN OUT SB_CSC_CUSTOM_FLAG_EN eFlag;
    IN OUT float flCSCCoefecients[eMaxCustomWGMatrix][SB_NUM_CSC_COEFFICIENTS]; // WG Co-efficients
    IN OUT float flGELUTCoefficients[SB_NUM_GE_LUT_COEFFICIENTS];               // GE LUT Co-efficients
    IN BOOLEAN bEnableGamutExpansion;                                           // Enable/Disable Gamut Expansion
    OUT SB_DISPLAY_CHROMATICITY_DETAILS stChromaticityDetails;                  // Display chromaticiy details given in EDID
    OUT BOOLEAN bIsGamutExpansionEnabled;                                       // Will be true for WideGamut as well Narrow Gamut
} SB_CSC_CUSTOM_WG_PARAMS, *PSB_CSC_CUSTOM_WG_PARAMS;

// Struct: _SB_GET_SET_CSC_ARGS
// This structure provides a external interface to support
// CSC configuration via escape interface
typedef struct _SB_CSC_ARGS
{
    IN CSC_OPERATION_TYPE eCSCOperationType;
    IN DDU32 ulDisplayID;
    IN SB_CSC_MATRIX_TYPE_EN eMatrixType;

    // Feature caps reporte to CUI
    OUT BOOLEAN bCSCFeatureSupport;   // This flag indicates whether H&S is supported by platform/configuration
    OUT BOOLEAN bIsWGFeatureSuported; // This flag indicates wheteher Wide Gamut feature is supportedrted

    union {
        SB_CSCUNIT_CONFIG_PARAMS stConfigParams;   // Use this for normal get set csc
        SB_CSC_CUSTOM_WG_PARAMS  stCustomWGParams; // use this for custom wide gamut panel
    };
    OUT BOOLEAN bIsNarrowGamutFeatureSuported; // This Flag indicates if Narrow Gammut feature is supported
} SB_CSC_ARGS, *PSB_CSC_ARGS;

#define SB_CSC_FLAGS_ENABLE_CSC 0x1
#define SB_CSC_FLAGS_ENABLE_PRE_OFFSET 0x2
#define SB_CSC_FLAGS_ENABLE_POST_OFFSET 0x4
#define SB_CSC_FLAGS_ENABLE_PRE_CSC_GAMMA 0x8
#define SB_CSC_FLAGS_ENABLE_POST_CSC_GAMMA 0x10
#define SB_CSC_FLAGS_ENABLE_GAMMA_NONE 0x20

#define ONEDLUT_MAX_NUM_SAMPLES 1025

typedef struct _SB_DETAILED_OS_MODE
{
    DDU32           ulDisplayUid;
    DDU32           PixelClock;             // Pixel clock / 10000
    SCAN_LINE_ORDER eScanningType;          // Frame scanning type
    DDU16           HorizontalActivePixels; // Horizontal active image pixel number
    DDU16           HorizontalBlankPixels;  // Horizontal blank pixel number
    struct
    {
        DDU16 HorizontalFrontPorch : 15;  // Horizontal offset (front porch) pixel number
        DDU16 HorizontalSyncPolarity : 1; // Horizontal sync polarity
    };
    DDU16 HorizontalSyncWidth; // Horizontal sync pixel number
    DDU16 VerticalActiveLines; // Number of lines of vertical active image
    DDU16 VerticalBlankLines;  // Number of lines of vertical blank
    struct
    {
        DDU16 VerticalFrontPorch : 15;  // Number of lines of vertical offset (front porch)
        DDU16 VerticalSyncPolarity : 1; // Vertical sync polarity
    };
    DDU16 VerticalSyncWidth;
} SB_DETAILED_OS_MODE, *PSB_DETAILED_OS_MODE;

// struct to be used for adding Win7 additional target modes to SB mode list.
typedef struct _SB_ADD_WIN7_TARGET_MODE_ARGS
{
    DDU32                ulDisplayUid;
    DDU32                ulNumOfModes;
    PSB_DETAILED_OS_MODE pstDetailedOSMode;
} SB_ADD_WIN7_TARGET_MODE_ARGS, *PSB_ADD_WIN7_TARGET_MODE_ARGS;

typedef struct _SB_TPV_ENCODER_DISP_CAPS_INFO
{
    IN DDU32 ulDisplayUID;     // DisplayUID of the WiDi Encoder whose caps will be udpated.
    IN DDU32 ulScalingCaps;    // indicates scaling capabilities
    IN BOOL bIsMCCSSupported;  // indicates whether MCCS is supported by adapter or not
    IN BOOL bIsXVYCCSupported; // indicates whether xvYCC is supported or not
} SB_TPV_ENCODER_DISP_CAPS_INFO, *PSB_TPV_ENCODER_DISP_CAPS_INFO;

// HDMI / HDCP related
#define MAX_HDCP_DEVICES 127
#define KSV_SIZE 5
#define V_SIZE 20

#define RECEIVER_ID_SIZE 5
#define MAX_DEVICE_COUNT 31

typedef enum _HDCP2_MESSAGE_ID
{
    NULL_MESSAGE                      = 1,
    AKE_INIT                          = 2,
    AKE_SEND_CERT                     = 3,
    AKE_NO_STORED_KM                  = 4,
    AKE_STORED_KM                     = 5,
    AKE_SEND_H_PRIME                  = 7,
    AKE_SEND_PAIRING_INFO             = 8,
    LC_INIT                           = 9,
    LC_SEND_L_PRIME                   = 10,
    SKE_SEND_EKS                      = 11,
    REPEATERAUTH_SEND_RECEIVERID_LIST = 12,
    REPEATERAUTH_SEND_ACK             = 15,
    REPEATER_AUTH_STREAM_MANAGE       = 16,
    REPEATER_AUTH_STREAM_READY        = 17,
    // Special cases
    // Errata
    ERRATA_DP_STREAM_TYPE = 50,
} HDCP2_MESSAGE_ID;

typedef enum _SB_HDCP_AUTH_STATUS
{
    SB_HDCP2_UNAUTHENTICATED = 1,
    SB_HDCP2_AUTH_IN_PROGRESS,
    SB_HDCP2_AUTH_COMPLETE,
    SB_HDCP2_LINKINTEGRITY_FAILED, // Link Integrity check failed
    SB_HDCP2_LINK_DISABLED,        // Diaply Unplugged\Deactivated
} SB_HDCP_AUTH_STATUS;

typedef struct _SB_HDCP_AUTH_DATA
{
    SB_HDCP_AUTH_STATUS eHDCPAuthStatus;              // indicates the current status of Authentication
    BOOL                bHDCPAuthenticationPass;      // indicates whether HDCP Auth is successfully done for the display or not. Valid only if is bHDCPSupported TRUE
    UCHAR               ReceiverId[RECEIVER_ID_SIZE]; // 40 bit long receiver id extracted from CertRx
                                                      // UCHAR   ucVersion;                     //The HDCP version 2.0 or 2.1
    UCHAR ucMajorVersion;                             // The HDCP version 2.0 or 2.1
    UCHAR ucMinorVersion;                             // The HDCP version 2.0 or 2.1
    BOOL  bRepeater;                                  // Boolean indicating whether the Remote Display is Repeater or not
    BOOL  bHasHDCP2_0_Repeater;                       // BOOL indicating whther the downstream topology has HDCP 2_0 Repeater
    BOOL  bHasHDCP1_Device;                           // BOOL indicating whther the downstream topology has HDCP 1 Device
    DDU32 uiRepeaterDeviceCount;                      // Number of Repeaters in the down stream. Valid only if bRepeater is TRUE
    UCHAR ucReceiverIDList[MAX_DEVICE_COUNT *
                           RECEIVER_ID_SIZE]; // List of Receiver Ids each of 40 bit long. Max number of repeaters can be 31 as per HDCP 2.0 spec. Valid only if bRepeater is TRUE
    DDU32 dwTypeStatus;                       // The last successful Type notification. Default value is 0
} SB_HDCP_AUTH_DATA, *PSB_HDCP_AUTH_DATA;

// Structure to return EDID information of the TPV device along with with few other Device capabilities.
typedef struct _SB_HDCP_ARGS
{
    IN DDU32          ulDisplayUid;
    BOOLEAN           bIsHDCPSupported;
    SB_HDCP_AUTH_DATA stHDCPAuthData;
} SB_HDCP_ARGS, *PSB_HDCP_ARGS;

typedef enum
{
    eSB_HDCPSTATUS_LINKINTEGRITY, // To pass link integrity state to KMD
    eSB_HDCPSTATUS_AUTH_PROGRESS, // To indicates if authentication is in prgress
    eSB_HDCPSTATUS_AUTH_DATA      // To pass HDCP 2.0 authentication data
} SB_HDCP_STATUS_TYPE,
*PSB_HDCP_STATUS_TYPE;

typedef enum _HDCP_AUTH_LEVEL
{
    HDCP_NO_AUTH = 0,
    HDCP_AUTH_TYPE_ZERO,
    HDCP_AUTH_TYPE_ONE,
    MAX_HDCP_AUTH_TYPE
} HDCP_AUTH_LEVEL,
*PHDCP_AUTH_LEVEL;

typedef struct _SB_TPV_ENCODER_HDCP_STATUS
{
    IN DDU32            ulDisplayUID; // DisplayUID of the WiDi Encoder whose caps will be udpated.
    SB_HDCP_STATUS_TYPE eHDCPStatus;
    union {
        BOOLEAN           bAdapterLinkIntegrityFailed; // Indicates that adapter's down stream link integrity has failed
        BOOLEAN           bAuthenticationInProgress;   // Indicates if authentication is in prgress
        SB_HDCP_AUTH_DATA stHDCPAuthData;
    };
} SB_TPV_ENCODER_HDCP_STATUS, *PSB_TPV_ENCODER_HDCP_STATUS;

typedef struct _SB_TPV_SUPPORTED_MODE_ARGS
{
    IN DDU32   ulDisplayUID; // DisplayUID of the WiDi Encoder whose supported mode list will be udpated.
    DDU32      ulNumModes;
    PMODE_INFO pTPVSupportedMode; // list of modes that can be supported by TPV display
} SB_TPV_SUPPORTED_MODE_ARGS, *PSB_TPV_SUPPORTED_MODE_ARGS;

// Structure which takes X, Y, RR as input and generates a Timing for it..
// Added for Collage implementationto genrate fake target timings for Collage modes
typedef struct _SB_GENERATE_TIMING_ARGS
{
    IN DDU32 ulXRes;
    IN DDU32 ulYRes;
    IN DDU32 ulRRate;
    IN BOOLEAN bMargin_Req;
    IN BOOLEAN bInterLaced;
    IN BOOLEAN bRed_Blank_Req;
    IN DDU32 eTimingType;
    OUT MODE_TIMINGINFO stModeTimingInfo;
} SB_GENERATE_TIMING_ARGS, *PSB_GENERATE_TIMING_ARGS;

typedef struct _SB_GET_CURRENT_TIMING_ARGS
{
    IN DDU32 ulPipeIndex;
    OUT DDU32 dwHTotal;      // Horizontal total in pixels
    OUT DDU32 dwHActive;     // Active in pixels
    OUT DDU32 dwHBlankStart; // From start of active in pixels
    OUT DDU32 dwHBlankEnd;   // From start of active in pixels
    OUT DDU32 dwHSyncStart;  // From start of active in pixels
    OUT DDU32 dwHSyncEnd;    // From start of active in pixels
    OUT DDU32 dwHRefresh;    // Refresh Rate
    OUT DDU32 dwVTotal;      // Vertical total in lines
    OUT DDU32 dwVActive;     // Active lines
    OUT DDU32 dwVBlankStart; // From start of active lines
    OUT DDU32 dwVBlankEnd;   // From start of active lines
    OUT DDU32 dwVSyncStart;  // From start of active lines
    OUT DDU32 dwVSyncEnd;    // From start of active lines
    OUT DDU32 dwVRefresh;    // Refresh Rate
} SB_GET_CURRENT_TIMING_ARGS, *PSB_GET_CURRENT_TIMING_ARGS;

typedef struct _SB_FASTMODESET_POSSIBLE_ARGS
{
    IN DDU32 ulPipeIndex;
    IN PSB_SETDISPLAYDEV_ARGS pSetDisplayDeviceArgs;
    IN PSB_SETMODE_ARGS pSetModeArgs;
    OUT BOOLEAN bFastModeSetPossible;
} SB_FASTMODESET_ARGS, *PSB_FASTMODESET_ARGS;

typedef struct _SB_SETAUDIO_ARGS
{
    DDU32 ulDisplayUID[MAX_PHYSICAL_PIPES]; // DisplayUID of Audio Device whose bits have to be set.
    DDU32 ulPipeID;                         // This is to indicate pipe Id for the current display
    DDU32 ulNumOfDisplays;                  // Not being used as of now. Assigning it to 1 always.

    DDU32 ulOperationType; // This could be one of macros defined about defining which bits have to be set.

    union {
        UCHAR ucAudioState;
        struct
        {
            UCHAR bCPReady : 1;  // 1 – Graphics Device Ready, 0 – Graphics Device Not Ready.
            UCHAR bPDState : 1;  // 1 – Audio endpoint, 0 – Non - Audio endpoint .
            UCHAR bIAState : 1;  // 0 – Device Active, 1 – Device Inactive.
            UCHAR bELDState : 1; // 1 – ELD State Active, 0 – ELD State Not Active.
            UCHAR Reserved : 4;  // Reserved bits.
        };
    };
    BOOLEAN bMaster; // Applicable only for Cloned Audio
} SB_SETAUDIO_ARGS, *PSB_SETAUDIO_ARGS;

typedef enum
{
    SB_AUDIO_EVENT_NONE = 0,
    SB_AUDIO_EVENT_STOP_DEVICE,
    SB_AUDIO_EVENT_DOCK_START,
    SB_AUDIO_EVENT_DOCK_END, // TODO: Check if it is required
    SB_AUDIO_EVENT_TOPOLOGY_CHANGED,
    SB_AUDIO_EVENT_PIPE_DISABLE,
    SB_AUDIO_EVENT_POWER_ACTION,
    SB_AUDIO_EVENT_CPREADY, // TODO: Check if VP_AUDIO_ENCRYPT_CMD_ACKNOWLEDGE can be handled with this
    SB_AUDIO_EVENT_PRE_CDCLK_CHANGE,
    SB_AUDIO_EVENT_POST_CDCLK_CHANGE,
    SB_AUDIO_EVENT_PRE_TDR_RECOVERY,
    SB_AUDIO_EVENT_POST_TDR_RECOVERY,
    SB_AUDIO_EVENT_DRIVER_DISABLE
} SB_AUDIO_EVENT;

typedef struct _SB_AUDIO_PIPE_INFO
{
    DDU32   ulDisplayUID;
    DDU32   ulPipeIndex;
    BOOLEAN bIsAudioEnabled;
} SB_AUDIO_PATH_INFO;

typedef struct _SB_AUDIO_TOPOLOGY_INFO
{
    DDU32              dwNumPaths;
    SB_AUDIO_PATH_INFO stPathInfo[MAX_PHYSICAL_PIPES];
} SB_AUDIO_TOPOLOGY_INFO;

typedef struct _SB_AUDIO_EVENT_PARAMS
{
    SB_AUDIO_EVENT         eEventType;
    SB_AUDIO_TOPOLOGY_INFO stTopologyInfo;
} SB_AUDIO_EVENT_PARAMS, *PSB_AUDIO_EVENT_PARAMS;

#ifndef _COMMON_PPA
// MPO
typedef struct _SB_GET_PLANE_ZORDER_ARGS
{
    IN DDU32 ulPlaneType;
    OUT PLANE_ZORDER ePlaneZOrder;
} SB_GET_PLANE_ZORDER_ARGS, *PSB_GET_PLANE_ZORDER_ARGS;
#endif

typedef struct _SB_GET_MPO_CAPS_ARGS
{
    IN DDU32 ulDisplayUID[MAX_PHYSICAL_PIPES]; // For Clone
    IN DDU32 ulNumDevices;
    OUT MPO_CAPS stMPOCaps;
} SB_GET_MPO_CAPS_ARGS, *PSB_GET_MPO_CAPS_ARGS;

typedef struct _SB_GET_MPO_GROUP_CAPS_ARGS
{
    IN DDU32 ulDisplayUID[MAX_PHYSICAL_PIPES]; // For Clone
    IN DDU32 ulNumDevices;
    IN DDU32 ulGroupIndex; // Addition done by [Simi]
    OUT MPO_GROUP_CAPS stMPOGroupCaps;
} SB_GET_MPO_GROUP_CAPS_ARGS, *PSB_GET_MPO_GROUP_CAPS_ARGS;

//*************** CheckMPOSupport *********************************
////////////MP to SoftBIOS
// All the aspects of the Plane that SoftBIOS has to validate for support - includes OS given info and internal context info for that plane.
typedef struct _SB_MPO_CHECKMPOSUPPORT_PLANE_INFO
{
    DDU32   uiLayerIndex;    // top mostplane is layer 0, 0 based index
    DDU32   ulSize;          // adding for 2LM, this indicates the mem size
    DDU32   uiOSPlaneNumber; // This is the plane number that OS assigned for this plane. This is returned if we fail checkMPO due to this plane.
    BOOLEAN bIsDWMPlane;
    // The below are those information which OS doesn't directly give as part of checkMPO call but we need to find out internally before calling SoftBIOS.
    BOOLEAN                 bEnabled;
    BOOLEAN                 bIsAsyncMMIOFlip; // Not be used currently for MPO as it is always Synchronous flips..
    HANDLE                  hAllocation;
    MPO_PLANE_ATTRIBUTES    stPlaneAttributes;
    SURFACE_MEM_OFFSET_INFO stSurfaceMemInfo;
    SB_PIXELFORMAT          eSBPixelFormat;
    BOOLEAN                 bFakeCheckMPOCall; // set to true if its an internal call (not from OS)
} SB_MPO_CHECKMPOSUPPORT_PLANE_INFO, *PSB_MPO_CHECKMPOSUPPORT_PLANE_INFO;

// All aspects of the Path which needs to be validated - this would contain information from multiple planes in a path and corresponding Pipe\DisplayUID.
typedef struct _SB_MPO_CHECKMPOSUPPORT_PATH_INFO
{
    IN DDU32 uiPlaneCount;
    IN SB_MPO_CHECKMPOSUPPORT_PLANE_INFO stMPOPlaneInfo[MAX_PLANES]; // sjm: max planes per pipe ?
    IN UCHAR ucPipeIndex;
    IN DDU32 ulDisplayUID;                        // Only Pipe index should be sufficient but let's fill this also for implementation ease in SoftBIOS.
    IN BOOLEAN bHDREnabled;                       // This flag will be set by MP based on OS commit. If OS enabled HDR then this will be set.
    IN MPO_POST_COMPOSITION stMPOPostComposition; // this is filled if driver has to enable Pipe panel fitter.
} SB_MPO_CHECKMPOSUPPORT_PATH_INFO, *PSB_MPO_CHECKMPOSUPPORT_PATH_INFO;
// Parent structure containing information on all paths which is being asked for MPO support. This should be the structure going to SoftBIOS for validation.
typedef struct _SB_MPO_CHECKMPOSUPPORT_ARGS
{
    IN SB_MPO_CHECKMPOSUPPORT_PATH_INFO stCheckMPOPathInfo[MAX_PHYSICAL_PIPES]; //_simi: replaced MAX_PATH with MAX_PHYSICAL_PIPES
    IN DDU32 ulNumPaths;
    IN DDU32 ulConfig; // Ideally SoftBIOS doesn't need this info, but providing it for basic level verification before going deeper and for any future needs.

    OUT BOOLEAN bSupported;
    OUT BOOLEAN bSecureSpriteBWExceeds;
    OUT DDU32 ulFailureReason; // We can define macros and store internally, if OS requests  this info we can give back later.
    OUT CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo;
} SB_MPO_CHECKMPOSUPPORT_ARGS, *PSB_MPO_CHECKMPOSUPPORT_ARGS;

// GetDisplayStartMPO
// Structure for get display start MPO
typedef struct _SB_GETDISPLAYSTARTMPO_ARGS
{
    IN DDU32 ulDisplayStart;
    IN       BOOLEAN
             bGetDoubleBufferedAddress; // From Cantiga onwards, SoftBIOS can get the Live Display Start Address. This is more to do whether u want to get Live or Double Buffered address.
    IN DDU32 uiLayerIndex;
    IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
    IN DDU32 uiEnabledPlaneCount;
    IN BOOLEAN bIsYUY2Enabled;
    IN BOOLEAN bIsScalingRequired;
} SB_GETDISPLAYSTARTMPO_ARGS, *PSB_GETDISPLAYSTARTMPO_ARGS;

#define SB_MPO_sRGB_MASK 0x00000002
#define SB_MPO_xvYCC_MASK 0x00000004

/***********************************************************/

typedef struct _SB_SURFACE_MEM_INFO
{
    DDU32 hGfxAddress; // Gfx address after getting from GMM by passing the allocation address from OS.
    DDU32 ulOSAddress;

    DDU32                   ulScanLineLength; // for stride programming
    DDU32                   ulAuxScanLineLength;
    SURFACE_MEM_OFFSET_INFO stSurfaceMemInfo;
    DDU32                   ulPlaneXPos;
    DDU32                   ulPlaneYPos;
} SB_SURFACE_MEM_INFO, *PSB_SURFACE_MEM_INFO;

/*************** Flip ************************************************/
typedef struct _SB_MPO_PLANE_INFO
{
    BOOLEAN                         bEnabled;
    BOOLEAN                         bIsPlaneEncrypted;
    BOOLEAN                         bIsAsyncMMIOFlip;
    BOOLEAN                         bIsAsyncMMIOFlipWaitNeeded;
    BOOLEAN                         bReported;
    DDU32                           uiLayerIndex;
    DDU32                           uiOSLayerIndex;
    DDU32                           uiMaxImmediateFlipLine;
    DDU32                           hGfxAddress; // Gfx address after getting from GMM by passing the allocation address from OS.
    DDU32                           ulOSAddress;
    DDU32                           ulScanLineLength;    // for stride programming
    DDU32                           ulAuxScanLineLength; // For Unified allocations, this corresponds to Pitch of Control surface.
    DDU32                           ulBitsPerPixel;
    DDU64                           ulPresentID;
    PVOID                           pGmmBlock;
    MPO_PLANE_ATTRIBUTES            stPlaneAttributes;
    DDU32                           uiDirtyRectCount;
    PM_RECT                         pDirtyRects;
    SURFACE_MEM_OFFSET_INFO         stSurfaceMemInfo;
    SB_PIXELFORMAT                  eSBPixelFormat;
    IGFX_ENCRYPTION_TYPE            bEncryptiontype;
    SB_SURFACE_MEM_INFO             stYSurfaceDetails; // This will have all details w.r.t. memory for Y surface
    MPO_PLANE_SPECIFIC_INPUT_FLAGS  stPlaneSpecificInputFlags;
    MPO_PLANE_SPECIFIC_OUTPUT_FLAGS stPlaneSpecificOutputFlags;
    // Separate, Y, U, V offsets from GMM for NV12 – TBD..
} SB_MPO_PLANE_INFO, *PSB_MPO_PLANE_INFO;

typedef struct _SB_MPO_SSA_ARGS
{
    DDU32                ulDisplayUID;
    UCHAR                ucPipeIndex;
    DDU32                uiPlaneCount;
    DDU32                ulSourceID;   // added for 2LM
    PSB_HDR_SURFACE_DESC pHDRSurfInfo; // HDR surface info has to be sent out to SB to send it to the panel.
    SB_MPO_PLANE_INFO    stMPOPlaneArgs[MAX_PLANES];
    MPO_POST_COMPOSITION stPostComposition;
} SB_MPO_SSA_ARGS, *PSB_MPO_SSA_ARGS;

typedef struct _SB_TILE_LOCATION_INFO
{
    DDU32 ulHLocation;
    DDU32 ulVLocation;
    DDU32 dwTargetID;
} SB_TILE_LOCATION_INFO, *PSB_TILE_LOCATION_INFO;

// Indicates Scaling type for Tiled display
typedef enum _TILED_DISPLAY_SCALING_TYPE
{
    UNINITIALIZED = 0,
    NO_STRETCH,
    STRETCH_ENTIRE_DISPLAY,
    CLONE_OTHER_DISPLAYS
} TILED_DISPLAY_SCALING_TYPE;

typedef struct _SB_GET_TILED_DISPLAY_INFO
{
    IN DDU32 ulDisplayID;
    OUT BOOLEAN bIsTiledDisplay;
    OUT UCHAR ucHTiles;
    OUT UCHAR ucVTiles;
    OUT BOOLEAN bIsMasterDisplay;
    OUT DDU32 ulOtherDisplayUID;
    OUT DDU16 usX;
    OUT DDU16 usY;
    OUT DDU16 usNativeX;
    OUT DDU16 usNativeY;
    OUT TILED_DISPLAY_SCALING_TYPE eTileScalingType;
    OUT DDU32 ulTotalTiles;
    OUT SB_TILE_LOCATION_INFO stTileLocations[MAX_PHYSICAL_PIPES]; // location 0 always for master display
} SB_GET_TILED_DISPLAY_INFO, *PSB_GET_TILED_DISPLAY_INFO;

typedef struct _SB_GET_SOURCE_MODE_TYPE
{
    IN DDU32 ulDisplayId;
    IN SOURCE_MODE_INFO stSourceModeInfo;
    OUT MODE_TYPE eModeType;
    OUT BOOLEAN bIsTrueEdidMode;
    OUT BOOLEAN bIsTileMode;
    OUT BOOLEAN bIsPipeGangedMode;
} SB_GET_SOURCE_MODE_TYPE, *PSB_GET_SOURCE_MODE_TYPE;

typedef enum _SB_HDR_SUPPORT_FLAGS
{
    eHDR_CAP_ERROR_SYSTEM_INCAPABLE, // display HW on this platform is incapable
                                     // of transmitting HDR signals

    eHDR_CAP_ERROR_MULTI_MON_ACTIVE, // multi-monitor mode is active

    eHDR_CAP_ERROR_NONE_HDR_PORT, // although this platform can support HDR
                                  // signals, it cannot do so on the currently
                                  // active port (display connector
                                  // being driving by the graphics HW)

    eHDR_CAP_ERROR_NO_HDR_DISPLAY, // although the currently active port can
                                   // support HDR-out, the currently attached
                                   // monitor does not support HDR signals

    eHDR_CAP_GOOD_TO_GO, // current port and attached display support HDR signals
} SB_HDR_SUPPORT_FLAGS,
*PSB_HDR_SUPPORT_FLAGS;

// Struct: _SB_HDR_CAPS_ARGS
// This structure provides a external interface to support
// HDR configuration via escape interface
typedef struct _SB_HDR_CAPS_ARGS
{
    OUT SB_HDR_SUPPORT_FLAGS eHDRSupported;
    IN DDU32 ulTargetID;
} SB_HDR_CAPS_ARGS, *PSB_HDR_CAPS_ARGS;

typedef struct _SB_HDCP2_GETSTATUS_ARGS
{
    IN DDU32 ulDisplayUID;
    WORD     wRxStatus;
} SB_HDCP2_GETSTATUS_ARGS, *PSB_HDCP2_GETSTATUS_ARGS;

typedef struct _SB_HDCP2_WRITEMSG_ARGS
{
    IN DDU32 ulDisplayUID;
    DDU8 *   pBuff;
    DDU32    ulBufferSize;
    BOOLEAN  bIsHRI;
} SB_HDCP2_WRITEMSG_ARGS, *PSB_HDCP2_WRITEMSG_ARGS;

typedef struct _SB_HDCP2_READMSG_ARGS
{
    IN DDU32 ulDisplayUID;
    DDU8 *   pBuff;
    DDU32    ulBufferSize;
    DDU32    ulBytesRead;
    BOOLEAN  bIsHRI;
} SB_HDCP2_READMSG_ARGS, *PSB_HDCP2_READMSG_ARGS;

typedef struct _SB_HDCP2HRI_SETUP_ARGS
{
    IN DDU32 ulDisplayUID;
    BOOLEAN  bHRIMode;
} SB_HDCP2HRI_SETUP_ARGS, *PSB_HDCP2HRI_SETUP_ARGS;

typedef struct _SB_HDCP2HRI_SET_RXSTATUS_ARGS
{
    IN DDU32 ulDisplayUID;
    DDU32    ulRxStatus;
} SB_HDCP2HRI_SET_RXSTATUS_ARGS, *PSB_HDCP2HRI_SET_RXSTATUS_ARGS;

typedef struct _SB_HDCP2_UPDATESTATUS_ARGS
{
    IN DDU32          ulDisplayUID;
    SB_HDCP_AUTH_DATA stHDCPAuthData;
} SB_HDCP2_UPDATESTATUS_ARGS, *PSB_HDCP2_UPDATESTATUS_ARGS;

typedef enum _COLORSPACE_RANGE
{
    bFullRange         = 0,
    b16To235ColorRange = 1
} COLORSPACE_RANGE;

typedef struct _SB_PLANE_COLORSPACE_INFO
{
    COLORSPACE_RANGE     bRange; // Full or Studio
    DDU32                ulGamma;
    SB_COLORSPACE_TYPES  eColorSpace; // specifies RGB or YCbCr
    SB_PIXELFORMAT       eformat;
    MPO_COLORSPACE_FLAGS stFlags;
} SB_PLANE_COLORSPACE_INFO, *PSB_PLANE_COLORSPACE_INFO;

// 0x5F64, 0x0A - Get/Set Video Parameters ----------------------------------

#define GetSetParameter_FuncCode (0x5F64)
#define GetSetParameter_SubFunc (0x0a)

typedef struct _SB_CONTAINERID_ARGS
{
    GUID  Guid; // GUID of this structure
    DDU32 ulDisplayUID;
    struct
    {
        DDU64 PortId;
        DDU16 ManufacturerName;
        DDU16 ProductCode;
    } EldInfo;
} SB_CONTAINERID_ARGS, *PSB_CONTAINERID_ARGS;

// Get Set parameters args structure
typedef struct _SB_GETSETPARAM_ARGS
{
    IN DDU32 ulDisplayUID; // Unique display ID (cannot accept generic types)
    IN_OUT union {
        VIDEOPARAMETERS      VideoParameters;
        HDCP_PARAMETERS      HdcpParameters;
        LFPPARAMETERS        LfpParameters;
        CP_PARAMETERS_T      CPParameters;
        HDMI_PARAMETERS      HDMIParameters;
        GET_CONNECTOR_INFO   GetConnectorInfo;
        AVI_INFOFRAME_CUSTOM AVIInfoFrameCustom;
        SB_CONTAINERID_ARGS  ContainerIDArgs;
    };
} SB_GETSETPARAM_ARGS, *PSB_GETSETPARAM_ARGS;

// 0x5F67 - Blank Video -----------------------------------------------------

#define BlankVideo_FuncCode (0x5F67)

// Blank video args structure
typedef struct _SB_BLANKVIDEO_ARGS
{
    IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
    IN DDU32 ulVideoOn;   // 0 = Video Off, 1 = Video On
} SB_BLANKVIDEO_ARGS, *PSB_BLANKVIDEO_ARGS;

// 0x5F69 - Set Primary Pipe ------------------------------------------------

#define PrimaryPipe_FuncCode (0x5F69)

// primary pipe args structure
typedef struct _SB_PRIMARYPIPE_ARGS
{
    IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
} SB_PRIMARYPIPE_ARGS, *PSB_PRIMARYPIPE_ARGS;

// DisplayUIDFromTypeandIndex/GetTypeAndIndexFromDisplayUID - 5F64, 0Fh-------

#define Query_DisplayDetails_FuncCode (0x5F64)
#define Query_DisplayDetails_GetSubFuncCode (0x0F)

// Display details flag enum
typedef enum _DISPLAY_DETAILS_FLAG
{
    QUERY_DISPLAYUID = 1,
    QUERY_DISPLAYTYPE_INDEX
} DISPLAY_DETAILS_FLAG;

// query display details args structure
typedef struct _SB_QUERY_DISPLAY_DETAILS_ARGS
{
    // eflag = QUERY_DISPLAYUID -> Indicates that Display Type & Index will be sent & we need to return DisplayUID & bExternalEncoderDriven
    // eflag = QUERY_DISPLAYTYPE_INDEX -> Indicates that DisplayUID will be sent & we need to return  Display Type ,Index & bExternalEncoderDriven
    IN DISPLAY_DETAILS_FLAG eflag;

    IN_OUT DDU32 ulDisplayUID;
#ifndef _COMMON_PPA
    IN_OUT DISPLAY_TYPE eType;
#endif
    IN_OUT UCHAR ucIndex;

    // Is display ID driven by external encoder?
    OUT BOOLEAN bExternalEncoderDriven; // Includes both sDVO and NIVO Displays

    OUT BOOLEAN bTPVDrivenEncoder;

    // Type of Port Used.
    OUT PORT_TYPES ePortType;

    // This interprets logical port mapping for physical connector.
    // This indicates mapping multiple encoders to the same port
    OUT UCHAR ucLogicalPortIndex;
} SB_QUERY_DISPLAY_DETAILS_ARGS, *PSB_QUERY_DISPLAY_DETAILS_ARGS;

// Device combination validation -- 0x5F80 -----------------------------------
// Device combination Args structure
typedef struct _SB_DEVCOMBO_ARGS
{
    IN PPIPE_DISPLAYS pPipeDisplayList;
    IN BOOLEAN bValidateRunTimeDispConfig; // TRUE/FALSE
    IN BOOLEAN bNonFunctionalISVCall;
} SB_DEVCOMBO_ARGS, *PSB_DEVCOMBO_ARGS;

/******************************************************************************************
//Longhorn specific definitions
*******************************************************************************************/

#define SB_EDID_SIZE 128 // EDID size is minimum 128 Bytes
#ifndef DDU8
typedef UCHAR DDU8;
#endif
// This is almost identical to D3DKMDT_VIDEO_OUTPUT_TECHNOLOGY defined in OS header.
// To keep SB independent of OS header dependencies, it is being redefined here.

// Enum for monitor interface type
typedef enum _SB_MONITOR_INTERFACE_TYPE
{
    MIT_UNINITIALIZED        = 0,
    MIT_HD15                 = 1,
    MIT_DVI                  = 2,
    MIT_HDMI                 = 3,
    MIT_LVDS                 = 4,
    MIT_SVIDEO               = 5,
    MIT_D_JPN                = 6,
    MIT_COMPOSITE            = 7,
    MIT_COMPONENT            = 8,
    MIT_SDI                  = 9,
    MIT_DISPLAYPORT_EXTERNAL = 10,
    MIT_DISPLAYPORT_EMBEDDED = 11,
    MIT_UDI_EXTERNAL         = 12,
    MIT_UDI_EMBEDDED         = 13,
    MIT_SDTVDONGLE           = 14,
    MIT_INTERNAL             = 15,
    MIT_MIRACAST             = 16,
    MIT_OTHER                = 255
} MONITOR_INTERFACE_TYPE;

// This is almost identical to DXGK_CHILD_DEVICE_HPD_AWARENESS defined in OS header.
// To keep SB independent of OS header dependencies, it is being redefined here.

// Enum for targer HPD type
typedef enum _SB_TARGET_HPD_TYPE
{
    HpdTypeUninitialized   = 0,
    HpdTypeAlwaysConnected = 1,
    HpdTypeNone            = 2,
    HpdTypePolled          = 3,
    HpdTypeInterruptible   = 4
} TARGET_HPD_TYPE;

// Enum for MCCS
typedef enum _SB_MCCSCAPS
{
    SB_MCCS_NOTSUPPORTED = 0,
    SB_MCCS_V1           = 1,
    SB_MCCS_V2           = 2
} SB_MCCSCAPS;

// EDID structure
typedef struct _SB_EDID
{
    BOOL  bInitialized;  // Whether this EDID is valid
    DDU32 ulEdidVersion; // version of the EDID as reported by the monitor
    DDU32 ulEdidSize;    // EDID size as reported by the monitor
    DDU8  buffer[SB_EDID_SIZE];
} SB_EDID;

// Monitor properties structure
typedef struct _SB_MONITOR_PROPERTIES
{
    DDU32   ulNativeResolutionX; // Native resolution (x, y)
    DDU32   ulNativeResolutionY; // This also tells the aspect ratio
    DDU32   ulNativeRefreshRate;
    SB_EDID stEdid;                    // EDID for this monitor
    DDU32   ulAspectScalingPreference; // full screen/centering/aspect scaling
    BOOL    bLidStatus;                // for displays with lids
                                       // DEVICE_POWER_STATE    currentPowerState;
} SB_MONITOR_PROPERTIES;

// Used by the SBGetTargetList() function
typedef struct _SB_TARGET_DESCRIPTOR_ARGS
{
    DDU32                  ulDisplayUID;          // Display device UID
    TARGET_HPD_TYPE        eTargetHpdType;        // Target HPD type
    MONITOR_INTERFACE_TYPE eMonitorInterfaceType; // Monitor interface type
    PORT_TYPES             ePort;
} SB_TARGET_DESCRIPTOR_ARGS, *PSB_TARGET_DESCRIPTOR_ARGS;

// Used by the SBGetTargetList() function
typedef struct _SB_TARGET_ENUMERATION_ARGS
{
    DDU32                      ulNumOfTargets;          // Number of targets
    PSB_TARGET_DESCRIPTOR_ARGS pSbTargetDescriptorArgs; // pointer to targer descriptor args structure
} SB_TARGET_ENUMERATION_ARGS, *PSB_TARGET_ENUMERATION_ARGS;

// Data Sructures for Target Mode List
typedef struct _SB_MONITOR_TARGET_MODES_ARGS
{
    IN DDU32 ulDisplayUID;                   // Display Device UID
    IN BOOLEAN bDownScalarSupported;         // to SB to include higher modes for DS in the monitor mode list
    OUT DDU32 ulNumOfModes;                  // Number of modes
    OUT PMONITOR_MODE_INFO pMonitorModeInfo; // pointer to monitor mode info structure
} SB_MONITOR_TARGET_MODES_ARGS, *PSB_MONITOR_TARGET_MODES_ARGS;

typedef struct _SB_GET_TARGET_MODE_LIST_ARGS
{
    IN DDU32 ulDisplayUID; // Display Device UID
    IN BOOLEAN bEnumerateOnlyMonitorModes;
    OUT DDU32 ulNumOfModes;                  // Number of modes
    OUT PMONITOR_MODE_INFO pMonitorModeInfo; // pointer to monitor mode info structure
} SB_GET_TARGET_MODE_LIST_ARGS, *PSB_GET_TARGET_MODE_LIST_ARGS;

typedef struct _SB_GET_SOURCE_MODE_LIST_ARGS
{
    IN DDU32 ulDisplayUID; // Display device UID
    IN BOOLEAN bEnumerateOnlyMonitorModes;
    OUT DDU32 ulNumOfModes;                  // Total number of modes
    OUT PSOURCE_MODE_INFO pstSourceModeInfo; // Pointer to source mode info structure
} SB_GET_SOURCE_MODE_LIST_ARGS, *PSB_GET_SOURCE_MODE_LIST_ARGS;

typedef struct _SOURCE_TARGET_RELATION_INFO
{
    // The DDU32 below for scaling is a Multi-Select Bit Mask. The individual values are defined as:
    // COMP_FULL_SCREEN -> (1<<1)
    DDU32 ulScaling;
} SOURCE_TARGET_RELATION_INFO, *PSOURCE_TARGET_RELATION_INFO;

typedef struct _TARGET_RELATION_MODE_INFO
{
    SOURCE_TARGET_RELATION_INFO stSrcTgtRelationInfo;
    MONITOR_MODE_INFO           stMonitorModeInfo;
} TARGET_RELATION_MODE_INFO, *PTARGET_RELATION_MODE_INFO;

typedef struct _SB_GET_TARGET_MODELIST_FOR_SOURCE_MODE_ARGS
{
    IN DDU32 ulDisplayUID;                // Display Device UID
    IN SOURCE_MODE_INFO stSourceModeInfo; // Mode info structure
    IN SOURCE_TARGET_RELATION_INFO stRelationInfo;
    IN BOOLEAN bEnumerateOnlyMonitorModes;
    OUT MONITOR_MODE_SUPPORT eSourceModeMonitorSupport;
    OUT DDU32 ulNumOfTargetModes;
    OUT PTARGET_RELATION_MODE_INFO pstTargetRelationModeInfo;
} SB_GET_TARGET_MODELIST_FOR_SOURCE_MODE_ARGS, *PSB_GET_TARGET_MODELIST_FOR_SOURCE_MODE_ARGS;

typedef struct _SB_GET_RELATION_FOR_SOURCE_TARGET_MODE_ARGS
{
    IN DDU32 ulDisplayUID;                  // Display Device UID
    IN SOURCE_MODE_INFO stSourceModeInfo;   // Source Mode info structure
    IN MONITOR_MODE_INFO stMonitorModeInfo; // Target Mode info structure
    OUT SOURCE_TARGET_RELATION_INFO stRelationInfo;
} SB_GET_RELATION_FOR_SOURCE_TARGET_MODE_ARGS, *PSB_GET_RELATION_FOR_SOURCE_TARGET_MODE_ARGS;

#define GetTableInfo_FuncCode (0x5F98)

typedef enum _SB_ENUM_TABLES
{
    eSource = 0,
    eTarget,
    eMapping,
    eInvalid,
} SB_ENUM_TABLES;

typedef struct _SB_GET_TABLE_INFO_ARGS
{
    DDU32          ulDisplayUID;
    SB_ENUM_TABLES eTable;
    DDU32          ulNumOfModes;
    UCHAR          stModeInfo[1];
} SB_GET_TABLE_INFO_ARGS, *PSB_GET_TABLE_INFO_ARGS;

// Get scan line info Args Structure
typedef struct _SB_GET_SCAN_LINE_INFO_ARGS
{
    DDU32 ulPipeIndex;   // pipe index
    DDU32 ulCurScanLine; // Cursor scan line
                         // Current VActive value - Used by Miniport to scale down the
                         // Scan line values when scaling is applied. For e.g in 10*7 mode
                         // 16*12 by timing apps (and the DTM test) will not expect scan line
                         // values above 768 where as the original values could go upto 1200.
                         // Miniport will scale down the actual value in such cases.
    DDU32    ulVActive;
    BOOLEAN  bInVerticalBlank;          // Currently in VBlank or not
    LONGLONG ulTimeElapsedFromVBIStart; // Time elapsed from VBI start
} SB_GET_SCAN_LINE_INFO_ARGS, *PSB_GET_SCAN_LINE_INFO_ARGS;

typedef struct _SB_GET_TILE_FMT
{
    IN DDU32 ulHorizontalRes;
    IN SB_PIXELFORMAT eSBPixelFormat;
    IN PLANE_ORIENTATION eRotation;
    IN BOOLEAN bS3DAllocation; // Flag to indicate S3D allocation. TRUE means allocation is for OS aware S3D resource else it is normal 2D resource.
    IN DDU32 ulSourceID;       // Source ID information for allocation.
    OUT DDU32 ulMemFormat;     // YTiled is set if possible else XTiled set if possible else none.
} SB_GET_TILE_FMT, *PSB_GET_TILE_FMT;

typedef enum _SB_SPRITE_COLORSPACE_ENUM
{
    eSpriteInvalidColorSpace = 0,
    eBT601ColorSpace         = 1,
    eBT709ColorSpace         = 2,
    eBT2020ColorSpace        = 3,
} SB_SPRITE_COLORSPACE_EN;

// Get Sprite details interface
typedef enum _SB_SPRITE_SOURCE_FORMAT_ENUM
{
    eSpriteInvalidFormat = 0,
    eSpriteRGBFormat     = 1,
    eSpriteY422Format    = 2,
    eSpriteRGBFP16Format = 3,
} SB_SPRITE_SOURCE_FORMAT;

typedef struct _SB_SPRITE_DETAILS
{
    BOOLEAN                 bIsEnabled;
    SB_SPRITE_COLORSPACE_EN eColorSpace;
    SB_SPRITE_SOURCE_FORMAT eSourceFormat;
} SB_SPRITE_DETAILS, *PSB_SPRITE_DETAILS;

typedef struct _SB_OVERLAY_CURSOR_EVENT_ARGS
{
    IN DDU32 ulPipe;
    IN DDU32 ulScreenXRes;
    IN DDU32 ulScreenYRes;
    IN DDU32 ulSpriteWidth;
    IN DDU32 ulSpriteHeight;
    IN DDU32 ulSpriteLeft;
    IN DDU32 ulSpriteTop;
    IN DDU32 ulDestColorKey;
    IN DDU32 ulBitsPerPixel;
    IN DDU32 ulDstKey; // TODO: reuse the ulDestColorKey variable
    IN DDU32 ulKeyMask;
    IN DDU32 ePlaneType;
    IN SB_SPRITE_DETAILS SpriteDetails;
} SB_OVERLAY_CURSOR_EVENT_ARGS, *PSB_OVERLAY_CURSOR_EVENT_ARGS;

// XVYCC function codes
#define GetSetXVYCCSettings_FuncCode (0x5F86)
#define SB_GBD_DATA_SIZE 28
#define HDMI_GBD_VERSION_1_3 0x0103
// CUI Change, Added
typedef struct _SB_MEDIA_SOURCE_HDMI_GBD
{
    DDU16 usVersion;                     // field (=1.3 only supported) [indicates HDMI 1.3 GBD profile]
                                         // High DDU8 = 1, Low DDU8 = 3
    DDU32 ulSize;                        //(HDMI P0 GBD payload size)
                                         // GBD_P0_HDMI_1_3 HdmiGBD; //Data/Payload (send directly to HDMI 1.3 sink)
    DDU8 byGBDPayLoad[SB_GBD_DATA_SIZE]; // Need SB to change to its struct
} SB_MEDIA_SOURCE_HDMI_GBD, *PSB_MEDIA_SOURCE_HDMI_GBD;

typedef enum _SB_COLORSPACE_SUPPORTED
{
    SUPPORTS_COLORSPACE_NONE = 0, // Both xvycc and ycbcr not supported
    SUPPORTS_COLORSPACE_YCbCr,
    SUPPORTS_COLORSPACE_xvYCC
} SB_COLORSPACE_SUPPORTED,
*PSB_COLORSPACE_SUPPORTED;
//
//  SB COM interface get/set
//
typedef enum SB_OPERATION_TYPE_ENUM
{
    SB_OPTYPE_UNKNOWN = 0,     // Invalid operation type
    SB_OPTYPE_GET,             // Get
    SB_OPTYPE_SET,             // Set
    SB_OPTYPE_SET_PERSISTENCE, // Set Persistence
    NUM_OF_SB_OPTYPE
} SB_OPERATION_TYPE;

// colorspace control specific data
typedef struct _SB_COLORSPACE_CTRL_DATA
{
    IN SB_OPERATION_TYPE OpType;             // Operation Type
    IN DDU32 ulDisplayUID;                   // Dispay UID index
    IN OUT BOOLEAN bEnablePreference;        // This indicates the CUI preference to enable this feature
                                             // 1 : Enable   - the preference to activate supported colorspace
                                             // 0 : Disable  - the prefernce to activate supported colorspace
    OUT SB_COLORSPACE_SUPPORTED eColorspace; // This provides the colorspace supported

    IN SB_MEDIA_SOURCE_HDMI_GBD stMediaSourceHDMIGBD; // CUI Change, Added
} SB_COLORSPACE_CTRL_DATA, *PSB_COLORSPACE_CTRL_DATA;

#define GetS3DCaps_FuncCode (0x5F94)

typedef struct _S3D_MODE_CAPS_STRUCT
{
    // Note: All modes with 32BPP color only
    DDU16   usResWidth;    // 0xFFFF if s3d possible with all modes
    DDU16   usResHeight;   // 0xFFFF if s3d possible with all modes
    DDU32   ulRefreshRate; // 0xFFFF if s3d possible with all modes
    BOOLEAN bInterlaced;
    DDU32   dwMonitorS3DFormats; // mask of IGFX_S3D_FORMAT
    DDU32   dwGFXS3DFormats;     // mask of IGFX_S3D_FORMAT
} S3D_MODE_CAPS_STRUCT, *PS3D_MODE_CAPS_STRUCT;

// S3D Caps
typedef struct _SB_GET_S3D_CAPS
{
    IN DDU32 dwDisplayUID;
    // Indicates support for s3d in the platform with any of the ports
    // Caller shall use the display specific interface to get format/mode/display
    // specific s3d support details by display & GFX driver

    OUT BOOLEAN bSupportsS3DLRFrames;
    // Display specific S3D details
    // Valid iff dwDisplayUID is a valid display identifier

    OUT DDU32 ulNumEntries; // number of entries in S3DCapsPerMode[]
    OUT S3D_MODE_CAPS_STRUCT S3DCapsPerMode[MAX_S3D_MODES];
    OUT S3D_FORMAT eCurrentS3DFormat; // Current S3D Format
    OUT BOOLEAN bIsOverlayEnabled;
} SB_GET_S3D_CAPS, *PSB_GET_S3D_CAPS;

typedef enum _PANEL_DRIVER_EVENT_NAME // Critical events to be notified to Panel driver
{
    IGD_EVENT_UNDEFINED = 0,
    IGD_PANEL_POWER_OFF,
    IGD_PANEL_POWER_ON,
    IGD_DRIVER_UNLOAD,
    IGD_DRIVER_LOADED,
    IGD_SYSTEM_D3_D4,
    IGD_SYSTEM_D0,
    IGD_BACKLIGHT_ON,
    IGD_BACKLIGHT_OFF
} PANEL_DRIVER_EVENT_NAME,
*PPANEL_DRIVER_EVENT_NAME;

typedef enum _PANEL_DRIVER_EVENT_TYPE // Event type, if it is pre event or post event
{
    IGD_EVENT_TYPE_SINGLE_EVENT = 0,
    IGD_EVENT_TYPE_PRE_EVENT,
    IGD_EVENT_TYPE_POST_EVENT
} PANEL_DRIVER_EVENT_TYPE,
*PPANEL_DRIVER_EVENT_TYPE;

typedef struct _SB_GET_TILE_OFFSET
{
    IN DDU32 ulLayerIndex; // Input layer index which helps uniquely identify Plane or GMMBlock Descriptor. For non MPO case, it will be 0 and there is only one BlockDescriptor.
                           // Only in MPO case, there could be  many buffers and MP needs this info to get to the correct Block Descriptor.
    IN PIPE_ID ePipeIndex; // Input Path which uniquely identifies the path.
    IN PLANE_ORIENTATION eHwRotAngle;
    IN DDU32 ulClipWidth;
    IN DDU32 ulClippingHeight;
    OUT SURFACE_MEM_OFFSET_INFO stOffsetInfo;
} SB_GET_TILE_OFFSET, *PSB_GET_TILE_OFFSET;

//
// MAX_COLOR_BPP definition
//
typedef union _BPP_MASK {
    // Currently required color depth values : 8, 16, 32, 64
    // If in the future, a new color depth support is required, add it here.
    // In this case you should update MAX_COLOR_BPP & ALLCOLOR_BPP_MASK
    UCHAR ucBPPMask;
    struct
    {
        UCHAR b4BPP : 1; // 1: Supported, 0 : no supported.
        UCHAR b8BPP : 1;
        UCHAR b16BPP : 1;
        UCHAR b32BPP : 1;
        UCHAR b64BPP : 1;
        UCHAR ulReserved : 3;
    };
} BPP_MASK, *PBPP_MASK;

#define ALLCOLOR_BPP_MASK 0x1F
#define WINDOWS_COLOR_MASK 0x1E // doesn't have 4bpp

// you can define what type of resource you want, spinlock, mutex, semaphore, atomic wait lock, etc...
typedef enum _RESOURCE_TYPE_INDEX
{
    eResourceTypeIndexInvalid = 0,
    eResourceTypeIndexAtomicLock,
    eResourceTypeIndexMutex,
    eResourceTypeSpinLock,
    eResourceTypeIndexMaxValue,
} RESOURCE_TYPE_INDEX;

//-----Short Pulse Interrupt related Data Structure Definitions.
// The enum value specifies the type of operation to be performed on Event Objects.
#define SB_SPI_MAX_EVENT 2
typedef enum _SB_EVENTOBJ_FUNC_TYPE
{
    SB_SET_EVENT = 0,
    SB_CLEAR_EVENT,
    SB_READ_EVENT,
    SB_WAIT_EVENT,
    SB_WAIT_MULTIPLE_EVENT,
    SB_INVALID_EVENT
} SB_EVENTOBJ_FUNC_TYPE,
*PSB_EVENTOBJ_FUNC_TYPE;

// The enum will be used as an index into the Eventobjects array in Miniport for setting and
// waiting on events. SoftBIOS will just pass the variable of this type while calling for
// any event related operation.
typedef enum _SB_SPI_EVENT_OBJECT_INDEX
{
    eSBEventUninitialized      = -1,
    eSB_DPB_WAIT_Ri            = 0,
    eSB_DPB_WAIT_KSV_FIFO      = 1,
    eSB_DPC_WAIT_Ri            = 2,
    eSB_DPC_WAIT_KSV_FIFO      = 3,
    eSB_DPD_WAIT_Ri            = 4,
    eSB_DPD_WAIT_KSV_FIFO      = 5,
    eSB_DPB_WAIT_SideBandReply = 6,
    eSB_DPC_WAIT_SideBandReply = 7,
    eSB_DPD_WAIT_SideBandReply = 8,
    eSB_MAX_SPI_EVENT_OBJECTS
} SB_SPI_EVENT_OBJECT_INDEX;

// The enum will be used as an index into the Eventobjects array in Miniport for setting and
// waiting on events. SoftBIOS will just pass the variable of this type while calling for
// any event related operation.
typedef enum _SB_WIGIG_EVENT_OBJECT_INDEX
{
    eSBWiGigEventUninitialized    = -1,
    eSB_WIGIG_CONN_SETUP_EVENT    = 0,
    eSB_WIGIG_WDE_MSG_REPLY_EVENT = 1,
    eSB_WIGIG_WNICD3_EVENT        = 2,
    eSB_MAX_WIGIG_EVENT_OBJECTS
} SB_WIGIG_EVENT_OBJECT_INDEX;

// Structure passed as parameter while performing different actions on an event object.
typedef struct _SB_EVENTOBJ_PARAMS
{
    IN SB_EVENTOBJ_FUNC_TYPE eFuncType; // Defines the type of operation.
    union {
        IN SB_SPI_EVENT_OBJECT_INDEX eEventObjIndex;        // The index to SPI Event Object array on which
        IN SB_WIGIG_EVENT_OBJECT_INDEX eWiGigEventObjIndex; // The index to WiGig Event Object array on which
    };
    // operation has to be performed.
    IN LONG lTimeOut;   // The Time out value for Wait event. This will be looked only for Wait operation.
    OUT LONG lOpResult; // Return Value. Varies based on the operation.
} SB_EVENTOBJ_PARAMS, *PSB_EVENTOBJ_PARAMS;

typedef enum _SB_SP_INT_ID
{
    eDPortA_SPI = 1,
    eDPortB_SPI = 2,
    eDPortC_SPI = 3,
    eDPortD_SPI = 4,
    eDPortE_SPI = 5,
    eDPortF_SPI = 6,
    eDPortG_SPI = 7,
    eDPortH_SPI = 8,
    eDPortI_SPI = 9,
    eWiGigPort_SPI,
    eUndefined_SPI
} SB_SP_INT_ID;

typedef struct _SB_SPI_EVENT_DATA
{
    OUT DDU32 ulPort;
    OUT DDU32 ulHandleEvent;                          // uses the ENUM SPI_EVENT_TYPE
    OUT SB_SPI_EVENT_OBJECT_INDEX eHDCPEventObjIndex; // Today its Valid only for eKSVFifoReady event..
    OUT UCHAR ucValidDisplayUidCount;
    OUT DDU32 ulDisplayUidList[3]; // Display for which event is generated
} SB_SPI_EVENT_DATA, *PSB_SPI_EVENT_DATA;

typedef enum _SB_WAIT_TYPE
{
    eSB_WAIT_ALL,
    eSB_WAIT_ANY,
    eSB_WAIT_NOTIFICATION
} SB_WAIT_TYPE;

// Wigig: Structure passed as parameter while performing different actions on an event object.
typedef struct _SB_WIGIG_EVENTOBJ_PARAMS
{
    IN SB_EVENTOBJ_FUNC_TYPE eFuncType; // Defines the type of operation.
    IN DDU32 ulNumEvents;
    IN SB_WIGIG_EVENT_OBJECT_INDEX eWiGigEventObjIndex; // The index to WiGig Event Object array on which
    IN SB_WAIT_TYPE eSBWaitType;
    IN DDU32 ulPriorityBoost;    // This is OS's KPRIORITY typedef for DDU32
    IN LARGE_INTEGER ullTimeOut; // The Time out value for Wait event. This will be looked only for Wait operation.
    OUT LONG lOpResult;          // Return Value. Varies based on the operation.
} SB_WIGIG_EVENTOBJ_PARAMS, *PSB_WIGIG_EVENTOBJ_PARAMS;

typedef struct _SB_SPI_ALLEVENTS_DATA
{
    SB_SPI_EVENT_DATA stSPIEventData[MAX_DP_PORTS * 2]; // This is even to add even for HDMI related ports..
    DDU32             ulNumEventsDetected;              // Num Events actually Detected based on SPI..
    DDU32             ulMaxNumEvents;                   // Maximum Events that can be actually detected. Should be initialized to MAX_DP_PORTS
} SB_SPI_ALLEVENTS_DATA, *PSB_SPI_ALLEVENTS_DATA;

typedef struct _SB_SPI_DATA
{
    IN DDU32 ulNumSPIDetected; // Number of SPI's called during the worker thread..Should be always less than MAX_DP_PORTS
    IN SB_SP_INT_ID       eSPIDetected[MAX_DP_PORTS];
    SB_SPI_ALLEVENTS_DATA stAllSPIEvents;
} SB_SPI_DATA, *PSB_SPI_DATA;

// Always dynamically allocate the below structure because of the array size..
typedef struct _SB_GET_SBIOS_EDID
{
    IN DDU32 ulDisplayUid;
    OUT DDU32 ulEdidSize; // Actual EDID Size retrieved from SBIOS
    OUT UCHAR ucEdidData[256];
} SB_GET_SBIOS_EDID, *PSB_GET_SBIOS_EDID;

typedef struct _IOCTL_ARGS
{
    DDU32 *   pInputBuffer;
    DDU32     InputBufferLength;
    DDU32 *   pOutputBuffer;
    DDU32     OutputBufferLength;
    WCHAR *   pDeviceName;
    DDU32     DesiredAccess;
    DDU32     FileAttributes;
    DDU32     CreateDisposition;
    DDU32     CreateOptions;
    DDU32     IoControlCode;
    DDU64_PTR BytesReturned;
} IOCTL_ARGS, *PIOCTL_ARGS;

typedef enum _SPB_SYNC_EVENT
{
    CS_ENTRY = 1,
    CS_EXIT,
    MIPI_REMOVED_FROM_ACTIVE_TOPOLOGY,
    MIPI_ADDED_TO_ACTIVE_TOPOLOGY,
    PRE_DSI_OFF,
    POST_DSI_OFF,
    PRE_DSI_ON,
    POST_DSI_ON,
} SPB_SYNC_EVENT;

typedef struct _SB_WGBOX_PARAMS_REC
{
    struct
    {
        /* IN  */ struct
        {
            DDU32 Sps;
            DDU32 Pps;
        } Size; // 128 DDU32S + SPSSize + PPSSize
        /* OUT */ void *pCpuAddress;
        /* OUT */ DDU64 GfxAddress;
        /* OUT */ DDU64 Pitch;
        /* OUT */ DDU32 PpsOffset; // 64b Cache Line Aligned
        /* OUT */ DDU32 SpsOffset; // 64b Cache Line Aligned
    } SB_EncodeState;

    struct
    {
        /* IN  */ DDU32 BaseHeight;
        /* IN  */ DDU64 BaseWidth;
        /* IN  */ DDU32 Format;
        /* OUT */ DDU64 GfxAddress;
        /* OUT */ DDU64 Pitch;
        /* OUT */ DDU64 UOffsetY;
        /* OUT */ DDU64 VOffsetY;
    } SB_EncodeDisplaySurface, SB_EncodeReferenceSurface;

    struct
    {
        /* IN  */ DDU32 Entries;
        /* IN  */ DDU32 EntrySize;
        /* OUT */ void *pCpuAddress;
        /* OUT */ DDU64 GfxAddress;
        /* OUT */ DDU64 Pitch;
    } SB_EncodeTfdSurface;

    struct
    {
        /* IN  */ DDU32 EncodeState : 1;
        /* IN  */ DDU32 EncodeDisplaySurface : 1;
        /* IN  */ DDU32 EncodeReferenceSurface : 1;
        /* IN  */ DDU32 EncodeTfdSurface : 1;
    } SB_Flags;
} SB_WGBOX_PARAMS;

typedef struct _SB_VRR_RR_DATA
{
    IN BOOLEAN bConstRR;
    IN DDU32 ulRR;
    IN DDU32 bFractionalRR;
} SB_VRR_RR_DATA, *PSB_VRR_RR_DATA;

typedef struct _SB_PROGRAM_VRR_ARGS
{
    // either DisplayUID or PipeIndex is passed as input. DisplayUID is passed as input to SoftBIOS alone.
    IN union {
        DDU32 ulDisplayUID;
        DDU32 ulPipeIndex;
    };
    // either FlipType (Asyncflip/Syncflip) or Request to Enable/Disable VRR is passed as input
    IN union {
        IN BOOLEAN bAsyncFlip;
        IN BOOLEAN bEnableVRRMode;
    };
    // Refresh Rate Data:  if bConstRR is set, ulRR (inidcating the constant RR value) and bFractionalRR (indicating if it is a media RR which is fractional (ulRR/1.001) or not)
    // have to be filled appropriately
    IN SB_VRR_RR_DATA stRRData;
} SB_PROGRAM_VRR_ARGS, *PSB_PROGRAM_VRR_ARGS;

// Gamma Related Args
// Pallette table is of 1024 values for 10 bit gamma. For split gamma 512 values will be de-gamma and next 512 will be the actual gamma.
// Default table size is 1024. OS will send 256 values as relative gamma. That will be interpolated to 1024 values before applying.
#define MAX_PALETTE_TABLE_SIZE 1024
// OS palette table size is 256. (Fixed from OS) We will interpolate it to 1024 values before applying.
#define MAX_OS_PALETTE_TABLE_SIZE 256

// Palette table entry structure
typedef struct _SBPALETTEENTRY
{
    UCHAR ucRed;   // Red value
    UCHAR ucGreen; // Green value
    UCHAR ucBlue;  // Blue value
} SBPALETTEENTRY, *PSBPALETTEENTRY;

typedef enum _SBGAMMA_TYPE
{
    LUT_RELATIVE = 0, // Relative gamma wil be relative to what is already applied. If CUI gamma was applied and then you try to apply-
                      // OS gamma then OS gamma will be relative to CUI gamma.
    LUT_ABSOLUTE = 1, // Absolute gamma is applied from DisplayTune app (Via CUI escape) Customer can set this as default gamma.
    LUT_DEFAULT  = 2  // This is to reset previously applied absolute gamma.
} SBGAMMA_TYPE;

// Palatte table sturcture
typedef struct _SBPALETTE_TABLE
{
    DDU16          usNumEntries;      // Number of palette entries
    DDU16          usFirstIndexEntry; // First index entry
    SBPALETTEENTRY PaletteEntries[MAX_PALETTE_TABLE_SIZE];
} SBPALETTE_TABLE, *PSBPALETTE_TABLE;

typedef struct _SBPALETTE_TABLE_EXTENDED
{
    DDU16  usNumEntries; // Number of palette entries
    DDU16 *pRedPalette;
    DDU16 *pGreenPalette;
    DDU16 *pBluePalette;
} SBPALETTE_TABLE_EXTENDED, *PSBPALETTE_TABLE_EXTENDED;

// Enum defining Pipe gamma mode
typedef enum _GMCH_PIPEGAMMA_MODE
{
    // Pipe pre csc gamma not required. Legacy non-linear blending case
    eNormalGammaMode = 0,

    // Legacy use cases (all 709 planes).
    // For CNL BT2020: Input pixel is non-linear (non-linear blending case). Pipe pre csc gamma linearizes pixel
    eSplitGammaMode,

    // Input pixel is linearized in plane level (linear blending case). Pipe pre csc gamma block uses unity curve.
    eLinearPreCscGammaMode,

    // Input pixel is linearized in plane level (linear blending case). Pipe pre csc gamma non-linearizes pixel
    eEncodePreCscGammaMode,

    // Pipe post CSC gamma not used No usage TBD?
    eBypassPostCscGammaMode
} GMCH_PIPEGAMMA_MODE;

// Gamma handler args
typedef struct _SBGAMMAHANDLER_ARGS
{
    GMCH_PIPEGAMMA_MODE ePipeGammaMode;  // Pipe Gamma Mode
    PSBPALETTE_TABLE    pSBPaletteTable; // palette table structure
    UCHAR               ucPipeIndex;     // pipe index
    UCHAR               ucPlaneIndex;    // plane index
    SBGAMMA_TYPE        eLUTType;        // absolute/relative/default
    DDU32               ulDeviceID;
    // GAMMA_MODE     eGammaMode;
    BOOLEAN bEnableFlag;
} SBGAMMAHANDLER_ARGS, *PSB_GAMMAHANDLER_ARGS;

// Arguments for checking the bandwidth availability of secure sprite
typedef struct _SB_SECURESPRITE_ARGS
{
    IN SB_MPO_CHECKMPOSUPPORT_PATH_INFO stCheckMPOPathInfo[MAX_PHYSICAL_PIPES];
    IN DDU32 ulNumPaths;
    IN DDU32 ulPipeIndex;
    IN DDU32 ulSpriteHeight;
    IN DDU32 ulSpriteWidth;
    IN DDU32 ulBitsPerPixel;

    OUT BOOLEAN bIsBWAvailable;
    OUT DDU32 ulFailureReason;
} SB_SECURESPRITE_ARGS, *PSB_SECURESPRITE_ARGS;

/**
 * Data structure for mode table used within miniport
 **/
typedef struct _SOURCE_TARGET_MODE_RELATION_INFO
{
    SOURCE_MODE_INFO           stSourceModeInfo;
    DDU32                      ulNumOfTargetModes;
    PTARGET_RELATION_MODE_INFO pTargetRelationModeInfo;
} SOURCE_TARGET_MODE_RELATION_INFO, *PSOURCE_TARGET_MODE_RELATION_INFO;

typedef struct _SOURCE_TARGET_MODE_RELATION_LIST
{
    PSOURCE_TARGET_MODE_RELATION_INFO pSrcTgtModeRelInfo;
    DDU32                             ulNumOfSrcModes;
    DDU32                             ulNumOfTotalModes;
} SOURCE_TARGET_MODE_RELATION_LIST, *PSOURCE_TARGET_MODE_RELATION_LIST;

// SB_IS_FLIPCOMPLETED_ARGS -> Interface Valid only for Vista
// This is used in _IsFlipCompleted call by MP. This call is for ensuring Flip is complete when notifying OS about the VBlank interrupt & new Start Address.
typedef struct _SB_IS_FLIPCOMPLETE_ARGS
{
    DDU32   ulPipeIndex;   // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
    BOOLEAN bFlipComplete; // Out Argument : Will be TRUE only if we are sure that flip is complete.
} SB_IS_FLIPCOMPLETE_ARGS, *PSB_IS_FLIPCOMPLETE_ARGS;

// Structure added for use in WaitForVBlank interface
// Currently only KCH uses this
typedef struct _SB_PIPE_WAIT_FOR_VBLANK_ARGS
{
    DDU32   ulPipe;
    BOOLEAN bWaitOnAnyPipeIfPrefrerredPipeDisabled;
} SB_PIPE_WAIT_FOR_VBLANK_ARGS, *PSB_PIPE_WAIT_FOR_VBLANK_ARGS;

// virtual display hot plug
//#pragma pack (1)
typedef struct __TPV_GET_SET_HOTPLUG__
{
    BOOLEAN bEnable;
    BOOLEAN bSupport;
    DDU32   ulDisplayUID;
    BOOLEAN bEDIDSupported;
    DDU32   uiEDIDSize;  // Size of the EDID passed
    UCHAR   ucEDID[512]; // EDID buffer...
} TPV_GET_SET_HOTPLUG, *PTPV_GET_SET_HOTPLUG;
//#pragma pack()

// Cursor services data structure (not supported on legacy SB code)------------

// cursor constants
#define CURSOR_COLOR_BLACK_ALPHA 0xFF000000
#define CURSOR_COLOR_WHITE_ALPHA 0xFFFFFFFF
#define CURSOR_COLOR_TRANSPARENT_ALPHA 0x00000000
#define CURSOR_COLOR_INVERTED_ALPHA 0x88000000

#define CURSOR_MAX_WIDTH_64_PIXEL (64)
#define CURSOR_MAX_HEIGHT_64_PIXEL (64)
#define CURSOR_MAX_WIDTH_128_PIXEL (128)
#define CURSOR_MAX_HEIGHT_128_PIXEL (128)
#define CURSOR_MAX_WIDTH_256_PIXEL (256)
#define CURSOR_MAX_HEIGHT_256_PIXEL (256)

#define CURSOR_MAX_PALETTE_ENTRIES 4
//// Cursor position
// typedef struct _CURSOR_POS
//{
//    short   x, y; // X and Y position for Cursor
//} CURSOR_POS;

// Cursor flags structure
typedef struct _CURSOR_FLAGS
{
    DDU32 GammaEnabled : 1; // Gamma enabled flag
    DDU32 VgaEnabled : 1;   // VGA enabled flag
    DDU32 PopEnabled : 1;   // Pop enabled flag
} CURSOR_FLAGS;

// set of available cursor operation
typedef enum _CURSOR_OPERATIONS
{
    CURSOR_GET_CAPS = 1,
    CURSOR_SET_POSITION,
    CURSOR_GET_POSITION,
    CURSOR_SET_SHAPE,
    CURSOR_GET_SHAPE,
    CURSOR_SET_PALETTE,
    CURSOR_GET_PALETTE,
    CURSOR_CONNECT_PIPE,
    CURSOR_DISCONNECT_PIPE,
    CURSOR_GET_DATA,
    CURSOR_180_ROTATION,
    CURSOR_ENABLE_DISABLE_CSC
} CURSOR_OPERATIONS;

// set of available CSC operation
typedef enum _CURSOR_CSC
{
    CUR_CSC_DISABLE = 1,
    CUR_CSC_ENABLE,
    CUR_CSC_STATUS
} CURSOR_CSC;

// cursor color mode and size
typedef enum _CURSOR_MODE
{
    CUR_DISABLED = 1,
    CUR_128_128_AND_INVERT,
    CUR_256_256_AND_INVERT,
    CUR_64_64_2BPP_3COLOR,
    CUR_64_64_2BPP_XOR,
    CUR_64_64_2BPP_4COLOR,
    CUR_64_64_32BPP_AND_INVERT,
    CUR_128_128_32BPP_ARGB,
    CUR_256_256_32BPP_ARGB,
    CUR_64_64_32BPP_ARGB,
    CUR_64_64_32BPP_XOR,   // new added cursor mode.Valid frm ILK
    CUR_128_128_32BPP_XOR, // new added cursor mode.Valid frm ILK
    CUR_256_256_32BPP_XOR  // new added cursor mode.Valid frm ILK
} CURSOR_MODE;

// Cursor args structure
typedef struct _SB_CURSOR_ARGS
{
    IN CURSOR_ID eCursorID;         // Cursor ID
    IN CURSOR_OPERATIONS eCursorOp; // cursor operations
                                    // Only one of the following structs in this union should be used at a time to avoid conflicts.
    union {
        struct
        {
            IN CURSOR_MODE eCursorMode;             // cursor format
            IN DDU32 ulPipeIndex;                   // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
            IN CURSOR_FLAGS eCursorFlags;           // use these flags to avoid b-spec violations
                                                    // ex - 256x256 32bpp ARGB (not available for VGA use)
            IN DDU32 ulBaseAddress;                 // Needed to trigger the update.
            IN PLANE_ORIENTATION ePlaneOrientation; // ORIENTATION_DEFAULT,ORIENTATION_0 = ORIENTATION_DEFAULT,ORIENTATION_180
        } Enable;

        struct
        {
            IN DDU32 ulPipeIndex; // Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
        } Disable;

        struct
        {
            IN CURSOR_FLAGS eCursorFlags; // Cursor flags
            IN DDU32 PaletteData[CURSOR_MAX_PALETTE_ENTRIES];
        } SetPalette;

        struct
        {
            IN SHORT x;
            IN SHORT y;
        } SetPosition;

        struct
        {
            struct
            {
                OUT DDU32 ulMonochrome : 1; // 0x00000001
                OUT DDU32 ulColor : 1;      // 0x00000002
            } Color;
            OUT DDU32 ulMaxWidth;  // maximum width
            OUT DDU32 ulMaxHeight; // maximum height
        } CursorCaps;

        struct
        {
            OUT DDU32 ulAttachedToPipe;              // Returns the pipe cursor is attached to.....Can be one of the values PIPE_A, PIPE_B, VIRTUAL_PIPE(Index)/
            OUT CURSOR_MODE eCursorMode;             // The cursor mode plane is configured to
            OUT DDU32 ulBaseAddress;                 // Needed to trigger the update.
            OUT PLANE_ORIENTATION ePlaneOrientation; // This gets the current curstor plane orientation
            OUT DDU32 ulCursorWidth;                 // Current cursor width
            OUT DDU32 ulCursorHeight;                // Current cursor height
            OUT DDU32 ulBitsPerPixel;                // Bits per pixel for this cursor
            OUT SHORT x;
            OUT SHORT y;
        } CursorData;

        struct
        {
            IN PLANE_ORIENTATION ePlaneOrientation;
            IN DDU32 ulBaseAddress; // Needed to trigger the update.
        } Rotation;
        struct
        {
            IN CURSOR_CSC eCursorCSCOps;
            OUT BOOLEAN bCSCStatus;
            OUT BOOLEAN bEnableAlphaBlendingCursor; // Enable alpha blending for cursor plane
        } EnableDisableCSC;
    };
    struct
    {
        IN DDU32 uiRotationAngle;
        IN BOOLEAN bVisible;
        IN DDU32 dwSourceID;
    } TPV_Pos_Data; // This is not used by Softbios for GMCH cursor operation.
} SB_CURSOR_ARGS, *PSB_CURSOR_ARGS;

// Virtual Display Cursor Args
typedef struct _SB_VHALCURSOR_SHAPE_ARGS
{
    DDU32 Flags;
    DDU32 Width;
    DDU32 Height;
    DDU32 Pitch;
    LONG  lCursorScanWidth;
    DDU32 VidPnSourceId;
    DDU8  Pixels[CURSOR_MAX_WIDTH_256_PIXEL * CURSOR_MAX_HEIGHT_256_PIXEL * CURSOR_MAX_PALETTE_ENTRIES];
    DDU32 XHot;
    DDU32 YHot;
    DDU32 uiOrientation;
} SB_VHALCURSOR_SHAPE_ARGS, *PSB_VHALCURSOR_SHAPE_ARGS;

typedef struct _SB_VHAL_GET_CURSOR_SHAPE
{
    SB_VHALCURSOR_SHAPE_ARGS stCursorShapeArgs;
    SHORT                    scursorImageId;
    DDU32                    ulDisplayID;
    BOOLEAN                  bCursorVisible;
} SB_VHAL_GET_CURSOR_SHAPE, *PSB_VHAL_GET_CURSOR_SHAPE;

// TDR args
typedef struct _SB_TDR_ARGS
{
    TDR_OPERATION eOperation;          // TDR operation
    PVOID         pOCABlobHdr;         // Pointer to OCA blob header
    PVOID         pDebugBuff;          // pointer to debug buffer
    DDU32         ulDebugBufAvailSize; // Available size of the debug buffer
    DDU32         ulOutputSize;        // output size
} SB_TDR_ARGS, *PSB_TDR_ARGS;

//
//  Macros related to displayUID

#define SB_GetDisplayType(arg) (arg >> 16)
#define MIPI_CONNECTOR 17
#define SB_IsMIPI(arg) ((arg >> 8 & 0x1F) == MIPI_CONNECTOR)
#define HDMI_CONNECTOR 6
#define SB_IsHDMI(arg) (((arg >> 8) & 0x1F) == HDMI_CONNECTOR)
#define ExtDP_CONNECTOR 14
#define SB_IsDP(arg) (((arg >> 8) & 0x1F) == ExtDP_CONNECTOR)
#define EmbDP_CONNECTOR 15
#define SB_IseDP(arg) (((arg >> 8) & 0x1F) == EmbDP_CONNECTOR)
#define TPV_CONNECTOR 16
#define SB_IsTPVLegacy(arg) (((arg >> 8) & 0x1F) == TPV_CONNECTOR)
#define WIGIG_CONNECTOR 19
#define IS_WIGIG_DISPLAY(arg) (((arg >> 8) & 0x1F) == WIGIG_CONNECTOR)
#define SB_GetConnectorIndex(arg) ((arg >> 13) & 0x7)

//#pragma pack(pop, CUIREGPACK)
