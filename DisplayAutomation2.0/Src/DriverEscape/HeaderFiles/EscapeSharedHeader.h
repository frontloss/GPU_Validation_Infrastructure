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
#include "..\Logger\log.h"
#define GDI32_LIB L"gdi32.dll"

#define LEGACY_ESC_VERSION 2
#define LEGACY_ESC_FILE_VERSION 2

#define YANGRA_ESC_VERSION 1
#define YANGRA_ESC_FILE_VERSION 2
#define TOOLS_ESC_VERSION 0

#define STRING_MAX_SIZE 256

#define MAX_EDID_BLOCK 8
#define EDID_BLOCK_SIZE 128
#define EXTENSIONS_BYTE 126
#define WB_EDID_BLOCK_SIZE (256)

#define MAX_LINK_COUNT 15
#define MAX_BYTES_RAD ((MAX_LINK_COUNT) / 2)

#define MAX_LUT_AUX_BUFSIZE 0x0200
#define GBD_DATA_SIZE 28

typedef UCHAR  DDU8;  // unsigned 8 bit data type
typedef USHORT DDU16; // unsigned 16 bit data type
typedef ULONG  DDU32; // unsigned 32 bit data type
typedef unsigned long long DDU64; // unsigned 64 bit data type
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

#define VERIFY_IGFX_ADAPTER(adapterInfo)                                                                                                                 \
    {                                                                                                                                                    \
        if ((0 != wcscmp(adapterInfo.vendorID, INTEL_ADAPTER)) || (0 == wcslen(adapterInfo.busDeviceID)) || (0 == wcslen(adapterInfo.deviceInstanceID))) \
        {                                                                                                                                                \
            ERROR_LOG("Invalid Adapter Details Provided, Exiting !!!");                                                                                  \
            return FALSE;                                                                                                                                \
        }                                                                                                                                                \
    }

#define VERIFY_IGFX_ADAPTER_STATUS(status)                                 \
    {                                                                      \
        if (FALSE == status)                                               \
        {                                                                  \
            ERROR_LOG("Failed to Get Adapter GdiDeviceName, Exiting !!!"); \
            return FALSE;                                                  \
        }                                                                  \
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

typedef enum _MISC_ESC_OP_CODE
{
    MISC_ESC_REGISTRY_RW = 0,
    MISC_ESC_GET_SYSTEM_INFO,
    MISC_ESC_CONFIG_DXGK_POWER_COMPONENT,
    MISC_ESC_MAX
} MISC_ESC_OP_CODE;

typedef enum _MISC_ESC_PRODUCT_FAMILY
{
    MISC_ESC_IGFX_UNKNOWN = 0,
    MISC_ESC_IGFX_GRANTSDALE_G,
    MISC_ESC_IGFX_ALVISO_G,
    MISC_ESC_IGFX_LAKEPORT_G,
    MISC_ESC_IGFX_CALISTOGA_G,
    MISC_ESC_IGFX_BROADWATER_G,
    MISC_ESC_IGFX_CRESTLINE_G,
    MISC_ESC_IGFX_BEARLAKE_G,
    MISC_ESC_IGFX_CANTIGA_G,
    MISC_ESC_IGFX_CEDARVIEW_G,
    MISC_ESC_IGFX_EAGLELAKE_G,
    MISC_ESC_IGFX_IRONLAKE_G,
    MISC_ESC_IGFX_GT,
    MISC_ESC_IGFX_IVYBRIDGE,
    MISC_ESC_IGFX_HASWELL,
    MISC_ESC_IGFX_VALLEYVIEW,
    MISC_ESC_IGFX_BROADWELL,
    MISC_ESC_IGFX_CHERRYVIEW,
    MISC_ESC_IGFX_SKYLAKE,
    MISC_ESC_IGFX_KABYLAKE,
    MISC_ESC_IGFX_COFFEELAKE,
    MISC_ESC_IGFX_WILLOWVIEW,
    MISC_ESC_IGFX_BROXTON,
    MISC_ESC_IGFX_GEMINILAKE,
    MISC_ESC_IGFX_GLENVIEW,
    MISC_ESC_IGFX_GOLDWATERLAKE,
    MISC_ESC_IGFX_CANNONLAKE,
    MISC_ESC_IGFX_CNX_G,
    MISC_ESC_IGFX_ICELAKE,
    MISC_ESC_IGFX_ICELAKE_LP,
    MISC_ESC_IGFX_LAKEFIELD,
    MISC_ESC_IGFX_JASPERLAKE,
    MISC_ESC_IGFX_TIGERLAKE_LP,
    MISC_ESC_IGFX_TIGERLAKE_HP,
    MISC_ESC_IGFX_RYEFIELD,
    MISC_ESC_IGFX_DG1,
    MISC_ESC_IGFX_ROCKETLAKE,
    MISC_ESC_IGFX_DG2,
    MISC_ESC_IGFX_LAKEFILED_R,
    MISC_ESC_IGFX_ALDERLAKE_S,
    MISC_ESC_IGFX_ALDERLAKE_UH,
    MISC_ESC_IGFX_MAX_PRODUCT,

    MISC_ESC_IGFX_GENNEXT               = 0x7ffffffe,
    MISC_ESC_PRODUCT_FAMILY_FORCE_ULONG = 0x7fffffff
} MISC_ESC_PRODUCT_FAMILY;

typedef enum _MISC_ESC_PLATFORM_TYPE
{
    MISC_ESC_PLATFORM_NONE    = 0x00,
    MISC_ESC_PLATFORM_DESKTOP = 0x01,
    MISC_ESC_PLATFORM_MOBILE  = 0x02,
    MISC_ESC_PLATFORM_TABLET  = 0X03,
    MISC_ESC_PLATFORM_ALL     = 0xff,
} MISC_ESC_PLATFORM_TYPE;

typedef enum __MISC_ESC_CPUTYPE
{
    MISC_ESC_CPU_UNDEFINED = 0x0,
    MISC_ESC_CPU_CORE_I3,
    MISC_ESC_CPU_CORE_I5,
    MISC_ESC_CPU_CORE_I7,
    MISC_ESC_CPU_PENTIUM,
    MISC_ESC_CPU_CELERON,
    MISC_ESC_CPU_CORE,
    MISC_ESC_CPU_VPRO,
    MISC_ESC_CPU_SUPER_SKU,
    MISC_ESC_CPU_ATOM,
    MISC_ESC_CPU_CORE1,
    MISC_ESC_CPU_CORE2,
    MISC_ESC_CPU_WS,
    MISC_ESC_CPU_SERVER,
    MISC_ESC_CPU_CORE_I5_I7,
    MISC_ESC_CPU_COREX1_4,
    MISC_ESC_CPU_ULX_PENTIUM,
    MISC_ESC_CPU_MB_WORKSTATION,
    MISC_ESC_CPU_DT_WORKSTATION,
    MISC_ESC_CPU_M3,
    MISC_ESC_CPU_M5,
    MISC_ESC_CPU_M7,
    MISC_ESC_CPU_MEDIA_SERVER // Added for KBL
} MISC_ESC_CPUTYPE,
*PMISC_ESC_CPUTYPE;

typedef enum __MISC_ESC_GTTYPE
{
    MISC_ESC_GTTYPE_GT1 = 0x0,
    MISC_ESC_GTTYPE_GT2,
    MISC_ESC_GTTYPE_GT2_FUSED_TO_GT1,
    MISC_ESC_GTTYPE_GT2_FUSED_TO_GT1_6, // IVB
    MISC_ESC_GTTYPE_GTL,                // HSW
    MISC_ESC_GTTYPE_GTM,                // HSW
    MISC_ESC_GTTYPE_GTH,                // HSW
    MISC_ESC_GTTYPE_GT1_5,              // HSW
    MISC_ESC_GTTYPE_GT1_75,             // HSW
    MISC_ESC_GTTYPE_GT3,                // BDW
    MISC_ESC_GTTYPE_GT4,                // BDW
    MISC_ESC_GTTYPE_GT0,                // BDW
    MISC_ESC_GTTYPE_GTA,                // BXT
    MISC_ESC_GTTYPE_GTC,                // BXT
    MISC_ESC_GTTYPE_GTX,                // BXT
    MISC_ESC_GTTYPE_GT2_5,              // CNL
    MISC_ESC_GTTYPE_GT3_5,              // SKL
    MISC_ESC_GTTYPE_GT0_5,              // CNL
    MISC_ESC_GTTYPE_UNDEFINED,          // Always at the end.
} MISC_ESC_GTTYPE,
*PMISC_ESC_GTTYPE;

typedef enum _DD_SIGNAL_STANDARD
{
    DD_SIGNAL_UNKNOWN = 0,
    DD_VESA_DMT       = 1,
    DD_VESA_GTF       = 2,
    DD_VESA_CVT       = 3,
    DD_CEA_861B,
} DD_SIGNAL_STANDARD;

typedef enum CUI_ESC_OPERATION_TYPE_ENUM
{
    CUI_ESC_COLORSPACE_OPTYPE_UNKNOWN = 0,     // Invalid operation type
    CUI_ESC_COLORSPACE_OPTYPE_GET,             // Get
    CUI_ESC_COLORSPACE_OPTYPE_SET,             // Set
    CUI_ESC_COLORSPACE_OPTYPE_SET_PERSISTENCE, // Set Persistence
    CUI_ESC_NUM_OF_CUI_OPTYPE
} CUI_ESC_OPERATION_TYPE;

typedef enum _CUI_ESC_COLORSPACE_SUPPORTED
{
    CUI_ESC_SUPPORTS_COLORSPACE_NONE = 0, // Both xvycc and ycbcr not supported
    CUI_ESC_SUPPORTS_COLORSPACE_YCbCr,
    CUI_ESC_SUPPORTS_COLORSPACE_xvYCC
} CUI_ESC_COLORSPACE_SUPPORTED,
*PCUI_ESC_COLORSPACE_SUPPORTED;

typedef enum _IGCC_SUPPORTED_OUTPUT_ENCODING
{
    ENCNOTSUPPORTED = 0,
    ENCDEFAULT      = 1,
    RGB             = 2,
    YCBCR420        = 4,
    YCBCR422        = 8,
    YCBCR444        = 16
} IGCC_SUPPORTED_OUTPUT_ENCODING;

typedef enum _IGCC_SUPPORTED_OUTPUT_BPC
{
    BPCNOTSUPPORTED = 0,
    BPCDEFAULT      = 1,
    BPC6            = 2,
    BPC8            = 4,
    BPC10           = 8,
    BPC12           = 16
} IGCC_SUPPORTED_OUTPUT_BPC;

typedef enum SB_OPERATION_TYPE_ENUM
{
    SB_OPTYPE_UNKNOWN = 0,
    SB_OPTYPE_GET,
    SB_OPTYPE_SET,
    SB_OPTYPE_SET_PERSISTENCE,
    NUM_OF_SB_OPTYPE
} SB_OPERATION_TYPE;

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

#pragma pack(1)

typedef struct _PLATFORM_INFO
{
    MISC_ESC_PRODUCT_FAMILY productFamily;
    MISC_ESC_PLATFORM_TYPE  platformType;
    MISC_ESC_CPUTYPE        cpuType;
    ULONG                   deviceID;
    MISC_ESC_GTTYPE         gtType;
    USHORT                  revID;
    wchar_t                 adapterString[STRING_MAX_SIZE];
    wchar_t                 chipTypeString[STRING_MAX_SIZE];
    UCHAR                   maxSupportedPipes;
} MISC_ESC_PLATFORM_INFO;

typedef struct _MISC_ESC_OS_INFO
{
    ULONG   wddmVer;
    BOOLEAN vmsSupport;
} MISC_ESC_OS_INFO;

typedef struct _MISC_ESC_DVMT_MEM_SIZE
{
    ULONG minVidMemSize;
    ULONG maxVidMemSize;
    ULONG inUseVidMemSize;
    ULONG systemMemTotal;
} MISC_ESC_DVMT_MEM_SIZE;

typedef struct _MISC_ESC_DXGK_POWER_COMPONENT_ARGS
{
    BOOL active; /* Indicate DXGK power component active or idle */
} MISC_ESC_DXGK_POWER_COMPONENT_ARGS;

typedef struct _MISC_ESC_GET_SYSTEM_INFO_ARGS
{
    ULONG                  featureList;
    MISC_ESC_PLATFORM_INFO platformInfo;
    MISC_ESC_DVMT_MEM_SIZE dvmtMemSize;
    MISC_ESC_OS_INFO       oSInfo;
    UCHAR                  gopVersion[0x20];
    BOOLEAN                isS0ixCapable;
    BOOLEAN                isHASActive;
} MISC_ESC_GET_SYSTEM_INFO_ARGS;

typedef struct _CUI_ESC_MEDIA_SOURCE_HDMI_GBD
{
    USHORT usVersion;
    ULONG  ulSize;
    BYTE   byGBDPayLoad[GBD_DATA_SIZE];
} CUI_ESC_MEDIA_SOURCE_HDMI_GBD, *PCUI_ESC_MEDIA_SOURCE_HDMI_GBD;

typedef struct _IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT
{
    CUI_ESC_OPERATION_TYPE         opType;
    DWORD                          displayID;
    IGCC_SUPPORTED_OUTPUT_BPC      overrideBpc;
    IGCC_SUPPORTED_OUTPUT_BPC      supportedBpcMask;
    IGCC_SUPPORTED_OUTPUT_ENCODING overrideEncodingFormat;
    IGCC_SUPPORTED_OUTPUT_ENCODING supportedEncodingMask;
    ULONG64                        Reserved;
} IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT, *PIGCC_GET_SET_OVERRIDE_OUTPUTFORMAT;

typedef struct _CUI_ESC_GET_SET_COLORSPACE_ARGS
{
    _In_ CUI_ESC_OPERATION_TYPE opType;
    _In_ DWORD displayUID;
    _Inout_ BOOLEAN enablePreference;
    _Out_ CUI_ESC_COLORSPACE_SUPPORTED colorspace;
    _In_ CUI_ESC_MEDIA_SOURCE_HDMI_GBD stMediaSourceHDMIGBD;
} CUI_ESC_GET_SET_COLORSPACE_ARGS, *PCUI_ESC_GET_SET_COLORSPACE_ARGS;

#pragma pack()
