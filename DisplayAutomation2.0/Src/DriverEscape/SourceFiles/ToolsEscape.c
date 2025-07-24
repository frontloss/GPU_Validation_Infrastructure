/*------------------------------------------------------------------------------------------------*
 *
 * @file     ToolsEscape.c
 * @brief    This file contains Implementation of Tools Escape API - LegacyQueryDisplayDetails
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "ToolsEscape.h"
#include "DriverEscape.h"

/**---------------------------------------------------------------------------------------------------------*
 * @brief       LegacyQueryDisplayDetails (Exposed API)
 * Description  This function is used query display related details for Legacy Driver.
 * @param       adapterInfoGdiName (Pointer to _ADAPTER_INFO_GDI_NAME structure)
 * @param       pQueryDisplayDetails (Pointer of _TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS structure)
 * @return      Return TRUE on success and FALSE on failure
 *----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyQueryDisplayDetails(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS *pQueryDisplayDetails)
{

    GFX_ESCAPE_HEADER_T escapeOpcode = { 0 };
    BOOLEAN             status       = FALSE;

    NULL_PTR_CHECK(pQueryDisplayDetails);
    VERIFY_IGFX_ADAPTER_STATUS(GetAdapterDetails(&adapterInfoGdiName));

    escapeOpcode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;
    escapeOpcode.minorEscapeCode       = TOOL_ESC_QUERY_DISPLAY_DETAILS;
    escapeOpcode.majorEscapeCode       = GFX_ESCAPE_TOOLS_CONTROL;
    escapeOpcode.majorInterfaceVersion = TOOLS_ESC_VERSION;

    VERIFY_ESCAPE_STATUS(InvokeDriverEscape(&adapterInfoGdiName, sizeof(TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS), escapeOpcode, pQueryDisplayDetails));

    return TRUE;
}
