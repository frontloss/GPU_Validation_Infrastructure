#include "ImageIO.h"

IPIXEL* ImageIO::ReadFile(WCHAR* pFilename, UINT& width, UINT& height)
{
    IWICImagingFactory* pFactory = NULL;
    IWICBitmapDecoder* pDecoder = NULL;
    IPIXEL* pRetPixel = NULL;

    HRESULT hr = S_OK;
    CoInitialize(NULL);

    hr = CoCreateInstance(CLSID_WICImagingFactory, NULL, CLSCTX_INPROC_SERVER, IID_IWICImagingFactory, (LPVOID*)&pFactory);

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateDecoderFromFilename(pFilename, NULL, GENERIC_READ, WICDecodeMetadataCacheOnDemand, &pDecoder);

        if (!SUCCEEDED(hr))
        {
            return pRetPixel;
        }
    }

    UINT uiFrameCount = 0;
    hr = pDecoder->GetFrameCount(&uiFrameCount);

    if (uiFrameCount > 0)
    {
        IWICBitmapFrameDecode* Frame = NULL;
        pDecoder->GetFrame(0, &Frame);

        WICPixelFormatGUID pixFormat;
        Frame->GetPixelFormat(&pixFormat);

        DWORD nChannels = 3, pixelCompnentSizeInBytes = 1;

        if (pixFormat == GUID_WICPixelFormat48bppRGB || pixFormat == GUID_WICPixelFormat48bppBGR || pixFormat == GUID_WICPixelFormat64bppRGBA || pixFormat == GUID_WICPixelFormat64bppBGRA)
        {
            pixelCompnentSizeInBytes = 2;
        }

        if (pixFormat == GUID_WICPixelFormat32bppRGBA || pixFormat == GUID_WICPixelFormat32bppBGRA || pixFormat == GUID_WICPixelFormat64bppRGBA ||
            pixFormat == GUID_WICPixelFormat64bppBGRA || pixFormat == GUID_WICPixelFormat32bppBGR101010 || pixFormat == GUID_WICPixelFormat32bppRGBA1010102)
        {
            nChannels = 4;
        }

        Frame->GetSize(&width, &height);

        UINT bufferSize = width * height * nChannels * pixelCompnentSizeInBytes;
        BYTE* pBuffer = (PBYTE)malloc(bufferSize);

        hr = Frame->CopyPixels(NULL, nChannels * width * pixelCompnentSizeInBytes, bufferSize, (BYTE*)pBuffer); //copy the image pixel data to buffer

        if (SUCCEEDED(hr))
        {
            if (pixFormat == GUID_WICPixelFormat64bppRGBA)
            {
                return (IPIXEL*)pBuffer;
            }
            else if (pixFormat == GUID_WICPixelFormat64bppBGRA)
            {
                R16G16B16A16_PIXEL* pInPixel = (R16G16B16A16_PIXEL*)pBuffer;
                pRetPixel = (IPIXEL*)malloc(width * height * sizeof(IPIXEL));

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].alpha = pInPixel[linearPosition].b;
                        pRetPixel[linearPosition].red = pInPixel[linearPosition].g;
                        pRetPixel[linearPosition].green = pInPixel[linearPosition].r;
                        pRetPixel[linearPosition].blue = pInPixel[linearPosition].a;
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat48bppRGB)
            {
                R16G16B16_PIXEL* pInPixel = (R16G16B16_PIXEL*)pBuffer;
                pRetPixel = (IPIXEL*)malloc(width * height * sizeof(IPIXEL));

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);
                        pRetPixel[linearPosition].red = pInPixel[linearPosition].r;
                        pRetPixel[linearPosition].green = pInPixel[linearPosition].g;
                        pRetPixel[linearPosition].blue = pInPixel[linearPosition].b;
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat48bppBGR)
            {
                R16G16B16_PIXEL* pInPixel = (R16G16B16_PIXEL*)pBuffer;
                pRetPixel = (IPIXEL*)malloc(width * height * sizeof(IPIXEL));

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);
                        pRetPixel[linearPosition].red = pInPixel[linearPosition].b;
                        pRetPixel[linearPosition].green = pInPixel[linearPosition].g;
                        pRetPixel[linearPosition].blue = pInPixel[linearPosition].r;
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat32bppRGBA)
            {
                R8G8B8A8_PIXEL* pInPixel = (R8G8B8A8_PIXEL*)pBuffer;
                pRetPixel = (IPIXEL*)malloc(width * height * sizeof(IPIXEL));
                double scaleFactor = MAX_16BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].alpha = round((double)pInPixel[linearPosition].a * scaleFactor);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat32bppBGRA)
            {
                R8G8B8A8_PIXEL* pInPixel = (R8G8B8A8_PIXEL*)pBuffer;
                pRetPixel = (IPIXEL*)malloc(width * height * sizeof(IPIXEL));
                double scaleFactor = MAX_16BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].alpha = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].red = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].blue = round((double)pInPixel[linearPosition].a * scaleFactor);
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat32bppBGR101010)
            {
                R10G10B10_PIXEL* pInPixel = (R10G10B10_PIXEL*)pBuffer;
                pRetPixel = (IPIXEL*)malloc(width * height * sizeof(IPIXEL));
                double scaleFactor = MAX_16BPC_PIXEL_VALUE / 1023.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;// Ignoring 2 bit alpha
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat24bppRGB)
            {
                R8G8B8_PIXEL* pInPixel = (R8G8B8_PIXEL*)pBuffer;
                pRetPixel = (IPIXEL*)malloc(width * height * sizeof(IPIXEL));
                double scaleFactor = MAX_16BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;// Ignoring 2 bit alpha
                    }
                }
            }
            else if (pixFormat == GUID_WICPixelFormat24bppBGR)
            {
                R8G8B8_PIXEL* pInPixel = (R8G8B8_PIXEL*)pBuffer;
                pRetPixel = (IPIXEL*)malloc(width * height * sizeof(IPIXEL));
                double scaleFactor = MAX_16BPC_PIXEL_VALUE / 255.0;

                for (int y = 0; y < height; y++)
                {
                    for (int x = 0; x < width; x++)
                    {
                        int linearPosition = (y * width + x);

                        pRetPixel[linearPosition].red = round((double)pInPixel[linearPosition].b * scaleFactor);
                        pRetPixel[linearPosition].green = round((double)pInPixel[linearPosition].g * scaleFactor);
                        pRetPixel[linearPosition].blue = round((double)pInPixel[linearPosition].r * scaleFactor);
                        pRetPixel[linearPosition].alpha = ALPHA_OPAQUE;
                    }
                }
            }

            free(pBuffer);
        }
    }

    if (pFactory)
        pFactory->Release();

    if (pDecoder)
        pDecoder->Release();

    return pRetPixel;
}


int ImageIO::WriteFile(WCHAR* pFilename, UINT width, UINT height, IPIXEL* pPixelData)
{
    IWICImagingFactory* pFactory = NULL;
    IWICBitmapEncoder* pEncoder = NULL;
    IWICStream* pStream = NULL;
    IWICBitmapFrameEncode* pBitmapFrame = NULL;
    IPropertyBag2* pPropertyBag = NULL;
    HRESULT hr = S_OK;

    CoInitialize(NULL);

    hr = CoCreateInstance(CLSID_WICImagingFactory, NULL, CLSCTX_INPROC_SERVER, IID_IWICImagingFactory, (LPVOID*)&pFactory);

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateEncoder(GUID_ContainerFormatPng, NULL, &pEncoder);

        if (!SUCCEEDED(hr))
            printf(" PNG Encoder creation Failed \n");
    }

    if (SUCCEEDED(hr))
    {
        hr = pFactory->CreateStream(&pStream);
        if (!SUCCEEDED(hr)) printf(" Stream creation Failed \n");
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
        hr = pBitmapFrame->SetPixelFormat(&pixFormat);

        if (pixFormat != GUID_WICPixelFormat64bppRGBA)
        {
            printf("Pixel format not supported\n");
        }
    }

    if (SUCCEEDED(hr))
    {
        UINT bufferSize = height * width * sizeof(IPIXEL);

        //write Buffer to output image
        hr = pBitmapFrame->WritePixels(height, (width * sizeof(IPIXEL)), bufferSize, (PBYTE)pPixelData);
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