/**
* @file
* @addtogroup Dll_SHEUtility
* @brief
* DLL provide interfaces to get SHE tool connection status, Powerline switching, Lid switching and Display Hot plug and unplug.
* @remarks
* SHEUtility dll exposes APIs to get information related to SHE tool connection status, Powerline switching, lid switching and Hot plug and unplug.
* \n Refer structures defined in @ref SHEUtility.h file to know more how to make use of API interfaces \n
* <ul>
* <li> @ref GetDLLVersion						\n \copybrief GetDLLVersion \n
* <li> @ref GetSHEDeviceTypeandComPort		    \n \copybrief GetSHEDeviceTypeandComPort \n
* <li> @ref HotPlugUnplug						\n \copybrief HotPlugUnplug \n
* <li> @ref DisplayUnplugPLug					\n \copybrief DisplayUnplugPLug \n
* </ul>
*
* @author Sharath M
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

/* System defined headers*/
#include <stdbool.h>

/* Preprocessor Macros*/

#ifdef _DLL_EXPORTS
#define CDLL_EXPORT __declspec(dllexport)
#else
#define CDLL_EXPORT __declspec(dllimport)
#endif

/* DLL version information*/
#define SHE_INTERFACE_VERSION 0x2 

/* Enable or Disable dll's debug prints*/
#define DEBUG true

/* Specify list of display devices*/
typedef enum _DISPLAYTYPE
{
	SHE_UNKNOWN_DISPLAYTYPE = -1,
	SHE_DP_1 = 0, //port 1
	SHE_DP_2, //port 2
	SHE_DP_3, //port 3
	SHE_HDMI_1, //port 4
	SHE_EDP, //port 5
	IO_PORT6,
	SHE_DP_4, //port 7	
	SHE_HDMI_2, //port 8
	IO_PORT9,
	IO_PORT10,
	IO_PORT11,
	IO_PORT12,
	EMULATOR_PORT1,
	EMULATOR_PORT2,
	EMULATOR_PORT3
} DISPLAYTYPE;


/**
* @brief                  Get version details of DLL
*
* @param[out]             Contains information about version
*
* @return                 bool if success true otherwise false
*/
CDLL_EXPORT bool GetDLLVersion(PULONG pVersion);

/**
* @brief                  Get Diempel device/SHE 1.0 Device connection status
*
* @param[out]			  Contains information about SHE device configuration type.
*
* @param[out]			  Contains information about SHE device Com Port details.
*
* @return                 Return status if connected true else false
*/
CDLL_EXPORT int GetSHEDeviceTypeandComPort(PINT configuration_type, PINT ComNumber);

/**
* @brief                  Plug the display with specified delay for next operation
*
* @param[in]              opcode contains the information needed to be sent to HW
* @param[in]              delay command execution time if required in seconds
* @param[in]              Contains information about SHE device Com Port details.
*
* @return                 True or False based on request success
*/
CDLL_EXPORT bool HotPlugUnplug(PINT ComNumber, int opcode, int delay);



/**
* @brief                  Perform Lid switch operation with plug/unplug and hibernate for EDP
*
* @param[in]              opcode1 and opcode2 contains information about the data sent to HW
* @param[in]              delay command execution time if required in seconds
* @param[in]              Contains information about SHE device Com Port details.
* @param[in]              Contains information about whether SHE device needed to wake from Hibernate.
* @return                 True or False based on request success

*/
CDLL_EXPORT bool DisplayUnplugPLug(PINT ComPort, int opcode1, int opcode2, int delay1, bool LidSwitchPress );













