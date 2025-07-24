#ifndef __DRIVER_H__
#define __DRIVER_H__

#include <wdm.h>
#include <ntddk.h>
#include <ntdef.h>
#include <string.h>
#include <ntstrsafe.h>
#include <initguid.h>
#include <ntddvdeo.h>
#include "SimDrvToGfx.h"

// NT device name
#define SIMDRV_DEVICE_NAME L"\\Device\\GfxValSimDriver"
#define SIMDRV_ALLOC_TAG 'VSIM'
#define BUILD_NUMBER_WDDM2_5 17700
#define STATE_SEPARATION_ENABLED(osBuildNumber) (osBuildNumber >= BUILD_NUMBER_WDDM2_5 ? TRUE : FALSE)

typedef struct _SIMDEV_EXTENTSION
{
    UNICODE_STRING   DosDeviceName;
    UNICODE_STRING   SymbolicLink;
    PDEVICE_OBJECT   pstPhysicalDeviceObject;
    PDEVICE_OBJECT   pstLowerDeviceObject;
    PDEVICE_OBJECT   pstDeviceObject;
    PDRIVER_OBJECT   pstDriverObject;
    UNICODE_STRING   DriverRegPath;
    OSVERSIONINFOEXW OsInfo;
    PVOID            pvSimDrvToGfxContext;
} SIMDEV_EXTENTSION, *PSIMDEV_EXTENTSION;

PSIMDEV_EXTENTSION GetSimDrvExtension();

#endif