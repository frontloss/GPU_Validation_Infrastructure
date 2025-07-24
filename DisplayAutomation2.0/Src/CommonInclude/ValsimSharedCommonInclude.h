/*------------------------------------------------------------------------------------------------*
 *
 * @file     ValsimSharedCommonInclude.h
 * @brief    Contains Structure of _GFX_ADAPTER_INFO shared between valsim and application.
 *
 * @author   Chandrakanth, Pabolu; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#ifdef __KERNELMODE
#include "ntdef.h"
#define MAX_DEVICE_ID_LEN 200
#else
#include "Windows.h"
#include "cfgmgr32.h"
#endif // __KERNELMODE

#include <stdbool.h>

#define MAX_GFX_ADAPTER 5

#pragma pack(1)

typedef struct _GFX_ADAPTER_INFO
{
    WCHAR busDeviceID[MAX_DEVICE_ID_LEN];      // Bus DeviceID (Ex: PCI\VEN_8086&DEV_0166&SUBSYS_21F917AA&REV_09\3&33FD14CA&0&10)
    WCHAR vendorID[6];                         // GFX Adapter Vendor ID
    WCHAR deviceID[6];                         // GFX Adapter Device ID
    WCHAR deviceInstanceID[MAX_DEVICE_ID_LEN]; // GFX Adapter Instance ID
    WCHAR gfxIndex[6];                         // GFX Adapter Index (Ex: gfx_0)
    bool  isActive;                            // GFX Adapter is Active (Driver Enabled) or Not (Driver Disabled)
    LUID  adapterLUID;                         // GFX Adapter LUID information
} GFX_ADAPTER_INFO, *PGFX_ADAPTER_INFO;

#pragma pack()