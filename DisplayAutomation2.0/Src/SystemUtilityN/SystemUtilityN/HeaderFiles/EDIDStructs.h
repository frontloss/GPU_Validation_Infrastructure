/*===========================================================================
; EDIDStructs.h
;----------------------------------------------------------------------------
;	Copyright (c) 2004-2005  Intel Corporation.
;	All Rights Reserved.  Copyright notice does not imply publication.
;	This software is protected as an unpublished work.  This software
;	contains the valuable trade secrets of Intel Corporation, and must
;	and must be maintained in confidence.
;
; File Description:
;	This file declares all the VESA EDID specific data types
;
;--------------------------------------------------------------------------*/
#ifndef EDIDSTRUCTS_H
#define EDIDSTRUCTS_H

//#include "..\\..\\Common\\Platform.h"

////////////////////////////////////////////
//
// Max number of EDID extensions possible
//
////////////////////////////////////////////
#define MAX_EDID_EXTENSIONS 254 // Max EDID blocks minus Block 0
#define NUM_BASEEDID_STANDARD_TIMING 8
#define MAX_BASEEDID_DTD_BLOCKS 4

#define MAX_VIC_DEFINED 128

///////////EDID Details

#define CEA_VERSION 0x00
#define CEA_861_VERSION 0x01
#define CEA_861A_VERSION 0x02
#define CEA_861B_VERSION 0x03

#define BASE_ELD_SIZE 0x0E
#define CEA_EDID_HEADER_SIZE 0x04
#define EDID_BLOCK_SIZE 128

#define MAX_NUM_SADS 15

#define IS_DP_PORT(x) ((x == INTDPA_PORT) || (x == INTDPB_PORT) || (x == INTDPC_PORT) || (x == INTDPD_PORT) || (x == INTDPE_PORT) || (x == INTDPF_PORT))
#define ABSOLUTE_DIFF(a, b) ((a > b) ? (a - b) : (b - a))
#define SB_MEM_COPY_SAFE(dest, destsize, src, src_size) memcpy_s((dest), (destsize), (src), (src_size))
#define MAKEDWORD(ucByte1, ucByte2, ucByte3, ucByte4) (ucByte1 | ucByte2 << 8 | ucByte3 << 16 | ucByte4 << 24)

typedef enum _AUDIO_FORMAT_CODES
{
    AUDIO_LPCM               = 0x0001, // Linear PCM (eg. IEC60958)
    AUDIO_DOLBY_DIGITAL      = 0x0002, // AC-3
    AUDIO_MPEG1              = 0x0003, // MPEG1 (Layers 1 & 2)
    AUDIO_MP3                = 0x0004, // MP3   (MPEG1 Layer 3)
    AUDIO_MPEG2              = 0x0005, // MPEG2 (multichannel)
    AUDIO_AAC                = 0x0006, // AAC
    AUDIO_DTS                = 0x0007, // DTS
    AUDIO_ATRAC              = 0x0008, // ATRAC
    AUDIO_OBA                = 0x0009, // One Bit Audio
    AUDIO_DOLBY_DIGITAL_PLUS = 0x000A, // Dolby Digital
    AUDIO_DTS_HD             = 0x000B, // DTS-HD
    AUDIO_DOLBY_TRUE_HD      = 0x000C, // MAT (MLP)
    AUDIO_DST                = 0x000D, // DST
    AUDIO_WMA_PRO            = 0x000E  // WMA Pro
} AUDIO_FORMAT_CODES;

PCHAR gAudioFormatCodes[16] = {
    "",       "LPCM",         "Dolby Digital", "MPEG-1",           "MPEG-3", "MPEG-2", "AAC", "DTS Audio", "ATRAC", "One-bit Audio", "Dolby Digital Plus",
    "DTS-HD", "Dolby TrueHD", "DST Audio",     "Microsoft WMA Pro"
};

typedef struct
{
#pragma pack(1)
    UCHAR nChannels : 3;
    UCHAR audFormat : 4;
    UCHAR ucReserved1 : 1;
    UCHAR uc32KHz : 1;
    UCHAR uc44KHz : 1;
    UCHAR uc48KHz : 1;
    UCHAR uc88KHz : 1;
    UCHAR uc96KHz : 1;
    UCHAR uc176KHz : 1;
    UCHAR uc192KHz : 1;
    UCHAR ucReserved2 : 1;
    UCHAR uc16bit : 1;
    UCHAR uc20bit : 1;
    UCHAR uc24bit : 1;
    UCHAR ucReserved3 : 5;
#pragma pack()
} AUDIO_SAD;

typedef struct _VSDB_BYTE6_TO_BYTE8
{
#pragma pack(1)

    union {
        UCHAR ucByte1;
        struct
        {
            UCHAR ucDVIDual : 1;     // Bit[0]
            UCHAR ucB1Reserved : 2;  // Bits[1-2]
            UCHAR ucDCY444 : 1;      // Bit[3] YCBCR 4:4:4 in Deep Color modes.
            UCHAR ucDC30bit : 1;     // Bit[4]
            UCHAR ucDC36bit : 1;     // Bit[5]
            UCHAR ucDC48bit : 1;     // Bit[6]
            UCHAR ucSupports_AI : 1; // Bit[7]
        };
    };

    UCHAR ucMaxTMDSClock;

    union {
        UCHAR ucByte3;
        struct
        {
            UCHAR ucB3Reserved : 6;           // Bit[0-5] reserved
            UCHAR ucILatencyFieldPresent : 1; // Bit[6]
            UCHAR ucLatencyFieldPresent : 1;  // Bits[7]
        };
    };

#pragma pack()
} VSDB_BYTE6_TO_BYTE8, *PVSDB_BYTE6_TO_BYTE8;

typedef struct _CEA_861B_ADB
{
#pragma pack(1)
    union {
        UCHAR ucbyte1;
        struct
        {
            UCHAR ucMaxChannels : 3;     // Bits[0-2]
            UCHAR ucAudioFormatCode : 4; // Bits[3-6], see AUDIO_FORMAT_CODES
            UCHAR ucB1Reserved : 1;      // Bit[7] - reserved
        };
    };
    union {
        UCHAR ucByte2;
        struct
        {
            UCHAR uc32kHz : 1;      // Bit[0] sample rate = 32kHz
            UCHAR uc44kHz : 1;      // Bit[1] sample rate = 44kHz
            UCHAR uc48kHz : 1;      // Bit[2] sample rate = 48kHz
            UCHAR uc88kHz : 1;      // Bit[3] sample rate = 88kHz
            UCHAR uc96kHz : 1;      // Bit[4] sample rate = 96kHz
            UCHAR uc176kHz : 1;     // Bit[5] sample rate = 176kHz
            UCHAR uc192kHz : 1;     // Bit[6] sample rate = 192kHz
            UCHAR ucB2Reserved : 1; // Bit[7] - reserved
        };
    };
    union {
        UCHAR ucByte3; // maximum bit rate divided by 8kHz
                       // following is the format of 3rd byte for uncompressed(LPCM) audio
        struct
        {
            UCHAR uc16Bit : 1;      // Bit[0]
            UCHAR uc20Bit : 1;      // Bit[1]
            UCHAR uc24Bit : 1;      // Bit[2]
            UCHAR ucB3Reserved : 5; // Bits[3-7]
        };
    };
#pragma pack()
} CEA_861B_ADB, *PCEA_861B_ADB;

typedef struct _SPEAKER_ALLOCATION
{
    UCHAR ucFLR : 1;       // Front Left and Right channels
    UCHAR ucLFE : 1;       // Low Frequency Effect channel
    UCHAR ucFC : 1;        // Center transmission channel
    UCHAR ucRLR : 1;       // Rear Left and Right channels
    UCHAR ucRC : 1;        // Rear Center channel
    UCHAR ucFLRC : 1;      // Front left and Right of Center transmission channels
    UCHAR ucRLRC : 1;      // Rear left and Right of Center transmission channels
    UCHAR ucReserved3 : 1; // Reserved
} SPEAKER_ALLOCATION;

typedef struct _ELDV2
{
#pragma pack(1)
    UCHAR              ucReserved1 : 3;
    UCHAR              ucELDVersion : 5; // Should be 0x2
    UCHAR              ucReserved2;
    UCHAR              ucBaselineELDLength;
    UCHAR              ucReserved3;
    UCHAR              ucMNL : 5; // Monitor Name Length
    UCHAR              ucCEAEDIDVersion : 3;
    UCHAR              ucHDCP : 1;           // Indicates HDCP support
    UCHAR              ucAI : 1;             // Inidcates AI support
    UCHAR              ucConnectionType : 2; // Indicates Connection type. 00: HDMI, 01: DP, 10-11: Reserved
    UCHAR              ucSADCount : 4;       // Indicates number of 3 bytes Short Audio Descriptors. Maximum 15
    UCHAR              ucAudioSyncDelay;     // The amount of latency added by the sink in units of 2 ms.
    SPEAKER_ALLOCATION stSpkrAllocation;
    UCHAR              ucPortID[8];
    UCHAR              ucManufacturerName[2];
    UCHAR              ucProductCode[2];
    UCHAR              ucMNSAndSADs[64]; // This will include: ASCII string of Monitor name, List of 3 byte SADs, Zero padding
#pragma pack()
} ELDV2, *PELDV2;

typedef struct
{
    ELDV2      m_stBaseELDV2;
    ELDV2      m_stPrunedELDV2;
    UCHAR      m_ucProgLatency;
    UCHAR      m_ucIntLatency;
    PORT_TYPES m_ePort;

} BASEAUDIOPROTOCOL, *PBASEAUDIOPROTOCOL;

// New Macros for supporting EDID 1.4

// Macros for EDID Revision and Version
#define EDID_VERSION_1 0x01
#define EDID_REVISION_4 0x04

// Macros for CVT and GTF related support in Monitor descriptor
#define EDID14_CVT_TIMING_SUPPORTED 0x04
#define EDID14_DEFAULT_GTF_SUPPORTED 0x00
#define EDID14_SECONDARY_GTF_SUPPORTED 0x02

// Macros for display device data block in CEA.
#define EDID14_DISPLAY_DEVICE_DATA_TAG 0xFF
#define EDID14_DISPLAY_DEVICE_DATA_CHILD_TAG 0x02
#define EDID14_DISPLAY_DEVICE_DATA_LENGTH 0x20
#define EDID14_DISPLAY_PORT_INTERFACE 0x09

// Macros indicating digital interfaces supported by the display.
#define EDID14_DVI_SUPPORTED 0x01
#define EDID14_DISPLAY_PORT_SUPPORTED 0x05
#define EDID14_HDMI_A_SUPPORTED 0x02
#define EDID14_HDMI_B_SUPPORTED 0x03

#define EDID14_MAX_MONITOR_DESCRIPTORS 0x03

// Macros related to EDID 1.4 Color Bit Depth support
#define EDID14_COLOR_BIT_DEPTH_UNDEFINED 0x00
#define EDID14_SIX_BITS_PER_PRIMARY_COLOR 0x06
#define EDID14_EIGHT_BITS_PER_PRIMARY_COLOR 0x08
#define EDID14_TEN_BITS_PER_PRIMARY_COLOR 0x0A
#define EDID14_TWELVE_BITS_PER_PRIMARY_COLOR 0x0C
#define EDID14_FOURTEEN_BITS_PER_PRIMARY_COLOR 0x0E
#define EDID14_SIXTEEN_BITS_PER_PRIMARY_COLOR 0x10
#define EDID14_INVALID_COLOR_BIT_DEPTH 0x07

// Macro for showing Color Bit Depth support for existing displays
#define EDID_EIGHT_BITS_PER_PRIMARY_COLOR 0x08

// Macro for Established Timings III Block descriptor
#define EST_TIMINGS_III_BLOCK_TAG 0xF7
#define EST_TIMINGS_III_BLOCK_DATA_LENGTH 0x06

// Macro for indicating byte length
#define BYTE_LENGTH 0x08

////////////////////////////////////////////
//
// Max number of EDID Blocks
//
////////////////////////////////////////////
#define MAX_EDID_BLOCKS 255 // According to E-EDID Standard doc.
#define SCDC_BLOCK_SIZE 255
// Macros for EDID Revision and Version for EDID 1.3
#define EDID_VERSION_1_3 0x01
#define EDID_REVISION_1_3 0x03

////////////////////////////////////////////
// Base EDID header
////////////////////////////////////////////
static const unsigned char BASEEDID_Header[8] = { 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00 };

// Display Range Limits Offset Flags.
// Applicable only from EDID 1.4 onwards
typedef union _EDID_RANGE_LIMITS_FLAGS {
    UCHAR ucRangeLimitOffsetFlags; // Range Limits Offset Flags
    struct
    {
        UCHAR ucVerticalRateOffset : 2;   // Vertical Rate Offset
        UCHAR ucHorizontalRateOffset : 2; // Horizontal Rate Offset
        UCHAR ucReserved : 4;             // Reserved.
    };
} EDID_RANGE_LIMITS_FLAGS, *PEDID_RANGE_LIMITS_FLAGS;

// EDID 1.4 Monitor Range Limits with CVT Support Definition block
typedef enum
{
    e4_3   = 0,
    e16_9  = 1,
    e16_10 = 2,
    e5_4   = 3,
    e15_9  = 4,
} PREFERRED_AR;

// The following structure groups the 12 bytes which are
// common between  EDID_DTD_TIMING and EDID_S3D_PRIVATE_TIMING
typedef struct _VESA_DTD_S3D_COMMON_TIMING_PART
{
#pragma pack(1)
    WORD wPixelClock; // Pixel clock / 10000

    UCHAR ucHA_low;  // Lower 8 bits of H. active pixels
    UCHAR ucHBL_low; // Lower 8 bits of H. blanking
    union {
        UCHAR ucHAHBL_high;
        struct
        {
            UCHAR ucHBL_high : 4; // Upper 4 bits of H. blanking
            UCHAR ucHA_high : 4;  // Upper 4 bits of H. active pixels
        };
    };

    UCHAR ucVA_low;  // Lower 8 bits of V. active lines
    UCHAR ucVBL_low; // Lower 8 bits of V. blanking

    union {
        UCHAR ucVAVBL_high;
        struct
        {
            UCHAR ucVBL_high : 4; // Upper 4 bits of V. blanking
            UCHAR ucVA_high : 4;  // Upper 4 bits of V. active pixels
        };
    };

    UCHAR ucHSO_low;  // Lower 8 bits of H. sync offset
    UCHAR ucHSPW_low; // Lower 8 bits of H. sync pulse width

    union {
        UCHAR ucVSOVSPW_low;
        struct
        {
            UCHAR ucVSPW_low : 4; // Lower 4 bits of V. sync pulse width
            UCHAR ucVSO_low : 4;  // Lower 4 bits of V. sync offset
        };
    };

    union {
        UCHAR ucHSVS_high;
        struct
        {
            UCHAR ucVSPW_high : 2; // Upper 2 bits of V. sync pulse width
            UCHAR ucVSO_high : 2;  // Upper 2 bits of V. sync offset
            UCHAR ucHSPW_high : 2; // Upper 2 bits of H. sync pulse width
            UCHAR ucHSO_high : 2;  // Upper 2 bits of H. sync offset
        };
    };
#pragma pack()
} VESA_DTD_S3D_COMMON_TIMING_PART, PVESA_DTD_S3D_COMMON_TIMING_PART;

////////////////////////////////////////////
//
//	18-byte DTD block
//  Refer Table 3.16, 3.17 & 3.18 of
//  EDID spec
//
////////////////////////////////////////////
typedef struct _EDID_DTD_TIMING
{
#pragma pack(1)
    union {
        VESA_DTD_S3D_COMMON_TIMING_PART timingPart;
        UCHAR                           ucVesaDTDS3DCommonTimingPart[sizeof(VESA_DTD_S3D_COMMON_TIMING_PART)];
    };

    UCHAR ucHIS_low; // Lower 8 bits of H. image size in mm
    UCHAR ucVIS_low; // Lower 8 bits of V. image size in mm
    union {
        UCHAR ucHISVIS_high;
        struct
        {
            UCHAR ucVIS_high : 4; // Upper 4 bits of V. image size
            UCHAR ucHIS_high : 4; // Upper 4 bits of H. image size
        };
    };

    UCHAR ucHBorder; // H. border in pixels
    UCHAR ucVBorder; // V. border in pixels

    union {
        UCHAR ucFlags; // Hsync & Vsync polarity, etc. flags
        struct
        {
            UCHAR ucStereo1 : 1;    // Stereo definition with bit[6:5]
            UCHAR ucHSync_Pol : 1;  // Hsync polarity (0: Neg, 1: Pos)
            UCHAR ucVSync_Pol : 1;  // Vsync polarity (0: Neg, 1: Pos)
            UCHAR ucSync_Conf : 2;  // Sync configuration
                                    // 00 : Analog composite
                                    // 01 : Bipolar analog composite
                                    // 00 : Digital composite
                                    // 00 : Digital separate
            UCHAR ucStereo2 : 2;    // Stereo definition
                                    // 00 : Normal display, no stereo
                                    // xx : Stereo definition with bit0
            UCHAR ucInterlaced : 1; // Interlaced / Non-interlaced
                                    // 0 : Non-interlaced
                                    // 1 : Interlaced
        };
    };

#pragma pack()
} EDID_DTD_TIMING, *PEDID_DTD_TIMING;

////////////////////////////////////////////
//
//	Standard timing identification
//  Refer Table 3.15 of EDID spec
//
////////////////////////////////////////////
typedef union _EDID_STD_TIMING {
    USHORT usStdTiming;

    struct
    {
#pragma pack(1)
        UCHAR ucHActive; // (HActive/8) - 31;
        struct
        {
            UCHAR ucRefreshRate : 6; // Refresh Rate - 60
            UCHAR ucAspectRatio : 2; // Aspect ratio (HActive/VActive)
                                     // 00:  1:1 Aspect ratio
                                     // 01:  4:3 Aspect ratio
                                     // 10:  5:4 Aspect ratio
                                     // 11: 16:9 Aspect ratio
        };
    };
#pragma pack()

} EDID_STD_TIMING, *PEDID_STD_TIMING;
////////////////////////////////////////////////////////
// Aspect Ratio def's as per Edid 1.3 Standard Timings
////////////////////////////////////////////////////////
#define EDID_STD_ASPECT_RATIO_16_10 0x0
#define EDID_STD_ASPECT_RATIO_4_3 0x1
#define EDID_STD_ASPECT_RATIO_5_4 0x2
#define EDID_STD_ASPECT_RATIO_16_9 0x3

////////////////////////////////////////////
//
//	Monitor range limits
//
////////////////////////////////////////////
typedef struct _MONITOR_RANGE_LIMITS
{
#pragma pack(1)

    UCHAR ucMin_vert_rate;          // Min Vertical Rate,in Hz
    UCHAR ucMax_vert_rate;          // Max Vertical Rate, in Hz
    UCHAR ucMin_horz_rate;          // Min Horizontal Rate, in Hz
    UCHAR ucMax_horz_rate;          // Max Horizontal Rate, in Hz
    UCHAR ucMax_pixel_clock;        // Max Pixel Clock,Value/10 Mhz
    UCHAR ucTiming_formula_support; // 00 - No Secondary Timing Formula Supported
                                    // 02 - Secondary GTF Curve Supported
                                    // 04 - CVT Supported
                                    // In EDID 1.4, this may indicate CVT support as well

    union {
        // If timing_formula_support is 02
        struct
        {
            UCHAR ucReserved;   // 00h
            UCHAR ucStart_freq; // Horizontal Freq, Value/2, KHz
            UCHAR ucByte_C;     // C*2
            UCHAR ucLSB_M;      // LSB of M Value
            UCHAR ucMSB_M;      // MSB of M Value
            UCHAR ucByte_K;     // K Value
            UCHAR ucByte_J;     // J*2
        };

        // If timing_formula_support is 04
        struct
        {
            UCHAR ucCVT_Version_Number; // byte 11, CVT Standard Version Number: e.g. ‘11h’ implies “Version 1.1”

            union {
                UCHAR ucByte12;
                struct
                {
                    UCHAR ucMSB_Max_Active_Pixels : 2; // bit 1:0, range is 00..11
                    UCHAR ucAddn_pixel_clock : 6;      // bit 7:2, 6bits of extra pixel clock for 0.25MHz accuracy
                                                       // takes values from 000000....111111
                };
            };

            UCHAR ucLSB_Max_ActivePixels; // byte 13, range is from 00000000...11111111

            /*7 6 5 4 3 2 1 0 Supported Aspect Ratios:
              1 _ _ _ _ 0 0 0 4 : 3 AR
              _ 1 _ _ _ 0 0 0 16 : 9 AR
              _ _ 1 _ _ 0 0 0 16 : 10 AR
              _ _ _ 1 _ 0 0 0 5 : 4 AR
              _ _ _ _ 1 0 0 0 15 : 9 AR
              _ _ _ _ _ 0 0 0 Reserved Bits: Shall be set to ‘000’*/
            union {
                UCHAR ucByte14;
                struct
                {
                    UCHAR   ucReserved2 : 3;        // bit 2:0
                    BOOLEAN bSupportedAR_15_9 : 1;  // bit 3
                    BOOLEAN bSupportedAR_5_4 : 1;   // bit 4
                    BOOLEAN bSupportedAR_16_10 : 1; // bit 5
                    BOOLEAN bSupportedAR_16_9 : 1;  // bit 6
                    BOOLEAN bSupportedAR_4_3 : 1;   // bit 7
                };
            };

            /*7 6 5 2 1 0 Preferred Aspect Ratio:
              0 0 0 _ _ 0 0 0 4 : 3 AR
              0 0 1 _ _ 0 0 0 16 : 9 AR
              0 1 0 _ _ 0 0 0 16 : 10 AR
              0 1 1 _ _ 0 0 0 5 : 4 AR
              1 0 0 _ _ 0 0 0 15 : 9 AR
              n n n _ _ 0 0 0 Reserved Values: ‘nnn’ = ‘101’ ‘111’ shall not be used.
                    4 3 CVT Blanking Support:
              _ _ _ _ 0 0 0 0 Standard CVT Blanking is not supported.
              _ _ _ _ 1 0 0 0 Standard CVT Blanking is supported.
              _ _ _ 0 _ 0 0 0 Reduced CVT Blanking is not supported.
              _ _ _ 1 _ 0 0 0 Reduced CVT Blanking is supported (preferred).
              _ _ _ _ _ 0 0 0 Reserved Bits: Shall be set to ‘000’ */

            union {
                UCHAR ucByte15;
                struct
                {
                    UCHAR   ucReserved3 : 3;          // bit 2:0
                    BOOLEAN bCVTStdBlank_Support : 1; // bit 3
                    BOOLEAN bCVTRedBlank_Support : 1; // bit 4
                    UCHAR   ucPreferredAR : 3;        // bit 7:5
                };
            };

            /*7 6 5 4 3 2 1 0 Type of Display Scaling Supported:
              1 _ _ _ 0 0 0 0 Horizontal Shrink
              _ 1 _ _ 0 0 0 0 Horizontal Stretch
              _ _ 1 _ 0 0 0 0 Vertical Shrink
              _ _ _ 1 0 0 0 0 Vertical Stretch
              _ _ _ _ 0 0 0 0 Reserved Bits: Shall be set to ‘0000’ */

            union {
                UCHAR ucByte16;
                struct
                {
                    UCHAR   ucReserved4 : 4;  // bit 3:0
                    BOOLEAN bVertStretch : 1; // bit 4
                    BOOLEAN bVertShrink : 1;  // bit 5
                    BOOLEAN bHorStretch : 1;  // bit 6
                    BOOLEAN bHorShrink : 1;   // bit 7
                };
            };

            UCHAR ucPreferred_Vertical_Refresh_Rate;
        };
    };

#pragma pack()
} MONITOR_RANGE_LIMITS, *PMONITOR_RANGE_LIMITS;

////////////////////////////////////////////
//
// Color point
//
////////////////////////////////////////////
typedef struct _COLOR_POINT
{
#pragma pack(1)

    UCHAR ucWhite_point_index_number_1;
    UCHAR ucWhite_low_bits_1;
    UCHAR ucWhite_x_1;
    UCHAR ucWhite_y_1;
    UCHAR ucWhite_gamma_1;
    UCHAR ucWhite_point_index_number_2;
    UCHAR ucWhite_low_bits_2;
    UCHAR ucWhite_x_2;
    UCHAR ucWhite_y_2;
    UCHAR ucWhite_gamma_2;
    UCHAR ucByte_15;
    UCHAR ucByte_16_17[2];

#pragma pack()
} COLOR_POINT;

////////////////////////////////////////////
//
//	Monitor description descriptor
//  Refer Table 3.19 & 3.20 of EDID spec
//
////////////////////////////////////////////
#define BASEEDID_MONITORSN_MDDATATYPE 0xFF
#define BASEEDID_ASCIISTRING_MDDATATYPE 0xFE
#define BASEEDID_MONITORRANGELIMIT_MDDATATYPE 0xFD
#define BASEEDID_MONITORNAME_MDDATATYPE 0xFC
#define BASEEDID_COLORPOINT_MDDATATYPE 0xFB
#define BASEEDID_STDTIMINGS_MDDATATYPE 0xFA

// Structure definition for Established Timings III monitor block
typedef struct _EST_TIMINGS_III_BLOCK
{
#pragma pack(1)
    // The first byte will show the VESA DMTS Standard Version.
    // The following six bytes will have the Timings Bit Mask.
    // Right now only 6 bytes are used for this!!!
    // Rest is reserved.
    UCHAR ucVesaDMTVersion;   // Byte 0 indicating the VESA DMT Version.
    UCHAR ucTimingBitMask[6]; // Next 6 bytes indicating the Timing Bit Mask Bytes used in Est Timing III.
    UCHAR bReserved[6];       // Next 6 bytes are reserved
#pragma pack()
} EST_TIMINGS_III_BLOCK, *PEST_TIMINGS_III_BLOCK;

typedef struct _MONITOR_DESCRIPTOR
{
#pragma pack(1)

    WORD  wFlag;   // = 0000 when block is used as descriptor
    UCHAR ucFlag0; // Reserved

    UCHAR ucDataTypeTag;

    UCHAR ucFlag1; // 00 for descriptor

    union {

        // Monitor S/N (ucDataTypeTag = FF)
        UCHAR ucMonitorSerialNumber[13];

        // ASCII string (ucDataTypeTag = FE)
        UCHAR ucASCIIString[13];

        // Monitor range limit (ucDataTypeTag = FD)
        MONITOR_RANGE_LIMITS MonitorRangeLimits;

        // Monitor name (ucDataTypeTag = FC)
        UCHAR ucMonitorName[13];

        // Color point (ucDataTypeTag = FB)
        COLOR_POINT ColorPoint;

        // ESTABLISHED TIMINGS III BLOCK = F7 (Added for EDID 1.4)
        EST_TIMINGS_III_BLOCK stEstTimingsIIIBlock;

        // Standard timings (ucDataTypeTag = FA)
        struct
        {
            EDID_STD_TIMING ExtraStdTiming[6];
            UCHAR           ucFixedValueOfA0; // Should be 0xA0
        };

        // Manufacturer specific value (ucDataTypeTag = 0F-00)
        UCHAR ucMfgSpecificData[13];
    };

#pragma pack()
} MONITOR_DESCRIPTOR, *PMONITOR_DESCRIPTOR;

////////////////////////////////////////////
//
//	EDID PnP ID fields
//
////////////////////////////////////////////
typedef struct _BASEEDID_PNPID
{
    union {
        UCHAR VendorProductID[10]; // Vendor / Product identification

        struct
        {
            UCHAR ManufacturerID[2]; // Bytes 8, 9: Manufacturer ID
            UCHAR ProductID[2];      // Bytes 10, 11: Product ID
            UCHAR SerialNumber[4];   // Bytes 12-15: Serial numbers
            UCHAR WeekOfManufacture; // Byte 16: Week of manufacture
            UCHAR YearOfManufacture; // Byte 17: Year of manufacture
        };
    };
} BASEEDID_PNPID, *PBASEEDID_PNPID;

//////////////////////////////////////////////
// S3D Caps Field
//////////////////////////////////////////////

typedef union _S3D_CAPS {
    UCHAR ucS3DCaps;

    struct
    {
        UCHAR ucReserved : 3;       // Bits 0,1,2 Reserved
        UCHAR ImageSize : 2;        // Field Indicating Image Size
        UCHAR uc3DMultiPresent : 2; // Bits 6,5 indicating multi 3D present support
        UCHAR uc3DPresent : 1;      // Bit 7 indicating 3D present status
    };
} S3D_CAPS, *PS3D_CAPS;

typedef union _S3D_FORMATS {
    USHORT usS3DFormats;

    struct
    {
        USHORT us3DStructureAll_0 : 1;   // Sink Supports " Frame Packing 3D Formats
        USHORT us3DStructureALL1_5 : 5;  // Reserved
        USHORT us3DStructureALL1_6 : 1;  // Sink Supports " Top & Bottom 3D Formats
        USHORT us3DStructureALL7 : 1;    // Reserved
        USHORT us3DStructureALL8 : 1;    // Sink Supports " Side by Side with horizontal sub-sampling 3D Formats
        USHORT us3DStructureALL9_15 : 7; // Reserved
    };
} S3D_FORMATS, *PS3D_FORMATS;

//
// Chromaticity structure
// Table 3.12 of Base Block for details
//
typedef struct _BASEEDID_CHROMATICITY_BLOCK
{
    union {
        UCHAR RedGreenLowBits; // Byte 1
        struct
        {
            UCHAR ucGreenYLowBits : 2; // bit 1:0
            UCHAR ucGreenXLowBits : 2; // bit 3:2
            UCHAR ucRedYLowBits : 2;   // bit 5:4
            UCHAR ucRedXLowBits : 2;   // bit 7:6
        };
    };

    union {
        UCHAR ucBlueWhiteLowBits; // Byte 2
        struct
        {
            UCHAR ucWhiteYLowBits : 2; // bit 1:0
            UCHAR ucWhiteXLowBits : 2; // bit 3:2
            UCHAR ucBlueYLowBits : 2;  // bit 5:4
            UCHAR ucBlueXLowBits : 2;  // bit 7:6
        };
    };

    UCHAR ucRedXUpperBits; // bit 9:2          Byte 3
    UCHAR ucRedYUpperBits; // bit 9:2          Byte 4

    UCHAR ucGreenXUpperBits; // bit 9:2        Byte 5
    UCHAR ucGreenYUpperBits; // bit 9:2        Byte 6

    UCHAR ucBlueXUpperBits; // bit 9:2         Byte 7
    UCHAR ucBlueYUpperBits; // bit 9:2         Byte 8

    UCHAR ucWhiteXUpperBits; // bit 9:2        Byte 9
    UCHAR ucWhiteYUpperBits; // bit 9:2        Byte 10
} BASEEDID_CHROMATICITY_BLOCK, *PBASEEDID_CHROMATICITY_BLOCK;

////////////////////////////////////////////
//
//	128-byte EDID 1.x block0 structure
//
////////////////////////////////////////////
typedef struct _BASEEDID_1_X
{
#pragma pack(1)

    //
    // Header: 8 bytes (Table 3.3 of EDID spec)
    char Header[8]; // EDID1.x header "0 FFh FFh FFh FFh FFh FFh 0"

    //
    // Vendor/Product ID: 10 bytes (Table 3.4, 3.5 & 3.6 of EDID spec)
    BASEEDID_PNPID PNPID;

    //
    // EDID structure Version/Revision: 2 bytes (Table 3.7 of EDID spec)
    UCHAR ucVersion;  // EDID version no.
    UCHAR ucRevision; // EDID revision no.

    //
    // Basic display parameters & features: 5 bytes (Table 3.8 of EDID spec)
    union {
        UCHAR ucVideoInput; // Video input definition (Refer Table 3.9 of EDID spec)

        struct
        {
            UCHAR ucSyncInput : 4; // Sync input supported (iff ucDigitInput = 0)
            UCHAR ucSetup : 1;     // Display setup (iff ucDigitInput = 0)
            UCHAR ucSigLevStd : 2; // Signal level Standard (iff ucDigitInput = 0)

            UCHAR ucDigitInput : 1; // 1: Digital input; 0: Analog input
        };
    };

    // Image size (Table 3.10 of EDID spec)
    UCHAR ucMaxHIS; // Maximum H. image size in cm
    UCHAR ucMaxVIS; // Maximum V. image size in cm

    // Gamma (display transfer characteristic)
    UCHAR ucGamma; // Display gamma value	[= (gamma*100)-100]

    // Feature support (Table 3.11 of EDID spec)
    union {
        UCHAR ucDMPSFeature; // DPMS feature support

        struct
        {
            UCHAR ucGTFSupport : 1; // GTF timing support (1: Yes)
            UCHAR ucPTM : 1;        // Preferred timing is 1st DTD (1: Yes) [Must if EDID >= 1.3]
            UCHAR ucColorSpace : 1; // Use STD color space (1:Yes) [If set ColorChars should match sRGB values in EDID spec Appendix A]
            UCHAR ucDispType : 2;   // Display type
                                    // 00: Monochrome
                                    // 01: R/G/B color display
                                    // 10: Non R/G/B multicolor display
                                    // 11: Undefined
            UCHAR ucActiveOff : 1;  // Active off (Display consumes less power/blanks out when it receives an out of range timing)
            UCHAR ucSuspend : 1;    // Suspend	(Refer VESA DPMS spec)
            UCHAR ucStandBy : 1;    // Stand-by	(Refer VESA DPMS spec)
        };
    };

    //
    // Phosphor or Filter Chromaticity: 10 bytes
    UCHAR ColorChars[10]; // Color characteristics	(Refer Table 3.12 of EDID spec)

    //
    // Established timings: 3 bytes (Table 3.14 of EDID spec)
    union {
        UCHAR EstTiming1;
        struct
        {
            UCHAR bSupports800x600_60 : 1;
            UCHAR bSupports800x600_56 : 1;
            UCHAR bSupports640x480_75 : 1;
            UCHAR bSupports640x480_72 : 1;
            UCHAR bSupports640x480_67 : 1;
            UCHAR bSupports640x480_60 : 1;
            UCHAR bSupports720x400_88 : 1;
            UCHAR bSupports720x400_70 : 1;
        };
    };
    union {
        UCHAR EstTiming2;
        struct
        {
            UCHAR bSupports1280x1024_75 : 1;
            UCHAR bSupports1024x768_75 : 1;
            UCHAR bSupports1024x768_70 : 1;
            UCHAR bSupports1024x768_60 : 1;
            UCHAR bSupports1024x768_87i : 1;
            UCHAR bSupports832x624_75 : 1;
            UCHAR bSupports800x600_75 : 1;
            UCHAR bSupports800x600_72 : 1;
        };
    };
    union {
        UCHAR MfgTimings;
        struct
        {
            UCHAR bMfgReservedTimings : 7;
            UCHAR bSupports1152x870_75 : 1;
        };
    };

    //
    // Standard timings: 8 bytes (Table 3.15 of EDID spec)
    EDID_STD_TIMING StdTiming[NUM_BASEEDID_STANDARD_TIMING]; // 8 Standard timing support

    //
    // Detailed timing section - 72 bytes (4*18 bytes)
    union {
        EDID_DTD_TIMING DTD[MAX_BASEEDID_DTD_BLOCKS]; // Four DTD data blocks

        MONITOR_DESCRIPTOR MonitorInfo[MAX_BASEEDID_DTD_BLOCKS];
    };

    UCHAR ucNumExtBlocks; // Number of extension EDID blocks
    UCHAR ucChecksum;     // Checksum of the EDID block

#pragma pack()
} BASEEDID_1_X, *PBASEEDID_1_X;

////////////////////////////////////////////
//
//	128-byte EDID 1.4 block0 structure
//  EDID 1.4 block0 structure is different from 1.3 block0
//  Thats why this new structure has been added
//  Changes are commented in the structure itself
//
////////////////////////////////////////////
typedef struct _BASEEDID_1_4
{
#pragma pack(1)

    //
    // Header: 8 bytes (Table 3.3 of EDID spec)
    char Header[8]; // EDID1.x header "0 FFh FFh FFh FFh FFh FFh 0"

    //
    // Vendor/Product ID: 10 bytes (Table 3.4, 3.5 & 3.6 of EDID spec)
    BASEEDID_PNPID PNPID;

    //
    // EDID structure Version/Revision: 2 bytes (Table 3.7 of EDID spec)
    UCHAR ucVersion;  // EDID version no.
    UCHAR ucRevision; // EDID revision no.

    //
    // Basic display parameters & features: 5 bytes (Table 3.8 of EDID spec)
    union {
        UCHAR ucVideoInput; // Video input definition (Refer Table 3.9 of EDID spec)

        struct
        {
            UCHAR ucSyncInput : 4; // Sync input supported (iff ucDigitInput = 0)
            UCHAR ucSetup : 1;     // Display setup (iff ucDigitInput = 0)
            UCHAR ucSigLevStd : 2; // Signal level Standard (iff ucDigitInput = 0)

            UCHAR ucDigitInput : 1; // 1: Digital input; 0: Analog input
        };
        // This structure has been introduced to reflect the changes in EDID 1.4 spec
        // This sturcture shows new meaning of VIDEO INPUT DEFINITION when input is digital
        struct
        {
            UCHAR ucDigitalVideoInterface : 4;        // Digital Video Interface Standard Supported.
            UCHAR ucColorBitDepth : 3;                // Color Bit Depth.
                                                      // 0 0 0 -- Color Bit Depth is undefined
                                                      // 0 0 1 -- 6 Bits per Primary Color
                                                      // 0 1 0 -- 8 Bits per Primary Color
                                                      // 0 1 1 -- 10 Bits per Primary Color
                                                      // 1 0 0 -- 12 Bits per Primary Color
                                                      // 1 0 1 -- 14 Bits per Primary Color
                                                      // 1 1 0 -- 16 Bits per Primary Color
                                                      // 1 1 1 -- Reserved (Do Not Use)
            UCHAR bIsDigitalVideoSignalInterface : 1; // Bit 7
        };
    };

    // As per the EDID spec 1.4, the following two fields can be aspect ratios as well.
    union {
        UCHAR ucMaxHIS;      // Maximum H. image size in cm
        UCHAR ucARLandscape; // Landscape Aspect raio as per EDID 1.4 spec
    };
    union {
        UCHAR ucMaxVIS;     // Maximum V. image size in cm
        UCHAR ucARPortrait; // Portrait Aspect raio as per EDID 1.4 spec
    };

    // Gamma (display transfer characteristic)
    UCHAR ucGamma; // Display gamma value	[= (gamma*100)-100]

    // Feature support (Table 3.11 of EDID spec)
    union {
        UCHAR ucDMPSFeature; // DPMS feature support

        struct
        {
            UCHAR ucContinuousDisplay : 1; // Display is continuous or non-continuous (1: Yes)
            UCHAR ucPTM : 1;               // Preferred timing mode indicates native pixel format and native RR.
            UCHAR ucColorSpace : 1;        // Use STD color space (1:Yes) [If set ColorChars should match sRGB values in EDID spec Appendix A]
            UCHAR ucDispType : 2;          // Display type
                                           // 00: Monochrome
                                           // 01: R/G/B color display
                                           // 10: Non R/G/B multicolor display
                                           // 11: Undefined
            UCHAR ucActiveOff : 1;         // Active off (Display consumes less power/blanks out when it receives an out of range timing)
            UCHAR ucSuspend : 1;           // Suspend	(Refer VESA DPMS spec)
            UCHAR ucStandBy : 1;           // Stand-by	(Refer VESA DPMS spec)
        };

        struct
        {
            UCHAR bReserved0 : 1;
            UCHAR bReserved1 : 1;
            UCHAR bReserved2 : 1;
            UCHAR ucColorEncodingFormat : 2; // Supported Color Encoding Format if Video Input is digital
                                             // 00: RGB 4:4:4
                                             // 01: RGB 4:4:4 & YCrCb 4:4:4
                                             // 10: RGB 4:4:4 & YCrCb 4:2:2
                                             // 11: RGB 4:4:4 & YCrCb 4:4:4 & YCrCb 4:2:2
            UCHAR bReserved3 : 1;
            UCHAR bReserved4 : 1;
            UCHAR bReserved5 : 1;
        };
    };

    //
    // Phosphor or Filter Chromaticity: 10 bytes
    UCHAR ColorChars[10]; // Color characteristics	(Refer Table 3.12 of EDID spec)

    //
    // Established timings: 3 bytes (Table 3.14 of EDID spec)
    union {
        UCHAR EstTiming1;
        struct
        {
            UCHAR bSupports800x600_60 : 1;
            UCHAR bSupports800x600_56 : 1;
            UCHAR bSupports640x480_75 : 1;
            UCHAR bSupports640x480_72 : 1;
            UCHAR bSupports640x480_67 : 1;
            UCHAR bSupports640x480_60 : 1;
            UCHAR bSupports720x400_88 : 1;
            UCHAR bSupports720x400_70 : 1;
        };
    };
    union {
        UCHAR EstTiming2;
        struct
        {
            UCHAR bSupports1280x1024_75 : 1;
            UCHAR bSupports1024x768_75 : 1;
            UCHAR bSupports1024x768_70 : 1;
            UCHAR bSupports1024x768_60 : 1;
            UCHAR bSupports1024x768_87i : 1;
            UCHAR bSupports832x624_75 : 1;
            UCHAR bSupports800x600_75 : 1;
            UCHAR bSupports800x600_72 : 1;
        };
    };
    union {
        UCHAR MfgTimings;
        struct
        {
            UCHAR bMfgReservedTimings : 7;
            UCHAR bSupports1152x870_75 : 1;
        };
    };

    //
    // Standard timings: 8 bytes (Table 3.15 of EDID spec)
    EDID_STD_TIMING StdTiming[NUM_BASEEDID_STANDARD_TIMING]; // 8 Standard timing support

    // Detailed timing section - 72 bytes (4*18 bytes)
    // As per the new spec 1.4, the first Detailed Timing Section should contain the PREFERED TIMING BLOCK
    EDID_DTD_TIMING PreferedTimingMode;
    // The rest 54 bytes of the Detailed Timing Section.
    union {
        EDID_DTD_TIMING DTD[MAX_BASEEDID_DTD_BLOCKS - 1]; // Three DTD data blocks

        MONITOR_DESCRIPTOR MonitorInfo[MAX_BASEEDID_DTD_BLOCKS - 1]; // Three Monitor Descriptor blocks
    };

    UCHAR ucNumExtBlocks; // Number of extension EDID blocks
    UCHAR ucChecksum;     // Checksum of the EDID block

#pragma pack()
} BASEEDID_1_4, *PBASEEDID_1_4;

//
// Private S3D timing block (total = 18 bytes)
//
typedef struct _EDID_S3D_PRIVATE_TIMING
{
#pragma pack(1)
    WORD  wFlag;   // = 0000 when block is used as descriptor
    UCHAR ucFlag0; // Reserved, 00 for descriptor

    UCHAR ucDataTypeTag; // should be 05h indicating custom s3d timing private to Intel certified panel

    UCHAR ucFlag1; // 00 for descriptor

    // union
    //{
    // VESA_DTD_S3D_COMMON_TIMING_PART timingPart;
    UCHAR ucVesaDTDS3DCommonTimingPart[sizeof(VESA_DTD_S3D_COMMON_TIMING_PART)];
    //};

    UCHAR ucFlags; // Reserved should be 0

#pragma pack()
} EDID_S3D_PRIVATE_TIMING, *PEDID_S3D_PRIVATE_TIMING;

//*****************************************************
//*****************************************************
//
// DATA STRUCTURES AND DEFINITIONS FOR CE-EXTENSION
//
//*****************************************************
//*****************************************************

/////////////////////////////////
//
// CE - Extension Block Structure
//
/////////////////////////////////
typedef struct _CE_EDID
{
    UCHAR ucTag;
    UCHAR ucRevision;
    UCHAR ucDTDOffset;
    UCHAR ucCapabilty;
    UCHAR data[123];
    UCHAR ucCheckSum;
} CE_EDID, *PCE_EDID;

////////////////////////////////////////////
//
// CE - Video Capability Data block structure
//
////////////////////////////////////////////
typedef union _VIDEO_CAP_DATA_BLOCK {
    UCHAR ucValue;
    struct
    {
        UCHAR ucCEScanBehavior : 2;       // Indicates scan behavior of CE mode
        UCHAR ucITScanBehavior : 2;       // Indicates scan behavior of IT mode
        UCHAR ucPTScanBehavior : 2;       // Indicates scan behavior of Preferred mode
        UCHAR ucQuantRangeSelectable : 1; // Indicates if RGB Quantization Range can be overridden
        UCHAR ucReserved : 1;
    };
} VIDEO_CAP_DATA_BLOCK, *PVIDEO_CAP_DATA_BLOCK;

////////////////////////////////////////////
//
// CEA Extn Block Byte3 structure
//
////////////////////////////////////////////
typedef union _CEA_EXT_CAPABILITY {
    UCHAR ucValue;
    struct
    {
        UCHAR ucTotalNativeDTDs : 4;     // Total number of DTDs in extension block
        UCHAR ucSupportsYCBCR422 : 1;    // Indicates support for YCBCR 4:2:2
        UCHAR ucSupportsYCBCR444 : 1;    // Indicates support for YCBCR 4:4:4
        UCHAR ucSupportsBasicAudio : 1;  // Indicates support for Basic audio
        UCHAR ucUnderscansITFormats : 1; // Indicates underscan behavior of IT formats
    };
} CEA_EXT_CAPABILITY, *PCEA_EXT_CAPABILITY;

////////////////////////////////////////////
//
// CE - Video Capability Data block structure
//
////////////////////////////////////////////
typedef enum
{
    FORMAT_NOT_SUPPORTED        = 0, // Format is not supported
    ALWAYS_OVERSCANNED          = 1, // Format is always overscanned
    ALWAYS_UNDERSCANNED         = 2, // Format is always underscanned
    SUPPORTS_OVER_AND_UNDERSCAN = 3  // Sink supports both overscan and underscan
} CEA_SCAN_BEHAVIOR;

////////////////////////////////////////////
//
// CE - Colorimetry data block
//
////////////////////////////////////////////
// Extended Data block type
// This bit definitions are as per CE 861-D spec
#define CEA_COLORIMETRY_DATABLOCK 0x5
#define CE_COLORIMETRY_MD0_MASK BIT0
#define CE_COLORIMETRY_MD1_MASK BIT1
#define CE_COLORIMETRY_MD2_MASK BIT3

#define CE_XVYCC601_COLORIMETRY BIT0
#define CE_XVYCC709_COLORIMETRY BIT1
#define CE_BT2020YCC_COLORIMETRY BIT6
#define CE_BT2020RGB_COLORIMETRY BIT7
typedef struct _CEA_EXT_COLORIMETRY_DATA_BLOCK
{
#pragma pack(1)

    UCHAR eCEColorimetry;

    union {
        UCHAR ucByte2;
        struct
        {
            UCHAR eCEGBDProfileSupport : 3;
            UCHAR ucReserved2 : 5;
        };
    };
#pragma pack()
} CEA_EXT_COLORIMETRY_DATA_BLOCK, *PCEA_EXT_COLORIMETRY_DATA_BLOCK;

#define CEA_HDR_STATIC_META_DATABLOCK 0x6
#define EOTF_TRADITIONAL_GAMMA_SDR BIT0
#define EOTF_TRADITIONAL_GAMMA_HDR BIT1
#define EOTF_SMPTE_ST2084 BIT2
#define EOTF_FUTURE_EOTF BIT3
#define HDR_SM_TYPE1_MASK BIT0

typedef struct _CEA_EXT_HDR_STATIC_META_DATA_BLOCK
{
#pragma pack(1)
    union {
        UCHAR ucByte1;
        struct
        {
            UCHAR eEOTFSupported : 6;
            UCHAR ucReserved1 : 2;
        };
    };
    UCHAR eSMTypesSupported;
    UCHAR DesiredMaxCLL;  // Max content luminance level
    UCHAR DesiredMaxFALL; // Max frame avereage luminance level
    UCHAR DesiredMinCLL;  // Min content luminance level
#pragma pack()
} CEA_EXT_HDR_STATIC_META_DATA_BLOCK, *PCEA_EXT_HDR_STATIC_META_DATA_BLOCK;

/////////////////////////////////
//
// #defines required for CE Etxn
//
/////////////////////////////////
#define CEA_EXT_TAG 0x02
#define CEA_EXT_SUPPORTED_VERSION 0x03
#define CEA_EXT_861_REVISION 0x01
#define CEA_EXT_861_REVISION_F 0x06

#define CEA_USE_EXTENDED_TAG 0x7

#define CEA_AUDIO_DATABLOCK 0x1
#define CEA_VIDEO_DATABLOCK 0x2
#define CEA_VENDOR_DATABLOCK 0x3
#define CEA_SPEAKER_DATABLOCK 0x4
#define CEA_VIDEO_CAP_DATABLOCK 0x0

#define CEA_DATABLOCK_TAG_MASK 0xE0
#define CEA_DATABLOCK_LENGTH_MASK 0x1F
#define CEA_SHORT_VIDEO_DESCRIPTOR_CODE_MASK 0x7F
#define CEA_NATIVE_FORMAT_BIT_MASK 0x80

#define CEA_HDMI_IEEE_REG_ID 0x00000C03
#define CEA_HDMI2_IEEE_REG_ID 0xC45DD8
#define CEA_EDID_HEADER_SZIE 0x04
#define DID_EXT_TAG 0x70

#define CEA_420_CAPABILITY_MAP_DATABLOCK 0x0F
#define CEA_420_VIDEO_DATABLOCK 0x0E
#define CEA_VIDEO_FORMAT_PREFERENCE_DATABLOCK 0x0D

//==================================================================================
//==================================================================================
//	DATA Structure definitions for VTB parsing.....
//  Reference VESA Documents are VTB Extension(Release A) & CVT standard version 1.1
//===================================================================================
//	#defines for VTB-EXT
//===================================================================================

#define VTB_EXT_TAG 0x10
#define VTB_EXT_SUPPORTED_VERSION 0x03

#define VTB_MAX_DTD_TIMINGS 6
#define VTB_MAX_CVT_TIMINGS 40
#define VTB_MAX_STANDARD_TIMINGS 61

#define VTB_DTD_OFFSET 5
#define VTB_DTD_SIZE 18
#define VTB_CVT_SIZE 3
#define VTB_ST_SIZE 2
#define VTB_DATA_SIZE 122

// This struct is for VTB Extension block.
typedef struct _VTB_EXT
{
    UCHAR ucTag;
    UCHAR ucVersion;
    UCHAR ulNumDTD;
    UCHAR ulNumCVT;
    UCHAR ulNumST;
    UCHAR DATA[VTB_DATA_SIZE];
    UCHAR ucChecksum;
} VTB_EXT, *PVTB_EXT;

// Following struct is for CVT descriptor (Version 1.1)
typedef struct _VTB_CVT_TIMING
{
#pragma pack(1)

    UCHAR ucVA_low; // Lower 8 bits of Vertical size. This Vsize = (vertical active lines/2)-1.
                    //	Range for VA lines is 2 to 8192. CVT supprts only an even no. of active lines per frame.

    union {
        UCHAR ucVA_high_AR;
        struct
        {

            UCHAR ucReserved00 : 2;  // Bits 1-0 are reserved and set to 00h
            UCHAR ucAspectRatio : 2; //	Aspect Ratio specifier bits.
                                     // 00:	 4:3 Aspect ratio
                                     // 01:	16:9 Aspect ratio
                                     // 10:	16:10 Aspect ratio
                                     // 11: Undefined (Reserved)

            UCHAR ucVA_high : 4; //	Upper 4 bits of Vertical Size.
        };
    };

    union {
        UCHAR ucRefresh_Rate_Bits;
        struct
        {

            UCHAR ucRR_60Hz_RB : 1;            // When set, indicates 60Hz support with Reduced Blanking.
            UCHAR ucRR_85Hz : 1;               //				||	   85Hz				||												.
            UCHAR ucRR_75Hz : 1;               //				||	   75Hz				||												.
            UCHAR ucRR_60Hz : 1;               //				||	   60Hz				||												.
            UCHAR ucRR_50Hz : 1;               // When set, indicates 50Hz Refrash Rate with CRT Blanking supports specified pixel format.
            UCHAR ucPreferredRefresh_Rate : 2; // Preferred Refresh Rate specifier bits.
                                               // 00:	50 Hz
                                               // 01:	60 Hz (this means either CRT blanking or Reduced Blanking whichever is supported.
                                               //				If both are supported, then RB is preferred.)
                                               // 10:	75 Hz
                                               // 11:	85 Hz

            UCHAR ucReserved0 : 1; // This bit is reserved and set to '0'.
        };
    };
#pragma pack()
} VTB_CVT_TIMING, *PVTB_CVT_TIMING;

// This struct is for storing extracted Info from CVT descriptor....
// This is defined by author.....not based on CVT specs.
typedef struct _CVT_INFO
{
    ULONG   ulYRes;
    ULONG   ulXRes;
    ULONG   ulRRate[5]; // As max 5 Refresh Rates can be supported.
    BOOLEAN bRed_Blank_Req[5];
    BOOLEAN bPreferred_RR[5]; // To set flag for Preffered RR
    ULONG   ulNumRates;       // Number of Refresh rates Supported. (Max. 5)
} CVT_INFO, *PCVT_INFO;

typedef struct _HF_VSDB_INFO
{
    ULONG   ulThirdOctet;
    ULONG   ulSecondOctet;
    ULONG   ulFirstOctet;
    ULONG   ulVersion;
    ULONG   ulMaxTMDSCharRate;
    BOOLEAN bSCDCPresent;
    BOOLEAN bRRCapable;
    BOOLEAN bLTE_340Mcsc_Scramble;
    BOOLEAN bDC_48Bit_420;
    BOOLEAN bDC_36Bit_420;
    BOOLEAN bDC_30Bit_420;
} HF_VSDB_INFO, *PHF_VSDB_INFO;

// This structure is for stroing the Display device Data retreived from CEA block
// This is defined as per the Display Device Data Block standard.
typedef struct _DISPLAY_DEVICE_DATA
{
#pragma pack(1)
    union {
        UCHAR ucTagAndLength; // Data Block Tag and Block Length. should be 0xFF
        struct
        {
            UCHAR ucLength : 5;
            UCHAR ucTag : 3;
        };
    };
    UCHAR ucChildTag; // Child tag required as per CEA spec  should be 0x02
    union {
        UCHAR ucInterfaceType;
        struct
        {
            UCHAR ucNumOfChannels : 4; // Number of channels supported
            UCHAR ucInterfaceCode : 4; // Interface code
        };
    };
    union {
        UCHAR ucVerAndRel;
        struct
        {
            UCHAR ucRelease : 4; // Release
            UCHAR ucVersion : 4; // Version.
        };
    };
    UCHAR ucContentProtectionSuppFlag; // Flag indicating support for content protection.
    union {
        USHORT usClockFrequency; // Clock Frequency
        struct
        {
            USHORT usMinClockFrequency : 6;  // First 6 bits indicates Min frequency
            USHORT usMaxClockFrequency : 10; // Next 10 bits indicates Max frequency
        };
    };
    union {
        UCHAR ucNativePixelFormat[4]; // Pixel Format
        struct
        {
            UCHAR ucHorizontalPixelCntLower; // Lower byte value of the Horizontal pixel count
            UCHAR ucHorizontalPixelCntUpper; // Upper byte value of the Horizontal pixel count
            UCHAR ucVerticalPixelCntLower;   //  Lower byte value of the vertical pixel count
            UCHAR ucVerticalPixelCntUpper;   // Upper byte value of the vertical pixel count
        };
    };
    UCHAR ucAspectRatio; // Byte indicating Aspect ratio.
    union {
        UCHAR ucOrientationAndRotation;
        struct
        {
            UCHAR ucScanDirection : 2;      // Scan direction.
            UCHAR ucZeroPixelLocation : 2;  // Zero Pixel Location.
            UCHAR ucRotationCapability : 2; // Indicates rotation capability
            UCHAR ucDefaultOrientation : 2; // Default Orientation.
        };
    };
    UCHAR ucSubPixelInfo;    // Sub-Pixle Information.
    UCHAR ucHorizontalPitch; // Horizontal Pitch
    UCHAR ucVerticalPitch;   // Vertical Pitch
    union {
        UCHAR ucMiscDisplayCapabilities;
        struct
        {
            UCHAR bReserved : 3;
            UCHAR ucDeinterlacing : 1; // indicates deinterlacing support
            UCHAR ucOverdriverNotRecommended : 1;
            UCHAR ucDirectDrive : 1; // indicates DirectDrive support
            UCHAR ucDithering : 2;   // indicates Dithering support.
        };
    };
    union {
        UCHAR ucAudioFlags; // Flags indicating Audio details
        struct
        {
            UCHAR bReserved1 : 4;
            UCHAR ucAudioInputOverride : 1;         // Indicates Audio Input Override
            UCHAR ucSeparateAudioInputs : 1;        // Indicates Separate Audio Inputs
            UCHAR ucAudioInputOnVideoInterface : 1; // Shows whether Audio input is through the video interface.
        };
    };
    union {
        UCHAR ucAudioDelayFlags; // Audio Delay Flags
        struct
        {
            UCHAR ucAudioDelay : 7; // Absolute offset between the audio and video signals.
            UCHAR ucAudioSign : 1;  // Indicates positive or negative delay.
        };
    };
    union {
        UCHAR ucFrameRateAndModeConversion;
        struct
        {
            UCHAR ucFrameRateRange : 6;      // Device Frame rate Range
            UCHAR ucFrameRateConversion : 2; // 00 – No dedicated rate conversion hardware is provided;
                                             // 01 – The display provides a single frame buffer
                                             // 10 – The display provides double-buffering
                                             // 11- The display provides frame-rate conversion involving interframe interpolation
        };
    };
    UCHAR ucDeviceNativeRate; // Device Native Frame rate
    union {
        UCHAR ucColorBitDepth; // Color bit depth
        struct
        {
            UCHAR ucDisplayDeviceColBitDepth : 4; // Color bit depth of the display device
            UCHAR ucInterfaceColBitDepth : 4;     // color bit depth supported by the interface.h
        };
    };
    UCHAR ucAddPrimaryChromaticities[8]; // Additional Primary Chromaticities.
    union {
        UCHAR ucResponseTimeFlags;
        struct
        {
            UCHAR ucResponseTime : 7; // Time for transition.
            UCHAR ucBlackToWhite : 1; // if 1, then transition from black to white
                                      // if 0, then transition from white to black
        };
    };
    union {
        UCHAR ucOverscanInformation;
        struct
        {
            UCHAR ucVerticalPercentage : 4;   // Percentage of Overscan in vertical direction.
            UCHAR ucHorizontalPercentage : 4; // Percentage of Overscan in horizontal direction.
        };
    };
#pragma pack()
} DISPLAY_DEVICE_DATA, *PDISPLAY_DEVICE_DATA;

//=========================================================================
//=========================================================================
// #defines for Block Map Ext.
//=========================================================================
//=========================================================================
#define BLOCK_MAP_EXT_TAG 0xF0

#endif // EDIDSTRUCTS_H
