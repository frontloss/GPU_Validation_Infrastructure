/*------------------------------------------------------------------------------------------------*
 *
 * @file     LegacyDisplayEscape.c
 * @brief    This file contains Implementation of Legacy Display Escape APIs - LegacyDpcdRead, LegacyDpcdWrite
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "DisplayEscape.h"
#include "DriverEscape.h"

/**---------------------------------------------------------------------------------------------------------*
 * @brief           LegacyDpcdRead (Internal API)
 * Description      This function has implementation to Read DPCD Register Value for given offset for Legacy Driver
 * @param[In]       gfxInfo (GFX_INFO - Adapter Information structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[Out]      dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyDpcdRead(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[])
{
    BOOLEAN               status             = FALSE;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    SB_AUXACCESS_ARGS     dpcdArgs           = { 0 };

    dpcdArgs.portType    = SB_DP_PORT;
    dpcdArgs.usePortType = SB_DP_PORTNUMBER;
    dpcdArgs.command     = SB_DP_READ;
    dpcdArgs.address     = startOffset;
    dpcdArgs.deviceUID   = gfxInfo.targetID;
    dpcdArgs.size        = SB_DATA_SIZE;

    ZeroMemory(dpcdArgs.data, MAX_LUT_AUX_BUFSIZE);

    escapeOpCode.minorInterfaceVersion = LEGACY_ESC_FILE_VERSION;
    escapeOpCode.minorEscapeCode       = SB_ESC_AUX_ACCESS;
    escapeOpCode.majorEscapeCode       = GFX_ESCAPE_DISPLAY_CONTROL;
    escapeOpCode.majorInterfaceVersion = LEGACY_ESC_VERSION;

    INFO_LOG("Performing DPCD Read over Legacy Driver");
    status = InvokeDriverEscape(gfxInfo, sizeof(SB_AUXACCESS_ARGS), escapeOpCode, &dpcdArgs);
    if (FALSE == status)
    {
        ERROR_LOG("DPCD Read - Status: %d, port type : %d, Target ID : %lu", dpcdArgs.eSBAuxErrorType, dpcdArgs.portType, dpcdArgs.deviceUID);
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
 * @param[In]       gfxInfo (GFX_INFO - Adapter Information structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[In]       dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN LegacyDpcdWrite(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[])
{
    BOOLEAN               status             = FALSE;
    GFX_ESCAPE_HEADER_T   escapeOpCode       = { 0 };
    SB_AUXACCESS_ARGS     dpcdArgs           = { 0 };

    dpcdArgs.portType    = SB_DP_PORT;
    dpcdArgs.usePortType = SB_DP_PORTNUMBER;
    dpcdArgs.command     = SB_DP_WRITE;
    dpcdArgs.address     = startOffset;
    dpcdArgs.deviceUID   = gfxInfo.targetID;
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

    INFO_LOG("Performing DPCD Write over Legacy Driver");
    status = InvokeDriverEscape(gfxInfo, sizeof(SB_AUXACCESS_ARGS), escapeOpCode, &dpcdArgs);
    if (FALSE == status)
    {
        ERROR_LOG("DPCD Write - Status: %d, port type : %d, Target ID : %lu", dpcdArgs.eSBAuxErrorType, dpcdArgs.portType, dpcdArgs.deviceUID);
    }

    return status;
}
