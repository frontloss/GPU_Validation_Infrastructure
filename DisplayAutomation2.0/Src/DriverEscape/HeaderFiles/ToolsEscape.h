/*------------------------------------------------------------------------------------------------*
 *
 * @file     ToolsEscape.h
 * @brief    This file contains Implementation of LegacyQueryDisplayDetails
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#include "CommonInclude.h"
#include "EscapeSharedHeader.h"
#include "LegacyDisplayEscape.h"

typedef enum _ESCAPE_CODES
{
    TOOL_ESC_READ_MMIO_REGISTER,
    TOOL_ESC_DP_APPLET_MISC_FUNC,
    TOOL_ESC_GET_PNM_PIXELCLK_DATA,
    TOOL_ESC_SET_PNM_PIXELCLK_DATA,
    TOOL_ESC_GET_PSR_RESIDENCY_COUNTER,
    TOOL_ESC_QUERY_DISPLAY_DETAILS,
    TOOL_ESC_SIMULATE_DP12_TOPOLOGY,
    TOOL_ESC_ENABLE_FUZZING_OPTIMIZATIONS,
    TOOL_ESC_AUX_ACCESS_DPCD_RW_TOOL,
    MAX_TOOLS_ESCAPES
} ESCAPE_CODE;

#pragma pack(1)

typedef struct _TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS
{
    UINT32       ulDisplayUID;
    DISPLAY_TYPE eType;
    CHAR         ucIndex;
    PORT_TYPES   ePortType;
} TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS;

#pragma pack()

CDLL_EXPORT BOOLEAN LegacyQueryDisplayDetails(_In_ ADAPTER_INFO_GDI_NAME adapterInfoGdiName, TOOL_ESC_QUERY_DISPLAY_DETAILS_ARGS *pQueryDisplayDetails);
