/**
 * @file
 * @section DeviceSimulation_h
 * @brief Internal header file which contains data structures and helper functions required for device simulation etc..,
 *
 * @ref DeviceSimulation.h
 * @author Reeju Srivastava, Aafiya Kaleem
 */

/**********************************************************************************
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
#include "CommonDetails.h"

#define OPERATION_FAILED 0 // 0 indicates DeviceIOControl call failed

/**
 * @brief        Internal API to create gfxValStub driver context
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT InitializeGfxValSimulator();

/**
 * @brief        Internal API to close the handle of gfxvalsimulator
 * @return       If the function succeeds, the return value is nonzero
 */
BOOL CloseGfxValSimulator();

/**
 * @brief        Internal API to handle Plug devices request
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   pEdidFile contains name of edid file
 * @params[in]   pDpcdFile contains name of dpcd file
 * @params[in]   pDPDPCDModelData is pointer to DP DPCD model data which contains port num, topology type and DPCD model data
 * @params[in]   lowPower it can be True or False for Low power plug scenario
 * @params[in]   uiConnectorType contains port type to be plugged - NATIVE/TC/TBT
 * @params[in]   bIsLFP is boolean to indicate embedded/external displays
 * @params[in]   uiDongleType contains dongle type to be plugged - Default/Type1/Type2/DVI/LsPCon
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT SimulatePlug(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in CHAR *pEdidFile, __in CHAR *pDpcdFile,
                     __in PDP_DPCD_MODEL_DATA pDPDPCDModelData, __in BOOL bLowPower, __in UINT uiConnectorType, __in BOOL bIsLFP, __in UINT uiDongleType);

/**
 * @brief        Internal API to handle UnPlug devices request
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   lowPower it can be True or False for Low power plug scenario
 * @params[in]   uiConnectorType contains port type to be unplugged - NATIVE/TC/TBT
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT SimulateUnPlug(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in BOOL bLowPower, __in UINT uiConnectorType);

/**
 * @brief        Internal API to handle SetHPD devices request
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   bAttachorDettach is flag True or False
 * @params[in]   uiConnectorType contains port type for - NATIVE/TC/TBT
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT SetHPD(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in BOOL bAttachorDettach, __in UINT uiConnectorType);

/**
 * @brief        Internal API to handle TriggerHPD devices request
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   bAttachorDettach is flag True or False
 * @params[in]   uiConnectorType contains port type for - NATIVE/TC/TBT
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT TriggerHPD(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in BOOL bAttachorDettach, __in UINT uiConnectorType);

/**
 * @brief        Internal API to handle to Generate TE interrupt for MIPI
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum of type MIPI_DSI_PORT_TYPE
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT GenerateMipiTeInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum);

/**
 * @brief        Internal API to handle setting EDID/DPCD request to uiPortNum
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   pFile contains EDID or DPCD file name
 * @params[in]   ulIOCTLNum for passed EDID or DPCD
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT SetEDIDDPCDData(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in CHAR *pFile, __in ULONG ulIOCTLNum);

/**
 * @brief        Internal API to handle UnPlug devices request
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiNumPorts number of ports to be initialised
 * @params[in]   uiPortNum contains display port number
 * @params[in]   eRxType is enum type RX_TYPE
 * @params[in]   bIsLFP is boolean to indicate embedded/external displays
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT InitPort(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiNumPorts, __in UINT uiPortNum[], __in RX_TYPE eRxType[], __in bool bIsLFP[]);

/**
 * @brief        Internal API to handle UnPlug devices request
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   eTopologyType is enum type DP_TOPOLOGY_TYPE
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT InitDPPort(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in DP_TOPOLOGY_TYPE eTopologyType);

/**
 * @brief        Internal API to handle low power plug/unplug request
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   pPowerData contains port data to be used after power events
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT SetLowPowerState(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA pPowerData);

/**
 * @brief        Internal API to handle setting LT model data request to uiPortNum
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   pDPDPCDModelData is pointer to structure containing port num, topology type, and the DPCD model data
 * @params[in]   ulIOCTLNum tells which IOCTL to call
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT SetLTModelData(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in PDP_DPCD_MODEL_DATA pDPDPCDModelData, __in ULONG ulIOCTLNum);

/**
 * @brief        Internal API to set DongleType
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   uiDongleType specifies type of Dongle
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT InitDongleType(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in UINT uiDongleType);

/*
 * @brief        Exposed API Writing panel ReadOnly Dpcd's
 * @params[in]   Adapter info
 * @params[in]   Port
 * @param[in]    Offset
 * @param[in]    Value
 * @return       Return  True on success otherwise returns False
 */
HRESULT PanelDpcdWrite(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT uPort, _In_ UINT16 uOffset, _In_ UINT8 uValue);

/**
 * @brief        Internal API to trigger SCDC Interrupt
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   uiPortNum contains display port number
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
HRESULT TriggerScdcInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiPortNum, __in DD_SPI_EVENTS eSpiEventType);
