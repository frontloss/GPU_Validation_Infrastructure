
#ifndef __MPO_IOCTL_H__
#define __MPO_IOCTL_H__

#include <windows.h>
#include <stdio.h>
#include "../Logger/log.h"
#include "inc/legacy/SimDrvGfxMpo.h"

typedef enum _GFX_MPO_EVENT
{
    ENABLE_DISABLE_MPO,
    GET_OVERLAY_CAPS,
    CHECK_MPO3,
    SET_SOURCE_ADDRESS3,
    CREATE_RESOURCE,
    FREE_RESOURCE
} GFX_MPO_EVENT;

typedef struct _MPO_FLIP_DELAY_ARGS
{
    BOOLEAN waitForFlipDone;
    BOOLEAN waitForScanline;
    UINT32  scanLineToWait;
    ULONG   ScanlineCountOffset; // Scanline count offset.
    UINT64  FrameCountOffset;    // Frame count offset.
} MPO_FLIP_DELAY_ARGS, *PMPO_FLIP_DELAY_ARGS;

typedef struct _MPO_DATA
{
    GFX_MPO_EVENT        eMPOEvent;
    PVOID                pMPOArgs;
    ULONG                ulArgSize;
    PMPO_FLIP_DELAY_ARGS pMpoFlipDelayArgs;
} MPO_DATA, *PMPO_DATA;

typedef struct _RESOURCE_INFO_
{
    UINT64 pGmmBlock;
    UINT64 pUserVirtualAddress;
    UINT64 u64SurfaceSize;
    ULONG  ulPitch;
} RESOURCE_INFO, *PRESOURCE_INFO;

#endif
