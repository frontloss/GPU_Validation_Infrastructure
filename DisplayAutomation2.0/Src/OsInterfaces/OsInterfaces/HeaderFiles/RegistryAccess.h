#pragma once
#include <windows.h>
#include "DisplayEscape.h"
#include "CommonInclude.h"
#include "cfgmgr32.h"

// ValSim interface GUID definition
static const GUID SIMDRV_INTERFACE_GUID = { 0xa9cd4d20, 0xccb8, 0x414f, 0xb0, 0x35, 0x82, 0x7a, 0x4, 0x2e, 0x6, 0x87 };

/**
 * @brief         Macro for verifying registry access status
 * @param[in]     Registry Access Status Code
 * @return        Return on registry access failure
 */
#define REGISTRY_ACCESS_STATUS_CHECK(statusCode) \
    {                                            \
        if (0 != statusCode)                     \
            return statusCode;                   \
    }

#define VERIFY_REG_KEY_HANDLE_STATUS(errorcode)                                  \
    {                                                                            \
        if (CR_SUCCESS != errorcode)                                             \
        {                                                                        \
            ERROR_LOG("Failed to get RegKey handle with error: %ld", errorcode); \
            return FALSE;                                                        \
        }                                                                        \
    }

/* Registry Values in winnt.h */
typedef enum _REGISTRY_TYPES
{
    REGISTRY_BINARY = 3,
    REGISTRY_DWORD  = 4,
    REGISTRY_MAX    = 5,
} REGISTRY_TYPES;

/* sructure definition for audio controller type*/
typedef enum AUDIO_CONTROLLER_TYPE
{
    INTEL_AUDIO_CONTROLLER = 1,
    MS_AUDIO_CONTROLLER    = 2
} AUDIO_CONTROLLER_TYPE;

/* Internal & Exposed function*/
CDLL_EXPORT BOOL GetRegKeyHandle(_In_ WCHAR deviceID[], _In_ WCHAR deviceInstanceID[], _In_ GUID guid, _In_ ULONG filterType, _In_ UINT keyType, _Out_ PVOID pHKey);

CDLL_EXPORT BOOL GetSimDrvRegKeyHandle(_Out_ PVOID pHKey);
