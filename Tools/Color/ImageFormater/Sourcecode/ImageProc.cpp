#include <stdio.h>
#include <math.h>
#include "ImageProc.h"
#include "ColorAlgo.h"

//#define DONOT_USE_LUT

ImageProc::ImageProc(WCHAR* pImageFile)
{
    mPixelDataTmp = NULL;

    mImageIO = new ImageIO;

    mPixelData = mImageIO->ReadFile(pImageFile, mImageHeader.width, mImageHeader.height);


    if (!mPixelData)
    {
        throw;
    }

    memcpy(mImageHeader.tag, "iimg", 4);
    mImageHeader.size = sizeof(mImageHeader);

    mImageHeader.coloInfo.size = sizeof(mImageHeader.coloInfo);
    mImageHeader.coloInfo.ecolorModel = COLOR_MODEL_RGB;
    mImageHeader.coloInfo.eColorRange = COLOR_RANGE_FULL;
    mImageHeader.coloInfo.eDataPrecision = COLOR_DATA_PRECISION_16BPC;
    mImageHeader.coloInfo.ecolorSpace = COLOR_SPACE_2020;
    mImageHeader.coloInfo.eEncoding = COLOR_ENCODING_LINEAR;
    mImageHeader.coloInfo.maxLuminance = 10000;
    mImageHeader.coloInfo.minLuminance = 0;

    //Always start with full range 16 bpc RGB image
    ColorAlgo::ComputePixelScaleFactorAndOffsets(COLOR_DATA_PRECISION_16BPC, COLOR_RANGE_FULL, &mScaleOffset);
    mMaxPixelVal = mScaleOffset.maxPixelVal;
}

ImageProc::ImageProc(DWORD width, DWORD height, IMAGE_COLOR_INFO* pColorInfo, IPIXEL* pBackground)
{
    memcpy(mImageHeader.tag, "iimg", 4);
    mImageHeader.size = sizeof(mImageHeader);
    mImageHeader.width = width;
    mImageHeader.height = height;
    mPixelDataTmp = NULL;

    if (NULL == pColorInfo)
    {
        mImageHeader.coloInfo.size = sizeof(mImageHeader.coloInfo);
        mImageHeader.coloInfo.ecolorModel = COLOR_MODEL_RGB;
        mImageHeader.coloInfo.eColorRange = COLOR_RANGE_FULL;
        mImageHeader.coloInfo.eDataPrecision = COLOR_DATA_PRECISION_16BPC;
        mImageHeader.coloInfo.ecolorSpace = COLOR_SPACE_2020;
        mImageHeader.coloInfo.eEncoding = COLOR_ENCODING_LINEAR;
        mImageHeader.coloInfo.maxLuminance = 10000;
        mImageHeader.coloInfo.minLuminance = 0;
    }
    else
    {
        mImageHeader.coloInfo = *pColorInfo;

        if (!IsmageHeaderValid())
        {
            throw;
        }
    }

    if (Initialize() != IMAGE_ERR_NONE)
    {
        throw;
    }

    InitializeBackground(pBackground);
}

ImageProc::ImageProc(WCHAR* pImageFile, DWORD width, DWORD height)
{
    FILE* pF = _wfopen(pImageFile, L"rb");

    if (!pF)
    {
        throw;
    }

    memcpy(mImageHeader.tag, "iimg", 4);
    mImageHeader.size = sizeof(mImageHeader);
    mImageHeader.width = width;
    mImageHeader.height = height;

    mImageHeader.coloInfo.size = sizeof(mImageHeader.coloInfo);
    mImageHeader.coloInfo.ecolorModel = COLOR_MODEL_RGB;
    mImageHeader.coloInfo.eColorRange = COLOR_RANGE_FULL;
    mImageHeader.coloInfo.eDataPrecision = COLOR_DATA_PRECISION_16BPC;
    mImageHeader.coloInfo.ecolorSpace = COLOR_SPACE_2020;
    mImageHeader.coloInfo.eEncoding = COLOR_ENCODING_LINEAR;
    mImageHeader.coloInfo.maxLuminance = 10000;
    mImageHeader.coloInfo.minLuminance = 0;

    mPixelDataTmp = NULL;

    if (Initialize() != IMAGE_ERR_NONE)
    {
        fclose(pF);
        throw;
    }

    DWORD dataSize = mImageHeader.width * mImageHeader.height * sizeof(IPIXEL);

    fread(mPixelData, 1, dataSize, pF);
    fclose(pF);
}

ImageProc::~ImageProc()
{
    if (mPixelData)
    {
        free(mPixelData);
        mPixelData = NULL;
    }

    if (mPixelDataTmp)
    {
        free(mPixelDataTmp);
        mPixelDataTmp = NULL;
    }
}

void ImageProc::GetImageColorInfo(IMAGE_COLOR_INFO& colorInfo)
{
    colorInfo = mImageHeader.coloInfo;
}

void ImageProc::GetImageDimension(DWORD& w, DWORD& h)
{
    w = mImageHeader.width;
    h = mImageHeader.height;

}

IMAGE_ERR ImageProc::RotateImage(DWORD dwAngle)
{
    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::ResizeImage(DWORD width, DWORD height)
{
    if (width > MAX_IMAGE_DIMENSION || height > MAX_IMAGE_DIMENSION)
    {
        return IMAGE_ERR_INVALID_PARAMETER;
    }

    if (mImageHeader.height == height && mImageHeader.width == width)
    {
        return IMAGE_ERR_NONE;
    }

    mPixelDataTmp = (IPIXEL*)malloc(width * mImageHeader.height * sizeof(IPIXEL));

    if (!mPixelDataTmp)
    {
        return IMAGE_ERR_INSUFFICIENT_MEMORY;
    }

    for (DWORD i = 0; i < mImageHeader.height; i++)
    {
        ResizeRow(i, width);
    }
    free(mPixelData);
    mPixelData = mPixelDataTmp;

    mImageHeader.width = width;
    mPixelDataTmp = (IPIXEL*)malloc(width * height * sizeof(IPIXEL));

    for (DWORD i = 0; i < mImageHeader.width; i++)
    {
        ResizeColumn(i, height);
    }

    mImageHeader.height = height;
    mImageHeader.sizeOfFile = sizeof(mImageHeader) * mImageHeader.width * mImageHeader.height * sizeof(IPIXEL);

    free(mPixelData);

    mPixelData = mPixelDataTmp;
    mPixelDataTmp = NULL;

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::ConvertToRGB(COLOR_RANGE eRange, COLOR_DATA_PRECISION ePrecision, void* pPixelData)
{
    ColorAlgo::ComputePixelScaleFactorAndOffsets(ePrecision, eRange, &mScaleOffset);

    // Scale factor for bpc conversion
    mScaleOffset.rgbScale *= (mScaleOffset.maxRGBVal + 1.0) / (mMaxPixelVal + 1.0);

    if (ePrecision == COLOR_DATA_PRECISION_10BPC)
    {
        ColorA2R10G10B10* pPix = (ColorA2R10G10B10*)pPixelData;

        for (DWORD i = 0; i < mImageHeader.height * mImageHeader.width; i++)
        {
            pPix[i].r = ConvertPixelRange(mPixelData[i].red);
            pPix[i].g = ConvertPixelRange(mPixelData[i].green);
            pPix[i].b = ConvertPixelRange(mPixelData[i].blue);
            pPix[i].a = mScaleOffset.maxPixelVal;
        }
    }
    else if (ePrecision == COLOR_DATA_PRECISION_FP16)
    {
        ColorARGBFP16* pARGB = (ColorARGBFP16*)pPixelData;

        for (DWORD i = 0; i < mImageHeader.height * mImageHeader.width; i++)
        {
            pARGB[i].r = ColorAlgo::DoubleToHalf((double)mPixelData[i].red / 65535.0);
            pARGB[i].g = ColorAlgo::DoubleToHalf((double)mPixelData[i].green / 65535.0);
            pARGB[i].b = ColorAlgo::DoubleToHalf((double)mPixelData[i].blue / 65535.0);
            pARGB[i].a = ColorAlgo::DoubleToHalf((double)mPixelData[i].alpha / 65535.0);
        }
    }

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::ConvertToYCBCR(COLOR_MODEL eModel, COLOR_RANGE eRange, COLOR_SUBSAMPLING eSampling, COLOR_DATA_PRECISION ePrecision, void* pPixelData)
{
    IMAGE_ERR retVal = IMAGE_ERR_NONE;

    ComputeRGB2YCBCRMatrix(eModel, eRange, ePrecision);

    if (eSampling == COLOR_SUBSAMPLING_444)
    {
        ConvertToYCbCr444Planar(pPixelData, ePrecision);
    }
    else if (eSampling == COLOR_SUBSAMPLING_420)
    {
        ConvertToYCbCr420Planar(pPixelData, ePrecision);
    }
    else if (eSampling == COLOR_SUBSAMPLING_422)
    {
        ConvertToYCbCr422Planar(pPixelData, ePrecision);
    }

    return retVal;
}

IMAGE_ERR ImageProc::WriteImage(WCHAR* pImageFile)
{
    IMAGE_ERR retVal = IMAGE_ERR_NONE;

    if (0 != mImageIO->WriteFile(pImageFile, mImageHeader.width, mImageHeader.height, mPixelData))
    {
        retVal = IMAGE_ERR_FILE_IO;
    }

    return retVal;
}

IMAGE_ERR ImageProc::WriteImageAsRaw(WCHAR* pImageFile)
{
    FILE* pF = _wfopen(pImageFile, L"wb");

    if (!pF)
    {
        return IMAGE_ERR_FILE_IO;
    }

    DWORD dataSize = mImageHeader.width * mImageHeader.height * sizeof(IPIXEL);

    fwrite(mPixelData, 1, dataSize, pF);

    fclose(pF);
}

IMAGE_ERR ImageProc::WriteImageAsBMP(WCHAR* pImageFile, COLOR_RANGE eRange)
{
    FILE* pF = _wfopen(pImageFile, L"wb");

    if (!pF)
    {
        return IMAGE_ERR_FILE_IO;
    }

    BMP_FILE_HEADER hdr = { 0 };

    DWORD dataSize = CreateBMPHeader(hdr);

    ColorBGR10* pPixData = (ColorBGR10*)malloc(dataSize);

    if (!pPixData)
    {
        fclose(pF);
        return IMAGE_ERR_INSUFFICIENT_MEMORY;
    }

    ColorBGR10* pBmpPix = pPixData;
    IPIXEL* pPix = mPixelData;

    ColorAlgo::ComputePixelScaleFactorAndOffsets(COLOR_DATA_PRECISION_10BPC, eRange, &mScaleOffset);

    mScaleOffset.rgbScale *= (mScaleOffset.maxPixelVal + 1.0) / (mMaxPixelVal + 1.0);

    for (DWORD y = 0; y < mImageHeader.height; y++)
    {
        for (DWORD x = 0; x < mImageHeader.width; x++)
        {
            pBmpPix->r = ConvertPixelRange(pPix->red);
            pBmpPix->g = ConvertPixelRange(pPix->green);
            pBmpPix->b = ConvertPixelRange(pPix->blue);
            pBmpPix->a = min((((DWORD)pPix->alpha + 1) >> 14), 3);             // rounding off by adding 1

            pBmpPix++;
            pPix++;
        }
    }

    fwrite(&hdr, 1, sizeof(hdr), pF);
    fwrite(pPixData, 1, dataSize, pF);

    fclose(pF);
    free(pPixData);

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::WriteImageAsBMP(WCHAR* pImageFile, COLOR_SPACE eSpace, COLOR_RANGE eRange)
{
    double iPix[3], oPix[3], convMat[3][3] = { 0 };

    FILE* pF = _wfopen(pImageFile, L"wb");

    if (!pF)
    {
        return IMAGE_ERR_FILE_IO;
    }

    if (eSpace == COLOR_SPACE_SRGB)
    {
        ColorAlgo::Create2020To709Matrix(convMat);
    }
    else if (eSpace == COLOR_SPACE_DCIP3)
    {
        ColorAlgo::Create2020ToDCIP3Matrix(convMat);
    }
    else if (eSpace == COLOR_SPACE_2020)
    {
        convMat[0][0] = convMat[1][1] = convMat[2][2] = 1.0;
        convMat[0][1] = convMat[0][2] = convMat[1][0] = 0.0;
        convMat[1][2] = convMat[2][0] = convMat[2][1] = 0.0;
    }
    else
    {
        fclose(pF);
        return IMAGE_ERR_UNSUPPORTED_FEATURE;
    }

    BMP_FILE_HEADER hdr = { 0 };

    DWORD dataSize = CreateBMPHeader(hdr);

    ColorBGR10* pPixData = (ColorBGR10*)malloc(dataSize);

    if (!pPixData)
    {
        fclose(pF);
        return IMAGE_ERR_INSUFFICIENT_MEMORY;
    }

    ColorBGR10* pBmpPix = pPixData;
    IPIXEL* pPix = mPixelData;

    ColorAlgo::ComputePixelScaleFactorAndOffsets(COLOR_DATA_PRECISION_10BPC, eRange, &mScaleOffset);
    double scaleFactor = mScaleOffset.rgbScale * mScaleOffset.maxPixelVal;

    for (DWORD y = 0; y < mImageHeader.height; y++)
    {
        for (DWORD x = 0; x < mImageHeader.width; x++)
        {
            iPix[0] = ColorAlgo::GetSRGBDecodingValue((double)pPix->red / mMaxPixelVal);
            iPix[1] = ColorAlgo::GetSRGBDecodingValue((double)pPix->green / mMaxPixelVal);
            iPix[2] = ColorAlgo::GetSRGBDecodingValue((double)pPix->blue / mMaxPixelVal);

            ColorAlgo::MatrixMult3x3With3x1(convMat, iPix, oPix);

            oPix[0] = ColorAlgo::GetSRGBEncodingValue(oPix[0]) * scaleFactor + mScaleOffset.rgbOffset;
            oPix[1] = ColorAlgo::GetSRGBEncodingValue(oPix[1]) * scaleFactor + mScaleOffset.rgbOffset;
            oPix[2] = ColorAlgo::GetSRGBEncodingValue(oPix[2]) * scaleFactor + mScaleOffset.rgbOffset;

            pBmpPix->r = ColorAlgo::Clip(oPix[0], 0, mScaleOffset.maxPixelVal);
            pBmpPix->g = ColorAlgo::Clip(oPix[1], 0, mScaleOffset.maxPixelVal);
            pBmpPix->b = ColorAlgo::Clip(oPix[2], 0, mScaleOffset.maxPixelVal);
            pBmpPix->a = min((((DWORD)pPix->alpha + 1) >> 14), 3);             // rounding off by adding 1

            pBmpPix++;
            pPix++;
        }
    }

    fwrite(&hdr, 1, sizeof(hdr), pF);
    fwrite(pPixData, 1, dataSize, pF);

    fclose(pF);
    free(pPixData);

    return IMAGE_ERR_NONE;
}


IMAGE_ERR ImageProc::GetRectangle(IMAGE_RECTANGLE* pRect, IPIXEL* pPixData)
{
    if (((pRect->left + pRect->width) > mImageHeader.width) ||
        ((pRect->top + pRect->height) > mImageHeader.height))
    {
        return IMAGE_ERR_INVALID_PARAMETER;
    }

    for (DWORD y = pRect->top; y < (pRect->top + pRect->height); y++)
    {
        for (DWORD x = pRect->left; x < (pRect->left + pRect->width); x++)
        {
            *pPixData++ = *GetPixelAtPos(x, y);
        }
    }

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::PaintRectangle(IMAGE_RECTANGLE* pRect, IPIXEL* pSolidColor)
{
    if (((pRect->left + pRect->width) > mImageHeader.width) ||
        ((pRect->top + pRect->height) > mImageHeader.height))
    {
        return IMAGE_ERR_INVALID_PARAMETER;
    }

    for (DWORD y = pRect->top; y < (pRect->top + pRect->height); y++)
    {
        for (DWORD x = pRect->left; x < (pRect->left + pRect->width); x++)
        {
            *GetPixelAtPos(x, y) = *pSolidColor;
        }
    }

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::SetRectangle(IMAGE_RECTANGLE* pRect, IPIXEL* pPixels)
{
    DWORD inputIndex = 0;

    if (((pRect->left + pRect->width) > mImageHeader.width) ||
        ((pRect->top + pRect->height) > mImageHeader.height))
    {
        return IMAGE_ERR_INVALID_PARAMETER;
    }

    for (DWORD y = pRect->top; y < (pRect->top + pRect->height); y++)
    {
        for (DWORD x = pRect->left; x < (pRect->left + pRect->width); x++)
        {
            *GetPixelAtPos(x, y) = pPixels[inputIndex];
            inputIndex++;
        }
    }

    return IMAGE_ERR_NONE;
}

void ImageProc::BlendPixels(IPIXEL* pPix1, IPIXEL* pPix2, double alpha, IMAGE_METADATA* pMetadata1, IMAGE_METADATA* pMetadata2, IMAGE_METADATA* pOutMetadata)
{
    double r1, r2, g1, g2, b1, b2;

    if (pMetadata1->encoding == COLOR_ENCODING_LINEAR && pMetadata2->encoding == COLOR_ENCODING_LINEAR &&
        pMetadata1->maxLuminance == pMetadata2->maxLuminance)
    {
        pPix1->red = round((double)pPix1->red * (1.0 - alpha) + (double)pPix2->red * alpha);
        pPix1->green = round((double)pPix1->green * (1.0 - alpha) + (double)pPix2->green * alpha);
        pPix1->blue = round((double)pPix1->blue * (1.0 - alpha) + (double)pPix2->blue * alpha);
        return;
    }

    r1 = (double)pPix1->red / 65535.0;
    g1 = (double)pPix1->green / 65535.0;
    b1 = (double)pPix1->blue / 65535.0;

    r2 = (double)pPix2->red / 65535.0;
    g2 = (double)pPix2->green / 65535.0;
    b2 = (double)pPix2->blue / 65535.0;

    if (pMetadata1->encoding == COLOR_ENCODING_22)
    {
        r1 = ColorAlgo::GetSRGBDecodingValue(r1);
        g1 = ColorAlgo::GetSRGBDecodingValue(g1);
        b1 = ColorAlgo::GetSRGBDecodingValue(b1);
    }
    else if (pMetadata1->encoding == COLOR_ENCODING_2084)
    {
        r1 = ColorAlgo::EOTF_2084(r1);
        g1 = ColorAlgo::EOTF_2084(g1);
        b1 = ColorAlgo::EOTF_2084(b1);
    }

    if (pMetadata2->encoding == COLOR_ENCODING_22)
    {
        r2 = ColorAlgo::GetSRGBDecodingValue(r2);
        g2 = ColorAlgo::GetSRGBDecodingValue(g2);
        b2 = ColorAlgo::GetSRGBDecodingValue(b2);
    }
    else if (pMetadata2->encoding == COLOR_ENCODING_2084)
    {
        r2 = ColorAlgo::EOTF_2084(r2);
        g2 = ColorAlgo::EOTF_2084(g2);
        b2 = ColorAlgo::EOTF_2084(b2);
    }

    //Always assuming output has higher max luminance
    double toneMappingFactor1 = pMetadata1->maxLuminance / pOutMetadata->maxLuminance;
    double toneMappingFactor2 = pMetadata2->maxLuminance / pOutMetadata->maxLuminance;

    r1 *= toneMappingFactor1;
    g1 *= toneMappingFactor1;
    b1 *= toneMappingFactor1;

    r2 *= toneMappingFactor2;
    g2 *= toneMappingFactor2;
    b2 *= toneMappingFactor2;

    r1 = r1 * (1.0 - alpha) + r2 * alpha;
    g1 = g1 * (1.0 - alpha) + g2 * alpha;
    b1 = b1 * (1.0 - alpha) + b2 * alpha;

    if (pOutMetadata->encoding == COLOR_ENCODING_LINEAR)
    {
        pPix1->red = min(round(65535.0 * r1), 65535);
        pPix1->green = min(round(65535.0 * g1), 65535);
        pPix1->blue = min(round(65535.0 * b1), 65535);
    }
    else if (pOutMetadata->encoding == COLOR_ENCODING_22)
    {
        pPix1->red = min(round(65535.0 * ColorAlgo::GetSRGBEncodingValue(r1)), 65535);
        pPix1->green = min(round(65535.0 * ColorAlgo::GetSRGBEncodingValue(g1)), 65535);
        pPix1->blue = min(round(65535.0 * ColorAlgo::GetSRGBEncodingValue(b1)), 65535);
    }
    else if (pOutMetadata->encoding == COLOR_ENCODING_2084)
    {
        pPix1->red = min(round(65535.0 * ColorAlgo::OETF_2084(r1)), 65535);
        pPix1->green = min(round(65535.0 * ColorAlgo::OETF_2084(g1)), 65535);
        pPix1->blue = min(round(65535.0 * ColorAlgo::OETF_2084(b1)), 65535);
    }
}

IMAGE_ERR ImageProc::BlendRectangle(IPIXEL* pPixels, double alpha, IMAGE_RECTANGLE* pBlendRect,
    IMAGE_RECTANGLE* pAlphaRect, IMAGE_METADATA* pBackgroundMetadata,
    IMAGE_METADATA* pForegroundMetadata, IMAGE_METADATA* pOutMetadata)
{
    DWORD inputIndex = 0;

    if (pBlendRect == NULL || pPixels == NULL)
    {
        return IMAGE_ERR_INVALID_PARAMETER;
    }

    DWORD xEnd = pBlendRect->left + pBlendRect->width;
    DWORD yEnd = pBlendRect->top + pBlendRect->height;

    if (xEnd > mImageHeader.width) xEnd = mImageHeader.width;
    if (yEnd > mImageHeader.height) yEnd = mImageHeader.height;

    IMAGE_METADATA backgorundMetadata, foregrounddMetadata, outMetadata;

    if (NULL != pBackgroundMetadata)
    {
        backgorundMetadata = *pBackgroundMetadata;
    }
    else
    {
        backgorundMetadata.encoding = COLOR_ENCODING_LINEAR;
        backgorundMetadata.maxLuminance = 80.0;
        backgorundMetadata.minLuminance = 0;
    }

    if (NULL != pForegroundMetadata)
    {
        foregrounddMetadata = *pForegroundMetadata;
    }
    else
    {
        foregrounddMetadata.encoding = COLOR_ENCODING_LINEAR;
        foregrounddMetadata.maxLuminance = 80.0;
        foregrounddMetadata.minLuminance = 0;
    }

    if (NULL != pOutMetadata)
    {
        outMetadata = *pOutMetadata;
    }
    else
    {
        outMetadata.encoding = COLOR_ENCODING_LINEAR;
        outMetadata.maxLuminance = 80.0;
        outMetadata.minLuminance = 0;
    }

    if (pAlphaRect == NULL)
    {
        pAlphaRect = pBlendRect;
    }

    double toneMappingFactor = outMetadata.maxLuminance / backgorundMetadata.maxLuminance;

    for (DWORD y = 0; y < mImageHeader.height; y++)
    {
        for (DWORD x = 0; x < mImageHeader.width; x++)
        {
            IPIXEL* pPix1 = GetPixelAtPos(x, y);

            //Within belnding widnow
            if (y >= pBlendRect->top && y < yEnd && x >= pBlendRect->left && x < xEnd)
            {
                IPIXEL* pPix2 = &pPixels[inputIndex];

                //Within alpha window
                if (x >= pAlphaRect->left && x < (pAlphaRect->left + pAlphaRect->width) &&
                    y >= pAlphaRect->top && y < (pAlphaRect->top + pAlphaRect->height))
                {
                    BlendPixels(pPix1, pPix2, alpha, &backgorundMetadata, &foregrounddMetadata, &outMetadata);
                }
                else
                {
                    BlendPixels(pPix1, pPix2, 1.0, &backgorundMetadata, &foregrounddMetadata, &outMetadata);
                }
                inputIndex++;
            }
            else
            {
                BlendPixels(pPix1, pPix1, 0.0, &backgorundMetadata, &foregrounddMetadata, &outMetadata);
            }
        }
    }

    return IMAGE_ERR_NONE;
}


IPIXEL* ImageProc::GetPixelArray()
{
    return mPixelData;
}

IMAGE_ERR ImageProc::ApplyLUT(OneDLUT* pLUT)
{
    for (DWORD y = 0; y < mImageHeader.height; y++)
    {
        for (DWORD x = 0; x < mImageHeader.width; x++)
        {
            IPIXEL* pPix = GetPixelAtPos(x, y);
            double r = (double)pPix->red / 65535.0;
            double g = (double)pPix->green / 65535.0;
            double b = (double)pPix->blue / 65535.0;

            pPix->red = min(round(65535.0 * ColorAlgo::ApplyLUT(pLUT, r, COLOR_CHANNEL_RED)), 65535);
            pPix->green = min(round(65535.0 * ColorAlgo::ApplyLUT(pLUT, g, COLOR_CHANNEL_GREEN)), 65535);
            pPix->blue = min(round(65535.0 * ColorAlgo::ApplyLUT(pLUT, b, COLOR_CHANNEL_BLUE)), 65535);
        }
    }

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::ApplyEOTF(COLOR_ENCODING encoding)
{
    if (encoding == COLOR_ENCODING_22)
    {
        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x++)
            {
                IPIXEL* pPix = GetPixelAtPos(x, y);
                double r = (double)pPix->red / 65535.0;
                double g = (double)pPix->green / 65535.0;
                double b = (double)pPix->blue / 65535.0;

                pPix->red = min(round(65535.0 * ColorAlgo::GetSRGBDecodingValue(r)), 65535);
                pPix->green = min(round(65535.0 * ColorAlgo::GetSRGBDecodingValue(g)), 65535);
                pPix->blue = min(round(65535.0 * ColorAlgo::GetSRGBDecodingValue(b)), 65535);
            }
        }
    }
    else if (encoding == COLOR_ENCODING_2084)
    {
        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x++)
            {
                IPIXEL* pPix = GetPixelAtPos(x, y);
                double r = (double)pPix->red / 65535.0;
                double g = (double)pPix->green / 65535.0;
                double b = (double)pPix->blue / 65535.0;

                pPix->red = min(round(65535.0 * ColorAlgo::EOTF_2084(r)), 65535);
                pPix->green = min(round(65535.0 * ColorAlgo::EOTF_2084(g)), 65535);
                pPix->blue = min(round(65535.0 * ColorAlgo::EOTF_2084(b)), 65535);
            }
        }
    }

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::ApplyOETF(COLOR_ENCODING encoding)
{
    if (encoding == COLOR_ENCODING_22)
    {
        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x++)
            {
                IPIXEL* pPix = GetPixelAtPos(x, y);
                double r = (double)pPix->red / 65535.0;
                double g = (double)pPix->green / 65535.0;
                double b = (double)pPix->blue / 65535.0;

                pPix->red = min(round(65535.0 * ColorAlgo::GetSRGBEncodingValue(r)), 65535);
                pPix->green = min(round(65535.0 * ColorAlgo::GetSRGBEncodingValue(g)), 65535);
                pPix->blue = min(round(65535.0 * ColorAlgo::GetSRGBEncodingValue(b)), 65535);
            }
        }
    }
    else if (encoding == COLOR_ENCODING_2084)
    {
        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x++)
            {
                IPIXEL* pPix = GetPixelAtPos(x, y);
                double r = (double)pPix->red / 65535.0;
                double g = (double)pPix->green / 65535.0;
                double b = (double)pPix->blue / 65535.0;

                pPix->red = min(round(65535.0 * ColorAlgo::OETF_2084(r)), 65535);
                pPix->green = min(round(65535.0 * ColorAlgo::OETF_2084(g)), 65535);
                pPix->blue = min(round(65535.0 * ColorAlgo::OETF_2084(b)), 65535);
            }
        }
    }

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::ApplyLUTAndMatrix(OneDLUT* pPreLUT, OneDLUT* pPostLUT, double ctm[3][3])
{
    double toneMappingFactor = 80.0 / 10000.0;

    for (DWORD y = 0; y < mImageHeader.height; y++)
    {
        for (DWORD x = 0; x < mImageHeader.width; x++)
        {
            IPIXEL* pPix = GetPixelAtPos(x, y);
            double inPix[3], outPix[3];

            inPix[0] = (double)pPix->red / 65535.0;
            inPix[1] = (double)pPix->green / 65535.0;
            inPix[2] = (double)pPix->blue / 65535.0;

            inPix[0] = ColorAlgo::ApplyLUT(pPreLUT, inPix[0], COLOR_CHANNEL_RED);
            inPix[1] = ColorAlgo::ApplyLUT(pPreLUT, inPix[1], COLOR_CHANNEL_GREEN);
            inPix[2] = ColorAlgo::ApplyLUT(pPreLUT, inPix[2], COLOR_CHANNEL_BLUE);

            ColorAlgo::MatrixMult3x3With3x1(ctm, inPix, outPix);

            outPix[0] = ColorAlgo::Clip(outPix[0], 0, 1);
            outPix[1] = ColorAlgo::Clip(outPix[1], 0, 1);
            outPix[2] = ColorAlgo::Clip(outPix[2], 0, 1);

            outPix[0] = ColorAlgo::ApplyLUT(pPostLUT, outPix[0], COLOR_CHANNEL_RED);
            outPix[1] = ColorAlgo::ApplyLUT(pPostLUT, outPix[1], COLOR_CHANNEL_GREEN);
            outPix[2] = ColorAlgo::ApplyLUT(pPostLUT, outPix[2], COLOR_CHANNEL_BLUE);

            pPix->red = min(round(65535.0 * outPix[0]), 65535);
            pPix->green = min(round(65535.0 * outPix[1]), 65535);
            pPix->blue = min(round(65535.0 * outPix[2]), 65535);
        }
    }

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::ApplyMatrix(double ctm[3][3], COLOR_ENCODING inpEncoding, COLOR_ENCODING outEncoding, double inpLuminance)
{
    double toneMappingFactor = inpLuminance / 10000.0;

    for (DWORD y = 0; y < mImageHeader.height; y++)
    {
        for (DWORD x = 0; x < mImageHeader.width; x++)
        {
            IPIXEL* pPix = GetPixelAtPos(x, y);
            double inPix[3], outPix[3];

            inPix[0] = (double)pPix->red / 65535.0;
            inPix[1] = (double)pPix->green / 65535.0;
            inPix[2] = (double)pPix->blue / 65535.0;

            if (inpEncoding == COLOR_ENCODING_22)
            {
                inPix[0] = ColorAlgo::GetSRGBDecodingValue(inPix[0]);
                inPix[1] = ColorAlgo::GetSRGBDecodingValue(inPix[1]);
                inPix[2] = ColorAlgo::GetSRGBDecodingValue(inPix[2]);
            }
            else if (inpEncoding == COLOR_ENCODING_2084)
            {
                inPix[0] = ColorAlgo::EOTF_2084(inPix[0]);
                inPix[1] = ColorAlgo::EOTF_2084(inPix[1]);
                inPix[2] = ColorAlgo::EOTF_2084(inPix[2]);
            }

            ColorAlgo::MatrixMult3x3With3x1(ctm, inPix, outPix);

            outPix[0] *= toneMappingFactor;
            outPix[1] *= toneMappingFactor;
            outPix[2] *= toneMappingFactor;

            if (outEncoding == COLOR_ENCODING_22)
            {
                outPix[0] = ColorAlgo::GetSRGBEncodingValue(outPix[0]);
                outPix[1] = ColorAlgo::GetSRGBEncodingValue(outPix[1]);
                outPix[2] = ColorAlgo::GetSRGBEncodingValue(outPix[2]);
            }
            else if (outEncoding == COLOR_ENCODING_2084)
            {
                outPix[0] = ColorAlgo::OETF_2084(outPix[0]);
                outPix[1] = ColorAlgo::OETF_2084(outPix[1]);
                outPix[2] = ColorAlgo::OETF_2084(outPix[2]);
            }

            pPix->red = min(round(65535.0 * outPix[0]), 65535);
            pPix->green = min(round(65535.0 * outPix[1]), 65535);
            pPix->blue = min(round(65535.0 * outPix[2]), 65535);
        }
    }

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::Initialize()
{
    DWORD dataSize = mImageHeader.width * mImageHeader.height * sizeof(IPIXEL);

    mPixelData = (IPIXEL*)malloc(dataSize);

    if (!mPixelData)
    {
        return IMAGE_ERR_INSUFFICIENT_MEMORY;
    }

    //Always start with full range 16 bpc RGB image
    ColorAlgo::ComputePixelScaleFactorAndOffsets(COLOR_DATA_PRECISION_16BPC, COLOR_RANGE_FULL, &mScaleOffset);
    mMaxPixelVal = mScaleOffset.maxPixelVal;

    double scaleFactor = mMaxPixelVal / MAX_NITS;        //MAX_NITS will be mapped to mMaxPixelVal

    if (mImageHeader.coloInfo.eDataPrecision == COLOR_DATA_PRECISION_FP16)
    {
        for (DWORD i = 0; i < (mImageHeader.width * mImageHeader.height); i++)
        {
            mPixelData[i].red = min(round(scaleFactor * ColorAlgo::HalfToDouble(mPixelData[i].red)), mMaxPixelVal);
            mPixelData[i].green = min(round(scaleFactor * ColorAlgo::HalfToDouble(mPixelData[i].green)), mMaxPixelVal);
            mPixelData[i].blue = min(round(scaleFactor * ColorAlgo::HalfToDouble(mPixelData[i].blue)), mMaxPixelVal);
            mPixelData[i].alpha = min(round(scaleFactor * ColorAlgo::HalfToDouble(mPixelData[i].alpha)), mMaxPixelVal);
        }
    }

    return IMAGE_ERR_NONE;
}

BOOL ImageProc::IsmageHeaderValid()
{
    if (mImageHeader.width > MAX_IMAGE_DIMENSION || mImageHeader.height > MAX_IMAGE_DIMENSION)
    {
        return FALSE;
    }

    if (memcmp(mImageHeader.tag, "iimg", 4) != 0)
    {
        return FALSE;
    }

    if (mImageHeader.size != sizeof(mImageHeader))
    {
        return FALSE;
    }

    if (mImageHeader.coloInfo.size != sizeof(mImageHeader.coloInfo))
    {
        return FALSE;
    }

    if (mImageHeader.coloInfo.ecolorModel != COLOR_MODEL_RGB)
    {
        return FALSE;
    }

    if (mImageHeader.coloInfo.eColorRange != COLOR_RANGE_FULL)
    {
        return FALSE;
    }

    if (mImageHeader.coloInfo.eDataPrecision != COLOR_DATA_PRECISION_16BPC &&
        mImageHeader.coloInfo.eDataPrecision != COLOR_DATA_PRECISION_FP16)
    {
        return FALSE;
    }

    if (mImageHeader.coloInfo.ecolorSpace != COLOR_SPACE_2020)
    {
        return FALSE;
    }

    if (mImageHeader.coloInfo.eEncoding != COLOR_ENCODING_LINEAR)
    {
        return FALSE;
    }

    return TRUE;
}

void ImageProc::InitializeBackground(IPIXEL* pBackground)
{
    IPIXEL background;

    if (pBackground)
    {
        background = *pBackground;
    }
    else
    {
        background.red = background.green = background.blue = background.alpha = mMaxPixelVal;
    }

    IPIXEL* pPix = mPixelData;

    for (DWORD i = 0; i < (mImageHeader.width * mImageHeader.height); i++)
    {
        *pPix++ = background;
    }
}

IMAGE_ERR ImageProc::ConvertToYCbCr444Planar(void* pPixelData, COLOR_DATA_PRECISION ePrecision)
{
    if (ePrecision == COLOR_DATA_PRECISION_8BPC)
    {
        UINT8* pY = (UINT8*)pPixelData;
        UINT8* pCb = pY + (mImageHeader.height * mImageHeader.width);
        UINT8* pCr = pCb + (mImageHeader.height * mImageHeader.width);

        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x++)
            {
                ConvertPixelToYCBCR(GetPixelAtPos(x, y), pY, pCb, pCr);
                pY++;
                pCb++;
                pCr++;
            }
        }
    }
    else if (ePrecision == COLOR_DATA_PRECISION_FP16)
    {
        //TBD
    }
    else
    {
        UINT16* pY = (UINT16*)pPixelData;
        UINT16* pCb = pY + (mImageHeader.height * mImageHeader.width);
        UINT16* pCr = pCb + (mImageHeader.height * mImageHeader.width);

        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x++)
            {
                ConvertPixelToYCBCR(GetPixelAtPos(x, y), pY, pCb, pCr);
                pY++;
                pCb++;
                pCr++;
            }
        }
    }

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::ConvertToYCbCr420Planar(void* pPixelData, COLOR_DATA_PRECISION ePrecision)
{
    if (ePrecision == COLOR_DATA_PRECISION_8BPC)
    {
        UINT8 tmp;
        UINT8* pY = (UINT8*)pPixelData;
        UINT8* pCb = pY + (mImageHeader.height * mImageHeader.width);
        UINT8* pCr = pCb + (mImageHeader.height * mImageHeader.width) / 4;

        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x++)
            {
                ConvertPixelToYCBCR(GetPixelAtPos(x, y), pY, pCb, pCr);
                pY++;
            }
        }

        for (DWORD y = 0; y < mImageHeader.height; y += 2)
        {
            for (DWORD x = 0; x < mImageHeader.width; x += 2)
            {
                ConvertPixelToYCBCR(GetPixelAtPos(x, y), &tmp, pCb, pCr);
                pCb++;
                pCr++;
            }
        }
    }
    else if (ePrecision == COLOR_DATA_PRECISION_FP16)
    {
        //TBD
    }
    else
    {
        UINT16 tmp;
        UINT16* pY = (UINT16*)pPixelData;
        UINT16* pCb = pY + (mImageHeader.height * mImageHeader.width);
        UINT16* pCr = pCb + (mImageHeader.height * mImageHeader.width) / 4;

        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x++)
            {
                ConvertPixelToYCBCR(GetPixelAtPos(x, y), pY, pCb, pCr);
                pY++;
            }
        }

        for (DWORD y = 0; y < mImageHeader.height; y += 2)
        {
            for (DWORD x = 0; x < mImageHeader.width; x += 2)
            {
                ConvertPixelToYCBCR(GetPixelAtPos(x, y), &tmp, pCb, pCr);
                pCb++;
                pCr++;
            }
        }
    }

    return IMAGE_ERR_NONE;
}

IMAGE_ERR ImageProc::ConvertToYCbCr422Planar(void* pPixelData, COLOR_DATA_PRECISION ePrecision)
{
    if (ePrecision == COLOR_DATA_PRECISION_8BPC)
    {
        UINT8 tmp[2];
        UINT8* pY = (UINT8*)pPixelData;
        UINT8* pCb = pY + (mImageHeader.height * mImageHeader.width);
        UINT8* pCr = pCb + (mImageHeader.height * mImageHeader.width) / 2;

        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x++)
            {
                ConvertPixelToYCBCR(GetPixelAtPos(x, y), pY, pCb, pCr);
                pY++;
            }

            for (DWORD y = 0; y < mImageHeader.height; y++)
            {
                for (DWORD x = 0; x < mImageHeader.width; x += 2)
                {
                    ConvertPixelToYCBCR(GetPixelAtPos(x, y), &tmp[0], pCb, &tmp[1]);
                    ConvertPixelToYCBCR(GetPixelAtPos((x + 1), y), &tmp[0], &tmp[1], pCr);
                    pCb++;
                    pCr++;
                }
            }
        }
    }
    else if (ePrecision == COLOR_DATA_PRECISION_FP16)
    {
        //TBD
    }
    else
    {
        UINT16 tmp[2];
        UINT16* pY = (UINT16*)pPixelData;
        UINT16* pCb = pY + (mImageHeader.height * mImageHeader.width);
        UINT16* pCr = pCb + (mImageHeader.height * mImageHeader.width) / 2;

        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x++)
            {
                ConvertPixelToYCBCR(GetPixelAtPos(x, y), pY, pCb, pCr);
                pY++;
            }
        }

        for (DWORD y = 0; y < mImageHeader.height; y++)
        {
            for (DWORD x = 0; x < mImageHeader.width; x += 2)
            {
                ConvertPixelToYCBCR(GetPixelAtPos(x, y), &tmp[0], pCb, &tmp[1]);
                ConvertPixelToYCBCR(GetPixelAtPos((x + 1), y), &tmp[0], &tmp[1], pCr);
                pCb++;
                pCr++;
            }
        }
    }

    return IMAGE_ERR_NONE;
}

void ImageProc::ConvertPixelToYCBCR(IPIXEL* pRGB, UINT16* pY, UINT16* pCb, UINT16* pCr)
{
    double dY = mScaleOffset.yOffset + mYCbCrMat[0][0] * (double)pRGB->red + mYCbCrMat[0][1] * (double)pRGB->green + mYCbCrMat[0][2] * (double)pRGB->blue;
    double dCb = mScaleOffset.cbCrOffset + mYCbCrMat[1][0] * (double)pRGB->red + mYCbCrMat[1][1] * (double)pRGB->green + mYCbCrMat[1][2] * (double)pRGB->blue;
    double dCr = mScaleOffset.cbCrOffset + mYCbCrMat[2][0] * (double)pRGB->red + mYCbCrMat[2][1] * (double)pRGB->green + mYCbCrMat[2][2] * (double)pRGB->blue;

    *pY = min(round(dY), mScaleOffset.maxYVal);
    *pCb = min(round(dCb), mScaleOffset.maxCbCrVal);
    *pCr = min(round(dCr), mScaleOffset.maxCbCrVal);
}

void ImageProc::ConvertPixelToYCBCR(IPIXEL* pRGB, UINT8* pY, UINT8* pCb, UINT8* pCr)
{
    double dY = mScaleOffset.yOffset + mYCbCrMat[0][0] * (double)pRGB->red + mYCbCrMat[0][1] * (double)pRGB->green + mYCbCrMat[0][2] * (double)pRGB->blue;
    double dCb = mScaleOffset.cbCrOffset + mYCbCrMat[1][0] * (double)pRGB->red + mYCbCrMat[1][1] * (double)pRGB->green + mYCbCrMat[1][2] * (double)pRGB->blue;
    double dCr = mScaleOffset.cbCrOffset + mYCbCrMat[2][0] * (double)pRGB->red + mYCbCrMat[2][1] * (double)pRGB->green + mYCbCrMat[2][2] * (double)pRGB->blue;

    *pY = min(round(dY), mScaleOffset.maxYVal);
    *pCb = min(round(dCb), mScaleOffset.maxCbCrVal);
    *pCr = min(round(dCr), mScaleOffset.maxCbCrVal);
}


void ImageProc::ComputeRGB2YCBCRMatrix(COLOR_MODEL eModel, COLOR_RANGE eRange, COLOR_DATA_PRECISION ePrecision)
{
    ColorAlgo::CreateRGB2YCbCrMatrix(eModel, mYCbCrMat);
    ColorAlgo::ComputePixelScaleFactorAndOffsets(ePrecision, eRange, &mScaleOffset);

    double yScaleFactor = (mScaleOffset.maxPixelVal + 1.0) / (mMaxPixelVal + 1.0);// Scale factor for bpc conversion
    double cbCrScaleFactor = yScaleFactor;

    if (eRange == COLOR_RANGE_LIMITED)
    {
        yScaleFactor *= mScaleOffset.yScale;
        cbCrScaleFactor *= mScaleOffset.cbCrScale;
    }

    mYCbCrMat[0][0] *= yScaleFactor;
    mYCbCrMat[0][1] *= yScaleFactor;
    mYCbCrMat[0][2] *= yScaleFactor;

    mYCbCrMat[1][0] *= cbCrScaleFactor;
    mYCbCrMat[1][1] *= cbCrScaleFactor;
    mYCbCrMat[1][2] *= cbCrScaleFactor;

    mYCbCrMat[2][0] *= cbCrScaleFactor;
    mYCbCrMat[2][1] *= cbCrScaleFactor;
    mYCbCrMat[2][2] *= cbCrScaleFactor;
}

UINT16 ImageProc::ConvertPixelRange(UINT16 data)
{
    double out = (double)data * mScaleOffset.rgbScale + mScaleOffset.rgbOffset;
    out = min(round(out), mScaleOffset.maxRGBVal);

    return out;
}

void ImageProc::InterpolatePixel(IPIXEL* p1, IPIXEL* p2, IPIXEL* pResult, double a)
{
    double b = 1.0 - a;

    pResult->red = (double)p1->red * b + (double)p2->red * a;
    pResult->green = (double)p1->green * b + (double)p2->green * a;
    pResult->blue = (double)p1->blue * b + (double)p2->blue * a;
    pResult->alpha = (double)p1->alpha * b + (double)p2->alpha * a;
}

void ImageProc::ResizeRow(DWORD rowIndex, DWORD targetWidth)
{
    DWORD i;
    IPIXEL* pDst = &mPixelDataTmp[targetWidth * rowIndex];

    double scaleRatio = (double)(mImageHeader.width - 1) / (double)(targetWidth - 1);

    for (i = 0; i < (targetWidth - 1); i++)
    {
        double srcPixelIndex = (double)i * scaleRatio;
        DWORD nearestIndex = srcPixelIndex;                    // Nearest Neighbour
        double diffIndex = srcPixelIndex - (double)nearestIndex;

        IPIXEL* p1 = GetPixelAtPos(nearestIndex++, rowIndex);
        IPIXEL* p2 = GetPixelAtPos(nearestIndex, rowIndex);

        InterpolatePixel(p1, p2, &pDst[i], diffIndex);
    }

    pDst[i] = *GetPixelAtPos((mImageHeader.width - 1), rowIndex);
}

void ImageProc::ResizeColumn(DWORD columnIndex, DWORD targetHeight)
{
    DWORD i;

    //TODO Resize a horizontal line from mPixelData;
    double scaleRatio = (double)(mImageHeader.height - 1) / (double)(targetHeight - 1);

    for (i = 0; i < (targetHeight - 1); i++)
    {
        double srcPixelIndex = (double)i * scaleRatio;
        DWORD nearestIndex = srcPixelIndex;                     // Nearest Neighbour ----??
        double diffIndex = srcPixelIndex - (double)nearestIndex;

        IPIXEL* p1 = GetPixelAtPos(columnIndex, srcPixelIndex++);
        IPIXEL* p2 = GetPixelAtPos(columnIndex, srcPixelIndex);

        InterpolatePixel(p1, p2, &mPixelDataTmp[i * mImageHeader.width + columnIndex], diffIndex);
    }

    mPixelDataTmp[i * mImageHeader.width + columnIndex] = *GetPixelAtPos(columnIndex, (mImageHeader.height - 1));
}

IPIXEL* ImageProc::GetPixelAtPos(DWORD x, DWORD y)
{
    return &mPixelData[mImageHeader.width * y + x];
}

DWORD ImageProc::CreateBMPHeader(BMP_FILE_HEADER& hdr)
{
    DWORD dwDataSize = mImageHeader.width * mImageHeader.height * sizeof(ColorBGR10);

    hdr.hdr.bfType = 0x4D42;
    hdr.hdr.bfSize = sizeof(BMP_FILE_HEADER) + dwDataSize;
    hdr.hdr.bfOffBits = sizeof(BMP_FILE_HEADER);
    hdr.infoHdr.bV4Size = sizeof(BITMAPV4HEADER);
    hdr.infoHdr.bV4Width = mImageHeader.width;
    hdr.infoHdr.bV4Height = -(int)(mImageHeader.height);
    hdr.infoHdr.bV4Planes = 1;
    hdr.infoHdr.bV4BitCount = 32;
    hdr.infoHdr.bV4V4Compression = BI_BITFIELDS;
    hdr.infoHdr.bV4RedMask = BMP_RED_MASK;
    hdr.infoHdr.bV4GreenMask = BMP_GREEN_MASK;
    hdr.infoHdr.bV4BlueMask = BMP_BLUE_MASK;

    return dwDataSize;
}



