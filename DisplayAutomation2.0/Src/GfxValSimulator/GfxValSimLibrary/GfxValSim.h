/**
 * @file
 * @addtogroup CDll_GfxValSim
 * @brief
 * DLL provide user interface to interact with gfxValSimulator driver for device simulation, VBT, MPO, Register read/write etc.., functionalities
 * @remarks
 * DisplayDeviceSimulation dll exposes APIs to simulated various display devices like eDP, DP, HDMI, MIPI, USB-typeC and VBT related get and set functionalities.
 * <ul>
 * <li><b>Display Simulation APIs</b> \n
 * <ul>
 * <li> @ref InitGfxValSimulator \n			\copybrief InitGfxValSimulator \n
 * <li> @ref InitAllPorts \n					\copybrief InitAllPorts \n
 * <li> @ref Plug   \n						\copybrief Plug \n
 * <li> @ref UnPlug \n						\copybrief UnPlug \n
 * </ul>
 * </li>
 * <li><b>VBT APIs</b> \n
 * <ul>
 * <li> @ref EnableDisableVBTSimulation \n	\copybrief EnableDisableVBTSimulation \n
 * <li> @ref GetSetVbt \n					\copybrief GetSetVbt \n
 * </ul>
 * </li>
 * <li><b>DSB APIs</b> \n
 * <ul>
 * <li> @ref GfxValSimTriggerDSB \n	\copybrief GfxValSimTriggerDSB \n
 * </ul>
 * </li>
 *
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

/* Avoid multi inclusion of header file*/
#pragma once
#include <Windows.h>
#include <stdbool.h>

#include "..\\GfxValSimDriver\\DriverInterfaces\\CommonIOCTL.h"
#include "Brightness3Commands.h"
#include "DisplayStateBuffer.h"
#include "DispDiag.h"
#include "MIPIDSICommands.h"
#include <cfgmgr32.h>

/* Preprocessor Macros*/
#ifdef _DLL_EXPORTS
#define CDLL_EXPORT __declspec(dllexport)
#else
#define CDLL_EXPORT __declspec(dllimport)
#endif

static const GUID SIMDRV_INTERFACE_GUID = { 0xa9cd4d20, 0xccb8, 0x414f, 0xb0, 0x35, 0x82, 0x7a, 0x4, 0x2e, 0x6, 0x87 };

#define SIMDRV_REG_PATH "System\\CurrentControlSet\\Services\\GfxValSimDriver"
#define RS5_BASE_BUILD_VERSION 17700
#define BUFFER_SIZE 256
#define MAX_STRING_LEN 128

#define REGISTRY_ACCESS_STATUS_CHECK(statusCode) \
    {                                            \
        if (0 != statusCode)                     \
            return statusCode;                   \
    }

/** Structure Defination to hold OS Information */
typedef struct _OS_VERSION_INFOW
{
    ULONG major_version;
    ULONG minor_version;
    ULONG buildNumber;
    ULONG platformId;
} OS_VERSION_INFOW, *POS_VERSION_INFOW;

/* Registry Values in winnt.h */
typedef enum _REGISTRY_TYPES
{
    REGISTRY_BINARY = 3,
    REGISTRY_DWORD  = 4,
    REGISTRY_MAX    = 5,
} REGISTRY_TYPES;

typedef enum _SIMDRV_GFX_ACCESS_REQUEST_TYPE
{
    SIMDRV_GFX_ACCESS_REQUEST_READ,
    SIMDRV_GFX_ACCESS_REQUEST_WRITE,
} SIMDRV_GFX_ACCESS_REQUEST_TYPE;

typedef struct _SIMDRV_MMIO_ACCESS_ARGS
{
    SIMDRV_GFX_ACCESS_REQUEST_TYPE accessType;
    ULONG                          offset;
    PULONG                         pValue;
} SIMDRV_MMIO_ACCESS_ARGS;


typedef enum _SIMDRV_WAKE_LOCK_REQUEST_TYPE
{
    SIMDRV_WAKE_LOCK_REQUEST_ACQUIRE,
    SIMDRV_WAKE_LOCK_REQUEST_RELEASE,
} SIMDRV_WAKE_LOCK_REQUEST_TYPE;

typedef struct _SIMDRV_WAKE_LOCK_ACCESS_ARGS
{
    SIMDRV_WAKE_LOCK_REQUEST_TYPE accessType;
} SIMDRV_WAKE_LOCK_ACCESS_ARGS;

#pragma pack()

/* Details of functinality exposed by the utility DLL*/
/**
 * @brief        Interface to get version details of DLL
 * @param[In]    VOID
 * @return       Contains information about DLL version
 */
CDLL_EXPORT INT GetDLLVersion();

/**
 * @brief        Exposed API to initialize Gfx val simulation driver and get the handle and state
 * @param[In]    VOID
 * @return       HANDLE of GfxValSimulator if successful otherwise INVALID_HANDLE_VALUE
 */
extern CDLL_EXPORT HANDLE GetGfxValSimHandle();

/**
 * @brief        Exposed API to close the handle of gfxvalsimulator
 * @return       If the function succeeds, the return value is nonzero
 */
CDLL_EXPORT BOOL CloseGfxValSimHandle();

/**
 * @brief        Exposed API to Initialize all the available ports on the execution platform
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    uiNumPorts, uiPortNum, eRxType is needed for Initializing the port objects
 * @params[in]   bIsLFP is boolean to indicate embedded/external displays
 * @return       HRESULT		'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
CDLL_EXPORT HRESULT InitAllPorts(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiNumPorts, __in UINT uiPortNum[], __in RX_TYPE eRxType[],
                                 __in bool bIsLFP[]);

/**
 * @brief        Exposed API to Initialize all DP port (SST/MST) on the execution platform
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    uiPortNum, eTopologyType is needed for Initializing the DP port objects
 * @return       HRESULT		'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
CDLL_EXPORT HRESULT InitAllDPPorts(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in DP_TOPOLOGY_TYPE eTopologyType);

/**
 * @brief        Exposed API to Plug devices
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   pEdidFile		contains name of edid file
 * @params[in]   pDpcdFile		contains name of dpcd file
 * @params[in]   pDPDPCDModelData is pointer to structure containing port num, topology type, and the DPCD model data
 * @params[in]   lowPower		it can be True or False for Low power plug scenarios
 * @params[in]   uiConnectorType contains port type to be plugged - NATIVE/TC/TBT
 * @params[in]   bIsLFP is boolean to indicate embedded/external displays
 * @params[in]   uiDongleType contains dongle type to be plugged - Type1/Type2/DVI/LsPCon
 * @return       HRESULT			'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
CDLL_EXPORT HRESULT Plug(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in CHAR *pEdidFile, __in CHAR *pDpcdFile,
                         __in PDP_DPCD_MODEL_DATA pDPDPCDModelData, __in BOOL lowPower, __in UINT uiConnectorType, __in BOOL bIsLFP, __in UINT uiDongleType);

/**
 * @brief        Exposed API to Initialize DP devices
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    uiPortNum contains display port number
 * @params[in]   lowPower	it can be True or False for Low power plug scenarios
 * @params[in]   uiConnectorType contains port type to be unplugged - NATIVE/TC/TBT
 * @return       HRESULT		'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
CDLL_EXPORT HRESULT UnPlug(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in BOOL lowPower, __in UINT uiConnectorType);

/**
 * @brief        Internal API to handle SetHPD devices request
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   bAttachorDettach is flag True or False
 * @params[in]   uiConnectorType contains port type for HPD - NATIVE/TC/TBT
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
CDLL_EXPORT HRESULT SetHPDInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in BOOL bAttachorDettach, __in UINT uiConnectorType);

/**
 * @brief        Internal API to handle TriggerHPD devices request
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   bAttachorDettach is flag True or False
 * @params[in]   uiConnectorType contains port type for HPD - NATIVE/TC/TBT
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
CDLL_EXPORT HRESULT TriggerHPDInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum, __in BOOL bAttachorDettach,
                                        __in UINT uiConnectorType);

CDLL_EXPORT HRESULT SetTEInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT uiPortNum);

/**
 * @brief			Exposed API to Get and Set VBT Data based on BlockID
 * @params[in]		blockId		block number to be read or set
 * @params[inout]	pBlockData  Block data to be read or set
 * @params[in]		bSet		true if read operation and false if write
 * @return			HRESULT '	S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
CDLL_EXPORT HRESULT GetSetVbtBlock(__inout PBYTE pBlockData, __in BOOL bSet);

/**
 * @brief			Exposed API to Get and Set VBT Data based on BlockID
 * @params[in]		dataSize	size of data
 * @params[inout]	pVbtData    VBT data to be read or set
 * @params[in]		bSet		true if read operation and false if write
 * @return			HRESULT '	S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
CDLL_EXPORT HRESULT ReadWriteVBT(__inout PBYTE pVbtData, __inout UINT32 dataSize, __in BOOL bSet);

/**
 * @brief        Exposed API to Simulate VBT
 * @params[in]   flag		True to enable and False to disable simulation
 * @return       HRESULT		'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
CDLL_EXPORT HRESULT EnableDisableVBTSimulation(__in BOOL bFlag);

/**
 * @brief        Exposed API for Trigger DSB
 * @params[in]   pDsbBufferArgs DSB buffer data
 * @return       ULONG Returns Status Code
 */
CDLL_EXPORT ULONG GfxValSimTriggerDSB(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in SIMDRV_DSB_BUFFER_ARGS *pDsbBufferArgs);

/*
 * @brief        Exposed API for MMIO access
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    MMIO Access Args
 * @return       Return  True on success otherwise returns False
 */
CDLL_EXPORT BOOL ValSimMMIOAccess(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, _In_ SIMDRV_MMIO_ACCESS_ARGS *pMMIOAccessArgs);

/*
 * @brief        Exposed API for WakeLock access
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    Acquire or Release wakelock
 * @return       Return  True on success otherwise returns False
 */
CDLL_EXPORT BOOL ValSimWakeLockAccess(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in BOOL bAcquireOrRelease);

/*
 * @brief        Exposed API for reading graphics mmio
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    Offset
 * @param[out]   Mmio offiset value
 * @return       Return True on success otherwise return false
 */
#ifdef __cplusplus
extern "C"
{
    BOOL ValSimReadMMIO(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, _In_ ULONG offset, _Out_ PULONG pValue);
}
#else
CDLL_EXPORT BOOL ValSimReadMMIO(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, _In_ ULONG offset, _Out_ PULONG pValue);
#endif
/*
 * @brief        Exposed API for writing graphics mmio
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    Offset
 * @param[in]    Mmio offiset value
 * @return       Return True on success otherwise return false
 */
#ifdef __cplusplus
extern "C"
{
    BOOL ValSimWriteMMIO(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, _In_ ULONG offset, _In_ ULONG value);
}
#else
CDLL_EXPORT BOOL ValSimWriteMMIO(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, _In_ ULONG offset, _In_ ULONG value);
#endif

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
                                 _In_ PVOID pOutBuffer, _In_ ULONG outBufferSize);

/*
 * @brief        Exposed API for SetBrightness3
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @param[in]    targetId of the panel
 * @param[in]    pBufferArgs holds Brightness3 buffer
 * @return       Return True on success otherwise return false
 */
CDLL_EXPORT BOOL GfxValSimSetBrightness3(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, __in UINT targetId, __in VOID *pBufferArgs);

CDLL_EXPORT BOOL GfxValSimGetDisplayNonIntrusiveData(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, PDISPLAYSTATE_NONINTRUSIVE pNonIntrusiveData);

CDLL_EXPORT BOOL GfxValSimGetDisplayIntrusiveData(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, PDISPLAYSTATE_INTRUSIVE pIntrusiveData);

CDLL_EXPORT HRESULT ValSimDpcdWrite(_In_ PGFX_ADAPTER_INFO pAdapterInfo, _In_ UINT uPort, _In_ UINT16 uOffset, _In_ UINT8 uValue);

/**
 * @brief        Internal API to handle TriggerSCDC request
 * @params[in]   Adapter info
 * @params[in]   Adapter info size
 * @params[in]   uiPortNum contains display port number
 * @params[in]   uiConnectorType contains port type for HPD - NATIVE/TC/TBT
 * @return       HRESULT. 'S_OK' indicates SUCCESS and 'S_FALSE' indicates FAILURE
 */
CDLL_EXPORT HRESULT TriggerSCDCInterrupt(__in PGFX_ADAPTER_INFO pAdapterInfo, __in UINT gfxAdapterInfoSize, UINT uiPortNum, __in DD_SPI_EVENTS eScdcFailureType);
