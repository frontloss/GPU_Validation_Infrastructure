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
#include "Gen11p5MMIO.h"
#include "Gen10MMIO.h"
#include "CommonMMIO.h"
#include "..\DriverInterfaces\SimDrvToGfx.h"
#include "..\\CommonInclude\\ETWLogging.h"

#define PORT_CONNECTOR_NORMAL 1
#define PORT_CONNECTOR_TYPEC 0
#define PORT_CONNECTOR_TBT 0

BOOLEAN GEN11P5MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface);

BOOLEAN GEN11P5MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN11P5MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);
BOOLEAN GEN11P5MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo);

BOOLEAN GEN11P5MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_TBTHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                     PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_DEPortIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_DSIInterIdentMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite);

BOOLEAN GEN11P5MMIOHANDLERS_RegisterGeneralMMIOHandHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;

    do
    {

        bRet = GEN11P5MMIOHANDLERS_RegisterHotPlugHandlers(pstMMIOInterface);

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11P5MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    if (pstMMIOInterface)
    {

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_START] = DDI_AUX_DATA_A_START_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_END]   = DDI_AUX_DATA_A_END_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_A]        = DDI_AUX_CTL_A_GEN11P5;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_START] = DDI_AUX_DATA_B_START_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_END]   = DDI_AUX_DATA_B_END_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_B]        = DDI_AUX_CTL_B_GEN11P5;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = DDI_AUX_DATA_C_START_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = DDI_AUX_DATA_C_END_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = DDI_AUX_CTL_C_GEN11P5;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = DDI_AUX_DATA_D_START_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = DDI_AUX_DATA_D_END_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = DDI_AUX_CTL_D_GEN11P5;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_START] = DDI_AUX_DATA_E_START_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_END]   = DDI_AUX_DATA_E_END_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_E]        = DDI_AUX_CTL_E_GEN11P5;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_START] = DDI_AUX_DATA_F_START_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_END]   = DDI_AUX_DATA_F_END_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_F]        = DDI_AUX_CTL_F_GEN11P5;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_G_START] = DDI_AUX_DATA_G_START_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_G_END]   = DDI_AUX_DATA_G_END_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_G]        = DDI_AUX_CTL_G_GEN11P5;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_H_START] = DDI_AUX_DATA_H_START_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_H_END]   = DDI_AUX_DATA_H_END_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_H]        = DDI_AUX_CTL_H_GEN11P5;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_I_START] = DDI_AUX_DATA_I_START_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_I_END]   = DDI_AUX_DATA_I_END_GEN11P5;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_I]        = DDI_AUX_CTL_I_GEN11P5;

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

BOOLEAN GEN11P5MMIOHANDLERS_RegisterHotPlugHandlers(PMMIO_INTERFACE pstMMIOInterface)
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
        bRet =
        COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, GFX_MSTR_INTR_ADDR_GEN11P5, GFX_MSTR_INTR_ADDR_GEN11P5, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                GEN11P5MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler, GEN11P5MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Display Interrupt Control Regsiter
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/20451
        bRet =
        COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DISPLAY_INTR_CTL_ADDR_GEN11P5, DISPLAY_INTR_CTL_ADDR_GEN11P5, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                GEN11P5MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler, GEN11P5MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/8409
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_DE_INTR_ADDR_SPT_GEN11P5, SOUTH_DE_INTR_ADDR_SPT_GEN11P5, 0, NULL, NULL, 0, FALSE,
                                                       eNoExecHw, GEN11P5MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler, NULL, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_DE_INTR_ADDR_SPT_GEN11P5 + 0x8, SOUTH_DE_INTR_ADDR_SPT_GEN11P5 + 0x8, 0, NULL, NULL, 0,
                                                       TRUE, eReadCombine, NULL,
                                                       // GEN11P5MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler,
                                                       GEN11P5MMIOHANDLERS_HotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21778
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21779
        // The status fields indicate the hot plug detect status on each port. When HPD is enabled and either a long or short pulse is detected for a port
        // These two are the south hot plug control registers
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN11P5, SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN11P5, 0, NULL,
                                                       NULL, 0, TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_HotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN11P5, THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN11P5, 0, NULL, NULL,
                                                       0, TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_TBTHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, TYPE_C_HOT_PLUG_CTL_ADDR_GEN11P5, TYPE_C_HOT_PLUG_CTL_ADDR_GEN11P5, 0, NULL, NULL, 0, TRUE,
                                                       eNoExecHw, NULL, GEN11P5MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // DE Engine IIR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21261?dstFilter=ICLHP&mode=Filter
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       (DE_HPD_INTR_ADDR_GEN11P5 + 0x8), // DE IIR
                                                       (DE_HPD_INTR_ADDR_GEN11P5 + 0x8), 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       GEN11P5MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // DE Engine ISR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21261?dstFilter=ICLHP&mode=Filter
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE,
                                                       (DE_HPD_INTR_ADDR_GEN11P5 + 0x0), // ISR LiveState
                                                       (DE_HPD_INTR_ADDR_GEN11P5 + 0x0), 0, NULL, NULL, 0, FALSE, eNoExecHw, GEN11P5MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler,
                                                       NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // MGPhyLanes Handlers - FIA1
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN11P5, PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN11P5, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // MGPhyLanes Handlers - FIA2
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN11P5, PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN11P5, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // MGPhyLanes Handlers - FIA3
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN11P5, PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN11P5, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        /*To handle upfront link training
          Each FIA can have upto 4 instance of scratch pad
          FIA1 - SP1 to SP4
        */
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA1_ADDR_D11P5, PORT_TX_DFLEXDPSP4_FIA1_ADDR_D11P5, 0, NULL, NULL, 0,
                                                       FALSE, eReadCombine, GEN11P5MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        /*To handle upfront link training
        Each FIA can have upto 4 instance of scratch pad
        FIA2 - SP1 to SP4
        */
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA2_ADDR_D11P5, PORT_TX_DFLEXDPSP4_FIA2_ADDR_D11P5, 0, NULL, NULL, 0,
                                                       FALSE, eReadCombine, GEN11P5MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        /*To handle upfront link training
        Each FIA can have upto 4 instance of scratch pad
        FIA3 - SP1 to SP4
        */
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPSP1_FIA3_ADDR_D11P5, PORT_TX_DFLEXDPSP4_FIA3_ADDR_D11P5, 0, NULL, NULL, 0,
                                                       FALSE, eReadCombine, GEN11P5MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // DPCSSS MGPhyLanes Handlers - FIA1
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPCSSS_FIA1_ADDR_D11P5, PORT_TX_DFLEXDPCSSS_FIA1_ADDR_D11P5, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DPCSSS MGPhyLanes Handlers - FIA2
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPCSSS_FIA2_ADDR_D11P5, PORT_TX_DFLEXDPCSSS_FIA2_ADDR_D11P5, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DPCSSS MGPhyLanes Handlers - FIA3
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPMLE1_FIA3_ADDR_D11P5, PORT_TX_DFLEXDPMLE1_FIA3_ADDR_D11P5, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DFLEXDPMLE1 MGPhyLanes Handlers - FIA1
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPMLE1_FIA1_ADDR_D11P5, PORT_TX_DFLEXDPMLE1_FIA1_ADDR_D11P5, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DFLEXDPMLE1 MGPhyLanes Handlers - FIA2
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPMLE1_FIA2_ADDR_D11P5, PORT_TX_DFLEXDPMLE1_FIA2_ADDR_D11P5, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DFLEXDPMLE1 MGPhyLanes Handlers - FIA3
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_TX_DFLEXDPMLE1_FIA3_ADDR_D11P5, PORT_TX_DFLEXDPMLE1_FIA3_ADDR_D11P5, 0, NULL, NULL, 0,
                                                       TRUE, eNoExecHw, NULL, GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DKL_TX_DPCNTL0_L_INSTANCE_LKF
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, (DKL_PHYBASE_PORT1_ADDR + DKL_TX_DPCTRL0_L_TX1LN0_ADDR_LKF),
                                                       (DKL_PHYBASE_PORT1_ADDR + DKL_TX_DPCTRL0_L_TX1LN0_ADDR_LKF), 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DKL_TX_DPCNTL1_L_INSTANCE_LKF
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, (DKL_PHYBASE_PORT1_ADDR + DKL_TX_DPCNTL1_L_TX2LN0_ADDR_LKF),
                                                       (DKL_PHYBASE_PORT1_ADDR + DKL_TX_DPCNTL1_L_TX2LN0_ADDR_LKF), 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DKL_TX_DPCNTL2_INSTANCE_LKF
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, (DKL_PHYBASE_PORT1_ADDR + DKL_TX_DPCNTL2_TX2LN0_ADDR_LKF),
                                                       (DKL_PHYBASE_PORT1_ADDR + DKL_TX_DPCNTL2_TX2LN0_ADDR_LKF), 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DKL_PHYBASE_PORT2_ADDR DKL_TX_DPCNTL0_L_INSTANCE_LKF
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, (DKL_PHYBASE_PORT2_ADDR + DKL_TX_DPCTRL0_L_TX1LN0_ADDR_LKF),
                                                       (DKL_PHYBASE_PORT2_ADDR + DKL_TX_DPCTRL0_L_TX1LN0_ADDR_LKF), 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DKL_PHYBASE_PORT2_ADDR DKL_TX_DPCNTL1_L_INSTANCE_LKF
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, (DKL_PHYBASE_PORT2_ADDR + DKL_TX_DPCNTL1_L_TX2LN0_ADDR_LKF),
                                                       (DKL_PHYBASE_PORT2_ADDR + DKL_TX_DPCNTL1_L_TX2LN0_ADDR_LKF), 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DKL_PHYBASE_PORT2_ADDR DKL_TX_DPCNTL2_INSTANCE_LKF
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, (DKL_PHYBASE_PORT2_ADDR + DKL_TX_DPCNTL2_TX2LN0_ADDR_LKF),
                                                       (DKL_PHYBASE_PORT2_ADDR + DKL_TX_DPCNTL2_TX2LN0_ADDR_LKF), 0, NULL, NULL, 0, TRUE, eNoExecHw, NULL,
                                                       GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // Workaround to support TypeC ports. In the default mode for TC ports, IOM wouldn't have initialized PHY. So, the DDI Buffer is IDLE. As per the recommendation from
        // Ganesh/Raghu, it is being masked in valsim.
        for (int ddi_offset = DDI_BUF_CTL_USBC1_ADDR_D11P5; ddi_offset <= DDI_BUF_CTL_USBC6_ADDR_D11P5; ddi_offset += 256)
        {
            bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, ddi_offset, ddi_offset, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                           GEN11P5MMIOHANDLERS_DdiBufferControlMMIOReadHandler, NULL, NULL, NULL, NULL);

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
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PWR_WELL_CTL_DDI2_ADDR_D11P5, PWR_WELL_CTL_DDI2_ADDR_D11P5, 0, NULL, NULL, 0, FALSE,
                                                       eNoExecHw, GEN11P5MMIOHANDLERS_PwrWellDDIControlMMIOReadHandler, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // DE PORT IIR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/7541
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DE_PORT_IIR_ADDR_D11P5, DE_PORT_IIR_ADDR_D11P5, 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       GEN11P5MMIOHANDLERS_DEPortIIRMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // DE PORT Engine ISR Register
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/7541
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DE_PORT_ISR_ADDR_D11P5, DE_PORT_ISR_ADDR_D11P5, 0, NULL, NULL, 0, TRUE, eReadCombine, NULL,
                                                       NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

        // DE PORT Engine ISR Register -> DSI0
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/19736
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DSI_INTER_IDENT_REG_0_ADDR_D11, DSI_INTER_IDENT_REG_0_ADDR_D11, 0, NULL, NULL, 0, TRUE,
                                                       eReadCombine, NULL, GEN11P5MMIOHANDLERS_DSIInterIdentMMIOWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }

        // DE PORT Engine ISR Register -> DSI1
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/19736
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, DSI_INTER_IDENT_REG_1_ADDR_D11, DSI_INTER_IDENT_REG_1_ADDR_D11, 0, NULL, NULL, 0, TRUE,
                                                       eReadCombine, NULL, GEN11P5MMIOHANDLERS_DSIInterIdentMMIOWriteHandler, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11P5MMIOHANDLERS_MasterInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    GFX_MSTR_INTR_GEN11P5 stMasterIntCtrl = { 0 };
    stMasterIntCtrl.Value = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stMasterIntCtrl.MasterInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                   // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stMasterIntCtrl.Value;

    return TRUE;
}

BOOLEAN GEN11P5MMIOHANDLERS_MasterInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN11P5 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN11P5)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    GFX_MSTR_INTR_GEN11P5 stMasterIntCtrlTemp = { 0 };

    stMasterIntCtrlTemp.Value               = ulWriteData;
    pstMasterIntCtrl->MasterInterruptEnable = stMasterIntCtrlTemp.MasterInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN11P5MMIOHANDLERS_DisplayInterruptCtlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    DISPLAY_INT_CTL_GEN11P5 stDisplayIntCtrl = { 0 };
    stDisplayIntCtrl.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    if (peRegRWExecSite)
        *peRegRWExecSite = eReadCombine;

    stDisplayIntCtrl.DisplayInterruptEnable = FALSE; // Setting enable bit to false as this register would be Bitwise Or'ed with the actual hardware register.
                                                     // Enable bit would be appropriately set by the Or'ing if its set in the actual hardware.

    *pulReadData = stDisplayIntCtrl.ulValue;

    return TRUE;
}

BOOLEAN GEN11P5MMIOHANDLERS_DisplayInterruptCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PDISPLAY_INT_CTL_GEN11P5 stDisplayIntCtrl =
    (PDISPLAY_INT_CTL_GEN11P5)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    DISPLAY_INT_CTL_GEN11P5 stDisplayIntCtrlTemp = { 0 };

    stDisplayIntCtrlTemp.ulValue             = ulWriteData;
    stDisplayIntCtrl->DisplayInterruptEnable = stDisplayIntCtrlTemp.DisplayInterruptEnable;

    if (peRegRWExecSite)
        *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN11P5MMIOHANDLERS_HotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN11P5 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN11P5)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN11P5 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5 *pstPCHIIRReg    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5  stPCHIIRRegTemp = { 0 };
    pstPCHIIRReg =
    (SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5 *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.ulValue = ulWriteData;

    if (stPCHIIRRegTemp.ulValue != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        pstPCHIIRReg->ulValue &= ~stPCHIIRRegTemp.ulValue;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN11P5MMIOHANDLERS_HotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                                  bRet             = TRUE;
    SHOTPLUG_CTL_DDI_GEN11P5                 stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_TC_GEN11P5                  stHotPlugCtl2    = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5 stLiveStateReg   = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5 stLiveStateRegHw = { 0 };
    ULONG                                    driverRegValue   = 0;

    stHotPlugCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN11P5 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stHotPlugCtl2.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN11P5 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

    stLiveStateReg.ulValue = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, SOUTH_DE_INTR_ADDR_SPT_GEN11P5, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
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
BOOLEAN GEN11P5MMIOHANDLERS_HotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/21778
    SHOTPLUG_CTL_DDI_GEN11P5 stHotPlugCtl     = { 0 };
    SHOTPLUG_CTL_DDI_GEN11P5 stHotPlugCtlTemp = { 0 };

    /* SPT_HOTPLUG_CTL2_REG_ST stHotPlugCtl2 = { 0 };
     SPT_HOTPLUG_CTL2_REG_ST stHotPlugCtlTemp2 = { 0 };*/

    // Bspec: https://gfxspecs.intel.com/Predator/Home/Index/21779
    SHOTPLUG_CTL_TC_GEN11P5 stHotPlugCtl2     = { 0 };
    SHOTPLUG_CTL_TC_GEN11P5 stHotPlugCtlTemp2 = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN11P5 == ulMMIOOffset)
        {
            pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

            stHotPlugCtlTemp.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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
            stHotPlugCtlTemp2.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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

BOOLEAN GEN11P5MMIOHANDLERS_IsHPDEnabledForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                    bRet                = FALSE;
    SHOTPLUG_CTL_DDI_GEN11P5   stSouthDDICtlReg    = { 0 };
    SHOTPLUG_CTL_TC_GEN11P5    stSouthTCCtlreg     = { 0 };
    HOTPLUG_CTL_GEN11P5        stNorthTCCtlreg     = { 0 };
    HOTPLUG_CTL_GEN11P5        stNorthTBTCtlreg    = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stSouthDDICtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stSouthTCCtlreg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthTCCtlreg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stNorthTBTCtlreg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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
            else if (stSouthTCCtlreg.Tc1HpdEnable && PortConnectorInfo.IsTypeC == FALSE && PortConnectorInfo.IsTbt == FALSE)
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
            else if (stSouthTCCtlreg.Tc2HpdEnable && PortConnectorInfo.IsTypeC == FALSE && PortConnectorInfo.IsTbt == FALSE)
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
            else if (stSouthTCCtlreg.Tc3HpdEnable && PortConnectorInfo.IsTypeC == FALSE && PortConnectorInfo.IsTbt == FALSE)
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
            else if (stSouthTCCtlreg.Tc4HpdEnable && PortConnectorInfo.IsTypeC == FALSE && PortConnectorInfo.IsTbt == FALSE)
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
            else if (stSouthTCCtlreg.Tc5HpdEnable && PortConnectorInfo.IsTypeC == FALSE && PortConnectorInfo.IsTbt == FALSE)
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
            else if (stSouthTCCtlreg.Tc6HpdEnable && PortConnectorInfo.IsTypeC == FALSE && PortConnectorInfo.IsTbt == FALSE)
            {
                bRet = TRUE;
            }
            break;

        default:
            break;
        }

    } while (FALSE);
    GFXVALSIM_HPDSTATUS(pstMMIOInterface->eIGFXPlatform, SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN11P5, stSouthDDICtlReg.ulValue, SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN11P5,
                        stSouthTCCtlreg.ulValue, TYPE_C_HOT_PLUG_CTL_ADDR_GEN11P5, stNorthTCCtlreg.ulValue, THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN11P5, stNorthTBTCtlreg.ulValue);
    return bRet;
}

// bIsHPD == FALSE ==> SPI
BOOLEAN GEN11P5MMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, BOOLEAN bIsHPD,
                                                               PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                 bRet             = FALSE;
    GFX_MSTR_INTR_GEN11P5   stMasterIntCtrl  = { 0 };
    DISPLAY_INT_CTL_GEN11P5 stDisplayIntCtrl = { 0 };

    SHOTPLUG_CTL_DDI_GEN11P5 stSouthCtlReg = { 0 };
    SHOTPLUG_CTL_TC_GEN11P5  stTCCTLreg    = { 0 };

    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5 stPCHLiveReg = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5 stPCHIMRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5 stPCHIIRReg  = { 0 };
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5 stPCHIERReg  = { 0 };

    HOTPLUG_CTL_GEN11P5 stTBTHotPlugCtl   = { 0 };
    HOTPLUG_CTL_GEN11P5 stTYPECHotPlugCtl = { 0 };

    DE_HPD_INTR_DEFINITION_GEN11P5 stDEHPDISR = { 0 };
    DE_HPD_INTR_DEFINITION_GEN11P5 stDEHPDIMR = { 0 };
    DE_HPD_INTR_DEFINITION_GEN11P5 stDEHPDIIR = { 0 };
    DE_HPD_INTR_DEFINITION_GEN11P5 stDEHPDIER = { 0 };

    PORT_TX_DFLEXDPPMS_GEN11P5 stTypeCFia1Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN11P5 stTypeCFia2Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN11P5 stTypeCFia3Status = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        // Check if HPD has been enabled by Gfx
        if (FALSE == GEN11P5MMIOHANDLERS_IsHPDEnabledForPort(pstMMIOInterface, ePortType, PortConnectorInfo))
        {
            break;
        }

        stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Bspec Ref; https://gfxspecs.intel.com/Predator/Home/Index/21778
        stSouthCtlReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/21779
        stTCCTLreg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // Legacy
        // Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/8409
        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_GEN11P5)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIMRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_GEN11P5 + 0x4) - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIIRReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_GEN11P5 + 0x8) - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stPCHIERReg.ulValue  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_GEN11P5 + 0xC) - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stTBTHotPlugCtl.ulValue   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTYPECHotPlugCtl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        // TypeC or TBT
        stDEHPDISR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_INTR_ADDR_GEN11P5)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIMR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_INTR_ADDR_GEN11P5 + 0x4) - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIIR.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_INTR_ADDR_GEN11P5 + 0x8) - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDIER.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_INTR_ADDR_GEN11P5 + 0xC) - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stTypeCFia1Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFia2Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFia3Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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
                    stSouthCtlReg.DdibHpdStatus = 0x1;
                    bRet                        = TRUE;
                }
            }

            break;

        case INTDPD_PORT:
        case INTHDMID_PORT:
            // TYPE_C North Bridge
            if (stTYPECHotPlugCtl.Port1HpdEnable && stDEHPDIMR.Tc1Hotplug == FALSE && stDEHPDIER.Tc1Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc1Hotplug                                        = TRUE;
                    stDEHPDISR.Tc1Hotplug                                        = bAttach; // LiveState Register
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
            else if (stTBTHotPlugCtl.Port1HpdEnable && stDEHPDIMR.Tbt1Hotplug == FALSE && stDEHPDIER.Tbt1Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt1Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt1Hotplug                                       = bAttach; // LiveState Register
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
            if (stTCCTLreg.Tc1HpdEnable && stPCHIMRReg.HotplugTypecPort1 == FALSE && stPCHIERReg.HotplugTypecPort1)
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
            if (stTYPECHotPlugCtl.Port2HpdEnable && stDEHPDIMR.Tc2Hotplug == FALSE && stDEHPDIER.Tc2Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc2Hotplug                                        = TRUE;
                    stDEHPDISR.Tc2Hotplug                                        = bAttach; // LiveState Register
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
            else if (stTBTHotPlugCtl.Port2HpdEnable && stDEHPDIMR.Tbt2Hotplug == FALSE && stDEHPDIER.Tbt2Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt2Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt2Hotplug                                       = bAttach; // LiveState Register
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
            if (stTCCTLreg.Tc2HpdEnable && stPCHIMRReg.HotplugTypecPort2 == FALSE && stPCHIERReg.HotplugTypecPort2)
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
            if (stTYPECHotPlugCtl.Port3HpdEnable && stDEHPDIMR.Tc3Hotplug == FALSE && stDEHPDIER.Tc3Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc3Hotplug                                        = TRUE;
                    stDEHPDISR.Tc3Hotplug                                        = bAttach; // LiveState Register
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
            else if (stTBTHotPlugCtl.Port3HpdEnable && stDEHPDIMR.Tbt3Hotplug == FALSE && stDEHPDIER.Tbt3Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt3Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt3Hotplug                                       = bAttach; // LiveState Register
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
            if (stTCCTLreg.Tc3HpdEnable && stPCHIMRReg.HotplugTypecPort3 == FALSE && stPCHIERReg.HotplugTypecPort3)
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
            if (stTYPECHotPlugCtl.Port4HpdEnable && stDEHPDIMR.Tc4Hotplug == FALSE && stDEHPDIER.Tc4Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc4Hotplug                                        = TRUE;
                    stDEHPDISR.Tc4Hotplug                                        = bAttach; // LiveState Register
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
            else if (stTBTHotPlugCtl.Port4HpdEnable && stDEHPDIMR.Tbt4Hotplug == FALSE && stDEHPDIER.Tbt4Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt4Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt4Hotplug                                       = bAttach; // LiveState Register
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
            if (stTCCTLreg.Tc4HpdEnable && stPCHIMRReg.HotplugTypecPort4 == FALSE && stPCHIERReg.HotplugTypecPort4)
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
            if (stTYPECHotPlugCtl.Port5HpdEnable && stDEHPDIMR.Tc5Hotplug == FALSE && stDEHPDIER.Tc5Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc5Hotplug                                        = TRUE;
                    stDEHPDISR.Tc5Hotplug                                        = bAttach; // LiveState Register
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
            else if (stTBTHotPlugCtl.Port5HpdEnable && stDEHPDIMR.Tbt5Hotplug == FALSE && stDEHPDIER.Tbt5Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt5Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt5Hotplug                                       = bAttach; // LiveState Register
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
            if (stTCCTLreg.Tc5HpdEnable && stPCHIMRReg.HotplugTypecPort5 == FALSE && stPCHIERReg.HotplugTypecPort5)
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
            if (stTYPECHotPlugCtl.Port6HpdEnable && stDEHPDIMR.Tc6Hotplug == FALSE && stDEHPDIER.Tc6Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tc6Hotplug                                        = TRUE;
                    stDEHPDISR.Tc6Hotplug                                        = bAttach; // LiveState Register
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
            else if (stTBTHotPlugCtl.Port6HpdEnable && stDEHPDIMR.Tbt6Hotplug == FALSE && stDEHPDIER.Tbt6Hotplug)
            {
                if (bIsHPD)
                {
                    stDEHPDIIR.Tbt6Hotplug                                       = TRUE;
                    stDEHPDISR.Tbt6Hotplug                                       = bAttach; // LiveState Register
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
            if (stTCCTLreg.Tc6HpdEnable && stPCHIMRReg.HotplugTypecPort6 == FALSE && stPCHIERReg.HotplugTypecPort6)
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
        // Below line is a temp workaround
        stPCHLiveReg.HotplugDdia                 = TRUE;
        stMasterIntCtrl.DisplayInterruptsPending = TRUE;
        stDisplayIntCtrl.DeHpdInterruptsPending  = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_DDI_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset])   = stSouthCtlReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_HOT_PLUG_CTL_FOR_TYPEC_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTCCTLreg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_INTR_ADDR_SPT_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset])            = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(SOUTH_DE_INTR_ADDR_SPT_GEN11P5 + 0x8) - pstGlobalMMORegData->ulMMIOBaseOffset])    = stPCHIIRReg.ulValue;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia1Status.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia2Status.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia3Status.ulValue;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTBTHotPlugCtl.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset])      = stTYPECHotPlugCtl.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_INTR_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset])              = stDEHPDISR.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_HPD_INTR_ADDR_GEN11P5 + 0x8) - pstGlobalMMORegData->ulMMIOBaseOffset])      = stDEHPDIIR.ulValue;
    }

    return bRet;
}

BOOLEAN GEN11P5MMIOHANDLERS_SetupInterruptRegistersForTE(PMMIO_INTERFACE pstMMIOInterface, MIPI_DSI_PORT_TYPE ePortType)
{
    BOOLEAN                 bRet             = FALSE;
    GFX_MSTR_INTR_GEN11P5   stMasterIntCtrl  = { 0 };
    DISPLAY_INT_CTL_GEN11P5 stDisplayIntCtrl = { 0 };

    DE_PORT_INTERRUPT_DEFINITION_D11P5 stDEPortLiveReg = { 0 };
    DE_PORT_INTERRUPT_DEFINITION_D11P5 stDEPortIMRReg  = { 0 };
    DE_PORT_INTERRUPT_DEFINITION_D11P5 stDEPortIIRReg  = { 0 };
    DE_PORT_INTERRUPT_DEFINITION_D11P5 stDEPortIERReg  = { 0 };

    DSI_INTER_IDENT_REG_D11 stDsi0InterIdentReg = { 0 };
    DSI_INTER_IDENT_REG_D11 stDsi1InterIdentReg = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        stMasterIntCtrl.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDisplayIntCtrl.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDEPortLiveReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_PORT_ISR_ADDR_D11P5)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEPortIMRReg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_PORT_IMR_ADDR_D11P5)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEPortIIRReg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_PORT_IIR_ADDR_D11P5)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEPortIERReg.Value  = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_PORT_IER_ADDR_D11P5)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        stDsi0InterIdentReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DSI_INTER_IDENT_REG_0_ADDR_D11)-pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDsi1InterIdentReg.Value = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DSI_INTER_IDENT_REG_1_ADDR_D11)-pstGlobalMMORegData->ulMMIOBaseOffset]);

        switch (ePortType)
        {
        case DD_PORT_TYPE_DSI_PORT_0:

            if (stDEPortIMRReg.Dsi0Te == FALSE && stDEPortIERReg.Dsi0Te)
            {
                stDsi0InterIdentReg.TeEvent = TRUE;
                stDEPortIIRReg.Dsi0Te       = TRUE;
                stDEPortLiveReg.Dsi0Te      = TRUE;
                bRet                        = TRUE;
            }

            break;

        case DD_PORT_TYPE_DSI_PORT_1:
        case DD_PORT_TYPE_DSI_PORT_DUAL: // sending DSI1 Te is enough in case of dual port. Input from Srikanth.
            if (stDEPortIMRReg.Dsi1Te == FALSE && stDEPortIERReg.Dsi1Te)
            {
                stDsi1InterIdentReg.TeEvent = TRUE;
                stDEPortIIRReg.Dsi1Te       = TRUE;
                stDEPortLiveReg.Dsi1Te      = TRUE;
                bRet                        = TRUE;
            }

            break;

        default:

            break;
        }

    } while (FALSE);

    if (bRet)
    {
        stMasterIntCtrl.DisplayInterruptsPending = TRUE;
        stDisplayIntCtrl.DePortInterruptsPending = TRUE;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_PORT_ISR_ADDR_D11P5)-pstGlobalMMORegData->ulMMIOBaseOffset]) = stDEPortLiveReg.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_PORT_IMR_ADDR_D11P5)-pstGlobalMMORegData->ulMMIOBaseOffset]) = stDEPortIMRReg.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_PORT_IIR_ADDR_D11P5)-pstGlobalMMORegData->ulMMIOBaseOffset]) = stDEPortIIRReg.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DE_PORT_IER_ADDR_D11P5)-pstGlobalMMORegData->ulMMIOBaseOffset]) = stDEPortIERReg.Value;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DSI_INTER_IDENT_REG_0_ADDR_D11)-pstGlobalMMORegData->ulMMIOBaseOffset]) = stDsi0InterIdentReg.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[(DSI_INTER_IDENT_REG_1_ADDR_D11)-pstGlobalMMORegData->ulMMIOBaseOffset]) = stDsi1InterIdentReg.Value;

        /*********we might need memory barrier here to save us from compiler or processor re-ordering *******/
        // x86 is generally strongly ordered but barriers would guard against compiler reordering when optimization is enabled

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DISPLAY_INTR_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stDisplayIntCtrl.ulValue;
        // New update. Upper comment doesn't hold because the whole thing happens in a single thread. o0OPs
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stMasterIntCtrl.Value;
    }

    return bRet;
}

// TODO: Need to take care of TBT/TypeC
BOOLEAN GEN11P5MMIOHANDLERS_SetLiveStateForPort(PMMIO_INTERFACE pstMMIOInterface, PORT_TYPE ePortType, BOOLEAN bAttach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN                                  bRet                = TRUE;
    SOUTH_DE_INTR_BIT_DEFINITION_SPT_GEN11P5 stPCHLiveReg        = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA               pstGlobalMMORegData = &pstMMIOInterface->stGlobalMMORegData;
    DE_HPD_INTR_DEFINITION_GEN11P5           stDEHPDISR          = { 0 };

    // MG PHY Lines Enabling for Port D - Port F
    PORT_TX_DFLEXDPPMS_GEN11P5 stTypeCFia1Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN11P5 stTypeCFia2Status = { 0 };
    PORT_TX_DFLEXDPPMS_GEN11P5 stTypeCFia3Status = { 0 };

    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        /* get current TYPE C FIA Status from val-sim MMIO database before before enabling MG PHY lane for different ports (BUG ID - 1607574661)  */
        stTypeCFia1Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFia2Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stTypeCFia3Status.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

        stPCHLiveReg.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_INTR_ADDR_SPT_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);
        stDEHPDISR.ulValue   = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_INTR_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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
        stPCHLiveReg.HotplugDdia                                                                                                          = TRUE;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[SOUTH_DE_INTR_ADDR_SPT_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset])       = stPCHLiveReg.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[DE_HPD_INTR_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset])             = stDEHPDISR.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA1_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia1Status.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA2_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia2Status.ulValue;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[PORT_TX_DFLEXDPPMS_FIA3_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]) = stTypeCFia3Status.ulValue;
    }

    return bRet;
}

BOOLEAN GEN11P5MMIOHANDLERS_DEHotPlugLiveStateMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = TRUE;
    // THUNDERBOLT
    HOTPLUG_CTL_GEN11P5 stHotPlugCtl = { 0 };
    // TYPE_C
    HOTPLUG_CTL_GEN11P5            stHotPlugCtl2  = { 0 };
    DE_HPD_INTR_DEFINITION_GEN11P5 stLiveStateReg = { 0 };

    stHotPlugCtl.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN11P5 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);
    stHotPlugCtl2.ulValue =
    *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN11P5 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

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

BOOLEAN GEN11P5MMIOHANDLERS_DEHotPlugIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN11P5 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN11P5)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN11P5 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    DE_HPD_INTR_DEFINITION_GEN11P5 *pstPCHIIRReg    = { 0 }; // DE Interrupt IIR
    DE_HPD_INTR_DEFINITION_GEN11P5  stPCHIIRRegTemp = { 0 }; // DE Interrupt IIR

    pstPCHIIRReg =
    (DE_HPD_INTR_DEFINITION_GEN11P5 *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stPCHIIRRegTemp.ulValue = ulWriteData;

    if (stPCHIIRRegTemp.ulValue != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        pstPCHIIRReg->ulValue &= ~stPCHIIRRegTemp.ulValue;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN11P5MMIOHANDLERS_TBTHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    HOTPLUG_CTL_GEN11P5 stHotPlugCtl     = { 0 };
    HOTPLUG_CTL_GEN11P5 stHotPlugCtlTemp = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN11P5 == ulMMIOOffset)
        {
            pstGlobalMMORegData      = &pstMMIOHandlerInfo->stGlobalMMORegData;
            stHotPlugCtlTemp.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[THUNDERBOLT_HOT_PLUG_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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

BOOLEAN GEN11P5MMIOHANDLERS_TYPECHotPlugCtlMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    HOTPLUG_CTL_GEN11P5 stHotPlugCtl     = { 0 };
    HOTPLUG_CTL_GEN11P5 stHotPlugCtlTemp = { 0 };

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        if (TYPE_C_HOT_PLUG_CTL_ADDR_GEN11P5 == ulMMIOOffset)
        {
            pstGlobalMMORegData      = &pstMMIOHandlerInfo->stGlobalMMORegData;
            stHotPlugCtlTemp.ulValue = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[TYPE_C_HOT_PLUG_CTL_ADDR_GEN11P5 - pstGlobalMMORegData->ulMMIOBaseOffset]);

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

// This function needs to be revisited once Gfx Driver code for TYPEC/TBT code is fianlised
// This may or may not be needed
BOOLEAN GEN11P5MMIOHANDLERS_MgPhyLanesMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = ulWriteData;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

/**-------------------------------------------------------------
 * @brief GEN11P5MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler
 *
 * Description: Set the number of lanes assigned to display for Read MG Phy scratch register (DFLEXDPSP1)
 *       This call is valid only for MG Phy ports (DDI C/D/E/F) and Type-C connector
 *
 * TBD: This is a replacement for upfront link training to determine # lanes used in Type-C.
 *       Need to pass this info. up to Protocol.
 *-------------------------------------------------------------*/
BOOLEAN GEN11P5MMIOHANDLERS_GetLanesAssignedfromMGPhyMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                     PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = FALSE;

    PORT_TX_DFLEXDPSP_D11P5    LaneData            = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
        LaneData.ulValue    = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);
        // Setting ModularFia bit to 1 for the first instance of FIA i.e, DPSP1_FIA1;
        // This bit is static for a board and will be set by IOM FW
        // This will not be altered by Driver and will not change dynamically
        // Reference from : https://gfxspecs.intel.com/Predator/Home/Index/21563
        if (ulMMIOOffset == PORT_TX_DFLEXDPSP1_FIA1_ADDR_D11P5)
        {
            LaneData.ModularFia_Mf = 1;
        }
        // Currently 2 lanes are assinged for all the Port Types
        // TODO:
        // 1) Based on Live State of a Port, Lane Values can be assigned to a particualr port
        // 2) Lane Values can be configured run time also.Run time configuration can be done through registry write/read
        // These two items will be taken up later after discussing with VCO

        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector0 = D11P5_PHY_TX1_TX0;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector1 = D11P5_PHY_TX1_TX0;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector2 = D11P5_PHY_TX1_TX0;
        LaneData.DisplayPortX4TxLaneAssignmentForTypeCConnector3 = D11P5_PHY_TX1_TX0;

        *pulReadData = LaneData.ulValue;

        // The value of ulMMIOOffset will be either
        //	PORT_TX_DFLEXDPSP1_FIA1_ADDR_D11P5 = 0x1638A0,
        //	PORT_TX_DFLEXDPSP2_FIA1_ADDR_D11P5 = 0x1638A4,
        //	PORT_TX_DFLEXDPSP3_FIA1_ADDR_D11P5 = 0x1638A8,
        //	PORT_TX_DFLEXDPSP4_FIA1_ADDR_D11P5 = 0x1638AC,
        //	PORT_TX_DFLEXDPSP1_FIA2_ADDR_D11P5 = 0x16E8A0,
        //	PORT_TX_DFLEXDPSP2_FIA2_ADDR_D11P5 = 0x16E8A4,
        //	PORT_TX_DFLEXDPSP3_FIA2_ADDR_D11P5 = 0x16E8A8,
        //	PORT_TX_DFLEXDPSP4_FIA2_ADDR_D11P5 = 0x16E8AC,
        //	PORT_TX_DFLEXDPSP1_FIA3_ADDR_D11P5 = 0x16F8A0,
        //	PORT_TX_DFLEXDPSP2_FIA3_ADDR_D11P5 = 0x16F8A4,
        //	PORT_TX_DFLEXDPSP3_FIA3_ADDR_D11P5 = 0x16F8A8,
        //	PORT_TX_DFLEXDPSP4_FIA3_ADDR_D11P5 = 0x16F8AC,

        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = LaneData.ulValue;

        bRet = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN GEN11P5MMIOHANDLERS_DdiBufferControlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN            bRet            = TRUE;
    DDI_BUF_CTL_D11P5  stDdiBufCtlReg  = { 0 };
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

BOOLEAN GEN11P5MMIOHANDLERS_PwrWellDDIControlMMIOReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                bRet               = TRUE;
    PWR_WELL_CTL_DDI_D11P5 stPwrWellDdiCtlReg = { 0 };

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

BOOLEAN GEN11P5MMIOHANDLERS_DEPortIIRMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PGFX_MSTR_INTR_GEN11P5 pstMasterIntCtrl =
    (PGFX_MSTR_INTR_GEN11P5)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[GFX_MSTR_INTR_ADDR_GEN11P5 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];

    DE_PORT_INTERRUPT_DEFINITION_D11P5 *pstDEPortIIRReg    = { 0 }; // DE Port Interrupt IIR
    DE_PORT_INTERRUPT_DEFINITION_D11P5  stDEPortIIRRegTemp = { 0 }; // DE Port Interrupt IIR

    pstDEPortIIRReg =
    (DE_PORT_INTERRUPT_DEFINITION_D11P5 *)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
    stDEPortIIRRegTemp.Value = ulWriteData;

    if (stDEPortIIRRegTemp.Value != 0)
    {
        pstMasterIntCtrl->DisplayInterruptsPending = FALSE;
        pstDEPortIIRReg->Value &= ~stDEPortIIRRegTemp.Value;

        if (stDEPortIIRRegTemp.Dsi0Te)
        {
            // Clear DSI0Te ISR
            DE_PORT_INTERRUPT_DEFINITION_D11P5 *pstDEPortISRReg = (DE_PORT_INTERRUPT_DEFINITION_D11P5 *)&pstMMIOHandlerInfo->stGlobalMMORegData
                                                                  .ucMMIORegisterFile[DE_PORT_ISR_ADDR_D11P5 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
            pstDEPortISRReg->Dsi0Te = 0;
        }

        if (stDEPortIIRRegTemp.Dsi1Te)
        {
            // Clear DSI1Te ISR
            DE_PORT_INTERRUPT_DEFINITION_D11P5 *pstDEPortISRReg = (DE_PORT_INTERRUPT_DEFINITION_D11P5 *)&pstMMIOHandlerInfo->stGlobalMMORegData
                                                                  .ucMMIORegisterFile[DE_PORT_ISR_ADDR_D11P5 - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];
            pstDEPortISRReg->Dsi1Te = 0;
        }
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}

BOOLEAN GEN11P5MMIOHANDLERS_DSIInterIdentMMIOWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    PDSI_INTER_IDENT_REG_D11 pstDsiInterReg    = NULL;
    DSI_INTER_IDENT_REG_D11  stDsiInterRegTemp = { 0 };

    pstDsiInterReg = (PDSI_INTER_IDENT_REG_D11)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulMMIOOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset];

    stDsiInterRegTemp.Value = ulWriteData;

    if (stDsiInterRegTemp.Value != 0)
    {
        pstDsiInterReg->Value &= ~stDsiInterRegTemp.Value;
    }

    *peRegRWExecSite = eExecHW;

    return TRUE;
}