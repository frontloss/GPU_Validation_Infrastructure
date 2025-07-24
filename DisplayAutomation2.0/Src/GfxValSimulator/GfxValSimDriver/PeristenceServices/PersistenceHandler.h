#ifndef __PERSISTENCE_H__
#define __PERSISTENCE_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\DriverInterfaces\\CommonRxHandlers.h"
#include "..\\DriverInterfaces\\CommonIOCTL.h"
#include "..\\DriverInterfaces\\DPIOCTL.h"

#define SIGNATURE_HEADER                               \
    {                                                  \
        0x53, 0x61, 0x6E, 0x6A, 0x65, 0x65, 0x76, 0x00 \
    } // 0x0053616E6A656576ull
#define SIGNATURE_FOOTER                               \
    {                                                  \
        0x00, 0x4B, 0x75, 0x6D, 0x61, 0x72, 0x00, 0x00 \
    } // 0x0000004B756D6172ull

typedef struct _HDMI_PERSISTENCE_DATA
{
    PFILE_DATA   pstEDIDData;
    unsigned int uiDongleType;
    // PFILE_DATA pstEDIDDataS3S4;

} HDMI_PERSISTENCE_DATA, *PHDMI_PERSISTENCE_DATA;

// The below struct is used for both DP(SST/MST) and EDP.
// Certain fields like eTopologyType are only valid for DP not EDP
typedef struct _DP_PERSISTENCE_DATA
{
    DP_TOPOLOGY_TYPE eTopologyType;
    ULONG            ulNumEDIDs;                    // No. of Valid EDIDs  //Should be 1 for SST and eDP
    PFILE_DATA       pstEDIDData[MAX_NUM_DISPLAYS]; // Only Index 0 is used for SST and eDP
    // ULONG ulNumEDIDsS3S4;  //No. of Valid EDIDs  //Should be 1 for SST and eDP
    // PFILE_DATA pstEDIDDataS3S4[MAX_NUM_DISPLAYS]; //Only Index 0 is used for SST and eDP
    ULONG      ulNumDPCDs;                                       // No. of Valid DPCDs //Should be 1 for SST and eDP
    PFILE_DATA pstDPCDData[MAX_NUM_DISPLAYS + MAX_NUM_BRANCHES]; // Only Index 0 is used for SST and eDP
                                                                 // ULONG ulNumDPCDsS3S4;  //No. of Valid DPCDs //Should be 1 for SST and eDP
                                                                 // PFILE_DATA pstDPCDDataS3S4[MAX_NUM_DISPLAYS + MAX_NUM_BRANCHES]; // Only Index 0 is used for SST and eDP
    ULONG                  ulNumDPCDModelDatas;                  // No. of Valid DPCD model datas //Should be 1 for SST and eDP
    PDP_DPCD_MODEL_DATA    pstDpDPCDModelData[MAX_NUM_DISPLAYS + MAX_NUM_BRANCHES]; // Only Index 0 is used for SST and eDP
    PBRANCHDISP_DATA_ARRAY pstBranchDispDataArray;

} DP_PERSISTENCE_DATA, *PDP_PERSISTENCE_DATA;

typedef struct _PORT_PERSISTENCE_DATA
{
    ULONG                 ulPortNum;
    RX_TYPE               eRxType;
    PORT_CONNECTOR_INFO   uPortConnectorInfo;
    SINK_PLUGGED_STATE    eSinkPluggedState;
    HDMI_PERSISTENCE_DATA stHDMIPersistenceData;
    DP_PERSISTENCE_DATA   stDPPersistenceData;

} PORT_PERSISTENCE_DATA, *PPORT_PERSISTENCE_DATA;

typedef struct _SIMDRV_PERSISTENCE_DATA
{
    DP_FILEHANDLLE        stPersistenceFileHandle;
    ULONG                 ulNumEnumeratedPorts;
    PORT_PERSISTENCE_DATA stPortPersistenceData[MAX_ENCODERS];

} SIMDRV_PERSISTENCE_DATA, *PSIMDRV_PERSISTENCE_DATA;

#pragma pack(1)

typedef struct _PERSISTENCE_INFO_HEADER
{
    // We can include Checksup over the whole data bytes for added robustness but calculation would contribute to increased time latency
    UCHAR ucSignatureHeader[8]; // Can be used optionally
    ULONG ulPeristenceDataSize;
    // SIMDRV_PERSISTENCE_DATA follows here in the actual disk file
} PERSISTENCE_INFO_HEADER, *PPERSISTENCE_INFO_HEADER;

#pragma pack()

BOOLEAN PERSISTENCEHANDLER_InitPeristenceContext(PVOID pGfxAdapterContext, PSIMDRV_PERSISTENCE_DATA *ppstPersistenceData, PSIMDRV_PERSISTENCE_DATA *ppstPersistenceDataS3S4);

BOOLEAN PERSISTENCEHANDLER_CleanupPeristenceContext(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PSIMDRV_PERSISTENCE_DATA pstPersistenceDataS3S4);

BOOLEAN PERSISTENCEHANDLER_SetRxInfo(PPORT_INFO pstPortInfo, PSIMDRV_PERSISTENCE_DATA pstPersistenceData);

BOOLEAN PERSISTENCEHANDLER_SetEDIDData(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PFILE_DATA pstEdidData);

BOOLEAN PERSISTENCEHANDLER_SetDongleType(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PORT_TYPE ePortType, DONGLE_TYPE eDongleType);

BOOLEAN PERSISTENCEHANDLER_InitDPTopologyType(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PDP_INIT_INFO pstDPInitInfo);

BOOLEAN PERSISTENCEHANDLER_SetDPCDData(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PFILE_DATA pstDPCDData);

BOOLEAN PERSISTENCEHANDLER_SetDPCDModelData(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PDP_DPCD_MODEL_DATA pstDpDPCDModelData);

BOOLEAN PERSISTENCEHANDLER_SetDPMSTTopology(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArr);

BOOLEAN PERSISTENCEHANDLER_UpdateMSTTopologyToPersist(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PVOID pstRxInfoArr, PDP_SUBTOPOLOGY_ARGS pstCSNArgs);

BOOLEAN PERSISTENCEHANDLER_UpdatePortPluggedState(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, ULONG ulPortNum, SINK_PLUGGED_STATE eSinkPluggedState,
                                                  PORT_CONNECTOR_INFO PortConnectorInfo);

BOOLEAN PERSISTENCEHANDLER_ConfigurePeristenceForS3S4Path(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PVOID pstRxInfoArr,
                                                          PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA pstGfxS3S4AllPortsPlugUnplugData);

BOOLEAN PERSISTENCEHANDLER_UpdatePeristenceWithS3S4ResumeData(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PSIMDRV_PERSISTENCE_DATA pstPersistenceDataS3S4,
                                                              PRX_INFO_ARR pstRxInfoArr, DEVICE_POWER_STATE eGfxPowerState, POWER_ACTION eActionType);

BOOLEAN PERSISTENCEHANDLER_WritePeristenceDataToDisk(PSIMDRV_PERSISTENCE_DATA pstPersistenceData);

BOOLEAN PERSISTENCEHANDLER_ReadPeristenceDataFromDisk(PVOID pGfxAdapterContext);

BOOLEAN PERSISTENCEHANDLER_ReconstructSinkConfigFromPersistenceData(PVOID pGfxAdapterContext);

BOOLEAN PERSISTENCEHANDLER_CleanUpPort(PSIMDRV_PERSISTENCE_DATA pstPersistenceDataa, PORT_TYPE ePortNum);

BOOLEAN PERSISTENCEHANDLER_CleanUpAllPorts(PSIMDRV_PERSISTENCE_DATA pstPersistenceDataa);

BOOLEAN PERSISTENCEHANDLER_IsPersistenceFileOpen(PVOID pGfxAdapterContext);

#endif