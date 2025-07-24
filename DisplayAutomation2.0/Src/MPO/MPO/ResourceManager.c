/**
 * @file		DivaAccess.c
 * @brief	API's for Resource creation
 *
 * @author	  Ilamparithi Mahendran, Anjali Shetty
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

#include <stdio.h>
#include <time.h>
#include "ResourceManager.h"
#include "..\inc\mainline\GfxValStub_DisplayFeature.h"
#include "../Logger/log.h"

ULONG create_resource = 0;
ULONG free_resource   = 0;

/* Structs to enable/disbale feature(s)*/
typedef struct _GVSTUB_FEATURE_INFO_ARGS
{
    GVSTUB_META_DATA stFeatureMetaData; // stValStubFeatureBasicInfo.ulServiceType as GFX_VAL_STUB_FEATURE_TYPE
    union {
        GVSTUB_DISPLAY_FEATURE_ARGS stDisplayFeatureArgs; // Access Display features like MPO/DeviceSimulation etc.
    };
} GVSTUB_FEATURE_INFO_ARGS, *PGVSTUB_FEATURE_INFO_ARGS;

/**
 * @brief		Routine to fill the buffer to make a flip.
 *
 * @param[inout]		pResourceInfo Pointer to structue @ref RESOURCE_INFO to get resource info
 * @param[in]		lWidth Width of the plane
 * @param[in]		lHeight Height of the plane
 * @param[in]		PixelFormat Pixel Format of the plane
 * @param[in]		eTileFormat Tile Format of the plane
 * @param[in]		uiLayerIndex Layer index of the plane
 * @param[in]		pPath Path to the dump file
 * @return			Returns 1(True) on creating the resource; else 0(False)
 */
VOID DFTCreateBufferContent(PPYPLANES_RESOURCE_INFO pResourceInfo, LONG lWidth, LONG lHeight, GVSTUB_PIXELFORMAT PixelFormat, GVSTUB_SURFACE_MEMORY_TYPE TileFormat,
                            UINT uiLayerIndex, CHAR *pPath, BOOL IsAsyncFlip)
{
    UCHAR *ucUserVirtualAddressTemp;
    ucUserVirtualAddressTemp = (UCHAR *)pResourceInfo->pUserVirtualAddress;
    if (pPath == NULL)
    {
        int        COLORS[5]     = { 0 };
        int        COLORS1[5]    = { 0 };
        static int color_counter = 0;

        int async_flip_colors[3][5] = {
            0x083D77FF, 0xEBEB3DFF, 0xF4D35EFF, 0xEE964BFF, 0xF95738FF, 0xFF6796D9, 0x32FF9FD9, 0x75E522E3,
            0xb948ACED, 0xC78F2EEE, 0x2D39003C, 0x0622003C, 0x882B003C, 0x8736003C, 0x6636003C,
        };

        int    flagPlanar = 0;
        int    flag64BPP  = 0;
        UINT64 UVbytepos  = 0;
        UINT   stride     = 0;

        srand((UINT)time(NULL));
        int    ColorPick        = uiLayerIndex;
        UCHAR *ucVirtualAddress = (UCHAR *)pResourceInfo->pUserVirtualAddress;

        INFO_LOG("Resource size : %d \t Pitch: %d", (int)pResourceInfo->u64SurfaceSize, pResourceInfo->ulPitch);

        if (TileFormat == GVSTUB_SURFACE_MEMORY_LINEAR)
            stride = pResourceInfo->ulPitch * 64;
        else if (TileFormat == GVSTUB_SURFACE_MEMORY_X_TILED)
            stride = pResourceInfo->ulPitch * 512;
        else if (TileFormat == GVSTUB_SURFACE_MEMORY_Y_LEGACY_TILED)
            stride = pResourceInfo->ulPitch * 128;

        INFO_LOG("Stride: %d", stride);

        if (TRUE == IsAsyncFlip)
        {
            // Assign a seperate color for each new flip on each layer
            if (PixelFormat == GVSTUB_PIXEL_FORMAT_B8G8R8X8 || PixelFormat == GVSTUB_PIXEL_FORMAT_B8G8R8A8 || PixelFormat == GVSTUB_PIXEL_FORMAT_R8G8B8X8 ||
                PixelFormat == GVSTUB_PIXEL_FORMAT_R8G8B8A8)
            {
                COLORS[0] = async_flip_colors[0][color_counter];
                COLORS[1] = async_flip_colors[1][color_counter];
                COLORS[2] = async_flip_colors[2][color_counter];
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_R10G10B10X2 || PixelFormat == GVSTUB_PIXEL_FORMAT_R10G10B10A2 || PixelFormat == GVSTUB_PIXEL_FORMAT_B10G10R10X2 ||
                     PixelFormat == GVSTUB_PIXEL_FORMAT_B10G10R10A2)
            {
                COLORS[0] = async_flip_colors[0][color_counter];
                COLORS[1] = async_flip_colors[1][color_counter];
                COLORS[2] = async_flip_colors[2][color_counter];
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_R16G16B16X16F || PixelFormat == GVSTUB_PIXEL_FORMAT_R16G16B16A16F)
            {
                flag64BPP = 1;

                COLORS[0] = async_flip_colors[0][color_counter];
                COLORS[1] = async_flip_colors[1][color_counter];
                COLORS[2] = async_flip_colors[2][color_counter];
            }
            color_counter++;
            color_counter = color_counter % 5;
        }
        else
        {
            // Use the old flow of Colors assignmnet per layer if the flip is Sync
            if (PixelFormat == GVSTUB_PIXEL_FORMAT_B8G8R8X8 || PixelFormat == GVSTUB_PIXEL_FORMAT_B8G8R8A8 || PixelFormat == GVSTUB_PIXEL_FORMAT_R8G8B8X8 ||
                PixelFormat == GVSTUB_PIXEL_FORMAT_R8G8B8A8)
            {
                COLORS[0] = 0xFF0000FF;
                COLORS[1] = 0x00FF00FF;
                COLORS[2] = 0x0000FFFF;
                COLORS[3] = 0xFFFF00FF;
                COLORS[4] = 0xFF00FFFF;
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_R10G10B10X2 || PixelFormat == GVSTUB_PIXEL_FORMAT_R10G10B10A2 || PixelFormat == GVSTUB_PIXEL_FORMAT_B10G10R10X2 ||
                     PixelFormat == GVSTUB_PIXEL_FORMAT_B10G10R10A2)
            {
                COLORS[0] = 0x0000C0FF;
                COLORS[1] = 0x00F03F00;
                COLORS[2] = 0xFC0F0000;
                COLORS[3] = 0x00F0FFFF;
                COLORS[4] = 0xFC0FC0FF;
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_R16G16B16X16F || PixelFormat == GVSTUB_PIXEL_FORMAT_R16G16B16A16F)
            {
                flag64BPP = 1;

                COLORS[0] = 0x3C00003C;
                COLORS[1] = 0x003C003C;
                COLORS[2] = 0x00003C3C;
                COLORS[3] = 0x3C3C003C;
                COLORS[4] = 0x3C003C3C;
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_YUV422)
            {
                COLORS[0] = 0x29F0296E;
                COLORS[1] = 0x91369136;
                COLORS[2] = 0x525A52F0;
                COLORS[3] = 0xAAA6AA10;
                COLORS[4] = 0x68CA68DE;
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_YUV444_8)
            {
                COLORS[0] = 0x6EF02900;
                COLORS[1] = 0x36369100;
                COLORS[2] = 0xF05A5200;
                COLORS[3] = 0x10A6AA00;
                COLORS[4] = 0xDECA6800;
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_NV12YUV420)
            {
                flagPlanar = 1;
                COLORS[2]  = 0x52;
                COLORS[1]  = 0x91;
                COLORS[0]  = 0x29;
                COLORS[3]  = 0xAA;
                COLORS[4]  = 0x68;
                COLORS1[2] = 0x5AF0;
                COLORS1[1] = 0x3636;
                COLORS1[0] = 0xF06E;
                COLORS1[3] = 0xA610;
                COLORS1[4] = 0xCADE;
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_YUV444_10)
            {
                COLORS[0] = 0xC093821B;
                COLORS[1] = 0xD810890D;
                COLORS[2] = 0x6821053C;
                COLORS[3] = 0x98A20A04;
                COLORS[4] = 0xCAACE10D;
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_YUV422_10 || PixelFormat == GVSTUB_PIXEL_FORMAT_YUV422_12 || PixelFormat == GVSTUB_PIXEL_FORMAT_YUV422_16)
            {
                flag64BPP = 1;

                COLORS[0]  = 0x2900F000;
                COLORS[1]  = 0x91003600;
                COLORS[2]  = 0x52005A00;
                COLORS[3]  = 0xAA00A600;
                COLORS1[4] = 0x6B00CA00;

                COLORS1[0] = 0x29006E00;
                COLORS1[1] = 0x91003600;
                COLORS1[2] = 0x5200F000;
                COLORS1[3] = 0xAA001000;
                COLORS1[4] = 0x6B00DE00;
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_P010YUV420 || PixelFormat == GVSTUB_PIXEL_FORMAT_P012YUV420 || PixelFormat == GVSTUB_PIXEL_FORMAT_P016YUV420)
            {
                flagPlanar = 1;
                flag64BPP  = 1;
                COLORS[2]  = 0x0052;
                COLORS[1]  = 0x0091;
                COLORS[0]  = 0x0029;
                COLORS[3]  = 0x00AA;
                COLORS[4]  = 0x006B;
                COLORS1[2] = 0x005A00F0;
                COLORS1[1] = 0x00360036;
                COLORS1[0] = 0x00F0006E;
                COLORS1[3] = 0x00A60010;
                COLORS1[4] = 0x00CA00DE;
            }
            else if (PixelFormat == GVSTUB_PIXEL_FORMAT_YUV444_12 || PixelFormat == GVSTUB_PIXEL_FORMAT_YUV444_16)
            {
                flag64BPP = 1;

                COLORS[0] = 0xF0002900;
                COLORS[1] = 0x36009100;
                COLORS[2] = 0x5A005200;
                COLORS[3] = 0xA600AA00;
                COLORS[4] = 0xCA006B00;

                COLORS1[0] = 0x6E000000;
                COLORS1[1] = 0x36000000;
                COLORS1[2] = 0xF0000000;
                COLORS1[3] = 0x10000000;
                COLORS1[4] = 0xDE000000;
            }
        }

        if (flag64BPP == 0 && flagPlanar == 0)
        {
            for (UINT64 bytepos = 0; (bytepos + 3) < pResourceInfo->u64SurfaceSize; bytepos += 4)
            {
                ucVirtualAddress[bytepos]     = (byte)(COLORS[ColorPick] >> 24);
                ucVirtualAddress[bytepos + 1] = (byte)(COLORS[ColorPick] >> 16);
                ucVirtualAddress[bytepos + 2] = (byte)(COLORS[ColorPick] >> 8);
                ucVirtualAddress[bytepos + 3] = (byte)COLORS[ColorPick];
            }
        }
        else if (flag64BPP == 1 && flagPlanar == 0)
        {
            for (UINT64 bytepos = 0; (bytepos + 7) < pResourceInfo->u64SurfaceSize; bytepos += 8)
            {

                ucVirtualAddress[bytepos]     = (byte)(COLORS[ColorPick] >> 16);
                ucVirtualAddress[bytepos + 1] = (byte)(COLORS[ColorPick] >> 24);
                ucVirtualAddress[bytepos + 2] = (byte)(COLORS[ColorPick]);
                ucVirtualAddress[bytepos + 3] = (byte)(COLORS[ColorPick] >> 8);
                ucVirtualAddress[bytepos + 4] = (byte)(COLORS1[ColorPick] >> 16);
                ucVirtualAddress[bytepos + 5] = (byte)(COLORS1[ColorPick] >> 24);
                ucVirtualAddress[bytepos + 6] = (byte)(COLORS1[ColorPick]);
                ucVirtualAddress[bytepos + 7] = (byte)(COLORS1[ColorPick] >> 8);
            }
        }
        else if (flag64BPP == 0 && flagPlanar == 1)
        {

            // Added a workaround to handle the exception seen due to incorrect pitch value returned from GMM.
            for (UINT64 bytepos = 0; bytepos < (stride * lHeight) && bytepos < pResourceInfo->u64SurfaceSize; bytepos++)
            {
                ucVirtualAddress[bytepos] = (byte)(COLORS[ColorPick]);
                UVbytepos                 = bytepos;
            }
            if ((UVbytepos + 1) == pResourceInfo->u64SurfaceSize)
            {
                INFO_LOG("UV content is not filled");
            }
            INFO_LOG("UV BytePosition %d SUrface Size : %d", (int)UVbytepos, (int)pResourceInfo->u64SurfaceSize);
            for (UINT64 bytepos = UVbytepos + 1; (bytepos + 1) < pResourceInfo->u64SurfaceSize; bytepos += 2)
            {
                ucVirtualAddress[bytepos]     = (byte)(COLORS1[ColorPick] >> 8);
                ucVirtualAddress[bytepos + 1] = (byte)COLORS1[ColorPick];
            }
        }
        else if (flag64BPP == 1 && flagPlanar == 1)
        {
            // int max = stride * lHeight * 2;
            int max = lWidth * lHeight * 2;

            for (UINT64 bytepos = 0; (bytepos + 1) < max; bytepos += 2)
            {
                ucVirtualAddress[bytepos]     = (byte)(COLORS[ColorPick] >> 8);
                ucVirtualAddress[bytepos + 1] = (byte)(COLORS[ColorPick]);
                UVbytepos                     = bytepos;
            }

            for (UINT64 bytepos = UVbytepos + 2; (bytepos + 3) < pResourceInfo->u64SurfaceSize; bytepos += 4)
            {
                ucVirtualAddress[bytepos]     = (byte)(COLORS1[ColorPick] >> 24);
                ucVirtualAddress[bytepos + 1] = (byte)(COLORS1[ColorPick] >> 16);
                ucVirtualAddress[bytepos + 2] = (byte)(COLORS1[ColorPick] >> 8);
                ucVirtualAddress[bytepos + 3] = (byte)COLORS1[ColorPick];
            }
        }
    }
    else
    {
        FILE *fp = NULL;
        fopen_s(&fp, pPath, "rb");
        if (fp != NULL)
        {
            fread_s(ucUserVirtualAddressTemp, pResourceInfo->u64SurfaceSize, 1, pResourceInfo->u64SurfaceSize, fp);
            fclose(fp);
        }
    }
}

BOOL DDRW_DFTCreateResource(PGFX_ADAPTER_INFO pAdapterInfo, PPYPLANES_RESOURCE_INFO pResourceInfo, LONG lWidth, LONG lHeight, INT PixelFormat, INT TileFormat, UINT uiLayerIndex,
                            CHAR *pPath, BOOL IsAsyncFlips)
{
    BOOL                   bStatus = FALSE;
    MPO_DATA               MpoData;
    GVSTUB_CREATE_RES_ARGS stCreateResource = { 0 };
    DWORD                  dwBytesReturned  = 0;
    GFX_ADAPTER_INFO       adapterInfo      = { 0 };

    stCreateResource.bAuxSurf       = FALSE;
    stCreateResource.ulBaseHeight   = lHeight;
    stCreateResource.ulBaseWidth    = lWidth;
    stCreateResource.eFormat        = PixelFormat;
    stCreateResource.Info.ulLinear  = (TileFormat == GVSTUB_SURFACE_MEMORY_LINEAR) ? 1 : 0;
    stCreateResource.Info.ulTiledW  = /*(TileFormat == DIVA_SURFACE_TILEFORMAT_W) ? 1 :*/ 0;
    stCreateResource.Info.ulTiledX  = (TileFormat == GVSTUB_SURFACE_MEMORY_X_TILED) ? 1 : 0;
    stCreateResource.Info.ulTiledY  = (TileFormat == GVSTUB_SURFACE_MEMORY_Y_LEGACY_TILED) ? 1 : 0;
    stCreateResource.Info.ulTiledYf = (TileFormat == GVSTUB_SURFACE_MEMORY_Y_F_TILED) ? 1 : 0;
    stCreateResource.Info.ulTiledYs = /*(TileFormat == DIVA_SURFACE_TILEFORMAT_Ys) ? 1 :*/ 0;
    stCreateResource.Info.ulTiled4  = (TileFormat == GVSTUB_SURFACE_MEMORY_TILE4) ? 1 : 0;

    MpoData.eMPOEvent = CREATE_RESOURCE;
    MpoData.pMPOArgs  = calloc(1, sizeof(GVSTUB_CREATE_RES_ARGS));
    memcpy_s(MpoData.pMPOArgs, sizeof(GVSTUB_CREATE_RES_ARGS), &stCreateResource, sizeof(GVSTUB_CREATE_RES_ARGS));
    MpoData.ulArgSize = sizeof(GVSTUB_CREATE_RES_ARGS);
    
    bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), &MpoData, sizeof(MPO_DATA));
    
    memcpy_s(&stCreateResource, sizeof(GVSTUB_CREATE_RES_ARGS), MpoData.pMPOArgs, sizeof(GVSTUB_CREATE_RES_ARGS));
    free(MpoData.pMPOArgs);

    if (bStatus == FALSE)
    {
        ERROR_LOG("IOCTL failed in create resource: %d", bStatus);
        return FALSE;
    }

    pResourceInfo->pGmmBlock           = stCreateResource.pGmmBlock;
    pResourceInfo->pUserVirtualAddress = stCreateResource.pUserVirtualAddress;
    pResourceInfo->u64SurfaceSize      = stCreateResource.u64SurfaceSize;
    pResourceInfo->ulPitch             = stCreateResource.ulPitch;
    INFO_LOG("Create Resource: %lld", pResourceInfo->pGmmBlock);
    _flushall();

    if (pResourceInfo->pGmmBlock == 0)
        return FALSE;

    create_resource++;
    DFTCreateBufferContent(pResourceInfo, lWidth, lHeight, PixelFormat, TileFormat, uiLayerIndex, pPath, IsAsyncFlips);

    return bStatus;
}

BOOL DDRW_DFTFreeResource(PGFX_ADAPTER_INFO pAdapterInfo, PPYPLANES_RESOURCE_INFO pResourceInfo)
{
    BOOL                        bStatus = FALSE;
    MPO_DATA                    MpoData;
    GVSTUB_FREE_RES_ARGS_YANGRA stFreeResource  = { 0 };
    GFX_ADAPTER_INFO            adapterInfo     = { 0 };
    DWORD                       dwBytesReturned = 0;

    INFO_LOG("Free Resource: %lld", pResourceInfo->pGmmBlock);
    stFreeResource.pGmmBlock           = pResourceInfo->pGmmBlock;
    stFreeResource.pUserVirtualAddress = pResourceInfo->pUserVirtualAddress;

    MpoData.eMPOEvent = FREE_RESOURCE;
    MpoData.pMPOArgs  = calloc(1, sizeof(GVSTUB_FREE_RES_ARGS_YANGRA));
    memcpy_s(MpoData.pMPOArgs, sizeof(GVSTUB_FREE_RES_ARGS_YANGRA), &stFreeResource, sizeof(GVSTUB_FREE_RES_ARGS_YANGRA));
    MpoData.ulArgSize = sizeof(GVSTUB_FREE_RES_ARGS_YANGRA);

    bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), &MpoData, sizeof(MPO_DATA));

    memcpy_s(&stFreeResource, sizeof(GVSTUB_FREE_RES_ARGS_YANGRA), MpoData.pMPOArgs, sizeof(GVSTUB_FREE_RES_ARGS_YANGRA));
    free(MpoData.pMPOArgs);

    if (bStatus == FALSE)
    {
        ERROR_LOG("IOCTL failed in Free Resource: %d", bStatus);
        return FALSE;
    }

    pResourceInfo->pGmmBlock           = 0;
    pResourceInfo->pUserVirtualAddress = 0;
    pResourceInfo->u64SurfaceSize      = 0;
    pResourceInfo->ulPitch             = 0;
    free_resource++;

    return TRUE;
}

/**
 * @brief			To create the resource for a particular plane.
 *
 * @param[inout]		pResourceInfo Pointer to structue @ref RESOURCE_INFO to get resource info
 * @param[in]		lWidth Width of the plane
 * @param[in]		lHeight Height of the plane
 * @param[in]		PixelFormat Pixel Format of the plane
 * @param[in]		eTileFormat Tile Format of the plane
 * @param[in]		uiLayerIndex Layer index of the plane
 * @param[in]		pPath Path to the dump file
 * @return			Returns 1(True) on creating the resource; else 0(False)
 */
BOOL mainline_DFTCreateResource(PGFX_ADAPTER_INFO pAdapterInfo, PPYPLANES_RESOURCE_INFO pResourceInfo, LONG lWidth, LONG lHeight, SIMDRIVER_PIXELFORMAT PixelFormat,
                                SIMDRIVER_SURFACE_MEMORY_TYPE TileFormat, UINT uiLayerIndex, CHAR *pPath)
{
    BOOL                           bStatus         = FALSE;
    DWORD                          dwBytesReturned = 0;
    SIMDRIVER_DISPLAY_FEATURE_ARGS stDisplayFeatureArgs;
    SIMDRIVER_CREATE_RES_ARGS      stCreateResource = { 0 };
    GFX_ADAPTER_INFO               adapterInfo      = { 0 };

    stCreateResource.bAuxSurf       = FALSE;
    stCreateResource.ulBaseHeight   = lHeight;
    stCreateResource.ulBaseWidth    = lWidth;
    stCreateResource.eFormat        = PixelFormat;
    stCreateResource.Info.ulLinear  = (TileFormat == SIMDRIVER_SURFACE_MEMORY_LINEAR) ? 1 : 0;
    stCreateResource.Info.ulTiledW  = /*(TileFormat == DIVA_SURFACE_TILEFORMAT_W) ? 1 :*/ 0;
    stCreateResource.Info.ulTiledX  = (TileFormat == SIMDRIVER_SURFACE_MEMORY_X_TILED) ? 1 : 0;
    stCreateResource.Info.ulTiledY  = (TileFormat == SIMDRIVER_SURFACE_MEMORY_Y_LEGACY_TILED) ? 1 : 0;
    stCreateResource.Info.ulTiledYf = (TileFormat == SIMDRIVER_SURFACE_MEMORY_Y_F_TILED) ? 1 : 0;
    stCreateResource.Info.ulTiledYs = /*(TileFormat == DIVA_SURFACE_TILEFORMAT_Ys) ? 1 :*/ 0;

    stDisplayFeatureArgs.ulSize       = sizeof(SIMDRIVER_CREATE_RES_ARGS);
    stDisplayFeatureArgs.eServiceType = SIMDRIVER_CREATE_RESOURCE;
    stDisplayFeatureArgs.pMpoArgs     = calloc(1, sizeof(SIMDRIVER_CREATE_RES_ARGS));
    memcpy_s(stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_CREATE_RES_ARGS), &stCreateResource, sizeof(SIMDRIVER_CREATE_RES_ARGS));

    bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), &stDisplayFeatureArgs, sizeof(SIMDRIVER_DISPLAY_FEATURE_ARGS));

    memcpy_s(&stCreateResource, sizeof(SIMDRIVER_CREATE_RES_ARGS), stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_CREATE_RES_ARGS));
    free(stDisplayFeatureArgs.pMpoArgs);

    if (bStatus == FALSE)
    {
        ERROR_LOG("IOCTL failed in create resource: %d", bStatus);
        return FALSE;
    }

    pResourceInfo->pGmmBlock           = stCreateResource.pGmmBlock;
    pResourceInfo->pUserVirtualAddress = stCreateResource.pUserVirtualAddress;
    pResourceInfo->u64SurfaceSize      = stCreateResource.u64SurfaceSize;
    pResourceInfo->ulPitch             = stCreateResource.ulPitch;

    if (pResourceInfo->pGmmBlock == 0)
        return FALSE;

    create_resource++;
    DFTCreateBufferContent(pResourceInfo, lWidth, lHeight, PixelFormat, TileFormat, uiLayerIndex, pPath,
                           FALSE); // IsAsyncFlip = FALSE as there is no Async flip implementation for Legacy DFT flips

    return bStatus;
}

/**
 * @brief		To free the resource of particular plane.
 *
 * @param[in]	pResourceInfo Pointer to structure @ref RESOURCE_INFO to free the resource of a particular plane
 * @return		Returns 1(True) on freeing the resource; else 0(False)
 */
BOOL mainline_DFTFreeResource(PGFX_ADAPTER_INFO pAdapterInfo, PPYPLANES_RESOURCE_INFO pResourceInfo)
{
    BOOL                           bStatus         = FALSE;
    DWORD                          dwBytesReturned = 0;
    SIMDRIVER_DISPLAY_FEATURE_ARGS stDisplayFeatureArgs;
    SIMDRIVER_FREE_RES_ARGS        stFreeResource = { 0 };
    GFX_ADAPTER_INFO               adapterInfo    = { 0 };

    stFreeResource.pGmmBlock = pResourceInfo->pGmmBlock;
    INFO_LOG("Free Resource %llu", pResourceInfo->pGmmBlock);

    stDisplayFeatureArgs.ulSize       = sizeof(SIMDRIVER_FREE_RES_ARGS);
    stDisplayFeatureArgs.eServiceType = SIMDRIVER_FREE_RESOURCE;
    stDisplayFeatureArgs.pMpoArgs     = calloc(1, sizeof(SIMDRIVER_FREE_RES_ARGS));
    memcpy_s(stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_FREE_RES_ARGS), &stFreeResource, sizeof(SIMDRIVER_FREE_RES_ARGS));

    bStatus = ValSim_DeviceIoControl(pAdapterInfo, sizeof(GFX_ADAPTER_INFO), &stDisplayFeatureArgs, sizeof(SIMDRIVER_DISPLAY_FEATURE_ARGS));

    memcpy_s(&stFreeResource, sizeof(SIMDRIVER_FREE_RES_ARGS), stDisplayFeatureArgs.pMpoArgs, sizeof(SIMDRIVER_FREE_RES_ARGS));
    free(stDisplayFeatureArgs.pMpoArgs);

    if (bStatus == FALSE)
    {
        ERROR_LOG("IOCTL failed in Free Resource: %d", bStatus);
        return FALSE;
    }

    pResourceInfo->pGmmBlock           = 0;
    pResourceInfo->pUserVirtualAddress = 0;
    pResourceInfo->u64SurfaceSize      = 0;
    pResourceInfo->ulPitch             = 0;
    free_resource++;

    return bStatus;
}

BOOL FlipQDFTCreateResource(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes)
{
    
    BOOL bStatus = FALSE;
    UINT ulPlaneindex = 0;

    for (ulPlaneindex = 0; ulPlaneindex < pPlanes->uiPlaneCount; ulPlaneindex++)
    {
        //No front and back buffers required as buffers are queued. Using a single instance per plane.
        bStatus = DDRW_DFTCreateResource(pAdapterInfo, &pPlanes->stPlaneInfo[ulPlaneindex].stResourceInfo[pPlanes->stPlaneInfo[ulPlaneindex].iResourceInUse],
                                         pPlanes->stPlaneInfo[ulPlaneindex].lWidth,
                               pPlanes->stPlaneInfo[ulPlaneindex].lHeight,
                               pPlanes->stPlaneInfo[ulPlaneindex].ePixelFormat, pPlanes->stPlaneInfo[ulPlaneindex].eSurfaceMemType, pPlanes->stPlaneInfo[ulPlaneindex].uiLayerIndex,
                               pPlanes->stPlaneInfo[ulPlaneindex].cpDumpFilePath, FALSE);
    }

    return bStatus;
    
}
