#include "GfxValSimAccess.h"

extern char *LIBRARY_NAME = "MPO.dll";

GFX_ADAPTER_INFO GFX_0_ADPTER_INFO = { 0 };

BOOL ValSim_DeviceIoControl(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT gfxAdapterInfoSize, VOID *pMpoData, ULONG uldatasize)
{
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    if (hGfxValSimAccess == NULL)
    {
        printf("\nError: Gfx Val Simulation driver not initialized!!!... Exiting...\n");
        return FALSE;
    }
    if (pMpoData == NULL)
    {
        printf("\nError: MPO Data buffer is NULL!!!... Exiting...\n");
        return FALSE;
    }
    if (FALSE == GfxValSimVerifyGfxAdapter(pAdapterInfo))
        return FALSE;

    devIoControlBuffer.pInBuffer    = pMpoData;
    devIoControlBuffer.inBufferSize = uldatasize;
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    dwStatus = DeviceIoControl(hGfxValSimAccess, (DWORD)IOCTL_SIMDRVTOGFX_DISPLAY_DFTHOOKS, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        printf("\nError: IoCTL Call Failed with error code: 0x%u\n", GetLastError());
        return FALSE;
    }
    return TRUE;
}

BOOL GfxValSimVerifyGfxAdapter(PGFX_ADAPTER_INFO pAdapterInfo)
{
    GFX_ADAPTER_DETAILS adapterDetails = { 0 };
    if (NULL == pAdapterInfo)
        return FALSE;
    if (0 != wcscmp(pAdapterInfo->vendorID, INTEL_VENDOR_ID))
        return FALSE;
    if (sizeof(GFX_ADAPTER_INFO) != sizeof(adapterDetails.adapterInfo[0]))
        return FALSE;
    return TRUE;
}
