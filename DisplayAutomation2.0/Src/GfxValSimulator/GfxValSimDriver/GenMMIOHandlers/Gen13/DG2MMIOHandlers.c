/**********************************************************************************************************
DG2 HPD Flow

MASTER_CTL_INT(0x190010) - MasterInterruptRW[Gfx IP or others] Get the Interrupt Source ie Display Interrupt
DISPLAY_INTR_CTL_ADDR_ICL(0x44200) - DisplayInterruptRW[Display, GPU or Render] Get the Legacy Interrupt Source means is it HPD/Port/Pipe/Audio
SOUTH_DE_IIR_ADDR_SPT(0xC4008) - HotPlugIIRWrite[Pipe or Port interrupt Interrupt Source ie PCH Display]
SOUTH_HOT_PLUG_CTL_ADDR_SPT(0xC4030) - HotPlugCTLWrite[Which port is being connected? Short or Long Pulse]

SOUTH_DE_ISR_ADDR_SPT(0xc4000) - HotPlugLiveStateRead[Connected / Disconnected]


Call Flow: Gfx Mainline Driver: Legacy:
1. DG2_INTRHANDLER_GetInterruptSource  ---> case DG2_DISPLAY_INTERRUPT_BIT_POS --> LegacyInterruptsOccurred Flag should be set
2. DG2_INTRHANDLER_GetLegacyInterruptSource
3. DG2_INTRHANDLER_GetHPDInterruptSource

********************************************************************************************************/
#include "DG2MMIO.h"
#include "..\..\DriverInterfaces\SimDrvToGfx.h"
#include "..\\..\\CommonInclude\\ETWLogging.h"

BOOLEAN DG2_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {
        bRet = DG2_MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);
    } while (FALSE);

    return bRet;
}

BOOLEAN DG2_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
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
        COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_TILE_INTR_ADDR_DG2, GFX_MSTR_TILE_INTR_ADDR_DG2, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                DG2_MMIOHANDLERS_MasterTileInterruptCtlMMIOReadHandler, DG2_MMIOHANDLERS_MasterTileInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // TODO: Can we remove the below?
        // Master Interrupt Control Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/53222
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_INTR_ADDR_GEN13, GFX_MSTR_INTR_ADDR_GEN13, 0, NULL, NULL, 0, TRUE, eReadCombine,
                                                       NULL, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Display Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/20451
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DISPLAY_INTR_CTL_ADDR_GEN13, DISPLAY_INTR_CTL_ADDR_GEN13, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN13_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler, GEN13_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler, NULL,
                                                       NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/49961
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_ISR_ADDR_DG2, SDE_ISR_ADDR_DG2, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       DG2_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_IIR_ADDR_DG2, SDE_IIR_ADDR_DG2, 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       GEN13_CMN_MMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/49956
        // The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port
        // These two are the south hot plug control registers
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SHOTPLUG_CTL_DDI_ADDR_DG2, SHOTPLUG_CTL_TC_ADDR_DG2, 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       DG2_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50093
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, TC_HOTPLUG_CTL_ADDR_D13, TC_HOTPLUG_CTL_ADDR_D13, 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       DG2_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        // DE Engine IIR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50062
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DE_HPD_IIR_ADDR_D13, DE_HPD_IIR_ADDR_D13, 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       GEN13_CMN_MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler, NULL, NULL, NULL); // DE IIR

        if (bRet == FALSE)
        {
            break;
        }

        // DE Engine ISR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50062
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, (DE_HPD_ISR_ADDR_D13), (DE_HPD_ISR_ADDR_D13), 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       DG2_MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL); // ISR LiveState

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/53888
        // Synopsys phy TypeC status register
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SNPS_PHY_TYPEC_STATUS_PORT_A_ADDR_DG2, SNPS_PHY_TYPEC_STATUS_PORT_A_ADDR_DG2, 0, NULL, NULL,
                                                       0, FALSE, eReadCombine, DG2_MMIOHANDLERS_GetLanesAssignedfromSnpPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SNPS_PHY_TYPEC_STATUS_PORT_B_ADDR_DG2, SNPS_PHY_TYPEC_STATUS_PORT_B_ADDR_DG2, 0, NULL, NULL,
                                                       0, FALSE, eReadCombine, DG2_MMIOHANDLERS_GetLanesAssignedfromSnpPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SNPS_PHY_TYPEC_STATUS_PORT_C_ADDR_DG2, SNPS_PHY_TYPEC_STATUS_PORT_C_ADDR_DG2, 0, NULL, NULL,
                                                       0, FALSE, eReadCombine, DG2_MMIOHANDLERS_GetLanesAssignedfromSnpPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SNPS_PHY_TYPEC_STATUS_PORT_D_ADDR_DG2, SNPS_PHY_TYPEC_STATUS_PORT_D_ADDR_DG2, 0, NULL, NULL,
                                                       0, FALSE, eReadCombine, DG2_MMIOHANDLERS_GetLanesAssignedfromSnpPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SNPS_PHY_TYPEC_STATUS_PORT_TC1_ADDR_DG2, SNPS_PHY_TYPEC_STATUS_PORT_TC1_ADDR_DG2, 0, NULL,
                                                       NULL, 0, FALSE, eReadCombine, DG2_MMIOHANDLERS_GetLanesAssignedfromSnpPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        //// For DG2 post-silicon, DP_F_TC port is removed and supports only Native. GfxDriver identifies it by reading PHY REF Control register set to 100Mhz.
        // bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SNPS_PHY_REF_CONTROL_PORT_TC1_ADDR_DG2, SNPS_PHY_REF_CONTROL_PORT_TC1_ADDR_DG2, 0, NULL,
        // NULL,
        //                                               0, FALSE, eReadCombine, DG2_MMIOHANDLERS_SnpsTypecConfigure100MhzRefClkMMIOReadHandler, NULL, NULL, NULL, NULL);

        // if (bRet == FALSE)
        //{
        //    break;
        //}

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, IGT_PAVP_FUSE_2, IGT_PAVP_FUSE_2, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       DG2_MMIOHANDLERS_ProductionSkuMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        //************************************************************************************
        // Intentionally commented for further use during TypeC final enabling in driver.
        //************************************************************************************

        //        // MGPhyLanes Handlers - FIA1
        // bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12, PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12, 0, NULL, NULL, 0,
        //                                               TRUE, eNoExecHw, NULL, GEN12_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        // if (bRet == FALSE)
        //{
        //    break;
        //}
        //// MGPhyLanes Handlers - FIA2
        // bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12, PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12, 0, NULL, NULL, 0,
        //                                               TRUE, eNoExecHw, NULL, GEN12_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        // if (bRet == FALSE)
        //{
        //    break;
        //}
        //// MGPhyLanes Handlers - FIA3
        // bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12, PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12, 0, NULL, NULL, 0,
        //                                               TRUE, eNoExecHw, NULL, GEN12_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        // if (bRet == FALSE)
        //{
        //    break;
        //}
        ///*To handle upfront link training
        // Each FIA can have upto 4 instance of scratch pad
        // FIA1 - SP1 to SP4
        //*/
        // bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA1_ADDR_GEN12, PORT_TX_DFLEXDPSP4_FIA1_ADDR_GEN12, 0, NULL, NULL, 0,
        //                                               FALSE, eReadCombine, GEN12_CMN_MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler, NULL, NULL, NULL, NULL);
        // if (bRet == FALSE)
        //{
        //    break;
        //}
        ///*To handle upfront link training
        // Each FIA can have upto 4 instance of scratch pad
        // FIA2 - SP1 to SP4
        //*/
        // bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA2_ADDR_GEN12, PORT_TX_DFLEXDPSP4_FIA2_ADDR_GEN12, 0, NULL, NULL, 0,
        //                                               FALSE, eReadCombine, GEN12_CMN_MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler, NULL, NULL, NULL, NULL);
        // if (bRet == FALSE)
        //{
        //    break;
        //}
        ///*To handle upfront link training
        // Each FIA can have upto 4 instance of scratch pad
        // FIA3 - SP1 to SP4
        //*/
        // bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA3_ADDR_GEN12, PORT_TX_DFLEXDPSP4_FIA3_ADDR_GEN12, 0, NULL, NULL, 0,
        //                                               FALSE, eReadCombine, GEN12_CMN_MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler, NULL, NULL, NULL, NULL);
        // if (bRet == FALSE)
        //{
        //    break;
        //}
        //// Workaround to support TypeC ports. In the default mode for TC ports, IOM wouldn't have initialized PHY. So, the DDI Buffer is IDLE. As per the recommendation from
        //// Ganesh/Raghu, it is being masked in valsim.
        // for (int ddi_offset = DDI_BUF_CTL_USBC1_ADDR_D12; ddi_offset <= DDI_BUF_CTL_USBC6_ADDR_D12; ddi_offset += 256)
        //{
        //    bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, ddi_offset, ddi_offset, 0, NULL, NULL, 0, FALSE, eNoExecHw,
        //                                                   TGLLP_MMIOHANDLERS_DdiBufferControlMMIOReadHandler, NULL, NULL, NULL, NULL);
        //    if (bRet == FALSE)
        //    {
        //        break;
        //    }
        //}
        // if (bRet == FALSE)
        //{
        //    break;
        //}
        //// Workaround to support TypeC ports. In the default mode for TC ports, IOM wouldn't have initialized PHY. So, the Powerwell DDI status bit is not set. As per the
        //// recommendation from Ganesh/Raghu, it is being masked in valsim.
        // bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PWR_WELL_CTL_DDI2_ADDR_D12, PWR_WELL_CTL_DDI2_ADDR_D12, 0, NULL, NULL, 0, FALSE, eNoExecHw,
        //                                               TGLLP_MMIOHANDLERS_PwrWellDDIControlMMIOReadHandler, NULL, NULL, NULL, NULL);
        // if (bRet == FALSE)
        //{
        //    break;
        //}
    } while (FALSE);

    return bRet;
}
BOOLEAN DG2_MMIOHANDLERS_RegisterMasterTileInterrupt(PMMIO_INTERFACE pstMMIOInterface)
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
        COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_TILE_INTR_ADDR_DG2, GFX_MSTR_TILE_INTR_ADDR_DG2, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                DG2_MMIOHANDLERS_MasterTileInterruptCtlMMIOReadHandler, DG2_MMIOHANDLERS_MasterTileInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN DG2_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    if (pstMMIOInterface)
    {

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_START] = DDI_AUX_DATA_A_START_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_END]   = DDI_AUX_DATA_A_END_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_A]        = DDI_AUX_CTL_A_GEN13;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_START] = DDI_AUX_DATA_B_START_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_END]   = DDI_AUX_DATA_B_END_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_B]        = DDI_AUX_CTL_B_GEN13;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = DDI_AUX_DATA_C_START_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = DDI_AUX_DATA_C_END_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = DDI_AUX_CTL_C_GEN13;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = DDI_AUX_DATA_D_START_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = DDI_AUX_DATA_D_END_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = DDI_AUX_CTL_D_GEN13;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_START] = DDI_AUX_DATA_TC1_START_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_END]   = DDI_AUX_DATA_TC1_END_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_F]        = DDI_AUX_CTL_TC1_GEN13;

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

BOOLEAN DG2_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                            PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                            bRet                = FALSE;
    GRAPHICS_MASTER_TILE_INTERRUPT_DG2 stMasterTileIntCtrl = { 0 };
    GFX_MSTR_INTR_GEN13                stMasterIntCtrl     = { 0 };
    DISPLAY_INT_CTL_GEN13              stDisplayIntCtrl    = { 0 };

    SHOTPLUG_CTL_DDI_DG2 stSouthDdiCtlReg = { 0 };
    SHOTPLUG_CTL_TC_DG2  stSouthTCCtlReg  = { 0 };

    SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_DG2 stPCHLiveReg = { 0 };
    SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_DG2 stPCHIMRReg  = { 0 };
    SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_DG2 stPCHIIRReg  = { 0 };
    SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_DG2 stPCHIERReg  = { 0 };

    HOTPLUG_CTL_D13 stTYPECHotPlugCtl = { 0 };

    DE_HPD_INTERRUPT_DEFINITION_D13 stDEHPDISR = { 0 };
    DE_HPD_INTERRUPT_DEFINITION_D13 stDEHPDIMR = { 0 };
    DE_HPD_INTERRUPT_DEFINITION_D13 stDEHPDIIR = { 0 };
    DE_HPD_INTERRUPT_DEFINITION_D13 stDEHPDIER = { 0 };

    // PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia1Status = { 0 };
    // PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia2Status = { 0 };
    // PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia3Status = { 0 };

    // PORT_TX_DFLEXDPSP_GEN12    stFia1LiveState     = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Check if HPD has been enabled by Gfx
        if (FALSE == DG2_MMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType, PortConnectorInfo))
        {
            break;
        }

        stMasterTileIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stSouthDdiCtlReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_DDI_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stSouthTCCtlReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_TC_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Legacy
        stPCHLiveReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_ISR_ADDR_DG2)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IMR_ADDR_DG2)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_DG2)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IER_ADDR_DG2)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        // TypeC North Bridge
        stTYPECHotPlugCtl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TC_HOTPLUG_CTL_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDEHPDISR.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_ISR_ADDR_D13)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIMR.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_IMR_ADDR_D13)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIIR.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_IIR_ADDR_D13)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIER.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_IER_ADDR_D13)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        // stTypeCFia1Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // stTypeCFia2Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // stTypeCFia3Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // stFia1LiveState.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
        case INTHDMIA_PORT:

            if (stSouthDdiCtlReg.DdiaHpdEnable && stPCHIMRReg.HotplugDdia == FALSE && stPCHIERReg.HotplugDdia)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugDdia  = TRUE;
                    stPCHLiveReg.HotplugDdia = bAttach;
                    // Long Pulse
                    stSouthDdiCtlReg.DdiaHpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_DG2;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdia) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdia = TRUE;
                    // Short Pulse
                    stSouthDdiCtlReg.DdiaHpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_DG2;
                    bRet                           = TRUE;
                }
            }

            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:

            if (stSouthDdiCtlReg.DdibHpdEnable && stPCHIMRReg.HotplugDdib == FALSE && stPCHIERReg.HotplugDdib)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugDdib        = TRUE;
                    stPCHLiveReg.HotplugDdib       = bAttach;
                    stSouthDdiCtlReg.DdibHpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_DG2;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdib) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdib        = TRUE;
                    stSouthDdiCtlReg.DdibHpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_DG2;
                    bRet                           = TRUE;
                }
            }

            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:

            if (stSouthDdiCtlReg.DdicHpdEnable && stPCHIMRReg.HotplugDdic == FALSE && stPCHIERReg.HotplugDdic)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugDdic        = TRUE;
                    stPCHLiveReg.HotplugDdic       = bAttach;
                    stSouthDdiCtlReg.DdicHpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_DG2;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdic) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdic        = TRUE;
                    stSouthDdiCtlReg.DdicHpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_DG2;
                    bRet                           = TRUE;
                }
            }

            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:

            if (stSouthDdiCtlReg.DdidHpdEnable && stPCHIMRReg.HotplugDdid == FALSE && stPCHIERReg.HotplugDdid)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugDdid        = TRUE;
                    stPCHLiveReg.HotplugDdid       = bAttach;
                    stSouthDdiCtlReg.DdidHpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_DG2;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdid) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdid        = TRUE;
                    stSouthDdiCtlReg.DdidHpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_DG2;
                    bRet                           = TRUE;
                }
            }

            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:

            if (stTYPECHotPlugCtl.Port1HpdEnable && (FALSE == stDEHPDIMR.Tc1Hotplug) && stDEHPDIER.Tc1Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc1Hotplug = TRUE;
                    stDEHPDISR.Tc1Hotplug = bAttach; // LiveState Register
                                                     // stFia1LiveState.Tc0LiveState                                 = bAttach; // LiveState Register
                    // stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTYPECHotPlugCtl.Port1HpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_DG2;
                    bRet                             = TRUE;
                }
                else if (stDEHPDISR.Tc1Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc1Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port1HpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_DG2;
                    bRet                             = TRUE;
                }
            }

            // Legacy south bridge
            if (stSouthTCCtlReg.Tc1HpdEnable && stPCHIMRReg.HotplugTypecPort1 == FALSE && stPCHIERReg.HotplugTypecPort1)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort1  = TRUE;
                    stPCHLiveReg.HotplugTypecPort1 = bAttach;
                    stSouthTCCtlReg.Tc1HpdStatus   = HPD_STATUS_LONG_PULSE_DETECTED_DG2;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort1) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort1 = TRUE;
                    stSouthTCCtlReg.Tc1HpdStatus  = HPD_STATUS_SHORT_PULSE_DETECTED_DG2;
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
        stMasterTileIntCtrl.Tile0                = TRUE;
        stMasterIntCtrl.DisplayInterruptsPending = TRUE;
        stDisplayIntCtrl.DeHpdInterruptsPending  = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_DDI_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthDdiCtlReg.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_TC_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset])  = stSouthTCCtlReg.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset])          = stPCHLiveReg.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset])          = stPCHIIRReg.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TC_HOTPLUG_CTL_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTYPECHotPlugCtl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_ISR_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset])     = stDEHPDISR.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_IIR_ADDR_D13)-pstGlobalMMORegData->ulMMIOBaseOffset])     = stDEHPDIIR.Value;

        /* *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia1Status.ulValue;
         *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia2Status.ulValue;
         *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia3Status.ulValue;
         */

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset])    = stMasterIntCtrl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterTileIntCtrl.Value;
    }

    return bRet;
}

BOOLEAN DG2_MMIOHANDLERS_SetMasterTileInterrupt(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN                            bRet                = FALSE;
    GRAPHICS_MASTER_TILE_INTERRUPT_DG2 stMasterTileIntCtrl = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stMasterTileIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stMasterTileIntCtrl.Tile0 = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterTileIntCtrl.Value;
        bRet                                                                                                                     = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN DG2_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                                           bRet                = TRUE;
    SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_DG2 stPCHLiveReg        = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA                        pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;
    DE_HPD_INTERRUPT_DEFINITION_D13                   stDEHPDISR          = { 0 };

    //// MG PHY Lines Enabling for Port D - Port F
    // PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia1Status = { 0 };
    // PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia2Status = { 0 };
    // PORT_TX_DFLEXDPPMS_GEN12 stTypeCFia3Status = { 0 };
    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        /*stTypeCFia1Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
         stTypeCFia2Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
         stTypeCFia3Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]);
         */

        stPCHLiveReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDISR.Value   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_ISR_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc1Hotplug = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort1 = bAttach;
            }
            // stTypeCFia1Status.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        // Below line is a temp workaround
        stPCHLiveReg.HotplugDdia                                                                                         = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset])    = stPCHLiveReg.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_ISR_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDEHPDISR.Value;
        /* *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia1Status.ulValue;
         *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia2Status.ulValue;
         *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN12 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia3Status.ulValue;
         */
    }

    return bRet;
}

/*
This function will clear the HpdStatus value of a particular DDI
which Gfx Driver wants to.
*/
BOOLEAN DG2_MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                    bRet                = FALSE;
    SHOTPLUG_CTL_DDI_DG2       stSouthDDICtlReg    = { 0 };
    SHOTPLUG_CTL_TC_DG2        stSouthTCCtlreg     = { 0 };
    HOTPLUG_CTL_D13            stNorthTCCtlreg     = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stSouthDDICtlReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_DDI_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthTCCtlreg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_TC_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthTCCtlreg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TC_HOTPLUG_CTL_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
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

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            if (stNorthTCCtlreg.Port1HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc1HpdEnable && (1 != PortConnectorInfo.IsTypeC))
            {
                bRet = TRUE;
            }
            break;

        default:
            break;
        }

    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, SHOTPLUG_CTL_DDI_ADDR_DG2, stSouthDDICtlReg.Value, SHOTPLUG_CTL_TC_ADDR_DG2, stSouthTCCtlreg.Value,
                        TC_HOTPLUG_CTL_ADDR_D13, stNorthTCCtlreg.Value, 0, 0);
    return bRet;
}

BOOLEAN DG2_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                                           bRet             = TRUE;
    SHOTPLUG_CTL_DDI_DG2                              stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_TC_DG2                               stHotPlugCtl2    = { 0 };
    SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_DG2 stLiveStateReg   = { 0 };
    SOUTH_DISPLAY_ENGINE_INTERRUPT_BIT_DEFINITION_DG2 stLiveStateRegHw = { 0 };
    ULONG                                             driverRegValue   = 0;

    stHotPlugCtl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SHOTPLUG_CTL_DDI_ADDR_DG2 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stHotPlugCtl2.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SHOTPLUG_CTL_TC_ADDR_DG2 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stLiveStateReg.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, SDE_ISR_ADDR_DG2, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        stLiveStateRegHw.Value = driverRegValue;
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

    if (stHotPlugCtl2.Tc1HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort1 = FALSE;
    }

    *pulReadData = stLiveStateReg.Value;

    return bRet;
}

/*
This function will clear the HpdStatus value of a particular DDI
which Gfx Driver wants to.
*/
BOOLEAN DG2_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/33768 ??
    SHOTPLUG_CTL_DDI_DG2 stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_DDI_DG2 stHotPlugCtlTemp = { 0 };

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/21779 ??
    SHOTPLUG_CTL_TC_DG2 stHotPlugCtl2     = { 0 };
    SHOTPLUG_CTL_TC_DG2 stHotPlugCtlTemp2 = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (SHOTPLUG_CTL_DDI_ADDR_DG2 == ulMMIOOffset)
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

            stHotPlugCtlTemp.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_DDI_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stHotPlugCtl.Value = ulWriteData;

            stHotPlugCtl.DdiaHpdStatus = stHotPlugCtlTemp.DdiaHpdStatus;
            stHotPlugCtl.DdibHpdStatus = stHotPlugCtlTemp.DdibHpdStatus;
            stHotPlugCtl.DdicHpdStatus = stHotPlugCtlTemp.DdicHpdStatus;
            stHotPlugCtl.DdidHpdStatus = stHotPlugCtlTemp.DdidHpdStatus;

            stHotPlugCtlTemp.Value = ulWriteData;

            stHotPlugCtl.DdiaHpdStatus &= ~stHotPlugCtlTemp.DdiaHpdStatus;
            stHotPlugCtl.DdibHpdStatus &= ~stHotPlugCtlTemp.DdibHpdStatus;
            stHotPlugCtl.DdicHpdStatus &= ~stHotPlugCtlTemp.DdicHpdStatus;
            stHotPlugCtl.DdidHpdStatus &= ~stHotPlugCtlTemp.DdidHpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl.Value;
        }
        else
        {
            pstGlobalMMORegData     = &pstMMIOHandlerInfo->stGlobalMMORegData;
            stHotPlugCtlTemp2.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_TC_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stHotPlugCtl2.Value = ulWriteData;

            stHotPlugCtl2.Tc1HpdStatus = stHotPlugCtlTemp2.Tc1HpdStatus;

            stHotPlugCtlTemp2.Value = ulWriteData;

            stHotPlugCtl2.Tc1HpdStatus &= ~stHotPlugCtlTemp2.Tc1HpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl2.Value;
        }
        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN DG2_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    HOTPLUG_CTL_D13 stHotPlugCtl     = { 0 };
    HOTPLUG_CTL_D13 stHotPlugCtlTemp = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData    = &pstMMIOHandlerInfo->stGlobalMMORegData;
        stHotPlugCtlTemp.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stHotPlugCtl.Value = ulWriteData;

        stHotPlugCtl.Port1HpdStatus = stHotPlugCtlTemp.Port1HpdStatus;

        stHotPlugCtlTemp.Value = ulWriteData;

        stHotPlugCtl.Port1HpdStatus &= ~stHotPlugCtlTemp.Port1HpdStatus;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl.Value;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN DG2_MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = TRUE;
    // TYPE_C
    HOTPLUG_CTL_D13                 stHotPlugCtl   = { 0 };
    DE_HPD_INTERRUPT_DEFINITION_D13 stLiveStateReg = { 0 };

    stHotPlugCtl.Value   = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[TC_HOTPLUG_CTL_ADDR_D13 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stLiveStateReg.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    // TYPE_C
    if (stHotPlugCtl.Port1HpdEnable == FALSE)
    {
        stLiveStateReg.Tc1Hotplug = FALSE;
    }

    *pulReadData = stLiveStateReg.Value;

    return bRet;
}

BOOLEAN DG2_MMIOHANDLERS_MasterTileInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    GRAPHICS_MASTER_TILE_INTERRUPT_DG2 stMasterTileIntCtrl = { 0 };
    stMasterTileIntCtrl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stMasterTileIntCtrl.MasterInterrupt = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                 // Enable` bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stMasterTileIntCtrl.Value;

    return TRUE;
}

BOOLEAN DG2_MMIOHANDLERS_MasterTileInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGRAPHICS_MASTER_TILE_INTERRUPT_DG2 pstMasterTileIntCtrl =
    (PGRAPHICS_MASTER_TILE_INTERRUPT_DG2)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    GRAPHICS_MASTER_TILE_INTERRUPT_DG2 stMasterTileIntCtrlTemp = { 0 };

    stMasterTileIntCtrlTemp.Value         = ulWriteData;
    pstMasterTileIntCtrl->MasterInterrupt = stMasterTileIntCtrlTemp.MasterInterrupt;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

/**-------------------------------------------------------------
 * @brief DG2_MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler
 *
 * Description: Set the number of lanes assigned to display for Read TypeC Phy register
 *       This call is valid only for all Synopsys Phy ports (DDI A/B/C/D/F)
 *
 *-------------------------------------------------------------*/
BOOLEAN DG2_MMIOHANDLERS_GetLanesAssignedfromSnpPhyMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    SNPS_PHY_TYPEC_STATUS_DG2  LaneData            = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
        LaneData.Value      = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Currently 4 lanes are assigned for all the Ports
        // TODO:
        // 1) Based on Live State of a Port, Lane Values can be assigned to a particualr port
        // 2) Lane Values can be configured run time also.Run time configuration can be done through registry write/read
        // These two items will be taken up later after discussing with VCO

        LaneData.Dpalt_Dp4 = DPALT_DP4_4_LANES_ACCESSIBLE_DG2;

        *pulReadData = LaneData.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = LaneData.Value;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

/**-------------------------------------------------------------
 * @brief DG2_MMIOHANDLERS_SnpsTypecConfigure100MhzRefClkMMIOReadHandler
 *
 * Description: Set the reference clock to 100Mhz to simulate default static DP/HDMI ports
 *       This call is valid only for Synopsys Phy port (DDI F)
 *
 *-------------------------------------------------------------*/
BOOLEAN DG2_MMIOHANDLERS_SnpsTypecConfigure100MhzRefClkMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                       PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    SNPS_PHY_REF_CONTROL_DG2   SnpRefCtl           = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
        SnpRefCtl.Value     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

        SnpRefCtl.RefclkMuxSelect = REFCLK_MUX_SELECT_100_MHZ_DG2;

        *pulReadData = SnpRefCtl.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = SnpRefCtl.Value;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

/**-------------------------------------------------------------
 * @brief DG2_MMIOHANDLERS_ProductionSkuMMIOReadHandler
 *
 * Description: Production sku can be authenticated only with Production Oprom signature done by ubit. When we modify vbt, from infra we sign it with debug signature.
                This works fine for pre-production sku's. For MA configurations, we see production sku's connected. We are resetting production sku flag in valsim.
                With this change, gfx driver thinks it is an pre-production sku and authenticates with debug signature.
 *-------------------------------------------------------------*/
BOOLEAN DG2_MMIOHANDLERS_ProductionSkuMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                    bRet                = FALSE;
    DDU32                      ulPavpFuse2         = 0;
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

        if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, ulMMIOOffset, &ulPavpFuse2, SIMDRV_GFX_ACCESS_REQUEST_READ))
        {
            ulPavpFuse2 = ulPavpFuse2 & (~0x4);

            *pulReadData = ulPavpFuse2;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = ulPavpFuse2;

            bRet = TRUE;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN DG2_MMIOHANDLERS_ScdcInterruptGeneration(PMMIO_INTERFACE pstMMIOInterface, PSCDC_ARGS pstScdcArgs)
{
    BOOLEAN                                bRet                = FALSE;
    GRAPHICS_MASTER_TILE_INTERRUPT_DG2     stMasterTileIntCtrl = { 0 };
    GFX_MSTR_INTR_GEN13                    stMasterIntCtrl     = { 0 };
    DISPLAY_INT_CTL_GEN13                  stDisplayIntCtrl    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 stSouthDeInt        = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stMasterTileIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stMasterIntCtrl.Value     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDisplayIntCtrl.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthDeInt.ulValue      = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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
        case INTHDMIF_PORT:
            stSouthDeInt.ScdcTc1 = TRUE;
            bRet                 = TRUE;
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

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthDeInt.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset])    = stMasterIntCtrl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_DG2 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterTileIntCtrl.Value;
    }

    return bRet;
}
