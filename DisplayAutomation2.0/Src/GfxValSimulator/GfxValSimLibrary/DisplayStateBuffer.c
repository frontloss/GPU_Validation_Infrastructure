#include "CommonDetails.h"

ULONG GfxValSimTriggerDSB(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, SIMDRV_DSB_BUFFER_ARGS *pDsbBufferArgs)
{
    HANDLE                   hGfxValSimHandle;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    hGfxValSimHandle = GetGfxValSimHandle();
    /* Check for GfxValSimDriver handler */
    if (hGfxValSimHandle == NULL)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: Gfx Val Simulation driver not initialized!!!... Exiting...\n");
        return SIMDRV_DSB_VALSIM_INIT_FAILED;
    }
    /* Check for pDsbBufferArgs is null or not */
    if (pDsbBufferArgs == NULL)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: DSB buffer is NULL!!!... Exiting...\n");
        return SIMDRV_DSB_INVALID_MEMORY_ACCESS;
    }

    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);
    devIoControlBuffer.pInBuffer    = pDsbBufferArgs;
    devIoControlBuffer.inBufferSize = sizeof(SIMDRV_DSB_BUFFER_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    /* Send DeviceIoCtl for port objects. DP GfxValSim driver doesn't expect/return any argument */
    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_SIMDRVTOGFX_TRIGGER_DSB, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: IoCTL Failed for trigger DSB with error code: 0x%u\n", GetLastError());
        return SIMDRV_DSB_VALSIM_IOCTL_FAILED;
    }

    /* If DeviceIoCtl Status is success check DSB trigger status */
    ULONG Status = SIMDRV_DSB_SUCCESS;
    for (ULONG pipeIndex = 0; pipeIndex < pDsbBufferArgs->NumDisplayPipe; pipeIndex++)
    {
        Status |= pDsbBufferArgs->DsbBufferPipeArgs[pipeIndex].Status;
    }
    if (Status != SIMDRV_DSB_SUCCESS)
        return SIMDRV_DSB_FAILED;
    return SIMDRV_DSB_SUCCESS;
}