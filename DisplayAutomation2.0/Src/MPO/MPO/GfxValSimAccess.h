// Imp: IOCTL Files shouldn't include any driver headers execept other IOCTL files and dependant files accessible to the APP world

#ifndef __MPO_IOCTL_H__
#define __MPO_IOCTL_H__

#include <windows.h>
#include <stdio.h>
#include "..\..\GfxValSimulator\GfxValSimDriver\DriverInterfaces\CommonIOCTL.h"
#include "..\..\OsInterfaces\OsInterfaces\HeaderFiles\DisplayConfig.h"
#include "..\inc\mainline\SimDrv_Gfx_MPO.h"

#define INTEL_VENDOR_ID L"8086"

HANDLE hGfxValSimAccess;

typedef enum _GFX_MPO_EVENT
{
    ENABLE_DISABLE_MPO,
    GET_OVERLAY_CAPS,
    CHECK_MPO3,
    SET_SOURCE_ADDRESS3,
    CREATE_RESOURCE,
    FREE_RESOURCE
} GFX_MPO_EVENT;

typedef struct _MPO_DATA
{
    GFX_MPO_EVENT eMPOEvent;
    PVOID         pMPOArgs;
    ULONG         ulArgSize;
} MPO_DATA, *PMPO_DATA;

BOOL GfxValSimVerifyGfxAdapter(PGFX_ADAPTER_INFO pAdapterInfo);

BOOL ValSim_DeviceIoControl(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT gfxAdapterInfoSize, VOID *pMpoData, ULONG uldatasize);

#endif
