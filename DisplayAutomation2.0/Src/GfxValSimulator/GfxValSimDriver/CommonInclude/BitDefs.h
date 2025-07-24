/*===========================================================================
; BitDefs.h
;----------------------------------------------------------------------------

INTEL CONFIDENTIAL
Copyright 2000-2014
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
;--------------------------------------------------------------------------*/
/////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// Platform specific defines
//
// This is for exclusive use between CSLStub, CSL & GAL. So don't include
// anything outside which has dependencies with HW_DEVICE_EXTENTION
//
/////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifndef BITDEFS_H
#define BITDEFS_H

///////////////////////////////////////////////////////////////////
//
// Bit definition
// Bit mask
//
///////////////////////////////////////////////////////////////////
#define BIT(x) (1 << x)

//////////////////////////////////////////////////////////
//
// Typedef to be used while describing bitwise structures
//
//////////////////////////////////////////////////////////
typedef unsigned __int64 SIZE64BITS;
typedef unsigned int     SIZE32BITS;
typedef unsigned short   SIZE16BITS;
typedef unsigned char    SIZE8BITS;

//////////////////////////////////////////////////////////
//
// Macro  to generate set of 1's given
// a range
// Bit mask
//
//////////////////////////////////////////////////////////
#define BITRANGE(ulHighBit, ulLowBit) ((((ULONG)(1 << ulHighBit) - 1) | (1 << ulHighBit)) & (~((ULONG)(1 << ulLowBit) - 1)))

//*****************************************************************************
// Macro: BITFIELD_RANGE
// PURPOSE: Calculates the number of bits between the startbit and the endbit
// and count is inclusive of both bits. The bits are 0 based.
//*****************************************************************************
#define BITFIELD_RANGE(ulLowBit, ulHighBit) ((ulHighBit) - (ulLowBit) + 1)

//*****************************************************************************
// Macro: BITFIELD_BIT
// PURPOSE: Used to declare single bit width
//*****************************************************************************
#define BITFIELD_BIT(bit) 1

// size in multiple of DWORD
#ifndef SIZE32
#define SIZE32(x) ((DWORD)(sizeof(x) / sizeof(DWORD)))
#endif

#endif // BITDEFS_H
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
