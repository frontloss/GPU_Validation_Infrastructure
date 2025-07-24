/**
 * @file
 * @section VbtAccess_h
 * @brief Internal header file which contains data structures and function declarations required for
 * VBT Get and Set through DFT calls.
 *
 * @ref VbtAccess.h
 * @author Sri Sumanth Geesala
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

/** User defined header files*/
#include <Windows.h>
#include "SystemUtility.h"
#include "DivaAccess.h"
#include "CommonDetails.h"

#define GVSTUB_VBT_MAX_SIZE 8192
#define VBT_HEADER_SIZE_OFFSET 22
#define VBT_CHECKSUM_OFFSET 26

#pragma pack(1)
typedef struct _VBT_BIOS_DATA_HEADER
{
    UCHAR  BDB_Signature[16];
    USHORT BDB_Version;
    USHORT BDB_Header_Size;
    USHORT BDB_Size;
} VBT_BIOS_DATA_HEADER, *PVBT_BIOS_DATA_HEADER;

typedef struct _VBT_DATA_BLOCK
{
    UCHAR ucId;  // BIOS Data Block ID. Always first
    WORD  wSize; // Size of this block
    // Variable size Actual Data.
} VBT_DATA_BLOCK, *PVBT_DATA_BLOCK;
#pragma pack()

/**
 * @brief			Helper function to fill GVSTUB MetaData and make the DFT call.
 *
 * @param[inout]		pValStubFeatureInfo pointer to GVSTUB_FEATURE_INFO_ARGS with filled in feature args (stGetSetVBT) is passed. VBT data can get in and out with these args.
 * @return			returns True if call passed, returns False otherwise.
 */
BOOL GetSetVbtDFT(PGVSTUB_FEATURE_INFO_ARGS pValStubFeatureInfo);