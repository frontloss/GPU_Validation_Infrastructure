/**********************************************************************************************************
TGL HPD Flow

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
1. GEN12INTRHANDLER_GetInterruptSource  ---> case GEN12_DISPLAY_INTERRUPT_BIT_POS --> LegacyInterruptsOccurred Flag should be set
2. GEN12INTRHANDLER_GetLegacyInterruptSource
3. GEN12INTRHANDLER_GetHPDInterruptSource

********************************************************************************************************/

/** VBT port-BSpec DDI naming convention/mapping.
HPD Register mapping per port
Phy mapping per port for Gen12 Platforms **/
/******************************************************************************************************************************************************************************************
TGL                         ||            DG1                       ||              RKL                                       ||              LKFR
VBT
Port         Bspec DDI     | HPD         | PHY  ||  Bspec DDI      | HPD       | PHY    ||  Bspec DDI        HPD-TGLPCH   HPD-CMP-PCH    | PHY    ||  Bspec DDI      | HPD         |
PHY
---------------------------------------------------------------------------------------------------------------------------------
A           A:   0x640xx   | A:0xC4030   |Combo ||  A:   0x640xx   | A:0xC4030 | Combo  ||   A:   0x640xx   | A:0xC4030   | A:0xC4030    | Combo  ||  A:   0x640xx   | A:0xC4030   |
Combo

B           B:   0x641xx   | B:0xC4030   |Combo ||  B:   0x641xx   | B:0xC4030 | Combo  ||   B:   0x641xx   | B:0xC4030   | B:0xC4030    | Combo  ||  B:   0x641xx   | B:0xC4030   |
Combo

C           C:   0x642xx   | C:0xC4030   |Combo ||  TC1: 0x643xx   | C:0xC4030 | Combo  ||   TC1: 0x643xx   | TC1:0xC4034 | C:0xC4030    | Combo  ||  Follows TGL & Port C is not
used for LKF-R

D           TC1: 0x643xx   | TC1:0xC4034 |Dkl   ||  TC2: 0x644xx   | D:0xC4030 | Combo  ||   TC2: 0x644xx   | TC2:0xC4034 | D:0xC4030    | Combo  ||  TC1: 0x643xx   | TC1:0xC4034 |
Dkl

E           TC2: 0x644xx   | TC2:0xC4034 |Dkl   ||                                                                                                ||  TC2: 0x644xx   | TC2:0xC4034 |
Dkl


F           TC3: 0x645xx   | TC3:0xC4034 |Dkl   ||

G           TC4: 0x646xx   | TC4:0xC4034 |Dkl   ||

H           TC5: 0x647xx   | TC5:0xC4034 |Dkl   ||

I           TC6: 0x648xx   | TC6:0xC4034 |Dkl   ||

******************************************************************************************************************************************************/

#include "Gen12CommonMMIO.h"

BOOLEAN GEN12_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    GFX_MSTR_INTR_GEN12 stMasterIntCtrl = { 0 };
    stMasterIntCtrl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stMasterIntCtrl.MasterInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                   // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stMasterIntCtrl.Value;

    return TRUE;
}

BOOLEAN GEN12_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN12 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN12)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    GFX_MSTR_INTR_GEN12 stMasterIntCtrlTemp = { 0 };

    stMasterIntCtrlTemp.Value               = ulWriteData;
    pstMasterIntCtrl->MasterInterruptEnable = stMasterIntCtrlTemp.MasterInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN12_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    DISPLAY_INT_CTL_GEN12 stDisplayIntCtrl = { 0 };
    stDisplayIntCtrl.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stDisplayIntCtrl.DisplayInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                     // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stDisplayIntCtrl.ulValue;

    return TRUE;
}

BOOLEAN GEN12_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PDISPLAY_INT_CTL_GEN12 stDisplayIntCtrl =
    (PDISPLAY_INT_CTL_GEN12)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    DISPLAY_INT_CTL_GEN12 stDisplayIntCtrlTemp = { 0 };

    stDisplayIntCtrlTemp.ulValue             = ulWriteData;
    stDisplayIntCtrl->DisplayInterruptEnable = stDisplayIntCtrlTemp.DisplayInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN12_CMN_MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN12 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN12)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 *pstPCHIIRReg    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12  stPCHIIRRegTemp = { 0 };
    pstPCHIIRReg =
    (SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.ulValue = ulWriteData;

    if (stPCHIIRRegTemp.ulValue != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        pstPCHIIRReg->ulValue &= ~stPCHIIRRegTemp.ulValue;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN12_CMN_MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN12 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN12)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    DE_HPD_INTR_DEFINITION_GEN12 *pstPCHIIRReg    = { 0 }; // DE Interrupt IIR
    DE_HPD_INTR_DEFINITION_GEN12  stPCHIIRRegTemp = { 0 }; // DE Interrupt IIR

    pstPCHIIRReg =
    (DE_HPD_INTR_DEFINITION_GEN12 *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.ulValue = ulWriteData;

    if (stPCHIIRRegTemp.ulValue != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        pstPCHIIRReg->ulValue &= ~stPCHIIRRegTemp.ulValue;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

// This function needs to be revisited once Gfx Driver code for TYPEC/TBT code is fianlised
// This may or may not be needed
BOOLEAN GEN12_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    PORT_TX_DFLEXDPPMS_GEN12   TypeCFiaStatus      = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData    = &pstMMIOHandlerInfo->stGlobalMMORegData;
        TypeCFiaStatus.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

        TypeCFiaStatus.ulValue = ulWriteData;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = TypeCFiaStatus.ulValue;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

/**-------------------------------------------------------------
 * @brief GEN12_CMN_MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler
 *
 * Description: Set the number of lanes assigned to display for Read MG Phy scratch register (DFLEXDPSP1)
 *       This call is valid only for MG Phy ports (DDI C/D/E/F) and Type-C connector
 *
 * TBD: This is a replacement for upfront link training to determine # lanes used in Type-C.
 *       Need to pass this info. up to Protocol.
 *-------------------------------------------------------------*/
BOOLEAN GEN12_CMN_MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                        PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    PORT_TX_DFLEXDPSP_GEN12    LaneData            = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
        LaneData.ulValue    = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // Setting ModularFia bit to 1 for the first instance of FIA i.e, DPSP1_FIA1;
        // This bit is static for a board and will be set by IOM FW
        // This will not be altered by Driver and will not change dynamically
        // Reference from : https://gfxspecs.intel.com/Predator/Home/Index/21563
        if ((ulMMIOOffset == PORT_TX_DFLEXDPSP1_FIA1_ADDR_GEN12) || (ulMMIOOffset == PORT_TX_DFLEXDPSP1_FIA2_ADDR_GEN12) || (ulMMIOOffset == PORT_TX_DFLEXDPSP1_FIA3_ADDR_GEN12))
        {
            LaneData.ModularFia_Mf = 1;
        }
        // Currently 4 lanes are assigned for all the Port Types
        // TODO:
        // 1) Based on Live State of a Port, Lane Values can be assigned to a particualr port
        // 2) Lane Values can be configured run time also.Run time configuration can be done through registry write/read
        // These two items will be taken up later after discussing with VCO

        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector0 = D12_PHY_TX3_TX2_TX1_TX0;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector1 = D12_PHY_TX3_TX2_TX1_TX0;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector2 = D12_PHY_TX3_TX2_TX1_TX0;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector3 = D12_PHY_TX3_TX2_TX1_TX0;

        *pulReadData = LaneData.ulValue;

        // The value of ulMMIOOffset will be either
        //	PORT_TX_DFLEXDPSP1_FIA1_ADDR_GEN12 = 0x1638A0,
        //	PORT_TX_DFLEXDPSP2_FIA1_ADDR_GEN12 = 0x1638A4,
        //	PORT_TX_DFLEXDPSP3_FIA1_ADDR_GEN12 = 0x1638A8,
        //	PORT_TX_DFLEXDPSP4_FIA1_ADDR_GEN12 = 0x1638AC,
        //	PORT_TX_DFLEXDPSP1_FIA2_ADDR_GEN12 = 0x16E8A0,
        //	PORT_TX_DFLEXDPSP2_FIA2_ADDR_GEN12 = 0x16E8A4,
        //	PORT_TX_DFLEXDPSP3_FIA2_ADDR_GEN12 = 0x16E8A8,
        //	PORT_TX_DFLEXDPSP4_FIA2_ADDR_GEN12 = 0x16E8AC,
        //	PORT_TX_DFLEXDPSP1_FIA3_ADDR_GEN12 = 0x16F8A0,
        //	PORT_TX_DFLEXDPSP2_FIA3_ADDR_GEN12 = 0x16F8A4,
        //	PORT_TX_DFLEXDPSP3_FIA3_ADDR_GEN12 = 0x16F8A8,
        //	PORT_TX_DFLEXDPSP4_FIA3_ADDR_GEN12 = 0x16F8AC,

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = LaneData.ulValue;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN12_CMN_MMIOHANDLERS_GetPinAssignedfromphyMMIOReadHandlers(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                     PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                    bRet                = FALSE;
    PORT_TX_DFLEXPA1_D12       LaneData            = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
        LaneData.Value      = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

        LaneData.DisplayportPinAssignmentForTypeCConnector0 = DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C_D12;
        LaneData.DisplayportPinAssignmentForTypeCConnector1 = DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C_D12;

        *pulReadData                                                                                              = LaneData.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = LaneData.Value;
        bRet                                                                                                      = TRUE;

    } while (FALSE);
    return bRet;
}
