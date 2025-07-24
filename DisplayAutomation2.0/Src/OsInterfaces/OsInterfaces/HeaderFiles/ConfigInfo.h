/*=================================================================================================
;
;   Copyright (c) Intel Corporation (2000 - 2018)
;
;   INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
;   ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
;   INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
;   ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
;   MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
;   OTHER WARRANTY.  Intel disclaims all liability, including liability for
;   infringement of any proprietary rights, relating to use of the code. No license,
;   express or implied, by estoppel or otherwise, to any intellectual property
;   rights is granted herein.
;
;------------------------------------------------------------------------------------------------*/

/*------------------------------------------------------------------------------------------------*
 *
 * @file  ConfigInfo.h
 * @brief This header file contains function definition for Internal API's.
 *
 *------------------------------------------------------------------------------------------------*/

#include "DisplayConfig.h"
#include "DisplayEscape.h"
#include "DriverEscape.h"
#include "../Logger/log.h"

#pragma pack(1)

/*! Structure definition for link list node for display mode list */
typedef struct DISPLAYNODE
{
    _In_ DISPLAY_MODE        displayMode; //< Resolution details
    _In_ struct DISPLAYNODE *next;        //< Pointer to next node.
} L_DISPLAYNODE;

/*! Structure definition for link list node for AdapterInfo with ViewGDIDeviceName and AdapterId */
typedef struct ADAPTERNODE
{
    _In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName; //< Adapter Details
    _In_ struct ADAPTERNODE *  next;               //< Pointer to next adapter.
} L_ADAPTERNODE;

#pragma pack()

/**
 * @brief         Macro for Checking and Logging Error Code
 * @param[in]     API return Code
 * @return:VOID
 */
#define VERIFY_STATUS(statusCode)                     \
    {                                                 \
        if (0 != statusCode)                          \
            ERROR_LOG("StatusCode : %d", statusCode); \
    }

INT RefreshRateRoundOff(FLOAT float_rr);

DISPLAY_CONFIG_ERROR_CODE DisplayConfigErrorCode(_In_ LONG status);

BOOLEAN GetTargetTimingsFromLegacyDriver(_In_ PDISPLAY_MODE pDisplayMode, _Out_ PRR_RATIONAL_INFO pDisplayTimings);

BOOLEAN UpdateScalingInfoForModeTableYangra(_In_ PANEL_INFO *pPanelInfo, _In_ struct DISPLAYNODE *pInputDisplayNode, _Out_ struct DISPLAYNODE **pOutputDisplayNode,
                                            _Out_ PINT pNumOfDisplayModes);

BOOLEAN UpdateScalingInfoForModeTableLegacy(_In_ PANEL_INFO *pPanelInfo, _In_ struct DISPLAYNODE *pInputDisplayNode, _Out_ struct DISPLAYNODE **pOutputDisplayNode,
                                            _Out_ PINT pNumOfDisplayModes);

BOOLEAN UpdateScalingInfoForModeTable3rdParty(_Inout_ PANEL_INFO *pPanelInfo, _In_ struct DISPLAYNODE *pInputDisplayNode, _Out_ struct DISPLAYNODE **pOutputDisplayNode,
                                              _Out_ PINT pNumOfDisplayModes);

CONNECTOR_PORT_TYPE MapConnectorTypeLegacy(PORT_TYPES displayPort);

CONNECTOR_PORT_TYPE MapConnectorTypeYangra(UINT targetId);

BOOLEAN ComputeScalingData(_In_ BOOLEAN virtualModeSetAware, _In_ SCALING inputScaling, _In_ PPOINTL pSourceXY, _In_ PPOINTL pTargetXY, _Out_ PRECTL pImageRegion,
                           _Out_ DISPLAYCONFIG_SCALING *pOSScaling);

BOOLEAN UpdateGfxIndex(_Inout_ PDISPLAY_PATH_INFO pDisplayPathInfo);

VOID ClearDisplayNode(_In_ struct DISPLAYNODE *pHeadRef);

BOOLEAN AddAdapterToList(_In_ struct ADAPTERNODE **pHeadRef, _In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName);

BOOLEAN IsAdapterPresentInList(_In_ struct ADAPTERNODE *pHeadRef, _Inout_ PADAPTER_INFO_GDI_NAME pAdapterInfoGdiName);

BOOLEAN IsAdapterIDPresentInList(_In_ struct ADAPTERNODE *pHeadRef, _Inout_ PADAPTER_INFO_GDI_NAME pAdapterInfoGdiName);

VOID ClearAdapterNode(_In_ struct ADAPTERNODE *pHeadRef);
VOID PrintDisplayInfo(CHAR *pTableName, UINT32 numPathArrayElements, DISPLAYCONFIG_PATH_INFO *pPathInfoArray, UINT32 numModeInfoArrayElements,
                      DISPLAYCONFIG_MODE_INFO *pModeInfoArray);

///////////////////////////////////////////////////////////////////////////////////////////////////
BOOLEAN GetSourceIdFromPanelInfo(_Inout_ PPANEL_INFO pPanelInfo, PUINT sourceId);
BOOLEAN UpdateViewGdiDeviceName(_Inout_ PPANEL_INFO pPanelInfo, UINT sourceId);
//////////////////////////////////////////////////////////////////////////////////////////////////