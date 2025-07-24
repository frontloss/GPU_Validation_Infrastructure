/*------------------------------------------------------------------------------------------------*
 *
 * @file     YangraDisplayEscape.c
 * @brief    This file contains Implementation of Yangra Display Escape APIs - YangraDpcdRead, YangraDpcdWrite
 *           YangraGetEdidData, YangraInvokeCollage, YangraQueryModeTable, YangraGetMiscSystemInfo,
 *           YangraAlsAggressivenessLevelOverride, YangraGetSetDPPHWLUT, YangraGetColorimetryInfo,
 *           YangraSetColorimetryInfo, YangraGetSetVrr, YangraPlugUnplugWBDevice, YangraQueryWB, YangraGetSetOutputFormat
 *           YangraDumpWBBuffer, YangraGetSetCfps, YangraGetSetNNScaling, YangraAddCustomMode
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "DisplayEscape.h"
#include "DriverEscape.h"
#include "ColorModelInterface.h"
#include "..\Logger\ETWTestLogging.h"

const WCHAR *PIXEL_FORMAT[] = { L"8BPP_INDEXED",  L"B5G6R5X0",  L"B8G8R8X8",   L"R8G8B8X8",   L"B10G10R10X2", L"R10G10B10X2", L"R10G10B10X2_XR_BIAS",
                                L"R16G16B16X16F", L"YUV444_8",  L"YUV444_10",  L"YUV422_12",  L"YUV422_16",   L"YUV422_16",   L"YUV444_10",
                                L"YUV444_12",     L"YUV444_16", L"NV12YUV420", L"P010YUV420", L"P012YUV420",  L"P016YUV420",  L"MAX_PIXELFORMAT" };

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraDpcdRead (Internal API)
 * Description      This function has implementation to Read DPCD Register Value for given offset for Yangra Driver
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[Out]      dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraDpcdRead(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[])
{
    BOOLEAN                    status             = FALSE;
    BOOLEAN                    adapterStatus      = FALSE;
    GFX_ESCAPE_HEADER_T        escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME      adapterInfoGdiName = { 0 };
    DD_ESC_AUX_I2C_ACCESS_ARGS dpcdArgs           = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);
    VERIFY_IGFX_ADAPTER_STATUS(adapterStatus);

    TARGET_ID targetId = { 0 };
    targetId.Value     = pPanelInfo->targetID;

    dpcdArgs.i2cAuxArgs.operation  = DD_NATIVE_AUX;
    dpcdArgs.i2cAuxArgs.write      = 0;
    dpcdArgs.i2cAuxArgs.port       = targetId.bitInfo.portType;
    dpcdArgs.i2cAuxArgs.address    = startOffset;
    dpcdArgs.i2cAuxArgs.dataLength = 16;
    ZeroMemory(dpcdArgs.i2cAuxArgs.data, MAX_LUT_AUX_BUFSIZE);

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_AUX_I2C_ACCESS;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;

    EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);

    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_AUX_I2C_ACCESS_ARGS), escapeOpCode, &dpcdArgs);

    if (DD_ESCAPE_STATUS_SUCCESS != dpcdArgs.status)
        ERROR_LOG("Read DPCD escape failed with errorcode - %d", dpcdArgs.status);

    for (UINT index = 0; index < dpcdBufferSize; index++)
    {
        dpcdBuffer[index] = dpcdArgs.i2cAuxArgs.data[index];
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraDpcdWrite (Internal API)
 * Description      This function has implementation to Write DPCD Register Value for given offset for Yangra Driver
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[In]       dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraDpcdWrite(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[])
{
    BOOLEAN                    status             = FALSE;
    BOOLEAN                    adapterStatus      = FALSE;
    GFX_ESCAPE_HEADER_T        escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME      adapterInfoGdiName = { 0 };
    DD_ESC_AUX_I2C_ACCESS_ARGS dpcdArgs           = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);
    VERIFY_IGFX_ADAPTER_STATUS(adapterStatus);

    TARGET_ID targetId = { 0 };
    targetId.Value     = pPanelInfo->targetID;

    dpcdArgs.i2cAuxArgs.operation  = DD_NATIVE_AUX;
    dpcdArgs.i2cAuxArgs.write      = 1;
    dpcdArgs.i2cAuxArgs.port       = targetId.bitInfo.portType;
    dpcdArgs.i2cAuxArgs.address    = startOffset;
    dpcdArgs.i2cAuxArgs.dataLength = 16;
    ZeroMemory(dpcdArgs.i2cAuxArgs.data, MAX_LUT_AUX_BUFSIZE);

    for (UINT index = 0; index < dpcdBufferSize; index++)
    {
        dpcdArgs.i2cAuxArgs.data[index] = (UCHAR)dpcdBuffer[index];
    }

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_AUX_I2C_ACCESS;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_AUX_I2C_ACCESS_ARGS), escapeOpCode, &dpcdArgs);

    if (DD_ESCAPE_STATUS_SUCCESS != dpcdArgs.status)
        ERROR_LOG("Write DPCD escape failed with errorcode - %d", dpcdArgs.status);

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraGetEdidData (Internal API)
 * Description      This function has implementation to Get RAW EDID Data of the Display for Yangra Driver
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[Out]      edidData (BYTE[] - Edid data block)
 * @param[Out]      pNumEdidBlock (UINT - Pointer to edid block)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetEdidData(_In_ PANEL_INFO *pPanelInfo, _Out_ BYTE edidData[], _Out_ UINT *pNumEdidBlock)
{
    BOOLEAN               status             = TRUE;
    UINT                  numExtensionBlock  = 0;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    ESC_GET_EDID_ARGS     edidBuffer         = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    NULL_PTR_CHECK(edidData);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    edidBuffer.displayID     = pPanelInfo->targetID;
    edidBuffer.edidBlockNum  = 0;
    edidBuffer.forceEDIDRead = TRUE;

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_EDID;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(ESC_GET_EDID_ARGS), escapeOpCode, &edidBuffer);

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
            EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
            status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(ESC_GET_EDID_ARGS), escapeOpCode, &edidBuffer);
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
 * @brief           GetSetOutputFormat (Exposed API)
 * Description      This function has implementation for get and set the BPC and Encoding
 * @param[In]       pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[In]       pSetOutputFormatArgs (Pointer to structure IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetSetOutputFormat(_In_ PANEL_INFO *pPanelInfo, _Inout_ IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT *pGetSetOutputFormat)
{

    BOOLEAN               status             = FALSE;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_SET_OVERRIDE_OUTPUT_FORMAT;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    if (pGetSetOutputFormat->opType == CUI_ESC_COLORSPACE_OPTYPE_GET)
    {
        EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    else
    {
        EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT), escapeOpCode, pGetSetOutputFormat));

    return TRUE;
}

/**--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*
 * @brief                                                LogCollageStructureData (Internal API)
 * @description                                          Logs the structure based on the structure type passed.
 * @params       STRUCTURE_TYPE                          (_In_ argType: Structure Type of the data pointed by void pointer)
 * @params       VOID*                                   (_In_ collageData: Pointer to the structure that has to be converted to string)
 *---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*/
VOID LogCollageStructureData(_In_ DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS collageData)
{
    DEBUG_LOG("*************************************** COLLAGE MODE ARGS **************************************");
    DEBUG_LOG("cConfigurationInfo->CollageConfigPossible        : %d", collageData.collageConfigPossible);
    DEBUG_LOG("cConfigurationInfo->CollageSupported             : %d", collageData.collageSupported);
    DEBUG_LOG("cConfigurationInfo->Operation                    : %d", collageData.operation);

    DEBUG_LOG("**************************************** COLLAGE TOPOLOGY ***************************************");
    DEBUG_LOG("CollageTopology.TotalNumberOfHTiles: %d.", collageData.collageTopology.totalNumberOfHTiles);
    DEBUG_LOG("CollageTopology.TotalNumberOfVTiles: %d.", collageData.collageTopology.totalNumberOfVTiles);

    // Iterate through each childinfo and log the information.
    for (int i = 0; i < DD_CUI_ESC_MAX_PHYSICAL_PIPES; ++i)
    {
        DEBUG_LOG("CollageTopology.CollageChildInfo[%d].ChildId             : %d", i, collageData.collageTopology.collageChildInfo[i].childID);
        DEBUG_LOG("CollageTopology.CollageChildInfo[%d].HTileLocation       : %d", i, collageData.collageTopology.collageChildInfo[i].hTileLocation);
        DEBUG_LOG("CollageTopology.CollageChildInfo[%d].VTileLocation       : %d", i, collageData.collageTopology.collageChildInfo[i].vTileLocation);
        DEBUG_LOG("CollageTopology.CollageChildInfo[%d].LeftBezelsize       : %d", i, collageData.collageTopology.collageChildInfo[i].leftBezelsize);
        DEBUG_LOG("CollageTopology.CollageChildInfo[%d].RightBezelsize      : %d", i, collageData.collageTopology.collageChildInfo[i].rightBezelsize);
        DEBUG_LOG("CollageTopology.CollageChildInfo[%d].TopBezelsize        : %d", i, collageData.collageTopology.collageChildInfo[i].topBezelsize);
        DEBUG_LOG("CollageTopology.CollageChildInfo[%d].BottomBezelsize     : %d", i, collageData.collageTopology.collageChildInfo[i].bottomBezelsize);
        DEBUG_LOG("CollageTopology.CollageChildInfo[%d].TileBezelInformation: %d", i, collageData.collageTopology.collageChildInfo[i].tileBezelInformation);
    }
}

/**--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*
 * @brief           YangraInvokeCollage (Exposed API)
 * @description     Invokes required collage functionality based on the input collage operation
 * @param[In]       pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[InOut]    pConfigurationInfo (Pointer to DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS - Contains the collage topology information and collage operation)
 * @return          Return TRUE on success and FALSE on failure
 *---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraInvokeCollage(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS *pConfigurationInfo)
{
    BOOLEAN               status             = FALSE;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    NULL_PTR_CHECK(pConfigurationInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_SET_COLLAGE_MODE;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    if (pConfigurationInfo->operation == DD_CUI_ESC_COLLAGE_OPERATION_GET)
    {
        EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    else
    {
        EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }

    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);

    switch (pConfigurationInfo->operation)
    {
    case DD_CUI_ESC_COLLAGE_OPERATION_GET:
    case DD_CUI_ESC_COLLAGE_OPERATION_VALIDATE:
    case DD_CUI_ESC_COLLAGE_OPERATION_ENABLE:
    case DD_CUI_ESC_COLLAGE_OPERATION_DISABLE:
        status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS), escapeOpCode, pConfigurationInfo);
        if (FALSE == status)
        {
            ERROR_LOG("DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS collageSupported :%d collageConfigPossible :%d", pConfigurationInfo->collageSupported,
                      pConfigurationInfo->collageConfigPossible);
        }
        status = TRUE;
        break;
    case DD_CUI_ESC_COLLAGE_OPERATION_BEZEL_UPDATE:
        WARNING_LOG("Yet to be implemented from driver side");
        break;
    default:
        ERROR_LOG("Unknown collage functionality");
        break;
    }
    INFO_LOG("Collage Operation : %d Collage Supported: %d Collage Config Possible : %d", pConfigurationInfo->operation, pConfigurationInfo->collageSupported,
             pConfigurationInfo->collageConfigPossible);
    // LogCollageStructureData(*pConfigurationInfo); // Uncomment to Print Collage Structure Data within logs
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraQueryModeTable (Exposed API)
 * Description      This function has implementation to Get query mode table details for Yangra Driver
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       pSourceAndTargetModeTable (Pointer to _DD_ESC_QUERY_MODE_TABLE_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraQueryModeTable(_In_ PANEL_INFO *pPanelInfo, _In_ DD_ESC_QUERY_MODE_TABLE_ARGS *pSourceAndTargetModeTable)
{

    INT                   modeTableSize      = 0;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    NULL_PTR_CHECK(pSourceAndTargetModeTable);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_QUERY_MODE_TABLE;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    if (pSourceAndTargetModeTable->numSrcModes == 0 && pSourceAndTargetModeTable->numTgtModes == 0)
    {
        VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS), escapeOpCode, pSourceAndTargetModeTable));
    }
    else
    {
        modeTableSize = sizeof(DD_ESC_QUERY_MODE_TABLE_ARGS) + sizeof(DD_SOURCE_MODE_INFO) * pSourceAndTargetModeTable->numSrcModes +
                        sizeof(DD_TIMING_INFO) * pSourceAndTargetModeTable->numTgtModes;
        VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, modeTableSize, escapeOpCode, pSourceAndTargetModeTable));
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief       YangraAlsAggressivenessLevelOverride (Exposed API)
 * Description  This function has implementation to Enable\Disable LACE with Aggressiveness Level and Lux values
 * @param[In]   pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[In]   luxOperation (BOOL - To perform lux operation)
 * @param[In]   aggressivenessOperation (BOOL - To perform aggressiveness operation)
 * @param[In]   lux (INT - Lux value)
 * @param[In]   aggressivenessLevel (INT(0\1\2) - Aggressiveness value)
 * @return      Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraAlsAggressivenessLevelOverride(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ BOOL luxOperation, _In_ BOOL aggressivenessOperation, _In_ INT lux,
                                             _In_ INT aggressivenessLevel)
{
    BOOLEAN                          status                 = FALSE;
    ADAPTER_INFO_GDI_NAME            adapterInfoGdiName     = { 0 };
    GFX_ESCAPE_HEADER_T              escapeOpCode           = { 0 };
    COM_ESC_POWER_CONSERVATION_ARGS *pPowerConservationArgs = NULL;

    NULL_PTR_CHECK(pAdapterInfo);

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    if (lux < 0)
    {
        ERROR_LOG("Invalid Lux value passed");
        return FALSE;
    }

    pPowerConservationArgs = (COM_ESC_POWER_CONSERVATION_ARGS *)malloc(sizeof(COM_ESC_POWER_CONSERVATION_ARGS));
    NULL_PTR_CHECK(pPowerConservationArgs);

    ZeroMemory(pPowerConservationArgs, sizeof(COM_ESC_POWER_CONSERVATION_ARGS));

    pPowerConservationArgs->operation                                                   = PWRCONS_OP_ALS_SETTINGS;
    pPowerConservationArgs->opType                                                      = PWRCONS_OPTYPE_SET;
    pPowerConservationArgs->opParameters.ambientLightParam.luxOperation                 = luxOperation;
    pPowerConservationArgs->opParameters.ambientLightParam.lux                          = lux;
    pPowerConservationArgs->opParameters.ambientLightParam.aggressivenessLevelOperation = aggressivenessOperation;
    pPowerConservationArgs->opParameters.ambientLightParam.aggressivenessLevelFromCUI   = aggressivenessLevel;

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_POWER_CONSERVATION;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);
    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(COM_ESC_POWER_CONSERVATION_ARGS), escapeOpCode, pPowerConservationArgs);
    if (FALSE == status)
    {
        ERROR_LOG("COM_ESC_POWER_CONSERVATION_ARGS opType: %d opStatus : %d", pPowerConservationArgs->opType, pPowerConservationArgs->opStatus);
    }
    free(pPowerConservationArgs);
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraConfigDxgkPowerComponent (Internal API)
 * Description      This function has implementation to perform driver escape to configure dxgk power componenet
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[InOut]    pDxgkPowerCompArgs (Pointer to MISC_ESC_DXGK_POWER_COMPONENT_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraConfigDxgkPowerComponent(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Inout_ MISC_ESC_DXGK_POWER_COMPONENT_ARGS *pDxgkPowerCompArgs)
{
    BOOLEAN             status       = FALSE;
    GFX_ESCAPE_HEADER_T escapeOpCode = { 0 };

    NULL_PTR_CHECK(pDxgkPowerCompArgs);

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.minorEscapeCode       = MISC_ESC_CONFIG_DXGK_POWER_COMPONENT;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_MISC;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(MISC_ESC_DXGK_POWER_COMPONENT_ARGS), escapeOpCode, pDxgkPowerCompArgs));

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraGetMiscSystemInfo
 * Description      This function has implementation to perform driver escape call to Get System info for Yangra Driver
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[Out]      pMiscSystemInfo (Pointer to _MISC_ESC_GET_SYSTEM_INFO_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetMiscSystemInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Out_ MISC_ESC_GET_SYSTEM_INFO_ARGS *pMiscSystemInfo)
{

    GFX_ESCAPE_HEADER_T escapeOpCode = { 0 };

    NULL_PTR_CHECK(pMiscSystemInfo);
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.minorEscapeCode       = MISC_ESC_GET_SYSTEM_INFO;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_MISC;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(MISC_ESC_GET_SYSTEM_INFO_ARGS), escapeOpCode, pMiscSystemInfo));

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraGetSetDPPHWLUT
 * Description      This function has implementation to perform driver escape call for Get/Set DPPHWLUT for Yangra Driver
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[In]       dppHwLutInfo (Type of _DD_ESC_SET_3D_LUT_ARGS structure)
 * @param[In]       pDepth (Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetSetDPPHWLUT(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _In_ DD_ESC_SET_3D_LUT_ARGS *pdppHwLutInfo, _In_ ULONG *pDepth)
{

    GFX_ESCAPE_HEADER_T escapeOpCode = { 0 };
    NULL_PTR_CHECK(pDepth);

    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_SET_3D_LUT;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_SET_3D_LUT_ARGS), escapeOpCode, pdppHwLutInfo));

    *pDepth = HWLUT_SAMPLE_SIZE;
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraGetColorimetryInfo
 * Description      This function has implementation to perform driver escape call to Get colorimetry info for Yangra Driver
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[InOut]    pQueryDisplayDetails (Pointer to _DD_ESC_QUERY_DISPLAY_DETAILS_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetColorimetryInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _Inout_ DD_ESC_QUERY_DISPLAY_DETAILS_ARGS *pQueryDisplayDetails)
{

    GFX_ESCAPE_HEADER_T escapeOpCode = { 0 };
    NULL_PTR_CHECK(pQueryDisplayDetails);

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_QUERY_DISPLAY_DETAILS;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_QUERY_DISPLAY_DETAILS_ARGS), escapeOpCode, pQueryDisplayDetails));

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraSetColorimetryInfo
 * Description      This function has implementation to perform driver escape call to Set colorimetry info for Yangra Driver
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[In]       colorModelArgs (Pointer to _DD_ESC_GET_SET_COLOR_MODEL_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraSetColorimetryInfo(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, _In_ DD_ESC_GET_SET_COLOR_MODEL_ARGS colorModelArgs)
{

    GFX_ESCAPE_HEADER_T escapeOpCode = { 0 };

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_SET_COLOR_MODEL;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_GET_SET_COLOR_MODEL_ARGS), escapeOpCode, &colorModelArgs));

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraGetSetVrr (Exposed API)
 * @param[In]       pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[InOut]    pGetSetVrrArgs (Pointer to _DD_CUI_ESC_GET_SET_VRR_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetSetVrr(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_CUI_ESC_GET_SET_VRR_ARGS *pGetSetVrrArgs)
{
    BOOLEAN               status             = FALSE;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_SET_VRR;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    if (pGetSetVrrArgs->operation == DD_CUI_ESC_VRR_OPERATION_GET_INFO)
    {
        EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    else
    {
        EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);
    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_CUI_ESC_GET_SET_VRR_ARGS), escapeOpCode, pGetSetVrrArgs);
    if (FALSE == status)
    {

        ERROR_LOG("DD_CUI_ESC_GET_SET_VRR_ARGS operation: %d vrrSupported : %d vrrEnabled :%d vrrHighFpsSlonEnabled : %d vrrLoeFpsSlonEnabled : %d", pGetSetVrrArgs->operation,
                  pGetSetVrrArgs->vrrEnabled, pGetSetVrrArgs->vrrHighFpsSolnEnabled, pGetSetVrrArgs->vrrLowFpsSolnEnabled);
    }
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraPlugUnplugWBDevice (Exposed API)
 * Description      This function has implementation to escape call to Plug/Unplug WB device
 * @param[In]       pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[In]       wbHpdArgs (Pointer to _DD_ESC_WRITEBACK_HPD structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraPlugUnplugWBDevice(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ DD_ESC_WRITEBACK_HPD wbHpdArgs, _In_ CHAR *filePath)
{
    BOOLEAN               status             = FALSE;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));
    DEBUG_LOG("hotplug is : %d", wbHpdArgs.hotPlug);

    if (TRUE == wbHpdArgs.OverrideDefaultEdid && NULL != filePath)
    {
        FILE *  fhandle;
        errno_t err        = 0;
        size_t  bytes_read = 0;

        err = fopen_s(&fhandle, filePath, "rb");
        if (err != 0)
        {
            ERROR_LOG("Failed to get EDID file handle");
            return FALSE;
        }

        bytes_read = fread_s(wbHpdArgs.EdidData, WB_EDID_BLOCK_SIZE, sizeof(BYTE), WB_EDID_BLOCK_SIZE, fhandle);
        DEBUG_LOG("bytes_read is : %d", bytes_read);
        fclose(fhandle);
    }
    else
    {
        wbHpdArgs.OverrideDefaultEdid = FALSE;
        DEBUG_LOG("OverrideDefaultEdid is None or No EDID filepath provided, FakeEDID will get plugged");
    }

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_WRITEBACK_ENABLE_DISABLE;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);
    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_WRITEBACK_HPD), escapeOpCode, &wbHpdArgs);
    DEBUG_LOG("Resolution.cX : %d, Resolution.cY : %d, TargetID : %d", wbHpdArgs.resolution.cX, wbHpdArgs.resolution.cY, wbHpdArgs.deviceID);
    if (FALSE == status)
    {
        ERROR_LOG("DD_ESC_WRITEBACK_HPD DeviceID : %lu HotPlug :%d ", wbHpdArgs.deviceID, wbHpdArgs.hotPlug);
    }

    DEBUG_LOG("Override default EDID is : %d", wbHpdArgs.OverrideDefaultEdid);
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraQueryWB (Exposed API)
 * Description      This function has implementation to check if WB feature is enabled/disabled
 * @param[In]       pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[InOut]    pWbQueryArgs (Pointer to _DD_WRITEBACK_QUERY_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraQueryWB(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_WRITEBACK_QUERY_ARGS *pWbQueryArgs)
{
    BOOLEAN               status             = FALSE;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    NULL_PTR_CHECK(pWbQueryArgs);

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_WRITEBACK_QUERY;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);
    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_WRITEBACK_QUERY_ARGS), escapeOpCode, pWbQueryArgs);
    if (FALSE == status)
    {

        ERROR_LOG("WriteBack feature status :%d ", pWbQueryArgs->isWbFeatureEnabled);
    }
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           GenerateFileName (Exposed API)
 * Description      This function has implementation to dump the WB buffer
 * @param[In]       fileName (Pointer to File for dumping data)
 * @param[InOut]    wbBufferInfo (Structure of _DD_WB_BUFFER_INFO containing resolution)
 * @return          Returns Nothing
 *-----------------------------------------------------------------------------------------------------------*/
VOID GenerateFileName(WCHAR *fileName, UINT deviceNumber, _In_ UINT instance, DD_WB_BUFFER_INFO wbBufferInfo)
{
    const WCHAR *pixel_format = L"";
    if (wbBufferInfo.pixelFormat <= DD_CUI_ESC_MAX_PIXELFORMAT)
        pixel_format = PIXEL_FORMAT[wbBufferInfo.pixelFormat];

    swprintf(fileName, FILE_SIZE, L"Logs//WB_%d_%ls_%lu.png", deviceNumber, pixel_format, instance);
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraDumpWBBuffer (Exposed API)
 * Description      This function has implementation to dump the WB buffer
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[InOut]    pWbBufferInfo (Pointer to _DD_WB_BUFFER_INFO structure)
 * @param[In].......imageBpc (Bits per pixel for output dump)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraDumpWBBuffer(_In_ PANEL_INFO *pPanelInfo, _In_ UINT instance, _Inout_ DD_WB_BUFFER_INFO *pWbBufferInfo, _In_ UINT imageBpc)
{
    ADAPTER_INFO_GDI_NAME                 adapterInfoGdiName   = { 0 };
    GFX_ESCAPE_HEADER_T                   escapeOpCode         = { 0 };
    DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS  wbCaptureBufferArgs  = { 0 };
    DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS *pWbCaptureBufferArgs = NULL;
    WCHAR                                 fileName[FILE_SIZE]  = L"";
    BOOLEAN                               status               = FALSE;

    NULL_PTR_CHECK(pPanelInfo);
    NULL_PTR_CHECK(pWbBufferInfo);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_WRITEBACK_CAPTURE_BUFFER;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    wbCaptureBufferArgs.deviceID   = pPanelInfo->targetID;
    wbCaptureBufferArgs.bufferSize = 0;

    /* Escape call to get buffer size */
    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS), escapeOpCode, &wbCaptureBufferArgs);
    if (status == FALSE || (wbCaptureBufferArgs.bufferSize == 0))
    {
        ERROR_LOG("Escape call to get buffersize failed or has returned buffersize as 0");
        return FALSE;
    }

    /* Escape call to get buffer filled with pipe output*/
    pWbCaptureBufferArgs = (DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS *)malloc((sizeof(DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS) + wbCaptureBufferArgs.bufferSize));
    if (pWbCaptureBufferArgs == NULL)
    {
        ERROR_LOG("Memory allocation for buffer failed");
        return FALSE;
    }
    pWbCaptureBufferArgs->bufferSize = wbCaptureBufferArgs.bufferSize;
    pWbCaptureBufferArgs->deviceID   = pPanelInfo->targetID;
    EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    status = InvokeDriverEscape(&adapterInfoGdiName, (sizeof(DD_ESC_WRITEBACK_CAPTURE_BUFFER_ARGS) + pWbCaptureBufferArgs->bufferSize), escapeOpCode, pWbCaptureBufferArgs);
    if (status == FALSE)
    {
        free(pWbCaptureBufferArgs);
        ERROR_LOG("Escape call to get bufferdump failed");
        return FALSE;
    }

    /* Copy details to pWbBufferInfo to use in test layer */
    pWbBufferInfo->memoryFormat = pWbCaptureBufferArgs->memoryFormat;
    pWbBufferInfo->pixelFormat  = pWbCaptureBufferArgs->pixelFormat;
    memcpy(&pWbBufferInfo->resolution, &pWbCaptureBufferArgs->resolution, sizeof(DD_2DREGION));

    /* BIT8 of target ID indicates the writeback device number */
    GenerateFileName(fileName, ((pPanelInfo->targetID >> 8) & 1), instance, *pWbBufferInfo);

    /* Dump data to png file*/
    DumpWbBufferToPngFile(&fileName[0], pWbCaptureBufferArgs->resolution.cX, pWbCaptureBufferArgs->resolution.cY, pWbCaptureBufferArgs->wdBuffer, imageBpc);

    free(pWbCaptureBufferArgs);
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraGetQuantisationRange
 * Description      This function has implementation to perform driver escape call to Get quantisation range  for Yangra Driver
 * @param[In]       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param[InOut]    avi_quantisation_struct (Pointer to DD_CUI_ESC_AVI_INFOFRAME_CUSTOM structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetSetQuantisationRange(_In_ PANEL_INFO *pPanelInfo, _Inout_ DD_CUI_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME_ARGS *avi_quantisation_struct)
{

    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    NULL_PTR_CHECK(avi_quantisation_struct);
    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    if (avi_quantisation_struct->Operation == DD_COLOR_OPERATION_GET)
    {
        EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    else
    {
        EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pPanelInfo->gfxAdapter.deviceID,
             pPanelInfo->gfxAdapter.busDeviceID, pPanelInfo->gfxAdapter.deviceInstanceID, pPanelInfo->gfxAdapter.gfxIndex, pPanelInfo->gfxAdapter.vendorID,
             pPanelInfo->gfxAdapter.isActive);

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_CUI_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME_ARGS), escapeOpCode, avi_quantisation_struct));
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraGetSetCfps (Exposed API)
 * @param[In]       pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[InOut]    pGetSetCappedFpsArgs (Pointer to _DD_CUI_ESC_GET_SET_CAPPED_FPS_ARGS structure)
 * @return BOOLEAN  Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetSetCfps(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_CUI_ESC_GET_SET_CAPPED_FPS_ARGS *pGetSetCappedFpsArgs)
{

    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_SET_CAPPED_FPS;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    if (pGetSetCappedFpsArgs->OpCode == DD_CUI_ESC_SET_CAPPED_FPS)
    {
        EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    else
    {
        EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_CUI_ESC_GET_SET_CAPPED_FPS_ARGS), escapeOpCode, pGetSetCappedFpsArgs));

    return TRUE;
}

/**--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*
 * @brief           YangraGetSetNNScaling (Internal API)
 * Description      Invokes required enable disable functionality based on the input operation.
 * @param[In]       pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[InOut]    pGetSetargs (Pointer to DD_CUI_ESC_GET_SET_NN_ARGS structure)
 * @return          Return TRUE on success and FALSE on failure
 *---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetSetNNScaling(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_CUI_ESC_GET_SET_NN_ARGS *pGetSetargs)
{
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_SET_NN_SCALING;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    if (pGetSetargs->OpCode == DD_CUI_ESC_GET_NN_SCALING_STATE)
    {
        EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    else
    {
        EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_CUI_ESC_GET_SET_NN_ARGS), escapeOpCode, pGetSetargs));

    return TRUE;
}

BOOLEAN YangraGetCustomMode(_In_ PANEL_INFO *pPanelInfo, _Inout_ DD_CUI_ESC_GET_SET_CUSTOM_MODE_ARGS *pCustomModeArgs)
{
    DWORD                       modeTableSize      = 0;
    BOOLEAN                     status             = FALSE;
    DD_CUI_ESC_CUSTOM_SRC_MODE *pSourceMode        = NULL;
    ADAPTER_INFO_GDI_NAME       adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T         escapeOpCode       = { 0 };
    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);
    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));
    pCustomModeArgs->CustomModeOp = DD_CUI_ESC_CUSTOM_MODE_GET_MODES;
    pCustomModeArgs->TargetId     = pPanelInfo->targetID;

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_CUSTOM_MODES;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;

    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    // This is to get the NUmber of modes being added as the custom mode
    status = InvokeDriverEscape(&adapterInfoGdiName, (sizeof(DD_CUI_ESC_GET_SET_CUSTOM_MODE_ARGS)), escapeOpCode, pCustomModeArgs);

    // This is to get the resolution of the custom mode added
    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_CUI_ESC_GET_SET_CUSTOM_MODE_ARGS) + (sizeof(DD_CUI_ESC_CUSTOM_SRC_MODE) * pCustomModeArgs->NumOfModes), escapeOpCode,
                                pCustomModeArgs);

    return status;
}
/**--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*
 * @brief           YangraAddCustomMode (Exposed API)
 * Description      This function has implementation to add Custom mode
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       hzRes (ULONG - Horizontal Resolution of the mode)
 * @param[In]       vtRes (ULONG - Vertical Resolution of the mode)
 * @return          Return TRUE on success and FALSE on failure
 *---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraAddCustomMode(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG hzRez, _In_ ULONG vtRes)
{
    BOOLEAN                              status             = FALSE;
    DD_CUI_ESC_GET_SET_CUSTOM_MODE_ARGS *pCustomModeArgs    = NULL;
    DD_CUI_ESC_CUSTOM_SRC_MODE *         pSourceMode        = NULL;
    DWORD                                size               = sizeof(DD_CUI_ESC_GET_SET_CUSTOM_MODE_ARGS) + sizeof(DD_CUI_ESC_CUSTOM_SRC_MODE);
    ADAPTER_INFO_GDI_NAME                adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T                  escapeOpCode       = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    pCustomModeArgs = (DD_CUI_ESC_GET_SET_CUSTOM_MODE_ARGS *)malloc(size);
    NULL_PTR_CHECK(pCustomModeArgs);

    ZeroMemory(pCustomModeArgs, size);
    pSourceMode                   = (DD_CUI_ESC_CUSTOM_SRC_MODE *)DD_VOID_PTR_INC(&(pCustomModeArgs->NumOfModes), sizeof(DDU8));
    pCustomModeArgs->CustomModeOp = DD_CUI_ESC_CUSTOM_MODE_ADD_MODES;
    pCustomModeArgs->NumOfModes   = 1;
    pCustomModeArgs->TargetId     = pPanelInfo->targetID;

    pSourceMode->SourceX = (DDU32)hzRez;
    pSourceMode->SourceY = (DDU32)vtRes;

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_CUSTOM_MODES;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pPanelInfo->gfxAdapter.deviceID,
             pPanelInfo->gfxAdapter.busDeviceID, pPanelInfo->gfxAdapter.deviceInstanceID, pPanelInfo->gfxAdapter.gfxIndex, pPanelInfo->gfxAdapter.vendorID,
             pPanelInfo->gfxAdapter.isActive);
    status = InvokeDriverEscape(&adapterInfoGdiName, size, escapeOpCode, pCustomModeArgs);
    if (FALSE == status)
    {
        ERROR_LOG(" YangraAddCustomMode hzRez : %lu vtRes :%lu", pSourceMode->SourceX, pSourceMode->SourceY);
    }
    free(pCustomModeArgs);

    return status;
}

/**--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*
 * @brief           YangraApplyCSC (Exposed API)
 * Description      This function has implementation to add Linear\Non-Linear CSC
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       cscOperation (INT - Get\Set CSC Escape Call)
 * @param[In]       matrixType (INT - Linear\Non-Linear CSC Matrix type)
 * @param[In]       pColorPipeMatrixParams (Pointer to CSC_PARAMS structure)
 * @return          Return TRUE on success and FALSE on failure
 *---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*/

BOOLEAN YangraApplyCSC(_In_ PANEL_INFO *pPanelInfo, _In_ INT cscOperation, _In_ INT matrixType, _In_ CSC_PARAMS pColorPipeMatrixParams)
{
    ADAPTER_INFO_GDI_NAME           adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T             escapeOpCode       = { 0 };
    PDD_CUI_ESC_COLOR_MATRIX_CONFIG pcolorMatrixConfig = NULL;
    BOOLEAN                         status             = FALSE;
    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    pcolorMatrixConfig = (DD_CUI_ESC_COLOR_MATRIX_CONFIG *)malloc(sizeof(DD_CUI_ESC_COLOR_MATRIX_CONFIG));
    NULL_PTR_CHECK(pcolorMatrixConfig);

    ZeroMemory(pcolorMatrixConfig, sizeof(DD_CUI_ESC_COLOR_MATRIX_CONFIG));
    pcolorMatrixConfig->size              = sizeof(DD_CUI_ESC_COLOR_MATRIX_CONFIG);
    pcolorMatrixConfig->operation         = cscOperation;
    pcolorMatrixConfig->targetId          = pPanelInfo->targetID;
    pcolorMatrixConfig->matrixType        = matrixType;
    pcolorMatrixConfig->pipeMatrix.enable = pColorPipeMatrixParams.enable;
    for (int index = 0; index < DD_ESC_COLOR_MATRIX_NUM_COEFFICIENTS; index++)
    {
        pcolorMatrixConfig->pipeMatrix.coefficients[index].value = pColorPipeMatrixParams.coefficients[index];
    }

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_SET_CSC;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_CUI_ESC_COLOR_MATRIX_CONFIG), escapeOpCode, pcolorMatrixConfig);
    free(pcolorMatrixConfig);

    VERIFY_ESCAPE_STATUS(status);
    return TRUE;
}

/**-----------------------------------------------------------------------------------------------------------------------------
 * @brief           YangraI2CAuxRead (Internal API)
 * Description      This function has implementation to Read Remote DPCD Register Value for given offset for Yangra Driver
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[Out]      dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraI2CAuxRead(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[])
{
    BOOLEAN                    adapterStatus      = FALSE;
    GFX_ESCAPE_HEADER_T        escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME      adapterInfoGdiName = { 0 };
    DD_ESC_AUX_I2C_ACCESS_ARGS dpcdArgs           = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);
    VERIFY_IGFX_ADAPTER_STATUS(adapterStatus);

    TARGET_ID targetId = { 0 };
    targetId.Value     = pPanelInfo->targetID;

    dpcdArgs.i2cAuxArgs.operation  = DD_I2C_AUX;
    dpcdArgs.i2cAuxArgs.write      = 0;
    dpcdArgs.i2cAuxArgs.port       = targetId.bitInfo.portType;
    dpcdArgs.i2cAuxArgs.address    = startOffset;
    dpcdArgs.i2cAuxArgs.dataLength = 16;
    ZeroMemory(dpcdArgs.i2cAuxArgs.data, MAX_LUT_AUX_BUFSIZE);

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_AUX_I2C_ACCESS;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_AUX_I2C_ACCESS_ARGS), escapeOpCode, &dpcdArgs));

    for (UINT index = 0; index < dpcdBufferSize; index++)
    {
        dpcdBuffer[index] = dpcdArgs.i2cAuxArgs.data[index];
    }

    return TRUE;
}

/**------------------------------------------------------------------------------------------------------------------------------
 * @brief           YangraDpcdWrite (Internal API)
 * Description      This function has implementation to Write Remote DPCD Register Value for given offset for Yangra Driver
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[In]       dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraI2CAuxWrite(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[])
{
    BOOLEAN                    adapterStatus      = FALSE;
    GFX_ESCAPE_HEADER_T        escapeOpCode       = { 0 };
    ADAPTER_INFO_GDI_NAME      adapterInfoGdiName = { 0 };
    DD_ESC_AUX_I2C_ACCESS_ARGS dpcdArgs           = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    adapterStatus                  = GetAdapterDetails(&adapterInfoGdiName);
    VERIFY_IGFX_ADAPTER_STATUS(adapterStatus);

    TARGET_ID targetId = { 0 };
    targetId.Value     = pPanelInfo->targetID;

    dpcdArgs.i2cAuxArgs.operation  = DD_I2C_AUX;
    dpcdArgs.i2cAuxArgs.write      = 1;
    dpcdArgs.i2cAuxArgs.port       = targetId.bitInfo.portType;
    dpcdArgs.i2cAuxArgs.address    = startOffset;
    dpcdArgs.i2cAuxArgs.dataLength = 16;
    ZeroMemory(dpcdArgs.i2cAuxArgs.data, MAX_LUT_AUX_BUFSIZE);

    for (UINT index = 0; index < dpcdBufferSize; index++)
    {
        dpcdArgs.i2cAuxArgs.data[index] = (UCHAR)dpcdBuffer[index];
    }

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_AUX_I2C_ACCESS;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_AUX_I2C_ACCESS_ARGS), escapeOpCode, &dpcdArgs));

    return TRUE;
}

/**------------------------------------------------------------------------------------------------------------------------------
 * @brief           YangraGetSetCustomScaling (Internal API)
 * Description      This function has implementation to Get or Set Custom Scaling for the given Target ID
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[In]       dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetSetCustomScaling(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_ESC_SET_CUSTOM_SCALING_ARGS *pGetSetargs)
{
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_SET_CUSTOM_SCALING;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_SET_CUSTOM_SCALING_ARGS), escapeOpCode, pGetSetargs));

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief       YangraGetSetPcFeatures (Exposed API)
 * Description  This function has implementation to Query PC feature support & enable status
 * @param[In]   pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[In]   pPowerConservationArgs (Pointer to COM_ESC_POWER_CONSERVATION_ARGS structure)
 * @return      Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetSetPcFeatures(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ COM_ESC_POWER_CONSERVATION_ARGS *pPowerConservationArgs)
{
    BOOLEAN               status             = FALSE;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };

    NULL_PTR_CHECK(pPowerConservationArgs);
    NULL_PTR_CHECK(pAdapterInfo);

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_POWER_CONSERVATION;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    if (pPowerConservationArgs->opType == PWRCONS_OPTYPE_GET)
    {
        EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    else
    {
        EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);
    status = InvokeDriverEscape(&adapterInfoGdiName, sizeof(COM_ESC_POWER_CONSERVATION_ARGS), escapeOpCode, pPowerConservationArgs);
    if (FALSE == status)
    {
        ERROR_LOG("COM_ESC_POWER_CONSERVATION_ARGS opType: %d opStatus : %d", pPowerConservationArgs->opType, pPowerConservationArgs->opStatus);
    }
    return status;
}

/**------------------------------------------------------------------------------------------------------------------------------
 * @brief           YangraGetSetGenlockMode (Internal API)
 * Description      This function has implementation to Get or Set Custom Scaling for the given Target ID
 * @param[In]       pPanelInfo (Pointer to _PANEL_INFO structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------------------------*/
// _In_ UINT numTargetIds, _In_ ULONG targetIds[]
BOOLEAN YangraGetSetGenlockMode(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ BOOLEAN bEnable, _Inout_ DD_CAPI_ESC_GET_SET_GENLOCK_ARGS *pGetSetGenlockArgs)
{
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ULONG                 targetId           = 0;

    NULL_PTR_CHECK(pAdapterInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));
    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    for (UINT index = 0; index < pGetSetGenlockArgs->GenlockTopology.NumGenlockDisplays; index += 1)
        INFO_LOG("Genlock requested for TargetId: %lu. Display has target mode as %lu x %lu @%f", pGetSetGenlockArgs->GenlockTopology.GenlockDisplayInfo[index].TargetId,
                 pGetSetGenlockArgs->GenlockTopology.GenlockModeList[index].pTargetModes->HActive, pGetSetGenlockArgs->GenlockTopology.GenlockModeList[index].pTargetModes->VActive,
                 pGetSetGenlockArgs->GenlockTopology.GenlockModeList[index].pTargetModes->RefreshRate);

    INFO_LOG("Genlock requested with common target mode as %lu x %lu @%f", pGetSetGenlockArgs->GenlockTopology.CommonTargetModeTiming.HActive,
             pGetSetGenlockArgs->GenlockTopology.CommonTargetModeTiming.VActive, pGetSetGenlockArgs->GenlockTopology.CommonTargetModeTiming.RefreshRate);

    pGetSetGenlockArgs->Operation = bEnable ? DD_CAPI_ESC_GENLOCK_OPERATION_ENABLE : DD_CAPI_ESC_GENLOCK_OPERATION_DISABLE;

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_SET_GENLOCK;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    if (pGetSetGenlockArgs->Operation == (DD_CAPI_ESC_GENLOCK_OPERATION_GET_TIMING_DETAILS & DD_CAPI_ESC_GENLOCK_OPERATION_GET_TOPOLOGY))
    {
        EtwGetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    else if (pGetSetGenlockArgs->Operation == (DD_CAPI_ESC_GENLOCK_OPERATION_ENABLE & DD_CAPI_ESC_GENLOCK_OPERATION_DISABLE))
    {
        EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);
    }
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);
    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_CAPI_ESC_GET_SET_GENLOCK_ARGS), escapeOpCode, pGetSetGenlockArgs));

    return TRUE;
}

/**------------------------------------------------------------------------------------------------------------------------------
 * @brief           YangraGetSetVblankTs (Internal API)
 * Description      This function has implementation to Get or Set VBlankTS for the given Target ID
 * @param[In]       pPanelInfo (Pointer to PANEL_INFO structure)
 * @param[In]       pGetSetVblankTsForTarget (Pointer to DD_CAPI_GET_VBLANK_TIMESTAMP_FOR_TARGET structure)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraGetSetVblankTs(_In_ PANEL_INFO *pPanelInfo, _Inout_ DD_CAPI_GET_VBLANK_TIMESTAMP_FOR_TARGET *pGetSetVblankTsForTarget)
{
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    ULONG                 targetId           = 0;

    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);
    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    pGetSetVblankTsForTarget->TargetID = pPanelInfo->targetID;

    INFO_LOG("Genlock VBlank TS requested for target id as %lu ", pGetSetVblankTsForTarget->TargetID);

    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.minorEscapeCode       = DD_ESC_CAPI_GET_SET_VBLANK_TS;
    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;

    EtwSetDriverEscape(escapeOpCode.minorEscapeCode, escapeOpCode.majorEscapeCode, escapeOpCode.minorInterfaceVersion, escapeOpCode.majorInterfaceVersion);

    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pPanelInfo->gfxAdapter.deviceID,
             pPanelInfo->gfxAdapter.busDeviceID, pPanelInfo->gfxAdapter.deviceInstanceID, pPanelInfo->gfxAdapter.gfxIndex, pPanelInfo->gfxAdapter.vendorID,
             pPanelInfo->gfxAdapter.isActive);

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_CAPI_GET_VBLANK_TIMESTAMP_FOR_TARGET), escapeOpCode, pGetSetVblankTsForTarget));
    INFO_LOG("Genlock VBlank TS for TargetId %lu is %lu ", pGetSetVblankTsForTarget->TargetID, pGetSetVblankTsForTarget->VblankTS);
    return TRUE;
}