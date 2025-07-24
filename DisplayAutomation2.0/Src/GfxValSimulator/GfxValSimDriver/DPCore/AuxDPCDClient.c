
#include "AuxDPCDClient.h"
#include "..\CommonInclude\ETWLogging.h"

// Dev note: Initially thought it to be a threaded call but now
// This won't be in a thread then but a direct call.
BOOLEAN AUXCLIENT_SideBandReadHandler(PDPCD_CLIENTINFO pDPCDClientInfo)
{
    PDP12_TOPOLOGY pstDP12Topology    = (PDP12_TOPOLOGY)pDPCDClientInfo->pvCallerPersistedContext;
    PBRANCH_NODE   pstBranchNode      = pstDP12Topology->pstBranchConnectedToSrc;
    PUCHAR         pucDownReplyBuff   = pstBranchNode->stDownReplyBuffInfo.puchBuffPtr;
    PUCHAR         pucUpReqBuff       = pstBranchNode->stUpRequestBuffInfo.puchUpReqBuffPtr;
    PUCHAR         pucPrimaryReadBuff = pDPCDClientInfo->ucPrimaryReadBuffer;
    ULONG          ulCurrReadLen      = pDPCDClientInfo->ucCurrTransactionLen;
    // Tell the caller(DataRegProcessor here) to send an ACK/NAK to the current Aux Transaction by setting bClientRet to TRUE or FALSE
    BOOLEAN bClientRet = TRUE;

    ULONG ulBuffOffset = 0;

    do
    {
        if ((pDPCDClientInfo->ulCurrTransactionAddr >= MST_DPCD_DOWN_REQ_START) && (pDPCDClientInfo->ulCurrTransactionAddr <= MST_DPCD_DOWN_REQ_END))
        {

            // Come to think about it we would need another thread for Read on this DPCD range cuz Read can come in parallel
            // Signal the thread
        }

        if ((pDPCDClientInfo->ulCurrTransactionAddr >= MST_DPCD_UP_REPLY_START) && (pDPCDClientInfo->ulCurrTransactionAddr <= MST_DPCD_UP_REPLY_END))
        {
            // Ack/Nack reply to CSN etc
        }

        if ((pDPCDClientInfo->ulCurrTransactionAddr >= MST_DPCD_DOWN_REP_START) && (pDPCDClientInfo->ulCurrTransactionAddr <= MST_DPCD_DOWN_REP_END))
        {
            ulBuffOffset = pDPCDClientInfo->ulCurrTransactionAddr - MST_DPCD_DOWN_REP_START;
            memcpy_s(pucPrimaryReadBuff, ulCurrReadLen, &pucDownReplyBuff[ulBuffOffset], ulCurrReadLen);
            break;
        }

        if ((pDPCDClientInfo->ulCurrTransactionAddr >= MST_DPCD_UP_REQ_START) && (pDPCDClientInfo->ulCurrTransactionAddr <= MST_DPCD_UP_REQ_END))
        {
            ulBuffOffset = pDPCDClientInfo->ulCurrTransactionAddr - MST_DPCD_UP_REQ_START;
            memcpy_s(pucPrimaryReadBuff, ulCurrReadLen, &pucUpReqBuff[ulBuffOffset], ulCurrReadLen);
            break;
        }

    } while (FALSE);

    return bClientRet;
}

// Current implementation will handle only sideband messages with Zero Seq No
// But creating a sort of placehholder for Seq No. 1 support enabling too
BOOLEAN AUXCLIENT_SideBandWriteHandler(PDPCD_CLIENTINFO pDPCDClientInfo)
{
    PPORTINGLAYER_OBJ         pstPortingObj      = GetPortingObj();
    PDP12_TOPOLOGY            pstDP12Topology    = (PDP12_TOPOLOGY)pDPCDClientInfo->pvCallerPersistedContext;
    PBRANCH_NODE              pstBranchNode      = NULL;
    PMST_DWNREQUEST_BUFF_INFO pstDownReqBuffInfo = NULL;
    PMST_UPREQUEST_BUFF_INFO  pstUpReqBuffInfo   = NULL;
    PMST_NAK_REPLY_INFO       pstNakInfoEntry    = NULL;

    BOOLEAN bClientRet = TRUE;

    if ((pDPCDClientInfo->ulDPCDStartAddress >= MST_DPCD_DOWN_REP_START) && (pDPCDClientInfo->ulDPCDStartAddress <= MST_DPCD_UP_REQ_END))
    {
        // The above address range is only Read only for source. NACK any Write access
        // pDPCDClientInfo->bClientResponse = FALSE here will lead to sending NACK
        bClientRet = FALSE;
    }

    do
    {
        if (pstDP12Topology == NULL)
        {
            break;
        }

        pstBranchNode = pstDP12Topology->pstBranchConnectedToSrc;

        if (pstBranchNode == NULL)
        {
            break;
        }

        if ((pDPCDClientInfo->ulCurrTransactionAddr >= MST_DPCD_DOWN_REQ_START) && (pDPCDClientInfo->ulCurrTransactionAddr <= MST_DPCD_DOWN_REQ_END))
        {

            do
            {
                pstNakInfoEntry = (PMST_NAK_REPLY_INFO)pstPortingObj->pfnGetEntryFromLookAsideList(&pstBranchNode->NakInfoLookAsideListHead);

                pstDownReqBuffInfo = pstBranchNode->pfnGetAvailableDownReqBuff(pstDP12Topology->pstBranchConnectedToSrc);

                if (pstDownReqBuffInfo == NULL)
                {
                    // No Resource Available Nack
                    pstNakInfoEntry->bIsNak  = TRUE;
                    pstNakInfoEntry->pGuid   = &pstBranchNode->uidBranchGUID;
                    pstNakInfoEntry->eReason = eMST_ALLOCATE_FAIL;
                    break;
                }

                SIDEBANDUTIL_ExtractAndValidateSideBandMessage(pstBranchNode, &pstDownReqBuffInfo->stHeaderInfo, pDPCDClientInfo->ucPrimaryWriteBuffer,
                                                               pDPCDClientInfo->ulCurrTransactionAddr, pDPCDClientInfo->ucCurrTransactionLen, pstDownReqBuffInfo->puchBuffPtr,
                                                               &pstDownReqBuffInfo->ulCurrWriteLength, pstNakInfoEntry, MST_DPCD_DOWN_REQ_START);

            } while (FALSE);

            if (pstNakInfoEntry->bIsNak == FALSE && pstDownReqBuffInfo->stHeaderInfo.IsEMTReceived)
            {

                // There was no NAK, return the Nak Entry back to lookaside list
                pstPortingObj->pfnReturnEntryToLookAsideList(&pstBranchNode->NakInfoLookAsideListHead, &pstNakInfoEntry->DPListEntry);

                // We need to set this buff state in with a lock acquired?
                // Since we are going to process this buffer for this request so we set it as in use
                // So that any new request with another sequence number to this node can't corrupt it
                pstBranchNode->pfnSetDownReqBuffState(pstBranchNode, pstDownReqBuffInfo->ucThisBuffIndex, eBuffInUse);

                pstPortingObj->pfnSetDPEvent(&pstDownReqBuffInfo->stBuffEvent, PRIORITY_NO_INCREMENT);
            }

            if (pstNakInfoEntry->bIsNak)
            {
                // Since we are returning NAK for this request so we can return the current down request buffer to the free pool
                pstBranchNode->pfnSetDownReqBuffState(pstBranchNode, pstDownReqBuffInfo->ucThisBuffIndex, eReturnToFreePool);
                pstPortingObj->pfnInterlockedInsertTailList(&pstBranchNode->NakInfoProcessingListHead, &pstNakInfoEntry->DPListEntry);
                pstPortingObj->pfnSetDPEvent(pstBranchNode->pstThisNodeNAKReplyEvent, PRIORITY_NO_INCREMENT);
            }
        }

        if ((pDPCDClientInfo->ulCurrTransactionAddr >= MST_DPCD_UP_REPLY_START) && (pDPCDClientInfo->ulCurrTransactionAddr <= MST_DPCD_UP_REPLY_END))
        {
            MST_NAK_REPLY_INFO stNakInfoEntry = { 0 };
            PMST_REPLY_DATA    pstReplyData   = NULL;
            pstUpReqBuffInfo                  = &pstBranchNode->stUpRequestBuffInfo;

            SIDEBANDUTIL_ExtractAndValidateSideBandMessage(pstBranchNode, &pstBranchNode->stUpReplyInfo.stHeaderInfo, pDPCDClientInfo->ucPrimaryWriteBuffer,
                                                           pDPCDClientInfo->ulCurrTransactionAddr, pDPCDClientInfo->ucCurrTransactionLen, pstBranchNode->stUpReplyInfo.puchBuffPtr,
                                                           &pstBranchNode->stUpReplyInfo.ulCurrWriteLength, &stNakInfoEntry, MST_DPCD_UP_REPLY_START);

            if (stNakInfoEntry.bIsNak == TRUE)
            {
                // ASSERT
                // Source Messed up something in the reply. Most probably the Header or Data CRC
            }
            else
            {
                // Check the ACK Reply from Source.
                // Expecting Source to First send ACK/NACK UpReply to the UpReq sent from the sink side
                // before clearing the UpReqRead Bit in the IRQ_VECTOR DPCD 0x201
                // If the source does so then we can be assured the pstUpReqBuffInfo->ucRequestID is equal to the current
                // UpReq ID. As soon as the UpReqRead Bit in the IRQ_VECTOR DPCD 0x201 is cleared, the current implementation
                // would try to service any pending UpReq from the app and the pstUpReqBuffInfo->ucRequestID might change
                // And not meet the pstReplyData->ucRequestID
                pstReplyData = (PMST_REPLY_DATA)pstBranchNode->stUpReplyInfo.puchBuffPtr;

                // 0 is sideband message ACK and 1 is NACK
                if (pstReplyData->bReplyType == 0 && pstReplyData->ucRequestID == pstUpReqBuffInfo->ucRequestID)
                {
                    // Successs
                }
                else
                {
                    //******************************PRINT ERROR MESSAGE*****************************************
                }
            }
        }

    } while (FALSE);
    // Tell the caller (DataRegProcessor here) to send an ACK to the current Aux Transaction by setting bClientResponse to TRUE
    return bClientRet;
}

BOOLEAN AUXCLIENT_ServiceIRQVectorRWHandler(PDPCD_CLIENTINFO pDPCDClientInfo)
{
    // Operations atomic at byte level

    BOOLEAN                bRet                  = TRUE;
    PUCHAR                 pucDPCDMap            = pDPCDClientInfo->pucClientDPCDMap;
    PPORTINGLAYER_OBJ      pstPortingObj         = GetPortingObj();
    PDP12_TOPOLOGY         pstDP12Topology       = (PDP12_TOPOLOGY)pDPCDClientInfo->pvCallerPersistedContext;
    PBRANCH_NODE           pstBranchNode         = pstDP12Topology->pstBranchConnectedToSrc;
    DPCDDEF_SPI_IRQ_VECTOR stSPIIRQEventsBefore  = { 0 };
    DPCDDEF_SPI_IRQ_VECTOR stSPIIRQEventsAfter   = { 0 };
    PULONG                 pulTotalDownReplySize = &pstBranchNode->stDownReplyBuffInfo.ulTotalReplySize;
    PULONG                 pulTotalUpRequestSize = &pstBranchNode->stUpRequestBuffInfo.ulTotalUpReqSize;

    do
    {
        if (pDPCDClientInfo->eAccessType == eRead)
        {
            *pDPCDClientInfo->ucPrimaryReadBuffer = pucDPCDMap[DPCD_SERVICE_IRQ_VECTOR];
        }
        else
        {
            // Read-Modify-Write IRQ Vector Within Spin Lock
            // Spin Lock Acquire
            pstPortingObj->pfnAcquireDPLock(&pstBranchNode->stServiceIRQVectorSpinLock);

            stSPIIRQEventsBefore.ucVal = pucDPCDMap[DPCD_SERVICE_IRQ_VECTOR];

            stSPIIRQEventsAfter.ucVal = pDPCDClientInfo->ucPrimaryWriteBuffer[0];

            // clear this branch's IRQ bits depending on What bits are 1 in the incomping write Byte.
            pucDPCDMap[DPCD_SERVICE_IRQ_VECTOR] = pucDPCDMap[DPCD_SERVICE_IRQ_VECTOR] ^ (pDPCDClientInfo->ucPrimaryWriteBuffer[0]);

            // Check if the Bit was reset and not already zero
            if (stSPIIRQEventsBefore.IRQVectorBits.bDownReplyMsgRdy && stSPIIRQEventsAfter.IRQVectorBits.bDownReplyMsgRdy)
            {

                // updating the down reply size variable incase the down reply size was more than MST_MAX_SBM_CHUNK_SIZE
                // Deduct the amount of data read by the upstream from the total reply size so that the
                // Downstream device knows how much data is still pending to be sent. Here it means the down stream reply thread would
                // left shift the remaining data by MST_MAX_SBM_CHUNK_SIZE
                *pulTotalDownReplySize = *pulTotalDownReplySize - min(*pulTotalDownReplySize, MST_MAX_SBM_CHUNK_SIZE);

                // Inform the downstream node that Reply buffer data has been read
                pstPortingObj->pfnSetDPEvent(&pstBranchNode->stUpReadDownReplyEvent, PRIORITY_NO_INCREMENT);
            }

            // Check if the Bit was reset and not already zero
            if (stSPIIRQEventsBefore.IRQVectorBits.bUpRequestMsgRdy && stSPIIRQEventsAfter.IRQVectorBits.bUpRequestMsgRdy)
            {
                // Deduct the amount of data read by the upstream from the total reply size so that the
                // Downstream device knows how much data is still pending to be sent
                *pulTotalUpRequestSize = *pulTotalUpRequestSize - min(*pulTotalUpRequestSize, MST_MAX_SBM_CHUNK_SIZE);

                // If there is UpReq data still left to be consumed (i.e total up req size > 48bytes), signal the uprequest handler
                // thread to move the next 48bytes to the front of the buffer and set UpReqReady Bit again
                if (*pulTotalUpRequestSize)
                {
                    pstPortingObj->pfnSetDPEvent(&pstBranchNode->stUpRequestEvent, PRIORITY_NO_INCREMENT);
                }
            }

            // Spin Lock Release
            pstPortingObj->pfnReleaseDPLock(&pstBranchNode->stServiceIRQVectorSpinLock);
        }
    } while (FALSE);

    return bRet;
}

// Try to minimise local variables and instructions in these critical paths
// Source can write past DPCD_VCPAYLOAD_NUM_SLOTS in a multibyte write
// But we need to trigger the VC Palyload update as soon as the DPCD_VCPAYLOAD_NUM_SLOTS DPCD is written
BOOLEAN AUXCLIENT_VCPayloadTableUpdateRWHandler(PDPCD_CLIENTINFO pDPCDClientInfo)
{
    BOOLEAN        bRet            = FALSE;
    ULONG          ulCount         = 0;
    PDP12_TOPOLOGY pstDP12Topology = (PDP12_TOPOLOGY)pDPCDClientInfo->pvCallerPersistedContext;
    PUCHAR         pucDPCDMap      = pDPCDClientInfo->pucClientDPCDMap;

    if (pDPCDClientInfo->eAccessType == eRead)
    {
        for (ulCount = 0; ulCount < pDPCDClientInfo->ucCurrTransactionLen; ulCount++)
        {
            *pDPCDClientInfo->ucPrimaryReadBuffer = pucDPCDMap[DPCD_VCPAYLOAD_ID + ulCount];
        }

        bRet = TRUE;
    }
    else
    {
        bRet = DP12TOPOLOGY_UpdateVCPayloadTable(pstDP12Topology->pstBranchConnectedToSrc, pDPCDClientInfo->ucPrimaryWriteBuffer,
                                                 pDPCDClientInfo->ulCurrTransactionAddr, pDPCDClientInfo->ucCurrTransactionLen);
    }

    return bRet;
}

BOOLEAN AUXCLIENT_VCPayloadTableStatusRWHandler(PDPCD_CLIENTINFO pDPCDClientInfo)
{
    BOOLEAN                             bRet                         = FALSE;
    PUCHAR                              pucDPCDMap                   = pDPCDClientInfo->pucClientDPCDMap;
    PDPCDDEF_PAYLOADTABLE_UPDATE_STATUS pstPayloadTableUpdateStatus  = (PDPCDDEF_PAYLOADTABLE_UPDATE_STATUS)&pucDPCDMap[DPCD_VCPAYLOAD_UPDATE_STATUS];
    PDPCDDEF_PAYLOADTABLE_UPDATE_STATUS pstPayloadTableUpdateStatus2 = NULL;

    if (pDPCDClientInfo->ucCurrTransactionLen == 1)
    {
        if (pDPCDClientInfo->eAccessType == eRead)
        {
            *pDPCDClientInfo->ucPrimaryReadBuffer = pucDPCDMap[DPCD_VCPAYLOAD_UPDATE_STATUS];

            // Setting ACT instantenously for now. We need to find a way to figure out when ACT is sent from the Source Side
            if (pstPayloadTableUpdateStatus->bPayloadTableUpdated)
            {
                pstPayloadTableUpdateStatus->bActHandled = 1;
            }
        }
        else
        {
            pstPayloadTableUpdateStatus2 = (PDPCDDEF_PAYLOADTABLE_UPDATE_STATUS)&pDPCDClientInfo->ucPrimaryReadBuffer[0];

            if (pstPayloadTableUpdateStatus->bPayloadTableUpdated == 1 && pstPayloadTableUpdateStatus2->bPayloadTableUpdated == 1)
            {
                pstPayloadTableUpdateStatus->bPayloadTableUpdated = 0;
            }
        }

        bRet = TRUE;
    }

    return bRet;
}

VOID AUXHELPER_GetReceiverCapability(PUCHAR pucDPCDBuff, PRECEIVER_CAPS pReceiverCaps)
{
    PDPCDEF_TRAINING_AUX_RD_INTERVAL regValue  = (PDPCDEF_TRAINING_AUX_RD_INTERVAL)&pucDPCDBuff[DPCD_TRAINING_AUX_RD_INTERVAL];
    UCHAR                            ucDPCDRev = eDPCDRev_Invalid;

    if (regValue->ucExtendedReceiverCapibilityFieldPresent)
    {
        ucDPCDRev = pucDPCDBuff[DPCD_REVISION_EXT];
        if (ucDPCDRev >= eDPCDRev_1_4 && ucDPCDRev < eDPCDRev_Max)
        {
            /* If extended receiver capability is supported and DP1.4+ then DPCD address is read through 0x2200-0x220F*/
            pReceiverCaps->eDPCDRev                   = pucDPCDBuff[DPCD_REVISION_EXT];
            pReceiverCaps->ulMaxLinkRateDPCDAddress   = DPCD_MAX_LINK_RATE_EXT;
            pReceiverCaps->ulMaxLaneCountDPCDAddress  = DPCD_MAX_LANE_COUNT_EXT;
            pReceiverCaps->ulMaxDownSpreadDPCDAddress = DPCD_MAX_DOWNSPREAD_EXT;

            return;
        }
        /* If extended receiver capability is supported and DPCD revision less than DP1.4 -> Invalid scenario as per spec*/
        GFXVALSIM_DBG_MSG("DPCD Spec violation: Extended receiver capability field enabled but DPCD Rev = %d\n", ucDPCDRev);
    }

    /* If extended receiver capability is not supported then defalut DPCD address is read through 0x00-0x0F*/
    pReceiverCaps->eDPCDRev                   = pucDPCDBuff[DPCD_REVISION];
    pReceiverCaps->ulMaxLinkRateDPCDAddress   = DPCD_MAX_LINK_RATE;
    pReceiverCaps->ulMaxLaneCountDPCDAddress  = DPCD_MAX_LANE_COUNT;
    pReceiverCaps->ulMaxDownSpreadDPCDAddress = DPCD_MAX_DOWNSPREAD;
}