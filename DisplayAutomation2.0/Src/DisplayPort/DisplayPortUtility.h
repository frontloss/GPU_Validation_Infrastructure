/*!
 * @file
 * @addtogroup CDll_DisplayPortUtility
 * \brief
 * DLL provide interfaces for MST(Multi-Stream Transport) related functionalities using directly DIVA KMD via IOCTL.
 * \remarks
 * DisplayPortUtility exposes below APIs for MST(Multi-Stream Transport) related functionalities using DIVA framework: \n
 * <ul>
 * <li> @ref  GetDLLToDivaKMDConnectionStatus		\n \copybrief GetDLLToDivaKMDConnectionStatus \n
 * <li> @ref  PlugUnplugTiledDisplay					\n \copybrief PlugUnplugTiledDisplay \n
 * <li> @ref  PlugMasterOrUnplugSlavePort			\n \copybrief PlugMasterOrUnplugSlavePort \n
 * <li> @ref  GetDisplayPortInterfaceVersion         \n \copybrief GetDisplayPortInterfaceVersion \n
 * <li> @ref  GetMSTTopologyDetails					\n \copybrief GetMSTTopologyDetails \n
 * <li> @ref  DisplayPortLoadLogger					\n \copybrief DisplayPortLoadLogger \n
 * </li>
 * </ul>
 * \todo Development is underprogress
 * \attention Donot modify this API without consent from the author
 * @author:			Diwakar C
 */

#pragma once

#include "Exports\DivaPublic.h"
#include "Exports\DivaUtilityInterface_DisplayFeature.h"
#include "Exports\DivaUtilityInterface_DisplayFeatureCommon.h"

/* User defined header(s)*/
#include "Exports\rapidxml.hpp"
#include "Exports\rapidxml_print.hpp"
#include "Exports\rapidxml_utils.hpp"
#include "..\externaldep\include\pythonlogger.h"

#define GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION 0x1
#define GVSTUB_DISPLAY_FEATURE_STATUS_FAILURE 0x00000001
#define GVSTUB_FEATURE_INFO_VERSION 0x1
#define GVSTUB_FEATURE_FAILURE 0x00000008
#define GVSTUB_FEATURE_SUCCESS 0x00000000
#define DISPLAYPORT_INTERFACE_VERSION 0x1 // Indicates DP interface version
#define OPERATION_FAILED 0                // 0 indicates DeviceIOControl call failed
#define PORT_NOT_AVAILABLE -1             // -1 indicates port not free
#define MAX_NUM_BRANCHES 15               // Indicates the Maximum nodes
#define MAX_NUM_DISPLAYS 30               // Indicates the Display nodes

#if defined DLL_EXPORT
#define EXPORT_API __declspec(dllexport)
#else
#define EXPORT_API __declspec(dllimport)
#endif

#ifndef _DEBUG
#define DLL_NAME "DisplayPortUtility.dll"
#endif

/* Enum for features*/
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

/* Structs to enable/disbale feature(s)*/
typedef struct _GVSTUB_FEATURE_INFO_ARGS
{
    GVSTUB_META_DATA stFeatureMetaData; // stValStubFeatureBasicInfo.ulServiceType as GFX_VAL_STUB_FEATURE_TYPE
    union {
        GVSTUB_DISPLAY_FEATURE_ARGS stDisplayFeatureArgs; // Access Display features like MPO/DeviceSimulation etc.
    };
} GVSTUB_FEATURE_INFO_ARGS, *PGVSTUB_FEATURE_INFO_ARGS;

/* DisplayPort Device Context*/
struct DisplayPortDevice_Context
{
    HANDLE hDivaAccess; // Handle to DIVA KMD driver
} DPDevice_Context;

/* Structure for DP1.2 Branch Nodes*/
typedef struct _BRANCH_NODE_DESC
{
    unsigned char  ucUpStrmBranchOutPort;
    unsigned char  ucThisBranchInputPort;
    float          ulMaxLinkRate;
    unsigned int   ulMaxLaneCount;
    unsigned short usTotalPBN;
    unsigned int   ulBranchReplyDelay;
    unsigned int   ulLinkAddressDelay;
    unsigned int   ulRemoteI2ReadDelay;
    unsigned int   ulRemoteI2WriteDelay;
    unsigned int   ulRemoteDPCDReadDelay;
    unsigned int   ulRemoteDPCDWriteDelay;
    unsigned int   ulEPRDelay;
    unsigned int   ulAllocatePayloadDelay;
    unsigned int   ulClearPayLoadDelay;

} BRANCH_NODE_DESC, *PBRANCH_NODE_DESC;

typedef struct _BRANCH_DATA
{
    unsigned int     uiThisIndex;
    unsigned int     uiParentBranchIndex;
    BRANCH_NODE_DESC stBranchNodeDec;

} BRANCH_DATA, *PBRANCH_DATA;

typedef struct _BRANCH_DATA_ARRAY
{
    unsigned int uiNumBranches;
    BRANCH_DATA  stBranchData[MAX_NUM_BRANCHES];

} BRANCH_DATA_ARRAY, *PBRANCH_DATA_ARRAY;

/* Structure for DP1.2 Display Nodes */
typedef struct _DISPLAY_NODE_DESC
{
    unsigned char  ucUpStrmBranchOutPort;
    unsigned char  ucThisDisplayInputPort;
    float          ulMaxLinkRate;
    unsigned int   ulMaxLaneCount;
    unsigned short usTotalPBN;
    unsigned int   ulRemoteI2ReadDelay;
    unsigned int   ulRemoteI2WriteDelay;
    unsigned int   ulRemoteDPCDReadDelay;
    unsigned int   ulRemoteDPCDWriteDelay;

} DISPLAY_NODE_DESC, *PDISPLAY_NODE_DESC;

typedef struct _DISPLAY_DATA
{
    unsigned int      ulThisIndex;
    unsigned int      ulParentDisplayIndex;
    DISPLAY_NODE_DESC stDisplayNodeDesc;

} DISPLAY_DATA, *PDISPLAY_DATA;

typedef struct _DISPLAY_DATA_ARRAY
{
    unsigned int uiDisplays;
    DISPLAY_DATA stDisplayData[MAX_NUM_DISPLAYS];

} DISPLAY_DATA_ARRAY, *PDISPLAY_DATA_ARRAY;

/* Structuer for EDID Data*/
typedef struct _EDID_ARRAY
{
    unsigned int   uiNumEdidBlocks;
    unsigned char *ucEdidBuffPtrs[MAX_NUM_DISPLAYS];

} EDID_ARRAY, *PEDID_ARRAY;

/* Structure for DPCD Data*/
typedef struct _DPCD_ARRAY
{
    unsigned int   uiNumDPCDBlocks;
    unsigned char *ucDPCDBuffPtrs[MAX_NUM_DISPLAYS];

} DPCD_ARRAY, *PDPCD_ARRAY;

/* Structure for Tiled Master and Slave Display ID*/
typedef struct _TARGET_IDS_OF_TILES
{
    ULONG uMasterDisplayID;
    ULONG uSlaveDisplayID;
} TARGET_IDS_OF_TILES, *PTARGET_IDS_OF_TILES;

extern "C"
{
    /**
     * @brief        Exposed API to verify DisplayPortUtility DLL and DIVA KMD connection status.
     *               True indicates connection b/w DLL and DIVA KMD success and False indicates Failure
     * @param[In]    VOID
     * @return       BOOL
     */
    EXPORT_API BOOL GetDLLToDivaKMDConnectionStatus();

    /**
     * @brief        Exposed API to Plug/Unplug tiled Display when system is in running or low-power sleep state
     * @params       MasterDispPlug/SlaveDispPlug: 'FALSE' indicates UnPlug and 'TRUE' indicates Plug, MasterPortId: Port id of the Master Display/tile
     *               SlavePortId: Port id of the Slave Display/tile, MasterTileEDID: EDID of the Master tile, SlaveTileEDID: EDID of the Slave tile,
     *               TileDPCD: DPCD file and lowPower: 'TRUE' indicates Plug in low state whereas FALSE' indicates Plug when System in running state
     *				TargetIDsOfTiles: Structure to be filled with MasterDisplayID and SlaveDisplayID after Tiled display is simulated.
     * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
     */
    EXPORT_API BOOL PlugUnplugTiledDisplay(BOOL masterDispPlug, BOOL slaveDispPlug, UINT masterPort, UINT slavePort, PCHAR masterTileEDID, PCHAR slaveTileEDID, PCHAR tileDPCD,
                                           BOOL lowPower, PTARGET_IDS_OF_TILES pTargetIDsOfTiles);

    /**
     * @brief        Exposed to Plug Master Por/Unplug Slave Port when system is in running or low-power sleep state
     * @params       MasterPortId: Port id of the Master Display/tile, SlavePortId: Port id of the Slave Display/tile,
     *               MasterTileEDID: EDID of the Master tile, SlaveTileEDID: EDID of the Slave tile,
     *               TileDPCD: DPCD file and lowPower: 'TRUE' indicates Plug in low state whereas FALSE' indicates Plug when System in running state,
     *				TargetIDsOfTiles: Structure having MasterDisplayID and SlaveDisplayID
     * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
     */
    EXPORT_API BOOL PlugMasterOrUnplugSlavePort(UINT uiMasterPortId, UINT uiSlavePortId, PCHAR pMasterTileEDID, PCHAR pSlaveTileEDID, PCHAR pTileDPCD, BOOL bLowPower,
                                                PTARGET_IDS_OF_TILES pTargetIDsOfTiles);

    /**
     * @brief        Exposed API for Get DisplayPortUtility DLL's Interface version
     * @param[out]   Pointer to API version
     * @return       VOID
     */
    EXPORT_API VOID GetDisplayPortInterfaceVersion(_Out_ PINT pVersion);

    /*
     * @brief        Exposed API for Get Node details from the XML
     * @param[out]   pErrorCode
     * @return       VOID
     */
    EXPORT_API VOID GetMSTTopologyDetails(_Out_ HRESULT *pErrorCode);
#ifndef _DEBUG
    /*
     * @brief        Exposed API to load logger and get its handle for usage
     * @return       True or False based on request success
     */
    EXPORT_API BOOL DisplayPortLoadLogger();
#endif
}

/* Helper functions*/
BOOL  ULT_FW_WriteDPCDList(UINT Index, UINT displayUID, UINT address, UCHAR DPCDData[], UINT size);
BOOL  ULT_FW_WriteDPCDByte(UINT Index, UINT displayUID, UINT address, UCHAR DPCDData, UINT size);
BOOL  SetDpcdData(_Inout_ PDIVA_DEV_SIM_CACHE_DPCD_DATA_ARGS pDpcpDataArgs);
BOOL  ProgramAllDPCDData(UINT displayUID, CHAR dpcdFile[]);
BOOL  ULT_FW_WriteDPCDByte(UINT Index, UINT displayUID, UINT address, UCHAR DPCDByte, UINT size);
BOOL  ULT_FW_WriteDPCDList(UINT index, UINT displayUID, UINT address, UCHAR DPCDData[], UINT size);
ULONG GetDisplayDetailsFromPort(DIVA_PORT_TYPE portType);
BOOL  EnumerateDevices(_Out_ PDIVA_ENUM_DEVICE_ARGS pEnumDeviceArgs);
BOOL  EnableDisableFramework(_Inout_ PDIVA_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS pEnableDisableFrameworkArgs);
BOOL  EnableDisableFeature(_Inout_ PDIVA_ENABLE_DISABLE_FEATURE_ARGS pEnableDisableFeatureArgs);
BOOL  RecursiveParseTopologyXML(rapidxml::xml_node<> *Branch_node, PBRANCH_DATA_ARRAY pDataArray, PDISPLAY_DATA_ARRAY pDisplayArray, unsigned int parentIndex);
BOOL  RecursiveParseDisplayXML(rapidxml::xml_node<> *BranchOrDisplay_node, PDISPLAY_DATA_ARRAY pDisplayArray, unsigned int parentIndex);
BOOL  RecursiveParseEdid(rapidxml::xml_node<> *root_node, PEDID_ARRAY pEdidArray);
BOOL  RecursiveParseDpcd(rapidxml::xml_node<> *root_node, PDPCD_ARRAY pDpcdArray);