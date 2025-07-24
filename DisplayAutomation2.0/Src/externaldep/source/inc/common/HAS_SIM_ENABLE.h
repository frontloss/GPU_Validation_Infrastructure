/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**
** Copyright (c) Intel Corporation (2009-2012).
**
** INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
** ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
** INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
** ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
** MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
** OTHER WARRANTY.  Intel disclaims all liability, including liability for
** infringement of any proprietary rights, relating to use of the code. No license,
** express or implied, by estoppel or otherwise, to any intellectual property
** rights is granted herein.
**
**
** File Name: HAS_SIM_ENABLE.H
**
** Abstract:  Enables HAS. This can be done in a ClearCase config spec by
**            including:
**
**            element * .../DEV_ENABLE_HAS/LATEST
**
**+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#pragma once

//////////////////////////////////////////
// Enable driver simulation support code
// by defining HAS as "1".  Otherwise,
// define HAS as "0" for normal production
// builds.  This will remove sim support
// code
//////////////////////////////////////////

#if (_DEBUG || _RELEASE_INTERNAL)
#define HAS 1 // Set to "1" to enable simulation support
#else
#define HAS 0 // Should be set to "0" to remove simulation support
#endif

#define DFT_SIM 1 // Set to 1 to enable DFT simulation support
