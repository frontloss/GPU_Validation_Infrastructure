
#include "Gen15CommonMMIO.h"
#include "..\..\DriverInterfaces\SimDrvToGfx.h"
#include "..\..\CommonInclude\ETWLogging.h"

BOOLEAN GEN15_CMN_MMIOHANDLERS_GetPhyassignedfromphyMMIOReadHandlers(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData,
                                                                     PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                    bRet                = TRUE;
    PORT_BUF_CTL1_D15          Port_Buf            = { 0 };
    PSIMDEV_EXTENTSION         pstSimDrvDevExt     = GetSimDrvExtension();
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    ULONG driverRegValue = 0;
    if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, ulMMIOOffset, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        Port_Buf.Value          = driverRegValue;
        Port_Buf.SocPhyReady    = SOC_PHY_READY_READY_D15;
        Port_Buf.TcssPowerState = TRUE;

        *pulReadData = Port_Buf.Value;
    }
    return bRet;
}

BOOLEAN GEN15_CMN_MMIOHANDLERS_PinAssignmentReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                    bRet                = FALSE;
    ULONG                      driverRegValue      = 0;
    TCSS_DDI_STATUS_D15        LaneData            = { 0 };
    TCSS_DDI_STATUS_D15        LaneDataHw          = { 0 };
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;

    do
    {
        PSIMDEV_EXTENTSION pstSimDrvDevExt = GetSimDrvExtension();
        GFXVALSIM_DBG_MSG("Entered.");

        pstGlobalMMORegData = &pstMMIOHandlerInfo->stGlobalMMORegData;
        LaneData.Value      = *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]);

        LaneData.PinAssignment = PIN_ASSIGNMENT_ASSIGNMENT_C_D15; // By Default we are assigning 4 lane for type-C DP-alt pin assignment

        if (TRUE == SIMDRVTOGFX_HwMmioAccess((PGFX_ADAPTER_CONTEXT)pstMMIOHandlerInfo->pAdapterInfo, ulMMIOOffset, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
        {
            GFXVALSIM_DBG_MSG("HW PinAssignment data: %d", driverRegValue);
            LaneDataHw.Value = driverRegValue;
            if (LaneDataHw.PinAssignment == PIN_ASSIGNMENT_ASSIGNMENT_D_D15)
            {
                GFXVALSIM_DBG_MSG("Modified.");
                LaneData.PinAssignment = PIN_ASSIGNMENT_ASSIGNMENT_D_D15;
            }
        }
        GFXVALSIM_DBG_MSG("Exit.");
        LaneData.Ready                                                                                            = TRUE;
        *pulReadData                                                                                              = LaneData.Value;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = LaneData.Value;
        bRet                                                                                                      = TRUE;

    } while (FALSE);
    return bRet;
}

BOOLEAN GEN15_CMN_MMIOHANDLERS_PinAssignmentWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN                    bRet                = FALSE;
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData = NULL;
    TCSS_DDI_STATUS_D15        LaneData            = { 0 };
    do
    {
        pstGlobalMMORegData                                                                                       = &pstMMIOHandlerInfo->stGlobalMMORegData;
        LaneData.Value                                                                                            = ulWriteData;
        *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulMMIOOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = LaneData.Value;

        bRet = TRUE;

    } while (FALSE);
    return bRet;
}