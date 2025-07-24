/**
 * @file
 * @brief DisplayDeviceSimulationApp Test header file contains function pointers and helper functions
 * required to test the DisplayDeviceSimulation DLL's exposed APIs
 *
 * @ref GfxValSimTestApp.h
 * @author Reeju Srivastava, Aafiya Kaleem
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

#pragma once
/* System Includes*/
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

/* User Includes*/
#include "..\GfxValSimLibrary\GfxValSim.h"

/* Port Numbers*/
CONST UINT INVALID_PORT = 0;
CONST UINT SIM_DP_A     = 11;
CONST UINT SIM_DP_B     = 12;
CONST UINT SIM_DP_C     = 13;
CONST UINT SIM_DP_D     = 14;
CONST UINT SIM_DP_E     = 6;
CONST UINT SIM_DP_F     = 21;
CONST UINT SIM_DP_G     = 24;
CONST UINT SIM_DP_H     = 27;
CONST UINT SIM_DP_I     = 30;
CONST UINT SIM_HDMI_B   = 7;
CONST UINT SIM_HDMI_C   = 8;
CONST UINT SIM_HDMI_D   = 9;
CONST UINT SIM_HDMI_E   = 23;
CONST UINT SIM_HDMI_F   = 20;
CONST UINT SIM_HDMI_G   = 26;
CONST UINT SIM_HDMI_H   = 29;
CONST UINT SIM_HDMI_I   = 32;

/* Port connector type*/
CONST UINT NATIVE = 0;
CONST UINT TC     = 1;
CONST UINT TBT    = 2;

UINT HelperInit();
UINT HelperPlug(INT, BOOL);
UINT HelperUnPlug(INT, BOOL);
UINT GetPortNo(const char *);
UINT ConnectorType(const char *);
void GetAdapterInfo();