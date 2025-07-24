#ifndef _IMAGE_FILE_HANDLER
#define _IMAGE_FILE_HANDLER

#include <wincodec.h>
#include <wincodecsdk.h>
#include <atlbase.h>
#include <iostream>
#include <fstream>
#include <stdlib.h>

#include "ColorAlgo.h"

#pragma comment(lib, "WindowsCodecs.lib")

#define MAX_16BPC_PIXEL_VALUE 65535.0
#define ALPHA_OPAQUE MAX_16BPC_PIXEL_VALUE

typedef struct
{
    UINT8 r;
    UINT8 g;
    UINT8 b;
}R8G8B8_PIXEL;

typedef struct
{
    UINT8 a;
    UINT8 r;
    UINT8 g;
    UINT8 b;
}R8G8B8A8_PIXEL;

typedef struct
{
    UINT16 r : 10;
    UINT16 g : 10;
    UINT16 b : 10;
}R10G10B10_PIXEL;

typedef struct
{
    unsigned int a : 2;
    unsigned int r : 10;
    unsigned int g : 10;
    unsigned int b : 10;
}R10G10B10A2_PIXEL;

typedef struct
{
    UINT16 r;
    UINT16 g;
    UINT16 b;
}R16G16B16_PIXEL;

typedef struct
{
    UINT16 r;
    UINT16 g;
    UINT16 b;
    UINT16 a;
}R16G16B16A16_PIXEL;

typedef struct
{
    UINT16 red;     // Either in UINT16 or FP16
    UINT16 green;
    UINT16 blue;
    UINT16 alpha;
}IPIXEL;

class ImageIO
{

public:

    IPIXEL* ReadFile(WCHAR* pFilename, UINT& width, UINT& height);
    int WriteFile(WCHAR* pFilename, UINT width, UINT height, IPIXEL* pPixelData);
};

#endif   //_IMAGE_FILE_HANDLER