#pragma once

#include <windows.h>
#include <cstdint>
#include <stdio.h>
#include <xmmintrin.h>
#include <immintrin.h>

#define _USE_SIMD
//#define _USE_DXVA

typedef INT32         DDI32;
typedef int8_t        DDS8;   // signed 8 bit data type
typedef uint8_t       DDU8;   // unsigned 8 bit data type
typedef int16_t       DDS16;  // signed 16 bit data type
typedef uint16_t      DDU16;  // unsigned 16 bit data type
typedef int32_t       DDS32;  // signed 32 bit data type
typedef uint32_t      DDU32;  // unsigned 32 bit data type
typedef int64_t       DDS64;  // signed 64 bit data type
typedef uint64_t      DDU64;  // unsigned 64 bit data type
typedef wchar_t       WCHAR;  // Wide string character
typedef wchar_t       DDWSTR; // Wide string character
typedef char          CHAR;
typedef unsigned char DD_BOOL;

#define DDASSERT
#define DDS_UNSUCCESSFUL -1
#define DDS_SUCCESS 0

#define UNITY_VAL_IN_8_24_FORMAT 16777216
#define FINAL_SLOPE_TM_CURVE 503316 // 0.03 * UNITY_VAL_IN_8_24_FORMAT
#define VALUE_AT_UNITY_SLOPE 167772 // 0.01 * VALUE_AT_UNITY_SLOPE
#define VALUE_AT_INFLECTION_POINT1

#define MAX_8BIT_NUM 255
#define MAX_8BIT_VALUE 255.0
#define MAX_10BIT_NUM 1023
#define MAX_10BIT_VALUE 1023.0
#define MAX_16BIT_NUM 65535
#define MAX_16BIT_VALUE 65535.0
#define MAX_24BIT_NUM 16777216
#define MAX_24BIT_VALUE 16777215.0
#define MAX_32BIT_NUM 4294967295
#define MAX_32BIT_VALUE 4294967295.0

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

typedef struct
{
    DDU64 timeConsumed;
    DDU64 nIterations;
    BOOL  bIsNano; // Time is in nano sec if this flag is true. Otherwise time is in micro sec
    DDU8  funcName[64];
} PROFILE_DATA;

#define ZERO_MEM(dst, sizeInBytes) (memset(dst, 0, sizeof(sizeInBytes)))

extern unsigned __int64 GetTimeInMicroSec();
extern unsigned __int64 GetTimeInNanoSec();

__inline void LogProfileInfo(PROFILE_DATA *pProfileData, DDU32 nEntries, FILE *pLogFile)
{
    if (!pLogFile)
        return;

    for (DDU32 i = 0; i < nEntries; i++)
    {
        if (pProfileData[i].nIterations)
        {
            DDU64 averageTime = (pProfileData[i].timeConsumed) / pProfileData[i].nIterations;

            if (!pProfileData[i].bIsNano)
            {
                fprintf(pLogFile, "%s: Number of iterations: %I64d, Average time: %I64d uS\n", pProfileData[i].funcName, pProfileData[i].nIterations, averageTime);
            }
            else
            {
                fprintf(pLogFile, "%s: Number of iterations: %I64d, Average time: %I64d nS\n", pProfileData[i].funcName, pProfileData[i].nIterations, averageTime);
            }
        }
    }
}
