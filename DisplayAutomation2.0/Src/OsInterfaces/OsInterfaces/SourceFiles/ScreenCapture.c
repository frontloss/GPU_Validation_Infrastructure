#include <windows.h>
#include <string.h>
#include <tchar.h>
#include "CommonInclude.h"
#include "..\HeaderFiles\DisplayConfig.h"

#define FILE_SIZE 124

BOOLEAN CaptureScreen(_In_ UINT instance, _In_ GFX_ADAPTER_INFO gfxAdapter, _In_ SCREEN_CAPTURE_ARGS captureArgs)
{
    HDC     hdcScreen;
    HDC     hdcWindow;
    HDC     hdcMemDC  = NULL;
    HBITMAP hbmScreen = NULL;
    HANDLE  hDIB      = NULL;
    HANDLE  hFile     = NULL;
    BITMAP  bmpScreen;
    WCHAR   fileName[FILE_SIZE] = L"";
    BOOLEAN status              = FALSE;
    HWND    hWnd                = GetDesktopWindow();

    hdcScreen = GetDC(NULL);
    hdcWindow = GetDC(hWnd);
    hdcMemDC  = CreateCompatibleDC(hdcWindow);

    do
    {
        if (NULL == hdcMemDC)
            break;
        swprintf(fileName, FILE_SIZE, L"Logs//Src_Frame_%lu.png", instance);

        RECT resolution = { resolution.left = 0, resolution.top = 0, resolution.right = captureArgs.HzRes, resolution.bottom = captureArgs.VtRes };
        SetStretchBltMode(hdcWindow, HALFTONE);

        if (!StretchBlt(hdcWindow, 0, 0, resolution.right, resolution.bottom, hdcScreen, 0, 0, GetSystemMetrics(SM_CXSCREEN), GetSystemMetrics(SM_CYSCREEN), SRCCOPY))
            break;
        hbmScreen = CreateCompatibleBitmap(hdcWindow, resolution.right - resolution.left, resolution.bottom - resolution.top);

        if (!hbmScreen)
            break;

        SelectObject(hdcMemDC, hbmScreen);
        if (!BitBlt(hdcMemDC, 0, 0, resolution.right - resolution.left, resolution.bottom - resolution.top, hdcWindow, 0, 0, SRCCOPY))
            break;

        GetObject(hbmScreen, sizeof(BITMAP), &bmpScreen);

        BITMAPFILEHEADER bmfHeader;
        BITMAPINFOHEADER bi;

        bi.biSize          = sizeof(BITMAPINFOHEADER);
        bi.biWidth         = bmpScreen.bmWidth;
        bi.biHeight        = bmpScreen.bmHeight;
        bi.biPlanes        = 1;
        bi.biBitCount      = 32;
        bi.biCompression   = BI_RGB;
        bi.biSizeImage     = 0;
        bi.biXPelsPerMeter = 0;
        bi.biYPelsPerMeter = 0;
        bi.biClrUsed       = 0;
        bi.biClrImportant  = 0;

        DWORD dwBmpSize = ((bmpScreen.bmWidth * bi.biBitCount + 31) / 32) * 4 * bmpScreen.bmHeight;
        hDIB            = GlobalAlloc(GHND, dwBmpSize);
        char *lpbitmap  = (char *)GlobalLock(hDIB);
        GetDIBits(hdcWindow, hbmScreen, 0, (UINT)bmpScreen.bmHeight, lpbitmap, (BITMAPINFO *)&bi, DIB_RGB_COLORS);

        // A file is created, this is where we will save the screen capture.
        hFile = CreateFile(fileName, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

        // Add the size of the headers to the size of the bitmap to get the total file size
        DWORD dwSizeofDIB = dwBmpSize + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

        // Offset to where the actual bitmap bits start.
        bmfHeader.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + (DWORD)sizeof(BITMAPINFOHEADER);

        // Size of the file
        bmfHeader.bfSize = dwSizeofDIB;

        // bfType must always be BM for Bitmaps
        bmfHeader.bfType = 0x4D42;

        DWORD dwBytesWritten = 0;
        status               = WriteFile(hFile, (LPSTR)&bmfHeader, sizeof(BITMAPFILEHEADER), &dwBytesWritten, NULL);
        status               = WriteFile(hFile, (LPSTR)&bi, sizeof(BITMAPINFOHEADER), &dwBytesWritten, NULL);
        status               = WriteFile(hFile, (LPSTR)lpbitmap, dwBmpSize, &dwBytesWritten, NULL);

    } while (FALSE);

    GlobalUnlock(hDIB);
    GlobalFree(hDIB);
    CloseHandle(hFile);

    DeleteObject(hbmScreen);
    DeleteObject(hdcMemDC);
    ReleaseDC(NULL, hdcScreen);
    ReleaseDC(hWnd, hdcWindow);
    return status;
}