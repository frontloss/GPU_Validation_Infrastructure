/*------------------------------------------------------------------------------------------------*
 *
 * @file     DisplayEscape.c
 * @brief    This file contains Implementation of Internal APIs - GetD3DEscapeHandles, InvokeDriverEscape,
 *           TdrDriverEscape, GetGfxAdapterInfo
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "DriverEscape.h"
#include "..\Logger\ETWTestLogging.h"
#include <Utilities.h>

extern char *LIBRARY_NAME = "DriverEscape.dll";

static D3DKMT_ESCAPE_ARGS d3dkmtEscape = { 0 };

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           GetD3DEscapeHandles Helper Function (Internal API)
 * Description:                     This function returns the D3DKMT_ESCAPE_ARGS for the escape call.
 * @return D3DKMT_ESCAPE_ARGS       Returns the args after retrieving the handles
 *----------------------------------------------------------------------------------------------------------*/
D3DKMT_ESCAPE_ARGS GetD3DEscapeHandles()
{
    if (d3dkmtEscape.gdi32handle != NULL && d3dkmtEscape.pfnD3DKmtEscape != NULL && d3dkmtEscape.pfnCloseAdapter != NULL && d3dkmtEscape.pfnOpenAdapterFromLuid != NULL)
        return d3dkmtEscape;

    /* Load gdi32 library and proccess address for D3D KMT functions*/
    d3dkmtEscape.gdi32handle = LoadLibraryEx(GDI32_LIB, NULL, LOAD_LIBRARY_SEARCH_SYSTEM32);
    /* Get process handles to operate on for escape call*/
    d3dkmtEscape.pfnOpenAdapterFromLuid = (PFND3DKMT_OPENADAPTERFROMLUID)GetProcAddress(d3dkmtEscape.gdi32handle, "D3DKMTOpenAdapterFromLuid");
    d3dkmtEscape.pfnD3DKmtEscape        = (PFND3DKMT_ESCAPE)GetProcAddress(d3dkmtEscape.gdi32handle, "D3DKMTEscape");
    d3dkmtEscape.pfnCloseAdapter        = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(d3dkmtEscape.gdi32handle, "D3DKMTCloseAdapter");
    return d3dkmtEscape;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           InvokeDriverEscape (Internal API)
 * Description:                     This function Invokes Driver Escape based on header input <escapeOpCode>.
 * @param ADAPTER_INFO_GDI_NAME     _In_    pointer of _ADAPTER_INFO_GDI_NAME, It contains viewGDIDeviceName of the Respective Adapter
 * @param INT                       _In_    Size of ESC Data Structure
 * @param GFX_ESCAPE_HEADER_T       _In_    escapeOpCode Driver ESC Opcode
 * @param VOID                      _Out_   Pointer of Structure of required Data
 * @return BOOLEAN                  Returns TRUE on Success else FALSE on Failure
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN InvokeDriverEscape(_In_ ADAPTER_INFO_GDI_NAME *pAdapterInfoGdiName, _In_ INT escapeDataSize, _In_ GFX_ESCAPE_HEADER_T escapeOpCode, _Out_ void *pEscapeData)
{
    BOOLEAN                    status           = FALSE;
    NTSTATUS                   escapeStatus     = S_FALSE;
    D3DKMT_ESCAPE_ARGS         dedkmtEscapeArgs = { 0 };
    GFX_ESCAPE_HEADER_T        header           = { 0 };
    D3DKMT_ESCAPE              kmtEscape        = { 0 };
    D3DKMT_OPENADAPTERFROMLUID openAdapterLuid  = { 0 };
    D3DKMT_CLOSEADAPTER        closeAdapter     = { 0 };
    D3DKMT_HANDLE              hAdapter         = 0;

    /* Initailize variables*/
    PVOID  pLocal = NULL;
    HANDLE hLocal = NULL;

    NULL_PTR_CHECK(pAdapterInfoGdiName);
    NULL_PTR_CHECK(pEscapeData);

    do
    {
        /* Load gdi32 library and proccess address for D3D KMT functions, if not set*/
        dedkmtEscapeArgs = GetD3DEscapeHandles();

        if (dedkmtEscapeArgs.gdi32handle == NULL || dedkmtEscapeArgs.pfnOpenAdapterFromLuid == NULL || dedkmtEscapeArgs.pfnD3DKmtEscape == NULL ||
            dedkmtEscapeArgs.pfnCloseAdapter == NULL)
        {
            ERROR_LOG("GetD3DEscapeHandles is NULL");
            break;
        }

        openAdapterLuid.AdapterLuid = pAdapterInfoGdiName->adapterID;
        if (S_OK != d3dkmtEscape.pfnOpenAdapterFromLuid(&openAdapterLuid))
        {
            ERROR_LOG("Failed to identify adapter device name for gfx_index : %ls", pAdapterInfoGdiName->adapterInfo.gfxIndex);
            break;
        }

        hAdapter = openAdapterLuid.hAdapter;
        if (0 == hAdapter)
        {
            ERROR_LOG("Found no adapter handle.");
            break;
        }

        hLocal = GlobalAlloc(GHND, escapeDataSize + sizeof(GFX_ESCAPE_HEADER_T));
        if (NULL == hLocal)
        {
            ERROR_LOG("GlobalAlloc is NULL");
            break;
        }

        pLocal = GlobalLock(hLocal);
        if (NULL == pLocal)
        {
            ERROR_LOG("GlobalLock is NULL");
            break;
        }

        /* Prepare Escape header*/
        kmtEscape.hAdapter           = hAdapter;
        kmtEscape.Type               = D3DKMT_ESCAPE_DRIVERPRIVATE;
        kmtEscape.pPrivateDriverData = pLocal;
        if (NULL == kmtEscape.pPrivateDriverData)
        {
            ERROR_LOG("Memory Allocation is NULL");
            break;
        }
        kmtEscape.PrivateDriverDataSize = escapeDataSize + sizeof(GFX_ESCAPE_HEADER_T);

        ///* Set header with the escape request type*/
        header.minorInterfaceVersion = escapeOpCode.minorInterfaceVersion;
        header.majorEscapeCode       = escapeOpCode.majorEscapeCode;
        header.minorEscapeCode       = escapeOpCode.minorEscapeCode;
        header.majorInterfaceVersion = escapeOpCode.majorInterfaceVersion;

        memcpy(kmtEscape.pPrivateDriverData, &header, sizeof(GFX_ESCAPE_HEADER_T));

        /* Fill escape header with the details*/
        PVOID pOutData = (PCHAR)kmtEscape.pPrivateDriverData + sizeof(GFX_ESCAPE_HEADER_T);
        memcpy(pOutData, pEscapeData, escapeDataSize);

        /* Make a driver Escape call*/
        escapeStatus = dedkmtEscapeArgs.pfnD3DKmtEscape(&kmtEscape);
        if (S_OK == escapeStatus)
        {
            status = TRUE;
            memcpy(pEscapeData, pOutData, escapeDataSize);
        }
        else
            ERROR_LOG("InvokeDriverEscape failed for minorEscapeCode= %d and majorEscapeCode=%d with error - %ld", escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode,
                      escapeStatus);

    } while (FALSE);

    if (0 != hAdapter)
    {
        closeAdapter.hAdapter = hAdapter;
        if (S_OK != d3dkmtEscape.pfnCloseAdapter(&closeAdapter))
        {
            ERROR_LOG("Failed to close adapter!!");
        }
    }

    /* Release handles and heap variables*/
    if (hLocal != NULL)
    {
        GlobalUnlock(hLocal);
        GlobalFree(hLocal);
    }

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               TdrDriverEscape (Internal API)
 * Description          This function invokes D3D TDR Driver Escape
 * @param[In]           pAdapterInfo (Pointer to GFX_ADAPTER_INFO structure)
 * @param[In]           displayTdr (To specify VSYNC TDR or KMD TDR)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN TdrDriverEscape(_In_ ADAPTER_INFO_GDI_NAME *pAdapterInfoGdiName, _In_ BOOLEAN displayTdr)
{
    BOOLEAN                    status           = FALSE;
    D3DKMT_ESCAPE_ARGS         dedkmtEscapeArgs = { 0 };
    D3DKMT_ESCAPE              kmtEscape        = { 0 };
    D3DKMT_OPENADAPTERFROMLUID openAdapterLuid  = { 0 };
    D3DKMT_CLOSEADAPTER        closeAdapter     = { 0 };
    D3DKMT_HANDLE              hAdapter         = 0;
    ULONG                      escapeDataSize   = sizeof(D3DKMT_ESCAPE_TDRDBGCTRL);

    /* Initailize variables*/
    PVOID  pLocal = NULL;
    HANDLE hLocal = NULL;

    NULL_PTR_CHECK(pAdapterInfoGdiName);

    do
    {
        /* Load gdi32 library and proccess address for D3D KMT functions, if not set*/
        dedkmtEscapeArgs = GetD3DEscapeHandles();

        if (dedkmtEscapeArgs.gdi32handle == NULL || dedkmtEscapeArgs.pfnOpenAdapterFromLuid == NULL || dedkmtEscapeArgs.pfnD3DKmtEscape == NULL ||
            dedkmtEscapeArgs.pfnCloseAdapter == NULL)
        {
            ERROR_LOG("Failed to get GetD3DEscapeHandles");
            break;
        }

        openAdapterLuid.AdapterLuid = pAdapterInfoGdiName->adapterID;
        if (S_OK != d3dkmtEscape.pfnOpenAdapterFromLuid(&openAdapterLuid))
        {
            ERROR_LOG("Failed to identify adapter device name for gfx_index : %ls", pAdapterInfoGdiName->adapterInfo.gfxIndex);
            break;
        }

        hAdapter = openAdapterLuid.hAdapter;
        if (0 == hAdapter)
        {
            ERROR_LOG("Found no adapter handle.");
            break;
        }

        hLocal = GlobalAlloc(GHND, escapeDataSize);
        if (NULL == hLocal)
        {
            ERROR_LOG("GlobalAlloc is NULL");
            break;
        }

        pLocal = GlobalLock(hLocal);
        if (NULL == pLocal)
        {
            ERROR_LOG("GlobalLock is NULL");
            break;
        }

        /* Prepare Escape header*/
        kmtEscape.hAdapter              = hAdapter;
        kmtEscape.Type                  = D3DKMT_ESCAPE_TDRDBGCTRL;
        kmtEscape.pPrivateDriverData    = pLocal;
        kmtEscape.PrivateDriverDataSize = escapeDataSize;

        if (displayTdr == TRUE)
        {
            EtwTdrEscape(pAdapterInfoGdiName->adapterInfo.deviceID, pAdapterInfoGdiName->adapterInfo.deviceInstanceID, D3DKMT_TDRDBGCTRLTYPE_VSYNCTDR);
            (*(int *)kmtEscape.pPrivateDriverData) = D3DKMT_TDRDBGCTRLTYPE_VSYNCTDR;
        }
        else
        {
            EtwTdrEscape(pAdapterInfoGdiName->adapterInfo.deviceID, pAdapterInfoGdiName->adapterInfo.deviceInstanceID, D3DKMT_TDRDBGCTRLTYPE_FORCETDR);
            (*(int *)kmtEscape.pPrivateDriverData) = D3DKMT_TDRDBGCTRLTYPE_FORCETDR;
        }

        /* Make a driver Escape call*/
        if (S_OK == dedkmtEscapeArgs.pfnD3DKmtEscape(&kmtEscape))
        {
            status = TRUE;
        }
        else
            ERROR_LOG("InvokeDriverEscape failed with error");
    } while (FALSE);

    /* Release all memory*/
    if (0 != hAdapter)
    {
        closeAdapter.hAdapter = hAdapter;
        if (S_OK != d3dkmtEscape.pfnCloseAdapter(&closeAdapter))
        {
            ERROR_LOG("Failed to close adapter!!");
        }
    }

    /* Release handles and heap variables*/
    if (hLocal != NULL)
    {
        GlobalUnlock(hLocal);
        GlobalFree(hLocal);
    }

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           SplitString Helper Function (Internal API)
 * Description      Function to tokenize Device Instance Path and assign corresponding IDs
 * @param [In]      string (pointer to WCHAR - String to be tokenized)
 * @param [In]      delimiter (const pointer to WCHAR - identifier with which tokens are generated)
 * @param [In]      buffer (2D array of WCHAR - remaining of the tokenized string is present)
 * return: VOID     None
 *----------------------------------------------------------------------------------------------------------*/
VOID SplitString(_In_ WCHAR *string, _In_ const WCHAR *delimiter, _In_ WCHAR buffer[][MAX_DEVICE_ID_LEN])
{
    WCHAR  tempstring[MAX_DEVICE_ID_LEN];
    int    index = 0;
    WCHAR *p     = 0;
    memset(tempstring, 0, sizeof(tempstring));
    memset(buffer, 0, sizeof(buffer));

    CopyWchar(tempstring, _countof(tempstring), string);
    WCHAR *token = wcstok_s(tempstring, delimiter, &p);
    while (token != NULL)
    {
        memcpy(buffer[index++], token, (wcslen(token) * sizeof(WCHAR)));
        token = wcstok_s(NULL, delimiter, &p);
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               GetGFXAdapterInfo (Internal API)
 * Description          Function to get GetGfxAdapterInfo and ViewGdiDeviceName for given Source ID and Adapter ID.
 *                      To Get Adapter ID for given Adapter Info - use other Function ( GetAdapterDetails )
 *                      This function is used mainly when we have to make Driver escape call which operates based on both Display and Adapter info.
 * @param [In]          UINT32 sourceID
 * @param [InOut]       ADAPTER_INFO_GDI_NAME pInternalAdapterInfo
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetGfxAdapterInfo(_In_ UINT32 sourceID, _Inout_ ADAPTER_INFO_GDI_NAME *pInternalAdapterInfo)
{
    BOOLEAN                          status = FALSE;
    ULONG                            instanceInfoRet;
    SIZE_T                           ven_index      = 0;
    SIZE_T                           devId_index    = 0;
    SIZE_T                           instance_index = 0;
    DWORD                            devId          = 0;
    ULONG                            deviceInfoRet;
    DISPLAYCONFIG_ADAPTER_NAME       instanceInfo;
    DISPLAYCONFIG_SOURCE_DEVICE_NAME deviceInfo; // This initialize is used for to find Source Device Name (Ex: \\.\DISPLAY1)
    DISPLAY_DEVICE                   deviceName;
    WCHAR                            adapterDevicePath[MAX_DEVICE_ID_LEN];
    deviceName.cb = sizeof(DISPLAY_DEVICE);

    // Initialize deviceInfo Header to find Source Device Name (Which is required for getting Handle in Driver ESC)
    ZeroMemory(&deviceInfo, sizeof(DISPLAYCONFIG_SOURCE_DEVICE_NAME));
    deviceInfo.header.size      = sizeof(DISPLAYCONFIG_SOURCE_DEVICE_NAME);
    deviceInfo.header.type      = DISPLAYCONFIG_DEVICE_INFO_GET_SOURCE_NAME;
    deviceInfo.header.id        = sourceID;
    deviceInfo.header.adapterId = pInternalAdapterInfo->adapterID;

    // Initialize instanceInfo Header to find Adapter Device Name (Which is required to get Device InstanceID)
    ZeroMemory(&instanceInfo, sizeof(DISPLAYCONFIG_ADAPTER_NAME));
    instanceInfo.header.size      = sizeof(DISPLAYCONFIG_ADAPTER_NAME);
    instanceInfo.header.type      = DISPLAYCONFIG_DEVICE_INFO_GET_ADAPTER_NAME;
    instanceInfo.header.id        = sourceID;
    instanceInfo.header.adapterId = pInternalAdapterInfo->adapterID;

    deviceInfoRet   = DisplayConfigGetDeviceInfo(&deviceInfo.header);
    instanceInfoRet = DisplayConfigGetDeviceInfo(&instanceInfo.header);

    if (S_OK == deviceInfoRet)
    {
        devId = 0;
        /* Get Device Hardware ID for given Target ID. Cannot map Target ID and Hardware ID directly, hence find DISPLAYCONFIG_SOURCE_DEVICE_NAME and Map with
         EnumDisplayDevices's Device Name and get respective Hardware/Device ID. */
        while (EnumDisplayDevices(NULL, devId++, &deviceName, 0)) // DISPLAY_DEVICE_ATTACHED_TO_DESKTOP
        {
            if (wcscmp((wchar_t *)deviceName.DeviceName, deviceInfo.viewGdiDeviceName) == S_OK)
            {
                WCHAR tempDevInstance[MAX_DEVICE_ID_LEN];
                WCHAR tempvendorID[MAX_DEVICE_ID_LEN];
                WCHAR tempdeviceID[MAX_DEVICE_ID_LEN];
                WCHAR buffer[6][MAX_DEVICE_ID_LEN];
                memset(buffer, 0, sizeof(buffer));
                memset(adapterDevicePath, 0, sizeof(adapterDevicePath));

                CopyWchar(adapterDevicePath, _countof(adapterDevicePath), instanceInfo.adapterDevicePath);
                SplitString(adapterDevicePath, L"#", buffer);

                CopyWchar(pInternalAdapterInfo->adapterInfo.deviceInstanceID, _countof(pInternalAdapterInfo->adapterInfo.deviceInstanceID), buffer[2]); // Set device Instance ID
                CopyWchar(tempDevInstance, _countof(tempDevInstance), buffer[1]); // copy VEN_8086&DEV_5916&SUBSYS_079F1028&REV_02 to tempDevInstance

                memset(buffer, 0, sizeof(buffer));
                SplitString(tempDevInstance, L"&", buffer);

                CopyWchar(tempvendorID, _countof(tempvendorID), buffer[0]); // copy VEN_8086 to tempvendorID
                CopyWchar(tempdeviceID, _countof(tempdeviceID), buffer[1]); // copy VEN_8086 to tempdeviceID

                memset(buffer, 0, sizeof(buffer));
                SplitString(tempvendorID, L"_", buffer);
                CopyWchar(pInternalAdapterInfo->adapterInfo.vendorID, _countof(pInternalAdapterInfo->adapterInfo.vendorID), buffer[1]); // Set vendor ID

                memset(buffer, 0, sizeof(buffer));
                SplitString(tempdeviceID, L"_", buffer);
                CopyWchar(pInternalAdapterInfo->adapterInfo.deviceID, _countof(pInternalAdapterInfo->adapterInfo.deviceID), buffer[1]); // Set device ID

                CopyWchar(pInternalAdapterInfo->adapterInfo.busDeviceID, _countof(pInternalAdapterInfo->adapterInfo.busDeviceID), deviceName.DeviceID);
                CopyWchar(pInternalAdapterInfo->viewGdiDeviceName, _countof(pInternalAdapterInfo->viewGdiDeviceName), deviceInfo.viewGdiDeviceName);

                pInternalAdapterInfo->adapterInfo.adapterLUID = pInternalAdapterInfo->adapterID;
                pInternalAdapterInfo->adapterInfo.isActive    = TRUE;
                status                                        = TRUE;
            }
        }
    }
    else
    {
        ERROR_LOG("Failed to get Adapter Info with error status : %lu", deviceInfoRet);
    }
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               GetAdapterDetails (Internal API)
 * Description          This function is used to get AdapterID which is unique identifier (LUID) and viewGDIDeviceName that identifies the adapter.
 *                      This function is used mainly when we have to make Driver escape call which operates based on Adpater Information.
 * @param [InOut]       pInternalAdapterInfo (POINTER to _ADAPTER_INFO_GDI_NAME Structure)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetAdapterDetails(_Inout_ ADAPTER_INFO_GDI_NAME *pInternalAdapterInfo)
{
    BOOLEAN                  retStatus = FALSE;
    LONG                     status;
    UINT                     flags;
    UINT32                   numPathArrayElements     = 0;
    UINT32                   numModeInfoArrayElements = 0;
    DISPLAYCONFIG_PATH_INFO *pPathInfoArray           = NULL;
    DISPLAYCONFIG_MODE_INFO *pModeInfoArray           = NULL;
    ADAPTER_INFO_GDI_NAME    adapterInfoGdiName       = { 0 };
    /* Initialize the AdapterFound Flag*/
    BOOLEAN bAdapterFound = FALSE;

    do
    {
        /* This Flag provides data about both active and inactive display path */
        flags = QDC_ALL_PATHS;

        /* Get Path Array buffer size and Mode array buffer size through OS API. */
        status = GetDisplayConfigBufferSizes(flags, &numPathArrayElements, &numModeInfoArrayElements);

        if (ERROR_SUCCESS != status)
        {
            ERROR_LOG("Get PathArray and ModeArray Buffer Size Failed with status code %d", status);
            break;
        }

        /* Allocate Buffer for QueryDisplayConfig */
        pPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, (sizeof(DISPLAYCONFIG_PATH_INFO)));
        pModeInfoArray = (DISPLAYCONFIG_MODE_INFO *)calloc(numModeInfoArrayElements, (sizeof(DISPLAYCONFIG_MODE_INFO)));

        if (NULL == pPathInfoArray || NULL == pModeInfoArray)
        {
            ERROR_LOG("PathArray and ModeArray Memory Allocation is Null");
            break;
        }

        /* Windows API which retrieves information about all possible display paths for all display devices */
        status = QueryDisplayConfig(flags, &numPathArrayElements, pPathInfoArray, &numModeInfoArrayElements, pModeInfoArray, NULL);

        if (ERROR_SUCCESS != status)
        {
            ERROR_LOG("QueryDisplayConfig Failed with Error Code: %d", status);
            break;
        }

        int  eleminated_adapterID_count                 = 0;
        LUID eleminated_adapterID_list[MAX_GFX_ADAPTER] = { 0 };

        /* Step-1 First check whether you have matching Adapter ID - for a given AdapterInfo/
        /* if we get matching one - break the loop and return*/
        /* if it is NOT matching - add that Adapter ID to Eleminated adapter ID List , So that for next path if we see same Adapter ID - we can move on next path*/
        /* instead of calling  GetGfxAdapterInfo() for each path */
        /* this optimization is needed since we have used QDC with All path flag - which will have generally more path information details 100 + active / Inactive path */
        for (UINT pathIndex = 0; pathIndex < numPathArrayElements; pathIndex++)
        {
            BOOLEAN eleminated_adapterID_found = FALSE;
            for (int i = 0; i < eleminated_adapterID_count; i++)
            {
                if (eleminated_adapterID_list[i].HighPart == pPathInfoArray[pathIndex].targetInfo.adapterId.HighPart &&
                    eleminated_adapterID_list[i].LowPart == pPathInfoArray[pathIndex].targetInfo.adapterId.LowPart)
                {
                    eleminated_adapterID_found = TRUE;
                    break;
                }
            }
            if (TRUE == eleminated_adapterID_found)
            {
                continue;
            }
            /* Getting the AdapterInfo for each path source id and adapter id*/
            adapterInfoGdiName.adapterID = pPathInfoArray[pathIndex].targetInfo.adapterId;
            retStatus                    = GetGfxAdapterInfo(pPathInfoArray[pathIndex].sourceInfo.id, &adapterInfoGdiName);
            if (TRUE == retStatus)
            {
                /* compare the whole instance path of adapterinfo */
                if ((0 == _wcsicmp(pInternalAdapterInfo->adapterInfo.busDeviceID, adapterInfoGdiName.adapterInfo.busDeviceID)) &&
                    (0 == _wcsicmp(pInternalAdapterInfo->adapterInfo.deviceInstanceID, adapterInfoGdiName.adapterInfo.deviceInstanceID)))
                {
                    bAdapterFound                   = TRUE;
                    pInternalAdapterInfo->adapterID = pPathInfoArray[pathIndex].targetInfo.adapterId;
                    CopyWchar(pInternalAdapterInfo->viewGdiDeviceName, _countof(adapterInfoGdiName.viewGdiDeviceName), adapterInfoGdiName.viewGdiDeviceName);
                    break;
                }
                else
                {
                    eleminated_adapterID_list[eleminated_adapterID_count] = pPathInfoArray[pathIndex].targetInfo.adapterId;
                    eleminated_adapterID_count++;
                }
            }
        }
        if (FALSE == bAdapterFound)
        {
            ERROR_LOG("AdapterID Not Found for given AdapterInformation Bus deviceID: %ls and InstanceId: %ls", pInternalAdapterInfo->adapterInfo.busDeviceID,
                      pInternalAdapterInfo->adapterInfo.deviceInstanceID);
        }
    } while (FALSE);
    /* Cleanup Dynamic Allocated Memory */
    free(pPathInfoArray);
    free(pModeInfoArray);
    return bAdapterFound;
}
