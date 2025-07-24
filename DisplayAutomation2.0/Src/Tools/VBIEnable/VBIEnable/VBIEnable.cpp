
#include <iostream>
#include <cstdlib>
#include <signal.h>
#include "VBIEnable.h"
using namespace std;

D3DKMT_HANDLE adapterHandle    = NULL;
D3DKMT_ARGS   d3dkmtArgsHandle = { 0 };

// Define the function to be called when ctrl-c (SIGINT) is sent to process
void signal_callback_handler(int signum)
{
    D3DKMT_CLOSEADAPTER closeAdapter = { 0 };
    INFO_LOG("Caught signal %d", signum);
    closeAdapter.hAdapter = adapterHandle;
    if (S_OK != d3dkmtArgsHandle.pfnCloseAdapter(&closeAdapter))
    {
        ERROR_LOG("Failed to close adapter");
    }
    else
        INFO_LOG("Closed Adapter");
    // Terminate program
    exit(signum);
}

D3DKMT_ARGS D3DKMTGetHandle()
{
    D3DKMT_ARGS d3dkmtArgs = { 0 };
    if (d3dkmtArgs.gdi32handle != NULL && d3dkmtArgs.pfnWaitForVerticalBlankEvent2 != NULL && d3dkmtArgs.pfnCloseAdapter != NULL && d3dkmtArgs.pfnOpenAdapterFromHDC != NULL)
        return d3dkmtArgs;

    /* Load gdi32 library and process address for D3D KMT functions*/
    d3dkmtArgs.gdi32handle = LoadLibraryEx(GDI32_DLL, NULL, LOAD_LIBRARY_SEARCH_SYSTEM32);

    if (d3dkmtArgs.gdi32handle)
    {
        d3dkmtArgs.pfnWaitForVerticalBlankEvent2 = (PFND3DKMT_WAITFORVERTICALBLANKEVENT2)GetProcAddress(d3dkmtArgs.gdi32handle, "D3DKMTWaitForVerticalBlankEvent2");
        d3dkmtArgs.pfnOpenAdapterFromHDC         = (PFND3DKMT_OPENADAPTERFROMHDC)GetProcAddress(d3dkmtArgs.gdi32handle, "D3DKMTOpenAdapterFromHdc");
        d3dkmtArgs.pfnCloseAdapter               = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(d3dkmtArgs.gdi32handle, "D3DKMTCloseAdapter");
    }
    return d3dkmtArgs;
}

int main()
{

    D3DKMT_WAITFORVERTICALBLANKEVENT2 waitForVBlank  = { 0 };
    D3DKMT_OPENADAPTERFROMHDC         openAdapterHDC = { 0 };
    DISPLAY_DEVICE                    deviceName;
    deviceName.cb  = sizeof(DISPLAY_DEVICE);
    UINT16   devID = 0;
    HDC      hdc   = NULL;
    NTSTATUS status;
    // Register signal and signal handler
    signal(SIGINT, signal_callback_handler);

    d3dkmtArgsHandle = D3DKMTGetHandle();

    if (d3dkmtArgsHandle.gdi32handle == NULL || d3dkmtArgsHandle.pfnWaitForVerticalBlankEvent2 == NULL || d3dkmtArgsHandle.pfnCloseAdapter == NULL ||
        d3dkmtArgsHandle.pfnOpenAdapterFromHDC == NULL)
        ERROR_LOG("Get Process handles is NULL");

    /* Enumerate through available displays as DISPLAY1 may not be always primary display*/
    while (EnumDisplayDevices(NULL, devID++, &deviceName, 0))
    {
        hdc = CreateDC(deviceName.DeviceName, NULL, NULL, 0);
        /* Check if Device context is not valid*/
        if (0 != hdc)
            break;
    }

    openAdapterHDC.hDc = hdc;

    if (S_OK != d3dkmtArgsHandle.pfnOpenAdapterFromHDC(&openAdapterHDC))
    {
        ERROR_LOG("Failed to open adapter");
    }
    INFO_LOG("Successfully opened adapter");

    waitForVBlank.hAdapter      = openAdapterHDC.hAdapter;
    waitForVBlank.VidPnSourceId = openAdapterHDC.VidPnSourceId;
    adapterHandle               = openAdapterHDC.hAdapter;

    while (true)
    {
        status = d3dkmtArgsHandle.pfnWaitForVerticalBlankEvent2(&waitForVBlank);
        if (S_OK != status)
        {
            ERROR_LOG("Wait for VBlank event failed %ld", status);
        }
        INFO_LOG("Executing Wait for VBlank");
    }
    return EXIT_SUCCESS;
}