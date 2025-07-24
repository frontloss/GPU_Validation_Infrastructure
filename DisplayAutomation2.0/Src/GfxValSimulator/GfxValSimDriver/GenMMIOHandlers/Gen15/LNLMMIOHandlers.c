
#include "LNLMMIO.h"
#include "../../CommonInclude/ETWLogging.h"

BOOLEAN LNL_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    if (pstMMIOInterface)
    {

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_START] = DDI_AUX_DATA_A_START_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_A_END]   = DDI_AUX_DATA_A_END_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_A]        = DDI_AUX_CTL_A_GEN15;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_START] = DDI_AUX_DATA_B_START_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_B_END]   = DDI_AUX_DATA_B_END_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_B]        = DDI_AUX_CTL_B_GEN15;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_START] = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_C_END]   = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_C]        = OFFSET_INVALID;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_START] = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_D_END]   = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_D]        = OFFSET_INVALID;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_START] = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_E_END]   = OFFSET_INVALID;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_E]        = OFFSET_INVALID;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_START] = DDI_AUX_DATA_TC1_START_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_F_END]   = DDI_AUX_DATA_TC1_END_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_F]        = DDI_AUX_CTL_TC1_GEN15;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_G_START] = DDI_AUX_DATA_TC2_START_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_G_END]   = DDI_AUX_DATA_TC2_END_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_G]        = DDI_AUX_CTL_TC2_GEN15;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_H_START] = DDI_AUX_DATA_TC3_START_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_H_END]   = DDI_AUX_DATA_TC3_END_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_H]        = DDI_AUX_CTL_TC3_GEN15;

        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_I_START] = DDI_AUX_DATA_TC4_START_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_DATA_I_END]   = DDI_AUX_DATA_TC4_END_GEN15;
        pstMMIOInterface->pulGenMMIOOffsetArray[eINDEX_DDI_AUX_CTL_I]        = DDI_AUX_CTL_TC4_GEN15;

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

BOOLEAN LNL_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = FALSE;
    do
    {
        if (pstMMIOInterface == NULL)
        {
            break;
        }

        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_BUF_CTL1_A_ADDR_D15, PORT_BUF_CTL1_A_ADDR_D15, 0, NULL, NULL, 0, FALSE, eReadCombine,
                                                       GEN15_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, FALSE, PORT_BUF_CTL1_B_ADDR_D15, PORT_BUF_CTL1_B_ADDR_D15, 0, NULL, NULL, 0, FALSE, eReadCombine,
                                                       GEN15_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers, NULL, NULL, NULL, NULL);

        if (bRet == FALSE)
        {
            break;
        }
        // TCSS_DDI_STATUS_ADDR_D15 Handlers
        bRet = COMMONMMIOHANDLERS_RegisterMMIOHandlers(pstMMIOInterface, 0xFF, TRUE, TCSS_DDI_STATUS_1_ADDR_D15, TCSS_DDI_STATUS_4_ADDR_D15, 0, NULL, NULL, 0, FALSE, eNoExecHw,
                                                       GEN15_CMN_MMIOHANDLERS_PinAssignmentReadHandler, GEN15_CMN_MMIOHANDLERS_PinAssignmentWriteHandler, NULL, NULL, NULL);
        if (bRet == FALSE)
        {
            break;
        }
    } while (FALSE);
    return bRet;
}
