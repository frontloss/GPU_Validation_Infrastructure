#include "ImageIO.h"

void UpdateMinMaxComponentValues(IPIXEL32 *pRetPixel, int linearPosition, UINT32 &MinRed, UINT32 &MinGreen, UINT32 &MinBlue, UINT32 &MinAlpha, UINT32 &MaxRed, UINT32 &MaxGreen,
                                 UINT32 &MaxBlue, UINT32 &MaxAlpha);

IPIXEL32 *ImageIO::ReadFile32(WCHAR *pFilename, DDU32 &width, DDU32 &height)
{
    IWICImagingFactory *pFactory  = NULL;
    IWICBitmapDecoder * pDecoder  = NULL;
    IPIXEL32 *          pRetPixel = NULL;
    UINT32              MinRed    = 0;
    UINT32              MinBlue   = 0;
    UINT32              MinGreen  = 0;
    UINT32              MinAlpha  = 0;
    UINT32              MaxRed    = MAX_32BPC_PIXEL_VALUE;
    UINT32              MaxBlue   = MAX_32BPC_PIXEL_VALUE;
    UINT32              MaxGreen  = MAX_32BPC_PIXEL_VALUE;
    UINT32              MaxAlpha  = MAX_32BPC_PIXEL_VALUE;

    HRESULT hr = S_OK;
    CoInitialize(NULL);

    hr = CoCreateInstance(CLSID_WICImagingFactory, NULL, CLSCTX_INPROC_SERVER, IID_IWICImagingFactory, (LPVOID *)&pFactory);

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateDecoderFromFilename(pFilename, NULL, GENERIC_READ, WICDecodeMetadataCacheOnDemand, &pDecoder);

        if (!SUCCEEDED(hr))
        {
            return pRetPixel;
        }
    }

    UINT uiFrameCount = 0;
    hr                = pDecoder->GetFrameCount(&uiFrameCount);

    if (uiFrameCount > 0)
    {
        IWICBitmapFrameDecode *Frame = NULL;
        pDecoder->GetFrame(0, &Frame);

        WICPixelFormatGUID pixFormat;
        Frame->GetPixelFormat(&pixFormat);

        UINT32 nChannels = 3, pixelCompnentSizeInBytes = 1;

        if (pixFormat == GUID_WICPixelFormat48bppRGB || pixFormat == GUID_WICPixelFormat48bppBGR || pixFormat == GUID_WICPixelFormat64bppRGBA ||
            pixFormat == GUID_WICPixelFormat64bppBGRA)
        {
            pixelCompnentSizeInBytes = 2;
        }

        if (pixFormat == GUID_WICPixelFormat32bppRGBA || pixFormat == GUID_WICPixelFormat32bppBGRA || pixFormat == GUID_WICPixelFormat64bppRGBA ||
            pixFormat == GUID_WICPixelFormat64bppBGRA || pixFormat == GUID_WICPixelFormat32bppBGR101010 || pixFormat == GUID_WICPixelFormat32bppRGBA1010102)
        {
            nChannels = 4;
        }

        Frame->GetSize(&width, &height);

        UINT  bufferSize = width * height * nChannels * pixelCompnentSizeInBytes;
        BYTE *pBuffer    = (PBYTE)_aligned_malloc(bufferSize, 32);

        hr = Frame->CopyPixels(NULL, nChannels * width * pixelCompnentSizeInBytes, bufferSize, (BYTE *)pBuffer); // copy the image pixel data to buffer

        if (SUCCEEDED(hr))
        {
            if (pixFormat == GUID_WICPixelFormat64bppRGBA)
            {
                IPIXEL16 *pInPixel = (IPIXEL16 *)pBuffer;
                pRetPixel          = (IPIXEL32 *)_aligned_malloc(width * height * sizeof(IPIXEL32), 32);
                double scaleFactor = MAX_32BPC_PIXEL_VALUE / MAX_16BPC_PIXEL_VALUE;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition              = (y * width + x);
                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].red * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].green * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].blue * scaleFactor);
                        pRetPixel[linearPosition].alpha = round((double)pInPixel[linearPosition].alpha * scaleFactor);

                        UpdateMinMaxComponentValues(pRetPixel, linearPosition, MinRed, MinGreen, MinBlue, MinAlpha, MaxRed, MaxGreen, MaxBlue, MaxAlpha);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat64bppBGRA)
            {
                IPIXEL16 *pInPixel = (IPIXEL16 *)pBuffer;
                pRetPixel          = (IPIXEL32 *)_aligned_malloc(width * height * sizeof(IPIXEL32), 32);
                double scaleFactor = MAX_32BPC_PIXEL_VALUE / MAX_16BPC_PIXEL_VALUE;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition              = (y * width + x);
                        pRetPixel[linearPosition].alpha = round((double)pInPixel[linearPosition].blue * scaleFactor);
                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].green * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].red * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].alpha * scaleFactor);

                        UpdateMinMaxComponentValues(pRetPixel, linearPosition, MinRed, MinGreen, MinBlue, MinAlpha, MaxRed, MaxGreen, MaxBlue, MaxAlpha);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat48bppRGB)
            {
                R16G16B16_PIXEL *pInPixel = (R16G16B16_PIXEL *)pBuffer;
                pRetPixel                 = (IPIXEL32 *)_aligned_malloc(width * height * sizeof(IPIXEL32), 32);
                double scaleFactor        = MAX_32BPC_PIXEL_VALUE / MAX_16BPC_PIXEL_VALUE;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition              = (y * width + x);
                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].b * scaleFactor);
                        ;
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;
                        UpdateMinMaxComponentValues(pRetPixel, linearPosition, MinRed, MinGreen, MinBlue, MinAlpha, MaxRed, MaxGreen, MaxBlue, MaxAlpha);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat48bppBGR)
            {
                R16G16B16_PIXEL *pInPixel = (R16G16B16_PIXEL *)pBuffer;
                pRetPixel                 = (IPIXEL32 *)_aligned_malloc(width * height * sizeof(IPIXEL32), 32);
                double scaleFactor        = MAX_32BPC_PIXEL_VALUE / MAX_16BPC_PIXEL_VALUE;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition              = (y * width + x);
                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;
                        UpdateMinMaxComponentValues(pRetPixel, linearPosition, MinRed, MinGreen, MinBlue, MinAlpha, MaxRed, MaxGreen, MaxBlue, MaxAlpha);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat32bppRGBA)
            {
                R8G8B8A8_PIXEL *pInPixel = (R8G8B8A8_PIXEL *)pBuffer;
                pRetPixel                = (IPIXEL32 *)_aligned_malloc(width * height * sizeof(IPIXEL32), 32);
                double scaleFactor       = MAX_32BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].alpha = round((double)pInPixel[linearPosition].a * scaleFactor);
                        UpdateMinMaxComponentValues(pRetPixel, linearPosition, MinRed, MinGreen, MinBlue, MinAlpha, MaxRed, MaxGreen, MaxBlue, MaxAlpha);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat32bppBGRA)
            {
                R8G8B8A8_PIXEL *pInPixel = (R8G8B8A8_PIXEL *)pBuffer;
                pRetPixel                = (IPIXEL32 *)_aligned_malloc(width * height * sizeof(IPIXEL32), 32);
                double scaleFactor       = MAX_32BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].alpha = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].a * scaleFactor);
                        UpdateMinMaxComponentValues(pRetPixel, linearPosition, MinRed, MinGreen, MinBlue, MinAlpha, MaxRed, MaxGreen, MaxBlue, MaxAlpha);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat32bppBGR101010)
            {
                R10G10B10_PIXEL *pInPixel = (R10G10B10_PIXEL *)pBuffer;
                pRetPixel                 = (IPIXEL32 *)_aligned_malloc(width * height * sizeof(IPIXEL32), 32);
                double scaleFactor        = MAX_32BPC_PIXEL_VALUE / 1023.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE; // Ignoring 2 bit alpha
                        UpdateMinMaxComponentValues(pRetPixel, linearPosition, MinRed, MinGreen, MinBlue, MinAlpha, MaxRed, MaxGreen, MaxBlue, MaxAlpha);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat24bppRGB)
            {
                R8G8B8_PIXEL *pInPixel = (R8G8B8_PIXEL *)pBuffer;
                pRetPixel              = (IPIXEL32 *)_aligned_malloc(width * height * sizeof(IPIXEL32), 32);
                double scaleFactor     = MAX_32BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE; // Ignoring 2 bit alpha
                        UpdateMinMaxComponentValues(pRetPixel, linearPosition, MinRed, MinGreen, MinBlue, MinAlpha, MaxRed, MaxGreen, MaxBlue, MaxAlpha);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat24bppBGR)
            {
                R8G8B8_PIXEL *pInPixel = (R8G8B8_PIXEL *)pBuffer;
                pRetPixel              = (IPIXEL32 *)_aligned_malloc(width * height * sizeof(IPIXEL32), 32);
                double scaleFactor     = MAX_32BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;
                        UpdateMinMaxComponentValues(pRetPixel, linearPosition, MinRed, MinGreen, MinBlue, MinAlpha, MaxRed, MaxGreen, MaxBlue, MaxAlpha);
                    }
                }
            }

            _aligned_free(pBuffer);
        }
    }

    if (pFactory)
        pFactory->Release();

    if (pDecoder)
        pDecoder->Release();

    return pRetPixel;
}

void UpdateMinMaxComponentValues(IPIXEL32 *pRetPixel, int linearPosition, UINT32 &MinRed, UINT32 &MinGreen, UINT32 &MinBlue, UINT32 &MinAlpha, UINT32 &MaxRed, UINT32 &MaxGreen,
                                 UINT32 &MaxBlue, UINT32 &MaxAlpha)
{
    MinRed   = DD_MIN(MinRed, pRetPixel[linearPosition].red);
    MinGreen = DD_MIN(MinRed, pRetPixel[linearPosition].green);
    MinBlue  = DD_MIN(MinRed, pRetPixel[linearPosition].blue);
    MinAlpha = DD_MIN(MinRed, pRetPixel[linearPosition].alpha);

    MaxRed   = DD_MAX(MaxRed, pRetPixel[linearPosition].red);
    MaxGreen = DD_MAX(MaxRed, pRetPixel[linearPosition].green);
    MaxBlue  = DD_MAX(MaxRed, pRetPixel[linearPosition].blue);
    MaxAlpha = DD_MAX(MaxRed, pRetPixel[linearPosition].alpha);
}

IPIXEL16 *ImageIO::ReadFile16(WCHAR *pFilename, DDU32 &width, DDU32 &height)
{
    IWICImagingFactory *pFactory  = NULL;
    IWICBitmapDecoder * pDecoder  = NULL;
    IPIXEL16 *          pRetPixel = NULL;

    HRESULT hr = S_OK;
    CoInitialize(NULL);

    hr = CoCreateInstance(CLSID_WICImagingFactory, NULL, CLSCTX_INPROC_SERVER, IID_IWICImagingFactory, (LPVOID *)&pFactory);

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateDecoderFromFilename(pFilename, NULL, GENERIC_READ, WICDecodeMetadataCacheOnDemand, &pDecoder);

        if (!SUCCEEDED(hr))
        {
            return pRetPixel;
        }
    }

    DDU32 uiFrameCount = 0;
    hr                 = pDecoder->GetFrameCount(&uiFrameCount);

    if (uiFrameCount > 0)
    {
        IWICBitmapFrameDecode *Frame = NULL;
        pDecoder->GetFrame(0, &Frame);

        WICPixelFormatGUID pixFormat;
        Frame->GetPixelFormat(&pixFormat);

        DDU32 nChannels = 3, pixelCompnentSizeInBytes = 1;

        if (pixFormat == GUID_WICPixelFormat48bppRGB || pixFormat == GUID_WICPixelFormat48bppBGR || pixFormat == GUID_WICPixelFormat64bppRGBA ||
            pixFormat == GUID_WICPixelFormat64bppBGRA)
        {
            pixelCompnentSizeInBytes = 2;
        }

        if (pixFormat == GUID_WICPixelFormat32bppRGBA || pixFormat == GUID_WICPixelFormat32bppBGRA || pixFormat == GUID_WICPixelFormat64bppRGBA ||
            pixFormat == GUID_WICPixelFormat64bppBGRA || pixFormat == GUID_WICPixelFormat32bppBGR101010 || pixFormat == GUID_WICPixelFormat32bppRGBA1010102 ||
            pixFormat == GUID_WICPixelFormat32bppRGB || pixFormat == GUID_WICPixelFormat32bppBGR)
        {
            nChannels = 4;
        }

        Frame->GetSize(&width, &height);

        DDU32 bufferSize = width * height * nChannels * pixelCompnentSizeInBytes;
        BYTE *pBuffer    = (PBYTE)_aligned_malloc(bufferSize, 32);

        hr = Frame->CopyPixels(NULL, nChannels * width * pixelCompnentSizeInBytes, bufferSize, (BYTE *)pBuffer); // copy the image pixel data to buffer

        if (SUCCEEDED(hr))
        {
            if (pixFormat == GUID_WICPixelFormat64bppRGBA)
            {
                return (IPIXEL16 *)pBuffer;
            }
            else if (pixFormat == GUID_WICPixelFormat64bppBGRA)
            {
                IPIXEL16 *pInPixel = (IPIXEL16 *)pBuffer;
                pRetPixel          = (IPIXEL16 *)_aligned_malloc(width * height * sizeof(IPIXEL16), 32);

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].alpha = pInPixel[linearPosition].blue;
                        pRetPixel[linearPosition].red   = pInPixel[linearPosition].green;
                        pRetPixel[linearPosition].green = pInPixel[linearPosition].red;
                        pRetPixel[linearPosition].blue  = pInPixel[linearPosition].alpha;
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat48bppRGB)
            {
                R16G16B16_PIXEL *pInPixel = (R16G16B16_PIXEL *)pBuffer;
                pRetPixel                 = (IPIXEL16 *)_aligned_malloc(width * height * sizeof(IPIXEL16), 32);

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition              = (y * width + x);
                        pRetPixel[linearPosition].red   = pInPixel[linearPosition].r;
                        pRetPixel[linearPosition].green = pInPixel[linearPosition].g;
                        pRetPixel[linearPosition].blue  = pInPixel[linearPosition].b;
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat48bppBGR)
            {
                R16G16B16_PIXEL *pInPixel = (R16G16B16_PIXEL *)pBuffer;
                pRetPixel                 = (IPIXEL16 *)_aligned_malloc(width * height * sizeof(IPIXEL16), 32);

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition              = (y * width + x);
                        pRetPixel[linearPosition].red   = pInPixel[linearPosition].b;
                        pRetPixel[linearPosition].green = pInPixel[linearPosition].g;
                        pRetPixel[linearPosition].blue  = pInPixel[linearPosition].r;
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;
                    }
                }
            }
            else if ((pixFormat == GUID_WICPixelFormat32bppRGBA) || (pixFormat == GUID_WICPixelFormat32bppRGB))
            {
                R8G8B8A8_PIXEL *pInPixel = (R8G8B8A8_PIXEL *)pBuffer;
                pRetPixel                = (IPIXEL16 *)_aligned_malloc(width * height * sizeof(IPIXEL16), 32);
                double scaleFactor       = MAX_16BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].alpha = round((double)pInPixel[linearPosition].a * scaleFactor);
                    }
                }
            }
            else if ((pixFormat == GUID_WICPixelFormat32bppBGRA) || pixFormat == GUID_WICPixelFormat32bppBGR)
            {
                R8G8B8A8_PIXEL *pInPixel = (R8G8B8A8_PIXEL *)pBuffer;
                pRetPixel                = (IPIXEL16 *)_aligned_malloc(width * height * sizeof(IPIXEL16), 32);
                double scaleFactor       = MAX_16BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].alpha = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].a * scaleFactor);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat32bppBGR101010)
            {
                R10G10B10_PIXEL *pInPixel = (R10G10B10_PIXEL *)pBuffer;
                pRetPixel                 = (IPIXEL16 *)_aligned_malloc(width * height * sizeof(IPIXEL16), 32);
                double scaleFactor        = MAX_16BPC_PIXEL_VALUE / 1023.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE; // Ignoring 2 bit alpha
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat24bppRGB)
            {
                R8G8B8_PIXEL *pInPixel = (R8G8B8_PIXEL *)pBuffer;
                pRetPixel              = (IPIXEL16 *)_aligned_malloc(width * height * sizeof(IPIXEL16), 32);
                double scaleFactor     = MAX_16BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE; // Ignoring 2 bit alpha
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat24bppBGR)
            {
                R8G8B8_PIXEL *pInPixel = (R8G8B8_PIXEL *)pBuffer;
                pRetPixel              = (IPIXEL16 *)_aligned_malloc(width * height * sizeof(IPIXEL16), 32);
                double scaleFactor     = MAX_16BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red   = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue  = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;
                    }
                }
            }

            _aligned_free(pBuffer);
        }
    }

    if (pFactory)
        pFactory->Release();

    if (pDecoder)
        pDecoder->Release();

    return pRetPixel;
}

BOOL ImageIO::Conver8bitArrayto16BitArray(IPIXEL8 *pBitArray, DDU32 &width, DDU32 &height, IPIXEL16 *pPixArray)
{
    for (DDU32 i = 0; i < width * height; i++)
    {
        pPixArray[i].red   = pBitArray[i].red << 8;
        pPixArray[i].green = pBitArray[i].green << 8;
        pPixArray[i].blue  = pBitArray[i].blue << 8;
        pPixArray[i].alpha = 0xFF << 8; // pPixel8[i].alpha << 8;
    }
    return TRUE;
}

BOOL ImageIO::Conver10bitArrayto16BitArray(IPIXEL10 *pBitArray, DDU32 &width, DDU32 &height, IPIXEL16 *pPixArray)
{
    for (DDU32 i = 0; i < width * height; i++)
    {
        pPixArray[i].red   = pBitArray[i].red << 6;
        pPixArray[i].green = pBitArray[i].green << 6;
        pPixArray[i].blue  = pBitArray[i].blue << 6;
        pPixArray[i].alpha = 0xFFFF; // pPixel8[i].alpha << 8;
    }
    return TRUE;
}

IPIXEL16 *ImageIO::ReadFile8(WCHAR *pFilename, INT &width, INT &height)
{
    DWORD     dataSize8, dataSize16;
    IPIXEL8 * pPixel8;
    IPIXEL16 *pPixel16;

    FILE *pF = NULL;
    _wfopen_s(&pF, pFilename, L"rb");

    dataSize8 = (width * height * sizeof(IPIXEL8));
    pPixel8   = (IPIXEL8 *)malloc(dataSize8);
    if (NULL == pPixel8)
        exit;

    dataSize16 = (width * height * sizeof(IPIXEL16));
    pPixel16   = (IPIXEL16 *)malloc(dataSize16);
    if (NULL == pPixel16)
        exit;

    if (pF)
        fread(pPixel8, 1, dataSize8, pF);
    else
        printf("Failed opening the file\n");
    printf("Reading done\n");

    for (int i = 0; i < width * height; i++)
    {
        pPixel16[i].red   = pPixel8[i].red << 8;
        pPixel16[i].green = pPixel8[i].green << 8;
        pPixel16[i].blue  = pPixel8[i].blue << 8;
        pPixel16[i].alpha = 0xFF << 8; // pPixel8[i].alpha << 8;
    }
    return pPixel16;
}

DDS32 ImageIO::WriteFile(WCHAR *pFilename, UINT width, UINT height, IPIXEL32 *pPixelData, UINT MaxPixelValue, UINT8 ImageBpc)
{
    IWICImagingFactory *   pFactory     = NULL;
    IWICBitmapEncoder *    pEncoder     = NULL;
    IWICStream *           pStream      = NULL;
    IWICBitmapFrameEncode *pBitmapFrame = NULL;
    IPropertyBag2 *        pPropertyBag = NULL;
    HRESULT                hr           = S_OK;

    CoInitialize(NULL);

    _wremove(pFilename);

    hr = CoCreateInstance(CLSID_WICImagingFactory, NULL, CLSCTX_INPROC_SERVER, IID_IWICImagingFactory, (LPVOID *)&pFactory);

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateEncoder(GUID_ContainerFormatPng, NULL, &pEncoder);

        if (!SUCCEEDED(hr))
            printf(" PNG Encoder creation Failed \n");
    }

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateStream(&pStream);
        if (!SUCCEEDED(hr))
            printf(" Stream creation Failed \n");
    }

    if (SUCCEEDED(hr))
    {
        hr = pStream->InitializeFromFilename(pFilename, GENERIC_WRITE);
    }

    if (SUCCEEDED(hr))
    {
        hr = pEncoder->Initialize(pStream, WICBitmapEncoderNoCache);
    }

    if (SUCCEEDED(hr))
    {
        hr = pEncoder->CreateNewFrame(&pBitmapFrame, &pPropertyBag);
    }

    if (SUCCEEDED(hr))
    {
        hr = pBitmapFrame->Initialize(pPropertyBag);
    }

    if (SUCCEEDED(hr))
    {
        hr = pBitmapFrame->SetSize(width, height);
    }

    if (SUCCEEDED(hr))
    {
        if (8 >= ImageBpc)
        {
            WICPixelFormatGUID pixFormat = GUID_WICPixelFormat24bppBGR;
            hr                           = pBitmapFrame->SetPixelFormat(&pixFormat);

            if (pixFormat != GUID_WICPixelFormat24bppBGR)
            {
                printf("IPIXEL32 format not supporetd\n");
            }
        }
        /*if (10 == ImageBpc)
        {
            WICPixelFormatGUID pixFormat = GUID_WICPixelFormat32bppRGBA1010102XR;
            hr = pBitmapFrame->SetPixelFormat(&pixFormat);

            if (pixFormat != GUID_WICPixelFormat32bppRGBA1010102XR)
            {
                printf("IPIXEL32 format not supporetd\n");
            }
        }*/
        else // if (16 >= ImageBpc)
        {
            WICPixelFormatGUID pixFormat = GUID_WICPixelFormat64bppRGBA;
            hr                           = pBitmapFrame->SetPixelFormat(&pixFormat);

            if (pixFormat != GUID_WICPixelFormat64bppRGBA)
            {
                printf("IPIXEL32 format not supporetd\n");
            }
        }
    }

    if (SUCCEEDED(hr))
    {
        if (8 >= ImageBpc)
        {
            R8G8B8_PIXEL *pFinalPixels = (R8G8B8_PIXEL *)_aligned_malloc(sizeof(R8G8B8_PIXEL) * height * width, 32);
            const DDU32   outputMask   = ((1 << ImageBpc) - 1) << (8 - ImageBpc);

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    int linearPosition = (y * width + x);

                    pFinalPixels[linearPosition].b = round((((double)(pPixelData[linearPosition].red) / (double)(MaxPixelValue)) * 255.0));
                    pFinalPixels[linearPosition].g = round((((double)(pPixelData[linearPosition].green) / (double)(MaxPixelValue)) * 255.0));
                    pFinalPixels[linearPosition].r = round((((double)(pPixelData[linearPosition].blue) / (double)(MaxPixelValue)) * 255.0));

                    pFinalPixels[linearPosition].r &= outputMask;
                    pFinalPixels[linearPosition].g &= outputMask;
                    pFinalPixels[linearPosition].b &= outputMask;
                }
            }

            // write Buffer to output image
            hr = pBitmapFrame->WritePixels(height, (width * sizeof(R8G8B8_PIXEL)), sizeof(R8G8B8_PIXEL) * height * width, (PBYTE)pFinalPixels);
            _aligned_free(pFinalPixels);
        }
        else
        {
            IPIXEL16 *  pFinalPixels = (IPIXEL16 *)_aligned_malloc(sizeof(IPIXEL16) * height * width, 32);
            const DDU32 outputMask   = ((1 << ImageBpc) - 1) << (16 - ImageBpc);

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    int linearPosition = (y * width + x);

                    pFinalPixels[linearPosition].alpha = round((((double)(pPixelData[linearPosition].alpha) / (double)(MaxPixelValue)) * 65535.0));
                    pFinalPixels[linearPosition].red   = round((((double)(pPixelData[linearPosition].red) / (double)(MaxPixelValue)) * 65535.0));
                    pFinalPixels[linearPosition].green = round((((double)(pPixelData[linearPosition].green) / (double)(MaxPixelValue)) * 65535.0));
                    pFinalPixels[linearPosition].blue  = round((((double)(pPixelData[linearPosition].blue) / (double)(MaxPixelValue)) * 65535.0));

                    pFinalPixels[linearPosition].red &= outputMask;
                    pFinalPixels[linearPosition].green &= outputMask;
                    pFinalPixels[linearPosition].blue &= outputMask;
                }
            }
            // write Buffer to output image
            hr = pBitmapFrame->WritePixels(height, (width * sizeof(IPIXEL16)), sizeof(IPIXEL16) * height * width, (PBYTE)pFinalPixels);
            _aligned_free(pFinalPixels);
        }
    }

    if (SUCCEEDED(hr))
        hr = pBitmapFrame->Commit();

    if (SUCCEEDED(hr))
        hr = pEncoder->Commit();

    if (pFactory)
        pFactory->Release();

    if (pBitmapFrame)
        pBitmapFrame->Release();

    if (pEncoder)
        pEncoder->Release();

    if (pStream)
        pStream->Release();

    return 0;
}

DDS32 ImageIO::WriteFile(WCHAR *pFilename, UINT width, UINT height, IPIXEL16 *pPixelData, UINT MaxPixelValue, UINT8 ImageBpc)
{
    IWICImagingFactory *   pFactory     = NULL;
    IWICBitmapEncoder *    pEncoder     = NULL;
    IWICStream *           pStream      = NULL;
    IWICBitmapFrameEncode *pBitmapFrame = NULL;
    IPropertyBag2 *        pPropertyBag = NULL;
    HRESULT                hr           = S_OK;

    CoInitialize(NULL);

    _wremove(pFilename);

    hr = CoCreateInstance(CLSID_WICImagingFactory, NULL, CLSCTX_INPROC_SERVER, IID_IWICImagingFactory, (LPVOID *)&pFactory);

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateEncoder(GUID_ContainerFormatPng, NULL, &pEncoder);

        if (!SUCCEEDED(hr))
            printf(" PNG Encoder creation Failed \n");
    }

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateStream(&pStream);
        if (!SUCCEEDED(hr))
            printf(" Stream creation Failed \n");
    }

    if (SUCCEEDED(hr))
    {
        hr = pStream->InitializeFromFilename(pFilename, GENERIC_WRITE);
    }

    if (SUCCEEDED(hr))
    {
        hr = pEncoder->Initialize(pStream, WICBitmapEncoderNoCache);
    }

    if (SUCCEEDED(hr))
    {
        hr = pEncoder->CreateNewFrame(&pBitmapFrame, &pPropertyBag);
    }

    if (SUCCEEDED(hr))
    {
        hr = pBitmapFrame->Initialize(pPropertyBag);
    }

    if (SUCCEEDED(hr))
    {
        hr = pBitmapFrame->SetSize(width, height);
    }

    if (SUCCEEDED(hr))
    {
        if (8 >= ImageBpc)
        {
            WICPixelFormatGUID pixFormat = GUID_WICPixelFormat24bppBGR;
            hr                           = pBitmapFrame->SetPixelFormat(&pixFormat);

            if (pixFormat != GUID_WICPixelFormat24bppBGR)
            {
                printf("IPIXEL32 format not supporetd\n");
            }
        }
        /*if (10 == ImageBpc)
        {
            WICPixelFormatGUID pixFormat = GUID_WICPixelFormat32bppRGBA1010102XR;
            hr = pBitmapFrame->SetPixelFormat(&pixFormat);

            if (pixFormat != GUID_WICPixelFormat32bppRGBA1010102XR)
            {
                printf("IPIXEL32 format not supporetd\n");
            }
        }*/
        else // if (16 >= ImageBpc)
        {
            WICPixelFormatGUID pixFormat = GUID_WICPixelFormat64bppRGBA;
            hr                           = pBitmapFrame->SetPixelFormat(&pixFormat);

            if (pixFormat != GUID_WICPixelFormat64bppRGBA)
            {
                printf("IPIXEL32 format not supporetd\n");
            }
        }
    }

    if (SUCCEEDED(hr))
    {
        if (8 >= ImageBpc)
        {
            R8G8B8_PIXEL *pFinalPixels = (R8G8B8_PIXEL *)_aligned_malloc(sizeof(R8G8B8_PIXEL) * height * width, 32);
            const DDU32   outputMask   = ((1 << ImageBpc) - 1) << (8 - ImageBpc);

            for (int linearPosition = 0; linearPosition < (width * height); linearPosition++)
            {
                pFinalPixels[linearPosition].b = round((((double)(pPixelData[linearPosition].red) / (double)(MaxPixelValue)) * 255.0));
                pFinalPixels[linearPosition].g = round((((double)(pPixelData[linearPosition].green) / (double)(MaxPixelValue)) * 255.0));
                pFinalPixels[linearPosition].r = round((((double)(pPixelData[linearPosition].blue) / (double)(MaxPixelValue)) * 255.0));

                pFinalPixels[linearPosition].r &= outputMask;
                pFinalPixels[linearPosition].g &= outputMask;
                pFinalPixels[linearPosition].b &= outputMask;
            }

            // write Buffer to output image
            hr = pBitmapFrame->WritePixels(height, (width * sizeof(R8G8B8_PIXEL)), sizeof(R8G8B8_PIXEL) * height * width, (PBYTE)pFinalPixels);
            _aligned_free(pFinalPixels);
        }
        else
        {
            IPIXEL16 *  pFinalPixels = (IPIXEL16 *)_aligned_malloc(sizeof(IPIXEL16) * height * width, 32);
            const DDU32 outputMask   = ((1 << ImageBpc) - 1) << (16 - ImageBpc);

            for (int linearPosition = 0; linearPosition < (width * height); linearPosition++)
            {
                pFinalPixels[linearPosition].alpha = round((((double)(pPixelData[linearPosition].alpha) / (double)(MaxPixelValue)) * 65535.0));
                pFinalPixels[linearPosition].red   = round((((double)(pPixelData[linearPosition].red) / (double)(MaxPixelValue)) * 65535.0));
                pFinalPixels[linearPosition].green = round((((double)(pPixelData[linearPosition].green) / (double)(MaxPixelValue)) * 65535.0));
                pFinalPixels[linearPosition].blue  = round((((double)(pPixelData[linearPosition].blue) / (double)(MaxPixelValue)) * 65535.0));

                pFinalPixels[linearPosition].red &= outputMask;
                pFinalPixels[linearPosition].green &= outputMask;
                pFinalPixels[linearPosition].blue &= outputMask;
            }

            // write Buffer to output image
            hr = pBitmapFrame->WritePixels(height, (width * sizeof(IPIXEL16)), sizeof(IPIXEL16) * height * width, (PBYTE)pFinalPixels);
            _aligned_free(pFinalPixels);
        }
    }

    if (SUCCEEDED(hr))
        hr = pBitmapFrame->Commit();

    if (SUCCEEDED(hr))
        hr = pEncoder->Commit();

    if (pFactory)
        pFactory->Release();

    if (pBitmapFrame)
        pBitmapFrame->Release();

    if (pEncoder)
        pEncoder->Release();

    if (pStream)
        pStream->Release();

    return 0;
}

DDS32 ImageIO::WriteFile(WCHAR *pFilename, DDU32 width, DDU32 height, IPIXEL16 *pPixelData)
{
    IWICImagingFactory *   pFactory     = NULL;
    IWICBitmapEncoder *    pEncoder     = NULL;
    IWICStream *           pStream      = NULL;
    IWICBitmapFrameEncode *pBitmapFrame = NULL;
    IPropertyBag2 *        pPropertyBag = NULL;
    HRESULT                hr           = S_OK;

    CoInitialize(NULL);

    hr = CoCreateInstance(CLSID_WICImagingFactory, NULL, CLSCTX_INPROC_SERVER, IID_IWICImagingFactory, (LPVOID *)&pFactory);

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateEncoder(GUID_ContainerFormatPng, NULL, &pEncoder);

        if (!SUCCEEDED(hr))
            printf(" PNG Encoder creation Failed \n");
    }

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateStream(&pStream);
        if (!SUCCEEDED(hr))
            printf(" Stream creation Failed \n");
    }

    if (SUCCEEDED(hr))
    {
        hr = pStream->InitializeFromFilename(pFilename, GENERIC_WRITE);
    }

    if (SUCCEEDED(hr))
    {
        hr = pEncoder->Initialize(pStream, WICBitmapEncoderNoCache);
    }

    if (SUCCEEDED(hr))
    {
        hr = pEncoder->CreateNewFrame(&pBitmapFrame, &pPropertyBag);
    }

    if (SUCCEEDED(hr))
    {
        hr = pBitmapFrame->Initialize(pPropertyBag);
    }

    if (SUCCEEDED(hr))
    {
        hr = pBitmapFrame->SetSize(width, height);
    }

    if (SUCCEEDED(hr))
    {
        WICPixelFormatGUID pixFormat = GUID_WICPixelFormat64bppRGBA;
        hr                           = pBitmapFrame->SetPixelFormat(&pixFormat);

        if (pixFormat != GUID_WICPixelFormat64bppRGBA)
        {
            printf("Pixel format not supporetd\n");
        }
    }

    if (SUCCEEDED(hr))
    {
        DDU32 bufferSize = height * width * sizeof(IPIXEL16);

        // write Buffer to output image
        hr = pBitmapFrame->WritePixels(height, (width * sizeof(IPIXEL16)), bufferSize, (PBYTE)pPixelData);
    }

    if (SUCCEEDED(hr))
        hr = pBitmapFrame->Commit();

    if (SUCCEEDED(hr))
        hr = pEncoder->Commit();

    if (pFactory)
        pFactory->Release();

    if (pBitmapFrame)
        pBitmapFrame->Release();

    if (pEncoder)
        pEncoder->Release();

    if (pStream)
        pStream->Release();

    return 0;
}

IPIXEL16 *ImageIO::GetRectangle(IPIXEL16 *pSrc, DDU32 srcW, DDU32 srcH, IMAGE_RECTANGLE *pRect)
{
    if (((pRect->left + pRect->width) > srcW) || ((pRect->top + pRect->height) > srcH))
    {
        return NULL;
    }

    DDU32     nOutPixels = pRect->width * pRect->height * sizeof(IPIXEL16);
    IPIXEL16 *pOutPixel  = (IPIXEL16 *)_aligned_malloc(nOutPixels, 32);
    memset(pOutPixel, 0, nOutPixels);

    IPIXEL16 *pDstPixel = pOutPixel;

    for (DDU32 y = pRect->top; y < (pRect->top + pRect->height); y++)
    {
        for (DDU32 x = pRect->left; x < (pRect->left + pRect->width); x++)
        {
            *pDstPixel++ = pSrc[srcW * y + x];
        }
    }

    return pOutPixel;
}
