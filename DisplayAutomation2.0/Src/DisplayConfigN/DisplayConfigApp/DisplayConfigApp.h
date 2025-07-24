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

/**
 * file name       DisplayConfigApp.h
 * Date:           7/27/2016
 * @version        0.1
 * @Author		  Amit Sau
 * Modified by
 * Description:    Switch display configuration between connected display
 */

#include "windows.h"
#include "..\DisplayConfigN\HeaderFiles\DisplayConfig.h"

#ifndef DISPLAY_CONFIG_APP_H
#define DISPLAY_CONFIG_APP_H

#pragma pack(push, DISPLAY_CONFIG_APP)
#pragma pack(1)

typedef enum _REQUEST_TYPE
{
    GET_VERSION                  = 0,
    GET_DISPLAY_CONFIG           = 1,
    SET_DISPLAY_CONFIG           = 2,
    GET_CURRENT_MODE             = 3,
    GET_SUPPORTED_MODES          = 4,
    SET_DISPLAY_MODE             = 5,
    GET_DISPLAY_TIMINGS          = 6,
    CLEANUP                      = 7,
    GET_ACTIVE_DISPLAY_CONFIG    = 8,
    GET_OS_PREFFERED_MODE        = 9,
    QUERY_DISPLAY_CONFIG_EX      = 10,
    GET_ALL_GFX_ADAPTER          = 11,
    GET_DISPLAY_AND_ADAPTER_INFO = 12,
    ENUMERATED_DISPLAYS_INFO     = 13,

} REQUEST_TYPE;

typedef HRESULT(__cdecl *PFN_GET_DISPLAY_TIMINGS)(PDISPLAY_MODE, PDISPLAY_TIMINGS);
typedef HRESULT(__cdecl *PFN_GET_VERSION)(PULONG);
typedef HRESULT(__cdecl *PFN_GET_DISP_CONFIG)(PDISPLAY_CONFIG);
typedef HRESULT(__cdecl *PFN_SET_DISP_CONFIG)(PDISPLAY_CONFIG);
typedef HRESULT(__cdecl *PFN_GET_CURRENT_MODE)(PDISPLAY_AND_ADAPTER_INFO, PDISPLAY_MODE);
typedef HRESULT(__cdecl *PFN_GET_SUPPORTED_MODES)(PDISPLAY_AND_ADAPTER_INFO, BOOLEAN, PENUMERATED_DISPLAY_MODES);
typedef HRESULT(__cdecl *PFN_SET_DISP_MODE)(PDISPLAY_MODE, BOOLEAN, INT);
typedef HRESULT(__cdecl *PFN_CLEANUP)();
typedef HRESULT(__cdecl *PFN_GET_ACTIVE_DISPLAY_CONFIG)();
typedef HRESULT(__cdecl *PFN_GET_OS_PREFFERED_MODE)(PDISPLAY_AND_ADAPTER_INFO, PDISPLAY_TIMINGS);
typedef HRESULT(__cdecl *PFN_QUERY_DISPLAY_CONFIG_EX)(UINT, PDISPLAY_AND_ADAPTER_INFO, PQUERY_DISPLAY_CONFIG);
typedef HRESULT(__cdecl *PFN_GET_ALL_GFX_ADAPTER)(PGFX_ADAPTER_DETAILS);
typedef HRESULT(__cdecl *PFN_GET_DISPLAY_AND_ADAPTER_INFO)(UINT32, LUID, PDISPLAY_AND_ADAPTER_INFO);
typedef HRESULT(__cdecl *PFN_ENUMERATED_DISPLAYS_INFO)(PENUMERATED_DISPLAYS, HRESULT);

PFN_GET_DISPLAY_TIMINGS          pfnGetDisplayTimings        = NULL;
PFN_GET_VERSION                  pfnGetVersion               = NULL;
PFN_GET_DISP_CONFIG              pfnGetDisplayConfig         = NULL;
PFN_SET_DISP_CONFIG              pfnSetDisplayConfig         = NULL;
PFN_GET_CURRENT_MODE             pfnGetCurrentMode           = NULL;
PFN_GET_SUPPORTED_MODES          pfnGetSupportedModes        = NULL;
PFN_SET_DISP_MODE                pfnSetDisplayMode           = NULL;
PFN_CLEANUP                      pfnCleanup                  = NULL;
PFN_GET_ACTIVE_DISPLAY_CONFIG    pfnGetActiveDisplayConfig   = NULL;
PFN_GET_OS_PREFFERED_MODE        pfnGetOSPrefferedMode       = NULL;
PFN_QUERY_DISPLAY_CONFIG_EX      pfnQueryDisplayConfigEx     = NULL;
PFN_GET_ALL_GFX_ADAPTER          pfnGetAllGfxAdapterDetails  = NULL;
PFN_GET_DISPLAY_AND_ADAPTER_INFO pfnGetDisplayAndAdapterInfo = NULL;
PFN_ENUMERATED_DISPLAYS_INFO     pfnGetEnumeratedDisplayInfo = NULL;

PVOID GetFunctionHandle(_In_ REQUEST_TYPE requestType);

VOID    GetAPIVersion(_Inout_ PULONG pVersion);
VOID    GetDisplayConfiguration(_Inout_ PDISPLAY_CONFIG pConfig);
VOID    SetDisplayConfiguration(_Inout_ PDISPLAY_CONFIG pConfig);
VOID    GetCurrentMode(_In_ PDISPLAY_AND_ADAPTER_INFO pDisplayAdapterId, _Out_ PDISPLAY_MODE pDisplayMode);
VOID    GetAllSupportedModes(_Inout_ PDISPLAY_AND_ADAPTER_INFO pdisplayadapterId, _In_ BOOLEAN rotation_flag, _Out_ PENUMERATED_DISPLAY_MODES pEnumDisplayModes);
VOID    GetDisplayTimings(_In_ PDISPLAY_MODE pCurrentMode, _Out_ PDISPLAY_TIMINGS pDisplayTimings);
VOID    SetDisplayMode(_Inout_ PDISPLAY_MODE pModeList, _In_ BOOLEAN virtualModeSetAware, _In_ INT delayTime);
VOID    Cleanup();
VOID    GetActiveDisplayConfiguration(_Out_ PACTIVE_DISPLAY_CONFIG pDisplayConfig);
BOOLEAN GetOSPrefferedMode(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayadapterId, _Out_ PDISPLAY_TIMINGS pDisplayTimings);
VOID    QueryDisplayConfigEx(_In_ UINT qdcflag, _In_ PDISPLAY_AND_ADAPTER_INFO pDisplayAdapterId, _Out_ PQUERY_DISPLAY_CONFIG pQueryDisplay);
VOID    GetAllGfxAdapterDetails(_Out_ PGFX_ADAPTER_DETAILS pAdapterDetails);
VOID    GetDisplayAndAdapterInfo(_In_ UINT32 SourceID, _In_ LUID adapterID, _Inout_ PDISPLAY_AND_ADAPTER_INFO pdisplay_and_adapter_info);
VOID    GetEnumeratedDisplayInfo(_Out_ PENUMERATED_DISPLAYS pEnumDisplay, _Out_ HRESULT *pErrorCode);

#pragma pack(pop, DISPLAY_CONFIG_APP)
#endif