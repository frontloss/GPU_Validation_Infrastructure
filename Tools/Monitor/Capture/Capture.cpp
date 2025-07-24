// Capture.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include<Windows.h>
#include <process.h>
#include "..\DrvInterface\DrvInterface.h"

HANDLE hFrameUpdate;
BOOLEAN Collapse;
HMODULE hDriverInterface;
typedef HRESULT(*PFNQWBS)(WB_CAPS *pWbCaps);
PFNQWBS pfnQueryWbStatus;
typedef HRESULT(*PFNCWBF)(WB_CAPTURE *pWbCapture, int *pBuffer);
PFNCWBF pfnCaptureWbFrame;
#define WB_LOG printf
void CaptureLoop(void *)
{
    WB_CAPS WbCaps;
    WB_CAPTURE WbCapture = { 0 };
    int *pFrameBuffer = NULL;
    do
    {
        WaitForSingleObject(hFrameUpdate, 10000);
        if (Collapse)
        {
            WB_LOG("User exited the main App. Teardown the capture loop");
            SetEvent(hFrameUpdate);
            break;
        }
        if (FAILED(pfnQueryWbStatus(&WbCaps)))
        {
            WB_LOG("pfnQueryWbStatus call failed. Teardown the capture loop");
            break;
        }
        // initiate a capture if the Writeback is enabled
        if (FALSE == WbCaps.IsEnabled)
        {
            WB_LOG("Write Back is not enabled yet. Keep waiting");
            continue;
        }
        if (NULL != pFrameBuffer)
        {
            free(pFrameBuffer);
        }
        pFrameBuffer = NULL;
        if (FAILED(pfnCaptureWbFrame(&WbCapture, pFrameBuffer)))
        {
            WB_LOG("pfnCaptureWbFrame call failed. Teardown the capture loop");
            break;
        }
        pFrameBuffer = (int*)malloc(WbCapture.BufferSize);
        if (FAILED(pfnCaptureWbFrame(&WbCapture, pFrameBuffer)))
        {
            WB_LOG("pfnCaptureWbFrame call failed. Teardown the capture loop");
            break;
        }
        WB_LOG("Capture complete");
        // Write the content to a file. TBD
        FILE *fp;
        fopen_s( &fp, "WbWriteBack.bin", "wb");
        if (fp == NULL)
        {
            break;
        }
        fwrite(pFrameBuffer, 1, WbCapture.BufferSize, fp);

        fclose(fp);
        WB_LOG("Dumped the content to WbWriteBack.bin");
    }
    while (TRUE);
    if (NULL != pFrameBuffer)
    {
        free(pFrameBuffer);
    }
}
int main()
{
    // Initializations
    Collapse = FALSE;
    // Create the event to synchronize the cature
    hFrameUpdate = CreateEvent(NULL, false, false, NULL);
    hDriverInterface = LoadLibraryEx(L"DrvInterface.dll", NULL, 0);
    pfnQueryWbStatus = (PFNQWBS)GetProcAddress(hDriverInterface, "QueryWbStatus");
    pfnCaptureWbFrame = (PFNCWBF)GetProcAddress(hDriverInterface, "CaptureFrame");
    // Start the thread
    _beginthread(CaptureLoop, 0,  NULL);

    // Wait for the user to quit
    while (getchar() != 'q');

    // Clean up
    Collapse = TRUE;
    SetEvent(hFrameUpdate);
    WaitForSingleObject(hFrameUpdate, 1000);
    FreeLibrary(hDriverInterface);
    return 0;
}

