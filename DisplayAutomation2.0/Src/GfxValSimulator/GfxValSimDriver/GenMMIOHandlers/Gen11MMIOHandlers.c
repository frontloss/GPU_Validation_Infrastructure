/**********************************************************************************************************
ICL HPD Flow

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
1. GEN11INTRHANDLER_GetInterruptSource  ---> case GEN11_DISPLAY_INTERRUPT_BIT_POS --> LegacyInterruptsOccurred Flag should be set
2. GEN11INTRHANDLER_GetLegacyInterruptSource
3. GEN11INTRHANDLER_GetHPDInterruptSource

********************************************************************************************************/

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\DriverInterfaces\\SIMDRV_GFX_COMMON.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"
#include "..\\DriverInterfaces\\CommonRxHandlers.h"
#include "..\\DriverInterfaces\\DPHandlers.h"
#include "Gen11MMIO.h"
#include "Gen10MMIO.h"
#include "CommonMMIO.h"
#include "..\DriverInterfaces\SimDrvToGfx.h"
#include "..\\CommonInclude\\ETWLogging.h"

#define PORT_CONNECTOR_NORMAL 1
#define PORT_CONNECTOR_TYPEC 0
#define PORT_CONNECTOR_TBT 0

BOOLEAN GEN11MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN GEN11JSL_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface);

BOOLEAN GEN11MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN11MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN11MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN11JSL_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN11JSL_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo);

BOOLEAN GEN11MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_TBTHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_MgPhyLanesMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {

        bRet = GEN11MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11JSL_MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {

        bRet = GEN11JSL_MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    if (pstMMIOInterface)
    {

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_START] = DDI_AUX_DATA_A_START_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_END]   = DDI_AUX_DATA_A_END_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_A]        = DDI_AUX_CTL_A_ICL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_START] = DDI_AUX_DATA_B_START_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_END]   = DDI_AUX_DATA_B_END_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_B]        = DDI_AUX_CTL_B_ICL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = DDI_AUX_DATA_C_START_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = DDI_AUX_DATA_C_END_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = DDI_AUX_CTL_C_ICL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = DDI_AUX_DATA_D_START_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = DDI_AUX_DATA_D_END_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = DDI_AUX_CTL_D_ICL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_START] = DDI_AUX_DATA_E_START_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_END]   = DDI_AUX_DATA_E_END_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_E]        = DDI_AUX_CTL_E_ICL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_START] = DDI_AUX_DATA_F_START_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_END]   = DDI_AUX_DATA_F_END_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_F]        = DDI_AUX_CTL_F_ICL;

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

BOOLEAN GEN11JSL_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    if (pstMMIOInterface)
    {

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_START] = DDI_AUX_DATA_A_START_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_END]   = DDI_AUX_DATA_A_END_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_A]        = DDI_AUX_CTL_A_ICL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_START] = DDI_AUX_DATA_B_START_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_END]   = DDI_AUX_DATA_B_END_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_B]        = DDI_AUX_CTL_B_ICL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = DDI_AUX_DATA_C_START_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = DDI_AUX_DATA_C_END_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = DDI_AUX_CTL_C_ICL;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = DDI_AUX_DATA_D_START_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = DDI_AUX_DATA_D_END_ICL;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = DDI_AUX_CTL_D_ICL;

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

BOOLEAN GEN11MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
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

        // Master Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/20451
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_INTR_ADDR_ICL, GFX_MSTR_INTR_ADDR_ICL, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN11MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler, GEN11MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Display Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/20451
        bRet =
        COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DISPLAY_INTR_CTL_ADDR_ICL, DISPLAY_INTR_CTL_ADDR_ICL, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                GEN11MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler, GEN11MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/8409
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       SOUTH_DE_INTR_ADDR_SPT_ICL, // SOUTH_DE_ISR_ADDR_SPT,
                                                       SOUTH_DE_INTR_ADDR_SPT_ICL, // SOUTH_DE_ISR_ADDR_SPT,
                                                       0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       // GEN11MMIOHANDLERS_HotPlugIIRMMIOWriteHandler,
                                                       GEN11MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       SOUTH_DE_INTR_ADDR_SPT_ICL + 0x8, // SOUTH_DE_IIR_ADDR_SPT,
                                                       SOUTH_DE_INTR_ADDR_SPT_ICL + 0x8, // SOUTH_DE_IIR_ADDR_SPT,
                                                       0,                                // stLiveStateReg.ulValue,
                                                       NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       // GEN11MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler,
                                                       GEN11MMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21778
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21779
        // The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port
        // These two are the south hot plug control registers
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL, // SOUTH_HOT_PLUG_CTL_ADDR_SPT,
                                                       SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL, 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL, GEN11MMIOHANDLERS_HotPlugCtlMMIOWriteHandler,
                                                       NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, THUNDERBOLT_HOT_PLUG_CTL_ADDR_ICL, THUNDERBOLT_HOT_PLUG_CTL_ADDR_ICL, 0, NULL, NULL, 0, TRUE,
                                                       eNoExecHw, NULL,
                                                       // GEN11MMIOHANDLERS_HotPlugCtlMMIOWriteHandler,
                                                       GEN11MMIOHANDLERS_TBTHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet =
        COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, TYPE_C_HOT_PLUG_CTL_ADDR_ICL, TYPE_C_HOT_PLUG_CTL_ADDR_ICL, 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                // GEN11MMIOHANDLERS_HotPlugCtlMMIOWriteHandler,
                                                GEN11MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // DE Engine IIR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21261?dstFilter=ICLHP&mode=Filter
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       (DE_HPD_INTR_ADDR_ICL + 0x8), // DE IIR
                                                       (DE_HPD_INTR_ADDR_ICL + 0x8), 0, NULL, NULL, 0, TRUE, eReadCombine, NULL, GEN11MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler,
                                                       NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // DE Engine ISR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21261?dstFilter=ICLHP&mode=Filter
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       (DE_HPD_INTR_ADDR_ICL + 0x0), // ISR LiveState
                                                       (DE_HPD_INTR_ADDR_ICL + 0x0),
                                                       0, // stLiveStateReg.ulValue,
                                                       NULL, NULL, 0, FALSE, eNoExecHw, GEN11MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // MGPhyLanes Handlers
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_ADDR_ICL, PORT_TX_DFLEXDPPMS_ADDR_ICL, 0, NULL, NULL, 0, TRUE, eNoExecHw,
                                                       NULL, GEN11MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // To handle upfront link training
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_ADDR_ICL, PORT_TX_DFLEXDPSP4_ADDR_ICL, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN11MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Workaround to support TypeC ports. In the default mode for TC ports, IOM wouldn't have initialized PHY. So, the DDI Buffer is IDLE. As per the recommendation from
        // Ganesh/Raghu, it is being masked in valsim.
        for (int ddi_offset = DDI_BUF_CTL_C_ADDR_D11; ddi_offset <= DDI_BUF_CTL_F_ADDR_D11; ddi_offset += 256)
        {
            bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, ddi_offset, ddi_offset, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                           GEN11MMIOHANDLERS_DdiBufferControlMMIOReadHandler, NULL, NULL, NULL, NULL);

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
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PWR_WELL_CTL_DDI2_ADDR_D11, PWR_WELL_CTL_DDI2_ADDR_D11, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN11MMIOHANDLERS_PwrWellDDIControlMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11JSL_MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
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

        // Master Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/20451
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_INTR_ADDR_ICL, GFX_MSTR_INTR_ADDR_ICL, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN11MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler, GEN11MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Display Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/20451
        bRet =
        COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DISPLAY_INTR_CTL_ADDR_ICL, DISPLAY_INTR_CTL_ADDR_ICL, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                GEN11MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler, GEN11MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/8409
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       SOUTH_DE_INTR_ADDR_SPT_ICL, // SOUTH_DE_ISR_ADDR_SPT,
                                                       SOUTH_DE_INTR_ADDR_SPT_ICL, // SOUTH_DE_ISR_ADDR_SPT,
                                                       0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       // GEN11MMIOHANDLERS_HotPlugIIRMMIOWriteHandler,
                                                       GEN11JSL_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       SOUTH_DE_INTR_ADDR_SPT_ICL + 0x8, // SOUTH_DE_IIR_ADDR_SPT,
                                                       SOUTH_DE_INTR_ADDR_SPT_ICL + 0x8, // SOUTH_DE_IIR_ADDR_SPT,
                                                       0,                                // stLiveStateReg.ulValue,
                                                       NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       // GEN11MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler,
                                                       GEN11MMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21778
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21779
        // The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port
        // These two are the south hot plug control registers
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL, // SOUTH_HOT_PLUG_CTL_ADDR_SPT,
                                                       SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL, 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       GEN11JSL_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    GFX_MSTR_INTR_ICL stMasterIntCtrl = { 0 };
    stMasterIntCtrl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stMasterIntCtrl.MasterInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                   // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stMasterIntCtrl.Value;

    return TRUE;
}

BOOLEAN GEN11MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_ICL pstMasterIntCtrl =
    (PGFX_MSTR_INTR_ICL)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    GFX_MSTR_INTR_ICL stMasterIntCtrlTemp = { 0 };

    stMasterIntCtrlTemp.Value               = ulWriteData;
    pstMasterIntCtrl->MasterInterruptEnable = stMasterIntCtrlTemp.MasterInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN11MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    DISPLAY_INT_CTL_ICL stDisplayIntCtrl = { 0 };
    stDisplayIntCtrl.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stDisplayIntCtrl.DisplayInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                     // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stDisplayIntCtrl.ulValue;

    return TRUE;
}

BOOLEAN GEN11MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PDISPLAY_INT_CTL_ICL stDisplayIntCtrl =
    (PDISPLAY_INT_CTL_ICL)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    DISPLAY_INT_CTL_ICL stDisplayIntCtrlTemp = { 0 };

    stDisplayIntCtrlTemp.ulValue             = ulWriteData;
    stDisplayIntCtrl->DisplayInterruptEnable = stDisplayIntCtrlTemp.DisplayInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN11MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_ICL pstMasterIntCtrl =
    (PGFX_MSTR_INTR_ICL)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_ICL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL *pstPCHIIRReg    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL  stPCHIIRRegTemp = { 0 };
    pstPCHIIRReg =
    (SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.ulValue = ulWriteData;

    if (stPCHIIRRegTemp.ulValue != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        pstPCHIIRReg->ulValue &= ~stPCHIIRRegTemp.ulValue;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN11MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                              bRet             = TRUE;
    SHOTPLUG_CTL_DDI_ICL                 stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_TC_ICL                  stHotPlugCtl2    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stLiveStateReg   = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stLiveStateRegHw = { 0 };
    ULONG                                driverRegValue   = 0;

    stHotPlugCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stHotPlugCtl2.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stLiveStateReg.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, SOUTH_DE_INTR_ADDR_SPT_ICL, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
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

BOOLEAN GEN11JSL_MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                              bRet             = TRUE;
    SHOTPLUG_CTL_DDI_ICL                 stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_TC_ICL                  stHotPlugCtl2    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stLiveStateReg   = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stLiveStateRegHw = { 0 };
    ULONG                                driverRegValue   = 0;

    stHotPlugCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stHotPlugCtl2.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stLiveStateReg.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, SOUTH_DE_INTR_ADDR_SPT_ICL, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
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

    // JSL DDI-C Combo PHY port
    if (stHotPlugCtl2.Tc1HpdEnable == FALSE)
    {
        stLiveStateReg.HotplugTypecPort1 = FALSE;
    }

    *pulReadData = stLiveStateReg.ulValue;

    return bRet;
}

/*
This function will clear the HpdStatus value of a perticular DDI
which Gfx Driver wants to.
*/
BOOLEAN GEN11MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/21778
    SHOTPLUG_CTL_DDI_ICL *pstHotPlugCtl    = { 0 };
    SHOTPLUG_CTL_DDI_ICL  stHotPlugCtlTemp = { 0 };

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/21779
    SHOTPLUG_CTL_TC_ICL *pstHotPlugCtl2    = { 0 };
    SHOTPLUG_CTL_TC_ICL  stHotPlugCtlTemp2 = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL == ulMMIOOffset)
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

            pstHotPlugCtl = ((SHOTPLUG_CTL_DDI_ICL *)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

            pstHotPlugCtl->ulValue   = ulWriteData;
            stHotPlugCtlTemp.ulValue = ulWriteData;

            pstHotPlugCtl->DdiaHpdStatus &= ~stHotPlugCtlTemp.DdiaHpdStatus;
            pstHotPlugCtl->DdibHpdStatus &= ~stHotPlugCtlTemp.DdibHpdStatus;
        }
        else
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

            pstHotPlugCtl2 = ((SHOTPLUG_CTL_TC_ICL *)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

            pstHotPlugCtl2->ulValue   = ulWriteData;
            stHotPlugCtlTemp2.ulValue = ulWriteData;

            pstHotPlugCtl2->Tc1HpdStatus &= ~stHotPlugCtlTemp2.Tc1HpdStatus;
            pstHotPlugCtl2->Tc2HpdStatus &= ~stHotPlugCtlTemp2.Tc2HpdStatus;
            pstHotPlugCtl2->Tc3HpdStatus &= ~stHotPlugCtlTemp2.Tc3HpdStatus;
            pstHotPlugCtl2->Tc4HpdStatus &= ~stHotPlugCtlTemp2.Tc4HpdStatus;
            pstHotPlugCtl2->Tc5HpdStatus &= ~stHotPlugCtlTemp2.Tc5HpdStatus;
            pstHotPlugCtl2->Tc6HpdStatus &= ~stHotPlugCtlTemp2.Tc6HpdStatus;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11JSL_MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/21778
    SHOTPLUG_CTL_DDI_ICL *pstHotPlugCtl    = { 0 };
    SHOTPLUG_CTL_DDI_ICL  stHotPlugCtlTemp = { 0 };

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/21779
    PSHOTPLUG_CTL_TC_ICL pstHotPlugCtl2    = NULL;
    SHOTPLUG_CTL_TC_ICL  stHotPlugCtlTemp2 = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL == ulMMIOOffset)
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

            pstHotPlugCtl = ((SHOTPLUG_CTL_DDI_ICL *)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

            pstHotPlugCtl->ulValue   = ulWriteData;
            stHotPlugCtlTemp.ulValue = ulWriteData;

            pstHotPlugCtl->DdiaHpdStatus &= ~stHotPlugCtlTemp.DdiaHpdStatus;
            pstHotPlugCtl->DdibHpdStatus &= ~stHotPlugCtlTemp.DdibHpdStatus;
            pstHotPlugCtl->DdicHpdStatus &= ~stHotPlugCtlTemp.DdicHpdStatus;
        }
        else
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

            pstHotPlugCtl2 = ((SHOTPLUG_CTL_TC_ICL *)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

            pstHotPlugCtl2->ulValue   = ulWriteData;
            stHotPlugCtlTemp2.ulValue = ulWriteData;

            pstHotPlugCtl2->Tc1HpdStatus &= ~stHotPlugCtlTemp2.Tc1HpdStatus;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                    bRet                = FALSE;
    SHOTPLUG_CTL_DDI_ICL       stSouthDDICtlReg    = { 0 };
    SHOTPLUG_CTL_TC_ICL        stSouthTCCTLreg     = { 0 };
    HOTPLUG_CTL_ICL            stNorthTCCtlreg     = { 0 };
    HOTPLUG_CTL_ICL            stNorthTBTCtlreg    = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stSouthDDICtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthTCCTLreg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthTCCtlreg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthTBTCtlreg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
            bRet = (BOOLEAN)stSouthDDICtlReg.DdiaHpdEnable;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            bRet = (BOOLEAN)stSouthDDICtlReg.DdibHpdEnable;
            break;

        // IMP NOTE: For PORTS C,D,E and F

        // The sequence of checking North DE Register first
        // followed by SOUTH DE register has to be maintianed
        // bec Gfx driver always sets the SOUTH DE registers first
        // and then NORTH DE register as per the bspec.
        // For Ex: for DP_C with TYPE_C enabled port,
        // stNorthTCCtlreg.Port1HpdEnable and stSouthTCCTLreg.Tc1HpdEnable
        // both will be set. But for TYPE_C enabled port, HPD has to be
        // triggered on NORTH DE. Hence stNorthTCCtlreg.Port1HpdEnable is the valid one.
        // Suppose if we reverse the order of checking these registers, then for DP_C with TYPE_C enabled port
        // HPD will be triggered in SOUTH DE as stSouthTCCTLreg.Tc1HpdEnable will also be set.
        // But for DP_C (Legacy) enabled port, only stSouthTCCTLreg.Tc1HpdEnable will be set
        // and HPD will be triggered in SOUTH DE if we follow this sequence.
        case INTDPC_PORT:
        case INTHDMIC_PORT:
            if (stNorthTCCtlreg.Port1HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port1HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCTLreg.Tc1HpdEnable && PortConnectorInfo.IsTypeC == FALSE && PortConnectorInfo.IsTbt == FALSE)
            {
                bRet = TRUE;
            }

            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            if (stNorthTCCtlreg.Port2HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port2HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCTLreg.Tc2HpdEnable && PortConnectorInfo.IsTypeC == FALSE && PortConnectorInfo.IsTbt == FALSE)
            {
                bRet = TRUE;
            }

            break;

        case INTDPE_PORT:
        case INTHDMIE_PORT:
            if (stNorthTCCtlreg.Port3HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port3HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCTLreg.Tc3HpdEnable && PortConnectorInfo.IsTypeC == FALSE && PortConnectorInfo.IsTbt == FALSE)
            {
                bRet = TRUE;
            }

            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            if (stNorthTCCtlreg.Port4HpdEnable && PortConnectorInfo.IsTypeC)
            {
                bRet = TRUE;
            }
            else if (stNorthTBTCtlreg.Port4HpdEnable && PortConnectorInfo.IsTbt)
            {
                bRet = TRUE;
            }
            else if (stSouthTCCTLreg.Tc4HpdEnable && PortConnectorInfo.IsTypeC == FALSE && PortConnectorInfo.IsTbt == FALSE)
            {
                bRet = TRUE;
            }

            break;

        default:
            break;
        }

    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL, stSouthDDICtlReg.ulValue, SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL,
                        stSouthTCCTLreg.ulValue, TYPE_C_HOT_PLUG_CTL_ADDR_ICL, stNorthTCCtlreg.ulValue, THUNDERBOLT_HOT_PLUG_CTL_ADDR_ICL, stNorthTBTCtlreg.ulValue);
    return bRet;
}

BOOLEAN GEN11JSL_MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                    bRet                = FALSE;
    SHOTPLUG_CTL_DDI_ICL       stSouthDDICtlReg    = { 0 };
    SHOTPLUG_CTL_TC_ICL        stSouthTCCTLreg     = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stSouthDDICtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthTCCTLreg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
        // DDI-D muxing via combo PHY A. Need to use HPD on port A
        case INTDPD_PORT:
        case INTHDMID_PORT:
            bRet = (BOOLEAN)stSouthDDICtlReg.DdiaHpdEnable;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            bRet = (BOOLEAN)stSouthDDICtlReg.DdibHpdEnable;
            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:
            if (pstMMIOInterface->ePCHProductFamily == PCH_JSP_N) // JSL N PCH Device IDs for JSL+ Rev02
            {
                bRet = (BOOLEAN)stSouthDDICtlReg.DdicHpdEnable;
            }
            else
            {
                bRet = (BOOLEAN)stSouthTCCTLreg.Tc1HpdEnable;
            }
            break;

        default:
            break;
        }
    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL, stSouthDDICtlReg.ulValue, SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL,
                        stSouthTCCTLreg.ulValue, 0, 0, 0, 0);
    return bRet;
}

// bIsHPD == FALSE ==> SPI
BOOLEAN GEN11MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                             PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN             bRet             = FALSE;
    GFX_MSTR_INTR_ICL   stMasterIntCtrl  = { 0 };
    DISPLAY_INT_CTL_ICL stDisplayIntCtrl = { 0 };

    SHOTPLUG_CTL_DDI_ICL stSouthCtlReg = { 0 };
    SHOTPLUG_CTL_TC_ICL  stTCCTLreg    = { 0 };

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stPCHLiveReg = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stPCHIMRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stPCHIIRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stPCHIERReg  = { 0 };

    HOTPLUG_CTL_ICL stTBTHotPlugCtl   = { 0 };
    HOTPLUG_CTL_ICL stTYPECHotPlugCtl = { 0 };

    DE_HPD_INTR_DEFINITION_ICL stDEHPDISR = { 0 };
    DE_HPD_INTR_DEFINITION_ICL stDEHPDIMR = { 0 };
    DE_HPD_INTR_DEFINITION_ICL stDEHPDIIR = { 0 };
    DE_HPD_INTR_DEFINITION_ICL stDEHPDIER = { 0 };

    PORT_TX_DFLEXDPPMS_ICL stTypeCFiaStatus = { 0 };

    PORT_TX_DFLEXDPSP_ICL stFIALiveState = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Check if HPD has been enabled by Gfx
        if (FALSE == GEN11MMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType, PortConnectorInfo))
        {
            break;
        }

        stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Bspec Ref; https://gfxspecs.intel.com/Predator/Home/Index/21778
        stSouthCtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21779
        stTCCTLreg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Legacy
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/8409
        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_ICL)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_ICL + 0x4) - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_ICL + 0x8) - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_ICL + 0xC) - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // TypeC or TBT
        stTBTHotPlugCtl.ulValue   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTYPECHotPlugCtl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // TypeC or TBT
        stDEHPDISR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_INTR_ADDR_ICL)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIMR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_INTR_ADDR_ICL + 0x4) - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIIR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_INTR_ADDR_ICL + 0x8) - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIER.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_INTR_ADDR_ICL + 0xC) - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stTypeCFiaStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stFIALiveState.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // IMP NOTE: For PORTS C,D,E and F

        // The sequence of checking North DE Register first
        // followed by SOUTH DE register has to be maintianed
        // bec Gfx driver always sets the SOUTH DE registers first
        // and then NORTH DE register as per the bspec.
        // For Ex: for DP_C with TYPE_C enabled port,
        // stNorthTCCtlreg.Port1HpdEnable and stSouthTCCTLreg.Tc1HpdEnable
        // both will be set. But for TYPE_C enabled port, HPD has to be
        // triggered on NORTH DE. Hence stNorthTCCtlreg.Port1HpdEnable is the valid one.
        // Suppose if we reverse the order of checking these registers, then for DP_C with TYPE_C enabled port
        // HPD will be triggered in SOUTH DE as stSouthTCCTLreg.Tc1HpdEnable will also be set.
        // But for DP_C (Legacy) enabled port, only stSouthTCCTLreg.Tc1HpdEnable will be set
        // and HPD will be triggered in SOUTH DE if we follow this sequence.

        switch (ePortType)
        {
        case INTDPA_PORT:

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

            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port1HpdEnable && stDEHPDIMR.Tc1Hotplug == FALSE && stDEHPDIER.Tc1Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc1Hotplug                                       = TRUE;
                    stDEHPDISR.Tc1Hotplug                                       = bAttach; // LiveState Register
                    stFIALiveState.Tc0LiveState                                 = bAttach; // LiveState Register
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTYPECHotPlugCtl.Port1HpdStatus                            = 2;
                    bRet                                                        = TRUE;
                }
                else if (stDEHPDISR.Tc1Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc1Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port1HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }

            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port1HpdEnable && stDEHPDIMR.Tbt1Hotplug == FALSE && stDEHPDIER.Tbt1Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt1Hotplug                                      = TRUE;
                    stDEHPDISR.Tbt1Hotplug                                      = bAttach; // LiveState Register
                    stFIALiveState.Tbt0LiveState                                = bAttach; // LiveState Register
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTBTHotPlugCtl.Port1HpdStatus                              = 2;
                    bRet                                                        = TRUE;
                }
                else if (stDEHPDISR.Tbt1Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt1Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port1HpdStatus = 0x1;
                    bRet                           = TRUE;
                }
            }

            // Legacy South Bridge
            else if (stTCCTLreg.Tc1HpdEnable && stPCHIMRReg.HotplugTypecPort1 == FALSE && stPCHIERReg.HotplugTypecPort1)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort1                               = TRUE;
                    stPCHLiveReg.HotplugTypecPort1                              = bAttach;
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
                    stTCCTLreg.Tc1HpdStatus                                     = 2;
                    bRet                                                        = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort1) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort1 = TRUE;
                    stTCCTLreg.Tc1HpdStatus       = 0x1;
                    bRet                          = TRUE;
                }
            }

            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:

            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port2HpdEnable && stDEHPDIMR.Tc2Hotplug == FALSE && stDEHPDIER.Tc2Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc2Hotplug                                       = TRUE;
                    stDEHPDISR.Tc2Hotplug                                       = bAttach; // LiveState Register
                    stFIALiveState.Tc1LiveState                                 = bAttach; // LiveState Register
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTYPECHotPlugCtl.Port2HpdStatus                            = 2;
                    bRet                                                        = TRUE;
                }
                else if (stDEHPDISR.Tc2Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc2Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port2HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }

            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port2HpdEnable && stDEHPDIMR.Tbt2Hotplug == FALSE && stDEHPDIER.Tbt2Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt2Hotplug                                      = TRUE;
                    stDEHPDISR.Tbt2Hotplug                                      = bAttach; // LiveState Register
                    stFIALiveState.Tbt1LiveState                                = bAttach; // LiveState Register
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTBTHotPlugCtl.Port2HpdStatus                              = 2;
                    bRet                                                        = TRUE;
                }
                else if (stDEHPDISR.Tbt2Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt2Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port2HpdStatus = 0x1;
                    bRet                           = TRUE;
                }
            }

            // Legacy South Bridge
            else if (stTCCTLreg.Tc2HpdEnable && stPCHIMRReg.HotplugTypecPort2 == FALSE && stPCHIERReg.HotplugTypecPort2)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort2                               = TRUE;
                    stPCHLiveReg.HotplugTypecPort2                              = bAttach;
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
                    stTCCTLreg.Tc2HpdStatus                                     = 2;
                    bRet                                                        = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort2) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort2 = TRUE;
                    stTCCTLreg.Tc2HpdStatus       = 0x1;
                    bRet                          = TRUE;
                }
            }

            break;

        case INTDPE_PORT:
        case INTHDMIE_PORT:

            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port3HpdEnable && stDEHPDIMR.Tc3Hotplug == FALSE && stDEHPDIER.Tc3Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc3Hotplug                                       = TRUE;
                    stDEHPDISR.Tc3Hotplug                                       = bAttach; // LiveState Register
                    stFIALiveState.Tc2LiveState                                 = bAttach; // LiveState Register
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector2 = bAttach;
                    stTYPECHotPlugCtl.Port3HpdStatus                            = 2;
                    bRet                                                        = TRUE;
                }
                else if (stDEHPDISR.Tc3Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc3Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port3HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }

            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port3HpdEnable && stDEHPDIMR.Tbt3Hotplug == FALSE && stDEHPDIER.Tbt3Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt3Hotplug                                      = TRUE;
                    stDEHPDISR.Tbt3Hotplug                                      = bAttach; // LiveState Register
                    stFIALiveState.Tbt2LiveState                                = bAttach; // LiveState Register
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector2 = bAttach;
                    stTBTHotPlugCtl.Port3HpdStatus                              = 2;
                    bRet                                                        = TRUE;
                }
                else if (stDEHPDISR.Tbt3Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt3Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port3HpdStatus = 0x1;
                    bRet                           = TRUE;
                }
            }
            // Legacy South Bridge
            else if (stTCCTLreg.Tc3HpdEnable && stPCHIMRReg.HotplugTypecPort3 == FALSE && stPCHIERReg.HotplugTypecPort3)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort3                               = TRUE;
                    stPCHLiveReg.HotplugTypecPort3                              = bAttach;
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector2 = bAttach;
                    stTCCTLreg.Tc3HpdStatus                                     = 2;
                    bRet                                                        = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort3) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort3 = TRUE;
                    stTCCTLreg.Tc3HpdStatus       = 0x1;
                    bRet                          = TRUE;
                }
            }

            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:

            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port4HpdEnable && stDEHPDIMR.Tc4Hotplug == FALSE && stDEHPDIER.Tc4Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc4Hotplug                                       = TRUE;
                    stDEHPDISR.Tc4Hotplug                                       = bAttach; // LiveState Register
                    stFIALiveState.Tc3LiveState                                 = bAttach; // LiveState Register
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector3 = bAttach;
                    stTYPECHotPlugCtl.Port4HpdStatus                            = 2;
                    bRet                                                        = TRUE;
                }
                else if (stDEHPDISR.Tc4Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tc4Hotplug            = TRUE;
                    stTYPECHotPlugCtl.Port4HpdStatus = 0x1;
                    bRet                             = TRUE;
                }
            }

            // TBT North Bridge
            else if (stTBTHotPlugCtl.Port4HpdEnable && stDEHPDIMR.Tbt4Hotplug == FALSE && stDEHPDIER.Tbt4Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt4Hotplug                                      = TRUE;
                    stDEHPDISR.Tbt4Hotplug                                      = bAttach; // LiveState Register
                    stFIALiveState.Tbt3LiveState                                = bAttach; // LiveState Register
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector3 = bAttach;
                    stTBTHotPlugCtl.Port4HpdStatus                              = 2;
                    bRet                                                        = TRUE;
                }
                else if (stDEHPDISR.Tbt4Hotplug) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stDEHPDIIR.Tbt4Hotplug         = TRUE;
                    stTBTHotPlugCtl.Port4HpdStatus = 0x1;
                    bRet                           = TRUE;
                }
            }
            // Legacy South Bridge
            else if (stTCCTLreg.Tc4HpdEnable && stPCHIMRReg.HotplugTypecPort4 == FALSE && stPCHIERReg.HotplugTypecPort4)
            {
                if (bIsHPD)
                {
                    stPCHIIRReg.HotplugTypecPort4                               = TRUE;
                    stPCHLiveReg.HotplugTypecPort4                              = bAttach;
                    stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector3 = bAttach;
                    stTCCTLreg.Tc4HpdStatus                                     = 2;
                    bRet                                                        = TRUE;
                }
                else if (stPCHLiveReg.HotplugTypecPort4) // Live state should already be up i.e display to be connected for SPI to make sense
                {
                    stPCHIIRReg.HotplugTypecPort4 = TRUE;
                    stTCCTLreg.Tc4HpdStatus       = 0x1;
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
        // Below line is a temp workaround
        stPCHLiveReg.HotplugDdia                 = TRUE;
        stMasterIntCtrl.DisplayInterruptsPending = TRUE;
        stDisplayIntCtrl.DeHpdInterruptsPending  = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset])   = stSouthCtlReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTCCTLreg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_INTR_ADDR_SPT_ICL - pstGlobalMMORegData->ulMMIOBaseOffset])            = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_ICL + 0x8) - pstGlobalMMORegData->ulMMIOBaseOffset])    = stPCHIIRReg.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFiaStatus.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPSP1_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stFIALiveState.ulValue;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTBTHotPlugCtl.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset])      = stTYPECHotPlugCtl.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_INTR_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset])              = stDEHPDISR.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_INTR_ADDR_ICL + 0x8) - pstGlobalMMORegData->ulMMIOBaseOffset])      = stDEHPDIIR.ulValue;
    }

    return bRet;
}

BOOLEAN GEN11JSL_MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                                 PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN             bRet             = FALSE;
    GFX_MSTR_INTR_ICL   stMasterIntCtrl  = { 0 };
    DISPLAY_INT_CTL_ICL stDisplayIntCtrl = { 0 };

    SHOTPLUG_CTL_DDI_ICL stSouthCtlReg   = { 0 };
    SHOTPLUG_CTL_TC_ICL  stSouthTCCTLreg = { 0 };

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stPCHLiveReg = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stPCHIMRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stPCHIIRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stPCHIERReg  = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Check if HPD has been enabled by Gfx
        if (FALSE == GEN11JSL_MMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType, PortConnectorInfo))
        {
            break;
        }

        stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Bspec Ref; https://gfxspecs.intel.com/Predator/Home/Index/21778
        stSouthCtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21779
        stSouthTCCTLreg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Legacy
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/8409
        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_ICL)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_ICL + 0x4) - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_ICL + 0x8) - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_ICL + 0xC) - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
        // JasperLake DDI-D muxing
        case INTDPD_PORT:
        case INTHDMID_PORT:

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

            if (pstMMIOInterface->ePCHProductFamily == PCH_JSP_N) // JSL N PCH Device IDs for JSL+ Rev02
            {
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
            }
            else
            {
                // Legacy South Bridge with TC port
                if (stSouthTCCTLreg.Tc1HpdEnable && stPCHIMRReg.HotplugTypecPort1 == FALSE && stPCHIERReg.HotplugTypecPort1)
                {
                    if (bIsHPD)
                    {
                        stPCHIIRReg.HotplugTypecPort1  = TRUE;
                        stPCHLiveReg.HotplugTypecPort1 = bAttach;
                        stSouthTCCTLreg.Tc1HpdStatus   = 2;
                        bRet                           = TRUE;
                    }
                    else if (stPCHLiveReg.HotplugTypecPort1) // Live state should already be up i.e display to be connected for SPI to make sense
                    {
                        stPCHIIRReg.HotplugTypecPort1 = TRUE;
                        stSouthTCCTLreg.Tc1HpdStatus  = 0x1;
                        bRet                          = TRUE;
                    }
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
        stPCHLiveReg.HotplugDdia                 = TRUE;
        stMasterIntCtrl.DisplayInterruptsPending = TRUE;
        stDisplayIntCtrl.DeHpdInterruptsPending  = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset])   = stSouthCtlReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stSouthTCCTLreg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_INTR_ADDR_SPT_ICL - pstGlobalMMORegData->ulMMIOBaseOffset])            = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_ICL + 0x8) - pstGlobalMMORegData->ulMMIOBaseOffset])    = stPCHIIRReg.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;
    }

    return bRet;
}

// TODO: Need to take care of TBT/TypeC
BOOLEAN GEN11MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                              bRet                = TRUE;
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stPCHLiveReg        = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA           pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;
    DE_HPD_INTR_DEFINITION_ICL           stDEHPDISR          = { 0 };

    // MG PHY Lines Enabling for Port C- Port F
    PORT_TX_DFLEXDPPMS_ICL stTypeCFiaStatus = { 0 };

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stPCHLiveReg.ulValue     = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_INTR_ADDR_SPT_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDISR.ulValue       = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_INTR_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFiaStatus.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
            stPCHLiveReg.HotplugDdia = bAttach;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            stPCHLiveReg.HotplugDdib = bAttach;
            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc1Hotplug = bAttach; // LiveState Register
            }
            else if (PortConnectorInfo.IsTbt)
            {
                stDEHPDISR.Tbt1Hotplug = bAttach; // LiveState Register
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort1 = bAttach;
            }
            stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector0 = bAttach;
            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc2Hotplug = bAttach; // LiveState Register
            }
            else if (PortConnectorInfo.IsTbt)
            {
                stDEHPDISR.Tbt2Hotplug = bAttach; // LiveState Register
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort2 = bAttach;
            }
            stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector1 = bAttach;
            break;

        case INTDPE_PORT:
        case INTHDMIE_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc3Hotplug = bAttach; // LiveState Register
            }
            else if (PortConnectorInfo.IsTbt)
            {
                stDEHPDISR.Tbt3Hotplug = bAttach; // LiveState Register
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort3 = bAttach;
            }
            stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector2 = bAttach;

            break;

        case INTDPF_PORT:
        case INTHDMIF_PORT:
            if (PortConnectorInfo.IsTypeC)
            {
                stDEHPDISR.Tc4Hotplug = bAttach; // LiveState Register
            }
            else if (PortConnectorInfo.IsTbt)
            {
                stDEHPDISR.Tbt4Hotplug = bAttach; // LiveState Register
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort4 = bAttach;
            }
            stTypeCFiaStatus.DisplayPortPhyModeStatusForTypeCConnector3 = bAttach;

            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        // Below line is a temp workaround
        stPCHLiveReg.HotplugDdia                                                                                                 = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_INTR_ADDR_SPT_ICL - pstGlobalMMORegData->ulMMIOBaseOffset])  = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_INTR_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset])        = stDEHPDISR.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFiaStatus.ulValue;
    }

    return bRet;
}

BOOLEAN GEN11JSL_MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                              bRet                = TRUE;
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_ICL stPCHLiveReg        = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA           pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_INTR_ADDR_SPT_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case INTDPA_PORT:
        // JSL DDI-D muxing
        case INTDPD_PORT:
        case INTHDMID_PORT:
            stPCHLiveReg.HotplugDdia = bAttach;
            break;

        case INTDPB_PORT:
        case INTHDMIB_PORT:
            stPCHLiveReg.HotplugDdib = bAttach;
            break;

        case INTDPC_PORT:
        case INTHDMIC_PORT:
            if (pstMMIOInterface->ePCHProductFamily == PCH_JSP_N) // JSL N PCH Device IDs for JSL+ Rev02
            {
                stPCHLiveReg.HotplugDdic = bAttach;
            }
            else
            {
                stPCHLiveReg.HotplugTypecPort1 = bAttach;
            }
            break;

        default:
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    if (bRet)
    {
        // Below line is a temp workaround
        stPCHLiveReg.HotplugDdia                                                                                                = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_INTR_ADDR_SPT_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = stPCHLiveReg.ulValue;
    }

    return bRet;
}

BOOLEAN GEN11MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = TRUE;
    // THUNDERBOLT
    HOTPLUG_CTL_ICL stHotPlugCtl = { 0 };
    // TYPE_C
    HOTPLUG_CTL_ICL            stHotPlugCtl2  = { 0 };
    DE_HPD_INTR_DEFINITION_ICL stLiveStateReg = { 0 };

    stHotPlugCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_ICL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stHotPlugCtl2.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_ICL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

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

BOOLEAN GEN11MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_ICL pstMasterIntCtrl =
    (PGFX_MSTR_INTR_ICL)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_ICL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    DE_HPD_INTR_DEFINITION_ICL *pstPCHIIRReg    = { 0 }; // DE Interrupt IIR
    DE_HPD_INTR_DEFINITION_ICL  stPCHIIRRegTemp = { 0 }; // DE Interrupt IIR
    pstPCHIIRReg = (DE_HPD_INTR_DEFINITION_ICL *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.ulValue = ulWriteData;

    if (stPCHIIRRegTemp.ulValue != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        pstPCHIIRReg->ulValue &= ~stPCHIIRRegTemp.ulValue;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN11MMIOHANDLERS_TBTHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    HOTPLUG_CTL_ICL *pstHotPlugCtl    = { 0 };
    HOTPLUG_CTL_ICL  stHotPlugCtlTemp = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (THUNDERBOLT_HOT_PLUG_CTL_ADDR_ICL == ulMMIOOffset)
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
            pstHotPlugCtl       = ((HOTPLUG_CTL_ICL *)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

            pstHotPlugCtl->ulValue   = ulWriteData;
            stHotPlugCtlTemp.ulValue = ulWriteData;

            pstHotPlugCtl->Port1HpdStatus &= ~stHotPlugCtlTemp.Port1HpdStatus;
            pstHotPlugCtl->Port2HpdStatus &= ~stHotPlugCtlTemp.Port2HpdStatus;
            pstHotPlugCtl->Port3HpdStatus &= ~stHotPlugCtlTemp.Port3HpdStatus;
            pstHotPlugCtl->Port4HpdStatus &= ~stHotPlugCtlTemp.Port4HpdStatus;

            pstHotPlugCtl->Port5HpdStatus &= ~stHotPlugCtlTemp.Port5HpdStatus;
            pstHotPlugCtl->Port6HpdStatus &= ~stHotPlugCtlTemp.Port6HpdStatus;
            pstHotPlugCtl->Port7HpdStatus &= ~stHotPlugCtlTemp.Port7HpdStatus;
            pstHotPlugCtl->Port8HpdStatus &= ~stHotPlugCtlTemp.Port8HpdStatus;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    HOTPLUG_CTL_ICL *pstHotPlugCtl    = { 0 };
    HOTPLUG_CTL_ICL  stHotPlugCtlTemp = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (TYPE_C_HOT_PLUG_CTL_ADDR_ICL == ulMMIOOffset)
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
            pstHotPlugCtl       = ((HOTPLUG_CTL_ICL *)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]);

            pstHotPlugCtl->ulValue   = ulWriteData;
            stHotPlugCtlTemp.ulValue = ulWriteData;

            pstHotPlugCtl->Port1HpdStatus &= ~stHotPlugCtlTemp.Port1HpdStatus;
            pstHotPlugCtl->Port2HpdStatus &= ~stHotPlugCtlTemp.Port2HpdStatus;
            pstHotPlugCtl->Port3HpdStatus &= ~stHotPlugCtlTemp.Port3HpdStatus;
            pstHotPlugCtl->Port4HpdStatus &= ~stHotPlugCtlTemp.Port4HpdStatus;

            pstHotPlugCtl->Port5HpdStatus &= ~stHotPlugCtlTemp.Port5HpdStatus;
            pstHotPlugCtl->Port6HpdStatus &= ~stHotPlugCtlTemp.Port6HpdStatus;
            pstHotPlugCtl->Port7HpdStatus &= ~stHotPlugCtlTemp.Port7HpdStatus;
            pstHotPlugCtl->Port8HpdStatus &= ~stHotPlugCtlTemp.Port8HpdStatus;
        }

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

// This function needs to be revisited once Gfx Drive code for TYPEC/TBT code is fianlised
// This may or may not be needed
BOOLEAN GEN11MMIOHANDLERS_MgPhyLanesMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    PORT_TX_DFLEXDPPMS_ICL     TypeCFiaStatus      = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
        TypeCFiaStatus.ulValue =
        *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_ADDR_ICL - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

        TypeCFiaStatus.ulValue = ulWriteData;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_ADDR_ICL - pstGlobalMMORegData->ulMMIOBaseOffset]) = TypeCFiaStatus.ulValue;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

/**-------------------------------------------------------------
 * @brief GEN11MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler
 *
 * Description: Set the number of lanes assigned to display for Read MG Phy scratch register (DFLEXDPSP1)
 *       This call is valid only for MG Phy ports (DDI C/D/E/F) and Type-C connector
 *
 * TBD: This is a replacement for upfront link training to determine # lanes used in Type-C.
 *       Need to pass this info. up to Protocol.
 *-------------------------------------------------------------*/
BOOLEAN GEN11MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    PORT_TX_DFLEXDPSP_ICL LaneData = {
        0,
    };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

        LaneData.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Currently 4 lanes are assigned for all the Port Types
        // TODO:
        // 1) Based on Live State of a Port, Lane Values can be assigned to a particualr port
        // 2) Lane Values can be configured run time also.Run time configuration can be done through registry write/read
        // These two items will be taken up later after discussing with VCO
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector0 = PHY_TX3_TX2_TX1_TX0;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector1 = PHY_TX3_TX2_TX1_TX0;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector2 = PHY_TX3_TX2_TX1_TX0;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector3 = PHY_TX3_TX2_TX1_TX0;

        *pulReadData = LaneData.ulValue;

        // The value of ulMMIOOffset will be either
        // PORT_TX_DFLEXDPSP1_ADDR_ICL = 0X1638A0
        // PORT_TX_DFLEXDPSP2_ADDR_ICL = 0X1638A4
        // PORT_TX_DFLEXDPSP3_ADDR_ICL = 0X1638A8
        // PORT_TX_DFLEXDPSP4_ADDR_ICL = 0X1638AC
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = LaneData.ulValue;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11MMIOHANDLERS_DdiBufferControlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN            bRet            = TRUE;
    DDI_BUF_CTL_D11    stDdiBufCtlReg  = { 0 };
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

BOOLEAN GEN11MMIOHANDLERS_PwrWellDDIControlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN              bRet               = TRUE;
    PWR_WELL_CTL_DDI_D11 stPwrWellDdiCtlReg = { 0 };

    stPwrWellDdiCtlReg.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (stPwrWellDdiCtlReg.DdiCIoPowerRequest == TRUE)
    {
        stPwrWellDdiCtlReg.DdiCIoPowerState = TRUE;
    }

    if (stPwrWellDdiCtlReg.DdiDIoPowerRequest == TRUE)
    {
        stPwrWellDdiCtlReg.DdiDIoPowerState = TRUE;
    }

    if (stPwrWellDdiCtlReg.DdiEIoPowerRequest == TRUE)
    {
        stPwrWellDdiCtlReg.DdiEIoPowerState = TRUE;
    }

    if (stPwrWellDdiCtlReg.DdiFIoPowerRequest == TRUE)
    {
        stPwrWellDdiCtlReg.DdiFIoPowerState = TRUE;
    }

    *pulReadData = stPwrWellDdiCtlReg.Value;

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    return bRet;
}
