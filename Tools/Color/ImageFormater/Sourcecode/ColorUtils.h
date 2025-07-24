#ifndef _COLORUTILS
#define _COLORUTILS
#include"common.h"


#define MAX_NUMBER_OF_PLANES 10
#define ONED_LUT_MAX_NUM_SAMPLES 2048
#define ALPHA 0.055

#define MAX_CSC_COEFF_VAL 3.9921875




typedef struct
{
    INT16 mantissa;
    INT16 shiftFactor;

}CSCCoefficient;

typedef struct
{
    UINT16 comp1;       // R or Y
    UINT16 comp2;       // G or Cb
    UINT16 comp3;       // B or Cr
    UINT16 alpha;
}PIXEL;

typedef struct
{
    UINT8 comp1;
    UINT8 comp2;
    UINT8 comp3;
}IMAGEPIXEL;



typedef struct
{
    double comp1;
    double comp2;
    double comp3;
    double alpha;

}NORMALISED_PIXEL;

typedef struct RGBPIXEL {
    unsigned char Red;
    unsigned char Green;
    unsigned char Blue;
};

typedef struct YCBCRPIXEL {
    unsigned char Y;
    unsigned char Cr;
    unsigned char Cb;
};

typedef struct
{
    unsigned int xorigin;
    unsigned int yorigin;
    unsigned int height;
    unsigned int width;
} PLANE_RECT;

typedef struct GLUT {
    unsigned int numberSamples;
    unsigned int maxSampleValue;
    unsigned int lutComp1[ONED_LUT_MAX_NUM_SAMPLES];
    unsigned int lutComp2[ONED_LUT_MAX_NUM_SAMPLES];
    unsigned int lutComp3[ONED_LUT_MAX_NUM_SAMPLES];
};

typedef enum DisplayStandard { SDTV, HDTV, UHDTV };
typedef enum BitsPerPixel { EIGHT = 8, TEN = 10, TWELVE = 12, SIXTEEN = 16 };
typedef enum ColourRange { FULL, LIMITED };

extern double Rgb2YcbcrMatrixBt601[3][3];
extern double Rgb2YcbcrMatrixBt709[3][3];
extern double Rgb2YcbcrMatrixBt2020[3][3];
extern double Ycbcr2RgbMatrixBt601[3][3];
extern double Ycbcr2RgbMatrixBt709[3][3];
extern double Ycbcr2RgbMatrixBt2020[3][3];

static double BT2020_TO_BT709_RGB[3][3] =
{
    1.6604910021084347, -0.58764113878854973, -0.072849863319884745,
    -0.12455047452159063, 1.1328998971259601, -0.0083494226043694941,
    -0.018150763354905206, -0.10057889800800743, 1.1187296613629121
};

class ColorUtils
{

public:
    static void Max(double in1, double* in2);
    static void CopyMatrix3x3(double sourceMatrix[3][3], double destinationMatrix[3][3]);
    static void CopyVector3x1(double sourcematrix[3], double destinationMatrix[3]);
    static void MatrixMultiply3X1With3X3(double matrix3x1[3], double matrix3x3[3][3]);
    static void MatrixMultiply3X1With3X3(DWORD rgbIn[3], INT32 mat[3][3]);

    static void ComputeRgb2YcbcrMatrix(BitsPerPixel bpp, ColourRange Crange, DisplayStandard Dstandard, double convertionMatrix[3][3], double offset[3]);
    static void ComputeYcbcr2RgbMatrix(BitsPerPixel bpp, ColourRange Crange, DisplayStandard dStandard, double convertionMatrix[3][3], double offset[3]);


    static void Rgb2Ycrbcr(BitsPerPixel bpp, ColourRange Crange, DisplayStandard Dformat, RGBPIXEL* rgb, YCBCRPIXEL& ycbcr);
    static void Ycbcr2Rgb(BitsPerPixel bpp, ColourRange Crange, DisplayStandard Dformat, YCBCRPIXEL* ycbcr, RGBPIXEL& rgb);
    static void RgbLimited2RgbFull(BitsPerPixel bpp, RGBPIXEL* rgb);
    static void RgbFull2RgbLimited(BitsPerPixel bpp, RGBPIXEL* rgb);

    static void GetLutValue(GLUT Lut, NORMALISED_PIXEL inputValue, NORMALISED_PIXEL* outputValue);

    static void linear2srgb(double& ci);
    static void srgb2linear(double& ci);

    static void float2Fixedpoint(double inputValue, INT32& outputValue, int IntBits, int fractionlBits);
    static void fixedpoint2Float(INT32 inputInt, double& outputValue, int IntBits, int fractionlBits);
};

#endif