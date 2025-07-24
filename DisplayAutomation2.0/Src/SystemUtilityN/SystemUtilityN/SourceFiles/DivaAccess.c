/**
 * @file		DivaAccess.c
 * @brief	API's for Diva Access
 *
 * @author	  Anjali Shetty
 */

/*************************************************************************
**                                                                      **
**                    I N T E L   C O N F I D E N T I A L               **
**       Copyright (c) 2016 Intel Corporation All Rights Reserved.      **
**                                                                      **
**  The source code contained or described herein and all documents     **
**  related to the source code ("Material") are owned by Intel          **
**  Corporation or its suppliers or licensors. Title to the Material    **
**  remains with Intel Corporation or its suppliers and licensors. The  **
**  Material contains trade secrets and proprietary and confidential    **
**  information of Intel or its suppliers and licensors. The Material   **
**  is protected by worldwide copyright and trade secret laws and       **
**  treaty provisions. No part of the Material may be used, copied,     **
**  reproduced, modified, published, uploaded, posted, transmitted,     **
**  distributed, or disclosed in any way without Intel’s prior express  **
**  written permission.                                                 **
**                                                                      **
**  No license under any patent, copyright, trade secret or other       **
**  intellectual property right is granted to or conferred upon you by  **
**  disclosure or delivery of the Materials, either expressly, by       **
**  implication, inducement, estoppel or otherwise. Any license under   **
**  such intellectual property rights must be express and approved by   **
**  Intel in writing.                                                   **
**                                                                      **
*************************************************************************/

#include "../HeaderFiles/DivaAccess.h"
#include "../HeaderFiles/SystemUtility.h"

extern HANDLE hDivaAccess;

BOOLEAN InitDIVA()
{
    BOOLEAN bStatus = TRUE;
    do
    {
        if (hDivaAccess != NULL)
            break;

        hDivaAccess = CreateFile(TEXT(DIVA_DOS_DEVICE_NAME),         // Device Name
                                 GENERIC_READ | GENERIC_WRITE,       // Desired Access
                                 FILE_SHARE_READ | FILE_SHARE_WRITE, // Share Mode
                                 NULL,                               // Default Security Attributes
                                 OPEN_EXISTING,                      // Creation disposition
                                 0,                                  // Flags & Attributes
                                 NULL                                // Template File
        );
        if (hDivaAccess == NULL)
            bStatus = FALSE;

    } while (FALSE);

    return bStatus;
}

BOOL CloseDIVA()
{
    BOOL bStatus = TRUE;
    do
    {
        if (hDivaAccess == NULL)
            break;

        bStatus     = CloseHandle(hDivaAccess);
        hDivaAccess = NULL;

    } while (FALSE);
    return bStatus;
}

BOOL EnableDisableFramework(BOOLEAN bEnable)
{
    BOOL                     bStatus = FALSE;
    GVSTUB_FEATURE_INFO_ARGS ValStubFeatureInfo;

    ValStubFeatureInfo.stDisplayFeatureArgs.stEnableDisableFramework.bEnableFramework = bEnable;

    ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulSize        = sizeof(GVSTUB_META_DATA) + sizeof(GVSTUB_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS);
    ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulVersion     = GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION;
    ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulServiceType = GVSTUB_ENABLE_DISABLE_FRAMEWORK;
    ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulStatus      = GVSTUB_DISPLAY_FEATURE_STATUS_FAILURE;

    ValStubFeatureInfo.stFeatureMetaData.ulSize        = sizeof(GVSTUB_META_DATA) + ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulSize;
    ValStubFeatureInfo.stFeatureMetaData.ulVersion     = GVSTUB_FEATURE_INFO_VERSION;
    ValStubFeatureInfo.stFeatureMetaData.ulServiceType = GVSTUB_FEATURE_DISPLAY;
    ValStubFeatureInfo.stFeatureMetaData.ulStatus      = GVSTUB_FEATURE_FAILURE;

    // Make an IOCTL call
    DWORD BytesReturned = 0;
    bStatus             = DeviceIoControl(hDivaAccess,                                 // Device handle
                              (DWORD)DIVA_IOCTL_GfxValStubCommunication,   // IOCTL code
                              &(ValStubFeatureInfo),                       // Input buffer
                              ValStubFeatureInfo.stFeatureMetaData.ulSize, // Input buffer size
                              &(ValStubFeatureInfo),                       // Output buffer
                              ValStubFeatureInfo.stFeatureMetaData.ulSize, // Output buffer size
                              &BytesReturned,                              // Variable to receive size of data stored in output buffer
                              NULL                                         // Ignored
    );
    printf("Status: %d %d %d\n", bStatus, ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulStatus, ValStubFeatureInfo.stFeatureMetaData.ulStatus);

    if ((GVSTUB_DISPLAY_FEATURE_STATUS_SUCCESS != ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulStatus) ||
        (GVSTUB_FEATURE_SUCCESS != ValStubFeatureInfo.stFeatureMetaData.ulStatus))
    {
        printf("%lu\n", ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulStatus);
        printf("%lu\n", ValStubFeatureInfo.stFeatureMetaData.ulStatus);
        return bStatus = FALSE;
    }

    return bStatus;
}

BOOL EnableDisableFeature(BOOLEAN bEnable, GVSTUB_DISPLAY_FEATURE eFeature)
{
    BOOL                     bStatus = FALSE;
    GVSTUB_FEATURE_INFO_ARGS ValStubFeatureInfo;

    ValStubFeatureInfo.stDisplayFeatureArgs.stEnableDisableFeature.bEnableFeature = bEnable;
    ValStubFeatureInfo.stDisplayFeatureArgs.stEnableDisableFeature.eFeatureEnable = eFeature;

    ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulSize        = sizeof(GVSTUB_META_DATA) + sizeof(GVSTUB_ENABLE_DISABLE_FEATURE_ARGS);
    ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulVersion     = GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION;
    ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulServiceType = GVSTUB_ENABLE_DISABLE_FEATURE;
    ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulStatus      = GVSTUB_DISPLAY_FEATURE_STATUS_FAILURE;

    ValStubFeatureInfo.stFeatureMetaData.ulSize        = sizeof(GVSTUB_META_DATA) + ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulSize;
    ValStubFeatureInfo.stFeatureMetaData.ulVersion     = GVSTUB_FEATURE_INFO_VERSION;
    ValStubFeatureInfo.stFeatureMetaData.ulServiceType = GVSTUB_FEATURE_DISPLAY;
    ValStubFeatureInfo.stFeatureMetaData.ulStatus      = GVSTUB_FEATURE_FAILURE;

    // Make an IOCTL call
    DWORD BytesReturned = 0;
    bStatus             = DeviceIoControl(hDivaAccess,                                 // Device handle
                              (DWORD)DIVA_IOCTL_GfxValStubCommunication,   // IOCTL code
                              &(ValStubFeatureInfo),                       // Input buffer
                              ValStubFeatureInfo.stFeatureMetaData.ulSize, // Input buffer size
                              &(ValStubFeatureInfo),                       // Output buffer
                              ValStubFeatureInfo.stFeatureMetaData.ulSize, // Output buffer size
                              &BytesReturned,                              // Variable to receive size of data stored in output buffer
                              NULL                                         // Ignored
    );
    printf("Status: %d %d %d\n", bStatus, ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulStatus, ValStubFeatureInfo.stFeatureMetaData.ulStatus);

    if ((GVSTUB_DISPLAY_FEATURE_STATUS_SUCCESS != ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulStatus) ||
        (GVSTUB_FEATURE_SUCCESS != ValStubFeatureInfo.stFeatureMetaData.ulStatus))
    {
        printf("%lu\n", ValStubFeatureInfo.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulStatus);
        printf("%lu\n", ValStubFeatureInfo.stFeatureMetaData.ulStatus);
        return bStatus = FALSE;
    }

    return bStatus;
}

CDLL_EXPORT BOOL EnableDisableDFT(BOOL bEnable)
{
    BOOL bStatus = FALSE;
    if (bEnable == TRUE)
    {
        InitDIVA();
        bStatus = EnableDisableFramework(TRUE);
    }
    else
    {
        if (hDivaAccess)
        {
            bStatus = EnableDisableFramework(FALSE);
            CloseDIVA();
        }
    }
    return bStatus;
}

/**
 * @brief			DFT based MMIO Access (Read/Write)
 *
 * @param[in]		pointer to MMIO access args of type DFT_MMIO_ACCESS
 * @return			return True if call passed False otherwiose
 */
CDLL_EXPORT BOOLEAN DftMMIOAccess(PDFT_MMIO_ACCESS pMmioAccessArgs)
{
    BOOLEAN status = FALSE;
    do
    {
        InitDIVA();
        if (NULL == hDivaAccess)
            break;

        // Prepare a buffer to inform the GFX driver to read MMIO info
        GVSTUB_FEATURE_INFO_ARGS ValStubFeatureInfo;

        PGVSTUB_GENERIC_GFX_ACCESS_ARGS pGfxAccessArgs = &(ValStubFeatureInfo.stGenericGfxAccessArgs);
        pGfxAccessArgs->stMmioAccessArgs.ulOffset      = pMmioAccessArgs->offset;
        if (pMmioAccessArgs->accessType == DFT_MMIO_WRITE)
        {
            pGfxAccessArgs->stMmioAccessArgs.ulValue = pMmioAccessArgs->value;
        }

        PGVSTUB_META_DATA pGfxAccessMetaData = &(pGfxAccessArgs->stGenericGfxAccessMetaData);
        pGfxAccessMetaData->ulSize           = sizeof(GVSTUB_META_DATA) + sizeof(GVSTUB_MMIO_ACCESS_ARGS);
        pGfxAccessMetaData->ulVersion        = GVSTUB_GENERIC_GFX_ACCESS_VERSION;
        pGfxAccessMetaData->ulServiceType    = (pMmioAccessArgs->accessType == DFT_MMIO_READ ? GVSTUB_READ_MMIO : GVSTUB_WRITE_MMIO);
        pGfxAccessMetaData->ulStatus         = GVSTUB_GENERIC_ACCESS_FAILURE;

        PGVSTUB_META_DATA pValStubMetaData = &(ValStubFeatureInfo.stFeatureMetaData);
        pValStubMetaData->ulSize           = sizeof(GVSTUB_META_DATA) + pGfxAccessMetaData->ulSize;
        pValStubMetaData->ulVersion        = GVSTUB_FEATURE_INFO_VERSION;
        pValStubMetaData->ulServiceType    = GVSTUB_GENERIC_GFX_ACCESS;
        pValStubMetaData->ulStatus         = GVSTUB_FEATURE_FAILURE;

        // Make an IOCTL call
        DWORD bytesReturned = 0;
        if (DeviceIoControl(hDivaAccess,                               // Device handle
                            (DWORD)DIVA_IOCTL_GfxValStubCommunication, // IOCTL code
                            &(ValStubFeatureInfo),                     // Input buffer
                            pValStubMetaData->ulSize,                  // Input buffer size
                            &(ValStubFeatureInfo),                     // Output buffer
                            pValStubMetaData->ulSize,                  // Output buffer size
                            &bytesReturned,                            // Variable to receive size of data stored in output buffer
                            NULL                                       // Ignored
                            ) == FALSE)
        {
            TRACE_LOG(DEBUG_LOGS, "Ioctl call failed for Gfx MMIO access");
            break;
        }

        if ((GVSTUB_GENERIC_ACCESS_SUCCESS != pGfxAccessMetaData->ulStatus) || (GVSTUB_FEATURE_SUCCESS != pValStubMetaData->ulStatus))
        {
            TRACE_LOG(DEBUG_LOGS, "MMIO Access through DFT call failed from Gfx Driver");
            break;
        }

        if (pMmioAccessArgs->accessType == DFT_MMIO_READ)
            pMmioAccessArgs->value = pGfxAccessArgs->stMmioAccessArgs.ulValue;
        status = TRUE;

    } while (FALSE);
    return status;
}