/*------------------------------------------------------------------------------------------------*
 *
 * @file     Utilities.h
 * @brief    This file contains Implementation of reusable utility functions.
 * @author   Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/

#include "..\Logger\log.h"

// Copy Methods
CDLL_EXPORT errno_t CopyWchar(_Out_ WCHAR dest[], _In_ size_t destSize, _In_ WCHAR src[]);
CDLL_EXPORT errno_t CopyStr(_Out_ CHAR dest[], _In_ size_t destSize, _In_ CHAR src[]);

CDLL_EXPORT UINT GetGfxIndexValue(WCHAR *gfxIndex);

// Comparison Methods
CDLL_EXPORT BOOLEAN CompareAdapterInfo(GFX_ADAPTER_INFO adapter1, GFX_ADAPTER_INFO adapter2);
CDLL_EXPORT BOOLEAN ComparePanelInfo(PANEL_INFO panel1, PANEL_INFO panel2);
