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
* @file DisplayErrorDef.h
* @brief List of Display error codes to be used by 3 layers of Display driver
*
*
*
*********************************************************************
**/
#ifndef _DISPLAY_ERROR_H_
#define _DISPLAY_ERROR_H_

#define DD_ERROR_CODE_VER 1 // bump up rev when we modify the file

/**
 * \brief @c DDSTATUS error code used across all display driver modules to return
 * function status
 *
 * The error code has below major categories
 * 1. generic failure
 * 2. DSL (Display OS Layer) error
 * 3. DPL (Display Protocol layer) error
 * 4. DHL (Display HW-Abstraction layer) error
 * 5. Success codes
 */
typedef enum _DDSTATUS
{
    /////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////
    //
    //      start of generic failure codes   0x8000 0000 - 0x8000 00FF
    //
    /////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////
    DDS_UNSUCCESSFUL = 0x80000000, // -2147483648
    DDS_NO_MEMORY,
    DDS_INVALID_PARAM,
    DDS_NULL_PARAM,
    DDS_TIMEOUT,
    DDS_I2C_DEVICE_DOES_NOT_EXIST,
    DDS_I2C_DATA_READ_ERROR,
    DDS_I2C_DATA_WRITE_ERROR,
    DDS_BUFFER_TOO_SMALL,
    DDS_BUFFER_OVERFLOW,
    DDS_SET_TIMING_MONITOR_NOT_CONNECTED,
    DDS_ERROR_UNKNOWN,
    DDS_BUSY,
    DDS_NOT_SUPPORTED,
    DDS_DATA_OVERFLOW,
    DDS_DEVICE_NOT_READY,
    DDS_MONITOR_NOT_CONNECTED,
    DDS_INTERFACE_NOT_IMPLEMENTED,
    DDS_INVALID_DATA,
    DDS_INVALID_CONTEXT,
    DDS_DATA_ERROR,
    DDS_INVALID_LEVEL,
    DDS_INVALID_OPERATION,
    DDS_CRC_ERROR,
    DDS_LOCKING_FAILURE,
    DDS_NACK_RECVD,
    DDS_NO_RESOURCE,
    DDS_INVALID_ESC_VER,
    DDS_INVALID_REQ,
    DDS_USER_APC,
    DDS_ABANDONED,
    DDS_NO_RECOMMEND_FUNCTIONAL_VIDPN,
    DDS_MONITOR_NO_MORE_DESCRIPTOR_DATA,
    DDS_MONITOR_NO_DESCRIPTOR_DATA,
    // add new generic failure code above this line
    __DD_STATUS_RANGE_GENERIC_FAILURE_MAX, // max allowed value = 0x80000100, // range limit, *not* to be used in coding
                                           /////////////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////
    //
    //      start of DSL status codes        0x8000 0102 - 0x8FFF FFFF
    //
    /////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////
    __DD_STATUS_RANGE_DSL_START = 0x80000101, // range limit, *not* to be used in coding
    DDS_INVALID_PC_EVENT,
    // add new DSL error code above this line
    __DD_STATUS_RANGE_DSL_MAX, // max allowed value = 0x90000000, // range limit, *not* to be used in coding
                               /////////////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////
    //
    //      start of protocol status codes   0x90000002 - 0x9FFF FFFF
    //
    /////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////
    __DD_STATUS_RANGE_DPL_START = 0x90000001, // range limit, *not* to be used in coding
    DDS_DPL_VBT_PARSING_ERROR,
    DDS_DPL_INVALID_MONITOR_DESC_TAG,
    DDS_DPL_INVALID_VIC_ID,
    DDS_DPL_INVALID_VBT_VERSION,
    DDS_DPL_DETECTION_INCOMPLETE,
    DDS_DPL_INVALID_PORT,
    DDS_DPL_INVALID_PIPE,
    DDS_DPL_INVALID_PROTOCOL,
    DDS_DPL_INVALID_CONNECTOR,
    DDS_DPL_FAILED_HAL_PROGRAMMING,
    DDS_DPL_INVALID_HAL_DATA,
    DDS_DPL_FAILED_EDID_READ,
    DDS_DPL_EDID_PARSE_ERROR,
    DDS_DPL_NO_SINK,

    // DP Protocol error codes  ------- {{{
    DDS_DPL_DP_AUX_FAILURE,
    // link training related
    DDS_DPL_DP_INVALID_LINK_RATE,
    DDS_DPL_DP_INVALID_LANE_COUNT,
    DDS_DPL_DP_LINK_TRAINING_FAILED,
    DDS_DPL_DP_LT_CLOCK_RECOVERY_FAILED,
    DDS_DPL_DP_LT_FAILED_TO_GET_NEXT_LINKRATE,
    DDS_DPL_DP_LT_MAX_CLK_REC_ITER_REACHED,
    DDS_DPL_DP_LT_CHAN_EQ_FAILED,
    DDS_DPL_DP_LT_MAX_EQ_ITER_REACHED,
    DDS_DPL_DP_GET_REQUESTED_DRIVE_SETTING_FAILED,
    DDS_DPL_DP_ADJUST_DRIVE_SETTING_FAILED,
    DDS_DPL_DP_INSUFFICIENT_LINK_BW,
    DDS_DPL_DP_FAILED_LINK_CONFIG_SET,
    DDS_DPL_DP_FAILED_SET_ASSR_CFG,
    DDS_DPL_DP_FAILED_DPCD_READ,
    DDS_DPL_DP_FAILED_DPCD_WRITE,
    DDS_DPL_DP_LINK_LOST,
    DDS_DPL_DP_LINK_LOST_POST_MODESET,
    DDS_DPL_DP_LQA_FAILED,
    DDS_DPL_DP_ACT_HANDLING_ERROR,
    DDS_DPL_DP_PREPARE_FOR_ENABLE_FAILED,
    // sideband related
    DDS_DPL_DP_SIDEBAND_MSG_ID_MISMATCH,
    DDS_DPL_DP_SIDEBAND_INVALID_RAD,
    DDS_DPL_DP_SIDEBAND_INVALID_HEADER,
    DDS_DPL_DP_SIDEBAND_SEND_MSG_FAILURE,
    DDS_DPL_DP_SIDEBAND_REPLY_TIMEOUT,
    DDS_DPL_DP_SIDEBAND_INVALID_REPLY,
    DDS_DPL_DP_SIDEBAND_READ_MSG_FAILURE,
    //----------------------------- }}}
    DDS_DPL_HDCP_REVOKED_DEVICE_ATTACHED,
    DDS_DPL_HDCP_INVALID_KSV,

    //***********************************************************************
    // HDCP Protocol error codes
    //
    //
    DDS_DPL_HDCP_LINK_INTEGRITY_FAILED,

    // stream / BANDWIDTH related
    DDS_DPL_FAILED_TO_ENABLE_STREAM,
    DDS_DPL_FAILED_SET_BANDWIDTH,

    // HDMI protocol related
    DDS_DPL_HDMI_INVALID_SINK_VERSION,
    DDS_DPL_HDMI_SCRAMBLING_ENABLE_FAILED,

    // EDP PSR Sepcific
    DDS_SINK_PSR_NOTSUPPORTED,
    DDS_GTC_SET_CONTROL_FAILED,
    DDS_PSR_DISABLE_FAILED,
    DDS_PSR_CONTEXT_NOT_INITIALIZED,

    // add new protocol success code above this line
    __DD_STATUS_RANGE_DPL_MAX = 0xA0000000, // range limit, *not* to be used in coding
                                            /////////////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////
    //
    //      start of HAL status codes        0xA000 0002 - 0xFFFFFFFE
    //
    /////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////
    __DD_STATUS_RANGE_DHL_START = 0xA0000001, // range limit, *not* to be used in coding
    DDS_DHL_INTERFACE_UNSUPPORTED_ON_GEN,
    DDS_DHL_INVALID_PORT,
    DDS_DHL_INVALID_PIPE,
    DDS_DHL_INVALID_PLANE,
    DDS_DHL_INVALID_TRANSPORT,
    DDS_DHL_PPS_ERROR,
    DDS_DHL_INVALID_DIP_TYPE,
    DDS_DHL_INVALID_CDCLOCK_FREQ,
    DDS_DHL_INVALID_VOLTAGE_INFO,
    DDS_DHL_INVALID_DMC_FW_SIZE,
    DDS_DHL_INVALID_IRQL,
    DDS_DHL_INVALID_DC_STATE,

    DDS_DHL_AUX_BUSY,
    DDS_DHL_AUX_UNKNOWN,
    DDS_DHL_AUX_NOTSUPPORTED,
    DDS_DHL_AUX_OPEN,
    DDS_DHL_AUX_DATA_READ_ERROR,
    DDS_DHL_AUX_DATA_WRITE_ERROR,
    DDS_DHL_AUX_INVALID_CHANNEL,
    DDS_DHL_AUX_MORE_DATA,
    DDS_DHL_AUX_DEFER,
    DDS_DHL_AUX_TIMEOUT,

    DDS_DHL_I2C_BUSY,
    DDS_DHL_I2C_NACK_RECIEVED,
    DDS_DHL_I2C_TIMEOUT,
    DDS_DHL_I2C_NOTSUPPORTED,
    DDS_DHL_I2C_ERROR_OPEN,
    DDS_DHL_I2C_ERROR_CLOSE,
    DDS_DHL_I2C_ERROR_SEGMENT_POINTER_WRITE,
    DDS_DHL_I2C_INVALID_PARAM,

    DDS_DHL_TRANS_INVALID_TIMINGS,
    DDS_DHL_TRANS_INVALID_PARAM,
    DDS_DHL_TRANS_TIMEOUT,

    DDS_DHL_DBUF_PWRSTATE_ERROR,

    DDS_PG_DISTRIB_ERROR,
    DDS_PG_NOT_POWERED,
    DDS_PG_INVALID_PARAM,

    DDS_PIPE_INVALID_PIPE_SRCSZ,

    DDS_PLL_NOT_LOCKED,
    DDS_PLL_NOT_UNLOCKED,
    DDS_PLL_POWER_NOT_ENABLED,
    DDS_PLL_POWER_NOT_DISABLED,
    DDS_PLL_INVALID_LINK_RATE,
    DDS_PLL_INVALID_PLL,
    DDS_PLL_INVALID_DIVIDERS,

    DDS_DHL_PORT_INVALID_PATTERN,
    DDS_DHL_PORT_INVALID_DRIVE_SETTING,
    DDS_DHL_PORT_DISABLE_TIMEOUT,
    DDS_DHL_PORT_BUFFER_IDLE,
    DDS_DHL_PORT_INVALID_LANES,
    DDS_DHL_PORT_DP_ACT_SENT_ERROR,
    DDS_DHL_PORT_DP_ACT_HANDLING_ERROR,
    DDS_DHL_PORT_POWERUP_LANE_FAILED,
    DDS_DHL_PORT_POWERDOWN_LANE_FAILED,

    DDS_DHL_RM_NUM_PLANE_EXCEEDS_LIMIT,
    DDS_DHL_RM_NUM_SCALARS_EXCEEDS_LIMIT,
    DDS_DHL_RM_INVALID_PIXEL_FORMAT,
    DDS_DHL_RM_INVALID_PLANE_INDEX,
    DDS_DHL_RM_ASYNC_FLIP_NOT_SUPPORTED,
    DDS_DHL_RM_ASYNC_FLIP_HW_RESTRICTION_NOT_MET,
    DDS_DHL_RM_ALPHA_BLEND_NOT_SUPPORTED,
    DDS_DHL_RM_SURF_WIDTH_HEIGHT_HW_RESTRICTION_NOT_MET,
    DDS_DHL_RM_SURF_SIZE_HW_RESTRICTION_NOT_MET,
    DDS_DHL_RM_AUX_SURF_HW_RESTRICTION_NOT_MET,
    DDS_DHL_RM_SURF_OFFSET_HW_RESTRICTION_NOT_MET,
    DDS_DHL_RM_VFLIP_NOT_SUPPORTED,
    DDS_DHL_RM_VFLIP_HW_RESTRICTION_NOT_MET,
    DDS_DHL_RM_HFLIP_NOT_SUPPORTED,
    DDS_DHL_RM_HFLIP_HW_RESTRICTION_NOT_MET,
    DDS_DHL_RM_ROTATION_NOT_SUPPORTED,
    DDS_DHL_RM_ROTATION_HW_RESTRICTION_NOT_MET,
    DDS_DHL_RM_SCALE_NOT_SUPPORTED,
    DDS_DHL_RM_SCALE_HW_RESTRICTION_NOT_MET,
    DDS_DHL_RM_HIGH_Q_SCALE_NOT_SUPPORTED,
    DDS_DHL_RM_BILINEAR_SCALE_NOT_SUPPORTED,
    DDS_DHL_RM_HORZ_STRETCH_FACTOR_EXCEEDS_LIMIT,
    DDS_DHL_RM_HORZ_SHRINK_FACTOR_EXCEEDS_LIMIT,
    DDS_DHL_RM_VERT_STRETCH_FACTOR_EXCEEDS_LIMIT,
    DDS_DHL_RM_VERT_SHRINK_FACTOR_EXCEEDS_LIMIT,
    DDS_DHL_RM_COLOR_CONFIG_NOT_SUPPORTED,
    DDS_DHL_HDCP_AUTH_FAILURE,
    DDS_DHL_HDCP_ENCRYPTION_FAILURE,
    DDS_DHL_HDCP_KEYLOAD_FAILURE,
    DDS_DHL_HDCP_AN_GENERATION_FAILURE,
    DDS_DHL_HDCP_BKSV_UPDATE_FAILURE,
    DDS_DHL_HDCP_RI_NOT_READY,
    DDS_DHL_HDCP_RI_MISMATCH,
    DDS_DHL_HDCP_REPEATER_STATE_UPDATE_FAILURE,
    DDS_DHL_HDCP_COMPUTE_V_FAILURE,
    DDS_DHL_HDCP_VPRIME_MISMATCH,
    DDS_DHL_INVALID_PWMCTRL_TYPE,

    DDS_DHL_RM_WM_EXCEEDED_FIFO,
    DDS_DHL_RM_DBUF_EXCEEDED_PIPE_ALLOC,
    DDS_DHL_3D_LUT_INVALID_PIPE,
    // add new HAL error code above this line
    __DD_STATUS_RANGE_DHL_MAX, // max allowed value = 0xFFFFFFFF, // range limit, *not* to be used in coding
                               /////////////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////
    //
    //      start of generic success codes   0 - 0x7FFF FFFE
    //
    /////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////
    DDS_SUCCESS = 0,
    DDS_MORE_ENTRIES,
    DDS_NO_ACTION_REQUIRED,
    DDS_SUCCESS_ENTRY_EXISTS_NO_UPDATE,
    DDS_SUCCESS_ENTRY_EXISTS_REPLACED,
    DDS_SUCCESS_ENTRY_NEW_ADDED,
    DDS_SUCCESS_MODE_INTERLACE_MODE_REMOVED_BY_OEM,
    DDS_SUCCESS_MODE_NO_PIXEL_FORMAT_SUPPORTED,
    DDS_CE_EXTN_BLOCK_NOT_FOUND,
    DDS_DISPLAY_ID_BLOCK_NOT_FOUND,
    DDS_HDMI_VSDB_BLOCK_NOT_FOUND,
    DDS_CE_EXTN_DTD_NOT_FOUND,
    DDS_CE_EXTN_S3D_MODES_NOT_PRESENT,
    DDS_DPL_TIMING_NOT_SUPPORTED,
    DDS_DPL_HDMI2_0_SCDC_NOT_SUPPORTED,
    DDS_PSR_ALREADY_ENABLED,
    DDS_PSR_ALREADY_DISABLED,

    DDS_STATUS_PENDING,
    DDS_HDCP1_ENCRYPTING_RI_YET_TO_MATCH,
    DDS_DPST_UNSUPPORTED_CONFIGURATION,
    // add new generic success code above this line
    __DD_STATUS_RANGE_GENERIC_SUCCESS_MAX // max value allowed = 0x7FFFFFFF, // range limit, *not* to be used in coding
                                          /////////////////////////////////////////////////////////////////////////
} DDSTATUS;

C_ASSERT(__DD_STATUS_RANGE_GENERIC_FAILURE_MAX < __DD_STATUS_RANGE_DSL_START);
C_ASSERT(__DD_STATUS_RANGE_DSL_MAX < __DD_STATUS_RANGE_DPL_START);
C_ASSERT(__DD_STATUS_RANGE_DPL_MAX < __DD_STATUS_RANGE_DHL_START);
C_ASSERT(__DD_STATUS_RANGE_DHL_MAX < DDS_SUCCESS);
C_ASSERT(__DD_STATUS_RANGE_GENERIC_SUCCESS_MAX > DDS_SUCCESS && __DD_STATUS_RANGE_GENERIC_SUCCESS_MAX <= 0x7FFFFFFF);

/////////////////////////////////////////////////////////////////////////
//
// error code handling macros
//

/// returns true if @c Err is a success code
#define IS_DDSTATUS_SUCCESS(Err) (((DDSTATUS)(Err)) >= DDS_SUCCESS)

/** returns true if @c Err is not a success code */
#define IS_DDSTATUS_ERROR(Err) (((DDSTATUS)(Err)) < DDS_SUCCESS)

/**
 * \brief Returns TRUE if @c Status is Display OS Layer error code
 * \param  Status is the @c DDSTATUS code
 * \return true or false
 */
DD_S_INLINE BOOLEAN _IsDslError(DDSTATUS Status)
{
    return ((Status > __DD_STATUS_RANGE_GENERIC_FAILURE_MAX) && (Status < __DD_STATUS_RANGE_DSL_MAX));
}

/**
 * \brief Returns TRUE if @c Status is Display Protocol Layer error code
 * \param  Status is the @c DDSTATUS code
 * \return true or false
 */
DD_S_INLINE BOOLEAN _IsDplError(DDSTATUS Status)
{
    return ((Status > __DD_STATUS_RANGE_DSL_MAX) && (Status < __DD_STATUS_RANGE_DPL_MAX));
}

/**
 * \brief Returns TRUE if @c Status is Display HW Abstraction Layer error code
 * \param  Status is the @c DDSTATUS code
 * \return true or false
 */
DD_S_INLINE BOOLEAN _IsDhlError(DDSTATUS Status)
{
    return ((Status > __DD_STATUS_RANGE_DPL_MAX) && (Status < __DD_STATUS_RANGE_DHL_MAX));
}

#if _DEBUG || _RELEASE_INTERNAL
#define DDASSERT(expr) \
    if (!(expr))       \
    __debugbreak()
//#define DDASSERT_RET(expr, ...) \
//    do { if (!(expr)) {__debugbreak();return __VA_ARGS__;} } while(0)
#else
#define DDASSERT(expr) // if (!(expr)) __debugbreak()
//#define DDASSERT_RET(expr, ...) \
//    if (!(expr)) return __VA_ARGS__
#endif
/// return Status if Status is not DDS_SUCCESS
#define RETURN_STATUS_IF_NOT_SUCCESS(eStatus) \
    if ((eStatus != DDS_SUCCESS))             \
    {                                         \
        return eStatus;                       \
    }

/////////////////////////////////////////////////////////////////////////

#endif // _DISPLAY_ERROR_H_
