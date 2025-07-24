/**
 * @file
 * @addtogroup CDll_WritebackUtility
 * @brief
 * DLL fetches information related to display writeback feature
 * @remarks
 * WritebackUtility dll exposes APIs to get information related to writeback plug, unplug, buffer dump etc.., \n
 * <ul>
 * <li> @ref PlugWBDevice \n \copybrief PlugWBDevice \n
 * <li> @ref UnplugWBDevice \n \copybrief UnplugWBDevice \n
 * <li> @ref IsWBFeatureEnable \n \copybrief IsWBFeatureEnable \n
 * <li> @ref DumpWBBuffer \n \copybrief DumpWBBuffer \n
 * </li>
 * </ul>
 *
 * @author Reeju Srivastava, Ankurkumar Patel
 */

/***********************************************************************************************
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

/* System header(s) */
#include <windows.h>
#include <stdbool.h>

/* Preprocessor Macros*/
#ifdef _DLL_EXPORTS
#define CDLL_EXPORT __declspec(dllexport)
#else
#define CDLL_EXPORT __declspec(dllimport)
#endif
#define DLL_NAME "WritebackUtility.dll"

#pragma warning(disable : 4201)

typedef ULONG         DDU32;
typedef unsigned char DDU8;

#pragma pack(push, 1)

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

//
// Surface memory type
//
typedef enum _DD_ESC_SURFACE_MEMORY_TYPE
{
    DD_ESC_SURFACE_MEMORY_INVALID        = 0,
    DD_ESC_SURFACE_MEMORY_LINEAR         = 1, // Surface uses linear memory
    DD_ESC_SURFACE_MEMORY_TILED          = 2, // Surface uses tiled memory
    DD_ESC_SURFACE_MEMORY_X_TILED        = DD_ESC_SURFACE_MEMORY_TILED,
    DD_ESC_SURFACE_MEMORY_Y_LEGACY_TILED = 4, // Surface uses Legacy Y tiled memory (Gen9+)
    DD_ESC_SURFACE_MEMORY_Y_F_TILED      = 8, // Surface uses Y F tiled memory
} DD_ESC_SURFACE_MEMORY_TYPE;

/* Contains writeback devices details*/
typedef struct _WB_DEVICES_INFO
{
    BOOLEAN                isEnable;
    INT                    HResolution;
    INT                    VResolution;
    DD_CUI_ESC_PIXELFORMAT PixelFormat;
    ULONG                  DeviceId;
    HRESULT                error;
} WB_DEVICE_INFO;

/* Contains writeback mode/resolution details*/
typedef struct _WB_MODE
{
    DDU32 Cx;
    DDU32 Cy;
} WB_MODE;

/* Contains writeback escape HPD details*/
typedef struct _DD_ESC_WRITEBACK_HPD
{
    BOOLEAN HotPlug;                   // Plug or Unplug
    DDU32   DeviceId;                  // Target id of the device that is plugged in or needs unplug
    WB_MODE Resolution;                // Mode
    HANDLE  hWbSurfaceHandle;          // Surface Address input given by App
    HANDLE  hNotifyScreenCaptureEvent; // Screen capture Event that will be set when the capture is complete.
    BOOLEAN OverrideDefaultEdid;
    DDU8    EdidData[256];
} DD_ESC_WRITEBACK_HPD;

#pragma pack(pop)

/* All exported functions*/
/**
 * @brief                  Plug writeback device
 * @param[in]              deviceCount number of write back devices to be plug
 * @param[out]             pDeviceInfo contains WB device information
 * @return                 bool - TRUE/FALSE
 */
CDLL_EXPORT BOOLEAN PlugWBDevice(WB_MODE *mode, WB_DEVICE_INFO *pDeviceInfo);

/**
 * @brief                  UnPlug writeback device
 * @param[in]              deviceId id of wb device to be unplugged
 * @return                 bool - TRUE/FALSE
 */
CDLL_EXPORT BOOLEAN UnplugWBDevice(ULONG deviceId);

/**
 * @brief                  Provide information if feature is enable or not
 * @param[in]              pErrorCode error code
 * @return                 bool - TRUE is enable or FALSE if not
 */
CDLL_EXPORT BOOLEAN IsWBFeatureEnable(HRESULT *pErrorCode);

/**
 * @brief                  Dump writeback device buffer
 * @param[in]              deviceCount number of write back devices to be dump
 * @param[out]             count no of buffers
 * @return                 bool - TRUE/FALSE
 */
CDLL_EXPORT BOOLEAN DumpWBBuffer(ULONG deviceId, UINT count, UINT delayInSeconds);