#pragma once

#define DllExport   __declspec( dllexport )
#pragma pack(push, 8)  
typedef struct _WB_CAPS
{
    int IsSupported;
    int IsEnabled;
    int HResolution;
    int VResolution;
    int PixelFormat;
}WB_CAPS;
typedef struct _WB_CAPTURE
{
    int WdSource;
    int HResolution;
    int VResolution;
    int PixelFormat;
    long BufferSize;
    int *pBuffer;
}WB_CAPTURE;
#pragma pack(pop) 