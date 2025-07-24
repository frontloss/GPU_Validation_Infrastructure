/**
 * @file
 * @section Vbt_c
 * @brief Internal source file which contains implementation required for VBT Simulation
 *
 * @ref Vbt.c
 * @author Reeju Srivastava
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

#pragma once
#include "Vbt.h"

CDLL_EXPORT HRESULT GetSetVbtBlock(__inout PBYTE pBlockData, __in BOOL bSet)
{
    return S_OK;
}

CDLL_EXPORT HRESULT EnableDisableVBTSimulation(__in BOOL bFlag)
{
    return S_OK;
}

CDLL_EXPORT HRESULT ReadWriteVBT(__out PBYTE pVbtData, __inout UINT32 dataSize, __in BOOL bSet)
{
    return S_OK;
}
