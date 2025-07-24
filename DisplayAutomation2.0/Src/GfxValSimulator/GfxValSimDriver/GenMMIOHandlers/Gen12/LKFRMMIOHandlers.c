#include "LKFRMMIO.h"
#include "..\\..\\CommonInclude\\ETWLogging.h"
#include "..\\..\\DriverInterfaces\\SimDrvToGfx.h"

BOOLEAN LKFR_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {

        bRet = LKFR_MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);

    } while (FALSE);

    return bRet;
}

BOOLEAN LKFR_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Master Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/20451
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_INTR_ADDR_GEN12, GFX_MSTR_INTR_ADDR_GEN12, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN12_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler, GEN12_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler, NULL,
                                                       NULL, NULL);

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

        // Regirstering SDE ISR - 0xC4000
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/8409
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_ISR_ADDR_GEN12, SDE_ISR_ADDR_GEN12, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       LKFR_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_IIR_ADDR_GEN12, SDE_IIR_ADDR_GEN12, 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       // TGLLP_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler,
                                                       GEN12_CMN_MMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21778
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21779
        // The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port
        // These two are the south hot plug control registers
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12, SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN12, 0, NULL, NULL,
                                                       0, TRUE, eNoExecHw, NULL, LKFR_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // North DE ISR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21261?dstFilter=ICLHP&mode=Filter
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       (NDE_ISR_ADDR_GEN12), // ISR LiveState
                                                       (NDE_ISR_ADDR_GEN12), 0, NULL, NULL, 0, FALSE, eNoExecHw, LKFR_MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler, NULL, NULL,
                                                       NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // North DE IIR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21261?dstFilter=ICLHP&mode=Filter
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       (NDE_IIR_ADDR_GEN12), // DE IIR
                                                       (NDE_IIR_ADDR_GEN12), 0, NULL, NULL, 0, TRUE, eReadCombine, NULL, GEN12_CMN_MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler, NULL,
                                                       NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, TYPE_C_HOT_PLUG_CTL_ADDR_GEN12, TYPE_C_HOT_PLUG_CTL_ADDR_GEN12, 0, NULL, NULL, 0, TRUE,
                                                       eNoExecHw, NULL, LKFR_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // MGPhyLanes Handlers - FIA1
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12, PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN12_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // MGPhyLanes Handlers - FIA2
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12, PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN12_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // MGPhyLanes Handlers - FIA3
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12, PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN12_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        /*To handle upfront link training
        Each FIA can have upto 4 instance of scratch pad
        FIA1 - SP1 to SP4
        */
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA1_ADDR_GEN12, PORT_TX_DFLEXDPSP4_FIA1_ADDR_GEN12, 0, NULL, NULL, 0,
                                                       FALSE, eReadCombine, GEN12_CMN_MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        /*To handle upfront link training
        Each FIA can have upto 4 instance of scratch pad
        FIA2 - SP1 to SP4
        */
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA2_ADDR_GEN12, PORT_TX_DFLEXDPSP4_FIA2_ADDR_GEN12, 0, NULL, NULL, 0,
                                                       FALSE, eReadCombine, GEN12_CMN_MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        /*To handle upfront link training
        Each FIA can have upto 4 instance of scratch pad
        FIA3 - SP1 to SP4
        */
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA3_ADDR_GEN12, PORT_TX_DFLEXDPSP4_FIA3_ADDR_GEN12, 0, NULL, NULL, 0,
                                                       FALSE, eReadCombine, GEN12_CMN_MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN LKFR_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
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

BOOLEAN LKFR_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                                bRet             = TRUE;
    SHOTPLUG_CTL_DDI_GEN12                 stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_TC_GEN12                  stHotPlugCtl2    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stLiveStateReg   = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stLiveStateRegHw = { 0 };
    ULONG                                  driverRegValue   = 0;

    stHotPlugCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stHotPlugCtl2.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN12 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

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

    if (stHotPlugCtl2.Tc1HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort1 = FALSE;
    }

    if (stHotPlugCtl2.Tc2HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort2 = FALSE;
    }

    *pulReadData = stLiveStateReg.ulValue;

    return bRet;
}

BOOLEAN LKFR_MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                    bRet                = FALSE;
    SHOTPLUG_CTL_DDI_GEN12     stSouthDDICtlReg    = { 0 };
    SHOTPLUG_CTL_TC_GEN12      stSouthTCCtlreg     = { 0 };
    HOTPLUG_CTL_GEN12          stNorthTCCtlreg     = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stSouthDDICtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthTCCtlreg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthTCCtlreg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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

            // IMP NOTE : For PORTS D, E and F

            // The sequence of checking North DE Register first
            // followed by SOUTH DE register has to be maintianed
            // bec Gfx driver always sets the SOUTH DE registers first
            // and then NORTH DE register as per the bspec.
            // For Ex: for DP_D with TYPE_C enabled port,
            // stNorthTCCtlreg.Port1HpdEnable and stSouthTCCtlreg.Tc1HpdEnable
            // both will be set. But for TYPE_C enabled port, HPD has to be
            // triggered on NORTH DE. Hence stNorthTCCtlreg.Port1HpdEnable is the valid one.
            // Suppose if we reverse the order of checking these registers, then for DP_C with TYPE_C enabled port
            // HPD will be triggered in SOUTH DE as stSouthTCCtlreg.Tc1HpdEnable will also be set.
            // But for DP_D (Legacy) enabled port, only stSouthTCCtlreg.Tc1HpdEnable will be set
            // and HPD will be triggered in SOUTH DE if we follow this sequence.

        case INTDPD_PORT:
        case INTHDMID_PORT:
            if (stNorthTCCtlreg.Port1HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc1HpdEnable && !PortConnectorInfo.IsTypeC && !PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            break;

        case INTDPE_PORT:
        case INTHDMIE_PORT:
            if (stNorthTCCtlreg.Port2HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc2HpdEnable && !PortConnectorInfo.IsTypeC && !PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            break;

        default:
            break;
        }

    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12, stSouthDDICtlReg.ulValue, SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN12,
                        stSouthTCCtlreg.ulValue, TYPE_C_HOT_PLUG_CTL_ADDR_GEN12, stNorthTCCtlreg.ulValue, 0, 0);
    return bRet;
}

BOOLEAN LKFR_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                             PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN               bRet             = FALSE;
    GFX_MSTR_INTR_GEN12   stMasterIntCtrl  = { 0 };
    DISPLAY_INT_CTL_GEN12 stDisplayIntCtrl = { 0 };

    SHOTPLUG_CTL_DDI_GEN12 stSouthCtlReg = { 0 };
    SHOTPLUG_CTL_TC_GEN12  stTCCTLreg    = { 0 };

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stSouthISR = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stSouthIMR = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stSouthIIR = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stSouthIER = { 0 };

    HOTPLUG_CTL_GEN12 stTYPECHotPlugCtl = { 0 };

    DE_HPD_INTR_DEFINITION_GEN12 stNorthISR = { 0 };
    DE_HPD_INTR_DEFINITION_GEN12 stNorthIMR = { 0 };
    DE_HPD_INTR_DEFINITION_GEN12 stNorthIIR = { 0 };
    DE_HPD_INTR_DEFINITION_GEN12 stNorthIER = { 0 };

    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia1Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia2Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia3Status = { 0 };

    PORT_TX_DFLEXDPSP_GEN12 stFIA1LiveState = { 0 };
    PORT_TX_DFLEXDPSP_GEN12 stFIA2LiveState = { 0 };
    PORT_TX_DFLEXDPSP_GEN12 stFIA3LiveState = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Check if HPD has been enabled by Gfx
        if (FALSE == LKFR_MMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType, PortConnectorInfo))
        {
            break;
        }

        stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Bspec Ref; https://gfxspecs.intel.com/Predator/Home/Index/21778
        stSouthCtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21779
        stTCCTLreg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Legacy
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/8409
        stSouthISR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_ISR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthIMR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IMR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthIIR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthIER.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IER_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        stTYPECHotPlugCtl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // TypeC
        stNorthISR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(NDE_ISR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthIMR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(NDE_IMR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthIIR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(NDE_IIR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthIER.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(NDE_IER_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        stTypeCFia1Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stFIA1LiveState.ulValue   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
        case INTHDMIA_PORT:

            if (stSouthCtlReg.DdiaHpdEnable && !stSouthIMR.HotplugDdia && stSouthIER.HotplugDdia)
            {
                if (bIsHPD)
                {
                    stSouthIIR.HotplugDdia = TRUE;
                    stSouthISR.HotplugDdia = bAttach;
                    // Long Pulse
                    stSouthCtlReg.DdiaHpdStatus = 2;
                    bRet                        = TRUE;
                }
                else if (stSouthISR.HotplugDdia) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stSouthIIR.HotplugDdia = TRUE;
                    // Short Pulse
                    stSouthCtlReg.DdiaHpdStatus = 0x1;
                    bRet                        = TRUE;
                }
            }

            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:

            if (stSouthCtlReg.DdibHpdEnable && !stSouthIMR.HotplugDdib && stSouthIER.HotplugDdib)
            {
                if (bIsHPD)
                {
                    stSouthIIR.HotplugDdib      = TRUE;
                    stSouthISR.HotplugDdib      = bAttach;
                    stSouthCtlReg.DdibHpdStatus = 2;
                    bRet                        = TRUE;
                }
                else if (stSouthISR.HotplugDdib) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stSouthIIR.HotplugDdib      = TRUE;
                    stSouthCtlReg.DdibHpdStatus = 0x1;
                    bRet                        = TRUE;
                }
            }

            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port1HpdEnable && !stNorthIMR.Tc1Hotplug && stNorthIER.Tc1Hotplug)
            {
                if (bIsHPD)
                {
                    stNorthIIR.Tc1Hotplug                                        = TRUE;
                    stNorthISR.Tc1Hotplug                                        = bAttach; // LiveState Register
                    stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stFIA1LiveState.Tc0LiveState                                 = bAttach;
                    stTYPECHotPlugCtl.Port1HpdStatus                             = 2;
                    bRet                                                         = TRUE;
                }
                else if (stNorthISR.Tc1Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stNorthIIR.Tc1Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port1HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }

            // Legacy south bridge
            if (stTCCTLreg.Tc1HpdEnable && !stSouthIMR.HotplugTypecPort1 && stSouthIER.HotplugTypecPort1)
            {
                if (bIsHPD)
                {
                    stSouthIIR.HotplugTypecPort1                                 = TRUE;
                    stSouthISR.HotplugTypecPort1                                 = bAttach;
                    stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTCCTLreg.Tc1HpdStatus                                      = 2;
                    bRet                                                         = TRUE;
                }
                else if (stSouthISR.HotplugTypecPort1) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stSouthIIR.HotplugTypecPort1 = TRUE;
                    stTCCTLreg.Tc1HpdStatus      = 0x1;
                    bRet                         = TRUE;
                }
            }

            break;

        case INTDPE_PORT:
        case INTHDMIE_PORT:

            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port2HpdEnable && !stNorthIMR.Tc2Hotplug && stNorthIER.Tc2Hotplug)
            {
                if (bIsHPD)
                {
                    stNorthIIR.Tc2Hotplug                                        = TRUE;
                    stNorthISR.Tc2Hotplug                                        = bAttach; // LiveState Register
                    stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stFIA1LiveState.Tc1LiveState                                 = bAttach;
                    stTYPECHotPlugCtl.Port2HpdStatus                             = 2;
                    bRet                                                         = TRUE;
                }
                else if (stNorthISR.Tc2Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stNorthIIR.Tc2Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port2HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }

            // Legacy south bridge
            if (stTCCTLreg.Tc2HpdEnable && !stSouthIMR.HotplugTypecPort2 && stSouthIER.HotplugTypecPort2)
            {
                if (bIsHPD)
                {
                    stSouthIIR.HotplugTypecPort2                                 = TRUE;
                    stSouthISR.HotplugTypecPort2                                 = bAttach;
                    stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTCCTLreg.Tc2HpdStatus                                      = 2;
                    bRet                                                         = TRUE;
                }
                else if (stSouthISR.HotplugTypecPort2) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stSouthIIR.HotplugTypecPort2 = TRUE;
                    stTCCTLreg.Tc2HpdStatus      = 0x1;
                    bRet                         = TRUE;
                }
            }

            break;

        default:

            break;
        }

    } while (FALSE);

    if (bRet)
    {
        stMasterIntCtrl.DisplayInterruptsPending = TRUE;
        stDisplayIntCtrl.DeHpdInterruptsPending  = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])   = stSouthCtlReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTCCTLreg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])                      = stSouthISR.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset])                      = stSouthIIR.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia1Status.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stFIA1LiveState.ulValue;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTYPECHotPlugCtl.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[NDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])             = stNorthISR.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(NDE_IIR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset])             = stNorthIIR.ulValue;
    }

    return bRet;
}

BOOLEAN LKFR_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                                bRet                = TRUE;
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHLiveReg        = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA             pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;
    DE_HPD_INTR_DEFINITION_GEN12           stDEHPDISR          = { 0 };

    // MG PHY Lines Enabling for Port C & Port D
    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia1Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia2Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia3Status = { 0 };

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stTypeCFia1Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFia2Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFia3Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDISR.ulValue   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[NDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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

        case INTDPD_PORT:
        case INTHDMID_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc1Hotplug = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort1 = bAttach;
            }
            stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
            break;

        case INTDPE_PORT:
        case INTHDMIE_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc2Hotplug = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort2 = bAttach;
            }
            stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        // Below line is a temp workaround
        stPCHLiveReg.HotplugDdia                                                                                                        = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])                 = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[NDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])                 = stDEHPDISR.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia1Status.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia2Status.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia3Status.ulValue;
    }

    return bRet;
}

BOOLEAN LKFR_MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = TRUE;
    // TYPE_C
    HOTPLUG_CTL_GEN12            stHotPlugCtl2  = { 0 };
    DE_HPD_INTR_DEFINITION_GEN12 stLiveStateReg = { 0 };

    stHotPlugCtl2.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN12 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stLiveStateReg.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    // TYPE_C
    if (stHotPlugCtl2.Port1HpdEnable == FALSE)
    {
        stLiveStateReg.Tc1Hotplug = FALSE;
    }

    if (stHotPlugCtl2.Port2HpdEnable == FALSE)
    {
        stLiveStateReg.Tc2Hotplug = FALSE;
    }

    *pulReadData = stLiveStateReg.ulValue;

    return bRet;
}

BOOLEAN LKFR_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    HOTPLUG_CTL_GEN12 stHotPlugCtl     = { 0 };
    HOTPLUG_CTL_GEN12 stHotPlugCtlTemp = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (TYPE_C_HOT_PLUG_CTL_ADDR_GEN12 == ulMMIOOffset)
        {
            pstGlobalMMORegData      = &pstMMIOHandlerInfo->stGlobalMMORegData;
            stHotPlugCtlTemp.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stHotPlugCtl.ulValue = ulWriteData;

            stHotPlugCtl.Port1HpdStatus = stHotPlugCtlTemp.Port1HpdStatus;
            stHotPlugCtl.Port2HpdStatus = stHotPlugCtlTemp.Port2HpdStatus;

            stHotPlugCtlTemp.ulValue = ulWriteData;

            stHotPlugCtl.Port1HpdStatus &= ~stHotPlugCtlTemp.Port1HpdStatus;
            stHotPlugCtl.Port2HpdStatus &= ~stHotPlugCtlTemp.Port2HpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl.ulValue;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

/*
This function will clear the HpdStatus value of a particular DDI
which Gfx Driver wants to.
*/
BOOLEAN LKFR_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/21778
    SHOTPLUG_CTL_DDI_GEN12 stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_DDI_GEN12 stHotPlugCtlTemp = { 0 };

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/21779
    SHOTPLUG_CTL_TC_GEN12 stHotPlugCtl2     = { 0 };
    SHOTPLUG_CTL_TC_GEN12 stHotPlugCtlTemp2 = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 == ulMMIOOffset)
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

            stHotPlugCtlTemp.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stHotPlugCtl.ulValue = ulWriteData;

            stHotPlugCtl.DdiaHpdStatus = stHotPlugCtlTemp.DdiaHpdStatus;
            stHotPlugCtl.DdibHpdStatus = stHotPlugCtlTemp.DdibHpdStatus;

            stHotPlugCtlTemp.ulValue = ulWriteData;

            stHotPlugCtl.DdiaHpdStatus &= ~stHotPlugCtlTemp.DdiaHpdStatus;
            stHotPlugCtl.DdibHpdStatus &= ~stHotPlugCtlTemp.DdibHpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl.ulValue;
        }
        else
        {
            pstGlobalMMORegData       = &pstMMIOHandlerInfo->stGlobalMMORegData;
            stHotPlugCtlTemp2.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stHotPlugCtl2.ulValue = ulWriteData;

            stHotPlugCtl2.Tc1HpdStatus = stHotPlugCtlTemp2.Tc1HpdStatus;
            stHotPlugCtl2.Tc2HpdStatus = stHotPlugCtlTemp2.Tc2HpdStatus;

            stHotPlugCtlTemp2.ulValue = ulWriteData;

            stHotPlugCtl2.Tc1HpdStatus &= ~stHotPlugCtlTemp2.Tc1HpdStatus;
            stHotPlugCtl2.Tc2HpdStatus &= ~stHotPlugCtlTemp2.Tc2HpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl2.ulValue;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}
