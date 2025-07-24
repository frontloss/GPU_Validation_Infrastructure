/**
 * @file		MPO.c
 * @brief	API's for MPO - DDRW
 *
 * Details of the file is as follows.
 * MPO Utility APIs for RS2 on DDRW
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
**  distributed, or disclosed in any way without Intel's prior express  **
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

#include "Yangra.h"
#include "ResourceManager.h"
#include "CommonArgs.h"
#include "..\CommonDetails.h"
#include "..\GfxValSimAccess.h"
#include "..\..\..\Logger\ETWTestLogging.h"

extern ULONG create_resource;
extern ULONG free_resource;
BOOL         is_mpo_enable = FALSE;

void TranslateOSInputColorInfoToDrv(IN PYPLANES_MPO_COLOR_SPACE_TYPE InValue, OUT DD_COLOR_PIXEL_DESC *pColorInfo);

BOOL DDRW_EnableDisableMPOFeature(PGFX_ADAPTER_INFO pAdapterInfo, BOOLEAN bEnable)
{
    BOOL             bStatus         = FALSE;
    DWORD            dwBytesReturned = 0;
    MPO_DATA         MpoData;
    GFX_ADAPTER_INFO adapterInfo = { 0 };
    if (bEnable == is_mpo_enable)
        return TRUE;

    MpoData.eMPOEvent = ENABLE_DISABLE_MPO;
    MpoData.pMPOArgs  = calloc(1, sizeof(BOOLEAN));
    NULL_PTR_CHECK(MpoData.pMPOArgs);

    memcpy_s(MpoData.pMPOArgs, sizeof(BOOLEAN), &bEnable, sizeof(BOOLEAN));
    MpoData.ulArgSize = sizeof(BOOLEAN);
    bStatus           = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &MpoData, sizeof(MPO_DATA));
    memcpy_s(&bEnable, sizeof(BOOLEAN), MpoData.pMPOArgs, sizeof(BOOLEAN));
    FREE_MEMORY(MpoData.pMPOArgs);
    is_mpo_enable = bEnable;
    return bStatus;
}

BOOL DDRW_EnableDisableMPOSimulation(PGFX_ADAPTER_INFO pAdapterInfo, HANDLE hGfxValSim, BOOL bEnable)
{
    BOOL bStatus = FALSE;
    if (bEnable)
    {
        if (DDRW_EnableDisableMPOFeature(pAdapterInfo, TRUE))
        {
            INFO_LOG("Entered to initialize prev planes");
            _flushall();
            pPreviouspPlanes = calloc(1, sizeof(_PLANES_));
            NULL_PTR_CHECK(pPreviouspPlanes);
            bStatus = TRUE;
        }
    }
    else
    {
        if (pPreviouspPlanes)
        {
            for (UINT PlaneIndex = 0; PlaneIndex < pPreviouspPlanes->uiPlaneCount; PlaneIndex++)
            {
                INT iResourceInUse = pPreviouspPlanes->stPlaneInfo[PlaneIndex].iResourceInUse;
                if (pPreviouspPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse].pGmmBlock)
                    DDRW_DFTFreeResource(pAdapterInfo, &pPreviouspPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse]);
            }
        }

        if (DDRW_EnableDisableMPOFeature(pAdapterInfo, FALSE))
        {
            bStatus = TRUE;
            FREE_MEMORY(pPreviouspPlanes);
        }
        INFO_LOG("Create Resource Count = %lu Free Resource Count = %lu", create_resource, free_resource);
    }
    return bStatus;
}

UINT DDRW_CheckForMultiPlaneOverlaySupport3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes)
{
    BOOL             bStatus = FALSE;
    MPO_DATA         MpoData;
    GFX_ADAPTER_INFO adapterInfo    = { 0 };
    DD_ARG_CHECK_MPO stCheckMPOArgs = { 0 };
    UINT             ulPathIndex = 0, ulPlaneindex = 0, ulPlaneIndexPerPipe = 0;
    DWORD            dwBytesReturned = 0;
    BOOL             bResourceStatus = FALSE;

    // Sort PreviousPlanes based on current Planes order for easy comparison in resource creation.
    _flushall();
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
                        PPLANE_INFO pPlaneInfo = calloc(1, sizeof(PLANE_INFO));
                        if (NULL == pPlaneInfo)
                        {
                            ERROR_LOG("NULL Pointer");
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

        // First GMM Block allocation
        if (pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse].pGmmBlock == 0)
        {
            bResourceStatus = DDRW_DFTCreateResource(pAdapterInfo, &pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse], pPlanes->stPlaneInfo[PlaneIndex].lWidth,
                                                     pPlanes->stPlaneInfo[PlaneIndex].lHeight, pPlanes->stPlaneInfo[PlaneIndex].ePixelFormat,
                                                     pPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType, uiLayerIndex, pPlanes->stPlaneInfo[PlaneIndex].cpDumpFilePath,
                                                     FALSE); // Keeping the IsAsyncFlip paramter as False as the first Async flip will get converted to AllParams flips
            if (bResourceStatus == FALSE)
            {
                bStatus = FALSE;
                goto FreeResource;
            }
        }
        // Subsequent GMM Block allocation
        else if (pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUse].pGmmBlock != 0)
        {
            // Create new resource if the prev plane and new plane parameters doesnt match or if the Flip type is Async
            if (pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.right - pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.left !=
                pPreviouspPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.right - pPreviouspPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.left ||
                pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.bottom - pPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.top !=
                pPreviouspPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.bottom - pPreviouspPlanes->stPlaneInfo[PlaneIndex].stMPOSrcRect.top ||
                pPlanes->stPlaneInfo[PlaneIndex].ePixelFormat != pPreviouspPlanes->stPlaneInfo[PlaneIndex].ePixelFormat ||
                pPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType != pPreviouspPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType ||
                pPlanes->stPlaneInfo[PlaneIndex].stMPOPlaneInFlags.FlipImmediate == 1)
            {
                BOOLEAN iResourceInUseComplement = (iResourceInUse == 0) ? TRUE : FALSE;
                bResourceStatus                  = DDRW_DFTCreateResource(
                pAdapterInfo, &pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceInUseComplement], pPlanes->stPlaneInfo[PlaneIndex].lWidth,
                pPlanes->stPlaneInfo[PlaneIndex].lHeight, pPlanes->stPlaneInfo[PlaneIndex].ePixelFormat, pPlanes->stPlaneInfo[PlaneIndex].eSurfaceMemType, uiLayerIndex,
                pPlanes->stPlaneInfo[PlaneIndex].cpDumpFilePath, (pPlanes->stPlaneInfo[PlaneIndex].stMPOPlaneInFlags.FlipImmediate == 1) ? TRUE : FALSE);
                pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse = iResourceInUseComplement;

                if (bResourceStatus == FALSE)
                {
                    bStatus = FALSE;
                    goto FreeResource;
                }
            }
            else
            {
                // Resource already available
                bResourceStatus = TRUE;
            }
        }
    }

    // Fill structure and call Check MPO
    stCheckMPOArgs.pViews = calloc(sizeof(DD_CHECK_MPO_VIEW_DETAILS), 8); // TODO: WA currently in driver, this is done for 8 views

    for (ulPlaneindex = 0; ulPlaneindex < pPlanes->uiPlaneCount; ulPlaneindex++)
    {
        ulPathIndex = pPlanes->stPlaneInfo[ulPlaneindex].iPathIndex; // Primary will have source as 0; Secondary will be 1

        ulPlaneIndexPerPipe = stCheckMPOArgs.pViews[ulPathIndex].PlaneCount;

        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].ulLayerIndex           = pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneInFlags.Enabled = pPlanes->stPlaneInfo[ulPlaneindex].bEnabled;

        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stFlags.ulValue         = 0;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stFlags.HorizontalFlip  = pPlanes->stPlaneInfo[ulPlaneindex].stMPOFlipFlags.HorizontalFlip;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stSource.lBottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.bottom;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stSource.lTop    = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.top;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stSource.lLeft   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.left;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stSource.lRight  = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.right;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stDest.lBottom   = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.bottom;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stDest.lTop      = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.top;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stDest.lLeft     = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.left;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stDest.lRight    = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.right;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stClip.lBottom   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.bottom;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stClip.lLeft     = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.left;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stClip.lRight    = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.right;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stClip.lTop      = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.top;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stBoundedDirtyRect.lBottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPODirtRect.bottom;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stBoundedDirtyRect.lLeft   = pPlanes->stPlaneInfo[ulPlaneindex].stMPODirtRect.left;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stBoundedDirtyRect.lRight  = pPlanes->stPlaneInfo[ulPlaneindex].stMPODirtRect.right;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stBoundedDirtyRect.lTop    = pPlanes->stPlaneInfo[ulPlaneindex].stMPODirtRect.top;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneInFlags.FlipImmediate = pPlanes->stPlaneInfo[ulPlaneindex].stMPOPlaneInFlags.FlipImmediate;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneInFlags.FlipImmediateNoTearing =
        pPlanes->stPlaneInfo[ulPlaneindex].stMPOPlaneInFlags.FlipImmediateNoTearing;

        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].hAllocation =
        (HANDLE)pPlanes->stPlaneInfo[ulPlaneindex].stResourceInfo[pPlanes->stPlaneInfo[ulPlaneindex].iResourceInUse].pGmmBlock;
        _flushall();
        // ICL/RS2 changes to include MPO Post Composition
        /*pSbArgs->stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPOSrcRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.bottom;
        pSbArgs->stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPOSrcRect.top = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.top;
        pSbArgs->stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPOSrcRect.left = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.left;
        pSbArgs->stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPOSrcRect.right = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.right;
        pSbArgs->stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPODstRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.bottom;
        pSbArgs->stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPODstRect.top = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.top;
        pSbArgs->stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPODstRect.left = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.left;
        pSbArgs->stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPODstRect.right = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.right;
        pSbArgs->stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.stMPOFlags.uiValue = 0;
        pSbArgs->stCheckMPOPathInfo[ulPathIndex].stMPOPostComposition.eHWOrientation = pPlanes->stPlaneInfo[ulPlaneindex].eHWOrientation;
        pPlanes->stPlaneInfo[ulPlaneindex].ResourceInfo.ulSourceHeight = pPlanes->stPlaneInfo[ulPlaneindex].MPODstRect.bottom - pPlanes->stPlaneInfo[ulPlaneindex].MPOSrcRect.top;
        pPlanes->stPlaneInfo[ulPlaneindex].ResourceInfo.ulSourceWidth = pPlanes->stPlaneInfo[ulPlaneindex].MPODstRect.right - pPlanes->stPlaneInfo[ulPlaneindex].MPOSrcRect.left;*/

        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.eRotation = pPlanes->stPlaneInfo[ulPlaneindex].eHWOrientation - 1;
        TranslateOSInputColorInfoToDrv(pPlanes->stPlaneInfo[ulPlaneindex].eColorSpace,
                                       &stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stColorInfo);
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stFlags.AlphaBlend = pPlanes->stPlaneInfo[ulPlaneindex].stMPOBlendVal.uiValue;

        stCheckMPOArgs.pViews[ulPathIndex].PlaneCount++;
    }

    MpoData.eMPOEvent = CHECK_MPO3;
    MpoData.pMPOArgs  = calloc(1, sizeof(DD_ARG_CHECK_MPO));
    NULL_PTR_CHECK(MpoData.pMPOArgs);
    memcpy_s(MpoData.pMPOArgs, sizeof(DD_ARG_CHECK_MPO), &stCheckMPOArgs, sizeof(DD_ARG_CHECK_MPO));
    MpoData.ulArgSize = sizeof(DD_ARG_CHECK_MPO);

    bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &MpoData, sizeof(MPO_DATA));

    memcpy_s(&stCheckMPOArgs, sizeof(DD_ARG_CHECK_MPO), MpoData.pMPOArgs, sizeof(DD_ARG_CHECK_MPO));
    FREE_MEMORY(MpoData.pMPOArgs);

FreeResource:
    if (bStatus && stCheckMPOArgs.Supported)
    {
        bStatus = TRUE;
    }
    else
    {
        // release the allocated memory in case CheckMPO failed
        for (UINT PlaneIndex = 0; PlaneIndex < pPlanes->uiPlaneCount; PlaneIndex++)
        {
            if (pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse == pPreviouspPlanes->stPlaneInfo[PlaneIndex].iResourceInUse)
            {
                INT iResourceUsed = pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse;
                if (pPreviouspPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceUsed].pGmmBlock == 0)
                {
                    DDRW_DFTFreeResource(pAdapterInfo, &pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iResourceUsed]);
                }
            }
            else
            {
                INT iCurrResourceUsed = pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse;
                INT iPrevResourceUsed = pPreviouspPlanes->stPlaneInfo[PlaneIndex].iResourceInUse;
                if (pPreviouspPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iPrevResourceUsed].pGmmBlock != 0 &&
                    pPreviouspPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iPrevResourceUsed].pGmmBlock !=
                    pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iCurrResourceUsed].pGmmBlock)
                {
                    BOOLEAN iResourceInUseComplement = (pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse == 0) ? TRUE : FALSE;
                    DDRW_DFTFreeResource(pAdapterInfo, &pPlanes->stPlaneInfo[PlaneIndex].stResourceInfo[iCurrResourceUsed]);
                    pPlanes->stPlaneInfo[PlaneIndex].iResourceInUse = iResourceInUseComplement;
                }
            }
        }
        bStatus = FALSE;
    }

    FREE_MEMORY(stCheckMPOArgs.pViews);
    if (bResourceStatus == FALSE)
        return PLANES_RESOURCE_CREATION_FAILURE;

    if (bStatus)
        return PLANES_SUCCESS;
    else
    {
        ERROR_LOG("IOCTL failed in Check MPO3: %d", bStatus);
        return PLANES_FAILURE;
    }
}

UINT DDRW_SetSourceAddressForMultiPlaneOverlay3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes)
{
    BOOL             bStatus = FALSE;
    MPO_DATA         MpoData;
    GFX_ADAPTER_INFO adapterInfo = { 0 };
    DD_ARG_FLIP_MPO  stFlipArgs[MAX_VIEWS];
    INT              ulPathIndex     = 0;
    UINT             ulPlaneindex    = 0;
    DWORD            dwBytesReturned = 0;
    LARGE_INTEGER    Frequency;
    LARGE_INTEGER    PerformanceTime;
    ULONG64          CurrentTime;
    static UINT      uiPresentId = 1;

    memset(stFlipArgs, 0, sizeof(DD_ARG_FLIP_MPO));
    QueryPerformanceFrequency(&Frequency);

    for (ulPathIndex = 0; ulPathIndex < MAX_VIEWS; ulPathIndex++)
    {
        DEBUG_LOG("%d duration in flip args incoming %d", stFlipArgs[ulPathIndex].ulDuration, pPlanes->uDuration);
        stFlipArgs[ulPathIndex].ulPlaneCount          = 0;
        stFlipArgs[ulPathIndex].stCommonInFlags.Value = 0;
        stFlipArgs[ulPathIndex].pPlanes               = calloc(MAX_PLANES_PER_PIPE, sizeof(DD_FLIP_MPO_PLANE));
        NULL_PTR_CHECK(stFlipArgs[ulPathIndex].pPlanes);
        // stFlipArgs[ulPathIndex].pHDRMetaData = NULL;
        for (ulPlaneindex = 0; ulPlaneindex < pPlanes->uiPlaneCount; ulPlaneindex++)
        {
            if (pPlanes->stPlaneInfo[ulPlaneindex].iPathIndex != ulPathIndex)
                continue;

            stFlipArgs[ulPathIndex].ulVidPnSourceId = pPlanes->stPlaneInfo[ulPlaneindex].iPathIndex;

            // Considering Plane count here as Plane count indexing starts with 0.
            // With using layer index, there is possiblity that data will be copied to index1 but flip params considered will be from index 0 (For only layer1 cases)
            UINT ulLayerIndex = stFlipArgs[ulPathIndex].ulPlaneCount;

            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].ulLayerIndex           = pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].ulPresentId            = uiPresentId++;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneInFlags.Value   = 0;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneInFlags.Enabled = pPlanes->stPlaneInfo[ulPlaneindex].bEnabled;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].hAllocation =
            (HANDLE)pPlanes->stPlaneInfo[ulPlaneindex].stResourceInfo[pPlanes->stPlaneInfo[ulPlaneindex].iResourceInUse].pGmmBlock;
            _flushall();
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].ulMaxImmediateFlipLine                       = pPlanes->stPlaneInfo[ulPlaneindex].ulMaxImmediateFlipLine;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneOutFlags.FlipConvertedToImmediate     = 0;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stFlags.ulValue            = 0;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stFlags.HorizontalFlip     = pPlanes->stPlaneInfo[ulPlaneindex].stMPOFlipFlags.HorizontalFlip;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lBottom    = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.bottom;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lLeft      = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.left;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lRight     = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.right;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lTop       = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.top;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lBottom      = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.bottom;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lLeft        = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.left;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lRight       = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.right;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lTop         = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.top;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lBottom      = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.bottom;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lLeft        = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.left;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lRight       = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.right;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lTop         = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.top;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lBottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPODirtRect.bottom;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lLeft   = pPlanes->stPlaneInfo[ulPlaneindex].stMPODirtRect.left;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lRight  = pPlanes->stPlaneInfo[ulPlaneindex].stMPODirtRect.right;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lTop    = pPlanes->stPlaneInfo[ulPlaneindex].stMPODirtRect.top;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneInFlags.FlipImmediate                 = pPlanes->stPlaneInfo[ulPlaneindex].stMPOPlaneInFlags.FlipImmediate;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneInFlags.FlipImmediateNoTearing = pPlanes->stPlaneInfo[ulPlaneindex].stMPOPlaneInFlags.FlipImmediateNoTearing;

            INFO_LOG("Metadata Luminance Values : %d %d %d %d ", pPlanes->stMPOHDRMetaData.usMaxDisplayMasteringLuminance, pPlanes->stMPOHDRMetaData.usMinDisplayMasteringLuminance,
                     pPlanes->stMPOHDRMetaData.usMaxCLL, pPlanes->stMPOHDRMetaData.usMaxFALL);

            // Logging Mpo3Flip Plane in ETL
            EtwMpo3FlipPlane(pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex, pPlanes->stPlaneInfo[ulPlaneindex].stMPOPlaneInFlags.uiValue,
                             stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].ulPresentId, 0xFFFFFFFF);

            // Logging Mpo3Flip Plane Details in ETL - not logging Colorspace, StretchQuality and SDRWhitelevel now
            EtwMpo3FlipPlane_Details(
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].ulMaxImmediateFlipLine, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stFlags.ulValue,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stFlags.AlphaBlend, 256, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.eRotation, 256,
            256, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lLeft,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lTop,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lRight,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lBottom,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lLeft, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lTop,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lRight,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lBottom,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lLeft, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lTop,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lRight,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lBottom,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lLeft,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lTop,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lRight,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lBottom, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].hAllocation);

            // HDR Metadata copy
            stFlipArgs[ulPathIndex].HDRMetaData.HdrMetadataType = DD_MPO_HDR_METADATA_TYPE_HDR10;
            memcpy(&stFlipArgs[ulPathIndex].HDRMetaData.HdrStaticMetaData, &pPlanes->stMPOHDRMetaData, sizeof(DD_HDR_STATIC_METADATA));

            // ICL/RS2 changes to include MPO Post Composition

            /*stFlipArgs[ulPathIndex].stMPOPostComposition.stMPOSrcRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.bottom;
            stFlipArgs[ulPathIndex].stMPOPostComposition.stMPOSrcRect.top = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.top;
            stFlipArgs[ulPathIndex].stMPOPostComposition.stMPOSrcRect.left = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.left;
            stFlipArgs[ulPathIndex].stMPOPostComposition.stMPOSrcRect.right = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.right;
            stFlipArgs[ulPathIndex].stMPOPostComposition.stMPODstRect.bottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.bottom;
            stFlipArgs[ulPathIndex].stMPOPostComposition.stMPODstRect.top = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.top;
            stFlipArgs[ulPathIndex].stMPOPostComposition.stMPODstRect.left = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.left;
            stFlipArgs[ulPathIndex].stMPOPostComposition.stMPODstRect.right = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.right;
            stFlipArgs[ulPathIndex].stMPOPostComposition.eHWOrientation = pPlanes->stPlaneInfo[ulPlaneindex].eHWOrientation;*/

            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.eRotation = pPlanes->stPlaneInfo[ulPlaneindex].eHWOrientation - 1;
            TranslateOSInputColorInfoToDrv(pPlanes->stPlaneInfo[ulPlaneindex].eColorSpace, &stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stColorInfo);
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stFlags.AlphaBlend = pPlanes->stPlaneInfo[ulPlaneindex].stMPOBlendVal.uiValue;

            stFlipArgs[ulPathIndex].ulPlaneCount++;
        }

        QueryPerformanceCounter(&PerformanceTime);
        CurrentTime                                = (PerformanceTime.QuadPart * 1000000) / Frequency.QuadPart;
        stFlipArgs[ulPathIndex].TargetFlipTimeInUs = CurrentTime;
        stFlipArgs[ulPathIndex].TargetFlipTime     = PerformanceTime.QuadPart;
        stFlipArgs[ulPathIndex].ulDuration         = pPlanes->uDuration;

        if (stFlipArgs[ulPathIndex].ulPlaneCount > 0)
        {
            MpoData.eMPOEvent         = SET_SOURCE_ADDRESS3;
            MpoData.pMPOArgs          = calloc(1, sizeof(DD_ARG_FLIP_MPO));
            MpoData.pMpoFlipDelayArgs = calloc(1, sizeof(MPO_FLIP_DELAY_ARGS));
            if (NULL == MpoData.pMPOArgs)
            {
                ERROR_LOG("NULL pointer");
                FREE_MEMORY(stFlipArgs[ulPathIndex].pPlanes);
                return FALSE;
            }
            memcpy_s(MpoData.pMPOArgs, sizeof(DD_ARG_FLIP_MPO), &stFlipArgs[ulPathIndex], sizeof(DD_ARG_FLIP_MPO));
            MpoData.ulArgSize = sizeof(DD_ARG_FLIP_MPO);

            memcpy_s(MpoData.pMpoFlipDelayArgs, sizeof(MPO_FLIP_DELAY_ARGS), &pPlanes->stMpoFlipDelayArgs[ulPathIndex], sizeof(MPO_FLIP_DELAY_ARGS));

            EtwMpo3FlipData(stFlipArgs[ulPathIndex].ulVidPnSourceId, stFlipArgs[ulPathIndex].stCommonInFlags.Value, stFlipArgs[ulPathIndex].ulPlaneCount,
                            stFlipArgs[ulPathIndex].ulDuration, stFlipArgs[ulPathIndex].TargetFlipTimeInUs);

            bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &MpoData, sizeof(MPO_DATA));

            memcpy_s(&stFlipArgs[ulPathIndex], sizeof(DD_ARG_FLIP_MPO), MpoData.pMPOArgs, sizeof(DD_ARG_FLIP_MPO));
            FREE_MEMORY(MpoData.pMPOArgs);
            FREE_MEMORY(MpoData.pMpoFlipDelayArgs);
        }
        FREE_MEMORY(stFlipArgs[ulPathIndex].pPlanes);
    }

    // Freeing the previous planes resource
    for (UINT PreviousIndex = 0; PreviousIndex < pPreviouspPlanes->uiPlaneCount; PreviousIndex++)
    {
        if (pPlanes->stPlaneInfo[PreviousIndex].iResourceInUse != pPreviouspPlanes->stPlaneInfo[PreviousIndex].iResourceInUse)
        {
            INT iResourceUsed = pPreviouspPlanes->stPlaneInfo[PreviousIndex].iResourceInUse;
            if (pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iResourceUsed].pGmmBlock != 0)
            {
                DDRW_DFTFreeResource(pAdapterInfo, &pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iResourceUsed]);
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
                DDRW_DFTFreeResource(pAdapterInfo, &pPreviouspPlanes->stPlaneInfo[PreviousIndex].stResourceInfo[iPrevResourceUsed]);
            }
        }
    }

    memcpy(pPreviouspPlanes, pPlanes, sizeof(_PLANES_));

    if (bStatus)
        return PLANES_SUCCESS;
    else
    {
        ERROR_LOG("IOCTL failed in set source address MPO3: %d", bStatus);
        return PLANES_FAILURE;
    }
}

BOOL DDRW_GetMPOCaps(PGFX_ADAPTER_INFO pAdapterInfo, PMPO_CAPS_ARG pMPOCaps)
{
    BOOL                bStatus = FALSE;
    MPO_DATA            MpoData;
    DD_GET_MPO_CAPS_ARG stMPOCapArgs;
    DWORD               dwBytesReturned = 0;

    if (pMPOCaps == NULL)
        return FALSE;

    stMPOCapArgs.VidPnSourceId = pMPOCaps->VidPnSourceId;

    MpoData.eMPOEvent = GET_OVERLAY_CAPS;
    MpoData.pMPOArgs  = calloc(1, sizeof(DD_GET_MPO_CAPS_ARG));
    NULL_PTR_CHECK(MpoData.pMPOArgs);
    memcpy_s(MpoData.pMPOArgs, sizeof(DD_GET_MPO_CAPS_ARG), &stMPOCapArgs, sizeof(DD_GET_MPO_CAPS_ARG));
    MpoData.ulArgSize = sizeof(DD_GET_MPO_CAPS_ARG);

    bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &MpoData, sizeof(MPO_DATA));

    memcpy_s(&stMPOCapArgs, sizeof(DD_GET_MPO_CAPS_ARG), MpoData.pMPOArgs, sizeof(DD_GET_MPO_CAPS_ARG));
    FREE_MEMORY(MpoData.pMPOArgs);

    if (bStatus == FALSE)
    {
        ERROR_LOG("IOCTL failed in MPO capabilities: %d", bStatus);
        return FALSE;
    }

    pMPOCaps->MaxPlanes                         = stMPOCapArgs.MaxPlanes;
    pMPOCaps->MaxRgbPlanes                      = stMPOCapArgs.MaxRgbPlanes;
    pMPOCaps->MaxYuvPlanes                      = stMPOCapArgs.MaxYuvPlanes;
    pMPOCaps->OverlayCaps.Value                 = stMPOCapArgs.OverlayCaps.Value;
    pMPOCaps->MaxStretchFactorMultBy100         = stMPOCapArgs.MaxStretchFactorMultBy100;
    pMPOCaps->MaxShrinkFactorPlanarMultBy100    = stMPOCapArgs.MaxShrinkFactorPlanarMultBy100;
    pMPOCaps->MaxShrinkFactorNonPlanarMultBy100 = stMPOCapArgs.MaxShrinkFactorNonPlanarMultBy100;
    pMPOCaps->MaxFlipQueues                     = stMPOCapArgs.MaxFlipQueues;
    pMPOCaps->MaxFlipQueueDepth                 = stMPOCapArgs.MaxFlipQueueDepth;
    pMPOCaps->MaxPlaneOffset                    = stMPOCapArgs.MaxPlaneOffset;

    INFO_LOG("Size: %lu Queue: %ld Queue depth: %ld", sizeof(stMPOCapArgs), pMPOCaps->MaxFlipQueues, pMPOCaps->MaxFlipQueueDepth);

    return bStatus;
}

void TranslateOSInputColorInfoToDrv(IN PYPLANES_MPO_COLOR_SPACE_TYPE InValue, OUT DD_COLOR_PIXEL_DESC *pColorInfo)
{
    switch (InValue)
    {
    case PYPLANES_MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_709, DD_COLOR_RANGE_TYPE_FULL, DD_COLOR_MODEL_RGB, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_RGB_FULL_G10_NONE_P709:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_709, DD_COLOR_RANGE_TYPE_FULL, DD_COLOR_MODEL_SCRGB, DD_COLOR_ENCODING_LINEAR);
        break;

    case PYPLANES_MPO_COLOR_SPACE_RGB_STUDIO_G22_NONE_P709:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_709, DD_COLOR_RANGE_TYPE_LIMITED, DD_COLOR_MODEL_RGB, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_RGB_STUDIO_G22_NONE_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_LIMITED, DD_COLOR_MODEL_RGB, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_FULL_G22_NONE_P709_X601:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_709, DD_COLOR_RANGE_TYPE_FULL, DD_COLOR_MODEL_YCBCR_601, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P601:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_709, DD_COLOR_RANGE_TYPE_LIMITED, DD_COLOR_MODEL_YCBCR_601, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P601:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_709, DD_COLOR_RANGE_TYPE_FULL, DD_COLOR_MODEL_YCBCR_601, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_709, DD_COLOR_RANGE_TYPE_LIMITED, DD_COLOR_MODEL_YCBCR_709, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P709:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_709, DD_COLOR_RANGE_TYPE_FULL, DD_COLOR_MODEL_YCBCR_709, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_LIMITED, DD_COLOR_MODEL_YCBCR_2020, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_FULL, DD_COLOR_MODEL_YCBCR_2020, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_FULL, DD_COLOR_MODEL_RGB, DD_COLOR_ENCODING_2084);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G2084_LEFT_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_LIMITED, DD_COLOR_MODEL_YCBCR_2020, DD_COLOR_ENCODING_2084);
        break;

    case PYPLANES_MPO_COLOR_SPACE_RGB_STUDIO_G2084_NONE_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_LIMITED, DD_COLOR_MODEL_RGB, DD_COLOR_ENCODING_2084);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G22_TOPLEFT_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_LIMITED, DD_COLOR_MODEL_YCBCR_2020, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_G2084_TOPLEFT_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_LIMITED, DD_COLOR_MODEL_YCBCR_2020, DD_COLOR_ENCODING_2084);
        break;

    case PYPLANES_MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_FULL, DD_COLOR_MODEL_RGB, DD_COLOR_ENCODING_SRGB);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_STUDIO_GHLG_TOPLEFT_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_LIMITED, DD_COLOR_MODEL_YCBCR_2020, DD_COLOR_ENCODING_HLG);
        break;

    case PYPLANES_MPO_COLOR_SPACE_YCBCR_FULL_GHLG_TOPLEFT_P2020:
        FILL_RGB_COLOR_INFO(pColorInfo, DD_COLOR_GAMUT_2020, DD_COLOR_RANGE_TYPE_FULL, DD_COLOR_MODEL_YCBCR_2020, DD_COLOR_ENCODING_HLG);
        break;

    case PYPLANES_MPO_COLOR_SPACE_CUSTOM:
    case PYPLANES_MPO_COLOR_SPACE_RESERVED:
        return;
    default:
        break;
    }
    return;
}

BOOL FlipQEnableDisableMPOSimulation(PGFX_ADAPTER_INFO pAdapterInfo, HANDLE hGfxValSim, BOOL bEnable)
{
    BOOL bStatus = FALSE;

    if (bEnable)
    {
        if (DDRW_EnableDisableMPOFeature(pAdapterInfo, TRUE))
        {
            _flushall();
            bStatus = TRUE;
        }
    }
    else
    {
        if (DDRW_EnableDisableMPOFeature(pAdapterInfo, FALSE))
        {
            bStatus = TRUE;
        }
        INFO_LOG("Create Resource Count = %lu Free Resource Count = %lu", create_resource, free_resource);
    }

    return bStatus;
}

UINT FlipQCheckForMultiPlaneOverlaySupport3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes)
{
    BOOL             bStatus = FALSE;
    MPO_DATA         MpoData;
    GFX_ADAPTER_INFO adapterInfo    = { 0 };
    DD_ARG_CHECK_MPO stCheckMPOArgs = { 0 };
    UINT             ulPathIndex = 0, ulPlaneindex = 0, ulPlaneIndexPerPipe = 0;
    DWORD            dwBytesReturned = 0;
    BOOL             bResourceStatus = FALSE;

    // Fill structure and call Check MPO
    stCheckMPOArgs.pViews = calloc(sizeof(DD_CHECK_MPO_VIEW_DETAILS), 8); // TODO: WA currently in driver, this is done for 8 views
    NULL_PTR_CHECK(stCheckMPOArgs.pViews);

    for (ulPlaneindex = 0; ulPlaneindex < pPlanes->uiPlaneCount; ulPlaneindex++)
    {
        ulPathIndex = pPlanes->stPlaneInfo[ulPlaneindex].iPathIndex; // Primary will have source as 0; Secondary will be 1

        ulPlaneIndexPerPipe = stCheckMPOArgs.pViews[ulPathIndex].PlaneCount;

        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].ulLayerIndex           = pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneInFlags.Enabled = pPlanes->stPlaneInfo[ulPlaneindex].bEnabled;

        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stFlags.ulValue         = 0;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stFlags.HorizontalFlip  = pPlanes->stPlaneInfo[ulPlaneindex].stMPOFlipFlags.HorizontalFlip;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stSource.lBottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.bottom;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stSource.lTop    = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.top;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stSource.lLeft   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.left;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stSource.lRight  = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.right;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stDest.lBottom   = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.bottom;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stDest.lTop      = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.top;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stDest.lLeft     = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.left;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stDest.lRight    = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.right;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stClip.lBottom   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.bottom;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stClip.lLeft     = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.left;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stClip.lRight    = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.right;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stRect.stClip.lTop      = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.top;
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneInFlags.FlipImmediate = pPlanes->stPlaneInfo[ulPlaneindex].stMPOPlaneInFlags.FlipImmediate;

        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].hAllocation =
        (HANDLE)pPlanes->stPlaneInfo[ulPlaneindex].stResourceInfo[pPlanes->stPlaneInfo[ulPlaneindex].iResourceInUse].pGmmBlock;

        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.eRotation = pPlanes->stPlaneInfo[ulPlaneindex].eHWOrientation - 1;
        TranslateOSInputColorInfoToDrv(pPlanes->stPlaneInfo[ulPlaneindex].eColorSpace,
                                       &stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stColorInfo);
        stCheckMPOArgs.pViews[ulPathIndex].Planes[ulPlaneIndexPerPipe].stPlaneAttributes.stFlags.AlphaBlend = pPlanes->stPlaneInfo[ulPlaneindex].stMPOBlendVal.uiValue;

        stCheckMPOArgs.pViews[ulPathIndex].PlaneCount++;
    }

    MpoData.eMPOEvent = CHECK_MPO3;
    MpoData.pMPOArgs  = calloc(1, sizeof(DD_ARG_CHECK_MPO));
    if (NULL == MpoData.pMPOArgs)
    {
        ERROR_LOG("NULL pointer");
        FREE_MEMORY(stCheckMPOArgs.pViews);
        return FALSE;
    }
    memcpy_s(MpoData.pMPOArgs, sizeof(DD_ARG_CHECK_MPO), &stCheckMPOArgs, sizeof(DD_ARG_CHECK_MPO));
    MpoData.ulArgSize = sizeof(DD_ARG_CHECK_MPO);

    bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &MpoData, sizeof(MPO_DATA));
    memcpy_s(&stCheckMPOArgs, sizeof(DD_ARG_CHECK_MPO), MpoData.pMPOArgs, sizeof(DD_ARG_CHECK_MPO));

    if (bStatus && stCheckMPOArgs.Supported)
    {
        bStatus = TRUE;
    }
    FREE_MEMORY(MpoData.pMPOArgs);
    FREE_MEMORY(stCheckMPOArgs.pViews);

    if (bStatus)
        return PLANES_SUCCESS;
    else
    {
        ERROR_LOG("IOCTL failed in Check MPO3: %d", bStatus);
        return PLANES_FAILURE;
    }
}

UINT FlipQSetSourceAddressForMultiPlaneOverlay3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes)
{
    static UINT      uiPresentTd = 1;
    BOOL             bStatus     = FALSE;
    MPO_DATA         MpoData;
    GFX_ADAPTER_INFO adapterInfo = { 0 };
    DD_ARG_FLIP_MPO  stFlipArgs[MAX_VIEWS];
    INT              ulPathIndex     = 0;
    UINT             ulPlaneindex    = 0;
    DWORD            dwBytesReturned = 0;
    LARGE_INTEGER    Frequency;
    LARGE_INTEGER    PerformanceTime;
    ULONG64          CurrentTime;
    ULONG64          Delay;
    memset(stFlipArgs, 0, sizeof(DD_ARG_FLIP_MPO));

    QueryPerformanceFrequency(&Frequency);

    for (ulPathIndex = 0; ulPathIndex < MAX_VIEWS; ulPathIndex++)
    {
        stFlipArgs[ulPathIndex].ulPlaneCount          = 0;
        stFlipArgs[ulPathIndex].stCommonInFlags.Value = 0;
        stFlipArgs[ulPathIndex].pPlanes               = calloc(MAX_PLANES_PER_PIPE, sizeof(DD_FLIP_MPO_PLANE));
        NULL_PTR_CHECK(stFlipArgs[ulPathIndex].pPlanes);
        for (ulPlaneindex = 0; ulPlaneindex < pPlanes->uiPlaneCount; ulPlaneindex++)
        {
            if (pPlanes->stPlaneInfo[ulPlaneindex].iPathIndex != ulPathIndex)
                continue;

            stFlipArgs[ulPathIndex].ulVidPnSourceId = pPlanes->stPlaneInfo[ulPlaneindex].iPathIndex;

            // Considering Plane count here as Plane count indexing starts with 0.
            // With using layer index, there is possiblity that data will be copied to index1 but flip params considered will be from index 0 (For only layer1 cases)
            UINT ulLayerIndex = stFlipArgs[ulPathIndex].ulPlaneCount;

            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].ulLayerIndex           = pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].ulPresentId            = uiPresentTd++;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneInFlags.Value   = 0;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneInFlags.Enabled = pPlanes->stPlaneInfo[ulPlaneindex].bEnabled;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].hAllocation =
            (HANDLE)pPlanes->stPlaneInfo[ulPlaneindex].stResourceInfo[pPlanes->stPlaneInfo[ulPlaneindex].iResourceInUse].pGmmBlock;
            _flushall();
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].ulMaxImmediateFlipLine                    = pPlanes->stPlaneInfo[ulPlaneindex].ulMaxImmediateFlipLine;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneOutFlags.FlipConvertedToImmediate  = 0;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stFlags.ulValue         = 0;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stFlags.HorizontalFlip  = pPlanes->stPlaneInfo[ulPlaneindex].stMPOFlipFlags.HorizontalFlip;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lBottom = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.bottom;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lLeft   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.left;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lRight  = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.right;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lTop    = pPlanes->stPlaneInfo[ulPlaneindex].stMPOSrcRect.top;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lBottom   = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.bottom;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lLeft     = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.left;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lRight    = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.right;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lTop      = pPlanes->stPlaneInfo[ulPlaneindex].stMPODstRect.top;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lBottom   = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.bottom;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lLeft     = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.left;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lRight    = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.right;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lTop      = pPlanes->stPlaneInfo[ulPlaneindex].stMPOClipRect.top;
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneInFlags.FlipImmediate              = pPlanes->stPlaneInfo[ulPlaneindex].stMPOPlaneInFlags.FlipImmediate;
            // HDR Metadata copy
            stFlipArgs[ulPathIndex].HDRMetaData.HdrMetadataType = DD_MPO_HDR_METADATA_TYPE_HDR10;
            memcpy(&stFlipArgs[ulPathIndex].HDRMetaData.HdrStaticMetaData, &pPlanes->stMPOHDRMetaData, sizeof(DD_HDR_STATIC_METADATA));

            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.eRotation = pPlanes->stPlaneInfo[ulPlaneindex].eHWOrientation - 1;
            TranslateOSInputColorInfoToDrv(pPlanes->stPlaneInfo[ulPlaneindex].eColorSpace, &stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stColorInfo);
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stFlags.AlphaBlend = pPlanes->stPlaneInfo[ulPlaneindex].stMPOBlendVal.uiValue;

            stFlipArgs[ulPathIndex].ulPlaneCount++;

            // Logging Mpo3Flip Plane in ETL
            EtwMpo3FlipPlane(pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex, pPlanes->stPlaneInfo[ulPlaneindex].stMPOPlaneInFlags.uiValue,
                             stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].ulPresentId, 0xFFFFFFFF);

            // Logging Mpo3Flip Plane Details in ETL - not logging Colorspace, StretchQuality and SDRWhitelevel now
            EtwMpo3FlipPlane_Details(
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].ulMaxImmediateFlipLine, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stFlags.ulValue,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stFlags.AlphaBlend, 256, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.eRotation, 256,
            256, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lLeft,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lTop,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lRight,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stSource.lBottom,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lLeft, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lTop,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lRight,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stDest.lBottom,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lLeft, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lTop,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lRight,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stRect.stClip.lBottom,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lLeft,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lTop,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lRight,
            stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].stPlaneAttributes.stBoundedDirtyRect.lBottom, stFlipArgs[ulPathIndex].pPlanes[ulLayerIndex].hAllocation);
        }

        stFlipArgs[ulPathIndex].TargetFlipTimeInUs = (ULONG64)((pPlanes->ulTargetFlipTime * 1000000) / Frequency.QuadPart);
        QueryPerformanceCounter(&PerformanceTime);
        CurrentTime                            = (PerformanceTime.QuadPart * 1000000) / Frequency.QuadPart;
        Delay                                  = stFlipArgs[ulPathIndex].TargetFlipTimeInUs - CurrentTime;
        pPlanes->uldelay                       = Delay;
        stFlipArgs[ulPathIndex].TargetFlipTime = pPlanes->ulTargetFlipTime;
        INFO_LOG("Target Fliptime = %lu", stFlipArgs[ulPathIndex].TargetFlipTimeInUs);

        if (stFlipArgs[ulPathIndex].ulPlaneCount > 0)
        {
            MpoData.eMPOEvent         = SET_SOURCE_ADDRESS3;
            MpoData.pMPOArgs          = calloc(1, sizeof(DD_ARG_FLIP_MPO));
            MpoData.pMpoFlipDelayArgs = calloc(1, sizeof(MPO_FLIP_DELAY_ARGS));
            if (NULL == MpoData.pMPOArgs)
            {
                ERROR_LOG("NULL pointer");
                FREE_MEMORY(stFlipArgs[ulPathIndex].pPlanes);
                return FALSE;
            }
            memcpy_s(MpoData.pMPOArgs, sizeof(DD_ARG_FLIP_MPO), &stFlipArgs[ulPathIndex], sizeof(DD_ARG_FLIP_MPO));
            MpoData.ulArgSize = sizeof(DD_ARG_FLIP_MPO);

            memcpy_s(MpoData.pMpoFlipDelayArgs, sizeof(MPO_FLIP_DELAY_ARGS), &pPlanes->stMpoFlipDelayArgs[ulPathIndex], sizeof(MPO_FLIP_DELAY_ARGS));

            bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &MpoData, sizeof(MPO_DATA));

            memcpy_s(&stFlipArgs[ulPathIndex], sizeof(DD_ARG_FLIP_MPO), MpoData.pMPOArgs, sizeof(DD_ARG_FLIP_MPO));
            FREE_MEMORY(MpoData.pMPOArgs);
            FREE_MEMORY(MpoData.pMpoFlipDelayArgs);
        }
        FREE_MEMORY(stFlipArgs[ulPathIndex].pPlanes);
    }

    if (bStatus)
        return PLANES_SUCCESS;
    else
    {
        ERROR_LOG("IOCTL failed in set source address MPO3: %d", bStatus);
        return PLANES_FAILURE;
    }
}