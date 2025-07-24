/**
 * @file
 * @section GfxValSim_c
 * @brief Internal source file which contains implementation required for getting information related to
 * machine, operating system, driver, register read, diva status, generic escape etc..,
 *
 * @ref GfxValSim.c
 * @author Reeju Srivastava, Aafiya Kaleem
 */

/***********************************************************************************************
 * INTEL CONFIDENTIAL. Copyright (c) 2016 Intel Corporation All Rights Reserved.
 *  <br>The source code contained or described herein and all documents related to the source code
 *  ("Material") are owned by Intel Corporation or its suppliers or licensors. Title to the
 *  Material remains with Intel Corporation or its suppliers and licensors. The Material contains
 *  trade secrets and proprietary and confidential information of Intel or its suppliers and licensors.
 *  The Material is protected by worldwide copyright and trade secret laws and treaty provisions.
 *  No part of the Material may be used, copied, reproduced, modified, published, uploaded, posted,
 *  transmitted, distributed, or disclosed in any way without Intel’s prior express written permission.
 *  <br>No license under any patent, copyright, trade secret or other intellectual property right is
 *  granted to or conferred upon you by disclosure or delivery of the Materials, either expressly,
 *  by implication, inducement, estoppel or otherwise. Any license under such intellectual property
 *  rights must be express and approved by Intel in writing.
 */

/* Avoid multi inclusion of header file*/
#pragma once
#include "DeviceSimulation.h"

#pragma warning(disable : 4996)
#pragma warning(disable : 4127)
#pragma warning(disable : 4047)
#pragma warning(disable : 4090)
#pragma warning(disable : 4133)
#pragma warning(disable : 4024)

static OS_VERSION_INFOW OS_INFORMATION = { 0 };

OS_VERSION_INFOW GetWindowsVersion()
{
    CHAR  buffer[BUFFER_SIZE];
    FILE *pFileHandle = NULL;
    PCHAR pTemp       = NULL;
    ULONG osInfo[5]   = { 0 };
    do
    {
        if (0 != OS_INFORMATION.major_version || 0 != OS_INFORMATION.minor_version)
            break;
        pFileHandle = _popen("ver", "r");
        if (pFileHandle == NULL)
            break;

        while (fgets(buffer, BUFFER_SIZE, pFileHandle) != NULL)
        {
            INT index = 0;
            if (strlen(buffer) > 1)
            {
                pTemp = buffer;
                while (*pTemp)
                {
                    if (isdigit(*pTemp) && index < 5)
                        osInfo[index++] = strtol(pTemp, &pTemp, 10);
                    else
                        pTemp++;
                }
                break;
            }
        }
        _pclose(pFileHandle);

        OS_INFORMATION.major_version = osInfo[0];
        OS_INFORMATION.minor_version = osInfo[1];
        OS_INFORMATION.buildNumber   = osInfo[2];
        OS_INFORMATION.platformId    = osInfo[3];

    } while (FALSE);
    return OS_INFORMATION;
}

CDLL_EXPORT INT GetDLLVersion()
{
    /* Set current DLL version details*/
    return (INT)DLL_INTERFACE_VERSION;
}

CDLL_EXPORT HANDLE GetGfxValSimHandle()
{
    /* Init gfxValSim context*/
    if (InitializeGfxValSimulator() != S_OK)
    {
        ERROR_LOG("FAILED: Gfx Val Simulator Init Failed");
    }

    /* Return HANDLE*/
    return hGfxValSimHandle;
}

CDLL_EXPORT BOOL CloseGfxValSimHandle()
{
    /* close gfxValSim handle*/
    return CloseGfxValSimulator();
}

CDLL_EXPORT HRESULT InitAllPorts(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiNumPorts, UINT uiPortNum[], RX_TYPE eRxType[], bool bIsLFP[])
{
    return InitPort(pAdapterInfo, gfxAdapterInfoSize, uiNumPorts, uiPortNum, eRxType, bIsLFP);
}

CDLL_EXPORT HRESULT InitAllDPPorts(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiPortNum, DP_TOPOLOGY_TYPE eTopologyType)
{
    return InitDPPort(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, eTopologyType);
}

CDLL_EXPORT HRESULT Plug(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiPortNum, CHAR *pEdidFile, CHAR *pDpcdFile,
                         __in PDP_DPCD_MODEL_DATA pDPDPCDModelData, BOOL lowPower, __in UINT uiConnectorType, BOOL bIsLFP, __in UINT uiDongleType)
{
    return SimulatePlug(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, pEdidFile, pDpcdFile, pDPDPCDModelData, lowPower, uiConnectorType, bIsLFP, uiDongleType);
}

CDLL_EXPORT HRESULT UnPlug(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiPortNum, BOOL lowPower, __in UINT uiConnectorType)
{
    return SimulateUnPlug(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, lowPower, uiConnectorType);
}

CDLL_EXPORT HRESULT SetHPDInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiPortNum, BOOL bAttachorDettach, __in UINT uiConnectorType)
{
    return SetHPD(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, bAttachorDettach, uiConnectorType);
}

CDLL_EXPORT HRESULT TriggerHPDInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiPortNum, BOOL bAttachorDettach, __in UINT uiConnectorType)
{
    return TriggerHPD(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, bAttachorDettach, uiConnectorType);
}

CDLL_EXPORT HRESULT SetTEInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiPortNum)
{
    return GenerateMipiTeInterrupt(pAdapterInfo, gfxAdapterInfoSize, uiPortNum);
}

CDLL_EXPORT HRESULT ValSimDpcdWrite(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT uPort, _In_ UINT16 uOffset, _In_ UINT8 uValue)
{
    return PanelDpcdWrite(pAdapterInfo, uPort, uOffset, uValue);
}

CDLL_EXPORT HRESULT TriggerSCDCInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiPortNum, __in DD_SPI_EVENTS eScdcFailureType)
{
    return TriggerScdcInterrupt(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, eScdcFailureType);
}

/*
 * @brief        Exposed API for MMIO access
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    MMIO Access Args
 * @return       Return  True on success otherwise returns False
 */
CDLL_EXPORT BOOL ValSimMMIOAccess(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT gfxAdapterInfoSize, _In_ SIMDRV_MMIO_ACCESS_ARGS *pMMIOAccessArgs)
{
    HANDLE                   hGfxValSimHandle;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    hGfxValSimHandle = GetGfxValSimHandle();
    /* Check for GfxValSimDriver handler */
    if (hGfxValSimHandle == NULL)
    {
        DEBUG_LOG("Gfx Val Simulation driver not initialized!!!... Exiting...");
        return FALSE;
    }
    /* Check for pMMIOAccessArgs is null or not */
    if (pMMIOAccessArgs == NULL)
    {
        DEBUG_LOG("MMIO Access buffer is NULL!!!... Exiting...");
        return FALSE;
    }
    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    devIoControlBuffer.pInBuffer    = pMMIOAccessArgs;
    devIoControlBuffer.inBufferSize = sizeof(SIMDRV_MMIO_ACCESS_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_SIMDRVTOGFX_MMIO_ACCESS, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        DEBUG_LOG("Error: IoCTL Failed for MMIO Access with error code: 0x%u", GetLastError());
        return FALSE;
    }
    return TRUE;
}


/*
 * @brief        Exposed API for Wakelock access
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    Acquire or Release wakelock
 * @return       Return  True on success otherwise returns False
 */
CDLL_EXPORT BOOL ValSimWakeLockAccess(_In_ PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in BOOL bAcquireOrRelease)
{
    HANDLE                   hGfxValSimHandle;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    hGfxValSimHandle = GetGfxValSimHandle();
    /* Check for GfxValSimDriver handler */
    if (hGfxValSimHandle == NULL)
    {
        DEBUG_LOG("Gfx Val Simulation driver not initialized!!!... Exiting...");
        return FALSE;
    }
    
    SIMDRV_WAKE_LOCK_ACCESS_ARGS WakeLockAccessArgs = { 0 };
    WakeLockAccessArgs.accessType                   = SIMDRV_WAKE_LOCK_REQUEST_RELEASE;
    if (bAcquireOrRelease == TRUE)
    {
        WakeLockAccessArgs.accessType = SIMDRV_WAKE_LOCK_REQUEST_ACQUIRE;
    }

    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    devIoControlBuffer.pInBuffer    = &WakeLockAccessArgs;
    devIoControlBuffer.inBufferSize = sizeof(SIMDRV_WAKE_LOCK_ACCESS_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_SIMDRVTOGFX_WAKE_LOCK_ACCESS, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        DEBUG_LOG("Error: IoCTL Failed for WakeLock Access with error code: 0x%u", GetLastError());
        return FALSE;
    }
    return TRUE;
}

/*
 * @brief        Exposed API Reading display MMIO register
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    Offset
 * @param[out]   Ulong Pointer to get MMIO value
 * @return       Return  True on success otherwise returns False
 */
CDLL_EXPORT BOOL ValSimReadMMIO(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT gfxAdapterInfoSize, _In_ ULONG offset, _Out_ PULONG pValue)
{
    BOOL                    status = FALSE;
    SIMDRV_MMIO_ACCESS_ARGS mmio_access_args;
    if (NULL == pValue)
        return status;
    mmio_access_args.accessType = SIMDRV_GFX_ACCESS_REQUEST_READ;
    mmio_access_args.offset     = offset;
    mmio_access_args.pValue     = pValue;
    return ValSimMMIOAccess(pAdapterInfo, gfxAdapterInfoSize, &mmio_access_args);
}

/*
 * @brief        Exposed API Writing display MMIO register
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    Offset
 * @param[out]   Value
 * @return       Return  True on success otherwise returns False
 */
CDLL_EXPORT BOOL ValSimWriteMMIO(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT gfxAdapterInfoSize, _In_ ULONG offset, _In_ ULONG value)
{
    SIMDRV_MMIO_ACCESS_ARGS mmio_access_args;
    mmio_access_args.accessType = SIMDRV_GFX_ACCESS_REQUEST_WRITE;
    mmio_access_args.offset     = offset;
    mmio_access_args.pValue     = &value;
    return ValSimMMIOAccess(pAdapterInfo, gfxAdapterInfoSize, &mmio_access_args);
}

/*
 * @brief        Exposed API for Generic IOCTL Call
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    IOCTL Code
 * @param[in]    IOCTL Buffer
 * @param[in]    IOCTL Buffer size
 * @return       Return  True on success otherwise returns False
 */
CDLL_EXPORT BOOL ValsimIoctlCall(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT gfxAdapterInfoSize, _In_ ULONG ioctlCode, _In_ PVOID pInBuffer, _In_ ULONG inBufferSize,
                                 _In_ PVOID pOutBuffer, _In_ ULONG outBufferSize)
{
    HANDLE                   hGfxValSimHandle;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    hGfxValSimHandle = GetGfxValSimHandle();
    /* Check for GfxValSimDriver handler */
    if (hGfxValSimHandle == NULL)
    {
        ERROR_LOG("Gfx Val Simulation driver not initialized!!!... Exiting...");
        return FALSE;
    }
    // GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    devIoControlBuffer.pInBuffer     = pInBuffer;
    devIoControlBuffer.inBufferSize  = inBufferSize;
    devIoControlBuffer.pAdapterInfo  = pAdapterInfo;
    devIoControlBuffer.pOutBuffer    = pOutBuffer;
    devIoControlBuffer.outBufferSize = outBufferSize;

    ioctlCode = CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + ioctlCode), METHOD_BUFFERED, SIM_FILE_ACCESS);

    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)ioctlCode, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, NULL, &BytesReturned, NULL);
    if (0 == dwStatus)
    {
        ERROR_LOG("IoCTL Failed for ValsimIoctlCall with error code: 0x%u", GetLastError());
        return FALSE;
    }
    return TRUE;
}
