/*------------------------------------------------------------------------------------------------*
 *
 * @file  EscapeSharedHeader.h
 * @brief This file contains Implementation of commonly used identifiers and Macros
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "Windows.h"
#include "d3dkmthk.h"
#include "..\..\Logger\log.h"
#define GDI32_LIB L"gdi32.dll"

#define LEGACY_ESC_VERSION 2
#define LEGACY_ESC_FILE_VERSION 2

#define YANGRA_ESC_VERSION 1
#define YANGRA_ESC_FILE_VERSION 2

#define MAX_LUT_AUX_BUFSIZE 0x0200

#define MAX_LINK_COUNT 15
#define MAX_BYTES_RAD ((MAX_LINK_COUNT) / 2)

#define TARGET_ID_MASK 0x00FFFFFF
/* Macro to Unmask windows target id if OS is Win 10 or above we are masking windows target id
 *  since win 10 onwords though driver reports 24 bit target id, OS enumerate as 28 bit target id. */
#define UNMASK_TARGET_ID(a) (a & TARGET_ID_MASK)

typedef UCHAR  DDU8;  // unsigned 8 bit data type
typedef USHORT DDU16; // unsigned 16 bit data type
typedef ULONG  DDU32; // unsigned 32 bit data type
typedef INT    DDS32;

#define VERIFY_ESCAPE_STATUS(status)           \
    {                                          \
        if (FALSE == status)                   \
        {                                      \
            ERROR_LOG("Escape called Failed"); \
            return FALSE;                      \
        }                                      \
    }

#define NULL_PTR_CHECK(ptr)                         \
    {                                               \
        if (NULL == ptr)                            \
        {                                           \
            ERROR_LOG("NULL Pointer, Exiting !!!"); \
            return FALSE;                           \
        }                                           \
    }

#define VERIFY_DRIVER_TYPE(type)                                 \
    {                                                            \
        if (DRIVER_UNKNOWN == type)                              \
        {                                                        \
            ERROR_LOG("Invalid Driver Type Found, Exiting !!!"); \
            return FALSE;                                        \
        }                                                        \
    }

typedef enum _GFX_ESCAPE_CODE_T
{
    GFX_ESCAPE_CODE_DEBUG_CONTROL = 0L,
    GFX_ESCAPE_DISPLAY_CONTROL,
    GFX_ESCAPE_TOOLS_CONTROL = 20,
    GFX_ESCAPE_MISC          = 106
} GFX_ESCAPE_CODE_T;

typedef enum _DRIVER_TYPE
{
    DRIVER_UNKNOWN = 0,
    LEGACY_DRIVER  = 1,
    YANGRA_DRIVER  = 2
} DRIVER_TYPE;

typedef enum _DD_SIGNAL_STANDARD
{
    DD_SIGNAL_UNKNOWN = 0,
    DD_VESA_DMT       = 1,
    DD_VESA_GTF       = 2,
    DD_VESA_CVT       = 3,
    DD_CEA_861B,
} DD_SIGNAL_STANDARD;

// Structure requried for sending request details and data
typedef struct _GFX_ESCAPE_HEADER_T
{
    UINT              reserved;
    USHORT            majorInterfaceVersion;
    USHORT            minorInterfaceVersion;
    GFX_ESCAPE_CODE_T majorEscapeCode;
    UINT              minorEscapeCode;
} GFX_ESCAPE_HEADER_T;

typedef struct _D3DKMT_ESCAPE_ARGS
{
    HMODULE                       gdi32handle;
    PFND3DKMT_OPENADAPTERFROMLUID pfnOpenAdapterFromLuid;
    PFND3DKMT_ESCAPE              pfnD3DKmtEscape;
    PFND3DKMT_CLOSEADAPTER        pfnCloseAdapter;
} D3DKMT_ESCAPE_ARGS;

typedef struct _GFX_INFO
{
    LUID  adapterID;
    DWORD targetID;
    DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY outputTechnology;
} GFX_INFO;

typedef struct _GFX_INFO_ARR
{
    LONG     count;
    GFX_INFO arr[50];
} GFX_INFO_ARR;
