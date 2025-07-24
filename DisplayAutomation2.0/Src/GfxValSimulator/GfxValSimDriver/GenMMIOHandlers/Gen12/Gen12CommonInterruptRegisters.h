/*===========================================================================
; Gen12InterruptRegisters.h - Gen12 InterruptHandler interface
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
;       This file contains all the InterruptHandler interface function and data structure definitions for GEN12
;--------------------------------------------------------------------------*/

#ifndef __GEN12INTERRUPT_REGS_H__
#define __GEN12INTERRUPT_REGS_H__

#include "..\\..\\CommonInclude\\BitDefs.h"
#include "..\\..\\CommonInclude\\\DisplayDefs.h"

typedef enum _MASTER_INTERRUPT_GEN12
{
    MASTER_INTERRUPT_DISABLE_GEN12 = 0x0,
    MASTER_INTERRUPT_ENABLE_GEN12  = 0x1
} MASTER_INTERRUPT_GEN12;

typedef enum _GFX_MSTR_INTR_INSTANCE_GEN12
{
    GFX_MSTR_INTR_ADDR_GEN12 = 0X190010,
} GFX_MSTR_INTR_INSTANCE_GEN12;

#define GEN12_MASTER_INTERRUPT_BIT_POS (31)
#define GEN12_PCU_INTERRUPT_BIT_POS (30)
#define GEN12_DISPLAY_INTERRUPT_BIT_POS (16)
#define GEN12_DW1_INTERRUPT_BIT_POS (1)
#define GEN12_DW0_INTERRUPT_BIT_POS (0)

/*****************************************************************************
Description:  Top level register that indicates interrupt from hardware.
Bits in this register are set interrupts are pending in the underlying PCU, display or GT interrupts
Bspec: https://gfxspecs.intel.com/Predator/Home/Index/53222
******************************************************************************/
typedef union _GFX_MSTR_INTR_GEN12 {
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
} GFX_MSTR_INTR_GEN12, *PGFX_MSTR_INTR_GEN12;

C_ASSERT(4 == sizeof(GFX_MSTR_INTR_GEN12));

// IMPLICIT ENUMERATIONS USED BY DISPLAY_INT_CTL_GEN12
//
typedef enum _DISPLAY_INTR_GEN12
{
    DISPLAY_INTR_DISABLE_GEN12 = 0x0,
    DISPLAY_INTR_ENABLE_GEN12  = 0x1,
} DISPLAY_INTR_GEN12;

typedef enum _DISPLAY_INTR_CTL_INSTANCE_GEN12
{
    DISPLAY_INTR_CTL_ADDR_GEN12 = 0x44200,
} DISPLAY_INTR_CTL_INSTANCE_GEN12;

typedef enum _DISPLAY_INT_CTL_MASKS_GEN12
{
    DISPLAY_INT_CTL_MASKS_WO_GEN12  = 0x0,
    DISPLAY_INT_CTL_MASKS_MBZ_GEN12 = 0x0,
    DISPLAY_INT_CTL_MASKS_PBC_GEN12 = 0x0,
} DISPLAY_INT_CTL_MASKS_GEN12;

/*****************************************************************************\
This register has the master enable for display interrupts and gives an overview of what interrupts are pending.
An interrupt pending bit will read 1b while one or more interrupts of that category are set (IIR) and enabled (IER).
All Pending Interrupts are ORed together to generate the combined interrupt.
The combined interrupt is ANDed with the Display Interrupt enable to create the display enabled interrupt.
The display enabled interrupt goes to graphics interrupt processing.
The master interrupt enable must be set before any of these interrupts will propagate to graphics interrupt processing.
\*****************************************************************************/
typedef union _DISPLAY_INT_CTL_GEN12 {
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

} DISPLAY_INT_CTL_GEN12, *PDISPLAY_INT_CTL_GEN12;

C_ASSERT(4 == sizeof(DISPLAY_INT_CTL_GEN12));

// IMPLICIT ENUMERATIONS USED BY DE_PORT_INTR_DEFINITION_GEN12
//
typedef enum _DE_PORT_INTR_INSTANCE_GEN12
{
    DE_PORT_INTR_ADDR_GEN12 = 0x44440,
} DE_PORT_INTR_INSTANCE_GEN12;

typedef enum _DE_PORT_INTR_GEN12
{
    DE_PORT_INTR_WO_GEN12  = 0x0,
    DE_PORT_INTR_MBZ_GEN12 = 0x0,
    DE_PORT_INTR_PBC_GEN12 = 0x0,
} DE_PORT_INTR_GEN12;

typedef enum _NORTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_INSTANCE_GEN12
{
    NDE_ISR_ADDR_GEN12 = 0x44470,
    NDE_IMR_ADDR_GEN12 = 0x44474,
    NDE_IIR_ADDR_GEN12 = 0x44478,
    NDE_IER_ADDR_GEN12 = 0x4447C,
} NORTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_INSTANCE_GEN12;

typedef enum _DE_HPD_INTR_GEN12
{
    DE_HPD_INTR_WO_GEN12  = 0x0,
    DE_HPD_INTR_MBZ_GEN12 = 0x0,
    DE_HPD_INTR_PBC_GEN12 = 0x0,
} DE_HPD_INTR_GEN12;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine HPD Interrupt registers.
0x44470 = ISR
0x44474 = IMR
0x44478 = IIR
0x4447C = IER
\*****************************************************************************/
typedef union _DE_HPD_INTR_DEFINITION_GEN12 {
    struct
    {

        /*****************************************************************************\
        The ISR gives the live state of the HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        SIZE32BITS Tbt1Hotplug : BITFIELD_BIT(0);
        SIZE32BITS Tbt2Hotplug : BITFIELD_BIT(1);
        SIZE32BITS Tbt3Hotplug : BITFIELD_BIT(2);
        SIZE32BITS Tbt4Hotplug : BITFIELD_BIT(3);
        SIZE32BITS Tbt5Hotplug : BITFIELD_BIT(4);
        SIZE32BITS Tbt6Hotplug : BITFIELD_BIT(5);
        SIZE32BITS Tbt7Hotplug : BITFIELD_BIT(6);
        SIZE32BITS Tbt8Hotplug : BITFIELD_BIT(7);
        SIZE32BITS Unused8 : BITFIELD_BIT(8);
        SIZE32BITS Unused9 : BITFIELD_BIT(9);
        SIZE32BITS Unused10 : BITFIELD_BIT(10);
        SIZE32BITS Unused11 : BITFIELD_BIT(11);
        SIZE32BITS Unused12 : BITFIELD_BIT(12);
        SIZE32BITS Unused13 : BITFIELD_BIT(13);
        SIZE32BITS Unused14 : BITFIELD_BIT(14);
        SIZE32BITS Unused15 : BITFIELD_BIT(15);
        SIZE32BITS Tc1Hotplug : BITFIELD_BIT(16);
        SIZE32BITS Tc2Hotplug : BITFIELD_BIT(17);
        SIZE32BITS Tc3Hotplug : BITFIELD_BIT(18);
        SIZE32BITS Tc4Hotplug : BITFIELD_BIT(19);
        SIZE32BITS Tc5Hotplug : BITFIELD_BIT(20);
        SIZE32BITS Tc6Hotplug : BITFIELD_BIT(21);
        SIZE32BITS Tc7Hotplug : BITFIELD_BIT(22);
        SIZE32BITS Tc8Hotplug : BITFIELD_BIT(23);
        SIZE32BITS Unused24 : BITFIELD_BIT(24);
        SIZE32BITS Unused25 : BITFIELD_BIT(25);
        SIZE32BITS Unused26 : BITFIELD_BIT(26);
        SIZE32BITS Unused27 : BITFIELD_BIT(27);
        SIZE32BITS Unused28 : BITFIELD_BIT(28);
        SIZE32BITS Unused29 : BITFIELD_BIT(29);
        SIZE32BITS Unused30 : BITFIELD_BIT(30);
        SIZE32BITS Unused31 : BITFIELD_BIT(31);
    };
    SIZE32BITS ulValue;

} DE_HPD_INTR_DEFINITION_GEN12, *PDE_HPD_INTR_DEFINITION_GEN12;

C_ASSERT(4 == sizeof(DE_HPD_INTR_DEFINITION_GEN12));

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

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_DDI_GEN12
//
typedef enum _DDIA_HPD_STATUS_GEN12
{
    DDIA_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    DDIA_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    DDIA_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    DDIA_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} DDIA_HPD_STATUS_GEN12;

typedef enum _DDIA_HPD_OUTPUT_DATA_GEN12
{
    DDIA_HPD_OUTPUT_DATA_DRIVE_0_GEN12 = 0x0,
    DDIA_HPD_OUTPUT_DATA_DRIVE_1_GEN12 = 0x1,
} DDIA_HPD_OUTPUT_DATA_GEN12;

typedef enum _DDIA_HPD_ENABLE_GEN12
{
    DDIA_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    DDIA_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} DDIA_HPD_ENABLE_GEN12;

typedef enum _DDIB_HPD_STATUS_GEN12
{
    DDIB_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    DDIB_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    DDIB_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    DDIB_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} DDIB_HPD_STATUS_GEN12;

typedef enum _DDIB_HPD_OUTPUT_DATA_GEN12
{
    DDIB_HPD_OUTPUT_DATA_DRIVE_0_GEN12 = 0x0,
    DDIB_HPD_OUTPUT_DATA_DRIVE_1_GEN12 = 0x1,
} DDIB_HPD_OUTPUT_DATA_GEN12;

typedef enum _DDIB_HPD_ENABLE_GEN12
{
    DDIB_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    DDIB_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} DDIB_HPD_ENABLE_GEN12;

typedef enum _DDIC_HPD_STATUS_GEN12
{
    DDIC_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    DDIC_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    DDIC_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    DDIC_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} DDIC_HPD_STATUS_GEN12;

typedef enum _DDIC_HPD_OUTPUT_DATA_GEN12
{
    DDIC_HPD_OUTPUT_DATA_DRIVE_0_GEN12 = 0x0,
    DDIC_HPD_OUTPUT_DATA_DRIVE_1_GEN12 = 0x1,
} DDIC_HPD_OUTPUT_DATA_GEN12;

typedef enum _DDIC_HPD_ENABLE_GEN12
{
    DDIC_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    DDIC_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} DDIC_HPD_ENABLE_GEN12;

typedef enum _SOUTH_HOT_PLUG_CTL_FOR_DDI_INSTANCE_GEN12
{
    SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 = 0xC4030,
} SOUTH_HOT_PLUG_CTL_FOR_DDI_INSTANCE_GEN12;

typedef enum _SHOTPLUG_CTL_DDI_MASKS_GEN12
{
    SHOTPLUG_CTL_DDI_MASKS_MBZ_GEN12 = 0xFFFFF000,
    SHOTPLUG_CTL_DDI_MASKS_WO_GEN12  = 0x0,
    SHOTPLUG_CTL_DDI_MASKS_PBC_GEN12 = 0x0,
} SHOTPLUG_CTL_DDI_MASKS_GEN12;

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
typedef union _SHOTPLUG_CTL_DDI_GEN12 {
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

} SHOTPLUG_CTL_DDI_GEN12, *PSHOTPLUG_CTL_DDI_GEN12;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_DDI_GEN12));

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_TC_GEN12
//
typedef enum _TC1_HPD_STATUS_GEN12
{
    TC1_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    TC1_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    TC1_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    TC1_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} TC1_HPD_STATUS_GEN12;

typedef enum _TC1_HPD_OUTPUT_DATA_GEN12
{
    TC1_HPD_OUTPUT_DATA_DRIVE_0_GEN12 = 0x0,
    TC1_HPD_OUTPUT_DATA_DRIVE_1_GEN12 = 0x1,
} TC1_HPD_OUTPUT_DATA_GEN12;

typedef enum _TC1_HPD_ENABLE_GEN12
{
    TC1_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    TC1_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} TC1_HPD_ENABLE_GEN12;

typedef enum _TC2_HPD_STATUS_GEN12
{
    TC2_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    TC2_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    TC2_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    TC2_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} TC2_HPD_STATUS_GEN12;

typedef enum _TC2_HPD_OUTPUT_DATA_GEN12
{
    TC2_HPD_OUTPUT_DATA_DRIVE_0_GEN12 = 0x0,
    TC2_HPD_OUTPUT_DATA_DRIVE_1_GEN12 = 0x1,
} TC2_HPD_OUTPUT_DATA_GEN12;

typedef enum _TC2_HPD_ENABLE_GEN12
{
    TC2_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    TC2_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} TC2_HPD_ENABLE_GEN12;

typedef enum _TC3_HPD_STATUS_GEN12
{
    TC3_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    TC3_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    TC3_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    TC3_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} TC3_HPD_STATUS_GEN12;

typedef enum _TC3_HPD_OUTPUT_DATA_GEN12
{
    TC3_HPD_OUTPUT_DATA_DRIVE_0_GEN12 = 0x0,
    TC3_HPD_OUTPUT_DATA_DRIVE_1_GEN12 = 0x1,
} TC3_HPD_OUTPUT_DATA_GEN12;

typedef enum _TC3_HPD_ENABLE_GEN12
{
    TC3_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    TC3_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} TC3_HPD_ENABLE_GEN12;

typedef enum _TC4_HPD_STATUS_GEN12
{
    TC4_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    TC4_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    TC4_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    TC4_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} TC4_HPD_STATUS_GEN12;

typedef enum _TC4_HPD_OUTPUT_DATA_GEN12
{
    TC4_HPD_OUTPUT_DATA_DRIVE_0_GEN12 = 0x0,
    TC4_HPD_OUTPUT_DATA_DRIVE_1_GEN12 = 0x1,
} TC4_HPD_OUTPUT_DATA_GEN12;

typedef enum _TC4_HPD_ENABLE_GEN12
{
    TC4_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    TC4_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} TC4_HPD_ENABLE_GEN12;

typedef enum _TC5_HPD_STATUS_GEN12
{
    TC5_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    TC5_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    TC5_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    TC5_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} TC5_HPD_STATUS_GEN12;

typedef enum _TC5_HPD_OUTPUT_DATA_GEN12
{
    TC5_HPD_OUTPUT_DATA_DRIVE_0_GEN12 = 0x0,
    TC5_HPD_OUTPUT_DATA_DRIVE_1_GEN12 = 0x1,
} TC5_HPD_OUTPUT_DATA_GEN12;

typedef enum _TC5_HPD_ENABLE_GEN12
{
    TC5_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    TC5_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} TC5_HPD_ENABLE_GEN12;

typedef enum _TC6_HPD_STATUS_GEN12
{
    TC6_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    TC6_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    TC6_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    TC6_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} TC6_HPD_STATUS_GEN12;

typedef enum _TC6_HPD_OUTPUT_DATA_GEN12
{
    TC6_HPD_OUTPUT_DATA_DRIVE_0_GEN12 = 0x0,
    TC6_HPD_OUTPUT_DATA_DRIVE_1_GEN12 = 0x1,
} TC6_HPD_OUTPUT_DATA_GEN12;

typedef enum _TC6_HPD_ENABLE_GEN12
{
    TC6_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    TC6_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} TC6_HPD_ENABLE_GEN12;

typedef enum _SOUTH_HOT_PLUG_CTL_FOR_TYPEC_INSTANCE_GEN12
{
    SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN12 = 0xC4034,
} SOUTH_HOT_PLUG_CTL_FOR_TYPEC_INSTANCE_GEN12;

typedef enum _SHOTPLUG_CTL_TC_MASKS_GEN12
{
    SHOTPLUG_CTL_TC_MASKS_MBZ_GEN12 = 0xFF000000,
    SHOTPLUG_CTL_TC_MASKS_WO_GEN12  = 0x0,
    SHOTPLUG_CTL_TC_MASKS_PBC_GEN12 = 0x0,
} SHOTPLUG_CTL_TC_MASKS_GEN12;

/*****************************************************************************\
The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port, one of the status bits will set and
the hotplug IIR will be set (if unmasked in the IMR).  The status bits are sticky bits, cleared by writing 1s to the bits.Each HPD pin can be configured as an input or output.  The
HPD status function will only work when the pin is configured as an input.  The HPD Output Data function will only work when the HPD pin is configured as an output.The short pulse
duration is programmed in SHPD_PULSE_CNT.
\*****************************************************************************/
typedef union _SHOTPLUG_CTL_TC_GEN12 {
    struct
    {
        SIZE32BITS Tc1HpdStatus : BITFIELD_RANGE(0, 1);
        SIZE32BITS Tc1HpdOutputData : BITFIELD_BIT(2);
        SIZE32BITS Tc1HpdEnable : BITFIELD_BIT(3);
        SIZE32BITS Tc2HpdStatus : BITFIELD_RANGE(4, 5);
        SIZE32BITS Tc2HpdOutputData : BITFIELD_BIT(6);
        SIZE32BITS Tc2HpdEnable : BITFIELD_BIT(7);
        SIZE32BITS Tc3HpdStatus : BITFIELD_RANGE(8, 9);
        SIZE32BITS Tc3HpdOutputData : BITFIELD_BIT(10);
        SIZE32BITS Tc3HpdEnable : BITFIELD_BIT(11);
        SIZE32BITS Tc4HpdStatus : BITFIELD_RANGE(12, 13);
        SIZE32BITS Tc4HpdOutputData : BITFIELD_BIT(14);
        SIZE32BITS Tc4HpdEnable : BITFIELD_BIT(15);
        SIZE32BITS Tc5HpdStatus : BITFIELD_RANGE(16, 17);
        SIZE32BITS Tc5HpdOutputData : BITFIELD_BIT(18);
        SIZE32BITS Tc5HpdEnable : BITFIELD_BIT(19);
        SIZE32BITS Tc6HpdStatus : BITFIELD_RANGE(20, 21);
        SIZE32BITS Tc6HpdOutputData : BITFIELD_BIT(22);
        SIZE32BITS Tc6HpdEnable : BITFIELD_BIT(23);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(24, 31);
    };
    SIZE32BITS ulValue;

} SHOTPLUG_CTL_TC_GEN12, *PSHOTPLUG_CTL_TC_GEN12;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_TC_GEN12));

typedef enum _SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_INSTANCE_GEN12
{
    SDE_ISR_ADDR_GEN12 = 0xC4000,
    SDE_IMR_ADDR_GEN12 = 0xC4004,
    SDE_IIR_ADDR_GEN12 = 0xC4008,
    SDE_IER_ADDR_GEN12 = 0xC400C,
} SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_INSTANCE_GEN12;

typedef enum _SOUTH_DE_INTR_BIT_GEN12
{
    SOUTH_DE_INTR_BIT_MBZ_GEN12 = 0xC078C0F8,
    SOUTH_DE_INTR_BIT_WO_GEN12  = 0x0,
    SOUTH_DE_INTR_BIT_PBC_GEN12 = 0x0,
} SOUTH_DE_INTR_BIT_GEN12;

/*****************************************************************************\
South Display Engine (SDE) interrupt bits come from events within the south display engine.The SDE_IIR bits are ORed together to generate the South/PCH Display Interrupt Event
which will appear in the North Display Engine Interrupt Control Registers.	The South Display Engine Interrupt Control Registers all share the same bit definitions from this table.
\*****************************************************************************/
typedef union _SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 {
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

} SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12, *PSOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12;

C_ASSERT(4 == sizeof(SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12));

// IMPLICIT ENUMERATIONS USED BY HOTPLUG_CTL_GEN12
//
typedef enum _PORT1_HPD_STATUS_GEN12
{
    PORT1_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    PORT1_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    PORT1_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    PORT1_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} PORT1_HPD_STATUS_GEN12;

typedef enum _PORT1_HPD_ENABLE_GEN12
{
    PORT1_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    PORT1_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} PORT1_HPD_ENABLE_GEN12;

typedef enum _PORT2_HPD_STATUS_GEN12
{
    PORT2_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    PORT2_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    PORT2_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    PORT2_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} PORT2_HPD_STATUS_GEN12;

typedef enum _PORT2_HPD_ENABLE_GEN12
{
    PORT2_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    PORT2_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} PORT2_HPD_ENABLE_GEN12;

typedef enum _PORT3_HPD_STATUS_GEN12
{
    PORT3_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    PORT3_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    PORT3_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    PORT3_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} PORT3_HPD_STATUS_GEN12;

typedef enum _PORT3_HPD_ENABLE_GEN12
{
    PORT3_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    PORT3_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} PORT3_HPD_ENABLE_GEN12;

typedef enum _PORT4_HPD_STATUS_GEN12
{
    PORT4_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    PORT4_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    PORT4_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    PORT4_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} PORT4_HPD_STATUS_GEN12;

typedef enum _PORT4_HPD_ENABLE_GEN12
{
    PORT4_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    PORT4_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} PORT4_HPD_ENABLE_GEN12;

typedef enum _PORT5_HPD_STATUS_GEN12
{
    PORT5_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    PORT5_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    PORT5_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    PORT5_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} PORT5_HPD_STATUS_GEN12;

typedef enum _PORT5_HPD_ENABLE_GEN12
{
    PORT5_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    PORT5_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} PORT5_HPD_ENABLE_GEN12;

typedef enum _PORT6_HPD_STATUS_GEN12
{
    PORT6_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    PORT6_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    PORT6_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    PORT6_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} PORT6_HPD_STATUS_GEN12;

typedef enum _PORT6_HPD_ENABLE_GEN12
{
    PORT6_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    PORT6_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} PORT6_HPD_ENABLE_GEN12;

typedef enum _PORT7_HPD_STATUS_GEN12
{
    PORT7_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    PORT7_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    PORT7_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    PORT7_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} PORT7_HPD_STATUS_GEN12;

typedef enum _PORT7_HPD_ENABLE_GEN12
{
    PORT7_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    PORT7_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} PORT7_HPD_ENABLE_GEN12;

typedef enum _PORT8_HPD_STATUS_GEN12
{
    PORT8_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_GEN12    = 0x0,
    PORT8_HPD_STATUS_SHORT_PULSE_DETECTED_GEN12           = 0x1,
    PORT8_HPD_STATUS_LONG_PULSE_DETECTED_GEN12            = 0x2,
    PORT8_HPD_STATUS_SHORT_AND_LONG_PULSES_DETECTED_GEN12 = 0x3,
} PORT8_HPD_STATUS_GEN12;

typedef enum _PORT8_HPD_ENABLE_GEN12
{
    PORT8_HPD_ENABLE_DISABLE_GEN12 = 0x0,
    PORT8_HPD_ENABLE_ENABLE_GEN12  = 0x1,
} PORT8_HPD_ENABLE_GEN12;

typedef enum _THUNDERBOLT_HOT_PLUG_CTL_INSTANCE_GEN12
{
    THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN12 = 0x44030,
} THUNDERBOLT_HOT_PLUG_CTL_INSTANCE_GEN12;

typedef enum _TYPE_C_HOT_PLUG_CTL_INSTANCE_GEN12
{
    TYPE_C_HOT_PLUG_CTL_ADDR_GEN12 = 0x44038,
} TYPE_C_HOT_PLUG_CTL_INSTANCE_GEN12;

typedef enum _HOTPLUG_CTL_MASKS_GEN12
{
    HOTPLUG_CTL_MASKS_WO_GEN12  = 0x0,
    HOTPLUG_CTL_MASKS_MBZ_GEN12 = 0x0,
    HOTPLUG_CTL_MASKS_PBC_GEN12 = 0x0,
} HOTPLUG_CTL_MASKS_GEN12;

typedef union _HOTPLUG_CTL_GEN12 {
    struct
    {
        SIZE32BITS Port1HpdStatus : BITFIELD_RANGE(0, 1);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(2);
        SIZE32BITS Port1HpdEnable : BITFIELD_BIT(3);
        SIZE32BITS Port2HpdStatus : BITFIELD_RANGE(4, 5);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(6);
        SIZE32BITS Port2HpdEnable : BITFIELD_BIT(7);
        SIZE32BITS Port3HpdStatus : BITFIELD_RANGE(8, 9);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(10);
        SIZE32BITS Port3HpdEnable : BITFIELD_BIT(11);
        SIZE32BITS Port4HpdStatus : BITFIELD_RANGE(12, 13);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(14);
        SIZE32BITS Port4HpdEnable : BITFIELD_BIT(15);
        SIZE32BITS Port5HpdStatus : BITFIELD_RANGE(16, 17);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(18);
        SIZE32BITS Port5HpdEnable : BITFIELD_BIT(19);
        SIZE32BITS Port6HpdStatus : BITFIELD_RANGE(20, 21);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(22);
        SIZE32BITS Port6HpdEnable : BITFIELD_BIT(23);
        SIZE32BITS Port7HpdStatus : BITFIELD_RANGE(24, 25);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(26);
        SIZE32BITS Port7HpdEnable : BITFIELD_BIT(27);
        SIZE32BITS Port8HpdStatus : BITFIELD_RANGE(28, 29);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(30);
        SIZE32BITS Port8HpdEnable : BITFIELD_BIT(31);
    };
    SIZE32BITS ulValue;

} HOTPLUG_CTL_GEN12, *PHOTPLUG_CTL_GEN12;

C_ASSERT(4 == sizeof(HOTPLUG_CTL_GEN12));

typedef enum _PORT_TX_DFLEXDPPMS_INSTANCE_GEN12
{
    PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 = 0x163890,
    PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12 = 0x16E890,
    PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12 = 0x16F890,
} PORT_TX_DFLEXDPPMS_INSTANCE_GEN12;

/*****************************************************************************
Description:  PD FW writes  1  to this register's bit to tell DP Driver that it had put the FIA and PHY into DP PHY Mode and it s safe now for DP Driver to proceed to bring up the
DP Controller. Once DP Driver poll a value  1  in this register, DP Driver write  0  to clear this bit for PD FW to use it in the next round.

******************************************************************************/
typedef union _PORT_TX_DFLEXDPPMS_GEN12 {
    struct
    {
        /******************************************************************************************************************
        PD FW writes  1  to this bit to tell DP Driver that it had put the FIA and PHY into DP PHY Mode
        and it s safe now for DP Driver to proceed to bring up the DP Controller. Once DP Driver poll a value  1
        in this register, DP Driver write  0  to clear this bit for PD FW to use it in the next round.
        Similar to register DFLEXDPPMS.DPPMSTC0 but this register is for Type-C Connector
        \******************************************************************************************************************/
        DDU32 DisplayPortPhyModeStatusForTypeCConnector0 : DD_BITFIELD_BIT(0);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector1 : DD_BITFIELD_BIT(1);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector2 : DD_BITFIELD_BIT(2);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector3 : DD_BITFIELD_BIT(3);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector4 : DD_BITFIELD_BIT(4);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector5 : DD_BITFIELD_BIT(5);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector6 : DD_BITFIELD_BIT(6);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector7 : DD_BITFIELD_BIT(7);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector8 : DD_BITFIELD_BIT(8);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector9 : DD_BITFIELD_BIT(9);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector10 : DD_BITFIELD_BIT(10);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector11 : DD_BITFIELD_BIT(11);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector12 : DD_BITFIELD_BIT(12);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector13 : DD_BITFIELD_BIT(13);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector14 : DD_BITFIELD_BIT(14);
        DDU32 DisplayPortPhyModeStatusForTypeCConnector15 : DD_BITFIELD_BIT(15);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(16, 31); // RESERVED
    };

    DDU32 ulValue;
} PORT_TX_DFLEXDPPMS_GEN12;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXDPPMS_GEN12));

typedef enum _PORT_TX_LANES_ALLOCATED_D12
{
    D12_PHY_TX0_ALONE       = 0x1,
    D12_PHY_TX1_ALONE       = 0x2,
    D12_PHY_TX1_TX0         = 0x3,
    D12_PHY_TX2_ALONE       = 0x4,
    D12_PHY_TX3_ALONE       = 0x8,
    D12_PHY_TX3_TX2         = 0xC,
    D12_PHY_TX3_TX2_TX1_TX0 = 0xF,
} PORT_TX_LANES_ALLOCATED_D12;

typedef enum _PORT_TX_DFLEXDPSP_INSTANCE_GEN12
{
    PORT_TX_DFLEXDPSP1_FIA1_ADDR_GEN12 = 0x1638A0,
    PORT_TX_DFLEXDPSP2_FIA1_ADDR_GEN12 = 0x1638A4,
    PORT_TX_DFLEXDPSP3_FIA1_ADDR_GEN12 = 0x1638A8,
    PORT_TX_DFLEXDPSP4_FIA1_ADDR_GEN12 = 0x1638AC,
    PORT_TX_DFLEXDPSP1_FIA2_ADDR_GEN12 = 0x16E8A0,
    PORT_TX_DFLEXDPSP2_FIA2_ADDR_GEN12 = 0x16E8A4,
    PORT_TX_DFLEXDPSP3_FIA2_ADDR_GEN12 = 0x16E8A8,
    PORT_TX_DFLEXDPSP4_FIA2_ADDR_GEN12 = 0x16E8AC,
    PORT_TX_DFLEXDPSP1_FIA3_ADDR_GEN12 = 0x16F8A0,
    PORT_TX_DFLEXDPSP2_FIA3_ADDR_GEN12 = 0x16F8A4,
    PORT_TX_DFLEXDPSP3_FIA3_ADDR_GEN12 = 0x16F8A8,
    PORT_TX_DFLEXDPSP4_FIA3_ADDR_GEN12 = 0x16F8AC,
} PORT_TX_DFLEXDPSP_INSTANCE_GEN12;

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
typedef union _PORT_TX_DFLEXDPSP_GEN12 {
    struct
    {
        /******************************************************************************************************************
        DPX4TXLATC0
        4 bits correspond to 4 TX, i.e. TX[3:0] Lane in PHY.
        Lower 2 bits correspond to the 2 lower TX lane on the PHY lane of Type-C connector 0.
        Upper 2 bits correspond to the upper 2 TX lane on the PHY of Type-C connector 0.
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
        This bit is set by IOM FW and read by Display Driver. It tells the Display Driver if Modular FIA is used in the SOC.
        If Modular FIA is used in the SOC, then Display Driver will access the additional instances of FIA based on pre-assigned offset in GTTMADDR space.
        Each Modular FIA instance has its own IOSF Sideband Port ID and it houses only 2 Type-C Port. Hence in SOC that have more than two Type-C Ports and hence multiple instances
        of Modular FIA, Gunit will need to use different destination ID when it access different pair of Type-C Port. If Modular FIA is not used in the SOC, then a single
        monolithic FIA is used to house all the Type-C Ports which has only one IOSF Sideband Port ID. If Modular FIA is used in the SOC, this register bit MF exist in all the
        instances of Modular FIA. IOM FW is required to program only the MF bit in first FIA instance that house the Type-C Port 0 and Port 1, for Display Driver to read from.
        \******************************************************************************************************************/
        DDU32 ModularFia_Mf : DD_BITFIELD_BIT(4); // MODULAR_FIA_MF
        DDU32 Tc0LiveState : DD_BITFIELD_BIT(5);
        DDU32 Tbt0LiveState : DD_BITFIELD_BIT(6);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(7);
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector1 : DD_BITFIELD_RANGE(8, 11); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(12);
        DDU32 Tc1LiveState : DD_BITFIELD_BIT(13);
        DDU32 Tbt1LiveState : DD_BITFIELD_BIT(14);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(15); // RESERVED
        /*Same definition as DFLEXDPSP1.DPX4TXLATC0, but this register is for Type-C Connector 2.*/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector2 : DD_BITFIELD_RANGE(16, 19); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(20);
        DDU32 Tc2LiveState : DD_BITFIELD_BIT(21);
        DDU32 Tbt2LiveState : DD_BITFIELD_BIT(22);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(23); // RESERVED
        /*Same definition as DFLEXDPSP1.DPX4TXLATC0, but this register is for Type-C Connector 3.*/
        DDU32 DisplayPortX4TxLaneAssignmentForTypeCConnector3 : DD_BITFIELD_RANGE(24, 27); // DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(28);
        DDU32 Tc3LiveState : DD_BITFIELD_BIT(29);
        DDU32 Tbt3LiveState : DD_BITFIELD_BIT(30);
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(31); // RESERVED
    };

    DDU32 ulValue;

} PORT_TX_DFLEXDPSP_GEN12;

typedef enum _DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_ENUM_D12
{
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_NO_PIN_ASSIGNMENT_FOR_NON_TYPEC_DP_D12 = 0x0,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_A_D12                   = 0x1,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_B_D12                   = 0x2,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C_D12                   = 0x3,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_D_D12                   = 0x4,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_E_D12                   = 0x5,
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_F_D12                   = 0x6,

} DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_ENUM_D12;

typedef enum _PORT_TX_DFLEXPA1_INSTANCE_D12
{
    PORT_TX_DFLEXPA1_FIA1_ADDR_D12 = 0x163880,
    PORT_TX_DFLEXPA1_FIA2_ADDR_D12 = 0x16E880,
    PORT_TX_DFLEXPA1_FIA3_ADDR_D12 = 0x16F880,
} PORT_TX_DFLEXPA1_INSTANCE_D12;

/*****************************************************************************
Description:  FIA has per Connector register to govern the Pin Assignment of each Type-C Connector. For example, DFLEXPA1.DPPATC0 is used to govern the Pin Assignment of Type-C
Connector 0. The Type-C Connector number (e.g. "0" in register DPPATC0) is logical number.

******************************************************************************/
typedef union _PORT_TX_DFLEXPA1_D12 {
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

} PORT_TX_DFLEXPA1_D12;

C_ASSERT(4 == sizeof(PORT_TX_DFLEXPA1_D12));

#endif // GEN12INTRREGS_H
