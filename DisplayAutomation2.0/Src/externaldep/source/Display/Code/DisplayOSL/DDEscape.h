/*===========================================================================
; DDEscape - DDEscape interface functions
;----------------------------------------------------------------------------
;   Copyright (c) Intel Corporation (2000 - 2017)
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
;
;   File Description:
;       This file contains all the DDEscape structe related interface functions
;--------------------------------------------------------------------------*/
#pragma once

#include "..\\..\\Code\\DisplayContext.h"
//#include "..\\..\\..\\..\\inc\\common\\Chipsimc.h"
#include <Chipsimc.h>

#define MAX_BUFFER_SIZE 2048
#define QUANT_RANGE_MASK 0x0000FFFF

typedef struct _DD_I2C_AUX_ARGS DD_I2C_AUX_ARGS;
typedef DD_COLOR_3DLUT_CONFIG   DD_ESC_SET_3D_LUT_ARGS;

typedef struct _DD_ESC_GET_INVALID_DISP_COMBO_ARGS
{
    DDU8  SpecificConfig; // If this is not set, then all valid configs are returned.
    DDU32 NumOfInvalidConfigs;
    DDU32 NumOfDisplaysPerConfig[3];
    // Variable size data array below. To be used after verifying incoming buffer size.
    //  OUT DD_ESC_DISP_CFG   ConfigTable[];
} DD_ESC_GET_INVALID_DISP_COMBO_ARGS;

typedef struct _DD_ESC_DISP_CFG
{
    DDU8  DisplayConfig; // SPSD/Collage/ED-Clone
    DDU32 DisplayUID[MAX_POSSIBLE_PIPES];
} DD_ESC_DISP_CFG;

typedef struct _DD_ESC_GET_VERSION_ARGS
{
    DDU8 MajorVer;
    DDU8 MinorVer;
} DD_ESC_GET_VERSION_ARGS;

typedef struct _PINNED_MODE_INFO
{
    DDU32               TgtID;   // has to be valid
    DD_SOURCE_MODE_INFO SrcMode; // can be 0 if nothing is pinned
    DD_TIMING_INFO      TgtMode; // can be 0 if nothing is pinned
} PINNED_MODE_INFO;

/* Structure to return the source and target timing list to CUI
This is 2 pass call,in teh first call driver returns the number or source and target modes
In second call, driver returns the list of target and source mode for the queried display
If CUI has pinned target timings for other displays then driver returns Sourec and Target cofunctional to the pinned mode
[i.e bandwidth checked]
*/
typedef struct _DD_ESC_QUERY_MODE_TABLE_ARGS
{
    PINNED_MODE_INFO   ModeInfo[MAX_POSSIBLE_PIPES]; // This contains the pinned src and tgt mode info
    DDU8               NumPinnedTgt;                 // will be 0 if nothing is pinned
    DDU8               NumSrcModes;                  // If 0, implies it is first pass call.
    DDU8               NumTgtModes;                  // If 0, implies it is first pass call.
    DD_SCALING_SUPPORT Scaling;
    // To add error code? Close with CUI- BW prune
    // Var size below
    // OUT DD_TIMING_INFO TgtModeTable[];
    // OUT SOURCE_MODE_INFO SrcModeTable[];
} DD_ESC_QUERY_MODE_TABLE_ARGS;

typedef struct _DD_ESC_GET_EDID_ARGS
{
    DDU32 DisplayUID;
    DDU32 EdidBlockNum;
    DDU8  EdidData[EDID_BLOCK_SIZE];
} DD_ESC_GET_EDID_ARGS;

typedef struct _DD_ESC_DETECT_DEVICE_ARGS
{
    DDU32 DetectDeviceFlags; // Bit0:  Do Redetect
                             // Bit1:  Do Legacy Detection
                             // Bit 11:  Do Force Detection : RCR- 2262091
    DD_DISPLAY_LIST DispList;
} DD_ESC_DETECT_DEVICE_ARGS;

typedef struct _DD_ESC_AUX_I2C_ACCESS_ARGS
{
    DD_ESCAPE_STATUS Status;
    DD_I2C_AUX_ARGS  I2CAuxArgs;
} DD_ESC_AUX_I2C_ACCESS_ARGS;

typedef DD_COLOR_MATRIX_CONFIG DD_ESC_SET_CSC_ARGS;
typedef DD_COLOR_1DLUT_CONFIG  DD_ESC_GET_SET_GAMMA_ARGS;
typedef DD_COLOR_3DLUT_CONFIG  DD_ESC_SET_3D_LUT_ARGS;

typedef struct _DD_ESC_GET_SET_COLOR_MODEL_ARGS
{
    DDU32              TargetID;
    DD_COLOR_OPERATION Operation;
    DD_COLOR_MODEL     ColorModel;
} DD_ESC_GET_SET_COLOR_MODEL_ARGS;

typedef struct _DD_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME_ARGS
{
    DDU32                TargetID;
    DD_COLOR_OPERATION   Operation;
    AVI_INFOFRAME_CUSTOM AVIInfoFrame;
} DD_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME_ARGS;

typedef enum _DD_VRR_OPERATION
{
    DD_VRR_OPERATION_GET_INFO, // Get details of VRR support and current status
    DD_VRR_OPERATION_ENABLE,   // Enable VRR
    DD_VRR_OPERATION_DISABLE,  // Disable VRR
} DD_VRR_OPERATION;

typedef struct _DD_ESC_VRR_INFO
{
    DDU32 TargetId;
    DDU32 MinRr;
    DDU32 MaxRr;
} DD_ESC_VRR_INFO;

typedef struct _DD_ESC_GET_SET_VRR_ARGS
{
    DD_VRR_OPERATION Operation; // Specifies operation to perform
    // Below parameters applicable to "DD_VRR_OPERATION_GET_INFO" ONLY
    BOOLEAN         VrrSupported;                   // Whether the feature is Supported for the platform or not (Static choice by OEM)
    BOOLEAN         VrrEnabled;                     // Whether the feature is currently enabled or not (Dynamic choice by end user)
    DDU32           NumDisplays;                    // Number of connected displays that support VRR
    DD_ESC_VRR_INFO EscVrrInfo[MAX_POSSIBLE_PIPES]; // VRR info for each display that supports VRR
} DD_ESC_GET_SET_VRR_ARGS;

typedef struct _DD_DISPLAY_FEATURE_SUPPORT
{
    BOOLEAN YCbCrSupport : 1;
    BOOLEAN RelativeCSCSupport : 1;
} DD_DISPLAY_FEATURE_SUPPORT;

typedef struct _DD_ESC_QUERY_DISPLAY_DETAILS_ARGS
{
    IN DDU32                   TargetId;
    DD_DISPLAY_FEATURE_SUPPORT DispFtrSupport;
    DD_CONNECTOR_INFO          ConnectorInfo;
    DDU32                      NumPipesForTarget;
} DD_ESC_QUERY_DISPLAY_DETAILS_ARGS;
