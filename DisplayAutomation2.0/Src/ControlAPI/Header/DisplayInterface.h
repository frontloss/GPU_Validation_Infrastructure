
#pragma once

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include "conio.h"
#include "log.h"
#include <iostream>
#include "Control_API.h"
#include <ze_api.h>
#include <ze_ddi.h>

#define MAX_EDID_BLOCK 8
#define EDID_BLOCK_SIZE 128
#define EXTENSIONS_BYTE 126
#define WB_EDID_BLOCK_SIZE (256)
#define MAX_DISPLAY 4

/* Preprocessor Macros*/
#ifdef _DLL_EXPORT
#define EXPORT_API __declspec(dllexport)
#else
#define EXPORT_API __declspec(dllimport)
#endif

#define NULL_PTR_CHECK(ptr)                         \
    {                                               \
        if (NULL == ptr)                            \
        {                                           \
            ERROR_LOG("NULL Pointer, Exiting !!!"); \
            return FALSE;                           \
        }                                           \
    }

#define VERIFY_ONECORE_API_STATUS(status)                              \
    {                                                                  \
        if (CTL_RESULT_SUCCESS != status)                              \
        {                                                              \
            ERROR_LOG("Control API Failed - Error code 0x%x", status); \
            return FALSE;                                              \
        }                                                              \
    }

#define VERIFY_API_STATUS(status)                                     \
    {                                                                 \
        if (TRUE != status)                                           \
        {                                                             \
            ERROR_LOG("API Status Failed - Error code 0x%x", status); \
            return FALSE;                                             \
        }                                                             \
    }

#define FREE_MEMORY(ptr) \
    {                    \
        if (NULL != ptr) \
        {                \
            free(ptr);   \
            ptr = NULL;  \
        }                \
    }

typedef enum _user_requested_color_blk
{
    HW3DLUT        = 0,
    DGLUT          = 1,
    CSC            = 2,
    GLUT           = 3,
    OCSC           = 4,
    DGLUT_CSC      = 5,
    DGLUT_CSC_GLUT = 6,
    CSC_GLUT       = 7,
    DGLUT_GLUT     = 8,
    ALL            = 9,
    ERROR_BLOCK    = 99

} user_requested_color_blk;

typedef enum _enabled_mode
{
    SDR = 0,
    HDR = 1,
    WCG = 2,
} enabled_mode;

typedef struct _CTRL_API_CONTEXT
{
    ctl_api_handle_t                            apiHandle;
    ctl_pfnInit_t                               pfnCtrlApiInitialize;
    ctl_pfnClose_t                              pfnCtrlApiCleanup;
    ctl_pfnEnumerateDevices_t                   pfnEnumerateDevices;
    ctl_pfnGetDeviceProperties_t                pfnGetDeviceProperties;
    ctl_pfnEnumerateDisplayOutputs_t            pfnEnumerateDisplayOutputs;
    ctl_pfnEnumerateMuxDevices_t                pfnEnumerateMuxDevices;
    ctl_pfnGetMuxProperties_t                   pfnGetMuxProperties;
    ctl_pfnSwitchMux_t                          pfnSwitchMux;
    ctl_pfnGetDisplayProperties_t               pfnGetDisplayProperties;
    ctl_pfnGetAdaperDisplayEncoderProperties_t  pfnGetDisplayEncoderProperties;
    ctl_pfnCheckDriverVersion_t                 pfnCheckDriverVersion;
    ctl_pfnGetZeDevice_t                        pfnGetZeDevice;
    ctl_pfnI2CAccess_t                          pfnI2CAccess;
    ctl_pfnAUXAccess_t                          pfnAUXAccess;
    ctl_pfnGetSharpnessCaps_t                   pfnGetSharpnessCaps;
    ctl_pfnGetCurrentSharpness_t                pfnGetCurrentSharpness;
    ctl_pfnSetCurrentSharpness_t                pfnSetCurrentSharpness;
    ctl_pfnPanelDescriptorAccess_t              pfnPanelDescriptorAccess;
    ctl_pfnPixelTransformationGetConfig_t       pfnPixelTransformationGetConfig;
    ctl_pfnPixelTransformationSetConfig_t       pfnPixelTransformationSetConfig;
    ctl_pfnGetPowerOptimizationCaps_t           pfnGetPowerOptimizationCaps;
    ctl_pfnGetPowerOptimizationSetting_t        pfnGetPowerOptimizationSetting;
    ctl_pfnSetPowerOptimizationSetting_t        pfnSetPowerOptimizationSetting;
    ctl_pfnGetSupportedRetroScalingCapability_t pfnGetSupportedRetroScalingCapability;
    ctl_pfnGetSetRetroScaling_t                 pfnGetSetRetroScaling;
    ctl_pfnGetSupportedScalingCapability_t      pfnGetSupportedScalingCapability;
    ctl_pfnGetCurrentScaling_t                  pfnGetCurrentScaling;
    ctl_pfnSetCurrentScaling_t                  pfnSetCurrentScaling;
    ctl_pfnGetSet3DFeature_t                    pfnGetSet3DFeature;
    ctl_pfnGetLACEConfig_t                      pfnGetLACEConfig;
    ctl_pfnSetLACEConfig_t                      pfnSetLACEConfig;
    ctl_pfnGetIntelArcSyncInfoForMonitor_t      pfnGetIntelArcSyncInfoForMonitor;
    ctl_pfnGetIntelArcSyncProfile_t             pfnGetIntelArcSyncProfile;
    ctl_pfnSetIntelArcSyncProfile_t             pfnSetIntelArcSyncProfile;
    ctl_pfnSetBrightnessSetting_t               pfnSetBrightnessSetting;
    ctl_pfnGetBrightnessSetting_t               pfnGetBrightnessSetting;
    ctl_pfnEdidManagement_t                     pfnEdidManagement;
    ctl_pfnGetSetDisplayGenlock_t               pfnGetSetDisplayGenlock;
    ctl_pfnGetSetCombinedDisplay_t              pfnGetSetCombinedDisplay;
    ctl_pfnGetSetWireFormat_t                   pfnGetSetWireFormat;
} CTRL_API_CONTEXT;

EXPORT_API bool ControlAPIInitialize();
EXPORT_API bool ControlAPICleanup();
EXPORT_API bool ControlAPIGetDisplayProperties(ctl_display_properties_t *displayProperties, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetDisplayEncoderProperties(ctl_adapter_display_encoder_properties_t *displayEncoderProperties, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetDeviceProperties(ctl_device_adapter_properties_t *deviceProperties, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISwitchMux();
EXPORT_API bool ControlAPIGetZeDevice(ze_device_module_properties_t *zeProperties);
EXPORT_API bool ControlAPII2CAccess(ctl_i2c_access_args_t *argsi2c, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIAuxAccess(ctl_aux_access_args_t *auxargs, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetSharpnessCaps(ctl_sharpness_caps_t *getSharpnessCaps, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetCurrentSharpness(ctl_sharpness_settings_t *setSharpness, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetCurrentSharpness(ctl_sharpness_settings_t *getSharpness, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetPanelDescriptorAccess(ctl_panel_descriptor_access_args_t *argsPanelDesc, ctl_panel_descriptor_access_args_t *argsExtBlockPanelDesc,
                                                   PANEL_INFO *pPanelInfo, BYTE edidData[]);
EXPORT_API bool ControlAPIGetPowerCaps(ctl_power_optimization_caps_t *argsGetPowerCaps, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetPSR(ctl_power_optimization_settings_t *argsSetPowerSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetPSR(ctl_power_optimization_settings_t *argsGetPowerSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetUBRR(ctl_power_optimization_settings_t *argsSetPowerSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetUBRR(ctl_power_optimization_settings_t *argsGetPowerSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetGamma(ctl_pixtx_pipe_get_config_t *argsGetConfig, ctl_pixtx_block_config_t *argsLutConfig, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetGamma(ctl_pixtx_pipe_set_config_t *argsSetConfig, ctl_pixtx_block_config_t *blockConfig, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetCSC(ctl_pixtx_pipe_set_config_t *argsSetCSC, ctl_pixtx_pipe_get_config_t *getBlockConfig, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIColorGetCapability(ctl_pixtx_pipe_get_config_t *argsGetConfig, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIRestoreDefault(ctl_pixtx_pipe_set_config_t *argsRestoreDefault, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIHueSaturation(ctl_pixtx_pipe_set_config_t *argsSetCSC, ctl_pixtx_block_config_t *blockConfig, double hueValue, double satValue, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISet3DLUT(ctl_pixtx_pipe_set_config_t *argsSetConfig, ctl_pixtx_block_config_t *blockConfig, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetDPST(ctl_power_optimization_settings_t *argsGetPowerSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetDPST(ctl_power_optimization_settings_t *argsSetPowerSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetScaling(ctl_scaling_settings_t *argsGetScalingSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetScaling(ctl_scaling_settings_t *argsSetScalingSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetSetRetoScaling(ctl_retro_scaling_settings_t *argsRetroScalingSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetRetroScalingCaps(ctl_retro_scaling_caps_t *argsGetScalingCaps, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetColorFeature(ctl_pixtx_pipe_set_config_t *argsSetColorBlks, ctl_pixtx_pipe_get_config_t *blkConfig, PANEL_INFO *pPanelInfo, uint32_t user_req_blk,
                                          uint8_t Enabled_Mode);

EXPORT_API bool ControlAPIGetSetEnduranceGaming(ctl_3d_feature_getset_t *argsGetSet3DFeature, ctl_endurance_gaming_t *argsEnduranceGaming, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetGamingFlipModes(ctl_3d_feature_getset_t *argsGetSet3DFeature, ctl_gaming_flip_mode_flags_t *argsGamingFlipCaps, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetLace(ctl_lace_config_t *argsGetLace, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetLace(ctl_lace_config_t *argsSetLace, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetIntelArcSyncInfo(ctl_intel_arc_sync_monitor_params_t *argsMonitorParams, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetIntelArcSyncProfile(ctl_intel_arc_sync_profile_params_t *argsProfileParams, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetCurrentArcSyncProfile(ctl_intel_arc_sync_profile_t *argsProfileParams, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetBrightnessSetting(ctl_set_brightness_t *argsSetBrightnessSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetBrightnessSetting(ctl_get_brightness_t *argsGetBrightnessSettings, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIEDIDManagement(ctl_edid_management_args_t *argsEDIDManagement, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetSetDisplayGenlock(ctl_genlock_args_t *pGenlockArgs, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetAllDisplayTimingsGenlock(ctl_genlock_args_t *argsGenlock, GFX_ADAPTER_INFO gfxAdapterInfo);
EXPORT_API bool GetTargetDisplayHandle(ctl_display_output_handle_t *htargetDisplay, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetSetWireFormat(ctl_get_set_wire_format_config_t *pGetSetWireFormatSetting, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPISetOutputFormat(ctl_get_set_wire_format_config_t *pGetSetWireFormatSetting, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetOutputFormat(ctl_get_set_wire_format_config_t *pGetSetWireFormatSetting, PANEL_INFO *pPanelInfo);
EXPORT_API bool ControlAPIGetSetCombinedDisplay(ctl_combined_display_args_t *argsCombinedDisplay, MULTI_PANEL_INFO *pMultiPanelInfo);
