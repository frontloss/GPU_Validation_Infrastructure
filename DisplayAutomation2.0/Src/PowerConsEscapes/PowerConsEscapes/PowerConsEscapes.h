/**
 * @file		PowerConsEscapes.h
 * @brief	This contains exposed functions of PowerConsEscapes.dll
 * @remarks
 * PowerConsEscapes DLL exposes below functions/APIs:
 * <ul>
 * <li> @ref  AlsOverride				</li><br> @copybrief  AlsOverride
 * </ul>
 * @attention Do not modify this API without consent from the author.
 *
 * @author	Ashish Tripathi
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

/* Avoid multi inclusion of header file */
#pragma once

#include <Windows.h>

/* Preprocessor Macros*/
#ifdef _DLL_EXPORTS
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT __declspec(dllimport)
#endif

/**
 * @brief									Set driver to use ALS override data
 * @param[in]	override					Boolean argument to override
 * @param[in]	lux							lux value
 * @param[out]	pErrorCode					contains error if any
 * @return		BOOLEAN
 */
DLL_EXPORT BOOLEAN AlsOverride(_In_ BOOLEAN override, _In_ INT lux, _Out_ HRESULT *pErrorCode);
