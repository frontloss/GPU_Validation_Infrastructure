/*===========================================================================
;
;   Copyright (c) Intel Corporation (2017)
;
;   INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
;   ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
;   INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
;   ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
;   MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
;   OTHER WARRANTY.  Intel disclaims all liability, including liability for
;   infringement of any proprietary rights, relating to use of the code. No license,
;   express or implied, by estoppel or otherwise, to any intellectual property
;   rights is granted herein.
;
;--------------------------------------------------------------------------*/

/**
********************************************************************
*
* @file DisplayDefs.h
*
* @brief Defines all basic types used inside display
*
*********************************************************************
**/

#ifndef _DD_DEF_
#define _DD_DEF_

#ifdef _WIN32
///////////////////////////////////////////////////////////////////////////////
//
// Windows definitions
//

#ifdef _DISPLAY_
#ifndef _DISP_UTF_
#include <ntdef.h>
#endif
#endif
//-----------------------------------------------------------------------------
// basic data types
//

// arg types
#define DD_IN IN
#define DD_OUT OUT
#define DD_IN_OUT

//
// typedef DDU8 DDBOOL; // DD_FALSE = 0, DD_TRUE = 1
// typedef void void;

typedef CHAR    DDS8;   // signed 8 bit data type
typedef UCHAR   DDU8;   // unsigned 8 bit data type
typedef SHORT   DDS16;  // signed 16 bit data type
typedef USHORT  DDU16;  // unsigned 16 bit data type
typedef LONG    DDS32;  // signed 32 bit data type
typedef ULONG   DDU32;  // unsigned 32 bit data type
typedef LONG64  DDS64;  // signed 64 bit data type
typedef ULONG64 DDU64;  // unsigned 64 bit data type
typedef WCHAR   DDWSTR; // Wide string character
// typedef UCHAR BYTE;

typedef ULONG_PTR DDU64_PTR;

// for strings
typedef CHAR *       PDDSTR;
typedef WCHAR *      PDDWSTR;
typedef const CHAR * PDDCSTR;
typedef const WCHAR *PDDCWSTR;

// data type value range limits
#define DDMINS8 MINCHAR
#define DDMAXS8 MAXCHAR
#define DDMINS16 MINSHORT
#define DDMAXS16 MAXSHORT
#define DDMINS32 MINLONG
#define DDMAXS32 MAXLONG
#define DDMAXU8 MAXUCHAR
#define DDMAXU16 MAXUSHORT
#define DDMAXU32 MAXULONG
#define DDMAXU64_PTR MAXULONG_PTR

#define MAX_8BIT_VALUE 255.0f
#define MAX_8BIT_NUM 256
#define MAX_16BIT_NUM 65536
#define MAX_16BIT_VALUE 65535.0f
#define MAX_24BIT_NUM 16777216
#define MAX_24BIT_VALUE 16777215
#define GAMMA_UNITY 16777216 // 1<<24

#define MAX_RELATIVE_LUT_VALUE MAX_24BIT_VALUE // this is assuming all correction LUTs are 8.24 format
#define MAX_PARS_POSSIBLE_WITH_1_VIC 2

#define CONVERT_16BIT_TO_8_24BIT(InputIn16Bit) ((DDU32)((((double)InputIn16Bit) / MAX_16BIT_VALUE) * MAX_24BIT_NUM))
#define CONVERT_8_24BIT_TO_3_16BIT(InputIn32Bit) (DD_MIN(InputIn32Bit, GAMMA_UNITY) >> 8)     // HW format 3.16 i.e 512,513 and 514
#define CONVERT_8_24BIT_TO_0_16BIT(InputIn32Bit) (DD_MIN(InputIn32Bit, GAMMA_UNITY - 1) >> 8) // HW format 0.16 i.e 0 to 511 entries

//#define USE_DELTAE_2000

#define CLIPVALUE(value, lower, higher) ((value < lower) ? lower : ((value > higher) ? higher : value))

#define TWOS_TO_SIGNED_MAGNITUDE(a) (a < 0) ? (~a + 1) : a // for -ve cursor positions compute 2's complement to get the +ve offset and then set the signed bit for HW
#define TWOS_TO_SIGNED_SIGN(a) (a < 0) ? 1 : 0             // for -ve cursor positions compute 2's complement to get the +ve offset and then set the signed bit for HW
//-----------------------------------------------------------------------------
// Function declaration related
//

// inline func macro
#define DD_INLINE __inline
#define DD_S_INLINE static __inline

///////////////////////////////////////////////////////////////////////////////
#else // ! _WIN32
// TODO:  add defn for other OS env

#endif // #ifdef _WIN32

///////////////////////////////////////////////////////////////////////////////
//
// Common user defined data types
//
///////////////////////////////////////////////////////////////////////////////

#define DD_IS_NULL(pArg) (NULL == (void *)pArg)
#define DD_IS_NOT_NULL(pArg) (NULL != (void *)pArg)

typedef enum _DD_REQUEST
{
    DD_REQUEST_UNKNOWN = 0,
    DD_REQUEST_GET,
    DD_REQUEST_SET,
} DD_REQUEST;

typedef enum _DD_ENABLE_DISABLE
{
    DD_ACTION_UNKNOWN = 0,
    DD_ENABLE,
    DD_DISABLE
} DD_ENABLE_DISABLE;

typedef union _DD_LARGE_INTEGER {
    struct
    {
        DDU32 LowPart;
        DDS32 HighPart;
    };
    DDS64 QuadPart;
} DD_LARGE_INTEGER;

// ========================================================
//  Timer related struct
// ========================================================

// Structure used to measure time delatas
typedef struct _DD_ELAPSED_TIME
{
    DDU32 StartTime;
    DDU32 ElapsedTime;
} DD_ELAPSED_TIME;

typedef enum _DD_TIMER_TYPE
{
    NOTIFICATION,
    SYNCHRONIZATION
} DD_TIMER_TYPE;

typedef struct _DD_PERIODIC_TIMER_OBJECT
{
    void *pKDPC;
    void *pKTIMER;
} DD_PERIODIC_TIMER_OBJECT;

///////////////////////////////////////////////////////////////////////////////

#ifdef _DISPLAY_INTERNAL_ // ndef BIT0 // reusing SB defn

///////////////////////////////////////////////////////////////////////////////
//
// Bit definition
// Bit manipulation macros
//
///////////////////////////////////////////////////////////////////////////////
#define __BIT(x) (1UL << (x)) // internal to this file
#define BIT64(x) ((UINT64)1 << (x))

#define BIT0 __BIT(0)
#define BIT1 __BIT(1)
#define BIT2 __BIT(2)
#define BIT3 __BIT(3)
#define BIT4 __BIT(4)
#define BIT5 __BIT(5)
#define BIT6 __BIT(6)
#define BIT7 __BIT(7)
#define BIT8 __BIT(8)
#define BIT9 __BIT(9)
#define BIT10 __BIT(10)
#define BIT11 __BIT(11)
#define BIT12 __BIT(12)
#define BIT13 __BIT(13)
#define BIT14 __BIT(14)
#define BIT15 __BIT(15)
#define BIT16 __BIT(16)
#define BIT17 __BIT(17)
#define BIT18 __BIT(18)
#define BIT19 __BIT(19)
#define BIT20 __BIT(20)
#define BIT21 __BIT(21)
#define BIT22 __BIT(22)
#define BIT23 __BIT(23)
#define BIT24 __BIT(24)
#define BIT25 __BIT(25)
#define BIT26 __BIT(26)
#define BIT27 __BIT(27)
#define BIT28 __BIT(28)
#define BIT29 __BIT(29)
#define BIT30 __BIT(30)
#define BIT31 __BIT(31)
#endif // _DISPLAY_INTERNAL_

#ifndef UNIQUENAME                          // reusing SB defn
#define __RESERVED2(x, y) x##y              // defn. internal to this file
#define __RESERVED1(x, y) __RESERVED2(x, y) // defn. internal to this file
#define __RANDOMNUMBER __LINE__             // __COUNTER__   // defn. internal to this file
#define UNIQUENAME(ValueName) __RESERVED1(ValueName, __RANDOMNUMBER)
#endif // UNIQUENAME

//-----------------------------------------------------------------------------
// Macro  to generate set of 1's given
// a range
// Bit mask
//-----------------------------------------------------------------------------
#define DD_BITRANGE_MASK(ulHighBit, ulLowBit) ((((DDU32)(1 << ulHighBit) - 1) | (1 << ulHighBit)) & (~((DDU32)(1 << ulLowBit) - 1)))

//-----------------------------------------------------------------------------
// Macro: DD_BITFIELD_RANGE
// PURPOSE: Calculates the number of bits between the startbit and the endbit
// and count is inclusive of both bits. The bits are 0 based.
//-----------------------------------------------------------------------------
#define DD_BITFIELD_RANGE(ulLowBit, ulHighBit) ((ulHighBit) - (ulLowBit) + 1)

//-----------------------------------------------------------------------------
// Macro: DD_BITFIELD_BIT
// PURPOSE: Used to declare single bit width
//-----------------------------------------------------------------------------
#define DD_BITFIELD_BIT(bit) 1

// size in multiple of DDU32
#define DD_SIZE32(x) ((DDU32)(sizeof(x) / sizeof(DDU32)))

#define DD_IS_ALIGN(A, B) (((A) % (B)) == 0)

#define DD_SET_BIT(A, b) (A |= __BIT(b))
#define DD_CLEAR_BIT(A, b) (A &= ~__BIT(b))
#define DD_IS_BIT_SET(A, b) (A & __BIT(b))
#define DD_IS_BIT_CLEAR(A, b) ((A & __BIT(b)) == 0)
#define DD_IS_EVEN(A) DD_IS_BIT_CLEAR(A, 0)
#define DD_IS_ODD(A) DD_IS_BIT_SET(A, 0)
#define DD_IS_MASK_SET(A, mask) ((A & mask) == mask)
#define DD_IS_MASK_CLEAR(A, mask)  ((((DDU32)A) | ~((DDU32)mask)) == ~((DDU32)mask)))

#define DD_ROUND_TO_4K(LENGTH) (((DDU32)(LENGTH) + 0x1000 - 1) & ~(0x1000 - 1))
#define DD_DIVIDE_BY_4K(Value) ((Value) >> 12)
#define DD_MULT_BY_4K(Value) ((Value) << 12)
#define DD_IS_4K_ALIGNED(Value) ((Value & 0xfffff000) == Value)

// Macros for quick use
#define DD_GET_BYTE(dwValue, nStartPos) ((dwValue >> nStartPos) & 0xFF)
// This macro will convert between little/big endian
#define DD_SWAP_ENDIAN(dwValue) ((DD_GET_BYTE(dwValue, 0) << 24) | (DD_GET_BYTE(dwValue, 8) << 16) | (DD_GET_BYTE(dwValue, 16) << 8) | (DD_GET_BYTE(dwValue, 24)))
#define DD_VOID_PTR_INC(p, n) ((void *)((char *)(p) + (n)))
#define DD_VOID_PTR_DEC(p, n) ((void *)((char *)(p) - (n)))
#define DD_OFFSETOF(str, memVar) (DDU64_PTR) & (((str *)0)->memVar) // Macro to get relative offset of a member variable in a stucture
#define DD_CONTAINING_RECORD(address, type, field) ((type *)((DDU8 *)(address) - (DDU64_PTR)(&((type *)0)->field)))
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
//
// All standard macros for primitive operations go here:
//
///////////////////////////////////////////////////////////////////////////////

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

/**
Macro to get twos compliment of a DDU16 variable.
**/
#define DD_TWOS_COMPLEMENT(x) (DDU8)((~(x) + 1) & 0x3F)

/**
Macro to swap two bytes of a DDU16 variable.
**/
#define DD_DDU16_SWAP_ENDIAN(Value) ((DD_GET_BYTE(Value, 0) << 8) | (DD_GET_BYTE(Value, 8)))

// Required for CVT Timing Calculation
#define DD_ROUNDTO3DECIMALS(z) (float)(DD_ROUNDTONEARESTINT((z)*1000)) / 1000
#define DD_CHECK_ASPECTRATIO(x, CellGran, Vpixels) (DDU32)(CellGran * ((DDU32)((Vpixels * x)) / CellGran))

#define DD_ALIGN(x, a) (((x) + ((a)-1)) - (((x) + ((a)-1)) & ((a)-1))) // Alt implementation
// with bitwise not (~) has issue with uint32 align used with 64-bit value, since ~'ed value will remain 32-bit.

//-----------------------------------------------------------------------------
// unit conversion macros
//-----------------------------------------------------------------------------
#define DD_KILO(a) ((a)*1024)
#define DD_MEGA(a) ((a)*1024 * 1024)
#define DD_GIGA(a) (((DDU64)1024) * 1024 * 1024 * (a))

// Macros added for TEN and Mega
// Didnt use the name MEGA for the second macro since its already defined in CSLBase.c with value 1048576
#define TEN 10
#define MEGA_HERTZ 1000000

//-----------------------------------------------------------------------------
// Precision related macros
//-----------------------------------------------------------------------------
#define DD_PRECISION2DEC 100   // multiply the floating point no to get 2 places after decimal
#define DD_PRECISION3DEC 1000  // multiply the floating point no to get 3 places after decimal
#define DD_PRECISION4DEC 10000 // multiply the floating point no to get 4 places after decimal

//-----------------------------------------------------------------------------
// Time related macros
//-----------------------------------------------------------------------------
#define DD_SEC_TO_MILLI_SEC 1000    // Milli seconds in a Second
#define DD_MILLI_TO_MICRO_SEC 1000  // Micro seconds in a milli Second
#define DD_MICRO_TO_100_NANO_SEC 10 // 100 Nano seconds in a micro Second

#define DD_MS_TO_HUNDRED_NS(n) (10 * 1000 * (n))         // Convert from ms to 100ns units
#define DD_S_TO_HUNDRED_NS(n) (10 * 1000 * 1000 * (n))   // Convert from sec to 100ns unit
#define DD_HUNDRED_NS_TO_S(n) ((n) / (10 * 1000 * 1000)) // Convert from 100ns units to s
// Memory operations

// memcpy_s source to destination
// copy count bytes from src to dest if destsize is less than count
#define DD_MEM_COPY_SAFE(dest, destsize, src, count) memcpy_s((dest), (destsize), (src), (count))

// Zero out dest memory
#define DD_ZERO_MEM(dest, size) memset(dest, 0, size)

#define DD_CENT 100
#define DD_1K 1000
#define DD_MILLION 1000000 // Multiply by 10^6 to conver to Parts Per Million

#define STRING2(x) #x
#define DD_STRINGIFY(x) STRING2(x)

///////////////////////////////////////////////////////////////////////////////
//
// inline functions
//
DD_S_INLINE DDU32 DDPtrToUlong(const void *p)
{
    return ((DDU32)(DDU64_PTR)p);
}

DD_INLINE DDU32 DD_FindGCD(DDU32 ulNumber1, DDU32 ulNumber2)
{
    DDU32 ulLargerNumber, ulSmallerNumber = 0, ulRemainder = 0;

    if (ulNumber1 > ulNumber2)
    {
        ulLargerNumber  = ulNumber1;
        ulSmallerNumber = ulNumber2;
    }
    else
    {
        ulLargerNumber  = ulNumber2;
        ulSmallerNumber = ulNumber1;
    }

    while (1)
    {
        if (ulSmallerNumber == 0)
            break; // We have got the LCD

        ulRemainder     = ulLargerNumber % ulSmallerNumber;
        ulLargerNumber  = ulSmallerNumber;
        ulSmallerNumber = ulRemainder;
    }

    return ulLargerNumber;
}

///////////////////////////////////////////////////////////////////////////////
#ifdef _DISPLAY_
#ifdef _STDBOOL
#undef bool
#undef false
#undef true
#endif // _STDBOOL

#endif // _DISPLAY_

#endif // _DD_DEF_
