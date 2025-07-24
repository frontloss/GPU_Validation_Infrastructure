#ifndef __SIDEBANDMESSAGEHANDLERS_H__
#define __SIDEBANDMESSAGEHANDLERS_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "SidebandUtil.h"
#include "SST_MST_Common.h"

typedef enum _PROCESSING_RESULT
{
    eDID_NOT_PROCESS = 0,
    ePROCESSED,
    ePARTIALLY_PROCESSED, // Lol don't know what this means. Just keeping it as a placeholder
    ePROCESSING_ERROR

} PROCESSING_RESULT;

#pragma pack(1)

// below struct is not in direct relation to any of the Messages in DP1.2 spec.
// This is purely for ease of this Implementation as all four messages namely
// Remote DPCD Read/Write and Remote I2C Read/Write use this common signature for
// their first byte + next nibble (.i.e 4 bits to encode downstream sink port number).
// Will be using this in SIDEBANDMESSAGE_SinkDirectedMsgsPreHandler, the common
// pre-handler for all these 4 messages
typedef struct _REMOTE_DPCD_I2C_RW_COMMON_HEADER_SIGNATURE
{
    UCHAR ucRequestID;

    UCHAR ucDontCare : 4;

    UCHAR ucPortNumber : 4;

} REMOTE_DPCD_I2C_RW_COMMON_HEADER_SIGNATURE, *PREMOTE_DPCD_I2C_RW_COMMON_HEADER_SIGNATURE;

typedef struct _MST_LINK_ADDRESS_REPLY
{
    GUID guid;

    UCHAR ucPortNo : 4;
    UCHAR ucZeros : 4;
} MST_LINK_ADDRESS_REPLY_DATA, *PMST_LINK_ADDRESS_REPLY_DATA;

typedef struct _MST_LINK_ADDRESS_REPLY_PORT_DETAILS_0
{
    UCHAR ucPortNumber : 4;
    UCHAR ucPeerDeviceType : 3;
    UCHAR ucInputPort : 1;

    UCHAR ucZeros : 6;
    UCHAR ucDPDevicePlugStatus : 1;
    UCHAR ucMsgCapStatus : 1;

} MST_LINK_ADDRESS_INPUT_PORT_DETAILS, *PMST_LINK_ADDRESS_INPUT_PORT_DETAILS;

typedef struct _MST_LINK_ADDRESS_REPLY_PORT_DETAILS
{
    UCHAR ucPortNumber : 4;
    UCHAR ucPeerDeviceType : 3;
    UCHAR ucInputPort : 1;

    UCHAR ucZeros : 5;
    UCHAR ucLegacyDevicePlugStatus : 1;
    UCHAR ucDPDevicePlugStatus : 1;
    UCHAR ucMsgCapStatus : 1;

    UCHAR DPCDRev : 8;
    GUID  Peerguid;

    UCHAR ucNumSDPStreamSinks : 4;
    UCHAR ucNumSDPStreams : 4;
} MST_LINK_ADDRESS_OUTPORT_PORT_DETAILS, *PMST_LINK_ADDRESS_OUTPUT_PORT_DETAILS;

typedef struct _MST_LINK_ADDRESS_REPLY_PORT_DETAILS_CCS
{
    UCHAR ucPortNumber : 4;
    UCHAR ucPeerDeviceType : 3;
    UCHAR ucInputPort : 1;

    UCHAR ucCCSUpperSixBits : 6;
    UCHAR ucDPDevicePlugStatus : 1;
    UCHAR ucMsgCapStatus : 1;

    UCHAR ucCCSMiddleBits[15];

    UCHAR ucZeros : 5;
    UCHAR ucLegacyDevicePlugStatus : 1;
    UCHAR ucCCSLowestTwoBits : 2;

    UCHAR DPCDRev : 8;
    GUID  Peerguid;

    UCHAR ucNumSDPStreamSinks : 4;
    UCHAR ucNumSDPStreams : 4;
} MST_LINK_ADDRESS_REPLY_PORT_DETAILS_CCS, *PMST_LINK_ADDRESS_REPLY_PORT_DETAILS_CCS;

// 2 unsigned ints.
//.Request ID
// Port No.
typedef struct _MST_ENUM_PATH_RESOURCES
{
    UCHAR ucRequestID;

    UCHAR ucZero : 4;
    UCHAR ucPortNumber : 4;

    UCHAR ucCRC;
} MST_ENUM_PATH_RESOURCES, *PMST_ENUM_PATH_RESOURCES;

typedef struct _MST_ENUM_PATH_RESOURCES_REPLY
{
    UCHAR ucRequestID;
    UCHAR FEC_Capability : 1;
    UCHAR uczeros : 3;
    UCHAR Port_Number : 4;
    UCHAR Payload_Bandwidth_Full_Number15_8;
    UCHAR Payload_Bandwidth_Full_Number7_0;
    UCHAR Payload_Bandwidth_Available_Number15_8;
    UCHAR Payload_Bandwidth_Available_Number7_0;

} MST_ENUM_PATH_RESOURCES_REPLY, *PMST_ENUM_PATH_RESOURCES_REPLY;

typedef struct _MST_ALLOC_PAYLOAD
{
    UCHAR ucRequestID;

    UCHAR ucNumSDPStreams : 4;
    UCHAR ucPortNumber : 4;

    UCHAR ucVCPID;

    UCHAR ucPBN8_15;
    UCHAR ucPBN0_7;

    // UCHAR ucCRC;

} MST_ALLOC_PAYLOAD, *PMST_ALLOC_PAYLOAD;

typedef struct _MST_ALLOC_PAYLOAD_REPLY
{
    UCHAR ucRequestID;
    UCHAR uczeros : 4;
    UCHAR Port_Number : 4;
    UCHAR zero : 1;
    UCHAR ucVCPID : 7;
    UCHAR ucPBN15_8;
    UCHAR ucPBN7_0;

} MST_ALLOC_PAYLOAD_REPLY, *PMST_ALLOC_PAYLOAD_REPLY;

// 5 Bytes
// Request ID
// Port Number : 4 bits
// DPCD Address: 20 bits
// Num of Bytes to Read
typedef struct _MST_REMOTE_DPCD_READ_ST
{
    CHAR ucRequestID : 8;

    CHAR ulAddress19_16 : 4;
    CHAR ucPortNumber : 4;

    CHAR ulAddress15_8 : 8;
    CHAR ulAddress7_0 : 8;

    CHAR ucNumBytesRead : 8;
    CHAR ucCRC;

} MST_REMOTE_DPCD_READ_ST, *PMST_REMOTE_DPCD_READ_ST;

typedef struct _MST_REMOTE_DPCD_READ_REPLY_ST
{
    CHAR  ucRequestID : 8;
    UCHAR Port_Number : 4;
    UCHAR uczeros : 4;
    UCHAR Number_Of_Bytes_Read : 8;
    // Rest are pBuffer of the size Number_Of_Bytes_Read

} MST_REMOTE_DPCD_READ_REPLY_ST, *PMST_REMOTE_DPCD_READ_REPLY_ST;

typedef struct _MST_REMOTE_DPCD_WRITE_ST
{
    CHAR ucRequestID;

    CHAR ulAddress19_16 : 4;
    CHAR ucPortNumber : 4;

    CHAR ulAddress15_8 : 8;
    CHAR ulAddress7_0 : 8;

    CHAR ucNumBytestoWrite;

} MST_REMOTE_DPCD_WRITE_ST, *PMST_REMOTE_DPCD_WRITE_ST;

typedef struct _MST_REMOTE_DPCD_WRITE_REPLY_ST
{
    CHAR  ucRequestID;
    UCHAR uczeros : 8;
    UCHAR Port_Number : 8;

} MST_REMOTE_DPCD_WRITE_REPLY_ST, *PMST_REMOTE_DPCD_WRITE_REPLY_ST;

// 2 ints
// Request ID
// No of I2CTxn : 2 bits
// zeros        : 2
// Port Number  : 4 bits
typedef struct _MST_REMOTE_I2C_READ_ST1
{
    UCHAR ucRequestID;

    UCHAR ucNumOfI2CWriteTxn : 2;

    UCHAR ucZeros : 2;

    UCHAR ucPortNumber : 4;

} MST_REMOTE_I2C_READ_ST1, *PMST_REMOTE_I2C_READ_ST1;

typedef struct _MST_REMOTE_I2C_READ_ST2
{
    UCHAR ucI2CAddress : 7;
    UCHAR ucZero : 1;

    UCHAR ucNumBytesToRead;
    UCHAR ucCRC;
} MST_REMOTE_I2C_READ_ST2, *PMST_REMOTE_I2C_READ_ST2;

typedef struct __MST_REMOTE_I2C_WRITEB4READ_HEAD
{
    UCHAR ucI2CAddress : 7; // 7 Bit Address, for eg: EDID Read 0x50
    UCHAR ucZero : 1;

    UCHAR ucNumBytesToWrite;

} MST_REMOTE_I2C_WRITEB4READ_HEAD, *PMST_REMOTE_I2C_WRITEB4READ_HEAD;

typedef struct _MST_REMOTE_I2C_WRITEB4READ_BOTTOM
{
    UCHAR ucI2CTxnDelay : 4;
    UCHAR ucNoStopBit : 1;
    UCHAR ucZero2 : 3;

} MST_REMOTE_I2C_WRITEB4READ_BOTTOM, *PMST_REMOTE_I2C_WRITEB4READ_BOTTOM;

typedef struct _MST_REMOTE_I2C_READ_REPLY_ST
{
    UCHAR Port_Number : 4;
    UCHAR uczeros : 4;
    UCHAR Number_Of_Bytes_Read : 8;
    // Rest are pBuffer of the size Number_Of_Bytes_Read
} MST_REMOTE_I2C_READ_REPLY_ST, *PMST_REMOTE_I2C_READ_REPLY_ST;

// 5 Bytes
// Request ID
// Port Number : 4 bits
// DPCD Address: 20 bits
// Num of Bytes to Write
// Data to Write
typedef struct _MST_REMOTE_I2C_WRITE_ST
{
    UCHAR ucRequestID;

    UCHAR ucZeros : 4;
    UCHAR ucPortNumber : 4;

    UCHAR ucI2CAddress : 7; // 7 Bit Address, for eg: EDID Read 0x50
    UCHAR ucZero : 1;

    UCHAR ucNumBytesToWrite;

} MST_REMOTE_I2C_WRITE_ST, *PMST_REMOTE_I2C_WRITE_ST;

// 2 Bytes
// Request ID
// Port No
typedef struct _MST_POWER_UP_DOWN_PHY
{
    UCHAR ucRequestID;

    UCHAR ucZeros : 4;
    UCHAR ucPortNumber : 4;

    UCHAR CRC;
} MST_POWER_UP_DOWN_PHY, *PMST_POWER_UP_DOWN_PHY;

// PWR_UP_DOWN_PHY_REPLY
typedef struct _MST_POWER_UP_DOWN_PHY_REPLY
{
    UCHAR ucZeros : 4;
    UCHAR ucPort_Number : 4;
} MST_POWER_UP_DOWN_PHY_REPLY, *PMST_POWER_UP_DOWN_PHY_REPLY;

typedef struct _MST_CONNECTION_STATUS_NOTIFY_REQUEST
{
    UCHAR ucRequestId;
    UCHAR ucZeros : 4;
    UCHAR ucPortNumber : 4;

    GUID guid;

    UCHAR ucPeerDeviceType : 3;
    UCHAR ucInputPort : 1;
    UCHAR ucMessaging_Capability_Status : 1;
    UCHAR ucDisplayPort_Device_Plug_Status : 1;
    UCHAR ucLegacy_Device_Plug_Status : 1;
    UCHAR ucEndZero : 1;

} MST_CONNECTION_STATUS_NOTIFY_REQUEST, PMST_CONNECTION_STATUS_NOTIFY_REQUEST;

#pragma pack()

typedef struct _UPREQUEST_NODE_ENTRY
{
    DP_LIST_ENTRY ListEntry;
    ULONG         ulUpRequestSize;
    UCHAR         ucRequestID;
    PVOID         pstGfxAdapterInfo;
    ULONG         ulPortNum;

    union {
        MST_CONNECTION_STATUS_NOTIFY_REQUEST stCSNRequestData;
        // RSN_STRUCT
    };

} UPREQUEST_NODE_ENTRY, *PUPREQUEST_NODE_ENTRY;

PROCESSING_RESULT SIDEBANDMESSAGE_ClearPayloadIDDownRequestHandler(void *pstBranchNode, void *pstDwnReqBuffInfo, PMST_REASON_FOR_NAK peReasonForNak);

PROCESSING_RESULT SIDEBANDMESSAGE_ClearPayloadIDDownReplyHandler(void *pstBranchNode, UCHAR ucGeneratedEventPortNum, BOOLEAN bSeqNo);

PROCESSING_RESULT SIDEBANDMESSAGE_LinkAddressDownRequestHandler(void *pstBranchNode, void *pstDwnReqBuffInfo, enum _MST_REASON_FOR_NAK *peReasonForNak);

PROCESSING_RESULT SIDEBANDMESSAGE_EnumPathResourcesDownRequestHandler(void *pstBranchNode, void *pstDwnReqBuffInfo, enum _MST_REASON_FOR_NAK *peReasonForNak);

PROCESSING_RESULT SIDEBANDMESSAGE_EnumPathResourcesDownReplyHandler(void *pstBranchNode, PUCHAR pucReplyBuff, UCHAR ucHeaderSize);

PROCESSING_RESULT SIDEBANDMESSAGE_AllocatePayloadDownRequestHandler(void *pstBranchNode, void *pstDwnReqBuffInfo, enum _MST_REASON_FOR_NAK *peReasonForNak);

ULONG SIDEBANDMESSAGE_PacketizeInto48ByteChunks(PUCHAR puchDataBuff, ULONG ulBodyLength, PMST_RELATIVEADDRESS pstRAD, BOOLEAN bPathMsg, BOOLEAN bBroadCast, UCHAR ucSeqNo);

PROCESSING_RESULT SIDEBANDMESSAGE_SinkDirectedMsgsPreHandler(void *pstBranchNode, void *pstDwnReqBuffInfo, enum _MST_REASON_FOR_NAK *peReasonForNak);

PUPREQUEST_NODE_ENTRY SIDEBANDMESSAGE_ConnectionStatusNotifyUpRequestHandler(void *pstBranchConnectedToSrc, void *pstTargettedBranch, UCHAR ucPortNum);

PROCESSING_RESULT SIDEBANDMESSAGE_PowerUpPhyDownRequestHandler(void *pstBranchNode, void *pstDwnReqBuffInfo, enum _MST_REASON_FOR_NAK *peReasonForNak);

PROCESSING_RESULT SIDEBANDMESSAGE_PowerUpPhyDownReplyHandler(void *pstBranchNode, PUCHAR pucReplyBuff, UCHAR ucHeaderSize);

#endif // !__SIDEBANDMESSAGEHANDLERS_H__
