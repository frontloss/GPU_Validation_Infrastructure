/*************************************************************************
**                                                                      **
**                    I N T E L   C O N F I D E N T I A L               **
**       Copyright (c) 2015 Intel Corporation All Rights Reserved.      **
**                                                                      **
**  The source code contained or described herein and all documents     **
**  related to the source code ("Material") are owned by Intel          **
**  Corporation or its suppliers or licensors. Title to the Material    **
**  remains with Intel Corporation or its suppliers and licensors. The  **
**  Material contains trade secrets and proprietary and confidential    **
**  information of Intel or its suppliers and licensors. The Material   **
**  is protected by worldwide copyright and trade secret laws and       **
**  treaty provisions. No part of the Material may be used, copied,     **
**  reproduced, modified, published, uploaded, posted, transmitted,     **
**  distributed, or disclosed in any way without Intel's prior express  **
**  written permission.                                                 **
**                                                                      **
**  No license under any patent, copyright, trade secret or other       **
**  intellectual property right is granted to or conferred upon you by  **
**  disclosure or delivery of the Materials, either expressly, by       **
**  implication, inducement, estoppel or otherwise. Any license under   **
**  such intellectual property rights must be express and approved by   **
**  Intel in writing.                                                   **
**                                                                      **
*************************************************************************/

/**
 * file name       GfxValStub_MetaData.h
 * Date:           04/02/2015
 * @version        0.1
 * @Author		  Naveen SG /Amit
 * Modified by
 * Description:
 */

/*
*********************************************************************************************
*********************************************************************************************
GVSTUB is an acronym for 'GFX VAL STUB'
*********************************************************************************************
*********************************************************************************************
*/

#ifndef GVSTUB_META_DATA_H
#define GVSTUB_META_DATA_H

// Gfx Driver and Validation Driver/App should communicate w/o structure packing
#pragma pack(push, GFX_VAL_STUB_META_DATA)
#pragma pack(1)

#ifdef IN
#undef IN
#endif

#ifdef OUT
#undef OUT
#endif

#ifdef IN_OUT
#undef IN_OUT
#endif

#define IN _In_
#define OUT _Out_
#define IN_OUT _Inout_
#define RESERVED _Reserved_
#define IN_OUT_OPT _Inout_opt_

// It is structure acting as Data header in each level.

typedef struct _GVSTUB_META_DATA
{
    IN ULONG   ulSize;
    IN_OUT_OPT ULONG ulVersion;
    IN ULONG ulServiceType;
    RESERVED ULONG ulReserved1;
    RESERVED ULONG ulReserved2;
    RESERVED ULONG ulReserved3;
    OUT ULONG ulStatus; // status field to be checked based on each layer error code.
} GVSTUB_META_DATA, *PGVSTUB_META_DATA;

#pragma pack(pop, GFX_VAL_STUB_META_DATA)

#endif