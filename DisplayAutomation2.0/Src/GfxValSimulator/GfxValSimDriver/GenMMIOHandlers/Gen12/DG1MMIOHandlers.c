/**********************************************************************************************************
DG1 HPD Flow

MASTER_CTL_INT(0x190010) - MasterInterruptRW[Gfx IP or others] Get the Interrupt Source ie Display Interrupt
DISPLAY_INTR_CTL_ADDR_ICL(0x44200) - DisplayInterruptRW[Display, GPU or Render] Get the Legacy Interrupt Source means is it HPD/Port/Pipe/Audio
SOUTH_DE_IIR_ADDR_SPT(0xC4008) - HotPlugIIRWrite[Pipe or Port interrupt Interrupt Source ie PCH Display]
SOUTH_HOT_PLUG_CTL_ADDR_SPT(0xC4030) - HotPlugCTLWrite[Which port is being connected? Short or Long Pulse]

SOUTH_DE_ISR_ADDR_SPT(0xc4000) - HotPlugLiveStateRead[Connected / Disconnected]


Call Flow: Gfx Mainline Driver: Legacy:
1. GEN12DG1_INTRHANDLER_GetInterruptSource  ---> case GEN12DG1_DISPLAY_INTERRUPT_BIT_POS --> LegacyInterruptsOccurred Flag should be set
2. GEN12DG1_INTRHANDLER_GetLegacyInterruptSource
3. GEN12DG1_INTRHANDLER_GetHPDInterruptSource

********************************************************************************************************/
#include "DG1MMIO.h"
#include "..\..\DriverInterfaces\SimDrvToGfx.h"
#include "..\\..\\CommonInclude\\ETWLogging.h"

BOOLEAN DG1_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {

        bRet = DG1_MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);

    } while (FALSE);

    return bRet;
}

BOOLEAN DG1_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Master Tile Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50862
        bRet =
        COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_TILE_INTR_ADDR_DG1, GFX_MSTR_TILE_INTR_ADDR_DG1, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                DG1_MMIOHANDLERS_MasterTileInterruptCtlMMIOReadHandler, DG1_MMIOHANDLERS_MasterTileInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // TODO: Can we remove the below?
        // Master Interrupt Control Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/53222
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_INTR_ADDR_GEN12, GFX_MSTR_INTR_ADDR_GEN12, 0, NULL, NULL, 0, TRUE, eReadCombine,
                                                       NULL, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Display Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/20451
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DISPLAY_INTR_CTL_ADDR_GEN12, DISPLAY_INTR_CTL_ADDR_GEN12, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN12_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler, GEN12_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler, NULL,
                                                       NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/33773
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_ISR_ADDR_GEN12, SDE_ISR_ADDR_GEN12, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       DG1_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_IIR_ADDR_GEN12, SDE_IIR_ADDR_GEN12, 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       // DG1_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler,
                                                       GEN12_CMN_MMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/33768
        // The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port
        // These two are the south hot plug control registers
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12, 0, NULL, NULL,
                                                       0, TRUE, eNoExecHw, NULL, DG1_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, IGT_PAVP_FUSE_2, IGT_PAVP_FUSE_2, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       DG1_MMIOHANDLERS_ProductionSkuMMIOReadHandler, NULL, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN DG1_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    if (pstMMIOInterface)
    {

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_START] = DDI_AUX_DATA_A_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_END]   = DDI_AUX_DATA_A_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_A]        = DDI_AUX_CTL_A_GEN12;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_START] = DDI_AUX_DATA_B_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_END]   = DDI_AUX_DATA_B_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_B]        = DDI_AUX_CTL_B_GEN12;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = DDI_AUX_DATA_TC1_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = DDI_AUX_DATA_TC1_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = DDI_AUX_CTL_TC1_GEN12;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = DDI_AUX_DATA_TC2_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = DDI_AUX_DATA_TC2_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = DDI_AUX_CTL_TC2_GEN12;

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

BOOLEAN DG1_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                            PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                            bRet                = FALSE;
    GRAPHICS_MASTER_TILE_INTERRUPT_DG1 stMasterTileIntCtrl = { 0 };
    GFX_MSTR_INTR_GEN12                stMasterIntCtrl     = { 0 };
    DISPLAY_INT_CTL_GEN12              stDisplayIntCtrl    = { 0 };

    SHOTPLUG_CTL_DDI_GEN12 stSouthCtlReg = { 0 };

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHLiveReg = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHIMRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHIIRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHIERReg  = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Check if HPD has been enabled by Gfx
        if (FALSE == DG1_MMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType, PortConnectorInfo))
        {
            break;
        }

        stMasterTileIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_DG1 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Bspec Ref; https://gfxspecs.intel.com/Predator/Home/Index/33768
        stSouthCtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Legacy
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/33773
        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_ISR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IMR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IER_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
        case INTHDMIA_PORT:

            if (stSouthCtlReg.DdiaHpdEnable && stPCHIMRReg.HotplugDdia == FALSE && stPCHIERReg.HotplugDdia)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugDdia  = TRUE;
                    stPCHLiveReg.HotplugDdia = bAttach;
                    // Long Pulse
                    stSouthCtlReg.DdiaHpdStatus = 2;
                    bRet                        = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdia) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdia = TRUE;
                    // Short Pulse
                    stSouthCtlReg.DdiaHpdStatus = 0x1;
                    bRet                        = TRUE;
                }
            }

            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:

            if (stSouthCtlReg.DdibHpdEnable && stPCHIMRReg.HotplugDdib == FALSE && stPCHIERReg.HotplugDdib)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugDdib     = TRUE;
                    stPCHLiveReg.HotplugDdib    = bAttach;
                    stSouthCtlReg.DdibHpdStatus = 2;
                    bRet                        = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdib) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdib     = TRUE;
                    stSouthCtlReg.DdibHpdStatus = 0x1;
                    bRet                        = TRUE;
                }
            }

            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:

            if (stSouthCtlReg.DdicHpdEnable && stPCHIMRReg.HotplugDdic == FALSE && stPCHIERReg.HotplugDdic)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugDdic     = TRUE;
                    stPCHLiveReg.HotplugDdic    = bAttach;
                    stSouthCtlReg.DdicHpdStatus = 2;
                    bRet                        = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdic) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdic     = TRUE;
                    stSouthCtlReg.DdicHpdStatus = 0x1;
                    bRet                        = TRUE;
                }
            }

            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:

            if (stSouthCtlReg.DdidHpdEnable && stPCHIMRReg.HotplugDdid == FALSE && stPCHIERReg.HotplugDdid)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugDdid     = TRUE;
                    stPCHLiveReg.HotplugDdid    = bAttach;
                    stSouthCtlReg.DdidHpdStatus = 2;
                    bRet                        = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdid) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdid     = TRUE;
                    stSouthCtlReg.DdidHpdStatus = 0x1;
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
        stMasterTileIntCtrl.Tile0                = TRUE;
        stMasterIntCtrl.DisplayInterruptsPending = TRUE;
        stDisplayIntCtrl.DeHpdInterruptsPending  = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthCtlReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])                    = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])                    = stPCHIIRReg.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])    = stMasterIntCtrl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_DG1 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterTileIntCtrl.Value;
    }

    return bRet;
}

BOOLEAN DG1_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                                bRet                = TRUE;
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHLiveReg        = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA             pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
        case INTHDMIA_PORT:
            stPCHLiveReg.HotplugDdia = bAttach;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            stPCHLiveReg.HotplugDdib = bAttach;
            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:
            stPCHLiveReg.HotplugDdic = bAttach;
            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            stPCHLiveReg.HotplugDdid = bAttach;
            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        // Below line is a temp workaround
        stPCHLiveReg.HotplugDdia                                                                                        = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPCHLiveReg.ulValue;
    }

    return bRet;
}

/*
This function will clear the HpdStatus value of a particular DDI
which Gfx Driver wants to.
*/
BOOLEAN DG1_MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                    bRet                = FALSE;
    SHOTPLUG_CTL_DDI_GEN12     stSouthDDICtlReg    = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stSouthDDICtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
        case INTHDMIA_PORT:
            bRet = (BOOLEAN)stSouthDDICtlReg.DdiaHpdEnable;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            bRet = (BOOLEAN)stSouthDDICtlReg.DdibHpdEnable;
            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:
            bRet = (BOOLEAN)stSouthDDICtlReg.DdicHpdEnable;
            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            bRet = (BOOLEAN)stSouthDDICtlReg.DdidHpdEnable;
            break;

        default:
            break;
        }

    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12, stSouthDDICtlReg.ulValue, 0, 0, 0, 0, 0, 0);
    return bRet;
}

BOOLEAN DG1_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                                bRet             = TRUE;
    SHOTPLUG_CTL_DDI_GEN12                 stHotPlugCtl     = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stLiveStateReg   = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stLiveStateRegHw = { 0 };
    ULONG                                  driverRegValue   = 0;

    stHotPlugCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stLiveStateReg.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, SDE_ISR_ADDR_GEN12, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        stLiveStateRegHw.ulValue = driverRegValue;
        if (TRUE == stLiveStateRegHw.HotplugDdia)
        {
            stLiveStateReg.HotplugDdia = stLiveStateRegHw.HotplugDdia;
        }
    }

    if (stHotPlugCtl.DdibHpdEnable == FALSE)
    {
        stLiveStateReg.HotplugDdib = FALSE;
    }

    if (stHotPlugCtl.DdicHpdEnable == FALSE)
    {
        stLiveStateReg.HotplugDdic = FALSE;
    }

    if (stHotPlugCtl.DdidHpdEnable == FALSE)
    {
        stLiveStateReg.HotplugDdid = FALSE;
    }

    *pulReadData = stLiveStateReg.ulValue;

    return bRet;
}

/*
This function will clear the HpdStatus value of a particular DDI
which Gfx Driver wants to.
*/
BOOLEAN DG1_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/33768
    SHOTPLUG_CTL_DDI_GEN12 stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_DDI_GEN12 stHotPlugCtlTemp = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

        stHotPlugCtlTemp.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stHotPlugCtl.ulValue = ulWriteData;

        stHotPlugCtl.DdiaHpdStatus = stHotPlugCtlTemp.DdiaHpdStatus;
        stHotPlugCtl.DdibHpdStatus = stHotPlugCtlTemp.DdibHpdStatus;
        stHotPlugCtl.DdicHpdStatus = stHotPlugCtlTemp.DdicHpdStatus;
        stHotPlugCtl.DdidHpdStatus = stHotPlugCtlTemp.DdidHpdStatus;

        stHotPlugCtlTemp.ulValue = ulWriteData;

        stHotPlugCtl.DdiaHpdStatus &= ~stHotPlugCtlTemp.DdiaHpdStatus;
        stHotPlugCtl.DdibHpdStatus &= ~stHotPlugCtlTemp.DdibHpdStatus;
        stHotPlugCtl.DdicHpdStatus &= ~stHotPlugCtlTemp.DdicHpdStatus;
        stHotPlugCtl.DdidHpdStatus &= ~stHotPlugCtlTemp.DdidHpdStatus;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl.ulValue;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN DG1_MMIOHANDLERS_MasterTileInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    GRAPHICS_MASTER_TILE_INTERRUPT_DG1 stMasterTileIntCtrl = { 0 };
    stMasterTileIntCtrl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stMasterTileIntCtrl.MasterInterrupt = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                 // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stMasterTileIntCtrl.Value;

    return TRUE;
}

BOOLEAN DG1_MMIOHANDLERS_MasterTileInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGRAPHICS_MASTER_TILE_INTERRUPT_DG1 pstMasterTileIntCtrl =
    (PGRAPHICS_MASTER_TILE_INTERRUPT_DG1)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    GRAPHICS_MASTER_TILE_INTERRUPT_DG1 stMasterTileIntCtrlTemp = { 0 };

    stMasterTileIntCtrlTemp.Value         = ulWriteData;
    pstMasterTileIntCtrl->MasterInterrupt = stMasterTileIntCtrlTemp.MasterInterrupt;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

/**-------------------------------------------------------------
 * @brief DG1_MMIOHANDLERS_ProductionSkuMMIOReadHandler
 *
 * Description: Production sku can be authenticated only with Production Oprom signature done by ubit. When we modify vbt, from infra we sign it with debug signature.
                This works fine for pre-production sku's. For MA configurations, we see production sku's connected. We are resetting production sku flag in valsim.
                With this change, gfx driver thinks it is an pre-production sku and authenticates with debug signature.
 *-------------------------------------------------------------*/
BOOLEAN DG1_MMIOHANDLERS_ProductionSkuMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                    bRet                = FALSE;
    DDU32                      ulPavpFuse2         = 0;
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;
    GFXVALSIM_FUNC_ENTRY();

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

        if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, ulMMIOOffset, &ulPavpFuse2, SIMDRV_GFX_ACCESS_REQUEST_READ))
        {
            GFXVALSIM_DBG_MSG("Production sku data modified.\r\n");
            ulPavpFuse2 = ulPavpFuse2 & (~0x4);

            *pulReadData = ulPavpFuse2;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = ulPavpFuse2;

            bRet = TRUE;
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(TRUE != bRet);
    return bRet;
}

BOOLEAN DG1_MMIOHANDLERS_ScdcInterruptGeneration(PMMIO_INTERFACE pstMMIOInterface, PSCDC_ARGS pstScdcArgs)
{
    BOOLEAN                                bRet                = FALSE;
    GRAPHICS_MASTER_TILE_INTERRUPT_DG1     stMasterTileIntCtrl = { 0 };
    GFX_MSTR_INTR_GEN12                    stMasterIntCtrl     = { 0 };
    DISPLAY_INT_CTL_GEN12                  stDisplayIntCtrl    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stSouthDeInt        = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }
        stMasterTileIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_DG1 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stMasterIntCtrl.Value    = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthDeInt.ulValue     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (pstScdcArgs->ulPortNum)
        {
        case INTHDMIA_PORT:
            stSouthDeInt.ScdcDdia = TRUE;
            bRet                  = TRUE;
            break;
        case INTHDMIB_PORT:
            stSouthDeInt.ScdcDdib = TRUE;
            bRet                  = TRUE;
            break;
        case INTHDMIC_PORT:
            stSouthDeInt.ScdcDdic = TRUE;
            bRet                  = TRUE;
            break;
        case INTHDMID_PORT:
            stSouthDeInt.ScdcDdid = TRUE;
            bRet                  = TRUE;
            break;
        default:
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        stMasterTileIntCtrl.Tile0                = TRUE;
        stMasterIntCtrl.DisplayInterruptsPending = TRUE;

        stDisplayIntCtrl.DePchInterruptsPending = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthDeInt.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])    = stMasterIntCtrl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_DG1 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterTileIntCtrl.Value;
    }

    return bRet;
}
