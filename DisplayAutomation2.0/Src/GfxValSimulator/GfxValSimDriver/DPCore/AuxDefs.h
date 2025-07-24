#ifndef __AUXDEF_H__
#define __AUXDEF_H__

#include "..\\CommonCore\\PortingLayer.h"

#define AUX_MAX_BYTES 5 * 4
#define AUX_MAX_TXN_LEN 16
//
// Command definitions
//
typedef enum _AUX_REQUEST_COMMAND_TYPES
{
    // Native AUX
    eAUXWrite = 8, // 1000
    eAUXRead  = 9, // 1001

    // I2C on AUX
    eI2CAUXWrite          = 0,     // 0000
    eI2CAUXRead           = 1,     // 0001
    eI2CAUXWriteStatusReq = 2,     // 0010
                                   // I2C with MOT set
    eI2CAUXWrite_MOT          = 4, // 0100
    eI2CAUXRead_MOT           = 5, // 0101
    eI2CAUXWriteStatusReq_MOT = 6  // 0110

} AUX_REQUEST_COMMAND_TYPES;

typedef enum _AUX_REPLY_COMMAND_TYPES
{
    // Native AUX reply
    eAUX_ACK   = 0, // 0000
    eAUX_NACK  = 1, // 0001
    eAUX_DEFER = 2, // 0010

    // I2C over AUX reply
    eI2CAUX_ACK   = 0, // 0000
    eI2CAUX_NACK  = 4, // 0100
    eI2CAUX_DEFER = 8, // 1000

} AUX_REPLY_COMMAND_TYPES;

#pragma pack(1)
// Note: These are following little-endian format

//
// Request syntax
//  SYNC > COMM3:0| ADDR19:16 > ADDR15:8 > ADDR7:0 > LEN7:0 > (DATA0 7:0 ? ) > STOP
//
// Write: STOP when (LEN7:0 + 1) data bytes have been transmitted
typedef struct _AUX_REQUEST_SYNTAX
{
    // Header in data1 register - first one to be transmitted
    union {
        ULONG ulHeader;

        struct
        {
            UCHAR ucLength : 8;
            UCHAR ulAddress7_0 : 8;
            UCHAR ulAddress15_8 : 8;
            UCHAR ulAddress19_16 : 4;
            UCHAR ucCommand : 4; // This will be transmitted first

        } Request;

    } ReqVal;

    // Data in data2-5 registers (valid only for write_request transactions
    // UCHAR ucData[MAX_DP_DATA_SIZE];   // 16 bytes of data (Note: ucData[0] will be transmitted first)

} AUX_REQUEST_SYNTAX;

typedef union _AUX_CTRLREG_STRUCT {
    volatile ULONG ulValue;

    struct
    {
        ULONG ul2XBitClockDivider : 11;   // bits 10:0
        ULONG bDoublePreChargeTime : 1;   // bit 11
        ULONG bDisableDeGlitchLogic : 1;  // bit 12
        ULONG bSyncOnlyClockRecovery : 1; // bit 13
        ULONG bInvertManchester : 1;      // bit 14
        ULONG bUseAKSVBuffer : 1;         // bit 15
        ULONG ulPreChargeTime : 4;        // bits 19:16 (No of us * 2, defalt is 5 which gives 10us)
        ULONG ulMessageSize : 5;          // bits 24:20 (0 < size <= 20; Valid iff bDone is set and timeout/errors are not there)
        ULONG bReceiveError : 1;          // bit 25
        ULONG ulTimeOutTimer : 2;         // bits 27:26 (Default: 00 - 400us)
        ULONG bTimeOutError : 1;          // bit 28
        ULONG bEnableInterrupt : 1;       // bit 29
        ULONG bDone : 1;                  // bit 30
        ULONG bSendOrBusy : 1;            // bit 31 (Write 1 only, Read indicates status)

    } CtrlRegBits;

} AUX_CTRLREG_STRUCT, *PAUX_CTRLREG_STRUCT;

//
// Data registers (DPn_AUX_CTRL_REG+4 to DPn_AUX_CTRL_REG+0x24 - 5 registers of 4 bytes each = 20 bytes)
//
// Note: Data transmit order is MSB --> LSB within a data register
// Between data registers it's Data register 1 --> 5
#define AUX_DATAREG_OFFSET 4
typedef union _AUX_DATAREG_STRUCT {
    ULONG ulValue;

    struct
    {
        UCHAR ucData4 : 8; // bits 7:0
        UCHAR ucData3 : 8;
        UCHAR ucData2 : 8;
        UCHAR ucData1 : 8; // first byte to transmit
    } DataRegBytes;

} AUX_DATAREG_STRUCT, *PAUX_DATAREG_STRUCT;

typedef union _AUX_ALLDATAREG_STRUCT {
    AUX_DATAREG_STRUCT stValue[AUX_MAX_BYTES / 4];
} AUX_ALLDATAREG_STRUCT;

typedef struct _AUX_REQUEST_COMMAND_SYNTAX
{
    // Header in data1 register - first one to be transmitted
    union {
        ULONG ulHeader;

        struct
        {
            UCHAR ulAddress19_16 : 4;
            UCHAR ucCommand : 4; // This will be transmitted first

            UCHAR ulAddress15_8 : 8;
            UCHAR ulAddress7_0 : 8;

            UCHAR ucLength : 8;
        } Request;

        /*struct
        {
        ULONG ucCommand     : 4; // This will be transmitted first
        ULONG ulAddress     : 20;
        ULONG ucLength      : 8;
        }Request;*/
    } CommandDwordBits;

} AUX_COMMAND_SYNTAX, *PAUX_COMMAND_SYNTAX;

// Since the SW Handler directly uses the Aux data DWORD formatted as per the Aux protocol and MSBit is sent first as per the Aux
// protocol but here everything is in memory so we need to have our structure aligned to that fact instead of as per Aux protocol
// thus reversing the bit field order of the above original structure that would be used if this code ran on an Actual sink and received
// data on an Aux Link
typedef struct _AUX_REQUEST_COMMAND_SYNTAX_DIRECT_COPY
{
    // Header in data1 register - first one to be transmitted
    union {
        ULONG ulHeader;

        struct
        {
            UCHAR ucLength : 8;
            UCHAR ulAddress7_0 : 8;
            UCHAR ulAddress15_8 : 8;
            UCHAR ulAddress19_16 : 4;
            UCHAR ucCommand : 4;
        } Request;

    } CommandDwordBits;

} AUX_COMMAND_SYNTAX_DIRECT_COPY, *PAUX_COMMAND_SYNTAX_DIRECT_COPY;

typedef struct _AUX_COMMAND_BYTE
{
    union {
        UCHAR ucValue;

        struct
        {
            UCHAR ulDummy : 4;
            UCHAR ucCommand : 4; // This will be transmitted first

        } CmdByte;
    } AuxCommand;

} AUX_COMMAND_BYTE, *PAUX_COMMAND_BYTE;

#pragma pack()
#endif