/*------------------------------------------------------------------------------------------------*
 *
 * @file     DisplayEscape.h
 * @brief    This file contains Implementation of DpcdRead, DpcdWrite
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "LegacyDisplayEscape.h"
#include "YangraDisplayEscape.h"

VOID PrintDisplayInfo(CHAR *pTableName, UINT32 numPathArrayElements, DISPLAYCONFIG_PATH_INFO *pPathInfoArray, UINT32 numModeInfoArrayElements, DISPLAYCONFIG_MODE_INFO *pModeInfoArray);
CDLL_EXPORT BOOLEAN QueryAdapterDetails(GFX_INFO_ARR *gfxArr);

/* Driver Escape Call*/
CDLL_EXPORT BOOLEAN DpcdRead(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[]);
CDLL_EXPORT BOOLEAN DpcdWrite(_In_ GFX_INFO gfxInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[]);
