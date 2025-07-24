/**********************************************************************************************************
HPD Flow

MASTER_CTL_INT(0x190010) - MasterInterruptRW[Gfx IP or others] Get the Interrupt Source ie Display Interrupt
DISPLAY_INTR_CTL_ADDR_ICL(0x44200) - DisplayInterruptRW[Display, GPU or Render] Get the Legacy Interrupt Source means is it HPD/Port/Pipe/Audio
SOUTH_DE_IIR_ADDR_SPT(0xC4008) - HotPlugIIRWrite[Pipe or Port interrupt Interrupt Source ie PCH Display]
SOUTH_HOT_PLUG_CTL_ADDR_SPT(0xC4030) - HotPlugCTLWrite[Which port is being connected? Short or Long Pulse]
SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL(0xC4034) - HotPlugCTLWrite[Which port is being connected? Short or Long Pulse]
SOUTH_DE_ISR_ADDR_SPT(0xc4000) - HotPlugLiveStateRead[Connected / Disconnected]

DE_HPD_INTR_ADDR(0x44470) + 0x8 - DEHotPlugIIRWrite[Pipe or Port interrupt]
THUNDERBOLD_HOT_PLUG_CTL_ADDR_ICL(0x44030) - TBTHotPlugCTLWrite[Which port is being connected? ]
TYPEC_HOT_PLUG_CTL_ADDR_ICL(0x44038) - TypeCHotPlugCTLWrite[Which port is being connected? ]
DE_HPD_INTR_ADDR(0x44470) + 0x0 - DEHotLiveStateRead[Connected / Disconnected]

Call Flow: Gfx Mainline Driver: Legacy:
1. GEN13INTRHANDLER_GetInterruptSource  ---> case GEN13_DISPLAY_INTERRUPT_BIT_POS --> LegacyInterruptsOccurred Flag should be set
2. GEN13INTRHANDLER_GetLegacyInterruptSource
3. GEN13INTRHANDLER_GetHPDInterruptSource

********************************************************************************************************/

/** VBT port-BSpec DDI naming convention/mapping.
HPD Register mapping per port
Phy mapping per port for Gen13 Platforms **/
/******************************************************************************************************
                    ADL                         ||            DG2
VBT
Port         Bspec DDI     | HPD         | PHY  ||  Bspec DDI      | HPD       | PHY    | Type
----------------------------------------------------------------------------------------
A           A:   0x64000   | A:0xC4030   |Combo ||  A:   0x64000   | A:0xC4030 | Snps   | Combo

B           B:   0x64100   | B:0xC4030   |Combo ||  B:   0x64100   | B:0xC4030 | Snps   | Combo

C           C:   Rsvd                           ||  C:   0x64200   | C:0xC4030 | Snps   | Combo

D           D:   Rsvd                           ||  D:   0x64700   | E:0xC4030 | Snps   | Combo

E           E:   Rsvd                           || Rsvd

F           TC1: 0x64300   | TC1:0xC4034 |Dkl   ||  TC1: 0x64300   | D:0x44030 | Snps   | TypeC

G           TC2: 0x64400   | TC2:0xC4034 |Dkl   ||

H           TC3: 0x64500   | TC3:0xC4034 |Dkl   ||

I           TC4: 0x64600   | TC4:0xC4034 |Dkl   ||

*****************************************************************************************/

#include "Gen13CommonMMIO.h"

BOOLEAN GEN13_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    GFX_MSTR_INTR_GEN13 stMasterIntCtrl = { 0 };
    stMasterIntCtrl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stMasterIntCtrl.MasterInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                   // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stMasterIntCtrl.Value;

    return TRUE;
}

BOOLEAN GEN13_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN13 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN13)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    GFX_MSTR_INTR_GEN13 stMasterIntCtrlTemp = { 0 };

    stMasterIntCtrlTemp.Value               = ulWriteData;
    pstMasterIntCtrl->MasterInterruptEnable = stMasterIntCtrlTemp.MasterInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN13_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    DISPLAY_INT_CTL_GEN13 stDisplayIntCtrl = { 0 };
    stDisplayIntCtrl.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stDisplayIntCtrl.DisplayInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                     // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stDisplayIntCtrl.ulValue;

    return TRUE;
}

BOOLEAN GEN13_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PDISPLAY_INT_CTL_GEN13 stDisplayIntCtrl =
    (PDISPLAY_INT_CTL_GEN13)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    DISPLAY_INT_CTL_GEN13 stDisplayIntCtrlTemp = { 0 };

    stDisplayIntCtrlTemp.ulValue             = ulWriteData;
    stDisplayIntCtrl->DisplayInterruptEnable = stDisplayIntCtrlTemp.DisplayInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN13_CMN_MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN13 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN13)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN13 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 *pstPCHIIRReg    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13  stPCHIIRRegTemp = { 0 };
    pstPCHIIRReg =
    (SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.ulValue = ulWriteData;

    if (stPCHIIRRegTemp.ulValue != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        pstPCHIIRReg->ulValue &= ~stPCHIIRRegTemp.ulValue;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN13_CMN_MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN13 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN13)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN13 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];

    DE_HPD_INTERRUPT_DEFINITION_D13 *pstPCHIIRReg    = { 0 }; // DE Interrupt IIR
    DE_HPD_INTERRUPT_DEFINITION_D13  stPCHIIRRegTemp = { 0 }; // DE Interrupt IIR

    pstPCHIIRReg =
    (DE_HPD_INTERRUPT_DEFINITION_D13 *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];

    stPCHIIRRegTemp.Value = ulWriteData;

    if (stPCHIIRRegTemp.Value != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        pstPCHIIRReg->Value &= ~stPCHIIRRegTemp.Value;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN13_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                    bRet                = FALSE;
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = ulWriteData;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN13_CMN_MMIOHANDLERS_GetPinAssignedfromphyMMIOReadHandlers(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                     PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                    bRet                = FALSE;
    PORT_TX_DFLEXPA1_D13       LaneData            = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
        LaneData.Value      = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

        LaneData.DisplayportPinAssignmentForTypeCConnector0 = DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C_D13;
        LaneData.DisplayportPinAssignmentForTypeCConnector1 = DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C_D13;

        *pulReadData                                                                                              = LaneData.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = LaneData.Value;
        bRet                                                                                                      = TRUE;

    } while (FALSE);
    return bRet;
}

/**-------------------------------------------------------------
 * @brief GEN13_CMN_MMIOHANDLERS_GetLanesAssignedfromDKLPhyMMIOReadHandler
 *
 * Description: Set the number of lanes assigned to display for Read MG Phy scratch register (DFLEXDPSP1)
 *       This call is valid only for MG Phy ports (DDI F/G/H/I) and Type-C connector
 *
 * TBD: This is a replacement for upfront link training to determine # lanes used in Type-C.
 *       Need to pass this info. up to Protocol.
 *-------------------------------------------------------------*/
BOOLEAN GEN13_CMN_MMIOHANDLERS_GetLanesAssignedfromDKLPhyMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                         PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    PORT_TX_DFLEXDPSP_D13      LaneData            = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
        LaneData.Value      = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Currently 4 lanes are assigned for all the Port Types
        // TODO:
        // 1) Based on Live State of a Port, Lane Values can be assigned to a particualr port
        // 2) Lane Values can be configured run time also.Run time configuration can be done through registry write/read
        // These two items will be taken up later after discussing with VCO

        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector0 = DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX30_D13;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector1 = DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX30_D13;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector2 = DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX30_D13;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector3 = DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX30_D13;

        *pulReadData = LaneData.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = LaneData.Value;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}
