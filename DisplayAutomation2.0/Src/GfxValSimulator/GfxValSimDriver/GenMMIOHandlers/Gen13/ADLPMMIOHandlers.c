/**********************************************************************************************************
ADLP HPD Flow

MASTER_CTL_INT(0x190010) - MasterInterruptRW[Gfx IP or others] Get the Interrupt Source ie Display Interrupt
DISPLAY_INTR_CTL_ADDR_ICL(0x44200) - DisplayInterruptRW[Display, GPU or Render] Get the Legacy Interrupt Source means is it HPD/Port/Pipe/Audio
SOUTH_DE_IIR_ADDR_SPT(0xC4008) - HotPlugIIRWrite[Pipe or Port interrupt Interrupt Source ie PCH Display]
SOUTH_HOT_PLUG_CTL_ADDR_SPT(0xC4030) - HotPlugCTLWrite[Which port is being connected? Short or Long Pulse]

SOUTH_DE_ISR_ADDR_SPT(0xc4000) - HotPlugLiveStateRead[Connected / Disconnected]


Call Flow: Gfx Mainline Driver: Legacy:
1. ADLP_INTRHANDLER_GetInterruptSource  ---> case ADLP_DISPLAY_INTERRUPT_BIT_POS --> LegacyInterruptsOccurred Flag should be set
2. ADLP_INTRHANDLER_GetLegacyInterruptSource
3. ADLP_INTRHANDLER_GetHPDInterruptSource

********************************************************************************************************/
#include "ADLPMMIO.h"
#include "..\..\DriverInterfaces\SimDrvToGfx.h"
#include "..\\..\\CommonInclude\\ETWLogging.h"

BOOLEAN ADLP_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {
        bRet = ADLP_MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);
    } while (FALSE);

    return bRet;
}

BOOLEAN ADLP_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Master Interrupt Control Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50832
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_INTR_ADDR_GEN13, GFX_MSTR_INTR_ADDR_GEN13, 0, NULL, NULL, 0, TRUE, eReadCombine,
                                                       GEN13_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler, GEN13_CMN_MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler, NULL,
                                                       NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Display Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50081
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DISPLAY_INTR_CTL_ADDR_GEN13, DISPLAY_INTR_CTL_ADDR_GEN13, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN13_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler, GEN13_CMN_MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler, NULL,
                                                       NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50478
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_ISR_ADDR_GEN13, SDE_ISR_ADDR_GEN13, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       ADLP_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SDE_IIR_ADDR_GEN13, SDE_IIR_ADDR_GEN13, 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       GEN13_CMN_MMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50471
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50472
        // The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port
        // These two are the south hot plug control registers
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN13, SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN13, 0, NULL, NULL,
                                                       0, TRUE, eNoExecHw, NULL, ADLP_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50093
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, TBT_HOTPLUG_CTL_ADDR_D13, TBT_HOTPLUG_CTL_ADDR_D13, 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       ADLP_MMIOHANDLERS_TBTHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/50093
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, TC_HOTPLUG_CTL_ADDR_D13, TC_HOTPLUG_CTL_ADDR_D13, 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       ADLP_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

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
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DE_HPD_ISR_ADDR_D13, DE_HPD_ISR_ADDR_D13, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       ADLP_MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL); // ISR LiveState

        if (bRet == FALSE)
        {
            break;
        }

        // TCSS_DDI_STATUS_D13 Handlers
        // BSPEC Ref: https://gfxspecs.intel.com/Predator/Home/Index/55481
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, TCSS_DDI_STATUS_1_ADDR_D13, TCSS_DDI_STATUS_4_ADDR_D13, 0, NULL, NULL, 0, TRUE, eNoExecHw,
                                                       NULL, GEN13_CMN_MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXPA1_FIA1_ADDR_D13, PORT_TX_DFLEXPA1_FIA1_ADDR_D13, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN13_CMN_MMIOHANDLERS_GetPinAssignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXPA1_FIA2_ADDR_D13, PORT_TX_DFLEXPA1_FIA2_ADDR_D13, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN13_CMN_MMIOHANDLERS_GetPinAssignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        /*To handle upfront link training
        Each FIA can have upto 4 instance of scratch pad
        FIA1 - SP1 to SP4
        */
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA1_ADDR_D13, PORT_TX_DFLEXDPSP4_FIA1_ADDR_D13, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN13_CMN_MMIOHANDLERS_GetLanesAssignedfromDKLPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        /*To handle upfront link training
        Each FIA can have upto 4 instance of scratch pad
        FIA2 - SP1 to SP4
        */
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA2_ADDR_D13, PORT_TX_DFLEXDPSP4_FIA2_ADDR_D13, 0, NULL, NULL, 0, FALSE,
                                                       eReadCombine, GEN13_CMN_MMIOHANDLERS_GetLanesAssignedfromDKLPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Workaround to support TypeC ports. In the default mode for TC ports, IOM wouldn't have initialized PHY. So, the DDI Buffer is IDLE. As per the recommendation from
        // Ganesh/Raghu, it is being masked in valsim driver.
        for (int ddi_offset = DDI_BUF_CTL_USBC1_ADDR_D13; ddi_offset <= DDI_BUF_CTL_USBC4_ADDR_D13; ddi_offset += 256)
        {
            bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, ddi_offset, ddi_offset, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                           ADLP_MMIOHANDLERS_DdiBufferControlMMIOReadHandler, NULL, NULL, NULL, NULL);

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
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PWR_WELL_CTL_DDI2_ADDR_D13, PWR_WELL_CTL_DDI2_ADDR_D13, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       ADLP_MMIOHANDLERS_PwrWellDDIControlMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        // To update the DPCD 2008H for PSR panel based on PSR enable/disable state
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SRD_CTL_A_ADDR_D13, SRD_CTL_A_ADDR_D13, 0, NULL, NULL, 0, TRUE, eExecHW, NULL,
                                                       ADLP_MMIOHANDLERS_Psr1MMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        // To update the DPCD 2008H for PSR panel based on PSR enable/disable state
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SRD_CTL_B_ADDR_D13, SRD_CTL_B_ADDR_D13, 0, NULL, NULL, 0, TRUE, eExecHW, NULL,
                                                       ADLP_MMIOHANDLERS_Psr1MMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        // To update the DPCD 2008H for PSR panel based on PSR enable/disable state
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PSR2_CTL_A_ADDR_D13, PSR2_CTL_A_ADDR_D13, 0, NULL, NULL, 0, TRUE, eExecHW, NULL,
                                                       ADLP_MMIOHANDLERS_Psr2MMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        // To update the DPCD 2008H for PSR panel based on PSR enable/disable state
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PSR2_CTL_B_ADDR_D13, PSR2_CTL_B_ADDR_D13, 0, NULL, NULL, 0, TRUE, eExecHW, NULL,
                                                       ADLP_MMIOHANDLERS_Psr2MMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN ADLP_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
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

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = OFFSET_INVALID;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = OFFSET_INVALID;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_START] = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_END]   = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_E]        = OFFSET_INVALID;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_START] = DDI_AUX_DATA_TC1_START_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_END]   = DDI_AUX_DATA_TC1_END_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_F]        = DDI_AUX_CTL_TC1_GEN13;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_G_START] = DDI_AUX_DATA_TC2_START_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_G_END]   = DDI_AUX_DATA_TC2_END_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_G]        = DDI_AUX_CTL_TC2_GEN13;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_H_START] = DDI_AUX_DATA_TC3_START_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_H_END]   = DDI_AUX_DATA_TC3_END_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_H]        = DDI_AUX_CTL_TC3_GEN13;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_I_START] = DDI_AUX_DATA_TC4_START_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_I_END]   = DDI_AUX_DATA_TC4_END_GEN13;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_I]        = DDI_AUX_CTL_TC4_GEN13;

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

BOOLEAN ADLP_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                             PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN               bRet             = FALSE;
    GFX_MSTR_INTR_GEN13   stMasterIntCtrl  = { 0 };
    DISPLAY_INT_CTL_GEN13 stDisplayIntCtrl = { 0 };

    SHOTPLUG_CTL_DDI_GEN13 stSouthDdiCtlReg = { 0 };
    SHOTPLUG_CTL_TC_GEN13  stSouthTCCtlReg  = { 0 };

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 stPCHLiveReg = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 stPCHIMRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 stPCHIIRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 stPCHIERReg  = { 0 };

    HOTPLUG_CTL_D13 stTBTHotPlugCtl   = { 0 };
    HOTPLUG_CTL_D13 stTYPECHotPlugCtl = { 0 };

    DE_HPD_INTERRUPT_DEFINITION_D13 stDEHPDISR = { 0 };
    DE_HPD_INTERRUPT_DEFINITION_D13 stDEHPDIMR = { 0 };
    DE_HPD_INTERRUPT_DEFINITION_D13 stDEHPDIIR = { 0 };
    DE_HPD_INTERRUPT_DEFINITION_D13 stDEHPDIER = { 0 };

    TCSS_DDI_STATUS_D13 stTc1DdiStatus = { 0 };
    TCSS_DDI_STATUS_D13 stTc2DdiStatus = { 0 };
    TCSS_DDI_STATUS_D13 stTc3DdiStatus = { 0 };
    TCSS_DDI_STATUS_D13 stTc4DdiStatus = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            GFXVALSIM_DBG_MSG("ADLP_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI: pstMMIOInterface is null.");
            break;
        }

        //// Check if HPD has been enabled by Gfx
        // if (FALSE == ADLP_MMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType, PortConnectorInfo))
        //{
        //  GFXVALSIM_DBG_MSG("ADLP_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI: HPD not enabled for  port.");
        //    break;
        //}

        stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stSouthDdiCtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stSouthTCCtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Legacy
        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_ISR_ADDR_GEN13)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IMR_ADDR_GEN13)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IIR_ADDR_GEN13)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SDE_IER_ADDR_GEN13)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        // TypeC & TBT North Bridge
        stTBTHotPlugCtl.Value   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TBT_HOTPLUG_CTL_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTYPECHotPlugCtl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TC_HOTPLUG_CTL_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDEHPDISR.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_ISR_ADDR_D13)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIMR.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_IMR_ADDR_D13)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIIR.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_IIR_ADDR_D13)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIER.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_IER_ADDR_D13)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        // TC DKL PHY
        stTc1DdiStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc2DdiStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc3DdiStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc4DdiStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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
                    stSouthDdiCtlReg.DdiaHpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdia) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdia = TRUE;
                    // Short Pulse
                    stSouthDdiCtlReg.DdiaHpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
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
                    stSouthDdiCtlReg.DdibHpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugDdib) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugDdib        = TRUE;
                    stSouthDdiCtlReg.DdibHpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                           = TRUE;
                }
            }

            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            // North Bridge
            if (stTYPECHotPlugCtl.Port1HpdEnable && (FALSE == stDEHPDIMR.Tc1Hotplug) && stDEHPDIER.Tc1Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc1Hotplug            = TRUE;
                    stDEHPDISR.Tc1Hotplug            = bAttach; // LiveState Register
                    stTYPECHotPlugCtl.Port1HpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc1DdiStatus.Ready             = bAttach;
                    bRet                             = TRUE;
                }
                else if (stDEHPDISR.Tc1Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc1Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port1HpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                             = TRUE;
                }
            }
            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port1HpdEnable && (FALSE == stDEHPDIMR.Tbt1Hotplug) && stDEHPDIER.Tbt1Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt1Hotplug         = TRUE;
                    stDEHPDISR.Tbt1Hotplug         = bAttach; // LiveState Register
                    stTBTHotPlugCtl.Port1HpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc1DdiStatus.Ready           = bAttach;
                    bRet                           = TRUE;
                }
                else if (stDEHPDISR.Tbt1Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt1Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port1HpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                           = TRUE;
                }
            }

            // Legacy south bridge
            if (stSouthTCCtlReg.Tc1HpdEnable && stPCHIMRReg.HotplugTypecPort1 == FALSE && stPCHIERReg.HotplugTypecPort1)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort1  = TRUE;
                    stPCHLiveReg.HotplugTypecPort1 = bAttach;
                    stSouthTCCtlReg.Tc1HpdStatus   = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc1DdiStatus.Ready           = bAttach;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort1) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort1 = TRUE;
                    stSouthTCCtlReg.Tc1HpdStatus  = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                          = TRUE;
                }
            }

            break;

        case INTDPG_PORT:
        case INTHDMIG_PORT:

            if (stTYPECHotPlugCtl.Port2HpdEnable && (FALSE == stDEHPDIMR.Tc2Hotplug) && stDEHPDIER.Tc2Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc2Hotplug = TRUE;
                    stDEHPDISR.Tc2Hotplug = bAttach; // LiveState Register

                    stTc2DdiStatus.Ready             = bAttach;
                    stTYPECHotPlugCtl.Port2HpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;

                    bRet = TRUE;
                }
                else if (stDEHPDISR.Tc2Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc2Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port2HpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                             = TRUE;
                }
            }
            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port2HpdEnable && (FALSE == stDEHPDIMR.Tbt2Hotplug) && stDEHPDIER.Tbt2Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt2Hotplug         = TRUE;
                    stDEHPDISR.Tbt2Hotplug         = bAttach; // LiveState Register
                    stTBTHotPlugCtl.Port2HpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc2DdiStatus.Ready           = bAttach;
                    bRet                           = TRUE;
                }
                else if (stDEHPDISR.Tbt2Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt2Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port2HpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                           = TRUE;
                }
            }

            // Legacy south bridge
            if (stSouthTCCtlReg.Tc2HpdEnable && stPCHIMRReg.HotplugTypecPort2 == FALSE && stPCHIERReg.HotplugTypecPort2)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort2  = TRUE;
                    stPCHLiveReg.HotplugTypecPort2 = bAttach;
                    stSouthTCCtlReg.Tc2HpdStatus   = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc2DdiStatus.Ready           = bAttach;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort2) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort2 = TRUE;
                    stSouthTCCtlReg.Tc2HpdStatus  = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                          = TRUE;
                }
            }

            break;

        case INTDPH_PORT:
        case INTHDMIH_PORT:

            if (stTYPECHotPlugCtl.Port3HpdEnable && (FALSE == stDEHPDIMR.Tc3Hotplug) && stDEHPDIER.Tc3Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc3Hotplug            = TRUE;
                    stDEHPDISR.Tc3Hotplug            = bAttach; // LiveState Register
                    stTYPECHotPlugCtl.Port3HpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc3DdiStatus.Ready             = bAttach;
                    bRet                             = TRUE;
                }
                else if (stDEHPDISR.Tc3Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc3Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port3HpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                             = TRUE;
                }
            }
            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port3HpdEnable && (FALSE == stDEHPDIMR.Tbt3Hotplug) && stDEHPDIER.Tbt3Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt3Hotplug         = TRUE;
                    stDEHPDISR.Tbt3Hotplug         = bAttach; // LiveState Register
                    stTBTHotPlugCtl.Port3HpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc3DdiStatus.Ready           = bAttach;
                    bRet                           = TRUE;
                }
                else if (stDEHPDISR.Tbt3Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt3Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port3HpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                           = TRUE;
                }
            }
            // Legacy south bridge
            if (stSouthTCCtlReg.Tc3HpdEnable && stPCHIMRReg.HotplugTypecPort3 == FALSE && stPCHIERReg.HotplugTypecPort3)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort3  = TRUE;
                    stPCHLiveReg.HotplugTypecPort3 = bAttach;
                    stSouthTCCtlReg.Tc3HpdStatus   = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc3DdiStatus.Ready           = bAttach;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort3) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort3 = TRUE;
                    stSouthTCCtlReg.Tc3HpdStatus  = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                          = TRUE;
                }
            }

            break;

        case INTDPI_PORT:
        case INTHDMII_PORT:

            if (stTYPECHotPlugCtl.Port4HpdEnable && (FALSE == stDEHPDIMR.Tc4Hotplug) && stDEHPDIER.Tc4Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc4Hotplug            = TRUE;
                    stDEHPDISR.Tc4Hotplug            = bAttach; // LiveState Register
                    stTYPECHotPlugCtl.Port4HpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc4DdiStatus.Ready             = bAttach;
                    bRet                             = TRUE;
                }
                else if (stDEHPDISR.Tc4Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc4Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port4HpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                             = TRUE;
                }
            }
            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port4HpdEnable && (FALSE == stDEHPDIMR.Tbt4Hotplug) && stDEHPDIER.Tbt4Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt4Hotplug         = TRUE;
                    stDEHPDISR.Tbt4Hotplug         = bAttach; // LiveState Register
                    stTBTHotPlugCtl.Port4HpdStatus = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc4DdiStatus.Ready           = bAttach;
                    bRet                           = TRUE;
                }
                else if (stDEHPDISR.Tbt4Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt4Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port4HpdStatus = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
                    bRet                           = TRUE;
                }
            }
            // Legacy south bridge
            if (stSouthTCCtlReg.Tc4HpdEnable && stPCHIMRReg.HotplugTypecPort4 == FALSE && stPCHIERReg.HotplugTypecPort4)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort4  = TRUE;
                    stPCHLiveReg.HotplugTypecPort4 = bAttach;
                    stSouthTCCtlReg.Tc4HpdStatus   = HPD_STATUS_LONG_PULSE_DETECTED_GEN13;
                    stTc4DdiStatus.Ready           = bAttach;
                    bRet                           = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort4) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort4 = TRUE;
                    stSouthTCCtlReg.Tc4HpdStatus  = HPD_STATUS_SHORT_PULSE_DETECTED_GEN13;
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

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset])   = stSouthDdiCtlReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthTCCtlReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset])                      = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset])                      = stPCHIIRReg.ulValue;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TBT_HOTPLUG_CTL_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTBTHotPlugCtl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TC_HOTPLUG_CTL_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset])  = stTYPECHotPlugCtl.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_ISR_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset])      = stDEHPDISR.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_IIR_ADDR_D13)-pstGlobalMMORegData->ulMMIOBaseOffset])      = stDEHPDIIR.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTc1DdiStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTc2DdiStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTc3DdiStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTc4DdiStatus.Value;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;
    }
    else
    {
        GFXVALSIM_DBG_MSG("ADLP_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI: Couldn't configure registers.");
    }
    return bRet;
}

BOOLEAN ADLP_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                    bRet                = TRUE;
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 stPCHLiveReg = { 0 };
    DE_HPD_INTERRUPT_DEFINITION_D13        stDEHPDISR   = { 0 };

    TCSS_DDI_STATUS_D13 stTc1DdiStatus = { 0 };
    TCSS_DDI_STATUS_D13 stTc2DdiStatus = { 0 };
    TCSS_DDI_STATUS_D13 stTc3DdiStatus = { 0 };
    TCSS_DDI_STATUS_D13 stTc4DdiStatus = { 0 };

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDISR.Value     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_ISR_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stTc1DdiStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc2DdiStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc3DdiStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTc4DdiStatus.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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
            stTc1DdiStatus.Ready = bAttach;
            break;

        case INTDPG_PORT:
        case INTHDMIG_PORT:
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
            stTc2DdiStatus.Ready = bAttach;
            break;

        case INTDPH_PORT:
        case INTHDMIH_PORT:
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
            stTc3DdiStatus.Ready = bAttach;
            break;

        case INTDPI_PORT:
        case INTHDMII_PORT:
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
            stTc4DdiStatus.Ready = bAttach;
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
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_ISR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset])  = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_ISR_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDEHPDISR.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_1_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTc1DdiStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_2_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTc2DdiStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_3_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTc3DdiStatus.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TCSS_DDI_STATUS_4_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTc4DdiStatus.Value;
    }

    return bRet;
}

/*
This function will clear the HpdStatus value of a particular DDI
which Gfx Driver wants to.
*/
BOOLEAN ADLP_MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                    bRet                = FALSE;
    SHOTPLUG_CTL_DDI_GEN13     stSouthDDICtlReg    = { 0 };
    SHOTPLUG_CTL_TC_GEN13      stSouthTCCtlreg     = { 0 };
    HOTPLUG_CTL_D13            stNorthTCCtlreg     = { 0 };
    HOTPLUG_CTL_D13            stNorthTBTCtlreg    = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stSouthDDICtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthTCCtlreg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthTCCtlreg.Value    = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TC_HOTPLUG_CTL_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthTBTCtlreg.Value   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TBT_HOTPLUG_CTL_ADDR_D13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            if (stNorthTCCtlreg.Port1HpdEnable && PortConnectorInfo.IsTypeC)
            {
                GFXVALSIM_DBG_MSG("ADLP_MMIOHANDLERS_IsHPDEnabledForPort: stNorthTCCtlreg bit is set.");
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port1HpdEnable && PortConnectorInfo.IsTbt)
            {
                GFXVALSIM_DBG_MSG("ADLP_MMIOHANDLERS_IsHPDEnabledForPort: stNorthTBTCtlreg bit is set.");
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc1HpdEnable && (0 == PortConnectorInfo.IsTypeC && 0 == PortConnectorInfo.IsTbt))
            {
                GFXVALSIM_DBG_MSG("ADLP_MMIOHANDLERS_IsHPDEnabledForPort: TC1HpdEnable bit is set.");
                bRet = TRUE;
            }
            else
            {
                GFXVALSIM_DBG_MSG("ADLP_MMIOHANDLERS_IsHPDEnabledForPort: TC1HpdEnable bit is not set.");
            }
            break;

        case INTDPG_PORT:
        case INTHDMIG_PORT:
            if (stNorthTCCtlreg.Port2HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port2HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc2HpdEnable && (0 == PortConnectorInfo.IsTypeC && 0 == PortConnectorInfo.IsTbt))
            {
                bRet = TRUE;
            }
            break;

        case INTDPH_PORT:
        case INTHDMIH_PORT:
            if (stNorthTCCtlreg.Port3HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port3HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc3HpdEnable && (0 == PortConnectorInfo.IsTypeC && 0 == PortConnectorInfo.IsTbt))
            {
                bRet = TRUE;
            }
            break;

        case INTDPI_PORT:
        case INTHDMII_PORT:
            if (stNorthTCCtlreg.Port4HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port4HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCtlreg.Tc4HpdEnable && (0 == PortConnectorInfo.IsTypeC && 0 == PortConnectorInfo.IsTbt))
            {
                bRet = TRUE;
            }
            break;

        default:
            break;
        }

    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN13, stSouthDDICtlReg.ulValue, SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN13,
                        stSouthTCCtlreg.ulValue, TC_HOTPLUG_CTL_ADDR_D13, stNorthTCCtlreg.Value, TBT_HOTPLUG_CTL_ADDR_D13, stNorthTBTCtlreg.Value);
    return bRet;
}

BOOLEAN ADLP_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                                bRet             = TRUE;
    SHOTPLUG_CTL_DDI_GEN13                 stHotPlugDdiCtl  = { 0 };
    SHOTPLUG_CTL_TC_GEN13                  stHotPlugTcCtl   = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 stLiveStateReg   = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 stLiveStateRegHw = { 0 };
    ULONG                                  driverRegValue   = 0;

    stHotPlugDdiCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN13 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stHotPlugTcCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN13 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stLiveStateReg.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, SDE_ISR_ADDR_GEN13, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        stLiveStateRegHw.ulValue = driverRegValue;
        if (TRUE == stLiveStateRegHw.HotplugDdia)
        {
            stLiveStateReg.HotplugDdia = stLiveStateRegHw.HotplugDdia;
        }
    }

    if (stHotPlugDdiCtl.DdibHpdEnable == FALSE)
    {
        stLiveStateReg.HotplugDdib = FALSE;
    }

    if (stHotPlugTcCtl.Tc1HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort1 = FALSE;
    }

    if (stHotPlugTcCtl.Tc2HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort2 = FALSE;
    }

    if (stHotPlugTcCtl.Tc3HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort3 = FALSE;
    }

    if (stHotPlugTcCtl.Tc4HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort4 = FALSE;
    }

    *pulReadData = stLiveStateReg.ulValue;

    return bRet;
}

/*
This function will clear the HpdStatus value of a particular DDI
which Gfx Driver wants to.
*/
BOOLEAN ADLP_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    SHOTPLUG_CTL_DDI_GEN13 stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_DDI_GEN13 stHotPlugCtlTemp = { 0 };

    SHOTPLUG_CTL_TC_GEN13 stHotPlugCtl2     = { 0 };
    SHOTPLUG_CTL_TC_GEN13 stHotPlugCtlTemp2 = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN13 == ulMMIOOffset)
        {
            pstGlobalMMORegData      = &pstMMIOHandlerInfo->stGlobalMMORegData;
            stHotPlugCtlTemp.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

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
            stHotPlugCtlTemp2.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

            stHotPlugCtl2.ulValue = ulWriteData;

            stHotPlugCtl2.Tc1HpdStatus = stHotPlugCtlTemp2.Tc1HpdStatus;
            stHotPlugCtl2.Tc2HpdStatus = stHotPlugCtlTemp2.Tc2HpdStatus;
            stHotPlugCtl2.Tc3HpdStatus = stHotPlugCtlTemp2.Tc3HpdStatus;
            stHotPlugCtl2.Tc4HpdStatus = stHotPlugCtlTemp2.Tc4HpdStatus;

            stHotPlugCtlTemp2.ulValue = ulWriteData;

            stHotPlugCtl2.Tc1HpdStatus &= ~stHotPlugCtlTemp2.Tc1HpdStatus;
            stHotPlugCtl2.Tc2HpdStatus &= ~stHotPlugCtlTemp2.Tc2HpdStatus;
            stHotPlugCtl2.Tc3HpdStatus &= ~stHotPlugCtlTemp2.Tc3HpdStatus;
            stHotPlugCtl2.Tc4HpdStatus &= ~stHotPlugCtlTemp2.Tc4HpdStatus;

            *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl2.ulValue;
        }
        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN ADLP_MMIOHANDLERS_TBTHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
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
        stHotPlugCtl.Port2HpdStatus = stHotPlugCtlTemp.Port2HpdStatus;
        stHotPlugCtl.Port3HpdStatus = stHotPlugCtlTemp.Port3HpdStatus;
        stHotPlugCtl.Port4HpdStatus = stHotPlugCtlTemp.Port4HpdStatus;

        stHotPlugCtlTemp.Value = ulWriteData;

        stHotPlugCtl.Port1HpdStatus &= ~stHotPlugCtlTemp.Port1HpdStatus;
        stHotPlugCtl.Port2HpdStatus &= ~stHotPlugCtlTemp.Port2HpdStatus;
        stHotPlugCtl.Port3HpdStatus &= ~stHotPlugCtlTemp.Port3HpdStatus;
        stHotPlugCtl.Port4HpdStatus &= ~stHotPlugCtlTemp.Port4HpdStatus;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl.Value;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN ADLP_MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
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
        stHotPlugCtl.Port2HpdStatus = stHotPlugCtlTemp.Port2HpdStatus;
        stHotPlugCtl.Port3HpdStatus = stHotPlugCtlTemp.Port3HpdStatus;
        stHotPlugCtl.Port4HpdStatus = stHotPlugCtlTemp.Port4HpdStatus;

        stHotPlugCtlTemp.Value = ulWriteData;

        stHotPlugCtl.Port1HpdStatus &= ~stHotPlugCtlTemp.Port1HpdStatus;
        stHotPlugCtl.Port2HpdStatus &= ~stHotPlugCtlTemp.Port2HpdStatus;
        stHotPlugCtl.Port3HpdStatus &= ~stHotPlugCtlTemp.Port3HpdStatus;
        stHotPlugCtl.Port4HpdStatus &= ~stHotPlugCtlTemp.Port4HpdStatus;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = stHotPlugCtl.Value;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN ADLP_MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = TRUE;
    // TYPE_C
    HOTPLUG_CTL_D13                 stHotPlugCtl   = { 0 };
    DE_HPD_INTERRUPT_DEFINITION_D13 stLiveStateReg = { 0 };

    stHotPlugCtl.Value   = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[TC_HOTPLUG_CTL_ADDR_D13 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stLiveStateReg.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    //// TYPE_C
    if (stHotPlugCtl.Port1HpdEnable == FALSE)
    {
        stLiveStateReg.Tc1Hotplug = FALSE;
    }
    if (stHotPlugCtl.Port2HpdEnable == FALSE)
    {
        stLiveStateReg.Tc2Hotplug = FALSE;
    }
    if (stHotPlugCtl.Port3HpdEnable == FALSE)
    {
        stLiveStateReg.Tc3Hotplug = FALSE;
    }
    if (stHotPlugCtl.Port4HpdEnable == FALSE)
    {
        stLiveStateReg.Tc4Hotplug = FALSE;
    }

    *pulReadData = stLiveStateReg.Value;

    return bRet;
}

BOOLEAN ADLP_MMIOHANDLERS_DdiBufferControlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN            bRet            = TRUE;
    DDI_BUF_CTL_D13    stDdiBufCtlReg  = { 0 };
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

BOOLEAN ADLP_MMIOHANDLERS_PwrWellDDIControlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN              bRet               = TRUE;
    PWR_WELL_CTL_DDI_D13 stPwrWellDdiCtlReg = { 0 };

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

    *pulReadData = stPwrWellDdiCtlReg.Value;

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    return bRet;
}

BOOLEAN ADLP_MMIOHANDLERS_ScdcInterruptGeneration(PMMIO_INTERFACE pstMMIOInterface, PSCDC_ARGS pstScdcArgs)
{
    BOOLEAN                                bRet             = FALSE;
    GFX_MSTR_INTR_GEN13                    stMasterIntCtrl  = { 0 };
    DISPLAY_INT_CTL_GEN13                  stDisplayIntCtrl = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN13 stSouthDeInt     = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stMasterIntCtrl.Value    = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthDeInt.ulValue     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (pstScdcArgs->ulPortNum)
        {
        case INTHDMIA_PORT:
            stSouthDeInt.ScdcDdia = TRUE;
            bRet                  = TRUE;
            break;
        case INTHDMIB_PORT:
            stSouthDeInt.ScdcDdia = TRUE;
            bRet                  = TRUE;
            break;
        case INTHDMIC_PORT:
            stSouthDeInt.ScdcDdic = TRUE;
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
        stMasterIntCtrl.DisplayInterruptsPending = TRUE;

        stDisplayIntCtrl.DePchInterruptsPending = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SDE_IIR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthDeInt.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN13 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;
    }

    return bRet;
}

BOOLEAN ADLP_MMIOHANDLERS_Psr1MMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN     bRet        = TRUE;
    SRD_CTL_D13 stSrdCtlReg = { 0 };
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
        if (SRD_CTL_B_ADDR_D13 == ulMMIOOffset)
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

BOOLEAN ADLP_MMIOHANDLERS_Psr2MMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN      bRet         = TRUE;
    PSR2_CTL_D13 stPsr2CtlReg = { 0 };
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
        if (PSR2_CTL_B_ADDR_D13 == ulMMIOOffset)
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
