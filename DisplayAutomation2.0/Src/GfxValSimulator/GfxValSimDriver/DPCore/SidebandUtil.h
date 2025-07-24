#ifndef __SIDEBANDCOMMON_H__
#define __SIDEBANDCOMMON_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\DriverInterfaces\\DPCoreIOCTLCommonDefs.h"

// As every Address for a link requires 4 Bits, therefore total 14 links(MAX_LINK_COUNT - 1, since for 1st link RAD is not required) would require 56 bits.
// Hence total 7 Bytes
#define MST_MAX_LINK_COUNT 15
#define MSTMAX_BYTES_RAD ((MST_MAX_LINK_COUNT) / 2)
#define MST_MSG_STATIC_HEADER_SIZE 3

#define MST_SBM_BUFF_SIZE 0x300

#define MST_MAX_SBM_CHUNK_SIZE 48u

#define MST_REALISTIC_SBM_BUFF_SIZE (3 * MST_MAX_SBM_CHUNK_SIZE) // should be enough? Max needed for EDID : EDID is 128 bytes + 3 bytes static header size + 13 bytes for RAD

#define MST_SBM_STATIC_HEADER_SIZE 3

#define DP_PORT_NA 0xFF // Port not available

#define CEIL_DIVIDE(x, y) ((y * (x / y) < x) ? (x / y + 1) : (x / y))
#define FLOOR_DIVIDE(x, y) (x / y)

typedef enum _MST_REQ_ID_TYPE
{
    eMST_GET_MESSAGE_TRANSACTION_VERSION = 0x00,
    eMST_LINK_ADDRESS                    = 0x01, // PATH_MSG , BROADCAST_MSG = 0
    eMST_CONNECTION_STATUS_NOTIFY        = 0x02, // UPSTREAM_MSG
    eMST_ENUM_PATH_RESOURCES             = 0x10, // PATH_MSG = 1, BROADCAST_MSG = 0
    eMST_ALLOCATE_PAYLOAD                = 0x11, // PATH_MSG = 1, BROADCAST_MSG = 0
    eMST_QUERY_PAYLOAD                   = 0x12, // PATH_MSG = 1, BROADCAST_MSG = 0
    eMST_RESOURCE_STATUS_NOTIFY          = 0x13, // UPSTREAM_MSG
    eMST_CLEAR_PAYLOAD_ID_TABLE          = 0x14, // PATH_MSG = 1, BROADCAST_MSG = 1
    eMST_REMOTE_DPCD_READ                = 0x20, // PATH_MSG = 0, BROADCAST_MSG = 0
    eMST_REMOTE_DPCD_WRITE               = 0x21, // PATH_MSG = 0, BROADCAST_MSG = 0
    eMST_REMOTE_I2C_READ                 = 0x22, // PATH_MSG = 0, BROADCAST_MSG  =0
    eMST_REMOTE_I2C_WRITE                = 0x23, // PATH_MSG = 0, BROADCAST_MSG = 0
    eMST_POWER_UP_PHY                    = 0x24, // PATH_MSG = 1, BROADCAST_MSG = 0
    eMST_POWER_DOWN_PHY                  = 0x25, // PATH_MSG = 1, BROADCAST_MSG = 0
    eMST_SINK_EVENT_NOTIFY               = 0x30, // UPSTREAM_MSG,(Functionality Undefined)
    eMST_QUERY_STREAM_ENCRYPTION_STATUS  = 0x38, // Undefined.
    eMST_UNDEFINED                       = 0XFF
} MST_REQ_ID_TYPE;

typedef enum _MST_REASON_FOR_NAK
{
    eMST_INVALID       = 0,
    eMST_WRITE_FAILURE = 1,
    eMST_INVALID_RAD,
    eMST_CRC_FAILURE,
    eMST_BAD_PARAM,
    eMST_DEFER,
    eMST_LINK_FAILURE,
    eMST_NO_RESOURCES,
    eMST_DPCD_FAIL,
    eMST_I2C_NACK,
    eMST_ALLOCATE_FAIL

} MST_REASON_FOR_NAK,
*PMST_REASON_FOR_NAK;

typedef struct _SBM_CURRENT_HEADER_INFO
{
    BOOLEAN             IsSMTReceived;
    BOOLEAN             IsEMTReceived;
    UCHAR               ucCurrentHeaderSize;
    MST_RELATIVEADDRESS stCurrentHeaderRAD;
    ULONG               ulTotalBodySize;
    ULONG               ulSeqNumber;
    BOOLEAN             bIsPathMsg;
    BOOLEAN             bIsBroadcastMsg;

} SBM_CURRENT_HEADER_INFO, *PSBM_CURRENT_HEADER_INFO;

#pragma pack(1)

typedef struct _MST_NAK_REPLY_DATA
{
    UCHAR ucRequestID : 7;
    UCHAR bReplyType : 1;
    GUID  guid;
    UCHAR ucReasonForNak;
    UCHAR ucNAKData;

} MST_NAK_REPLY_DATA, *PMST_NAK_REPLY_DATA;

typedef struct __MST_REPLY_DATA
{
    UCHAR ucRequestID : 7;
    UCHAR bReplyType : 1;
} MST_REPLY_DATA, *PMST_REPLY_DATA;

typedef union _MST_RAD_BYTE {
    UCHAR ucData;
    struct
    {
        UCHAR LowerRAD : 4;
        UCHAR HigherRAD : 4;
    } RadNibbles;
} MST_RAD_BYTE, *PMST_RAD_BYTE;

typedef struct _MST_SIDEBAND_HEADER_TOP
{
    UCHAR Link_Count_Remaining : 4;
    UCHAR Link_Count_Total : 4;
} MST_SIDEBAND_HEADER_TOP, *PMST_SIDEBAND_HEADER_TOP;

typedef struct _MST_SIDEBAND_HEADER_BOTTOM
{
    UCHAR SideBand_MSG_Body_Length : 6;
    UCHAR Path_Message : 1;
    UCHAR Broadcast_Message : 1;

    UCHAR Sideband_MSG_Header_CRC : 4;
    UCHAR Message_Sequence_No : 1;
    UCHAR ucZero : 1;
    UCHAR EMT : 1;
    UCHAR SMT : 1;

} MST_SIDEBAND_HEADER_BOTTOM, *PMST_SIDEBAND_HEADER_BOTTOM;

typedef struct __MST_SIDEBAND_MSG_HEADER
{
    MST_SIDEBAND_HEADER_TOP    SBMSG_HEADER_TOP;
    UCHAR                      ucRelativeAddress[MAX_BYTES_RAD];
    MST_SIDEBAND_HEADER_BOTTOM SBMSG_HEADER_BOTTOM;

} MST_SIDEBAND_MSG_HEADER, *PMST_SIDEBAND_MSG_HEADER;

typedef enum _MST_MSG_TYPE
{
    eUpRequest   = 0,
    eUpReply     = 1,
    eDownRequest = 2,
    eDownReply   = 3

} MST_MSG_TYPE,
PMST_MSG_TYPE;

#pragma pack()

BOOLEAN SIDEBANDUTIL_ExtractAndValidateSideBandMessage(PVOID pstBranchNode, PSBM_CURRENT_HEADER_INFO pstCurrHeaderInfo, PUCHAR pucClientWriteBuff, ULONG ulCurrTransactionAddr,
                                                       ULONG ulCurrAuxTranLen, PUCHAR pucDwnReqOrUpReplyBuff, PULONG pulCurrentWriteLength, PVOID pstNakInfoEntry,
                                                       ULONG ulSideBandStartOffset);

BOOLEAN SIDEBANDUTIL_DecodeSidebandHeader(PUCHAR pucBuff, PUCHAR pucHeaderSize, PUCHAR pucCurrentBodyLength, PUCHAR pucCurrentRadSize, PMST_RELATIVEADDRESS pstCurrentRAD,
                                          PBOOLEAN pbSMT, PBOOLEAN pbEMT, PBOOLEAN pbPathMsg, PBOOLEAN pbBroadcastMsg, PUCHAR pucSeqNo, PUCHAR pucCRC);

UCHAR SIDEBANDUTIL_CalculateHeaderCRC(const PUCHAR pucData, int iNoOfNibbles);
UCHAR SIDEBANDUTIL_CalculateDataCRC(const PUCHAR pucData, int iNumDataBytes);
// Returns the first nibble as Port No.
UCHAR   SIDEBANDUTIL_DecRemainingLinkCountAndAdjustRAD(PMST_RELATIVEADDRESS pstRAD);
BOOLEAN SIDEBANDUTIL_DeHeaderizeDataAndDataCRCCheck(PUCHAR pucDataBuff, PULONG pulTotalBodySize, UCHAR ucHeaderSize);

#endif