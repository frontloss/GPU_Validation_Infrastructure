#ifndef __COMMONCORE_H__
#define __COMMONCORE_H__

#include "..\\CommonInclude\\DisplayDefs.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"

#define REGISTRY_PATH_LENGTH 128
#define SIMDRV_REGKEY_FEATURE_CONTROL L"FeatureControl"

/*
 * @brief        Interface to Get Gfx Registry
 * @param[in]    Registry Key Name
 * @param[in]    Registry Value Type (REG_DWORD, REG_BINARY etc)
 * @param[out]   Data buffer
 * @param[in]    Size of Registry Data
 * @return        NTSTATUS
 */
NTSTATUS COMMONCORE_GetRegistryInfo(PDDWSTR pRegKeyName, ULONG valueType, PVOID pValueData, ULONG valueLength);

/*
 * @brief        Interface to Write Set Registry
 * @param[in]    Registry Key Name
 * @param[in]    Registry Value Type (REG_DWORD, REG_BINARY etc)
 * @param[in]    Data buffer
 * @param[in]    Size of Registry Data
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_SetRegistryInfo(PDDWSTR pRegKeyName, ULONG valueType, PVOID pValueData, ULONG valueLength);

/*
 * @brief        Interface to Delete Set Registry
 * @param[in]    Registry Key Name
 * @return       NTSTATUS
 */
NTSTATUS COMMONCORE_DeleteRegistryInfo(PDDWSTR pRegKeyName);

/*
 * @brief        Interface to lock common resource for synchronization
 * @param[in]    Pointer to mutex object
 * @param[in]    Wait reason
 * @param[in]    Wait is alertable or not
 * @param[in]    Optional - pointer to a timeout value in 100ns
 * @return       NTSTATUS
 */
NTSTATUS AcquireLockToSerialize(PRKMUTEX pMutex, KWAIT_REASON waitReason, BOOLEAN alertable, PLARGE_INTEGER timeout OPTIONAL);

/*
 * @brief        Interface to release common resource
 * @param[in]    Pointer to mutex object
 * @param[in]    Wait reason
 * @return       NTSTATUS
 */
NTSTATUS ReleaseLockToSerialize(PRKMUTEX pMutex, BOOLEAN wait);

#endif