#include "CommonCore.h"
#include "..\\DriverInterfaces\SIMDRV_GFX_COMMON.h"
#include "..\\DriverInterfaces\SimDriver.h"
#include "..\\CommonInclude\\ETWLogging.h"

#pragma warning(disable : 4127)
#pragma warning(disable : 4100)
#pragma warning(disable : 4214)
#pragma warning(disable : 4201)

// This allows partial registry reads based on provided buffer size.
typedef struct _REGISTRY_BUFFER
{
    ULONG ulMaxValueLength;
    PVOID pvValueData;
} REGISTRY_BUFFER, *PREGISTRY_BUFFER;

/*
 * @brief        Sets registry ValueData for specified ValueName
 * @param[in]    Registry Key Name
 * @param[in]    Registry Value Type (REG_DWORD, REG_BINARY etc)
 * @param[out]   Data buffer
 * @param[in]    Size of Registry Data
 * @param[in]    Registry Read Context
 * @param[in]    Entry Context
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_cbGetRegistryInfo(IN PWSTR ValueName, IN ULONG ValueType, IN PVOID ValueData, IN ULONG ValueLength, IN PVOID Context, IN PVOID EntryContext)
{
    PREGISTRY_BUFFER pReadBuffer = (PREGISTRY_BUFFER)EntryContext;

    // Suported types
    switch (ValueType)
    {
    case REG_BINARY:
    case REG_DWORD:
    case REG_QWORD:
    case REG_SZ:
    case REG_EXPAND_SZ:
        break;

    default:
        return STATUS_INVALID_PARAMETER;
    }

    if (Context)
    {
        Context   = Context;
        ValueName = ValueName;
    }
    if (ValueLength == 0)
    {
        return STATUS_OBJECT_NAME_NOT_FOUND;
    }

    if (ValueData == NULL)
    {
        return STATUS_INVALID_PARAMETER;
    }

    //.Use the smaller length out of two: user-supplied (i.e. pReadBuffer->ulMaxValueLength) or OS-supplied (i.e. ValueLength).
    if ((pReadBuffer->ulMaxValueLength < ValueLength) && (pReadBuffer->ulMaxValueLength != 0))
    {
        if (0 != memcpy_s(pReadBuffer->pvValueData, pReadBuffer->ulMaxValueLength, ValueData, pReadBuffer->ulMaxValueLength))
        {
            return STATUS_INVALID_PARAMETER;
        }
    }
    else
    {
        if (0 != memcpy_s(pReadBuffer->pvValueData, ValueLength, ValueData, ValueLength))
        {
            return STATUS_INVALID_PARAMETER;
        }
    }

    return STATUS_SUCCESS;
}

/*
 * @brief        Delete Gfx Registry Access with legacy path
 * @param[in]    Registry Key Name
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_LegacyDeleteRegistryInfo(PDDWSTR pRegKeyName)

{
    UNICODE_STRING    uPath, uName;
    NTSTATUS          ntStatus = STATUS_UNSUCCESSFUL;
    HANDLE            hHandle  = NULL;
    OBJECT_ATTRIBUTES objAttribs;

    RtlInitUnicodeString(&uPath, SIMDRV_REG_PATH);
    RtlInitUnicodeString(&uName, pRegKeyName);

    do
    {
        InitializeObjectAttributes(&objAttribs, &uPath, OBJ_CASE_INSENSITIVE, NULL, NULL);

        // Open simulation driver registry path
        ntStatus = ZwOpenKey(&hHandle, KEY_WRITE, &objAttribs);

        if (NT_SUCCESS(ntStatus) == FALSE)
        {
            GFXVALSIM_DBG_MSG("Failed to get SimDriver regkey handle!");
            break;
        }

        // Update the Simulation mode in registry
        ntStatus = ZwDeleteValueKey(hHandle, &uName);

    } while (FALSE);

    if (NT_SUCCESS(ntStatus) == FALSE)
    {
        GFXVALSIM_DBG_MSG("DeleteRegistryInfoFromUnicodeString: Registry delete failed");
    }

    return ntStatus;
}

/*
 * @brief        Set Gfx Registry Access with legacy path
 * @param[in]    Registry Key Name
 * @param[in]    Registry Value Type (REG_DWORD, REG_BINARY etc)
 * @param[in]    Data buffer
 * @param[in]    Size of Registry Data
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_LegacySetRegistryInfo(PDDWSTR pRegKeyName, ULONG valueType, PVOID pValueData, ULONG valueLength)

{
    UNICODE_STRING    uPath, uName;
    NTSTATUS          ntStatus = STATUS_UNSUCCESSFUL;
    HANDLE            hHandle  = NULL;
    OBJECT_ATTRIBUTES objAttribs;

    RtlInitUnicodeString(&uPath, SIMDRV_REG_PATH);
    RtlInitUnicodeString(&uName, pRegKeyName);

    do
    {
        InitializeObjectAttributes(&objAttribs, &uPath, OBJ_CASE_INSENSITIVE, NULL, NULL);

        // Open simulation driver registry path
        ntStatus = ZwOpenKey(&hHandle, KEY_WRITE, &objAttribs);

        if (NT_SUCCESS(ntStatus) == FALSE)
        {
            break;
        }

        // Update the Simulation mode in registry
        ntStatus = ZwSetValueKey(hHandle, &uName, 0, valueType, pValueData, valueLength);

    } while (FALSE);

    if (NT_SUCCESS(ntStatus) == FALSE)
    {
        GFXVALSIM_DBG_MSG("SetRegistryInfoFromUnicodeString: Registry write failed");
    }

    return ntStatus;
}

/*
 * @brief        Get Gfx Registry Info with legacy path
 * @param[in]    Registry Key Name
 * @param[in]    Registry Value Type (REG_DWORD, REG_BINARY etc)
 * @param[out]   Data buffer
 * @param[in]    Size of Registry Data
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_LegacyGetRegistryInfo(PDDWSTR pRegKeyName, ULONG valueType, PVOID pValueData, ULONG valueLength)
{
    NTSTATUS                 ntStatus = STATUS_UNSUCCESSFUL;
    RTL_QUERY_REGISTRY_TABLE queryTable[2];
    REGISTRY_BUFFER          stReadBuffer = { 0 };
    UNICODE_STRING           pRegPath     = { 0 };

    pRegPath.Buffer        = SIMDRV_REG_PATH;
    pRegPath.Length        = REGISTRY_PATH_LENGTH;
    pRegPath.MaximumLength = (REGISTRY_PATH_LENGTH * 2);

    stReadBuffer.ulMaxValueLength = valueLength;
    stReadBuffer.pvValueData      = pValueData;

    switch (valueType)
    {
    case REG_BINARY:
    case REG_DWORD:
    case REG_QWORD:
    case REG_SZ:
    case REG_EXPAND_SZ:
        break;

    default:
        return ntStatus;
    }

    RtlZeroMemory(queryTable, 2 * sizeof(RTL_QUERY_REGISTRY_TABLE));

    queryTable[0].Flags         = RTL_QUERY_REGISTRY_REQUIRED;
    queryTable[0].Name          = (PWSTR)pRegKeyName;
    queryTable[0].EntryContext  = (PVOID)&stReadBuffer;
    queryTable[0].DefaultType   = REG_NONE;
    queryTable[0].DefaultLength = 0;
    queryTable[0].DefaultData   = NULL;
    queryTable[0].QueryRoutine  = COMMONCORE_cbGetRegistryInfo;

    ntStatus = RtlQueryRegistryValues(RTL_REGISTRY_ABSOLUTE, pRegPath.Buffer, queryTable, NULL, NULL);

    if (NT_SUCCESS(ntStatus) == FALSE)
    {
        GFXVALSIM_DBG_MSG("ExtReadRegistryValue: Registry Read failed");
    }

    return ntStatus;
}

/*
 * @brief        Gfx Registry Deletion with Driver Isolation and State Separation
 * @param[in]    Registry Key Name
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_DeleteStateSeparatedRegistryInfo(PDDWSTR pRegKeyName)
{
    NTSTATUS           ntStatus         = STATUS_UNSUCCESSFUL;
    PSIMDEV_EXTENTSION pSimDrvExtension = NULL;
    HANDLE             regKeyPathHandle = NULL;
    UNICODE_STRING     keyName;

    pSimDrvExtension = GetSimDrvExtension();
    if (NULL == pSimDrvExtension || NULL == pRegKeyName)
    {
        GFXVALSIM_DBG_MSG("pSimDrvExtension or pRegKeyName is NULL");
        return ntStatus;
    }
    ntStatus = IoOpenDeviceInterfaceRegistryKey(&pSimDrvExtension->SymbolicLink, KEY_WRITE, &regKeyPathHandle);
    if (NT_SUCCESS(ntStatus) == FALSE)
    {
        GFXVALSIM_DBG_MSG("Failed to open Device Interface for write event");
        return ntStatus;
    }
    RtlInitUnicodeString(&keyName, pRegKeyName);
    ntStatus = ZwDeleteValueKey(regKeyPathHandle, &keyName);
    ZwClose(regKeyPathHandle);
    return ntStatus;
}

/*
 * @brief        Gfx Registry Access with Driver Isolation and State Separation
 * @param[in]    Registry Key Name
 * @param[in]    Registry Value Type (REG_DWORD, REG_BINARY etc)
 * @param[in]    Data buffer
 * @param[in]    Size of Registry Data
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_SetStateSeparatedRegistryInfo(PDDWSTR pRegKeyName, ULONG valueType, PVOID pValueData, ULONG valueLength)
{
    NTSTATUS           ntStatus         = STATUS_UNSUCCESSFUL;
    PSIMDEV_EXTENTSION pSimDrvExtension = NULL;
    HANDLE             regKeyPathHandle = NULL;
    UNICODE_STRING     keyName;

    pSimDrvExtension = GetSimDrvExtension();
    if (NULL == pSimDrvExtension || NULL == pRegKeyName || NULL == pValueData)
    {
        GFXVALSIM_DBG_MSG("pSimDrvExtension or pRegKeyName or pValueData is NULL");
        return ntStatus;
    }
    ntStatus = IoOpenDeviceInterfaceRegistryKey(&pSimDrvExtension->SymbolicLink, KEY_WRITE, &regKeyPathHandle);
    if (NT_SUCCESS(ntStatus) == FALSE)
    {
        GFXVALSIM_DBG_MSG("Failed to open Device Interface for write event");
        return ntStatus;
    }
    RtlInitUnicodeString(&keyName, pRegKeyName);
    ntStatus = ZwSetValueKey(regKeyPathHandle, &keyName, 0, valueType, pValueData, valueLength);
    ZwClose(regKeyPathHandle);
    return ntStatus;
}

/*
 * @brief        Gfx Registry Access with Driver Isolation and State Separation
 * @param[in]    Registry Key Name
 * @param[in]    Registry Value Type (REG_DWORD, REG_BINARY etc)
 * @param[out]    Data buffer
 * @param[in]    Size of Registry Data
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_GetStateSeparatedRegistryInfo(PDDWSTR pRegKeyName, ULONG valueType, PVOID pValueData, ULONG valueLength)
{
    NTSTATUS                       ntStatus         = STATUS_UNSUCCESSFUL;
    PSIMDEV_EXTENTSION             pSimDrvExtension = NULL;
    PKEY_VALUE_PARTIAL_INFORMATION pKeyInformation  = NULL;
    HANDLE                         regKeyPathHandle = NULL;
    UNICODE_STRING                 keyName;
    ULONG                          resultLength;
    PPORTINGLAYER_OBJ              pstPortingObj = GetPortingObj();
    KIRQL                          kIrql         = KeGetCurrentIrql();
    if (PASSIVE_LEVEL != kIrql)
    {
        return ntStatus;
    }

    pSimDrvExtension = GetSimDrvExtension();
    if (NULL == pSimDrvExtension || NULL == pRegKeyName || NULL == pValueData)
    {
        GFXVALSIM_DBG_MSG("pSimDrvExtension or pRegKeyName or pValueData is NULL");
        return ntStatus;
    }
    ntStatus = IoOpenDeviceInterfaceRegistryKey(&pSimDrvExtension->SymbolicLink, KEY_READ, &regKeyPathHandle);
    if (NT_SUCCESS(ntStatus) == FALSE)
    {
        GFXVALSIM_DBG_MSG("Failed to open Device Interface for read event");
        return ntStatus;
    }
    pKeyInformation = pstPortingObj->pfnAllocateMem(sizeof(KEY_VALUE_PARTIAL_INFORMATION) + valueLength, TRUE);
    if (NULL == pKeyInformation)
    {
        GFXVALSIM_DBG_MSG("Failed to allocate memory for pKeyInformation object");
        ZwClose(regKeyPathHandle);
        return STATUS_NO_MEMORY;
    }

    RtlInitUnicodeString(&keyName, pRegKeyName);
    ntStatus = ZwQueryValueKey(regKeyPathHandle, &keyName, KeyValuePartialInformation, pKeyInformation, sizeof(KEY_VALUE_PARTIAL_INFORMATION) + valueLength, &resultLength);
    if (NT_SUCCESS(ntStatus))
    {
        DD_MEM_COPY_SAFE(pValueData, valueLength, &pKeyInformation->Data, valueLength);
    }
    pstPortingObj->pfnFreeMem(pKeyInformation);
    ZwClose(regKeyPathHandle);
    return ntStatus;
}

/*
 * @brief        Interface to Delete Set Registry
 * @param[in]    Registry Key Name
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_DeleteRegistryInfo(PDDWSTR pRegKeyName)
{
    NTSTATUS           ntStatus         = STATUS_UNSUCCESSFUL;
    PSIMDEV_EXTENTSION pSimDrvExtension = NULL;
    KIRQL              kIrql            = KeGetCurrentIrql();
    GFXVALSIM_FUNC_ENTRY();

    if (PASSIVE_LEVEL != kIrql)
    {
        return ntStatus;
    }

    pSimDrvExtension = GetSimDrvExtension();
    if (NULL == pSimDrvExtension || NULL == pRegKeyName)
    {
        GFXVALSIM_DBG_MSG("pSimDrvExtension or pRegKeyName is NULL");
        GFXVALSIM_FUNC_EXIT(ntStatus);
        return ntStatus;
    }

    if (STATE_SEPARATION_ENABLED(pSimDrvExtension->OsInfo.dwBuildNumber))
    {
        ntStatus = COMMONCORE_DeleteStateSeparatedRegistryInfo(pRegKeyName);
    }
    else
    {
        ntStatus = COMMONCORE_LegacyDeleteRegistryInfo(pRegKeyName);
    }

    GFXVALSIM_FUNC_EXIT(ntStatus == STATUS_SUCCESS);
    return ntStatus;
}

/*
 * @brief        Interface to Write Set Registry
 * @param[in]    Registry Key Name
 * @param[in]    Registry Value Type (REG_DWORD, REG_BINARY etc)
 * @param[in]    Data buffer
 * @param[in]    Size of Registry Data
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_SetRegistryInfo(PDDWSTR pRegKeyName, ULONG valueType, PVOID pValueData, ULONG valueLength)
{
    NTSTATUS           ntStatus         = STATUS_UNSUCCESSFUL;
    PSIMDEV_EXTENTSION pSimDrvExtension = NULL;
    KIRQL              kIrql            = KeGetCurrentIrql();
    if (PASSIVE_LEVEL != kIrql)
    {
        return ntStatus;
    }

    pSimDrvExtension = GetSimDrvExtension();
    if (NULL == pSimDrvExtension || NULL == pRegKeyName || NULL == pValueData)
        return ntStatus;
    if (STATE_SEPARATION_ENABLED(pSimDrvExtension->OsInfo.dwBuildNumber))
    {
        ntStatus = COMMONCORE_SetStateSeparatedRegistryInfo(pRegKeyName, valueType, pValueData, valueLength);
    }
    else
    {
        ntStatus = COMMONCORE_LegacySetRegistryInfo(pRegKeyName, valueType, pValueData, valueLength);
    }
    return ntStatus;
}

/*
 * @brief        Interface to Get Gfx Registry
 * @param[in]    Registry Key Name
 * @param[in]    Registry Value Type (REG_DWORD, REG_BINARY etc)
 * @param[out]   Data buffer
 * @param[in]    Size of Registry Data
 * @return        NTSTATUS
 */
NTSTATUS COMMONCORE_GetRegistryInfo(PDDWSTR pRegKeyName, ULONG valueType, PVOID pValueData, ULONG valueLength)
{
    NTSTATUS           ntStatus         = STATUS_UNSUCCESSFUL;
    PSIMDEV_EXTENTSION pSimDrvExtension = NULL;
    KIRQL              kIrql            = KeGetCurrentIrql();
    if (PASSIVE_LEVEL != kIrql)
    {
        return ntStatus;
    }

    pSimDrvExtension = GetSimDrvExtension();

    if (NULL == pSimDrvExtension || NULL == pRegKeyName || NULL == pValueData)
        return ntStatus;
    if (STATE_SEPARATION_ENABLED(pSimDrvExtension->OsInfo.dwBuildNumber))
    {
        ntStatus = COMMONCORE_GetStateSeparatedRegistryInfo(pRegKeyName, valueType, pValueData, valueLength);
    }
    else
    {
        ntStatus = COMMONCORE_LegacyGetRegistryInfo(pRegKeyName, valueType, pValueData, valueLength);
    }
    return ntStatus;
}

/*
 * @brief        Interface to lock common resource for synchronization
 * @param[in]    Pointer to mutex object
 * @param[in]    Wait reason
 * @param[in]    Wait is alertable or not
 * @param[in]    Optional - pointer to a timeout value in 100ns
 * @return       NTSTATUS
 */
NTSTATUS AcquireLockToSerialize(PRKMUTEX pMutex, KWAIT_REASON waitReason, BOOLEAN alertable, PLARGE_INTEGER timeout OPTIONAL)
{
    NTSTATUS ntStatus = STATUS_INVALID_PARAMETER;
    KIRQL    kIrql    = KeGetCurrentIrql();
    if (timeout != NULL && timeout->QuadPart == 0)
    {
        if (kIrql > DISPATCH_LEVEL)
            return STATUS_INVALID_LEVEL;
    }
    else
    {
        if (kIrql > APC_LEVEL)
            return STATUS_INVALID_LEVEL;
    }
    ntStatus = KeWaitForMutexObject(pMutex, waitReason, KernelMode, alertable, timeout);
    return ntStatus;
}

/*
 * @brief        Interface to release common resource
 * @param[in]    Pointer to mutex object
 * @param[in]    Wait reason
 * @return       NTSTATUS
 */
NTSTATUS ReleaseLockToSerialize(PRKMUTEX pMutex, BOOLEAN wait)
{
    KIRQL    kIrql    = KeGetCurrentIrql();
    NTSTATUS ntStatus = STATUS_INVALID_PARAMETER;
    LONG     lReturn  = -1;
    if (kIrql > DISPATCH_LEVEL)
        return STATUS_INVALID_LEVEL;
    lReturn  = KeReleaseMutex(pMutex, wait);
    ntStatus = (lReturn == 0) ? STATUS_SUCCESS : STATUS_UNSUCCESSFUL;
    return ntStatus;
}
