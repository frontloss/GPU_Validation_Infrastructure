#ifndef __AUXINTERFACE_H__
#define __AUXINTERFACE_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "AuxDefs.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"
#include "..\\DriverInterfaces\\DPCoreIOCTLCommonDefs.h"
#include "MSTTopology.h"
#include "SSTDisplay.h"
#include "I2CSlaves.h"

#define ALL_DP_PORTS 0xFFFFFFFFu
#define MAX_CURRENT_DPCDS_SUPPORTED 0xF1000
#define MAX_REGISTERED_DPCD_CLIENTS 50
#define NUM_BACKUP_DPCD_BUFF_SIZE 1000 // We can handle thousand random DPCD Accesses

typedef BOOLEAN (*PFN_DPCDCLIENT)(void *pDPCDClientInfo);
typedef BOOLEAN (*PFN_DPCDCLIENT_PRIVATEDATA_INIT)(void *pDPCDClientInfo, PVOID pvCallerNonPersistedData, ULONG ulNonPersistedSize);
typedef BOOLEAN (*PFN_DPCDCLIENT_CLEANUP_HANDLER)(void *pDPCDClientInfo);

typedef enum _REGISTRATION_RESULT
{
    eRegistrationFailed  = 0,
    eRegistrationSuccess = 1,
    eAlreadyRegistered   = 2,

} REGISTRATION_RESULT,
*PREGISTRATION_RESULT;

typedef struct _CLIENT_TIMEOUT_DATA
{
    BOOLEAN bTimeout;
    BOOLEAN bTimeoutAlways;
    BOOLEAN bTimeOutOnlyFirstTime;
    ULONG   ulCurrTimeoutCount;
    ULONG   ulMaxTimeoutCount;

} CLIENT_TIMEOUT_DATA, *PCLIENT_TIMEOUT_DATA;

typedef struct _CLIENT_DEFER_DATA
{
    BOOLEAN bDefer;
    BOOLEAN bDeferAlways;
    BOOLEAN bDeferOnlyFirstTime;
    ULONG   ulCurrDeferCount;
    ULONG   ulMaxDeferCount;

} CLIENT_DEFER_DATA, *PCLIENT_DEFER_DATA;

typedef struct _CLIENT_NACK_DATA
{
    BOOLEAN bNack;
    BOOLEAN bNackAlways;
    BOOLEAN bNackOnlyFirstTime;
    ULONG   ulCurrNackCount;
    ULONG   ulMaxNackCount;

} CLIENT_NACK_DATA, *PCLIENT_NACK_DATA;

typedef struct _CLIENT_RECEIVERROR_DATA
{
    BOOLEAN bReceiveError;
    BOOLEAN bReceiveErrorAlways;
    BOOLEAN bReceiveErrorOnlyFirstTime;
    ULONG   ulCurrReceiveErrorCount;
    ULONG   ulMaxReceiveErrorCount;

} CLIENT_RECEIVERROR_DATA, *PCLIENT_RECEIVERROR_DATA;

typedef struct _CLIENT_PARTIALWRITE_DATA
{
    BOOLEAN bPartialWrite;
    BOOLEAN bPartialWriteAlways;
    BOOLEAN bPartialWriteOnlyFirstTime;
    UCHAR   ucCurrPartialWriteCount;
    UCHAR   ucMaxPartialWriteCount;
    UCHAR   ucNumOfPartialBytesToWrite;

} CLIENT_PARTIALWRITE_DATA, *PCLIENT_PARTIALWRITE_DATA;

typedef struct _AUX_ERROR_PARAMS
{
    CLIENT_TIMEOUT_DATA      stTimeoutData;
    CLIENT_DEFER_DATA        stDeferData;
    CLIENT_NACK_DATA         stNackData;
    CLIENT_RECEIVERROR_DATA  stReceiveErrorData;
    CLIENT_PARTIALWRITE_DATA stPartialWriteData;

} AUX_ERROR_PARAMS, *PAUX_ERROR_PARAMS;

typedef struct _DPCD_CLIENTINFO
{
    DP_LIST_ENTRY DPListEntry;
    ULONG         ulDPCDStartAddress;
    ULONG         ulDPCDEndAddress;

    // In case client wants to register a single function for both DPCD read and write. It can use this fielt to know what kind of DPCD access
    // it was
    ACCESS_TYPE eAccessType;

    HANDLE            hThreadHandleReadClient;
    ULONG             ulThreadIDReadClient;
    DP_EVENT          stReadHandlerThreadEvent;
    UCHAR             ucPrimaryReadBuffer[AUX_MAX_TXN_LEN];
    PAUX_ERROR_PARAMS pstReadErrorParams;
    PFN_DPCDCLIENT    pfnDPCDReadClient;

    HANDLE            hThreadHandleWriteClient;
    ULONG             ulThreadIDWriteClient;
    DP_EVENT          stWriteHandlerThreadEvent;
    UCHAR             ucPrimaryWriteBuffer[AUX_MAX_TXN_LEN];
    PAUX_ERROR_PARAMS pstWriteErrorParams;
    PFN_DPCDCLIENT    pfnDPCDWriteClient;

    DP_EVENT stThreadedClientResponseEvent;

    // Thread Client can return a FALSE in the bClientResponse field to the caller (Data Reg Processor) which would mean its telling the caller
    // that it found some issues while handling the request (Unexpected or corrupt data) and it wants the caller to send a NACK
    // to the source. If the request was handled successfully by the client then bClientResponse should be set to TRUE
    BOOLEAN bThreadClientResponse;

    PVOID pvClientPrivateData;

    // The guy that register's this client is responsible to persist this context if as long as this client's handlers' are called
    // What this data is depends on the client
    PVOID pvCallerPersistedContext;

    // Current Transaction dynamic details that would refresh everytime this client gets called
    ULONG ulCurrTransactionAddr;
    UCHAR ucCurrTransactionLen;

    PUCHAR pucClientDPCDMap;

    PFN_DPCDCLIENT_CLEANUP_HANDLER pfnClientCleanupHandler;

} DPCD_CLIENTINFO, *PDPCD_CLIENTINFO;

typedef struct _CLIENT_INFO_ARRAY
{
    ULONG           ulNumRegisteredClients;
    DPCD_CLIENTINFO ulDPCDClientList[MAX_REGISTERED_DPCD_CLIENTS];

} CLIENT_INFO_ARRAY, *PCLIENT_INFO_ARRAY;

typedef struct _BACKUP_DPCD_BUFF
{
    ULONG ulStartOffset;
    UCHAR ucValue;
    UCHAR ucReserved1;
    UCHAR ucReserved2;
    UCHAR ucReserved3;

} BACKUP_DPCD_BUFF, *PBACKUP_DPCD_BUFF;

typedef struct _BACKUP_DPCD_BUFF_ARR
{
    ULONG            ulCurrentFilledSize;
    BACKUP_DPCD_BUFF BackupDPCDBuff[NUM_BACKUP_DPCD_BUFF_SIZE];

} BACKUP_DPCD_BUFF_ARR, *PBACKUP_DPCD_BUFF_ARR;

typedef struct _DPAUX_INTERFACE
{
    SINGLE_LIST_ENTRY   pListEntry; // This is redundant I think, remove later?
    BOOLEAN             bInterfaceInitalized;
    DP_TOPOLOGY_TYPE    eTopologyType;
    ULONG               ulThreadIDDataRegProcessor;
    DP_EVENT            stDataRegProcessorThreadEvent;
    DP_EVENT            stDataRegProcessorKillEvent;
    PORT_TYPE           ePortNum; // PORT_TYPE?
    ULONG               ulOffsetAuxCtl;
    PAUX_CTRLREG_STRUCT pstAuxCtlReg;
    ULONG               ulOffsetAuxDataStart;
    ULONG               ulOffsetAuxDataEnd;
    PAUX_DATAREG_STRUCT pstAuxDataRegs;

    // Registered Client List
    // DP_LIST_HEAD  DPCDClientListHead;
    CLIENT_INFO_ARRAY stClientInfoArray;

    // Only one of the below i.e SST or MST structure would be valid at any given time or during a simulation
    // SST Display Details
    PSST_DISPLAY_INFO pstSSTDisplayInfo;

    // MST Topology Details
    PDP12_TOPOLOGY pstDP12Topology;
    // PUCHAR pstDP12Topology;

    ULONG ulDPCDBuffSize;
    // This will point to the DPCD buffer of directly connected downstream device: Branch DPCD buff for MST and Display DPCD buff for SST
    PUCHAR pucDownStreamDPCDBuff; // This will be used for both MST and SST for native aux read and writess

    BACKUP_DPCD_BUFF_ARR arrBackupDPCDBuff;

    BOOLEAN bSinkPluggedState; // TRUE: SInk is Plugged    FALSE: Sink is not connected/unplugged

} DPAUX_INTERFACE, *PDPAUX_INTERFACE;

typedef struct _DEFAULT_DPCD_ERROR_MAP
{
    PAUX_ERROR_PARAMS pstAuxReadErrorParams;
    PAUX_ERROR_PARAMS pstAuxWriteErrorParams;
} DEFAULT_DPCD_ERROR_MAP, *PDEFAULT_DPCD_ERROR_MAP;

// Function Declarations: To be used by functions in other files

BOOLEAN AUXINTERFACE_Init(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucGlobalMMIORegFile, ULONG ulMMIOBaseOffset, PORT_TYPE ePortType, ULONG ulDataStartReg, ULONG ulDataEndReg,
                          ULONG ulControlReg);

DP_TOPOLOGY_TYPE AUXINTERFACE_GetTopologyType(PDPAUX_INTERFACE pstDPAuxInterface);

PVOID AUXINTERFACE_GetMSTTopologPtr(PDPAUX_INTERFACE pstDPAuxInterface);

PVOID AUXINTERFACE_GetSSTDisplayInfoPtr(PDPAUX_INTERFACE pstDPAuxInterface);

PUCHAR AUXINTERFACE_SetDwnStrmDPCDMap(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucDPCDBuff, ULONG ulDPCDSize);

PUCHAR AUXINTERFACE_GetDwnStrmDPCDMap(PDPAUX_INTERFACE pstDPAuxInterface);

BOOLEAN AUXINTERFACE_ReadDPCDAppWorld(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucReadBuff, ULONG ulDPCDAddress, ULONG ulLength);

BOOLEAN AUXINTERFACE_WriteDPCDAppWorld(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucWriteBuff, ULONG ulDPCDAddress, ULONG ulLength);

BOOLEAN AUXINTERFACE_ControlRegWriteHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulRegOffset, ULONG ulRegVal);

BOOLEAN AUXINTERFACE_ControlRegReadHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulRegOffset, PULONG pulRegVal);

BOOLEAN AUXINTERFACE_DataRegWriteHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulRegOffset, ULONG ulRegVal);

BOOLEAN AUXINTERFACE_DataRegReadHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulRegOffset, PULONG pulRegVal);

VOID AUXINTERFACE_DataRegProcessHandler(PDPAUX_INTERFACE pstDPAuxInterface);

BOOLEAN AUXINTERFACE_UpdateTopologyType(PDPAUX_INTERFACE pstDPAuxInterface, DP_TOPOLOGY_TYPE eTopologyType);

BOOLEAN AUXINTERFACE_InitialDPCDClientsRegister(PDPAUX_INTERFACE pstDPAuxInterface, DP_TOPOLOGY_TYPE eTopologyType);

BOOLEAN AUXINTERFACE_GfxS3S4UpdateTopology(PDPAUX_INTERFACE pstDPAuxInterface, DP_TOPOLOGY_TYPE eTopologyType, PDP12_TOPOLOGY pstDP12Topology, PUCHAR pucBranch0DPCDBuff,
                                           ULONG ulBranch0DPCDSize, PUCHAR pucSSTEDID, ULONG ulSSTEDIDSize, PUCHAR pucNewSSTDPCDBuff, ULONG ulNewSSTDPCDSize,
                                           PDPCD_CONFIG_DATA pstNewSSTDPCDConfigData);

BOOLEAN AUXINTERFACE_CleanUp(PDPAUX_INTERFACE pstDPAuxInterface);

#endif