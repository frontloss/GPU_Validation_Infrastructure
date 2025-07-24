/**
 * @file
 * @section WritebackUtilityDetails_h
 * @brief Internal header file which contains data structures and helper function required for escape call
 * related functionality and writeback functionalities
 *
 * @ref WritebackUtilityDetails.h
 * @author Reeju Srivastava, Ankurkumar Patel
 */

/**********************************************************************************
 * INTEL CONFIDENTIAL. Copyright (c) 2016 Intel Corporation All Rights Reserved.
 *  <br>The source code contained or described herein and all documents related to the source code
 *  ("Material") are owned by Intel Corporation or its suppliers or licensors. Title to the
 *  Material remains with Intel Corporation or its suppliers and licensors. The Material contains
 *  trade secrets and proprietary and confidential information of Intel or its suppliers and licensors.
 *  The Material is protected by worldwide copyright and trade secret laws and treaty provisions.
 *  No part of the Material may be used, copied, reproduced, modified, published, uploaded, posted,
 *  transmitted, distributed, or disclosed in any way without Intel’s prior express written permission.
 *  <br>No license under any patent, copyright, trade secret or other intellectual property right is
 *  granted to or conferred upon you by disclosure or delivery of the Materials, either expressly,
 *  by implication, inducement, estoppel or otherwise. Any license under such intellectual property
 *  rights must be express and approved by Intel in writing.
 */

#pragma once

/* System define header(s)*/
#include <d3dkmthk.h>
#include <stdio.h>

/* User define header(s)*/
#include "WritebackUtility.h"

/* Constants numbers*/
#define MAX_WRITEBACK_DEVICE 2
#define MinorEscVersion 2
#define MajorEscVersion 2
#define GDI32_LIB L"gdi32.dll"
#define SET_PTR(p, n) ((void *)((char *)(p) + (n)))
#define FILE_SIZE 124

#pragma pack(push, 1)

typedef enum _DD_ESC_WRITEBACK_FUN
{
    DD_ESC_WRITEBACK_QUERY          = 105,
    DD_ESC_WRITEBACK_ENABLE_DISABLE = 106,
    DD_ESC_WRITEBACK_CAPTURE_BUFFER = 107,
    DD_ESC_WRITEBACK_QUERY_MAX
} DD_ESC_WRITEBACK_FUN;

typedef enum _WB_OPERATION_MODE
{
    WB_OS_MODE,
    WB_DFT_MODE,
} WB_OPERATION_MODE;

typedef enum _PLUG_ACTIONS
{
    UNPLUG_WB,
    PLUG_WB,
    MAX_ACTION
} PLUG_ACTIONS;

typedef struct _DD_WRITEBACK_QUERY_ARGS
{
    BOOLEAN           IsWbFeatureEnabled;                // INF is set or not
    BOOLEAN           WbPluggedIn[MAX_WRITEBACK_DEVICE]; // To get the status of Writeback device plugged in or not
    ULONG             DeviceId[MAX_WRITEBACK_DEVICE];
    WB_MODE           CurrentResolution[MAX_WRITEBACK_DEVICE]; // Current Resolution if active
    WB_MODE           MaxResolution;                           // Max Resolution supported
    WB_OPERATION_MODE OperationMode;                           // OS/DFT mode for flip.
} DD_WRITEBACK_QUERY_ARGS;

typedef struct _DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS
{
    DDU32                      DeviceId;     // Child Id
    WB_MODE                    Resolution;   // Mode that is applied
    DD_CUI_ESC_PIXELFORMAT     PixelFormat;  // Pixel Format
    DD_ESC_SURFACE_MEMORY_TYPE MemoryFormat; // tiling
    DDU32                      BufferSize;   // This will contain size of Buffer.Input can be 0 inorder to query the buffer size.
    DDU8                       WdBuffer[1];  // Will contain the captured buffer.
} DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS;

#pragma pack(pop)

/* Structure definition for escpae opcode details*/
typedef struct _ESCAPE_OPCODES
{
    _In_ INT MajorEscapeCode;
    _In_ INT MinorEscapeCode;
    _In_ SHORT MinorInterfaceVersion;
    _In_ SHORT MajorInterfaceVersion;
} ESCAPE_OPCODES;

/* Enum contains details of gfx escape opcodes*/
typedef enum
{
    GFX_ESCAPE_CODE_DEBUG_CONTROL = 0L, // DO NOT CHANGE
    GFX_ESCAPE_DISPLAY_CONTROL,
    GFX_ESCAPE_CUICOM_CONTROL = GFX_ESCAPE_DISPLAY_CONTROL,
    GFX_ESCAPE_GMM_CONTROL,
    GFX_ESCAPE_CAMARILLO_CONTROL,
    GFX_ESCAPE_ROTATION_CONTROL,
    GFX_ESCAPE_PAVP_CONTROL,
    GFX_ESCAPE_UMD_GENERAL_CONTROL,
    GFX_ESCAPE_RESOURCE_CONTROL,
    GFX_ESCAPE_SOFTBIOS_CONTROL,
    GFX_ESCAPE_ACPI_CONTROL,
    GFX_ESCAPE_CODE_KM_DAF,
    GFX_ESCAPE_CODE_PERF_CONTROL,
    GFX_ESCAPE_IGPA_INSTRUMENTATION_CONTROL,
    GFX_ESCAPE_CODE_OCA_TEST_CONTROL,
    GFX_ESCAPE_GPUCP,
    GFX_ESCAPE_GPUCP_RESOURCE,
    GFX_ESCAPE_PWRCONS_CONTROL,
    GFX_ESCAPE_KMD,
    GFX_ESCAPE_DDE,
    GFX_ESCAPE_IFFS,
    GFX_ESCAPE_RRDW_MMIO_FW           = 21,
    GFX_ESCAPE_GBG_ESCAPE_TO_PROCESS  = 50,
    GFX_ESCAPE_GBG_ESCAPES_TO_FORWARD = 51,
    GFX_ESCAPE_KM_GUC,
    GFX_ESCAPE_EVENT_PROFILING,
    GFX_ESCAPE_WAFTR,
    GFX_ESCAPE_PERF_STATS = 100,
    GFX_MAX_ESCAPE_CODES // MUST BE LAST
} GFX_ESCAPE_CODE_T;

/* Escape status from driver*/
typedef enum _DD_ESCAPE_STATUS
{
    DD_ESCAPE_STATUS_SUCCESS = 0,
    DD_ESCAPE_AUX_ERROR_DEFER,
    DD_ESCAPE_AUX_ERROR_TIMEOUT,
    DD_ESCAPE_AUX_ERROR_INCOMPLETE_WRITE,
    DD_ESCAPE_COLOR_3DLUT_INVALID_PIPE,
    DD_ESCAPE_STATUS_UNKNOWN
} DD_ESCAPE_STATUS;

/* Structure requried for sending request details and data*/
typedef struct _GFX_ESCAPE_HEADER_T_T
{
    unsigned int      ulReserved;
    unsigned short    ulMinorInterfaceVersion;
    unsigned short    ulMajorInterfaceVersion;
    GFX_ESCAPE_CODE_T uiMajorEscapeCode;
    unsigned int      uiMinorEscapeCode;
} GFX_ESCAPE_HEADER_T_T;

/**
 * @brief                  Makes escape call to driver
 * @param[in]              size of writeback escape struct
 * @param[out]             pEscapeData contains WB related requested information
 * @param[in]              escapeOpCodeReq contains WB related requested information
 * @return                 S_OK/S_FALSE based on function success
 */
HRESULT GetDetails(INT size, void *pEscapeData, ESCAPE_OPCODES escapeOpCodeReq);
