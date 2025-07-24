/**
* @file
* @section OsInterface
* @brief Internal source file which contains implementation required for getting information related to
                  ReadRegistry, WriteRegistry, DeleteRegistry,
                  GetExecutionEnvironmentDetails
*
* @ref RegistryAccess.c
*
*/

/***********************************************************************************************
 * INTEL CONFIDENTIAL. Copyright (c) 2020 Intel Corporation All Rights Reserved.
 *  <br>The source code contained or described herein and all documents related to the source code
 *  ("Material") are owned by Intel Corporation or its suppliers or licensors. Title to the
 *  Material remains with Intel Corporation or its suppliers and licensors. The Material contains
 *  trade secrets and proprietary and confidential information of Intel or its suppliers and licensors.
 *  The Material is protected by worldwide copyright and trade secret laws and treaty provisions.
 *  No part of the Material may be used, copied, reproduced, modified, published, uploaded, posted,
 *  transmitted, distributed, or disclosed in any way without Intel's prior express written permission.
 *  <br>No license under any patent, copyright, trade secret or other intellectual property right is
 *  granted to or conferred upon you by disclosure or delivery of the Materials, either expressly,
 *  by implication, inducement, estoppel or otherwise. Any license under such intellectual property
 *  rights must be express and approved by Intel in writing.
 */

/* Avoid multi inclusion of header file*/
#pragma once

/* User defined header(s)*/
#include "wchar.h"
#include "../HeaderFiles/RegistryAccess.h"
#include <initguid.h>
#include <devpkey.h>
#include <devguid.h>

/**---------------------------------------------------------------------------------------------------------*
 * @brief        Checks if s1 is substring of s2 (Internal API)
 * @param[in]    s1 first string
 * @param[in]    s2 second string
 * @return       BOOL True on success otherwise False
 *----------------------------------------------------------------------------------------------------------*/
BOOL IsSubstringOf(_In_ PWCHAR s1, _In_ PWCHAR s2)
{
    s1       = _wcslwr(s1);
    s2       = _wcslwr(s2);
    size_t M = wcslen(s1);
    size_t N = wcslen(s2);

    /* A loop to slide pat[] one by one */
    for (int i = 0; i <= N - M; i++)
    {
        int j;

        /* For current index i, check for pattern match */
        for (j = 0; j < M; j++)
            if (s2[i + j] != s1[j])
                break;

        if (j == M)
            return TRUE;
    }
    return FALSE;
}

/* Function implementation*/

/**---------------------------------------------------------------------------------------------------------*
 * @brief           GetRegKeyHandle (Exposed API)
 * Description      This function returns a RegKey Handle to caller for a given adapter
 * @param[In]       deviceID (wchar string of adapter Device ID)
 * @param[In]       deviceInstanceID (wchar string of adapter Device Instance ID)
 * @param[In]       filterType (Flags for CM_Get_Device_ID_List, CM_Get_Device_ID_List_Size [CM_GETIDLIST_FILTER_CLASS/CM_GETIDLIST_FILTER_SERVICE])
 * @param[In]       keyType (Registry Branch Locations for CM_Open_DevNode_Key [CM_REGISTRY_SOFTWARE/CM_REGISTRY_HARDWARE])
 * @param[Out]      pHKey (PVOID - Void Pointer for passing the Handle)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOL GetRegKeyHandle(_In_ WCHAR deviceID[], _In_ WCHAR deviceInstanceID[], _In_ GUID guid, _In_ ULONG filterType, _In_ UINT keyType, _Out_ PVOID pHKey)
{
    BOOL        status           = FALSE;
    PWSTR       deviceList       = NULL;
    ULONG       deviceListLength = 0;
    ULONG       errorCode        = 0;
    PWSTR       currentDevice;
    DEVINST     devInstance;
    ULONG       propertySize;
    DEVPROPTYPE propertyType;
    WCHAR       deviceDesc[2048];
    OLECHAR     GUID_STRING[MAX_GUID_STRING_LEN];

    do
    {
        if (wcslen(deviceID) == 0 || wcslen(deviceInstanceID) == 0)
        {
            ERROR_LOG("DeviceID or DeviceInstanceID is empty");
            break;
        }
        if (StringFromGUID2(&guid, GUID_STRING, MAX_GUID_STRING_LEN) == 0)
            ERROR_LOG("Buffer too small to fill GUID");
        DEBUG_LOG("Fetching RegKey Handle for Adapter with deviceID: %ls, devInstID: %ls", deviceID, deviceInstanceID);

        VERIFY_REG_KEY_HANDLE_STATUS(CM_Get_Device_ID_List_Size(&deviceListLength, GUID_STRING, filterType));

        deviceList = (PWSTR)malloc((deviceListLength * 2) * sizeof(WCHAR));
        NULL_PTR_CHECK(deviceList);

        VERIFY_REG_KEY_HANDLE_STATUS(CM_Get_Device_ID_List(GUID_STRING, deviceList, deviceListLength, filterType));

        for (currentDevice = deviceList; *currentDevice; currentDevice += wcslen(currentDevice) + 1)
        {
            errorCode = CM_Locate_DevNode(&devInstance, currentDevice, CM_LOCATE_DEVNODE_NORMAL);
            if (errorCode != ERROR_SUCCESS)
                continue;

            propertySize = sizeof(deviceDesc);
            errorCode    = CM_Get_DevNode_Property(devInstance, &DEVPKEY_Device_InstanceId, &propertyType, (PBYTE)deviceDesc, &propertySize, 0);
            if (errorCode != ERROR_SUCCESS)
                continue;

            if (IsSubstringOf(deviceID, deviceDesc) && IsSubstringOf(deviceInstanceID, deviceDesc))
            {
                VERIFY_REG_KEY_HANDLE_STATUS(CM_Open_DevNode_Key(devInstance, KEY_ALL_ACCESS, 0, RegDisposition_OpenExisting, pHKey, keyType));
                status = TRUE;
                break;
            }
        }
    } while (FALSE);

    free(deviceList);
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           GetSimDrvRegKeyHandle (Exposed API)
 * Description      This function returns a RegKey Handle to caller for ValSim instance
 * @param[Out]      pHKey (PVOID - Void Pointer for fetching the Handle)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOL GetSimDrvRegKeyHandle(_Out_ PVOID pHKey)
{
    BOOL    status           = FALSE;
    PZZWSTR deviceList       = NULL;
    ULONG   deviceListLength = 0;
    PZZWSTR currentDevice;

    do
    {
        VERIFY_REG_KEY_HANDLE_STATUS(CM_Get_Device_Interface_List_Size(&deviceListLength, (GUID *)&SIMDRV_INTERFACE_GUID, NULL, CM_GET_DEVICE_INTERFACE_LIST_ALL_DEVICES));

        if (deviceListLength <= 1)
        {
            DEBUG_LOG("No devices available with SimDriver GUID ");
            break;
        }

        deviceList = (PZZWSTR)malloc((deviceListLength * 2) * sizeof(WCHAR));
        NULL_PTR_CHECK(deviceList);

        VERIFY_REG_KEY_HANDLE_STATUS(CM_Get_Device_Interface_List((GUID *)&SIMDRV_INTERFACE_GUID, NULL, deviceList, deviceListLength, CM_GET_DEVICE_INTERFACE_LIST_ALL_DEVICES));

        for (currentDevice = deviceList; *currentDevice; currentDevice += wcslen(currentDevice) + 1)
        {
            // Query a property on the device.
            VERIFY_REG_KEY_HANDLE_STATUS(CM_Open_Device_Interface_Key((LPCWSTR)currentDevice, KEY_ALL_ACCESS, RegDisposition_OpenAlways, (PHKEY)pHKey, 0));
            status = TRUE;
            break;
        }
    } while (FALSE);

    free(deviceList);
    return status;
}