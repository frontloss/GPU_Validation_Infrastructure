/**
 * @file MPO.h
 * @addtogroup CDll_MPO
 * @brief DLL that checks for the hardware support for the planes, present multiple surfaces on the screen, check MPO capabilities.
 * @remarks
 * MPO  DLL that checks for the hardware support for the planes, present multiple surfaces on the screen, check MPO capabilities and MPO group capabilities. \n
 * <ul>
 * <li> @ref CheckForMultiPlaneOverlaySupport			\n @copybrief CheckForMultiPlaneOverlaySupport \n
 * <li> @ref SetSourceAddressForMultiPlaneOverlay		\n @copybrief SetSourceAddressForMultiPlaneOverlay \n
 * <li> @ref GetMPOCaps									\n @copybrief GetMPOCaps \n
 * <li> @ref GetMPOGroupCaps								\n @copybrief GetMPOGroupCaps \n
 * <li> @ref EnableDisableMPODFT							\n @copybrief EnableDisableMPODFT \n
 * <li> @ref CheckForMultiPlaneOverlaySupport3			\n @copybrief CheckForMultiPlaneOverlaySupport3 \n
 * <li> @ref SetSourceAddressForMultiPlaneOverlay3		\n @copybrief SetSourceAddressForMultiPlaneOverlay3 \n
 * </ul>
 * \attention Do not modify this API without consent from the author
 * @author	  Anjali Shetty, Ilamparithi Mahendran
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

#ifndef MPO_H
#define MPO_H
#include <Windows.h>
#include "..\inc\mainline\SimDrv_Gfx_MPO.h"
#include "GfxValSimAccess.h"
#include "PyPlanes.h"
#include "ResourceManager.h"

#define MPO_DLL _declspec(dllexport)

/*HDR Metadata SB Strcture Eq*/
typedef struct _MPO_HDR_STATIC_METADATA
{
    USHORT usEOTF;
    USHORT usDisplayPrimariesX[3];
    USHORT usDisplayPrimariesY[3];
    USHORT usWhitePointX;
    USHORT usWhitePointY;
    USHORT usMaxDisplayMasteringLuminance;
    USHORT usMinDisplayMasteringLuminance;
    USHORT usMaxCLL;
    USHORT usMaxFALL; // Maximum Frame Average Light Level
} MPO_HDR_STATIC_METADATA, *PMPO_HDR_STATIC_METADATA;

/*MPO Capabilities*/
typedef struct _MPO_CAPS
{
    UINT uiMaxPlanes;
    UINT uiNumCapabilityGroups;
} MPO_CAPS, *PMPO_CAPS;

/*MPO Capabilities Arguments*/
typedef struct _MPO_CAPS_ARGS
{
    ULONG    ulSourceID;
    MPO_CAPS stMPOCaps;
} MPO_CAPS_ARGS, *PMPO_CAPS_ARGS;

/*MPO Group capabilities*/
typedef struct _MPO_GROUP_CAPS
{
    UINT uiMaxPlanes;
    UINT uiMaxStretchFactorNum;
    UINT uiMaxStretchFactorDenm;
    UINT uiMaxShrinkFactorNum;
    UINT uiMaxShrinkFactorDenm;
    UINT uiOverlayFtrCaps;
    UINT uiStereoCaps;
} MPO_GROUP_CAPS, *PMPO_GROUP_CAPS;

/*MPO Group capabilities arguments*/
typedef struct _MPO_GROUP_CAPS_ARGS
{
    ULONG          ulSourceID;
    MPO_GROUP_CAPS stMPOGroupCaps;
} MPO_GROUP_CAPS_ARGS, *PMPO_GROUP_CAPS_ARGS;

/**
 * @brief	    It checks the details of hardware support for multiplane overlays.
 *
 * @param[in]	pPlanes Pointer to structure @ref _PLANES_ containing the plane info
 * @return		Returns 1(True) if hardware supports the passed plane info, else 1 for check MPO failure and 2 for resource allocation failure
 */
MPO_DLL UINT mainline_CheckForMultiPlaneOverlaySupport(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes);

/**
 * @brief	    It flips the given resources/surfaces on the plane. Presents the buffer onto the Display.
 *
 * @param[in]	pPlanes Pointer to structure @ref _PLANES_ containing the plane info
 * @return		Returns 1 for SSA MPO failure and 2 for resource allocation failure; else 1(True)
 */
MPO_DLL UINT mainline_SetSourceAddressForMultiPlaneOverlay(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes);

/**
 * @brief	        It checks the basic overlay plane capabilities.
 *
 * @param[inout]	pMPOCaps Pointer to structure @ref MPO_CAPS_ARGS to get MPO caps for specific source id
 * @return			Returns 0(False) on function failure; else 1(True)
 */
MPO_DLL BOOL mainline_GetMPOCaps(PGFX_ADAPTER_INFO pAdapterInfo, PMPO_CAPS_ARGS pMPOCaps);

/**
 * @brief	        It checks the group of overlay plane capabilities.
 *
 * @param[in]		uiGroupIndex The group index of the no of capable groups
 * @param[inout]	pMPOCaps Pointer to structure @ref MPO_GROUP_CAPS_ARGS to get MPO caps for specific source id and group index
 * @return			Returns 0(False) on function failure; else 1(True)
 */
MPO_DLL BOOL mainline_GetMPOGroupCaps(PGFX_ADAPTER_INFO pAdapterInfo, PMPO_GROUP_CAPS_ARGS pMPOGroupCaps, UINT uiGroupIndex);

/**
 * @brief	    It checks the details of hardware support for multiplane overlays on RS2.
 *
 * @param[in]	pPlanes Pointer to structure @ref _PLANES_ containing the plane info
 * @return		Returns 1(True) if hardware supports the passed plane info, else 1 for check MPO failure and 2 for resource allocation failure
 */
MPO_DLL UINT mainline_CheckForMultiPlaneOverlaySupport3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes);

/**
 * @brief	    It flips the given resources/surfaces on the plane. Presents the buffer onto the Display on RS2.
 *
 * @param[in]	pPlanes Pointer to structure @ref _PLANES_ containing the plane info
 * @return		Returns 1 for SSA MPO failure and 2 for resource allocation failure; else 1(True)
 */
MPO_DLL UINT mainline_SetSourceAddressForMultiPlaneOverlay3(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes);

/**
 * @brief		To enable and disable DFT framework.
 *
 * @param[in]	bEnable A boolean value to either enable or disable DFT
 * @param[in]	eFeature To enable a specific feature
 * @return		Returns 0(False) on function failure; else 1(True)
 */
MPO_DLL BOOL mainline_EnableDisableMPODFT(PGFX_ADAPTER_INFO pAdapterInfo, HANDLE hGfxValSim, BOOL bEnable, SIMDRIVER_DISPLAY_FEATURE eFeature);

/**
 * @brief		To enable or disable specific feature.
 *
 * @param[in]	bEnable A boolean value to either enable or disable feature
 * @param[in]	eFeature have details of enable/disable feature information
 * @return		Returns 0(False) on function failure; else 1(True)
 */
BOOL mainline_EnableDisableMPO(PGFX_ADAPTER_INFO pAdapterInfo, BOOL bEnable, SIMDRIVER_DISPLAY_FEATURE eFeature);

#endif