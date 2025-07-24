/*------------------------------------------------------------------------------------------------*
 *
 * @file     Utilities.c
 * @brief    This file contains Implementation of Reusable APIs - CopyWchar, CopyStr
 * @author   Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/

#include "Utilities.h"

/**---------------------------------------------------------------------------------------------------------*
 * @brief               CopyWchar (Internal Helper API)
 * Description          This function helps to copy wchar string from source to destination memory.
 * @param[Out]          dest (Pointer to WCHAR destination string)
 * @param[In]           destSize (NOTE: Always pass _countof(dest) from caller)
 * @param[In]           src (Pointer to WCHAR source string)
 * @return errno_t      Returns [0 if success, -1 if buffer size insufficient]
 *-----------------------------------------------------------------------------------------------------------*/
errno_t CopyWchar(_Out_ WCHAR dest[], _In_ size_t destSize, _In_ WCHAR src[])
{
    errno_t errorCode = -1;
    size_t  srcSize   = wcslen(src) + 1;
    if (destSize < srcSize)
        ERROR_LOG("Copy Failed. src_size: %zu, dest_size: %zu, buf: %ls", srcSize, destSize, src);
    else
        errorCode = wcscpy_s(dest, destSize, src);
    return errorCode;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               CopyStr (Internal Helper API)
 * Description          This function helps to copy string from source to destination memory.
 * @param[Out]          dest (Pointer to destination string)
 * @param[In]           destSize (NOTE: Always pass _countof(dest) from caller)
 * @param[In]           src (Pointer to source string)
 * @return errno_t      Returns [0 if success, -1 if buffer size insufficient]
 *-----------------------------------------------------------------------------------------------------------*/
errno_t CopyStr(_Out_ CHAR dest[], _In_ size_t destSize, _In_ CHAR src[])
{
    errno_t errorCode = -1;
    size_t  srcSize   = strlen(src) + 1;
    if (destSize < srcSize)
        ERROR_LOG("Copy Failed. src_size: %zu, dest_size: %zu, buf: %s", srcSize, destSize, src);
    else
        errorCode = strcpy_s(dest, destSize, src);
    return errorCode;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               GetGfxIndexValue (Internal Helper API)
 * Description          This helper function gets adapter index as integer from input gfxIndex.
 * @param[In]           gfxIndex (GFX Adapter Index)
 * @return INT          Returns Adapter Index
 *-----------------------------------------------------------------------------------------------------------*/
UINT GetGfxIndexValue(WCHAR* gfxIndex)
{
    if ((int)wcslen(gfxIndex) == 5) // "gfx_0" or "gfx_1" is expected
    {
        return _wtoi(&gfxIndex[4]);
    }
    return -1;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               CompareAdapterInfo (Internal Helper API)
 * Description          This function is used to compare 2 adapters' device ID and deviceInstance ID
 * @param[In]           adapter1 (structure of type GFX_ADAPTER_INFO)
 * @param[In]           adapter2 (structure of type GFX_ADAPTER_INFO)
 * @return BOOLEAN      Returns [1 if both adapters match, else 0]
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN CompareAdapterInfo(GFX_ADAPTER_INFO adapter1, GFX_ADAPTER_INFO adapter2)
{
    // Fail for invalid adapter passed
    if (wcslen(adapter1.deviceID) == 0 || wcslen(adapter1.deviceInstanceID) == 0 ||
        wcslen(adapter2.deviceID) == 0 || wcslen(adapter2.deviceInstanceID) == 0)
    {
        ERROR_LOG("Adapter 1 device ID: {%ls} instance ID: {%ls}", adapter1.deviceID, adapter1.deviceInstanceID);
        ERROR_LOG("Adapter 2 device ID: {%ls} instance ID: {%ls}", adapter2.deviceID, adapter2.deviceInstanceID);
        return FALSE;
    }
    return (0 == wcscmp(adapter1.deviceID, adapter2.deviceID) && 0 == wcscmp(adapter1.deviceInstanceID, adapter2.deviceInstanceID));
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               ComparePanelInfo (Internal Helper API)
 * Description          This function is used to compare 2 panels' target ID and corresponding adapter details
 * @param[In]           panel1 (structure of type PANEL_INFO)
 * @param[In]           panel2 (structure of type PANEL_INFO)
 * @return BOOLEAN      Returns [1 if both panels match, else 0]
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN ComparePanelInfo(PANEL_INFO panel1, PANEL_INFO panel2)
{
    // Fail for invalid panel passed
    if (panel1.targetID == 0 || panel2.targetID == 0)
    {
        ERROR_LOG("Panel 1 target ID: {%lu} Panel 2 target ID: {%lu}", panel1.targetID, panel2.targetID);
        return FALSE;
    }
    return (CompareAdapterInfo(panel1.gfxAdapter, panel2.gfxAdapter) && (panel1.targetID == panel2.targetID));
}
