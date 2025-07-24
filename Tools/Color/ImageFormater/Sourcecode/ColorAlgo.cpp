
#include<cmath>
#include<cstdlib>
#include "ColorAlgo.h"

double m1 = 0.1593017578125;
double m2 = 78.84375;
double c1 = 0.8359375;
double c2 = 18.8515625;
double c3 = 18.6875;


static double XYZ2LMS[3][3] =
{
    { 0.8951, 0.2664, -0.1614 },
    { -0.7502, 1.7135, 0.0367 },
    { 0.0389, -0.0685, 1.0296 }
};

double RGB2CBCR_2020_FullRange[3][3] =
{
    { 0.26270000000, 0.67800000000, 0.05930000000 },
    { -0.13963006272, -0.36036993728, 0.50000000000 },
    { 0.50000000000, -0.45978570460, -0.04021429540 }
};

double RGB2CBCR_709_FullRange[3][3] =
{
    { 0.21260000000, 0.71520000000, 0.07220000000 },
    { -0.11457210606, -0.38542789394, 0.50000000000 },
    { 0.50000000000, -0.45415290831, -0.04584709169 }
};

double RGB2CBCR_601_FullRange[3][3] =
{
    { 0.29900000000, 0.58700000000, 0.11400000000 },
    { -0.16873589165, -0.33126410835, 0.50000000000 },
    { 0.50000000000, -0.41868758916, -0.08131241084 }
};

ColorAlgo::ColorAlgo()
{

}

ColorAlgo::~ColorAlgo()
{

}

COLOR_ALGO_ERR ColorAlgo::GenerateDeGammaLUT(OneDLUT& lut)
{
    for (DWORD i = 0; i < lut.nSamples; i++)
    {
        double normalized_input = (double)i / (double)(lut.nSamples - 1);
        lut.pLutData[i].r = (double)lut.maxVal * GetSRGBDecodingValue(normalized_input) + 0.5;

        if (lut.pLutData[i].r > lut.maxVal)
        {
            lut.pLutData[i].r = lut.maxVal;
        }

        lut.pLutData[i].g = lut.pLutData[i].b = lut.pLutData[i].r;
    }

    return COLOR_ALGO_ERR_NONE;
}

COLOR_ALGO_ERR ColorAlgo::GenerateEOTF2084LUT(OneDLUT& lut)
{
    for (DWORD i = 0; i < lut.nSamples; i++)
    {
        double normalized_input = (double)i / (double)(lut.nSamples - 1);
        lut.pLutData[i].r = (double)lut.maxVal * EOTF_2084(normalized_input) + 0.5;

        if (lut.pLutData[i].r > lut.maxVal)
        {
            lut.pLutData[i].r = lut.maxVal;
        }

        lut.pLutData[i].g = lut.pLutData[i].b = lut.pLutData[i].r;
    }

    return COLOR_ALGO_ERR_NONE;
}

COLOR_ALGO_ERR ColorAlgo::GenerateGammaLUT(OneDLUT& lut)
{
    for (DWORD i = 0; i < lut.nSamples; i++)
    {
        double normalized_input = (double)i / (double)(lut.nSamples - 1);
        lut.pLutData[i].r = (double)lut.maxVal * ColorAlgo::GetSRGBEncodingValue(normalized_input) + 0.5;

        if (lut.pLutData[i].r > lut.maxVal)
        {
            lut.pLutData[i].r = lut.maxVal;
        }

        lut.pLutData[i].g = lut.pLutData[i].b = lut.pLutData[i].r;
    }

    return COLOR_ALGO_ERR_NONE;
}

COLOR_ALGO_ERR ColorAlgo::GenerateOETF2084LUT(OneDLUT& lut, double toneMappingFactor)
{
    for (DWORD i = 0; i < lut.nSamples; i++)
    {
        double normalized_input = toneMappingFactor * (double)i / (double)(lut.nSamples - 1);
        lut.pLutData[i].r = (double)lut.maxVal * OETF_2084(normalized_input) + 0.5;

        if (lut.pLutData[i].r > lut.maxVal)
        {
            lut.pLutData[i].r = lut.maxVal;
        }

        lut.pLutData[i].g = lut.pLutData[i].b = lut.pLutData[i].r;
    }

    return COLOR_ALGO_ERR_NONE;
}

COLOR_ALGO_ERR ColorAlgo::GenerateSDR2HDRLUT(OneDLUT& lut)
{
    for (DWORD i = 0; i < lut.nSamples; i++)
    {
        double normalized_input = (double)i / (double)(lut.nSamples - 1);
        double degamma_output = GetSRGBDecodingValue(normalized_input);

        degamma_output *= 80.0 / 10000.0;

        lut.pLutData[i].r = (double)lut.maxVal * OETF_2084(degamma_output) + 0.5;

        if (lut.pLutData[i].r > lut.maxVal)
        {
            lut.pLutData[i].r = lut.maxVal;
        }

        lut.pLutData[i].g = lut.pLutData[i].b = lut.pLutData[i].r;
    }

    return COLOR_ALGO_ERR_NONE;
}


COLOR_ALGO_ERR ColorAlgo::ResizeLUT(OneDLUT* pSrcLUT, OneDLUT* pDstLUT)
{
    DWORD i;
    double input, maxOutIndex = pDstLUT->nSamples - 1;

    for (i = 0; i < pDstLUT->nSamples; i++)
    {
        input = (double)i / maxOutIndex;

        pDstLUT->pLutData[i].r = pDstLUT->maxVal * ApplyLUT(pSrcLUT, input, COLOR_CHANNEL_RED);
        pDstLUT->pLutData[i].g = pDstLUT->maxVal * ApplyLUT(pSrcLUT, input, COLOR_CHANNEL_GREEN);
        pDstLUT->pLutData[i].b = pDstLUT->maxVal * ApplyLUT(pSrcLUT, input, COLOR_CHANNEL_BLUE);
    }

    return COLOR_ALGO_ERR_NONE;
}

double ColorAlgo::ApplyLUT(OneDLUT* pLUT, double input, COLOR_CHANNEL channel)
{
    double dIndex = (double)input * (double)(pLUT->nSamples - 1);
    DWORD iIndex = dIndex;

    double outVal;
    double correction = 0;

    switch (channel)
    {
    case COLOR_CHANNEL_RED:
        outVal = pLUT->pLutData[iIndex].r;
        break;

    case COLOR_CHANNEL_GREEN:
        outVal = pLUT->pLutData[iIndex].g;
        break;

    case COLOR_CHANNEL_BLUE:
        outVal = pLUT->pLutData[iIndex].b;
        break;
    }

    if (iIndex < (pLUT->nSamples - 1))
    {
        switch (channel)
        {
        case COLOR_CHANNEL_RED:
            correction = (double)pLUT->pLutData[iIndex + 1].r - (double)pLUT->pLutData[iIndex].r;
            break;

        case COLOR_CHANNEL_GREEN:
            correction = (double)pLUT->pLutData[iIndex + 1].g - (double)pLUT->pLutData[iIndex].g;
            break;

        case COLOR_CHANNEL_BLUE:
            correction = (double)pLUT->pLutData[iIndex + 1].b - (double)pLUT->pLutData[iIndex].b;
            break;
        }

        correction *= (dIndex - iIndex);
    }

    outVal += correction + 0.5;

    if (outVal > pLUT->maxVal) outVal = pLUT->maxVal;

    outVal /= (double)pLUT->maxVal;

    return outVal;
}


double ColorAlgo::CIELabTxFn(double inp)
{
    double retVal = 0;

    /*
    https://en.wikipedia.org/wiki/Lab_color_space#Forward_transformation
    */

    if (inp > pow(6.0 / 29.0, 3.0))
    {
        retVal = pow(inp, (1.0 / 3.0));
    }
    else
    {
        retVal = inp * (pow(29.0 / 6.0, 2.0) / 3.0) + (4.0 / 29.0);
    }

    return retVal;
}

void ColorAlgo::GetCIELab(ChromaticityXYZ color, ChromaticityXYZ whitePoint, ChromaticityLab& colorLab)
{
    /*
    https://en.wikipedia.org/wiki/Lab_color_space#Forward_transformation
    */

    color.X /= whitePoint.X;
    color.Y /= whitePoint.Y;
    color.Z /= whitePoint.Z;

    colorLab.L = 116.0 * (CIELabTxFn(color.Y)) - 16;
    colorLab.a = 500.0 * (CIELabTxFn(color.X) - CIELabTxFn(color.Y));
    colorLab.b = 200.0 * (CIELabTxFn(color.Y) - CIELabTxFn(color.Z));
}

double ColorAlgo::CalculateDeltaECIE94(ChromaticityLab refColor, ChromaticityLab color)
{
    /*
    https://en.wikipedia.org/wiki/Color_difference#CIE94
    */

    double err = 0;
    double deltaL = refColor.L - color.L;
    double Lcomponent = pow(deltaL, 2.0);

    double C1 = sqrt(pow(refColor.a, 2.0) + pow(refColor.b, 2.0));
    double C2 = sqrt(pow(color.a, 2.0) + pow(color.b, 2.0));
    double deltaC = C1 - C2;
    double deltaA = refColor.a - color.a;
    double deltaB = refColor.b - color.b;
    double deltaH = 0;

    double tmp = pow(deltaA, 2.0) + pow(deltaB, 2.0) - pow(deltaC, 2.0);

    if (tmp > 0)
    {
        deltaH = sqrt(pow(deltaA, 2.0) + pow(deltaB, 2.0) - pow(deltaC, 2.0));
    }

    double Sc = 1.0 + 0.045 * C1;
    double Ccomponent = pow(deltaC / Sc, 2.0);

    double Sh = 1.0 + 0.015 * C1;
    double Hcomponent = pow(deltaH / Sh, 2.0);

    err = sqrt(Lcomponent + Ccomponent + Hcomponent);

    return err;
}

double ColorAlgo::CalculateDeltaE(ChromaticityXYZ refColor, ChromaticityXYZ color)
{
    ChromaticityLab colorLab = { 0 };
    ChromaticityLab refLab = { 0 };
    ChromaticityXYZ RefWhitePointXYZ = { 95.045593, 100.0, 108.905775 };

    // WA. Zero values can't be handled
    if (color.X == 0) color.X = refColor.X;
    if (color.Z == 0) color.Z = refColor.Z;

    GetCIELab(refColor, RefWhitePointXYZ, refLab);
    GetCIELab(color, RefWhitePointXYZ, colorLab);

#ifdef USE_DELTAE_2000
    return CalculateDeltaECIEDE2000(refLab, colorLab);
#else
    return CalculateDeltaECIE94(refLab, colorLab);
#endif
}

void ColorAlgo::CreateRGB2XYZMatrix(ColorSpace* pCspace, double rgb2xyz[3][3])
{
    /*
    http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
    */

    double XYZsum[3];
    double z[4];
    double XYZw[3];
    Chromaticity* pChroma = &pCspace->white;

    for (int i = 0; i < 4; i++)
    {
        z[i] = 1 - pChroma[i].x - pChroma[i].y;
    }

    XYZw[0] = pCspace->white.x / pCspace->white.y;
    XYZw[1] = 1;
    XYZw[2] = z[0] / pCspace->white.y;

    double xyzrgb[3][3] =
    {
        { pCspace->red.x, pCspace->green.x, pCspace->blue.x },
        { pCspace->red.y, pCspace->green.y, pCspace->blue.y },
        { z[1], z[2], z[3] }
    };

    double mat1[3][3];

    MatrixInverse3x3(xyzrgb, mat1);
    MatrixMult3x3With3x1(mat1, XYZw, XYZsum);

    double mat2[3][3] = { { XYZsum[0], 0, 0 }, { 0, XYZsum[1], 0 }, { 0, 0, XYZsum[2] } };

    MatrixMult3x3(xyzrgb, mat2, rgb2xyz);
}

void ColorAlgo::CreateGamutScalingMatrix(ColorSpace* pSrc, ColorSpace* pDst, double result[3][3])
{
    double mat1[3][3], mat2[3][3], tmp[3][3];

    CreateRGB2XYZMatrix(pSrc, mat1);
    CreateRGB2XYZMatrix(pDst, mat2);

    MatrixInverse3x3(mat2, tmp);
    MatrixMult3x3(tmp, mat1, result);
}

void ColorAlgo::Create2020To709Matrix(double result[3][3])
{
    /*
    https://en.wikipedia.org/wiki/Rec._2020#System_colorimetry
    https://en.wikipedia.org/wiki/Rec._709#Primary_chromaticities
    */

    ColorSpace bt2020, bt709;

    bt2020.white.x = 0.3127; bt2020.white.y = 0.3290; bt2020.white.luminance = 100.0;
    bt2020.red.x = 0.708; bt2020.red.y = 0.292;
    bt2020.green.x = 0.170; bt2020.green.y = 0.797;
    bt2020.blue.x = 0.131; bt2020.blue.y = 0.046;

    bt709.white.x = 0.3127; bt709.white.y = 0.3290; bt709.white.luminance = 100.0;
    bt709.red.x = 0.64; bt709.red.y = 0.33;
    bt709.green.x = 0.30; bt709.green.y = 0.60;
    bt709.blue.x = 0.15; bt709.blue.y = 0.06;

    CreateGamutScalingMatrix(&bt2020, &bt709, result);
}

void ColorAlgo::Create709To2020Matrix(double result[3][3])
{
    /*
    https://en.wikipedia.org/wiki/Rec._2020#System_colorimetry
    https://en.wikipedia.org/wiki/Rec._709#Primary_chromaticities
    */

    ColorSpace bt2020, bt709;

    bt2020.white.x = 0.3127; bt2020.white.y = 0.3290; bt2020.white.luminance = 100.0;
    bt2020.red.x = 0.708; bt2020.red.y = 0.292;
    bt2020.green.x = 0.170; bt2020.green.y = 0.797;
    bt2020.blue.x = 0.131; bt2020.blue.y = 0.046;

    bt709.white.x = 0.3127; bt709.white.y = 0.3290; bt709.white.luminance = 100.0;
    bt709.red.x = 0.64; bt709.red.y = 0.33;
    bt709.green.x = 0.30; bt709.green.y = 0.60;
    bt709.blue.x = 0.15; bt709.blue.y = 0.06;

    CreateGamutScalingMatrix(&bt709, &bt2020, result);
}

void ColorAlgo::Create2020ToDCIP3Matrix(double result[3][3])
{
    /*
    https://en.wikipedia.org/wiki/Rec._2020#System_colorimetry
    https://en.wikipedia.org/wiki/DCI-P3#System_colorimetry
    */

    ColorSpace bt2020, dcip3;
    double mat1[3][3], mat2[3][3], tmp[3][3];

    bt2020.white.x = 0.3127; bt2020.white.y = 0.3290; bt2020.white.luminance = 100.0;
    bt2020.red.x = 0.708; bt2020.red.y = 0.292;
    bt2020.green.x = 0.170; bt2020.green.y = 0.797;
    bt2020.blue.x = 0.131; bt2020.blue.y = 0.046;

    dcip3.white.x = 0.314; dcip3.white.y = 0.351; dcip3.white.luminance = 100.0;
    dcip3.red.x = 0.680; dcip3.red.y = 0.320;
    dcip3.green.x = 0.265; dcip3.green.y = 0.690;
    dcip3.blue.x = 0.150; dcip3.blue.y = 0.060;

    CreateGamutScalingMatrix(&bt2020, &dcip3, result);
}

void ColorAlgo::Create709ToDCIP3Matrix(double result[3][3])
{
    /*
    https://en.wikipedia.org/wiki/DCI-P3#System_colorimetry
    https://en.wikipedia.org/wiki/Rec._709#Primary_chromaticities
    */

    ColorSpace bt709, dcip3;
    double mat1[3][3], mat2[3][3], tmp[3][3];

    bt709.white.x = 0.3127; bt709.white.y = 0.3290; bt709.white.luminance = 100.0;
    bt709.red.x = 0.64; bt709.red.y = 0.33;
    bt709.green.x = 0.30; bt709.green.y = 0.60;
    bt709.blue.x = 0.15; bt709.blue.y = 0.06;

    dcip3.white.x = 0.314; dcip3.white.y = 0.351; dcip3.white.luminance = 100.0;
    dcip3.red.x = 0.680; dcip3.red.y = 0.320;
    dcip3.green.x = 0.265; dcip3.green.y = 0.690;
    dcip3.blue.x = 0.150; dcip3.blue.y = 0.060;

    CreateGamutScalingMatrix(&bt709, &dcip3, result);
}

void ColorAlgo::CreateRGB2YCbCrMatrix(COLOR_MODEL eModel, double rgb2ycbcr[3][3])
{
    if (eModel == COLOR_MODEL_YCBCR_601)
    {
        memcpy(rgb2ycbcr, RGB2CBCR_601_FullRange, sizeof(RGB2CBCR_601_FullRange));
    }
    else if (eModel == COLOR_MODEL_YCBCR_709)
    {
        memcpy(rgb2ycbcr, RGB2CBCR_709_FullRange, sizeof(RGB2CBCR_709_FullRange));
    }
    else if (eModel == COLOR_MODEL_YCBCR_2020)
    {
        memcpy(rgb2ycbcr, RGB2CBCR_2020_FullRange, sizeof(RGB2CBCR_2020_FullRange));
    }
}

void ColorAlgo::GetxyYFromCCT(double T, double& x, double& y)
{
    /*
    https://en.wikipedia.org/wiki/Standard_illuminant#Illuminant_series_D
    */

    if (T >= 4000 && T <= 7000)
    {
        x = 0.244063 + 0.09911e+3 / (double)T + 2.9678e+6 * pow((double)T, -2) - 4.6070e+9 * pow((double)T, -3);
    }
    else
    {
        x = 0.237040 + 0.24748e+3 / (double)T + 1.9018e+6 * pow((double)T, -2) - 2.0064e+9 * pow((double)T, -3);
    }

    y = -3.0 * pow(x, 2) + 2.870 * x - 0.275;
}

void ColorAlgo::GeWhitePointAdaptationMatrixXYZ(Chromaticity* pSrcWhitePoint, Chromaticity* pTrgetWhitePoint, double result[3][3])
{
    double xTgt = pTrgetWhitePoint->x, yTgt = pTrgetWhitePoint->y;
    double xSrc = pSrcWhitePoint->x, ySrc = pSrcWhitePoint->y;

    double XYZSrc[3] = { xSrc / ySrc, 1, (1 - xSrc - ySrc) / ySrc };
    double XYZTgt[3] = { xTgt / yTgt, 1, (1 - xTgt - yTgt) / yTgt };
    double LMSSrc[3];
    double LMSTgt[3];
    double LMS2XYZ[3][3];

    MatrixMult3x3With3x1(XYZ2LMS, XYZSrc, LMSSrc);
    MatrixMult3x3With3x1(XYZ2LMS, XYZTgt, LMSTgt);
    MatrixInverse3x3(XYZ2LMS, LMS2XYZ);

    result[0][0] = LMSTgt[0] / LMSSrc[0];
    result[1][1] = LMSTgt[1] / LMSSrc[1];
    result[2][2] = LMSTgt[2] / LMSSrc[2];

    result[0][1] = result[0][2] = result[1][0] = result[1][2] = result[2][0] = result[2][1] = 0;

    MatrixMult3x3(LMS2XYZ, result, result);
    MatrixMult3x3(result, XYZ2LMS, result);
}

void ColorAlgo::GeWhitePointAdaptationMatrixRGB(ColorSpace* pSrcColorSpace, ColorSpace* pPanelColorSpace, Chromaticity* pTargetWhitePoint, double result[3][3])
{
    double XYZ2RGB_PANEL[3][3] = { 0 };
    double RGB2XYZ_SOURCE[3][3] = { 0 };
    double RGB2XYZ_PANEL[3][3] = { 0 };
    double mat[3][3];

    CreateRGB2XYZMatrix(pSrcColorSpace, RGB2XYZ_SOURCE);
    CreateRGB2XYZMatrix(pPanelColorSpace, RGB2XYZ_PANEL);
    MatrixInverse3x3(RGB2XYZ_PANEL, XYZ2RGB_PANEL);

    GeWhitePointAdaptationMatrixXYZ(&pSrcColorSpace->white, pTargetWhitePoint, mat);

    MatrixMult3x3(XYZ2RGB_PANEL, mat, mat);
    MatrixMult3x3(mat, RGB2XYZ_SOURCE, result);
}


double ColorAlgo::GetSRGBDecodingValue(double input)
{
    /*
    https://en.wikipedia.org/wiki/SRGB#The_forward_transformation_.28CIE_xyY_or_CIE_XYZ_to_sRGB.29
    */

    double output;

    if (input <= 0.04045)
    {
        output = input / 12.92;
    }
    else
    {
        output = pow(((input + 0.055) / 1.055), 2.4);
    }

    return output;
}

double ColorAlgo::GetSRGBEncodingValue(double input)
{
    /*
    https://en.wikipedia.org/wiki/SRGB#The_forward_transformation_.28CIE_xyY_or_CIE_XYZ_to_sRGB.29
    */

    double output;

    if (input <= 0.0031308)
    {
        output = input * 12.92;
    }
    else
    {
        output = (1.055 * pow(input, 1.0 / 2.4)) - 0.055;
    }

    return output;
}

double ColorAlgo::EOTF_2084(double input)
{
    double output = 0.0f;

    if (input != 0.0f)
    {
        output = pow(((max((pow(input, (1.0 / m2)) - c1), 0)) / (c2 - (c3 * pow(input, (1.0 / m2))))), (1.0 / m1));
    }

    return output;
}

double ColorAlgo::OETF_2084(double input, double srcMaxLuminance)
{
    double cf = 1.0;
    double output = 0.0f;

    if (input != 0.0f)
    {
        cf = srcMaxLuminance / 10000.0;

        input *= cf;
        output = pow(((c1 + (c2 * pow(input, m1))) / (1 + (c3 * pow(input, m1)))), m2);
    }

    return output;
}

USHORT ColorAlgo::DoubleToHalf(double inp)
{
    /*
    https://en.wikipedia.org/wiki/Half-precision_floating-point_format#IEEE_754_half-precision_binary_floating-point_format:_binary16
    */

    USHORT signBit = 0;
    USHORT exponent = 0;
    USHORT mantissa = 0;
    USHORT retVal = 0;

    if (inp < 0) signBit = 1;

    inp = abs(inp);

    if (inp > 65504) inp = INFINITY;

    if (inp == INFINITY)
    {
        exponent = 0x1F;
        mantissa = 0;
    }
    else if (inp == 0)
    {
        exponent = 0;
        mantissa = 0;
    }
    else if (inp == NAN)
    {
        exponent = 0x1F;
        mantissa = 1;
    }
    else if (inp > 0 && inp < pow(2.0, -14.0))
    {
        inp = inp * 1024.0 + 0.5;
        if (inp > 1023) inp = 1023;
        mantissa = inp;
        exponent = 0;
    }
    else if (inp >= 1.0)
    {
        DWORD i = 0;

        for (i = 0; i <= 16; i++)
        {
            double val = inp / (double)(1 << i);

            if (val >= 1.0 && val < 2.0)
            {
                mantissa = (val - 1.0) * 1024.0 + 0.5;
                if (mantissa > 1023) mantissa = 1023;
                break;
            }
        }

        exponent = i + 15;
    }
    else
    {
        DWORD i = 0;

        for (i = 0; i <= 16; i++)
        {
            double val = inp * (double)(1 << i);

            if (val >= 1.0 && val < 2.0)
            {
                mantissa = (val - 1.0) * 1024.0 + 0.5;
                if (mantissa > 1023) mantissa = 1023;
                break;
            }
        }

        exponent = 15 - i;
    }

    retVal = signBit << 15;
    retVal |= exponent << 10;
    retVal |= mantissa;

    return retVal;
}

double ColorAlgo::HalfToDouble(USHORT inp)
{
    /*
    https://en.wikipedia.org/wiki/Half-precision_floating-point_format#IEEE_754_half-precision_binary_floating-point_format:_binary16
    */

    USHORT signBit = inp & 0x8000;
    USHORT exponent = (inp & 0x7C00) >> 10;
    USHORT mantissa = inp & 0x03FF;
    double scaleFactor = 1.0;
    double retVal = NAN;

    if (exponent == 31)
    {
        if (mantissa == 0)
        {
            retVal = INFINITY;

            if (signBit) retVal = -retVal;
        }

        return retVal;
    }

    if (exponent == 0)
    {
        scaleFactor = 1.0 / (double)(1 << 14);
    }
    else
    {
        mantissa |= 0x0400;
        scaleFactor = pow(2.0, (double)(exponent - 15));
    }

    retVal = (double)mantissa * scaleFactor / 1024.0;

    if (signBit) retVal = -retVal;

    return retVal;
}

void ColorAlgo::GetSrgbColorSpace(ColorSpace& srgbColorSpace)
{
    srgbColorSpace.white.x = 0.3127; srgbColorSpace.white.y = 0.3290; srgbColorSpace.white.luminance = 1.0;
    srgbColorSpace.red.x = 0.64; srgbColorSpace.red.y = 0.33; srgbColorSpace.red.luminance = 0.2126;
    srgbColorSpace.green.x = 0.30; srgbColorSpace.green.y = 0.60; srgbColorSpace.green.luminance = 0.7152;
    srgbColorSpace.blue.x = 0.15; srgbColorSpace.blue.y = 0.06; srgbColorSpace.blue.luminance = 0.0722;
}

COLOR_ALGO_ERR ColorAlgo::GetEDIDChromaticity(UINT8* edidV1Chromaticity, ColorSpace& colorSpace)
{
    COLOR_ALGO_ERR err = COLOR_ALGO_ERR_NONE;

    if (NULL != edidV1Chromaticity)
    {
        INT32 val = (edidV1Chromaticity[0] >> 6) & 0x3;
        val |= edidV1Chromaticity[2] << 2;

        colorSpace.white.x = (double)val / 1024.0;

        val = (edidV1Chromaticity[0] >> 4) & 0x3;
        val |= edidV1Chromaticity[3] << 2;

        colorSpace.white.y = (double)val / 1024.0;

        val = (edidV1Chromaticity[0] >> 2) & 0x3;
        val |= edidV1Chromaticity[4] << 2;

        colorSpace.red.x = (double)val / 1024.0;

        val = edidV1Chromaticity[0] & 0x3;
        val |= edidV1Chromaticity[5] << 2;

        colorSpace.red.y = (double)val / 1024.0;

        val = (edidV1Chromaticity[1] >> 6) & 0x3;
        val |= edidV1Chromaticity[6] << 2;

        colorSpace.green.x = (double)val / 1024.0;

        val = (edidV1Chromaticity[1] >> 4) & 0x3;
        val |= edidV1Chromaticity[7] << 2;

        colorSpace.green.y = (double)val / 1024.0;

        val = (edidV1Chromaticity[1] >> 2) & 0x3;
        val |= edidV1Chromaticity[8] << 2;

        colorSpace.blue.x = (double)val / 1024.0;

        val = edidV1Chromaticity[1] & 0x3;
        val |= edidV1Chromaticity[9] << 2;

        colorSpace.blue.y = (double)val / 1024.0;
    }
    else
    {
        err = COLOR_ALGO_ERR_INVALID_ARGS;
    }

    return err;
}

COLOR_ALGO_ERR ColorAlgo::CreateGamutMappingMatrix(ColorSpace* pSrcColorSpace, ColorSpace* pPanelColorSpace, double result[3][3])
{
    result[0][0] = result[1][1] = result[2][2] = 1;
    result[0][1] = result[0][2] = result[1][0] = 0;
    result[1][2] = result[2][0] = result[2][1] = 0;

    COLOR_ALGO_ERR err = COLOR_ALGO_ERR_INVALID_DATA;

    ColorSpace srgbColorSpace = { 0 };
    GetSrgbColorSpace(srgbColorSpace);

    if (NULL == pSrcColorSpace)
    {
        pSrcColorSpace = &srgbColorSpace;
    }

    if (NULL == pPanelColorSpace)
    {
        pPanelColorSpace = &srgbColorSpace;
    }

    if (IsColorSpaceValid(pPanelColorSpace) && IsColorSpaceValid(pPanelColorSpace))
    {
        CreateGamutScalingMatrix(pSrcColorSpace, pPanelColorSpace, result);
        MatrixNormalize3x3(result);
        err = COLOR_ALGO_ERR_NONE;
    }

    return err;
}

COLOR_ALGO_ERR ColorAlgo::CreateWhitePointAdaptationMatrix(ColorSpace* pSrcColorSpace, ColorSpace* pPanelColorSpace, Chromaticity* pTargetWhitePoint, double result[3][3])
{
    result[0][0] = result[1][1] = result[2][2] = 1;
    result[0][1] = result[0][2] = result[1][0] = 0;
    result[1][2] = result[2][0] = result[2][1] = 0;

    COLOR_ALGO_ERR err = COLOR_ALGO_ERR_INVALID_DATA;

    ColorSpace srgbColorSpace = { 0 };
    GetSrgbColorSpace(srgbColorSpace);

    if (NULL == pSrcColorSpace)
    {
        pSrcColorSpace = &srgbColorSpace;
    }

    if (NULL == pPanelColorSpace)
    {
        pPanelColorSpace = &srgbColorSpace;
    }

    if (IsColorSpaceValid(pPanelColorSpace) && IsColorSpaceValid(pPanelColorSpace) && IsChromaticityValid(pTargetWhitePoint))
    {
        GeWhitePointAdaptationMatrixRGB(pSrcColorSpace, pPanelColorSpace, pTargetWhitePoint, result);
        MatrixNormalize3x3(result);
        err = COLOR_ALGO_ERR_NONE;
    }

    return err;
}

COLOR_ALGO_ERR ColorAlgo::CreateWhitePointAdaptationMatrix(ColorSpace* pSrcSpace, ColorSpace* pPanelSpace, double T, double mat[3][3])
{
    COLOR_ALGO_ERR retVal = COLOR_ALGO_ERR_NONE;
    double xTarget, yTarget;
    Chromaticity targetWhitePoint = { 0 };

    if (T != 6504)
    {
        GetxyYFromCCT(T, xTarget, yTarget);

        targetWhitePoint.x = xTarget;
        targetWhitePoint.y = yTarget;
        targetWhitePoint.luminance = 100;

        retVal = CreateWhitePointAdaptationMatrix(pSrcSpace, pPanelSpace, &targetWhitePoint, mat);
    }
    else
    {
        mat[0][1] = mat[0][2] = mat[1][0] = mat[1][2] = mat[2][0] = mat[2][1] = 0.0;
        mat[0][0] = mat[1][1] = mat[2][2] = 1.0;
    }

    return retVal;
}

COLOR_ALGO_ERR ColorAlgo::CreateWhitePointAdaptationLUT(ColorSpace* pSrcSpace, ColorSpace* pPanelSpace, double T, OneDLUT* pLUT)
{
    DWORD nSamples = pLUT->nSamples;
    double maxInputVal = nSamples - 1;
    double maxOutVal = pLUT->maxVal;
    double wbMat[3][3] = { 0 };

    COLOR_ALGO_ERR retVal = CreateWhitePointAdaptationMatrix(pSrcSpace, pPanelSpace, T, wbMat);

    if (retVal == COLOR_ALGO_ERR_NONE)
    {
        // Scale Factor is mat[] multiplied with column vector [1.0, 1.0, 1.0] i.e. normalized white pixel.
        double rScaleFactor = wbMat[0][0] + wbMat[0][1] + wbMat[0][2];
        double gScaleFactor = wbMat[1][0] + wbMat[1][1] + wbMat[1][2];
        double bScaleFactor = wbMat[2][0] + wbMat[2][1] + wbMat[2][2];

        for (DWORD i = 0; i < nSamples; i++)
        {
            double normalizedInput = (double)i / maxInputVal;

            // Scale pixel
            double r = rScaleFactor * normalizedInput;
            double g = gScaleFactor * normalizedInput;
            double b = bScaleFactor * normalizedInput;

            // Convert to integer format
            pLUT->pLutData[i].r = min(round(maxOutVal * r), maxOutVal);
            pLUT->pLutData[i].g = min(round(maxOutVal * g), maxOutVal);
            pLUT->pLutData[i].b = min(round(maxOutVal * b), maxOutVal);
        }
    }

    return retVal;
}

bool ColorAlgo::IsChromaticityValid(Chromaticity* pChroma)
{
    bool bChromaValid = false;

    if (NULL == pChroma)
    {
        return bChromaValid;
    }

    if (pChroma->x > 0 && pChroma->x < 1 && pChroma->y > 0 && pChroma->y < 1 && pChroma->luminance >= MIN_Y && pChroma->luminance <= MAX_Y)
    {
        bChromaValid = true;
    }

    return bChromaValid;
}

bool ColorAlgo::IsColorSpaceValid(ColorSpace* pSpace)
{
    bool bColorSapceValid = true;
    ColorSpace srgbColorSpace = { 0 };

    if (NULL == pSpace)
    {
        return false;
    }

    srgbColorSpace.white.x = 0.3127; srgbColorSpace.white.y = 0.3290; srgbColorSpace.white.luminance = 1.0;
    srgbColorSpace.red.x = 0.64; srgbColorSpace.red.y = 0.33; srgbColorSpace.red.luminance = 0.2126;
    srgbColorSpace.green.x = 0.30; srgbColorSpace.green.y = 0.60; srgbColorSpace.green.luminance = 0.7152;
    srgbColorSpace.blue.x = 0.15; srgbColorSpace.blue.y = 0.06; srgbColorSpace.blue.luminance = 0.0722;

    Chromaticity* pChromaticty = &pSpace->white;

    for (int i = 0; i < 4; i++)
    {
        if (!IsChromaticityValid(pChromaticty))
        {
            bColorSapceValid = false;
            break;
        }

        pChromaticty++;
    }

    if (bColorSapceValid)
    {
        double targetArea = CalculateTriangleArea(pSpace);
        double sRGBArea = CalculateTriangleArea(&srgbColorSpace);

        if ((targetArea / sRGBArea) < 0.33)
        {
            bColorSapceValid = false;
        }

        if (bColorSapceValid)
        {
            bColorSapceValid = IsWhitePointWithinTriangle(pSpace);
        }
    }

    return bColorSapceValid;
}

bool ColorAlgo::IsNarrowGamut(ColorSpace* pPanelColorSpace)
{
    bool retVal = false;
    ColorSpace srgbColorSpace = { 0 };

    GetSrgbColorSpace(srgbColorSpace);

    double targetArea = CalculateTriangleArea(pPanelColorSpace);
    double sourceArea = CalculateTriangleArea(&srgbColorSpace);

    if ((targetArea / sourceArea) < 0.8)
    {
        retVal = true;
    }

    return retVal;
}

double ColorAlgo::DegreeToRadian(double degrees)
{
    return degrees * PI / 180.0;
}

double ColorAlgo::CalculateTriangleArea(ColorSpace* cspace)
{
    double theta = atan2((cspace->green.y - cspace->blue.y), (cspace->green.x - cspace->blue.x));
    theta -= atan2((cspace->red.y - cspace->blue.y), (cspace->red.x - cspace->blue.x));

    double h = sqrt(pow((cspace->green.x - cspace->blue.x), 2) + pow((cspace->green.y - cspace->blue.y), 2)) * sin(theta);
    double b = sqrt(pow((cspace->red.x - cspace->blue.x), 2) + pow((cspace->red.y - cspace->blue.y), 2));

    double area = 0.5 * b * h;

    return area;
}

bool ColorAlgo::IsWhitePointWithinTriangle(ColorSpace* cspace)
{
    bool retVal = false;

    if (cspace->white.x < 0.4 && cspace->white.x > 0.2 &&
        cspace->white.y < 0.4 && cspace->white.y > 0.2)
    {
        retVal = true;
    }

    return retVal;
}

double ColorAlgo::CalculateDeltaECIEDE2000(ChromaticityLab refColor, ChromaticityLab color)
{
    double err = 0;

    double C1ab = sqrt((pow(refColor.a, 2) + pow(refColor.b, 2)));
    double C2ab = sqrt((pow(color.a, 2) + pow(color.b, 2)));

    double Cab = (C1ab + C2ab) / 2;

    double G = 0.5 * (1 - sqrt(pow(Cab, 7) / (pow(Cab, 7) + pow(25.0, 7.0))));

    double a1Prime = (1 + G) * refColor.a;
    double a2Prime = (1 + G) * color.a;

    double C1Prime = sqrt(pow(a1Prime, 2) + pow(refColor.b, 2));
    double C2Prime = sqrt(pow(a2Prime, 2) + pow(color.b, 2));

    double h1Prime = 0, h2Prime = 0;

    if (refColor.b == 0 && a1Prime == 0)
    {
        h1Prime = 0;
    }
    else
    {
        h1Prime = atan2(refColor.b, a1Prime);
        h1Prime *= 180.0 / PI;
        h1Prime = (int)(h1Prime + 360) % 360;
    }

    if (color.b == 0 && a2Prime == 0)
    {
        h2Prime = 0;
    }
    else
    {
        h2Prime = atan2(color.b, a2Prime);
        h2Prime *= 180.0 / PI;
        h2Prime = (int)(h2Prime + 360) % 360;
    }

    double deltaL = color.L - refColor.L;
    double deltaCPrime = C2Prime - C1Prime;

    double deltaHPrime = 0;

    double h = 0.0;

    if (C1Prime == 0 || C2Prime == 0)
    {
        deltaHPrime = 0;
    }
    else
    {
        if (std::abs(h1Prime - h2Prime) <= 180.0)
            deltaHPrime = h2Prime - h1Prime;
        else if (abs(h1Prime - h2Prime) > 180.0 && h2Prime <= h1Prime)
            deltaHPrime = h2Prime - h1Prime + 360.0;
        else
            deltaHPrime = h2Prime - h1Prime - 360.0;
    }

    if (C1Prime * C2Prime == 0)
    {
        h = h1Prime + h2Prime;
    }
    else
    {
        if (abs(h1Prime - h2Prime) <= 180.0)
            h = (h1Prime + h2Prime) / 2;
        else if (abs(h1Prime - h2Prime) > 180.0 && h1Prime + h2Prime < 360.0)
            h = (h1Prime + h2Prime + 360.0) / 2;
        else
            h = (h1Prime + h2Prime - 360.0) / 2;
    }

    double deltaH = 2 * sqrt(C1Prime * C2Prime) * sin(DegreeToRadian(deltaHPrime / 2));

    double avgL = (color.L + refColor.L) / 2;
    double avgC = (C1Prime + C2Prime) / 2;

    double T = 1 - (0.17 * cos(DegreeToRadian(h - 30))) + (0.24 * cos(DegreeToRadian(2 * h))) + (0.32 * cos(DegreeToRadian((3 * h) + 6))) - (0.20 * cos(DegreeToRadian((4 * h) - 63)));

    double deltaTheta = 30 * exp(-(pow((h - 275) / 25, 2)));

    double Rc = 2 * sqrt(pow(avgC, 7) / (pow(avgC, 7) + pow(25.0, 7)));
    double Sl = 1 + ((0.015 * pow(avgL - 50, 2)) / sqrt(20 + pow(avgL - 50, 2)));
    double Sc = 1 + (0.045 * avgC);
    double Sh = 1 + (0.015 * avgC * T);
    double Rt = -sin(DegreeToRadian(2 * deltaTheta)) * Rc;
    double Kl = 1.0, Kc = 1.0, Kh = 1.0;

    double LComponent = pow(deltaL / (Kl * Sl), 2);
    double CComponent = pow(deltaCPrime / (Kc * Sc), 2);
    double HComponent = pow(deltaH / (Kh * Sh), 2);
    double mixedComponent = Rt * (deltaCPrime / (Kc * Sc)) * (deltaH / (Kh * Sh));

    err = sqrt(LComponent + CComponent + HComponent + mixedComponent);

    return err;
}

void ColorAlgo::MatrixMult3x3(double matrix1[3][3], double matrix2[3][3], double result[3][3])
{
    int x, y;
    double tmp[3][3];

    for (y = 0; y < 3; y++)
    {
        for (x = 0; x < 3; x++)
        {
            tmp[y][x] = matrix1[y][0] * matrix2[0][x] + matrix1[y][1] * matrix2[1][x] + matrix1[y][2] * matrix2[2][x];
        }
    }

    for (y = 0; y < 3; y++)
    {
        for (x = 0; x < 3; x++)
        {
            result[y][x] = tmp[y][x];
        }
    }
}

void ColorAlgo::MatrixMult3x3With3x1(double matrix1[3][3], double matrix2[3], double result[3])
{
    double tmp[3];

    tmp[0] = matrix1[0][0] * matrix2[0] + matrix1[0][1] * matrix2[1] + matrix1[0][2] * matrix2[2];
    tmp[1] = matrix1[1][0] * matrix2[0] + matrix1[1][1] * matrix2[1] + matrix1[1][2] * matrix2[2];
    tmp[2] = matrix1[2][0] * matrix2[0] + matrix1[2][1] * matrix2[1] + matrix1[2][2] * matrix2[2];

    result[0] = tmp[0];
    result[1] = tmp[1];
    result[2] = tmp[2];
}

INT32 ColorAlgo::MatrixInverse3x3(double matrix[3][3], double result[3][3])
{
    int retVal = -1;
    double tmp[3][3];
    double determinant = MatrixDeterminant3x3(matrix);

    if (0 != determinant)
    {
        tmp[0][0] = (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) / determinant;
        tmp[0][1] = (matrix[0][2] * matrix[2][1] - matrix[2][2] * matrix[0][1]) / determinant;
        tmp[0][2] = (matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1]) / determinant;
        tmp[1][0] = (matrix[1][2] * matrix[2][0] - matrix[1][0] * matrix[2][2]) / determinant;
        tmp[1][1] = (matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]) / determinant;
        tmp[1][2] = (matrix[0][2] * matrix[1][0] - matrix[0][0] * matrix[1][2]) / determinant;
        tmp[2][0] = (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]) / determinant;
        tmp[2][1] = (matrix[0][1] * matrix[2][0] - matrix[0][0] * matrix[2][1]) / determinant;
        tmp[2][2] = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) / determinant;

        result[0][0] = tmp[0][0]; result[0][1] = tmp[0][1]; result[0][2] = tmp[0][2];
        result[1][0] = tmp[1][0]; result[1][1] = tmp[1][1]; result[1][2] = tmp[1][2];
        result[2][0] = tmp[2][0]; result[2][1] = tmp[2][1]; result[2][2] = tmp[2][2];

        retVal = 0;
    }

    return retVal;
}

double ColorAlgo::MatrixDeterminant3x3(double matrix[3][3])
{
    double result;

    result = matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]);
    result -= matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]);
    result += matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]);

    return result;
}

double ColorAlgo::MatrixMaxVal3x3(double matrix[3][3])
{
    double val, maxVal = 0;

    for (INT32 y = 0; y < 3; y++)
    {
        for (INT32 x = 0; x < 3; x++)
        {
            val = abs(matrix[y][x]);

            if (val > maxVal)
            {
                maxVal = val;
            }
        }
    }

    return maxVal;
}


double ColorAlgo::MatrixMaxSumOfRow3x3(double matrix[3][3])
{
    double val, maxVal = 0;

    for (INT32 y = 0; y < 3; y++)
    {
        val = abs(matrix[y][0] + matrix[y][1] + matrix[y][2]);

        if (val > maxVal)
        {
            maxVal = val;
        }
    }

    return maxVal;
}

void ColorAlgo::MatrixMultScalar3x3(double matrix[3][3], double multiplier)
{
    for (INT32 y = 0; y < 3; y++)
    {
        for (INT32 x = 0; x < 3; x++)
        {
            matrix[y][x] *= multiplier;
        }
    }
}

void ColorAlgo::MatrixNormalize3x3(double matrix[3][3])
{
    double rowSum, rowSumMax = 0;
    double* pMat = (double*)matrix;

    for (int i = 0; i < 3; i++)
    {
        rowSum = matrix[i][0] + matrix[i][1] + matrix[i][2];

        if (abs(rowSum) > rowSumMax)
        {
            rowSumMax = abs(rowSum);
        }
    }

    for (int i = 0; i < 9; i++)
    {
        pMat[i] /= rowSumMax;
    }
}

double ColorAlgo::Clip(double val, double minVal, double maxVal)
{
    if (val < minVal)
    {
        val = minVal;
    }

    if (val > maxVal)
    {
        val = maxVal;
    }

    return val;
}

COLOR_ALGO_ERR ColorAlgo::ComputePixelScaleFactorAndOffsets(COLOR_DATA_PRECISION eBpc, COLOR_RANGE eRange, PIXEL_SCALE_OFFSETS* pScaleOffset)
{
    COLOR_ALGO_ERR retVal = COLOR_ALGO_ERR_NONE;

    if (eRange == COLOR_RANGE_FULL)
    {
        pScaleOffset->rgbScale = pScaleOffset->yScale = pScaleOffset->cbCrScale = 1.0;
        pScaleOffset->yOffset = pScaleOffset->rgbOffset = 0;

        if (eBpc == COLOR_DATA_PRECISION_8BPC)
        {
            pScaleOffset->maxPixelVal = pScaleOffset->maxRGBVal = pScaleOffset->maxYVal = pScaleOffset->maxCbCrVal = 255;
            pScaleOffset->cbCrOffset = 128;
        }
        else if (eBpc == COLOR_DATA_PRECISION_10BPC)
        {
            pScaleOffset->maxPixelVal = pScaleOffset->maxRGBVal = pScaleOffset->maxYVal = pScaleOffset->maxCbCrVal = 1023;
            pScaleOffset->cbCrOffset = 512;
        }
        else if (eBpc == COLOR_DATA_PRECISION_12BPC)
        {
            pScaleOffset->maxPixelVal = pScaleOffset->maxRGBVal = pScaleOffset->maxYVal = pScaleOffset->maxCbCrVal = 4095;
            pScaleOffset->cbCrOffset = 2048;
        }
        else if (eBpc == COLOR_DATA_PRECISION_16BPC)
        {
            pScaleOffset->maxPixelVal = pScaleOffset->maxRGBVal = pScaleOffset->maxYVal = pScaleOffset->maxCbCrVal = 65535;
            pScaleOffset->cbCrOffset = 32768;
        }
        else
        {
            retVal = COLOR_ALGO_ERR_INVALID_ARGS;
        }
    }
    else if (eRange == COLOR_RANGE_LIMITED)
    {
        if (eBpc == COLOR_DATA_PRECISION_8BPC)
        {
            pScaleOffset->maxPixelVal = 255;
            pScaleOffset->maxYVal = pScaleOffset->maxRGBVal = 235;
            pScaleOffset->maxCbCrVal = 240;

            pScaleOffset->yScale = pScaleOffset->rgbScale = 219.0 / 255.0;
            pScaleOffset->cbCrScale = 224.0 / 255.0;
            pScaleOffset->yOffset = pScaleOffset->rgbOffset = 16;
            pScaleOffset->cbCrOffset = 128;
        }
        else if (eBpc == COLOR_DATA_PRECISION_10BPC)
        {
            pScaleOffset->maxPixelVal = 1023;
            pScaleOffset->maxYVal = pScaleOffset->maxRGBVal = 235 * 4;
            pScaleOffset->maxCbCrVal = 240 * 4;

            pScaleOffset->yScale = pScaleOffset->rgbScale = (219.0 * 4.0) / 1023.0;
            pScaleOffset->cbCrScale = (224.0 * 4.0) / 1023.0;
            pScaleOffset->yOffset = pScaleOffset->rgbOffset = 16 * 4;
            pScaleOffset->cbCrOffset = 128 * 4;
        }
        else if (eBpc == COLOR_DATA_PRECISION_12BPC)
        {
            pScaleOffset->maxPixelVal = 4095;
            pScaleOffset->maxYVal = pScaleOffset->maxRGBVal = 235 * 16;
            pScaleOffset->maxCbCrVal = 240 * 16;

            pScaleOffset->yScale = pScaleOffset->rgbScale = (219.0 * 16.0) / 4095.0;
            pScaleOffset->cbCrScale = (224.0 * 16.0) / 4095.0;
            pScaleOffset->yOffset = pScaleOffset->rgbOffset = 16 * 16;
            pScaleOffset->cbCrOffset = 128 * 16;
        }
        else if (eBpc == COLOR_DATA_PRECISION_16BPC)
        {
            pScaleOffset->maxPixelVal = 65535;
            pScaleOffset->maxYVal = pScaleOffset->maxRGBVal = 235 * 256;
            pScaleOffset->maxCbCrVal = 240 * 256;

            pScaleOffset->yScale = pScaleOffset->rgbScale = (219.0 * 256.0) / 65535.0;
            pScaleOffset->cbCrScale = (224.0 * 256.0) / 65535.0;
            pScaleOffset->yOffset = pScaleOffset->rgbOffset = 16 * 256;
            pScaleOffset->cbCrOffset = 128 * 256;
        }
        else
        {
            retVal = COLOR_ALGO_ERR_INVALID_ARGS;
        }
    }
    else
    {
        retVal = COLOR_ALGO_ERR_INVALID_ARGS;
    }

    return retVal;
}



INT32 ColorAlgo::MatrixInverse4X4(double matrix[4][4], double result[4][4])
{

    double det = Determinant(matrix, 4);
    if (det == 0)
    {
        return -1;
    }

    double adjoint[4][4];
    CalculateAdjointMatrix(matrix, adjoint);

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            result[i][j] = adjoint[i][j] / det;
        }
    }
    return 0;

}

double ColorAlgo::MatrixDeterminant4x4(double matrix[4][4])
{
    return Determinant(matrix, 4);
}

void ColorAlgo::GetCofactorMatrix(double mat[4][4], double cofactor[4][4], int order, int currentRow, int currentColumn)
{
    int cofactorRow = 0, CofactorCol = 0;

    for (int i = 0; i < order; i++)
    {
        for (int j = 0; j < order; j++)
        {
            if (i != currentRow && j != currentColumn)
            {
                cofactor[cofactorRow][CofactorCol] = mat[i][j];
                CofactorCol++;
            }
            if (CofactorCol == order - 1)
            {
                CofactorCol = 0;
                cofactorRow++;
            }
        }
    }
}
double ColorAlgo::Determinant(double mat[4][4], int order)
{
    double det = 0;
    double coFactor[4][4];
    int sign = 1;

    if (order == 1)
        return mat[0][0];

    for (int i = 0; i < order; i++)
    {
        GetCofactorMatrix(mat, coFactor, order, 0, i);
        det = det + sign * mat[0][i] * Determinant(coFactor, order - 1);

        sign = sign * -1;
    }
    return det;
}

void ColorAlgo::CalculateAdjointMatrix(double mat[4][4], double adjoint[4][4])
{
    double coFactor[4][4];
    int sign;

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            GetCofactorMatrix(mat, coFactor, 4, i, j);
            sign = pow(-1.0, (i + j));

            adjoint[j][i] = sign * Determinant(coFactor, 3);
        }
    }
}