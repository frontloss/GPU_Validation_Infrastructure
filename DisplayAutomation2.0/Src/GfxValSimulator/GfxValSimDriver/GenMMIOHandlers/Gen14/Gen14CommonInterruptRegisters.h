/*===========================================================================
; Gen13InterruptRegisters.h - Gen14 InterruptHandler interface
;----------------------------------------------------------------------------
;   Copyright (c) Intel Corporation (2000 - 2018)
;
;   INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
;   ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
;   INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
;   ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
;   MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
;   OTHER WARRANTY.  Intel disclaims all liability, including liability for
;   infringement of any proprietary rights, relating to use of the code. No license,
;   express or implied, by estoppel or otherwise, to any intellectual property
;   rights is granted herein.
;
;
;   File Description:
;       This file contains all the InterruptHandler interface function and data structure definitions for GEN14
;--------------------------------------------------------------------------*/

#ifndef __GEN14INTERRUPT_REGS_H__
#define __GEN14INTERRUPT_REGS_H__

#include "..\\..\\CommonInclude\\BitDefs.h"
#include "..\\..\\CommonInclude\\\DisplayDefs.h"

typedef enum _GFX_MSTR_INTR_INSTANCE_GEN14
{
    GFX_MSTR_INTR_ADDR_GEN14 = 0X190010,
} GFX_MSTR_INTR_INSTANCE_GEN14;

typedef enum _MASTER_INTERRUPT_GEN14
{
    MASTER_INTERRUPT_DISABLE_GEN14 = 0x0,
    MASTER_INTERRUPT_ENABLE_GEN14  = 0x1
} MASTER_INTERRUPT_GEN13;

/*****************************************************************************
Description:  Top level register that indicates interrupt from hardware.
Bits in this register are set interrupts are pending in the underlying PCU, display or GT interrupts
Bspec: https://gfxspecs.intel.com/Predator/Home/Index/54028
******************************************************************************/
typedef union _GFX_MSTR_INTR_GEN14 {
    struct
    {
        DDU32 GtDw0InterruptsPending : DD_BITFIELD_BIT(0);
        DDU32 GtDW1InterruptsPending : DD_BITFIELD_BIT(1);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(2, 7);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(8);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(9, 15);
        DDU32 DisplayInterruptsPending : DD_BITFIELD_BIT(16);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(17, 25);
        DDU32 CorrectableError : DD_BITFIELD_BIT(26);
        DDU32 NonFatalError : DD_BITFIELD_BIT(27);
        DDU32 FatalError : DD_BITFIELD_BIT(28);
        DDU32 GuMiscInterruptsPending : DD_BITFIELD_BIT(29);
        DDU32 PcuInterruptsPending : DD_BITFIELD_BIT(30);
        /*This is the master control for graphics interrupts. This must be enabled for any of these interrupts to propagate to PCI device 2 interrupt processing */
        DDU32 MasterInterruptEnable : DD_BITFIELD_BIT(31);
    };
    DDU32 Value;
} GFX_MSTR_INTR_GEN14, *PGFX_MSTR_INTR_GEN14;

C_ASSERT(4 == sizeof(GFX_MSTR_INTR_GEN14));

// IMPLICIT ENUMERATIONS USED BY DISPLAY_INT_CTL_GEN13
//
typedef enum _DISPLAY_INTR_GEN14
{
    DISPLAY_INTR_DISABLE_GEN14 = 0x0,
    DISPLAY_INTR_ENABLE_GEN14  = 0x1,
} DISPLAY_INTR_GEN14;

typedef enum _DISPLAY_INTR_CTL_INSTANCE_GEN14
{
    DISPLAY_INTR_CTL_ADDR_GEN14 = 0x44200,
} DISPLAY_INTR_CTL_INSTANCE_GEN14;

/*****************************************************************************\
This register has the master enable for display interrupts and gives an overview of what interrupts are pending.
An interrupt pending bit will read 1b while one or more interrupts of that category are set (IIR) and enabled (IER).
All Pending Interrupts are ORed together to generate the combined interrupt.
The combined interrupt is ANDed with the Display Interrupt enable to create the display enabled interrupt.
The display enabled interrupt goes to graphics interrupt processing.
The master interrupt enable must be set before any of these interrupts will propagate to graphics interrupt processing.
\*****************************************************************************/
typedef union _DISPLAY_INT_CTL_GEN14 {
    struct
    {
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(0, 15);
        SIZE32BITS DePipeAInterruptsPending : BITFIELD_BIT(16);
        SIZE32BITS DePipeBInterruptsPending : BITFIELD_BIT(17);
        SIZE32BITS DePipeCInterruptsPending : BITFIELD_BIT(18);
        SIZE32BITS DePipeDInterruptsPending : BITFIELD_BIT(19);
        SIZE32BITS DePortInterruptsPending : BITFIELD_BIT(20);
        SIZE32BITS DeHpdInterruptsPending : BITFIELD_BIT(21);
        SIZE32BITS DeMiscInterruptsPending : BITFIELD_BIT(22);
        SIZE32BITS DePchInterruptsPending : BITFIELD_BIT(23);
        SIZE32BITS AudioCodecInterruptsPending : BITFIELD_BIT(24);
        SIZE32BITS DirectPICAInterruptsPending : BITFIELD_BIT(25);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(26, 30);
        SIZE32BITS DisplayInterruptEnable : BITFIELD_BIT(31);
    };
    SIZE32BITS ulValue;

} DISPLAY_INT_CTL_GEN14, *PDISPLAY_INT_CTL_GEN14;

C_ASSERT(4 == sizeof(DISPLAY_INT_CTL_GEN14));

/*****************************************************************************\
The status fields indicate the hot plug detect status on each port.
When HPD is enabled and either a long or short pulse is detected for a port,
one of the status bits will set and the hotplug IIR will be set (if unmasked in the IMR).
The status bits are sticky bits, cleared by writing 1s to the bits.
Each HPD pin can be configured as an input or output.
The HPD status function will only work when the pin is configured as an input.
The HPD Output Data function will only work when the HPD pin is configured as an output.
The short pulse duration is programmed in SHPD_PULSE_CNT.
\*****************************************************************************/

typedef union _SHOTPLUG_CTL_DDI_GEN14 {
    struct
    {
        SIZE32BITS DdiaHpdStatus : BITFIELD_RANGE(0, 1);
        SIZE32BITS DdiaHpdOutputData : BITFIELD_BIT(2);
        SIZE32BITS DdiaHpdEnable : BITFIELD_BIT(3);
        SIZE32BITS DdibHpdStatus : BITFIELD_RANGE(4, 5);
        SIZE32BITS DdibHpdOutputData : BITFIELD_BIT(6);
        SIZE32BITS DdibHpdEnable : BITFIELD_BIT(7);
        SIZE32BITS DdicHpdStatus : BITFIELD_RANGE(8, 9);
        SIZE32BITS DdicHpdOutputData : BITFIELD_BIT(10);
        SIZE32BITS DdicHpdEnable : BITFIELD_BIT(11);
        SIZE32BITS DdidHpdStatus : BITFIELD_RANGE(12, 13);
        SIZE32BITS DdidHpdOutputData : BITFIELD_BIT(14);
        SIZE32BITS DdidHpdEnable : BITFIELD_BIT(15);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(16, 31);
    };
    SIZE32BITS ulValue;

} SHOTPLUG_CTL_DDI_GEN14, *PSHOTPLUG_CTL_DDI_GEN14;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_DDI_GEN14));

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_DDI_GEN13
//
typedef enum _SOUTH_HOT_PLUG_CTL_FOR_DDI_INSTANCE_GEN14
{
    SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN14 = 0xC4030,

} SOUTH_HOT_PLUG_CTL_FOR_DDI_INSTANCE_GEN14;

/*****************************************************************************\
South Display Engine (SDE) interrupt bits come from events within the south display engine.The SDE_IIR bits are ORed together to generate the South/PCH Display Interrupt Event
which will appear in the North Display Engine Interrupt Control Registers.	The South Display Engine Interrupt Control Registers all share the same bit definitions from this table.
\*****************************************************************************/
typedef union _SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 {
    struct
    {

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcDdia : BITFIELD_BIT(0);
        SIZE32BITS ScdcDdib : BITFIELD_BIT(1);
        SIZE32BITS ScdcDdic : BITFIELD_BIT(2);
        SIZE32BITS ScdcDdid : BITFIELD_BIT(3);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(4, 7); // MBZ
        SIZE32BITS ScdcTc1 : BITFIELD_BIT(8);
        SIZE32BITS ScdcTc2 : BITFIELD_BIT(9);
        SIZE32BITS ScdcTc3 : BITFIELD_BIT(10);
        SIZE32BITS ScdcTc4 : BITFIELD_BIT(11);
        SIZE32BITS ScdcTc5 : BITFIELD_BIT(12);
        SIZE32BITS ScdcTc6 : BITFIELD_BIT(13);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(14, 15); // MBZ
        SIZE32BITS HotplugDdia : BITFIELD_BIT(16);
        SIZE32BITS HotplugDdib : BITFIELD_BIT(17);
        SIZE32BITS HotplugDdic : BITFIELD_BIT(18);
        SIZE32BITS HotplugDdid : BITFIELD_BIT(19);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(20, 22); // MBZ
        SIZE32BITS Gmbus : BITFIELD_BIT(23);
        SIZE32BITS HotplugTypecPort1 : BITFIELD_BIT(24);
        SIZE32BITS HotplugTypecPort2 : BITFIELD_BIT(25);
        SIZE32BITS HotplugTypecPort3 : BITFIELD_BIT(26);
        SIZE32BITS HotplugTypecPort4 : BITFIELD_BIT(27);
        SIZE32BITS HotplugTypecPort5 : BITFIELD_BIT(28);
        SIZE32BITS HotplugTypecPort6 : BITFIELD_BIT(29);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(31);
        SIZE32BITS PICAInterrupt : BITFIELD_BIT(31);
    };
    SIZE32BITS ulValue;

} SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14, *PSOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14;

C_ASSERT(4 == sizeof(SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14));

// IMPLICIT ENUMERATIONS USED BY SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13
//
typedef enum _SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_INSTANCE_GEN14
{
    SDE_ISR_ADDR_GEN14 = 0xC4000,
    SDE_IMR_ADDR_GEN14 = 0xC4004,
    SDE_IIR_ADDR_GEN14 = 0xC4008,
    SDE_IER_ADDR_GEN14 = 0xC400C,
} SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_INSTANCE_GEN14;

typedef enum _HPD_STATUS_ENUM_GEN14
{
    HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN14    = 0x0,
    HPD_STATUS_SHORT_PULSE_DETECTED_GEN14           = 0x1,
    HPD_STATUS_LONG_PULSE_DETECTED_GEN14            = 0x2,
    HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN14 = 0x3,

} HPD_STATUS_ENUM_GEN14;

typedef union _PORT_TX_DFLEXDPPMS_D14 {
    struct
    {
        /******************************************************************************************************************
         DFLEXDPPMS.DPPMSTC0 PD FW writes 1 to this bit to tell DP Driver that PHY is ready. PD FW writes '0' to this bit to tell DP Driver that PHY is not ready.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector0 : DD_BITFIELD_BIT(0); // DISPLAY_PORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 1.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector1 : DD_BITFIELD_BIT(1); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 2.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector2 : DD_BITFIELD_BIT(2); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 3.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector3 : DD_BITFIELD_BIT(3); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 4.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector4 : DD_BITFIELD_BIT(4); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 5.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector5 : DD_BITFIELD_BIT(5); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 6.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector6 : DD_BITFIELD_BIT(6); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 7.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector7 : DD_BITFIELD_BIT(7); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 8.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector8 : DD_BITFIELD_BIT(8); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 9.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector9 : DD_BITFIELD_BIT(9); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 10.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector10 : DD_BITFIELD_BIT(10); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 11.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector11 : DD_BITFIELD_BIT(11); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 12.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector12 : DD_BITFIELD_BIT(12); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 13.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector13 : DD_BITFIELD_BIT(13); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 14.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector14 : DD_BITFIELD_BIT(14); //

        /******************************************************************************************************************
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector 15.
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector15 : DD_BITFIELD_BIT(15); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(16, 31); //
    };

    DDU32 Value;

} PORT_TX_DFLEXDPPMS_D14;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXDPPMS_D14));
/*****************************************************************************
Description:   This table indicates which events are mapped to each bit of the PICA Interrupt registers. The hotplug bits use a modified interrupt structure where the live value
goes to the ISR and a processed event goes to the IMR and IIR path. The IIR bits are ORed together to generate the PICA Display Interrupt Event which will appear in South Display
Engine Interrupt Control Registers. ISR is at the BASE, IMR is at BASE+0x4, IIR is at BASE+0x8, IER is at BASE+0xC. Reference : INTERRUPT structure

******************************************************************************/
typedef union _PICA_INTERRUPT_DEFINTION_GEN14 {
    struct
    {
        SIZE32BITS TbtHotplugPort1 : BITFIELD_BIT(0);
        SIZE32BITS TbtHotplugPort2 : BITFIELD_BIT(1);
        SIZE32BITS TbtHotplugPort3 : BITFIELD_BIT(2);
        SIZE32BITS TbtHotplugPort4 : BITFIELD_BIT(3);
        SIZE32BITS Unused4 : BITFIELD_BIT(4);
        SIZE32BITS Unused5 : BITFIELD_BIT(5);
        SIZE32BITS Unused6 : BITFIELD_BIT(6);
        SIZE32BITS Unused7 : BITFIELD_BIT(7);
        SIZE32BITS AuxPort1 : BITFIELD_BIT(8);
        SIZE32BITS AuxPort2 : BITFIELD_BIT(9);
        SIZE32BITS AuxPort3 : BITFIELD_BIT(10);
        SIZE32BITS AuxPort4 : BITFIELD_BIT(11);
        SIZE32BITS Unused12 : BITFIELD_BIT(12);
        SIZE32BITS Unused13 : BITFIELD_BIT(13);
        SIZE32BITS Unused14 : BITFIELD_BIT(14);
        SIZE32BITS Unused15 : BITFIELD_BIT(15);
        SIZE32BITS DpAltHotplugPort1 : BITFIELD_BIT(16);
        SIZE32BITS DpAltHotplugPort2 : BITFIELD_BIT(17);
        SIZE32BITS DpAltHotplugPort3 : BITFIELD_BIT(18);
        SIZE32BITS DpAltHotplugPort4 : BITFIELD_BIT(19);
        SIZE32BITS Unused20 : BITFIELD_BIT(20);
        SIZE32BITS Unused21 : BITFIELD_BIT(21);
        SIZE32BITS Unused22 : BITFIELD_BIT(22);
        SIZE32BITS Unused23 : BITFIELD_BIT(23);
        SIZE32BITS Unused24 : BITFIELD_BIT(24);
        SIZE32BITS Unused25 : BITFIELD_BIT(25);
        SIZE32BITS Unused26 : BITFIELD_BIT(26);
        SIZE32BITS Unused27 : BITFIELD_BIT(27);
        SIZE32BITS Unused28 : BITFIELD_BIT(28);
        SIZE32BITS Unused29 : BITFIELD_BIT(29);
        SIZE32BITS Unused30 : BITFIELD_BIT(30);
        SIZE32BITS TypecMailbox : BITFIELD_BIT(31);
    };
    SIZE32BITS ulValue;

} PICA_INTERRUPT_DEFINTION_GEN14, *PPICA_INTERRUPT_DEFINTION_GEN14;

C_ASSERT(4 == sizeof(PICA_INTERRUPT_DEFINTION_GEN14));

typedef union _PORT_HOTPLUG_CTL_GEN14 {
    struct
    {
        SIZE32BITS DpAltStatus : BITFIELD_RANGE(0, 1);
        SIZE32BITS DpAltEnable : BITFIELD_BIT(2);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(3);
        SIZE32BITS TbtStatus : BITFIELD_RANGE(4, 5);
        SIZE32BITS TbtEnable : BITFIELD_BIT(6);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(7, 31);
    };
    SIZE32BITS ulValue;
} PORT_HOTPLUG_CTL_GEN14, *PPORT_HOTPLUG_CTL_GEN14;

C_ASSERT(4 == sizeof(PORT_HOTPLUG_CTL_GEN14));

typedef enum _DP_ALT_STATUS_ENUM_GEN14
{
    DP_ALT_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN14    = 0x0,
    DP_ALT_STATUS_SHORT_PULSE_DETECTED_GEN14           = 0x1,
    DP_ALT_STATUS_LONG_PULSE_DETECTED_GEN14            = 0x2,
    DP_ALT_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN14 = 0x3,

} DP_ALT_STATUS_ENUM_GEN14;

typedef enum _DP_ALT_ENABLE_ENUM_GEN14
{
    DP_ALT_DISABLE_GEN14 = 0x0,
    DP_ALT_ENABLE_GEN14  = 0x1,

} DP_ALT_ENABLE_ENUM_GEN14;

typedef enum _TBT_STATUS_ENUM_GEN14
{
    TBT_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN14    = 0x0,
    TBT_STATUS_SHORT_PULSE_DETECTED_GEN14           = 0x1,
    TBT_STATUS_LONG_PULSE_DETECTED_GEN14            = 0x2,
    TBT_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN14 = 0x3,

} TBT_STATUS_ENUM_GEN14;

typedef enum _TBT_ENABLE_ENUM_GEN14
{
    TBT_DISABLE_GEN14 = 0x0,
    TBT_ENABLE_GEN14  = 0x1,

} TBT_ENABLE_ENUM_GEN14;

typedef enum _PICA_INTERRUPT_DEFINTION_INSTANCE_GEN14 // https://gfxspecs.intel.com/Predator/Home/Index/65112
{
    PICAINTERRUPTDEFINTION_0_ADDR_GEN14 = 0x16FE50, // ISR
    PICAINTERRUPTDEFINTION_1_ADDR_GEN14 = 0x16FE54, // IMR
    PICAINTERRUPTDEFINTION_2_ADDR_GEN14 = 0x16FE58, // IIR
    PICAINTERRUPTDEFINTION_3_ADDR_GEN14 = 0x16FE5C, // IER

} PICA_INTERRUPT_DEFINITION_INSTANCE_GEN14;

typedef enum _DE_PORT_INTERRUPT_DEFINITION_INSTANCE_GEN14
{
    DE_PORT_ISR_ADDR_GEN14 = 0x44440,
    DE_PORT_IMR_ADDR_GEN14 = 0x44444,
    DE_PORT_IIR_ADDR_GEN14 = 0x44448,
    DE_PORT_IER_ADDR_GEN14 = 0x4444C,
} DE_PORT_INTERRUPT_DEFINITION_INSTANCE_GEN14;

typedef enum _PORT_HOTPLUG_CTL_INSTANCE_GEN14
{
    PORT_HOTPLUG_CTL_USBC1_ADDR_GEN14 = 0x16F270,
    PORT_HOTPLUG_CTL_USBC2_ADDR_GEN14 = 0x16F470,
    PORT_HOTPLUG_CTL_USBC3_ADDR_GEN14 = 0x16F670,
    PORT_HOTPLUG_CTL_USBC4_ADDR_GEN14 = 0x16F870,
} PORT_HOTPLUG_CTL_INSTANCE_GEN14;

typedef enum _TCSS_DDI_STATUS_INSTANCE_GEN14
{
    TCSS_DDI_STATUS_1_ADDR_GEN14 = 0x161500,
    TCSS_DDI_STATUS_2_ADDR_GEN14 = 0x161504,
    TCSS_DDI_STATUS_3_ADDR_GEN14 = 0x161508,
    TCSS_DDI_STATUS_4_ADDR_GEN14 = 0x16150C,
} TCSS_DDI_STATUS_INSTANCE_GEN14;

typedef union _TCSS_DDI_STATUS_GEN14 {
    struct
    {
        SIZE32BITS Hpd_LiveStatus_Alt : BITFIELD_BIT(0);
        SIZE32BITS HPD_LiveState_Tbt : BITFIELD_BIT(1);
        SIZE32BITS Ready : BITFIELD_BIT(2);
        SIZE32BITS Sss : BITFIELD_BIT(3);
        SIZE32BITS Src_Port_Num : BITFIELD_RANGE(4, 7);
        SIZE32BITS Hpd_In_Progress : BITFIELD_BIT(8);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(9, 31);
    };
    SIZE32BITS ulValue;
} TCSS_DDI_STATUS_GEN14, *PTCSS_DDI_STATUS_GEN14;

C_ASSERT(4 == sizeof(TCSS_DDI_STATUS_GEN14));

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_TC_GEN13
//
typedef enum _SHOTPLUG_CTL_TC_INSTANCE_GEN14
{
    SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN14 = 0xC4034,
} SHOTPLUG_CTL_TC_INSTANCE_GEN14;

typedef enum _TYPEC_PHY_OWNERSHIP_ENUM_D14
{
    TYPEC_PHY_OWNERSHIP_RELEASE_OWNERSHIP_D14 = 0x0,
    TYPEC_PHY_OWNERSHIP_TAKE_OWNERSHIP_D14    = 0x1,

} TYPEC_PHY_OWNERSHIP_ENUM_D14;

typedef enum _PORT_TX_DFLEXPA1_INSTANCE_D14
{
    PORT_TX_DFLEXPA1_FIA1_ADDR_D14 = 0x163880,
    PORT_TX_DFLEXPA1_FIA2_ADDR_D14 = 0x16E880,
} PORT_TX_DFLEXPA1_INSTANCE_D14;

typedef enum _PORT_BUF_CTL1_INSTANCE_D14
{
    PORT_BUF_CTL1_A_ADDR_D14     = 0x64004,
    PORT_BUF_CTL1_B_ADDR_D14     = 0x64104,
    PORT_BUF_CTL1_USBC1_ADDR_D14 = 0x16F200,
    PORT_BUF_CTL1_USBC2_ADDR_D14 = 0x16F400,
    PORT_BUF_CTL1_USBC3_ADDR_D14 = 0x16F600,
    PORT_BUF_CTL1_USBC4_ADDR_D14 = 0x16F800,

} PORT_BUF_CTL1_INSTANCE_D14;

typedef enum _SHOTPLUG_CTL_TC_INSTANCE_ADP
{
    SHOTPLUG_CTL_TC_ADDR_ADP = 0xC4034,
} SHOTPLUG_CTL_TC_INSTANCE_ADP;

/*****************************************************************************
Description : The status fields indicate the hot plug detect status on each type C port when using non - type C connectors(legacy or static configuration).When HPD is enabled and
either a long or short pulse is detected for a port, one of the status bits will set and the hotplug IIR will be set(if unmasked in the IMR).The status bits are sticky bits,
cleared by writing 1s to the bits. Each HPD pin can be configured as an input or output.The HPD status function will only work when the pin is configured as an input.The HPD Output
Data function will only work when the HPD pin is configured as an output.The short pulse duration is programmed in SHPD_PULSE_CNT.

******************************************************************************
*/
typedef union _SHOTPLUG_CTL_TC_ADP {
    struct
    {
        /******************************************************************************************************************/
        DDU32 Tc1HpdStatus : DD_BITFIELD_RANGE(0, 1); // TC1_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 Tc1HpdOutputData : DD_BITFIELD_BIT(2); // TC1_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 Tc1HpdEnable : DD_BITFIELD_BIT(3); // TC1_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Tc2HpdStatus : DD_BITFIELD_RANGE(4, 5); // TC2_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 Tc2HpdOutputData : DD_BITFIELD_BIT(6); // TC2_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 Tc2HpdEnable : DD_BITFIELD_BIT(7); // TC2_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Tc3HpdStatus : DD_BITFIELD_RANGE(8, 9); // TC3_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 Tc3HpdOutputData : DD_BITFIELD_BIT(10); // TC3_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 Tc3HpdEnable : DD_BITFIELD_BIT(11); // TC3_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Tc4HpdStatus : DD_BITFIELD_RANGE(12, 13); // TC4_HPD_STATUS
        /******************************************************************************************************************/
        DDU32 Tc4HpdOutputData : DD_BITFIELD_BIT(14); // TC4_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 Tc4HpdEnable : DD_BITFIELD_BIT(15); // TC4_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Tc5HpdStatus : DD_BITFIELD_RANGE(16, 17); // TC5_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 Tc5HpdOutputData : DD_BITFIELD_BIT(18); // TC5_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 Tc5HpdEnable : DD_BITFIELD_BIT(19); // TC5_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Tc6HpdStatus : DD_BITFIELD_RANGE(20, 21); // TC6_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 Tc6HpdOutputData : DD_BITFIELD_BIT(22); // TC6_HPD_OUTPUT_DATA

        /******************************************************************************************************************/
        DDU32 Tc6HpdEnable : DD_BITFIELD_BIT(23); // TC6_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(24, 31); //
    };

    DDU32 Value;

} SHOTPLUG_CTL_TC_ADP;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_TC_ADP));

/*****************************************************************************
Description:

******************************************************************************/
typedef union _PORT_BUF_CTL1_D14 {
    struct
    {
        /******************************************************************************************************************
        This field enables the HDMI 2.1 FRL 18b to 20b shifting and data output.
        \******************************************************************************************************************/
        DDU32 HdmiFrlShifterEnable : DD_BITFIELD_BIT(0); // HDMI_FRL_SHIFTER_ENABLE

        /******************************************************************************************************************
        This field selects the number of transmit lanes to use.

        Programming Notes:
        Restriction : The value selected here must match the width selected in DDI_CTL_DE attached to this port and follow the restrictions listed there.
        \******************************************************************************************************************/
        DDU32 PortWidth : DD_BITFIELD_RANGE(1, 3); //

        /******************************************************************************************************************
        This field indicates the status of TCSS power.
        \******************************************************************************************************************/
        DDU32 TcssPowerState : DD_BITFIELD_BIT(4); // TCSS_POWER_STATE

        /******************************************************************************************************************
        This field requests TypeC Subsystem to power up to be accessible for display use. This field is ignored for ports not associated with type-C ports.
        \******************************************************************************************************************/
        DDU32 TcssPowerRequest : DD_BITFIELD_BIT(5); // TCSS_POWER_REQUEST

        /******************************************************************************************************************
        This field is configured to take ownership of the type-C PHY as part of the type-C connect and disconnect flows. This field is ignored for ports not associated with type-C
        ports. The ownership is de-asserted during reset preparation for FLR and warm resets.
        \******************************************************************************************************************/
        DDU32 TypecPhyOwnership : DD_BITFIELD_BIT(6); // TYPEC_PHY_OWNERSHIP

        /******************************************************************************************************************
        This bit indicates when the PHY is idle (electrical idle and power state Ready).
        \******************************************************************************************************************/
        DDU32 IdleStatus : DD_BITFIELD_BIT(7); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(8, 10); //

        /******************************************************************************************************************
        This field selects which IO path to use. It must not be switched while port is enabled.
        \******************************************************************************************************************/
        DDU32 IoSelect : DD_BITFIELD_BIT(11); //

        /******************************************************************************************************************
        PHYs that have frequency programmed in dividers through message bus use the default 1001 setting.
        \******************************************************************************************************************/
        DDU32 PhyMode : DD_BITFIELD_RANGE(12, 15); // PHY_MODE

        /******************************************************************************************************************
        This field indicates data has been lane reversed in the DDI.

        Programming Notes:
        Restriction : The value selected here must match the reversal selected in DDI_CTL_DE attached to this port and follow the restrictions listed there.
        \******************************************************************************************************************/
        DDU32 PortReversal : DD_BITFIELD_BIT(16); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(17); //

        /******************************************************************************************************************
        This value represents PHY data lane width. This field propagates to all PHY lanes assigned to display.

        Programming Notes: Restriction : The value selected here must match the value selected in DDI_CTL_DE attached to this port.
        \******************************************************************************************************************/
        DDU32 DataWidth : DD_BITFIELD_RANGE(18, 19); //

        /******************************************************************************************************************
        PHYs that have frequency programmed in dividers through message bus use the default all 1s setting.
        \******************************************************************************************************************/
        DDU32 PhyLinkRate : DD_BITFIELD_RANGE(20, 23); // PHY_LINK_RATE

        /******************************************************************************************************************
        This field indicates the SoC has made the PHY ready for use.
        \******************************************************************************************************************/
        DDU32 SocPhyReady : DD_BITFIELD_BIT(24); // SOC_PHY_READY

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(25, 27); //

        /******************************************************************************************************************
        This field indicates the status of D2D link.
        \******************************************************************************************************************/
        DDU32 D2DLinkState : DD_BITFIELD_BIT(28); // D2D_LINK_STATE

        /******************************************************************************************************************
        This field requests D2D to enable the link for display.
        \******************************************************************************************************************/
        DDU32 D2DLinkEnable : DD_BITFIELD_BIT(29); // D2D_LINK_ENABLE

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(30, 31); //
    };

    DDU32 Value;

} PORT_BUF_CTL1_D14;

C_ASSERT(4 == sizeof(PORT_BUF_CTL1_D14));

typedef enum _PORT_TX_DFLEXDPPMS_INSTANCE_D14
{
    PORT_TX_DFLEXDPPMS_FIA1_ADDR_D14 = 0x163890,
    PORT_TX_DFLEXDPPMS_FIA2_ADDR_D14 = 0x16E890,

} PORT_TX_DFLEXDPPMS_INSTANCE_D14;

typedef enum _DD_LANE_WIDTH
{
    LANE_X0 = 0, // No lanes enabled
    LANE_X1 = 1,
    LANE_X2 = 2,
    LANE_X3 = 3, // used only for MIPI DSI
    LANE_X4 = 4,
} DD_LANE_WIDTH;

typedef enum _PORT_TX_DFLEXDPSP_INSTANCE_D14
{
    PORT_TX_DFLEXDPSP1_FIA1_ADDR_D14 = 0x1638A0,
    PORT_TX_DFLEXDPSP2_FIA1_ADDR_D14 = 0x1638A4,
    PORT_TX_DFLEXDPSP3_FIA1_ADDR_D14 = 0x1638A8,
    PORT_TX_DFLEXDPSP4_FIA1_ADDR_D14 = 0x1638AC,
    PORT_TX_DFLEXDPSP1_FIA2_ADDR_D14 = 0x16E8A0,
    PORT_TX_DFLEXDPSP2_FIA2_ADDR_D14 = 0x16E8A4,
    PORT_TX_DFLEXDPSP3_FIA2_ADDR_D14 = 0x16E8A8,
    PORT_TX_DFLEXDPSP4_FIA2_ADDR_D14 = 0x16E8AC,
} PORT_TX_DFLEXDPSP_INSTANCE_D14;

/*****************************************************************************
Description:  FIA has per Connector register to govern the Pin Assignment of each Type-C Connector. Forexample, DFLEXPA1.DPPATC0 is used to govern the Pin Assignment of Type-C
Connector 0.The Type-C Connector number (e.g. 0 in register DPPATC0) is logical number.

******************************************************************************/
typedef union _PORT_TX_DFLEXPA2_D14 {
    struct
    {
        /******************************************************************************************************************
        Display Port Pin Assignment for Type-C Connector 8 (DPPATC8): 0000 : No Pin Assignment (For Non Type-C DP) 0001 : Pin Assignment A 0010 : Pin Assignment B 0011 : Pin
        Assignment C 0100 : Pin Assignment D 0101 : Pin Assignment E 0110 : Pin Assignment F 0111-1111 : Reserved
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector8 : DD_BITFIELD_RANGE(0, 3); //

        /******************************************************************************************************************
        Similar to register DFLEXPA2.DPPATC8 but this register is for Type-C Connector 9.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector9 : DD_BITFIELD_RANGE(4, 7); //

        /******************************************************************************************************************
        Similar to register DFLEXPA2.DPPATC8 but this register is for Type-C Connector 10.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector10 : DD_BITFIELD_RANGE(8, 11); //

        /******************************************************************************************************************
        Similar to register DFLEXPA2.DPPATC8 but this register is for Type-C Connector 11.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector11 : DD_BITFIELD_RANGE(12, 15); //

        /******************************************************************************************************************
        Similar to register DFLEXPA2.DPPATC8 but this register is for Type-C Connector 12.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector12 : DD_BITFIELD_RANGE(16, 19); //

        /******************************************************************************************************************
        Similar to register DFLEXPA2.DPPATC8 but this register is for Type-C Connector 13.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector13 : DD_BITFIELD_RANGE(20, 23); //

        /******************************************************************************************************************
        Similar to register DFLEXPA2.DPPATC8 but this register is for Type-C Connector 14.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector14 : DD_BITFIELD_RANGE(24, 27); //

        /******************************************************************************************************************
        Similar to register DFLEXPA2.DPPATC8 but this register is for Type-C Connector 15.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector15 : DD_BITFIELD_RANGE(28, 31); //
    };

    DDU32 Value;

} PORT_TX_DFLEXPA2_D14;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXPA2_D14));

/*****************************************************************************
Description:   Dynamic FlexIO DP Scratch Pad (Type-C)
 See the TypeC Programming section for information on how the connector number here maps to the port instance.

******************************************************************************/
typedef union _PORT_TX_DFLEXDPSP_D14 {
    struct
    {
        /******************************************************************************************************************
         DPX4TXLATC0 SOC FW writes to these bits to tell display software the Lane Assignment, which it generates based on the DP Pin Assignment and the Connector Orientation.
        Display software uses this value to determine the number of lanes that can be enabled, and along with other registers, to determine the DP mode programming. See the Typec
        PHY DDI Buffer page for DP mode programming. The 4 bits correspond to 4 TX, i.e. TX[3:0] Lane in PHY. Lower 2 bits correspond to the 2 lower TX lane on the PHY of Type-C
        connector. Upper 2 bits correspond to the upper 2 TX lane on the PHY of Type-C connector. For example, in DP Pin Assignment D (Multi function) and Flip case, the x2 TX lane
        are on the upper TypeC Lane, hence the value written into this register will be 1100b. Another example, in DP Pin Assignment B (Multi function) Active Gen2 cable and Flip
        case, the x1 TX lane is on the 1st TX of upper TypeC Lane, hence the value written into this register will be 0100b.
        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector0 : DD_BITFIELD_RANGE(0, 3); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(4, 6); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(7); //

        /******************************************************************************************************************
        Same definition as DFLEXDPSP1.DPX4TXLATC0, but this register is for Type-C Connector 1.
        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector1 : DD_BITFIELD_RANGE(8, 11); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1

        /******************************************************************************************************************
        This field identifies the IOM firmware that is used.
        \******************************************************************************************************************/
        DDU32 IomFwVersion : DD_BITFIELD_BIT(12); // IOM_FW_VERSION

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(13, 14); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(15); //

        /******************************************************************************************************************
        Same definition as DFLEXDPSP1.DPX4TXLATC0, but this register is for Type-C Connector 2.
        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector2 : DD_BITFIELD_RANGE(16, 19); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(20); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(21, 22); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(23); //

        /******************************************************************************************************************
        Same definition as DFLEXDPSP1.DPX4TXLATC0, but this register is for Type-C Connector 3.
        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector3 : DD_BITFIELD_RANGE(24, 27); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(28); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(29, 30); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(31); //
    };

    DDU32 Value;

} PORT_TX_DFLEXDPSP_D14;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXDPSP_D14));

typedef enum _DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_ENUM_D14
{
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_NO_PIN_ASSIGNMENT_FOR_NON_TYPEC_DP_D14 = 0x0,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_A_D14                   = 0x1,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_B_D14                   = 0x2,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C_D14                   = 0x3,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_D_D14                   = 0x4,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_E_D14                   = 0x5,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_F_D14                   = 0x6,

} DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_ENUM_D14;

/*****************************************************************************
Description:  FIA has per Connector register to govern the Pin Assignment of each Type-C Connector. For example, DFLEXPA1.DPPATC0 is used to govern the Pin Assignment of Type-C
Connector 0. The Type-C Connector number (e.g. "0" in register DPPATC0) is logical number.

******************************************************************************/
typedef union _PORT_TX_DFLEXPA1_D14 {
    struct
    {
        /******************************************************************************************************************
         Display Port Pin Assignment for Type-C Connector 0 (DPPATC0): Assignments A, C, and E have 4 lanes for DP alternate mode. Assignments B, D, and F have 2 lanes for DP
        alternate mode.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector0 : DD_BITFIELD_RANGE(0, 3); // DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0

        /******************************************************************************************************************
        Similar to register DFLEXPA1.DPPATC0 but this register is for Type-C Connector 1.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector1 : DD_BITFIELD_RANGE(4, 7); //

        /******************************************************************************************************************
        Similar to register DFLEXPA1.DPPATC0 but this register is for Type-C Connector 2.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector2 : DD_BITFIELD_RANGE(8, 11); //

        /******************************************************************************************************************
        Similar to register DFLEXPA1.DPPATC0 but this register is for Type-C Connector 3.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector3 : DD_BITFIELD_RANGE(12, 15); //

        /******************************************************************************************************************
        Similar to register DFLEXPA1.DPPATC0 but this register is for Type-C Connector 4.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector4 : DD_BITFIELD_RANGE(16, 19); //

        /******************************************************************************************************************
        Similar to register DFLEXPA1.DPPATC0 but this register is for Type-C Connector 5.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector5 : DD_BITFIELD_RANGE(20, 23); //

        /******************************************************************************************************************
        Similar to register DFLEXPA1.DPPATC0 but this register is for Type-C Connector 6.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector6 : DD_BITFIELD_RANGE(24, 27); //

        /******************************************************************************************************************
        Similar to register DFLEXPA1.DPPATC0 but this register is for Type-C Connector 7.
        \******************************************************************************************************************/
        DDU32 DisplayportPinAssignmentForTypeCConnector7 : DD_BITFIELD_RANGE(28, 31); //
    };

    DDU32 Value;

} PORT_TX_DFLEXPA1_D14;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXPA1_D14));

typedef enum _SRD_CTL_INSTANCE_D14
{
    SRD_CTL_A_ADDR_D14 = 0x60800,
    SRD_CTL_B_ADDR_D14 = 0x61800,
    SRD_CTL_C_ADDR_D14 = 0x62800,
    SRD_CTL_D_ADDR_D14 = 0x63800,
} SRD_CTL_INSTANCE_D14;

/*****************************************************************************
Description:  Restriction : PSR needs to be enabled only when at least one plane is enabled.
Transcoder B/C/D may support link disable for internal testing.Restriction : Only the SRD Enable and Single Frame Update Enable fields can be changed while SRD is enabled. The
other fields must not be changed while SRD is enabled.To use FBC modification tracking for idleness calculations when FBC is disabled, program FBC_CTL CPU Fence Enable,
FBC_CONTROL_SA_REGISTER, FBC_CPU_FENCE_OFFSET_REGISTER, FBC_RT_BASE_ADDR_REGISTER, and BLITTER_TRACKING_REGISTER as they are programmed when FBC is enabled.Cursor front buffer
modifications are not tracked in hardware. If the cursor front buffer is modified, touch (write without changing) any cursor register to trigger the PSR idleness tracking.

******************************************************************************/
typedef union _SRD_CTL_D14 {
    struct
    {
        /******************************************************************************************************************
        This field is the number of idle frames required before entering SRD (sleeping).
        \******************************************************************************************************************/
        DDU32 IdleFrames : DD_BITFIELD_RANGE(0, 3); // IDLE_FRAMES

        /******************************************************************************************************************
        This field selects the TP1 time when training the link on exiting SRD (waking).
        \******************************************************************************************************************/
        DDU32 Tp1Time : DD_BITFIELD_RANGE(4, 5); // TP1_TIME

        /******************************************************************************************************************
         This field selects the TP4 time when training the link on exiting SRD (waking). If this field is set to any value other than "11", TP4 pattern will be sent at PSR reentry.

        Programming Notes:
         Always program TP4 to 11b.
        \******************************************************************************************************************/
        DDU32 Tp4Time : DD_BITFIELD_RANGE(6, 7); // TP4_TIME

        /******************************************************************************************************************
        This field selects the TP2 or TP3 time when training the link on exiting SRD (waking).
        \******************************************************************************************************************/
        DDU32 Tp2Tp3Time : DD_BITFIELD_RANGE(8, 9); // TP2_TP3_TIME

        /******************************************************************************************************************
        This field controls whether the PSR CRC value will be placed in the VSC packet.

        Programming Notes:
        When CRC is enabled, the Max Sleep Timer should be disabled to provide additional power savings. Disable the Max Sleep Timer by setting register 0x6F860 bit 28 to 1.
        Re-enable the Max Sleep Timer by clearing register 0x6F860 bit 28 to 0.Workaround : When Single Frame Update is enabled, the CRC must be disabled for panel compatibility.
        \******************************************************************************************************************/
        DDU32 CrcEnable : DD_BITFIELD_BIT(10); // CRC_ENABLE

        /******************************************************************************************************************
        This field controls whether TP1 is followed by TP2 or TP3 for training the link on exiting SRD (waking).

        Programming Notes:
        This bit impacts PSR2. Clear it before enabling PSR2 and do not set it while PSR2 is enabled.
        \******************************************************************************************************************/
        DDU32 Tp2Tp3Select : DD_BITFIELD_BIT(11); // TP2_TP3_SELECT

        /******************************************************************************************************************
        This field controls whether the AUX channel handshake will be sent when exiting SRD (waking).
        \******************************************************************************************************************/
        DDU32 SkipAuxOnExit : DD_BITFIELD_BIT(12); // SKIP_AUX_ON_EXIT

        /******************************************************************************************************************/
        DDU32 Tps4Control : DD_BITFIELD_BIT(13); // TPS4_CONTROL

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(14, 16); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(17, 19); //

        /******************************************************************************************************************
        This field is the maximum time to spend in SRD (sleeping). It is programmed in increments of approximately 1/8 a second.Programming all 1s gives ~3.875 seconds.

        Programming Notes:
        Restriction : Programming all 0s is invalid.
        \******************************************************************************************************************/
        DDU32 MaxSleepTime : DD_BITFIELD_RANGE(20, 24); // MAX_SLEEP_TIME

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(25, 26); //

        /******************************************************************************************************************
         This field controls the behavior of the link when in SRD (sleeping). The timing generator and pixel data fetches are disabled when the link is disabled. Only pixel data
        fetches are disabled when the link is in standby. This field is ignored by transcoder A/B/C since they only operate in standby.

        Programming Notes:
        Transcoder A/B/C may support link disable for internal testing.
        \******************************************************************************************************************/
        DDU32 LinkCtrl : DD_BITFIELD_BIT(27); // LINK_CTRL

        /******************************************************************************************************************
        This field enables the Adaptive Sync Frame Update mode where a flip will cause a single frame to be sent to the receiver. Updates to this field will take effect at the next
        vertical blank. This field must be enabled with VRR enable.

        Programming Notes:
        Restriction : This mode should only be enabled with the SRD Link Disable mode. This mode does not support VRR Max Shift. However, normal and flipline VRR modes are
        supported.Set register PIPE_MISC field Change Mask for Vblank Vsync Int to 1b (Masked) if vblank or vsync interrupts will be used together with single frame update.
        \******************************************************************************************************************/
        DDU32 AdaptiveSyncFrameUpdate : DD_BITFIELD_BIT(28); // ADAPTIVE_SYNC_FRAME_UPDATE

        /******************************************************************************************************************
        This field restores eDP context to PSR Active on a context restore.

        Programming Notes:
        Restriction : This field is used for hardware communication. Software must not change this field.
        \******************************************************************************************************************/
        DDU32 ContextRestoreToPsrActive : DD_BITFIELD_BIT(29); // CONTEXT_RESTORE_TO_PSR_ACTIVE

        /******************************************************************************************************************
        This field enables the single frame update mode where a plane flip will cause a single frame to be sent to the receiver.Updates to this field will take effect at the next
        vertical blank.

        Programming Notes:
        Restriction : This mode should only be enabled with link standby.  Set register PIPE_MISC field Change Mask for Vblank Vsync Int to 1b (Masked) if vblank or vsync
        interrupts will be used together with single frame update. Workaround : When Single Frame Update is enabled, the CRC must be disabled for panel compatibility.
        \******************************************************************************************************************/
        DDU32 SingleFrameUpdateEnable : DD_BITFIELD_BIT(30); // SINGLE_FRAME_UPDATE_ENABLE

        /******************************************************************************************************************
        This bit enables the Self Refreshing Display function.Updates will take place at the start of the next vertical blank. The port will send SRD VDMs while enabled.When
        idleness conditions have been met for the programmed number of idle frames, hardware will enter SRD (sleep) and can disable the link and stop fetching data from memory.When
        activity occurs, hardware will exit SRD (wake) and re-enable the link and resume fetching data from memory.

        Programming Notes:
        Restriction : SRD must not be enabled when the PSR Setup time from DPCD 00071h is greater than the time for vertical blank minus one line.Restriction : SRD must not be
        enabled together with Interlacing, Black Frame Insertion (BFI), or audio on the same transcoder.
        \******************************************************************************************************************/
        DDU32 SrdEnable : DD_BITFIELD_BIT(31); // SRD_ENABLE
    };

    DDU32 Value;

} SRD_CTL_D14;

C_ASSERT(4 == sizeof(SRD_CTL_D14));

typedef enum _PSR2_CTL_INSTANCE_D14
{
    PSR2_CTL_A_ADDR_D14 = 0x60900,
    PSR2_CTL_B_ADDR_D14 = 0x61900,
} PSR2_CTL_INSTANCE_D14;

/*****************************************************************************
Description:  Restriction : PSR needs to be enabled only when at least one plane is enabled.
Restriction : Only the PSR2 Enable can be changed while PSR2 is enabled. The other fields must not be changed while PSR2 is enabled. Selective Update Tracking Enable must be set
before or along with PSR2 enableRestriction : PSR2 is supported for pipe active sizes up to 5120 pixels wide and 3200 lines tall.To use FBC modification tracking for idleness
calculations when FBC is disabled, program FBC_CTL CPU Fence Enable, FBC_CONTROL_SA_REGISTER, FBC_CPU_FENCE_OFFSET_REGISTER, FBC_RT_BASE_ADDR_REGISTER, and
BLITTER_TRACKING_REGISTER as they are programmed when FBC is enabled.

******************************************************************************/
typedef union _PSR2_CTL_D14 {
    struct
    {
        /******************************************************************************************************************
        This field is the number of idle frames required before entering PSR2 Deep Sleep.

        Programming Notes:
        Write to this field doesn't cause a PSR2 exit and frame update.
        \******************************************************************************************************************/
        DDU32 IdleFrames : DD_BITFIELD_RANGE(0, 3); //

        /******************************************************************************************************************
         This field is the number of frames it takes to enter into Selective Update when PSR2 is enabled. Note: HW takes a minimum of 2frames, so'0' and '1' are are not valid
        entries for this field.

        \******************************************************************************************************************/
        DDU32 FramesBeforeSuEntry : DD_BITFIELD_RANGE(4, 7); // FRAMES_BEFORE_SU_ENTRY

        /******************************************************************************************************************
        This field selects the TP2 time when training the link on exit from PSR2 DeepSleep (waking).
        \******************************************************************************************************************/
        DDU32 Tp2Time : DD_BITFIELD_RANGE(8, 9); // TP2_TIME

        /******************************************************************************************************************
        This field selects the number of lines before the Selective Update Region to send the Fast Wake.

        Programming Notes:
        To program line 9 to 12, block count number bit [28] must be set.
        \******************************************************************************************************************/
        DDU32 FastWake : DD_BITFIELD_RANGE(10, 12); // FAST_WAKE

        /******************************************************************************************************************
        This field selects the number of lines before the Selective Update Region to wake the IO Buffers.

        Programming Notes:
        To program line 9 to 12, block count number bit [28] must be set.
        \******************************************************************************************************************/
        DDU32 IoBufferWake : DD_BITFIELD_RANGE(13, 15); // IO_BUFFER_WAKE

        /******************************************************************************************************************
        This field controls the number of bits to flip within the static Data + ECC value
        \******************************************************************************************************************/
        DDU32 ErrorInjectionFlipBits : DD_BITFIELD_RANGE(16, 17); // ERROR_INJECTION_FLIP_BITS

        /******************************************************************************************************************/
        DDU32 Psr2RamPowerState : DD_BITFIELD_BIT(18); //

        /******************************************************************************************************************
        This bit enables the error injection path within the ECC logic. The static Data + ECC value will be driven into the ECC decoders when enabled.
        \******************************************************************************************************************/
        DDU32 EccErrorInjectionEnable : DD_BITFIELD_BIT(19); // ECC_ERROR_INJECTION_ENABLE

        /******************************************************************************************************************
        This field is the maximum time to spend in PSR2 Selective update without fetching a full frame. It is programmed in increments of sixty frames. Programming all 1s gives
        31x60 frames time.

        Programming Notes:
        Restriction : Programming all 0s disable the forced fetch of a full frame in SU.
        \******************************************************************************************************************/
        DDU32 MaxSuDisableTime : DD_BITFIELD_RANGE(20, 24); // MAX_SU_DISABLE_TIME

        /******************************************************************************************************************/
        DDU32 SuSdpScanlineIndication : DD_BITFIELD_BIT(25); // SU_SDP_SCANLINE_INDICATION

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(26, 27); //

        /******************************************************************************************************************
        This field selects block count number before SU turn on sequence
        \******************************************************************************************************************/
        DDU32 BlockCountNumber : DD_BITFIELD_BIT(28); // BLOCK_COUNT_NUMBER

        /******************************************************************************************************************
        This field restores PSR2 into Deep Sleep State

        Programming Notes:
        Restriction : This bit should only be used with context save restore.
        \******************************************************************************************************************/
        DDU32 ContextRestoreToPsr2DeepSleepState : DD_BITFIELD_BIT(29); // CONTEXT_RESTORE_TO_PSR2_DEEP_SLEEP_STATE

        /******************************************************************************************************************
        After DC6v exit, psr2 state machine restores to sleep state.
        \******************************************************************************************************************/
        DDU32 RestoreToSleep : DD_BITFIELD_BIT(30); // RESTORE_TO_SLEEP

        /******************************************************************************************************************
        This bit enables Revision 2.0 of the Panel Self Refresh function.Updates will take place at the start of the next vertical blank. The port will send PSR2 VDMs while
        enabled.

        Programming Notes:
        Restriction : PSR2 must not be enabled when the PSR Setup time from DPCD 00071h is greater than the time for vertical blank minus one line.Restriction : PSR2 must not be
        enabled together with Interlacing, Black Frame Insertion (BFI), Compression Mode, or S3D.Restriction : Disable FBC when PSR2 is enabled. Clear the register field SRD_CTL
        [TP2 TP3 Select] before enabling this bit. Do not set the register field SRD_CTL [TP2 TP3 Select] while PSR2 is enabled.
        \******************************************************************************************************************/
        DDU32 Psr2Enable : DD_BITFIELD_BIT(31); // PSR2_ENABLE
    };

    DDU32 Value;

} PSR2_CTL_D14;

C_ASSERT(4 == sizeof(PSR2_CTL_D14));

typedef enum _PICA_PHY_CONFIG_CONTROL_INSTANCE_XE3_D
{
    PICA_PHY_CONFIG_CONTROL_0_ADDR_XE3_D = 0x16FE68,
} PICA_PHY_CONFIG_CONTROL_INSTANCE_XE3_D;

/*****************************************************************************
Description:

******************************************************************************/
typedef union _PICA_PHY_CONFIG_CONTROL_XE3_D {
    struct
    {
        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 30); //

        /******************************************************************************************************************
        This bit indicates if 2nd eDP is enabled over a Type-C port based on "eDP on Type-C" strap setting.
        \******************************************************************************************************************/
        DDU32 Edp2OnTypec : DD_BITFIELD_BIT(31); // EDP2_ON_TYPEC
    };

    DDU32 Value;

} PICA_PHY_CONFIG_CONTROL_XE3_D, *PPICA_PHY_CONFIG_CONTROL_XE3_D;

C_ASSERT(4 == sizeof(PICA_PHY_CONFIG_CONTROL_XE3_D));

typedef enum _IOM_DP_RESOURCE_MNG_INSTANCE_XE3P_D
{
    IOM_DP_RESOURCE_MNG_ADDR_XE3P_D = 0x16802C,
} IOM_DP_RESOURCE_MNG_INSTANCE_XE3P_D;

typedef enum _DDI_CONSUMER_VALUE_XE3P_D
{
    CONSUMER_FREE_XE3P_D       = 0x0,
    CONSUMER_TBT0_DPIN0_XE3P_D = 0x1,
    CONSUMER_TBT0_DPIN1_XE3P_D = 0x2,
    CONSUMER_TBT0_DPIN2_XE3P_D = 0x3,
    CONSUMER_TBT1_DPIN0_XE3P_D = 0x5,
    CONSUMER_TBT1_DPIN1_XE3P_D = 0x6,
    CONSUMER_TBT1_DPIN2_XE3P_D = 0x7,
    CONSUMER_TC0_XE3P_D        = 0x8,
    CONSUMER_TC1_XE3P_D        = 0x9,
    CONSUMER_TC2_XE3P_D        = 0xA,
    CONSUMER_TC3_XE3P_D        = 0xB,

} DDI_CONSUMER_VALUE_XE3P_D;

typedef union _IOM_DP_RESOURCE_MNG_XE3P {
    struct
    {
        SIZE32BITS DDI0_CONSUMER : BITFIELD_RANGE(0, 3);
        SIZE32BITS DDI1_CONSUMER : BITFIELD_RANGE(4, 7);
        SIZE32BITS DDI2_CONSUMER : BITFIELD_RANGE(8, 11);
        SIZE32BITS DDI3_CONSUMER : BITFIELD_RANGE(12, 15);
        SIZE32BITS DDI4_CONSUMER : BITFIELD_RANGE(16, 19);
        SIZE32BITS DDI5_CONSUMER : BITFIELD_RANGE(20, 23);
        SIZE32BITS DDI6_CONSUMER : BITFIELD_RANGE(24, 27);
        SIZE32BITS DDI7_CONSUMER : BITFIELD_RANGE(28, 31);
    };
    SIZE32BITS ulValue;
} IOM_DP_RESOURCE_MNG_XE3P, *PIOM_DP_RESOURCE_MNG_XE3P;

C_ASSERT(4 == sizeof(IOM_DP_RESOURCE_MNG_XE3P));

#endif // GEN14INTRREGS_H
