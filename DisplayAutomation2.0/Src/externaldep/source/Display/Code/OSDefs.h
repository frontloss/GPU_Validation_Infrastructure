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
;   File Name: OSDefs.h

;   File Description:
;       This file contains enums defined in OS WDK in C++ syntax, since our
;   driver code is in "C", so need to redefine here in C syntax to avoid
;   using magic numbers in code. Make sure this is same as OS structs/enums
;--------------------------------------------------------------------------*/
#pragma once

typedef enum _DXGK_CONNECTION_STATES
{
    DXGK_CS_UNINITIALIZED = 0,

    DXGK_CS_TARGET_STATUS_DISCONNECTED = 4,
    DXGK_CS_TARGET_STATUS_CONNECTED,
    DXGK_CS_TARGET_STATUS_JOINED,

    DXGK_CS_MONITOR_STATUS_DISCONNECTED = 8,
    DXGK_CS_MONITOR_STATUS_UNKNOWN,
    DXGK_CS_MONITOR_STATUS_CONNECTED,

    DXGK_CS_LINK_CONFIGURATION_STARTED = 12,
    DXGK_CS_LINK_CONFIGURATION_FAILED,
    DXGK_CS_LINK_CONFIGURATION_SUCCEEDED
} DXGK_CONNECTION_STATES;

typedef enum _DXGK_DISPLAY_DETECT_CONTROL_TYPE
{
    DXGK_DDC_TYPE_UNINITIALIZED = 0,
    DXGK_DDC_TYPE_POLL_ONE,
    DXGK_DDC_TYPE_POLL_ALL,
    DXGK_DDC_TYPE_ENABLE_HPD,
    DXGK_DDC_TYPE_DISABLE_HPD
} DXGK_DISPLAY_DETECT_CONTROL_TYPE;

typedef enum _DXGK_DISPLAY_PANEL_ORIENTATION
{
    DXGK_DPO_0_DEGREE = 0,
    DXGK_DPO_90_DEGREE,
    DXGK_DPO_180_DEGREE,
    DXGK_DPO_270_DEGREE
} DXGK_DISPLAY_PANEL_ORIENTATION;

typedef enum _DXGK_DISPLAY_DESCRIPTOR
{
    DXGK_DD_TYPE_INVALID = 0,
    DXGK_DD_TYPE_EDID
} DXGK_DISPLAY_DESCRIPTOR;

typedef enum _DXGK_DISPLAY_TECHNOLOGY_TYPE
{
    DXGK_DTT_INVALID = 0,
    DXGK_DTT_OTHER,
    DXGK_DTT_LCD,
    DXGK_DTT_OLED
} DXGK_DISPLAY_TECHNOLOGY_TYPE;

typedef enum _DXGK_DISPLAY_USAGE_TYPE
{
    DXGK_DUT_INVALID = 0,
    DXGK_DUT_GENERIC,
    DXGK_DUT_AUXILIARY,
    DXGK_DUT_AR,
    DXGK_DUT_VR
} DXGK_DISPLAY_USAGE_TYPE;

typedef enum _DXGK_GLITCH_CAUSE_TYPE
{
    DXGK_GLITCH_CAUSE_TYPE_DRIVER_ERROR        = 0,
    DXGK_GLITCH_CAUSE_TYPE_TIMING_CHANGE       = 1,
    DXGK_GLITCH_CAUSE_TYPE_PIPELINE_CHANGE     = 2,
    DXGK_GLITCH_CAUSE_TYPE_MEMORY_TIMING       = 3,
    DXGK_GLITCH_CAUSE_TYPE_ENCODER_RECONFIG    = 4,
    DXGK_GLITCH_CAUSE_TYPE_MODIFIED_WIRE_USAGE = 5,
    DXGK_GLITCH_CAUSE_TYPE_METADATA_CHANGE     = 6,
    DXGK_GLITCH_CAUSE_TYPE_NONE                = 255
} DXGK_GLITCH_CAUSE_TYPE;

typedef enum _DXGK_GLITCH_EFFECT_TYPE
{
    DXGK_GLITCH_EFFECT_TYPE_SYNC_LOSS        = 0,
    DXGK_GLITCH_EFFECT_TYPE_GARBAGE_CONTENT  = 1,
    DXGK_GLITCH_EFFECT_TYPE_STALE_CONTENT    = 2,
    DXGK_GLITCH_EFFECT_TYPE_BLACK_CONTENT    = 3,
    DXGK_GLITCH_EFFECT_TYPE_DEGRADED_CONTENT = 4,
    DXGK_GLITCH_EFFECT_TYPE_SEAMLESS         = 255
} DXGK_GLITCH_EFFECT_TYPE;

typedef enum _DXGK_GLITCH_DURATION_TYPE
{
    DXGK_GLITCH_DURATION_TYPE_INDEFINITE   = 0,
    DXGK_GLITCH_DURATION_TYPE_MULTI_FRAME  = 1,
    DXGK_GLITCH_DURATION_TYPE_SINGLE_FRAME = 2,
    DXGK_GLITCH_DURATION_TYPE_MULTI_LINE   = 3,
    DXGK_GLITCH_DURATION_TYPE_SINGLE_LINE  = 4,
    DXGK_GLITCH_DURATION_TYPE_NONE         = 255
} DXGK_GLITCH_DURATION_TYPE;
