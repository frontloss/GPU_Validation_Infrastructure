/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**
** Copyright (c) Intel Corporation (1998-2003).
**
** INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
** ON AN ""AS IS"" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
** INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
** ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
** MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
** OTHER WARRANTY.  Intel disclaims all liability, including liability for
** infringement of any proprietary rights, relating to use of the code. No license,
** express or implied, by estoppel or otherwise, to any intellectual property
** rights is granted herein.
**
**
** File Name:   	itvout.h
**
** Abstract:
**
**
** Environment: 	Win95, Win98, WinNT
**
** Notes:           This file is only required as a temporary header, to be used
**                  only until Microsoft releases the "tvout.h" file that the
**                  Windows 98 DDK documentation refers to.
**
**+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#ifndef __ITVOUT_H__
#define __ITVOUT_H__

#ifdef _COMMON_PPA
#include "OMPTool.h"
#endif

#ifndef DWORD
typedef unsigned long DWORD;
#endif

#ifndef ULONGLONG
typedef unsigned __int64 ULONGLONG;
#endif

#if (_WIN32_WINNT == 0x0400) // NT4 build
#ifndef INITGUID
#include <guiddef.h>
#endif
#endif // NT4 build

//#if (_WIN32_WINNT == 0x0500) // NT5 build
#include <tvout.h> // this will define VIDEOPARAMETERS
//#endif

// This definition needs to be included outside because tvout.h is included already and the
// ifndef VP_COMMAND_GET becomes false and hence the new format is not getting defined
// PAL_NC RCR Changes
#define VP_TV_STANDARD_PAL_NC 0x00100000
#define VPNEWPOLICY 0xF9
#define VPOLDPOLICY 0x00

// Passive is for Vista only   to handle TDR (as OS does not understand VideoParameter).
// There can be any possible combinations like passive with oldpolicy, active with newpolicy etc.,
// Set bOEMCopyProtection[3] = VP_UPDATE_TVPARAMS_PASSIVELY //Driver will just update the TV Parameters and will not do any settiming nor update any information
// Set bOEMCopyProtection[3] = VP_UPDATE_TVPARAMS_ACTIVELY //Driver will update the TV Parameters and will do settiming

#define VP_UPDATE_TVPARAMS_PASSIVELY 0x01
#define VP_UPDATE_TVPARAMS_ACTIVELY 0x00

// bOEMCopyProtection[4] is used by UAIM to indicate CUI that it is SDVO TVOUT
// Bug #2447996-If bOEMCopyProtection[4] == VP_SDVO_TVOUT, CUI will issue a passive update when Overscan is changed.
#define VP_SDVO_TVOUT 0x01

#define TV_VP_GUID "{02C62061-1097-11d1-920F-00A024DF156E}"
DEFINE_GUID(GUID_TV_VP, 0x02C62061, 0x1097, 0x11d1, 0x92, 0x0F, 0x00, 0xA0, 0x24, 0xDF, 0x15, 0x6E);

#ifndef VP_COMMAND_GET // if MS TVOUT.H isn't already included

// dwCommand defines
#define VP_COMMAND_GET \
    0x0001                    // return capabilities.
                              // return dwFlags = 0 if not supported.
#define VP_COMMAND_SET 0x0002 // parameters set.

// dwFlags
#define VP_FLAGS_TV_MODE 0x0001
#define VP_FLAGS_TV_STANDARD 0x0002
#define VP_FLAGS_FLICKER 0x0004
#define VP_FLAGS_OVERSCAN 0x0008
#define VP_FLAGS_MAX_UNSCALED 0x0010 // do not use on SET
#define VP_FLAGS_POSITION 0x0020
#define VP_FLAGS_BRIGHTNESS 0x0040
#define VP_FLAGS_CONTRAST 0x0080
#define VP_FLAGS_COPYPROTECT 0x0100

// dwMode
#define VP_MODE_WIN_GRAPHICS \
    0x0001 // the display is optimized for Windows
           // FlickerFilter on and OverScan off
#define VP_MODE_TV_PLAYBACK \
    0x0002 // optimize for TV video playback:
           // FlickerFilter off and OverScan on

// dwTVStandard
#define VP_TV_STANDARD_NTSC_M 0x0001   //        75 IRE Setup
#define VP_TV_STANDARD_NTSC_M_J 0x0002 // Japan,  0 IRE Setup
#define VP_TV_STANDARD_PAL_B 0x0004
#define VP_TV_STANDARD_PAL_D 0x0008
#define VP_TV_STANDARD_PAL_H 0x0010
#define VP_TV_STANDARD_PAL_I 0x0020
#define VP_TV_STANDARD_PAL_M 0x0040
#define VP_TV_STANDARD_PAL_N 0x0080
#define VP_TV_STANDARD_SECAM_B 0x0100
#define VP_TV_STANDARD_SECAM_D 0x0200
#define VP_TV_STANDARD_SECAM_G 0x0400
#define VP_TV_STANDARD_SECAM_H 0x0800
#define VP_TV_STANDARD_SECAM_K 0x1000
#define VP_TV_STANDARD_SECAM_K1 0x2000
#define VP_TV_STANDARD_SECAM_L 0x4000
#define VP_TV_STANDARD_WIN_VGA 0x8000 // the display can do VGA graphics
#define VP_TV_STANDARD_NTSC_433 0x00010000
#define VP_TV_STANDARD_PAL_G 0x00020000
#define VP_TV_STANDARD_PAL_60 0x00040000
#define VP_TV_STANDARD_SECAM_L1 0x00080000

// dwAvailableModes
#define VP_MODE_WIN_GRAPHICS \
    0x0001                         // optimize for Windows display:
                                   // max FlickerFilter and OverScan off
#define VP_MODE_TV_PLAYBACK 0x0002 // optimize for TV video playback:

// FlickerFilter off and OverScan on
// dwAvailableTVStandard
// see dwTVStandard

// dwCPType
#define VP_CP_TYPE_APS_TRIGGER 0x0001 // DVD trigger bits only
#define VP_CP_TYPE_MACROVISION 0x0002

// dwCPCommand
#define VP_CP_CMD_ACTIVATE 0x0001 // CP command type
#define VP_CP_CMD_DEACTIVATE 0x0002
#define VP_CP_CMD_CHANGE 0x0004

/*
typedef struct _MACROVISION {
  WORD    wVersion;
  WORD    wFlags;
  BYTE    bCPCData;
  BYTE    bCPSData[34];
} MACROVISION, *PMACROVISION, FAR *LPMACROVISION;
*/

#define MV_FLAGS_CPC_ONLY 0x0001
#define MV_FLAGS_CPS_ONLY 0x0002 // don't know if this is valid or not.
#define MV_FLAGS_CPC_CPS 0x0004  // both 8 bit and 132 bits are defined.

typedef struct _VIDEOPARAMETERS
{
    GUID  Guid;
    DWORD dwOffset;
    DWORD dwCommand;
    DWORD dwFlags;
    DWORD dwMode;
    DWORD dwTVStandard;
    DWORD dwAvailableModes;
    DWORD dwAvailableTVStandard;
    DWORD dwFlickerFilter;
    DWORD dwOverScanX;
    DWORD dwOverScanY;
    DWORD dwMaxUnscaledX;
    DWORD dwMaxUnscaledY;
    DWORD dwPositionX;
    DWORD dwPositionY;
    DWORD dwBrightness;
    DWORD dwContrast;
    DWORD dwCPType;
    DWORD dwCPCommand;
    DWORD dwCPStandard;
    DWORD dwCPKey;
    BYTE  bCP_APSTriggerBits;
    BYTE  bOEMCopyProtection[256];
} VIDEOPARAMETERS, *PVIDEOPARAMETERS, FAR *LPVIDEOPARAMETERS;

#endif // ifndef VP_COMMAND_GET (tvout.h)

#ifndef VIDEO_PARAMETER
#define VIDEO_PARAMETER 0x13077
#endif

/////////////////////////////////////////////////////////
//
// Extended TV Control
//
#define EXTV_COMMAND_GET 0x0001
#define EXTV_COMMAND_SET 0x0002

#define EXTV_FLAG_NOT_SUPPORTED 0x0000
#define EXTV_FLAG_SHARPNESS 0x0001
#define EXTV_FLAG_ADAPTIVE_FF 0x0002
#define EXTV_FLAG_2D_FF 0x0004
#define EXTV_FLAG_SATURATION 0x0008
#define EXTV_FLAG_HUE 0x0010
#define EXTV_FLAG_DOTCRAWL 0x0020
#define EXTV_FLAG_LUMA_FLTR 0x0040
#define EXTV_FLAG_CHROMA_FLTR 0x0080

// Following are the Flags related to Different Connectors.
// This were added part of the RCR 906429
#define EXTV_FLAG_DAC_RGB 0x0100
#define EXTV_FLAG_DAC_YC 0x0200
#define EXTV_FLAG_DAC_COMP 0x0400
#define EXTV_FLAG_DAC_HDTV 0x0800
#define EXTV_FLAG_DAC_HTRGB 0x1000
#define EXTV_FLAG_DAC_CMPT 0x2000
#define EXTV_FLAG_AUTO_CONNECTOR_SELECTION 0x4000

// Extended TV Parameters GUID
//
#define INTEL_EXTENDEDVP_GUID "{1A2FF4DB-FC03-42d4-AC86-8275D6555062}"
DEFINE_GUID(GUID_INTEL_EXTENDEDVP, 0x1A2FF4DB, 0xFC03, 0x42d4, 0xAC, 0x86, 0x82, 0x75, 0xD6, 0x55, 0x50, 0x62);

#pragma pack(1)

// Extended TV Data Format
//
typedef struct _EXTVDATA
{
    DWORD Value;
    DWORD Default;
    DWORD Min;
    DWORD Max;
    DWORD Step; // arbitrary unit (e.g. pixel, percent) returned during VP_COMMAND_GET
} EXTVDATA, *PEXTVDATA;

#define TV_CONNECTED 0x0001
#define TV_NOT_CONNECTED 0x0002
#define TV_CONNECTION_STATUS_UNKNOWN 0x0003
#define CURRENT_CONNECTOR_SELECTION 0x0004

// Extended TV-Control Parameters
//
typedef struct _EXTENDED_TVCTRL
{
    GUID     guid;             // this is {1A2FF4DB-FC03-42d4-AC86-8275D6555062}
    DWORD    dwCommand;        // EXTV_COMMAND_SET or EXTV_COMMAND_GET
    DWORD    dwFlags;          // OR in each flag supported
    EXTVDATA Sharpness;        // Continuous
    EXTVDATA AdaptiveFlicker;  // Continuous
    EXTVDATA TwoDFlicker;      // Continuous
    EXTVDATA Saturation;       // Continuous
    EXTVDATA Hue;              // Continuous
    EXTVDATA DotCrawl;         // Boolean
    EXTVDATA LumaFilter;       // Boolean
    EXTVDATA ChromaFilter;     // Boolean
    EXTVDATA DACModeRGB;       // Boolean (SCART)
    EXTVDATA DACModeYC;        // Boolean (SVIDEO)
    EXTVDATA DACModeComposite; // Boolean (RCA)
    EXTVDATA DACModeHDTV;      // Boolean
    EXTVDATA DACModeHDRGB;     // Boolean
    EXTVDATA DACModeComponent; // Boolean (Y,Cb,Cr)
} EXTENDED_TVCTRL, *PEXTENDED_TVCTRL;

// Bug ID: Tibet 960930
// Description: New Structure needed for CUI/Standard TV Controls
// Fix: Adding structure needed for STDTVOUT (Standard TVout)
// Files changed: itvout.h
//
// the GUID for this structure is:
// {FBA0991C-C43C-43df-B5DF-489F12195A43}
// which can be declared as...
// DEFINE_GUID(<<name>>, 0xfba0991c, 0xc43c, 0x43df, 0xb5, 0xdf, 0x48, 0x9f, 0x12, 0x19, 0x5a, 0x43);
// or
// static const GUID <<name>> = { 0xfba0991c, 0xc43c, 0x43df, { 0xb5, 0xdf, 0x48, 0x9f, 0x12, 0x19, 0x5a, 0x43 } };

#define INTEL_STDTVOUT_GUID "{FBA0991C-C43C-43df-B5DF-489F12195A43}"
DEFINE_GUID(GUID_INTEL_STDTVOUT, 0xfba0991c, 0xc43c, 0x43df, 0xb5, 0xdf, 0x48, 0x9f, 0x12, 0x19, 0x5a, 0x43);

typedef struct _STANDARD_TVCTRL
{
    GUID Guid;          // GUID for this structure
                        // {FBA0991C-C43C-43df-B5DF-489F12195A43}
    DWORD    dwCommand; // EXTV_COMMAND_SET or EXTV_COMMAND_GET
    DWORD    dwFlags;   // OR in each flag supported
    EXTVDATA PositionX;
    EXTVDATA PositionY;
    EXTVDATA SizeX;
    EXTVDATA SizeY;
    EXTVDATA Brightness;
    EXTVDATA Contrast;
    EXTVDATA Flicker;
} STANDARD_TVCTRL, *PSTANDARD_TVCTRL;

// STDTV dwFlags

#define STDTV_FLAGS_POS_Y 0x0001
#define STDTV_FLAGS_POS_X 0x0002
#define STDTV_FLAGS_SIZEY 0x0004
#define STDTV_FLAGS_SIZEX 0x0008
#define STDTV_FLAGS_BRIGHTNESS 0x0010
#define STDTV_FLAGS_CONTRAST 0x0020
#define STDTV_FLAGS_FLICKER 0x0040

// HDTV standard defination added using the unused upper 12 bits of dwTVStandard
#define VP_HDTV_SMPTE_170M_480i59 0x00100000
#define VP_HDTV_SMPTE_293M_480p60 0x00200000
#define VP_HDTV_SMPTE_293M_480p59 0x00400000
#define VP_HDTV_ITURBT601_576i50 0x00800000
#define VP_HDTV_ITURBT601_576p50 0x01000000
#define VP_HDTV_SMPTE_296M_720p50 0x02000000
#define VP_HDTV_SMPTE_296M_720p59 0x04000000
#define VP_HDTV_SMPTE_296M_720p60 0x08000000
#define VP_HDTV_SMPTE_274M_1080i50 0x10000000
#define VP_HDTV_SMPTE_274M_1080i59 0x20000000
#define VP_HDTV_SMPTE_274M_1080i60 0x40000000
#define VP_HDTV_SMPTE_274M_1080p60 0x80000000

// RCR 916573 , 4:3 letter box support in D-connector
#define VP_FLAGS_LETTERBOX 0x8000 // support for D-Connnector 4:3LetterBOX mode
#define LETTERBOX_ON 0x01
#define LETTERBOX_OFF (0x01 << 1)

// RCR TV Aspect Scaling RCR
#define VP_FLAGS_TV_ASPECT_SCALING 0x10000 // support for TV Aspect Scaling RCR
#define TV_ASPECT_SCALING_4_3 0x04
#define TV_ASPECT_SCALING_16_9 0x08

//===== 'SMI 1.3 Update C' defined codes ========
// HDTV Standard Codes
// Mapping of the Driver SMPTE std to CEA std.
#define VP_HDTV_BT1358_31_576p VP_HDTV_ITURBT601_576p50
#define VP_HDTV_BT6564_33_576i VP_HDTV_ITURBT601_576i50
#define VP_HDTV_CEA_7702_480p60 VP_HDTV_SMPTE_293M_480p60
#define VP_HDTV_CEA_7702_480p59 VP_HDTV_SMPTE_293M_480p59
#define VP_HDTV_CEA_7703_720p60 // XXXXXX - Not Supported in Driver 720p 60 CEA_7703//
#define VP_HDTV_CEA_7703_720p59 // XXXXXX - Not Supported in Driver 720p 59 CEA_7703//
#define VP_HDTV_CEA_7703_1080p60 VP_HDTV_SMPTE_274M_1080p60
#define VP_HDTV_CEA_7703_1080p59 // XXXXXX - Not Supported in Driver 1080p 59//
#define VP_HDTV_CEA_7703_1080i60 VP_HDTV_SMPTE_274M_1080i60
#define VP_HDTV_CEA_7703_1080i59 VP_HDTV_SMPTE_274M_1080i59
#define VP_HDTV_CEA_7702_480i60 // XXXXXX - New One for SMI 1.3 'C'//
#define VP_HDTV_CEA_7702_480i59 VP_HDTV_SMPTE_170M_480i59
//===== 'SMI 1.3 Update C' defined codes ========

// New structure to get mode related information for HDTV mode of operation
#define INTEL_HDTVCAPS_GUID "{3CA0E9B0-AED9-4bb1-BFBA-2BDD57AF40FD}"
DEFINE_GUID(GUID_INTEL_HDTVCAPS, 0x3ca0e9b0, 0xaed9, 0x4bb1, 0xbf, 0xba, 0x2b, 0xdd, 0x57, 0xaf, 0x40, 0xfd);

// {3CA0E9B0-AED9-4bb1-BFBA-2BDD57AF40FD}

#define NUM_MAX_MODES 50 // Modes for TV display got from OS

typedef struct _HDTV_MODE_INFO
{

    IN SHORT usXResolution;
    IN SHORT usYResolution;
    IN SHORT usColorBpp;
    IN SHORT usReserved;
    OUT DWORD ulSupportedStds; // Bit OR of all VP_HDTV_SMPTE Stds that support this X,Y
    OUT DWORD ulPreferrredStd; // The VP_HDTV_SMPTE std for which this is the native resolution

} HDTV_MODE_INFO, *PHDTV_MODE_INFO;

#define BPP_8BITS 8
#define BPP_16BITS 16
#define BPP_32BITS 32

typedef struct _HDTV_CAPS
{

    IN GUID GUID;
    IN DWORD Command; // HDTV_COMMAND_* values
    IN DWORD DisplayUID;
    IN DWORD       dwNumOfModes;
    HDTV_MODE_INFO ModeInfo[NUM_MAX_MODES];

} HDTV_CAPS, *PHDTV_CAPS;

#define HDTVCAPS_COMMAND_GET 0x0001

// New structure to get mode related information for HDTV mode of operation
// Get Video parameter will return TV std only when TV is active.
// But OS needs to know the TV std during mode enumeration and hence this structure
#define INTEL_GETTVSTANDARD_GUID "{FC852D0C-8619-4c5e-AC30-AED5B54AF50A}"
DEFINE_GUID(GUID_INTEL_GETTVSTANDARD, 0xfc852d0c, 0x8619, 0x4c5e, 0xac, 0x30, 0xae, 0xd5, 0xb5, 0x4a, 0xf5, 0x0a);

typedef struct _GET_SELECTED_TVSTANDARD
{
    GUID Guid;          // GUID for this structure
                        // {FC852D0C-8619-4c5e-AC30-AED5B54AF50A}
    DWORD dwTVStandard; // NTSC_M / PAL_D / Etc.

    BOOLEAN bHDTV; // This tells whether its an HDTV or SDTV.
} GET_SELECTED_TVSTANDARD, *PGET_SELECTED_TVSTANDARD;

#pragma pack()

#endif //__ITVOUT_H__