#pragma once

#ifdef __KERNELMODE
#include <ntdef.h>
#endif

#ifdef __USERMODE
#include <Windows.h>
#include "CommonDetails.h"
#endif

#include "sku_wa.h"

typedef enum _DRIVER_WA
{
    Wa_NONE        = 0,
    Wa_22010492432 = 1,
    Wa_14010527661 = 2,
    Wa_14013475917 = 3,
    Wa_22012278275 = 4,
    Wa_22012279113 = 5,
    Wa_14014971492 = 6,
    Wa_16012604467 = 7,
    Wa_16011303918 = 8,
    Wa_16014451276 = 9
} DRIVER_WA;

typedef struct _GFX_DRV_WA_TABLE
{
    PVOID pGfxSkuTable;
    ULONG gfxSkuTableSize;
    PVOID pGfxWaTable;
    ULONG gfxWaTableSize;
} GFX_DRV_WA_TABLE;

#ifdef __USERMODE
/*
 * @brief        Exposed API for GetDriverWATable
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   driver_wa of type DRIVER_WA
 * @param[out]   data
 * @return       Return True on success otherwise return false
 */
CDLL_EXPORT BOOL GetDriverWATable(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in DRIVER_WA driver_wa, __out UINT *pData);
#endif