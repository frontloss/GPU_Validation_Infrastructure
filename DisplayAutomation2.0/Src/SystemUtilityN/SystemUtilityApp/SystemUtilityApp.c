// SystemUtilityApp.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "SystemUtilityApp.h"
#include <windows.h>

int main(int argc, _TCHAR *argv[])
{
    // Target ID's Not Same For mentioned Platform.
    /*
    Port	: Legacy : Yangra
    eDP_A	: 265988 : 8388688
    DP_B	: 200195 : 8257
    HDMI_C	: 206371 : 24626
    */

    //====TEST : Get EnumeratedDisplayInfo  ====

    ENUMERATED_DISPLAYS pEnumDisplay = { 0 };
    pEnumDisplay.Size                = sizeof(ENUMERATED_DISPLAYS);
    HRESULT pError                   = S_FALSE;
    GetEnumeratedDisplayInfo(&pEnumDisplay, &pError);

    if (argc > 1)
    {
        TestGetSetVrr(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo.adapterInfo, strtol(argv[1], NULL, 10));
    }

	BOOLEAN isNNscalingSupported      = FALSE;
	if (IsRetroscalingSupport(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo) == TRUE)
    {
		UINT Cstate = 0;
		BOOLEAN AddSucess = FALSE;
		printf("SUCCESS: IsNNscalingSupport.");
		isNNscalingSupported = TRUE;
		EnDsRetroScalingState(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo, 0);
		Cstate = CurrentRetroscalingState(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo);
		EnDsRetroScalingState(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo, 1);
		Cstate = CurrentRetroscalingState(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo);
		EnDsRetroScalingState(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo, 2);
		Cstate = CurrentRetroscalingState(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo);
		AddSucess = Add_Custom_Mode(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo,400,300);
		AddSucess = Add_Custom_Mode(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo,320,200);
		AddSucess = Add_Custom_Mode(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo,1000,600);
		AddSucess = Add_Custom_Mode(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo,1800,1200);
    }

    //====TEST : Get GetMiscSystemInfo  ====
    /*ENVIRONMENT_TYPE env_type;
    MISC_ESC_GET_SYSTEM_INFO_ARGS miscSystemInfo = { 0 };
    GetMiscSystemInfo(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo.adapterInfo, &miscSystemInfo, &pError);*/

    //====TEST 1: Get DLL Version ====
    // ULONG result;
    // GetDLLVersion(&result);
    // printf ("%d", &result);

    //====TEST 2: DPCD Registry ====
    // ULONG ulStartOffset = 1792; // 0x46000;
    // ULONG ulDpcdBuffer[sizeof(ULONG) * 512];
    // UINT dpcdBufferSize = 512;
    // DPCDRead(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo, ulStartOffset, ulDpcdBuffer, dpcdBufferSize, &pError);

    //====TEST 2: Read Registry ====
    /*REGISTRY_ACCESS_PROVIDER registryAccessProvider = 0;
    LPCSTR registrykey = "FeatureTestControl";
    PVOID outBuffer;
    outBuffer = malloc(sizeof(ULONG));
    ReadRegistry(registryAccessProvider, registrykey, outBuffer);*/

    //====TEST 3: Write Registry ====
    /*REGISTRY_ACCESS_PROVIDER registryAccessProvider = 0;
    LPCSTR registrykey = "FeatureTestControl";
    PVOID outBuffer;
    outBuffer = malloc(sizeof(ULONG));
    REGISTRY_TYPES registryType = 3;
    ULONG dataCount;
    WriteRegistry(registryAccessProvider, registrykey, outBuffer, registryType, dataCount);*/

    //====TEST 4: Delete Registry ====
    /*REGISTRY_ACCESS_PROVIDER registryAccessProvider = 0;
    LPCSTR registrykey = "FeatureTestControl";
    DeleteRegistry(registryAccessProvider, registrykey);*/

    //====TEST 5: Display Audio Format ====
    /*HRESULT *pErrorCode = S_FALSE;
    AUDIO_ENDPOINTS_INFO pAudioEndpointsInformation = { 0 };
    BOOL output;
    output = DisplayAudioFormat(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo, &pAudioEndpointsInformation, pErrorCode);
    printf(&output);*/

    //====TEST 6: Get EDID Data ====

    // HRESULT *pErrorCode = S_FALSE;
    /*PBYTE output;
    output = GetEdidData(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo, &pError);*/
    // printf(&output);

    //====TEST 7: Get Environment Details ====

    /*ENVIRONMENT_TYPE env_type;
    HRESULT pError = S_FALSE;
    env_type = GetExecutionEnvironmentDetails(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo.adapterInfo, &pError);*/

    //====TEST 8: IsxvYCC Supported ====
    // IsxvYCCSupportedByDisplayId(&pEnumDisplay.ConnectedDisplays[1].DisplayAndAdapterInfo, &pError);

    //====TEST 9: IsYCbCr Supported ====
    // IsYCbCrSupportedByDisplayId(&pEnumDisplay.ConnectedDisplays[1].DisplayAndAdapterInfo, &pError);

    //====TEST 10: EnableDisableYCbCr ====
    /*BOOLEAN bEnable = TRUE;
    EnableDisableYCbCr(&pEnumDisplay.ConnectedDisplays[1].DisplayAndAdapterInfo, bEnable, &pError);*/

    //====TEST 11: EnableDisablexvYCC ====
    /*BOOLEAN bEnable = FALSE;
    EnableDisablexvYCC(&pEnumDisplay.ConnectedDisplays[1].DisplayAndAdapterInfo, bEnable, &pError);*/

    //====TEST 12: GetDPPHWLUT ====
    /*ULONG Depth;
    CUI_DPP_HW_LUT_INFO CuiDppHwLutInfo = { 0 };

    Depth = GetDPPHWLUT(&CuiDppHwLutInfo, &pEnumDisplay.ConnectedDisplays[1].DisplayAndAdapterInfo.adapterInfo, &pError);*/

    //====TEST 13: SetDPPHWLUT ====
    /*CUI_DPP_HW_LUT_INFO CuiDppHwLutInfo = { 0 };
    CUI_DRIVER_ERROR driver_error = { 0 };
    CuiDppHwLutInfo.ulDepth = 16;
    CuiDppHwLutInfo.dwDisplayID = 8388688;
    CuiDppHwLutInfo.eOpType = APPLY_LUT;
    CuiDppHwLutInfo.LUTData = "C:\\SHAREDBINARY\\920697932\\Color\\Hw3DLUT\\CustomLUT\\CustomLUT_default.bin";
    CuiDppHwLutInfo.ErrorInfo = driver_error;
    SetDPPHWLUT(&CuiDppHwLutInfo, &pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo.adapterInfo);*/

    //====TEST 14: IsDDRW ====
    /*BOOL driver_type = FALSE;
    driver_type = Is_DDRW(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo.adapterInfo);*/

    //====TEST 15: AlsAggressivenessLevelOverride ====
    /*BOOLEAN lux_operation = TRUE;
    BOOLEAN aggressiveness_operation = TRUE;
    INT lux = 3500;
    INT aggressiveness_level = 2;
    AlsAggressivenessLevelOverride(&pEnumDisplay.ConnectedDisplays[0].DisplayAndAdapterInfo.adapterInfo, lux_operation, aggressiveness_operation, lux, aggressiveness_level);*/
    return 0;
}

PVOID GetFunctionHandle(_In_ REQUEST_TYPE requestType)
{
    PVOID          functionPointer  = NULL;
    static HMODULE dispConfigHandle = NULL;
    if (NULL == dispConfigHandle)
        dispConfigHandle = LoadLibraryA("OsInterfaces.dll");

    if (dispConfigHandle == NULL)
        return NULL;

    static HMODULE systemUtilityHandle = NULL;
    if (NULL == systemUtilityHandle)
        systemUtilityHandle = LoadLibraryA("SystemUtilityN.dll");

    if (systemUtilityHandle == NULL)
        return NULL;

    switch (requestType)
    {
    case GET_DLL_VERSION:
        if (NULL == pfnGetDLLVersion)
        {
            pfnGetDLLVersion = (PFN_GET_DLL_VERSION)GetProcAddress(systemUtilityHandle, "GetDLLVersion");
            functionPointer  = pfnGetDLLVersion;
        }
        else
        {
            functionPointer = pfnGetDLLVersion;
        }
        break;
    case GET_EDID_DATA:
        if (NULL == pfnGetEdidData)
        {
            pfnGetEdidData  = (PFN_GET_EDID_DATA)GetProcAddress(systemUtilityHandle, "GetEdidData");
            functionPointer = pfnGetEdidData;
        }
        else
        {
            functionPointer = pfnGetEdidData;
        }
        break;
    case DISPLAY_AUDIO_FORMAT:
        if (NULL == pfnDisplayAudioFormat)
        {
            pfnDisplayAudioFormat = (PFN_DISPLAY_AUDIO_FORMAT)GetProcAddress(systemUtilityHandle, "DisplayAudioFormat");
            functionPointer       = pfnDisplayAudioFormat;
        }
        else
        {
            functionPointer = pfnDisplayAudioFormat;
        }
        break;
    case GET_ENVIRONMENT:
        if (NULL == pfnGetExecutionEnvironmentDetails)
        {
            pfnGetExecutionEnvironmentDetails = (PFN_GET_ENVIRONMENT)GetProcAddress(systemUtilityHandle, "GetExecutionEnvironmentDetails");
            functionPointer                   = pfnGetExecutionEnvironmentDetails;
        }
        else
        {
            functionPointer = pfnGetExecutionEnvironmentDetails;
        }
        break;
    case DPCD_READ:
        if (NULL == pfnDPCDRead)
        {
            pfnDPCDRead     = (PFN_DPCD_READ)GetProcAddress(systemUtilityHandle, "DPCDRead");
            functionPointer = pfnDPCDRead;
        }
        else
        {
            functionPointer = pfnDPCDRead;
        }
        break;
    case READ_REGISTRY:
        if (NULL == pfnReadRegistry)
        {
            pfnReadRegistry = (PFN_READ_REGISTRY)GetProcAddress(systemUtilityHandle, "ReadRegistry");
            functionPointer = pfnReadRegistry;
        }
        else
        {
            functionPointer = pfnReadRegistry;
        }
        break;
    case WRITE_REGISTRY:
        if (NULL == pfnWriteRegistry)
        {
            pfnWriteRegistry = (PFN_WRITE_REGISTRY)GetProcAddress(systemUtilityHandle, "WriteRegistry");
            functionPointer  = pfnWriteRegistry;
        }
        else
        {
            functionPointer = pfnWriteRegistry;
        }
        break;
    case DELETE_REGISTRY:
        if (NULL == pfnDeleteRegistry)
        {
            pfnDeleteRegistry = (PFN_DELETE_REGISTRY)GetProcAddress(systemUtilityHandle, "DeleteRegistry");
            functionPointer   = pfnDeleteRegistry;
        }
        else
        {
            functionPointer = pfnDeleteRegistry;
        }
        break;
    case ISxvYCC_SUPPORTED:
        if (NULL == pfnIsxvYCCSupportedByDisplayId)
        {
            pfnIsxvYCCSupportedByDisplayId = (PFN_ISxvYCC_SUPPORTED)GetProcAddress(systemUtilityHandle, "IsxvYCCSupportedByDisplayId");
            functionPointer                = pfnIsxvYCCSupportedByDisplayId;
        }
        else
        {
            functionPointer = pfnIsxvYCCSupportedByDisplayId;
        }
        break;
    case ISYCbCr_SUPPORTED:
        if (NULL == pfnISYCbCrSupportedByDisplayId)
        {
            pfnISYCbCrSupportedByDisplayId = (PFN_ISYCbCr_SUPPORTED)GetProcAddress(systemUtilityHandle, "IsYCbCrSupportedByDisplayId");
            functionPointer                = pfnISYCbCrSupportedByDisplayId;
        }
        else
        {
            functionPointer = pfnISYCbCrSupportedByDisplayId;
        }
        break;
    case ENBLE_DISABLE_YCbCr:
        if (NULL == pfnEnableDisableYCbCr)
        {
            pfnEnableDisableYCbCr = (PFN_ENBLE_DISABLE_YCbCr)GetProcAddress(systemUtilityHandle, "EnableDisableYCbCr");
            functionPointer       = pfnEnableDisableYCbCr;
        }
        else
        {
            functionPointer = pfnEnableDisableYCbCr;
        }
        break;
    case ENBLE_DISABLE_xvYCC:
        if (NULL == pfnEnableDisablexvYCC)
        {
            pfnEnableDisablexvYCC = (PFN_ENBLE_DISABLE_xvYCC)GetProcAddress(systemUtilityHandle, "EnableDisablexvYCC");
            functionPointer       = pfnEnableDisablexvYCC;
        }
        else
        {
            functionPointer = pfnEnableDisablexvYCC;
        }
        break;
    case GET_DPP_HWLUT:
        if (NULL == pfnGetDPPHWLUT)
        {
            pfnGetDPPHWLUT  = (PFN_GET_DPP_HWLUT)GetProcAddress(systemUtilityHandle, "GetDPPHWLUT");
            functionPointer = pfnGetDPPHWLUT;
        }
        else
        {
            functionPointer = pfnGetDPPHWLUT;
        }
        break;
    case SET_DPP_HWLUT:
        if (NULL == pfnSetDPPHWLUT)
        {
            pfnSetDPPHWLUT  = (PFN_SET_DPP_HWLUT)GetProcAddress(systemUtilityHandle, "SetDPPHWLUT");
            functionPointer = pfnSetDPPHWLUT;
        }
        else
        {
            functionPointer = pfnSetDPPHWLUT;
        }
        break;
    case ENUMERATED_DISPLAYS_INFO:
        if (NULL == pfnGetEnumeratedDisplayInfo)
        {
            pfnGetEnumeratedDisplayInfo = (PFN_ENUMERATED_DISPLAYS_INFO)GetProcAddress(dispConfigHandle, "GetEnumeratedDisplayInfo");
            functionPointer             = pfnGetEnumeratedDisplayInfo;
        }
        else
        {
            functionPointer = pfnGetEnumeratedDisplayInfo;
        }
        break;
    case GET_MISC_SYSTEM_INFO:
        if (NULL == pfnGetMiscSystemInfo)
        {
            pfnGetMiscSystemInfo = (PFN_GET_MISC_SYSTEM_INFO)GetProcAddress(systemUtilityHandle, "GetMiscSystemInfo");
            functionPointer      = pfnGetMiscSystemInfo;
        }
        else
        {
            functionPointer = pfnGetMiscSystemInfo;
        }
        break;
    case ISDDRW:
        if (NULL == pfnIsDDRW)
        {
            pfnIsDDRW       = (PFN_IS_DDRW)GetProcAddress(systemUtilityHandle, "IsDDRW");
            functionPointer = pfnIsDDRW;
        }
        else
        {
            functionPointer = pfnIsDDRW;
        }
        break;
    case LACE_ALS_AGGRLEVEL_OVERRIDE:
        if (NULL == pfnLaceAlsAggrLevelOverride)
        {
            pfnLaceAlsAggrLevelOverride = (PFN_ALS_AGGRLEVEL_OVERRIDE)GetProcAddress(systemUtilityHandle, "AlsandAggressivessLevelOverride");
            functionPointer             = pfnLaceAlsAggrLevelOverride;
        }
        else
        {
            functionPointer = pfnLaceAlsAggrLevelOverride;
        }
        break;
    case GET_SET_VRR:
        if (NULL == pfnGetSetVrr)
        {
            pfnGetSetVrr    = (PFN_GET_SET_VRR)GetProcAddress(systemUtilityHandle, "GetSetVrr");
            functionPointer = pfnGetSetVrr;
        }
        else
        {
            functionPointer = pfnGetSetVrr;
        }
        break;
	default:
		functionPointer = NULL;
		break;
    }
    return functionPointer;
}

VOID TestGetSetVrr(PGFX_ADAPTER_INFO pAdapterInfo, LONG operation)
{
    if (NULL == (PFN_GET_SET_VRR)GetFunctionHandle(GET_SET_VRR))
    {
        printf("Could't Get GetSetVrr Handle\n");
        return;
    }
    DD_CUI_ESC_GET_SET_VRR_ARGS args = { 0 };
    args.Operation                   = operation;
    HRESULT result                   = (pfnGetSetVrr)(pAdapterInfo, &args);
    if (result != S_OK)
    {
        printf("Escape Call Failed\n");
    }
    else
    {
        printf("Escape Call is successful\n");
    }
    printf("VrrSupported: %d\n", args.VrrSupported);
    printf("VrrEnabled: %d\n", args.VrrEnabled);
    printf("VrrHighFpsSolnEnabled: %d\n", args.VrrHighFpsSolnEnabled);
    printf("VrrLowFpsSolnEnabled: %d\n", args.VrrLowFpsSolnEnabled);
}

VOID GetDLLVersion(_Inout_ PULONG pVersion)
{
    if (NULL == (PFN_GET_DLL_VERSION)GetFunctionHandle(GET_DLL_VERSION))
    {
        printf("Could't Get GetDisplayConfigInterfaceVersion Handle\n");
        return;
    }
    (pfnGetDLLVersion)(pVersion);
}

PBYTE GetEdidData(_In_ PDISPLAY_AND_ADAPTER_INFO pDisplayAdapterId, _Out_ HRESULT *pErrorCode)
{
    PBYTE pEdidByte = NULL;
    if (NULL == (PFN_GET_EDID_DATA)GetFunctionHandle(GET_EDID_DATA))
    {
        printf("Could't Get GetDisplayConfigInterfaceVersion Handle\n");
        return NULL;
    }
    pEdidByte = (pfnGetEdidData)(pDisplayAdapterId, pErrorCode);
    return pEdidByte;
}

BOOL DisplayAudioFormat(PDISPLAY_AND_ADAPTER_INFO pDisplayandAdapterInfo, AUDIO_ENDPOINTS_INFO *pAudioEndpointsInformation, HRESULT *pErrorCode)
{
    BOOL status = FALSE;
    if (NULL == (PFN_DISPLAY_AUDIO_FORMAT)GetFunctionHandle(DISPLAY_AUDIO_FORMAT))
    {
        printf("Could't Get DisplayAudioFormat Handle\n");
        return status;
    }
    status = (pfnDisplayAudioFormat)(pDisplayandAdapterInfo, pAudioEndpointsInformation, pErrorCode);
    return status;
}
ENVIRONMENT_TYPE GetExecutionEnvironmentDetails(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _Out_ HRESULT *pErrorCode)
{
    ENVIRONMENT_TYPE env_type;
    if (NULL == (PFN_GET_ENVIRONMENT)GetFunctionHandle(GET_ENVIRONMENT))
    {
        printf("Could't Get GetExecutionEnvironmentDetails Handle\n");
        return MAX_SIZE;
    }
    env_type = (pfnGetExecutionEnvironmentDetails)(pAdapterInfo, pErrorCode);
    return env_type;
}
BOOL DPCDRead(PDISPLAY_AND_ADAPTER_INFO DisplayAndAdapterInfo, ULONG ulStartOffset, ULONG ulDpcdBuffer[], UINT dpcdBufferSize, HRESULT *pErrorCode)
{
    BOOL status = FALSE;
    if (NULL == (PFN_DPCD_READ)GetFunctionHandle(DPCD_READ))
    {
        printf("Could't Get GetDisplayConfigInterfaceVersion Handle\n");
        return FALSE;
    }
    status = (pfnDPCDRead)(DisplayAndAdapterInfo, ulStartOffset, ulDpcdBuffer, dpcdBufferSize, pErrorCode);
    return status;
}

LONG ReadRegistry(_In_ REGISTRY_ACCESS_PROVIDER registryAccessProvider, _In_ LPCSTR registrykey, PVOID outBuffer)
{
    LONG status;
    if (NULL == (PFN_READ_REGISTRY)GetFunctionHandle(READ_REGISTRY))
    {
        printf("Could't Get SystemUtility_ReadRegistry Handle\n");
        return 0;
    }
    status = (pfnReadRegistry)(registryAccessProvider, registrykey, outBuffer);
    return status;
}
LONG WriteRegistry(_In_ REGISTRY_ACCESS_PROVIDER registryAccessProvider, _In_ LPCSTR registrykey, _In_ PVOID buffer, _In_ REGISTRY_TYPES registryType, _In_ ULONG dataCount)
{
    LONG status;
    if (NULL == (PFN_WRITE_REGISTRY)GetFunctionHandle(WRITE_REGISTRY))
    {
        printf("Could't Get SystemUtility_WriteRegistry Handle\n");
        return 0;
    }
    status = (pfnWriteRegistry)(registryAccessProvider, registrykey, buffer, registryType, dataCount);
    return status;
}
LONG DeleteRegistry(_In_ REGISTRY_ACCESS_PROVIDER registryAccessProvider, _In_ LPCSTR registrykey)
{
    LONG status;
    if (NULL == (PFN_DELETE_REGISTRY)GetFunctionHandle(DELETE_REGISTRY))
    {
        printf("Could't Get SystemUtility_DeleteRegistry Handle\n");
        return 0;
    }
    status = (pfnDeleteRegistry)(registryAccessProvider, registrykey);
    return status;
}

BOOL IsxvYCCSupportedByDisplayId(PDISPLAY_AND_ADAPTER_INFO pDisplayAndAdapterInfo, HRESULT *pErrorCode)
{
    BOOL bxvYCCSupported = FALSE;
    if (NULL == (PFN_ISxvYCC_SUPPORTED)GetFunctionHandle(ISxvYCC_SUPPORTED))
    {
        printf("Could't Get IsxvYCCSupportedByDisplayId Handle\n");
        return bxvYCCSupported;
    }
    bxvYCCSupported = (pfnIsxvYCCSupportedByDisplayId)(pDisplayAndAdapterInfo, pErrorCode);
    return bxvYCCSupported;
}
BOOL IsYCbCrSupportedByDisplayId(PDISPLAY_AND_ADAPTER_INFO pDisplayAndAdapterInfo, HRESULT *pErrorCode)
{
    BOOL bYCbCrSupported = FALSE;
    if (NULL == (PFN_ISYCbCr_SUPPORTED)GetFunctionHandle(ISYCbCr_SUPPORTED))
    {
        printf("Could't Get IsYCbCrSupportedByDisplayId Handle\n");
        return bYCbCrSupported;
    }
    bYCbCrSupported = (pfnISYCbCrSupportedByDisplayId)(pDisplayAndAdapterInfo, pErrorCode);
    return bYCbCrSupported;
}
BOOL EnableDisableYCbCr(PDISPLAY_AND_ADAPTER_INFO pDisplayAndAdapterInfo, BOOLEAN bEnable, HRESULT *pErrorCode)
{
    BOOL status = FALSE;
    if (NULL == (PFN_ENBLE_DISABLE_YCbCr)GetFunctionHandle(ENBLE_DISABLE_YCbCr))
    {
        printf("Could't Get EnableDisableYCbCr Handle\n");
        return status;
    }
    status = (pfnEnableDisableYCbCr)(pDisplayAndAdapterInfo, bEnable, pErrorCode);
    return status;
}
BOOL EnableDisablexvYCC(PDISPLAY_AND_ADAPTER_INFO pDisplayAndAdapterInfo, BOOLEAN bEnable, HRESULT *pErrorCode)
{
    BOOL status = FALSE;
    if (NULL == (PFN_ENBLE_DISABLE_xvYCC)GetFunctionHandle(ENBLE_DISABLE_xvYCC))
    {
        printf("Could't Get EnableDisablexvYCC Handle\n");
        return status;
    }
    status = (pfnEnableDisablexvYCC)(pDisplayAndAdapterInfo, bEnable, pErrorCode);
    return status;
}
ULONG GetDPPHWLUT(PCUI_DPP_HW_LUT_INFO pCuiDppHwLutInfo, PGFX_ADAPTER_INFO pAdapterInfo, HRESULT *pErrorCode)
{
    ULONG ulDepth;
    if (NULL == (PFN_GET_DPP_HWLUT)GetFunctionHandle(GET_DPP_HWLUT))
    {
        printf("Could't Get GetDPPHWLUT Handle\n");
        return 0;
    }
    ulDepth = (pfnGetDPPHWLUT)(pCuiDppHwLutInfo, pAdapterInfo, pErrorCode);
    return ulDepth;
}
HRESULT SetDPPHWLUT(PCUI_DPP_HW_LUT_INFO pCuiDppHwLutInfo, PGFX_ADAPTER_INFO pAdapterInfo)
{
    HRESULT status = S_FALSE;
    if (NULL == (PFN_SET_DPP_HWLUT)GetFunctionHandle(SET_DPP_HWLUT))
    {
        printf("Could't Get SetDPPHWLUT Handle\n");
    }
    status = (pfnSetDPPHWLUT)(pCuiDppHwLutInfo, pAdapterInfo);
    return status;
}

VOID GetEnumeratedDisplayInfo(_Out_ PENUMERATED_DISPLAYS pEnumDisplay, _Out_ HRESULT *pErrorCode)
{
    if (NULL == (PFN_ENUMERATED_DISPLAYS_INFO)GetFunctionHandle(ENUMERATED_DISPLAYS_INFO))
    {
        printf("Could't Get GetAllGfxAdapter Handle\n");
    }
    (pfnGetEnumeratedDisplayInfo)(pEnumDisplay, pErrorCode);
}

VOID GetMiscSystemInfo(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _Out_ MISC_ESC_GET_SYSTEM_INFO_ARGS *pMiscSystemInfo, _Out_ HRESULT *pErrorCode)
{
    if (NULL == (PFN_GET_MISC_SYSTEM_INFO)GetFunctionHandle(GET_MISC_SYSTEM_INFO))
    {
        printf("Could't Get GetExecutionEnvironmentDetails Handle\n");
    }
    (pfnGetMiscSystemInfo)(pAdapterInfo, pMiscSystemInfo, pErrorCode);
}

BOOL Is_DDRW(_In_ PGFX_ADAPTER_INFO pAdapterInfo)
{
    BOOL is_ddrw = FALSE;
    if (NULL == (PFN_IS_DDRW)GetFunctionHandle(ISDDRW))
    {
        printf("Could't Get IsDDRW Handle\n");
    }
    is_ddrw = (pfnIsDDRW)(pAdapterInfo);
    return is_ddrw;
}

BOOL AlsAggressivenessLevelOverride(_In_ PGFX_ADAPTER_INFO pAdapterInfo, BOOL lux_operation, BOOL aggressiveness_operation, INT lux, INT aggressiveness_level)
{
    BOOL status = FALSE;
    if (NULL == (PFN_ALS_AGGRLEVEL_OVERRIDE)GetFunctionHandle(LACE_ALS_AGGRLEVEL_OVERRIDE))
    {
        printf("Could't Get LaceAlsAggressivenesslevelOverride function Handle\n");
        return status;
    }
    status = (pfnLaceAlsAggrLevelOverride)(pAdapterInfo, lux_operation, aggressiveness_operation, lux, aggressiveness_level);
    return status;
}