#include"ImageFormater.h"

int YtillingBuffer(char* inData, int width, int height, int format, char* OutData);  //tilling remap function in surface conversion.cpp


int ImageFormater::SetBufferParameters(IMAGEPROPERTIES imageProperties)
{
    mImageProperties = imageProperties;
    return 0;
}

//Linaer processing
void ImageFormater::ProcessLinear(wchar_t* inFileName, IPIXEL* pImageData)
{
    ImageProc Image(inFileName);
    Image.ResizeImage(mImageProperties.width, mImageProperties.height);
    DWORD a, b;
    Image.GetImageDimension(a, b);

    IPIXEL* inImageData = Image.GetPixelArray();

    if (mImageProperties.pixelFormat == SB_R8G8B8X8 || mImageProperties.pixelFormat == SB_R8G8B8A8)
    {
        RGBA8 pixelRGB, * RGB8 = (RGBA8*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double scalefactor = 255.0 / 65535.0;
        int linearPosition = 0;

        for (int row = 0; row < mImageProperties.height; row++)
        {
            for (int col = 0; col < mImageProperties.width; col++)
            {
                pixelRGB.r = round(pixel[linearPosition].red * scalefactor);
                pixelRGB.g = round(pixel[linearPosition].green * scalefactor);
                pixelRGB.b = round(pixel[linearPosition].blue * scalefactor);
                pixelRGB.a = round(pixel[linearPosition].alpha * scalefactor);

                RGB8[linearPosition] = pixelRGB;
                linearPosition++;
            }
        }
    }
    else if (mImageProperties.pixelFormat == SB_B8G8R8X8 || mImageProperties.pixelFormat == SB_B8G8R8A8)
    {

        BGRA8 pixelRGB, * RGB8 = (BGRA8*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double scalefactor = 255.0 / 65535.0;
        int linearPosition = 0;

        for (int row = 0; row < mImageProperties.height; row++)
        {
            for (int col = 0; col < mImageProperties.width; col++)
            {
                pixelRGB.b = round(pixel[linearPosition].blue * scalefactor);
                pixelRGB.g = round(pixel[linearPosition].green * scalefactor);
                pixelRGB.r = round(pixel[linearPosition].red * scalefactor);
                pixelRGB.a = round(pixel[linearPosition].alpha * scalefactor);

                RGB8[linearPosition] = pixelRGB;
                linearPosition++;
            }

        }

    }
    else if (mImageProperties.pixelFormat == SB_R10G10B10X2 || mImageProperties.pixelFormat == SB_R10G10B10A2)
    {
        UINT32 r, g, b, a;
        R10G10B10A2* RGB10 = (R10G10B10A2*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double scalefactor = 1023.0 / 65535.0;
        int linearPosition = 0;
        for (int row = 0; row < mImageProperties.height; row++)
        {
            for (int col = 0; col < mImageProperties.width; col++)
            {
                r = round(pixel[linearPosition].red * scalefactor);
                g = round(pixel[linearPosition].green * scalefactor);
                b = round(pixel[linearPosition].blue * scalefactor);
                a = round(pixel[linearPosition].alpha * 3.0 / 65535.0);
                RGB10[linearPosition].a = a;
                RGB10[linearPosition].r = r;
                RGB10[linearPosition].g = g;
                RGB10[linearPosition].b = b;
                linearPosition++;
            }
        }
    }
    else if (mImageProperties.pixelFormat == SB_B10G10R10X2 || mImageProperties.pixelFormat == SB_B10G10R10A2)
    {
        UINT32 r, g, b, a;
        B10G10R10A2* RGB10 = (B10G10R10A2*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double scalefactor = 1023.0 / 65535.0;
        int linearPosition = 0;

        for (int row = 0; row < mImageProperties.height; row++)
        {
            for (int col = 0; col < mImageProperties.width; col++)
            {
                r = round(pixel[linearPosition].blue * scalefactor);
                g = round(pixel[linearPosition].green * scalefactor);
                b = round(pixel[linearPosition].red * scalefactor);
                a = round(pixel[linearPosition].alpha * 3.0 / 65535.0);
                RGB10[linearPosition].a = a;
                RGB10[linearPosition].r = r;
                RGB10[linearPosition].g = g;
                RGB10[linearPosition].b = b;
                linearPosition++;
            }
        }


    }
    else if (mImageProperties.pixelFormat == SB_R16G16B16X16F || mImageProperties.pixelFormat == SB_R16G16B16A16F)
    {
        R16G16B16A16_PIXEL pixelFP16, * FP16 = (R16G16B16A16_PIXEL*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double r, g, b, a;
        int linearPosition = 0;
        double R, G, B, rgb[3];

        for (int row = 0; row < mImageProperties.height; row++)
        {
            for (int col = 0; col < mImageProperties.width; col++)
            {
                r = (double)pixel[linearPosition].red / 65535.0;
                g = (double)pixel[linearPosition].green / 65535.0;
                b = (double)pixel[linearPosition].blue / 65535.0;
                a = (double)pixel[linearPosition].alpha / 65535.0;

                if (mImageProperties.HDR == 1)
                {

                    R = ColorAlgo::EOTF_2084(r);
                    G = ColorAlgo::EOTF_2084(g);
                    B = ColorAlgo::EOTF_2084(b);

                    rgb[0] = R * mImageProperties.brightness_unit;//brightness unit 10000/80 by default
                    rgb[1] = G * mImageProperties.brightness_unit;
                    rgb[2] = B * mImageProperties.brightness_unit;

                    ColorUtils::MatrixMultiply3X1With3X3(rgb, BT2020_TO_BT709_RGB);

                    r = rgb[0];
                    g = rgb[1];
                    b = rgb[2];
                }



                pixelFP16.r = ColorAlgo::DoubleToHalf(r);
                pixelFP16.g = ColorAlgo::DoubleToHalf(g);
                pixelFP16.b = ColorAlgo::DoubleToHalf(b);
                pixelFP16.a = ColorAlgo::DoubleToHalf(a);

                FP16[linearPosition].r = pixelFP16.r;
                FP16[linearPosition].g = pixelFP16.g;
                FP16[linearPosition].b = pixelFP16.b;
                FP16[linearPosition].a = pixelFP16.a;

                linearPosition++;
            }
        }

    }
    else if (mImageProperties.pixelFormat == SB_NV12YUV420)
    {
        UINT8* Y = (UINT8*)pImageData;
        UINT16* CbCr = (UINT16*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double dYValue, dCbValue, dCrValue;
        UINT yValue, cbValue, crValue;
        double rgb2YCbCr[3][3], offset[3];
        int n4KBlocks = ((mImageProperties.width + 4095) & 0xF000) >> 12;
        mImageProperties.height = (mImageProperties.height + 1) & (0xFFFE);   //height should be always an even number
        ColorUtils::ComputeRgb2YcbcrMatrix(EIGHT, LIMITED, SDTV, rgb2YCbCr, offset);
        int CbCrOffset = (mImageProperties.height * 4096 * n4KBlocks) >> 1;   //CbCr starts at end of Y
        CbCr = CbCr + CbCrOffset;

        int CbCrLinearPosition = 0, CbCrCounter = 0;
        double r, g, b, a;
        int i = 0;
        int row, col, writeLinearPosition = 0;
        long  readposition = 0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            for (col = 0; col < mImageProperties.width; col++)
            {
                i = i + 1;

                r = (double)pixel[readposition].red / 65535;
                g = (double)pixel[readposition].green / 65535;
                b = (double)pixel[readposition].blue / 65535;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 255);
                cbValue = round(dCbValue * 255);
                crValue = round(dCrValue * 255);

                Y[writeLinearPosition++] = yValue;

                if (row % 2 == 0 && col % 2 == 0)  //2:1 sampling in horizontal and vertical
                {
                    CbCr[CbCrLinearPosition++] = crValue << 8 | cbValue;
                }

            }

            memset((Y + writeLinearPosition), 0, (n4KBlocks * 4096) - col);
            if (row % 2 == 0)
            {
                memset((CbCr + CbCrLinearPosition), 128, (n4KBlocks * 4096) - col);
            }

        }
    }
    else if (mImageProperties.pixelFormat == SB_P016YUV420 || mImageProperties.pixelFormat == SB_P012YUV420 || mImageProperties.pixelFormat == SB_P010YUV420)
    {
        UINT16* Y = (UINT16*)pImageData;
        UINT32* CbCr = (UINT32*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double dYValue, dCbValue, dCrValue;
        UINT16 yValue, cbValue, crValue;
        double rgb2YCbCr[3][3], offset[3];
        int CbCrLinearPosition = 0, CbCrCounter = 0;
        int yBytecount = 0, cbCrByteCount = 0;
        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;

        int n4KBlocks = ((mImageProperties.width + 4095) & 0xF000) >> 12;  //ceil of divided by 4096 (multiple of 4096 bytes)
        mImageProperties.height = (mImageProperties.height + 1) & (0xFFFE); //height should be always an even number
        int CbCrOffset = (mImageProperties.height * 4096 * n4KBlocks) >> 2;   //CbCr starts at end of Y
        CbCr = CbCr + CbCrOffset;
        ColorUtils::ComputeRgb2YcbcrMatrix(SIXTEEN, LIMITED, SDTV, rgb2YCbCr, offset);

        for (row = 0; row < mImageProperties.height; row++)
        {
            yBytecount = 0;
            if (row % 2 == 0)
                cbCrByteCount = 0;
            for (col = 0; col < (mImageProperties.width); col++)
            {
                r = (double)pixel[readposition].red / 65535;
                g = (double)pixel[readposition].green / 65535;
                b = (double)pixel[readposition].blue / 65535;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 65535);
                cbValue = round(dCbValue * 65535);
                crValue = round(dCrValue * 65535);

                Y[writeLinearPosition++] = yValue;
                yBytecount = yBytecount + 2;

                if (row % 2 == 0 && col % 2 == 0)  //2:1 sampling in horizontal and vertical
                {
                    CbCr[CbCrLinearPosition++] = crValue << 16 | cbValue;
                    cbCrByteCount = cbCrByteCount + 4;
                }

            }

            while (yBytecount < (n4KBlocks * 4096)) //padding to Y , make stride aligned to 4k
            {

                Y[writeLinearPosition++] = 0x00;
                yBytecount = yBytecount + 2;
            }

            while (cbCrByteCount < (n4KBlocks * 4096)) //padding to UV ,make stride aligned to 4k
            {
                CbCr[CbCrLinearPosition++] = 0x8000 << 16 | 0x8000;
                cbCrByteCount = cbCrByteCount + 4;
            }
        }
    }
    else if (mImageProperties.pixelFormat == SB_YUV444_8)
    {
        UINT8* wp = (UINT8*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double dYValue, dCbValue, dCrValue;
        UINT yValue, cbValue, crValue, alpha;
        double rgb2YCbCr[3][3], offset[3];

        ColorUtils::ComputeRgb2YcbcrMatrix(EIGHT, LIMITED, SDTV, rgb2YCbCr, offset);

        int CbCrLinearPosition = 0, CbCrCounter = 0;
        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;
        double scaleFactor = 255.0 / 65535.0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            for (col = 0; col < mImageProperties.width; col++)
            {
                r = (double)pixel[readposition].red / 65535.0;
                g = (double)pixel[readposition].green / 65535.0;
                b = (double)pixel[readposition].blue / 65535.0;
                a = (double)pixel[readposition].alpha / 65535.0;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 255);
                cbValue = round(dCbValue * 255);
                crValue = round(dCrValue * 255);
                alpha = round(a * 255);

                wp[writeLinearPosition++] = crValue;
                wp[writeLinearPosition++] = cbValue;
                wp[writeLinearPosition++] = yValue;
                wp[writeLinearPosition++] = alpha;
            }

        }
    }
    else if (mImageProperties.pixelFormat == SB_YUV444_10)
    {
        Cb10Y10Cr10A2* wp = (Cb10Y10Cr10A2*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double dYValue, dCbValue, dCrValue;
        UINT16 yValue, cbValue, crValue, alpha;
        double rgb2YCbCr[3][3], offset[3];

        ColorUtils::ComputeRgb2YcbcrMatrix(SIXTEEN, LIMITED, SDTV, rgb2YCbCr, offset);

        int CbCrLinearPosition = 0, CbCrCounter = 0;
        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;


        for (row = 0; row < mImageProperties.height; row++)
        {
            for (col = 0; col < mImageProperties.width; col++)
            {
                r = (double)pixel[readposition].red / 65535.0;
                g = (double)pixel[readposition].green / 65535.0;
                b = (double)pixel[readposition].blue / 65535.0;
                a = (double)pixel[readposition].alpha / 65535.0;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 1023);
                cbValue = round(dCbValue * 1023);
                crValue = round(dCrValue * 1023);
                alpha = round(a * 3);

                wp[writeLinearPosition].a = alpha;
                wp[writeLinearPosition].cr = crValue;
                wp[writeLinearPosition].y = yValue;
                wp[writeLinearPosition].cb = cbValue;

            }

        }
    }
    else if (mImageProperties.pixelFormat == SB_YUV444_16 || mImageProperties.pixelFormat == SB_YUV444_12)
    {
        UINT16* wp = (UINT16*)pImageData;
        IPIXEL pixel;
        double dYValue, dCbValue, dCrValue;
        UINT16 yValue, cbValue, crValue, alpha;
        double rgb2YCbCr[3][3], offset[3];

        ColorUtils::ComputeRgb2YcbcrMatrix(SIXTEEN, LIMITED, SDTV, rgb2YCbCr, offset);

        int CbCrLinearPosition = 0, CbCrCounter = 0;
        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;
        double scaleFactor = 255.0 / 65535.0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            for (col = 0; col < mImageProperties.width; col++)
            {
                IPIXEL* pixel = (IPIXEL*)inImageData;

                r = (double)pixel[readposition].red / 65535.0;
                g = (double)pixel[readposition].green / 65535.0;
                b = (double)pixel[readposition].blue / 65535.0;
                a = (double)pixel[readposition].alpha;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 65535);
                cbValue = round(dCbValue * 65535);
                crValue = round(dCrValue * 65535);
                alpha = round(a);

                wp[writeLinearPosition++] = cbValue;
                wp[writeLinearPosition++] = yValue;
                wp[writeLinearPosition++] = crValue;
                wp[writeLinearPosition++] = alpha;
            }

        }
    }
    else if (mImageProperties.pixelFormat == SB_YUV422)
    {
        UINT8* WritePtr = (UINT8*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double dYValue, dCbValue, dCrValue;
        UINT yValue, cbValue, crValue;
        double rgb2YCbCr[3][3], offset[3];

        ColorUtils::ComputeRgb2YcbcrMatrix(EIGHT, LIMITED, SDTV, rgb2YCbCr, offset);

        int CbCrLinearPosition = 0, CbCrCounter = 0;
        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            for (col = 0; col < mImageProperties.width; col++)
            {
                r = (double)pixel[readposition].red / 65535;
                g = (double)pixel[readposition].green / 65535;
                b = (double)pixel[readposition].blue / 65535;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 255);
                cbValue = round(dCbValue * 255);
                crValue = round(dCrValue * 255);

                WritePtr[writeLinearPosition++] = yValue;

                if (col % 2 == 0)  //each y acompnaied with one of the chroma
                {
                    WritePtr[writeLinearPosition++] = cbValue;
                }
                else
                {
                    WritePtr[writeLinearPosition++] = crValue;
                }

            }

        }
    }
    else if (mImageProperties.pixelFormat == SB_YUV422_16 || mImageProperties.pixelFormat == SB_YUV422_12 || mImageProperties.pixelFormat == SB_YUV422_10)
    {
        UINT16* WritePtr = (UINT16*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double dYValue, dCbValue, dCrValue;
        UINT16 yValue, cbValue, crValue;
        double rgb2YCbCr[3][3], offset[3];

        ColorUtils::ComputeRgb2YcbcrMatrix(SIXTEEN, LIMITED, SDTV, rgb2YCbCr, offset);

        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            for (col = 0; col < mImageProperties.width; col++)
            {
                r = (double)pixel[readposition].red / 65535;
                g = (double)pixel[readposition].green / 65535;
                b = (double)pixel[readposition].blue / 65535;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 65535);
                cbValue = round(dCbValue * 65535);
                crValue = round(dCrValue * 65535);

                WritePtr[writeLinearPosition++] = yValue;

                if (col % 2 == 0)  //each y acompnaied with one of the chroma
                {
                    WritePtr[writeLinearPosition++] = cbValue;
                }
                else
                {
                    WritePtr[writeLinearPosition++] = crValue;
                }

            }

        }
    }
}



//y tilled processing
void ImageFormater::ProcessYTilled(wchar_t* inFileName, IPIXEL* pImageData)
{
    ImageProc Image(inFileName);
    Image.ResizeImage(mImageProperties.width, mImageProperties.height);
    IPIXEL* inImageData = Image.GetPixelArray();

    if (mImageProperties.pixelFormat == SB_R8G8B8X8 || mImageProperties.pixelFormat == SB_R8G8B8A8)
    {

        RGBA8 pixelRGB, * RGB8 = (RGBA8*)pImageData;
        IPIXEL pixel, * inPixel;
        inPixel = (IPIXEL*)inImageData;
        int row = 0, col = 0;
        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 4 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes)
        int bytesWritenInLine = 0;
        int linearPosition = 0;

        double scalefactor = 255.0 / 65535.0;
        for (row = 0; row < mImageProperties.height; row++)
        {
            bytesWritenInLine = 0;
            for (col = 0; col < mImageProperties.width; col++)
            {
                pixelRGB.r = round(inPixel[linearPosition].red * scalefactor);
                pixelRGB.g = round(inPixel[linearPosition].green * scalefactor);
                pixelRGB.b = round(inPixel[linearPosition].blue * scalefactor);
                pixelRGB.a = round(inPixel[linearPosition].alpha * scalefactor);

                RGB8[linearPosition].r = pixelRGB.r;
                RGB8[linearPosition].g = pixelRGB.g;
                RGB8[linearPosition].b = pixelRGB.b;
                RGB8[linearPosition].a = pixelRGB.a;

                linearPosition++;
                bytesWritenInLine += 4;

            }
            for (; bytesWritenInLine < nTiles * 128;) //row padding for pithch is multiple of tilewidth
            {
                RGB8[linearPosition++] = { 0, 0, 0, 0 };
                bytesWritenInLine += 4;
            }

        }

        for (; row < 64 * n64Rows; row++)
        {
            bytesWritenInLine = 0;
            for (; bytesWritenInLine < nTiles * 128;) //row padding for pithch is multiple of tilewidth
            {
                RGB8[linearPosition++] = { 0, 0, 0, 0 };
                bytesWritenInLine += 4;
            }
        }

        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64);
        YtillingBuffer((char*)RGB8, nTiles * 128, n64Rows * 64, 5, (char*)dest_buffer);
        memcpy(RGB8, dest_buffer, nTiles * 128 * n64Rows * 64);
        free(dest_buffer);
    }
    else if (mImageProperties.pixelFormat == SB_B8G8R8X8 || mImageProperties.pixelFormat == SB_B8G8R8A8)
    {

        BGRA8 pixelRGB, * RGB8 = (BGRA8*)pImageData;
        IPIXEL* inPixel = (IPIXEL*)inImageData;
        double scalefactor = 255.0 / 65535.0;

        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 4 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes)
        int bytesPerLine = 0;
        int row = 0, col = 0;
        int linearPosition = 0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            bytesPerLine = 0;
            for (col = 0; col < mImageProperties.width; col++)
            {
                pixelRGB.b = round(inPixel[linearPosition].blue * scalefactor);
                pixelRGB.g = round(inPixel[linearPosition].green * scalefactor);
                pixelRGB.r = round(inPixel[linearPosition].red * scalefactor);
                pixelRGB.a = round(inPixel[linearPosition].alpha * scalefactor);

                RGB8[linearPosition].a = pixelRGB.a;
                RGB8[linearPosition].r = pixelRGB.r;
                RGB8[linearPosition].g = pixelRGB.g;
                RGB8[linearPosition].b = pixelRGB.b;

                linearPosition++;
                bytesPerLine += 4;

            }
            for (; bytesPerLine < nTiles * 128;) //padding for pithch is multiple of tilewidth
            {
                RGB8[linearPosition++] = { 0, 0, 0, 0 };
                bytesPerLine += 4;
            }

        }

        for (; row < 64 * n64Rows; row++)   //padding rows ;rows must be multiple of 64
        {
            bytesPerLine = 0;
            for (; bytesPerLine < nTiles * 128;) //padding for pithch is multiple of tilewidth
            {
                RGB8[linearPosition++] = { 0, 0, 0, 0 };
                bytesPerLine += 4;
            }
        }

        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64);  //allocate memory for tilled output
        YtillingBuffer((char*)RGB8, nTiles * 128, n64Rows * 64, 5, (char*)dest_buffer);    //tilling rearragement
        memcpy(RGB8, dest_buffer, nTiles * 128 * n64Rows * 64);                            //replace the memory with tilled output
        free(dest_buffer);

    }
    else if (mImageProperties.pixelFormat == SB_R10G10B10X2 || mImageProperties.pixelFormat == SB_R10G10B10A2)
    {
        UINT32 r, g, b, a;
        R10G10B10A2* RGB10 = (R10G10B10A2*)pImageData;
        IPIXEL* RGBin = (IPIXEL*)inImageData;
        IPIXEL pixel;
        int row = 0, col = 0;
        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 4 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes)
        int bytesWritenInLine = 0;
        int linearPosition = 0;
        double scalefactor = 1023.0 / 65535.0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            bytesWritenInLine = 0;
            for (col = 0; col < mImageProperties.width; col++)
            {
                r = round(RGBin[linearPosition].red * scalefactor);
                g = round(RGBin[linearPosition].green * scalefactor);
                b = round(RGBin[linearPosition].blue * scalefactor);
                a = round(RGBin[linearPosition].alpha * 3.0 / 65535.0);

                RGB10[linearPosition].a = a;
                RGB10[linearPosition].r = r;
                RGB10[linearPosition].g = g;
                RGB10[linearPosition].b = b;

                linearPosition++;
                bytesWritenInLine += 4;
            }
            for (; bytesWritenInLine < nTiles * 128;) //row padding for pithch is multiple of tilewidth
            {
                RGB10[linearPosition++] = { 0, 0, 0, 0 };
                bytesWritenInLine += 4;
            }

        }

        for (; row < 64 * n64Rows; row++)
        {
            bytesWritenInLine = 0;
            for (; bytesWritenInLine < nTiles * 128;) //row padding for pithch is multiple of tilewidth
            {
                RGB10[linearPosition++] = { 0, 0, 0, 0 };
                bytesWritenInLine += 4;
            }
        }
        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64);  //allocate memory for tilled output
        YtillingBuffer((char*)RGB10, nTiles * 128, n64Rows * 64, 5, (char*)dest_buffer);    //tilling rearragement
        memcpy(RGB10, dest_buffer, nTiles * 128 * n64Rows * 64);                            //replace the memory with tilled output
        free(dest_buffer);

    }
    else if (mImageProperties.pixelFormat == SB_B10G10R10X2 || mImageProperties.pixelFormat == SB_B10G10R10A2)
    {
        UINT32 r, g, b, a;
        B10G10R10A2* RGB10 = (B10G10R10A2*)pImageData;
        IPIXEL* RGBin = (IPIXEL*)inImageData;
        IPIXEL pixel;
        int row = 0, col = 0;
        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 4 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes)
        int bytesWritenInLine = 0;
        int linearPosition = 0;
        double scalefactor = 1023.0 / 65535.0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            bytesWritenInLine = 0;
            for (col = 0; col < mImageProperties.width; col++)
            {
                r = round(RGBin[linearPosition].red * scalefactor);
                g = round(RGBin[linearPosition].green * scalefactor);
                b = round(RGBin[linearPosition].blue * scalefactor);
                a = round(RGBin[linearPosition].alpha * 3.0 / 65535.0);

                RGB10[linearPosition].a = a;
                RGB10[linearPosition].r = r;
                RGB10[linearPosition].g = g;
                RGB10[linearPosition].b = b;

                linearPosition++;
                bytesWritenInLine += 4;
            }
            for (; bytesWritenInLine < nTiles * 128;) //row padding for pithch is multiple of tilewidth
            {
                RGB10[linearPosition++] = { 0, 0, 0, 0 };
                bytesWritenInLine += 4;
            }

        }

        for (; row < 64 * n64Rows; row++)
        {
            bytesWritenInLine = 0;
            for (; bytesWritenInLine < nTiles * 128;) //row padding for pithch is multiple of tilewidth
            {
                RGB10[linearPosition++] = { 0, 0, 0, 0 };
                bytesWritenInLine += 4;
            }
        }

        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64);  //allocate memory for tilled output
        YtillingBuffer((char*)RGB10, nTiles * 128, n64Rows * 64, 5, (char*)dest_buffer);    //tilling rearragement
        memcpy(RGB10, dest_buffer, nTiles * 128 * n64Rows * 64);                            //replace the memory with tilled output
        free(dest_buffer);

    }
    else if (mImageProperties.pixelFormat == SB_R16G16B16X16F || mImageProperties.pixelFormat == SB_R16G16B16A16F)
    {
        R16G16B16A16_PIXEL pixelFP16, * FP16 = (R16G16B16A16_PIXEL*)pImageData;
        IPIXEL* pixel = (IPIXEL*)inImageData;
        double r, g, b, a;
        int linearPosition = 0;
        int row = 0;
        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 8 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes) ;FP-16 has 4 components of 2 bytes each
        int bytesWritenInLine = 0;
        double rgb[3], R, G, B;

        for (row = 0; row < mImageProperties.height; row++)
        {
            bytesWritenInLine = 0;
            for (int col = 0; col < mImageProperties.width; col++)
            {
                r = (double)pixel[linearPosition].red / 65535.0;
                g = (double)pixel[linearPosition].green / 65535.0;
                b = (double)pixel[linearPosition].blue / 65535.0;
                a = (double)pixel[linearPosition].alpha / 65535.0;

                if (mImageProperties.HDR == 1)
                {

                    R = ColorAlgo::EOTF_2084(r);
                    G = ColorAlgo::EOTF_2084(g);
                    B = ColorAlgo::EOTF_2084(b);

                    rgb[0] = R * 125.0;
                    rgb[1] = G * 125.0;
                    rgb[2] = B * 125.0;

                    ColorUtils::MatrixMultiply3X1With3X3(rgb, BT2020_TO_BT709_RGB);

                    r = rgb[0];
                    g = rgb[1];
                    b = rgb[2];
                }
                pixelFP16.r = ColorAlgo::DoubleToHalf(r);
                pixelFP16.g = ColorAlgo::DoubleToHalf(g);
                pixelFP16.b = ColorAlgo::DoubleToHalf(b);
                pixelFP16.a = ColorAlgo::DoubleToHalf(a);

                FP16[linearPosition].r = pixelFP16.r;
                FP16[linearPosition].g = pixelFP16.g;
                FP16[linearPosition].b = pixelFP16.b;
                FP16[linearPosition].a = pixelFP16.a;

                bytesWritenInLine += 8;
                linearPosition++;
            }

            for (; bytesWritenInLine < nTiles * 128;)
            {
                FP16[linearPosition] = { 0, 0, 0, 0 };
                linearPosition++;
                bytesWritenInLine += 8;
            }
        }
        for (; row < n64Rows * 64; row++)
        {
            for (bytesWritenInLine = 0; bytesWritenInLine < nTiles * 128;)
            {
                FP16[linearPosition] = { 0, 0, 0, 0 };
                linearPosition++;
                bytesWritenInLine += 8;
            }
        }

        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64);  //allocate memory for tilled output
        YtillingBuffer((char*)FP16, nTiles * 128, n64Rows * 64, 5, (char*)dest_buffer);    //tilling rearragement
        memcpy(FP16, dest_buffer, nTiles * 128 * n64Rows * 64);                            //replace the memory with tilled output
        free(dest_buffer);
    }
    else if (mImageProperties.pixelFormat == SB_NV12YUV420)
    {
        UINT8* Y = (UINT8*)pImageData;
        UINT16* CbCr = (UINT16*)pImageData;
        IPIXEL pixel;
        double dYValue, dCbValue, dCrValue;
        UINT yValue, cbValue, crValue;
        double rgb2YCbCr[3][3], offset[3];

        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes)
        int CbCrLinearPosition = 0, CbCrCounter = 0;
        double r, g, b, a, rgb[3];
        int row, col, writeLinearPosition = 0;
        int readposition = 0;
        ColorUtils::ComputeRgb2YcbcrMatrix(EIGHT, LIMITED, SDTV, rgb2YCbCr, offset);
        CbCr = CbCr + (INT)round((n64Rows * 64 * nTiles * 128) / 2.0);

        for (row = 0; row < mImageProperties.height; row++)
        {
            for (col = 0; col < mImageProperties.width; col++)
            {
                IPIXEL* pixel = (IPIXEL*)inImageData;

                rgb[0] = (double)pixel[readposition].red / 65535;
                rgb[1] = (double)pixel[readposition].green / 65535;
                rgb[2] = (double)pixel[readposition].blue / 65535;
                readposition += 1;

                ColorUtils::MatrixMultiply3X1With3X3(rgb, rgb2YCbCr);

                dYValue = rgb[0] + offset[0];  //rgb to YCbCr conversion offset
                dCbValue = rgb[1] + offset[1];
                dCrValue = rgb[2] + offset[2];

                yValue = round(dYValue * 255);         //scale to 8 bit value
                cbValue = round(dCbValue * 255);
                crValue = round(dCrValue * 255);

                Y[writeLinearPosition++] = yValue;   //write the luma component;no sampling

                if (row % 2 == 0 && col % 2 == 0)  //2:1 sampling in horizontal and vertical for chroma
                {
                    CbCr[CbCrLinearPosition++] = crValue << 8 | cbValue;
                }

            }

            for (; col < nTiles * 128; col++) // padding for pithch is multiple of tilewidth
            {
                Y[writeLinearPosition++] = 0;

                if (row % 2 == 0 && col % 2 == 0)  //2:1 sampling in horizontal and vertical for chroma nt
                {
                    CbCr[CbCrLinearPosition++] = 0 << 8 | 0;
                }
            }

        }
        for (; row < 64 * n64Rows; row++) //padding to reach rows as multiple of 64
        {
            for (col = 0; col < mImageProperties.width; col++)
            {
                Y[writeLinearPosition++] = 0x00;
                if (row % 2 == 0 && col % 2 == 0)  //2:1 sampling in horizontal and vertical
                {
                    CbCr[CbCrLinearPosition++] = 0 << 8 | 0;
                }
            }
        }
        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64 * 1.5);  //allocate memory for tilled output
        YtillingBuffer((char*)pImageData, nTiles * 128, n64Rows * 64, 1, (char*)dest_buffer);    //tilling rearragement
        memcpy(pImageData, dest_buffer, nTiles * 128 * n64Rows * 64 * 1.5);                            //replace the memory with tilled output
        free(dest_buffer);
    }
    else if (mImageProperties.pixelFormat == SB_P016YUV420 || mImageProperties.pixelFormat == SB_P012YUV420 || mImageProperties.pixelFormat == SB_P010YUV420)
    {
        UINT16* Y = (UINT16*)pImageData;
        UINT32* CbCr = (UINT32*)pImageData;
        IPIXEL pixel;
        double dYValue, dCbValue, dCrValue;
        UINT16 yValue, cbValue, crValue;

        double rgb2YCbCr[3][3], offset[3];

        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 2 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes); each pixels of 2 Byte component

        ColorUtils::ComputeRgb2YcbcrMatrix(SIXTEEN, LIMITED, SDTV, rgb2YCbCr, offset);

        CbCr = CbCr + (INT)round((n64Rows * 64 * nTiles * 128) / 4.0);  //set to UV start address

        int CbCrLinearPosition = 0;
        int yBytecount = 0, cbCrByteCount = 0;
        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            yBytecount = 0;
            if (row % 2 == 0)
                cbCrByteCount = 0;
            for (col = 0; col < (mImageProperties.width); col++)
            {
                IPIXEL* pixel = (IPIXEL*)inImageData;

                r = (double)pixel[readposition].red / 65535;
                g = (double)pixel[readposition].green / 65535;
                b = (double)pixel[readposition].blue / 65535;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 65535);
                cbValue = round(dCbValue * 65535);
                crValue = round(dCrValue * 65535);

                Y[writeLinearPosition++] = yValue;
                yBytecount += 2;


                if (row % 2 == 0 && col % 2 == 0)  //2:1 sampling in horizontal and vertical
                {
                    CbCr[CbCrLinearPosition++] = crValue << 16 | cbValue;
                    cbCrByteCount += 4;
                }

            }

            for (; yBytecount < nTiles * 128; yBytecount += 2)
            {
                Y[writeLinearPosition++] = 0;
            }
            for (; cbCrByteCount < nTiles * 128; cbCrByteCount += 4)
            {
                CbCr[CbCrLinearPosition++] = 0 << 16 | 0;
            }
        }


        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64 * 1.5);  //allocate memory for tilled output
        YtillingBuffer((char*)pImageData, nTiles * 128, n64Rows * 64, 2, (char*)dest_buffer);    //tilling rearragement
        memcpy(pImageData, dest_buffer, nTiles * 128 * n64Rows * 64 * 1.5);                            //replace the memory with tilled output
        free(dest_buffer);
    }
    else if (mImageProperties.pixelFormat == SB_YUV444_8)
    {

        RGBA8* writePointer = (RGBA8*)pImageData;
        IPIXEL pixel;
        double dYValue, dCbValue, dCrValue;
        UINT yValue, cbValue, crValue, alpha;
        double rgb2YCbCr[3][3], offset[3];

        ColorUtils::ComputeRgb2YcbcrMatrix(EIGHT, LIMITED, SDTV, rgb2YCbCr, offset);

        int CbCrLinearPosition = 0, CbCrCounter = 0;
        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;
        double scaleFactor = 255.0 / 65535.0;
        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 4 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes);each pixel 4 components
        int rowByteCount = 0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            rowByteCount = 0;
            for (col = 0; col < mImageProperties.width; col++)
            {
                IPIXEL* pixel = (IPIXEL*)inImageData;

                r = (double)pixel[readposition].red / 65535.0;
                g = (double)pixel[readposition].green / 65535.0;
                b = (double)pixel[readposition].blue / 65535.0;
                a = (double)pixel[readposition].alpha / 65535.0;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 255);
                cbValue = round(dCbValue * 255);
                crValue = round(dCrValue * 255);
                alpha = round(a * 255);

                writePointer[writeLinearPosition].a = crValue;
                writePointer[writeLinearPosition].r = cbValue;
                writePointer[writeLinearPosition].g = yValue;
                writePointer[writeLinearPosition++].b = alpha;
                rowByteCount += 4;
            }

            for (; rowByteCount < nTiles * 128;)
            {
                writePointer[writeLinearPosition].a = 0;
                writePointer[writeLinearPosition].r = 0;
                writePointer[writeLinearPosition].g = 0;
                writePointer[writeLinearPosition++].b = 0;
                rowByteCount += 4;
            }

        }
        for (; row < n64Rows * 64; row++)
        {
            rowByteCount = 0;
            for (; rowByteCount < nTiles * 128;)
            {
                writePointer[writeLinearPosition].a = 0;
                writePointer[writeLinearPosition].r = 0;
                writePointer[writeLinearPosition].g = 0;
                writePointer[writeLinearPosition++].b = 0;
                rowByteCount += 4;
            }
        }

        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64);  //allocate memory for tilled output
        YtillingBuffer((char*)pImageData, nTiles * 128, n64Rows * 64, 5, (char*)dest_buffer);    //tilling rearragement
        memcpy(pImageData, dest_buffer, nTiles * 128 * n64Rows * 64);                            //replace the memory with tilled output
        free(dest_buffer);

    }
    else if (mImageProperties.pixelFormat == SB_YUV444_10)
    {
        UINT32* wp = (UINT32*)pImageData;
        IPIXEL pixel;
        double dYValue, dCbValue, dCrValue;
        UINT16 yValue, cbValue, crValue, alpha;
        double rgb2YCbCr[3][3], offset[3];

        ColorUtils::ComputeRgb2YcbcrMatrix(SIXTEEN, LIMITED, SDTV, rgb2YCbCr, offset);

        int CbCrLinearPosition = 0, CbCrCounter = 0;
        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;

        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 4 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes);each pixel 4 components

        int rowByteCount = 0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            rowByteCount = 0;
            for (col = 0; col < mImageProperties.width; col++)
            {
                IPIXEL* pixel = (IPIXEL*)inImageData;

                r = (double)pixel[readposition].red / 65535.0;
                g = (double)pixel[readposition].green / 65535.0;
                b = (double)pixel[readposition].blue / 65535.0;
                a = (double)pixel[readposition].alpha / 65535.0;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 1023);
                cbValue = round(dCbValue * 1023);
                crValue = round(dCrValue * 1023);
                alpha = round(a * 3);

                wp[writeLinearPosition++] = alpha << 30 | crValue << 20 | yValue << 10 | cbValue;
                rowByteCount += 4;

            }
            for (; rowByteCount < nTiles * 128;)
            {
                wp[writeLinearPosition++] = 0;
                rowByteCount += 4;
            }

        }
        for (; row < n64Rows * 64; row++)
        {
            rowByteCount = 0;
            for (; rowByteCount < nTiles * 128;)
            {
                wp[writeLinearPosition++] = 0;
                rowByteCount += 4;
            }
        }

        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64);  //allocate memory for tilled output
        YtillingBuffer((char*)pImageData, nTiles * 128, n64Rows * 64, 5, (char*)dest_buffer);    //tilling rearragement
        memcpy(pImageData, dest_buffer, nTiles * 128 * n64Rows * 64);                            //replace the memory with tilled output
        free(dest_buffer);
    }
    else if (mImageProperties.pixelFormat == SB_YUV444_16 || mImageProperties.pixelFormat == SB_YUV444_12)
    {
        UINT16* wp = (UINT16*)pImageData;
        double dYValue, dCbValue, dCrValue;
        UINT16 yValue, cbValue, crValue, alpha;
        double rgb2YCbCr[3][3], offset[3];

        ColorUtils::ComputeRgb2YcbcrMatrix(SIXTEEN, LIMITED, SDTV, rgb2YCbCr, offset);

        int CbCrLinearPosition = 0, CbCrCounter = 0;
        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;
        double scaleFactor = 255.0 / 65535.0;
        IPIXEL* pixel = (IPIXEL*)inImageData;

        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 8 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes);each pixel 4 2-Byte components
        int rowByteCount = 0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            rowByteCount = 0;
            for (col = 0; col < mImageProperties.width; col++)
            {

                r = (double)pixel[readposition].red / 65535.0;
                g = (double)pixel[readposition].green / 65535.0;
                b = (double)pixel[readposition].blue / 65535.0;
                a = (double)pixel[readposition].alpha;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 65535);
                cbValue = round(dCbValue * 65535);
                crValue = round(dCrValue * 65535);
                alpha = round(a);

                wp[writeLinearPosition++] = cbValue;
                wp[writeLinearPosition++] = yValue;
                wp[writeLinearPosition++] = crValue;
                wp[writeLinearPosition++] = alpha;
                rowByteCount += 8;
            }

            for (; rowByteCount < nTiles * 128;)
            {
                wp[writeLinearPosition++] = 0;
                wp[writeLinearPosition++] = 0;
                wp[writeLinearPosition++] = 0;
                wp[writeLinearPosition++] = 0;
                rowByteCount += 8;
            }
        }
        for (; row < n64Rows * 64; row++)
        {
            rowByteCount = 0;
            for (; rowByteCount < nTiles * 128;)
            {
                wp[writeLinearPosition++] = 0;
                wp[writeLinearPosition++] = 0;
                wp[writeLinearPosition++] = 0;
                wp[writeLinearPosition++] = 0;
                rowByteCount += 8;
            }
        }

        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64);  //allocate memory for tilled output
        YtillingBuffer((char*)pImageData, nTiles * 128, n64Rows * 64, 5, (char*)dest_buffer);    //tilling rearragement
        memcpy(pImageData, dest_buffer, nTiles * 128 * n64Rows * 64);                            //replace the memory with tilled output
        free(dest_buffer);
    }
    else if (mImageProperties.pixelFormat == SB_YUV422)
    {
        UINT8* WritePtr = (UINT8*)pImageData;
        double dYValue, dCbValue, dCrValue;
        UINT yValue, cbValue, crValue;
        double rgb2YCbCr[3][3], offset[3];

        ColorUtils::ComputeRgb2YcbcrMatrix(EIGHT, LIMITED, SDTV, rgb2YCbCr, offset);

        IPIXEL* pixel = (IPIXEL*)inImageData;
        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;


        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 2 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes);
        int rowByteCount = 0;


        for (row = 0; row < mImageProperties.height; row++)
        {
            rowByteCount = 0;
            for (col = 0; col < mImageProperties.width; col++)
            {


                r = (double)pixel[readposition].red / 65535;
                g = (double)pixel[readposition].green / 65535;
                b = (double)pixel[readposition].blue / 65535;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 255);
                cbValue = round(dCbValue * 255);
                crValue = round(dCrValue * 255);

                WritePtr[writeLinearPosition++] = yValue;

                if (col % 2 == 0)  //each y acompnaied with one of the chroma
                {
                    WritePtr[writeLinearPosition++] = cbValue;
                }
                else
                {
                    WritePtr[writeLinearPosition++] = crValue;
                }
                rowByteCount += 2;

            }
            for (; rowByteCount < nTiles * 128;)
            {
                WritePtr[writeLinearPosition++] = 0;
                WritePtr[writeLinearPosition++] = 0;
                rowByteCount += 2;
            }

        }

        for (; row < n64Rows * 64; row++)
        {
            rowByteCount = 0;
            for (; rowByteCount < nTiles * 128;)
            {
                WritePtr[writeLinearPosition++] = 0;
                WritePtr[writeLinearPosition++] = 0;
                rowByteCount += 2;
            }
        }

        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64);  //allocate memory for tilled output
        YtillingBuffer((char*)pImageData, nTiles * 128, n64Rows * 64, 5, (char*)dest_buffer);    //tilling rearragement
        memcpy(pImageData, dest_buffer, nTiles * 128 * n64Rows * 64);                            //replace the memory with tilled output
        free(dest_buffer);

    }
    else if (mImageProperties.pixelFormat == SB_YUV422_16 || mImageProperties.pixelFormat == SB_YUV422_12 || mImageProperties.pixelFormat == SB_YUV422_10)
    {
        UINT16* WritePtr = (UINT16*)pImageData;
        double dYValue, dCbValue, dCrValue;
        UINT16 yValue, cbValue, crValue;
        double rgb2YCbCr[3][3], offset[3];
        IPIXEL* pixel = (IPIXEL*)inImageData;

        ColorUtils::ComputeRgb2YcbcrMatrix(SIXTEEN, LIMITED, SDTV, rgb2YCbCr, offset);

        double r, g, b, a;
        int row, col, writeLinearPosition = 0;
        int readposition = 0;

        int n64Rows = (mImageProperties.height + 63) & 0xFFC0;       //ceil of divided by 64 (multiple of 64 rows)
        int nTiles = (mImageProperties.width * 4 + 127) & 0xFF80;   //ceil of divided by 128 (tile widht in 128 bytes);
        int rowByteCount = 0;

        for (row = 0; row < mImageProperties.height; row++)
        {
            rowByteCount = 0;
            for (col = 0; col < mImageProperties.width; col++)
            {

                r = (double)pixel[readposition].red / 65535;
                g = (double)pixel[readposition].green / 65535;
                b = (double)pixel[readposition].blue / 65535;
                readposition += 1;

                dYValue = r * rgb2YCbCr[0][0] + g * rgb2YCbCr[0][1] + b * rgb2YCbCr[0][2] + offset[0];  //rgb to YCbCr conversion
                dCbValue = r * rgb2YCbCr[1][0] + g * rgb2YCbCr[1][1] + b * rgb2YCbCr[1][2] + offset[1];
                dCrValue = r * rgb2YCbCr[2][0] + g * rgb2YCbCr[2][1] + b * rgb2YCbCr[2][2] + offset[2];

                yValue = round(dYValue * 65535);
                cbValue = round(dCbValue * 65535);
                crValue = round(dCrValue * 65535);

                WritePtr[writeLinearPosition++] = yValue;

                if (col % 2 == 0)  //each y acompnaied with one of the chroma
                {
                    WritePtr[writeLinearPosition++] = cbValue;
                }
                else
                {
                    WritePtr[writeLinearPosition++] = crValue;
                }
                rowByteCount += 4;
            }

            for (; rowByteCount < nTiles * 128;)
            {
                WritePtr[writeLinearPosition++] = 0;
                WritePtr[writeLinearPosition++] = 0;
                rowByteCount += 4;
            }

        }

        for (; row < n64Rows * 64; row++)
        {
            rowByteCount = 0;
            for (; rowByteCount < nTiles * 128;)
            {
                WritePtr[writeLinearPosition++] = 0;
                WritePtr[writeLinearPosition++] = 0;
                rowByteCount += 4;
            }
        }

        unsigned char* dest_buffer = (unsigned char*)malloc(nTiles * 128 * n64Rows * 64);  //allocate memory for tilled output
        YtillingBuffer((char*)pImageData, nTiles * 128, n64Rows * 64, 5, (char*)dest_buffer);    //tilling rearragement
        memcpy(pImageData, dest_buffer, nTiles * 128 * n64Rows * 64);                            //replace the memory with tilled output
        free(dest_buffer);
    }


}


