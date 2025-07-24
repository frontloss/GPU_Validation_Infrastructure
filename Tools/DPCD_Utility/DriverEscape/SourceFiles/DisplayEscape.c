/*------------------------------------------------------------------------------------------------*
 *
 * @file     DisplayEscape.c
 * @brief    This file contains Implementation of Display Escape APIs - GetDriverType, 
 *           DpcdRead, DpcdWrite
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "DisplayEscape.h"
#include "DriverEscape.h"


VOID PrintDisplayInfo(CHAR *pTableName, UINT32 numPathArrayElements, DISPLAYCONFIG_PATH_INFO *pPathInfoArray, UINT32 numModeInfoArrayElements,
                      DISPLAYCONFIG_MODE_INFO *pModeInfoArray)
{
    if (numPathArrayElements != 0)
    {
        DEBUG_LOG("Table : %s", pTableName);
        DEBUG_LOG("pPathInfoArray sourceInfo:-");
        DEBUG_LOG("%-6s %-11s %-11s %-11s %-11s %-15s %-15s %-11s %-11s", "Index", "lowpart", "highpart", "id", "modeInfoIdx", "cloneGroupId", "srcModeInfoIdx", "statusFlags",
                  "Flags");
        for (UINT32 p1 = 0; p1 < numPathArrayElements; p1++)
        {
            DEBUG_LOG("%-6d %-11X %-11X %-11X %-11X %-15X %-15X %-11X %-11X", p1, pPathInfoArray[p1].sourceInfo.adapterId.LowPart, pPathInfoArray[p1].sourceInfo.adapterId.HighPart,
                      pPathInfoArray[p1].sourceInfo.id, pPathInfoArray[p1].sourceInfo.modeInfoIdx, pPathInfoArray[p1].sourceInfo.cloneGroupId,
                      pPathInfoArray[p1].sourceInfo.sourceModeInfoIdx, pPathInfoArray[p1].sourceInfo.statusFlags, pPathInfoArray[p1].flags);
        }
        DEBUG_LOG("pPathInfoArray targetInfo:-");
        DEBUG_LOG("%-6s %-11s %-11s %-11s %-11s %-17s %-11s %-11s %-11s %-11s %-11s %-11s %-11s", "Index", "lowpart", "highpart", "id", "modeInfoIdx", "tgtModeInfoIdx",
                  "outputTech", "RR", "rotation", "scaling", "scanLine", "tgAvailable", "statusFlags");
        for (UINT32 p1 = 0; p1 < numPathArrayElements; p1++)
        {
            DEBUG_LOG("%-6d %-11X %-11X %-11X %-11X %-17X %-11lu %-11lu %-11d %-11d %-11d %-11d %-11lu", p1, pPathInfoArray[p1].targetInfo.adapterId.LowPart,
                      pPathInfoArray[p1].targetInfo.adapterId.HighPart, pPathInfoArray[p1].targetInfo.id, pPathInfoArray[p1].targetInfo.modeInfoIdx,
                      pPathInfoArray[p1].targetInfo.targetModeInfoIdx, pPathInfoArray[p1].targetInfo.outputTechnology, pPathInfoArray[p1].targetInfo.refreshRate,
                      pPathInfoArray[p1].targetInfo.rotation, pPathInfoArray[p1].targetInfo.scaling, pPathInfoArray[p1].targetInfo.scanLineOrdering,
                      pPathInfoArray[p1].targetInfo.targetAvailable, pPathInfoArray[p1].targetInfo.statusFlags);
        }
    }
    else
    {
        DEBUG_LOG("pPathInfoArray is Empty!!!");
    }
    if (numModeInfoArrayElements != 0)
    {
        DEBUG_LOG("pModeInfoArray sourceMode:-");
        DEBUG_LOG("%-6s %-11s %-11s %-15s %-15s %-15s %-15s %-15s %-15s %-15s", "Index", "Lowpart", "HighPart", "id", "infoType", "height", "width", "position.x", "position.y",
                  "pixelFormat");
        for (UINT32 m1 = 0; m1 < numModeInfoArrayElements; m1++)
        {
            if (pModeInfoArray[m1].infoType == 1)
                DEBUG_LOG("%-6d %-11X %-11X %-15X %-15d %-15lu %-15lu %-15ld %-15ld %-15d", m1, pModeInfoArray[m1].adapterId.LowPart, pModeInfoArray[m1].adapterId.HighPart,
                          pModeInfoArray[m1].id, pModeInfoArray[m1].infoType, pModeInfoArray[m1].sourceMode.height, pModeInfoArray[m1].sourceMode.width,
                          pModeInfoArray[m1].sourceMode.position.x, pModeInfoArray[m1].sourceMode.position.y, pModeInfoArray[m1].sourceMode.pixelFormat);
        }
        DEBUG_LOG("pModeInfoArray targetMode.targetVideoSignalInfo:-");
        DEBUG_LOG("%-6s %-11s %-11s %-15s %-15s %-11s %-11s %-11s %-11s %-15s %-11s %-11s %-11s %-11s %-11s %-11s", "Index", "Lowpart", "HighPart", "id", "infoType", "active.cx",
                  "active.cy", "hSyncFreq.D", "hSyncFreq.N", "pixelRate", "scanLine", "total.cx", "total.cy", "videoStd", "vSyncFreq.D", "vSyncFreq.N");
        for (UINT32 m1 = 0; m1 < numModeInfoArrayElements; m1++)
        {
            if (pModeInfoArray[m1].infoType == 2)
                DEBUG_LOG("%-6d %-11X %-11X %-15X %-15d %-11lu %-11lu %-11lu %-11lu %-15llu %-11d %-11lu %-11lu %-11lu %-11lu %-11lu", m1, pModeInfoArray[m1].adapterId.LowPart,
                          pModeInfoArray[m1].adapterId.HighPart, pModeInfoArray[m1].id, pModeInfoArray[m1].infoType,
                          pModeInfoArray[m1].targetMode.targetVideoSignalInfo.activeSize.cx, pModeInfoArray[m1].targetMode.targetVideoSignalInfo.activeSize.cy,
                          pModeInfoArray[m1].targetMode.targetVideoSignalInfo.hSyncFreq.Denominator, pModeInfoArray[m1].targetMode.targetVideoSignalInfo.hSyncFreq.Numerator,
                          pModeInfoArray[m1].targetMode.targetVideoSignalInfo.pixelRate, pModeInfoArray[m1].targetMode.targetVideoSignalInfo.scanLineOrdering,
                          pModeInfoArray[m1].targetMode.targetVideoSignalInfo.totalSize.cx, pModeInfoArray[m1].targetMode.targetVideoSignalInfo.totalSize.cy,
                          pModeInfoArray[m1].targetMode.targetVideoSignalInfo.videoStandard, pModeInfoArray[m1].targetMode.targetVideoSignalInfo.vSyncFreq.Denominator,
                          pModeInfoArray[m1].targetMode.targetVideoSignalInfo.vSyncFreq.Numerator);
        }
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               GetDriverType (Internal API)
 * Description:         This function is used to check whether Yangra driver installed by checking ESC Version through Driver Escape.
 * @param[In]           gfxInfo (GFX_INFO - Adapter Information)
 * return: DRIVER_TYPE  DRIVER_YANGRA OR DRIVER_LEGACY OR DRIVER_UNKNOWN
 *----------------------------------------------------------------------------------------------------------*/
DRIVER_TYPE GetDriverType(_In_ GFX_INFO gfxInfo)
{
    BOOLEAN                 status        = FALSE;
    GFX_ESCAPE_HEADER_T     escapeOpCode  = { 0 };
    DRIVER_TYPE             driverBranch  = DRIVER_UNKNOWN;
    DD_ESC_GET_VERSION_ARGS escapeVersion = { 0 };

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;

    /* Invoke Yangra driver escape*/
    if (TRUE == InvokeDriverEscape(gfxInfo, sizeof(DD_ESC_GET_VERSION_ARGS), escapeOpCode, &escapeVersion))
    {
        driverBranch = YANGRA_DRIVER; // Yangra Driver installed
    }
    else
    {
        /* Escape call structure */
        CUI_ESC_QUERY_COMPENSATION_ARGS queryCurrentConfig = { 0 };

        escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;
        escapeOpCode.minorEscapeCode       = COM_ESC_QUERY_CURRENT_CONFIG;
        escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
        escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;

        /* Invoke Legacy driver escape*/
        if (TRUE == InvokeDriverEscape(gfxInfo, sizeof(CUI_ESC_QUERY_COMPENSATION_ARGS), escapeOpCode, &queryCurrentConfig))
        {
            driverBranch = LEGACY_DRIVER; // Legacy driver installed
        }
        else
        {
            ERROR_LOG("DriverEscape Failed to Find DriverBranch for target ID : %lu", gfxInfo.targetID);
        }
    }
    return driverBranch;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               DpcdRead (Exposed API)
 * Description          This function has implementation to Read DPCD Register Value for given offset
 * @param[In]           gfxInfo (GFX_INFO - Adapter Information)
 * @param[In]           startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]           dpcdBufferSize (INT - Size of the dpcd buffer)
 * @param[Out]          dpcdBuffer (Pointer to ULONG)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN DpcdRead(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[])
{
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;

    NULL_PTR_CHECK(dpcdBuffer);

    if (dpcdBufferSize <= 0 || dpcdBufferSize > MAX_LUT_AUX_BUFSIZE)
    {
        ERROR_LOG("Invalid Buffer Size");
        return FALSE;
    }

    // Getting GFX Adapter DriverType - Legacy/ Yangra
    driverBranch = GetDriverType(gfxInfo);
    VERIFY_DRIVER_TYPE(driverBranch);

    if (driverBranch == LEGACY_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(LegacyDpcdRead(gfxInfo, startOffset, dpcdBufferSize, dpcdBuffer));
    }
    else if (driverBranch == YANGRA_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(YangraDpcdRead(gfxInfo, startOffset, dpcdBufferSize, dpcdBuffer));
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               DpcdWrite (Exposed API)
 * Description          This function has implementation to Write DPCD Register Value for given offset
 * @param[In]           gfxInfo (GFX_INFO - Adapter Information)
 * @param[In]           startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]           dpcdBufferSize (INT - Size of the dpcd buffer)
 * @param[In]           dpcdBuffer (Pointer to ULONG)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN DpcdWrite(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[])
{
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;

    NULL_PTR_CHECK(dpcdBuffer);

    if (dpcdBufferSize <= 0 || dpcdBufferSize > MAX_LUT_AUX_BUFSIZE)
    {
        ERROR_LOG("Invalid Buffer Size");
        return FALSE;
    }

    // Getting GFX Adapter DriverType - Legacy/ Yangra
    driverBranch = GetDriverType(gfxInfo);
    VERIFY_DRIVER_TYPE(driverBranch);

    if (driverBranch == LEGACY_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(LegacyDpcdWrite(gfxInfo, startOffset, dpcdBufferSize, dpcdBuffer));
    }
    else if (driverBranch == YANGRA_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(YangraDpcdWrite(gfxInfo, startOffset, dpcdBufferSize, dpcdBuffer));
    }
    return TRUE;
}

BOOLEAN QueryAdapterDetails(GFX_INFO_ARR *gfxArr)
{
    LONG                     status;
    UINT                     flags;
    GFX_INFO                 gfxInfo;
    BOOLEAN                  isFound;
    UINT32                   numPathArrayElements     = 0;
    UINT32                   numModeInfoArrayElements = 0;
    DISPLAYCONFIG_PATH_INFO *pPathInfoArray           = NULL;
    DISPLAYCONFIG_MODE_INFO *pModeInfoArray           = NULL;

    do
    {
        flags = QDC_ALL_PATHS;
        /* Get Path Array buffer size and Mode array buffer size through OS API. */
        status = GetDisplayConfigBufferSizes(flags, &numPathArrayElements, &numModeInfoArrayElements);

        INFO_LOG("GetDisplayConfigBufferSizes Flag - %d, status - %ld, numPath - %lu, numMode - %lu", flags, status, numPathArrayElements, numModeInfoArrayElements);

        if (ERROR_SUCCESS != status)
        {
            ERROR_LOG("Get PathArray and ModeArray Buffer Size Failed with status code %ld", status);
            break;
        }

        /* Allocate Buffer for QueryDisplayConfig */
        pPathInfoArray = (DISPLAYCONFIG_PATH_INFO *)calloc(numPathArrayElements, (sizeof(DISPLAYCONFIG_PATH_INFO)));
        pModeInfoArray = (DISPLAYCONFIG_MODE_INFO *)calloc(numModeInfoArrayElements, (sizeof(DISPLAYCONFIG_MODE_INFO)));

        if (NULL == pPathInfoArray || NULL == pModeInfoArray)
        {
            ERROR_LOG("PathArray and ModeArray Memory Allocation is Null");
            break;
        }

        /* Windows API which retrieves information about all possible display paths for all display devices */
        status = QueryDisplayConfig(flags, &numPathArrayElements, pPathInfoArray, &numModeInfoArrayElements, pModeInfoArray, NULL);
        INFO_LOG("QueryDisplayConfig status - %ld", status);

        PrintDisplayInfo("QDC call -", numPathArrayElements, pPathInfoArray, numModeInfoArrayElements, pModeInfoArray);

        if (ERROR_SUCCESS != status)
        {
            ERROR_LOG("QueryDisplayConfig Failed with Error Code: %ld", status);
            break;
        }

        for (UINT pathIndex = 0; pathIndex < numPathArrayElements; pathIndex++)
        {
            if (pPathInfoArray[pathIndex].targetInfo.targetAvailable == FALSE) // Panel is disconnected, But DISPLAYCONFIG_TARGET_IN_USE might have set
            {
                continue;
            }

            gfxInfo = (GFX_INFO){ 0 };

            INFO_LOG("pathIndex %lu, adapter low - %lu and high - %ld, tgtID - %lu", 
                pathIndex, pPathInfoArray[pathIndex].targetInfo.adapterId.LowPart, pPathInfoArray[pathIndex].targetInfo.adapterId.HighPart, pPathInfoArray[pathIndex].targetInfo.id);

            isFound = FALSE;
            for (LONG gfxIndex = 0; gfxIndex < gfxArr->count; gfxIndex++)
            {
                if ((UNMASK_TARGET_ID(pPathInfoArray[pathIndex].targetInfo.id) == gfxArr->arr[gfxIndex].targetID) &&
                    (pPathInfoArray[pathIndex].targetInfo.adapterId.HighPart == gfxArr->arr[gfxIndex].adapterID.HighPart) &&
                    (pPathInfoArray[pathIndex].targetInfo.adapterId.LowPart == gfxArr->arr[gfxIndex].adapterID.LowPart))
                {
                    isFound = TRUE;
                    break;
                }
            }

            if (isFound == FALSE || gfxArr->count == 0)
            {
                gfxInfo.adapterID = pPathInfoArray[pathIndex].targetInfo.adapterId;
                gfxInfo.targetID = UNMASK_TARGET_ID(pPathInfoArray[pathIndex].targetInfo.id);
                gfxInfo.outputTechnology = pPathInfoArray[pathIndex].targetInfo.outputTechnology;

                memcpy_s(&gfxArr->arr[gfxArr->count], sizeof(GFX_INFO), &gfxInfo, sizeof(GFX_INFO));
                gfxArr->count++;
            }
        }

    } while (FALSE);

    return status == 0 ? TRUE : FALSE;
}
