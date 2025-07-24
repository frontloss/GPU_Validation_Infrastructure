
#include "Gen14CommonMMIO.h"
#include "..\..\DriverInterfaces\SimDrvToGfx.h"

BOOLEAN GEN14_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    GFX_MSTR_INTR_GEN14 stMasterIntCtrl = { 0 };
    stMasterIntCtrl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stMasterIntCtrl.MasterInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                   // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stMasterIntCtrl.Value;

    return TRUE;
}

BOOLEAN GEN14_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN14 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN14)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    GFX_MSTR_INTR_GEN14 stMasterIntCtrlTemp = { 0 };

    stMasterIntCtrlTemp.Value               = ulWriteData;
    pstMasterIntCtrl->MasterInterruptEnable = stMasterIntCtrlTemp.MasterInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN14_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    DISPLAY_INT_CTL_GEN14 stDisplayIntCtrl = { 0 };
    stDisplayIntCtrl.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stDisplayIntCtrl.DisplayInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                     // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stDisplayIntCtrl.ulValue;

    return TRUE;
}

BOOLEAN GEN14_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PDISPLAY_INT_CTL_GEN14 stDisplayIntCtrl =
    (PDISPLAY_INT_CTL_GEN14)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    DISPLAY_INT_CTL_GEN14 stDisplayIntCtrlTemp = { 0 };

    stDisplayIntCtrlTemp.ulValue             = ulWriteData;
    stDisplayIntCtrl->DisplayInterruptEnable = stDisplayIntCtrlTemp.DisplayInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN14_CMN_MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN14 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN14)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN14 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 *pstPCHIIRReg    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14  stPCHIIRRegTemp = { 0 };
    pstPCHIIRReg =
    (SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.ulValue = ulWriteData;

    if (stPCHIIRRegTemp.ulValue != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        pstPCHIIRReg->ulValue &= ~stPCHIIRRegTemp.ulValue;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN14_CMN_MMIOHANDLERS_PICAMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
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

BOOLEAN GEN14_CMN_MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN14 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN14)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN14 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];

    PICA_INTERRUPT_DEFINTION_GEN14 *stPICAIIRReg     = { 0 };
    PICA_INTERRUPT_DEFINTION_GEN14  stPICAIIRRegTemp = { 0 };

    stPICAIIRReg =
    (PICA_INTERRUPT_DEFINTION_GEN14 *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];

    stPICAIIRRegTemp.ulValue = ulWriteData;
    if (stPICAIIRRegTemp.ulValue != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        stPICAIIRReg->ulValue &= ~stPICAIIRRegTemp.ulValue;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN14_CMN_MMIOHANDLERS_GetLanesAssignedfromphyMMIOReadHandlers(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                       PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                    bRet                = FALSE;
    PORT_TX_DFLEXPA1_D14       LaneData            = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
        LaneData.Value      = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

        LaneData.DisplayportPinAssignmentForTypeCConnector0 = DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C_D14;
        LaneData.DisplayportPinAssignmentForTypeCConnector1 = DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C_D14;

        *pulReadData                                                                                              = LaneData.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = LaneData.Value;
        bRet                                                                                                      = TRUE;

    } while (FALSE);
    return bRet;
}

BOOLEAN GEN14_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                     PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN            bRet            = TRUE;
    PORT_BUF_CTL1_D14  Port_Buf        = { 0 };
    PSIMDEV_EXTENTSION pstSimDrvDevExt = GetSimDrvExtension();

    ULONG driverRegValue = 0;
    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, ulMMIOOffset, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        Port_Buf.Value       = driverRegValue;
        Port_Buf.SocPhyReady = 1;

        *pulReadData = Port_Buf.Value;
    }

    return bRet;
}