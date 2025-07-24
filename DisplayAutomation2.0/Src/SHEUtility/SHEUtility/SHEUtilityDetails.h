/**
* @file
* @section SHEUtilityDetails_h
* @brief Internal header file which contains common data structures, macro and helper functions
*
* @ref SHEUtilityDetails.h
* @author Reeju Srivastava
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

/* Avoid multi inclusion of header file*/
#pragma once

#include <stdio.h>
#include <string.h>
#include <tchar.h>
#include <stdlib.h>
#include <windows.h>

/* User define headers*/
#include "SHEUtility.h"
#include "../../externaldep/include/CommonLogger.h"

/* Preprocessor magic numbers*/
#define MAXPORTS 255
#define BUFFERSIZE 20

#define __func__ __FUNCTION__

/* Helper function to get the connected COM port details of SHE 1.0 and 2.0*/
bool GetcomBufferDetails(PINT ComPort, PCHAR Buffer);

/* Helper function to write user opcode to the COM port*/
bool SerialWrite(PCHAR pBuffer, DWORD noOfBytesToWrite, PINT ComNumber);


