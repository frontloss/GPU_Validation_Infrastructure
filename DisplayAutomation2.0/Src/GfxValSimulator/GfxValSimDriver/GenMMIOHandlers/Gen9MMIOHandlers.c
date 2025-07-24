#include "..\\CommonCore\\PortingLayer.h"
#include "..\\DriverInterfaces\\SIMDRV_GFX_COMMON.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"
#include "..\\DriverInterfaces\\CommonRxHandlers.h"
#include "..\\DriverInterfaces\\DPHandlers.h"
#include "Gen9MMIO.h"
#include "CommonMMIO.h"
#include "..\\GenMMIOHandlers\\Gen12\Gen12CommonInterruptRegisters.h"
#include "..\\GenMMIOHandlers\\Gen12\\RKLMMIO.h"
#include "..\\..\\CommonInclude\\ETWLogging.h"
#include "..\\..\DriverInterfaces\\SimDrvToGfx.h"

BOOLEAN GEN9MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface);

BOOLEAN GEN9MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN9MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN9MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN9MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN9MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN9MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType);

BOOLEAN GEN9MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {
        bRet = GEN9MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN9MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    if (pstMMIOInterface)
    {

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_START] = DDI_AUX_DATA_A_START_SKL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_END]   = DDI_AUX_DATA_A_END_SKL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_A]        = DDI_AUX_CTL_A_SKL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_START] = DDI_AUX_DATA_B_START_SKL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_END]   = DDI_AUX_DATA_B_END_SKL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_B]        = DDI_AUX_CTL_B_SKL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = DDI_AUX_DATA_C_START_SKL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = DDI_AUX_DATA_C_END_SKL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = DDI_AUX_CTL_C_SKL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = DDI_AUX_DATA_D_START_SKL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = DDI_AUX_DATA_D_END_SKL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = DDI_AUX_CTL_D_SKL;

        // Every new offset should be added above this. So as to invalidate the rest
        // Do below: ulCount = [Last enum in above list] + 1;
        ulCount = eINDEX_DDI_AUX_CTL_D + 1;
        for (; ulCount < MAX_GEN_MMIO_OFFSETS_STORED; ulCount++)
        {
            pstMMIOInterface->pulGenMMIOOffsetArray[ulCount] = OFFSET_INVALID;
        }

        bRet = TRUE;
    }

    return bRet;
}

BOOLEAN GEN9MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN           bRet           = FALSE;
    SPT_PCH_INT_TABLE stLiveStateReg = { 0 };
    stLiveStateReg.bDdiAHotplug      = TRUE;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }
        if (pstMMIOInterface->eIGFXPlatform == eIGFX_ROCKETLAKE)
        {
            bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_INTR_ADDR_GEN12, GFX_MSTR_INTR_ADDR_GEN12, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                           GEN12_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler, GEN12_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler,
                                                           NULL, NULL, NULL);

            if (bRet == FALSE)
            {
                break;
            }
            bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DISPLAY_INTR_CTL_ADDR_GEN12, DISPLAY_INTR_CTL_ADDR_GEN12, 0, NULL, NULL, 0, FALSE,
                                                           eNoExecHw, GEN12_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler,
                                                           GEN12_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

            if (bRet == FALSE)
            {
                break;
            }
        }
        else
        {
            bRet =
            COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, MASTER_INTR_CTL_SKL, MASTER_INTR_CTL_SKL, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                    GEN9MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler, GEN9MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

            if (bRet == FALSE)
            {
                break;
            }
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SPT_SHOTPLUG_CTL_REG, SPT_SHOTPLUG_CTL_REG, 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       GEN9MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SPT_SHOTPLUG_CTL2_REG, SPT_SHOTPLUG_CTL2_REG, 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       GEN9MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SPT_PCH_IIR, SPT_PCH_IIR, 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       GEN9MMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SPT_PCH_ISR, SPT_PCH_ISR, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN9MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN9MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    SKL_MSTR_INTR_TABLE stMasterIntCtrl = { 0 };
    stMasterIntCtrl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stMasterIntCtrl.MstrInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                 // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stMasterIntCtrl.Value;

    return TRUE;
}

BOOLEAN GEN9MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PSKL_MSTR_INTR_TABLE pstMasterIntCtrl =
    (PSKL_MSTR_INTR_TABLE)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    SKL_MSTR_INTR_TABLE stMasterIntCtrlTemp = { 0 };

    stMasterIntCtrlTemp.Value             = ulWriteData;
    pstMasterIntCtrl->MstrInterruptEnable = stMasterIntCtrlTemp.MstrInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN9MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PSKL_MSTR_INTR_TABLE pstMasterIntCtrl =
    (PSKL_MSTR_INTR_TABLE)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[MASTER_INTR_CTL_SKL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    SPT_PCH_INT_TABLE *pstPCHIIRReg    = { 0 }; // DE Interrupt IIR
    SPT_PCH_INT_TABLE  stPCHIIRRegTemp = { 0 }; // DE Interrupt IIR
    pstPCHIIRReg = (SPT_PCH_INT_TABLE *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.ulValue = ulWriteData;

    if (stPCHIIRRegTemp.ulValue != 0)
    {
        pstMasterIntCtrl->DEPCHInterruptsPending = FALSE;
        pstPCHIIRReg->ulValue &= ~stPCHIIRRegTemp.ulValue;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN9MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                 bRet             = TRUE;
    SPT_HOTPLUG_CTL_REG_ST  stHotPlugCtl     = { 0 };
    SPT_HOTPLUG_CTL2_REG_ST stHotPlugCtl2    = { 0 };
    SPT_PCH_INT_TABLE       stLiveStateReg   = { 0 };
    SPT_PCH_INT_TABLE       stLiveStateRegHw = { 0 };
    ULONG                   driverRegValue   = 0;

    stHotPlugCtl.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SPT_SHOTPLUG_CTL_REG - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stLiveStateReg.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, SPT_PCH_ISR, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        stLiveStateRegHw.ulValue = driverRegValue;
        if (TRUE == stLiveStateRegHw.bDdiAHotplug)
        {
            stLiveStateReg.bDdiAHotplug = stLiveStateRegHw.bDdiAHotplug;
        }
    }

    if (stHotPlugCtl.bDdiBHpdInputEnable == FALSE)
    {
        stLiveStateReg.bDdiBHotplug = FALSE;
    }

    if (stHotPlugCtl.bDdiCHpdInputEnable == FALSE)
    {
        stLiveStateReg.bDdiCHotplug = FALSE;
    }

    if (stHotPlugCtl.bDdiDHpdInputEnable == FALSE)
    {
        stLiveStateReg.bDdiDHotplug = FALSE;
    }

    if (stHotPlugCtl2.bDdiEHpdInputEnable == FALSE)
    {
        stLiveStateReg.bDdiEHotplug = FALSE;
    }

    *pulReadData = stLiveStateReg.ulValue;

    return bRet;
}

BOOLEAN GEN9MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                 bRet             = FALSE;
    SPT_HOTPLUG_CTL_REG_ST *pstHotPlugCtl    = NULL;
    SPT_HOTPLUG_CTL_REG_ST  stHotPlugCtlTemp = { 0 };

    SPT_HOTPLUG_CTL2_REG_ST *pstHotPlugCtl2    = NULL;
    SPT_HOTPLUG_CTL2_REG_ST  stHotPlugCtlTemp2 = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;
    pstGlobalMMORegData                            = &pstMMIOHandlerInfo->stGlobalMMORegData;

    do
    {
        if (SPT_SHOTPLUG_CTL_REG == ulMMIOOffset)
        {

            pstHotPlugCtl = ((SPT_HOTPLUG_CTL_REG_ST *)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_SHOTPLUG_CTL_REG - pstGlobalMMORegData->ulMMIOBaseOffset]);

            pstHotPlugCtl->ulValue   = ulWriteData;
            stHotPlugCtlTemp.ulValue = ulWriteData;

            pstHotPlugCtl->bDdiA_LongPulseStatus &= ~stHotPlugCtlTemp.bDdiA_LongPulseStatus;
            pstHotPlugCtl->bDdiA_ShortPulseStatus &= ~stHotPlugCtlTemp.bDdiA_ShortPulseStatus;

            pstHotPlugCtl->bDdiB_LongPulseStatus &= ~stHotPlugCtlTemp.bDdiB_LongPulseStatus;
            pstHotPlugCtl->bDdiB_ShortPulseStatus &= ~stHotPlugCtlTemp.bDdiB_ShortPulseStatus;

            pstHotPlugCtl->bDdiC_LongPulseStatus &= ~stHotPlugCtlTemp.bDdiC_LongPulseStatus;
            pstHotPlugCtl->bDdiC_ShortPulseStatus &= ~stHotPlugCtlTemp.bDdiC_ShortPulseStatus;

            pstHotPlugCtl->bDdiD_LongPulseStatus &= ~stHotPlugCtlTemp.bDdiD_LongPulseStatus;
            pstHotPlugCtl->bDdiD_ShortPulseStatus &= ~stHotPlugCtlTemp.bDdiD_ShortPulseStatus;
        }
        else
        {
            pstHotPlugCtl2 = ((SPT_HOTPLUG_CTL2_REG_ST *)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_SHOTPLUG_CTL2_REG - pstGlobalMMORegData->ulMMIOBaseOffset]);

            pstHotPlugCtl2->ulValue   = ulWriteData;
            stHotPlugCtlTemp2.ulValue = ulWriteData;

            pstHotPlugCtl2->bDdiE_LongPulseStatus &= ~stHotPlugCtlTemp2.bDdiE_LongPulseStatus;
            pstHotPlugCtl2->bDdiE_ShortPulseStatus &= ~stHotPlugCtlTemp2.bDdiE_ShortPulseStatus;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN9MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType)
{
    BOOLEAN                    bRet                = FALSE;
    SPT_HOTPLUG_CTL_REG_ST     stHotPlugCtl        = { 0 };
    SPT_HOTPLUG_CTL2_REG_ST    stHotPlugCtl2       = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stHotPlugCtl.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_SHOTPLUG_CTL_REG - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stHotPlugCtl2.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_SHOTPLUG_CTL2_REG - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.bDdiAHpdInputEnable;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.bDdiBHpdInputEnable;
            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.bDdiCHpdInputEnable;
            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            bRet = (BOOLEAN)stHotPlugCtl.bDdiDHpdInputEnable;
            break;

        case INTDPE_PORT:
        case INTHDMIE_PORT:
            bRet = (BOOLEAN)stHotPlugCtl2.bDdiEHpdInputEnable;
            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, SPT_SHOTPLUG_CTL_REG, stHotPlugCtl.ulValue, SPT_SHOTPLUG_CTL2_REG, stHotPlugCtl2.ulValue, 0, 0, 0, 0);
    return bRet;
}

// bIsHPD == FALSE ==> SPI
BOOLEAN GEN9MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD)
{
    BOOLEAN                 bRet                 = FALSE;
    SKL_MSTR_INTR_TABLE     stMasterIntCtrl      = { 0 };
    GFX_MSTR_INTR_GEN12     stMasterIntCtrlGen12 = { 0 };
    DISPLAY_INT_CTL_GEN12   stDisplayIntCtrl     = { 0 };
    SPT_HOTPLUG_CTL_REG_ST  stHotPlugCtl         = { 0 };
    SPT_HOTPLUG_CTL2_REG_ST stHotPlugCtl2        = { 0 };

    SPT_PCH_INT_TABLE          stPCHLiveReg        = { 0 }; // DE Interrupt ISR
    SPT_PCH_INT_TABLE          stPCHIMRReg         = { 0 }; // DE Interrupt IMR
    SPT_PCH_INT_TABLE          stPCHIIRReg         = { 0 }; // DE Interrupt IIR
    SPT_PCH_INT_TABLE          stPCHIERReg         = { 0 }; // DE Interrupt IER
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Check if HPD has been enabled by Gfx
        if (FALSE == GEN9MMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType))
        {
            break;
        }
        if (pstMMIOInterface->eIGFXPlatform == eIGFX_ROCKETLAKE)
        {
            stMasterIntCtrlGen12.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        }
        else
        {
            stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[MASTER_INTR_CTL_SKL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        }

        stHotPlugCtl.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_SHOTPLUG_CTL_REG - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stHotPlugCtl2.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_SHOTPLUG_CTL2_REG - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_PCH_ISR - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_PCH_IMR - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_PCH_IIR - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_PCH_IER - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:

            if (stHotPlugCtl.bDdiAHpdInputEnable && !stPCHIMRReg.bDdiAHotplug && stPCHIERReg.bDdiAHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.bDdiAHotplug           = TRUE;
                    stPCHLiveReg.bDdiAHotplug          = bAttach;
                    stHotPlugCtl.bDdiA_LongPulseStatus = TRUE;
                    bRet                               = TRUE;
                }
                else if (stPCHLiveReg.bDdiAHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.bDdiAHotplug            = TRUE;
                    stHotPlugCtl.bDdiA_ShortPulseStatus = TRUE;
                    bRet                                = TRUE;
                }
            }

            break;

        case INTHDMIB_PORT:
        case INTDPB_PORT:

            if (stHotPlugCtl.bDdiBHpdInputEnable && !stPCHIMRReg.bDdiBHotplug && stPCHIERReg.bDdiBHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.bDdiBHotplug           = TRUE;
                    stPCHLiveReg.bDdiBHotplug          = bAttach;
                    stHotPlugCtl.bDdiB_LongPulseStatus = TRUE;
                    bRet                               = TRUE;
                }
                else if (stPCHLiveReg.bDdiBHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.bDdiBHotplug            = TRUE;
                    stHotPlugCtl.bDdiB_ShortPulseStatus = TRUE;
                    bRet                                = TRUE;
                }
            }

            break;

        case INTHDMIC_PORT:
        case INTDPC_PORT:

            if (stHotPlugCtl.bDdiCHpdInputEnable && !stPCHIMRReg.bDdiCHotplug && stPCHIERReg.bDdiCHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.bDdiCHotplug           = TRUE;
                    stPCHLiveReg.bDdiCHotplug          = bAttach;
                    stHotPlugCtl.bDdiC_LongPulseStatus = TRUE;
                    bRet                               = TRUE;
                }
                else if (stPCHLiveReg.bDdiCHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.bDdiCHotplug            = TRUE;
                    stHotPlugCtl.bDdiC_ShortPulseStatus = TRUE;
                    bRet                                = TRUE;
                }
            }

            break;

        case INTHDMID_PORT:
        case INTDPD_PORT:

            if (stHotPlugCtl.bDdiDHpdInputEnable && !stPCHIMRReg.bDdiDHotplug && stPCHIERReg.bDdiDHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.bDdiDHotplug           = TRUE;
                    stPCHLiveReg.bDdiDHotplug          = bAttach;
                    stHotPlugCtl.bDdiD_LongPulseStatus = TRUE;
                    bRet                               = TRUE;
                }
                else if (stPCHLiveReg.bDdiDHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.bDdiDHotplug            = TRUE;
                    stHotPlugCtl.bDdiD_ShortPulseStatus = TRUE;
                    bRet                                = TRUE;
                }
            }

            break;

        case INTHDMIE_PORT:
        case INTDPE_PORT:

            if (stHotPlugCtl2.bDdiEHpdInputEnable && !stPCHIMRReg.bDdiEHotplug && stPCHIERReg.bDdiEHotplug)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.bDdiEHotplug            = TRUE;
                    stPCHLiveReg.bDdiEHotplug           = bAttach;
                    stHotPlugCtl2.bDdiE_LongPulseStatus = TRUE;
                    bRet                                = TRUE;
                }
                else if (stPCHLiveReg.bDdiEHotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.bDdiEHotplug             = TRUE;
                    stHotPlugCtl2.bDdiE_ShortPulseStatus = TRUE;
                    bRet                                 = TRUE;
                }
            }

            break;

        default:

            break;
        }

    } while (FALSE);

    if (bRet)
    {
        if (pstMMIOInterface->eIGFXPlatform == eIGFX_ROCKETLAKE)
        {
            stDisplayIntCtrl.DePchInterruptsPending                                                                                  = TRUE;
            stMasterIntCtrlGen12.DisplayInterruptsPending                                                                            = TRUE;
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])    = stMasterIntCtrlGen12.Value;
        }
        else
        {
            // Below line is a temp workaround
            stPCHLiveReg.bDdiAHotplug              = TRUE;
            stMasterIntCtrl.DEPCHInterruptsPending = TRUE;
            /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
            // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[MASTER_INTR_CTL_SKL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;
        }
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_SHOTPLUG_CTL_REG - pstGlobalMMORegData->ulMMIOBaseOffset])  = stHotPlugCtl.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_SHOTPLUG_CTL2_REG - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl2.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_PCH_ISR - pstGlobalMMORegData->ulMMIOBaseOffset])           = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_PCH_IIR - pstGlobalMMORegData->ulMMIOBaseOffset])           = stPCHIIRReg.ulValue;
    }

    return bRet;
}

BOOLEAN GEN9MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach)
{
    BOOLEAN                    bRet                = TRUE;
    SPT_PCH_INT_TABLE          stPCHLiveReg        = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_PCH_ISR - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
            stPCHLiveReg.bDdiAHotplug = bAttach;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            stPCHLiveReg.bDdiBHotplug = bAttach;
            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:
            stPCHLiveReg.bDdiCHotplug = bAttach;
            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            stPCHLiveReg.bDdiDHotplug = bAttach;
            break;

        case INTDPE_PORT:
        case INTHDMIE_PORT:
            stPCHLiveReg.bDdiEHotplug = bAttach;
            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        stPCHLiveReg.bDdiAHotplug                                                                                = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SPT_PCH_ISR - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPCHLiveReg.ulValue;
    }

    return bRet;
}
