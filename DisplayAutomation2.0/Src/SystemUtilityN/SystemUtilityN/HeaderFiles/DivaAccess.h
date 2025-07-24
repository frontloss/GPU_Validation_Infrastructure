/**
 * @file DivaAccess.h
 * @addtogroup CDll_Diva
 * @brief DLL provide interfaces to access DIVA and DFT framework
 * @remarks
 * DIVA Dll's below intarfaces can be used for framework and feature(s) enabling/disabling  \n
 * <ul>
 * <li> @ref InitDIVA \n @copybrief InitDIVA \n
 * <li> @ref CloseDIVA \n @copybrief CloseDIVA \n
 * <li> @ref EnableDisableFramework \n @copybrief EnableDisableFramework \n
 * <li> @ref EnableDisableFeature \n @copybrief EnableDisableFeature \n
 * </ul>
 * \attention Donot modify this API without consent from the author
 * @author	  Anjali Shetty
 */

/*************************************************************************
**                                                                      **
**                    I N T E L   C O N F I D E N T I A L               **
**       Copyright (c) 2016 Intel Corporation All Rights Reserved.      **
**                                                                      **
**  The source code contained or described herein and all documents     **
**  related to the source code ("Material") are owned by Intel          **
**  Corporation or its suppliers or licensors. Title to the Material    **
**  remains with Intel Corporation or its suppliers and licensors. The  **
**  Material contains trade secrets and proprietary and confidential    **
**  information of Intel or its suppliers and licensors. The Material   **
**  is protected by worldwide copyright and trade secret laws and       **
**  treaty provisions. No part of the Material may be used, copied,     **
**  reproduced, modified, published, uploaded, posted, transmitted,     **
**  distributed, or disclosed in any way without Intel’s prior express  **
**  written permission.                                                 **
**                                                                      **
**  No license under any patent, copyright, trade secret or other       **
**  intellectual property right is granted to or conferred upon you by  **
**  disclosure or delivery of the Materials, either expressly, by       **
**  implication, inducement, estoppel or otherwise. Any license under   **
**  such intellectual property rights must be express and approved by   **
**  Intel in writing.                                                   **
**                                                                      **
*************************************************************************/

#ifndef DIVA_ACCESS_H
#define DIVA_ACCESS_H

#include <Windows.h>
#include "GfxValStub_DisplayFeature.h"
#include "GfxValStub_GenericGfxAccess.h"
#include <stdio.h>

/* To avoid warning*/
#pragma warning(disable : 4127)

/* Define an  Interface Guid so that app can find the device and talk to it*/
DEFINE_GUID(GUID_DEVINTERFACE_DIVA_KMD, 0xefda009e, 0xb0aa, 0x49fe, 0xb5, 0x11, 0xe8, 0xd2, 0xd5, 0xbf, 0x45, 0xa4);
// {efda009e-b0aa-49fe-b511-e8d2d5bf45a4}

#define DIVA_DOS_DEVICE_NAME_WCHAR L"\\DosDevices\\DivaKmd" // Symbolic DOS Name for the Device
#define DIVA_DOS_DEVICE_NAME "\\\\.\\DivaKmd"               // Symbolic DOS Name for the Device

#define DIVA_IOCTL_DEVICE_TYPE (0x8086)                           // Device type to be used for IOCTL calls; any value > 0x8000
#define DIVA_IOCTL_FUNC_CODE_BASE (0x808)                         // Base function code for IOCTL calls; any value > 0x800
#define DIVA_IOCTL_ACCESS_TYPE (FILE_READ_DATA | FILE_WRITE_DATA) // Type of access to be requested while opening the file object for device

/* Helper macro to reduce typing for each of the IOCTL calls*/
#define _DIVA_CTL_CODE(_FxnCode) CTL_CODE(DIVA_IOCTL_DEVICE_TYPE, DIVA_IOCTL_FUNC_CODE_BASE + _FxnCode, METHOD_BUFFERED, DIVA_IOCTL_ACCESS_TYPE)

/* IOCTL to extract version information of the DIVA Driver*/
#define DIVA_IOCTL_GetVersion _DIVA_CTL_CODE(0)

typedef struct _DIVA_IOCTL_GetVersion_Out
{
    ULONG Version;
} DIVA_IOCTL_GetVersion_Out, *PDIVA_IOCTL_GetVersion_Out;

/* IOCTL to carry out the communication between GFX & DIVA drivers using VAL_STUB callback object*/
#define DIVA_IOCTL_GfxValStubCommunication _DIVA_CTL_CODE(1)

HANDLE hDivaAccess;

#define GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION 0x1
#define GVSTUB_DISPLAY_FEATURE_STATUS_FAILURE 0x00000001
#define GVSTUB_FEATURE_INFO_VERSION 0x1
#define GVSTUB_FEATURE_FAILURE 0x00000008
#define GVSTUB_FEATURE_SUCCESS 0x00000000

/* Enum for features*/
typedef enum _GVSTUB_FEATURE_TYPE
{
    GVSTUB_FEATURE_UNDEFINED = 0,
    GVSTUB_GENERIC_GFX_ACCESS,
    GVSTUB_THUNK_ESCAPE,
    GVSTUB_FEATURE_DISPLAY,
    GVSTUB_FEATURE_KMRENDER,
    GVSTUB_FEATURE_PWRCONS,
    GVSTUB_FEATURE_GMM,
    GVSTUB_FEATURE_PINNING,
    GVSTUB_FEATURE_MAX
} GVSTUB_FEATURE_TYPE;

/* Structs to enable/disbale feature(s)*/
typedef struct _GVSTUB_FEATURE_INFO_ARGS
{
    GVSTUB_META_DATA stFeatureMetaData; // stValStubFeatureBasicInfo.ulServiceType as GFX_VAL_STUB_FEATURE_TYPE
    union {
        GVSTUB_GENERIC_GFX_ACCESS_ARGS stGenericGfxAccessArgs; // Generic access like read or write MMIO/IOSF/Registry etc.
        GVSTUB_DISPLAY_FEATURE_ARGS    stDisplayFeatureArgs;   // Access Display features like MPO/DeviceSimulation etc.
    };
} GVSTUB_FEATURE_INFO_ARGS, *PGVSTUB_FEATURE_INFO_ARGS;

/**
 * @brief	Get handle of DIVA driver to make IOCTL calls
 *
 * @return	Returns 1(True) if handle is obtained; else 0(False)
 */
BOOLEAN InitDIVA();

/**
 * @brief	Release handle of DIVA driver
 *
 * @return	Returns 1(True) if handle is closed; else 0(False)
 */
BOOL CloseDIVA();

/**
 * @brief		To enable or disable the DFT framework in Gfx driver
 *
 * @param[in]	bEnable A boolean value to either enable or disable framework
 * @return		Returns 0(False) on function failure; else 1(True)
 */
BOOL EnableDisableFramework(BOOLEAN bEnable);

/**
 * @brief		To enable or disable specific feature in DIVA framework
 *
 * @param[in]	bEnable A boolean value to either enable or disable feature
 * @param[in]	eFeature have details of enable/disable feature information
 * @return		Returns 0(False) on function failure; else 1(True)
 */
BOOL EnableDisableFeature(BOOLEAN bEnable, GVSTUB_DISPLAY_FEATURE eFeature);

#endif