#ifndef __DPHANDLERS_H__
#define __DPHANDLERS_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "SIMDRV_GFX_COMMON.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"
#include "..\\DPCore\\AuxInterface.h"
#include "CommonIOCTL.h"
#include "DPIOCTL.h"

typedef struct _DP_SX_PLUGUNPLUG_DATA
{
    BOOLEAN          bPlugUnplugAtSource;
    DP_TOPOLOGY_TYPE eTopologyType;

    // If the new topology after S3 resume is SST. Below Data pertains to that:
    PUCHAR            pucNewSSTEDIDBuff; // If to be applied DP Topology after S3->Resume is SST, this buffer would hold the EDID
    ULONG             ulNewSSTEDIDSize;
    PUCHAR            pucNewSSTDPCDBuff;
    ULONG             ulNewSSTDPCDSize;
    PDPCD_CONFIG_DATA pstNewSSTDPCDConfigData;

    // If the new topology after S3 resume is SST. Below Data pertains to that:
    PVOID         pvNewDP12Topology; // In case a whole new topology is being added at source
    PUCHAR        pucBranch0DPCDBuff;
    ULONG         ulBranch0DPCDSize;
    PVOID         pvNewSubTopologyNode; // In case a subtopology is being added somewhere in the MST Topology
    UCHAR         ulNewNodeInputPort;
    UCHAR         ucReserved1;
    UCHAR         ucReserved2;
    UCHAR         ucReserved3;
    RAD_NODE_INFO stRADInfo; // RAD Information of the Node where the New Sub topology has to be added or deleted

} DP_SX_PLUGUNPLUG_DATA, *PDP_SX_PLUGUNPLUG_DATA;

typedef struct _DPCD_ADDR_VALUE_PAIR
{
    ULONG ulDPCDAddr;
    UCHAR ucDPCDVal;
} DPCD_ADDR_VALUE_PAIR, *PDPCD_ADDR_VALUE_PAIR;

PDPAUX_INTERFACE DPHANDLERS_DPInterfaceInit(PVOID pstRxInfoArr, PORT_TYPE ePortType);

BOOLEAN DPHANDLERS_InitDPTopologyType(PVOID pstRxInfoArr, PDP_INIT_INFO pstDPInitInfo);
BOOLEAN DPHANDLERS_SetEDIDData(PVOID pstRxInfoArr, PFILE_DATA pstEdidData);
BOOLEAN DPHANDLERS_SetDPCDData(PVOID pstRxInfoArr, PFILE_DATA pstEdidData);
BOOLEAN DPHANDLERS_SetDPMSTTopology(PVOID pstRxInfoArr, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArr);

BOOLEAN DPHANDLERS_ReadDPCD(PVOID pstRxInfoArr, PGET_DPCD_ARGS pstReadDPCDArgs, PUCHAR pucReadBuff);
BOOLEAN DPHANDLERS_WriteDPCD(PVOID pstRxInfoArr, PSET_DPCD_ARGS pstSetDPCDArgs);

BOOLEAN DPHANDLERS_GetMSTTopologyRADArray(PVOID pstRxInfoArr, PORT_TYPE ePortNum, PBRANCHDISP_RAD_ARRAY pstBranchDispRADArray);
BOOLEAN DPHANDLERS_ExtractCurrentTopologyInArrayFormat(PVOID pstRxInfoArr, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArray, PORT_TYPE ePortNum);
BOOLEAN DPHANDLERS_ExecuteConnectionStatusNotify(PVOID pstRxInfoArr, PVOID pGfxAdapterContext, PDP_SUBTOPOLOGY_ARGS pstCSNArgs);

BOOLEAN DPHANDLERS_SetDPCDModelData(PVOID pstRxInfoArr, PDP_DPCD_MODEL_DATA pstDpDPCDModelData);
BOOLEAN DPHANDLERS_SetDPCDModelDataForS3S4Cycle(PVOID pstRxInfoArr, PDP_DPCD_MODEL_DATA pstDpDPCDModelData);
BOOLEAN DPHANDLERS_SetPanelDpcd(PVOID pstRxInfoArr, PORT_TYPE ePortType, UINT16 Offset, UINT8 Value);

// MMIO Handlers
BOOLEAN DPHANDLERS_AuxDataReadHandler(PVOID pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DPHANDLERS_AuxDataWriteHandler(PVOID pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DPHANDLERS_AuxControlReadHandler(PVOID pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN DPHANDLERS_AuxControlWriteHandler(PVOID pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN DPHANDLERS_ConfigureDPGfxS3S4PlugUnplugData(PVOID pstRxInfoArr, PGFXS3S4_PORT_PLUGUNPLUG_DATA pstGfxS3S4PortPlugUnplugData);
BOOLEAN DPHANDLERS_HandleGfxPowerNotification(PVOID pstRxInfoArr, PORT_TYPE ePortType, PVOID pstRxS3S4PlugUnPlugData, DEVICE_POWER_STATE eGfxPowerState, POWER_ACTION eActionType,
                                              PORT_CONNECTOR_INFO PortConnectorInfo);

BOOLEAN DPHANDLERS_SetEDIDDataForS3S4Cycle(PVOID pstRxInfoArr, PFILE_DATA pstEdidData);
BOOLEAN DPHANDLERS_SetDPCDDataForS3S4Cycle(PVOID pstRxInfoArr, PFILE_DATA pstDPCDData);
BOOLEAN DPHANDLERS_SetDPMSTTopologyForS3S4Cycle(PVOID pstRxInfoArr, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArr);
BOOLEAN DPHANDLERS_AddOrRemoveSubtopologyForS3S4Cycle(PVOID pstRxInfoArr, PDP_SUBTOPOLOGY_ARGS pstSubTopologyArgs);

BOOLEAN DPHANDLERS_CleanUp(PVOID pstRxInfoArr, PORT_TYPE ePortType);

#endif