/*===========================================================================
; InterruptHandler.h - IceLake/IceLake-LP InterruptHandler interface
;----------------------------------------------------------------------------
;   Copyright (c) Intel Corporation (2000 - 2017)
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
;       This file contains all the InterruptHandler interface function and data structure definitions for IceLake/IceLake-LP
;--------------------------------------------------------------------------*/

#ifndef __GEN11INTERRUPT_REGS_H__
#define __GEN11INTERRUPT_REGS_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\CommonInclude\\BitDefs.h"
#include "..\\CommonInclude\\\DisplayDefs.h"

typedef enum _MASTER_INTERRUPT_ICL
{
    MASTER_INTERRUPT_DISABLE_ICL = 0x0,
    MASTER_INTERRUPT_ENABLE_ICL  = 0x1
} MASTER_INTERRUPT_ICL;

typedef enum _GFX_MSTR_INTR_INSTANCE_ICL
{
    GFX_MSTR_INTR_ADDR_ICL = 0X190010,
} GFX_MSTR_INTR_INSTANCE_ICL;

#define GEN11_MASTER_INTERRUPT_BIT_POS (31)
#define GEN11_PCU_INTERRUPT_BIT_POS (30)
#define GEN11_DISPLAY_INTERRUPT_BIT_POS (16)
#define GEN11_DW1_INTERRUPT_BIT_POS (1)
#define GEN11_DW0_INTERRUPT_BIT_POS (0)

/*****************************************************************************
Description:  Top level register that indicates interrupt from hardware.
Bits in this register are set interrupts are pending in the underlying PCU, display or GT interrupts

******************************************************************************/
typedef union _GFX_MSTR_INTR_ICL {
    struct
    {
        /******************************************************************************************************************

        \******************************************************************************************************************/
        DDU32 GtDw0InterruptsPending : DD_BITFIELD_BIT(0); // GT_DW0

        /******************************************************************************************************************

        \******************************************************************************************************************/
        DDU32 GtDW1InterruptsPending : DD_BITFIELD_BIT(1); // GT_DW1

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(2, 15); // RESERVED

        /******************************************************************************************************************

        \******************************************************************************************************************/
        DDU32 DisplayInterruptsPending : DD_BITFIELD_BIT(16); // DISPLAY

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(17, 28); // RESERVED

        /******************************************************************************************************************

        \******************************************************************************************************************/
        DDU32 GuMiscInterruptsPending : DD_BITFIELD_BIT(29); // GU_MISC

        /******************************************************************************************************************

        \******************************************************************************************************************/
        DDU32 PcuInterruptsPending : DD_BITFIELD_BIT(30); // PCU

        /******************************************************************************************************************
        This is the master control for graphics interrupts. This must be enabled for any of these interrupts to propagate to PCI device 2 interrupt processing.

        \******************************************************************************************************************/
        DDU32 MasterInterruptEnable : DD_BITFIELD_BIT(31); // MASTER_INTERRUPT
    };

    DDU32 Value;
} GFX_MSTR_INTR_ICL, *PGFX_MSTR_INTR_ICL;

C_ASSERT(4 == sizeof(GFX_MSTR_INTR_ICL));

// IMPLICIT ENUMERATIONS USED BY DISPLAY_INT_CTL_ICL
//
typedef enum _DISPLAY_INTR_ICL
{
    DISPLAY_INTR_DISABLE_ICL = 0x0,
    DISPLAY_INTR_ENABLE_ICL  = 0x1,
} DISPLAY_INTR_ICL;

typedef enum _DISPLAY_INTR_CTL_INSTANCE_ICL
{
    DISPLAY_INTR_CTL_ADDR_ICL = 0x44200,
} DISPLAY_INTR_CTL_INSTANCE_ICL;

typedef enum _DISPLAY_INT_CTL_MASKS_ICL
{
    DISPLAY_INT_CTL_MASKS_WO_ICL  = 0x0,
    DISPLAY_INT_CTL_MASKS_MBZ_ICL = 0x0,
    DISPLAY_INT_CTL_MASKS_PBC_ICL = 0x0,
} DISPLAY_INT_CTL_MASKS_ICL;

/*****************************************************************************\
This register has the master enable for display interrupts and gives an overview of what interrupts are pending.
An interrupt pending bit will read 1b while one or more interrupts of that category are set (IIR) and enabled (IER).
All Pending Interrupts are ORed together to generate the combined interrupt.
The combined interrupt is ANDed with the Display Interrupt enable to create the display enabled interrupt.
The display enabled interrupt goes to graphics interrupt processing.
The master interrupt enable must be set before any of these interrupts will propagate to graphics interrupt processing.
\*****************************************************************************/
typedef union _DISPLAY_INT_CTL_ICL {
    struct
    {
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(0, 15); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        SIZE32BITS DePipeAInterruptsPending : BITFIELD_BIT(16); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        SIZE32BITS DePipeBInterruptsPending : BITFIELD_BIT(17); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        SIZE32BITS DePipeCInterruptsPending : BITFIELD_BIT(18); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        SIZE32BITS DePipeDInterruptsPending : BITFIELD_BIT(19); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        SIZE32BITS DePortInterruptsPending : BITFIELD_BIT(20); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        SIZE32BITS DeHpdInterruptsPending : BITFIELD_BIT(21); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        SIZE32BITS DeMiscInterruptsPending : BITFIELD_BIT(22); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        The PCH Display interrupt is configured through the SDE interrupt registers.
        \*****************************************************************************/
        SIZE32BITS DePchInterruptsPending : BITFIELD_BIT(23); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        SIZE32BITS AudioCodecInterruptsPending : BITFIELD_BIT(24); //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(25, 30);  //

        /*****************************************************************************\
        This is the master control for display interrupts.
        This must be enabled for any of these interrupts to propagate to graphics interrupt processing.
        \*****************************************************************************/
        SIZE32BITS DisplayInterruptEnable : BITFIELD_BIT(31); // DISPLAY_INTR_ENABLE_ICL
    };
    SIZE32BITS ulValue;

} DISPLAY_INT_CTL_ICL, *PDISPLAY_INT_CTL_ICL;

C_ASSERT(4 == sizeof(DISPLAY_INT_CTL_ICL));

// IMPLICIT ENUMERATIONS USED BY DE_PORT_INTR_DEFINITION_ICL
//
typedef enum _DE_PORT_INTR_INSTANCE_ICL
{
    DE_PORT_INTR_ADDR_ICL = 0x44440,
} DE_PORT_INTR_INSTANCE_ICL;

typedef enum _DE_PORT_INTR_ICL
{
    DE_PORT_INTR_WO_ICL  = 0x0,
    DE_PORT_INTR_MBZ_ICL = 0x0,
    DE_PORT_INTR_PBC_ICL = 0x0,
} DE_PORT_INTR_ICL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine Port Interrupt registers.
0x44440 = ISR
0x44444 = IMR
0x44448 = IIR
0x4444C = IER
\*****************************************************************************/
typedef union _DE_PORT_INTR_DEFINITION_ICL {
    struct
    {

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI A done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        SIZE32BITS Aux_Channel_A : BITFIELD_BIT(0); //

        /*****************************************************************************\
        The ISR is an active high pulse when any of the unmasked events in GMBUS4 Interrupt Mask register occur.
        This field is only used on projects that have GMBUS integrated into the north display.
        Projects that have GMBUS in the south display have the GMBUS interrupt in the south display interrupts.
        \*****************************************************************************/
        SIZE32BITS Gmbus : BITFIELD_BIT(1);                //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(2); //

        /*****************************************************************************\
        The ISR gives the live state of the DDI HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        This field is unused in projects that have a PCH.
        \*****************************************************************************/
        SIZE32BITS DdiAHotplug : BITFIELD_BIT(3); //

        /*****************************************************************************\
        The ISR gives the live state of the DDI HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        This field is unused in projects that have a PCH.
        \*****************************************************************************/
        SIZE32BITS DdiBHotplug : BITFIELD_BIT(4); //

        /*****************************************************************************\
        The ISR gives the live state of the DDI HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        This field is unused in projects that have a PCH.
        \*****************************************************************************/
        SIZE32BITS DdiCHotplug : BITFIELD_BIT(5);                //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(6, 22); //

        /*****************************************************************************\
        The ISR is an active high level indicating a TE interrupt is set in DSI_INTER_IDENT_REG_0.
        \*****************************************************************************/
        SIZE32BITS Dsi0Te : BITFIELD_BIT(23); //

        /*****************************************************************************\
        The ISR is an active high level indicating a TE interrupt is set in DSI_INTER_IDENT_REG_1.
        \*****************************************************************************/
        SIZE32BITS Dsi1Te : BITFIELD_BIT(24); //

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI B done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        SIZE32BITS AuxChannelB : BITFIELD_BIT(25); //

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI C done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        SIZE32BITS AuxChannelC : BITFIELD_BIT(26); //

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI D done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        SIZE32BITS AuxChannelD : BITFIELD_BIT(27); //

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI F done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        SIZE32BITS AuxChannelF : BITFIELD_BIT(28); //

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI E done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        SIZE32BITS AuxChannelE : BITFIELD_BIT(29); //

        /*****************************************************************************\
        The ISR is an active high level indicating an interrupt is set in DSI_INTER_IDENT_REG_0.
        \*****************************************************************************/
        SIZE32BITS Dsi0 : BITFIELD_BIT(30); //

        /*****************************************************************************\
        The ISR is an active high level indicating an interrupt is set in DSI_INTER_IDENT_REG_1.
        \*****************************************************************************/
        SIZE32BITS Dsi1 : BITFIELD_BIT(31); //
    };
    SIZE32BITS ulValue;

} DE_PORT_INTR_DEFINITION_ICL, *PDE_PORT_INTR_DEFINITION_ICL;

C_ASSERT(4 == sizeof(DE_PORT_INTR_DEFINITION_ICL));

// IMPLICIT ENUMERATIONS USED BY DE_HPD_INTR_DEFINITION_ICL
//
typedef enum _DE_HPD_INTR_INSTANCE_ICL
{
    DE_HPD_INTR_ADDR_ICL = 0x44470,
} DE_HPD_INTR_INSTANCE_ICL;

typedef enum _DE_HPD_INTR_ICL
{
    DE_HPD_INTR_WO_ICL  = 0x0,
    DE_HPD_INTR_MBZ_ICL = 0x0,
    DE_HPD_INTR_PBC_ICL = 0x0,
} DE_HPD_INTR_ICL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine HPD Interrupt registers.
0x44470 = ISR
0x44474 = IMR
0x44478 = IIR
0x4447C = IER
\*****************************************************************************/
typedef union _DE_HPD_INTR_DEFINITION_ICL {
    struct
    {

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tbt1Hotplug : BITFIELD_BIT(0); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tbt2Hotplug : BITFIELD_BIT(1); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tbt3Hotplug : BITFIELD_BIT(2); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tbt4Hotplug : BITFIELD_BIT(3); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tbt5Hotplug : BITFIELD_BIT(4); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tbt6Hotplug : BITFIELD_BIT(5); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tbt7Hotplug : BITFIELD_BIT(6); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tbt8Hotplug : BITFIELD_BIT(7); //
        SIZE32BITS Unused8 : BITFIELD_BIT(8);     //
        SIZE32BITS Unused9 : BITFIELD_BIT(9);     //
        SIZE32BITS Unused10 : BITFIELD_BIT(10);   //
        SIZE32BITS Unused11 : BITFIELD_BIT(11);   //
        SIZE32BITS Unused12 : BITFIELD_BIT(12);   //
        SIZE32BITS Unused13 : BITFIELD_BIT(13);   //
        SIZE32BITS Unused14 : BITFIELD_BIT(14);   //
        SIZE32BITS Unused15 : BITFIELD_BIT(15);   //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tc1Hotplug : BITFIELD_BIT(16); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tc2Hotplug : BITFIELD_BIT(17); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tc3Hotplug : BITFIELD_BIT(18); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tc4Hotplug : BITFIELD_BIT(19); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tc5Hotplug : BITFIELD_BIT(20); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tc6Hotplug : BITFIELD_BIT(21); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tc7Hotplug : BITFIELD_BIT(22); //

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tc8Hotplug : BITFIELD_BIT(23); //
        SIZE32BITS Unused24 : BITFIELD_BIT(24);   //
        SIZE32BITS Unused25 : BITFIELD_BIT(25);   //
        SIZE32BITS Unused26 : BITFIELD_BIT(26);   //
        SIZE32BITS Unused27 : BITFIELD_BIT(27);   //
        SIZE32BITS Unused28 : BITFIELD_BIT(28);   //
        SIZE32BITS Unused29 : BITFIELD_BIT(29);   //
        SIZE32BITS Unused30 : BITFIELD_BIT(30);   //
        SIZE32BITS Unused31 : BITFIELD_BIT(31);   //
    };
    SIZE32BITS ulValue;

} DE_HPD_INTR_DEFINITION_ICL, *PDE_HPD_INTR_DEFINITION_ICL;

C_ASSERT(4 == sizeof(DE_HPD_INTR_DEFINITION_ICL));

// IMPLICIT ENUMERATIONS USED BY DE_MISC_INTR_DEFINITION_ICL
//
typedef enum _DE_MISC_INTR_INSTANCE_ICL
{
    DE_MISC_INTR_ADDR_ICL = 0x44460,
} DE_MISC_INTR_INSTANCE_ICL;

typedef enum _DE_MISC_INTR_ICL
{
    DE_MISC_INTR_WO_ICL  = 0x0,
    DE_MISC_INTR_PBC_ICL = 0x0,
    DE_MISC_INTR_MBZ_ICL = 0x3C737F0F,
} DE_MISC_INTR_ICL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine Miscellaneous Interrupt registers.
0x44460 = ISR
0x44464 = IMR
0x44468 = IIR
0x4446C = IER
\*****************************************************************************/
typedef union _DE_MISC_INTR_DEFINITION_ICL {
    struct
    {

        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(0, 3); // MBZ

        /*****************************************************************************\
        The ISR is an active high pulse on receiving a PM Request.
        \*****************************************************************************/
        SIZE32BITS PmRequestReceived : BITFIELD_BIT(4); //

        /*****************************************************************************\
        The ISR is an active high pulse on sending a PM Response.
        \*****************************************************************************/
        SIZE32BITS PmResponseSent : BITFIELD_BIT(5); //

        /*****************************************************************************\
        The ISR is an active high pulse on asserting DE Wake.
        \*****************************************************************************/
        SIZE32BITS DeWakeAsserted : BITFIELD_BIT(6); //

        /*****************************************************************************\
        The ISR is an active high pulse on asserting DE Poke.
        \*****************************************************************************/
        SIZE32BITS DePokeAsserted : BITFIELD_BIT(7); //

        /*****************************************************************************\
        The ISR is an active high pulse on receiving the pinning context switch interrupt.
        \*****************************************************************************/
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(8, 14); // MBZ

        /*****************************************************************************\
        The ISR is an active high level while any of the GTC_IIR bits are set.
        \*****************************************************************************/
        SIZE32BITS Gtc_Interrupts_Combined : BITFIELD_BIT(15);    //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(16, 17); // MBZ

        /*****************************************************************************\
        The ISR is an active high level while any of the WD1_IIR bits are set.
        \*****************************************************************************/
        SIZE32BITS Wd1_Interrupts_Combined : BITFIELD_BIT(18); //

        /*****************************************************************************\
        The ISR is an active high level while any of the SRD_IIR bits are set.
        \*****************************************************************************/
        SIZE32BITS Srd_Interrupts_Combined : BITFIELD_BIT(19);    //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(20, 22); // MBZ

        /*****************************************************************************\
        The ISR is an active high level while any of the WD0_IIR bits are set.
        \*****************************************************************************/
        SIZE32BITS Wd0_Interrupts_Combined : BITFIELD_BIT(23); //

        /*****************************************************************************\
        The ISR is an active high pulse on the DMC interrupt event.
        \*****************************************************************************/
        SIZE32BITS Dmc_Interrupt_Event : BITFIELD_BIT(24); //

        /*****************************************************************************\
        The ISR is an active high pulse on the DMC error event.
        \*****************************************************************************/
        SIZE32BITS Dmc_Error : BITFIELD_BIT(25);                  //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(26, 29); // MBZ

        /*****************************************************************************\
        The ISR is an active high level while any of the ECC Double Error status bits are set.
        \*****************************************************************************/
        SIZE32BITS Ecc_Double_Error : BITFIELD_BIT(30); //

        /*****************************************************************************\
        The ISR is an active high pulse on receiving the poison response to a memory transaction.
        \*****************************************************************************/
        SIZE32BITS Poison : BITFIELD_BIT(31); //
    };
    SIZE32BITS ulValue;

} DE_MISC_INTR_DEFINITION_ICL, *PDE_MISC_INTR_DEFINITION_ICL;

C_ASSERT(4 == sizeof(DE_MISC_INTR_DEFINITION_ICL));

// IMPLICIT ENUMERATIONS USED BY AUDIO_CODEC_INTR_DEFINITION_ICL
//
typedef enum _AUDIO_CODEC_INTR_INSTANCE_ICL
{
    AUDIO_CODEC_INTR_ADDR_ICL = 0x44480,
} AUDIO_CODEC_INTR_INSTANCE_ICL;

typedef enum _AUDIO_CODEC_INTR_ICL
{
    AUDIO_CODEC_INTR_WO_ICL  = 0x0,
    AUDIO_CODEC_INTR_MBZ_ICL = 0x0,
    AUDIO_CODEC_INTR_PBC_ICL = 0x0,
} AUDIO_CODEC_INTR_ICL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Audio Codec Interrupt registers.
0x44480 = ISR
0x44484 = IMR
0x44488 = IIR
0x4448C = IER
\*****************************************************************************/
typedef union _AUDIO_CODEC_INTR_DEFINITION_ICL {
    struct
    {

        /*****************************************************************************\
        The ISR is an active high pulse when there is a write to any of the four Audio Mail box verbs in vendor defined node ID 8
        \*****************************************************************************/
        SIZE32BITS Audio_Mailbox_Write : BITFIELD_BIT(0); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for transcoder A.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Change_Transcoder_A : BITFIELD_BIT(1); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder A. It is valid after the
        Audio_CP_Change_Transcoder_A event has occurred.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Request_Transcoder_A : BITFIELD_BIT(2); //

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        SIZE32BITS Unused_Int_4_3 : BITFIELD_RANGE(3, 4); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for transcoder B.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Change_Transcoder_B : BITFIELD_BIT(5); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder B. It is valid after the
        Audio_CP_Change_Transcoder_B event has occurred.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Request_Transcoder_B : BITFIELD_BIT(6); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for transcoder C.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Change_Transcoder_C : BITFIELD_BIT(7); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder C. It is valid after the
        Audio_CP_Change_Transcoder_C event has occurred.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Request_Transcoder_C : BITFIELD_BIT(8); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for transcoder C.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Change_Transcoder_D : BITFIELD_BIT(9); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder C. It is valid after the
        Audio_CP_Change_Transcoder_C event has occurred.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Request_Transcoder_D : BITFIELD_BIT(10); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for DDI F.
        \*****************************************************************************/
        SIZE32BITS Audio_Power_State_Change_Ddi_F : BITFIELD_BIT(11); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for DDI E.
        \*****************************************************************************/
        SIZE32BITS Audio_Power_State_Change_Ddi_E : BITFIELD_BIT(12); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for WD 0.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Change_Wd_0 : BITFIELD_BIT(13); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for WD 0. It is valid after the Audio_CP_Change_WD_0 event has
        occurred.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Request_Wd_0 : BITFIELD_BIT(14); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for WD 1.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Change_Wd_1 : BITFIELD_BIT(15); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for WD 0. It is valid after the Audio_CP_Change_WD_1 event has
        occurred.
        \*****************************************************************************/
        SIZE32BITS Audio_Cp_Request_Wd_1 : BITFIELD_BIT(16); //

        /*****************************************************************************\
        The ISR is an active high level indicating an overflow in the Audio Wireless slice 0 RAM.
        \*****************************************************************************/
        SIZE32BITS Audio_Ramfull_Error_Wd_0 : BITFIELD_BIT(17); //

        /*****************************************************************************\
        The ISR is an active high level indicating an overflow in the Audio Wireless slice 1 RAM.
        \*****************************************************************************/
        SIZE32BITS Audio_Ramfull_Error_Wd_1 : BITFIELD_BIT(18); //
        SIZE32BITS Spare19 : BITFIELD_BIT(19);                  //
        SIZE32BITS Spare20 : BITFIELD_BIT(20);                  //
        SIZE32BITS Spare21 : BITFIELD_BIT(21);                  //
        SIZE32BITS Spare22 : BITFIELD_BIT(22);                  //
        SIZE32BITS Spare23 : BITFIELD_BIT(23);                  //
        SIZE32BITS Spare24 : BITFIELD_BIT(24);                  //
        SIZE32BITS Spare25 : BITFIELD_BIT(25);                  //
        SIZE32BITS Spare26 : BITFIELD_BIT(26);                  //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for WD 1.
        \*****************************************************************************/
        SIZE32BITS Audio_Power_State_Change_Wd_1 : BITFIELD_BIT(27); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for WD 0.
        \*****************************************************************************/
        SIZE32BITS Audio_Power_State_Change_Wd_0 : BITFIELD_BIT(28); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for DDI B.
        \*****************************************************************************/
        SIZE32BITS Audio_Power_State_Change_Ddi_B : BITFIELD_BIT(29); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for DDI C.
        \*****************************************************************************/
        SIZE32BITS Audio_Power_State_Change_Ddi_C : BITFIELD_BIT(30); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for DDI D.
        \*****************************************************************************/
        SIZE32BITS Audio_Power_State_Change_Ddi_D : BITFIELD_BIT(31); //
    };
    SIZE32BITS ulValue;

} AUDIO_CODEC_INTR_DEFINITION_ICL, *PAUDIO_CODEC_INTR_DEFINITION_ICL;

C_ASSERT(4 == sizeof(AUDIO_CODEC_INTR_DEFINITION_ICL));

// IMPLICIT ENUMERATIONS USED BY DE_PIPE_INTR_ICL
//
typedef enum _DE_PIPE_A_INTR_INSTANCE_ICL
{
    DE_PIPE_A_INTR_ADDR_ICL = 0x44400,
} DE_PIPE_A_INTR_INSTANCE_ICL;

typedef enum _DE_PIPE_B_INTR_INSTANCE_ICL
{
    DE_PIPE_B_INTR_ADDR_ICL = 0x44410,
} DE_PIPE_B_INTR_INSTANCE_ICL;

typedef enum _DE_PIPE_C_INTR_INSTANCE_ICL
{
    DE_PIPE_C_INTR_ADDR_ICL = 0x44420,
} DE_PIPE_C_INTR_INSTANCE_ICL;

typedef enum _DE_PIPE_D_INTR_INSTANCE_ICL
{
    DE_PIPE_D_INTR_ADDR_ICL = 0x44430,
} DE_PIPE_D_INTR_INSTANCE_ICL;

typedef enum _DE_PIPE_INTR_MASKS_ICL
{
    DE_PIPE_INTR_MASKS_WO_ICL  = 0x0,
    DE_PIPE_INTR_MASKS_PBC_ICL = 0x0,
    DE_PIPE_INTR_MASKS_MBZ_ICL = 0xF0000,
} DE_PIPE_INTR_MASKS_ICL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine Pipe Interrupt registers.

The IER enabled Display Engine Pipe Interrupt IIR (sticky) bits are ORed together to generate the DE_Pipe Interrupts Pending bit in the Master Interrupt Control register.

There is one full set of Display Engine Pipe interrupts per display pipes A/B/C.

The STEREO3D_EVENT_MASK selects between left eye and right eye reporting of vertical blank, vertical sync, and scanline events in stereo 3D modes.0x44400 = ISR A, 0x44410 = ISR B,
0x44420 = ISR C, 0x44430 = ISR D 0x44404 = IMR A, 0x44414 = IMR B, 0x44424 = IMR C, 0x44434 = IMR D 0x44408 = IIR A, 0x44418 = IIR B, 0x44428 = IIR C, 0x44438 = IIR D 0x4440C = IER
A, 0x4441C = IER B, 0x4442C = IER C, 0x4443C = IER D
\*****************************************************************************/
typedef union _DE_PIPE_INTR_ICL {
    struct
    {

        /*****************************************************************************\
        The ISR is an active high level for the duration of the vertical blank of the transcoder attached to this pipe.
        \*****************************************************************************/
        SIZE32BITS Vblank : BITFIELD_BIT(0); //

        /*****************************************************************************\
        The ISR is an active high level for the duration of the vertical sync of the transcoder attached to this pipe.

        Programming Notes:
        Restriction : Not supported with MIPI DSI.
        \*****************************************************************************/
        SIZE32BITS Vsync : BITFIELD_BIT(1); //

        /*****************************************************************************\
        The ISR is an active high pulse on the scan line event of the transcoder attached to this pipe.

        Programming Notes:
        Restriction : Not supported with MIPI DSI.
        \*****************************************************************************/
        SIZE32BITS Scan_Line_Event : BITFIELD_BIT(2); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 1 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane1_Flip_Done : BITFIELD_BIT(3); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 2 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane2_Flip_Done : BITFIELD_BIT(4); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 3 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane3_Flip_Done : BITFIELD_BIT(5); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 4 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane4_Flip_Done : BITFIELD_BIT(6); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 1 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane1_Gtt_Fault_Status : BITFIELD_BIT(7); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 2 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane2_Gtt_Fault_Status : BITFIELD_BIT(8); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 3 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane3_Gtt_Fault_Status : BITFIELD_BIT(9); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 4 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane4_Gtt_Fault_Status : BITFIELD_BIT(10); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for the cursor on this pipe.
        \*****************************************************************************/
        SIZE32BITS Cursor_Gtt_Fault_Status : BITFIELD_BIT(11); //

        /*****************************************************************************\
        The ISR is an active high pulse on the DPST Histogram event on this pipe.
        \*****************************************************************************/
        SIZE32BITS Dpst_Histogram_Event : BITFIELD_BIT(12); //

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        SIZE32BITS Unused_Int_15_13 : BITFIELD_RANGE(13, 15); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 5 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane5_Flip_Done : BITFIELD_BIT(16); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 6 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane6_Flip_Done : BITFIELD_BIT(17); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 7 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane7_Flip_Done : BITFIELD_BIT(18);     //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(19); // MBZ

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 5 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane5_Gtt_Fault_Status : BITFIELD_BIT(20); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 6 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane6_Gtt_Fault_Status : BITFIELD_BIT(21); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 7 on this pipe.
        \*****************************************************************************/
        SIZE32BITS Plane7_Gtt_Fault_Status : BITFIELD_BIT(22); //

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        SIZE32BITS Unused_Int_27_23 : BITFIELD_RANGE(23, 27); //

        /*****************************************************************************\
        The ISR is an active high pulse when the CRC completes a frame.
        \*****************************************************************************/
        SIZE32BITS Cdclk_Crc_Done : BITFIELD_BIT(28); //

        /*****************************************************************************\
        The ISR is an active high pulse when a completed CRC mismatches with the expected value.
        \*****************************************************************************/
        SIZE32BITS Cdclk_Crc_Error : BITFIELD_BIT(29); //

        /*****************************************************************************\
        The ISR is an active high pulse on the eDP/DP Variable Refresh Rate double buffer update event on this pipe. VRR Double Buffer update is triggered by either a master flip
        or a VRR vblank max time out.
        \*****************************************************************************/
        SIZE32BITS VrrDoubleBufferUpdate : BITFIELD_BIT(30); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is an underrun on the transcoder attached to this pipe.
        \*****************************************************************************/
        SIZE32BITS Underrun : BITFIELD_BIT(31); //
    };
    SIZE32BITS ulValue;

} DE_PIPE_INTR_ICL, *PDE_PIPE_INTR_ICL;

C_ASSERT(4 == sizeof(DE_PIPE_INTR_ICL));

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_DDI_ICL
//
typedef enum _DDIA_HPD_STATUS_ICL
{
    DDIA_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    DDIA_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    DDIA_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    DDIA_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} DDIA_HPD_STATUS_ICL;

typedef enum _DDIA_HPD_OUTPUT_DATA_ICL
{
    DDIA_HPD_OUTPUT_DATA_DRIVE_0_ICL = 0x0,
    DDIA_HPD_OUTPUT_DATA_DRIVE_1_ICL = 0x1,
} DDIA_HPD_OUTPUT_DATA_ICL;

typedef enum _DDIA_HPD_ENABLE_ICL
{
    DDIA_HPD_ENABLE_DISABLE_ICL = 0x0,
    DDIA_HPD_ENABLE_ENABLE_ICL  = 0x1,
} DDIA_HPD_ENABLE_ICL;

typedef enum _DDIB_HPD_STATUS_ICL
{
    DDIB_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    DDIB_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    DDIB_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    DDIB_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} DDIB_HPD_STATUS_ICL;

typedef enum _DDIB_HPD_OUTPUT_DATA_ICL
{
    DDIB_HPD_OUTPUT_DATA_DRIVE_0_ICL = 0x0,
    DDIB_HPD_OUTPUT_DATA_DRIVE_1_ICL = 0x1,
} DDIB_HPD_OUTPUT_DATA_ICL;

typedef enum _DDIB_HPD_ENABLE_ICL
{
    DDIB_HPD_ENABLE_DISABLE_ICL = 0x0,
    DDIB_HPD_ENABLE_ENABLE_ICL  = 0x1,
} DDIB_HPD_ENABLE_ICL;

typedef enum _DDIC_HPD_STATUS_ICL
{
    DDIC_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    DDIC_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    DDIC_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    DDIC_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} DDIC_HPD_STATUS_ICL;

typedef enum _DDIC_HPD_OUTPUT_DATA_ICL
{
    DDIC_HPD_OUTPUT_DATA_DRIVE_0_ICL = 0x0,
    DDIC_HPD_OUTPUT_DATA_DRIVE_1_ICL = 0x1,
} DDIC_HPD_OUTPUT_DATA_ICL;

typedef enum _DDIC_HPD_ENABLE_ICL
{
    DDIC_HPD_ENABLE_DISABLE_ICL = 0x0,
    DDIC_HPD_ENABLE_ENABLE_ICL  = 0x1,
} DDIC_HPD_ENABLE_ICL;

typedef enum _SOUTH_HOT_PLUG_CTL_FOR_DDI_INSTANCE_ICL
{
    SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL = 0xC4030,
} SOUTH_HOT_PLUG_CTL_FOR_DDI_INSTANCE_ICL;

typedef enum _SHOTPLUG_CTL_DDI_MASKS_ICL
{
    SHOTPLUG_CTL_DDI_MASKS_MBZ_ICL = 0xFFFFF000,
    SHOTPLUG_CTL_DDI_MASKS_WO_ICL  = 0x0,
    SHOTPLUG_CTL_DDI_MASKS_PBC_ICL = 0x0,
} SHOTPLUG_CTL_DDI_MASKS_ICL;

/*****************************************************************************\
The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port, one of the status bits will set and
the hotplug IIR will be set (if unmasked in the IMR).  The status bits are sticky bits, cleared by writing 1s to the bits.Each HPD pin can be configured as an input or output.  The
HPD status function will only work when the pin is configured as an input.  The HPD Output Data function will only work when the HPD pin is configured as an output.The short pulse
duration is programmed in SHPD_PULSE_CNT.
\*****************************************************************************/
typedef union _SHOTPLUG_CTL_DDI_ICL {
    struct
    {
        SIZE32BITS DdiaHpdStatus : BITFIELD_RANGE(0, 1);          // DDIA_HPD_STATUS_ICL
        SIZE32BITS DdiaHpdOutputData : BITFIELD_BIT(2);           // DDIA_HPD_OUTPUT_DATA_ICL
        SIZE32BITS DdiaHpdEnable : BITFIELD_BIT(3);               // DDIA_HPD_ENABLE_ICL
        SIZE32BITS DdibHpdStatus : BITFIELD_RANGE(4, 5);          // DDIB_HPD_STATUS_ICL
        SIZE32BITS DdibHpdOutputData : BITFIELD_BIT(6);           // DDIB_HPD_OUTPUT_DATA_ICL
        SIZE32BITS DdibHpdEnable : BITFIELD_BIT(7);               // DDIB_HPD_ENABLE_ICL
        SIZE32BITS DdicHpdStatus : BITFIELD_RANGE(8, 9);          // DDIC_HPD_STATUS_ICL
        SIZE32BITS DdicHpdOutputData : BITFIELD_BIT(10);          // DDIC_HPD_OUTPUT_DATA_ICL
        SIZE32BITS DdicHpdEnable : BITFIELD_BIT(11);              // DDIC_HPD_ENABLE_ICL
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(12, 31); // MBZ
    };
    SIZE32BITS ulValue;

} SHOTPLUG_CTL_DDI_ICL, *PSHOTPLUG_CTL_DDI_ICL;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_DDI_ICL));

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_TC_ICL
//
typedef enum _TC1_HPD_STATUS_ICL
{
    TC1_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    TC1_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    TC1_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    TC1_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} TC1_HPD_STATUS_ICL;

typedef enum _TC1_HPD_OUTPUT_DATA_ICL
{
    TC1_HPD_OUTPUT_DATA_DRIVE_0_ICL = 0x0,
    TC1_HPD_OUTPUT_DATA_DRIVE_1_ICL = 0x1,
} TC1_HPD_OUTPUT_DATA_ICL;

typedef enum _TC1_HPD_ENABLE_ICL
{
    TC1_HPD_ENABLE_DISABLE_ICL = 0x0,
    TC1_HPD_ENABLE_ENABLE_ICL  = 0x1,
} TC1_HPD_ENABLE_ICL;

typedef enum _TC2_HPD_STATUS_ICL
{
    TC2_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    TC2_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    TC2_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    TC2_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} TC2_HPD_STATUS_ICL;

typedef enum _TC2_HPD_OUTPUT_DATA_ICL
{
    TC2_HPD_OUTPUT_DATA_DRIVE_0_ICL = 0x0,
    TC2_HPD_OUTPUT_DATA_DRIVE_1_ICL = 0x1,
} TC2_HPD_OUTPUT_DATA_ICL;

typedef enum _TC2_HPD_ENABLE_ICL
{
    TC2_HPD_ENABLE_DISABLE_ICL = 0x0,
    TC2_HPD_ENABLE_ENABLE_ICL  = 0x1,
} TC2_HPD_ENABLE_ICL;

typedef enum _TC3_HPD_STATUS_ICL
{
    TC3_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    TC3_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    TC3_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    TC3_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} TC3_HPD_STATUS_ICL;

typedef enum _TC3_HPD_OUTPUT_DATA_ICL
{
    TC3_HPD_OUTPUT_DATA_DRIVE_0_ICL = 0x0,
    TC3_HPD_OUTPUT_DATA_DRIVE_1_ICL = 0x1,
} TC3_HPD_OUTPUT_DATA_ICL;

typedef enum _TC3_HPD_ENABLE_ICL
{
    TC3_HPD_ENABLE_DISABLE_ICL = 0x0,
    TC3_HPD_ENABLE_ENABLE_ICL  = 0x1,
} TC3_HPD_ENABLE_ICL;

typedef enum _TC4_HPD_STATUS_ICL
{
    TC4_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    TC4_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    TC4_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    TC4_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} TC4_HPD_STATUS_ICL;

typedef enum _TC4_HPD_OUTPUT_DATA_ICL
{
    TC4_HPD_OUTPUT_DATA_DRIVE_0_ICL = 0x0,
    TC4_HPD_OUTPUT_DATA_DRIVE_1_ICL = 0x1,
} TC4_HPD_OUTPUT_DATA_ICL;

typedef enum _TC4_HPD_ENABLE_ICL
{
    TC4_HPD_ENABLE_DISABLE_ICL = 0x0,
    TC4_HPD_ENABLE_ENABLE_ICL  = 0x1,
} TC4_HPD_ENABLE_ICL;

typedef enum _TC5_HPD_STATUS_ICL
{
    TC5_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    TC5_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    TC5_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    TC5_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} TC5_HPD_STATUS_ICL;

typedef enum _TC5_HPD_OUTPUT_DATA_ICL
{
    TC5_HPD_OUTPUT_DATA_DRIVE_0_ICL = 0x0,
    TC5_HPD_OUTPUT_DATA_DRIVE_1_ICL = 0x1,
} TC5_HPD_OUTPUT_DATA_ICL;

typedef enum _TC5_HPD_ENABLE_ICL
{
    TC5_HPD_ENABLE_DISABLE_ICL = 0x0,
    TC5_HPD_ENABLE_ENABLE_ICL  = 0x1,
} TC5_HPD_ENABLE_ICL;

typedef enum _TC6_HPD_STATUS_ICL
{
    TC6_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    TC6_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    TC6_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    TC6_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} TC6_HPD_STATUS_ICL;

typedef enum _TC6_HPD_OUTPUT_DATA_ICL
{
    TC6_HPD_OUTPUT_DATA_DRIVE_0_ICL = 0x0,
    TC6_HPD_OUTPUT_DATA_DRIVE_1_ICL = 0x1,
} TC6_HPD_OUTPUT_DATA_ICL;

typedef enum _TC6_HPD_ENABLE_ICL
{
    TC6_HPD_ENABLE_DISABLE_ICL = 0x0,
    TC6_HPD_ENABLE_ENABLE_ICL  = 0x1,
} TC6_HPD_ENABLE_ICL;

typedef enum _SOUTH_HOT_PLUG_CTL_FOR_TYPEC_INSTANCE_ICL
{
    SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL = 0xC4034,
} SOUTH_HOT_PLUG_CTL_FOR_TYPEC_INSTANCE_ICL;

typedef enum _SHOTPLUG_CTL_TC_MASKS_ICL
{
    SHOTPLUG_CTL_TC_MASKS_MBZ_ICL = 0xFF000000,
    SHOTPLUG_CTL_TC_MASKS_WO_ICL  = 0x0,
    SHOTPLUG_CTL_TC_MASKS_PBC_ICL = 0x0,
} SHOTPLUG_CTL_TC_MASKS_ICL;

/*****************************************************************************\
The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port, one of the status bits will set and
the hotplug IIR will be set (if unmasked in the IMR).  The status bits are sticky bits, cleared by writing 1s to the bits.Each HPD pin can be configured as an input or output.  The
HPD status function will only work when the pin is configured as an input.  The HPD Output Data function will only work when the HPD pin is configured as an output.The short pulse
duration is programmed in SHPD_PULSE_CNT.
\*****************************************************************************/
typedef union _SHOTPLUG_CTL_TC_ICL {
    struct
    {
        SIZE32BITS Tc1HpdStatus : BITFIELD_RANGE(0, 1);           // TC1_HPD_STATUS_ICL
        SIZE32BITS Tc1HpdOutputData : BITFIELD_BIT(2);            // TC1_HPD_OUTPUT_DATA_ICL
        SIZE32BITS Tc1HpdEnable : BITFIELD_BIT(3);                // TC1_HPD_ENABLE_ICL
        SIZE32BITS Tc2HpdStatus : BITFIELD_RANGE(4, 5);           // TC2_HPD_STATUS_ICL
        SIZE32BITS Tc2HpdOutputData : BITFIELD_BIT(6);            // TC2_HPD_OUTPUT_DATA_ICL
        SIZE32BITS Tc2HpdEnable : BITFIELD_BIT(7);                // TC2_HPD_ENABLE_ICL
        SIZE32BITS Tc3HpdStatus : BITFIELD_RANGE(8, 9);           // TC3_HPD_STATUS_ICL
        SIZE32BITS Tc3HpdOutputData : BITFIELD_BIT(10);           // TC3_HPD_OUTPUT_DATA_ICL
        SIZE32BITS Tc3HpdEnable : BITFIELD_BIT(11);               // TC3_HPD_ENABLE_ICL
        SIZE32BITS Tc4HpdStatus : BITFIELD_RANGE(12, 13);         // TC4_HPD_STATUS_ICL
        SIZE32BITS Tc4HpdOutputData : BITFIELD_BIT(14);           // TC4_HPD_OUTPUT_DATA_ICL
        SIZE32BITS Tc4HpdEnable : BITFIELD_BIT(15);               // TC4_HPD_ENABLE_ICL
        SIZE32BITS Tc5HpdStatus : BITFIELD_RANGE(16, 17);         // TC5_HPD_STATUS_ICL
        SIZE32BITS Tc5HpdOutputData : BITFIELD_BIT(18);           // TC5_HPD_OUTPUT_DATA_ICL
        SIZE32BITS Tc5HpdEnable : BITFIELD_BIT(19);               // TC5_HPD_ENABLE_ICL
        SIZE32BITS Tc6HpdStatus : BITFIELD_RANGE(20, 21);         // TC6_HPD_STATUS_ICL
        SIZE32BITS Tc6HpdOutputData : BITFIELD_BIT(22);           // TC6_HPD_OUTPUT_DATA_ICL
        SIZE32BITS Tc6HpdEnable : BITFIELD_BIT(23);               // TC6_HPD_ENABLE_ICL
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(24, 31); // MBZ
    };
    SIZE32BITS ulValue;

} SHOTPLUG_CTL_TC_ICL, *PSHOTPLUG_CTL_TC_ICL;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_TC_ICL));

// The below defines were generated after modifying BXML file. The AublistXML is not able to handle the following changes in bxml that resulted in inablity to generate this without
// modifications 1) "+" as part of project list is not working, so change "SPT+" to "SPT" (upgrading the aublistXML to r92173 resolves this) 2) remove the entire section under
// <DWord Name="0" Project="REMOVEDBY(GEN11:HAS:399096)"> 3) rename the section <DWord Name="0" Project="GEN11:HAS:399096"> to <DWord Name="0>

// IMPLICIT ENUMERATIONS USED BY SOUTH_DE_INTR_BIT_DEFINITION_SPT
//

typedef enum _SOUTH_DE_INTR_INSTANCE_SPT_ICL
{
    SOUTH_DE_INTR_ADDR_SPT_ICL = 0xC4000,
} SOUTH_DE_INTR_INSTANCE_SPT_ICL;

typedef enum _SOUTH_DE_INTR_BIT_SPT
{
    SOUTH_DE_INTR_BIT_MBZ_SPT = 0xC078C0F8,
    SOUTH_DE_INTR_BIT_WO_SPT  = 0x0,
    SOUTH_DE_INTR_BIT_PBC_SPT = 0x0,
} SOUTH_DE_INTR_BIT_SPT;

/*****************************************************************************\
South Display Engine (SDE) interrupt bits come from events within the south display engine.The SDE_IIR bits are ORed together to generate the South/PCH Display Interrupt Event
which will appear in the North Display Engine Interrupt Control Registers.	The South Display Engine Interrupt Control Registers all share the same bit definitions from this table.
\*****************************************************************************/
typedef union _SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL {
    struct
    {

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcDdia : BITFIELD_BIT(0); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcDdib : BITFIELD_BIT(1); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcDdic : BITFIELD_BIT(2);                  //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(3, 7); // MBZ

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcTc1 : BITFIELD_BIT(8); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcTc2 : BITFIELD_BIT(9); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcTc3 : BITFIELD_BIT(10); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcTc4 : BITFIELD_BIT(11); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcTc5 : BITFIELD_BIT(12); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcTc6 : BITFIELD_BIT(13);                    //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(14, 15); // MBZ

        /*****************************************************************************\
        The ISR indicates the live value of the hotplug line when hotplug detect  is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port
        Hot Plug Control Register.
        \*****************************************************************************/
        SIZE32BITS HotplugDdia : BITFIELD_BIT(16); //

        /*****************************************************************************\
        The ISR indicates the live value of the hotplug line when hotplug detect  is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port
        Hot Plug Control Register.
        \*****************************************************************************/
        SIZE32BITS HotplugDdib : BITFIELD_BIT(17); //

        /*****************************************************************************\
        The ISR indicates the live value of the hotplug line when hotplug detect  is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port
        Hot Plug Control Register.
        \*****************************************************************************/
        SIZE32BITS HotplugDdic : BITFIELD_BIT(18);                //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(19, 22); // MBZ

        /*****************************************************************************\
        This is an active high pulse when any of the events unmasked events in GMBUS4 Interrupt Mask register occur.
        \*****************************************************************************/
        SIZE32BITS Gmbus : BITFIELD_BIT(23); //

        /*****************************************************************************\
        The ISR indicates the live value of the hotplug line when hotplug detect  is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port
        Hot Plug Control Register.
        \*****************************************************************************/
        SIZE32BITS HotplugTypecPort1 : BITFIELD_BIT(24); //

        /*****************************************************************************\
        The ISR indicates the live value of the hotplug line when hotplug detect  is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port
        Hot Plug Control Register.
        \*****************************************************************************/
        SIZE32BITS HotplugTypecPort2 : BITFIELD_BIT(25); //

        /*****************************************************************************\
        The ISR indicates the live value of the hotplug line when hotplug detect  is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port
        Hot Plug Control Register.
        \*****************************************************************************/
        SIZE32BITS HotplugTypecPort3 : BITFIELD_BIT(26); //

        /*****************************************************************************\
        The ISR indicates the live value of the hotplug line when hotplug detect  is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port
        Hot Plug Control Register.
        \*****************************************************************************/
        SIZE32BITS HotplugTypecPort4 : BITFIELD_BIT(27); //

        /*****************************************************************************\
        The ISR indicates the live value of the hotplug line when hotplug detect  is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port
        Hot Plug Control Register.
        \*****************************************************************************/
        SIZE32BITS HotplugTypecPort5 : BITFIELD_BIT(28); //

        /*****************************************************************************\
        The ISR indicates the live value of the hotplug line when hotplug detect  is enabled. The IIR is set on either a short or long pulse detection status in the Digital Port
        Hot Plug Control Register.
        \*****************************************************************************/
        SIZE32BITS HotplugTypecPort6 : BITFIELD_BIT(29);          //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(30, 31); // MBZ
    };
    SIZE32BITS ulValue;

} SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL, *PSOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL;

C_ASSERT(4 == sizeof(SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL));

// IMPLICIT ENUMERATIONS USED BY HOTPLUG_CTL_ICL
//
typedef enum _PORT1_HPD_STATUS_ICL
{
    PORT1_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    PORT1_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    PORT1_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    PORT1_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} PORT1_HPD_STATUS_ICL;

typedef enum _PORT1_HPD_ENABLE_ICL
{
    PORT1_HPD_ENABLE_DISABLE_ICL = 0x0,
    PORT1_HPD_ENABLE_ENABLE_ICL  = 0x1,
} PORT1_HPD_ENABLE_ICL;

typedef enum _PORT2_HPD_STATUS_ICL
{
    PORT2_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    PORT2_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    PORT2_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    PORT2_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} PORT2_HPD_STATUS_ICL;

typedef enum _PORT2_HPD_ENABLE_ICL
{
    PORT2_HPD_ENABLE_DISABLE_ICL = 0x0,
    PORT2_HPD_ENABLE_ENABLE_ICL  = 0x1,
} PORT2_HPD_ENABLE_ICL;

typedef enum _PORT3_HPD_STATUS_ICL
{
    PORT3_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    PORT3_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    PORT3_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    PORT3_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} PORT3_HPD_STATUS_ICL;

typedef enum _PORT3_HPD_ENABLE_ICL
{
    PORT3_HPD_ENABLE_DISABLE_ICL = 0x0,
    PORT3_HPD_ENABLE_ENABLE_ICL  = 0x1,
} PORT3_HPD_ENABLE_ICL;

typedef enum _PORT4_HPD_STATUS_ICL
{
    PORT4_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    PORT4_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    PORT4_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    PORT4_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} PORT4_HPD_STATUS_ICL;

typedef enum _PORT4_HPD_ENABLE_ICL
{
    PORT4_HPD_ENABLE_DISABLE_ICL = 0x0,
    PORT4_HPD_ENABLE_ENABLE_ICL  = 0x1,
} PORT4_HPD_ENABLE_ICL;

typedef enum _PORT5_HPD_STATUS_ICL
{
    PORT5_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    PORT5_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    PORT5_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    PORT5_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} PORT5_HPD_STATUS_ICL;

typedef enum _PORT5_HPD_ENABLE_ICL
{
    PORT5_HPD_ENABLE_DISABLE_ICL = 0x0,
    PORT5_HPD_ENABLE_ENABLE_ICL  = 0x1,
} PORT5_HPD_ENABLE_ICL;

typedef enum _PORT6_HPD_STATUS_ICL
{
    PORT6_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    PORT6_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    PORT6_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    PORT6_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} PORT6_HPD_STATUS_ICL;

typedef enum _PORT6_HPD_ENABLE_ICL
{
    PORT6_HPD_ENABLE_DISABLE_ICL = 0x0,
    PORT6_HPD_ENABLE_ENABLE_ICL  = 0x1,
} PORT6_HPD_ENABLE_ICL;

typedef enum _PORT7_HPD_STATUS_ICL
{
    PORT7_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    PORT7_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    PORT7_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    PORT7_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} PORT7_HPD_STATUS_ICL;

typedef enum _PORT7_HPD_ENABLE_ICL
{
    PORT7_HPD_ENABLE_DISABLE_ICL = 0x0,
    PORT7_HPD_ENABLE_ENABLE_ICL  = 0x1,
} PORT7_HPD_ENABLE_ICL;

typedef enum _PORT8_HPD_STATUS_ICL
{
    PORT8_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_ICL    = 0x0,
    PORT8_HPD_STATUS_SHORT_PULSE_DETECTED_ICL           = 0x1,
    PORT8_HPD_STATUS_LONG_PULSE_DETECTED_ICL            = 0x2,
    PORT8_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_ICL = 0x3,
} PORT8_HPD_STATUS_ICL;

typedef enum _PORT8_HPD_ENABLE_ICL
{
    PORT8_HPD_ENABLE_DISABLE_ICL = 0x0,
    PORT8_HPD_ENABLE_ENABLE_ICL  = 0x1,
} PORT8_HPD_ENABLE_ICL;

typedef enum _THUNDERBOLT_HOT_PLUG_CTL_INSTANCE_ICL
{
    THUNDERBOLT_HOT_PLUG_CTL_ADDR_ICL = 0x44030,
} THUNDERBOLT_HOT_PLUG_CTL_INSTANCE_ICL;

typedef enum _TYPE_C_HOT_PLUG_CTL_INSTANCE_ICL
{
    TYPE_C_HOT_PLUG_CTL_ADDR_ICL = 0x44038,
} TYPE_C_HOT_PLUG_CTL_INSTANCE_ICL;

typedef enum _HOTPLUG_CTL_MASKS_ICL
{
    HOTPLUG_CTL_MASKS_WO_ICL  = 0x0,
    HOTPLUG_CTL_MASKS_MBZ_ICL = 0x0,
    HOTPLUG_CTL_MASKS_PBC_ICL = 0x0,
} HOTPLUG_CTL_MASKS_ICL;

typedef union _HOTPLUG_CTL_ICL {
    struct
    {
        SIZE32BITS Port1HpdStatus : BITFIELD_RANGE(0, 1);   // PORT1_HPD_STATUS_ICL
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(2);  //
        SIZE32BITS Port1HpdEnable : BITFIELD_BIT(3);        // PORT1_HPD_ENABLE_ICL
        SIZE32BITS Port2HpdStatus : BITFIELD_RANGE(4, 5);   // PORT2_HPD_STATUS_ICL
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(6);  //
        SIZE32BITS Port2HpdEnable : BITFIELD_BIT(7);        // PORT2_HPD_ENABLE_ICL
        SIZE32BITS Port3HpdStatus : BITFIELD_RANGE(8, 9);   // PORT3_HPD_STATUS_ICL
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(10); //
        SIZE32BITS Port3HpdEnable : BITFIELD_BIT(11);       // PORT3_HPD_ENABLE_ICL
        SIZE32BITS Port4HpdStatus : BITFIELD_RANGE(12, 13); // PORT4_HPD_STATUS_ICL
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(14); //
        SIZE32BITS Port4HpdEnable : BITFIELD_BIT(15);       // PORT4_HPD_ENABLE_ICL
        SIZE32BITS Port5HpdStatus : BITFIELD_RANGE(16, 17); // PORT5_HPD_STATUS_ICL
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(18); //
        SIZE32BITS Port5HpdEnable : BITFIELD_BIT(19);       // PORT5_HPD_ENABLE_ICL
        SIZE32BITS Port6HpdStatus : BITFIELD_RANGE(20, 21); // PORT6_HPD_STATUS_ICL
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(22); //
        SIZE32BITS Port6HpdEnable : BITFIELD_BIT(23);       // PORT6_HPD_ENABLE_ICL
        SIZE32BITS Port7HpdStatus : BITFIELD_RANGE(24, 25); // PORT7_HPD_STATUS_ICL
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(26); //
        SIZE32BITS Port7HpdEnable : BITFIELD_BIT(27);       // PORT7_HPD_ENABLE_ICL
        SIZE32BITS Port8HpdStatus : BITFIELD_RANGE(28, 29); // PORT8_HPD_STATUS_ICL
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(30); //
        SIZE32BITS Port8HpdEnable : BITFIELD_BIT(31);       // PORT8_HPD_ENABLE_ICL
    };
    SIZE32BITS ulValue;

} HOTPLUG_CTL_ICL, *PHOTPLUG_CTL_ICL;

C_ASSERT(4 == sizeof(HOTPLUG_CTL_ICL));

typedef enum _PORT_TX_DFLEXDPPMS_INSTANCE_ICL
{
    PORT_TX_DFLEXDPPMS_ADDR_ICL = 0X163890,
} PORT_TX_DFLEXDPPMS_INSTANCE_ICL;

/*****************************************************************************
Description:  PD FW writes  1  to this register's bit to tell DP Driver that it had put the FIA and PHY into DP PHY Mode and it s safe now for DP Driver to proceed to bring up the
DP Controller. Once DP Driver poll a value  1  in this register, DP Driver write  0  to clear this bit for PD FW to use it in the next round.

******************************************************************************/
typedef union _PORT_TX_DFLEXDPPMS_ICL {
    struct
    {
        /******************************************************************************************************************
        PD FW writes  1  to this bit to tell DP Driver that it had put the FIA and PHY into DP PHY Mode
        and it s safe now for DP Driver to proceed to bring up the DP Controller. Once DP Driver poll a value  1
        in this register, DP Driver write  0  to clear this bit for PD FW to use it in the next round.

        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector0 : DD_BITFIELD_BIT(0); // DISPLAY_DRIVER_MG_LANE_STATUS

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

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(16, 31); // RESERVED
    };

    DDU32 ulValue;
} PORT_TX_DFLEXDPPMS_ICL;

typedef enum _PORT_TX_LANES_ASSIGNED_ICL
{
    PHY_TX0_ALONE       = 0x1,
    PHY_TX1_ALONE       = 0x2,
    PHY_TX1_TX0         = 0x3,
    PHY_TX2_ALONE       = 0x4,
    PHY_TX3_ALONE       = 0x8,
    PHY_TX3_TX2         = 0xC,
    PHY_TX3_TX2_TX1_TX0 = 0xF,
} PORT_TX_LANES_ASSIGNED_ICL;

typedef enum _PORT_TX_DFLEXDPSP_INSTANCE_ICL
{
    PORT_TX_DFLEXDPSP1_ADDR_ICL = 0X1638A0,
    PORT_TX_DFLEXDPSP2_ADDR_ICL = 0X1638A4,
    PORT_TX_DFLEXDPSP3_ADDR_ICL = 0X1638A8,
    PORT_TX_DFLEXDPSP4_ADDR_ICL = 0X1638AC,
} PORT_TX_DFLEXDPSP_INSTANCE_ICL;

/*****************************************************************************
Description:  Dynamic FlexIO DP Scratch Pad (Type-C)

******************************************************************************/
typedef union _PORT_TX_DFLEXDPSP_ICL {
    struct
    {
        /******************************************************************************************************************
        Display Port x4 TX Lane Assignment for Type-C Connector 0(DPX4TXLATC0):
        4 bits correspond to 4 TX, i.e. TX[3:0] Lane in PHY.
        Lower 2 bits correspond to the 2 lower TX lane on the PHY lane of Type-C connector 0.
        Upper 2 bits correspond to the upper 2 TX lane on the PHY
        of Type-C connector 0.
        0000 : Reserved
        0001 : PHY TX[0] is used
        0010 : PHY TX[1] is used
        0011 : PHY TX[1:0] is used
        0100 : PHY TX[2] is used
        0101 : Reserved
        0110 : Reserved
        0111 : Reserved
        1000 : PHY TX[3] is used
        1001 : Reserved
        1010 : Reserved
        1011 : Reserved
        1100 : PHY TX[3:2] is used
        1101 : Reserved
        1110 : Reserved
        1111 : PHY TX[3:0] is used
        The Type-C Connector number is logical number. It is not physical lane numbers.
        Refer to the SOC block diagram for the mapping of Type-C Connector number to the actual physical lane number of the PHY.
        SOC FW writes to these bits to tell Display Driver the x4 TX Lane Assignment of Display Port on Type-C Connector 0.
        SOC FW generate the value based on the DP Pin Assignment and the Connector Orientation.
        For example, in DP Pin Assignment D (Multi function) and Flip case, the x2 TX lane are on the upper TypeC Lane hence the value written into this register will be 1100b.
        Another example, in DP Pin Assignment B (Multi function) Active Gen2 cable and Flip case, the x1 TX lane is on the 1st TX of upper TypeC Lane hence the value written into
        this register will be 0100b. This register is not use by HW.

        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector0 : DD_BITFIELD_RANGE(0, 3); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0

        /******************************************************************************************************************


        \******************************************************************************************************************/
        DDU32 DpScratchPadTc0Lsb_Dpsptc0Lsb : DD_BITFIELD_BIT(4); //

        /******************************************************************************************************************


        \******************************************************************************************************************/
        DDU32 Tc0LiveState : DD_BITFIELD_BIT(5);  //
        DDU32 Tbt0LiveState : DD_BITFIELD_BIT(6); //

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(7); // RESERVED
        /******************************************************************************************************************
        Same definition as DFLEXDPSP1.DPX4TXLATC0, but this register is for Type-C Connector 1.

        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector1 : DD_BITFIELD_RANGE(8, 11); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(12); // RESERVED
        /******************************************************************************************************************


        \******************************************************************************************************************/
        DDU32 Tc1LiveState : DD_BITFIELD_BIT(13);  //
        DDU32 Tbt1LiveState : DD_BITFIELD_BIT(14); //

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(15); // RESERVED
        /******************************************************************************************************************
        Same definition as DFLEXDPSP1.DPX4TXLATC0, but this register is for Type-C Connector 2.

        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector2 : DD_BITFIELD_RANGE(16, 19); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(20); // RESERVED
        /******************************************************************************************************************


        \******************************************************************************************************************/
        DDU32 Tc2LiveState : DD_BITFIELD_BIT(21);  //
        DDU32 Tbt2LiveState : DD_BITFIELD_BIT(22); //

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(23); // RESERVED
        /******************************************************************************************************************
        Same definition as DFLEXDPSP1.DPX4TXLATC0, but this register is for Type-C Connector 3.

        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector3 : DD_BITFIELD_RANGE(24, 27); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(28); // RESERVED
        /******************************************************************************************************************


        \******************************************************************************************************************/
        DDU32 Tc3LiveState : DD_BITFIELD_BIT(29);  //
        DDU32 Tbt3LiveState : DD_BITFIELD_BIT(30); //

        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(31); // RESERVED
    };

    DDU32 ulValue;
} PORT_TX_DFLEXDPSP_ICL;

#endif // GEN11INTRREGS_H
