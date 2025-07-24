
#include "MSTTopology.h"
#include "SidebandMessageHandlers.h"
#include "AuxDefs.h"
#include "..\CommonInclude\ETWLogging.h"

PROCESSING_RESULT SIDEBANDMESSAGE_RemoteDPCDReadDownRequestHandler(PBRANCH_NODE pstBranchNode, PVOID pvNode, NODE_TYPE eNodeType, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo,
                                                                   PMST_REASON_FOR_NAK peReasonForNak);
PROCESSING_RESULT SIDEBANDMESSAGE_RemoteDPCDWriteDownRequestHandler(PBRANCH_NODE pstBranchNode, PVOID pvNode, NODE_TYPE eNodeType, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo,
                                                                    PMST_REASON_FOR_NAK peReasonForNak);
PROCESSING_RESULT SIDEBANDMESSAGE_RemoteI2CReadDownRequestHandler(PBRANCH_NODE pstBranchNode, PDISPLAY_NODE pstDisplayNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo,
                                                                  PMST_REASON_FOR_NAK peReasonForNak);
PROCESSING_RESULT SIDEBANDMESSAGE_RemoteI2CWriteDownRequestHandler(PBRANCH_NODE pstBranchNode, PDISPLAY_NODE pstDisplayNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo,
                                                                   PMST_REASON_FOR_NAK peReasonForNak);

PROCESSING_RESULT SIDEBANDMESSAGE_RemoteI2CReadEDIDHandler(PBRANCH_NODE pstBranchNode, PDISPLAY_NODE pstDisplayNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo,
                                                           PMST_REMOTE_I2C_READ_ST1 pstRemoteI2CReadSt1, PMST_REMOTE_I2C_WRITEB4READ_HEAD pstRemoteI2CB4ReadHead,
                                                           PMST_REMOTE_I2C_READ_ST2 pstRemoteI2CReadSt2, PEDID_I2C_DATA pstEDIDI2CData, PMST_REASON_FOR_NAK peReasonForNak);

PROCESSING_RESULT SIDEBANDMESSAGE_RemoteI2CWriteEDIDHandler(PBRANCH_NODE pstBranchNode, PDISPLAY_NODE pstDisplayNode, PMST_REMOTE_I2C_WRITE_ST pstRemoteI2CWrite,
                                                            PEDID_I2C_DATA pstEDIDI2CData, PMST_REASON_FOR_NAK peReasonForNak);

BOOLEAN SIDEBANDMESSAGE_GetNodePBN(PVOID pvNode, NODE_TYPE eNodeType, PUSHORT pusFullPBN, PUSHORT pusAvailablePBN);

BOOLEAN SIDEBANDMESSAGE_GetFECPathInfo(PVOID pvNode, NODE_TYPE eNodeType, PUCHAR bFECPathInfo);

// Since clearpayload is a brute force way to clear all ports so
PROCESSING_RESULT SIDEBANDMESSAGE_ClearPayloadIDDownRequestHandler(PBRANCH_NODE pstBranchNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo, PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT         eProcessingResult      = ePROCESSING_ERROR;
    USHORT                    usCount                = 0;
    PBRANCH_NODE              pstDwnStreamBranchNode = NULL;
    PMST_DWNREQUEST_BUFF_INFO pstDwnStreamBuffInfo   = NULL;
    PPORTINGLAYER_OBJ         pstPortingObj          = GetPortingObj();

    do
    {
        if (pstDwnReqBuffInfo->stHeaderInfo.bIsPathMsg == FALSE || pstDwnReqBuffInfo->stHeaderInfo.bIsBroadcastMsg == FALSE)
        {
            // Link Address can't be a path message
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        if (pstDwnReqBuffInfo->stHeaderInfo.stCurrentHeaderRAD.ucRemainingLinkCount != 6)
        {
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        // Since clearpayload is a brute force way to clear all ports
        for (usCount = 0; usCount < MAX_OUTPUT_PORTS; usCount++)
        {

            if (pstBranchNode->stOutPortList[usCount].bPortConnectedStatus && pstBranchNode->stOutPortList[usCount].eConnectedDeviceNodeType == eBRANCH &&
                pstBranchNode->stOutPortList[usCount].ucStreamID != VCPLAYLOAD_STREAMID_INVALID && pstBranchNode->stOutPortList[usCount].stStreamRAD.ucTotalLinkCount > 1)
            {

                pstBranchNode->bAllocPayloadSentForClearPayload = TRUE;
                pstBranchNode->ulNumAllocPayloadSentForClearPayload++;

                pstBranchNode->usCurrentAvailablePBN += pstBranchNode->stOutPortList[usCount].usAllocatedPBN;

                if (pstBranchNode->stOutPortList[usCount].eConnectedDeviceNodeType == eDISPLAY)
                {
                    pstBranchNode->stOutPortList[usCount].usAllocatedPBN = 0;
                    pstBranchNode->stOutPortList[usCount].ucStreamID     = VCPLAYLOAD_STREAMID_INVALID;
                    continue;
                }

                pstDwnStreamBranchNode = (PBRANCH_NODE)pstBranchNode->stOutPortList[usCount].pvConnectedDeviceNodePointer;

                pstDwnStreamBuffInfo                                  = pstDwnStreamBranchNode->pfnGetAvailableDownReqBuff(pstDwnStreamBranchNode);
                pstDwnStreamBuffInfo->stHeaderInfo.bIsPathMsg         = TRUE;
                pstDwnStreamBuffInfo->stHeaderInfo.ulTotalBodySize    = sizeof(MST_ALLOC_PAYLOAD);
                pstDwnStreamBuffInfo->stHeaderInfo.stCurrentHeaderRAD = pstBranchNode->stOutPortList[usCount].stStreamRAD;

                ((PMST_ALLOC_PAYLOAD)pstDwnReqBuffInfo->puchBuffPtr)->ucVCPID            = pstBranchNode->stOutPortList[usCount].ucStreamID;
                ((PMST_ALLOC_PAYLOAD)pstDwnStreamBuffInfo->puchBuffPtr)->ucRequestID     = eMST_ALLOCATE_PAYLOAD;
                ((PMST_ALLOC_PAYLOAD)pstDwnStreamBuffInfo->puchBuffPtr)->ucPBN0_7        = 0;
                ((PMST_ALLOC_PAYLOAD)pstDwnStreamBuffInfo->puchBuffPtr)->ucPBN8_15       = 0;
                ((PMST_ALLOC_PAYLOAD)pstDwnStreamBuffInfo->puchBuffPtr)->ucNumSDPStreams = 0;

                // Now reset the PBN on this port
                pstBranchNode->stOutPortList[usCount].usAllocatedPBN = 0;
                // Reset RAD
                memset(&pstBranchNode->stOutPortList[usCount].stStreamRAD, 0, sizeof(MST_RELATIVEADDRESS));
                // memset(&pstBranchNode->stOutPortList[usCount].StreamID will be zeroed as a part of Post Processing in DP12TOPOLOGY_UpdateDownStreamBranchVCPayloadTable
                // Because StreamID is needed there
                // Below field will be reset in SIDEBANDMESSAGE_ClearPayloadIDDownReplyHandler
                pstBranchNode->stOutPortList[usCount].bPostUpdateDownStreamTable = TRUE;

                // Since we have forwareded this request to the downstream node so we can return this buffer of the current node
                // to its free downrequest buffer pool
                pstBranchNode->pfnSetDownReqBuffState(pstBranchNode, pstDwnReqBuffInfo->ucThisBuffIndex, eReturnToFreePool);

                // Set the downstream node event to unblock its down request processing handler and make it handle this request
                pstPortingObj->pfnSetDPEvent(&pstDwnStreamBuffInfo->stBuffEvent, PRIORITY_NO_INCREMENT);
            }
        }

        if (pstBranchNode->bAllocPayloadSentForClearPayload)
        {
            eProcessingResult = ePARTIALLY_PROCESSED;
        }
        else
        {
            pstDwnReqBuffInfo->ulFinalReplySize =
            SIDEBANDMESSAGE_PacketizeInto48ByteChunks(pstDwnReqBuffInfo->puchBuffPtr, sizeof(MST_REPLY_DATA), &pstBranchNode->stBranchRAD, FALSE, FALSE, 0);
            eProcessingResult = ePROCESSED;
        }

    } while (FALSE);

    return eProcessingResult;
}

PROCESSING_RESULT SIDEBANDMESSAGE_ClearPayloadIDDownReplyHandler(PBRANCH_NODE pstBranchNode, UCHAR ucGeneratedEventPortNum, BOOLEAN bSeqNo)
{
    // ClearPayload sideband message handling
    PROCESSING_RESULT eProcessingResult = ePARTIALLY_PROCESSED;

    pstBranchNode->ulNumAllocPayloadSentForClearPayload--;

    if (pstBranchNode->ulNumAllocPayloadSentForClearPayload == 0)
    {
        pstBranchNode->bAllocPayloadSentForClearPayload                                = FALSE;
        ((PMST_REPLY_DATA)pstBranchNode->stDownReplyBuffInfo.puchBuffPtr)->bReplyType  = 0; // ACK
        ((PMST_REPLY_DATA)pstBranchNode->stDownReplyBuffInfo.puchBuffPtr)->ucRequestID = eMST_CLEAR_PAYLOAD_ID_TABLE;
        pstBranchNode->stDownReplyBuffInfo.ulTotalReplySize =
        SIDEBANDMESSAGE_PacketizeInto48ByteChunks(pstBranchNode->stDownReplyBuffInfo.puchBuffPtr, sizeof(MST_REPLY_DATA), &pstBranchNode->stBranchRAD, FALSE, FALSE, bSeqNo);
        eProcessingResult = ePROCESSED;
    }

    return eProcessingResult;
}

// Implementation Note: 2 ways to create Reply Header
// 1. Pass the saved header details like RAD of the Original sideband request and simply append it here
//   One issue with approach, Lets say header CRC was bad and we want to return NAK with reason for NAK as
//   Bad header CRC so we would be be sending the same Bad CRC again
//   Another issue with this approach is that I was wrong to assume all Headers would have different SMT and EMT and CRC..LOL
// 2. Branch Node has its RAD info. Create Header from that
//   Approach 2  seems better because of the issue with approach 1
PROCESSING_RESULT SIDEBANDMESSAGE_LinkAddressDownRequestHandler(PBRANCH_NODE pstBranchNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo, PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT eProcessingResult = ePROCESSING_ERROR;
    UCHAR             ucCount           = 0;
    PUCHAR            pucTemp           = NULL;

    ULONG ulTotalBodyLength = 0;
    GUID *pGUID             = NULL;
    UCHAR ucDPCDRev         = 0;

    do
    {

        if (pstDwnReqBuffInfo->stHeaderInfo.stCurrentHeaderRAD.ucRemainingLinkCount != 0)
        {
            eProcessingResult = eDID_NOT_PROCESS;
            break;
        }

        if (pstDwnReqBuffInfo->stHeaderInfo.bIsPathMsg)
        {
            // Link Address can't be a path message
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        // Link Address targetted at this branch
        pucTemp = pstDwnReqBuffInfo->puchBuffPtr;

        // Move beyond the first byte as it would contain the ACK:1 and RequestID:7
        pucTemp++;
        ulTotalBodyLength++;

        ((PMST_LINK_ADDRESS_REPLY_DATA)pucTemp)->guid = pstBranchNode->uidBranchGUID;
        ((PMST_LINK_ADDRESS_REPLY_DATA)pucTemp)->ucPortNo =
        ((pstBranchNode->ucTotalInputPorts - pstBranchNode->ucAvailableInputPorts) + (pstBranchNode->ucTotalPhysicalPorts - pstBranchNode->ucAvailablePhysicalPorts) +
         (pstBranchNode->ucTotalVirtualPorts - pstBranchNode->ucAvailableVirtualPorts));

        ulTotalBodyLength += sizeof(MST_LINK_ADDRESS_REPLY_DATA);
        pucTemp += sizeof(MST_LINK_ADDRESS_REPLY_DATA);

        for (ucCount = 0; ucCount < pstBranchNode->ucTotalInputPorts; ucCount++)
        {
            if (pstBranchNode->stInportList[ucCount].ucInputPortNumber == DP_PORT_NA)
            {
                break;
            }

            memset(pucTemp, 0, sizeof(MST_LINK_ADDRESS_INPUT_PORT_DETAILS));

            ((PMST_LINK_ADDRESS_INPUT_PORT_DETAILS)pucTemp)->ucPortNumber         = pstBranchNode->stInportList[ucCount].ucInputPortNumber;
            ((PMST_LINK_ADDRESS_INPUT_PORT_DETAILS)pucTemp)->ucPeerDeviceType     = pstBranchNode->stInportList[ucCount].stUpStreamDevicePeerType;
            ((PMST_LINK_ADDRESS_INPUT_PORT_DETAILS)pucTemp)->ucInputPort          = 1; // Yes its an input port
            ((PMST_LINK_ADDRESS_INPUT_PORT_DETAILS)pucTemp)->ucDPDevicePlugStatus = pstBranchNode->stInportList[ucCount].bPortConnectedStatus;
            ((PMST_LINK_ADDRESS_INPUT_PORT_DETAILS)pucTemp)->ucMsgCapStatus =
            1; // Set MsgCap status to true. Lets handle it more programmatically in future by putting it in the node

            ulTotalBodyLength += sizeof(MST_LINK_ADDRESS_INPUT_PORT_DETAILS);
            pucTemp += sizeof(MST_LINK_ADDRESS_INPUT_PORT_DETAILS);
        }

        for (ucCount = pstBranchNode->ucTotalInputPorts; ucCount < MAX_PORTS_PER_BRANCH; ucCount++)
        {
            if (pstBranchNode->stOutPortList[ucCount].ucOutPortNumber == DP_PORT_NA || pstBranchNode->stOutPortList[ucCount].bPortConnectedStatus == FALSE)
            {
                continue;
            }

            memset(pucTemp, 0, sizeof(MST_LINK_ADDRESS_OUTPORT_PORT_DETAILS));

            if (pstBranchNode->stOutPortList[ucCount].eConnectedDeviceNodeType == eBRANCH)
            {

                pGUID     = &((PBRANCH_NODE)(pstBranchNode->stOutPortList[ucCount].pvConnectedDeviceNodePointer))->uidBranchGUID;
                ucDPCDRev = ((PBRANCH_NODE)(pstBranchNode->stOutPortList[ucCount].pvConnectedDeviceNodePointer))->eDPCDRev;
            }
            else
            {

                pGUID     = &((PDISPLAY_NODE)(pstBranchNode->stOutPortList[ucCount].pvConnectedDeviceNodePointer))->uidDisplayGUID;
                ucDPCDRev = ((PDISPLAY_NODE)(pstBranchNode->stOutPortList[ucCount].pvConnectedDeviceNodePointer))->eDPCDRev;
            }

            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->ucPortNumber             = pstBranchNode->stOutPortList[ucCount].ucOutPortNumber;
            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->ucPeerDeviceType         = pstBranchNode->stOutPortList[ucCount].stConnectedDevicePeerType;
            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->ucInputPort              = 0; // Its an Output port
            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->ucZeros                  = 0;
            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->ucLegacyDevicePlugStatus = 0;
            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->ucDPDevicePlugStatus     = pstBranchNode->stOutPortList[ucCount].bPortConnectedStatus;
            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->ucMsgCapStatus           = pstBranchNode->stOutPortList[ucCount].bConnectedDeviceMsgCapStatus;
            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->DPCDRev                  = ucDPCDRev;
            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->Peerguid                 = *pGUID;
            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->ucNumSDPStreamSinks      = 0;
            ((PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS)pucTemp)->ucNumSDPStreams          = 0;

            ulTotalBodyLength += sizeof(MST_LINK_ADDRESS_OUTPORT_PORT_DETAILS);
            pucTemp += sizeof(MST_LINK_ADDRESS_OUTPORT_PORT_DETAILS);
        }

        pstDwnReqBuffInfo->ulFinalReplySize =
        SIDEBANDMESSAGE_PacketizeInto48ByteChunks(pstDwnReqBuffInfo->puchBuffPtr, ulTotalBodyLength, &pstBranchNode->stBranchRAD, FALSE, FALSE, 0);

        eProcessingResult = ePROCESSED;

    } while (FALSE);

    return eProcessingResult;
}

PROCESSING_RESULT SIDEBANDMESSAGE_EnumPathResourcesDownRequestHandler(PBRANCH_NODE pstBranchNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo, PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT              eProcessingResult   = ePROCESSING_ERROR;
    PMST_ENUM_PATH_RESOURCES       pstEnumPathRsrcReq  = NULL;
    PMST_ENUM_PATH_RESOURCES_REPLY pstEnumPathRrcReply = NULL;
    USHORT                         usFullPBN           = 0;
    UCHAR                          ucFECPathInfo       = 0;
    USHORT                         usAvailablePBN      = 0;
    POUTPORT_ENTRY                 pstOutportEntry     = NULL;
    UCHAR                          ucOutportNum        = 0;

    ULONG ulTotalBodyLength = 0;

    do
    {
        if (pstDwnReqBuffInfo->stHeaderInfo.bIsPathMsg == FALSE)
        {
            // Link Address can't be a path message
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        if (pstDwnReqBuffInfo->stHeaderInfo.stCurrentHeaderRAD.ucRemainingLinkCount != 0)
        {
            eProcessingResult = eDID_NOT_PROCESS;
            break;
        }

        pstEnumPathRsrcReq = (PMST_ENUM_PATH_RESOURCES)pstDwnReqBuffInfo->puchBuffPtr;

        // Reusing the request buffer to compile the reply and finally will fill it in the downreply buffer
        pstEnumPathRrcReply = (PMST_ENUM_PATH_RESOURCES_REPLY)pstDwnReqBuffInfo->puchBuffPtr;

        ucOutportNum = (UCHAR)pstEnumPathRsrcReq->ucPortNumber;

        if (ucOutportNum > MAX_PORTS_PER_BRANCH)
        {
            // Bad port number
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        pstOutportEntry = &pstBranchNode->stOutPortList[ucOutportNum];

        if (pstOutportEntry->bPortConnectedStatus == FALSE)
        {
            // Bad port number
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        // ulPBN = pstOutportEntry->ulTrainedLinkPBN;
        SIDEBANDMESSAGE_GetNodePBN(pstOutportEntry->pvConnectedDeviceNodePointer, pstOutportEntry->eConnectedDeviceNodeType, &usFullPBN, &usAvailablePBN);
        SIDEBANDMESSAGE_GetFECPathInfo(pstOutportEntry->pvConnectedDeviceNodePointer, pstOutportEntry->eConnectedDeviceNodeType, &ucFECPathInfo);

        // Now take the min of this Branch node PBN and the downstream Node PBN we just got
        // Basically we are doing the same thing here as SIDEBANDMESSAGE_EnumPathResourcesDownReplyHandler as the reply travels upstream
        // But SIDEBANDMESSAGE_EnumPathResourcesDownReplyHandler does this for nodes above this branch node so we have to this here
        // manually without using SIDEBANDMESSAGE_EnumPathResourcesDownReplyHandler. Its faster too.
        usFullPBN      = pstBranchNode->usTotalAvailablePBN < usFullPBN ? pstBranchNode->usTotalAvailablePBN : usFullPBN;
        usAvailablePBN = pstBranchNode->usCurrentAvailablePBN < usAvailablePBN ? pstBranchNode->usCurrentAvailablePBN : usAvailablePBN;

        pstEnumPathRrcReply->uczeros                                = 0;
        pstEnumPathRrcReply->FEC_Capability                         = ucFECPathInfo;
        pstEnumPathRrcReply->Port_Number                            = ucOutportNum;
        pstEnumPathRrcReply->Payload_Bandwidth_Full_Number7_0       = usFullPBN & 0xFF;
        pstEnumPathRrcReply->Payload_Bandwidth_Full_Number15_8      = (usFullPBN & 0xFF00) >> 8;
        pstEnumPathRrcReply->Payload_Bandwidth_Available_Number7_0  = usAvailablePBN & 0xFF;
        pstEnumPathRrcReply->Payload_Bandwidth_Available_Number15_8 = (usAvailablePBN & 0xFF00) >> 8;

        ulTotalBodyLength += sizeof(MST_ENUM_PATH_RESOURCES_REPLY);

        pstDwnReqBuffInfo->ulFinalReplySize =
        SIDEBANDMESSAGE_PacketizeInto48ByteChunks(pstDwnReqBuffInfo->puchBuffPtr, ulTotalBodyLength, &pstBranchNode->stBranchRAD, TRUE, FALSE, 0);

        eProcessingResult = ePROCESSED;

    } while (FALSE);

    return eProcessingResult;
}

PROCESSING_RESULT SIDEBANDMESSAGE_EnumPathResourcesDownReplyHandler(PBRANCH_NODE pstBranchNode, PUCHAR pucReplyBuff, UCHAR ucHeaderSize)
{
    PROCESSING_RESULT eProcessingResult = ePROCESSING_ERROR;

    PMST_ENUM_PATH_RESOURCES_REPLY pstEnumPathRrcReply     = NULL;
    USHORT                         usDwnStreamFullPBN      = 0;
    USHORT                         usDwnStreamAvailablePBN = 0;
    USHORT                         usThisFullPBN           = 0;
    USHORT                         usThisAvailablePBN      = 0;
    UCHAR                          ucCurrentDataCRC        = 0;
    UCHAR                          ucBodyLen               = 6; // size of EPR message body data as per DP spec

    do
    {
        if (pstBranchNode == NULL)
        {
            break;
        }

        // Move past header
        pucReplyBuff += ucHeaderSize;

        pstEnumPathRrcReply = (PMST_ENUM_PATH_RESOURCES_REPLY)pucReplyBuff;

        usDwnStreamFullPBN      = (USHORT)((pstEnumPathRrcReply->Payload_Bandwidth_Full_Number15_8 << 8) | pstEnumPathRrcReply->Payload_Bandwidth_Full_Number7_0);
        usDwnStreamAvailablePBN = (USHORT)((pstEnumPathRrcReply->Payload_Bandwidth_Available_Number15_8 << 8) | pstEnumPathRrcReply->Payload_Bandwidth_Available_Number7_0);

        SIDEBANDMESSAGE_GetNodePBN(pstBranchNode, eBRANCH, &usThisFullPBN, &usThisAvailablePBN);

        if (usThisFullPBN < usDwnStreamFullPBN)
        {
            pstEnumPathRrcReply->Payload_Bandwidth_Full_Number7_0  = usThisFullPBN & 0xFF;
            pstEnumPathRrcReply->Payload_Bandwidth_Full_Number15_8 = (usDwnStreamFullPBN & 0xFF00) >> 8;
            ucCurrentDataCRC                                       = SIDEBANDUTIL_CalculateDataCRC(pucReplyBuff, ucBodyLen);
            *(pucReplyBuff + ucBodyLen)                            = ucCurrentDataCRC;
        }

        if (usThisAvailablePBN < usDwnStreamAvailablePBN)
        {
            pstEnumPathRrcReply->Payload_Bandwidth_Available_Number7_0  = usThisAvailablePBN & 0xFF;
            pstEnumPathRrcReply->Payload_Bandwidth_Available_Number15_8 = (usThisAvailablePBN & 0xFF00) >> 8;
            ucCurrentDataCRC                                            = SIDEBANDUTIL_CalculateDataCRC(pucReplyBuff, ucBodyLen);
            *(pucReplyBuff + ucBodyLen)                                 = ucCurrentDataCRC;
        }

        eProcessingResult = ePROCESSED;

    } while (FALSE);

    return eProcessingResult;
}

// Bunch of notes about Allocate Payload. As per spec:
// Case 1: We update the VC Payload table of the downstream branch before forwarding the AllocPayload Sideband message to the downstream branch
// only if : 1) The stream ID is already allocated and we are increasing its current PBN. 2) We are allocating a totally new stream ID.
//
// Case 2: We update the VC Payload table of the downstream branch after forwarding the AllocPayload Sideband message to the downstream branch
// only if : 1) The stream ID is already allocated and we are decreasing its current PBN. 2) We are deleting a stream.
//
// We use pstBranchNode->stCurrentALlocPayloadData.bPostUpdateDownStreamTable flag to make this decision.
// Pre update (Case 1) is done in DP12TOPOLOGY_DownRequestHandlerThread while post update (Case 2) is done in DP12TOPOLOGY_PostProcessAndFowardDownStreamsReply
//
// If the Source gets a NAK for AllocatePayload for whatever reason (not enough available PBN etc), then it's source responsibility to send another
// Allocate Payload sideband message with Zero PBN to clear any allocated PBN along the path (some intial branches along a virtual channel may handle
// Allocate Payload successfully before a downstream Branch eventually fails it) so we want to clear allocation for branches that handled it successfully.
// After this as per spec the Source should also clear Payload table through native aux
PROCESSING_RESULT SIDEBANDMESSAGE_AllocatePayloadDownRequestHandler(PBRANCH_NODE pstBranchNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo, PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT  eProcessingResult  = ePROCESSING_ERROR;
    PMST_ALLOC_PAYLOAD pstAllocPayloadReq = NULL;
    USHORT             usNewPBN           = 0;
    UCHAR              ucStreamID         = 0;
    POUTPORT_ENTRY     pstOutportEntry    = NULL;
    UCHAR              ucOutportNum       = 0;
    ULONG              ulCount            = 0;

    ULONG ulTotalBodyLength = 0;

    USHORT  usCurrentAllocatedPBN = 0;
    BOOLEAN bSlotsAllocated       = FALSE;

    MST_RELATIVEADDRESS stTempRAD            = pstDwnReqBuffInfo->stHeaderInfo.stCurrentHeaderRAD;
    PPAYLOADTABLE_STATE pstPayloadTableState = &pstBranchNode->stBranchPayloadTableState;

    do
    {
        if (pstDwnReqBuffInfo->stHeaderInfo.bIsPathMsg == FALSE)
        {
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        pstAllocPayloadReq = (PMST_ALLOC_PAYLOAD)pstDwnReqBuffInfo->puchBuffPtr;

        usNewPBN   = (pstAllocPayloadReq->ucPBN8_15 << 8) | pstAllocPayloadReq->ucPBN0_7;
        ucStreamID = pstAllocPayloadReq->ucVCPID;

        for (ulCount = 0; ulCount < pstPayloadTableState->ulNumStreamsSlotsAllocated; ulCount++)
        {
            if (pstPayloadTableState->stPTEntryArray[ulCount].ucStreamID == ucStreamID)
            {
                bSlotsAllocated = TRUE;
                break;
            }
        }

        if (bSlotsAllocated == FALSE)
        {
            *peReasonForNak = eMST_ALLOCATE_FAIL;
            break;
        }

        if (pstDwnReqBuffInfo->stHeaderInfo.stCurrentHeaderRAD.ucRemainingLinkCount == 0)
        {
            ucOutportNum = (UCHAR)pstAllocPayloadReq->ucPortNumber;
        }
        else
        {
            ucOutportNum = SIDEBANDUTIL_DecRemainingLinkCountAndAdjustRAD(&stTempRAD);
        }

        if (ucOutportNum > MAX_PORTS_PER_BRANCH)
        {
            // Bad port number
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        pstOutportEntry = &pstBranchNode->stOutPortList[ucOutportNum];

        if (pstOutportEntry->bPortConnectedStatus == FALSE)
        {
            // Bad port number
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        // So Allocate Payload table should always come for an end Sink device(device indicated by the ucOutportNum of the Alloc message)
        // of display type. The only time it can be a device of Branch type is when the Branch is disconnected from the topology
        // via CSN.
        // In Below Case ucOutportNum = (UCHAR)pstAllocPayloadReq->ucPortNumber hence pstOutportEntry corresponds to pstAllocPayloadReq->ucPortNumber
        if (pstDwnReqBuffInfo->stHeaderInfo.stCurrentHeaderRAD.ucRemainingLinkCount == 0 && pstOutportEntry->eConnectedDeviceNodeType == eBRANCH)
        {
            // Bad port number
            *peReasonForNak = eMST_BAD_PARAM;
            ucOutportNum    = (UCHAR)pstAllocPayloadReq->ucPortNumber;
            break;
        }

        if (pstOutportEntry->ucStreamID != VCPLAYLOAD_STREAMID_INVALID && pstOutportEntry->ucStreamID != ucStreamID)
        {
            *peReasonForNak = eMST_ALLOCATE_FAIL;
            break;
        }

        usCurrentAllocatedPBN           = pstOutportEntry->usAllocatedPBN;
        pstOutportEntry->usAllocatedPBN = usNewPBN;
        pstOutportEntry->ucStreamID     = ucStreamID;

        if (usNewPBN)
        {
            if (pstOutportEntry->eConnectedDeviceNodeType == eBRANCH)
            {
                pstOutportEntry->stStreamRAD = stTempRAD;
            }
        }
        else
        {
            if (pstOutportEntry->eConnectedDeviceNodeType == eBRANCH)
            {
                // reset the RAD for Zero PBN
                memset(&pstOutportEntry->stStreamRAD, 0, sizeof(MST_RELATIVEADDRESS));
            }
            else
            {
                pstOutportEntry->usAllocatedPBN = 0;
                pstOutportEntry->ucStreamID     = VCPLAYLOAD_STREAMID_INVALID;
            }
        }

        pstOutportEntry->bPostUpdateDownStreamTable = usNewPBN < usCurrentAllocatedPBN ? TRUE : FALSE;

        // The payload table was not updated with the stream ID so no stream was found OR
        // Trying to allocate More PBN than available, hence fail
        if (usNewPBN > pstBranchNode->usCurrentAvailablePBN + usCurrentAllocatedPBN)
        {
            // Call Reply Function
            *peReasonForNak = eMST_ALLOCATE_FAIL;
            break;
        }

        pstBranchNode->usCurrentAvailablePBN = pstBranchNode->usCurrentAvailablePBN + usCurrentAllocatedPBN - usNewPBN;

        // Don't do anything if there was no PBN change
        if (usNewPBN == usCurrentAllocatedPBN)
        {
            // Call Reply Function
            eProcessingResult = ePROCESSED;
            break;
        }

        if (pstDwnReqBuffInfo->stHeaderInfo.stCurrentHeaderRAD.ucRemainingLinkCount != 0)
        {
            eProcessingResult = eDID_NOT_PROCESS;
            break;
        }

        eProcessingResult = ePROCESSED;

    } while (FALSE);

    if (eProcessingResult == ePROCESSED)
    {
        // Reusing the request buffer to compile the reply and finally will fill it in the downreply buffer
        ((PMST_ALLOC_PAYLOAD_REPLY)pstDwnReqBuffInfo->puchBuffPtr)->uczeros     = 0;
        ((PMST_ALLOC_PAYLOAD_REPLY)pstDwnReqBuffInfo->puchBuffPtr)->Port_Number = ucOutportNum;
        ((PMST_ALLOC_PAYLOAD_REPLY)pstDwnReqBuffInfo->puchBuffPtr)->zero        = 0;
        ((PMST_ALLOC_PAYLOAD_REPLY)pstDwnReqBuffInfo->puchBuffPtr)->ucVCPID     = ucStreamID;
        ((PMST_ALLOC_PAYLOAD_REPLY)pstDwnReqBuffInfo->puchBuffPtr)->ucPBN15_8   = (UCHAR)(usNewPBN >> 8);
        ((PMST_ALLOC_PAYLOAD_REPLY)pstDwnReqBuffInfo->puchBuffPtr)->ucPBN7_0    = (UCHAR)usNewPBN;

        ulTotalBodyLength += sizeof(MST_ALLOC_PAYLOAD_REPLY);

        pstDwnReqBuffInfo->ulFinalReplySize =
        SIDEBANDMESSAGE_PacketizeInto48ByteChunks(pstDwnReqBuffInfo->puchBuffPtr, ulTotalBodyLength, &pstBranchNode->stBranchRAD, TRUE, FALSE, 0);
    }

    return eProcessingResult;
}

PUPREQUEST_NODE_ENTRY SIDEBANDMESSAGE_ConnectionStatusNotifyUpRequestHandler(PBRANCH_NODE pstBranchConnectedToSrc, PBRANCH_NODE pstTargettedBranch, UCHAR ucPortNum)
{
    PROCESSING_RESULT     eProcessingResult = ePROCESSING_ERROR;
    PPORTINGLAYER_OBJ     pstPortingObj     = GetPortingObj();
    PUPREQUEST_NODE_ENTRY pstUpReqNodeEntry = NULL;
    do
    {
        if (pstBranchConnectedToSrc == NULL || pstTargettedBranch == NULL)
        {
            break;
        }

        // Port No. Sanity Check
        if (ucPortNum < pstTargettedBranch->ucTotalInputPorts || ucPortNum >= MAX_PORTS_PER_BRANCH)
        {
            break;
        }

        pstUpReqNodeEntry = pstPortingObj->pfnAllocateMem(sizeof(UPREQUEST_NODE_ENTRY), TRUE);

        // Create CSN Reply
        pstUpReqNodeEntry->stCSNRequestData.ucRequestId                 = eMST_CONNECTION_STATUS_NOTIFY;
        pstUpReqNodeEntry->stCSNRequestData.ucPortNumber                = ucPortNum;
        pstUpReqNodeEntry->stCSNRequestData.guid                        = pstTargettedBranch->uidBranchGUID;
        pstUpReqNodeEntry->stCSNRequestData.ucInputPort                 = 0;
        pstUpReqNodeEntry->stCSNRequestData.ucLegacy_Device_Plug_Status = 0;
        pstUpReqNodeEntry->stCSNRequestData.ucPeerDeviceType            = pstTargettedBranch->stOutPortList[ucPortNum].stConnectedDevicePeerType;

        if (pstTargettedBranch->stOutPortList[ucPortNum].eConnectedDeviceNodeType == eBRANCH)
        {
            pstUpReqNodeEntry->stCSNRequestData.ucMessaging_Capability_Status    = pstTargettedBranch->stOutPortList[ucPortNum].bConnectedDeviceMsgCapStatus;
            pstUpReqNodeEntry->stCSNRequestData.ucDisplayPort_Device_Plug_Status = pstTargettedBranch->stOutPortList[ucPortNum].bPortConnectedStatus;
        }
        else
        {
            pstUpReqNodeEntry->stCSNRequestData.ucDisplayPort_Device_Plug_Status = pstTargettedBranch->stOutPortList[ucPortNum].bPortConnectedStatus;
        }

        pstUpReqNodeEntry->ulUpRequestSize = sizeof(MST_CONNECTION_STATUS_NOTIFY_REQUEST);

        eProcessingResult = ePROCESSED;

    } while (FALSE);

    if (ePROCESSED != eProcessingResult)
    {
        if (pstUpReqNodeEntry)
        {
            pstPortingObj->pfnFreeMem(pstUpReqNodeEntry);
            pstUpReqNodeEntry = NULL;
        }
    }
    return pstUpReqNodeEntry;
}

//!!!Remote DPCD Read/Write COULD ACTUALLY BE DIRECTED AT MID BRANCHES ALSO SO THEY NOT EXACTLY SINK DIRECTED LIKE REMOTE I2C WHICH ALAWAYS
// HAVE TO BE DIRECTED AT END PANEL. SO THE  NAME GOT A BIT MISLEADING
// This is the common prehandler for Remote DPCD Read/Write and Remote I2C Read/Write as all these four sideband messages will
// need a common set of error checks before they can do their own message specific things
PROCESSING_RESULT SIDEBANDMESSAGE_SinkDirectedMsgsPreHandler(PBRANCH_NODE pstBranchNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo, PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT eProcessingResult = ePROCESSING_ERROR;
    UCHAR             ucPortNum         = DP_PORT_NA;

    do
    {

        if (pstDwnReqBuffInfo->stHeaderInfo.stCurrentHeaderRAD.ucRemainingLinkCount != 0)
        {
            // This branch is not supposed to process this Msg
            eProcessingResult = eDID_NOT_PROCESS;
            break;
        }

        if (pstDwnReqBuffInfo->stHeaderInfo.bIsPathMsg)
        {
            // Remote I2C Read Can't be a path message
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        // For Remote DPCD read/write and Remote I2C read/write, all of these messages First Req Msg byte = Request ID, Second Msg Req byte = DwnStream Port Num
        ucPortNum = (UCHAR)((PREMOTE_DPCD_I2C_RW_COMMON_HEADER_SIGNATURE)pstDwnReqBuffInfo->puchBuffPtr)->ucPortNumber;

        if (pstBranchNode->stOutPortList[ucPortNum].ucOutPortNumber == DP_PORT_NA)
        {
            // Got a RAD with end nibble that doesn't correspond to a valid port
            *peReasonForNak = eMST_INVALID_RAD;
            break;
        }

        if (pstBranchNode->stOutPortList[ucPortNum].bPortConnectedStatus == FALSE)
        {
            // If its a valid port that should should be plugged at it. That's how the current ADD NODE (branch or display) logic is
            *peReasonForNak = eMST_INVALID_RAD;
            break;
        }

        if (pstBranchNode->stOutPortList[ucPortNum].pvConnectedDeviceNodePointer == NULL || pstBranchNode->stOutPortList[ucPortNum].eConnectedDeviceNodeType == eBRANCH)
        {
            *peReasonForNak = eMST_INVALID_RAD;
            break;
        }

        // Now call the specfic Handler for the sink Directed Msgs like remoteI2C and remoteDPCD
        switch (pstDwnReqBuffInfo->ucCurrRequestID)
        {
        case eMST_REMOTE_DPCD_READ:
            eProcessingResult =
            SIDEBANDMESSAGE_RemoteDPCDReadDownRequestHandler(pstBranchNode, pstBranchNode->stOutPortList[ucPortNum].pvConnectedDeviceNodePointer,
                                                             pstBranchNode->stOutPortList[ucPortNum].eConnectedDeviceNodeType, pstDwnReqBuffInfo, peReasonForNak);

            break;

        case eMST_REMOTE_DPCD_WRITE:
            eProcessingResult =
            SIDEBANDMESSAGE_RemoteDPCDWriteDownRequestHandler(pstBranchNode, pstBranchNode->stOutPortList[ucPortNum].pvConnectedDeviceNodePointer,
                                                              pstBranchNode->stOutPortList[ucPortNum].eConnectedDeviceNodeType, pstDwnReqBuffInfo, peReasonForNak);
            break;

        case eMST_REMOTE_I2C_READ:
            eProcessingResult =
            SIDEBANDMESSAGE_RemoteI2CReadDownRequestHandler(pstBranchNode, pstBranchNode->stOutPortList[ucPortNum].pvConnectedDeviceNodePointer, pstDwnReqBuffInfo, peReasonForNak);
            break;

        case eMST_REMOTE_I2C_WRITE:
            eProcessingResult = SIDEBANDMESSAGE_RemoteI2CWriteDownRequestHandler(pstBranchNode, pstBranchNode->stOutPortList[ucPortNum].pvConnectedDeviceNodePointer,
                                                                                 pstDwnReqBuffInfo, peReasonForNak);
            break;
        }

    } while (FALSE);

    return eProcessingResult;
}

PROCESSING_RESULT SIDEBANDMESSAGE_RemoteDPCDReadDownRequestHandler(PBRANCH_NODE pstBranchNode, PVOID pvTargetNode, NODE_TYPE eNodeType, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo,
                                                                   PMST_REASON_FOR_NAK peReasonForNak)
{
    GFXVALSIM_FUNC_ENTRY();

    PROCESSING_RESULT              eProcessingResult      = ePROCESSING_ERROR;
    PMST_REMOTE_DPCD_READ_REPLY_ST pstRemoteDPCDReadReply = (PMST_REMOTE_DPCD_READ_REPLY_ST)pstDwnReqBuffInfo->puchBuffPtr;
    PUCHAR                         pucDPCDBuff            = NULL;
    ULONG                          ulDPCDSize             = 0;
    ULONG                          ulDPCDAddress          = ((PMST_REMOTE_DPCD_READ_ST)pstDwnReqBuffInfo->puchBuffPtr)->ulAddress7_0 |
                          ((PMST_REMOTE_DPCD_READ_ST)pstDwnReqBuffInfo->puchBuffPtr)->ulAddress15_8 << 8 |
                          ((PMST_REMOTE_DPCD_READ_ST)pstDwnReqBuffInfo->puchBuffPtr)->ulAddress19_16 << 16;

    UCHAR ucNumBytesToRead = ((PMST_REMOTE_DPCD_READ_ST)pstDwnReqBuffInfo->puchBuffPtr)->ucNumBytesRead;
    UCHAR ucPortNum        = ((PMST_REMOTE_DPCD_READ_ST)pstDwnReqBuffInfo->puchBuffPtr)->ucPortNumber;

    // Pre-Intialize NAK to Failure
    *peReasonForNak = eMST_DPCD_FAIL;

    if (eNodeType == eBRANCH)
    {
        pucDPCDBuff = ((PBRANCH_NODE)pvTargetNode)->stBranchDPCDMap.pucDPCDBuff;
        ulDPCDSize  = ((PBRANCH_NODE)pvTargetNode)->stBranchDPCDMap.ulDPCDBuffSize;
    }
    else
    {
        pucDPCDBuff = ((PDISPLAY_NODE)pvTargetNode)->stDisplayDPCDMap.pucDPCDBuff;
        ulDPCDSize  = ((PDISPLAY_NODE)pvTargetNode)->stDisplayDPCDMap.ulDPCDBuffSize;
    }

    if (ulDPCDAddress + ucNumBytesToRead <= ulDPCDSize)
    {
        pstRemoteDPCDReadReply->Port_Number          = ucPortNum;
        pstRemoteDPCDReadReply->Number_Of_Bytes_Read = ucNumBytesToRead;

        memcpy_s((pstDwnReqBuffInfo->puchBuffPtr + sizeof(MST_REMOTE_DPCD_READ_REPLY_ST)), ucNumBytesToRead, &pucDPCDBuff[ulDPCDAddress], ucNumBytesToRead);
        pstDwnReqBuffInfo->ulFinalReplySize = SIDEBANDMESSAGE_PacketizeInto48ByteChunks(pstDwnReqBuffInfo->puchBuffPtr, (sizeof(MST_REMOTE_DPCD_READ_REPLY_ST) + ucNumBytesToRead),
                                                                                        &pstBranchNode->stBranchRAD, FALSE, FALSE, 0);

        eProcessingResult = ePROCESSED;
    }

    GFXVALSIM_FUNC_EXIT(0);

    return eProcessingResult;
}

// Since we are a software only entity we'd never do NAK with partial write completed so not using the below partial write
// NAK condition in the code. We'd either return success or NAK the whole write with zero bytes indicated as written
// Below struct is taken from the spec for Partial write Naks
// REMOTE_DPCD__WRITE_Nak_Reply()
//{
//    Reply_Type
//        Request_Type
//        zeros
//        Port_Number
//        Reason_For_Nak
//        Number_Of_Bytes_Written_Before_Failure
//}
PROCESSING_RESULT SIDEBANDMESSAGE_RemoteDPCDWriteDownRequestHandler(PBRANCH_NODE pstBranchNode, PVOID pvTargetNode, NODE_TYPE eNodeType,
                                                                    PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo, PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT               eProcessingResult       = ePROCESSING_ERROR;
    PMST_REMOTE_DPCD_WRITE_REPLY_ST pstRemoteDPCDWriteReply = (PMST_REMOTE_DPCD_WRITE_REPLY_ST)pstDwnReqBuffInfo->puchBuffPtr;
    PUCHAR                          pucDPCDBuff             = NULL;
    ULONG                           ulDPCDSize              = 0;
    ULONG                           ulDPCDAddress           = ((PMST_REMOTE_DPCD_WRITE_ST)pstDwnReqBuffInfo->puchBuffPtr)->ulAddress7_0 |
                          ((PMST_REMOTE_DPCD_WRITE_ST)pstDwnReqBuffInfo->puchBuffPtr)->ulAddress15_8 << 8 |
                          ((PMST_REMOTE_DPCD_WRITE_ST)pstDwnReqBuffInfo->puchBuffPtr)->ulAddress19_16 << 16;

    ULONG ulNumBytesToWrite = ((PMST_REMOTE_DPCD_WRITE_ST)pstDwnReqBuffInfo->puchBuffPtr)->ucNumBytestoWrite;
    UCHAR ucPortNum         = ((PMST_REMOTE_DPCD_READ_ST)pstDwnReqBuffInfo->puchBuffPtr)->ucPortNumber;

    // Pre-Intialize NAK to Failure
    *peReasonForNak = eMST_DPCD_FAIL;

    if (eNodeType == eBRANCH)
    {
        pucDPCDBuff = ((PBRANCH_NODE)pvTargetNode)->stBranchDPCDMap.pucDPCDBuff;
        ulDPCDSize  = ((PBRANCH_NODE)pvTargetNode)->stBranchDPCDMap.ulDPCDBuffSize;
    }
    else
    {
        pucDPCDBuff = ((PDISPLAY_NODE)pvTargetNode)->stDisplayDPCDMap.pucDPCDBuff;
        ulDPCDSize  = ((PDISPLAY_NODE)pvTargetNode)->stDisplayDPCDMap.ulDPCDBuffSize;
    }

    pstRemoteDPCDWriteReply->Port_Number = ucPortNum;

    if (ulDPCDAddress + ulNumBytesToWrite <= ulDPCDSize)
    {
        memcpy_s(&pucDPCDBuff[ulDPCDAddress], ulNumBytesToWrite, (pstDwnReqBuffInfo->puchBuffPtr + sizeof(MST_REMOTE_DPCD_WRITE_ST)), ulNumBytesToWrite);
        pstRemoteDPCDWriteReply->Port_Number = ucPortNum;
        pstDwnReqBuffInfo->ulFinalReplySize =
        SIDEBANDMESSAGE_PacketizeInto48ByteChunks(pstDwnReqBuffInfo->puchBuffPtr, sizeof(MST_REMOTE_DPCD_WRITE_REPLY_ST), &pstBranchNode->stBranchRAD, FALSE, FALSE, 0);
        eProcessingResult = ePROCESSED;
    }

    return eProcessingResult;
}

PROCESSING_RESULT SIDEBANDMESSAGE_RemoteI2CReadDownRequestHandler(PBRANCH_NODE pstBranchNode, PDISPLAY_NODE pstDisplayNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo,
                                                                  PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT                eProcessingResult           = ePROCESSING_ERROR;
    PUCHAR                           pucTemp                     = pstDwnReqBuffInfo->puchBuffPtr;
    PMST_REMOTE_I2C_READ_ST1         pstRemoteI2CReadSt1         = (PMST_REMOTE_I2C_READ_ST1)pucTemp;
    PMST_REMOTE_I2C_READ_ST2         pstRemoteI2CReadSt2         = NULL;
    PMST_REMOTE_I2C_WRITEB4READ_HEAD pstRemoteI2CWriteB4ReadHead = NULL;

    ULONG ulCount = 0;

    pucTemp                     = pucTemp + sizeof(MST_REMOTE_I2C_READ_ST1);
    pstRemoteI2CWriteB4ReadHead = (PMST_REMOTE_I2C_WRITEB4READ_HEAD)pucTemp;

    for (ulCount = 0; ulCount < pstRemoteI2CReadSt1->ucNumOfI2CWriteTxn; ulCount++)
    {
        pucTemp = pucTemp + sizeof(MST_REMOTE_I2C_WRITEB4READ_HEAD) + ((PMST_REMOTE_I2C_WRITEB4READ_HEAD)pucTemp)->ucNumBytesToWrite + sizeof(MST_REMOTE_I2C_WRITEB4READ_BOTTOM);
    }

    pstRemoteI2CReadSt2 = (PMST_REMOTE_I2C_READ_ST2)pucTemp;

    // Currently we don't have any support any I2C slave address other than the EDID ones
    switch (pstRemoteI2CReadSt2->ucI2CAddress)
    {
    case I2C_EDID_SLAVE_ADDRESS:
        eProcessingResult = SIDEBANDMESSAGE_RemoteI2CReadEDIDHandler(pstBranchNode, pstDisplayNode, pstDwnReqBuffInfo, pstRemoteI2CReadSt1, pstRemoteI2CWriteB4ReadHead,
                                                                     pstRemoteI2CReadSt2, &pstDisplayNode->stDisplayEDIDI2CData, peReasonForNak);
        break;

    default:
        *peReasonForNak = eMST_I2C_NACK;
        break;
    }

    return eProcessingResult;
}

PROCESSING_RESULT SIDEBANDMESSAGE_RemoteI2CWriteDownRequestHandler(PBRANCH_NODE pstBranchNode, PDISPLAY_NODE pstDisplayNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo,
                                                                   PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT        eProcessingResult = ePROCESSING_ERROR;
    PMST_REMOTE_I2C_WRITE_ST pstRemoteI2CWrite = NULL;

    pstRemoteI2CWrite = (PMST_REMOTE_I2C_WRITE_ST)pstDwnReqBuffInfo->puchBuffPtr;

    // Currently we don't have any support any I2C slave address other than the EDID ones
    switch (pstRemoteI2CWrite->ucI2CAddress)
    {
    case I2C_EDID_SLAVE_ADDRESS:
    case I2C_EDID_SEGPTR_ADDRESS:
        eProcessingResult = SIDEBANDMESSAGE_RemoteI2CWriteEDIDHandler(pstBranchNode, pstDisplayNode, pstRemoteI2CWrite, &pstDisplayNode->stDisplayEDIDI2CData, peReasonForNak);
        break;

    default:
        *peReasonForNak = eMST_I2C_NACK;
        break;
    }

    return eProcessingResult;
}

PROCESSING_RESULT SIDEBANDMESSAGE_RemoteI2CReadEDIDHandler(PBRANCH_NODE pstBranchNode, PDISPLAY_NODE pstDisplayNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo,
                                                           PMST_REMOTE_I2C_READ_ST1 pstRemoteI2CReadSt1, PMST_REMOTE_I2C_WRITEB4READ_HEAD pstRemoteI2CWriteB4ReadHead,
                                                           PMST_REMOTE_I2C_READ_ST2 pstRemoteI2CReadSt2, PEDID_I2C_DATA pstEDIDI2CData, PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT eProcessingResult = ePROCESSING_ERROR;
    BOOLEAN           bRet              = TRUE;
    ULONG             ulCount           = 0;
    PUCHAR            pucEDIDBlock      = NULL;
    ULONG             ulTotalBodySize   = 0;
    UCHAR             ucTempBytesToRead = 0;
    UCHAR             ucTempPortNum     = 0;
    PUCHAR            pucTemp           = (PUCHAR)pstRemoteI2CWriteB4ReadHead;

    do
    {
        for (ulCount = 0; ulCount < pstRemoteI2CReadSt1->ucNumOfI2CWriteTxn; ulCount++)
        {
            if (pstRemoteI2CWriteB4ReadHead->ucNumBytesToWrite != 1)
            {
                bRet = FALSE;
                break;
            }

            if (pstRemoteI2CWriteB4ReadHead->ucI2CAddress == I2C_EDID_SEGPTR_ADDRESS)
            {
                pstEDIDI2CData->ucLastSegmentPtr = *((PUCHAR)(pstRemoteI2CWriteB4ReadHead + 1));
            }

            if (pstRemoteI2CWriteB4ReadHead->ucI2CAddress == I2C_EDID_SLAVE_ADDRESS)
            {
                if (pstEDIDI2CData->ucLastWriteAddress == I2C_EDID_SLAVE_ADDRESS && ulCount == 0)
                {
                    pstEDIDI2CData->ucLastSegmentPtr = I2C_EDID_DEFAULT_SEGPTR;
                }

                pstEDIDI2CData->ucLastWriteAddress = (UCHAR)pstRemoteI2CWriteB4ReadHead->ucI2CAddress;
                pstEDIDI2CData->ucBlockByteOffset  = *((PUCHAR)(pstRemoteI2CWriteB4ReadHead + 1));
            }

            pucTemp =
            pucTemp + sizeof(MST_REMOTE_I2C_WRITEB4READ_HEAD) + ((PMST_REMOTE_I2C_WRITEB4READ_HEAD)pucTemp)->ucNumBytesToWrite + sizeof(MST_REMOTE_I2C_WRITEB4READ_BOTTOM);
            pstRemoteI2CWriteB4ReadHead = (PMST_REMOTE_I2C_WRITEB4READ_HEAD)pucTemp;
        }

        if (bRet == FALSE || pstEDIDI2CData->ucLastWriteAddress != I2C_EDID_SLAVE_ADDRESS || pstRemoteI2CReadSt2->ucI2CAddress != I2C_EDID_SLAVE_ADDRESS)
        {
            *peReasonForNak = eMST_I2C_NACK;
            break;
        }

        // We have stored EDID in such a way that each block has 256 bytes data corresponding to a seg ptr value
        // So the byte offset from where to start reading and read length should not go beyond the block
        if ((pstEDIDI2CData->ucBlockByteOffset + pstRemoteI2CReadSt2->ucNumBytesToRead) > 2 * SIZE_EDID_BLOCK)
        {
            *peReasonForNak = eMST_I2C_NACK;
            break;
        }

        // Array bound + Sanity check
        if (pstEDIDI2CData->ucLastSegmentPtr >= pstDisplayNode->pstDisplayEDID->ulNumEDIDBlocks)
        {
            *peReasonForNak = eMST_I2C_NACK;
            break;
        }

        pucEDIDBlock = pstDisplayNode->pstDisplayEDID->pucEDIDBlocks[pstEDIDI2CData->ucLastSegmentPtr];

        // Now create EDID reply Data

        pucTemp = pstDwnReqBuffInfo->puchBuffPtr;

        // Jump past first byte of request ID
        pucTemp++;
        ulTotalBodySize++;

        // Make a local copy of the Port Num and ucNumBytesToRead before you start clobbering the data. Since we use the Same DownReq buffer with the original request to populate
        // the response too
        ucTempPortNum     = pstRemoteI2CReadSt1->ucPortNumber;
        ucTempBytesToRead = pstRemoteI2CReadSt2->ucNumBytesToRead;

        ((PMST_REMOTE_I2C_READ_REPLY_ST)pucTemp)->Port_Number          = ucTempPortNum;
        ((PMST_REMOTE_I2C_READ_REPLY_ST)pucTemp)->uczeros              = 0;
        ((PMST_REMOTE_I2C_READ_REPLY_ST)pucTemp)->Number_Of_Bytes_Read = ucTempBytesToRead;

        pucTemp = pucTemp + sizeof(MST_REMOTE_I2C_READ_REPLY_ST);
        ulTotalBodySize += sizeof(MST_REMOTE_I2C_READ_REPLY_ST);

        memcpy_s(pucTemp, ucTempBytesToRead, (pucEDIDBlock + pstEDIDI2CData->ucBlockByteOffset), ucTempBytesToRead);

        ulTotalBodySize += ucTempBytesToRead;

        pstDwnReqBuffInfo->ulFinalReplySize =
        SIDEBANDMESSAGE_PacketizeInto48ByteChunks(pstDwnReqBuffInfo->puchBuffPtr, ulTotalBodySize, &pstBranchNode->stBranchRAD, FALSE, FALSE, 0);

        eProcessingResult = ePROCESSED;

    } while (FALSE);

    return eProcessingResult;
}

PROCESSING_RESULT SIDEBANDMESSAGE_RemoteI2CWriteEDIDHandler(PBRANCH_NODE pstBranchNode, PDISPLAY_NODE pstDisplayNode, PMST_REMOTE_I2C_WRITE_ST pstRemoteI2CWrite,
                                                            PEDID_I2C_DATA pstEDIDI2CData, PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT eProcessingResult = ePROCESSING_ERROR;

    do
    {
        // For EDID read addresses, write size should always be one:
        // 1Byte Block offset for 0x50 Edid I2C slave address and 0x30 for Segment pointer offset
        if (pstRemoteI2CWrite->ucNumBytesToWrite != 1)
        {
            *peReasonForNak = eMST_I2C_NACK;
            break;
        }

        if (pstRemoteI2CWrite->ucI2CAddress == I2C_EDID_SEGPTR_ADDRESS)
        {
            pstEDIDI2CData->ucLastSegmentPtr = *((PUCHAR)(pstRemoteI2CWrite + sizeof(MST_REMOTE_I2C_WRITE_ST)));
        }

        // After Writing Segment pointer at 0x30, the next write should be Slave Address Write with byte offset between 0 to 0xFF
        // into a 256byte EDID block. This should be followed by a read at 0x50.
        // If we get another Write at 0x50 again instead of the above expected read then we should reset the segment pointer.
        // This is my understanding
        if (pstRemoteI2CWrite->ucI2CAddress == I2C_EDID_SLAVE_ADDRESS)
        {

            if (pstEDIDI2CData->ucLastWriteAddress == I2C_EDID_SLAVE_ADDRESS)
            {
                pstEDIDI2CData->ucLastSegmentPtr = I2C_EDID_DEFAULT_SEGPTR;
            }

            pstEDIDI2CData->ucBlockByteOffset = *((PUCHAR)(pstRemoteI2CWrite + sizeof(MST_REMOTE_I2C_WRITE_ST)));
        }

        pstEDIDI2CData->ucLastWriteAddress = (UCHAR)pstRemoteI2CWrite->ucI2CAddress;

        eProcessingResult = ePROCESSED;

    } while (FALSE);

    return eProcessingResult;
}

// This function appends header with appropriate header field values at the end of every 48Byte chunk in accordance with Sideband Protocol
// 48byte chunk = Header + BodyData + BodyDataCRC
// How does this work: Data already present in the passed buffer filled by the caller. So create header, move data to create space for header
// + dataCRC, copy header in the created space, check if we'll need another 48bytes chunk because there's still some data left. If so repeat
// the whole thing
ULONG SIDEBANDMESSAGE_PacketizeInto48ByteChunks(PUCHAR puchDataBuff, ULONG ulBodyLength, PMST_RELATIVEADDRESS pstRAD, BOOLEAN bPathMsg, BOOLEAN bBroadCast, UCHAR ucSeqNo)
{
    BOOLEAN bRet = TRUE;
    BOOLEAN bSMT = TRUE;
    BOOLEAN bEMT = TRUE;

    UCHAR ucHeaderSize       = 0;
    UCHAR ucCurrentBodyLen   = 0;
    ULONG ulRemainingBodyLen = 0;
    UCHAR ucCurrentHeaderCRC = 0;
    UCHAR ucCurrentDataCRC   = 0;
    UCHAR ucSpaceForData     = 0;

    ULONG ulTemp = 0;

    ULONG  ulOffset         = 0;
    ULONG  ulTotalReplySize = 0;
    PUCHAR pucSource        = NULL;
    PUCHAR pucDestination   = NULL;

    do
    {
        if (puchDataBuff == NULL || pstRAD == NULL)
        {
            bRet = FALSE;
            break;
        }

        // Add one byte for CRC

        ucHeaderSize   = MST_SBM_STATIC_HEADER_SIZE + pstRAD->ucRadSize;
        ucSpaceForData = MST_MAX_SBM_CHUNK_SIZE - (ucHeaderSize + sizeof(UCHAR));

        ulRemainingBodyLen = ulBodyLength;

        while (ulRemainingBodyLen)
        {
            // Create Space for Header. No divide by zero possible because of static header size
            ulTemp = CEIL_DIVIDE(ulRemainingBodyLen, MST_MAX_SBM_CHUNK_SIZE);

            // Start copying at the back making room for header in the front
            while (ulTemp)
            {
                pucDestination = (puchDataBuff + ulOffset) + MST_MAX_SBM_CHUNK_SIZE * ulTemp;
                ulTemp--;
                pucSource = (puchDataBuff + ulOffset) + MST_MAX_SBM_CHUNK_SIZE * ulTemp;

                memcpy_s(pucDestination, MST_MAX_SBM_CHUNK_SIZE, pucSource, MST_MAX_SBM_CHUNK_SIZE);
            }

            // Find out how much data is going in current  48byte chunk
            // ucCurrentBodyLen would always be less than 48bytes and fit in UCHAR hence the typecaste
            ucCurrentBodyLen = (UCHAR)min(ulRemainingBodyLen, ucSpaceForData); // sizeof(UCHAR) = 1 CRC byte itself

            ulTemp = CEIL_DIVIDE(ulRemainingBodyLen, ucCurrentBodyLen);

            pucDestination = puchDataBuff + ucHeaderSize + ulOffset;

            ULONG ulCopyOffset = ucSpaceForData + sizeof(UCHAR);

            while (ulTemp--)
            {
                pucSource = (puchDataBuff + ucHeaderSize + ulOffset) + ulCopyOffset;
                memcpy_s(pucDestination, ucCurrentBodyLen, pucSource, ucCurrentBodyLen);
                pucDestination = pucSource;
                ulCopyOffset += ucCurrentBodyLen;
            }

            // Find out how much data is remaining. If it remains we would need further 48byte chunks
            ulRemainingBodyLen = ulRemainingBodyLen - ucCurrentBodyLen;

            bEMT = !ulRemainingBodyLen;

            // Now for this chunk one header worth of space is created. Copy header data in that space

            ((PMST_SIDEBAND_HEADER_TOP)(puchDataBuff + ulOffset))->Link_Count_Total     = pstRAD->ucTotalLinkCount;
            ((PMST_SIDEBAND_HEADER_TOP)(puchDataBuff + ulOffset))->Link_Count_Remaining = pstRAD->ucRemainingLinkCount;

            ulOffset += sizeof(MST_SIDEBAND_HEADER_TOP);

            if (pstRAD->ucRadSize)
            {
                memcpy_s((puchDataBuff + ulOffset), pstRAD->ucRadSize, pstRAD->ucAddress, pstRAD->ucRadSize);
                ulOffset += pstRAD->ucRadSize;
            }

            ((PMST_SIDEBAND_HEADER_BOTTOM)(puchDataBuff + ulOffset))->ucZero                   = 0;
            ((PMST_SIDEBAND_HEADER_BOTTOM)(puchDataBuff + ulOffset))->SMT                      = bSMT;
            ((PMST_SIDEBAND_HEADER_BOTTOM)(puchDataBuff + ulOffset))->EMT                      = bEMT;
            ((PMST_SIDEBAND_HEADER_BOTTOM)(puchDataBuff + ulOffset))->Broadcast_Message        = bBroadCast;
            ((PMST_SIDEBAND_HEADER_BOTTOM)(puchDataBuff + ulOffset))->Path_Message             = bPathMsg;
            ((PMST_SIDEBAND_HEADER_BOTTOM)(puchDataBuff + ulOffset))->Message_Sequence_No      = ucSeqNo;
            ((PMST_SIDEBAND_HEADER_BOTTOM)(puchDataBuff + ulOffset))->SideBand_MSG_Body_Length = ucCurrentBodyLen + sizeof(UCHAR); // Bodylength includes one byte of CRC

            ucCurrentHeaderCRC = SIDEBANDUTIL_CalculateHeaderCRC(puchDataBuff, (2 * ucHeaderSize - 1));

            ((PMST_SIDEBAND_HEADER_BOTTOM)(puchDataBuff + ulOffset))->Sideband_MSG_Header_CRC = ucCurrentHeaderCRC;

            ulOffset += sizeof(MST_SIDEBAND_HEADER_BOTTOM);

            ucCurrentDataCRC = SIDEBANDUTIL_CalculateDataCRC((puchDataBuff + ulOffset), ucCurrentBodyLen);

            ulOffset += ucCurrentBodyLen;

            *(puchDataBuff + ulOffset) = ucCurrentDataCRC;

            ulOffset++;

            puchDataBuff += ulOffset;
            ulTotalReplySize += ulOffset;

            ulOffset = 0;

            bSMT = FALSE;
            // One Chunk Done!
        }

    } while (FALSE);

    return ulTotalReplySize; // This will be final reply size
}

// Keeping this function here instead of MSTTopology.c because this function is not should not be needed outside this
// file
BOOLEAN SIDEBANDMESSAGE_GetNodePBN(PVOID pvNode, NODE_TYPE eNodeType, PUSHORT pusFullPBN, PUSHORT pusAvailablePBN)
{
    BOOLEAN       bRet           = FALSE;
    PBRANCH_NODE  pstBranchNode  = NULL;
    PDISPLAY_NODE pstDisplayNode = NULL;

    *pusFullPBN      = 0;
    *pusAvailablePBN = 0;

    do
    {
        if (pvNode == NULL || (eNodeType != eBRANCH && eNodeType != eDISPLAY))
        {
            break;
        }

        if (eNodeType == eBRANCH)
        {
            pstBranchNode    = (PBRANCH_NODE)pvNode;
            *pusFullPBN      = pstBranchNode->usTotalAvailablePBN;
            *pusAvailablePBN = pstBranchNode->usCurrentAvailablePBN;
        }
        else
        {
            pstDisplayNode   = (PDISPLAY_NODE)pvNode;
            *pusFullPBN      = pstDisplayNode->usTotalAvailablePBN;
            *pusAvailablePBN = pstDisplayNode->usCurrentAvailablePBN;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN SIDEBANDMESSAGE_GetFECPathInfo(PVOID pvNode, NODE_TYPE eNodeType, PUCHAR ucFECPathInfo)
{
    BOOLEAN       bRet           = FALSE;
    PBRANCH_NODE  pstBranchNode  = NULL;
    PDISPLAY_NODE pstDisplayNode = NULL;

    *ucFECPathInfo = FALSE;

    do
    {
        if (pvNode == NULL || (eNodeType != eBRANCH && eNodeType != eDISPLAY))
        {
            break;
        }

        if (eNodeType == eBRANCH)
        {
            pstBranchNode  = (PBRANCH_NODE)pvNode;
            *ucFECPathInfo = pstBranchNode->ucFECPathInfo;
        }
        else
        {
            pstDisplayNode = (PDISPLAY_NODE)pvNode;
            *ucFECPathInfo = pstDisplayNode->ucFECPathInfo;
        }

    } while (FALSE);

    return bRet;
}

/* Handler to handle Power Up Phy requests from Gfx Driver as a part of SetMode*/
PROCESSING_RESULT SIDEBANDMESSAGE_PowerUpPhyDownRequestHandler(PBRANCH_NODE pstBranchNode, PMST_DWNREQUEST_BUFF_INFO pstDwnReqBuffInfo, PMST_REASON_FOR_NAK peReasonForNak)
{
    PROCESSING_RESULT            eProcessingResult  = ePROCESSING_ERROR;
    PMST_POWER_UP_DOWN_PHY       pstPowerUpPhyReq   = NULL;
    PMST_POWER_UP_DOWN_PHY_REPLY pstPowerUpPhyReply = NULL;
    PMST_REPLY_DATA              pstMSTReplyData    = NULL;
    POUTPORT_ENTRY               pstOutportEntry    = NULL;
    UCHAR                        ucOutportNum       = 0;
    ULONG                        ulTotalBodyLength  = 0;
    do
    {
        pstPowerUpPhyReq = (PMST_POWER_UP_DOWN_PHY)pstDwnReqBuffInfo->puchBuffPtr;
        pstMSTReplyData  = (PMST_REPLY_DATA)pstDwnReqBuffInfo->puchBuffPtr;

        ucOutportNum = (UCHAR)pstPowerUpPhyReq->ucPortNumber;

        if (ucOutportNum > MAX_PORTS_PER_BRANCH)
        {
            // Bad port number
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        pstOutportEntry = &pstBranchNode->stOutPortList[ucOutportNum];

        if (pstOutportEntry->bPortConnectedStatus == FALSE)
        {
            // Bad port number
            *peReasonForNak = eMST_BAD_PARAM;
            break;
        }

        pstMSTReplyData->bReplyType  = eAUX_ACK;
        pstMSTReplyData->ucRequestID = eMST_POWER_UP_PHY;

        pstPowerUpPhyReply = (PMST_POWER_UP_DOWN_PHY_REPLY)(pstDwnReqBuffInfo->puchBuffPtr + sizeof(MST_REPLY_DATA));

        pstPowerUpPhyReply->ucZeros       = 0;
        pstPowerUpPhyReply->ucPort_Number = ucOutportNum;

        ulTotalBodyLength += sizeof(MST_REPLY_DATA);
        ulTotalBodyLength += sizeof(MST_POWER_UP_DOWN_PHY_REPLY);

        pstDwnReqBuffInfo->ulFinalReplySize =
        SIDEBANDMESSAGE_PacketizeInto48ByteChunks(pstDwnReqBuffInfo->puchBuffPtr, ulTotalBodyLength, &pstBranchNode->stBranchRAD, TRUE, FALSE, 0);

        eProcessingResult = ePROCESSED;

    } while (FALSE);

    return eProcessingResult;
}

PROCESSING_RESULT SIDEBANDMESSAGE_PowerUpPhyDownReplyHandler(PBRANCH_NODE pstBranchNode, PUCHAR pucReplyBuff, UCHAR ucHeaderSize)
{
    PROCESSING_RESULT eProcessingResult = ePROCESSING_ERROR;

    PMST_POWER_UP_DOWN_PHY_REPLY pstPowerUpPhyReply = NULL;

    do
    {
        pucReplyBuff += ucHeaderSize + sizeof(UCHAR);
        pstPowerUpPhyReply = (PMST_POWER_UP_DOWN_PHY_REPLY)pucReplyBuff;

        eProcessingResult = ePROCESSED;
    } while (FALSE);

    return eProcessingResult;
}
