#include "CommonDetails.h"


BOOL GfxValSimGetDisplayNonIntrusiveData(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, PDISPLAYSTATE_NONINTRUSIVE pNonIntrusiveData)
{
    HANDLE                   hGfxValSimHandle;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };
    DXGKARG_GETDISPLAYSTATENONINTRUSIVE displayStateNonIntrusive = { 0 };
    SIMDRV_DISPLAY_DIAG_DATA            simDrvDispDiagData       = { 0 };
    DXGK_DISPLAYSTATE_NONINTRUSIVE *ptrNonIntrusive[MAX_DISPLAY_FOR_DIAGNOSTICS] = { 0 };

    hGfxValSimHandle = GetGfxValSimHandle();
    /* Check for GfxValSimDriver handler */
    if (hGfxValSimHandle == NULL)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: Gfx Val Simulation driver not initialized!!!... Exiting...\n");
        return FALSE;
    }
    /* Check for buffer is null or not */
    if (pNonIntrusiveData == NULL)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: Buffer is NULL!!!... Exiting...\n");
        return FALSE;
    }
    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    displayStateNonIntrusive.NumOfTargets = pNonIntrusiveData->NumOfTargets;
    for (UINT noOfTarget = 0; noOfTarget < pNonIntrusiveData->NumOfTargets; noOfTarget++)
    {
        ptrNonIntrusive[noOfTarget] = &pNonIntrusiveData->NonIntrusiveData[noOfTarget];
    }

    simDrvDispDiagData.type = NONINTRUSIVE;
    displayStateNonIntrusive.ppDisplayStateNonIntrusive = ptrNonIntrusive;
    memcpy_s(&simDrvDispDiagData.nonIntrusiveData, sizeof(DXGKARG_GETDISPLAYSTATENONINTRUSIVE), &displayStateNonIntrusive, sizeof(DXGKARG_GETDISPLAYSTATENONINTRUSIVE));

    devIoControlBuffer.pInBuffer    = &simDrvDispDiagData;
    devIoControlBuffer.inBufferSize = sizeof(SIMDRV_DISPLAY_DIAG_DATA);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_GET_DISP_DIAG_DATA, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: IoCTL Failed for ValsimIoctlCall with error code: 0x%u\n", GetLastError());
        return FALSE;
    }
    return (simDrvDispDiagData.sizeofData == sizeof(DXGKARG_GETDISPLAYSTATENONINTRUSIVE));
}

BOOL GfxValSimGetDisplayIntrusiveData(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, PDISPLAYSTATE_INTRUSIVE pIntrusiveData)
{
    HANDLE                              hGfxValSimHandle;
    DWORD                               dwStatus                 = 0;
    DWORD                               BytesReturned            = 0;
    DEVICE_IO_CONTROL_BUFFER            devIoControlBuffer       = { 0 };
    DXGKARG_GETDISPLAYSTATEINTRUSIVE    displayStateIntrusive    = { 0 };
    SIMDRV_DISPLAY_DIAG_DATA            simDrvDispDiagData       = { 0 };
    DXGK_DISPLAYSTATE_INTRUSIVE         *ptrIntrusive[MAX_DISPLAY_FOR_DIAGNOSTICS] = { 0 };

    hGfxValSimHandle = GetGfxValSimHandle();
    /* Check for GfxValSimDriver handler */
    if (hGfxValSimHandle == NULL)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: Gfx Val Simulation driver not initialized!!!... Exiting...\n");
        return FALSE;
    }
    /* Check for buffer is null or not */
    if (pIntrusiveData == NULL)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: Buffer is NULL!!!... Exiting...\n");
        return FALSE;
    }
    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    displayStateIntrusive.NumOfTargets = pIntrusiveData->NumOfTargets;
    for (UINT noOfTarget = 0; noOfTarget < pIntrusiveData->NumOfTargets; noOfTarget++)
    {
        ptrIntrusive[noOfTarget] = &pIntrusiveData->IntrusiveData[noOfTarget];
    }

    simDrvDispDiagData.type                       = INTRUSIVE;
    displayStateIntrusive.ppDisplayStateIntrusive = ptrIntrusive;
    memcpy_s(&simDrvDispDiagData.intrusiveData, sizeof(DXGKARG_GETDISPLAYSTATEINTRUSIVE), &displayStateIntrusive, sizeof(DXGKARG_GETDISPLAYSTATEINTRUSIVE));

    devIoControlBuffer.pInBuffer    = &simDrvDispDiagData;
    devIoControlBuffer.inBufferSize = sizeof(SIMDRV_DISPLAY_DIAG_DATA);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_GET_DISP_DIAG_DATA, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        TRACE_LOG(DEBUG_LOGS, "\nError: IoCTL Failed for ValsimIoctlCall with error code: 0x%u\n", GetLastError());
        return FALSE;
    }
    return (simDrvDispDiagData.sizeofData == sizeof(DXGKARG_GETDISPLAYSTATEINTRUSIVE));
}