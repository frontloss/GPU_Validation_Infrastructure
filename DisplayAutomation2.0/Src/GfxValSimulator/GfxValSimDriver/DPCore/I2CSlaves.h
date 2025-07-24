#ifndef __I2CSLAVES_H__
#define __I2CSLAVES_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "SST_MST_Common.h"

// You can register max upto 4 offset ranges per slave info in case different i2c slave addresses have handling interterdependancy so need to share data
// e.g. I2C_EDID_SEGPTR_ADDRESS (0x30) and (0x50) are DDC slave addresses. Inspite of being two different addresses they work together for EDID fetching by the source.
//     Source uses I2C_EDID_SEGPTR_ADDRESS to set the EDID 256bytes block pointer. So we need one SlaveInfo mainting the state of transactions on both these I2C slave offsets
//
//    ***********THIS KIND OF APPROACH CAN BE ADDOPTED FOR MMIO HANDLER RERGISTRATION TOO  IF NEEDED**************
#define MAX_OFFSETRANGE_PER_SLAVEINFO 4

typedef BOOLEAN (*PFN_I2CSLAVEHANDLER)(void *pstI2CSlaveInfo);
typedef BOOLEAN (*PFN_I2CSLAVEINITROUTINE)(void *pstI2CSlaveInfo, PVOID pvCallerNonPersistedData, ULONG ulNonPersistedSize);
typedef BOOLEAN (*PFN_I2CSLAVECLEANUPROUTINE)(void *pstI2CSlaveInfo);

typedef struct _I2CSLAVE_OFFSETS
{
    ULONG ulSlaveStartAddress;
    ULONG ulSlaveEndAddress;

} I2CSLAVE_OFFSETS, *PI2CSLAVE_OFFSETS;

typedef struct _SLAVEOFFSETS_ARRAY
{
    ULONG            ulNumOffsetRanges;
    I2CSLAVE_OFFSETS stI2CSlaveOffsets[MAX_OFFSETRANGE_PER_SLAVEINFO];

} SLAVEOFFSETS_ARRAY, *PSLAVEOFFSETS_ARRAY;

typedef struct _I2C_SLAVE_INFO
{
    DP_LIST_ENTRY DPListEntry;

    SLAVEOFFSETS_ARRAY stSlaveOffsetsArray;

    ULONG       ulCurrTransAddr;
    ULONG       ulCurrTransLen;
    ACCESS_TYPE eCurrAccessType;
    ULONG       ulCurrentSlaveOffset;
    // Identify start of transaction. Set to TRUE if it is a Start of Transaction.
    BOOLEAN bIsIndexWrite;

    ULONG  ulSlaveTransBuffSize;
    PUCHAR pucSlaveIntermediateDataBuff;

    PVOID pvI2CSlavePvtData;

    PVOID pvCallNonPersistedData;
    // The guy that register's this client is responsible to persist this context if as long as this client's handlers' are called
    // What this data is depends on the client
    PVOID pvCallerPersistedContext;

    PFN_I2CSLAVEINITROUTINE pfnI2CSlaveUpdateRoutine;

    PFN_I2CSLAVEHANDLER pfnI2CSlaveReadHandler;
    PFN_I2CSLAVEHANDLER pfnI2CSlaveWriteHandler;

    PFN_I2CSLAVECLEANUPROUTINE pfnI2CSlaveCleanUpRoutine;

} I2C_SLAVE_INFO, *PI2C_SLAVE_INFO;

typedef struct _EDID_HOUSEKEEPING_DATA
{
    UCHAR  ucDisplayName[MAX_NODE_NAME_SIZE]; // Not being used currently
    ULONG  ulNumEdidBlocks;
    PUCHAR pucEDIDBlocks[MAX_NUM_EDID_BLOCKS];

    ULONG ulLastSegPtrVal;
    ULONG ulLastWriteOffset;
    ULONG ulBlockByteOffset;

} EDID_HOUSEKEEPING_DATA, *PEDID_HOUSEKEEPING_DATA;

BOOLEAN I2CSLAVES_DDCEDIDUpdateRoutine(PI2C_SLAVE_INFO pstI2CSlaveInfo, PUCHAR pucEDIDBuff, ULONG ulEdidSize);
BOOLEAN I2CSLAVES_DDCEDIDHandler(PI2C_SLAVE_INFO pstI2CSlaveInfo);

BOOLEAN I2CSLAVES_DDCEDIDCleanUpRoutine(PI2C_SLAVE_INFO pstI2CSlaveInfo);

#endif