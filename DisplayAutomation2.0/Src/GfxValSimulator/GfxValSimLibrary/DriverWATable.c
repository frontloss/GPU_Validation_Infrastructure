#include "DriverWATable.h"

BOOL GetDriverWATable(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in DRIVER_WA driver_wa, __out UINT *pData)
{
    BOOL             status        = FALSE;
    WA_TABLE         waTable       = { 0 };
    GFX_DRV_WA_TABLE driverWaTable = { 0 };

    status = ValsimIoctlCall(pAdapterInfo, gfxAdapterInfoSize, 13, &driverWaTable, sizeof(GFX_DRV_WA_TABLE), &waTable, sizeof(WA_TABLE));

    if (sizeof(WA_TABLE) != driverWaTable.gfxWaTableSize)
    {
        ERROR_LOG("Gfx WA table size mismatch. Expected size: %d, Actual Size: %lu", (int)sizeof(WA_TABLE), driverWaTable.gfxWaTableSize);
    }

    if (status)
    {
        switch (driver_wa)
        {
        case Wa_22010492432:
            *pData = waTable.Wa_22010492432;
            break;
        case Wa_14010527661:
            *pData = waTable.Wa_14010527661;
            break;
        case Wa_14013475917:
            *pData = waTable.Wa_14013475917;
            break;
        case Wa_22012278275:
            *pData = waTable.Wa_22012278275;
            break;
        case Wa_22012279113:
            *pData = waTable.Wa_22012279113;
            break;
        case Wa_14014971492:
            *pData = waTable.Wa_14014971492;
            break;
        case Wa_16012604467:
            *pData = waTable.Wa_16012604467;
            break;
        case Wa_16011303918:
            *pData = waTable.Wa_16011303918;
            break;
        case Wa_16014451276:
            *pData = waTable.Wa_16014451276;
            break;
        default:
            DEBUG_LOG("Invalid Enum passed : %d", driver_wa);
            return FALSE;
        }
    }
    return status;
}
