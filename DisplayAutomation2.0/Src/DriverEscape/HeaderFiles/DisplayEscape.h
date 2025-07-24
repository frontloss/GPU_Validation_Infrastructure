/*------------------------------------------------------------------------------------------------*
 *
 * @file     DisplayEscape.h
 * @brief    This file contains Implementation of DpcdRead, GetMiscSystemInfo, GetEdidData,
 *           GetDPPHWLUT, SetDPPHWLUT, IsXvYccSupported, IsYCbCrSupported, ConfigureYCbCr,
 *           ConfigureXvYcc, GenerateTdr, LegacyGetSupportedScaling, LegacyGetTargetTimings, LegacyGetSetOutputFormat,
 *           YangraInvokeCollage, YangraQueryModeTable, YangraAlsAggressivenessLevelOverride,
 *           YangraGetSetVrr, YangraPlugUnplugWBDevice, YangraQueryWB, YangraDumpWBBuffer, YangraGetSetOutputFormat, DpcdWrite
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "CommonInclude.h"
#include "LegacyDisplayEscape.h"
#include "YangraDisplayEscape.h"

typedef enum _DPP_HW_LUT_OPTYPE
{
    UNKNOWN_LUT_TYPE,
    APPLY_LUT,
    DISABLE_LUT,
    MAX_LUT_TYPE
} DPP_HW_LUT_OPTYPE;

#pragma pack(1)

typedef struct _CUI_DPP_HW_LUT_INFO
{
    DWORD                 displayID;
    DPP_HW_LUT_OPTYPE     opType;
    ULONG                 depth;
    BYTE                  lutData[MAX_LUT_DATA];
    DD_COLOR_3DLUT_STATUS status;
} CUI_DPP_HW_LUT_INFO, *PCUI_DPP_HW_LUT_INFO;

#pragma pack()

/* Legacy Escape Call */
CDLL_EXPORT BOOLEAN LegacyGetSupportedScaling(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ UINT32 targetID, _In_ CUI_ESC_MODE_INFO modeInfo, _Out_ USHORT *pSupportedScaling);
CDLL_EXPORT BOOLEAN LegacyGetTargetTimings(_In_ PANEL_INFO *pPanelInfo, _Inout_ CUI_ESC_CONVERT_RR_RATIONAL_ARGS *pConvertRRrational);
CDLL_EXPORT BOOLEAN LegacyGetCurrentConfig(_In_ PANEL_INFO *pPanelInfo, _Inout_ CUI_ESC_QUERY_COMPENSATION_ARGS *pCompensation);

/* Legacy & Yangra Escape Call*/
CDLL_EXPORT BOOLEAN DpcdRead(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[]);
CDLL_EXPORT BOOLEAN DpcdWrite(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[]);
CDLL_EXPORT BOOLEAN CfgDxgkPowerComponent(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ BOOL active);
CDLL_EXPORT BOOLEAN GetMiscSystemInfo(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Out_ MISC_ESC_GET_SYSTEM_INFO_ARGS *pMiscSystemInfo);
CDLL_EXPORT BOOLEAN GetEdidData(_In_ PANEL_INFO *pPanelInfo, _Out_ BYTE edidData[], _Out_ UINT *pNumEdidBlock);
CDLL_EXPORT BOOLEAN GetDPPHWLUTN(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ CUI_DPP_HW_LUT_INFO *pCuiDppHwLutInfo);
CDLL_EXPORT BOOLEAN SetDPPHWLUTN(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ CUI_DPP_HW_LUT_INFO *pCuiDppHwLutInfo);
CDLL_EXPORT BOOLEAN IsXvYccSupported(_In_ PANEL_INFO *pPanelInfo);
CDLL_EXPORT BOOLEAN IsYCbCrSupported(_In_ PANEL_INFO *pPanelInfo);
CDLL_EXPORT BOOLEAN ConfigureYCbCr(_In_ PANEL_INFO *pPanelInfo, _In_ BOOLEAN isEnable, _In_ INT color_model);
CDLL_EXPORT BOOLEAN ConfigureXvYcc(_In_ PANEL_INFO *pPanelInfo, _In_ BOOLEAN isEnable);
CDLL_EXPORT BOOLEAN GetSetOutputFormat(_In_ PANEL_INFO *pPanelInfo, _Inout_ IGCC_GET_SET_OVERRIDE_OUTPUTFORMAT *pGetSetOutputFormat);
CDLL_EXPORT BOOLEAN GenerateTdr(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ BOOLEAN displayTdr);

/* Yangra Escape Call */
CDLL_EXPORT BOOLEAN YangraInvokeCollage(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_CUI_ESC_GET_SET_COLLAGE_MODE_ARGS *pConfigurationInfo);
CDLL_EXPORT BOOLEAN YangraQueryModeTable(_In_ PANEL_INFO *pPanelInfo, _In_ DD_ESC_QUERY_MODE_TABLE_ARGS *pSourceAndTargetModeTable);
CDLL_EXPORT BOOLEAN YangraAlsAggressivenessLevelOverride(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ BOOL luxOperation, _In_ BOOL aggressivenessOperation, _In_ INT lux,
                                                         _In_ INT aggressivenessLevel);
CDLL_EXPORT BOOLEAN YangraGetSetVrr(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_CUI_ESC_GET_SET_VRR_ARGS *pGetSetVrrArgs);
CDLL_EXPORT BOOLEAN YangraPlugUnplugWBDevice(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ DD_ESC_WRITEBACK_HPD wbHpdArgs, _In_ CHAR *filePath);
CDLL_EXPORT BOOLEAN YangraQueryWB(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_WRITEBACK_QUERY_ARGS *pWbQueryArgs);
CDLL_EXPORT BOOLEAN YangraDumpWBBuffer(_In_ PANEL_INFO *pPanelInfo, _In_ UINT instance, _Inout_ DD_WB_BUFFER_INFO *pWbBufferInfo, _In_ UINT imageBpc);
CDLL_EXPORT BOOLEAN YangraGetSetQuantisationRange(_In_ PANEL_INFO *pPanelInfo, _Inout_ DD_CUI_ESC_GET_SET_CUSTOM_AVI_INFO_FRAME_ARGS *avi_quantisation_struct);
CDLL_EXPORT BOOLEAN YangraGetSetCfps(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_CUI_ESC_GET_SET_CAPPED_FPS_ARGS *pGetSetCappedFpsArgs);
CDLL_EXPORT BOOLEAN YangraGetSetNNScaling(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_CUI_ESC_GET_SET_NN_ARGS *pGetSetargs);
CDLL_EXPORT BOOLEAN YangraGetCustomMode(_In_ PANEL_INFO *pPanelInfo, _Inout_ DD_CUI_ESC_GET_SET_CUSTOM_MODE_ARGS *pCustomModeArgs);
CDLL_EXPORT BOOLEAN YangraAddCustomMode(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG HzRes, _In_ ULONG VtRes);
CDLL_EXPORT BOOLEAN YangraApplyCSC(_In_ PANEL_INFO *pPanelInfo, _In_ INT cscOperation, _In_ INT matrixType, _In_ CSC_PARAMS pColorPipeMatrixParams);
CDLL_EXPORT BOOLEAN YangraI2CAuxRead(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _Out_ ULONG dpcdBuffer[]);
CDLL_EXPORT BOOLEAN YangraI2CAuxWrite(_In_ PANEL_INFO *pPanelInfo, _In_ ULONG startOffset, _In_ UINT dpcdBufferSize, _In_ ULONG dpcdBuffer[]);
CDLL_EXPORT BOOLEAN YangraGetSetCustomScaling(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ DD_ESC_SET_CUSTOM_SCALING_ARGS *pGetSetargs);
CDLL_EXPORT BOOLEAN YangraGetSetPcFeatures(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _Inout_ COM_ESC_POWER_CONSERVATION_ARGS *pPowerConservationArgs);
CDLL_EXPORT BOOLEAN YangraGetSetGenlockMode(_In_ GFX_ADAPTER_INFO *pAdapterInfo, _In_ BOOLEAN bEnable, _Inout_ DD_CAPI_ESC_GET_SET_GENLOCK_ARGS *pGetSetGenlockArgs);
CDLL_EXPORT BOOLEAN YangraGetSetVblankTs(_In_ PANEL_INFO *pPanelInfo, _Inout_ DD_CAPI_GET_VBLANK_TIMESTAMP_FOR_TARGET *pGetSetVblankTsForTarget);
