#ifndef __GMBUS_H__
#define __GMBUS_H__

#include "CommonInclude\DisplayDefs.h"
#include "GenMMIOHandlers\Gen9MMIO.h"
#include "GenMMIOHandlers\Gen11p5MMIO.h"
#include "CommonInclude\ValSimCommonInclude.h"

/*-----------------------------------------------------------------------*
 *
 *-----------------------------------------------------------------------*/
#define GMBUS_BASE GMBUS0
#define MAX_GMBUS_REGISTERS 6
#define SIZE_EDID_BLOCK 128u
#define MAX_HDMI_PORTS 9

typedef enum _ENUM_EDID_PORT_INDEX
{
    EDID_INDEX_FOR_HDMIA = 0,
    EDID_INDEX_FOR_HDMIB,
    EDID_INDEX_FOR_HDMIC,
    EDID_INDEX_FOR_HDMID,
    EDID_INDEX_FOR_HDMIE,
    EDID_INDEX_FOR_HDMIF,
    EDID_INDEX_FOR_HDMIG,
    EDID_INDEX_FOR_HDMIH,
    EDID_INDEX_FOR_HDMII,
    EDID_INDEX_INVALID
} ENUM_EDID_PORT_INDEX,
*PENUM_EDID_PORT_INDEX;

typedef enum _ENUM_SCDC_PORT_INDEX
{
    SCDC_INDEX_FOR_HDMIA = 0,
    SCDC_INDEX_FOR_HDMIB,
    SCDC_INDEX_FOR_HDMIC,
    SCDC_INDEX_FOR_HDMID,
    SCDC_INDEX_FOR_HDMIE,
    SCDC_INDEX_FOR_HDMIF,
    SCDC_INDEX_FOR_HDMIG,
    SCDC_INDEX_FOR_HDMIH,
    SCDC_INDEX_FOR_HDMII,
    SCDC_INDEX_INVALID
} ENUM_SCDC_PORT_INDEX,
*PENUM_SCDC_PORT_INDEX;

//////////////////////////////////////////////////
//
// GMBUS3 - Data buffer (double buffered)
//
//////////////////////////////////////////////////
typedef union _GMBUS3_REG_STRUCT {
    SIZE32BITS ulValue;

    struct
    {
        SIZE32BITS ulDataByte0 : 8;
        SIZE32BITS ulDataByte1 : 8;
        SIZE32BITS ulDataByte2 : 8;
        SIZE32BITS ulDataByte3 : 8;
    };

} GMBUS3_REG_STRUCT;

//////////////////////////////////////////////////
//
// GMBUS4 - Interrupt mask
//
//////////////////////////////////////////////////
typedef union _GMBUS4_REG_STRUCT {
    SIZE32BITS ulValue;

    struct
    {
        /*
        0XXXXb	Slave Stall Timeout Interrupt Disable
        1XXXXb	Slave Stall Timeout Interrupt Enable
        X0XXXb	NAK Interrupt Disable
        X1XXXb	NAK Interrupt Enable
        XX0XXb	Idle Interrupt Disable
        XX1XXb	Idle Interrupt Enable
        XXX0Xb	HW Wait Interrupt(cycle without a stop has completed) Disable
        XXX1Xb	W Wait Interrupt(cycle without a stop has completed) Enable
        XXXX0b	HW Ready(Data transferred) Interrupt Disable
        XXXX1b	HW Ready(Data transferred) Interrupt Enable
        */
        SIZE32BITS ulInterruptMask : 5;       // bit 4:0
        SIZE32BITS UNIQUENAME(Reserved) : 27; // bit 31:5
    };

} GMBUS4_REG_STRUCT;

//////////////////////////////////////////////////
//
// GMBUS5 - This register provides a method for the software to
//			indicate to the GMBUS controller the 2 byte device index.
//
//////////////////////////////////////////////////
typedef union _GMBUS5_REG_STRUCT {
    SIZE32BITS ulValue;

    struct
    {
        // This is the 2 byte index used in all GMBUS accesses when bit 31 is asserted (1).
        SIZE32BITS ul2ByteSlaveIndex : 16;    // bits 15:0
        SIZE32BITS UNIQUENAME(Reserved) : 15; // bits 30:16

        /******************************************************************************************************************
        When this bit is asserted (1), then bits 15:0 are used as the index.
        Bits 15:8 are used in the first byte which is the most significant index bits.
        The slave index in the GMBUS1<15:8> are ignored.
        Bits 7:0 are used in the second byte which is the least significant index bits.
        ******************************************************************************************************************/
        SIZE32BITS ul2ByteIndexEnable : 1; // bit 31
    };

} GMBUS5_REG_STRUCT;

//////////////////////////////////////////////////
//
// GMBUS1 - Command/Status
//
//////////////////////////////////////////////////
typedef union _GMBUS1_REG_STRUCT {
    SIZE32BITS ulValue;

    // Separate struct in indicate 8-bit slave address (inlcudes read/write indication as well)
    struct
    {
        SIZE32BITS ulSlaveAddress : 8;        // bits 7:0		(Slave address as referred by upper clients: 8 bits ones)
        SIZE32BITS UNIQUENAME(Reserved) : 24; // bits 31:8
    };

    struct
    {
        SIZE32BITS bReadFromSlave : 1;     // bit 0		(0 - Read from slave, 1 - Write to slave)
        SIZE32BITS ul7BitSlaveAddress : 7; // bits 7:1		(Note: No clients so far who use 10-bit addressing)

        // const SIZE32BITS ulSlaveRegisterIndex	: 8;	// bits 15:8	(Reduntant)
        SIZE32BITS ulSlaveRegisterIndex : 8; // bits 15:8	(Enabling since legacy code base uses this! Also enabled in Gen4 BSpec)

        SIZE32BITS ulTotalBytes : 9;         // bits 24:16	(Bytes of data transfered during DATA phase)
        SIZE32BITS ulBusCycleSelect : 3;     // bits 27:25	(See GMBUS_BUSCYCLE_SELECT)
        SIZE32BITS UNIQUENAME(Reserved) : 2; // bits 29:28	(Must be 0)
        SIZE32BITS bSWReady : 1;          // bit 30		(0 - De-asserted via the assertion event for HW_RDY bit, 1 - When asserted by software, results in de-assertion of HW_RDY bit)
        SIZE32BITS bSWClearInterrupt : 1; // bit 31		(0 - If this bit is written as a zero when it's current state is a one, will clear the
        //				( HW_RDY bit and allows register writes to be accepted to the GMBUS registers (Write Protect Off).
        //				( This bit is cleared to zero on the event that causes the HW_RDY bit transition to asserted.
        //				( This bit must be clear for normal operation.  Setting the bit and then clearing it acts as
        //				( local reset to the GMBUS controller.
        //				(1 - Asserted by software after servicing the GMBUS interrupt.   Setting this bit causes
        //				( the INT status bit to be cleared.  Setting (1) this bit also asserts the HW_RDY
        //				( bit (until this bit is written with a 0).   When this bit is set, no writes to GMBUS
        //				( registers will cause the contents to change with the exception of this bit which can be written.)
    };

} GMBUS1_REG_STRUCT;

//////////////////////////////////////////////////
//
// GMBUS0 - Clock/Port Select struct
//
//////////////////////////////////////////////////
typedef union _GMBUS0_REG_STRUCT {
    SIZE32BITS ulValue;

    struct
    {
        SIZE32BITS ulPinPairSelect : 5;       // bits 4:0 (See GMBUS_PIN_PAIR
        SIZE32BITS UNIQUENAME(Reserved) : 1;  // bit 5
        SIZE32BITS bByteCountOverride : 1;    // bit 6
        SIZE32BITS b300nsHoldTime : 1;        // bit 7	(0 - 0ns, 1 - 300ns hold time extension)
        SIZE32BITS ulRateSelect : 2;          // bits 9:8 (See GMBUS_RATE_SELECT)
        SIZE32BITS UNIQUENAME(Reserved) : 22; // bits 31:10
    };

} GMBUS0_REG_STRUCT;

/*-----------------------------------------------------------------------*
 *
 *-----------------------------------------------------------------------*/
typedef union _GMBUS2_RW_REG_STRUCT {
    SIZE32BITS ulValue; // Readonly since no one should change this directly

    struct
    {
        SIZE32BITS ulCurrentByteCount : 9;    // bits 8:0
        SIZE32BITS bGMBusIsActive : 1;        // bit 9
        SIZE32BITS bSlaveAckTimeout : 1;      // bit 10	(BUS_ERROR)
        SIZE32BITS bHWReady : 1;              // bit 11
        SIZE32BITS bInterrupt : 1;            // bit 12
        SIZE32BITS UNIQUENAME(Reserved) : 1;  // bit 13
        SIZE32BITS bInWaitPhase : 1;          // bit 14
        SIZE32BITS bInUse : 1;                // bit 15	(To relinquish control set this)
        SIZE32BITS UNIQUENAME(Reserved) : 16; // bit 31:16
    };

} GMBUS2_RW_REG_STRUCT;

/*-----------------------------------------------------------------------*
 *
 *-----------------------------------------------------------------------*/
typedef enum GMBUS_STATE_ENUM
{
    GMBUS_DEFAULT,
    GMBUS_ACQUIRE,
    GMBUS_START,
    GMBUS_READY,
    GMBUS_READ,
    GMBUS_STOP,
    GMBUS_RESET,
    GMBUS_RELEASE
} GMBUS_STATE;

typedef enum DONGLE_TYPE_ENUM
{
    DONGLE_TYPE_DEFAULT,
    DONGLE_TYPE_1_ADAPTER,
    DONGLE_TYPE_2_ADAPTER,
    DONGLE_TYPE_DVI,
    DONGLE_TYPE_LSPCON,
    DONGLE_TYPE_2_ADAPTER_PS8469,
} DONGLE_TYPE;

typedef struct _EDID_DATA
{
    // ULT_EDID edidIndex;
    ULONG  ulHDMIPort;
    ULONG  ulEdidDataSize;
    ULONG  ulNumEDIDBlocks;
    PUCHAR pucEdidData;
    // PUCHAR pucEDIDBlocks[MAX_NUM_EDID_BLOCKS];
} EDID_DATA, *PEDID_DATA;

typedef struct _SCDC_DATA
{
    ULONG  ulHDMIPort;
    ULONG  ulScdcDataSize;
    PUCHAR pucScdcData;

} SCDC_DATA, *PSCDC_DATA;
typedef struct _GMBUS_INTERFACE
{
    ULONG              GMBUSData[MAX_GMBUS_REGISTERS];
    EDID_DATA          EdidData[MAX_HDMI_PORTS];
    SCDC_DATA          ScdcData[MAX_HDMI_PORTS];
    DONGLE_TYPE        DongleType[MAX_HDMI_PORTS];
    GMBUS_STATE        eGMBUSCurrentState;
    IGFX_PLATFORM      eIGFXPlatform;
    PCH_PRODUCT_FAMILY ePCHProductFamily;
    ULONG              ulNumRefCount;

} GMBUS_INTERFACE, *PGMBUS_INTERFACE;

PGMBUS_INTERFACE GMBusInterface_GetSingletonGMBusObject(IGFX_PLATFORM eIGFXPlatform, PCH_PRODUCT_FAMILY ePCHProductFamily);
BOOLEAN          GMBusInterface_SetEDIDData(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulEDIDSize, PUCHAR pucEDIDBuff, ULONG ulHDMIPort);
BOOLEAN          GMBusInterface_GetEDIDIndexFromPort(ULONG ulHDMIPort, PULONG pulEDIDIndex);
BOOLEAN          GMBusInterface_GetEDIDDataBlock(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulGPIOPin);
BOOLEAN          GMBusInterface_GMBUSStateMachineHandler(PGMBUS_INTERFACE pstGMBusInterface, GMBUS_STATE eNewState);
BOOLEAN          GMBusInterface_GMBUS0WriteHandler(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulOffset, ULONG ulData);
BOOLEAN          GMBusInterface_GMBUS1WriteHandler(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulOffset, ULONG ulData);
BOOLEAN          GMBusInterface_GMBUS2WriteHandler(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulOffset, ULONG ulData);
// SCDC Functions declarations.
BOOLEAN GMBusInterface_SetSCDCData(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulSCDCSize, PUCHAR pucSCDCBuff, ULONG ulHDMIPort);
BOOLEAN GMBusInterface_GetSCDCIndexFromPort(ULONG ulHDMIPort, PULONG pulSCDCIndex);
BOOLEAN GMBusInterface_GetSCDCDataBlock(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulGPIOPin);

// DongleType Functions declarations
BOOLEAN GMBusInterface_GetDongleTypeData(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulGPIOPin);
BOOLEAN GMBusInterface_SetDongleType(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulPortType, DONGLE_TYPE eDongleType);

__inline GMBUS_STATE GMBusInterface_GetGMBUSCurrentState(PGMBUS_INTERFACE pstGMBusInterface)
{
    // PHDMIINTERFACE pstHDMIInterface = (HDMIINTERFACE *)pstMMIOHandlerInfo->pvPrivateData;
    return pstGMBusInterface->eGMBUSCurrentState;
}

__inline void GMBusInterface_SetGMBUSCurrentState(PGMBUS_INTERFACE pstGMBusInterface, GMBUS_STATE eState)
{
    // PHDMIINTERFACE pstHDMIInterface = (HDMIINTERFACE *)pstMMIOHandlerInfo->pvPrivateData;
    pstGMBusInterface->eGMBUSCurrentState = eState;
}

__inline ULONG GMBusInterface_ReadGMBUSDWORDRegister(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulMMIOOffset)
{
    // PHDMIINTERFACE pstHDMIInterface = (HDMIINTERFACE *)pstMMIOHandlerInfo->pvPrivateData;
    return pstGMBusInterface->GMBUSData[(ulMMIOOffset - GMBUS_BASE) / 4];
}

__inline void GMBusInterface_WriteGMBUSDWORDRegister(PGMBUS_INTERFACE pstGMBusInterface, ULONG ulMMIOOffset, ULONG ulData)
{
    // PHDMIINTERFACE pstHDMIInterface = (HDMIINTERFACE *)pstMMIOHandlerInfo->pvPrivateData;
    pstGMBusInterface->GMBUSData[(ulMMIOOffset - GMBUS_BASE) / 4] = ulData;
}

#endif
