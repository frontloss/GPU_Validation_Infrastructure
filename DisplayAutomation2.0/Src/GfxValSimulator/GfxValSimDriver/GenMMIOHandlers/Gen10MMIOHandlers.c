
#include "Gen10MMIO.h"
#include "..\\DriverInterfaces\\SIMDRV_GFX_COMMON.h"
#include ".\\CommonInclude\\ETWLogging.h"
#include "..\\..\\DriverInterfaces\\SimDrvToGfx.h"

BOOLEAN GEN10MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN GEN10LPMMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface);

BOOLEAN GEN10MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN10MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN10MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN10LPMMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN10MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN10LPMMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN10MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN10LPMMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN10MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType);

BOOLEAN GEN10MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {

        bRet = GEN10MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN10LPMMIOHANDLERS_RegisterGeneralMMIOHandHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {

        bRet = GEN10LPMMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);

    } while (FALSE);

    return bRet;
}

// dc
BOOLEAN GEN10MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    if (pstMMIOInterface)
    {
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_START] = DDI_AUX_DATA_A_START_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_END]   = DDI_AUX_DATA_A_END_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_A]        = DDI_AUX_CTL_A_CNL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_START] = DDI_AUX_DATA_B_START_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_END]   = DDI_AUX_DATA_B_END_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_B]        = DDI_AUX_CTL_B_CNL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = DDI_AUX_DATA_C_START_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = DDI_AUX_DATA_C_END_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = DDI_AUX_CTL_C_CNL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = DDI_AUX_DATA_D_START_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = DDI_AUX_DATA_D_END_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = DDI_AUX_CTL_D_CNL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_START] = DDI_AUX_DATA_E_START_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_END]   = DDI_AUX_DATA_E_END_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_E]        = DDI_AUX_CTL_E_CNL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_START] = DDI_AUX_DATA_F_START_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_END]   = DDI_AUX_DATA_F_END_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_F]        = DDI_AUX_CTL_F_CNL;

        // Every new offset should be added above this. So as to invalidate the rest
        // Do below: ulCount = [Last enum in above list] + 1;
        ulCount = eINDEX_DDI_AUX_CTL_F + 1;
        for (; ulCount < MAX_GEN_MMIO_OFFSETS_STORED; ulCount++)
        {
            pstMMIOInterface->pulGenMMIOOffsetArray[ulCount] = OFFSET_INVALID;
        }

        bRet = TRUE;
    }

    return bRet;
}

BOOLEAN GEN10LPMMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    if (pstMMIOInterface)
    {

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_START] = DDI_AUX_DATA_A_START_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_END]   = DDI_AUX_DATA_A_END_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_A]        = DDI_AUX_CTL_A_CNL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_START] = DDI_AUX_DATA_B_START_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_END]   = DDI_AUX_DATA_B_END_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_B]        = DDI_AUX_CTL_B_CNL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = DDI_AUX_DATA_C_START_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = DDI_AUX_DATA_C_END_CNL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = DDI_AUX_CTL_C_CNL;

        // Every new offset should be added above this. So as to invalidate the rest
        // Do below: ulCount = [Last enum in above list] + 1;
        ulCount = eINDEX_DDI_AUX_CTL_C + 1;
        for (; ulCount < MAX_GEN_MMIO_OFFSETS_STORED; ulCount++)
        {
            pstMMIOInterface->pulGenMMIOOffsetArray[ulCount] = OFFSET_INVALID;
        }

        bRet = TRUE;
    }

    return bRet;
}

BOOLEAN GEN10MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN                          bRet         = FALSE;
    SOUTH_DE_INTR_BIT_DEFINITION_SPT stPCHLiveReg = { 0 };
    stPCHLiveReg.DdiAHotplug                      = TRUE;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, MASTER_INTR_CTL_ADDR_CNL, MASTER_INTR_CTL_ADDR_CNL, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN10MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler, GEN10MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_HOT_PLUG_CTL_ADDR_SPT, SOUTH_HOT_PLUG_CTL_ADDR_SPT, stPCHLiveReg.Value, NULL, NULL, 0,
                                                       TRUE, eNoExecHw,
                                                       NULL, // reusing the GEN9 Handler since it just has to return the MMIO offset value
                                                       GEN10MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_DE_IIR_ADDR_SPT, SOUTH_DE_IIR_ADDR_SPT, 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       GEN10MMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_DE_ISR_ADDR_SPT, SOUTH_DE_ISR_ADDR_SPT, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN10MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_HOT_PLUG_CTL_2_ADDR_SPT, SOUTH_HOT_PLUG_CTL_2_ADDR_SPT, 0, NULL, NULL, 0, TRUE,
                                                       eNoExecHw, NULL, GEN10MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN10LPMMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN                bRet          = FALSE;
    DE_PORT_INTR_TABLE_CNL stPortLiveReg = { 0 };
    stPortLiveReg.DdiAHotplug            = TRUE;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, MASTER_INTR_CTL_ADDR_CNL, MASTER_INTR_CTL_ADDR_CNL, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN10MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler, GEN10MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, HOT_PLUG_CTL_ADDR_GLK, HOT_PLUG_CTL_ADDR_GLK, 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       GEN10LPMMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DE_PORT_IIR_INTR_ADDR_CNL, DE_PORT_IIR_INTR_ADDR_CNL, 0, NULL, NULL, 0, TRUE, eReadCombine,
                                                       NULL, GEN10LPMMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DE_PORT_ISR_INTR_ADDR_CNL, DE_PORT_ISR_INTR_ADDR_CNL, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN10LPMMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN10MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    MASTER_INT_CTL_CNL stMasterIntCtrl = { 0 };
    stMasterIntCtrl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stMasterIntCtrl.MasterInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                   // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.
    *pulReadData = stMasterIntCtrl.Value;

    return TRUE;
}

BOOLEAN GEN10MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PMASTER_INT_CTL_CNL pstMasterIntCtrl =
    (PMASTER_INT_CTL_CNL)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[MASTER_INTR_CTL_ADDR_CNL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    MASTER_INT_CTL_CNL stMasterIntCtrlTemp = { 0 };

    stMasterIntCtrlTemp.Value               = ulWriteData;
    pstMasterIntCtrl->MasterInterruptEnable = stMasterIntCtrlTemp.MasterInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN10MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PMASTER_INT_CTL_CNL pstMasterIntCtrl =
    (PMASTER_INT_CTL_CNL)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[MASTER_INTR_CTL_ADDR_CNL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    SOUTH_DE_INTR_BIT_DEFINITION_SPT *pstPCHIIRReg    = { 0 }; // DE Interrupt IIR
    SOUTH_DE_INTR_BIT_DEFINITION_SPT  stPCHIIRRegTemp = { 0 }; // DE Interrupt IIR
    pstPCHIIRReg =
    (SOUTH_DE_INTR_BIT_DEFINITION_SPT *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.Value = ulWriteData;

    if (stPCHIIRRegTemp.Value != 0)
    {
        pstMasterIntCtrl->DePchInterruptsPending = FALSE;
        pstPCHIIRReg->Value &= ~stPCHIIRRegTemp.Value;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN10LPMMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{

    PMASTER_INT_CTL_CNL pstMasterIntCtrl =
    (PMASTER_INT_CTL_CNL)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[MASTER_INTR_CTL_ADDR_CNL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    DE_PORT_INTR_TABLE_CNL *pstPCHIIRReg    = { 0 }; // DE Interrupt IIR
    DE_PORT_INTR_TABLE_CNL  stPCHIIRRegTemp = { 0 }; // DE Interrupt IIR
    pstPCHIIRReg = (DE_PORT_INTR_TABLE_CNL *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.Value = ulWriteData;

    if (stPCHIIRRegTemp.Value != 0)
    {
        pstMasterIntCtrl->DePortInterruptsPending = FALSE;
        pstPCHIIRReg->Value &= ~stPCHIIRRegTemp.Value;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN10MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                          bRet                = TRUE;
    SHOTPLUG_CTL_SPT                 stHotPlugCtl        = { 0 };
    SHOTPLUG_CTL2_SPT                stHotPlugCtl2       = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT stPCHLiveReg        = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA       pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
    SOUTH_DE_INTR_BIT_DEFINITION_SPT stPCHLiveRegHw      = { 0 };
    ULONG                            driverRegValue      = 0;

    stHotPlugCtl.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);
    stHotPlugCtl2.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_2_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);

    stPCHLiveReg.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_DE_ISR_ADDR_SPT - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, SOUTH_DE_ISR_ADDR_SPT, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        stPCHLiveRegHw.Value = driverRegValue;
        if (TRUE == stPCHLiveRegHw.DdiAHotplug)
        {
            stPCHLiveReg.DdiAHotplug = stPCHLiveRegHw.DdiAHotplug;
        }
    }

    if (stHotPlugCtl.DdiBHpdInputEnable == FALSE)
    {
        stPCHLiveReg.DdiBHotplug = FALSE;
    }

    if (stHotPlugCtl.DdiCHpdInputEnable == FALSE)
    {
        stPCHLiveReg.DdiCHotplug = FALSE;
    }

    if (stHotPlugCtl.DdiDHpdInputEnable == FALSE)
    {
        stPCHLiveReg.DdiDHotplug = FALSE;
    }

    if (stHotPlugCtl2.DdiEHpdInputEnable == FALSE)
    {
        stPCHLiveReg.DdiEHotplug = FALSE;
    }

    if (stHotPlugCtl2.DdiFHpdInputEnable == FALSE)
    {
        stPCHLiveReg.DdiFHotplug = FALSE;
    }

    *pulReadData = stPCHLiveReg.Value;

    return bRet;
}

BOOLEAN GEN10LPMMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                bRet            = TRUE;
    HOTPLUG_CTL_GLK        stHotPlugCtl    = { 0 };
    DE_PORT_INTR_TABLE_CNL stPortLiveReg   = { 0 };
    DE_PORT_INTR_TABLE_CNL stPortLiveRegHw = { 0 };
    ULONG                  driverRegValue  = 0;

    stHotPlugCtl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[HOT_PLUG_CTL_ADDR_GLK - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stPortLiveReg.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, DE_PORT_ISR_INTR_ADDR_CNL, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        stPortLiveRegHw.Value = driverRegValue;
        if (TRUE == stPortLiveRegHw.DdiAHotplug)
        {
            stPortLiveReg.DdiAHotplug = stPortLiveRegHw.DdiAHotplug;
        }
    }

    if (stHotPlugCtl.DdiBHpdInputEnable == FALSE)
    {
        stPortLiveReg.DdiBHotplug = FALSE;
    }

    if (stHotPlugCtl.DdiCHpdInputEnable == FALSE)
    {
        stPortLiveReg.DdiCHotplug = FALSE;
    }

    *pulReadData = stPortLiveReg.Value;

    return bRet;
}

BOOLEAN GEN10MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN           bRet             = FALSE;
    SHOTPLUG_CTL_SPT *pstHotPlugCtl    = NULL;
    SHOTPLUG_CTL_SPT  stHotPlugCtlTemp = { 0 };

    SHOTPLUG_CTL2_SPT *pstHotPlugCtl2    = NULL;
    SHOTPLUG_CTL2_SPT  stHotPlugCtlTemp2 = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (SOUTH_HOT_PLUG_CTL_ADDR_SPT == ulMMIOOffset)
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
            pstHotPlugCtl       = ((SHOTPLUG_CTL_SPT *)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);

            pstHotPlugCtl->Value   = ulWriteData;
            stHotPlugCtlTemp.Value = ulWriteData;

            pstHotPlugCtl->DdiAHpdStatus &= ~stHotPlugCtlTemp.DdiAHpdStatus;
            pstHotPlugCtl->DdiBHpdStatus &= ~stHotPlugCtlTemp.DdiBHpdStatus;
            pstHotPlugCtl->DdiCHpdStatus &= ~stHotPlugCtlTemp.DdiCHpdStatus;
            pstHotPlugCtl->DdiDHpdStatus &= ~stHotPlugCtlTemp.DdiDHpdStatus;
        }
        else
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
            pstHotPlugCtl2      = ((SHOTPLUG_CTL2_SPT *)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_2_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);

            pstHotPlugCtl2->Value   = ulWriteData;
            stHotPlugCtlTemp2.Value = ulWriteData;

            pstHotPlugCtl2->DdiEHpdStatus &= ~stHotPlugCtlTemp2.DdiEHpdStatus;
            pstHotPlugCtl2->DdiFHpdStatus &= ~stHotPlugCtlTemp2.DdiFHpdStatus;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN10LPMMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                    bRet                = FALSE;
    HOTPLUG_CTL_GLK *          pstHotPlugCtl       = NULL;
    HOTPLUG_CTL_GLK            stHotPlugCtlTemp    = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        // stHotPlugCtlTemp.Value = ulWriteData;

        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

        //**Warning Pointer aliasing is not allowed by C++11 standard but Windows doesn't seem to mind it
        pstHotPlugCtl = ((HOTPLUG_CTL_GLK *)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

        pstHotPlugCtl->Value   = ulWriteData;
        stHotPlugCtlTemp.Value = ulWriteData;

        // Below bits are clear on write
        pstHotPlugCtl->DdiAHpdStatus &= ~stHotPlugCtlTemp.DdiAHpdStatus;
        pstHotPlugCtl->DdiBHpdStatus &= ~stHotPlugCtlTemp.DdiBHpdStatus;
        pstHotPlugCtl->DdiCHpdStatus &= ~stHotPlugCtlTemp.DdiCHpdStatus;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}
// dc
BOOLEAN GEN10MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType)
{
    BOOLEAN           bRet          = FALSE;
    SHOTPLUG_CTL_SPT  stHotPlugCtl  = { 0 };
    SHOTPLUG_CTL2_SPT stHotPlugCtl2 = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stHotPlugCtl.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stHotPlugCtl2.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_2_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.DdiAHpdInputEnable;
            break;

        case INTHDMIB_PORT:
        case INTDPB_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.DdiBHpdInputEnable;
            break;

        case INTHDMIC_PORT:
        case INTDPC_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.DdiCHpdInputEnable;
            break;

        case INTHDMID_PORT:
        case INTDPD_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.DdiDHpdInputEnable;
            break;

        case INTHDMIE_PORT:
        case INTDPE_PORT:
            bRet = (BOOLEAN)stHotPlugCtl2.DdiEHpdInputEnable;
            break;

        case INTHDMIF_PORT:
        case INTDPF_PORT:
            bRet = (BOOLEAN)stHotPlugCtl2.DdiFHpdInputEnable;
            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, SOUTH_HOT_PLUG_CTL_ADDR_SPT, stHotPlugCtl.Value, SOUTH_HOT_PLUG_CTL_2_ADDR_SPT, stHotPlugCtl2.Value, 0, 0, 0, 0);
    return bRet;
}

// dc
BOOLEAN GEN10LPMMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType)
{
    BOOLEAN                    bRet                = FALSE;
    HOTPLUG_CTL_GLK            stHotPlugCtl        = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stHotPlugCtl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[HOT_PLUG_CTL_ADDR_GLK - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.DdiAHpdInputEnable;
            break;

        case INTHDMIB_PORT:
        case INTDPB_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.DdiBHpdInputEnable;
            break;

        case INTHDMIC_PORT:
        case INTDPC_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.DdiCHpdInputEnable;
            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, HOT_PLUG_CTL_ADDR_GLK, stHotPlugCtl.Value, 0, 0, 0, 0, 0, 0);
    return bRet;
}

// bIsHPD == FALSE ==> SPI
BOOLEAN GEN10MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD)
{
    BOOLEAN                          bRet                = FALSE;
    MASTER_INT_CTL_CNL               stMasterIntCtrl     = { 0 };
    SHOTPLUG_CTL_SPT                 stHotPlugCtl        = { 0 };
    SHOTPLUG_CTL2_SPT                stHotPlugCtl2       = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT stPCHLiveReg        = { 0 }; // DE Interrupt ISR
    SOUTH_DE_INTR_BIT_DEFINITION_SPT stPCHIMRReg         = { 0 }; // DE Interrupt IMR
    SOUTH_DE_INTR_BIT_DEFINITION_SPT stPCHIIRReg         = { 0 }; // DE Interrupt IIR
    SOUTH_DE_INTR_BIT_DEFINITION_SPT stPCHIERReg         = { 0 }; // DE Interrupt IER
    PGLOBAL_MMIO_REGISTER_DATA       pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Check if HPD has been enabled by Gfx
        if (FALSE == GEN10MMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType))
        {
            break;
        }

        stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[MASTER_INTR_CTL_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stHotPlugCtl.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stHotPlugCtl2.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_2_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stPCHLiveReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_ISR_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_IMR_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_IIR_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_IER_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:

            if (stHotPlugCtl.DdiAHpdInputEnable && !stPCHIMRReg.DdiAHotplug && stPCHIERReg.DdiAHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.DdiAHotplug    = TRUE;
                    stPCHLiveReg.DdiAHotplug   = bAttach;
                    stHotPlugCtl.DdiAHpdStatus = 0x2;
                    bRet                       = TRUE;
                }
                else if (stPCHLiveReg.DdiAHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.DdiAHotplug    = TRUE;
                    stHotPlugCtl.DdiAHpdStatus = 0x1;
                    bRet                       = TRUE;
                }
            }

            break;

        case INTHDMIB_PORT:
        case INTDPB_PORT:

            if (stHotPlugCtl.DdiBHpdInputEnable && !stPCHIMRReg.DdiBHotplug && stPCHIERReg.DdiBHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.DdiBHotplug    = TRUE;
                    stPCHLiveReg.DdiBHotplug   = bAttach;
                    stHotPlugCtl.DdiBHpdStatus = 0x2;
                    bRet                       = TRUE;
                }
                else if (stPCHLiveReg.DdiBHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.DdiBHotplug    = TRUE;
                    stHotPlugCtl.DdiBHpdStatus = 0x1;
                    bRet                       = TRUE;
                }
            }

            break;

        case INTHDMIC_PORT:
        case INTDPC_PORT:

            if (stHotPlugCtl.DdiCHpdInputEnable && !stPCHIMRReg.DdiCHotplug && stPCHIERReg.DdiCHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.DdiCHotplug    = TRUE;
                    stPCHLiveReg.DdiCHotplug   = bAttach;
                    stHotPlugCtl.DdiCHpdStatus = 0x2;
                    bRet                       = TRUE;
                }
                else if (stPCHLiveReg.DdiCHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.DdiCHotplug    = TRUE;
                    stHotPlugCtl.DdiCHpdStatus = 0x1;
                    bRet                       = TRUE;
                }
            }

            break;

        case INTHDMID_PORT:
        case INTDPD_PORT:

            if (stHotPlugCtl.DdiDHpdInputEnable && !stPCHIMRReg.DdiDHotplug && stPCHIERReg.DdiDHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.DdiDHotplug    = TRUE;
                    stPCHLiveReg.DdiDHotplug   = bAttach;
                    stHotPlugCtl.DdiDHpdStatus = 0x2;
                    bRet                       = TRUE;
                }
                else if (stPCHLiveReg.DdiDHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.DdiDHotplug    = TRUE;
                    stHotPlugCtl.DdiDHpdStatus = 0x1;
                    bRet                       = TRUE;
                }
            }

            break;

        case INTHDMIE_PORT:
        case INTDPE_PORT:

            if (stHotPlugCtl2.DdiEHpdInputEnable && !stPCHIMRReg.DdiEHotplug && stPCHIERReg.DdiEHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.DdiEHotplug     = TRUE;
                    stPCHLiveReg.DdiEHotplug    = bAttach;
                    stHotPlugCtl2.DdiEHpdStatus = 0x2;
                    bRet                        = TRUE;
                }
                else if (stPCHLiveReg.DdiEHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.DdiEHotplug     = TRUE;
                    stHotPlugCtl2.DdiEHpdStatus = 0x1;
                    bRet                        = TRUE;
                }
            }

            break;

        case INTHDMIF_PORT:
        case INTDPF_PORT:

            if (stHotPlugCtl2.DdiFHpdInputEnable && !stPCHIMRReg.DdiFHotplug && stPCHIERReg.DdiFHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.DdiFHotplug     = TRUE;
                    stPCHLiveReg.DdiFHotplug    = bAttach;
                    stHotPlugCtl2.DdiFHpdStatus = 0x2;
                    bRet                        = TRUE;
                }
                else if (stPCHLiveReg.DdiFHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.DdiFHotplug     = TRUE;
                    stHotPlugCtl2.DdiFHpdStatus = 0x1;
                    bRet                        = TRUE;
                }
            }

            break;

        default:

            break;
        }

    } while (FALSE);

    if (bRet)
    {
        // Below line is a temp workaround
        stPCHLiveReg.DdiAHotplug                                                                                                   = TRUE;
        stMasterIntCtrl.DePchInterruptsPending                                                                                     = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset])   = stHotPlugCtl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_2_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl2.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_ISR_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset])         = stPCHLiveReg.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_IIR_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset])         = stPCHIIRReg.Value;
        // Master Interrupt Controller should be written at the end

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[MASTER_INTR_CTL_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;
    }

    return bRet;
}

// bIsHPD == FALSE ==> SPI
BOOLEAN GEN10LPMMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD)
{
    BOOLEAN                    bRet                = FALSE;
    MASTER_INT_CTL_CNL         stMasterIntCtrl     = { 0 };
    HOTPLUG_CTL_GLK            stHotPlugCtl        = { 0 };
    DE_PORT_INTR_TABLE_CNL     stPortLiveReg       = { 0 };
    DE_PORT_INTR_TABLE_CNL     stPortIMRReg        = { 0 }; // DE Interrupt IMR
    DE_PORT_INTR_TABLE_CNL     stPortIIRReg        = { 0 }; // DE Interrupt IIR
    DE_PORT_INTR_TABLE_CNL     stPortIERReg        = { 0 }; // DE Interrupt IER
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;
    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        if (FALSE == GEN10LPMMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType))
        {
            break;
        }

        stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[MASTER_INTR_CTL_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stHotPlugCtl.Value    = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[HOT_PLUG_CTL_ADDR_GLK - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPortLiveReg.Value   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_PORT_ISR_INTR_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPortIMRReg.Value    = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_PORT_IMR_INTR_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPortIIRReg.Value    = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_PORT_IIR_INTR_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPortIERReg.Value    = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_PORT_IER_INTR_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:

            if (stHotPlugCtl.DdiAHpdInputEnable && !stPortIMRReg.DdiAHotplug && stPortIERReg.DdiAHotplug) // Interrupt shouldn't be masked by Gfx and also enabled by Gfx
            {
                if (bIsHPD)
                {
                    stPortIIRReg.DdiAHotplug   = TRUE;
                    stPortLiveReg.DdiAHotplug  = bAttach;
                    stHotPlugCtl.DdiAHpdStatus = 0x2;
                    bRet                       = TRUE;
                }
                else if (stPortLiveReg.DdiAHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPortIIRReg.DdiAHotplug   = TRUE;
                    stHotPlugCtl.DdiAHpdStatus = 0x1;
                    bRet                       = TRUE;
                }
            }

            break;

        case INTHDMIB_PORT:
        case INTDPB_PORT:

            if (stHotPlugCtl.DdiBHpdInputEnable && !stPortIMRReg.DdiBHotplug && stPortIERReg.DdiBHotplug) //
            {
                if (bIsHPD)
                {
                    stPortIIRReg.DdiBHotplug   = TRUE;
                    stPortLiveReg.DdiBHotplug  = bAttach;
                    stHotPlugCtl.DdiBHpdStatus = 0x2;
                    bRet                       = TRUE;
                }
                else if (stPortLiveReg.DdiBHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPortIIRReg.DdiBHotplug   = TRUE;
                    stHotPlugCtl.DdiBHpdStatus = 0x1;
                    bRet                       = TRUE;
                }
            }

            break;

        case INTHDMIC_PORT:
        case INTDPC_PORT:

            if (stHotPlugCtl.DdiCHpdInputEnable && !stPortIMRReg.DdiCHotplug && stPortIERReg.DdiCHotplug)
            {
                if (bIsHPD)
                {
                    stPortIIRReg.DdiCHotplug   = TRUE;
                    stPortLiveReg.DdiCHotplug  = bAttach;
                    stHotPlugCtl.DdiCHpdStatus = 0x2;
                    bRet                       = TRUE;
                }
                else if (stPortLiveReg.DdiCHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPortIIRReg.DdiCHotplug   = TRUE;
                    stHotPlugCtl.DdiCHpdStatus = 0x1;
                    bRet                       = TRUE;
                }
            }

            break;

        default:

            break;
        }

    } while (FALSE);

    if (bRet)
    {
        // Below line is a temp workaround
        stPortLiveReg.DdiAHotplug                                                                                              = TRUE;
        stMasterIntCtrl.DePortInterruptsPending                                                                                = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[HOT_PLUG_CTL_ADDR_GLK - pstGlobalMMORegData->ulMMIOBaseOffset])     = stHotPlugCtl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_PORT_ISR_INTR_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPortLiveReg.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_PORT_IIR_INTR_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPortIIRReg.Value;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[MASTER_INTR_CTL_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;
    }

    return bRet;
}

// This function would just set/reset the ISR/Live State register without caring for CTL, IMR or IER registers
// This is especially needed for plugging/Unplugging while S3/S4
BOOLEAN GEN10MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach)
{
    BOOLEAN                          bRet                = TRUE;
    SOUTH_DE_INTR_BIT_DEFINITION_SPT stPCHLiveReg        = { 0 }; // DE Interrupt ISR
    PGLOBAL_MMIO_REGISTER_DATA       pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stPCHLiveReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_ISR_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
            stPCHLiveReg.DdiAHotplug = bAttach;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            stPCHLiveReg.DdiBHotplug = bAttach;
            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:
            stPCHLiveReg.DdiCHotplug = bAttach;
            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            stPCHLiveReg.DdiDHotplug = bAttach;
            break;

        case INTDPE_PORT:
        case INTHDMIE_PORT:
            stPCHLiveReg.DdiEHotplug = bAttach;
            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            stPCHLiveReg.DdiFHotplug = bAttach;
            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        // Below line is a temp workaround
        stPCHLiveReg.DdiAHotplug                                                                                           = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_ISR_ADDR_SPT - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPCHLiveReg.Value;
    }

    return bRet;
}

// This function would just set/reset the ISR/Live State register without caring for CTL, IMR or IER registers
// This is especially needed for plugging/Unplugging while S3/S4
BOOLEAN GEN10LPMMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach)
{
    BOOLEAN                    bRet                = TRUE;
    DE_PORT_INTR_TABLE_CNL     stPortLiveReg       = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stPortLiveReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_PORT_ISR_INTR_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
            stPortLiveReg.DdiAHotplug = bAttach;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            stPortLiveReg.DdiBHotplug = bAttach;
            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:
            stPortLiveReg.DdiCHotplug = bAttach;
            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        // Below line is a temp workaround
        stPortLiveReg.DdiAHotplug                                                                                              = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_PORT_ISR_INTR_ADDR_CNL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPortLiveReg.Value;
    }

    return bRet;
}
