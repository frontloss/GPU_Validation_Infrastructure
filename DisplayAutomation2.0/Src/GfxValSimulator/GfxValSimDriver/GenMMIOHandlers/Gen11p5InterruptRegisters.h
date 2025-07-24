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

#ifndef __GEN11p5INTERRUPT_REGS_H__
#define __GEN11p5INTERRUPT_REGS_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\CommonInclude\\BitDefs.h"
#include "..\\CommonInclude\\\DisplayDefs.h"

typedef enum _MASTER_INTERRUPT_GEN11P5
{
    MASTER_INTERRUPT_DISABLE_GEN11P5 = 0x0,
    MASTER_INTERRUPT_ENABLE_GEN11P5  = 0x1
} MASTER_INTERRUPT_GEN11P5;

typedef enum _GFX_MSTR_INTR_INSTANCE_GEN11P5
{
    GFX_MSTR_INTR_ADDR_GEN11P5 = 0X190010,
} GFX_MSTR_INTR_INSTANCE_GEN11P5;

#define GEN11_MASTER_INTERRUPT_BIT_POS (31)
#define GEN11_PCU_INTERRUPT_BIT_POS (30)
#define GEN11_DISPLAY_INTERRUPT_BIT_POS (16)
#define GEN11_DW1_INTERRUPT_BIT_POS (1)
#define GEN11_DW0_INTERRUPT_BIT_POS (0)

/*****************************************************************************
Description:  Top level register that indicates interrupt from hardware.
Bits in this register are set interrupts are pending in the underlying PCU, display or GT interrupts

******************************************************************************/
typedef union _GFX_MSTR_INTR_GEN11P5 {
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
} GFX_MSTR_INTR_GEN11P5, *PGFX_MSTR_INTR_GEN11P5;

C_ASSERT(4 == sizeof(GFX_MSTR_INTR_GEN11P5));

// IMPLICIT ENUMERATIONS USED BY DISPLAY_INT_CTL_GEN11P5
//
typedef enum _DISPLAY_INTR_GEN11P5
{
    DISPLAY_INTR_DISABLE_GEN11P5 = 0x0,
    DISPLAY_INTR_ENABLE_GEN11P5  = 0x1,
} DISPLAY_INTR_GEN11P5;

typedef enum _DISPLAY_INTR_CTL_INSTANCE_GEN11P5
{
    DISPLAY_INTR_CTL_ADDR_GEN11P5 = 0x44200,
} DISPLAY_INTR_CTL_INSTANCE_GEN11P5;

typedef enum _DISPLAY_INT_CTL_MASKS_GEN11P5
{
    DISPLAY_INT_CTL_MASKS_WO_GEN11P5  = 0x0,
    DISPLAY_INT_CTL_MASKS_MBZ_GEN11P5 = 0x0,
    DISPLAY_INT_CTL_MASKS_PBC_GEN11P5 = 0x0,
} DISPLAY_INT_CTL_MASKS_GEN11P5;

/*****************************************************************************\
This register has the master enable for display interrupts and gives an overview of what interrupts are pending.
An interrupt pending bit will read 1b while one or more interrupts of that category are set (IIR) and enabled (IER).
All Pending Interrupts are ORed together to generate the combined interrupt.
The combined interrupt is ANDed with the Display Interrupt enable to create the display enabled interrupt.
The display enabled interrupt goes to graphics interrupt processing.
The master interrupt enable must be set before any of these interrupts will propagate to graphics interrupt processing.
\*****************************************************************************/
typedef union _DISPLAY_INT_CTL_GEN11P5 {
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
        SIZE32BITS DisplayInterruptEnable : BITFIELD_BIT(31); // DISPLAY_INTR_ENABLE_GEN11P5
    };
    SIZE32BITS ulValue;

} DISPLAY_INT_CTL_GEN11P5, *PDISPLAY_INT_CTL_GEN11P5;

C_ASSERT(4 == sizeof(DISPLAY_INT_CTL_GEN11P5));

// IMPLICIT ENUMERATIONS USED BY DE_PORT_INTR_DEFINITION_GEN11P5
//
typedef enum _DE_PORT_INTR_INSTANCE_GEN11P5
{
    DE_PORT_INTR_ADDR_GEN11P5 = 0x44440,
} DE_PORT_INTR_INSTANCE_GEN11P5;

typedef enum _DE_PORT_INTR_GEN11P5
{
    DE_PORT_INTR_WO_GEN11P5  = 0x0,
    DE_PORT_INTR_MBZ_GEN11P5 = 0x0,
    DE_PORT_INTR_PBC_GEN11P5 = 0x0,
} DE_PORT_INTR_GEN11P5;

#if 0
/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine Port Interrupt registers.
0x44440 = ISR
0x44444 = IMR
0x44448 = IIR
0x4444C = IER
\*****************************************************************************/
typedef union _DE_PORT_INTR_DEFINITION_ICL {
    struct {

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI A done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        SIZE32BITS Aux_Channel_A : BITFIELD_BIT(0); // 

		/*****************************************************************************\
		The ISR is an active high pulse when any of the unmasked events in GMBUS4 Interrupt Mask register occur.
		This field is only used on projects that have GMBUS integrated into the north display. 
		Projects that have GMBUS in the south display have the GMBUS interrupt in the south display interrupts.
		\*****************************************************************************/
        SIZE32BITS Gmbus : BITFIELD_BIT(1); // 
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
        SIZE32BITS DdiCHotplug : BITFIELD_BIT(5); // 
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
#endif

// IMPLICIT ENUMERATIONS USED BY DE_HPD_INTR_DEFINITION_GEN11P5
//
typedef enum _DE_HPD_INTR_INSTANCE_GEN11P5
{
    DE_HPD_INTR_ADDR_GEN11P5 = 0x44470,
} DE_HPD_INTR_INSTANCE_GEN11P5;

typedef enum _DE_HPD_INTR_GEN11P5
{
    DE_HPD_INTR_WO_GEN11P5  = 0x0,
    DE_HPD_INTR_MBZ_GEN11P5 = 0x0,
    DE_HPD_INTR_PBC_GEN11P5 = 0x0,
} DE_HPD_INTR_GEN11P5;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine HPD Interrupt registers.
0x44470 = ISR
0x44474 = IMR
0x44478 = IIR
0x4447C = IER
\*****************************************************************************/
typedef union _DE_HPD_INTR_DEFINITION_GEN11P5 {
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

} DE_HPD_INTR_DEFINITION_GEN11P5, *PDE_HPD_INTR_DEFINITION_GEN11P5;

C_ASSERT(4 == sizeof(DE_HPD_INTR_DEFINITION_GEN11P5));

#if 0
// IMPLICIT ENUMERATIONS USED BY DE_MISC_INTR_DEFINITION_ICL
//
typedef enum _DE_MISC_INTR_INSTANCE_ICL {
    DE_MISC_INTR_ADDR_ICL = 0x44460,
} DE_MISC_INTR_INSTANCE_ICL;

typedef enum _DE_MISC_INTR_ICL {
    DE_MISC_INTR_WO_ICL = 0x0,
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
    struct {

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
        SIZE32BITS Gtc_Interrupts_Combined : BITFIELD_BIT(15); // 
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(16, 17); // MBZ

                                                                  /*****************************************************************************\
                                                                  The ISR is an active high level while any of the WD1_IIR bits are set.
                                                                  \*****************************************************************************/
        SIZE32BITS Wd1_Interrupts_Combined : BITFIELD_BIT(18); // 

                                                               /*****************************************************************************\
                                                               The ISR is an active high level while any of the SRD_IIR bits are set.
                                                               \*****************************************************************************/
        SIZE32BITS Srd_Interrupts_Combined : BITFIELD_BIT(19); // 
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
        SIZE32BITS Dmc_Error : BITFIELD_BIT(25); // 
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
typedef enum _AUDIO_CODEC_INTR_INSTANCE_ICL {
    AUDIO_CODEC_INTR_ADDR_ICL = 0x44480,
} AUDIO_CODEC_INTR_INSTANCE_ICL;

typedef enum _AUDIO_CODEC_INTR_ICL {
    AUDIO_CODEC_INTR_WO_ICL = 0x0,
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
    struct {

        /*****************************************************************************\
        The ISR is an active high pulse when there is a write to any of the four Audio Mail box verbs in vendor defined node ID 8
        \*****************************************************************************/
        SIZE32BITS Audio_Mailbox_Write : BITFIELD_BIT(0); // 

                                                          /*****************************************************************************\
                                                          The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for transcoder A.
                                                          \*****************************************************************************/
        SIZE32BITS Audio_Cp_Change_Transcoder_A : BITFIELD_BIT(1); // 

                                                                   /*****************************************************************************\
                                                                   The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder A. It is valid after the Audio_CP_Change_Transcoder_A event has occurred.
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
                                                                   The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder B. It is valid after the Audio_CP_Change_Transcoder_B event has occurred.
                                                                   \*****************************************************************************/
        SIZE32BITS Audio_Cp_Request_Transcoder_B : BITFIELD_BIT(6); // 

                                                                    /*****************************************************************************\
                                                                    The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for transcoder C.
                                                                    \*****************************************************************************/
        SIZE32BITS Audio_Cp_Change_Transcoder_C : BITFIELD_BIT(7); // 

                                                                   /*****************************************************************************\
                                                                   The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder C. It is valid after the Audio_CP_Change_Transcoder_C event has occurred.
                                                                   \*****************************************************************************/
        SIZE32BITS Audio_Cp_Request_Transcoder_C : BITFIELD_BIT(8); // 

                                                                    /*****************************************************************************\
                                                                    The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for transcoder C.
                                                                    \*****************************************************************************/
        SIZE32BITS Audio_Cp_Change_Transcoder_D : BITFIELD_BIT(9); // 

                                                                   /*****************************************************************************\
                                                                   The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder C. It is valid after the Audio_CP_Change_Transcoder_C event has occurred.
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
                                                            The ISR is an active high level indicating content protection is requested by audio azalia verb programming for WD 0. It is valid after the Audio_CP_Change_WD_0 event has occurred.
                                                            \*****************************************************************************/
        SIZE32BITS Audio_Cp_Request_Wd_0 : BITFIELD_BIT(14); // 

                                                             /*****************************************************************************\
                                                             The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for WD 1.
                                                             \*****************************************************************************/
        SIZE32BITS Audio_Cp_Change_Wd_1 : BITFIELD_BIT(15); // 

                                                            /*****************************************************************************\
                                                            The ISR is an active high level indicating content protection is requested by audio azalia verb programming for WD 0. It is valid after the Audio_CP_Change_WD_1 event has occurred.
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
        SIZE32BITS Spare19 : BITFIELD_BIT(19); // 
        SIZE32BITS Spare20 : BITFIELD_BIT(20); // 
        SIZE32BITS Spare21 : BITFIELD_BIT(21); // 
        SIZE32BITS Spare22 : BITFIELD_BIT(22); // 
        SIZE32BITS Spare23 : BITFIELD_BIT(23); // 
        SIZE32BITS Spare24 : BITFIELD_BIT(24); // 
        SIZE32BITS Spare25 : BITFIELD_BIT(25); // 
        SIZE32BITS Spare26 : BITFIELD_BIT(26); // 

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
typedef enum _DE_PIPE_A_INTR_INSTANCE_ICL {
    DE_PIPE_A_INTR_ADDR_ICL = 0x44400,
} DE_PIPE_A_INTR_INSTANCE_ICL;

typedef enum _DE_PIPE_B_INTR_INSTANCE_ICL {
    DE_PIPE_B_INTR_ADDR_ICL = 0x44410,
} DE_PIPE_B_INTR_INSTANCE_ICL;

typedef enum _DE_PIPE_C_INTR_INSTANCE_ICL {
    DE_PIPE_C_INTR_ADDR_ICL = 0x44420,
} DE_PIPE_C_INTR_INSTANCE_ICL;

typedef enum _DE_PIPE_D_INTR_INSTANCE_ICL {
    DE_PIPE_D_INTR_ADDR_ICL = 0x44430,
} DE_PIPE_D_INTR_INSTANCE_ICL;

typedef enum _DE_PIPE_INTR_MASKS_ICL {
    DE_PIPE_INTR_MASKS_WO_ICL = 0x0,
    DE_PIPE_INTR_MASKS_PBC_ICL = 0x0,
    DE_PIPE_INTR_MASKS_MBZ_ICL = 0xF0000,
} DE_PIPE_INTR_MASKS_ICL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine Pipe Interrupt registers.

The IER enabled Display Engine Pipe Interrupt IIR (sticky) bits are ORed together to generate the DE_Pipe Interrupts Pending bit in the Master Interrupt Control register.

There is one full set of Display Engine Pipe interrupts per display pipes A/B/C.

The STEREO3D_EVENT_MASK selects between left eye and right eye reporting of vertical blank, vertical sync, and scanline events in stereo 3D modes.0x44400 = ISR A, 0x44410 = ISR B, 0x44420 = ISR C, 0x44430 = ISR D
0x44404 = IMR A, 0x44414 = IMR B, 0x44424 = IMR C, 0x44434 = IMR D
0x44408 = IIR A, 0x44418 = IIR B, 0x44428 = IIR C, 0x44438 = IIR D
0x4440C = IER A, 0x4441C = IER B, 0x4442C = IER C, 0x4443C = IER D
\*****************************************************************************/
typedef union _DE_PIPE_INTR_ICL {
    struct {

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
        SIZE32BITS Plane7_Flip_Done : BITFIELD_BIT(18); // 
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
                                                       The ISR is an active high pulse on the eDP/DP Variable Refresh Rate double buffer update event on this pipe. VRR Double Buffer update is triggered by either a master flip or a VRR vblank max time out.
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

#endif

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_DDI_GEN11P5
//
typedef enum _DDIA_HPD_STATUS_GEN11P5
{
    DDIA_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    DDIA_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    DDIA_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    DDIA_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} DDIA_HPD_STATUS_GEN11P5;

typedef enum _DDIA_HPD_OUTPUT_DATA_GEN11P5
{
    DDIA_HPD_OUTPUT_DATA_DRIVE_0_GEN11P5 = 0x0,
    DDIA_HPD_OUTPUT_DATA_DRIVE_1_GEN11P5 = 0x1,
} DDIA_HPD_OUTPUT_DATA_GEN11P5;

typedef enum _DDIA_HPD_ENABLE_GEN11P5
{
    DDIA_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    DDIA_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} DDIA_HPD_ENABLE_GEN11P5;

typedef enum _DDIB_HPD_STATUS_GEN11P5
{
    DDIB_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    DDIB_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    DDIB_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    DDIB_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} DDIB_HPD_STATUS_GEN11P5;

typedef enum _DDIB_HPD_OUTPUT_DATA_GEN11P5
{
    DDIB_HPD_OUTPUT_DATA_DRIVE_0_GEN11P5 = 0x0,
    DDIB_HPD_OUTPUT_DATA_DRIVE_1_GEN11P5 = 0x1,
} DDIB_HPD_OUTPUT_DATA_GEN11P5;

typedef enum _DDIB_HPD_ENABLE_GEN11P5
{
    DDIB_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    DDIB_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} DDIB_HPD_ENABLE_GEN11P5;

typedef enum _DDIC_HPD_STATUS_GEN11P5
{
    DDIC_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    DDIC_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    DDIC_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    DDIC_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} DDIC_HPD_STATUS_GEN11P5;

typedef enum _DDIC_HPD_OUTPUT_DATA_GEN11P5
{
    DDIC_HPD_OUTPUT_DATA_DRIVE_0_GEN11P5 = 0x0,
    DDIC_HPD_OUTPUT_DATA_DRIVE_1_GEN11P5 = 0x1,
} DDIC_HPD_OUTPUT_DATA_GEN11P5;

typedef enum _DDIC_HPD_ENABLE_GEN11P5
{
    DDIC_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    DDIC_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} DDIC_HPD_ENABLE_GEN11P5;

typedef enum _SOUTH_HOT_PLUG_CTL_FOR_DDI_INSTANCE_GEN11P5
{
    SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN11P5 = 0xC4030,
} SOUTH_HOT_PLUG_CTL_FOR_DDI_INSTANCE_GEN11P5;

typedef enum _SHOTPLUG_CTL_DDI_MASKS_GEN11P5
{
    SHOTPLUG_CTL_DDI_MASKS_MBZ_GEN11P5 = 0xFFFFF000,
    SHOTPLUG_CTL_DDI_MASKS_WO_GEN11P5  = 0x0,
    SHOTPLUG_CTL_DDI_MASKS_PBC_GEN11P5 = 0x0,
} SHOTPLUG_CTL_DDI_MASKS_GEN11P5;

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
typedef union _SHOTPLUG_CTL_DDI_GEN11P5 {
    struct
    {
        SIZE32BITS DdiaHpdStatus : BITFIELD_RANGE(0, 1);          // DDIA_HPD_STATUS_GEN11P5
        SIZE32BITS DdiaHpdOutputData : BITFIELD_BIT(2);           // DDIA_HPD_OUTPUT_DATA_GEN11P5
        SIZE32BITS DdiaHpdEnable : BITFIELD_BIT(3);               // DDIA_HPD_ENABLE_GEN11P5
        SIZE32BITS DdibHpdStatus : BITFIELD_RANGE(4, 5);          // DDIB_HPD_STATUS_GEN11P5
        SIZE32BITS DdibHpdOutputData : BITFIELD_BIT(6);           // DDIB_HPD_OUTPUT_DATA_GEN11P5
        SIZE32BITS DdibHpdEnable : BITFIELD_BIT(7);               // DDIB_HPD_ENABLE_GEN11P5
        SIZE32BITS DdicHpdStatus : BITFIELD_RANGE(8, 9);          // DDIC_HPD_STATUS_GEN11P5
        SIZE32BITS DdicHpdOutputData : BITFIELD_BIT(10);          // DDIC_HPD_OUTPUT_DATA_GEN11P5
        SIZE32BITS DdicHpdEnable : BITFIELD_BIT(11);              // DDIC_HPD_ENABLE_GEN11P5
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(12, 31); // MBZ
    };
    SIZE32BITS ulValue;

} SHOTPLUG_CTL_DDI_GEN11P5, *PSHOTPLUG_CTL_DDI_GEN11P5;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_DDI_GEN11P5));

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_TC_GEN11P5
//
typedef enum _TC1_HPD_STATUS_GEN11P5
{
    TC1_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    TC1_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    TC1_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    TC1_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} TC1_HPD_STATUS_GEN11P5;

typedef enum _TC1_HPD_OUTPUT_DATA_GEN11P5
{
    TC1_HPD_OUTPUT_DATA_DRIVE_0_GEN11P5 = 0x0,
    TC1_HPD_OUTPUT_DATA_DRIVE_1_GEN11P5 = 0x1,
} TC1_HPD_OUTPUT_DATA_GEN11P5;

typedef enum _TC1_HPD_ENABLE_GEN11P5
{
    TC1_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    TC1_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} TC1_HPD_ENABLE_GEN11P5;

typedef enum _TC2_HPD_STATUS_GEN11P5
{
    TC2_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    TC2_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    TC2_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    TC2_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} TC2_HPD_STATUS_GEN11P5;

typedef enum _TC2_HPD_OUTPUT_DATA_GEN11P5
{
    TC2_HPD_OUTPUT_DATA_DRIVE_0_GEN11P5 = 0x0,
    TC2_HPD_OUTPUT_DATA_DRIVE_1_GEN11P5 = 0x1,
} TC2_HPD_OUTPUT_DATA_GEN11P5;

typedef enum _TC2_HPD_ENABLE_GEN11P5
{
    TC2_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    TC2_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} TC2_HPD_ENABLE_GEN11P5;

typedef enum _TC3_HPD_STATUS_GEN11P5
{
    TC3_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    TC3_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    TC3_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    TC3_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} TC3_HPD_STATUS_GEN11P5;

typedef enum _TC3_HPD_OUTPUT_DATA_GEN11P5
{
    TC3_HPD_OUTPUT_DATA_DRIVE_0_GEN11P5 = 0x0,
    TC3_HPD_OUTPUT_DATA_DRIVE_1_GEN11P5 = 0x1,
} TC3_HPD_OUTPUT_DATA_GEN11P5;

typedef enum _TC3_HPD_ENABLE_GEN11P5
{
    TC3_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    TC3_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} TC3_HPD_ENABLE_GEN11P5;

typedef enum _TC4_HPD_STATUS_GEN11P5
{
    TC4_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    TC4_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    TC4_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    TC4_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} TC4_HPD_STATUS_GEN11P5;

typedef enum _TC4_HPD_OUTPUT_DATA_GEN11P5
{
    TC4_HPD_OUTPUT_DATA_DRIVE_0_GEN11P5 = 0x0,
    TC4_HPD_OUTPUT_DATA_DRIVE_1_GEN11P5 = 0x1,
} TC4_HPD_OUTPUT_DATA_GEN11P5;

typedef enum _TC4_HPD_ENABLE_GEN11P5
{
    TC4_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    TC4_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} TC4_HPD_ENABLE_GEN11P5;

typedef enum _TC5_HPD_STATUS_GEN11P5
{
    TC5_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    TC5_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    TC5_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    TC5_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} TC5_HPD_STATUS_GEN11P5;

typedef enum _TC5_HPD_OUTPUT_DATA_GEN11P5
{
    TC5_HPD_OUTPUT_DATA_DRIVE_0_GEN11P5 = 0x0,
    TC5_HPD_OUTPUT_DATA_DRIVE_1_GEN11P5 = 0x1,
} TC5_HPD_OUTPUT_DATA_GEN11P5;

typedef enum _TC5_HPD_ENABLE_GEN11P5
{
    TC5_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    TC5_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} TC5_HPD_ENABLE_GEN11P5;

typedef enum _TC6_HPD_STATUS_GEN11P5
{
    TC6_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    TC6_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    TC6_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    TC6_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} TC6_HPD_STATUS_GEN11P5;

typedef enum _TC6_HPD_OUTPUT_DATA_GEN11P5
{
    TC6_HPD_OUTPUT_DATA_DRIVE_0_GEN11P5 = 0x0,
    TC6_HPD_OUTPUT_DATA_DRIVE_1_GEN11P5 = 0x1,
} TC6_HPD_OUTPUT_DATA_GEN11P5;

typedef enum _TC6_HPD_ENABLE_GEN11P5
{
    TC6_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    TC6_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} TC6_HPD_ENABLE_GEN11P5;

typedef enum _SOUTH_HOT_PLUG_CTL_FOR_TYPEC_INSTANCE_GEN11P5
{
    SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN11P5 = 0xC4034,
} SOUTH_HOT_PLUG_CTL_FOR_TYPEC_INSTANCE_GEN11P5;

typedef enum _SHOTPLUG_CTL_TC_MASKS_GEN11P5
{
    SHOTPLUG_CTL_TC_MASKS_MBZ_GEN11P5 = 0xFF000000,
    SHOTPLUG_CTL_TC_MASKS_WO_GEN11P5  = 0x0,
    SHOTPLUG_CTL_TC_MASKS_PBC_GEN11P5 = 0x0,
} SHOTPLUG_CTL_TC_MASKS_GEN11P5;

/*****************************************************************************\
The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port, one of the status bits will set and
the hotplug IIR will be set (if unmasked in the IMR).  The status bits are sticky bits, cleared by writing 1s to the bits.Each HPD pin can be configured as an input or output.  The
HPD status function will only work when the pin is configured as an input.  The HPD Output Data function will only work when the HPD pin is configured as an output.The short pulse
duration is programmed in SHPD_PULSE_CNT.
\*****************************************************************************/
typedef union _SHOTPLUG_CTL_TC_GEN11P5 {
    struct
    {
        SIZE32BITS Tc1HpdStatus : BITFIELD_RANGE(0, 1);           // TC1_HPD_STATUS_GEN11P5
        SIZE32BITS Tc1HpdOutputData : BITFIELD_BIT(2);            // TC1_HPD_OUTPUT_DATA_GEN11P5
        SIZE32BITS Tc1HpdEnable : BITFIELD_BIT(3);                // TC1_HPD_ENABLE_GEN11P5
        SIZE32BITS Tc2HpdStatus : BITFIELD_RANGE(4, 5);           // TC2_HPD_STATUS_GEN11P5
        SIZE32BITS Tc2HpdOutputData : BITFIELD_BIT(6);            // TC2_HPD_OUTPUT_DATA_GEN11P5
        SIZE32BITS Tc2HpdEnable : BITFIELD_BIT(7);                // TC2_HPD_ENABLE_GEN11P5
        SIZE32BITS Tc3HpdStatus : BITFIELD_RANGE(8, 9);           // TC3_HPD_STATUS_GEN11P5
        SIZE32BITS Tc3HpdOutputData : BITFIELD_BIT(10);           // TC3_HPD_OUTPUT_DATA_GEN11P5
        SIZE32BITS Tc3HpdEnable : BITFIELD_BIT(11);               // TC3_HPD_ENABLE_GEN11P5
        SIZE32BITS Tc4HpdStatus : BITFIELD_RANGE(12, 13);         // TC4_HPD_STATUS_GEN11P5
        SIZE32BITS Tc4HpdOutputData : BITFIELD_BIT(14);           // TC4_HPD_OUTPUT_DATA_GEN11P5
        SIZE32BITS Tc4HpdEnable : BITFIELD_BIT(15);               // TC4_HPD_ENABLE_GEN11P5
        SIZE32BITS Tc5HpdStatus : BITFIELD_RANGE(16, 17);         // TC5_HPD_STATUS_GEN11P5
        SIZE32BITS Tc5HpdOutputData : BITFIELD_BIT(18);           // TC5_HPD_OUTPUT_DATA_GEN11P5
        SIZE32BITS Tc5HpdEnable : BITFIELD_BIT(19);               // TC5_HPD_ENABLE_GEN11P5
        SIZE32BITS Tc6HpdStatus : BITFIELD_RANGE(20, 21);         // TC6_HPD_STATUS_GEN11P5
        SIZE32BITS Tc6HpdOutputData : BITFIELD_BIT(22);           // TC6_HPD_OUTPUT_DATA_GEN11P5
        SIZE32BITS Tc6HpdEnable : BITFIELD_BIT(23);               // TC6_HPD_ENABLE_GEN11P5
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(24, 31); // MBZ
    };
    SIZE32BITS ulValue;

} SHOTPLUG_CTL_TC_GEN11P5, *PSHOTPLUG_CTL_TC_GEN11P5;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_TC_GEN11P5));

// The below defines were generated after modifying BXML file. The AublistXML is not able to handle the following changes in bxml that resulted in inablity to generate this without
// modifications 1) "+" as part of project list is not working, so change "SPT+" to "SPT" (upgrading the aublistXML to r92173 resolves this) 2) remove the entire section under
// <DWord Name="0" Project="REMOVEDBY(GEN11:HAS:399096)"> 3) rename the section <DWord Name="0" Project="GEN11:HAS:399096"> to <DWord Name="0>

// IMPLICIT ENUMERATIONS USED BY SOUTH_DE_INTR_BIT_DEFINITION_SPT
//

typedef enum _SOUTH_DE_INTR_INSTANCE_SPT_GEN11P5
{
    SOUTH_DE_INTR_ADDR_SPT_GEN11P5 = 0xC4000,
} SOUTH_DE_INTR_INSTANCE_SPT_GEN11P5;

typedef enum _SOUTH_DE_INTR_BIT_GEN11P5
{
    SOUTH_DE_INTR_BIT_MBZ_GEN11P5 = 0xC078C0F8,
    SOUTH_DE_INTR_BIT_WO_GEN11P5  = 0x0,
    SOUTH_DE_INTR_BIT_PBC_GEN11P5 = 0x0,
} SOUTH_DE_INTR_BIT_GEN11P5;

/*****************************************************************************\
South Display Engine (SDE) interrupt bits come from events within the south display engine.The SDE_IIR bits are ORed together to generate the South/PCH Display Interrupt Event
which will appear in the North Display Engine Interrupt Control Registers.	The South Display Engine Interrupt Control Registers all share the same bit definitions from this table.
\*****************************************************************************/
typedef union _SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5 {
    struct
    {

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        SIZE32BITS ScdcDdia : BITFIELD_BIT(0); //

        /*****************************************************************************\
                                               The IIR is set when a HDMI 2.0 SCDC read request event is detected. The ISR is active high level signal that will indicate if the
           read request (RR) is still active.
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

} SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5, *PSOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5;

C_ASSERT(4 == sizeof(SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5));

// IMPLICIT ENUMERATIONS USED BY HOTPLUG_CTL_GEN11P5
//
typedef enum _PORT1_HPD_STATUS_GEN11P5
{
    PORT1_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    PORT1_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    PORT1_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    PORT1_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} PORT1_HPD_STATUS_GEN11P5;

typedef enum _PORT1_HPD_ENABLE_GEN11P5
{
    PORT1_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    PORT1_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} PORT1_HPD_ENABLE_GEN11P5;

typedef enum _PORT2_HPD_STATUS_GEN11P5
{
    PORT2_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    PORT2_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    PORT2_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    PORT2_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} PORT2_HPD_STATUS_GEN11P5;

typedef enum _PORT2_HPD_ENABLE_GEN11P5
{
    PORT2_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    PORT2_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} PORT2_HPD_ENABLE_GEN11P5;

typedef enum _PORT3_HPD_STATUS_GEN11P5
{
    PORT3_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    PORT3_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    PORT3_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    PORT3_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} PORT3_HPD_STATUS_GEN11P5;

typedef enum _PORT3_HPD_ENABLE_GEN11P5
{
    PORT3_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    PORT3_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} PORT3_HPD_ENABLE_GEN11P5;

typedef enum _PORT4_HPD_STATUS_GEN11P5
{
    PORT4_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    PORT4_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    PORT4_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    PORT4_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} PORT4_HPD_STATUS_GEN11P5;

typedef enum _PORT4_HPD_ENABLE_GEN11P5
{
    PORT4_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    PORT4_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} PORT4_HPD_ENABLE_GEN11P5;

typedef enum _PORT5_HPD_STATUS_GEN11P5
{
    PORT5_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    PORT5_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    PORT5_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    PORT5_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} PORT5_HPD_STATUS_GEN11P5;

typedef enum _PORT5_HPD_ENABLE_GEN11P5
{
    PORT5_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    PORT5_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} PORT5_HPD_ENABLE_GEN11P5;

typedef enum _PORT6_HPD_STATUS_GEN11P5
{
    PORT6_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    PORT6_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    PORT6_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    PORT6_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} PORT6_HPD_STATUS_GEN11P5;

typedef enum _PORT6_HPD_ENABLE_GEN11P5
{
    PORT6_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    PORT6_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} PORT6_HPD_ENABLE_GEN11P5;

typedef enum _PORT7_HPD_STATUS_GEN11P5
{
    PORT7_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    PORT7_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    PORT7_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    PORT7_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} PORT7_HPD_STATUS_GEN11P5;

typedef enum _PORT7_HPD_ENABLE_GEN11P5
{
    PORT7_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    PORT7_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} PORT7_HPD_ENABLE_GEN11P5;

typedef enum _PORT8_HPD_STATUS_GEN11P5
{
    PORT8_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN11P5    = 0x0,
    PORT8_HPD_STATUS_SHORT_PULSE_DETECTED_GEN11P5           = 0x1,
    PORT8_HPD_STATUS_LONG_PULSE_DETECTED_GEN11P5            = 0x2,
    PORT8_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN11P5 = 0x3,
} PORT8_HPD_STATUS_GEN11P5;

typedef enum _PORT8_HPD_ENABLE_GEN11P5
{
    PORT8_HPD_ENABLE_DISABLE_GEN11P5 = 0x0,
    PORT8_HPD_ENABLE_ENABLE_GEN11P5  = 0x1,
} PORT8_HPD_ENABLE_GEN11P5;

typedef enum _THUNDERBOLT_HOT_PLUG_CTL_INSTANCE_GEN11P5
{
    THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN11P5 = 0x44030,
} THUNDERBOLT_HOT_PLUG_CTL_INSTANCE_GEN11P5;

typedef enum _TYPE_C_HOT_PLUG_CTL_INSTANCE_GEN11P5
{
    TYPE_C_HOT_PLUG_CTL_ADDR_GEN11P5 = 0x44038,
} TYPE_C_HOT_PLUG_CTL_INSTANCE_GEN11P5;

typedef enum _HOTPLUG_CTL_MASKS_GEN11P5
{
    HOTPLUG_CTL_MASKS_WO_GEN11P5  = 0x0,
    HOTPLUG_CTL_MASKS_MBZ_GEN11P5 = 0x0,
    HOTPLUG_CTL_MASKS_PBC_GEN11P5 = 0x0,
} HOTPLUG_CTL_MASKS_GEN11P5;

typedef union _HOTPLUG_CTL_GEN11P5 {
    struct
    {
        SIZE32BITS Port1HpdStatus : BITFIELD_RANGE(0, 1);   // PORT1_HPD_STATUS_GEN11P5
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(2);  //
        SIZE32BITS Port1HpdEnable : BITFIELD_BIT(3);        // PORT1_HPD_ENABLE_GEN11P5
        SIZE32BITS Port2HpdStatus : BITFIELD_RANGE(4, 5);   // PORT2_HPD_STATUS_GEN11P5
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(6);  //
        SIZE32BITS Port2HpdEnable : BITFIELD_BIT(7);        // PORT2_HPD_ENABLE_GEN11P5
        SIZE32BITS Port3HpdStatus : BITFIELD_RANGE(8, 9);   // PORT3_HPD_STATUS_GEN11P5
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(10); //
        SIZE32BITS Port3HpdEnable : BITFIELD_BIT(11);       // PORT3_HPD_ENABLE_GEN11P5
        SIZE32BITS Port4HpdStatus : BITFIELD_RANGE(12, 13); // PORT4_HPD_STATUS_GEN11P5
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(14); //
        SIZE32BITS Port4HpdEnable : BITFIELD_BIT(15);       // PORT4_HPD_ENABLE_GEN11P5
        SIZE32BITS Port5HpdStatus : BITFIELD_RANGE(16, 17); // PORT5_HPD_STATUS_GEN11P5
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(18); //
        SIZE32BITS Port5HpdEnable : BITFIELD_BIT(19);       // PORT5_HPD_ENABLE_GEN11P5
        SIZE32BITS Port6HpdStatus : BITFIELD_RANGE(20, 21); // PORT6_HPD_STATUS_GEN11P5
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(22); //
        SIZE32BITS Port6HpdEnable : BITFIELD_BIT(23);       // PORT6_HPD_ENABLE_GEN11P5
        SIZE32BITS Port7HpdStatus : BITFIELD_RANGE(24, 25); // PORT7_HPD_STATUS_GEN11P5
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(26); //
        SIZE32BITS Port7HpdEnable : BITFIELD_BIT(27);       // PORT7_HPD_ENABLE_GEN11P5
        SIZE32BITS Port8HpdStatus : BITFIELD_RANGE(28, 29); // PORT8_HPD_STATUS_GEN11P5
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(30); //
        SIZE32BITS Port8HpdEnable : BITFIELD_BIT(31);       // PORT8_HPD_ENABLE_GEN11P5
    };
    SIZE32BITS ulValue;

} HOTPLUG_CTL_GEN11P5, *PHOTPLUG_CTL_GEN11P5;

C_ASSERT(4 == sizeof(HOTPLUG_CTL_GEN11P5));

typedef enum _PORT_TX_DFLEXDPPMS_INSTANCE_GEN11P5
{
    PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN11P5 = 0x163890,
    PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN11P5 = 0x16E890,
    PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN11P5 = 0x16F890,
} PORT_TX_DFLEXDPPMS_INSTANCE_GEN11P5;

/*****************************************************************************
Description:  PD FW writes  1  to this register's bit to tell DP Driver that it had put the FIA and PHY into DP PHY Mode and it s safe now for DP Driver to proceed to bring up the
DP Controller. Once DP Driver poll a value  1  in this register, DP Driver write  0  to clear this bit for PD FW to use it in the next round.

******************************************************************************/
typedef union _PORT_TX_DFLEXDPPMS_GEN11P5 {
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
} PORT_TX_DFLEXDPPMS_GEN11P5;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXDPPMS_GEN11P5));

typedef enum _PORT_TX_LANES_ALLOCATED_D11P5
{
    D11P5_PHY_TX0_ALONE       = 0x1,
    D11P5_PHY_TX1_ALONE       = 0x2,
    D11P5_PHY_TX1_TX0         = 0x3,
    D11P5_PHY_TX2_ALONE       = 0x4,
    D11P5_PHY_TX3_ALONE       = 0x8,
    D11P5_PHY_TX3_TX2         = 0xC,
    D11P5_PHY_TX3_TX2_TX1_TX0 = 0xF,
} PORT_TX_LANES_ALLOCATED_D11P5;

typedef enum _PORT_TX_DFLEXDPSP_INSTANCE_D11P5
{
    PORT_TX_DFLEXDPSP1_FIA1_ADDR_D11P5 = 0x1638A0,
    PORT_TX_DFLEXDPSP2_FIA1_ADDR_D11P5 = 0x1638A4,
    PORT_TX_DFLEXDPSP3_FIA1_ADDR_D11P5 = 0x1638A8,
    PORT_TX_DFLEXDPSP4_FIA1_ADDR_D11P5 = 0x1638AC,
    PORT_TX_DFLEXDPSP1_FIA2_ADDR_D11P5 = 0x16E8A0,
    PORT_TX_DFLEXDPSP2_FIA2_ADDR_D11P5 = 0x16E8A4,
    PORT_TX_DFLEXDPSP3_FIA2_ADDR_D11P5 = 0x16E8A8,
    PORT_TX_DFLEXDPSP4_FIA2_ADDR_D11P5 = 0x16E8AC,
    PORT_TX_DFLEXDPSP1_FIA3_ADDR_D11P5 = 0x16F8A0,
    PORT_TX_DFLEXDPSP2_FIA3_ADDR_D11P5 = 0x16F8A4,
    PORT_TX_DFLEXDPSP3_FIA3_ADDR_D11P5 = 0x16F8A8,
    PORT_TX_DFLEXDPSP4_FIA3_ADDR_D11P5 = 0x16F8AC,
} PORT_TX_DFLEXDPSP_INSTANCE_D11P5;

/*****************************************************************************
Description:  Dynamic FlexIO DP Scratch Pad (Type-C)
There are 4 instances of this register per FIA.
DFLEXDPSP1 supports connectors 0-3 (logical number).
DFLEXDPSP2supports connectors 4-7(logical number).
DFLEXDPSP3supports connectors 8-11(logical number).
DFLEXDPSP4supports connectors 12-15(logical number).
The connector number specified in these fields is relative to the connector supproted by this register instance. ie. DFLEXDPSP2 field Display Port x4 TX Lane Assignment for Type-C
Connector 0 is referring to connector 4 (logical number), andDFLEXDPSP4 fieldDisplay Port x4 TX Lane Assignment for Type-C Connector 3 is referring to connector 15 (local number).

******************************************************************************/
typedef union _PORT_TX_DFLEXDPSP_D11P5 {
    struct
    {
        /******************************************************************************************************************
        Display Port x4 TX Lane Assignment for Type-C Connector 0(DPX4TXLATC0):
        4 bits correspond to 4 TX, i.e. TX[3:0] Lane in PHY.
        Lower 2 bits correspond to the 2 lower TX lane on the PHY lane of Type-C connector 0.
        Upper 2 bits correspond to the upper 2 TX lane on the PHY of Type-C connector 0.
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
        The Type-C Connector number is logical number. It s not physical lane numbers.
        Refer to the SOC block diagram for the mapping of Type-C Connector number to the actual physical lane number of the PHY.
        SOC FW writes to these bits to tell Display Driver the x4 TX Lane Assignment of Display Port on Type-C Connector 0.
        SOC FW generate the value based on the DP Pin Assignment and the Connector Orientation.
        For example, in DP Pin Assignment D (Multi function) and Flip case, the x2 TX lane are on the upper MG Lane hence the value written into this register will be 1100b.
        Another example, in DP Pin Assignment B (Multi function) Active Gen2 cable and Flip case, the x1 TX lane is on the 1st TX of upper MG Lane hence the value written into this
        register will be 0100b. This register is not use by HW.



        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector0 : DD_BITFIELD_RANGE(0, 3); //

        /******************************************************************************************************************
        This bit is set by IOM FW and read by Display Driver. It tells the Display Driver if Modular FIA is used in the SOC.
        If Modular FIA is used in the SOC, then Display Driver will access the additional instances of FIA based on pre-assigned offset in Gunit s GTTMADDR space.
        Each Modular FIA instance has its own IOSF Sideband Port ID and it houses only 2 Type-C Port. Hence in SOC that have more than two Type-C Ports and hence multiple instances
        of Modular FIA, Gunit will need to use different destination ID when it access different pair of Type-C Port. If Modular FIA is not used in the SOC, then a single
        monolithic FIA is used to house all the Type-C Ports which has only one IOSF Sideband Port ID. If Modular FIA is used in the SOC, this register bit MF exist in all the
        instances of Modular FIA. IOM FW is required to program only the MF bit in first FIA instance that house the Type-C Port 0 and Port 1, for Display Driver to read from.

        \******************************************************************************************************************/
        DDU32 ModularFia_Mf : DD_BITFIELD_BIT(4); // MODULAR_FIA_MF

        /******************************************************************************************************************


        \******************************************************************************************************************/
        DDU32 DpScratchPadTc0_Dpsptc0 : DD_BITFIELD_RANGE(5, 7); //

        /******************************************************************************************************************
        Similar to register DFLEXDPSP1.DPX4TXLATC0 but this register is for Type-C Connector 1.

        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector1 : DD_BITFIELD_RANGE(8, 11); //

        /******************************************************************************************************************


        \******************************************************************************************************************/
        DDU32 DpScratchPadTc1_Dpsptc1 : DD_BITFIELD_RANGE(12, 15); //

        /******************************************************************************************************************
        Similar to register DFLEXDPSP1.DPX4TXLATC0 but this register is for Type-C Connector 2.

        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector2 : DD_BITFIELD_RANGE(16, 19); //

        /******************************************************************************************************************


        \******************************************************************************************************************/
        DDU32 DpScratchPadTc2_Dpsptc2 : DD_BITFIELD_RANGE(20, 23); //

        /******************************************************************************************************************
        Similar to register DFLEXDPSP1.DPX4TXLATC0 but this register is for Type-C Connector 3.


        \******************************************************************************************************************/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector3 : DD_BITFIELD_RANGE(24, 27); //

        /******************************************************************************************************************


        \******************************************************************************************************************/
        DDU32 DpScratchPadTc3_Dpsptc3 : DD_BITFIELD_RANGE(28, 31); //
    };

    DDU32 ulValue;

} PORT_TX_DFLEXDPSP_D11P5;

/**********************************************************************************************************************************************************************************************
***********************************************************************************************************************************************************************************************/
typedef enum _DISPLAYPORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0_ENUM_D11P5
{
    DISPLAYPORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0_DP_CONTROLLER_IS_NOT_IN_SAFE_STATE_D11P5 = 0x1,
    DISPLAYPORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0_DP_CONTROLLER_IS_IN_SAFE_STATE_D11P5     = 0x0,

} DISPLAYPORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0_ENUM_D11P5;

typedef enum _PORT_TX_DFLEXDPCSSS_INSTANCE_D11P5
{
    PORT_TX_DFLEXDPCSSS_FIA1_ADDR_D11P5 = 0x163894,
    PORT_TX_DFLEXDPCSSS_FIA2_ADDR_D11P5 = 0x16E894,
    PORT_TX_DFLEXDPCSSS_FIA3_ADDR_D11P5 = 0x16F894,
} PORT_TX_DFLEXDPCSSS_INSTANCE_D11P5;

/*****************************************************************************
Description:  The Type-C Connector number (e.g. "0" in register DPPMSTC0) is logical number.

******************************************************************************/
typedef union _PORT_TX_DFLEXDPCSSS_D11P5 {
    struct
    {
        /******************************************************************************************************************
         Displayport Phy Mode Status for Type-C Connector 0 (DPPMSTC0): The Type-C Connector number is logical number. It is not physical lane numbers. Refer to the SoC block
        diagram for the mapping of Type-C Connector number to the actual physical lane number of the PHY.
        \******************************************************************************************************************/
        DDU32 DisplayportPhyModeStatusForTypeCConnector0 : DD_BITFIELD_BIT(0); // DISPLAYPORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0

        /******************************************************************************************************************
        Similar to register DFLEXDPCSSS.DPPMSTC0 but this register is for Type-C Connector 1.
        \******************************************************************************************************************/
        DDU32 DisplayportPhyModeStatusForTypeCConnector1 : DD_BITFIELD_BIT(1); //

        /******************************************************************************************************************
        Similar to register DFLEXDPCSSS.DPPMSTC0 but this register is for Type-C Connector 2.
        \******************************************************************************************************************/
        DDU32 DisplayportPhyModeStatusForTypeCConnector2 : DD_BITFIELD_BIT(2); //

        /******************************************************************************************************************
        Similar to register DFLEXDPCSSS.DPPMSTC0 but this register is for Type-C Connector 3.
        \******************************************************************************************************************/
        DDU32 DisplayportPhyModeStatusForTypeCConnector3 : DD_BITFIELD_BIT(3); //

        /******************************************************************************************************************
        Similar to register DFLEXDPCSSS.DPPMSTC0 but this register is for Type-C Connector 4.
        \******************************************************************************************************************/
        DDU32 DisplayportPhyModeStatusForTypeCConnector4 : DD_BITFIELD_BIT(4); //

        /******************************************************************************************************************
        Similar to register DFLEXDPCSSS.DPPMSTC0 but this register is for Type-C Connector 5.
        \******************************************************************************************************************/
        DDU32 DisplayportPhyModeStatusForTypeCConnector5 : DD_BITFIELD_BIT(5); //

        /******************************************************************************************************************
        Similar to register DFLEXDPCSSS.DPPMSTC0 but this register is for Type-C Connector 6.
        \******************************************************************************************************************/
        DDU32 DisplayportPhyModeStatusForTypeCConnector6 : DD_BITFIELD_BIT(6); //

        /******************************************************************************************************************
        Similar to register DFLEXDPCSSS.DPPMSTC0 but this register is for Type-C Connector 7.
        \******************************************************************************************************************/
        DDU32 DisplayportPhyModeStatusForTypeCConnector7 : DD_BITFIELD_BIT(7); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(8, 31); //
    };

    DDU32 Value;

} PORT_TX_DFLEXDPCSSS_D11P5;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXDPCSSS_D11P5));

/**********************************************************************************************************************************************************************************************
***********************************************************************************************************************************************************************************************/
typedef enum _DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ENUM_D11P5
{
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML0_D11P5  = 0x1,
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML10_D11P5 = 0x3,
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML32_D11P5 = 0xC,
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML30_D11P5 = 0xF,

} DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ENUM_D11P5;

typedef enum _PORT_TX_DFLEXDPMLE1_INSTANCE_D11P5
{
    PORT_TX_DFLEXDPMLE1_FIA1_ADDR_D11P5 = 0x1638C0,
    PORT_TX_DFLEXDPMLE1_FIA2_ADDR_D11P5 = 0x16E8C0,
    PORT_TX_DFLEXDPMLE1_FIA3_ADDR_D11P5 = 0x16F8C0,
} PORT_TX_DFLEXDPMLE1_INSTANCE_D11P5;

/*****************************************************************************
Description:   Display Driver writes to these bits to tell FIA hardware which Main Links of the Display Port are enabled on Type-C Connector 0. FIA hardware uses this information
for PHY to Controller signal mapping. For example, in DP Pin Assignment C, the register DFLEXDPSP1.DPX4TXLATC0 tells Display Driver that all the 4 TX Lanes in PHY can be used.
However, Display Driver may choose to use only x1, i.e. for ML0. Then Display Driver will program “0001b” to this register. For x2 and x4, Display Driver will program “0011b” and
“1111b”, respectively. In the case of "No pin assignment" (fixed or static DP connection in Gen11 MG PHY programming page), if display driver chooses to use only x2 with no lane
reversal, then display driver will program "0011" to this register. If display driver chooses to use only x2 with lane reversal, then display driver will program "1100" to this
register. If display driver chooses to use only x1 with no lane reversal, then display driver will program "0001" to this register. If display driver chooses to use only x1 with
lane reversal, then display driver will program "1000" to this register. Display Driver is expected to write to this register when the DDI Interface between DP Controller and FIA
is in the Safe Mode, e.g. pllen=pwrreq=lane_enable=0. Display Driver writes to this register and then only it brings up the DP Controller, i.e. to bring the DDI interface out from
Safe Mode. A mode set is required to switch the number of DP lanes. This register is applciable in both Type-C connector's Alternate mode and also DP connector mode.

******************************************************************************/
typedef union _PORT_TX_DFLEXDPMLE1_D11P5 {
    struct
    {
        /******************************************************************************************************************
         Display Port Main Link Enable for Type-C Connector 0 (DPMLETC0): 4 bits correspond to 4 Main Link in DP Controller. Bit [0] is ML0,bit [1] is ML1 and so on. The Type-C
        Connector number is logical number. Its not physical lane numbers. Refer to the SOC block diagram for the mapping of Type-C Connector number to the actual physical lane
        number of the PHY. Display Driver writes to these bits to tell FIA hardware which Main Links of the Display Port are enabled on Type-C Connector 0. FIA hardware use this
        information for PHY to Controller signal mapping. For example, in DP Pin Assignment C, the register DFLEXDPSP1.DPX4TXLATC0 tells Display Driver that all the 4 TX Lane in
        PHY can be used. However, Display Driver may choose to use only x1, i.e. for ML0. Then Display Driver will program 0001b to this register. For x2 and x4, Display Driver
        will program 0011b and 1111b, respectively.
        \******************************************************************************************************************/
        DDU32 DisplayportMainLinkEnableForTypeCConnector0 : DD_BITFIELD_RANGE(0, 3); // DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0

        /******************************************************************************************************************
         Similar to register DFLEXDPMLE1.DPMLETC0 but this register is for Type-C Connector 1.
        \******************************************************************************************************************/
        DDU32 DisplayportMainLinkEnableForTypeCConnector1 : DD_BITFIELD_RANGE(4, 7); // DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1

        /******************************************************************************************************************
        Similar to register DFLEXDPMLE1.DPMLETC0 but this register is for Type-C Connector 2.
        \******************************************************************************************************************/
        DDU32 DisplayportMainLinkEnableForTypeCConnector2 : DD_BITFIELD_RANGE(8, 11); // DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2

        /******************************************************************************************************************
        Similar to register DFLEXDPMLE1.DPMLETC0 but this register is for Type-C Connector 3.
        \******************************************************************************************************************/
        DDU32 DisplayportMainLinkEnableForTypeCConnector3 : DD_BITFIELD_RANGE(12, 15); // DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3

        /******************************************************************************************************************
        Similar to register DFLEXDPMLE1.DPMLETC0 but this register is for Type-C Connector 4.
        \******************************************************************************************************************/
        DDU32 DisplayportMainLinkEnableForTypeCConnector4 : DD_BITFIELD_RANGE(16, 19); // DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4

        /******************************************************************************************************************
        Similar to register DFLEXDPMLE1.DPMLETC0 but this register is for Type-C Connector 5.
        \******************************************************************************************************************/
        DDU32 DisplayportMainLinkEnableForTypeCConnector5 : DD_BITFIELD_RANGE(20, 23); // DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5

        /******************************************************************************************************************
        Similar to register DFLEXDPMLE1.DPMLETC0 but this register is for Type-C Connector 6.
        \******************************************************************************************************************/
        DDU32 DisplayportMainLinkEnableForTypeCConnector6 : DD_BITFIELD_RANGE(24, 27); // DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6

        /******************************************************************************************************************
        Similar to register DFLEXDPMLE1.DPMLETC0 but this register is for Type-C Connector 7.
        \******************************************************************************************************************/
        DDU32 DisplayportMainLinkEnableForTypeCConnector7 : DD_BITFIELD_RANGE(28, 31); // DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7
    };

    DDU32 Value;

} PORT_TX_DFLEXDPMLE1_D11P5;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXDPMLE1_D11P5));



/**********************************************************************************************************************************************************************************************
***********************************************************************************************************************************************************************************************/
typedef enum _DKL_PHY_BASE_ADDR_LKF
{
    DKL_PHYBASE_PORT1_ADDR = 0x168000,
    DKL_PHYBASE_PORT2_ADDR = 0x169000,
} DKL_PHY_BASE_ADDR_LKF;

typedef enum _DKL_TX_DPCNTL0_L_INSTANCE_LKF
{
    DKL_TX_DPCTRL0_L_TX1LN0_ADDR_LKF = 0x2C0,
} DKL_TX_DPCNTL0_L_INSTANCE_LKF;

typedef enum _DKL_TX_DPCNTL1_L_INSTANCE_LKF
{
    DKL_TX_DPCNTL1_L_TX2LN0_ADDR_LKF = 0x2C4,
} DKL_TX_DPCNTL1_L_INSTANCE_LKF;

typedef enum _DKL_TX_DPCNTL2_INSTANCE_LKF
{
    DKL_TX_DPCNTL2_TX2LN0_ADDR_LKF = 0x2C8,
} DKL_TX_DPCNTL2_INSTANCE_LKF;

typedef enum _DKL_DP_MODE_INSTANCE_LKF
{
    DKL_DP_MODE_LN0_ACU_ADDR_LKF = 0x0A0,
} DKL_DP_MODE_INSTANCE_LKF;

/**********************************************************************************************************************************************************************************************
***********************************************************************************************************************************************************************************************/

//To support ESD for MIPI

typedef enum _DE_PORT_INTERRUPT_DEFINITION_INSTANCE_D11P5
{
    DE_PORT_ISR_ADDR_D11P5 = 0x44440,
    DE_PORT_IMR_ADDR_D11P5 = 0x44444,
    DE_PORT_IIR_ADDR_D11P5 = 0x44448,
    DE_PORT_IER_ADDR_D11P5 = 0x4444C,
} DE_PORT_INTERRUPT_DEFINITION_INSTANCE_D11P5;

/*****************************************************************************
Description:   This table indicates which events are mapped to each bit of the Display Engine Port Interrupt registers. 0x44440 = ISR 0x44444 = IMR 0x44448 = IIR 0x4444C = IER

******************************************************************************/
typedef union _DE_PORT_INTERRUPT_DEFINITION_D11P5 {
    struct
    {
        /******************************************************************************************************************
        The ISR is an active high pulse on the AUX done event. This event will not occur for HW triggered AUX transactions.
        \******************************************************************************************************************/
        DDU32 AuxDdia : DD_BITFIELD_BIT(0); //

        /******************************************************************************************************************
        The ISR is an active high pulse on the AUX done event. This event will not occur for HW triggered AUX transactions.
        \******************************************************************************************************************/
        DDU32 AuxDdib : DD_BITFIELD_BIT(1); //

        /******************************************************************************************************************
        The ISR is an active high pulse on the AUX done event. This event will not occur for HW triggered AUX transactions.
        \******************************************************************************************************************/
        DDU32 AuxDdic : DD_BITFIELD_BIT(2); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(3, 7); //

        /******************************************************************************************************************
        The ISR is an active high pulse on the AUX done event. This event will not occur for HW triggered AUX transactions.
        \******************************************************************************************************************/
        DDU32 AuxUsbc1 : DD_BITFIELD_BIT(8); //

        /******************************************************************************************************************
        The ISR is an active high pulse on the AUX done event. This event will not occur for HW triggered AUX transactions.
        \******************************************************************************************************************/
        DDU32 AuxUsbc2 : DD_BITFIELD_BIT(9); //

        /******************************************************************************************************************
        The ISR is an active high pulse on the AUX done event. This event will not occur for HW triggered AUX transactions.
        \******************************************************************************************************************/
        DDU32 AuxUsbc3 : DD_BITFIELD_BIT(10); //

        /******************************************************************************************************************
        The ISR is an active high pulse on the AUX done event. This event will not occur for HW triggered AUX transactions.
        \******************************************************************************************************************/
        DDU32 AuxUsbc4 : DD_BITFIELD_BIT(11); //

        /******************************************************************************************************************
        The ISR is an active high pulse on the AUX done event. This event will not occur for HW triggered AUX transactions.
        \******************************************************************************************************************/
        DDU32 AuxUsbc5 : DD_BITFIELD_BIT(12); //

        /******************************************************************************************************************
        The ISR is an active high pulse on the AUX done event. This event will not occur for HW triggered AUX transactions.
        \******************************************************************************************************************/
        DDU32 AuxUsbc6 : DD_BITFIELD_BIT(13); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(14, 16); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(17, 22); //

        /******************************************************************************************************************
        The ISR is an active high level indicating a TE interrupt is set in DSI_INTER_IDENT_REG_0.
        \******************************************************************************************************************/
        DDU32 Dsi0Te : DD_BITFIELD_BIT(23); //

        /******************************************************************************************************************
        The ISR is an active high level indicating a TE interrupt is set in DSI_INTER_IDENT_REG_1.
        \******************************************************************************************************************/
        DDU32 Dsi1Te : DD_BITFIELD_BIT(24); //

        /******************************************************************************************************************/
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(25, 29); //

        /******************************************************************************************************************
        The ISR is an active high level indicating a non-TE interrupt is set in DSI_INTER_IDENT_REG_0.
        \******************************************************************************************************************/
        DDU32 Dsi0 : DD_BITFIELD_BIT(30); //

        /******************************************************************************************************************
        The ISR is an active high level indicating a non-TE interrupt is set in DSI_INTER_IDENT_REG_1.
        \******************************************************************************************************************/
        DDU32 Dsi1 : DD_BITFIELD_BIT(31); //
    };

    DDU32 Value;

} DE_PORT_INTERRUPT_DEFINITION_D11P5;

C_ASSERT(4 == sizeof(DE_PORT_INTERRUPT_DEFINITION_D11P5));


//
typedef enum _DSI_INTER_IDENT_REG_INSTANCE_D11
{
    DSI_INTER_IDENT_REG_0_ADDR_D11 = 0x6B074,
    DSI_INTER_IDENT_REG_1_ADDR_D11 = 0x6B874,
} DSI_INTER_IDENT_REG_INSTANCE_D11;

/*****************************************************************************
Description:  The DSI Interrupt Identity Register (IIR)  logs non-masked DSI interrupts received from the Periphery and Host. The DSI_INTER_MSK_REG (IMR) controls which interrupts
will be logged within the IIR.

******************************************************************************/
typedef union _DSI_INTER_IDENT_REG_D11 {
    struct
    {
        /******************************************************************************************************************
        Peripheral reported a Start of Transmission Error
        \******************************************************************************************************************/
        DDU32 SotError : DD_BITFIELD_BIT(0); //

        /******************************************************************************************************************
        Peripheral reported a Start of Transmission leader sequence corruption error
        \******************************************************************************************************************/
        DDU32 SotSyncError : DD_BITFIELD_BIT(1); //

        /******************************************************************************************************************
        Peripheral reported an End of Transmission byte alignment problem
        \******************************************************************************************************************/
        DDU32 EotSyncError : DD_BITFIELD_BIT(2); //

        /******************************************************************************************************************
        Peripheral reported an Escape Mode entry command error
        \******************************************************************************************************************/
        DDU32 PeripheralEscapeModeEntryCommandError : DD_BITFIELD_BIT(3); //

        /******************************************************************************************************************
        Peripheral reported a LP Transmission byte alignment problem
        \******************************************************************************************************************/
        DDU32 PeripheralLowPowerTransmitSyncError : DD_BITFIELD_BIT(4); //

        /******************************************************************************************************************
        Peripheral reported a timeout error
        \******************************************************************************************************************/
        DDU32 PeripheralTimeoutError : DD_BITFIELD_BIT(5); //

        /******************************************************************************************************************
        Peripheral reported a False Control error
        \******************************************************************************************************************/
        DDU32 PeripheralFalseControlError : DD_BITFIELD_BIT(6); //

        /******************************************************************************************************************
        Peripheral reported a LP contention
        \******************************************************************************************************************/
        DDU32 PeripheralContentionDetected : DD_BITFIELD_BIT(7); //

        /******************************************************************************************************************
        Peripheral reported a single-bit ECC error
        \******************************************************************************************************************/
        DDU32 PeripheralSingleEccError : DD_BITFIELD_BIT(8); //

        /******************************************************************************************************************
        Peripheral reported a multi-bit ECC error
        \******************************************************************************************************************/
        DDU32 PeripheralMultiEccError : DD_BITFIELD_BIT(9); //

        /******************************************************************************************************************
        Peripheral reported a checksum error
        \******************************************************************************************************************/
        DDU32 PeripheralChecksumError : DD_BITFIELD_BIT(10); //

        /******************************************************************************************************************
        Peripheral reported a non-recognizable DSI Data Type
        \******************************************************************************************************************/
        DDU32 InvalidDataType : DD_BITFIELD_BIT(11); //

        /******************************************************************************************************************
        Peripheral reported an invalid DSI VC ID
        \******************************************************************************************************************/
        DDU32 InvalidVc : DD_BITFIELD_BIT(12); //

        /******************************************************************************************************************
        Peripheral reported an invalid transmission length
        \******************************************************************************************************************/
        DDU32 InvalidTxLength : DD_BITFIELD_BIT(13); //

        /******************************************************************************************************************
         Spare R/WC bit for future use
        \******************************************************************************************************************/
        DDU32 Spare14 : DD_BITFIELD_BIT(14); //

        /******************************************************************************************************************
        Peripheral reported a protocol violation
        \******************************************************************************************************************/
        DDU32 ProtocolViolation : DD_BITFIELD_BIT(15); //

        /******************************************************************************************************************
         A frame update is done. This interrupt is only valid when the transcoder is in Command Mode
        \******************************************************************************************************************/
        DDU32 FrameUpdateDone : DD_BITFIELD_BIT(16); //

        /******************************************************************************************************************
         Spare R/WC bits for future use
        \******************************************************************************************************************/
        DDU32 Spare18_17 : DD_BITFIELD_RANGE(17, 18); //

        /******************************************************************************************************************
        Host reported an Escape Mode entry command error
        \******************************************************************************************************************/
        DDU32 HostEscapeModeEntryCommandError : DD_BITFIELD_BIT(19); //

        /******************************************************************************************************************
        Host reported a LP Transmission byte alignment problem
        \******************************************************************************************************************/
        DDU32 HostLowPowerTransmitSyncError : DD_BITFIELD_BIT(20); //

        /******************************************************************************************************************
        Host reported a Timeouterror
        \******************************************************************************************************************/
        DDU32 HostTimeoutError : DD_BITFIELD_BIT(21); //

        /******************************************************************************************************************
        Host reported a False Control error
        \******************************************************************************************************************/
        DDU32 HostFalseControlError : DD_BITFIELD_BIT(22); //

        /******************************************************************************************************************
        Host reported a LP contention
        \******************************************************************************************************************/
        DDU32 HostContentionDetected : DD_BITFIELD_BIT(23); //

        /******************************************************************************************************************
        Host reported a single-bit ECC
        \******************************************************************************************************************/
        DDU32 HostSingleEccError : DD_BITFIELD_BIT(24); //

        /******************************************************************************************************************
        Host reported a multi-bit ECC error
        \******************************************************************************************************************/
        DDU32 HostMultiEccError : DD_BITFIELD_BIT(25); //

        /******************************************************************************************************************
        Host reported a checksum error
        \******************************************************************************************************************/
        DDU32 HostChecksumError : DD_BITFIELD_BIT(26); //

        /******************************************************************************************************************
        A non-TE trigger has been received from the Periphery. The DSI_CMD_RXCTL will indicate the trigger received.
        \******************************************************************************************************************/
        DDU32 NonTeTriggerReceived : DD_BITFIELD_BIT(27); //

        /******************************************************************************************************************
        A Ultra Low Power State Entry flow has completed
        \******************************************************************************************************************/
        DDU32 UlpsEntryDone : DD_BITFIELD_BIT(28); //

        /******************************************************************************************************************
        A transmit credit has been freed
        \******************************************************************************************************************/
        DDU32 TxData : DD_BITFIELD_BIT(29); //

        /******************************************************************************************************************
        READ response data has been received, or the BTA has been terminated
        \******************************************************************************************************************/
        DDU32 RxDataBtaTerminated : DD_BITFIELD_BIT(30); //

        /******************************************************************************************************************
        A Tear Effect (TE) event was received
        \******************************************************************************************************************/
        DDU32 TeEvent : DD_BITFIELD_BIT(31); //
    };

    DDU32 Value;

} DSI_INTER_IDENT_REG_D11, *PDSI_INTER_IDENT_REG_D11;

C_ASSERT(4 == sizeof(DSI_INTER_IDENT_REG_D11));

#endif // GEN11p5INTRREGS_H
