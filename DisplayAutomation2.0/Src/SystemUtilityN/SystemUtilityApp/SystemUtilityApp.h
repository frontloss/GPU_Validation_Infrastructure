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

/**
 * file name       SystemUtilityApp.h
 * @Author		  Raghupathy
 */

#include "windows.h"
#include "..\SystemUtilityN\HeaderFiles\SystemUtility.h"
#include "..\SystemUtilityN\HeaderFiles\Color.h"
#include "..\..\DisplayConfigN\DisplayConfigN\HeaderFiles\DisplayConfig.h"
#include "..\SystemUtilityN\HeaderFiles\Audio.h"

#ifndef SYSTEM_UTILITY_APP_H
#define SYSTEM_UTILITY_APP_H

#pragma pack(push, SYSTEM_UTILITY_APP)
#pragma pack(1)

typedef enum _REQUEST_TYPE
{
    GET_DLL_VERSION             = 0,
    DISPLAY_AUDIO_FORMAT        = 1,
    GET_EDID_DATA               = 2,
    GET_ENVIRONMENT             = 3,
    DPCD_READ                   = 4,
    READ_REGISTRY               = 5,
    WRITE_REGISTRY              = 6,
    DELETE_REGISTRY             = 7,
    ISxvYCC_SUPPORTED           = 8,
    ISYCbCr_SUPPORTED           = 9,
    ENBLE_DISABLE_YCbCr         = 10,
    ENBLE_DISABLE_xvYCC         = 11,
    GET_DPP_HWLUT               = 12,
    SET_DPP_HWLUT               = 13,
    ENUMERATED_DISPLAYS_INFO    = 14,
    GET_MISC_SYSTEM_INFO        = 15,
    ISDDRW                      = 16,
    LACE_ALS_AGGRLEVEL_OVERRIDE = 17,
    GET_SET_VRR
} REQUEST_TYPE;

typedef HRESULT(__cdecl *PFN_GET_DLL_VERSION)(PULONG);
typedef HRESULT(__cdecl *PFN_DISPLAY_AUDIO_FORMAT)(PDISPLAY_AND_ADAPTER_INFO, AUDIO_ENDPOINTS_INFO *, HRESULT *);
typedef PBYTE(__cdecl *PFN_GET_EDID_DATA)(PDISPLAY_AND_ADAPTER_INFO, HRESULT *);
typedef HRESULT(__cdecl *PFN_GET_ENVIRONMENT)(PGFX_ADAPTER_INFO, HRESULT *);
typedef HRESULT(__cdecl *PFN_DPCD_READ)(PDISPLAY_AND_ADAPTER_INFO, ULONG, ULONG[], UINT, HRESULT *);
typedef HRESULT(__cdecl *PFN_READ_REGISTRY)(REGISTRY_ACCESS_PROVIDER, LPCSTR, PVOID);
typedef HRESULT(__cdecl *PFN_WRITE_REGISTRY)(REGISTRY_ACCESS_PROVIDER, LPCSTR, PVOID, REGISTRY_TYPES, ULONG);
typedef HRESULT(__cdecl *PFN_DELETE_REGISTRY)(REGISTRY_ACCESS_PROVIDER, LPCSTR);
typedef HRESULT(__cdecl *PFN_ISxvYCC_SUPPORTED)(PDISPLAY_AND_ADAPTER_INFO, HRESULT *);
typedef HRESULT(__cdecl *PFN_ISYCbCr_SUPPORTED)(PDISPLAY_AND_ADAPTER_INFO, HRESULT *);
typedef HRESULT(__cdecl *PFN_ENBLE_DISABLE_YCbCr)(PDISPLAY_AND_ADAPTER_INFO, BOOLEAN, HRESULT *);
typedef HRESULT(__cdecl *PFN_ENBLE_DISABLE_xvYCC)(PDISPLAY_AND_ADAPTER_INFO, BOOLEAN, HRESULT *);
typedef HRESULT(__cdecl *PFN_GET_DPP_HWLUT)(PCUI_DPP_HW_LUT_INFO, PGFX_ADAPTER_INFO, HRESULT *);
typedef HRESULT(__cdecl *PFN_SET_DPP_HWLUT)(PCUI_DPP_HW_LUT_INFO, PGFX_ADAPTER_INFO);
typedef HRESULT(__cdecl *PFN_ENUMERATED_DISPLAYS_INFO)(PENUMERATED_DISPLAYS, HRESULT *);
typedef HRESULT(__cdecl *PFN_GET_MISC_SYSTEM_INFO)(PGFX_ADAPTER_INFO, MISC_ESC_GET_SYSTEM_INFO_ARGS *, HRESULT *);
typedef HRESULT(__cdecl *PFN_IS_DDRW)(PGFX_ADAPTER_INFO);
typedef HRESULT(__cdecl *PFN_ALS_AGGRLEVEL_OVERRIDE)(PGFX_ADAPTER_INFO, BOOL, BOOL, INT, INT);
typedef HRESULT(__cdecl *PFN_GET_SET_VRR)(PGFX_ADAPTER_INFO, PDD_CUI_ESC_GET_SET_VRR_ARGS);

PFN_ENUMERATED_DISPLAYS_INFO pfnGetEnumeratedDisplayInfo       = NULL;
PFN_GET_DLL_VERSION          pfnGetDLLVersion                  = NULL;
PFN_DISPLAY_AUDIO_FORMAT     pfnDisplayAudioFormat             = NULL;
PFN_GET_EDID_DATA            pfnGetEdidData                    = NULL;
PFN_GET_ENVIRONMENT          pfnGetExecutionEnvironmentDetails = NULL;
PFN_DPCD_READ                pfnDPCDRead                       = NULL;

PFN_READ_REGISTRY   pfnReadRegistry   = NULL;
PFN_WRITE_REGISTRY  pfnWriteRegistry  = NULL;
PFN_DELETE_REGISTRY pfnDeleteRegistry = NULL;

PFN_ISxvYCC_SUPPORTED   pfnIsxvYCCSupportedByDisplayId = NULL;
PFN_ISYCbCr_SUPPORTED   pfnISYCbCrSupportedByDisplayId = NULL;
PFN_ENBLE_DISABLE_YCbCr pfnEnableDisableYCbCr          = NULL;
PFN_ENBLE_DISABLE_xvYCC pfnEnableDisablexvYCC          = NULL;
PFN_GET_DPP_HWLUT       pfnGetDPPHWLUT                 = NULL;
PFN_SET_DPP_HWLUT       pfnSetDPPHWLUT                 = NULL;

PFN_GET_MISC_SYSTEM_INFO   pfnGetMiscSystemInfo        = NULL;
PFN_IS_DDRW                pfnIsDDRW                   = NULL;
PFN_ALS_AGGRLEVEL_OVERRIDE pfnLaceAlsAggrLevelOverride = NULL;
PFN_GET_SET_VRR            pfnGetSetVrr                = NULL;

PVOID GetFunctionHandle(_In_ REQUEST_TYPE requestType);

VOID             GetDLLVersion(_Inout_ PULONG pVersion);
BOOL             DisplayAudioFormat(PDISPLAY_AND_ADAPTER_INFO pDisplayandAdapterInfo, AUDIO_ENDPOINTS_INFO *pAudioEndpointsInformation, HRESULT *pErrorCode);
PBYTE            GetEdidData(_In_ PDISPLAY_AND_ADAPTER_INFO pDisplayAndAdapterInfo, _Out_ HRESULT *pErrorCode);
ENVIRONMENT_TYPE GetExecutionEnvironmentDetails(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _Out_ HRESULT *pErrorCode);
BOOL             DPCDRead(PDISPLAY_AND_ADAPTER_INFO DisplayAndAdapterInfo, ULONG ulStartOffset, ULONG ulDpcdBuffer[], UINT dpcdBufferSize, HRESULT *errorCode);
LONG             ReadRegistry(_In_ REGISTRY_ACCESS_PROVIDER registryAccessProvider, _In_ LPCSTR registrykey, PVOID outBuffer);
LONG    WriteRegistry(_In_ REGISTRY_ACCESS_PROVIDER registryAccessProvider, _In_ LPCSTR registrykey, _In_ PVOID buffer, _In_ REGISTRY_TYPES registryType, _In_ ULONG dataCount);
LONG    DeleteRegistry(_In_ REGISTRY_ACCESS_PROVIDER registryAccessProvider, _In_ LPCSTR registrykey);
BOOL    IsxvYCCSupportedByDisplayId(PDISPLAY_AND_ADAPTER_INFO pDisplayAndAdapterInfo, HRESULT *pErrorCode);
BOOL    IsYCbCrSupportedByDisplayId(PDISPLAY_AND_ADAPTER_INFO pDisplayAndAdapterInfo, HRESULT *pErrorCode);
BOOL    EnableDisableYCbCr(PDISPLAY_AND_ADAPTER_INFO pDisplayAndAdapterInfo, BOOLEAN bEnable, HRESULT *pErrorCode);
BOOL    EnableDisablexvYCC(PDISPLAY_AND_ADAPTER_INFO pDisplayAndAdapterInfo, BOOLEAN bEnable, HRESULT *pErrorCode);
ULONG   GetDPPHWLUT(PCUI_DPP_HW_LUT_INFO pCuiDppHwLutInfo, PGFX_ADAPTER_INFO pAdapterInfo, HRESULT *pErrorCode);
HRESULT SetDPPHWLUT(PCUI_DPP_HW_LUT_INFO pCuiDppHwLutInfo, PGFX_ADAPTER_INFO pAdapterInfo);
VOID    GetEnumeratedDisplayInfo(_Out_ PENUMERATED_DISPLAYS pEnumDisplay, _Out_ HRESULT *pErrorCode);
VOID    GetMiscSystemInfo(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _Out_ MISC_ESC_GET_SYSTEM_INFO_ARGS *pMiscSystemInfo, _Out_ HRESULT *pErrorCode);
BOOL    IsDDRW(PGFX_ADAPTER_INFO pAdapterInfo);
BOOL    AlsAggressivenessLevelOverride(_In_ PGFX_ADAPTER_INFO pAdapterInfo, BOOL lux_operation, BOOL aggressiveness_operation, INT lux, INT aggressiveness_level);
VOID    TestGetSetVrr(PGFX_ADAPTER_DETAILS, LONG);

#pragma pack(pop, SYSTEM_UTILITY_APP)
#endif