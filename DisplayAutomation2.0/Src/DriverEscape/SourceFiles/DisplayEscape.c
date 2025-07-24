/*------------------------------------------------------------------------------------------------*
 *
 * @file     DisplayEscape.c
 * @brief    This file contains Implementation of Display Escape APIs - GetDriverType, DpcdRead,
 *           GetMiscSystemInfo, GetEdidData, GetDPPHWLUT, SetDPPHWLUT, IsXvYccSupported,
 *           IsYCbCrSupported, ConfigureYCbCr, ConfigureXvYcc, GenerateTdr, DpcdWrite
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "DisplayEscape.h"
#include "DriverEscape.h"

/**---------------------------------------------------------------------------------------------------------*
 * @brief               GetDriverType (Internal API)
 * Description:         This function is used to check whether Yangra driver installed by checking ESC Version through Driver Escape.
 * @param[In]           adapterInfoGdiName (pInternalAdapterInfo of the Adapter)
 * return: DRIVER_TYPE  DRIVER_YANGRA OR DRIVER_LEGACY OR DRIVER_UNKNOWN
 *----------------------------------------------------------------------------------------------------------*/
DRIVER_TYPE GetDriverType(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName)
{
    BOOLEAN                 status        = FALSE;
    GFX_ESCAPE_HEADER_T     escapeOpCode  = { 0 };
    DRIVER_TYPE             driverBranch  = DRIVER_UNKNOWN;
    DD_ESC_GET_VERSION_ARGS escapeVersion = { 0 };

    VERIFY_IGFX_ADAPTER(adapterInfoGdiName.adapterInfo);

    escapeOpCode.minorInterfaceVersion = YANGRA_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = DD_ESC_GET_VERSION;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = YANGRA_ESC_VERSION;

    /* Invoke Yangra driver escape*/
    if (TRUE == InvokeDriverEscape(&adapterInfoGdiName, sizeof(DD_ESC_GET_VERSION_ARGS), escapeOpCode, &escapeVersion))
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
        if (TRUE == InvokeDriverEscape(&adapterInfoGdiName, sizeof(CUI_ESC_QUERY_COMPENSATION_ARGS), escapeOpCode, &queryCurrentConfig))
        {
            driverBranch = LEGACY_DRIVER; // Legacy driver installed
        }
        else
        {
            ERROR_LOG("DriverEscape Failed to Find DriverBranch for gfx_Index:%ls", adapterInfoGdiName.adapterInfo.gfxIndex);
        }
    }
    return driverBranch;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               DpcdRead (Exposed API)
 * Description          This function has implementation to Read DPCD Register Value for given offset
 * @param[In]           pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]           startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]           dpcdBufferSize (INT - Size of the dpcd buffer)
 * @param[Out]          dpcdBuffer (Pointer to ULONG)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN DpcdRead(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[])
{
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;

    NULL_PTR_CHECK(dpcdBuffer);
    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    if (dpcdBufferSize <= 0 || dpcdBufferSize > MAX_LUT_AUX_BUFSIZE)
    {
        ERROR_LOG("Invalid Buffer Size");
        return FALSE;
    }

    // Getting GFX Adapter DriverType - Legacy/ Yangra
    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);

    if (driverBranch == LEGACY_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(LegacyDpcdRead(pPanelInfo, startOffset, dpcdBufferSize, dpcdBuffer));
    }
    else if (driverBranch == YANGRA_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(YangraDpcdRead(pPanelInfo, startOffset, dpcdBufferSize, dpcdBuffer));
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               DpcdWrite (Exposed API)
 * Description          This function has implementation to Write DPCD Register Value for given offset
 * @param[In]           pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]           startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]           dpcdBufferSize (INT - Size of the dpcd buffer)
 * @param[In]           dpcdBuffer (Pointer to ULONG)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN DpcdWrite(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[])
{
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;

    NULL_PTR_CHECK(dpcdBuffer);
    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    if (dpcdBufferSize <= 0 || dpcdBufferSize > MAX_LUT_AUX_BUFSIZE)
    {
        ERROR_LOG("Invalid Buffer Size");
        return FALSE;
    }

    // Getting GFX Adapter DriverType - Legacy/ Yangra
    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);

    if (driverBranch == LEGACY_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(LegacyDpcdWrite(pPanelInfo, startOffset, dpcdBufferSize, dpcdBuffer));
    }
    else if (driverBranch == YANGRA_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(YangraDpcdWrite(pPanelInfo, startOffset, dpcdBufferSize, dpcdBuffer));
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               CfgDxgkPowerComponent (Exposed API)
 * Description          This function has implementation to configure dxgk power componenet
 * @param[In]           pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[In]           active (BOOL - TRUE to configure power component to Active, FALSE to make it Idle)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN CfgDxgkPowerComponent(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ BOOL active)
{
    DRIVER_TYPE                        driverBranch       = DRIVER_UNKNOWN;
    ADAPTER_INFO_GDI_NAME              adapterInfoGdiName = { 0 };
    MISC_ESC_DXGK_POWER_COMPONENT_ARGS dxgkPowerCompArgs  = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    adapterInfoGdiName.adapterID   = pAdapterInfo->adapterLUID;

    INFO_LOG("gfxIndex: %ls LUID: low- %lu, high- %ld  Set dxgk Power Component to '%s' State", pAdapterInfo->gfxIndex, pAdapterInfo->adapterLUID.LowPart,
             pAdapterInfo->adapterLUID.HighPart, (active ? "ACTIVE" : "IDLE"));

    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);

    dxgkPowerCompArgs.active = active;

    if (driverBranch == LEGACY_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(LegacyConfigDxgkPowerComponent(adapterInfoGdiName, &dxgkPowerCompArgs));
    }
    else if (driverBranch == YANGRA_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(YangraConfigDxgkPowerComponent(adapterInfoGdiName, &dxgkPowerCompArgs));
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               GetMiscSystemInfo (Exposed API)
 * Description          This function has implementation to Get Miscellaneous System Information
 * @param[In]           pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[Out]          pMiscSystemInfo (Pointer to _MISC_ESC_GET_SYSTEM_INFO_ARGS structure)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetMiscSystemInfo(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Out_ MISC_ESC_GET_SYSTEM_INFO_ARGS *pMiscSystemInfo)
{
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;

    NULL_PTR_CHECK(pAdapterInfo);
    NULL_PTR_CHECK(pMiscSystemInfo);

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);

    if (driverBranch == LEGACY_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(LegacyGetMiscSystemInfo(adapterInfoGdiName, pMiscSystemInfo));
    }
    else if (driverBranch == YANGRA_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(YangraGetMiscSystemInfo(adapterInfoGdiName, pMiscSystemInfo));
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               GetEdidData (Exposed API)
 * Description          This function has implementation to Get RAW EDID Data of the Display
 * @param[In]           pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[Out]          edidData (BYTE[] - Edid data block output)
 * @param[Out]          pNumEdidBlock (UINT - Pointer to edid block)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetEdidData(_In_ PANEL_INFO *pPanelInfo, _Out_ BYTE edidData[], _Out_ UINT *pNumEdidBlock)
{

    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(edidData);
    NULL_PTR_CHECK(pNumEdidBlock);
    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pPanelInfo->gfxAdapter.deviceID,
             pPanelInfo->gfxAdapter.busDeviceID, pPanelInfo->gfxAdapter.deviceInstanceID, pPanelInfo->gfxAdapter.gfxIndex, pPanelInfo->gfxAdapter.vendorID,
             pPanelInfo->gfxAdapter.isActive);
    if (driverBranch == YANGRA_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(YangraGetEdidData(pPanelInfo, edidData, pNumEdidBlock));
    }
    else if (driverBranch == LEGACY_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(LegacyGetEdidData(pPanelInfo, edidData, pNumEdidBlock));
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           ConvertRGBA8ToRGB10 (Internal)
 * Description      Call to convert RGB8 data to RGB10 data
 * @param[in]       pRGB8 (ULONG - Pointer containing the RGB8 data)
 * @param[in]       depth (ULONG - Depth of the color)
 * @param[in]       pRGB10 (ULONG - Pointer to which the RGB10 data has to be filled)
 * @return          Returns Nothing
 *-----------------------------------------------------------------------------------------------------------*/
VOID ConvertRGBA8ToRGB10(BYTE *pRGB8, ULONG depth, DD_RGB_1010102 *pRGB10)
{
    COLOR_RGBA *RGB8        = (COLOR_RGBA *)pRGB8;
    ULONG       totalValues = depth * depth * depth;

    for (ULONG bIndex = 0; bIndex < depth; bIndex++)
    {
        for (ULONG gIndex = 0; gIndex < depth; gIndex++)
        {
            for (ULONG rIndex = 0; rIndex < depth; rIndex++)
            {
                ULONG rgbIndex = (depth * depth * rIndex) + (depth * gIndex) + bIndex;
                ULONG bgrIndex = (depth * depth * bIndex) + (depth * gIndex) + rIndex;

                if ((rgbIndex < totalValues) && (bgrIndex < totalValues))
                {
                    pRGB10[rgbIndex].Blue  = ((ULONG)RGB8[bgrIndex].Blue) << 2;
                    pRGB10[rgbIndex].Green = ((ULONG)RGB8[bgrIndex].Green) << 2;
                    pRGB10[rgbIndex].Red   = ((ULONG)RGB8[bgrIndex].Red) << 2;
                }
            }
        }
    }
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               GetDPPHWLUT (Exposed API)
 * Description          This function has implementation to find the depth of the color
 * @param[In]           pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[InOut]        pCuiDppHwLutInfo (Pointer to structure _CUI_DPP_HW_LUT_INFO)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetDPPHWLUTN(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ CUI_DPP_HW_LUT_INFO *pCuiDppHwLutInfo)
{
    BOOLEAN               status             = FALSE;
    ULONG                 depth              = 0;
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    NULL_PTR_CHECK(pCuiDppHwLutInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);

    if (driverBranch == YANGRA_DRIVER)
    {
        DD_ESC_SET_3D_LUT_ARGS DppHwLutInfo = { 0 };
        DppHwLutInfo.operation              = DD_COLOR_OPERATION_GET;
        DppHwLutInfo.targetID               = pCuiDppHwLutInfo->displayID;

        status                   = YangraGetSetDPPHWLUT(adapterInfoGdiName, &DppHwLutInfo, &depth);
        pCuiDppHwLutInfo->status = DppHwLutInfo.status;
    }
    else if (driverBranch == LEGACY_DRIVER)
    {
        CUI_ESC_GET_SET_HW_3DLUT_ARGS DppHwLutInfo = { 0 };
        DppHwLutInfo.opType                        = HW_3DLUT_OPTYPE_GET_HW_SUPPORT_INFO;
        DppHwLutInfo.deviceUID                     = pCuiDppHwLutInfo->displayID;

        status = LegacyGetSetDPPHWLUT(adapterInfoGdiName, sizeof(CUI_ESC_GET_SET_HW_3DLUT_ARGS), &DppHwLutInfo);
        depth  = DppHwLutInfo.LUTDepth;
    }
    pCuiDppHwLutInfo->depth = depth;

    VERIFY_ESCAPE_STATUS(status);
    return status;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               SetDPPHWLUT (Exposed API)
 * Description          This function has implementation to Set DPP Hardware LUT data
 * @param[In]           pAdapterInfo (Pointer to _GFX_ADAPTER_INFO structure)
 * @param[In]           pCuiDppHwLutInfo (Pointer to structure _CUI_DPP_HW_LUT_INFO)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN SetDPPHWLUTN(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ CUI_DPP_HW_LUT_INFO *pCuiDppHwLutInfo)
{
    BOOLEAN               status = FALSE;
    ULONG                 dataSize;
    ULONG                 depth;
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    NULL_PTR_CHECK(pCuiDppHwLutInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pAdapterInfo->deviceID, pAdapterInfo->busDeviceID,
             pAdapterInfo->deviceInstanceID, pAdapterInfo->gfxIndex, pAdapterInfo->vendorID, pAdapterInfo->isActive);

    if (driverBranch == YANGRA_DRIVER)
    {
        DD_ESC_SET_3D_LUT_ARGS *pDppHwLutInfo;
        dataSize      = sizeof(ULONG) * DD_COLOR_3DLUT_NUM_SAMPLES;
        pDppHwLutInfo = (DD_ESC_SET_3D_LUT_ARGS *)malloc(sizeof(DD_ESC_SET_3D_LUT_ARGS));
        NULL_PTR_CHECK(pDppHwLutInfo);

        ZeroMemory(pDppHwLutInfo, sizeof(DD_ESC_SET_3D_LUT_ARGS));
        pDppHwLutInfo->operation = DD_COLOR_OPERATION_SET;
        if (APPLY_LUT == pCuiDppHwLutInfo->opType)
            pDppHwLutInfo->enable = TRUE;
        if (DISABLE_LUT == pCuiDppHwLutInfo->opType)
            pDppHwLutInfo->enable = FALSE;

        pDppHwLutInfo->targetID = pCuiDppHwLutInfo->displayID;

        ConvertRGBA8ToRGB10(pCuiDppHwLutInfo->lutData, HWLUT_SAMPLE_SIZE, pDppHwLutInfo->LUTData);

        status = YangraGetSetDPPHWLUT(adapterInfoGdiName, pDppHwLutInfo, &depth);

        pCuiDppHwLutInfo->status = pDppHwLutInfo->status;
        free(pDppHwLutInfo);
        pDppHwLutInfo = NULL;
    }
    else if (driverBranch == LEGACY_DRIVER)
    {
        CUI_ESC_GET_SET_HW_3DLUT_ARGS *pDppHwLutInfo  = NULL;
        INT                            escapeDataSize = 0;
        depth                                         = pCuiDppHwLutInfo->depth;
        dataSize                                      = sizeof(ULONG) * depth * depth * depth; // For Disable_LUT dataSize = 0 since Depth will be 0
        escapeDataSize                                = sizeof(CUI_ESC_GET_SET_HW_3DLUT_ARGS) + dataSize;
        pDppHwLutInfo                                 = (CUI_ESC_GET_SET_HW_3DLUT_ARGS *)malloc(sizeof(CUI_ESC_GET_SET_HW_3DLUT_ARGS) + dataSize);
        NULL_PTR_CHECK(pDppHwLutInfo);

        ZeroMemory(pDppHwLutInfo, escapeDataSize);

        if (APPLY_LUT == pCuiDppHwLutInfo->opType)
        {
            pDppHwLutInfo->opType = HW_3DLUT_OPTYPE_ENABLE;
        }
        if (DISABLE_LUT == pCuiDppHwLutInfo->opType)
        {
            pDppHwLutInfo->opType = HW_3DLUT_OPTYPE_DISABLE;
        }
        pDppHwLutInfo->deviceUID = pCuiDppHwLutInfo->displayID;
        pDppHwLutInfo->LUTDepth  = pCuiDppHwLutInfo->depth;

        ConvertRGBA8ToRGB10(pCuiDppHwLutInfo->lutData, depth, (DD_RGB_1010102 *)((CUI_ESC_GET_SET_HW_3DLUT_ARGS *)pDppHwLutInfo + 1));

        status = LegacyGetSetDPPHWLUT(adapterInfoGdiName, escapeDataSize, pDppHwLutInfo);
        free(pDppHwLutInfo);
        pDppHwLutInfo = NULL;
    }

    VERIFY_ESCAPE_STATUS(status);
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               IsXvYccSupported (Exposed API)
 * Description          This function has implementation to find the Display is xvYCC Supported or Not
 * @param[In]           pPanelInfo (Pointer to _PANEL_INFO structure)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN IsXvYccSupported(_In_ PANEL_INFO *pPanelInfo)
{
    BOOLEAN               xvyccStatus        = FALSE;
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pPanelInfo);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pPanelInfo->gfxAdapter.deviceID,
             pPanelInfo->gfxAdapter.busDeviceID, pPanelInfo->gfxAdapter.deviceInstanceID, pPanelInfo->gfxAdapter.gfxIndex, pPanelInfo->gfxAdapter.vendorID,
             pPanelInfo->gfxAdapter.isActive);
    if (driverBranch == YANGRA_DRIVER)
    {
        /* Yangra Driver dose not support XvYcc */
        WARNING_LOG("Yangra Driver does not support XvYcc");
        xvyccStatus = FALSE;
    }
    else if (driverBranch == LEGACY_DRIVER)
    {
        CUI_ESC_GET_SET_COLORSPACE_ARGS colorSpaceArgs = { 0 };
        colorSpaceArgs.opType                          = SB_OPTYPE_GET;
        colorSpaceArgs.displayUID                      = pPanelInfo->targetID;
        colorSpaceArgs.enablePreference                = FALSE;

        VERIFY_ESCAPE_STATUS(LegacyGetColorimetryInfo(adapterInfoGdiName, &colorSpaceArgs));
        xvyccStatus = (CUI_ESC_SUPPORTS_COLORSPACE_xvYCC == colorSpaceArgs.colorspace);
    }
    return xvyccStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               IsYCbCrSupported (Exposed API)
 * Description          This function has implementation to find the Display is YcbCr Supported or Not
 * @param[In]           pPanelInfo (Pointer to _PANEL_INFO structure)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN IsYCbCrSupported(_In_ PANEL_INFO *pPanelInfo)
{
    BOOLEAN               ycbcrStatus        = FALSE;
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pPanelInfo);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pPanelInfo->gfxAdapter.deviceID,
             pPanelInfo->gfxAdapter.busDeviceID, pPanelInfo->gfxAdapter.deviceInstanceID, pPanelInfo->gfxAdapter.gfxIndex, pPanelInfo->gfxAdapter.vendorID,
             pPanelInfo->gfxAdapter.isActive);
    if (driverBranch == YANGRA_DRIVER)
    {
        DD_ESC_QUERY_DISPLAY_DETAILS_ARGS queryDisplayDetails = { 0 };
        queryDisplayDetails.targetID                          = pPanelInfo->targetID;

        VERIFY_ESCAPE_STATUS(YangraGetColorimetryInfo(adapterInfoGdiName, &queryDisplayDetails));
        ycbcrStatus = queryDisplayDetails.dispFtrSupport.yCbCrSupport;
    }
    else if (driverBranch == LEGACY_DRIVER)
    {
        CUI_ESC_GET_SET_COLORSPACE_ARGS colorSpaceArgs = { 0 };
        colorSpaceArgs.opType                          = SB_OPTYPE_GET;
        colorSpaceArgs.displayUID                      = pPanelInfo->targetID;
        colorSpaceArgs.enablePreference                = FALSE;

        VERIFY_ESCAPE_STATUS(LegacyGetColorimetryInfo(adapterInfoGdiName, &colorSpaceArgs));
        ycbcrStatus = (CUI_ESC_SUPPORTS_COLORSPACE_YCbCr == colorSpaceArgs.colorspace);
    }
    return ycbcrStatus;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               ConfigureYCbCr (Exposed API)
 * Description          This function has implementation to Configure YCbCr feature on the display
 * @param[In]           pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]           isEnable (BOOLEAN - To enable or disable YCbCr based on this flag)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN ConfigureYCbCr(_In_ PANEL_INFO *pPanelInfo, _In_ BOOLEAN isEnable, _In_ INT color_model)
{
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pPanelInfo);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pPanelInfo->gfxAdapter.deviceID,
             pPanelInfo->gfxAdapter.busDeviceID, pPanelInfo->gfxAdapter.deviceInstanceID, pPanelInfo->gfxAdapter.gfxIndex, pPanelInfo->gfxAdapter.vendorID,
             pPanelInfo->gfxAdapter.isActive);
    if (driverBranch == YANGRA_DRIVER)
    {
        DD_ESC_GET_SET_COLOR_MODEL_ARGS colorModelArgs = { 0 };
        colorModelArgs.targetID                        = pPanelInfo->targetID;
        colorModelArgs.operation                       = DD_COLOR_OPERATION_SET;

        if (isEnable)
        {
            colorModelArgs.colorModel = color_model;
        }
        else
        {
            colorModelArgs.colorModel = DD_COLOR_MODEL_RGB;
        }

        VERIFY_ESCAPE_STATUS(YangraSetColorimetryInfo(adapterInfoGdiName, colorModelArgs));
    }
    else if (driverBranch == LEGACY_DRIVER)
    {
        CUI_ESC_GET_SET_COLORSPACE_ARGS colorSpaceArgs = { 0 };
        colorSpaceArgs.opType                          = SB_OPTYPE_GET;
        colorSpaceArgs.displayUID                      = pPanelInfo->targetID;
        colorSpaceArgs.enablePreference                = FALSE;

        VERIFY_ESCAPE_STATUS(LegacyGetColorimetryInfo(adapterInfoGdiName, &colorSpaceArgs));

        colorSpaceArgs.opType           = SB_OPTYPE_SET;
        colorSpaceArgs.enablePreference = isEnable;

        VERIFY_ESCAPE_STATUS(LegacySetColorimetryInfo(adapterInfoGdiName, &colorSpaceArgs));
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               ConfigureXvYcc (Exposed API)
 * Description          This function has implementation to Configure xvYCC feature on the display
 * @param[In]           pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]           isEnable (BOOLEAN - To enable or disable YCbCr based on this flag)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN ConfigureXvYcc(_In_ PANEL_INFO *pPanelInfo, _In_ BOOLEAN isEnable)
{
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pPanelInfo);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pPanelInfo->gfxAdapter.deviceID,
             pPanelInfo->gfxAdapter.busDeviceID, pPanelInfo->gfxAdapter.deviceInstanceID, pPanelInfo->gfxAdapter.gfxIndex, pPanelInfo->gfxAdapter.vendorID,
             pPanelInfo->gfxAdapter.isActive);
    if (driverBranch == YANGRA_DRIVER)
    {
        WARNING_LOG("Yangra Driver does not support XvYcc Feature");
        return FALSE;
    }
    else if (driverBranch == LEGACY_DRIVER)
    {
        CUI_ESC_GET_SET_COLORSPACE_ARGS colorSpaceArgs = { 0 };
        colorSpaceArgs.opType                          = SB_OPTYPE_GET;
        colorSpaceArgs.displayUID                      = pPanelInfo->targetID;
        colorSpaceArgs.enablePreference                = FALSE;

        VERIFY_ESCAPE_STATUS(LegacyGetColorimetryInfo(adapterInfoGdiName, &colorSpaceArgs));

        colorSpaceArgs.opType           = SB_OPTYPE_SET;
        colorSpaceArgs.enablePreference = isEnable;

        VERIFY_ESCAPE_STATUS(LegacySetColorimetryInfo(adapterInfoGdiName, &colorSpaceArgs));
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               GetSetOutputFormat (Exposed API)
 * Description          This function has implementation for get and set the BPC and Encoding
 * @param[In]       	pPanelInfo (Pointer to _PANEL_INFO structure)
 * @param[In]       	pSetOutputFormatArgs (Pointer to structure IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GetSetOutputFormat(_In_ PANEL_INFO *pPanelInfo, _Inout_ IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT *pGetSetOutputFormat)
{
    BOOLEAN               status             = FALSE;
    DRIVER_TYPE           driverBranch       = DRIVER_UNKNOWN;
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pGetSetOutputFormat);
    NULL_PTR_CHECK(pPanelInfo);
    VERIFY_IGFX_ADAPTER(pPanelInfo->gfxAdapter);

    adapterInfoGdiName.adapterInfo = pPanelInfo->gfxAdapter;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    driverBranch = GetDriverType(adapterInfoGdiName);
    VERIFY_DRIVER_TYPE(driverBranch);
    INFO_LOG("AdapterInfo DeviceID :%ls BusDeviceID : %ls DeviceInstanceID :%ls gfxIndex :%ls VendorID :%ls IsActive : %d", pPanelInfo->gfxAdapter.deviceID,
             pPanelInfo->gfxAdapter.busDeviceID, pPanelInfo->gfxAdapter.deviceInstanceID, pPanelInfo->gfxAdapter.gfxIndex, pPanelInfo->gfxAdapter.vendorID,
             pPanelInfo->gfxAdapter.isActive);

    if (driverBranch == LEGACY_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(LegacyGetSetOutputFormat(pPanelInfo, pGetSetOutputFormat));
    }
    else if (driverBranch == YANGRA_DRIVER)
    {
        VERIFY_ESCAPE_STATUS(YangraGetSetOutputFormat(pPanelInfo, pGetSetOutputFormat));
    }
    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief               GenerateTdr (Exposed API)
 * Description          This function has implementation to Generate TDR
 * @param[In]           pAdapterInfo (Pointer to GFX_ADAPTER_INFO structure)
 * @param[In]           displayTdr (BOOLEAN - To specify VSYNC TDR or KMD TDR)
 * @return BOOLEAN      Returns TRUE on Success else FALSE on Failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN GenerateTdr(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ BOOLEAN displayTdr)
{
    ADAPTER_INFO_GDI_NAME adapterInfoGdiName = { 0 };

    NULL_PTR_CHECK(pAdapterInfo);
    VERIFY_IGFX_ADAPTER((*pAdapterInfo));

    adapterInfoGdiName.adapterInfo = *pAdapterInfo;
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));
    VERIFY_ESCAPE_STATUS(TdrDriverEscape(&adapterInfoGdiName, TRUE));
    return TRUE;
}
