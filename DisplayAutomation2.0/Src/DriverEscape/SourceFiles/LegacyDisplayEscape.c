/*------------------------------------------------------------------------------------------------*
 *
 * @file     LegacyDisplayEscape.c
 * @brief    This file contains Implementation of Legacy Display Escape APIs - LegacyGetSupportedScaling,
 *           LegacyQueryCurrentConfig, LegacyDpcdRead, LegacyDpcdWrite, LegacyGetEdidData, LegacyGetTargetTimings,
 *           LegacyGetMiscSystemInfo, LegacyGetSetDPPHWLUT, LegacyGetColorimetryInfo, LegacyGetSetOutputFormat
 *           LegacySetColorimetryInfo, LegacyGetCurrentConfig
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "DisplayEscape.h"
#include "DriverEscape.h"

/**---------------------------------------------------------------------------------------------------------*
 * @brief       LegacyGetSupportedScaling (Exposed API)
 * Description  This function is used query driver to get all supported scaling for given source mode for Legacy Driver.
 * @param[In]   pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[In]   targetID (UINT32 - Target ID of the display)
 * @param[In]   modeInfo (Pointer of _CUI_ESC_MODE_INFO structure)
 * @param[Out]  pSupportedScaling (USHORT - Pointer to supported scaling variable)
 * @return      Return TRUE on success and FALSE on failure
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyGetSupportedScaling(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ UINT32 targetID, _In_ CUI_ESC_MODE_INFO modeInfo, _Out_ USHORT *pSupportedScaling)
{
    BOOLEAN                         status                = FALSE;
    BOOLEAN                         adapterStatus         = FALSE;
    GFX_ESCAPE_HEADER_T             escapeOpCode          = { 0 };
    ADAPTER_INFO_GDI_NAME           adapterInfoGdiName    = { 0 };
    CUI_ESC_QUERY_COMPENSATION_ARGS queryCompensationArgs = { 0 };
    CUI_ESC_QUERY_COMPENSATION_ARGS queryCurrentConfig    = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);
    VERIFY_IGFX_ADAPTER_STATUS(adapterStatus);

    status = LegacyQueryCurrentConfig(pAdapterInfo, &queryCurrentConfig);
    if (FALSE == status)
        return status;
    memcpy_s(&queryCompensationArgs.stTopology, sizeof(CUI_ESC_TOPOLOGY), &queryCurrentConfig.stTopology, sizeof(CUI_ESC_TOPOLOGY));
    queryCompensationArgs.stTopology.ignoreUnsupportedModes = 1;

    for (UINT displayIndex = 0; displayIndex < queryCurrentConfig.stTopology.numOfPaths; displayIndex++)
    {
        if (queryCurrentConfig.stTopology.stPathInfo[displayIndex].targetID == targetID)
        {
            queryCompensationArgs.stTopology.stPathInfo[displayIndex].eModeInfoType             = CUI_ESC_MODE_INFO_SCALING_QUERIED;
            queryCompensationArgs.stTopology.stPathInfo[displayIndex].stModeInfo.sourceX        = modeInfo.sourceX;
            queryCompensationArgs.stTopology.stPathInfo[displayIndex].stModeInfo.sourceY        = modeInfo.sourceY;
            queryCompensationArgs.stTopology.stPathInfo[displayIndex].stModeInfo.refreshRate    = modeInfo.refreshRate;
            queryCompensationArgs.stTopology.stPathInfo[displayIndex].stModeInfo.eScanLineOrder = modeInfo.eScanLineOrder;
        }
        else
            queryCompensationArgs.stTopology.stPathInfo[displayIndex].eModeInfoType = CUI_ESC_MODE_PINNED;
    }

    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = COM_ESC_QUERY_COMPENSATION_IN_TOPOLOGY;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;

    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(CUI_ESC_QUERY_COMPENSATION_ARGS), escapeOpCode, &queryCompensationArgs);
    if (FALSE == status)
    {
        ERROR_LOG("CUI_ESC_QUERY_COMPENSATION_ARG TargetID : %u", targetID);
    }
    for (UINT displayIndex = 0; displayIndex < queryCurrentConfig.stTopology.numOfPaths; displayIndex++)
    {
        if (queryCompensationArgs.stTopology.stPathInfo[displayIndex].targetID == targetID)
        {
            *pSupportedScaling = queryCompensationArgs.stTopology.stPathInfo[displayIndex].stModeInfo.stCompensationCaps.compensation;
            status             = TRUE;
            break;
        }
    }
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyQueryCurrentConfig (Internal API)
 * Description      This function is used perform driver escape to get current query configuration for Legacy Driver.
 * @param[In]       pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[InOut]    pQueryCurrentConfig (Pointer of _CUI_ESC_QUERY_COMPENSATION_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyQueryCurrentConfig(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ CUI_ESC_QUERY_COMPENSATION_ARGS *pQueryCurrentConfig)
{
    BOOLEAN               adapterStatus      = FALSE;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);
    VERIFY_IGFX_ADAPTER_STATUS(adapterStatus);

    /* Initailize the escape structures*/
    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = COM_ESC_QUERY_CURRENT_CONFIG;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;

    adapterStatus = InvokeDriverEscape(&adapterInfoGdiName, sizeof(CUI_ESC_QUERY_COMPENSATION_ARGS), escapeOpCode, pQueryCurrentConfig);
    if (FALSE == adapterStatus)
    {
        ERROR_LOG("CUI_ESC_QUERY_COMPENSATION_ARGS error :%lu ", pQueryCurrentConfig->error);
    }
    return adapterStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyDpcdRead (Internal API)
 * Description      This function has implementation to Read DPCD Register Value for given offset for Legacy Driver
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[Out]      dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyDpcdRead(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[])
{

    BOOLEAN               status             = FALSE;
    BOOLEAN               adapterStatus      = FALSE;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    SB_AUXACCESS_ARGS     dpcdArgs           = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);
    VERIFY_IGFX_ADAPTER_STATUS(adapterStatus);

    dpcdArgs.portType    = SB_DP_PORT;
    dpcdArgs.usePortType = SB_DP_PORTNUMBER;
    dpcdArgs.command     = SB_DP_READ;
    dpcdArgs.address     = startOffset;
    dpcdArgs.deviceUID   = pPanelInfo->targetID;
    dpcdArgs.size        = SB_DATA_SIZE;

    ZeroMemory(dpcdArgs.data, MAX_LUT_AUX_BUFSIZE);

    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = SB_ESC_AUX_ACCESS;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;

    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(SB_AUXACCESS_ARGS), escapeOpCode, &dpcdArgs);
    if (FALSE == status)
    {
        ERROR_LOG("DPCD porttype : %d  eSBAuxErrorType: %d DeviceUID : %lu", dpcdArgs.portType, dpcdArgs.eSBAuxErrorType, dpcdArgs.deviceUID);
    }
    for (UINT index = 0; index < dpcdBufferSize; index++)
    {
        dpcdBuffer[index] = dpcdArgs.data[index];
    }
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyDpcdWrite (Internal API)
 * Description      This function has implementation to Write DPCD Register Value for given offset for Legacy Driver
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[In]      dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyDpcdWrite(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[])
{

    BOOLEAN               status             = FALSE;
    BOOLEAN               adapterStatus      = FALSE;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    SB_AUXACCESS_ARGS     dpcdArgs           = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);
    VERIFY_IGFX_ADAPTER_STATUS(adapterStatus);

    dpcdArgs.portType    = SB_DP_PORT;
    dpcdArgs.usePortType = SB_DP_PORTNUMBER;
    dpcdArgs.command     = SB_DP_WRITE;
    dpcdArgs.address     = startOffset;
    dpcdArgs.deviceUID   = pPanelInfo->targetID;
    dpcdArgs.size        = SB_DATA_SIZE;

    ZeroMemory(dpcdArgs.data, MAX_LUT_AUX_BUFSIZE);

    for (UINT index = 0; index < dpcdBufferSize; index++)
    {
        dpcdArgs.data[index] = (BYTE)dpcdBuffer[index];
    }

    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = SB_ESC_AUX_ACCESS;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;

    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(SB_AUXACCESS_ARGS), escapeOpCode, &dpcdArgs);
    if (FALSE == status)
    {
        ERROR_LOG("DPCD porttype : %d  eSBAuxErrorType: %d DeviceUID : %lu", dpcdArgs.portType, dpcdArgs.eSBAuxErrorType, dpcdArgs.deviceUID);
    }

    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyGetEdidData (Internal API)
 * Description      This function has implementation to Get RAW EDID Data of the Display for Legacy Driver
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[Out]      edidData (BYTE[] - Edid data block)
 * @param[Out]      pNumEdidBlock (UINT - Pointer to edid block)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyGetEdidData(_In_ PANEL_INFO *pPanelInfo, _Out_ BYTE edidData[], _Out_ UINT *pNumEdidBlock)
{
    BOOLEAN               status             = TRUE;
    UINT                  numExtensionBlock  = 0;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    COM_ESC_GET_EDID_ARGS edidBuffer         = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    NULL_PTR_CHECK(edidData);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    edidBuffer.displayID    = pPanelInfo->targetID;
    edidBuffer.edidBlockNum = 0;

    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = COM_ESC_GET_EDID;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(COM_ESC_GET_EDID_ARGS), escapeOpCode, &edidBuffer));

    numExtensionBlock = (UINT)edidBuffer.edidData[EXTENSIONS_BYTE];
    DEBUG_LOG("Number of extension blocks = %lu", numExtensionBlock);
    memcpy(edidData, edidBuffer.edidData, EDID_BLOCK_SIZE);
    (*pNumEdidBlock)++;

    /* Read extension blocks*/
    if (numExtensionBlock > 0)
    {
        for (UINT count = 1; (count <= numExtensionBlock) && (*pNumEdidBlock < MAX_EDID_BLOCK); count++)
        {
            edidBuffer.displayID    = pPanelInfo->targetID;
            edidBuffer.edidBlockNum = count;

            status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(COM_ESC_GET_EDID_ARGS), escapeOpCode, &edidBuffer);
            if (FALSE == status)
            {
                ERROR_LOG("Failed to fetch EDID BUFFER for DisplayID : %lu of ExtensionBlock : %d", edidBuffer.displayID, count);
                break;
            }
            DEBUG_LOG("EDID BUFFER for DisplayID : %lu of ExtensionBlock : %d fetched with buffer size - %d", edidBuffer.displayID, count, sizeof edidBuffer.edidData);
            memcpy((edidData + (count * EDID_BLOCK_SIZE)), &edidBuffer.edidData, EDID_BLOCK_SIZE);
            (*pNumEdidBlock)++;
        }
    }
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyGetTargetTimings (Internal API)
 * Description      This function is used to get Display Timing for given DisplayMode for Legacy Driver.
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[InOut]    pConvertRRrational (Pointer to _CUI_ESC_CONVERT_RR_RATIONAL_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyGetTargetTimings(_In_ PANEL_INFO *pPanelInfo, _Inout_ CUI_ESC_CONVERT_RR_RATIONAL_ARGS *pConvertRRrational)
{
    BOOLEAN               status             = FALSE;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    NULL_PTR_CHECK(pConvertRRrational);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_VERSION;
    escapeOpCode.minorEscapeCode       = COM_ESC_CONVERT_RR_RATIONAL;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_FILE_VERSION;

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(CUI_ESC_CONVERT_RR_RATIONAL_ARGS), escapeOpCode, pConvertRRrational));
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyConfigDxgkPowerComponent (Internal API)
 * Description      This function has implementation to perform driver escape to configure dxgk power componenet
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[InOut]    pDxgkPowerCompArgs (Pointer to MISC_ESC_DXGK_POWER_COMPONENT_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyConfigDxgkPowerComponent(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Inout_ MISC_ESC_DXGK_POWER_COMPONENT_ARGS *pDxgkPowerCompArgs)
{
    BOOLEAN             status       = FALSE;
    GFX_ESCAPE_HEADER_T escapeOpCode = { 0 };

    NULL_PTR_CHECK(pDxgkPowerCompArgs);

    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_VERSION;
    escapeOpCode.minorEscapeCode       = MISC_ESC_CONFIG_DXGK_POWER_COMPONENT;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_MISC;
    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_FILE_VERSION;

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(MISC_ESC_DXGK_POWER_COMPONENT_ARGS), escapeOpCode, pDxgkPowerCompArgs));

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyGetMiscSystemInfo (Internal API)
 * Description      This function has implementation to perform driver escape call to Get System info for Legacy Driver
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[Out]      pMiscSystemInfo (Pointer to _MISC_ESC_GET_SYSTEM_INFO_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyGetMiscSystemInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Out_ MISC_ESC_GET_SYSTEM_INFO_ARGS *pMiscSystemInfo)
{
    BOOLEAN             status       = FALSE;
    GFX_ESCAPE_HEADER_T escapeOpCode = { 0 };
    NULL_PTR_CHECK(pMiscSystemInfo);

    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_VERSION;
    escapeOpCode.minorEscapeCode       = MISC_ESC_GET_SYSTEM_INFO;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_MISC;
    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_FILE_VERSION;

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(MISC_ESC_GET_SYSTEM_INFO_ARGS), escapeOpCode, pMiscSystemInfo));

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyGetSetDPPHWLUT (Internal API)
 * Description      This function has implementation to perform driver escape call for Get/Set DPPHWLUT for Legacy Driver
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[In]       size (Type of ULONG)
 * @param[InOut]    pCuiDppHwLutInfo (Pointer to structure _CUI_ESC_GET_SET_HW_3DLUT_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyGetSetDPPHWLUT(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _In_ ULONG escapeDataSize, _Inout_ CUI_ESC_GET_SET_HW_3DLUT_ARGS *pDppHwLutInfo)
{
    BOOLEAN             status       = FALSE;
    GFX_ESCAPE_HEADER_T escapeOpCode = { 0 };
    NULL_PTR_CHECK(pDppHwLutInfo);

    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_VERSION;
    escapeOpCode.minorEscapeCode       = COM_ESC_GET_SET_HW_3DLUT;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_FILE_VERSION;

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, escapeDataSize, escapeOpCode, pDppHwLutInfo));

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyGetColorimetryInfo (Internal API)
 * Description      This function has implementation to perform driver escape call to Get colorimetry info for Legacy Driver
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[InOut]    pColorimetryArgs (Pointer to _CUI_ESC_GET_SET_COLORSPACE_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyGetColorimetryInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Inout_ CUI_ESC_GET_SET_COLORSPACE_ARGS *pColorimetryArgs)
{
    BOOLEAN             status       = FALSE;
    GFX_ESCAPE_HEADER_T escapeOpCode = { 0 };
    NULL_PTR_CHECK(pColorimetryArgs);

    pColorimetryArgs->opType = SB_OPTYPE_GET;

    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = COM_ESC_GET_SET_COLORSPACE;
    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(CUI_ESC_GET_SET_COLORSPACE_ARGS), escapeOpCode, pColorimetryArgs));

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacySetColorimetryInfo (Internal API)
 * Description      This function has implementation to perform driver escape call to Set colorimetry info for Legacy Driver
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[InOut]    pColorimetryArgs (Pointer to _CUI_ESC_GET_SET_COLORSPACE_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacySetColorimetryInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Inout_ CUI_ESC_GET_SET_COLORSPACE_ARGS *pColorimetryArgs)
{
    BOOLEAN             status       = FALSE;
    GFX_ESCAPE_HEADER_T escapeOpCode = { 0 };
    NULL_PTR_CHECK(pColorimetryArgs);

    pColorimetryArgs->opType = SB_OPTYPE_SET;

    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = COM_ESC_GET_SET_COLORSPACE;
    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(CUI_ESC_GET_SET_COLORSPACE_ARGS), escapeOpCode, pColorimetryArgs));

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyGetSetOutputFormat (Exposed API)
 * Description      This function has implementation for get and set the BPC and Encoding
 * @param[In]       pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[In]       pSetOutputFormatArgs (Pointer to structure IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyGetSetOutputFormat(_In_ PANEL_INFO *pPanelInfo, _Inout_ IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT *pGetSetOutputFormat)
{

    BOOLEAN               status             = FALSE;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = COM_ESC_GET_SET_OVERRIDE_OUTPUT_FORMAT;
    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT), escapeOpCode, pGetSetOutputFormat));
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyGetCurrentConfig (Exposed API)
 * Description      This function has implementation to perform driver escape call to Get Current Config
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[InOut]    pCompensation (Pointer to CUI_ESC_QUERY_COMPENSATION_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyGetCurrentConfig(_In_ PANEL_INFO *pPanelInfo, _Inout_ CUI_ESC_QUERY_COMPENSATION_ARGS *pCompensation)
{
    BOOLEAN               status             = FALSE;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = COM_ESC_QUERY_CURRENT_CONFIG;
    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(CUI_ESC_QUERY_COMPENSATION_ARGS), escapeOpCode, pCompensation));

    return TRUE;
}
