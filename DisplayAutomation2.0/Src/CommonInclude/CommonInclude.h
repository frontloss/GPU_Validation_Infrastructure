/*------------------------------------------------------------------------------------------------*
 *
 * @file     CommonInclude.h
 * @brief    This file contains Implementation of Structures _PANEL_INFO, _DISPLAY_TIMINGS
 *           _ADAPTER_INFO_GDI_NAME
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "ValsimSharedCommonInclude.h"

/* Display adapter-related Macros */
#define INTEL_ADAPTER L"8086"
#define CCHDEVICENAME 32
#define MAX_SUPPORTED_DISPLAYS 16

/* Time Definition Macros */
#define MILLI_SEC_100 100
#define SEC_TO_MILLI_SEC 1000

/* Preprocessor Macros*/
#ifdef _DLL_EXPORTS
#define CDLL_EXPORT __declspec(dllexport)
#else
#define CDLL_EXPORT __declspec(dllimport)
#endif

// Polling Count
#define GET_RETRY_COUNT(totalPollingTime, pollInterval) (totalPollingTime / pollInterval)

typedef enum _DRIVER_TYPE
{
    DRIVER_UNKNOWN = 0,
    LEGACY_DRIVER  = 1,
    YANGRA_DRIVER  = 2
} DRIVER_TYPE;

/* Supported display type */
typedef enum _CONNECTOR_PORT_TYPE
{
    DispNone = 0,
    DP_A,
    MIPI_A,
    MIPI_C,
    CRT,

    DP_B,
    DP_C,
    DP_D,
    DP_E,
    DP_F,
    DP_G,
    DP_H,
    DP_I,

    DP_TYPE_C_B,
    DP_TYPE_C_C,
    DP_TYPE_C_D,
    DP_TYPE_C_E,
    DP_TYPE_C_F,
    DP_TYPE_C_G,
    DP_TYPE_C_H,
    DP_TYPE_C_I,

    DP_TBT_B,
    DP_TBT_C,
    DP_TBT_D,
    DP_TBT_E,
    DP_TBT_F,
    DP_TBT_G,
    DP_TBT_H,
    DP_TBT_I,

    HDMI_B,
    HDMI_C,
    HDMI_D,
    HDMI_E,
    HDMI_F,
    HDMI_G,
    HDMI_H,
    HDMI_I,

    DVI_B,
    DVI_C,
    DVI_D,
    DVI_E,
    DVI_F,
    DVI_G,
    DVI_H,
    DVI_I,

    VIRTUALDISPLAY,

    WIDI,
    WD_0,
    WD_1,
    HDMI_A,

    COLLAGE_0

} CONNECTOR_PORT_TYPE;

/*! Display Configuration Error Code */
typedef enum _DISPLAY_CONFIG_ERROR_CODE
{
    DISPLAY_CONFIG_ERROR_SUCCESS                  = 0,
    DISPLAY_CONFIG_ERROR_INVALID_PARAMETER        = 1,
    DISPLAY_CONFIG_ERROR_NOT_SUPPORTED            = 2,
    DISPLAY_CONFIG_ERROR_ACCESS_DENIED            = 3,
    DISPLAY_CONFIG_ERROR_GEN_FAILURE              = 4,
    DISPLAY_CONFIG_ERROR_INSUFFICIENT_BUFFER      = 5,
    DISPLAY_CONFIG_ERROR_BAD_CONFIGURATION        = 6,
    DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED = 7,
    DISPLAY_CONFIG_ERROR_SIZE_MISMATCH            = 8,
    DISPLAY_CONFIG_ERROR_TARGET_INACTIVE          = 9,
    DISPLAY_CONFIG_ERROR_INVALID_DEVICE_NAME      = 10,
    DISPLAY_CONFIG_ERROR_QUERY_MODE_FAILED        = 11,
    DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED     = 12,
    DISPLAY_CONFIG_ERROR_REGISTRY_ACCESS          = 13,
    DISPLAY_CONFIG_ERROR_MODE_VERIFICATION_FAILED = 14,
    DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID       = 15,
    DISPLAY_CONFIG_ERROR_OS_API_CALL_FAILED       = 16,
    DISPLAY_CONFIG_ERROR_SUCCUESS_RR_MISMATCH     = 17,
    DISPLAY_CONFIG_ERROR_VERIFICATION_FAILED      = 18,
    DISPLAY_CONFIG_ERROR_UNDEFINED                = 255
} DISPLAY_CONFIG_ERROR_CODE;

#pragma pack(1)

/*! Structure definition display timings  */
typedef struct _DISPLAY_TIMINGS
{
    _Out_ UINT targetId;                                    // HActive value
    _Out_ ULONG hActive;                                    // HActive value
    _Out_ ULONG vActive;                                    // VActive value
    _Out_ UINT64 hSyncNumerator;                            // Hsync numerator value
    _Out_ UINT64 hSyncDenominator;                          // Hsync denominator value
    _Out_ UINT64 targetPixelRate;                           // target pixel rate value
    _Out_ ULONG hTotal;                                     // Htotal value
    _Out_ ULONG vTotal;                                     // Vtotal value
    _Out_ UINT64 vSyncNumerator;                            // Vsync numerator value
    _Out_ UINT64 vSyncDenominator;                          // Vsync denominator value
    _Out_ UINT isPrefferedMode;                             // If given timing is from preffered mode
    _Out_ DISPLAY_CONFIG_ERROR_CODE status;                 // Error Code for get/Set display mode
    _Out_ DISPLAYCONFIG_SCANLINE_ORDERING scanLineOrdering; //<Scanline ordering (PROGRESSIVE or INTERLACED)
    _Out_ UINT refreshRate;                                 // Refresh rate
} DISPLAY_TIMINGS, *PDISPLAY_TIMINGS;

typedef struct _PANEL_INFO
{
    INT                 sourceID;                         // Source device ID. To be removed later
    UINT32              targetID;                         // Windows Monitor ID
    GFX_ADAPTER_INFO    gfxAdapter;                       // GFX Adapter information
    UINT                version;                          // Legacy: 1, OS_Library_Rewrite:2
    DRIVER_TYPE         driverBranch;                     // V2 -> Legacy/Yangra/Unknown, To be Moved to GFX_ADAPTER_INFO
    CONNECTOR_PORT_TYPE ConnectorNPortType;               // V2 -> Connected Display Type (EDP/DP/HDMI)
    WCHAR               viewGdiDeviceName[CCHDEVICENAME]; // V2 -> It gives Device Display Name (Ex: \\.\DISPLAY1)
    WCHAR               monitorFriendlyDeviceName[128];   // V2 -> Monitor Friendly Device Name
    DISPLAY_TIMINGS     osPreferredMode;                  // V2 -> Os Preferred Mode
} PANEL_INFO, *PPANEL_INFO;

typedef struct _MULTI_PANEL_INFO
{
    _In_ UINT size;                                       //  Size of DISPLAY_CONFIG
    _Inout_ PANEL_INFO panelInfo[MAX_SUPPORTED_DISPLAYS]; //  Panel Info Array
    _In_ UINT Count;                                      //  Count of display and adaptor info entries
    _Out_ DISPLAY_CONFIG_ERROR_CODE status;               //  Error Code
} MULTI_PANEL_INFO, *PMULTI_PANEL_INFO;

/** Structure definition for GFX Adapter Information */
typedef struct _ADAPTER_INFO_GDI_NAME
{
    LUID             adapterID;                        // Locally Unique Identifier
    WCHAR            viewGdiDeviceName[CCHDEVICENAME]; // It gives Device Display Name (Ex: \\.\DISPLAY1)
    GFX_ADAPTER_INFO adapterInfo;                      // GFX Adapter information
} ADAPTER_INFO_GDI_NAME, *PADAPTER_INFO_GDI_NAME;

#pragma pack()