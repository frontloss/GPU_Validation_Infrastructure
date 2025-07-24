/*------------------------------------------------------------------------------------------------*
 *
 * @file     YangraDisplayEscape.c
 * @brief    This file contains Implementation of Yangra Display Escape APIs - YangraDpcdRead, YangraDpcdWrite
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "DisplayEscape.h"
#include "DriverEscape.h"

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraDpcdRead (Internal API)
 * Description      This function has implementation to Read DPCD Register Value for given offset for Yangra Driver
 * @param[In]       gfxInfo (GFX_INFO - Adapter Information structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[Out]      dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraDpcdRead(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[])
{
    BOOLEAN                    status             = FALSE;
    GFX_ESCAPE_HEADER_T        escapeOpCode       = { 0 };
    DD_ESC_AUX_I2C_ACCESS_ARGS dpcdArgs           = { 0 };

    TARGET_ID targetId = { 0 };
    targetId.Value     = gfxInfo.targetID;

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

    INFO_LOG("Performing DPCD Read over Yangra Driver");
    status = InvokeDriverEscape(gfxInfo, sizeof(DD_ESC_AUX_I2C_ACCESS_ARGS), escapeOpCode, &dpcdArgs);
    if (FALSE == status)
    {
        ERROR_LOG("DPCD Read - Status: %d, port type : %d, Target ID : %lu", dpcdArgs.status, dpcdArgs.i2cAuxArgs.port, targetId.Value);
    }

    for (UINT index = 0; index < dpcdBufferSize; index++)
    {
        dpcdBuffer[index] = dpcdArgs.i2cAuxArgs.data[index];
    }

    return TRUE;
}

/**---------------------------------------------------------------------------------------------------------*
 * @brief           YangraDpcdWrite (Internal API)
 * Description      This function has implementation to Write DPCD Register Value for given offset for Yangra Driver
 * @param[In]       gfxInfo (GFX_INFO - Adapter Information structure)
 * @param[In]       startOffset (ULONG - Address / Offset value in Hex)
 * @param[In]       dpcdBufferSize (UINT - Size of the dpcd buffer)
 * @param[In]       dpcdBuffer (ULONG - Pointer to ULONG)
 * @return          Return TRUE on success and FALSE on failure
 *-----------------------------------------------------------------------------------------------------------*/
BOOLEAN YangraDpcdWrite(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[])
{
    BOOLEAN                    status             = FALSE;
    GFX_ESCAPE_HEADER_T        escapeOpCode       = { 0 };
    DD_ESC_AUX_I2C_ACCESS_ARGS dpcdArgs           = { 0 };

    TARGET_ID targetId = { 0 };
    targetId.Value     = gfxInfo.targetID;

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

    INFO_LOG("Performing DPCD Write over Yangra Driver");
    status = InvokeDriverEscape(gfxInfo, sizeof(DD_ESC_AUX_I2C_ACCESS_ARGS), escapeOpCode, &dpcdArgs);
    if (FALSE == status)
    {
        ERROR_LOG("DPCD Write - Status: %d, port type : %d, Target ID : %lu", dpcdArgs.status, dpcdArgs.i2cAuxArgs.port, targetId.Value);
    }

    return TRUE;
}
