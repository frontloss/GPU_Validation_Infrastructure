
#include "MTLMMIO.h"
#include "../../CommonInclude/ETWLogging.h"
#include "../../DriverInterfaces/CommonRxHandlers.h"
#include "..\..\DriverInterfaces\SimDrvToGfx.h"

BOOLEAN MTL_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;
    do
    {
        bRet = MTL_MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);
    } while (FALSE);
    return bRet;
}

BOOLEAN MTL_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;
    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Master Tile
        bRet =
        COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_TILE_INTR_ADDR_MTL, GFX_MSTR_TILE_INTR_ADDR_MTL, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                MTL_MMIOHANDLERS_MasterTileInterruptCtlMMIOReadHandler, MTL_MMIOHANDLERS_MasterTileInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Master Interrupt Control Register
        // BSpec Ref :
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_INTR_ADDR_GEN14, GFX_MSTR_INTR_ADDR_GEN14, 0, NULL, NULL, 0, TRUE, eReadCombine,
                                                       GEN14_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler, GEN14_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler, NULL,
                                                       NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // Display Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50081
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DISPLAY_INTR_CTL_ADDR_GEN14, DISPLAY_INTR_CTL_ADDR_GEN14, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN14_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler, GEN14_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler, NULL,
                                                       NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_ISR_ADDR_GEN14, SDE_ISR_ADDR_GEN14, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       MTL_MMIOHANDLERS_HotPlugLiveStateMMIOReadHanlder, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_IIR_ADDR_GEN14, SDE_IIR_ADDR_GEN14, 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       GEN14_CMN_MMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN14, SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN14, 0, NULL, NULL,
                                                       0, TRUE, eNoExecHw, NULL, MTL_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_HOTPLUG_CTL_USBC1_ADDR_GEN14, PORT_HOTPLUG_CTL_USBC1_ADDR_GEN14, 0, NULL, NULL, 0, TRUE,
                                                       eNoExecHw, NULL, MTL_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_HOTPLUG_CTL_USBC2_ADDR_GEN14, PORT_HOTPLUG_CTL_USBC2_ADDR_GEN14, 0, NULL, NULL, 0, TRUE,
                                                       eNoExecHw, NULL, MTL_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_HOTPLUG_CTL_USBC3_ADDR_GEN14, PORT_HOTPLUG_CTL_USBC3_ADDR_GEN14, 0, NULL, NULL, 0, TRUE,
                                                       eNoExecHw, NULL, MTL_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_HOTPLUG_CTL_USBC4_ADDR_GEN14, PORT_HOTPLUG_CTL_USBC4_ADDR_GEN14, 0, NULL, NULL, 0, TRUE,
                                                       eNoExecHw, NULL, MTL_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PICAINTERRUPTDEFINTION_2_ADDR_GEN14, PICAINTERRUPTDEFINTION_2_ADDR_GEN14, 0, NULL, NULL, 0,
                                                       TRUE, eReadCombine, NULL, GEN14_CMN_MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PICAINTERRUPTDEFINTION_0_ADDR_GEN14, PICAINTERRUPTDEFINTION_0_ADDR_GEN14, 0, NULL, NULL, 0,
                                                       FALSE, eNoExecHw, MTL_MMIOHANDLERS_PICAHotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXPA1_FIA1_ADDR_D14, PORT_TX_DFLEXPA1_FIA1_ADDR_D14, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN14_CMN_MMIOHANDLERS_GetLanesAssignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXPA1_FIA2_ADDR_D14, PORT_TX_DFLEXPA1_FIA2_ADDR_D14, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN14_CMN_MMIOHANDLERS_GetLanesAssignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_BUF_CTL1_A_ADDR_D14, PORT_BUF_CTL1_A_ADDR_D14, 0, NULL, NULL, 0, FALSE, eReadCombine,
                                                       GEN14_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_BUF_CTL1_B_ADDR_D14, PORT_BUF_CTL1_B_ADDR_D14, 0, NULL, NULL, 0, FALSE, eReadCombine,
                                                       GEN14_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_BUF_CTL1_USBC1_ADDR_D14, PORT_BUF_CTL1_USBC1_ADDR_D14, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN14_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_BUF_CTL1_USBC2_ADDR_D14, PORT_BUF_CTL1_USBC2_ADDR_D14, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN14_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_BUF_CTL1_USBC3_ADDR_D14, PORT_BUF_CTL1_USBC3_ADDR_D14, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN14_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_BUF_CTL1_USBC4_ADDR_D14, PORT_BUF_CTL1_USBC4_ADDR_D14, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN14_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        // TCSS_DDI_STATUS_D14 Handlers
        // BSPEC Ref: https://gfxspecs.intel.com/Predator/Home/Index/55481
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, TCSS_DDI_STATUS_1_ADDR_GEN14, TCSS_DDI_STATUS_4_ADDR_GEN14, 0, NULL, NULL, 0, TRUE, eNoExecHw,
                                                       NULL, GEN14_CMN_MMIOHANDLERS_PICAMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }
        // To update the DPCD 2008H for PSR panel based on PSR enable/disable state
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SRD_CTL_A_ADDR_D14, SRD_CTL_A_ADDR_D14, 0, NULL, NULL, 0, TRUE, eExecHW, NULL,
                                                       MTL_MMIOHANDLERS_Psr1MMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        // To update the DPCD 2008H for PSR panel based on PSR enable/disable state
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SRD_CTL_B_ADDR_D14, SRD_CTL_B_ADDR_D14, 0, NULL, NULL, 0, TRUE, eExecHW, NULL,
                                                       MTL_MMIOHANDLERS_Psr1MMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        // To update the DPCD 2008H for PSR panel based on PSR enable/disable state
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PSR2_CTL_A_ADDR_D14, PSR2_CTL_A_ADDR_D14, 0, NULL, NULL, 0, TRUE, eExecHW, NULL,
                                                       MTL_MMIOHANDLERS_Psr2MMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        // To update the DPCD 2008H for PSR panel based on PSR enable/disable state
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PSR2_CTL_B_ADDR_D14, PSR2_CTL_B_ADDR_D14, 0, NULL, NULL, 0, TRUE, eExecHW, NULL,
                                                       MTL_MMIOHANDLERS_Psr2MMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PICA_PHY_CONFIG_CONTROL_0_ADDR_XE3_D, PICA_PHY_CONFIG_CONTROL_0_ADDR_XE3_D, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        if (pstMMIOInterface->eIGFXPlatform == eIGFX_ELG)
        {
            bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, IGT_PAVP_FUSE_2, IGT_PAVP_FUSE_2, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                           ELG_MMIOHANDLERS_ProductionSkuMMIOReadHandler, NULL, NULL, NULL, NULL);

            if (bRet == FALSE)
                break;
        }
    } while (FALSE);

    return bRet;
}

BOOLEAN MTL_MMIOHANDLERS_MasterTileInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGRAPHICS_MASTER_TILE_INTERRUPT_MTL pstMasterTileIntCtrl =
    (PGRAPHICS_MASTER_TILE_INTERRUPT_MTL)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    GRAPHICS_MASTER_TILE_INTERRUPT_MTL stMasterTileIntCtrlTemp = { 0 };

    stMasterTileIntCtrlTemp.Value         = ulWriteData;
    pstMasterTileIntCtrl->MasterInterrupt = stMasterTileIntCtrlTemp.MasterInterrupt;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN MTL_MMIOHANDLERS_MasterTileInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    GRAPHICS_MASTER_TILE_INTERRUPT_MTL stMasterTileIntCtrl = { 0 };
    stMasterTileIntCtrl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stMasterTileIntCtrl.MasterInterrupt = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.

    *pulReadData = stMasterTileIntCtrl.Value;

    return TRUE;
}

BOOLEAN MTL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                            PORT_CONNECTOR_INFO PortConnectorInfo)
{

    BOOLEAN                            bRet                = FALSE;
    GRAPHICS_MASTER_TILE_INTERRUPT_MTL stMasterTileIntCtrl = { 0 };
    GFX_MSTR_INTR_GEN14                stMasterIntctrl     = { 0 };
    DISPLAY_INT_CTL_GEN14              stDisplayIntCtrl    = { 0 };

    SHOTPLUG_CTL_DDI_GEN14 stSouthDdiCtlReg = { 0 };
    SHOTPLUG_CTL_TC_ADP    SouthDdiTcCtrl   = { 0 };

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHLiveReg = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHIMRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHIIRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHIERReg  = { 0 };

    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb1 = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb2 = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb3 = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb4 = { 0 };

    PICA_INTERRUPT_DEFINTION_GEN14 stPICALiveReg = { 0 };
    PICA_INTERRUPT_DEFINTION_GEN14 stPICAIMRReg  = { 0 };
    PICA_INTERRUPT_DEFINTION_GEN14 stPICAIIRReg  = { 0 };
    PICA_INTERRUPT_DEFINTION_GEN14 stPICAIERReg  = { 0 };

    PORT_TX_DFLEXDPPMS_D14 stTypeCFia1DppmsStatus = { 0 };
    PORT_TX_DFLEXPA1_D14   Fia1LiveStatus         = { 0 };
    PORT_TX_DFLEXPA1_D14   Fia2LiveStatus         = { 0 };

    TCSS_DDI_STATUS_GEN14 stTc1DdiStatus = { 0 };
    TCSS_DDI_STATUS_GEN14 stTc2DdiStatus = { 0 };
    TCSS_DDI_STATUS_GEN14 stTc3DdiStatus = { 0 };
    TCSS_DDI_STATUS_GEN14 stTc4DdiStatus = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;
    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stMasterTileIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_MTL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stMasterIntctrl.Value     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDisplayIntCtrl.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stSouthDdiCtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        SouthDdiTcCtrl.Value     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_TC_ADDR_ADP - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // Legacy
        stPCHLiveReg.ulValue         = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_ISR_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.ulValue          = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IMR_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.ulValue          = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.ulValue          = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IER_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFia1DppmsStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // PICA HPD
        stPorthpdUsb1.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPorthpdUsb2.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPorthpdUsb3.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPorthpdUsb4.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // PICA Interrupt

        stPICALiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_0_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPICAIMRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPICAIIRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPICAIERReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        Fia1LiveStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXPA1_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        Fia2LiveStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXPA1_FIA2_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // TypeC
        stTc1DdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc2DdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc3DdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc4DdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
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
                    stSouthDdiCtlReg.DdiaHpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdia) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdia = TRUE;
                    // Short Pulse
                    stSouthDdiCtlReg.DdiaHpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN14;
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
                    stSouthDdiCtlReg.DdibHpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdib) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdib        = TRUE;
                    stSouthDdiCtlReg.DdibHpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
            }
            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            // DP Alt TC
            if (stPorthpdUsb1.DpAltEnable && stPICAIMRReg.DpAltHotplugPort1 == FALSE && stPICAIERReg.DpAltHotplugPort1)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.DpAltHotplugPort1                                    = TRUE;
                    stPICALiveReg.DpAltHotplugPort1                                   = bAttach;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTc1DdiStatus.Ready                                              = bAttach;
                    stPorthpdUsb1.DpAltStatus                                         = DP_ALT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                                                              = TRUE;
                }
                else if (stPICALiveReg.DpAltHotplugPort1)
                {
                    stPICAIIRReg.DpAltHotplugPort1 = TRUE;
                    stPorthpdUsb1.DpAltStatus      = DP_ALT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            // TBT
            else if (stPorthpdUsb1.TbtEnable && stPICAIMRReg.TbtHotplugPort1 == FALSE && stPICAIERReg.TbtHotplugPort1)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.TbtHotplugPort1  = TRUE;
                    stPICALiveReg.TbtHotplugPort1 = bAttach;
                    stPorthpdUsb1.TbtStatus       = TBT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                          = TRUE;
                }
                else if (stPICALiveReg.TbtHotplugPort1)
                {
                    stPICAIIRReg.TbtHotplugPort1 = TRUE;
                    stPorthpdUsb1.TbtStatus      = TBT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                         = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            if (SouthDdiTcCtrl.Tc1HpdEnable && stPCHIMRReg.HotplugTypecPort1 == FALSE && stPCHIERReg.HotplugTypecPort1)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort1                                     = TRUE;
                    stPCHLiveReg.HotplugTypecPort1                                    = bAttach;
                    SouthDdiTcCtrl.Tc1HpdStatus                                       = 0x2;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTc1DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort1)
                {
                    stPCHIIRReg.HotplugTypecPort1 = TRUE;
                    SouthDdiTcCtrl.Tc1HpdStatus   = 0x1;
                    bRet                          = TRUE;
                }
            }
            break;

        case INTDPG_PORT:
        case INTHDMIG_PORT:
            // DP Alt
            if (stPorthpdUsb2.DpAltEnable && stPICAIMRReg.DpAltHotplugPort2 == FALSE && stPICAIERReg.DpAltHotplugPort2)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.DpAltHotplugPort2                                    = TRUE;
                    stPICALiveReg.DpAltHotplugPort2                                   = bAttach;
                    stPorthpdUsb2.DpAltStatus                                         = DP_ALT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTc2DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPICALiveReg.DpAltHotplugPort2)
                {
                    stPICAIIRReg.DpAltHotplugPort2 = TRUE;
                    stPorthpdUsb2.DpAltStatus      = DP_ALT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    stTc2DdiStatus.Ready           = bAttach;
                    bRet                           = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            // TBT
            else if (stPorthpdUsb2.TbtEnable && stPICAIMRReg.TbtHotplugPort2 == FALSE && stPICAIERReg.TbtHotplugPort2)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.TbtHotplugPort2  = TRUE;
                    stPICALiveReg.TbtHotplugPort2 = bAttach;
                    stPorthpdUsb2.TbtStatus       = TBT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                          = TRUE;
                }
                else if (stPICALiveReg.TbtHotplugPort2)
                {
                    stPICAIIRReg.TbtHotplugPort2 = TRUE;
                    stPorthpdUsb2.TbtStatus      = TBT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                         = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }

            if (SouthDdiTcCtrl.Tc2HpdEnable && stPCHIMRReg.HotplugTypecPort2 == FALSE && stPCHIERReg.HotplugTypecPort2)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort2                                     = TRUE;
                    stPCHLiveReg.HotplugTypecPort2                                    = bAttach;
                    SouthDdiTcCtrl.Tc2HpdStatus                                       = 0x2;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTc2DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort2)
                {
                    stPCHIIRReg.HotplugTypecPort2 = TRUE;
                    SouthDdiTcCtrl.Tc2HpdStatus   = 0x1;
                    bRet                          = TRUE;
                }
            }

            break;

        case INTDPH_PORT:
        case INTHDMIH_PORT:
            // DP Alt
            if (stPorthpdUsb3.DpAltEnable && stPICAIMRReg.DpAltHotplugPort3 == FALSE && stPICAIERReg.DpAltHotplugPort3)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.DpAltHotplugPort3                                    = TRUE;
                    stPICALiveReg.DpAltHotplugPort3                                   = bAttach;
                    stPorthpdUsb3.DpAltStatus                                         = DP_ALT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector2 = bAttach;
                    stTc3DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPICALiveReg.DpAltHotplugPort3)
                {
                    stPICAIIRReg.DpAltHotplugPort3 = TRUE;
                    stPorthpdUsb3.DpAltStatus      = DP_ALT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            // TBT
            else if (stPorthpdUsb3.TbtEnable && stPICAIMRReg.TbtHotplugPort3 == FALSE && stPICAIERReg.TbtHotplugPort3)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.TbtHotplugPort3  = TRUE;
                    stPICALiveReg.TbtHotplugPort3 = bAttach;
                    stPorthpdUsb3.TbtStatus       = TBT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                          = TRUE;
                }
                else if (stPICALiveReg.TbtHotplugPort3)
                {
                    stPICAIIRReg.TbtHotplugPort3 = TRUE;
                    stPorthpdUsb3.TbtStatus      = TBT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                         = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }

            if (SouthDdiTcCtrl.Tc3HpdEnable && stPCHIMRReg.HotplugTypecPort3 == FALSE && stPCHIERReg.HotplugTypecPort3)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort3                                     = TRUE;
                    stPCHLiveReg.HotplugTypecPort3                                    = bAttach;
                    SouthDdiTcCtrl.Tc3HpdStatus                                       = 0x2;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector2 = bAttach;
                    stTc3DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort3)
                {
                    stPCHIIRReg.HotplugTypecPort3 = TRUE;
                    SouthDdiTcCtrl.Tc3HpdStatus   = 0x1;
                    bRet                          = TRUE;
                }
            }

            break;
        case INTDPI_PORT:
        case INTHDMII_PORT:
            // DP Alt
            if (stPorthpdUsb4.DpAltEnable && stPICAIMRReg.DpAltHotplugPort4 == FALSE && stPICAIERReg.DpAltHotplugPort4)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.DpAltHotplugPort4                                    = TRUE;
                    stPICALiveReg.DpAltHotplugPort4                                   = bAttach;
                    stPorthpdUsb4.DpAltStatus                                         = DP_ALT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector3 = bAttach;
                    stTc4DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPICALiveReg.DpAltHotplugPort4)
                {
                    stPICAIIRReg.DpAltHotplugPort4 = TRUE;
                    stPorthpdUsb4.DpAltStatus      = DP_ALT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            // TBT
            else if (stPorthpdUsb4.TbtEnable && stPICAIMRReg.TbtHotplugPort4 == FALSE && stPICAIERReg.TbtHotplugPort4)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.TbtHotplugPort4  = TRUE;
                    stPICALiveReg.TbtHotplugPort4 = bAttach;
                    stPorthpdUsb4.TbtStatus       = TBT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                          = TRUE;
                }
                else if (stPICALiveReg.TbtHotplugPort4)
                {
                    stPICAIIRReg.TbtHotplugPort4 = TRUE;
                    stPorthpdUsb4.TbtStatus      = TBT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                         = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            if (SouthDdiTcCtrl.Tc4HpdEnable && stPCHIMRReg.HotplugTypecPort4 == FALSE && stPCHIERReg.HotplugTypecPort4)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort4                                     = TRUE;
                    stPCHLiveReg.HotplugTypecPort4                                    = bAttach;
                    SouthDdiTcCtrl.Tc4HpdStatus                                       = 0x2;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector3 = bAttach;
                    stTc4DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort4)
                {
                    stPCHIIRReg.HotplugTypecPort4 = TRUE;
                    SouthDdiTcCtrl.Tc4HpdStatus   = 0x1;
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
        stMasterIntctrl.DisplayInterruptsPending = TRUE;
        stDisplayIntCtrl.DePchInterruptsPending  = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthDdiCtlReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_TC_ADDR_ADP - pstGlobalMMORegData->ulMMIOBaseOffset])              = SouthDdiTcCtrl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_ISR_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset])                    = stPCHLiveReg.ulValue;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset])                = stPCHIIRReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset])  = stTypeCFia1DppmsStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPorthpdUsb1.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPorthpdUsb2.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPorthpdUsb3.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPorthpdUsb4.ulValue;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])        = stTc1DdiStatus.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])        = stTc2DdiStatus.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])        = stTc3DdiStatus.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])        = stTc4DdiStatus.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXPA1_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset])      = Fia1LiveStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXPA1_FIA2_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset])      = Fia2LiveStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_0_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPICALiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPICAIIRReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])         = stDisplayIntCtrl.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])            = stMasterIntctrl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_MTL - pstGlobalMMORegData->ulMMIOBaseOffset])         = stMasterTileIntCtrl.Value;
    }
    else
    {
        GFXVALSIM_DBG_MSG("Return Statement of HPD %d", bRet);
    }
    return bRet;
}

BOOLEAN MTL_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                    bRet                = TRUE;
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHLiveReg = { 0 };

    PICA_INTERRUPT_DEFINTION_GEN14 stPICALiveReg = { 0 };

    TCSS_DDI_STATUS_GEN14 stTcDdiStatus = { 0 };

    PORT_TX_DFLEXDPPMS_D14 stTypeCFia1DppmsStatus = { 0 };

    stTypeCFia1DppmsStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
    stPCHLiveReg.ulValue         = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
    // PICA Interrupt
    stPICALiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_0_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

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

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            stTcDdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
            if (PortConnectorInfo.IsTbt)
            {
                stPICALiveReg.TbtHotplugPort1 = bAttach;
            }
            else if (PortConnectorInfo.IsTypeC)
            {
                stPICALiveReg.DpAltHotplugPort1 = bAttach;
                stTcDdiStatus.Ready             = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort1 = bAttach;
                stTcDdiStatus.Ready            = bAttach;
            }
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTcDdiStatus.ulValue;
            stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector0                                                         = bAttach;
            break;

        case INTDPG_PORT:
        case INTHDMIG_PORT:
            stTcDdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
            if (PortConnectorInfo.IsTbt)
            {
                stPICALiveReg.TbtHotplugPort2 = bAttach;
            }
            else if (PortConnectorInfo.IsTypeC)
            {

                stPICALiveReg.DpAltHotplugPort2 = bAttach;
                stTcDdiStatus.Ready             = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort2 = bAttach;
                stTcDdiStatus.Ready            = bAttach;
            }
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTcDdiStatus.ulValue;
            stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector1                                                         = bAttach;
            break;

        case INTDPH_PORT:
        case INTHDMIH_PORT:
            stTcDdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
            if (PortConnectorInfo.IsTbt)
            {
                stPICALiveReg.TbtHotplugPort3 = bAttach;
            }
            else if (PortConnectorInfo.IsTypeC)
            {
                stPICALiveReg.DpAltHotplugPort3 = bAttach;
                stTcDdiStatus.Ready             = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort3 = bAttach;
                stTcDdiStatus.Ready            = bAttach;
            }
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTcDdiStatus.ulValue;
            stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector2                                                         = bAttach;
            break;

        case INTDPI_PORT:
        case INTHDMII_PORT:
            stTcDdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
            if (PortConnectorInfo.IsTbt)
            {
                stPICALiveReg.TbtHotplugPort4 = bAttach;
            }
            else if (PortConnectorInfo.IsTypeC)
            {
                stPICALiveReg.DpAltHotplugPort4 = bAttach;
                stTcDdiStatus.Ready             = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort4 = bAttach;
                stTcDdiStatus.Ready            = bAttach;
            }
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTcDdiStatus.ulValue;
            stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector3                                                         = bAttach;
            break;
        default:
            bRet = FALSE;
            break;
        }
    } while (FALSE);
    if (bRet)
    {
        stPCHLiveReg.HotplugDdia                                                                                                      = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])               = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia1DppmsStatus.Value;
        // PICA Interrupt
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_0_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPICALiveReg.ulValue;
    }
    return bRet;
}
BOOLEAN MTL_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    if (pstMMIOInterface)
    {

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_START] = DDI_AUX_DATA_A_START_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_END]   = DDI_AUX_DATA_A_END_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_A]        = DDI_AUX_CTL_A_GEN14;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_START] = DDI_AUX_DATA_B_START_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_END]   = DDI_AUX_DATA_B_END_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_B]        = DDI_AUX_CTL_B_GEN14;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = OFFSET_INVALID;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = OFFSET_INVALID;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_START] = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_END]   = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_E]        = OFFSET_INVALID;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_START] = DDI_AUX_DATA_TC1_START_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_END]   = DDI_AUX_DATA_TC1_END_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_F]        = DDI_AUX_CTL_TC1_GEN14;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_G_START] = DDI_AUX_DATA_TC2_START_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_G_END]   = DDI_AUX_DATA_TC2_END_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_G]        = DDI_AUX_CTL_TC2_GEN14;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_H_START] = DDI_AUX_DATA_TC3_START_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_H_END]   = DDI_AUX_DATA_TC3_END_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_H]        = DDI_AUX_CTL_TC3_GEN14;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_I_START] = DDI_AUX_DATA_TC4_START_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_I_END]   = DDI_AUX_DATA_TC4_END_GEN14;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_I]        = DDI_AUX_CTL_TC4_GEN14;

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

/*
This function will clear the HPD status value of a paticular DDI
which gfx driver wants to
*/

BOOLEAN MTL_MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                bRet            = FALSE;
    SHOTPLUG_CTL_DDI_GEN14 stHotPlugDdiCtl = { 0 };
    SHOTPLUG_CTL_TC_ADP    stSouthTCCtlreg = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb1   = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb2   = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb3   = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb4   = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stHotPlugDdiCtl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthTCCtlreg.Value   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPorthpdUsb1.ulValue   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_0_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPorthpdUsb2.ulValue   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPorthpdUsb3.ulValue   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPorthpdUsb4.ulValue   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
        case INTHDMIA_PORT:
            bRet = (BOOLEAN)stHotPlugDdiCtl.DdiaHpdEnable;
            break;
        case INTDPB_PORT:
        case INTHDMIB_PORT:
            bRet = (BOOLEAN)stHotPlugDdiCtl.DdibHpdEnable;
            break;
        case INTDPF_PORT:
        case INTHDMIF_PORT:
            if (stPorthpdUsb1.DpAltEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stPorthpdUsb1.TbtEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc1HpdEnable)
            {
                bRet = TRUE;
            }
            break;
        case INTDPG_PORT:
        case INTHDMIG_PORT:
            if (stPorthpdUsb2.DpAltEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stPorthpdUsb2.TbtEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc2HpdEnable)
            {
                bRet = TRUE;
            }
            break;
        case INTDPH_PORT:
        case INTHDMIH_PORT:
            if (stPorthpdUsb3.DpAltEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stPorthpdUsb3.TbtEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc3HpdEnable)
            {
                bRet = TRUE;
            }
            break;

        case INTDPI_PORT:
        case INTHDMII_PORT:
            if (stPorthpdUsb4.DpAltEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stPorthpdUsb4.TbtEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc4HpdEnable)
            {
                bRet = TRUE;
            }
            break;
        default:
            break;
        }
    } while (FALSE);

    return bRet;
}
BOOLEAN MTL_MMIOHANDLERS_HotPlugLiveStateMMIOReadHanlder(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = TRUE;

    SHOTPLUG_CTL_DDI_GEN14                 stHotPlugDdiCtl = { 0 };
    SHOTPLUG_CTL_TC_ADP                    stHotPlugTcCtl  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHLiveReg    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHLiveRegHw  = { 0 };
    ULONG                                  driverRegValue  = 0;

    stHotPlugDdiCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN14 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stHotPlugTcCtl.Value =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN14 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stPCHLiveReg.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, SDE_ISR_ADDR_GEN14, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        stPCHLiveRegHw.ulValue = driverRegValue;
        if (TRUE == stPCHLiveRegHw.HotplugDdia)
        {
            stPCHLiveReg.HotplugDdia = stPCHLiveRegHw.HotplugDdia;
        }
    }

    if (stHotPlugDdiCtl.DdibHpdEnable == FALSE)
    {
        stPCHLiveReg.HotplugDdib = FALSE;
    }
    if (stHotPlugTcCtl.Tc1HpdEnable == FALSE)
    {
        stPCHLiveReg.HotplugTypecPort1 = FALSE;
    }
    if (stHotPlugTcCtl.Tc2HpdEnable == FALSE)
    {
        stPCHLiveReg.HotplugTypecPort2 = FALSE;
    }
    if (stHotPlugTcCtl.Tc3HpdEnable == FALSE)
    {
        stPCHLiveReg.HotplugTypecPort3 = FALSE;
    }
    if (stHotPlugTcCtl.Tc4HpdEnable == FALSE)
    {
        stPCHLiveReg.HotplugTypecPort4 = FALSE;
    }
    *pulReadData = stPCHLiveReg.ulValue;
    return bRet;
}

BOOLEAN MTL_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                bRet                = FALSE;
    SHOTPLUG_CTL_DDI_GEN14 stHotPlugDdiCtl     = { 0 };
    SHOTPLUG_CTL_DDI_GEN14 stHotPlugDdiCtlTemp = { 0 };

    SHOTPLUG_CTL_TC_ADP stHotPlugCtl2     = { 0 };
    SHOTPLUG_CTL_TC_ADP stHotPlugCtlTemp2 = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN14 == ulMMIOOffset)
        {
            pstGlobalMMORegData         = &pstMMIOHandlerInfo->stGlobalMMORegData;
            stHotPlugDdiCtlTemp.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stHotPlugDdiCtl.ulValue = ulWriteData;

            stHotPlugDdiCtl.DdiaHpdStatus = stHotPlugDdiCtlTemp.DdiaHpdStatus;
            stHotPlugDdiCtl.DdibHpdStatus = stHotPlugDdiCtlTemp.DdibHpdStatus;
            stHotPlugDdiCtlTemp.ulValue   = ulWriteData;
            stHotPlugDdiCtl.DdiaHpdStatus &= ~stHotPlugDdiCtlTemp.DdiaHpdStatus;
            stHotPlugDdiCtl.DdibHpdStatus &= ~stHotPlugDdiCtlTemp.DdibHpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugDdiCtl.ulValue;
        }
        else
        {
            pstGlobalMMORegData     = &pstMMIOHandlerInfo->stGlobalMMORegData;
            stHotPlugCtlTemp2.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stHotPlugCtl2.Value = ulWriteData;

            stHotPlugCtl2.Tc1HpdStatus = stHotPlugCtlTemp2.Tc1HpdStatus;
            stHotPlugCtl2.Tc2HpdStatus = stHotPlugCtlTemp2.Tc2HpdStatus;
            stHotPlugCtl2.Tc3HpdStatus = stHotPlugCtlTemp2.Tc3HpdStatus;
            stHotPlugCtl2.Tc4HpdStatus = stHotPlugCtlTemp2.Tc4HpdStatus;

            stHotPlugCtlTemp2.Value = ulWriteData;

            stHotPlugCtl2.Tc1HpdStatus &= ~stHotPlugCtlTemp2.Tc1HpdStatus;
            stHotPlugCtl2.Tc2HpdStatus &= ~stHotPlugCtlTemp2.Tc2HpdStatus;
            stHotPlugCtl2.Tc3HpdStatus &= ~stHotPlugCtlTemp2.Tc3HpdStatus;
            stHotPlugCtl2.Tc4HpdStatus &= ~stHotPlugCtlTemp2.Tc4HpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl2.Value;
        }
        bRet = TRUE;
    } while (FALSE);

    return bRet;
}

BOOLEAN MTL_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData                                                                                       = &pstMMIOHandlerInfo->stGlobalMMORegData;
        stPorthpdUsb.ulValue                                                                                      = ulWriteData;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPorthpdUsb.ulValue;
        bRet                                                                                                      = TRUE;

    } while (FALSE);
    return bRet;
}

BOOLEAN MTL_MMIOHANDLERS_PICAHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = TRUE;
    // TYPE_C
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb1 = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb2 = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb3 = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb4 = { 0 };

    PICA_INTERRUPT_DEFINTION_GEN14 stPICALiveReg = { 0 };

    stPorthpdUsb1.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC1_ADDR_GEN14 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stPorthpdUsb2.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC2_ADDR_GEN14 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stPorthpdUsb3.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC3_ADDR_GEN14 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stPorthpdUsb4.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC4_ADDR_GEN14 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stPICALiveReg.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (stPorthpdUsb1.DpAltEnable == FALSE)
    {
        stPICALiveReg.DpAltHotplugPort1 = FALSE;
    }
    if (stPorthpdUsb2.DpAltEnable == FALSE)
    {
        stPICALiveReg.DpAltHotplugPort2 = FALSE;
    }
    if (stPorthpdUsb3.DpAltEnable == FALSE)
    {
        stPICALiveReg.DpAltHotplugPort3 = FALSE;
    }
    if (stPorthpdUsb4.DpAltEnable == FALSE)
    {
        stPICALiveReg.DpAltHotplugPort4 = FALSE;
    }

    *pulReadData = stPICALiveReg.ulValue;

    return bRet;
}

BOOLEAN MTL_MMIOHANDLERS_ScdcInterruptGeneration(PMMIO_INTERFACE pstMMIOInterface, PSCDC_ARGS pstScdcArgs)
{
    BOOLEAN                                bRet                = FALSE;
    GRAPHICS_MASTER_TILE_INTERRUPT_MTL     stMasterTileIntCtrl = { 0 };
    GFX_MSTR_INTR_GEN14                    stMasterIntCtrl     = { 0 };
    DISPLAY_INT_CTL_GEN14                  stDisplayIntCtrl    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stSouthDeInt        = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stMasterTileIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_MTL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stMasterIntCtrl.Value     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDisplayIntCtrl.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthDeInt.ulValue      = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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
        case INTHDMIF_PORT:
            stSouthDeInt.ScdcTc1 = TRUE;
            bRet                 = TRUE;
            break;
        case INTHDMIG_PORT:
            stSouthDeInt.ScdcTc2 = TRUE;
            bRet                 = TRUE;
            break;
        case INTHDMIH_PORT:
            stSouthDeInt.ScdcTc3 = TRUE;
            bRet                 = TRUE;
            break;
        case INTHDMII_PORT:
            stSouthDeInt.ScdcTc4 = TRUE;
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

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthDeInt.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])    = stMasterIntCtrl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_MTL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterTileIntCtrl.Value;
    }

    return bRet;
}

BOOLEAN MTL_MMIOHANDLERS_Psr1MMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN     bRet        = TRUE;
    SRD_CTL_D14 stSrdCtlReg = { 0 };
    PORT_TYPE   ePortType   = INTDPA_PORT;
    UINT16      Offset      = DPCD_SINK_DEVICE_PSR_STATUS;
    UINT8       Value;

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;
    PSIMDEV_EXTENTSION         pSimDrvExtension    = GetSimDrvExtension();
    PSIMDRVGFX_CONTEXT         pstSimDrvGfxContext = (PSIMDRVGFX_CONTEXT)pSimDrvExtension->pvSimDrvToGfxContext;

    do
    {
        if (NULL == pstSimDrvGfxContext)
            break;
        if (SRD_CTL_B_ADDR_D14 == ulMMIOOffset)
        {
            ePortType = INTDPB_PORT;
        }
        pstGlobalMMORegData                                                                                       = &pstMMIOHandlerInfo->stGlobalMMORegData;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = ulWriteData;
        stSrdCtlReg.Value                                                                                         = ulWriteData;

        if (peRegRWExecSite)
            *peRegRWExecSite = eExecHW;

        Value = 0x0;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSrdCtlReg.Value;

        bRet = COMMRXHANDLERS_SetPanelDpcd(((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo)->pstRxInfoArr, ePortType, Offset, Value);
    } while (FALSE);
    return bRet;
}

BOOLEAN MTL_MMIOHANDLERS_Psr2MMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN      bRet         = TRUE;
    PSR2_CTL_D14 stPsr2CtlReg = { 0 };
    PORT_TYPE    ePortType    = INTDPA_PORT;
    UINT16       Offset       = DPCD_SINK_DEVICE_PSR_STATUS;
    UINT8        Value;

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;
    PSIMDEV_EXTENTSION         pSimDrvExtension    = GetSimDrvExtension();
    PSIMDRVGFX_CONTEXT         pstSimDrvGfxContext = (PSIMDRVGFX_CONTEXT)pSimDrvExtension->pvSimDrvToGfxContext;

    do
    {
        if (NULL == pstSimDrvGfxContext)
            break;
        if (PSR2_CTL_B_ADDR_D14 == ulMMIOOffset)
        {
            ePortType = INTDPB_PORT;
        }
        pstGlobalMMORegData                                                                                       = &pstMMIOHandlerInfo->stGlobalMMORegData;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = ulWriteData;
        stPsr2CtlReg.Value                                                                                        = ulWriteData;

        if (peRegRWExecSite)
            *peRegRWExecSite = eExecHW;

        Value = 0x0;

        bRet = COMMRXHANDLERS_SetPanelDpcd(((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo)->pstRxInfoArr, ePortType, Offset, Value);
    } while (FALSE);
    return bRet;
}

BOOLEAN PTL_SetEdpOnTypeC(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortNum)
{
    BOOLEAN                       bRet                = FALSE;
    PICA_PHY_CONFIG_CONTROL_XE3_D PicaPhyCtrl         = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA    pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    if (ePortNum != INTDPB_PORT)
    {
        return TRUE;
    }

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        PicaPhyCtrl.Value       = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICA_PHY_CONFIG_CONTROL_0_ADDR_XE3_D - pstGlobalMMORegData->ulMMIOBaseOffset]);
        PicaPhyCtrl.Edp2OnTypec = TRUE;
        bRet                    = TRUE;

    } while (FALSE);

    if (bRet)
    {
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICA_PHY_CONFIG_CONTROL_0_ADDR_XE3_D - pstGlobalMMORegData->ulMMIOBaseOffset]) = PicaPhyCtrl.Value;
    }

    return bRet;
}

BOOLEAN PTL_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                                bRet                   = TRUE;
    PGLOBAL_MMIO_REGISTER_DATA             pstGlobalMMORegData    = &pstMMIOInterface->stGlobalMMORegData;
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHLiveReg           = { 0 };
    PICA_INTERRUPT_DEFINTION_GEN14         stPICALiveReg          = { 0 };
    TCSS_DDI_STATUS_GEN14                  stTcDdiStatus          = { 0 };
    PORT_TX_DFLEXDPPMS_D14                 stTypeCFia1DppmsStatus = { 0 };

    stTypeCFia1DppmsStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
    stPCHLiveReg.ulValue         = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
    // PICA Interrupt
    stPICALiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_0_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        switch (ePortType)
        {
        case INTDPA_PORT:
        case INTHDMIA_PORT:
            stPCHLiveReg.HotplugDdia = bAttach;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            if (TRUE == GFX_IS_WCL_CONFIG(pstMMIOInterface->stGfxGmdId))
            {
                stPCHLiveReg.HotplugDdib = bAttach;
            }
            else
            {
                stTcDdiStatus.ulValue          = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
                stPCHLiveReg.HotplugTypecPort1 = bAttach;
                stTcDdiStatus.Ready            = bAttach;
                *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTcDdiStatus.ulValue;
            }
            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            stTcDdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
            if (PortConnectorInfo.IsTbt)
            {
                stPICALiveReg.TbtHotplugPort1 = bAttach;
            }
            else if (PortConnectorInfo.IsTypeC)
            {
                stPICALiveReg.DpAltHotplugPort1 = bAttach;
                stTcDdiStatus.Ready             = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort1 = bAttach;
                stTcDdiStatus.Ready            = bAttach;
            }
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTcDdiStatus.ulValue;
            stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector0                                                         = bAttach;
            break;

        case INTDPG_PORT:
        case INTHDMIG_PORT:
            stTcDdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
            if (PortConnectorInfo.IsTbt)
            {
                stPICALiveReg.TbtHotplugPort2 = bAttach;
            }
            else if (PortConnectorInfo.IsTypeC)
            {

                stPICALiveReg.DpAltHotplugPort2 = bAttach;
                stTcDdiStatus.Ready             = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort2 = bAttach;
                stTcDdiStatus.Ready            = bAttach;
            }
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTcDdiStatus.ulValue;
            stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector1                                                         = bAttach;
            break;

        case INTDPH_PORT:
        case INTHDMIH_PORT:
            stTcDdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
            if (PortConnectorInfo.IsTbt)
            {
                stPICALiveReg.TbtHotplugPort3 = bAttach;
            }
            else if (PortConnectorInfo.IsTypeC)
            {
                stPICALiveReg.DpAltHotplugPort3 = bAttach;
                stTcDdiStatus.Ready             = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort3 = bAttach;
                stTcDdiStatus.Ready            = bAttach;
            }
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTcDdiStatus.ulValue;
            stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector2                                                         = bAttach;
            break;

        case INTDPI_PORT:
        case INTHDMII_PORT:
            stTcDdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
            if (PortConnectorInfo.IsTbt)
            {
                stPICALiveReg.TbtHotplugPort4 = bAttach;
            }
            else if (PortConnectorInfo.IsTypeC)
            {
                stPICALiveReg.DpAltHotplugPort4 = bAttach;
                stTcDdiStatus.Ready             = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort4 = bAttach;
                stTcDdiStatus.Ready            = bAttach;
            }
            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTcDdiStatus.ulValue;
            stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector3                                                         = bAttach;
            break;
        default:
            bRet = FALSE;
            break;
        }
    } while (FALSE);
    if (bRet)
    {
        stPCHLiveReg.HotplugDdia                                                                                                      = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])               = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia1DppmsStatus.Value;
        // PICA Interrupt
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_0_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPICALiveReg.ulValue;
    }
    return bRet;
}

BOOLEAN PTL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                            PORT_CONNECTOR_INFO PortConnectorInfo)
{

    BOOLEAN                            bRet                = FALSE;
    GRAPHICS_MASTER_TILE_INTERRUPT_MTL stMasterTileIntCtrl = { 0 };
    GFX_MSTR_INTR_GEN14                stMasterIntctrl     = { 0 };
    DISPLAY_INT_CTL_GEN14              stDisplayIntCtrl    = { 0 };

    SHOTPLUG_CTL_DDI_GEN14 stSouthDdiCtlReg = { 0 };
    SHOTPLUG_CTL_TC_ADP    SouthDdiTcCtrl   = { 0 };

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHLiveReg = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHIMRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHIIRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN14 stPCHIERReg  = { 0 };

    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb1 = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb2 = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb3 = { 0 };
    PORT_HOTPLUG_CTL_GEN14 stPorthpdUsb4 = { 0 };

    PICA_INTERRUPT_DEFINTION_GEN14 stPICALiveReg = { 0 };
    PICA_INTERRUPT_DEFINTION_GEN14 stPICAIMRReg  = { 0 };
    PICA_INTERRUPT_DEFINTION_GEN14 stPICAIIRReg  = { 0 };
    PICA_INTERRUPT_DEFINTION_GEN14 stPICAIERReg  = { 0 };

    PORT_TX_DFLEXDPPMS_D14 stTypeCFia1DppmsStatus = { 0 };
    PORT_TX_DFLEXPA1_D14   Fia1LiveStatus         = { 0 };
    PORT_TX_DFLEXPA1_D14   Fia2LiveStatus         = { 0 };

    TCSS_DDI_STATUS_GEN14 stTc1DdiStatus = { 0 };
    TCSS_DDI_STATUS_GEN14 stTc2DdiStatus = { 0 };
    TCSS_DDI_STATUS_GEN14 stTc3DdiStatus = { 0 };
    TCSS_DDI_STATUS_GEN14 stTc4DdiStatus = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;
    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stMasterTileIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_MTL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stMasterIntctrl.Value     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDisplayIntCtrl.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stSouthDdiCtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        SouthDdiTcCtrl.Value     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_TC_ADDR_ADP - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // Legacy
        stPCHLiveReg.ulValue         = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_ISR_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.ulValue          = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IMR_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.ulValue          = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.ulValue          = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IER_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFia1DppmsStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // PICA HPD
        stPorthpdUsb1.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPorthpdUsb2.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPorthpdUsb3.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPorthpdUsb4.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // PICA Interrupt

        stPICALiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_0_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPICAIMRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPICAIIRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPICAIERReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        Fia1LiveStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXPA1_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        Fia2LiveStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXPA1_FIA2_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // TypeC
        stTc1DdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc2DdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc3DdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc4DdiStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]);
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
                    stSouthDdiCtlReg.DdiaHpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdia) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdia = TRUE;
                    // Short Pulse
                    stSouthDdiCtlReg.DdiaHpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
            }
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            if (TRUE == GFX_IS_WCL_CONFIG(pstMMIOInterface->stGfxGmdId))
            {
                GFXVALSIM_DBG_MSG("WCL Platform! Arch: %ld, Release: %ld", pstMMIOInterface->stGfxGmdId.GmdID.GMDArch, pstMMIOInterface->stGfxGmdId.GmdID.GMDRelease);
                if (stSouthDdiCtlReg.DdibHpdEnable && stPCHIMRReg.HotplugDdib == FALSE && stPCHIERReg.HotplugDdib)
                {
                    if (bIsHPD)
                    {
                        stPCHIIRReg.HotplugDdib  = TRUE;
                        stPCHLiveReg.HotplugDdib = bAttach;
                        // Long Pulse
                        stSouthDdiCtlReg.DdibHpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN14;
                        bRet                           = TRUE;
                    }
                    else if (stPCHLiveReg.HotplugDdib) // Live state should already be up i.e display to be connected for SPI to make sense
                    {
                        stPCHIIRReg.HotplugDdib = TRUE;
                        // Short Pulse
                        stSouthDdiCtlReg.DdibHpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN14;
                        bRet                           = TRUE;
                    }
                }
            }
            else
            {
                GFXVALSIM_DBG_MSG("Non WCL Platform! Arch: %ld, Release: %ld", pstMMIOInterface->stGfxGmdId.GmdID.GMDArch, pstMMIOInterface->stGfxGmdId.GmdID.GMDRelease);
                // In PTL TC1 south ddi bits to be modified instead of DDI_B.
                if (SouthDdiTcCtrl.Tc1HpdEnable)
                {
                    if (bIsHPD)
                    {
                        stPCHIIRReg.HotplugTypecPort1  = TRUE;
                        stPCHLiveReg.HotplugTypecPort1 = bAttach;
                        SouthDdiTcCtrl.Tc1HpdStatus    = 0x2;
                        stTc1DdiStatus.Ready           = bAttach;
                        bRet                           = TRUE;
                    }
                    else if (stPCHLiveReg.HotplugTypecPort1)
                    {
                        stPCHIIRReg.HotplugTypecPort1 = TRUE;
                        SouthDdiTcCtrl.Tc1HpdStatus   = 0x1;
                        bRet                          = TRUE;
                    }
                }
            }
            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            // DP Alt TC
            if (stPorthpdUsb1.DpAltEnable && stPICAIMRReg.DpAltHotplugPort1 == FALSE && stPICAIERReg.DpAltHotplugPort1)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.DpAltHotplugPort1                                    = TRUE;
                    stPICALiveReg.DpAltHotplugPort1                                   = bAttach;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTc1DdiStatus.Ready                                              = bAttach;
                    stPorthpdUsb1.DpAltStatus                                         = DP_ALT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                                                              = TRUE;
                }
                else if (stPICALiveReg.DpAltHotplugPort1)
                {
                    stPICAIIRReg.DpAltHotplugPort1 = TRUE;
                    stPorthpdUsb1.DpAltStatus      = DP_ALT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            // TBT
            else if (stPorthpdUsb1.TbtEnable && stPICAIMRReg.TbtHotplugPort1 == FALSE && stPICAIERReg.TbtHotplugPort1)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.TbtHotplugPort1  = TRUE;
                    stPICALiveReg.TbtHotplugPort1 = bAttach;
                    stPorthpdUsb1.TbtStatus       = TBT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                          = TRUE;
                }
                else if (stPICALiveReg.TbtHotplugPort1)
                {
                    stPICAIIRReg.TbtHotplugPort1 = TRUE;
                    stPorthpdUsb1.TbtStatus      = TBT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                         = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            if (SouthDdiTcCtrl.Tc1HpdEnable && stPCHIMRReg.HotplugTypecPort1 == FALSE && stPCHIERReg.HotplugTypecPort1)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort1                                     = TRUE;
                    stPCHLiveReg.HotplugTypecPort1                                    = bAttach;
                    SouthDdiTcCtrl.Tc1HpdStatus                                       = 0x2;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTc1DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort1)
                {
                    stPCHIIRReg.HotplugTypecPort1 = TRUE;
                    SouthDdiTcCtrl.Tc1HpdStatus   = 0x1;
                    bRet                          = TRUE;
                }
            }
            break;

        case INTDPG_PORT:
        case INTHDMIG_PORT:
            // DP Alt
            if (stPorthpdUsb2.DpAltEnable && stPICAIMRReg.DpAltHotplugPort2 == FALSE && stPICAIERReg.DpAltHotplugPort2)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.DpAltHotplugPort2                                    = TRUE;
                    stPICALiveReg.DpAltHotplugPort2                                   = bAttach;
                    stPorthpdUsb2.DpAltStatus                                         = DP_ALT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTc2DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPICALiveReg.DpAltHotplugPort2)
                {
                    stPICAIIRReg.DpAltHotplugPort2 = TRUE;
                    stPorthpdUsb2.DpAltStatus      = DP_ALT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    stTc2DdiStatus.Ready           = bAttach;
                    bRet                           = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            // TBT
            else if (stPorthpdUsb2.TbtEnable && stPICAIMRReg.TbtHotplugPort2 == FALSE && stPICAIERReg.TbtHotplugPort2)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.TbtHotplugPort2  = TRUE;
                    stPICALiveReg.TbtHotplugPort2 = bAttach;
                    stPorthpdUsb2.TbtStatus       = TBT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                          = TRUE;
                }
                else if (stPICALiveReg.TbtHotplugPort2)
                {
                    stPICAIIRReg.TbtHotplugPort2 = TRUE;
                    stPorthpdUsb2.TbtStatus      = TBT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                         = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }

            if (SouthDdiTcCtrl.Tc2HpdEnable && stPCHIMRReg.HotplugTypecPort2 == FALSE && stPCHIERReg.HotplugTypecPort2)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort2                                     = TRUE;
                    stPCHLiveReg.HotplugTypecPort2                                    = bAttach;
                    SouthDdiTcCtrl.Tc2HpdStatus                                       = 0x2;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTc2DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort2)
                {
                    stPCHIIRReg.HotplugTypecPort2 = TRUE;
                    SouthDdiTcCtrl.Tc2HpdStatus   = 0x1;
                    bRet                          = TRUE;
                }
            }

            break;

        case INTDPH_PORT:
        case INTHDMIH_PORT:
            // DP Alt
            if (stPorthpdUsb3.DpAltEnable && stPICAIMRReg.DpAltHotplugPort3 == FALSE && stPICAIERReg.DpAltHotplugPort3)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.DpAltHotplugPort3                                    = TRUE;
                    stPICALiveReg.DpAltHotplugPort3                                   = bAttach;
                    stPorthpdUsb3.DpAltStatus                                         = DP_ALT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector2 = bAttach;
                    stTc3DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPICALiveReg.DpAltHotplugPort3)
                {
                    stPICAIIRReg.DpAltHotplugPort3 = TRUE;
                    stPorthpdUsb3.DpAltStatus      = DP_ALT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            // TBT
            else if (stPorthpdUsb3.TbtEnable && stPICAIMRReg.TbtHotplugPort3 == FALSE && stPICAIERReg.TbtHotplugPort3)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.TbtHotplugPort3  = TRUE;
                    stPICALiveReg.TbtHotplugPort3 = bAttach;
                    stPorthpdUsb3.TbtStatus       = TBT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                          = TRUE;
                }
                else if (stPICALiveReg.TbtHotplugPort3)
                {
                    stPICAIIRReg.TbtHotplugPort3 = TRUE;
                    stPorthpdUsb3.TbtStatus      = TBT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                         = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }

            if (SouthDdiTcCtrl.Tc3HpdEnable && stPCHIMRReg.HotplugTypecPort3 == FALSE && stPCHIERReg.HotplugTypecPort3)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort3                                     = TRUE;
                    stPCHLiveReg.HotplugTypecPort3                                    = bAttach;
                    SouthDdiTcCtrl.Tc3HpdStatus                                       = 0x2;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector2 = bAttach;
                    stTc3DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort3)
                {
                    stPCHIIRReg.HotplugTypecPort3 = TRUE;
                    SouthDdiTcCtrl.Tc3HpdStatus   = 0x1;
                    bRet                          = TRUE;
                }
            }

            break;
        case INTDPI_PORT:
        case INTHDMII_PORT:
            // DP Alt
            if (stPorthpdUsb4.DpAltEnable && stPICAIMRReg.DpAltHotplugPort4 == FALSE && stPICAIERReg.DpAltHotplugPort4)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.DpAltHotplugPort4                                    = TRUE;
                    stPICALiveReg.DpAltHotplugPort4                                   = bAttach;
                    stPorthpdUsb4.DpAltStatus                                         = DP_ALT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector3 = bAttach;
                    stTc4DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPICALiveReg.DpAltHotplugPort4)
                {
                    stPICAIIRReg.DpAltHotplugPort4 = TRUE;
                    stPorthpdUsb4.DpAltStatus      = DP_ALT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                           = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            // TBT
            else if (stPorthpdUsb4.TbtEnable && stPICAIMRReg.TbtHotplugPort4 == FALSE && stPICAIERReg.TbtHotplugPort4)
            {
                if (bIsHPD)
                {
                    stPICAIIRReg.TbtHotplugPort4  = TRUE;
                    stPICALiveReg.TbtHotplugPort4 = bAttach;
                    stPorthpdUsb4.TbtStatus       = TBT_STATUS_LONG_PULSE_DETECTED_GEN14;
                    bRet                          = TRUE;
                }
                else if (stPICALiveReg.TbtHotplugPort4)
                {
                    stPICAIIRReg.TbtHotplugPort4 = TRUE;
                    stPorthpdUsb4.TbtStatus      = TBT_STATUS_SHORT_PULSE_DETECTED_GEN14;
                    bRet                         = TRUE;
                }
                stPCHLiveReg.PICAInterrupt = TRUE;
                stPCHIIRReg.PICAInterrupt  = TRUE;
            }
            if (SouthDdiTcCtrl.Tc4HpdEnable && stPCHIMRReg.HotplugTypecPort4 == FALSE && stPCHIERReg.HotplugTypecPort4)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort4                                     = TRUE;
                    stPCHLiveReg.HotplugTypecPort4                                    = bAttach;
                    SouthDdiTcCtrl.Tc4HpdStatus                                       = 0x2;
                    stTypeCFia1DppmsStatus.DisplayPortPhyModeStatusForTypeCConnector3 = bAttach;
                    stTc4DdiStatus.Ready                                              = bAttach;
                    bRet                                                              = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort4)
                {
                    stPCHIIRReg.HotplugTypecPort4 = TRUE;
                    SouthDdiTcCtrl.Tc4HpdStatus   = 0x1;
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
        stMasterIntctrl.DisplayInterruptsPending = TRUE;
        stDisplayIntCtrl.DePchInterruptsPending  = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthDdiCtlReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SHOTPLUG_CTL_TC_ADDR_ADP - pstGlobalMMORegData->ulMMIOBaseOffset])              = SouthDdiTcCtrl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_ISR_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset])                    = stPCHLiveReg.ulValue;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_GEN14)-pstGlobalMMORegData->ulMMIOBaseOffset])                = stPCHIIRReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset])  = stTypeCFia1DppmsStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPorthpdUsb1.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPorthpdUsb2.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPorthpdUsb3.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_HOTPLUG_CTL_USBC4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPorthpdUsb4.ulValue;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])        = stTc1DdiStatus.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])        = stTc2DdiStatus.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])        = stTc3DdiStatus.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])        = stTc4DdiStatus.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXPA1_FIA1_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset])      = Fia1LiveStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXPA1_FIA2_ADDR_D14 - pstGlobalMMORegData->ulMMIOBaseOffset])      = Fia2LiveStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_0_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPICALiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PICAINTERRUPTDEFINTION_2_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPICAIIRReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])         = stDisplayIntCtrl.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN14 - pstGlobalMMORegData->ulMMIOBaseOffset])            = stMasterIntctrl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_TILE_INTR_ADDR_MTL - pstGlobalMMORegData->ulMMIOBaseOffset])         = stMasterTileIntCtrl.Value;
    }
    else
    {
        GFXVALSIM_DBG_MSG("Return Statement of HPD %d", bRet);
    }
    return bRet;
}

/**-------------------------------------------------------------
 * @brief ELG_MMIOHANDLERS_ProductionSkuMMIOReadHandler
 *
 * Description: Production sku can be authenticated only with Production Oprom signature done by ubit. When we modify vbt, from infra we sign it with debug signature.
                This works fine for pre-production sku's. For MA configurations, we see production sku's connected. We are resetting production sku flag in valsim.
                With this change, gfx driver thinks it is an pre-production sku and authenticates with debug signature.
 *-------------------------------------------------------------*/
BOOLEAN ELG_MMIOHANDLERS_ProductionSkuMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
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

BOOLEAN NVL_MMIOHANDLERS_SetupIOMRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                  bRet        = FALSE;
    IOM_DP_RESOURCE_MNG_XE3P stIomResMng = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stIomResMng.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[IOM_DP_RESOURCE_MNG_ADDR_XE3P_D - pstGlobalMMORegData->ulMMIOBaseOffset]);

        GFXVALSIM_DBG_MSG("Initial IOM register value %ul", stIomResMng.ulValue);

        // Any TC0 to TC3 DDI which is free need to be reset to some consumed value before freeing required DDI
        // For very first plug , all TC ports would be free initially , they need to be locked before freeing only required port.
        // For unplug call, driver would free the specific port in unplug sequence. Any plug call after that will have that port in free state. That needs to be locked before
        // proceeding.
        if (stIomResMng.DDI0_CONSUMER == CONSUMER_FREE_XE3P_D)
        {
            stIomResMng.DDI0_CONSUMER = CONSUMER_TBT0_DPIN0_XE3P_D;
        }
        if (stIomResMng.DDI1_CONSUMER == CONSUMER_FREE_XE3P_D)
        {
            stIomResMng.DDI1_CONSUMER = CONSUMER_TBT0_DPIN0_XE3P_D;
        }
        if (stIomResMng.DDI2_CONSUMER == CONSUMER_FREE_XE3P_D)
        {
            stIomResMng.DDI2_CONSUMER = CONSUMER_TBT0_DPIN0_XE3P_D;
        }
        if (stIomResMng.DDI3_CONSUMER == CONSUMER_FREE_XE3P_D)
        {
            stIomResMng.DDI3_CONSUMER = CONSUMER_TBT0_DPIN0_XE3P_D;
        }

        switch (ePortType)
        {
        case INTDPA_PORT:
        case INTHDMIA_PORT:
        case INTDPB_PORT:
        case INTHDMIB_PORT:
            bRet = TRUE;
            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            if (bAttach && bIsHPD)
            {
                stIomResMng.DDI0_CONSUMER = CONSUMER_FREE_XE3P_D; // Free DDI0 or Port F
            }
            bRet = TRUE;
            break;

        case INTDPG_PORT:
        case INTHDMIG_PORT:
            if (bAttach && bIsHPD)
            {
                stIomResMng.DDI1_CONSUMER = CONSUMER_FREE_XE3P_D; // Free DDI1 or Port G
            }
            bRet = TRUE;
            break;

        case INTDPH_PORT:
        case INTHDMIH_PORT:
            if (bAttach && bIsHPD)
            {
                stIomResMng.DDI2_CONSUMER = CONSUMER_FREE_XE3P_D; // Free DDI2 or Port H
            }
            bRet = TRUE;
            break;

        case INTDPI_PORT:
        case INTHDMII_PORT:
            if (bAttach && bIsHPD)
            {
                stIomResMng.DDI3_CONSUMER = CONSUMER_FREE_XE3P_D; // Free DDI3 or Port I
            }
            bRet = TRUE;
            break;

        default:
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[IOM_DP_RESOURCE_MNG_ADDR_XE3P_D - pstGlobalMMORegData->ulMMIOBaseOffset]) = stIomResMng.ulValue;
        GFXVALSIM_DBG_MSG("Modified IOM register value %ul", stIomResMng.ulValue);
    }
    else
    {
        GFXVALSIM_DBG_MSG("Return Flag of IOM Register Setup %d", bRet);
    }

    return bRet;
}