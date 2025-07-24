#include "SimDriver.h"
#include "CommonIOCTL.h"
#include "DPIOCTL.h"
#include "EDPIOCTL.h"
#include "HDMIIOCTL.h"
#include "CommonRxHandlers.h"
#include "DPHandlers.h"
#include "SimDrvToGfx.h"
#include "..\\CommonCore\CommonCore.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"
#include "..\\CommonInclude\\ETWLogging.h"
#include "..\\VBTSimulation\\VBTSimulation.h"

#include "..\\PeristenceServices\\PersistenceHandler.h"

VOID                   SIMDRIVER_Unload(IN PDRIVER_OBJECT DriverObject);
_Use_decl_annotations_ NTSTATUS SIMDRIVER_AddDevice(PDRIVER_OBJECT pDriverObj, PDEVICE_OBJECT pPDO);
NTSTATUS                        SIMDRIVER_CreateFileHandler(IN PDEVICE_OBJECT pDevObj, IN PIRP pIrp);
NTSTATUS                        SIMDRIVER_CloseFileHandler(IN PDEVICE_OBJECT pDevObj, IN PIRP pIrp);
NTSTATUS                        SIMDRIVER_PnPHandler(IN PDEVICE_OBJECT pDevObj, IN PIRP pIrp);
NTSTATUS                        SIMDRIVER_IOCTLHandler(IN PDEVICE_OBJECT pDevObj, IN PIRP pIrp);
NTSTATUS                        SIMDRIVER_ShutDownHandler(IN PDEVICE_OBJECT pDevObj, IN PIRP pIrp);

static PVOID pSimDrvExtension = NULL;

NTSTATUS DriverEntry(IN PDRIVER_OBJECT DriverObject, IN PUNICODE_STRING RegistryPath)
{

    EventRegisterIntel_Gfx_Display_ValSim_Driver();
    NTSTATUS ntStatus = STATUS_SUCCESS;

    // Create dispatch points for the IRPs.
    DriverObject->DriverExtension->AddDevice           = SIMDRIVER_AddDevice;
    DriverObject->MajorFunction[IRP_MJ_CREATE]         = SIMDRIVER_CreateFileHandler;
    DriverObject->MajorFunction[IRP_MJ_CLOSE]          = SIMDRIVER_CloseFileHandler;
    DriverObject->MajorFunction[IRP_MJ_PNP]            = SIMDRIVER_PnPHandler;
    DriverObject->MajorFunction[IRP_MJ_DEVICE_CONTROL] = SIMDRIVER_IOCTLHandler;
    DriverObject->MajorFunction[IRP_MJ_SHUTDOWN]       = SIMDRIVER_ShutDownHandler;
    DriverObject->DriverUnload                         = SIMDRIVER_Unload;

    return ntStatus;
}

NTSTATUS SIMDRIVER_AddDevice(PDRIVER_OBJECT pDriverObj, PDEVICE_OBJECT pPDO)
{
    NTSTATUS           ntStatus        = STATUS_SUCCESS;
    PDEVICE_OBJECT     pstDevObj       = NULL;
    PSIMDEV_EXTENTSION pstSimDrvDevExt = NULL;
    UNICODE_STRING     NtDeviceName;

    do
    {
        RtlInitUnicodeString(&NtDeviceName, SIMDRV_DEVICE_NAME);

        // Create a device object.
        ntStatus = IoCreateDevice(pDriverObj, sizeof(SIMDEV_EXTENTSION), &NtDeviceName, FILE_DEVICE_UNKNOWN, 0, FALSE, &pstDevObj);

        if (!NT_SUCCESS(ntStatus))
        {
            // Either not enough memory to create a deviceobject or another
            // deviceobject with the same name exits. This could happen
            // if you install another instance of this device.
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        pstSimDrvDevExt  = (PSIMDEV_EXTENTSION)pstDevObj->DeviceExtension;
        pSimDrvExtension = (PSIMDEV_EXTENTSION)pstSimDrvDevExt;

        RtlInitUnicodeString(&pstSimDrvDevExt->DosDeviceName, SIMDRVDOS_DEVICE_NAME);

        ntStatus = IoCreateSymbolicLink(&pstSimDrvDevExt->DosDeviceName, &NtDeviceName);

        if (!NT_SUCCESS(ntStatus)) // If we we couldn't create the link then abort installation
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        /* Get OS Info */
        RtlGetVersion((PRTL_OSVERSIONINFOW)&pstSimDrvDevExt->OsInfo);

        pstSimDrvDevExt->pstPhysicalDeviceObject = pPDO;
        pstSimDrvDevExt->pstDeviceObject         = pstDevObj;
        pstSimDrvDevExt->pstDriverObject         = pDriverObj;

        // pstLowerDeviceObject would be pPDO mostly unless the root bus driver has an upper filter
        pstSimDrvDevExt->pstLowerDeviceObject = IoAttachDeviceToDeviceStack(pstDevObj, pPDO);

        pstDevObj->Flags &= ~DO_DEVICE_INITIALIZING;

        // Lets Register Device Interface
        ntStatus = IoRegisterDeviceInterface(pPDO, &SIMDRV_INTERFACE_GUID, NULL, &pstSimDrvDevExt->SymbolicLink);

        if (!NT_SUCCESS(ntStatus))
        {
            break;
        }

        GFXVALSIM_FUNC_ENTRY();
        // Init Porting Layer
        PORTINGLAYER_Init();

        ntStatus = SIMDRVTOGFX_InitSimDrvToGfxInterfaces(&((PSIMDRVGFX_CONTEXT)pstSimDrvDevExt->pvSimDrvToGfxContext));

        if (!NT_SUCCESS(ntStatus))
        {
            GFXVALSIM_DBG_MSG("SIMDRVTOGFX_InitSimDrvToGfxInterfaces Failed !!");
            break;
        }

        ntStatus = IoSetDeviceInterfaceState(&pstSimDrvDevExt->SymbolicLink, TRUE);

        if (!NT_SUCCESS(ntStatus))
        {
            GFXVALSIM_DBG_MSG("SIMDRVTOGFX_InitSimDrvToGfxInterfaces Failed !!");
            break;
        }

        ntStatus = IoRegisterShutdownNotification(pstDevObj);

        if (!NT_SUCCESS(ntStatus))
        {
            GFXVALSIM_DBG_MSG("SIMDRVTOGFX_InitSimDrvToGfxInterfaces Failed !!");
            break;
        }
        McGenEventRegister(&GfxValSimDisplayDriverProvider, GfxMcGenControlCallbackV2, pDriverObj, &Intel_Gfx_ValSimDiverTrackingHandle);
        // Now enable simulation mode since Simulation driver load and KMIF exchange b/w Gfx & Sim drivers are successful
        ntStatus = SIMDRVTOGFX_EnableDisableGfxSimulationMode(TRUE);

    } while (FALSE);

    if (!NT_SUCCESS(ntStatus) && pstDevObj)
    {
        IoDeleteDevice(pstDevObj);
    }

    GFXVALSIM_FUNC_EXIT(ntStatus);
    return ntStatus;
}

NTSTATUS SIMDRIVER_CreateFileHandler(IN PDEVICE_OBJECT pDevObj, IN PIRP pIrp)
{
    NTSTATUS ntStatus = STATUS_SUCCESS;

    return ntStatus;
}

NTSTATUS SIMDRIVER_CloseFileHandler(IN PDEVICE_OBJECT pDevObj, IN PIRP pIrp)
{
    NTSTATUS ntStatus = STATUS_SUCCESS;
    return ntStatus;
}

NTSTATUS SIMDRIVER_IOCTLHandler(IN PDEVICE_OBJECT pDevObj, IN PIRP pIrp)
{
    PIO_STACK_LOCATION        pIrpStack            = NULL;
    NTSTATUS                  ntStatus             = STATUS_SUCCESS;
    ULONG                     ulRetInfo            = 0;
    ULONG                     ulDataLen            = 0;
    PPORT_HPD_ARGS            pstPortHPDArgs       = NULL;
    PGET_DPCD_ARGS            pstGetDPCDArgs       = NULL;
    PSIMDRV_MMIO_ACCESS_ARGS  psimDrvMmioAccess    = NULL;
    PSIMDRVGFX_CONTEXT        pstSimDrvGfxContext  = NULL;
    PGFX_ADAPTER_CONTEXT      pGfxAdapterContext   = NULL;
    PDEVICE_IO_CONTROL_BUFFER pDeviceControlBuffer = NULL;
    PDPCD_ARGS                pstDpcdArgs          = NULL;
    PPORT_INFO                pstPortInfo          = NULL;

    ULONG ulPortNum = PORT_NONE;

    GFXVALSIM_FUNC_ENTRY();

    PSIMDEV_EXTENTSION pstSimDrvDevExt = (PSIMDEV_EXTENTSION)pDevObj->DeviceExtension;
    if (NULL == pstSimDrvDevExt)
    {
        GFXVALSIM_DBG_MSG("SIMDEV_EXTENTSION is NULL");
        ntStatus = STATUS_UNSUCCESSFUL;
        goto end;
    }

    pstSimDrvGfxContext = (PSIMDRVGFX_CONTEXT)pstSimDrvDevExt->pvSimDrvToGfxContext;
    if (NULL == pstSimDrvGfxContext)
    {
        GFXVALSIM_DBG_MSG("SimDrvToGfxContext is NULL");
        ntStatus = STATUS_UNSUCCESSFUL;
        goto end;
    }

    pDeviceControlBuffer = (PDEVICE_IO_CONTROL_BUFFER)pIrp->AssociatedIrp.SystemBuffer;

    if (pDeviceControlBuffer == NULL)
    {
        GFXVALSIM_DBG_MSG("DEVICE_IO_CONTROL_BUFFER is NULL");
        ntStatus = STATUS_UNSUCCESSFUL;
        goto end;
    }

    pIrpStack = IoGetCurrentIrpStackLocation(pIrp);

    if (pIrpStack == NULL)
    {
        ntStatus = STATUS_UNSUCCESSFUL;
        goto end;
    }

    ulDataLen                  = pIrpStack->Parameters.DeviceIoControl.InputBufferLength;
    pIrp->IoStatus.Information = ulRetInfo;

    if (pIrp->AssociatedIrp.SystemBuffer == NULL)
    {
        ntStatus = STATUS_UNSUCCESSFUL;
        goto end;
    }

    if (pIrpStack->Parameters.DeviceIoControl.IoControlCode == IOCTL_GET_DISP_ADAPTER_CAPS)
    {
        if (FALSE == SIMDRVTOGFX_GetDisplayAdapterCaps(pstSimDrvGfxContext, pDeviceControlBuffer->pInBuffer, pDeviceControlBuffer->inBufferSize))
        {
            GFXVALSIM_DBG_MSG("SIMDRVTOGFX_GetDisplayAdapterCaps: Failed!");
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }
        goto end;
    }

    pGfxAdapterContext =
    pstSimDrvGfxContext->pfnGetAdapterContext(pstSimDrvGfxContext, pDeviceControlBuffer->pAdapterInfo->busDeviceID, pDeviceControlBuffer->pAdapterInfo->deviceInstanceID);

    if (pGfxAdapterContext == NULL)
    {
        GFXVALSIM_DBG_MSG("GfxAdapterContext is NULL");
        ntStatus = STATUS_UNSUCCESSFUL;
        goto end;
    }
    if (pGfxAdapterContext->bIsGfxReady == FALSE)
    {
        GFXVALSIM_DBG_MSG("Gfx Driver is not running");
        ntStatus = STATUS_UNSUCCESSFUL;
        goto end;
    }
    if (TRUE == pGfxAdapterContext->isDisplayLessAdapter)
    {
        GFXVALSIM_DBG_MSG("Input adapter is display less adapter, Exiting !!!");
        ntStatus = STATUS_GRAPHICS_INVALID_DISPLAY_ADAPTER;
        goto end;
    }

    switch (pIrpStack->Parameters.DeviceIoControl.IoControlCode)
    {
    case IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS:

        if (FALSE == SIMDRVTOGFX_Display_Hooks(pGfxAdapterContext, pDeviceControlBuffer->pInBuffer, pDeviceControlBuffer->inBufferSize))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        goto end;

    case IOCTL_SIMDRVTOGFX_TRIGGER_DSB:

        if (FALSE == SIMDRVTOGFX_Trigger_Dsb(pGfxAdapterContext, pDeviceControlBuffer->pInBuffer, pDeviceControlBuffer->inBufferSize))
        {
            GFXVALSIM_DBG_MSG("IOCTL_SIMDRVTOGFX_TRIGGER_DSB: Failed");
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }
        goto end;

    case IOCTL_SIMDRVTOGFX_MMIO_ACCESS:

        psimDrvMmioAccess   = (PSIMDRV_MMIO_ACCESS_ARGS)((PDEVICE_IO_CONTROL_BUFFER)pIrp->AssociatedIrp.SystemBuffer)->pInBuffer;
        BOOLEAN bMmioStatus = FALSE;
        bool    bStateModified;
        if (psimDrvMmioAccess->accessType == SIMDRV_GFX_ACCESS_REQUEST_READ)
        {
            bMmioStatus = SIMDRVTOGFX_GfxReadMMIOHandler(pGfxAdapterContext, psimDrvMmioAccess->offset, psimDrvMmioAccess->pValue, &bStateModified);
        }
        else if (psimDrvMmioAccess->accessType == SIMDRV_GFX_ACCESS_REQUEST_WRITE)
        {
            bMmioStatus = SIMDRVTOGFX_GfxWriteMMIOHandler(pGfxAdapterContext, psimDrvMmioAccess->offset, *psimDrvMmioAccess->pValue, &bStateModified);
        }

        if (FALSE == bMmioStatus)
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = pDeviceControlBuffer->inBufferSize;
        }
        goto end;

    case IOCTL_SIMDRVTOGFX_WAKE_LOCK_ACCESS:
        GFXVALSIM_DBG_MSG("Calling SIMDRVTOGFX_WAKE_LOCK_Access!");
        if (FALSE == SIMDRVTOGFX_WAKE_LOCK_Access(pGfxAdapterContext, pDeviceControlBuffer->pInBuffer, pDeviceControlBuffer->inBufferSize))
        {
            GFXVALSIM_DBG_MSG("SIMDRVTOGFX_WAKE_LOCK_Access: Failed");
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }
        goto end;

    case IOCTL_SIMDRVTOGFX_TRIGGER_MIPI_DSI_DCS:

        if (FALSE == SIMDRVTOGFX_Trigger_MIPI_DSI_Commands(pGfxAdapterContext, pDeviceControlBuffer->pInBuffer, pDeviceControlBuffer->inBufferSize))
        {
            GFXVALSIM_DBG_MSG("IOCTL_SIMDRVTOGFX_TRIGGER_MIPI_DSI: Failed");
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }
        goto end;

    case IOCTL_SIMDRVTOGFX_TRIGGER_BRIGHTNESS3:

        if (FALSE == SIMDRVTOGFX_Trigger_Brightness3_Commands(pGfxAdapterContext, pDeviceControlBuffer->pInBuffer, pDeviceControlBuffer->inBufferSize))
        {
            GFXVALSIM_DBG_MSG("IOCTL_SIMDRVTOGFX_TRIGGER_BRIGHTNESS3: Failed");
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }
        goto end;

    case IOCTL_SIMDRVTOGFX_PLATFORM_DETAILS:

        if (NULL == pDeviceControlBuffer->pInBuffer)
        {
            GFXVALSIM_DBG_MSG("IOCTL_SIMDRVTOGFX_PLATFORM_DETAILS: Failed");
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            PVALSIM_PLATFORM_INFO pPlatformInfo = (PVALSIM_PLATFORM_INFO)((PDEVICE_IO_CONTROL_BUFFER)pIrp->AssociatedIrp.SystemBuffer)->pInBuffer;
            pPlatformInfo->GfxPlatform          = pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface->eIGFXPlatform;
            pPlatformInfo->GfxPchFamily         = pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface->ePCHProductFamily;
            pPlatformInfo->GfxGmdId             = pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface->stGfxGmdId.Value;

            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }
        goto end;

    case IOCTL_GET_DRIVER_WA_TABLE:
        if (FALSE == SIMDRVTOGFX_GetDriverWaTable(pGfxAdapterContext, pDeviceControlBuffer->pInBuffer, pDeviceControlBuffer->inBufferSize, pDeviceControlBuffer->pOutBuffer,
                                                  pDeviceControlBuffer->outBufferSize))
        {
            GFXVALSIM_DBG_MSG("IOCTL_GET_DRIVER_WA_TABLE: Failed");
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }
        goto end;

    case IOCTL_GET_DISP_DIAG_DATA:
        if (FALSE == SIMDRVTOGFX_GetBuffer(pGfxAdapterContext, GetDiagnosticsData, pDeviceControlBuffer->pInBuffer, pDeviceControlBuffer->inBufferSize))
        {
            GFXVALSIM_DBG_MSG("SIMDRVTOGFX_GetBuffer: Failed");
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }
        goto end;

    default:
        break;
    }

    if (((PSIMDRVGFX_CONTEXT)pstSimDrvDevExt->pvSimDrvToGfxContext)->featureControl.DisableSinkSimulation == TRUE)
    {
        GFXVALSIM_DBG_MSG("SIMDRIVER_IOCTLHandler: Sink simulation not enabled.");
        ntStatus = STATUS_UNSUCCESSFUL;
        goto end;
    }

    switch (pIrpStack->Parameters.DeviceIoControl.IoControlCode)
    {
        // Init should be called only once after SIM driver load

    case IOCTL_INIT_PORT_INFO:
        if (FALSE == COMMONRXHANDLERS_SetRxInfo((PPORT_INFO)pDeviceControlBuffer->pInBuffer, pGfxAdapterContext->pstRxInfoArr))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        if (FALSE == PERSISTENCEHANDLER_SetRxInfo((PPORT_INFO)pDeviceControlBuffer->pInBuffer, pGfxAdapterContext->pvSimPersistenceData))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }

        pstPortInfo = (PPORT_INFO)pDeviceControlBuffer->pInBuffer;
        if (FALSE == COMMONMMIOHANDLERS_SetEdpTypeCMappingInfo(pGfxAdapterContext->pstRxInfoArr->pstMMIOInterface, pstPortInfo->ulPortNum))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }

        break;

    case IOCTL_GENERATE_HPD:
        pstPortHPDArgs = (PPORT_HPD_ARGS)pDeviceControlBuffer->pInBuffer;
        GFXVALSIM_HPD_MSG(pstPortHPDArgs->ulPortNum, pstPortHPDArgs->bAttachorDettach, 0x2, pstPortHPDArgs->uPortConnectorInfo.Value);
        if (FALSE == COMMRXHANDLERS_SetPortPluggedState(pGfxAdapterContext->pstRxInfoArr, pstPortHPDArgs->ulPortNum,
                                                        (pstPortHPDArgs->bAttachorDettach == TRUE ? eSinkPlugged : eSinkUnplugged), pstPortHPDArgs->uPortConnectorInfo))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        if (pstSimDrvGfxContext->featureControl.HybridSimulation == FALSE)
        {
            if (FALSE == SIMDRVTOGFX_GenerateHPDorSPI(pGfxAdapterContext, pstPortHPDArgs->ulPortNum, TRUE, pstPortHPDArgs->bAttachorDettach, pstPortHPDArgs->uPortConnectorInfo))
            {
                GFXVALSIM_DBG_MSG("SIMDRVTOGFX_GenerateHPDorSPI() failed");

                // Since the HPD call failed to Undo the above Port Plugged State
                COMMRXHANDLERS_SetPortPluggedState(pGfxAdapterContext->pstRxInfoArr, pstPortHPDArgs->ulPortNum,
                                                   (pstPortHPDArgs->bAttachorDettach == TRUE ? eSinkUnplugged : eSinkPlugged), pstPortHPDArgs->uPortConnectorInfo);
                ntStatus = STATUS_UNSUCCESSFUL;
                break;
            }
        }

        if (FALSE == PERSISTENCEHANDLER_UpdatePortPluggedState(pGfxAdapterContext->pvSimPersistenceData, pstPortHPDArgs->ulPortNum,
                                                               (pstPortHPDArgs->bAttachorDettach == TRUE ? eSinkPlugged : eSinkUnplugged), pstPortHPDArgs->uPortConnectorInfo))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }

        break;

    case IOCTL_TRIGGER_SPI:
        pstPortHPDArgs = (PPORT_HPD_ARGS)pDeviceControlBuffer->pInBuffer;
        GFXVALSIM_HPD_MSG(pstPortHPDArgs->ulPortNum, pstPortHPDArgs->bAttachorDettach, 0x1, pstPortHPDArgs->uPortConnectorInfo.Value);
        if (FALSE == SIMDRVTOGFX_GenerateHPDorSPI(pGfxAdapterContext, pstPortHPDArgs->ulPortNum, FALSE, TRUE, pstPortHPDArgs->uPortConnectorInfo))
        {
            GFXVALSIM_DBG_MSG("SPI Generation Failed.");

            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_TRIGGER_HPD:
        pstPortHPDArgs = (PPORT_HPD_ARGS)pDeviceControlBuffer->pInBuffer;
        GFXVALSIM_HPD_MSG(pstPortHPDArgs->ulPortNum, pstPortHPDArgs->bAttachorDettach, 0x1, pstPortHPDArgs->uPortConnectorInfo.Value);
        if (FALSE == SIMDRVTOGFX_GenerateHPDorSPI(pGfxAdapterContext, pstPortHPDArgs->ulPortNum, TRUE, pstPortHPDArgs->bAttachorDettach, pstPortHPDArgs->uPortConnectorInfo))
        {
            GFXVALSIM_DBG_MSG("TRIGGER HPD Failed.");

            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_GENERATE_MIPI_DSI_TE:
        pstPortHPDArgs = (PPORT_HPD_ARGS)pDeviceControlBuffer->pInBuffer;

        if (FALSE == SIMDRVTOGFX_GenerateTE(pGfxAdapterContext, pstPortHPDArgs->ulPortNum))
        {
            GFXVALSIM_DBG_MSG("SIMDRVTOGFX_GenerateTE() failed");

            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }
        break;

    case IOCTL_INIT_DP_TOPOLOGY:
        if (FALSE == DPHANDLERS_InitDPTopologyType(pGfxAdapterContext->pstRxInfoArr, (PDP_INIT_INFO)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        if (FALSE == PERSISTENCEHANDLER_InitDPTopologyType(pGfxAdapterContext->pvSimPersistenceData, (PDP_INIT_INFO)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_SET_EDID_DATA:
        if (FALSE == COMMRXHANDLERS_SetEDIDData(pGfxAdapterContext->pstRxInfoArr, (PFILE_DATA)pDeviceControlBuffer->pInBuffer, FALSE))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        if (FALSE == PERSISTENCEHANDLER_SetEDIDData(pGfxAdapterContext->pvSimPersistenceData, (PFILE_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_SET_DPCD_DATA:
        if (FALSE == DPHANDLERS_SetDPCDData(pGfxAdapterContext->pstRxInfoArr, (PFILE_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        if (FALSE == PERSISTENCEHANDLER_SetDPCDData(pGfxAdapterContext->pvSimPersistenceData, (PFILE_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_SET_DONGLE_TYPE:
        if (FALSE == COMMRXHANDLERS_SetDongleType(pGfxAdapterContext->pstRxInfoArr, ((PDONGLE_TYPE_INFO)pDeviceControlBuffer->pInBuffer)->uiPortNum,
                                                  ((PDONGLE_TYPE_INFO)pDeviceControlBuffer->pInBuffer)->uiDongleType))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        if (FALSE == PERSISTENCEHANDLER_SetDongleType(pGfxAdapterContext->pvSimPersistenceData, ((PDONGLE_TYPE_INFO)pDeviceControlBuffer->pInBuffer)->uiPortNum,
                                                      ((PDONGLE_TYPE_INFO)pDeviceControlBuffer->pInBuffer)->uiDongleType))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_SET_BRANCHDISP_DATA:
        if (FALSE == DPHANDLERS_SetDPMSTTopology(pGfxAdapterContext->pstRxInfoArr, (PBRANCHDISP_DATA_ARRAY)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }
        else
        {
            if (FALSE == PERSISTENCEHANDLER_SetDPMSTTopology(pGfxAdapterContext->pvSimPersistenceData, (PBRANCHDISP_DATA_ARRAY)pDeviceControlBuffer->pInBuffer))
            {
                ntStatus = STATUS_UNSUCCESSFUL;
                break;
            }
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
            break;
        }

    case IOCTL_GET_MST_RAD:
        ulPortNum = *((PULONG)pDeviceControlBuffer->pInBuffer);
        // Same buffer pIrp->AssociatedIrp.SystemBuffer is being used as buffer to contain the OUT RAD Data.
        if (FALSE == DPHANDLERS_GetMSTTopologyRADArray(pGfxAdapterContext->pstRxInfoArr, ulPortNum, (PBRANCHDISP_RAD_ARRAY)pDeviceControlBuffer->pOutBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }
        break;

    case IOCTL_READ_DPCD:
        pstGetDPCDArgs = (PGET_DPCD_ARGS)pDeviceControlBuffer->pInBuffer;
        // Same buffer pIrp->AssociatedIrp.SystemBuffer is being used for output too. Be cautious that pIrp->AssociatedIrp.SystemBuffer
        // doesn't get overwritten before pstGetDPCDArgs parameters have been used.
        if (FALSE == DPHANDLERS_ReadDPCD(pGfxAdapterContext->pstRxInfoArr, pstGetDPCDArgs, pDeviceControlBuffer->pOutBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }

        break;

    case IOCTL_WRITE_DPCD:
        if (FALSE == DPHANDLERS_WriteDPCD(pGfxAdapterContext->pstRxInfoArr, (PSET_DPCD_ARGS)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_GENERATE_CSN:
        if (FALSE == DPHANDLERS_ExecuteConnectionStatusNotify(pGfxAdapterContext->pstRxInfoArr, pGfxAdapterContext, (PDP_SUBTOPOLOGY_ARGS)pDeviceControlBuffer->pInBuffer))
        {
            GFXVALSIM_DBG_MSG("DPHANDLERS_ExecuteConnectionStatusNotify Error");
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        if (FALSE == PERSISTENCEHANDLER_UpdateMSTTopologyToPersist(pGfxAdapterContext->pvSimPersistenceData, pGfxAdapterContext->pstRxInfoArr,
                                                                   (PDP_SUBTOPOLOGY_ARGS)pDeviceControlBuffer->pInBuffer))
        {
            GFXVALSIM_DBG_MSG("PERSISTENCEHANDLER_UpdateMSTTopologyToPersist Error");
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

        // NEXT 4 IOCTL are related plug and unplug of sinks during S3/S4 Cycles

    case IOCTL_GFXS3S4_PLUGUNPLUG_DATA:
        if (FALSE == COMMRXHANDLERS_ConfigureAllPortsGfxS3S4PlugUnplugData(pGfxAdapterContext->pstRxInfoArr, (PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        if (FALSE == PERSISTENCEHANDLER_ConfigurePeristenceForS3S4Path(pGfxAdapterContext->pvSimPersistenceDataS3S4, pGfxAdapterContext->pstRxInfoArr,
                                                                       (PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_SET_GFXS3S4_EDID_DATA:
        if (FALSE == COMMRXHANDLERS_SetEDIDData(pGfxAdapterContext->pstRxInfoArr, (PFILE_DATA)pDeviceControlBuffer->pInBuffer, TRUE))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }
        if (FALSE == PERSISTENCEHANDLER_SetEDIDData(pGfxAdapterContext->pvSimPersistenceDataS3S4, (PFILE_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_SET_GFXS3S4_DPCD_DATA:
        if (FALSE == DPHANDLERS_SetDPCDDataForS3S4Cycle(pGfxAdapterContext->pstRxInfoArr, (PFILE_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }

        if (FALSE == PERSISTENCEHANDLER_SetDPCDData(pGfxAdapterContext->pvSimPersistenceData, (PFILE_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_SET_GFXS3S4_BRANCHDISP_DATA:
        if (FALSE == DPHANDLERS_SetDPMSTTopologyForS3S4Cycle(pGfxAdapterContext->pstRxInfoArr, (PBRANCHDISP_DATA_ARRAY)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_GFXS3S4_ADDREMOVESUBTOPOLOGY:
        if (FALSE == DPHANDLERS_AddOrRemoveSubtopologyForS3S4Cycle(pGfxAdapterContext->pstRxInfoArr, (PDP_SUBTOPOLOGY_ARGS)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_SET_DPCD_MODEL_DATA:
        if (FALSE == DPHANDLERS_SetDPCDModelData(pGfxAdapterContext->pstRxInfoArr, (PDP_DPCD_MODEL_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }
        if (FALSE == PERSISTENCEHANDLER_SetDPCDModelData(pGfxAdapterContext->pvSimPersistenceData, (PDP_DPCD_MODEL_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_SET_GFXS3S4_DPCD_MODEL_DATA:
        if (FALSE == DPHANDLERS_SetDPCDModelDataForS3S4Cycle(pGfxAdapterContext->pstRxInfoArr, (PDP_DPCD_MODEL_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
            break;
        }
        if (FALSE == PERSISTENCEHANDLER_SetDPCDModelData(pGfxAdapterContext->pvSimPersistenceData, (PDP_DPCD_MODEL_DATA)pDeviceControlBuffer->pInBuffer))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;
    case IOCTL_TRIGGER_DPCD_WRITE:
        pstDpcdArgs = (PDPCD_ARGS)pDeviceControlBuffer->pInBuffer;
        if (FALSE == COMMRXHANDLERS_SetPanelDpcd(pGfxAdapterContext->pstRxInfoArr, pstDpcdArgs->ulPortNum, pstDpcdArgs->uOffset, pstDpcdArgs->uValue))
        {
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        break;

    case IOCTL_TRIGGER_SCDC_INTERRUPT:
        if (FALSE == SIMDRVTOGFX_TriggerScdcInterrupt(pGfxAdapterContext, (PSCDC_ARGS)pDeviceControlBuffer->pInBuffer))
        {
            GFXVALSIM_DBG_MSG("SIMDRVTOGFX_TriggerScdcInterrupt: Failed");
            ntStatus = STATUS_UNSUCCESSFUL;
        }
        else
        {
            pIrp->IoStatus.Information = sizeof(DEVICE_IO_CONTROL_BUFFER);
        }
        break;

    default:
        ntStatus = STATUS_NOT_IMPLEMENTED;
        break;
    }

end:
    // We're done with I/O request.  Record the status of the I/O action.
    pIrp->IoStatus.Status = ntStatus;

    // Don't boost priority when returning since this took little time.
    IoCompleteRequest(pIrp, IO_NO_INCREMENT);
    GFXVALSIM_FUNC_EXIT(ntStatus);
    return ntStatus;
}

NTSTATUS SIMDRIVER_PnPHandler(IN PDEVICE_OBJECT pDevObj, IN PIRP pIrp)
{
    NTSTATUS           ntStatus        = STATUS_UNSUCCESSFUL;
    ULONG              edpSimulation   = FALSE;
    PPORTINGLAYER_OBJ  pstPortingObj   = GetPortingObj();
    PSIMDEV_EXTENTSION pstSimDrvDevExt = (PSIMDEV_EXTENTSION)pDevObj->DeviceExtension;
    UCHAR              ucMinorFunction = IoGetCurrentIrpStackLocation(pIrp)->MinorFunction;

    IoSkipCurrentIrpStackLocation(pIrp);

    ntStatus = IoCallDriver(pstSimDrvDevExt->pstLowerDeviceObject, pIrp);

    if (ucMinorFunction == IRP_MN_REMOVE_DEVICE)
    {
        SIMDRVTOGFX_EnableDisableGfxSimulationMode(FALSE);
        SIMDRVTOGFX_RegDeRegCallBack(pstSimDrvDevExt->pvSimDrvToGfxContext, FALSE);

        // Cleanup SimDrv to Gfx Interfaces first
        SIMDRVTOGFX_CleanUp(pstSimDrvDevExt->pvSimDrvToGfxContext);
        pstPortingObj->pfnFreeMem(pstSimDrvDevExt->pvSimDrvToGfxContext);
        pstSimDrvDevExt->pvSimDrvToGfxContext = NULL;

        // Driver specific De-Init
        IoDeleteSymbolicLink(&pstSimDrvDevExt->DosDeviceName);
        IoSetDeviceInterfaceState(&pstSimDrvDevExt->SymbolicLink, FALSE);
        RtlFreeUnicodeString(&pstSimDrvDevExt->SymbolicLink);
        IoDetachDevice(pstSimDrvDevExt->pstLowerDeviceObject);
        IoDeleteDevice(pDevObj);
        McGenEventUnregister(&Intel_Gfx_ValSimDiverTrackingHandle);
    }

    return ntStatus;
}

NTSTATUS SIMDRIVER_ShutDownHandler(IN PDEVICE_OBJECT pDevObj, IN PIRP pIrp)
{
    PPORTINGLAYER_OBJ   pstPortingObj       = GetPortingObj();
    GFX_ADAPTER_CONTEXT gfxAdapterContext   = { 0 };
    PSIMDRVGFX_CONTEXT  pstSimDrvGfxContext = NULL;
    PSIMDEV_EXTENTSION  pstSimDrvDevExt     = (PSIMDEV_EXTENTSION)pDevObj->DeviceExtension;
    if (NULL == pstSimDrvDevExt)
        return STATUS_UNSUCCESSFUL;

    pstSimDrvGfxContext = pstSimDrvDevExt->pvSimDrvToGfxContext;
    if (NULL == pstSimDrvGfxContext)
        return STATUS_UNSUCCESSFUL;

    for (INT adapterIndex = 0; adapterIndex < pstSimDrvGfxContext->gfxAdapterCount; adapterIndex++)
    {
        gfxAdapterContext = pstSimDrvGfxContext->GfxAdapterContext[adapterIndex];
        // Delete default VBT regkey upon shutdown
        if (FALSE == VBTSimulation_DeleteDefaultVBT(gfxAdapterContext))
        {
            GFXVALSIM_DBG_MSG("FAIL: Deleting Default VBT on Shutdown failed");
            // ASSERT
        }
        else
        {
            GFXVALSIM_DBG_MSG("PASS: Deleting Default VBT on Shutdown");
        }
        if (FALSE == PERSISTENCEHANDLER_WritePeristenceDataToDisk(gfxAdapterContext.pvSimPersistenceData))
        {
            // ASSERT
        }
        if (NULL != pstPortingObj)
        {
            pstPortingObj->pfnFileClose(&((PSIMDRV_PERSISTENCE_DATA)gfxAdapterContext.pvSimPersistenceData)->stPersistenceFileHandle);
        }
    }

    IoSkipCurrentIrpStackLocation(pIrp);

    return IoCallDriver(pstSimDrvDevExt->pstLowerDeviceObject, pIrp);
}

VOID SIMDRIVER_Unload(IN PDRIVER_OBJECT DriverObject)
{
    EventUnregisterIntel_Gfx_Display_ValSim_Driver();
    return;
}

PSIMDEV_EXTENTSION GetSimDrvExtension()
{
    return (PSIMDEV_EXTENTSION)pSimDrvExtension;
}
