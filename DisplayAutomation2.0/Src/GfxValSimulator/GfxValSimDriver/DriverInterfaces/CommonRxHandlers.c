#include "..\\CommonCore\\PortingLayer.h"
#include "CommonRxHandlers.h"
#include "DPHandlers.h"
#include "HDMIHandlers.h"
#include "SimDrvToGfx.h"
#include "..\\GenMMIOHandlers\\CommonMMIO.h"
#include "..\\CommonInclude\\ETWLogging.h"
#include "..\\PeristenceServices\\PersistenceHandler.h"

BOOLEAN COMMONRxHANDLERS_InitSimulationDriverContext(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PRX_INFO_ARR *ppstRxInfoArr)
{
    BOOLEAN              status                 = FALSE;
    PMMIO_INTERFACE      pstMMIOInterface       = NULL;
    PRX_INFO_ARR         pstRxInfoArr           = NULL;
    PSIMDRVGFX_CONTEXT   pstSimDrvGfxContext    = NULL;
    PGFX_ADAPTER_CONTEXT pTempGfxAdapterContext = NULL;
    GFXVALSIM_FUNC_ENTRY();

    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    if (NULL == pstPortingObj || NULL == pGfxAdapterContext)
        return FALSE;

    pstSimDrvGfxContext = (PSIMDRVGFX_CONTEXT)pGfxAdapterContext->pstSimDrvGfxContext;
    if (NULL == pstSimDrvGfxContext)
        return FALSE;

    do
    {
        pTempGfxAdapterContext = pstSimDrvGfxContext->pfnGetAdapterContext(pstSimDrvGfxContext, pGfxAdapterContext->PCIBusDeviceId, pGfxAdapterContext->PCIBusInstanceId);
        if (pTempGfxAdapterContext != NULL) /* Adapter details already in lookup table */
        {
            *ppstRxInfoArr = pTempGfxAdapterContext->pstRxInfoArr; /* Assign existing pointer */
            status         = TRUE;
        }
        else
        {
            pstRxInfoArr = pstPortingObj->pfnAllocateMem(sizeof(RX_INFO_ARR), TRUE);
            if (pstRxInfoArr == NULL)
                break;

            pstRxInfoArr->pstMMIOInterface = pstPortingObj->pfnAllocateMem(sizeof(MMIO_INTERFACE), TRUE);
            if (pstRxInfoArr->pstMMIOInterface == NULL)
                break;

            *ppstRxInfoArr = pstRxInfoArr;
            status         = TRUE;
        }
    } while (FALSE);
    GFXVALSIM_FUNC_EXIT(0);
    return status;
}

// This call would come once for each port to configure a port for a particular transport
// A note on eDP simulation:
// App world should call in the order below (the same order as for DP SST simulation):
// COMMONRXHANDLERS_SetRxInfo with eDP Port info (DPPORT_A normally)
// DPHANDLERS_InitDPTopologyType with topology type as SST
// DPHANDLERS_SetEDIDData
// DPHANDLERS_SetDPCDData
// DON'T GENERATE ANY HPD FOR PORT_A but reboot to allow this eDP info to persist
// reboot the system to allow simulated EDP to come up from persistence database
BOOLEAN COMMONRXHANDLERS_SetRxInfo(PPORT_INFO pstPortInfo, PRX_INFO_ARR pstRxInfoArr)
{
    BOOLEAN bRet = FALSE;

    GFXVALSIM_FUNC_ENTRY();
    GFXVALSIM_DBG_MSG("Initializing: %lu", pstPortInfo->ulPortNum);
    do
    {
        if (pstRxInfoArr == NULL || pstPortInfo == NULL)
        {
            break;
        }

        // Cleanup any previous instantiation of pstRxInfoArr as it is called only once after SIM driver load
        // This worked perfectly well in the first implementation where all ports were configured in one shot and
        // cleanup was done in one shot (the original call was COMMRXHANDLERS_CleanUp(pstRxInfoArr))
        // In this current implementation Port B for example could be configured for DP first and then for HDMI
        // but DPPOrt and HDMIPOrt enum values are different so the objects for both would reside at different indicies
        // in the pstRxInfoArr object array and the purpose of this pre cleanup would be somewhat defeated
        if (FALSE == COMMRXHANDLERS_CleanUpPort(pstRxInfoArr, pstPortInfo->ulPortNum))
        {
            break;
        }

        pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].ePortNum = pstPortInfo->ulPortNum;
        pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].eRxType  = pstPortInfo->eRxTypes;

        if (pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].eRxType == DP)
        {

            pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].pstDPAuxInterface =
            DPHANDLERS_DPInterfaceInit(pstRxInfoArr, pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].ePortNum);

            if (pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].pstDPAuxInterface == NULL)
            {
                break;
            }
        }
        else if (pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].eRxType == HDMI)
        {
            pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].pstHDMIInterface =
            HDMIHANDLERS_HDMIInterfaceInit(pstRxInfoArr, pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].ePortNum);
            if (pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].pstHDMIInterface == NULL)
            {
                break;
            }
        }

        pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].eSinkPluggedState = pstPortInfo->eInitialPlugState;

        if (DP == pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].eRxType)
        {
            if (pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].eSinkPluggedState == eSinkPlugged)
            {
                pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].pstDPAuxInterface->bSinkPluggedState = TRUE;
            }
            else
            {
                pstRxInfoArr->stRxInfoObj[pstRxInfoArr->ulNumEnumeratedPorts].pstDPAuxInterface->bSinkPluggedState = FALSE;
            }
        }

        pstRxInfoArr->ulNumEnumeratedPorts++;

        bRet = TRUE;

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

PDPAUX_INTERFACE COMMRXHANDLERS_GetAuxInterfaceFromPortType(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType)
{
    PDPAUX_INTERFACE pstDPAuxInterface = NULL;
    ULONG            ulCount           = 0;

    GFXVALSIM_FUNC_ENTRY();

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {

        if (pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == ePortType && pstRxInfoArr->stRxInfoObj[ulCount].eRxType == DP)
        {
            pstDPAuxInterface = pstRxInfoArr->stRxInfoObj[ulCount].pstDPAuxInterface;

            break;
        }
    }

    GFXVALSIM_FUNC_EXIT((pstDPAuxInterface == NULL) ? 1 : 0);
    return pstDPAuxInterface;
}

RX_TYPE COMMRXHANDLERS_GetRxTypeFromPortType(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType)
{
    ULONG   ulCount = 0;
    RX_TYPE eRxType = RxInvalidType;

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {

        if (pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == ePortType)
        {
            eRxType = pstRxInfoArr->stRxInfoObj[ulCount].eRxType;
            break;
        }
    }

    return eRxType;
}

PHDMI_INTERFACE COMMRXHANDLERS_GetHDMIInterfaceFromPortType(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType)
{
    PHDMI_INTERFACE pstHDMIInterface = NULL;
    ULONG           ulCount          = 0;

    GFXVALSIM_FUNC_ENTRY();

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {

        if (pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == ePortType && pstRxInfoArr->stRxInfoObj[ulCount].eRxType == HDMI)
        {
            pstHDMIInterface = pstRxInfoArr->stRxInfoObj[ulCount].pstHDMIInterface;
            break;
        }
    }

    GFXVALSIM_FUNC_EXIT((pstHDMIInterface == NULL) ? 1 : 0);
    return pstHDMIInterface;
}

// Implementation Notes:
// The EDID IOCTL handler is in the common file because the same IOCTL would be used to set EDID data for any
// Display type e.g. HDMI, DP etc. From here the Display Type specific Handlers would be called
BOOLEAN COMMRXHANDLERS_SetEDIDData(PRX_INFO_ARR pstRxInfoArr, PFILE_DATA pstEdidData, BOOLEAN bIsEDIDForS3S4Cycle)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    GFXVALSIM_FUNC_ENTRY();

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == (PORT_TYPE)pstEdidData->uiPortNum)
        {
            if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == DP || pstRxInfoArr->stRxInfoObj[ulCount].eRxType == DP)
            {
                if (bIsEDIDForS3S4Cycle)
                {
                    bRet = DPHANDLERS_SetEDIDDataForS3S4Cycle(pstRxInfoArr, pstEdidData);
                }
                else
                {
                    bRet = DPHANDLERS_SetEDIDData(pstRxInfoArr, pstEdidData);
                }

                break;
            }
            else if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == HDMI)
            {
                if (bIsEDIDForS3S4Cycle)
                {
                    bRet = HDMIHANDLERS_SetEDIDDataForS3S4Cycle(pstRxInfoArr, pstEdidData);
                }
                else
                {
                    bRet = HDMIHANDLERS_SetEDIDData(pstRxInfoArr, pstEdidData);
                }

                break;
            }
        }
    }

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

BOOLEAN COMMRXHANDLERS_SetPortPluggedState(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, SINK_PLUGGED_STATE eSinkPluggedState, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    GFXVALSIM_FUNC_ENTRY();

    // For HDMI Unplug, free the allocated EDID memory

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {
        if ((ePortType == pstRxInfoArr->stRxInfoObj[ulCount].ePortNum))
        {
            if (HDMI == pstRxInfoArr->stRxInfoObj[ulCount].eRxType && eSinkPlugged == pstRxInfoArr->stRxInfoObj[ulCount].eSinkPluggedState && eSinkUnplugged == eSinkPluggedState)
            {
                HDMIHANDLERS_EDID_SCDC_CleanUp(pstRxInfoArr->stRxInfoObj[ulCount].pstHDMIInterface, ePortType);
            }

            // NOTE:
            // For DP, The DP Handlers are not cleaned after unplug
            // The reason being to handle the Stress Case Scenario of Plug-->Unplug infinite times

            // Update the plug status
            pstRxInfoArr->stRxInfoObj[ulCount].eSinkPluggedState = eSinkPluggedState;
            // This is to keep track of the AUX Transcation for Sink
            // Reply for AUX Transcations will not be responded if Sink is not Plugged
            if (DP == pstRxInfoArr->stRxInfoObj[ulCount].eRxType)
            {
                if (eSinkPluggedState == eSinkPlugged)
                {
                    pstRxInfoArr->stRxInfoObj[ulCount].pstDPAuxInterface->bSinkPluggedState = TRUE;
                }
                else
                {
                    pstRxInfoArr->stRxInfoObj[ulCount].pstDPAuxInterface->bSinkPluggedState = FALSE;
                }
            }

            // Update the Connector Info like TC/TBT
            pstRxInfoArr->stRxInfoObj[ulCount].uPortConnectorInfo = PortConnectorInfo;

            bRet = TRUE;
            break;
        }
    }

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet; // bRet == FALSE =>> Invalid Port
}

PRX_S3S4_PLUGUNPLUG_DATA COMMRXHANDLERS_GetRxS3S4PlugUnPlugDataPtr(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, RX_TYPE eRxType)
{
    PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData = NULL;
    ULONG                    ulCount                 = 0;

    GFXVALSIM_FUNC_ENTRY();

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {

        if (pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == ePortType && pstRxInfoArr->stRxInfoObj[ulCount].eRxType == DP)
        {
            pstRxS3S4PlugUnPlugData = &pstRxInfoArr->stRxInfoObj[ulCount].stRxS3S4PlugUnplugData;

            break;
        }

        if (pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == ePortType && pstRxInfoArr->stRxInfoObj[ulCount].eRxType == HDMI)
        {
            pstRxS3S4PlugUnPlugData = &pstRxInfoArr->stRxInfoObj[ulCount].stRxS3S4PlugUnplugData;

            break;
        }
    }

    GFXVALSIM_FUNC_EXIT((pstRxS3S4PlugUnPlugData == NULL) ? 1 : 0);
    return pstRxS3S4PlugUnPlugData;
}

BOOLEAN COMMRXHANDLERS_ConfigureAllPortsGfxS3S4PlugUnplugData(PRX_INFO_ARR pstRxInfoArr, PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA pstGfxS3S4AllPortsPlugUnplugData)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;
    RX_TYPE eRxType = RxInvalidType;

    GFXVALSIM_FUNC_ENTRY();

    do
    {
        if (pstGfxS3S4AllPortsPlugUnplugData == NULL)
        {
            break;
        }

        for (ulCount = 0; ulCount < pstGfxS3S4AllPortsPlugUnplugData->ulNumPorts; ulCount++)
        {

            eRxType = COMMRXHANDLERS_GetRxTypeFromPortType(pstRxInfoArr, pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount].ulPortNum);

            COMMRXHANDLERS_SetConnectorInfo(pstRxInfoArr, pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount].ulPortNum,
                                            pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount].uConnectorInfoAfterResume);

            if (eRxType == DP)
            {
                bRet = DPHANDLERS_ConfigureDPGfxS3S4PlugUnplugData(pstRxInfoArr, &pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount]);
            }
            else if (eRxType == HDMI)
            {
                bRet = HDMIHANDLERS_ConfigureDPGfxS3S4PlugUnplugData(pstRxInfoArr, &pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount]);
            }
        }

        bRet = TRUE;

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN COMMRXHANDLERS_GfxPowerStateNotification(PRX_INFO_ARR pstRxInfoArr, DEVICE_POWER_STATE eGfxPowerState, POWER_ACTION eActionType)
{
    PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData = NULL;
    ULONG                    ulCount                 = 0;
    BOOLEAN                  bRet                    = FALSE;

    GFXVALSIM_FUNC_ENTRY();
    GFXVALSIM_GFX_POWER_STATE_NOTIFICATION(pstRxInfoArr->pstMMIOInterface->eIGFXPlatform, eGfxPowerState, eActionType);
    do
    {
        if (pstRxInfoArr == NULL)
        {
            break;
        }

        for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
        {
            pstRxS3S4PlugUnPlugData = &pstRxInfoArr->stRxInfoObj[ulCount].stRxS3S4PlugUnplugData;

            if (pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest != ePlugRequestInvalid)
            {
                if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == DP)
                {
                    bRet = DPHANDLERS_HandleGfxPowerNotification(pstRxInfoArr, pstRxInfoArr->stRxInfoObj[ulCount].ePortNum, pstRxS3S4PlugUnPlugData, eGfxPowerState, eActionType,
                                                                 pstRxInfoArr->stRxInfoObj[ulCount].uPortConnectorInfo);
                }
                else if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == HDMI)
                {
                    bRet = HDMIHANDLERS_HandleGfxPowerNotification(pstRxInfoArr, pstRxInfoArr->stRxInfoObj[ulCount].ePortNum, pstRxS3S4PlugUnPlugData, eGfxPowerState, eActionType,
                                                                   pstRxInfoArr->stRxInfoObj[ulCount].uPortConnectorInfo);
                }
            }
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

void COMMRXHANDLERS_FreeAuxInterfaceForPort(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType)
{
    ULONG             ulCount       = 0;
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {

        if (pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == ePortType && pstRxInfoArr->stRxInfoObj[ulCount].eRxType == DP)
        {
            if (pstRxInfoArr->stRxInfoObj[ulCount].pstDPAuxInterface)
            {
                pstPortingObj->pfnFreeMem(pstRxInfoArr->stRxInfoObj[ulCount].pstDPAuxInterface);
                pstRxInfoArr->stRxInfoObj[ulCount].pstDPAuxInterface = NULL;
            }

            break;
        }
    }
}

BOOLEAN COMMRXHANDLERS_CleanUpPort(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortNum)
{
    BOOLEAN bRet    = TRUE;
    ULONG   ulCount = 0;

    GFXVALSIM_FUNC_ENTRY();

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == ePortNum)
        {
            if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == DP)
            {
                // For a more streamlined design, this clean up has to be done through the cleanup Routine of the
                // MMIO hanler for Aux. Maybe do this later?
                bRet = DPHANDLERS_CleanUp(pstRxInfoArr, pstRxInfoArr->stRxInfoObj[ulCount].ePortNum);
            }
            else if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == HDMI)
            {
                bRet = HDMIHANDLERS_CleanUp(pstRxInfoArr, pstRxInfoArr->stRxInfoObj[ulCount].ePortNum);
            }

            if (bRet == TRUE)
            {
                pstRxInfoArr->ulNumEnumeratedPorts--;

                // Now left shift in the array to replace the cleaned up index
                for (; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
                {
                    pstRxInfoArr->stRxInfoObj[ulCount] = pstRxInfoArr->stRxInfoObj[ulCount + 1];
                }

                break;
            }
        }
    }
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN COMMRXHANDLERS_CleanUpAllPorts(PRX_INFO_ARR pstRxInfoArr)
{
    BOOLEAN bRet    = TRUE;
    ULONG   ulCount = 0;

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == DP)
        {
            // For a more streamlined design, this clean up has to be done through the cleanup Routine of the
            // MMIO hanler for Aux. Maybe do this later?
            bRet = DPHANDLERS_CleanUp(pstRxInfoArr, pstRxInfoArr->stRxInfoObj[ulCount].ePortNum);
        }
        else if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == HDMI)
        {
            bRet = HDMIHANDLERS_CleanUp(pstRxInfoArr, pstRxInfoArr->stRxInfoObj[ulCount].ePortNum);
        }
    }

    pstRxInfoArr->ulNumEnumeratedPorts = 0;

    return bRet;
}

//////////////////////////////////////////////////////////
//
// Get the Connector Info like TC/TBT
// Parameters:
// pstRxInfoArr: Pointer to structure RX_INFO_ARR
// ePortType: Port Number
// Iterate through the RX_INFO_OBJ array and
// return the Connector Info for matching Port Number
//////////////////////////////////////////////////////////
PORT_CONNECTOR_INFO COMMRXHANDLERS_GetConnectorInfo(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType)
{
    PORT_CONNECTOR_INFO PortConnectorInfo = {
        0,
    };
    ULONG ulCount = 0;

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {
        if ((ePortType == pstRxInfoArr->stRxInfoObj[ulCount].ePortNum))
        {
            // Update the Connector Info like TC/TBT
            PortConnectorInfo = pstRxInfoArr->stRxInfoObj[ulCount].uPortConnectorInfo;
            break;
        }
    }

    return PortConnectorInfo;
}

//////////////////////////////////////////////////////////
//
// Set the Connector Info like TC/TBT
// Parameters:
// pstRxInfoArr: Pointer to structure RX_INFO_ARR
// ePortType: Port Number
// PortConnectorInfo: this is OUT parameter.
// Iterate through the RX_INFO_OBJ array and
// update the Connector Info for matching Port Number
//////////////////////////////////////////////////////////
BOOLEAN COMMRXHANDLERS_SetConnectorInfo(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    ULONG   ulCount = 0;
    BOOLEAN bRet    = FALSE;

    for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
    {

        if (pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == ePortType)
        {
            pstRxInfoArr->stRxInfoObj[ulCount].uPortConnectorInfo = PortConnectorInfo;
            bRet                                                  = TRUE;
            break;
        }
    }

    return bRet;
}

//////////////////////////////////////////////////////////
//
// Set the DongleType
// Parameters:
// pstRxInfoArr: Pointer to structure RX_INFO_ARR
// ePortType: Port Number
// Iterate through the RX_INFO_OBJ array and
// update the DongleType Info for matching Port Number
//////////////////////////////////////////////////////////
BOOLEAN COMMRXHANDLERS_SetDongleType(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, DONGLE_TYPE eDongleType)
{
    ULONG   ulCount = 0;
    BOOLEAN bRet    = FALSE;
    do
    {
        if (NULL == pstRxInfoArr)
        {
            GFXVALSIM_DBG_MSG("pstRxInfoArr is NULL.");
            break;
        }

        for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
        {
            if (pstRxInfoArr->stRxInfoObj[ulCount].ePortNum == ePortType)
            {
                if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == HDMI)
                {
                    bRet = HDMIHANDLERS_SetDongleType(pstRxInfoArr, ePortType, eDongleType);
                    break;
                }
                else if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == DP)
                {
                    bRet = TRUE;
                }
            }
        }

    } while (FALSE);

    return bRet;
}

//////////////////////////////////////////////////////////
//
// Set panel DPCD data
// Parameters:
// pstRxInfoArr: pointer to Rx_info array
// ePortType: Port Number
// Offset: DPCD offset
// Value : DPCD value
// update the dpcd data for the given Port Number
//////////////////////////////////////////////////////////
BOOLEAN COMMRXHANDLERS_SetPanelDpcd(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, UINT16 Offset, UINT8 Value)
{
    GFXVALSIM_FUNC_ENTRY();
    BOOLEAN bRet = FALSE;
    do
    {
        if (NULL == pstRxInfoArr)
            break;

        bRet = DPHANDLERS_SetPanelDpcd(pstRxInfoArr, ePortType, Offset, Value);
    } while (FALSE);
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}
