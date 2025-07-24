/**
 * @file
 * @section DisplayPortUtility_cpp
 * @brief Internal source file which contains implementation required for getting information related to
 * machine, operating system, driver, register read, diva status, generic escape etc..,
 *
 * @ref DisplayPortUtility.cpp
 * @author C, Diwakar
 */

/*===================== begin_copyright_notice ==================================

INTEL CONFIDENTIAL
Copyright 2000-2015
Intel Corporation All Rights Reserved.

The source code contained or described herein and all documents related to the
source code ("Material") are owned by Intel Corporation or its suppliers or
licensors. Title to the Material remains with Intel Corporation or its suppliers
and licensors. The Material contains trade secrets and proprietary and confidential
information of Intel or its suppliers and licensors. The Material is protected by
worldwide copyright and trade secret laws and treaty provisions. No part of the
Material may be used, copied, reproduced, modified, published, uploaded, posted,
transmitted, distributed, or disclosed in any way without Intel’s prior express
written permission.

No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express
and approved by Intel in writing.

======================= end_copyright_notice ==================================*/

#pragma once

#include <Windows.h>
#include <stdio.h>
#include <stdlib.h>
#include "..\Common\DisplayPort.h"

struct DPDeviceContext stDPDevContext;

/*
 * @brief        Exposed API to get DisplayPort DLL's interface version
 * @param[out]   Pointer to API version
 * @return       VOID
 */
BOOL GetDisplayPortInterfaceVersion(_Out_ PINT pVersion)
{
    if (NULL == pVersion)
    {
        TRACE_LOG(DEBUG_LOGS, "[DisplayPort.DLL]: Null pointer error.\n");
        return FALSE;
    }

    /* Assign DisplayPort API version into pVersion which is then returned back to the user space */
    *pVersion = (INT)DISPLAYPORT_INTERFACE_VERSION;

    TRACE_LOG(DEBUG_LOGS, "[DisplayPort.DLL]: DisplayPort API version is %d\n", *pVersion);
    return TRUE;
}