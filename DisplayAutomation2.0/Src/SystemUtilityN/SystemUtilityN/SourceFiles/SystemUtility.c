/**
* @file
* @section SystemUtility
* @brief Internal source file which contains implementation required for getting information related to
                  GetDLLVersion
*
* @ref SystemUtility.c
* @author Reeju Srivastava, Ami Golwala, Amanpreet Kaur Khurana, Raghupathy
*/

/***********************************************************************************************
 * INTEL CONFIDENTIAL. Copyright (c) 2016 Intel Corporation All Rights Reserved.
 *  <br>The source code contained or described herein and all documents related to the source code
 *  ("Material") are owned by Intel Corporation or its suppliers or licensors. Title to the
 *  Material remains with Intel Corporation or its suppliers and licensors. The Material contains
 *  trade secrets and proprietary and confidential information of Intel or its suppliers and licensors.
 *  The Material is protected by worldwide copyright and trade secret laws and treaty provisions.
 *  No part of the Material may be used, copied, reproduced, modified, published, uploaded, posted,
 *  transmitted, distributed, or disclosed in any way without Intel's prior express written permission.
 *  <br>No license under any patent, copyright, trade secret or other intellectual property right is
 *  granted to or conferred upon you by disclosure or delivery of the Materials, either expressly,
 *  by implication, inducement, estoppel or otherwise. Any license under such intellectual property
 *  rights must be express and approved by Intel in writing.
 */

/* Avoid multi inclusion of header file*/
#pragma once

/* User defined header(s)*/
#include "../HeaderFiles/DivaAccess.h"
#include "wchar.h"
#include <cfgmgr32.h>
#include "../HeaderFiles/SystemUtility.h"

#include <initguid.h>
#include <devpkey.h>
#include <devguid.h>

CONST PCWSTR REGISTRY_ACCESS_PROVIDERS[] = { L"igfx", L"dgfx", L"HDAudBus", L"kbdhid", L"i8042prt", L"IntcAudiobus" };



char *LIBRARY_NAME = "SystemUtility.dll";

/* Function implementation*/

/**---------------------------------------------------------------------------------------------------------*
 * @brief GetDLLVersion (Exposed API)
 * Description: This function helps to Get System Utility DLL version
 * @param PULONG		(Pointer of PULONG to get API version)
 * return: VOID		Void
 *----------------------------------------------------------------------------------------------------------*/
CDLL_EXPORT VOID GetDLLVersion(PULONG pVersion)
{
    /* Check for the parameter is passed properly,
       this check is done only for exported functions*/
    if (NULL == pVersion)
        return;

    /* Set current DLL version details*/
    *pVersion = (ULONG)UTILITY_INTERFACE_VERSION;
    TRACE_LOG(INFO_LOGS, "Supported DLL version: 0x%05X", *pVersion);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           FreeAllocations (Exposed API)
 * Description      This function has implementation to close DIVA Handle if Enabled
 *-----------------------------------------------------------------------------------------------------------*/
CDLL_EXPORT VOID FreeAllocations()
{
    CloseDIVA();
}

