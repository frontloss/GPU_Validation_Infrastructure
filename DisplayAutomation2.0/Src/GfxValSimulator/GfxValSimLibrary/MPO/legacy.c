/**
 * @file		MPO.c
 * @brief	API's for MPO
 *
 * Details of the file is as follows.
 * MPO Utility APIs for TH2
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
**  distributed, or disclosed in any way without Intel�s prior express  **
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

#include "stdio.h"
#include "legacy.h"
#include "..\CommonDetails.h"

extern ULONG create_resource;
extern ULONG free_resource;

BOOL mainline_EnableDisableMPO(PGFX_ADAPTER_INFO pAdapterInfo, BOOL bEnable, SIMDRIVER_DISPLAY_FEATURE eFeature);

BOOL mainline_EnableDisableMPODFT(PGFX_ADAPTER_INFO pAdapterInfo, HANDLE hGfxValSim, BOOL bEnable, SIMDRIVER_DISPLAY_FEATURE eFeature)
{
    BOOL status = TRUE;
    if (bEnable == TRUE)
    {
        if (mainline_EnableDisableMPO(pAdapterInfo, TRUE, eFeature))
        {
            pPreviouspPlanes = calloc(1, sizeof(_PLANES_));
            NULL_PTR_CHECK(pPreviouspPlanes);
        }
    }
    else
    {
        if (pPreviouspPlanes != NULL)
        {
            for (UINT PlaneIndex = 0; PlaneIndex < pPreviouspPlanes->uiPlaneCount; PlaneIndex++)
            {
                INT iResourceInUse = pPreviouspPlanes->stPlaneInfo[PlaneIndex].iResourceInUse;
                if (pPreviouspPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse].pGmmBlock)
                    mainline_DFTFreeResource(pAdapterInfo, &pPreviouspPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse]);
            }
            FREE_MEMORY(pPreviouspPlanes);
        }

        if (FALSE == mainline_EnableDisableMPO(pAdapterInfo, FALSE, eFeature))
            status = FALSE;
        INFO_LOG("Create Resource Count = %lu Free Resource Count = %lu", create_resource, free_resource);
    }
    return status;
}

BOOL mainline_EnableDisableMPO(PGFX_ADAPTER_INFO pAdapterInfo, BOOL bEnable, SIMDRIVER_DISPLAY_FEATURE eFeature)
{
    BOOL                                  bStatus         = FALSE;
    DWORD                                 dwBytesReturned = 0;
    SIMDRIVER_DISPLAY_FEATURE_ARGS        stDisplayFeatureArgs;
    SIMDRIVER_ENABLE_DISABLE_FEATURE_ARGS stEnableDisableFeature = { 0 };
    GFX_ADAPTER_INFO                      adapterInfo            = { 0 };

    stEnableDisableFeature.bEnableFeature = bEnable;
    stEnableDisableFeature.eFeatureEnable = eFeature;

    stDisplayFeatureArgs.ulSize       = sizeof(SIMDRIVER_ENABLE_DISABLE_FEATURE_ARGS);
    stDisplayFeatureArgs.eServiceType = SIMDRIVER_ENABLE_DISABLE_MPO;
    stDisplayFeatureArgs.pMpoArgs     = calloc(1, sizeof(SIMDRIVER_ENABLE_DISABLE_FEATURE_ARGS));
    NULL_PTR_CHECK(stDisplayFeatureArgs.pMpoArgs);
    memcpy_s(stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_ENABLE_DISABLE_FEATURE_ARGS), &stEnableDisableFeature, sizeof(SIMDRIVER_ENABLE_DISABLE_FEATURE_ARGS));

    bStatus =
    ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &stDisplayFeatureArgs, sizeof(SIMDRIVER_DISPLAY_FEATURE_ARGS));

    if (bStatus == FALSE)
        ERROR_LOG("IOCTL failed in enable disable MPO: %d", bStatus);

    FREE_MEMORY(stDisplayFeatureArgs.pMpoArgs);
    return bStatus;
}

UINT mainline_CheckForMultiPlaneOverlaySupport(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes)
{
    BOOL                           bStatus         = FALSE;
    DWORD                          dwBytesReturned = 0;
    SIMDRIVER_DISPLAY_FEATURE_ARGS stDisplayFeatureArgs;
    SIMDRIVER_CHECK_MPO_ARGS       SIMDRIVERArgs = { 0 };
    GFX_ADAPTER_INFO               adapterInfo   = { 0 };

    if (pPlanes == NULL || pPlanes->uiPlaneCount <= 0)
        return FALSE;

    SIMDRIVERArgs.ulNumPaths = 1; // TODO Get No Of Active Paths
    SIMDRIVERArgs.ulConfig   = 1;

    for (UINT PlaneIndex = 0; PlaneIndex < pPlanes->uiPlaneCount; PlaneIndex++)
    {
        INT  PathIndex  = pPlanes->stPlaneInfo[PlaneIndex].iPathIndex;
        UINT LayerIndex = pPlanes->stPlaneInfo[PlaneIndex].uiLayerIndex;

        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].uiPlaneCount += 1;

        // Default Parameters
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPOFlags.uiValue = 0;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.uiMPOYCbCrFlags    = pPlanes->stPlaneInfo[PlaneIndex].uiYCbCrFlags;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.eMPOVideoFormat    = SIMDRIVER_MPO_VIDEO_FRAME_FORMAT_PROGRESSIVE;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.eMPOStereoFormat   = SIMDRIVER_MPO_FORMAT_MONO;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.bMPOBaseViewFrame0 = 0;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.bMPOLeftViewFrame0 = 0;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.eMPOStereoFlipMode = SIMDRIVER_MPO_FLIP_NONE;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.eStretchQuality    = SIMDRIVER_MPO_STRETCH_QUALITY_BILINEAR;

        // Parameters from the wrapper
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].uiLayerIndex                     = pPlanes->stPlaneInfo[PlaneIndex].uiLayerIndex;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].bEnabled                         = (BOOLEAN)pPlanes->stPlaneInfo[PlaneIndex].bEnabled;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].eULTPixelFormat                  = pPlanes->stPlaneInfo[PlaneIndex].ePixelFormat;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stSurfaceMemInfo.eSurfaceMemType = pPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType;

        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPOSrcRect.left   = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.left;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPOSrcRect.top    = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.top;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPOSrcRect.right  = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.right;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPOSrcRect.bottom = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.bottom;

        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPODstRect.left   = pPlanes->stPlaneInfo[PlaneIndex].stMPODstRect.left;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPODstRect.top    = pPlanes->stPlaneInfo[PlaneIndex].stMPODstRect.top;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPODstRect.right  = pPlanes->stPlaneInfo[PlaneIndex].stMPODstRect.right;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPODstRect.bottom = pPlanes->stPlaneInfo[PlaneIndex].stMPODstRect.bottom;

        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPOClipRect.left   = pPlanes->stPlaneInfo[PlaneIndex].stMPOClipRect.left;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPOClipRect.top    = pPlanes->stPlaneInfo[PlaneIndex].stMPOClipRect.top;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPOClipRect.right  = pPlanes->stPlaneInfo[PlaneIndex].stMPOClipRect.right;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPOClipRect.bottom = pPlanes->stPlaneInfo[PlaneIndex].stMPOClipRect.bottom;

        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.eHWOrientation     = pPlanes->stPlaneInfo[PlaneIndex].eHWOrientation;
        SIMDRIVERArgs.stCheckMPOPathInfo[PathIndex].stMPOPlaneInfo[LayerIndex].stPlaneAttributes.stMPOBlend.uiValue = pPlanes->stPlaneInfo[PlaneIndex].stMPOBlendVal.uiValue;
    }

    stDisplayFeatureArgs.ulSize       = sizeof(SIMDRIVER_CHECK_MPO_ARGS);
    stDisplayFeatureArgs.eServiceType = SIMDRIVER_CHECK_MPO;
    stDisplayFeatureArgs.pMpoArgs     = calloc(1, sizeof(SIMDRIVER_CHECK_MPO_ARGS));
    NULL_PTR_CHECK(stDisplayFeatureArgs.pMpoArgs);
    memcpy_s(stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_CHECK_MPO_ARGS), &SIMDRIVERArgs, sizeof(SIMDRIVER_CHECK_MPO_ARGS));

    bStatus =
    ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &stDisplayFeatureArgs, sizeof(SIMDRIVER_DISPLAY_FEATURE_ARGS));

    memcpy_s(&SIMDRIVERArgs, sizeof(SIMDRIVER_CHECK_MPO_ARGS), stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_CHECK_MPO_ARGS));
    FREE_MEMORY(stDisplayFeatureArgs.pMpoArgs);

    if (bStatus == FALSE)
    {
        ERROR_LOG("IOCTL failed in check MPO: %d", bStatus);
        return PLANES_FAILURE;
    }

    if (SIMDRIVERArgs.bSupported)
        return PLANES_SUCCESS;
    else
        return PLANES_FAILURE;
}

UINT mainline_SetSourceAddressForMultiPlaneOverlay(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes)
{
    BOOL                           bStatus         = FALSE;
    BOOL                           bResourceStatus = FALSE;
    DWORD                          dwBytesReturned = 0;
    SIMDRIVER_DISPLAY_FEATURE_ARGS stDisplayFeatureArgs;
    SIMDRIVER_SET_SRC_ADD_MPO_ARGS SIMDRIVERArgs = { 0 };
    GFX_ADAPTER_INFO               adapterInfo   = { 0 };

    if (pPlanes == NULL || pPlanes->uiPlaneCount <= 0)
        return PLANES_FAILURE;

    // Sorts the previous planes according to the index of the current planes
    if (pPreviouspPlanes->uiPlaneCount != 0)
    {
        for (UINT PlaneIndex = 0; PlaneIndex < pPlanes->uiPlaneCount; PlaneIndex++)
        {
            INT iResourceInUse = pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse;
            for (UINT PreviousIndex = 0; PreviousIndex < pPreviouspPlanes->uiPlaneCount; PreviousIndex++)
            {
                BOOLEAN iResourceInUseComplement = (iResourceInUse == 0) ? TRUE : FALSE;
                if ((pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse].pGmmBlock != 0 &&
                     pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse].pGmmBlock ==
                     pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iResourceInUse].pGmmBlock) ||
                    (pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUseComplement].pGmmBlock != 0 &&
                     pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUseComplement].pGmmBlock ==
                     pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iResourceInUseComplement].pGmmBlock))
                {
                    if (PlaneIndex != PreviousIndex)
                    {
                        PPLANE_INFO pPlaneInfo = malloc(sizeof(PLANE_INFO));
                        if (NULL == pPlaneInfo)
                        {
                            ERROR_LOG("NULL pointer");
                            continue;
                        }
                        memcpy(pPlaneInfo, &pPreviouspPlanes->stPlaneInfo[PlaneIndex], sizeof(PLANE_INFO));
                        memcpy(&pPreviouspPlanes->stPlaneInfo[PlaneIndex], &pPreviouspPlanes->stPlaneInfo[PreviousIndex], sizeof(PLANE_INFO));
                        memcpy(&pPreviouspPlanes->stPlaneInfo[PreviousIndex], pPlaneInfo, sizeof(PLANE_INFO));
                        FREE_MEMORY(pPlaneInfo);
                    }
                }
            }
        }
        pPreviouspPlanes->uiPlaneCount = (pPlanes->uiPlaneCount > pPreviouspPlanes->uiPlaneCount) ? pPlanes->uiPlaneCount : pPreviouspPlanes->uiPlaneCount;
    }

    // Create the resource
    for (UINT PlaneIndex = 0; PlaneIndex < pPlanes->uiPlaneCount; PlaneIndex++)
    {
        INT  iResourceInUse                      = pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse;
        UINT uiLayerIndex                        = pPlanes->stPlaneInfo[PlaneIndex].uiLayerIndex;
        pPlanes->stPlaneInfo[PlaneIndex].lWidth  = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.right - pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.left;
        pPlanes->stPlaneInfo[PlaneIndex].lHeight = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.bottom - pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.top;

        if (pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse].pGmmBlock == 0)
        {
            bResourceStatus = mainline_DFTCreateResource(pAdapterInfo, &pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse], pPlanes->stPlaneInfo[PlaneIndex].lWidth,
                                                         pPlanes->stPlaneInfo[PlaneIndex].lHeight, pPlanes->stPlaneInfo[PlaneIndex].ePixelFormat,
                                                         pPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType, uiLayerIndex, pPlanes->stPlaneInfo[PlaneIndex].cpDumpFilePath);
            if (bResourceStatus == FALSE)
                goto FreeResource;
        }
        else if (pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse].pGmmBlock != 0)
        {
            // Create the resource if previous plane and current plane is not same
            if (pPlanes->stPlaneInfo[PlaneIndex].lWidth != pPreviouspPlanes->stPlaneInfo[PlaneIndex].lWidth ||
                pPlanes->stPlaneInfo[PlaneIndex].lHeight != pPreviouspPlanes->stPlaneInfo[PlaneIndex].lHeight ||
                pPlanes->stPlaneInfo[PlaneIndex].ePixelFormat != pPreviouspPlanes->stPlaneInfo[PlaneIndex].ePixelFormat ||
                pPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType != pPreviouspPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType)
            {
                BOOLEAN iResourceInUseComplement = (iResourceInUse == 0) ? TRUE : FALSE;
                bResourceStatus =
                mainline_DFTCreateResource(pAdapterInfo, &pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUseComplement], pPlanes->stPlaneInfo[PlaneIndex].lWidth,
                                           pPlanes->stPlaneInfo[PlaneIndex].lHeight, pPlanes->stPlaneInfo[PlaneIndex].ePixelFormat,
                                           pPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType, uiLayerIndex, pPlanes->stPlaneInfo[PlaneIndex].cpDumpFilePath);
                pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse = iResourceInUseComplement;

                if (bResourceStatus == FALSE)
                    goto FreeResource;
            }
            else
            {
                // Resource already available
                bResourceStatus = TRUE;
            }
        }
    }

    // Perform a flip
    for (INT PathIndex = 0; PathIndex < SIMDRIVER_MAX_PIPES; PathIndex++)
    {
        for (UINT PlaneIndex = 0; PlaneIndex < pPlanes->uiPlaneCount; PlaneIndex++)
        {
            SIMDRIVERArgs.dwSourceID = pPlanes->stPlaneInfo[PlaneIndex].iPathIndex;
            UINT LayerIndex          = pPlanes->stPlaneInfo[PlaneIndex].uiLayerIndex;

            if (pPlanes->stPlaneInfo[PlaneIndex].iPathIndex == PathIndex)
            {
                SIMDRIVERArgs.ulNumPlanes += 1;

                // Parameters from wrapper
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].hAllocation =
                (VOID *)pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse].pGmmBlock;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].uiLayerIndex = pPlanes->stPlaneInfo[PlaneIndex].uiLayerIndex;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].bEnabled     = (BOOLEAN)pPlanes->stPlaneInfo[PlaneIndex].bEnabled;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].bAffected    = TRUE;

                // Default Parameters
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPOFlags.uiValue = 0;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.uiMPOYCbCrFlags    = pPlanes->stPlaneInfo[PlaneIndex].uiYCbCrFlags;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.eMPOVideoFormat    = SIMDRIVER_MPO_VIDEO_FRAME_FORMAT_PROGRESSIVE;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.eMPOStereoFormat   = SIMDRIVER_MPO_FORMAT_MONO;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.bMPOBaseViewFrame0 = 0;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.bMPOLeftViewFrame0 = 0;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.eMPOStereoFlipMode = SIMDRIVER_MPO_FLIP_NONE;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.eStretchQuality    = SIMDRIVER_MPO_STRETCH_QUALITY_BILINEAR;

                // Parameters from wrapper
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPOSrcRect.left   = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.left;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPOSrcRect.top    = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.top;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPOSrcRect.right  = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.right;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPOSrcRect.bottom = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.bottom;

                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPODstRect.left   = pPlanes->stPlaneInfo[PlaneIndex].stMPODstRect.left;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPODstRect.top    = pPlanes->stPlaneInfo[PlaneIndex].stMPODstRect.top;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPODstRect.right  = pPlanes->stPlaneInfo[PlaneIndex].stMPODstRect.right;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPODstRect.bottom = pPlanes->stPlaneInfo[PlaneIndex].stMPODstRect.bottom;

                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPOClipRect.left   = pPlanes->stPlaneInfo[PlaneIndex].stMPOClipRect.left;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPOClipRect.top    = pPlanes->stPlaneInfo[PlaneIndex].stMPOClipRect.top;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPOClipRect.right  = pPlanes->stPlaneInfo[PlaneIndex].stMPOClipRect.right;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPOClipRect.bottom = pPlanes->stPlaneInfo[PlaneIndex].stMPOClipRect.bottom;

                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.eHWOrientation     = pPlanes->stPlaneInfo[PlaneIndex].eHWOrientation;
                SIMDRIVERArgs.stDxgkMPOPlaneArgs[LayerIndex].stPlaneAttributes.stMPOBlend.uiValue = pPlanes->stPlaneInfo[PlaneIndex].stMPOBlendVal.uiValue;
            }
        }

        if (SIMDRIVERArgs.ulNumPlanes > 0 && bResourceStatus)
        {
            stDisplayFeatureArgs.ulSize       = sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS);
            stDisplayFeatureArgs.eServiceType = SIMDRIVER_SET_SRC_ADD_MPO;
            stDisplayFeatureArgs.pMpoArgs     = calloc(1, sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS));
            NULL_PTR_CHECK(stDisplayFeatureArgs.pMpoArgs);
            memcpy_s(stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS), &SIMDRIVERArgs, sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS));

            bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &stDisplayFeatureArgs,
                                             sizeof(SIMDRIVER_DISPLAY_FEATURE_ARGS));

            memcpy_s(&SIMDRIVERArgs, sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS), stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS));
            FREE_MEMORY(stDisplayFeatureArgs.pMpoArgs);

            if (bStatus == FALSE)
            {
                ERROR_LOG("IOCTL failed in set source address: %d", bStatus);
                return PLANES_FAILURE;
            }
        }
    }

FreeResource:
    // Free the resource
    for (UINT PreviousIndex = 0; PreviousIndex < pPreviouspPlanes->uiPlaneCount; PreviousIndex++)
    {
        // Free the resource if the resource used by the current plane and previous plane is different
        if (pPlanes->stPlaneInfo[PreviousIndex].iResourceInUse != pPreviouspPlanes->stPlaneInfo[PreviousIndex].iResourceInUse)
        {
            INT iResourceInUse = pPreviouspPlanes->stPlaneInfo[PreviousIndex].iResourceInUse;
            if (pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iResourceInUse].pGmmBlock != 0)
            {
                mainline_DFTFreeResource(pAdapterInfo, &pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iResourceInUse]);
                pPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iResourceInUse].pGmmBlock = 0;
            }
        }
        // Free the resource if the resource used by the current plane and previous plane is same but the previous plane was removed
        else
        {
            INT iCurrResourceInUse = pPlanes->stPlaneInfo[PreviousIndex].iResourceInUse;
            INT iPrevResourceInUse = pPreviouspPlanes->stPlaneInfo[PreviousIndex].iResourceInUse;
            if (pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iPrevResourceInUse].pGmmBlock != 0 &&
                pPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iCurrResourceInUse].pGmmBlock !=
                pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iPrevResourceInUse].pGmmBlock)
                mainline_DFTFreeResource(pAdapterInfo, &pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iPrevResourceInUse]);
        }
    }

    memcpy(pPreviouspPlanes, pPlanes, sizeof(_PLANES_));

    if (bResourceStatus == FALSE)
        return PLANES_RESOURCE_CREATION_FAILURE;

    return PLANES_SUCCESS;
}

UINT mainline_CheckForMultiPlaneOverlaySupport3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes)
{
    BOOL                           bStatus         = FALSE;
    DWORD                          dwBytesReturned = 0;
    SIMDRIVER_DISPLAY_FEATURE_ARGS stDisplayFeatureArgs;
    SIMDRIVER_CHECK_MPO_ARGS       stSbArgs    = { 0 };
    GFX_ADAPTER_INFO               adapterInfo = { 0 };
    UINT                           ulPathIndex = 0, ulPlaneindex = 0, ulPlaneIndexPerPipe = 0;
    UINT                           iLayerIndex = 0;

    stSbArgs.ulConfig   = 1;
    stSbArgs.ulNumPaths = 1;

    for (ulPlaneindex = 0; ulPlaneindex < pPlanes->uiPlaneCount; ulPlaneindex++)
    {
        ulPathIndex = pPlanes->stPlaneInfo[ulPlaneindex].iPathIndex; // Primary will have source as 0; Secondary will be 1
        if ((ulPathIndex + 1) > stSbArgs.ulNumPaths)
            stSbArgs.ulNumPaths = ulPathIndex + 1;

        ulPlaneIndexPerPipe = stSbArgs.stCheckMPOPathInfo[ulPathIndex].uiPlaneCount;

        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].uiLayerIndex = pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].bEnabled     = pPlanes->stPlaneInfo[ulPlaneindex].bEnabled;
        // ICL/RS2 changes to add uiOSPlaneNumber that driver returns incase checkMPO failure
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].uiOSPlaneNumber = ulPlaneindex + 1;

        // Default Parameters
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].bIsAsyncMMIOFlip = FALSE;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPOFlags.uiValue =
        pPlanes->stPlaneInfo[ulPlaneindex].stMPOFlipFlags.uiValue;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.eMPOVideoFormat    = SIMDRIVER_MPO_VIDEO_FRAME_FORMAT_PROGRESSIVE;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.uiMPOYCbCrFlags    = pPlanes->stPlaneInfo[ulPlaneindex].uiYCbCrFlags;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.eMPOStereoFormat   = SIMDRIVER_MPO_FORMAT_MONO;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.bMPOLeftViewFrame0 = 0;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.bMPOBaseViewFrame0 = 0;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.eMPOStereoFlipMode = SIMDRIVER_MPO_FLIP_NONE;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.eStretchQuality    = SIMDRIVER_MPO_STRETCH_QUALITY_BILINEAR;

        // Parameters from Python
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].eULTPixelFormat                       = pPlanes->stPlaneInfo[ulPlaneindex].ePixelFormat;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.eColorSpace         = pPlanes->stPlaneInfo[ulPlaneindex].eColorSpace;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPOSrcRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.bottom;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPOSrcRect.top    = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.top;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPOSrcRect.left   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.left;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPOSrcRect.right  = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.right;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPODstRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.bottom;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPODstRect.top    = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.top;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPODstRect.left   = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.left;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPODstRect.right  = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.right;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPOClipRect.bottom =
        pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.bottom;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPOClipRect.left  = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.left;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPOClipRect.right = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.right;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPOClipRect.top   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.top;

        // ICL/RS2 changes to include MPO Post Composition
        /*stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPOSrcRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.bottom;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPOSrcRect.top = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.top;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPOSrcRect.left = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.left;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPOSrcRect.right = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.right;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPODstRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.bottom;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPODstRect.top = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.top;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPODstRect.left = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.left;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPODstRect.right = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.right;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPOFlags.uiValue = 0;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.eHWOrientation = pPlanes->stPlaneInfo[ulPlaneindex].eHWOrientation;
        pPlanes->stPlaneInfo[ulPlaneindex].ResourceInfo.ulSourceHeight = pPlanes->stPlaneInfo[ulPlaneindex].MPODstRect.bottom - pPlanes->stPlaneInfo[ulPlaneindex].MPOSrcRect.top;
        pPlanes->stPlaneInfo[ulPlaneindex].ResourceInfo.ulSourceWidth = pPlanes->stPlaneInfo[ulPlaneindex].MPODstRect.right - pPlanes->stPlaneInfo[ulPlaneindex].MPOSrcRect.left;*/

        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.eHWOrientation = pPlanes->stPlaneInfo[ulPlaneindex].eHWOrientation;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stPlaneAttributes.stMPOBlend.uiValue =
        pPlanes->stPlaneInfo[ulPlaneindex].stMPOBlendVal.uiValue;
        stSbArgs.stCheckMPOPathInfo[ulPathIndex].stMPOPlaneInfo[ulPlaneIndexPerPipe].stSurfaceMemInfo.eSurfaceMemType = pPlanes->stPlaneInfo[ulPlaneindex].eSurfaceMemType;

        stSbArgs.stCheckMPOPathInfo[ulPathIndex].uiPlaneCount++;
    }

    stDisplayFeatureArgs.ulSize       = sizeof(SIMDRIVER_CHECK_MPO_ARGS);
    stDisplayFeatureArgs.eServiceType = SIMDRIVER_CHECK_MPO3;
    stDisplayFeatureArgs.pMpoArgs     = calloc(1, sizeof(SIMDRIVER_CHECK_MPO_ARGS));
    NULL_PTR_CHECK(stDisplayFeatureArgs.pMpoArgs);
    memcpy_s(stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_CHECK_MPO_ARGS), &stSbArgs, sizeof(SIMDRIVER_CHECK_MPO_ARGS));

    bStatus =
    ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &stDisplayFeatureArgs, sizeof(SIMDRIVER_DISPLAY_FEATURE_ARGS));

    memcpy_s(&stSbArgs, sizeof(SIMDRIVER_CHECK_MPO_ARGS), stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_CHECK_MPO_ARGS));
    FREE_MEMORY(stDisplayFeatureArgs.pMpoArgs);

    if (bStatus == FALSE)
    {
        ERROR_LOG("IOCTL failed in Check MPO3: %d", bStatus);
        return PLANES_FAILURE;
    }

    if (stSbArgs.bSupported == 0)
        return PLANES_FAILURE;
    else
        return PLANES_SUCCESS;
}

UINT mainline_SetSourceAddressForMultiPlaneOverlay3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes)
{
    BOOL                           bStatus         = FALSE;
    DWORD                          dwBytesReturned = 0;
    SIMDRIVER_DISPLAY_FEATURE_ARGS stDisplayFeatureArgs;
    SIMDRIVER_SET_SRC_ADD_MPO_ARGS stMPOFlipArgs[SIMDRIVER_MAX_PIPES] = { 0 };
    GFX_ADAPTER_INFO               adapterInfo                        = { 0 };
    INT                            ulPathIndex                        = 0;
    UINT                           ulPlaneindex = 0, ulPlaneIndexPerPipe = 0;
    UINT                           iLayerIndex     = 0;
    BOOL                           bResourceStatus = FALSE;

    // Sort PreviousPlanes based on current Planes order for easy comparison in resource creation.
    if (pPreviouspPlanes->uiPlaneCount != 0)
    {
        for (UINT currPlaneIndex = 0; currPlaneIndex < pPlanes->uiPlaneCount; currPlaneIndex++)
        {
            for (UINT prevPlaneIndex = 0; prevPlaneIndex < pPreviouspPlanes->uiPlaneCount; prevPlaneIndex++)
            {
                if ((pPlanes->stPlaneInfo[currPlaneIndex].stResourceInfo[0].pGmmBlock != 0 &&
                     pPlanes->stPlaneInfo[currPlaneIndex].stResourceInfo[0].pGmmBlock == pPreviouspPlanes->stPlaneInfo[prevPlaneIndex].stResourceInfo[0].pGmmBlock) ||
                    (pPlanes->stPlaneInfo[currPlaneIndex].stResourceInfo[1].pGmmBlock != 0 &&
                     pPlanes->stPlaneInfo[currPlaneIndex].stResourceInfo[1].pGmmBlock == pPreviouspPlanes->stPlaneInfo[prevPlaneIndex].stResourceInfo[1].pGmmBlock))
                {
                    if (currPlaneIndex != prevPlaneIndex)
                    {
                        PPLANE_INFO pPlaneInfo = malloc(sizeof(PLANE_INFO));
                        if (NULL == pPlaneInfo)
                        {
                            ERROR_LOG("NULL pointer");
                            continue;
                        }
                        memcpy(pPlaneInfo, &pPreviouspPlanes->stPlaneInfo[prevPlaneIndex], sizeof(PLANE_INFO));
                        memcpy(&pPreviouspPlanes->stPlaneInfo[prevPlaneIndex], &pPreviouspPlanes->stPlaneInfo[currPlaneIndex], sizeof(PLANE_INFO));
                        memcpy(&pPreviouspPlanes->stPlaneInfo[currPlaneIndex], pPlaneInfo, sizeof(PLANE_INFO));
                        FREE_MEMORY(pPlaneInfo);
                    }
                    break;
                }
            }
        }
        pPreviouspPlanes->uiPlaneCount = (pPlanes->uiPlaneCount > pPreviouspPlanes->uiPlaneCount) ? pPlanes->uiPlaneCount : pPreviouspPlanes->uiPlaneCount;
    }

    // Resource Allocation

    for (UINT PlaneIndex = 0; PlaneIndex < pPlanes->uiPlaneCount; PlaneIndex++)
    {
        INT  iResourceInUse                      = pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse;
        UINT uiLayerIndex                        = pPlanes->stPlaneInfo[PlaneIndex].uiLayerIndex;
        pPlanes->stPlaneInfo[PlaneIndex].lWidth  = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.right - pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.left;
        pPlanes->stPlaneInfo[PlaneIndex].lHeight = pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.bottom - pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.top;

        if (pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse].pGmmBlock == 0)
        {
            bResourceStatus = mainline_DFTCreateResource(pAdapterInfo, &pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse], pPlanes->stPlaneInfo[PlaneIndex].lWidth,
                                                         pPlanes->stPlaneInfo[PlaneIndex].lHeight, pPlanes->stPlaneInfo[PlaneIndex].ePixelFormat,
                                                         pPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType, uiLayerIndex, pPlanes->stPlaneInfo[PlaneIndex].cpDumpFilePath);
            if (bResourceStatus == FALSE)
                goto FreeResource;
        }
        else if (pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse].pGmmBlock != 0)
        {
            if (pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.right - pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.left !=
                pPreviouspPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.right - pPreviouspPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.left ||
                pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.bottom - pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.top !=
                pPreviouspPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.bottom - pPreviouspPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.top ||
                pPlanes->stPlaneInfo[PlaneIndex].ePixelFormat != pPreviouspPlanes->stPlaneInfo[PlaneIndex].ePixelFormat ||
                pPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType != pPreviouspPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType)
            {
                BOOLEAN iResourceInUseComplement = (iResourceInUse == 0) ? TRUE : FALSE;
                bResourceStatus =
                mainline_DFTCreateResource(pAdapterInfo, &pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUseComplement], pPlanes->stPlaneInfo[PlaneIndex].lWidth,
                                           pPlanes->stPlaneInfo[PlaneIndex].lHeight, pPlanes->stPlaneInfo[PlaneIndex].ePixelFormat,
                                           pPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType, uiLayerIndex, pPlanes->stPlaneInfo[PlaneIndex].cpDumpFilePath);
                pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse = iResourceInUseComplement;

                if (bResourceStatus == FALSE)
                    goto FreeResource;
            }
            else
            {
                // Resource already available
                bResourceStatus = TRUE;
            }
        }
    }

    for (ulPathIndex = 0; ulPathIndex < SIMDRIVER_MAX_PIPES; ulPathIndex++)
    {
        ulPlaneIndexPerPipe                           = 0;
        stMPOFlipArgs[ulPathIndex].ulNumPlanes        = 0;
        stMPOFlipArgs[ulPathIndex].stInputFlags.Value = 0;
        stMPOFlipArgs[ulPathIndex].pHDRMetaData       = NULL;
        for (ulPlaneindex = 0; ulPlaneindex < pPlanes->uiPlaneCount; ulPlaneindex++)
        {
            if (pPlanes->stPlaneInfo[ulPlaneindex].iPathIndex != ulPathIndex)
                continue;

            iLayerIndex                           = pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex;
            stMPOFlipArgs[ulPathIndex].dwSourceID = pPlanes->stPlaneInfo[ulPlaneindex].iPathIndex;

            stMPOFlipArgs[ulPathIndex].ulNumPlanes++;

            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].uiLayerIndex       = pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].uiOSLayerIndex     = pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].ulPresentID        = 1;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stInputFlags.Value = 1;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].bEnabled           = (BOOLEAN)pPlanes->stPlaneInfo[ulPlaneindex].bEnabled;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].hAllocation =
            (HANDLE)pPlanes->stPlaneInfo[ulPlaneindex].stResourceInfo[pPlanes->stPlaneInfo[ulPlaneindex].iResourceInUse].pGmmBlock;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].bAffected                              = TRUE;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].uiMaxImmediateFlipLine                 = 0;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stOutputFlags.FlipConvertedToImmediate = 0;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPOFlags.uiValue   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOFlipFlags.uiValue;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.eMPOVideoFormat      = SIMDRIVER_MPO_VIDEO_FRAME_FORMAT_PROGRESSIVE;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.uiMPOYCbCrFlags      = pPlanes->stPlaneInfo[ulPlaneindex].uiYCbCrFlags;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.eMPOStereoFormat     = SIMDRIVER_MPO_FORMAT_MONO;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.bMPOLeftViewFrame0   = 0;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.bMPOBaseViewFrame0   = 0;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.eMPOStereoFlipMode   = SIMDRIVER_MPO_FLIP_NONE;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.eStretchQuality      = SIMDRIVER_MPO_STRETCH_QUALITY_BILINEAR;

            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPOSrcRect.bottom  = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.bottom;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPOSrcRect.left    = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.left;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPOSrcRect.right   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.right;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPOSrcRect.top     = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.top;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPODstRect.bottom  = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.bottom;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPODstRect.left    = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.left;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPODstRect.right   = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.right;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPODstRect.top     = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.top;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPOClipRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.bottom;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPOClipRect.left   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.left;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPOClipRect.right  = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.right;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPOClipRect.top    = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.top;

            // HDR Metadata copy
            stMPOFlipArgs[ulPathIndex].pHDRMetaData = (PSIMDRIVER_MPO_HDR_METADATA)calloc(1, sizeof(SIMDRIVER_HDR_METADATA));
            if (NULL == stMPOFlipArgs[ulPathIndex].pHDRMetaData)
            {
                ERROR_LOG("NULL pointer");
                continue;
            }
            stMPOFlipArgs[ulPathIndex].pHDRMetaData->Size      = sizeof(MPO_HDR_STATIC_METADATA);
            stMPOFlipArgs[ulPathIndex].pHDRMetaData->pMetaData = (VOID *)&pPlanes->stMPOHDRMetaData;

            // ICL/RS2 changes to include MPO Post Composition

            /*stMPOFlipArgs[ulPathIndex].stMPOPostComposition.stMPOSrcRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.bottom;
            stMPOFlipArgs[ulPathIndex].stMPOPostComposition.stMPOSrcRect.top = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.top;
            stMPOFlipArgs[ulPathIndex].stMPOPostComposition.stMPOSrcRect.left = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.left;
            stMPOFlipArgs[ulPathIndex].stMPOPostComposition.stMPOSrcRect.right = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.right;
            stMPOFlipArgs[ulPathIndex].stMPOPostComposition.stMPODstRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.bottom;
            stMPOFlipArgs[ulPathIndex].stMPOPostComposition.stMPODstRect.top = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.top;
            stMPOFlipArgs[ulPathIndex].stMPOPostComposition.stMPODstRect.left = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.left;
            stMPOFlipArgs[ulPathIndex].stMPOPostComposition.stMPODstRect.right = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.right;
            stMPOFlipArgs[ulPathIndex].stMPOPostComposition.eHWOrientation = pPlanes->stPlaneInfo[ulPlaneindex].eHWOrientation;*/

            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.eHWOrientation     = pPlanes->stPlaneInfo[ulPlaneindex].eHWOrientation;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.stMPOBlend.uiValue = pPlanes->stPlaneInfo[ulPlaneindex].stMPOBlendVal.uiValue;
            stMPOFlipArgs[ulPathIndex].stDxgkMPOPlaneArgs[iLayerIndex].stPlaneAttributes.eColorSpace        = pPlanes->stPlaneInfo[ulPlaneindex].eColorSpace;

            ulPlaneIndexPerPipe++;
        }

        if (stMPOFlipArgs[ulPathIndex].ulNumPlanes > 0)
        {
            stDisplayFeatureArgs.ulSize       = sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS);
            stDisplayFeatureArgs.eServiceType = SIMDRIVER_SET_SOURCE_ADDRESS_MPO3;
            stDisplayFeatureArgs.pMpoArgs     = calloc(1, sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS));
            NULL_PTR_CHECK(stDisplayFeatureArgs.pMpoArgs);
            memcpy_s(stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS), &stMPOFlipArgs[ulPathIndex], sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS));

            bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &stDisplayFeatureArgs,
                                             sizeof(SIMDRIVER_DISPLAY_FEATURE_ARGS));

            memcpy_s(&stMPOFlipArgs[ulPathIndex], sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS), stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_SET_SRC_ADD_MPO_ARGS));
            FREE_MEMORY(stDisplayFeatureArgs.pMpoArgs);

            if (bStatus == FALSE)
            {
                ERROR_LOG("IOCTL failed in set source address MPO3: %d", bStatus);
                return PLANES_FAILURE;
            }
        }

        FREE_MEMORY(stMPOFlipArgs[ulPathIndex].pHDRMetaData);
    }

FreeResource:
    for (UINT PreviousIndex = 0; PreviousIndex < pPreviouspPlanes->uiPlaneCount; PreviousIndex++)
    {
        if (pPlanes->stPlaneInfo[PreviousIndex].iResourceInUse != pPreviouspPlanes->stPlaneInfo[PreviousIndex].iResourceInUse)
        {
            INT iResourceUsed = pPreviouspPlanes->stPlaneInfo[PreviousIndex].iResourceInUse;
            if (pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iResourceUsed].pGmmBlock != 0)
            {
                mainline_DFTFreeResource(pAdapterInfo, &pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iResourceUsed]);
                pPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iResourceUsed].pGmmBlock = 0;
            }
        }
        else
        {
            INT iCurrResourceUsed = pPlanes->stPlaneInfo[PreviousIndex].iResourceInUse;
            INT iPrevResourceUsed = pPreviouspPlanes->stPlaneInfo[PreviousIndex].iResourceInUse;
            if (pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iPrevResourceUsed].pGmmBlock != 0 &&
                pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iPrevResourceUsed].pGmmBlock !=
                pPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iCurrResourceUsed].pGmmBlock)
            {
                mainline_DFTFreeResource(pAdapterInfo, &pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iPrevResourceUsed]);
            }
        }
    }

    memcpy(pPreviouspPlanes, pPlanes, sizeof(_PLANES_));

    if (bResourceStatus == FALSE)
        return PLANES_RESOURCE_CREATION_FAILURE;

    return PLANES_SUCCESS;
}

BOOL mainline_GetMPOCaps(PGFX_ADAPTER_INFO pAdapterInfo, PMPO_CAPS_ARGS pMPOCaps)
{
    BOOL                           bStatus         = FALSE;
    DWORD                          dwBytesReturned = 0;
    SIMDRIVER_DISPLAY_FEATURE_ARGS stDisplayFeatureArgs;
    SIMDRIVER_MPO_CAPS_ARGS        SIMDRIVERArgs = { 0 };
    GFX_ADAPTER_INFO               adapterInfo   = { 0 };

    NULL_PTR_CHECK(pMPOCaps);
    SIMDRIVERArgs.ulVidpnSourceID = pMPOCaps->ulSourceID;

    stDisplayFeatureArgs.ulSize       = sizeof(SIMDRIVER_MPO_CAPS_ARGS);
    stDisplayFeatureArgs.eServiceType = SIMDRIVER_GET_MPO_CAPS;

    stDisplayFeatureArgs.pMpoArgs = calloc(1, sizeof(SIMDRIVER_MPO_CAPS_ARGS));
    NULL_PTR_CHECK(stDisplayFeatureArgs.pMpoArgs);
    memcpy_s(stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_MPO_CAPS_ARGS), &SIMDRIVERArgs, sizeof(SIMDRIVER_MPO_CAPS_ARGS));

    bStatus =
    ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &stDisplayFeatureArgs, sizeof(SIMDRIVER_DISPLAY_FEATURE_ARGS));

    memcpy_s(&SIMDRIVERArgs, sizeof(SIMDRIVER_MPO_CAPS_ARGS), stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_MPO_CAPS_ARGS));
    FREE_MEMORY(stDisplayFeatureArgs.pMpoArgs);

    if (bStatus == FALSE)
    {
        ERROR_LOG("IOCTL failed in MPO capabilities: %d", bStatus);
        return FALSE;
    }

    pMPOCaps->stMPOCaps.uiMaxPlanes           = SIMDRIVERArgs.stMPOCaps.uiMaxPlanes;
    pMPOCaps->stMPOCaps.uiNumCapabilityGroups = SIMDRIVERArgs.stMPOCaps.uiNumCapabilityGroups;

    return bStatus;
}

BOOL mainline_GetMPOGroupCaps(PGFX_ADAPTER_INFO pAdapterInfo, PMPO_GROUP_CAPS_ARGS pMPOGroupCaps, UINT uiGroupIndex)
{
    BOOL                           bStatus         = FALSE;
    DWORD                          dwBytesReturned = 0;
    SIMDRIVER_DISPLAY_FEATURE_ARGS stDisplayFeatureArgs;
    SIMDRIVER_MPO_GROUP_CAPS_ARGS  SIMDRIVERArgs = { 0 };
    GFX_ADAPTER_INFO               adapterInfo   = { 0 };

    NULL_PTR_CHECK(pMPOGroupCaps);
    if (uiGroupIndex < 0)
        return FALSE;

    SIMDRIVERArgs.ulVidpnSourceID = pMPOGroupCaps->ulSourceID;
    SIMDRIVERArgs.uiGroupIndex    = uiGroupIndex;

    stDisplayFeatureArgs.ulSize       = sizeof(SIMDRIVER_MPO_GROUP_CAPS_ARGS);
    stDisplayFeatureArgs.eServiceType = SIMDRIVER_GET_MPO_GROUP_CAPS;
    stDisplayFeatureArgs.pMpoArgs     = calloc(1, sizeof(SIMDRIVER_MPO_GROUP_CAPS_ARGS));
    NULL_PTR_CHECK(stDisplayFeatureArgs.pMpoArgs);
    memcpy_s(stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_MPO_GROUP_CAPS_ARGS), &SIMDRIVERArgs, sizeof(SIMDRIVER_MPO_GROUP_CAPS_ARGS));

    bStatus =
    ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &stDisplayFeatureArgs, sizeof(SIMDRIVER_DISPLAY_FEATURE_ARGS));

    memcpy_s(&SIMDRIVERArgs, sizeof(SIMDRIVER_MPO_GROUP_CAPS_ARGS), stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_MPO_GROUP_CAPS_ARGS));
    FREE_MEMORY(stDisplayFeatureArgs.pMpoArgs);

    if (bStatus == FALSE)
    {
        ERROR_LOG("IOCTL failed in MPO group capabilities: %d", bStatus);
        return FALSE;
    }

    pMPOGroupCaps->stMPOGroupCaps.uiMaxPlanes            = SIMDRIVERArgs.stMPOGroupCaps.uiMaxPlanes;
    pMPOGroupCaps->stMPOGroupCaps.uiMaxStretchFactorNum  = SIMDRIVERArgs.stMPOGroupCaps.uiMaxStretchFactorNum;
    pMPOGroupCaps->stMPOGroupCaps.uiMaxStretchFactorDenm = SIMDRIVERArgs.stMPOGroupCaps.uiMaxStretchFactorDenm;
    pMPOGroupCaps->stMPOGroupCaps.uiMaxShrinkFactorNum   = SIMDRIVERArgs.stMPOGroupCaps.uiMaxShrinkFactorNum;
    pMPOGroupCaps->stMPOGroupCaps.uiMaxShrinkFactorDenm  = SIMDRIVERArgs.stMPOGroupCaps.uiMaxShrinkFactorDenm;
    pMPOGroupCaps->stMPOGroupCaps.uiOverlayFtrCaps       = SIMDRIVERArgs.stMPOGroupCaps.uiOverlayFtrCaps;
    pMPOGroupCaps->stMPOGroupCaps.uiStereoCaps           = SIMDRIVERArgs.stMPOGroupCaps.uiStereoCaps;

    return bStatus;
}
