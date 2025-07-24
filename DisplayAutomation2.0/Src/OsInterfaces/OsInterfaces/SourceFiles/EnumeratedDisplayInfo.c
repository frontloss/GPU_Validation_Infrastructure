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

//=================================================================================================
//                                  Get Enumerated Display Info
//=================================================================================================

/*------------------------------------------------------------------------------------------------*
 *
 * @file  EnumeratedDisplayInfo.c
 * @brief This file contains Implementation of GetEnumeratedDisplayInfo() Function.
 *
 *------------------------------------------------------------------------------------------------*/

#include "../HeaderFiles/ConfigInfo.h"
#include "ToolsEscape.h"
#include "DisplayEscape.h"

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           GetEnumeratedDisplayInfo (Exposed API)
 * Description:                     This function helps to Get all connected Display Info with PortName
 * @param PENUMERATED_DISPLAYS      (_Out_ Pointer of ENUMERATED_DISPLAYS, Which carries all connected Display Info)
 * @param HRESULT                   (_Out_ Pointer of HRESULT, which carries Error code)
 * return: VOID                     (Though this function returns VOID, status will be updated through pErrorCode)
 *----------------------------------------------------------------------------------------------------------*/
VOID GetEnumeratedDisplayInfo(_Out_ PENUMERATED_DISPLAYS pEnumDisplay, _Out_ HRESULT *pErrorCode)
{

    /* Input Node to stores data from EDS (X, Y, RR and Scanline) */
    struct ADAPTERNODE *adapter_info_node = NULL;

    do
    {
        /* Check for the error parameter if it is passed properly or not,
        this check is done only for exported functions*/
        if (pEnumDisplay == NULL || pErrorCode == NULL)
        {
            *pErrorCode = DISPLAY_CONFIG_ERROR_INVALID_PARAMETER;
            ERROR_LOG("Invalid Parameter error.Null pointer passed");
            break;
        }

        /* Check for the passed struct validity*/
        if (pEnumDisplay->Size != sizeof(ENUMERATED_DISPLAYS))
        {
            *pErrorCode = DISPLAY_CONFIG_ERROR_SIZE_MISMATCH;
            ERROR_LOG("GetEnumeratedDisplayInfo size mismatch");
            break;
        }

        /* Initialize the datastrutures and variables*/
        DISPLAY_CONFIG        config = { 0 };
        CONNECTOR_PORT_TYPE   connectorPort;
        BOOLEAN               adapterStatus      = FALSE;
        ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

        *pErrorCode         = DISPLAY_CONFIG_ERROR_SUCCESS;
        pEnumDisplay->Count = 0;

        /* Get display configuration details*/
        config.size = sizeof(DISPLAY_CONFIG);
        GetDisplayConfiguration(&config);

        if (config.status != DISPLAY_CONFIG_ERROR_SUCCESS)
        {
            ERROR_LOG("Get DisplayConfiguration Failed");
            *pErrorCode = config.status;
            break;
        }

        /* Get number(s) of display present from display config structure*/
        pEnumDisplay->Count = config.numberOfDisplays;

        for (INT pathIndex = 0; pathIndex < pEnumDisplay->Count; pathIndex++)
        {
            pEnumDisplay->ConnectedDisplays[pathIndex].IsActive = config.displayPathInfo[pathIndex].isActive;
            pEnumDisplay->ConnectedDisplays[pathIndex].TargetID = UNMASK_TARGET_ID(config.displayPathInfo[pathIndex].targetId);
            memcpy(pEnumDisplay->ConnectedDisplays[pathIndex].FriendlyDeviceName, config.displayPathInfo[pathIndex].panelInfo.monitorFriendlyDeviceName, DEVICE_NAME_SIZE);
            pEnumDisplay->ConnectedDisplays[pathIndex].panelInfo = config.displayPathInfo[pathIndex].panelInfo;

            adapterInfoGdiName.adapterInfo = config.displayPathInfo[pathIndex].panelInfo.gfxAdapter;
            /* Check for Duplicate Adapter Info found */
            if (IsAdapterPresentInList(adapter_info_node, &adapterInfoGdiName) == FALSE)
            {
                // Getting AdapterID and ViewGDIDeviceName based on AdapterInfo.
                adapterStatus = GetAdapterDetails(&adapterInfoGdiName);
                if (adapterStatus == FALSE)
                {
                    ERROR_LOG("Unable to fetch AdapterId/ViewGdiDeviceName Adapter Information.");
                    *pErrorCode = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
                    break;
                }

                AddAdapterToList(&adapter_info_node, adapterInfoGdiName);
            }

            DRIVER_TYPE driverBranch = GetDriverType(adapterInfoGdiName);

            if (driverBranch == YANGRA_DRIVER)
            {
                /* Get connector type details based on the driver port information*/
                pEnumDisplay->ConnectedDisplays[pathIndex].ConnectorNPortType = MapConnectorTypeYangra(config.displayPathInfo[pathIndex].targetId);
            }
            else if (driverBranch == LEGACY_DRIVER)
            {
                /* Escape call structure */
                TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS toolEscSbInfo;

                toolEscSbInfo.ulDisplayUID = UNMASK_TARGET_ID(config.displayPathInfo[pathIndex].targetId);

                if (FALSE == LegacyQueryDisplayDetails(adapterInfoGdiName, &toolEscSbInfo))
                {
                    *pErrorCode = DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED;
                }
                pEnumDisplay->ConnectedDisplays[pathIndex].ConnectorNPortType = MapConnectorTypeLegacy(toolEscSbInfo.ePortType);
            }
            else if (driverBranch == DRIVER_UNKNOWN)
            {
                ERROR_LOG("Unknown Driver type detected");
                pEnumDisplay->ConnectedDisplays[pathIndex].ConnectorNPortType = DispNone;
            }
            else
            {
                ERROR_LOG("Driver ESC to get driver type Failed / Third Party Gfx driver.");
                *pErrorCode = DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED;
                break;
            }
        }
    } while (FALSE);

    ClearAdapterNode(adapter_info_node);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                       MapConnectorTypeYangra (Internal API)
 * Description:                 This function helps to Map given Target with its respective PortName
 * @param UINT                  (UINT Target ID of respective display)
 * return: CONNECTOR_PORT_TYPE  (Returns Enum Value of Respective PortName)
 *----------------------------------------------------------------------------------------------------------*/
CONNECTOR_PORT_TYPE MapConnectorTypeYangra(UINT targetId)
{
    /*Get the port and connector type information*/
    TARGET_ID           targetID      = { 0 };
    CONNECTOR_PORT_TYPE connectorType = DispNone;

    targetID.Value = targetId;

    /* LFP specific*/
    if (targetID.bitInfo.sinkType == DD_VOT_DISPLAYPORT_EMBEDDED)
    {
        /* Map connector based on port type*/
        switch (targetID.bitInfo.portType)
        {
        case DD_PORT_TYPE_DIGITAL_PORT_A:
            connectorType = DP_A;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_B:
            connectorType = DP_B;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_C:
            connectorType = DP_C;
            break;
        default:
            break;
        }
    }
    else if (targetID.bitInfo.sinkType == DD_VOT_HDMI) /* HDMI specific*/
    {
        switch (targetID.bitInfo.portType)
        {
        case DD_PORT_TYPE_DIGITAL_PORT_A:
            connectorType = HDMI_A;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_B:
            connectorType = HDMI_B;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_C:
            connectorType = HDMI_C;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_D:
            connectorType = HDMI_D;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_E:
            connectorType = HDMI_E;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_F:
            connectorType = HDMI_F;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_G:
            connectorType = HDMI_G;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_H:
            connectorType = HDMI_H;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_I:
            connectorType = HDMI_I;
            break;
        default:

            ERROR_LOG("Sink DD_VOT_HDMI connector type is INVALID");
            break;
        }
    }
    else if (targetID.bitInfo.sinkType == DD_VOT_DISPLAYPORT_EXTERNAL) /* DP specific*/
    {
        switch (targetID.bitInfo.portType)
        {
        case DD_PORT_TYPE_DIGITAL_PORT_A:
            connectorType = DP_A;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_B:
            connectorType = DP_B;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_C:
            connectorType = DP_C;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_D:
            connectorType = DP_D;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_E:
            connectorType = DP_E;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_F:
            connectorType = DP_F;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_G:
            connectorType = DP_G;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_H:
            connectorType = DP_H;
            break;
        case DD_PORT_TYPE_DIGITAL_PORT_I:
            connectorType = DP_I;
            break;
        case DD_PORT_TYPE_COLLAGE_PORT_0:
            connectorType = COLLAGE_0;
            break;
        default:
            ERROR_LOG("Sink DD_VOT_DISPLAYPORT_EXTERNAL connector type is INVALID");
            break;
        }
    }
    else if (targetID.bitInfo.sinkType == DD_VOT_MIPI) /* MIPI specific*/
    {
        switch (targetID.bitInfo.portType)
        {
        case DD_PORT_TYPE_DSI_PORT_0:
            connectorType = MIPI_A;
            break;
        case DD_PORT_TYPE_DSI_PORT_1:
            connectorType = MIPI_C;
            break;
        default:
            ERROR_LOG("Sink DD_VOT_MIPI connector type is INVALID");
            break;
        }
    }
    else if (targetID.bitInfo.sinkType == DD_VOT_VIRTUAL) /* Virtual Display specific*/
    {
        /* Map connector based on port type*/
        if (targetID.bitInfo.portType == DD_PORT_TYPE_VIRTUAL_PORT)
        {
            connectorType = VIRTUALDISPLAY;
        }
        else
            ERROR_LOG("Port DD_PORT_TYPE_VIRTUAL_PORT  Port type is INVALID");
    }
    else if (targetID.bitInfo.sinkType == DD_VOT_WDE) /* Writeback specific*/
    {
        /* Map connector based on port type*/
        if (targetID.bitInfo.portType == DD_PORT_TYPE_WRITEBACK_PORT)
        {
            if (targetID.bitInfo.sinkIndex)
                connectorType = WD_1;
            else
                connectorType = WD_0;
        }
        else
            ERROR_LOG("Sink DD_VOT_WDE connector type is INVALID");
    }
    else
        ERROR_LOG("Sink and ConnectorType Mapping NOT Found");
    /* Return mapping information*/
    return connectorType;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                       MapConnectorTypeLegacy (Internal API)
 * Description:                 This function helps to Map given PORT_TYPES with its respective PortName
 * @param PORT_TYPES            (ePortType from TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS Structure)
 * return: CONNECTOR_PORT_TYPE  (Returns Enum Value of Respective PortName)
 *----------------------------------------------------------------------------------------------------------*/
CONNECTOR_PORT_TYPE MapConnectorTypeLegacy(PORT_TYPES displayPort)
{
    /* Convert the port details into readable one */

    CONNECTOR_PORT_TYPE connectorType;
    switch (displayPort)
    {
    case INTDPA_PORT:
        connectorType = DP_A;
        break;
    case INTDPB_PORT:
        connectorType = DP_B;
        break;
    case INTDPC_PORT:
        connectorType = DP_C;
        break;
    case INTDPD_PORT:
        connectorType = DP_D;
        break;
    case INTDPE_PORT:
        connectorType = DP_E;
        break;
    case INTDPF_PORT:
        connectorType = DP_F;
        break;
    case INTDPG_PORT:
        connectorType = DP_G;
        break;
    case INTDPH_PORT:
        connectorType = DP_H;
        break;
    case INTDPI_PORT:
        connectorType = DP_I;
        break;
    case INTHDMIB_PORT:
    case DVOB_PORT:
        connectorType = HDMI_B;
        break;
    case INTHDMIC_PORT:
    case DVOC_PORT:
        connectorType = HDMI_C;
        break;
    case INTHDMID_PORT:
    case DVOD_PORT:
        connectorType = HDMI_D;
        break;
    case INTHDMIE_PORT:
    case DVOE_PORT:
        connectorType = HDMI_E;
        break;
    case INTHDMIF_PORT:
    case DVOF_PORT:
        connectorType = HDMI_F;
        break;
    case INTHDMIG_PORT:
    case DVOG_PORT:
        connectorType = HDMI_G;
        break;
    case INTHDMIH_PORT:
    case DVOH_PORT:
        connectorType = HDMI_H;
        break;
    case INTHDMII_PORT:
    case DVOI_PORT:
        connectorType = HDMI_I;
        break;
    case ANALOG_PORT:
        connectorType = CRT;
        break;
    case INTMIPIA_PORT:
        connectorType = MIPI_A;
        break;
    case INTMIPIC_PORT:
        connectorType = MIPI_C;
        break;
    /* considering TPV_PORT will be assigned for both virtual display & WIDI, as of now we are not considering WIDI scenario
    Need to take care of this while adding tests of WIDI*/
    case TPV_PORT:
        connectorType = VIRTUALDISPLAY;
        break;
    default:
        connectorType = DispNone;
        ERROR_LOG("Port type is None");
        break;
    }
    /* Return mapping information*/
    return connectorType;
}
