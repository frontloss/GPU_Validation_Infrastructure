/*------------------------------------------------------------------------------------------------*
 *
 * @file     YangraDisplayEscape.h
 * @brief    This file contains Implementation of YangraDpcdRead, YangraDpcdWrite
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "EscapeSharedHeader.h"

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

typedef enum _DD_CONNECTOR_TYPE
{
    DD_CONNECTOR_NONE,
    DD_CONNECTOR_EDP,
    DD_CONNECTOR_DP,
    DD_CONNECTOR_HDMI,
    DD_CONNECTOR_DVI,
    DD_CONNECTOR_MIPI
} DD_CONNECTOR_TYPE;

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

#pragma pack(1)

typedef struct _DD_ESC_GET_VERSION_ARGS
{
    DDU8 MajorVer;
    DDU8 MinorVer;
} DD_ESC_GET_VERSION_ARGS;

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

#pragma pack()

/* Private Function */
BOOLEAN YangraDpcdRead(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[]);
BOOLEAN YangraDpcdWrite(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[]);
