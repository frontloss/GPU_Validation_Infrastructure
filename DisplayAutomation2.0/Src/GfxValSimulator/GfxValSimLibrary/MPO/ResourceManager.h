/**
 * @file ResourceManager.h
 * @addtogroup CDll_MPO
 * @brief DLL that provides interfaces to create and free resources
 * @remarks
 * MPO Dll's below intarfaces can be used for resource creation/deletion  \n
 * <ul>
 * <li> @ref DFTCreateResource		\n @copybrief DFTCreateResource \n
 * <li> @ref DFTFreeResource			\n @copybrief DFTFreeResource \n
 * <li> @ref DFTCreateBufferContent	\n @copybrief DFTCreateBufferContent \n
 * </ul>
 * \attention Donot modify this API without consent from the author
 * @author	  Anjali Shetty, Ilamparithi Mahedran
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

#pragma once

#ifndef _RESOURCE_MANAGER_H_
#define _RESOURCE_MANAGER_H_

#include "Windows.h"
#include "PyPlanes.h"
#include "inc/legacy/SimDrvGfxMpo.h"
#include "../../../CommonInclude/CommonInclude.h"

#define MAX_RESOURCE 2

/**
 * @brief		    Routine to fill the buffer to make a flip.
 *
 * @param[inout]		pResourceInfo Pointer to structue @ref RESOURCE_INFO to get resource info
 * @param[in]		lWidth Width of the plane
 * @param[in]		lHeight Height of the plane
 * @param[in]		PixelFormat Pixel Format of the plane
 * @param[in]		eTileFormat Tile Format of the plane
 * @param[in]		uiLayerIndex Layer index of the plane
 * @param[in]		pPath Path to the dump file
 * @param[in]        IsAsyncFlips True if Async flip required; False, otherwise
 * @return			Returns 1(True) on creating the resource; else 0(False)
 */
VOID DFTCreateBufferContent(PPYPLANES_RESOURCE_INFO pResourceInfo, LONG lWidth, LONG lHeight, INT PixelFormat, INT TileFormat, UINT uiLayerIndex, CHAR *pPath, BOOL IsAsyncFlip);

/**
 * @brief			To create the resource for a particular plane on DDRW.
 *
 * @param[inout]		pResourceInfo Pointer to structue @ref RESOURCE_INFO to get resource info
 * @param[in]		lWidth Width of the plane
 * @param[in]		lHeight Height of the plane
 * @param[in]		PixelFormat Pixel Format of the plane
 * @param[in]		eTileFormat Tile Format of the plane
 * @param[in]		uiLayerIndex Layer index of the plane
 * @param[in]		pPath Path to the dump file
 * @param[in]        IsAsyncFlips True if Async flip required; False, otherwise
 * @return			Returns 1(True) on creating the resource; else 0(False)
 */
BOOL DDRW_DFTCreateResource(PGFX_ADAPTER_INFO pAdapterInfo, PPYPLANES_RESOURCE_INFO pResourceInfo, LONG lWidth, LONG lHeight, INT PixelFormat, INT TileFormat, UINT uiLayerIndex,
                            CHAR *pPath, BOOL IsAsyncFlips);

/**
 * @brief			To create the resource for a particular plane.
 *
 * @param[inout]		pResourceInfo Pointer to structue @ref RESOURCE_INFO to get resource info
 * @param[in]		lWidth Width of the plane
 * @param[in]		lHeight Height of the plane
 * @param[in]		PixelFormat Pixel Format of the plane
 * @param[in]		eTileFormat Tile Format of the plane
 * @param[in]		uiLayerIndex Layer index of the plane
 * @param[in]		pPath Path to the dump file
 * @return			Returns 1(True) on creating the resource; else 0(False)
 */
BOOL mainline_DFTCreateResource(PGFX_ADAPTER_INFO pAdapterInfo, PPYPLANES_RESOURCE_INFO pResourceInfo, LONG lWidth, LONG lHeight, SIMDRIVER_PIXELFORMAT PixelFormat,
                                SIMDRIVER_SURFACE_MEMORY_TYPE TileFormat, UINT uiLayerIndex, CHAR *pPath);

/**
 * @brief		To free the resource of particular plane.
 *
 * @param[in]	pResourceInfo Pointer to structure @ref RESOURCE_INFO to free the resource of a particular plane
 * @return		Returns 1(True) on freeing the resource; else 0(False)
 */
BOOL mainline_DFTFreeResource(PGFX_ADAPTER_INFO pAdapterInfo, PPYPLANES_RESOURCE_INFO pResourceInfo);

/**
 * @brief		To create the resource of particular plane.
 *
 * @param[in]	pPlanes Pointer to structure @ref _PLANES_ to create the resource of a particular plane
 * @return		Returns True on successfully creating the resource; else False
 */
CDLL_EXPORT BOOL FlipQDFTCreateResource(PGFX_ADAPTER_INFO pAdapterInfo, PPLANES pPlanes);

/**
 * @brief		To free the resource of particular plane on DDRW.
 *
 * @param[in]	pResourceInfo Pointer to structure @ref RESOURCE_INFO to free the resource of a particular plane
 * @return		Returns 1(True) on freeing the resource; else 0(False)
 */
CDLL_EXPORT BOOL DDRW_DFTFreeResource(PGFX_ADAPTER_INFO pAdapterInfo, PPYPLANES_RESOURCE_INFO pResourceInfo);

#endif