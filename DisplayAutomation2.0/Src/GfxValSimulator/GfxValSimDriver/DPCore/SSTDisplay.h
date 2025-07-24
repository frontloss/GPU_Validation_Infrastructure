#ifndef __SSTDISPLAY_H__
#define __SSTDISPLAY_H__

#include "I2CSlaves.h"
#include "..\\DriverInterfaces\\DPCoreIOCTLCommonDefs.h"

BOOLEAN (*PFN_I2CSLAVE_INITIALIZE)(PI2C_SLAVE_INFO pstI2CSlaveInfo);

typedef struct _SST_DISPLAY_INFO
{

    ACCESS_TYPE eOngoingAccessType;
    ULONG       ulCurrTransactionAddr;
    BOOLEAN     bTransStarted;

    ULONG ulNumI2CSlaves;

    // TBD: Change this from link list to array implementation to simplify
    DP_LIST_HEAD I2CSlaveInfoListHead; // I2C Slave List for SST I2C Slaves

    DPCD_CONFIG_DATA stDPCDConfigData;

} SST_DISPLAY_INFO, *PSST_DISPLAY_INFO;

PSST_DISPLAY_INFO SSTDISPLAY_SSTDisplayInit(void);

BOOLEAN SSTDISPLAY_SetEDIDData(PSST_DISPLAY_INFO pstSSTDisplayInfo, ULONG ulEDIDSize, PUCHAR pucEDIDBuff);

BOOLEAN SSTDISPLAY_Cleanup(PSST_DISPLAY_INFO pstSSTDisplayInfo);

#endif