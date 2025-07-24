#ifndef IMAGE_FORMAT_INCLUDED

#include "ImageProc.h"
#include"ColorAlgo.h"
#include"ColorUtils.h"
// #include<cmath>
#include<cstdlib>


typedef enum _GVSTUB_SURFACE_MEMORY_TYPE
{
    GVSTUB_SURFACE_MEMORY_INVALID = 0,
    GVSTUB_SURFACE_MEMORY_LINEAR = 1,                      // Surface uses linear momory
    GVSTUB_SURFACE_MEMORY_TILED = 2,                       // Surface uses tiled memory
    GVSTUB_SURFACE_MEMORY_X_TILED = GVSTUB_SURFACE_MEMORY_TILED,
    GVSTUB_SURFACE_MEMORY_Y_LEGACY_TILED = 4,              // Surface uses Legacy Y tiled memory (Gen9+)
    GVSTUB_SURFACE_MEMORY_Y_F_TILED = 8,                   // Surface uses Y F tiled memory
} GVSTUB_SURFACE_MEMORY_TYPE;


typedef enum _SB_PIXELFORMAT {
    SB_UNINITIALIZED = 0,
    SB_8BPP_INDEXED,        // for 8bpp
    SB_B5G6R5X0,            // for 16bpp
    SB_B8G8R8X8,            // for 32bpp (default)
    SB_B8G8R8A8,
    SB_R8G8B8X8,
    SB_R8G8B8A8,
    SB_R10G10B10X2,         // for 32bpp 10bpc
    SB_R10G10B10A2,         // for 32bpp 10bpc
    SB_B10G10R10X2,         // for 32bpp 10bpc
    SB_B10G10R10A2,         // for 32bpp 10bpc
    SB_R10G10B10A2_XR_BIAS, // for 32bpp 10bpc, XR BIAS format (used by Win7)
    SB_R16G16B16X16F,       // for 64bpp, 16bit floating
    SB_R16G16B16A16F,       // for 64bpp, 16bit floating
    SB_MAX_PIXELFORMAT, // Last one - just for internal bitmask usage
    SB_NV12YUV420,
    SB_YUV422,
    SB_P010YUV420,
    SB_P012YUV420,
    SB_P016YUV420,
    SB_YUV444_10,
    SB_YUV422_10,
    SB_YUV422_12,
    SB_YUV422_16,
    SB_YUV444_8,
    SB_YUV444_12,
    SB_YUV444_16,
    SB_MAXALL_PIXELFORMAT,
} SB_PIXELFORMAT, * PSB_PIXELFORMAT;

typedef struct
{
    unsigned int r : 10;
    unsigned int g : 10;
    unsigned int b : 10;
    unsigned int a : 2;
}R10G10B10A2;


typedef struct
{
    unsigned int cb : 10;
    unsigned int y : 10;
    unsigned int cr : 10;
    unsigned int a : 2;
}Cb10Y10Cr10A2;


typedef struct
{
    unsigned int b : 10;
    unsigned int g : 10;
    unsigned int r : 10;
    unsigned int a : 2;
}B10G10R10A2;

typedef struct RGBA8
{
    UINT8 r;
    UINT8 g;
    UINT8 b;
    UINT8 a;
};

typedef struct BGRA8
{
    UINT8 b;
    UINT8 g;
    UINT8 r;
    UINT8 a;
};

typedef struct IMAGEPROPERTIES
{
    int height;
    int width;
    int HDR;
    SB_PIXELFORMAT pixelFormat;
    GVSTUB_SURFACE_MEMORY_TYPE tile;
    double brightness_unit;
};

class ImageFormater
{
    IMAGEPROPERTIES  mImageProperties;

public:
    int SetBufferParameters(IMAGEPROPERTIES imageProperties);

    //Process function for Linear Buffer
    void ProcessLinear(wchar_t* inFileName, IPIXEL* pOutStr);

    //Process function for Y Tilled Buffer
    void ProcessYTilled(wchar_t* inFileName, IPIXEL* pOutStr);




};


#endif// IMAGE_FORMATER_INCLUDED