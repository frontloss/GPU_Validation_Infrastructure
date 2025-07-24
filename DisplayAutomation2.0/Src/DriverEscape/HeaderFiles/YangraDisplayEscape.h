/*------------------------------------------------------------------------------------------------*
 *
 * @file     YangraDisplayEscape.h
 * @brief    This file contains Implementation of YangraDpcdRead, YangraDpcdWrite, YangraGetEdidData, YangraGetMiscSystemInfo
 *           YangraGetSetDPPHWLUT, YangraGetColorimetryInfo, YangraSetColorimetryInfo
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "CommonInclude.h"
#include "EscapeSharedHeader.h"

#define DD_MAX(a, b) ((a) < (b) ? (b) : (a))
#define DD_BITFIELD_RANGE(lowBit, highBit) ((highBit) - (lowBit) + 1)

#define DD_CUI_ESC_MAX_POSSIBLE_PIPES 8
#define DD_CUI_ESC_MAX_PHYSICAL_PIPES 4
#define DD_CAPI_ESC_MAX_PHYSICAL_PIPES 4
#define MAX_POSSIBLE_PIPES DD_MAX(DD_CUI_ESC_MAX_PHYSICAL_PIPES, 8)

#define MAX_NUM_IDENTITY_TARGET_MODE_PER_SOURCE_MODE 32
#define MAX_NUM_SCALED_TARGET_MODE_PER_SOURCE_MODE (MAX_NUM_IDENTITY_TARGET_MODE_PER_SOURCE_MODE / 2)
#define MAX_NUM_TARGET_MODE_PER_SOURCE_MODE (MAX_NUM_IDENTITY_TARGET_MODE_PER_SOURCE_MODE + MAX_NUM_SCALED_TARGET_MODE_PER_SOURCE_MODE)

#define MAX_PARS_POSSIBLE_WITH_1_VIC 2
#define DD_COLOR_3DLUT_NUM_SAMPLES 4913
#define MAX_DPSTATES 10
#define HWLUT_SAMPLE_SIZE 17
#define MAX_LUT_DATA 19652

#define FILE_SIZE 124
#define MAX_WRITEBACK_DEVICE 2
#define DD_BITFIELD_BIT(bit) 1
#define DD_ESC_COLOR_MATRIX_NUM_COEFFICIENTS 9
#define DD_ESC_COLOR_MATRIX_NUM_OFFSET 3

#define MAX_PHYSICAL_PIPES 4

typedef enum _DD_ESCAPE_FUNC
{
    DD_ESC_QUERY_MODE_TABLE = 0,
    DD_ESC_DETECT_DEVICE,
    DD_ESC_GET_INVALID_DISP_COMBO,
    DD_ESC_SET_CUSTOM_SCALING,
    DD_ESC_CUSTOM_MODES,
    DD_ESC_POWER_CONSERVATION,
    DD_ESC_S3D, // TODO
    DD_ESC_GET_SET_COLLAGE_MODE,
    DD_ESC_GET_CURSOR_SHAPE, // TODO
    DD_ESC_VIRTUAL_DISPLAY,  // TODO
    DD_ESC_GET_SET_VRR,
    DD_ESC_ROTATION_FOR_KVM, // TODO
    DD_ESC_DISP_PWR_MAX,

    // Color Escapes
    DD_ESC_SET_CSC,
    DD_ESC_GET_SET_GAMMA,
    DD_ESC_GET_SET_COLOR_MODEL,
    DD_ESC_SET_3D_LUT,
    DD_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME,

    // IntegerScaling
    DD_ESC_GET_SET_NN_SCALING,

    // Tool Escapes
    DD_ESC_GET_VERSION = 100,
    DD_ESC_AUX_I2C_ACCESS,
    DD_ESC_GET_EDID,
    DD_ESC_QUERY_DISPLAY_DETAILS,

    // This is for development use only
    DD_ESC_EXPERIMENT,
    // Writeback Escape
    DD_ESC_WRITEBACK_QUERY,
    DD_ESC_WRITEBACK_ENABLE_DISABLE,
    DD_ESC_WRITEABCK_CAPTURE_BUFFER,
    DD_ESC_UPDATE_GET_DP_CAPABILITIES,
    DD_ESC_GET_SET_SMOOTH_SYNC,
    DD_ESC_GET_DP_MST_PORT_DETAILS,
    DD_ESC_GET_SET_CAPPED_FPS,
    // Sharpness Enhancement using Display Scaler Filters
    DD_ESC_GET_SET_SHARPNESS_FACTOR,
    // Genlock
    DD_ESC_GET_SET_GENLOCK,
    DD_ESC_GET_SET_OVERRIDE_OUTPUT_FORMAT = 114,
    DD_ESC_CAPI_GET_SET_VBLANK_TS,
    // Add before this
    DD_ESC_MAX
} DD_ESCAPE_FUNC;

typedef enum _DD_ESCAPE_STATUS
{
    DD_ESCAPE_STATUS_SUCCESS = 0,
    DD_ESCAPE_AUX_ERROR_DEFER,
    DD_ESCAPE_AUX_ERROR_TIMEOUT,
    DD_ESCAPE_AUX_ERROR_INCOMPLETE_WRITE,
    DD_ESCAPE_COLOR_3DLUT_INVALID_PIPE,
    DD_ESCAPE_STATUS_UNKNOWN
} DD_ESCAPE_STATUS;

typedef enum _DD_AUX_I2C_OPERATIONS
{
    DD_OPERATION_UNKNOWN = 0,
    DD_NATIVE_AUX,
    DD_I2C_AUX,
    DD_I2C,
    DD_ATOMICI2C,
    DD_REMOTE_DPCD,
    DD_I2C_MOT
} DD_AUX_I2C_OPERATION;

/* Port structure related to DDRW*/
typedef enum _DD_PORT_TYPE
{
    DD_PORT_TYPE_UNKNOWN = -1,
    DD_PORT_TYPE_DIGITAL_PORT_A,
    DD_PORT_TYPE_DIGITAL_PORT_B,
    DD_PORT_TYPE_DIGITAL_PORT_C,
    DD_PORT_TYPE_DIGITAL_PORT_D,
    DD_PORT_TYPE_DIGITAL_PORT_E,
    DD_PORT_TYPE_DIGITAL_PORT_F,
    DD_PORT_TYPE_DIGITAL_PORT_G,
    DD_PORT_TYPE_DIGITAL_PORT_H,
    DD_PORT_TYPE_DIGITAL_PORT_I,
    DD_PORT_TYPE_DSI_PORT_0,
    DD_PORT_TYPE_DSI_PORT_1,
    DD_PORT_TYPE_WRITEBACK_PORT,
    DD_PORT_TYPE_VIRTUAL_PORT,
    DD_PORT_TYPE_COLLAGE_PORT_0 = 14,
    DD_PORT_TYPE_MAX
} DD_PORT_TYPE;

typedef enum _DD_CUI_ESC_COLLAGE_OPERATION
{
    DD_CUI_ESC_COLLAGE_OPERATION_GET          = 0,
    DD_CUI_ESC_COLLAGE_OPERATION_VALIDATE     = 1,
    DD_CUI_ESC_COLLAGE_OPERATION_ENABLE       = 2,
    DD_CUI_ESC_COLLAGE_OPERATION_DISABLE      = 3,
    DD_CUI_ESC_COLLAGE_OPERATION_BEZEL_UPDATE = 4
} DD_CUI_ESC_COLLAGE_OPERATION;

typedef enum _DD_COLOR_OPERATION
{
    DD_COLOR_OPERATION_GET             = 0,
    DD_COLOR_OPERATION_SET             = 1,
    DD_COLOR_OPERATION_RESTORE_DEFAULT = 2,
    DD_COLOR_OPERATION_MAX
} DD_COLOR_OPERATION;

typedef enum _DD_COLOR_3DLUT_STATUS
{
    DD_COLOR_3DLUT_SUCCESS,
    DD_COLOR_3DLUT_INVALID_PIPE,
    DD_COLOR_3DLUT_INVALID_DATA,
    DD_COLOR_3DLUT_NOT_SUPPORTED_IN_HDR,
    DD_COLOR_3DLUT_INVALID_OPERATION,
    DD_COLOR_3DLUT_UNSUCCESS
} DD_COLOR_3DLUT_STATUS;

typedef enum _DD_COLOR_MODEL
{
    DD_COLOR_MODEL_UNINITIALIZED   = 0,
    DD_COLOR_MODEL_RGB             = 1,
    DD_COLOR_MODEL_YCBCR_601       = 2,
    DD_COLOR_MODEL_YCBCR_709       = 3,
    DD_COLOR_MODEL_YCBCR_2020      = 4,
    DD_COLOR_MODEL_YCBCR_PREFERRED = 5,
    DD_COLOR_MODEL_SCRGB           = 6,
    DD_COLOR_MODEL_INTENSITY_ONLY  = 7,
    DD_COLOR_MODEL_CUSTOM          = 8,
    DD_COLOR_MODEL_MAX
} DD_COLOR_MODEL;

typedef enum _DD_CUI_ESC_VRR_OPERATION
{
    DD_CUI_ESC_VRR_OPERATION_GET_INFO,         // Get details of VRR support and current status
    DD_CUI_ESC_VRR_OPERATION_ENABLE,           // Enable VRR
    DD_CUI_ESC_VRR_OPERATION_DISABLE,          // Disable VRR
    DD_CUI_ESC_VRR_OPERATION_LOW_FPS_ENABLE,   // Enable Low FPS VRR
    DD_CUI_ESC_VRR_OPERATION_LOW_FPS_DISABLE,  // Disable Low FPS VRR
    DD_CUI_ESC_VRR_OPERATION_HIGH_FPS_ENABLE,  // Enable High FPS VRR -> Async Flip Enabling
    DD_CUI_ESC_VRR_OPERATION_HIGH_FPS_DISABLE, // Disable High FPS VRR
} DD_CUI_ESC_VRR_OPERATION;

typedef enum _DD_CUI_ESC_PIXELFORMAT
{
    // IF ANY NEW FORMAT IS ADDED HERE, PLEASE UPDATE ALL THE BELOW MACORS.
    DD_CUI_ESC_8BPP_INDEXED = 0,
    DD_CUI_ESC_B5G6R5X0,
    DD_CUI_ESC_B8G8R8X8,
    DD_CUI_ESC_R8G8B8X8,
    DD_CUI_ESC_B10G10R10X2,
    DD_CUI_ESC_R10G10B10X2,
    DD_CUI_ESC_R10G10B10X2_XR_BIAS,
    DD_CUI_ESC_R16G16B16X16F,
    DD_CUI_ESC_YUV422_8,
    DD_CUI_ESC_YUV422_10,
    DD_CUI_ESC_YUV422_12,
    DD_CUI_ESC_YUV422_16,
    DD_CUI_ESC_YUV444_8,
    DD_CUI_ESC_YUV444_10,
    DD_CUI_ESC_YUV444_12,
    DD_CUI_ESC_YUV444_16,
    DD_CUI_ESC_NV12YUV420,
    DD_CUI_ESC_P010YUV420,
    DD_CUI_ESC_P012YUV420,
    DD_CUI_ESC_P016YUV420,
    DD_CUI_ESC_MAX_PIXELFORMAT
    // IF ANY NEW FORMAT IS ADDED HERE, PLEASE UPDATE ALL THE BELOW MACORS.
} DD_CUI_ESC_PIXELFORMAT;

typedef enum _PLUG_ACTIONS
{
    UNPLUG_WB,
    PLUG_WB,
    MAX_ACTION
} PLUG_ACTIONS;

typedef enum _WB_OPERATION_MODE
{
    WB_OS_MODE,
    WB_DFT_MODE,
} WB_OPERATION_MODE;

typedef enum _DD_ESC_SURFACE_MEMORY_TYPE
{
    DD_ESC_SURFACE_MEMORY_INVALID        = 0,
    DD_ESC_SURFACE_MEMORY_LINEAR         = 1, // Surface uses linear memory
    DD_ESC_SURFACE_MEMORY_TILED          = 2, // Surface uses tiled memory
    DD_ESC_SURFACE_MEMORY_X_TILED        = DD_ESC_SURFACE_MEMORY_TILED,
    DD_ESC_SURFACE_MEMORY_Y_LEGACY_TILED = 4, // Surface uses Legacy Y tiled memory (Gen9+)
    DD_ESC_SURFACE_MEMORY_Y_F_TILED      = 8, // Surface uses Y F tiled memory
} DD_ESC_SURFACE_MEMORY_TYPE;

/* Video output technology (VOT) type*/
typedef enum _DD_VIDEO_OUTPUT_TECHNOLOGY
{
    DD_VOT_UNKNOWN = 0,
    DD_VOT_VGA,
    DD_VOT_DVI,
    DD_VOT_HDMI,
    DD_VOT_DISPLAYPORT_EXTERNAL,
    DD_VOT_DISPLAYPORT_EMBEDDED,
    DD_VOT_MIPI,
    DD_VOT_VIRTUAL,
    DD_VOT_WDE,
    DD_VOT_MIRACAST,
    DD_VOT_MAX = DD_VOT_MIRACAST
} DD_VIDEO_OUTPUT_TECHNOLOGY;

typedef enum _DD_CONNECTOR_TYPE
{
    DD_CONNECTOR_NONE,
    DD_CONNECTOR_EDP,
    DD_CONNECTOR_DP,
    DD_CONNECTOR_HDMI,
    DD_CONNECTOR_DVI,
    DD_CONNECTOR_MIPI
} DD_CONNECTOR_TYPE;

/** Enum for HDCP Version */
typedef enum _DD_CUI_ESC_HDCP_VERSION
{
    DD_CUI_ESC_INVALIDHDCPVERSION = 0,
    DD_CUI_ESC_HDCP1_4            = 1,
    DD_CUI_ESC_HDCP2_2            = 2,
} DD_CUI_ESC_HDCP_VERSION;

/** Enum for Reporting the Reason to GCP/CUI why the Panel Max Mode is not Supported. There are two restrictions defined:
1. Platform Restriction(VBT,SKUing)
2. Dongle Restriction(i.e Dongle is not capable to support the particular mode). */
typedef enum _DD_CUI_ESC_MODE_ENUM_RESTRICTIONS
{
    CUI_ESC_PLATFORM_RESTRICTION = 0,
    CUI_ESC_DONGLE_RESTRICTION,
} DD_CUI_ESC_MODE_ENUM_RESTRICTIONS;

typedef enum _PWRCONS_OPERATION_TYPE_ENUM
{
    PWRCONS_OPTYPE_UNKNOWN = 0,
    PWRCONS_OPTYPE_GET,
    PWRCONS_OPTYPE_SET,
    NUM_OF_PWRCONS_OPTYPE
} PWRCONS_OPERATION_TYPE;

typedef enum _DD_PWR_SRC_EVENT_ARGS
{
    DD_PWR_UNKNOWN,
    DD_PWR_AC,
    DD_PWR_DC
} DD_PWR_SRC_EVENT_ARGS;

typedef enum _PWRCONS_OPERATION_ENUM
{
    PWRCONS_OP_UNKNOWN = 0,         // Invalid operation
    PWRCONS_OP_FEATURE_SETTINGS,    // User Feature Setting operation
    PWRCONS_OP_BACKLIGHT_SETTINGS,  // User Backlight Setting operation
    PWRCONS_OP_POWER_PLAN_SETTINGS, // User Power Plan Setting operation
    PWRCONS_OP_TURBO_SETTINGS,      // Turbo Settings
    PWRCONS_OP_TURBO_OC_SETTINGS,   // Turbo Over-clocking Settings
    PWRCONS_OP_ALS_SETTINGS,        // ALS lux value from CUI for assertive display and LACE
    NUM_OF_PWRCONS_OPERATION
} PWRCONS_OPERATION;

// PC Operation return status definitions
typedef enum _PWRCONS_OPERATION_STATUS_ENUM
{
    OPERATION_STATUS_UNKNOWN,               // Unknown return status
    OPERATION_STATUS_SUCCESS,               // Success
    OPERATION_STATUS_FAILURE,               // Failure
    OPERATION_INVALID_PARAMETERS,           // Invalid Parameters
    OPERATION_STATUS_INVALID_INVERTER_TYPE, // Invalid Inverter Type, Backlight OP
    OPERATION_STATUS_INVALID_PWM_FREQUENCY, // Invalid PWM Frequency, Backlight OP
    OPERATION_STATUS_NOT_SUPPORTED          // Operation not supported under system configuration
} PWRCONS_OPERATION_STATUS;

// PC User Power Plan ENUM definitions
typedef enum _PWRCONS_USER_POWER_PLAN_ENUM
{
    PWRCONS_PLAN_CURRENT = 0,           // Current user power plan if get operation
    PWRCONS_PLAN_BEST_POWER_SAVINGS,    // PC ignores other input parameters, adjust for enabled features only
    PWRCONS_PLAN_BETTER_POWER_SAVINGS,  // PC ignores other input parameters, adjust for enabled features only
    PWRCONS_PLAN_GOOD_POWER_SAVINGS,    // PC ignores other input parameters, adjust for enabled features only
    PWRCONS_PLAN_DISABLE_POWER_SAVINGS, // PC ignores other input parameters, disables all power savings features
    PWRCONS_PLAN_CUSTOM,                // PC uses all input parameters for power savings adjustment
    NUM_OF_PWRCONS_USER_PLANS
} PWRCONS_USER_POWER_PLAN;

// PC Backlight Operation Inverter type enum
typedef enum _PWRCONS_BACKLIGHT_INVERTER_TYPE_ENUM
{
    BACKLIGHT_INVERTER_UNKNOWN,
    BACKLIGHT_INVERTER_I2C,
    BACKLIGHT_INVERTER_PWM,
    NUM_OF_BACKLIGHT_INVERTER_TYPE
} PWRCONS_BACKLIGHT_INVERTER_TYPE;

// PC LACE Aggressiveness type enum
typedef enum _DISPLAY_LACE_AGGRESSIVENESS_PROFILE
{
    DISPLAY_LACE_AGGRESSIVENESS_LOW = 0,
    DISPLAY_LACE_AGGRESSIVENESS_MODERATE,
    DISPLAY_LACE_AGGRESSIVENESS_HIGH,
    DISPLAY_LACE_AGGRESSIVENESS_NUM
} DISPLAY_LACE_AGGRESSIVENESS_PROFILE;

typedef enum _DD_ESC_WRITEBACK_FUN
{
    DD_ESC_WRITEBACK_CAPTURE_BUFFER = 107,
    DD_ESC_WRITEBACK_QUERY_MAX
} DD_ESC_WRITEBACK_FUN;

typedef enum _DD_CUI_ESC_CAPPED_FPS_OPCODE
{
    DD_CUI_ESC_GET_CAPPED_FPS,
    DD_CUI_ESC_SET_CAPPED_FPS,
} DD_CUI_ESC_CAPPED_FPS_OPCODE;

typedef enum _DD_CUI_ESC_CAPPED_FPS_STATE
{
    DD_CUI_ESC_CAPPED_FPS_STATE_DISABLE, // Disable RRC_ASYNC_FLIPS
    DD_CUI_ESC_CAPPED_FPS_STATE_ENABLE,  // Enable RRC_ASYNC_FLIPS
    DD_CUI_ESC_CAPPED_FPS_STATE_AUTO,    // Auto RRC_ASYNC_FLIPS based on Plan and Power source
} DD_CUI_ESC_CAPPED_FPS_STATE;

/* Structure to decode Target ID to identify Port details in Yangra */
typedef union _TARGET_ID {
    ULONG Value;
    struct
    {
        ULONG portType : 4;
        ULONG sinkType : 4;
        ULONG sinkIndex : 4;
        ULONG uniqueIndex : 5;
        ULONG reserved : 4;
        ULONG virtualDiplay : 1;
        ULONG tiledDisplay : 1;
        ULONG internalDisplay : 1;
        ULONG reservedForOS : 8;
    } bitInfo;
} TARGET_ID;

typedef enum _DD_CUI_ESC_NN_SCALING_OPCODE
{
    DD_CUI_ESC_GET_NN_SCALING_STATE, // get NN scaling state = 0
    DD_CUI_ESC_SET_NN_SCALING_STATE, // set NN scaling state = 1
} DD_CUI_ESC_NN_SCALING_OPCODE;

typedef enum _DD_CUI_ESC_NN_SCALING_STATE
{
    DD_CUI_ESC_NN_SCALING_DISABLE,           // Disable NN Scaling = 0
    DD_CUI_ESC_NN_SCALING_ENABLE,            // Enable NN Scaling = 1
    DD_CUI_ESC_FORCE_INTEGER_SCALING_ENABLE, // Force Integer Scaling = 2
} DD_CUI_ESC_NN_SCALING_STATE;

typedef enum _DD_CUI_ESC_CUSTOM_MODE_OPERATION
{
    DD_CUI_ESC_CUSTOM_MODE_GET_MODES,    // Get details of all previous applied custom modes if any
    DD_CUI_ESC_CUSTOM_MODE_ADD_MODES,    // Add a new mode
    DD_CUI_ESC_CUSTOM_MODE_REMOVE_MODES, // Remove previously applied custom mode
} DD_CUI_ESC_CUSTOM_MODE_OPERATION;

typedef enum _DD_CUI_ESC_CUSTOMMODE_ERRORCODES
{
    DD_CUI_ESC_CUSTOMMODE_NO_ERROR = 0,
    DD_CUI_ESC_CUSTOMMODE_INVALID_PARAMETER,
    DD_CUI_ESC_CUSTOMMODE_STANDARD_CUSTOM_MODE_EXISTS,
    DD_CUI_ESC_CUSTOMMODE_NON_CUSTOM_MATCHING_MODE_EXISTS,
    DD_CUI_ESC_CUSTOMMODE_INSUFFICIENT_MEMORY,
    DD_CUI_ESC_CUSTOMMODE_GENERIC_ERROR_CODE
} DD_CUI_ESC_CUSTOMMODE_ERRORCODES;

typedef struct _PWRCONS_FEATURES_REC
{
    DDU16 Reserved : 1; // Reserve for future use (Need to maintain bit positions for persistence of user settings).
    DDU16 DPST : 1;     // DPST
    DDU16 LACE : 1;     // LACE
    DDU16 CXSR : 1;     // Rapid Memory Management
    DDU16 FBC : 1;      // Smart 2D
    DDU16 GSV : 1;      // Graphics P States
    DDU16 DPS : 1;      // DRRS
    DDU16 RS : 1;       // Graphics Render Standby
    DDU16 PSR : 1;      // Panel PSR
    DDU16 IPS : 1;      // Intermediate Pixel Storage
    DDU16 SS : 1;       // Slice ShutDown
    DDU16 DFPS : 1;     // Dynamic FPS
    DDU16 ADT : 1;      // Assertive Display
    DDU16 PVQC : 1;     // ARC (Adaptive Rendering Control), a.k.a PVQC
    DDU16 DCC : 1;      // Duty Cycle Control
    DDU16 SLPM : 1;     // Single-loop Power Management
} PWRCONS_FEATURES;

typedef struct _PWRCONS_FEATURES_POLICY_REC
{
    OUT PWRCONS_FEATURES featuresTiedToPowerPlan;
    union {
        DDU32 featuresPolicy;
        struct
        {
            PWRCONS_FEATURES enabled;
            PWRCONS_FEATURES supported;
        };
    };
} PWRCONS_FEATURES_POLICY;

// DPST Feature Parameters
typedef struct _PWRCONS_DPST_PARAM_REC
{
    DDU32   numOfAvailableAggrLevel; // Set by PC to CUI in Get operation
    DDU32   userMaximumAggrLevel;    // Current/User select Maximum Aggressiveness level
    BOOLEAN isEPSMEnabled;           // (Enhanced Power Savings Mode) Indicates application of backlight ceiling for DPST 6.3
    BOOLEAN isEPSMSupported;         // Output parameter indicating that backlight ceiling is supported.

} PWRCONS_DPST_PARAM;

// Graphics P-States feature Parameters
typedef struct _PWRCONS_GFX_PSTATE_PARAM_REC
{
    DDU16 numOfAvailablePStates; // Sent by PC to CUI in Get operation
    union {
        DDU16 userMaximumPState; // Current/User-Select Maximum RP State
    };
} PWRCONS_GFX_PSTATE_PARAM;

typedef struct _PWRCONS_DPS_PARAM_REC
{
    BOOLEAN isMFD;                        // OUT - Set by PC to indicate whether or not MFD panel
    BOOLEAN isSupportForStaticDRRS;       // OUT - Set by PC to indicate whether or not Static DRRS is supported on seamless-switching platforms
    DDU32   numOfRefreshRates;            // OUT - Set by PC to reflect the number of refresh rates to expose in the minimum drop-down menu
    DDU32   dpsRefreshRate[MAX_DPSTATES]; // OUT - Set by PC to reflect the list of possible refresh rates to expose in the minimum drop-down menu
    DDU32   lastUserSelectedModeSetRR;    // OUT - Set by PC to reflect the last user-selected mode set refresh rate
    DDU32   baseLowRefreshRate;           // IN - User selection for Base Lo for the current SET event / OUT - Last user-selected Base Lo refresh rate
    DDU32   dpsParamsReturnCode;

} PWRCONS_DPS_PARAM;

typedef struct _PWRCONS_OP_FEATURE_SETTINGS_PARAM_REC
{
    DD_PWR_SRC_EVENT_ARGS    pwrSrcType;
    PWRCONS_FEATURES_POLICY  policy;
    PWRCONS_USER_POWER_PLAN  powerPlan;
    PWRCONS_DPST_PARAM       dpstParams;
    PWRCONS_GFX_PSTATE_PARAM gfxPStatesParam;
    PWRCONS_DPS_PARAM        dpsParams;

} PWRCONS_OP_FEATURE_SETTINGS_PARAM;

// Backlight operation parameters definition
typedef struct _PWRCONS_OP_BACKLIGHT_PARAM_REC
{
    PWRCONS_BACKLIGHT_INVERTER_TYPE inverterType;
    DDU32                           pwmInverterFrequency;
} PWRCONS_OP_BACKLIGHT_PARAM;

typedef struct _PWRCONS_OP_POWER_PLAN_PARAM_REC
{
    PWRCONS_USER_POWER_PLAN  userPowerPlan; // User Power Plan
    PWRCONS_FEATURES_POLICY  policy;
    PWRCONS_DPST_PARAM       dpstParams;
    PWRCONS_GFX_PSTATE_PARAM gfxPStatesParam;
    PWRCONS_DPS_PARAM        dpsParams;
} PWRCONS_OP_POWER_PLAN_PARAM;

// PC Operation Turbo Settings data structure definition
typedef struct _PWRCONS_OP_TURBO_PARAM_REC
{
    BOOLEAN isTurboSupported;
    BOOLEAN turboEnabled;
    BOOLEAN gfxInTurboState;
    DDU32   bias;
} PWRCONS_OP_TURBO_PARAM;

// PC Operation Turbo Overclocking Settings data structure definition
typedef struct _PWRCONS_OP_TURBO_OC_PARAM_REC
{
    BOOLEAN isTurboOcSupported;
    DDU32   ocMaxFrequency;
    DDU32   ocMaxVoltageOffset;
    DDU32   ocMinFrequency;
    BOOLEAN turboOcEnabled;
    DDU32   ocFrequency;
    DDU32   ocVoltageOffset;
} PWRCONS_OP_TURBO_OC_PARAM;

// PC Operation Assertive Display Ambient Light settings structure
typedef struct _PWRCONS_OP_AMBIENT_LIGHT_PARAM_REC
{
    DDU32                               lux;
    DDU32                               kelvin;
    DISPLAY_LACE_AGGRESSIVENESS_PROFILE defaultAggressivenessLevel;
    DISPLAY_LACE_AGGRESSIVENESS_PROFILE aggressivenessLevelFromCUI;
    union {
        DDU16 AlsOperation;
        struct
        {
            DDU16 luxOperation : 1;
            DDU16 aggressivenessLevelOperation : 1;
            DDU16 reserved : 14;
        };
    };
} PWRCONS_OP_AMBIENT_LIGHT_PARAM;

typedef struct _PWRCONS_OPERATION_PARAMS_REC
{
    union {
        PWRCONS_OP_FEATURE_SETTINGS_PARAM featureSettingsParam;
        PWRCONS_OP_BACKLIGHT_PARAM        backlightParam;
        PWRCONS_OP_POWER_PLAN_PARAM       powerPlanParam;
        PWRCONS_OP_TURBO_PARAM            turboParam;
        PWRCONS_OP_TURBO_OC_PARAM         turboOcParam;
        PWRCONS_OP_AMBIENT_LIGHT_PARAM    ambientLightParam;
    };
} PWRCONS_OPERATION_PARAMS;

#pragma pack(1)

typedef struct _DD_ESC_GET_VERSION_ARGS
{
    DDU8 MajorVer;
    DDU8 MinorVer;
} DD_ESC_GET_VERSION_ARGS;

typedef struct _DD_CUI_ESC_COLLAGE_TILE_INFO
{
    DDU32 childID;
    DDU8  hTileLocation;
    DDU8  vTileLocation;
    union {
        DDU32 tileBezelInformation;
        struct
        {
            DDU8 topBezelsize;
            DDU8 bottomBezelsize;
            DDU8 rightBezelsize;
            DDU8 leftBezelsize;
        };
    };
} DD_CUI_ESC_COLLAGE_TILE_INFO;

typedef struct _DD_CUI_ESC_COLLAGE_TOPOLOGY
{
    DDU8                         totalNumberOfHTiles;
    DDU8                         totalNumberOfVTiles;
    DD_CUI_ESC_COLLAGE_TILE_INFO collageChildInfo[DD_CUI_ESC_MAX_PHYSICAL_PIPES];
} DD_CUI_ESC_COLLAGE_TOPOLOGY, *PDD_CUI_ESC_COLLAGE_TOPOLOGY;

typedef struct _DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS
{
    DD_CUI_ESC_COLLAGE_OPERATION operation;
    DD_CUI_ESC_COLLAGE_TOPOLOGY  collageTopology;
    BOOLEAN                      collageSupported;
    BOOLEAN                      collageConfigPossible;
} DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS, *PDD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS;

typedef struct _DD_DISPLAY_FEATURE_SUPPORT
{
    BOOLEAN yCbCrSupport : 1;
    BOOLEAN relativeCSCSupport : 1;
} DD_DISPLAY_FEATURE_SUPPORT;

typedef struct _DD_CONNECTOR_INFO
{
    DD_CONNECTOR_TYPE          supportedConnectors;
    DD_CONNECTOR_TYPE          attachedConnectors;
    DD_CONNECTOR_TYPE          activeConnectors;
    DD_VIDEO_OUTPUT_TECHNOLOGY dongleDwnStreamPortType;
} DD_CONNECTOR_INFO;

/** HDCP Capabilities of Monitor and System */
typedef struct _DD_CUI_ESC_HDCP_VERSION_INFO
{
    DD_CUI_ESC_HDCP_VERSION monitorHdcpVersion;
    DD_CUI_ESC_HDCP_VERSION systemHdcpVersion;
} DD_CUI_ESC_HDCP_VERSION_INFO;

/** Max Resolution Supported and RR. */
typedef struct _DD_CUI_ESC_RESOLUTION
{
    DDU32 resX;
    DDU32 resY;
    DDU32 refreshRate;
} DD_CUI_ESC_RESOLUTION;

/** Resolution Capability of Monitor */
typedef struct _DD_CUI_RESOLUTION_CAPABILITIES
{
    DD_CUI_ESC_RESOLUTION             monitorMaxResolution;
    DD_CUI_ESC_MODE_ENUM_RESTRICTIONS restriction;
} DD_CUI_ESC_RESOLUTION_CAPABILITIES;

typedef struct _DD_CUI_DIAGNOSTIC_INFO
{
    DD_CUI_ESC_HDCP_VERSION_INFO       hdcpVersionInfo;
    DD_CUI_ESC_RESOLUTION_CAPABILITIES resolutionCaps;
} DD_CUI_ESC_DIAGNOSTIC_INFO;

typedef struct _DD_ESC_QUERY_DISPLAY_DETAILS_ARGS
{
    _In_ DDU32                 targetID;
    DD_DISPLAY_FEATURE_SUPPORT dispFtrSupport;
    DD_CONNECTOR_INFO          connectorInfo;
    DDU32                      sstDongleDwnStreamPortType;
    DDU32                      numPipesForTarget;
    DD_CUI_ESC_DIAGNOSTIC_INFO diagnosticInfo;
} DD_ESC_QUERY_DISPLAY_DETAILS_ARGS;

typedef union _DD_RGB_1010102 {
    DDU32 Value;
    struct
    {
        DDU32 Blue : DD_BITFIELD_RANGE(0, 9);
        DDU32 Green : DD_BITFIELD_RANGE(10, 19);
        DDU32 Red : DD_BITFIELD_RANGE(20, 29);
        DDU32 Reserved : DD_BITFIELD_RANGE(30, 31);
    };
} DD_RGB_1010102;

typedef struct _DD_COLOR_3DLUT_CONFIG
{
    DDU32                 size;
    DDU32                 targetID;
    BOOLEAN               enable;
    DD_COLOR_OPERATION    operation;
    DD_COLOR_3DLUT_STATUS status;
    DD_RGB_1010102        LUTData[DD_COLOR_3DLUT_NUM_SAMPLES];
} DD_COLOR_3DLUT_CONFIG;

typedef DD_COLOR_3DLUT_CONFIG DD_ESC_SET_3D_LUT_ARGS;

typedef struct _DD_ESC_GET_SET_COLOR_MODEL_ARGS
{
    DDU32              targetID;
    DD_COLOR_OPERATION operation;
    DD_COLOR_MODEL     colorModel;
} DD_ESC_GET_SET_COLOR_MODEL_ARGS;

typedef struct _DD_CUI_ESC_VRR_INFO
{
    DDU32 targetID;
    DDU32 minRr;
    DDU32 maxRr;
} DD_CUI_ESC_VRR_INFO;

typedef struct _DD_CUI_ESC_GET_SET_VRR_ARGS
{
    DD_CUI_ESC_VRR_OPERATION operation;                                 // Specifies operation to perform
    BOOLEAN                  vrrSupported;                              // Whether the feature is Supported for the platform or not (Static choice by OEM)
    BOOLEAN                  vrrEnabled;                                // Whether the feature is currently enabled or not (Dynamic choice by end user)
    BOOLEAN                  vrrHighFpsSolnEnabled;                     // Whether high FPS feature is currently enabled or not (Dynamic choice by end user)
    BOOLEAN                  vrrLowFpsSolnEnabled;                      // Whether low FPS feature is currently enabled or not (Dynamic choice by end user)
    DDU32                    numDisplays;                               // Number of connected displays that support VRR
    DD_CUI_ESC_VRR_INFO      escVrrInfo[DD_CUI_ESC_MAX_POSSIBLE_PIPES]; // VRR info for each display that supports VRR
} DD_CUI_ESC_GET_SET_VRR_ARGS, *PDD_CUI_ESC_GET_SET_VRR_ARGS;

typedef struct _DD_2DREGION
{
    DDU32 cX;
    DDU32 cY;
} DD_2DREGION;

/* Contains writeback escape HPD details*/
typedef struct _DD_ESC_WRITEBACK_HPD
{
    BOOLEAN     hotPlug;                  // Plug or Unplug
    DDU32       deviceID;                 // Target id of the device that is plugged in or needs unplug
    DD_2DREGION resolution;               // Mode
    HANDLE      wbSurfaceHandle;          // Surface Address input given by App
    HANDLE      notifyScreenCaptureEvent; // Screen capture Event that will be set when the capture is complete.
    BOOLEAN     OverrideDefaultEdid;
    DDU8        EdidData[WB_EDID_BLOCK_SIZE];
} DD_ESC_WRITEBACK_HPD;

typedef struct _DD_WRITEBACK_QUERY_ARGS
{
    BOOLEAN           isWbFeatureEnabled;                // INF is set or not
    BOOLEAN           wbPluggedIn[MAX_WRITEBACK_DEVICE]; // To get the status of Writeback device plugged in or not
    ULONG             deviceID[MAX_WRITEBACK_DEVICE];
    DD_2DREGION       currentResolution[MAX_WRITEBACK_DEVICE]; // Current Resolution if active
    DD_2DREGION       maxResolution;                           // Max Resolution supported
    WB_OPERATION_MODE operationMode;                           // OS/DFT mode for flip.
} DD_WRITEBACK_QUERY_ARGS;

typedef struct _DD_WB_BUFFER_INFO
{
    DD_2DREGION                resolution;
    DD_CUI_ESC_PIXELFORMAT     pixelFormat;
    DD_ESC_SURFACE_MEMORY_TYPE memoryFormat;
} DD_WB_BUFFER_INFO;

typedef struct _DD_WB_BUFFER_ARGS
{
    DDU32 bufferSize;
    DDU8 *pData;
} DD_WB_BUFFER_ARGS;

typedef struct _DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS
{
    DDU32                      deviceID;     // Child Id
    DD_2DREGION                resolution;   // Mode that is applied
    DD_CUI_ESC_PIXELFORMAT     pixelFormat;  // Pixel Format
    DD_ESC_SURFACE_MEMORY_TYPE memoryFormat; // tiling
    DDU32                      bufferSize;   // This will contain size of Buffer.Input can be 0 inorder to query the buffer size.
    DDU8                       wdBuffer[1];  // Will contain the captured buffer.
} DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS;

/** Structure used for edid escape*/
typedef struct _ESC_GET_EDID_ARGS
{
    IN ULONG displayID;
    IN ULONG edidBlockNum;
    IN UCHAR forceEDIDRead;
    OUT UCHAR edidData[EDID_BLOCK_SIZE];
} ESC_GET_EDID_ARGS, *PESC_GET_EDID_ARGS;

typedef union _DD_TAREGT_MODE_ID {
    DDU32 value;
    struct
    {
        DDU32 targetUniqueIndex : 8;
        DDU32 index : 24;
    };
} DD_TAREGT_MODE_ID;

typedef union _DD_CE_ASPECT_RATIO {
    DDU8 Value;
    struct
    {
        DDU8 isAviPar_4_3 : 1;
        DDU8 isAviPar_16_9 : 1;
        DDU8 isAviPar_64_27 : 1;
        DDU8 reservedCePar : 5;
    };
} DD_CE_ASPECT_RATIO;

typedef union _DD_SAMPLING_MODE {
    DDU8 Value;
    struct
    {
        DDU8 rgb : 1;
        DDU8 yuv420 : 1;
        DDU8 reserved : 6;
    };
} DD_SAMPLING_MODE;

typedef struct _DD_CE_DATA
{
    union {
        DDU8 value;
        struct
        {
            DDU8 pixelReplication : 5;
            DDU8 reservedCeData : 3;
        };
    };
    DD_SAMPLING_MODE   samplingMode;
    DD_CE_ASPECT_RATIO par[MAX_PARS_POSSIBLE_WITH_1_VIC];
    BOOLEAN            isNativeFormat[MAX_PARS_POSSIBLE_WITH_1_VIC];
    DDU8               vicId[MAX_PARS_POSSIBLE_WITH_1_VIC];
    DDU8               vicId4k2k;
} DD_CE_DATA;

typedef struct _DD_TIMING_FLAGS
{
    DD_CE_DATA ceData;
    DDU32      preferredMode : 1; // 1 - Preferred Mode
} DD_TIMING_FLAGS;

typedef struct _DD_TIMING_INFO
{
    DDU32             dotClock;     // Pixel clock in Hz
    DDU32             hTotal;       // Horizontal total in pixels
    DDU32             hActive;      // Active in pixels
    DDU32             hRefresh;     // Refresh Rate
    DDU32             vTotal;       // Vertical total in lines
    DDU32             vActive;      // Active lines
    DDU32             vRoundedRR;   // Refresh Rate
    BOOLEAN           isInterlaced; // 1 = Interlaced Mode
    DD_TIMING_FLAGS   flags;        // Timing Flags
    DD_TAREGT_MODE_ID modeId;       // Keep it at bottom as upper struct maps to pre defined timings values.
} DD_TIMING_INFO;

typedef union _DD_SCALING_SUPPORT {
    struct
    {
        DDU32 identity : 1;
        DDU32 centered : 1;
        DDU32 stretched : 1;
        DDU32 aspectRatioCenteredMax : 1;
        DDU32 custom : 1;
        DDU32 reserved : 27;
    };
    DDU32 scalingSupport;
} DD_SCALING_SUPPORT;

typedef struct _DD_SOURCE_MODE_INFO
{
    DDU32 visibleScreenX;
    DDU32 visibleScreenY;
    DDU32 pixelFormatMask;
    DDU8  numMappedTgtModes;
    DDU8  mappedTgtModeIndex[MAX_NUM_TARGET_MODE_PER_SOURCE_MODE];
} DD_SOURCE_MODE_INFO;

typedef struct _PINNED_MODE_INFO
{
    DDU32               targetID;
    DD_SOURCE_MODE_INFO sourceMode;
    DD_TIMING_INFO      targetMode;
} PINNED_MODE_INFO;

typedef struct _DD_ESC_QUERY_MODE_TABLE_ARGS
{
    PINNED_MODE_INFO   modeInfo[MAX_POSSIBLE_PIPES];
    DDU8               numPinnedTgt;
    DDU8               numSrcModes;
    DDU8               numTgtModes;
    DD_SCALING_SUPPORT scaling;
} DD_ESC_QUERY_MODE_TABLE_ARGS;

typedef struct _DD_I2C_AUX_ARGS
{
    DD_AUX_I2C_OPERATION operation;
    BOOLEAN              write;
    DD_PORT_TYPE         port;
    ULONG                address;
    ULONG                index;
    UCHAR                relAddress[MAX_BYTES_RAD];
    ULONG                readBytes;
    ULONG                writeBytes;
    ULONG                dataLength;
    UCHAR                data[MAX_LUT_AUX_BUFSIZE];
} DD_I2C_AUX_ARGS;

typedef struct _DD_ESC_AUX_I2C_ACCESS_ARGS
{
    DD_ESCAPE_STATUS status;
    DD_I2C_AUX_ARGS  i2cAuxArgs;
} DD_ESC_AUX_I2C_ACCESS_ARGS;

typedef struct _TURBO_POLICY_DATA_REC
{
    union {
        DDU32 turboPolicyData;
        struct
        {
            DDU16 enabled;   // User preference for the Platform Turbo feature (both GFX & CPU)
            DDU16 supported; // Whether the GFX portion of Turbo is allowed at all on the system
        };
    };
} TURBO_POLICY_DATA;

typedef struct _COM_ESC_POWER_CONSERVATION_ARGS
{
    BOOLEAN                  oldVersion;
    PWRCONS_OPERATION_TYPE   opType;
    DD_PWR_SRC_EVENT_ARGS    pwrSrcType;
    PWRCONS_OPERATION        operation;
    PWRCONS_OPERATION_STATUS opStatus;
    PWRCONS_OPERATION_PARAMS opParameters;
} COM_ESC_POWER_CONSERVATION_ARGS;

typedef struct _DD_CUI_ESC_GET_SET_CAPPED_FPS_ARGS
{
    DD_CUI_ESC_CAPPED_FPS_OPCODE OpCode;           // Specifies the operation
    DD_CUI_ESC_CAPPED_FPS_STATE  CappedFpsState;   // For Opcode Set/ Get
    BOOLEAN                      CappedFpsSupport; // This parameter reports platform support for Refresh rate Capped Async Flips
} DD_CUI_ESC_GET_SET_CAPPED_FPS_ARGS, *PDD_CUI_ESC_GET_SET_CAPPED_FPS_ARGS;

typedef struct _DD_ESC_SET_CUSTOM_SCALING_ARGS
{
    BOOLEAN Get;
    DDU32   TargetId;
    BOOLEAN Supported;
    BOOLEAN Enable;
    DDU8    CustomScalingX;
    DDU8    CustomScalingY;
} DD_ESC_SET_CUSTOM_SCALING_ARGS;

typedef struct _CAPI_TIMING
{
    DDU64 PixelClock;     ///< [out] Pixel Clock in Hz
    DDU32 HActive;        ///< [out] Horizontal Active
    DDU32 VActive;        ///< [out] Vertical Active
    DDU32 HTotal;         ///< [out] Horizontal Total
    DDU32 VTotal;         ///< [out] Vertical Total
    DDU32 HBlank;         ///< [out] Horizontal Blank
    DDU32 VBlank;         ///< [out] Vertical Blank
    DDU32 HSync;          ///< [out] Horizontal Blank
    DDU32 VSync;          ///< [out] Vertical Blank
    float RefreshRate;    ///< [out] Refresh Rate
    DDU32 SignalStandard; ///< [out] Signal Standard
    DDU8  VicId;
} CAPI_TIMING;

//------------------------------------------------------------------------------------------------------
// DD_CUI_ESC_SET_NEAREST_NEIGHBOUR(NN)_SCALING_ARGS
//------------------------------------------------------------------------------------------------------
typedef struct _NN_SCALING_SUPPORT
{
    BOOLEAN NNScalingFilterSupport;     // Enable Nearest Neighbour Scaling
    BOOLEAN ForceIntegerScalingSupport; // Force Scaling with Integer Multiples
} NN_SCALING_SUPPORT;

typedef struct _DD_CUI_ESC_GET_SET_NN_ARGS
{
    DD_CUI_ESC_NN_SCALING_OPCODE OpCode;           // Specifies the operation
    DD_CUI_ESC_NN_SCALING_STATE  NNScalingState;   // For Opcode Set/ Get
    NN_SCALING_SUPPORT           NNScalingSupport; // For Opcode Get
} DD_CUI_ESC_GET_SET_NN_ARGS;

//------------------------------------------------------------------------------------------------------
// DD_CUI_ESC_GET_SET_CUSTOM_MODE_ARGS
//------------------------------------------------------------------------------------------------------
typedef struct _DD_CUI_ESC_CUSTOM_SRC_MODE
{
    DDU32 SourceX; // CustomMode Source X Size
    DDU32 SourceY; // CustomMode Source Y Size
} DD_CUI_ESC_CUSTOM_SRC_MODE;

typedef struct _DD_CUI_ESC_GET_SET_CUSTOM_MODE_ARGS
{
    DDU32                            TargetId;     // Display for which custom mode is to be applied
    DD_CUI_ESC_CUSTOM_MODE_OPERATION CustomModeOp; // Kind of Operation to be done
    DD_CUI_ESC_CUSTOMMODE_ERRORCODES ErrCode;
    DDU8                             NumOfModes;
    DD_CUI_ESC_CUSTOM_SRC_MODE       SourceMode[3]; // Number of Custom Src Modes to be added/removed/Read.
} DD_CUI_ESC_GET_SET_CUSTOM_MODE_ARGS;

typedef enum _DD_CUI_ESC_COLOR_MATRIX_TYPE
{
    DD_CUI_ESC_COLOR_MATRIX_LINEAR     = 0, // Set the Matrix to operate on Linear Data
    DD_CUI_ESC_COLOR_MATRIX_NON_LINEAR = 1, // Set the Matrix to operate on Non-Linear Data
} DD_CUI_ESC_COLOR_MATRIX_TYPE;

typedef enum _DD_CUI_ESC_COLOR_OPERATION
{
    DD_CUI_ESC_COLOR_OPERATION_GET             = 0, // Get currently applied configuration
    DD_CUI_ESC_COLOR_OPERATION_SET             = 1, // Set given configuration
    DD_CUI_ESC_COLOR_OPERATION_RESTORE_DEFAULT = 2, // Restore driver to default settings,
    DD_CUI_ESC_COLOR_OPERATION_MAX
} DD_CUI_ESC_COLOR_OPERATION;

typedef union _DD_CUI_ESC_DDI15_16 {
    DDS32 value;
    struct
    {
        DDU32 fraction : DD_BITFIELD_RANGE(0, 15);
        DDU32 integer : DD_BITFIELD_RANGE(16, 30);
        DDU32 sign : DD_BITFIELD_BIT(31);
    };
} DD_CUI_ESC_DDI15_16;

typedef struct _DD_CUI_ESC_COLOR_PIPE_MATRIX_PARAMS
{
    BOOLEAN             enable;
    DD_CUI_ESC_DDI15_16 coefficients[DD_ESC_COLOR_MATRIX_NUM_COEFFICIENTS];
    DD_CUI_ESC_DDI15_16 preOffsets[DD_ESC_COLOR_MATRIX_NUM_OFFSET];
    DD_CUI_ESC_DDI15_16 postOffsets[DD_ESC_COLOR_MATRIX_NUM_OFFSET];
} DD_CUI_ESC_COLOR_PIPE_MATRIX_PARAMS, *PDD_CUI_ESC_COLOR_PIPE_MATRIX_PARAMS;

typedef struct _TEMP_CSC_PARAMS_
{
    INT   enable;
    DDS32 coefficients[DD_ESC_COLOR_MATRIX_NUM_COEFFICIENTS];
    DDS32 preOffsets[DD_ESC_COLOR_MATRIX_NUM_OFFSET];
    DDS32 postOffsets[DD_ESC_COLOR_MATRIX_NUM_OFFSET];
} CSC_PARAMS;

typedef struct _DD_CUI_ESC_COLOR_MATRIX_CONFIG
{
    DDU32                               size;     // Size of this structure
    DDU32                               targetId; // TagetId when communicating with user mode.
    DD_CUI_ESC_COLOR_OPERATION          operation;
    DD_CUI_ESC_COLOR_PIPE_MATRIX_PARAMS pipeMatrix;
    DD_CUI_ESC_COLOR_MATRIX_TYPE        matrixType;
} DD_CUI_ESC_COLOR_MATRIX_CONFIG, *PDD_CUI_ESC_COLOR_MATRIX_CONFIG;

//------------------------------------------------------------------------------------------------------
// DD_CUI_ESC_GET_SET_AVI_INFOFRAME_ARGS
//------------------------------------------------------------------------------------------------------
typedef struct _DD_CUI_ESC_AVI_IT_CONTENT_TYPE
{
    BOOLEAN GraphicsContent;
    BOOLEAN PhotoContent;
    BOOLEAN CinemaContent;
    BOOLEAN GameContent;
} DD_CUI_ESC_AVI_IT_CONTENT_TYPE;

typedef struct _DD_CUI_ESC_AVI_INFOFRAME_CUSTOM
{
    GUID                           Guid;          // GUID
    DDU32                          Command;       // Command
    DDU32                          Flags;         // Flags
    DDU32                          TypeCode;      // Type code of AVI Infoframe
    DDU32                          Length;        // Length of AVI Info Frame
    BOOLEAN                        ITContent;     // IT Content
    DDU8                           BarInfo[8];    // Reserved
    DDU32                          AspectRatio;   // Reserved
    DDU32                          QuantRange;    // Quantization Range
    DDU32                          ScanInfo;      // Scan Information
    DDU32                          ITContentType; // IT Content Type
    DD_CUI_ESC_AVI_IT_CONTENT_TYPE ITContentCaps; // IT Content Type Caps
} DD_CUI_ESC_AVI_INFOFRAME_CUSTOM;

typedef struct _DD_CUI_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME_ARGS
{
    DDU32                           TargetID;
    DD_COLOR_OPERATION              Operation;
    DD_CUI_ESC_AVI_INFOFRAME_CUSTOM AVIInfoFrame;
} DD_CUI_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME_ARGS;

//------------------------------------------------------------------------------------------------------
// DD_CAPI_ESC_GET_SET_GENLOCK_ARGS
//------------------------------------------------------------------------------------------------------

typedef enum _DD_CAPI_ESC_GENLOCK_OPERATION
{
    DD_CAPI_ESC_GENLOCK_OPERATION_GET_TIMING_DETAILS = 0, // Get details of GENLOCK support and timing information
    DD_CAPI_ESC_GENLOCK_OPERATION_VALIDATE,               // Driver to verify that the topology is Genlock capable
    DD_CAPI_ESC_GENLOCK_OPERATION_ENABLE,                 // Enable GENLOCK
    DD_CAPI_ESC_GENLOCK_OPERATION_DISABLE,                // Disable GENLOCK
    DD_CAPI_ESC_GENLOCK_OPERATION_GET_TOPOLOGY            // Get details of the current Genlock topology that is applied
} DD_CAPI_ESC_GENLOCK_OPERATION;

typedef struct _DD_CAPI_ESC_GENLOCK_DISPLAY_INFO
{
    DDU32   TargetId;
    BOOLEAN IsMaster;
    DDU64   VBlankTimeStamp;
    // For DP Displays
    DDU32 LinkRateMbps;
    DDU8  DpLaneWidthSelection;
} DD_CAPI_ESC_GENLOCK_DISPLAY_INFO;

typedef struct _DD_GENLOCK_TARGET_MODE_LIST
{
    DDU32 TargetId;
    DDU32 NumModes; // Number of modes for following TargetID.
                    // If NumModes==0 then we return the number of modes on this target
                    // If NumModes!=0 then we return the timing information for those modes.
    // Variable size data array below. To be used after verifying incoming buffer size.
    CAPI_TIMING *pTargetModes;
} DD_GENLOCK_TARGET_MODE_LIST;

typedef struct _DD_GENLOCK_TOPOLOGY
{
    DDU8                             NumGenlockDisplays;
    BOOLEAN                          IsMasterGenlockSystem;
    CAPI_TIMING                      CommonTargetModeTiming;
    DD_CAPI_ESC_GENLOCK_DISPLAY_INFO GenlockDisplayInfo[DD_CAPI_ESC_MAX_PHYSICAL_PIPES];
    DD_GENLOCK_TARGET_MODE_LIST      GenlockModeList[DD_CAPI_ESC_MAX_PHYSICAL_PIPES];
} DD_GENLOCK_DISPLAY_TOPOLOGY;

typedef struct _DD_CAPI_ESC_GET_SET_GENLOCK_ARGS
{
    DD_CAPI_ESC_GENLOCK_OPERATION Operation; // Specifies operation to perform
                                             // Below parameters applicable to "DD_GENLOCK_OPERATION_GET_INFO" ONLY
    DD_GENLOCK_DISPLAY_TOPOLOGY GenlockTopology;
    BOOLEAN                     IsGenlockSupported; // Whether the feature is Supported for the platform or not (Static choice by OEM)
    BOOLEAN                     IsGenlockEnabled;   // Whether the feature is currently enabled or not (Dynamic choice by end user)
    BOOLEAN                     IsGenlockPossible;  // Indicates if Genlock can be enabled/disable with the given topology
    DDU32                       LdaAdapterIndex;    // 0 = LDA primary or Non-LDA case
} DD_CAPI_ESC_GET_SET_GENLOCK_ARGS;

typedef struct _DD_CAPI_GET_VBLANK_TIMESTAMP_FOR_TARGET
{
    DDU32 TargetID; // Target ID for which VblankTs is required

    DDU8  NumOfTargets;
    DDU64 VblankTS[16]; // / Max supported Displays in SLS; 4 displays per GPU
} DD_CAPI_GET_VBLANK_TIMESTAMP_FOR_TARGET;

#pragma pack()

/* Private Function */
BOOLEAN YangraDpcdRead(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[]);
BOOLEAN YangraDpcdWrite(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[]);
BOOLEAN YangraGetEdidData(_In_ PANEL_INFO *pPanelInfo, _Out_ BYTE edidData[], _Out_ UINT *pNumEdidBlock);
BOOLEAN YangraGetMiscSystemInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Out_ MISC_ESC_GET_SYSTEM_INFO_ARGS *pMiscSystemInfo);
BOOLEAN YangraGetSetDPPHWLUT(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _In_ DD_ESC_SET_3D_LUT_ARGS *pDppHwLutInfo, _In_ ULONG *pDepth);
BOOLEAN YangraGetColorimetryInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Inout_ DD_ESC_QUERY_DISPLAY_DETAILS_ARGS *pQueryDisplayDetails);
BOOLEAN YangraSetColorimetryInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _In_ DD_ESC_GET_SET_COLOR_MODEL_ARGS colorModelArgs);
BOOLEAN YangraGetSetOutputFormat(_In_ PANEL_INFO *pPanelInfo, _Inout_ IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT *pGetSetOutputFormat);
BOOLEAN YangraConfigDxgkPowerComponent(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Inout_ MISC_ESC_DXGK_POWER_COMPONENT_ARGS *pDxgkPowerCompArgs);
