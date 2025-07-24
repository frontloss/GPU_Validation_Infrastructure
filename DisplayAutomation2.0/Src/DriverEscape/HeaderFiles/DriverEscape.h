/*------------------------------------------------------------------------------------------------*
 *
 * @file     DriverEscape.h
 * @brief    This header file contains function definition for Internal API's.
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "CommonInclude.h"
#include "EscapeSharedHeader.h"

#define DD_VOID_PTR_INC(p, n) ((void *)((char *)(p) + (n)))

#define GDI32_LIB L"gdi32.dll"
#define PRODUCTIONESCAPEVERSION 0
#define MAJORESCAPECODE 20

#define CUI_ESC_MAX_PATHS 3
#define CUI_ESC_MAX_VIEWS 8

#define GFX_ESCAPE_DISPLAY_CONTROL 1L
#define ESCAPE_DISPLAY_CONTROL 1

#define YANGRA_ESC_GET_VERSION 100

#define BUFFER_SIZE 256
#define DD_ESC_QUERY_MODE_TABLE_MINOR 0
#define MAXCONNECTEDDISPLAYS 4
#define MAXMODELIST 10
// Constant used for calling Legacy Driver ESC
#define GFX_CONVERT_RR_RATIONAL 3
#define GFX_QUERY_CURRENT_CONFIG 21
#define GFX_QUERY_COMPENSATION 19

typedef enum _DD_MODE_TYPE
{
    DD_MODE_TYPE_UNKNOWN,
    DD_EDID_MODE,
    DD_NO_EDID_DEFAULT_MODE,
    DD_MEDIA_RR_MODE,
    DD_OS_ADDL_MODE,
    DD_JOINED_MODE,
#if 0
    DD_OEM_CUSTOM_MODE,     // OEM customizable modes
    DD_USER_STANDARD_CUSTOM_MODE, // Custom modes added through CUI's Standard Custom Mode page.
    DD_USER_DETAILED_CUSTOM_MODE // Custom modes added through CUI's Detailed Custom Mode page
#endif // 0
} DD_MODE_TYPE;

typedef enum _MSO_NUMLINKS
{
    NON_SEGMENTED  = 0,
    TWO_SST_LINKS  = 2,
    FOUR_SST_LINKS = 4
} MSO_NUMLINKS;

typedef enum _DD_PIXELFORMAT
{
    // IF ANY NEW FORMAT IS ADDED HERE, PLEASE UPDATE ALL THE BELOW MACORS.
    DD_8BPP_INDEXED = 0,
    DD_B5G6R5X0,
    DD_B8G8R8X8,
    DD_R8G8B8X8,
    DD_B10G10R10X2,
    DD_R10G10B10X2,
    DD_R10G10B10X2_XR_BIAS,
    DD_R16G16B16X16F,
    DD_YUV422,
    DD_YUV444_8,
    DD_YUV444_10,
    DD_NV12YUV420,
    DD_P010YUV420,
    DD_P012YUV420,
    DD_P016YUV420,
    DD_MAX_PIXELFORMAT
    // IF ANY NEW FORMAT IS ADDED HERE, PLEASE UPDATE ALL THE BELOW MACORS.
} DD_PIXELFORMAT;

typedef enum _MODE_INFO_TYPE
{
    MODE_NOT_PINNED = 0,
    MODE_PINNED,                // User selected mode, try not to modify
    MODE_LIST_NUM_ONLY_QUERIED, // How many number of modes there? required to allocate buffer for mode list query
    MODE_LIST_DETAILS_QUERIED,  // Give the mode list for this path (only 1 path can have this set in Topology)
    MODE_INFO_SCALING_QUERIED,
    MODE_INFO_ROTATION_QUERIED,
    MODE_INFO_PREF_MODE_QUERIED,
    MODE_INFO_UPDATE_NUM_MODES,
    MODE_INFO_UPDATE_DETAILS_MODES,
    MAX_MODE_INFO_TYPE = 9
} MODE_INFO_TYPE;

typedef struct _RR_RATIONAL_INFO
{
    _Out_ ULONG hActive;                     // Hactive value
    _Out_ ULONG vActive;                     // VActive value
    _Out_ ULONG hSyncNumerator;              // Hsync numerator value
    _Out_ ULONG hSyncDenominator;            // Hsync denominator value
    _Out_ ULONG pixelRate;                   // pixel rate value
    _Out_ ULONG hTotal;                      // Htotal value
    _Out_ ULONG vTotal;                      // Vtotal value
    _Out_ DD_SIGNAL_STANDARD signalStandard; // signal standard
    _Out_ ULONG vSyncNumerator;              // Vsync numerator value
    _Out_ ULONG vSyncDenominator;            // Vsync denominator value
} RR_RATIONAL_INFO, *PRR_RATIONAL_INFO;

typedef union _DD_BPC_SUPPORTED {
    DDU16 ColorDepthMask;
    struct
    {
        DDU16 SupportsRGB565Color : 1;
        DDU16 Supports6BitsPerColor : 1;
        DDU16 Supports6BitsLooselyPackedColor : 1;
        DDU16 Supports8BitsPerColor : 1;
        DDU16 Supports10BitsPerColor : 1;
        DDU16 Supports12BitsPerColor : 1;
        DDU16 Supports14BitsPerColor : 1;
        DDU16 Supports16BitsPerColor : 1;
        DDU16 SupportsCompressedBits : 1;
        DDU16 ColordepthReserved : 7;
    };
} DD_BPC_SUPPORTED;

typedef union _DD_SOURCE_MODE_ID {
    DDU32 Value;
    struct
    {
        DD_PIXELFORMAT PixelFormat : 8; // Pixel format range is (0-31) so should not exceed 5 bits.
        DDU32          TgtUniqueIndex : 8;
        DDU32          Index : 16;
    };
} DD_SOURCE_MODE_ID;

CDLL_EXPORT DRIVER_TYPE GetDriverType(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName);
CDLL_EXPORT BOOLEAN GetGfxAdapterInfo(_In_ UINT32 sourceID, _Inout_ ADAPTER_INFO_GDI_NAME *pInternalAdapterInfo);
CDLL_EXPORT BOOLEAN GetAdapterDetails(_Inout_ ADAPTER_INFO_GDI_NAME *pInternalAdapterInfo);
CDLL_EXPORT BOOLEAN TdrDriverEscape(_In_ ADAPTER_INFO_GDI_NAME *pAdapterInfoGdiName, _In_ BOOLEAN displayTdr);
CDLL_EXPORT BOOLEAN InvokeDriverEscape(_In_ ADAPTER_INFO_GDI_NAME *pAdapterInfoGdiName, _In_ INT escapeDataSize, _In_ GFX_ESCAPE_HEADER_T escapeOpCode, _Out_ void *pEscapeData);
