#include "CommonDetails.h"

BOOL GfxValSimGetMIPIDSICaps(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT targetId, VOID *pBufferArgs)
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
        return FALSE;
    }
    /* Check for pBufferArgs is null or not */
    if (pBufferArgs == NULL)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: MIPI DSI caps buffer is NULL!!!... Exiting...\n");
        return FALSE;
    }
    SIMDRV_MIPI_ARGS mipiArgs = { 0 };
    mipiArgs.ulTargetId       = targetId;
    mipiArgs.ulMipiEventType  = SIMDRV_MIPI_DSI_CAPS;
    mipiArgs.pArgs            = (void *)pBufferArgs;

    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);
    devIoControlBuffer.pInBuffer    = &mipiArgs;
    devIoControlBuffer.inBufferSize = sizeof(SIMDRV_MIPI_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_SIMDRVTOGFX_TRIGGER_MIPI_DSI_DCS, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: IoCTL Failed to trigger MIPI DSI Caps with error code: 0x%u\n", GetLastError());
        return FALSE;
    }

    return TRUE;
}

BOOL GfxValSimPerformMIPIDSITransmission(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT targetId, VOID *pBufferArgs)
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
        return FALSE;
    }
    /* Check for pBufferArgs is null or not */
    if (pBufferArgs == NULL)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: MIPI DSI Transmission buffer is NULL!!!... Exiting...\n");
        return FALSE;
    }
    SIMDRV_MIPI_ARGS mipiArgs = { 0 };
    mipiArgs.ulTargetId       = targetId;
    mipiArgs.ulMipiEventType  = SIMDRV_MIPI_DSI_TRANSMISSION;
    mipiArgs.pArgs            = (void *)pBufferArgs;

    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);
    devIoControlBuffer.pInBuffer    = &mipiArgs;
    devIoControlBuffer.inBufferSize = sizeof(SIMDRV_MIPI_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_SIMDRVTOGFX_TRIGGER_MIPI_DSI_DCS, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: IoCTL Failed to trigger MIPI DSI Transmission with error code: 0x%u\n", GetLastError());
        return FALSE;
    }

    return TRUE;
}
