#ifndef __HDMIHANDLERS_H__
#define __HDMIHANDLERS_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "SIMDRV_GFX_COMMON.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"
#include "..\\HDMICore\\HDMIInterface.h"
#include "CommonIOCTL.h"
#include "HDMIIOCTL.h"

typedef struct _HDMI_SX_PLUGUNPLUG_DATA
{
    BOOLEAN      bPlugUnplugAtSource;
    PUCHAR       pucNewHDMIEDIDBuff; // If to be applied DP Topology after S3->Resume is SST, this buffer would hold the EDID
    ULONG        ulNewHDMIEDIDSize;
    unsigned int uiDongleType;

} HDMI_SX_PLUGUNPLUG_DATA, *PHDMI_SX_PLUGUNPLUG_DATA;

PHDMI_INTERFACE HDMIHANDLERS_HDMIInterfaceInit(PVOID pstRxInfoArr, PORT_TYPE ePortType);
BOOLEAN         HDMIHANDLERS_SetEDIDData(PVOID pstRxInfoArr, PFILE_DATA pstEdidData);
BOOLEAN         HDMIHANDLERS_SetEDIDDataForS3S4Cycle(PVOID pstRxInfoArr, PFILE_DATA pstEdidData);
BOOLEAN         HDMIHANDLERS_GMBUSReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN         HDMIHANDLERS_GMBUSWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN         HDMIHANDLERS_EDID_SCDC_CleanUp(PHDMI_INTERFACE pstHDMIInterface, PORT_TYPE ePortType);
BOOLEAN         HDMIHANDLERS_CleanUp(PVOID pstRxInfoArr, PORT_TYPE ePortType);
BOOLEAN         HDMIHANDLERS_ConfigureDPGfxS3S4PlugUnplugData(PVOID pstRxInfoArr, PVOID pstGfxS3S4PortPlugUnplugData);
BOOLEAN HDMIHANDLERS_HandleGfxPowerNotification(PVOID pstRxInfoArr, PORT_TYPE ePortType, PVOID pstRxS3S4PlugUnPlugData, DEVICE_POWER_STATE eGfxPowerState, POWER_ACTION eActionType,
                                                PORT_CONNECTOR_INFO PortConnectorInfo);
BOOLEAN HDMIHANDLERS_SetSCDCData(PVOID pstRxInfoArr, PFILE_DATA pstScdcData);

BOOLEAN HDMIHANDLERS_SetDongleType(PVOID pstRxInfoArr, PORT_TYPE ePortType, DONGLE_TYPE eDongleType);

#endif
