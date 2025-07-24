/**
 * @file DDRW_MPO.h
 * @addtogroup CDll_MPO
 * @brief DLL provide interfaces to access GfxValSimulator
 * <ul>
 * <li> @ref DDRW_EnableDisableMPOSimulation \n @copybrief DDRW_EnableDisableMPOSimulation \n
 * <li> @ref CloseDIVA \n @copybrief CloseDIVA \n
 * <li> @ref EnableDisableFramework \n @copybrief EnableDisableFramework \n
 * <li> @ref EnableDisableFeature \n @copybrief EnableDisableFeature \n
 * </ul>
 * \attention Donot modify this API without consent from the author
 * @author	  Ilamparithi Mahendran
 */

/*************************************************************************
**                                                                      **
**                    I N T E L   C O N F I D E N T I A L               **
**       Copyright (c) 2017 Intel Corporation All Rights Reserved.      **
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
**  distributed, or disclosed in any way without Intel's prior express  **
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

#ifndef DDRW_MPO_H
#define DDRW_MPO_H

#include <Windows.h>
#include "..\inc\YANGRA\MPOArgs.h"
#include "GfxValSimAccess.h"
#include "PyPlanes.h"
#include "ResourceManager.h"

#define MPO_DLL _declspec(dllexport)

typedef struct _MPO_CAPS
{
    union {
        struct
        {
            ULONG Rotation : 1;                       // Full rotation
            ULONG RotationWithoutIndependentFlip : 1; // Rotation, but without simultaneous IndependentFlip support
            ULONG VerticalFlip : 1;                   // Can flip the data vertically
            ULONG HorizontalFlip : 1;                 // Can flip the data horizontally
            ULONG StretchRGB : 1;                     // Supports RGB formats
            ULONG StretchYUV : 1;                     // Supports YUV formats
            ULONG BilinearFilter : 1;                 // Blinear filtering
            ULONG HighFilter : 1;                     // Better than bilinear filtering
            ULONG Shared : 1;                         // MPO resources are shared across VidPnSources
            ULONG Immediate : 1;                      // Immediate flip support
            ULONG Plane0ForVirtualModeOnly : 1;       // Stretching plane 0 will also stretch the HW cursor and should only be used for virtual mode support
            ULONG QueuedFlip : 1;                     // Queued flip support
            ULONG FlipQSupportParamChange : 1;        // Allow Queued flips with attribute changes or different set of enabled/disabled planes
            ULONG FlipQSupportFenceSync : 1;          // Capablity to monitor fence submitted to GPU and write the monitored fence when flip is visible
            ULONG Reserved : 18;
        };
        ULONG Value;
    };
} MPO_CAPS, PMPO_CAPS;

typedef struct _MPO_CAPS_ARG
{
    IN ULONG        VidPnSourceId;
    IN ULONG        PipeId;
    OUT ULONG       MaxPlanes;
    OUT ULONG       MaxRgbPlanes;
    OUT ULONG       MaxYuvPlanes;
    OUT DD_MPO_CAPS OverlayCaps;
    OUT ULONG       MaxStretchFactorMultBy100;
    OUT ULONG       MaxShrinkFactorPlanarMultBy100;
    OUT ULONG       MaxShrinkFactorNonPlanarMultBy100;
    OUT ULONG       MaxFlipQueues;     // Valid only for QueuedFlip
    OUT ULONG       MaxFlipQueueDepth; // Valid only for QueuedFlip; Assuming symmetrical depth for each queue
} MPO_CAPS_ARG, *PMPO_CAPS_ARG;

/**
 * @brief	It enables and disables DFT framework for MPO feature and creates an handle to DIVA.
 *
 * @param[in]	hGfxValSimAccess Handle to access GfxValSimulator
 * @param[in]	bEnable A boolean value to either enable or disable DFT
 * @return		Returns 0(False) on function failure; else 1(True)
 */
MPO_DLL BOOL DDRW_EnableDisableMPOSimulation(PGFX_ADAPTER_INFO pAdapterInfo, HANDLE hGfxValSim, BOOL bEnable);

/**
 * @brief	It checks the details of hardware support for multiplane overlays on RS2.
 *
 * @param[in]	pPlanes Pointer to structure @ref _PLANES_ containing the plane info
 * @return		Returns 0(Success) if hardware supports the passed plane info, else 1 for check MPO failure and 2 for resource allocation failure
 */
MPO_DLL UINT DDRW_CheckForMultiPlaneOverlaySupport3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes);

/**
 * @brief	It checks the basic overlay plane capabilities.

 * @param[in]	    hGfxValSimAccess Handle to access GfxValSimulator
 * @param[inout]	pMPOCaps Pointer to structure @ref MPO_CAPS_ARGS to get MPO caps for specific source id
 * @return			Returns 0(False) on function failure; else 1(True)
 */
MPO_DLL BOOL DDRW_GetMPOCaps(PGFX_ADAPTER_INFO pAdapterInfo, PMPO_CAPS_ARG pMPOCaps);

/**
 * @brief	It flips the given resources/surfaces on the plane. Presents the buffer onto the Display on RS2.
 *
 * @param[in]	pPlanes Pointer to structure @ref _PLANES_ containing the plane info
 * @return		Returns 1 for SSA MPO failure and 2 for resource allocation failure; else 0(Success)
 */
MPO_DLL UINT DDRW_SetSourceAddressForMultiPlaneOverlay3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes);

void TranslateOSInputColorInfoToDrv(IN PYPLANES_MPO_COLOR_SPACE_TYPE InValue, OUT DD_COLOR_PIXEL_DESC *pColorInfo);

/**
 * @brief	It enables and disables DFT framework for FlipQ feature and creates an handle to Valsim.
 *
 * @param[in]	hGfxValSimAccess Handle to access GfxValSimulator
 * @param[in]	bEnable A boolean value to either enable or disable DFT
 * @return		Returns 0(False) on function failure; else 1(True)
 */
MPO_DLL BOOL FlipQEnableDisableMPOSimulation(PGFX_ADAPTER_INFO pAdapterInfo, HANDLE hGfxValSim, BOOL bEnable);

/**
 * @brief	It checks the details of hardware support for multiplane overlays.
 *
 * @param[in]	pPlanes Pointer to structure @ref _PLANES_ containing the plane info
 * @return		Returns 0(Success) if hardware supports the passed plane info, else 1 for check MPO failure
 */
MPO_DLL UINT FlipQCheckForMultiPlaneOverlaySupport3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes);

/**
 * @brief	It flips the given resources/surfaces on the plane. Presents the buffer onto the Display.
 *
 * @param[in]	pPlanes Pointer to structure @ref _PLANES_ containing the plane info
 * @return		Returns 1 for SSA MPO failure and 0 for Success
 */
MPO_DLL UINT FlipQSetSourceAddressForMultiPlaneOverlay3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes);

#endif