/**
 * @file
 * @section Audio_c
 * @brief Internal source file which contains implementation required for audio features
 *
 * @ref Audio.c
 * @author Sridharan.V, Rohit Kumar
 */

/***********************************************************************************************
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

#include "../HeaderFiles/Audio.h"

/** \copydoc DisplayAudioFormat */
CDLL_EXPORT BOOL DisplayAudioFormat(PPANEL_INFO pDisplayandAdapterInfo, AUDIO_ENDPOINTS_INFO *pAudioEndpointsInformation, HRESULT *pErrorCode)
{
    //PBYTE pEdidBuffer = NULL;
    BOOL  status      = FALSE;
    // PBYTE pAudio_Data = NULL;
    UINT    numExt = 0;
    BYTE EdidData[EDID_BLOCK_SIZE * MAX_EDID_BLOCK];

    BASEAUDIOPROTOCOL protocol = { 0 };

    do
    {
        if (pAudioEndpointsInformation->Size != sizeof(AUDIO_ENDPOINTS_INFO))
        {
            TRACE_LOG(DEBUG_LOGS, "\n Invalid Parameters. Exiting ...");
            break;
        }
        /* Check for the parameters*/
        if (pDisplayandAdapterInfo->targetID == 0)
        {
            TRACE_LOG(DEBUG_LOGS, "\n Target Id of Display is invalid. Exiting ...");
            break;
        }

        ZeroMemory(&EdidData, EDID_BLOCK_SIZE * MAX_EDID_BLOCK);

        /* Call GetEdidData() to get pointer to EDID memory and then point local pointer pEdidBuffer to same location */
        status = GetEdidData(pDisplayandAdapterInfo, EdidData, &numExt);

        /* Check for the pEdidBuffer, if NULL then return FALSE */
        if (status == FALSE)
        {
            TRACE_LOG(DEBUG_LOGS, "\nGetEdidData escape call failed!\n");
            break;
        }
        if (EdidData == NULL)
        {
            TRACE_LOG(DEBUG_LOGS, "\n NULL pointer detected. Exiting ...\n");
            break;
        }
        if (BASEAUDIOPROTOCOL_CreateEELDPacket(&protocol, EdidData, EDIDSIZE))
        {
            pAudioEndpointsInformation->MaxNumberOfChannels = NumSupportedChannels(&protocol.m_stPrunedELDV2.stSpkrAllocation);
            if (pAudioEndpointsInformation->MaxNumberOfChannels > 0)
            {
                if (ParseELD(&protocol.m_stPrunedELDV2, pAudioEndpointsInformation))
                    status = TRUE;
                else
                    TRACE_LOG(DEBUG_LOGS, "\n Total No of channel is not correct. Exiting ...\n");
            }
            else
            {
                TRACE_LOG(DEBUG_LOGS, "\n Total No of channel is not correct. Exiting ...\n");
            }
        }
        else
            TRACE_LOG(DEBUG_LOGS, "\n EDID Packet is not correct. Exiting ...\n");
    } while (FALSE);

    return status;
}

BOOLEAN BASEAUDIOPROTOCOL_CreateEELDPacket(PBASEAUDIOPROTOCOL pThis, PUCHAR pEDID, ULONG EDIDSize)
{
    CEA_861B_ADB  SADBlocks[15]       = { 0 };
    INT           sizeOfCEADataBlock  = 0;
    INT           numBytesInDataBlock = 0;
    DWORD         numSupportedSADs    = 0;
    UCHAR         dataBlockTag        = 0;
    PUCHAR        pDataBlock          = NULL;
    BOOLEAN       LPCMSADFound        = FALSE;
    PELDV2        pEldV2              = NULL;
    PBASEEDID_1_X pEdid               = NULL;
    PCE_EDID      pCeEdid             = NULL;

    do
    {
        memset(&pThis->m_stBaseELDV2, 0, sizeof(pThis->m_stBaseELDV2));
        memset(&pThis->m_stPrunedELDV2, 0, sizeof(pThis->m_stPrunedELDV2));
        pThis->m_ucProgLatency = 0;
        pThis->m_ucIntLatency  = 0;

        pEldV2 = (PELDV2)&pThis->m_stBaseELDV2;

        // Fill Version info
        pEldV2->ucCEAEDIDVersion = CEA_861B_VERSION;
        pEldV2->ucELDVersion     = CEA_861A_VERSION;

        // Indicate the connetion type in EELD data as DP
        // By default this is zero indicating HDMI
        pEldV2->ucConnectionType = (IS_DP_PORT(pThis->m_ePort)) ? 1 : 0;

        if (pEDID == NULL || EDIDSize < EDID_BLOCK_SIZE)
        {
            break;
        }

        pCeEdid = (PCE_EDID)(pEDID + 128);

        // Now pull out data from CEA Extension EDID
        // If Offset <= 4, we will not have CEA DataBlocks
        if (pCeEdid->ucDTDOffset <= CEA_EDID_HEADER_SZIE)
        {
            break;
        }

        sizeOfCEADataBlock = pCeEdid->ucDTDOffset - CEA_EDID_HEADER_SZIE;

        pDataBlock = (PUCHAR)pCeEdid;

        // skip header (first 4 bytes) in CEA EDID Timing Extension
        // and set pointer to start of DataBlocks collection
        pDataBlock += CEA_EDID_HEADER_SZIE;

        while (sizeOfCEADataBlock > 2)
        {
            // Get the Size of CEA DataBlock in bytes and TAG
            numBytesInDataBlock = 1 + (pDataBlock[0] & CEA_DATABLOCK_LENGTH_MASK); // Including the Zeroth byte
            dataBlockTag        = (*pDataBlock & CEA_DATABLOCK_TAG_MASK) >> 5;

            if (dataBlockTag == CEA_AUDIO_DATABLOCK)
            {
                LPCMSADFound = BASEAUDIOPROTOCOL_CreateSADBlocks(pThis, &pDataBlock[1], numBytesInDataBlock, SADBlocks, &numSupportedSADs);
            }
            else if (dataBlockTag == CEA_VENDOR_DATABLOCK)
            {
                BASEAUDIOPROTOCOL_CreateVendorDataBlock(pThis, &pDataBlock[1], numBytesInDataBlock);
            }
            else if (dataBlockTag == CEA_SPEAKER_DATABLOCK)
            {
                pEldV2->stSpkrAllocation = *((SPEAKER_ALLOCATION *)(&pDataBlock[1]));
            }

            pDataBlock += numBytesInDataBlock;         // Move pointer to next CEA Datablock
            sizeOfCEADataBlock -= numBytesInDataBlock; // Decrement size of CEA DataBlock
        }

        // We have to report an LPCM SAD for 48Khz with 2 channel support if SAD is not found in EDID
        if (LPCMSADFound == FALSE)
        {
            SADBlocks[numSupportedSADs].ucAudioFormatCode = AUDIO_LPCM;
            SADBlocks[numSupportedSADs].uc48kHz           = 1;
            SADBlocks[numSupportedSADs].ucMaxChannels     = 1;
            SADBlocks[numSupportedSADs].uc16Bit           = 1;
            numSupportedSADs += 1;
        }

        // If speaker allocation block is not present in EDID, create a default speaker allocation block
        if (*((PUCHAR)&pEldV2->stSpkrAllocation) == 0)
        {
            pEldV2->stSpkrAllocation.ucFLR = 1;
        }

        if (EDIDSize < EDID_BLOCK_SIZE)
        {
            break;
        }

        pEdid = (PBASEEDID_1_X)pEDID;

        // Update the Manufacturer ID and Product Code here
        SB_MEM_COPY_SAFE(pEldV2->ucManufacturerName, sizeof(pEldV2->ucManufacturerName), pEdid->PNPID.ManufacturerID, sizeof(pEdid->PNPID.ManufacturerID));
        SB_MEM_COPY_SAFE(pEldV2->ucProductCode, sizeof(pEldV2->ucProductCode), pEdid->PNPID.ProductID, sizeof(pEdid->PNPID.ProductID));

        BASEAUDIOPROTOCOL_CreateMonitorName(pThis, &pEdid->MonitorInfo[1], pEldV2);

        // Check if number of SAD Bytes > 0 and for size within limits of allowed Base line Data size as per EELD spec
        if ((numSupportedSADs > 0) && (numSupportedSADs <= MAX_NUM_SADS))
        {
            // Copy the SADs immediately after the Monitor Name String
            SB_MEM_COPY_SAFE(&pEldV2->ucMNSAndSADs[pEldV2->ucMNL], numSupportedSADs * sizeof(CEA_861B_ADB), SADBlocks, numSupportedSADs * sizeof(CEA_861B_ADB));
            pEldV2->ucSADCount = numSupportedSADs;
        }

        pThis->m_stPrunedELDV2 = pThis->m_stBaseELDV2;

    } while (FALSE);

    return TRUE;
}

BOOLEAN BASEAUDIOPROTOCOL_CreateVendorDataBlock(PBASEAUDIOPROTOCOL pThis, PUCHAR pDataBlock, DWORD dwNumBytesInDataBlock)
{
    PVSDB_BYTE6_TO_BYTE8 pVSDB = NULL;

    if (dwNumBytesInDataBlock > 8) // latency flags are in byte 8 of VSDB
    {
        // audio wants data from 6th byte of VSDB onwards
        pVSDB = (PVSDB_BYTE6_TO_BYTE8)(pDataBlock + 5);

        if (pVSDB->ucLatencyFieldPresent == 1 && pVSDB->ucILatencyFieldPresent == 0)
        {
            // Interlaced latency fields not present
            if (dwNumBytesInDataBlock >= 10)
            {
                pThis->m_ucProgLatency = ABSOLUTE_DIFF(*(pDataBlock + 9), *(pDataBlock + 8));
            }
        }
        else if (pVSDB->ucLatencyFieldPresent == 1 && pVSDB->ucILatencyFieldPresent == 1)
        {
            if (dwNumBytesInDataBlock > 12)
            {
                pThis->m_ucProgLatency = ABSOLUTE_DIFF(*(pDataBlock + 9), *(pDataBlock + 8));
                pThis->m_ucIntLatency  = ABSOLUTE_DIFF(*(pDataBlock + 11), *(pDataBlock + 10));
            }
        }
    }

    return TRUE;
}

BOOLEAN BASEAUDIOPROTOCOL_CreateSADBlocks(PBASEAUDIOPROTOCOL pThis, PUCHAR pDataBlock, DWORD dwNumBytesInDataBlock, PCEA_861B_ADB pOutSADs, DWORD *pNumOutSADs)
{
    DWORD         dwNumOutSADs  = 0;
    BOOLEAN       bLPCMSADFound = FALSE;
    BOOLEAN       bSupportedSAD = FALSE;
    DWORD         index, dwNumSADs = 0;
    PCEA_861B_ADB pADB = NULL;

    dwNumSADs = dwNumBytesInDataBlock / SADCOUNT;
    pADB      = (PCEA_861B_ADB)pDataBlock;

    for (index = 0; index < dwNumSADs; index++)
    {
        bSupportedSAD = FALSE;

        if (pADB[index].ucAudioFormatCode == AUDIO_LPCM)
        {
            bSupportedSAD = TRUE;
            bLPCMSADFound = TRUE;
        }

        if (pADB[index].ucAudioFormatCode != AUDIO_MPEG1 && pADB[index].ucAudioFormatCode != AUDIO_MP3 && pADB[index].ucAudioFormatCode != AUDIO_MPEG2 &&
            pADB[index].ucAudioFormatCode != AUDIO_DST)
        {
            bSupportedSAD = TRUE;
        }

        if (bSupportedSAD)
        {
            pOutSADs[dwNumOutSADs] = pADB[index];
            dwNumOutSADs++;
        }
    }

    *pNumOutSADs = dwNumOutSADs;
    return bLPCMSADFound;
}

BOOLEAN BASEAUDIOPROTOCOL_CreateMonitorName(PBASEAUDIOPROTOCOL pThis, PMONITOR_DESCRIPTOR pMonitorDescriptor, PELDV2 pEldV2)
{
    BOOLEAN status = FALSE;
    DWORD   dtdindex, monitorstringindex;
    PUCHAR  pData;

    // Now Fill the monitor string name
    // Search through DTD blocks, looking for monitor name
    for (dtdindex = 0; dtdindex < MAX_BASEEDID_DTD_BLOCKS - 1; dtdindex++, pMonitorDescriptor++)
    {
        // Set a UCHAR pointer to DTD data
        pData = (PUCHAR)pMonitorDescriptor;

        // Check if this block is used as descriptor
        if (pMonitorDescriptor->wFlag == NULLBYTE && pMonitorDescriptor->ucDataTypeTag == 0xFC)
        {
            pData = (PUCHAR)pMonitorDescriptor->ucMonitorName;

            // Copy monitor name
            for (monitorstringindex = 0; monitorstringindex < MAXMONITORSTRING && pData[monitorstringindex] != NEWLINE;
                 monitorstringindex++) // New line char 0x0A indicates end of string
            {
                pEldV2->ucMNSAndSADs[monitorstringindex] = pData[monitorstringindex];
            }

            pEldV2->ucMNL = monitorstringindex;
            status        = TRUE;
            break;
        }
    }

    return status;
}

ULONG NumSupportedChannels(SPEAKER_ALLOCATION *pSpkrAllocation)
{
    ULONG nChannel = 2;

    if (pSpkrAllocation->ucFLR > 0)
    {
        if (pSpkrAllocation->ucRLR > 0) // 4.0 quad
        {
            nChannel += 2;
        }

        if (pSpkrAllocation->ucFC > 0) // 3.0 - 4.0 surround
        {
            nChannel += 1 + (ULONG)(pSpkrAllocation->ucRC);

            if (pSpkrAllocation->ucLFE > 0) // 3.1 - 4.1
            {
                nChannel += 1;

                if (pSpkrAllocation->ucRLR > 0) // 5.1 - 7.1 - 9.1
                {
                    nChannel += (ULONG)((pSpkrAllocation->ucFLRC * 2) + (pSpkrAllocation->ucRLRC * 2));
                }
            }
        }
    }

    return nChannel;
}

UINT GetNumBitDepths(AUDIO_SAD *pSAD, UINT bitDepths[3])
{
    UINT nBitDepthsSupported = 0;

    if (pSAD->uc16bit)
    {
        bitDepths[0] = 16;
        nBitDepthsSupported++;
    }

    if (pSAD->uc20bit)
    {
        bitDepths[1] = 20;
        nBitDepthsSupported++;
    }

    if (pSAD->uc24bit)
    {
        bitDepths[2] = 24;
        nBitDepthsSupported++;
    }

    return nBitDepthsSupported;
}

UINT GetNumSamplingRates(AUDIO_SAD *pSAD, UINT samplingRates[8])
{
    UINT nSamplingRateSupported = 0;

    if (pSAD->uc32KHz)
    {
        samplingRates[0] = 32000;
        nSamplingRateSupported++;
    }
    if (pSAD->uc44KHz)
    {
        samplingRates[1] = 44100;
        nSamplingRateSupported++;
    }
    if (pSAD->uc48KHz)
    {
        samplingRates[2] = 48000;
        nSamplingRateSupported++;
    }
    if (pSAD->uc88KHz)
    {
        samplingRates[3] = 88200;
        nSamplingRateSupported++;
    }
    if (pSAD->uc96KHz)
    {
        samplingRates[4] = 96000;
        nSamplingRateSupported++;
    }
    if (pSAD->uc176KHz)
    {
        samplingRates[5] = 176400;
        nSamplingRateSupported++;
    }
    if (pSAD->uc192KHz)
    {
        samplingRates[6] = 192000;
        nSamplingRateSupported++;
    }

    return nSamplingRateSupported;
}

// This returns number of formats added
UINT GetAudioFomratFromSAD(AUDIO_SAD *pSAD, AUDIO_FORMAT *pFormat)
{
    UINT bitDepthsSupported[3]     = { 0 };
    UINT samplingRatesSupported[8] = { 0 };
    UINT nFormatAdded              = 0;

    UINT numBitDepthsSupported     = GetNumBitDepths(pSAD, bitDepthsSupported);
    UINT numSamplingRatesSupported = GetNumSamplingRates(pSAD, samplingRatesSupported);

    for (UINT bitDepthIndex = 0; bitDepthIndex < numBitDepthsSupported; bitDepthIndex++)
    {
        for (UINT sRateIndex = 0; sRateIndex < numSamplingRatesSupported; sRateIndex++)
        {
            pFormat[nFormatAdded].pFormatName = gAudioFomatStrings[pSAD->audFormat];
            pFormat[nFormatAdded].BitDepth    = bitDepthsSupported[bitDepthIndex];
            pFormat[nFormatAdded].SampleRate  = samplingRatesSupported[sRateIndex];
            nFormatAdded++;
        }
    }

    return nFormatAdded;
}

void ParseSADBlocks(ELDV2 *pELD, AUDIO_ENDPOINTS_INFO *pAudioEndpointsInformation)
{
    UINT numFormats = 0;

    AUDIO_SAD *   pSAD    = (AUDIO_SAD *)&pELD->ucMNSAndSADs[pELD->ucMNL];
    AUDIO_FORMAT *pFormat = &pAudioEndpointsInformation->AudFormat[numFormats];

    for (UINT index = 0; index < pELD->ucSADCount; index++)
    {
        numFormats += GetAudioFomratFromSAD(pSAD, &pFormat[numFormats]);
        pSAD++;
    }

    pAudioEndpointsInformation->NumFormats = numFormats;
}

BOOLEAN ParseELD(ELDV2 *pELD, AUDIO_ENDPOINTS_INFO *pAudioEndpointsInformation)
{
    BOOLEAN status = FALSE;

    if (HDMITYPE == pELD->ucConnectionType || DPTYPE == pELD->ucConnectionType)
    {
        // PUCHAR pSpkrAlloc = (PUCHAR)&pELD->stSpkrAllocation;
        ParseSADBlocks(pELD, pAudioEndpointsInformation);
        status = TRUE;
    }
    else
        TRACE_LOG(DEBUG_LOGS, "\n Unsupported Connection type. Exiting ...\n");

    return status;
}
