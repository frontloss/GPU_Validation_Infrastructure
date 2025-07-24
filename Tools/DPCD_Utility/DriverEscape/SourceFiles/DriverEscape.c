/*------------------------------------------------------------------------------------------------*
 *
 * @file     DisplayEscape.c
 * @brief    This file contains Implementation of Internal APIs - GetD3DEscapeHandles, InvokeDriverEscape,
 *           TdrDriverEscape, GetGfxAdapterInfo
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "DriverEscape.h"

extern char *LIBRARY_NAME = "DriverEscape.dll";

static D3DKMT_ESCAPE_ARGS d3dkmtEscape = { 0 };

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           GetD3DEscapeHandles Helper Function (Internal API)
 * Description:                     This function returns the D3DKMT_ESCAPE_ARGS for the escape call.
 * @return D3DKMT_ESCAPE_ARGS       Returns the args after retrieving the handles
 *----------------------------------------------------------------------------------------------------------*/
D3DKMT_ESCAPE_ARGS GetD3DEscapeHandles()
{
    if (d3dkmtEscape.gdi32handle != NULL && d3dkmtEscape.pfnD3DKmtEscape != NULL && d3dkmtEscape.pfnCloseAdapter != NULL && d3dkmtEscape.pfnOpenAdapterFromLuid != NULL)
        return d3dkmtEscape;

    /* Load gdi32 library and proccess address for D3D KMT functions*/
    d3dkmtEscape.gdi32handle = LoadLibraryEx(GDI32_LIB, NULL, LOAD_LIBRARY_SEARCH_SYSTEM32);
    /* Get process handles to operate on for escape call*/
    d3dkmtEscape.pfnOpenAdapterFromLuid = (PFND3DKMT_OPENADAPTERFROMLUID)GetProcAddress(d3dkmtEscape.gdi32handle, "D3DKMTOpenAdapterFromLuid");
    d3dkmtEscape.pfnD3DKmtEscape        = (PFND3DKMT_ESCAPE)GetProcAddress(d3dkmtEscape.gdi32handle, "D3DKMTEscape");
    d3dkmtEscape.pfnCloseAdapter        = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(d3dkmtEscape.gdi32handle, "D3DKMTCloseAdapter");
    return d3dkmtEscape;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           InvokeDriverEscape (Internal API)
 * Description:                     This function Invokes Driver Escape based on header input <escapeOpCode>.
 * @param ADAPTER_INFO_GDI_NAME     _In_    pointer of _ADAPTER_INFO_GDI_NAME, It contains viewGDIDeviceName of the Respective Adapter
 * @param INT                       _In_    Size of ESC Data Structure
 * @param GFX_ESCAPE_HEADER_T       _In_    escapeOpCode Driver ESC Opcode
 * @param VOID                      _Out_   Pointer of Structure of required Data
 * @return BOOLEAN                  Returns TRUE on Success else FALSE on Failure
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN InvokeDriverEscape(_In_ GFX_INFO gfxInfo, _In_ INT escapeDataSize, _In_ GFX_ESCAPE_HEADER_T escapeOpCode, _Out_ void *pEscapeData)
{
    BOOLEAN                    status           = FALSE;
    D3DKMT_ESCAPE_ARGS         dedkmtEscapeArgs = { 0 };
    GFX_ESCAPE_HEADER_T        header           = { 0 };
    D3DKMT_ESCAPE              kmtEscape        = { 0 };
    D3DKMT_OPENADAPTERFROMLUID openAdapterLuid  = { 0 };
    D3DKMT_CLOSEADAPTER        closeAdapter     = { 0 };
    D3DKMT_HANDLE              hAdapter         = 0;

    /* Initailize variables*/
    PVOID  pLocal = NULL;
    HANDLE hLocal = NULL;

    NULL_PTR_CHECK(pEscapeData);

    do
    {
        /* Load gdi32 library and proccess address for D3D KMT functions, if not set*/
        dedkmtEscapeArgs = GetD3DEscapeHandles();

        if (dedkmtEscapeArgs.gdi32handle == NULL || dedkmtEscapeArgs.pfnOpenAdapterFromLuid == NULL || dedkmtEscapeArgs.pfnD3DKmtEscape == NULL ||
            dedkmtEscapeArgs.pfnCloseAdapter == NULL)
        {
            ERROR_LOG("GetD3DEscapeHandles is NULL");
            break;
        }

        openAdapterLuid.AdapterLuid = gfxInfo.adapterID;
        if (S_OK != d3dkmtEscape.pfnOpenAdapterFromLuid(&openAdapterLuid))
        {
            ERROR_LOG("Failed to identify adapter device name for target ID : %lu,  high : %ld, low : %lu", gfxInfo.targetID, openAdapterLuid.AdapterLuid.HighPart, openAdapterLuid.AdapterLuid.LowPart);
            break;
        }

        hAdapter = openAdapterLuid.hAdapter;
        if (0 == hAdapter)
        {
            ERROR_LOG("Found no adapter handle.");
            break;
        }

        hLocal = GlobalAlloc(GHND, escapeDataSize + sizeof(GFX_ESCAPE_HEADER_T));
        if (NULL == hLocal)
        {
            ERROR_LOG("GlobalAlloc is NULL");
            break;
        }

        pLocal = GlobalLock(hLocal);
        if (NULL == pLocal)
        {
            ERROR_LOG("GlobalLock is NULL");
            break;
        }

        /* Prepare Escape header*/
        kmtEscape.hAdapter           = hAdapter;
        kmtEscape.Type               = D3DKMT_ESCAPE_DRIVERPRIVATE;
        kmtEscape.pPrivateDriverData = pLocal;
        if (NULL == kmtEscape.pPrivateDriverData)
        {
            ERROR_LOG("Memory Allocation is NULL");
            break;
        }
        kmtEscape.PrivateDriverDataSize = escapeDataSize + sizeof(GFX_ESCAPE_HEADER_T);

        ///* Set header with the escape request type*/
        header.minorInterfaceVersion = escapeOpCode.minorInterfaceVersion;
        header.majorEscapeCode       = escapeOpCode.majorEscapeCode;
        header.minorEscapeCode       = escapeOpCode.minorEscapeCode;
        header.majorInterfaceVersion = escapeOpCode.majorInterfaceVersion;

        memcpy(kmtEscape.pPrivateDriverData, &header, sizeof(GFX_ESCAPE_HEADER_T));

        /* Fill escape header with the details*/
        PVOID pOutData = (PCHAR)kmtEscape.pPrivateDriverData + sizeof(GFX_ESCAPE_HEADER_T);
        memcpy(pOutData, pEscapeData, escapeDataSize);

        /* Make a driver Escape call*/
        if (S_OK == dedkmtEscapeArgs.pfnD3DKmtEscape(&kmtEscape))
        {
            status = TRUE;
            memcpy(pEscapeData, pOutData, escapeDataSize);
        }
    } while (FALSE);

    if (0 != hAdapter)
    {
        closeAdapter.hAdapter = hAdapter;
        if (S_OK != d3dkmtEscape.pfnCloseAdapter(&closeAdapter))
        {
            ERROR_LOG("Failed to close adapter!!");
        }
    }

    /* Release handles and heap variables*/
    if (hLocal != NULL)
    {
        GlobalUnlock(hLocal);
        GlobalFree(hLocal);
    }

    return status;
}
