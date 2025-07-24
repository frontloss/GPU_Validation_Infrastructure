/*************************************************************************
**                                                                      **
**                    I N T E L   C O N F I D E N T I A L               **
**       Copyright (c) 2016 Intel Corporation All Rights Reserved.      **
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
 * file name       GfxValStub_GenericGfxAccess.h
 * Date:           27/01/2015
 * @version        0.1
 * @Author         Naveen SG /Amit
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

#ifndef GVSTUB_GENERIC_GFX_ACCESS_H
#define GVSTUB_GENERIC_GFX_ACCESS_H

#include "GfxValStub_MetaData.h"

// Gfx Driver and Validation Driver/App should communicate w/o structure packing
#pragma pack(push, GFX_VAL_STUB_GFX_ACCESS)
#pragma pack(1)
/* To avoid warning*/
#pragma warning(disable : 4201)
#pragma warning(disable : 4214)

#define GVSTUB_GENERIC_GFX_ACCESS_VERSION 0x1

// Error codes used by Gfx and Validation Driver to indicate the operation success/failure in this layer
#define GVSTUB_GENERIC_ACCESS_SUCCESS 0x00000000
#define GVSTUB_GENERIC_ACCESS_VERSION_MISMATCH 0x00000001
#define GVSTUB_GENERIC_ACCESS_NO_MEMORY 0x00000002
#define GVSTUB_GENERIC_ACCESS_INVALID_REQUEST 0x00000004
#define GVSTUB_GENERIC_ACCESS_FAILURE 0x00000008
#define GVSTUB_GENERIC_ACCESS_SIZE_MISMATCH 0x00000010
#define GVSTUB_GENERIC_ACCESS_DENIED 0x00000020

#define MAX_DATA_SIZE (1024 * 1)

// status can be set only if ValStubFeatureArg exits
#define __GVSTUB_GENERIC_ACCESS_NULLPTR(expr, status)                                                     \
    {                                                                                                     \
        if (!expr)                                                                                        \
        {                                                                                                 \
            if (pValStubFeatureArgs)                                                                      \
            {                                                                                             \
                pValStubFeatureArgs->stGenericGfxAccessArgs.stGenericGfxAccessMetaData.ulStatus = status; \
            }                                                                                             \
            return;                                                                                       \
        }                                                                                                 \
    }

typedef enum _GVSTUB_GENERIC_GFX_ACCESS_REQUEST_TYPE
{
    GVSTUB_GENERIC_ACCESS_UNKNOWN,
    GVSTUB_READ_MMIO,
    GVSTUB_WRITE_MMIO,
    GVSTUB_IOSF_SB_ACCESS,
    GVSTUB_READ_GFX_REGISTRY,
    GVSTUB_WRITE_GFX_REGISTRY,
    GVSTUB_ADAPTER_INFO_ACCESS,
    GVSTUB_ADAPTER_DRIVER_CAPS,
    GVSTUB_ADAPTER_GPUMMU_CAPS,
    GVSTUB_GENERIC_REQUEST_TYPE_MAX
} GVSTUB_GENERIC_GFX_ACCESS_REQUEST_TYPE;

#pragma region Structure Defination for MMIO Access Start
/*
Structure defination for read MMIO/Write MMIO operation
*/
typedef struct _GVSTUB_MMIO_ACCESS_ARGS
{
    IN ULONG ulOffset;    // Offset of the MMIO register to be read.
    IN_OUT ULONG ulValue; // Value of the MMIO register at the given offset.
} GVSTUB_MMIO_ACCESS_ARGS, *PGVSTUB_MMIO_ACCESS_ARGS;
#pragma endregion Structure Defination for MMIO Access End

#pragma region Structure Defination for IOSF SB Register Access Start
// Access type
#define GVSTUB_IOSF_SB_READ 0
#define GVSTUB_IOSF_SB_WRITE 1

/*
Structure Defination for IOSFSB_ACCESS (read and wright operation)
*/
typedef struct _GVSTUB_IOSFSB_ACCESS_ARGS
{
    IN BOOLEAN bAccessType;             // 0-Read, 1-Write.
    IN ULONG ulOpcode;                  // Opcode to be used for the transaction.
    IN ULONG ulPortID;                  // Destination PortID
    IN ULONG ulRoutingID;               // SideBand Routing ID
    IN ULONG ulOffset;                  // Offset of the register to be accessed
    IN_OUT ULONG ulDataSize;            // Data Size for Read/Write Transactions. # of bytes.
    IN_OUT ULONG ulData[MAX_DATA_SIZE]; // Data Buffer for Read/Write Transactions
} GVSTUB_IOSFSB_ACCESS_ARGS, *PGVSTUB_IOSFSB_ACCESS_ARGS;
#pragma endregion Structure Defination for IOSF SB Register Access End

#pragma region Structure for Registry Access Start

/*
Structure for Registry Service Key
*/
typedef enum _GVSTUB_REGISTRY_SERVICE_TYPE
{
    GVSTUB_REG_ABSOLUTE   = 0, // Path is a full path
    GVSTUB_REG_SERVICES   = 1, // HKLM\System\System\CurrentControlSet\Services
    GVSTUB_REG_CONTROL    = 2, // HKLM\System\System\CurrentControlSet\Control
    GVSTUB_REG_WINDOWS_NT = 3, // HKLM\Software\Microsoft\Windows NT\CurrentVersion
    GVSTUB_REG_DEVICEMAP  = 4, // HKLM\Hardware\DeviceMap
    GVSTUB_REG_USER       = 5, // HKCU
} GVSTUB_REGISTRY_SERVICE_TYPE;

/*
Structure for Miniport supported Keys and value
Specify absolute registry path or a path relative to the known location specified by GVSTUB_REGISTRY_SERVICE_TYPE
*/
typedef enum _GVSTUB_REGISTRY_KEY_TYPE
{
    GVSTUB_REG_GENERAL_KEY,        // Specify Empty relative path
    GVSTUB_REG_DISP1_KEY,          // Specify Empty relative path
    GVSTUB_REG_DISP2_KEY,          // Specify Empty relative path
    GVSTUB_REG_SERVICE_KEY,        // Specify Empty relative path
    GVSTUB_REG_OPMSRM_HEADER_KEY,  // relative path is "PersistentDataH"
    GVSTUB_REG_OPMSRM_VRL_KEY,     // relative path is "PersistentDataL"
    GVSTUB_REG_OPMSRM_VRL_LEN_KEY, // relative path is "PersistentDataLen"
} GVSTUB_REGISTRY_KEY_TYPE;

/*
Structure defination for read and write registry.
*/
typedef struct _GVSTUB_REGISTRY_ACCESS_ARGS
{
    IN GVSTUB_REGISTRY_SERVICE_TYPE eRelativeTo;
    IN GVSTUB_REGISTRY_KEY_TYPE eKeyType;
    IN wchar_t ValueName[MAX_DATA_SIZE];
    IN ULONG ulValueType;
    IN_OUT CHAR ValueData[MAX_DATA_SIZE];
    IN ULONG ulMaxValueLength;
} GVSTUB_REGISTRY_ACCESS_ARGS, *PGVSTUB_REGISTRY_ACCESS_ARGS;
#pragma endregion Structure for Registry Access End

/**++
Structure for perform Generic GFX Access
In this stage Data Structure is defined as [Header2 + Data]

Header2 -> GVSTUB_META_DATA
Data can be any one of GVSTUB_MMIO_ACCESS_ARGS/GVSTUB_IOSFSB_ACCESS_ARGS/GVSTUB_REGISTRY_ACCESS_ARGS etc

Meta data is used for below specific reason
the size of Input data (ie sizeof(GVSTUB_META_DATA) + sizeof(GVSTUB_MMIO_ACCESS_ARGS) - as a example
ulServiceType as GVSTUB_GENERIC_GFX_ACCESS_REQUEST_TYPE type.
ulStatus will specify Status of Generic GFX Access Call
All Generic GFX Access Error code is defined in this file.
*/
typedef struct _GVSTUB_GENERIC_GFX_ACCESS_ARGS
{
    IN_OUT GVSTUB_META_DATA stGenericGfxAccessMetaData;
    union {
        IN_OUT GVSTUB_MMIO_ACCESS_ARGS stMmioAccessArgs;
        IN_OUT GVSTUB_IOSFSB_ACCESS_ARGS stIosfSbAccessArgs;
        IN_OUT GVSTUB_REGISTRY_ACCESS_ARGS stRegistryAccessArgs;
        // any new Generic GFX access service data structure should be added here.
    };
} GVSTUB_GENERIC_GFX_ACCESS_ARGS, *PGVSTUB_GENERIC_GFX_ACCESS_ARGS;

#pragma pack(pop, GFX_VAL_STUB_GFX_ACCESS)

#endif