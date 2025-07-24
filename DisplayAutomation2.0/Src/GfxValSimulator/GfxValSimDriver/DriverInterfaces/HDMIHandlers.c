
#include "HDMIHandlers.h"
#include "..\\HDMICore\\GMBusInterface.h"
#include "CommonRxHandlers.h"
#include "..\CommonInclude\ETWLogging.h"

PHDMI_INTERFACE HDMIHANDLERS_HDMIInterfaceInit(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType)
{
    PPORTINGLAYER_OBJ pstPortingObj    = GetPortingObj();
    PHDMI_INTERFACE   pstHDMIInterface = (PHDMI_INTERFACE)pstPortingObj->pfnAllocateMem(sizeof(*pstHDMIInterface), TRUE);
    BOOLEAN           bFound           = FALSE;

    if (pstHDMIInterface == NULL || pstRxInfoArr == NULL)
    {
        goto EXIT;
    }
    else
    {
        // For an adapter only one GMBus Object to be created. So, loop through ulNumEnumeratedPorts and return if exists.
        // If GMBus Object is not found, create a new one.
        for (ULONG ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
        {
            if (pstRxInfoArr->stRxInfoObj[ulCount].eRxType == HDMI && pstRxInfoArr->stRxInfoObj[ulCount].pstHDMIInterface != NULL)
            {
                pstHDMIInterface->pstGMBusInterface = pstRxInfoArr->stRxInfoObj[ulCount].pstHDMIInterface->pstGMBusInterface;
                pstHDMIInterface->pstGMBusInterface->ulNumRefCount++;
                GFXVALSIM_DBG_MSG("pstHDMIInterface->pstGMBusInterface->ulNumRefCount: %d", pstHDMIInterface->pstGMBusInterface->ulNumRefCount);
                bFound = TRUE;
                break;
            }
        }

        if (FALSE == bFound)
        {
            pstHDMIInterface->pstGMBusInterface =
            GMBusInterface_GetSingletonGMBusObject(pstRxInfoArr->pstMMIOInterface->eIGFXPlatform, pstRxInfoArr->pstMMIOInterface->ePCHProductFamily);
        }

        // InitGMBUSHandler()  -- pstMMIOPrimaryRoutines->pfnRegisterGMBUSMMIOInitHandlers
        // Register all the GMBUS read/write handlers..
        if (FALSE == COMMONMMIOHANDLERS_RegisterGMBUSHandlers(pstRxInfoArr->pstMMIOInterface, pstHDMIInterface, ePortType))
        {
            GFXVALSIM_DBG_MSG("Gmbus handlers registration failed.");
            goto EXIT;
        }
        else
        {
            return pstHDMIInterface;
        }
    }

EXIT:
    if (pstHDMIInterface)
    {
        pstPortingObj->pfnFreeMem(pstHDMIInterface);
        pstHDMIInterface = NULL;
    }

    GFXVALSIM_FUNC_EXIT((pstHDMIInterface == NULL) ? 1 : 0);
    return pstHDMIInterface;
}

BOOLEAN HDMIHANDLERS_SetEDIDData(PRX_INFO_ARR pstRxInfoArr, PFILE_DATA pstEdidData)
{
    BOOLEAN bRet = FALSE;
    do
    {
        if (NULL == pstEdidData)
        {
            break;
        }
        PHDMI_INTERFACE pstHDMIInterface = COMMRXHANDLERS_GetHDMIInterfaceFromPortType(pstRxInfoArr, pstEdidData->uiPortNum);
        ULONG           ulEDIDSize       = pstEdidData->uiDataSize;
        ULONG           ulHDMIPort       = pstEdidData->uiPortNum;
        PUCHAR          pucEDIDBuff      = (PUCHAR)(((PUCHAR)pstEdidData) + sizeof(*pstEdidData));
        if (pstHDMIInterface && ((ulEDIDSize % SIZE_EDID_BLOCK) == 0) && pucEDIDBuff)
        {
            // Need to add ports for HDMI
            // pstHDMIInterface->EdidData.ulPortNum = pstRxInfoArr->stRxInfoObj->ePortNum;
            bRet = GMBusInterface_SetEDIDData(pstHDMIInterface->pstGMBusInterface, ulEDIDSize, pucEDIDBuff, ulHDMIPort);
        }
    } while (FALSE);

    return bRet;
}

BOOLEAN HDMIHANDLERS_SetSCDCData(PRX_INFO_ARR pstRxInfoArr, PFILE_DATA pstScdcData)
{
    BOOLEAN bRet = FALSE;
    do
    {
        if (NULL == pstScdcData)
        {
            break;
        }
        PHDMI_INTERFACE pstHDMIInterface = COMMRXHANDLERS_GetHDMIInterfaceFromPortType(pstRxInfoArr, pstScdcData->uiPortNum);
        ULONG           ulSCDCSize       = pstScdcData->uiDataSize;
        ULONG           ulHDMIPort       = pstScdcData->uiPortNum;
        PUCHAR          pucSCDCBuff      = (PUCHAR)(((PUCHAR)pstScdcData) + sizeof(*pstScdcData));
        if (pstHDMIInterface && pucSCDCBuff)
        {
            bRet = GMBusInterface_SetSCDCData(pstHDMIInterface->pstGMBusInterface, ulSCDCSize, pucSCDCBuff, ulHDMIPort);
        }
    } while (FALSE);

    return bRet;
}

BOOLEAN HDMIHANDLERS_SetEDIDDataForS3S4Cycle(PRX_INFO_ARR pstRxInfoArr, PFILE_DATA pstEdidData)
{
    BOOLEAN                  bRet                    = FALSE;
    PUCHAR                   pucIncomingEDIDBuff     = NULL;
    PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData = COMMRXHANDLERS_GetRxS3S4PlugUnPlugDataPtr(pstRxInfoArr, pstEdidData->uiPortNum, HDMI);
    PHDMI_INTERFACE          pstHDMIInterface        = COMMRXHANDLERS_GetHDMIInterfaceFromPortType(pstRxInfoArr, pstEdidData->uiPortNum);
    PPORTINGLAYER_OBJ        pstPortingObj           = GetPortingObj();

    do
    {
        if (pstRxS3S4PlugUnPlugData == NULL || NULL == pstHDMIInterface)
        {
            break;
        }

        pucIncomingEDIDBuff                                            = (PUCHAR)(((PUCHAR)pstEdidData) + sizeof(FILE_DATA));
        pstRxS3S4PlugUnPlugData->stS3S4HDMIPlugData.pucNewHDMIEDIDBuff = pstPortingObj->pfnAllocateMem(pstEdidData->uiDataSize, TRUE);
        memcpy_s(pstRxS3S4PlugUnPlugData->stS3S4HDMIPlugData.pucNewHDMIEDIDBuff, pstEdidData->uiDataSize, pucIncomingEDIDBuff, pstEdidData->uiDataSize);
        pstRxS3S4PlugUnPlugData->stS3S4HDMIPlugData.ulNewHDMIEDIDSize = pstEdidData->uiDataSize;
        bRet                                                          = TRUE;

    } while (FALSE);

    return bRet;
}

BOOLEAN HDMIHANDLERS_SetDongleType(PVOID pstRxInfoArr, PORT_TYPE ePortType, DONGLE_TYPE eDongleType)
{
    BOOLEAN bRet = FALSE;
    do
    {
        PHDMI_INTERFACE pstHDMIInterface = COMMRXHANDLERS_GetHDMIInterfaceFromPortType(pstRxInfoArr, ePortType);

        if (NULL == pstHDMIInterface)
        {
            break;
        }

        bRet = GMBusInterface_SetDongleType(pstHDMIInterface->pstGMBusInterface, ePortType, eDongleType);

    } while (FALSE);

    return bRet;
}

BOOLEAN HDMIHANDLERS_GMBUSReadHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, PULONG pulReadData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = TRUE;
    // PHDMI_INTERFACE pstHDMIInterface = (HDMI_INTERFACE *)pstMMIOHandlerInfo->pvPrivateData;
    PHDMI_INTERFACE pstHDMIInterface = (HDMI_INTERFACE *)pstMMIOHandlerInfo->pvCallerPersistedData;

    switch (ulMMIOOffset)
    {
    case GMBUS0:
    case GMBUS1:
    case GMBUS2:
    {
        *pulReadData = GMBusInterface_ReadGMBUSDWORDRegister(pstHDMIInterface->pstGMBusInterface, ulMMIOOffset);
        break;
    }
    case GMBUS3:
    {
        bRet         = GMBusInterface_GMBUSStateMachineHandler(pstHDMIInterface->pstGMBusInterface, GMBUS_READ);
        *pulReadData = GMBusInterface_ReadGMBUSDWORDRegister(pstHDMIInterface->pstGMBusInterface, ulMMIOOffset);
        break;
    }
    default:
        break;
    }
    return bRet;
}

BOOLEAN HDMIHANDLERS_GMBUSWriteHandler(PMMIO_HANDLER_INFO pstMMIOHandlerInfo, ULONG ulMMIOOffset, ULONG ulWriteData, PREGRW_EXEC_SITE peRegRWExecSite)
{
    BOOLEAN bRet = TRUE;
    // PHDMI_INTERFACE pstHDMIInterface = (HDMI_INTERFACE *)pstMMIOHandlerInfo->pvPrivateData;
    PHDMI_INTERFACE pstHDMIInterface = (HDMI_INTERFACE *)pstMMIOHandlerInfo->pvCallerPersistedData;

    switch (ulMMIOOffset)
    {
    case GMBUS0:
    {
        bRet = GMBusInterface_GMBUS0WriteHandler(pstHDMIInterface->pstGMBusInterface, ulMMIOOffset, ulWriteData);
        break;
    }
    case GMBUS1:
    {
        bRet = GMBusInterface_GMBUS1WriteHandler(pstHDMIInterface->pstGMBusInterface, ulMMIOOffset, ulWriteData);
        break;
    }
    case GMBUS2:
    {
        bRet = GMBusInterface_GMBUS2WriteHandler(pstHDMIInterface->pstGMBusInterface, ulMMIOOffset, ulWriteData);
        break;
    }
    case GMBUS3:
    {
        GMBusInterface_WriteGMBUSDWORDRegister(pstHDMIInterface->pstGMBusInterface, ulMMIOOffset, ulWriteData);
        bRet = TRUE;
        break;
    }
    default:
        break;
    }
    return bRet;
}

BOOLEAN HDMIHANDLERS_CleanUp(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType)
{
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    BOOLEAN           bRet          = FALSE;
    ULONG             ulCount       = 0;

    PHDMI_INTERFACE pstHDMIInterface = COMMRXHANDLERS_GetHDMIInterfaceFromPortType(pstRxInfoArr, ePortType);

    if (pstHDMIInterface)
    {
        bRet = HDMIHANDLERS_EDID_SCDC_CleanUp(pstHDMIInterface, ePortType);

        if ((pstHDMIInterface->pstGMBusInterface) && bRet)
        {
            pstHDMIInterface->pstGMBusInterface->ulNumRefCount--;

            // Free GMBus interface once its reference count becomes ZERO
            if (0 == pstHDMIInterface->pstGMBusInterface->ulNumRefCount)
            {
                pstPortingObj->pfnFreeMem(pstHDMIInterface->pstGMBusInterface);

                pstHDMIInterface->pstGMBusInterface = NULL;

                for (ulCount = 0; ulCount < pstRxInfoArr->ulNumEnumeratedPorts; ulCount++)
                {
                    if (HDMI == pstRxInfoArr->stRxInfoObj[ulCount].eRxType)
                    {
                        // It is to asssign NULL to GmBus object in all the enumarated HDMI interfaces
                        // as GMbus object is singleton and has already been freed.
                        // It is required, otherwise it will become dangling pointer and could result into BSOD
                        pstRxInfoArr->stRxInfoObj[ulCount].pstHDMIInterface->pstGMBusInterface = NULL;

                        // GMBus interface is already freed, so now we can free the HDMI interfaces
                        // Reference count is ZERO, hence all HDMI interfaces can be freed
                        pstPortingObj->pfnFreeMem(pstRxInfoArr->stRxInfoObj[ulCount].pstHDMIInterface);
                        pstRxInfoArr->stRxInfoObj[ulCount].pstHDMIInterface = NULL;
                    }
                }
            }
        }
    }
    return TRUE;
}

BOOLEAN HDMIHANDLERS_EDID_SCDC_CleanUp(PHDMI_INTERFACE pstHDMIInterface, PORT_TYPE ePortType)
{
    PPORTINGLAYER_OBJ pstPortingObj = GetPortingObj();
    ULONG             ulEDIDIndex   = EDID_INDEX_INVALID;
    ULONG             ulSCDCIndex   = SCDC_INDEX_INVALID;
    BOOLEAN           bRet          = GMBusInterface_GetEDIDIndexFromPort(ePortType, &ulEDIDIndex);

    if (bRet && pstHDMIInterface && (pstHDMIInterface->pstGMBusInterface))
    {
        if (pstHDMIInterface->pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData)
        {
            pstPortingObj->pfnFreeMem((PVOID)pstHDMIInterface->pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData);
            pstHDMIInterface->pstGMBusInterface->EdidData[ulEDIDIndex].ulEdidDataSize  = 0;
            pstHDMIInterface->pstGMBusInterface->EdidData[ulEDIDIndex].ulHDMIPort      = 0;
            pstHDMIInterface->pstGMBusInterface->EdidData[ulEDIDIndex].ulNumEDIDBlocks = 0;
            pstHDMIInterface->pstGMBusInterface->EdidData[ulEDIDIndex].pucEdidData     = NULL;
        }
    }

    bRet = GMBusInterface_GetSCDCIndexFromPort(ePortType, &ulSCDCIndex);

    if (bRet && pstHDMIInterface && (pstHDMIInterface->pstGMBusInterface))
    {
        if (pstHDMIInterface->pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData)
        {
            pstPortingObj->pfnFreeMem((PVOID)pstHDMIInterface->pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData);
            pstHDMIInterface->pstGMBusInterface->ScdcData[ulSCDCIndex].ulScdcDataSize = 0;
            pstHDMIInterface->pstGMBusInterface->ScdcData[ulSCDCIndex].ulHDMIPort     = 0;
            pstHDMIInterface->pstGMBusInterface->ScdcData[ulSCDCIndex].pucScdcData    = NULL;
        }
    }

    return bRet;
}

BOOLEAN HDMIHANDLERS_ConfigureDPGfxS3S4PlugUnplugData(PRX_INFO_ARR pstRxInfoArr, PGFXS3S4_PORT_PLUGUNPLUG_DATA pstGfxS3S4PortPlugUnplugData)
{
    BOOLEAN                  bRet                    = TRUE;
    PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData = COMMRXHANDLERS_GetRxS3S4PlugUnPlugDataPtr(pstRxInfoArr, pstGfxS3S4PortPlugUnplugData->ulPortNum, HDMI);

    pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest                     = pstGfxS3S4PortPlugUnplugData->eSinkPlugReq;
    pstRxS3S4PlugUnPlugData->stS3S4HDMIPlugData.bPlugUnplugAtSource = pstGfxS3S4PortPlugUnplugData->stS3S4DPPlugUnplugData.bPlugOrUnPlugAtSource;
    pstRxS3S4PlugUnPlugData->stS3S4HDMIPlugData.uiDongleType        = pstGfxS3S4PortPlugUnplugData->uiDongleType;

    return bRet;
}

BOOLEAN HDMIHANDLERS_HandleGfxPowerNotification(PRX_INFO_ARR pstRxInfoArr, PORT_TYPE ePortType, PRX_S3S4_PLUGUNPLUG_DATA pstRxS3S4PlugUnPlugData, DEVICE_POWER_STATE eGfxPowerState,
                                                POWER_ACTION eActionType, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN           bRet             = FALSE;
    PHDMI_INTERFACE   pstHDMIInterface = COMMRXHANDLERS_GetHDMIInterfaceFromPortType(pstRxInfoArr, ePortType);
    PPORTINGLAYER_OBJ pstPortingObj    = GetPortingObj();

    if (eGfxPowerState != PowerDeviceD0)
    {
        if (pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.bPlugUnplugAtSource)
        {
            if (pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == ePlugSink || pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == eUnPlugOldPlugNew)
            {
                // Turn off Live State here First:
                bRet = COMMONMMIOHANDLERS_SetLiveStateForPort(pstRxInfoArr->pstMMIOInterface, ePortType, FALSE, PortConnectorInfo);

                if (bRet)
                {
                    bRet = GMBusInterface_SetDongleType(pstHDMIInterface->pstGMBusInterface, ePortType, pstRxS3S4PlugUnPlugData->stS3S4HDMIPlugData.uiDongleType);

                    bRet = GMBusInterface_SetEDIDData(pstHDMIInterface->pstGMBusInterface, pstRxS3S4PlugUnPlugData->stS3S4HDMIPlugData.ulNewHDMIEDIDSize,
                                                      pstRxS3S4PlugUnPlugData->stS3S4HDMIPlugData.pucNewHDMIEDIDBuff, ePortType);

                    // turn on live state here again if it was turned on:
                    bRet = COMMONMMIOHANDLERS_SetLiveStateForPort(pstRxInfoArr->pstMMIOInterface, ePortType, TRUE, PortConnectorInfo);
                }
            }
            else if (pstRxS3S4PlugUnPlugData->eRxS3S4PlugRequest == eUnplugSink)
            {
                bRet = COMMONMMIOHANDLERS_SetLiveStateForPort(pstRxInfoArr->pstMMIOInterface, ePortType, FALSE, PortConnectorInfo);
            }
        }

        // Since we have finally processed the S3/S4 data so cleanup and reset the cache
        if (pstRxS3S4PlugUnPlugData->stS3S4HDMIPlugData.pucNewHDMIEDIDBuff)
        {
            pstPortingObj->pfnFreeMem(pstRxS3S4PlugUnPlugData->stS3S4DPPlugData.pucNewSSTEDIDBuff);
        }

        memset(pstRxS3S4PlugUnPlugData, 0, sizeof(RX_S3S4_PLUGUNPLUG_DATA));
    }

    return bRet;
}
