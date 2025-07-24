#ifndef __DPCDS_H__
#define __DPCDS_H__

#define MAX_DPCD_ADDRESS_RANGE 0x1005

#define TIMESLOT_START 1
#define TIMESLOT_END 64
#define MAX_SUPPORTED_STREAMS 10 // This is currently set to 3 in Gfx for <= KBL Platforms
#define VCPLAYLOAD_STREAMID_INVALID 0x0
#define VCPAYLOAD_TABLE_SIZE 0x40

typedef enum _DPCD_REV
{
    eDPCDRev_Invalid = 0x0,
    eDPCDRev_1_0     = 0x10,
    eDPCDRev_1_1     = 0x11,
    eDPCDRev_1_2     = 0x12,
    eDPCDRev_1_4     = 0x14,
    eDPCDRev_Max

} DPCD_REV,
*PDPCD_REV;

#pragma pack(1)

#define DPCD_REVISION 0x0
#define DPCD_MAX_LINK_RATE 0x1
#define DPCD_MAX_LANE_COUNT 0x2
typedef union _DPCDEF_MAX_LANE_COUNT {
    UCHAR ucValue;
    struct
    {
        UCHAR ucMaxLaneCount : 5;    // Bit 4:0 Maximum number of lanes
        UCHAR ucReserved2 : 1;       // Bit 5: reserved
        UCHAR bTP3Supported : 1;     // Bit 6: TRUE : Supported FALSE: Not supported
                                     // Training pattern sequence 3 supported as described in section 2.9.3.1
        UCHAR bEnhancedFrameCap : 1; // Bit 7: TRUE : Supported FALSE: Not supported
                                     // Enhanced Framing symbol sequence for BS, SR, CPBS, and
                                     // CPSR supported as described in Section 2.2.1.2.
    };

} DPCDEF_MAX_LANE_COUNT, *PDPCDEF_MAX_LANE_COUNT;

///////************************************************************************************************************************************************//////

#define DPCD_MAX_DOWNSPREAD 0x3
typedef union _DPCDDEF_MAX_DOWNSPREAD {
    UCHAR ucValue;
    struct
    {

        UCHAR ucMaxDwnSpread : 1;  // Bit 0
                                   // For DPCD Rev.1.0 ; 0 No down spread 1 0.5% down spread
                                   // For DPCD Rev.1.1 this bit should be 1
        UCHAR ucReserved1 : 5;     // Bit 5:1
        UCHAR bNoAuxHandShake : 1; // Bit 6
                                   // FALSE: Requires Aux hand shake to synch DP transmitter
                                   // TRUE : Does not need AUX CH handshake when link config already known
        UCHAR bTPS4Supported : 1;  // Bit 7 ( Mandatory for Downstream Devices with DPCD Rev 1.4 except for eDP DPRxs)
    };

} DPCDDEF_MAX_DOWNSPREAD, *PDPCDDEF_MAX_DOWNSPREAD;

#define DPCD_TRAINING_AUX_RD_INTERVAL 0xE
typedef union _DPCDEF_TRAINING_AUX_RD_INTERVAL {
    UCHAR ucValue;
    struct
    {

        UCHAR ucTrainingAuxRdInterval : 7; // Bit 6:0
        /*
        Link Status / Adjust Request read interval during Main - Link Training.
        00h = 100us for the Main - Link LANEx_CR_DONE sequence; 400us for the
        Main - Link LANEx_CHANNEL_EQ_DONE sequence.
        01h = 100us for the Main - Link LANEx_CR_DONE sequence; 4ms for the
        Main - Link LANEx_CHANNEL_EQ_DONE sequence.
        02h = 100us for the Main - Link LANEx_CR_DONE sequence; 8ms for the
        Main - Link LANEx_CHANNEL_EQ_DONE sequence.
        03h = 100us for the Main - Link LANEx_CR_DONE sequence; 12ms for the
        Main - Link LANEx_CHANNEL_EQ_DONE sequence.
        04h = 100us for the Main - Link LANEx_CR_DONE sequence; 16ms for the
        Main - Link LANEx_CHANNEL_EQ_DONE sequence*/
        UCHAR ucExtendedReceiverCapibilityFieldPresent : 1; // Bit 7
        /*
        0 = Not present.
        1 = Present at DPCD Addresses 02200h through 022FFh.
        A DPRX with DPCD r1.4 (or higher) shall have an Extended Receiver
        Capability field
        */
    };

} DPCDEF_TRAINING_AUX_RD_INTERVAL, *PDPCDEF_TRAINING_AUX_RD_INTERVAL;

/***************************************************/
/* DPCD REGISTERS OF EXTENDED RECEIVER CAPABILITY */
#define DPCD_REVISION_EXT 0x2200
#define DPCD_MAX_LINK_RATE_EXT 0x2201
#define DPCD_MAX_LANE_COUNT_EXT 0x2202
#define DPCD_MAX_DOWNSPREAD_EXT 0x2203
/***************************************************/

///////************************************************************************************************************************************************//////

// Link Training Related DPCDS
#define DPCD_SET_LINK_RATE 0x100
#define DPCD_SET_LANE_COUNT 0x101
#define DPCD_SET_TRAINING_PATTERN 0x102
typedef union _DPDDEF_TRAINING_PATTERN_SET {
    UCHAR ucValue;
    struct
    {
        UCHAR ucTrainingPatternSet : 2; // Bit 1:0
        UCHAR ucLinkQualPatternSet : 2; // Bit 3:2
        UCHAR bRecoveredClockOutEn : 1; // Bit 4
        UCHAR bScramblingDisable : 1;   // Bit 5
        UCHAR ucSymErrCntSel : 2;       // Bit 7:6
    };

} DPDDEF_TRAINING_PATTERN_SET, *PDPDDEF_TRAINING_PATTERN_SET;

typedef union _DPDEF_TRAINING_PATTERN_SET_REV14 {
    UCHAR ucValue;
    struct
    {
        UCHAR ucTrainingPatternSet : 4; // Bit 3:0
        UCHAR bRecoveredClockOutEn : 1; // Bit 4
        UCHAR bScramblingDisable : 1;   // Bit 5
        UCHAR ucSymErrCntSel : 2;       // Bit 7:6
    };

} DPDEF_TRAINING_PATTERN_SET_REV14, *PDPDEF_TRAINING_PATTERN_SET_REV14;

///////************************************************************************************************************************************************//////

// IRQ Events Vector DPCD
#define DPCD_SERVICE_IRQ_VECTOR 0x201u
typedef union _DPCDDEF_SPI_IRQ_VECTOR {
    UCHAR ucVal;

    struct
    {

        UCHAR ucReserved1 : 1;        // Bit 0 is reserved for REMOTE CONTROL COMMAND PASSTRHOUGH
        UCHAR bIsAutoTestRequest : 1; // Bit1 AUTOMATED_TEST_REQUEST
        UCHAR bIsCPIRQ : 1;           // Bit2, used for Content Protection
        UCHAR bIsMCCSIRQ : 1;         // Bit3, Optional used for MCCS
        UCHAR bDownReplyMsgRdy : 1;   // Bit4, used when Down Reply Msg is ready
        UCHAR bUpRequestMsgRdy : 1;   // Bit5, Used when Up Request Msg is ready
        UCHAR bSinkSpecificIRQ : 1;   // Bit6, SINK_SPECIFIC_IRQ, this can be Vendor Specific Requests
        UCHAR ucReserved2 : 1;        // Bit7, Reserved

    } IRQVectorBits;

} DPCDDEF_SPI_IRQ_VECTOR, *PDPCDDEF_SPI_IRQ_VECTOR;

///////************************************************************************************************************************************************//////

// VC Payload Related DPCDs
#define DPCD_VCPAYLOAD_ID 0x1C0
#define DPCD_VCPAYLOAD_START_SLOT 0x1C1
#define DPCD_VCPAYLOAD_NUM_SLOTS 0x1C2
#define DPCD_VCPAYLOAD_UPDATE_STATUS 0x2C0
typedef union _DPCDDEF_PAYLOADTABLE_UPDATE_STATUS {
    UCHAR ucVal;

    struct
    {
        UCHAR bPayloadTableUpdated : 1;
        UCHAR bActHandled : 1;
        UCHAR ucReserved2 : 6;
    };

} DPCDDEF_PAYLOADTABLE_UPDATE_STATUS, *PDPCDDEF_PAYLOADTABLE_UPDATE_STATUS;
#define DPCD_VCPAYLOAD_TABLE_START 0x2C1
#define DPCD_VCPAYLOAD_TABLE_END 0x2FF

///////************************************************************************************************************************************************//////

#define MST_DPCD_DOWN_REQ_START 0x1000u // RW
#define MST_DPCD_DOWN_REQ_END 0x11FFu

#define MST_DPCD_UP_REPLY_START 0x1200u // RW
#define MST_DPCD_UP_REPLY_END 0x13FFu

#define MST_DPCD_DOWN_REP_START 0x1400u // RO
#define MST_DPCD_DOWN_REP_END 0x15FFu

#define MST_DPCD_UP_REQ_START 0x1600u // RO
#define MST_DPCD_UP_REQ_END 0x17FFu

#define FEC_CAPABILITY 0x90u               // RO
#define DPCD_SINK_DEVICE_PSR_STATUS 0x2008 // RO
#define DPCD_PSR_CAPABILITY 0x70           // RO
///////************************************************************************************************************************************************//////

#pragma pack()

#endif