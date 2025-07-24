/**
 * @file
 * @section DeviceSimulation_c
 * @brief Internal source file which contains implementation required for device simulation
 *
 * @ref DeviceSimulation.c
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
 *  transmitted, distributed, or disclosed in any way without Intel's prior express written permission.
 *  <br>No license under any patent, copyright, trade secret or other intellectual property right is
 *  granted to or conferred upon you by disclosure or delivery of the Materials, either expressly,
 *  by implication, inducement, estoppel or otherwise. Any license under such intellectual property
 *  rights must be express and approved by Intel in writing.
 */
#pragma once
#include <sys/stat.h>
#include <direct.h>
#include <stdlib.h>
#include "DeviceSimulation.h"

extern char *LIBRARY_NAME = "GfxValSim.dll";

HRESULT InitializeGfxValSimulator()
{
    /* Check for GfxValSim existing handle*/
    if (NULL != hGfxValSimHandle)
    {
        // DEBUG_LOG("Returning existing handle of GfxValSim driver");
        return S_OK;
    }

    /* Get a handle to gfxValSim driver */
    hGfxValSimHandle = CreateFile(L"\\\\.\\SimDrvDosDev",             /* Device Name */
                                  GENERIC_READ | GENERIC_WRITE,       /* Desired Access*/
                                  FILE_SHARE_READ | FILE_SHARE_WRITE, /* Share Mode*/
                                  NULL,                               /* Default Security Attributes*/
                                  OPEN_EXISTING,                      /* Creation disposition*/
                                  0,                                  /* Flags & Attributes*/
                                  NULL                                /* Template File*/
    );

    if (INVALID_HANDLE_VALUE == hGfxValSimHandle)
    {
        DEBUG_LOG("Error in opening the Gfx Val Simulation driver handle with error code: %d", GetLastError());
        hGfxValSimHandle = NULL;
        return S_FALSE;
    }
    else
    {
        DEBUG_LOG("Successful: Get handle to Gfx Val Simulation driver");
        return S_OK;
    }
}

BOOL CloseGfxValSimulator()
{
    BOOL bStatus = TRUE;
    do
    {
        if (hGfxValSimHandle == NULL)
            break;

        bStatus          = CloseHandle(hGfxValSimHandle);
        hGfxValSimHandle = NULL;

    } while (FALSE);

    return bStatus;
}

HRESULT SimulatePlug(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in CHAR *pEdidFile, __in CHAR *pDpcdFile,
                     __in PDP_DPCD_MODEL_DATA pDPDPCDModelData, __in BOOL bLowPower, __in UINT uiConnectorType, __in BOOL bIsLFP, __in UINT uiDongleType)
{
    HRESULT bStatus = S_OK;
    /* Check for GfxValSim existing handle*/
    if (hGfxValSimHandle == NULL)
    {
        ERROR_LOG("Gfx Val Simulation driver not initialized");
        return S_FALSE;
    }

    /* Initializing DP ports before simulating, if the request is for DP */
    if (pDpcdFile != NULL)
    {
        bStatus = InitDPPort(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, eDPSST);
        if (bStatus != S_OK)
            return bStatus;
    }

    if (uiConnectorType > 3 || uiConnectorType < 0)
    {
        ERROR_LOG("Both Type-C and TBT cannot be enabled for Plug call");
        return S_FALSE;
    }

    INFO_LOG("Port = %d EDID = %s DPCD = %s", uiPortNum, pEdidFile, pDpcdFile);

    if (bLowPower == TRUE)
    {
        GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA stPowerData = { 0 };
        memset(&stPowerData, 0, sizeof(GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA));
        stPowerData.ulNumPorts                                                               = 1;
        stPowerData.stS3S4PortPlugUnplugData[0].eSinkPlugReq                                 = ePlugSink;
        stPowerData.stS3S4PortPlugUnplugData[0].ulPortNum                                    = uiPortNum;
        stPowerData.stS3S4PortPlugUnplugData[0].stS3S4DPPlugUnplugData.bPlugOrUnPlugAtSource = TRUE;
        stPowerData.stS3S4PortPlugUnplugData[0].uConnectorInfoAfterResume.Value              = (UCHAR)uiConnectorType;
        stPowerData.stS3S4PortPlugUnplugData[0].uiDongleType                                 = uiDongleType;
        if (pDpcdFile != NULL)
        {
            stPowerData.stS3S4PortPlugUnplugData[0].stS3S4DPPlugUnplugData.eTopologyAfterResume = eDPSST;
        }

        /* Send low power state data to GfxValSimulator for resume events*/
        bStatus = SetLowPowerState(pAdapterInfo, gfxAdapterInfoSize, &stPowerData);
        if (bStatus != S_OK)
            return bStatus;

        /* Pass the EDID DATA to GfxValSimulator */
        bStatus = SetEDIDDPCDData(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, pEdidFile, IOCTL_SET_GFXS3S4_EDID_DATA);
        if (bStatus != S_OK)
            return bStatus;

        if (pDPDPCDModelData != NULL)
        {
            /* Pass the DPCD Model Data to GfxValSimulator*/
            bStatus = SetLTModelData(pAdapterInfo, gfxAdapterInfoSize, pDPDPCDModelData, IOCTL_SET_GFXS3S4_DPCD_MODEL_DATA);
            if (bStatus != S_OK)
                return bStatus;
        }

        if (pDpcdFile != NULL)
        {
            /* Pass the DPCD DATA to GfxValSimulator */
            bStatus = SetEDIDDPCDData(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, pDpcdFile, IOCTL_SET_GFXS3S4_DPCD_DATA);
            if (bStatus != S_OK)
                return bStatus;
        }
    }
    else
    {
        InitDongleType(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, uiDongleType);

        /* Pass the EDID DATA to GfxValSimulator */
        bStatus = SetEDIDDPCDData(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, pEdidFile, IOCTL_SET_EDID_DATA);
        if (bStatus != S_OK)
            return bStatus;

        if (pDPDPCDModelData != NULL)
        {
            INFO_LOG("Setting DPCD model Data");
            /* Pass the DPCD Model Data to GfxValSimulator*/
            bStatus = SetLTModelData(pAdapterInfo, gfxAdapterInfoSize, pDPDPCDModelData, IOCTL_SET_DPCD_MODEL_DATA);
            if (bStatus != S_OK)
                return bStatus;
        }

        if (pDpcdFile != NULL)
        {
            /* Pass the DPCD DATA to GfxValSimulator */
            INFO_LOG("Setting DPCD");
            bStatus = SetEDIDDPCDData(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, pDpcdFile, IOCTL_SET_DPCD_DATA);
            if (bStatus != S_OK)
                return bStatus;
        }

        if (bIsLFP == FALSE)
        { // For embedded display, it is expected to be plugged, HPD is not needed
            /* Generate the HPD - with True for the 'port' number passed */
            bStatus = SetHPD(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, TRUE, uiConnectorType);
            if (bStatus != S_OK)
                return bStatus;
        }
    }
    return S_OK;
}

HRESULT SimulateUnPlug(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in BOOL bLowPower, __in UINT uiConnectorType)
{
    HRESULT bStatus = S_OK;
    /* Check for GfxValSim existing handle*/
    if (hGfxValSimHandle == NULL)
    {
        ERROR_LOG("Gfx Val Simulation driver not initialized");
        return S_FALSE;
    }

    if (uiConnectorType > 3 || uiConnectorType < 0)
    {
        ERROR_LOG("Both Type-C and TBT cannot be enabled for Plug call");
        return S_FALSE;
    }

    if (bLowPower == TRUE)
    {
        GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA stPowerData = { 0 };
        memset(&stPowerData, 0, sizeof(GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA));
        stPowerData.ulNumPorts                                                               = 1;
        stPowerData.stS3S4PortPlugUnplugData[0].eSinkPlugReq                                 = eUnplugSink;
        stPowerData.stS3S4PortPlugUnplugData[0].ulPortNum                                    = uiPortNum;
        stPowerData.stS3S4PortPlugUnplugData[0].stS3S4DPPlugUnplugData.bPlugOrUnPlugAtSource = TRUE;
        stPowerData.stS3S4PortPlugUnplugData[0].uConnectorInfoAfterResume.Value              = (UCHAR)uiConnectorType;
        bStatus                                                                              = SetLowPowerState(pAdapterInfo, gfxAdapterInfoSize, &stPowerData);
    }
    else
    {
        /* Call SetHPD - with False*/
        bStatus = SetHPD(pAdapterInfo, gfxAdapterInfoSize, uiPortNum, FALSE, uiConnectorType);
    }
    return bStatus;
}

HRESULT InitPort(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiNumPorts, __in UINT uiPortNum[], __in RX_TYPE eRxType[], __in bool bIsLFP[])
{
    UINT                     portIndex          = 0;
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    PPORT_INFO               pPortInfo          = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };
    HRESULT                  result             = S_OK;

    /* Check for GfxValSim existing handle*/
    if (hGfxValSimHandle == NULL)
    {
        ERROR_LOG("Gfx Val Simulation driver not initialized");
        return S_FALSE;
    }
    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    /* Check if number of ports is zero */
    if (uiNumPorts == 0)
    {
        ERROR_LOG("There are no ports available");
        return S_FALSE;
    }

    DEBUG_LOG("number of ports: %d", uiNumPorts);

    for (portIndex = 0; portIndex < uiNumPorts; portIndex++)
    {
        INFO_LOG("Init port %d Rx Type %d", uiPortNum[portIndex], eRxType[portIndex]);
        pPortInfo = (PPORT_INFO)malloc(sizeof(PORT_INFO));
        /* Check for PPORT_INFO pointer for NULL value */
        if (pPortInfo == NULL)
        {
            ERROR_LOG("PortInfo Object is NULL");
            return S_FALSE;
        }
        memset(pPortInfo, 0, sizeof(PORT_INFO));

        /* Populating port number and plug/unplug status */
        pPortInfo->ulPortNum = uiPortNum[portIndex];
        pPortInfo->eRxTypes  = eRxType[portIndex];
        if (bIsLFP[portIndex]) // For embedded display, it is expected to be plugged
        {
            pPortInfo->eInitialPlugState = eSinkPlugged;
        }
        else
        {
            pPortInfo->eInitialPlugState = eSinkUnplugged;
        }

        devIoControlBuffer.pInBuffer    = pPortInfo;
        devIoControlBuffer.inBufferSize = sizeof(PORT_INFO);
        devIoControlBuffer.pAdapterInfo = pAdapterInfo;

        /* Send DeviceIoCtl for port objects. DP GfxValSim driver doesn't expect/return any argument */
        dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_INIT_PORT_INFO, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

        if (OPERATION_FAILED == dwStatus)
        {
            ERROR_LOG("IoCTL Failed while initializing port with error code 0x%u", GetLastError());
            result = S_FALSE;
        }

        if (pPortInfo != NULL)
        {
            free(pPortInfo);
        }
    }

    return result;
}

HRESULT InitDPPort(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in DP_TOPOLOGY_TYPE eTopologyType)
{
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    PDP_INIT_INFO            pDPInfo            = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    if (hGfxValSimHandle == NULL)
    {
        ERROR_LOG("Gfx Val Simulation driver not initialized");
        return S_FALSE;
    }
    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    INFO_LOG("Port number = %d DP Topology = %d", uiPortNum, eTopologyType);

    pDPInfo = (PDP_INIT_INFO)malloc(sizeof(DP_INIT_INFO));
    /* Check for PDP_INIT_INFO pointer for NULL value */
    if (pDPInfo == NULL)
    {
        ERROR_LOG("pDPInfo Object is NULL");
        return S_FALSE;
    }
    memset(pDPInfo, 0, sizeof(DP_INIT_INFO));

    /* Populating port number and plug/unplug status */
    pDPInfo->uiPortNum     = uiPortNum;
    pDPInfo->eTopologyType = eTopologyType;

    devIoControlBuffer.pInBuffer    = pDPInfo;
    devIoControlBuffer.inBufferSize = sizeof(DP_INIT_INFO);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    /* Send DeviceIoCtl for port objects. DP GfxValSim driver doesn't expect/return any argument */
    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_INIT_DP_TOPOLOGY, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

    if (OPERATION_FAILED == dwStatus)
    {
        ERROR_LOG("IoCTL Failed while initialization DP object with error code 0x%u", GetLastError());
        return S_FALSE;
    }

    if (pDPInfo != NULL)
    {
        free(pDPInfo);
    }

    return S_OK;
}
HRESULT SetHPD(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in BOOL bAttachorDettach, __in UINT uiConnectorType)
{
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    PPORT_HPD_ARGS           pPortHPDData       = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    /* Memory Allocation for Branch/Display Nodes in Topology XML*/
    pPortHPDData = (PPORT_HPD_ARGS)malloc(sizeof(PORT_HPD_ARGS));
    if (pPortHPDData == NULL)
    {
        ERROR_LOG("Failed to allocate Memory for Port HPD data");
        return S_FALSE;
    }

    memset(pPortHPDData, 0, sizeof(PORT_HPD_ARGS));

    /* Populating port number and plug/unplug status */
    pPortHPDData->ulPortNum                = uiPortNum;
    pPortHPDData->bAttachorDettach         = bAttachorDettach;
    pPortHPDData->uPortConnectorInfo.Value = (UCHAR)uiConnectorType;

    INFO_LOG("Port = %d Attach/Dettach = %d Connector Type = %d", uiPortNum, bAttachorDettach, uiConnectorType);

    devIoControlBuffer.pInBuffer    = pPortHPDData;
    devIoControlBuffer.inBufferSize = sizeof(PORT_HPD_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    /* IoCTL call for sending EDID/DPCD data to Simulation driver */
    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_GENERATE_HPD, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);
    INFO_LOG("SetHpd IOCTL returned status: %d", dwStatus);

    if (OPERATION_FAILED == dwStatus)
    {
        ERROR_LOG("Failed to send IOCTLs during Set HPD call with error code 0x%u", GetLastError());
        return S_FALSE;
    }

    if (pPortHPDData != NULL)
    {
        free(pPortHPDData);
    }

    return S_OK;
}

HRESULT TriggerHPD(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in BOOL bAttachorDettach, __in UINT uiConnectorType)
{
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    PPORT_HPD_ARGS           pPortHPDData       = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    /* Memory Allocation for Branch/Display Nodes in Topology XML*/
    pPortHPDData = (PPORT_HPD_ARGS)malloc(sizeof(PORT_HPD_ARGS));
    if (pPortHPDData == NULL)
    {
        ERROR_LOG("Failed to allocate Memory for Port HPD data");
        return S_FALSE;
    }

    memset(pPortHPDData, 0, sizeof(PORT_HPD_ARGS));

    /* Populating port number and plug/unplug status */
    pPortHPDData->ulPortNum                = uiPortNum;
    pPortHPDData->bAttachorDettach         = bAttachorDettach;
    pPortHPDData->uPortConnectorInfo.Value = (UCHAR)uiConnectorType;

    INFO_LOG("Port = %d Attach/Dettach = %d Connector Type = %d", uiPortNum, bAttachorDettach, uiConnectorType);

    devIoControlBuffer.pInBuffer    = pPortHPDData;
    devIoControlBuffer.inBufferSize = sizeof(PORT_HPD_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    /* IoCTL call for sending EDID/DPCD data to Simulation driver */
    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_TRIGGER_HPD, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

    if (OPERATION_FAILED == dwStatus)
    {
        ERROR_LOG("Failed to send IOCTLs during Trigger HPD call:  0x%u", GetLastError());
        return S_FALSE;
    }

    if (pPortHPDData != NULL)
    {
        free(pPortHPDData);
    }

    return S_OK;
}

HRESULT GenerateMipiTeInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum)
{
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    PPORT_HPD_ARGS           pPortHPDData       = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    /* Memory Allocation for Branch/Display Nodes in Topology XML*/
    pPortHPDData = (PPORT_HPD_ARGS)malloc(sizeof(PORT_HPD_ARGS));
    if (pPortHPDData == NULL)
    {
        ERROR_LOG("Failed to allocate Memory for Port HPD data");
        return S_FALSE;
    }

    memset(pPortHPDData, 0, sizeof(PORT_HPD_ARGS));

    /* Populating port number and plug/unplug status */
    pPortHPDData->ulPortNum = uiPortNum;

    DEBUG_LOG("port number : %d", uiPortNum);

    devIoControlBuffer.pInBuffer    = pPortHPDData;
    devIoControlBuffer.inBufferSize = sizeof(PORT_HPD_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    /* IoCTL call for sending EDID/DPCD data to Simulation driver */
    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_GENERATE_MIPI_DSI_TE, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

    if (pPortHPDData != NULL)
    {
        free(pPortHPDData);
    }

    if (OPERATION_FAILED == dwStatus)
    {
        ERROR_LOG("Failed to send IOCTLs during IOCTL_GENERATE_MIPI_DSI_TE to Gfx Sim driver with error code: 0x%u", GetLastError());
        return S_FALSE;
    }

    return S_OK;
}

HRESULT SetEDIDDPCDData(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in CHAR *pFile, __in ULONG ulIOCTLNum)
{
    DWORD dwStatus      = 0;
    DWORD BytesReturned = 0;
    INT   iFileSize;
    CHAR  chFilePath[256];

    struct stat st;
    size_t      bytes_read = 0;
    errno_t     err        = 0;

    FILE *                   fptrBuff;
    BYTE *                   pFileDataBuffer    = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    /* EDID and DPCD complete path is sent from python script*/
    if (pFile == NULL)
    {
        ERROR_LOG("EDID file path is empty");
        return S_FALSE;
    }
    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    strcpy_s(chFilePath, 255, pFile);

    /* Fill the size of the EDID in the 4 bytes of edidBuffer*/
    stat(chFilePath, &st);
    iFileSize       = st.st_size;
    pFileDataBuffer = (BYTE *)malloc(sizeof(FILE_DATA) + iFileSize);
    if (pFileDataBuffer == NULL)
    {
        return S_FALSE;
    }
    ZeroMemory(pFileDataBuffer, sizeof(FILE_DATA) + iFileSize);
    /* Populate the port number to file structure*/
    ((PFILE_DATA)pFileDataBuffer)->uiPortNum = uiPortNum;

    /* Populate the file size to file structure*/
    ((PFILE_DATA)pFileDataBuffer)->uiDataSize = iFileSize;

    // ucNodeName is not required SST and tiled cases and it is used only in MST case
    // strcpy_s((char *)(((PFILE_DATA)pFileDataBuffer)->ucNodeName), iFileSize, pFile);
    err = fopen_s(&fptrBuff, chFilePath, "rb");
    if (err == 0)
    {
        if (fptrBuff != NULL)
        {
            bytes_read = fread((pFileDataBuffer + sizeof(FILE_DATA)), sizeof(unsigned char), iFileSize, fptrBuff);

            /* Close the file handle*/
            fclose(fptrBuff);
        }
    }
    else
    {
        DEBUG_LOG("DPCD file read failed!!! Exiting with error code : 0x%u", GetLastError());
        return S_FALSE;
    }

    DEBUG_LOG("Port number : %d, file : %s, IOCTL no : %d", uiPortNum, pFile, ulIOCTLNum);

    devIoControlBuffer.pInBuffer    = pFileDataBuffer;
    devIoControlBuffer.inBufferSize = (sizeof(FILE_DATA) + iFileSize);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    /* IoCTL call for sending EDID/DPCD data to Simulation driver */
    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)ulIOCTLNum, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

    /* free file data buffer created */
    if (pFileDataBuffer != NULL)
    {
        free(pFileDataBuffer);
    }

    if (OPERATION_FAILED == dwStatus)
    {
        ERROR_LOG("Failed to send IOCTLs during EDID data to Gfx Sim driver with error code: 0x%u", GetLastError());
        return S_FALSE;
    }

    return S_OK;
}

HRESULT SetLowPowerState(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA pPowerData)
{
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    /* Check for pPowerData pointer for NULL value */
    if (pPowerData == NULL)
    {
        DEBUG_LOG("Failed to allocate Memory for Port HPD data");
        return S_FALSE;
    }
    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    devIoControlBuffer.pInBuffer    = pPowerData;
    devIoControlBuffer.inBufferSize = sizeof(GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    /* Send DeviceIoCtl to plug/unplug display in low power mode */
    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_GFXS3S4_PLUGUNPLUG_DATA, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

    if (OPERATION_FAILED == dwStatus)
    {
        ERROR_LOG("Failed to send IOCTLs during Set HPD call to Gfx Sim driver with error code: 0x%u", GetLastError());
        return S_FALSE;
    }

    return S_OK;
}

HRESULT SetLTModelData(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in PDP_DPCD_MODEL_DATA pDPDPCDModelData, __in ULONG ulIOCTLNum)
{
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    // pointer to DPCD model data (pDPDPCDModelData) received from python. Passing same pointer directly to Valsim driver.
    devIoControlBuffer.pInBuffer    = pDPDPCDModelData;
    devIoControlBuffer.inBufferSize = sizeof(DP_DPCD_MODEL_DATA);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    /* IoCTL call for sending DPCD model data to Simulation driver */
    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)ulIOCTLNum, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

    if (OPERATION_FAILED == dwStatus)
    {
        ERROR_LOG("Failed to send IOCTLs during send DPCD model data to Gfx Sim driver with error code: 0x%u", GetLastError());
        return S_FALSE;
    }
    return S_OK;
}

HRESULT InitDongleType(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in UINT uiDongleType)
{
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    PDONGLE_TYPE_INFO        pDongleTypeInfo    = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    if (hGfxValSimHandle == NULL)
    {
        ERROR_LOG("Gfx Val Simulation driver not initialized");
        return S_FALSE;
    }
    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    INFO_LOG("Port number = %d DongleType = %d", uiPortNum, uiDongleType);

    pDongleTypeInfo = (PDONGLE_TYPE_INFO)malloc(sizeof(DONGLE_TYPE_INFO));

    if (pDongleTypeInfo == NULL)
    {
        ERROR_LOG("pDongleTypeInfo Object is NULL!!!... Exiting...");
        return S_FALSE;
    }
    memset(pDongleTypeInfo, 0, sizeof(DONGLE_TYPE_INFO));

    /* Populating port number and DongleType */
    pDongleTypeInfo->uiPortNum    = uiPortNum;
    pDongleTypeInfo->uiDongleType = uiDongleType;

    devIoControlBuffer.pInBuffer    = pDongleTypeInfo;
    devIoControlBuffer.inBufferSize = sizeof(DONGLE_TYPE_INFO);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_SET_DONGLE_TYPE, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

    if (pDongleTypeInfo != NULL)
    {
        free(pDongleTypeInfo);
    }

    if (OPERATION_FAILED == dwStatus)
    {
        ERROR_LOG("IoCTL Failed while initializing DongleType.");
        return S_FALSE;
    }

    return S_OK;
}

HRESULT PanelDpcdWrite(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT uPort, _In_ UINT16 uOffset, _In_ UINT8 uValue)
{
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    PDPCD_ARGS               pDpcdData          = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    /* Memory Allocation */
    pDpcdData = (PDPCD_ARGS)malloc(sizeof(PDPCD_ARGS));
    if (pDpcdData == NULL)
    {
        ERROR_LOG("Failed to allocate Memory for Panel Dpcd data !!!... Exiting...");
        return S_FALSE;
    }

    memset(pDpcdData, 0, sizeof(PDPCD_ARGS));

    /* Populating DPCD args */
    pDpcdData->ulPortNum = uPort;
    pDpcdData->uOffset   = uOffset;
    pDpcdData->uValue    = uValue;

    INFO_LOG("Port = %d DPCD offset = %04x Value = %d", uPort, uOffset, uValue);

    devIoControlBuffer.pInBuffer    = pDpcdData;
    devIoControlBuffer.inBufferSize = sizeof(PDPCD_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    /* IoCTL call for sending EDID/DPCD data */
    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_TRIGGER_DPCD_WRITE, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

    if (pDpcdData != NULL)
    {
        free(pDpcdData);
    }

    if (OPERATION_FAILED == dwStatus)
    {
        ERROR_LOG("Failed to send IOCTLs during Panel DPCD update call:  0x%u", GetLastError());
        return S_FALSE;
    }

    return S_OK;
}

HRESULT TriggerScdcInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiPortNum, __in DD_SPI_EVENTS eSpiEventType)
{
    DWORD                    dwStatus           = 0;
    DWORD                    BytesReturned      = 0;
    PSCDC_ARGS               pScdcData          = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize);

    /* Memory Allocation for Branch/Display Nodes in Topology XML*/
    pScdcData = (PSCDC_ARGS)malloc(sizeof(SCDC_ARGS));
    if (pScdcData == NULL)
    {
        ERROR_LOG("Failed to allocate Memory for SCDC data !!!... Exiting...");
        return S_FALSE;
    }

    memset(pScdcData, 0, sizeof(PSCDC_ARGS));

    /* Populating port number and plug/unplug status */
    pScdcData->ulPortNum     = uiPortNum;
    pScdcData->eSpiEventType = eSpiEventType;

    DEBUG_LOG("Port Number: %d", uiPortNum);

    devIoControlBuffer.pInBuffer    = pScdcData;
    devIoControlBuffer.inBufferSize = sizeof(PSCDC_ARGS);
    devIoControlBuffer.pAdapterInfo = pAdapterInfo;

    /* IoCTL call for sending port info, invoking SCDC interrupt, to Simulation driver */
    dwStatus = DeviceIoControl(hGfxValSimHandle, (DWORD)IOCTL_TRIGGER_SCDC_INTERRUPT, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

    if (pScdcData != NULL)
    {
        free(pScdcData);
    }

    if (OPERATION_FAILED == dwStatus)
    {
        ERROR_LOG("Failed to send IOCTLs during IOCTL_TRIGGER_SCDC_INTERRUPT to Gfx Sim driver with error code: 0x%u", GetLastError());
        return S_FALSE;
    }
    return S_OK;
}
