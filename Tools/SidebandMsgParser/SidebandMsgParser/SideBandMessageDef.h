/*===========================================================================
; SideBandMessageDef.h - SideBandMessaging Interface Function Argument Definition Module
;----------------------------------------------------------------------------
;   Copyright (c) 2001-2010  Intel Corporation.
;   All Rights Reserved.  Copyright notice does not imply publication.
;   This software is protected as an unpublished work.  This software
;   contains the valuable trade secrets of Intel Corporation,
;   and must be maintained in confidence.
;
; File Description:
;   This file contains SideBandMessaging Interface Arguments Definition.
;
;--------------------------------------------------------------------------*/

#ifndef SIDEBANDMESSAGEDEF_H
#define SIDEBANDMESSAGEDEF_H

//#include "..\\inc\\DPInc\\GfxCommDPRoutines.h"

#define BUFFERID_SIZE 16
#define MAX_WAIT_TIMEOUT 4000000000 // 4 Seconds.
#define MAX_DPCD_WRITE_SIZE 16

#define UNINIT_PBNBW 0xFFFFFFFF

#define IS_PATH_MSG(ID) (( ID >= 0x10 && ID <= 0x12 ) || ( ID == 0x14 ) || (ID >= 0x24 && ID <= 0x25) )
#define IS_BROADCAST_MSG(ID) ((ID == 0x14) || (ID == 0x02) || (ID == 0x13))

#define EVENT_DP_TOPOLOGY 0x80000

#define GET_PORT_NUMBER(RAD) ((RAD.ucTotalLinkCount == 1) ? 0 : ((RAD.ucTotalLinkCount % 2 == 0) ? ((RAD.ucAddress[(RAD.ucTotalLinkCount/ 2) - 1] & 0xF0) >> 4) : (RAD.ucAddress[(RAD.ucTotalLinkCount / 2) - 1] & 0x0F)))

typedef enum _MESSAGE_TRANSACTION_VERSION_NUMBER
{
    Ver1Rev2a   = 0x1,
    Ver1Rev2b   = 0x2,
    Ver1Rev3    = 0x3
}MESSAGE_TRANSACTION_VERSION_NUMBER;

typedef enum _MSG_TYPE
{
    eUpRequest      = 0,
    eUpReply        = 1,
    eDownRequest    = 2,
    eDownReply      = 3
}MSG_TYPE;

#define SIDEBAND_MSG_STATIC_HEADER_CRC_NIBBLES 5       // Note: - This is the no of nibbles without CRC nibble itself. If theres non-zero RAD, that would be added into CRC calc also.
#define SIDEBAND_MSG_STATIC_HEADER_SIZE 3       // Note: - This is the no of bytes. If theres non-zero RAD, that should be added to size also.

#pragma pack(1)

typedef union _RAD_BYTE_ST
{
    BYTE ucData;
    struct
    {
        BYTE LowerRAD    : 4;
        BYTE HigherRAD   : 4;
    };
}RAD_BYTE_ST;


#define SIZE_OF_RAD(SBM_HEADER) ( (SBM_HEADER.SBMSG_HEADER_TOP.Link_Count_Total > 1) ? \
       ((SBM_HEADER.SBMSG_HEADER_TOP.Link_Count_Total) / 2) : 0)

#define SIZE_OF_MSG_HDR(SBM_HEADER) (SIDEBAND_MSG_STATIC_HEADER_SIZE + SIZE_OF_RAD(SBM_HEADER))

#define SIDEBAND_MSG_HEADER_CRC_NIBBLES(SBM_HEADER) (2 * SIZE_OF_MSG_HDR(SBM_HEADER) - 1)

// REQUEST DATA
// SIDE BAND MESSAGE DOWN REQUEST and UP REPLY DATA STRUCTURES.
// All Data must be byte aligned.

// Only Request ID is required, 1 Byte.
typedef struct _SB_LINK_ADDRESS_REQ_DATA
{
    BYTE ucRequestID;
    BYTE ucCRC;
}SB_LINK_ADDRESS_REQ_DATA;

// 2 Bytes.
//.Request ID 
// Port No.
typedef struct _SB_ENUM_PATH_RESOURCES_ST
{
    BYTE ucRequestID;

    BYTE ucZero        : 4 ;
    BYTE ucPortNumber  : 4;

    BYTE ucCRC;
}SB_ENUM_PATH_RESOURCES_ST;


// 6 Bytes
// Request ID
// Port No, Num SDP Streams
// VCPID
// PBN 2 bytes
// Stream Sink No
typedef struct _ALLOC_PAYLOAD_ST
{
    BYTE ucRequestID;

    BYTE ucNumSDPStreams       : 4;
    BYTE ucPortNumber          : 4;


    BYTE ucVCPID;

    BYTE ucPBN8_15;
    BYTE ucPBN0_7;


    // ****************************************************************
    // NOTE: The bits below are used to indicate Stream sink IDs, 
    //       if there are multiple SDP Streams on the same Sink.
    //       We are not planning to have a usage model to support multiple audio endpoints from one sink.
    // ***************************************************************
    //    BYTE ucSDPStreamSink        : 4;
    //    BYTE ucZero        : 4 ;
    BYTE ucCRC;
}ALLOC_PAYLOAD_ST;

// 3 bytes
// RequestID
// PortNumber
// VCPID
typedef struct _SB_QUERY_PAYLOAD_ST
{

    BYTE ucRequestID;

    BYTE ucPortNumber     : 4;
    const BYTE ucZero    : 4 ;

    BYTE ucVCPID;
    BYTE ucCRC;
}SB_QUERY_PAYLOAD_ST;


// 5 Bytes
// Request ID
// Port Number : 4 bits
// DPCD Address: 20 bits
// Num of Bytes to Read 
typedef struct _SB_REMOTE_DPCD_READ_ST
{
    BYTE ucRequestID    : 8;

    BYTE ulAddress19_16: 4;
    BYTE ucPortNumber  : 4; 

    BYTE ulAddress15_8 : 8;
    BYTE ulAddress7_0  : 8;

    BYTE ucNumBytesRead : 8;
    //    BYTE ucDPCDDataToRead; // (x ucNumBytesRead
    BYTE ucCRC;
}SB_REMOTE_DPCD_READ_ST;


// 5 Bytes
// Request ID
// Port Number : 4 bits
// DPCD Address: 20 bits
// Num of Bytes to Write
// Data to Write
typedef struct _SB_REMOTE_DPCD_WRITE_HEADER
{
    BYTE ucRequestID;

    BYTE ulAddress19_16: 4;
    BYTE ucPortNumber  : 4; 

    BYTE ulAddress15_8 : 8;
    BYTE ulAddress7_0  : 8;

    BYTE ucNumBytestoWrite;
}SB_REMOTE_DPCD_WRITE_HEADER, *PSB_REMOTE_DPCD_WRITE_HEADER;

typedef struct _SB_REMOTE_DPCD_WRITE_ST
{
    SB_REMOTE_DPCD_WRITE_HEADER stHeader;
    BYTE ucCRC;
}SB_REMOTE_DPCD_WRITE_ST;

typedef struct _I2C_READ_PKT
{
    BYTE ucI2CAddress  : 7; // 7 Bit Address, for eg: EDID Read 0x50
    BYTE ucZero        : 1 ;     

    BYTE ucNumBytesToWrite;

    BYTE byData;            // Note:- To Revisit this for implementation for MCCS, i.e generic I2C read / write

    BYTE ucI2CTxnDelay : 4;
    BYTE ucNoStopBit   : 1;
    BYTE ucZero2       : 3 ;     
}I2C_READ_PKT;



// 2 Bytes
// Request ID
// No of I2CTxn : 2 bits
// zeros        : 2 
// Port Number  : 4 bits
typedef struct _SB_REMOTE_I2C_READ_ST1
{
    BYTE ucRequestID;

    BYTE ucNumOfI2CTxn    : 2;
    BYTE ucZeros          : 2;

    BYTE ucPortNumber     : 4;       

}SB_REMOTE_I2C_READ_ST1;

typedef struct _SB_REMOTE_I2C_READ_ST2
{
    BYTE ucI2CAddress    : 7;
    BYTE ucZero          : 1 ;


    BYTE ucNumBytesToRead;
    BYTE ucCRC;
}SB_REMOTE_I2C_READ_ST2;


// 5 Bytes
// Request ID
// Port Number : 4 bits
// DPCD Address: 20 bits
// Num of Bytes to Write
// Data to Write
typedef struct _SB_REMOTE_I2C_WRITE_ST
{
    BYTE ucRequestID;

    BYTE ucZeros    : 4 ;
	BYTE ucPortNumber     : 4;

    BYTE ucI2CAddress    : 7; // 7 Bit Address, for eg: EDID Read 0x50
	BYTE ucZero    : 1 ;

    BYTE ucNumBytesToWrite;

}SB_REMOTE_I2C_WRITE_ST;


// 2 Bytes
// Request ID
// Port No
typedef struct _POWER_UP_DOWN_PHY_ST
{

    BYTE ucRequestID;

    BYTE ucZeros    :4 ;
    BYTE ucPortNumber    :4;

    BYTE ucCRC;
}POWER_UP_DOWN_PHY_ST;



// UP REQUEST EVENTS
typedef union _SB_SINK_EVENT_NOTIFY_ST
{
    BYTE ucData[6];
    struct
    {
        BYTE ucRequestID;

        const BYTE ucZeros    :4 ;
        BYTE ucLinkCount    :4;

    };

}SB_SINK_EVENT_NOTIFY_ST;


/****************************************************************************************************************************************************************
// REPLY DATA
// structures for SIDEBANDMESSAGE Replies
****************************************************************************************************************************************************************/

typedef enum _REASON_FOR_NAK
{
    WRITE_FAILURE                   = 0x01,         //Not Enough buffer space to store message transaction
    INVALID_RAD                     = 0x02,          //Invalid address including link count
    CRC_FAILURE                     = 0x03,          //Message Transaction CRC error
    BAD_PARAM                       = 0x04,          //Invalid request parameter
    DEFER                           = 0x05,          //Unable to process message within time-out period (defer)
    LINK_FAILURE                    = 0x06,          //Link failure
    NO_RESOURCES                    = 0x07,          //Not enough resources
    DPCD_FAIL                       = 0x08,          //DPCD access failure
    I2C_NAK                         = 0x09,          //I2C NAK received
    ALLOCATE_FAIL                   = 0x0A,          //SB_ALLOCATE_PAYLOAD request failure (not due to lack ofresources)
}REASON_FOR_NAK;

typedef struct _NAK_REPLY_DATA
{
    GUID guid;
    BYTE ucReasonForNak;
    BYTE ucNAKData;

}NAK_REPLY_DATA;

typedef struct _REPLY_DATA
{
    BYTE    ucRequestID            :7;
    BOOLEAN bReplyType             :1;
}REPLY_DATA;

typedef struct _UP_REQUEST_REPLY_DATA
{
    BYTE    ucRequestID            :7;
    BOOLEAN bReplyType             :1;
    BYTE    ucCRC;
}UP_REQUEST_REPLY_DATA;

typedef struct _SB_LINK_ADDRESS_REPLY_PORT_DETAILS_0
{
    BYTE ucPortNumber              :4;
    BYTE ucPeerDeviceType          :3;
    BYTE ucInputPort               :1;

    BYTE ucZeros                   :6;
    BYTE ucDPDevicePlugStatus      :1;
    BYTE ucMsgCapStatus            :1;

}SB_LINK_ADDRESS_REPLY_PORT_DETAILS_0;

typedef struct _SB_LINK_ADDRESS_REPLY_PORT_DETAILS
{
    BYTE ucPortNumber              :4;
    BYTE ucPeerDeviceType          :3;
    BYTE ucInputPort               :1;

    BYTE ucZeros                   :5;
    BYTE ucLegacyDevicePlugStatus  :1;
    BYTE ucDPDevicePlugStatus      :1;
    BYTE ucMsgCapStatus            :1;

    BYTE DPCDRev                   :8;
    GUID Peerguid;                   

    BYTE ucNumSDPStreamSinks       :4;
    BYTE ucNumSDPStreams           :4;
}SB_LINK_ADDRESS_REPLY_PORT_DETAILS;

typedef struct _SB_LINK_ADDRESS_REPLY_PORT_DETAILS_CCS
{
    BYTE ucPortNumber              :4;
    BYTE ucPeerDeviceType          :3;
    BYTE ucInputPort               :1;

    BYTE ucCCSUpperSixBits         :6;
    BYTE ucDPDevicePlugStatus      :1;
    BYTE ucMsgCapStatus            :1;

    BYTE ucCCSMiddleBits[15];

    BYTE ucZeros                   :5;
    BYTE ucLegacyDevicePlugStatus  :1;
    BYTE ucCCSLowestTwoBits        :2;

    BYTE DPCDRev                   :8;
    GUID Peerguid;                   

    BYTE ucNumSDPStreamSinks       :4;
    BYTE ucNumSDPStreams           :4;
}SB_LINK_ADDRESS_REPLY_PORT_DETAILS_CCS,*PSB_LINK_ADDRESS_REPLY_PORT_DETAILS_CCS;


typedef struct _MESSAGE_TRANSACTION_VERSION_REQUEST_DATA_ST
{
    BYTE ucRequestID;
    BYTE ucZeros:4;
    BYTE ucPortNumber:4;
    BYTE ucCrc;
}MESSAGE_TRANSACTION_VERSION_REQUEST_DATA_ST;

typedef struct _SB_LINK_ADDRESS_REPLY
{
    GUID guid;

    BYTE ucPortNo              :4;
    BYTE ucZeros               :4;
}SB_LINK_ADDRESS_REPLY_DATA;


typedef struct _SB_ENUM_PATH_RESOURCES_REPLY
{
    BYTE   uczeros                      :4;
    BYTE   Port_Number                  :4;
    BYTE   Payload_Bandwidth_Full_Number15_8;
    BYTE   Payload_Bandwidth_Full_Number7_0;
    BYTE   Payload_Bandwidth_Available_Number15_8;
    BYTE   Payload_Bandwidth_Available_Number7_0;
}SB_ENUM_PATH_RESOURCES_REPLY;

typedef struct _ALLOC_PAYLOAD_REPLY
{
    BYTE    uczeros                                 :4;
    BYTE    Port_Number                             :4;
    BYTE    zero                                    :1;
    BYTE    Virtual_Channel_Payload_Identifier      :7;
    BYTE   Payload_Bandwidth_Number15_8;
    BYTE   Payload_Bandwidth_Number7_0;
}ALLOC_PAYLOAD_REPLY;




typedef struct _SB_CONNECTION_STATUS_NOTIFY_REQUEST
{
    BYTE     Request_Identifier;
    BYTE     zeros                                     :4;
    BYTE     Port_Number                               :4;

    GUID     guid;

    BYTE     Peer_Device_Type                          :3;
    BYTE     Input_Port                                :1;
    BYTE     Messaging_Capability_Status               :1;
    BYTE     DisplayPort_Device_Plug_Status            :1;
    BYTE     Legacy_Device_Plug_Status                 :1;
    BYTE     EndZero                                   :1;
}SB_CONNECTION_STATUS_NOTIFY_REQUEST;

typedef struct _SB_QUERY_PAYLOAD_REPLY
{
    BYTE    uczeros                                 :4;
    BYTE    Port_Number                             :4;
    BYTE    Alloc_Payload15_8;
    BYTE    Alloc_Payload7_0;
}SB_QUERY_PAYLOAD_REPLY;

typedef struct _SB_REMOTE_DPCD_READ_REPLY_ST
{
    BYTE    Port_Number                             :4;
    BYTE    uczeros                                 :4;
    BYTE    Number_Of_Bytes_Read                    :8;
    // Rest are pBuffer of the size Number_Of_Bytes_Read
}SB_REMOTE_DPCD_READ_REPLY_ST;

typedef struct _SB_REMOTE_DPCD_WRITE_READ_REPLY_ST
{
    BYTE    uczeros                                 :8;
    BYTE    Port_Number                             :8;
}SB_REMOTE_DPCD_WRITE_READ_REPLY_ST;

typedef struct _SB_REMOTE_I2C_READ_REPLY_ST
{
    BYTE Port_Number                                :4;
    BYTE    uczeros                                 :4;
    BYTE Number_Of_Bytes_Read                       :8;
    // Rest are pBuffer of the size Number_Of_Bytes_Read
}SB_REMOTE_I2C_READ_REPLY_ST;

// PWR_UP_DOWN_PHY_REPLY
typedef struct _POWER_UP_DOWN_PHY_REPLY_ST
{
    BYTE    uczeros                                 :8;
    BYTE    Port_Number                             :8;
}POWER_UP_DOWN_PHY_REPLY_ST;


// UpStream Message Structures
typedef struct _SB_CONNECTION_STATUS_NOTIFY_ST
{
    BYTE ucRequestID;
    SB_LINK_ADDRESS_REPLY_PORT_DETAILS_0 stConnectionStatusNotifyData;
}SB_CONNECTION_STATUS_NOTIFY_ST;

typedef struct _SB_RESOURCE_STATUS_NOTIFY_ST
{
    BYTE ucRequestID;
    BYTE byZeros                                    :4;
    BYTE Port_Number                                :4;
    GUID guid;
    USHORT usAvailablePBN;  	
}SB_RESOURCE_STATUS_NOTIFY_ST;


#pragma pack()

#define GET_SIDEBAND_MSG_PAYLOAD_SIZE(a) (a.SBMSG_HEADER_BOTTOM.SideBand_MSG_Body_Length - 1)



typedef struct _VALIDATE_AND_EXTRACT_ERROR_STATUS
{
    UCHAR ucReasonForNak;

    BOOLEAN bNAKRecieved         : 1;

    BOOLEAN bSPInotRecieved      : 1;

    BOOLEAN bWrongCRCinReply     : 1;

    BOOLEAN bWrongHeader         : 1;

    BOOLEAN bMemAllocationFailed : 1;

    BOOLEAN bWrongReply          : 1;

    BOOLEAN bInvalidMsgBodyLength : 1;

    BOOLEAN _Reserved             : 1;

}VALIDATE_AND_EXTRACT_ERROR_STATUS, *PVALIDATE_AND_EXTRACT_ERROR_STATUS;

#endif