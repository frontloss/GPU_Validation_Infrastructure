#include "TGLLPMMIO.h"
#include "..\..\DriverInterfaces\SimDrvToGfx.h"
#include "..\\..\\CommonInclude\\ETWLogging.h"

BOOLEAN TGLLP_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {

        bRet = TGLLP_MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);

    } while (FALSE);

    return bRet;
}

BOOLEAN TGLLP_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
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

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/8409
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_ISR_ADDR_GEN12, SDE_ISR_ADDR_GEN12, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       TGLLP_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);
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
                                                       0, TRUE, eNoExecHw, NULL, TGLLP_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN12, THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN12, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, TGLLP_MMIOHANDLERS_TBTHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, TYPE_C_HOT_PLUG_CTL_ADDR_GEN12, TYPE_C_HOT_PLUG_CTL_ADDR_GEN12, 0, NULL, NULL, 0, TRUE,
                                                       eNoExecHw, NULL, TGLLP_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // DE Engine IIR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21261?dstFilter=ICLHP&mode=Filter
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       (NDE_IIR_ADDR_GEN12), // DE IIR
                                                       (NDE_IIR_ADDR_GEN12), 0, NULL, NULL, 0, TRUE, eReadCombine, NULL, GEN12_CMN_MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler, NULL,
                                                       NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // DE Engine ISR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21261?dstFilter=ICLHP&mode=Filter
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       (NDE_ISR_ADDR_GEN12), // ISR LiveState
                                                       (NDE_ISR_ADDR_GEN12), 0, NULL, NULL, 0, FALSE, eNoExecHw, TGLLP_MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler, NULL, NULL,
                                                       NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // MGPhyLanes Handlers - FIA1
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12, PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12, 0, NULL, NULL, 0,
                                                       TRUE, eReadCombine, NULL, GEN12_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // MGPhyLanes Handlers - FIA2
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12, PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12, 0, NULL, NULL, 0,
                                                       TRUE, eReadCombine, NULL, GEN12_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // MGPhyLanes Handlers - FIA3
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12, PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12, 0, NULL, NULL, 0,
                                                       TRUE, eReadCombine, NULL, GEN12_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
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

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXPA1_FIA1_ADDR_D12, PORT_TX_DFLEXPA1_FIA1_ADDR_D12, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN12_CMN_MMIOHANDLERS_GetPinAssignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXPA1_FIA2_ADDR_D12, PORT_TX_DFLEXPA1_FIA2_ADDR_D12, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN12_CMN_MMIOHANDLERS_GetPinAssignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXPA1_FIA3_ADDR_D12, PORT_TX_DFLEXPA1_FIA3_ADDR_D12, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN12_CMN_MMIOHANDLERS_GetPinAssignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Workaround to support TypeC ports. In the default mode for TC ports, IOM wouldn't have initialized PHY. So, the DDI Buffer is IDLE. As per the recommendation from
        // Ganesh/Raghu, it is being masked in valsim.
        for (int ddi_offset = DDI_BUF_CTL_USBC1_ADDR_D12; ddi_offset <= DDI_BUF_CTL_USBC6_ADDR_D12; ddi_offset += 256)
        {
            bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, ddi_offset, ddi_offset, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                           TGLLP_MMIOHANDLERS_DdiBufferControlMMIOReadHandler, NULL, NULL, NULL, NULL);

            if (bRet == FALSE)
            {
                break;
            }
        }

        if (bRet == FALSE)
        {
            break;
        }

        // Workaround to support TypeC ports. In the default mode for TC ports, IOM wouldn't have initialized PHY. So, the Powerwell DDI status bit is not set. As per the
        // recommendation from Ganesh/Raghu, it is being masked in valsim.
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PWR_WELL_CTL_DDI2_ADDR_D12, PWR_WELL_CTL_DDI2_ADDR_D12, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       TGLLP_MMIOHANDLERS_PwrWellDDIControlMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN TGLLP_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
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

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = DDI_AUX_DATA_C_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = DDI_AUX_DATA_C_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = DDI_AUX_CTL_C_GEN12;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = DDI_AUX_DATA_TC1_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = DDI_AUX_DATA_TC1_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = DDI_AUX_CTL_TC1_GEN12;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_START] = DDI_AUX_DATA_TC2_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_END]   = DDI_AUX_DATA_TC2_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_E]        = DDI_AUX_CTL_TC2_GEN12;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_START] = DDI_AUX_DATA_TC3_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_END]   = DDI_AUX_DATA_TC3_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_F]        = DDI_AUX_CTL_TC3_GEN12;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_G_START] = DDI_AUX_DATA_TC4_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_G_END]   = DDI_AUX_DATA_TC4_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_G]        = DDI_AUX_CTL_TC4_GEN12;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_H_START] = DDI_AUX_DATA_TC5_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_H_END]   = DDI_AUX_DATA_TC5_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_H]        = DDI_AUX_CTL_TC5_GEN12;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_I_START] = DDI_AUX_DATA_TC6_START_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_I_END]   = DDI_AUX_DATA_TC6_END_GEN12;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_I]        = DDI_AUX_CTL_TC6_GEN12;

        // Every new offset should be added above this. So as to invalidate the rest
        // Do below: ulCount = [Last enum in above list] + 1;
        ulCount = eINDEX_DDI_AUX_CTL_I + 1;
        for (; ulCount < MAX_GEN_MMIO_OFFSETS_STORED; ulCount++)
        {
            pstMMIOInterface->pulGenMMIOOffsetArray[ulCount] = OFFSET_INVALID;
        }

        bRet = TRUE;
    }

    return bRet;
}

// bIsHPD == FALSE ==> SPI
BOOLEAN TGLLP_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                              PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN               bRet             = FALSE;
    GFX_MSTR_INTR_GEN12   stMasterIntCtrl  = { 0 };
    DISPLAY_INT_CTL_GEN12 stDisplayIntCtrl = { 0 };

    SHOTPLUG_CTL_DDI_GEN12 stSouthCtlReg = { 0 };
    SHOTPLUG_CTL_TC_GEN12  stTCCTLreg    = { 0 };

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHLiveReg = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHIMRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHIIRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHIERReg  = { 0 };

    HOTPLUG_CTL_GEN12 stTBTHotPlugCtl   = { 0 };
    HOTPLUG_CTL_GEN12 stTYPECHotPlugCtl = { 0 };

    DE_HPD_INTR_DEFINITION_GEN12 stDEHPDISR = { 0 };
    DE_HPD_INTR_DEFINITION_GEN12 stDEHPDIMR = { 0 };
    DE_HPD_INTR_DEFINITION_GEN12 stDEHPDIIR = { 0 };
    DE_HPD_INTR_DEFINITION_GEN12 stDEHPDIER = { 0 };

    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia1Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia2Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia3Status = { 0 };

    PORT_TX_DFLEXDPSP_GEN12 stFia1LiveState = { 0 };
    PORT_TX_DFLEXDPSP_GEN12 stFia2LiveState = { 0 };
    PORT_TX_DFLEXDPSP_GEN12 stFia3LiveState = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Check if HPD has been enabled by Gfx
        if (FALSE == TGLLP_MMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType, PortConnectorInfo))
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
        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_ISR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IMR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IER_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        stTBTHotPlugCtl.ulValue   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTYPECHotPlugCtl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // TypeC or TBT
        stDEHPDISR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(NDE_ISR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIMR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(NDE_IMR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIIR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(NDE_IIR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIER.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(NDE_IER_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        stTypeCFia1Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFia2Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFia3Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stFia1LiveState.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stFia2LiveState.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_FIA2_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stFia3LiveState.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_FIA3_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
        case INTHDMIA_PORT:
            if (stSouthCtlReg.DdiaHpdEnable && !stPCHIMRReg.HotplugDdia && stPCHIERReg.HotplugDdia)
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

            if (stSouthCtlReg.DdibHpdEnable && !stPCHIMRReg.HotplugDdib && stPCHIERReg.HotplugDdib)
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

            if (stSouthCtlReg.DdicHpdEnable && !stPCHIMRReg.HotplugDdic && stPCHIERReg.HotplugDdic)
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
                    stSouthCtlReg.DdibHpdStatus = 0x1;
                    bRet                        = TRUE;
                }
            }

            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port1HpdEnable && !stDEHPDIMR.Tc1Hotplug && stDEHPDIER.Tc1Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc1Hotplug                                        = TRUE;
                    stDEHPDISR.Tc1Hotplug                                        = bAttach; // LiveState Register
                    stFia1LiveState.Tc0LiveState                                 = bAttach; // LiveState Register
                    stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTYPECHotPlugCtl.Port1HpdStatus                             = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tc1Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc1Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port1HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }
            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port1HpdEnable && !stDEHPDIMR.Tbt1Hotplug && stDEHPDIER.Tbt1Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt1Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt1Hotplug                                       = bAttach; // LiveState Register
                    stFia1LiveState.Tbt0LiveState                                = bAttach; // LiveState Register
                    stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTBTHotPlugCtl.Port1HpdStatus                               = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tbt1Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt1Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port1HpdStatus = 0x1;
                    bRet                           = TRUE;
                }
            }
            // Legacy south bridge
            if (stTCCTLreg.Tc1HpdEnable && !stPCHIMRReg.HotplugTypecPort1 && stPCHIERReg.HotplugTypecPort1)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort1                                = TRUE;
                    stPCHLiveReg.HotplugTypecPort1                               = bAttach;
                    stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTCCTLreg.Tc1HpdStatus                                      = 2;
                    bRet                                                         = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort1) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort1 = TRUE;
                    stTCCTLreg.Tc1HpdStatus       = 0x1;
                    bRet                          = TRUE;
                }
            }
            break;
        case INTDPE_PORT:
        case INTHDMIE_PORT:
            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port2HpdEnable && !stDEHPDIMR.Tc2Hotplug && stDEHPDIER.Tc2Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc2Hotplug                                        = TRUE;
                    stDEHPDISR.Tc2Hotplug                                        = bAttach; // LiveState Register
                    stFia1LiveState.Tc1LiveState                                 = bAttach; // LiveState Register
                    stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTYPECHotPlugCtl.Port2HpdStatus                             = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tc2Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc2Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port2HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }
            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port2HpdEnable && !stDEHPDIMR.Tbt2Hotplug && stDEHPDIER.Tbt2Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt2Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt2Hotplug                                       = bAttach; // LiveState Register
                    stFia1LiveState.Tbt1LiveState                                = bAttach; // LiveState Register
                    stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTBTHotPlugCtl.Port2HpdStatus                               = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tbt2Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt2Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port2HpdStatus = 0x1;
                    bRet                           = TRUE;
                }
            }
            // Legacy south bridge
            if (stTCCTLreg.Tc2HpdEnable && !stPCHIMRReg.HotplugTypecPort2 && stPCHIERReg.HotplugTypecPort2)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort2                                = TRUE;
                    stPCHLiveReg.HotplugTypecPort2                               = bAttach;
                    stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTCCTLreg.Tc2HpdStatus                                      = 2;
                    bRet                                                         = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort2) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort2 = TRUE;
                    stTCCTLreg.Tc2HpdStatus       = 0x1;
                    bRet                          = TRUE;
                }
            }
            break;
        case INTDPF_PORT:
        case INTHDMIF_PORT:
            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port3HpdEnable && !stDEHPDIMR.Tc3Hotplug && stDEHPDIER.Tc3Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc3Hotplug                                        = TRUE;
                    stDEHPDISR.Tc3Hotplug                                        = bAttach; // LiveState Register
                    stFia2LiveState.Tc0LiveState                                 = bAttach; // LiveState Register
                    stTypeCFia2Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTYPECHotPlugCtl.Port3HpdStatus                             = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tc3Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc3Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port3HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }
            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port3HpdEnable && !stDEHPDIMR.Tbt3Hotplug && stDEHPDIER.Tbt3Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt3Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt3Hotplug                                       = bAttach; // LiveState Register
                    stFia2LiveState.Tbt0LiveState                                = bAttach; // LiveState Register
                    stTypeCFia2Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTBTHotPlugCtl.Port3HpdStatus                               = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tbt3Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt3Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port3HpdStatus = 0x1;
                    bRet                           = TRUE;
                }
            }
            // Legacy south bridge
            if (stTCCTLreg.Tc3HpdEnable && !stPCHIMRReg.HotplugTypecPort3 && stPCHIERReg.HotplugTypecPort3)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort3                                = TRUE;
                    stPCHLiveReg.HotplugTypecPort3                               = bAttach;
                    stTypeCFia2Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTCCTLreg.Tc3HpdStatus                                      = 2;
                    bRet                                                         = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort3) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort3 = TRUE;
                    stTCCTLreg.Tc3HpdStatus       = 0x1;
                    bRet                          = TRUE;
                }
            }
            break;
        case INTDPG_PORT:
        case INTHDMIG_PORT:
            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port4HpdEnable && !stDEHPDIMR.Tc4Hotplug && stDEHPDIER.Tc4Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc4Hotplug                                        = TRUE;
                    stDEHPDISR.Tc4Hotplug                                        = bAttach; // LiveState Register
                    stFia2LiveState.Tc1LiveState                                 = bAttach; // LiveState Register
                    stTypeCFia2Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTYPECHotPlugCtl.Port4HpdStatus                             = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tc4Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc4Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port4HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }
            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port4HpdEnable && !stDEHPDIMR.Tbt4Hotplug && stDEHPDIER.Tbt4Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt4Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt4Hotplug                                       = bAttach; // LiveState Register
                    stFia2LiveState.Tbt1LiveState                                = bAttach; // LiveState Register
                    stTypeCFia2Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTBTHotPlugCtl.Port4HpdStatus                               = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tbt4Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt4Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port4HpdStatus = 0x1;
                    bRet                           = TRUE;
                }
            }
            // Legacy south bridge
            if (stTCCTLreg.Tc4HpdEnable && !stPCHIMRReg.HotplugTypecPort4 && stPCHIERReg.HotplugTypecPort4)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort4                                = TRUE;
                    stPCHLiveReg.HotplugTypecPort4                               = bAttach;
                    stTypeCFia2Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTCCTLreg.Tc4HpdStatus                                      = 2;
                    bRet                                                         = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort4) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort4 = TRUE;
                    stTCCTLreg.Tc4HpdStatus       = 0x1;
                    bRet                          = TRUE;
                }
            }
            break;
        case INTDPH_PORT:
        case INTHDMIH_PORT:
            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port5HpdEnable && !stDEHPDIMR.Tc5Hotplug && stDEHPDIER.Tc5Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc5Hotplug                                        = TRUE;
                    stDEHPDISR.Tc5Hotplug                                        = bAttach; // LiveState Register
                    stFia3LiveState.Tc0LiveState                                 = bAttach; // LiveState Register
                    stTypeCFia3Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTYPECHotPlugCtl.Port5HpdStatus                             = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tc5Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc5Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port5HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }
            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port5HpdEnable && !stDEHPDIMR.Tbt5Hotplug && stDEHPDIER.Tbt5Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt5Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt5Hotplug                                       = bAttach; // LiveState Register
                    stFia3LiveState.Tbt0LiveState                                = bAttach; // LiveState Register
                    stTypeCFia3Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTBTHotPlugCtl.Port5HpdStatus                               = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tbt5Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt5Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port5HpdStatus = 0x1;
                    bRet                           = TRUE;
                }
            }
            // Legacy south bridge
            if (stTCCTLreg.Tc5HpdEnable && !stPCHIMRReg.HotplugTypecPort5 && stPCHIERReg.HotplugTypecPort5)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort5                                = TRUE;
                    stPCHLiveReg.HotplugTypecPort5                               = bAttach;
                    stTypeCFia3Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTCCTLreg.Tc5HpdStatus                                      = 2;
                    bRet                                                         = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort5) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort5 = TRUE;
                    stTCCTLreg.Tc5HpdStatus       = 0x1;
                    bRet                          = TRUE;
                }
            }
            break;
        case INTDPI_PORT:
        case INTHDMII_PORT:
            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port6HpdEnable && !stDEHPDIMR.Tc6Hotplug && stDEHPDIER.Tc6Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc6Hotplug                                        = TRUE;
                    stDEHPDISR.Tc6Hotplug                                        = bAttach; // LiveState Register
                    stFia3LiveState.Tc1LiveState                                 = bAttach; // LiveState Register
                    stTypeCFia3Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTYPECHotPlugCtl.Port6HpdStatus                             = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tc6Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc6Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port6HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }
            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port6HpdEnable && !stDEHPDIMR.Tbt6Hotplug && stDEHPDIER.Tbt6Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt6Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt6Hotplug                                       = bAttach; // LiveState Register
                    stFia3LiveState.Tbt1LiveState                                = bAttach; // LiveState Register
                    stTypeCFia3Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTBTHotPlugCtl.Port6HpdStatus                               = 2;
                    bRet                                                         = TRUE;
                }
                else if (stDEHPDISR.Tbt6Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt6Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port6HpdStatus = 0x1;
                    bRet                           = TRUE;
                }
            }
            // Legacy south bridge
            if (stTCCTLreg.Tc6HpdEnable && !stPCHIMRReg.HotplugTypecPort6 && stPCHIERReg.HotplugTypecPort6)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort6                                = TRUE;
                    stPCHLiveReg.HotplugTypecPort6                               = bAttach;
                    stTypeCFia3Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTCCTLreg.Tc6HpdStatus                                      = 2;
                    bRet                                                         = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort6) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort6 = TRUE;
                    stTCCTLreg.Tc6HpdStatus       = 0x1;
                    bRet                          = TRUE;
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
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])                      = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset])                      = stPCHIIRReg.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stFia1LiveState.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_FIA2_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stFia2LiveState.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_FIA3_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stFia3LiveState.ulValue;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia1Status.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia2Status.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia3Status.ulValue;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTBTHotPlugCtl.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])      = stTYPECHotPlugCtl.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[NDE_ISR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset])                  = stDEHPDISR.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(NDE_IIR_ADDR_GEN12)-pstGlobalMMORegData->ulMMIOBaseOffset])                  = stDEHPDIIR.ulValue;
    }

    return bRet;
}

// TODO: Need to take care of TBT/TypeC
BOOLEAN TGLLP_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                                bRet                = TRUE;
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stPCHLiveReg        = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA             pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;
    DE_HPD_INTR_DEFINITION_GEN12           stDEHPDISR          = { 0 };

    // MG PHY Lines Enabling for Port D - Port F
    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia1Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia2Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia3Status = { 0 };

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        /* get current TYPE C FIA Status from val-sim MMIO database before before enabling MG PHY lane for different ports (BUG ID - 1607574661)  */
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

        case INTDPC_PORT:
        case INTHDMIC_PORT:
            stPCHLiveReg.HotplugDdic = bAttach;
            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc1Hotplug = bAttach;
            }
            else if (PortConnectorInfo.IsTbt)
            {
                stDEHPDISR.Tbt1Hotplug = bAttach;
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
            else if (PortConnectorInfo.IsTbt)
            {
                stDEHPDISR.Tbt2Hotplug = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort2 = bAttach;
            }
            stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc3Hotplug = bAttach;
            }
            else if (PortConnectorInfo.IsTbt)
            {
                stDEHPDISR.Tbt3Hotplug = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort3 = bAttach;
            }
            stTypeCFia2Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
            break;

        case INTDPG_PORT:
        case INTHDMIG_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc4Hotplug = bAttach;
            }
            else if (PortConnectorInfo.IsTbt)
            {
                stDEHPDISR.Tbt4Hotplug = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort4 = bAttach;
            }
            stTypeCFia2Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
            break;

        case INTDPH_PORT:
        case INTHDMIH_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc5Hotplug = bAttach;
            }
            else if (PortConnectorInfo.IsTbt)
            {
                stDEHPDISR.Tbt5Hotplug = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort5 = bAttach;
            }
            stTypeCFia3Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
            break;

        case INTDPI_PORT:
        case INTHDMII_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc6Hotplug = bAttach;
            }
            else if (PortConnectorInfo.IsTbt)
            {
                stDEHPDISR.Tbt6Hotplug = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort6 = bAttach;
            }
            stTypeCFia3Status.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
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

BOOLEAN TGLLP_MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                    bRet                = FALSE;
    SHOTPLUG_CTL_DDI_GEN12     stSouthDDICtlReg    = { 0 };
    SHOTPLUG_CTL_TC_GEN12      stSouthTCCtlreg     = { 0 };
    HOTPLUG_CTL_GEN12          stNorthTCCtlreg     = { 0 };
    HOTPLUG_CTL_GEN12          stNorthTBTCtlreg    = { 0 };
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
        stNorthTBTCtlreg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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
            else if (stNorthTBTCtlreg.Port1HpdEnable && PortConnectorInfo.IsTbt)
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
            else if (stNorthTBTCtlreg.Port2HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc2HpdEnable && !PortConnectorInfo.IsTypeC && !PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            if (stNorthTCCtlreg.Port3HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port3HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc3HpdEnable && !PortConnectorInfo.IsTypeC && !PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            break;

        case INTDPG_PORT:
        case INTHDMIG_PORT:
            if (stNorthTCCtlreg.Port4HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port4HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc4HpdEnable && !PortConnectorInfo.IsTypeC && !PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            break;

        case INTDPH_PORT:
        case INTHDMIH_PORT:
            if (stNorthTCCtlreg.Port5HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port5HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc5HpdEnable && !PortConnectorInfo.IsTypeC && !PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            break;

        case INTDPI_PORT:
        case INTHDMII_PORT:
            if (stNorthTCCtlreg.Port6HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port6HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc6HpdEnable && !PortConnectorInfo.IsTypeC && !PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            break;

        default:
            break;
        }

    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN12, stSouthDDICtlReg.ulValue, SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN12,
                        stSouthTCCtlreg.ulValue, TYPE_C_HOT_PLUG_CTL_ADDR_GEN12, stNorthTCCtlreg.ulValue, THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN12, stNorthTBTCtlreg.ulValue);
    return bRet;
}

BOOLEAN TGLLP_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
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

    if (stHotPlugCtl.DdicHpdEnable == FALSE)
    {
        stLiveStateReg.HotplugDdic = FALSE;
    }

    if (stHotPlugCtl2.Tc1HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort1 = FALSE;
    }

    if (stHotPlugCtl2.Tc2HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort2 = FALSE;
    }

    if (stHotPlugCtl2.Tc3HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort3 = FALSE;
    }

    if (stHotPlugCtl2.Tc4HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort4 = FALSE;
    }

    if (stHotPlugCtl2.Tc5HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort5 = FALSE;
    }

    if (stHotPlugCtl2.Tc6HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort6 = FALSE;
    }

    *pulReadData = stLiveStateReg.ulValue;

    return bRet;
}

/*
This function will clear the HpdStatus value of a perticular DDI
which Gfx Driver wants to.
*/
BOOLEAN TGLLP_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/21778
    SHOTPLUG_CTL_DDI_GEN12 stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_DDI_GEN12 stHotPlugCtlTemp = { 0 };

    /* SPT_HOTPLUG_CTL2_REG_ST stHotPlugCtl2 = { 0 };
    SPT_HOTPLUG_CTL2_REG_ST stHotPlugCtlTemp2 = { 0 };*/

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
            stHotPlugCtl.DdicHpdStatus = stHotPlugCtlTemp.DdicHpdStatus;

            stHotPlugCtlTemp.ulValue = ulWriteData;

            stHotPlugCtl.DdiaHpdStatus &= ~stHotPlugCtlTemp.DdiaHpdStatus;
            stHotPlugCtl.DdibHpdStatus &= ~stHotPlugCtlTemp.DdibHpdStatus;
            stHotPlugCtl.DdicHpdStatus &= ~stHotPlugCtlTemp.DdicHpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl.ulValue;
        }
        else
        {
            pstGlobalMMORegData       = &pstMMIOHandlerInfo->stGlobalMMORegData;
            stHotPlugCtlTemp2.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stHotPlugCtl2.ulValue = ulWriteData;

            stHotPlugCtl2.Tc1HpdStatus = stHotPlugCtlTemp2.Tc1HpdStatus;
            stHotPlugCtl2.Tc2HpdStatus = stHotPlugCtlTemp2.Tc2HpdStatus;
            stHotPlugCtl2.Tc3HpdStatus = stHotPlugCtlTemp2.Tc3HpdStatus;
            stHotPlugCtl2.Tc4HpdStatus = stHotPlugCtlTemp2.Tc4HpdStatus;
            stHotPlugCtl2.Tc5HpdStatus = stHotPlugCtlTemp2.Tc5HpdStatus;
            stHotPlugCtl2.Tc6HpdStatus = stHotPlugCtlTemp2.Tc6HpdStatus;

            stHotPlugCtlTemp2.ulValue = ulWriteData;

            stHotPlugCtl2.Tc1HpdStatus &= ~stHotPlugCtlTemp2.Tc1HpdStatus;
            stHotPlugCtl2.Tc2HpdStatus &= ~stHotPlugCtlTemp2.Tc2HpdStatus;
            stHotPlugCtl2.Tc3HpdStatus &= ~stHotPlugCtlTemp2.Tc3HpdStatus;
            stHotPlugCtl2.Tc4HpdStatus &= ~stHotPlugCtlTemp2.Tc4HpdStatus;
            stHotPlugCtl2.Tc5HpdStatus &= ~stHotPlugCtlTemp2.Tc5HpdStatus;
            stHotPlugCtl2.Tc6HpdStatus &= ~stHotPlugCtlTemp2.Tc6HpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl2.ulValue;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN TGLLP_MMIOHANDLERS_TBTHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    HOTPLUG_CTL_GEN12 stHotPlugCtl     = { 0 };
    HOTPLUG_CTL_GEN12 stHotPlugCtlTemp = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN12 == ulMMIOOffset)
        {
            pstGlobalMMORegData      = &pstMMIOHandlerInfo->stGlobalMMORegData;
            stHotPlugCtlTemp.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stHotPlugCtl.ulValue = ulWriteData;

            stHotPlugCtl.Port1HpdStatus = stHotPlugCtlTemp.Port1HpdStatus;
            stHotPlugCtl.Port2HpdStatus = stHotPlugCtlTemp.Port2HpdStatus;
            stHotPlugCtl.Port3HpdStatus = stHotPlugCtlTemp.Port3HpdStatus;
            stHotPlugCtl.Port4HpdStatus = stHotPlugCtlTemp.Port4HpdStatus;

            stHotPlugCtl.Port5HpdStatus = stHotPlugCtlTemp.Port5HpdStatus;
            stHotPlugCtl.Port6HpdStatus = stHotPlugCtlTemp.Port6HpdStatus;
            stHotPlugCtl.Port7HpdStatus = stHotPlugCtlTemp.Port7HpdStatus;
            stHotPlugCtl.Port8HpdStatus = stHotPlugCtlTemp.Port8HpdStatus;

            stHotPlugCtlTemp.ulValue = ulWriteData;

            stHotPlugCtl.Port1HpdStatus &= ~stHotPlugCtlTemp.Port1HpdStatus;
            stHotPlugCtl.Port2HpdStatus &= ~stHotPlugCtlTemp.Port2HpdStatus;
            stHotPlugCtl.Port3HpdStatus &= ~stHotPlugCtlTemp.Port3HpdStatus;
            stHotPlugCtl.Port4HpdStatus &= ~stHotPlugCtlTemp.Port4HpdStatus;

            stHotPlugCtl.Port5HpdStatus &= ~stHotPlugCtlTemp.Port5HpdStatus;
            stHotPlugCtl.Port6HpdStatus &= ~stHotPlugCtlTemp.Port6HpdStatus;
            stHotPlugCtl.Port7HpdStatus &= ~stHotPlugCtlTemp.Port7HpdStatus;
            stHotPlugCtl.Port8HpdStatus &= ~stHotPlugCtlTemp.Port8HpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl.ulValue;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN TGLLP_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
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
            stHotPlugCtl.Port3HpdStatus = stHotPlugCtlTemp.Port3HpdStatus;
            stHotPlugCtl.Port4HpdStatus = stHotPlugCtlTemp.Port4HpdStatus;

            stHotPlugCtl.Port5HpdStatus = stHotPlugCtlTemp.Port5HpdStatus;
            stHotPlugCtl.Port6HpdStatus = stHotPlugCtlTemp.Port6HpdStatus;
            stHotPlugCtl.Port7HpdStatus = stHotPlugCtlTemp.Port7HpdStatus;
            stHotPlugCtl.Port8HpdStatus = stHotPlugCtlTemp.Port8HpdStatus;

            stHotPlugCtlTemp.ulValue = ulWriteData;

            stHotPlugCtl.Port1HpdStatus &= ~stHotPlugCtlTemp.Port1HpdStatus;
            stHotPlugCtl.Port2HpdStatus &= ~stHotPlugCtlTemp.Port2HpdStatus;
            stHotPlugCtl.Port3HpdStatus &= ~stHotPlugCtlTemp.Port3HpdStatus;
            stHotPlugCtl.Port4HpdStatus &= ~stHotPlugCtlTemp.Port4HpdStatus;

            stHotPlugCtl.Port5HpdStatus &= ~stHotPlugCtlTemp.Port5HpdStatus;
            stHotPlugCtl.Port6HpdStatus &= ~stHotPlugCtlTemp.Port6HpdStatus;
            stHotPlugCtl.Port7HpdStatus &= ~stHotPlugCtlTemp.Port7HpdStatus;
            stHotPlugCtl.Port8HpdStatus &= ~stHotPlugCtlTemp.Port8HpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl.ulValue;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN TGLLP_MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = TRUE;
    // THUNDERBOLT
    HOTPLUG_CTL_GEN12 stHotPlugCtl = { 0 };
    // TYPE_C
    HOTPLUG_CTL_GEN12            stHotPlugCtl2  = { 0 };
    DE_HPD_INTR_DEFINITION_GEN12 stLiveStateReg = { 0 };

    stHotPlugCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN12 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stHotPlugCtl2.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN12 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stLiveStateReg.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    // THUNDERBOLT
    if (stHotPlugCtl.Port1HpdEnable == FALSE)
    {
        stLiveStateReg.Tbt1Hotplug = FALSE;
    }

    if (stHotPlugCtl.Port2HpdEnable == FALSE)
    {
        stLiveStateReg.Tbt2Hotplug = FALSE;
    }

    if (stHotPlugCtl.Port3HpdEnable == FALSE)
    {
        stLiveStateReg.Tbt3Hotplug = FALSE;
    }

    if (stHotPlugCtl.Port4HpdEnable == FALSE)
    {
        stLiveStateReg.Tbt4Hotplug = FALSE;
    }

    if (stHotPlugCtl.Port5HpdEnable == FALSE)
    {
        stLiveStateReg.Tbt5Hotplug = FALSE;
    }

    if (stHotPlugCtl.Port6HpdEnable == FALSE)
    {
        stLiveStateReg.Tbt6Hotplug = FALSE;
    }

    if (stHotPlugCtl.Port7HpdEnable == FALSE)
    {
        stLiveStateReg.Tbt7Hotplug = FALSE;
    }

    if (stHotPlugCtl.Port8HpdEnable == FALSE)
    {
        stLiveStateReg.Tbt8Hotplug = FALSE;
    }

    // TYPE_C
    if (stHotPlugCtl2.Port1HpdEnable == FALSE)
    {
        stLiveStateReg.Tc1Hotplug = FALSE;
    }

    if (stHotPlugCtl2.Port2HpdEnable == FALSE)
    {
        stLiveStateReg.Tc2Hotplug = FALSE;
    }

    if (stHotPlugCtl2.Port3HpdEnable == FALSE)
    {
        stLiveStateReg.Tc3Hotplug = FALSE;
    }

    if (stHotPlugCtl2.Port4HpdEnable == FALSE)
    {
        stLiveStateReg.Tc4Hotplug = FALSE;
    }

    if (stHotPlugCtl2.Port5HpdEnable == FALSE)
    {
        stLiveStateReg.Tc5Hotplug = FALSE;
    }

    if (stHotPlugCtl2.Port6HpdEnable == FALSE)
    {
        stLiveStateReg.Tc6Hotplug = FALSE;
    }

    if (stHotPlugCtl2.Port7HpdEnable == FALSE)
    {
        stLiveStateReg.Tc7Hotplug = FALSE;
    }

    if (stHotPlugCtl2.Port8HpdEnable == FALSE)
    {
        stLiveStateReg.Tc8Hotplug = FALSE;
    }

    *pulReadData = stLiveStateReg.ulValue;

    return bRet;
}

BOOLEAN TGLLP_MMIOHANDLERS_DdiBufferControlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN            bRet            = TRUE;
    DDI_BUF_CTL_D12    stDdiBufCtlReg  = { 0 };
    PSIMDEV_EXTENTSION pstSimDrvDevExt = GetSimDrvExtension();

    ULONG driverRegValue = 0;
    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, ulMMIOOffset, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        stDdiBufCtlReg.Value = driverRegValue;

        if (stDdiBufCtlReg.DdiBufferEnable == TRUE)
        {
            stDdiBufCtlReg.DdiIdleStatus = FALSE;
        }

        *pulReadData = stDdiBufCtlReg.Value;
    }
    else
    {
        bRet = FALSE;
    }

    return bRet;
}

BOOLEAN TGLLP_MMIOHANDLERS_PwrWellDDIControlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN              bRet               = TRUE;
    PWR_WELL_CTL_DDI_D12 stPwrWellDdiCtlReg = { 0 };

    stPwrWellDdiCtlReg.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (stPwrWellDdiCtlReg.Usbc1IoPowerRequest == TRUE)
    {
        stPwrWellDdiCtlReg.Usbc1IoPowerState = TRUE;
    }

    if (stPwrWellDdiCtlReg.Usbc2IoPowerRequest == TRUE)
    {
        stPwrWellDdiCtlReg.Usbc2IoPowerState = TRUE;
    }

    if (stPwrWellDdiCtlReg.Usbc3IoPowerRequest == TRUE)
    {
        stPwrWellDdiCtlReg.Usbc3IoPowerState = TRUE;
    }

    if (stPwrWellDdiCtlReg.Usbc4IoPowerRequest == TRUE)
    {
        stPwrWellDdiCtlReg.Usbc4IoPowerState = TRUE;
    }

    if (stPwrWellDdiCtlReg.Usbc5IoPowerRequest == TRUE)
    {
        stPwrWellDdiCtlReg.Usbc5IoPowerState = TRUE;
    }

    if (stPwrWellDdiCtlReg.Usbc6IoPowerRequest == TRUE)
    {
        stPwrWellDdiCtlReg.Usbc6IoPowerState = TRUE;
    }

    *pulReadData = stPwrWellDdiCtlReg.Value;

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    return bRet;
}

BOOLEAN TGLLP_MMIOHANDLERS_ScdcInterruptGeneration(PMMIO_INTERFACE pstMMIOInterface, PSCDC_ARGS pstScdcArgs)
{
    BOOLEAN                                bRet             = FALSE;
    GFX_MSTR_INTR_GEN12                    stMasterIntCtrl  = { 0 };
    DISPLAY_INT_CTL_GEN12                  stDisplayIntCtrl = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN12 stSouthDeInt     = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

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
            stSouthDeInt.ScdcTc1 = TRUE;
            bRet                 = TRUE;
            break;
        case INTHDMIE_PORT:
            stSouthDeInt.ScdcTc2 = TRUE;
            bRet                 = TRUE;
            break;
        case INTHDMIF_PORT:
            stSouthDeInt.ScdcTc3 = TRUE;
            bRet                 = TRUE;
            break;
        case INTHDMIG_PORT:
            stSouthDeInt.ScdcTc4 = TRUE;
            bRet                 = TRUE;
            break;
        case INTHDMIH_PORT:
            stSouthDeInt.ScdcTc5 = TRUE;
            bRet                 = TRUE;
            break;
        case INTHDMII_PORT:
            stSouthDeInt.ScdcTc6 = TRUE;
            bRet                 = TRUE;
            break;
        default:
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        stMasterIntCtrl.DisplayInterruptsPending = TRUE;

        stDisplayIntCtrl.DePchInterruptsPending = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthDeInt.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;
    }

    return bRet;
}
