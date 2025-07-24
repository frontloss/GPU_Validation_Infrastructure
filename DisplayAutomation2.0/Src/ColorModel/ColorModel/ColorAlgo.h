// INTEL CONFIDENTIAL
// Copyright(2016-2020) Intel Corporation All Rights Reserved.
// The source code contained or described herein and all documents related to the source code ("Material")
// are owned by Intel Corporation or its suppliers or licensors. Title to the Material remains with
// Intel Corporation or its suppliers and licensors. The Material contains trade secrets and proprietary
// and confidential information of Intel or its suppliers and licensors.
//
// The Material is protected by worldwide copyright and trade secret laws and treaty provisions.
// No part of the Material may be used, copied, reproduced, modified, published, uploaded, posted,
// transmitted, distributed, or disclosed in any way without Intel’s prior express written permission.
//
// No license under any patent, copyright, trade secret or other intellectual property right is granted
// to or conferred upon you by disclosure or delivery of the Materials, either expressly, by implication,
// inducement, estoppel or otherwise. Any license under such intellectual property rights must be express
// and approved by Intel in writing.

//------------------------------------------------------------------------------------------------------
// PRIMARY AUTHOR : susantab
//------------------------------------------------------------------------------------------------------

#ifndef _COLOR_ALGO_INCLUDED
#define _COLOR_ALGO_INCLUDED

#include <Windows.h>
#include "StandardDef.h"

#define PI 3.141592653589793

#define MIN_Y 0
#define MAX_Y 1000

// typedef UINT8  DDU8;
// typedef UINT16 DDU16;
// typedef UINT32 DDU32;
// typedef INT32  DDI32;
// typedef UINT64 DDU64;
//
typedef INT32 DDSTATUS;

#define DDASSERT
#define DDS_UNSUCCESSFUL -1
#define DDS_SUCCESS 0

#define UNITY_VAL_IN_8_24_FORMAT 16777216
#define FINAL_SLOPE_TM_CURVE 503316 // 0.03 * UNITY_VAL_IN_8_24_FORMAT
#define VALUE_AT_UNITY_SLOPE 167772 // 0.01 * VALUE_AT_UNITY_SLOPE
#define VALUE_AT_INFLECTION_POINT1

//#define USE_DELTAE_2000

#define CONVERT_MILLI_NITS_VALUE_TO_8_24_FORMAT(InputValue) (DD_ROUND_DIV((DDU64)InputValue * (DDU64)MAX_24BIT_VALUE, 1000 * 10000))
#define NITS_700_IN_8_24_FORMAT 1174405
#define DD_ZERO_MEM ZeroMemory

//-----------------------------------------------------------------------------
// Macro: DD_BITFIELD_RANGE
// PURPOSE: Calculates the number of bits between the startbit and the endbit
// and count is inclusive of both bits. The bits are 0 based.
//-----------------------------------------------------------------------------
#define DD_BITFIELD_RANGE(ulLowBit, ulHighBit) ((ulHighBit) - (ulLowBit) + 1)

#define DD_MIN(a, b) ((a) < (b) ? (a) : (b))
#define DD_MAX(a, b) ((a) < (b) ? (b) : (a))
#define DD_CLAMP_MIN_MAX(a, min, max) ((a) < (min) ? (min) : DD_MIN((a), (max)))
#define DD_ROUND_UP_DIV(x, y) (((x) % (y) == 0) ? ((x) / (y)) : (((x) / (y)) + 1))
#define DD_ROUND_DIV(x, y) (((x) + (y) / 2) / (y))
#define DD_ROUND_DOWN_DIV(x, y) ((x) / (y))
#define DD_ROUNDTONEARESTINT(p) (int)(p + 0.5)
#define DD_ABS(x) ((x) < 0 ? -(x) : (x))
#define DD_DIFF(a, b) (((a) > (b)) ? ((a) - (b)) : ((b) - (a)))
#define DD_GET_ELAPSED_COUNT(curr, last, count_max) (((curr) >= (last)) ? ((curr) - (last)) : ((count_max) - (last) + (curr) + 1))
#define DD_SWAP(X, Y) \
    {                 \
        (X) ^= (Y);   \
        (Y) ^= (X);   \
        (X) ^= (Y);   \
    }

typedef enum
{
    COLOR_CHANNEL_RED   = 1,
    COLOR_CHANNEL_GREEN = 2,
    COLOR_CHANNEL_BLUE  = 4,
    COLOR_CHANNEL_ALL   = (COLOR_CHANNEL_RED | COLOR_CHANNEL_GREEN | COLOR_CHANNEL_BLUE)
} COLOR_CHANNEL;

typedef enum
{
    COLOR_ALGO_ERR_NONE = 0,
    COLOR_ALGO_ERR_INVALID_ARGS,
    COLOR_ALGO_ERR_INVALID_DATA,
    COLOR_ALGO_ERR_INSUFFICIENT_MEMORY
} COLOR_ALGO_ERR;

typedef enum
{
    COLOR_MODEL_RGB        = 0,
    COLOR_MODEL_YCBCR_601  = 1,
    COLOR_MODEL_YCBCR_709  = 2,
    COLOR_MODEL_YCBCR_2020 = 1,
    COLOR_MODEL_HSV        = 2
} COLOR_MODEL;

typedef enum
{
    COLOR_SUBSAMPLING_444 = 0,
    COLOR_SUBSAMPLING_422 = 1,
    COLOR_SUBSAMPLING_420 = 2
} COLOR_SUBSAMPLING;

typedef enum
{
    COLOR_ENCODING_22     = 0,
    COLOR_ENCODING_2084   = 1,
    COLOR_ENCODING_LINEAR = 2
} COLOR_ENCODING;

typedef enum
{
    COLOR_SPACE_SRGB  = 0,
    COLOR_SPACE_ARGB  = 1,
    COLOR_SPACE_DCIP3 = 2,
    COLOR_SPACE_2020  = 3,
    COLOR_SPACE_CCCS  = 4,
    COLOR_SPACE_CUSTOM
} COLOR_SPACE;

typedef enum
{
    COLOR_RANGE_FULL    = 0,
    COLOR_RANGE_LIMITED = 1,
    COLOR_RANGE_XR_BIAS = 2,
    COLOR_RANGE_XVYCC   = 3
} COLOR_RANGE;

typedef enum
{
    COLOR_DATA_PRECISION_8BPC  = 0,
    COLOR_DATA_PRECISION_10BPC = 1,
    COLOR_DATA_PRECISION_12BPC = 2,
    COLOR_DATA_PRECISION_16BPC = 3,
    COLOR_DATA_PRECISION_FP16  = 4
} COLOR_DATA_PRECISION;

typedef struct
{
    double x;         // CIE1931 x
    double y;         // CIE1931 y
    double luminance; // CIE1931 Y
} Chromaticity;

typedef struct
{
    double X;
    double Y;
    double Z;
} ChromaticityXYZ;

typedef struct
{
    double L;
    double a;
    double b;
} ChromaticityLab;

typedef struct
{
    DWORD red;
    DWORD green;
    DWORD blue;
} ColorRGB;

typedef struct
{
    DDU8 red;
    DDU8 green;
    DDU8 blue;
    DDU8 alpha;
} IPIXEL8;

#pragma pack(1)
typedef struct
{
    UINT red : 10;
    UINT green : 10;
    UINT blue : 10;
    UINT alpha : 2;
} IPIXEL10;
#pragma pack()

typedef struct
{
    DDU16 red; // Either in DDU16 or FP16
    DDU16 green;
    DDU16 blue;
    DDU16 alpha;
} IPIXEL16;

#ifdef _USE_SIMD
typedef union {
    struct
    {
        DDU32 red;
        DDU32 green;
        DDU32 blue;
        DDU32 alpha;
    };
    __m128i vPix;
} IPIXEL32;
#else
typedef struct
{
    DDU32 red;
    DDU32 green;
    DDU32 blue;
    DDU32 alpha;
} IPIXEL32;
#endif

#ifdef _USE_SIMD
typedef union {
    struct
    {
        float red;
        float green;
        float blue;
        float alpha;
    };
    __m128 vPix;
} IPIXELF;
#else
typedef struct
{
    float red;
    float green;
    float blue;
    float alpha;
} IPIXELF;
#endif

#ifdef _USE_SIMD
typedef union {
    struct
    {
        double red;
        double green;
        double blue;
        double alpha;
    };
    __m256d vPix;
} IPIXELD;
#else
typedef struct
{
    double red;
    double green;
    double blue;
    double alpha;
} IPIXELD;
#endif

typedef struct
{
    Chromaticity white;
    Chromaticity red;
    Chromaticity green;
    Chromaticity blue;
} ColorSpace;

typedef struct
{
    UINT blue : 10;
    UINT green : 10;
    UINT red : 10;
    UINT x : 2;
} ColorB10G10R10X2;

typedef struct
{
    DWORD     nSamples;
    DWORD     maxVal;
    ColorRGB *pLutData;
} OneDLUT;

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
} PIXEL_SCALE_OFFSETS;

typedef struct _DD_POINT
{
    DDU32 X;
    DDU32 Y;
} DD_POINT;

// The below structure is used for gamma LUT values.
// Format is 8.24 format. This is doen to avoid Floating point caluclations in driver.
// Gamma cannot be negative hence this is unsigned
// This gives 24 bit precision which is good enough for most of OS like windows(16bpc), Linux(24bpc)
typedef union _DDU8_24 {
    DDU32 Value;
    struct
    {
        DDU32 Fraction : DD_BITFIELD_RANGE(0, 23);
        DDU32 Integer : DD_BITFIELD_RANGE(24, 31);
    };
} DDU8_24;

typedef union _DDU16_48 {
    DDU64 Value;
    struct
    {
        DDU64 Fraction : DD_BITFIELD_RANGE(0, 47);
        DDU64 Integer : DD_BITFIELD_RANGE(48, 63);
    };
} DDU16_48;

typedef union _DDU40_24 {
    DDU64 Value;
    struct
    {
        DDU64 Fraction : DD_BITFIELD_RANGE(0, 23);
        DDU64 Integer : DD_BITFIELD_RANGE(24, 63);
    };
} DDU40_24;

typedef struct _DD_TONE_MAPPING_PARAMS
{
    DDU32 MinOutputLuminanceInMilliNits;
    DDU32 MaxOutputLuminanceInMilliNits;
    DDU32 MinInputLuminanceInMilliNits;
    DDU32 MaxInputLuminanceInMilliNits;
    DDU32 LutSize; // Generated Output Lut Size
} DD_TONE_MAPPING_PARAMS;

class ColorAlgo
{
  public:
    ColorAlgo();
    ~ColorAlgo();

    static COLOR_ALGO_ERR CreateGamutMappingMatrix(ColorSpace *pSrcColorSpace, ColorSpace *pPanelColorSpace, double result[3][3]);
    static COLOR_ALGO_ERR CreateWhitePointAdaptationMatrix(ColorSpace *pSrcColorSpace, ColorSpace *pPanelColorSpace, Chromaticity *pTargetWhitePoint, double result[3][3]);
    static COLOR_ALGO_ERR CreateWhitePointAdaptationMatrix(ColorSpace *pSrcSpace, ColorSpace *pPanelSpace, double T, double mat[3][3]);
    static COLOR_ALGO_ERR CreateWhitePointAdaptationLUT(ColorSpace *pSrcSpace, ColorSpace *pPanelSpace, double T, OneDLUT *pLUT);

    static COLOR_ALGO_ERR GenerateDeGammaLUT(OneDLUT &lut);
    static COLOR_ALGO_ERR GenerateUnityLUT(OneDLUT &lut);
    static COLOR_ALGO_ERR GenerateGammaLUT(OneDLUT &lut);
    static COLOR_ALGO_ERR GenerateEOTF2084LUT(OneDLUT &lut);
    static COLOR_ALGO_ERR GenerateOETF2084LUT(OneDLUT &lut, double toneMappingFactor = 1.0);
    static COLOR_ALGO_ERR Generate3SegmentedOETFTable_524Samples_16BPC(DWORD *pTab, double toneMappingFactor = 1.0);
    static COLOR_ALGO_ERR Generate3SegmentedOETFTable_524Samples_Normalized(double *pTab, double toneMappingFactor = 1.0);
    static COLOR_ALGO_ERR NewGenerate3SegmentedOETFTable_524Samples_16BPC(double *pTab, double toneMappingFactor = 1.0);
    static COLOR_ALGO_ERR GenerateSDR2HDRLUT(OneDLUT &lut);

    static COLOR_ALGO_ERR ResizeLUT(OneDLUT *pSrcLUT, OneDLUT *pDstLUT);
    static COLOR_ALGO_ERR GetEDIDChromaticity(UINT8 *edidV1Chromaticity, ColorSpace &colorSpace);
    static COLOR_ALGO_ERR ComputePixelScaleFactorAndOffsets(COLOR_DATA_PRECISION eBpc, COLOR_RANGE eRange, PIXEL_SCALE_OFFSETS *pScaleOffset);

    static void GetSrgbColorSpace(ColorSpace &cspace);
    static void Create2020To709Matrix(double result[3][3]);
    static void Create2020ToDCIP3Matrix(double result[3][3]);
    static void CreateDCIP3To2020Matrix(double result[3][3]);
    static void Create709ToDCIP3Matrix(double result[3][3]);
    static void CreateDCIP3To709Matrix(double result[3][3]);
    static void Create709To2020Matrix(double result[3][3]);

    static double Clip(double val, double minVal, double maxVal);
    static double GetSRGBDecodingValue(double input);
    static double GetSRGBEncodingValue(double input);
    static double EOTF_2084(double input);
    static double OETF_2084(double input, double srcMaxLuminance = 10000.0f);
    static double MatrixDeterminant3x3(double matrix[3][3]);
    static double MatrixMaxVal3x3(double matrix[3][3]);
    static double MatrixMaxSumOfRow3x3(double matrix[3][3]);
    static double CalculateDeltaE(ChromaticityXYZ refColor, ChromaticityXYZ color);
    static double ApplyLUT(OneDLUT *pLUT, double input, COLOR_CHANNEL channel);
    static double ApplyLUT(OneDLUT *pLUT, double input); // Only Red channel of LUT will be used for computation.
    static DDU32  ApplyLUT(DDU8_24 *pInputLut, DDU32 NumSamples, DDU32 Input);
    static void   ApplyTMLUT(IPIXELD &Rgbd, double *pLUT, DDU32 nSamples);
    static void   ApplyD12TMLUT(IPIXELD &Rgbd, double *pLUT);
    static void   ApplyLogTMLUT(IPIXELD &NormalizedPixel, DDU32 NumOfSegments, DDU32 *pNumOfEntriesPerSegment, DDU32 *pSegmentLutIndexMapping, DDU32 *pInputLut,
                                DDU32 NumOfInputLutSamples, DDU32 MaxValue);
    static double ApplyMultiSegmentedLUT_524Samples_16BPC(DWORD *pLUT, double inp);

    static double HalfToDouble(USHORT inp);
    static USHORT DoubleToHalf(double inp);
    static INT32  MatrixInverse3x3(double matrix[3][3], double result[3][3]);
    static bool   IsColorSpaceValid(ColorSpace *pSpace);

    static void MatrixMult3x3(double matrix1[3][3], double matrix2[3][3], double result[3][3]);
    static void MatrixMult3x3With3x1(double matrix1[3][3], double matrix2[3], double result[3]);
    static void MatrixMultScalar3x3(double matrix[3][3], double multiplier);
    static void MatrixNormalize3x3(double matrix[3][3]);
    static void CreateRGB2XYZMatrix(ColorSpace *cspace, double rgb2xyz[3][3]);
    static void CreateRGB2YCbCrMatrix(COLOR_MODEL eModel, double rgb2ycbcr[3][3]);

    static void     Apply3DLUT(ColorB10G10R10X2 *pLUT, DWORD dwLUTDepth, IPIXELD *pInPixel, IPIXELD *pOutPixel);
    static DDSTATUS GenerateH2HToneMappingLut(DD_TONE_MAPPING_PARAMS *pToneMappingParams, DDU8_24 *pOutputMultiplierLut);
    static DDSTATUS GenerateH2HToneMappingLut_Bezier(DD_TONE_MAPPING_PARAMS *pToneMappingParams, DDU8_24 *pOutputMultiplierLut);
    static DDSTATUS GenerateH2HToneMappingLut_TGL(DD_TONE_MAPPING_PARAMS *pToneMappingParams, DDU8_24 *pOutputMultiplierLut);

    static void  Create_LogLut_OETF2084_24Bit(DDU32 NumOfSegments, DDU32 *pNumOfEntriesPerSegment, DDU32 *pOutputLut, DDU32 *pSegmentLutIndexMapping);
    static void  Create_LogLut_UNITY_24Bit(DDU32 NumOfSegments, DDU32 *pNumOfEntriesPerSegment, DDU32 *pOutputLut, DDU32 *pSegmentLutIndexMapping);
    static DDU32 Apply_LogLut_24Bit(DDU32 NumOfSegments, DDU32 *pNumOfEntriesPerSegment, DDU32 *pSegmentLutIndexMapping, DDU32 *pInputLut, DDU32 InputLutNumOfSamples, DDU32 Input);
    static DDU32 Apply_LogLut_24Bit(DDU32 *pNumOfEntriesPerSegment, DDU32 *pSegmentLutIndexMapping, DDU32 *pInputLut, DDU32 Input);
    static double Apply_LogLut_24Bit(double *pSegmentIndexMappingFactor, DDU32 *pSegmentLutIndexMapping, double *pInputLut, DDU32 LutMaxSampleVal, double Input);
    static double Apply_Uniformly_Segmented_LogLut_24Bit(double *pLut, double DenormalizedInput, DDU32 NumSamplesWithinSegment);

  private:
    static void   CreateGamutScalingMatrix(ColorSpace *pSrc, ColorSpace *pDst, double result[3][3]);
    static void   GeWhitePointAdaptationMatrixRGB(ColorSpace *pSrcColorSpace, ColorSpace *pPanelColorSpace, Chromaticity *pTargetWhitePoint, double result[3][3]);
    static void   GeWhitePointAdaptationMatrixXYZ(Chromaticity *pSrcWhitePoint, Chromaticity *pPanelWhitePoint, double result[3][3]);
    static void   GetCIELab(ChromaticityXYZ color, ChromaticityXYZ whitePoint, ChromaticityLab &colorLab);
    static void   GetxyYFromCCT(double T, double &x, double &y);
    static bool   IsNarrowGamut(ColorSpace *pPanelColorSpace);
    static bool   IsChromaticityValid(Chromaticity *pChroma);
    static bool   IsWhitePointWithinTriangle(ColorSpace *cspace);
    static double DegreeToRadian(double degrees);
    static double CIELabTxFn(double inp);
    static double CalculateTriangleArea(ColorSpace *cspace);
    static double CalculateDeltaECIE94(ChromaticityLab refColor, ChromaticityLab color);
    static double CalculateDeltaECIEDE2000(ChromaticityLab refColor, ChromaticityLab color);

    static void GetValueAtRGB(ColorB10G10R10X2 *pLUT, DWORD dwDepth, double r, double g, double b, IPIXELD *pVal);
    static void Interpolate3D(ColorB10G10R10X2 *pLUT, DWORD dwDepth, IPIXELD *p0, IPIXELD *p1, IPIXELD *p, IPIXELD *pOut);

    static DDU32   MultiplyTwo_8_24Numbers(DDU32 Number1, DDU32 Number2);
    static DDU32   DivideTwo_8_24Numbers(DDU32 Number1, DDU32 Number2);
    static DDU32   GetPreToneMappingScaleFactor(DDU32 MaxContentLuminance);
    static BOOLEAN IsToneMappingPossible(DDU32 MaxContentLuminance, DDU32 MaxDisplayLuminance, DDU32 LutSize);

    static void GenerateToneMappingAnchorPoints(DD_POINT AnchorPoints[6], DDU32 MinDisplayLuminance, DDU32 SecondAnchorPointInNits, DDU32 MaxContentLuminance,
                                                DDU32 MaxDisplayLuminance, DDU32 SlopeOfLastButOneSegment);

    static void GenerateLuminanceOutputLut(DD_POINT AnchorPoints[6], DDU32 InputStepSize, DDU32 LutSize, DDU32 FinalIndex, DDU32 MaxContentLuminance, DDU32 MaxDisplayLuminance,
                                           DDU8_24 *pOutputLuminanceLut);

    static void CreateBezierCurve(DDU8_24 y1, DDU8_24 y2, DDU8_24 y3, DDU8_24 y4, DDU8_24 inputStepSize, DDU32 startIndex, DDU32 endIndex, DDU8_24 *pOutputMultiplierLut);

    static void WindowFilterWith17Points(DDU32 StartIndex, DDU32 EndIndex, DDU8_24 *pOutputMultiplierLut);
    static void WindowFilterWith9Points(DDU32 StartIndex, DDU32 EndIndex, DDU8_24 *pOutputMultiplierLut);
    static void WindowFilterWith5Points(DDU32 StartIndex, DDU32 EndIndex, DDU8_24 *pOutputMultiplierLut);
    static void WindowFilterWith3Points(DDU32 StartIndex, DDU32 EndIndex, DDU8_24 *pOutputMultiplierLut);
};

#endif // _COLOR_ALGO_INCLUDED
