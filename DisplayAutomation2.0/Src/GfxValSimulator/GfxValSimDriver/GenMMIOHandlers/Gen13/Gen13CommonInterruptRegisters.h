/*===========================================================================
; Gen13InterruptRegisters.h - Gen13 InterruptHandler interface
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
;       This file contains all the InterruptHandler interface function and data structure definitions for GEN13
;--------------------------------------------------------------------------*/

#ifndef __GEN13INTERRUPT_REGS_H__
#define __GEN13INTERRUPT_REGS_H__

#include "..\\..\\CommonInclude\\BitDefs.h"
#include "..\\..\\CommonInclude\\\DisplayDefs.h"

typedef enum _MASTER_INTERRUPT_GEN13
{
    MASTER_INTERRUPT_DISABLE_GEN13 = 0x0,
    MASTER_INTERRUPT_ENABLE_GEN13  = 0x1
} MASTER_INTERRUPT_GEN13;

typedef enum _GFX_MSTR_INTR_INSTANCE_GEN13
{
    GFX_MSTR_INTR_ADDR_GEN13 = 0X190010,
} GFX_MSTR_INTR_INSTANCE_GEN13;

#define GEN13_MASTER_INTERRUPT_BIT_POS (31)
#define GEN13_PCU_INTERRUPT_BIT_POS (30)
#define GEN13_DISPLAY_INTERRUPT_BIT_POS (16)
#define GEN13_DW1_INTERRUPT_BIT_POS (1)
#define GEN13_DW0_INTERRUPT_BIT_POS (0)

/*****************************************************************************
Description:  Top level register that indicates interrupt from hardware.
Bits in this register are set interrupts are pending in the underlying PCU, display or GT interrupts
Bspec: https://gfxspecs.intel.com/Predator/Home/Index/53222
******************************************************************************/
typedef union _GFX_MSTR_INTR_GEN13 {
    struct
    {
        DDU32 GtDw0InterruptsPending : DD_BITFIELD_BIT(0);
        DDU32 GtDW1InterruptsPending : DD_BITFIELD_BIT(1);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(2, 15);
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
} GFX_MSTR_INTR_GEN13, *PGFX_MSTR_INTR_GEN13;

C_ASSERT(4 == sizeof(GFX_MSTR_INTR_GEN13));

// IMPLICIT ENUMERATIONS USED BY DISPLAY_INT_CTL_GEN13
//
typedef enum _DISPLAY_INTR_GEN13
{
    DISPLAY_INTR_DISABLE_GEN13 = 0x0,
    DISPLAY_INTR_ENABLE_GEN13  = 0x1,
} DISPLAY_INTR_GEN13;

typedef enum _DISPLAY_INTR_CTL_INSTANCE_GEN13
{
    DISPLAY_INTR_CTL_ADDR_GEN13 = 0x44200,
} DISPLAY_INTR_CTL_INSTANCE_GEN13;

/*****************************************************************************\
This register has the master enable for display interrupts and gives an overview of what interrupts are pending.
An interrupt pending bit will read 1b while one or more interrupts of that category are set (IIR) and enabled (IER).
All Pending Interrupts are ORed together to generate the combined interrupt.
The combined interrupt is ANDed with the Display Interrupt enable to create the display enabled interrupt.
The display enabled interrupt goes to graphics interrupt processing.
The master interrupt enable must be set before any of these interrupts will propagate to graphics interrupt processing.
\*****************************************************************************/
typedef union _DISPLAY_INT_CTL_GEN13 {
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
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(25, 30);
        SIZE32BITS DisplayInterruptEnable : BITFIELD_BIT(31);
    };
    SIZE32BITS ulValue;

} DISPLAY_INT_CTL_GEN13, *PDISPLAY_INT_CTL_GEN13;

C_ASSERT(4 == sizeof(DISPLAY_INT_CTL_GEN13));

// IMPLICIT ENUMERATIONS USED BY DE_PORT_INTR_DEFINITION_GEN13
//
typedef enum _DE_PORT_INTR_INSTANCE_GEN13
{
    DE_PORT_INTR_ADDR_GEN13 = 0x44440,
} DE_PORT_INTR_INSTANCE_GEN13;

/******************************************************************************************************************************************************************************************************************
******************************************************************************************************************************************************************************************************************/
typedef enum _HPD_STATUS_ENUM_GEN13
{
    HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN13    = 0x0,
    HPD_STATUS_SHORT_PULSE_DETECTED_GEN13           = 0x1,
    HPD_STATUS_LONG_PULSE_DETECTED_GEN13            = 0x2,
    HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN13 = 0x3,

} HPD_STATUS_ENUM_GEN13;

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_DDI_GEN13
//
typedef enum _SOUTH_HOT_PLUG_CTL_FOR_DDI_INSTANCE_GEN13
{
    SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN13 = 0xC4030,
} SOUTH_HOT_PLUG_CTL_FOR_DDI_INSTANCE_GEN13;

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
typedef union _SHOTPLUG_CTL_DDI_GEN13 {
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

} SHOTPLUG_CTL_DDI_GEN13, *PSHOTPLUG_CTL_DDI_GEN13;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_DDI_GEN13));

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_TC_GEN13
//
typedef enum _SHOTPLUG_CTL_TC_INSTANCE_GEN13
{
    SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN13 = 0xC4034,
} SHOTPLUG_CTL_TC_INSTANCE_GEN13;

/*****************************************************************************
Description:   The status fields indicate the hot plug detect status on each type C portwhen using non-type C connectors (legacy or static configuration). When HPD is enabled and
either a long or short pulse is detected for a port, one of the status bits will set and the hotplug IIR will be set (if unmasked in the IMR). The status bits are sticky bits,
cleared by writing 1s to the bits. Each HPD pin can be configured as an input or output. The HPD status function will only work when the pin is configured as an input. The HPD
Output Data function will only work when the HPD pin is configured as an output.The short pulse duration is programmed in SHPD_PULSE_CNT.

******************************************************************************/
typedef union _SHOTPLUG_CTL_TC_GEN13 {
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

    DDU32 ulValue;

} SHOTPLUG_CTL_TC_GEN13;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_TC_GEN13));

// IMPLICIT ENUMERATIONS USED BY SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13
//
typedef enum _SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_INSTANCE_GEN13
{
    SDE_ISR_ADDR_GEN13 = 0xC4000,
    SDE_IMR_ADDR_GEN13 = 0xC4004,
    SDE_IIR_ADDR_GEN13 = 0xC4008,
    SDE_IER_ADDR_GEN13 = 0xC400C,
} SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_INSTANCE_GEN13;

/*****************************************************************************\
South Display Engine (SDE) interrupt bits come from events within the south display engine.The SDE_IIR bits are ORed together to generate the South/PCH Display Interrupt Event
which will appear in the North Display Engine Interrupt Control Registers.	The South Display Engine Interrupt Control Registers all share the same bit definitions from this table.
\*****************************************************************************/
typedef union _SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 {
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
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(30, 31); // MBZ
    };
    SIZE32BITS ulValue;

} SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13, *PSOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13;

C_ASSERT(4 == sizeof(SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13));

#endif // GEN13INTRREGS_H

typedef enum _HOTPLUG_CTL_INSTANCE_D13
{
    TBT_HOTPLUG_CTL_ADDR_D13 = 0x44030,
    TC_HOTPLUG_CTL_ADDR_D13  = 0x44038,
} HOTPLUG_CTL_INSTANCE_D13;

/*****************************************************************************
Description:

******************************************************************************/
typedef union _HOTPLUG_CTL_D13 {
    struct
    {
        /******************************************************************************************************************/
        DDU32 Port1HpdStatus : DD_BITFIELD_RANGE(0, 1); // PORT1_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(2); //

        /******************************************************************************************************************/
        DDU32 Port1HpdEnable : DD_BITFIELD_BIT(3); // PORT1_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Port2HpdStatus : DD_BITFIELD_RANGE(4, 5); // PORT2_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(6); //

        /******************************************************************************************************************/
        DDU32 Port2HpdEnable : DD_BITFIELD_BIT(7); // PORT2_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Port3HpdStatus : DD_BITFIELD_RANGE(8, 9); // PORT3_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(10); //

        /******************************************************************************************************************/
        DDU32 Port3HpdEnable : DD_BITFIELD_BIT(11); // PORT3_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Port4HpdStatus : DD_BITFIELD_RANGE(12, 13); // PORT4_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(14); //

        /******************************************************************************************************************/
        DDU32 Port4HpdEnable : DD_BITFIELD_BIT(15); // PORT4_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Port5HpdStatus : DD_BITFIELD_RANGE(16, 17); // PORT5_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(18); //

        /******************************************************************************************************************/
        DDU32 Port5HpdEnable : DD_BITFIELD_BIT(19); // PORT5_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Port6HpdStatus : DD_BITFIELD_RANGE(20, 21); // PORT6_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(22); //

        /******************************************************************************************************************/
        DDU32 Port6HpdEnable : DD_BITFIELD_BIT(23); // PORT6_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Port7HpdStatus : DD_BITFIELD_RANGE(24, 25); // PORT7_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(26); //

        /******************************************************************************************************************/
        DDU32 Port7HpdEnable : DD_BITFIELD_BIT(27); // PORT7_HPD_ENABLE

        /******************************************************************************************************************/
        DDU32 Port8HpdStatus : DD_BITFIELD_RANGE(28, 29); // PORT8_HPD_STATUS

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(30); //

        /******************************************************************************************************************/
        DDU32 Port8HpdEnable : DD_BITFIELD_BIT(31); // PORT8_HPD_ENABLE
    };

    DDU32 Value;

} HOTPLUG_CTL_D13;

C_ASSERT(4 == sizeof(HOTPLUG_CTL_D13));

typedef enum _DE_HPD_INTERRUPT_DEFINITION_INSTANCE_D13
{
    DE_HPD_ISR_ADDR_D13 = 0x44470,
    DE_HPD_IMR_ADDR_D13 = 0x44474,
    DE_HPD_IIR_ADDR_D13 = 0x44478,
    DE_HPD_IER_ADDR_D13 = 0x4447C,
} DE_HPD_INTERRUPT_DEFINITION_INSTANCE_D13;

/*****************************************************************************
Description:   This table indicates which events are mapped to each bit of the Display Engine HPD Interrupt registers. 0x44470 = ISR 0x44474 = IMR 0x44478 = IIR 0x4447C = IER

******************************************************************************/
typedef union _DE_HPD_INTERRUPT_DEFINITION_D13 {
    struct
    {
        /******************************************************************************************************************
        The ISR gives the live state of the HPD for thunderbolt. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tbt1Hotplug : DD_BITFIELD_BIT(0); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for thunderbolt. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tbt2Hotplug : DD_BITFIELD_BIT(1); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for thunderbolt. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tbt3Hotplug : DD_BITFIELD_BIT(2); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for thunderbolt. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tbt4Hotplug : DD_BITFIELD_BIT(3); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for thunderbolt. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tbt5Hotplug : DD_BITFIELD_BIT(4); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for thunderbolt. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tbt6Hotplug : DD_BITFIELD_BIT(5); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for thunderbolt. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tbt7Hotplug : DD_BITFIELD_BIT(6); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for thunderbolt. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tbt8Hotplug : DD_BITFIELD_BIT(7); //

        /******************************************************************************************************************/
        DDU32 Unused8 : DD_BITFIELD_BIT(8); //

        /******************************************************************************************************************/
        DDU32 Unused9 : DD_BITFIELD_BIT(9); //

        /******************************************************************************************************************/
        DDU32 Unused10 : DD_BITFIELD_BIT(10); //

        /******************************************************************************************************************/
        DDU32 Unused11 : DD_BITFIELD_BIT(11); //

        /******************************************************************************************************************/
        DDU32 Unused12 : DD_BITFIELD_BIT(12); //

        /******************************************************************************************************************/
        DDU32 Unused13 : DD_BITFIELD_BIT(13); //

        /******************************************************************************************************************/
        DDU32 Unused14 : DD_BITFIELD_BIT(14); //

        /******************************************************************************************************************/
        DDU32 Unused15 : DD_BITFIELD_BIT(15); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for typeC DP alternate mode. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tc1Hotplug : DD_BITFIELD_BIT(16); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for typeC DP alternate mode. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tc2Hotplug : DD_BITFIELD_BIT(17); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for typeC DP alternate mode. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tc3Hotplug : DD_BITFIELD_BIT(18); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for typeC DP alternate mode. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tc4Hotplug : DD_BITFIELD_BIT(19); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for typeC DP alternate mode. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tc5Hotplug : DD_BITFIELD_BIT(20); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for typeC DP alternate mode. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tc6Hotplug : DD_BITFIELD_BIT(21); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for typeC DP alternate mode. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tc7Hotplug : DD_BITFIELD_BIT(22); //

        /******************************************************************************************************************
        The ISR gives the live state of the HPD for typeC DP alternate mode. The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \******************************************************************************************************************/
        DDU32 Tc8Hotplug : DD_BITFIELD_BIT(23); //

        /******************************************************************************************************************/
        DDU32 Unused24 : DD_BITFIELD_BIT(24); //

        /******************************************************************************************************************/
        DDU32 Unused25 : DD_BITFIELD_BIT(25); //

        /******************************************************************************************************************/
        DDU32 Unused26 : DD_BITFIELD_BIT(26); //

        /******************************************************************************************************************/
        DDU32 Unused27 : DD_BITFIELD_BIT(27); //

        /******************************************************************************************************************/
        DDU32 Unused28 : DD_BITFIELD_BIT(28); //

        /******************************************************************************************************************/
        DDU32 Unused29 : DD_BITFIELD_BIT(29); //

        /******************************************************************************************************************/
        DDU32 Unused30 : DD_BITFIELD_BIT(30); //

        /******************************************************************************************************************/
        DDU32 Unused31 : DD_BITFIELD_BIT(31); //
    };

    DDU32 Value;

} DE_HPD_INTERRUPT_DEFINITION_D13;

C_ASSERT(4 == sizeof(DE_HPD_INTERRUPT_DEFINITION_D13));

/*********************************************************************************************************************************************************************************************
*************************************************************************************************************************************************************************************************/

typedef enum _TCSS_DDI_STATUS_INSTANCE_D13
{
    TCSS_DDI_STATUS_1_ADDR_D13 = 0x161500,
    TCSS_DDI_STATUS_2_ADDR_D13 = 0x161504,
    TCSS_DDI_STATUS_3_ADDR_D13 = 0x161508,
    TCSS_DDI_STATUS_4_ADDR_D13 = 0x16150C,
} TCSS_DDI_STATUS_INSTANCE_D13;

/*****************************************************************************
Description:

******************************************************************************/
typedef union _TCSS_DDI_STATUS_D13 {
    struct
    {
        /******************************************************************************************************************
         HPD live status for dp_alt_mode. This drives the DP-alt HPD wire to DE.
         \******************************************************************************************************************/
        DDU32 Hpd_Live_Status_Alt : DD_BITFIELD_BIT(0); //

        /******************************************************************************************************************
        HPD live status for TBT. This drives the TBT HPD wire to DE.
        \******************************************************************************************************************/
        DDU32 Hpd_Live_Status_Tbt : DD_BITFIELD_BIT(1); //

        /******************************************************************************************************************
        PHY and FIA are ready for use for display in DP-alt or native/fixed/legacy modes. Not set for thunderbolt modes. PHY_READY_FOR_DE (AKA DPPMS)
        \******************************************************************************************************************/
        DDU32 Ready : DD_BITFIELD_BIT(2); //

        /******************************************************************************************************************
        Readback of display phy ownership wire (driven from DE), AKS SSS (safe state status).
        \******************************************************************************************************************/
        DDU32 Sss : DD_BITFIELD_BIT(3); //

        /******************************************************************************************************************
        Which type_c/TBT port HPD is sent from.
        \******************************************************************************************************************/
        DDU32 Src_Port_Num : DD_BITFIELD_RANGE(4, 7); //

        /******************************************************************************************************************
        HPD flow is in progress.
        \******************************************************************************************************************/
        DDU32 Hpd_In_Progress : DD_BITFIELD_BIT(8); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(9, 31); //
    };

    DDU32 Value;

} TCSS_DDI_STATUS_D13;

C_ASSERT(4 == sizeof(TCSS_DDI_STATUS_D13));

typedef enum _DDI_BUF_CTL_INSTANCE_D13
{
    DDI_BUF_CTL_A_ADDR_D13     = 0x64000,
    DDI_BUF_CTL_B_ADDR_D13     = 0x64100,
    DDI_BUF_CTL_C_ADDR_D13     = 0x64200,
    DDI_BUF_CTL_USBC1_ADDR_D13 = 0x64300,
    DDI_BUF_CTL_USBC2_ADDR_D13 = 0x64400,
    DDI_BUF_CTL_USBC3_ADDR_D13 = 0x64500,
    DDI_BUF_CTL_USBC4_ADDR_D13 = 0x64600,
    DDI_BUF_CTL_D_ADDR_D13     = 0x64700,
    DDI_BUF_CTL_E_ADDR_D13     = 0x64800,
} DDI_BUF_CTL_INSTANCE_D13;

/*****************************************************************************
Description:  Do not read or write the register when the associated power well is disabled.

******************************************************************************/
typedef union _DDI_BUF_CTL_D13 {
    struct
    {
        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(0); //

        /******************************************************************************************************************
        This bit selects the number of lanes to be enabled on the DDI link for DisplayPort.

        Programming Notes:
        Restriction : When in DisplayPort mode the value selected here must match the value selected in TRANS_DDI_FUNC_CTL attached to this DDI.Restriction : This field must not be
        changed while the DDI is enabled.
        \******************************************************************************************************************/
        DDU32 DpPortWidthSelection : DD_BITFIELD_RANGE(1, 3); // DP_PORT_WIDTH_SELECTION

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(4, 5); //

        /******************************************************************************************************************
         This field is configured to take ownership of the type-C PHY as part of the type-C connect and disconnect flows. This field is ignored for DDIs not associated with type-C
        ports. The ownership is de-asserted during reset preparation for FLR and warm resets.
        \******************************************************************************************************************/
        DDU32 TypecPhyOwnership : DD_BITFIELD_BIT(6); // TYPEC_PHY_OWNERSHIP

        /******************************************************************************************************************
        This bit indicates when the DDI buffer is idle.
        \******************************************************************************************************************/
        DDU32 DdiIdleStatus : DD_BITFIELD_BIT(7); // DDI_IDLE_STATUS

        /******************************************************************************************************************
         Specifies the number of symbol clocks delay used to stagger assertion/deassertion of the port lane enables. The target time recommended by circuit team is 100ns or
        greater. The delay should be programmed based on link clock frequency. This staggering delay is ONLY required when the port is used in USB Type C mode. Otherwise the
        default delay is zero which means no staggering. Example: 270MHz link clock = 1/270MHz = 3.7ns. (100ns/3.7ns)=27.02 symbols. Round up to 28.
        \******************************************************************************************************************/
        DDU32 UsbTypeCDpLaneStaggeringDelay : DD_BITFIELD_RANGE(8, 15); //

        /******************************************************************************************************************
        This field enables lane reversal within the port. Lane reversal swaps the data on the lanes as they are output from the port.

        Programming Notes:
        Restriction : This field must not be changed while the DDI is enabled. Type-C/TBT dynamic connections: The DDIs going to thunderbolt or USB-C DP alternate mode should not
        be reversed here. The reversal is taken care of in the FIA. Static/fixed connections (DP/HDMI) through FIA: In the case of static connections such as "No pin assignment
        (Non Type-C DP)", DDIs will use this lane reversal bit. All other connections: DDIs will use this lane reversal bit.
        \******************************************************************************************************************/
        DDU32 PortReversal : DD_BITFIELD_BIT(16); // PORT_REVERSAL

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(17); //

        /******************************************************************************************************************
         This value represents PHY data lane width. Note that there are 2 PHY data lanes per port, each supporting 2 TX differential pairs. Display controller will use only one
        copy of this field per port. FIA will propagate this value to all PHY lanes assigned to display. Example : When 2 is selected as per PIPE specification, it means 32/40 bit
        mode for each of PHY TX lane. This field is ignored by non Type-C PHYs.
        \******************************************************************************************************************/
        DDU32 PhyLaneWidth : DD_BITFIELD_RANGE(18, 19); // PHY_LANE_WIDTH

        /******************************************************************************************************************
         This field indicates PHY link rate (Gbps) in blocks. This field is programmed based on HDMI or DP port type. Programming of this field must match PLL (PLL1 or PLL2)
        programming. This field is applicable to Type-C PHYs only. Non Type-C PHYs will ignore this field.
        \******************************************************************************************************************/
        DDU32 PhyLinkRate : DD_BITFIELD_RANGE(20, 23); // PHY_LINK_RATE

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(24, 27); //

        /******************************************************************************************************************
         Enables adjustment of Phy parameters such as voltage swing and pre emphasis outside lnik training process. This field is conditioned on "override training enable"
        (DDI_BUF_CTL[29]).
        \******************************************************************************************************************/
        DDU32 PhyParamAdjust : DD_BITFIELD_BIT(28); // PHY_PARAM_ADJUST

        /******************************************************************************************************************
        This field enables the override on the training enable signal that tells the DDI I/O to pick up any DDI voltage swing and pre-emphasis changes.
        \******************************************************************************************************************/
        DDU32 OverrideTrainingEnable : DD_BITFIELD_BIT(29); // OVERRIDE_TRAINING_ENABLE

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(30); //

        /******************************************************************************************************************
        This bit enables the DDI buffer.
        \******************************************************************************************************************/
        DDU32 DdiBufferEnable : DD_BITFIELD_BIT(31); // DDI_BUFFER_ENABLE
    };

    DDU32 Value;

} DDI_BUF_CTL_D13;

C_ASSERT(4 == sizeof(DDI_BUF_CTL_D13));

typedef enum _PWR_WELL_CTL_DDI_INSTANCE_D13
{
    PWR_WELL_CTL_DDI1_ADDR_D13 = 0x45450,
    PWR_WELL_CTL_DDI2_ADDR_D13 = 0x45454,
    PWR_WELL_CTL_DDI4_ADDR_D13 = 0x4545C,
} PWR_WELL_CTL_DDI_INSTANCE_D13;

/*****************************************************************************
Description:   This register is used for display power control. There are multiple instances of this register format to allow software components to have parallel control of the
display power. PWR_WELL_CTL _DDI1 is generally used for BIOS to control power. PWR_WELL_CTL_DDI2 is generally used for driver to control power. The power enable requests from all
sources are logically ORd together to enable the power, so the power will only disable after all sources have requested the power to disable. When a power well is disabled (powered
down), access to any registers in the power well will complete, but write data will be dropped and read data will be all zeroes. The display connections diagram indicates which
functional blocks are contained in each power well. The display MMIO register specification has a field for each register to indicate which power well it is in. PWR_WELL_CTL_DDI4
is used for debug power well control.Restriction : The power request field must not be changed for a resource while a power enable/disable for that resource is currently in
progress, as indicated by power well state for that resource.

******************************************************************************/
typedef union _PWR_WELL_CTL_DDI_D13 {
    struct
    {
        /******************************************************************************************************************
        This field indicates the status of power for DDI A IO.
        \******************************************************************************************************************/
        DDU32 DdiAIoPowerState : DD_BITFIELD_BIT(0); // DDI_A_IO_POWER_STATE

        /******************************************************************************************************************
        This field requests power for DDI A IO to enable or disable.
        \******************************************************************************************************************/
        DDU32 DdiAIoPowerRequest : DD_BITFIELD_BIT(1); // DDI_A_IO_POWER_REQUEST

        /******************************************************************************************************************
        This field indicates the status of power for DDI B IO.
        \******************************************************************************************************************/
        DDU32 DdiBIoPowerState : DD_BITFIELD_BIT(2); // DDI_B_IO_POWER_STATE

        /******************************************************************************************************************
        This field requests power for DDI B IO to enable or disable.
        \******************************************************************************************************************/
        DDU32 DdiBIoPowerRequest : DD_BITFIELD_BIT(3); // DDI_B_IO_POWER_REQUEST

        /******************************************************************************************************************
        This field indicates the status of power for DDI C IO.
        \******************************************************************************************************************/
        DDU32 DdiCIoPowerState : DD_BITFIELD_BIT(4); // DDI_C_IO_POWER_STATE

        /******************************************************************************************************************
        This field requests power for DDI C IO to enable or disable.
        \******************************************************************************************************************/
        DDU32 DdiCIoPowerRequest : DD_BITFIELD_BIT(5); // DDI_C_IO_POWER_REQUEST

        /******************************************************************************************************************
        This field indicates the status of power for USBC1 IO.
        \******************************************************************************************************************/
        DDU32 Usbc1IoPowerState : DD_BITFIELD_BIT(6); //

        /******************************************************************************************************************
        This field requests power for USBC1 IO to enable or disable.
        \******************************************************************************************************************/
        DDU32 Usbc1IoPowerRequest : DD_BITFIELD_BIT(7); //

        /******************************************************************************************************************
        This field indicates the status of power for USBC2 IO.
        \******************************************************************************************************************/
        DDU32 Usbc2IoPowerState : DD_BITFIELD_BIT(8); //

        /******************************************************************************************************************
        This field requests power for USBC2 IO to enable or disable.
        \******************************************************************************************************************/
        DDU32 Usbc2IoPowerRequest : DD_BITFIELD_BIT(9); //

        /******************************************************************************************************************
        This field indicates the status of power for USBC3 IO.
        \******************************************************************************************************************/
        DDU32 Usbc3IoPowerState : DD_BITFIELD_BIT(10); //

        /******************************************************************************************************************
        This field requests power for USBC3 IO to enable or disable.
        \******************************************************************************************************************/
        DDU32 Usbc3IoPowerRequest : DD_BITFIELD_BIT(11); //

        /******************************************************************************************************************
        This field indicates the status of power for USBC4 IO.
        \******************************************************************************************************************/
        DDU32 Usbc4IoPowerState : DD_BITFIELD_BIT(12); //

        /******************************************************************************************************************
        This field requests power for USBC4 IO to enable or disable.
        \******************************************************************************************************************/
        DDU32 Usbc4IoPowerRequest : DD_BITFIELD_BIT(13); //

        /******************************************************************************************************************
        This field indicates the status of power for DDI D IO.
        \******************************************************************************************************************/
        DDU32 DdiDIoPowerState : DD_BITFIELD_BIT(14); // DDI_D_IO_POWER_STATE

        /******************************************************************************************************************
        This field requests power for DDI D IO to enable or disable.
        \******************************************************************************************************************/
        DDU32 DdiDIoPowerRequest : DD_BITFIELD_BIT(15); // DDI_D_IO_POWER_REQUEST

        /******************************************************************************************************************
        This field indicates the status of power for DDI E IO.
        \******************************************************************************************************************/
        DDU32 DdiEIoPowerState : DD_BITFIELD_BIT(16); // DDI_E_IO_POWER_STATE

        /******************************************************************************************************************
        This field requests power for DDI E IO to enable or disable.
        \******************************************************************************************************************/
        DDU32 DdiEIoPowerRequest : DD_BITFIELD_BIT(17); // DDI_E_IO_POWER_REQUEST

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(18, 22); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(23, 31); //
    };

    DDU32 Value;

} PWR_WELL_CTL_DDI_D13;

C_ASSERT(4 == sizeof(PWR_WELL_CTL_DDI_D13));

/*********************************************************************************************************************************************************************************************
*************************************************************************************************************************************************************************************************/

typedef enum _DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_ENUM_D13
{
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_NO_PIN_ASSIGNMENT_FOR_NON_TYPEC_DP_D13 = 0x0,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_A_D13                   = 0x1,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_B_D13                   = 0x2,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C_D13                   = 0x3,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_D_D13                   = 0x4,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_E_D13                   = 0x5,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_F_D13                   = 0x6,

} DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_ENUM_D13;

typedef enum _PORT_TX_DFLEXPA1_INSTANCE_D13
{
    PORT_TX_DFLEXPA1_FIA1_ADDR_D13 = 0x163880,
    PORT_TX_DFLEXPA1_FIA2_ADDR_D13 = 0x16E880,
} PORT_TX_DFLEXPA1_INSTANCE_D13;

/*****************************************************************************
Description:  FIA has per Connector register to govern the Pin Assignment of each Type-C Connector. For example, DFLEXPA1.DPPATC0 is used to govern the Pin Assignment of Type-C
Connector 0. The Type-C Connector number (e.g. "0" in register DPPATC0) is logical number.

******************************************************************************/
typedef union _PORT_TX_DFLEXPA1_D13 {
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

} PORT_TX_DFLEXPA1_D13;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXPA1_D13));

typedef enum _DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_ENUM_D13
{
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX0_D13     = 0x1,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX1_D13     = 0x2,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX10_D13    = 0x3,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX2_D13     = 0x4,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX2_TX0_D13 = 0x5,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX3_D13     = 0x8,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX32_D13    = 0xC,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX30_D13    = 0xF,

} DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_ENUM_D13;

typedef enum _DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_ENUM_D13
{
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX0_D13     = 0x1,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX1_D13     = 0x2,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX10_D13    = 0x3,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX2_D13     = 0x4,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX2_TX0_D13 = 0x5,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX3_D13     = 0x8,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX32_D13    = 0xC,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX30_D13    = 0xF,

} DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_ENUM_D13;

typedef enum _IOM_FW_VERSION_ENUM_D13
{
    IOM_FW_VERSION_OLD_IOM_FW_D13                   = 0x0,
    IOM_FW_VERSION_IOM_FW_WITH_MFD_GEN2_SUPPORT_D13 = 0x1,

} IOM_FW_VERSION_ENUM_D13;

typedef enum _DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_ENUM_D13
{
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX0_D13     = 0x1,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX1_D13     = 0x2,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX10_D13    = 0x3,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX2_D13     = 0x4,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX2_TX0_D13 = 0x5,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX3_D13     = 0x8,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX32_D13    = 0xC,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX30_D13    = 0xF,

} DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_ENUM_D13;

typedef enum _DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_ENUM_D13
{
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX0_D13     = 0x1,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX1_D13     = 0x2,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX10_D13    = 0x3,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX2_D13     = 0x4,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX2_TX0_D13 = 0x5,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX3_D13     = 0x8,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX32_D13    = 0xC,
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX30_D13    = 0xF,

} DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_ENUM_D13;

typedef enum _PORT_TX_DFLEXDPSP_INSTANCE_D13
{
    PORT_TX_DFLEXDPSP1_FIA1_ADDR_D13 = 0x1638A0,
    PORT_TX_DFLEXDPSP2_FIA1_ADDR_D13 = 0x1638A4,
    PORT_TX_DFLEXDPSP3_FIA1_ADDR_D13 = 0x1638A8,
    PORT_TX_DFLEXDPSP4_FIA1_ADDR_D13 = 0x1638AC,
    PORT_TX_DFLEXDPSP1_FIA2_ADDR_D13 = 0x16E8A0,
    PORT_TX_DFLEXDPSP2_FIA2_ADDR_D13 = 0x16E8A4,
    PORT_TX_DFLEXDPSP3_FIA2_ADDR_D13 = 0x16E8A8,
    PORT_TX_DFLEXDPSP4_FIA2_ADDR_D13 = 0x16E8AC,
} PORT_TX_DFLEXDPSP_INSTANCE_D13;

/*****************************************************************************
Description:   Dynamic FlexIO DP Scratch Pad (Type-C)
 See the TypeC Programming section for information on how the connector number here maps to the port instance.

******************************************************************************/
typedef union _PORT_TX_DFLEXDPSP_D13 {
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

} PORT_TX_DFLEXDPSP_D13;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXDPSP_D13));

typedef enum _SRD_CTL_INSTANCE_D13
{
    SRD_CTL_A_ADDR_D13 = 0x60800,
    SRD_CTL_B_ADDR_D13 = 0x61800,
    SRD_CTL_C_ADDR_D13 = 0x62800,
    SRD_CTL_D_ADDR_D13 = 0x63800,
} SRD_CTL_INSTANCE_D13;

/*****************************************************************************
Description:  Restriction : PSR needs to be enabled only when at least one plane is enabled.
Transcoder B/C/D may support link disable for internal testing.Restriction : Only the SRD Enable and Single Frame Update Enable fields can be changed while SRD is enabled. The
other fields must not be changed while SRD is enabled.To use FBC modification tracking for idleness calculations when FBC is disabled, program FBC_CTL CPU Fence Enable,
FBC_CONTROL_SA_REGISTER, FBC_CPU_FENCE_OFFSET_REGISTER, FBC_RT_BASE_ADDR_REGISTER, and BLITTER_TRACKING_REGISTER as they are programmed when FBC is enabled.Cursor front buffer
modifications are not tracked in hardware. If the cursor front buffer is modified, touch (write without changing) any cursor register to trigger the PSR idleness tracking.

******************************************************************************/
typedef union _SRD_CTL_D13 {
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

} SRD_CTL_D13;

C_ASSERT(4 == sizeof(SRD_CTL_D13));

typedef enum _PSR2_CTL_INSTANCE_D13
{
    PSR2_CTL_A_ADDR_D13 = 0x60900,
    PSR2_CTL_B_ADDR_D13 = 0x61900,
} PSR2_CTL_INSTANCE_D13;

/*****************************************************************************
Description:  Restriction : PSR needs to be enabled only when at least one plane is enabled.
Restriction : Only the PSR2 Enable can be changed while PSR2 is enabled. The other fields must not be changed while PSR2 is enabled. Selective Update Tracking Enable must be set
before or along with PSR2 enableRestriction : PSR2 is supported for pipe active sizes up to 5120 pixels wide and 3200 lines tall.To use FBC modification tracking for idleness
calculations when FBC is disabled, program FBC_CTL CPU Fence Enable, FBC_CONTROL_SA_REGISTER, FBC_CPU_FENCE_OFFSET_REGISTER, FBC_RT_BASE_ADDR_REGISTER, and
BLITTER_TRACKING_REGISTER as they are programmed when FBC is enabled.

******************************************************************************/
typedef union _PSR2_CTL_D13 {
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
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(26); //

        /******************************************************************************************************************
        This field selects whether the frame sync will be sent on Aux channel.

        Programming Notes:
        Restriction : Must be programmed to match the panel's requirements.
        \******************************************************************************************************************/
        DDU32 AuxFrameSyncEnable : DD_BITFIELD_BIT(27); // AUX_FRAME_SYNC_ENABLE

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

} PSR2_CTL_D13;

C_ASSERT(4 == sizeof(PSR2_CTL_D13));