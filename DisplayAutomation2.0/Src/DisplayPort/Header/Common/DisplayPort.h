/*!
 * @file
 * @addtogroup Dll_DisplayPortUtility
 * \brief
 * DLL provide interfaces for MST(Multi-Stream Transport) related functionalities using directly DIVA KMD via IOCTL.
 * \remarks
 * DisplayPortUtility exposes below APIs to for MST(Multi-Stream Transport) related functionalities using DIVA framework: \n
 * <ul>
 * <li> @ref  GetDLLToDivaKMDConnectionStatus		\n \copybrief GetDLLToDivaKMDConnectionStatus \n
 * <li> @ref  GetDisplayPortInterfaceVersion         \n \copybrief GetDisplayPortInterfaceVersion \n
 * </li>
 * </ul>
 * \todo Development is underprogress
 * \attention Donot modify this API without consent from the author
 * @author:			Diwakar C
 */

#pragma once

#include "targetver.h"
#include <windows.h>
#include <winioctl.h>
#include <stdio.h>
#include <stdlib.h>
#include "conio.h"

extern "C"
{
#include "..\..\externaldep\include\CommonLogger.h"
}

#define DLL_NAME "DisplayPort.dll"

#include "..\GfxValSimulator\GfxValSimDriver\DriverInterfaces\CommonIOCTL.h"
#include "..\GfxValSimulator\GfxValSimDriver\DriverInterfaces\DPIOCTL.h"

#include "Common.h"
#define m_dwVersion 1

#define GFX_0_ADPTER_INDEX L"gfx_0" // Multiadapter WA, currently display port support only default adapter.

/* Enum for features */
typedef enum _GVSTUB_FEATURE_TYPE
{
    GVSTUB_FEATURE_UNDEFINED = 0,
    GVSTUB_GENERIC_GFX_ACCESS,
    GVSTUB_THUNK_ESCAPE,
    GVSTUB_FEATURE_DISPLAY,
    GVSTUB_FEATURE_KMRENDER,
    GVSTUB_FEATURE_PWRCONS,
    GVSTUB_FEATURE_GMM,
    GVSTUB_FEATURE_PINNING,
    GVSTUB_FEATURE_MAX
} GVSTUB_FEATURE_TYPE;

/* DFT/DIVA error codes */
#define GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION 0x1
#define GVSTUB_DISPLAY_FEATURE_STATUS_FAILURE 0x00000001
#define GVSTUB_FEATURE_INFO_VERSION 0x1
#define GVSTUB_FEATURE_FAILURE 0x00000008
#define GVSTUB_FEATURE_SUCCESS 0x00000000

/* Common error codes between Simulation driver and python Scripts */
#define GFXSIM_DISPLAY_TOPOLOGIES_MATCHING 0x00000000
#define GFXSIM_DISPLAY_FAILURE 0x00000001
#define GFXSIM_DISPLAY_DISPLAYS_MISMATCH 0x00000002
#define GFXSIM_DISPLAY_BRANCHES_MISMATCH 0x00000003
#define GFXSIM_DISPLAY_TOPOLOGY_NOT_PRESENT 0x00000004

/* Port String details*/
CONST PCHAR GET_PORT_STRING[] = { "ANALOG_PORT",   "DVOA_PORT",    "DVOB_PORT",     "DVOC_PORT",   "DVOD_PORT",   "LVDS_PORT",     "INTDPE_PORT", "INTHDMIB_PORT", "INTHDMIC_PORT",
                                  "INTHDMID_PORT", "INT_DVI_PORT", "INTDPA_PORT",   "INTDPB_PORT", "INTDPC_PORT", "INTDPD_PORT",   "TPV_PORT",    "INTMIPIA_PORT", "INTMIPIC_PORT",
                                  "WIGIG_PORT",    "DVOF_PORT",    "INTHDMIF_PORT", "INTDPF_PORT", "DVOE_PORT",   "INTHDMIE_PORT", "MAX_PORTS" };

typedef struct DPDeviceContext
{
    BOOL   bGfxValSimStatus; // This flag says whether DP AUX Stub initialized or not
    HANDLE hGfxValSimHandle; // Handle to DP AUX Stub driver
} DPDeviceContext, *PDPDeviceContext;

extern DPDeviceContext stDPDevContext;

#define MAX_NUM_BRANCHES 15 // Indicates the Maximum nodes
#define MAX_NUM_DISPLAYS 30 // Indicates the Display nodes

#define DISPLAYPORT_INTERFACE_VERSION 0x1 // Indicates DP interface version
#define OPERATION_FAILED 0                // 0 indicates DeviceIOControl call failed
#define INTEL_VENDOR_ID L"8086"

#define GFX_VALSIM_VERIFY_IGFX_ADAPTER(pAdapterInfo, gfxAdapterInfoSize)                                                                           \
    {                                                                                                                                              \
        if (NULL == pAdapterInfo)                                                                                                                  \
        {                                                                                                                                          \
            TRACE_LOG(DEBUG_LOGS, "Error: GFX_ADAPTER_INFO Pointer is NULL! \n");                                                                      \
            return FALSE;                                                                                                                          \
        }                                                                                                                                          \
        if (0 != wcscmp(pAdapterInfo->vendorID, INTEL_VENDOR_ID))                                                                                  \
        {                                                                                                                                          \
            TRACE_LOG(DEBUG_LOGS, "Error: Invalid vendor id %d provided, Supported vendor id is %d !\n", pAdapterInfo->vendorID, INTEL_VENDOR_ID); \
            return FALSE;                                                                                                                          \
        }                                                                                                                                          \
        if (sizeof(GFX_ADAPTER_INFO) != gfxAdapterInfoSize)                                                                                            \
        {                                                                                                                                          \
            TRACE_LOG(DEBUG_LOGS, "Error: GFX_ADAPTER_INFO size mismatch !\n");                                                                        \
            return FALSE;                                                                                                                          \
        }                                                                                                                                          \
    }

/* Preprocessor Macros*/
#ifdef _DLL_EXPORT
#define EXPORT_API __declspec(dllexport)
#else
#define EXPORT_API __declspec(dllimport)
#endif

/**
 * @brief        Exposed API for Get DisplayPortUtility DLL's Interface version
 * @param[out]   Pointer to API version
 * @return       VOID
 */
EXPORT_API BOOL GetDisplayPortInterfaceVersion(_Out_ PINT pVersion);

/**
 * @brief        Exposed API to Initialize DP devices
 * @params       Adapter info
 * @params       Adapter info size
 * @params       DisplayportInit	: This is needed for Initializing the DP SST/MST Aux objects
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
EXPORT_API BOOL DisplayportInit(PGFX_ADAPTER_INFO pAdapterInfo, UINT gfxAdapterInfoSize, PDP_INIT_INFO pDPInfo);

/**
* @brief        Exposed API to Parse XML Files and send topology to drivers
* @params       uiPortNum	: Port Number of device
*				eTopologyType	: Topology Type
*               xmlFile		: This is needed for parsing the SST/MST data
                bIsLowPower : This is needed for enabling Plug/Unplug in low power state
* @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
*/
EXPORT_API BOOL ParseNSendTopology(UINT uiPortNum, DP_TOPOLOGY_TYPE eTopologyType, CHAR *pchXmlFile, BOOL bIsLowPower);

/**
* @brief        Exposed API to verify whether expected and applied MST topologies are identical or not
* @params       ulPortNum: Port number from where topology should be verified
* @return       UINT. Returns error code depending on the error. Error code could be SUCCESS, FAILURE, TOPOLOGIES_MATCHING,
                DISPLAYS_MISMATCH, BRANCHES_MISMATCH, TOPOLOGIES_MISMATCH or TOPOLOGY_NOT_PRESENT
*/
EXPORT_API UINT VerifyMSTTopology(ULONG ulPortNum);

/**
 * @brief        Exposed API to Read DPCD Value
 * @params       pDpcdData	 : pointer to structure GET_DPCD_ARGS contains port num and RAD
 * @params       pOutputBuffer: For sending the value of the offset requested by user
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
EXPORT_API BOOL ReadDPCD(PGET_DPCD_ARGS pDpcdData, ULONG ulOutputBuffer[]);

/**
 * @brief			Routine that calls to add/delete node/branch from the Topology
 * @params[In]       uiPortNum : Port number from where topology should be verified
 * @params[In]       pRADData : structure to get all RAD details
 * @return			BOOL. TRUE if PASS, FALSE if FAIL
 */
EXPORT_API BOOL GetMSTTopologyRAD(ULONG ulPortNum, PBRANCHDISP_RAD_ARRAY pRADData);

/**
 * @brief			Routine that calls to add/delete node/branch from the Topology
 * @params[In]   	ulPortNum : Port Number from where DPCDs should be read
 * @params[In]   	Attach/Detach details of Branch/Display passed by the user
 * @params[In]   	RAD details passed by the user
 * @params[In]   	subTopology details needed for attaching branch/display
 * @params[In]   	bIsLowPower : To indicate the system to be in low power state
 * @return			BOOL. TRUE if PASS, FALSE if FAIL
 */
EXPORT_API BOOL AddRemoveSubTopology(ULONG ulPortNum, BOOL bAttachDetach, PMST_RELATIVEADDRESS pstRAD, CHAR *pchSubTopologyXmlFile, BOOL bIsLowPower);

/**
 * @brief			Routine that calls to set target to low power state
 * @params			pPowerData : pointer to structure GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA contains number of ports, port number, plug/unplug status
 * @return			BOOL. TRUE if PASS, FALSE if FAIL
 */
EXPORT_API BOOL SetLowPowerState(PGFXS3S4_ALLPORTS_PLUGUNPLUG_DATA pPowerData);

/**
 * @brief        Exposed API to Write DPCD Value
 * @param[in]    pDpcdWriteData	  : pointer to structure GET_DPCD_ARGS contains port number and RAD
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
EXPORT_API BOOL WriteDPCD(PSET_DPCD_ARGS pDpcdWriteData);

/**
 * @brief        Exposed API to check if Collage is supported or not in the platform
 * @param[in]    None
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
EXPORT_API BOOL GetCollageInfo();

/**
 * @brief        Exposed API to check if Collage is Enabled or Disabled
 * @param[in]    None
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
EXPORT_API BOOL IsCollageEnabled();

/**
 * @brief		API to Initaizlize CUI SDK
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
EXPORT_API BOOL InitializeCUISDK();

/**
 * @breief       API to Uninitialize CUI SDK
 */
EXPORT_API BOOL UninitializeCUISDK();

/**
 * @brief        Exposed API to set the Collage Mode for the selected Displays
 * @param[in]    pstGetSystemConfigExData: Pointer to structure IGFX_SYSTEM_CONFIG_DATA_N_VIEW
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
EXPORT_API BOOL ApplyCollage(PIGFX_SYSTEM_CONFIG_DATA_N_VIEW pstGetSystemConfigExData);

/**
 * @brief        Exposed API to get all the supported Config For Ex, SD,DD CLone, Tri Clone, Tri ED, Dual Hor Collage, etc
 * @param[in]    pstConfigEx: Pointer to structure IGFX_TEST_CONFIG_EX
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
EXPORT_API BOOL GetSupportedConfig(PIGFX_TEST_CONFIG_EX pstConfigEx);

/**
 * @brief        Exposed API to get all the supported modes for the applied collage config
 * @param[in]    pstGetSystemConfigExData: Pointer to structure IGFX_SYSTEM_CONFIG_DATA_N_VIEW
 * @param[in]    uiDisplayIndex: display index
 * @param[out]   pstVideoModesListEx2: Pointer to structure IGFX_VIDEO_MODE_LIST_EX
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
EXPORT_API BOOL Collage_GetSupportedModes(PIGFX_SYSTEM_CONFIG_DATA_N_VIEW pstGetSystemConfigExData, UINT uiDisplayIndex, PIGFX_VIDEO_MODE_LIST_EX pstVideoModesListEx2);