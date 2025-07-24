// DP1.2Infra.cpp : Defines the entry point for the console application.
//

#include "MSTTopology.h"
#include "..\\CommonCore\\ExternalCallBacks.h"
#include "AuxDPCDClient.h"
#include "..\CommonInclude\ETWLogging.h"

void DP12TOPOLOGY_CreateRad(PMST_RELATIVEADDRESS pucUpStreamRAD, PMST_RELATIVEADDRESS pucNewRad, UCHAR ucUpStreamPortNumber);

PORTABLE_THREAD_ROUTINE_SIGNATURE(DP12TOPOLOGY_DownRequestHandlerThread, lpThreadParameter);
PORTABLE_THREAD_ROUTINE_SIGNATURE(DP12TOPOLOGY_DownReplyHandlerThread, lpThreadParameter);
PORTABLE_THREAD_ROUTINE_SIGNATURE(DP12TOPOLOGY_UpRequestHandlerThread, lpThreadParameter);

BOOLEAN DP12TOPOLOGY_SendACKReply(PBRANCH_NODE pstBranchNode, ULONG ulDwnReqBuffIndex);
BOOLEAN DP12TOPOLOGY_SendNAKReply(PBRANCH_NODE pstBranchNode);
BOOLEAN DP12TOPOLOGY_PostProcessAndFowardDownStreamsReply(PBRANCH_NODE pstBranchNode, UCHAR ucGeneratedEventPortNum);
BOOLEAN DP12TOPOLOGY_SendDownReply(PBRANCH_NODE pstBranchNode);

PMST_DWNREQUEST_BUFF_INFO DP12TOPOLOGY_GetAvailableDownReqBuff(PBRANCH_NODE pstBranchNode);
void                      DP12TOPOLOGY_SetDownReqBuffState(PBRANCH_NODE pstBranchNode, ULONG ulThisBuffIndex, DWNREQBUFF_SETSTATE eSetState);
BOOLEAN                   DP12TOPOLOGY_CheckSeqNumValidity(PBRANCH_NODE pstBranchNode, UCHAR ucSeqNum);

BOOLEAN DP12TOPOLOGY_UpdateDownStreamBranchVCPayloadTable(PBRANCH_NODE pstUpStreamBranchNode, UCHAR ucDownStreamPortNum);

PORTABLE_TIMER_CALLBACK_SIGNATURE(DP12TOPOLOGY_VCPayloadTableUpdateStatusTimerCb, pvTimerCbContext);
void DP12TOPOLOGY_VCPayloadTableUpdateStatusNonTimer(PUCHAR pucBranchDPCDBuff);

PROCESSING_RESULT DP12TOPOLOGY_AllocatePayloadDownReplyPostProcess(PBRANCH_NODE pstBranchNode, UCHAR ucGeneratedEventPortNum, BOOLEAN bSeqNo);

void DP12TOPOLOGY_DFSGetTopologyRAD(PBRANCH_NODE pstBranchNode, PBRANCHDISP_RAD_ARRAY pstBranchDispRADArray, ULONG ulParentIndex);

USHORT DP12TOPOLOGY_ComputePBNBasedOnLinkRateAndLaneCount(UCHAR ucMaxLinkRate, UCHAR ucMaxLaneCount);
void   DP12TOPOLOGY_DFSBranchCleanUp(PBRANCH_NODE pstBranchNode);
void   DP12TOPOLOGY_BranchNodeCleanUp(PBRANCH_NODE pstBranchNode);
void   DP12TOPOLOGY_DisplayNodeCleanUp(PDISPLAY_NODE pstDisplayNode);
void   DP12TOPOLOGY_DFSReCalculateDownStreamNodesRAD(PBRANCH_NODE pstBranchNode, PMST_RELATIVEADDRESS pstUpStreamNodeRAD, UCHAR ucUpStreamOutPort);
void   DP12TOPOLOGY_DFSExtractCurrentTopologyInArrayFormat(PBRANCH_NODE pstBranchNode, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArray, ULONG ulParentIndex,
                                                           UCHAR ucUpstreamDeviceOutPortNumber, UCHAR ucThisDevicePortNumber);

PDP12_TOPOLOGY DP12TOPOLOGY_TopologyObjectInit()
{
    GFXVALSIM_FUNC_ENTRY();

    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    PDP12_TOPOLOGY pstDP12Topology = NULL;

    pstDP12Topology = (PDP12_TOPOLOGY)pstPortingObj->pfnAllocateMem(sizeof(DP12_TOPOLOGY), TRUE);

    GFXVALSIM_FUNC_EXIT(pstDP12Topology == NULL ? 0 : 1);

    return pstDP12Topology;
}

PBRANCH_NODE DP12TOPOLOGY_CreateBranchNode(PDP12_TOPOLOGY pstDP12Topology, MST_PEER_DEVICE_TYPE ePeerDeviceType, UCHAR ucTotalInputPorts, UCHAR ucTotalPhysicalPorts,
                                           UCHAR ucTotalVirtualPorts, ULONG ulMaxLinkRate, ULONG ulMaxLaneCount, ULONG ulBranchReplyDelay, USHORT usTotalAvailablePBN,
                                           ULONG ulLinkAddressDelay, ULONG ulRemoteI2ReadDelay, ULONG ulRemoteI2WriteDelay, ULONG ulRemoteDPCDReadDelay,
                                           ULONG ulRemoteDPCDWriteDelay, ULONG ulEPRDelay, ULONG ulAllocatePayloadDelay, ULONG ulClearPayLoadDelay, PUCHAR pucDPCDName)

{
    GFXVALSIM_FUNC_ENTRY();

    PBRANCH_NODE      pstBranchNode          = NULL;
    BOOLEAN           bRet                   = FALSE;
    ULONG             ulCount                = 0;
    PBRANCHDISP_DPCD  pstTempBranchDPCDMap   = NULL;
    ULONG             ulDPCDBuffSize         = 0;
    USHORT            usLinkRateLaneCountPBN = 0;
    PPORTINGLAYER_OBJ pstPortingObj          = GetPortingObj();
    RECEIVER_CAPS     stReceiverCaps         = { 0 };
    do
    {
        if (ucTotalPhysicalPorts + ucTotalVirtualPorts + ucTotalInputPorts > MAX_PORTS_PER_BRANCH)
        {
            break;
        }

        pstBranchNode = (PBRANCH_NODE)pstPortingObj->pfnAllocateMem(sizeof(BRANCH_NODE), TRUE);

        if (pstBranchNode)
        {
            if (!pstPortingObj->pfnCreateGuid(&pstBranchNode->uidBranchGUID))
            {
                break;
            }

            pstBranchNode->eDPCDRev                = eDPCDRev_Invalid;
            pstBranchNode->eNodeType               = eBRANCH;
            pstBranchNode->bIsBranchConnectedToSrc = FALSE;
            pstBranchNode->ePeerDeviceType         = ePeerDeviceType;
            pstBranchNode->usTotalAvailablePBN     = usTotalAvailablePBN;
            pstBranchNode->usCurrentAvailablePBN   = usTotalAvailablePBN;
            pstBranchNode->ucTotalInputPorts       = ucTotalInputPorts;
            pstBranchNode->ucAvailableInputPorts   = ucTotalInputPorts;

            pstBranchNode->ucTotalPhysicalPorts     = ucTotalPhysicalPorts;
            pstBranchNode->ucAvailablePhysicalPorts = ucTotalPhysicalPorts;

            pstBranchNode->ucTotalVirtualPorts     = ucTotalVirtualPorts;
            pstBranchNode->ucAvailableVirtualPorts = ucTotalVirtualPorts;

            // Initialize Function Pointers
            pstBranchNode->pfnGetAvailableDownReqBuff = DP12TOPOLOGY_GetAvailableDownReqBuff;
            pstBranchNode->pfnSetDownReqBuffState     = DP12TOPOLOGY_SetDownReqBuffState;
            pstBranchNode->pfnCheckSeqNumValidity     = DP12TOPOLOGY_CheckSeqNumValidity;

            // Initialize DPCDMap

            if (pucDPCDName)
            {
                pstTempBranchDPCDMap = DP12TOPOLOGY_GetNodeDPCD(pstDP12Topology, pucDPCDName);

                if (pstTempBranchDPCDMap == NULL)
                {
                    break;
                }

                // We can't just reference the Global DPCD buffer. We need to make a copy of it because DPCD is Read-Write
                // And each Node's DPCD data can be individually written to. So we can't share the single global copy of DPDCD data
                // between different nodes.
                memcpy_s(pstBranchNode->stBranchDPCDMap.ucDPCDName, MAX_NODE_NAME_SIZE, pstTempBranchDPCDMap->ucDPCDName, MAX_NODE_NAME_SIZE);

                ulDPCDBuffSize = pstBranchNode->stBranchDPCDMap.ulDPCDBuffSize = pstTempBranchDPCDMap->ulDPCDBuffSize;

                pstBranchNode->stBranchDPCDMap.pucDPCDBuff = pstPortingObj->pfnAllocateMem(ulDPCDBuffSize, TRUE);

                memcpy_s(pstBranchNode->stBranchDPCDMap.pucDPCDBuff, ulDPCDBuffSize, pstTempBranchDPCDMap->pucDPCDBuff, ulDPCDBuffSize);

                AUXHELPER_GetReceiverCapability(pstBranchNode->stBranchDPCDMap.pucDPCDBuff, &stReceiverCaps);
                pstBranchNode->eDPCDRev = stReceiverCaps.eDPCDRev;

                // Updating the FEC path info for the branch node
                pstBranchNode->ucFECPathInfo = pstBranchNode->stBranchDPCDMap.pucDPCDBuff[FEC_CAPABILITY] & 1;

                // Update TotalAvailablePBN and PBN per Slot value
                usLinkRateLaneCountPBN = DP12TOPOLOGY_ComputePBNBasedOnLinkRateAndLaneCount(pstBranchNode->stBranchDPCDMap.pucDPCDBuff[stReceiverCaps.ulMaxLinkRateDPCDAddress],
                                                                                            pstBranchNode->stBranchDPCDMap.pucDPCDBuff[stReceiverCaps.ulMaxLaneCountDPCDAddress]);
                pstBranchNode->usTotalAvailablePBN   = min(pstBranchNode->usTotalAvailablePBN, usLinkRateLaneCountPBN);
                pstBranchNode->usCurrentAvailablePBN = pstBranchNode->usTotalAvailablePBN;
            }

            // Allocating additional space of MST_MAX_SBM_CHUNK_SIZE because our header packetization logic uses the same buffer to append header to data in this buffer
            // For that we need to move around data and it may go beyond MST_SBM_BUFF_SIZE buffer size temporarily
            pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_1].puchBuffPtr = pstPortingObj->pfnAllocateMem(MST_SBM_BUFF_SIZE + MST_MAX_SBM_CHUNK_SIZE, TRUE);

            if (pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_1].puchBuffPtr == NULL)
            {
                break;
            }

            if (!pstPortingObj->pfnInitializeDPEvent(&pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_1].stBuffEvent, FALSE, FALSE))
            {
                break;
            }

            pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_1].ucThisBuffIndex = INDEX_BUFF_1;

            // Allocating additional space of MST_MAX_SBM_CHUNK_SIZE because our header packetization logic uses the same buffer to append header to data in this buffer
            // For that we need to move around data and it may go beyond MST_SBM_BUFF_SIZE buffer size temporarily
            pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_2].puchBuffPtr = pstPortingObj->pfnAllocateMem(MST_SBM_BUFF_SIZE + MST_MAX_SBM_CHUNK_SIZE, TRUE);

            if (pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_2].puchBuffPtr == NULL)
            {
                break;
            }

            if (!pstPortingObj->pfnInitializeDPEvent(&pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_2].stBuffEvent, FALSE, FALSE))
            {
                break;
            }

            pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_2].ucThisBuffIndex = INDEX_BUFF_2;

            pstBranchNode->stDownReplyBuffInfo.puchBuffPtr = pstPortingObj->pfnAllocateMem(MST_SBM_BUFF_SIZE, TRUE);

            if (pstBranchNode->stDownReplyBuffInfo.puchBuffPtr == NULL)
            {
                break;
            }

            if (!pstPortingObj->pfnInitializeDPEvent(&pstBranchNode->stDownRequestHandlerThreadKillEvent, FALSE, FALSE))
            {
                break;
            }

            for (ulCount = ucTotalInputPorts; ulCount < MAX_PORTS_PER_BRANCH; ulCount++)
            {
                // Mark the ports beyond ucTotalInputPorts as not available as input port. They could be used as only output ports
                pstBranchNode->stInportList[ulCount].ucInputPortNumber = DP_PORT_NA;
            }

            for (ulCount = 0; ulCount < ucTotalInputPorts; ulCount++)
            {
                // Mark the ports before ucTotalInputPorts as not available as output port. They could be used as only input ports
                pstBranchNode->stOutPortList[ulCount].ucOutPortNumber = DP_PORT_NA;
            }

            // Below are the event Objects for ACK/NACK generated by the curent branch node. It would be the first event in the list. This event
            // So its index is the EventList of the downreplyhandler of this node would be same as the index of the downreqbuffer.
            // This even Will be fired by the downrequest handler thread of the branch node if the same branch node  thread will be the target node and send ACK/NAK
            // The correspondance between index in the downreply handler thread event list and downreqbuffer index is maintained to figure which downreqbuff for this node has
            // ACK/NACK data Rest all events will be fired by the downstream connected branches when the down reply is ready
            ulCount = INDEX_BUFF_1;
            if (pstPortingObj->pfnInitializeDPEvent(&pstBranchNode->stDownStreamPortEvents.stDownReplyEventList[ulCount], FALSE, FALSE))
            {
                pstBranchNode->pstThisNodeACKReplyEvent[0]                       = &pstBranchNode->stDownStreamPortEvents.stDownReplyEventList[ulCount];
                pstBranchNode->stDownStreamPortEvents.ucPortMappingList[ulCount] = DP_PORT_NA;
                pstBranchNode->stDownStreamPortEvents.ulEventInUseCount++;
            }
            else
            {
                // ASSERT
                break;
            }

            ulCount = INDEX_BUFF_2;
            if (pstPortingObj->pfnInitializeDPEvent(&pstBranchNode->stDownStreamPortEvents.stDownReplyEventList[ulCount], FALSE, FALSE))
            {
                pstBranchNode->pstThisNodeACKReplyEvent[1]                       = &pstBranchNode->stDownStreamPortEvents.stDownReplyEventList[ulCount];
                pstBranchNode->stDownStreamPortEvents.ucPortMappingList[ulCount] = DP_PORT_NA;
                pstBranchNode->stDownStreamPortEvents.ulEventInUseCount++;
            }
            else
            {
                // ASSERT
                break;
            }

            ulCount = NAK_REPLY_READY_INDEX;
            if (pstPortingObj->pfnInitializeDPEvent(&pstBranchNode->stDownStreamPortEvents.stDownReplyEventList[ulCount], FALSE, FALSE))
            {
                pstBranchNode->pstThisNodeNAKReplyEvent                          = &pstBranchNode->stDownStreamPortEvents.stDownReplyEventList[ulCount];
                pstBranchNode->stDownStreamPortEvents.ucPortMappingList[ulCount] = DP_PORT_NA;
                pstBranchNode->stDownStreamPortEvents.ulEventInUseCount++;
            }
            else
            {
                // ASSERT
                break;
            }

            // This event is fired whenever we want to terminate the thread
            ulCount = THREAD_KILL_EVENT_INDEX;
            if (pstPortingObj->pfnInitializeDPEvent(&pstBranchNode->stDownStreamPortEvents.stDownReplyEventList[ulCount], FALSE, FALSE))
            {
                pstBranchNode->pstDownReplyHandlerThreadKillEvent                = &pstBranchNode->stDownStreamPortEvents.stDownReplyEventList[ulCount];
                pstBranchNode->stDownStreamPortEvents.ucPortMappingList[ulCount] = DP_PORT_NA;
                pstBranchNode->stDownStreamPortEvents.ulEventInUseCount++;
            }
            else
            {
                // ASSERT
                break;
            }

            for (ulCount = MAX_NON_DOWNPORTS_EVENTS; ulCount < MAX_NON_DOWNPORTS_EVENTS + MAX_PORTS_PER_BRANCH; ulCount++)
            {
                if (pstPortingObj->pfnInitializeDPEvent(&pstBranchNode->stDownStreamPortEvents.stDownReplyEventList[ulCount], FALSE, FALSE))
                {
                    pstBranchNode->stDownStreamPortEvents.ucPortMappingList[ulCount] = DP_PORT_NA;
                }
                else
                {
                    // ASSERT
                    break;
                }
            }

            if (!pstPortingObj->pfnInitializeDPEvent(&pstBranchNode->stUpReadDownReplyEvent, FALSE, FALSE))
            {
                // ASSERT
                break;
            }

            // Intialize Spin Lock for Up Request/Service IRQ Vector DPCD Handling
            if (!pstPortingObj->pfnInitializeDPLock(&pstBranchNode->stServiceIRQVectorSpinLock))
            {
                break;
            }

            // Create NAK INfo LookAside List for this Branch node to handle Nak processing if upstream device sends requests one after
            // the other that result in NAK reply
            if (!pstPortingObj->pfnInitializeLookAsideList(&pstBranchNode->NakInfoLookAsideListHead, sizeof(MST_NAK_REPLY_INFO), LOOKASIDE_INITIAL_COUNT, MAX_LOOKASIDE_NODE_COUNT,
                                                           LOOKASIDE_EXPAND_FACTOR))
            {
                break;
            }
            // Take the Nak struct entry from lookaside list and put in the processing list;
            if (!pstPortingObj->pfnInitializeListHead(&pstBranchNode->NakInfoProcessingListHead))
            {
                break;
            }

            // Now start Branch Threads

            pstBranchNode->hDownRequestHandlerThreadHandle =
            pstPortingObj->pfnCreateThread(pstBranchNode, DP12TOPOLOGY_DownRequestHandlerThread, &pstBranchNode->dwDownRequestHandlerThreadID, SIMDRV_THREAD_PRIORITY, 0);
            if (pstBranchNode->hDownRequestHandlerThreadHandle == NULL)
            {
                bRet = FALSE;
                break;
            }

            pstBranchNode->hDownReplyHandlerThreadHandle =
            pstPortingObj->pfnCreateThread(pstBranchNode, DP12TOPOLOGY_DownReplyHandlerThread, &pstBranchNode->dwDownReplyHandlerThreadID, SIMDRV_THREAD_PRIORITY, 0);
            if (pstBranchNode->hDownReplyHandlerThreadHandle == NULL)
            {
                bRet = FALSE;
                break;
            }

            bRet = TRUE;
        }

    } while (FALSE);

    if (bRet == FALSE)
    {
        if (pstBranchNode)
        {
            DP12TOPOLOGY_BranchNodeCleanUp(pstBranchNode);
        }
    }
    GFXVALSIM_FUNC_EXIT(0);
    return pstBranchNode;
}

PDISPLAY_NODE DP12TOPOLOGY_CreateDisplayNode(PDP12_TOPOLOGY pstDP12Topology, MST_PEER_DEVICE_TYPE ePeerDeviceType, UCHAR ucTotalInputPorts, USHORT usTotalAvailablePBN,
                                             ULONG ulMaxLinkRate, ULONG ulMaxLaneCount, ULONG ulRemoteI2ReadDelay, ULONG ulRemoteI2WriteDelay, ULONG ulRemoteDPCDReadDelay,
                                             ULONG ulRemoteDPCDWriteDelay, PUCHAR pucDPCDName, PUCHAR pucDisplayName)
{
    GFXVALSIM_FUNC_ENTRY();

    BOOLEAN           bRet                  = FALSE;
    PDISPLAY_NODE     pstDisplayNode        = NULL;
    UCHAR             ucCount               = 0;
    PBRANCHDISP_DPCD  pstTempDisplayDPCDMap = NULL;
    ULONG             ulDPCDBuffSize        = 0;
    PPORTINGLAYER_OBJ pstPortingObj         = GetPortingObj();

    do
    {
        if (ucTotalInputPorts > MAX_STREAMSINK_PER_DISPLAY)
        {
            break;
        }

        pstDisplayNode = (PDISPLAY_NODE)pstPortingObj->pfnAllocateMem(sizeof(DISPLAY_NODE), TRUE);

        if (pstDisplayNode)
        {
            if (!pstPortingObj->pfnCreateGuid(&pstDisplayNode->uidDisplayGUID))
            {
                break;
            }

            pstDisplayNode->eDPCDRev              = eDPCDRev_Invalid;
            pstDisplayNode->eNodeType             = eDISPLAY;
            pstDisplayNode->ePeerDeviceType       = ePeerDeviceType;
            pstDisplayNode->usTotalAvailablePBN   = usTotalAvailablePBN;
            pstDisplayNode->usCurrentAvailablePBN = usTotalAvailablePBN;
            pstDisplayNode->ucTotalInputPorts     = ucTotalInputPorts;

            pstDisplayNode->pstDisplayEDID = DP12TOPOLOGY_GetDisplayEDID(pstDP12Topology, pucDisplayName);

            if (pstDisplayNode->pstDisplayEDID == NULL)
            {
                break;
            }

            // Initialize DPCDMap
            pstTempDisplayDPCDMap = DP12TOPOLOGY_GetNodeDPCD(pstDP12Topology, pucDPCDName);

            if (pstTempDisplayDPCDMap == NULL)
            {
                break;
            }

            // We can't just reference the Global DPCD buffer. We need to make a copy of it because DPCD is Read-Write
            // And each Node's DPCD data can be individually written to. So we can't share the single global copy of DPDCD data
            // between different nodes. This is different from EDID data handling. Each display can reference a single Global copy
            // because EDID data is Read only
            memcpy_s(pstDisplayNode->stDisplayDPCDMap.ucDPCDName, MAX_NODE_NAME_SIZE, pstTempDisplayDPCDMap->ucDPCDName, MAX_NODE_NAME_SIZE);

            ulDPCDBuffSize = pstDisplayNode->stDisplayDPCDMap.ulDPCDBuffSize = pstTempDisplayDPCDMap->ulDPCDBuffSize;

            pstDisplayNode->stDisplayDPCDMap.pucDPCDBuff = pstPortingObj->pfnAllocateMem(ulDPCDBuffSize, TRUE);

            memcpy_s(pstDisplayNode->stDisplayDPCDMap.pucDPCDBuff, ulDPCDBuffSize, pstTempDisplayDPCDMap->pucDPCDBuff, ulDPCDBuffSize);

            // Updating FEC path infor for the display node.
            pstDisplayNode->ucFECPathInfo = pstDisplayNode->stDisplayDPCDMap.pucDPCDBuff[FEC_CAPABILITY] & 1;

            // Now copy the revision number from first byte of DPCD
            pstDisplayNode->eDPCDRev = *pstDisplayNode->stDisplayDPCDMap.pucDPCDBuff;

            for (ucCount = ucTotalInputPorts; ucCount < MAX_STREAMSINK_PER_DISPLAY; ucCount++)
            {
                // As per spec's port numbering, these input ports and not available

                pstDisplayNode->stInportList[ucCount].ucInputPortNumber = DP_PORT_NA;
            }

            bRet = TRUE;
        }

    } while (FALSE);

    if (bRet == FALSE)
    {
        if (pstDisplayNode)
        {
            DP12TOPOLOGY_DisplayNodeCleanUp(pstDisplayNode);
        }
    }

    GFXVALSIM_FUNC_EXIT(0);

    return pstDisplayNode;
}

NODE_ADD_ERRROR_CODES DP12TOPOLOGY_AddFirstBranch(PDP12_TOPOLOGY pstDP12Topology, PBRANCH_NODE pstNewBranchNode, UCHAR ucNewBranchInputPort, PUCHAR pucSharedDPCDBuff,
                                                  PUCHAR pucDPCDName, ULONG ulDPCDSize)
{
    NODE_ADD_ERRROR_CODES eRet                   = eGENERIC_ERROR;
    USHORT                usLinkRateLaneCountPBN = 0;
    PPORTINGLAYER_OBJ     pstPortingObj          = GetPortingObj();
    RECEIVER_CAPS         stReceiverCaps         = { 0 };

    do
    {
        if (!(pstDP12Topology && pstNewBranchNode))
        {
            break;
        }

        if (ucNewBranchInputPort > pstNewBranchNode->ucTotalInputPorts)
        {
            eRet = eINVALID_INPUT_PORT;
            break;
        }

        if (pstNewBranchNode->stInportList[ucNewBranchInputPort].bPortConnectedStatus == TRUE)
        {
            eRet = ePORT_ALREADY_IN_USE;
            break;
        }

        if (pstNewBranchNode->ucAvailableInputPorts)
        {
            pstNewBranchNode->ucAvailableInputPorts--;
        }
        else
        {
            eRet = eNO_FREE_PORT_AVAILABLE;
            break;
        }

        if (pucSharedDPCDBuff != NULL && pucDPCDName != NULL && ulDPCDSize != 0)
        {
            // DPCD Buffer handling for the branch connected to the Source is different from other branches
            // This branch shares the DPCD buffer pointer actually stored in AuxInterface. Because Auxinterface
            // would directly reply to most Native aux transactions without forwarding it to branch.
            // This reduces latency and simplifies things
            // But First branch needs a pointer to this buffer mainly for handling 0x201 for now.
            // Because for now 0x201 has a handler registered for it and that handler updates the DPCD
            memcpy_s(pstNewBranchNode->stBranchDPCDMap.ucDPCDName, MAX_NODE_NAME_SIZE, pucDPCDName, MAX_NODE_NAME_SIZE);

            pstNewBranchNode->stBranchDPCDMap.ulDPCDBuffSize = ulDPCDSize;

            pstNewBranchNode->stBranchDPCDMap.pucDPCDBuff = pucSharedDPCDBuff;

            AUXHELPER_GetReceiverCapability(pstNewBranchNode->stBranchDPCDMap.pucDPCDBuff, &stReceiverCaps);
            pstNewBranchNode->eDPCDRev      = stReceiverCaps.eDPCDRev;
            pstNewBranchNode->ucFECPathInfo = pstNewBranchNode->stBranchDPCDMap.pucDPCDBuff[FEC_CAPABILITY] & 1;

            // Update TotalAvailablePBN and PBN per Slot value
            usLinkRateLaneCountPBN = DP12TOPOLOGY_ComputePBNBasedOnLinkRateAndLaneCount(pstNewBranchNode->stBranchDPCDMap.pucDPCDBuff[stReceiverCaps.ulMaxLinkRateDPCDAddress],
                                                                                        pstNewBranchNode->stBranchDPCDMap.pucDPCDBuff[stReceiverCaps.ulMaxLaneCountDPCDAddress]);
            pstNewBranchNode->usTotalAvailablePBN   = min(pstNewBranchNode->usTotalAvailablePBN, usLinkRateLaneCountPBN);
            pstNewBranchNode->usCurrentAvailablePBN = pstNewBranchNode->usTotalAvailablePBN;
        }

        // pucUpReqestBuff is being created in AddFirstBranch rather than CreateBranchNode
        // Because only the first branch i.e. branch connected to source will need it to send CSN and other uprequest messages
        pstNewBranchNode->stUpRequestBuffInfo.puchUpReqBuffPtr = pstPortingObj->pfnAllocateMem(MST_SBM_BUFF_SIZE, TRUE);

        if (pstNewBranchNode->stUpRequestBuffInfo.puchUpReqBuffPtr == NULL)
        {
            break;
        }

        // pucUpReplyBuff is being created in AddFirstBranch rather than CreateBranchNode
        // Because only the first branch i.e. branch connected to source will Service the UpReply Coming from Source
        pstNewBranchNode->stUpReplyInfo.puchBuffPtr = pstPortingObj->pfnAllocateMem(MST_SBM_BUFF_SIZE, TRUE);

        if (pstNewBranchNode->stUpReplyInfo.puchBuffPtr == NULL)
        {
            break;
        }

        // All the Up Requests like CSN and RSN will be handled by first Branch itself hence creating the UpRequestHandler thread
        // and related data structures in this Add first branch instead of create first branch
        // Initialize Up Request List Head;
        if (!pstPortingObj->pfnInitializeListHead(&pstNewBranchNode->stUpRequestListHead))
        {
            break;
        }

        if (!pstPortingObj->pfnInitializeDPEvent(&pstNewBranchNode->stUpRequestEvent, FALSE, FALSE))
        {
            // ASSERT
            break;
        }

        if (!pstPortingObj->pfnInitializeDPEvent(&pstNewBranchNode->stUpRequestHandlerThreadKillEvent, FALSE, FALSE))
        {
            // ASSERT
            break;
        }

        pstNewBranchNode->hUpRequestHandlerThreadHandle =
        pstPortingObj->pfnCreateThread(pstNewBranchNode, DP12TOPOLOGY_UpRequestHandlerThread, &pstNewBranchNode->dwUpRequestHandlerThreadID, SIMDRV_THREAD_PRIORITY, 0);
        if (pstNewBranchNode->hUpRequestHandlerThreadHandle == NULL)
        {
            break;
        }

        pstNewBranchNode->bIsBranchConnectedToSrc = TRUE;
        pstDP12Topology->pstBranchConnectedToSrc  = pstNewBranchNode;
        pstDP12Topology->ulTotalNumBranches++;

        pstNewBranchNode->stInportList[ucNewBranchInputPort].bPortConnectedStatus     = TRUE;
        pstNewBranchNode->stInportList[ucNewBranchInputPort].eUpStreamNodeType        = eDPSource;
        pstNewBranchNode->stInportList[ucNewBranchInputPort].stUpStreamDevicePeerType = eSOURCEORSSTBRANCHDEVICE;
        pstNewBranchNode->stInportList[ucNewBranchInputPort].ucUpStreamPortNumber     = 0;
        pstNewBranchNode->stInportList[ucNewBranchInputPort].ucInputPortNumber        = ucNewBranchInputPort;
        pstNewBranchNode->stInportList[ucNewBranchInputPort].pvUpStreamNodePointer    = NULL;

        // First Branch doesn't need a RAD but setting LinkCount to 1 would enable creating RADs attached to this Node
        pstNewBranchNode->stBranchRAD.ucTotalLinkCount = 1;

        eRet = eNODE_ADD_SUCCESS;

    } while (FALSE);

    return eRet;
}

NODE_ADD_ERRROR_CODES DP12TOPOLOGY_AddBranch(PDP12_TOPOLOGY pstDP12Topology, PBRANCH_NODE pstTargetBranchNode, PBRANCH_NODE pstNewBranchNode, UCHAR ucTargetBranchOutPort,
                                             UCHAR   ucNewBranchInputPort,
                                             BOOLEAN bSubTopologyAddition) // Set this flag when Adding a sub topology to an already existing
{                                                                          // Existing topology. Mainly used in CSN
    NODE_ADD_ERRROR_CODES eRet = eGENERIC_ERROR;

    do
    {
        if (!(pstTargetBranchNode && pstNewBranchNode))
        {
            eRet = eGENERIC_ERROR;
            break;
        }

        if (ucTargetBranchOutPort < pstTargetBranchNode->ucTotalInputPorts)
        {
            eRet = eINVALID_OUTPUT_PORT;
            break;
        }

        if (ucNewBranchInputPort >= pstNewBranchNode->ucTotalInputPorts)
        {
            eRet = eINVALID_INPUT_PORT;
            break;
        }

        if (pstNewBranchNode->stInportList[ucNewBranchInputPort].bPortConnectedStatus == TRUE)
        {
            eRet = ePORT_ALREADY_IN_USE;
            break;
        }

        if (pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].bPortConnectedStatus == TRUE)
        {
            eRet = ePORT_ALREADY_IN_USE;
            break;
        }

        if (ucTargetBranchOutPort <= MAX_PHYSICAL_OUT_PORTS)
        {
            if (pstTargetBranchNode->ucAvailablePhysicalPorts)
            {
                pstTargetBranchNode->ucAvailablePhysicalPorts--;
            }
            else
            {
                eRet = eNO_FREE_PORT_AVAILABLE;
                break;
            }
        }
        else
        {
            if (pstTargetBranchNode->ucAvailableVirtualPorts)
            {
                pstTargetBranchNode->ucAvailableVirtualPorts--;
            }
            else
            {
                eRet = eNO_FREE_PORT_AVAILABLE;
                break;
            }
        }

        if (pstNewBranchNode->ucAvailableInputPorts)
        {
            pstNewBranchNode->ucAvailableInputPorts--;
        }
        else
        {
            eRet = eNO_FREE_PORT_AVAILABLE;
            break;
        }

        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].bPortConnectedStatus         = TRUE;
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].bConnectedDeviceMsgCapStatus = TRUE; // Since we are adding a branch
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].eConnectedDeviceNodeType     = pstNewBranchNode->eNodeType;
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].stConnectedDevicePeerType    = pstNewBranchNode->ePeerDeviceType;
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].ucConnectedDevicePortNumber  = ucNewBranchInputPort;
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].ucOutPortNumber              = ucTargetBranchOutPort;
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].pvConnectedDeviceNodePointer = pstNewBranchNode;

        pstNewBranchNode->pstDownReplyReadyEvent = &pstTargetBranchNode->stDownStreamPortEvents.stDownReplyEventList[pstTargetBranchNode->stDownStreamPortEvents.ulEventInUseCount];
        pstTargetBranchNode->stDownStreamPortEvents.ucPortMappingList[pstTargetBranchNode->stDownStreamPortEvents.ulEventInUseCount] = ucTargetBranchOutPort;
        pstTargetBranchNode->stDownStreamPortEvents.ulEventInUseCount++;

        pstNewBranchNode->stInportList[ucNewBranchInputPort].bPortConnectedStatus     = TRUE;
        pstNewBranchNode->stInportList[ucNewBranchInputPort].eUpStreamNodeType        = pstTargetBranchNode->eNodeType;
        pstNewBranchNode->stInportList[ucNewBranchInputPort].stUpStreamDevicePeerType = pstTargetBranchNode->ePeerDeviceType;
        pstNewBranchNode->stInportList[ucNewBranchInputPort].ucUpStreamPortNumber     = ucTargetBranchOutPort;
        pstNewBranchNode->stInportList[ucNewBranchInputPort].ucInputPortNumber        = ucNewBranchInputPort;
        pstNewBranchNode->stInportList[ucNewBranchInputPort].pvUpStreamNodePointer    = pstTargetBranchNode;
        pstNewBranchNode->ucFECPathInfo                                               = pstNewBranchNode->ucFECPathInfo & pstTargetBranchNode->ucFECPathInfo;

        pstTargetBranchNode->usDwnStreamPBNPerMTPSlot = pstNewBranchNode->usTotalAvailablePBN / NUM_SLOTS_PER_MTP;

        if (bSubTopologyAddition)
        {
            DP12TOPOLOGY_DFSReCalculateDownStreamNodesRAD(pstNewBranchNode, &pstTargetBranchNode->stBranchRAD, ucTargetBranchOutPort);
        }
        else
        {
            DP12TOPOLOGY_CreateRad(&pstTargetBranchNode->stBranchRAD, &pstNewBranchNode->stBranchRAD, ucTargetBranchOutPort);
        }

        pstDP12Topology->ulTotalNumBranches++;

        eRet = eNODE_ADD_SUCCESS;

    } while (FALSE);

    return eRet;
}
NODE_ADD_ERRROR_CODES DP12TOPOLOGY_AddDisplay(PDP12_TOPOLOGY pstDP12Topology, PBRANCH_NODE pstTargetBranchNode, PDISPLAY_NODE pstDisplayNode, UCHAR ucTargetBranchOutPort,
                                              UCHAR ucNewDisplayInputPort)
{
    NODE_ADD_ERRROR_CODES eRet = eGENERIC_ERROR;

    do
    {
        if (!pstTargetBranchNode)
        {
            break;
        }

        if (ucTargetBranchOutPort < pstTargetBranchNode->ucTotalInputPorts)
        {
            eRet = eINVALID_OUTPUT_PORT;
            break;
        }

        if (ucNewDisplayInputPort >= pstDisplayNode->ucTotalInputPorts)
        {
            eRet = eINVALID_INPUT_PORT;
            break;
        }

        if (ucTargetBranchOutPort <= MAX_PHYSICAL_OUT_PORTS)
        {
            if (pstTargetBranchNode->ucAvailablePhysicalPorts)
            {
                pstTargetBranchNode->ucAvailablePhysicalPorts--;
            }
            else
            {
                eRet = eNO_FREE_PORT_AVAILABLE;
                break;
            }
        }
        else
        {
            if (pstTargetBranchNode->ucAvailableVirtualPorts)
            {
                pstTargetBranchNode->ucAvailableVirtualPorts--;
            }
            else
            {
                eRet = eNO_FREE_PORT_AVAILABLE;
                break;
            }
        }

        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].bPortConnectedStatus         = TRUE;
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].bConnectedDeviceMsgCapStatus = FALSE; // Since we are adding a Sink/Display
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].eConnectedDeviceNodeType     = pstDisplayNode->eNodeType;
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].stConnectedDevicePeerType    = pstDisplayNode->ePeerDeviceType;
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].ucConnectedDevicePortNumber  = ucNewDisplayInputPort;
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].ucOutPortNumber              = ucTargetBranchOutPort;
        pstTargetBranchNode->stOutPortList[ucTargetBranchOutPort].pvConnectedDeviceNodePointer = pstDisplayNode;

        pstDisplayNode->stInportList[ucNewDisplayInputPort].bPortConnectedStatus     = TRUE;
        pstDisplayNode->stInportList[ucNewDisplayInputPort].eUpStreamNodeType        = pstTargetBranchNode->eNodeType;
        pstDisplayNode->stInportList[ucNewDisplayInputPort].stUpStreamDevicePeerType = pstTargetBranchNode->ePeerDeviceType;
        pstDisplayNode->stInportList[ucNewDisplayInputPort].ucUpStreamPortNumber     = ucTargetBranchOutPort;
        pstDisplayNode->stInportList[ucNewDisplayInputPort].ucInputPortNumber        = ucNewDisplayInputPort;
        pstDisplayNode->stInportList[ucNewDisplayInputPort].pvUpStreamNodePointer    = pstTargetBranchNode;
        pstDisplayNode->ucFECPathInfo                                                = pstTargetBranchNode->ucFECPathInfo & pstDisplayNode->ucFECPathInfo;

        DP12TOPOLOGY_CreateRad(&pstTargetBranchNode->stBranchRAD, &pstDisplayNode->stDisplayRAD, ucTargetBranchOutPort);

        pstDP12Topology->ulTotalNumDisplays++;

        eRet = eNODE_ADD_SUCCESS;

    } while (FALSE);

    return eRet;
}

void DP12TOPOLOGY_CreateRad(PMST_RELATIVEADDRESS pucUpStreamRAD, PMST_RELATIVEADDRESS pucNewRad, UCHAR ucUpStreamPortNumber)
{
    USHORT        usNumRadBytes = 0;
    PMST_RAD_BYTE pstRadByte    = NULL;
    do
    {
        if (pucUpStreamRAD == NULL || pucNewRad == NULL || ucUpStreamPortNumber >= MAX_PORTS_PER_BRANCH)
        {
            break;
        }

        usNumRadBytes = (pucUpStreamRAD->ucTotalLinkCount / 2);

        if (usNumRadBytes)
        {
            memcpy_s(&pucNewRad->ucAddress, usNumRadBytes, &pucUpStreamRAD->ucAddress, usNumRadBytes);
        }

        pucNewRad->ucTotalLinkCount = pucUpStreamRAD->ucTotalLinkCount + 1;

        // So this remaining field has been intialized here to total link count - 1
        // This intialization is specific to this MST framework implementation
        // When the App world queries the topology RADs and uses them for CSN generation, etc,
        // SIDEBANDUTIL_DecRemainingLinkCountAndAdjustRAD will be used in that CSN generation handling.
        // SIDEBANDUTIL_DecRemainingLinkCountAndAdjustRAD will make use of this remaining field to find
        // out the nodes, port num, etc for which CSN has to be generated using this link count remaining field
        pucNewRad->ucRemainingLinkCount = pucUpStreamRAD->ucTotalLinkCount;

        usNumRadBytes = pucNewRad->ucTotalLinkCount / 2;
        pstRadByte    = (PMST_RAD_BYTE)&pucNewRad->ucAddress[usNumRadBytes - 1];

        // Pay heed that in the below line we are using using pucUpStreamRAD total link count to find even or odd
        // If we use newRad's link count then HigherRad and LowerRad will swap places in the below condition
        if (pucUpStreamRAD->ucTotalLinkCount & 0x1)
        {
            pstRadByte->RadNibbles.HigherRAD = ucUpStreamPortNumber;
        }
        else
        {
            pstRadByte->RadNibbles.LowerRAD = ucUpStreamPortNumber;
        }

        pucNewRad->ucRadSize = pucNewRad->ucTotalLinkCount / 2;

    } while (FALSE);
}

// Two Ways to 2 do LINK_ADDRESS in this Software Simulation
// 1. Just parse through the RAD and reach the valid target branch Node and Pass that BranchNode to the Routine to Create a Reply Message
// 2. Pass every node decribed by the RAD to the Reply Creating routine. The routine would inspect if the passed node is target node or not
// If not it would just adjust the LINK Count and RAD nibble as per spec and return something like DID_NOT_PROCESS
// 2nd Approach is closer to how hardware does it if not the same
PORTABLE_THREAD_ROUTINE_SIGNATURE(DP12TOPOLOGY_DownRequestHandlerThread, lpThreadParameter)
{
    BOOLEAN           bRet                   = FALSE;
    PBRANCH_NODE      pstBranchNode          = (PBRANCH_NODE)lpThreadParameter;
    PBRANCH_NODE      pstDwnStreamBranchNode = NULL;
    PPORTINGLAYER_OBJ pstPortingObj          = GetPortingObj();
    PDP_EVENT         pDPEventArray[3]       = { 0 };
    ULONG             ulGeneratedEventIndex  = 0xFF;

    PROCESSING_RESULT eProcessingResult = ePROCESSING_ERROR;

    PMST_DWNREQUEST_BUFF_INFO pstCurrNodeBuffInfo = NULL;

    UCHAR ucPortNo    = DP_PORT_NA;
    UCHAR ucCurrReqID = 0xFF;

    pDPEventArray[0] = &pstBranchNode->stDownRequestBuffInfo[0].stBuffEvent;
    pDPEventArray[1] = &pstBranchNode->stDownRequestBuffInfo[1].stBuffEvent;
    pDPEventArray[2] = &pstBranchNode->stDownRequestHandlerThreadKillEvent;

    PMST_NAK_REPLY_INFO pstNakInfoEntry = NULL;
    MST_REASON_FOR_NAK  eReasonForNak   = eMST_INVALID;

    while (1)
    {
        ulGeneratedEventIndex = pstPortingObj->pfnDPWaitForMultipleEvents(pDPEventArray, 3, FALSE, NULL);

        if (ulGeneratedEventIndex == 2)
        {
            pstPortingObj->pfnTermninateThread();
        }

        eProcessingResult   = ePROCESSING_ERROR;
        pstCurrNodeBuffInfo = &pstBranchNode->stDownRequestBuffInfo[ulGeneratedEventIndex];

        do
        {
            if (pstCurrNodeBuffInfo == NULL || pstCurrNodeBuffInfo->puchBuffPtr == NULL)
            {
                // ASSERT
                break;
            }

            // First Byte of Any message is RequestID
            pstCurrNodeBuffInfo->ucCurrRequestID = *pstCurrNodeBuffInfo->puchBuffPtr;

            pstNakInfoEntry = (PMST_NAK_REPLY_INFO)pstPortingObj->pfnGetEntryFromLookAsideList(&pstBranchNode->NakInfoLookAsideListHead);

            if (pstNakInfoEntry == NULL)
            {
                // ASSERT
                // Lookaside exhausted!
                break;
            }

            pstNakInfoEntry->bIsNak      = FALSE;
            pstNakInfoEntry->ucRequestID = pstCurrNodeBuffInfo->ucCurrRequestID;
            pstNakInfoEntry->pGuid       = &pstBranchNode->uidBranchGUID;
            pstNakInfoEntry->eReason     = eMST_INVALID;

            ucCurrReqID = pstCurrNodeBuffInfo->ucCurrRequestID;

            switch (ucCurrReqID)
            {
            case eMST_GET_MESSAGE_TRANSACTION_VERSION:

                eReasonForNak = eMST_DEFER;
                // THIS HAS TO BE PROPERLY IMPLEMENTED. RIGHT NOW THE FIRST BRANCH IS HANDLING IRRESPECTIVE OF THE RAD
                // eProcessingResult = DP12TOPOLOGY_MsgTransactionVersionThread(pstDP12Topology);
                break;

            case eMST_CLEAR_PAYLOAD_ID_TABLE:
                eProcessingResult = SIDEBANDMESSAGE_ClearPayloadIDDownRequestHandler(pstBranchNode, pstCurrNodeBuffInfo, &eReasonForNak);
                break;

            case eMST_LINK_ADDRESS:
                eProcessingResult = SIDEBANDMESSAGE_LinkAddressDownRequestHandler(pstBranchNode, pstCurrNodeBuffInfo, &eReasonForNak);
                break;

            case eMST_POWER_UP_PHY:
                eProcessingResult = SIDEBANDMESSAGE_PowerUpPhyDownRequestHandler(pstBranchNode, pstCurrNodeBuffInfo, &eReasonForNak);
                break;

            case eMST_ENUM_PATH_RESOURCES:
                eProcessingResult = SIDEBANDMESSAGE_EnumPathResourcesDownRequestHandler(pstBranchNode, pstCurrNodeBuffInfo, &eReasonForNak);
                break;

            case eMST_ALLOCATE_PAYLOAD:
                eProcessingResult = SIDEBANDMESSAGE_AllocatePayloadDownRequestHandler(pstBranchNode, pstCurrNodeBuffInfo, &eReasonForNak);
                break;

            case eMST_REMOTE_DPCD_READ:
            case eMST_REMOTE_DPCD_WRITE:
            case eMST_REMOTE_I2C_READ:
            case eMST_REMOTE_I2C_WRITE:
                eProcessingResult = SIDEBANDMESSAGE_SinkDirectedMsgsPreHandler(pstBranchNode, pstCurrNodeBuffInfo, &eReasonForNak);
                break;

            default:
                // Unknown Msg type. Return sideband NACK
                break;
            }

            if (eProcessingResult == ePROCESSED)
            {
                pstPortingObj->pfnReturnEntryToLookAsideList(&pstBranchNode->NakInfoLookAsideListHead, &pstNakInfoEntry->DPListEntry);
                pstPortingObj->pfnSetDPEvent(pstBranchNode->pstThisNodeACKReplyEvent[ulGeneratedEventIndex], PRIORITY_NO_INCREMENT);
                break;
            }

            if (eProcessingResult == ePARTIALLY_PROCESSED)
            {
                // Right now ePARTIALLY_PROCESSED is being used for ClearPayload only. ClearPayload internally sends
                // a bunch of AllocatePayload internally per enabled stream coming from that Node's Rx
                pstPortingObj->pfnReturnEntryToLookAsideList(&pstBranchNode->NakInfoLookAsideListHead, &pstNakInfoEntry->DPListEntry);
                break;
            }

            if (eProcessingResult == ePROCESSING_ERROR)
            {
                // Ideally this should only get hit if we don't handle a particular Sideband Message
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eReasonForNak;
                break;
            }

            // Did Not Process Case
            ucPortNo = SIDEBANDUTIL_DecRemainingLinkCountAndAdjustRAD(&pstCurrNodeBuffInfo->stHeaderInfo.stCurrentHeaderRAD);

            if (pstBranchNode->stOutPortList[ucPortNo].bPortConnectedStatus == FALSE)
            {
                // Wrong RAD by the Source. Port available but nothing connected on it
                eProcessingResult        = ePROCESSING_ERROR;
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_INVALID_RAD;
                break;
            }

            if (pstBranchNode->stOutPortList[ucPortNo].eConnectedDeviceNodeType != eBRANCH)
            {
                // Wrong RAD by the Source. Source probably gave an input port by mistake
                eProcessingResult        = ePROCESSING_ERROR;
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_INVALID_RAD;
                break;
            }

            pstDwnStreamBranchNode = (PBRANCH_NODE)pstBranchNode->stOutPortList[ucPortNo].pvConnectedDeviceNodePointer;

            // The below comparison will work because both PBRANCH_NODE and DISPLAY_NODE has their first member as eNodeType
            // The below failure means Source directed a LINK_ADDRESS or EPR or similar messages that are supposed to be handled
            // by the upstream branch to the targetted end SINK
            if (pstDwnStreamBranchNode == NULL || pstDwnStreamBranchNode->eNodeType == eDISPLAY)
            {
                // This should never get hit. If it does something is major league wrong
                eProcessingResult        = ePROCESSING_ERROR;
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_INVALID_RAD;
                break;
            }

        } while (FALSE);

        if (eProcessingResult == eDID_NOT_PROCESS && pstDwnStreamBranchNode)
        {
            // First do any Message specific pre-processing on the downstream node if needed like updating certain
            // DPCDs before forwarding the message
            bRet = TRUE;

            switch (ucCurrReqID)
            {
            case eMST_GET_MESSAGE_TRANSACTION_VERSION:
                eReasonForNak = eMST_DEFER;
                break;

            case eMST_LINK_ADDRESS:
                break;

            case eMST_ENUM_PATH_RESOURCES:
                break;

            case eMST_ALLOCATE_PAYLOAD:

                // This stFullRADFromSrc will be used in Clearpayload to Pass AllocatePayload Msg to downstream Nodes with PBN Zero
                // This is in accordance with the Spec
                // pstBranchNode->stCurrentALlocPayloadData.pstCurrPayloadTableEntry->stFullRADFromSrc = pstCurrNodeBuffInfo->stHeaderInfo.stCurrentHeaderRAD;
                if (pstBranchNode->stOutPortList[ucPortNo].bPostUpdateDownStreamTable == FALSE)
                {
                    bRet                     = DP12TOPOLOGY_UpdateDownStreamBranchVCPayloadTable(pstBranchNode, ucPortNo);
                    pstNakInfoEntry->eReason = eMST_ALLOCATE_FAIL;
                    pstNakInfoEntry->bIsNak  = !bRet;
                }
                break;

            case eMST_REMOTE_DPCD_READ:
            case eMST_REMOTE_DPCD_WRITE:
            case eMST_REMOTE_I2C_READ:
            case eMST_REMOTE_I2C_WRITE:
                break;

            default:
                // Unknown Msg type. Return sideband NACK
                break;
            }

            if (bRet)
            {
                PMST_DWNREQUEST_BUFF_INFO pstDwnStreamBuffInfo = NULL;
                ULONG                     ulTotalBodyMsgSize   = pstCurrNodeBuffInfo->stHeaderInfo.ulTotalBodySize;
                pstDwnStreamBuffInfo                           = pstDwnStreamBranchNode->pfnGetAvailableDownReqBuff(pstDwnStreamBranchNode);
                pstDwnStreamBuffInfo->stHeaderInfo             = pstCurrNodeBuffInfo->stHeaderInfo;
                memcpy_s(pstDwnStreamBuffInfo->puchBuffPtr, ulTotalBodyMsgSize, pstCurrNodeBuffInfo->puchBuffPtr, ulTotalBodyMsgSize);

                // Since we have forwareded this request to the downstream node so we can return this buffer of the current node
                // to its free downrequest buffer pool
                pstBranchNode->pfnSetDownReqBuffState(pstBranchNode, ulGeneratedEventIndex, eReturnToFreePool);

                // There was no NAK, return the Nak Entry back to lookaside list
                pstPortingObj->pfnReturnEntryToLookAsideList(&pstBranchNode->NakInfoLookAsideListHead, &pstNakInfoEntry->DPListEntry);

                // Set the downstream node event to unblock its down request processing handler and make it handle this request
                pstPortingObj->pfnSetDPEvent(&pstDwnStreamBuffInfo->stBuffEvent, PRIORITY_NO_INCREMENT);
            }
        }

        if (pstNakInfoEntry->bIsNak)
        {
            // Since we are returning NAK for this request so we can return the current down request buffer to the free pool
            pstBranchNode->pfnSetDownReqBuffState(pstBranchNode, ulGeneratedEventIndex, eReturnToFreePool);
            pstPortingObj->pfnInterlockedInsertTailList(&pstBranchNode->NakInfoProcessingListHead, &pstNakInfoEntry->DPListEntry);
            pstPortingObj->pfnSetDPEvent(pstBranchNode->pstThisNodeNAKReplyEvent, PRIORITY_NO_INCREMENT);
        }
    }
}

PORTABLE_THREAD_ROUTINE_SIGNATURE(DP12TOPOLOGY_DownReplyHandlerThread, lpThreadParameter)
{
    PBRANCH_NODE pstBranchNode = (PBRANCH_NODE)lpThreadParameter;

    PUCHAR pucPortEventMappingList = pstBranchNode->stDownStreamPortEvents.ucPortMappingList;

    ULONG             ulCount                 = 0;
    UCHAR             ucGeneratedEventPortNum = 0;
    ULONG             ulSingnaledEventIndex   = 0;
    PPORTINGLAYER_OBJ pstPortingObj           = GetPortingObj();

    PDP_EVENT *ppDPEventArray = pstPortingObj->pfnAllocateMem((MAX_NON_DOWNPORTS_EVENTS + MAX_PORTS_PER_BRANCH) * sizeof(PDP_EVENT), TRUE);

    for (ulCount = 0; ulCount < (MAX_NON_DOWNPORTS_EVENTS + MAX_PORTS_PER_BRANCH); ulCount++)
    {
        ppDPEventArray[ulCount] = &pstBranchNode->stDownStreamPortEvents.stDownReplyEventList[ulCount];
    }

    while (1)
    {

        ulSingnaledEventIndex = pstPortingObj->pfnDPWaitForMultipleEvents(ppDPEventArray, (MAX_NON_DOWNPORTS_EVENTS + MAX_PORTS_PER_BRANCH), FALSE, NULL);

        if (pucPortEventMappingList[ulSingnaledEventIndex] == DP_PORT_NA)
        {
            // This branch itself has either NAK or a valid response because if was the SBM target Node

            if (ulSingnaledEventIndex == INDEX_BUFF_1 || ulSingnaledEventIndex == INDEX_BUFF_2)
            {
                DP12TOPOLOGY_SendACKReply(pstBranchNode, ulSingnaledEventIndex);
            }
            else if (ulSingnaledEventIndex == NAK_REPLY_READY_INDEX)
            {
                DP12TOPOLOGY_SendNAKReply(pstBranchNode);
            }
            else if (ulSingnaledEventIndex == THREAD_KILL_EVENT_INDEX)
            {
                if (ppDPEventArray)
                {
                    pstPortingObj->pfnFreeMem(ppDPEventArray);
                }

                pstPortingObj->pfnTermninateThread();
            }
        }
        else
        {
            ucGeneratedEventPortNum = pucPortEventMappingList[ulSingnaledEventIndex];
            DP12TOPOLOGY_PostProcessAndFowardDownStreamsReply(pstBranchNode, ucGeneratedEventPortNum);
        }
    }
}
PORTABLE_THREAD_ROUTINE_SIGNATURE(DP12TOPOLOGY_UpRequestHandlerThread, lpThreadParameter)
{
    PBRANCH_NODE pstBranchConnectedToSrc = (PBRANCH_NODE)lpThreadParameter;
    PDP_EVENT    pDPEventArray[2]        = { 0 };
    ULONG        ulGeneratedEventIndex   = 0;

    ULONG  ulCount        = 0;
    ULONG  ulTemp         = 0;
    PUCHAR pucDestination = NULL;
    PUCHAR pucSource      = NULL;

    DPCDDEF_SPI_IRQ_VECTOR stSPIIRQEvents = { 0 };
    PPORTINGLAYER_OBJ      pstPortingObj  = GetPortingObj();

    pDPEventArray[0] = &pstBranchConnectedToSrc->stUpRequestEvent;
    pDPEventArray[1] = &pstBranchConnectedToSrc->stUpRequestHandlerThreadKillEvent;

    while (1)
    {
        ulGeneratedEventIndex = pstPortingObj->pfnDPWaitForMultipleEvents(pDPEventArray, 2, FALSE, NULL);

        PUPREQUEST_NODE_ENTRY pstUpReqNodeEntry = NULL;

        if (ulGeneratedEventIndex == 1)
        {
            pstPortingObj->pfnTermninateThread();
        }

        if (pstBranchConnectedToSrc->stUpRequestBuffInfo.ulTotalUpReqSize)
        {
            ulTemp = CEIL_DIVIDE(pstBranchConnectedToSrc->stUpRequestBuffInfo.ulTotalUpReqSize, MST_MAX_SBM_CHUNK_SIZE);

            while (ulCount != ulTemp)
            {
                pucDestination = pstBranchConnectedToSrc->stUpRequestBuffInfo.puchUpReqBuffPtr + ulCount * MST_MAX_SBM_CHUNK_SIZE;
                ulCount++;
                pucSource = pstBranchConnectedToSrc->stUpRequestBuffInfo.puchUpReqBuffPtr + ulCount * MST_MAX_SBM_CHUNK_SIZE;
                memcpy_s(pucDestination, MST_MAX_SBM_CHUNK_SIZE, pucSource, MST_MAX_SBM_CHUNK_SIZE);

                // Read-Modify-Write IRQ Vector inside spin lock
                pstPortingObj->pfnAcquireDPLock(&pstBranchConnectedToSrc->stServiceIRQVectorSpinLock);
                stSPIIRQEvents.ucVal = pstBranchConnectedToSrc->stBranchDPCDMap.pucDPCDBuff[DPCD_SERVICE_IRQ_VECTOR];
                if (stSPIIRQEvents.IRQVectorBits.bUpRequestMsgRdy == FALSE)
                {
                    stSPIIRQEvents.IRQVectorBits.bUpRequestMsgRdy                                 = TRUE;
                    pstBranchConnectedToSrc->stBranchDPCDMap.pucDPCDBuff[DPCD_SERVICE_IRQ_VECTOR] = stSPIIRQEvents.ucVal;
                }
                pstPortingObj->pfnReleaseDPLock(&pstBranchConnectedToSrc->stServiceIRQVectorSpinLock);
            }
        }
        else
        {
            pstUpReqNodeEntry = (PUPREQUEST_NODE_ENTRY)pstPortingObj->pfnInterlockedRemoveHeadList(&pstBranchConnectedToSrc->stUpRequestListHead);

            if (pstUpReqNodeEntry)
            {

                memcpy_s(pstBranchConnectedToSrc->stUpRequestBuffInfo.puchUpReqBuffPtr, pstUpReqNodeEntry->ulUpRequestSize, &pstUpReqNodeEntry->stCSNRequestData,
                         pstUpReqNodeEntry->ulUpRequestSize);

                pstBranchConnectedToSrc->stUpRequestBuffInfo.ucRequestID      = pstUpReqNodeEntry->ucRequestID;
                pstBranchConnectedToSrc->stUpRequestBuffInfo.ulTotalUpReqSize = SIDEBANDMESSAGE_PacketizeInto48ByteChunks(
                pstBranchConnectedToSrc->stUpRequestBuffInfo.puchUpReqBuffPtr, pstUpReqNodeEntry->ulUpRequestSize, &pstBranchConnectedToSrc->stBranchRAD, FALSE, FALSE, 0);

                pstPortingObj->pfnAcquireDPLock(&pstBranchConnectedToSrc->stServiceIRQVectorSpinLock);
                stSPIIRQEvents.ucVal = pstBranchConnectedToSrc->stBranchDPCDMap.pucDPCDBuff[DPCD_SERVICE_IRQ_VECTOR];
                if (stSPIIRQEvents.IRQVectorBits.bUpRequestMsgRdy == FALSE)
                {
                    stSPIIRQEvents.IRQVectorBits.bUpRequestMsgRdy                                 = TRUE;
                    pstBranchConnectedToSrc->stBranchDPCDMap.pucDPCDBuff[DPCD_SERVICE_IRQ_VECTOR] = stSPIIRQEvents.ucVal;
                }
                pstPortingObj->pfnReleaseDPLock(&pstBranchConnectedToSrc->stServiceIRQVectorSpinLock);

                // Generate SPI
                EXTERNALCALLBACKS_GenerateSPI(pstUpReqNodeEntry->pstGfxAdapterInfo, pstUpReqNodeEntry->ulPortNum);

                // Destroy the pstUpReqNodeEntry
                pstPortingObj->pfnFreeMem(pstUpReqNodeEntry);
            }
        }
    }
}

BOOLEAN DP12TOPOLOGY_UpRequestHandler(PDP12_TOPOLOGY pstDP12Topology, PUP_REQUEST_ARGS pstUpRequestArgs)
{
    BOOLEAN               bRet              = FALSE;
    PUPREQUEST_NODE_ENTRY pstUpReqNodeEntry = NULL;

    PBRANCH_NODE pstBranchConnectedToSrc = pstDP12Topology->pstBranchConnectedToSrc;

    RAD_NODE_INFO     stRADNodeInfo = { 0 };
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    do
    {
        if (pstDP12Topology == NULL || pstUpRequestArgs == NULL)
        {
            break;
        }

        stRADNodeInfo = DP12TOPOLOGY_GetNodeForAGivenRAD(pstDP12Topology, &pstUpRequestArgs->stRAD);

        GFXVALSIM_DBG_MSG("UpRequest Handler Request ID %d", pstUpRequestArgs->eUpRequestID);

        switch (pstUpRequestArgs->eUpRequestID)
        {
        case eMST_CONNECTION_STATUS_NOTIFY:

            if (DP12TOPOLOGY_AddOrDeleteSubTopology(pstDP12Topology, pstUpRequestArgs->stCSNArgs.bAttachOrDetatch, FALSE,
                                                    // Detach Parameters:
                                                    stRADNodeInfo.pvRADNode,
                                                    // Attach Parameters:
                                                    stRADNodeInfo.pstBranchNode, pstUpRequestArgs->stCSNArgs.pvNewNodeToBeAdded, stRADNodeInfo.ucPortNum,
                                                    pstUpRequestArgs->stCSNArgs.ucNewNodeInputPort))
            {
                pstUpReqNodeEntry = SIDEBANDMESSAGE_ConnectionStatusNotifyUpRequestHandler(pstBranchConnectedToSrc, stRADNodeInfo.pstBranchNode, stRADNodeInfo.ucPortNum);
            }

            break;

        case eMST_RESOURCE_STATUS_NOTIFY:
            break;

        default:
            break;
        }

        if (pstUpReqNodeEntry)
        {
            pstUpReqNodeEntry->ucRequestID       = pstUpRequestArgs->eUpRequestID;
            pstUpReqNodeEntry->pstGfxAdapterInfo = pstUpRequestArgs->pstGfxAdapterInfo;
            pstUpReqNodeEntry->ulPortNum         = pstUpRequestArgs->ulPortNum;
            pstPortingObj->pfnInterlockedInsertTailList(&pstBranchConnectedToSrc->stUpRequestListHead, &pstUpReqNodeEntry->ListEntry);
            // Now signal the event to unblock the upstream down reply processing thread
            pstPortingObj->pfnSetDPEvent(&pstBranchConnectedToSrc->stUpRequestEvent, PRIORITY_NO_INCREMENT);

            bRet = TRUE;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN DP12TOPOLOGY_AddOrDeleteSubTopology(
PDP12_TOPOLOGY pstDP12Topology, BOOLEAN bAttachOrDetach,
BOOLEAN bForceAttach, // If we want to force attach the new node even though the branch's outport for a given RAD has already something attached on it
// Detach Parameters:
PVOID pvNodeToBeDeleted,
// Attach Parameters:
PBRANCH_NODE pstTargetBranchNode, PVOID pvNewNodeToBeAdded, UCHAR ucTargetBranchOutPort, UCHAR ucNewBranchInputPort)
{
    BOOLEAN bRet                    = FALSE;
    BOOLEAN bCurrentAttatchedStatus = DP12TOPOLOGY_GetNodePortAttachStatus(pstTargetBranchNode, eBRANCH, ucTargetBranchOutPort);
    do
    {
        // So clean up the existing attached node in 2 cases:
        // 1. Caller requested for a detach and node is not already detached i.e something is indeed attached on the port
        // 2. The caller wants to attach a new node forcefully. Thus we need to cleanup the old node
        if ((bAttachOrDetach == FALSE && TRUE == bCurrentAttatchedStatus) || (bForceAttach == TRUE))
        {
            if (pvNodeToBeDeleted == NULL)
            {
                break;
            }

            if (((PBRANCH_NODE)pvNodeToBeDeleted)->eNodeType == eBRANCH)
            {
                DP12TOPOLOGY_DFSBranchCleanUp(pvNodeToBeDeleted);
                GFXVALSIM_DBG_MSG("DP12Topology Branch CleanUp");
            }
            else
            {
                DP12TOPOLOGY_DisplayNodeCleanUp(pvNodeToBeDeleted);
                GFXVALSIM_DBG_MSG("DP12Topology Display Node CleanUp");
            }
        }

        // In case of forced attached, the clean up would have set the current attached state to FALSE.
        // In a normal attached call, there should not be anything attached on the given port anyways
        if (bAttachOrDetach == TRUE)
        {
            if (pvNewNodeToBeAdded == NULL)
            {
                break;
            }

            if (((PBRANCH_NODE)pvNewNodeToBeAdded)->eNodeType == eBRANCH)
            {
                if (eNODE_ADD_SUCCESS != DP12TOPOLOGY_AddBranch(pstDP12Topology, pstTargetBranchNode, pvNewNodeToBeAdded, ucTargetBranchOutPort, ucNewBranchInputPort, TRUE))
                {
                    GFXVALSIM_DBG_MSG("DP12Topology Add Branch Error");
                    break;
                }
                GFXVALSIM_DBG_MSG("DP12Topology Add Branch");
            }
            else
            {
                if (eNODE_ADD_SUCCESS != DP12TOPOLOGY_AddDisplay(pstDP12Topology, pstTargetBranchNode, pvNewNodeToBeAdded, ucTargetBranchOutPort, ucNewBranchInputPort))
                {
                    GFXVALSIM_DBG_MSG("DP12Topology Add Display Error");
                    break;
                }
                GFXVALSIM_DBG_MSG("DP12Topology Add Display");
            }
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN DP12TOPOLOGY_SendACKReply(PBRANCH_NODE pstBranchNode, ULONG ulDwnReqBuffIndex)
{
    BOOLEAN bRet               = FALSE;
    PUCHAR  ucThisDwnReqBuff   = pstBranchNode->stDownRequestBuffInfo[ulDwnReqBuffIndex].puchBuffPtr;
    ULONG   ulTotalReplySize   = pstBranchNode->stDownRequestBuffInfo[ulDwnReqBuffIndex].ulFinalReplySize;
    PUCHAR  ucThisDwnReplyBuff = pstBranchNode->stDownReplyBuffInfo.puchBuffPtr;
    memcpy_s(ucThisDwnReplyBuff, ulTotalReplySize, ucThisDwnReqBuff, ulTotalReplySize);
    pstBranchNode->stDownReplyBuffInfo.ulTotalReplySize = ulTotalReplySize;

    // We need to set this buff state in with a lock acquired?
    pstBranchNode->pfnSetDownReqBuffState(pstBranchNode, ulDwnReqBuffIndex, eReturnToFreePool);
    bRet = DP12TOPOLOGY_SendDownReply(pstBranchNode);

    return bRet;
}

BOOLEAN DP12TOPOLOGY_SendNAKReply(PBRANCH_NODE pstBranchNode)
{
    BOOLEAN             bRet            = FALSE;
    PPORTINGLAYER_OBJ   pstPortingObj   = GetPortingObj();
    PMST_NAK_REPLY_INFO pstNakInfoEntry = NULL;
    PMST_NAK_REPLY_DATA pstNakReplyData = (PMST_NAK_REPLY_DATA)pstBranchNode->stDownReplyBuffInfo.puchBuffPtr;

    while (!pstPortingObj->pfnIsListEmpty(&pstBranchNode->NakInfoProcessingListHead))
    {
        pstNakInfoEntry = (PMST_NAK_REPLY_INFO)pstPortingObj->pfnInterlockedRemoveHeadList(&pstBranchNode->NakInfoProcessingListHead);

        pstNakReplyData->bReplyType     = 1;                            // 1 is Nak
        pstNakReplyData->ucRequestID    = pstNakInfoEntry->ucRequestID; // TBD Not populating Request ID properly currently
        pstNakReplyData->guid           = *pstNakInfoEntry->pGuid;
        pstNakReplyData->ucReasonForNak = pstNakInfoEntry->eReason;
        pstNakReplyData->ucNAKData      = pstNakInfoEntry->ucNakData;

        // Packetize into 48byte chunks
        // And save the Size of this NAK reply. Upstream branches will copy from this downstream buffer to their own reply buffer using this size
        pstBranchNode->stDownReplyBuffInfo.ulTotalReplySize =
        SIDEBANDMESSAGE_PacketizeInto48ByteChunks((PUCHAR)pstNakReplyData, sizeof(MST_NAK_REPLY_DATA), &pstBranchNode->stBranchRAD, FALSE, FALSE, pstNakInfoEntry->ucSeqNum);

        // Copied the NAK data to down reply buffer. So now return the Nak Entry back to lookaside list
        pstPortingObj->pfnReturnEntryToLookAsideList(&pstBranchNode->NakInfoLookAsideListHead, &pstNakInfoEntry->DPListEntry);

        bRet = DP12TOPOLOGY_SendDownReply(pstBranchNode);
    }

    return bRet;
}

BOOLEAN DP12TOPOLOGY_PostProcessAndFowardDownStreamsReply(PBRANCH_NODE pstBranchNode, UCHAR ucGeneratedEventPortNum)
{
    BOOLEAN                bRet                    = TRUE;
    PROCESSING_RESULT      eProcessingResult       = ePROCESSED;
    PMST_REPLY_DATA        pstMSTReplyData         = NULL;
    PPORTINGLAYER_OBJ      pstPortingObj           = GetPortingObj();
    DPCDDEF_SPI_IRQ_VECTOR stSPIIRQVector          = { 0 };
    UCHAR                  ucCurrentHeaderSize     = 0;
    BOOLEAN                bSeqNo                  = 0;
    PBRANCH_NODE           pstDownStreamBranchNode = pstBranchNode->stOutPortList[ucGeneratedEventPortNum].pvConnectedDeviceNodePointer;

    PUCHAR pucThisReplyBuff      = pstBranchNode->stDownReplyBuffInfo.puchBuffPtr;
    PUCHAR pucDwnStreamReplyBuff = pstDownStreamBranchNode->stDownReplyBuffInfo.puchBuffPtr;

    ULONG ulTotalReplySize = pstDownStreamBranchNode->stDownReplyBuffInfo.ulTotalReplySize;

    PUCHAR pucDPCDMap = pstDownStreamBranchNode->stBranchDPCDMap.pucDPCDBuff;

    // Read-Modify-Write IRQ Vector Within Spin Lock
    // Spin Lock Acquire
    pstPortingObj->pfnAcquireDPLock(&pstDownStreamBranchNode->stServiceIRQVectorSpinLock);

    stSPIIRQVector.ucVal = pucDPCDMap[DPCD_SERVICE_IRQ_VECTOR];

    // Copy the downstream buffer only if the downstream device has set the DownReply Bit
    if (stSPIIRQVector.IRQVectorBits.bDownReplyMsgRdy)
    {
        memcpy_s(pucThisReplyBuff, ulTotalReplySize, pucDwnStreamReplyBuff, ulTotalReplySize);
        pstBranchNode->stDownReplyBuffInfo.ulTotalReplySize = ulTotalReplySize;

        // Tell the downstream device we have read all its data by setting its total reply size to zero
        pstDownStreamBranchNode->stDownReplyBuffInfo.ulTotalReplySize -= ulTotalReplySize;

        // Now clear the downstream device's DownReplyReady bit
        stSPIIRQVector.IRQVectorBits.bDownReplyMsgRdy = 0;
        pucDPCDMap[DPCD_SERVICE_IRQ_VECTOR]           = stSPIIRQVector.ucVal;

        // Spin Lock Release
        pstPortingObj->pfnReleaseDPLock(&pstDownStreamBranchNode->stServiceIRQVectorSpinLock);

        // Now signal the event to unblock the downstream thread waiting for the reply to be read
        pstPortingObj->pfnSetDPEvent(&pstDownStreamBranchNode->stUpReadDownReplyEvent, PRIORITY_NO_INCREMENT);

        // Get the header size
        // Ideally we need to find the body size too to figure out if the reply is distributed over multiple
        // 48bytes chunks and modify it accordingly by the upstream node if needed depending on the sideband band message type

        bRet = SIDEBANDUTIL_DecodeSidebandHeader(pucThisReplyBuff, &ucCurrentHeaderSize, NULL, NULL, NULL, NULL, NULL, NULL, NULL, &bSeqNo, NULL);

        //++ because first Byte is Ack Bit plus 7 bits of Request ID
        // Can't use the whole Char because in case of Nak pstMSTReplyData stMSTReplyData->bReplyType = 1
        // So *(pstMSTReplyData) != pstMSTReplyData->ucRequestID as in case where there's an ACK reply because for ACK Reply stMSTReplyData->bReplyType = 0
        // So value in 7bits (8th bit is zero for ACK)  = Value in 8 bits

        pstMSTReplyData = (PMST_REPLY_DATA)(pucThisReplyBuff + ucCurrentHeaderSize);

        if (pstMSTReplyData->bReplyType == 0) // ACK
        {
            switch (pstMSTReplyData->ucRequestID)
            {
            case eMST_GET_MESSAGE_TRANSACTION_VERSION:
                break;

            case eMST_LINK_ADDRESS:
                break;

            case eMST_POWER_UP_PHY:
                eProcessingResult = SIDEBANDMESSAGE_PowerUpPhyDownReplyHandler(pstBranchNode, pucThisReplyBuff, ucCurrentHeaderSize);
                break;

            case eMST_ENUM_PATH_RESOURCES:
                eProcessingResult = SIDEBANDMESSAGE_EnumPathResourcesDownReplyHandler(pstBranchNode, pucThisReplyBuff, ucCurrentHeaderSize);
                break;

            case eMST_ALLOCATE_PAYLOAD:
                eProcessingResult = DP12TOPOLOGY_AllocatePayloadDownReplyPostProcess(pstBranchNode, ucGeneratedEventPortNum, bSeqNo);

            case eMST_REMOTE_DPCD_READ:
            case eMST_REMOTE_DPCD_WRITE:
            case eMST_REMOTE_I2C_READ:
            case eMST_REMOTE_I2C_WRITE:
                break;

            default:
                // Unknown Msg type. Return sideband NACK
                break;
            }
        }

        if (eProcessingResult == ePROCESSED)
        {
            DP12TOPOLOGY_SendDownReply(pstBranchNode);
        }
        else if (eProcessingResult == ePARTIALLY_PROCESSED)
        {
            DP12TOPOLOGY_SendNAKReply(pstBranchNode);
        }
    }
    else
    {
        // Spin Lock Release
        pstPortingObj->pfnReleaseDPLock(&pstDownStreamBranchNode->stServiceIRQVectorSpinLock);
    }

    return bRet;
}

BOOLEAN DP12TOPOLOGY_SendDownReply(PBRANCH_NODE pstBranchNode)
{
    BOOLEAN                bRet              = TRUE;
    PUCHAR                 pucDPCDMap        = pstBranchNode->stBranchDPCDMap.pucDPCDBuff;
    DPCDDEF_SPI_IRQ_VECTOR stSPIIRQVector    = { 0 };
    PPORTINGLAYER_OBJ      pstPortingObj     = GetPortingObj();
    PULONG                 pulTotalReplySize = &pstBranchNode->stDownReplyBuffInfo.ulTotalReplySize;
    PUCHAR                 pucThisReplyBuff  = pstBranchNode->stDownReplyBuffInfo.puchBuffPtr;
    ULONG                  ulTemp            = 0;
    ULONG                  ulCount           = 0;
    PUCHAR                 pucSource         = NULL;
    PUCHAR                 pucDestination    = NULL;

    while (1)
    {
        ulCount = 0;

        // Read-Modify-Write IRQ Vector Within Spin Lock
        // Spin Lock Acquire
        pstPortingObj->pfnAcquireDPLock(&pstBranchNode->stServiceIRQVectorSpinLock);
        stSPIIRQVector.ucVal                          = pucDPCDMap[DPCD_SERVICE_IRQ_VECTOR];
        stSPIIRQVector.IRQVectorBits.bDownReplyMsgRdy = 1;
        pucDPCDMap[DPCD_SERVICE_IRQ_VECTOR]           = stSPIIRQVector.ucVal;
        // Spin Lock Release
        pstPortingObj->pfnReleaseDPLock(&pstBranchNode->stServiceIRQVectorSpinLock);

        // Now signal the event to unblock the upstream down reply processing thread
        pstPortingObj->pfnSetDPEvent(pstBranchNode->pstDownReplyReadyEvent, PRIORITY_NO_INCREMENT);

        pstPortingObj->pfnDPWaitForSingleEvent(&pstBranchNode->stUpReadDownReplyEvent, NULL);

        stSPIIRQVector.ucVal = pucDPCDMap[DPCD_SERVICE_IRQ_VECTOR];

        if (stSPIIRQVector.IRQVectorBits.bDownReplyMsgRdy == 1)
        {
            // Assert
            // Upstream set the event but didn't clear the reply ready bit.
            // Something went wrong
            bRet = FALSE;
            break;
        }

        // If the downReplyReady bit is clear it means atleast MST_MAX_SBM_CHUNK_SIZE (48bytes) of data has been read
        // So checking if there's more DownReply data left in the buffer
        // If so, Move the remaining data to the front of the buffer by MST_MAX_SBM_CHUNK_SIZE and signal the client
        // again to read the next SBM chunk
        if (*pulTotalReplySize == 0)
        {
            break;
        }

        ulTemp = CEIL_DIVIDE(*pulTotalReplySize, MST_MAX_SBM_CHUNK_SIZE);

        while (ulCount != ulTemp)
        {
            pucDestination = pucThisReplyBuff + ulCount * MST_MAX_SBM_CHUNK_SIZE;
            ulCount++;
            pucSource = pucThisReplyBuff + ulCount * MST_MAX_SBM_CHUNK_SIZE;
            memcpy_s(pucDestination, MST_MAX_SBM_CHUNK_SIZE, pucSource, MST_MAX_SBM_CHUNK_SIZE);
        }
    }

    return bRet;
}

// eGetFreeBuff Will get the free or current buffer
// eSetAsInUse Will Mark the buffer as in Use
// eReturnToFreePool will return the buffer to free pool once we have processed it
PMST_DWNREQUEST_BUFF_INFO DP12TOPOLOGY_GetAvailableDownReqBuff(PBRANCH_NODE pstBranchNode)
{
    PMST_DWNREQUEST_BUFF_INFO pstTempSidebandBuffInfo = NULL;

    if (pstBranchNode->stDownRequestBuffInfo[0].bIsBuffInUse == FALSE)
    {

        pstTempSidebandBuffInfo = &pstBranchNode->stDownRequestBuffInfo[0];
    }
    else if (pstBranchNode->stDownRequestBuffInfo[1].bIsBuffInUse == FALSE)
    {
        pstTempSidebandBuffInfo = &pstBranchNode->stDownRequestBuffInfo[1];
    }

    return pstTempSidebandBuffInfo;
}

void DP12TOPOLOGY_SetDownReqBuffState(PBRANCH_NODE pstBranchNode, ULONG ulThisBuffIndex, DWNREQBUFF_SETSTATE eSetState)
{
    if (eSetState == eReturnToFreePool)
    {
        memset(&pstBranchNode->stDownRequestBuffInfo[ulThisBuffIndex].stHeaderInfo, 0, sizeof(SBM_CURRENT_HEADER_INFO));
        pstBranchNode->stDownRequestBuffInfo[ulThisBuffIndex].ulCurrWriteLength = 0;
        pstBranchNode->stDownRequestBuffInfo[ulThisBuffIndex].ulFinalReplySize  = 0;
    }

    pstBranchNode->stDownRequestBuffInfo[ulThisBuffIndex].bIsBuffInUse = (BOOLEAN)eSetState;

    return;
}

BOOLEAN DP12TOPOLOGY_CheckSeqNumValidity(PBRANCH_NODE pstBranchNode, UCHAR ucSeqNum)
{
    BOOLEAN                   bRet        = TRUE;
    PMST_DWNREQUEST_BUFF_INFO pstBuffInfo = pstBranchNode->stDownRequestBuffInfo;

    if (pstBuffInfo[0].bIsBuffInUse && pstBuffInfo[0].stHeaderInfo.ulSeqNumber == ucSeqNum)
    {
        bRet = FALSE;
    }
    else if (pstBuffInfo[1].bIsBuffInUse && pstBuffInfo[1].stHeaderInfo.ulSeqNumber == ucSeqNum)
    {
        bRet = FALSE;
    }

    return bRet;
}

// Implementation Notes:
// XML pareses and sends all the EDID for all the displays in one we maintain a global copy of these EDIDs in the topology Node
// All the displays in the topology just reference these global copies.
// We can afford to do this because EDID is Read-Only data.
BOOLEAN DP12TOPOLOGY_SetEDIDData(PDP12_TOPOLOGY pstDP12Topology, PUCHAR pucDisplayName, ULONG ulEDIDSize, PUCHAR pucEDIDBuff)
{
    BOOLEAN                 bRet                 = TRUE;
    PMST_DISPLAY_EDID_ARRAY pstMSTEDIDArray      = NULL;
    PDISPLAY_EDID           pstDisplayEDID       = NULL;
    PUCHAR *                ppucTemp256ByteBlock = NULL;
    PPORTINGLAYER_OBJ       pstPortingObj        = GetPortingObj();

    do
    {
        if (!(pstDP12Topology && pucDisplayName && pucEDIDBuff && ulEDIDSize))
        {
            bRet = FALSE;
            break;
        }

        // Expect EDID size to be an integral multiple of SIZE_EDID_BLOCK
        if (ulEDIDSize % SIZE_EDID_BLOCK)
        {
            bRet = FALSE;
            break;
        }

        pstMSTEDIDArray = &pstDP12Topology->stMSTEDIDArray;

        pstDisplayEDID = &pstMSTEDIDArray->stMSTDispEDID[pstMSTEDIDArray->ulNumEDIDTypes];

        strcpy_s((char *)pstDisplayEDID->ucDisplayName, MAX_NODE_NAME_SIZE, (const char *)pucDisplayName);

        // We have decided to keep EDID in blocks of 256 bytes to simply the logic of sending EDID simple when Gfx asks for it
        // via I2C-Aux or Remote I2C sideband Message

        while (ulEDIDSize / (2 * SIZE_EDID_BLOCK))
        {
            ppucTemp256ByteBlock  = &pstDisplayEDID->pucEDIDBlocks[pstDisplayEDID->ulNumEDIDBlocks];
            *ppucTemp256ByteBlock = pstPortingObj->pfnAllocateMem((2 * SIZE_EDID_BLOCK), TRUE);

            if (*ppucTemp256ByteBlock == NULL)
            {
                bRet = FALSE;
                break;
            }

            memcpy_s(*ppucTemp256ByteBlock, 2 * SIZE_EDID_BLOCK, pucEDIDBuff, 2 * SIZE_EDID_BLOCK);
            pucEDIDBuff = pucEDIDBuff + 2 * SIZE_EDID_BLOCK;
            ulEDIDSize  = ulEDIDSize - 2 * SIZE_EDID_BLOCK;
            pstDisplayEDID->ulNumEDIDBlocks++;
        }

        // Now copy the last 128 bytes block if left or if EDID has only 128bytes
        if (ulEDIDSize / SIZE_EDID_BLOCK)
        {
            ppucTemp256ByteBlock  = &pstDisplayEDID->pucEDIDBlocks[pstDisplayEDID->ulNumEDIDBlocks];
            *ppucTemp256ByteBlock = pstPortingObj->pfnAllocateMem((2 * SIZE_EDID_BLOCK), TRUE);
            memcpy_s(*ppucTemp256ByteBlock, SIZE_EDID_BLOCK, pucEDIDBuff, SIZE_EDID_BLOCK);
            pstDisplayEDID->ulNumEDIDBlocks++;
        }

        pstMSTEDIDArray->ulNumEDIDTypes++;

    } while (FALSE);

    return bRet;
}

// Implementation Notes:
// XML pareses and sends all the DPCDs for all the displays and branches in one we maintain a global copy of these DPCDs in the topology Node
// All the displays and Branch nodes will copy from this and maintain a local copy and finally destroy this local copy once the topology is built
// This is different from EDID case because unlike EDID, DPCDs are Read-Write and cane written from Native aux and Remote DPCD
BOOLEAN DP12TOPOLOGY_SetDPCDData(PDP12_TOPOLOGY pstDP12Topology, PUCHAR pucDPCDName, ULONG ulDPCDBuffSize, PUCHAR pucDPCDBuff)
{
    BOOLEAN bRet = FALSE;

    PMST_BRANCHDISP_DPCD_ARRAY pstBranchDispDPCDArr = NULL;
    PBRANCHDISP_DPCD           pstBranchDispDPCD    = NULL;
    PPORTINGLAYER_OBJ          pstPortingObj        = GetPortingObj();

    do
    {
        if (!(pstDP12Topology && pucDPCDName && pucDPCDBuff && ulDPCDBuffSize != 0))
        {
            break;
        }

        pstBranchDispDPCDArr = &pstDP12Topology->stMSTDPCDArray;
        pstBranchDispDPCD    = &pstBranchDispDPCDArr->stMSTBranchDispDPCD[pstBranchDispDPCDArr->ulNumDPCDTypes];

        pstBranchDispDPCD->ulDPCDBuffSize = ulDPCDBuffSize;

        pstBranchDispDPCD->pucDPCDBuff = pstPortingObj->pfnAllocateMem(ulDPCDBuffSize, TRUE);

        if (pstBranchDispDPCD->pucDPCDBuff == NULL)
        {
            break;
        }

        memcpy_s(pstBranchDispDPCD->pucDPCDBuff, ulDPCDBuffSize, pucDPCDBuff, ulDPCDBuffSize);

        strcpy_s((char *)pstBranchDispDPCD->ucDPCDName, MAX_NODE_NAME_SIZE, (const char *)pucDPCDName);

        pstBranchDispDPCDArr->ulNumDPCDTypes++;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

PDISPLAY_EDID DP12TOPOLOGY_GetDisplayEDID(PDP12_TOPOLOGY pstDP12Topology, PUCHAR pucDisplayName)
{
    PUCHAR                  pucTempDisplayName = NULL;
    PDISPLAY_EDID           pstDisplayEDID     = NULL;
    ULONG                   ulCount            = 0;
    PMST_DISPLAY_EDID_ARRAY pstDisplayEDIDArr  = &pstDP12Topology->stMSTEDIDArray;

    do
    {
        if (pstDP12Topology == NULL || pucDisplayName == NULL)
        {
            break;
        }

        for (ulCount = 0; ulCount < pstDisplayEDIDArr->ulNumEDIDTypes; ulCount++)
        {
            pstDisplayEDID = &pstDisplayEDIDArr->stMSTDispEDID[ulCount];

            pucTempDisplayName = pstDisplayEDID->ucDisplayName;

            if (0 == strcmp((char *)pucTempDisplayName, (const char *)pucDisplayName))
            {
                break;
            }
        }

    } while (FALSE);

    return pstDisplayEDID;
}

PBRANCHDISP_DPCD DP12TOPOLOGY_GetNodeDPCD(PDP12_TOPOLOGY pstDP12Topology, PUCHAR pucDPCDName)
{
    PUCHAR                     pucTempDPCDName      = NULL;
    PBRANCHDISP_DPCD           pstBranchDispDCPD    = NULL;
    ULONG                      ulCount              = 0;
    PMST_BRANCHDISP_DPCD_ARRAY pstBranchDispDPCDArr = &pstDP12Topology->stMSTDPCDArray;

    do
    {
        if (pstDP12Topology == NULL || pucDPCDName == NULL)
        {
            break;
        }

        for (ulCount = 0; ulCount < pstBranchDispDPCDArr->ulNumDPCDTypes; ulCount++)
        {
            pstBranchDispDCPD = &pstBranchDispDPCDArr->stMSTBranchDispDPCD[ulCount];

            pucTempDPCDName = pstBranchDispDCPD->ucDPCDName;

            if (0 == strcmp((char *)pucTempDPCDName, (const char *)pucDPCDName))
            {
                break;
            }
        }

    } while (FALSE);

    return pstBranchDispDCPD;
}

// This is a interface called from the APP world and has nothing to do with the RemoteDPCDRead sideband message
BOOLEAN DP12TOPOLOGY_GetRemoteDPCD(PDP12_TOPOLOGY pstDP12Topology, PMST_RELATIVEADDRESS pstRAD, PUCHAR pucReadBuff)
{
    BOOLEAN bRet = TRUE;

    do
    {

    } while (FALSE);

    return bRet;
}

// This is a interface called from the APP world and has nothing to do with the RemoteDPCDWrite sideband message
BOOLEAN DP12TOPOLOGY_SetRemoteDPCD(PDP12_TOPOLOGY pstDP12Topology, PMST_RELATIVEADDRESS pstRAD, PUCHAR pucWriteBuff)
{
    BOOLEAN bRet = TRUE;

    do
    {

    } while (FALSE);

    return bRet;
}

BOOLEAN DP12TOPOLOGY_GetMSTTopologyRADArray(PDP12_TOPOLOGY pstDP12Topology, PBRANCHDISP_RAD_ARRAY pstBranchDispRADArray)
{
    BOOLEAN      bRet                    = FALSE;
    PBRANCH_NODE pstBranchConnectedToSrc = pstDP12Topology->pstBranchConnectedToSrc;

    if (pstBranchConnectedToSrc && pstBranchDispRADArray)
    {
        pstBranchDispRADArray->ulNumBranches = 0;
        pstBranchDispRADArray->ulNumDisplays = 0;

        DP12TOPOLOGY_DFSGetTopologyRAD(pstBranchConnectedToSrc, pstBranchDispRADArray, 0xFFFFFFFF);

        bRet = TRUE;
    }

    return bRet;
}

// Get RAD of all attached Nodes in Depth First Search Manner
void DP12TOPOLOGY_DFSGetTopologyRAD(PBRANCH_NODE pstBranchNode, PBRANCHDISP_RAD_ARRAY pstBranchDispRADArray, ULONG ulParentIndex)
{
    USHORT        usCount        = 0;
    PDISPLAY_NODE pstDisplayNode = NULL;

    do
    {
        if (!pstBranchNode)
        {
            break;
        }
        pstBranchDispRADArray->stBranchRADInfo[pstBranchDispRADArray->ulNumBranches].stNodeRAD           = pstBranchNode->stBranchRAD;
        pstBranchDispRADArray->stBranchRADInfo[pstBranchDispRADArray->ulNumBranches].ulParentBranchIndex = ulParentIndex;
        pstBranchDispRADArray->stBranchRADInfo[pstBranchDispRADArray->ulNumBranches].ulThisNodeIndex     = pstBranchDispRADArray->ulNumBranches;
        pstBranchDispRADArray->ulNumBranches++;

        for (usCount = pstBranchNode->ucTotalInputPorts; usCount < MAX_PORTS_PER_BRANCH; usCount++)
        {

            if (pstBranchNode->stOutPortList[usCount].bPortConnectedStatus)
            {
                if (pstBranchNode->stOutPortList[usCount].eConnectedDeviceNodeType == eDISPLAY)
                {
                    pstDisplayNode = (PDISPLAY_NODE)pstBranchNode->stOutPortList[usCount].pvConnectedDeviceNodePointer;

                    pstBranchDispRADArray->stDisplayRADInfo[pstBranchDispRADArray->ulNumDisplays].stNodeRAD           = pstDisplayNode->stDisplayRAD;
                    pstBranchDispRADArray->stDisplayRADInfo[pstBranchDispRADArray->ulNumDisplays].ulParentBranchIndex = pstBranchDispRADArray->ulNumBranches - 1;
                    pstBranchDispRADArray->stDisplayRADInfo[pstBranchDispRADArray->ulNumDisplays].ulThisNodeIndex     = pstBranchDispRADArray->ulNumDisplays;
                    pstBranchDispRADArray->ulNumDisplays++;
                }
                else if (pstBranchNode->stOutPortList[usCount].eConnectedDeviceNodeType == eBRANCH)
                {
                    DP12TOPOLOGY_DFSGetTopologyRAD(pstBranchNode->stOutPortList[usCount].pvConnectedDeviceNodePointer, pstBranchDispRADArray,
                                                   pstBranchDispRADArray->ulNumBranches - 1);
                }
            }
        }

    } while (FALSE);
}

BOOLEAN DP12TOPOLOGY_ExtractCurrentTopologyInArrayFormat(PDP12_TOPOLOGY pstDP12Topology, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArray)
{
    BOOLEAN      bRet                    = FALSE;
    PBRANCH_NODE pstBranchConnectedToSrc = pstDP12Topology->pstBranchConnectedToSrc;

    if (pstBranchConnectedToSrc && pstBranchDispDataArray)
    {
        pstBranchDispDataArray->uiNumBranches = 0;
        pstBranchDispDataArray->uiNumDisplays = 0;

        GFXVALSIM_DBG_MSG("DP12TOPOLOGY_ExtractCurrentTopologyInArrayFormat Entered");

        DP12TOPOLOGY_DFSExtractCurrentTopologyInArrayFormat(pstBranchConnectedToSrc, pstBranchDispDataArray, 0xFFFFFFFF, 0, 0);

        bRet = TRUE;
    }

    return bRet;
}
// Get RAD of all attached Nodes in Depth First Search Manner
void DP12TOPOLOGY_DFSExtractCurrentTopologyInArrayFormat(PBRANCH_NODE pstBranchNode, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArray, ULONG ulParentIndex,
                                                         UCHAR ucUpstreamDeviceOutPortNumber, UCHAR ucThisDevicePortNumber)
{
    USHORT        usCount        = 0;
    PDISPLAY_NODE pstDisplayNode = NULL;

    do
    {
        if (!pstBranchNode)
        {
            break;
        }

        GFXVALSIM_DBG_MSG("DP12TOPOLOGY_DFSExtractCurrentTopologyInArrayFormat Entered");

        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].uiParentBranchIndex = ulParentIndex;
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].uiThisIndex         = pstBranchDispDataArray->uiNumBranches;

        memcpy_s(pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].ucDPCDName, MAX_STR_SIZE, pstBranchNode->stBranchDPCDMap.ucDPCDName, MAX_STR_SIZE);

        // Any node should have only one input port connected to an upstream device. Atleast for now

        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.ucUpStrmBranchOutPort = ucUpstreamDeviceOutPortNumber;
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.ucThisBranchInputPort = ucThisDevicePortNumber;
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.ucTotalInputPorts     = pstBranchNode->ucTotalInputPorts;
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.ucTotalPhysicalPorts  = pstBranchNode->ucTotalPhysicalPorts;
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.ucTotalVirtualPorts   = pstBranchNode->ucTotalVirtualPorts;
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.ucReserved;
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.usTotalAvailablePBN    = pstBranchNode->usTotalAvailablePBN;
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiMaxLinkRate          = 0; // TBD
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiMaxLaneCount         = 0; // TBD
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiBranchReplyDelay     = 0; // TBD
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiLinkAddressDelay     = 0; // TBD
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiRemoteI2ReadDelay    = 0; // TBD
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiRemoteI2WriteDelay   = 0; // TBD
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiRemoteDPCDReadDelay  = 0; // TBD
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiRemoteDPCDWriteDelay = 0; // TBD
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiEPRDelay             = 0; // TBD
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiAllocatePayloadDelay = 0; // TBD
        pstBranchDispDataArray->stBranchData[pstBranchDispDataArray->uiNumBranches].stBranchNodeDesc.uiClearPayLoadDelay    = 0; // TBD

        pstBranchDispDataArray->uiNumBranches++;

        for (usCount = pstBranchNode->ucTotalInputPorts; usCount < MAX_PORTS_PER_BRANCH; usCount++)
        {
            if (pstBranchNode->stOutPortList[usCount].bPortConnectedStatus)
            {
                if (pstBranchNode->stOutPortList[usCount].eConnectedDeviceNodeType == eDISPLAY)
                {
                    GFXVALSIM_DBG_MSG("DP12TOPOLOGY_DFSExtractCurrentTopologyInArrayFormat Display Case Entered for Count %hu", usCount);
                    pstDisplayNode = (PDISPLAY_NODE)pstBranchNode->stOutPortList[usCount].pvConnectedDeviceNodePointer;

                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].uiParentBranchIndex = pstBranchDispDataArray->uiNumBranches - 1;
                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].uiThisIndex         = pstBranchDispDataArray->uiNumDisplays;
                    memcpy_s(pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].ucDPCDName, MAX_STR_SIZE, pstDisplayNode->stDisplayDPCDMap.ucDPCDName,
                             MAX_STR_SIZE);

                    // Any node should have only one input port connected to an upstream device. Atleast for now

                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.ucUpStrmBranchOutPort =
                    pstBranchNode->stOutPortList[usCount].ucOutPortNumber;
                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.ucThisDisplayInputPort =
                    pstBranchNode->stOutPortList[usCount].ucConnectedDevicePortNumber;

                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.ucTotalInputPorts = pstDisplayNode->ucTotalInputPorts;
                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.ucReserved;
                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.usTotalAvailablePBN    = pstDisplayNode->usTotalAvailablePBN;
                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.uiMaxLinkRate          = 0; // TBD
                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.uiMaxLaneCount         = 0; // TBD
                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.uiRemoteI2ReadDelay    = 0; // TBD
                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.uiRemoteI2WriteDelay   = 0; // TBD
                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.uiRemoteDPCDReadDelay  = 0; // TBD
                    pstBranchDispDataArray->stDisplayData[pstBranchDispDataArray->uiNumDisplays].stDisplayNodeDesc.uiRemoteDPCDWriteDelay = 0; // TBD
                    pstBranchDispDataArray->uiNumDisplays++;
                }
                else if (pstBranchNode->stOutPortList[usCount].eConnectedDeviceNodeType == eBRANCH)
                {
                    GFXVALSIM_DBG_MSG("DP12TOPOLOGY_DFSExtractCurrentTopologyInArrayFormat Branch Case Entered for Count %hu", usCount);
                    DP12TOPOLOGY_DFSExtractCurrentTopologyInArrayFormat(pstBranchNode->stOutPortList[usCount].pvConnectedDeviceNodePointer, pstBranchDispDataArray,
                                                                        pstBranchDispDataArray->uiNumBranches - 1, pstBranchNode->stOutPortList[usCount].ucOutPortNumber,
                                                                        pstBranchNode->stOutPortList[usCount].ucConnectedDevicePortNumber);
                }
            }
        }

    } while (FALSE);
}

// 1. stRADNodeInfo.pstBranchNode  = Node to which the node corresponding to the given RAD is connected
// 2. stRADNodeInfo.pvRADNode  = Node corresponding to the given RAD is connected  (Can be NULL depending on the RAD)
// 3. stRADNodeInfo.ucPortNum = Out Port Number of the Branch to which the node corresponding to the given RAD is connected
RAD_NODE_INFO DP12TOPOLOGY_GetNodeForAGivenRAD(PDP12_TOPOLOGY pstDP12Topology, PMST_RELATIVEADDRESS pstInputRAD)
{
    UCHAR               ucPortNum         = DP_PORT_NA;
    PVOID               pvNode            = pstDP12Topology->pstBranchConnectedToSrc;
    PBRANCH_NODE        pstTempBranchNode = NULL;
    RAD_NODE_INFO       stRADNodeInfo     = { 0 };
    MST_RELATIVEADDRESS stTempRAD         = *pstInputRAD;

    do
    {
        if (pstInputRAD->ucTotalLinkCount == 0)
        {
            break;
        }

        do
        {
            pstTempBranchNode = (PBRANCH_NODE)pvNode;

            if (pstTempBranchNode == NULL)
            {
                break;
            }

            if (pstTempBranchNode->eNodeType == eDISPLAY)
            {
                pvNode = NULL;
                break;
            }

            ucPortNum = SIDEBANDUTIL_DecRemainingLinkCountAndAdjustRAD(&stTempRAD);

            if (ucPortNum == DP_PORT_NA)
            {
                break;
            }

            pvNode = pstTempBranchNode->stOutPortList[ucPortNum].pvConnectedDeviceNodePointer;

        } while (stTempRAD.ucRemainingLinkCount > 0);

        if (pvNode == NULL)
        {
            break;
        }

        // Sanity check: Compare Input RAD and the RAD of the node we found. They must be equal
        if (((PBRANCH_NODE)pvNode)->eNodeType == eBRANCH)
        {
            // Memcmp works because MST_RELATIVE address is packed to 1 byte alignment
            if (memcmp(((PBRANCH_NODE)pvNode)->stBranchRAD.ucAddress, pstInputRAD->ucAddress, sizeof(pstInputRAD->ucAddress)))
            {
                break;
            }
        }
        else
        {
            // Memcmp works because MST_RELATIVE address is packed to 1 byte alignment
            if (memcmp(((PDISPLAY_NODE)pvNode)->stDisplayRAD.ucAddress, pstInputRAD->ucAddress, sizeof(pstInputRAD->ucAddress)))
            {
                break;
            }
        }

    } while (FALSE);

    stRADNodeInfo.pstBranchNode = pstTempBranchNode;
    stRADNodeInfo.pvRADNode     = pvNode;
    stRADNodeInfo.ucPortNum     = ucPortNum;

    return stRADNodeInfo;
}

BOOLEAN DP12TOPOLOGY_GetNodePortAttachStatus(PVOID pvNode, NODE_TYPE eNodeType, UCHAR ucPortNum)
{
    BOOLEAN       bRet           = FALSE;
    PBRANCH_NODE  pstBranchNode  = NULL;
    PDISPLAY_NODE pstDisplayNode = NULL;

    do
    {
        if (pvNode == NULL || ucPortNum >= MAX_PORTS_PER_BRANCH)
        {
            break;
        }

        if (eNodeType == eBRANCH)
        {
            pstBranchNode = (PBRANCH_NODE)pvNode;

            if (ucPortNum < pstBranchNode->ucTotalInputPorts)
            {
                bRet = pstBranchNode->stInportList[ucPortNum].bPortConnectedStatus;
            }
            else
            {
                bRet = pstBranchNode->stOutPortList[ucPortNum].bPortConnectedStatus;
            }
        }
        else
        {
            pstDisplayNode = (PDISPLAY_NODE)pvNode;

            if (ucPortNum < pstBranchNode->ucTotalInputPorts)
            {
                bRet = pstBranchNode->stInportList[ucPortNum].bPortConnectedStatus;
            }
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN DP12TOPOLOGY_UpdateDownStreamBranchVCPayloadTable(PBRANCH_NODE pstUpStreamBranchNode, UCHAR ucDownStreamPortNum)
{
    BOOLEAN      bRet                    = FALSE;
    ULONG        ulCount                 = 0;
    UCHAR        ucSlotData[3]           = { 0 };
    PBRANCH_NODE pstDownStreamBranchNode = (PBRANCH_NODE)pstUpStreamBranchNode->stOutPortList[ucDownStreamPortNum].pvConnectedDeviceNodePointer;
    UCHAR        ucNumMTPSlots           = (UCHAR)(pstUpStreamBranchNode->stOutPortList[ucDownStreamPortNum].usAllocatedPBN / pstUpStreamBranchNode->usDwnStreamPBNPerMTPSlot);

    PPAYLOADTABLE_STATE pstDwnStreamPayloadTableState = &pstDownStreamBranchNode->stBranchPayloadTableState;

    ucSlotData[0] = pstUpStreamBranchNode->stOutPortList[ucDownStreamPortNum].ucStreamID;

    // Lets Initialize the start slot to an unused slot. The below for loop will then reassign the value of an already
    // existing stream, if there is one.
    ucSlotData[1] = pstDwnStreamPayloadTableState->ucTotalNumSlotsInUse + 1;

    for (ulCount = 0; ulCount < pstDwnStreamPayloadTableState->ulNumStreamsSlotsAllocated; ulCount++)
    {
        if (pstDwnStreamPayloadTableState->stPTEntryArray[ulCount].ucStreamID == ucSlotData[0])
        {
            ucSlotData[1] = pstDwnStreamPayloadTableState->stPTEntryArray[ulCount].ucStartSlot;
            break;
        }
    }

    // Num Slots
    ucSlotData[2] = (ucNumMTPSlots * pstUpStreamBranchNode->usDwnStreamPBNPerMTPSlot) < (pstUpStreamBranchNode->stOutPortList[ucDownStreamPortNum].usAllocatedPBN) ?
                    (ucNumMTPSlots + 1) :
                    ucNumMTPSlots;

    bRet = DP12TOPOLOGY_UpdateVCPayloadTable(pstDownStreamBranchNode, ucSlotData, DPCD_VCPAYLOAD_ID, 3);

    if (bRet && ucNumMTPSlots == 0)
    {
        // If we are landing here, it means the allocate payload to the downstream branch freed the PBN
        // as a part of Deleting virtual stream procedureulMaxLinkRate
        pstUpStreamBranchNode->stOutPortList[ucDownStreamPortNum].ucStreamID = VCPLAYLOAD_STREAMID_INVALID;
    }
    return bRet;
}
// Imp: In my implementation, I am taking it to be that a stream is considered when the payload table is updated AND Allocate payload is received for that
// stream ID with non zero PBN, hence in case of new stream addition,  pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated  is incremented
// in AllocatePayloadHandler
// In the stream deletion case, its the opposite pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated  is decremented in
// in DP12TOPOLOGY_UpdateVCPayloadTable, i.e we would consider stream deleted once we ALlocate Payload with zero PBN AND Payloadtable is updated (the stream slots
// are deleted)

// Intel Graphics Driver currently doesn't increase or reduce the PBN dynamically currently
// It deletes the whole existing stream for a resolution X on a daisychained dispaly through disable encoder.
// IGD then applies the new resolution Y by allocating a fresh stream rather than just dynamically changing the number of slots and PBN value.
// The below implementation is a more generic work in accordance with the DP1.2 spec that allows dynamic increase or reduction in the
// number of slots without deleting the whole stream.
BOOLEAN DP12TOPOLOGY_UpdateVCPayloadTable(PBRANCH_NODE pstBranchNode, PUCHAR pucBuffToWriteFrom, ULONG ulAddress, ULONG ulLen)
{
    BOOLEAN           bRet                = TRUE;
    ULONG             ulCount             = 0;
    ULONG             ulSlotCount         = 0;
    PPORTINGLAYER_OBJ pstPortingObj       = GetPortingObj();
    PUCHAR            pucDPCDMap          = pstBranchNode->stBranchDPCDMap.pucDPCDBuff;
    PUCHAR            pucDPCDVCTableStart = pucDPCDMap + DPCD_VCPAYLOAD_TABLE_START;

    // Reset the VC Status DPCD
    pucDPCDMap[DPCD_VCPAYLOAD_UPDATE_STATUS] = 0;

    for (; ulCount < ulLen; ulCount++)
    {
        pucDPCDMap[ulAddress + ulCount] = pucBuffToWriteFrom[ulCount];
    }

    if (ulAddress + ulLen > DPCD_VCPAYLOAD_NUM_SLOTS)
    {
        // Flush the whole actual current DPCD table
        memset(pucDPCDVCTableStart, VCPLAYLOAD_STREAMID_INVALID, VCPAYLOAD_TABLE_SIZE);

        // Delete the whole table case:
        if (pucDPCDMap[DPCD_VCPAYLOAD_ID] == 0 && pucDPCDMap[DPCD_VCPAYLOAD_START_SLOT] == 0 && pucDPCDMap[DPCD_VCPAYLOAD_NUM_SLOTS] == VCPAYLOAD_TABLE_SIZE)
        {
            // Clear the internal structure that maintains active streams state
            memset(&pstBranchNode->stBranchPayloadTableState, sizeof(PAYLOADTABLE_STATE), 0);
        }
        else if (pucDPCDMap[DPCD_VCPAYLOAD_ID] != VCPLAYLOAD_STREAMID_INVALID)
        {
            UCHAR   ucNumStreamSlots              = 0;
            BOOLEAN bNewStream                    = TRUE;
            ULONG   ulAffectedStreamIndex         = 0;
            char    cNumStreamSlotsDiff           = pucDPCDMap[DPCD_VCPAYLOAD_NUM_SLOTS]; // this is signed so can be negative as well
            ULONG   ulNumStreamsOriginallyEnabled = pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated;

            do
            {
                if (pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated == 0 && pucDPCDMap[DPCD_VCPAYLOAD_START_SLOT] != TIMESLOT_START)
                {
                    // ASSERT or WARNING. Start Slot should always be 1 if no streamslots are allocated. This will eventually corrupt the table
                }

                for (ulCount = 0; ulCount < pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated; ulCount++)
                {
                    if (pstBranchNode->stBranchPayloadTableState.stPTEntryArray[ulCount].ucStreamID == pucDPCDMap[DPCD_VCPAYLOAD_ID] &&
                        pstBranchNode->stBranchPayloadTableState.stPTEntryArray[ulCount].ucStartSlot == pucDPCDMap[DPCD_VCPAYLOAD_START_SLOT])
                    {
                        ucNumStreamSlots    = pstBranchNode->stBranchPayloadTableState.stPTEntryArray[ulCount].ucNumOfSlots;
                        cNumStreamSlotsDiff = (char)(pucDPCDMap[DPCD_VCPAYLOAD_NUM_SLOTS] - ucNumStreamSlots);
                        // cNumStreamSlotsDiff can never be 0xFF and result in -1( which would be misleading)
                        // because MAX num slots is 63 and should be taken care by the Source

                        // The newly requested number of slots resulting in total allocated slots exeeding Table Size so abort with error
                        if (pstBranchNode->stBranchPayloadTableState.ucTotalNumSlotsInUse + cNumStreamSlotsDiff > VCPAYLOAD_TABLE_SIZE)
                        {
                            bRet = FALSE;
                            break;
                        }

                        pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated -= !pucDPCDMap[DPCD_VCPAYLOAD_NUM_SLOTS];
                        pstBranchNode->stBranchPayloadTableState.stPTEntryArray[ulCount].ucNumOfSlots = pucDPCDMap[DPCD_VCPAYLOAD_NUM_SLOTS];
                        ulAffectedStreamIndex                                                         = ulCount;
                        bNewStream                                                                    = FALSE;
                        break;
                    }
                }

                // The newly requested number of slots resulting in total allocated slots exeeding Table Size so abort with error
                if (pstBranchNode->stBranchPayloadTableState.ucTotalNumSlotsInUse + cNumStreamSlotsDiff > VCPAYLOAD_TABLE_SIZE)
                {
                    bRet = FALSE;
                    break;
                }

                if (bNewStream)
                {
                    pstBranchNode->stBranchPayloadTableState.stPTEntryArray[pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated].ucStreamID =
                    pucDPCDMap[DPCD_VCPAYLOAD_ID];
                    pstBranchNode->stBranchPayloadTableState.stPTEntryArray[pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated].ucStartSlot =
                    pucDPCDMap[DPCD_VCPAYLOAD_START_SLOT];
                    pstBranchNode->stBranchPayloadTableState.stPTEntryArray[pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated].ucNumOfSlots =
                    pucDPCDMap[DPCD_VCPAYLOAD_NUM_SLOTS];
                    pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated++;
                }
                else
                {
                    // If we are here, it means that the changes were made in an existing stream(i.e no new stream added), so modify the start slot of all
                    // the successive streams as per new slot allocation. Additionally in case of existing stream deleted, shift left all the remaining slots.
                    // we iterate upto ulNumStreamsSlotsAllocated - 1 in the loop below to protect from the array bound execedding due to stPayloadTableEntry[ulCount + 1]
                    //(ulNumStreamsIterator = pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated - 1)
                    for (ulCount = ulAffectedStreamIndex; ulCount < ulNumStreamsOriginallyEnabled - 1; ulCount++)
                    {
                        pstBranchNode->stBranchPayloadTableState.stPTEntryArray[ulCount + 1].ucStartSlot += cNumStreamSlotsDiff;

                        if (pucDPCDMap[DPCD_VCPAYLOAD_NUM_SLOTS] == 0)
                        {
                            pstBranchNode->stBranchPayloadTableState.stPTEntryArray[ulCount] = pstBranchNode->stBranchPayloadTableState.stPTEntryArray[ulCount + 1];
                        }
                    }
                }

                // Now if an entry was deleted, then delete the unused entry in the end to avoid any side effects
                // We can do this because only one entry can be deleted in single call hence only one entry would vaccated towards the end
                if (pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated < ulNumStreamsOriginallyEnabled)
                {
                    pstBranchNode->stBranchPayloadTableState.stPTEntryArray[pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated].ucStreamID =
                    VCPLAYLOAD_STREAMID_INVALID;
                    pstBranchNode->stBranchPayloadTableState.stPTEntryArray[pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated].ucStartSlot  = 0;
                    pstBranchNode->stBranchPayloadTableState.stPTEntryArray[pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated].ucNumOfSlots = 0;
                }

                // Now write the table with the new values/state
                for (ulCount = 0; ulCount < pstBranchNode->stBranchPayloadTableState.ulNumStreamsSlotsAllocated; ulCount++)
                {
                    for (ulSlotCount = 0; ulSlotCount < pstBranchNode->stBranchPayloadTableState.stPTEntryArray[ulCount].ucNumOfSlots; ulSlotCount++)
                    {
                        *pucDPCDVCTableStart++ = pstBranchNode->stBranchPayloadTableState.stPTEntryArray[ulCount].ucStreamID;
                    }
                }

                pstBranchNode->stBranchPayloadTableState.ucTotalNumSlotsInUse += cNumStreamSlotsDiff;

            } while (FALSE);
        }

        // Commenting this code (part of older link training implementation) as pstLTStateData->liLQADelay is not being filled anywhere.
        // So the 'update status with timer delay' part is unused. Can be refactored and enabled later if this functionality is needed.
        //// Do an LQA delay if Asked by the XML
        // if (pstLTStateData && pstLTStateData->liLQADelay.QuadPart)
        //{
        //    TIMER_CB_CONTEXT stTimerCbContext = { 0 };

        //    pstPortingObj->pfnInterLockedIncrement(&pstLTStateData->ulLQAimerScheduledCount);
        //    stTimerCbContext.pulTimerScheduleCount = &pstLTStateData->ulLQAimerScheduledCount;
        //    stTimerCbContext.pvCallBackContext     = pstBranchNode->stBranchDPCDMap.pucDPCDBuff;
        //    // Schedule the Timer to Update the VCPayload Update DPCDs
        //    pstPortingObj->pfnSetDPTimer(&pstLTStateData->stLQADelayTimer, pstLTStateData->liLQADelay, 0, GLOBAL_ENV_TIMER_BIAS, DP12TOPOLOGY_VCPayloadTableUpdateStatusTimerCb,
        //                                 &stTimerCbContext);
        //}

        // 'update status with non-timer' case
        DP12TOPOLOGY_VCPayloadTableUpdateStatusNonTimer(pstBranchNode->stBranchDPCDMap.pucDPCDBuff);
    }

    return bRet;
}

// Not Implementing it in SidebandMessagingHandler.c But here because this function mostly does Non-Sidebandy things and
// calls Routines of DP12TOPOLOGY_ type
PROCESSING_RESULT DP12TOPOLOGY_AllocatePayloadDownReplyPostProcess(PBRANCH_NODE pstBranchNode, UCHAR ucGeneratedEventPortNum, BOOLEAN bSeqNo)
{
    PROCESSING_RESULT eProcessingResult = ePROCESSING_ERROR;
    UCHAR             ucSlotData[3]     = { 0, 0, VCPAYLOAD_TABLE_SIZE };

    do
    {
        if (pstBranchNode->stOutPortList[ucGeneratedEventPortNum].bPostUpdateDownStreamTable)
        {
            if (FALSE == DP12TOPOLOGY_UpdateDownStreamBranchVCPayloadTable(pstBranchNode, ucGeneratedEventPortNum))
            {
                break;
            }

            pstBranchNode->stOutPortList[ucGeneratedEventPortNum].bPostUpdateDownStreamTable = FALSE;
        }

        // Handling for ClearPayload
        if (pstBranchNode->bIsBranchConnectedToSrc && pstBranchNode->bAllocPayloadSentForClearPayload)
        {
            eProcessingResult = SIDEBANDMESSAGE_ClearPayloadIDDownReplyHandler(pstBranchNode, ucGeneratedEventPortNum, bSeqNo);

            if (eProcessingResult != ePROCESSED)
            {
                break;
            }

            // Clear Stream Slot data for this branch

            if (FALSE == DP12TOPOLOGY_UpdateVCPayloadTable(pstBranchNode, ucSlotData, DPCD_VCPAYLOAD_ID, 3))
            {
                break;
            }
        }

        eProcessingResult = ePROCESSED;

    } while (FALSE);

    return eProcessingResult;
}

PORTABLE_TIMER_CALLBACK_SIGNATURE(DP12TOPOLOGY_VCPayloadTableUpdateStatusTimerCb, pvTimerCbContext)
{
    DPCDDEF_PAYLOADTABLE_UPDATE_STATUS stPayloadTableUpdateStatus = { 0 };
    PPORTINGLAYER_OBJ                  pstPortingObj              = GetPortingObj();

    stPayloadTableUpdateStatus.ucVal = ((PUCHAR)((PTIMER_CB_CONTEXT)pvTimerCbContext)->pvCallBackContext)[DPCD_VCPAYLOAD_UPDATE_STATUS];

    // Clear ACT Handled
    stPayloadTableUpdateStatus.bActHandled                                                           = 0;
    stPayloadTableUpdateStatus.bPayloadTableUpdated                                                  = 1;
    ((PUCHAR)((PTIMER_CB_CONTEXT)pvTimerCbContext)->pvCallBackContext)[DPCD_VCPAYLOAD_UPDATE_STATUS] = stPayloadTableUpdateStatus.ucVal;

    pstPortingObj->pfnInterLockedDecrement(((PTIMER_CB_CONTEXT)pvTimerCbContext)->pulTimerScheduleCount);

    return;
}

void DP12TOPOLOGY_VCPayloadTableUpdateStatusNonTimer(PUCHAR pucBranchDPCDBuff)
{
    DPCDDEF_PAYLOADTABLE_UPDATE_STATUS stPayloadTableUpdateStatus = { 0 };

    stPayloadTableUpdateStatus.ucVal = pucBranchDPCDBuff[DPCD_VCPAYLOAD_UPDATE_STATUS];

    // Clear ACT Handled
    stPayloadTableUpdateStatus.bActHandled          = 0;
    stPayloadTableUpdateStatus.bPayloadTableUpdated = 1;
    pucBranchDPCDBuff[DPCD_VCPAYLOAD_UPDATE_STATUS] = stPayloadTableUpdateStatus.ucVal;
    return;
}

// AppWorld to differentiate ReadRemoteDPCD Sideband Message
BOOLEAN DP12TOPOLOGY_ReadRemoteDPCDAppWorld(PDP12_TOPOLOGY pstDP12Topology, PMST_RELATIVEADDRESS pstRAD, PUCHAR pucReadBuff, ULONG ulDPCDAddress, ULONG ulLength)
{
    BOOLEAN       bRet          = FALSE;
    RAD_NODE_INFO stNodeRADInfo = { 0 };
    PUCHAR        pucDPCDBuff   = NULL;
    ULONG         ulDPCDSize    = 0;

    do
    {
        stNodeRADInfo = DP12TOPOLOGY_GetNodeForAGivenRAD(pstDP12Topology, pstRAD);

        if (((PBRANCH_NODE)stNodeRADInfo.pvRADNode)->eNodeType == eBRANCH)
        {
            pucDPCDBuff = ((PBRANCH_NODE)stNodeRADInfo.pvRADNode)->stBranchDPCDMap.pucDPCDBuff;
            ulDPCDSize  = ((PBRANCH_NODE)stNodeRADInfo.pvRADNode)->stBranchDPCDMap.ulDPCDBuffSize;
        }
        else
        {
            pucDPCDBuff = ((PDISPLAY_NODE)stNodeRADInfo.pvRADNode)->stDisplayDPCDMap.pucDPCDBuff;
            ulDPCDSize  = ((PDISPLAY_NODE)stNodeRADInfo.pvRADNode)->stDisplayDPCDMap.ulDPCDBuffSize;
        }

        if (ulDPCDAddress + ulLength <= ulDPCDSize)
        {
            memcpy_s(pucReadBuff, ulLength, &pucDPCDBuff[ulDPCDAddress], ulLength);
            bRet = TRUE;
        }

    } while (FALSE);

    return bRet;
}

// AppWorld to differentiate ReadRemoteDPCD Sideband Message
BOOLEAN DP12TOPOLOGY_WriteRemoteDPCDAppWorld(PDP12_TOPOLOGY pstDP12Topology, PMST_RELATIVEADDRESS pstRAD, PUCHAR pucWriteBuff, ULONG ulDPCDAddress, ULONG ulLength)
{
    BOOLEAN       bRet          = FALSE;
    RAD_NODE_INFO stNodeRADInfo = { 0 };
    PUCHAR        pucDPCDBuff   = NULL;
    ULONG         ulDPCDSize    = 0;

    do
    {
        stNodeRADInfo = DP12TOPOLOGY_GetNodeForAGivenRAD(pstDP12Topology, pstRAD);

        if (((PBRANCH_NODE)stNodeRADInfo.pvRADNode)->eNodeType == eBRANCH)
        {
            pucDPCDBuff = ((PBRANCH_NODE)stNodeRADInfo.pvRADNode)->stBranchDPCDMap.pucDPCDBuff;
            ulDPCDSize  = ((PBRANCH_NODE)stNodeRADInfo.pvRADNode)->stBranchDPCDMap.ulDPCDBuffSize;
        }
        else
        {
            pucDPCDBuff = ((PDISPLAY_NODE)stNodeRADInfo.pvRADNode)->stDisplayDPCDMap.pucDPCDBuff;
            ulDPCDSize  = ((PDISPLAY_NODE)stNodeRADInfo.pvRADNode)->stDisplayDPCDMap.ulDPCDBuffSize;
        }

        if (ulDPCDAddress + ulLength <= ulDPCDSize)
        {
            memcpy_s(&pucDPCDBuff[ulDPCDAddress], ulLength, pucWriteBuff, ulLength);
            bRet = TRUE;
        }

    } while (FALSE);

    return bRet;
}

USHORT DP12TOPOLOGY_ComputePBNBasedOnLinkRateAndLaneCount(UCHAR ucMaxLinkRate, UCHAR ucMaxLaneCount)
{
    USHORT usPortPBN = 0;

    switch (ucMaxLinkRate)
    {
    case DP_LINKBW_1_62_GBPS:
        usPortPBN = ucMaxLaneCount * 3 * (NUM_SLOTS_PER_MTP - 1);
        break;
    case DP_LINKBW_2_7_GBPS:
        usPortPBN = ucMaxLaneCount * 5 * (NUM_SLOTS_PER_MTP - 1);
        break;
    case DP_LINKBW_5_4_GBPS:
        usPortPBN = ucMaxLaneCount * 10 * (NUM_SLOTS_PER_MTP - 1);
        break;
    case DP_LINKBW_8_1_GBPS:
        usPortPBN = ucMaxLaneCount * 15 * (NUM_SLOTS_PER_MTP - 1);
        break;
    };

    return usPortPBN;
}

BOOLEAN DP12TOPOLOGY_Cleanup(PDP12_TOPOLOGY pstDP12Topology)
{
    BOOLEAN           bRet            = FALSE;
    ULONG             ulCount         = 0;
    ULONG             ulNumBlockCount = 0;
    PPORTINGLAYER_OBJ pstPortingObj   = GetPortingObj();

    do
    {
        if (!pstDP12Topology)
        {
            break;
        }

        // Cleanup Global EDID repository
        for (ulCount = 0; ulCount < pstDP12Topology->stMSTEDIDArray.ulNumEDIDTypes; ulCount++)
        {
            for (ulNumBlockCount = 0; ulNumBlockCount < pstDP12Topology->stMSTEDIDArray.stMSTDispEDID[ulCount].ulNumEDIDBlocks; ulNumBlockCount++)
            {
                if (pstDP12Topology->stMSTEDIDArray.stMSTDispEDID[ulCount].pucEDIDBlocks[ulNumBlockCount])
                {
                    pstPortingObj->pfnFreeMem(pstDP12Topology->stMSTEDIDArray.stMSTDispEDID[ulCount].pucEDIDBlocks[ulNumBlockCount]);
                }
            }

            pstDP12Topology->stMSTEDIDArray.stMSTDispEDID[ulCount].ulNumEDIDBlocks = 0;
        }

        pstDP12Topology->stMSTEDIDArray.ulNumEDIDTypes = 0;

        // Cleanup Global DPCD repository
        for (ulCount = 0; ulCount < pstDP12Topology->stMSTDPCDArray.ulNumDPCDTypes; ulCount++)
        {
            if (pstDP12Topology->stMSTDPCDArray.stMSTBranchDispDPCD[ulCount].pucDPCDBuff)
            {
                pstPortingObj->pfnFreeMem(pstDP12Topology->stMSTDPCDArray.stMSTBranchDispDPCD[ulCount].pucDPCDBuff);
            }
        }

        pstDP12Topology->stMSTDPCDArray.ulNumDPCDTypes = 0;

        if (!pstDP12Topology->pstBranchConnectedToSrc)
        {
            break;
        }

        if (pstDP12Topology->pstBranchConnectedToSrc)
        {
            DP12TOPOLOGY_DFSBranchCleanUp(pstDP12Topology->pstBranchConnectedToSrc);
            pstDP12Topology->pstBranchConnectedToSrc = NULL;
        }

        // So we have branch. Now free in depth first search manner

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

// Fix this to free Sideband buffers associated with this branch node, if any
void DP12TOPOLOGY_DFSBranchCleanUp(PBRANCH_NODE pstBranchNode)
{
    USHORT usCount = 0;
    do
    {
        if (!pstBranchNode)
        {
            break;
        }

        for (usCount = pstBranchNode->ucTotalInputPorts; usCount < MAX_PORTS_PER_BRANCH; usCount++)
        {

            if (pstBranchNode->stOutPortList[usCount].bPortConnectedStatus)
            {
                if (pstBranchNode->stOutPortList[usCount].eConnectedDeviceNodeType == eDISPLAY)
                {
                    DP12TOPOLOGY_DisplayNodeCleanUp(pstBranchNode->stOutPortList[usCount].pvConnectedDeviceNodePointer);
                    pstBranchNode->stOutPortList[usCount].pvConnectedDeviceNodePointer = NULL;
                }
                else if (pstBranchNode->stOutPortList[usCount].eConnectedDeviceNodeType == eBRANCH)
                {
                    DP12TOPOLOGY_DFSBranchCleanUp(pstBranchNode->stOutPortList[usCount].pvConnectedDeviceNodePointer);
                    pstBranchNode->stOutPortList[usCount].pvConnectedDeviceNodePointer = NULL;
                }
            }
        }

        DP12TOPOLOGY_BranchNodeCleanUp(pstBranchNode);

    } while (FALSE);
}

void DP12TOPOLOGY_BranchNodeCleanUp(PBRANCH_NODE pstBranchNode)
{
    PPORTINGLAYER_OBJ pstPortingObj         = GetPortingObj();
    PBRANCH_NODE      pstUpStreamBranchNode = NULL;
    UCHAR             ucUpStreamPortNum     = 0;
    ULONG             ulCount               = 0;

    if (pstBranchNode)
    {
        // Adjust the upstream node's variables that would be affected on deletion of this node
        for (ulCount = 0; ulCount < pstBranchNode->ucTotalInputPorts; ulCount++)
        {
            if (pstBranchNode->stInportList[ulCount].bPortConnectedStatus == TRUE)
            {
                // UpStream has to be a branch or Topology Object in which case pstBranchNode->stInportList[ulCount].pvUpStreamNodePointer will be NULL
                if (pstBranchNode->stInportList[ulCount].pvUpStreamNodePointer)
                {
                    ucUpStreamPortNum     = pstBranchNode->stInportList[ulCount].ucUpStreamPortNumber;
                    pstUpStreamBranchNode = (PBRANCH_NODE)pstBranchNode->stInportList[ulCount].pvUpStreamNodePointer;

                    pstUpStreamBranchNode->stOutPortList[ucUpStreamPortNum].bConnectedDeviceMsgCapStatus = FALSE;
                    pstUpStreamBranchNode->stOutPortList[ucUpStreamPortNum].bPortConnectedStatus         = FALSE;
                    pstUpStreamBranchNode->stOutPortList[ucUpStreamPortNum].pvConnectedDeviceNodePointer = NULL;

                    if (ucUpStreamPortNum <= MAX_PHYSICAL_OUT_PORTS)
                    {
                        pstUpStreamBranchNode->ucAvailablePhysicalPorts++;
                    }
                    else
                    {
                        pstUpStreamBranchNode->ucAvailableVirtualPorts++;
                    }
                }
            }
        }

        // Kill DownRequest Handler thread
        pstPortingObj->pfnTerminateThreadAndExitCleanly(pstBranchNode->hDownRequestHandlerThreadHandle, &pstBranchNode->stDownRequestHandlerThreadKillEvent, NULL);

        // Kill DownReply Handler thread
        pstPortingObj->pfnTerminateThreadAndExitCleanly(pstBranchNode->hDownReplyHandlerThreadHandle, pstBranchNode->pstDownReplyHandlerThreadKillEvent, NULL);

        // Kill UpRequest Handler thread
        pstPortingObj->pfnTerminateThreadAndExitCleanly(pstBranchNode->hUpRequestHandlerThreadHandle, &pstBranchNode->stUpRequestHandlerThreadKillEvent, NULL);

        // Free lookaside List
        pstPortingObj->pfnPurgeLookAsideList(&pstBranchNode->NakInfoLookAsideListHead);

        // Free Nak Info Processing List
        pstPortingObj->pfnPurgeList(&pstBranchNode->NakInfoProcessingListHead);

        // Free UpRequest List
        pstPortingObj->pfnPurgeList(&pstBranchNode->stUpRequestListHead);

        // Free down request data buffers 1 & 2
        if (pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_1].puchBuffPtr)
        {
            pstPortingObj->pfnFreeMem(pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_1].puchBuffPtr);
            pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_1].puchBuffPtr = NULL;
        }

        if (pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_2].puchBuffPtr)
        {
            pstPortingObj->pfnFreeMem(pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_2].puchBuffPtr);
            pstBranchNode->stDownRequestBuffInfo[INDEX_BUFF_2].puchBuffPtr = NULL;
        }

        // Free Down Reply Buffer
        if (pstBranchNode->stDownReplyBuffInfo.puchBuffPtr)
        {
            pstPortingObj->pfnFreeMem(pstBranchNode->stDownReplyBuffInfo.puchBuffPtr);
            pstBranchNode->stDownReplyBuffInfo.puchBuffPtr = NULL;
        }

        // Free Up Request Buffer
        if (pstBranchNode->stUpRequestBuffInfo.puchUpReqBuffPtr)
        {
            pstPortingObj->pfnFreeMem(pstBranchNode->stUpRequestBuffInfo.puchUpReqBuffPtr);
            pstBranchNode->stUpRequestBuffInfo.puchUpReqBuffPtr = NULL;
        }

        // Free Up Reply Buffer
        if (pstBranchNode->stUpReplyInfo.puchBuffPtr)
        {
            pstPortingObj->pfnFreeMem(pstBranchNode->stUpReplyInfo.puchBuffPtr);
            pstBranchNode->stUpReplyInfo.puchBuffPtr = NULL;
        }

        // Free Branch's DPCD Buffer
        // BranchConnectedToSrc just has a pointer to the DPCDBuffer Allocated during DPAuxInterface Init
        // So the contract here is that only DPAuxInterface Cleanup code will free it
        // So cleanup pstBranchNode->stBranchDPCDMap.pucDPCDBuff only for non-BranchConnectedToSrc
        if (pstBranchNode->bIsBranchConnectedToSrc == FALSE && pstBranchNode->stBranchDPCDMap.pucDPCDBuff)
        {
            pstPortingObj->pfnFreeMem(pstBranchNode->stBranchDPCDMap.pucDPCDBuff);
            pstBranchNode->stBranchDPCDMap.pucDPCDBuff = NULL;
        }

        pstPortingObj->pfnFreeMem(pstBranchNode);
    }
}

void DP12TOPOLOGY_DisplayNodeCleanUp(PDISPLAY_NODE pstDisplayNode)
{
    PPORTINGLAYER_OBJ pstPortingObj         = GetPortingObj();
    PBRANCH_NODE      pstUpStreamBranchNode = NULL;
    UCHAR             ucUpStreamPortNum     = 0;
    ULONG             ulCount               = 0;

    if (pstDisplayNode)
    {
        // Adjust the upstream node's variables that would be affected on deletion of this node
        for (ulCount = 0; ulCount < pstDisplayNode->ucTotalInputPorts; ulCount++)
        {
            if (pstDisplayNode->stInportList[ulCount].bPortConnectedStatus == TRUE)
            {
                // UpStream has to be a branch or Topology Object in which case pstBranchNode->stInportList[ulCount].pvUpStreamNodePointer will be NULL
                if (pstDisplayNode->stInportList[ulCount].pvUpStreamNodePointer)
                {
                    ucUpStreamPortNum     = pstDisplayNode->stInportList[ulCount].ucUpStreamPortNumber;
                    pstUpStreamBranchNode = (PBRANCH_NODE)pstDisplayNode->stInportList[ulCount].pvUpStreamNodePointer;

                    pstUpStreamBranchNode->stOutPortList[ucUpStreamPortNum].bConnectedDeviceMsgCapStatus = FALSE;
                    pstUpStreamBranchNode->stOutPortList[ucUpStreamPortNum].bPortConnectedStatus         = FALSE;
                    pstUpStreamBranchNode->stOutPortList[ucUpStreamPortNum].pvConnectedDeviceNodePointer = NULL;

                    if (ucUpStreamPortNum <= MAX_PHYSICAL_OUT_PORTS)
                    {
                        pstUpStreamBranchNode->ucAvailablePhysicalPorts++;
                    }
                    else
                    {
                        pstUpStreamBranchNode->ucAvailableVirtualPorts++;
                    }
                }
            }
        }

        if (pstDisplayNode->stDisplayDPCDMap.pucDPCDBuff)
        {
            pstPortingObj->pfnFreeMem(pstDisplayNode->stDisplayDPCDMap.pucDPCDBuff);
            pstDisplayNode->stDisplayDPCDMap.pucDPCDBuff = NULL;
        }

        pstPortingObj->pfnFreeMem(pstDisplayNode);
    }
}

void DP12TOPOLOGY_DFSReCalculateDownStreamNodesRAD(PBRANCH_NODE pstBranchNode, PMST_RELATIVEADDRESS pstUpStreamNodeRAD, UCHAR ucUpStreamOutPort)
{
    UCHAR         ucCount            = 0;
    PBRANCH_NODE  pstTempBranchNode  = NULL;
    PDISPLAY_NODE pstTempDisplayNode = NULL;
    do
    {
        if (!pstBranchNode)
        {
            break;
        }

        DP12TOPOLOGY_CreateRad(pstUpStreamNodeRAD, &pstBranchNode->stBranchRAD, ucUpStreamOutPort);

        for (ucCount = pstBranchNode->ucTotalInputPorts; ucCount < MAX_PORTS_PER_BRANCH; ucCount++)
        {

            if (pstBranchNode->stOutPortList[ucCount].bPortConnectedStatus)
            {
                pstTempDisplayNode = (PDISPLAY_NODE)pstBranchNode->stOutPortList[ucCount].pvConnectedDeviceNodePointer;
                pstTempBranchNode  = (PBRANCH_NODE)pstBranchNode->stOutPortList[ucCount].pvConnectedDeviceNodePointer;

                if (pstTempBranchNode->eNodeType == eBRANCH)
                {
                    DP12TOPOLOGY_DFSReCalculateDownStreamNodesRAD(pstTempBranchNode, &pstBranchNode->stBranchRAD, ucCount);
                }
                else
                {
                    DP12TOPOLOGY_CreateRad(&pstBranchNode->stBranchRAD, &pstTempDisplayNode->stDisplayRAD, ucCount);
                }
            }
        }

    } while (FALSE);

    return;
}

/*
//This function takes daisychain depth and an array of PBN values for each branch node. Length of array = ucDaisyChainDepth
//bSidebandBuffFirstBranchOnly means caller wants to create a topology in which only first branch has sidebandbuffers
//Caller could choose to do so if it neevr intends to read or write to any of the sideband buffers of branch nodes beyond the first branch
//This parameter just allows us not to allocate sideband buff memory that would never be used
BOOLEAN DP12TOPOLOGY_CreateDefaultMSTTopology(PDP12_TOPOLOGY pstDP12Topology, ULONG ulDaisyChainDepth, PPBN_AVAILABLE peBranchPBNAvailable, PPBN_AVAILABLE peDisplayPBNAvailable,
PUCHAR pucClientDPCDMap)
{
ULONG ulCount = 0;
NODE_ADD_ERRROR_CODES eErrorCode = eGENERIC_ERROR;
PBRANCH_NODE pstNewBranchNode = NULL;
PBRANCH_NODE pstTempBranchNode = NULL;
PDISPLAY_NODE pstDisplayNode = NULL;
BOOLEAN bRet = FALSE;

do
{


if (!ulDaisyChainDepth)
{
//Depth needs to be Non zero
break;
}

pstNewBranchNode = DP12TOPOLOGY_CreateBranchNode(  pstDP12Topology,
eMSTBRANCHDEVICE,
peBranchPBNAvailable[ulCount],
1,
1,
1,
eDPCDRev_1_2,
pucClientDPCDMap);

if (!pstNewBranchNode)
{
break;
}

eErrorCode = DP12TOPOLOGY_AddFirstBranch(   pstDP12Topology,
pstNewBranchNode,
0,
eMST);

if (eErrorCode != eNODE_ADD_SUCCESS)
{
break;
}

pstDisplayNode = DP12TOPOLOGY_CreateDisplayNode(pstDP12Topology,
eSSTSINKORSTREAMSINK,
eDELL_3011,
peDisplayPBNAvailable[ulCount],
1,
eDPCDRev_1_2,
ulDPCDIndex);

if (!pstDisplayNode)
{
break;
}

eErrorCode = DP12TOPOLOGY_AddDisplay(   pstNewBranchNode,
pstDisplayNode,
8,
0);

if (eErrorCode != eNODE_ADD_SUCCESS)
{
break;
}

pstTempBranchNode = pstNewBranchNode;

for (ulCount = 1; ulCount < ulDaisyChainDepth; ulCount++)
{

pstNewBranchNode = DP12TOPOLOGY_CreateBranchNode(   pstDP12Topology,
eMSTBRANCHDEVICE,
peBranchPBNAvailable[ulCount],
1,
1,
1,
eDPCDRev_1_2,
NULL);


if (!pstNewBranchNode)
{
break;
}

eErrorCode = DP12TOPOLOGY_AddBranch( pstTempBranchNode,
pstNewBranchNode,
1,
0);

if (eErrorCode != eNODE_ADD_SUCCESS)
{
break;
}

pstTempBranchNode = pstNewBranchNode;

pstDisplayNode = DP12TOPOLOGY_CreateDisplayNode(   pstDP12Topology,
eSSTSINKORSTREAMSINK,
eDELL_3011,
peDisplayPBNAvailable[ulCount],
1,
eDPCDRev_1_2,
NULL);

if (!pstDisplayNode)
{
break;
}

eErrorCode = DP12TOPOLOGY_AddDisplay(   pstTempBranchNode,
pstDisplayNode,
8,
0);

if (eErrorCode != eNODE_ADD_SUCCESS)
{
break;
}

}

if (eErrorCode == eNODE_ADD_SUCCESS)
{
pstDisplayNode = DP12TOPOLOGY_CreateDisplayNode( pstDP12Topology,
eSSTSINKORSTREAMSINK,
eDELL_3011,
peDisplayPBNAvailable[ulCount],
1,
eDPCDRev_1_2,
NULL);

if (!pstDisplayNode)
{
break;
}

eErrorCode = DP12TOPOLOGY_AddDisplay(   pstTempBranchNode,
pstDisplayNode,
1,
0);

if (eErrorCode == eNODE_ADD_SUCCESS)
{
bRet = TRUE;
}
}


} while (FALSE);

if (bRet == FALSE)
{
if (pstDP12Topology)
{
DP12TOPOLOGY_CleanupTopology(pstDP12Topology);
}

}

return bRet;
}

BOOLEAN DP12TOPOLOGY_UpRequestHandler(PDP12_TOPOLOGY pstDP12Topology, PUP_REQUEST_ARGS pstUpRequestArgs)
{
    BOOLEAN bRet = FALSE;
    PUPREQUEST_NODE_ENTRY   pstUpReqNodeEntry = NULL;

    PBRANCH_NODE pstBranchConnectedToSrc = pstDP12Topology->pstBranchConnectedToSrc;

    RAD_NODE_INFO stRADNodeInfo = { 0 };
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    do
    {
        if (pstDP12Topology == NULL || pstUpRequestArgs == NULL)
        {
            break;
        }

        stRADNodeInfo = DP12TOPOLOGY_GetNodeForAGivenRAD(pstDP12Topology, &pstUpRequestArgs->stRAD);

        switch (pstUpRequestArgs->eUpRequestID)
        {
            case eMST_CONNECTION_STATUS_NOTIFY:

                //Requested Attach/Detach status is same as the current one
                if (pstUpRequestArgs->stCSNArgs.bAttachOrDetatch == DP12TOPOLOGY_GetNodePortAttachStatus(stRADNodeInfo.pstBranchNode, eBRANCH, stRADNodeInfo.ucPortNum))
                {
                    break;
                }

                if (pstUpRequestArgs->stCSNArgs.bAttachOrDetatch == FALSE)
                {
                    if (stRADNodeInfo.pvRADNode == NULL)
                    {
                        break;
                    }

                    if (((PBRANCH_NODE)stRADNodeInfo.pvRADNode)->eNodeType == eBRANCH)
                    {
                        DP12TOPOLOGY_DFSBranchCleanUp(stRADNodeInfo.pvRADNode);
                    }
                    else
                    {
                        DP12TOPOLOGY_DisplayNodeCleanUp(stRADNodeInfo.pvRADNode);
                    }
                }
                else if (pstUpRequestArgs->stCSNArgs.bAttachOrDetatch == TRUE)
                {
                    if (pstUpRequestArgs->stCSNArgs.pvNewNodeToBeAdded == NULL)
                    {
                        break;
                    }

                    if (((PBRANCH_NODE)pstUpRequestArgs->stCSNArgs.pvNewNodeToBeAdded)->eNodeType == eBRANCH)
                    {
                        if (eNODE_ADD_SUCCESS != DP12TOPOLOGY_AddBranch(pstDP12Topology,
                                                                        stRADNodeInfo.pstBranchNode,
                                                                        pstUpRequestArgs->stCSNArgs.pvNewNodeToBeAdded,
                                                                        stRADNodeInfo.ucPortNum,
                                                                        pstUpRequestArgs->stCSNArgs.ucNewNodeInputPort,
                                                                        TRUE))
                        {
                            break;
                        }
                    }
                    else
                    {
                        if (eNODE_ADD_SUCCESS != DP12TOPOLOGY_AddDisplay(pstDP12Topology,
                                                                         stRADNodeInfo.pstBranchNode,
                                                                         pstUpRequestArgs->stCSNArgs.pvNewNodeToBeAdded,
                                                                         stRADNodeInfo.ucPortNum,
                                                                         pstUpRequestArgs->stCSNArgs.ucNewNodeInputPort))
                        {
                            break;
                        }
                    }
                }

                pstUpReqNodeEntry = SIDEBANDMESSAGE_ConnectionStatusNotifyUpRequestHandler(pstBranchConnectedToSrc, stRADNodeInfo.pstBranchNode, stRADNodeInfo.ucPortNum);

                break;

            case eMST_RESOURCE_STATUS_NOTIFY:
                break;

            default:
                break;
        }

        if (pstUpReqNodeEntry)
        {
            pstUpReqNodeEntry->ucRequestID = pstUpRequestArgs->eUpRequestID;
            pstUpReqNodeEntry->pvSimDrvToGfxContext = pstUpRequestArgs->pvSimDrvToGfxContext;
            pstUpReqNodeEntry->ulPortNum = pstUpRequestArgs->ulPortNum;
            pstPortingObj->pfnInterlockedInsertTailList(&pstBranchConnectedToSrc->stUpRequestListHead, &pstUpReqNodeEntry->ListEntry);
            //Now signal the event to unblock the upstream down reply processing thread
            pstPortingObj->pfnSetDPEvent(&pstBranchConnectedToSrc->stUpRequestEvent, PRIORITY_NO_INCREMENT);

            bRet = TRUE;
        }

    } while (FALSE);

    return bRet;

}

*/
