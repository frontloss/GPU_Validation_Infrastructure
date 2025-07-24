#pragma once

#include <wincodec.h>
#include <wincodecsdk.h>
#include <atlbase.h>
#include <iostream>
#include <fstream>
#include <stdlib.h>

#include "GlobalDefinitions.h"

#define DLL_EXPORT 1
/* Preprocessor Macros*/
#if defined DLL_EXPORT
#define EXPORT_API __declspec(dllexport)
#else
#define EXPORT_API __declspec(dllimport)
#endif

#pragma comment(lib, "WindowsCodecs.lib")

template <class T> void SafeRelease(T **ppT)
{
    if (*ppT)
    {
        (*ppT)->Release();
        *ppT = NULL;
    }
}

typedef struct
{
    UINT32 top;
    UINT32 left;
    UINT32 width;
    UINT32 height;
} IMAGE_RECTANGLE;

typedef struct
{
    DDU8 a;
    DDU8 r;
    DDU8 g;
    DDU8 b;
} R8G8B8A8_PIXEL;

typedef struct
{
    DDU16 r : 10;
    DDU16 g : 10;
    DDU16 b : 10;
} R10G10B10_PIXEL;

typedef struct
{
    DDU16 r;
    DDU16 g;
    DDU16 b;
} R16G16B16_PIXEL;

typedef struct
{
    DDU8 r;
    DDU8 g;
    DDU8 b;
} R8G8B8_PIXEL;

class ImageIO
{
  public:
    EXPORT_API IPIXEL16 *ReadFile16(WCHAR *pFilename, DDU32 &width, DDU32 &height);
    EXPORT_API IPIXEL32 *ReadFile32(WCHAR *pFilename, DDU32 &width, DDU32 &height);
    EXPORT_API IPIXEL16 *ReadFile8(WCHAR *pFilename, INT &width, INT &height);

    EXPORT_API static IPIXEL16 *GetRectangle(IPIXEL16 *pSrc, DDU32 srcW, DDU32 srcH, IMAGE_RECTANGLE *pRect);
    EXPORT_API static DDS32     WriteFile(WCHAR *pFilename, DDU32 width, DDU32 height, IPIXEL16 *pPixelData);
    EXPORT_API static DDS32     WriteFile(WCHAR *pFilename, UINT width, UINT height, IPIXEL32 *pPixelData, UINT MaxPixelValue, UINT8 ImageBpc);
    EXPORT_API static DDS32     WriteFile(WCHAR *pFilenam, UINT width, UINT height, IPIXEL16 *pPixelData, UINT MaxPixelValue, UINT8 ImageBpc);

    EXPORT_API BOOL Conver8bitArrayto16BitArray(IPIXEL8 *pBitArray, DDU32 &width, DDU32 &height, IPIXEL16 *pPixArray);
    EXPORT_API BOOL Conver10bitArrayto16BitArray(IPIXEL10 *pBitArray, DDU32 &width, DDU32 &height, IPIXEL16 *pPixArray);
};
