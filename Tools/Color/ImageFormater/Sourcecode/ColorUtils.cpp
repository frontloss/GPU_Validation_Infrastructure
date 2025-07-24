#include "ColorUtils.h"
#define SIZE_OF_DOUBLE_3X3_MATRIX 72
#define SIZE_OF_DOUBLE_3X1_MATRIX 24

//FULL RANGE MATRICES

double Rgb2YcbcrMatrixBt601[3][3] =
{
    0.29900000000, 0.58700000000, 0.11400000000,
    -0.16873589165, -0.33126410835, 0.50000000000,
    0.50000000000, -0.41868758916, -0.08131241084
};

double Ycbcr2RgbMatrixBt601[3][3] =
{
    1.00000000000, 0.00000000000, 1.40200000000,
    1.00000000000, -0.34413628620, -0.71413628620,
    1.00000000000, 1.77200000000, 0.00000000000
};


double Rgb2YcbcrMatrixBt709[3][3] =
{
    0.21260000000, 0.71520000000, 0.07220000000,
    -0.11457210606, -0.38542789394, 0.50000000000,
    0.50000000000, -0.45415290831, -0.04584709169
};

double Ycbcr2RgbMatrixBt709[3][3] =
{
    1.00000000000, 0.00000000000, 1.57480000000,
    1.00000000000, -0.18732427293, -0.46812427293,
    1.00000000000, 1.85560000000, 0.00000000000
};


double Rgb2YcbcrMatrixBt2020[3][3] =
{
    0.26270000000, 0.67800000000, 0.05930000000,
    -0.13963006272, -0.36036993728, 0.50000000000,
    0.50000000000, -0.45978570460, -0.04021429540
};

double Ycbcr2RgbMatrixBt2020[3][3] =
{
    1.00000000000, 0.00000000000, 1.47460000000,
    1.00000000000, -0.16455312684, -0.57135312684,
    1.00000000000, 1.88140000000, 0.00000000000
};


void ColorUtils::Max(double in1, double* in2)
{
    if (in1 > * in2)
    {
        *in2 = in1;
    }

}

void ColorUtils::CopyMatrix3x3(double sourceMatrix[3][3], double destinationMatrix[3][3])
{
    //memcpy(destinationMatrix, sourceMatrix, sizeof(destinationMatrix));
    memcpy(destinationMatrix, sourceMatrix, SIZE_OF_DOUBLE_3X3_MATRIX);
}

void ColorUtils::CopyVector3x1(double sourceMatrix[3], double destinationMatrix[3])
{
    //memcpy(destinationMatrix, sourceMatrix, sizeof(destinationMatrix));
    memcpy(destinationMatrix, sourceMatrix, SIZE_OF_DOUBLE_3X1_MATRIX);
}


void ColorUtils::MatrixMultiply3X1With3X3(double rgb[3], double mat[3][3])
{
    double ycbcr[3];

    ycbcr[0] = (rgb[0] * (mat[0][0]) + rgb[1] * (mat[0][1]) + rgb[2] * (mat[0][2]));
    ycbcr[1] = (rgb[0] * (mat[1][0]) + rgb[1] * (mat[1][1]) + rgb[2] * (mat[1][2]));
    ycbcr[2] = (rgb[0] * (mat[2][0]) + rgb[1] * (mat[2][1]) + rgb[2] * (mat[2][2]));

    rgb[0] = ycbcr[0];
    rgb[1] = ycbcr[1];
    rgb[2] = ycbcr[2];


}


void ColorUtils::ComputeRgb2YcbcrMatrix(BitsPerPixel bpp, ColourRange Crange, DisplayStandard Dstandard, double convertionMatrix[3][3], double offset[3])   //selects the converstion matrix
{
    double Yfactor, Cfactor;
    int i, j;

    double maxValue = pow(2.0, bpp) - 1.0;

    if (Dstandard == SDTV) CopyMatrix3x3(Rgb2YcbcrMatrixBt601, convertionMatrix);
    else if (Dstandard == HDTV) CopyMatrix3x3(Rgb2YcbcrMatrixBt709, convertionMatrix);
    else CopyMatrix3x3(Rgb2YcbcrMatrixBt2020, convertionMatrix);


    offset[0] = 0.0;
    offset[1] = round(maxValue / 2.0) / (double)maxValue;
    offset[2] = round(maxValue / 2.0) / (double)maxValue;
    if (Crange == 1)
    {

        Yfactor = (219.0 * pow(2, (bpp - 8))) / maxValue;
        Cfactor = (224.0 * pow(2, (bpp - 8))) / maxValue;
        for (i = 0; i < 3; i++)
        {
            convertionMatrix[0][i] = convertionMatrix[0][i] * Yfactor;
        }
        for (i = 1; i < 3; i++)
        {
            for (j = 0; j < 3; j++)
            {
                convertionMatrix[i][j] = convertionMatrix[i][j] * Cfactor;
            }
        }
        offset[0] = (16.0 * pow(2, (bpp - 8))) / (double)maxValue;

    }
}

void ColorUtils::ComputeYcbcr2RgbMatrix(BitsPerPixel bpp, ColourRange Crange, DisplayStandard dStandard, double convertionMatrix[3][3], double offset[3])  //selects the conversion matrix for inverse transform
{
    double Yfactor, Cfactor;
    int i, j;
    double maxValue = pow(2.0, bpp) - 1.0;

    if (dStandard == SDTV) CopyMatrix3x3(Ycbcr2RgbMatrixBt601, convertionMatrix);
    else if (dStandard == HDTV) CopyMatrix3x3(Ycbcr2RgbMatrixBt709, convertionMatrix);
    else CopyMatrix3x3(Ycbcr2RgbMatrixBt2020, convertionMatrix);

    offset[0] = 0.0;
    offset[1] = round(maxValue / 2.0) / (double)maxValue;
    offset[2] = round(maxValue / 2.0) / (double)maxValue;
    if (Crange == 1)
    {

        Yfactor = maxValue / (219.0 * pow(2, (bpp - 8)));
        Cfactor = maxValue / (224.0 * pow(2, (bpp - 8)));
        for (i = 0; i < 3; i++)
        {
            convertionMatrix[i][0] = convertionMatrix[i][0] * Yfactor;
        }
        for (i = 1; i < 3; i++)
        {
            for (j = 0; j < 3; j++)
            {
                convertionMatrix[j][i] = convertionMatrix[j][i] * Cfactor;
            }
        }

        offset[0] = (16.0 * pow(2, (bpp - 8))) / (double)maxValue;

    }

}

void ColorUtils::Rgb2Ycrbcr(BitsPerPixel bpp, ColourRange Crange, DisplayStandard Dformat, RGBPIXEL* rgb, YCBCRPIXEL& ycbcr)
{

    double rgbNumeric[3];
    double convertionmatrix[3][3], offset[3];

    rgbNumeric[0] = rgb->Red;
    rgbNumeric[1] = rgb->Green;
    rgbNumeric[2] = rgb->Blue;

    ComputeRgb2YcbcrMatrix(bpp, Crange, Dformat, convertionmatrix, offset);
    MatrixMultiply3X1With3X3(rgbNumeric, convertionmatrix);
    ycbcr.Y = round(rgbNumeric[0] + offset[0]);
    ycbcr.Cb = round(rgbNumeric[1] + offset[1]);
    ycbcr.Cr = round(rgbNumeric[2] + offset[2]);
}

void ColorUtils::Ycbcr2Rgb(BitsPerPixel bpp, ColourRange Crange, DisplayStandard Dformat, YCBCRPIXEL* ycbcr, RGBPIXEL& rgb)
{

    double ycbcrNumeric[3];
    double InverseMatrix[3][3], offset[3];

    ComputeYcbcr2RgbMatrix(bpp, Crange, Dformat, InverseMatrix, offset);
    ycbcrNumeric[0] = ycbcr->Y - offset[0];
    ycbcrNumeric[1] = ycbcr->Cb - offset[1];
    ycbcrNumeric[2] = ycbcr->Cr - offset[2];


    MatrixMultiply3X1With3X3(ycbcrNumeric, InverseMatrix);
    Max(0, &ycbcrNumeric[0]);
    Max(0, &ycbcrNumeric[1]);
    Max(0, &ycbcrNumeric[2]);

    rgb.Red = ycbcrNumeric[0];
    rgb.Green = ycbcrNumeric[1];
    rgb.Blue = ycbcrNumeric[2];

}

void ColorUtils::RgbLimited2RgbFull(BitsPerPixel bpp, RGBPIXEL* rgb)
{
    double maxValue = pow(2.0, bpp) - 1.0;

    rgb->Red = round(((rgb->Red - 16) * maxValue) / (219.0 * pow(2, (bpp - 8))));
    rgb->Green = round(((rgb->Green - 16) * maxValue) / (224.0 * pow(2, (bpp - 8))));
    rgb->Blue = round(((rgb->Blue - 16) * maxValue) / (224.0 * pow(2, (bpp - 8))));
}

void ColorUtils::RgbFull2RgbLimited(BitsPerPixel bpp, RGBPIXEL* rgb)
{
    double maxValue = pow(2.0, bpp) - 1.0;

    rgb->Red = round(((rgb->Red * (219.0 * pow(2, (bpp - 8)))) / maxValue) + 16 * pow(2, (bpp - 8)));
    rgb->Green = round(((rgb->Green * (224.0 * pow(2, (bpp - 8)))) / maxValue) + 16 * pow(2, (bpp - 8)));
    rgb->Blue = round(((rgb->Blue * (224.0 * pow(2, (bpp - 8)))) / maxValue) + 16 * pow(2, (bpp - 8)));
}

void ColorUtils::GetLutValue(GLUT Lut, NORMALISED_PIXEL inputValue, NORMALISED_PIXEL* outputValue)
{
    double x0, y0, x1, y1, stepSize;
    double inputComponent[3], outputComponent[3];
    stepSize = (double)1.0 / (double)(Lut.numberSamples - 1);

    inputComponent[0] = (double)inputValue.comp1;
    inputComponent[1] = (double)inputValue.comp2;
    inputComponent[2] = (double)inputValue.comp3;

    for (int i = 1; i <= Lut.numberSamples - 1; i++)   //interpolation for first component
    {
        if (inputComponent[0] <= (double)i * stepSize)
        {
            x1 = (double)i * stepSize;
            x0 = x1 - stepSize;
            y1 = Lut.lutComp1[i];
            y0 = Lut.lutComp1[i - 1];
            outputComponent[0] = y0 + (y1 - y0) * (inputComponent[0] - x0) / (x1 - x0);
            outputComponent[0] = outputComponent[0] / (double)Lut.maxSampleValue;
            break;
        }
    }

    for (int i = 1; i <= Lut.numberSamples - 1; i++) //interpolation for second component
    {
        if (inputComponent[1] <= (double)i * stepSize)
        {
            x1 = (double)i * stepSize;
            x0 = x1 - stepSize;
            y1 = Lut.lutComp2[i];
            y0 = Lut.lutComp2[i - 1];
            outputComponent[1] = y0 + (y1 - y0) * (inputComponent[1] - x0) / (x1 - x0);
            outputComponent[1] = outputComponent[1] / (double)Lut.maxSampleValue;
            break;
        }
    }

    for (int i = 1; i <= Lut.numberSamples - 1; i++) //interpolation for third component
    {
        if (inputComponent[2] <= (double)i * stepSize)
        {
            x1 = (double)i * stepSize;
            x0 = x1 - stepSize;
            y1 = Lut.lutComp3[i];
            y0 = Lut.lutComp3[i - 1];
            outputComponent[2] = y0 + (y1 - y0) * (inputComponent[2] - x0) / (x1 - x0);
            outputComponent[2] = outputComponent[2] / (double)Lut.maxSampleValue;
            break;
        }
    }
    outputValue->comp1 = min(outputComponent[0], 1);
    outputValue->comp2 = min(outputComponent[1], 1);
    outputValue->comp3 = min(outputComponent[2], 1);


}

void ColorUtils::linear2srgb(double& ci)
{
    double tempci;
    if (ci > 0.0031308)
    {
        tempci = pow(ci, (1 / 2.4));
        ci = ((1 + ALPHA) * tempci - ALPHA);
    }
    else
    {
        ci = 12.92 * ci;
    }
}

void ColorUtils::srgb2linear(double& ci)
{
    double tempci;
    if (ci > 0.04045)
    {
        tempci = (ci + ALPHA) / (1 + ALPHA);
        tempci = pow(tempci, 2.4);
        ci = tempci;

    }
    else
    {
        ci = (ci / 12.92);
    }
}


void ColorUtils::fixedpoint2Float(INT32 inputInt, double& outputValue, int IntBits, int fractionalBits)
{
    int factor = pow(2, fractionalBits);
    outputValue = (double)inputInt / factor;
}

void ColorUtils::float2Fixedpoint(double inputValue, INT32& outputValue, int IntBits, int fractionalBits)
{
    int factor = pow(2, fractionalBits);
    outputValue = round(inputValue * factor);
}