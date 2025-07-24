#ifndef IMAGE_PROC_INCLUDED

#include <Windows.h>
#include "ColorAlgo.h"
#include "ImageIO.h"


/* 8 BPC
#define RED_MASK    0xFF000000
#define GREEN_MASK    0x00FF0000
#define BLUE_MASK    0x0000FF00
#define MAX_PIXEL_VAL 255
*/


// 10 BPC
#define BMP_RED_MASK    0xFFC00000
#define BMP_GREEN_MASK    0x003FF000
#define BMP_BLUE_MASK    0x00000FFC
#define MAX_PIXEL_VAL    1023

#define MAX_IMAGE_DIMENSION 8192
#define MAX_NITS 128.0

typedef enum
{
    IMAGE_ERR_NONE = 0,
    IMAGE_ERR_UNSUPPORTED_FILE_FORMAT,
    IMAGE_ERR_INSUFFICIENT_MEMORY,
    IMAGE_ERR_INVALID_PARAMETER,
    IMAGE_ERR_UNSUPPORTED_FEATURE,
    IMAGE_ERR_FILE_IO
}IMAGE_ERR;

typedef struct
{
    UINT32  size;                   // size of this structure
    UINT32  ecolorModel;            // enum COLOR_MODEL
    UINT32  eSubsampling;           // enum COLOR_SUBSAMPLING, applicable for YUV only. Second priority
    UINT32  eEncoding;              // enum COLOR_ENCODING
    UINT32  eColorRange;            // enum COLOR_RANGE
    UINT32  ecolorSpace;            // enum COLOR_SPACE
    UINT32  eDataPrecision;         // enum COLOR_DATA_PRECISION
    UINT32  reserved[4];            // for future use
    float   minLuminance;           // cd/m2
    float   maxLuminance;           // cd/m2
    ColorSpace colorSpace;          // applicable for COLOR_SPACE_CUSTOM
}IMAGE_COLOR_INFO;

typedef struct
{
    UINT8  tag[4];              // "iimg"
    UINT32 size;                // size of this structure
    UINT32 sizeOfFile;          // size of the entire image file
    UINT32 width;
    UINT32 height;
    IMAGE_COLOR_INFO coloInfo;
}IMAGE_HEADER;

typedef struct
{
    UINT32 top;
    UINT32 left;
    UINT32 width;
    UINT32 height;
}IMAGE_RECTANGLE;

typedef struct
{
    COLOR_ENCODING encoding;
    double minLuminance;
    double maxLuminance;
}IMAGE_METADATA;

typedef struct
{
    BITMAPFILEHEADER hdr;
    BITMAPV4HEADER infoHdr;
}BMP_FILE_HEADER;

class ImageProc
{
public:
    ImageProc(WCHAR* pImageFile);                                                                           // Initializes object with parameters from given file
    ImageProc(WCHAR* pImageFile, DWORD width, DWORD height);                                                // Open raw data file
    ImageProc(DWORD width, DWORD height, IMAGE_COLOR_INFO* pColorInfo = NULL, IPIXEL* pBackground = NULL);  // Creates empty image with given dimensions
    ~ImageProc();

    IMAGE_ERR RotateImage(DWORD dwAngle);                                           // Counter clock wise always. Supports only 90, 180, 270
    IMAGE_ERR ResizeImage(DWORD width, DWORD height);                               // Linear interpolation only
    IMAGE_ERR GetRectangle(IMAGE_RECTANGLE* pRect, IPIXEL* pPixData);               // Get pixels of a given rectangle
    IMAGE_ERR PaintRectangle(IMAGE_RECTANGLE* pRect, IPIXEL* pSolidColor);
    IMAGE_ERR SetRectangle(IMAGE_RECTANGLE* pRect, IPIXEL* pPixels);
    IMAGE_ERR BlendRectangle(IPIXEL* pPixels, double alpha, IMAGE_RECTANGLE* pBlendRect,
        IMAGE_RECTANGLE* pAlphaRect, IMAGE_METADATA* pBackgroundMetadata, IMAGE_METADATA* pForegroundMetadata, IMAGE_METADATA* pOutMetadata);
    IMAGE_ERR ConvertToRGB(COLOR_RANGE eRange, COLOR_DATA_PRECISION ePrecision, void* pPixelData);
    IMAGE_ERR ConvertToYCBCR(COLOR_MODEL eModel, COLOR_RANGE eRange, COLOR_SUBSAMPLING eSampling, COLOR_DATA_PRECISION ePrecision, void* pPixelData);

    IMAGE_ERR ApplyEOTF(COLOR_ENCODING encoding);
    IMAGE_ERR ApplyOETF(COLOR_ENCODING encoding);

    IMAGE_ERR ApplyLUT(OneDLUT* pLUT);
    IMAGE_ERR ApplyLUTAndMatrix(OneDLUT* pPreLUT, OneDLUT* pPostLUT, double ctm[3][3]);
    IMAGE_ERR ApplyMatrix(double ctm[3][3], COLOR_ENCODING inpEncoding, COLOR_ENCODING outEncoding, double inpLuminance = 10000.0);

    IMAGE_ERR WriteImage(WCHAR* pImageFile);        // Write image (may be transformed through different methods) to a file
    IMAGE_ERR WriteImageAsRaw(WCHAR* pImageFile);   // Write image as a raw dump of data
    IMAGE_ERR WriteImageAsBMP(WCHAR* pImageFile, COLOR_RANGE eRange = COLOR_RANGE_FULL);             // Write image as 10bpc BMP file
    IMAGE_ERR WriteImageAsBMP(WCHAR* pImageFile, COLOR_SPACE eSpace, COLOR_RANGE eRange = COLOR_RANGE_FULL);    // Gamut convert pixels and write image as 10bpc BMP file

    IPIXEL* GetPixelArray();

    void GetImageColorInfo(IMAGE_COLOR_INFO& colorInfo);
    void GetImageDimension(DWORD& w, DWORD& h);

private:

    ImageIO* mImageIO;

    IPIXEL* mPixelData;
    IPIXEL* mPixelDataTmp;
    IMAGE_HEADER mImageHeader;
    PIXEL_SCALE_OFFSETS mScaleOffset;

    double mYCbCrMat[3][3];
    double mMaxPixelVal;

    IMAGE_ERR Initialize();
    IMAGE_ERR ConvertToYCbCr444Planar(void* pPixelData, COLOR_DATA_PRECISION ePrecision);
    IMAGE_ERR ConvertToYCbCr420Planar(void* pPixelData, COLOR_DATA_PRECISION ePrecision);
    IMAGE_ERR ConvertToYCbCr422Planar(void* pPixelData, COLOR_DATA_PRECISION ePrecision);

    void ResizeRow(DWORD lineIndex, DWORD targetWidth);
    void ResizeColumn(DWORD lineIndex, DWORD targetHeight);
    void InterpolatePixel(IPIXEL* p1, IPIXEL* p2, IPIXEL* pResult, double ratio);
    void ComputeRGB2YCBCRMatrix(COLOR_MODEL eModel, COLOR_RANGE eRange, COLOR_DATA_PRECISION ePrecision);
    void ConvertPixelToYCBCR(IPIXEL* pRGB, UINT16* pY, UINT16* pCb, UINT16* pCr);
    void ConvertPixelToYCBCR(IPIXEL* pRGB, UINT8* pY, UINT8* pCbCr);
    void ConvertPixelToYCBCR(IPIXEL* pRGB, UINT8* pY, UINT8* pCb, UINT8* pCr);

    void InitializeBackground(IPIXEL* pBackground);
    void BlendPixels(IPIXEL* pPix1, IPIXEL* pPix2, double alpha, IMAGE_METADATA* pMetadata1, IMAGE_METADATA* pMetadata2, IMAGE_METADATA* pOutMetadata);

    DWORD CreateBMPHeader(BMP_FILE_HEADER& hdr);
    BOOL IsmageHeaderValid();

    IPIXEL* ImageProc::GetPixelAtPos(DWORD x, DWORD y);

    UINT16 ConvertPixelRange(UINT16 data);
};


#endif// IMAGE_PROC_INCLUDED

