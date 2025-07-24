/*===================== begin_copyright_notice ==================================

INTEL CONFIDENTIAL
Copyright 2000-2012
Intel Corporation All Rights Reserved.

The source code contained or described herein and all documents related to the
source code ("Material") are owned by Intel Corporation or its suppliers or
licensors. Title to the Material remains with Intel Corporation or its suppliers
and licensors. The Material contains trade secrets and proprietary and confidential
information of Intel or its suppliers and licensors. The Material is protected by
worldwide copyright and trade secret laws and treaty provisions. No part of the
Material may be used, copied, reproduced, modified, published, uploaded, posted,
transmitted, distributed, or disclosed in any way without Intel's prior express
written permission.

No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express
and approved by Intel in writing.

======================= end_copyright_notice ==================================*/
//
//  Filename : Driver_Model.h
//  Purpose  : Global definitions for many #defines and Macros to be used
//             By all portions of the driver
//
//  Date     : 7/11/2005
//  Date     : 4/04/2012  -  Removed XP support. Win7/Win8 only.
//=============================================================================

#ifndef _DRIVER_MODEL_H_
#define _DRIVER_MODEL_H_

// Info to determine version of OS for build

#if defined(_WIN32) || defined(WDDM_LINUX)

// These symbols should be taken from sdkddkver.h. But if not defined
// for any reason or driver_model.h is included before sdkddkver.h,
// do it here.
#ifndef _WIN32_WINNT_WIN10
#define _WIN32_WINNT_WIN10 0x0A00
#endif

#ifdef WINVER
#undef WINVER
#endif

#ifdef _WIN32_WINNT
#undef _WIN32_WINNT
#endif

#undef _NT_TARGET_VERSION
#undef NTDDI_VERSION

#define _WIN32_WINNT _WIN32_WINNT_WIN10
#define WINVER _WIN32_WINNT_WIN10
#define _NT_TARGET_VERSION _WIN32_WINNT_WIN10
#define NTDDI_VERSION 0x0A000006

#define LHDM 1
#define XPDM 0

#else // #ifdef _WIN32

// Not a Windows OS
#define LHDM 0
#define XPDM 0

#endif // #ifdef _WIN32

#endif // End of file Driver_Model.h
