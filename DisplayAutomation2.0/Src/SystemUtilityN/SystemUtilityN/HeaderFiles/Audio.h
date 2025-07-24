/**
 * @file
 * @section Audio.h
 * @brief Internal header file which contains data structure and helper function required for
 * getting audio data from EDID
 *
 * @ref AudioDetails.h
 * @author Sridharan.V, Rohit Kumar
 */

/**********************************************************************************
 * INTEL CONFIDENTIAL. Copyright (c) 2016 Intel Corporation All Rights Reserved.
 *  <br>The source code contained or described herein and all documents related to the source code
 *  ("Material") are owned by Intel Corporation or its suppliers or licensors. Title to the
 *  Material remains with Intel Corporation or its suppliers and licensors. The Material contains
 *  trade secrets and proprietary and confidential information of Intel or its suppliers and licensors.
 *  The Material is protected by worldwide copyright and trade secret laws and treaty provisions.
 *  No part of the Material may be used, copied, reproduced, modified, published, uploaded, posted,
 *  transmitted, distributed, or disclosed in any way without Intel’s prior express written permission.
 *  <br>No license under any patent, copyright, trade secret or other intellectual property right is
 *  granted to or conferred upon you by disclosure or delivery of the Materials, either expressly,
 *  by implication, inducement, estoppel or otherwise. Any license under such intellectual property
 *  rights must be express and approved by Intel in writing.
 */

/* Avoid multi inclusion of header file*/
#pragma once

/* System header(s) */
#include <math.h>
#include <string.h>
#include "CommonDetails.h"
#include "SystemUtility.h"
#include "EDIDStructs.h"

#define HDMITYPE 0
#define DPTYPE 1
#define AUDIOINDEX -1
#define INDEX -1
#define EDIDSIZE 255
#define MAXMONITORSTRING 13
#define NEWLINE 10
#define NULLBYTE 0x00
#define SADCOUNT 3
#define ZERO 0

/* Structure for Audio Endpoints information details*/
typedef struct
{
    CHAR *pFormatName; // LPCM, Dolby ...
    UINT  SampleRate;
    UINT  BitDepth; // 16, 20, 24
} AUDIO_FORMAT;

/* Structure for Audio Endpoints information details*/
typedef struct _AUDIO_ENDPOINTS_INFO
{
    _In_ UINT Size;
    _Out_ UINT NumFormats;
    _Out_ UINT MaxNumberOfChannels;
    _Out_ AUDIO_FORMAT AudFormat[15 * 3 * 7]; // 15 SADs. Each may support 3 bit depths and 7 sampling rates
} AUDIO_ENDPOINTS_INFO, *PAUDIO_ENDPOINTS_INFO;

CHAR *gAudioFomatStrings[] = {
    "Invalid", "LPCM",         "Dolby Digital", "MPEG-1",           "MPEG-3", "MPEG-2", "AAC", "DTS Audio", "ATRAC", "One-bit Audio", "Dolby Digital Plus",
    "DTS-HD",  "Dolby TrueHD", "DST Audio",     "Microsoft WMA Pro"
};

BOOLEAN BASEAUDIOPROTOCOL_CreateEELDPacket(PBASEAUDIOPROTOCOL pThis, PUCHAR pEDID, ULONG ulEDIDSize);
ULONG   NumSupportedChannels(SPEAKER_ALLOCATION *pSpkrAllocation);
BOOLEAN BASEAUDIOPROTOCOL_CreateSADBlocks(PBASEAUDIOPROTOCOL pThis, PUCHAR pDataBlock, DWORD dwNumBytesInDataBlock, PCEA_861B_ADB pOutSADs, DWORD *pNumOutSADs);
BOOLEAN BASEAUDIOPROTOCOL_CreateVendorDataBlock(PBASEAUDIOPROTOCOL pThis, PUCHAR pDataBlock, DWORD dwNumBytesInDataBlock);
BOOLEAN BASEAUDIOPROTOCOL_CreateMonitorName(PBASEAUDIOPROTOCOL pThis, PMONITOR_DESCRIPTOR pMonitorDescriptor, PELDV2 pEldV2);
BOOLEAN ParseELD(ELDV2 *pELD, AUDIO_ENDPOINTS_INFO *pAudioEndpointsInformation);
