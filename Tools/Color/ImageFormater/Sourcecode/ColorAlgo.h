#ifndef _COLOR_ALGO_INCLUDED
#define _COLOR_ALGO_INCLUDED

#include <Windows.h>

#define PI 3.141592653589793

#define MIN_Y 0
#define MAX_Y 1000

//#define USE_DELTAE_2000

typedef enum
{
    COLOR_CHANNEL_RED = 1,
    COLOR_CHANNEL_GREEN = 2,
    COLOR_CHANNEL_BLUE = 4,
    COLOR_CHANNEL_ALL = (COLOR_CHANNEL_RED | COLOR_CHANNEL_GREEN | COLOR_CHANNEL_BLUE)
}COLOR_CHANNEL;

typedef enum
{
    COLOR_ALGO_ERR_NONE = 0,
    COLOR_ALGO_ERR_INVALID_ARGS,
    COLOR_ALGO_ERR_INVALID_DATA,
    COLOR_ALGO_ERR_INSUFFICIENT_MEMORY
}COLOR_ALGO_ERR;

typedef enum
{
    COLOR_MODEL_RGB = 0,
    COLOR_MODEL_YCBCR_601 = 1,
    COLOR_MODEL_YCBCR_709 = 2,
    COLOR_MODEL_YCBCR_2020 = 1,
    COLOR_MODEL_HSV = 2
}COLOR_MODEL;

typedef enum
{
    COLOR_SUBSAMPLING_444 = 0,
    COLOR_SUBSAMPLING_422 = 1,
    COLOR_SUBSAMPLING_420 = 2
}COLOR_SUBSAMPLING;

typedef enum
{
    COLOR_ENCODING_22 = 0,
    COLOR_ENCODING_2084 = 1,
    COLOR_ENCODING_LINEAR = 2
}COLOR_ENCODING;

typedef enum
{
    COLOR_SPACE_SRGB = 0,
    COLOR_SPACE_ARGB = 1,
    COLOR_SPACE_DCIP3 = 2,
    COLOR_SPACE_2020 = 3,
    COLOR_SPACE_CCCS = 4,
    COLOR_SPACE_CUSTOM
}COLOR_SPACE;

typedef enum
{
    COLOR_RANGE_FULL = 0,
    COLOR_RANGE_LIMITED = 1,
    COLOR_RANGE_XR_BIAS = 2,
    COLOR_RANGE_XVYCC = 3
}COLOR_RANGE;

typedef enum
{
    COLOR_DATA_PRECISION_8BPC = 0,
    COLOR_DATA_PRECISION_10BPC = 1,
    COLOR_DATA_PRECISION_12BPC = 2,
    COLOR_DATA_PRECISION_16BPC = 3,
    COLOR_DATA_PRECISION_FP16 = 4
}COLOR_DATA_PRECISION;

typedef struct
{
    double x;           // CIE1931 x
    double y;           // CIE1931 y
    double luminance;   // CIE1931 Y
}Chromaticity;

typedef struct
{
    double X;
    double Y;
    double Z;
}ChromaticityXYZ;

typedef struct
{
    double L;
    double a;
    double b;
}ChromaticityLab;

typedef struct
{
    DWORD r;
    DWORD g;
    DWORD b;
}ColorRGB;

typedef struct
{
    Chromaticity white;
    Chromaticity red;
    Chromaticity green;
    Chromaticity blue;
}ColorSpace;

typedef struct
{
    UINT a : 2;
    UINT b : 10;
    UINT g : 10;
    UINT r : 10;
}ColorBGR10;

typedef struct
{
    UINT b : 10;
    UINT g : 10;
    UINT r : 10;
    UINT a : 2;
}ColorA2R10G10B10;

typedef struct
{
    UINT16 a;
    UINT16 r;
    UINT16 g;
    UINT16 b;
}ColorARGBFP16;

typedef struct
{
    DWORD nSamples;
    DWORD maxVal;
    ColorRGB* pLutData;
}OneDLUT;

typedef struct
{
    double maxPixelVal;
    double maxRGBVal;
    double maxYVal;
    double maxCbCrVal;
    double rgbScale;
    double yScale;
    double cbCrScale;
    UINT16 rgbOffset;
    UINT16 yOffset;
    UINT16 cbCrOffset;
}PIXEL_SCALE_OFFSETS;

class ColorAlgo
{
public:
    ColorAlgo();
    ~ColorAlgo();

    static COLOR_ALGO_ERR CreateGamutMappingMatrix(ColorSpace* pSrcColorSpace, ColorSpace* pPanelColorSpace, double result[3][3]);
    static COLOR_ALGO_ERR CreateWhitePointAdaptationMatrix(ColorSpace* pSrcColorSpace, ColorSpace* pPanelColorSpace, Chromaticity* pTargetWhitePoint, double result[3][3]);
    static COLOR_ALGO_ERR CreateWhitePointAdaptationMatrix(ColorSpace* pSrcSpace, ColorSpace* pPanelSpace, double T, double mat[3][3]);
    static COLOR_ALGO_ERR CreateWhitePointAdaptationLUT(ColorSpace* pSrcSpace, ColorSpace* pPanelSpace, double T, OneDLUT* pLUT);

    static COLOR_ALGO_ERR GenerateDeGammaLUT(OneDLUT& lut);
    static COLOR_ALGO_ERR GenerateGammaLUT(OneDLUT& lut);
    static COLOR_ALGO_ERR GenerateEOTF2084LUT(OneDLUT& lut);
    static COLOR_ALGO_ERR GenerateOETF2084LUT(OneDLUT& lut, double toneMappingFactor = 1.0);
    static COLOR_ALGO_ERR GenerateSDR2HDRLUT(OneDLUT& lut);

    static COLOR_ALGO_ERR ResizeLUT(OneDLUT* pSrcLUT, OneDLUT* pDstLUT);
    static COLOR_ALGO_ERR GetEDIDChromaticity(UINT8* edidV1Chromaticity, ColorSpace& colorSpace);
    static COLOR_ALGO_ERR ComputePixelScaleFactorAndOffsets(COLOR_DATA_PRECISION eBpc, COLOR_RANGE eRange, PIXEL_SCALE_OFFSETS* pScaleOffset);

    static void GetSrgbColorSpace(ColorSpace& cspace);
    static void Create2020To709Matrix(double result[3][3]);
    static void Create2020ToDCIP3Matrix(double result[3][3]);
    static void Create709ToDCIP3Matrix(double result[3][3]);
    static void Create709To2020Matrix(double result[3][3]);

    static double Clip(double val, double minVal, double maxVal);
    static double GetSRGBDecodingValue(double input);
    static double GetSRGBEncodingValue(double input);
    static double EOTF_2084(double input);
    static double OETF_2084(double input, double srcMaxLuminance = 10000.0f);
    static double MatrixDeterminant3x3(double matrix[3][3]);
    static double MatrixDeterminant4x4(double matrix[4][4]);
    static double MatrixMaxVal3x3(double matrix[3][3]);
    static double MatrixMaxSumOfRow3x3(double matrix[3][3]);
    static double CalculateDeltaE(ChromaticityXYZ refColor, ChromaticityXYZ color);
    static double ApplyLUT(OneDLUT* pLUT, double input, COLOR_CHANNEL channel);

    static double HalfToDouble(USHORT inp);
    static USHORT DoubleToHalf(double inp);
    static INT32 MatrixInverse3x3(double matrix[3][3], double result[3][3]);
    static INT32 MatrixInverse4X4(double matrix[4][4], double result[4][4]);
    static bool IsColorSpaceValid(ColorSpace* pSpace);

    static void MatrixMult3x3(double matrix1[3][3], double matrix2[3][3], double result[3][3]);
    static void MatrixMult3x3With3x1(double matrix1[3][3], double matrix2[3], double result[3]);
    static void MatrixMultScalar3x3(double matrix[3][3], double multiplier);
    static void MatrixNormalize3x3(double matrix[3][3]);
    static void CreateRGB2XYZMatrix(ColorSpace* cspace, double rgb2xyz[3][3]);
    static void CreateRGB2YCbCrMatrix(COLOR_MODEL eModel, double rgb2ycbcr[3][3]);

private:

    static void CreateGamutScalingMatrix(ColorSpace* pSrc, ColorSpace* pDst, double result[3][3]);
    static void GeWhitePointAdaptationMatrixRGB(ColorSpace* pSrcColorSpace, ColorSpace* pPanelColorSpace, Chromaticity* pTargetWhitePoint, double result[3][3]);
    static void GeWhitePointAdaptationMatrixXYZ(Chromaticity* pSrcWhitePoint, Chromaticity* pPanelWhitePoint, double result[3][3]);
    static void GetCIELab(ChromaticityXYZ color, ChromaticityXYZ whitePoint, ChromaticityLab& colorLab);
    static void GetxyYFromCCT(double T, double& x, double& y);
    static bool IsNarrowGamut(ColorSpace* pPanelColorSpace);
    static bool IsChromaticityValid(Chromaticity* pChroma);
    static bool IsWhitePointWithinTriangle(ColorSpace* cspace);
    static double DegreeToRadian(double degrees);
    static double CIELabTxFn(double inp);
    static double CalculateTriangleArea(ColorSpace* cspace);
    static double CalculateDeltaECIE94(ChromaticityLab refColor, ChromaticityLab color);
    static double CalculateDeltaECIEDE2000(ChromaticityLab refColor, ChromaticityLab color);

    static void GetCofactorMatrix(double mat[4][4], double cofactor[4][4], int order, int currentRow, int currentColumn);
    static double Determinant(double mat[4][4], int order);
    static void CalculateAdjointMatrix(double mat[4][4], double adjoint[4][4]);

};

#endif   // _COLOR_ALGO_INCLUDED
