
#include "SidebandUtil.h"
#include "MSTTopology.h"

BOOLEAN SIDEBANDUTIL_ExtractAndValidateSideBandMessage(PBRANCH_NODE pstBranchNode, PSBM_CURRENT_HEADER_INFO pstCurrHeaderInfo, PUCHAR pucClientWriteBuff,
                                                       ULONG ulCurrTransactionAddr, ULONG ulCurrAuxTranLen, PUCHAR pucDwnReqOrUpReplyBuff, PULONG pulCurrentWriteLength,
                                                       PMST_NAK_REPLY_INFO pstNakInfoEntry, ULONG ulSideBandStartOffset)
{
    BOOLEAN bRet = FALSE;
    // SidebandHeader Related
    BOOLEAN             bSMT                  = FALSE;
    BOOLEAN             bEMT                  = FALSE;
    BOOLEAN             bPathMsg              = FALSE;
    BOOLEAN             bBroadcastMsg         = FALSE;
    UCHAR               ucSeqNo               = 0;
    UCHAR               ucCurrentHeaderCRC    = 0;
    UCHAR               ucCurrentBodySize     = 0;
    UCHAR               ucCurrentRadSize      = 0;
    UCHAR               ucCalculatedHeaderCRC = 0;
    MST_RELATIVEADDRESS stCurrentRad          = { 0 };
    pstNakInfoEntry->pGuid                    = &pstBranchNode->uidBranchGUID;
    pstNakInfoEntry->bIsNak                   = FALSE;

    do
    {

        if (pstNakInfoEntry == NULL)
        {
            // ASSERT
        }

        // Caustion: If Msg Headersays source will write Message Body size number of before starting a new header
        // But starts writing a new header before writing promised number of body size bytes then we have no way
        // to find that out. We would decode any subsequent bytes as header after receiving body size number of bytes
        // Things would get ugly but this should be easy to debug Total body size in header info combined with currentwrite length

        memcpy_s(&pucDwnReqOrUpReplyBuff[*pulCurrentWriteLength], ulCurrAuxTranLen, pucClientWriteBuff, ulCurrAuxTranLen);

        *pulCurrentWriteLength = *pulCurrentWriteLength + ulCurrAuxTranLen;

        // If current write length becomes higher than the total body length till now means we just got a new header
        if (*pulCurrentWriteLength > pstCurrHeaderInfo->ulTotalBodySize)
        {

            // We are here that means atleast one byte was written into the down request buffer
            // One byte is enough to find the Header length cuz all we need is TotalLinkCount
            if (!pstCurrHeaderInfo->ucCurrentHeaderSize)
            {
                // Get the header size
                bRet = SIDEBANDUTIL_DecodeSidebandHeader(&pucDwnReqOrUpReplyBuff[pstCurrHeaderInfo->ulTotalBodySize], &pstCurrHeaderInfo->ucCurrentHeaderSize, NULL, NULL, NULL,
                                                         NULL, NULL, NULL, NULL, NULL, NULL);
                if (!bRet)
                {
                    pstNakInfoEntry->bIsNak  = TRUE;
                    pstNakInfoEntry->eReason = eMST_BAD_PARAM;
                    break;
                }
            }

            if ((*pulCurrentWriteLength - pstCurrHeaderInfo->ulTotalBodySize) < pstCurrHeaderInfo->ucCurrentHeaderSize)
            {
                // Not enough bytes have still been received to decode the current header at one go
                // Continue till we get the all the header bytes
                // And We would AUX-ACK this Aux transaction
                break;
            }

            // Now we got all the header bytes. Lets decode the header
            bRet = SIDEBANDUTIL_DecodeSidebandHeader(&pucDwnReqOrUpReplyBuff[pstCurrHeaderInfo->ulTotalBodySize], NULL, &ucCurrentBodySize, &ucCurrentRadSize, &stCurrentRad, &bSMT,
                                                     &bEMT, &bPathMsg, &bBroadcastMsg, &ucSeqNo, &ucCurrentHeaderCRC);

            if (!bRet)
            {
                // Unknown Error
                break;
            }

            if (pstCurrHeaderInfo->IsSMTReceived && bSMT)
            {
                // Another SMT reveived in further 48byte chunk header
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_BAD_PARAM;
                break;
            }

            pstCurrHeaderInfo->IsSMTReceived = bSMT;

            if (pstCurrHeaderInfo->IsSMTReceived == FALSE && bEMT)
            {
                // EMT received without SMT
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_BAD_PARAM;
                break;
            }

            pstCurrHeaderInfo->IsEMTReceived = bEMT;

            pstCurrHeaderInfo->bIsPathMsg      = bPathMsg;
            pstCurrHeaderInfo->bIsBroadcastMsg = bBroadcastMsg;

            if (ulSideBandStartOffset == MST_DPCD_DOWN_REQ_START && !pstBranchNode->pfnCheckSeqNumValidity(pstBranchNode, ucSeqNo))
            {
                // Only In case of DownRequest:
                // Someone tried to Write a new message with same seq no or some garbage into the down Request buffer while we were
                // still processing the previous message. Spec doesn't allow this hence nack and ABORT!
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_BAD_PARAM;
                break;
            }

            ucCalculatedHeaderCRC = SIDEBANDUTIL_CalculateHeaderCRC(&pucDwnReqOrUpReplyBuff[pstCurrHeaderInfo->ulTotalBodySize], (2 * pstCurrHeaderInfo->ucCurrentHeaderSize - 1));

            if (ucCurrentHeaderCRC != ucCalculatedHeaderCRC)
            {
                // CRC Mismatch!!!
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_CRC_FAILURE;
                break;
            }

            // Sizeof UCHAR is for DataCRC Byte
            if ((pstCurrHeaderInfo->ucCurrentHeaderSize + ucCurrentBodySize) > MST_MAX_SBM_CHUNK_SIZE)
            {
                // As per spec source has to break down any request more than 48 bytes into chunks of 48 bytes
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_BAD_PARAM;
            }

            if (((pstCurrHeaderInfo->ucCurrentHeaderSize + ucCurrentBodySize) < MST_MAX_SBM_CHUNK_SIZE) && !bEMT)
            {
                // Is Source trying to send another header with data without using the full spec defined capacity
                // of the current chunk. Source can only do so if this is the last chunk in which case it should
                // set EMT.
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_BAD_PARAM;
                break;
            }

            if ((ULONG)(pstCurrHeaderInfo->ucCurrentHeaderSize + ucCurrentBodySize) > (MST_SBM_BUFF_SIZE - pstCurrHeaderInfo->ulTotalBodySize))
            {
                // Bad Message size. return NACK. Or we could ultimate not reply to this message and timeout
                // But I think NACK here itself is better for debugging. This NACK would for the last chunk of header written by
                // the source
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_BAD_PARAM;
                break;
            }

            // This implementation assumes that a source always write a fresh Down Requeststarts at MST_DPCD_DOWN_REQ_START (or MST_DPCD_UP_REPLY_START)
            // and not at some MST_DPCD_DOWN_REQ_START + x DPCD. Not sure if the spec supports this implicitely
            if (bSMT == TRUE && ((ulCurrTransactionAddr - *pulCurrentWriteLength) > ulSideBandStartOffset))
            {
                // Source started a new message at some address MST_DPCD_DOWN_REQ_START + offset. We don't support this
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_BAD_PARAM;
                break;
            }

            if ((pstCurrHeaderInfo->ulTotalBodySize == 0) && (bSMT == FALSE))
            {
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_BAD_PARAM;
                break;
            }

            if (!bSMT)
            {
                // Any subsequent headers after the SMT should have the same RAD as
                // the SMT one
                if (!memcmp(&pstCurrHeaderInfo->stCurrentHeaderRAD, &stCurrentRad, sizeof(MST_RELATIVEADDRESS)))
                {
                    pstNakInfoEntry->bIsNak  = TRUE;
                    pstNakInfoEntry->eReason = eMST_BAD_PARAM;
                    break;
                }
            }

            if (bSMT)
            {
                memcpy_s(&pstCurrHeaderInfo->stCurrentHeaderRAD, sizeof(MST_RELATIVEADDRESS), &stCurrentRad, sizeof(MST_RELATIVEADDRESS));
            }

            pstCurrHeaderInfo->ulTotalBodySize = pstCurrHeaderInfo->ulTotalBodySize + ucCurrentBodySize + pstCurrHeaderInfo->ucCurrentHeaderSize;
        }

    } while (FALSE);

    if (pstNakInfoEntry->bIsNak == FALSE && pstCurrHeaderInfo->IsEMTReceived)
    {
        // Eventually the total write length of this message at this point (minus all the headers) should be equal
        // to the number of bytes of body data in the message or its an error
        if (*pulCurrentWriteLength > pstCurrHeaderInfo->ulTotalBodySize)
        {
            // CurrentWriteLength can never increase total bodysize
            pstNakInfoEntry->bIsNak  = TRUE;
            pstNakInfoEntry->eReason = eMST_BAD_PARAM;
        }

        if (*pulCurrentWriteLength == pstCurrHeaderInfo->ulTotalBodySize)
        {

            // Lets De-headerize the request buffer and check for Data CRC's of all 48byte chunks in the request message

            if (!SIDEBANDUTIL_DeHeaderizeDataAndDataCRCCheck(pucDwnReqOrUpReplyBuff, &pstCurrHeaderInfo->ulTotalBodySize, pstCurrHeaderInfo->ucCurrentHeaderSize))
            {
                // CurrentWriteLength can never increase total bodysize
                pstNakInfoEntry->bIsNak  = TRUE;
                pstNakInfoEntry->eReason = eMST_BAD_PARAM;
            }
        }
    }

    return !pstNakInfoEntry->bIsNak;
}

// Imp: This byte returns the bodylength from header + CRC Byte as the final body length
BOOLEAN SIDEBANDUTIL_DecodeSidebandHeader(PUCHAR pucBuff, PUCHAR pucHeaderSize, PUCHAR pucCurrentBodyLength, PUCHAR pucCurrentRadSize, PMST_RELATIVEADDRESS pstCurrentRAD,
                                          PBOOLEAN pbSMT, PBOOLEAN pbEMT, PBOOLEAN pbPathMsg, PBOOLEAN pbBroadcastMsg, PUCHAR pucSeqNo, PUCHAR pucCRC)
{
    BOOLEAN                     bRet      = FALSE;
    UCHAR                       ucHDRSize = MST_MSG_STATIC_HEADER_SIZE, ucRADSize = 0;
    PMST_SIDEBAND_HEADER_TOP    pstSBMHeaderTop    = NULL;
    PMST_SIDEBAND_HEADER_BOTTOM pstSBMHeaderBottom = NULL;

    do
    {
        if (pucBuff == NULL)
        {
            // invalid args !!
            break;
        }

        pstSBMHeaderTop = (PMST_SIDEBAND_HEADER_TOP)pucBuff;

        // read header top

        if (pstCurrentRAD)
        {
            pstCurrentRAD->ucTotalLinkCount     = (UCHAR)pstSBMHeaderTop->Link_Count_Total;
            pstCurrentRAD->ucRemainingLinkCount = (UCHAR)pstSBMHeaderTop->Link_Count_Remaining;
        }

        if (pstSBMHeaderTop->Link_Count_Total > 1)
        {
            ucRADSize = (UCHAR)(pstSBMHeaderTop->Link_Count_Total) / 2;
            if (ucRADSize > MSTMAX_BYTES_RAD)
            {
                // invalid RAD
                break;
            }

            if (pstCurrentRAD)
            {
                memcpy_s(pstCurrentRAD->ucAddress, ucRADSize, pucBuff + sizeof(MST_SIDEBAND_HEADER_TOP), ucRADSize);
                pstCurrentRAD->ucRadSize = ucRADSize;
            }
        }

        // read header bottom
        pstSBMHeaderBottom = (PMST_SIDEBAND_HEADER_BOTTOM)(pucBuff + sizeof(MST_SIDEBAND_HEADER_TOP) + ucRADSize);

        ucHDRSize = sizeof(MST_SIDEBAND_HEADER_TOP) + ucRADSize + sizeof(MST_SIDEBAND_HEADER_BOTTOM);

        if (pucHeaderSize)
        {
            *pucHeaderSize = ucHDRSize;
        }

        if (pucCurrentBodyLength)
        {
            // Body length contains 1 byte of data CRC in the end
            // So essentially data length = pstSBMHeaderBottom->SideBand_MSG_Body_Length -1
            *pucCurrentBodyLength = (UCHAR)pstSBMHeaderBottom->SideBand_MSG_Body_Length;
        }

        if (pucCurrentRadSize)
        {
            *pucCurrentRadSize = ucRADSize;
        }

        if (pbSMT)
        {
            *pbSMT = (BOOLEAN)pstSBMHeaderBottom->SMT;
        }

        if (pbEMT)
        {
            *pbEMT = (BOOLEAN)pstSBMHeaderBottom->EMT;
        }

        if (pbPathMsg)
        {
            *pbPathMsg = (BOOLEAN)pstSBMHeaderBottom->Path_Message;
        }

        if (pbBroadcastMsg)
        {
            *pbBroadcastMsg = (BOOLEAN)pstSBMHeaderBottom->Broadcast_Message;
        }

        if (pucCRC)
        {
            *pucCRC = (UCHAR)pstSBMHeaderBottom->Sideband_MSG_Header_CRC;
        }

        if (pucSeqNo)
        {
            *pucSeqNo = (UCHAR)pstSBMHeaderBottom->Message_Sequence_No;
        }
        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

// Returns the first nibble as Port No.
UCHAR SIDEBANDUTIL_DecRemainingLinkCountAndAdjustRAD(PMST_RELATIVEADDRESS pstRAD)
{
    UCHAR         ucPortNo          = DP_PORT_NA;
    UCHAR         ucNumRadBytes     = 0;
    PMST_RAD_BYTE pstRadByte        = NULL;
    PMST_RAD_BYTE pstRadBytePlusOne = NULL;
    UCHAR         ucTemp            = 0;

    do
    {
        if (pstRAD->ucRemainingLinkCount == 0)
        {
            // Caller shouldn't be calling us if Remaining Count was already zero
            break;
        }

        ucTemp = pstRAD->ucRemainingLinkCount;

        // Leaving the last byte
        ucNumRadBytes = (pstRAD->ucRemainingLinkCount + 1) / 2;

        pstRadByte        = (PMST_RAD_BYTE)pstRAD->ucAddress;
        pstRadBytePlusOne = pstRadByte + 1;

        ucPortNo = (UCHAR)pstRadByte->RadNibbles.HigherRAD;

        while (ucNumRadBytes)
        {
            pstRadByte->RadNibbles.HigherRAD = pstRadByte->RadNibbles.LowerRAD;
            pstRadByte->RadNibbles.LowerRAD  = pstRadBytePlusOne->RadNibbles.HigherRAD;

            pstRadByte++;
            pstRadBytePlusOne++;

            ucNumRadBytes--;
        }

        pstRAD->ucRemainingLinkCount--;

    } while (FALSE);

    return ucPortNo;
}
///////////////////////////////////////////////
// Calculate Header CRC
// Taken from Snippet in VESA DP 1.2 spec,
// Section: 2.11.3.1.9 Sideband_MSG_Header_CRC
///////////////////////////////////////////////
UCHAR SIDEBANDUTIL_CalculateHeaderCRC(const PUCHAR pucData, int iNoOfNibbles)
{
    UCHAR BitMask      = 0x80;
    UCHAR BitShift     = 7;
    UCHAR ArrayIndex   = 0;
    int   NumberOfBits = iNoOfNibbles * 4;
    UCHAR Remainder    = 0;

    while (NumberOfBits != 0)
    {
        NumberOfBits--;
        Remainder <<= 1;
        Remainder |= (pucData[ArrayIndex] & BitMask) >> BitShift;
        BitMask >>= 1;
        BitShift--;

        if (BitMask == 0)
        {
            BitMask  = 0x80;
            BitShift = 7;
            ArrayIndex++;
        }

        if ((Remainder & 0x10) == 0x10)
        {
            Remainder ^= 0x13;
        }
    }

    NumberOfBits = 4;

    while (NumberOfBits != 0)
    {
        NumberOfBits--;
        Remainder <<= 1;

        if ((Remainder & 0x10) != 0)
        {
            Remainder ^= 0x13;
        }
    }
    return Remainder;
}

UCHAR SIDEBANDUTIL_CalculateDataCRC(const PUCHAR pucData, int iNumDataBytes)
{
    UCHAR  BitMask      = 0x80;
    UCHAR  BitShift     = 7;
    UCHAR  ArrayIndex   = 0;
    USHORT NumberOfBits = (USHORT)iNumDataBytes * 8;
    USHORT Remainder    = 0;
    while (NumberOfBits != 0 && ArrayIndex < iNumDataBytes)
    {
        NumberOfBits--;
        Remainder <<= 1;
        Remainder |= (pucData[ArrayIndex] & BitMask) >> BitShift;
        BitMask >>= 1;
        BitShift--;
        if (BitMask == 0)
        {
            BitMask  = 0x80;
            BitShift = 7;
            ArrayIndex++;
        }

        if ((Remainder & 0x100) == 0x100)
        {
            Remainder ^= 0xD5;
        }
    }

    NumberOfBits = 8;
    while (NumberOfBits != 0)
    {
        NumberOfBits--;
        Remainder <<= 1;
        if ((Remainder & 0x100) != 0)
        {
            Remainder ^= 0xD5;
        }
    }
    return Remainder & 0xFF;
}

// The Data CRC is still embedded in the return Deheaderized buffer. Good to remove it other it would cause problems for
// Sidebandmessage Down Requests spanning multiple sideband 48byte chunks
// e.g in remote sideband I2C/DPCD write, if the data length exceeds 48bytes, we'd end up writing the CRC byte to the I2C
// or DPCD target too
// Removing the embedded Body CRCs too so that remote I2C/DPCD writes of more than 48 bytes can be processed more easily
//(The processing function doesn't have to take extra steps to remove data CRCs from the write Stream).
// All the sideband message structures used to typecast this buffer and get SBM data should thus exclude CRC in the end.
// e.g. the allocate_payload struct below notice that the ucCRC is commented with a //
/*
typedef struct _MST_ALLOC_PAYLOAD
{
    UCHAR ucRequestID;

    UCHAR ucNumSDPStreams : 4;
    UCHAR ucPortNumber : 4;


    UCHAR ucVCPID;

    UCHAR ucPBN8_15;
    UCHAR ucPBN0_7;

    //UCHAR ucCRC;

}MST_ALLOC_PAYLOAD, *PMST_ALLOC_PAYLOAD;
*/
BOOLEAN SIDEBANDUTIL_DeHeaderizeDataAndDataCRCCheck(PUCHAR pucDataBuff, PULONG pulTotalBodySize, UCHAR ucHeaderSize)
{

    BOOLEAN bRet                   = TRUE;
    ULONG   ulNumDataBytesPerChunk = 0;
    ULONG   ulNumTemp              = 0;
    ULONG   ulRemainingBodySize    = *pulTotalBodySize;
    UCHAR   ucCurrentDataCrc       = 0;
    UCHAR   ucChunkCount           = 0;

    *pulTotalBodySize = 0;

    do
    {
        ULONG ulCount          = 0;
        ulNumDataBytesPerChunk = min(ulRemainingBodySize, MST_MAX_SBM_CHUNK_SIZE) - ucHeaderSize;
        ulNumTemp              = CEIL_DIVIDE(ulNumDataBytesPerChunk, ucHeaderSize);

        while (ulCount != ulNumTemp)
        {
            ULONG uldataDestination = 0;
            ULONG uldataSource      = 0;
            uldataDestination       = *pulTotalBodySize + ulCount * ucHeaderSize;
            ulCount++;
            uldataSource = MST_MAX_SBM_CHUNK_SIZE * ucChunkCount + ulCount * ucHeaderSize;
            memcpy_s(&pucDataBuff[uldataDestination], ucHeaderSize, &pucDataBuff[uldataSource], ucHeaderSize);
        }

        ucCurrentDataCrc = SIDEBANDUTIL_CalculateDataCRC(&pucDataBuff[*pulTotalBodySize], ulNumDataBytesPerChunk - sizeof(UCHAR));

        *pulTotalBodySize += ulNumDataBytesPerChunk - sizeof(UCHAR);

        if (ucCurrentDataCrc != pucDataBuff[*pulTotalBodySize])
        {
            bRet = FALSE;
            break;
        }

        ulRemainingBodySize = ulRemainingBodySize - min(ulRemainingBodySize, MST_MAX_SBM_CHUNK_SIZE);

        ucChunkCount++;

    } while (ulRemainingBodySize);

    return bRet;
}