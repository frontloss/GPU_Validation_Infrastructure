#include "CommonDetails.h"

BOOL GfxValSimSetBrightness3(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT targetId, VOID *pBufferArgs)
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
        TRACE_LOG(DEBUG_LOGS, "\nError: SetBrightness3 buffer is NULL!!!... Exiting...\n");
        return FALSE;
    }
    SIMDRV_BRIGHTNESS3_ARGS brightness3Args = { 0 };
    brightness3Args.ulTargetId       = targetId;
    brightness3Args.ulBrightness3EventType  = SIMDRV_BRIGHTNESS3_SET;
    brightness3Args.pArgs            = (void *)pBufferArgs;

    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);
    devIoControlBuffer.pInBuffer    = &brightness3Args;
    devIoControlBuffer.inBufferSize = sizeof(SIMDRV_BRIGHTNESS3_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_SIMDRVTOGFX_TRIGGER_BRIGHTNESS3, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: IoCTL Failed to trigger SetBrightness3 with error code: 0x%u\n", GetLastError());
        return FALSE;
    }

    return TRUE;
}
