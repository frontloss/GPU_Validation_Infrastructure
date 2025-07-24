/*------------------------------------------------------------------------------------------------*
 *
 * @file     DriverEscape.h
 * @brief    This header file contains function definition for Internal API's.
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "EscapeSharedHeader.h"

#define GDI32_LIB L"gdi32.dll"

#define GFX_ESCAPE_DISPLAY_CONTROL 1L
#define ESCAPE_DISPLAY_CONTROL 1

#define YANGRA_ESC_GET_VERSION 100

CDLL_EXPORT DRIVER_TYPE GetDriverType(_In_ GFX_INFO gfxInfo);
CDLL_EXPORT BOOLEAN InvokeDriverEscape(_In_ GFX_INFO gfxInfo, _In_ INT escapeDataSize, _In_ GFX_ESCAPE_HEADER_T escapeOpCode, _Out_ void *pEscapeData);
