// DisplayConfigApp.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "DisplayConfigApp.h"
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

    /* Adapter Information*/
    /*INTEL - Mentioned Device & Instance ID can vary */
    WCHAR vendor[]   = L"8086";
    WCHAR device[]   = L"8A5B";
    WCHAR instance[] = L"3&11583659&0&10";
    /*NVIDIA - Mentioned Device & Instance ID can vary*/
    WCHAR vendor1[]   = L"10DE";
    WCHAR device1[]   = L"13BB";
    WCHAR instance1[] = L"4&34";
    /*AMD - Mentioned Device & Instance ID can vary*/
    WCHAR vendor2[]   = L"1002";
    WCHAR device2[]   = L"67EF";
    WCHAR instance2[] = L"4&34";

    //====TEST : Get EnumeratedDisplayInfo  ====
    /*ENUMERATED_DISPLAYS pEnumDisplay = { 0 };
    HRESULT pErrorCode = { 0 };
    pEnumDisplay.Size = sizeof(ENUMERATED_DISPLAYS);
    GetEnumeratedDisplayInfo(&pEnumDisplay, &pErrorCode);*/

    //=====TEST 1: Get Display Timings =====

    /*DISPLAY_MODE displayMode = { 0 };
    DISPLAY_TIMINGS displayTimings = { 0 };
    displayMode.HzRes = 1920;
    displayMode.VtRes = 1080;
    displayMode.refreshRate = 60;
    displayMode.rotation = ROTATE_0;
    displayMode.scaling = MDS;
    displayMode.scanlineOrdering = PROGRESSIVE;
    displayMode.targetId = 8388688;
    displayMode.DisplayAndAdapterInfo.TargetID = 8388688;
    wcscpy_s(displayMode.DisplayAndAdapterInfo.VendorID, '5', vendor);
    wcscpy_s(displayMode.DisplayAndAdapterInfo.DeviceID, '5', device);
    wcscpy_s(displayMode.DisplayAndAdapterInfo.DeviceInstanceID, '5', instance);
    GetDisplayTimings(&displayMode, &displayTimings);*/

    //====TEST 2: Get Display Configuration ====

    /*DISPLAY_CONFIG GetConfig = { 0 };
    GetDisplayConfiguration(&GetConfig);
    printf("\nTopology: %d\n", GetConfig.topology);*/

    //====TEST 3: Get Active Display Configuration ====

    /*ACTIVE_DISPLAY_CONFIG GetActiveConfig = { 0 };
    GetActiveDisplayConfiguration(&GetActiveConfig);*/

    //====TEST 4: Set Display Configuration ====

    /*DISPLAY_CONFIG SetConfig = { 0 };

    //No.of Displays and Topology are set here
    SetConfig.size = sizeof(DISPLAY_CONFIG);
    SetConfig.numberOfDisplays = 1;
    SetConfig.topology = SINGLE;
    //Based on displays Target ID filled in Respective pathInfo array
    SetConfig.displayPathInfo[0].targetId = 8388688;
    SetConfig.displayPathInfo[1].targetId = 8257;
    SetConfig.displayPathInfo[2].targetId = 708866;
    SetConfig.displayPathInfo[3].targetId = 708864;
    //DisplayAndAdapterInfo Structure filled with TargetID and Adapter Information for each Displays
    SetConfig.displayPathInfo[0].DisplayAndAdapterInfo.TargetID = 8388688;
    wcscpy_s(SetConfig.displayPathInfo[0].DisplayAndAdapterInfo.VendorID, '5', vendor);
    wcscpy_s(SetConfig.displayPathInfo[0].DisplayAndAdapterInfo.DeviceID, '5', device);
    wcscpy_s(SetConfig.displayPathInfo[0].DisplayAndAdapterInfo.DeviceInstanceID, '5', instance);
    SetConfig.displayPathInfo[1].DisplayAndAdapterInfo.TargetID = 8257;
    wcscpy_s(SetConfig.displayPathInfo[1].DisplayAndAdapterInfo.VendorID, '5', vendor);
    wcscpy_s(SetConfig.displayPathInfo[1].DisplayAndAdapterInfo.DeviceID, '5', device);
    wcscpy_s(SetConfig.displayPathInfo[1].DisplayAndAdapterInfo.DeviceInstanceID, '5', instance);
    SetConfig.displayPathInfo[2].DisplayAndAdapterInfo.TargetID = 708866;
    wcscpy_s(SetConfig.displayPathInfo[2].DisplayAndAdapterInfo.VendorID, '5', vendor1);
    wcscpy_s(SetConfig.displayPathInfo[2].DisplayAndAdapterInfo.DeviceID, '5', device1);
    wcscpy_s(SetConfig.displayPathInfo[2].DisplayAndAdapterInfo.DeviceInstanceID, '5', instance1);
    SetConfig.displayPathInfo[3].DisplayAndAdapterInfo.TargetID = 708864;
    wcscpy_s(SetConfig.displayPathInfo[3].DisplayAndAdapterInfo.VendorID, '5', vendor1);
    wcscpy_s(SetConfig.displayPathInfo[3].DisplayAndAdapterInfo.DeviceID, '5', device1);
    wcscpy_s(SetConfig.displayPathInfo[3].DisplayAndAdapterInfo.DeviceInstanceID, '5', instance1);
    SetDisplayConfiguration(&SetConfig);*/

    //====TEST 5: Get Current Mode ====

    /*DISPLAY_MODE displayMode = { 0 };
    DISPLAY_AND_ADAPTER_INFO displayAndAdapterInfo = { 0 };
    displayAndAdapterInfo.TargetID = 8388688;
    wcscpy_s(displayAndAdapterInfo.VendorID, '5', vendor);
    wcscpy_s(displayAndAdapterInfo.DeviceID, '5', device);
    wcscpy_s(displayAndAdapterInfo.DeviceInstanceID, '5', instance);
    GetCurrentMode(&displayAndAdapterInfo, &displayMode);*/

    // TEST 6: Get All Supported Modes ====

    /*BOOLEAN rotation = 1;
    DISPLAY_AND_ADAPTER_INFO displayAndAdapterInfo = { 0 };
    ENUMERATED_DISPLAY_MODES supportedModes = { 0 };
    displayAndAdapterInfo.TargetID = 8388688;
    wcscpy_s(displayAndAdapterInfo.VendorID, '5', vendor);
    wcscpy_s(displayAndAdapterInfo.DeviceID, '5', device);
    wcscpy_s(displayAndAdapterInfo.DeviceInstanceID, '5', instance);
    supportedModes.size = sizeof(ENUMERATED_DISPLAY_MODES);
    GetAllSupportedModes(&displayAndAdapterInfo, rotation, &supportedModes);*/

    //====TEST 7: Set Display Mode =====

    /*DISPLAY_MODE displayMode = { 0 };

    displayMode.HzRes = 1920;
    displayMode.VtRes = 1080;
    displayMode.refreshRate = 60;
    displayMode.rotation = ROTATE_0;
    displayMode.scaling = MDS;
    displayMode.scanlineOrdering = PROGRESSIVE;
    displayMode.targetId = 8388688;
    displayMode.DisplayAndAdapterInfo.TargetID = 8388688;
    wcscpy_s(displayMode.DisplayAndAdapterInfo.VendorID, '5', vendor);
    wcscpy_s(displayMode.DisplayAndAdapterInfo.DeviceID, '5', device);
    wcscpy_s(displayMode.DisplayAndAdapterInfo.DeviceInstanceID, '5', instance);
    SetDisplayMode(&displayMode, TRUE, 6000);*/

    //====TEST 8: Set Display Mode Based on Supported Modes ====

    /*int i = 0;
    BOOLEAN rotation = 1;
    DISPLAY_AND_ADAPTER_INFO displayAndAdapterInfo = { 0 };
    ENUMERATED_DISPLAY_MODES supportedModes = { 0 };
    displayAndAdapterInfo.TargetID = 8388688;
    wcscpy_s(displayAndAdapterInfo.VendorID, '5', vendor);
    wcscpy_s(displayAndAdapterInfo.DeviceID, '5', device);
    wcscpy_s(displayAndAdapterInfo.DeviceInstanceID, '5', instance);
    supportedModes.size = sizeof(ENUMERATED_DISPLAY_MODES);
    GetAllSupportedModes(&displayAndAdapterInfo, rotation, &supportedModes);
    for (int i = 0; i < supportedModes.noOfSupportedModes; i++)
    {
        if (supportedModes.pDisplayMode[i].HzRes != 1024 && supportedModes.pDisplayMode[i].VtRes != 768 && supportedModes.pDisplayMode[i].refreshRate != 23)
            continue;
        printf("\n****************************************[Mode Index: %d]****************************************\n", i + 1);
        char scaling[8];
        switch (supportedModes.pDisplayMode[i].scaling)
        {
        case MAR:
            strcpy(scaling, "MAR");
            break;
        case FS:
            strcpy(scaling, "FS");
            break;
        case MDS:
            strcpy(scaling, "MDS");
            break;
        case CI:
            strcpy(scaling, "CI");
            break;
        default:
            strcpy(scaling, "UNKNOWN");
            break;
        }
        supportedModes.pDisplayMode[i].rotation = ROTATE_90;
        printf("Requested Display Mode Res: [%d x %d] RR: [%d] Scanline: [%d] Scaling: [%s] \n", supportedModes.pDisplayMode[i].HzRes, supportedModes.pDisplayMode[i].VtRes,
            supportedModes.pDisplayMode[i].refreshRate, supportedModes.pDisplayMode[i].scanlineOrdering, scaling);
        SetDisplayMode(&supportedModes.pDisplayMode[i], TRUE,6000);
    }
    Cleanup();*/

    //====TEST 9: Get OS Preferred Mode ====

    /*DISPLAY_TIMINGS displayTimings = { 0 };
    DISPLAY_AND_ADAPTER_INFO displayAndAdapterInfo = { 0 };
    displayAndAdapterInfo.TargetID = 708866;
    wcscpy_s(displayAndAdapterInfo.VendorID, '5', vendor);
    wcscpy_s(displayAndAdapterInfo.DeviceID, '5', device);
    wcscpy_s(displayAndAdapterInfo.DeviceInstanceID, '5', instance);
    GetOSPrefferedMode(&displayAndAdapterInfo, &displayTimings);*/

    //====TEST 10: QueryDisplayConfigEx ====

    /*QUERY_DISPLAY_CONFIG querydisplay = { 0 };
    DISPLAY_AND_ADAPTER_INFO displayAndAdapterInfo = { 0 };
    UINT qdcFlag = 20;
    displayAndAdapterInfo.TargetID = 8388688;
    wcscpy_s(displayAndAdapterInfo.VendorID, '5', vendor);
    wcscpy_s(displayAndAdapterInfo.DeviceID, '5', device);
    wcscpy_s(displayAndAdapterInfo.DeviceInstanceID, '5', instance);
    QueryDisplayConfigEx(qdcFlag, &displayAndAdapterInfo, &querydisplay);*/

    //====TEST 11: Get All GFX Adapter Details ====

    /*GFX_ADAPTER_DETAILS pAdapterDetails = { 0 };
    GetAllGfxAdapterDetails(&pAdapterDetails);*/

    //====TEST 12: Get DisplayAndAdapterInfo Details ====

    /*DISPLAY_AND_ADAPTER_INFO displayAndAdapterInfo = { 0 };
    displayAndAdapterInfo.TargetID = 8388688;
    BOOLEAN status;
    status = GetDisplayAndAdapterInfo(&displayAndAdapterInfo);*/

    return 0;
}

PVOID GetFunctionHandle(_In_ REQUEST_TYPE requestType)
{
    PVOID          functionPointer  = NULL;
    static HMODULE dispConfigHandle = NULL;
    if (NULL == dispConfigHandle)
        dispConfigHandle = LoadLibraryA("../../../bin/DisplayConfigN.dll");

    if (dispConfigHandle == NULL)
        return NULL;

    switch (requestType)
    {
    case GET_DISPLAY_TIMINGS:
        if (NULL == pfnGetDisplayTimings)
        {
            pfnGetDisplayTimings = (PFN_GET_DISPLAY_TIMINGS)GetProcAddress(dispConfigHandle, "GetDisplayTimings");
            functionPointer      = pfnGetDisplayTimings;
        }
        else
        {
            functionPointer = pfnGetDisplayTimings;
        }
        break;
    case GET_VERSION:
        if (NULL == pfnGetVersion)
        {
            pfnGetVersion   = (PFN_GET_VERSION)GetProcAddress(dispConfigHandle, "GetDisplayConfigInterfaceVersion");
            functionPointer = pfnGetVersion;
        }
        else
        {
            functionPointer = pfnGetVersion;
        }
        break;
    case GET_DISPLAY_CONFIG:
        if (NULL == pfnGetDisplayConfig)
        {
            pfnGetDisplayConfig = (PFN_GET_DISP_CONFIG)GetProcAddress(dispConfigHandle, "GetDisplayConfiguration");
            functionPointer     = pfnGetDisplayConfig;
        }
        else
        {
            functionPointer = pfnGetDisplayConfig;
        }
        break;
    case SET_DISPLAY_CONFIG:
        if (NULL == pfnSetDisplayConfig)
        {
            pfnSetDisplayConfig = (PFN_SET_DISP_CONFIG)GetProcAddress(dispConfigHandle, "SetDisplayConfiguration");
            functionPointer     = pfnSetDisplayConfig;
        }
        else
        {
            functionPointer = pfnSetDisplayConfig;
        }
        break;
    case GET_CURRENT_MODE:
        if (NULL == pfnGetCurrentMode)
        {
            pfnGetCurrentMode = (PFN_GET_CURRENT_MODE)GetProcAddress(dispConfigHandle, "GetCurrentMode");
            functionPointer   = pfnGetCurrentMode;
        }
        else
        {
            functionPointer = pfnGetCurrentMode;
        }
        break;
    case GET_SUPPORTED_MODES:
        if (NULL == pfnGetSupportedModes)
        {
            pfnGetSupportedModes = (PFN_GET_SUPPORTED_MODES)GetProcAddress(dispConfigHandle, "GetAllSupportedModes");
            functionPointer      = pfnGetSupportedModes;
        }
        else
        {
            functionPointer = pfnGetSupportedModes;
        }
        break;
    case SET_DISPLAY_MODE:
        if (NULL == pfnSetDisplayMode)
        {
            pfnSetDisplayMode = (PFN_SET_DISP_MODE)GetProcAddress(dispConfigHandle, "SetDisplayMode");
            functionPointer   = pfnSetDisplayMode;
        }
        else
        {
            functionPointer = pfnSetDisplayMode;
        }
        break;
    case CLEANUP:
        if (NULL == pfnCleanup)
        {
            pfnCleanup      = (PFN_CLEANUP)GetProcAddress(dispConfigHandle, "Cleanup");
            functionPointer = pfnCleanup;
        }
        else
        {
            functionPointer = pfnCleanup;
        }
        break;

    case GET_ACTIVE_DISPLAY_CONFIG:
        if (NULL == pfnGetActiveDisplayConfig)
        {
            pfnGetActiveDisplayConfig = (PFN_GET_ACTIVE_DISPLAY_CONFIG)GetProcAddress(dispConfigHandle, "GetActiveDisplayConfiguration");
            functionPointer           = pfnGetActiveDisplayConfig;
        }
        else
        {
            functionPointer = pfnGetActiveDisplayConfig;
        }
        break;

    case GET_OS_PREFFERED_MODE:
        if (NULL == pfnGetOSPrefferedMode)
        {
            pfnGetOSPrefferedMode = (PFN_GET_OS_PREFFERED_MODE)GetProcAddress(dispConfigHandle, "GetOSPrefferedMode");
            functionPointer       = pfnGetOSPrefferedMode;
        }
        else
        {
            functionPointer = pfnGetOSPrefferedMode;
        }
        break;

    case QUERY_DISPLAY_CONFIG_EX:
        if (NULL == pfnQueryDisplayConfigEx)
        {
            pfnQueryDisplayConfigEx = (PFN_QUERY_DISPLAY_CONFIG_EX)GetProcAddress(dispConfigHandle, "QueryDisplayConfigEx");
            functionPointer         = pfnQueryDisplayConfigEx;
        }
        else
        {
            functionPointer = pfnQueryDisplayConfigEx;
        }
        break;

    case GET_ALL_GFX_ADAPTER:
        if (NULL == pfnGetAllGfxAdapterDetails)
        {
            pfnGetAllGfxAdapterDetails = (PFN_GET_ALL_GFX_ADAPTER)GetProcAddress(dispConfigHandle, "GetAllGfxAdapterDetails");
            functionPointer            = pfnGetAllGfxAdapterDetails;
        }
        else
        {
            functionPointer = pfnGetAllGfxAdapterDetails;
        }
        break;

    case GET_GFX_ADAPTER_INFO:
        if (NULL == pfnGetGfxAdapterInfo)
        {
            pfnGetGfxAdapterInfo = (PFN_GET_GFX_ADAPTER_INFO)GetProcAddress(dispConfigHandle, "GetGfxAdapterInfo");
            functionPointer      = pfnGetGfxAdapterInfo;
        }
        else
        {
            functionPointer = pfnGetGfxAdapterInfo;
        }
        break;
    case GET_DISPLAY_AND_ADAPTER_INFO:
        if (NULL == pfnGetDisplayAndAdapterInfo)
        {
            pfnGetDisplayAndAdapterInfo = (PFN_GET_DISPLAY_AND_ADAPTER_INFO)GetProcAddress(dispConfigHandle, "GetDisplayAndAdapterInfo");
            functionPointer             = pfnGetDisplayAndAdapterInfo;
        }
        else
        {
            functionPointer = pfnGetDisplayAndAdapterInfo;
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
    }
    return functionPointer;
}

VOID GetDisplayTimings(_In_ PDISPLAY_MODE pCurrentMode, _Out_ PDISPLAY_TIMINGS pDisplayTimings)
{
    memset(pDisplayTimings, 0, sizeof(PDISPLAY_TIMINGS));
    if (NULL == (PFN_GET_DISPLAY_TIMINGS)GetFunctionHandle(GET_DISPLAY_TIMINGS))
    {
        printf("Could't Get GetDisplayTimings Handle\n");
        return;
    }
    (pfnGetDisplayTimings)(pCurrentMode, pDisplayTimings);
}

VOID GetAPIVersion(_Inout_ PULONG pVersion)
{
    if (NULL == (PFN_GET_VERSION)GetFunctionHandle(GET_VERSION))
    {
        printf("Could't Get GetDisplayConfigInterfaceVersion Handle\n");
        return;
    }
    (pfnGetVersion)(pVersion);
}

VOID GetDisplayConfiguration(_Inout_ PDISPLAY_CONFIG pConfig)
{
    if (NULL == (PFN_GET_DISP_CONFIG)GetFunctionHandle(GET_DISPLAY_CONFIG))
    {
        printf("Could't Get GetDisplayConfiguration Handle\n");
        return;
    }
    pConfig->size = sizeof(DISPLAY_CONFIG);
    (pfnGetDisplayConfig)(pConfig);
}

VOID GetActiveDisplayConfiguration(_Out_ PACTIVE_DISPLAY_CONFIG pDisplayConfig)
{
    if (NULL == (PFN_GET_ACTIVE_DISPLAY_CONFIG)GetFunctionHandle(GET_ACTIVE_DISPLAY_CONFIG))
    {
        printf("Could't Get GetActiveDisplayConfiguration Handle\n");
        return;
    }
    pDisplayConfig->size = sizeof(PACTIVE_DISPLAY_CONFIG);
    (pfnGetActiveDisplayConfig)(pDisplayConfig);
}

VOID SetDisplayConfiguration(_Inout_ PDISPLAY_CONFIG pConfig)
{
    if (NULL == (PFN_SET_DISP_CONFIG)GetFunctionHandle(SET_DISPLAY_CONFIG))
    {
        printf("Could't Get SetDisplayConfiguration Handle\n");
        return;
    }
    pConfig->size = sizeof(DISPLAY_CONFIG);
    (pfnSetDisplayConfig)(pConfig);
    Sleep(2000);
}

VOID GetCurrentMode(_In_ PDISPLAY_AND_ADAPTER_INFO pDisplayAdapterId, _Out_ PDISPLAY_MODE pDisplayMode)
{
    memset(pDisplayMode, 0, sizeof(DISPLAY_MODE));
    if (NULL == (PFN_GET_CURRENT_MODE)GetFunctionHandle(GET_CURRENT_MODE))
    {
        printf("Could't Get GetCurrentMode Handle\n");
        return;
    }
    (pfnGetCurrentMode)(pDisplayAdapterId, pDisplayMode);
}

VOID GetAllSupportedModes(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayadapterId, _In_ BOOLEAN rotation_flag, _Out_ PENUMERATED_DISPLAY_MODES pEnumDisplayModes)
{
    if (NULL == (PFN_GET_SUPPORTED_MODES)GetFunctionHandle(GET_SUPPORTED_MODES))
    {
        printf("Could't Get GetAllSupportedModes Handle\n");
        return;
    }
    (pfnGetSupportedModes)(pdisplayadapterId, rotation_flag, pEnumDisplayModes);
}

VOID SetDisplayMode(_Inout_ PDISPLAY_MODE pModeList, _In_ BOOLEAN virtualModeSetAware, _In_ INT delayTime)
{
    if (NULL == (PFN_SET_DISP_MODE)GetFunctionHandle(SET_DISPLAY_MODE))
    {
        printf("Could't Get SetDisplayMode Handle\n");
    }
    (pfnSetDisplayMode)(pModeList, virtualModeSetAware, delayTime);
}

BOOLEAN GetOSPrefferedMode(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayadapterId, _Out_ PDISPLAY_TIMINGS pDisplayTimings)
{
    boolean result;
    if (NULL == (PFN_GET_OS_PREFFERED_MODE)GetFunctionHandle(GET_OS_PREFFERED_MODE))
    {
        printf("Could't Get GetOSPrefferedMode Handle\n");
        return FALSE;
    }
    result = (pfnGetOSPrefferedMode)(pdisplayadapterId, pDisplayTimings);
    return result;
}

VOID QueryDisplayConfigEx(_In_ UINT qdcflag, _In_ PDISPLAY_AND_ADAPTER_INFO pDisplayAdapterId, _Out_ PQUERY_DISPLAY_CONFIG pQueryDisplay)
{
    if (NULL == (PFN_QUERY_DISPLAY_CONFIG_EX)GetFunctionHandle(QUERY_DISPLAY_CONFIG_EX))
    {
        printf("Could't Get QueryDisplayConfig Handle\n");
    }
    (pfnQueryDisplayConfigEx)(qdcflag, pDisplayAdapterId, pQueryDisplay);
}

VOID GetAllGfxAdapterDetails(_Out_ PGFX_ADAPTER_DETAILS pAdapterDetails)
{
    if (NULL == (PFN_GET_ALL_GFX_ADAPTER)GetFunctionHandle(GET_ALL_GFX_ADAPTER))
    {
        printf("Could't Get GetAllGfxAdapter Handle\n");
    }
    (pfnGetAllGfxAdapterDetails)(pAdapterDetails);
}

BOOLEAN GetGfxAdapterInfo(_In_ PDISPLAY_AND_ADAPTER_INFO pdisplayadapterId, _Out_ PGFX_ADAPTER_INFO pAdapterInfo)
{
    boolean result;
    if (NULL == (PFN_GET_GFX_ADAPTER_INFO)GetFunctionHandle(GET_GFX_ADAPTER_INFO))
    {
        printf("Could't Get GetGfxAdapterInfo Handle\n");
    }
    result = (pfnGetGfxAdapterInfo)(pdisplayadapterId, pAdapterInfo);
    return result;
}

BOOLEAN GetDisplayAndAdapterInfo(_Inout_ PDISPLAY_AND_ADAPTER_INFO pDisplayAndAdapterInfo)
{
    boolean result;
    if (NULL == (PFN_GET_DISPLAY_AND_ADAPTER_INFO)GetFunctionHandle(GET_DISPLAY_AND_ADAPTER_INFO))
    {
        printf("Could't Get GetGfxAdapterInfo Handle\n");
    }
    result = (pfnGetDisplayAndAdapterInfo)(pDisplayAndAdapterInfo);
    return result;
}

VOID GetEnumeratedDisplayInfo(_Out_ PENUMERATED_DISPLAYS pEnumDisplay, _Out_ HRESULT *pErrorCode)
{
    if (NULL == (PFN_ENUMERATED_DISPLAYS_INFO)GetFunctionHandle(ENUMERATED_DISPLAYS_INFO))
    {
        printf("Could't Get GetAllGfxAdapter Handle\n");
    }
    (pfnGetEnumeratedDisplayInfo)(pEnumDisplay, *pErrorCode);
}

VOID Cleanup()
{
    if (NULL == (PFN_CLEANUP)GetFunctionHandle(CLEANUP))
    {
        printf("Could't Get Cleanup Handle\n");
    }
    (pfnCleanup)();
}
