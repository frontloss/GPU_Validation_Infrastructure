#include "PersistenceHandler.h"
#include "..\DriverInterfaces\SimDriver.h"
#include "..\DriverInterfaces\SimDrvToGfx.h"
#include "..\DriverInterfaces\\CommonIOCTL.h"
#include "..\\CommonInclude\\ETWLogging.h"

BOOLEAN PERSISTENCEHANDLER_InitPeristenceContext(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSIMDRV_PERSISTENCE_DATA *ppstPersistenceData,
                                                 PSIMDRV_PERSISTENCE_DATA *ppstPersistenceDataS3S4)
{
    BOOLEAN                  status                 = FALSE;
    PSIMDRV_PERSISTENCE_DATA pstPersistenceData     = NULL;
    PSIMDRV_PERSISTENCE_DATA pstPersistenceDataS3S4 = NULL;
    PSIMDRVGFX_CONTEXT       pstSimDrvGfxContext    = NULL;
    PGFX_ADAPTER_CONTEXT     pTempGfxAdapterContext = NULL;

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
            /* Assign Existing pointer */
            *ppstPersistenceData     = pTempGfxAdapterContext->pvSimPersistenceData;
            *ppstPersistenceDataS3S4 = pTempGfxAdapterContext->pvSimPersistenceDataS3S4;
            status                   = TRUE;
        }
        else
        {
            pstPersistenceData = pstPortingObj->pfnAllocateMem(sizeof(SIMDRV_PERSISTENCE_DATA), TRUE);
            if (NULL == pstPersistenceData)
                break;

            pstPersistenceDataS3S4 = pstPortingObj->pfnAllocateMem(sizeof(SIMDRV_PERSISTENCE_DATA), TRUE);
            if (NULL == pstPersistenceDataS3S4)
                break;

            *ppstPersistenceData     = pstPersistenceData;
            *ppstPersistenceDataS3S4 = pstPersistenceDataS3S4;
            status                   = TRUE;
        }

    } while (FALSE);
    return status;
}

BOOLEAN PERSISTENCEHANDLER_CleanupPeristenceContext(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PSIMDRV_PERSISTENCE_DATA pstPersistenceDataS3S4)
{
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    if (NULL == pstPortingObj)
        return FALSE;

    if (pstPersistenceData)
    {
        pstPortingObj->pfnFreeMem(pstPersistenceData);
    }

    if (pstPersistenceDataS3S4)
    {
        pstPortingObj->pfnFreeMem(pstPersistenceDataS3S4);
    }
    return TRUE;
}

BOOLEAN PERSISTENCEHANDLER_SetRxInfo(PPORT_INFO pstPortInfo, PSIMDRV_PERSISTENCE_DATA pstPersistenceData)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;
    GFXVALSIM_FUNC_ENTRY();

    do
    {
        if (pstPersistenceData == NULL || pstPortInfo == NULL)
        {
            break;
        }

        // Cleanup any previous persistence Data
        if (FALSE == PERSISTENCEHANDLER_CleanUpPort(pstPersistenceData, pstPortInfo->ulPortNum))
        {
            break;
        }

        pstPersistenceData->stPortPersistenceData[pstPersistenceData->ulNumEnumeratedPorts].ulPortNum         = pstPortInfo->ulPortNum;
        pstPersistenceData->stPortPersistenceData[pstPersistenceData->ulNumEnumeratedPorts].eRxType           = pstPortInfo->eRxTypes;
        pstPersistenceData->stPortPersistenceData[pstPersistenceData->ulNumEnumeratedPorts].eSinkPluggedState = pstPortInfo->eInitialPlugState;

        pstPersistenceData->ulNumEnumeratedPorts++;

        bRet = TRUE;

    } while (FALSE);
    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_SetDongleType(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PORT_TYPE ePortType, DONGLE_TYPE eDongleType)
{
    GFXVALSIM_FUNC_ENTRY();
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;

    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum == ePortType)
        {
            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == HDMI)
            {
                pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.uiDongleType = eDongleType;
                bRet                                                                                  = TRUE;
            }
            else
            {
                bRet = TRUE;
            }
            break;
        }
    }
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

// Implementation Notes:
// The EDID IOCTL handler is in the common file because the same IOCTL would be used to set EDID data for any
// Display type e.g. HDMI, DP etc. From here the Display Type specific Handlers would be called
BOOLEAN PERSISTENCEHANDLER_SetEDIDData(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PFILE_DATA pstEdidData)
{
    GFXVALSIM_FUNC_ENTRY();
    BOOLEAN           bRet            = FALSE;
    ULONG             ulCount         = 0;
    ULONG             ulNumMSTEDIDs   = 0;
    PFILE_DATA        pstTempEdidData = NULL;
    PPORTINGLAYER_OBJ pstPortingObj   = GetPortingObj();

    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum == pstEdidData->uiPortNum)
        {
            pstTempEdidData = pstPortingObj->pfnAllocateMem((sizeof(FILE_DATA) + pstEdidData->uiDataSize), TRUE);

            if (pstTempEdidData == NULL)
            {
                break;
            }

            memcpy_s(pstTempEdidData, (sizeof(FILE_DATA) + pstEdidData->uiDataSize), pstEdidData, (sizeof(FILE_DATA) + pstEdidData->uiDataSize));

            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == HDMI)
            {
                // We need to clear the previous EDID data before setting up a new one
                // assuming App is trying to set up another HDMI Panel
                if (pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData)
                {
                    pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData);
                }

                pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData = pstTempEdidData;
                bRet                                                                                 = TRUE;
                break;
            }
            else
            {
                if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
                {
                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eInvalidTopology)
                    {
                        GFXVALSIM_DBG_MSG("Invalid Topology passed.");
                        break;
                    }
                    else if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eDPMST)
                    {
                        // For EDP/SST ulNumMSTDPCDs is always Zero i.e we only use the first indext
                        ulNumMSTEDIDs = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs;

                        if (ulNumMSTEDIDs == MAX_NUM_DISPLAYS)
                        {
                            GFXVALSIM_DBG_MSG("Max MST EDID's  %d reached.", MAX_NUM_DISPLAYS);
                            // This means that a proper reset didn't happen using DPHANDLERS_SetDPTopologyType call
                            // Or App world is trying to allocate more EDID for an MST topology than currently supported
                            break;
                        }
                    }
                }

                if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulNumMSTEDIDs])
                {
                    pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulNumMSTEDIDs]);
                }

                pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulNumMSTEDIDs] = pstTempEdidData;
                pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs                 = ulNumMSTEDIDs + 1;

                bRet = TRUE;
                break;
            }
        }
    }

    if (bRet == FALSE && pstTempEdidData)
    {
        pstPortingObj->pfnFreeMem(pstTempEdidData);
    }
    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_InitDPTopologyType(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PDP_INIT_INFO pstDPInitInfo)
{
    GFXVALSIM_FUNC_ENTRY();
    BOOLEAN           bRet          = FALSE;
    ULONG             ulCount       = 0;
    ULONG             ulCount2      = 0;
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum == pstDPInitInfo->uiPortNum)
        {
            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
            {
                // Since the topology is switching from MST to SST or SST to MST i.e. a fresh topology so invalidate all the
                // Stored DPCDs and EDIDs on this Port
                if ((pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType != pstDPInitInfo->eTopologyType) &&
                    (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType != eInvalidTopology))
                {
                    // We need to free all the EDID buffer since the EDID of the displays in the next topology might of of different size
                    // and hence would need a buffer of a different size
                    for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs; ulCount2++)
                    {
                        pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2]);
                        pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2] = NULL;
                    }

                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs = 0;

                    for (ulCount2 = 1; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs; ulCount2++)
                    {
                        // Don't free the first DPCD buffer as DPCD buffer sizes are fixed by the SimDriver. Currently fixed to 0x1000
                        // This would save us from reallocating one buffer extra needlessly when calls for SetDPCDData come
                        pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2]);
                        pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2] = NULL;
                    }

                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs = 0;

                    // TODO: uncomment below code once DP userspace DLL starts sending DPCDModelData also when doing topology switching
                    /*for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas; ulCount2++)
                    {
                        if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2])
                        {
                            pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2]);
                            pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2] = NULL;
                        }
                    }

                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas = 0;*/
                }

                pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType = pstDPInitInfo->eTopologyType;

                bRet = TRUE;
                break;
            }
        }
    }
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_SetDPCDData(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PFILE_DATA pstDPCDData)
{
    GFXVALSIM_FUNC_ENTRY();
    BOOLEAN           bRet            = FALSE;
    ULONG             ulCount         = 0;
    ULONG             ulNumMSTDPCDs   = 0;
    PFILE_DATA        pstTempDPCDData = NULL;
    PPORTINGLAYER_OBJ pstPortingObj   = GetPortingObj();

    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum == pstDPCDData->uiPortNum)
        {

            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
            {
                if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eInvalidTopology)
                {
                    GFXVALSIM_DBG_MSG("Topology is invalid for SetDPCDData");
                    break;
                }
                else if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eDPMST)
                {
                    // For EDP/SST ulNumMSTDPCDs is always Zero i.e we only use the first indext
                    ulNumMSTDPCDs = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs;

                    if (ulNumMSTDPCDs == (MAX_NUM_DISPLAYS + MAX_NUM_BRANCHES))
                    {
                        GFXVALSIM_DBG_MSG("Allocated extra EDID for MST topology than required");
                        // This means that a proper reset didn't happen using DPHANDLERS_SetDPTopologyType call
                        // Or App world is trying to allocate more EDID for an MST topology than currently supported
                        break;
                    }
                }
            }

            if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulNumMSTDPCDs])
            {
                pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulNumMSTDPCDs]);
            }

            pstTempDPCDData = pstPortingObj->pfnAllocateMem((sizeof(FILE_DATA) + pstDPCDData->uiDataSize), TRUE);

            if (pstTempDPCDData == NULL)
            {
                break;
            }

            memcpy_s(pstTempDPCDData, (sizeof(FILE_DATA) + pstDPCDData->uiDataSize), pstDPCDData, (sizeof(FILE_DATA) + pstDPCDData->uiDataSize));
            pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulNumMSTDPCDs] = pstTempDPCDData;
            pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs                 = ulNumMSTDPCDs + 1;
            bRet                                                                                              = TRUE;
            break;
        }
    }
    if (bRet == FALSE && pstTempDPCDData)
    {
        pstPortingObj->pfnFreeMem(pstTempDPCDData);
    }
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_SetDPCDModelData(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PDP_DPCD_MODEL_DATA pstDpDPCDModelData)
{
    GFXVALSIM_FUNC_ENTRY();

    BOOLEAN             bRet                   = FALSE;
    ULONG               ulCount                = 0;
    ULONG               ulNumMSTDPCDModelDatas = 0;
    PDP_DPCD_MODEL_DATA pstTempDpDPCDModelData = NULL;
    PPORTINGLAYER_OBJ   pstPortingObj          = GetPortingObj();

    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum == pstDpDPCDModelData->uiPortNum)
        {
            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
            {
                if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eInvalidTopology)
                {
                    break;
                }
                else if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eDPMST)
                {
                    // For EDP/SST ulNumMSTDPCDs is always Zero i.e we only use the first indext
                    ulNumMSTDPCDModelDatas = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas;

                    if (ulNumMSTDPCDModelDatas == (MAX_NUM_DISPLAYS + MAX_NUM_BRANCHES))
                    {
                        // This means that a proper reset didn't happen using DPHANDLERS_SetDPTopologyType call
                        // Or App world is trying to allocate more EDID for an MST topology than currently supported
                        break;
                    }
                }
            }

            if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulNumMSTDPCDModelDatas] == NULL)
            {
                pstTempDpDPCDModelData = pstPortingObj->pfnAllocateMem(sizeof(DP_DPCD_MODEL_DATA), TRUE);

                if (pstTempDpDPCDModelData == NULL)
                {
                    break;
                }
            }
            else
            {
                pstTempDpDPCDModelData = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulNumMSTDPCDModelDatas];
            }

            memcpy_s(pstTempDpDPCDModelData, sizeof(DP_DPCD_MODEL_DATA), pstDpDPCDModelData, sizeof(DP_DPCD_MODEL_DATA));
            pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulNumMSTDPCDModelDatas] = pstTempDpDPCDModelData;
            pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas                        = ulNumMSTDPCDModelDatas + 1;
            bRet                                                                                                              = TRUE;
        }
    }

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_SetDPMSTTopology(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PBRANCHDISP_DATA_ARRAY pstBranchDispDataArr)
{
    BOOLEAN                bRet                    = FALSE;
    ULONG                  ulCount                 = 0;
    PPORTINGLAYER_OBJ      pstPortingObj           = GetPortingObj();
    PBRANCHDISP_DATA_ARRAY pstTempBranchDispDataAr = NULL;
    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum == pstBranchDispDataArr->uiPortNum)
        {
            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP && pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eDPMST)
            {
                pstTempBranchDispDataAr = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray;

                if (pstTempBranchDispDataAr == NULL)
                {
                    pstTempBranchDispDataAr = pstPortingObj->pfnAllocateMem(sizeof(BRANCHDISP_DATA_ARRAY), TRUE);
                }

                if (pstTempBranchDispDataAr == NULL)
                {
                    break;
                }

                memcpy_s(pstTempBranchDispDataAr, sizeof(BRANCHDISP_DATA_ARRAY), pstBranchDispDataArr, sizeof(BRANCHDISP_DATA_ARRAY));
                pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray = pstTempBranchDispDataAr;
                bRet                                                                                          = TRUE;
                break;
            }
        }
    }

    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_UpdateMSTTopologyToPersist(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PRX_INFO_ARR pstRxInfoArr, PDP_SUBTOPOLOGY_ARGS pstCSNArgs)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;
    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum == pstCSNArgs->ulPortNum && pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP &&
            pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eDPMST)
        {
            GFXVALSIM_DBG_MSG("PERSISTENCEHANDLER_UpdateMSTTopologyToPersist %lu", ulCount);
            bRet = DPHANDLERS_ExtractCurrentTopologyInArrayFormat(pstRxInfoArr, pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray,
                                                                  pstCSNArgs->ulPortNum);
        }
    }

    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_UpdatePortPluggedState(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, ULONG ulPortNum, SINK_PLUGGED_STATE eSinkPluggedState,
                                                  PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN bRet    = FALSE;
    ULONG   ulCount = 0;
    GFXVALSIM_FUNC_ENTRY();

    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum == ulPortNum)
        {
            pstPersistenceData->stPortPersistenceData[ulCount].eSinkPluggedState = eSinkPluggedState;
            // Update the Connctor Info like TC/TBT
            pstPersistenceData->stPortPersistenceData[ulCount].uPortConnectorInfo = PortConnectorInfo;
            bRet                                                                  = TRUE;
        }
    }
    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_ConfigurePeristenceForS3S4Path(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PRX_INFO_ARR pstRxInfoArr,
                                                          PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA pstGfxS3S4AllPortsPlugUnplugData)
{
    BOOLEAN bRet    = TRUE;
    ULONG   ulCount = 0;

    pstPersistenceData->ulNumEnumeratedPorts = pstGfxS3S4AllPortsPlugUnplugData->ulNumPorts;

    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        pstPersistenceData->stPortPersistenceData[ulCount].eRxType =
        COMMRXHANDLERS_GetRxTypeFromPortType(pstRxInfoArr, pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount].ulPortNum);

        // Update the Connector Info
        pstPersistenceData->stPortPersistenceData[ulCount].uPortConnectorInfo =
        COMMRXHANDLERS_GetConnectorInfo(pstRxInfoArr, pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount].ulPortNum);

        pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum = pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount].ulPortNum;

        pstPersistenceData->stPortPersistenceData[ulCount].eSinkPluggedState = pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount].eSinkPlugReq;

        if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
        {
            GFXVALSIM_DBG_MSG("Setting topology %d for RxType: %d, and portnum: %d",
                              pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount].stS3S4DPPlugUnplugData.eTopologyAfterResume,
                              pstPersistenceData->stPortPersistenceData[ulCount].eRxType, pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum);

            pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType =
            pstGfxS3S4AllPortsPlugUnplugData->stS3S4PortPlugUnplugData[ulCount].stS3S4DPPlugUnplugData.eTopologyAfterResume;
        }
    }

    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_UpdatePeristenceWithS3S4ResumeData(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PSIMDRV_PERSISTENCE_DATA pstPersistenceDataS3S4,
                                                              PRX_INFO_ARR pstRxInfoArr, DEVICE_POWER_STATE eGfxPowerState, POWER_ACTION eActionType)
{
    BOOLEAN bRet     = TRUE;
    ULONG   ulCount  = 0;
    ULONG   ulCount2 = 0;

    if (eGfxPowerState == PowerDeviceD0)
    {
        for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
        {
            for (ulCount2 = 0; ulCount < pstPersistenceDataS3S4->ulNumEnumeratedPorts; ulCount2++)
            {
                if (pstPersistenceDataS3S4->stPortPersistenceData[ulCount2].eSinkPluggedState == eSinkPlugged &&
                    pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum == pstPersistenceDataS3S4->stPortPersistenceData[ulCount2].ulPortNum)
                {
                    pstPersistenceData->stPortPersistenceData[ulCount] = pstPersistenceDataS3S4->stPortPersistenceData[ulCount2];

                    if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP &&
                        pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eDPMST)
                    {
                        bRet =
                        DPHANDLERS_ExtractCurrentTopologyInArrayFormat(pstRxInfoArr, pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray,
                                                                       pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum);
                    }
                }
            }
        }
    }

    return bRet;
}
// Two ways to write data to the disk. Either write to disk chunk by chunk via multiple file writes
// or write to a buffer in memory first and then write to the write that buffer to disk file in one shot via a single disk file write
// Going with first approach expecting OS to optimize disk operations.
// Additional checks can be put in the function to check the expected file sizes before writing to the Persistence file
BOOLEAN PERSISTENCEHANDLER_WritePeristenceDataToDisk(PSIMDRV_PERSISTENCE_DATA pstPersistenceData)
{
    BOOLEAN           bRet               = FALSE;
    ULONG             ulCount            = 0;
    ULONG             ulCount2           = 0;
    ULONG             ulWriteOffset      = 0;
    PUCHAR            pucPersistenceBuff = NULL;
    PFILE_DATA        pstFileData        = NULL;
    ULONG             ulFileSize;
    PULONG            pulNumPluggedPorts   = 0;
    PPORTINGLAYER_OBJ pstPortingObj        = GetPortingObj();
    UCHAR             ucSignatureHeader[8] = SIGNATURE_HEADER;
    UCHAR             ucSignatureFooter[8] = SIGNATURE_FOOTER;
    // const SIZE_T sizeofT = sizeof(DP_DPCD_MODEL_DATA);
    // Calculate Persistence Data size

    // A display EID will take around 1/2 KB for 4 blocks. So around 30 Displays = 15KB
    // A DPCD in current SimDrv config will take 4kb each. So 45 DPCDs =  114 KB
    // As per current definition of DP_DPCD_MODEL_DATA structure, it is 836 bytes size. So for 45 DPCDs, its ~= 38KB
    // Plus other data   = 4kb
    // So 240kb data allocation should work in most cases //60 4k Pages

    // Lets allocate 240kb then
    pucPersistenceBuff = pstPortingObj->pfnAllocateMem((240 * 1024), TRUE);

    if (pucPersistenceBuff)
    {
        memcpy_s(((PPERSISTENCE_INFO_HEADER)pucPersistenceBuff)->ucSignatureHeader, 8, ucSignatureHeader, 8);

        ulWriteOffset = sizeof(PERSISTENCE_INFO_HEADER);

        // Initialize the persistence file size of the default value of sizeof(PERSISTENCE_INFO_HEADER).
        // This is the default value when no port has been intialized
        ((PPERSISTENCE_INFO_HEADER)pucPersistenceBuff)->ulPeristenceDataSize = ulWriteOffset;

        pulNumPluggedPorts = ((PULONG)(pucPersistenceBuff + ulWriteOffset));

        *pulNumPluggedPorts = 0;

        ulWriteOffset += sizeof(ULONG);

        for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
        {
            *pulNumPluggedPorts = *pulNumPluggedPorts + 1;

            *((PULONG)(pucPersistenceBuff + ulWriteOffset)) = pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum;
            ulWriteOffset += sizeof(ULONG);
            *((PULONG)(pucPersistenceBuff + ulWriteOffset)) = pstPersistenceData->stPortPersistenceData[ulCount].eRxType;
            ulWriteOffset += sizeof(RX_TYPE);
            memcpy_s((pucPersistenceBuff + ulWriteOffset), sizeof(PORT_CONNECTOR_INFO), &pstPersistenceData->stPortPersistenceData[ulCount].uPortConnectorInfo,
                     sizeof(PORT_CONNECTOR_INFO));
            ulWriteOffset += sizeof(PORT_CONNECTOR_INFO);
            *((PULONG)(pucPersistenceBuff + ulWriteOffset)) = pstPersistenceData->stPortPersistenceData[ulCount].eSinkPluggedState;
            ulWriteOffset += sizeof(SINK_PLUGGED_STATE);

            if (pstPersistenceData->stPortPersistenceData[ulCount].eSinkPluggedState != eSinkPlugged)
            {
                continue; // If display is not eSinkPlugged, edid and dpcd will not be present. So, skip next steps.
            }

            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
            {
                *((DP_TOPOLOGY_TYPE *)(pucPersistenceBuff + ulWriteOffset)) = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType;
                ulWriteOffset += sizeof(DP_TOPOLOGY_TYPE);

                *((PULONG)(pucPersistenceBuff + ulWriteOffset)) = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs;
                ulWriteOffset += sizeof(ULONG);

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs; ulCount2++)
                {
                    pstFileData = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2];
                    ulFileSize  = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2]->uiDataSize;
                    memcpy_s((pucPersistenceBuff + ulWriteOffset), (ulFileSize + sizeof(FILE_DATA)), pstFileData, (ulFileSize + sizeof(FILE_DATA)));
                    ulWriteOffset += ulFileSize + sizeof(FILE_DATA);
                }

                *((PULONG)(pucPersistenceBuff + ulWriteOffset)) = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs;
                ulWriteOffset += sizeof(ULONG);

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs; ulCount2++)
                {
                    pstFileData = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2];
                    ulFileSize  = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2]->uiDataSize;
                    memcpy_s((pucPersistenceBuff + ulWriteOffset), (ulFileSize + sizeof(FILE_DATA)), pstFileData, (ulFileSize + sizeof(FILE_DATA)));
                    ulWriteOffset += ulFileSize + sizeof(FILE_DATA);
                }

                *((PULONG)(pucPersistenceBuff + ulWriteOffset)) = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas;
                ulWriteOffset += sizeof(ULONG);

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas; ulCount2++)
                {
                    memcpy_s((pucPersistenceBuff + ulWriteOffset), sizeof(DP_DPCD_MODEL_DATA),
                             pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2], sizeof(DP_DPCD_MODEL_DATA));
                    ulWriteOffset += sizeof(DP_DPCD_MODEL_DATA);
                }

                if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eDPMST)
                {
                    memcpy_s((pucPersistenceBuff + ulWriteOffset), sizeof(BRANCHDISP_DATA_ARRAY),
                             pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray, sizeof(BRANCHDISP_DATA_ARRAY));
                    ulWriteOffset += sizeof(BRANCHDISP_DATA_ARRAY);
                }

                // If we completed one iteration, that means atleast one sink/display was found. Hence Set bRet to TRUE;
                bRet = TRUE;
            }
            else if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == HDMI)
            {
                pstFileData = pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData;
                ulFileSize  = pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData->uiDataSize;
                memcpy_s((pucPersistenceBuff + ulWriteOffset), (ulFileSize + sizeof(FILE_DATA)), pstFileData, (ulFileSize + sizeof(FILE_DATA)));
                ulWriteOffset += ulFileSize + sizeof(FILE_DATA);

                *((unsigned int *)(pucPersistenceBuff + ulWriteOffset)) = pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.uiDongleType;
                ulWriteOffset += sizeof(ULONG);

                // If we completed one iteration, that means atleast one sink/display was found. Hence Set bRet to TRUE;
                bRet = TRUE;
            }
        }

        if (bRet)
        {
            memcpy_s((pucPersistenceBuff + ulWriteOffset), 8, ucSignatureFooter, 8);

            ulWriteOffset += sizeof(ucSignatureFooter);

            // Write offset finally contains the size of total file
            ((PPERSISTENCE_INFO_HEADER)pucPersistenceBuff)->ulPeristenceDataSize = ulWriteOffset;
        }

        bRet =
        pstPortingObj->pfnFileWrite(&pstPersistenceData->stPersistenceFileHandle, pucPersistenceBuff, ((PPERSISTENCE_INFO_HEADER)pucPersistenceBuff)->ulPeristenceDataSize, 0);

        pstPortingObj->pfnFreeMem(pucPersistenceBuff);
    }
    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_ReadPeristenceDataFromDisk(PGFX_ADAPTER_CONTEXT pGfxAdapterContext)
{
    BOOLEAN                  bRet            = TRUE;
    PUCHAR                   pucDiskFileBuff = NULL, pucIntialFileBuff = NULL;
    ULONG                    ulDiskFileOffset        = 0;
    ULONG                    ulCount                 = 0;
    ULONG                    ulCount2                = 0;
    ULONG                    ulNumBytesRead          = 0;
    PSIMDRV_PERSISTENCE_DATA pstPersistenceData      = NULL;
    PERSISTENCE_INFO_HEADER  stPersistenceInfoHeader = { 0 };
    UCHAR                    ucSignatureHeader[8]    = SIGNATURE_HEADER;
    UCHAR                    ucSignatureFooter[8]    = SIGNATURE_FOOTER;
    PFILE_DATA               pstFileData             = { 0 };
    PPORTINGLAYER_OBJ        pstPortingObj           = GetPortingObj();
    PSIMDEV_EXTENTSION       pSimDrvExtension        = NULL;
    WCHAR                    persistencefilePath[MAX_PATH_STRING_LEN];

    pSimDrvExtension = GetSimDrvExtension();
    if (NULL == pSimDrvExtension || NULL == pstPortingObj)
    {
        return bRet;
    }

    do
    {
        // Open the persistence file
        pstPersistenceData = (PSIMDRV_PERSISTENCE_DATA)pGfxAdapterContext->pvSimPersistenceData;
        if (NULL == pstPersistenceData)
            break;

        pstPortingObj->pfnGetPersistenceFilePath(pGfxAdapterContext, persistencefilePath);
        if (NULL == persistencefilePath)
            break;

        if (FALSE == pstPortingObj->pfnFileCreate(&pstPersistenceData->stPersistenceFileHandle, NULL, persistencefilePath, eRWBin, NULL))
        {
            break;
        }

        // Read the Header First
        // stPersistenceInfoHeader
        if (FALSE == pstPortingObj->pfnFileRead(&pstPersistenceData->stPersistenceFileHandle, (PUCHAR)(&stPersistenceInfoHeader), sizeof(PERSISTENCE_INFO_HEADER), ulDiskFileOffset,
                                                0, &ulNumBytesRead))
        {
            // If the read fails we assume that either that this is the first time SimDrv is loaded on
            // a fresh system to their is no persistence File OR
            // Persistence file was never saved because of a hard/ungraceful reboot/BSOD
            bRet = TRUE;
            break;
        }

        if (memcmp(stPersistenceInfoHeader.ucSignatureHeader, ucSignatureHeader, 8))
        {
            bRet = FALSE;
            break;
        }

        if (stPersistenceInfoHeader.ulPeristenceDataSize == sizeof(PERSISTENCE_INFO_HEADER))
        {
            // This means file opened but there was no persistence data. This could be the first fresh boot scenario where SimDriver is running for the first time and hasn't
            // saved any persistence data yet
            break;
        }

        // The size should be PERSISTENCE_INFO_HEADER or it should atleast be more than one EDID block size
        if (stPersistenceInfoHeader.ulPeristenceDataSize < SIZE_EDID_BLOCK)
        {
            bRet = FALSE;
            break;
        }

        pucIntialFileBuff = pucDiskFileBuff = pstPortingObj->pfnAllocateMem(stPersistenceInfoHeader.ulPeristenceDataSize, TRUE);

        if (pucDiskFileBuff == NULL)
        {
            bRet = FALSE;
            break;
        }

        ulDiskFileOffset += sizeof(PERSISTENCE_INFO_HEADER);

        // Read the whole buffer starting at offset
        // stPersistenceInfoHeader
        //
        if (FALSE ==
            pstPortingObj->pfnFileRead(&pstPersistenceData->stPersistenceFileHandle, pucDiskFileBuff, stPersistenceInfoHeader.ulPeristenceDataSize, ulDiskFileOffset, 0, NULL))
        {
            bRet = FALSE;
            break;
        }

        // Do the footer Check
        if (memcmp((pucDiskFileBuff + stPersistenceInfoHeader.ulPeristenceDataSize - sizeof(PERSISTENCE_INFO_HEADER) - sizeof(ucSignatureFooter)), ucSignatureFooter, 8))
        {
            bRet = FALSE;
            break;
        }

        pstPersistenceData->ulNumEnumeratedPorts = *((PULONG)pucDiskFileBuff);
        // ulDiskFileOffset += sizeof(ULONG);
        pucDiskFileBuff += sizeof(ULONG);

        for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
        {
            pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum = ((PPORT_PERSISTENCE_DATA)pucDiskFileBuff)->ulPortNum;
            pstPersistenceData->stPortPersistenceData[ulCount].eRxType   = ((PPORT_PERSISTENCE_DATA)pucDiskFileBuff)->eRxType;
            pucDiskFileBuff += sizeof(ULONG);
            pucDiskFileBuff += sizeof(RX_TYPE);
            memcpy_s(&pstPersistenceData->stPortPersistenceData[ulCount].uPortConnectorInfo, sizeof(PORT_CONNECTOR_INFO), pucDiskFileBuff, sizeof(PORT_CONNECTOR_INFO));
            pucDiskFileBuff += sizeof(PORT_CONNECTOR_INFO);
            memcpy_s(&pstPersistenceData->stPortPersistenceData[ulCount].eSinkPluggedState, sizeof(SINK_PLUGGED_STATE), pucDiskFileBuff, sizeof(SINK_PLUGGED_STATE));
            pucDiskFileBuff += sizeof(SINK_PLUGGED_STATE);

            if (pstPersistenceData->stPortPersistenceData[ulCount].eSinkPluggedState != eSinkPlugged)
            {
                continue; // If display is not eSinkPlugged, edid and dpcd will not be present. So, skip next steps.
            }

            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
            {
                pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType = *((DP_TOPOLOGY_TYPE *)pucDiskFileBuff);
                // ulDiskFileOffset += sizeof(DP_TOPOLOGY_TYPE);
                pucDiskFileBuff += sizeof(DP_TOPOLOGY_TYPE);

                pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs = *((PULONG)pucDiskFileBuff);
                // ulDiskFileOffset += sizeof(ULONG);
                pucDiskFileBuff += sizeof(ULONG);

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs; ulCount2++)
                {
                    pstFileData = (PFILE_DATA)pucDiskFileBuff;

                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2] =
                    pstPortingObj->pfnAllocateMem((pstFileData->uiDataSize + sizeof(FILE_DATA)), TRUE);

                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2] == NULL)
                    {
                        bRet = FALSE;
                        break;
                    }

                    memcpy_s(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2], (pstFileData->uiDataSize + sizeof(FILE_DATA)),
                             pucDiskFileBuff, (pstFileData->uiDataSize + sizeof(FILE_DATA)));

                    // ulDiskFileOffset += pstFileData->uiDataSize + sizeof(FILE_DATA);
                    pucDiskFileBuff += pstFileData->uiDataSize + sizeof(FILE_DATA);
                }

                if (bRet == FALSE)
                {
                    break;
                }

                pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs = *((PULONG)pucDiskFileBuff);
                // ulDiskFileOffset += sizeof(ULONG);
                pucDiskFileBuff += sizeof(ULONG);

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs; ulCount2++)
                {
                    pstFileData = (PFILE_DATA)pucDiskFileBuff;

                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2] =
                    pstPortingObj->pfnAllocateMem((pstFileData->uiDataSize + sizeof(FILE_DATA)), TRUE);

                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2] == NULL)
                    {
                        bRet = FALSE;
                        break;
                    }

                    memcpy_s(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2], (pstFileData->uiDataSize + sizeof(FILE_DATA)),
                             pucDiskFileBuff, (pstFileData->uiDataSize + sizeof(FILE_DATA)));

                    // ulDiskFileOffset += pstFileData->uiDataSize + sizeof(FILE_DATA);
                    pucDiskFileBuff += pstFileData->uiDataSize + sizeof(FILE_DATA);
                }

                if (bRet == FALSE)
                {
                    break;
                }

                pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas = *((PULONG)pucDiskFileBuff);
                // ulDiskFileOffset += sizeof(ULONG);
                pucDiskFileBuff += sizeof(ULONG);

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas; ulCount2++)
                {
                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2] =
                    pstPortingObj->pfnAllocateMem(sizeof(DP_DPCD_MODEL_DATA), TRUE);

                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2] == NULL)
                    {
                        bRet = FALSE;
                        break;
                    }

                    memcpy_s(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2], sizeof(DP_DPCD_MODEL_DATA), pucDiskFileBuff,
                             sizeof(DP_DPCD_MODEL_DATA));

                    // ulDiskFileOffset += pstFileData->uiDataSize + sizeof(FILE_DATA);
                    pucDiskFileBuff += sizeof(DP_DPCD_MODEL_DATA);
                }

                if (bRet == FALSE)
                {
                    break;
                }

                if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eDPMST)
                {

                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray =
                    pstPortingObj->pfnAllocateMem(sizeof(BRANCHDISP_DATA_ARRAY), TRUE);

                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray == NULL)
                    {
                        bRet = FALSE;
                        break;
                    }

                    memcpy_s(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray, sizeof(BRANCHDISP_DATA_ARRAY), pucDiskFileBuff,
                             sizeof(BRANCHDISP_DATA_ARRAY));

                    // ulDiskFileOffset += sizeof(BRANCHDISP_DATA_ARRAY);
                    pucDiskFileBuff += sizeof(BRANCHDISP_DATA_ARRAY);
                }
            }
            else if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == HDMI)
            {
                pstFileData = (PFILE_DATA)pucDiskFileBuff;

                pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData =
                pstPortingObj->pfnAllocateMem((pstFileData->uiDataSize + sizeof(FILE_DATA)), TRUE);

                if (pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData == NULL)
                {
                    bRet = FALSE;
                    break;
                }

                memcpy_s(pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData, (pstFileData->uiDataSize + sizeof(FILE_DATA)), pucDiskFileBuff,
                         (pstFileData->uiDataSize + sizeof(FILE_DATA)));

                // ulDiskFileOffset += pstFileData->uiDataSize + sizeof(FILE_DATA);
                pucDiskFileBuff += pstFileData->uiDataSize + sizeof(FILE_DATA);

                pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.uiDongleType = *((unsigned int *)pucDiskFileBuff);
                // ulDiskFileOffset += sizeof(ULONG);
                pucDiskFileBuff += sizeof(ULONG);
            }
        }

        bRet = TRUE;

    } while (FALSE);

    if (pucIntialFileBuff)
    {
        pstPortingObj->pfnFreeMem(pucIntialFileBuff);
    }

    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_ReconstructSinkConfigFromPersistenceData(PGFX_ADAPTER_CONTEXT pGfxAdapterContext)
{
    BOOLEAN                  bRet               = FALSE;
    ULONG                    ulCount            = 0;
    ULONG                    ulCount2           = 0;
    PORT_INFO                stPortInfo         = { 0 };
    DP_INIT_INFO             stDPInitInfo       = { 0 };
    PSIMDRV_PERSISTENCE_DATA pstPersistenceData = NULL;

    do
    {
        if (NULL == pGfxAdapterContext)
            return FALSE;
        pstPersistenceData = (PSIMDRV_PERSISTENCE_DATA)pGfxAdapterContext->pvSimPersistenceData;

        if (pstPersistenceData->ulNumEnumeratedPorts == 0)
        {
            // This means no persistence data has been saved yes so simply return TRUE
            bRet = TRUE;
            break;
        }

        for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
        {
            stPortInfo.ulPortNum         = pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum;
            stPortInfo.eRxTypes          = pstPersistenceData->stPortPersistenceData[ulCount].eRxType;
            stPortInfo.eInitialPlugState = pstPersistenceData->stPortPersistenceData[ulCount].eSinkPluggedState;

            bRet = COMMONRXHANDLERS_SetRxInfo(&stPortInfo, pGfxAdapterContext->pstRxInfoArr);

            if (bRet == FALSE)
            {
                break;
            }

            bRet = COMMONMMIOHANDLERS_SetEdpTypeCMappingInfo(pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface, stPortInfo.ulPortNum);
            if (bRet == FALSE)
            {
                break;
            }
        }

        if (bRet == FALSE)
        {
            break;
        }

        for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
        {
            if (pstPersistenceData->stPortPersistenceData[ulCount].eSinkPluggedState != eSinkPlugged)
            {
                continue; // If display is not eSinkPlugged, edid and dpcd will not be present. So, skip next steps.
            }

            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
            {
                stDPInitInfo.uiPortNum     = pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum;
                stDPInitInfo.eTopologyType = pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType;

                bRet = DPHANDLERS_InitDPTopologyType(pGfxAdapterContext->pstRxInfoArr, &stDPInitInfo);

                if (bRet == FALSE)
                {
                    break;
                }

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs; ulCount2++)
                {
                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2] == NULL)
                    {
                        break;
                    }

                    bRet = COMMRXHANDLERS_SetEDIDData(pGfxAdapterContext->pstRxInfoArr,
                                                      pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2], FALSE);

                    if (bRet == FALSE)
                    {
                        break;
                    }
                }

                if (bRet == FALSE)
                {
                    break;
                }

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs; ulCount2++)
                {
                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2] == NULL)
                    {
                        break;
                    }

                    bRet = DPHANDLERS_SetDPCDData(pGfxAdapterContext->pstRxInfoArr, pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2]);

                    if (bRet == FALSE)
                    {
                        break;
                    }
                }

                if (bRet == FALSE)
                {
                    break;
                }

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas; ulCount2++)
                {
                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2] == NULL)
                    {
                        break;
                    }

                    bRet = DPHANDLERS_SetDPCDModelData(pGfxAdapterContext->pstRxInfoArr,
                                                       pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2]);

                    if (bRet == FALSE)
                    {
                        break;
                    }
                }

                if (bRet == FALSE)
                {
                    break;
                }

                if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.eTopologyType == eDPMST &&
                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray)
                {

                    if (FALSE == DPHANDLERS_SetDPMSTTopology(pGfxAdapterContext->pstRxInfoArr,
                                                             pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray))
                    {
                        break;
                    }
                }
            }
            else if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == HDMI)
            {
                if (pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData == NULL)
                {
                    break;
                }

                if (FALSE ==
                    COMMRXHANDLERS_SetEDIDData(pGfxAdapterContext->pstRxInfoArr, pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData, FALSE))
                {
                    break;
                }

                if (FALSE == HDMIHANDLERS_SetDongleType(pGfxAdapterContext->pstRxInfoArr, pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum,
                                                        pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.uiDongleType))
                {
                    break;
                }
            }

            bRet = COMMONMMIOHANDLERS_SetLiveStateForPort(pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface, pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum, TRUE,
                                                          pstPersistenceData->stPortPersistenceData[ulCount].uPortConnectorInfo);

            if (bRet)
            {
                pstPersistenceData->stPortPersistenceData[ulCount].eSinkPluggedState = eSinkPlugged;
            }
        }

    } while (FALSE);

    return bRet;
}

BOOLEAN PERSISTENCEHANDLER_CleanUpPort(PSIMDRV_PERSISTENCE_DATA pstPersistenceData, PORT_TYPE ePortNum)
{
    ULONG             ulCount       = 0;
    ULONG             ulCount2      = 0;
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum == (ULONG)ePortNum)
        {
            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
            {
                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs; ulCount2++)
                {
                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2])
                    {
                        pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2]);
                        pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2] = NULL;
                    }
                }

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs; ulCount2++)
                {
                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2])
                    {
                        pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2]);
                        pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2] = NULL;
                    }
                }

                for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas; ulCount2++)
                {
                    if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2])
                    {
                        pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2]);
                        pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2] = NULL;
                    }
                }

                // Applicable only for MST
                if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray)
                {
                    pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray);
                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray = NULL;
                }
            }
            else if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == HDMI)
            {
                pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData);
                pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData = NULL;
            }

            // pstPersistenceData->stPortPersistenceData[ulCount].eRxType = RxInvalidType;
            // pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum = 0xFF;
            pstPersistenceData->ulNumEnumeratedPorts--;

            for (; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
            {
                pstPersistenceData->stPortPersistenceData[ulCount] = pstPersistenceData->stPortPersistenceData[ulCount + 1];
            }

            // memset structures to 0 at last index, since last and (last-1) have the same data/pointers after above shift left operation
            if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
            {
                memset(&(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData), 0, sizeof(DP_PERSISTENCE_DATA));
            }
            else if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == HDMI)
            {
                memset(&(pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData), 0, sizeof(HDMI_PERSISTENCE_DATA));
            }

            break;
        }
    }

    return TRUE;
}

BOOLEAN PERSISTENCEHANDLER_CleanUpAllPorts(PSIMDRV_PERSISTENCE_DATA pstPersistenceData)
{
    ULONG             ulCount       = 0;
    ULONG             ulCount2      = 0;
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();

    for (ulCount = 0; ulCount < pstPersistenceData->ulNumEnumeratedPorts; ulCount++)
    {
        if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == DP)
        {
            for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumEDIDs; ulCount2++)
            {
                if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2])
                {
                    pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2]);
                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstEDIDData[ulCount2] = NULL;
                }
            }

            for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDs; ulCount2++)
            {
                if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2])
                {
                    pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2]);
                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDPCDData[ulCount2] = NULL;
                }
            }

            for (ulCount2 = 0; ulCount2 < pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.ulNumDPCDModelDatas; ulCount2++)
            {
                if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2])
                {
                    pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2]);
                    pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstDpDPCDModelData[ulCount2] = NULL;
                }
            }

            // Applicable only for MST
            if (pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray)
            {
                pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray);
                pstPersistenceData->stPortPersistenceData[ulCount].stDPPersistenceData.pstBranchDispDataArray = NULL;
            }
        }
        else if (pstPersistenceData->stPortPersistenceData[ulCount].eRxType == HDMI)
        {
            pstPortingObj->pfnFreeMem(pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData);
            pstPersistenceData->stPortPersistenceData[ulCount].stHDMIPersistenceData.pstEDIDData = NULL;
        }

        pstPersistenceData->stPortPersistenceData[ulCount].eRxType   = RxInvalidType;
        pstPersistenceData->stPortPersistenceData[ulCount].ulPortNum = 0xFF;
    }

    pstPersistenceData->ulNumEnumeratedPorts = 0;

    return TRUE;
}

BOOLEAN PERSISTENCEHANDLER_IsPersistenceFileOpen(PGFX_ADAPTER_CONTEXT pGfxAdapterContext)
{
    if (NULL == pGfxAdapterContext)
        return FALSE;

    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    BOOLEAN           bRet          = pstPortingObj->pfnIsFileOpen(&((PSIMDRV_PERSISTENCE_DATA)pGfxAdapterContext->pvSimPersistenceData)->stPersistenceFileHandle);
    return bRet;
}
