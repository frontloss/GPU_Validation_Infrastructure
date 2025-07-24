#pragma once

#include <iostream>
#include "StandardDef.h"
#include "ColorAlgo.h"

#define MAX_24_BIT_NUM ((double)16777215.0)

#define MAX_8BPC_PIXEL_VALUE 255.0
#define MAX_10BPC_PIXEL_VALUE 1023.0
#define MAX_16BPC_PIXEL_VALUE 65535.0
#define MAX_32BPC_PIXEL_VALUE 4294967295.0
#define ALPHA_OPAQUE MAX_32BPC_PIXEL_VALUE

#define MAX_32BPC_PIXEL_NUM 4294967296.0
#define MAX_16BPC_NUM 65536.0

#define NORMALIZE(Input, MaxValue) ((double(Input) / double(MaxValue)))
#define NORMALIZE_24BITValue(Input) (NORMALIZE(Input, ((1 << 24) - 1)))
#define NORMALIZE_32BITValue(Input) (NORMALIZE(Input, MAX_32BPC_PIXEL_VALUE))
#define NORMALIZE_16BITValue(Input) (NORMALIZE(Input, MAX_16BPC_PIXEL_VALUE))

#define MAX_FRAME_DIMENSION 8192
#define PARALLEL_PRTITION_SIZE 32

typedef enum
{
    PIXEL_FORMAT_UNKNOWN      = 0,
    PIXEL_FORMAT_YUY2         = 1,
    PIXEL_FORMAT_NV12         = 2,
    PIXEL_FORMAT_B8G8R8A8     = 3,
    PIXEL_FORMAT_R8G8B8A8     = 4,
    PIXEL_FORMAT_R16G16B16A16 = 5,
    PIXEL_FORMAT_R32G32B32A32 = 6,
    PIXEL_FORMAT_RGBA_DOUBLE  = 7,
} PIXEL_FORMAT;

typedef enum _HW_BLOCK_TYPE
{
    HW_BLOCK_TYPE_CSC = 0,
    HW_BLOCK_TYPE_LUT,
    HW_BLOCK_TYPE_3DLUT,
    HW_BLOCK_TYPE_NORMALIZER,
    HW_BLOCK_TYPE_CUS,
    HW_BLOCK_TYPE_BLENDER,
    HW_BLOCK_TYPE_PLANE,
    HW_BLOCK_TYPE_PIPE,
    HW_BLOCK_TYPE_GEN11_MULTI_SEGMENTED_LUT,
    HW_BLOCK_TYPE_LOG_LUT,
    HW_BLOCK_TYPE_TONE_MAPPER_SINGLE_SEGMENT_LUT,
    HW_BLOCK_TYPE_TONE_MAPPER_MULTI_SEGMENT_LUT,
    HW_BLOCK_TYPE_TONE_MAPPER_LOG_LUT,
    HW_BLOCK_TYPE_LACE,
    HW_BLOCK_TYPE_DPST,
    HW_BLOCK_TYPE_PIXEL_PROCESSOR, // Generic pixel processing block
    HW_BLOCK_TYPE_SCALER
} HW_BLOCK_TYPE;

typedef enum _COMPUTE_PRECISION
{
    COMPUTE_PRECISION_HW     = 0,
    COMPUTE_PRECISION_DOUBLE = 1,
    COMPUTE_PRECISION_FLOAT  = 2,
    COMPUTE_PRECISION_I32    = 3
} COMPUTE_PRECISION;

typedef enum _PIXEL_PROCESSOR_BLOCK_TYPE
{
    PIXEL_PROCESSOR_TYPE_SRGB_DEGAMMA = 0,
    PIXEL_PROCESSOR_TYPE_SRGB_GAMMA,
    PIXEL_PROCESSOR_TYPE_EOTF_2084,
    PIXEL_PROCESSOR_TYPE_OETF_2084,
    PIXEL_PROCESSOR_TYPE_CUSTOM
} PIXEL_PROCESSOR_BLOCK_TYPE;

//////////////////////////////////////////////////////////////////////////////////
//      LUT Specific structures - Begin
//////////////////////////////////////////////////////////////////////////////////

typedef enum _HW_BLOCK_LUT_TYPE
{
    HW_BLOCK_LUT_SINGLE_SEGMENT_LUT = 0,
    HW_BLOCK_LUT_SINGLE_SEGMENT_LUT_RGB,
    HW_BLOCK_LUT_MULTI_SEGMENT_LUT,
    HW_BLOCK_LUT_MULTI_SEGMENT_LUT_RGB,
    HW_BLOCK_LUT_LOG_LUT,
    HW_BLOCK_LUT_LOG_LUT_RGB,
    HW_BLOCK_LUT_TONE_MAPPING_SINGLE_SEGMENT,
    HW_BLOCK_LUT_TONE_MAPPING_TWO_SEGMENT,
    HW_BLOCK_LUT_TONE_MAPPING_LOG_LUT,
} HW_BLOCK_LUT_TYPE;

typedef struct _NORMALIZED_LUT
{
    DDU32             NumOfSamples;
    double *          pLutData;
    double            MaxValue;
    HW_BLOCK_LUT_TYPE LutType;
} NORMALIZED_LUT;

//////////////////////////////////////////////////////////////////////////////////
//      LUT Specific structures - End
//////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////
//      3DLUT Specific structures - Begin
//////////////////////////////////////////////////////////////////////////////////

typedef struct _HW_3DLUT_CONFIG
{
    DDU32             Depth;
    ColorB10G10R10X2 *pData;
    DDU32             MaxValue;
} HW_3DLUT_CONFIG;

typedef struct _NORMALIZED_3DLUT
{
    DDU32    Depth;
    IPIXELD *pData;
    double   MaxValue;
} NORMALIZED_3DLUT;

//////////////////////////////////////////////////////////////////////////////////
//      3DLUT Specific structures - End
//////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////
//      CSC Specific structures - Begin
//////////////////////////////////////////////////////////////////////////////////

typedef struct _CSC_CFG
{
    double PreOffsets[3];
    double PostOffsets[3];
    double Coefficients[9];
    double MaxValue;
} CSC_CFG;

//////////////////////////////////////////////////////////////////////////////////
//      CSC Specific structures - End
//////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////
//      General structures - Begin
//////////////////////////////////////////////////////////////////////////////////

typedef struct _TIME
{
    DDU32 Hour;
    DDU32 Minute;
    DDU32 Second;
    DDU32 MilliSecond;
} TIME;

//////////////////////////////////////////////////////////////////////////////////
//      General structures - End
//////////////////////////////////////////////////////////////////////////////////