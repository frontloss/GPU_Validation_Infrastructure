/**
 * @file
 * @section WritebackUtility_c
 * @brief Internal source file which contains implementation for WB and related functionalities
 * like plugging, unplugging WB devices, dumping buffer etc..,
 *
 * @ref		WritebackUtility.c
 * @author	Reeju Srivastava, Ankurkumar Patel
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
#pragma warning(disable : 4996)

/* Local header(s)*/
#include "WritebackUtility.h"
#include "WritebackUtilityDetails.h"
#include "CommonLogger.h"

/**
 * @brief		Function to log information if Module is in debug mode
 * @param[in]    Message to print in text file
 * @return       VOID
 */
VOID Logger(LOG_LEVEL level, _In_ CONST PCHAR logMsgFormat, ...)
{
    va_list logArgs = NULL;                 // Variable argument list
    char    logOutput[MAX_LOG_BUFFER_SIZE]; // log buffer which contains expanded format string of variable args
    va_start(logArgs, logMsgFormat);        // Retreive the variable arguments
    vsprintf(logOutput, logMsgFormat, logArgs);
    /* Formation of formatted string*/
    CommonLogger(DLL_NAME, level, __FUNCTION__, __LINE__, logOutput);
}

CDLL_EXPORT BOOLEAN PlugWBDevice(WB_MODE *mode, WB_DEVICE_INFO *deviceInfo)
{
    HRESULT              retVal              = S_OK;
    DD_ESC_WRITEBACK_HPD wbHPDArgs           = { 0 };
    UINT32               sizeofEscDataStruct = (UINT32)sizeof(wbHPDArgs);

    /* set escape code and escape version*/
    ESCAPE_OPCODES escapeVerOpcodes;
    escapeVerOpcodes.MajorEscapeCode       = GFX_ESCAPE_CUICOM_CONTROL;
    escapeVerOpcodes.MinorEscapeCode       = DD_ESC_WRITEBACK_ENABLE_DISABLE;
    escapeVerOpcodes.MinorInterfaceVersion = MinorEscVersion;
    escapeVerOpcodes.MajorInterfaceVersion = MajorEscVersion;

    /* Set the request details and WB display Id*/
    wbHPDArgs.HotPlug       = PLUG_WB;
    wbHPDArgs.Resolution.Cx = mode->Cx;
    wbHPDArgs.Resolution.Cy = mode->Cy;
    wbHPDArgs.OverrideDefaultEdid = FALSE;

    /* Make escape call to plug writeback device*/
    retVal = GetDetails(sizeofEscDataStruct, &wbHPDArgs, escapeVerOpcodes);
    if (retVal != S_OK)
    {
        Logger(ERROR_LOGS, "Escape call to plug writeback device failed\n");
        return FALSE;
    }
    else
    {
        /* Fill writeback device info details in specified structure*/
        deviceInfo->error       = retVal;
        deviceInfo->DeviceId    = wbHPDArgs.DeviceId;
        deviceInfo->HResolution = wbHPDArgs.Resolution.Cx;
        deviceInfo->VResolution = wbHPDArgs.Resolution.Cy;
        Logger(DEBUG_LOGS, "Escape call to plug writeback device passed\n");
        return TRUE;
    }
}

CDLL_EXPORT BOOLEAN UnplugWBDevice(ULONG deviceId)
{
    HRESULT              retVal              = S_OK;
    DD_ESC_WRITEBACK_HPD wbHPDArgs           = { 0 };
    UINT32               sizeofEscDataStruct = (UINT32)sizeof(wbHPDArgs);

    /* set escape code and escape version*/
    ESCAPE_OPCODES escapeVerOpcodes;
    escapeVerOpcodes.MajorEscapeCode       = GFX_ESCAPE_CUICOM_CONTROL;
    escapeVerOpcodes.MinorEscapeCode       = DD_ESC_WRITEBACK_ENABLE_DISABLE;
    escapeVerOpcodes.MinorInterfaceVersion = MinorEscVersion;
    escapeVerOpcodes.MajorInterfaceVersion = MajorEscVersion;

    /* Set the request details and WB display Id*/
    wbHPDArgs.HotPlug  = UNPLUG_WB;
    wbHPDArgs.DeviceId = deviceId;
    wbHPDArgs.OverrideDefaultEdid = FALSE;

    /* Make escape call to unplug writeback device*/
    retVal = GetDetails(sizeofEscDataStruct, &wbHPDArgs, escapeVerOpcodes);

    if (retVal != S_OK)
    {
        Logger(ERROR_LOGS, "Escape call to unplug writeback device with target ID %lu failed\n", deviceId);
        return FALSE;
    }
    else
    {
        Logger(DEBUG_LOGS, "Escape call to unplug writeback device with target ID %lu passed\n", deviceId);
        return TRUE;
    }
}

CDLL_EXPORT BOOLEAN IsWBFeatureEnabled(HRESULT *pErrorCode)
{
    HRESULT                 retVal              = S_OK;
    DD_WRITEBACK_QUERY_ARGS wbQuery             = { 0 };
    UINT32                  sizeofEscDataStruct = (UINT32)sizeof(wbQuery);

    /* set escape code and escape version*/
    ESCAPE_OPCODES escapeVerOpcodes;
    escapeVerOpcodes.MajorEscapeCode       = GFX_ESCAPE_CUICOM_CONTROL;
    escapeVerOpcodes.MinorEscapeCode       = DD_ESC_WRITEBACK_QUERY;
    escapeVerOpcodes.MinorInterfaceVersion = MinorEscVersion;
    escapeVerOpcodes.MajorInterfaceVersion = MajorEscVersion;

    /* Make escape call to check writeback feature status*/
    retVal      = GetDetails(sizeofEscDataStruct, &wbQuery, escapeVerOpcodes);
    *pErrorCode = retVal;

    if (S_OK == retVal)
    {
        Logger(ERROR_LOGS, "Escape call to IsWBFeatureEnabled passed\n");
        return wbQuery.IsWbFeatureEnabled;
    }
    else
    {
        Logger(ERROR_LOGS, "Escape call to IsWBFeatureEnabled failed\n");
        return FALSE;
    }
}

CDLL_EXPORT BOOLEAN DumpWBBuffer(ULONG deviceId, UINT count, UINT delayInSeconds)
{
    HRESULT                              retVal          = S_OK;
    DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS wbCapBufferArgs = { 0 };
    void *                               p               = NULL;
    UINT                                 deviceNumber    = (deviceId >> 8) & 1; // to identify the WB device and save the dump in binary file accordingly

    /* set escape code and escape version*/
    ESCAPE_OPCODES escapeVerOpcodes;
    escapeVerOpcodes.MajorEscapeCode       = GFX_ESCAPE_CUICOM_CONTROL;
    escapeVerOpcodes.MinorEscapeCode       = DD_ESC_WRITEBACK_CAPTURE_BUFFER;
    escapeVerOpcodes.MinorInterfaceVersion = MinorEscVersion;
    escapeVerOpcodes.MajorInterfaceVersion = MajorEscVersion;

    for (UINT frameCounter = 0; frameCounter < count; frameCounter++)
    {
        /* Initialize name of the file to be dumped*/
        char fileName[FILE_SIZE] = "";

        /* Make escape call to get buffer size details*/
        wbCapBufferArgs.BufferSize = 0;
        wbCapBufferArgs.DeviceId   = deviceId;
        retVal                     = GetDetails(sizeof(wbCapBufferArgs), &wbCapBufferArgs, escapeVerOpcodes);
        if (retVal != S_OK || (wbCapBufferArgs.BufferSize == 0))
        {
            Logger(ERROR_LOGS, "Escape call to get buffersize failed or has returned buffersize as 0 \n");
            return FALSE;
        }

        /* Allocate memmory to a buffer to be passed to escape to get buffer capture data*/
        p = malloc((sizeof(DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS) + wbCapBufferArgs.BufferSize));
        if (p == NULL)
        {
            Logger(ERROR_LOGS, "Memory allocation failed for wb capture buffer args \n");
            return FALSE;
        }
        DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS *pWbEscArgs = (DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS *)p;

        /* set target ID and buffersize to be passed to escape to get buffer capture data*/
        pWbEscArgs->DeviceId   = deviceId;
        pWbEscArgs->BufferSize = wbCapBufferArgs.BufferSize;

        /* Make Escape call to get buffer capture data*/
        retVal = GetDetails((sizeof(DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS) + wbCapBufferArgs.BufferSize), pWbEscArgs, escapeVerOpcodes);
        if (retVal != S_OK)
        {
            free(p);
            Logger(ERROR_LOGS, "Escape call to get bufferdump failed \n");
            return FALSE;
        }

        /* Generate filename for particular dump*/
        snprintf(fileName, sizeof(fileName), "WB_%d_%d_%dx%d_WBBufferOutput.", deviceNumber, frameCounter, pWbEscArgs->Resolution.Cx, pWbEscArgs->Resolution.Cy);

        /* Add format details as file extention*/
        switch (pWbEscArgs->PixelFormat)
        {
        case DD_CUI_ESC_8BPP_INDEXED:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "8BPP_INDEXED");
            break;
        case DD_CUI_ESC_B5G6R5X0:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "B5G6R5X0");
            break;
        case DD_CUI_ESC_B8G8R8X8:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "B8G8R8X8");
            break;
        case DD_CUI_ESC_R8G8B8X8:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "R8G8B8X8");
            break;
        case DD_CUI_ESC_B10G10R10X2:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "B10G10R10X2");
            break;
        case DD_CUI_ESC_R10G10B10X2:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "R10G10B10X2");
            break;
        case DD_CUI_ESC_R10G10B10X2_XR_BIAS:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "R10G10B10X2_XR_BIAS");
            break;
        case DD_CUI_ESC_R16G16B16X16F:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "R16G16B16X16F");
            break;
        case DD_CUI_ESC_YUV422_8:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "YUV444_8");
            break;
        case DD_CUI_ESC_YUV422_10:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "YUV444_10");
            break;
        case DD_CUI_ESC_YUV422_12:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "YUV422_12");
            break;
        case DD_CUI_ESC_YUV422_16:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "YUV422_16");
            break;
        case DD_CUI_ESC_YUV444_8:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "YUV422_16");
            break;
        case DD_CUI_ESC_YUV444_10:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "YUV444_10");
            break;
        case DD_CUI_ESC_YUV444_12:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "YUV444_12");
            break;
        case DD_CUI_ESC_YUV444_16:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "YUV444_16");
            break;
        case DD_CUI_ESC_NV12YUV420:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "NV12YUV420");
            break;
        case DD_CUI_ESC_P010YUV420:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "P010YUV420");
            break;
        case DD_CUI_ESC_P012YUV420:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "P012YUV420");
            break;
        case DD_CUI_ESC_P016YUV420:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "P016YUV420");
            break;
        default:
            snprintf(fileName + strlen(fileName), FILE_SIZE - strlen(fileName), "%s", "MAX_PIXELFORMAT");
            break;
        }

        /* Copy buffer data from ecape buffer to temporary buffer*/
        DDU8 *tempBuffer = (DDU8 *)malloc(pWbEscArgs->BufferSize);
        memcpy(tempBuffer, pWbEscArgs->WdBuffer, pWbEscArgs->BufferSize);

        /* Dump memory data from temporary buffer to the file*/
        FILE *pFileDump = fopen(fileName, "wb");
        for (ULONG index = 0; index < pWbEscArgs->BufferSize; index++)
            fwrite((tempBuffer + index), 1, 1, pFileDump);
        fclose(pFileDump);

        /* Free dynamically allocated buffers*/
        free(tempBuffer);
        free(p);

        Logger(DEBUG_LOGS, "Escape call to get bufferdump passed and created bufferdump with name %s \n", fileName);
        Logger(DEBUG_LOGS, "Frame %d, Waiting for %d seconds before dumping next buffer\n", count, delayInSeconds);

        /* Wait for specified seconds before going to dump next buffer*/
        Sleep(delayInSeconds * 1000);
    }
    return TRUE;
}

HRESULT GetDetails(INT size, void *pEscapeData, ESCAPE_OPCODES escapeOpCodeReq)
{
    HRESULT hResult = E_FAIL;

    /*Initailise and get the OS escape handles*/
    HMODULE                      hGdi32          = NULL;
    PFND3DKMT_OPENADAPTERFROMHDC pfnOpenAdapter  = NULL;
    PFND3DKMT_ESCAPE             pfnD3DKmtEscape = NULL;
    PFND3DKMT_CLOSEADAPTER       pfnCloseAdapter = NULL;

    GFX_ESCAPE_HEADER_T_T      pHeader      = { 0 };
    D3DKMT_ESCAPE              kmtEscape    = { 0 };
    D3DKMT_OPENADAPTERFROMHDC *pOpenAdapter = NULL;
    D3DKMT_CLOSEADAPTER        closeAdapter = { 0 };

    /* Initailize variables*/
    PVOID          pLocal = NULL;
    HANDLE         hLocal = NULL;
    DISPLAY_DEVICE deviceName;
    UINT16         devID           = 0;
    UINT32         sizeofEscHeader = 0;
    HDC            hdc             = NULL;

    deviceName.cb = sizeof(DISPLAY_DEVICE);
    do
    {
        /* Load gdi32 library and proccess address for D3D KMT functions*/
        hGdi32 = LoadLibraryEx(GDI32_LIB, NULL, LOAD_LIBRARY_SEARCH_SYSTEM32);
        if (NULL == hGdi32)
            break;
        /* Get process handles to operate on for escape call*/
        pfnOpenAdapter = (PFND3DKMT_OPENADAPTERFROMHDC)GetProcAddress(hGdi32, "D3DKMTOpenAdapterFromHdc");
        if (NULL == pfnOpenAdapter)
            break;
        pfnD3DKmtEscape = (PFND3DKMT_ESCAPE)GetProcAddress(hGdi32, "D3DKMTEscape");
        if (NULL == pfnD3DKmtEscape)
            break;
        pfnCloseAdapter = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(hGdi32, "D3DKMTCloseAdapter");
        if (NULL == pfnCloseAdapter)
            break;

        hLocal = GlobalAlloc(GHND, size);
        if (NULL == hLocal)
            break;

        pLocal = GlobalLock(hLocal);
        if (NULL == pLocal)
            break;

        memcpy(pLocal, pEscapeData, size);
        while (EnumDisplayDevices(NULL, devID++, &deviceName, 0))
        {
            hdc = CreateDC(deviceName.DeviceName, NULL, NULL, 0);
            /* Check if Device context is valid not*/
            if (NULL != hdc)
                break;
        }

        /* Using device context make a call to OpenAdapter*/
        pOpenAdapter = (D3DKMT_OPENADAPTERFROMHDC *)malloc(sizeof(D3DKMT_OPENADAPTERFROMHDC));
        if (NULL == pOpenAdapter)
            break;

        ZeroMemory(pOpenAdapter, sizeof(pOpenAdapter));
        pOpenAdapter->hDc = hdc;

        /* creates a graphics adapter object*/
        if (pfnOpenAdapter(pOpenAdapter) != S_OK)
            break;

        /* Prepare Escape header*/
        kmtEscape.hAdapter           = pOpenAdapter->hAdapter;
        kmtEscape.Type               = D3DKMT_ESCAPE_DRIVERPRIVATE;
        kmtEscape.pPrivateDriverData = (void *)malloc(size + sizeof(GFX_ESCAPE_HEADER_T_T));
        if (NULL == kmtEscape.pPrivateDriverData)
            break;

        kmtEscape.PrivateDriverDataSize = size + sizeof(GFX_ESCAPE_HEADER_T_T);
        ZeroMemory(&pHeader, sizeof(GFX_ESCAPE_HEADER_T_T));

        /* Set header with the escape request type*/
        sizeofEscHeader                 = sizeof(pHeader);
        pHeader.ulReserved              = size;
        pHeader.ulMinorInterfaceVersion = escapeOpCodeReq.MinorInterfaceVersion;
        pHeader.ulMajorInterfaceVersion = escapeOpCodeReq.MajorInterfaceVersion;
        pHeader.uiMajorEscapeCode       = escapeOpCodeReq.MajorEscapeCode;
        pHeader.uiMinorEscapeCode       = escapeOpCodeReq.MinorEscapeCode;
        /* Fill escape header with the details*/
        memcpy(kmtEscape.pPrivateDriverData, &pHeader, sizeof(GFX_ESCAPE_HEADER_T_T));
        PCHAR pPrivateData = (PCHAR)kmtEscape.pPrivateDriverData;
        PVOID pOutData     = pPrivateData + sizeof(GFX_ESCAPE_HEADER_T_T);
        memcpy(pOutData, pLocal, size);

        /* Make a driver escape call*/
        HRESULT ret = pfnD3DKmtEscape(&kmtEscape);
        hResult     = ret;
        /* Copy escape call structure*/
        memcpy(pEscapeData, pOutData, size);

    } while (FALSE);

    /* Release all memory*/
    if (pOpenAdapter)
    {
        closeAdapter.hAdapter = pOpenAdapter->hAdapter;
        pfnCloseAdapter(&closeAdapter);

        /* Free all the mallocs*/
        free(pOpenAdapter);
        pOpenAdapter = NULL;
    }

    if (kmtEscape.pPrivateDriverData)
    {
        free(kmtEscape.pPrivateDriverData);
        kmtEscape.pPrivateDriverData = NULL;
    }

    /* Release handles and heap variables*/
    if (hLocal != NULL)
    {
        GlobalUnlock(hLocal);
        GlobalFree(hLocal);
    }
    if (hdc != NULL)
        DeleteDC(hdc);

    return hResult;
}
