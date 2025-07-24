#include "GfxValSimAccess.h"
#include "CommonDetails.h"
#include "../Logger/log.h"

BOOL ValSim_DeviceIoControl(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT gfxAdapterInfoSize, DWORD ioctl_code, VOID *pData, ULONG uldatasize)
{
    HANDLE                   hGfxValSimHandle;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };
    hGfxValSimHandle                            = GetGfxValSimHandle();

    NULL_PTR_CHECK(hGfxValSimHandle);
    NULL_PTR_CHECK(pData);
    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    devIoControlBuffer.pInBuffer    = pData;
    devIoControlBuffer.inBufferSize = uldatasize;
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    dwStatus = DeviceIoControl(hGfxValSimHandle, ioctl_code, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        ERROR_LOG("IoCTL Call Failed with error code: 0x%u\n", GetLastError());
        return FALSE;
    }
    return TRUE;
}
