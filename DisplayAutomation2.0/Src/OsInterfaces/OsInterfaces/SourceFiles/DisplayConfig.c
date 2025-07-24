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
//                                  Display Config Get & Set
//=================================================================================================

/*------------------------------------------------------------------------------------------------*
 *
 * @file  DisplayConfig.c
 * @brief This file contains Implementation of GetDisplayConfigInterfaceVersion, SetDisplayConfiguration
 *        GetDisplayConfiguration, GetActiveDisplayConfiguration, GetAllGfxAdapterDetails.
 *
 *------------------------------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <tchar.h>
#include "malloc.h"
#include "windows.h"
#include "DriverEscape.h"
#include "Utilities.h"
#include "../HeaderFiles/ConfigInfo.h"
#include "../Logger/ETWTestLogging.h"
#include <devguid.h> // for GUID_DEVCLASS_CDROM etc
#include <setupapi.h>
#include <initguid.h>
#include <devpkey.h>
#include <cfgmgr32.h> // for MAX_DEVICE_ID_LEN, CM_Get_Parent and CM_Get_Device_ID
#include "ToolsEscape.h"

extern char *LIBRARY_NAME = "OsInterfaces.dll";

/**---------------------------------------------------------------------------------------------------------*
 * @brief           GetDisplayConfigInterfaceVersion (Exposed API)
 * Description:     This function helps to Get Display configuration API version
 * @param PINT      (_In_ Pointer of INT to get API version)
 * return: VOID     (Returns Nothing)
 *----------------------------------------------------------------------------------------------------------*/
VOID GetDisplayConfigInterfaceVersion(_Out_ PINT pVersion)
{
    do
    {
        if (NULL == pVersion)
        {
            break;
        }
        *pVersion = (INT)DISPLAY_CONFIG_INTERFACE_VERSION;

        INFO_LOG("Display Config DLL Version : %d", *pVersion);

    } while (FALSE);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           SplitString Helper Function
 * Description      Function to tokenize Device Instance Path and assign corresponding IDs
 * @param [In]      string (pointer to WCHAR - String to be tokenized)
 * @param [In]      delimiter (const pointer to WCHAR - identifier with which tokens are generated)
 * @param [In]      buffer (2D array of WCHAR - remaining of the tokenized string is present)
 * return: VOID     None
 *----------------------------------------------------------------------------------------------------------*/
VOID SplitString(_In_ WCHAR *string, _In_ const WCHAR *delimiter, _In_ WCHAR buffer[][MAX_DEVICE_ID_LEN])
{
    WCHAR  tempstring[MAX_DEVICE_ID_LEN];
    int    index = 0;
    WCHAR *p     = 0;
    memset(tempstring, 0, sizeof(tempstring));
    memset(buffer, 0, sizeof(buffer));

    CopyWchar(tempstring, _countof(tempstring), string);
    WCHAR *token = wcstok_s(tempstring, delimiter, &p);
    while (token != NULL)
    {
        memcpy(buffer[index++], token, (wcslen(token) * sizeof(WCHAR)));
        token = wcstok_s(NULL, delimiter, &p);
    }
}

VOID PrintDisplayInfo(CHAR *pTableName, UINT32 numPathArrayElements, DISPLAYCONFIG_PATH_INFO *pPathInfoArray, UINT32 numModeInfoArrayElements,
                      DISPLAYCONFIG_MODE_INFO *pModeInfoArray)
{
    DISPCONFIG_LOG("Start of Table : %s", pTableName);
    if (numPathArrayElements != 0)
    {
        DISPCONFIG_LOG("pPathInfoArray sourceInfo:-");
        DISPCONFIG_LOG("%-6s %-13s %-13s %-13s %-13s %-13s %-11s %-14s %-11s", "Index", "lowpart", "highpart", "id", "modeInfoIdx", "cloneGroupId", "srcModeInfoIdx", "statusFlags",
                       "Flags");
        for (int p1 = 0; p1 < numPathArrayElements; p1++)
        {
            DISPCONFIG_LOG("%-6d 0x%-11X 0x%-11X 0x%-11X 0x%-11X 0x%-11X 0x%-12X 0x%-12X 0x%-11X", p1, pPathInfoArray[p1].sourceInfo.adapterId.LowPart,
                           pPathInfoArray[p1].sourceInfo.adapterId.HighPart, pPathInfoArray[p1].sourceInfo.id, pPathInfoArray[p1].sourceInfo.modeInfoIdx,
                           pPathInfoArray[p1].sourceInfo.cloneGroupId, pPathInfoArray[p1].sourceInfo.sourceModeInfoIdx, pPathInfoArray[p1].sourceInfo.statusFlags,
                           pPathInfoArray[p1].flags);
        }
        DISPCONFIG_LOG("pPathInfoArray targetInfo:-");
        DISPCONFIG_LOG("%-6s %-13s %-13s %-13s %-13s %-19s %-11s %-11s %-11s %-11s %-11s %-11s %-13s %-13s", "Index", "lowpart", "highpart", "id", "modeInfoIdx", "tgtModeInfoIdx",
                       "outputTech", "rotation", "scaling", "scanLine", "tgAvailable", "statusFlags", "RR Numerator", "RR Denominator");
        for (int p1 = 0; p1 < numPathArrayElements; p1++)
        {
            DISPCONFIG_LOG("%-6d 0x%-11X 0x%-11X 0x%-11X 0x%-11X 0x%-17X %-11lu %-11d %-11d %-11d %-11d %-11lu %-13lu %-11lu", p1, pPathInfoArray[p1].targetInfo.adapterId.LowPart,
                           pPathInfoArray[p1].targetInfo.adapterId.HighPart, pPathInfoArray[p1].targetInfo.id, pPathInfoArray[p1].targetInfo.modeInfoIdx,
                           pPathInfoArray[p1].targetInfo.targetModeInfoIdx, pPathInfoArray[p1].targetInfo.outputTechnology, pPathInfoArray[p1].targetInfo.rotation,
                           pPathInfoArray[p1].targetInfo.scaling, pPathInfoArray[p1].targetInfo.scanLineOrdering, pPathInfoArray[p1].targetInfo.targetAvailable,
                           pPathInfoArray[p1].targetInfo.statusFlags, pPathInfoArray[p1].targetInfo.refreshRate.Numerator, pPathInfoArray[p1].targetInfo.refreshRate.Denominator);
        }
        DISPCONFIG_LOG("\n");
    }
    else
    {
        DISPCONFIG_LOG("pPathInfoArray is Empty!!!");
    }
    if (numModeInfoArrayElements != 0)
    {
        DISPCONFIG_LOG("pModeInfoArray sourceMode:-");
        DISPCONFIG_LOG("%-6s %-13s %-13s %-13s %-11s %-11s %-11s %-11s %-11s %-11s", "Index", "Lowpart", "HighPart", "id", "infoType", "height", "width", "position.x",
                       "position.y", "pixelFormat");
        for (int m1 = 0; m1 < numModeInfoArrayElements; m1++)
        {
            if (pModeInfoArray[m1].infoType == DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE)
                DISPCONFIG_LOG("%-6d 0x%-11X 0x%-11X 0x%-11X %-11d %-11lu %-11lu %-11ld %-11ld %-11d", m1, pModeInfoArray[m1].adapterId.LowPart,
                               pModeInfoArray[m1].adapterId.HighPart, pModeInfoArray[m1].id, pModeInfoArray[m1].infoType, pModeInfoArray[m1].sourceMode.height,
                               pModeInfoArray[m1].sourceMode.width, pModeInfoArray[m1].sourceMode.position.x, pModeInfoArray[m1].sourceMode.position.y,
                               pModeInfoArray[m1].sourceMode.pixelFormat);
        }
        DISPCONFIG_LOG("pModeInfoArray targetMode.targetVideoSignalInfo:-");
        DISPCONFIG_LOG("%-6s %-13s %-13s %-13s %-11s %-11s %-11s %-11s %-11s %-11s %-11s %-11s %-11s %-11s %-11s %-11s", "Index", "Lowpart", "HighPart", "id", "infoType",
                       "active.cx", "active.cy", "hSyncFreq.D", "hSyncFreq.N", "pixelRate", "scanLine", "total.cx", "total.cy", "videoStd", "vSyncFreq.D", "vSyncFreq.N");
        for (int m1 = 0; m1 < numModeInfoArrayElements; m1++)
        {
            if (pModeInfoArray[m1].infoType == DISPLAYCONFIG_MODE_INFO_TYPE_TARGET)
                DISPCONFIG_LOG("%-6d 0x%-11X 0x%-11X 0x%-11X %-11d %-11lu %-11lu %-11lu %-11lu %-11llu %-11d %-11lu %-11lu %-11lu %-11lu %-11lu", m1,
                               pModeInfoArray[m1].adapterId.LowPart, pModeInfoArray[m1].adapterId.HighPart, pModeInfoArray[m1].id, pModeInfoArray[m1].infoType,
                               pModeInfoArray[m1].targetMode.targetVideoSignalInfo.activeSize.cx, pModeInfoArray[m1].targetMode.targetVideoSignalInfo.activeSize.cy,
                               pModeInfoArray[m1].targetMode.targetVideoSignalInfo.hSyncFreq.Denominator, pModeInfoArray[m1].targetMode.targetVideoSignalInfo.hSyncFreq.Numerator,
                               pModeInfoArray[m1].targetMode.targetVideoSignalInfo.pixelRate, pModeInfoArray[m1].targetMode.targetVideoSignalInfo.scanLineOrdering,
                               pModeInfoArray[m1].targetMode.targetVideoSignalInfo.totalSize.cx, pModeInfoArray[m1].targetMode.targetVideoSignalInfo.totalSize.cy,
                               pModeInfoArray[m1].targetMode.targetVideoSignalInfo.videoStandard, pModeInfoArray[m1].targetMode.targetVideoSignalInfo.vSyncFreq.Denominator,
                               pModeInfoArray[m1].targetMode.targetVideoSignalInfo.vSyncFreq.Numerator);
        }
        DISPCONFIG_LOG("pModeInfoArray targetMode.desktopImageInfo:-");
        DISPCONFIG_LOG("%-6s %-13s %-13s %-13s %-11s %-11s %-11s %-11s %-11s %-11s %-11s %-11s %-11s %-11s %-11s", "Index", "Lowpart", "HighPart", "id", "infoType",
                       "PathSrcSize.x", "PathSrcSize.y", "DesktopImgClip.L", "DesktopImgClip.R", "DesktopImgClip.T", "DesktopImgClip.B", "DesktopImgReg.L", "DesktopImgReg.R",
                       "DesktopImgReg.T", "DesktopImgReg.B");
        for (int m1 = 0; m1 < numModeInfoArrayElements; m1++)
        {
            if (pModeInfoArray[m1].infoType == DISPLAYCONFIG_MODE_INFO_TYPE_DESKTOP_IMAGE)
                DISPCONFIG_LOG("%-6d 0x%-11X 0x%-11X 0x%-11X %-11d %-11ld %-11ld %-11ld %-11ld %-11ld %-11ld %-11ld %-11ld %-11ld %-11ld", m1, pModeInfoArray[m1].adapterId.LowPart,
                               pModeInfoArray[m1].adapterId.HighPart, pModeInfoArray[m1].id, pModeInfoArray[m1].infoType, pModeInfoArray[m1].desktopImageInfo.PathSourceSize.x,
                               pModeInfoArray[m1].desktopImageInfo.PathSourceSize.y, pModeInfoArray[m1].desktopImageInfo.DesktopImageClip.left,
                               pModeInfoArray[m1].desktopImageInfo.DesktopImageClip.right, pModeInfoArray[m1].desktopImageInfo.DesktopImageClip.top,
                               pModeInfoArray[m1].desktopImageInfo.DesktopImageClip.bottom, pModeInfoArray[m1].desktopImageInfo.DesktopImageRegion.left,
                               pModeInfoArray[m1].desktopImageInfo.DesktopImageRegion.right, pModeInfoArray[m1].desktopImageInfo.DesktopImageRegion.top,
                               pModeInfoArray[m1].desktopImageInfo.DesktopImageRegion.bottom);
        }
        DISPCONFIG_LOG("\n");
    }
    DISPCONFIG_LOG("End of Table : %s", pTableName);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               CompareDisplayPathInfo (Internal Helper API)
 * Description          Helper function to check if all requested displays are present in current configuration
 * @param [IN]          getConfig (Pointer to DISPLAY_PATH_INFO structure - Current Display Path Info)
 * @param [IN]          requestedConfig (Pointer to DISPLAY_PATH_INFO structure - Requested Display Path Info)
 * @param [IN]          getConfigLength (Variable of type INT - Length of getConfig array)
 * @param [IN]          requestedConfigLength (Variable of type INT - Length of requestedConfig array)
 * return BOOLEAN       Returns TRUE if all elements of requestedConfig are present in getConfig array, FALSE otherwise
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN CompareDisplayPathInfo(_In_ DISPLAY_PATH_INFO getConfig[], _In_ DISPLAY_PATH_INFO requestedConfig[], _In_ INT getConfigLength, _In_ INT requestedConfigLength)
{
    INT pathInfoIndex1 = 0, pathInfoIndex2 = 0;

    // getConfig array is expected to contain all connected displays (including inactive ones)
    // For each requestedConfig array, check for a match in getConfig array which are active
    while (pathInfoIndex1 < getConfigLength && pathInfoIndex2 < requestedConfigLength)
    {
        // Currently few tests are not passing proper Target ID within DisplayAndAdapterInfo.
        // Adding this WA until test side issues are fixed.
        PANEL_INFO tempPanelInfo = requestedConfig[pathInfoIndex2].panelInfo;
        tempPanelInfo.targetID   = requestedConfig[pathInfoIndex2].targetId;

        // Compare if Target ID and Adapter DeviceID / DeviceInstanceID are matching for current panel
        BOOLEAN compareStatus = ComparePanelInfo(getConfig[pathInfoIndex1].panelInfo, tempPanelInfo);

        // We are not expecting requestedConfig array elements to be updated with isActive to TRUE,
        // since it is handled within SDC call for invoking the same.
        // Instead check for current element's isActive field which will be filled from QDC call.
        if (TRUE == compareStatus && TRUE == getConfig[pathInfoIndex1].isActive)
        {
            pathInfoIndex1 = 0;
            pathInfoIndex2++;
        }
        else
        {
            pathInfoIndex1++;
        }
    }

    // Note: Returns TRUE if requestedConfig array is completely traversed.
    // If all elements are found pathInfoIndex2 will become same as it's array length.
    // Hence comparing array length with current pathInfoIndex2 value
    if (pathInfoIndex2 == requestedConfigLength)
        return TRUE;

    // If any of requestedConfig elements are not found, pathInfoIndex2 will not become requestedConfigLength
    return FALSE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   SetDisplayConfiguration (Exposed API)
 * Description:             This function has Implementation for Set Display Topology either (SINGLE / CLONE / EXTENDED)
                            for given number of displays. (Tested with MAX 3 displays)
 * @param PDISPLAY_CONFIG   (_In_ Pointer to DISPLAY_CONFIG structure)
 * return: VOID             (Though function returns VOID, output structure (DISPLAY_CONFIG) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID SetDisplayConfiguration(_Inout_ PDISPLAY_CONFIG pConfig, _In_ BOOLEAN addForceModeEnumFlag)
{
    UINT                     flags;
    LONG                     status;
    UINT32                   numPathArrayElements;
    DISPLAYCONFIG_PATH_INFO *pPathInfoArray     = NULL;
    ADAPTER_INFO_GDI_NAME    adapterInfoGdiName = { 0 };
    BOOLEAN                  adapterStatus      = FALSE;
    UINT                     pollingCount       = GET_RETRY_COUNT(6 * SEC_TO_MILLI_SEC, MILLI_SEC_100);

    do
    {
        if (NULL == pConfig)
        {
            ERROR_LOG("Input Parameter pConfig(DISPLAY_CONFIG) is NULL.");
            break;
        }
        if ((pConfig->topology == SINGLE && pConfig->numberOfDisplays > 1) || ((pConfig->topology == CLONE || pConfig->topology == EXTENDED) && pConfig->numberOfDisplays <= 1))
        {
            pConfig->status = DISPLAY_CONFIG_ERROR_INVALID_PARAMETER;
            ERROR_LOG("Topology and Number_of_Displays are NOT Matching with status code %d", pConfig->status);
            break;
        }
        numPathArrayElements = pConfig->numberOfDisplays;

        /* Allocate Buffer for SetDisplayConfig */
        pPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, (sizeof(DISPLAYCONFIG_PATH_INFO)));

        if (pPathInfoArray == NULL)
        {
            pConfig->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            ERROR_LOG("PathArray and ModeArray Memory Allocation Failed with status code %d", pConfig->status);
            break;
        }

        for (UINT pathIndex = 0; pathIndex < numPathArrayElements; pathIndex++)
        {
            // Getting AdapterID and ViewGDIDeviceName based on AdapterInfo.
            adapterInfoGdiName.adapterInfo = pConfig->displayPathInfo[pathIndex].panelInfo.gfxAdapter;
            adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);
            if (adapterStatus == TRUE)
            {
                pPathInfoArray[pathIndex].flags                      = DISPLAYCONFIG_PATH_ACTIVE;
                pPathInfoArray[pathIndex].sourceInfo.adapterId       = adapterInfoGdiName.adapterID;
                pPathInfoArray[pathIndex].sourceInfo.id              = ((pConfig->topology == CLONE) ? 0 : pathIndex);
                pPathInfoArray[pathIndex].sourceInfo.modeInfoIdx     = DISPLAYCONFIG_PATH_MODE_IDX_INVALID;
                pPathInfoArray[pathIndex].targetInfo.adapterId       = adapterInfoGdiName.adapterID;
                pPathInfoArray[pathIndex].targetInfo.id              = pConfig->displayPathInfo[pathIndex].targetId;
                pPathInfoArray[pathIndex].targetInfo.modeInfoIdx     = DISPLAYCONFIG_PATH_MODE_IDX_INVALID;
                pPathInfoArray[pathIndex].targetInfo.scaling         = DISPLAYCONFIG_SCALING_PREFERRED;
                pPathInfoArray[pathIndex].targetInfo.targetAvailable = TRUE;
                if (pConfig->topology == CLONE)
                {
                    pPathInfoArray[pathIndex].sourceInfo.cloneGroupId = 1;
                }
            }
        }
        if (adapterStatus == FALSE)
        {
            pConfig->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
            ERROR_LOG("{GetAdapterDetails} for Given Adapter Information with status code %s", pConfig->status);
            break;
        }
        PrintDisplayInfo("Before SDC call", numPathArrayElements, pPathInfoArray, 0, NULL);

        /* Windows API which modifies the display topology, source, and target modes by exclusively enabling the specified paths in the current session
        We are passing mode information as NULL, OS will try to apply Mode information which are stored in CCD database
        If requested config was previously used - it will fetch from CCD data base and apply, otherwise this SDC call will fail - then we will call again SDC with Different Flag*/
        flags = SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_SAVE_TO_DATABASE;
        if (addForceModeEnumFlag == TRUE)
        {
            flags = SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_SAVE_TO_DATABASE | SDC_FORCE_MODE_ENUMERATION;
        }
        status = SetDisplayConfig(numPathArrayElements, pPathInfoArray, 0, NULL, flags);
        INFO_LOG("SDC call 1 - %ld", status);

        if (ERROR_SUCCESS != status)
        {
            // for 3rd party Adapter Extended and clone config we want to send this flags.
            flags  = SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_APPLY | SDC_SAVE_TO_DATABASE | SDC_FORCE_MODE_ENUMERATION;
            status = SetDisplayConfig(numPathArrayElements, pPathInfoArray, 0, NULL, flags);
            INFO_LOG("SDC call 2 - %ld", status);
        }

        /* We are calling SetDisplayConfig again with flag SDC_USE_SUPPLIED_DISPLAY_CONFIG.
        /* Windows API which modifies the display topology, source, and target modes by exclusively enabling the specified paths in the current session and store it in CCD database
      */
        if (ERROR_SUCCESS != status)
        {
            DEBUG_LOG("Requested Config Not available in CCD_DATABASE, Retrying with SDC_USE_SUPPLIED_DISPLAY_CONFIG flag");
            flags  = SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_ALLOW_CHANGES | SDC_SAVE_TO_DATABASE | SDC_VIRTUAL_MODE_AWARE | SDC_FORCE_MODE_ENUMERATION;
            status = SetDisplayConfig(numPathArrayElements, pPathInfoArray, 0, NULL, flags);
            INFO_LOG("SDC call 3 - %ld", status);
        }

        pConfig->status = DisplayConfigErrorCode(status);
        if (ERROR_SUCCESS != status)
        {
            ERROR_LOG("Failed to apply Config. Exited with error code %d", pConfig->status);
            break;
        }

        pConfig->status = DISPLAY_CONFIG_ERROR_VERIFICATION_FAILED;
        // Verify requested config switch with QDC call
        for (INT interval = 1; interval <= pollingCount; interval++)
        {
            DISPLAY_CONFIG getConfig = { 0 };
            getConfig.size           = sizeof(DISPLAY_CONFIG);

            GetDisplayConfiguration(&getConfig);

            if (DISPLAY_CONFIG_ERROR_SUCCESS == getConfig.status && pConfig->topology == getConfig.topology)
            {
                BOOLEAN compareStatus = CompareDisplayPathInfo(getConfig.displayPathInfo, pConfig->displayPathInfo, getConfig.numberOfDisplays, pConfig->numberOfDisplays);
                if (TRUE == compareStatus)
                {
                    pConfig->status = DISPLAY_CONFIG_ERROR_SUCCESS;
                    break;
                }
            }
            Sleep(MILLI_SEC_100); // polling interval
        }
    } while (FALSE);

    /* Cleanup Dynamic Allocated Memory */
    free(pPathInfoArray);
    EtwSetDisplayConfig(pConfig->status, pConfig->topology, pConfig->numberOfDisplays);
    for (int path = 0; path < pConfig->numberOfDisplays; path++)
    {
        int value = GetGfxIndexValue(pConfig->displayPathInfo[path].panelInfo.gfxAdapter.gfxIndex);
        EtwTargetDetails(value, pConfig->displayPathInfo[path].panelInfo.targetID, pConfig->displayPathInfo[path].isActive);
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           GetDisplayTopology (Internal API)
 * Description:                     This function has Implementation to get Topology configured between 2 paths
 * @param DISPLAYCONFIG_PATH_INFO   (_In_ Pointer to Path 1 DISPLAYCONFIG_PATH_INFO Structure)
 * @param DISPLAYCONFIG_PATH_INFO   (_In_ Pointer to Path 2 DISPLAYCONFIG_PATH_INFO Structure)
 * @param DISPLAYCONFIG_MODE_INFO   (_In_ Pointer to Mode 1 DISPLAYCONFIG_MODE_INFO Structure)
 * @param DISPLAYCONFIG_MODE_INFO   (_In_ Pointer to Mode 2 DISPLAYCONFIG_MODE_INFO Structure)
 * return: UINT                     (Topology Info: CLONE / EXTENDED / TOPOLOGY_NONE)
 *----------------------------------------------------------------------------------------------------------*/
UINT GetDisplayTopology(DISPLAYCONFIG_PATH_INFO *pPathInfo1, DISPLAYCONFIG_PATH_INFO *pPathInfo2, DISPLAYCONFIG_MODE_INFO *pModeInfo1, DISPLAYCONFIG_MODE_INFO *pModeInfo2)
{
    INT Invalid_Topology = -1;

    if (pPathInfo1->sourceInfo.id == Invalid_Topology || pPathInfo2->sourceInfo.id == Invalid_Topology)
    {
        return TOPOLOGY_NONE;
    }

    if ((pPathInfo1->sourceInfo.id == pPathInfo2->sourceInfo.id || pPathInfo1->sourceInfo.cloneGroupId == pPathInfo2->sourceInfo.cloneGroupId) &&
        (pModeInfo1->sourceMode.position.x == pModeInfo2->sourceMode.position.x && pModeInfo1->sourceMode.position.y == pModeInfo2->sourceMode.position.y))
    {
        return CLONE;
    }
    else
    {
        return EXTENDED;
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   GetDisplayConfiguration (Exposed API)
 * Description:             This function has Implementation to get display configuration of unique active and inactive displays
                            (CCD contains same panel entry duplicated for different configurations. Hence extract only unique ID's).
 * @param PDISPLAY_CONFIG   (_In_ Pointer to DISPLAY_CONFIG structure)
 * return: VOID             (Though function returns VOID, output structure (DISPLAY_CONFIG) has error status)
  Step-1    Call QDC with QDC_All_PATH Flag to Get both Active and Non Active Display
  Step-2    Fill all the connected displays to Output Structure ( Ensure there is No Duplicate Target ID getting added to Final DISPLAY_CONFIG Structure.
*----------------------------------------------------------------------------------------------------------*/
VOID GetDisplayConfiguration(_Inout_ PDISPLAY_CONFIG pConfig)
{
    LONG                             status;
    UINT                             flags;
    UINT                             targetId;
    UINT32                           numPathArrayElements     = 0;
    UINT32                           numModeInfoArrayElements = 0;
    SIZE_T                           length                   = 0;
    DISPLAYCONFIG_TARGET_DEVICE_NAME targetInfo;
    DISPLAYCONFIG_PATH_INFO *        pPathInfoArray      = NULL;
    DISPLAYCONFIG_MODE_INFO *        pModeInfoArray      = NULL;
    DISPLAY_PATH_INFO                pathInfo            = { 0 };
    BOOLEAN                          adapterStatus       = FALSE;
    ADAPTER_INFO_GDI_NAME            adapterInfoGdiName  = { 0 };
    struct ADAPTERNODE *             adapter_info_node   = NULL;
    BOOLEAN                          bAdapterInfoUpdated = FALSE;

    INT                    firstPinnedPath      = -1;
    INT                    is_clone_topology    = -1;
    INT                    is_extended_topology = -1;
    DISPLAYCONFIG_TOPOLOGY topology             = TOPOLOGY_NONE;
    BOOLEAN                is_invalid_topology  = FALSE;

    do
    {
        if (pConfig == NULL)
        {
            ERROR_LOG("Input Parameter pConfig is Null");
            break;
        }
        if (pConfig->size != sizeof(DISPLAY_CONFIG))
        {
            pConfig->status = DISPLAY_CONFIG_ERROR_INSUFFICIENT_BUFFER;
            ERROR_LOG("Input Parameter pConfig Structure Size Mismatch. Expected %d, Actual %d", (int)sizeof(DISPLAY_CONFIG), pConfig->size);
            break;
        }

        pConfig->status = DISPLAY_CONFIG_ERROR_SUCCESS;

        // Step - 1
        /* This Flag provides data about both active and inactive display path */
        flags = QDC_ALL_PATHS | QDC_VIRTUAL_MODE_AWARE;

        /* Get Path Array buffer size and Mode array buffer size through OS API. */
        status = GetDisplayConfigBufferSizes(flags, &numPathArrayElements, &numModeInfoArrayElements);

        if (status != ERROR_SUCCESS)
        {
            ERROR_LOG("Get PathArray and ModeArray Buffer Size Failed with error code %d", status);
            pConfig->status = DisplayConfigErrorCode(status);
            break;
        }

        /* Allocate Buffer for QueryDisplayConfig */
        pPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, (sizeof(DISPLAYCONFIG_PATH_INFO)));
        pModeInfoArray = (DISPLAYCONFIG_MODE_INFO *)calloc(numModeInfoArrayElements, (sizeof(DISPLAYCONFIG_MODE_INFO)));

        if (NULL == pPathInfoArray || NULL == pModeInfoArray)
        {
            ERROR_LOG("PathArray and ModeArray Memory Allocation is Null");
            pConfig->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            break;
        }

        /* Windows API which retrieves information about all possible display paths for all display devices */
        status = QueryDisplayConfig(flags, &numPathArrayElements, pPathInfoArray, &numModeInfoArrayElements, pModeInfoArray, NULL);
        PrintDisplayInfo("Get Display Configuration After QDC call", numPathArrayElements, pPathInfoArray, numModeInfoArrayElements, pModeInfoArray);

        if (ERROR_SUCCESS != status)
        {
            ERROR_LOG("QueryDisplayConfig Failed with Error Code: %d", status);
            pConfig->status = DisplayConfigErrorCode(status);
            break;
        }

        // Step - 2
        for (UINT pathIndex = 0; pathIndex < numPathArrayElements; pathIndex++)
        {
            if (pPathInfoArray[pathIndex].targetInfo.targetAvailable == FALSE) // Panel is disconnected, But DISPLAYCONFIG_TARGET_IN_USE might have set
            {
                continue;
            }

            memset(&adapterInfoGdiName, 0, sizeof(ADAPTER_INFO_GDI_NAME));
            adapterInfoGdiName.adapterID = pPathInfoArray[pathIndex].targetInfo.adapterId;
            if (IsAdapterIDPresentInList(adapter_info_node, &adapterInfoGdiName) == FALSE)
            {
                /* Get the adapterinfo for each path source id and adapter id*/
                adapterStatus = GetGfxAdapterInfo(pPathInfoArray[pathIndex].sourceInfo.id, &adapterInfoGdiName);
                if (adapterStatus == FALSE)
                {
                    ERROR_LOG("{GetGfxAdapterInfo} for given SourceId: %u and AdapterId LowPart: %lu HighPart: %d", pPathInfoArray[pathIndex].sourceInfo.id,
                              pPathInfoArray[pathIndex].targetInfo.adapterId.LowPart, pPathInfoArray[pathIndex].targetInfo.adapterId.HighPart);
                    break;
                }
                AddAdapterToList(&adapter_info_node, adapterInfoGdiName);
            }

            targetId = UNMASK_TARGET_ID(pPathInfoArray[pathIndex].targetInfo.id);

            /*Same PathArray(Display) data is duplicated in QDC PathArray Structure. Hence verifing if current PathArray is already available in pConfig */
            BOOLEAN target_found_flag = FALSE;

            for (UINT index = 0; index < pConfig->numberOfDisplays; index++)
            {
                if (targetId == pConfig->displayPathInfo[index].targetId &&
                    ((wcscmp(pConfig->displayPathInfo[index].panelInfo.gfxAdapter.busDeviceID, adapterInfoGdiName.adapterInfo.busDeviceID) == S_OK) &&
                     (wcscmp(pConfig->displayPathInfo[index].panelInfo.gfxAdapter.deviceInstanceID, adapterInfoGdiName.adapterInfo.deviceInstanceID) == S_OK)))
                {
                    target_found_flag = TRUE;

                    /* If same Target ID in DISPLAYCONFIG_PATH_INFO array has both Active and InActive elements. Will choose Active.*/
                    if (pPathInfoArray[pathIndex].targetInfo.statusFlags & DISPLAYCONFIG_TARGET_IN_USE)
                    {
                        pConfig->displayPathInfo[index].isActive = TRUE;
                    }
                    break;
                }
            }

            /*This will add connected Displays(Active and Non-Active) to pConfig List */
            if (target_found_flag == FALSE)
            {
                ZeroMemory(&targetInfo, sizeof(DISPLAYCONFIG_TARGET_DEVICE_NAME));
                targetInfo.header.size      = sizeof(DISPLAYCONFIG_TARGET_DEVICE_NAME);
                targetInfo.header.adapterId = pPathInfoArray[pathIndex].targetInfo.adapterId;
                targetInfo.header.id        = targetId;
                targetInfo.header.type      = DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_NAME;

                status = DisplayConfigGetDeviceInfo(&targetInfo.header);

                if (status == ERROR_SUCCESS)
                {
                    CopyWchar(pathInfo.panelInfo.monitorFriendlyDeviceName, (SIZE_T)DEVICE_NAME_SIZE, targetInfo.monitorFriendlyDeviceName);
                }
                else
                {
                    ERROR_LOG("DisplayConfigGetDeviceInfo Call Failed for Target ID: %u", targetId);
                }

                pathInfo.sourceId                                   = pPathInfoArray[pathIndex].sourceInfo.id;
                pathInfo.isActive                                   = (pPathInfoArray[pathIndex].targetInfo.statusFlags & DISPLAYCONFIG_TARGET_IN_USE) ? TRUE : FALSE;
                pathInfo.targetId                                   = targetId;
                pathInfo.panelInfo.gfxAdapter                       = adapterInfoGdiName.adapterInfo;
                pathInfo.panelInfo.sourceID                         = pPathInfoArray[pathIndex].sourceInfo.id;
                pathInfo.panelInfo.targetID                         = targetId;
                pathInfo.pathIndex                                  = pConfig->numberOfDisplays;
                pConfig->displayPathInfo[pConfig->numberOfDisplays] = pathInfo;
                pConfig->numberOfDisplays++;

                // Finding Topology with other paths.
                if (TRUE == pathInfo.isActive)
                {
                    if (-1 == firstPinnedPath)
                    {
                        firstPinnedPath   = pathIndex;
                        pConfig->topology = SINGLE;
                    }
                    else
                    {
                        /* path1 and path2 make all unique possible combination with given number of display path*/
                        topology = GetDisplayTopology(&pPathInfoArray[firstPinnedPath], &pPathInfoArray[pathIndex],
                                                      &pModeInfoArray[pPathInfoArray[firstPinnedPath].sourceInfo.sourceModeInfoIdx],
                                                      &pModeInfoArray[pPathInfoArray[pathIndex].sourceInfo.sourceModeInfoIdx]);

                        if (topology == CLONE)
                        {
                            is_clone_topology = TRUE;
                        }
                        else if (topology == EXTENDED)
                        {
                            is_extended_topology = TRUE;
                        }
                        else
                        {
                            is_invalid_topology = TRUE;
                        }
                    }
                } // end of Topology computation
            }     // end of connected display addition
        }

        if (is_invalid_topology == TRUE)
        {
            pConfig->topology = TOPOLOGY_NONE;
            pConfig->status   = DISPLAY_CONFIG_ERROR_BAD_CONFIGURATION;
            PrintDisplayInfo("Bad Configuration. Logging GetDisplayConfiguration()", numPathArrayElements, pPathInfoArray, numModeInfoArrayElements, pModeInfoArray);
        }
        else if (is_clone_topology == TRUE && is_extended_topology == -1)
        {
            pConfig->topology = CLONE;
        }
        else if (is_extended_topology == TRUE && is_clone_topology == -1)
        {
            pConfig->topology = EXTENDED;
        }
        else if (is_extended_topology == TRUE && is_clone_topology == TRUE)
        {
            pConfig->topology = HYBRID;
        }

        for (INT pathIndex = 0; pathIndex < pConfig->numberOfDisplays; pathIndex++)
        {
            bAdapterInfoUpdated = UpdateGfxIndex(&pConfig->displayPathInfo[pathIndex]);
            if (bAdapterInfoUpdated != TRUE)
            {
                pConfig->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
                ERROR_LOG("Get DisplayAdapter Info Failed with status code :%d", pConfig->status);
                break;
            }
        }
    } while (FALSE);

    /* Cleanup Dynamic Allocated Memory */
    free(pPathInfoArray);
    free(pModeInfoArray);
    ClearAdapterNode(adapter_info_node);
    EtwGetDisplayConfig(pConfig->status, pConfig->topology, pConfig->numberOfDisplays);
    for (int path = 0; path < pConfig->numberOfDisplays; path++)
    {
        int value = GetGfxIndexValue(pConfig->displayPathInfo[path].panelInfo.gfxAdapter.gfxIndex);
        EtwTargetDetails(value, pConfig->displayPathInfo[path].panelInfo.targetID, pConfig->displayPathInfo[path].isActive);
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           GetActiveDisplayConfiguration (Exposed API) (Used Internally in GetDisplayConfiguration and SetDisplayMode)
 * Description                      This function has Implementation to get Active Config Toplogy and
 *                                  CLONE and EXTENDED pair. This is mainly to identify HYBRID DisplayConfiguration.
 * @param PACTIVE_DISPLAY_CONFIG    (_Out_ Pointer PACTIVE_DISPLAY_CONFIG Structure)
 * return: VOID                     (Though function returns VOID, output parameter (PACTIVE_DISPLAY_CONFIG) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID GetActiveDisplayConfiguration(_Out_ PACTIVE_DISPLAY_CONFIG pDisplayConfig)
{

    INT                      is_clone_topology    = -1;
    INT                      is_extended_topology = -1;
    LONG                     status;
    DWORD                    flags;
    BOOLEAN                  is_invalid_topology = FALSE;
    DISPLAYCONFIG_TOPOLOGY   topology;
    UINT32                   numPathArrayElements     = 0;
    UINT32                   numModeInfoArrayElements = 0;
    DISPLAYCONFIG_PATH_INFO *pPathInfoArray           = NULL;
    DISPLAYCONFIG_MODE_INFO *pModeInfoArray           = NULL;
    BOOLEAN                  adapterStatus            = FALSE;
    ADAPTER_INFO_GDI_NAME    adapterInfoGdiName       = { 0 };
    struct ADAPTERNODE *     adapter_info_node        = NULL;

    do
    {
        if (pDisplayConfig == NULL)
        {
            DEBUG_LOG("Display Config Object {pConfig} is NULL");
            break;
        }
        ZeroMemory(pDisplayConfig, sizeof(ACTIVE_DISPLAY_CONFIG));

        flags = QDC_ONLY_ACTIVE_PATHS | QDC_VIRTUAL_MODE_AWARE;

        /* Get Path Array buffer size and Mode array buffer size through OS API. */
        status = GetDisplayConfigBufferSizes(flags, &numPathArrayElements, &numModeInfoArrayElements);

        if (status != ERROR_SUCCESS)
        {
            pDisplayConfig->status = DisplayConfigErrorCode(status);
            ERROR_LOG("Get PathArray and ModeArray Buffer Size Failed with status code : %d ", status);
            break;
        }

        /* Allocate Buffer for QueryDisplayConfig */
        pPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, (sizeof(DISPLAYCONFIG_PATH_INFO)));
        pModeInfoArray = (DISPLAYCONFIG_MODE_INFO *)calloc(numModeInfoArrayElements, (sizeof(DISPLAYCONFIG_MODE_INFO)));

        if (pPathInfoArray == NULL || pModeInfoArray == NULL)
        {
            pDisplayConfig->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            ERROR_LOG("PathArray and ModeArray Memory Allocation is NULL with status code :%d", pDisplayConfig->status);
            break;
        }

        /* Windows API which retrieves information about all possible display paths which is active */
        status = QueryDisplayConfig(flags, &numPathArrayElements, pPathInfoArray, &numModeInfoArrayElements, pModeInfoArray, NULL);
        PrintDisplayInfo("Get Active Display Configuration After QDC call", numPathArrayElements, pPathInfoArray, numModeInfoArrayElements, pModeInfoArray);

        if (status != ERROR_SUCCESS)
        {
            ERROR_LOG("QueryDisplayConfig Failed with Error Code: %d", status);
            break;
        }

        pDisplayConfig->size             = sizeof(ACTIVE_DISPLAY_CONFIG);
        pDisplayConfig->numberOfDisplays = numPathArrayElements;

        if (numPathArrayElements == 1)
        {
            pDisplayConfig->displayInfo[0].cloneGroupCount    = 0;
            pDisplayConfig->displayInfo[0].extendedGroupCount = 0;
            pDisplayConfig->displayInfo[0].pathIndex          = 0;
            pDisplayConfig->displayInfo[0].targetId           = UNMASK_TARGET_ID(pPathInfoArray[0].targetInfo.id);
            pDisplayConfig->displayInfo[0].sourceId           = pPathInfoArray[0].sourceInfo.id;
            // Getting adapterInformation based on SourceID and AdapterID.
            adapterInfoGdiName.adapterID = pPathInfoArray[0].targetInfo.adapterId;
            adapterStatus                = GetGfxAdapterInfo(pPathInfoArray[0].sourceInfo.id, &adapterInfoGdiName);
            if (adapterStatus == FALSE)
            {
                pDisplayConfig->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
                ERROR_LOG("{GetGfxAdapterInfo} for given SourceId: %u and AdapterId LowPart: %lu HighPart: %d", pPathInfoArray[0].sourceInfo.id,
                          pPathInfoArray[0].targetInfo.adapterId.LowPart, pPathInfoArray[0].targetInfo.adapterId.HighPart);
                break;
            }
            pDisplayConfig->displayInfo[0].panelInfo.sourceID   = pDisplayConfig->displayInfo[0].sourceId;
            pDisplayConfig->displayInfo[0].panelInfo.targetID   = pDisplayConfig->displayInfo[0].targetId;
            pDisplayConfig->displayInfo[0].panelInfo.gfxAdapter = adapterInfoGdiName.adapterInfo;
            pDisplayConfig->topology                            = SINGLE;
            pDisplayConfig->status                              = DISPLAY_CONFIG_ERROR_SUCCESS;
        }
        else
        {
            for (INT path1 = 0; path1 < numPathArrayElements; path1++)
            {
                memset(&adapterInfoGdiName, 0, sizeof(ADAPTER_INFO_GDI_NAME));
                // Fill Output Structure TargetID, SourceID and PathIndex
                pDisplayConfig->displayInfo[path1].targetId  = UNMASK_TARGET_ID(pPathInfoArray[path1].targetInfo.id);
                pDisplayConfig->displayInfo[path1].sourceId  = pPathInfoArray[path1].sourceInfo.id;
                pDisplayConfig->displayInfo[path1].pathIndex = path1;

                adapterInfoGdiName.adapterID = pPathInfoArray[path1].targetInfo.adapterId;
                if (IsAdapterIDPresentInList(adapter_info_node, &adapterInfoGdiName) == FALSE)
                {
                    /* Get the adapterinfo for each path source id and adapter id*/
                    adapterStatus = GetGfxAdapterInfo(pPathInfoArray[path1].sourceInfo.id, &adapterInfoGdiName);
                    if (adapterStatus == FALSE)
                    {
                        pDisplayConfig->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
                        ERROR_LOG("{GetGfxAdapterInfo} for given SourceId: %u and AdapterId LowPart: %lu HighPart: %d", pPathInfoArray[path1].sourceInfo.id,
                                  pPathInfoArray[path1].targetInfo.adapterId.LowPart, pPathInfoArray[path1].targetInfo.adapterId.HighPart);
                        break;
                    }
                    AddAdapterToList(&adapter_info_node, adapterInfoGdiName);
                }

                pDisplayConfig->displayInfo[path1].panelInfo.sourceID   = pDisplayConfig->displayInfo[path1].sourceId;
                pDisplayConfig->displayInfo[path1].panelInfo.targetID   = pDisplayConfig->displayInfo[path1].targetId;
                pDisplayConfig->displayInfo[path1].panelInfo.gfxAdapter = adapterInfoGdiName.adapterInfo;
                for (INT path2 = path1 + 1; path2 < numPathArrayElements; path2++)
                {
                    /* path1 and path2 make all unique possible combination with given number of display path*/
                    topology = GetDisplayTopology(&pPathInfoArray[path1], &pPathInfoArray[path2], &pModeInfoArray[pPathInfoArray[path1].sourceInfo.sourceModeInfoIdx],
                                                  &pModeInfoArray[pPathInfoArray[path2].sourceInfo.sourceModeInfoIdx]);

                    if (topology == CLONE)
                    {
                        is_clone_topology = TRUE;
                        // Path 1 Clone info
                        pDisplayConfig->displayInfo[path1].cloneGroupCount = pDisplayConfig->displayInfo[path1].cloneGroupCount + 1;
                        pDisplayConfig->displayInfo[path1].cloneGroupTargetIds[pDisplayConfig->displayInfo[path1].cloneGroupCount - 1] =
                        UNMASK_TARGET_ID(pPathInfoArray[path2].targetInfo.id);

                        // Path 2 Clone info
                        pDisplayConfig->displayInfo[path2].cloneGroupCount = pDisplayConfig->displayInfo[path2].cloneGroupCount + 1;
                        pDisplayConfig->displayInfo[path2].cloneGroupTargetIds[pDisplayConfig->displayInfo[path2].cloneGroupCount - 1] =
                        UNMASK_TARGET_ID(pPathInfoArray[path1].targetInfo.id);
                    }
                    else if (topology == EXTENDED)
                    {
                        is_extended_topology = TRUE;
                        // Path 1 Extended info
                        pDisplayConfig->displayInfo[path1].extendedGroupCount = pDisplayConfig->displayInfo[path1].extendedGroupCount + 1;
                        pDisplayConfig->displayInfo[path1].extendedGroupTargetIds[pDisplayConfig->displayInfo[path1].extendedGroupCount - 1] =
                        UNMASK_TARGET_ID(pPathInfoArray[path2].targetInfo.id);

                        // Path 2 Extended info
                        pDisplayConfig->displayInfo[path2].extendedGroupCount = pDisplayConfig->displayInfo[path2].extendedGroupCount + 1;
                        pDisplayConfig->displayInfo[path2].extendedGroupTargetIds[pDisplayConfig->displayInfo[path2].extendedGroupCount - 1] =
                        UNMASK_TARGET_ID(pPathInfoArray[path1].targetInfo.id);
                    }
                    else
                    {
                        is_invalid_topology = TRUE;
                    }
                }
            }

            if (is_invalid_topology == TRUE)
            {
                pDisplayConfig->topology = TOPOLOGY_NONE;
                pDisplayConfig->status   = DISPLAY_CONFIG_ERROR_BAD_CONFIGURATION;
            }
            else if (is_clone_topology == TRUE && is_extended_topology == -1)
            {
                pDisplayConfig->topology = CLONE;
                pDisplayConfig->status   = DISPLAY_CONFIG_ERROR_SUCCESS;
            }
            else if (is_extended_topology == TRUE && is_clone_topology == -1)
            {
                pDisplayConfig->topology = EXTENDED;
                pDisplayConfig->status   = DISPLAY_CONFIG_ERROR_SUCCESS;
            }
            else
            {
                pDisplayConfig->topology = HYBRID;
                pDisplayConfig->status   = DISPLAY_CONFIG_ERROR_SUCCESS;
            }
        }

        BOOLEAN bAdapterInfoUpdated = FALSE;
        for (INT pathIndex = 0; pathIndex < pDisplayConfig->numberOfDisplays; pathIndex++)
        {
            DISPLAY_PATH_INFO pathInfo = { 0 };
            pathInfo.panelInfo         = pDisplayConfig->displayInfo[pathIndex].panelInfo;
            pathInfo.targetId          = pDisplayConfig->displayInfo[pathIndex].targetId;
            pathInfo.sourceId          = pDisplayConfig->displayInfo[pathIndex].sourceId;
            pathInfo.pathIndex         = pDisplayConfig->displayInfo[pathIndex].pathIndex;
            bAdapterInfoUpdated        = UpdateGfxIndex(&pathInfo);
            if (bAdapterInfoUpdated != TRUE)
            {
                pDisplayConfig->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
                ERROR_LOG("Get DisplayAdapter Info Failed with status code :%d", pDisplayConfig->status);
                break;
            }
            CopyWchar(pDisplayConfig->displayInfo[pathIndex].panelInfo.gfxAdapter.gfxIndex, _countof(pDisplayConfig->displayInfo[pathIndex].panelInfo.gfxAdapter.gfxIndex),
                      pathInfo.panelInfo.gfxAdapter.gfxIndex);
        }
    } while (FALSE);

    free(pPathInfoArray);
    free(pModeInfoArray);
    ClearAdapterNode(adapter_info_node);
    EtwGetDisplayConfig(pDisplayConfig->status, pDisplayConfig->topology, pDisplayConfig->numberOfDisplays);
    for (int path = 0; path < pDisplayConfig->numberOfDisplays; path++)
    {
        int value = GetGfxIndexValue(pDisplayConfig->displayInfo[path].panelInfo.gfxAdapter.gfxIndex);
        EtwTargetDetails(value, pDisplayConfig->displayInfo[path].panelInfo.targetID, pDisplayConfig->displayInfo[path].panelInfo.gfxAdapter.isActive);
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                               DisplayConfigErrorCode (Internal API)
 * Description                          Function to translate OS error code to display Framework Error code
 * @param LONG                          (_In_ Status code reported by QueryDisplayConfig or SetDisplayConfig)
 * return: DISPLAY_CONFIG_ERROR_CODE    (Member of DISPLAY_CONFIG_ERROR_CODE Enum)
 *----------------------------------------------------------------------------------------------------------*/
DISPLAY_CONFIG_ERROR_CODE DisplayConfigErrorCode(_In_ LONG status)
{
    DISPLAY_CONFIG_ERROR_CODE errorCode = DISPLAY_CONFIG_ERROR_UNDEFINED;

    switch (status)
    {
    case ERROR_SUCCESS:
        errorCode = DISPLAY_CONFIG_ERROR_SUCCESS;
        break;
    case ERROR_INVALID_PARAMETER:
        errorCode = DISPLAY_CONFIG_ERROR_INVALID_PARAMETER;
        break;
    case ERROR_NOT_SUPPORTED:
        errorCode = DISPLAY_CONFIG_ERROR_NOT_SUPPORTED;
        break;
    case ERROR_ACCESS_DENIED:
        errorCode = DISPLAY_CONFIG_ERROR_ACCESS_DENIED;
        break;
    case ERROR_GEN_FAILURE:
        errorCode = DISPLAY_CONFIG_ERROR_GEN_FAILURE;
        break;
    case ERROR_INSUFFICIENT_BUFFER:
        errorCode = DISPLAY_CONFIG_ERROR_INSUFFICIENT_BUFFER;
        break;
    case ERROR_BAD_CONFIGURATION:
        errorCode = DISPLAY_CONFIG_ERROR_BAD_CONFIGURATION;
        break;
    default:
        errorCode = DISPLAY_CONFIG_ERROR_UNDEFINED;
        break;
    }
    return errorCode;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                       GetBDFDetails (Internal API)
 * Description                  This function returns BDF details for both Active & Non Active adapters
 * @param pAdapterDetails[Out]  (Array of BDF_INFO Structure to store adapter BDF information)
 * @param pAdapterDetails[Out]  (Object of UINT type to compute number of display adapters)
 * return: UINT                 (Error status - DISPLAY_CONFIG_ERROR_SUCCESS or DISPLAY_CONFIG_ERROR_OS_API_CALL_FAILED)
 *----------------------------------------------------------------------------------------------------------*/
UINT GetBDFDetails(_Out_ BDF_INFO bdfData[], _Out_ UINT *numDisplayAdapterOut)
{
    unsigned long   enumDeviceCount;
    DWORD           dwSize;
    DEVPROPTYPE     ulPropertyType;
    CONFIGRET       status;
    HDEVINFO        hDevInfo;
    SP_DEVINFO_DATA DeviceInfoData;
    TCHAR           adapterDevicePath[MAX_DEVICE_ID_LEN];
    WCHAR           szBuffer[4096];
    WCHAR           rawBdfBuffer[6][MAX_DEVICE_ID_LEN];
    WCHAR           tempBuffer[4][MAX_DEVICE_ID_LEN];
    int             busDeviceFunction[MAX_GFX_ADAPTER]; // Stores BDF ID by appending individual values. Used for sorting per location of device.
    WCHAR           szBDF[6];
    int             numDisplayAdapter = 0;

    // List all connected display adapters
    hDevInfo = SetupDiGetClassDevs(&GUID_DEVCLASS_DISPLAY, NULL, NULL, DIGCF_PRESENT);

    if (hDevInfo == INVALID_HANDLE_VALUE)
    {

        ERROR_LOG("INVALID_HANDLE_VALUE returned for SetupDiGetClassDevs()");
        return DISPLAY_CONFIG_ERROR_OS_API_CALL_FAILED;
    }

    for (enumDeviceCount = 0;; enumDeviceCount++)
    {
        memset(rawBdfBuffer, 0, sizeof(rawBdfBuffer));
        DeviceInfoData.cbSize = sizeof(DeviceInfoData);
        if (FALSE == SetupDiEnumDeviceInfo(hDevInfo, enumDeviceCount, &DeviceInfoData))
            break;

        status = CM_Get_Device_ID(DeviceInfoData.DevInst, adapterDevicePath, MAX_PATH, 0);
        if (status != CR_SUCCESS)
            continue;

        if (SetupDiGetDevicePropertyW(hDevInfo, &DeviceInfoData, &DEVPKEY_Device_LocationInfo, &ulPropertyType, (BYTE *)szBuffer, sizeof(szBuffer), &dwSize, 0))
        {
            ULONG devStatus, devProblemCode;
            // Step2: computing BDF(Bus, Device, Fuction) ID and store in busDeviceFunction array. Array elements is in sync with AdapterInfo in pAdapterDetails.
            // ex: PCI bus 0, device 2, function 0 => 020 => 20
            // ex: PCI bus 3, device 0, function 5 => 305 => 305
            SplitString(szBuffer, L",", rawBdfBuffer); // split by comma. Ex: "PCI bus 0, device 2, function 0"

            memset(tempBuffer, 0, sizeof(tempBuffer)); // compute pci bus value
            SplitString(rawBdfBuffer[0], L" ", tempBuffer);
            VERIFY_STATUS(CopyWchar(szBDF, _countof(szBDF), tempBuffer[2]));
            bdfData[numDisplayAdapter].bus = _wtoi(tempBuffer[2]);

            memset(tempBuffer, 0, sizeof(tempBuffer)); // compute device value
            SplitString(rawBdfBuffer[1], L" ", tempBuffer);
            VERIFY_STATUS(wcscat_s(szBDF, _countof(szBDF), tempBuffer[1]));
            bdfData[numDisplayAdapter].device = _wtoi(tempBuffer[1]);

            memset(tempBuffer, 0, sizeof(tempBuffer)); // compute function value
            SplitString(rawBdfBuffer[2], L" ", tempBuffer);
            VERIFY_STATUS(wcscat_s(szBDF, _countof(szBDF), tempBuffer[1]));
            bdfData[numDisplayAdapter].function = _wtoi(tempBuffer[1]);

            // step1: Copy adapterDevicePath to busDeviceID
            VERIFY_STATUS(CopyWchar(bdfData[numDisplayAdapter].busDeviceID, _countof(bdfData[numDisplayAdapter].busDeviceID), adapterDevicePath));

            // Step3: Compute Adapter Current status. Active/Inactive and update in adapterInfo.
            status = CM_Get_DevNode_Status(&devStatus, &devProblemCode, DeviceInfoData.DevInst, 0);
            if (status != CR_SUCCESS)
            {
                ERROR_LOG("DeviceInfoData.DevInst:%lu, status:%d", DeviceInfoData.DevInst, status);
            }
            else
            {
                if (devStatus & DN_STARTED)
                {
                    bdfData[numDisplayAdapter].isActive = TRUE;
                }
                else
                {
                    bdfData[numDisplayAdapter].isActive = FALSE;
                }
            }

            numDisplayAdapter++;
        }
    }

    *numDisplayAdapterOut = numDisplayAdapter;
    return DISPLAY_CONFIG_ERROR_SUCCESS;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                       GetRawGfxAdapterDetails (Internal API)
 * Description                  This function returns Both Active & Non Active adapters
 * @param pAdapterDetails[Out]  (POINTER to PGFX_ADAPTER_DETAILS Structure)
 * return: VOID                 (Though function returns VOID, output parameter (GFX_ADAPTER_DETAILS) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID GetRawGfxAdapterDetails(_Out_ PGFX_ADAPTER_DETAILS pAdapterDetails)
{
    UINT     adapterCount = 0;
    UINT     errorCode    = DISPLAY_CONFIG_ERROR_UNDEFINED;
    BDF_INFO busDeviceFunction[MAX_GFX_ADAPTER]; // Stores BDF ID by appending individual values. Used for sorting per location of device.
    WCHAR    currentBdf[10];
    WCHAR    nextBdf[10];
    INT      iCurrentBdf;
    INT      iNextBdf;

    if (pAdapterDetails == NULL)
    {
        DEBUG_LOG("GFX_ADAPTER_DETAILS Object {pAdapterDetails} is NULL");
        return;
    }

    // Step 1: Get BDF details from helper method
    errorCode                          = GetBDFDetails(busDeviceFunction, &adapterCount);
    pAdapterDetails->numDisplayAdapter = adapterCount;

    // Step 2: Copy AdapterInfo details
    for (int i = 0; i < pAdapterDetails->numDisplayAdapter; i++)
    {
        VERIFY_STATUS(CopyWchar(pAdapterDetails->adapterInfo[i].busDeviceID, _countof(pAdapterDetails->adapterInfo[i].busDeviceID), busDeviceFunction[i].busDeviceID));
        pAdapterDetails->adapterInfo[i].isActive = busDeviceFunction[i].isActive;
    }

    // Step 3: Swap AdapterInfo data with reference to Bus Device Function ID which was computed above in busDeviceFunction array.
    GFX_ADAPTER_INFO tempAdapterInfo = { 0 };
    BDF_INFO         temp            = { 0 };
    for (int i = 0; i < pAdapterDetails->numDisplayAdapter - 1; i++)
    {
        for (int j = 0; j < pAdapterDetails->numDisplayAdapter - i - 1; j++)
        {
            memset(currentBdf, 0, sizeof(currentBdf));
            memset(nextBdf, 0, sizeof(nextBdf));

            swprintf_s(currentBdf, sizeof(currentBdf), L"%d%d%d", busDeviceFunction[j].bus, busDeviceFunction[j].device, busDeviceFunction[j].function);
            swprintf_s(nextBdf, sizeof(nextBdf), L"%d%d%d", busDeviceFunction[j + 1].bus, busDeviceFunction[j + 1].device, busDeviceFunction[j + 1].function);

            iCurrentBdf = _wtoi(currentBdf);
            iNextBdf    = _wtoi(nextBdf);
            if (iCurrentBdf > iNextBdf)
            {
                // swap bdf object
                temp                     = busDeviceFunction[j];
                busDeviceFunction[j]     = busDeviceFunction[j + 1];
                busDeviceFunction[j + 1] = temp;

                // swap adpaterInfo correspondingly
                tempAdapterInfo                     = pAdapterDetails->adapterInfo[j];
                pAdapterDetails->adapterInfo[j]     = pAdapterDetails->adapterInfo[j + 1];
                pAdapterDetails->adapterInfo[j + 1] = tempAdapterInfo;
            }
        }
    }

    pAdapterDetails->status = errorCode;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                       GetAllGfxAdapterDetails (Exposed API)
 * Description                  Function to get all GFX adapter details.
 * @param PGFX_ADAPTER_DETAILS  (POINTER to GFX_ADAPTER_DETAILS Structure)
 * return: VOID                 (Though function returns VOID, output parameter (GFX_ADAPTER_DETAILS) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID GetAllGfxAdapterDetails(_Out_ PGFX_ADAPTER_DETAILS pAdapterDetails)
{
    /* Initialize the datastrutures and variables*/
    int   errorCode = 0;
    WCHAR szCount[MAX_GFX_ADAPTER];
    WCHAR gfx_index[] = L"gfx_";
    WCHAR pci_index[] = L"PCI\\";
    WCHAR buffer[5][MAX_DEVICE_ID_LEN];

    do
    {
        if (pAdapterDetails == NULL)
        {
            ERROR_LOG("GFX_ADAPTER_DETAILS Object {pAdapterDetails} is NULL");
            break;
        }

        ZeroMemory(pAdapterDetails, sizeof(GFX_ADAPTER_DETAILS));
        pAdapterDetails->numDisplayAdapter = 0;
        pAdapterDetails->status            = DISPLAY_CONFIG_ERROR_SUCCESS;

        // The below fn would fill raw adapter details in according to the increasing order of bus device function.
        GetRawGfxAdapterDetails(pAdapterDetails);

        if (pAdapterDetails->status != DISPLAY_CONFIG_ERROR_SUCCESS)
        {
            ERROR_LOG("Get GFX Adapter Details with status %d", pAdapterDetails->status);
            break;
        }

        for (int i = 0; i < pAdapterDetails->numDisplayAdapter; i++)
        {
            WCHAR tempVendorDeviceDetails[MAX_DEVICE_ID_LEN];
            WCHAR tempVendorID[MAX_DEVICE_ID_LEN];
            WCHAR tempDeviceID[MAX_DEVICE_ID_LEN];
            WCHAR tempBuffer[6][MAX_DEVICE_ID_LEN];
            memset(tempBuffer, 0, sizeof(tempBuffer));

            // Step 1: Split adapterDevicePath and fill adapterInfo.
            SplitString(pAdapterDetails->adapterInfo[i].busDeviceID, L"\\", tempBuffer); // Split PCI\VEN_8086&DEV_3EA0&SUBSYS_227917AA&REV_02\3&11583659&0&10

            VERIFY_STATUS(CopyWchar(pAdapterDetails->adapterInfo[i].busDeviceID, _countof(pAdapterDetails->adapterInfo[i].busDeviceID), pci_index)); // copy PCI\\

            VERIFY_STATUS(wcscat_s(pAdapterDetails->adapterInfo[i].busDeviceID, _countof(pAdapterDetails->adapterInfo[i].busDeviceID),
                                   tempBuffer[1])); // concatenate VEN_8086&DEV_3EA0&SUBSYS_227917AA&REV_02

            VERIFY_STATUS(CopyWchar(pAdapterDetails->adapterInfo[i].deviceInstanceID, _countof(pAdapterDetails->adapterInfo[i].deviceInstanceID),
                                    _wcslwr(tempBuffer[2]))); // copy 3&11583659&0&10

            VERIFY_STATUS(
            CopyWchar(tempVendorDeviceDetails, _countof(tempVendorDeviceDetails), tempBuffer[1])); // copy VEN_8086&DEV_5916&SUBSYS_079F1028&REV_02 to tempVendorDeviceDetails

            memset(tempBuffer, 0, sizeof(tempBuffer));
            SplitString(tempVendorDeviceDetails, L"&", tempBuffer);

            VERIFY_STATUS(CopyWchar(tempVendorID, _countof(tempVendorID), tempBuffer[0])); // copy VEN_8086 to tempvendorID
            VERIFY_STATUS(CopyWchar(tempDeviceID, _countof(tempDeviceID), tempBuffer[1])); // copy VEN_8086 to tempdeviceID

            memset(tempBuffer, 0, sizeof(tempBuffer));
            SplitString(tempVendorID, L"_", tempBuffer);
            VERIFY_STATUS(CopyWchar(pAdapterDetails->adapterInfo[i].vendorID, _countof(pAdapterDetails->adapterInfo[i].vendorID), tempBuffer[1])); // Set vendor ID

            memset(tempBuffer, 0, sizeof(tempBuffer));
            SplitString(tempDeviceID, L"_", tempBuffer);
            VERIFY_STATUS(CopyWchar(pAdapterDetails->adapterInfo[i].deviceID, _countof(pAdapterDetails->adapterInfo[i].deviceID), tempBuffer[1])); // Set device ID

            //--------------------------------------------------------------------------------------------------------------------------------------

            // Step2: Assign gfx_index from adapterInfo Index.
            VERIFY_STATUS(CopyWchar(pAdapterDetails->adapterInfo[i].gfxIndex, _countof(pAdapterDetails->adapterInfo[i].gfxIndex), gfx_index));

            memset(szCount, 0, sizeof(szCount));
            errorCode = swprintf_s(szCount, MAX_GFX_ADAPTER, L"%d", i);
            if (-1 == errorCode)
            {
                ERROR_LOG("Unable to write formatted data to gfx_index count string with status : %d", errorCode);
            }

            VERIFY_STATUS(wcscat_s(pAdapterDetails->adapterInfo[i].gfxIndex, _countof(pAdapterDetails->adapterInfo[i].gfxIndex), szCount));
        }

    } while (FALSE);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief							UpdateGfxIndex (Internal API)
 * Description						This function Update's GFX Index for Both Active & Non Active
 * @param PDISPLAY_PATH_INFO[InOut]	(POINTER to PDISPLAY_PATH_INFO Structure)
 * return: BOOLEAN					(BOOLEAN, TRUE on Adapter Info Update Success (Gfx Index))
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN UpdateGfxIndex(_Inout_ PDISPLAY_PATH_INFO pDisplayPathInfo)
{
    /* Initialize the AdapterFound Flag*/
    BOOLEAN             bAdapterInfoUpdated = FALSE;
    GFX_ADAPTER_DETAILS adapterDetails      = { 0 };

    do
    {
        GetAllGfxAdapterDetails(&adapterDetails);

        // Getting GFX Adapter Index for given DisplayAndAdapterInfo.
        for (INT adapterIndex = 0; adapterIndex < adapterDetails.numDisplayAdapter; adapterIndex++)
        {
            if ((S_OK == _wcsicmp(pDisplayPathInfo->panelInfo.gfxAdapter.busDeviceID, adapterDetails.adapterInfo[adapterIndex].busDeviceID)) &&
                (S_OK == _wcsicmp(pDisplayPathInfo->panelInfo.gfxAdapter.deviceInstanceID, adapterDetails.adapterInfo[adapterIndex].deviceInstanceID)))
            {
                bAdapterInfoUpdated = TRUE;
                VERIFY_STATUS(CopyWchar(pDisplayPathInfo->panelInfo.gfxAdapter.gfxIndex, _countof(pDisplayPathInfo->panelInfo.gfxAdapter.gfxIndex),
                                        adapterDetails.adapterInfo[adapterIndex].gfxIndex));
                break;
            }
        }
    } while (FALSE);
    return bAdapterInfoUpdated;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                       AddModeToList (Internal API)
 * Description:                 Function to add requested mode to link list.
 * @param ADAPTERNODE           (_In_ pHeadRef) - Double pointer to ADAPTERNODE structure.
 * @param ADAPTER_INFO_GDI_NAME (_In_ adapterInfoGdiName) - InternalAdapterInfo information need to be added to list.
 * return: BOOLEAN              (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN AddAdapterToList(_In_ struct ADAPTERNODE **pHeadRef, _In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName)
{
    struct ADAPTERNODE *new_node = (struct ADAPTERNODE *)malloc(sizeof(struct ADAPTERNODE));
    NULL_PTR_CHECK(new_node);

    memset(&new_node->adapterInfoGdiName, 0, sizeof(ADAPTER_INFO_GDI_NAME));

    new_node->adapterInfoGdiName = adapterInfoGdiName;
    new_node->next               = (*pHeadRef);
    (*pHeadRef)                  = new_node;
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           IsAdapterPresentInList (Internal API)
 * Description:                     Function to verify requested GFX_ADAPTER_INFO is present in INTERNAL_ADAPTER_INFO link list.
 * @param ADAPTERNODE               (_Inout_ Pointer to ADAPTERNODE structure.)
 * @param PADAPTER_INFO_GDI_NAME    (_In_ GfxAdapterinfo information need to be verfied with the list.)
 * return: BOOLEAN                  (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN IsAdapterPresentInList(_In_ struct ADAPTERNODE *pHeadRef, _Inout_ PADAPTER_INFO_GDI_NAME pAdapterInfoGdiName)
{
    BOOLEAN status = FALSE;
    if (NULL == pHeadRef)
        return FALSE;
    while (pHeadRef != NULL)
    {
        if ((wcscmp(pAdapterInfoGdiName->adapterInfo.busDeviceID, pHeadRef->adapterInfoGdiName.adapterInfo.busDeviceID) == S_OK) &&
            wcscmp(pAdapterInfoGdiName->adapterInfo.deviceInstanceID, pHeadRef->adapterInfoGdiName.adapterInfo.deviceInstanceID) == S_OK)
        {
            status               = TRUE;
            *pAdapterInfoGdiName = pHeadRef->adapterInfoGdiName;
            break;
        }
        pHeadRef = pHeadRef->next;
    }
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           IsAdapterIDPresentInList (Internal API)
 * Description:                     Function to verify requested INTERNAL_ADAPTER_INFO AdapterID is present in INTERNAL_ADAPTER_INFO link list.
 * @param ADAPTERNODE               (_Inout_ Pointer to ADAPTERNODE structure.)
 * @param PADAPTER_INFO_GDI_NAME    (_In_ AdapterID information need to be verfied with the list.)
 * return: BOOLEAN                  (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN IsAdapterIDPresentInList(_In_ struct ADAPTERNODE *pHeadRef, _Inout_ PADAPTER_INFO_GDI_NAME pAdapterInfoGdiName)
{
    BOOLEAN status = FALSE;
    if (NULL == pHeadRef)
        return FALSE;
    while (pHeadRef != NULL)
    {
        if (pAdapterInfoGdiName->adapterID.HighPart == pHeadRef->adapterInfoGdiName.adapterID.HighPart &&
            pAdapterInfoGdiName->adapterID.LowPart == pHeadRef->adapterInfoGdiName.adapterID.LowPart)
        {
            status               = TRUE;
            *pAdapterInfoGdiName = pHeadRef->adapterInfoGdiName;
            break;
        }
        pHeadRef = pHeadRef->next;
    }
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                       ClearAdapterNode (Internal API)
 * Description:                 Function to clear all data from INTERNAL_ADAPTER_INFO Link list.
 * @param ADAPTERNODE           (_In_ Pointer to ADAPTERNODE structure.)
 * return: VOID                 (Returns Nothing)
 *----------------------------------------------------------------------------------------------------------*/
VOID ClearAdapterNode(_In_ struct ADAPTERNODE *pHeadRef)
{
    while (pHeadRef != NULL)
    {
        struct ADAPTERNODE *temp = pHeadRef;
        memset(temp, 0, sizeof(ADAPTER_INFO_GDI_NAME));
        pHeadRef = pHeadRef->next;
        free(temp);
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               ConfigureHDR (Exposed API)
 * Description          This function has implementation to Configure OS aware way of HDR feature on the display
 * @param[In]           pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]           isEnable (BOOLEAN - To enable or disable HDR based on this flag)
 * @return LONG         Returns enable status code
 *-----------------------------------------------------------------------------------------------------------*/

LONG ConfigureHDR(_In_ PANEL_INFO *pPanelInfo, _In_ BOOLEAN isEnable)
{
    LONG                                   statusHDR;
    DISPLAYCONFIG_SET_ADVANCED_COLOR_STATE advancedColorState;
    ZeroMemory(&advancedColorState, sizeof(DISPLAYCONFIG_SET_ADVANCED_COLOR_STATE));

    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    adapterInfoGdiName.adapterInfo           = pPanelInfo->gfxAdapter;
    if (FALSE == GetAdapterDetails(&adapterInfoGdiName))
    {
        ERROR_LOG("Failed to Get Adapter GdiDeviceName!");
        return DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
    }
    advancedColorState.header.adapterId    = adapterInfoGdiName.adapterID;
    advancedColorState.header.id           = pPanelInfo->targetID; // target_id
    advancedColorState.header.size         = sizeof(advancedColorState);
    advancedColorState.header.type         = DISPLAYCONFIG_DEVICE_INFO_SET_ADVANCED_COLOR_STATE;
    advancedColorState.enableAdvancedColor = isEnable;
    statusHDR                              = DisplayConfigSetDeviceInfo(&advancedColorState.header);
    return statusHDR;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

BOOLEAN UpdateTopology(_Inout_ PDISPLAY_CONFIG pConfig)
{
    BOOLEAN                bStatus             = TRUE;
    INT                    isCloneTopology     = -1;
    INT                    isExtendedTopology  = -1;
    INT                    activeDisplaysCount = 0;
    DISPLAYCONFIG_TOPOLOGY topology            = TOPOLOGY_NONE;
    BOOLEAN                isInvalidTopology   = FALSE;

    do
    {
        for (INT pathIndex = 0; pathIndex < pConfig->numberOfDisplays; pathIndex++)
        {
            if (TRUE == pConfig->displayPathInfo[pathIndex].isActive)
                activeDisplaysCount++;
        }

        if (activeDisplaysCount == 1)
        {
            topology = SINGLE;
            break;
        }

        for (INT path1Index = 0; path1Index < pConfig->numberOfDisplays; path1Index++)
        {
            if (FALSE == pConfig->displayPathInfo[path1Index].isActive)
            {
                continue; // Path is not active. Topology computation not required.
            }
            DISPLAYCONFIG_PATH_SOURCE_INFO path1SourceInfo = pConfig->displayPathInfo[path1Index].osTopologyInfo.pathInfo.sourceInfo;
            DISPLAYCONFIG_SOURCE_MODE      path1SourceMode = pConfig->displayPathInfo[path1Index].osTopologyInfo.sourceModeInfo;

            // Finding Topology mapping with other paths.
            for (INT path2Index = 0; path2Index < pConfig->numberOfDisplays; path2Index++)
            {
                if (FALSE == pConfig->displayPathInfo[path2Index].isActive || path1Index == path2Index)
                {
                    continue;
                }

                DISPLAYCONFIG_PATH_SOURCE_INFO path2SourceInfo = pConfig->displayPathInfo[path2Index].osTopologyInfo.pathInfo.sourceInfo;
                DISPLAYCONFIG_SOURCE_MODE      path2SourceMode = pConfig->displayPathInfo[path2Index].osTopologyInfo.sourceModeInfo;

                if (path1SourceInfo.id == -1 || path2SourceInfo.id == -1) // checkout the default values from msdn???
                {
                    isInvalidTopology = TRUE;
                    continue;
                }

                /* path1 and path2 make all unique possible combination with given number of display path*/
                if ((path1SourceInfo.id == path2SourceInfo.id || path1SourceInfo.cloneGroupId == path2SourceInfo.cloneGroupId) &&
                    (path1SourceMode.position.x == path2SourceMode.position.x && path1SourceMode.position.y == path2SourceMode.position.y))
                {
                    isCloneTopology                                                                                              = TRUE;
                    pConfig->displayPathInfo[path1Index].cloneGroupPathIds[pConfig->displayPathInfo[path1Index].cloneGroupCount] = path2Index;
                    pConfig->displayPathInfo[path1Index].cloneGroupCount++;
                }
                else if (path1SourceMode.position.x + path1SourceMode.width == path2SourceMode.position.x && path1SourceMode.position.y == path2SourceMode.position.y)
                {
                    pConfig->displayPathInfo[path1Index].extendedGroupPathIds[pConfig->displayPathInfo[path1Index].extendedGroupCount] = path2Index;
                    pConfig->displayPathInfo[path1Index].extendedGroupCount++;
                    isExtendedTopology = TRUE;
                }
            } // end of Topology computation
        }

        if (isInvalidTopology == TRUE)
        {
            bStatus  = FALSE;
            topology = TOPOLOGY_NONE;
        }
        else if (isCloneTopology == TRUE && isExtendedTopology == -1)
        {
            topology = CLONE;
        }
        else if (isExtendedTopology == TRUE && isCloneTopology == -1)
        {
            topology = EXTENDED;
        }
        else if (isExtendedTopology == TRUE && isCloneTopology == TRUE)
        {
            topology = HYBRID;
        }
    } while (FALSE);

    pConfig->topology = topology;

    return bStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief							UpdateGfxAdapterIndex (Internal API)
 * Description						This function Update's GFX Index for passed Adapter
 * @param pGfxAdapter[InOut]      (POINTER to GFX_ADAPTER_INFO Structure)
 * return: BOOLEAN					(BOOLEAN, TRUE on Adapter Info Update Success (Gfx Index))
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN UpdateGfxAdapterIndex(_Inout_ PGFX_ADAPTER_INFO pGfxAdapter)
{
    /* Initialize the AdapterFound Flag*/
    BOOLEAN             bAdapterInfoUpdated = FALSE;
    GFX_ADAPTER_DETAILS adapterDetails      = { 0 };

    do
    {
        GetAllGfxAdapterDetails(&adapterDetails);

        // Getting GFX Adapter Index for given DisplayAndAdapterInfo.
        for (INT adapterIndex = 0; adapterIndex < adapterDetails.numDisplayAdapter; adapterIndex++)
        {
            if ((S_OK == _wcsicmp(pGfxAdapter->busDeviceID, adapterDetails.adapterInfo[adapterIndex].busDeviceID)) &&
                (S_OK == _wcsicmp(pGfxAdapter->deviceInstanceID, adapterDetails.adapterInfo[adapterIndex].deviceInstanceID)))
            {
                bAdapterInfoUpdated = TRUE;
                VERIFY_STATUS(CopyWchar(pGfxAdapter->gfxIndex, _countof(pGfxAdapter->gfxIndex), adapterDetails.adapterInfo[adapterIndex].gfxIndex));
                break;
            }
        }

    } while (FALSE);

    if (bAdapterInfoUpdated == FALSE)
    {
        ERROR_LOG("Failed to update GfxAdapterIndex for :%ls", pGfxAdapter->busDeviceID);
    }

    return bAdapterInfoUpdated;
}

BOOLEAN UpdateViewGdiDeviceName(_Inout_ PPANEL_INFO pPanelInfo, UINT sourceId)
{
    BOOLEAN                          status = FALSE;
    DISPLAYCONFIG_SOURCE_DEVICE_NAME deviceInfo; // This initialize is used for to find Source Device Name (Ex: \\.\DISPLAY1)

    do
    {
        if (pPanelInfo == NULL)
        {
            ERROR_LOG("pPanelInfo is NULL.");
            break;
        }

        // Initialize deviceInfo Header to find Source Device Name (Which is required for getting Handle in Driver ESC)
        ZeroMemory(&deviceInfo, sizeof(DISPLAYCONFIG_SOURCE_DEVICE_NAME));
        deviceInfo.header.size      = sizeof(DISPLAYCONFIG_SOURCE_DEVICE_NAME);
        deviceInfo.header.type      = DISPLAYCONFIG_DEVICE_INFO_GET_SOURCE_NAME;
        deviceInfo.header.id        = sourceId;
        deviceInfo.header.adapterId = pPanelInfo->gfxAdapter.adapterLUID;

        status = DisplayConfigGetDeviceInfo(&deviceInfo.header);

        if (status == ERROR_SUCCESS)
        {
            CopyWchar(pPanelInfo->viewGdiDeviceName, (SIZE_T)DEVICE_NAME_SIZE, deviceInfo.viewGdiDeviceName);
            status = TRUE;
        }
        else
        {
            ERROR_LOG("DisplayConfigGetDeviceInfo Call Failed for Source ID: %u", sourceId);
        }
    } while (FALSE);

    return status;
}

LONG UpdateMonitorFriendlyName(_Inout_ PPANEL_INFO pPanelInfo)
{
    LONG                             status = 0;
    DISPLAYCONFIG_TARGET_DEVICE_NAME targetInfo;

    do
    {
        if (pPanelInfo == NULL)
        {
            ERROR_LOG("pPanelInfo is NULL.");
            break;
        }

        ZeroMemory(&targetInfo, sizeof(DISPLAYCONFIG_TARGET_DEVICE_NAME));
        targetInfo.header.size      = sizeof(DISPLAYCONFIG_TARGET_DEVICE_NAME);
        targetInfo.header.adapterId = pPanelInfo->gfxAdapter.adapterLUID;
        targetInfo.header.id        = pPanelInfo->targetID;
        targetInfo.header.type      = DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_NAME;

        status = DisplayConfigGetDeviceInfo(&targetInfo.header);

        if (status == ERROR_SUCCESS)
        {
            CopyWchar(pPanelInfo->monitorFriendlyDeviceName, (SIZE_T)DEVICE_NAME_SIZE, targetInfo.monitorFriendlyDeviceName);
        }
        else
        {
            ERROR_LOG("DisplayConfigGetDeviceInfo Call Failed for Target ID: %u", pPanelInfo->targetID);
        }
    } while (FALSE);

    return status;
}

BOOLEAN UpdateConnectorPortType(_Inout_ PPANEL_INFO pPanelInfo)
{
    BOOLEAN status                 = FALSE;
    pPanelInfo->ConnectorNPortType = DispNone;
    DISPLAYCONFIG_TARGET_DEVICE_NAME targetInfo;

    do
    {
        if (pPanelInfo == NULL)
        {
            ERROR_LOG("pPanelInfo is NULL.");
            break;
        }

        if (pPanelInfo->driverBranch == YANGRA_DRIVER)
        {
            /* Get connector type details based on the driver port information*/
            pPanelInfo->ConnectorNPortType = MapConnectorTypeYangra(pPanelInfo->targetID);
            status                         = TRUE;
        }
        else if (pPanelInfo->driverBranch == LEGACY_DRIVER)
        {
            /* Escape call structure */
            TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS toolEscSbInfo;
            ADAPTER_INFO_GDI_NAME               adapterInfoGdiName = { 0 };

            adapterInfoGdiName.adapterID   = pPanelInfo->gfxAdapter.adapterLUID;
            adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
            toolEscSbInfo.ulDisplayUID     = pPanelInfo->targetID;

            if (FALSE == LegacyQueryDisplayDetails(adapterInfoGdiName, &toolEscSbInfo))
            {
                ERROR_LOG("Failed: LegacyQueryDisplayDetails()");
            }
            {
                pPanelInfo->ConnectorNPortType = MapConnectorTypeLegacy(toolEscSbInfo.ePortType);
                status                         = TRUE;
            }
        }
        else
        {
            ERROR_LOG("Failed to get connector port type for Third Party Gfx driver.");
        }

    } while (FALSE);

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                       GetOSPrefferedMode (Exposed API)
 * Description:                 This function is used to get Preffered Mode from OS for given Target ID.
 * @param PPANEL_INFO           (_In_   PPANEL_INFO Target ID and Adapter Information of the Respective Display)
 * @param PDISPLAY_TIMINGS      (_Out_  Output DISPLAY_TIMINGS Structure)
 * return: BOOLEAN              Returns True if it is Success else False.
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN UpdateMonitorPrefferedMode(_Inout_ PPANEL_INFO pPanelInfo)
{
    BOOLEAN                             retStatus = FALSE;
    LONG                                status    = 0;
    ULONGLONG                           mod_target_id;
    DISPLAYCONFIG_TARGET_PREFERRED_MODE preferredmodeInfo;
    BOOLEAN                             adapterStatus = FALSE;
    PDISPLAY_TIMINGS                    pDisplayTimings;

    do
    {
        pDisplayTimings = &pPanelInfo->osPreferredMode;

        ZeroMemory(&preferredmodeInfo, sizeof(DISPLAYCONFIG_TARGET_PREFERRED_MODE));
        preferredmodeInfo.header.size      = sizeof(DISPLAYCONFIG_TARGET_PREFERRED_MODE);
        preferredmodeInfo.header.id        = pPanelInfo->targetID;
        preferredmodeInfo.header.adapterId = pPanelInfo->gfxAdapter.adapterLUID;
        preferredmodeInfo.header.type      = DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_PREFERRED_MODE;

        status = DisplayConfigGetDeviceInfo(&preferredmodeInfo.header);
        if (status == ERROR_SUCCESS)
        {
            pDisplayTimings->targetId         = pPanelInfo->targetID;
            pDisplayTimings->hActive          = preferredmodeInfo.width;
            pDisplayTimings->hSyncNumerator   = preferredmodeInfo.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator;
            pDisplayTimings->hSyncDenominator = preferredmodeInfo.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator;

            pDisplayTimings->vActive          = preferredmodeInfo.height;
            pDisplayTimings->vSyncNumerator   = preferredmodeInfo.targetMode.targetVideoSignalInfo.vSyncFreq.Numerator;
            pDisplayTimings->vSyncDenominator = preferredmodeInfo.targetMode.targetVideoSignalInfo.vSyncFreq.Denominator;

            pDisplayTimings->hTotal = preferredmodeInfo.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator;
            pDisplayTimings->vTotal = (preferredmodeInfo.targetMode.targetVideoSignalInfo.vSyncFreq.Denominator / pDisplayTimings->hTotal);

            pDisplayTimings->targetPixelRate  = preferredmodeInfo.targetMode.targetVideoSignalInfo.pixelRate;
            pDisplayTimings->isPrefferedMode  = TRUE;
            pDisplayTimings->scanLineOrdering = preferredmodeInfo.targetMode.targetVideoSignalInfo.scanLineOrdering;

            float rr                     = (FLOAT)pDisplayTimings->vSyncNumerator / pDisplayTimings->vSyncDenominator;
            pDisplayTimings->refreshRate = RefreshRateRoundOff(rr);
            DEBUG_LOG("Target 0x{%X}, Active: {%lu}x{%lu}, Total: {%lu}x{%lu}, Computed RR: %f, Rounded RR: %lu", pPanelInfo->targetID, pDisplayTimings->hActive,
                      pDisplayTimings->vActive, pDisplayTimings->hTotal, pDisplayTimings->vTotal, rr, pDisplayTimings->refreshRate);

            pDisplayTimings->status = DISPLAY_CONFIG_ERROR_SUCCESS;
            retStatus               = TRUE;
        }
        else
        {
            ERROR_LOG("Get Preffered Mode failed with Error Code: %d", status);
            break;
        }
        break;
    } while (FALSE);

    return retStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   GetConfig (Exposed API)
 * Description:             This function has Implementation to get display configuration of unique active and inactive displays
                            (CCD contains same panel entry duplicated for different configurations. Hence extract only unique ID's).
 * @param PDISPLAY_CONFIG   (_In_ Pointer to DISPLAY_CONFIG structure)
 * return: VOID             (Though function returns VOID, output structure (OS_CONFIG) has error status)
  Step-1    Call QDC with QDC_All_PATH Flag to Get both Active and Non Active Display
  Step-2    Fill all the connected displays to Output Structure ( Ensure there is No Duplicate Target ID getting added to Final OS_CONFIG Structure.
*----------------------------------------------------------------------------------------------------------*/
VOID GetConfig(_Out_ PDISPLAY_CONFIG pConfig)
{
    LONG                     status;
    UINT                     flags;
    UINT                     targetId;
    UINT32                   numPathArrayElements     = 0;
    UINT32                   numModeInfoArrayElements = 0;
    DISPLAYCONFIG_PATH_INFO *pPathInfoArray           = NULL;
    DISPLAYCONFIG_MODE_INFO *pModeInfoArray           = NULL;
    DISPLAY_PATH_INFO        pathInfo                 = { 0 };
    BOOLEAN                  adapterStatus            = FALSE;
    ADAPTER_INFO_GDI_NAME    adapterInfoGdiName       = { 0 };
    struct ADAPTERNODE *     adapter_info_node        = NULL;

    do
    {
        if (pConfig == NULL)
        {
            ERROR_LOG("Input Parameter pConfig is Null");
            break;
        }
        if (pConfig->size != sizeof(DISPLAY_CONFIG))
        {
            pConfig->status = DISPLAY_CONFIG_ERROR_INSUFFICIENT_BUFFER;
            ERROR_LOG("Input Parameter pConfig Structure Size Mismatch. Expected %d, Actual %d", (int)sizeof(DISPLAY_CONFIG), pConfig->size);
            break;
        }

        pConfig->status = DISPLAY_CONFIG_ERROR_SUCCESS;

        // Step - 1
        /* This Flag provides data about both active and inactive display path */
        flags = QDC_ALL_PATHS | QDC_VIRTUAL_MODE_AWARE;

        /* Get Path Array buffer size and Mode array buffer size through OS API. */
        status = GetDisplayConfigBufferSizes(flags, &numPathArrayElements, &numModeInfoArrayElements);

        if (status != ERROR_SUCCESS)
        {
            ERROR_LOG("Get PathArray and ModeArray Buffer Size Failed with error code %d", status);
            pConfig->status = DisplayConfigErrorCode(status);
            break;
        }

        /* Allocate Buffer for QueryDisplayConfig */
        pPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, (sizeof(DISPLAYCONFIG_PATH_INFO)));
        pModeInfoArray = (DISPLAYCONFIG_MODE_INFO *)calloc(numModeInfoArrayElements, (sizeof(DISPLAYCONFIG_MODE_INFO)));

        if (NULL == pPathInfoArray || NULL == pModeInfoArray)
        {
            ERROR_LOG("PathArray and ModeArray Memory Allocation is Null");
            pConfig->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            break;
        }

        /* Windows API which retrieves information about all possible display paths for all display devices */
        status = QueryDisplayConfig(flags, &numPathArrayElements, pPathInfoArray, &numModeInfoArrayElements, pModeInfoArray, NULL);
        PrintDisplayInfo("Get Display Configuration After QDC call", numPathArrayElements, pPathInfoArray, numModeInfoArrayElements, pModeInfoArray);

        if (ERROR_SUCCESS != status)
        {
            ERROR_LOG("QueryDisplayConfig Failed with Error Code: %d", status);
            pConfig->status = DisplayConfigErrorCode(status);
            break;
        }

        // Step - 2
        for (UINT pathIndex = 0; pathIndex < numPathArrayElements; pathIndex++)
        {
            if (pPathInfoArray[pathIndex].targetInfo.targetAvailable == FALSE) // Panel is disconnected, But DISPLAYCONFIG_TARGET_IN_USE might have set
            {
                continue;
            }

            memset(&adapterInfoGdiName, 0, sizeof(ADAPTER_INFO_GDI_NAME));
            adapterInfoGdiName.adapterID = pPathInfoArray[pathIndex].targetInfo.adapterId;
            if (IsAdapterIDPresentInList(adapter_info_node, &adapterInfoGdiName) == FALSE)
            {
                /* Get the adapterinfo for each path source id and adapter id*/
                adapterStatus = GetGfxAdapterInfo(pPathInfoArray[pathIndex].sourceInfo.id, &adapterInfoGdiName);
                if (adapterStatus == FALSE)
                {
                    ERROR_LOG("{GetGfxAdapterInfo} for given SourceId: %u and AdapterId LowPart: %lu HighPart: %d", pPathInfoArray[pathIndex].sourceInfo.id,
                              pPathInfoArray[pathIndex].targetInfo.adapterId.LowPart, pPathInfoArray[pathIndex].targetInfo.adapterId.HighPart);
                    break;
                }

                UpdateGfxAdapterIndex(&adapterInfoGdiName.adapterInfo);
                AddAdapterToList(&adapter_info_node, adapterInfoGdiName);
            }

            targetId = UNMASK_TARGET_ID(pPathInfoArray[pathIndex].targetInfo.id);

            /*Same PathArray(Display) data is duplicated in QDC PathArray Structure. Hence verifing if current PathArray is already available in pConfig */
            BOOLEAN target_found_flag = FALSE;

            for (UINT index = 0; index < pConfig->numberOfDisplays; index++)
            {
                if (targetId == pConfig->displayPathInfo[index].panelInfo.targetID &&
                    ((wcscmp(pConfig->displayPathInfo[index].panelInfo.gfxAdapter.busDeviceID, adapterInfoGdiName.adapterInfo.busDeviceID) == S_OK) &&
                     (wcscmp(pConfig->displayPathInfo[index].panelInfo.gfxAdapter.deviceInstanceID, adapterInfoGdiName.adapterInfo.deviceInstanceID) == S_OK)))
                {
                    target_found_flag = TRUE;

                    /* If same Target ID in DISPLAYCONFIG_PATH_INFO array has both Active and InActive elements. Will choose Active.*/
                    if (pPathInfoArray[pathIndex].targetInfo.statusFlags & DISPLAYCONFIG_TARGET_IN_USE)
                    {
                        pConfig->displayPathInfo[index].isActive = TRUE;
                    }
                    break;
                }
            }

            /*This will add connected Displays(Active and Non-Active) to pConfig List */
            if (target_found_flag == FALSE)
            {
                pathInfo.isActive                = (pPathInfoArray[pathIndex].targetInfo.statusFlags & DISPLAYCONFIG_TARGET_IN_USE) ? TRUE : FALSE;
                pathInfo.pathIndex               = pConfig->numberOfDisplays;
                pathInfo.sourceId                = pPathInfoArray[pathIndex].sourceInfo.id;
                pathInfo.panelInfo.sourceID      = pPathInfoArray[pathIndex].sourceInfo.id;
                pathInfo.panelInfo.gfxAdapter    = adapterInfoGdiName.adapterInfo;
                pathInfo.panelInfo.targetID      = targetId;
                pathInfo.targetId                = targetId;
                pathInfo.osTopologyInfo.pathInfo = pPathInfoArray[pathIndex];

                pathInfo.panelInfo.driverBranch = GetDriverType(adapterInfoGdiName);

                UpdateMonitorFriendlyName(&pathInfo.panelInfo);
                UpdateViewGdiDeviceName(&pathInfo.panelInfo, pathInfo.sourceId);
                UpdateMonitorPrefferedMode(&pathInfo.panelInfo);
                UpdateConnectorPortType(&pathInfo.panelInfo);

                if (pPathInfoArray[pathIndex].targetInfo.targetModeInfoIdx != DISPLAYCONFIG_PATH_TARGET_MODE_IDX_INVALID)
                    pathInfo.osTopologyInfo.targetModeInfo = pModeInfoArray[pPathInfoArray[pathIndex].targetInfo.targetModeInfoIdx].targetMode;

                if (pPathInfoArray[pathIndex].sourceInfo.sourceModeInfoIdx != DISPLAYCONFIG_PATH_SOURCE_MODE_IDX_INVALID)
                    pathInfo.osTopologyInfo.sourceModeInfo = pModeInfoArray[pPathInfoArray[pathIndex].sourceInfo.sourceModeInfoIdx].sourceMode;

                if (pPathInfoArray[pathIndex].targetInfo.desktopModeInfoIdx != DISPLAYCONFIG_PATH_DESKTOP_IMAGE_IDX_INVALID)
                    pathInfo.osTopologyInfo.desktopImageInfo = pModeInfoArray[pPathInfoArray[pathIndex].targetInfo.desktopModeInfoIdx].desktopImageInfo;

                pConfig->displayPathInfo[pConfig->numberOfDisplays] = pathInfo;
                pConfig->numberOfDisplays++;
            } // end of connected display addition
        }

        UpdateTopology(pConfig);
        if (pConfig->topology == TOPOLOGY_NONE)
        {
            pConfig->status = DISPLAY_CONFIG_ERROR_BAD_CONFIGURATION;
            PrintDisplayInfo("Bad Configuration. Logging GetConfig()", numPathArrayElements, pPathInfoArray, numModeInfoArrayElements, pModeInfoArray);
            break;
        }
    } while (FALSE);

    /* Cleanup Dynamic Allocated Memory */
    free(pPathInfoArray);
    free(pModeInfoArray);
    ClearAdapterNode(adapter_info_node);
    EtwGetDisplayConfig(pConfig->status, pConfig->topology, pConfig->numberOfDisplays);
    for (int path = 0; path <= pConfig->numberOfDisplays; path++)
    {
        int value = GetGfxIndexValue(pConfig->displayPathInfo[path].panelInfo.gfxAdapter.gfxIndex);
        EtwTargetDetails(value, pConfig->displayPathInfo[path].panelInfo.targetID, pConfig->displayPathInfo[path].isActive);
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   SetConfig (Exposed API)
 * Description:             This function has Implementation for Set Display Topology either (SINGLE / CLONE / EXTENDED)
                            for given number of displays. (Tested with MAX 3 displays)
 * @param POS_CONFIG        (_In_ Pointer to OS_CONFIG structure)
 * return: VOID             (Though function returns VOID, output structure (OS_CONFIG) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID SetConfig(_Inout_ PDISPLAY_CONFIG pConfig)
{
    UINT                     flags;
    LONG                     status;
    UINT32                   numPathArrayElements;
    DISPLAYCONFIG_PATH_INFO *pPathInfoArray = NULL;
    BOOLEAN                  adapterStatus  = FALSE;
    UINT                     pollingCount   = GET_RETRY_COUNT(6 * SEC_TO_MILLI_SEC, MILLI_SEC_100);

    do
    {
        if (NULL == pConfig)
        {
            ERROR_LOG("Input Parameter pConfig(OS_CONFIG) is NULL.");
            break;
        }
        if (pConfig->size != sizeof(DISPLAY_CONFIG))
        {
            pConfig->status = DISPLAY_CONFIG_ERROR_INSUFFICIENT_BUFFER;
            ERROR_LOG("Input Parameter pConfig Structure Size Mismatch.");
            break;
        }

        if (pConfig->numberOfDisplays == 0 || (pConfig->topology == SINGLE && pConfig->numberOfDisplays > 1) ||
            ((pConfig->topology == CLONE || pConfig->topology == EXTENDED) && pConfig->numberOfDisplays <= 1))
        {
            pConfig->status = DISPLAY_CONFIG_ERROR_INVALID_PARAMETER;
            ERROR_LOG("Topology and Number_of_Displays are NOT Matching with status code %d", pConfig->status);
            break;
        }
        numPathArrayElements = pConfig->numberOfDisplays;

        /* Allocate Buffer for SetDisplayConfig */
        pPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, (sizeof(DISPLAYCONFIG_PATH_INFO)));

        if (pPathInfoArray == NULL)
        {
            pConfig->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            ERROR_LOG("PathArray and ModeArray Memory Allocation Failed with status code %d", pConfig->status);
            break;
        }

        for (UINT pathIndex = 0; pathIndex < numPathArrayElements; pathIndex++)
        {
            pPathInfoArray[pathIndex].flags                      = DISPLAYCONFIG_PATH_ACTIVE;
            pPathInfoArray[pathIndex].sourceInfo.adapterId       = pConfig->displayPathInfo[pathIndex].panelInfo.gfxAdapter.adapterLUID;
            pPathInfoArray[pathIndex].sourceInfo.id              = ((pConfig->topology == CLONE) ? 0 : pathIndex);
            pPathInfoArray[pathIndex].sourceInfo.modeInfoIdx     = DISPLAYCONFIG_PATH_MODE_IDX_INVALID;
            pPathInfoArray[pathIndex].targetInfo.adapterId       = pConfig->displayPathInfo[pathIndex].panelInfo.gfxAdapter.adapterLUID;
            pPathInfoArray[pathIndex].targetInfo.id              = pConfig->displayPathInfo[pathIndex].panelInfo.targetID;
            pPathInfoArray[pathIndex].targetInfo.modeInfoIdx     = DISPLAYCONFIG_PATH_MODE_IDX_INVALID;
            pPathInfoArray[pathIndex].targetInfo.scaling         = DISPLAYCONFIG_SCALING_PREFERRED;
            pPathInfoArray[pathIndex].targetInfo.targetAvailable = TRUE;
            if (pConfig->topology == CLONE)
            {
                pPathInfoArray[pathIndex].sourceInfo.cloneGroupId = 1;
            }
        }

        PrintDisplayInfo("SetConfig()", numPathArrayElements, pPathInfoArray, 0, NULL);

        /* Windows API which modifies the display topology, source, and target modes by exclusively enabling the specified paths in the current session
        We are passing mode information as NULL, OS will try to apply Mode information which are stored in CCD database
        If requested config was previously used - it will fetch from CCD data base and apply, otherwise this SDC call will fail - then we will call again SDC with Different Flag*/
        flags  = SDC_APPLY | SDC_TOPOLOGY_SUPPLIED;
        status = SetDisplayConfig(numPathArrayElements, pPathInfoArray, 0, NULL, flags);

        if (ERROR_SUCCESS != status)
        {
            // for 3rd party Adapter Extended and clone config we want to send this flags.
            flags  = SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_APPLY | SDC_SAVE_TO_DATABASE | SDC_FORCE_MODE_ENUMERATION;
            status = SetDisplayConfig(numPathArrayElements, pPathInfoArray, 0, NULL, flags);
        }

        /* We are calling SetDisplayConfig again with flag SDC_USE_SUPPLIED_DISPLAY_CONFIG.
        /* Windows API which modifies the display topology, source, and target modes by exclusively enabling the specified paths in the current session and store it in CCD database
      */
        if (ERROR_SUCCESS != status)
        {
            DEBUG_LOG("Requested Config Not available in CCD_DATABASE, Retrying with SDC_USE_SUPPLIED_DISPLAY_CONFIG flag");
            flags  = SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_ALLOW_CHANGES | SDC_SAVE_TO_DATABASE | SDC_VIRTUAL_MODE_AWARE | SDC_FORCE_MODE_ENUMERATION;
            status = SetDisplayConfig(numPathArrayElements, pPathInfoArray, 0, NULL, flags);
        }

        pConfig->status = DisplayConfigErrorCode(status);
        if (ERROR_SUCCESS != status)
        {
            ERROR_LOG("Failed to apply Config. Exited with error code %d", pConfig->status);
            break;
        }

        pConfig->status = DISPLAY_CONFIG_ERROR_VERIFICATION_FAILED;
        // Verify requested config switch with QDC call
        for (INT interval = 1; interval <= pollingCount; interval++)
        {
            DISPLAY_CONFIG getConfig = { 0 };
            getConfig.size           = sizeof(DISPLAY_CONFIG);

            GetConfig(&getConfig);

            if (DISPLAY_CONFIG_ERROR_SUCCESS == getConfig.status && pConfig->topology == getConfig.topology)
            {
                BOOLEAN compareStatus = CompareDisplayPathInfo(getConfig.displayPathInfo, pConfig->displayPathInfo, getConfig.numberOfDisplays, pConfig->numberOfDisplays);
                if (TRUE == compareStatus)
                {
                    pConfig->status = DISPLAY_CONFIG_ERROR_SUCCESS;
                    break;
                }
            }
            Sleep(MILLI_SEC_100); // polling interval
        }
    } while (FALSE);

    /* Cleanup Dynamic Allocated Memory */
    free(pPathInfoArray);
    EtwSetDisplayConfig(pConfig->status, pConfig->topology, pConfig->numberOfDisplays);
    for (int path = 0; path < pConfig->numberOfDisplays; path++)
    {
        int value = GetGfxIndexValue(pConfig->displayPathInfo[path].panelInfo.gfxAdapter.gfxIndex);
        EtwTargetDetails(value, pConfig->displayPathInfo[path].panelInfo.targetID, pConfig->displayPathInfo[path].isActive);
    }
}

// INTERNAL API
BOOLEAN GetSourceIdFromPanelInfo(_Inout_ PPANEL_INFO pPanelInfo, PUINT pSourceId)
{
    BOOLEAN        status    = FALSE;
    DISPLAY_CONFIG os_config = { 0 };

    do
    {
        if (pPanelInfo == NULL)
        {
            ERROR_LOG("pPanelInfo is NULL.");
            break;
        }

        os_config.size = sizeof(DISPLAY_CONFIG);
        GetConfig(&os_config);

        if (os_config.status == DISPLAY_CONFIG_ERROR_SUCCESS)
        {
            for (int path_index = 0; path_index < os_config.numberOfDisplays; path_index++)
            {
                PANEL_INFO panelInfo = os_config.displayPathInfo[path_index].panelInfo;
                if (pPanelInfo->targetID == panelInfo.targetID && pPanelInfo->gfxAdapter.adapterLUID.LowPart == panelInfo.gfxAdapter.adapterLUID.LowPart &&
                    pPanelInfo->gfxAdapter.adapterLUID.HighPart == panelInfo.gfxAdapter.adapterLUID.HighPart)
                {
                    status     = TRUE;
                    *pSourceId = os_config.displayPathInfo[path_index].sourceId;
                    break;
                }
            }
        }

    } while (FALSE);

    return status;
}
