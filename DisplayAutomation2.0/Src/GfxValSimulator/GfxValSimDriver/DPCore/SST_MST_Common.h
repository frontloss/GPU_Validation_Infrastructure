#ifndef __SST_MST_COMMON_H__
#define __SST_MST_COMMON_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\DriverInterfaces\\DPCoreIOCTLCommonDefs.h"

#define I2C_EDID_SLAVE_ADDRESS 0x50u
#define I2C_EDID_SEGPTR_ADDRESS 0x30u
#define I2C_EDID_DEFAULT_SEGPTR 0x0u
#define SIZE_EDID_BLOCK 128u
#define I2CAUX_START_TXN_SIZE 3u
#define MAX_NUM_EDID_BLOCKS 10

// This value is same as the NODE_NAME_STR_SIZE
#define MAX_NODE_NAME_SIZE 40

typedef enum _ACCESS_TYPE
{
    eWrite             = 0,
    eRead              = 1,
    eWriteStatusUpdate = 2 // This is only valid for I2C-over-Aux transaction
} ACCESS_TYPE;

typedef struct _TIMER_CB_CONTEXT
{
    PULONG pulTimerScheduleCount;
    PVOID  pvCallBackContext;

} TIMER_CB_CONTEXT, *PTIMER_CB_CONTEXT;

typedef struct _DPCD_CONFIG_DATA
{
    DPCD_MODEL_DATA stDPCDModelData;
    UCHAR           ucDPCDTransactionIndex;
} DPCD_CONFIG_DATA, *PDPCD_CONFIG_DATA;

#endif
