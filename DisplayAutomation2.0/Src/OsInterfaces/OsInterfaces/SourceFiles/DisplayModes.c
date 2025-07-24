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
//                                  Display Mode Get & Set
//=================================================================================================

/*------------------------------------------------------------------------------------------------*
*
* @file  DisplayModes.c
* @brief This file contains Implementation of GetAllSupportedModes, GetCurrentMode, SetDisplayMode,
*        GetOSPrefferedMode, GetDisplayTimings, QueryDisplayConfigEx and PrintDriverModeTable.

*------------------------------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <tchar.h>
#include <math.h>
#include "malloc.h"
#include "DisplayEscape.h"
#include "DriverEscape.h"
#include "Utilities.h"
#include "../HeaderFiles/ConfigInfo.h"
#include "../HeaderFiles/DisplayConfig.h"
#include "../Logger/ETWTestLogging.h"
#include "../DriverEscape/HeaderFiles/Utilities.h"
/**
* @brief    Helps to store DISPLAY_MODE structure's pointer.
            Later used in EDSMemoryCleanup() function to free Memory allocated for DISPLAY_MODE Structure during GetAllSupportedModes() function.
*/

MEMORY_MGR EDSMemoryCleanUpHelper;

static OS_VERSION_INFO OS_INFORMATION = { 0 };
/**---------------------------------------------------------------------------------------------------------*
 * @brief                               GetWindowsVersion (Exposed API)
 * Description:                         This function is used to get current windows version.
 * return: OS_VERSION_INFO             OS version Info Structure
 *----------------------------------------------------------------------------------------------------------*/
OS_VERSION_INFO GetWindowsVersion()
{
    CHAR  buffer[BUFFER_SIZE];
    FILE *pFileHandle = NULL;
    PCHAR pTemp       = NULL;
    ULONG osInfo[5]   = { 0 };
    do
    {
        if (0 != OS_INFORMATION.MajorVersion || 0 != OS_INFORMATION.MinorVersion)
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

        OS_INFORMATION.MajorVersion = osInfo[0];
        OS_INFORMATION.MinorVersion = osInfo[1];
        OS_INFORMATION.BuildNumber  = osInfo[2];
        OS_INFORMATION.PlatformId   = osInfo[3];

    } while (FALSE);
    return OS_INFORMATION;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                               GetDisplayConfigFlags
 * Description:                         This function is used to get flags for QDC/SDC call
 * @param flagType                      Enum to denote the flags required
 * return: UINT32                       Flag value
 *----------------------------------------------------------------------------------------------------------*/
UINT32 GetDisplayConfigFlags(_In_ FLAG_TYPES flagType)
{
    OS_VERSION_INFO osInfo;
    osInfo       = GetWindowsVersion();
    UINT32 flags = 0;

    switch (flagType)
    {
    case SDC_FLAGS_WITHOUT_OPTIMIZATION:
        flags = SDC_NO_OPTIMIZATION;

    case SDC_FLAGS:
        flags = flags | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_APPLY | SDC_SAVE_TO_DATABASE | SDC_VIRTUAL_MODE_AWARE;
        // From 21H2 OS supports virtual refresh rate aware flag
        if (osInfo.BuildNumber > WIN_21H2_BUILD_NUMBER)
            flags = flags | SDC_VIRTUAL_REFRESH_RATE_AWARE;
        break;

    case QDC_FLAGS:
        flags = QDC_VIRTUAL_MODE_AWARE | QDC_DATABASE_CURRENT;
        // From 21H2 OS supports virtual refresh rate aware flag
        if (osInfo.BuildNumber > WIN_21H2_BUILD_NUMBER)
            flags = flags | QDC_VIRTUAL_REFRESH_RATE_AWARE;
        break;

    case QDC_ACTIVE_PATHS:
        flags = QDC_VIRTUAL_MODE_AWARE | QDC_ONLY_ACTIVE_PATHS;
        // From 21H2 OS supports virtual refresh rate aware flag
        if (osInfo.BuildNumber > WIN_21H2_BUILD_NUMBER)
            flags = flags | QDC_VIRTUAL_REFRESH_RATE_AWARE;
        break;
    default:
        break;
    }
    return flags;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                               GetAllSupportedModes (Exposed API)
 * Description:                         This function is used to get all supported Modes with/without Rotation (90,180,270) based on PanelInfo and Rotation Flag.
 * @param PANEL_INFO                    (_Inout_ PANEL_INFO: Target ID and Adapter Information of the Display)
 * @param UINT                          (_In_ rotation_flag: If this flag is set, modes with ROTATION 90, 180, 270 will be added)
 * @param PENUMERATED_DISPLAY_MODES     (_Out_ Return ENUMERATED_DISPLAY_MODES Structure with all supported modes)
 * return: VOID                         (Though function returns VOID, output parameter (ENUMERATED_DISPLAY_MODES) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID GetAllSupportedModes(_Inout_ PANEL_INFO *pPanelInfo, _In_ BOOLEAN rotation_flag, _Out_ PENUMERATED_DISPLAY_MODES pEnumDisplayModes)
{
    INT                              count                  = 0;
    INT                              numberofSupportedModes = 0;
    BOOLEAN                          scaling_query          = FALSE;
    DWORD                            dwEdsFlag              = 0;
    DWORD                            modeIndex              = 0;
    DEVMODE                          devMode;
    ULONG                            deviceInfoRet;
    BOOLEAN                          adapterStatus                           = FALSE;
    WCHAR                            displayViewGdiDeviceName[CCHDEVICENAME] = { 0 };
    DISPLAY_MODE                     displayMode                             = { 0 };
    DISPLAYCONFIG_SOURCE_DEVICE_NAME deviceInfo;
    ADAPTER_INFO_GDI_NAME            adapterInfoGdiName = { 0 };

    /* Input Node to stores data from EDS (X, Y, RR and Scanline) */
    struct DISPLAYNODE *eds_input_node = NULL;
    /* Output Node to stores data of EDS with all supported SCALING */
    struct DISPLAYNODE *eds_output_node = NULL;

    do
    {
        if (pEnumDisplayModes == NULL)
        {
            pEnumDisplayModes->status = DISPLAY_CONFIG_ERROR_INVALID_PARAMETER;
            ERROR_LOG("pEnumDisplayModes of ENUMERATED_DISPLAY_MODES Structure is NULL.");
            break;
        }

        if (pEnumDisplayModes->size != sizeof(ENUMERATED_DISPLAY_MODES))
        {
            pEnumDisplayModes->status = DISPLAY_CONFIG_ERROR_SIZE_MISMATCH;
            ERROR_LOG("pEnumDisplayModes Size mismatch. Actual: %d Expected: %d.", pEnumDisplayModes->size, sizeof(ENUMERATED_DISPLAY_MODES));
            break;
        }

        /* Free if EDSMemoryCleanUpHelper, if ENUMERATED_DISPLAY_MODES pointer is available */
        EDSMemoryCleanup();

        // Getting AdapterID and ViewGDIDeviceName based on AdapterInfo.
        adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
        adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);

        if (adapterStatus == FALSE)
        {
            ERROR_LOG("{GetAdapterDetails} for Given Adapter Information.");
            pEnumDisplayModes->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
            break;
        }

        ZeroMemory(pEnumDisplayModes, sizeof(ENUMERATED_DISPLAY_MODES));
        pEnumDisplayModes->size = sizeof(ENUMERATED_DISPLAY_MODES);

        // Initialize deviceInfo Header to find Source Device Name (Which is required for getting Handle in Driver ESC)
        ZeroMemory(&deviceInfo, sizeof(DISPLAYCONFIG_SOURCE_DEVICE_NAME));
        deviceInfo.header.size      = sizeof(DISPLAYCONFIG_SOURCE_DEVICE_NAME);
        deviceInfo.header.type      = DISPLAYCONFIG_DEVICE_INFO_GET_SOURCE_NAME;
        deviceInfo.header.id        = pPanelInfo->sourceID;
        deviceInfo.header.adapterId = adapterInfoGdiName.adapterID;
        deviceInfoRet               = DisplayConfigGetDeviceInfo(&deviceInfo.header);
        CopyWchar(displayViewGdiDeviceName, _countof(displayViewGdiDeviceName), deviceInfo.viewGdiDeviceName);

        if (rotation_flag == TRUE)
        {
            INFO_LOG("Rotation Flag is SET. Get all Supported Modes with ROTATE_90, ROTATE_180 and ROTATE_270.");
            dwEdsFlag = EDS_ROTATEDMODE;
        }
        else
        {
            dwEdsFlag = EDS_RAWMODE;
        }

        devMode.dmSize = sizeof(DEVMODE);

        /* The EnumDisplaySettingsEx function retrieves information about one of the graphics modes for a display device.
        To retrieve information for all the graphics modes for a display device, make a series of calls to this function.*/
        while (EnumDisplaySettingsEx(displayViewGdiDeviceName, modeIndex, &devMode, dwEdsFlag))
        {
            displayMode.targetId         = pPanelInfo->targetID;
            displayMode.panelInfo        = *pPanelInfo;
            displayMode.refreshRate      = (UINT)devMode.dmDisplayFrequency;
            displayMode.scanlineOrdering = (devMode.dmDisplayFlags == 0 ? PROGRESSIVE : INTERLACED);

            /* Windows 8.1 and later can no longer query or set display modes that are less than 32 bits per pixel (bpp) these operations will fail.
            Hence hard coding BPP value as 32BPP.*/
            displayMode.BPP      = PIXELFORMAT_32BPP;
            displayMode.rotation = TranslateOrientationOsToInternal(devMode.dmDisplayOrientation);

            // EDS retuns Inverted X,Y for 90 and 270 degree, hence inverting X,Y (which is requirement for SDC while appling mode).
            if (displayMode.rotation == ROTATE_90 || displayMode.rotation == ROTATE_270)
            {
                displayMode.HzRes = (UINT)devMode.dmPelsHeight;
                displayMode.VtRes = (UINT)devMode.dmPelsWidth;
            }
            else
            {
                displayMode.HzRes = (UINT)devMode.dmPelsWidth;
                displayMode.VtRes = (UINT)devMode.dmPelsHeight;
            }

            if (displayMode.scanlineOrdering == INTERLACED)
            {
                /* For 29i, 59i and 119i display driver enumerate as 59i, 119i and 239i */
                if (displayMode.refreshRate == 29 || displayMode.refreshRate == 59 || displayMode.refreshRate == 119 || displayMode.refreshRate == 239)
                {
                    displayMode.refreshRate = (displayMode.refreshRate * 2) + 1;
                }
                else
                {
                    displayMode.refreshRate = displayMode.refreshRate * 2;
                }
            }

            /* Check for Duplicate X,Y RR, Scanline and Rotation */
            if (IsModePresentInList(eds_input_node, displayMode) == FALSE)
            {
                AddModeToList(&eds_input_node, displayMode);
            }
            modeIndex++;
        }

        // WA: adapterInfoGdiName memory gets corrupted after EDS call, To maintain the display name it is re-initialized
        adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
        adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);
        DRIVER_TYPE driverBranch       = GetDriverType(adapterInfoGdiName);

        /* EDS will report Scaling as "DEFAULT" For both MDS(Maintain Display Scaling ) and MAR ( Maintain Aspect Ratio )
        Hence need to ignore scaling information from EDS,  instead add scaling data according to driver mode table. */
        if (driverBranch == YANGRA_DRIVER)
        {
            scaling_query = UpdateScalingInfoForModeTableYangra(pPanelInfo, eds_input_node, &eds_output_node, &numberofSupportedModes);
        }
        else if (driverBranch == LEGACY_DRIVER)
        {
            scaling_query = UpdateScalingInfoForModeTableLegacy(pPanelInfo, eds_input_node, &eds_output_node, &numberofSupportedModes);
        }
        else if (driverBranch == DRIVER_UNKNOWN)
        {
            scaling_query = UpdateScalingInfoForModeTable3rdParty(pPanelInfo, eds_input_node, &eds_output_node, &numberofSupportedModes);
        }
        else
        {
            pEnumDisplayModes->status = DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED;
            ERROR_LOG("{GetDriverType} for given AdapterInfo / Maybe a Third Party Gfx driver.");
            break;
        }

        if (scaling_query == TRUE)
        {
            PDISPLAY_MODE pModeList = (PDISPLAY_MODE)calloc(numberofSupportedModes, sizeof(DISPLAY_MODE));

            if (pModeList == NULL)
            {
                pEnumDisplayModes->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
                ERROR_LOG("Memory allocation for pModeList Failed.");
                break;
            }

            struct DISPLAYNODE *temp_node = eds_output_node;

            while (NULL != temp_node)
            {
                pModeList[count] = temp_node->displayMode;
                temp_node        = temp_node->next;
                count++;
            }
            pEnumDisplayModes->noOfSupportedModes = numberofSupportedModes;
            pEnumDisplayModes->pDisplayMode       = pModeList;
            pEnumDisplayModes->status             = DISPLAY_CONFIG_ERROR_SUCCESS;

            /* Store Allocated memory in array list, during cleanup we will free this dynamically allocated memory */
            EDSMemoryCleanUpHelper.noOfSupportedModes = &numberofSupportedModes;
            EDSMemoryCleanUpHelper.pDisplayMode       = pModeList;
        }
        else
        {
            pEnumDisplayModes->noOfSupportedModes = 0;
            pEnumDisplayModes->status             = DISPLAY_CONFIG_ERROR_QUERY_MODE_FAILED;
            ERROR_LOG("Query Driver Mode Table for Adding scaling support Failed.");
        }
    } while (FALSE);

    ClearDisplayNode(eds_output_node);
    ClearDisplayNode(eds_input_node);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   UpdateScalingInfoForModeTableYangra (Internal API)
 * Description:             This function is used query driver to get all supported scaling for Supported Mode list for Yangra Driver.
 * @param PANEL_INFO        (_In_   Pointer to PANEL_INFO structure)
 * @param DISPLAYNODE       (_In_   Supported Modes)
 * @param DISPLAYNODE       (_Out_  Supported Modes updated with supported scaling)
 * @param PINT              (_Out_  Pointer to Number of Supported modes in Link list)
 * return: BOOLEAN          (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN UpdateScalingInfoForModeTableYangra(_In_ PANEL_INFO *pPanelInfo, _In_ struct DISPLAYNODE *pInputDisplayNode, _Out_ struct DISPLAYNODE **pOutputDisplayNode,
                                            _Out_ PINT pNumOfDisplayModes)
{
    BOOLEAN                       retStatus               = FALSE;
    ULONG                         vSyncDenominator        = 0;
    INT                           computedRoundedRR       = 0;
    INT                           iNumberOfSupportedModes = 0;
    UINT                          numSrcMode              = 0;
    UINT                          numTgtMode              = 0;
    DD_TIMING_INFO *              pTgtModeTable;
    DD_SOURCE_MODE_INFO *         pSrcModeTable;
    DD_ESC_QUERY_MODE_TABLE_ARGS  modeTableArgs  = { 0 };
    DD_ESC_QUERY_MODE_TABLE_ARGS *pModeTableArgs = NULL;
    FLOAT                         f_refreshRate  = 0.0;

    do
    {
        /* Call QueryDisplayModeTableFromYangraDriver to only NumberOfSourceMode and NumberOfTargetMode */
        modeTableArgs.modeInfo[0].targetID = pPanelInfo->targetID;
        if (FALSE == YangraQueryModeTable(pPanelInfo, &modeTableArgs))
            break;

        /* Allocate Memory based on NumberOfSourceMode and NumberOfTargetMode to fetch complete Source and Target Mode Table */
        pModeTableArgs = (DD_ESC_QUERY_MODE_TABLE_ARGS *)calloc(
        1, (sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS) + sizeof(DD_TIMING_INFO) * modeTableArgs.numTgtModes + sizeof(DD_SOURCE_MODE_INFO) * modeTableArgs.numSrcModes));

        pModeTableArgs->numSrcModes          = modeTableArgs.numSrcModes;
        pModeTableArgs->numTgtModes          = modeTableArgs.numTgtModes;
        pModeTableArgs->modeInfo[0].targetID = pPanelInfo->targetID;

        if (FALSE == YangraQueryModeTable(pPanelInfo, pModeTableArgs))
            break;

        // Iterated through InputDisplayMode list and update OutputDisplayMode list with all supported scaling and PixelClk.
        while (pInputDisplayNode != NULL)
        {
            DISPLAY_MODE displayMode = pInputDisplayNode->displayMode;

            /* Memory location of Target Mode Table from DD_ESC_QUERY_MODE_TABLE_ARGS*/
            pTgtModeTable = (DD_TIMING_INFO *)DD_VOID_PTR_INC(pModeTableArgs, sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS));
            /* Memory location of Source Mode Table from DD_ESC_QUERY_MODE_TABLE_ARGS*/
            pSrcModeTable = (DD_SOURCE_MODE_INFO *)DD_VOID_PTR_INC(pModeTableArgs, sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS) + (sizeof(DD_TIMING_INFO) * (pModeTableArgs->numTgtModes)));

            for (INT srcModeCount = 0; srcModeCount < modeTableArgs.numSrcModes; srcModeCount++)
            {
                // Step1: Find wheather requested Mode X and Y is available in SourceModeTable
                if ((pSrcModeTable->visibleScreenX == pInputDisplayNode->displayMode.HzRes) && (pSrcModeTable->visibleScreenY == pInputDisplayNode->displayMode.VtRes))
                {
                    INT numMappedTgtModes = pSrcModeTable->numMappedTgtModes;

                    for (INT targetModeCount = 0; targetModeCount < numMappedTgtModes; targetModeCount++)
                    {
                        displayMode.samplingMode = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].flags.ceData.samplingMode.Value;

                        // Check for Scanline and compute corresponding vSyncDenominator.
                        if (pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].isInterlaced)
                            vSyncDenominator = ((pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hTotal) *
                                                (pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vTotal)) /
                                               2;
                        else
                            vSyncDenominator = ((pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hTotal) *
                                                (pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vTotal));

                        // Calculate FLOAT RR and compute its Rounded Value
                        f_refreshRate     = ((FLOAT)pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock / vSyncDenominator);
                        computedRoundedRR = RefreshRateRoundOff(f_refreshRate);
                        INT drv_scanline  = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].isInterlaced ? INTERLACED : PROGRESSIVE;

                        // Check wheather requested X,Y,RR has exact matching Target in MappedTargetMode Table.
                        if ((pSrcModeTable->visibleScreenX == pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hActive) &&
                            (pSrcModeTable->visibleScreenY == pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vActive) &&
                            ((pInputDisplayNode->displayMode.refreshRate == computedRoundedRR) ||
                             (pInputDisplayNode->displayMode.refreshRate == pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vRoundedRR)) &&
                            (pInputDisplayNode->displayMode.scanlineOrdering == drv_scanline))
                        //|| (pInputDisplayNode->displayMode.refreshRate == pTgtModeTable[pSrcModeTable->MappedTgtModeIndex[targetModeCount]].VRoundedRR))
                        {
                            // Requested X, Y, RR has exact match, hence add MDS Scaling
                            displayMode.pixelClock_Hz = (LONG)pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock;
                            displayMode.scaling       = MDS;
                            displayMode.status        = DISPLAY_CONFIG_ERROR_SUCCESS;
                            if (AddModeToList(pOutputDisplayNode, displayMode))
                                iNumberOfSupportedModes++;
                        }
                        else
                        {
                            // Check wheather requested RR has different X, Y in MappedTargetMode Table.
                            if (((pSrcModeTable->visibleScreenX != pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hActive) ||
                                 (pSrcModeTable->visibleScreenY != pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vActive)) &&
                                ((pInputDisplayNode->displayMode.refreshRate == computedRoundedRR) && (pInputDisplayNode->displayMode.scanlineOrdering == drv_scanline)))
                            {
                                // Requested RR has differnt X,Y support, hence add all other Scaling (CI, MAR, FS).
                                displayMode.pixelClock_Hz = (LONG)pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock;
                                displayMode.scaling       = CI;
                                displayMode.status        = DISPLAY_CONFIG_ERROR_SUCCESS;
                                if (AddModeToList(pOutputDisplayNode, displayMode))
                                    iNumberOfSupportedModes++;

                                displayMode.scaling = MAR;
                                displayMode.status  = DISPLAY_CONFIG_ERROR_SUCCESS;
                                if (AddModeToList(pOutputDisplayNode, displayMode))
                                    iNumberOfSupportedModes++;

                                displayMode.scaling = FS;
                                displayMode.status  = DISPLAY_CONFIG_ERROR_SUCCESS;
                                if (AddModeToList(pOutputDisplayNode, displayMode))
                                    iNumberOfSupportedModes++;
                            }
                        }
                    } // targetModeCount FOR Loop END

                    // Requested X and Y Match found in SourceModeTable. Supported scaling Identified, Hence Break.
                    break;
                }

                // Requested X and Y Match not found Increment SourceModeTable pointer.
                pSrcModeTable = (DD_SOURCE_MODE_INFO *)DD_VOID_PTR_INC(pSrcModeTable, sizeof(DD_SOURCE_MODE_INFO));

            } // srcModeCount FOR Loop END
            // Move Pointer to Next DISPLAY_NODE to pInputDisplayNode
            pInputDisplayNode = pInputDisplayNode->next;
        } // InputDisplayNode While Loop END

        free(pModeTableArgs);

        if (iNumberOfSupportedModes == 0)
        {
            ERROR_LOG("Query Driver for DisplayMode Table failed. NumSrcMode: %c NumTgtMode: %c", modeTableArgs.numSrcModes, modeTableArgs.numTgtModes);
        }
        else
        {
            *pNumOfDisplayModes = iNumberOfSupportedModes;
            retStatus           = TRUE;
        }
    } while (FALSE);
    return retStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           GetDisplayHWTimingYangra (Internal API)
 * Description:                     This function is used to get Display Timing for given DisplayMode for Yangra Driver.
 *                                  ( Based on Target ID and X , Y , RR , Scanline )
 * @param DISPLAY_MODE              (_In_   Requested Display Mode)
 * @param PADAPTER_INFO_GDI_NAME    (_In_   pointer of ADAPTER_INFO_GDI_NAME)
 * @param DD_TIMING_INFO            (_Out_  Output Display Timing Structure)
 * @param PINT                      (_Out_  Pointer value - 1- If returned Timing is prefferred Mode's timings else 0)
 * return: BOOLEAN                  (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetDisplayHWTimingYangra(_In_ DISPLAY_MODE displayMode, _In_ PADAPTER_INFO_GDI_NAME pAdapterInfoGdiName, _Out_ DISPLAY_TIMINGS *pDisplayTimings,
                                 _Out_ PINT pIsOSPreferredMode)
{
    FLOAT f_refreshRate           = 0.0;
    BOOL  retStatus               = FALSE;
    ULONG vSyncDenominator        = 0;
    INT   computedRoundedRR       = 0;
    INT   iNumberOfSupportedModes = 0;
    UINT  numSrcMode              = 0;
    UINT  numTgtMode              = 0;
    BOOL  CompareRoundedRR        = FALSE;

    TARGET_DEVICE_INFO            targetDeviceInfo = { 0 };
    DD_TIMING_INFO *              pTgtModeTable;
    DD_SOURCE_MODE_INFO *         pSrcModeTable;
    DD_ESC_QUERY_MODE_TABLE_ARGS *pSourceAndTargetModeTableArgs = NULL;
    DD_ESC_QUERY_MODE_TABLE_ARGS  modeTableArgs                 = { 0 };

    do
    {
        /* Call QueryDisplayModeTableFromYangraDriver to only NumberOfSourceMode and NumberOfTargetMode */
        modeTableArgs.modeInfo[0].targetID = displayMode.panelInfo.targetID;
        if (FALSE == YangraQueryModeTable(&displayMode.panelInfo, &modeTableArgs))
            break;

        /* Allocate Memory based on NumberOfSourceMode and NumberOfTargetMode to fetch complete Source and Target Mode Table */
        pSourceAndTargetModeTableArgs = (DD_ESC_QUERY_MODE_TABLE_ARGS *)calloc(
        1, (sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS) + sizeof(DD_TIMING_INFO) * modeTableArgs.numTgtModes + sizeof(DD_SOURCE_MODE_INFO) * modeTableArgs.numSrcModes));
        pSourceAndTargetModeTableArgs->numSrcModes          = modeTableArgs.numSrcModes;
        pSourceAndTargetModeTableArgs->numTgtModes          = modeTableArgs.numTgtModes;
        pSourceAndTargetModeTableArgs->modeInfo[0].targetID = displayMode.panelInfo.targetID;

        if (FALSE == YangraQueryModeTable(&displayMode.panelInfo, pSourceAndTargetModeTableArgs))
            break;

        /* Memory location of Target Mode Table from DD_ESC_QUERY_MODE_TABLE_ARGS*/
        pTgtModeTable = (DD_TIMING_INFO *)DD_VOID_PTR_INC(pSourceAndTargetModeTableArgs, sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS));
        /* Memory location of Source Mode Table from DD_ESC_QUERY_MODE_TABLE_ARGS*/
        pSrcModeTable = (DD_SOURCE_MODE_INFO *)DD_VOID_PTR_INC(pSourceAndTargetModeTableArgs,
                                                               sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS) + (sizeof(DD_TIMING_INFO) * (pSourceAndTargetModeTableArgs->numTgtModes)));

        for (INT srcModeCount = 0; srcModeCount < pSourceAndTargetModeTableArgs->numSrcModes; srcModeCount++)
        {
            // Step1: Find wheather requested Mode X and Y is available in SourceModeTable
            if ((pSrcModeTable->visibleScreenX == displayMode.HzRes) && (pSrcModeTable->visibleScreenY == displayMode.VtRes))
            {
                INT numMappedTgtModes = pSrcModeTable->numMappedTgtModes;
                INT targetModeCount;

            ReRunToCheckRoundedRR:
                for (targetModeCount = 0; targetModeCount < numMappedTgtModes; targetModeCount++)
                {
                    // Check for Scanline and compute corresponding vSyncDenominator.
                    if (pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].isInterlaced)
                        vSyncDenominator =
                        ((pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hTotal) * (pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vTotal)) /
                        2;
                    else
                        vSyncDenominator =
                        ((pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hTotal) * (pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vTotal));

                    // Calculate FLOAT RR and compute its Rounded Value
                    INFO_LOG("RR calculated = dotClock %lu / vSyncDenominator %lu", pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock, vSyncDenominator);
                    f_refreshRate     = ((FLOAT)pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock / vSyncDenominator);
                    computedRoundedRR = RefreshRateRoundOff(f_refreshRate);
                    INFO_LOG("f_refreshRate = %f and computedRoundedRR = %d", f_refreshRate, computedRoundedRR);
                    INT drv_scanline = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].isInterlaced ? INTERLACED : PROGRESSIVE;

                    if (CompareRoundedRR == TRUE)
                    {
                        computedRoundedRR = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vRoundedRR;
                    }

                    if (displayMode.scaling == MDS)
                    {
                        // Check whether requested X,Y,RR has exact matching Target in MappedTargetMode Table.
                        if ((pSrcModeTable->visibleScreenX == pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hActive) &&
                            (pSrcModeTable->visibleScreenY == pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vActive) &&
                            (((displayMode.refreshRate == computedRoundedRR) && (displayMode.rrMode == LEGACY_RR)) ||
                             ((displayMode.rrMode == DYNAMIC_RR) && (pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].flags.preferredMode == 1))) &&
                            (displayMode.scanlineOrdering == drv_scanline))
                        //|| (pInputDisplayNode->displayMode.refreshRate == pTgtModeTable[pSrcModeTable->MappedTgtModeIndex[targetModeCount]].VRoundedRR))
                        {
                            // Requested X, Y, RR has exact match, hence add MDS Scaling
                            pDisplayTimings->hActive          = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hActive;
                            pDisplayTimings->vActive          = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vActive;
                            pDisplayTimings->hSyncNumerator   = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock;
                            pDisplayTimings->hSyncDenominator = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hTotal;
                            pDisplayTimings->targetPixelRate  = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock;
                            pDisplayTimings->hTotal           = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hTotal;
                            pDisplayTimings->vTotal           = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vTotal;
                            pDisplayTimings->vSyncNumerator   = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock;
                            if (drv_scanline == INTERLACED)
                            {
                                pDisplayTimings->vSyncDenominator = (pDisplayTimings->hTotal * pDisplayTimings->vTotal) / 2;
                                pDisplayTimings->scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                            }
                            else
                            {
                                pDisplayTimings->vSyncDenominator = pDisplayTimings->hTotal * pDisplayTimings->vTotal;
                                pDisplayTimings->scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE;
                            }

                            float rr                     = (FLOAT)pDisplayTimings->vSyncNumerator / pDisplayTimings->vSyncDenominator;
                            pDisplayTimings->refreshRate = RefreshRateRoundOff(rr);
                            pDisplayTimings->status      = DISPLAY_CONFIG_ERROR_SUCCESS;
                            retStatus                    = TRUE;
                            break;
                        }
                    }
                    else
                    {
                        // Check whether requested RR has different X, Y in MappedTargetMode Table.
                        if (((pSrcModeTable->visibleScreenX != pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hActive) ||
                             (pSrcModeTable->visibleScreenY != pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vActive)) &&
                            ((displayMode.refreshRate == computedRoundedRR) && (displayMode.scanlineOrdering == drv_scanline)))
                        {
                            pDisplayTimings->hActive          = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hActive;
                            pDisplayTimings->vActive          = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vActive;
                            pDisplayTimings->hSyncNumerator   = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock;
                            pDisplayTimings->hSyncDenominator = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hTotal;
                            pDisplayTimings->targetPixelRate  = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock;
                            pDisplayTimings->hTotal           = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hTotal;
                            pDisplayTimings->vTotal           = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vTotal;
                            pDisplayTimings->vSyncNumerator   = pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock;
                            if (drv_scanline == INTERLACED)
                            {
                                pDisplayTimings->vSyncDenominator = (pDisplayTimings->hTotal * pDisplayTimings->vTotal) / 2;
                                pDisplayTimings->scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                            }
                            else
                            {
                                pDisplayTimings->vSyncDenominator = pDisplayTimings->hTotal * pDisplayTimings->vTotal;
                                pDisplayTimings->scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE;
                            }

                            float rr                     = (FLOAT)pDisplayTimings->vSyncNumerator / pDisplayTimings->vSyncDenominator;
                            pDisplayTimings->refreshRate = RefreshRateRoundOff(rr);
                            pDisplayTimings->status      = DISPLAY_CONFIG_ERROR_SUCCESS;
                            retStatus                    = TRUE;
                            break;
                        }
                    }
                } // targetModeCount FOR Loop END
                if (retStatus == FALSE)
                {
                    if (CompareRoundedRR == FALSE)
                    {
                        CompareRoundedRR = TRUE;
                        goto ReRunToCheckRoundedRR;
                    }
                }
                // Requested X and Y Match found in SourceModeTable. Supported scaling Identified, Hence Break.
                break;
            }
            // Requested X and Y Match not found Increment SourceModeTable pointer.
            pSrcModeTable = (DD_SOURCE_MODE_INFO *)DD_VOID_PTR_INC(pSrcModeTable, sizeof(DD_SOURCE_MODE_INFO));
        } // srcModeCount FOR Loop END

        if (retStatus == TRUE)
        {
            // If Status is TRUE means TargetTimings Found.
            // If pIsOSPreferredMode is TRUE means retrying with OS Preffered mode completed.
            break;
        }
        else
        {
            // If Driver is not able to find respective Target Timing then will utilize Preffered Mode.
            DEBUG_LOG("Get DisplayTimings for requested mode failed. Retrying again with Prefferred Mode");
            retStatus = FALSE;
        }

        free(pSourceAndTargetModeTableArgs);

    } while (FALSE);

    return retStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           UpdateScalingInfoForModeTableLegacy (Internal API)
 * Description:                     This function is used query driver to get all supported scaling for Supported Mode list for Legacy Driver.
 * @param PANEL_INFO                (_In_   pointer of PANEL_INFO)
 * @param DISPLAYNODE               (_In_   Supported Modes)
 * @param DISPLAYNODE               (_Out_  Supported Modes updated with supported scaling)
 * @param PINT                      (_Out_  Pointer to Number of Supported modes in Link list)
 * return: BOOLEAN                  (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN UpdateScalingInfoForModeTableLegacy(_In_ PANEL_INFO *pPanelInfo, _In_ struct DISPLAYNODE *pInputDisplayNode, _Out_ struct DISPLAYNODE **pOutputDisplayNode,
                                            _Out_ PINT pNumOfDisplayModes)
{
    USHORT            supportedScaling        = 0;
    BOOLEAN           retStatus               = FALSE;
    INT               iNumberOfSupportedModes = 0;
    CUI_ESC_MODE_INFO escmodeInfo             = { 0 };

    while (pInputDisplayNode != NULL)
    {
        DISPLAY_MODE displayMode = pInputDisplayNode->displayMode;

        // Get supported scaling for current resolution.
        escmodeInfo.sourceX        = pInputDisplayNode->displayMode.HzRes;
        escmodeInfo.sourceY        = pInputDisplayNode->displayMode.VtRes;
        escmodeInfo.refreshRate    = pInputDisplayNode->displayMode.refreshRate;
        escmodeInfo.eScanLineOrder = pInputDisplayNode->displayMode.scanlineOrdering;

        // Get supported scaling for current resolution.
        if (FALSE == LegacyGetSupportedScaling(&pPanelInfo->gfxAdapter, displayMode.targetId, escmodeInfo, &supportedScaling))
            return retStatus;

        // Ignore CAR scaling, Since through OS API we can not apply custom aspect ratio
        supportedScaling &= ~(CAR);

        if ((supportedScaling & CI) != 0)
        {
            displayMode.pixelClock_Hz = 0;
            displayMode.scaling       = CI;
            displayMode.status        = DISPLAY_CONFIG_ERROR_SUCCESS;
            if (AddModeToList(pOutputDisplayNode, displayMode))
                iNumberOfSupportedModes++;
        }
        if ((supportedScaling & FS) != 0)
        {
            displayMode.pixelClock_Hz = 0;
            displayMode.scaling       = FS;
            displayMode.status        = DISPLAY_CONFIG_ERROR_SUCCESS;
            if (AddModeToList(pOutputDisplayNode, displayMode))
                iNumberOfSupportedModes++;
        }
        if ((supportedScaling & MAR) != 0)
        {
            displayMode.pixelClock_Hz = 0;
            displayMode.scaling       = MAR;
            displayMode.status        = DISPLAY_CONFIG_ERROR_SUCCESS;
            if (AddModeToList(pOutputDisplayNode, displayMode))
                iNumberOfSupportedModes++;
        }
        if ((supportedScaling & MDS) != 0)
        {
            displayMode.pixelClock_Hz = 0;
            displayMode.scaling       = MDS;
            displayMode.status        = DISPLAY_CONFIG_ERROR_SUCCESS;
            if (AddModeToList(pOutputDisplayNode, displayMode))
                iNumberOfSupportedModes++;
        }

        pInputDisplayNode = pInputDisplayNode->next;
    } // pInputDisplayNode While loop End

    if (iNumberOfSupportedModes == 0)
    {
        ERROR_LOG("Query Driver for DisplayMode Table failed.");
    }
    else
    {
        *pNumOfDisplayModes = iNumberOfSupportedModes;
        retStatus           = TRUE;
    }

    return retStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   UpdateScalingInfoForModeTable3rdParty (Internal API)
 * Description:             This function is used update scaling for Supported Mode list for 3rd Party Driver.( Like AMD / Nvidia )
 * @param PANEL_INFO        (_In_   PANEL_INFO Target ID and Adapter Information of the Respective Display)
 * @param DISPLAYNODE       (_In_   Supported Modes)
 * @param DISPLAYNODE       (_Out_  Supported Modes updated with supported scaling)
 * @param PINT              (_Out_  Pointer to Number of Supported modes in Link list)
 * return: BOOLEAN          (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN UpdateScalingInfoForModeTable3rdParty(_Inout_ PANEL_INFO *panelInfo, _In_ struct DISPLAYNODE *pInputDisplayNode, _Out_ struct DISPLAYNODE **pOutputDisplayNode,
                                              _Out_ PINT pNumOfDisplayModes)
{
    BOOLEAN         bStatus                 = TRUE;
    USHORT          supportedScaling        = 0;
    BOOLEAN         retStatus               = FALSE;
    INT             iNumberOfSupportedModes = 0;
    DISPLAY_TIMINGS targetTimingInfo        = { 0 };

    while (pInputDisplayNode != NULL)
    {
        DISPLAY_MODE displayMode = pInputDisplayNode->displayMode;

        // Get supported scaling for OS Preferred resolution.
        bStatus             = GetOSPrefferedMode(panelInfo, &targetTimingInfo);
        displayMode.scaling = MAR; // Right now we are only supporting One scaling Option "MAR " , based on need we can extend other scaling option CI / FS  ( MDS cannot be
                                   // supported, as we do not have details of Timing info other than Native mode)
        displayMode.pixelClock_Hz = targetTimingInfo.targetPixelRate;
        displayMode.status        = DISPLAY_CONFIG_ERROR_SUCCESS;
        if (AddModeToList(pOutputDisplayNode, displayMode))
            iNumberOfSupportedModes++;
        pInputDisplayNode = pInputDisplayNode->next;
    } // pInputDisplayNode While loop End

    if (iNumberOfSupportedModes == 0)
    {
        ERROR_LOG("Query Driver for DisplayMode Table failed.");
    }
    else
    {
        *pNumOfDisplayModes = iNumberOfSupportedModes;
        retStatus           = TRUE;
    }

    return retStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   GetDisplayHWTimingLegacy (Internal API)
 * Description:             This function is used to get Display Timing for given DisplayMode for Legacy Driver.
 * @param DISPLAY_MODE      (_In_   Requested Display Mode)
 * @param PDISPLAY_TIMINGS  (_Out_  Output Display Timing Structure)
 * @param PINT              (_Out_  Pointer value - 1- If returned a Prefferred Mode timings else 0)
 * return: BOOLEAN          (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetDisplayHWTimingLegacy(_In_ DISPLAY_MODE displayMode, _Out_ PDISPLAY_TIMINGS pDisplayTimings, _Out_ PINT pIsOSPreferredMode)
{
    BOOLEAN retStatus              = FALSE;
    BOOLEAN bEscStatus             = FALSE;
    *pIsOSPreferredMode            = FALSE;
    RR_RATIONAL_INFO rational_Info = { 0 };

    do
    {
        bEscStatus = GetTargetTimingsFromLegacyDriver(&displayMode, &rational_Info);

        if (bEscStatus == TRUE)
        {
            if (rational_Info.hActive != 0 || rational_Info.vActive != 0)
            {
                pDisplayTimings->hActive          = rational_Info.hActive;
                pDisplayTimings->vActive          = rational_Info.vActive;
                pDisplayTimings->hSyncNumerator   = rational_Info.hSyncNumerator;
                pDisplayTimings->hSyncDenominator = rational_Info.hSyncDenominator;
                pDisplayTimings->targetPixelRate  = rational_Info.pixelRate;
                pDisplayTimings->hTotal           = rational_Info.hTotal;
                pDisplayTimings->vTotal           = rational_Info.vTotal;
                pDisplayTimings->vSyncNumerator   = rational_Info.vSyncNumerator;
                pDisplayTimings->vSyncDenominator = rational_Info.vSyncDenominator;
                // Since Legacy Display HW Function is not providing Scanline information - we are assumming and assigning scanline based on input only.
                if (displayMode.scanlineOrdering == INTERLACED)
                {
                    pDisplayTimings->scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                }
                else
                {
                    pDisplayTimings->scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE;
                }

                pDisplayTimings->status = DISPLAY_CONFIG_ERROR_SUCCESS;
                retStatus               = TRUE;
            }
            else
            {
                // If Driver is not able to find respective Target Timing then will utilize Preffered Mode
                DEBUG_LOG("Get DisplayTimings for requested mode failed. Retrying again with Prefferred Mode");
                if (GetOSPrefferedMode(&displayMode.panelInfo, pDisplayTimings) == FALSE)
                {

                    ERROR_LOG("Get Preffered Mode from OS failed.");
                    break;
                }
                else
                {
                    retStatus = TRUE;
                }
            }
        }
        else
        {
            DEBUG_LOG("Get DisplayTimings through driver Escape Failed.");
            break;
        }
    } while (FALSE);

    return retStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   GetTargetTimingsLegacy (Internal API)
 * Description:             This function is used to get Display Timing for given DisplayMode for Legacy Driver.
 * @param PDISPLAY_MODE     (_In_   Pointer to Requested Display Mode)
 * @param PRR_RATIONAL_INFO (_Out_  Pointer to Output Display Timing Structure)
 * return: BOOLEAN          (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetTargetTimingsFromLegacyDriver(_In_ PDISPLAY_MODE pDisplayMode, _Out_ PRR_RATIONAL_INFO pDisplayTimings)
{
    HRESULT bEscRet;
    BOOLEAN retStatus      = FALSE;
    BOOLEAN bTargetIdFound = FALSE;

    CUI_ESC_CONVERT_RR_RATIONAL_ARGS convertRRrational    = { 0 };
    ACTIVE_DISPLAY_CONFIG            currentDisplayConfig = { 0 };

    CUI_ESC_TOPOLOGY  topology = { 0 };
    CUI_ESC_PATH_INFO pathInfo = { 0 };
    CUI_ESC_MODE_INFO modeInfo = { 0 };

    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    BOOLEAN               adapterStatus      = FALSE;

    do
    {
        if (pDisplayMode == NULL || pDisplayTimings == NULL)
        {
            ERROR_LOG("Function Parameter {pDisplayMode} or {pDisplayTimings} is NULL");
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_INVALID_PARAMETER;
            break;
        }

        ZeroMemory(pDisplayTimings, sizeof(RR_RATIONAL_INFO));
        GetActiveDisplayConfiguration(&currentDisplayConfig);

        topology.numOfPaths             = 1;
        topology.ignoreUnsupportedModes = 1;

        for (INT numDisplay = 0; numDisplay < currentDisplayConfig.numberOfDisplays; numDisplay++)
        {
            if ((currentDisplayConfig.displayInfo[numDisplay].targetId == pDisplayMode->panelInfo.targetID) &&
                (wcscmp(currentDisplayConfig.displayInfo[numDisplay].panelInfo.gfxAdapter.busDeviceID, pDisplayMode->panelInfo.gfxAdapter.busDeviceID) == S_OK) &&
                (wcscmp(currentDisplayConfig.displayInfo[numDisplay].panelInfo.gfxAdapter.deviceInstanceID, pDisplayMode->panelInfo.gfxAdapter.deviceInstanceID) == S_OK))
            {
                bTargetIdFound = TRUE;

                ZeroMemory(&pathInfo, sizeof(CUI_ESC_PATH_INFO));
                pathInfo.targetID      = pDisplayMode->panelInfo.targetID;
                pathInfo.sourceID      = pDisplayMode->panelInfo.sourceID;
                pathInfo.eModeInfoType = CUI_ESC_MODE_PINNED;

                modeInfo.sourceX                            = pDisplayMode->HzRes;
                modeInfo.sourceY                            = pDisplayMode->VtRes;
                modeInfo.colorBPP                           = (pDisplayMode->BPP * 8);
                modeInfo.eScanLineOrder                     = pDisplayMode->scanlineOrdering;
                modeInfo.refreshRate                        = pDisplayMode->refreshRate;
                modeInfo.stCurrentCompensation.compensation = pDisplayMode->scaling;

                pathInfo.stModeInfo          = modeInfo;
                topology.stPathInfo[0]       = pathInfo;
                convertRRrational.stTopology = topology;
            }
        }

        if (bTargetIdFound == FALSE)
        {
            ERROR_LOG("Given TargetId: %lu NOT Found in current display config", pDisplayMode->panelInfo.targetID);
        }

        retStatus = LegacyGetTargetTimings(&pDisplayMode->panelInfo, &convertRRrational);
        if (TRUE == retStatus)
        {
            CopyMemory(pDisplayTimings, &convertRRrational.stRR_RationalInfo, sizeof(CUI_ESC_RR_RATIONAL_INFO));
        }
    } while (FALSE);

    return retStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                       GetOSPrefferedMode (Exposed API)
 * Description:                 This function is used to get Preffered Mode from OS for given Target ID.
 * @param PPANEL_INFO           (_In_   PPANEL_INFO Target ID and Adapter Information of the Respective Display)
 * @param PDISPLAY_TIMINGS      (_Out_  Output DISPLAY_TIMINGS Structure)
 * return: BOOLEAN              Returns True if it is Success else False.
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetOSPrefferedMode(_In_ PPANEL_INFO pPanelInfo, _Out_ PDISPLAY_TIMINGS pDisplayTimings)
{
    BOOLEAN                             retStatus = FALSE;
    LONG                                status    = 0;
    ULONGLONG                           mod_target_id;
    DISPLAYCONFIG_TARGET_PREFERRED_MODE preferredmodeInfo;
    BOOLEAN                             adapterStatus      = FALSE;
    ADAPTER_INFO_GDI_NAME               adapterInfoGdiName = { 0 };

    do
    {
        if (pDisplayTimings == NULL)
        {
            ERROR_LOG("pDisplayTimings of PDISPLAY_TIMINGS Structure is NULL.");
            break;
        }
        adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
        // Getting AdapterID and ViewGDIDeviceName based on AdapterInfo.
        adapterStatus = GetAdapterDetails(&adapterInfoGdiName);
        if (adapterStatus == FALSE)
        {
            ERROR_LOG("{GetAdapterDetails} for Given Adapter Information.");
            pDisplayTimings->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
            break;
        }
        ZeroMemory(&preferredmodeInfo, sizeof(DISPLAYCONFIG_TARGET_PREFERRED_MODE));
        preferredmodeInfo.header.size      = sizeof(DISPLAYCONFIG_TARGET_PREFERRED_MODE);
        preferredmodeInfo.header.id        = pPanelInfo->targetID;
        preferredmodeInfo.header.adapterId = adapterInfoGdiName.adapterID;
        preferredmodeInfo.header.type      = DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_PREFERRED_MODE;

        status = DisplayConfigGetDeviceInfo(&preferredmodeInfo.header);
        if (status == ERROR_SUCCESS)
        {
            pDisplayTimings->targetId         = pPanelInfo->targetID;
            pDisplayTimings->hActive          = preferredmodeInfo.targetMode.targetVideoSignalInfo.activeSize.cx;
            pDisplayTimings->vActive          = preferredmodeInfo.targetMode.targetVideoSignalInfo.activeSize.cy;
            pDisplayTimings->hTotal           = preferredmodeInfo.targetMode.targetVideoSignalInfo.totalSize.cx;
            pDisplayTimings->vTotal           = preferredmodeInfo.targetMode.targetVideoSignalInfo.totalSize.cy;
            pDisplayTimings->hSyncNumerator   = preferredmodeInfo.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator;
            pDisplayTimings->hSyncDenominator = preferredmodeInfo.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator;
            pDisplayTimings->vSyncNumerator   = preferredmodeInfo.targetMode.targetVideoSignalInfo.vSyncFreq.Numerator;
            pDisplayTimings->vSyncDenominator = preferredmodeInfo.targetMode.targetVideoSignalInfo.vSyncFreq.Denominator;
            pDisplayTimings->targetPixelRate  = preferredmodeInfo.targetMode.targetVideoSignalInfo.pixelRate;
            pDisplayTimings->scanLineOrdering = preferredmodeInfo.targetMode.targetVideoSignalInfo.scanLineOrdering;

            float rr                     = (FLOAT)pDisplayTimings->vSyncNumerator / pDisplayTimings->vSyncDenominator;
            pDisplayTimings->refreshRate = RefreshRateRoundOff(rr);
            DEBUG_LOG("Target 0x{%X}, Active: {%lu}x{%lu}, Total: {%lu}x{%lu}, Computed RR: %f, Rounded RR: %lu", pPanelInfo->targetID, pDisplayTimings->hActive,
                      pDisplayTimings->vActive, pDisplayTimings->hTotal, pDisplayTimings->vTotal, rr, pDisplayTimings->refreshRate);

            pDisplayTimings->isPrefferedMode = TRUE;
            pDisplayTimings->status          = DISPLAY_CONFIG_ERROR_SUCCESS;
            retStatus                        = TRUE;
        }
        else
            ERROR_LOG("Failed to get preferred mode with Error Code: %d", status);
    } while (FALSE);

    return retStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   GetDisplayTimings (Exposed API)
 * Description:             This function is used to get Display Timing for given DisplayMode.
 * @param PDISPLAY_MODE     (_In_   Pointer to Requested Display Mode)
 * @param PDISPLAY_TIMINGS  (_Out_  Pointer to Output Display Timing Structure)
 * return: VOID             (Though function returns VOID, output parameter (PDISPLAY_TIMINGS) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID GetDisplayTimings(_In_ PDISPLAY_MODE pCurrentMode, _Out_ PDISPLAY_TIMINGS pDisplayTimings)
{

    BOOLEAN               status = FALSE;
    UINT                  isOSPreferredMode;
    DISPLAY_TIMINGS       display_timing_info = { 0 };
    BOOLEAN               adapterStatus       = FALSE;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName  = { 0 };

    do
    {
        adapterInfoGdiName.adapterInfo = pCurrentMode->panelInfo.gfxAdapter;
        // Getting AdapterID and ViewGDIDeviceName based on AdapterInfo.
        adapterStatus = GetAdapterDetails(&adapterInfoGdiName);
        if (adapterStatus == FALSE)
        {
            ERROR_LOG("{GetAdapterDetails} for Given Adapter Information.");
            pDisplayTimings->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
            break;
        }
        DRIVER_TYPE driverBranch = GetDriverType(adapterInfoGdiName);

        // Step1: Get DisplayHWTiming based on the requested X,Y,RR and Scanline.
        if (driverBranch == YANGRA_DRIVER)
        {
            status = GetDisplayHWTimingYangra(*pCurrentMode, &adapterInfoGdiName, &display_timing_info, &isOSPreferredMode);
        }
        else if (driverBranch == LEGACY_DRIVER)
        {
            status = GetDisplayHWTimingLegacy(*pCurrentMode, &display_timing_info, &isOSPreferredMode);
        }
        else
        {
            pDisplayTimings->status = DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED;
            ERROR_LOG("FAILED: Driver ESC to get driver type Failed / Third Party Gfx driver.");
            break;
        }

        if (status == TRUE)
        {
            CopyMemory(pDisplayTimings, &display_timing_info, sizeof(DISPLAY_TIMINGS));

            pDisplayTimings->targetId        = pCurrentMode->panelInfo.targetID;
            pDisplayTimings->isPrefferedMode = isOSPreferredMode;
        }
        else
        {

            ERROR_LOG("Get Display Timing DriverESC call Unable to get timing for requested Mode");
            pDisplayTimings->status = DISPLAY_CONFIG_ERROR_QUERY_MODE_FAILED;
        }

    } while (FALSE);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   SetDisplayMode (Exposed API)
 * Description:             This function is used to set Display Mode.
 * @param PDISPLAY_MODE     (_In_   Pointer to Requested Display Mode)
 * @param BOOLEAN           (_Out_  Flag to specify which scalar to enable PLANE (FLAG: TRUE) or PIPE)
 * @param INT               (_Out_  Time (In Milliseconds) to wait before and after calling SDC API)
 * @param BOOLEAN           (_In_   Flag to specify optimization is required or not while setting display mode)
 * return: VOID             (Though function returns VOID, output parameter (PDISPLAY_TIMINGS) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID SetDisplayMode(_Inout_ PDISPLAY_MODE pDisplayMode, _In_ BOOLEAN virtualModeSetAware, _In_ INT sdcDelayInMills, _In_ BOOLEAN force_modeset)
{
    LONG    ret;
    BOOLEAN bStatus = TRUE;
    INT     pIsOSPreferredMode;
    INT     path_index      = -1;
    INT     impactedPaths   = 0;
    INT     extendPathCount = 0;
    INT     div             = 10;

    UINT32 flags;
    UINT32 numPathArrayElements;
    UINT32 numModeInfoArrayElements;
    UINT32 sourceModeIndex                           = -1;
    UINT32 targetModeIndex                           = -1;
    UINT32 desktopImageInfoIndex                     = -1;
    UINT32 impactedTargetIds[MAX_SUPPORTED_DISPLAYS] = { 0 };
    UINT32 ExtendedTargetIds[MAX_SUPPORTED_DISPLAYS] = { 0 };

    /* Saving Input targetId separetly since pDisplayMode.targetId will be modified if Config is clone.*/
    UINT32 targetID                 = pDisplayMode->panelInfo.targetID;
    UINT32 impactedExtendedtargetid = 0;

    DISPLAYCONFIG_PATH_INFO *pSDCPathInfoArray  = NULL;
    DISPLAYCONFIG_MODE_INFO *pSDCModeInfoArray  = NULL;
    ACTIVE_DISPLAY_CONFIG    active_config      = { 0 };
    DISPLAY_TIMINGS          targetTimingInfo   = { 0 };
    BOOLEAN                  adapterStatus      = FALSE;
    ADAPTER_INFO_GDI_NAME    adapterInfoGdiName = { 0 };

    do
    {

        if (NULL == pDisplayMode)
        {
            ERROR_LOG("DISPLAY_MODE Object pDisplayMode is NULL.");
            break;
        }

        // From Win10 onwards driver supports VirtualMode, Hence Setting both ACTIVE and VIRTUALMODE flags
        flags = GetDisplayConfigFlags(QDC_ACTIVE_PATHS);

        // Get Path Array buffer size and Mode array buffer size through OS API.
        ret = GetDisplayConfigBufferSizes(flags, &numPathArrayElements, &numModeInfoArrayElements);

        if (ret != ERROR_SUCCESS)
        {
            ERROR_LOG("Get DisplayConfig Buffer Sizes Failed.");
            pDisplayMode->status = DisplayConfigErrorCode(ret);
            break;
        }

        // Allocate Buffer for SetDisplayConfig based on ModeArraySize and PathArraySize
        pSDCPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, (sizeof(DISPLAYCONFIG_PATH_INFO)));
        pSDCModeInfoArray = (DISPLAYCONFIG_MODE_INFO *)calloc(numModeInfoArrayElements, (sizeof(DISPLAYCONFIG_MODE_INFO)));

        if (pSDCPathInfoArray == NULL || pSDCModeInfoArray == NULL)
        {
            ERROR_LOG("Memory Allocation for Path Array/ Mode Array Failed.");
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            break;
        }

        /* Windows API which retrieves information about all possible display paths which are active */
        ret = QueryDisplayConfig(flags, &numPathArrayElements, pSDCPathInfoArray, &numModeInfoArrayElements, pSDCModeInfoArray, NULL);

        if (ERROR_SUCCESS != ret)
        {
            ERROR_LOG("QueryDisplayConfig Failed with return code: %d.", ret);
            pDisplayMode->status = DisplayConfigErrorCode(ret);
            break;
        }

        /* Get Active Display config, because if requested Target id is part of CLONE config need to modify those Path as well */
        GetActiveDisplayConfiguration(&active_config);

        if (active_config.status != DISPLAY_CONFIG_ERROR_SUCCESS)
        {
            ERROR_LOG("Get ActiveDisplayConfiguration Failed with return code: %d.", active_config.status);
            pDisplayMode->status = active_config.status;
            break;
        }

        for (INT path_index = 0; path_index < active_config.numberOfDisplays; path_index++)
        {
            if ((active_config.displayInfo[path_index].targetId == pDisplayMode->panelInfo.targetID) &&
                (wcscmp(active_config.displayInfo[path_index].panelInfo.gfxAdapter.busDeviceID, pDisplayMode->panelInfo.gfxAdapter.busDeviceID) == S_OK) &&
                (wcscmp(active_config.displayInfo[path_index].panelInfo.gfxAdapter.deviceInstanceID, pDisplayMode->panelInfo.gfxAdapter.deviceInstanceID) == S_OK))
            {
                impactedPaths        = active_config.displayInfo[path_index].cloneGroupCount;
                impactedTargetIds[0] = active_config.displayInfo[path_index].targetId;
                for (INT index = 1; index <= impactedPaths; index++)
                {
                    impactedTargetIds[index] = active_config.displayInfo[path_index].cloneGroupTargetIds[index - 1];
                    extendPathCount          = active_config.displayInfo[path_index].extendedGroupCount;
                    if (extendPathCount >= 1)
                    {
                        ExtendedTargetIds[index - 1] = active_config.displayInfo[path_index].extendedGroupTargetIds[index - 1];
                    }
                }
                impactedPaths++;
            }
        }

        for (INT targetId_index = 0; targetId_index < impactedPaths; targetId_index++)
        {
            pDisplayMode->panelInfo.targetID = impactedTargetIds[targetId_index];
            adapterInfoGdiName.adapterInfo   = pDisplayMode->panelInfo.gfxAdapter;
            // Getting AdapterID and ViewGDIDeviceName based on AdapterInfo.
            adapterStatus = GetAdapterDetails(&adapterInfoGdiName);
            if (adapterStatus == FALSE)
            {
                ERROR_LOG("{GetAdapterDetails} forr Given Adapter Information.");
                pDisplayMode->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
                bStatus              = FALSE;
                break;
            }

            DRIVER_TYPE driverBranch = GetDriverType(adapterInfoGdiName);

            // Step1: Get DisplayHWTiming based on the requested X,Y,RR and Scanline.
            if (driverBranch == YANGRA_DRIVER)
            {
                bStatus = GetDisplayHWTimingYangra(*pDisplayMode, &adapterInfoGdiName, &targetTimingInfo, &pIsOSPreferredMode);
            }
            else if (driverBranch == LEGACY_DRIVER)
            {
                bStatus = GetDisplayHWTimingLegacy(*pDisplayMode, &targetTimingInfo, &pIsOSPreferredMode);
                // Setting to 1 to avoid division by 10 again, since division is not required for legacy platforms
                div = 1;
            }

            // For 3rd party GFX we can't get timings for any Mode(Except Native). So Using Native Timings to set modes for 3rd party GFX.
            else if (driverBranch == DRIVER_UNKNOWN)
            {
                bStatus = GetOSPrefferedMode(&pDisplayMode->panelInfo, &targetTimingInfo);
            }
            else
            {
                ERROR_LOG("{GetDriverType} for Given Adapter Info / Maybe a Third Party Gfx driver.");
                pDisplayMode->status = DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED;
                bStatus              = FALSE;
                break;
            }

            // Unable to Get HW timing from Driver - We might be in Clone Configuration and Requested mode may not be available in in driver mode list
            // Hence get OS preffered mode and proceed ( but we need to Make sure - Target Id is part of Clone Configuration , Due to Clone Behaviour in Win 10+ RS3 )
            if (bStatus == FALSE && impactedPaths >= 2)
            {
                INFO_LOG("Failed to get target timing from driver. Retrying with OS API.");
                bStatus = GetOSPrefferedMode(&pDisplayMode->panelInfo, &targetTimingInfo);
                // Setting to 1 to avoid division by 10 again, since OS is already keeping track of proper data from driver
                div = 1;
            }

            if (bStatus == FALSE)
            {
                ERROR_LOG("GetDisplayHWTiming Failed.");
                pDisplayMode->status = DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED;
                break;
            }

            for (path_index = 0; path_index < numPathArrayElements; path_index++)
            {
                if (pSDCPathInfoArray[path_index].targetInfo.id == pDisplayMode->panelInfo.targetID)
                {
                    targetModeIndex       = pSDCPathInfoArray[path_index].targetInfo.targetModeInfoIdx;  // ModeInfoArray Index where Target Details to be filled
                    sourceModeIndex       = pSDCPathInfoArray[path_index].sourceInfo.sourceModeInfoIdx;  // ModeInfoArray Index where Source Details to be filled
                    desktopImageInfoIndex = pSDCPathInfoArray[path_index].targetInfo.desktopModeInfoIdx; // ModeInfoArray Index where Desktop ImageInfo Details to be filled
                    break;
                }
            }

            pSDCPathInfoArray[path_index].targetInfo.rotation = pDisplayMode->rotation;
            pSDCPathInfoArray[path_index].flags               = pDisplayMode->rrMode == DYNAMIC_RR ? (pSDCPathInfoArray[path_index].flags | DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE) :
                                                                                       (pSDCPathInfoArray[path_index].flags & ~(DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE));

            // Fill the passed refresh rate in case of dynamic RR
            if (pDisplayMode->rrMode == DYNAMIC_RR)
            {
                pSDCPathInfoArray[path_index].targetInfo.refreshRate.Numerator   = pDisplayMode->refreshRate;
                pSDCPathInfoArray[path_index].targetInfo.refreshRate.Denominator = 1;
            }

            // Fill the timing paramaters in case of physical mode to be set - Legacy
            else
            {
                pSDCPathInfoArray[path_index].targetInfo.refreshRate.Numerator   = targetTimingInfo.vSyncNumerator / div;
                pSDCPathInfoArray[path_index].targetInfo.refreshRate.Denominator = targetTimingInfo.vSyncDenominator / div;
            }

            // Fill Source Mode Information
            pSDCModeInfoArray[sourceModeIndex].sourceMode.width  = pDisplayMode->HzRes;
            pSDCModeInfoArray[sourceModeIndex].sourceMode.height = pDisplayMode->VtRes;

            // Fill Target Mode Information
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.activeSize.cx         = targetTimingInfo.hActive;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.activeSize.cy         = targetTimingInfo.vActive;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.pixelRate             = targetTimingInfo.targetPixelRate;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.hSyncFreq.Numerator   = targetTimingInfo.hSyncNumerator / div;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = targetTimingInfo.hSyncDenominator / div;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.vSyncFreq.Numerator   = targetTimingInfo.vSyncNumerator / div;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.vSyncFreq.Denominator = targetTimingInfo.vSyncDenominator / div;

            // Fill Scanline Information
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.scanLineOrdering = targetTimingInfo.scanLineOrdering;
            pSDCPathInfoArray[path_index].targetInfo.scanLineOrdering                            = targetTimingInfo.scanLineOrdering;

            // Fill Scaling Information
            if (pDisplayMode->HzRes == targetTimingInfo.hActive && pDisplayMode->VtRes == targetTimingInfo.vActive)
            {
                // Physical ModeSet (MDS Scaling)
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize.x = targetTimingInfo.hActive;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize.y = targetTimingInfo.vActive;

                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.left   = 0;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.top    = 0;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.right  = targetTimingInfo.hActive;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.bottom = targetTimingInfo.vActive;

                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageRegion = pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip;

                pSDCPathInfoArray[path_index].targetInfo.scaling = DISPLAYCONFIG_SCALING_IDENTITY;
            }
            else
            {
                // Virtual ModeSet
                DISPLAYCONFIG_SCALING scaling;
                RECTL                 rDesktopImageRegion = { 0 };
                POINTL                sourceXY            = { 0 };
                POINTL                targetXY            = { 0 };

                sourceXY.x = pDisplayMode->HzRes;
                sourceXY.y = pDisplayMode->VtRes;
                targetXY.x = targetTimingInfo.hActive;
                targetXY.y = targetTimingInfo.vActive;

                /* virtualModeSetAware is FALSE, enable PIPE Scalar else PLANE Scalar.
                For PIPE Scalar Desktop PathSourceSize, DesktopImageClip and DesktopImageRegion should be same as Source Mode */
                if (virtualModeSetAware == FALSE)
                {
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize = sourceXY;
                }
                else
                {
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize = targetXY;
                }

                // 'DesktopImageClip' Size Value will be always equal to Source Mode
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.left   = 0;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.top    = 0;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.right  = sourceXY.x;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.bottom = sourceXY.y;

                // Compute Scaling Values for Requested scaling.
                bStatus = ComputeScalingData(virtualModeSetAware, pDisplayMode->scaling, &sourceXY, &targetXY, &rDesktopImageRegion, &scaling);

                // Assign Computed Scaling Data to DesktopImageInfo Structure's DesktopImageRegion Member.
                if (bStatus == TRUE)
                {
                    pSDCPathInfoArray[path_index].targetInfo.scaling                             = scaling;
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageRegion = rDesktopImageRegion;
                }
            }
        } // END of ImpactedtargetIDs Loop

        // Below Loop executed on Hybrid Configuration
        for (INT targetId_index = 0; targetId_index < extendPathCount; targetId_index++)
        {
            impactedExtendedtargetid = ExtendedTargetIds[targetId_index];
            for (path_index = 0; path_index < numPathArrayElements; path_index++)
            {
                if (pSDCPathInfoArray[path_index].targetInfo.id == impactedExtendedtargetid)
                {
                    sourceModeIndex = pSDCPathInfoArray[path_index].sourceInfo.sourceModeInfoIdx; // ModeInfoArray Index where Source Details to be filled
                    pSDCModeInfoArray[sourceModeIndex].sourceMode.position.x = pDisplayMode->HzRes;
                    break;
                }
            }
        } // END of ImpactedExtendedtargetID's Loop
        // Below assignment is needed mainly when we have clone configuration ( Since we would have touched other path as well)
        pDisplayMode->panelInfo.targetID = targetID;

        DEBUG_LOG("Requested mode - Target:{%lu}, {%lu}x{%lu}@{%lu} Hz with clock:{%lu} Hz. Rotation:{%d}, Scaling:{%d}, BPP:{%d}, Scanline:{%d}, Sampling:{%d}, PortType:{%d}, "
                  "GfxIndex:{%ls}",
                  pDisplayMode->targetId, pDisplayMode->HzRes, pDisplayMode->VtRes, pDisplayMode->refreshRate, pDisplayMode->pixelClock_Hz, pDisplayMode->rotation,
                  pDisplayMode->scaling, pDisplayMode->BPP, pDisplayMode->scanlineOrdering, pDisplayMode->samplingMode, pDisplayMode->panelInfo.ConnectorNPortType,
                  pDisplayMode->panelInfo.gfxAdapter.gfxIndex);
        if (bStatus == TRUE)
        {
            flags = (force_modeset == TRUE) ? GetDisplayConfigFlags(SDC_FLAGS_WITHOUT_OPTIMIZATION) : GetDisplayConfigFlags(SDC_FLAGS);

            Sleep(sdcDelayInMills / 3); // WA: This wait is added to overcome Mode Set failure while switching from Interlaced to Progress or ViceVersa.
            ret = SetDisplayConfig(numPathArrayElements, pSDCPathInfoArray, numModeInfoArrayElements, pSDCModeInfoArray, flags);
            if (ret == ERROR_SUCCESS)
            {
                DISPLAY_MODE currentMode;
                for (INT interval = 100; interval <= sdcDelayInMills; interval += 100)
                {
                    Sleep(100); // polling interval
                    GetCurrentMode(&pDisplayMode->panelInfo, &currentMode);

                    if (pDisplayMode->HzRes == currentMode.HzRes && pDisplayMode->VtRes == currentMode.VtRes && pDisplayMode->scanlineOrdering == currentMode.scanlineOrdering &&
                        pDisplayMode->rotation == currentMode.rotation && pDisplayMode->scaling == currentMode.scaling)
                    {
                        if (pDisplayMode->refreshRate == currentMode.refreshRate)
                        {
                            pDisplayMode->status = DISPLAY_CONFIG_ERROR_SUCCESS;
                        }
                        else
                        {
                            INFO_LOG("Display Mode Set Success with RR Mismatch WA ( Fix - TBD from Driver).");
                            pDisplayMode->status = DISPLAY_CONFIG_ERROR_SUCCUESS_RR_MISMATCH;
                        }
                        break;
                    }
                    else if (interval == sdcDelayInMills)
                    {
                        // Timeout condition
                        ERROR_LOG("After Mode Set, Verification failed with timeout.");
                        pDisplayMode->status = DISPLAY_CONFIG_ERROR_MODE_VERIFICATION_FAILED;
                    }
                }
            }
            else
            {
                ERROR_LOG("Set Display Mode Failed with Error Code: 0x%X.", ret);
                PrintDisplayInfo("SetDisplayMode() failed", numPathArrayElements, pSDCPathInfoArray, numModeInfoArrayElements, pSDCModeInfoArray);
                pDisplayMode->status = DisplayConfigErrorCode(ret);
            }
        }

    } while (FALSE);

    /* cleanup dynamically allocated memory */
    free(pSDCPathInfoArray);
    free(pSDCModeInfoArray);

    int value = GetGfxIndexValue(pDisplayMode->panelInfo.gfxAdapter.gfxIndex);
    EtwSetMode(value, pDisplayMode->panelInfo.targetID, pDisplayMode->status, virtualModeSetAware, pDisplayMode->HzRes, pDisplayMode->VtRes, pDisplayMode->refreshRate,
               pDisplayMode->scaling, pDisplayMode->rotation, pDisplayMode->scanlineOrdering, pDisplayMode->BPP, pDisplayMode->pixelClock_Hz, pDisplayMode->rrMode);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                       ComputeScalingData (Internal API)
 * Description:                 This function is used to compute scaling value for PLANE Scalar based on Input Scaling.
 * @param BOOLEAN               (_In_  virtualModeSetAware - If FALSE, PIPE will be enabled)
 * @param SCALING               (_In_  Input Scaling)
 * @param PPOINTL               (_In_  Pointer to Source XY value)
 * @param PPOINTL               (_In_  Pointer to Target XY value)
 * @param PRECTL                (_In_  Pointer to Image Region)
 * @param DISPLAYCONFIG_SCALING (_In_  Pointer to DISPLAYCONFIG_SCALING structure)
 * return: BOOLEAN              (Returns TRUE if success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN ComputeScalingData(_In_ BOOLEAN virtualModeSetAware, _In_ SCALING inputScaling, _In_ PPOINTL pSourceXY, _In_ PPOINTL pTargetXY, _Out_ PRECTL pImageRegion,
                           _Out_ DISPLAYCONFIG_SCALING *pOSScaling)
{
    BOOLEAN bStatus = TRUE;
    memset(pImageRegion, 0, sizeof(RECTL));

    // If 'virtualModeSetAware' is FALSE, which means PIPE will be enabled. We can set default values for Desktop Image Info, OS will handle enabling requested scaling.
    if (virtualModeSetAware == FALSE)
    {
        pImageRegion->top    = 0;
        pImageRegion->left   = 0;
        pImageRegion->right  = pSourceXY->x;
        pImageRegion->bottom = pSourceXY->y;

        switch (inputScaling)
        {
        case FS:
        case MDS:
            *pOSScaling = DISPLAYCONFIG_SCALING_STRETCHED;
            break;
        case MAR:
            *pOSScaling = DISPLAYCONFIG_SCALING_ASPECTRATIOCENTEREDMAX;
            break;
        case CI:
            *pOSScaling = DISPLAYCONFIG_SCALING_CENTERED;
            break;
        default:
            bStatus = FALSE;
            ERROR_LOG("Requested Scaling {%d} Not Supported.", inputScaling);
            break;
        }
    }
    else
    {
        // For PLANE Scalare Calculate DesktopImageRegion Coordinates based on User requested Scaling
        switch (inputScaling)
        {
        case FS:
        case MDS:
        {
            pImageRegion->top    = 0;
            pImageRegion->left   = 0;
            pImageRegion->right  = pTargetXY->x;
            pImageRegion->bottom = pTargetXY->y;
            *pOSScaling          = DISPLAYCONFIG_SCALING_STRETCHED;
            break;
        }
        case MAR:
        {
            double targetAspectratio = (double)(pTargetXY->x) / (double)(pTargetXY->y);
            double sourceAspectratio = (double)(pSourceXY->x) / (double)(pSourceXY->y);

            if (targetAspectratio < sourceAspectratio)
            {
                INT xCoordinate = pTargetXY->x;
                INT yCoordinate = (INT)((xCoordinate / sourceAspectratio) + 0.5);

                pImageRegion->left   = (pTargetXY->x - xCoordinate) / 2;
                pImageRegion->top    = (pTargetXY->y - yCoordinate) / 2;
                pImageRegion->right  = pTargetXY->x - pImageRegion->left;
                pImageRegion->bottom = pTargetXY->y - pImageRegion->top;
            }
            else if (targetAspectratio > sourceAspectratio)
            {
                INT yCoordinate = pTargetXY->y;
                INT xCoordinate = (INT)((yCoordinate * sourceAspectratio) + 0.5);

                pImageRegion->left   = (pTargetXY->x - xCoordinate) / 2;
                pImageRegion->top    = (pTargetXY->y - yCoordinate) / 2;
                pImageRegion->right  = pTargetXY->x - pImageRegion->left;
                pImageRegion->bottom = pTargetXY->y - pImageRegion->top;
            }
            else
            {
                pImageRegion->top    = 0;
                pImageRegion->left   = 0;
                pImageRegion->right  = pTargetXY->x;
                pImageRegion->bottom = pTargetXY->y;
            }

            *pOSScaling = DISPLAYCONFIG_SCALING_ASPECTRATIOCENTEREDMAX;
            break;
        }
        case CI:
        {
            int left_calc_value = (pTargetXY->x / 2) - (pSourceXY->x / 2);
            int top_calc_value  = (pTargetXY->y / 2) - (pSourceXY->y / 2);

            /* In CLONE Mode, CI scaling request may come for Higher Source XY on Lower Target XY, in those case left or top margin may go outside boundary (Negative Value).
            To handle these scenarios set Left/Top Coordinate to 0 if we get Negative Value during calcualtion*/
            pImageRegion->left = (left_calc_value > 0) ? left_calc_value : 0;
            pImageRegion->top  = (top_calc_value > 0) ? top_calc_value : 0;

            pImageRegion->right  = pTargetXY->x - pImageRegion->left;
            pImageRegion->bottom = pTargetXY->y - pImageRegion->top;

            *pOSScaling = DISPLAYCONFIG_SCALING_CENTERED;
            break;
        }
        default:
            bStatus = FALSE;
            ERROR_LOG("Requested Scaling {%d} Not Supported.", inputScaling);
            break;
        }
    }
    return bStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   GetCurrentMode (Exposed API)
 * Description:             This function is used to get Currently applied Display Mode.
 * @param PPANEL_INFO       (_In_   PPANEL_INFO Target ID and Adapter Information of the Respective Display)
 * @param PDISPLAY_MODE     (_Out_  Pointer to Output Display Mode Structure)
 * return: VOID             (Though function returns VOID, output parameter (DISPLAY_MODE) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID GetCurrentMode(_In_ PPANEL_INFO pPanelInfo, _Out_ PDISPLAY_MODE pDisplayMode)
{
    LONG   status;
    INT    path_index = -1;
    INT    div        = 10;
    UINT32 flags;
    UINT32 numPathArrayElements;
    UINT32 numModeInfoArrayElements;
    UINT32 sourceModeIndex       = -1;
    UINT32 targetModeIndex       = -1;
    UINT32 desktopImageInfoIndex = -1;

    DISPLAYCONFIG_TOPOLOGY_ID CurrentTopology;
    DISPLAYCONFIG_PATH_INFO * pQDCPathInfoArray  = NULL;
    DISPLAYCONFIG_MODE_INFO * pQDCModeInfoArray  = NULL;
    ADAPTER_INFO_GDI_NAME     adapterInfoGdiName = { 0 };
    BOOLEAN                   adapterStatus      = FALSE;

    do
    {
        if (pDisplayMode == NULL)
        {
            ERROR_LOG("DISPLAY_MODE Object {pDisplayMode} is NULL.");
            break;
        }

        // From Win10 onwards driver supports VirtualMode, Hence Setting both ACTIVE and VIRTUALMODE flags
        flags = GetDisplayConfigFlags(QDC_FLAGS);

        // Get Path Array buffer size and Mode array buffer size through OS API.
        status = GetDisplayConfigBufferSizes(flags, &numPathArrayElements, &numModeInfoArrayElements);

        if (status != ERROR_SUCCESS)
        {
            ERROR_LOG("Get DisplayConfig Buffer Sizes Failed.");
            pDisplayMode->status = DisplayConfigErrorCode(status);
            break;
        }

        // Allocate Buffer for SetDisplayConfig based on ModeArraySize and PathArraySize
        pQDCPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, sizeof(DISPLAYCONFIG_PATH_INFO));
        pQDCModeInfoArray = (DISPLAYCONFIG_MODE_INFO *)calloc(numModeInfoArrayElements, sizeof(DISPLAYCONFIG_MODE_INFO));

        if (pQDCPathInfoArray == NULL || pQDCModeInfoArray == NULL)
        {
            ERROR_LOG("Memory Allocation for Path Array/ Mode Array Failed.");
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            break;
        }

        /* Windows API which retrieves information about all possible display paths which are active */
        status = QueryDisplayConfig(flags, &numPathArrayElements, pQDCPathInfoArray, &numModeInfoArrayElements, pQDCModeInfoArray, &CurrentTopology);
        PrintDisplayInfo("GetCurrentMode()", numPathArrayElements, pQDCPathInfoArray, numModeInfoArrayElements, pQDCModeInfoArray);

        if (ERROR_SUCCESS != status)
        {

            ERROR_LOG("QueryDisplayConfig Failed with return code: %d.", status);
            pDisplayMode->status = DisplayConfigErrorCode(status);
            break;
        }

        for (path_index = 0; path_index < numPathArrayElements; path_index++)
        {
            if (UNMASK_TARGET_ID(pQDCPathInfoArray[path_index].targetInfo.id) == pPanelInfo->targetID)
            {
                // Getting adapterInformation based on SourceID and AdapterID.
                adapterInfoGdiName.adapterID = pQDCPathInfoArray[path_index].targetInfo.adapterId;
                adapterStatus                = GetGfxAdapterInfo(pQDCPathInfoArray[path_index].sourceInfo.id, &adapterInfoGdiName);
                if (adapterStatus == FALSE)
                {

                    ERROR_LOG("{GetGfxAdapterInfo} for given SourceId: %u and AdapterId LowPart: %lu HighPart: %d", pQDCPathInfoArray[path_index].sourceInfo.id,
                              pQDCPathInfoArray[path_index].targetInfo.adapterId.LowPart, pQDCPathInfoArray[path_index].targetInfo.adapterId.HighPart);
                    break;
                }
                if ((wcscmp(pPanelInfo->gfxAdapter.busDeviceID, adapterInfoGdiName.adapterInfo.busDeviceID) == S_OK) &&
                    (wcscmp(pPanelInfo->gfxAdapter.deviceInstanceID, adapterInfoGdiName.adapterInfo.deviceInstanceID) == S_OK))
                {
                    targetModeIndex = pQDCPathInfoArray[path_index].targetInfo.targetModeInfoIdx; // 0
                    sourceModeIndex = pQDCPathInfoArray[path_index].sourceInfo.sourceModeInfoIdx; // 1
                    // In DOD part OS don't give desktopImageInfo data , Hence "desktopModeInfoIdx " remains as "65535" Invalid Index
                    // inspite of using QDC flag as "QDC_VIRTUAL_MODE_AWARE" - Hence for Graceful exit without memory access violation, following check added.
                    if (pQDCPathInfoArray[path_index].targetInfo.desktopModeInfoIdx != DEFAULT_DESKTOPIMAGEINFO_INDEX)
                    {
                        desktopImageInfoIndex = pQDCPathInfoArray[path_index].targetInfo.desktopModeInfoIdx; // 2
                    }
                    break;
                }
            }
        }
        // Getting AdapterID and ViewGDIDeviceName based on AdapterInfo.
        adapterStatus = GetAdapterDetails(&adapterInfoGdiName);
        if (adapterStatus == FALSE)
        {

            ERROR_LOG("To get AdapterId/ViewGdiDeviceName Given Adapter Information.");
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
            break;
        }
        if (targetModeIndex == -1 || sourceModeIndex == -1)
        {

            ERROR_LOG("Target ID: %d not found.", pPanelInfo->targetID);
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_TARGET_INACTIVE;
            break;
        }
        else
        {
            // WA for OS issue: When we apply MDS, scaling is NOT updated properly in CCD database. Hence predicting/assuming scaling as MDS when Source X,Y and Target X,Y are
            // equal.
            if ((pQDCModeInfoArray[sourceModeIndex].sourceMode.width == pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.activeSize.cx) &&
                (pQDCModeInfoArray[sourceModeIndex].sourceMode.height == pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.activeSize.cy))
            {
                pDisplayMode->scaling = MDS;
            }
            else
            {
                pDisplayMode->scaling = TranslateScalingOsToInternal(pQDCPathInfoArray[path_index].targetInfo.scaling);
            }

            pDisplayMode->targetId  = pPanelInfo->targetID;
            pDisplayMode->panelInfo = *pPanelInfo;
            pDisplayMode->BPP       = (PIXELFORMAT)pQDCModeInfoArray[sourceModeIndex].sourceMode.pixelFormat;

            pDisplayMode->rotation = TranslateOrientationInternalToOs(pQDCPathInfoArray[path_index].targetInfo.rotation);

            pDisplayMode->HzRes = pQDCModeInfoArray[sourceModeIndex].sourceMode.width;
            pDisplayMode->VtRes = pQDCModeInfoArray[sourceModeIndex].sourceMode.height;

            DRIVER_TYPE driverBranch = GetDriverType(adapterInfoGdiName);

            if (driverBranch == YANGRA_DRIVER)
            {
                UINT32 rrNumerator          = pQDCPathInfoArray[path_index].targetInfo.refreshRate.Numerator;
                UINT32 rrDenominator        = pQDCPathInfoArray[path_index].targetInfo.refreshRate.Denominator;
                pDisplayMode->refreshRate   = RefreshRateRoundOff((FLOAT)rrNumerator / rrDenominator);
                pDisplayMode->pixelClock_Hz = (UINT64)pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.hSyncFreq.Numerator * div;
                INFO_LOG("pixelClock_Hz = %llu", pDisplayMode->pixelClock_Hz);
                INFO_LOG("RR rounded = %lu, rrNumerator = %lu, rrDenominator = %lu", pDisplayMode->refreshRate, rrNumerator, rrDenominator);

                // If BOOST flag is set in pathInfoArray set rrmode as Dynamic RR
                pDisplayMode->rrMode = ((pQDCPathInfoArray[path_index].flags & DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE) == 0) ? LEGACY_RR : DYNAMIC_RR;
            }
            else if (driverBranch == LEGACY_DRIVER)
            {
                pDisplayMode->pixelClock_Hz = pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.pixelRate;
                pDisplayMode->rrMode        = LEGACY_RR;

                // Since we couldn't match RR RoundOff precision with Legacy driver, getting current applied RR from Driver.
                CUI_ESC_QUERY_COMPENSATION_ARGS queryCurrentConfig = { 0 };

                if (FALSE == LegacyGetCurrentConfig(pPanelInfo, &queryCurrentConfig))
                    break;

                for (int numPath = 0; numPath < queryCurrentConfig.stTopology.numOfPaths; numPath++)
                {
                    if (queryCurrentConfig.stTopology.stPathInfo[numPath].targetID == pPanelInfo->targetID)
                    {
                        pDisplayMode->refreshRate = queryCurrentConfig.stTopology.stPathInfo[numPath].stModeInfo.refreshRate;
                        INFO_LOG("RR rounded = %lu", pDisplayMode->refreshRate);
                        break;
                    }
                }
            }
            // For 3rd Party GFX RR Calculation is same like YANGRA. So here we are using same method.
            else if (driverBranch == DRIVER_UNKNOWN)
            {
                UINT32 rrNumerator        = pQDCPathInfoArray[path_index].targetInfo.refreshRate.Numerator;
                UINT32 rrDenominitor      = pQDCPathInfoArray[path_index].targetInfo.refreshRate.Denominator;
                pDisplayMode->refreshRate = RefreshRateRoundOff((FLOAT)rrNumerator / rrDenominitor);
                pDisplayMode->rrMode      = ((pQDCPathInfoArray[path_index].flags & DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE) == 0) ? LEGACY_RR : DYNAMIC_RR;
                INFO_LOG("RR rounded = %lu", pDisplayMode->refreshRate);
            }
            else
            {

                ERROR_LOG("{GetDriverType} for Given Adapter Information / Maybe a Third Party Gfx driver.");
                pDisplayMode->status = DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED;
                break;
            }

            if (pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.scanLineOrdering == DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED)
            {
                pDisplayMode->scanlineOrdering = INTERLACED;
            }
            else if (pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.scanLineOrdering == DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE)
            {
                pDisplayMode->scanlineOrdering = PROGRESSIVE;
            }
            else
            {
                pDisplayMode->scanlineOrdering = SCANLINE_ORDERING_UNSPECIFIED;
            }
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_SUCCESS;
        }

    } while (FALSE);

    /* cleanup dynamically allocated memory */
    free(pQDCPathInfoArray);
    free(pQDCModeInfoArray);

    int value = GetGfxIndexValue(pDisplayMode->panelInfo.gfxAdapter.gfxIndex);
    EtwGetMode(value, pDisplayMode->panelInfo.targetID, pDisplayMode->status, FALSE, pDisplayMode->HzRes, pDisplayMode->VtRes, pDisplayMode->refreshRate, pDisplayMode->scaling,
               pDisplayMode->rotation, pDisplayMode->scanlineOrdering, pDisplayMode->BPP, pDisplayMode->pixelClock_Hz, pDisplayMode->rrMode);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               PrintDriverModeTable (Exposed API)
 * Description:         This function is used print all Source and its respective Target Modes from Driver Mode Table.
 *                      Currently applicable only for Yangra.
 * @param PPANEL_INFO   (_In_  PPANEL_INFO Target ID and Adapter Information of the Respective Display)
 * return: VOID         (Returns Nothing)
 *----------------------------------------------------------------------------------------------------------*/
VOID PrintDriverModeTable(_In_ PPANEL_INFO pPanelInfo)
{
    INT   computedRoundedRR = 0;
    ULONG vSyncDenominator  = 0;
    FLOAT f_refreshRate     = 0.0;
    char  scanline[12];

    UINT                          numSrcMode = 0;
    UINT                          numTgtMode = 0;
    DD_TIMING_INFO *              pTgtModeTable;
    DD_SOURCE_MODE_INFO *         pSrcModeTable;
    DD_ESC_QUERY_MODE_TABLE_ARGS *pSourceAndTargetModeTableArgs = { 0 };

    ADAPTER_INFO_GDI_NAME        adapterInfoGdiName = { 0 };
    BOOLEAN                      adapterStatus      = FALSE;
    DD_ESC_QUERY_MODE_TABLE_ARGS modeTableArgs      = { 0 };

    do
    {
        adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
        // Getting AdapterID and ViewGDIDeviceName based on AdapterInfo.
        adapterStatus = GetAdapterDetails(&adapterInfoGdiName);
        if (adapterStatus == FALSE)
        {
            ERROR_LOG("{GetAdapterDetails} for Given Adapter Information.");
            break;
        }
        DRIVER_TYPE driverBranch = GetDriverType(adapterInfoGdiName);

        if (driverBranch == YANGRA_DRIVER)
        {
            /* Call QueryDisplayModeTableFromYangraDriver to only NumberOfSourceMode and NumberOfTargetMode */
            modeTableArgs.modeInfo[0].targetID = pPanelInfo->targetID;
            if (FALSE == YangraQueryModeTable(pPanelInfo, &modeTableArgs))
                break;

            /* Allocate Memory based on NumberOfSourceMode and NumberOfTargetMode to fetch complete Source and Target Mode Table */
            pSourceAndTargetModeTableArgs = (DD_ESC_QUERY_MODE_TABLE_ARGS *)calloc(
            1, (sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS) + sizeof(DD_TIMING_INFO) * modeTableArgs.numTgtModes + sizeof(DD_SOURCE_MODE_INFO) * modeTableArgs.numSrcModes));

            pSourceAndTargetModeTableArgs->numSrcModes          = modeTableArgs.numSrcModes;
            pSourceAndTargetModeTableArgs->numTgtModes          = modeTableArgs.numTgtModes;
            pSourceAndTargetModeTableArgs->modeInfo[0].targetID = pPanelInfo->targetID;

            if (FALSE == YangraQueryModeTable(pPanelInfo, pSourceAndTargetModeTableArgs))
                break;

            /* Memory location of Target Mode Table from DD_ESC_QUERY_MODE_TABLE_ARGS*/
            pTgtModeTable = (DD_TIMING_INFO *)DD_VOID_PTR_INC(pSourceAndTargetModeTableArgs, sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS));
            /* Memory location of Source Mode Table from DD_ESC_QUERY_MODE_TABLE_ARGS*/
            pSrcModeTable = (DD_SOURCE_MODE_INFO *)DD_VOID_PTR_INC(pSourceAndTargetModeTableArgs,
                                                                   sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS) + (sizeof(DD_TIMING_INFO) * (pSourceAndTargetModeTableArgs->numTgtModes)));

            // Source Mode Table iteration
            for (INT srcModeCount = 1; srcModeCount <= numSrcMode; srcModeCount++)
            {
                INT numMappedTgtModes = pSrcModeTable->numMappedTgtModes;
                DEBUG_LOG("***********************************Source Mode Index:[%d]***********************************\n", srcModeCount);

                DEBUG_LOG("SourceMode: (%lu x %lu) NumberMappedTarget: %d\n", pSrcModeTable->visibleScreenX, pSrcModeTable->visibleScreenY, numMappedTgtModes);
                // Target Mode Table iteration
                for (INT targetModeCount = 0; targetModeCount < numMappedTgtModes; targetModeCount++)
                {
                    // Check for Scanline and compute corresponding vSyncDenominator.
                    if (pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].isInterlaced)
                    {
                        CopyStr(scanline, _countof(scanline), "INTERLACED");
                        vSyncDenominator =
                        ((pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hTotal) * (pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vTotal)) /
                        2;
                    }
                    else
                    {
                        CopyStr(scanline, _countof(scanline), "PROGRESSIVE");
                        vSyncDenominator =
                        ((pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hTotal) * (pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vTotal));
                    }

                    // Calculate float RR and compute its Rounded Value
                    f_refreshRate     = ((FLOAT)pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock / vSyncDenominator);
                    computedRoundedRR = RefreshRateRoundOff(f_refreshRate);
                    DEBUG_LOG("\t%2d: Mode: (%4d x %4d) RefreshRate: %2d VRoundedRR: %2d Scanline: %12s DotClock: %d", targetModeCount + 1,
                              pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].hActive, pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vActive,
                              computedRoundedRR, pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].vRoundedRR, scanline,
                              pTgtModeTable[pSrcModeTable->mappedTgtModeIndex[targetModeCount]].dotClock);
                }

                // Move Source Mode Pointer to next item
                pSrcModeTable = (DD_SOURCE_MODE_INFO *)DD_VOID_PTR_INC(pSrcModeTable, sizeof(DD_SOURCE_MODE_INFO));
            }

            free(pSourceAndTargetModeTableArgs);
        }
        else
        {
            ERROR_LOG("Printing Driver Mode Table is currently supported only on Yangra");
        }
    } while (FALSE);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           QueryDisplayConfigEx (Exposed API)
 * Description:                     This exposed API will help in getting QueryDisplayConfig data for specified target ID.
 *                                  Refer MSDN for more details : "https://msdn.microsoft.com/en-us/library/windows/hardware/ff569215(v=vs.85).aspx"
 * @param UINT                      (_In_   QDC flag for QueryDisplayConfig)
 * @param PPANEL_INFO               (_In_   PPANEL_INFO Target ID and Adapter Information of the Respective Display)
 * @param PQUERY_DISPLAY_CONFIG     (_Out_  Pointer of QUERY_DISPLAY_CONFIG Structure)
 * return: VOID                     (Though function returns VOID, output parameter (PQUERY_DISPLAY_CONFIG) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID QueryDisplayConfigEx(_In_ UINT qdcFlag, _In_ PPANEL_INFO pPanelInfo, _Out_ PQUERY_DISPLAY_CONFIG pQueryDisplayConfig)
{
    ULONG                     retVal;
    UINT32                    pathArraySize = 0;
    UINT32                    modeArraySize = 0;
    DISPLAYCONFIG_PATH_INFO * PathArray;
    DISPLAYCONFIG_MODE_INFO * ModeArray;
    DISPLAYCONFIG_TOPOLOGY_ID CurrentTopology;
    PANEL_INFO                panelInfo;
    ADAPTER_INFO_GDI_NAME     adapterInfoGdiName = { 0 };
    BOOLEAN                   adapterStatus      = FALSE;

    do
    {

        if (pQueryDisplayConfig == NULL)
        {
            pQueryDisplayConfig->status = DISPLAY_CONFIG_ERROR_INVALID_PARAMETER;
            ERROR_LOG("{pQueryDisplayConfig} is NULL.");
            break;
        }

        ZeroMemory(pQueryDisplayConfig, sizeof(PQUERY_DISPLAY_CONFIG));

        /* Get Path Array buffer size and Mode array buffer size through OS API. */
        retVal = GetDisplayConfigBufferSizes(qdcFlag, &pathArraySize, &modeArraySize);

        if (retVal != ERROR_SUCCESS)
        {
            ERROR_LOG("Get DisplayConfig Buffer Sizes Failed.");
            pQueryDisplayConfig->status = DisplayConfigErrorCode(retVal);
            break;
        }

        PathArray = (DISPLAYCONFIG_PATH_INFO *)calloc(pathArraySize, sizeof(DISPLAYCONFIG_PATH_INFO));
        ModeArray = (DISPLAYCONFIG_MODE_INFO *)calloc(modeArraySize, sizeof(DISPLAYCONFIG_MODE_INFO));

        if (PathArray == NULL || ModeArray == NULL)
        {
            ERROR_LOG("Memory Allocation for Path Array/ Mode Array Failed.");
            pQueryDisplayConfig->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            break;
        }

        retVal = QueryDisplayConfig(qdcFlag, &pathArraySize, PathArray, &modeArraySize, ModeArray, &CurrentTopology);

        pQueryDisplayConfig->status = retVal;

        if (retVal != ERROR_SUCCESS)
        {
            DEBUG_LOG("QueryDisplayConfig Failed with return code: %d.", retVal);
            /* Cleanup dynamically allocated memory */
            free(PathArray);
            free(ModeArray);

            break;
        }

        pQueryDisplayConfig->topology = CurrentTopology;

        for (UINT32 patharrayindex = 0; patharrayindex < pathArraySize; patharrayindex++)
        {
            // Getting adapterInformation based on SourceID and AdapterID.
            adapterInfoGdiName.adapterID = PathArray[patharrayindex].targetInfo.adapterId;
            adapterStatus                = GetGfxAdapterInfo(PathArray[patharrayindex].sourceInfo.id, &adapterInfoGdiName);
            if (adapterStatus != TRUE)
            {
                ERROR_LOG("{GetGfxAdapterInfo} for given SourceId: %u and AdapterId LowPart: %lu HighPart: %d", PathArray[patharrayindex].sourceInfo.id,
                          PathArray[patharrayindex].targetInfo.adapterId.LowPart, PathArray[patharrayindex].targetInfo.adapterId.HighPart);
                break;
            }
            if ((pPanelInfo->targetID == UNMASK_TARGET_ID(PathArray[patharrayindex].targetInfo.id)) &&
                (wcscmp(pPanelInfo->gfxAdapter.deviceID, adapterInfoGdiName.adapterInfo.deviceID) == S_OK) &&
                (wcscmp(pPanelInfo->gfxAdapter.deviceInstanceID, adapterInfoGdiName.adapterInfo.deviceInstanceID) == S_OK))
            {
                pQueryDisplayConfig->targetId           = pPanelInfo->targetID;
                pQueryDisplayConfig->qdcFlag            = PathArray[patharrayindex].flags;
                pQueryDisplayConfig->pathInfo           = PathArray[patharrayindex];
                pQueryDisplayConfig->modeInfoTargetMode = ModeArray[PathArray[patharrayindex].targetInfo.targetModeInfoIdx].targetMode;
                pQueryDisplayConfig->modeInfoSourceMode = ModeArray[PathArray[patharrayindex].sourceInfo.sourceModeInfoIdx].sourceMode;
                // In DOD part OS don't give desktopImageInfo data , Hence "desktopModeInfoIdx " remains as "65535" Invalid Index
                // inspite of using QDC flag as "QDC_VIRTUAL_MODE_AWARE" - Hence for Graceful exit without memory access violation, following check added.
                if (PathArray[patharrayindex].targetInfo.desktopModeInfoIdx != DEFAULT_DESKTOPIMAGEINFO_INDEX)
                {
                    pQueryDisplayConfig->modeInfoDesktopInfo = ModeArray[PathArray[patharrayindex].targetInfo.desktopModeInfoIdx].desktopImageInfo;
                }
                break;
            }
        }
        if (adapterStatus == FALSE)
        {
            pQueryDisplayConfig->status = DISPLAY_CONFIG_ERROR_INVALID_ADAPTER_ID;
            break;
        }

        /* Cleanup dynamically allocated memory */
        free(PathArray);
        free(ModeArray);

    } while (FALSE);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               RefreshRateRoundOff (Internal API)
 * Description:         This Function is used to Round Off Floating RR value
 * @param FLOAT         (_In_   float_rr)
 * return: INT          (Rounded integer RR Value)
 *----------------------------------------------------------------------------------------------------------*/
INT RefreshRateRoundOff(FLOAT float_rr)
{
    /* 59.0-59.5 -->59, 59.5-60.5-->60,  and 59.94-59.97 -->59*/
    INT intPart = (INT)float_rr;
    if (intPart == 23 || intPart == 29 || intPart == 59 || intPart == 119)
    {
        FLOAT decPart = float_rr - intPart;
        if ((decPart >= 0.9345555 && decPart <= 0.9785500) || (decPart >= 0.00000000 && decPart <= 0.5000000))
            return intPart;
        else
            return (INT)ceilf(float_rr);
    }
    else
    {
        FLOAT roundRR, temp = float_rr;
        temp    = (float_rr + 0.0555555);
        temp    = roundf(temp * 100);
        roundRR = (temp) / 100;
        return (int)(roundRR);
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               AddModeToList (Internal API)
 * Description:         Function to add requested mode to link list.
 * @param DISPLAYNODE   (_In_   Double pointer to DISPLAYNODE structure.)
 * @param DISPLAY_MODE  (_In_   Mode information need to be added to list.)
 * return: BOOL         (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOL AddModeToList(_In_ struct DISPLAYNODE **pHeadRef, _In_ DISPLAY_MODE mode)
{
    struct DISPLAYNODE *new_node = (struct DISPLAYNODE *)malloc(sizeof(struct DISPLAYNODE));
    NULL_PTR_CHECK(new_node);

    memset(&new_node->displayMode, 0, sizeof(DISPLAY_MODE));

    new_node->displayMode = mode;
    new_node->next        = (*pHeadRef);
    (*pHeadRef)           = new_node;
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               IsModePresentInList (Internal API)
 * Description:         Function to verify requested DISPLAY_MODE is present in DISPLAYNODE link list.
 * @param DISPLAYNODE   (_In_   Pointer to DISPLAYNODE structure.)
 * @param DISPLAY_MODE  (_In_   Mode information need to be verfied with the list.)
 * return: BOOL         (Returns TRUE on Success else FALSE)
 *----------------------------------------------------------------------------------------------------------*/
BOOL IsModePresentInList(_In_ struct DISPLAYNODE *pHeadRef, _In_ DISPLAY_MODE mode)
{
    BOOL status = FALSE;
    if (NULL == pHeadRef)
        return FALSE;
    while (pHeadRef != NULL)
    {
        if (mode.HzRes == pHeadRef->displayMode.HzRes && mode.VtRes == pHeadRef->displayMode.VtRes && mode.refreshRate == pHeadRef->displayMode.refreshRate &&
            mode.scanlineOrdering == pHeadRef->displayMode.scanlineOrdering && mode.rotation == pHeadRef->displayMode.rotation)
        {
            status = TRUE;
            break;
        }
        pHeadRef = pHeadRef->next;
    }
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               ClearDisplayNode (Internal API)
 * Description:         Function to clear all data from DISPLAYNODE Link list.
 * @param DISPLAYNODE   (_In_   Pointer to DISPLAYNODE structure.)
 * return: VOID         Returns Nothing
 *----------------------------------------------------------------------------------------------------------*/
VOID ClearDisplayNode(_In_ struct DISPLAYNODE *pHeadRef)
{
    while (pHeadRef != NULL)
    {
        struct DISPLAYNODE *temp = pHeadRef;
        pHeadRef                 = pHeadRef->next;
        free(temp);
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               EDSMemoryCleanup (Exposed API)
 * Description:         API for Cleanup dynamically allocated memory during GetAllSupportedModes.
 * @param VOID          Doesn't requires any input parameter
 * return: VOID         Returns Nothing
 *----------------------------------------------------------------------------------------------------------*/
VOID EDSMemoryCleanup(VOID)
{
    if (EDSMemoryCleanUpHelper.pDisplayMode != NULL)
    {
        free(EDSMemoryCleanUpHelper.pDisplayMode);
        EDSMemoryCleanUpHelper.pDisplayMode = NULL;
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               TranslateOrientationOsToInternal (Internal API)
 * Description:         Function to map DEVMODE dmDisplayOrientation to ROTATION.
 * @param DWORD         (_In_   dmDisplayOrientation DEVMODE display orientation)
 * return: ROTATION     (Input parameter's equavalent ROTATION data)
 *----------------------------------------------------------------------------------------------------------*/
ROTATION TranslateOrientationOsToInternal(_In_ DWORD dmDisplayOrientation)
{
    ROTATION rotation = ROTATE_UNSPECIFIED;
    switch (dmDisplayOrientation)
    {
    case DMDO_DEFAULT:
        rotation = ROTATE_0;
        break;
    case DMDO_90:
        rotation = ROTATE_90;
        break;
    case DMDO_180:
        rotation = ROTATE_180;
        break;
    case DMDO_270:
        rotation = ROTATE_270;
        break;
    default:
        break;
    }
    return rotation;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           TranslateOrientationInternalToOs (Internal API)
 * Description:                     Function to map OS Rotation to Framework ROTATION.
 * @param DISPLAYCONFIG_ROTATION    (_In_   DISPLAYCONFIG_ROTATION os display orientation)
 * return: ROTATION                 (Input parameter's equavalent ROTATION data)
 *----------------------------------------------------------------------------------------------------------*/
ROTATION TranslateOrientationInternalToOs(_In_ DISPLAYCONFIG_ROTATION os_rotation)
{
    ROTATION rotation;
    switch (os_rotation)
    {
    case DISPLAYCONFIG_ROTATION_IDENTITY:
        rotation = ROTATE_0;
        break;
    case DISPLAYCONFIG_ROTATION_ROTATE90:
        rotation = ROTATE_90;
        break;
    case DISPLAYCONFIG_ROTATION_ROTATE180:
        rotation = ROTATE_180;
        break;
    case DISPLAYCONFIG_ROTATION_ROTATE270:
        rotation = ROTATE_270;
        break;
    default:
        rotation = ROTATE_UNSPECIFIED;
        break;
    }
    return rotation;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                           TranslateScalingOsToInternal (Internal API)
 * Description:                     Function to map OS defined scaling enum to gfx driver defined scaling type.
 * @param SCALING                   (_In_ OS Scaling (DISPLAYCONFIG_SCALING) data from QDC)
 * return: DISPLAYCONFIG_SCALING    (Input parameter's equavalent SCALING data)
 *----------------------------------------------------------------------------------------------------------*/
SCALING TranslateScalingOsToInternal(DISPLAYCONFIG_SCALING scaling)
{
    SCALING driverScaling = SCALING_NOTSPECIFIED;
    switch (scaling)
    {
    case DISPLAYCONFIG_SCALING_IDENTITY:
        driverScaling = MDS;
        break;
    case DISPLAYCONFIG_SCALING_CENTERED:
        driverScaling = CI;
        break;
    case DISPLAYCONFIG_SCALING_STRETCHED:
        driverScaling = FS;
        break;
    case DISPLAYCONFIG_SCALING_ASPECTRATIOCENTEREDMAX:
        driverScaling = MAR;
        break;
    case DISPLAYCONFIG_SCALING_CUSTOM:
        driverScaling = CAR;
        break;
    default:
        driverScaling = SCALING_NOTSPECIFIED;
        break;
    }
    return driverScaling;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**---------------------------------------------------------------------------------------------------------*
 * @brief                               GetModes (Exposed API)
 * Description:                         This function is used to get all supported Modes with/without Rotation (90,180,270) based on PanelInfo and Rotation Flag.
 * @param PANEL_INFO                    (_Inout_ PANEL_INFO: Target ID and Adapter Information of the Display)
 * @param UINT                          (_In_ rotation_flag: If this flag is set, modes with ROTATION 90, 180, 270 will be added)
 * @param PENUMERATED_DISPLAY_MODES     (_Out_ Return ENUMERATED_DISPLAY_MODES Structure with all supported modes)
 * return: VOID                         (Though function returns VOID, output parameter (ENUMERATED_DISPLAY_MODES) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID GetModes(_Inout_ PANEL_INFO *pPanelInfo, _In_ BOOLEAN rotation_flag, _Out_ PENUMERATED_DISPLAY_MODES pEnumDisplayModes)
{
    INT          count                  = 0;
    UINT         sourceId               = 0;
    INT          numberofSupportedModes = 0;
    BOOLEAN      scaling_query          = FALSE;
    DWORD        dwEdsFlag              = 0;
    DWORD        modeIndex              = 0;
    DEVMODE      devMode;
    WCHAR        displayViewGdiDeviceName[CCHDEVICENAME] = { 0 };
    DISPLAY_MODE displayMode                             = { 0 };

    /* Input Node to stores data from EDS (X, Y, RR and Scanline) */
    struct DISPLAYNODE *eds_input_node = NULL;
    /* Output Node to stores data of EDS with all supported SCALING */
    struct DISPLAYNODE *eds_output_node = NULL;

    do
    {
        if (pEnumDisplayModes == NULL)
        {
            pEnumDisplayModes->status = DISPLAY_CONFIG_ERROR_INVALID_PARAMETER;
            ERROR_LOG("pEnumDisplayModes of ENUMERATED_DISPLAY_MODES Structure is NULL.");
            break;
        }

        if (pEnumDisplayModes->size != sizeof(ENUMERATED_DISPLAY_MODES))
        {
            pEnumDisplayModes->status = DISPLAY_CONFIG_ERROR_SIZE_MISMATCH;
            ERROR_LOG("pEnumDisplayModes Size mismatch. Actual: %d Expected: %d.", pEnumDisplayModes->size, sizeof(ENUMERATED_DISPLAY_MODES));
            break;
        }

        /* Free if EDSMemoryCleanUpHelper, if ENUMERATED_DISPLAY_MODES pointer is available */
        EDSMemoryCleanup();

        ZeroMemory(pEnumDisplayModes, sizeof(ENUMERATED_DISPLAY_MODES));
        pEnumDisplayModes->size = sizeof(ENUMERATED_DISPLAY_MODES);

        //////////////////////////////////////////////////////////////////////////////////////////////////////
        // check below block can be removed

        if (FALSE == GetSourceIdFromPanelInfo(pPanelInfo, &sourceId))
        {
            ERROR_LOG("Unable to get sourceId for panelInfo");
            break;
        }

        if (FALSE == UpdateViewGdiDeviceName(pPanelInfo, sourceId))
        {
            ERROR_LOG("Unable to get ViewGdiDeviceName for panelInfo");
            break;
        }
        else
        {
            CopyWchar(displayViewGdiDeviceName, _countof(displayViewGdiDeviceName), pPanelInfo->viewGdiDeviceName);
        }

        //////////////////////////////////////////////////////////////////////////////////////////////////////
        if (rotation_flag == TRUE)
        {
            INFO_LOG("Rotation Flag is SET. Get all Supported Modes with ROTATE_90, ROTATE_180 and ROTATE_270.");
            dwEdsFlag = EDS_ROTATEDMODE;
        }
        else
        {
            dwEdsFlag = EDS_RAWMODE;
        }

        devMode.dmSize = sizeof(DEVMODE);

        /* The EnumDisplaySettingsEx function retrieves information about one of the graphics modes for a display device.
        To retrieve information for all the graphics modes for a display device, make a series of calls to this function.*/
        // Note: displayViewGdiDeviceName memory gets corrupted after EDS call
        while (EnumDisplaySettingsEx(displayViewGdiDeviceName, modeIndex, &devMode, dwEdsFlag))
        {
            displayMode.targetId         = pPanelInfo->targetID;
            displayMode.panelInfo        = *pPanelInfo;
            displayMode.refreshRate      = (UINT)devMode.dmDisplayFrequency;
            displayMode.scanlineOrdering = (devMode.dmDisplayFlags == 0 ? PROGRESSIVE : INTERLACED);

            /* Windows 8.1 and later can no longer query or set display modes that are less than 32 bits per pixel (bpp) these operations will fail.
            Hence hard coding BPP value as 32BPP.*/
            displayMode.BPP      = PIXELFORMAT_32BPP;
            displayMode.rotation = TranslateOrientationOsToInternal(devMode.dmDisplayOrientation);

            // EDS retuns Inverted X,Y for 90 and 270 degree, hence inverting X,Y (which is requirement for SDC while appling mode).
            if (displayMode.rotation == ROTATE_90 || displayMode.rotation == ROTATE_270)
            {
                displayMode.HzRes = (UINT)devMode.dmPelsHeight;
                displayMode.VtRes = (UINT)devMode.dmPelsWidth;
            }
            else
            {
                displayMode.HzRes = (UINT)devMode.dmPelsWidth;
                displayMode.VtRes = (UINT)devMode.dmPelsHeight;
            }

            if (displayMode.scanlineOrdering == INTERLACED)
            {
                /* For 29i, 59i and 119i display driver enumerate as 59i, 119i and 239i */
                if (displayMode.refreshRate == 29 || displayMode.refreshRate == 59 || displayMode.refreshRate == 119 || displayMode.refreshRate == 239)
                {
                    displayMode.refreshRate = (displayMode.refreshRate * 2) + 1;
                }
                else
                {
                    displayMode.refreshRate = displayMode.refreshRate * 2;
                }
            }

            /* Check for Duplicate X,Y RR, Scanline and Rotation */
            if (IsModePresentInList(eds_input_node, displayMode) == FALSE)
            {
                AddModeToList(&eds_input_node, displayMode);
            }
            modeIndex++;
        }

        /* EDS will report Scaling as "DEFAULT" For both MDS(Maintain Display Scaling ) and MAR ( Maintain Aspect Ratio )
        Hence need to ignore scaling information from EDS,  instead add scaling data according to driver mode table. */
        if (pPanelInfo->driverBranch == YANGRA_DRIVER)
        {
            scaling_query = UpdateScalingInfoForModeTableYangra(pPanelInfo, eds_input_node, &eds_output_node, &numberofSupportedModes);
        }
        else if (pPanelInfo->driverBranch == LEGACY_DRIVER)
        {
            scaling_query = UpdateScalingInfoForModeTableLegacy(pPanelInfo, eds_input_node, &eds_output_node, &numberofSupportedModes);
        }
        else
        {
            INFO_LOG("Given AdapterInfo / Maybe a Third Party Gfx driver.");
            scaling_query = UpdateScalingInfoForModeTable3rdParty(pPanelInfo, eds_input_node, &eds_output_node, &numberofSupportedModes);
        }

        if (scaling_query == TRUE)
        {
            PDISPLAY_MODE pModeList = (PDISPLAY_MODE)calloc(numberofSupportedModes, sizeof(DISPLAY_MODE));

            if (pModeList == NULL)
            {
                pEnumDisplayModes->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
                ERROR_LOG("Memory allocation for pModeList Failed.");
                break;
            }

            struct DISPLAYNODE *temp_node = eds_output_node;

            while (NULL != temp_node)
            {
                pModeList[count] = temp_node->displayMode;
                temp_node        = temp_node->next;
                count++;
            }
            pEnumDisplayModes->noOfSupportedModes = numberofSupportedModes;
            pEnumDisplayModes->pDisplayMode       = pModeList;
            pEnumDisplayModes->status             = DISPLAY_CONFIG_ERROR_SUCCESS;

            /* Store Allocated memory in array list, during cleanup we will free this dynamically allocated memory */
            EDSMemoryCleanUpHelper.noOfSupportedModes = &numberofSupportedModes;
            EDSMemoryCleanUpHelper.pDisplayMode       = pModeList;
        }
        else
        {
            pEnumDisplayModes->noOfSupportedModes = 0;
            pEnumDisplayModes->status             = DISPLAY_CONFIG_ERROR_QUERY_MODE_FAILED;
            ERROR_LOG("Query Driver Mode Table for Adding scaling support Failed.");
        }
    } while (FALSE);

    ClearDisplayNode(eds_output_node);
    ClearDisplayNode(eds_input_node);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   GetMode (Exposed API)
 * Description:             This function is used to get Currently applied Display Mode.
 * @param PPANEL_INFO       (_In_   PPANEL_INFO Target ID and Adapter Information of the Respective Display)
 * @param PDISPLAY_MODE     (_Out_  Pointer to Output Display Mode Structure)
 * return: VOID             (Though function returns VOID, output parameter (DISPLAY_MODE) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID GetMode(_In_ PPANEL_INFO pPanelInfo, _Out_ PDISPLAY_MODE pDisplayMode)
{
    LONG   status;
    INT    path_index = -1;
    UINT32 flags;
    UINT32 numPathArrayElements;
    UINT32 numModeInfoArrayElements;
    UINT32 sourceModeIndex       = -1;
    UINT32 targetModeIndex       = -1;
    UINT32 desktopImageInfoIndex = -1;

    DISPLAYCONFIG_TOPOLOGY_ID CurrentTopology;
    DISPLAYCONFIG_PATH_INFO * pQDCPathInfoArray = NULL;
    DISPLAYCONFIG_MODE_INFO * pQDCModeInfoArray = NULL;

    do
    {
        if (pDisplayMode == NULL)
        {
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_INSUFFICIENT_BUFFER;
            ERROR_LOG("DISPLAY_MODE Object {pDisplayMode} is NULL.");
            break;
        }

        // From Win10 onwards driver supports VirtualMode, Hence Setting both ACTIVE and VIRTUALMODE flags
        flags = GetDisplayConfigFlags(QDC_FLAGS);

        // Get Path Array buffer size and Mode array buffer size through OS API.
        status = GetDisplayConfigBufferSizes(flags, &numPathArrayElements, &numModeInfoArrayElements);

        if (status != ERROR_SUCCESS)
        {
            ERROR_LOG("Get DisplayConfig Buffer Sizes Failed.");
            pDisplayMode->status = DisplayConfigErrorCode(status);
            break;
        }

        // Allocate Buffer for SetDisplayConfig based on ModeArraySize and PathArraySize
        pQDCPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, sizeof(DISPLAYCONFIG_PATH_INFO));
        pQDCModeInfoArray = (DISPLAYCONFIG_MODE_INFO *)calloc(numModeInfoArrayElements, sizeof(DISPLAYCONFIG_MODE_INFO));

        if (pQDCPathInfoArray == NULL || pQDCModeInfoArray == NULL)
        {
            ERROR_LOG("Memory Allocation for Path Array/ Mode Array Failed.");
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            break;
        }

        /* Windows API which retrieves information about all possible display paths which are active */
        status = QueryDisplayConfig(flags, &numPathArrayElements, pQDCPathInfoArray, &numModeInfoArrayElements, pQDCModeInfoArray, &CurrentTopology);

        if (ERROR_SUCCESS != status)
        {
            ERROR_LOG("QueryDisplayConfig Failed with return code: %d.", status);
            pDisplayMode->status = DisplayConfigErrorCode(status);
            break;
        }

        for (path_index = 0; path_index < numPathArrayElements; path_index++)
        {
            if (pPanelInfo->targetID == UNMASK_TARGET_ID(pQDCPathInfoArray[path_index].targetInfo.id) &&
                pPanelInfo->gfxAdapter.adapterLUID.LowPart == pQDCPathInfoArray[path_index].targetInfo.adapterId.LowPart &&
                pPanelInfo->gfxAdapter.adapterLUID.HighPart == pQDCPathInfoArray[path_index].targetInfo.adapterId.HighPart)
            {
                targetModeIndex = pQDCPathInfoArray[path_index].targetInfo.targetModeInfoIdx; // 0
                sourceModeIndex = pQDCPathInfoArray[path_index].sourceInfo.sourceModeInfoIdx; // 1
                // In DOD part OS don't give desktopImageInfo data , Hence "desktopModeInfoIdx " remains as "65535" Invalid Index
                // inspite of using QDC flag as "QDC_VIRTUAL_MODE_AWARE" - Hence for Graceful exit without memory access violation, following check added.
                if (pQDCPathInfoArray[path_index].targetInfo.desktopModeInfoIdx != DEFAULT_DESKTOPIMAGEINFO_INDEX)
                {
                    desktopImageInfoIndex = pQDCPathInfoArray[path_index].targetInfo.desktopModeInfoIdx; // 2
                }
                break;
            }
        }

        if (targetModeIndex == -1 || sourceModeIndex == -1)
        {

            ERROR_LOG("Target ID: %d not found.", pPanelInfo->targetID);
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_TARGET_INACTIVE;
            break;
        }
        else
        {
            // WA for OS issue: When we apply MDS, scaling is NOT updated properly in CCD database. Hence predicting/assuming scaling as MDS when Source X,Y and Target X,Y are
            // equal.
            if ((pQDCModeInfoArray[sourceModeIndex].sourceMode.width == pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.activeSize.cx) &&
                (pQDCModeInfoArray[sourceModeIndex].sourceMode.height == pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.activeSize.cy))
            {
                pDisplayMode->scaling = MDS;
            }
            else
            {
                pDisplayMode->scaling = TranslateScalingOsToInternal(pQDCPathInfoArray[path_index].targetInfo.scaling);
            }

            pDisplayMode->targetId  = pPanelInfo->targetID;
            pDisplayMode->panelInfo = *pPanelInfo;
            pDisplayMode->BPP       = (PIXELFORMAT)pQDCModeInfoArray[sourceModeIndex].sourceMode.pixelFormat;

            pDisplayMode->pixelClock_Hz = pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.pixelRate;
            pDisplayMode->rotation      = TranslateOrientationInternalToOs(pQDCPathInfoArray[path_index].targetInfo.rotation);

            pDisplayMode->HzRes = pQDCModeInfoArray[sourceModeIndex].sourceMode.width;
            pDisplayMode->VtRes = pQDCModeInfoArray[sourceModeIndex].sourceMode.height;

            // For 3rd Party GFX RR Calculation is same like YANGRA. So here we are using same method.
            if (pPanelInfo->driverBranch == YANGRA_DRIVER || pPanelInfo->driverBranch == DRIVER_UNKNOWN)
            {
                UINT32 rrNumerator        = pQDCPathInfoArray[path_index].targetInfo.refreshRate.Numerator;
                UINT32 rrDenominitor      = pQDCPathInfoArray[path_index].targetInfo.refreshRate.Denominator;
                pDisplayMode->refreshRate = RefreshRateRoundOff((FLOAT)rrNumerator / rrDenominitor);
                // If BOOST flag is set in pathInfoArray set rrmode as Dynamic RR
                pDisplayMode->rrMode = ((pQDCPathInfoArray[path_index].flags & DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE) == 0) ? LEGACY_RR : DYNAMIC_RR;
            }
            else if (pPanelInfo->driverBranch == LEGACY_DRIVER)
            {
                pDisplayMode->rrMode = LEGACY_RR;
                // Since we couldn't match RR RoundOff precision with Legacy driver, getting current applied RR from Driver.
                CUI_ESC_QUERY_COMPENSATION_ARGS queryCurrentConfig = { 0 };

                if (FALSE == LegacyGetCurrentConfig(pPanelInfo, &queryCurrentConfig))
                {
                    pDisplayMode->status = DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED;
                    break;
                }

                for (int numPath = 0; numPath < queryCurrentConfig.stTopology.numOfPaths; numPath++)
                {
                    if (queryCurrentConfig.stTopology.stPathInfo[numPath].targetID == pPanelInfo->targetID)
                    {
                        pDisplayMode->refreshRate = queryCurrentConfig.stTopology.stPathInfo[numPath].stModeInfo.refreshRate;
                        break;
                    }
                }
            }

            if (pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.scanLineOrdering == DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED)
            {
                pDisplayMode->scanlineOrdering = INTERLACED;
            }
            else if (pQDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.scanLineOrdering == DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE)
            {
                pDisplayMode->scanlineOrdering = PROGRESSIVE;
            }
            else
            {
                pDisplayMode->scanlineOrdering = SCANLINE_ORDERING_UNSPECIFIED;
            }
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_SUCCESS;
        }

    } while (FALSE);

    /* cleanup dynamically allocated memory */
    free(pQDCPathInfoArray);
    free(pQDCModeInfoArray);

    int value = GetGfxIndexValue(pDisplayMode->panelInfo.gfxAdapter.gfxIndex);
    EtwGetMode(value, pDisplayMode->panelInfo.targetID, pDisplayMode->status, FALSE, pDisplayMode->HzRes, pDisplayMode->VtRes, pDisplayMode->refreshRate, pDisplayMode->scaling,
               pDisplayMode->rotation, pDisplayMode->scanlineOrdering, pDisplayMode->BPP, pDisplayMode->pixelClock_Hz, pDisplayMode->rrMode);
}

BOOLEAN GetPanelPathIndexFromOsPathArray(_In_ DISPLAYCONFIG_PATH_INFO *pSDCPathInfoArray, UINT32 numPathArrayElements, _In_ PANEL_INFO panelInfo, _Out_ PUINT pPathIndex)
{
    BOOLEAN status = FALSE;

    do
    {
        if (pSDCPathInfoArray == NULL)
        {
            ERROR_LOG("pSDCPathInfoArray is NULL.");
            break;
        }

        for (INT index = 0; index < numPathArrayElements; index++)
        {
            if (pSDCPathInfoArray[index].targetInfo.id == panelInfo.targetID && pSDCPathInfoArray[index].targetInfo.adapterId.LowPart == panelInfo.gfxAdapter.adapterLUID.LowPart &&
                pSDCPathInfoArray[index].targetInfo.adapterId.HighPart == panelInfo.gfxAdapter.adapterLUID.HighPart)
            {
                *pPathIndex = index;
                status      = TRUE;
            }
        }

    } while (FALSE);

    if (status == FALSE)
    {
        ERROR_LOG("Unable to find Path Index for targetId: %X", panelInfo.targetID);
    }
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   SetMode (Exposed API)
 * Description:             This function is used to set Display Mode.
 * @param PDISPLAY_MODE     (_In_   Pointer to Requested Display Mode)
 * @param BOOLEAN           (_Out_  Flag to specify which scalar to enable PLANE (FLAG: TRUE) or PIPE)
 * @param INT               (_Out_  Time (In Milliseconds) to wait before and after calling SDC API)
 * @param BOOLEAN           (_In_   Flag to specify optimization is required or not while setting display mode)
 * return: VOID             (Though function returns VOID, output parameter (PDISPLAY_TIMINGS) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID SetMode(_Inout_ PDISPLAY_MODE pDisplayMode, _In_ BOOLEAN virtualModeSetAware, _In_ INT sdcDelayInMills, _In_ BOOLEAN force_modeset)
{
    LONG    ret;
    BOOLEAN bStatus = TRUE;
    INT     pIsOSPreferredMode;
    INT     impactedPathCount = 0;
    INT     extendPathCount   = 0;
    INT     div               = 10;

    UINT32                    flags;
    UINT32                    numPathArrayElements;
    UINT32                    numModeInfoArrayElements;
    UINT32                    currentSourceModeIndex = 0;     // source mode index for panel passed by caller
    DISPLAYCONFIG_SOURCE_MODE currentSourceMode      = { 0 }; // source mode for panel passed by caller

    UINT32     ExtendedPathIds[MAX_SUPPORTED_DISPLAYS]        = { 0 };
    UINT32     ImpactedPathIds[MAX_SUPPORTED_DISPLAYS]        = { 0 };
    PANEL_INFO ImpactedPathsPanelInfo[MAX_SUPPORTED_DISPLAYS] = { 0 };

    DISPLAYCONFIG_PATH_INFO *pSDCPathInfoArray = NULL;
    DISPLAYCONFIG_MODE_INFO *pSDCModeInfoArray = NULL;
    DISPLAY_CONFIG           os_config         = { 0 };
    BOOLEAN                  setConfigFailForBFR = FALSE;

    do
    {
        if (NULL == pDisplayMode)
        {
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_INSUFFICIENT_BUFFER;
            ERROR_LOG("DISPLAY_MODE Object pDisplayMode is NULL.");
            break;
        }

        // From Win10 onwards driver supports VirtualMode, Hence Setting both ACTIVE and VIRTUALMODE flags
        flags = GetDisplayConfigFlags(QDC_ACTIVE_PATHS);

        // Get Path Array buffer size and Mode array buffer size through OS API.
        ret = GetDisplayConfigBufferSizes(flags, &numPathArrayElements, &numModeInfoArrayElements);

        if (ret != ERROR_SUCCESS)
        {
            ERROR_LOG("Get DisplayConfig Buffer Sizes Failed.");
            pDisplayMode->status = DisplayConfigErrorCode(ret);
            break;
        }

        // Allocate Buffer for SetDisplayConfig based on ModeArraySize and PathArraySize
        pSDCPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, (sizeof(DISPLAYCONFIG_PATH_INFO)));
        pSDCModeInfoArray = (DISPLAYCONFIG_MODE_INFO *)calloc(numModeInfoArrayElements, (sizeof(DISPLAYCONFIG_MODE_INFO)));
        if (pSDCPathInfoArray == NULL || pSDCModeInfoArray == NULL)
        {
            ERROR_LOG("Memory Allocation for Path Array/ Mode Array Failed.");
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            break;
        }

        /* Windows API which retrieves information about all possible display paths which are active */
        ret = QueryDisplayConfig(flags, &numPathArrayElements, pSDCPathInfoArray, &numModeInfoArrayElements, pSDCModeInfoArray, NULL);

        if (ERROR_SUCCESS != ret)
        {
            ERROR_LOG("QueryDisplayConfig Failed with return code: %d.", ret);
            pDisplayMode->status = DisplayConfigErrorCode(ret);
            break;
        }

        /* Get Display config, because if requested Target id is part of CLONE config need to modify those Path as well */
        os_config.size = sizeof(DISPLAY_CONFIG);
        GetConfig(&os_config);
        if (os_config.status != DISPLAY_CONFIG_ERROR_SUCCESS)
        {
            ERROR_LOG("GetConfig() Failed with return code: %d.", os_config.status);
            pDisplayMode->status = os_config.status;
            break;
        }

        // This below code maps PathIndexes of OS_Config to pSDCPathInfoArray pathIndexes.
        // For Current Path and All impacted Clone paths, SourceMode and TargetMode should be modified. This is stored in ImpactedPathIds[] and ImpactedPathsPanelInfo[]
        // For Extended path of current path, sourceMode x position to be modified. This is stored in ExtendedPathIds
        for (INT index = 0; index < os_config.numberOfDisplays; index++)
        {
            DISPLAY_PATH_INFO pathInfo  = os_config.displayPathInfo[index];
            PANEL_INFO        panelInfo = pathInfo.panelInfo;
            if (pDisplayMode->panelInfo.targetID == panelInfo.targetID && pDisplayMode->panelInfo.gfxAdapter.adapterLUID.LowPart == panelInfo.gfxAdapter.adapterLUID.LowPart &&
                pDisplayMode->panelInfo.gfxAdapter.adapterLUID.HighPart == panelInfo.gfxAdapter.adapterLUID.HighPart)
            {
                UINT osPathIndex = 0;

                GetPanelPathIndexFromOsPathArray(pSDCPathInfoArray, numPathArrayElements, panelInfo, &osPathIndex);
                ImpactedPathIds[impactedPathCount]        = osPathIndex; // Adding Current path as it should be modified.
                ImpactedPathsPanelInfo[impactedPathCount] = panelInfo;
                impactedPathCount++;

                // Find Clone paths and add it in ImpactedPathIds.
                for (INT index2 = 0; index2 < pathInfo.cloneGroupCount; index2++)
                {
                    UINT       cloneIndex     = pathInfo.cloneGroupPathIds[index2];
                    PANEL_INFO clonePanelInfo = os_config.displayPathInfo[cloneIndex].panelInfo;

                    GetPanelPathIndexFromOsPathArray(pSDCPathInfoArray, numPathArrayElements, clonePanelInfo, &osPathIndex);
                    ImpactedPathIds[impactedPathCount]        = osPathIndex;
                    ImpactedPathsPanelInfo[impactedPathCount] = clonePanelInfo;
                    impactedPathCount++;
                }

                for (INT index2 = 0; index2 < pathInfo.extendedGroupCount; index2++)
                {
                    UINT       extendedIndex     = pathInfo.extendedGroupPathIds[index2];
                    PANEL_INFO extendedPanelInfo = os_config.displayPathInfo[extendedIndex].panelInfo;

                    GetPanelPathIndexFromOsPathArray(pSDCPathInfoArray, numPathArrayElements, extendedPanelInfo, &osPathIndex);
                    ExtendedPathIds[extendPathCount] = osPathIndex;
                    extendPathCount++;
                }
            }
        }

        ReRunToApplyDynamicRR:
            for (INT index = 0; index < impactedPathCount; index++)
            {
                UINT32          sourceModeIndex       = -1;
                UINT32          targetModeIndex       = -1;
                UINT32          desktopImageInfoIndex = -1;
                DISPLAY_TIMINGS targetTimingInfo      = { 0 };

                // Getting Impacted Path to modify path details.
                INT        path_index = ImpactedPathIds[index];
                PANEL_INFO panelInfo  = ImpactedPathsPanelInfo[index];

                DISPLAY_MODE currentDisplayMode = *pDisplayMode;
                currentDisplayMode.panelInfo    = panelInfo;

                targetModeIndex       = pSDCPathInfoArray[path_index].targetInfo.targetModeInfoIdx;  // ModeInfoArray Index where Target Details to be filled
                sourceModeIndex       = pSDCPathInfoArray[path_index].sourceInfo.sourceModeInfoIdx;  // ModeInfoArray Index where Source Details to be filled
                desktopImageInfoIndex = pSDCPathInfoArray[path_index].targetInfo.desktopModeInfoIdx; // ModeInfoArray Index where Desktop ImageInfo Details to be filled

                // Step1: Get DisplayHWTiming based on the requested X,Y,RR and Scanline.
                if (panelInfo.driverBranch == YANGRA_DRIVER)
                {
                    // Getting AdapterID and ViewGDIDeviceName based on AdapterInfo.
                    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
                    adapterInfoGdiName.adapterInfo           = panelInfo.gfxAdapter;
                    adapterInfoGdiName.adapterID             = panelInfo.gfxAdapter.adapterLUID;
                    bStatus                                  = GetDisplayHWTimingYangra(currentDisplayMode, &adapterInfoGdiName, &targetTimingInfo, &pIsOSPreferredMode);
                }
                else if (panelInfo.driverBranch == LEGACY_DRIVER)
                {
                    bStatus = GetDisplayHWTimingLegacy(currentDisplayMode, &targetTimingInfo, &pIsOSPreferredMode);
                    // Setting to 1 to avoid division by 10 again, since division is not required for legacy platforms
                    div = 1;
                }

                // For 3rd party GFX we can't get timings for any Mode(Except Native). So Using Native Timings to set modes for 3rd party GFX.
                else
                {
                    INFO_LOG("Given Adapter Info / Maybe a Third Party Gfx driver. GetOSPrefferedMode()");
                    bStatus = GetOSPrefferedMode(&currentDisplayMode.panelInfo, &targetTimingInfo);
                }

                // Unable to Get HW timing from Driver - We might be in Clone Configuration and Requested mode may not be available in in driver mode list
                // Hence get OS preffered mode and proceed ( but we need to Make sure - Target Id is part of Clone Configuration , Due to Clone Behaviour in Win 10+ RS3 )
                if (bStatus == FALSE && impactedPathCount >= 2)
                {
                    bStatus = GetOSPrefferedMode(&currentDisplayMode.panelInfo, &targetTimingInfo);
                    // Setting to 1 to avoid division by 10 again, since OS is already keeping track of proper data from driver
                    div = 1;
                }

                if (bStatus == FALSE)
                {
                    ERROR_LOG("GetDisplayHWTiming Failed.");
                    pDisplayMode->status = DISPLAY_CONFIG_ERROR_DRIVER_ESCAPE_FAILED;
                    break;
                }

                pSDCPathInfoArray[path_index].targetInfo.rotation = currentDisplayMode.rotation;

                // if Dynamic RR is set to True in passed mode, 3rd bit to be set, else reset to set to static RR mode

                pSDCPathInfoArray[path_index].flags = pDisplayMode->rrMode == DYNAMIC_RR ? (pSDCPathInfoArray[path_index].flags | DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE) :
                                                                                           (pSDCPathInfoArray[path_index].flags & ~(DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE));

                
                // Fill the passed refresh rate in case of dynamic RR
                if (pDisplayMode->rrMode == DYNAMIC_RR)
                {
                    pSDCPathInfoArray[path_index].targetInfo.refreshRate.Numerator = pDisplayMode->refreshRate;
                    pSDCPathInfoArray[path_index].targetInfo.refreshRate.Denominator = 1;
                    pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.vSyncFreq.Numerator = pDisplayMode->pixelClock_Hz / div;
                    pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.vSyncFreq.Denominator = targetTimingInfo.vSyncDenominator / div;
                    if (setConfigFailForBFR == TRUE)
                        pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.vSyncFreq.Denominator = (targetTimingInfo.vSyncDenominator / div) / 2;
                }

                // Fill the timing paramaters in case of physical mode to be set - Legacy
                else
                {
                    pSDCPathInfoArray[path_index].targetInfo.refreshRate.Numerator   = targetTimingInfo.vSyncNumerator / div;
                    pSDCPathInfoArray[path_index].targetInfo.refreshRate.Denominator = targetTimingInfo.vSyncDenominator / div;
                    pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.vSyncFreq.Numerator   = targetTimingInfo.vSyncNumerator / div;
                    pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.vSyncFreq.Denominator = targetTimingInfo.vSyncDenominator / div;
                }

                // Fill Source Mode Information
                pSDCModeInfoArray[sourceModeIndex].sourceMode.width  = currentDisplayMode.HzRes;
                pSDCModeInfoArray[sourceModeIndex].sourceMode.height = currentDisplayMode.VtRes;

                // Fill Target Mode Information
                pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.activeSize.cx         = targetTimingInfo.hActive;
                pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.activeSize.cy         = targetTimingInfo.vActive;
                pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.pixelRate             = targetTimingInfo.targetPixelRate;
                pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.hSyncFreq.Numerator   = targetTimingInfo.hSyncNumerator / div;
                pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = targetTimingInfo.hSyncDenominator / div;

                // Fill Scanline Information
                pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.scanLineOrdering = targetTimingInfo.scanLineOrdering;
                pSDCPathInfoArray[path_index].targetInfo.scanLineOrdering                            = targetTimingInfo.scanLineOrdering;

                // Fill Scaling Information
                if (currentDisplayMode.HzRes == targetTimingInfo.hActive && currentDisplayMode.VtRes == targetTimingInfo.vActive)
                {
                    // Physical ModeSet (MDS Scaling)
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize.x = targetTimingInfo.hActive;
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize.y = targetTimingInfo.vActive;

                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.left   = 0;
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.top    = 0;
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.right  = targetTimingInfo.hActive;
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.bottom = targetTimingInfo.vActive;

                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageRegion = pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip;

                    pSDCPathInfoArray[path_index].targetInfo.scaling = DISPLAYCONFIG_SCALING_IDENTITY;
                }
                else
                {
                    // Virtual ModeSet
                    DISPLAYCONFIG_SCALING scaling;
                    RECTL                 rDesktopImageRegion = { 0 };
                    POINTL                sourceXY            = { 0 };
                    POINTL                targetXY            = { 0 };

                    sourceXY.x = currentDisplayMode.HzRes;
                    sourceXY.y = currentDisplayMode.VtRes;
                    targetXY.x = targetTimingInfo.hActive;
                    targetXY.y = targetTimingInfo.vActive;

                    /* virtualModeSetAware is FALSE, enable PIPE Scalar else PLANE Scalar.
                    For PIPE Scalar Desktop PathSourceSize, DesktopImageClip and DesktopImageRegion should be same as Source Mode */
                    if (virtualModeSetAware == FALSE)
                    {
                        pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize = sourceXY;
                    }
                    else
                    {
                        pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize = targetXY;
                    }

                    // 'DesktopImageClip' Size Value will be always equal to Source Mode
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.left   = 0;
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.top    = 0;
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.right  = sourceXY.x;
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.bottom = sourceXY.y;

                    // Compute Scaling Values for Requested scaling.
                    bStatus = ComputeScalingData(virtualModeSetAware, currentDisplayMode.scaling, &sourceXY, &targetXY, &rDesktopImageRegion, &scaling);

                    if (bStatus == FALSE)
                    {
                        ERROR_LOG("ComputeScalingData Failed.");
                        pDisplayMode->status = DISPLAY_CONFIG_ERROR_INVALID_PARAMETER;
                        break;
                    }
                    // Assign Computed Scaling Data to DesktopImageInfo Structure's DesktopImageRegion Member.
                    pSDCPathInfoArray[path_index].targetInfo.scaling                             = scaling;
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageRegion = rDesktopImageRegion;
                }
            } // END of ImpactedtargetIDs Loop

            currentSourceModeIndex = pSDCPathInfoArray[ImpactedPathIds[0]].sourceInfo.sourceModeInfoIdx; // Getting sourcemodeinfoIdx for panel passed by caller.
            currentSourceMode      = pSDCModeInfoArray[currentSourceModeIndex].sourceMode;
            // Below Loop executed on Extended/Hybrid Configuration
            for (INT extended_index = 0; extended_index < extendPathCount; extended_index++)
            {
                UINT extendedSourceModeIndex = pSDCPathInfoArray[ExtendedPathIds[extended_index]].sourceInfo.sourceModeInfoIdx; // ModeInfoArray Index where Source Details to be filled
                pSDCModeInfoArray[extendedSourceModeIndex].sourceMode.position.x = currentSourceMode.position.x + currentSourceMode.width;
            } // END of ImpactedExtendedtargetID's Loop

            flags = (force_modeset == TRUE) ? GetDisplayConfigFlags(SDC_FLAGS_WITHOUT_OPTIMIZATION) : GetDisplayConfigFlags(SDC_FLAGS);

            Sleep(sdcDelayInMills / 3); // WA: This wait is added to overcome Mode Set failure while switching from Interlaced to Progress or ViceVersa.

            ret = SetDisplayConfig(numPathArrayElements, pSDCPathInfoArray, numModeInfoArrayElements, pSDCModeInfoArray, flags);

            if (ret == ERROR_SUCCESS)
            {
                DISPLAY_MODE currentMode;
                for (INT interval = 100; interval <= sdcDelayInMills; interval += 100)
                {
                    Sleep(100); // polling interval
                    GetMode(&pDisplayMode->panelInfo, &currentMode);

                    if (pDisplayMode->HzRes == currentMode.HzRes && pDisplayMode->VtRes == currentMode.VtRes && pDisplayMode->scanlineOrdering == currentMode.scanlineOrdering &&
                        pDisplayMode->rotation == currentMode.rotation && pDisplayMode->scaling == currentMode.scaling)
                    {
                        if (pDisplayMode->refreshRate == currentMode.refreshRate)
                        {
                            pDisplayMode->status = DISPLAY_CONFIG_ERROR_SUCCESS;
                        }
                        else
                        {
                            INFO_LOG("Display Mode Set Success with RR Mismatch WA ( Fix - TBD from Driver).");
                            pDisplayMode->status = DISPLAY_CONFIG_ERROR_SUCCUESS_RR_MISMATCH;
                        }
                        break;
                    }
                    else if (interval == sdcDelayInMills)
                    {
                        // Timeout condition
                        ERROR_LOG("After Mode Set, Verification failed with timeout.");
                        pDisplayMode->status = DISPLAY_CONFIG_ERROR_MODE_VERIFICATION_FAILED;
                    }
                }
            }
            else
            {
                ERROR_LOG("Set Display Mode Failed with Error Code: 0x%X.", ret);
                PrintDisplayInfo("SetMode() failed", numPathArrayElements, pSDCPathInfoArray, numModeInfoArrayElements, pSDCModeInfoArray);
                // Incase of few BFR panels, VSync denominator/2 is to be applied. Hence retrying it. 
                if (pDisplayMode->rrMode == DYNAMIC_RR && setConfigFailForBFR == FALSE)
                {
                    setConfigFailForBFR = TRUE;
                    goto ReRunToApplyDynamicRR;
                }
                pDisplayMode->status = DisplayConfigErrorCode(ret);
            }

    } while (FALSE);

    /* cleanup dynamically allocated memory */
    free(pSDCPathInfoArray);
    free(pSDCModeInfoArray);

    int value = GetGfxIndexValue(pDisplayMode->panelInfo.gfxAdapter.gfxIndex);
    EtwSetMode(value, pDisplayMode->panelInfo.targetID, pDisplayMode->status, virtualModeSetAware, pDisplayMode->HzRes, pDisplayMode->VtRes, pDisplayMode->refreshRate,
               pDisplayMode->scaling, pDisplayMode->rotation, pDisplayMode->scanlineOrdering, pDisplayMode->BPP, pDisplayMode->pixelClock_Hz, pDisplayMode->rrMode);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief                   SetIgclMode (Exposed API)
 * Description:             This function is used to set Display Mode obtained from IGCL API.
 * @param PDISPLAY_MODE     (_In_   Pointer to Requested Display Mode)
 * @param BOOLEAN           (_Out_  Flag to specify which scalar to enable PLANE (FLAG: TRUE) or PIPE)
 * @param INT               (_Out_  Time (In Milliseconds) to wait before and after calling SDC API)
 * @param BOOLEAN           (_In_   Flag to specify optimization is required or not while setting display mode)
 * @param DD_TIMING_INFO    (_In_   Input Display Timing Structure with IGCL data)
 * return: VOID             (Though function returns VOID, output parameter (PDISPLAY_TIMINGS) has error status)
 *----------------------------------------------------------------------------------------------------------*/
VOID SetIgclMode(_Inout_ PDISPLAY_MODE pDisplayMode, _In_ BOOLEAN virtualModeSetAware, _In_ INT sdcDelayInMills, _In_ BOOLEAN force_modeset, _In_ PDISPLAY_TIMINGS pDisplayTimings)
{
    LONG    ret;
    BOOLEAN bStatus = TRUE;
    INT     pIsOSPreferredMode;
    INT     impactedPathCount = 0;
    INT     extendPathCount   = 0;
    INT     div               = 10;

    UINT32                    flags;
    UINT32                    numPathArrayElements;
    UINT32                    numModeInfoArrayElements;
    UINT32                    currentSourceModeIndex = 0;     // source mode index for panel passed by caller
    DISPLAYCONFIG_SOURCE_MODE currentSourceMode      = { 0 }; // source mode for panel passed by caller

    UINT32     ExtendedPathIds[MAX_SUPPORTED_DISPLAYS]        = { 0 };
    UINT32     ImpactedPathIds[MAX_SUPPORTED_DISPLAYS]        = { 0 };
    PANEL_INFO ImpactedPathsPanelInfo[MAX_SUPPORTED_DISPLAYS] = { 0 };

    DISPLAYCONFIG_PATH_INFO *pSDCPathInfoArray = NULL;
    DISPLAYCONFIG_MODE_INFO *pSDCModeInfoArray = NULL;
    DISPLAY_CONFIG           os_config         = { 0 };

    do
    {
        if (NULL == pDisplayMode)
        {
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_INSUFFICIENT_BUFFER;
            ERROR_LOG("DISPLAY_MODE Object pDisplayMode is NULL.");
            break;
        }

        // From Win10 onwards driver supports VirtualMode, Hence Setting both ACTIVE and VIRTUALMODE flags
        flags = GetDisplayConfigFlags(QDC_ACTIVE_PATHS);

        // Get Path Array buffer size and Mode array buffer size through OS API.
        ret = GetDisplayConfigBufferSizes(flags, &numPathArrayElements, &numModeInfoArrayElements);

        if (ret != ERROR_SUCCESS)
        {
            ERROR_LOG("Get DisplayConfig Buffer Sizes Failed.");
            pDisplayMode->status = DisplayConfigErrorCode(ret);
            break;
        }

        // Allocate Buffer for SetDisplayConfig based on ModeArraySize and PathArraySize
        pSDCPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, (sizeof(DISPLAYCONFIG_PATH_INFO)));
        pSDCModeInfoArray = (DISPLAYCONFIG_MODE_INFO *)calloc(numModeInfoArrayElements, (sizeof(DISPLAYCONFIG_MODE_INFO)));
        if (pSDCPathInfoArray == NULL || pSDCModeInfoArray == NULL)
        {
            ERROR_LOG("Memory Allocation for Path Array/ Mode Array Failed.");
            pDisplayMode->status = DISPLAY_CONFIG_ERROR_MEMORY_ALLOCATION_FAILED;
            break;
        }

        /* Windows API which retrieves information about all possible display paths which are active */
        ret = QueryDisplayConfig(flags, &numPathArrayElements, pSDCPathInfoArray, &numModeInfoArrayElements, pSDCModeInfoArray, NULL);

        if (ERROR_SUCCESS != ret)
        {
            ERROR_LOG("QueryDisplayConfig Failed with return code: %d.", ret);
            pDisplayMode->status = DisplayConfigErrorCode(ret);
            break;
        }

        /* Get Display config, because if requested Target id is part of CLONE config need to modify those Path as well */
        os_config.size = sizeof(DISPLAY_CONFIG);
        GetConfig(&os_config);
        if (os_config.status != DISPLAY_CONFIG_ERROR_SUCCESS)
        {
            ERROR_LOG("GetConfig() Failed with return code: %d.", os_config.status);
            pDisplayMode->status = os_config.status;
            break;
        }

        // This below code maps PathIndexes of OS_Config to pSDCPathInfoArray pathIndexes.
        // For Current Path and All impacted Clone paths, SourceMode and TargetMode should be modified. This is stored in ImpactedPathIds[] and ImpactedPathsPanelInfo[]
        // For Extended path of current path, sourceMode x position to be modified. This is stored in ExtendedPathIds
        for (INT index = 0; index < os_config.numberOfDisplays; index++)
        {
            DISPLAY_PATH_INFO pathInfo  = os_config.displayPathInfo[index];
            PANEL_INFO        panelInfo = pathInfo.panelInfo;
            if (pDisplayMode->panelInfo.targetID == panelInfo.targetID && pDisplayMode->panelInfo.gfxAdapter.adapterLUID.LowPart == panelInfo.gfxAdapter.adapterLUID.LowPart &&
                pDisplayMode->panelInfo.gfxAdapter.adapterLUID.HighPart == panelInfo.gfxAdapter.adapterLUID.HighPart)
            {
                UINT osPathIndex = 0;

                GetPanelPathIndexFromOsPathArray(pSDCPathInfoArray, numPathArrayElements, panelInfo, &osPathIndex);
                ImpactedPathIds[impactedPathCount]        = osPathIndex; // Adding Current path as it should be modified.
                ImpactedPathsPanelInfo[impactedPathCount] = panelInfo;
                impactedPathCount++;

                // Find Clone paths and add it in ImpactedPathIds.
                for (INT index2 = 0; index2 < pathInfo.cloneGroupCount; index2++)
                {
                    UINT       cloneIndex     = pathInfo.cloneGroupPathIds[index2];
                    PANEL_INFO clonePanelInfo = os_config.displayPathInfo[cloneIndex].panelInfo;

                    GetPanelPathIndexFromOsPathArray(pSDCPathInfoArray, numPathArrayElements, clonePanelInfo, &osPathIndex);
                    ImpactedPathIds[impactedPathCount]        = osPathIndex;
                    ImpactedPathsPanelInfo[impactedPathCount] = clonePanelInfo;
                    impactedPathCount++;
                }

                for (INT index2 = 0; index2 < pathInfo.extendedGroupCount; index2++)
                {
                    UINT       extendedIndex     = pathInfo.extendedGroupPathIds[index2];
                    PANEL_INFO extendedPanelInfo = os_config.displayPathInfo[extendedIndex].panelInfo;

                    GetPanelPathIndexFromOsPathArray(pSDCPathInfoArray, numPathArrayElements, extendedPanelInfo, &osPathIndex);
                    ExtendedPathIds[extendPathCount] = osPathIndex;
                    extendPathCount++;
                }
            }
        }

        for (INT index = 0; index < impactedPathCount; index++)
        {
            UINT32 sourceModeIndex       = -1;
            UINT32 targetModeIndex       = -1;
            UINT32 desktopImageInfoIndex = -1;

            // Getting Impacted Path to modify path details.
            INT        path_index = ImpactedPathIds[index];
            PANEL_INFO panelInfo  = ImpactedPathsPanelInfo[index];

            DISPLAY_MODE currentDisplayMode = *pDisplayMode;
            currentDisplayMode.panelInfo    = panelInfo;

            targetModeIndex       = pSDCPathInfoArray[path_index].targetInfo.targetModeInfoIdx;  // ModeInfoArray Index where Target Details to be filled
            sourceModeIndex       = pSDCPathInfoArray[path_index].sourceInfo.sourceModeInfoIdx;  // ModeInfoArray Index where Source Details to be filled
            desktopImageInfoIndex = pSDCPathInfoArray[path_index].targetInfo.desktopModeInfoIdx; // ModeInfoArray Index where Desktop ImageInfo Details to be filled

            if (panelInfo.driverBranch == LEGACY_DRIVER)
            {
                // Setting to 1 to avoid division by 10 again, since division is not required for legacy platforms
                div = 1;
            }
            // Unable to Get HW timing from Driver - We might be in Clone Configuration and Requested mode may not be available in in driver mode list
            // Hence get OS preffered mode and proceed ( but we need to Make sure - Target Id is part of Clone Configuration , Due to Clone Behaviour in Win 10+ RS3 )
            else if (impactedPathCount >= 2)
            {
                // Setting to 1 to avoid division by 10 again, since OS is already keeping track of proper data from driver
                div = 1;
            }

            pSDCPathInfoArray[path_index].targetInfo.rotation = currentDisplayMode.rotation;

            // if Dynamic RR is set to True in passed mode, 3rd bit to be set, else reset to set to static RR mode

            pSDCPathInfoArray[path_index].flags = pDisplayMode->rrMode == DYNAMIC_RR ? (pSDCPathInfoArray[path_index].flags | DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE) :
                                                                                       (pSDCPathInfoArray[path_index].flags & ~(DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE));

            // Fill the passed refresh rate in case of dynamic RR
            if (pDisplayMode->rrMode == DYNAMIC_RR)
            {
                pSDCPathInfoArray[path_index].targetInfo.refreshRate.Numerator   = pDisplayMode->refreshRate;
                pSDCPathInfoArray[path_index].targetInfo.refreshRate.Denominator = 1;
            }

            // Fill the timing paramaters in case of physical mode to be set - Legacy
            else
            {
                pSDCPathInfoArray[path_index].targetInfo.refreshRate.Numerator   = pDisplayTimings->vSyncNumerator / div;
                pSDCPathInfoArray[path_index].targetInfo.refreshRate.Denominator = pDisplayTimings->vSyncDenominator / div;
            }

            // Fill Source Mode Information
            pSDCModeInfoArray[sourceModeIndex].sourceMode.width  = currentDisplayMode.HzRes;
            pSDCModeInfoArray[sourceModeIndex].sourceMode.height = currentDisplayMode.VtRes;

            // Fill Target Mode Information
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.activeSize.cx         = pDisplayTimings->hActive;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.activeSize.cy         = pDisplayTimings->vActive;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.pixelRate             = pDisplayTimings->targetPixelRate;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.hSyncFreq.Numerator   = pDisplayTimings->hSyncNumerator / div;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.hSyncFreq.Denominator = pDisplayTimings->hSyncDenominator / div;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.vSyncFreq.Numerator   = pDisplayTimings->vSyncNumerator / div;
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.vSyncFreq.Denominator = pDisplayTimings->vSyncDenominator / div;

            // Fill Scanline Information
            pSDCModeInfoArray[targetModeIndex].targetMode.targetVideoSignalInfo.scanLineOrdering = pDisplayTimings->scanLineOrdering;
            pSDCPathInfoArray[path_index].targetInfo.scanLineOrdering                            = pDisplayTimings->scanLineOrdering;

            // Fill Scaling Information
            if (currentDisplayMode.HzRes == pDisplayTimings->hActive && currentDisplayMode.VtRes == pDisplayTimings->vActive)
            {
                // Physical ModeSet (MDS Scaling)
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize.x = pDisplayTimings->hActive;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize.y = pDisplayTimings->vActive;

                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.left   = 0;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.top    = 0;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.right  = pDisplayTimings->hActive;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.bottom = pDisplayTimings->vActive;

                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageRegion = pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip;

                pSDCPathInfoArray[path_index].targetInfo.scaling = DISPLAYCONFIG_SCALING_IDENTITY;
            }
            else
            {
                // Virtual ModeSet
                DISPLAYCONFIG_SCALING scaling;
                RECTL                 rDesktopImageRegion = { 0 };
                POINTL                sourceXY            = { 0 };
                POINTL                targetXY            = { 0 };

                sourceXY.x = currentDisplayMode.HzRes;
                sourceXY.y = currentDisplayMode.VtRes;
                targetXY.x = pDisplayTimings->hActive;
                targetXY.y = pDisplayTimings->vActive;

                /* virtualModeSetAware is FALSE, enable PIPE Scalar else PLANE Scalar.
                For PIPE Scalar Desktop PathSourceSize, DesktopImageClip and DesktopImageRegion should be same as Source Mode */
                if (virtualModeSetAware == FALSE)
                {
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize = sourceXY;
                }
                else
                {
                    pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.PathSourceSize = targetXY;
                }

                // 'DesktopImageClip' Size Value will be always equal to Source Mode
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.left   = 0;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.top    = 0;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.right  = sourceXY.x;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageClip.bottom = sourceXY.y;

                // Compute Scaling Values for Requested scaling.
                bStatus = ComputeScalingData(virtualModeSetAware, currentDisplayMode.scaling, &sourceXY, &targetXY, &rDesktopImageRegion, &scaling);

                if (bStatus == FALSE)
                {
                    ERROR_LOG("ComputeScalingData Failed.");
                    pDisplayMode->status = DISPLAY_CONFIG_ERROR_INVALID_PARAMETER;
                    break;
                }
                // Assign Computed Scaling Data to DesktopImageInfo Structure's DesktopImageRegion Member.
                pSDCPathInfoArray[path_index].targetInfo.scaling                             = scaling;
                pSDCModeInfoArray[desktopImageInfoIndex].desktopImageInfo.DesktopImageRegion = rDesktopImageRegion;
            }
        } // END of ImpactedtargetIDs Loop

        currentSourceModeIndex = pSDCPathInfoArray[ImpactedPathIds[0]].sourceInfo.sourceModeInfoIdx; // Getting sourcemodeinfoIdx for panel passed by caller.
        currentSourceMode      = pSDCModeInfoArray[currentSourceModeIndex].sourceMode;
        // Below Loop executed on Extended/Hybrid Configuration
        for (INT extended_index = 0; extended_index < extendPathCount; extended_index++)
        {
            UINT extendedSourceModeIndex = pSDCPathInfoArray[ExtendedPathIds[extended_index]].sourceInfo.sourceModeInfoIdx; // ModeInfoArray Index where Source Details to be filled
            pSDCModeInfoArray[extendedSourceModeIndex].sourceMode.position.x = currentSourceMode.position.x + currentSourceMode.width;
        } // END of ImpactedExtendedtargetID's Loop

        flags = (force_modeset == TRUE) ? GetDisplayConfigFlags(SDC_FLAGS_WITHOUT_OPTIMIZATION) : GetDisplayConfigFlags(SDC_FLAGS);

        Sleep(sdcDelayInMills / 3); // WA: This wait is added to overcome Mode Set failure while switching from Interlaced to Progress or ViceVersa.

        PrintDisplayInfo("SetIgclMode()", numPathArrayElements, pSDCPathInfoArray, numModeInfoArrayElements, pSDCModeInfoArray);

        ret = SetDisplayConfig(numPathArrayElements, pSDCPathInfoArray, numModeInfoArrayElements, pSDCModeInfoArray, flags);

        if (ret == ERROR_SUCCESS)
        {
            DISPLAY_MODE currentMode;
            for (INT interval = 100; interval <= sdcDelayInMills; interval += 100)
            {
                Sleep(100); // polling interval
                GetMode(&pDisplayMode->panelInfo, &currentMode);

                if (pDisplayMode->HzRes == currentMode.HzRes && pDisplayMode->VtRes == currentMode.VtRes && pDisplayMode->scanlineOrdering == currentMode.scanlineOrdering &&
                    pDisplayMode->rotation == currentMode.rotation && pDisplayMode->scaling == currentMode.scaling)
                {
                    if (pDisplayMode->refreshRate == currentMode.refreshRate)
                    {
                        pDisplayMode->status = DISPLAY_CONFIG_ERROR_SUCCESS;
                    }
                    else
                    {
                        INFO_LOG("Display Mode Set Success with RR Mismatch WA ( Fix - TBD from Driver).");
                        pDisplayMode->status = DISPLAY_CONFIG_ERROR_SUCCUESS_RR_MISMATCH;
                    }
                    break;
                }
                else if (interval == sdcDelayInMills)
                {
                    // Timeout condition
                    ERROR_LOG("After Mode Set, Verification failed with timeout.");
                    pDisplayMode->status = DISPLAY_CONFIG_ERROR_MODE_VERIFICATION_FAILED;
                }
            }
        }
        else
        {
            ERROR_LOG("Set Display Mode Failed with Error Code: 0x%X.", ret);
            PrintDisplayInfo("SetIgclMode() failed", numPathArrayElements, pSDCPathInfoArray, numModeInfoArrayElements, pSDCModeInfoArray);
            pDisplayMode->status = DisplayConfigErrorCode(ret);
        }

    } while (FALSE);

    /* cleanup dynamically allocated memory */
    free(pSDCPathInfoArray);
    free(pSDCModeInfoArray);

    int value = GetGfxIndexValue(pDisplayMode->panelInfo.gfxAdapter.gfxIndex);
    EtwSetMode(value, pDisplayMode->panelInfo.targetID, pDisplayMode->status, virtualModeSetAware, pDisplayMode->HzRes, pDisplayMode->VtRes, pDisplayMode->refreshRate,
               pDisplayMode->scaling, pDisplayMode->rotation, pDisplayMode->scanlineOrdering, pDisplayMode->BPP, pDisplayMode->pixelClock_Hz, pDisplayMode->rrMode);
}