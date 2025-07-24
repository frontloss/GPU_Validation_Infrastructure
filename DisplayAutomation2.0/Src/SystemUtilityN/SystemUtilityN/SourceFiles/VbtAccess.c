/**
 * @file
 * @section VbtAccess_c
 * @brief Internal source file which contains implementation required for VBT Get and Set through DFT calls.
 * Functions APIs are provided to Get and Set full VBT or VBT block data by block Id, and to reset the VBT.
 * After doing Set VBT, display driver should be disabled & enabled in order to load this VBT.
 *
 * @ref VbtAccess.c
 * @author Sri Sumanth Geesala
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

#include "../HeaderFiles/VbtAccess.h"
#include "math.h"

extern HANDLE hDivaAccess;

CDLL_EXPORT BOOL GetSetVbtBlock(UINT blockId, PBYTE pBlockData, BOOLEAN bSet)
{
    BOOL                     bStatus           = FALSE;
    PBYTE                    pData             = NULL;
    PVBT_BIOS_DATA_HEADER    pBDBHeader        = NULL;
    PVBT_DATA_BLOCK          pVBTDataBlock     = NULL;
    ULONG                    ulDataBlockOffset = 0;
    ULONG                    ulBlockSize       = 0;
    bool                     bIdFound          = FALSE;
    GVSTUB_FEATURE_INFO_ARGS ValStubFeatureInfo;
    PGVSTUB_GET_SET_VBT_ARGS GVStubArgs = &(ValStubFeatureInfo.stDisplayFeatureArgs.stGetSetVBT);
    memset(GVStubArgs, 0, sizeof(GVSTUB_GET_SET_VBT_ARGS));
    GVStubArgs->bEnable = 1;
    GVStubArgs->bSet    = 0; // get vbt

    if (pBlockData == NULL)
        return FALSE;

    // read VBT with DFT call
    bStatus = GetSetVbtDFT(&(ValStubFeatureInfo));
    if (bStatus == FALSE)
        return bStatus;

    // Find the address to first byte of block blockId
    pData      = (PBYTE)GVStubArgs->ulVBTData;
    pBDBHeader = (PVBT_BIOS_DATA_HEADER)(pData + (*(pData + VBT_HEADER_SIZE_OFFSET))); // skip the VBT header

    for (ulDataBlockOffset = sizeof(VBT_BIOS_DATA_HEADER); ulDataBlockOffset < pBDBHeader->BDB_Size; ulDataBlockOffset += (pVBTDataBlock->wSize + sizeof(VBT_DATA_BLOCK)))
    {
        pVBTDataBlock = (PVBT_DATA_BLOCK)((PBYTE)pBDBHeader + ulDataBlockOffset);
        if (pVBTDataBlock->ucId == blockId)
        {
            bIdFound    = TRUE;
            ulBlockSize = pVBTDataBlock->wSize + sizeof(VBT_DATA_BLOCK);
            break;
        }
    }
    if (bIdFound == FALSE)
        return FALSE;

    if (bSet == 0)
    {
        // memcpy ulBlockSize bytes from pVBTDataBlock to pBlockData. (pBlockData: caller will send pointer to empty array)
        memcpy(pBlockData, pVBTDataBlock, ulBlockSize);
    }
    else
    {
        // memcpy ulBlockSize bytes from pBlockData to pVBTDataBlock. (pBlockData: caller will send pointer to array filled with block data)
        memcpy(pVBTDataBlock, pBlockData, ulBlockSize);
        // write VBT with DFT call
        GVStubArgs->bEnable = 1;
        GVStubArgs->bSet    = bSet;
        bStatus             = GetSetVbtDFT(&(ValStubFeatureInfo));
        if (bStatus == FALSE)
            return bStatus;
    }

    return bStatus;
}

CDLL_EXPORT BOOL GetSetVbt(PBYTE pVbtData, PULONG pulVbtSize, BOOLEAN bSet)
{
    BOOL                     bStatus = FALSE;
    GVSTUB_FEATURE_INFO_ARGS ValStubFeatureInfo;
    PGVSTUB_GET_SET_VBT_ARGS GVStubArgs = &(ValStubFeatureInfo.stDisplayFeatureArgs.stGetSetVBT);
    memset(GVStubArgs, 0, sizeof(GVSTUB_GET_SET_VBT_ARGS));
    GVStubArgs->bEnable = 1;
    GVStubArgs->bSet    = bSet;

    if (pulVbtSize == NULL || pVbtData == NULL)
        return FALSE;

    // for set VBT, set vbtSize and VbtData in args
    if (bSet == 1)
    {
        // check vbt size
        if (*pulVbtSize > GVSTUB_VBT_MAX_SIZE)
            return FALSE;
        GVStubArgs->ulVBTSize = *pulVbtSize;
        memcpy(GVStubArgs->ulVBTData, pVbtData, *pulVbtSize);
    }

    bStatus = GetSetVbtDFT(&(ValStubFeatureInfo));
    if (bStatus == FALSE)
        return bStatus;

    // for get VBT, get vbtSize and VbtData from args
    if (bSet == 0)
    {
        *pulVbtSize = GVStubArgs->ulVBTSize;
        memcpy(pVbtData, GVStubArgs->ulVBTData, *pulVbtSize);
    }

    return bStatus;
}

CDLL_EXPORT BOOL ResetVbt()
{
    BOOL                     bStatus = FALSE;
    GVSTUB_FEATURE_INFO_ARGS ValStubFeatureInfo;
    PGVSTUB_GET_SET_VBT_ARGS GVStubArgs = &(ValStubFeatureInfo.stDisplayFeatureArgs.stGetSetVBT);
    memset(GVStubArgs, 0, sizeof(GVSTUB_GET_SET_VBT_ARGS));
    GVStubArgs->bEnable   = 0;
    GVStubArgs->bSet      = 1;
    GVStubArgs->ulVBTSize = 0;

    bStatus = GetSetVbtDFT(&(ValStubFeatureInfo));
    return bStatus;
}

BOOL GetSetVbtDFT(PGVSTUB_FEATURE_INFO_ARGS pValStubFeatureInfo)
{
    BOOL bStatus = FALSE;

    // Recalculate and update VBT checksum, since we modified VBT data
    ULONG                    sumVbtData  = 0;
    ULONG                    newChecksum = 0;
    PGVSTUB_GET_SET_VBT_ARGS GVStubArgs  = &(pValStubFeatureInfo->stDisplayFeatureArgs.stGetSetVBT);
    if (GVStubArgs->bSet == 1)
    {
        TRACE_LOG(DEBUG_LOGS, "recalculating checksum \n");

        for (ULONG index = 0; index < GVStubArgs->ulVBTSize; index++)
            if (index != VBT_CHECKSUM_OFFSET) // byte 26 is VBT checksum. Shouldn't add this to sum
                sumVbtData += (int)GVStubArgs->ulVBTData[index];
        newChecksum                                = ((int)(ceil(sumVbtData / 256.0)) * 256) - sumVbtData;
        GVStubArgs->ulVBTData[VBT_CHECKSUM_OFFSET] = (BYTE)newChecksum;
        TRACE_LOG(DEBUG_LOGS, "Updated checksum at offset= %d, newChecksum= %ld\n", VBT_CHECKSUM_OFFSET, newChecksum);
    }

    PGVSTUB_META_DATA pDisplayFeatureMetaData = &(pValStubFeatureInfo->stDisplayFeatureArgs.stDisplayFeatureMetaData);
    pDisplayFeatureMetaData->ulSize           = sizeof(GVSTUB_META_DATA) + sizeof(GVSTUB_GET_SET_VBT_ARGS);
    pDisplayFeatureMetaData->ulVersion        = GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION;
    pDisplayFeatureMetaData->ulServiceType    = GVSTUB_GET_SET_VBT_DATA;
    pDisplayFeatureMetaData->ulStatus         = GVSTUB_DISPLAY_FEATURE_STATUS_FAILURE;

    PGVSTUB_META_DATA pValStubMetaData = &(pValStubFeatureInfo->stFeatureMetaData);
    pValStubMetaData->ulSize           = sizeof(GVSTUB_META_DATA) + pDisplayFeatureMetaData->ulSize;
    pValStubMetaData->ulVersion        = GVSTUB_FEATURE_INFO_VERSION;
    pValStubMetaData->ulServiceType    = GVSTUB_FEATURE_DISPLAY;
    pValStubMetaData->ulStatus         = GVSTUB_FEATURE_FAILURE;

    // Make an IOCTL call to do the DFT call.
    DWORD BytesReturned = 0;
    bStatus             = DeviceIoControl(hDivaAccess,                                   // Device handle
                              (DWORD)DIVA_IOCTL_GfxValStubCommunication,     // IOCTL code
                              pValStubFeatureInfo,                           // Input buffer
                              pValStubFeatureInfo->stFeatureMetaData.ulSize, // Input buffer size
                              pValStubFeatureInfo,                           // Output buffer
                              pValStubFeatureInfo->stFeatureMetaData.ulSize, // Output buffer size
                              &BytesReturned,                                // Variable to receive size of data stored in output buffer
                              NULL                                           // Ignored
    );

    return bStatus;
}
