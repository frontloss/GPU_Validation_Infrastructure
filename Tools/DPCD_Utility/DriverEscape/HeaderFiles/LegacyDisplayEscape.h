/*------------------------------------------------------------------------------------------------*
 *
 * @file     LegacyDisplayEscape.h
 * @brief    This file contains Implementation of LegacyDpcdRead, LegacyDpcdWrite
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "EscapeSharedHeader.h"

#define CUI_ESC_MAX_PATHS 3

#define SB_DP_PORT 0
#define SB_DP_READ 9
#define SB_DP_WRITE 8
#define SB_DATA_SIZE 512
#define SB_DP_PORTNUMBER 0

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

#pragma pack(1)

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

typedef struct _CUI_ESC_QUERY_COMPENSATION_ARGS
{
    _Out_ CUI_ESC_TOPOLOGY stTopology;
    _Out_ ULONG error;
} CUI_ESC_QUERY_COMPENSATION_ARGS, *PCUI_ESC_QUERY_COMPENSATION_ARGS, CUI_ESC_QUERY_CURRENT_CONFIG_ARGS, *PCUI_ESC_QUERY_CURRENT_CONFIG_ARGS, CUI_ESC_QUERY_PREF_MODE_ARGS,
*PCUI_ESC_QUERY_PREF_MODE_ARGS;

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

#pragma pack()

/* Private Function */
BOOLEAN LegacyDpcdRead(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[]);
BOOLEAN LegacyDpcdWrite(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[]);
