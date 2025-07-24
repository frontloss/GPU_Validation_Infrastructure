#include "SimDrvToGfx.h"
// #include "..\\GenMMIOHandlers\\CommonMMIO.h"
#include "..\DriverInterfaces\PlatformInfo.h"
#include "CommonRxHandlers.h"
#include "..\CommonInclude\ETWLogging.h"
#include "..\VBTSimulation\VBTSimulation.h"
#include "..\\PeristenceServices\\PersistenceHandler.h"
#include "..\\CommonCore\CommonCore.h"
#include "..\\..\\GfxValSimLibrary\\DriverWATable.h"

NTSTATUS SIMDRVTOGFX_RegDeRegCallBack(PSIMDRVGFX_CONTEXT pstSimDrvGfxContext, BOOLEAN bRegister);

VOID SIMDRVTOGFX_GfxCallBackRoutine(PVOID pGfxContext, PVOID pArg1, PVOID pArg2);

NTSTATUS QueryDisplayAdapterDetails(IN PDEVICE_OBJECT pPhysicalDeviceObject, BUS_QUERY_ID_TYPE queryType, WCHAR *pBuffer);

NTSTATUS SIMDRVTOGFX_GfxStatusNofitication(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSIMDRV_GFX_STATUS_ARGS pstGfxStatusArgs);

BOOLEAN SIMDRVTOGFX_GfxPowerStateNotification(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, DEVICE_POWER_STATE eGfxPowerState, POWER_ACTION eActionType);

BOOLEAN SIMDRVTOGFX_GfxReadOPRomRegion(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, UCHAR *pBuffer, ULONG ulOffset, ULONG ulSize, ULONG *ulBytesRead);

NTSTATUS SIMDRVCB_GenericHandler(void *pvSimDrvContext, void *pGfxHwDev, SIMDRV_CB_GENERIC_HANDLER_ARGS *pSimDrvCbGenericHandlerArgs);

PGFX_ADAPTER_CONTEXT GetAdapterContext(SIMDRVGFX_CONTEXT *pstSimDrvGfxContext, WCHAR *pPCIBusDeviceId, WCHAR *pPCIBusInstanceId);
PGFX_ADAPTER_CONTEXT GetAdapterContextEx(SIMDRVGFX_CONTEXT *pstSimDrvGfxContext, PVOID pvGfxHwDev);
VOID                 UpdateAdapterContext(SIMDRVGFX_CONTEXT *pstSimDrvGfxContext, GFX_ADAPTER_SERVICE_TYPE requestType, PGFX_ADAPTER_CONTEXT pGfxAdapterContext);

NTSTATUS SIMDRVTOGFX_InitSimDrvToGfxInterfaces(PSIMDRVGFX_CONTEXT *ppstSimDrvGfxContext)
{
    NTSTATUS           ntStatus            = STATUS_UNSUCCESSFUL;
    PSIMDRVGFX_CONTEXT pstSimDrvGfxContext = NULL;
    PPORTINGLAYER_OBJ  pstPortingObj       = GetPortingObj();

    do
    {
        if (NULL == pstPortingObj)
            break;

        pstSimDrvGfxContext = pstPortingObj->pfnAllocateMem(sizeof(SIMDRVGFX_CONTEXT), TRUE);
        if (NULL == pstSimDrvGfxContext)
            break;

        pstSimDrvGfxContext->pfnGetAdapterContext    = GetAdapterContext;
        pstSimDrvGfxContext->pfnGetAdapterContextEx  = GetAdapterContextEx;
        pstSimDrvGfxContext->pfnUpdateAdapterContext = UpdateAdapterContext;

        ntStatus = SIMDRVTOGFX_RegDeRegCallBack(pstSimDrvGfxContext, TRUE);

        if (!NT_SUCCESS(ntStatus))
            break;
        *ppstSimDrvGfxContext = pstSimDrvGfxContext;
        ntStatus              = STATUS_SUCCESS;

    } while (FALSE);

    return ntStatus;
}

NTSTATUS SIMDRVTOGFX_RegDeRegCallBack(PSIMDRVGFX_CONTEXT pstSimDrvGfxContext, BOOLEAN bRegister)
{
    NTSTATUS          ntStatus = STATUS_UNSUCCESSFUL;
    UNICODE_STRING    ObjectName;
    OBJECT_ATTRIBUTES ObjectAttributes;

    KIRQL SimDrvIrql = { 0 };

    if (bRegister && NULL == pstSimDrvGfxContext->pvRegisteredCBObjHandle && pstSimDrvGfxContext->pvSimDrvGfxCallBackObj == NULL)
    {
        RtlInitUnicodeString(&ObjectName, SIMDRV_GFX_SHARED_OBJ_NAME);

        // 1. InitializeObjectAttributes initializes OBJECT_ATTRIBUTES structure that specifies the properties of an object
        // handle to be opened. The driver can then pass a pointer to this structure to ExCreateCallback to open the handle.
        InitializeObjectAttributes(&ObjectAttributes, &ObjectName, SIMDRV_GFX_OBJ_ATTRIB, NULL, NULL);

        // 2. The ExCreateCallback routine creates a new callback object. Returns STATUS_SUCCESS if a callback object
        // was opened or created. Otherwise, it returns an NTSTATUS error code.
        ntStatus = ExCreateCallback((PCALLBACK_OBJECT *)&pstSimDrvGfxContext->pvSimDrvGfxCallBackObj, &ObjectAttributes, TRUE, FALSE);

        // 3. Register the call back function and pass pHwdev as the context
        if (NT_SUCCESS(ntStatus))
        {
            // The ExRegisterCallback routine registers a given callback routine with a given callback object
            pstSimDrvGfxContext->pvRegisteredCBObjHandle = ExRegisterCallback(pstSimDrvGfxContext->pvSimDrvGfxCallBackObj, SIMDRVTOGFX_GfxCallBackRoutine, pstSimDrvGfxContext);
        }
    }

    // De-register callback if flag bRegister is FALSE
    if (!bRegister)
    {
        SimDrvIrql = KeGetCurrentIrql();
        if (DISPATCH_LEVEL >= SimDrvIrql)
        {
            if (APC_LEVEL >= SimDrvIrql && (NULL != pstSimDrvGfxContext->pvSimDrvGfxCallBackObj))
            {
                // The ExUnregisterCallback routine removes a callback routine previously registered with a callback object
                ExUnregisterCallback(pstSimDrvGfxContext->pvRegisteredCBObjHandle);
                pstSimDrvGfxContext->pvRegisteredCBObjHandle = NULL;
            }
            if (NULL != pstSimDrvGfxContext->pvSimDrvGfxCallBackObj)
            {
                // ObDereferenceObject decreases the reference count of an object by one and if reference count reaches
                // zero, then object will be deleted by the system
                ObDereferenceObject(pstSimDrvGfxContext->pvSimDrvGfxCallBackObj);
                pstSimDrvGfxContext->pvSimDrvGfxCallBackObj = NULL;
            }
        }
    }
    return ntStatus;
}

VOID UpdateSimulationEnvironmentInfo(PGFX_ADAPTER_CONTEXT pGfxAdapterContext)
{
    ULONG driverRegValue         = 0;
    pGfxAdapterContext->bIsPreSi = FALSE;

    if (TRUE == SIMDRVTOGFX_HwMmioAccess(pGfxAdapterContext, PRESI_ENV_DETECT_REG, &driverRegValue, SIMDRV_GFX_ACCESS_REQUEST_READ))
    {
        GFXVALSIM_DBG_MSG("reg value: %uld!\r\n", driverRegValue);
        if ((driverRegValue & PRESI_ENV_ENABLE_BIT) == PRESI_ENV_ENABLE_BIT)
        {
            pGfxAdapterContext->bIsPreSi = TRUE;
            GFXVALSIM_DBG_MSG("Pre-Silicon Environment!\r\n");
        }
        else
        {
            GFXVALSIM_DBG_MSG("Post-Silicon Environment!\r\n");
        }
    }
    else
    {
        GFXVALSIM_DBG_MSG("Failed: SIMDRVTOGFX_HwMmioAccess() for offset: 0x180F08 !\r\n");
    }
}

BOOLEAN InitializeTestMMIO(GFX_ADAPTER_CONTEXT gfxAdapterContext, PMMIO_INTERFACE pstMMIOInterface)
{
    BOOLEAN bRet = TRUE;

    NTSTATUS NtStatus;
    BOOLEAN  ret     = FALSE;
    DDU32    VbtSize = 0;
    WCHAR    RegistryKey[MAX_PATH_STRING_LEN];
    GFXVALSIM_FUNC_ENTRY();

    do
    {
        wcscpy(RegistryKey, gfxAdapterContext.PCIBusDeviceId);
        wcscat_s(RegistryKey, MAX_PATH_STRING_LEN, SIMDRV_REGKEY_TEST_MMIO_DATA);

        NtStatus = COMMONCORE_GetRegistryInfo(RegistryKey, REG_BINARY, &(pstMMIOInterface->stTestMMIOArray), sizeof(pstMMIOInterface->stTestMMIOArray));

        ret = NT_SUCCESS(NtStatus) ? TRUE : FALSE;
        if (ret == FALSE)
        {
            GFXVALSIM_DBG_MSG("Failed to Load Test MMIO from registry !!\r\n");
            break;
        }

        if (pstMMIOInterface->stTestMMIOArray.ulNumRegisters == 0 || pstMMIOInterface->stTestMMIOArray.ulNumRegisters > MAX_TEST_MMIO_OFFSETS_STORED)
        {
            GFXVALSIM_DBG_MSG("Either ulNumRegisters is 0 or more than MAX_TEST_MMIO_OFFSETS_STORED!!\r\n");
            break;
        }

        for (ULONG i = 0; i < pstMMIOInterface->stTestMMIOArray.ulNumRegisters; i++)
        {
            COMMONMMIOHANDLERS_UpdateMMIOInitialStateMMIOHandlers(pstMMIOInterface, pstMMIOInterface->stTestMMIOArray.stMMIOList[i].ulMMIOOffset,
                                                                  pstMMIOInterface->stTestMMIOArray.stMMIOList[i].ulMMIOData);
        }
        bRet = TRUE;
    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);
    return bRet;
}

VOID SIMDRVTOGFX_GfxCallBackRoutine(PVOID pGfxContext, PVOID pArg1, PVOID pArg2)
{
    GFX_ADAPTER_CONTEXT       gfxAdapterContext         = { 0 };
    PSIMDRVGFX_INTERFACE_DATA pstSimDrvGfxInterfaceData = (PSIMDRVGFX_INTERFACE_DATA)pArg1;
    PSIMDRVGFX_CONTEXT        pstSimDrvGfxContext       = (PSIMDRVGFX_CONTEXT)pGfxContext;

    // Initialize structure platform info to NULL
    PLATFORM_INFO               stPlatformInfo         = { 0 };
    SIMDRV_OPREGION_VBT_DETAILS OpRegionVbtDetails     = { 0 };
    SIMDRV_OPREGION_VBT_DETAILS TempOpRegionVbtDetails = { 0 };

    GFXVALSIM_FUNC_ENTRY();
    do
    {
        if (NULL == pstSimDrvGfxInterfaceData || NULL == pstSimDrvGfxContext)
        {
            GFXVALSIM_DBG_MSG("pstSimDrvGfxInterfaceData or pstSimDrvGfxContext is NULL");
            break; // Failure;
        }

        if (sizeof(SIMDRVGFX_INTERFACE_DATA) != pstSimDrvGfxInterfaceData->ulSize)
        {
            GFXVALSIM_DBG_MSG("pstSimDrvGfxInterfaceData size mismatch!");
            break; // Failure;
        }

        // Check the compatibility
        // Not using MinCompatible Version Right now
        if (pstSimDrvGfxInterfaceData->ulSimDrvInterfaceVersion != GFX_SIMDRV_INTERFACE_VERSION)
        {
            break;
        }
        if (NULL == pstSimDrvGfxInterfaceData->pvGfxHwDev || NULL == pstSimDrvGfxInterfaceData->pGfxPhysicalDeviceObject)
        {
            GFXVALSIM_DBG_MSG("pstSimDrvGfxInterfaceData: pvGfxHwDev or pGfxPhysicalDeviceObject is NULL");
            break;
        }
        COMMONCORE_GetRegistryInfo(SIMDRV_REGKEY_FEATURE_CONTROL, REG_DWORD, &(pstSimDrvGfxContext->featureControl.ulValue), sizeof(DDU32));

        // Get Gfx adapter details
        if (STATUS_SUCCESS !=
            QueryDisplayAdapterDetails(pstSimDrvGfxInterfaceData->pGfxPhysicalDeviceObject, BusQueryDeviceID, gfxAdapterContext.PCIBusDeviceId)) // get PCI Bus Device ID
        {
            GFXVALSIM_DBG_MSG("Failed to get PCI bus query device id!");
            break;
        }
        if (STATUS_SUCCESS !=
            QueryDisplayAdapterDetails(pstSimDrvGfxInterfaceData->pGfxPhysicalDeviceObject, BusQueryInstanceID, gfxAdapterContext.PCIBusInstanceId)) // get PCI Bus Instance ID
        {
            GFXVALSIM_DBG_MSG("Failed to get PCI bus instance id!");
            break;
        }
        gfxAdapterContext.pvGfxHwDev           = pstSimDrvGfxInterfaceData->pvGfxHwDev;
        gfxAdapterContext.isDisplayLessAdapter = pstSimDrvGfxInterfaceData->isDisplayLessAdapter;
        gfxAdapterContext.displayOnlyDriver    = pstSimDrvGfxInterfaceData->displayOnlyDriver;
        gfxAdapterContext.gfxAdapterGuid       = pstSimDrvGfxInterfaceData->gfxAdapterGuid;
        gfxAdapterContext.gfxAdapterLuid       = pstSimDrvGfxInterfaceData->gfxAdapterLuid;
        gfxAdapterContext.pstSimDrvGfxContext  = pstSimDrvGfxContext;
        memcpy_s(&gfxAdapterContext.GfxExposedInterfaces, sizeof(GFX_EXPOSED_INTERFACES), &pstSimDrvGfxInterfaceData->stGfxExposedInterfaces, sizeof(GFX_EXPOSED_INTERFACES));

        if (FALSE == COMMONRxHANDLERS_InitSimulationDriverContext(&gfxAdapterContext, &gfxAdapterContext.pstRxInfoArr))
            break;
        if (FALSE == PERSISTENCEHANDLER_InitPeristenceContext(&gfxAdapterContext, &((PSIMDRV_PERSISTENCE_DATA)gfxAdapterContext.pvSimPersistenceData),
                                                              &((PSIMDRV_PERSISTENCE_DATA)gfxAdapterContext.pvSimPersistenceDataS3S4)))
            break;

        if (NULL == pstSimDrvGfxInterfaceData->stGfxExposedInterfaces.pfnGfxCb_GetPlatformInfo)
        {
            GFXVALSIM_DBG_MSG("pfnGfxCb_GetPlatformInfo is NULL!");
            break;
        }
        // Call Gfx to get the Platform
        if (FALSE == pstSimDrvGfxInterfaceData->stGfxExposedInterfaces.pfnGfxCb_GetPlatformInfo(pstSimDrvGfxInterfaceData->pvGfxHwDev, &stPlatformInfo))
        {
            GFXVALSIM_DBG_MSG("Failed to get platform details!");
            break;
        }

        GFXVALSIM_SYSTEM_INFO(stPlatformInfo.eProductFamily, stPlatformInfo.ePCHProductFamily);
        // Register SimDrv MMIO handling interfaces with Gfx
        // These two handlers are the hooks into Gfx's MMIO accesses
        // They will be initialized once the app tells us which platform
        // it wants to test things for
        pstSimDrvGfxInterfaceData->pfnSimDrvCb_GenericHandler = SIMDRVCB_GenericHandler;

        UpdateSimulationEnvironmentInfo(&gfxAdapterContext);
        if (VBTSIMULATION_GetOpregionDetails(&gfxAdapterContext, stPlatformInfo, &OpRegionVbtDetails) == TRUE)
        {
            DD_MEM_COPY_SAFE(&TempOpRegionVbtDetails, sizeof(OpRegionVbtDetails), &OpRegionVbtDetails, sizeof(OpRegionVbtDetails));

            // Store current VBT as default VBT. Cache this data at first instance of driver-valsim handshake
            if (VBTSIMULATION_IsDefaultVBTPresent(gfxAdapterContext, &TempOpRegionVbtDetails) == FALSE)
            {
                GFXVALSIM_DBG_MSG("Default VBT not present. Assuming current VBT as default and updating regkey");
                // load opregion data to Default vbt regkey
                VBTSIMULATION_WriteDefaultVBT(gfxAdapterContext, OpRegionVbtDetails.pVBTBase, OpRegionVbtDetails.VbtSize);
            }

            // Update Test VBT to be simulated
            VBTSIMULATION_ConfigureTestVBT(&gfxAdapterContext, &OpRegionVbtDetails, (BOOLEAN)pstSimDrvGfxContext->featureControl.VBTSimulation);

            // Store current VBT to actual VBT
            VBTSIMULATION_DumpVBTFromPCI(&gfxAdapterContext, &OpRegionVbtDetails);

            // Store OpRegion data
            VBTSIMULATION_DumpOpRegionFromPCI(&gfxAdapterContext, &OpRegionVbtDetails);

            if (OpRegionVbtDetails.bUnmapVirtualAddr == TRUE)
            {
                MmUnmapIoSpace(OpRegionVbtDetails.pOpregionBaseVirtualAddr, OpRegionVbtDetails.OpRegionSize);
            }
        }
        else
        {
            GFXVALSIM_DBG_MSG("Unable to Get Opregion Details!\r\n");
        }

        if (pstSimDrvGfxContext->featureControl.DisableSinkSimulation == FALSE)
        {
            // Ideally at this point We should be able to Parse the VBT and call COMMRXHANDLERS_SetRxInfo from here itself to keep all
            // data structure in Sink and not end up with inadvertent stale pointers because someone disabled and enabled the Gfx
            // in which case COMMONMMIOHANDLERS_InitMMIOInterfaceForPlatform and COMMONMMIOHANDLERS_RegisterPlatormBasedGeneralMMIOHandHandlers
            // will be called from here but COMMRXHANDLERS_SetRxInfo which gets called only from the App might end up having stale pointers
            // Currently trying to mitigate this using flags bInterfaceInitialized and bGeneralMMIOInitalized
            if (FALSE == COMMONMMIOHANDLERS_InitMMIOInterfaceForPlatform(gfxAdapterContext.pstRxInfoArr->pstMMIOInterface, stPlatformInfo))
            {
                break;
            }
            if (pstSimDrvGfxContext->featureControl.HybridSimulation == 0)
            {
                // Now Register the Basic Primary MMIO Handlers
                if (FALSE == COMMONMMIOHANDLERS_RegisterPlatormBasedGeneralMMIOHandHandlers(gfxAdapterContext.pstRxInfoArr->pstMMIOInterface))
                {
                    break;
                }

                if (pstSimDrvGfxContext->featureControl.InitMmioReg == 1)
                {
                    if (FALSE == InitializeTestMMIO(gfxAdapterContext, gfxAdapterContext.pstRxInfoArr->pstMMIOInterface))
                    {
                        GFXVALSIM_DBG_MSG("Unable to Initialize Test MMIO!\r\n");
                        // break;
                    }
                }
            }

            // If Persistence File is Already opened that we means we are getting a SIMDRVTOGFX_GfxCallBackRoutine
            // and landing here as a result of Gfx Driver disable/enable call and not reboot, in which case we should
            // skip reading from the persistence file. (Edp persistence requires reboot so this fix should not break
            // edp persistence.
            if (PERSISTENCEHANDLER_IsPersistenceFileOpen(&gfxAdapterContext) == FALSE)
            {
                if (FALSE == PERSISTENCEHANDLER_ReadPeristenceDataFromDisk(&gfxAdapterContext))
                {
                    break;
                }

                if (FALSE == PERSISTENCEHANDLER_ReconstructSinkConfigFromPersistenceData(&gfxAdapterContext))
                {
                    break;
                }
            }
        }
        pstSimDrvGfxInterfaceData->pvSimDrvToGfxContext = pstSimDrvGfxContext; /* Share Sim Driver Context with Gfx driver */
        pstSimDrvGfxContext->pfnUpdateAdapterContext(pstSimDrvGfxContext, GFX_ADAPTER_SERVICE_ADD, &gfxAdapterContext);
    } while (FALSE);

    if (pstSimDrvGfxInterfaceData->pEventSimDrvDone)
    {
        // Using OS API makes this part of the code non portable. But this file has a lot of OS api's anyways that make it non portable
        KeSetEvent(pstSimDrvGfxInterfaceData->pEventSimDrvDone, PRIORITY_NO_INCREMENT, FALSE);
    }
    GFXVALSIM_FUNC_EXIT(0);
    return;
}

/*
 * @brief         Interface to query adapter details
 * @param[in]     PDO of display driver
 * @param[in]     Query Type
 * @param[out]    WCHAR Buffer
 * @return        NTSTATUS
 */
NTSTATUS QueryDisplayAdapterDetails(IN PDEVICE_OBJECT pPhysicalDeviceObject, BUS_QUERY_ID_TYPE queryType, WCHAR *pBuffer)
{
    NTSTATUS           ntStatus = STATUS_UNSUCCESSFUL;
    KEVENT             queryEvent;
    IO_STATUS_BLOCK    ioStatusBlock = { 0 };
    PIRP               pIrp          = NULL;
    PIO_STACK_LOCATION pIrpSp        = NULL;
    LARGE_INTEGER      timeout       = { 0 };
    GFXVALSIM_FUNC_ENTRY();
    do
    {
        if (NULL == pPhysicalDeviceObject || NULL == pBuffer)
            break;

        timeout.QuadPart = (-1000000); // 100 ms timeout for wait for KeWaitForSingleObject

        KeInitializeEvent(&queryEvent, SynchronizationEvent, FALSE);
        pIrp = IoBuildSynchronousFsdRequest(IRP_MJ_PNP, pPhysicalDeviceObject, NULL, 0, NULL, &queryEvent, &ioStatusBlock);
        if (NULL == pIrp)
            break;

        pIrp->IoStatus.Status      = STATUS_NOT_SUPPORTED;
        pIrp->IoStatus.Information = 0;

        pIrpSp = IoGetNextIrpStackLocation(pIrp);

        pIrpSp->MajorFunction             = IRP_MJ_PNP;
        pIrpSp->MinorFunction             = IRP_MN_QUERY_ID;
        pIrpSp->Parameters.QueryId.IdType = queryType;

        ntStatus = IoCallDriver(pPhysicalDeviceObject, pIrp);
        if (ntStatus == STATUS_PENDING)
        {
            KeWaitForSingleObject(&queryEvent, Executive, KernelMode, FALSE, &timeout);
            ntStatus = pIrp->IoStatus.Status;
        }
        if (ntStatus == STATUS_SUCCESS)
        {
            ntStatus = wcscpy_s(pBuffer, (wcslen((WCHAR *)ioStatusBlock.Information) + 1), (WCHAR *)ioStatusBlock.Information);
        }
    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(0);
    return ntStatus;
}

//===============================================================================================
//
// Function: SIMDRVTOGFX_GfxStatusNofitication
//
// Description:
//      SIMDRVTOGFX_GfxStatusNofitication is a callback function called by graphics driver to
//      indicate its status. Possible reasons - Graphics driver unloading, PM entry or PM exit.
//
// Parameters:
//      pDeviceObj - Void Pointer to Simulation device object
//
// Returns:
//      Appropriate NTSTATUS value
//===============================================================================================
NTSTATUS SIMDRVTOGFX_GfxStatusNofitication(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSIMDRV_GFX_STATUS_ARGS pstGfxStatusArgs)
{
    NTSTATUS ntStatus = STATUS_UNSUCCESSFUL;
    do
    {
        if (pGfxAdapterContext == NULL)
            break;
        if (pstGfxStatusArgs->eSimDrvOrGfxReady == SIMDRV_GFX_READY && pstGfxStatusArgs->eReadyReason == SIMDRV_GFX_READY_DRV_LOADED)
        {
            pGfxAdapterContext->bIsGfxReady = TRUE;
        }
        else
        {
            VBTSIMULATION_Cleanup(pGfxAdapterContext);
            pGfxAdapterContext->bIsGfxReady = FALSE;

            UpdateAdapterContext(pGfxAdapterContext->pstSimDrvGfxContext, GFX_ADAPTER_SERVICE_REMOVE, pGfxAdapterContext);
        }
        ntStatus = STATUS_SUCCESS;
    } while (FALSE);
    return ntStatus;
}

BOOLEAN SIMDRVTOGFX_GfxReadMMIOHandler(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, ULONG ulRegOffset, PULONG pulRegVal, bool *pbStateModified)
{

    BOOLEAN            bRet                 = TRUE;
    BOOLEAN            bHandlerFound        = FALSE;
    PMMIO_HANDLER_INFO pstMMIOHandlerInfo   = NULL;
    REGRW_EXEC_SITE    eRegRWExecSite       = eExecHW;
    ULONG              ulNumCurrentHandlers = 0;
    ULONG              ulCount = 0, ulTempData = 0;

    do
    {
        *pbStateModified = false;

        if (pGfxAdapterContext == NULL)
        {
            // Critical Error
            return FALSE;
        }

        if (((PSIMDRVGFX_CONTEXT)pGfxAdapterContext->pstSimDrvGfxContext)->featureControl.DisableSinkSimulation == TRUE || pGfxAdapterContext->bIsGfxReady == FALSE)
        {
            break;
        }

        pstMMIOHandlerInfo   = pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface->stMMIOHandlerArr.stMMIOHandlerList;
        ulNumCurrentHandlers = pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface->stMMIOHandlerArr.ulNumRegisteredHandlers;

        for (ulCount = 0; ulCount < ulNumCurrentHandlers; ulCount++)
        {
            if (ulRegOffset >= pstMMIOHandlerInfo[ulCount].ulMMIOStartOffset && ulRegOffset <= pstMMIOHandlerInfo[ulCount].ulMMIOEndOffset)
            {
                bHandlerFound = TRUE;
                break;
            }
        }

        if (bHandlerFound && pstMMIOHandlerInfo[ulCount].pfnMMIOReadHandler)
        {
            eRegRWExecSite                           = eNoExecHw;
            pstMMIOHandlerInfo[ulCount].pAdapterInfo = pGfxAdapterContext;
            bRet                                     = pstMMIOHandlerInfo[ulCount].pfnMMIOReadHandler(&pstMMIOHandlerInfo[ulCount], ulRegOffset, pulRegVal, &eRegRWExecSite);
        }
        else if (bHandlerFound && pstMMIOHandlerInfo[ulCount].bReadHandlerlessRegistration)
        {
            *pulRegVal = *((PULONG)&pstMMIOHandlerInfo->stGlobalMMORegData.ucMMIORegisterFile[ulRegOffset - pstMMIOHandlerInfo->stGlobalMMORegData.ulMMIOBaseOffset]);

            eRegRWExecSite = pstMMIOHandlerInfo[ulCount].eRegReadExecSite;
        }

    } while (FALSE);

    if (eRegRWExecSite != eNoExecHw)
    {
        ulTempData = *pulRegVal;

        bRet = SIMDRVTOGFX_HwMmioAccess(pGfxAdapterContext, ulRegOffset, pulRegVal, SIMDRV_GFX_ACCESS_REQUEST_READ);

        if (eRegRWExecSite == eReadCombine)
        {
            *pulRegVal = *pulRegVal | ulTempData;
        }
    }
    if (bHandlerFound && eRegRWExecSite != eExecHW)
    {
        *pbStateModified = true;
    }
    return bRet;
}

BOOLEAN SIMDRVTOGFX_GfxWriteMMIOHandler(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, ULONG ulRegOffset, ULONG ulRegVal, bool *pbStateModified)
{
    BOOLEAN                    bRet                 = TRUE;
    BOOLEAN                    bHandlerFound        = FALSE;
    PMMIO_HANDLER_INFO         pstMMIOHandlerInfo   = NULL;
    REGRW_EXEC_SITE            eRegRWExecSite       = eExecHW;
    ULONG                      ulNumCurrentHandlers = 0;
    ULONG                      ulCount              = 0;
    PGLOBAL_MMIO_REGISTER_DATA pstGlobalMMORegData  = NULL;

    do
    {
        *pbStateModified = false;

        if (pGfxAdapterContext == NULL)
        {
            return FALSE;
        }

        if (((PSIMDRVGFX_CONTEXT)pGfxAdapterContext->pstSimDrvGfxContext)->featureControl.DisableSinkSimulation == TRUE)
        {
            break;
        }

        pstGlobalMMORegData  = &(pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface->stGlobalMMORegData);
        pstMMIOHandlerInfo   = pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface->stMMIOHandlerArr.stMMIOHandlerList;
        ulNumCurrentHandlers = pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface->stMMIOHandlerArr.ulNumRegisteredHandlers;

        for (ulCount = 0; ulCount < ulNumCurrentHandlers; ulCount++)
        {
            if (ulRegOffset >= pstMMIOHandlerInfo[ulCount].ulMMIOStartOffset && ulRegOffset <= pstMMIOHandlerInfo[ulCount].ulMMIOEndOffset)
            {
                bHandlerFound = TRUE;
                break;
            }
        }
        if (bHandlerFound && pstMMIOHandlerInfo[ulCount].pfnMMIOWriteHandler)
        {

            eRegRWExecSite                           = eNoExecHw;
            pstMMIOHandlerInfo[ulCount].pAdapterInfo = pGfxAdapterContext;

            bRet = pstMMIOHandlerInfo[ulCount].pfnMMIOWriteHandler(&pstMMIOHandlerInfo[ulCount], ulRegOffset, ulRegVal, &eRegRWExecSite);
        }
        else
        {

            // We record the Write for any Reg offset that didn't have a write handler registerd for it
            // We primarily do this Because the read handler for the same Register might want to know the values previously written to this offset
            // This will also come in handing for debugging and logging

            // If a Write Handler was registered for a given MMIO, the handler is supposed to write to the Global MMIO Register buffer/File
            //*****Every Registered Write Handler Should do this
            if (ulRegOffset >= pstGlobalMMORegData->ulMMIOBaseOffset && (ulRegOffset - pstGlobalMMORegData->ulMMIOBaseOffset) < GFX_MMIO_FILE_SIZE)
            {
                *((PULONG)&pstGlobalMMORegData->ucMMIORegisterFile[ulRegOffset - pstGlobalMMORegData->ulMMIOBaseOffset]) = ulRegVal;
            }
        }

    } while (FALSE);

    if (eRegRWExecSite != eNoExecHw)
    {
        bRet = SIMDRVTOGFX_HwMmioAccess(pGfxAdapterContext, ulRegOffset, &ulRegVal, SIMDRV_GFX_ACCESS_REQUEST_WRITE);
    }
    if (bHandlerFound && eRegRWExecSite == eNoExecHw)
    {
        *pbStateModified = true;
    }
    return bRet;
}

// This will Called via App initiated IOCTL to generate HPD
BOOLEAN SIMDRVTOGFX_GenerateHPDorSPI(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PORT_TYPE ePortType, BOOLEAN bHPD, BOOLEAN bAttachOrDetach, PORT_CONNECTOR_INFO PortConnectorInfo)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };

    GFXVALSIM_FUNC_ENTRY();

    do
    {
        if (pGfxAdapterContext == NULL || pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler == NULL ||
            pGfxAdapterContext->bIsGfxReady == FALSE) // && Port Type Range Check?
        {
            break;
        }

        if (COMMONMMIOHANDLERS_SetupInterruptRegistersForHPDorSPI(pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface, ePortType, bAttachOrDetach, bHPD, PortConnectorInfo))
        {
            // Missed polling on Master Interrupt Control Enable bit to see if Gfx Interrupts are enabled
            // Generate the interrupt only when DDI is active. TBD
            stGfxCallbackArgs.eGfxCbEvent = GenerateInterrupt;
            bRet                          = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);

            if (FALSE == bRet)
            {
                GFXVALSIM_DBG_MSG("GenerateInterrupt callback pfnGfxCb_GenericHandler failed");
            }
        }
        else
        {
            GFXVALSIM_DBG_MSG("COMMONMMIOHANDLERS_SetupInterruptRegistersForHPDorSPI() failed");
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

// This will Called via App initiated IOCTL to generate ESD
BOOLEAN SIMDRVTOGFX_GenerateTE(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, MIPI_DSI_PORT_TYPE ePortType)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };

    GFXVALSIM_FUNC_ENTRY();

    do
    {
        if (pGfxAdapterContext == NULL || pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler == NULL ||
            pGfxAdapterContext->bIsGfxReady == FALSE) // && Port Type Range Check?
        {
            break;
        }

        if (COMMONMMIOHANDLERS_SetupInterruptRegistersForTE(pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface, ePortType))
        {
            // Missed polling on Master Interrupt Control Enable bit to see if Gfx Interrupts are enabled
            // Generate the interrupt only when DDI is active. TBD
            stGfxCallbackArgs.eGfxCbEvent = GenerateInterrupt;
            bRet                          = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);

            if (FALSE == bRet)
            {
                GFXVALSIM_DBG_MSG("GenerateInterrupt callback pfnGfxCb_GenericHandler failed");
            }
        }
        else
        {
            GFXVALSIM_DBG_MSG("COMMONMMIOHANDLERS_SetupInterruptRegistersForTE() failed");
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}

BOOLEAN SIMDRVTOGFX_GfxPowerStateNotification(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, DEVICE_POWER_STATE eGfxPowerState, POWER_ACTION eActionType)
{
    BOOLEAN bRet = FALSE;
    if (NULL == pGfxAdapterContext)
    {
        GFXVALSIM_DBG_MSG("GfxAdapterContext is NULL");
        return bRet;
    }
    pGfxAdapterContext->devicePowerState = (ULONG)eGfxPowerState;
    pGfxAdapterContext->powerAction      = (ULONG)eActionType;

    bRet = COMMRXHANDLERS_GfxPowerStateNotification(pGfxAdapterContext->pstRxInfoArr, eGfxPowerState, eActionType);

    if (bRet)
    {
        bRet = PERSISTENCEHANDLER_UpdatePeristenceWithS3S4ResumeData(pGfxAdapterContext->pvSimPersistenceData, pGfxAdapterContext->pvSimPersistenceDataS3S4,
                                                                     pGfxAdapterContext->pstRxInfoArr, eGfxPowerState, eActionType);
    }
    return bRet;
}

BOOLEAN SIMDRVTOGFX_CleanUp(PSIMDRVGFX_CONTEXT pstSimDrvGfxContext)
{
    GFX_ADAPTER_CONTEXT gfxAdapterContext = { 0 };
    PPORTINGLAYER_OBJ   pstPortingObj     = GetPortingObj();
    do
    {
        if (NULL == pstSimDrvGfxContext || NULL == pstPortingObj)
            break;

        /* Notify Sim driver unload status to all adapters */
        for (INT adapterIndex = 0; adapterIndex < pstSimDrvGfxContext->gfxAdapterCount; adapterIndex++)
        {
            gfxAdapterContext = pstSimDrvGfxContext->GfxAdapterContext[adapterIndex];
            if (gfxAdapterContext.bIsGfxReady)
            {
                gfxAdapterContext.GfxExposedInterfaces.pfnSimDrvCb_SimDrvtaStusNotification(gfxAdapterContext.pvGfxHwDev);
            }

            /* Close persistence file handle */
            pstPortingObj->pfnFileClose(&((PSIMDRV_PERSISTENCE_DATA)gfxAdapterContext.pvSimPersistenceData)->stPersistenceFileHandle);

            COMMRXHANDLERS_CleanUpAllPorts(gfxAdapterContext.pstRxInfoArr);
            COMMONMMIOHANDLERS_CleanUp(gfxAdapterContext.pstRxInfoArr->pstMMIOInterface);
            // Cleanup Normal Persistence Data
            PERSISTENCEHANDLER_CleanUpAllPorts(gfxAdapterContext.pvSimPersistenceData);
            // Cleanup S3S4 Persistence Data
            PERSISTENCEHANDLER_CleanUpAllPorts(gfxAdapterContext.pvSimPersistenceDataS3S4);

            pstPortingObj->pfnFreeMem(gfxAdapterContext.pstRxInfoArr->pstMMIOInterface);
            gfxAdapterContext.pstRxInfoArr->pstMMIOInterface = NULL;

            pstPortingObj->pfnFreeMem(gfxAdapterContext.pstRxInfoArr);
            gfxAdapterContext.pstRxInfoArr = NULL;

            pstPortingObj->pfnFreeMem(gfxAdapterContext.pvSimPersistenceData);
            gfxAdapterContext.pvSimPersistenceData = NULL;

            pstPortingObj->pfnFreeMem(gfxAdapterContext.pvSimPersistenceDataS3S4);
            gfxAdapterContext.pvSimPersistenceDataS3S4 = NULL;

            VBTSIMULATION_Cleanup(&gfxAdapterContext);
        }
    } while (FALSE);

    return TRUE;
}

NTSTATUS SIMDRVTOGFX_EnableDisableGfxSimulationMode(BOOLEAN bSetGfxSimMode)
{
    ULONG ulEnableDisableSimMode = (ULONG)bSetGfxSimMode;
    return COMMONCORE_SetRegistryInfo(SIMDRV_REG_KEYNAME, REG_DWORD, &ulEnableDisableSimMode, sizeof(DWORD));
}

BOOLEAN SIMDRVTOGFX_Display_Hooks(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };
    do
    {
        if (pGfxAdapterContext == NULL || pInputBuffer == NULL || pGfxAdapterContext->bIsGfxReady == FALSE ||
            pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler == NULL) // && Port Type Range Check?
        {
            break;
        }

        stGfxCallbackArgs.eGfxCbEvent         = DisplayHooks;
        stGfxCallbackArgs.stSimDrvDisplayArgs = pInputBuffer;
        bRet                                  = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);
        DD_MEM_COPY_SAFE(pInputBuffer, bufferSize, stGfxCallbackArgs.stSimDrvDisplayArgs, bufferSize);
    } while (FALSE);

    return bRet;
}

BOOLEAN SIMDRVTOGFX_Trigger_Dsb(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };
    do
    {
        if (pGfxAdapterContext == NULL || pInputBuffer == NULL || pGfxAdapterContext->bIsGfxReady == FALSE ||
            pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler == NULL)
        {
            break;
        }

        stGfxCallbackArgs.eGfxCbEvent         = TriggerDSB;
        stGfxCallbackArgs.stSimDrvDisplayArgs = pInputBuffer;
        bRet                                  = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);
        DD_MEM_COPY_SAFE(pInputBuffer, bufferSize, stGfxCallbackArgs.stSimDrvDisplayArgs, bufferSize);

    } while (FALSE);

    return bRet;
}

BOOLEAN SIMDRVTOGFX_GfxReadOPRomRegion(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, UCHAR *pBuffer, ULONG ulOffset, ULONG ulSize, ULONG *ulBytesRead)
{
    BOOLEAN               bRet              = FALSE;
    PEXPANSION_ROM_HEADER pROMBuffer        = NULL;
    GFXCALLBACK_ARGS      stGfxCallbackArgs = { 0 };

    do
    {
        if (pGfxAdapterContext == NULL || pBuffer == NULL || pGfxAdapterContext->bIsGfxReady == FALSE)
        {
            break;
        }

        // VBTSIMULATION_GetROMDataFromPCIROM(pGfxAdapterContext);
        pROMBuffer = pGfxAdapterContext->pvExpansionRomHeader;

        GFXVALSIM_DBG_MSG("ReadOPROM: ulOffset:%uld, ulSize:%uld, pBuffer: %p, pROMBuffer: %p, OPRomTotalSize: %uld", ulOffset, ulSize, (void *)pBuffer, (void *)pROMBuffer,
                          pGfxAdapterContext->OPRomTotalSize);

        if (pROMBuffer == NULL)
        {
            GFXVALSIM_DBG_MSG("SIMDRVTOGFX_GfxReadOPRomRegion: OPROM not initialized!");
            break;
            // stGfxCallbackArgs.eGfxCbEvent                     = ReadOPROM;
            // stGfxCallbackArgs.stSimReadPCIConfigArgs.ulSize   = ulSize;
            // stGfxCallbackArgs.stSimReadPCIConfigArgs.ulOffset = ulOffset;
            // stGfxCallbackArgs.stSimReadPCIConfigArgs.pBuffer  = pBuffer;

            //// Call Gfx Interface to read PCI ROM config space
            // bRet = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);

            // if (bRet == FALSE)
            //{
            //    GFXVALSIM_DBG_MSG("SIMDRVTOGFX_GfxReadOPRomRegion: Failed to read OPROM memory!\r\n");
            //    break;
            //}

            //(*ulBytesRead) = ulSize;
        }

        if (pGfxAdapterContext->OPRomTotalSize < (ulOffset + ulSize))
        {
            GFXVALSIM_DBG_MSG("SIMDRVTOGFX_GfxReadOPRomRegion: OPROM size less than read size!");
            break;
            // stGfxCallbackArgs.eGfxCbEvent                     = ReadOPROM;
            // stGfxCallbackArgs.stSimReadPCIConfigArgs.ulSize   = ulSize;
            // stGfxCallbackArgs.stSimReadPCIConfigArgs.ulOffset = ulOffset;
            // stGfxCallbackArgs.stSimReadPCIConfigArgs.pBuffer  = pBuffer;

            //// Call Gfx Interface to read PCI ROM config space
            // bRet = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);

            // if (bRet == FALSE)
            //{
            //    GFXVALSIM_DBG_MSG("SIMDRVTOGFX_GfxReadOPRomRegion: Failed to read OPROM memory!\r\n");
            //    break;
            //}

            //(*ulBytesRead) = ulSize;
        }

        memcpy(pBuffer, ((DDU8 *)pROMBuffer + ulOffset), ulSize);
        bRet           = TRUE;
        (*ulBytesRead) = ulSize;

    } while (FALSE);

    return bRet;
}

BOOLEAN SIMDRVTOGFX_MMIO_Access(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };
    do
    {
        if (pGfxAdapterContext == NULL || NULL == pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler ||
            pInputBuffer == NULL) //|| pGfxAdapterContext->bIsGfxReady == FALSE)
        {
            GFXVALSIM_DBG_MSG("Input buffer is NULL!");
            break;
        }

        stGfxCallbackArgs.eGfxCbEvent         = MMIOAccess;
        stGfxCallbackArgs.stSimDrvDisplayArgs = (PSIMDRV_MMIO_ACCESS_ARGS)pInputBuffer;
        bRet                                  = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);
        DD_MEM_COPY_SAFE(pInputBuffer, bufferSize, stGfxCallbackArgs.stSimDrvDisplayArgs, bufferSize);
    } while (FALSE);

    return bRet;
}

BOOLEAN SIMDRVTOGFX_WAKE_LOCK_Access(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };
    GFXVALSIM_DBG_MSG("In SIMDRVTOGFX_WAKE_LOCK_Access!");
    do
    {
        if (pGfxAdapterContext == NULL || NULL == pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler ||
            pInputBuffer == NULL) //|| pGfxAdapterContext->bIsGfxReady == FALSE)
        {
            GFXVALSIM_DBG_MSG("Input buffer is NULL!");
            break;
        }
        stGfxCallbackArgs.eGfxCbEvent         = WakeLock;
        stGfxCallbackArgs.stSimDrvDisplayArgs = pInputBuffer;
        bRet                                  = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);
        DD_MEM_COPY_SAFE(pInputBuffer, bufferSize, stGfxCallbackArgs.stSimDrvDisplayArgs, bufferSize);
    } while (FALSE);

    return bRet;
}

BOOLEAN SIMDRVTOGFX_HwMmioAccess(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, ULONG ulRegOffset, PULONG pulRegValue, SIMDRV_GFX_ACCESS_REQUEST_TYPE simRequestType)
{
    BOOLEAN bRet = FALSE;

    if (pGfxAdapterContext == NULL || pulRegValue == NULL)
    {
        return FALSE;
    }

    SIMDRV_MMIO_ACCESS_ARGS mmio_access_args = { 0 };
    ULONG                   driverRegValue   = 0;
    mmio_access_args.accessType              = simRequestType;
    mmio_access_args.offset                  = ulRegOffset;
    mmio_access_args.pValue                  = pulRegValue;

    bRet = SIMDRVTOGFX_MMIO_Access(pGfxAdapterContext, &mmio_access_args, sizeof(SIMDRV_MMIO_ACCESS_ARGS));

    return bRet;
}

/*
 * @brief         Interface to get adapter context for given adapter device id and instance id
 * @param[in]     Pointer to SimDrvGfxContext
 * @param[in]     PCIBusDeviceId
 * @param[in]     PCIBusInstanceId
 * @return        Pointer to GFX_ADAPTER_CONTEXT
 */
PGFX_ADAPTER_CONTEXT GetAdapterContext(SIMDRVGFX_CONTEXT *pstSimDrvGfxContext, WCHAR *pPCIBusDeviceId, WCHAR *pPCIBusInstanceId)
{
    PGFX_ADAPTER_CONTEXT pGfxAdapterContext = NULL;
    do
    {
        if (NULL == pstSimDrvGfxContext || NULL == pPCIBusDeviceId || NULL == pPCIBusInstanceId)
            break;

        for (INT index = 0; index < pstSimDrvGfxContext->gfxAdapterCount; index++)
        {
            /* To Do: Add PCI Bus Instance ID check in future when Gfx driver enumerates multiple adapter with same device ID  */
            if (STATUS_SUCCESS == wcscmp(pstSimDrvGfxContext->GfxAdapterContext[index].PCIBusDeviceId, pPCIBusDeviceId))
            {
                pGfxAdapterContext = &(pstSimDrvGfxContext->GfxAdapterContext[index]);
                break;
            }
        }
        if (NULL == pGfxAdapterContext)
        {
            GFXVALSIM_DBG_MSG("Required adapter context not present in lookup table");
        }

    } while (FALSE);
    return pGfxAdapterContext;
}

PGFX_ADAPTER_CONTEXT GetAdapterContextEx(SIMDRVGFX_CONTEXT *pstSimDrvGfxContext, PVOID pvGfxHwDev)
{
    PGFX_ADAPTER_CONTEXT pGfxAdapterContext = NULL;

    do
    {
        if (NULL == pstSimDrvGfxContext || NULL == pvGfxHwDev)
            break;

        for (INT index = 0; index < pstSimDrvGfxContext->gfxAdapterCount; index++)
        {
            /* To Do: Add PCI Bus Instance ID check in future when Gfx driver enumerates multiple adapter with same device ID  */
            if (pvGfxHwDev == pstSimDrvGfxContext->GfxAdapterContext[index].pvGfxHwDev)
            {
                pGfxAdapterContext = &(pstSimDrvGfxContext->GfxAdapterContext[index]);
                break;
            }
        }
        if (NULL == pGfxAdapterContext)
        {
            GFXVALSIM_DBG_MSG("Required adapter context not present in lookup table");
        }

    } while (FALSE);
    return pGfxAdapterContext;
}

/*
 * @brief         Interface to update adapter context lookup table
 * @param[in]     Pointer to SimDrvGfxContext
 * @param[in]     Request Type
 * @param[in]     Gfx Adapter Info
 * @return        VOID
 */
VOID UpdateAdapterContext(SIMDRVGFX_CONTEXT *pstSimDrvGfxContext, GFX_ADAPTER_SERVICE_TYPE requestType, PGFX_ADAPTER_CONTEXT pGfxAdapterContext)
{
    BOOLEAN              adapterContextExists = FALSE;
    PGFX_ADAPTER_CONTEXT pAliveAdapterContext = NULL;
    INT                  index                = 0;
    do
    {
        if (NULL == pstSimDrvGfxContext || NULL == pGfxAdapterContext || requestType >= GFX_ADAPTER_SERVICE_MAX)
            break;

        if (requestType == GFX_ADAPTER_SERVICE_ADD)
        {
            pAliveAdapterContext = GetAdapterContext(pstSimDrvGfxContext, pGfxAdapterContext->PCIBusDeviceId, pGfxAdapterContext->PCIBusInstanceId);
            if (pAliveAdapterContext != NULL) /* Adapter details already in lookup table */
            {
                GFXVALSIM_DBG_MSG("Adapter context already present in lookup table");
                /* Update new adapter details in existing index */
                memcpy_s(pAliveAdapterContext, sizeof(GFX_ADAPTER_CONTEXT), pGfxAdapterContext, sizeof(GFX_ADAPTER_CONTEXT));
            }
            else
            {
                for (; index < MAX_SUPPORTED_ADAPTERS; index++)
                {
                    if (pstSimDrvGfxContext->GfxAdapterContext[index].pvGfxHwDev == NULL)
                        break;
                }
                if (index >= MAX_SUPPORTED_ADAPTERS)
                {
                    GFXVALSIM_DBG_MSG("UpdateAdapterContext Index Out of Range");
                    break;
                }
                memcpy_s(&pstSimDrvGfxContext->GfxAdapterContext[index], sizeof(GFX_ADAPTER_CONTEXT), pGfxAdapterContext, sizeof(GFX_ADAPTER_CONTEXT));
                pstSimDrvGfxContext->gfxAdapterCount++;
                GFXVALSIM_DBG_MSG("Gfx adapter details: device_id=%s instance_id:%s added in lookup table", pGfxAdapterContext->PCIBusDeviceId,
                                  pGfxAdapterContext->PCIBusInstanceId);
            }
        }
        else if (requestType == GFX_ADAPTER_SERVICE_REMOVE)
        {
            for (; index < pstSimDrvGfxContext->gfxAdapterCount; index++)
            {
                if (pstSimDrvGfxContext->GfxAdapterContext[index].pvGfxHwDev == pGfxAdapterContext->pvGfxHwDev)
                    break;
            }

            if (index < pstSimDrvGfxContext->gfxAdapterCount) /* element present in array */
            {
                GFXVALSIM_DBG_MSG("Gfx adapter details present in lookup table, removing only gfx details from lookup table");
                pstSimDrvGfxContext->GfxAdapterContext[index].bIsGfxReady = FALSE;
                pstSimDrvGfxContext->GfxAdapterContext[index].pvGfxHwDev  = NULL;
                memset(&pstSimDrvGfxContext->GfxAdapterContext[index].GfxExposedInterfaces, 0, sizeof(GFX_EXPOSED_INTERFACES));
            }
            else
            {
                GFXVALSIM_DBG_MSG("Gfx adapter details not present in lookup table!");
            }
        }

    } while (FALSE);
}

NTSTATUS SIMDRVCB_GenericHandlerArgsSizeCheck(SIMDRV_CB_GENERIC_HANDLER_ARGS *pSimDrvCbGenericHandlerArgs)
{
    NTSTATUS ntStatus = STATUS_SUCCESS;
    do
    {
        if (NULL == pSimDrvCbGenericHandlerArgs)
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        switch (pSimDrvCbGenericHandlerArgs->SimDrvCbRequestType)
        {
        case SIMDRV_CB_REQUEST_GFX_POWER_STATE:
            if (sizeof(PSIMDRV_CB_POWER_STATE_ARGS) != sizeof(pSimDrvCbGenericHandlerArgs->SimDrvCbPowerStateArgs))
            {
                GFXVALSIM_DBG_MSG("SIMDRVCB_GenericHandler power state args size mismatch");
                ntStatus = STATUS_UNSUCCESSFUL;
            }
            break;
        case SIMDRV_CB_REQUEST_GFX_STATE:
            if (sizeof(SIMDRV_GFX_STATUS_ARGS) != sizeof(pSimDrvCbGenericHandlerArgs->SimDrvCbGfxStatusArgs))
            {
                GFXVALSIM_DBG_MSG("SIMDRVCB_GenericHandler gfx state args size mismatch");
                ntStatus = STATUS_UNSUCCESSFUL;
            }
            break;
        case SIMDRV_CB_REQUEST_GFX_READ_MMIO:
        case SIMDRV_CB_REQUEST_GFX_WRITE_MMIO:
            if (sizeof(SIMDRV_CB_MMIO_ARGS) != sizeof(pSimDrvCbGenericHandlerArgs->SimDrvCbMmioArgs))
            {
                GFXVALSIM_DBG_MSG("SIMDRVCB_GenericHandler mmio access args size mismatch");
                ntStatus = STATUS_UNSUCCESSFUL;
            }
            break;
        case SIMDRV_CB_REQUEST_READ_OP_ROM:
            if (sizeof(SIMDRV_CB_OPROM_ARGS) != sizeof(pSimDrvCbGenericHandlerArgs->SimDrvCbOpRomArgs))
            {
                GFXVALSIM_DBG_MSG("SIMDRVCB_GenericHandler read oprom args size mismatch");
                ntStatus = STATUS_UNSUCCESSFUL;
            }
            break;
        default:
            GFXVALSIM_DBG_MSG("SIMDRVCB_GenericHandler invalid request type");
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }
    } while (FALSE);
    return ntStatus;
}

NTSTATUS SIMDRVCB_GenericHandler(void *pvSimDrvContext, void *pGfxHwDev, SIMDRV_CB_GENERIC_HANDLER_ARGS *pSimDrvCbGenericHandlerArgs)
{
    NTSTATUS             ntStatus           = STATUS_UNSUCCESSFUL;
    SIMDRV_CB_OPROM_ARGS OpRomArgs          = { 0 };
    PGFX_ADAPTER_CONTEXT pGfxAdapterContext = NULL;
    PSIMDRVGFX_CONTEXT   pSimDrvGfxContext  = NULL;

    do
    {
        if (NULL == pvSimDrvContext || NULL == pGfxHwDev || NULL == pSimDrvCbGenericHandlerArgs)
            break;

        if (STATUS_SUCCESS != SIMDRVCB_GenericHandlerArgsSizeCheck(pSimDrvCbGenericHandlerArgs))
            break;

        pGfxAdapterContext = ((PSIMDRVGFX_CONTEXT)pvSimDrvContext)->pfnGetAdapterContextEx(pvSimDrvContext, pGfxHwDev);
        if (NULL == pGfxAdapterContext)
        {
            return STATUS_UNSUCCESSFUL;
        }

        switch (pSimDrvCbGenericHandlerArgs->SimDrvCbRequestType)
        {
        case SIMDRV_CB_REQUEST_GFX_POWER_STATE:
            ntStatus = (SIMDRVTOGFX_GfxPowerStateNotification(pGfxAdapterContext, pSimDrvCbGenericHandlerArgs->SimDrvCbPowerStateArgs.DevicePowerState,
                                                              pSimDrvCbGenericHandlerArgs->SimDrvCbPowerStateArgs.ActionType) == TRUE) ?
                       STATUS_SUCCESS :
                       STATUS_UNSUCCESSFUL;
            break;
        case SIMDRV_CB_REQUEST_GFX_STATE:
            ntStatus = SIMDRVTOGFX_GfxStatusNofitication(pGfxAdapterContext, &pSimDrvCbGenericHandlerArgs->SimDrvCbGfxStatusArgs);
            break;
        case SIMDRV_CB_REQUEST_GFX_READ_MMIO:
            ntStatus =
            (SIMDRVTOGFX_GfxReadMMIOHandler(pGfxAdapterContext, pSimDrvCbGenericHandlerArgs->SimDrvCbMmioArgs.ulRegOffset, pSimDrvCbGenericHandlerArgs->SimDrvCbMmioArgs.pulRegVal,
                                            &pSimDrvCbGenericHandlerArgs->SimDrvCbMmioArgs.bStateModified) == TRUE) ?
            STATUS_SUCCESS :
            STATUS_UNSUCCESSFUL;
            break;
        case SIMDRV_CB_REQUEST_GFX_WRITE_MMIO:
            ntStatus =
            (SIMDRVTOGFX_GfxWriteMMIOHandler(pGfxAdapterContext, pSimDrvCbGenericHandlerArgs->SimDrvCbMmioArgs.ulRegOffset,
                                             *pSimDrvCbGenericHandlerArgs->SimDrvCbMmioArgs.pulRegVal, &pSimDrvCbGenericHandlerArgs->SimDrvCbMmioArgs.bStateModified) == TRUE) ?
            STATUS_SUCCESS :
            STATUS_UNSUCCESSFUL;
            break;
        case SIMDRV_CB_REQUEST_READ_OP_ROM:
            OpRomArgs = pSimDrvCbGenericHandlerArgs->SimDrvCbOpRomArgs;
            ntStatus  = (SIMDRVTOGFX_GfxReadOPRomRegion(pGfxAdapterContext, OpRomArgs.pBuffer, OpRomArgs.ulOffset, OpRomArgs.ulSize, OpRomArgs.pulBytesRead) == TRUE) ?
                       STATUS_SUCCESS :
                       STATUS_UNSUCCESSFUL;
            break;
        default:
            GFXVALSIM_DBG_MSG("SIMDRVCB_GenericHandler invalid request type");
            break;
        }
    } while (FALSE);
    return ntStatus;
}

BOOLEAN SIMDRVTOGFX_Trigger_MIPI_DSI_Commands(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };
    do
    {
        if (pGfxAdapterContext == NULL || pInputBuffer == NULL || pGfxAdapterContext->bIsGfxReady == FALSE ||
            pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler == NULL)
        {
            break;
        }

        stGfxCallbackArgs.eGfxCbEvent         = MipiDsiCommand;
        stGfxCallbackArgs.stSimDrvDisplayArgs = pInputBuffer;
        bRet                                  = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);
        DD_MEM_COPY_SAFE(pInputBuffer, bufferSize, stGfxCallbackArgs.stSimDrvDisplayArgs, bufferSize);

    } while (FALSE);

    return bRet;
}

BOOLEAN SIMDRVTOGFX_Trigger_Brightness3_Commands(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG bufferSize)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };
    do
    {
        if (pGfxAdapterContext == NULL || pInputBuffer == NULL || pGfxAdapterContext->bIsGfxReady == FALSE ||
            pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler == NULL)
        {
            break;
        }

        stGfxCallbackArgs.eGfxCbEvent         = Brightness3Command;
        stGfxCallbackArgs.stSimDrvDisplayArgs = pInputBuffer;
        bRet                                  = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);
        DD_MEM_COPY_SAFE(pInputBuffer, bufferSize, stGfxCallbackArgs.stSimDrvDisplayArgs, bufferSize);

    } while (FALSE);

    return bRet;
}

BOOLEAN SIMDRVTOGFX_GetDriverWaTable(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PVOID pInputBuffer, ULONG inBufferSize, PVOID pOutputBuffer, ULONG outBufferSize)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };
    do
    {
        if (pGfxAdapterContext == NULL || pInputBuffer == NULL || pOutputBuffer == NULL || pGfxAdapterContext->bIsGfxReady == FALSE ||
            pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler == NULL)
        {
            break;
        }

        stGfxCallbackArgs.eGfxCbEvent         = GetDriverWaTable;
        stGfxCallbackArgs.stSimDrvDisplayArgs = pInputBuffer;
        bRet                                  = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);
        DD_MEM_COPY_SAFE(pInputBuffer, inBufferSize, stGfxCallbackArgs.stSimDrvDisplayArgs, inBufferSize);
        DD_MEM_COPY_SAFE(pOutputBuffer, outBufferSize, ((GFX_DRV_WA_TABLE *)stGfxCallbackArgs.stSimDrvDisplayArgs)->pGfxWaTable, outBufferSize);

    } while (FALSE);
    return bRet;
}

BOOLEAN SIMDRVTOGFX_GetDisplayAdapterCaps(PSIMDRVGFX_CONTEXT pstSimDrvGfxContext, PVOID pOutputBuffer, ULONG outBufferSize)
{
    DISP_ADAPTER_CAPS_DETAILS dispAdapterCapsDetails = { 0 };
    GFX_ADAPTER_CONTEXT       gfxAdapterContext      = { 0 };
    ULONG                     gfxAdapterCount        = 0;

    if (NULL == pstSimDrvGfxContext || NULL == pOutputBuffer || (sizeof(DISP_ADAPTER_CAPS_DETAILS) != outBufferSize))
        return FALSE;

    for (int i = 0; i < MAX_SUPPORTED_ADAPTERS; i++)
    {
        if (pstSimDrvGfxContext->GfxAdapterContext[i].pvGfxHwDev == NULL)
            continue;

        gfxAdapterContext = pstSimDrvGfxContext->GfxAdapterContext[i];
        wcscpy(dispAdapterCapsDetails.displayAdapterCaps[gfxAdapterCount].busDeviceID, gfxAdapterContext.PCIBusDeviceId);

        dispAdapterCapsDetails.displayAdapterCaps[gfxAdapterCount].adapterLuid        = gfxAdapterContext.gfxAdapterLuid;
        dispAdapterCapsDetails.displayAdapterCaps[gfxAdapterCount].adapterGuid        = gfxAdapterContext.gfxAdapterGuid;
        dispAdapterCapsDetails.displayAdapterCaps[gfxAdapterCount].displayLessAdapter = gfxAdapterContext.isDisplayLessAdapter;
        dispAdapterCapsDetails.displayAdapterCaps[gfxAdapterCount].displayOnlyDriver  = gfxAdapterContext.displayOnlyDriver;
        dispAdapterCapsDetails.displayAdapterCaps[gfxAdapterCount].isGfxReady         = gfxAdapterContext.bIsGfxReady;
        dispAdapterCapsDetails.displayAdapterCaps[gfxAdapterCount].devicePowerState   = gfxAdapterContext.devicePowerState;
        dispAdapterCapsDetails.displayAdapterCaps[gfxAdapterCount].powerAction        = gfxAdapterContext.powerAction;

        gfxAdapterCount++;
    }

    dispAdapterCapsDetails.numAdapterCaps = gfxAdapterCount;

    DD_MEM_COPY_SAFE(pOutputBuffer, outBufferSize, &dispAdapterCapsDetails, outBufferSize);

    return TRUE;
}

BOOLEAN SIMDRVTOGFX_GetBuffer(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, GFXCB_EVENT_TYPE eventType, PVOID pInputBuffer, ULONG bufferSize)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };
    do
    {
        if (pGfxAdapterContext == NULL || pInputBuffer == NULL || pGfxAdapterContext->bIsGfxReady == FALSE ||
            pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler == NULL)
        {
            break;
        }

        stGfxCallbackArgs.eGfxCbEvent         = eventType;
        stGfxCallbackArgs.stSimDrvDisplayArgs = pInputBuffer;
        bRet                                  = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);
        DD_MEM_COPY_SAFE(pInputBuffer, bufferSize, stGfxCallbackArgs.stSimDrvDisplayArgs, bufferSize);

    } while (FALSE);
    return bRet;
}

// This will be called via app initiated IOCTL to generate SCDC interrupt
BOOLEAN SIMDRVTOGFX_TriggerScdcInterrupt(PGFX_ADAPTER_CONTEXT pGfxAdapterContext, PSCDC_ARGS pstScdcArgs)
{
    BOOLEAN          bRet              = FALSE;
    GFXCALLBACK_ARGS stGfxCallbackArgs = { 0 };

    GFXVALSIM_FUNC_ENTRY();

    do
    {
        if (pGfxAdapterContext == NULL || pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler == NULL ||
            pGfxAdapterContext->bIsGfxReady == FALSE) // && Port Type Range Check?
        {
            break;
        }

        if (COMMONMMIOHANDLERS_SetupScdcInterrupt(pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface, pstScdcArgs))
        {
            // Missed polling on Master Interrupt Control Enable bit to see if Gfx Interrupts are enabled
            // Generate the interrupt only when DDI is active. TBD
            stGfxCallbackArgs.eGfxCbEvent = GenerateInterrupt;
            bRet                          = pGfxAdapterContext->GfxExposedInterfaces.pfnGfxCb_GenericHandler(pGfxAdapterContext->pvGfxHwDev, &stGfxCallbackArgs);

            if (FALSE == bRet)
            {
                GFXVALSIM_DBG_MSG("GenerateInterrupt callback pfnGfxCb_GenericHandler failed");
            }
        }
        else
        {
            GFXVALSIM_DBG_MSG("COMMONMMIOHANDLERS_SetupScdcInterrupt() failed");
        }

    } while (FALSE);

    GFXVALSIM_FUNC_EXIT(!bRet);

    return bRet;
}
