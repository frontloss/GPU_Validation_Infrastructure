/*------------------------------------------------------------------------------------------------*
 *
 * @file     CuiSdk.cpp
 * @brief    This file contains Implementation of CUI SDK APIs - InitializeCUISDK,
 *           UninitializeCUISDK
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "SdkSharedHeader.h"
#include "CuiSdk.h"

ICUIExternal8 *pCUIExternal = NULL;

extern char LIBRARY_NAME[] = "CuiSdk.dll";

BOOLEAN InitializeCUISDKN()
{
    HRESULT CoInit  = CoInitialize(NULL);
    BOOL    bStatus = FALSE;
    HRESULT hr      = S_FALSE;
    CLSID   clsid;

    hr = CLSIDFromProgID(L"Igfxext.CUIExternal", &clsid);
    if (SUCCEEDED(hr))
    {
        hr = CoCreateInstance(clsid, NULL, CLSCTX_SERVER, IID_ICUIExternal8, (void **)&pCUIExternal);
        if (FAILED(hr))
        {
            bStatus = FALSE;
            ERROR_LOG("Failed to Create Instance!!");
        }
        else
            bStatus = TRUE;
    }
    else
        ERROR_LOG("Failed to Get CLSID from SDK Service!!");

    return bStatus;
}

BOOLEAN UninitializeCUISDKN()
{
    BOOLEAN bStatus = FALSE;
    // Initialize CUISDK 2 times and uninitialize only once to properly cleanup the CUI COM objects.
    // If we don't initialize CUISDK 2 times, then control doesn't get transferred from DisplayPort.DLL
    // to the Python libraries resulting in Software hang. This is WA (WorkAround) only. Proper fix
    // needs to be figure-out. As per blogs on Python, this issue shouldn’t observe with latest Python
    // binaries but we needs to be verified.
    if (TRUE == InitializeCUISDKN())
    {
        pCUIExternal->Release();
        pCUIExternal = NULL;
        CoUninitialize();
        bStatus = TRUE;
    }
    else
        ERROR_LOG("Failed to Initialize CUI SDK!!");

    return bStatus;
}
