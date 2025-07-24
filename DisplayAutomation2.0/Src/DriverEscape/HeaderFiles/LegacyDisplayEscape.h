/*------------------------------------------------------------------------------------------------*
 *
 * @file     LegacyDisplayEscape.h
 * @brief    This file contains Implementation of LegacyQueryCurrentConfig, LegacyDpcdRead, LegacyDpcdWrite, LegacyGetEdidData
 *           LegacyGetMiscSystemInfo, LegacyGetSetDPPHWLUT, LegacyGetColorimetryInfo, LegacySetColorimetryInfo
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "CommonInclude.h"
#include "EscapeSharedHeader.h"

#define CUI_ESC_MAX_PATHS 3

#define SB_DP_PORT 0
#define SB_DP_READ 9
#define SB_DP_WRITE 8
#define SB_DATA_SIZE 512
#define SB_DP_PORTNUMBER 0

#define CUI_ESC_MAX_VIEWS 8

enum CUI_COM_FUNCTIONS
{
    COM_ESC_DETECT_DEVICE = 0, // Detect Display Devices
    COM_ESC_POWER_CONSERVATION,
    COM_ESC_GET_VALID_CONFIGS,
    COM_ESC_CONVERT_RR_RATIONAL,
    COM_ESC_QUERY_MODE_TABLE,
    COM_ESC_VALIDATE_OR_ADVISE_CONFIG_OR_MODE,
    COM_ESC_SET_S3D_MODE, // S3D Mode set request,
    COM_ESC_GET_S3D_CAPS, // Get the S3D Caps of platform or a particualr display ,
    COM_ESC_GET_SET_DISPLAY_POWER_STATE,
    COM_ESC_GET_SET_AUDIO_DATA,
    COM_ESC_MODE_SET_NOTIFY,
    COM_ESC_SET_BEZEL,
    COM_ESC_GET_BEZEL,
    COM_ESC_ENABLE_DISABLE_COLLAGE,
    COM_ESC_SMART_FRAME,
    COM_ESC_GET_PANELFIT,
    COM_ESC_GET_EVENTS,
    COM_ESC_GET_SET_COLORSPACE,
    COM_ESC_GET_SET_CSC_COEFFICIENTS,
    COM_ESC_QUERY_COMPENSATION_IN_TOPOLOGY,
    COM_ESC_QUERY_ROTATION_IN_TOPOLOGY,
    COM_ESC_QUERY_CURRENT_CONFIG,
    COM_ESC_QUERY_PREF_MODE_IN_TOPOLOGY,
    COM_ESC_SET_GAMMA,
    COM_ESC_GET_LAST_APPLIED_GAMMA,
    COM_ESC_GET_DEFAULT_GAMMA,
    COM_ESC_CUI_REGISTRY_DWORD,
    COM_ESC_CUI_REGISTRY_BINARY,
    COM_ESC_NVHG_GET_SET_DATA,               // Hybrid Graphics related Escape
    COM_ESC_NVHG_GET_SET_SCALING,            // Hybrid Graphics related Escape
    COM_ESC_GET_CURRENT_IGPU_STATUS_TPVTYPE, // Get system details (SG or not, active GPU, ML Scheme)
    COM_ESC_ROTATION_NOTIFICATION_FOR_KVM,   // Notify Driver about Rotation info in topology, only for WinTH+
    COM_ESC_GET_SET_HW_3DLUT,                // 3D LUT Escape code
    COM_ESC_GET_CURSOR_SHAPE,
    COM_ESC_GET_SET_VRR,
    SB_ESC_SET_CUSTOM_SCALING,
    SB_ESC_GET_SET_DISPLAY_PARAM,
    SB_ESC_I2C_ACCESS,
    SB_ESC_ATOMIC_I2C_ACCESS,
    SB_ESC_AUX_ACCESS,
    SB_ESC_ADD_CUSTOM_MODE,
    SB_ESC_GET_CUSTOM_MODES,
    SB_ESC_REMOVE_CUSTOM_MODE,
    SB_ESC_GET_COMPLETE_DP_TOPOLOGY,
    SB_ESC_SET_DP_TOPOLOGY,
    SB_ESC_GET_DP_LEAF_INFO,
    COM_ESC_GET_EDID                   = 200, // EDID Tool
    COM_ESC_GET_SYSTEM_INFO            = 201, // Get System Info. functions
    SB_ESC_QUERY_DISPLAY_DETAILS       = 202, // DP Applet Tool
    SB_ESC_GET_SET_LOCK_DISPLAY_CONFIG = 203, // RCR 2262236 - Integrated Intel DP issues on Lenovo ThinkStation P300/P310
    COM_ESC_GET_SET_REMOVE_SCALING_IN_OS_MODELIST,
    COM_ESC_HOT_PLUG_VIRTUAL_DISPLAY,
    COM_ESC_BLOCK_VIRTUAL_DISPLAY_CAPTURE,
    COM_ESC_GET_VERSION,
    COM_ESC_GET_SET_OVERRIDE_OUTPUT_FORMAT,
    MAX_CUI_COM_FUNCTIONS
};

typedef enum _CUI_ESC_MODE_INFO_TYPE
{
    CUI_ESC_MODE_NOT_PINNED = 0,
    CUI_ESC_MODE_PINNED,
    CUI_ESC_MODE_LIST_NUM_ONLY_QUERIED,
    CUI_ESC_MODE_LIST_DETAILS_QUERIED,
    CUI_ESC_MODE_INFO_SCALING_QUERIED,
    CUI_ESC_MODE_INFO_ROTATION_QUERIED,
    CUI_ESC_MODE_INFO_PREF_CUI_MODE_QUERIED,
    CUI_ESC_MODE_INFO_UPDATE_NUM_MODES,
    CUI_ESC_MODE_INFO_UPDATE_DETAILS_MODES,
    MAX_CUI_MODE_INFO_TYPE = 9
} CUI_ESC_MODE_INFO_TYPE;

typedef enum _CUI_ESC_SCAN_LINE_ORDER
{
    CUI_ESC_SCANORDER_UNKNOWN = 0,
    CUI_ESC_PROGRESSIVE       = 1,
    CUI_ESC_INTERLACED        = 2
} CUI_ESC_SCAN_LINE_ORDER;

typedef enum _CUI_ESC_PIXELFORMAT
{
    CUI_ESC_UNINITIALIZED = 0,
    CUI_ESC_8BPP_INDEXED,
    CUI_ESC_B5G6R5X0,
    CUI_ESC_B8G8R8X8,
    CUI_ESC_B8G8R8A8,
    CUI_ESC_R8G8B8X8,
    CUI_ESC_R8G8B8A8,
    CUI_ESC_R10G10B10X2,
    CUI_ESC_R10G10B10A2,
    CUI_ESC_B10G10R10X2,
    CUI_ESC_B10G10R10A2,
    CUI_ESC_R10G10B10A2_XR_BIAS,
    CUI_ESC_R16G16B16X16F,
    CUI_ESC_R16G16B16A16F,
    CUI_ESC_MAX_PIXELFORMAT,
    CUI_ESC_NV12YUV420,
    CUI_ESC_YUV422,
    CUI_ESC_P010YUV420,
    CUI_ESC_P012YUV420,
    CUI_ESC_P016YUV420,
    CUI_ESC_YUV444_10,
    CUI_ESC_YUV422_10,
    CUI_ESC_YUV422_12,
    CUI_ESC_YUV422_16,
    CUI_ESC_YUV444_8,
    CUI_ESC_YUV444_12,
    CUI_ESC_YUV444_16,
    CUI_ESC_MAXALL_PIXELFORMAT,
} CUI_ESC_PIXELFORMAT;

typedef enum _CUI_ESC_COLLAGE_TYPE
{
    CUI_ESC_NON_COLLAGE        = 0,
    CUI_ESC_HORIZONTAL_COLLAGE = 1,
    CUI_ESC_VERTICAL_COLLAGE   = 2,
    CUI_ESC_COLLAGE_MODE       = 4
} CUI_ESC_COLLAGE_TYPE;

typedef enum _SB_AUX_ERROR_TYPE
{
    SB_AUX_NOERROR = 0,
    SB_AUX_CORRUPT_BUFFER,
    SB_AUX_INVALID_AUX_DEVICE,
    SB_AUX_INVALID_OPERATION_TYPE,
    SB_AUX_INVALID_AUX_DATA_SIZE,
    SB_AUX_INVALID_AUX_ADDRESS,
    SB_AUX_ERROR_DEFER,
    SB_AUX_ERROR_TIMEOUT,
    SB_AUX_ERROR_INCOMPLETE_WRITE,
    SB_AUX_ERROR_UNKNOWN,
    SB_MAX_ERRORS
} SB_AUX_ERROR_TYPE;

typedef enum _PORT_TYPES
{
    NULL_PORT_TYPE = -1,
    ANALOG_PORT    = 0,
    DVOA_PORT,
    DVOB_PORT,
    DVOC_PORT,
    DVOD_PORT,
    LVDS_PORT,
    INTDPE_PORT,
    INTHDMIB_PORT,
    INTHDMIC_PORT,
    INTHDMID_PORT,
    INT_DVI_PORT,
    INTDPA_PORT,
    INTDPB_PORT,
    INTDPC_PORT,
    INTDPD_PORT,
    TPV_PORT,
    INTMIPIA_PORT,
    INTMIPIC_PORT,
    WIGIG_PORT,
    DVOF_PORT,
    INTHDMIF_PORT,
    INTDPF_PORT,
    DVOE_PORT,
    INTHDMIE_PORT,
    INTDPG_PORT, // Gen11P5 onwards
    DVOG_PORT,
    INTHDMIG_PORT,
    INTDPH_PORT,
    DVOH_PORT,
    INTHDMIH_PORT,
    INTDPI_PORT,
    DVOI_PORT,
    INTHDMII_PORT,
    VIRTUALDVI_PORT,
    MAX_PORTS
} PORT_TYPES;

typedef enum _DISPLAY_TYPE
{
    NULL_DISPLAY_TYPE = 0,
    CRT_TYPE,
    TV_TYPE,
    DFP_TYPE,
    LFP_TYPE,
    MAX_DISPLAY_TYPES = LFP_TYPE
} DISPLAY_TYPE;

typedef enum _CUI_ESC_HW_3DLUT_OPERATION_TYPE
{
    CUI_ESC_HW_3DLUT_OPTYPE_UNKNOWN = 0,         // Invalid operation type.
    CUI_ESC_HW_3DLUT_OPTYPE_GET_HW_SUPPORT_INFO, // Get details of currently applied LUT.
    CUI_ESC_HW_3DLUT_OPTYPE_ENABLE,              // Enable LUT on the given displayUid.
    CUI_ESC_HW_3DLUT_OPTYPE_DISABLE,             // Disable LUT that was applied previously.
    CUI_ESC_NUM_OF_HW_3DLUT_OPTYPE
} CUI_ESC_HW_3DLUT_OPERATION_TYPE;

typedef enum _HW_3DLUT_OPERATION_TYPE
{
    HW_3DLUT_OPTYPE_UNKNOWN = 0,         // Invalid operation type.
    HW_3DLUT_OPTYPE_GET_HW_SUPPORT_INFO, // Get details of currently applied LUT.
    HW_3DLUT_OPTYPE_ENABLE,              // Enable LUT on the given displayUid.
    HW_3DLUT_OPTYPE_DISABLE,             // Disable LUT that was applied previously.
    NUM_OF_HW_3DLUT_OPTYPE
} HW_3DLUT_OPERATION_TYPE;

#pragma pack(1)

typedef struct
{
    UCHAR Red;
    UCHAR Green;
    UCHAR Blue;
    UCHAR Alpha;
} COLOR_RGBA;

typedef struct
{
    ULONG Blue : 10;
    ULONG Green : 10;
    ULONG Red : 10;
    ULONG Reserved : 2;
} IGFX_3DLUT_COLOR_RGB;

typedef struct _CUI_ESC_CUSTOM_COMPENSATION_INFO
{
    ULONG minCustomScaling;     // Maximum down scaling
    ULONG maxCustomScaling;     // Maximum up scaling
    ULONG step;                 // Steps in which scaling can be requested
    ULONG currentCustomScaling; // Current value of custom scaling
    ULONG defaultScaling;       // Default value of custom scaling
} CUI_ESC_CUSTOM_COMPENSATION_INFO, *PCUI_ESC_CUSTOM_COMPENSATION_INFO;

typedef struct _CUI_ESC_COMPENSATION_ARGS
{
    USHORT                           compensation;
    CUI_ESC_CUSTOM_COMPENSATION_INFO customCompX; // Horizontal custom comp info
    CUI_ESC_CUSTOM_COMPENSATION_INFO customCompY; // Vertical custom comp info
} CUI_ESC_COMPENSATION_ARGS, *PCUI_ESC_COMPENSATION_ARGS;

typedef struct _CUI_ESC_MODE_INFO
{
    USHORT                    sourceX;               // Horizontal Resolution
    USHORT                    sourceY;               // Vertical Resolution
    USHORT                    colorBPP;              // Multi-select field, for pinned mode select only one value
    USHORT                    refreshRate;           // Refresh rate in integer format
    CUI_ESC_SCAN_LINE_ORDER   eScanLineOrder;        // Interlaced or Progressive
    CUI_ESC_PIXELFORMAT       eSourcePixelFormat;    // Unused; Multi-select field, for pinned mode select only one value
    CUI_ESC_COMPENSATION_ARGS stCompensationCaps;    // Supported compensation, Multi-select field, for pinned mode select only one value; for mode enum, all supported compensation
    CUI_ESC_COMPENSATION_ARGS stCurrentCompensation; // Current compensation, for current config, validate/advise etc
    CUI_ESC_COMPENSATION_ARGS stPreferredCompensation; // Preferred Compensation, used in Mode Enum Args
} CUI_ESC_MODE_INFO, *PCUI_ESC_MODE_INFO;

typedef struct _CUI_ESC_PATH_INFO
{
    ULONG                  sourceID;
    ULONG                  targetID;      // Display UID
    CUI_ESC_MODE_INFO_TYPE eModeInfoType; // mode pinned or not, num and details goes only with not_pinned
    CUI_ESC_MODE_INFO      stModeInfo;    // Actual mode details
} CUI_ESC_PATH_INFO, *PCUI_ESC_PATH_INFO;

typedef struct _CUI_ESC_TOPOLOGY
{
    ULONG                numOfPaths;                    // number of valid paths in the topology
    CUI_ESC_COLLAGE_TYPE eCollageConfig;                // this is bitwise field to indicate collage config type
    BOOLEAN              ignoreUnsupportedModes;        // If this is set(in threshold) driver will retrun native tgt timings for unsupported modes
    CUI_ESC_PATH_INFO    stPathInfo[CUI_ESC_MAX_PATHS]; // Array of Paths
} CUI_ESC_TOPOLOGY, *PCUI_ESC_TOPOLOGY;

typedef struct _CUI_ESC_RR_RATIONAL_INFO
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
} CUI_ESC_RR_RATIONAL_INFO, *PCUI_ESC__RATIONAL_INFO;

typedef struct _CUI_ESC_CONVERT_RR_RATIONAL_ARGS
{
    CUI_ESC_TOPOLOGY         stTopology;
    CUI_ESC_RR_RATIONAL_INFO stRR_RationalInfo[CUI_ESC_MAX_VIEWS];
} CUI_ESC_CONVERT_RR_RATIONAL_ARGS, *PCUI_ESC_CONVERT_RR_RATIONAL_ARGS;

typedef struct _CUI_ESC_QUERY_COMPENSATION_ARGS
{
    _Out_ CUI_ESC_TOPOLOGY stTopology;
    _Out_ ULONG error;
} CUI_ESC_QUERY_COMPENSATION_ARGS, *PCUI_ESC_QUERY_COMPENSATION_ARGS, CUI_ESC_QUERY_CURRENT_CONFIG_ARGS, *PCUI_ESC_QUERY_CURRENT_CONFIG_ARGS, CUI_ESC_QUERY_PREF_MODE_ARGS,
*PCUI_ESC_QUERY_PREF_MODE_ARGS;

typedef struct _CUI_ESC_GET_SET_HW_3DLUT_ARGS
{
    _In_ CUI_ESC_HW_3DLUT_OPERATION_TYPE opType;
    _In_ ULONG deviceUID;
    _Out_ BOOLEAN forceModeSetRequired;
    _Inout_ ULONG LUTDepth;
} CUI_ESC_GET_SET_HW_3DLUT_ARGS, *PCUI_ESC_GET_SET_HW_3DLUT_ARGS;

typedef struct _RELATIVEADDRESS
{
    UCHAR totalLinkCount;
    UCHAR address[MAX_BYTES_RAD];
} RELATIVEADDRESS, *PRELATIVEADDRESS;

/* I2C access args structure*/
typedef struct _SB_AUXCACCESS_ARGS
{
    _Out_ SB_AUX_ERROR_TYPE eSBAuxErrorType;
    _In_ PORT_TYPES portType;
    _In_ RELATIVEADDRESS relativeAddress;
    _In_ DWORD deviceUID;
    _In_ ULONG command;
    _In_ BOOLEAN usePortType;
    _Inout_ ULONG size;
    _Inout_ BYTE data[MAX_LUT_AUX_BUFSIZE];
    _In_ ULONG address;
} SB_AUXACCESS_ARGS, *PSB_AUXACCESS_ARGS;

/** Structure used for edid escape*/
typedef struct _COM_ESC_GET_EDID_ARGS
{
    _In_ ULONG displayID;
    _In_ ULONG edidBlockNum;
    _Out_ UCHAR edidData[EDID_BLOCK_SIZE];
} COM_ESC_GET_EDID_ARGS, *PCOM_ESC_GET_EDID_ARGS;

#pragma pack()

/* Private Function */
BOOLEAN LegacyQueryCurrentConfig(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ CUI_ESC_QUERY_COMPENSATION_ARGS *pQueryCurrentConfig);
BOOLEAN LegacyDpcdRead(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[]);
BOOLEAN LegacyDpcdWrite(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[]);
BOOLEAN LegacyGetEdidData(_In_ PANEL_INFO *pPanelInfo, _Out_ BYTE edidData[], _Out_ UINT *pNumEdidBlock);
BOOLEAN LegacyGetMiscSystemInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Out_ MISC_ESC_GET_SYSTEM_INFO_ARGS *pMiscSystemInfo);
BOOLEAN LegacyGetSetDPPHWLUT(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _In_ ULONG size, _Inout_ CUI_ESC_GET_SET_HW_3DLUT_ARGS *pDppHwLutInfo);
BOOLEAN LegacyGetColorimetryInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Inout_ CUI_ESC_GET_SET_COLORSPACE_ARGS *pColorimetryArgs);
BOOLEAN LegacySetColorimetryInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Inout_ CUI_ESC_GET_SET_COLORSPACE_ARGS *pColorimetryArgs);
BOOLEAN LegacyGetSetOutputFormat(_In_ PANEL_INFO *pPanelInfo, _Inout_ IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT *pGetSetOutputFormat);
BOOLEAN LegacyConfigDxgkPowerComponent(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Inout_ MISC_ESC_DXGK_POWER_COMPONENT_ARGS *pDxgkPowerCompArgs);
