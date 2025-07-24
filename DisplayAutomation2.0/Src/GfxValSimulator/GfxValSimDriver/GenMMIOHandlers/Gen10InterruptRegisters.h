/*****************************************************************************\

INTEL CONFIDENTIAL
Copyright 2013
Intel Corporation All Rights Reserved.

The source code contained or described herein and all documents related to the
source code ("Material") are owned by Intel Corporation or its suppliers or
licensors. Title to the Material remains with Intel Corporation or its suppliers
and licensors. The Material contains trade secrets and proprietary and confidential
information of Intel or its suppliers and licensors. The Material is protected by
worldwide copyright and trade secret laws and treaty provisions. No part of the
Material may be used, copied, reproduced, modified, published, uploaded, posted
transmitted, distributed, or disclosed in any way without Intel's prior express

written permission.

No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel
or otherwise. Any license under such intellectual property rights must be
express and approved by Intel in writing.

This file is auto-generated.  Do NOT modify this file as changes will be lost.

Generator Binary Version: r56346+

\*****************************************************************************/
#ifndef GEN10INTRREGS_H
#define GEN10INTRREGS_H

#include "..//CommonInclude//DisplayDefs.h"

// IMPLICIT ENUMERATIONS USED BY MASTER_INT_CTL_CNL
//
typedef enum _MASTER_INTR_ENABLE_CNL
{
    MASTER_INTR_ENABLE_MASTER_INTR_DISABLE_CNL = 0x0,
    MASTER_INTR_ENABLE_MASTER_INTR_ENABLE_CNL  = 0x1,
} MASTER_INTR_ENABLE_CNL;

typedef enum _MASTER_INTR_CTL_INSTANCE_CNL
{
    MASTER_INTR_CTL_ADDR_CNL = 0x44200,
} MASTER_INTR_CTL_INSTANCE_CNL;

typedef enum _MASTER_INT_CTL_MASKS_CNL
{
    MASTER_INT_CTL_MASKS_WO_CNL  = 0x0,
    MASTER_INT_CTL_MASKS_MBZ_CNL = 0x0,
    MASTER_INT_CTL_MASKS_PBC_CNL = 0x0,
} MASTER_INT_CTL_MASKS_CNL;

/*****************************************************************************\
This register has the master enable for graphics interrupts and gives an overview of what interrupts are pending.
An interrupt pending bit will read 1b while one or more interrupts of that category are set (IIR) and enabled (IER).
All Pending Interrupts are ORed together to generate the combined interrupt.
The combined interrupt is ANDed with the Master Interrupt enable to create the master enabled interrupt.
The master enabled interrupt goes to PCI device 2 interrupt processing.
The master interrupt enable must be set before any of these interrupts will propagate to PCI device 2 interrupt processing.
\*****************************************************************************/
typedef union _MASTER_INT_CTL_CNL {
    struct
    {

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 RenderInterruptsPending : DD_BITFIELD_BIT(0); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 BlitterInterruptsPending : DD_BITFIELD_BIT(1); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 Vcs1InterruptsPending : DD_BITFIELD_BIT(2); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 Vcs2InterruptsPending : DD_BITFIELD_BIT(3); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 GtpmInterruptsPending : DD_BITFIELD_BIT(4); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 GucInterruptsPending : DD_BITFIELD_BIT(5); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 VeboxInterruptsPending : DD_BITFIELD_BIT(6); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 WdboxOrOacsInterruptsPending : DD_BITFIELD_BIT(7); //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(8, 15);   //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 DePipeAInterruptsPending : DD_BITFIELD_BIT(16); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 DePipeBInterruptsPending : DD_BITFIELD_BIT(17); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 DePipeCInterruptsPending : DD_BITFIELD_BIT(18); //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(19);     //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 DePortInterruptsPending : DD_BITFIELD_BIT(20); //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(21);    //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 DeMiscInterruptsPending : DD_BITFIELD_BIT(22); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        The PCH Display interrupt is configured through the SDE interrupt registers.
        \*****************************************************************************/
        DDU32 DePchInterruptsPending : DD_BITFIELD_BIT(23); //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 AudioCodecInterruptsPending : DD_BITFIELD_BIT(24); //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(25, 29);  //

        /*****************************************************************************\
        This field indicates if interrupts of this category are pending.
        \*****************************************************************************/
        DDU32 PcuInterruptsPending : DD_BITFIELD_BIT(30); //

        /*****************************************************************************\
        This is the master control for graphics interrupts.
        This must be enabled for any of these interrupts to propagate to PCI device 2 interrupt processing.
        \*****************************************************************************/
        DDU32 MasterInterruptEnable : DD_BITFIELD_BIT(31); // MASTER_INTR_ENABLE_CNL
    };
    DDU32 Value;

} MASTER_INT_CTL_CNL, *PMASTER_INT_CTL_CNL;

C_ASSERT(4 == sizeof(MASTER_INT_CTL_CNL));

// IMPLICIT ENUMERATIONS USED BY GT_INTR_0_TABLE_CNL
//
typedef enum _GT_0_INTR_INSTANCE_CNL
{
    GT_0_INTR_ISR_ADDR_CNL = 0x44300,
    GT_0_INTR_IMR_ADDR_CNL = 0x44304,
    GT_0_INTR_IIR_ADDR_CNL = 0x44308,
    GT_0_INTR_IER_ADDR_CNL = 0x4430C,
} GT_0_INTR_INSTANCE_CNL;

typedef enum _GT_INTR_0_CNL
{
    GT_INTR_0_WO_CNL  = 0x0,
    GT_INTR_0_MBZ_CNL = 0x0,
    GT_INTR_0_PBC_CNL = 0x0,
} GT_INTR_0_CNL;

#define BDW_GT_REN_IMR 0x020A8
#define BDW_GT_VID_IMR 0x120A8
#define BDW_GT_BLT_IMR 0x220A8
#define BDW_GT_VECS_IMR 0x1A0A8
#define BDW_GT_VID2_IMR 0x1C0A8
#define BDW_GT_OA_IMR 0x02B20

#define CNL_GT_REN_IMR_PRESERVE_BITS (DD_BITRANGE_MASK(31, 15) | DD_BITRANGE_MASK(13, 12) | BIT5 | BIT2)
#define CNL_GT_VID_IMR_PRESERVE_BITS (DD_BITRANGE_MASK(31, 12) | BIT10 | BIT7 | DD_BITRANGE_MASK(2, 1))
#define CNL_GT_BLT_IMR_PRESERVE_BITS (DD_BITRANGE_MASK(31, 28) | DD_BITRANGE_MASK(26, 25) | BIT23 | BIT21 | DD_BITRANGE_MASK(18, 17) | DD_BITRANGE_MASK(15, 0))
#define CNL_GT_VECS_IMR_PRESERVE_BITS (DD_BITRANGE_MASK(31, 12) | DD_BITRANGE_MASK(10, 9) | BIT7 | BIT5 | BIT2 | BIT1)
#define CNL_GT_VID2_IMR_PRESERVE_BITS (DD_BITRANGE_MASK(31, 28) | BIT26 | BIT23 | DD_BITRANGE_MASK(18, 17) | DD_BITRANGE_MASK(15, 0))
#define CNL_GT_OA_IMR_PRESERVE_BITS (DD_BITRANGE_MASK(31, 29) | DD_BITRANGE_MASK(27, 0))

#define CNL_GT_REN_IMR_VALID (~CNL_GT_REN_IMR_PRESERVE_BITS)
#define CNL_GT_VID_IMR_VALID (~CNL_GT_VID_IMR_PRESERVE_BITS)
#define CNL_GT_BLT_IMR_VALID (~CNL_GT_BLT_IMR_PRESERVE_BITS)
#define CNL_GT_VECS_IMR_VALID (~CNL_GT_VECS_IMR_PRESERVE_BITS)
#define CNL_GT_VID2_IMR_VALID (~CNL_GT_VID2_IMR_PRESERVE_BITS)
#define CNL_GT_OA_IMR_VALID (~CNL_GT_OA_IMR_PRESERVE_BITS)
#define CNL_GT_WZ_BITS (0)

#define BDW_GT_BLT_MASK (BIT16 | DD_BITRANGE_MASK(20, 19) | BIT24 | BIT27)
#define BDW_GT_REN_MASK (DD_BITRANGE_MASK(1, 0) | DD_BITRANGE_MASK(8, 3) | BIT10 | BIT11)
#define BDW_GT_VCS1_MASK (BIT0 | DD_BITRANGE_MASK(6, 2) | BIT8 | BIT9 | BIT11)
#define BDW_GT_VECS_MASK (BIT0 | DD_BITRANGE_MASK(4, 2) | BIT8 | BIT11 | DD_BITRANGE_MASK(17, 16))
#define BDW_GT_OA_MASK (BIT28)
#define BDW_GT_VCS2_MASK (BIT16 | DD_BITRANGE_MASK(22, 18) | BIT24 | BIT25 | BIT27)

#define CNL_GT0_PRESERVE_BITS (DD_BITRANGE_MASK(31, 28) | DD_BITRANGE_MASK(26, 25) | DD_BITRANGE_MASK(23, 21) | BIT18 | BIT17 | BIT15 | DD_BITRANGE_MASK(13, 12) | BIT5 | BIT2)
#define CNL_GT0_WZ_BITS (0)
#define CNL_GT0_IMR_VALID (~CNL_GT0_PRESERVE_BITS)

/*****************************************************************************\
This table indicates which events are mapped to each bit of the GT Interrupt 0 registers.
Bits 15:0 are used for Render CS.
Bits 31:16 are used for Blitter CS.
The IER enabled Render Interrupt IIR (sticky) bits are ORed together to generate the Render Interrupts Pending bit in the Master Interrupt Control register.
The IER enabled Blitter Interrupt IIR (sticky) bits are ORed together to generate the Blitter Interrupts Pending bit in the Master Interrupt Control register.
0x44300 = ISR
0x44304 = IMR
0x44308 = IIR
0x4430C = IER
\*****************************************************************************/
typedef union _GT_INTR_0_TABLE_CNL {
    struct
    {
        DDU32 CsMiUserInterrupt : DD_BITFIELD_BIT(0);        //
        DDU32 EuDebugFromSvg : DD_BITFIELD_BIT(1);           //
        DDU32 Spare2 : DD_BITFIELD_BIT(2);                   //
        DDU32 CsErrorInterrupt : DD_BITFIELD_BIT(3);         //
        DDU32 CsPipe_ControlNotify : DD_BITFIELD_BIT(4);     //
        DDU32 Spare5 : DD_BITFIELD_BIT(5);                   //
        DDU32 CsWatchdogCounterExpired : DD_BITFIELD_BIT(6); //

        /*****************************************************************************\
        This interrupt is for handling Legacy Page Fault interface for all Command Streamers [BCS, RCS, VCS, VECS].
        When Fault Repair Mode is enabled, Interrupt mask register value is not looked at to generate interrupt due to page fault.
        Please refer to vol1c "page fault support" section for more details.

        In Advanced (PRQ) Fault Interface is done through GUC interface.
        \*****************************************************************************/
        DDU32 PageFaultInterrupt : DD_BITFIELD_BIT(7);         //
        DDU32 CsContextSwitchInterrupt : DD_BITFIELD_BIT(8);   //
        DDU32 CsTrInvalidTileDetection : DD_BITFIELD_BIT(9);   //
        DDU32 CsL3CounterSave : DD_BITFIELD_BIT(10);           //
        DDU32 CsWaitOnSemaphore : DD_BITFIELD_BIT(11);         //
        DDU32 Spare12 : DD_BITFIELD_BIT(12);                   //
        DDU32 Spare13 : DD_BITFIELD_BIT(13);                   //
        DDU32 EuRestartInterrupt : DD_BITFIELD_BIT(14);        //
        DDU32 Spare15 : DD_BITFIELD_BIT(15);                   //
        DDU32 BcsMiUserInterrupt : DD_BITFIELD_BIT(16);        //
        DDU32 Spare17 : DD_BITFIELD_BIT(17);                   //
        DDU32 Spare18 : DD_BITFIELD_BIT(18);                   //
        DDU32 BcsErrorInterrupt : DD_BITFIELD_BIT(19);         //
        DDU32 BcsMiFlushDwNotify : DD_BITFIELD_BIT(20);        //
        DDU32 Spare21 : DD_BITFIELD_BIT(21);                   //
        DDU32 BcsWatchdogCounterExpired : DD_BITFIELD_BIT(22); //
        DDU32 Spare23 : DD_BITFIELD_BIT(23);                   //
        DDU32 BcsContextSwitchInterrupt : DD_BITFIELD_BIT(24); //
        DDU32 Spare25 : DD_BITFIELD_BIT(25);                   //
        DDU32 Spare26 : DD_BITFIELD_BIT(26);                   //
        DDU32 BcsWaitOnSemaphore : DD_BITFIELD_BIT(27);        //
        DDU32 Spare28 : DD_BITFIELD_BIT(28);                   //
        DDU32 Spare29 : DD_BITFIELD_BIT(29);                   //
        DDU32 Spare30 : DD_BITFIELD_BIT(30);                   //
        DDU32 Spare31 : DD_BITFIELD_BIT(31);                   //
    };
    DDU32 Value;

} GT_INTR_0_TABLE_CNL;

C_ASSERT(4 == sizeof(GT_INTR_0_TABLE_CNL));

// IMPLICIT ENUMERATIONS USED BY GT_INTR_1_TABLE_CNL
//
typedef enum _GT_1_INTR_INSTANCE_CNL
{
    GT_1_INTR_ISR_ADDR_CNL = 0x44310,
    GT_1_INTR_IMR_ADDR_CNL = 0x44314,
    GT_1_INTR_IIR_ADDR_CNL = 0x44318,
    GT_1_INTR_IER_ADDR_CNL = 0x4431C,
} GT_1_INTR_INSTANCE_CNL;

typedef enum _GT_INTR_1_CNL
{
    GT_INTR_1_WO_CNL  = 0x0,
    GT_INTR_1_MBZ_CNL = 0x0,
    GT_INTR_1_PBC_CNL = 0x0,
} GT_INTR_1_CNL;

#define BDW_GT1_PRESERVE_BITS (DD_BITRANGE_MASK(31, 28) | BIT26 | BIT23 | BIT18 | BIT17 | DD_BITRANGE_MASK(15, 12) | BIT10 | BIT7 | BIT2 | BIT1)
#define BDW_GT1_WZ_BITS (0)
#define BDW_GT1_IMR_VALID (~BDW_GT1_PRESERVE_BITS)

/*****************************************************************************\
This table indicates which events are mapped to each bit of the GT Interrupt 1 registers.
Bits 15:0 are used for VCS1.
Bits 31:16 are used for VCS2.
The VCS1 Interrupt IIR (sticky) bits are ORed together to generate the VCS1 Interrupts Pending bit in the Master Interrupt Control register.
The VCS2 Interrupt IIR (sticky) bits are ORed together to generate the VCS2 Interrupts Pending bit in the Master Interrupt Control register.
0x44310 = ISR
0x44314 = IMR
0x44318 = IIR
0x4431C = IER
\*****************************************************************************/
typedef union _GT_INTR_1_TABLE_CNL {
    struct
    {
        DDU32 Vcs1MiUserInterrupt : DD_BITFIELD_BIT(0);                    //
        DDU32 Spare1 : DD_BITFIELD_BIT(1);                                 //
        DDU32 Spare2 : DD_BITFIELD_BIT(2);                                 //
        DDU32 Vcs1ErrorInterrupt : DD_BITFIELD_BIT(3);                     //
        DDU32 Vcs1MiFlushDwNotify : DD_BITFIELD_BIT(4);                    //
        DDU32 Vcs1NotifyPavpForInlineReadCompletion : DD_BITFIELD_BIT(5);  //
        DDU32 Vcs1WatchdogCounterExpired : DD_BITFIELD_BIT(6);             //
        DDU32 Spare7 : DD_BITFIELD_BIT(7);                                 //
        DDU32 Vcs1ContextSwitchInterrupt : DD_BITFIELD_BIT(8);             //
        DDU32 Vcs1TerminationonPavpAttack : DD_BITFIELD_BIT(9);            //
        DDU32 Spare10 : DD_BITFIELD_BIT(10);                               //
        DDU32 Vcs1WaitOnSemaphore : DD_BITFIELD_BIT(11);                   //
        DDU32 Spare12 : DD_BITFIELD_BIT(12);                               //
        DDU32 Spare13 : DD_BITFIELD_BIT(13);                               //
        DDU32 Spare14 : DD_BITFIELD_BIT(14);                               //
        DDU32 Spare15 : DD_BITFIELD_BIT(15);                               //
        DDU32 Vcs2MiUserInterrupt : DD_BITFIELD_BIT(16);                   //
        DDU32 Spare17 : DD_BITFIELD_BIT(17);                               //
        DDU32 Spare18 : DD_BITFIELD_BIT(18);                               //
        DDU32 Vcs2ErrorInterrupt : DD_BITFIELD_BIT(19);                    //
        DDU32 Vcs2MiFlushDwNotify : DD_BITFIELD_BIT(20);                   //
        DDU32 Vcs2NotifyPavpForInlineReadCompletion : DD_BITFIELD_BIT(21); //
        DDU32 Vcs2WatchdogCounterExpired : DD_BITFIELD_BIT(22);            //
        DDU32 Spare23 : DD_BITFIELD_BIT(23);                               //
        DDU32 Vcs2ContextSwitchInterrupt : DD_BITFIELD_BIT(24);            //
        DDU32 Vcs2TerminationonPavpAttack : DD_BITFIELD_BIT(25);           //
        DDU32 Spare26 : DD_BITFIELD_BIT(26);                               //
        DDU32 Vcs2WaitOnSemaphore : DD_BITFIELD_BIT(27);                   //
        DDU32 Spare28 : DD_BITFIELD_BIT(28);                               //
        DDU32 Spare29 : DD_BITFIELD_BIT(29);                               //
        DDU32 Spare30 : DD_BITFIELD_BIT(30);                               //
        DDU32 Spare31 : DD_BITFIELD_BIT(31);                               //
    };
    DDU32 Value;

} GT_INTR_1_TABLE_CNL;

C_ASSERT(4 == sizeof(GT_INTR_1_TABLE_CNL));

// IMPLICIT ENUMERATIONS USED BY GT_INTR_2_TABLE_CNL
//
typedef enum _GT_2_INTR_INSTANCE_CNL
{
    GT_2_INTR_ISR_ADDR_CNL = 0x44320,
    GT_2_INTR_IMR_ADDR_CNL = 0x44324,
    GT_2_INTR_IIR_ADDR_CNL = 0x44328,
    GT_2_INTR_IER_ADDR_CNL = 0x4432C,
} GT_2_INTR_INSTANCE_CNL;

typedef enum _GT_INTR_2_CNL
{
    GT_INTR_2_WO_CNL  = 0x0,
    GT_INTR_2_MBZ_CNL = 0x0,
    GT_INTR_2_PBC_CNL = 0x0,
} GT_INTR_2_CNL;

#define BDW_GT2_PRESERVE_BITS (BIT15 | BIT14 | BIT3 | BIT0)
#define BDW_GT2_WZ_BITS (0)
#define BDW_GT2_IMR_VALID (~BDW_GT2_PRESERVE_BITS)

/*****************************************************************************\
This table indicates which events are mapped to each bit of the GT Interrupt 2 registers.
Bits 15:0 are used for GTPM.
The IER enabled GTPM Interrupt IIR (sticky) bits are ORed together to generate the GTPM Interrupts Pending bit in the Master Interrupt Control register.
0x44320 = ISR
0x44324 = IMR
0x44328 = IIR
0x4432C = IERBits 31:16 are used for GuC. The IER enabled GuC Interrupt IIR (sticky) bits are ORed
together to generate the GuC Interrupts Pending bit in the Master Interrupt Control register.
\*****************************************************************************/
typedef union _GT_INTR_2_TABLE_CNL {
    struct
    {
        DDU32 Spare0 : DD_BITFIELD_BIT(0);                                                //
        DDU32 GtpmRenderGeyservilleDownEvaluationIntervalInterrupt : DD_BITFIELD_BIT(1);  //
        DDU32 GtpmRenderGeyservilleUpEvaluationIntervalInterrupt : DD_BITFIELD_BIT(2);    //
        DDU32 Spare3 : DD_BITFIELD_BIT(3);                                                //
        DDU32 GtpmRenderPStateDownThresholdInterrupt : DD_BITFIELD_BIT(4);                //
        DDU32 GtpmRenderPStateUpThresholdInterrupt : DD_BITFIELD_BIT(5);                  //
        DDU32 GtpmRenderFrequencyDownwardsTimeoutDuringRc6Interrupt : DD_BITFIELD_BIT(6); //
        DDU32 GtpmUncoreToCoreTrapInterrupt : DD_BITFIELD_BIT(7);                         //
        DDU32 GtpmEnginesIdleInterrupt : DD_BITFIELD_BIT(8);                              //

        /*****************************************************************************\
        Always Running Apic Timer Interrupt.  This interrupt is intended for use with the GT micro-controller.  Use by software is not supported.
        \*****************************************************************************/
        DDU32 AratInterrupt : DD_BITFIELD_BIT(9);                         //
        DDU32 NfadflFrequencyDownInterrupt : DD_BITFIELD_BIT(10);         //
        DDU32 NfadflFrequencyUpInterrupt : DD_BITFIELD_BIT(11);           //
        DDU32 UnsliceFrequencyControlDownInterrupt : DD_BITFIELD_BIT(12); //
        DDU32 UnsliceFrequencyControlUpInterrupt : DD_BITFIELD_BIT(13);   //
        DDU32 Spare14 : DD_BITFIELD_BIT(14);                              //
        DDU32 Spare15 : DD_BITFIELD_BIT(15);                              //
        DDU32 GucSwInterrupt0 : DD_BITFIELD_BIT(16);                      //
        DDU32 GucSwInterrupt1 : DD_BITFIELD_BIT(17);                      //
        DDU32 GucSwInterrupt2 : DD_BITFIELD_BIT(18);                      //
        DDU32 GucSwInterrupt3 : DD_BITFIELD_BIT(19);                      //
        DDU32 GucSwInterrupt4 : DD_BITFIELD_BIT(20);                      //
        DDU32 GucSwInterrupt5 : DD_BITFIELD_BIT(21);                      //
        DDU32 GucSwInterrupt6 : DD_BITFIELD_BIT(22);                      //
        DDU32 GucNotificationError : DD_BITFIELD_BIT(23);                 //
        DDU32 GucFatalError : DD_BITFIELD_BIT(24);                        //
        DDU32 GucDmaDone : DD_BITFIELD_BIT(25);                           //
        DDU32 GucDoorbellRang : DD_BITFIELD_BIT(26);                      //
        DDU32 IommuSentMessageToGuc : DD_BITFIELD_BIT(27);                //
        DDU32 GucSemaphoreSignaled : DD_BITFIELD_BIT(28);                 //
        DDU32 GucDisplayEventReceived : DD_BITFIELD_BIT(29);              //
        DDU32 GucExecutionError : DD_BITFIELD_BIT(30);                    //
        DDU32 GucInterruptToHost : DD_BITFIELD_BIT(31);                   //
    };
    DDU32 Value;

} GT_INTR_2_TABLE_CNL;

C_ASSERT(4 == sizeof(GT_INTR_2_TABLE_CNL));

// IMPLICIT ENUMERATIONS USED BY GT_INTR_3_TABLE_CNL
//
typedef enum _GT_3_INTR_INSTANCE_CNL
{
    GT_3_INTR_ISR_ADDR_CNL = 0x44330,
    GT_3_INTR_IMR_ADDR_CNL = 0x44334,
    GT_3_INTR_IIR_ADDR_CNL = 0x44338,
    GT_3_INTR_IER_ADDR_CNL = 0x4433C,
} GT_3_INTR_INSTANCE_CNL;

typedef enum _GT_INTR_3_CNL
{
    GT_INTR_3_WO_CNL  = 0x0,
    GT_INTR_3_MBZ_CNL = 0x0,
    GT_INTR_3_PBC_CNL = 0x0,
} GT_INTR_3_CNL;

#define CNL_GT3_PRESERVE_BITS \
    (DD_BITRANGE_MASK(31, 29) | DD_BITRANGE_MASK(27, 22) | DD_BITRANGE_MASK(19, 18) | DD_BITRANGE_MASK(15, 12) | DD_BITRANGE_MASK(10, 9) | BIT7 | BIT5 | BIT2 | BIT1)
#define CNL_GT3_IMR_VALID (~CNL_GT3_PRESERVE_BITS)

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
typedef union _GT_INTR_3_TABLE_CNL {
    struct
    {
        // VECS Interrupts
        DDU32 VecsMiUserInterrupt : DD_BITFIELD_BIT(0);        //
        DDU32 Spare1 : DD_BITFIELD_BIT(1);                     //
        DDU32 VecsMmioSyncFlushStatus : DD_BITFIELD_BIT(2);    //
        DDU32 VecsErrorInterrupt : DD_BITFIELD_BIT(3);         //
        DDU32 VecsMiFlushDwNotify : DD_BITFIELD_BIT(4);        //
        DDU32 Spare5 : DD_BITFIELD_BIT(5);                     //
        DDU32 VecsWatchDogCounterExpired : DD_BITFIELD_BIT(6); //
        DDU32 Spare7 : DD_BITFIELD_BIT(7);                     //
        DDU32 VecsContextSwitchInterrupt : DD_BITFIELD_BIT(8); //
        DDU32 Spare9 : DD_BITFIELD_BIT(9);                     //
        DDU32 Spare10 : DD_BITFIELD_BIT(10);                   //
        DDU32 VecsWaitOnSemaphore : DD_BITFIELD_BIT(11);       //
        DDU32 Spare12 : DD_BITFIELD_BIT(12);                   //
        DDU32 Spare13 : DD_BITFIELD_BIT(13);                   //
        DDU32 Spare14 : DD_BITFIELD_BIT(14);                   //
        DDU32 Spare15 : DD_BITFIELD_BIT(15);                   //

        // WDBox Interrupts
        DDU32 WDBox1EndOfFrameInterrupt : DD_BITFIELD_BIT(16); //
        DDU32 WDBox1StatusInterrupt : DD_BITFIELD_BIT(17);     //
        DDU32 Spare18 : DD_BITFIELD_BIT(18);                   //
        DDU32 Spare19 : DD_BITFIELD_BIT(19);                   //
        DDU32 Wdbox2EndOfFrameInterrupt : DD_BITFIELD_BIT(20); //
        DDU32 Wdbox2StatusInterrupt : DD_BITFIELD_BIT(21);     //
        DDU32 Spare22 : DD_BITFIELD_BIT(22);                   //
        DDU32 Spare23 : DD_BITFIELD_BIT(23);                   //
        DDU32 Spare24 : DD_BITFIELD_BIT(24);                   //
        DDU32 Spare25 : DD_BITFIELD_BIT(25);                   //
        DDU32 Spare26 : DD_BITFIELD_BIT(26);                   //
        DDU32 Spare27 : DD_BITFIELD_BIT(27);                   //

        /*****************************************************************************\
        For internal trigger (timer event based) reporting, this interrupt is generated if the report buffer crosses the half full limit.
        \*****************************************************************************/
        DDU32 PerformanceMonitoringBufferHalfFullInterrupt : DD_BITFIELD_BIT(28); //
        DDU32 Spare29 : DD_BITFIELD_BIT(29);                                      //
        DDU32 Spare30 : DD_BITFIELD_BIT(30);                                      //
        DDU32 Spare31 : DD_BITFIELD_BIT(31);                                      //
    };
    DDU32 Value;

} GT_INTR_3_TABLE_CNL;

C_ASSERT(4 == sizeof(GT_INTR_3_TABLE_CNL));

// IMPLICIT ENUMERATIONS USED BY PCU_INTR_TABLE_CNL
//
typedef enum _PCU_INTR_INSTANCE_CNL
{
    PCU_ISR_ADDR_CNL = 0x444E0,
    PCU_IMR_ADDR_CNL = 0x444E4,
    PCU_IIR_ADDR_CNL = 0x444E8,
    PCU_IER_ADDR_CNL = 0x444EC,
} PCU_INTR_INSTANCE_CNL;

typedef enum _PCU_INTR_CNL
{
    PCU_INTR_WO_CNL  = 0x0,
    PCU_INTR_MBZ_CNL = 0x0,
    PCU_INTR_PBC_CNL = 0x0,
} PCU_INTR_CNL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the PCU Interrupt registers.
0x444E0 = ISR
0x444E4 = IMR
0x444E8 = IIR
0x444EC = IER
\*****************************************************************************/
typedef union _PCU_INTR_TABLE_CNL {
    struct
    {

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        DDU32 Unused_Int_23_0 : DD_BITFIELD_RANGE(0, 23);           //
        DDU32 Pcu_Thermal_Event : DD_BITFIELD_BIT(24);              //
        DDU32 Pcu_Pcode2driver_Mailbox_Event : DD_BITFIELD_BIT(25); //

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        DDU32 Unused_Int_28_26 : DD_BITFIELD_RANGE(26, 28); //

        /*****************************************************************************\
        This field indicates DDIC hotplug activity was detected during DC9.
        \*****************************************************************************/
        DDU32 DdicDc9Hpd : DD_BITFIELD_BIT(29); //

        /*****************************************************************************\
        This field indicates DDIB hotplug activity was detected during DC9.
        \*****************************************************************************/
        DDU32 DdibDc9Hpd : DD_BITFIELD_BIT(30); //

        /*****************************************************************************\
        This field indicates DDIA hotplug activity was detected during DC9.
        \*****************************************************************************/
        DDU32 DdiaDc9Hpd : DD_BITFIELD_BIT(31); //
    };
    DDU32 Value;

} PCU_INTR_TABLE_CNL;

C_ASSERT(4 == sizeof(PCU_INTR_TABLE_CNL));

// IMPLICIT ENUMERATIONS USED BY DE_PORT_INTR_TABLE_CNL
//
typedef enum _DE_PORT_INTR_INSTANCE_CNL
{
    DE_PORT_ISR_INTR_ADDR_CNL = 0x44440,
    DE_PORT_IMR_INTR_ADDR_CNL = 0x44444,
    DE_PORT_IIR_INTR_ADDR_CNL = 0x44448,
    DE_PORT_IER_INTR_ADDR_CNL = 0x4444C,
} DE_PORT_INTR_INSTANCE_CNL;

typedef enum _DE_PORT_INTR_CNL
{
    DE_PORT_INTR_WO_CNL  = 0x0,
    DE_PORT_INTR_MBZ_CNL = 0x0,
    DE_PORT_INTR_PBC_CNL = 0x0,
} DE_PORT_INTR_CNL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine Port Interrupt registers.
The IER enabled Display Engine Port Interrupt IIR (sticky) bits are ORed together to generate the DE_Port Interrupts Pending bit in the Master Interrupt Control register.

0x44440 = ISR
0x44444 = IMR
0x44448 = IIR
0x4444C = IER
\*****************************************************************************/
typedef union _DE_PORT_INTR_TABLE_CNL {
    struct
    {

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI A done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        DDU32 Aux_Channel_A : DD_BITFIELD_BIT(0); //

        /*****************************************************************************\
        The ISR is an active high pulse when any of the unmasked events in GMBUS4 Interrupt Mask register occur.
        This field is only used on projects that have GMBUS integrated into the north display. Projects that have GMBUS in the south display
        have the GMBUS interrupt in the south display interrupts.
        \*****************************************************************************/
        DDU32 Gmbus : DD_BITFIELD_BIT(1);                //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(2); //

        /*****************************************************************************\
        The ISR gives the live state of the DDI A HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        DDU32 DdiAHotplug : DD_BITFIELD_BIT(3); //

        /*****************************************************************************\
        The ISR gives the live state of the DDI B HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        DDU32 DdiBHotplug : DD_BITFIELD_BIT(4); //

        /*****************************************************************************\
        The ISR gives the live state of the DDI C HPD pin when the HPD input is enabled.
        The IIR is set if a short or long pulse is detected when HPD input is enabled.
        \*****************************************************************************/
        DDU32 DdiCHotplug : DD_BITFIELD_BIT(5);               //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(6, 7); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected and is cleared by writing a '1' to this bit.
        The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        DDU32 ScdcReadRequestInterruptPortB : DD_BITFIELD_BIT(8); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected and is cleared by writing a '1' to this bit.
        The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        DDU32 ScdcReadRequestInterruptPortC : DD_BITFIELD_BIT(9); //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(10, 22);   //

        /*****************************************************************************\
        The ISR is an active high level indicating a TE interrupt is set in MIPIA_STATUS.
        \*****************************************************************************/
        DDU32 MipiATe : DD_BITFIELD_BIT(23); //

        /*****************************************************************************\
        The ISR is an active high level indicating a TE interrupt is set in MIPIC_STATUS.
        \*****************************************************************************/
        DDU32 MipiCTe : DD_BITFIELD_BIT(24); //

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI B done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        DDU32 AuxChannelB : DD_BITFIELD_BIT(25); //

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI C done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        DDU32 AuxChannelC : DD_BITFIELD_BIT(26); //

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI D done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        DDU32 AuxChannelD : DD_BITFIELD_BIT(27); //

        /*****************************************************************************\
        The ISR is an active high pulse on the AUX DDI F done event. This event will not occur for SRD AUX done.
        \*****************************************************************************/
        DDU32 AuxChannelF : DD_BITFIELD_BIT(28);          //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(29); //

        /*****************************************************************************\
        The ISR is an active high level indicating an interrupt is set in MIPIA_INTR_STAT_REG or MIPIA_INTR_STAT_REG_1.
        This field is only used on BXT.
        \*****************************************************************************/
        DDU32 MipiA : DD_BITFIELD_BIT(30); //

        /*****************************************************************************\
        The ISR is an active high level indicating an interrupt is set in MIPIC_INTR_STAT_REG or MIPIC_INTR_STAT_REG_1.
        \*****************************************************************************/
        DDU32 MipiC : DD_BITFIELD_BIT(31); //
    };
    DDU32 Value;

} DE_PORT_INTR_TABLE_CNL;

C_ASSERT(4 == sizeof(DE_PORT_INTR_TABLE_CNL));

// IMPLICIT ENUMERATIONS USED BY DE_PIPE_INTR_TABLE_CNL
//
typedef enum _DE_PIPE_A_INTR_INSTANCE_CNL
{
    DE_PIPE_A_ISR_ADDR_CNL = 0x44400,
    DE_PIPE_A_IMR_ADDR_CNL = 0x44404,
    DE_PIPE_A_IIR_ADDR_CNL = 0x44408,
    DE_PIPE_A_IER_ADDR_CNL = 0x4440C,
} DE_PIPE_A_INTR_INSTANCE_CNL;

typedef enum _DE_PIPE_B_INTR_INSTANCE_CNL
{
    DE_PIPE_B_ISR_ADDR_CNL = 0x44410,
    DE_PIPE_B_IMR_ADDR_CNL = 0x44414,
    DE_PIPE_B_IIR_ADDR_CNL = 0x44418,
    DE_PIPE_B_IER_ADDR_CNL = 0x4441C,
} DE_PIPE_B_INTR_INSTANCE_CNL;

typedef enum _DE_PIPE_C_INTR_INSTANCE_CNL
{
    DE_PIPE_C_ISR_ADDR_CNL = 0x44420,
    DE_PIPE_C_IMR_ADDR_CNL = 0x44424,
    DE_PIPE_C_IIR_ADDR_CNL = 0x44428,
    DE_PIPE_C_IER_ADDR_CNL = 0x4442C,
} DE_PIPE_C_INTR_INSTANCE_CNL;

typedef enum _DE_PIPE_INTR_CNL
{
    DE_PIPE_INTR_WO_CNL  = 0x0,
    DE_PIPE_INTR_PBC_CNL = 0x0,
    DE_PIPE_INTR_MBZ_CNL = 0xF0000,
} DE_PIPE_INTR_CNL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine Pipe Interrupt registers.

The IER enabled Display Engine Pipe Interrupt IIR (sticky) bits are ORed together to generate the DE_Pipe Interrupts Pending bit in the Master Interrupt Control register.

There is one full set of Display Engine Pipe interrupts per display pipes A/B/C.

The STEREO3D_EVENT_MASK selects between left eye and right eye reporting of vertical blank, vertical sync, and scanline events in stereo 3D modes.

0x44400 = ISR A, 0x44410 = ISR B, 0x44420 = ISR C
0x44404 = IMR A, 0x44414 = IMR B, 0x44424 = IMR C
0x44408 = IIR A, 0x44418 = IIR B, 0x44428 = IIR C
0x4440C = IER A, 0x4441C = IER B, 0x4442C = IER C
\*****************************************************************************/
typedef union _DE_PIPE_INTR_TABLE_CNL {
    struct
    {

        /*****************************************************************************\
        The ISR is an active high level for the duration of the vertical blank of the transcoder attached to this pipe.
        \*****************************************************************************/
        DDU32 Vblank : DD_BITFIELD_BIT(0); //

        /*****************************************************************************\
        The ISR is an active high level for the duration of the vertical sync of the transcoder attached to this pipe.
        \*****************************************************************************/
        DDU32 Vsync : DD_BITFIELD_BIT(1); //

        /*****************************************************************************\
        The ISR is an active high pulse on the scan line event of the transcoder attached to this pipe.
        \*****************************************************************************/
        DDU32 Scan_Line_Event : DD_BITFIELD_BIT(2); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 1 on this pipe.
        \*****************************************************************************/
        DDU32 Plane1_Flip_Done : DD_BITFIELD_BIT(3); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 2 on this pipe.
        \*****************************************************************************/
        DDU32 Plane2_Flip_Done : DD_BITFIELD_BIT(4); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 3 on this pipe.  Not all pipes have a plane 3.
        \*****************************************************************************/
        DDU32 Plane3_Flip_Done : DD_BITFIELD_BIT(5); //

        /*****************************************************************************\
        The ISR is an active high pulse when the flip is done for plane 4 on this pipe.  Not all pipes have a plane 4.
        \*****************************************************************************/
        DDU32 Plane4_Flip_Done : DD_BITFIELD_BIT(6); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 1 on this pipe.
        \*****************************************************************************/
        DDU32 Plane1_Gtt_Fault_Status : DD_BITFIELD_BIT(7); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 2 on this pipe.
        \*****************************************************************************/
        DDU32 Plane2_Gtt_Fault_Status : DD_BITFIELD_BIT(8); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 3 on this pipe.  Not all pipes a have plane 3.
        \*****************************************************************************/
        DDU32 Plane3_Gtt_Fault_Status : DD_BITFIELD_BIT(9); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for plane 4 on this pipe.  Not all pipes a have plane 4.
        \*****************************************************************************/
        DDU32 Plane4_Gtt_Fault_Status : DD_BITFIELD_BIT(10); //

        /*****************************************************************************\
        The ISR is an active high pulse when a GTT fault is detected for the cursor on this pipe.
        \*****************************************************************************/
        DDU32 Cursor_Gtt_Fault_Status : DD_BITFIELD_BIT(11); //

        /*****************************************************************************\
        The ISR is an active high pulse on the DPST Histogram event on this pipe.
        \*****************************************************************************/
        DDU32 Dpst_Histogram_Event : DD_BITFIELD_BIT(12); //

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        DDU32 Unused_Int_15_13 : DD_BITFIELD_RANGE(13, 15); //
        DDU32 Plane1FlipQueueEmpty : DD_BITFIELD_BIT(16);
        DDU32 Plane2FlipQueueEmpty : DD_BITFIELD_BIT(17);
        DDU32 Plane3FlipQueueEmpty : DD_BITFIELD_BIT(18);
        DDU32 Plane4FlipQueueEmpty : DD_BITFIELD_BIT(19); // BXT

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        DDU32 Unused_Int_27_20 : DD_BITFIELD_RANGE(20, 27); //

        /*****************************************************************************\
        The ISR is an active high pulse when the CRC completes a frame.
        \*****************************************************************************/
        DDU32 Cdclk_Crc_Done : DD_BITFIELD_BIT(28); //

        /*****************************************************************************\
        The ISR is an active high pulse when a completed CRC mismatches with the expected value.
        \*****************************************************************************/
        DDU32 Cdclk_Crc_Error : DD_BITFIELD_BIT(29); //

        /*****************************************************************************\
        The ISR is an active high pulse on the eDP/DP Variable Refresh Rate double buffer update event&amp;#160;on this pipe.
        \*****************************************************************************/
        DDU32 VrrDoubleBufferUpdate : DD_BITFIELD_BIT(30); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is an underrun on the transcoder attached to this pipe.
        \*****************************************************************************/
        DDU32 UnderRun : DD_BITFIELD_BIT(31); //
    };
    DDU32 Value;

} DE_PIPE_INTR_TABLE_CNL;

C_ASSERT(4 == sizeof(DE_PIPE_INTR_TABLE_CNL));

// IMPLICIT ENUMERATIONS USED BY DE_MISC_INTR_TABLE_CNL
//
typedef enum _DE_MISC_INTR_INSTANCE_CNL
{
    DE_MISC_INTR_ADDR_CNL = 0x44460,
} DE_MISC_INTR_INSTANCE_CNL;

typedef enum _DE_MISC_INTR_CNL
{
    DE_MISC_INTR_WO_CNL  = 0x0,
    DE_MISC_INTR_PBC_CNL = 0x0,
    DE_MISC_INTR_MBZ_CNL = 0x37EFE,
} DE_MISC_INTR_CNL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Display Engine Miscellaneous Interrupt registers.
The IER enabled Display Engine Miscellaneous Interrupt IIR (sticky) bits are ORed together to generate the DE_Misc Interrupts Pending bit in the Master Interrupt Control register.

0x44460 = ISR
0x44464 = IMR
0x44468 = IIR
0x4446C = IER
\*****************************************************************************/
typedef union _DE_MISC_INTR_TABLE_CNL {
    struct
    {

        /*****************************************************************************\
        The ISR is an active high pulse on receiving the pinning user interrupt.
        \*****************************************************************************/
        DDU32 PinningEngineUserInterrupt : DD_BITFIELD_BIT(0); //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(1, 7);  // MBZ

        /*****************************************************************************\
        The ISR is an active high pulse on receiving the pinning context switch interrupt.
        \*****************************************************************************/
        DDU32 PinningEngineContextSwitch : DD_BITFIELD_BIT(8); //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(9, 14); // MBZ

        /*****************************************************************************\
        The ISR is an active high level while any of the GTC_IIR bits are set.
        \*****************************************************************************/
        DDU32 Gtc_Interrupts_Combined : DD_BITFIELD_BIT(15);    //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(16, 17); // MBZ

        /*****************************************************************************\
        The ISR is an active high level while any of the WD1_IIR bits are set.
        \*****************************************************************************/
        DDU32 Wd1_Interrupts_Combined : DD_BITFIELD_BIT(18); //

        /*****************************************************************************\
        The ISR is an active high level while any of the SRD_IIR bits are set.
        \*****************************************************************************/
        DDU32 Srd_Interrupts_Combined : DD_BITFIELD_BIT(19); //

        /*****************************************************************************\
        The ISR is an active high pulse on receiving the iMPH SVM Device Mode Wait Descriptor Completion indication.
        This event indicates that IMPH completed Invalidation Wait Descriptor.
        \*****************************************************************************/
        DDU32 SvmDeviceModeWaitDescriptorCompletion : DD_BITFIELD_BIT(20); //

        /*****************************************************************************\
        The ISR is an active high pulse on receiving the iMPH SVM Device Mode VT-d fault indication.
        This event indicates GT encountered a non-recoverable translation fault.
        \*****************************************************************************/
        DDU32 SvmDeviceModeVtdFault : DD_BITFIELD_BIT(21); //

        /*****************************************************************************\
        The ISR is an active high pulse on receiving the iMPH SVM Device Mode PRQ event indication.
        This event indicates that a GT advanced context encountered a recoverable page fault.
        \*****************************************************************************/
        DDU32 SvmDeviceModePrqEvent : DD_BITFIELD_BIT(22); //

        /*****************************************************************************\
        The ISR is an active high level while any of the WD0_IIR bits are set.
        \*****************************************************************************/
        DDU32 Wd0_Interrupts_Combined : DD_BITFIELD_BIT(23); //

        /*****************************************************************************\
        The ISR is an active high pulse on the DMC interrupt event.
        \*****************************************************************************/
        DDU32 Dmc_Interrupt_Event : DD_BITFIELD_BIT(24); //

        /*****************************************************************************\
        The ISR is an active high pulse on the DMC error event.
        \*****************************************************************************/
        DDU32 Dmc_Error : DD_BITFIELD_BIT(25); //

        /*****************************************************************************\
        This interrupt is no longer used.
        \*****************************************************************************/
        DDU32 CameraInterruptEvent : DD_BITFIELD_BIT(26); //

        /*****************************************************************************\
        The ISR is an active high pulse on the GSE system level event.
        \*****************************************************************************/
        DDU32 Gse : DD_BITFIELD_BIT(27); //

        /*****************************************************************************\
        The ISR is an active high pulse on receiving the iMPH invalid page table entry data indication.
        \*****************************************************************************/
        DDU32 Invalid_Page_Table_Entry_Data : DD_BITFIELD_BIT(28); //

        /*****************************************************************************\
        The ISR is an active high pulse on receiving the iMPH invalid GTT page table entry indication.
        \*****************************************************************************/
        DDU32 Invalid_Gtt_Page_Table_Entry : DD_BITFIELD_BIT(29); //

        /*****************************************************************************\
        The ISR is an active high level while any of the ECC Double Error status bits are set.
        \*****************************************************************************/
        DDU32 Ecc_Double_Error : DD_BITFIELD_BIT(30); //

        /*****************************************************************************\
        The ISR is an active high pulse on receiving the poison response to a memory transaction.
        \*****************************************************************************/
        DDU32 Poison : DD_BITFIELD_BIT(31); //
    };
    DDU32 Value;

} DE_MISC_INTR_TABLE_CNL;

C_ASSERT(4 == sizeof(DE_MISC_INTR_TABLE_CNL));

// IMPLICIT ENUMERATIONS USED BY AUDIO_CODEC_INTR_TABLE_CNL
//
typedef enum _AUDIO_CODEC_INTR_INSTANCE_CNL
{
    AUDIO_CODEC_INTR_ADDR_CNL = 0x44480,
} AUDIO_CODEC_INTR_INSTANCE_CNL;

typedef enum _AUDIO_CODEC_INTR_CNL
{
    AUDIO_CODEC_INTR_WO_CNL  = 0x0,
    AUDIO_CODEC_INTR_MBZ_CNL = 0x0,
    AUDIO_CODEC_INTR_PBC_CNL = 0x0,
} AUDIO_CODEC_INTR_CNL;

/*****************************************************************************\
This table indicates which events are mapped to each bit of the Audio Codec Interrupt registers.
The IER enabled Audio Codec Interrupt IIR (sticky) bits are ORed together to generate the Audio Codec Interrupts Pending bit in the Master Interrupt Control register.

0x44480 = ISR
0x44484 = IMR
0x44488 = IIR
0x4448C = IER
\*****************************************************************************/
typedef union _AUDIO_CODEC_INTR_TABLE_CNL {
    struct
    {

        /*****************************************************************************\
        The ISR is an active high pulse when there is a write to any of the four Audio Mail box verbs in vendor defined node ID 8
        \*****************************************************************************/
        DDU32 Audio_Mailbox_Write : DD_BITFIELD_BIT(0); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for transcoder A.
        \*****************************************************************************/
        DDU32 Audio_Cp_Change_Transcoder_A : DD_BITFIELD_BIT(1); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder A.
        It is valid after the Audio_CP_Change_Transcoder_A event has occurred.
        \*****************************************************************************/
        DDU32 Audio_Cp_Request_Transcoder_A : DD_BITFIELD_BIT(2); //

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        DDU32 Unused_Int_4_3 : DD_BITFIELD_RANGE(3, 4); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for transcoder B.
        \*****************************************************************************/
        DDU32 Audio_Cp_Change_Transcoder_B : DD_BITFIELD_BIT(5); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder B.
        It is valid after the Audio_CP_Change_Transcoder_B event has occurred.
        \*****************************************************************************/
        DDU32 Audio_Cp_Request_Transcoder_B : DD_BITFIELD_BIT(6); //

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        DDU32 Unused_Int_8_7 : DD_BITFIELD_RANGE(7, 8); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for transcoder C.
        \*****************************************************************************/
        DDU32 Audio_Cp_Change_Transcoder_C : DD_BITFIELD_BIT(9); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for transcoder C.
        It is valid after the Audio_CP_Change_Transcoder_C event has occurred.
        \*****************************************************************************/
        DDU32 Audio_Cp_Request_Transcoder_C : DD_BITFIELD_BIT(10); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for DDI F.
        \*****************************************************************************/
        DDU32 Audio_Power_State_Change_Ddi_F : DD_BITFIELD_BIT(11); //

        /*****************************************************************************\
        This interrupt is currently unused.
        \*****************************************************************************/
        DDU32 Unused_Int_12 : DD_BITFIELD_BIT(12); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for WD 0.
        \*****************************************************************************/
        DDU32 Audio_Cp_Change_Wd_0 : DD_BITFIELD_BIT(13); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for WD 0.
        It is valid after the Audio_CP_Change_WD_0 event has occurred.
        \*****************************************************************************/
        DDU32 Audio_Cp_Request_Wd_0 : DD_BITFIELD_BIT(14); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a change in the protection request from audio azalia verb programming for WD 1.
        \*****************************************************************************/
        DDU32 Audio_Cp_Change_Wd_1 : DD_BITFIELD_BIT(15); //

        /*****************************************************************************\
        The ISR is an active high level indicating content protection is requested by audio azalia verb programming for WD 0.
        It is valid after the Audio_CP_Change_WD_1 event has occurred.
        \*****************************************************************************/
        DDU32 Audio_Cp_Request_Wd_1 : DD_BITFIELD_BIT(16); //

        /*****************************************************************************\
        The ISR is an active high level indicating an overflow in the Audio Wireless slice 0 RAM.
        \*****************************************************************************/
        DDU32 Audio_Ramfull_Error_Wd_0 : DD_BITFIELD_BIT(17); //

        /*****************************************************************************\
        The ISR is an active high level indicating an overflow in the Audio Wireless slice 1 RAM.
        \*****************************************************************************/
        DDU32 Audio_Ramfull_Error_Wd_1 : DD_BITFIELD_BIT(18); //

        /*****************************************************************************\
        These interrupts are currently unused.
        \*****************************************************************************/
        DDU32 Unused_Int_26_19 : DD_BITFIELD_RANGE(19, 26); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for WD 1.
        \*****************************************************************************/
        DDU32 Audio_Power_State_Change_Wd_1 : DD_BITFIELD_BIT(27); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for WD 0.
        \*****************************************************************************/
        DDU32 Audio_Power_State_Change_Wd_0 : DD_BITFIELD_BIT(28); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for DDI B.
        \*****************************************************************************/
        DDU32 Audio_Power_State_Change_Ddi_B : DD_BITFIELD_BIT(29); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for DDI C.
        \*****************************************************************************/
        DDU32 Audio_Power_State_Change_Ddi_C : DD_BITFIELD_BIT(30); //

        /*****************************************************************************\
        The ISR is an active high pulse when there is a power state change for audio for DDI D.
        \*****************************************************************************/
        DDU32 Audio_Power_State_Change_Ddi_D : DD_BITFIELD_BIT(31); //
    };
    DDU32 Value;

} AUDIO_CODEC_INTR_TABLE_CNL;

C_ASSERT(4 == sizeof(AUDIO_CODEC_INTR_TABLE_CNL));

// IMPLICIT ENUMERATIONS USED BY SOUTH_DE_INTR_BIT_DEFINITION_SPT
//
typedef enum _SOUTH_DE_INTR_INSTANCE_SPT
{
    SOUTH_DE_ISR_ADDR_SPT = 0xC4000,
    SOUTH_DE_IMR_ADDR_SPT = 0xC4004,
    SOUTH_DE_IIR_ADDR_SPT = 0xC4008,
    SOUTH_DE_IER_ADDR_SPT = 0xC400C,
} SOUTH_DE_INTR_INSTANCE_SPT;

typedef enum __SOUTH_DE_INTR_BIT_SPT
{
    _SOUTH_DE_INTR_BIT_MBZ_SPT = 0xFC1DF000,
    _SOUTH_DE_INTR_BIT_WO_SPT  = 0x0,
    _SOUTH_DE_INTR_BIT_PBC_SPT = 0x0,
} _SOUTH_DE_INTR_BIT_SPT;

/*****************************************************************************\
South Display Engine (SDE) interrupt bits come from events within the south display engine.
The SDE_IIR bits are ORed together to generate the South/PCH Display Interrupt Event which will appear in the North Display Engine Interrupt Control Registers.

The South Display Engine Interrupt Control Registers all share the same bit definitions from this table.
\*****************************************************************************/
typedef union _SOUTH_DE_INTR_BIT_DEFINITION_SPT {
    struct
    {
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(0, 6); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected and is cleared by writing a '1' to this bit.
        The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        DDU32 ScdcReadRequestInterruptPortE : DD_BITFIELD_BIT(7); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected and is cleared by writing a '1' to this bit.
        The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        DDU32 ScdcReadRequestInterruptPortB : DD_BITFIELD_BIT(8); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected and is cleared by writing a '1' to this bit.
        The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        DDU32 ScdcReadRequestInterruptPortC : DD_BITFIELD_BIT(9); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected and is cleared by writing a '1' to this bit.
        The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        DDU32 ScdcReadRequestInterruptPortD : DD_BITFIELD_BIT(10); //

        /*****************************************************************************\
        The IIR is set when a HDMI 2.0 SCDC read request event is detected and is cleared by writing a '1' to this bit.
        The ISR is active high level signal that will indicate if the read request (RR) is still active.
        \*****************************************************************************/
        DDU32 ScdcReadRequestInterruptPortF : DD_BITFIELD_BIT(11); //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(12, 16);    // MBZ

        /*****************************************************************************\
        This is an active high pulse when any of the events unmasked events in GMBUS4 Interrupt Mask register occur.
        \*****************************************************************************/
        DDU32 Gmbus : DD_BITFIELD_BIT(17);                      //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(18, 20); // MBZ

        /*****************************************************************************\
        The ISR is an active high level representing the Digital Port B hotplug line when the Digital Port B hotplug detect input is enabled.
        The IIR is set on either a short or long pulse detection status in the Digital Port Hot Plug Control Register.
        \*****************************************************************************/
        DDU32 DdiBHotplug : DD_BITFIELD_BIT(21); //

        /*****************************************************************************\
        The ISR is an active high level representing the Digital Port C hotplug line when the Digital Port C hotplug detect input is enabled.
        The IIR is set on either a short or long pulse detection status in the Digital Port Hot Plug Control Register.
        \*****************************************************************************/
        DDU32 DdiCHotplug : DD_BITFIELD_BIT(22); //

        /*****************************************************************************\
        The ISR is an active high level representing the Digital Port D hotplug line when the Digital Port D hotplug detect input is enabled.
        The IIR is set on either a short or long pulse detection status in the Digital Port Hot Plug Control Register.
        \*****************************************************************************/
        DDU32 DdiDHotplug : DD_BITFIELD_BIT(23); //

        /*****************************************************************************\
        The ISR is an active high level representing the Digital Port A hotplug line when the Digital Port A hotplug detect input is enabled.
        The IIR is set on either a short or long pulse detection status in the Digital Port Hot Plug Control Register.
        \*****************************************************************************/
        DDU32 DdiAHotplug : DD_BITFIELD_BIT(24); //

        /*****************************************************************************\
        The ISR is an active high level representing the Digital Port E hotplug line when the Digital Port E hotplug detect input is enabled.
        The IIR is set on either a short or long pulse detection status in the Digital Port Hot Plug Control Register.
        \*****************************************************************************/
        DDU32 DdiEHotplug : DD_BITFIELD_BIT(25);                //
        DDU32 DdiFHotplug : DD_BITFIELD_BIT(26);                //
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(27, 31); // MBZ
    };
    DDU32 Value;

} SOUTH_DE_INTR_BIT_DEFINITION_SPT;

C_ASSERT(4 == sizeof(SOUTH_DE_INTR_BIT_DEFINITION_SPT));

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL_SPT
//
typedef enum _SHOTPLUG_CTL_DDI_B_HPD_STATUS_SPT
{
    SHOTPLUG_CTL_DDI_B_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_SPT = 0x0,
} SHOTPLUG_CTL_DDI_B_HPD_STATUS_SPT;

typedef enum _SHOTPLUG_CTL_DDI_B_HPD_INPUT_ENABLE_SPT
{
    SHOTPLUG_CTL_DDI_B_HPD_INPUT_ENABLE_DISABLE_SPT = 0x0,
    SHOTPLUG_CTL_DDI_B_HPD_INPUT_ENABLE_ENABLE_SPT  = 0x1,
} SHOTPLUG_CTL_DDI_B_HPD_INPUT_ENABLE_SPT;

typedef enum _SHOTPLUG_CTL_DDI_C_HPD_STATUS_SPT
{
    SHOTPLUG_CTL_DDI_C_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_SPT = 0x0,
} SHOTPLUG_CTL_DDI_C_HPD_STATUS_SPT;

typedef enum _SHOTPLUG_CTL_DDI_C_HPD_INPUT_ENABLE_SPT
{
    SHOTPLUG_CTL_DDI_C_HPD_INPUT_ENABLE_DISABLE_SPT = 0x0,
    SHOTPLUG_CTL_DDI_C_HPD_INPUT_ENABLE_ENABLE_SPT  = 0x1,
} SHOTPLUG_CTL_DDI_C_HPD_INPUT_ENABLE_SPT;

typedef enum _SHOTPLUG_CTL_DDI_D_HPD_STATUS_SPT
{
    SHOTPLUG_CTL_DDI_D_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_SPT = 0x0,
} SHOTPLUG_CTL_DDI_D_HPD_STATUS_SPT;

typedef enum _SHOTPLUG_CTL_DDI_D_HPD_INPUT_ENABLE_SPT
{
    SHOTPLUG_CTL_DDI_D_HPD_INPUT_ENABLE_DISABLE_SPT = 0x0,
    SHOTPLUG_CTL_DDI_D_HPD_INPUT_ENABLE_ENABLE_SPT  = 0x1,
} SHOTPLUG_CTL_DDI_D_HPD_INPUT_ENABLE_SPT;

typedef enum _SHOTPLUG_CTL_DDI_A_HPD_STATUS_SPT
{
    SHOTPLUG_CTL_DDI_A_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_SPT = 0x0,
} SHOTPLUG_CTL_DDI_A_HPD_STATUS_SPT;

typedef enum _SHOTPLUG_CTL_DDI_A_HPD_INPUT_ENABLE_SPT
{
    SHOTPLUG_CTL_DDI_A_HPD_INPUT_ENABLE_DISABLE_SPT = 0x0,
    SHOTPLUG_CTL_DDI_A_HPD_INPUT_ENABLE_ENABLE_SPT  = 0x1,
} SHOTPLUG_CTL_DDI_A_HPD_INPUT_ENABLE_SPT;

typedef enum _SOUTH_HOT_PLUG_CTL_INSTANCE_SPT
{
    SOUTH_HOT_PLUG_CTL_ADDR_SPT = 0xC4030,
} SOUTH_HOT_PLUG_CTL_INSTANCE_SPT;

typedef enum __SHOTPLUG_CTL_MASKS_SPT
{
    _SHOTPLUG_CTL_MASKS_MBZ_SPT = 0xECECECEC,
    _SHOTPLUG_CTL_MASKS_WO_SPT  = 0x0,
    _SHOTPLUG_CTL_MASKS_PBC_SPT = 0x0,
} _SHOTPLUG_CTL_MASKS_SPT;

/*****************************************************************************\
The short pulse duration is programmed in SHPD_PULSE_CNT.
\*****************************************************************************/
typedef union _SHOTPLUG_CTL_SPT {
    struct
    {

        /*****************************************************************************\
        This field reflects the hot plug detect status on port B.  This bit is used for either monitor hotplug/unplug or for notification of a sink event.
        When HPD input is enabled and either a long or short pulse is detected, one of these bits will set and the hotplug IIR will be set (if unmasked in the IMR).
        The hotplug ISR gives the live state of the HPD pin.
        These are sticky bits, cleared by writing 1s to both of them.
        \*****************************************************************************/
        DDU32 DdiBHpdStatus : DD_BITFIELD_RANGE(0, 1);        // SHOTPLUG_CTL_DDI_B_HPD_STATUS_SPT
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(2, 3); // MBZ

        /*****************************************************************************\
        This field controls the state of the HPD pin for the digital port B.
        \*****************************************************************************/
        DDU32 DdiBHpdInputEnable : DD_BITFIELD_BIT(4);        // SHOTPLUG_CTL_DDI_B_HPD_INPUT_ENABLE_SPT
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(5, 7); // MBZ

        /*****************************************************************************\
        This field reflects the hot plug detect status on port C.
        This bit is used for either monitor hotplug/unplug or for notification of a sink event.
        When HPD input is enabled and either a long or short pulse is detected,
        one of these bits will set and the hotplug IIR will be set (if unmasked in the IMR).
        The hotplug ISR gives the live state of the HPD pin.
        These are sticky bits, cleared by writing 1s to both of them.
        \*****************************************************************************/
        DDU32 DdiCHpdStatus : DD_BITFIELD_RANGE(8, 9);          // SHOTPLUG_CTL_DDI_C_HPD_STATUS_SPT
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(10, 11); // MBZ

        /*****************************************************************************\
        This field controls the state of the HPD pin for the digital port C.
        \*****************************************************************************/
        DDU32 DdiCHpdInputEnable : DD_BITFIELD_BIT(12);         // SHOTPLUG_CTL_DDI_C_HPD_INPUT_ENABLE_SPT
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(13, 15); // MBZ

        /*****************************************************************************\
        This field reflects the hot plug detect status on port D.
        This bit is used for either monitor hotplug/unplug or for notification of a sink event.
        When HPD input is enabled and either a long or short pulse is detected,
        one of these bits will set and the hotplug IIR will be set (if unmasked in the IMR).
        The hotplug ISR gives the live state of the HPD pin.
        These are sticky bits, cleared by writing 1s to both of them.
        \*****************************************************************************/
        DDU32 DdiDHpdStatus : DD_BITFIELD_RANGE(16, 17);        // SHOTPLUG_CTL_DDI_D_HPD_STATUS_SPT
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(18, 19); // MBZ

        /*****************************************************************************\
        This field controls the state of the HPD pin for the digital port D.
        \*****************************************************************************/
        DDU32 DdiDHpdInputEnable : DD_BITFIELD_BIT(20);         // SHOTPLUG_CTL_DDI_D_HPD_INPUT_ENABLE_SPT
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(21, 23); // MBZ

        /*****************************************************************************\
        This field reflects the hot plug detect status on port A.
        This bit is used for either monitor hotplug/unplug or for notification of a sink event.
        When HPD input is enabled and either a long or short pulse is detected,
        one of these bits will set and the hotplug IIR will be set (if unmasked in the IMR).
        The hotplug ISR gives the live state of the HPD pin.
        These are sticky bits, cleared by writing 1s to both of them.
        \*****************************************************************************/
        DDU32 DdiAHpdStatus : DD_BITFIELD_RANGE(24, 25);        // SHOTPLUG_CTL_DDI_A_HPD_STATUS_SPT
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(26, 27); // MBZ

        /*****************************************************************************\
        This field controls the state of the HPD pin for the digital port A.
        \*****************************************************************************/
        DDU32 DdiAHpdInputEnable : DD_BITFIELD_BIT(28);         // SHOTPLUG_CTL_DDI_A_HPD_INPUT_ENABLE_SPT
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(29, 31); // MBZ
    };
    DDU32 Value;

} SHOTPLUG_CTL_SPT;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL_SPT));

// IMPLICIT ENUMERATIONS USED BY SHOTPLUG_CTL2_SPT
//
typedef enum _DDI_E_HPD_STATUS_SPT
{
    DDI_E_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_SPT = 0x0,
} DDI_E_HPD_STATUS_SPT;

typedef enum _DDI_E_HPD_OUTPUT_DATA_SPT
{
    DDI_E_HPD_OUTPUT_DATA_DRIVE_0_SPT = 0x0,
    DDI_E_HPD_OUTPUT_DATA_DRIVE_1_SPT = 0x1,
} DDI_E_HPD_OUTPUT_DATA_SPT;

typedef enum _DDI_E_HPD_INPUT_ENABLE_SPT
{
    DDI_E_HPD_INPUT_ENABLE_DISABLE_SPT = 0x0,
    DDI_E_HPD_INPUT_ENABLE_ENABLE_SPT  = 0x1,
} DDI_E_HPD_INPUT_ENABLE_SPT;

typedef enum _DDI_F_HPD_STATUS_SPT
{
    DDI_F_HPD_STATUS_HOT_PLUG_EVENT_NOT_DETECTED_SPT = 0x0,
} DDI_F_HPD_STATUS_SPT;

typedef enum _DDI_F_HDP_OUTPUT_DATA_SPT
{
    DDI_F_HDP_OUTPUT_DATA_DRIVE_0_SPT = 0x0,
    DDI_F_HDP_OUTPUT_DATA_DRIVE_1_SPT = 0x1,
} DDI_F_HDP_OUTPUT_DATA_SPT;

typedef enum _DDI_F_HPD_INPUT_ENABLE_SPT
{
    DDI_F_HPD_INPUT_ENABLE_DISABLE_SPT = 0x0,
    DDI_F_HPD_INPUT_ENABLE_ENABLE_SPT  = 0x1,
} DDI_F_HPD_INPUT_ENABLE_SPT;

typedef enum _SOUTH_HOT_PLUG_CTL_2_INSTANCE_SPT
{
    SOUTH_HOT_PLUG_CTL_2_ADDR_SPT = 0xC403C,
} SOUTH_HOT_PLUG_CTL_2_INSTANCE_SPT;

typedef enum _SHOTPLUG_CTL2_MASKS_SPT
{
    SHOTPLUG_CTL2_MASKS_MBZ_SPT = 0xFFFFFE0C,
    SHOTPLUG_CTL2_MASKS_WO_SPT  = 0x0,
    SHOTPLUG_CTL2_MASKS_PBC_SPT = 0x0,
} SHOTPLUG_CTL2_MASKS_SPT;

/*****************************************************************************\
Each HPD pin can be configured as an input or output.  The HPD input and status functions will only work when the pin is configured as an input.
The HPD Output Data function will only work when the HPD pin is configured as an output.The short pulse duration is programmed in SHPD_PULSE_CNT.
\*****************************************************************************/
typedef union _SHOTPLUG_CTL2_SPT {
    struct
    {

        /*****************************************************************************\
        This field reflects the hot plug detect status on port E.  This bit is used for either monitor hotplug/unplug or for notification of a sink event.
        When HPD input is enabled and either a long or short pulse is detected, one of these bits will set and the hotplug IIR will be set (if unmasked in the IMR).
        The hotplug ISR gives the live state of the HPD pin.
        These are sticky bits, cleared by writing 1s to both of them.

        On boards that are using DDI F, this field reflects the hot plug detect status on port F. This bit is used for either monitor hotplug/unplug or for notification of a sink
        event. When HPD input is enabled and either a long or short pulse is detected, one of these bits will set and the hotplug IIR will be set (if unmasked in the IMR). The
        hotplug ISR gives the live state of the HPD pin. These are sticky bits, cleared by writing 1s to both of them.
        \*****************************************************************************/
        DDU32 DdiEHpdStatus : DD_BITFIELD_RANGE(0, 1);   // DDI_E_HPD_STATUS_SPT
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_BIT(2); // MBZ

        /*****************************************************************************\
        This field drives an output on the HPD pin for the digital port E.

        On boards that are using DDI F, this field drives an output on the HPD pin for the digital port F.
        \*****************************************************************************/
        DDU32 DdiEHpdOutputData : DD_BITFIELD_BIT(3); // DDI_E_HPD_OUTPUT_DATA_SPT
        /*****************************************************************************\
        This field controls the state of the HPD buffer for the digital port E.

        On boards that are using DDI F, this field controls the state of the HPD buffer for the digital port F.
        \*****************************************************************************/
        DDU32 DdiEHpdInputEnable : DD_BITFIELD_BIT(4); // DDI_E_HPD_INPUT_ENABLE_SPT

        /*****************************************************************************\
        This field reflects the hot plug detect status on port F. This bit is used for either monitor hotplug/unplug or for notification of a sink event.
        When HPD input is enabled and either a long or short pulse is detected, one of these bits will set and the hotplug IIR will be set (if unmasked in the IMR).
        The hotplug ISR gives the live state of the HPD pin. These are sticky bits, cleared by writing 1s to both of them.
        \*****************************************************************************/
        DDU32 DdiFHpdStatus : DD_BITFIELD_RANGE(5, 6); // DDI_F_HPD_STATUS_SPT
        /*****************************************************************************\
        This field drives an output on the HPD pin for the digital port F.
        \*****************************************************************************/
        DDU32 DdiFHdpOutputData : DD_BITFIELD_BIT(7); // DDI_F_HDP_OUTPUT_DATA_SPT
        /*****************************************************************************\
        This field controls the state of the HPD buffer for the digital port F.
        \*****************************************************************************/
        DDU32 DdiFHpdInputEnable : DD_BITFIELD_BIT(8);         // DDI_F_HPD_INPUT_ENABLE_SPT
        DDU32 UNIQUENAME(Reserved) : DD_BITFIELD_RANGE(9, 31); // MBZ
    };
    DDU32 Value;

} SHOTPLUG_CTL2_SPT;

C_ASSERT(4 == sizeof(SHOTPLUG_CTL2_SPT));

#endif // GEN10INTRREGS_H
