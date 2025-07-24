/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**
** Copyright (c) Intel Corporation (2005).
**
** INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
** ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
** INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
** ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
** MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
** OTHER WARRANTY.  Intel disclaims all liability, including liability for
** infringement of any proprietary rights, relating to use of the code. No license,
** express or implied, by estoppel or otherwise, to any intellectual property
** rights is granted herein.
**
**
** File Name: iHDMI.h
**
** Abstract:  HDMI defines
**
** Notes:
**
** Items In File:
**
**+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#ifndef __IHDMI_H__
#define __IHDMI_H__

typedef unsigned char BOOLEAN;
#ifndef BYTE
typedef unsigned char BYTE;
#endif
//#include "DisplayDefs.h"
/////////////////////////////////////////////////////////
//
// HDMI Parameters
//

//
// GUID for HDMI Parameters
//
#define HDMI_PARAMETERS_GUID "{6FD3BE0E-80F9-4206-86B7-3714FA439634}"
DEFINE_GUID(GUID_HDMI_PARAMETERS, 0x6fd3be0e, 0x80f9, 0x4206, 0x86, 0xb7, 0x37, 0x14, 0xfa, 0x43, 0x96, 0x34);

#define AVI_INFOFRAME_GUID "{DFCB113B-E54F-49A2-B5E3-78D0C6B4F4CB}"
DEFINE_GUID(GUID_AVI_INFOFRAME, 0xdfcb113b, 0xe54f, 0x49a2, 0xb5, 0xe3, 0x78, 0xd0, 0xc6, 0xb4, 0xf4, 0xcb);

#define HDMI_DEVICE_NAME "ABC_VEND"
#define HDMI_DEVICE_DESC "XZ05 PC VIDEO"

#define MAX_PIXEL_REPETITION 0x04    // On Cantiga only upto 4X pixel repetition is supported
#define HBR_AUDIO_SAMPLE_RATE 192000 // 192kHz is the sample rate corresponding to the HBR audio formats
#define AUDIO_CLOCK_PACKET_RATE 1500 // Audio clock packet rate of 1.5kHz has to be considered while calculating audio BW

#define BAR_INFO_LENGTH 8 // 8 bytes of barinfo

// BaseLineDataLength.
// Total size is in multiple of 4 bytes. i.e, 80/4 = 20
#define EELD_BASELINE_DATA_LENGTH 0x14

// In CTG, the HW buffer is only 64 bytes and baseline data length is 60 bytes only
// So the total size in multiple of 4 bytes is 60/4 = 15
#define EELD_CTG_BASELINE_DATA_LENGTH 0x0F

// Header = 4, Baseline Data = 80 and Vendor (INTEL) specific = 2 as per EELD spec
// 4 + 80 + = 84
#define EELD_SIZE 84

//
// HDMI command types
//
typedef enum
{
    HDMI_COMMAND_GET,
    HDMI_COMMAND_SET
} HDMI_COMMAND;

#define AVI_FLAG_ITCONTENT 0x00800000
#define AVI_FLAG_RGB_QUANT_RANGE 0x00040000
#define AVI_FLAG_SCAN_INFO 0x00000001
#define AVI_FLAG_BAR_INFO 0x00000010
#define AVI_FLAG_PAR_INFO 0x00001000

//
// CEA-861b definitions
//
#define CEA_VERSION 0x00
#define ELD_VERSION 0x01
#define EELD_VERSION 0x02
#define BASE_ELD_SIZE 0x0E
#define CEA_EDID_HEADER_SIZE 0x04
#define EELD_CEA_EDID_VERSION 0x03

//
// Basic Audio support definitions
//

#define BASIC_AUDIO_SUPPORTED 0x40
#define CEA_EXTENSION_BLOCK_BYTE_3 3
#define FL_AND_FR_SPEAKERS_CONNECTED 0x1

//
// HDMI buffer/information types
//
typedef enum _HDMI_INFO_TYPE
{
    // Non-standard or non-HDMI type
    ELD_TYPE  = 0x00, // ELD buffer type
    EELD_TYPE = 0x01, // EELD buffer type

    // Per HDMI Spec, refer Table 2-1 in HDMI EDS
    // or Table 5-8 in HDMI spec
    VS_TYPE    = 0x81, // Vendor-Specific InfoFrame type
    AVI_TYPE   = 0x82, // AVI InfoFrame type
    SPD_TYPE   = 0x83, // SPD InfoFrame type
    AUDIO_TYPE = 0x84, // Audio InfoFrame type
    MS_TYPE    = 0x85, // MPEG Source InfoFrame type

    // Non-standard or non-HDMI types
    PR_PE_TYPE              = 0x86, // Pixel Replication & Pixel Encoding(colorimetry) type
    AUDIO_CAPS_TYPE         = 0x87, // Encoder Audio Capabilities type
    AUDIO_ENABLE_FLAGS_TYPE = 0x88, // Flags for enabling / disabling audio
    AUDIO_BUFFER_CAPS_TYPE  = 0x89  // Flags for getting the encoder audio buffer capablity.
} HDMI_INFO_TYPE;

//
// InfoFrame Version Information
//
typedef enum _INFOFRAME_VERSION
{
    VS_VERSION    = 1, // Vendor-Specific InfoFrame Version 1
    AVI_VERSION   = 1, // AVI InfoFrame Version 1
    AVI_VERSION2  = 2, // AVI InfoFrame Version 2
    SPD_VERSION   = 1, // SPD InfoFrame Version 1
    AUDIO_VERSION = 1, // Audio InfoFrame Version 1
    MS_VERSION    = 1, // MPEG Source InfoFrame Version 1
    DRM_VERSION   = 1  // DRM InfoFrame Version 1
} INFOFRAME_VERSION;

//
// InfoFrame Payload Length in bytes
//
typedef enum _HDMI_INFOFRAME_LENGTH
{
    HDMI_VS_LENGTH         = 27, // Vendor-Specific InfoFrame Payload Length, including IEEE reg ID
    HDMI_AVI_LENGTH        = 13, // AVI InfoFrame Payload Length
    HDMI_SPD_LENGTH        = 25, // SPD InfoFrame Payload Length
    HDMI_AUDIO_LENGTH      = 10, // Audio InfoFrame Payload Length
    HDMI_MS_LENGTH         = 10, // MPEG Source InfoFrame Payload Length
    HDMI_PR_PE_LENGTH      = 4,  // Length of PR_PE_TYPE
    HDMI_AUDIO_CAPS_LENGTH = 4,  // Length of AUDIO_CAPS_TYPE
    DRM_LENGTH             = 26  // Length of DRM InfoFrame Payload Length
} HDMI_INFOFRAME_LENGTH;

//
// InfoFrame TOTAL Length in bytes (includes header + payload)
//
typedef enum _INFOFRAME_TOTAL_LENGTH
{
    VS_MAX_TOTAL_LENGTH = HDMI_VS_LENGTH + 4,    // Max Total size of Vendor-Specific InfoFrame
    AVI_TOTAL_LENGTH    = HDMI_AVI_LENGTH + 4,   // Total size of AVI InfoFrame
    SPD_TOTAL_LENGTH    = HDMI_SPD_LENGTH + 4,   // Total size of SPD InfoFrame
    AUDIO_TOTAL_LENGTH  = HDMI_AUDIO_LENGTH + 4, // Total size of Audio InfoFrame
    MS_TOTAL_LENGTH     = HDMI_MS_LENGTH + 4,    // Total size of MPEG Source InfoFrame
    DRM_TOTAL_LENGTH    = DRM_LENGTH + 4         // Total size of DRM InfoFrame
} INFOFRAME_TOTAL_LENGTH;

//
// Pixel Replication multipliers
//
typedef enum
{
    HDMI_PR_ONE = 0, // No repetition (ie., pixel sent once)
    HDMI_PR_TWO,     // Pixel sent 2 times (ie.,repeated once)
    HDMI_PR_THREE,   // Pixel sent 3 times
    HDMI_PR_FOUR,    // Pixel sent 4 times
    HDMI_PR_FIVE,    // Pixel sent 5 times
    HDMI_PR_SIX,     // Pixel sent 6 times
    HDMI_PR_SEVEN,   // Pixel sent 7 times
    HDMI_PR_EIGHT,   // Pixel sent 8 times
    HDMI_PR_NINE,    // Pixel sent 9 times
    HDMI_PR_TEN      // Pixel sent 10 times
} HDMI_PIXEL_REPLICATION;

//
// Pixel encoding modes
//
typedef enum
{
    HDMI_RGB256   = 0x01,
    HDMI_RGB220   = 0x02,
    HDMI_YCrCb422 = 0x04,
    HDMI_YCrCb444 = 0x08
} HDMI_COLORIMETRY;

//
// AVI InfoFrame definitions - start
//
// Scan Info
typedef enum
{
    AVI_SCAN_NODATA    = 0, // No data
    AVI_SCAN_OVERSCAN  = 1, // Overscanned (TV)
    AVI_SCAN_UNDERSCAN = 2, // Underscanned (Computer)
    AVI_SCAN_FUTURE    = 3  // Future
} AVI_SCAN_INFO;

// Bar Info
typedef enum
{
    AVI_BAR_INVALID          = 0, // Bar data not valid
    AVI_BAR_VALID_VERTICAL   = 1, // Vertical Bar data valid
    AVI_BAR_VALID_HORIZONTAL = 2, // Horizontal Bar data valid
    AVI_BAR_VALID_BOTH       = 3  // Vertical & Horizontal Bar data valid
} AVI_BAR_INFO;

// Active Format Information
typedef enum
{
    AVI_AFI_INVALID = 0, // No data
    AVI_AFI_VALID   = 1  // Active Format Information valid
} AVI_AFI_INFO;

// AVI Pixel Encoding modes
typedef enum
{
    AVI_RGB_MODE      = 0, // RGB pixel encoding mode
    AVI_YCRCB422_MODE = 1, // YCrCb 4:2:2 mode
    AVI_YCRCB444_MODE = 2, // YCrCb 4:4:4 mode
    AVI_YCRCB420_MODE = 3, // YCrCb 4:2:0 mode
    AVI_FUTURE_MODE   = 4  // Future mode
} AVI_ENCODING_MODE;

// AVI Active Format Aspect Ratio
typedef enum
{
    AVI_AFAR_SAME = 8,  // same as picture aspect ratio
    AVI_AFAR_4_3  = 9,  // 4:3 center
    AVI_AFAR_16_9 = 10, // 16:9 center
    AVI_AFAR_14_9 = 11  // 14:9 center
} AVI_AFAR_INFO;

// AVI Picture Aspect Ratio
typedef enum _AVI_PAR_INFO
{
    AVI_PAR_NODATA = 0, // No Data
    AVI_PAR_4_3    = 1, // 4:3
    AVI_PAR_16_9   = 2, // 16:9
    AVI_PAR_64_27  = 3, // 64:27
    AVI_PAR_FUTURE = 4  // Future
} AVI_PAR_INFO;

// AVI Colorimetry Information
typedef enum
{
    AVI_COLOR_NODATA      = 0, // No data
    AVI_COLOR_ITU601      = 1, // SMPTE 170M, ITU601
    AVI_COLOR_ITU709      = 2, // ITU709
    AVI_COLOR_USEEXTENDED = 3  // Use the extended colorimetry for source format
} AVI_COLOR_INFO;

// AVI Non-uniform Picture Scaling Info
typedef enum
{
    AVI_SCALING_NODATA     = 0, // No scaling
    AVI_SCALING_HORIZONTAL = 1, // horizontal scaling
    AVI_SCALING_VERTICAL   = 2, // vertical scaling
    AVI_SCALING_BOTH       = 3  // horizontal & vertical scaling
} AVI_SCALING_INFO;

// AVI RGB Quantization Range
typedef enum
{
    AVI_RGBQUANT_DEFAULT = 0, // Default value
    AVI_RGBQUANT_LIMITED = 1, // Limited Range
    AVI_RGBQUANT_FULL    = 2, // Full Range
    AVI_RGBQUANT_FUTURE  = 3  // Future use
} AVI_RGBQUANT_RANGE;

// AVI IT Content
typedef enum
{
    AVI_ITC_NODATA   = 0, // No Data  - if bITContent is 0
    AVI_ITC_GRAPHICS = 0, // Graphics - if bITContent is 1
    AVI_ITC_PHOTO    = 1, // Photo
    AVI_ITC_CINEMA   = 2, // Cinema
    AVI_ITC_GAME     = 3  // Game
} AVI_IT_CONTENT;

typedef enum
{
    AVI_EXTCOLORIMETRY_XVYCC601       = 0,
    AVI_EXTCOLORIMETRY_XVYCC709       = 1,
    AVI_EXTCOLORIMETRY_cYCC_BT2020    = 5, // ITU-R BT.2020  constant luminance cY'C'C'
    AVI_EXTCOLORIMETRY_RGB_YCC_BT2020 = 6, // ITU-R BT.2020  R'G'B' or  Y'C'C'
    AVI_EXTCOLORIMETRY_RESERVED       = 7
} AVI_EXTCOLORIMETRY_INFO;

//
// AVI InfoFrame definitions - end
//

//
// SPD InfoFrame definitions - start
//
// SPD InfoFrame Data Byte 25, refer Table-17 in CEA-861b
typedef enum
{
    SPD_SRC_UNKNOWN     = 0x00, // unknown
    SPD_SRC_DIGITAL_STB = 0x01, // Digital STB
    SPD_SRC_DVD         = 0x02, // DVD
    SPD_SRC_DVHS        = 0x03, // D-VHS
    SPD_SRC_HDD_VIDEO   = 0x04, // HDD Video
    SPD_SRC_DVC         = 0x05, // DVC
    SPD_SRC_DSC         = 0x06, // DSC
    SPD_SRC_VCD         = 0x07, // Video CD
    SPD_SRC_GAME        = 0x08, // Game
    SPD_SRC_PC          = 0x09  // PC General
} SPD_SRC_TYPES;

// SPD InfoFrame Vendor Name & Descriptor Length in bytes
typedef enum
{
    SPD_VNAME_LENGTH = 8,  // SPD Vendor Name Length in bytes
    SPD_VDESC_LENGTH = 16, // SPD Vendor Descriptor Length in bytes
} SPD_NAMEDESC_LENGTH_INFO;

//
// SPD InfoFrame definitions - end
//

//
// InfoFrame Packet Header - generic
//
typedef struct _IF_HEADER
{
    unsigned char ucType;    // InfoFrame Type
    unsigned char ucVersion; // InfoFrame Version
    unsigned char ucLength;  // InfoFrame Length
    unsigned char ucChksum;  // Checksum of the InfoFrame
} IF_HEADER, *PIF_HEADER;

// AVI InfoFrame IT Content
typedef union _AVI_IT_CONTENT_TYPE {
    unsigned char ucValue;
    struct
    {
        unsigned char bGraphicsContent : 1;
        unsigned char bPhotoContent : 1;
        unsigned char bCinemaContent : 1;
        unsigned char bGameContent : 1;
        unsigned char ucReserved : 4; // Reserved BIT(4-7)
    };
} AVI_IT_CONTENT_TYPE, *PAVI_IT_CONTENT_TYPE;

// AVI InfoFrame IT Content
typedef struct _SB_AVI_IT_CONTENT_TYPE
{
    BOOLEAN bGraphicsContent;
    BOOLEAN bPhotoContent;
    BOOLEAN bCinemaContent;
    BOOLEAN bGameContent;
} SB_AVI_IT_CONTENT_TYPE, *PSB_AVI_IT_CONTENT_TYPE;

//
// AVI InfoFrame structure
//
typedef union _AVI_IF {
    unsigned char ucAviBuf[AVI_TOTAL_LENGTH];
#pragma pack(1)
    struct
    {
        IF_HEADER IfHeader; // AVI header data
        union {
            unsigned char ucByte1;
            struct
            {
                unsigned char ucScanInfo : 2; // scan information
                unsigned char ucBarInfo : 2;  // bar information
                unsigned char ucFormat : 1;   // active format information
                unsigned char ucEncMode : 3;  // pixel encoding (RGB or YCrCb 444 or YCbCr 420)
                                              // unsigned char ucB1Rsvd  :1;     // reserved
            };
        };
        union {
            unsigned char ucByte2;
            struct
            {
                unsigned char ucAFAR : 4;        // Active Format Aspect Ratio
                unsigned char ucPAR : 2;         // Picture Aspect Ratio
                unsigned char ucColorimetry : 2; // colorimetry
            };
        };
        union {
            unsigned char ucByte3;
            struct
            {
                unsigned char ucScalingInfo : 2;    // Scaling information
                unsigned char ucRGBQuantRange : 2;  // RGB Quantization Range
                unsigned char ucExtColorimetry : 3; // Extended Colorimetry uses AVI_EXTCOLORIMETRY_INFO
                unsigned char bITContent : 1;       // IT Content
            };
        };
        union {
            unsigned char ucByte4;
            struct
            {
                unsigned char ucVIC : 7;    // Video Identification code (refer Table 13 in CEA-861b)
                unsigned char ucB4Rsvd : 1; // reserved
            };
        };
        union {
            unsigned char ucByte5;
            struct
            {
                unsigned char ucPR : 4;     // pixel repetition (refer Table 15 in CEA-861b)
                unsigned char ucCN : 2;     // IT Content Type  (Table 8-6 : HDMI 1.4a spec)
                unsigned char ucB5Rsvd : 2; // reserved
            };
        };
        union {
            unsigned char ucBarData[BAR_INFO_LENGTH];
            struct
            {
                unsigned char ucByte6;  // end of top bar(lower), set to "00"
                unsigned char ucByte7;  // end of top bar(upper), set to "00"
                unsigned char ucByte8;  // start of bottom bar(lower), set to "00"
                unsigned char ucByte9;  // start of bottom bar(upper), set to "00"
                unsigned char ucByte10; // end of left bar(lower), set to "00"
                unsigned char ucByte11; // end of left bar(upper), set to "00"
                unsigned char ucByte12; // start of right bar(lower), set to "00"
                unsigned char ucByte13; // start of right bar(upper), set to "00"
            };
        };
    };
#pragma pack()
} AVI_IF, *PAVI_IF;

//
// SPD InfoFrame structure
//
typedef union _SPD_IF {
    unsigned char ucSpdBuf[SPD_TOTAL_LENGTH];
#pragma pack(1)
    struct
    {
        IF_HEADER     IfHeader;   // SPD header data
        unsigned char ucName[8];  // Vendor Name, 8 characters
        unsigned char ucDesc[16]; // Product Description, 16 characters
        unsigned char ucSDI;      // Source Device Information
    };
#pragma pack()
} SPD_IF, *PSPD_IF;

//
// Vendor Specific InfoFrame structure
//
typedef union _VS_IF {
    unsigned char ucVsBuf[VS_MAX_TOTAL_LENGTH];
#pragma pack(1)
    struct
    {
        IF_HEADER     IfHeader;       // VS header data
        unsigned char ucIEEERegID[3]; // 3-byte IEEE registration ID
        unsigned char ucPayload[24];  // Payload bytes
    };
#pragma pack()
} VS_IF, *PVS_IF;

//
// Dynamic Range and Mastering InfoFrame structure (HDR)
//
typedef union _DRM_IF {
    unsigned char ucDRMBuf[DRM_TOTAL_LENGTH];
#pragma pack(1)
    struct
    {
        IF_HEADER IfHeader; // VS header data
        union {
            unsigned char ucByte1;
            struct
            {
                unsigned char ucEOTF : 3;   // EOTF information
                unsigned char ucB1Rsvd : 5; // reserved
            };
        };
        union {
            unsigned char ucByte2;
            struct
            {
                unsigned char ucSMDId : 3;  // Static Metadata ID information
                unsigned char ucB2Rsvd : 5; // reserved
            };
        };

        union {
            unsigned short usDisplayPrimariesX0; // 2 bytes
            struct
            {
                unsigned char ucByte3; // display_primaries_x[0], LSB
                unsigned char ucByte4; // display_primaries_x[0], MSB
            };
        };
        union {
            unsigned short usDisplayPrimariesY0; // 2 bytes
            struct
            {
                unsigned char ucByte5; // display_primaries_y[0], LSB
                unsigned char ucByte6; // display_primaries_y[0], MSB
            };
        };
        union {
            unsigned short usDisplayPrimariesX1;
            struct
            {
                unsigned char ucByte7; // display_primaries_x[1], LSB
                unsigned char ucByte8; // display_primaries_x[1], MSB
            };
        };
        union {
            unsigned short usDisplayPrimariesY1;
            struct
            {
                unsigned char ucByte9;  // display_primaries_y[1], LSB
                unsigned char ucByte10; // display_primaries_y[1], MSB
            };
        };
        union {
            unsigned short usDisplayPrimariesX2;
            struct
            {
                unsigned char ucByte11; // display_primaries_x[2], LSB
                unsigned char ucByte12; // display_primaries_x[2], MSB
            };
        };
        union {
            unsigned short usDisplayPrimariesY2;
            struct
            {
                unsigned char ucByte13; // display_primaries_y[2], LSB
                unsigned char ucByte14; // display_primaries_y[2], MSB
            };
        };
        union {
            unsigned short usWhitePointX;
            struct
            {
                unsigned char ucByte15; // white_point_x, LSB
                unsigned char ucByte16; // white_point_x, MSB
            };
        };
        union {
            unsigned short usWhitePointY;
            struct
            {
                unsigned char ucByte17; // white_point_y, LSB
                unsigned char ucByte18; // white_point_y, MSB
            };
        };
        union {
            unsigned short usMaxDisplayMasteringLuminance;
            struct
            {
                unsigned char ucByte19; // max_display_mastering_luminance, LSB
                unsigned char ucByte20; // max_display_mastering_luminance, MSB
            };
        };
        union {
            unsigned short usMinDisplayMasteringLuminance;
            struct
            {
                unsigned char ucByte21; // min_display_mastering_luminance, LSB
                unsigned char ucByte22; // min_display_mastering_luminance, MSB
            };
        };
        union {
            unsigned short usMaxCLL;
            struct
            {
                unsigned char ucByte23; // max_content_light_level, LSB
                unsigned char ucByte24; // max_content_light_level, MSB
            };
        };
        union {
            unsigned short usMaxFALL;
            struct
            {
                unsigned char ucByte25; // max_frame_average_light_level, LSB
                unsigned char ucByte26; // max_frame_average_light_level, MSB
            };
        };
    };
#pragma pack()
} DRM_IF, *PDRM_IF;

//
// AVI Infoframe structure for customization
//

#pragma pack(1)

typedef struct _AVI_INFOFRAME_CUSTOM
{
    GUID                   guid;                      // GUID
    unsigned long          dwCommand;                 // Command
    unsigned long          dwFlags;                   // Flags
    unsigned long          uiTypeCode;                // Type code of AVI Infoframe
    unsigned long          uiVersion;                 // Version of AVI Infoframe
    unsigned long          uiLength;                  // Length of AVI Info Frame
    BOOLEAN                bR3R0Valid;                // Reserved
    BOOLEAN                bITContent;                // IT Content
    unsigned char          byBarInfo[8];              // Reserved
    unsigned long          dwActiveFormatAspectRatio; // Reserved
    unsigned long          dwNonUniformScaling;       // Reserved
    unsigned long          dwRGBYCCIndicator;         // Reserved
    unsigned long          dwExtColorimetry;          // Reserved
    unsigned long          dwPixelFactor;             // Reserved
    unsigned long          bBarInfoValid;             // Reserved
    unsigned long          dwColorimetry;             // Reserved
    unsigned long          dwAspectRatio;             // Reserved
    unsigned long          dwQuantRange;              // Quantization Range
    unsigned long          dwVideoCode;               // Reserved
    unsigned long          dwScanInfo;                // Scan Information
    unsigned long          dwITContentType;           // IT Content Type
    SB_AVI_IT_CONTENT_TYPE stITContentCaps;           // IT Content Type Caps
} AVI_INFOFRAME_CUSTOM, *PAVI_INFOFRAME_CUSTOM;

#pragma pack()

//
// LinearPCM Consolidated Audio Data(CAD) structure
//
typedef union _LPCM_CAD {
    unsigned char ucValue;
    struct
    {
        unsigned char ucMaxCh_CPOn : 3; // Max channels-1 supported with CP turned ON
        unsigned char ucMaxCh_CPOf : 3; // Max channels-1 supported with CP turned OFF
        unsigned char uc20Bit : 1;      // 20-bit sample support
        unsigned char uc24Bit : 1;      // 24-bit sample support
    };
} LPCM_CAD;

//
// EDID Like Data aka ELD structure
//
typedef union _ELD {
    unsigned char ucELD[256];
#pragma pack(1)
    struct
    {
        // Byte[0] = ELD Version Number
        union {
            unsigned char ucVersion;
            struct
            {
                unsigned char ucCEA_ver : 3; // CEA Version Number
                                             // 0 - signifies CEA Version 3
                                             // 1 - signifies CEA Version 4
                unsigned char ucELD_ver : 5; // ELD Version Number
                                             //  00000b - reserved
                                             //  00001b - first rev
                                             //  00010b:11111b - reserved for future
            };
        };

        // Byte[1] = Capability Flags
        union {
            //  +------------------------+
            //  |7|6|5|4|3| 2  |  1 | 0  |
            //  +------------------------+
            //  |R|R|R|R|R|44MS|RPTR|HDCP|
            //  +------------------------+

            unsigned char ucCapFlags;
            struct
            {
                unsigned char ucHDCP : 1;   // Driver, SDVO Device, and Receiver supports HDCP
                unsigned char ucRPTR : 1;   // Receiver is repeater
                unsigned char uc44MS : 1;   // 44.1kHz multiples are supported by the sink
                                            //    0 - 88.2 & 176.kHz are not supported by sink
                                            //  1 - If 96kHz is supproted then 88.2kHz is also supported
                                            //    1 - if 192kHz is supported then 176.4 is also supported
                                            // 44.1kHz is always supported by a sink
                unsigned char ucRsvd37 : 5; // Reserved bits
            };
        };

        // Byte[2-3] = Length Parameter
        union {
            unsigned short ucLength;
            struct
            {
                unsigned short ucMNL : 3;      // Monitor Name Length 7-based
                                               // 0 = 0 and no Monitor name
                                               // 1 = MNL is 7
                                               // 2 = MNL is 8
                                               // 7 = MNL is 13
                unsigned short ucVSDBL : 3;    // VSDB length in bytes
                                               //  0 - length is ZERO and no VSDB included
                                               //  1 - VSDB byte 6 is present
                                               //  2 - VSDB byte 6-7 are present
                                               //  ...
                                               //  7 - VSDB byte 6-12 are present
                unsigned short ucSADC : 4;     // count of SAD blocks
                unsigned short ucRsvd1015 : 6; // reserved bits
            };
        };

        unsigned short usManufacturerCode; // 2-byte ID Manufacturer Code from base EDID
        unsigned short usProductCode;      // 2-byte Product Code from base EDID
        LPCM_CAD       uc48CAD;            // Consolidated Audio Descriptor for 48kHz
        LPCM_CAD       uc96CAD;            // Consolidated Audio Descriptor for 96kHz
        LPCM_CAD       uc192CAD;           // Consolidated Audio Descriptor for 192kHz
        unsigned char  ucSAB[3];           // 3-byte EIA 861B Speaker Allocation Block

        // Rest of the ELD packet
        unsigned char ucData[242]; // Monitor Descriptor - ASCII string of monitor name
                                   // VSDB as extracted from EDID strcutre
                                   // Fill in from 6th byte of VBDB onwards, ignore 1-5bytes of VBDB
                                   // SAD 0 - 3-byte CEA-861B Short Audio Descriptor for non-LPCM content
                                   // SAD 1 - 3-byte CEA-861B Short Audio Descriptor for non-LPCM content
                                   // ...
                                   // ...
                                   // SAD N - 3-byte CEA-861B Short Audio Descriptor for non-LPCM content
    };
#pragma pack()
} ELD, *PELD;

//
// CEA Short Audio Descriptor
//
typedef struct _CEA_861B_ADB
{
#pragma pack(1)
    union {
        unsigned char ucbyte1;
        struct
        {
            unsigned char ucMaxChannels : 3;     // Bits[0-2]
            unsigned char ucAudioFormatCode : 4; // Bits[3-6], see AUDIO_FORMAT_CODES
            unsigned char ucB1Reserved : 1;      // Bit[7] - reserved
        };
    };
    union {
        unsigned char ucByte2;
        struct
        {
            unsigned char uc32kHz : 1;      // Bit[0] sample rate = 32kHz
            unsigned char uc44kHz : 1;      // Bit[1] sample rate = 44kHz
            unsigned char uc48kHz : 1;      // Bit[2] sample rate = 48kHz
            unsigned char uc88kHz : 1;      // Bit[3] sample rate = 88kHz
            unsigned char uc96kHz : 1;      // Bit[4] sample rate = 96kHz
            unsigned char uc176kHz : 1;     // Bit[5] sample rate = 176kHz
            unsigned char uc192kHz : 1;     // Bit[6] sample rate = 192kHz
            unsigned char ucB2Reserved : 1; // Bit[7] - reserved
        };
    };
    union {
        unsigned char ucByte3; // maximum bit rate divided by 8kHz
        // following is the format of 3rd byte for uncompressed(LPCM) audio
        struct
        {
            unsigned char uc16Bit : 1;      // Bit[0]
            unsigned char uc20Bit : 1;      // Bit[1]
            unsigned char uc24Bit : 1;      // Bit[2]
            unsigned char ucB3Reserved : 5; // Bits[3-7]
        };
    };
#pragma pack()
} CEA_861B_ADB, *PCEA_861B_ADB;

//
// Enhanced EDID Like Data aka EELD structure
//
typedef union _EELD {
    unsigned char ucEELD[EELD_SIZE];
#pragma pack(1)
    struct
    {
        // Byte[0] = ELD Version Number
        union {
            unsigned char ucByte0;
            struct
            {
                unsigned char bReserved : 3; // Reserf
                unsigned char ucELD_ver : 5; // ELD Version Number
                                             //  00000b - reserved
                                             //  00001b - first rev
                                             //  00010b:11111b - reserved for future
            };
        };

        // Byte[1] = Vendor Version Field
        union {
            unsigned char ucVendorVersion;
            struct
            {
                unsigned char ucReserved : 3;
                unsigned char ucVELD_ver : 5; // Version number of the ELD extension.
                                              // This value is provisioned and unique to each vendor.
            };
        };

        // Byte[2] = Baseline Lenght field
        unsigned char ucBaseline_ELD_Length; // Length of the Baseline structure divided by Four.

        // Byte [3] = Reserved for future use
        unsigned char ucByte3;

        // Starting of the BaseLine EELD structure
        // Byte[4] = Monitor Name Length
        union {
            unsigned char ucByte4;
            struct
            {
                unsigned char ucMNL : 5;
                unsigned char ucCEAEDIDRevID : 3;
            };
        };

        // Byte[5] = Capabilities
        union {
            unsigned char ucCapabilities;
            struct
            {
                unsigned char ucHDCP : 1;           // Indicates HDCP support
                unsigned char ucAISupport : 1;      // Inidcates AI support
                unsigned char ucConnectionType : 2; // Indicates Connection type
                                                    // 00 - HDMI
                                                    // 01 - DP
                                                    // 10 -11  Reserved for future connection types
                unsigned char ucSADC : 4;           // Indicates number of 3 bytes Short Audio Descriptors.
            };
        };

        // Byte[6] = Audio Synch Delay
        unsigned char ucAudioSynchDelay; // Amount of time reported by the sink that the video trails audio in milliseconds.

        // Byte[7] = Speaker Allocation Block
        union {
            unsigned char ucSpeakerAllocationBlock;
            struct
            {
                unsigned char ucFLR : 1;       // Front Left and Right channels
                unsigned char ucLFE : 1;       // Low Frequency Effect channel
                unsigned char ucFC : 1;        // Center transmission channel
                unsigned char ucRLR : 1;       // Rear Left and Right channels
                unsigned char ucRC : 1;        // Rear Center channel
                unsigned char ucFLRC : 1;      // Front left and Right of Center transmission channels
                unsigned char ucRLRC : 1;      // Rear left and Right of Center transmission channels
                unsigned char ucReserved3 : 1; // Reserved
            };
        };

        // Byte[8 - 15] - 8 Byte port identification value
        unsigned char ucPortIDValue[8];

        // Byte[16 - 17] - 2 Byte Manufacturer ID
        unsigned char ucManufacturerID[2];

        // Byte[18 - 19] - 2 Byte Product ID
        unsigned char ucProductID[2];

        // Byte [20-83] - 64 Bytes of BaseLine Data
        unsigned char ucMNSandSADs[64]; // This will include
                                        // - ASCII string of Monitor name
                                        // - List of 3 byte SADs
                                        // - Zero padding

        // Vendor ELD Block should continue here!
        // No Vendor ELD block defined as of now.
    };
#pragma pack()
} EELD, *PEELD;

typedef union _EELD_EXT {
    unsigned char ucEELDExt[8];
#pragma pack(1)

    struct
    {
        unsigned long ulEELDExtVer : 4; // EELD ext version
        unsigned long bAgEn : 1;        // Aggregation enable
        unsigned long ulAgConfig : 3;   // 0-clone/Redirect, 1-wide left-right, 2-wide right-left, 3-7 reserved

        unsigned long ulAgMask : 8;       // Bitmask identifying which of the endpoints are enabled for audio playback. Bit 0 for master and bits 1-7 for following slave EP
        unsigned long ulSlaveEpCount : 4; // Specifies the number of endpoints aggregated.

        unsigned long ulAEPin1 : 3; // This is zero based, with 0 standing for DDI B, 1 for DDI C, and 2 for DDI D
        unsigned long ulAEDE1 : 3;  // This field is non-zero only in case of DP1.2 endpoints

        unsigned long ulAEPin2 : 3;
        unsigned long ulAEDE2 : 3;

        unsigned long ulAEPin3 : 3;
        unsigned long ulAEDE3 : 3;

        unsigned long ulAEPin4 : 3;
        unsigned long ulAEDE4 : 3;

        unsigned long ulAEPin5 : 3;
        unsigned long ulAEDE5 : 3;

        unsigned long ulAEPin6 : 3;
        unsigned long ulAEDE6 : 3;

        unsigned long ulAEPin7 : 3;
        unsigned long ulAEDE7 : 3;

        unsigned long ulRsvd : 2;
    };

#pragma pack()
} EELD_EXT, *PEELD_EXT;

//
// Data structure for misc HDMI data
//
typedef struct _MISC_HDMI_DATA
{
    unsigned long Colorimetry : 4; //
    unsigned long PR : 4;          // pixel repetition value
    unsigned long Reserved : 24;   // reserved bits
} MISC_HDMI_DATA, *PMISC_HDMI_DATA;

//
// Audio capability structure
//
typedef struct _DEVICE_AUDIO_CAPS
{
    unsigned long NPLDesign : 8; // max number of audio packets device can
                                 // deliver per line
    unsigned long K0 : 8;        // The overhead(in pixels) per line requied
                                 // by device for setting up audio packets when
                                 // CP is disabled
    unsigned long K1 : 8;        // The overhead(in pixels) per line requied
                                 // by device for setting up audio packets when
                                 // CP is enabled
    // Misc data
    unsigned long PR : 4;       // Pixel Replication value
    unsigned long bIsHDCP : 1;  // Driver, Device and Receiver support HDCP
    unsigned long bIsRPTR : 1;  // Receiver is HDCP repeater
    unsigned long Reserved : 2; // reserved bits
} DEVICE_AUDIO_CAPS, *PDEVICE_AUDIO_CAPS;

typedef struct _AUDIO_ENABLE_FLAGS
{
    unsigned long bIsHDMIDisplay : 1; // 1 if HDMI display, 0 if not HDMI display
    unsigned long bIsELDValid : 1;    // 1 if ELD valid, 0 if ELD not valid
    unsigned long ucReserved1 : 30;
} AUDIO_ENABLE_FLAGS, *PAUDIO_ENABLE_FLAGS;

//
// Data structure to exchange HDMI data through GetSetParameters interface
//
typedef struct _HDMI_PARAMETERS
{
#pragma pack(1)
    GUID          Guid;
    HDMI_COMMAND  dwCommand;
    unsigned char ucType;
    unsigned char ucSize;
    union {
        ELD    ELD_BUFFER;
        EELD   EELD_BUFFER;
        AVI_IF AVI_INFOFRAME;
        SPD_IF SPD_INFOFRAME;
        VS_IF  VS_INFOFRAME;
        union {
            unsigned long      dwGenData;
            unsigned char      ucAudioBufferLength;
            DEVICE_AUDIO_CAPS  stAudioCaps;
            MISC_HDMI_DATA     stMiscData;
            AUDIO_ENABLE_FLAGS flAudioEnableFlags;
        };
    };
#pragma pack()
} HDMI_PARAMETERS, *PHDMI_PARAMETERS;

//
// Audio format codes
//
typedef enum _AUDIO_FORMAT_CODES
{
    AUDIO_LPCM          = 0x0001, // Linear PCM (eg. IEC60958)
    AUDIO_AC3           = 0x0002, // AC-3
    AUDIO_MPEG1         = 0x0003, // MPEG1 (Layers 1 & 2)
    AUDIO_MP3           = 0x0004, // MP3   (MPEG1 Layer 3)
    AUDIO_MPEG2         = 0x0005, // MPEG2 (multichannel)
    AUDIO_AAC           = 0x0006, // AAC
    AUDIO_DTS           = 0x0007, // DTS
    AUDIO_ATRAC         = 0x0008, // ATRAC
    AUDIO_OBA           = 0x0009, // One Bit Audio
    AUDIO_DOLBY_DIGITAL = 0x000A, // Dolby Digital
    AUDIO_DTS_HD        = 0x000B, // DTS-HD
    AUDIO_MAT           = 0x000C, // MAT (MLP)
    AUDIO_DST           = 0x000D, // DST
    AUDIO_WMA_PRO       = 0x000E  // WMA Pro
} AUDIO_FORMAT_CODES;

//
// Data structure for byte #6 to 8 which has fixed definition
//
typedef struct _VSDB_BYTE6_TO_BYTE8
{
#pragma pack(1)

    union {
        unsigned char ucByte1;
        struct
        {
            unsigned char ucDVIDual : 1;     // Bit[0]
            unsigned char ucB1Reserved : 2;  // Bits[1-2]
            unsigned char ucDCY444 : 1;      // Bit[3] YCBCR 4:4:4 in Deep Color modes.
            unsigned char ucDC30bit : 1;     // Bit[4]
            unsigned char ucDC36bit : 1;     // Bit[5]
            unsigned char ucDC48bit : 1;     // Bit[6]
            unsigned char ucSupports_AI : 1; // Bit[7]
        };
    };

    unsigned char ucMaxTMDSClock;

    union {
        unsigned char ucByte3;
        struct
        {
            unsigned char ucB3Reserved : 6;           // Bit[0-5] reserved
            unsigned char ucILatencyFieldPresent : 1; // Bit[6]
            unsigned char ucLatencyFieldPresent : 1;  // Bits[7]
        };
    };

#pragma pack()
} VSDB_BYTE6_TO_BYTE8, *PVSDB_BYTE6_TO_BYTE8;

//
// Gamut metadata structure
//
// Note : The data is written in big endian format

// GUID for calling GBD interface
// {EEE24BDF-6D30-40bf-9BA2-139F0FFFC797}
#define DXVA_HDMI13_GBD_P0_GUID "{EEE24BDF-6D30-40BF-9BA2-139F0FFFC797}"
DEFINE_GUID(GUID_DXVA_HDMI13_GBD_P0, 0xeee24bdf, 0x6d30, 0x40bf, 0x9b, 0xa2, 0x13, 0x9f, 0xf, 0xff, 0xc7, 0x97);

#define GBD_PKT_TYPE 0x0A
#define GBD_P0_DATA_SIZE 27
#define GBD_RAW_DATA_SIZE 28
#define MAX_VERTICES_DATA 25
#define MAX_FACET_DATA 25

typedef enum _GBD_FORMAT_FLAG_ENUM
{
    eVerticesAndFacets = 0,
    eRGBminmaxRange    = 1
} GBD_FORMAT_FLAG_EN;

typedef enum _GBD_COLOR_PRECISION_ENUM
{
    eGBD8BitPrecision  = 0,
    eGBD10BitPrecision = 1,
    eGBD12BitPrecision = 2
} GBD_COLOR_PRECISION_EN;

typedef enum _GBD_COLOR_SPACE_ENUM
{
    eRGBBT709  = 0,
    exvYCC601  = 1,
    exvYCC709  = 2,
    eRGBBT2020 = 3,
    eYCCBT2020 = 4,
    eReservedColorSpace
} GBD_COLOR_SPACE_EN;

typedef enum _GBD_RGB_RANGE_DATA_INDEX_ENUM
{
    eMinRedIndex            = 0,
    eMaxRedIndex            = 1,
    eMinGreenIndex          = 2,
    eMaxGreenIndex          = 3,
    eMinBlueIndex           = 4,
    eMaxBlueIndex           = 5,
    eMaxRangeDataIndexLimit = 6
} GBD_RGB_RANGE_DATA_INDEX_EN;

//
// App needs to feel the data in this structure
//
typedef struct _GBD_P0_HDMI_1_3
{
    BOOLEAN                bEnable;         // Enable/Disable GBD profile sending
    GBD_FORMAT_FLAG_EN     eFormatFlag;     // uses GBD_FORMAT_FLAG_EN, this defines the gamut data format
    GBD_COLOR_PRECISION_EN eColorPrecision; // uses GBD_COLOR_PRECISION, this is the bit precision of GBD vertex and range data
    GBD_COLOR_SPACE_EN     eColorSpace;     // uses GBD_COLOR_SPACE_EN, this defines the color space being represented
    BOOLEAN                bUseRawGBDData;
    union {
        // If bFormatFlag is 0
        struct
        {
            BOOLEAN        bFacetMode;    // spec supports 0 alone right now
            unsigned short usNumVertices; // Number of vertices
            unsigned short usNumFacets;   // Number of faces

            // For 4 vertices of 12bits size is 18
            // Max possible with 0 facets and 28 bytes of GBD is 28-5=23 bytes
            unsigned short usVerticesData[MAX_VERTICES_DATA]; // Vertices data representation
            unsigned short usFacetsData[MAX_FACET_DATA];      // kept it as input data but to be defined based on future spec
        } Vertices_Facets_Data;

        // If eFormatFlag is 1
        struct
        {
            unsigned short usRGBPrimaryData[eMaxRangeDataIndexLimit];
        } RGB_Range_Data;
        // If bUseRawGBDData is TRUE
        unsigned char ucGBD_DATA[GBD_RAW_DATA_SIZE]; // Assign this pointer to raw GBD data
    };

} GBD_P0_HDMI_1_3, *PGBD_P0_HDMI_1_3;

#define GBD_MAX_SEQ_NUM_INDEX 16

// various GBD profiles
typedef enum _GBD_PROFILE_TYPE_ENUM
{
    eP0Profile = 0,
    eP1Profile = 1,
    eP2Profile = 2,
    eP3Profile = 3,
    eInvalidProfile
} GBD_PROFILE_TYPE_EN;

// various packet transmission options
typedef enum _GBD_PKT_SEQ_ENUM
{
    eIntermediatePktInSeq = 0,
    eFirstPktInSeq        = 1,
    eLastPktInSeq         = 2,
    eOnlyPktInSeq         = 3
} GBD_PKT_SEQ_EN;

//
// Packet header defn as per HDMI spec
//
typedef struct _GAMUT_PKT_HEADER
{
    unsigned char ucPktType; // Defines the pkt type
    union {
        unsigned char ucFieldByte;
        struct
        {
            unsigned char ucAffectedGamutInfo : 4; // BIT 3:0
            unsigned char ucGBDProfile : 3;        // BIT 6:4 ; uses GBD_PROFILE_TYPE_EN
            unsigned char ucNextField : 1;         // BIT7
        };
    };

    union {
        unsigned char ucGBDSeqInfo;
        struct
        {
            unsigned char ucCurrentGamutInfo : 4; // BIT 3:0
            unsigned char ucPacketSeq : 2;        // BIT 5:4 ; use GBD_PKT_SEQ_EN
            unsigned char ucReserved2 : 1;        // BIT 6
            unsigned char ucNoCurrentGBD : 1;     // BIT 7
        };
    };

} GAMUT_PKT_HEADER;

//
// Gamut structure contains data in following format
//
typedef struct _GAMUT_METADATA_STRUCT
{
#pragma pack(1)
    GAMUT_PKT_HEADER stPktHdr; // Gamut Metadata header data
    union {
        unsigned char ucByte1;
        struct
        {
            unsigned char ucGBDColorSpace : 3;
            // Note: GBD buffer is formatted based upon the color precision
            // 8 bit precision : 1 sign bit, 2 bits of integer, 5 bits of fraction
            // 10 bit precision : 1 sign bit, 2 bits of integer, 7 bits of fraction
            // 12 bit precision : 1 sign bit, 2 bits of integer, 9 bits of fraction
            unsigned char ucGBDColorPrecision : 2;
            unsigned char ucReserved3 : 1;
            unsigned char bFacetMode : 1;   // 0 - No facet info in GBD; 1 - Facet info in GBD
            unsigned char ucFormatFlag : 1; // uses GBD_FORMAT_FLAG_EN
        } vertices_facet_byte1;

        struct
        {
            unsigned char ucGBDColorSpace : 3;
            // Note: GBD buffer is formatted based upon the color precision
            // 8 bit precision : 1 sign bit, 2 bits of integer, 5 bits of fraction
            // 10 bit precision : 1 sign bit, 2 bits of integer, 7 bits of fraction
            // 12 bit precision : 1 sign bit, 2 bits of integer, 9 bits of fraction
            unsigned char ucGBDColorPrecision : 2;
            unsigned char ucReserved4 : 2;
            unsigned char ucFormatFlag : 1; // uses GBD_FORMAT_FLAG_EN
        } rgb_range_byte1;
    };

    // For P0 profile below is the syntax in which data will be filled
    // If Format is YUV
    // BYTE 2 : Higher 8 bits of number of vertices
    // BYTE 3 : Lower 8 bits of number of vertices
    // BYTE 4 to VSIZE+2 : Vertex data of size VSIZE,
    // where VSIZE = 3*number of vertices*GBD color precision/8 + 0.99999
    // BYTE VSIZE+3: Higher 8 bits of number of facets
    // BYTE VSIZE+4: Lower 8 bits of number of facets
    // BYTE VSIZE+5 to VSIZE+FSIZE+4 : Facet data
    // where VSIZE = number of facet data
    unsigned char ucGBDData[GBD_P0_DATA_SIZE]; // data will be filled

#pragma pack()
} GAMUT_METADATA_ST, *PGAMUT_METADATA_ST;

// Status and Data Control Channel and Structure for HDMI2.0
typedef enum _SCDCS_REQ_ID
{
    SCDC_SINK_VERSION_OFFSET    = 0x01, // Sink Version = 1
    SCDC_SOURCE_VERSION_OFFSET  = 0x02, // Source Version = 1
    SCDC_UPDATE_READ_OFFSET     = 0x10,
    SCDC_TMDS_CONFIG_OFFSET     = 0x20,
    SCDC_SCRAMBLER_STS_OFFSET   = 0x21,
    SCDC_CONFIG_0_OFFSET        = 0x30,
    SCDC_IEEE_OUI_OFFSET        = 0xD0, // 3-byte Manufacturer IEEE OUI
    SCDC_DEVICEID_STRING_OFFSET = 0xD2, // 11-byte Device ID String
    SCDC_STATUS_FLAG_OFFSET     = 0x40,
} SCDCS_REQ_ID;

typedef enum _SCDCS_CED_ID
{
    SCDC_ERR_DET_0_L      = 0x50,
    SCDC_ERR_DET_0_H      = 0x51,
    SCDC_ERR_DET_1_L      = 0x52,
    SCDC_ERR_DET_1_H      = 0x53,
    SCDC_ERR_DET_2_L      = 0x54,
    SCDC_ERR_DET_2_H      = 0x55,
    SCDC_ERR_DET_CHECKSUM = 0x56,
} SCDCS_CED_ID;

#define SCDC_SINK_VERSION 0x01
#define SCDC_SOURCE_VERSION 0x01

typedef union _SCDC_TMDS_CONFIG {
    unsigned char Value;
    struct
    {
        unsigned char Scrambling : 1;
        unsigned char HighTMDSCharRate : 1;
        unsigned char Reserved : 6;
    };
} SCDC_TMDS_CONFIG;

typedef union _SCDC_SCRAMBLER_STS {
    unsigned char Value;
    struct
    {
        unsigned char ScramblingEnabled : 1;
        unsigned char Reserved : 7;
    };
} SCDC_SCRAMBLER_STS;

typedef union _SCDC_CONFIG_0 {
    unsigned char Value;
    struct
    {
        unsigned char RREnable : 1; // bit 0
    };
} SCDC_CONFIG_0;
typedef union _SCDC_STATUS_FLAGS {
    unsigned char Value;
    struct
    {
        unsigned char ClockDetected : 1; // bit 0
        unsigned char Ch0Locked : 1;     // bit 1
        unsigned char Ch1Locked : 1;     // bit 2
        unsigned char Ch2Locked : 1;     // bit 3
        unsigned char Reserved : 4;
    };
} SCDCS_STATUS_FLAGS;

typedef union _SCDC_UPDATE_FLAGS {
    unsigned char Value;
    struct
    {
        unsigned char StatusUpdate : 1; // bit 0
        unsigned char CedUpdate : 1;    // bit 1
        unsigned char RRtest : 1;       // bit 2
        unsigned char Reserved : 5;
    };
} SCDC_UPDATE_FLAGS;

#endif //__IHDMI_H__