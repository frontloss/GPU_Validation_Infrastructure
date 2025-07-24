// Imp: IOCTL Files shouldn't include any driver headers execept other IOCTL files and dependant files accessible to the APP world

#ifndef __VALSIM_ACCESS_IOCTL_H__
#define __VALSIM_ACCESS_IOCTL_H__

#include <windows.h>
#include <stdio.h>
#include "..\GfxValSimDriver\DriverInterfaces\CommonIOCTL.h"

BOOL ValSim_DeviceIoControl(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT gfxAdapterInfoSize, DWORD ioctl_code, VOID *pMpoData, ULONG uldatasize);

#endif
