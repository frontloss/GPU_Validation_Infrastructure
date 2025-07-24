#ifndef __COMMONRXHANDLERS_H__
#define __COMMONRXHANDLERS_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"
#include "..\\DPCore\\AuxInterface.h"
#include "..\\HDMICore\\HDMIInterface.h"
#include "CommonIOCTL.h"
#include "DPIOCTL.h"
#include "..\\GenMMIOHandlers\\CommonMMIO.h"
#include "DPHandlers.h"
#include "HDMIHandlers.h"

typedef struct _RX_S3S4_PLUGUNPLUG_DATA
{
    // Sx Cycles Related Fields
    PLUG_REQUEST eRxS3S4PlugRequest;

    union _UNNAMED_UNION_TAG {
        DP_SX_PLUGUNPLUG_DATA   stS3S4DPPlugData;
        HDMI_SX_PLUGUNPLUG_DATA stS3S4HDMIPlugData;
    };

} RX_S3S4_PLUGUNPLUG_DATA, *PRX_S3S4_PLUGUNPLUG_DATA;

typedef struct _RX_INFO_OBJ
{
    PORT_TYPE           ePortNum;
    SINK_PLUGGED_STATE  eSinkPluggedState;
    RX_TYPE             eRxType;
    PORT_CONNECTOR_INFO uPortConnectorInfo; // This will hold the info like Connector type is TC/TBT and this value will be updated during plug(normal/power events)
    PDPAUX_INTERFACE    pstDPAuxInterface;
    PHDMI_INTERFACE     pstHDMIInterface;

    RX_S3S4_PLUGUNPLUG_DATA stRxS3S4PlugUnplugData;

} RX_INFO_OBJ, *PRX_INFO_OBJ;

typedef struct _RX_INFO_ARR
{
    ULONG           ulNumEnumeratedPorts;
    PMMIO_INTERFACE pstMMIOInterface;
    RX_INFO_OBJ     stRxInfoObj[MAX_ENCODERS];

} RX_INFO_ARR, *PRX_INFO_ARR;

BOOLEAN          COMMONRxHANDLERS_InitSimulationDriverContext(PVOID gfxAdapterContext, PRX_INFO_ARR *ppstRxInfoArr);
BOOLEAN          COMMONRXHANDLERS_SetRxInfo(PPORT_INFO pstPortInfo, PRX_INFO_ARR pstRxInfoArr);
PDPAUX_INTERFACE COMMRXHANDLERS_GetAuxInterfaceFromPortType(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType);
RX_TYPE          COMMRXHANDLERS_GetRxTypeFromPortType(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType);
void             COMMRXHANDLERS_FreeAuxInterfaceForPort(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType);
PHDMI_INTERFACE  COMMRXHANDLERS_GetHDMIInterfaceFromPortType(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType);

BOOLEAN COMMRXHANDLERS_SetEDIDData(PRX_INFO_ARR pstRxInfoArr, PFILE_DATA pstEdidData, BOOLEAN bIsEDIDForS3S4Cycle);

BOOLEAN COMMRXHANDLERS_SetPortPluggedState(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, SINK_PLUGGED_STATE eSinkPluggedState, PORT_CONNECTOR_INFO PortConnectorInfo);

BOOLEAN COMMRXHANDLERS_ConfigureAllPortsGfxS3S4PlugUnplugData(PRX_INFO_ARR pstRxInfoArr, PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA pstGfxS3S4AllPortsPlugUnplugData);

PRX_S3S4_PLUGUNPLUG_DATA COMMRXHANDLERS_GetRxS3S4PlugUnPlugDataPtr(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, RX_TYPE eRxType);

BOOLEAN COMMRXHANDLERS_GfxPowerStateNotification(PRX_INFO_ARR pstRxInfoArr, DEVICE_POWER_STATE eGfxPowerState, POWER_ACTION eActionType);

BOOLEAN COMMRXHANDLERS_CleanUpPort(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortNum);

BOOLEAN COMMRXHANDLERS_CleanUpAllPorts(PRX_INFO_ARR pstRxInfoArr);

PORT_CONNECTOR_INFO COMMRXHANDLERS_GetConnectorInfo(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType);

BOOLEAN COMMRXHANDLERS_SetConnectorInfo(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo);

BOOLEAN COMMRXHANDLERS_SetDongleType(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, DONGLE_TYPE eDongleType);
BOOLEAN COMMRXHANDLERS_SetPanelDpcd(PVOID pstRxInfoArr, PORT_TYPE ePortType, UINT16 offset, UINT8 value);

#endif