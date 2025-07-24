/*===========================================================================
; SKLInterruptRegs.h
;----------------------------------------------------------------------------
;   Copyright (c) 2004-2005  Intel Corporation.
;   All Rights Reserved.  Copyright notice does not imply publication.
;   This software is protected as an unpublished work.  This software
;   contains the valuable trade secrets of Intel Corporation, and must
;   and must be maintained in confidence.
;
; File Description:
;   This file defines hotplug enable/status registers for SKL and Later..
;
;--------------------------------------------------------------------------*/

#ifndef SKLINTRREGS_H
#define SKLINTRREGS_H

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\CommonInclude\\BitDefs.h"
#include "..\\CommonInclude\\\DisplayDefs.h"
//**********************************************
//
// Register definitions
//
//**********************************************

#define MASTER_INTR_CTL_SKL 0x44200

#define SKL_DE_PIPEA_IMR 0x44404
#define SKL_DE_PIPEA_IIR 0x44408
#define SKL_DE_PIPEA_IER 0x4440C

#define SKL_DE_PIPEA_PRESERVE_BITS (BIT30 | BITRANGE(27, 19) | BITRANGE(15, 13) | BIT11 | BIT3)
#define SKL_DE_PIPEA_WZ_BITS (0)

#define SKL_DE_PIPEB_IMR 0x44414
#define SKL_DE_PIPEB_IIR 0x44418
#define SKL_DE_PIPEB_IER 0x4441C

#define SKL_PIPEB_PRESERVE_BITS (BIT30 | BITRANGE(27, 19) | BITRANGE(15, 13) | BIT11 | BIT3)
#define SKL_DE_PIPEB_WZ_BITS (0)

#define SKL_DE_PIPEC_IMR 0x44424
#define SKL_DE_PIPEC_IIR 0x44428
#define SKL_DE_PIPEC_IER 0x4442C

#define SKL_DE_PIPEC_PRESERVE_BITS (BIT30 | BITRANGE(27, 19) | BITRANGE(15, 13) | BIT11 | BIT3)
#define SKL_DE_PIPEC_WZ_BITS (0)

#define PIPE_UNDER_RUN_SCRATCHPAD_OFFSET 0x4f08c

typedef union _SKL_MSTR_INTR_TABLE {
    DDU32 Value;
    struct
    {
        DDU32 RenderInterruptsPending : 1;  // bit 0
        DDU32 BlitterInterruptsPending : 1; // bit 1
        DDU32 VCS1InterruptsPending : 1;    // bit 2
        DDU32 VCS2InterruptsPending : 1;    // bit 3
        DDU32 GTPMInterruptsPending : 1;    // bit 4
        DDU32 GuCInterruptsPending : 1;     // bit 5
        DDU32 VEBoxInterruptsPending : 1;   // bit 6
        DDU32 WDBoxInterruptsPending : 1;   // bit 7

        DDU32 UNIQUENAME(Reserved) : 8; // bit 8-15

        DDU32 DEPipeAInterruptsPending : 1; // bit 16
        DDU32 DEPipeBInterruptsPending : 1; // bit 17
        DDU32 DEPipeCInterruptsPending : 1; // bit 18

        DDU32 UNIQUENAME(Reserved) : 1; // bit 19

        DDU32 DEPortInterruptsPending : 1; // bit 20

        DDU32 UNIQUENAME(Reserved) : 1; // bit 21

        DDU32 DEMiscInterruptsPending : 1; // bit 22
        DDU32 DEPCHInterruptsPending : 1;  // bit 23

        DDU32 DEAudioCodecInterruptsPending : 1; // bit 24

        DDU32 UNIQUENAME(Reserved) : 5; // bit 25-29

        DDU32 PCUInterruptsPending : 1; // bit 30
        DDU32 MstrInterruptEnable : 1;  // bit 31
    };
} SKL_MSTR_INTR_TABLE, *PSKL_MSTR_INTR_TABLE;

typedef union _PIPE_UNDERRUN_SCRATCHPAD_REG {
    struct
    {
        DDU32 PipeAUnderRun : 1;                            // Bit 0
        DDU32 PipeBUnderRun : 1;                            // Bit 1
        DDU32 PipeCUnderRun : 1;                            // Bit 2
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(3, 31); // Bit 3 - 31
    };
    DDU32 ulValue;
} PIPE_UNDERRUN_SCRATCHPAD_REG;

typedef union _SKL_DE_PIPE_INTERRUPT_TABLE {
    DDU32 ulValue;
    struct
    {
        DDU32 bPipeVblank : BITFIELD_BIT(0);
        DDU32 bPipeVsync : BITFIELD_BIT(1);
        DDU32 bPipeScanLineEvent : BITFIELD_BIT(2);
        DDU32 bPlane1FlipDone : BITFIELD_BIT(3);
        DDU32 bPlane2FlipDone : BITFIELD_BIT(4);
        DDU32 bPlane3FlipDone : BITFIELD_BIT(5);
        DDU32 bPlane4FlipDone : BITFIELD_BIT(6); // BXT
        DDU32 bPlane1GTTFaultStatus : BITFIELD_BIT(7);
        DDU32 bPlane2GTTFaultStatus : BITFIELD_BIT(8);
        DDU32 bPlane3GTTFaultStatus : BITFIELD_BIT(9);
        DDU32 bPlane4GttFaultStatus : BITFIELD_BIT(10); // BXT
        DDU32 bCursorGTTFaultStatus : BITFIELD_BIT(11);
        DDU32 bDPSTHistogramEvent : BITFIELD_BIT(12);
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(13, 15);
        DDU32 bPlane1FlipQueueEmpty : BITFIELD_BIT(16);
        DDU32 bPlane2FlipQueueEmpty : BITFIELD_BIT(17);
        DDU32 bPlane3FlipQueueEmpty : BITFIELD_BIT(18);
        DDU32 bPlane4FlipQueueEmpty : BITFIELD_BIT(19); // BXT
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(20, 27);
        DDU32 bCDClkCrcDone : BITFIELD_BIT(28);
        DDU32 bCDClkCrcError : BITFIELD_BIT(29);
        DDU32 UNIQUENAME(Reserved) : BITFIELD_BIT(30);
        DDU32 bUnderRun : BITFIELD_BIT(31);
    };
} SKL_DE_PIPE_INTERRUPT_TABLE;

#define SKL_GT_REN_IMR_PRESERVE_BITS (BITRANGE(31, 15) | BITRANGE(13, 12) | BIT5 | BIT2)
#define SKL_GT_VID_IMR_PRESERVE_BITS (BITRANGE(31, 12) | BIT10 | BIT7 | BITRANGE(2, 1))
#define SKL_GT_BLT_IMR_PRESERVE_BITS (BITRANGE(31, 28) | BITRANGE(26, 25) | BIT23 | BIT21 | BITRANGE(18, 17) | BITRANGE(15, 0))
#define SKL_GT_VECS_IMR_PRESERVE_BITS (BITRANGE(31, 12) | BITRANGE(10, 9) | BIT7 | BIT5 | BIT2 | BIT1)
#define SKL_GT_VID2_IMR_PRESERVE_BITS (BITRANGE(31, 28) | BIT26 | BIT23 | BITRANGE(18, 17) | BITRANGE(15, 0))
#define SKL_GT_OA_IMR_PRESERVE_BITS (BITRANGE(31, 29) | BITRANGE(27, 0))

#define SKL_GT_REN_IMR_VALID (~SKL_GT_REN_IMR_PRESERVE_BITS)
#define SKL_GT_VID_IMR_VALID (~SKL_GT_VID_IMR_PRESERVE_BITS)
#define SKL_GT_BLT_IMR_VALID (~SKL_GT_BLT_IMR_PRESERVE_BITS)
#define SKL_GT_VECS_IMR_VALID (~SKL_GT_VECS_IMR_PRESERVE_BITS)
#define SKL_GT_VID2_IMR_VALID (~SKL_GT_VID2_IMR_PRESERVE_BITS)
#define SKL_GT_OA_IMR_VALID (~SKL_GT_OA_IMR_PRESERVE_BITS)
#define SKL_GT_WZ_BITS (0)

#define SKL_GT0_IMR 0x44304
#define SKL_GT0_IIR 0x44308
#define SKL_GT0_IER 0x4430C

#define SKL_GT0_PRESERVE_BITS (BITRANGE(31, 28) | BITRANGE(26, 25) | BITRANGE(23, 21) | BIT18 | BIT17 | BIT15 | BITRANGE(13, 12) | BIT5 | BIT2)
#define SKL_GT0_WZ_BITS (0)
#define SKL_GT0_IMR_VALID (~SKL_GT0_PRESERVE_BITS)

typedef union _SKL_GT0_INTR_TABLE {
    DDU32 ulValue;
    struct
    {
        // Render Interrupts
        DDU32 bRenderMIUserInterrupt : 1;    // bit 0
        DDU32 bRenderDebugInterrupt : 1;     // bit 1
        DDU32 UNIQUENAME(Reserved) : 1;      // bit 2
        DDU32 bRenderError : 1;              // bit 3
        DDU32 bRenderPipeControlNotify : 1;  // bit 4
        DDU32 UNIQUENAME(Reserved) : 1;      // bit 5
        DDU32 bCSWatchdogCounterExpired : 1; // bit 6
        DDU32 bPageFaultInterrupt : 1;       // bit 7

        DDU32 bRenderContextSwitchInterrupt : 1; // bit 8
        DDU32 bCSTRInvalidTileDetection : 1;     // bit 9
        DDU32 bL3CounterSave : 1;                // bit 10
        DDU32 bRenderWaitOnSemaphore : 1;        // bit 11
        DDU32 UNIQUENAME(Reserved) : 2;          // bit 12 - 13
        DDU32 bRenderTDLRetryInterrupt : 1;      // bit 14 (Restart Interrupt for KBL)
        DDU32 UNIQUENAME(Reserved) : 1;          // bit 15

        // Blitter Interrupts
        DDU32 bBlitterCommandParserUserInterrupt : 1; // bit 16
        DDU32 UNIQUENAME(Reserved) : 1;               // bit 17
        DDU32 UNIQUENAME(Reserved) : 1;               // bit 18
        DDU32 bBlitterCommandPasrserMasterError : 1;  // bit 19
        DDU32 bBlitterMIFlushDWNotify : 1;            // bit 20
        DDU32 UNIQUENAME(Reserved) : 3;               // bit 21 - 23

        DDU32 bBlitterASContextSwitchInterrupt : 1; // bit 24
        DDU32 UNIQUENAME(Reserved) : 2;             // bit 25 - 26
        DDU32 bBlitterWaitOnSemaphore : 1;          // bit 27
        DDU32 UNIQUENAME(Reserved) : 4;             // bit 28-31
    };
} SKL_GT0_INTR_TABLE;

#define SKL_GT1_IMR 0x44314
#define SKL_GT1_IIR 0x44318
#define SKL_GT1_IER 0x4431C

#define SKL_GT1_PRESERVE_BITS (BITRANGE(31, 28) | BIT26 | BIT23 | BIT18 | BIT17 | BITRANGE(15, 12) | BIT10 | BIT7 | BIT2 | BIT1)
#define SKL_GT1_WZ_BITS (0)
#define SKL_GT1_IMR_VALID (~SKL_GT1_PRESERVE_BITS)

typedef union _SKL_GT1_INTR_TABLE {
    DDU32 ulValue;
    struct
    {
        // VCS1 Interrupts
        DDU32 bVCS1UserInterrupt : 1;                     // bit 0
        DDU32 UNIQUENAME(Reserved) : 2;                   // bit 1-2
        DDU32 bVCS1Error : 1;                             // bit 3
        DDU32 bVCS1MIFlushDWNotify : 1;                   // bit 4
        DDU32 bVCS1NotifyPAVPForInlineReadCompletion : 1; // bit 5
        DDU32 bVCS1TimeoutCounterExpired : 1;             // bit 6
        DDU32 UNIQUENAME(Reserved) : 1;                   // bit 7

        DDU32 bVCS1ContextSwitchInterrupt : 1;  // bit 8
        DDU32 bVCS1TerminationonPAVPAttack : 1; // bit 9
        DDU32 UNIQUENAME(Reserved) : 1;         // bit 10
        DDU32 bVCS1WaitOnSemaphore : 1;         // bit 11
        DDU32 UNIQUENAME(Reserved) : 4;         // bit 12 - 15

        // VCS2 Interrupts
        DDU32 bVCS2UserInterrupt : 1;                     // bit 16
        DDU32 UNIQUENAME(Reserved) : 2;                   // bit 17-18
        DDU32 bVCS2Error : 1;                             // bit 19
        DDU32 bVCS2MIFlushDWNotify : 1;                   // bit 20
        DDU32 bVCS2NotifyPAVPForInlineReadCompletion : 1; // bit 21
        DDU32 bVCS2WatchDogCounterExpired : 1;            // bit 22
        DDU32 UNIQUENAME(Reserved) : 1;                   // bit 23

        DDU32 bVCS2ContextSwitchInterrupt : 1;  // bit 24
        DDU32 bVCS2TerminationonPAVPAttack : 1; // bit 25
        DDU32 UNIQUENAME(Reserved) : 1;         // bit 26
        DDU32 bVCS2WaitOnSemaphore : 1;         // bit 27
        DDU32 UNIQUENAME(Reserved) : 4;         // bit 28-31
    };
} SKL_GT1_INTR_TABLE;

#define SKL_GT2_IMR 0x44324
#define SKL_GT2_IIR 0x44328
#define SKL_GT2_IER 0x4432C

#define SKL_GT2_PRESERVE_BITS (BIT15 | BIT14 | BIT3 | BIT0)
#define SKL_GT2_WZ_BITS (0)
#define SKL_GT2_IMR_VALID (~SKL_GT2_PRESERVE_BITS)

typedef union _SKL_GT2_INTR_TABLE {
    DDU32 ulValue;
    struct
    {
        // GTPM Interrupts
        DDU32 UNIQUENAME(Reserved) : 1;                          // bit 0
        DDU32 bGTPMRenderGSVDownEvaluationIntervalInterrupt : 1; // bit 1
        DDU32 bGTPMRenderGSVUpEvaluationIntervalInterrupt : 1;   // bit 2
        DDU32 UNIQUENAME(Reserved) : 1;                          // bit 3
        DDU32 bGTPMRenderDownThresholdInterrupt : 1;             // bit 4
        DDU32 bGTPMRenderUpThresholdInterrupt : 1;               // bit 5
        DDU32 bGTPMRenderFreqDownTimeoutduringRC6 : 1;           // bit 6

        DDU32 UNIQUENAME(Reserved) : 16; // bit 22 - 7

        // GuC Interrupts
        DDU32 bGuCSHIMError : 1; // bit 23

        DDU32 bGuCDMAINTError : 1;          // bit 24
        DDU32 bGuCDMADone : 1;              // bit 25
        DDU32 bGuCDoorBellRang : 1;         // bit 26
        DDU32 bGuCIOMMUSentMsgtoGuc : 1;    // bit 27
        DDU32 bGuCSemaphoreSignaled : 1;    // bit 28
        DDU32 bGuCDisplayEventRecieved : 1; // bit 29
        DDU32 bGuCExecutionError : 1;       // bit 30
        DDU32 bGuCInterruptToHost : 1;      // bit 31
    };
} SKL_GT2_INTR_TABLE;

#define SKL_GT3_IMR 0x44334
#define SKL_GT3_IIR 0x44338
#define SKL_GT3_IER 0x4433C

#define SKL_GT3_PRESERVE_BITS (BITRANGE(31, 29) | BITRANGE(27, 18) | BITRANGE(15, 12) | BITRANGE(10, 9) | BIT7 | BIT5 | BIT2 | BIT1)
#define SKL_GT3_WZ_BITS (0)
#define SKL_GT3_IMR_VALID (~SKL_GT3_PRESERVE_BITS)

typedef union _SKL_GT3_INTR_TABLE {
    DDU32 ulValue;
    struct
    {
        // VECS Interrupts
        DDU32 bVECSMIUserInterrupt : 1;        // bit 0
        DDU32 UNIQUENAME(Reserved) : 1;        // bit 1
        DDU32 bVECSMMIOSyncFlushStatus : 1;    // bit 2
        DDU32 bVECSErrorInterrupt : 1;         // bit 3
        DDU32 bVECSMIFlushDWNotify : 1;        // bit 4
        DDU32 UNIQUENAME(Reserved) : 1;        // bit 5
        DDU32 bVECSWatchDogCounterExpired : 1; // bit 6
        DDU32 UNIQUENAME(Reserved) : 1;        // bit 7
        DDU32 bVECSContextSwitchInterrupt : 1; // bit 8
        DDU32 UNIQUENAME(Reserved) : 2;        // bit 9,10
        DDU32 bVECSWaitOnSemaphore : 1;        // bit 11
        DDU32 UNIQUENAME(Reserved) : 4;        // bit 12 -15

        // WDBox Interrupts
        DDU32 bWDBoxEndofFrameInterrupt : 1; // bit 16
        DDU32 bWDBoxInterrupt : 1;           // bit 17
        DDU32 UNIQUENAME(Reserved) : 10;     // bit 18 - 27

        // OACS Interrupts
        DDU32 bRenderPerfMonBufferHalfFull : 1; // bit 28
        DDU32 UNIQUENAME(Reserved) : 3;         // bit 29 - 31
    };
} SKL_GT3_INTR_TABLE;

#define SKL_DE_PORT_ISR 0x44440
#define SKL_DE_PORT_IMR 0x44444
#define SKL_DE_PORT_IIR 0x44448
#define SKL_DE_PORT_IER 0x4444C

#define SKL_DE_PORT_PRESERVE_BITS (BITRANGE(29, 28) | BITRANGE(24, 6) | BITRANGE(2, 1))
#define SKL_DE_PORT_WZ_BITS (0)

typedef union _SKL_DE_PORT_INTERRUPT_TABLE {
    DDU32 ulValue;
    struct
    {
        DDU32 bAuxChannelA : BITFIELD_BIT(0);                //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(1, 2);   //
        DDU32 bDdiAHotplug : BITFIELD_BIT(3);                //
        DDU32 bDdiBHotplug : BITFIELD_BIT(4);                //
        DDU32 bDdiCHotplug : BITFIELD_BIT(5);                //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(6, 24);  //
        DDU32 bAuxChannelB : BITFIELD_BIT(25);               //
        DDU32 bAuxChannelC : BITFIELD_BIT(26);               //
        DDU32 bAuxChannelD : BITFIELD_BIT(27);               //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(28, 29); //
        DDU32 bMipiA : BITFIELD_BIT(30);                     //
        DDU32 bMipiC : BITFIELD_BIT(31);                     //
    };
} SKL_DE_PORT_INTERRUPT_TABLE;

#define BXT_DE_PORT_PRESERVE_BITS (BITRANGE(29, 28) | BITRANGE(22, 6) | BITRANGE(2, 1))
#define BXT_DE_PORT_WZ_BITS (0)

#define GLK_DE_PORT_PRESERVE_BITS (BITRANGE(29, 28) | BITRANGE(22, 10) | BITRANGE(7, 6) | BITRANGE(2, 1))

#define DDI_HPD_LIVESTATE_MASK (BIT3 | BIT4 | BIT5)
typedef union _BXT_DE_PORT_INTERRUPT_TABLE {
    DDU32 ulValue;
    struct
    {
        DDU32 bAuxChannelA : BITFIELD_BIT(0);                   //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(1, 2);      //
        DDU32 bDdiAHotplug : BITFIELD_BIT(3);                   //
        DDU32 bDdiBHotplug : BITFIELD_BIT(4);                   //
        DDU32 bDdiCHotplug : BITFIELD_BIT(5);                   //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(6, 7);      //
        DDU32 bScdcReadRequestInterruptPortB : BITFIELD_BIT(8); //
        DDU32 bScdcReadRequestInterruptPortC : BITFIELD_BIT(9); //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(10, 22);    //
        DDU32 bMipiATe : BITFIELD_BIT(23);                      //
        DDU32 bMipiCTe : BITFIELD_BIT(24);                      //
        DDU32 bAuxChannelB : BITFIELD_BIT(25);                  //
        DDU32 bAuxChannelC : BITFIELD_BIT(26);                  //
        DDU32 bAuxChannelD : BITFIELD_BIT(27);                  //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(28, 29);    //
        DDU32 bMipiA : BITFIELD_BIT(30);                        //
        DDU32 bMipiC : BITFIELD_BIT(31);                        //
    };
} BXT_DE_PORT_INTERRUPT_TABLE, *PBXT_DE_PORT_INTERRUPT_TABLE;

typedef union _BXT_DE_PORT_INTERRUPT_TABLE_A0 {
    DDU32 ulValue;
    struct
    {
        DDU32 bAuxChannelA : BITFIELD_BIT(0);                //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(1, 2);   //
        DDU32 bDdiBHotplug : BITFIELD_BIT(3);                //
        DDU32 bDdiCHotplug : BITFIELD_BIT(4);                //
        DDU32 bDdiAHotplug : BITFIELD_BIT(5);                //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(6, 22);  //
        DDU32 bMipiATe : BITFIELD_BIT(23);                   //
        DDU32 bMipiCTe : BITFIELD_BIT(24);                   //
        DDU32 bAuxChannelB : BITFIELD_BIT(25);               //
        DDU32 bAuxChannelC : BITFIELD_BIT(26);               //
        DDU32 bAuxChannelD : BITFIELD_BIT(27);               //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(28, 29); //
        DDU32 bMipiA : BITFIELD_BIT(30);                     //
        DDU32 bMipiC : BITFIELD_BIT(31);                     //
    };
} BXT_DE_PORT_INTERRUPT_TABLE_A0, *PBXT_DE_PORT_INTERRUPT_TABLE_A0;

typedef enum _PCU_INTERRUPTS_INSTANCE_BXT
{
    PCU_INTERRUPTS_INSTANCE_ADDRESS_BXT = 0x444E0,
} PCU_INTERRUPTS_INSTANCE_BXT;

#define BXT_PCU_IMR 0x444E4
#define BXT_PCU_IIR 0x444E8
#define BXT_PCU_IER 0x444EC

typedef enum _PCU_INTERRUPT_DEFINITION_MASKS_BXT
{
    PCU_INTERRUPT_DEFINITION_MASKS_WO_BXT  = 0x0,
    PCU_INTERRUPT_DEFINITION_MASKS_MBZ_BXT = 0x0,
    PCU_INTERRUPT_DEFINITION_MASKS_PBC_BXT = 0x0,
} PCU_INTERRUPT_DEFINITION_MASKS_BXT;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the PCU Interrupt registers.
0x444E0 = ISR
0x444E4 = IMR
0x444E8 = IIR
0x444EC = IER
\*****************************************************************************/
typedef union _PCU_INTERRUPT_DEFINITION_BXT {
    struct
    {

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        DDU32 Unused_Int_23_0 : BITFIELD_RANGE(0, 23);           //
        DDU32 Pcu_Thermal_Event : BITFIELD_BIT(24);              //
        DDU32 Pcu_Pcode2driver_Mailbox_Event : BITFIELD_BIT(25); //

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        DDU32 Unused_Int_28_26 : BITFIELD_RANGE(26, 28); //

        /*****************************************************************************\
        This field indicates DDIC hotplug activity was detected during DC9.
        \*****************************************************************************/
        DDU32 DdicDc9Hpd : BITFIELD_BIT(29); //

        /*****************************************************************************\
        This field indicates DDIB hotplug activity was detected during DC9.
        \*****************************************************************************/
        DDU32 DdibDc9Hpd : BITFIELD_BIT(30); //

        /*****************************************************************************\
        This field indicates DDIA hotplug activity was detected during DC9.
        \*****************************************************************************/
        DDU32 DdiaDc9Hpd : BITFIELD_BIT(31); //
    };
    DDU32 ulValue;

} PCU_INTERRUPT_DEFINITION_BXT, *PPCU_INTERRUPT_DEFINITION_BXT;

C_ASSERT(4 == sizeof(PCU_INTERRUPT_DEFINITION_BXT));

#define SKL_DE_MISC_IMR 0x44464
#define SKL_DE_MISC_IIR 0x44468
#define SKL_DE_MISC_IER 0x4446C

#define SKL_DE_MISC_PRESERVE_BITS (BIT26 | BITRANGE(18, 16) | BITRANGE(14, 0))
#define SKL_DE_MISC_WZ_BITS (0)

typedef union _SKL_DE_MISC_INTERRUPT_TABLE {
    DDU32 ulValue;
    struct
    {
        DDU32 UNIQUENAME(Reserved) : 15;       // bit 14-0
        DDU32 bGTCCombinedEvent : 1;           // bit 15
        DDU32 UNIQUENAME(Reserved) : 3;        // bit 18-16
        DDU32 bSRDCombinedEvent : 1;           // bit 19
        DDU32 bSVMWaitDescriptorCompleted : 1; // bit 20
        DDU32 bSVMVTDFault : 1;                // bit 21
        DDU32 bSVMPRQEvent : 1;                // bit 22
        DDU32 bWDCombinedEvent : 1;            // bit 23
        DDU32 bDMCInterrupt : 1;               // bit 24
        DDU32 bDMCError : 1;                   // bit 25
        DDU32 bCameraInterruptEvent : 1;       // bit 26
        DDU32 bGSEEvent : 1;                   // bit 27
        DDU32 bInvalidPTEData : 1;             // bit 28
        DDU32 bInvalidGTTPTE : 1;              // bit 29
        DDU32 bECCDoubleError : 1;             // bit 30
        DDU32 bPoison : 1;                     // bit 31
    };
} SKL_DE_MISC_INTERRUPT_TABLE;

#define SPT_PCH_ISR 0xC4000ul
#define SPT_PCH_IMR 0xC4004ul
#define SPT_PCH_IIR 0xC4008ul
#define SPT_PCH_IER 0xC400Cul

#define SPT_PCH_PRESERVE_BITS (0)
#define SPT_PCH_WZ_BITS (BITRANGE(16, 0) | BITRANGE(20, 18) | BITRANGE(31, 26))

typedef union _SPT_PCH_INT_TABLE {
    DDU32 ulValue;
    struct
    {
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(0, 16);  // MBZ
        DDU32 bGmbus : BITFIELD_BIT(17);                     //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(18, 20); // MBZ
        DDU32 bDdiBHotplug : BITFIELD_BIT(21);               //
        DDU32 bDdiCHotplug : BITFIELD_BIT(22);               //
        DDU32 bDdiDHotplug : BITFIELD_BIT(23);               //
        DDU32 bDdiAHotplug : BITFIELD_BIT(24);               //
        DDU32 bDdiEHotplug : BITFIELD_BIT(25);               //
        DDU32 bDdiFHotplug : BITFIELD_BIT(26);               //
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(27, 31); // MBZ
    };
} SPT_PCH_INT_TABLE, *PSPT_PCH_INT_TABLE;

// BXT NDE HOT PLUG CTL
#define BXT_HOTPLUG_CTL_REG 0xC4030
#define BXT_HOTPLUG_CTL_WZ_BITS (BIT2 | BITRANGE(7, 5) | BIT10 | BITRANGE(23, 13) | BIT26 | BITRANGE(31, 29))

typedef union _BXT_HOTPLUG_CTL_REG_ST_A {
    UCHAR ucValueA;
    struct
    {
        SIZE8BITS bDdiA_ShortPulseStatus : BITFIELD_BIT(0);
        SIZE8BITS bDdiA_LongPulseStatus : BITFIELD_BIT(1);
        SIZE8BITS UNIQUENAME(Reserved) : BITFIELD_BIT(2);      // MBZ
        SIZE8BITS bDdiAHpdInvert : BITFIELD_BIT(3);            // DDI_B_HPD_INVERT
        SIZE8BITS bDdiAHpdInputEnable : BITFIELD_BIT(4);       // DDI_B_HPD_INPUT_ENABLE
        SIZE8BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(5, 7); // MBZ
    };
} BXT_HOTPLUG_CTL_REG_ST_A;

typedef union _BXT_HOTPLUG_CTL_REG_ST_B {
    UCHAR ucValueB;
    struct
    {
        SIZE8BITS bDdiB_ShortPulseStatus : BITFIELD_BIT(0);
        SIZE8BITS bDdiB_LongPulseStatus : BITFIELD_BIT(1);
        SIZE8BITS UNIQUENAME(Reserved) : BITFIELD_BIT(2);      // MBZ
        SIZE8BITS bDdiBHpdInvert : BITFIELD_BIT(3);            // DDI_B_HPD_INVERT
        SIZE8BITS bDdiBHpdInputEnable : BITFIELD_BIT(4);       // DDI_B_HPD_INPUT_ENABLE
        SIZE8BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(5, 7); // MBZ
    };
} BXT_HOTPLUG_CTL_REG_ST_B;

typedef union _BXT_HOTPLUG_CTL_REG_ST_C {
    UCHAR ucValueC;
    struct
    {
        SIZE8BITS bDdiC_ShortPulseStatus : BITFIELD_BIT(0);
        SIZE8BITS bDdiC_LongPulseStatus : BITFIELD_BIT(1);
        SIZE8BITS UNIQUENAME(Reserved) : BITFIELD_BIT(2);      // MBZ
        SIZE8BITS bDdiCHpdInvert : BITFIELD_BIT(3);            // DDI_B_HPD_INVERT
        SIZE8BITS bDdiCHpdInputEnable : BITFIELD_BIT(4);       // DDI_B_HPD_INPUT_ENABLE
        SIZE8BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(5, 7); // MBZ
    };

} BXT_HOTPLUG_CTL_REG_ST_C;

typedef union _BXT_HOTPLUG_CTL_REG_ST {
    DDU32 ulValue;
    struct
    {
        BXT_HOTPLUG_CTL_REG_ST_B;

        BXT_HOTPLUG_CTL_REG_ST_C;
        SIZE8BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(16, 23); // MBZ

        BXT_HOTPLUG_CTL_REG_ST_A;
    };
} BXT_HOTPLUG_CTL_REG_ST;

typedef union _BXT_HOTPLUG_CTL_REG_ST_A0 {
    DDU32 ulValue;
    struct
    {
        BXT_HOTPLUG_CTL_REG_ST_C;

        BXT_HOTPLUG_CTL_REG_ST_A;
        SIZE8BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(16, 23); // MBZ

        BXT_HOTPLUG_CTL_REG_ST_B;
    };
} BXT_HOTPLUG_CTL_REG_ST_A0;

// SPT SDE Hot plug CTL
#define SPT_SHOTPLUG_CTL_REG 0xC4030
#define SPT_SHOTPLUG_CTL_WZ_BITS (BITRANGE(3, 2) | BITRANGE(7, 5) | BITRANGE(11, 10) | BITRANGE(15, 13) | BITRANGE(11, 10) | BITRANGE(15, 13) | BITRANGE(27, 26) | BITRANGE(31, 29))

typedef union _SPT_HOTPLUG_CTL_REG_ST {
    DDU32 ulValue;
    struct
    {
        DDU32 bDdiB_ShortPulseStatus : BITFIELD_BIT(0);
        DDU32 bDdiB_LongPulseStatus : BITFIELD_BIT(1);
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(2, 3); // MBZ
        DDU32 bDdiBHpdInputEnable : BITFIELD_BIT(4);       // DDI_B_HPD_INPUT_ENABLE
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(5, 7); // MBZ

        DDU32 bDdiC_ShortPulseStatus : BITFIELD_BIT(8);
        DDU32 bDdiC_LongPulseStatus : BITFIELD_BIT(9);
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(10, 11); // MBZ
        DDU32 bDdiCHpdInputEnable : BITFIELD_BIT(12);        // DDI_C_HPD_INPUT_ENABLE
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(13, 15); // MBZ

        DDU32 bDdiD_ShortPulseStatus : BITFIELD_BIT(16);
        DDU32 bDdiD_LongPulseStatus : BITFIELD_BIT(17);
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(18, 19); // MBZ
        DDU32 bDdiDHpdInputEnable : BITFIELD_BIT(20);        // DDI_D_HPD_INPUT_ENABLE
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(21, 23); // MBZ

        DDU32 bDdiA_ShortPulseStatus : BITFIELD_BIT(24);
        DDU32 bDdiA_LongPulseStatus : BITFIELD_BIT(25);
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(26, 27); // MBZ
        DDU32 bDdiAHpdInputEnable : BITFIELD_BIT(28);        // DDI_A_HPD_INPUT_ENABLE
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(29, 31); // MBZ
    };
} SPT_HOTPLUG_CTL_REG_ST;

#define SPT_SHOTPLUG_CTL2_REG 0xC403C
#define SPT_SHOTPLUG_CTL2_WZ_BITS (BITRANGE(3, 2) | BITRANGE(31, 5))

typedef union _SPT_HOTPLUG_CTL2_REG_ST {
    DDU32 ulValue;
    struct
    {
        DDU32 bDdiE_ShortPulseStatus : BITFIELD_BIT(0);
        DDU32 bDdiE_LongPulseStatus : BITFIELD_BIT(1);
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(2, 3);  // MBZ
        DDU32 bDdiEHpdInputEnable : BITFIELD_BIT(4);        // DDI_E_HPD_INPUT_ENABLE
        DDU32 UNIQUENAME(Reserved) : BITFIELD_RANGE(5, 31); // MBZ
    };
} SPT_HOTPLUG_CTL2_REG_ST;

#define SKL_PCU_IMR 0x444E4
#define SKL_PCU_IIR 0x444E8
#define SKL_PCU_IER 0x444EC
#define SKL_PCU_PRESERVE_BITS (BITRANGE(31, 26) | BITRANGE(23, 2))
#define SKL_PCU_WZ_BITS (0)

typedef union _SKL_PCU_INTERRUPT_TABLE {
    DDU32 ulValue;
    struct
    {
        DDU32 bKVMRRequestDisplayEnable : 1; // bit 0
        DDU32 bKVMRReleaseDisplayEnable : 1; // bit 1
        DDU32 UNIQUENAME(Reserved) : 22;     // bit 23-2
        DDU32 bPCThermalEvent : 1;           // bit 24
        DDU32 bPCDriverMBEvent : 1;          // bit 25
        DDU32 UNIQUENAME(Reserved) : 6;      // bit 31-26
    };
} SKL_PCU_INTERRUPT_TABLE;
// IMPLICIT ENUMERATIONS USED BY GT_INTERRUPT_3_DEFINITION_BXT
//
typedef enum _GT_3_INTERRUPTS_INSTANCE_BXT
{
    GT_3_INTERRUPTS_INSTANCE_ADDRESS_BXT = 0x44330,
    BXT_GT3_IER                          = 0x4433C,
    BXT_GT3_IMR                          = 0x44334,
    BXT_GT3_IIR                          = 0x44338
} GT_3_INTERRUPTS_INSTANCE_BXT;

typedef enum _GT_INTERRUPT_3_DEFINITION_MASKS_BXT
{
    GT_INTERRUPT_3_DEFINITION_MASKS_WO_BXT  = 0x0,
    GT_INTERRUPT_3_DEFINITION_MASKS_MBZ_BXT = 0x0,
    GT_INTERRUPT_3_DEFINITION_MASKS_PBC_BXT = 0x0,
} GT_INTERRUPT_3_DEFINITION_MASKS_BXT;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the GT Interrupt 3 registers.
Bits 15:0 are used for VEBox.
Bits 27:16 are used for WDBox.
Bits 31:28 are used for OACS.
The VEBox Interrupt IIR (sticky) bits are ORed together to generate the VEBox Interrupts Pending bit in the Master Interrupt Control register.
The WDBox and OACS Interrupt IIR (sticky) bits are ORed together to generate the WDBox Interrupts Pending bit in the Master Interrupt Control register.
0x44330 = ISR
0x44334 = IMR
0x44338 = IIR
0x4433C = IER
\*****************************************************************************/
typedef union _GT_INTERRUPT_3_DEFINITION_BXT {
    struct
    {
        DDU32 VecsMiUserInterrupt : BITFIELD_BIT(0);        //
        DDU32 Spare1 : BITFIELD_BIT(1);                     //
        DDU32 Spare2 : BITFIELD_BIT(2);                     //
        DDU32 VecsErrorInterrupt : BITFIELD_BIT(3);         //
        DDU32 VecsMiFlushDwNotify : BITFIELD_BIT(4);        //
        DDU32 Spare5 : BITFIELD_BIT(5);                     //
        DDU32 Spare6 : BITFIELD_BIT(6);                     //
        DDU32 Spare7 : BITFIELD_BIT(7);                     //
        DDU32 VecsContextSwitchInterrupt : BITFIELD_BIT(8); //
        DDU32 Spare9 : BITFIELD_BIT(9);                     //
        DDU32 Spare10 : BITFIELD_BIT(10);                   //
        DDU32 VecsWaitOnSemaphore : BITFIELD_BIT(11);       //
        DDU32 Spare12 : BITFIELD_BIT(12);                   //
        DDU32 Spare13 : BITFIELD_BIT(13);                   //
        DDU32 Spare14 : BITFIELD_BIT(14);                   //
        DDU32 Spare15 : BITFIELD_BIT(15);                   //
        DDU32 Wdbox1StatusInterrupt : BITFIELD_BIT(16);     //
        DDU32 Wdbox1EndOfFrameInterrupt : BITFIELD_BIT(17); //
        DDU32 Spare18 : BITFIELD_BIT(18);                   //
        DDU32 Spare19 : BITFIELD_BIT(19);                   //
        DDU32 Spare20 : BITFIELD_BIT(20);                   //
        DDU32 Spare21 : BITFIELD_BIT(21);                   //
        DDU32 Spare22 : BITFIELD_BIT(22);                   //
        DDU32 Spare23 : BITFIELD_BIT(23);                   //
        DDU32 Spare24 : BITFIELD_BIT(24);                   //
        DDU32 Spare25 : BITFIELD_BIT(25);                   //
        DDU32 Spare26 : BITFIELD_BIT(26);                   //
        DDU32 Spare27 : BITFIELD_BIT(27);                   //

        /*****************************************************************************\
        For internal trigger (timer or NOA event based) based reporting, if the report buffer crosses half full limit, this interrupt is generated
        \*****************************************************************************/
        DDU32 PerformanceMonitoringBufferHalfFullInterrupt : BITFIELD_BIT(28); //
        DDU32 Spare29 : BITFIELD_BIT(29);                                      //
        DDU32 Spare30 : BITFIELD_BIT(30);                                      //
        DDU32 Spare31 : BITFIELD_BIT(31);                                      //
    };
    DDU32 ulValue;

} GT_INTERRUPT_3_DEFINITION_BXT, *PGT_INTERRUPT_3_DEFINITION_BXT;

#define BXT_GT3_PRESERVE_BITS (BITRANGE(2, 1) | BITRANGE(7, 5) | BITRANGE(10, 9) | BITRANGE(15, 13) | BITRANGE(27, 18) | BITRANGE(31, 29))
#define BXT_GT3_WZ_BITS (0)
#define BXT_GT3_IMR_VALID (~BXT_GT3_PRESERVE_BITS)

#define BXT_GT_VECS_MASK (BIT0 | BITRANGE(4, 3) | BIT8 | BIT11 | BITRANGE(17, 16))
#define BXT_GT_OA_MASK (BIT28)

#endif
