/**
 * @file
 * @section CommonDetails_h
 * @brief Internal header file which contains header files, data structures and helper functions required all over the solution.
 *
 * @ref CommonDetails.h
 * @author Reeju Srivastava
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

/* Avoid multi inclusion of header file*/
#pragma once
/* System header(s)*/
#include <windows.h>
#include <stdio.h>
#include <stdbool.h>

/* User defined headers*/
#include "GfxValSim.h"
#include "../Logger/log.h"
#include "..\\..\\externaldep\\include\CommonLogger.h"

/* gfxValSim global Handle*/
HANDLE hGfxValSimHandle;

#define DLL_NAME "GfxValSim.dll"

/* DLL version number*/
#define DLL_INTERFACE_VERSION 0x1
#define INTEL_VENDOR_ID L"8086"

#define GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize)                                                                           \
    {                                                                                                                                              \
        if (NULL == pAdapterInfo)                                                                                                                  \
        {                                                                                                                                          \
            TRACE_LOG(DEBUG_LOGS, "Error: GFX_ADAPTER_INFO Pointer is NULL! \n");                                                                  \
            return S_FALSE;                                                                                                                        \
        }                                                                                                                                          \
        if (0 != wcscmp(pAdapterInfo->vendorID, INTEL_VENDOR_ID))                                                                                  \
        {                                                                                                                                          \
            TRACE_LOG(DEBUG_LOGS, "Error: Invalid vendor id %d provided, Supported vendor id is %d !\n", pAdapterInfo->vendorID, INTEL_VENDOR_ID); \
            return S_FALSE;                                                                                                                        \
        }                                                                                                                                          \
        if (sizeof(GFX_ADAPTER_INFO) != gfxAdapterInfoSize)                                                                                        \
        {                                                                                                                                          \
            TRACE_LOG(DEBUG_LOGS, "Error: GFX_ADAPTER_INFO size mismatch !\n");                                                                    \
            return S_FALSE;                                                                                                                        \
        }                                                                                                                                          \
    }

#define NULL_PTR_CHECK(ptr)                         \
    {                                               \
        if (NULL == ptr)                            \
        {                                           \
            ERROR_LOG("NULL Pointer, Exiting !!!"); \
            return FALSE;                           \
        }                                           \
    }

#define FREE_MEMORY(ptr) \
    {                    \
        if (NULL != ptr) \
        {                \
            free(ptr);   \
            ptr = NULL;  \
        }                \
    }