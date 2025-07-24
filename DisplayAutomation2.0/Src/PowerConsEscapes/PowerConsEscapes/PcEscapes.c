/**
 * @file		PcEscapes.c
 * @brief	This Contains implementation for the AlsOverride using PC DriverEscapes.
 *
 * @author	Ashish Tripathi
 */

#pragma once
#include "PcEscapes.h"
#define GDI32_DLL L"gdi32.dll"

/**
 * @brief						          Treat pBuffer as an array of unsigned long and
 *                                         calculate the sum of all values in the array.
 *									      Used to calculate simple check sum to make sure
 *										  that data passed to EscapeCall is data send by user mode or OGL driver.
 * @param[in]	pBuffer                   Pointer to the buffer
 * @param[in]	BufferSize                Buffer size in bytes
 * @return		ULONG                     Checksum
 */
ULONG SumOfBufferData(VOID *pBuffer, ULONG BufferSize)
{
    ULONG  Index;
    ULONG  CheckSum;
    ULONG  NumOfUnsignedLongs = BufferSize / sizeof(ULONG);
    ULONG *pElement           = (ULONG *)pBuffer;
    // initialize CheckSum
    CheckSum = 0;
    for (Index = 0; Index < NumOfUnsignedLongs; Index++)
    {
        CheckSum += *pElement;
        pElement++;
    }
    return CheckSum;
}

/**
 * @brief									Set driver to use ALS override data
 * @param[in]	override					Boolean argument to override
 * @param[in]	lux							lux value
 * @param[out]	pErrorCode					contains error if any
 * @return		BOOLEAN
 */
BOOLEAN AlsOverride(BOOLEAN override, INT lux, HRESULT *pErrorCode)
{
    if (lux < 0)
    {
        return FALSE;
    }
    *pErrorCode                                    = S_OK;
    HRESULT                        errorCode       = S_FALSE;
    PC_ESCAPE_INFO                 pcEscapeInfo    = { 0 };
    PC_ESCAPE_ALS_OVERRIDE_DATA_IN alsOverrideData = { 0 };
    UINT32                         sizePCArgs      = (UINT32)sizeof(PC_ESCAPE_INFO);
    alsOverrideData.Lux                            = lux;
    alsOverrideData.Override                       = override;

    /* Set up the escape info struct*/
    pcEscapeInfo.EscapeOperation = PC_ESCAPE_OVERRIDE_ALS_INFO;
    pcEscapeInfo.DataInSize      = sizeof(PC_ESCAPE_ALS_OVERRIDE_DATA_IN);
    pcEscapeInfo.pDataIn         = &alsOverrideData;
    pcEscapeInfo.DataOutSize     = 0;
    pcEscapeInfo.pDataOut        = NULL;

    /* Set up driver escape header*/
    pcEscapeInfo.Header.Size       = sizeof(PC_ESCAPE_INFO) - sizeof(GFX_ESCAPE_HEADER);
    pcEscapeInfo.Header.EscapeCode = GFX_ESCAPE_PWRCONS_CONTROL;
    pcEscapeInfo.Header.CheckSum   = SumOfBufferData(((char *)(&pcEscapeInfo)) + sizeof(GFX_ESCAPE_HEADER), pcEscapeInfo.Header.Size);

    PcDriverEscape(sizePCArgs, &pcEscapeInfo, &errorCode);
    if (errorCode != S_OK)
    {
        *pErrorCode = errorCode;
        return FALSE;
    }
    return TRUE;
}

/**
 * @brief									Driver Escapes for PowerCons.
 * @param[in]	cbIn						Size of the PC_ESCAPE_INFO structure
 * @param[in]	pIn							required escape info struct for PC Escape operation
 * @param[out]	pErrorCode					contains error if any
 * @return		VOID
 */
VOID PcDriverEscape(INT cbIn, VOID *pIn, HRESULT *pErrorCode)
{
    *pErrorCode = S_OK;
    /*Initialize and get the OS escape handles*/
    HMODULE                      hGdi32       = NULL;
    PFND3DKMT_OPENADAPTERFROMHDC OpenAdapter  = NULL;
    PFND3DKMT_ESCAPE             D3DKmtEscape = NULL;
    PFND3DKMT_CLOSEADAPTER       CloseAdapter = NULL;
    D3DKMT_ESCAPE                esc          = { 0 };
    DISPLAY_DEVICE               deviceName;
    deviceName.cb = sizeof(DISPLAY_DEVICE);
    UINT16 devID  = 0;
    HDC    hdc    = NULL;

    /* Initialize variables*/
    VOID * pLocal = NULL;
    HANDLE hLocal = NULL;
    hLocal        = GlobalAlloc(GHND, cbIn);
    pLocal        = GlobalLock(hLocal);

    /* Using device context make a call to OpenAdapter*/
    D3DKMT_OPENADAPTERFROMHDC *poa = (D3DKMT_OPENADAPTERFROMHDC *)malloc(sizeof(D3DKMT_OPENADAPTERFROMHDC));
    NULLPTRCHECK(poa, *pErrorCode);

    /* Load gdi32 library and process address for D3D KMT functions*/
    hGdi32 = LoadLibraryEx(GDI32_DLL, NULL, LOAD_LIBRARY_SEARCH_SYSTEM32);
    if (hGdi32)
    {
        /* Get process handles to operate on for escape call*/
        OpenAdapter  = (PFND3DKMT_OPENADAPTERFROMHDC)GetProcAddress(hGdi32, "D3DKMTOpenAdapterFromHdc");
        D3DKmtEscape = (PFND3DKMT_ESCAPE)GetProcAddress(hGdi32, "D3DKMTEscape");
        CloseAdapter = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(hGdi32, "D3DKMTCloseAdapter");
    }

    /* Enumerate through available displays as DISPLAY1 may not be always primary display*/
    while (EnumDisplayDevices(NULL, devID++, &deviceName, 0))
    {
        hdc = CreateDC(deviceName.DeviceName, NULL, NULL, 0);
        /* Check if Device context is not valid*/
        if (0 != hdc)
            break;
    }
    ZeroMemory(poa, sizeof(poa));
    poa->hDc = hdc;

    /* creates a graphics adapter object*/
    if (OpenAdapter(poa) != S_OK)
    {
        *pErrorCode = E_OUTOFMEMORY;
        free(poa);
        return;
    }

    /* Prepare Escape header*/
    ZeroMemory(&esc, sizeof(esc));
    esc.hAdapter              = poa->hAdapter;
    esc.Type                  = D3DKMT_ESCAPE_DRIVERPRIVATE;
    esc.pPrivateDriverData    = (void *)malloc(cbIn);
    esc.PrivateDriverDataSize = cbIn;

    /* Fill escape header with the details*/
    CHAR *pPointer = (char *)esc.pPrivateDriverData;
    VOID *pret     = pPointer;
    memcpy(pret, pIn, cbIn);

    /* Make a driver escape call*/
    ULONG ntret = D3DKmtEscape(&esc);
    if (ntret != S_OK)
    {
        *pErrorCode = ntret;
    }
    else
    {
        /* Copy escape call structure*/
        memcpy(pIn, pret, cbIn);
    }

    /* Release all memory*/
    D3DKMT_CLOSEADAPTER ca;
    ca.hAdapter = poa->hAdapter;
    CloseAdapter(&ca);

    /* Free all the mallocs*/
    free(poa);
    poa = NULL;

    free(esc.pPrivateDriverData);
    esc.pPrivateDriverData = NULL;

    /* Release handles and heap variables*/
    GlobalUnlock(hLocal);
    GlobalFree(hLocal);
    DeleteDC(hdc);
}
