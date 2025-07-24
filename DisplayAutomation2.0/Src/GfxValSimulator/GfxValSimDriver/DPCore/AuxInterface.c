
#include "AuxInterface.h"
#include "AuxDefs.h"
#include "DPCDs.h"
#include "AuxDPCDClient.h"
#include "..\CommonInclude\ETWLogging.h"

// This Map will finally be a part of each RX be it branch or sink
// This will initilaized to default or XML provided Values?
// Will need to dump this data from a real sink and branch to populate it with default values
// Then through XML a particular DPCD can be modified.
// UCHAR g_ucDPDCMap[MAX_DPCD_ADDRESS_RANGE] = { 0 };

DEFAULT_DPCD_ERROR_MAP g_stDPCDErrorMap[MAX_DPCD_ADDRESS_RANGE] = { 0 }; // To be removed

void AUXINTERFACE_NativeAuxHandler(PDPAUX_INTERFACE pstDPAuxInterface, UCHAR ucAuxCommand, ULONG ulDPCDAddress, UCHAR ucTransactionLen);

void AUXINTERFACE_I2COverAuxHandler(PDPAUX_INTERFACE pstDPAuxInterface, UCHAR ucAuxCommand, ULONG ulI2CTxnAddress, UCHAR ucI2CTxnLen);

REGISTRATION_RESULT AUXINTERFACE_RegisterDPCDClient(
PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulDPCDStartAddress, ULONG ulDPCDEndAddress,
PFN_DPCDCLIENT_PRIVATEDATA_INIT pfnClientInitFunction, // Client can send a pointer to this function that does some private init task for this client
PFN_DPCDCLIENT_CLEANUP_HANDLER pfnClientCleanupHandler, PFN_DPCDCLIENT pfnDPCDReadClient, PDP_THREAD_START_ROUTINE pfnDPCDThreadedReadClient, PAUX_ERROR_PARAMS pstReadErrorParams,
PFN_DPCDCLIENT pfnDPCDWriteClient, PDP_THREAD_START_ROUTINE pfnDPCDThreadedWriteClient, PAUX_ERROR_PARAMS pstWriteErrorParams, BOOLEAN bCreateThreadedClientResponseEvent,
PUCHAR pucClientDPCDMap,
PVOID  pvCallerPersistedContext, // Caller would persist this data as long as it uses this client
PVOID  pvCallerNonPersistedData, // Caller won't persist this data after this call returns so client needs to copy
ULONG  ulNonPersistedSize);

BOOLEAN AUXINTERFACE_RegisterCommmonDPCDClientsSSTMST(PDPAUX_INTERFACE pstDPAuxInterface);

BOOLEAN AUXINTERFACE_DeRegisterDPCDClient(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulDPCDStartAddress, ULONG ulDPCDEndAddress);

BOOLEAN AUXINTERFACE_DeRegisterAllDPCDClients(PDPAUX_INTERFACE pstDPAuxInterface);

// To register clients Common to Both MST and SST
BOOLEAN AUXINTERFACE_RegisterCommmonDPCDClientsSSTMST(PDPAUX_INTERFACE pstDPAuxInterface);

BOOLEAN AUXINTERFACE_RegisterDPCDClientsSST(PDPAUX_INTERFACE pstDPAuxInterface);

BOOLEAN AUXINTERFACE_DeRegisterDPCDClientsSST(PDPAUX_INTERFACE pstDPAuxInterface);

BOOLEAN AUXINTERFACE_RegisterDPCDClientsMST(PDPAUX_INTERFACE pstDPAuxInterface);

BOOLEAN AUXINTERFACE_DeRegisterDPCDClientsMST(PDPAUX_INTERFACE pstDPAuxInterface);

// DWORD  AUXINTERFACE_DataRegProcessorThread(LPVOID lpThreadParameter);

BOOLEAN AUXINTERFACE_DefaultDPCDReadHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulDPCDAddr, UCHAR ucReadLength);

BOOLEAN AUXINTERFACE_DefaultDPCDWriteHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulDPCDAddr, UCHAR ucWriteLength);

BOOLEAN AUXINTERFACE_CopyDataFromDataRegsAndAck(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucDPCDSWriteBuff, UCHAR ucDataLen, BOOLEAN bSendAck);

BOOLEAN AUXINTERFACE_CopyDataToDataRegsAndAck(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucDPCDReadBuff, UCHAR ucDataLen);

BOOLEAN AUXINTERFACE_GenericErrorHandler(PDPAUX_INTERFACE pstDPAuxInterface, PAUX_ERROR_PARAMS pstAuxErrorParams);

BOOLEAN AUXINTERFACE_SendAuxAckReply(PDPAUX_INTERFACE pstDPAuxInterface, UCHAR ucMessageSize, AUX_REPLY_COMMAND_TYPES eAuxReplyType);

BOOLEAN AUXINTERFACE_SendAuxTimeoutReply(PDPAUX_INTERFACE pstDPAuxInterface);

BOOLEAN AUXINTERFACE_SendAuxReceiveErrorReply(PDPAUX_INTERFACE pstDPAuxInterface);

BOOLEAN AUXINTERFACE_SendAuxNACKOrDeferReply(PDPAUX_INTERFACE pstDPAuxInterface, UCHAR ucPartialWriteSize, AUX_REPLY_COMMAND_TYPES eAuxReplyType);

void AUXINTERFACE_ClearControlRegSendBusyBit(PDPAUX_INTERFACE pstDPAuxInterface);

BOOLEAN AUXINTERFACE_HandleDPCDTransaction(PDPCD_CONFIG_DATA pstDPCDConfigData, PUCHAR pucDownStreamDPCDBuff);

BOOLEAN AUXINTERFACE_Init(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucGlobalMMIORegFile, ULONG ulMMIOBaseOffset, PORT_TYPE ePortType, ULONG ulDataStartReg, ULONG ulDataEndReg,
                          ULONG ulControlReg)
{
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    BOOLEAN bRet = FALSE;

    do
    {
        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        // If someone already allocated and Initlaized the interface object for this Port, lets break.
        if (pstDPAuxInterface->bInterfaceInitalized == TRUE)
        {
            break;
        }

        pstDPAuxInterface->ePortNum             = ePortType;
        pstDPAuxInterface->eTopologyType        = eInvalidTopology;
        pstDPAuxInterface->ulOffsetAuxCtl       = ulControlReg;
        pstDPAuxInterface->ulOffsetAuxDataStart = ulDataStartReg;
        pstDPAuxInterface->ulOffsetAuxDataEnd   = ulDataEndReg;

        pstDPAuxInterface->pstAuxDataRegs = (PAUX_DATAREG_STRUCT)(pucGlobalMMIORegFile + ulDataStartReg - ulMMIOBaseOffset);
        pstDPAuxInterface->pstAuxCtlReg   = (PAUX_CTRLREG_STRUCT)(pucGlobalMMIORegFile + ulControlReg - ulMMIOBaseOffset);

        if (!pstPortingObj->pfnInitializeDPEvent(&pstDPAuxInterface->stDataRegProcessorThreadEvent, FALSE, FALSE))
        {
            break;
        }

        if (!pstPortingObj->pfnInitializeDPEvent(&pstDPAuxInterface->stDataRegProcessorKillEvent, FALSE, FALSE))
        {
            break;
        }

        // Initialize Memory for DPCD buffer for Native Aux Access. This buffer will be directly a part of Aux object for ease of
        // Implementation rather than being a part of the Sink. When we get calls from the app world to set the DPCD for a sink.
        // We'd copy the DPCD data to this buffer instead
        // We are PRE-ALLOCATING THIS MEMORY Because this DPCD Buff has to be passed during client registeration
        pstDPAuxInterface->pucDownStreamDPCDBuff = pstPortingObj->pfnAllocateMem(MAX_CURRENT_DPCDS_SUPPORTED, TRUE);

        if (pstDPAuxInterface->pucDownStreamDPCDBuff == NULL)
        {
            break;
        }

        // Init SST Display Object
        pstDPAuxInterface->pstSSTDisplayInfo = SSTDISPLAY_SSTDisplayInit();

        // Init MST Topology Object
        pstDPAuxInterface->pstDP12Topology = DP12TOPOLOGY_TopologyObjectInit();

        if (pstDPAuxInterface->pstDP12Topology == NULL)
        {
            break;
        }

        pstDPAuxInterface->bInterfaceInitalized = TRUE;

        // If we are here means everything Init wanted to do was done successfully so return TRUE
        bRet = TRUE;

    } while (FALSE);

    if (bRet == FALSE && pstDPAuxInterface)
    {
        pstPortingObj->pfnFreeMem(pstDPAuxInterface);
        pstDPAuxInterface = NULL;
    }

    return bRet;
}

BOOLEAN AUXINTERFACE_UpdateTopologyType(PDPAUX_INTERFACE pstDPAuxInterface, DP_TOPOLOGY_TYPE eTopologyType)
{
    BOOLEAN bRet = TRUE;

    if (pstDPAuxInterface->eTopologyType != eTopologyType)
    {
        pstDPAuxInterface->eTopologyType = eTopologyType;
    }

    return bRet;
}

BOOLEAN AUXINTERFACE_InitialDPCDClientsRegister(PDPAUX_INTERFACE pstDPAuxInterface, DP_TOPOLOGY_TYPE eTopologyType)
{
    BOOLEAN bRet = TRUE;
    GFXVALSIM_FUNC_ENTRY();

    do
    {
        if (eTopologyType == eDPMST)
        {
            if (FALSE == AUXINTERFACE_DeRegisterDPCDClientsSST(pstDPAuxInterface))
            {
                bRet = FALSE;
                break;
            }

            // SST Display Cleanup is not called because it will Deregister the DDC I2C Slave handlers.
            // Current implementation is that DDC I2C slaves are registered only during AuxInterfaceInit (that calls SSTDISPLAY_SSTDisplayInit
            // where I2C slave handler registeration happens) and afterwards only the EDID the DDC Slave Handler caches is
            // changed (through IOCTL_SET_EDID_DATA IOCTL). SSTDISPLAY_Cleanup deregisters/Cleans up the registered DDC I2C slave handlers.
            // If we Call SSTDISPLAY_Cleanup here then there would be no DDC I2C slave handler to handle
            // I2C-over-Aux traffic for DDC.
            // SSTDISPLAY_Cleanup(pstDPAuxInterface->pstSSTDisplayInfo);

            if (FALSE == AUXINTERFACE_RegisterDPCDClientsMST(pstDPAuxInterface))
            {
                bRet = FALSE;
                break;
            }
        }
        else if (eTopologyType == eDPSST)
        {
            if (FALSE == AUXINTERFACE_DeRegisterDPCDClientsMST(pstDPAuxInterface))
            {
                bRet = FALSE;
                break;
            }

            DP12TOPOLOGY_Cleanup(pstDPAuxInterface->pstDP12Topology);

            if (FALSE == AUXINTERFACE_RegisterDPCDClientsSST(pstDPAuxInterface))
            {
                bRet = FALSE;
                break;
            }
        }
    } while (FALSE);

    GFXVALSIM_FUNC_EXIT((bRet == TRUE) ? 0 : 1);
    return bRet;
}

BOOLEAN AUXINTERFACE_GfxS3S4UpdateTopology(PDPAUX_INTERFACE pstDPAuxInterface, DP_TOPOLOGY_TYPE eTopologyType, PDP12_TOPOLOGY pstDP12Topology, PUCHAR pucBranch0DPCDBuff,
                                           ULONG ulBranch0DPCDSize, PUCHAR pucSSTEDID, ULONG ulSSTEDIDSize, PUCHAR pucNewSSTDPCDBuff, ULONG ulNewSSTDPCDSize,
                                           PDPCD_CONFIG_DATA pstNewSSTDPCDConfigData)
{
    BOOLEAN           bRet          = FALSE;
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    do
    {
        if (eTopologyType == eDPMST)
        {
            if (FALSE == AUXINTERFACE_DeRegisterAllDPCDClients(pstDPAuxInterface))
            {
                break;
            }

            if (pstDP12Topology)
            {
                if (pstDPAuxInterface->pstDP12Topology)
                {
                    DP12TOPOLOGY_Cleanup(pstDPAuxInterface->pstDP12Topology);
                    // Free the Topology object as we have already constructed a whole new topology object
                    // set up during preparing for Gfx S3/S4
                    pstPortingObj->pfnFreeMem(pstDPAuxInterface->pstDP12Topology);
                }

                pstDPAuxInterface->pstDP12Topology = pstDP12Topology;
                // stDPCDConfigData is within pstDP12Topology. So for MST case, setting pstDP12Topology is enough.

                if (FALSE == AUXINTERFACE_SetDwnStrmDPCDMap(pstDPAuxInterface, pucBranch0DPCDBuff, ulBranch0DPCDSize))
                {
                    break;
                }

                if (FALSE == AUXINTERFACE_RegisterDPCDClientsMST(pstDPAuxInterface))
                {
                    break;
                }
            }
        }
        else if (eTopologyType == eDPSST)
        {
            if (FALSE == AUXINTERFACE_DeRegisterAllDPCDClients(pstDPAuxInterface))
            {
                break;
            }

            DP12TOPOLOGY_Cleanup(pstDPAuxInterface->pstDP12Topology);

            SSTDISPLAY_SetEDIDData(pstDPAuxInterface->pstSSTDisplayInfo, ulSSTEDIDSize, pucSSTEDID);

            if (FALSE == AUXINTERFACE_SetDwnStrmDPCDMap(pstDPAuxInterface, pucNewSSTDPCDBuff, ulNewSSTDPCDSize))
            {
                break;
            }

            if (pstNewSSTDPCDConfigData)
            {
                memcpy_s(&(pstDPAuxInterface->pstSSTDisplayInfo->stDPCDConfigData), sizeof(DPCD_CONFIG_DATA), pstNewSSTDPCDConfigData, sizeof(DPCD_CONFIG_DATA));
            }

            if (FALSE == AUXINTERFACE_RegisterDPCDClientsSST(pstDPAuxInterface))
            {
                break;
            }
        }

        pstDPAuxInterface->eTopologyType = eTopologyType;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}
// Implementation Notes:
// IMPORTANT:
//!!!!!*****Since any DPCD address Accessed by Gfx is looked into the list of Registered DPCD Clients by iterating ove the client array****!!!
//!!!!!!!!!*** so register handlers/clients for most frequently accessed DPCD addresses first whenever possible******!!!!!!!!!!!!!!!!

// The register function, for every DPCD address client, takes a Pointer to DPCD buffer with AuxInterface object (used for Native auxes) so it modifies the
// DPCD buffer common across ALL DPCDs
REGISTRATION_RESULT AUXINTERFACE_RegisterDPCDClient(
PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulDPCDStartAddress, ULONG ulDPCDEndAddress,
PFN_DPCDCLIENT_PRIVATEDATA_INIT pfnClientInitFunction, // Client can send a pointer to this function that does some private init task for this client
PFN_DPCDCLIENT_CLEANUP_HANDLER pfnClientCleanupHandler, PFN_DPCDCLIENT pfnDPCDReadClient, PDP_THREAD_START_ROUTINE pfnDPCDThreadedReadClient, PAUX_ERROR_PARAMS pstReadErrorParams,
PFN_DPCDCLIENT pfnDPCDWriteClient, PDP_THREAD_START_ROUTINE pfnDPCDThreadedWriteClient, PAUX_ERROR_PARAMS pstWriteErrorParams, BOOLEAN bCreateThreadedClientResponseEvent,
PUCHAR pucClientDPCDMap,
PVOID  pvCallerPersistedContext, // Caller would persist this data as long as it uses this client
PVOID  pvCallerNonPersistedData, // Caller won't persist this data after this call returns so client needs to copy
ULONG  ulNonPersistedSize)
{
    PPORTINGLAYER_OBJ   pstPortingObj        = GetPortingObj();
    REGISTRATION_RESULT eRegisterationResult = eRegistrationFailed;
    BOOLEAN             bRet                 = TRUE;
    ULONG               ulCount              = 0;
    PDPCD_CLIENTINFO    pDPCDClientInfo      = NULL;

    do
    {

        // The below condition can be && instead || in which either read or write would be handled by default handler
        // Leave it to be || for now?

        if ((pfnDPCDReadClient == NULL) && (pfnDPCDWriteClient == NULL))
        {
            break;
        }

        if (pstDPAuxInterface->stClientInfoArray.ulNumRegisteredClients >= MAX_REGISTERED_DPCD_CLIENTS)
        {
            break;
        }

        for (ulCount = 0; ulCount < pstDPAuxInterface->stClientInfoArray.ulNumRegisteredClients; ulCount++)
        {
            if (ulDPCDStartAddress >= pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount].ulDPCDStartAddress &&
                ulDPCDEndAddress <= pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount].ulDPCDEndAddress)
            {
                eRegisterationResult = eAlreadyRegistered;
                break;
            }
        }

        if (eRegisterationResult == eAlreadyRegistered)
        {
            break; // break from for loop
        }

        pDPCDClientInfo = &pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[pstDPAuxInterface->stClientInfoArray.ulNumRegisteredClients];

        pDPCDClientInfo->pucClientDPCDMap   = pucClientDPCDMap;
        pDPCDClientInfo->ulDPCDStartAddress = ulDPCDStartAddress;
        pDPCDClientInfo->ulDPCDEndAddress   = ulDPCDEndAddress;

        pDPCDClientInfo->pstReadErrorParams  = pstReadErrorParams;
        pDPCDClientInfo->pstWriteErrorParams = pstWriteErrorParams;

        if (bCreateThreadedClientResponseEvent)
        {
            if (FALSE == pstPortingObj->pfnInitializeDPEvent(&pDPCDClientInfo->stThreadedClientResponseEvent, FALSE, FALSE))
            {
                break;
            }
        }

        if (pfnDPCDThreadedReadClient != NULL)
        {
            if (FALSE == pstPortingObj->pfnInitializeDPEvent(&pDPCDClientInfo->stReadHandlerThreadEvent, FALSE, FALSE))
            {
                break;
            }

            pDPCDClientInfo->hThreadHandleReadClient =
            pstPortingObj->pfnCreateThread(pDPCDClientInfo, pfnDPCDThreadedReadClient, &pDPCDClientInfo->ulThreadIDReadClient, SIMDRV_THREAD_PRIORITY, 0);

            if (pDPCDClientInfo->hThreadHandleReadClient == NULL)
            {
                break;
            }
        }
        else
        {
            pDPCDClientInfo->pfnDPCDReadClient = pfnDPCDReadClient;
        }

        if (pfnDPCDThreadedWriteClient != NULL)
        {
            if (pstPortingObj->pfnInitializeDPEvent(&pDPCDClientInfo->stWriteHandlerThreadEvent, FALSE, FALSE))
            {
                break;
            }

            pDPCDClientInfo->hThreadHandleWriteClient =
            pstPortingObj->pfnCreateThread(pDPCDClientInfo, pfnDPCDThreadedWriteClient, &pDPCDClientInfo->ulThreadIDWriteClient, SIMDRV_THREAD_PRIORITY, 0);

            if (pDPCDClientInfo->hThreadHandleWriteClient == NULL)
            {
                break;
            }
        }
        else
        {
            pDPCDClientInfo->pfnDPCDWriteClient = pfnDPCDWriteClient;
        }

        // Now call client Init function and let it do its own private initilization
        if (pvCallerPersistedContext)
        {
            pDPCDClientInfo->pvCallerPersistedContext = pvCallerPersistedContext;
        }

        if (pfnClientInitFunction)
        {
            if (bRet == pfnClientInitFunction(pDPCDClientInfo, pvCallerNonPersistedData, ulNonPersistedSize))
            {
                break;
            }
        }

        pDPCDClientInfo->pfnClientCleanupHandler = pfnClientCleanupHandler;

        pstDPAuxInterface->stClientInfoArray.ulNumRegisteredClients++;

        eRegisterationResult = eRegistrationSuccess;

    } while (FALSE);

    return eRegisterationResult;
}

// Implementation Notes:
// The register function, for every DPCD address client, takes a Pointer to DPCD buffer with AuxInterface object (used for Native auxes) so it modifies the
// DPCD buffer common across ALL DPCDs
BOOLEAN AUXINTERFACE_DeRegisterDPCDClient(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulDPCDStartAddress, ULONG ulDPCDEndAddress)
{
    BOOLEAN          bRet            = TRUE;
    ULONG            ulCount         = 0;
    BOOLEAN          bClientFound    = FALSE;
    PDPCD_CLIENTINFO pDPCDClientInfo = NULL;

    do
    {

        for (ulCount = 0; ulCount < pstDPAuxInterface->stClientInfoArray.ulNumRegisteredClients; ulCount++)
        {
            if (ulDPCDStartAddress >= pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount].ulDPCDStartAddress &&
                ulDPCDEndAddress <= pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount].ulDPCDEndAddress)
            {
                bClientFound = TRUE;
                break;
            }
        }

        if (bClientFound == FALSE)
        {
            // Trying to unregister something thats not registered
            break; // break from for loop
        }

        pDPCDClientInfo = &pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount];

        // Call Client cleanup function to do client specific cleanup
        if (pDPCDClientInfo->pfnClientCleanupHandler)
        {
            pDPCDClientInfo->pfnClientCleanupHandler(pDPCDClientInfo);
        }

        if (pDPCDClientInfo->hThreadHandleReadClient)
        {
            // Terminate thread
            // TBD
            pDPCDClientInfo->hThreadHandleReadClient = NULL;
        }

        if (pDPCDClientInfo->hThreadHandleWriteClient)
        {
            // Terminate thread
            // TBD
            pDPCDClientInfo->hThreadHandleWriteClient = NULL;
        }

        // Now move the left registered client left by one to fill the gap created by deregistering
        for (; ulCount < pstDPAuxInterface->stClientInfoArray.ulNumRegisteredClients - 1; ulCount++)
        {
            pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount] = pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount + 1];
        }

        pstDPAuxInterface->stClientInfoArray.ulNumRegisteredClients--;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

// Implementation Notes:
// The register function, for every DPCD address client, takes a Pointer to DPCD buffer with AuxInterface object (used for Native auxes) so it modifies the
// DPCD buffer common across ALL DPCDs
BOOLEAN AUXINTERFACE_DeRegisterAllDPCDClients(PDPAUX_INTERFACE pstDPAuxInterface)
{
    BOOLEAN          bRet            = TRUE;
    ULONG            ulCount         = 0;
    PDPCD_CLIENTINFO pDPCDClientInfo = NULL;

    do
    {
        // Now move the left registered client left by one to fill the gap created by deregistering
        for (ulCount = 0; ulCount < pstDPAuxInterface->stClientInfoArray.ulNumRegisteredClients; ulCount++)
        {
            pDPCDClientInfo = &pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount];

            // Call Client cleanup function to do client specific cleanup
            if (pDPCDClientInfo->pfnClientCleanupHandler)
            {
                pDPCDClientInfo->pfnClientCleanupHandler(pDPCDClientInfo);
            }

            if (pDPCDClientInfo->hThreadHandleReadClient)
            {
                // Terminate thread
                // TBD
                pDPCDClientInfo->hThreadHandleReadClient = NULL;
            }

            if (pDPCDClientInfo->hThreadHandleWriteClient)
            {
                // Terminate thread
                // TBD
                pDPCDClientInfo->hThreadHandleWriteClient = NULL;
            }

            memset(pDPCDClientInfo, 0, sizeof(DPCD_CLIENTINFO));
        }

        pstDPAuxInterface->stClientInfoArray.ulNumRegisteredClients = 0;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN AUXINTERFACE_RegisterCommmonDPCDClientsSSTMST(PDPAUX_INTERFACE pstDPAuxInterface)
{
    BOOLEAN bRet = TRUE;

    return bRet;
}

// Implementation Notes
// All the current and Future client registers for any DPCD go inside this function
// Handlers registered first would be executed first.  So Register All time critical handlers earlier than others
// So allow faster searching and execution
BOOLEAN AUXINTERFACE_RegisterDPCDClientsSST(PDPAUX_INTERFACE pstDPAuxInterface)
{
    BOOLEAN bRet = TRUE;

    // for SST, no DPCDs as of now to register separate handler

    return bRet;
}

BOOLEAN AUXINTERFACE_DeRegisterDPCDClientsSST(PDPAUX_INTERFACE pstDPAuxInterface)
{
    BOOLEAN bRet = TRUE;

    // for SST, no DPCDs as of now to deregister separate handler

    return bRet;
}

// Implementation Notes
// All the current and Future client registers for any DPCD go inside this functionW
BOOLEAN AUXINTERFACE_RegisterDPCDClientsMST(PDPAUX_INTERFACE pstDPAuxInterface)
{
    // Register IRQ Vector Client
    // Passing private data as pstDP12Topology as the client for this DPCD needs access to pstDP12Topology members for its functionality
    AUXINTERFACE_RegisterDPCDClient(pstDPAuxInterface, DPCD_SERVICE_IRQ_VECTOR, DPCD_SERVICE_IRQ_VECTOR, NULL, NULL, AUXCLIENT_ServiceIRQVectorRWHandler, NULL, NULL,
                                    AUXCLIENT_ServiceIRQVectorRWHandler, NULL, NULL, FALSE, pstDPAuxInterface->pucDownStreamDPCDBuff, pstDPAuxInterface->pstDP12Topology, NULL, 0);

    // Register Sideband Client
    // Passing private data as pstDP12Topology as the client for this DPCD needs access to pstDP12Topology members for its functionality
    AUXINTERFACE_RegisterDPCDClient(pstDPAuxInterface, MST_DPCD_DOWN_REQ_START, MST_DPCD_UP_REQ_END, NULL, NULL, AUXCLIENT_SideBandReadHandler, NULL, NULL,
                                    AUXCLIENT_SideBandWriteHandler, NULL, NULL, FALSE, pstDPAuxInterface->pucDownStreamDPCDBuff, pstDPAuxInterface->pstDP12Topology, NULL, 0);

    AUXINTERFACE_RegisterDPCDClient(pstDPAuxInterface, DPCD_VCPAYLOAD_ID, DPCD_VCPAYLOAD_NUM_SLOTS, NULL, NULL, AUXCLIENT_VCPayloadTableUpdateRWHandler, NULL, NULL,
                                    AUXCLIENT_VCPayloadTableUpdateRWHandler, NULL, NULL, FALSE, pstDPAuxInterface->pucDownStreamDPCDBuff, pstDPAuxInterface->pstDP12Topology, NULL,
                                    0);

    AUXINTERFACE_RegisterDPCDClient(pstDPAuxInterface, DPCD_VCPAYLOAD_UPDATE_STATUS, DPCD_VCPAYLOAD_UPDATE_STATUS, NULL, NULL, AUXCLIENT_VCPayloadTableStatusRWHandler, NULL, NULL,
                                    AUXCLIENT_VCPayloadTableStatusRWHandler, NULL, NULL, FALSE, pstDPAuxInterface->pucDownStreamDPCDBuff, pstDPAuxInterface->pstDP12Topology, NULL,
                                    0);

    return TRUE;
}

BOOLEAN AUXINTERFACE_DeRegisterDPCDClientsMST(PDPAUX_INTERFACE pstDPAuxInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (FALSE == AUXINTERFACE_DeRegisterDPCDClient(pstDPAuxInterface, DPCD_SERVICE_IRQ_VECTOR, DPCD_SERVICE_IRQ_VECTOR))
        {
            break;
        }

        if (FALSE == AUXINTERFACE_DeRegisterDPCDClient(pstDPAuxInterface, MST_DPCD_DOWN_REQ_START, MST_DPCD_UP_REQ_END))
        {
            break;
        }

        if (FALSE == AUXINTERFACE_DeRegisterDPCDClient(pstDPAuxInterface, DPCD_VCPAYLOAD_ID, DPCD_VCPAYLOAD_NUM_SLOTS))
        {
            break;
        }

        if (FALSE == AUXINTERFACE_DeRegisterDPCDClient(pstDPAuxInterface, DPCD_VCPAYLOAD_UPDATE_STATUS, DPCD_VCPAYLOAD_UPDATE_STATUS))
        {
            break;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN AUXINTERFACE_ControlRegWriteHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulRegOffset, ULONG ulRegVal)
{
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    BOOLEAN           bRet          = FALSE;
    // TBD: Control Reg Bit resetting by Source by writing 1 to different control Reg bits e.g. bDone bit has not been implemented yet
    do
    {
        pstDPAuxInterface->pstAuxCtlReg->ulValue = (pstDPAuxInterface->pstAuxCtlReg->ulValue ^ ulRegVal);
        if (0x80000 == (ulRegVal & 0x80000)) // WA for handling MTL AUX_IO PhyPowerRequest
        {
            pstDPAuxInterface->pstAuxCtlReg->ulValue = pstDPAuxInterface->pstAuxCtlReg->ulValue | 0x80000;
        }
        else
        {
            pstDPAuxInterface->pstAuxCtlReg->ulValue = pstDPAuxInterface->pstAuxCtlReg->ulValue & ~0x80000;
        }
        if (pstDPAuxInterface->pstAuxCtlReg->CtrlRegBits.bSendOrBusy)
        {
            GFXVALSIM_AUXCTRL_REG(pstDPAuxInterface->ePortNum, pstDPAuxInterface->pstAuxCtlReg->ulValue);
            // process respective Aux Handler
            AUXINTERFACE_DataRegProcessHandler(pstDPAuxInterface);
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN AUXINTERFACE_ControlRegReadHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulRegOffset, PULONG pulRegVal)
{

    *pulRegVal = pstDPAuxInterface->pstAuxCtlReg->ulValue;

    return TRUE;
}

// Note.ExtInterface Parallel Producer thread to queue MMIO accesses to be fed to clients

BOOLEAN AUXINTERFACE_DataRegWriteHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulRegOffset, ULONG ulRegVal)
{
    pstDPAuxInterface->pstAuxDataRegs[(ulRegOffset - pstDPAuxInterface->ulOffsetAuxDataStart) / 4].ulValue = ulRegVal;

    return TRUE;
}
// Finally returning data to the MMIO read
BOOLEAN AUXINTERFACE_DataRegReadHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulRegOffset, PULONG pulRegVal)
{

    *pulRegVal = pstDPAuxInterface->pstAuxDataRegs[(ulRegOffset - pstDPAuxInterface->ulOffsetAuxDataStart) / 4].ulValue;

    return TRUE;
}

VOID AUXINTERFACE_DataRegProcessHandler(PDPAUX_INTERFACE pstDPAuxInterface)
{
    GFXVALSIM_FUNC_ENTRY();

    AUX_COMMAND_SYNTAX_DIRECT_COPY stAuxRequest       = { 0 };
    ULONG                          ulDPCDOrI2CAddress = 0; // 20bits
    BOOLEAN                        bRet               = FALSE;

    // Fetch Command data from Data Reg 0 and rearrange because our Aux Data registers send MSB of the dword first
    // in a big endian way and hence are packed in the same way

    // Re-arranging Aux data reg 0 in the little endian format and reading it to the request register
    stAuxRequest.CommandDwordBits.ulHeader = (pstDPAuxInterface->pstAuxDataRegs[0].DataRegBytes.ucData1 << 24) | (pstDPAuxInterface->pstAuxDataRegs[0].DataRegBytes.ucData2 << 16) |
                                             (pstDPAuxInterface->pstAuxDataRegs[0].DataRegBytes.ucData3 << 8) | (pstDPAuxInterface->pstAuxDataRegs[0].DataRegBytes.ucData4);

    // Since source programs actual data length - 1 in the Aux command so increment it
    stAuxRequest.CommandDwordBits.Request.ucLength++;

    // decode DPCD address
    ulDPCDOrI2CAddress = (stAuxRequest.CommandDwordBits.Request.ulAddress19_16 << 16) | (stAuxRequest.CommandDwordBits.Request.ulAddress15_8 << 8) |
                         (stAuxRequest.CommandDwordBits.Request.ulAddress7_0);

    if (stAuxRequest.CommandDwordBits.Request.ucLength > AUX_MAX_TXN_LEN)
    {
        GFXVALSIM_DBG_MSG("ReqLength: %u > AUX_MAX_TXN_LEN!\r\n", stAuxRequest.CommandDwordBits.Request.ucLength);
        // ASSERT!
    }

    if (stAuxRequest.CommandDwordBits.Request.ucCommand >> 3)
    {
        AUXINTERFACE_NativeAuxHandler(pstDPAuxInterface, stAuxRequest.CommandDwordBits.Request.ucCommand, ulDPCDOrI2CAddress, stAuxRequest.CommandDwordBits.Request.ucLength);
    }
    else
    {

        AUXINTERFACE_I2COverAuxHandler(pstDPAuxInterface, stAuxRequest.CommandDwordBits.Request.ucCommand, ulDPCDOrI2CAddress, stAuxRequest.CommandDwordBits.Request.ucLength);
    }

    GFXVALSIM_FUNC_EXIT(0);
}

void AUXINTERFACE_NativeAuxHandler(PDPAUX_INTERFACE pstDPAuxInterface, UCHAR ucAuxCommand, ULONG ulDPCDAddress, UCHAR ucTransactionLen)
{
    PPORTINGLAYER_OBJ pstPortingObj   = GetPortingObj();
    BOOLEAN           bRet            = FALSE;
    ULONG             ulCount         = 0;
    PDPCD_CLIENTINFO  pDPCDClientInfo = NULL;
    // Validate ulDPCDAddress to be in range of the DPCD addresses defined by DP spec????

    GFXVALSIM_FUNC_ENTRY();

    // Iterate through the registered DPCD Handlers
    // Find out if this DPCD addr has any handlers registered
    for (ulCount = 0; ulCount < pstDPAuxInterface->stClientInfoArray.ulNumRegisteredClients; ulCount++)
    {
        if (ulDPCDAddress >= pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount].ulDPCDStartAddress &&
            ulDPCDAddress <= pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount].ulDPCDEndAddress)
        {
            bRet = TRUE;
            break;
        }
    }

    if (bRet)
    {
        // Fill Current transaction details for client to use
        // Fill pDPCDClientInfo with current transaction's address and length.
        // We can't pass these values as function paramaters because some clients may register their own processing thread
        // In that case we have to pass the values through the context data used during thread creation
        // That thread context data in this case is stDPAuxInterface

        pDPCDClientInfo                        = &pstDPAuxInterface->stClientInfoArray.ulDPCDClientList[ulCount];
        pDPCDClientInfo->ulCurrTransactionAddr = ulDPCDAddress;
        pDPCDClientInfo->ucCurrTransactionLen  = ucTransactionLen;
    }

    if (ucAuxCommand == eAUXRead)
    {
        // handler to generate read data with ACK/NACK
        // using pTempEntry check in if below instead of pDPCDClientInfo because of the nature of the while loop above
        if (bRet)
        {
            bRet                         = FALSE;
            pDPCDClientInfo->eAccessType = eRead;

            if (pDPCDClientInfo->pstReadErrorParams)
            {
                bRet = AUXINTERFACE_GenericErrorHandler(pstDPAuxInterface, pDPCDClientInfo->pstReadErrorParams);
            }
            // FALSE: Error Handler wants us to call the Actual Client Registered Handler.

            //*********************Note: Unsupported DPCDs Handling as per Spec********************************
            //
            // Write: Reply with NACK with partial number of written bytes as ZERO
            // Read: Reply with *ACK* instead of NACK and read data set to ZERO: This is a bit counter intuitive
            //
            //************************************************************************************************

            if (!bRet)
            {
                if (pDPCDClientInfo->stReadHandlerThreadEvent.bIsEventIntialized)
                {
                    // This means this DPCD client wanted a separate thread for parallel processing
                    // and should be waiting on this Synchronization event so lets set it

                    pstPortingObj->pfnSetDPEvent(&pDPCDClientInfo->stReadHandlerThreadEvent, PRIORITY_NO_INCREMENT);

                    // Wait for Client's ACK
                    pstPortingObj->pfnDPWaitForSingleEvent(&pDPCDClientInfo->stThreadedClientResponseEvent, NULL);
                    bRet = pDPCDClientInfo->bThreadClientResponse;
                    if (bRet)
                    {
                        AUXINTERFACE_CopyDataToDataRegsAndAck(pstDPAuxInterface, pDPCDClientInfo->ucPrimaryReadBuffer, pDPCDClientInfo->ucCurrTransactionLen);
                    }
                    else
                    {
                        AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_NACK);
                    }
                }
                else if (pDPCDClientInfo->pfnDPCDReadClient)
                {
                    // Call the client directly if present
                    bRet = pDPCDClientInfo->pfnDPCDReadClient(pDPCDClientInfo);

                    if (bRet)
                    {
                        bRet = AUXINTERFACE_CopyDataToDataRegsAndAck(pstDPAuxInterface, pDPCDClientInfo->ucPrimaryReadBuffer, pDPCDClientInfo->ucCurrTransactionLen);
                    }
                    else
                    {
                        AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_NACK);
                    }
                }
                else
                {
                    // No read client was register for this Only write client so call default handler directly
                    bRet = AUXINTERFACE_DefaultDPCDReadHandler(pstDPAuxInterface, ulDPCDAddress, ucTransactionLen);
                    // Check for return?
                }
            }
        }
        else
        {
            // No client was registered for this DPCD so call default handler directly
            bRet = AUXINTERFACE_DefaultDPCDReadHandler(pstDPAuxInterface, ulDPCDAddress, ucTransactionLen);
        }

        // If the Client was called and it didn't find the data to its liking, it would ask us to send a NACK by returning false
        if (!bRet)
        {
            GFXVALSIM_DBG_MSG("If the Client was called and it didn't find the data to its liking, it would ask us to send a NACK by returning false!\r\n");
            // Send Nack
        }
    }
    else if (ucAuxCommand == eAUXWrite)
    {
        if (bRet)
        {
            bRet                         = FALSE;
            pDPCDClientInfo->eAccessType = eWrite;

            if (pDPCDClientInfo->pstReadErrorParams)
            {
                bRet = AUXINTERFACE_GenericErrorHandler(pstDPAuxInterface, pDPCDClientInfo->pstReadErrorParams);
            }

            if (!bRet)
            {
                // First copy the data into Client's write buffer and then set the event
                AUXINTERFACE_CopyDataFromDataRegsAndAck(pstDPAuxInterface, pDPCDClientInfo->ucPrimaryWriteBuffer, pDPCDClientInfo->ucCurrTransactionLen, FALSE);

                if (pDPCDClientInfo->stWriteHandlerThreadEvent.bIsEventIntialized)
                {
                    // This means this DPCD client wanted a separate thread for parallel processing
                    // and should be waiting on this Synchronization event so lets set it

                    // Tell the threaded client that data has been copied to its buffer for consumption by setting its Write Event
                    pstPortingObj->pfnSetDPEvent(&pDPCDClientInfo->stWriteHandlerThreadEvent, PRIORITY_NO_INCREMENT);

                    // Wait for Client's ACK
                    pstPortingObj->pfnDPWaitForSingleEvent(&pDPCDClientInfo->stThreadedClientResponseEvent, NULL);

                    // Thread Client processed the request successfully
                    if (pDPCDClientInfo->bThreadClientResponse)
                    {
                        AUXINTERFACE_SendAuxAckReply(pstDPAuxInterface, 0, eAUX_ACK);
                    }
                    else
                    {
                        // Add support for Client Nacking with Partial Write dynamically
                        AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_NACK);
                    }
                }
                else if (pDPCDClientInfo->pfnDPCDWriteClient)
                {
                    // Call the client directly if present
                    bRet = pDPCDClientInfo->pfnDPCDWriteClient(pDPCDClientInfo);

                    // Client processed the request successfully
                    if (bRet)
                    {
                        AUXINTERFACE_SendAuxAckReply(pstDPAuxInterface, 0, eAUX_ACK);
                    }
                    else
                    {
                        // Add support for Client Nacking with Partial Writ dynamically
                        AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_NACK);
                    }
                }
                else
                {
                    // No read client was register for this Only write client so call default handler directly
                    AUXINTERFACE_DefaultDPCDWriteHandler(pstDPAuxInterface, ulDPCDAddress, ucTransactionLen);
                    // Check for return?
                }
            }
        }
        else
        {
            // No client was registered for this DPCD so call default handler directly
            AUXINTERFACE_DefaultDPCDWriteHandler(pstDPAuxInterface, ulDPCDAddress, ucTransactionLen);
        }
    }
    else
    {
        GFXVALSIM_DBG_MSG("Invalid command: %u!\r\n", ucAuxCommand);
    }

    GFXVALSIM_FUNC_EXIT(bRet == TRUE ? 0 : 1);

    return;
}

// I2C-Over-Aux Notes:
// MOT Bit usage:
// 1. START transaction - Address only, MOT Set = 1 ( This generates the corresponding I2C START condition => SDA low to high transition while SCL is high)
// 2. Stop transaction -  Address only, MOT Set = 0 ( This generates the corresponding I2C STOP condition. This can terminate any I2C transaction anytime
// 3. Stop transaction (2nd way) - If you set MOT = 0, and give a non zero transaction length N (i.e, the transaction is not address only) then the sink Rx would send an I2C stop
// condition after N bytes of transaction.
// 4. Repeat Start -      Address only, MOT set = 1. This is used to change the transaction direction from read to write and vice versa or to change the I2C slave address
//                       **Spec says you can change the I2C slave address using this Repeat start transaction (Page 197) but shouldn't the ongoing transaction properly
//                       terminated?**
// 5. Ongoing transaction - Lets say a I2C Master wants to transfer 10 bytes. If the corresponding I2C-over-Aux transaction decides to break it down to 1 byte
//                         per I2C-over-Aux trancation, it should set MOT bit to 1 for first 9 transaction and zero for the last i.e 10th transaction.
//                         If it sets MOT to Zero for any prior transaction (i.e, for transactions 1 to 9), then corresponding I2C transaction would immediately terminate
//
// Read page 197 of the DP1.2 spec (2.7.7.2.2) for some very useful details

void AUXINTERFACE_I2COverAuxHandler(PDPAUX_INTERFACE pstDPAuxInterface, UCHAR ucAuxCommand, ULONG ulI2CTxnAddress, UCHAR ucI2CTxnLen)
{
    BOOLEAN           bRet              = FALSE;
    BOOLEAN           bHandlerExists    = FALSE;
    PSST_DISPLAY_INFO pstSSTDisplayInfo = pstDPAuxInterface->pstSSTDisplayInfo;
    ACCESS_TYPE       eAccessType       = (ucAuxCommand & eI2CAUXRead) ? eRead : eWrite;
    BOOLEAN           bIsMOTSet         = (ucAuxCommand & 4) ? TRUE : FALSE;
    PPORTINGLAYER_OBJ pstPortingObj     = GetPortingObj();
    PI2C_SLAVE_INFO   pstI2CSlaveInfo   = NULL;
    PDP_LIST_ENTRY    pDPTempEntry      = NULL;

    GFXVALSIM_FUNC_ENTRY();

    do
    {
        // Iterate through the registered I2C Slave Handlers to see if there is a handler registered for this I2C Slave Address
        pDPTempEntry = pstPortingObj->pfnInterLockedTraverseList(&pstSSTDisplayInfo->I2CSlaveInfoListHead, pDPTempEntry);

        while (pDPTempEntry)
        {
            ULONG ulCount   = 0;
            pstI2CSlaveInfo = (PI2C_SLAVE_INFO)pDPTempEntry;

            for (ulCount = 0; ulCount < pstI2CSlaveInfo->stSlaveOffsetsArray.ulNumOffsetRanges; ulCount++)
            {
                if (ulI2CTxnAddress >= pstI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[ulCount].ulSlaveStartAddress &&
                    ulI2CTxnAddress <= pstI2CSlaveInfo->stSlaveOffsetsArray.stI2CSlaveOffsets[ulCount].ulSlaveStartAddress)
                {
                    bHandlerExists = TRUE;
                    break; // break from For loop
                }
            }
            if (bHandlerExists)
            {
                break;
            }

            pDPTempEntry = pstPortingObj->pfnInterLockedTraverseList(&pstSSTDisplayInfo->I2CSlaveInfoListHead, pDPTempEntry);
        }

        if (pDPTempEntry == NULL)
        {
            GFXVALSIM_DBG_MSG("NO I2CSlave Handler registered for I2C Address: %lu\r\n", ulI2CTxnAddress);
            // NO I2CSlave Handler registered for the I2C Addressed being accessed by the Source
            // Return I2C NACK
            AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eI2CAUX_NACK);
            break;
        }

        pstI2CSlaveInfo->ulCurrTransAddr = ulI2CTxnAddress;
        pstI2CSlaveInfo->ulCurrTransLen  = ucI2CTxnLen;
        pstI2CSlaveInfo->eCurrAccessType = eAccessType;
        pstI2CSlaveInfo->bIsIndexWrite   = FALSE;

        // SoftBios I2C handler code has some issues, it programs 0xff in the length byte
        // but that gets masked because of the size field in the Control reg
        // resulting in Aux hardware sending only 3 bytes and leaving out the length byte
        // We need to handle that here and modify the length
        // For Address only transaction : pstDPAuxInterface->stAuxCtlReg.CtrlRegBits.ulMessageSize == I2CAUX_START_TXN_SIZE
        if (pstDPAuxInterface->pstAuxCtlReg->CtrlRegBits.ulMessageSize == I2CAUX_START_TXN_SIZE)
        {
            // So this is an address only transaction
            // @todo: need to handle this check later
            if (eAccessType == eWriteStatusUpdate)
            {
                GFXVALSIM_DBG_MSG("Address only can't have access type as Write Status Update!\r\n");
                // Address only can't have access type as Write Status Update
                break;
            }

            pstSSTDisplayInfo->bTransStarted = bIsMOTSet;
            if (pstSSTDisplayInfo->bTransStarted)
            {
                // Transaction started
                pstSSTDisplayInfo->ulCurrTransactionAddr = ulI2CTxnAddress;
                pstI2CSlaveInfo->ulCurrentSlaveOffset    = 0;
                pstSSTDisplayInfo->eOngoingAccessType    = eAccessType;
            }
            else
            {
                // Transaction terminated
                pstI2CSlaveInfo->ulCurrentSlaveOffset    = 0;
                pstSSTDisplayInfo->ulCurrTransactionAddr = 0xFFFFFFFF;
            }

            // Since this is an address only transaction with no data to process, so just send an I2C over Aux ACK eAUX_ACK = eI2CAUX_ACK
            bRet = AUXINTERFACE_SendAuxAckReply(pstDPAuxInterface, 0, eAUX_ACK);
            break;
        }

        if (bIsMOTSet == FALSE)
        {
            pstSSTDisplayInfo->bTransStarted = FALSE;
            bRet                             = TRUE;
        }
        else
        {
            if (pstSSTDisplayInfo->ulCurrTransactionAddr != ulI2CTxnAddress)
            {
                GFXVALSIM_DBG_MSG("Someone trying to I2C access a different slave address without ending previous & sending new address Tx for this address\r\n");
                // Someone trying to another I2C access to a different slave addresss without ending the previous
                // and sending a new address only transaction for this address
                break;
            }

            if ((pstSSTDisplayInfo->bTransStarted == FALSE) || (pstSSTDisplayInfo->bTransStarted == TRUE && pstSSTDisplayInfo->eOngoingAccessType != eAccessType))
            {
                GFXVALSIM_DBG_MSG("Updating I2C ongoing access type to %d\r\n", eAccessType);
                // Source can't change the I2C transaction Access direction without doing an address only start first to change the access direction
                // We are here that means source changed the access direction without doing the above said address only transaction
                pstSSTDisplayInfo->eOngoingAccessType = eAccessType;
            }

            if (eAccessType == eWriteStatusUpdate && pstSSTDisplayInfo->eOngoingAccessType == eRead)
            {
                GFXVALSIM_DBG_MSG("Source is asking for Write Status Update after an I2C over AUX Read. This is wrong so we Break with False and return NACK\r\n");
                // Source is asking for Write Status Update after an I2C over AUX Read. This is wrong so we Break with False and return NACK

                // for Writes:
                // Since we are software and we are always expected to complete the last write so we'd return ACK always
                // for status write update
                // So just check for the error case Read
                break;
            }

            bRet = TRUE;
        }

        if (bRet)
        {
            if (eAccessType == eRead)
            {
                if (pstI2CSlaveInfo->pfnI2CSlaveReadHandler == NULL)
                {
                    GFXVALSIM_DBG_MSG("No I2C slave Read registered\r\n");
                    // No I2C slave read handler registered. Return I2C Nack
                    break;
                }

                bRet = pstI2CSlaveInfo->pfnI2CSlaveReadHandler(pstI2CSlaveInfo);

                if (bRet)
                {
                    // Copy data to SlaveInfo's buffer
                    AUXINTERFACE_CopyDataToDataRegsAndAck(pstDPAuxInterface, pstI2CSlaveInfo->pucSlaveIntermediateDataBuff, ucI2CTxnLen);
                }
                else
                {
                    AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eI2CAUX_NACK);
                }
            }
            else
            {
                if (pstI2CSlaveInfo->pfnI2CSlaveWriteHandler == NULL)
                {
                    // No I2C slave read handler registered. Return I2C Nack
                    break;
                }

                // Copy Data from Slave Info but don't send ACK as yet, hence the FALSE. Wait for client to process it
                AUXINTERFACE_CopyDataFromDataRegsAndAck(pstDPAuxInterface, pstI2CSlaveInfo->pucSlaveIntermediateDataBuff, ucI2CTxnLen, FALSE);

                bRet = pstI2CSlaveInfo->pfnI2CSlaveWriteHandler(pstI2CSlaveInfo);

                if (bRet)
                {
                    AUXINTERFACE_SendAuxAckReply(pstDPAuxInterface, 0, eAUX_ACK); // eAUX_ACK = eI2CAUX_ACK
                }
                else
                {
                    AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eI2CAUX_NACK);
                }
            }
        }
        else
        {
            AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eI2CAUX_NACK);
        }

        // If MOT bit is set and current transaction is processed successfully
        if (bIsMOTSet && bRet)
        {
            if (pstI2CSlaveInfo->bIsIndexWrite == TRUE)
            {
                // So this is an address only transaction
                pstI2CSlaveInfo->bIsIndexWrite = FALSE;
            }
            else
            {
                // Change offset if its non-index write operation
                pstI2CSlaveInfo->ulCurrentSlaveOffset += ucI2CTxnLen;
            }
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(bRet == TRUE ? 0 : 1);

    return;
}

// Default DPCD Read Handler Gets called for any DPCD for which there's no explicit handler been registered
BOOLEAN AUXINTERFACE_DefaultDPCDReadHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulDPCDAddr, UCHAR ucReadLength)
{
    BOOLEAN                bRet            = FALSE;
    PUCHAR                 pucDPCDReadBuff = NULL;
    DEFAULT_DPCD_ERROR_MAP stDPCDErrorMap  = {
        0,
    };
    UCHAR             ucRandomDPCDValue = 0;
    PPORTINGLAYER_OBJ pstPortingObj     = GetPortingObj();

    // Boundary check for the continuous DPCD binary data provided by the app
    GFXVALSIM_FUNC_ENTRY();

    do
    {
        if (ulDPCDAddr + ucReadLength <= pstDPAuxInterface->ulDPCDBuffSize)
        {
            pucDPCDReadBuff = &pstDPAuxInterface->pucDownStreamDPCDBuff[ulDPCDAddr];
            // pstDPCDErrorMap = &g_stDPCDErrorMap[ulDPCDAddr]; //Can be used in future to pass error parameters, UNBLOCK if needed
            GFXVALSIM_AUX_READ(ulDPCDAddr, ucReadLength, pucDPCDReadBuff);
        }
        else
        {

            ULONG   ulCount = 0;
            BOOLEAN bFound  = FALSE;

            if (ucReadLength > 10)
            {
                // Can't support this in current implementation, NACK it
                AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_NACK);
                break;
            }

            for (; ulCount < pstDPAuxInterface->arrBackupDPCDBuff.ulCurrentFilledSize; ulCount++)
            {
                if (ulDPCDAddr == pstDPAuxInterface->arrBackupDPCDBuff.BackupDPCDBuff[ulCount].ulStartOffset)
                {
                    bFound = TRUE;
                    break;
                }
            }

            if (bFound)
            {
                pucDPCDReadBuff = &pstDPAuxInterface->arrBackupDPCDBuff.BackupDPCDBuff[ulCount].ucValue;
            }
            else
            {

                // Reading a DPCD beyond the contiguous range of DPCDs provided by parsing the topology XML
                // So we have no idea what the default value should be so just return zero
                pucDPCDReadBuff = &ucRandomDPCDValue;
            }
        }

        // Incase of Sink is not connected/unplugged,
        // AUX Read needs to replied with TImeOut error
        if (pstDPAuxInterface->bSinkPluggedState == FALSE)
        {
            stDPCDErrorMap.pstAuxReadErrorParams = pstPortingObj->pfnAllocateMem(sizeof(AUX_ERROR_PARAMS), TRUE);
            if (stDPCDErrorMap.pstAuxReadErrorParams != NULL)
            {
                stDPCDErrorMap.pstAuxReadErrorParams->stTimeoutData.bTimeout       = 1;
                stDPCDErrorMap.pstAuxReadErrorParams->stTimeoutData.bTimeoutAlways = 1;
            }
        }
        if (stDPCDErrorMap.pstAuxReadErrorParams)
        {
            bRet = AUXINTERFACE_GenericErrorHandler(pstDPAuxInterface, stDPCDErrorMap.pstAuxReadErrorParams);
        }

        // Error Handler returned false: Meaning it didn't anything and wants us to copy the data and send an ACK
        if (!bRet)
        {
            bRet = AUXINTERFACE_CopyDataToDataRegsAndAck(pstDPAuxInterface, pucDPCDReadBuff, ucReadLength);
        }

        if (stDPCDErrorMap.pstAuxReadErrorParams != NULL)
        {
            pstPortingObj->pfnFreeMem(stDPCDErrorMap.pstAuxReadErrorParams);
            stDPCDErrorMap.pstAuxReadErrorParams = NULL;
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(bRet != TRUE ? 0 : 1);

    return bRet;
}

// Default DPCD Write Handler Gets called for any DPCD for which there's no explicit handler been registered
BOOLEAN AUXINTERFACE_DefaultDPCDWriteHandler(PDPAUX_INTERFACE pstDPAuxInterface, ULONG ulDPCDAddr, UCHAR ucWriteLength)
{
    BOOLEAN                 bRet              = FALSE;
    PUCHAR                  pucDPCDWriteBuff  = NULL;
    PDEFAULT_DPCD_ERROR_MAP pstDPCDErrorMap   = NULL;
    DP_TOPOLOGY_TYPE        eTopologyType     = 0;
    PDPCD_CONFIG_DATA       pstDPCDConfigData = NULL;

    GFXVALSIM_FUNC_ENTRY();

    do
    {
        if (ulDPCDAddr + ucWriteLength <= pstDPAuxInterface->ulDPCDBuffSize)
        {
            pucDPCDWriteBuff = &pstDPAuxInterface->pucDownStreamDPCDBuff[ulDPCDAddr];
            // pstDPCDErrorMap = &g_stDPCDErrorMap[ulDPCDAddr]; //Can be used in future to pass error parameters, UNBLOCK if needed
            GFXVALSIM_AUX_WRITE(ulDPCDAddr, ucWriteLength, pucDPCDWriteBuff);
        }
        else
        {

            ULONG   ulCount = 0;
            BOOLEAN bFound  = FALSE;

            if (ucWriteLength > 1)
            {
                // Can't support this in current implementation, NACK it
                AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_NACK);
                break;
            }

            for (; ulCount < pstDPAuxInterface->arrBackupDPCDBuff.ulCurrentFilledSize; ulCount++)
            {
                if (ulDPCDAddr == pstDPAuxInterface->arrBackupDPCDBuff.BackupDPCDBuff[ulCount].ulStartOffset)
                {
                    bFound = TRUE;
                    break;
                }
            }

            if (bFound)
            {
                pucDPCDWriteBuff = &pstDPAuxInterface->arrBackupDPCDBuff.BackupDPCDBuff[ulCount].ucValue;
            }
            else
            {
                if (pstDPAuxInterface->arrBackupDPCDBuff.ulCurrentFilledSize >= NUM_BACKUP_DPCD_BUFF_SIZE)
                {
                    // Can't support this in current implementation, NACK it
                    AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_NACK);
                    break;
                }

                pstDPAuxInterface->arrBackupDPCDBuff.BackupDPCDBuff[pstDPAuxInterface->arrBackupDPCDBuff.ulCurrentFilledSize].ulStartOffset = ulDPCDAddr;
                pucDPCDWriteBuff = &pstDPAuxInterface->arrBackupDPCDBuff.BackupDPCDBuff[pstDPAuxInterface->arrBackupDPCDBuff.ulCurrentFilledSize].ucValue;
                pstDPAuxInterface->arrBackupDPCDBuff.ulCurrentFilledSize++;
            }
        }

        if (pstDPCDErrorMap && pstDPCDErrorMap->pstAuxWriteErrorParams)
        {
            bRet = AUXINTERFACE_GenericErrorHandler(pstDPAuxInterface, pstDPCDErrorMap->pstAuxWriteErrorParams);
        }

        // Error Handler returned false: Meaning it didn't anything and wants us to copy the data and send an ACK
        if (!bRet)
        {
            bRet = AUXINTERFACE_CopyDataFromDataRegsAndAck(pstDPAuxInterface, pucDPCDWriteBuff, ucWriteLength, TRUE);

            // handle DPCD transaction if ulDPCDAddr matches Trigger offset
            eTopologyType = AUXINTERFACE_GetTopologyType(pstDPAuxInterface);
            if (eTopologyType == eDPSST)
                pstDPCDConfigData = &(pstDPAuxInterface->pstSSTDisplayInfo->stDPCDConfigData);
            else if (eTopologyType == eDPMST)
                pstDPCDConfigData = &(pstDPAuxInterface->pstDP12Topology->stDPCDConfigData);
            if (pstDPCDConfigData != NULL)
            {
                ULONG ulTriggerOffset = pstDPCDConfigData->stDPCDModelData.ulTriggerOffset;
                if (ulDPCDAddr <= ulTriggerOffset && (ulDPCDAddr + ucWriteLength - 1) >= ulTriggerOffset)
                {
                    GFXVALSIM_DBG_MSG("Received DPCD write matching trigger offset for DPCD transaction. Trans start addr= 0x%X, length= %u\n", ulDPCDAddr, ucWriteLength);
                    bRet = AUXINTERFACE_HandleDPCDTransaction(pstDPCDConfigData, pstDPAuxInterface->pucDownStreamDPCDBuff);
                }
            }
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

// This function gets called from AUXINTERFACE_DefaultDPCDWriteHandler, when the DPCD write offset matches with user set DPCD transaction trigger offset.
// It will do the DPCD transaction exchange with Gfx driver by writing into DPCD as per user set DPCD model data.
BOOLEAN AUXINTERFACE_HandleDPCDTransaction(PDPCD_CONFIG_DATA pstDPCDConfigData, PUCHAR pucDownStreamDPCDBuff)
{
    GFXVALSIM_FUNC_ENTRY();

    BOOLEAN           bRet = FALSE;
    PDPCD_MODEL_DATA  pstDPCDModelData;
    PDPCD_TRANSACTION pstCurDPCDTransaction = NULL;
    BOOLEAN           bIsExpectedTrans      = TRUE;
    BOOLEAN           bIsFLTCase            = FALSE;

    do
    {
        if (pstDPCDConfigData == NULL || pstDPCDConfigData->stDPCDModelData.ucTransactionCount == 0)
        {
            GFXVALSIM_DBG_MSG("ERROR: No DPCD Model data passed with plug call.\n");
            break;
        }

        pstDPCDModelData = &(pstDPCDConfigData->stDPCDModelData);
        if (pstDPCDConfigData->ucDPCDTransactionIndex >= pstDPCDModelData->ucTransactionCount)
        {
            // Driver may do  these transactions again (e.g: Link training again after modeset on the already plugged display). So reset this index to 0.
            GFXVALSIM_DBG_MSG("Transactions in model data have exhausted. Resetting Transaction index to 0.\n");
            pstDPCDConfigData->ucDPCDTransactionIndex = 0;
        }

        if (pucDownStreamDPCDBuff[DPCD_SET_TRAINING_PATTERN] == 0x0)
        {
            // This is to handle Fast link training case. Here driver will set 0x0 to DPCD_SET_TRAINING_PATTERN (0x102) and then write last known values to lane registers 0x103 to
            // 0x106. So set index to last transaction of our model data. If current transaction input matches with this, response will be written and hence link training is
            // completed.
            bIsFLTCase = TRUE;
            GFXVALSIM_DBG_MSG("Training pattern is 0x0 (FLT case). Setting Transaction index to last one.\n");
            pstDPCDConfigData->ucDPCDTransactionIndex = pstDPCDModelData->ucTransactionCount - 1;
        }

        // read input DPCDs, check if their values are as per current expected DPCD transaction.
        GFXVALSIM_DBG_MSG("Current DPCD TransactionIndex= %u\n", pstDPCDConfigData->ucDPCDTransactionIndex);
        pstCurDPCDTransaction = &(pstDPCDModelData->stDPCDTransactions[pstDPCDConfigData->ucDPCDTransactionIndex]);
        for (UCHAR node_index = 0; node_index < pstCurDPCDTransaction->ucNumInputDpcdSets; node_index++)
        {
            PDPCD_VALUE_LIST pstInputDpcds = &(pstCurDPCDTransaction->stInputDpcdSets[node_index]);

            for (UCHAR item_index = 0; item_index < pstInputDpcds->ucLength; item_index++)
            {
                ULONG ulOffset = pstInputDpcds->ulStartingOffset + item_index;
                UCHAR ucValue  = pstInputDpcds->ucValues[item_index];
                UCHAR dpcdVal  = pucDownStreamDPCDBuff[ulOffset];

                if (pucDownStreamDPCDBuff[ulOffset] != ucValue)
                    bIsExpectedTrans = FALSE;
            }
        }

        if (bIsExpectedTrans == FALSE)
        {
            GFXVALSIM_DBG_MSG("ERROR: Input DPCDs are not as per current expected DPCD transaction\n");
            // In FLT case, if Input DPCDs doesn't match, that means FLT failed and it falls back to full Link training. So reset Transaction index to 0.
            if (bIsFLTCase == TRUE)
                pstDPCDConfigData->ucDPCDTransactionIndex = 0;
            break;

            // TODO: default response DPCD data sent by user can be used in failure case. If fail, write values as per stDefaultResponseDpcdSet
        }

        // write to Response DPCDs
        pstCurDPCDTransaction = &(pstDPCDModelData->stDPCDTransactions[pstDPCDConfigData->ucDPCDTransactionIndex]);
        for (UCHAR node_index = 0; node_index < pstCurDPCDTransaction->ucNumResponseDpcdSets; node_index++)
        {
            PDPCD_VALUE_LIST pstResponseDpcds = &(pstCurDPCDTransaction->stResponseDpcdSets[node_index]);

            for (UCHAR item_index = 0; item_index < pstResponseDpcds->ucLength; item_index++)
            {
                ULONG ulOffset = pstResponseDpcds->ulStartingOffset + item_index;
                UCHAR ucValue  = pstResponseDpcds->ucValues[item_index];

                pucDownStreamDPCDBuff[ulOffset] = ucValue;
                UCHAR dpcdVal                   = pucDownStreamDPCDBuff[ulOffset];
            }
        }

        // increment DPCD Transaction Index after successful transaction
        pstDPCDConfigData->ucDPCDTransactionIndex += 1;
        bRet = TRUE;
    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

// This function is getting called from Native Aux as well I2C-over-Aux handler functions currently but uses eAUX_ACK enum while sending ACK for both
// Since this function sends only ACK, it would work for both Native AUX ACK and I2C-over-ACK because for both the command nibble is 0000b i.e eAUX_ACK == eI2CAUX_ACK
BOOLEAN AUXINTERFACE_CopyDataFromDataRegsAndAck(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucDPCDWriteBuff, UCHAR ucDataLen, BOOLEAN bSendAck)
{
    BOOLEAN             bRet          = TRUE;
    UCHAR               ucOffset      = 0;
    ULONG               ulRegNum      = 0;
    PAUX_DATAREG_STRUCT pstAuxDataReg = &pstDPAuxInterface->pstAuxDataRegs[0];

    ucDataLen = min(16, ucDataLen);

    while (ucOffset < ucDataLen)
    {
        ulRegNum = 1 + ucOffset / 4;

        if (ucOffset < ucDataLen)
            pucDPCDWriteBuff[ucOffset++] = (UCHAR)pstAuxDataReg[ulRegNum].DataRegBytes.ucData1;

        if (ucOffset < ucDataLen)
            pucDPCDWriteBuff[ucOffset++] = (UCHAR)pstAuxDataReg[ulRegNum].DataRegBytes.ucData2;

        if (ucOffset < ucDataLen)
            pucDPCDWriteBuff[ucOffset++] = (UCHAR)pstAuxDataReg[ulRegNum].DataRegBytes.ucData3;

        if (ucOffset < ucDataLen)
            pucDPCDWriteBuff[ucOffset++] = (UCHAR)pstAuxDataReg[ulRegNum].DataRegBytes.ucData4;
    }

    if (bSendAck)
    {
        // Write ACK is just one byte with Command with no data to follow hence message length is Zero
        // This will work for both Native Aux and I2C over Aux since eAUX_ACK == eI2CAUX_ACK == 0000b
        bRet = AUXINTERFACE_SendAuxAckReply(pstDPAuxInterface, 0, eAUX_ACK);
    }

    return bRet;
}

// This function is getting called from Native Aux as well I2C-over-Aux handler functions currently but uses eAUX_ACK enum while sending ACK for both
// Since this function sends only ACK, it would work for both Native AUX ACK and I2C-over-ACK because for both the command nibble is 0000b i.e eAUX_ACK == eI2CAUX_ACK
BOOLEAN AUXINTERFACE_CopyDataToDataRegsAndAck(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucDPCDReadBuff, UCHAR ucDataLen)
{
    BOOLEAN             bRet          = FALSE;
    UCHAR               ucOffset      = 0;
    ULONG               ulRegNum      = 0;
    PAUX_DATAREG_STRUCT pstAuxDataReg = &pstDPAuxInterface->pstAuxDataRegs[0];

    // sanity check
    // DPCD Client should take care of sending Data less than or equal to Aux burst rate.
    // Or else we gonna send the data equal to burst rate and CLient can go to hell

    ucDataLen = min(16, ucDataLen);

    if (ucOffset < ucDataLen)
        pstAuxDataReg[0].DataRegBytes.ucData2 = pucDPCDReadBuff[ucOffset++];

    if (ucOffset < ucDataLen)
        pstAuxDataReg[0].DataRegBytes.ucData3 = pucDPCDReadBuff[ucOffset++];

    if (ucOffset < ucDataLen)
        pstAuxDataReg[0].DataRegBytes.ucData4 = pucDPCDReadBuff[ucOffset++];

    while (ucOffset < ucDataLen)
    {
        ulRegNum = (ucOffset + 1) / 4;

        if (ucOffset < ucDataLen)
            pstAuxDataReg[ulRegNum].DataRegBytes.ucData1 = pucDPCDReadBuff[ucOffset++];

        if (ucOffset < ucDataLen)
            pstAuxDataReg[ulRegNum].DataRegBytes.ucData2 = pucDPCDReadBuff[ucOffset++];

        if (ucOffset < ucDataLen)
            pstAuxDataReg[ulRegNum].DataRegBytes.ucData3 = pucDPCDReadBuff[ucOffset++];

        if (ucOffset < ucDataLen)
            pstAuxDataReg[ulRegNum].DataRegBytes.ucData4 = pucDPCDReadBuff[ucOffset++];
    }

    // Now send the data
    // This will work for both Native Aux and I2C over Aux since eAUX_ACK == eI2CAUX_ACK == 0000b
    bRet = AUXINTERFACE_SendAuxAckReply(pstDPAuxInterface, ucDataLen, eAUX_ACK);

    return bRet;
}

BOOLEAN AUXINTERFACE_GenericErrorHandler(PDPAUX_INTERFACE pstDPAuxInterface, PAUX_ERROR_PARAMS pstAuxErrorParams)
{
    ULONG   ulCount = 0;
    BOOLEAN bRet    = FALSE;

    // A DPCD Address client can send only one of the error messages in the current implementation
    // To send any other message would need Re-initialization of the whole module, getting the new values from the XML maybe?

    // Timeout Always : Always timeout
    // Timeout OnlyFirstTime : Timeout ulMaxTimeoutCount number of times for this DPCD and then start Acking
    // Timeout !OnlyFirstTime : Send and ACK after ulMaxTimeoutCount and reset ulCurrTimeoutCount to 0 to start sending ulMaxTimeoutCount
    //                         Numer of Timeouts after this ACK

    // Same logic goes for other types of Aux Errors
    do
    {
        if (pstAuxErrorParams == NULL)
        {
            break;
        }

        if (pstAuxErrorParams->stTimeoutData.bTimeout)
        {
            // Empty loop to simulate Aux timeout
            for (ulCount = 0; ulCount < 10000; ulCount++)
            {
                ;
            }

            if (pstAuxErrorParams->stTimeoutData.bTimeoutAlways)
            {
                bRet = AUXINTERFACE_SendAuxTimeoutReply(pstDPAuxInterface);
            }
            else
            {
                if (pstAuxErrorParams->stTimeoutData.ulCurrTimeoutCount < pstAuxErrorParams->stTimeoutData.ulMaxTimeoutCount)
                {
                    bRet = AUXINTERFACE_SendAuxTimeoutReply(pstDPAuxInterface);
                }
                else
                {
                    if (!pstAuxErrorParams->stTimeoutData.bTimeOutOnlyFirstTime)
                    {
                        pstAuxErrorParams->stTimeoutData.ulCurrTimeoutCount = 0;
                    }

                    // Else bRet = FALSE. False means asking the Caller to Send an ACK
                }
            }

            break;
        }

        if (pstAuxErrorParams->stDeferData.bDefer)
        {

            if (pstAuxErrorParams->stDeferData.bDeferAlways)
            {
                bRet = AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_DEFER);
            }
            else
            {
                if (pstAuxErrorParams->stDeferData.ulCurrDeferCount < pstAuxErrorParams->stDeferData.ulMaxDeferCount)
                {
                    bRet = AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_DEFER);
                }
                else
                {
                    if (!pstAuxErrorParams->stDeferData.bDeferOnlyFirstTime)
                    {
                        pstAuxErrorParams->stDeferData.ulCurrDeferCount = 0;
                    }

                    // else: bRet = FALSE: means asking the Caller to Send an ACK
                }
            }

            break;
        }

        if (pstAuxErrorParams->stNackData.bNack)
        {

            if (pstAuxErrorParams->stNackData.bNackAlways)
            {
                bRet = AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_NACK);
            }
            else
            {
                if (pstAuxErrorParams->stNackData.ulCurrNackCount < pstAuxErrorParams->stNackData.ulMaxNackCount)
                {
                    bRet = AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, 0, eAUX_NACK);
                }
                else
                {
                    if (!pstAuxErrorParams->stNackData.bNackOnlyFirstTime)
                    {
                        pstAuxErrorParams->stNackData.ulCurrNackCount = 0;
                    }

                    // else: bRet = FALSE: False means asking the Caller to Send an ACK
                }
            }

            break;
        }

        if (pstAuxErrorParams->stReceiveErrorData.bReceiveError)
        {

            if (pstAuxErrorParams->stReceiveErrorData.bReceiveErrorAlways)
            {
                bRet = AUXINTERFACE_SendAuxReceiveErrorReply(pstDPAuxInterface);
            }
            else
            {
                if (pstAuxErrorParams->stReceiveErrorData.ulCurrReceiveErrorCount < pstAuxErrorParams->stReceiveErrorData.ulMaxReceiveErrorCount)
                {
                    bRet = AUXINTERFACE_SendAuxReceiveErrorReply(pstDPAuxInterface);
                }
                else
                {
                    if (!pstAuxErrorParams->stReceiveErrorData.bReceiveErrorOnlyFirstTime)
                    {
                        pstAuxErrorParams->stReceiveErrorData.ulCurrReceiveErrorCount = 0;
                    }

                    // else bRet = FALSE : False means asking the Caller to Send an ACK
                }
            }

            break;
        }

        if (pstAuxErrorParams->stPartialWriteData.bPartialWrite)
        {
            // Read Partial Data from Data Regs here

            if (pstAuxErrorParams->stPartialWriteData.bPartialWriteAlways)
            {
                bRet = AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, pstAuxErrorParams->stPartialWriteData.ucNumOfPartialBytesToWrite, eAUX_NACK);
            }
            else
            {
                if (pstAuxErrorParams->stPartialWriteData.ucCurrPartialWriteCount < pstAuxErrorParams->stPartialWriteData.ucMaxPartialWriteCount)
                {
                    bRet = AUXINTERFACE_SendAuxNACKOrDeferReply(pstDPAuxInterface, pstAuxErrorParams->stPartialWriteData.ucNumOfPartialBytesToWrite, eAUX_NACK);
                }
                else
                {
                    if (!pstAuxErrorParams->stPartialWriteData.bPartialWriteOnlyFirstTime)
                    {
                        pstAuxErrorParams->stPartialWriteData.ucCurrPartialWriteCount = 0;
                    }

                    // else bRet = FALSE: False means asking the Caller to Send an ACK
                }
            }

            break;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN AUXINTERFACE_SendAuxAckReply(PDPAUX_INTERFACE pstDPAuxInterface, UCHAR ucMessageSize, AUX_REPLY_COMMAND_TYPES eAuxReplyType)
{
    PAUX_CTRLREG_STRUCT pstAuxCtrlReg = pstDPAuxInterface->pstAuxCtlReg;
    PAUX_DATAREG_STRUCT pstAuxDataReg = &pstDPAuxInterface->pstAuxDataRegs[0];
    AUX_COMMAND_BYTE    stAuxCmdByte  = { 0 };

    stAuxCmdByte.AuxCommand.CmdByte.ucCommand = eAuxReplyType;

    pstAuxDataReg[0].DataRegBytes.ucData1 = stAuxCmdByte.AuxCommand.ucValue;

    pstAuxCtrlReg->CtrlRegBits.bDone = 1;

    pstAuxCtrlReg->CtrlRegBits.ulMessageSize = ucMessageSize + sizeof(UCHAR); // Plus one to account for the command byte

    AUXINTERFACE_ClearControlRegSendBusyBit(pstDPAuxInterface);

    return TRUE;
}

BOOLEAN AUXINTERFACE_SendAuxNACKOrDeferReply(PDPAUX_INTERFACE pstDPAuxInterface, UCHAR ucPartialWriteSize, AUX_REPLY_COMMAND_TYPES eAuxReplyType)
{
    PAUX_CTRLREG_STRUCT pstAuxCtrlReg = pstDPAuxInterface->pstAuxCtlReg;
    PAUX_DATAREG_STRUCT pstAuxDataReg = &pstDPAuxInterface->pstAuxDataRegs[0];
    AUX_COMMAND_BYTE    stAuxCmdByte  = { 0 };

    stAuxCmdByte.AuxCommand.CmdByte.ucCommand = eAuxReplyType;

    pstAuxDataReg[0].DataRegBytes.ucData1 = stAuxCmdByte.AuxCommand.ucValue;

    pstAuxDataReg[0].DataRegBytes.ucData2 = ucPartialWriteSize;

    pstAuxCtrlReg->CtrlRegBits.bDone = 1;

    pstAuxCtrlReg->CtrlRegBits.ulMessageSize = (ucPartialWriteSize ? 1 : 0) + sizeof(UCHAR); // Plus one to account for the command byte

    AUXINTERFACE_ClearControlRegSendBusyBit(pstDPAuxInterface);

    return TRUE;
}

BOOLEAN AUXINTERFACE_SendAuxTimeoutReply(PDPAUX_INTERFACE pstDPAuxInterface)
{
    PAUX_CTRLREG_STRUCT pstAuxCtrlReg = pstDPAuxInterface->pstAuxCtlReg;

    pstAuxCtrlReg->CtrlRegBits.bTimeOutError = 1;

    AUXINTERFACE_ClearControlRegSendBusyBit(pstDPAuxInterface);

    return TRUE;
}

BOOLEAN AUXINTERFACE_SendAuxReceiveErrorReply(PDPAUX_INTERFACE pstDPAuxInterface)
{

    PAUX_CTRLREG_STRUCT pstAuxCtrlReg = pstDPAuxInterface->pstAuxCtlReg;

    GFXVALSIM_FUNC_ENTRY();

    pstAuxCtrlReg->CtrlRegBits.bReceiveError = 1;

    AUXINTERFACE_ClearControlRegSendBusyBit(pstDPAuxInterface);

    GFXVALSIM_FUNC_EXIT(0);

    return TRUE;
}

void AUXINTERFACE_ClearControlRegSendBusyBit(PDPAUX_INTERFACE pstDPAuxInterface)
{

    pstDPAuxInterface->pstAuxCtlReg->CtrlRegBits.bSendOrBusy = 0;
    // Set Done and other values
}

DP_TOPOLOGY_TYPE AUXINTERFACE_GetTopologyType(PDPAUX_INTERFACE pstDPAuxInterface)
{
    return pstDPAuxInterface->eTopologyType;
}

PVOID AUXINTERFACE_GetMSTTopologPtr(PDPAUX_INTERFACE pstDPAuxInterface)
{
    return pstDPAuxInterface->pstDP12Topology;
}

PVOID AUXINTERFACE_GetSSTDisplayInfoPtr(PDPAUX_INTERFACE pstDPAuxInterface)
{
    return pstDPAuxInterface->pstSSTDisplayInfo;
}

PUCHAR AUXINTERFACE_SetDwnStrmDPCDMap(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucDPCDBuff, ULONG ulDPCDSize)
{
    PUCHAR pvDPCDBuffToRet = NULL;

    if (ulDPCDSize != 0 && ulDPCDSize <= MAX_CURRENT_DPCDS_SUPPORTED && pucDPCDBuff && pstDPAuxInterface && pstDPAuxInterface->pucDownStreamDPCDBuff)
    {
        memcpy_s(pstDPAuxInterface->pucDownStreamDPCDBuff, ulDPCDSize, pucDPCDBuff, ulDPCDSize);
        pstDPAuxInterface->ulDPCDBuffSize = ulDPCDSize;
        pvDPCDBuffToRet                   = pstDPAuxInterface->pucDownStreamDPCDBuff;
    }
    GFXVALSIM_FUNC_EXIT((pvDPCDBuffToRet == NULL) ? 1 : 0);

    return pvDPCDBuffToRet;
}

PUCHAR AUXINTERFACE_GetDwnStrmDPCDMap(PDPAUX_INTERFACE pstDPAuxInterface)
{
    return pstDPAuxInterface->pucDownStreamDPCDBuff;
}

BOOLEAN AUXINTERFACE_ReadDPCDAppWorld(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucReadBuff, ULONG ulDPCDAddress, ULONG ulLength)
{
    BOOLEAN bRet = FALSE;

    do
    {
        // Boundary check for the continuous DPCD binary data provided by the app
        if (ulDPCDAddress + ulLength <= pstDPAuxInterface->ulDPCDBuffSize)
        {
            memcpy_s(pucReadBuff, ulLength, &pstDPAuxInterface->pucDownStreamDPCDBuff[ulDPCDAddress], ulLength);
        }
        else
        {

            ULONG ulCount = 0;

            *pucReadBuff = 0;

            if (ulLength != 1)
            {
                // In this dynamic DPCD support range, we don't support only DPCD Read length = 1
                break;
            }

            for (; ulCount < pstDPAuxInterface->arrBackupDPCDBuff.ulCurrentFilledSize; ulCount++)
            {
                if (ulDPCDAddress == pstDPAuxInterface->arrBackupDPCDBuff.BackupDPCDBuff[ulCount].ulStartOffset)
                {
                    *pucReadBuff = pstDPAuxInterface->arrBackupDPCDBuff.BackupDPCDBuff[ulCount].ucValue;
                }
            }
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN AUXINTERFACE_WriteDPCDAppWorld(PDPAUX_INTERFACE pstDPAuxInterface, PUCHAR pucWriteBuff, ULONG ulDPCDAddress, ULONG ulLength)
{
    BOOLEAN bRet = FALSE;

    do
    {
        // Boundary check for the continuous DPCD binary data provided by the app
        if (ulDPCDAddress + ulLength <= pstDPAuxInterface->ulDPCDBuffSize)
        {
            memcpy_s(&pstDPAuxInterface->pucDownStreamDPCDBuff[ulDPCDAddress], ulLength, pucWriteBuff, ulLength);
        }
        else
        {

            ULONG ulCount = 0;

            if (ulLength != 1)
            {
                // In this dynamic DPCD support range, we don't support only DPCD Read length = 1
                break;
            }

            for (; ulCount < pstDPAuxInterface->arrBackupDPCDBuff.ulCurrentFilledSize; ulCount++)
            {
                if (ulDPCDAddress == pstDPAuxInterface->arrBackupDPCDBuff.BackupDPCDBuff[ulCount].ulStartOffset)
                {
                    pstDPAuxInterface->arrBackupDPCDBuff.BackupDPCDBuff[ulCount].ucValue = *pucWriteBuff;
                }
            }
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN AUXINTERFACE_CleanUp(PDPAUX_INTERFACE pstDPAuxInterface)
{
    BOOLEAN           bRet          = FALSE;
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    do
    {
        if (pstDPAuxInterface == NULL)
        {
            break;
        }

        // Cleanup SST Display
        if (pstDPAuxInterface->pstSSTDisplayInfo)
        {
            SSTDISPLAY_Cleanup(pstDPAuxInterface->pstSSTDisplayInfo);
            pstPortingObj->pfnFreeMem(pstDPAuxInterface->pstSSTDisplayInfo);
            pstDPAuxInterface->pstSSTDisplayInfo = NULL;
        }

        // Cleanup MST Topology
        if (pstDPAuxInterface->pstDP12Topology)
        {
            DP12TOPOLOGY_Cleanup(pstDPAuxInterface->pstDP12Topology);
            pstPortingObj->pfnFreeMem(pstDPAuxInterface->pstDP12Topology);
            pstDPAuxInterface->pstDP12Topology = NULL;
        }

        // Since in MST mode, the DPCD buffer is shared between Branch connected to source and DPAuxInterface
        // as in both point the same DPCD buffer so if we were in MST mode when this clean up call came, then the above DP12TOPOLOGY_Cleanup
        // call would have already free'd the buffer pointed to by pstDPAuxInterface->pucDownStreamDPCDBuff
        // So we need pstDPAuxInterface->bIsMSTTopology == FALSE check here or else it would cause a BSOD trying to free the already freed memory
        if (pstDPAuxInterface->pucDownStreamDPCDBuff)
        {
            pstPortingObj->pfnFreeMem(pstDPAuxInterface->pucDownStreamDPCDBuff);
        }

        // Clean and Deregister all registered clients
        AUXINTERFACE_DeRegisterAllDPCDClients(pstDPAuxInterface);

    } while (FALSE);

    return bRet;
}

// Alternate Approach with Link List
/*
PDPCD_CLIENTINFO pDPCDClientInfo = NULL;
PDP_LIST_ENTRY pDPListEntry =  NULL;

pDPListEntry = pstPortingObj->pfnInterLockedTraverseList(&pstDPAuxInterface->DPCDClientListHead, pDPListEntry);

while (pDPListEntry)
{
//Lets check if a client isn't alread registered, in which case print error and exit
pDPCDClientInfo = (PDPCD_CLIENTINFO)pDPListEntry;

if (ulDPCDStartAddress >= pDPCDClientInfo->ulDPCDStartAddress  &&
ulDPCDEndAddress <= pDPCDClientInfo->ulDPCDEndAddress)
{
//printf("DPCD Client Already registered for the given DPCD range /r/n");
bRet = FALSE;
break; //break from while loop
}

pDPListEntry = pstPortingObj->pfnInterLockedTraverseList(&pstDPAuxInterface->DPCDClientListHead, pDPListEntry);
}

if (!bRet)
{
break; //break from for loop
}
*/
